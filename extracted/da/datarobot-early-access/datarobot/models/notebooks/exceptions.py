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
from __future__ import annotations


class KernelNotAssignedError(Exception):
    """
    Raised when a Codespace notebook does not have a kernel assigned.
    """
