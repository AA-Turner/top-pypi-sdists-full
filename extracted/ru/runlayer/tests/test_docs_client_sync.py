"""Guard the Detect docs against silent drift from the CLI detector.

``docs/shadow-ai/detect/index.mdx`` enumerates the presence-only clients and the
client detection methods. Both lists are hand-maintained copies of the detector
source of truth (``runlayer_cli.scan.clients`` and
``runlayer_cli.scan.client_presence``), so they drift silently when a client or
detection method is added without a docs edit. These tests turn that drift into
a failing check.

The tests locate the docs file relative to the repo root and skip when it is not
present (e.g. a CLI-only build context that ships without ``docs/``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from runlayer_cli import regex_safe
from runlayer_cli.scan.client_presence import DETECTION_METHOD_ORDER
from runlayer_cli.scan.clients import get_all_clients

_DOCS_RELATIVE = Path("docs") / "shadow-ai" / "detect" / "index.mdx"


def _find_docs() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / _DOCS_RELATIVE
        if candidate.is_file():
            return candidate
    return None


def _docs_text() -> str:
    docs = _find_docs()
    if docs is None:
        pytest.skip(f"{_DOCS_RELATIVE} not found (CLI-only checkout)")
    return docs.read_text(encoding="utf-8")


def _detector_presence_only_display_names() -> set[str]:
    """Display names of presence-only clients (no MCP config paths)."""
    return {client.display_name for client in get_all_clients() if not client.paths}


def _doc_presence_only_display_names(mdx: str) -> set[str]:
    """Parse the bold client list under the 'Presence-only clients' heading."""
    heading = "### Presence-only clients"
    assert heading in mdx, f"'{heading}' section missing from Detect docs"
    section = mdx.split(heading, 1)[1]
    # Bound the section to the next heading so a bold token elsewhere can't leak in.
    next_heading = regex_safe.search(r"^#{2,3} ", section, regex_safe.MULTILINE)
    if next_heading:
        section = section[: next_heading.start()]
    bold = regex_safe.search(r"\*\*(.+?)\*\*", section, regex_safe.DOTALL)
    assert bold, "presence-only client list (bold line) not found"
    raw = bold.group(1).strip().rstrip(".")
    names: set[str] = set()
    for part in raw.split(","):
        cleaned = regex_safe.sub(r"^\s*and\s+", "", part.strip())
        if cleaned:
            names.add(cleaned)
    return names


def _doc_detection_methods(mdx: str) -> list[str]:
    """Parse the backtick-quoted detection-method list from the docs."""
    match = regex_safe.search(r"detection methods:\s*(`[^\n]+?`)\.", mdx)
    assert match, "detection methods list not found in Detect docs"
    return regex_safe.findall(r"`([^`]+)`", match.group(1))


class TestDetectDocsClientSync:
    def test_presence_only_client_list_matches_detector(self) -> None:
        assert (
            _doc_presence_only_display_names(_docs_text())
            == _detector_presence_only_display_names()
        )

    def test_detection_methods_match_detector(self) -> None:
        assert set(_doc_detection_methods(_docs_text())) == set(DETECTION_METHOD_ORDER)

    def test_full_support_clients_appear_in_supported_tables(self) -> None:
        """Every config-scanning client's display name is documented.

        Guards against a client being wired into the detector but omitted from
        the Supported Clients tables entirely. Two clients whose table label is
        intentionally shortened are mapped to their documented spelling.
        """
        mdx = _docs_text()
        doc_label_overrides = {
            "Claude Desktop": "Claude Desktop / Cowork",
            "Cline (VS Code Extension)": "Cline (VS Code)",
        }
        missing = []
        for client in get_all_clients():
            if not client.paths:
                continue
            label = doc_label_overrides.get(client.display_name, client.display_name)
            if label not in mdx:
                missing.append(label)
        assert not missing, f"config-scanning clients absent from docs: {missing}"
