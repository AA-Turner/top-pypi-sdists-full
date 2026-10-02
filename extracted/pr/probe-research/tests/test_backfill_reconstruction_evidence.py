"""Bounded current-project evidence survives large folders and inherited metadata."""

from dataclasses import dataclass
import hashlib
import json
import re
import sqlite3

import pytest

from probe.cli import backfill_reconstruction as rec


@dataclass
class Scope:
    customer_id: str = "tenant"
    workspace_id: str = "workspace"
    backend: str = "https://api.invalid"


class LocalCoverage:
    source_id = "source"
    scope = Scope()

    def __init__(self, root, contents):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE versions(correlation TEXT, receipt TEXT)")
        self.rows = []
        for index, (name, text) in enumerate(contents.items()):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            correlation = str(index)
            self.rows.append(
                {
                    "path": name,
                    "approved_hash": digest,
                    "correlation": correlation,
                    "project_id": "project",
                }
            )
            receipt = {
                "artifact_id": "artifact-" + correlation,
                "readable": True,
                "is_reference": False,
                "state": "delivered",
                "status": "complete",
                "anchor_id": "project",
                "content_hash": digest,
            }
            self.conn.execute(
                "INSERT INTO versions VALUES (?,?)", (correlation, json.dumps(receipt))
            )


class ReadableClient:
    def presign_download_batch(self, ids):
        return {
            "items": {ident: {"download_url": "https://private.invalid/temporary"} for ident in ids}
        }


def inputs(root, coverage, rows=None):
    return rec._inputs(
        ReadableClient(), root, coverage, coverage.rows if rows is None else rows, None, "project"
    )


def test_overview_and_status_survive_vendored_readmes_and_housekeeping(tmp_path):
    contents = {f"vendor/dep-{i}/README.md": "An inherited library.\n" * 200 for i in range(70)}
    contents.update(
        {f".github/workflows/{i}.yml": "name: legacy-package\n" * 200 for i in range(70)}
    )
    contents.update(
        {
            "CHANGELOG.md": "A completed upstream maintenance issue.\n" * 200,
            "README.md": "This is the unfinished local reconstruction, derived from an older library.\n",
            "CURRENT_STATUS.md": "Implementation exists; evaluation and policy choices remain open.\n",
        }
    )
    coverage = LocalCoverage(tmp_path, contents)
    result = inputs(tmp_path, coverage)
    sources = list(result["sources"].values())
    assert sources[0]["path"] == "README.md"
    assert sources[1]["path"] == "CURRENT_STATUS.md"
    assert sources[0]["role_hint"] == "project_overview"
    assert sources[1]["role_hint"] == "status_or_handoff"
    assert result["inventory_count"] == len(contents)
    assert len(rec._json(result["sources"]).encode()) <= rec.MAX_INPUT_BYTES // 2
    assert len(rec._json(result).encode()) <= rec.MAX_INPUT_BYTES
    assert "private.invalid" not in rec._json(result)


def test_input_identity_and_citations_ignore_row_order_and_mtime(tmp_path):
    coverage = LocalCoverage(
        tmp_path,
        {
            "z.py": "CODE = 1\n",
            "STATUS.md": "The question remains open.\n",
            "README.md": "The local project.\n",
        },
    )
    before = inputs(tmp_path, coverage)
    import os

    for row in coverage.rows:
        os.utime(tmp_path / row["path"], (1234, 5678))
    after = inputs(tmp_path, coverage, list(reversed(coverage.rows)))
    assert before == after


def test_code_only_source_still_provides_bounded_evidence(tmp_path):
    coverage = LocalCoverage(tmp_path, {"z.py": "def evaluate():\n    return None\n"})
    result = inputs(tmp_path, coverage)
    assert result["inventory_count"] == 1
    assert result["sources"]["F001"]["role_hint"] == "implementation_or_data"
    assert "def evaluate" in result["sources"]["F001"]["text"]


def test_heading_windows_keep_current_configuration_and_open_limits_with_real_lines():
    lines = ["# Local reconstruction\n", "Identity and precedence.\n"]
    lines += ["Archived boilerplate " * 12 + "\n"] * 100
    lines += ["```markdown\n", "## Configuration\n", "FENCED_DECOY\n", "```\n"]
    lines += ["~~~\n", "## Current status\n", "TILDE_DECOY\n", "~~~\n"]
    lines += [
        "## Current status\n",
        "CURRENT_IMPLEMENTATION: built but not scientifically evaluated.\n",
        "\n",
    ]
    lines += ["Filler " * 20 + "\n"] * 80
    lines += [
        "## Configuration\n",
        "NO_VALUES: unconfigured is allowed and stays disabled.\n",
        "SOME_VALUES: partial configuration is an error.\n",
        "\n",
    ]
    lines += ["More detail " * 20 + "\n"] * 80
    lines += [
        "## Remaining evaluation\n",
        "OPEN_GATE: scientific comparison remains unperformed.\n",
    ]
    raw = "".join(lines)
    sample = rec._narrative_excerpt(raw)
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES
    for expected in (
        "Identity and precedence.",
        "CURRENT_IMPLEMENTATION",
        "NO_VALUES",
        "SOME_VALUES",
        "OPEN_GATE",
    ):
        assert expected in sample
    assert "FENCED_DECOY" not in sample and "TILDE_DECOY" not in sample
    assert "[... omitted ...]" in sample
    for match in re.finditer(
        r"\[Lines (\d+)-(\d+)\]\n(.*?)(?=\n?\[(?:Lines|\.\.\.)|\Z)", sample, re.S
    ):
        start, end = map(int, match.group(1, 2))
        assert match[3].rstrip("\n") == "".join(lines[start - 1 : end]).rstrip("\n")


