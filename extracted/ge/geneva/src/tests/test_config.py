import os
from pathlib import Path

import attrs
import pytest

from geneva.config import ConfigBase
from geneva.config.loader import (
    ConfigLoader,
    chain,
    from_dict,
    from_env,
    from_file,
    from_kv,
    from_pyproject,
    loader,
)


@attrs.define
class Config(ConfigBase):
    value: int = attrs.field(converter=int, validator=attrs.validators.ge(0))

    @classmethod
    def name(cls) -> str:
        return "config"


@pytest.mark.parametrize(
    "config_loader",
    map(
        loader,
        [
            from_dict({"config": {"value": "42"}}),
            from_kv({"config.value": "42"}),
        ],
    ),
)
def test_class_simple(config_loader: ConfigLoader) -> None:
    config = config_loader.load(Config)
    assert config.value == 42


@attrs.define
class NestedConfig(ConfigBase):
    config: Config = attrs.field()

    @classmethod
    def name(cls) -> str:
        return "nested_config"


@pytest.mark.parametrize(
    "config_loader",
    map(
        loader,
        [
            from_dict({"nested_config": {"config": {"value": "42"}}}),
            from_kv({"nested_config.config.value": "42"}),
        ],
    ),
)
def test_class_nested(config_loader: ConfigLoader) -> None:
    config = config_loader.load(NestedConfig)
    assert config.config.value == 42


@attrs.define
class ConfigWithDefault(ConfigBase):
    value: int = attrs.field(
        default=100, converter=int, validator=attrs.validators.ge(0)
    )

    @classmethod
    def name(cls) -> str:
        return "config"


def test_class_default() -> None:
    config = loader(from_dict({})).load(ConfigWithDefault)
    assert config.value == 100

    config = loader(from_dict({"config": {"value": "42"}})).load(ConfigWithDefault)
    assert config.value == 42


def test_config_key_missing() -> None:
    with pytest.raises(TypeError, match=r"missing [\d]* required .* argument"):
        loader(from_dict({})).load(Config)


@attrs.define
class MultiValueConfig(ConfigBase):
    value1: int = attrs.field(converter=int, validator=attrs.validators.ge(0))
    value2: int = attrs.field(converter=int, validator=attrs.validators.ge(0))
    value3: int = attrs.field(converter=int, validator=attrs.validators.ge(0))

    @classmethod
    def name(cls) -> str:
        return "config"


def test_chain_resolution() -> None:
    config_loader = loader(
        chain(
            from_dict({"config": {"value1": "40"}}),
            from_dict({"config": {"value1": "41", "value2": "42"}}),
            from_dict({"config": {"value1": "41", "value2": "42", "value3": "43"}}),
        )
    )
    config = config_loader.load(MultiValueConfig)
    assert config.value1 == 40
    assert config.value2 == 42
    assert config.value3 == 43


def test_attr_config_validation_behavior() -> None:
    config_loader = loader(
        chain(
            from_dict({"config": {"value1": "-1"}}),
            from_dict({"config": {"value1": "41", "value2": "42"}}),
            from_dict({"config": {"value1": "41", "value2": "42", "value3": "43"}}),
        )
    )
    with pytest.raises(ValueError, match=r"'value1' must be >= 0"):
        config_loader.load(MultiValueConfig)


def test_env_var_loader() -> None:
    os.environ["NESTED_CONFIG__CONFIG__VALUE"] = "42"

    config_loader = loader(from_env())
    config = config_loader.load(NestedConfig)
    assert config.config.value == 42


@attrs.define
class NestedConfigFromFile(ConfigBase):
    config: MultiValueConfig = attrs.field()

    @classmethod
    def name(cls) -> str:
        return "nested_config"


@pytest.mark.parametrize(
    "config_loader",
    map(
        loader,
        [
            from_file(Path(__file__).parent / "test_configs" / "config.json"),
            from_file(Path(__file__).parent / "test_configs" / "config.yaml"),
            from_file(
                Path(__file__).parent / "test_configs" / "config_json_as_yaml.yaml"
            ),
            from_file(Path(__file__).parent / "test_configs" / "config1.toml"),
            from_file(Path(__file__).parent / "test_configs" / "config2.toml"),
        ],
    ),
)
def test_file_loader(config_loader: ConfigLoader) -> None:
    config = config_loader.load(NestedConfigFromFile)
    assert config.config.value1 == 41
    assert config.config.value2 == 42
    assert config.config.value3 == 43


@attrs.define
class TestConfig(ConfigBase):
    __test__ = False
    config: NestedConfig = attrs.field()

    @classmethod
    def name(cls) -> str:
        return "test"


def test_pyproject_loader() -> None:
    config_loader = loader(from_pyproject())
    config = config_loader.load(TestConfig)
    assert config.config.config.value == 42
