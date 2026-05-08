#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""
This module contains compatibility fixes to allow usage of both 1.x and 2.x Trafaret versions
"""
# ruff: noqa

from __future__ import annotations

try:
    from trafaret import ToInt as Int
except ImportError:
    from trafaret import Int

try:
    from trafaret import AnyString as String
except ImportError:
    from trafaret import String

try:
    from typing import TypedDict  # novermin
except ImportError:
    from typing_extensions import TypedDict

try:
    from typing import Literal  # novermin
except ImportError:
    from typing_extensions import Literal  # type: ignore[assignment]
