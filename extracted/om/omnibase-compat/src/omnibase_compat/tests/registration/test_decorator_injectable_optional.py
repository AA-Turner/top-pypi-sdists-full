# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: test scaffolding (local fixture classes), not a migration model
"""Tests for @injectable_optional decorator."""

from __future__ import annotations

from typing import Any

import pytest

from omnibase_compat.registration.decorator_injectable_optional import injectable_optional


@pytest.mark.unit
class TestInjectableOptional:
    def test_attaches_metadata_to_class(self) -> None:
        @injectable_optional("event_bus", reason="optional Kafka publisher")
        class MyNode:
            pass

        assert hasattr(MyNode, "__injectable_optional__")
        meta: Any = MyNode.__injectable_optional__
        assert meta["param_name"] == "event_bus"
        assert meta["reason"] == "optional Kafka publisher"

    def test_multiple_params_accumulate(self) -> None:
        @injectable_optional("logger", reason="optional structured logger")
        @injectable_optional("event_bus", reason="optional Kafka publisher")
        class MultiNode:
            pass

        assert hasattr(MultiNode, "__injectable_optional__")
        meta: Any = MultiNode.__injectable_optional__
        assert isinstance(meta, list)
        param_names = {entry["param_name"] for entry in meta}
        assert "event_bus" in param_names
        assert "logger" in param_names

    def test_reason_is_required(self) -> None:
        with pytest.raises(TypeError):

            @injectable_optional("event_bus")  # type: ignore[call-arg]
            class BadNode:
                pass

    def test_class_still_instantiable(self) -> None:
        @injectable_optional("event_bus", reason="optional Kafka publisher")
        class SimpleNode:
            def __init__(self, event_bus: object = None) -> None:
                self.event_bus = event_bus

        node = SimpleNode()
        assert node.event_bus is None

    def test_decorated_class_identity_preserved(self) -> None:
        @injectable_optional("event_bus", reason="optional Kafka publisher")
        class NamedNode:
            pass

        assert NamedNode.__name__ == "NamedNode"

    def test_importable_from_registration_package(self) -> None:
        from omnibase_compat.registration import decorator_injectable_optional  # noqa: F401
