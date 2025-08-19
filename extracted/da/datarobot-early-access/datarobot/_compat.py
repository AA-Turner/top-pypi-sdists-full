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
from __future__ import annotations

try:
    from trafaret import ToInt as Int  # pylint: disable=unused-import
except ImportError:
    from trafaret import Int  # noqa pylint: disable=unused-import


try:
    from trafaret import AnyString as String  # pylint: disable=unused-import
except ImportError:
    from trafaret import String  # noqa pylint: disable=unused-import

try:
    from typing import TypedDict  # noqa pylint: disable=unused-import
except ImportError:
    from typing_extensions import TypedDict  # noqa pylint: disable=unused-import
