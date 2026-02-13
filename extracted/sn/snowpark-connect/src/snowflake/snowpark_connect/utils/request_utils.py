#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import uuid
from typing import Any


def get_or_generate_operation_id(request: Any) -> str:
    """Get operation_id from request if present, otherwise generate a new UUID."""
    operation_id = getattr(request, "operation_id", None)
    if operation_id:
        return operation_id
    return str(uuid.uuid4())
