from __future__ import annotations
import os
import inspect
from collections.abc import Set
from pathlib import Path
from dataclasses import dataclass
from typing import ClassVar, TypeAlias

from django.db import models as django_models
from django.db.models.fields import related as django_related_fields


@dataclass(frozen=True)
class Rule:
    type_name: ClassVar[str]
    id: str
    app_label: str
    path: Path

    def check(self, model_classes: Set[type[django_models.Model]]) -> CheckResult:
        raise NotImplementedError

    @property
    def rel_path(self) -> Path:
        return Path(os.path.relpath(self.path, Path.cwd()))


@dataclass(frozen=True)
class CheckResult:
    rule: Rule
    violations: frozenset[str]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CheckResult):
            raise NotImplementedError
        return self.rule.id < other.rule.id


DjangoModelSet: TypeAlias = Set[type[django_models.Model]]


@dataclass(frozen=True)
class NoInboundForeignKeysRule(Rule):
    type_name = "no_inbound_foreign_keys"
    models: DjangoModelSet
    allowed: DjangoModelSet = frozenset()
    silenced_violations: DjangoModelSet = frozenset()

    def check(self, model_classes: Set[type[django_models.Model]]) -> CheckResult:
        violations = set()
        models_to_ignore = self.allowed | self.silenced_violations

        for model_class in model_classes:
            if model_class in models_to_ignore:
                continue

            fields = model_class._meta.get_fields()
            for field in fields:
                if field.is_relation:
                    if isinstance(
                        field,
                        (
                            django_related_fields.ForeignKey,
                            django_related_fields.ManyToManyField,
                        ),
                    ):
                        file_path = Path(
                            os.path.relpath(inspect.getfile(model_class), Path.cwd())
                        )
                        related_model_class = field.related_model
                        if related_model_class == "self":
                            continue
                        if related_model_class in self.models:
                            violations.add(
                                f"[bold][red]{self.type_name}:[/red] "
                                f"{model_class._meta.app_label}.{model_class._meta.object_name}.{field.name} "
                                f"is a {type(field).__name__} to {related_model_class._meta.label}[/bold]\n"
                                f"  [blue]-->[/blue] Violates rule [blue bold]{self.id}[/blue bold] in [blue]{self.rel_path}[/blue]\n"
                                f"  [blue]-->[/blue] Field defined in [blue]{file_path}[/blue]"
                            )

        return CheckResult(
            rule=self,
            violations=frozenset(violations),
        )
