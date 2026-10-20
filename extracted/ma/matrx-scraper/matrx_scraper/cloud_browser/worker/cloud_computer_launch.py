"""What a Cloud Computer launch carries into the worker process.

Read once at the process boundary (``server.py``, the worker's one environment reader) and
passed down; nothing below the entrypoint reads the environment for these values.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CloudComputerLaunch:
    #: Machine files token minted at launch; empty when the launch carried none (sync stays off).
    files_token: str = ""
    #: The files bridge the token is good for; empty when the launch carried none.
    files_url: str = ""
    #: The process environment the loopback agent daemon starts from (secrets are stripped there).
    process_env: Mapping[str, str] = field(default_factory=dict)
