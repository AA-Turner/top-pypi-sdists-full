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
"""Integration tests for the SecOps CLI parser extension commands."""

import json
import subprocess
import time

import pytest


@pytest.mark.integration
def test_cli_parser_extension_lifecycle(cli_env, common_args):
    """Test the parser extension create, get, activate and delete commands."""

    parser_extension_id = None
    sample_log = (
        '{"actor":{"displayName":"TestUseruser1","alternateId":'
        '"user1@example.com"},"client":{"ipAddress":"192.168.1.100",'
        '"userAgent":{"os":"MacOSX","browser":"SAFARI"}},"displayMessage":'
        '"UserlogintoOkta","eventType":"user.session.start","outcome":'
        '{"result":"SUCCESS"},"published":"2025-07-18T12:17:00.386292Z"}'
    )
    field_extractors = (
        '{"extractors": [{"preconditionPath": "displayMessage"'
        ',"preconditionValue": "User login to Okta","preconditionOp": '
        '"EQUALS","fieldPath": "displayMessage","destinationPath": '
        '"udm.metadata.description"    }],"logFormat": "JSON",'
        '"appendRepeatedFields": true}'
    )
    log_type = "OKTA"

    try:
        # 1. Create parser extension
        create_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "parser-extension",
                "create",
                "--log-type",
                log_type,
                "--log",
                sample_log,
                "--field-extractors",
                field_extractors,
            ]
        )
        create_result = subprocess.run(
            create_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert create_result.returncode == 0

        # Parse the output to get the parser extension ID
        parser_extension_data = json.loads(create_result.stdout)
        assert "name" in parser_extension_data
        parser_extension_id = parser_extension_data["name"].split("/")[-1]
        print(f"Created parser extension with ID: {parser_extension_id}")

        # Wait briefly for the parser extension be fully created
        time.sleep(2)

        # 2. Get parser extension
        get_cmd = (
            [
                "secops",
            ]
            + common_args
            + [
                "parser-extension",
                "get",
                "--log-type",
                log_type,
                "--id",
                parser_extension_id,
            ]
        )
        get_result = subprocess.run(
            get_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert get_result.returncode == 0
        # Parse the output to get the parser extension ID
        parser_extension_get_data = json.loads(get_result.stdout)
        assert "name" in parser_extension_get_data
        assert (
            parser_extension_id
            == parser_extension_get_data["name"].split("/")[-1]
        )

        # 3. List parser extensions
        list_cmd = (
            [
                "secops",
            ]
            + common_args
            + ["parser-extension", "list", "--log-type", log_type]
        )
        list_result = subprocess.run(
            list_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert list_result.returncode == 0
        # Load parser extension list
        parser_extension_list_data = json.loads(list_result.stdout)

        assert "parserExtensions" in parser_extension_list_data
        assert parser_extension_list_data["parserExtensions"]
        # Check if created extension id is in list
        assert any(
            parser_extension_id == parser_extension["name"].split("/")[-1]
            for parser_extension in parser_extension_list_data.get(
                "parserExtensions", []
            )
        )

        # 4. Activate parser extension

        # Checking if parser validation completed
        get_result_validation_check = subprocess.run(
            get_cmd, env=cli_env, capture_output=True, text=True
        )

        # Check that the command executed successfully
        assert get_result_validation_check.returncode == 0
        # Parse the output to get the parser extension ID
        pe_validation_get_data = json.loads(get_result_validation_check.stdout)
        assert "state" in parser_extension_data
        if pe_validation_get_data["state"] == "VALIDATED":
            activate_cmd = (
                [
                    "secops",
                ]
                + common_args
                + [
                    "parser-extension",
                    "activate",
                    "--log-type",
                    log_type,
                    "--id",
                    parser_extension_id,
                ]
            )
            activate_result = subprocess.run(
                activate_cmd, env=cli_env, capture_output=True, text=True
            )

            # Check that the command executed successfully
            assert activate_result.returncode == 0

            # Get Parser extension to check state
            get_activate_result = subprocess.run(
                get_cmd, env=cli_env, capture_output=True, text=True
            )
            # Load parser extension data
            pe_activation_data = json.loads(get_activate_result.stdout)

            assert "name" in pe_activation_data
            assert (
                parser_extension_id == pe_activation_data["name"].split("/")[-1]
            )
            assert pe_activation_data["state"] == "LIVE"

        else:
            print("Parser extension is not validated yet. Skipping Activation")

    finally:
        # Clean up: Delete the parser extension
        if parser_extension_id:
            pe_delete_cmd = (
                [
                    "secops",
                ]
                + common_args
                + [
                    "parser-extension",
                    "delete",
                    "--log-type",
                    log_type,
                    "--id",
                    parser_extension_id,
                ]
            )

            print(f"\nCleaning up parser extension: {parser_extension_id}")
            pe_delete_result = subprocess.run(
                pe_delete_cmd, env=cli_env, capture_output=True, text=True
            )

            # Check that the command executed successfully
            if pe_delete_result.returncode == 0:
                print(f"Successfully cleaned up: {parser_extension_id}")
            else:
                print(f"Failed to clean-up: {pe_delete_result.stderr}")
