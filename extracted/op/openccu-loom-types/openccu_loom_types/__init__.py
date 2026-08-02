# SPDX-License-Identifier: MIT
# Copyright (C) 2026 OpenCCU-Loom authors.

"""openccu-loom-types — generated typing bindings for the openccu-loom daemon.

Submodules:

- :mod:`openccu_loom_types.enums` — every enum from `pkg/hmenum`
  (generated from `assets/schemas/enums.json`).
- :mod:`openccu_loom_types.rest` — Pydantic models for the REST
  surface (generated from `assets/openapi.yaml`).
- :mod:`openccu_loom_types.ws` — Pydantic models for the WebSocket
  envelope + push payloads (planned; currently bundled in
  :mod:`openccu_loom_types.rest` until the schema-grouping in
  openapi.yaml stabilises).

See README.md for the regeneration workflow.
"""

from typing import Final

from openccu_loom_types.const import DAEMON_API_VERSION, SCHEMA_DIGEST, VERSION

__version__: Final = VERSION

__all__ = ["DAEMON_API_VERSION", "SCHEMA_DIGEST", "VERSION", "__version__"]

