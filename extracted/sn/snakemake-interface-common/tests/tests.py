from dataclasses import dataclass
import pytest

from snakemake_interface_common import at_least_snakemake_version
from snakemake_interface_common.exceptions import ApiError, WorkflowError
from snakemake_interface_common.plugin_registry.plugin import TaggedSettings
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
