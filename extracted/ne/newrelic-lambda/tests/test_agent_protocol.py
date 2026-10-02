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

import os
from pathlib import Path

import newrelic.agent

from newrelic_lambda.agent_protocol import ServerlessModeProtocol, ServerlessModeSession


class Context:
    aws_request_id = "foobar"
    invoked_function_arn = "arn"
    function_name = "foobar"
    function_version = "$LATEST"
    memory_limit_in_mb = 128


def test_named_pipe_write(readable_fifo):
    assert Path("/tmp/newrelic-telemetry").exists()

    if ServerlessModeProtocol is not None:
        # New Relic Agent >=5.16
        protocol = ServerlessModeProtocol(newrelic.agent.global_settings())
        protocol.finalize()
    else:
        # New Relic Agent <5.16
        session = ServerlessModeSession("http://localhost", "foobar", newrelic.agent.global_settings())
        session.finalize()

    assert os.read(readable_fifo, 1024).decode().startswith('[1,"NR_LAMBDA_MONITORING"')
