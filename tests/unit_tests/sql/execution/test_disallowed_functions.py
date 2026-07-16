# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Tests for DISALLOWED_SQL_FUNCTIONS enforcement (CVE-2025-55674 follow-up).

The denylist is enforced on the SQL Lab / MCP path in ``SQLExecutor`` and, since
this forward-port, on the chart/data path in
``Database._execute_sql_with_mutation_and_logging``. Both share
``check_disallowed_functions`` so they stay consistent and comment-immune.
"""

import pytest
from flask import current_app
from pytest_mock import MockerFixture

from superset.exceptions import SupersetSecurityException
from superset.models.core import Database
from superset.sql.execution.executor import check_disallowed_functions
from superset.sql.parse import SQLScript


def _script(sql: str) -> SQLScript:
    return SQLScript(sql, "sqlite")


def test_check_disallowed_functions_flags_plain_call(app_context: None) -> None:
    current_app.config["DISALLOWED_SQL_FUNCTIONS"] = {"sqlite": {"upper"}}
    assert check_disallowed_functions(_script("SELECT upper('a')"), "sqlite") == {
        "upper"
    }


def test_check_disallowed_functions_is_comment_immune(app_context: None) -> None:
    # The comment is stripped when the sqlglot AST is re-serialized, so a payload
    # that splits/hides the token cannot slip past the denylist.
    current_app.config["DISALLOWED_SQL_FUNCTIONS"] = {"sqlite": {"upper"}}
    assert check_disallowed_functions(
        _script("SELECT /* c */ upper(/* c */ 'a')"), "sqlite"
    ) == {"upper"}


def test_check_disallowed_functions_allows_other_functions(app_context: None) -> None:
    current_app.config["DISALLOWED_SQL_FUNCTIONS"] = {"sqlite": {"upper"}}
    assert check_disallowed_functions(_script("SELECT lower('a')"), "sqlite") is None


def test_check_disallowed_functions_no_config(app_context: None) -> None:
    current_app.config["DISALLOWED_SQL_FUNCTIONS"] = {}
    assert check_disallowed_functions(_script("SELECT upper('a')"), "sqlite") is None


def test_check_disallowed_functions_other_engine(app_context: None) -> None:
    # A denylist for a different engine must not apply to this one.
    current_app.config["DISALLOWED_SQL_FUNCTIONS"] = {"postgresql": {"upper"}}
    assert check_disallowed_functions(_script("SELECT upper('a')"), "sqlite") is None


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT upper('a') AS x",
        "SELECT /* evade */ upper('a') AS x",
    ],
)
def test_get_df_blocks_disallowed_function(
    sql: str, database: Database, app_context: None, mocker: MockerFixture
) -> None:
    """
    Regression: the chart/data path (Database.get_df -> ... ->
    _execute_sql_with_mutation_and_logging) must enforce the denylist. Before
    this forward-port, 6.1.0 executed the query and returned data instead.
    """
    mocker.patch.dict(
        current_app.config, {"DISALLOWED_SQL_FUNCTIONS": {"sqlite": {"upper"}}}
    )
    # Fail loudly if the guard is bypassed and a connection is opened.
    raw_conn = mocker.patch.object(database, "get_raw_connection")

    with pytest.raises(SupersetSecurityException, match="Disallowed SQL functions"):
        database.get_df(sql)

    raw_conn.assert_not_called()


def test_get_df_allows_permitted_function(
    database: Database, app_context: None, mocker: MockerFixture
) -> None:
    """A query without any denylisted function runs normally on the same path."""
    mocker.patch.dict(
        current_app.config,
        {
            "DISALLOWED_SQL_FUNCTIONS": {"sqlite": {"upper"}},
            "SQL_QUERY_MUTATOR": None,
            "QUERY_LOGGER": None,
        },
    )

    df = database.get_df("SELECT lower('AB') AS x")

    assert df["x"].tolist() == ["ab"]
