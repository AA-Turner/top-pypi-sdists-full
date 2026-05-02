from __future__ import annotations
import os
import fnmatch

from collections.abc import Iterable, Sequence, Set
from pathlib import Path
from dataclasses import dataclass
from typing import Annotated, Any, TypedDict
import tomllib
import pydantic
import pydantic_core
from django import apps
from django.db import models as django_models

from . import _rules

RULE_FILE_NAME = "model_rules.toml"


@dataclass(frozen=True)
class RuleFile:
    path: Path
    app_label: str

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, RuleFile):
            raise NotImplementedError
        return self.app_label < other.app_label

    @property
    def rel_path(self) -> Path:
        return Path(os.path.relpath(self.path, Path.cwd()))


class InvalidRuleFile(Exception):
    """
    Raised when a rule file cannot be parsed.
    """

    def __init__(self, errors: Sequence[str], rule_file: RuleFile) -> None:
        self.errors = errors
        self.rule_file = rule_file


def discover_rule_files() -> set[RuleFile]:
    """
    Return rule files for all installed Django apps.
    """
    candidate_rule_files = {
        RuleFile(path=Path(app.path) / RULE_FILE_NAME, app_label=app.label)
        for app in apps.apps.get_app_configs()
    }
    return {rule_file for rule_file in candidate_rule_files if rule_file.path.exists()}


def read_rules_from_files(
    rule_files: Set[RuleFile], model_classes: Set[type[django_models.Model]]
) -> tuple[set[_rules.Rule], list[str]]:
    """
    Read the defined rules from the supplied rule files.

    Returns tuple of:
        1. All the Rules.
        2. A list of warnings to surface to the user.

    Raises:
        InvalidRuleFile: if a rule file could not be parsed.
    """
    all_rules, all_warnings = set(), []
    for rule_file in sorted(rule_files):  # Sort so the output is deterministic.
        rules, warnings = _read_rules_from_file(rule_file, model_classes)
        all_rules |= rules
        all_warnings.extend(warnings)
    return all_rules, all_warnings


def _read_rules_from_file(
    rule_file: RuleFile, model_classes: Set[type[django_models.Model]]
) -> tuple[set[_rules.Rule], list[str]]:
    return _parse_rule_file_contents(
        rule_file.path.read_text(), rule_file, model_classes
    )


def _parse_rule_file_contents(
    contents: str,
    rule_file: RuleFile,
    model_classes: Set[type[django_models.Model]],
) -> tuple[set[_rules.Rule], list[str]]:
    """
    Return parsed rules along with any warnings.

    Raises InvalidRuleFile.
    """
    try:
        data = tomllib.loads(contents)
    except tomllib.TOMLDecodeError as exc:
        raise InvalidRuleFile([f"Malformed TOML: {exc}"], rule_file) from None

    rules: set[_rules.Rule] = set()
    warnings: list[str] = []
    errors: list[str] = []

    # Get all the rules tables ([rule.foo], [rule.bar] etc.)
    try:
        rules_data = data["rule"]
    except KeyError:
        warnings.append(f"No rules found\n  [blue]--> {rule_file.rel_path}[/blue]\n")
        return rules, warnings

    for rule_id, rule_data in rules_data.items():
        rule_or_none, warnings_for_rule, errors_for_rule = _parse_into_rule(
            rule_id=rule_id,
            rule_file=rule_file,
            rule_data=rule_data,
            model_classes=model_classes,
        )
        warnings.extend(warnings_for_rule)
        errors.extend(errors_for_rule)
        if rule_or_none:
            rules.add(rule_or_none)

    if errors:
        raise InvalidRuleFile(errors, rule_file)

    return rules, warnings


class _PydanticContext(TypedDict):
    model_classes: _rules.DjangoModelSet


def _parse_into_rule(
    rule_id: str,
    rule_file: RuleFile,
    rule_data: dict[str, object],
    model_classes: Set[type[django_models.Model]],
) -> tuple[_rules.Rule | None, list[str], list[str]]:
    """
    Returns tuple of:
         - Rule, if one could be created.
         - Warnings to surface to the user.
         - Errors to surface to the user.
    """
    warnings: list[str] = []

    rule_reference = f"rule.{rule_id}"
    rule_display = f"[blue](in [bold]{rule_reference}[/bold])[/blue]"

    try:
        rule_type_name = rule_data["type"]
    except KeyError:
        error = f"Missing rule type {rule_display}"
        return None, [], [error]

    try:
        rule_config_class = RULE_CONFIG_CLASSES_BY_NAME[str(rule_type_name)]
    except KeyError:
        error = f"Unknown rule type [bold]'{rule_type_name}'[/bold] {rule_display}"
        return None, [], [error]

    try:
        rule_config = rule_config_class.model_validate(
            rule_data, extra="allow", context={"model_classes": model_classes}
        )
    except pydantic.ValidationError as e:
        errors = _extract_errors_from_validation_exception(e, rule_display)
        return None, [], errors

    warnings.extend(
        _extract_warnings_from_any_unexpected_keys(
            rule_config, rule_reference, rule_file
        )
    )

    rule = rule_config.create_rule(rule_id, rule_file)
    return rule, warnings, []


