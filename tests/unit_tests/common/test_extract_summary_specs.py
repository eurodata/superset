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

from superset.common.query_context_processor import extract_summary_specs


def test_extract_summary_specs_empty_without_show_totals() -> None:
    form_data = {"metrics": [{"aggregate": "SUM", "label": "amount"}]}
    assert extract_summary_specs(form_data) == []


def test_extract_summary_specs_collects_metrics_when_show_totals() -> None:
    form_data = {
        "show_totals": True,
        "metrics": [
            {"aggregate": "SUM", "label": "amount"},
            {"aggregate": "AVG", "label": "rate"},
        ],
    }
    assert extract_summary_specs(form_data) == [
        {"label": "amount", "aggregate": "SUM"},
        {"label": "rate", "aggregate": "AVG"},
    ]


def test_extract_summary_specs_skips_metrics_missing_aggregate() -> None:
    form_data = {
        "show_totals": True,
        "metrics": [
            {"aggregate": "", "label": "amount"},
            {"aggregate": "SUM", "label": "rate"},
        ],
    }
    assert extract_summary_specs(form_data) == [
        {"label": "rate", "aggregate": "SUM"},
    ]


def test_extract_summary_specs_no_metrics() -> None:
    assert extract_summary_specs({"show_totals": True}) == []
