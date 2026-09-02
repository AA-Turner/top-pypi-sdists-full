"""Fixtures for Phase 0 review tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def make_review_case(tmp_path: Path):
    """Build a valid mutable review case."""

    def factory(
        *,
        source_updates: dict[str, Any] | None = None,
        issue_title: str = "Example",
        snapshot_body: str | None = None,
    ) -> tuple[Path, Path]:
        source: dict[str, Any] = {
            "provider": "github",
            "issue_id": "42",
            "title": "Example",
            "status": "open",
            "body": "Body",
            "url": "https://github.com/example/repo/issues/42",
            "created_at": "2026-08-21T10:00:00Z",
            "updated_at": "2026-08-22T10:00:00+0000",
            "labels": ["feature", "phase-0"],
            "dependencies": ["#1", "#2"],
            "constraints": ["Exact"],
            "type": "feature",
            "truncated": False,
            "original_size": 4,
            "properties": {"effort": 3, "enabled": True},
        }
        if source_updates:
            source.update(source_updates)
            if "body" in source_updates and "original_size" not in source_updates:
                source["original_size"] = len(source["body"].encode("utf-8"))
        snapshot = (
            snapshot_body
            or """---
id: {{id}}
title: {{title}}
type: {{type}}
status: {{status}}
provider: {{provider}}
labels: {{labels}}
rendered_at: {{rendered_at}}
---
# {{title}}

## Description

{{description}}

## Dependencies

{{dependencies}}

## Constraints

{{constraints}}

| Property | Value |
| --- | --- |
| Effort | {{effort}} |
| Enabled | {{enabled}} |

Source: {{url}}
"""
        )
        issue = f"""---
id: "42"
title: "{issue_title}"
type: "feature"
status: "open"
provider: "github"
labels:
  - "feature"
  - "phase-0"
rendered_at: "2026-08-22T00:00:00+00:00"
---
# {issue_title}

## Description

{source["body"]}

## Dependencies

#1, #2

## Constraints

Exact

| Property | Value |
| --- | --- |
| Effort | 3 |
| Enabled | True |

Source: {source["url"]}
"""
        template = snapshot.split("---\n", 2)[-1]
        issue_path = tmp_path / "issue.md"
        template_path = tmp_path / "template.md"
        snapshot_path = tmp_path / "structure_snapshot.md"
        payload_path = tmp_path / "payload.json"
        issue_path.write_text(issue, encoding="utf-8")
        template_path.write_text(template, encoding="utf-8")
        snapshot_path.write_text(snapshot, encoding="utf-8")
        payload = {
            "schema_version": "phase0_factual_review_input/v1",
            "source": source,
            "issue_md": {"path": issue_path.relative_to(tmp_path).as_posix()},
            "template": {
                "selected_path": template_path.relative_to(tmp_path).as_posix(),
                "structure_snapshot_path": snapshot_path.relative_to(tmp_path).as_posix(),
            },
        }
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        integrity = {
            "payload_sha256": hashlib.sha256(payload_path.read_bytes()).hexdigest(),
            "selected_template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
            "snapshot_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
        }
        integrity_path = tmp_path / "phase0-integrity.json"
        integrity_path.write_text(json.dumps(integrity), encoding="utf-8")
        return payload_path, integrity_path

    return factory
