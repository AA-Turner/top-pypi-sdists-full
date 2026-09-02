import pytest
from pydantic import ValidationError

from matrx_ai.tools.arg_models.memory_args import MemoryArgs


def test_memory_recall_wire_limit_matches_implementation_limit() -> None:
    parsed = MemoryArgs.model_validate({"action": "recall", "limit": 20}).root
    assert parsed.limit == 20

    with pytest.raises(ValidationError):
        MemoryArgs.model_validate({"action": "recall", "limit": 25})
