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

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import SQLAlchemyError

from superset.views.utils import bootstrap_user_data, get_num_tax_offices

# eurodata: uuids the hidden_elements feature keys off of (see views/utils.py)
IST_ERLOESE_UUID = "1e741ee4-6ce1-4533-8877-c122d2c7301b"
KANZLEIVERGLEICH_UUID = "4e70bad9-d29e-45cc-bd17-2ff88a1d06cd"


def _mock_db_with_scalar(scalar_value=None, raise_exc=None):
    """Build a mock `db` whose engine.connect().execute().scalar() is controlled."""
    conn = MagicMock()
    if raise_exc is not None:
        conn.execute.side_effect = raise_exc
    else:
        conn.execute.return_value.scalar.return_value = scalar_value

    @contextmanager
    def connect():
        yield conn

    @contextmanager
    def get_sqla_engine():
        engine = MagicMock()
        engine.connect = connect
        yield engine

    database = MagicMock()
    database.get_sqla_engine = get_sqla_engine

    db = MagicMock()
    db.session.query.return_value.first.return_value = database
    return db


@patch("superset.views.utils.get_user_id", return_value=42)
def test_get_num_tax_offices_returns_scalar(mock_user_id):
    db = _mock_db_with_scalar(scalar_value=3)
    with patch("superset.views.utils.db", db):
        assert get_num_tax_offices() == 3


@patch("superset.views.utils.logger")
@patch("superset.views.utils.get_user_id", return_value=42)
def test_get_num_tax_offices_returns_zero_on_sqlalchemy_error(
    mock_user_id, mock_logger
):
    db = _mock_db_with_scalar(raise_exc=SQLAlchemyError("boom"))
    with patch("superset.views.utils.db", db):
        assert get_num_tax_offices() == 0
    mock_logger.error.assert_called_once()


def _normal_user():
    user = MagicMock()
    user.is_anonymous = False
    user.id = 7
    return user


@patch("superset.views.utils.security_manager")
@patch("superset.views.utils.get_num_tax_offices", return_value=5)
def test_bootstrap_user_data_no_hidden_elements_when_multiple_offices(
    mock_offices, mock_sm
):
    mock_sm.is_guest_user = MagicMock(return_value=False)
    payload = bootstrap_user_data(_normal_user())
    assert payload["hidden_elements"] == []


@patch("superset.views.utils.security_manager")
@patch("superset.views.utils.get_num_tax_offices", return_value=1)
def test_bootstrap_user_data_hides_chart_when_single_office(mock_offices, mock_sm):
    mock_sm.is_guest_user = MagicMock(return_value=False)

    dashboard = MagicMock()
    dashboard.position = {
        "CHART-abc": {
            "type": "CHART",
            "meta": {"uuid": KANZLEIVERGLEICH_UUID},
        },
        "CHART-other": {"type": "CHART", "meta": {"uuid": "unrelated"}},
        "GRID_ID": {"type": "GRID"},
    }

    db = MagicMock()
    db.session.query.return_value.filter_by.return_value.one_or_none.return_value = (
        dashboard
    )
    with patch("superset.views.utils.db", db):
        payload = bootstrap_user_data(_normal_user())
    assert payload["hidden_elements"] == ["CHART-abc"]


@patch("superset.views.utils.security_manager")
@patch("superset.views.utils.get_num_tax_offices", return_value=1)
def test_bootstrap_user_data_no_hidden_elements_when_dashboard_missing(
    mock_offices, mock_sm
):
    mock_sm.is_guest_user = MagicMock(return_value=False)

    db = MagicMock()
    db.session.query.return_value.filter_by.return_value.one_or_none.return_value = None
    with patch("superset.views.utils.db", db):
        payload = bootstrap_user_data(_normal_user())
    assert payload["hidden_elements"] == []
