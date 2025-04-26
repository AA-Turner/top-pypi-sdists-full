#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from datarobot.utils import camelize


def exclude_if(
    field_name: str, field_value: Any, if_matches: Optional[List[Any]] | None = None
) -> Dict[str, Any]:
    """
    Several API fields are optional but do not accept blank or empty values.
    This function returns a dict to use with update() to construct an API payload.
    If the field value matches any value in drop_if[], it returns {}, so update() has no effect,
    and the field is not included.

    Parameters
    ----------
    field_name: name of the field. Snake case is OK; this function camelizes
    field_value: value of the field. Enums are converted to strings.
    if_matches: if value matches any in this list, exclude the field. Default is ["", {}, None].

    To intentionally include a null or blank value in the payload, modify drop_if.

    Returns
    -------
    a dict of the value (possibly empty) to update the payload with

    """
    if if_matches is None:
        if_matches = ["", {}, None]
    if field_value in if_matches:
        return {}
    else:
        string_value = field_value
        if isinstance(field_value, Enum):
            string_value = field_value.value
        return {camelize(field_name): string_value}
