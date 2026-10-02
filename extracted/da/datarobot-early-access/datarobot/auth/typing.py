#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# limitations under the License.
from __future__ import annotations

from typing import Any, Awaitable, Mapping, TypeVar, Union

T = TypeVar("T")
SyncOrAsync = Union[T, Awaitable[T]]

Metadata = Mapping[str, Any]
