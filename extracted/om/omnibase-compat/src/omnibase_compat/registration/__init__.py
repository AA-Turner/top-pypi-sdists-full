# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.registration — idempotent registration helpers [OMN-9239]."""

from omnibase_compat.registration.decorator_idempotent_register import idempotent_register

__all__: list[str] = [
    "idempotent_register",
]
