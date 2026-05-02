from __future__ import annotations

import json
import tomllib
from collections.abc import Mapping, Sequence
from typing import Any
from typing_extensions import override
from django.core.management import base

from ... import _rule_files


class Command(base.BaseCommand):
    help = "Returns all model rules in JSON format."

    @override
    def handle(self, *args: Sequence[object], **options: Mapping[str, object]) -> None:
        rule_files = _rule_files.discover_rule_files()

        rules_data: list[dict[str, Any]] = []
        for rule_file in sorted(rule_files):
            toml_data = tomllib.loads(rule_file.path.read_text())
            for rule_id, rule_data in toml_data.get("rule", {}).items():
                rules_data.append(
                    {
                        "id": rule_id,
                        "app_label": rule_file.app_label,
                        **rule_data,
                    }
                )

        self.stdout.write(json.dumps(rules_data, indent=2))