def _extract_errors_from_validation_exception(
    exc: pydantic.ValidationError, rule_display: str
) -> list[str]:
    return [
        _extract_error_text_from_error_details(error_details, rule_display)
        for error_details in exc.errors()
    ]


def _extract_error_text_from_error_details(
    error_details: pydantic_core.ErrorDetails, rule_display: str
) -> str:
    if error_details["type"] == "missing":
        [field_name] = error_details["loc"]
        error_part = f"Missing key [bold]'{field_name}'[/bold]"
    else:
        error_part = error_details["msg"]
    error_text = f"{error_part} {rule_display}"
    return error_text


def _extract_warnings_from_any_unexpected_keys(
    rule_config: pydantic.BaseModel, rule_reference: str, rule_file: RuleFile
) -> list[str]:
    unexpected_keys = getattr(rule_config, "__pydantic_extra__", {}).keys() - {"type"}
    return [
        f"Unexpected key [bold]'{unexpected_key}'[/bold]\n"
        f"  [blue]--> [bold]{rule_reference}[/bold] in {rule_file.rel_path}[/blue]\n"
        for unexpected_key in sorted(unexpected_keys)
    ]


def _model_expressions_to_model_classes(
    expressions: Any, info: pydantic.ValidationInfo[_PydanticContext]
) -> _rules.DjangoModelSet:
    if isinstance(expressions, str):
        # Support passing in a single string, rather than an Array.
        expression_list = [expressions]
    else:
        expression_list = expressions

    if not isinstance(expression_list, Iterable):
        raise _make_pydantic_error(
            code="invalid_model_expression",
            message_tail="must be a String or Array of Strings",
            info=info,
        )

    matched_model_classes: set[type[django_models.Model]] = set()
    for expression in expression_list:
        if not isinstance(expression, str):
            raise _make_pydantic_error(
                code="invalid_model_expression",
                message_tail="must be a String or Array of Strings",
                info=info,
            )
        matched_model_classes |= _model_expression_to_model_classes(expression, info)

    return matched_model_classes


def _model_expression_to_model_classes(
    expression: str, info: pydantic.ValidationInfo[_PydanticContext]
) -> _rules.DjangoModelSet:
    matched_model_classes = {
        model_class
        for model_class in info.context["model_classes"]
        if fnmatch.fnmatch(model_class._meta.label, expression)
    }

    if not matched_model_classes:
        raise _make_pydantic_error(
            code="unmatched_model_expression",
            message_tail=f"expression '{expression}' did not match any installed models",
            info=info,
        )

    return matched_model_classes


def _make_pydantic_error(
    code: str,
    message_tail: str,
    info: pydantic.ValidationInfo[_PydanticContext],
) -> pydantic_core.PydanticCustomError:
    return pydantic_core.PydanticCustomError(
        code,
        f"[bold]{info.field_name}:[/bold] {message_tail}",
    )


DjangoModelSetPydanticField = Annotated[
    _rules.DjangoModelSet, pydantic.BeforeValidator(_model_expressions_to_model_classes)
]


class NoInboundForeignKeysRuleConfig(pydantic.BaseModel):
    """
    The config in the TOML file corresponding to a NoInboundForeignKeysRule.

    This is a separate class from the Rule class as the schema is slightly different.
    Its role is to validate the TOML and turn it into the Rule.
    """

    models: DjangoModelSetPydanticField
    allowed: DjangoModelSetPydanticField = frozenset()
    silenced_violations: DjangoModelSetPydanticField = frozenset()

    def create_rule(
        self, rule_id: str, rule_file: RuleFile
    ) -> _rules.NoInboundForeignKeysRule:
        return _rules.NoInboundForeignKeysRule(
            id=rule_id,
            app_label=rule_file.app_label,
            path=rule_file.path,
            models=self.models,
            allowed=self.allowed,
            silenced_violations=self.silenced_violations,
        )


RULE_CONFIG_CLASSES_BY_NAME = {
    _rules.NoInboundForeignKeysRule.type_name: NoInboundForeignKeysRuleConfig,
}
