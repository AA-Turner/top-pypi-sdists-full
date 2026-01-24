# Copyright 2025 Google LLC
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
#
"""Integration tests for parser extension management functionality."""

import time

import pytest

from secops.chronicle.parser_extension import ParserExtensionConfig
from secops.client import SecOpsClient

from ..config import CHRONICLE_CONFIG, SERVICE_ACCOUNT_JSON


@pytest.mark.integration
def test_parser_extension_crud_operations():
    """Test create, get, list, activate and delete parser extension."""

    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)
    log_type = "OKTA"  # Using a standard Chronicle log type

    # Test create
    extension = chronicle.create_parser_extension(
        log_type,
        log=(
            '{"actor":{"displayName":"TestUseruser1","alternateId":'
            '"user1@example.com"},"client":{"ipAddress":"192.168.1.100",'
            '"userAgent":{"os":"MacOSX","browser":"SAFARI"}},"displayMessage":'
            '"UserlogintoOkta","eventType":"user.session.start","outcome":'
            '{"result":"SUCCESS"},"published":"2025-07-18T12:17:00.386292Z"}'
        ),
        field_extractors=(
            '{"extractors": [{"preconditionPath": "displayMessage"'
            ',"preconditionValue": "User login to Okta","preconditionOp": '
            '"EQUALS","fieldPath": "displayMessage","destinationPath": '
            '"udm.metadata.description"    }],"logFormat": "JSON",'
            '"appendRepeatedFields": true}'
        ),
    )
    assert extension.get("name"), "Failed to get extension name"
    # Extracting ID from name
    extension_id = extension["name"].split("/")[-1]

    try:
        # Test get
        extension_details = chronicle.get_parser_extension(
            log_type, extension_id
        )
        assert extension_id in extension_details["name"]
        assert "fieldExtractors" in extension_details

        # Test list
        extensions = chronicle.list_parser_extensions(log_type)
        assert "parserExtensions" in extensions
        assert any(
            extension_id in e["name"] for e in extensions["parserExtensions"]
        )

        # Ensure the created extension is validated
        time.sleep(10)

        # Test activate
        if (
            chronicle.get_parser_extension(log_type, extension_id).get("state")
            == "VALIDATED"
        ):

            chronicle.activate_parser_extension(log_type, extension_id)
            # Get extension again to verify activation
            extension_details = chronicle.get_parser_extension(
                log_type, extension_id
            )
            assert extension_details["state"] == "LIVE"
        else:
            print("Parser extension is not validated yet. Skipping Activation")

    finally:
        # Cleanup: Delete the created extension
        chronicle.delete_parser_extension(log_type, extension_id)
        print(f"Cleaned up extension: {extension_id}")
        # Verify deletion
        with pytest.raises(Exception):
            chronicle.get_parser_extension(log_type, extension_id)


@pytest.mark.integration
def test_parser_extension_validation():
    """Test parser extension validation scenarios."""
    client = SecOpsClient(service_account_info=SERVICE_ACCOUNT_JSON)
    chronicle = client.chronicle(**CHRONICLE_CONFIG)
    log_type = "WINDOWS_DNS"
    extension_id = None

    try:
        # Test invalid log type
        with pytest.raises(Exception):
            chronicle.create_parser_extension(
                "INVALID_LOG_TYPE",
                parser_config="filter {}",
            )

        # Test valid creation with multiple configuration types
        # First with parser config
        extension = chronicle.create_parser_extension(
            log_type, parser_config="filter { }"
        )
        extension_id = extension["name"].split("/")[-1]
        assert extension_id

        # Wait till creation completes
        time.sleep(2)

        # Clean up first extension before testing next
        if chronicle.get_parser_extension(log_type, extension_id).get("name"):
            chronicle.delete_parser_extension(log_type, extension_id)
            extension_id = None

        # Then with field extractors
        extension = chronicle.create_parser_extension(
            log_type,
            field_extractors=(
                '{"extractors": [{"preconditionPath": "displayMessage"'
                ',"preconditionValue": "User login to Okta","preconditionOp": '
                '"EQUALS","fieldPath": "displayMessage","destinationPath": '
                '"udm.metadata.description"    }],"logFormat": "JSON",'
                '"appendRepeatedFields": true}'
            ),
        )
        extension_id = extension["name"].split("/")[-1]
        assert extension_id

        # Wait till creation completes
        time.sleep(2)

        # Clean up second extension before testing next
        if chronicle.get_parser_extension(log_type, extension_id).get("name"):
            chronicle.delete_parser_extension(log_type, extension_id)
            extension_id = None

        # Finally with dynamic parsing
        extension = chronicle.create_parser_extension(
            log_type,
            dynamic_parsing={
                "opted_fields": [{"path": "", "sample_value": ""}]
            },
        )
        extension_id = extension["name"].split("/")[-1]
        assert extension_id

        # Wait till creation completes
        time.sleep(2)

    finally:
        # Cleanup
        if extension_id and chronicle.get_parser_extension(
            log_type, extension_id
        ).get("name"):
            chronicle.delete_parser_extension(log_type, extension_id)
            print(f"Cleaned up extension: {extension_id}")
