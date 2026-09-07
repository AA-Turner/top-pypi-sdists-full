from dataclasses import dataclass
from typing import Optional
import pytest

from snakemake_interface_common import at_least_snakemake_version
from snakemake_interface_common.exceptions import ApiError, WorkflowError
from snakemake_interface_common.plugin_registry.plugin import TaggedSettings, SettingsBase, PluginBase
from snakemake_interface_common.rules import RuleInterface
from snakemake_interface_common.settings import SettingsEnumBase


@dataclass
class DummyRule(RuleInterface):
    lineno: int = 1
    name: str = "dummy_rule"
    snakefile: str = "dummy_snakefile"


def test_workflow_error():
    with pytest.raises(WorkflowError):
        raise WorkflowError("This is a test error")


def test_workflow_error_with_rule():
    with pytest.raises(WorkflowError):
        raise WorkflowError("This is a test error", rule=DummyRule())


def test_workflow_error_with_rule_and_snakefile():
    with pytest.raises(WorkflowError):
        raise WorkflowError(
            "This is a test error", rule=DummyRule(), snakefile="test_snakefile"
        )


def test_workflow_error_with_rule_and_snakefile_and_lineno():
    with pytest.raises(WorkflowError):
        raise WorkflowError(
            "This is a test error",
            rule=DummyRule(),
            snakefile="test_snakefile",
            lineno=1,
        )


def test_api_error():
    with pytest.raises(ApiError):
        raise ApiError("This is a test error")


class DummyEnum(SettingsEnumBase):
    FOO = 0
    BAR = 1


def test_settings_enum():
    assert DummyEnum.FOO == DummyEnum.parse_choice("foo")
    assert DummyEnum.BAR == DummyEnum.parse_choice("bar")
    assert "foo" == DummyEnum.FOO.item_to_choice()
    assert "bar" == DummyEnum.BAR.item_to_choice()
    assert ["bar", "foo"] == DummyEnum.choices()
    assert {DummyEnum.FOO, DummyEnum.BAR} == DummyEnum.all()
    assert [DummyEnum.FOO, DummyEnum.BAR] == DummyEnum.parse_choices_list(
        ["foo", "bar"]
    )
    assert {DummyEnum.FOO, DummyEnum.BAR} == DummyEnum.parse_choices_set(["foo", "bar"])


def test_tagged_settings():
    ts = TaggedSettings()
    ts.register_settings(object())
    ts.register_settings(object(), tag="foo")
    ts.get_settings(tag="foo")
    ts.get_settings()


def test_snakemake_version():
    assert at_least_snakemake_version("8.1.0")
    assert not at_least_snakemake_version("100.0.0")


@dataclass
class TestSettings(SettingsBase):
    required_int: int = 42
    optional_int: Optional[int] = None


class TestPlugin(PluginBase[TestSettings]):
    @property
    def name(self) -> str:
        return "test_plugin"

    @property
    def cli_prefix(self) -> str:
        return "test"

    @property
    def settings_cls(self) -> Optional[type[TestSettings]]:
        return TestSettings


def test_settings_int_conversion():
    """Test that settings converts both int and Optional[int] values from str to int."""
    plugin = TestPlugin()

    # Mock args object with string values
    class MockArgs:
        def __init__(self):
            self.test_required_int = "123"
            self.test_optional_int = "456"

    args = MockArgs()
    settings = plugin.get_settings(args)

    # Check that string values were converted to int
    assert isinstance(settings.required_int, int)
    assert settings.required_int == 123

    assert isinstance(settings.optional_int, int)
    assert settings.optional_int == 456


def test_settings_optional_int_none():
    """Test that Optional[int] can handle None values."""
    plugin = TestPlugin()

    # Mock args object with None for optional field
    class MockArgs:
        def __init__(self):
            self.test_required_int = "789"
            self.test_optional_int = None

    args = MockArgs()
    settings = plugin.get_settings(args)

    # Check that required int was converted and optional remains None
    assert isinstance(settings.required_int, int)
    assert settings.required_int == 789

    assert settings.optional_int is None
