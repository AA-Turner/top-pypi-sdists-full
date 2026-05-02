from __future__ import annotations
import os
from collections.abc import Mapping, Sequence, Set
from pathlib import Path
from django.core.management import base

from django.db import models
from rich import console as rich_console

from ... import _django, _rule_files, _rules

EXIT_CODE_VIOLATIONS_FOUND = 1
EXIT_CODE_ABNORMAL = 2


class Command(base.BaseCommand):
    help = "Lints the relationships between models."

    def handle(self, *args: Sequence[object], **options: Mapping[str, object]) -> None:
        console = rich_console.Console(
            # It's best practice for linters to output to stderr, not stdout.
            stderr=True,
            # More control over formatting.
            highlight=False,
        )

        model_classes = _django.get_model_classes()

        rule_files = _rule_files.discover_rule_files()
        try:
            rules, warnings = _rule_files.read_rules_from_files(
                rule_files, model_classes
            )
        except _rule_files.InvalidRuleFile as e:
            rel_path = Path(os.path.relpath(e.rule_file.path, Path.cwd()))
            console.print(f"[red]Invalid rule file {rel_path}:")
            for violation in e.errors:
                console.print(f"- {violation}")
            console.print("[red bold]Aborted.")
            exit(EXIT_CODE_ABNORMAL)

        for warning in warnings:
            console.print(f"⚠️ [yellow bold]warning:[/bold yellow] {warning}")

        results = set()
        for rule in rules:
            results.add(rule.check(model_classes))

        num_violations = 0

        for result in sorted(results):
            if result.violations:
                num_violations += len(result.violations)
                for violation in sorted(result.violations):
                    console.print(
                        f"❌ {violation}",
                        highlight=False,
                    )
                    console.print()

        console.print(
            _build_final_message(rules, rule_files, model_classes, num_violations)
        )

        if num_violations:
            exit(EXIT_CODE_VIOLATIONS_FOUND)


def _build_final_message(
    rules: Set[_rules.Rule],
    rule_files: Set[_rule_files.RuleFile],
    model_classes: Set[type[models.Model]],
    num_violations: int,
) -> str:
    check_summary = f"(checked {len(rules)} rules from {len(rule_files)} rule files)"
    if num_violations:
        suffix = "s" if num_violations != 1 else ""
        return (
            f":slightly_frowning_face: [bold red]{num_violations} violation{suffix} in {len(model_classes)} models "
            f"{check_summary}."
        )
    else:
        return (
            f":sunglasses: [bold green]No violations in {len(model_classes)} models "
            f"{check_summary}."
        )
