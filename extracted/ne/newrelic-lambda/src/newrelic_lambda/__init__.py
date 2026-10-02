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

import newrelic_lambda.agent_protocol  # noqa: F401

try:
    from newrelic_lambda._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "unknown"  # pragma: no cover
    __version_tuple__ = (0, 0, 0, "unknown")  # pragma: no cover


__all__ = ("agent_protocol",)
