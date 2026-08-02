# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest

from omnibase_compat.enums.enum_execution_status import EnumExecutionStatus
from omnibase_compat.enums.enum_message_category import EnumMessageCategory
from omnibase_compat.enums.enum_node_kind import EnumNodeKind


@pytest.mark.unit
def test_message_category_is_stable() -> None:
    assert "event" in EnumMessageCategory._value2member_map_
    assert "command" in EnumMessageCategory._value2member_map_
    assert "intent" in EnumMessageCategory._value2member_map_


@pytest.mark.unit
def test_node_kind_is_stable() -> None:
    assert "compute" in EnumNodeKind._value2member_map_
    assert "effect" in EnumNodeKind._value2member_map_
    assert "orchestrator" in EnumNodeKind._value2member_map_
    assert "reducer" in EnumNodeKind._value2member_map_
    assert "runtime_host" in EnumNodeKind._value2member_map_


@pytest.mark.unit
def test_execution_status_is_stable() -> None:
    assert "success" in EnumExecutionStatus._value2member_map_
    assert "failed" in EnumExecutionStatus._value2member_map_
    assert "pending" in EnumExecutionStatus._value2member_map_
    assert "running" in EnumExecutionStatus._value2member_map_
    assert "completed" in EnumExecutionStatus._value2member_map_
