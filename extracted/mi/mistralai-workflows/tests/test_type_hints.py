from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core.utils.type_hints import get_type_hints


class MyModel(BaseModel):
    name: str
    value: int


class TestGetTypeHints:
    def test_plain_function(self) -> None:
        def fn(x: int, y: str) -> bool:
            return True

        hints = get_type_hints(fn)
        assert hints == {"x": int, "y": str, "return": bool}

    def test_activity_decorated_function(self) -> None:
        """WFL-1243: @activity-wrapped functions lose type hints on Python 3.14+ (PEP 649)."""

        @workflows.activity(retry_policy_max_attempts=0, _skip_registering=True)
        async def process(data: MyModel) -> str:
            return data.name

        hints = get_type_hints(process)
        assert hints["data"] is MyModel
        assert hints["return"] is str
