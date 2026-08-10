# SPDX-License-Identifier: MIT
# Copyright (C) 2026 OpenCCU-Loom authors.

"""Constants for openccu-loom-types."""

from typing import Final

VERSION: Final = "0.3.10"

# Contract identity of the daemon build these types were generated
# from. Stamped by scripts/stamp_const.py (run via `make generate`);
# do not edit by hand. A client compares SCHEMA_DIGEST against the
# `schema_digest` field of `GET /api/v1/info`: equality means the
# types match the daemon build exactly; inequality means they were
# generated from a different build — fall back to DAEMON_API_VERSION
# vs `api_version` for compatibility reasoning.
SCHEMA_DIGEST: Final = "sha256:ebff941030e318970ed7ccc0f57231cd45841f5595ee5808e07da6cb3d8fcd44"
DAEMON_API_VERSION: Final = "5.14.0"
