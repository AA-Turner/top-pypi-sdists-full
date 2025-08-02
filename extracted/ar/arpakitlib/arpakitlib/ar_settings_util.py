# arpakit
from typing import Union, Any

from pydantic import ConfigDict, model_validator
from pydantic_core import PydanticUndefined
from pydantic_settings import BaseSettings

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_env_example(settings_class: Union[BaseSettings, type[BaseSettings]]):
    res = ""
    for k, f in settings_class.model_fields.items():
        if f.default is not PydanticUndefined:
            res += f"# {k}=\n"
        else:
            res += f"{k}=\n"
    return res


class SimpleSettings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def validate_all_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        for key, value in values.items():
            if isinstance(value, str) and value.lower().strip() in {"null", "none", "nil"}:
                values[key] = None
        return values

    @classmethod
    def generate_env_example(cls) -> str:
        return generate_env_example(settings_class=cls)

    @classmethod
    def save_env_example_to_file(cls, filepath: str) -> str:
        env_example = cls.generate_env_example()
        with open(filepath, mode="w") as f:
            f.write(env_example)
        return env_example


def __example():
    pass


if __name__ == '__main__':
    __example()
