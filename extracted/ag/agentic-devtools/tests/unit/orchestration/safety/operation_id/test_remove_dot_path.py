from __future__ import annotations

from agentic_devtools.orchestration.safety.operation_id import _remove_dot_path


class TestRemoveDotPath:
    """Tests for private dot-path removal helper."""

    def test_returns_non_dict_input_unchanged(self) -> None:
        data = ["not", "a", "dict"]

        assert _remove_dot_path(data, "metadata.session_id") is data
