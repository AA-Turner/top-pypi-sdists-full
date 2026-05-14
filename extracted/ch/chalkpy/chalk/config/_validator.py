from typing import Any, Mapping, Optional, Tuple


class Validator:
    @staticmethod
    def string(value: Any, name: str, *, one_of: Optional[Tuple[str, ...]] = None) -> str:
        if value is None:
            raise ValueError(f"Expected a string, but found nothing for '{name}'")
        if not isinstance(value, str):
            raise ValueError(f"Expected a string, but found '{value}' for '{name}'")
        if one_of is not None and value not in one_of:
            raise ValueError(f"Expected '{name}' to be one of {one_of}, got '{value}'")
        return value

    @staticmethod
    def optional_string(value: Any, name: str, *, one_of: Optional[Tuple[str, ...]] = None) -> Optional[str]:
        return None if value is None else Validator.string(value=value, name=name, one_of=one_of)

    @staticmethod
    def dict_with_str_keys(value: Any, name: str) -> Mapping[str, Any]:
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict for '{name}', got '{value}'")
        for k in value.keys():
            if not isinstance(k, str):
                raise ValueError(f"Expected string key for '{name}', got '{k}'")
        return value

    @staticmethod
    def dict_with_str_keys_or_none(value: Any, name: str) -> Optional[Mapping[str, Any]]:
        return None if value is None else Validator.dict_with_str_keys(value, name)
