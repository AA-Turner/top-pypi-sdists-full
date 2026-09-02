"""Test extract_references — code fence paths and classify_reference_kind edge cases."""

from agentic_devtools.cli.speckit.pass_g.models import ReferenceKind
from agentic_devtools.cli.speckit.pass_g.reference_extractor import (
    classify_reference_kind,
    extract_references,
)


def test_extract_from_code_fence_backtick():
    """Backtick references inside code fences are extracted."""
    plan = """\
# Plan

```python
from `module_name` import something
Use `helper_func` here.
```
"""
    refs = extract_references(plan)
    texts = [r.text for r in refs]
    assert "module_name" in texts
    assert "helper_func" in texts


def test_extract_bare_file_paths_from_code_fence():
    """Bare file paths (e.g. module.py) inside code fences are extracted."""
    plan = """\
# Plan

```
Edit agentic_devtools/cli/state.py to add the function.
Also modify utils/helpers.toml for config.
```
"""
    refs = extract_references(plan)
    texts = [r.text for r in refs]
    assert "agentic_devtools/cli/state.py" in texts
    assert "utils/helpers.toml" in texts


def test_extract_bare_file_paths_from_code_fence_for_all_supported_extensions() -> None:
    """Supported non-Python extensions inside code fences are extracted."""
    plan = """\
# Plan

```text
schema.proto
notebook.ipynb
templates/default.md.j2
poetry.lock
```
"""
    refs = extract_references(plan)
    texts = [r.text for r in refs]

    assert "schema.proto" in texts
    assert "notebook.ipynb" in texts
    assert "templates/default.md.j2" in texts
    assert "poetry.lock" in texts


def test_extract_passthrough_extensions_from_code_fence() -> None:
    """Passthrough extensions accepted by verify_artifacts are extracted from fences."""
    plan = """\
# Plan

```sql
schema.sql
```

```css
styles.css
```

```text
.env
template.html
config.xml
infra.tf
local.env
app.conf
export.csv
requirements.in
```
"""
    texts = [r.text for r in extract_references(plan)]

    assert "schema.sql" in texts
    assert "styles.css" in texts
    assert ".env" in texts
    assert "template.html" in texts
    assert "config.xml" in texts
    assert "infra.tf" in texts
    assert "local.env" in texts
    assert "app.conf" in texts
    assert "export.csv" in texts
    assert "requirements.in" in texts


def test_extract_conventional_extensionless_filenames_from_code_fence() -> None:
    """Conventional extensionless filenames are extracted from fenced text."""
    plan = """\
# Plan

```text
Makefile
docker/Makefile
```
"""
    texts = [r.text for r in extract_references(plan)]

    assert "Makefile" in texts
    assert "docker/Makefile" in texts


def test_does_not_extract_supported_extension_when_a_longer_token_continues() -> None:
    """Fenced path extraction rejects longer hyphenated or dotted suffix tokens."""
    plan = """\
# Plan

```text
templates/default.md.j2-old
schema.proto.backup
```
"""
    texts = [r.text for r in extract_references(plan)]

    assert "templates/default.md.j2" not in texts
    assert "schema.proto" not in texts


def test_extract_deduplicates_across_fences_and_inline():
    """Same reference in inline and fence is deduplicated."""
    plan = """\
# Plan

Use `module.py` inline.

```
Modify module.py here.
```
"""
    refs = extract_references(plan)
    module_refs = [r for r in refs if r.text == "module.py"]
    assert len(module_refs) == 1


def test_classify_reference_kind_method_name():
    """Dotted reference with lowercase after dot → METHOD_NAME."""
    kind = classify_reference_kind("MyClass.my_method")
    assert kind == ReferenceKind.METHOD_NAME


def test_classify_reference_kind_method_name_nested():
    """Dotted reference starting with uppercase, last part lowercase → METHOD_NAME."""
    kind = classify_reference_kind("Class.method")
    assert kind == ReferenceKind.METHOD_NAME


def test_classify_reference_kind_module_path():
    """Dotted reference starting lowercase without uppercase → MODULE_PATH."""
    kind = classify_reference_kind("agentic_devtools.cli.state")
    assert kind == ReferenceKind.MODULE_PATH


def test_classify_reference_kind_file_extension():
    """Various file extensions are classified as FILE_PATH."""
    for ext in (".py", ".toml", ".yml", ".yaml", ".json", ".md", ".ts", ".js", ".rs", ".go"):
        kind = classify_reference_kind(f"file{ext}")
        assert kind == ReferenceKind.FILE_PATH, f"Failed for {ext}"


def test_classify_reference_kind_cli_command():
    """agdt- prefix → CLI_COMMAND."""
    kind = classify_reference_kind("agdt-speckit-cross-ref")
    assert kind == ReferenceKind.CLI_COMMAND


def test_classify_reference_kind_cli_command_underscore():
    """agdt_ prefix → CLI_COMMAND."""
    kind = classify_reference_kind("agdt_test")
    assert kind == ReferenceKind.CLI_COMMAND


def test_classify_reference_kind_class_name():
    """CamelCase starting uppercase → CLASS_NAME."""
    kind = classify_reference_kind("MyValidator")
    assert kind == ReferenceKind.CLASS_NAME


def test_classify_reference_kind_function_name():
    """snake_case → FUNCTION_NAME."""
    kind = classify_reference_kind("process_data")
    assert kind == ReferenceKind.FUNCTION_NAME


def test_classify_reference_kind_unclassified():
    """Short or unrecognized patterns → UNCLASSIFIED."""
    kind = classify_reference_kind("xy")
    assert kind == ReferenceKind.UNCLASSIFIED


def test_empty_plan_returns_no_references():
    """Empty or whitespace-only plan yields no references."""
    assert extract_references("") == []
    assert extract_references("   \n  \n  ") == []


def test_extract_references_dedup_false_returns_all_backtick_occurrences() -> None:
    """dedup=False returns every backtick occurrence, including duplicates.

    When a backtick-quoted path appears multiple times (once in an annotated
    tree and once in prose), dedup=False must return both occurrences so
    callers can classify each by its context sentence.
    """
    content = (
        "```text\n"
        "├── `research.md`          # Optional — only when there are unresolved technical unknowns\n"
        "```\n"
        "\n"
        "See `research.md` for the Research Summary.\n"
    )

    refs = extract_references(content, dedup=False)
    texts = [r.text for r in refs]

    # Both occurrences must be present — exactly one per source occurrence.
    assert texts.count("research.md") == 2

    # At least one occurrence carries the annotation context.
    assert any("Optional — only when" in (r.context_sentence or "") for r in refs if r.text == "research.md")

    # At least one occurrence carries the unconditional prose context.
    assert any("Research Summary" in (r.context_sentence or "") for r in refs if r.text == "research.md")


def test_extract_references_dedup_true_still_deduplicates() -> None:
    """dedup=True (the default) continues to return only the first occurrence."""
    content = "See `research.md` once.\nSee `research.md` again.\n"

    refs = extract_references(content, dedup=True)
    assert [r.text for r in refs].count("research.md") == 1


def test_extract_references_dedup_false_bare_path_in_fence() -> None:
    """dedup=False returns each bare file-path occurrence inside code fences."""
    content = "```\nModify utils/helpers.py here.\n```\n\n```\nAlso update utils/helpers.py settings.\n```\n"

    refs = extract_references(content, dedup=False)
    texts = [r.text for r in refs]

    # Both occurrences must be present: one per fence block.
    assert texts.count("utils/helpers.py") == 2
