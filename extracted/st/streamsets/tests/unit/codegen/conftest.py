#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_data_json():
    """
    Load test data from JSON file and yield its content.
    """
    json_path = Path(__file__).parent.parent / "resources" / "codegen" / "multi_output.json"

    with open(json_path, 'r') as f:
        data = json.load(f)
        yield data


@pytest.fixture(scope="session")
def test_data_json_jdbc():
    """
    Load test data from JSON file and yield its content.
    """
    json_path = Path(__file__).parent.parent / "resources" / "codegen" / "jdbc_with_stream_selector.json"

    with open(json_path, 'r') as f:
        data = json.load(f)
        yield data


@pytest.fixture(scope="session")
def test_data_json_with_event_stage():
    """
    Load test data from JSON file and yield its content.
    """
    json_path = Path(__file__).parent.parent / "resources" / "codegen" / "dev_to_trash_with_event.json"

    with open(json_path, 'r') as f:
        data = json.load(f)
        yield data