def test_short_sections_return_unused_budget_to_configuration():
    prefix = "# Component\n" + "Preamble detail.\n" * 100
    config = "## Configuration\n" + "Context for the rule.\n" * 45
    config += "UNCONFIGURED is valid.\nPARTIAL is rejected.\n"
    raw = prefix + config + "## Evaluation\nStill open.\n" + "Other detail.\n" * 400
    sample = rec._narrative_excerpt(raw)
    assert "UNCONFIGURED is valid." in sample and "PARTIAL is rejected." in sample
    assert "Still open." in sample
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES


def test_giant_preamble_does_not_starve_later_sections_or_invent_full_line_citation():
    raw = (
        "x" * 20_000
        + "\n## Current status\nBuilt; not evaluated.\n## Configuration\nDefaults remain disabled.\n"
    )
    sample = rec._narrative_excerpt(raw)
    assert "Built; not evaluated." in sample and "Defaults remain disabled." in sample
    assert "[Lines 1-" not in sample
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES


@pytest.mark.parametrize("suffix", [".md", ".py"])
def test_valid_utf8_crossing_old_prefix_boundary_is_not_dropped(tmp_path, suffix):
    path = tmp_path / ("source" + suffix)
    path.write_text("a" * (rec.MAX_SAMPLE_BYTES - 1) + "μ" * 1000)
    row = {"path": path.name, "approved_hash": hashlib.sha256(path.read_bytes()).hexdigest()}
    sample, limitation = rec._read_sample(tmp_path, row)
    assert sample and limitation
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES
    assert "non-UTF-8" not in limitation


def test_changed_source_and_escaping_link_still_refuse(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    path = root / "README.md"
    path.write_text("Old identity")
    row = {"path": "README.md", "approved_hash": hashlib.sha256(path.read_bytes()).hexdigest()}
    path.write_text("Changed identity")
    with pytest.raises(ValueError, match="differ"):
        rec._read_sample(root, row)
    outside = tmp_path / "outside.md"
    outside.write_text("Outside")
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(ValueError, match="outside"):
        rec._read_sample(root, row)


def test_exhausted_windows_do_not_strand_a_long_configuration_line():
    raw = "# Component\n" + "Preamble detail.\n" * 100
    raw += "## Current status\nBuilt, evaluation remains open.\n"
    raw += "## Configuration\n" + "context " * 150 + "\n"
    raw += "UNCONFIGURED is valid; PARTIAL is rejected.\n"
    raw += "## Evaluation\nStill open.\n" + "Other detail.\n" * 400
    sample = rec._narrative_excerpt(raw)
    assert "UNCONFIGURED is valid; PARTIAL is rejected." in sample
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES


def test_nonclosing_fence_suffix_cannot_promote_fake_headings():
    raw = "# Component\n" + "Preamble detail.\n" * 100
    raw += "````markdown\n````not-a-closing-fence\n## Configuration\n"
    raw += "FAKE_CONFIG\n" * 400 + "````\n"
    raw += "## Configuration\nREAL_CONFIG\n## Open gates\nREAL_GATE\n"
    sample = rec._narrative_excerpt(raw)
    assert "FAKE_CONFIG" not in sample
    assert "REAL_CONFIG" in sample and "REAL_GATE" in sample


def test_extensionless_readme_uses_located_narrative_windows(tmp_path):
    path = tmp_path / "README"
    path.write_text(
        "# Project\n" + "Old detail.\n" * 500 + "## Configuration\nUNCONFIGURED allowed.\n"
    )
    row = {"path": path.name, "approved_hash": hashlib.sha256(path.read_bytes()).hexdigest()}
    sample, limitation = rec._read_sample(tmp_path, row)
    assert "UNCONFIGURED allowed." in sample and "[Lines" in sample
    assert "line ranges" in limitation


def test_unicode_line_separators_do_not_change_source_line_numbers():
    lines = ["# Project\n", "Unicode detail \u0085 \u2028 \u2029\n"]
    lines += ["Old detail.\n"] * 500
    lines += ["## Configuration\n", "THE_RULE\n"]
    sample = rec._narrative_excerpt("".join(lines))
    assert "[Lines 503-504]" in sample
    assert "THE_RULE" in sample


def test_parent_section_windows_include_nested_heading_content():
    raw = "# Project\n" + "Preamble detail.\n" * 400
    raw += "## Current status\n### Implementation\nCURRENT_BUILT\n"
    raw += "## Configuration\n### Defaults\nUNCONFIGURED_OK; PARTIAL_FAILS\n"
    raw += "## Evaluation\n### Results\nSCIENTIFIC_GATE_OPEN\n"
    sample = rec._narrative_excerpt(raw)
    for expected in ("CURRENT_BUILT", "UNCONFIGURED_OK; PARTIAL_FAILS", "SCIENTIFIC_GATE_OPEN"):
        assert expected in sample
    assert len(sample.encode()) <= rec.MAX_SAMPLE_BYTES
