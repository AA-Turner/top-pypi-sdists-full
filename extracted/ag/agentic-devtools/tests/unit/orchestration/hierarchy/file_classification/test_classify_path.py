"""Unit tests for file classification precedence and specialization (FR-007, FR-008)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.file_classification import (
    classify_path,
)
from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory

_TASKS_MD = """\
# Tasks

- [ ] T001 Create `agentic_devtools/foo.py` and `docs/foo.md`
- [ ] T002 Create `agentic_devtools/bar.py` for a sibling task
"""


def test_classify_path_covers_all_supported_categories() -> None:
    assert classify_path("a.py") == SpecializationCategory.PYTHON
    assert classify_path("a.md") == SpecializationCategory.MARKDOWN
    assert classify_path("a.yaml") == SpecializationCategory.YAML
    assert classify_path("a.yml") == SpecializationCategory.YAML
    assert classify_path("a.ts") == SpecializationCategory.TYPESCRIPT
    assert classify_path("a.tsx") == SpecializationCategory.TYPESCRIPT
    assert classify_path("a.bin") == SpecializationCategory.UNSUPPORTED_OR_BINARY
    assert classify_path("a.png") == SpecializationCategory.UNSUPPORTED_OR_BINARY
