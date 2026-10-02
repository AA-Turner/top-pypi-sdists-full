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

import pytest


@pytest.fixture(autouse=True, scope="session")
def initialize_agent():
    import newrelic.agent  # noqa: PLC0415

    import newrelic_lambda.agent_protocol  # noqa: PLC0415

    settings = newrelic.agent.global_settings()
    settings.developer_mode = True
    settings.transaction_tracer.transaction_threshold = 0
    newrelic.agent.initialize()
    newrelic.agent.register_application(timeout=10.0)
    yield
    newrelic.agent.shutdown_agent()


@pytest.fixture(scope="session")
def readable_fifo():
    fifo_path = Path("/tmp/newrelic-telemetry")
    if fifo_path.exists():
        fifo_path.unlink()
    os.mkfifo(fifo_path)
    # This will block if we don't pass these flags
    fifo = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
    yield fifo
    os.close(fifo)
