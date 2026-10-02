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

import logging
import os
from pathlib import Path

from newrelic.common.encoding_utils import json_encode, serverless_payload_encode

try:
    from newrelic.core.agent_protocol import ServerlessModeProtocol
except ImportError:
    ServerlessModeProtocol = None

from newrelic.core.data_collector import ServerlessModeSession

NAMED_PIPE_PATH = Path("/tmp/newrelic-telemetry")  # noqa: S108

logger = logging.getLogger(__name__)


def put_payload_cloudwatch(payload):
    try:
        cloudwatch_logging = __import__("newrelic_lambda.cloudwatch_logging", fromlist=["put_log_to_cloudwatch"])
        cloudwatch_logging.put_log_to_cloudwatch(payload)
    except Exception as e:
        print(f"Failed to send payload to CloudWatch: {e}, resorting to print payload.")
        print(payload)


if ServerlessModeProtocol is not None:
    # New Relic Agent >=5.16
    def protocol_finalize(self):
        for key in self.configuration.aws_lambda_metadata:
            if key not in self._metadata:
                self._metadata[key] = self.configuration.aws_lambda_metadata[key]

        data = self.client.finalize()

        payload = {"metadata": self._metadata, "data": data}

        encoded = serverless_payload_encode(payload)
        payload = json_encode((1, "NR_LAMBDA_MONITORING", encoded))

        if NAMED_PIPE_PATH.exists():
            try:
                with NAMED_PIPE_PATH.open("w") as named_pipe:
                    named_pipe.write(payload)
            except OSError:
                logger.exception("Failed to write to named pipe %s", NAMED_PIPE_PATH)
        else:
            if os.getenv("NEW_RELIC_MAX_PAYLOAD", "false").lower() == "true":
                put_payload_cloudwatch(payload)
            else:
                print(payload)

            return payload

    ServerlessModeProtocol.finalize = protocol_finalize

else:
    # New Relic Agent <5.16
    def session_finalize(self):
        encoded = serverless_payload_encode(self.payload)
        payload = json_encode((1, "NR_LAMBDA_MONITORING", encoded))

        if NAMED_PIPE_PATH.exists():
            try:
                with NAMED_PIPE_PATH.open("w") as named_pipe:
                    named_pipe.write(payload)
            except OSError:
                logger.exception("Failed to write to named pipe %s", NAMED_PIPE_PATH)
        else:
            print(payload)

        # Clear data after sending
        self._data.clear()
        return payload

    ServerlessModeSession.finalize = session_finalize
