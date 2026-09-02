from typing import Union

AvailableScopeTypes = Union[tuple[str], tuple[str, str], tuple[str, str, str]]

AVAILABLE_SCOPES: AvailableScopeTypes = ("data", "user_management", "publish")
