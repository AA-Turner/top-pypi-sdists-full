# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Entry point of the detached telemetry child process.

``_telemetry.record_invocation()`` spawns it as
``python -P <path to this file> '<signal JSON>'``.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __name__ == "__main__":
    # Under -P nothing changes sys.path after startup, so in an editable install
    # the ``google`` namespace package keeps the path a legacy ``*-nspkg.pth``
    # (e.g. google-cloud-aiplatform's) froze to site-packages, and
    # ``google.agents`` isn't found. Adding the directory holding ``google/``
    # changes sys.path, which makes the namespace recompute its path. Appended,
    # so it can't shadow the stdlib.
    sys.path.append(str(Path(__file__).resolve().parents[3]))

    from google.agents.cli._telemetry import run_child

    run_child(sys.argv[1] if len(sys.argv) > 1 else "")
