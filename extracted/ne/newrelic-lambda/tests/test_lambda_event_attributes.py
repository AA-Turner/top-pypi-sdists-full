# Copyright 2020 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from pathlib import Path

import pytest

from newrelic_lambda.lambda_handler import detect_event_type, get_attributes_for_event_type

FIXTURE = Path(__file__).parent / "fixtures" / "lambda" / "event_source_info.json"


def _load_tests():
    with FIXTURE.open() as fh:
        js = fh.read()
    return json.loads(js)


def _parametrize_test(fixture):
    # pytest.mark.parametrize expects each test to be a tuple
    return (fixture["expected_attributes"], fixture["event"])


_fixtures = [_parametrize_test(f) for f in _load_tests().values()]


@pytest.mark.parametrize("expected_attributes,event", _fixtures)
def test_labels(expected_attributes, event):
    event_type = detect_event_type(event)
    detected_attributes = get_attributes_for_event_type(event_type, event)

    assert detected_attributes == expected_attributes
