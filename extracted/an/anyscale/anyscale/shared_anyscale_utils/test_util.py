# AUTOGENERATED - modify shared_anyscale_util in root directory to make changes
from typing import Any, Dict, Tuple
from unittest.mock import _Call, MagicMock


# For `async with a() as b:`
class MockAsyncContextManagerReturnValue(MagicMock):
    async def __aenter__(self, *args) -> "MockAsyncContextManagerReturnValue":
        return self

    async def __aexit__(self, *args) -> None:
        return None


def get_args_from_call(call: _Call) -> Tuple[Any, ...]:
    args_tuple: Tuple[Any, ...] = call[0]
    return args_tuple


def get_kwargs_from_call(call: _Call) -> Dict[str, Any]:
    kw_args_dict: Dict[str, Any] = call[1]
    return kw_args_dict
