#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML", "pyspellchecker", "ruff==0.14.1"]
# ///

"""Lint the Tidy3D Quarto notebook source tree.

The structural checks run over the whole notebook corpus. Spellcheck and Ruff
syntax checks run only for changed QMD files by default so CI stays lightweight.
"""

from __future__ import annotations

import argparse
import ast
import concurrent.futures
import html
import io
import json
import logging
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

import yaml
from spellchecker import SpellChecker

ROOT = Path(__file__).resolve().parents[1]
CUSTOM_DICT_PATH = ROOT / "custom_dictionary.json"
GIT_LFS_POINTER_PREFIX = "version https://git-lfs.github.com/spec/v1"
IMPORT_MAPPING_LFS_MESSAGE = (
    "file is a Git LFS pointer, not the actual JSON content. Fetch notebook LFS assets with "
    "`git lfs pull --include 'flex/public/tidy3d/notebooks/misc/import_file_mapping.json'` "
    "from the repository root and rerun the check."
)
PYTHON_FENCE_RE = re.compile(r"^```\s*(?:\{python\b.*|python\b.*|py\b.*)$")
FENCE_END_RE = re.compile(r"^```\s*$")
WORD_RE = re.compile(r"\b[a-zA-Z][a-zA-Z'-]*[a-zA-Z]\b")
MISC_REF_RE = re.compile(r"(?<![A-Za-z0-9_./-])(?:\./)?misc/([A-Za-z0-9_.()+@=-]+)")
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
IPYTHON_SENTINEL_PREFIX = "__tidy3d_qmd_ruff_ipython_line_"
QUARTO_METADATA_SENTINEL_PREFIX = "__tidy3d_qmd_ruff_quarto_metadata_line_"
DEFAULT_RUFF_SELECT = "B,C,E,F,NPY201,UP,W"
DEFAULT_FIX_RUFF_SELECT = "E"
DEFAULT_RUFF_IGNORE_CODES = (
    "B006",
    "B007",
    "B008",
    "B018",
    "B028",
    "B904",
    "B905",
    "C408",
    "C417",
    "C901",
    "E402",
    "E501",
    "E703",
    "E722",
    "E731",
    "E741",
    "F401",
    "F811",
    "F821",
    "NPY201",
    "UP006",
    "UP007",
    "UP035",
)
DEFAULT_RUFF_IGNORE = ",".join(DEFAULT_RUFF_IGNORE_CODES)
NOTEBOOK_RUFF_FIX_IGNORE_CODES = ("E703",)
NOTEBOOK_RUFF_TARGET_VERSION = "py310"
NOTEBOOK_RUFF_LINE_LENGTH = "100"
RUFF_CONCISE_LOCATION_RE = re.compile(
    r"^(?P<path>.*?):(?P<line>\d+):(?P<column>\d+): (?P<message>.*)$"
)
RUFF_WRITEBACK_SAFE_SELECTOR_RE = re.compile(r"^E\d*$")
RUFF_WRITEBACK_UNSAFE_SELECTORS = {"E703"}
ORDERED_LIST_START_RE = re.compile(r"^\d+[.)]\s+")
LIST_ITEM_RE = re.compile(r"^(?:[-+*]|\d+[.)])\s+")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>\n]*>|[^\n)]*)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
HTML_LINK_ATTR_RE = re.compile(
    r"\b(?:href|src)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)
HTML_TAG_RE = re.compile(r"<[^>\n]+>")
BARE_HTTP_LINK_RE = re.compile(r"https?://[^\s<>\"]+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
DISALLOWED_FRONT_MATTER_KEYS = {
    "kernelspec",
    "language_info",
    "metadata",
    "nbformat",
    "nbformat_minor",
    "widgets",
}
LIST_FRONT_MATTER_KEYS = {"applications", "features", "tags"}
TEXT_FRONT_MATTER_KEYS = {"title", "seo_title", "description", "feature_image"}
WRITE_FILE_WHITELIST = {
    "fiber_lens.stl",
    "fiber_lens_params.npy",
    "inv_des_diamond_light_extractor.gds",
    "my_medium.json",
}
WRITE_METHODS = {
    "save",
    "savetxt",
    "to_file",
    "to_gds_file",
    "to_stl",
    "write_gds",
}
WRITE_VAR_PATTERNS = {
    "gc_file",
    "history_fname",
    "history_file_path",
    "npy_export_path",
    "output_dir",
    "restart_fname",
    "stl_export_path",
}
KNOWN_EXTERNAL_CATALOG_SLUGS = frozenset(
    {
        "AntennaCharacteristics",
        "CPWRFPhotonics1",
        "CPWRFPhotonics2",
        "CharacteristicImpedanceCalculator",
        "CircularlyPolarizedPatchAntenna",
        "CoupledLineBandpassFilter",
        "DifferentialStripline",
        "EdgeFeedPatchAntennaBenchmark",
        "GroundedCPWViaFence",
        "HybridMicrostripCPWBandpassFilter",
        "LinearLumpedElements",
        "MicroringRFElectrode",
        "PlanarHelicalAntennaArray",
        "RFParameterSweep",
        "RadarAbsorbingMetamaterial",
        "SMAEdgeMount",
        "SIWCSRRFilter",
        "ThroughSiliconVia",
        "VaractorTunedPatchAntenna",
        "WPDHarmonicSuppression1",
        "WPDHarmonicSuppression2",
        "WPDHarmonicSuppression3",
        "WidebandBeamSteerableReflectarrayWithPRUC",
    }
)
IGNORED_LINK_SCHEMES = {"data", "javascript", "mailto", "tel"}
REACHABLE_WITH_LIMITED_ACCESS_HTTP_STATUSES = {401, 403}
LINKCHECK_USER_AGENT = "tidy3d-notebook-linkcheck/1.0 (+https://www.flexcompute.com)"
TIDY3D_NOTEBOOK_DOCS_BASE_URL = "https://docs.flexcompute.com/projects/tidy3d/en/latest/notebooks/"
DEFAULT_LINKCHECK_TIMEOUT_SECONDS = 10.0
DEFAULT_LINKCHECK_WORKERS = 16
MAX_FRAGMENT_HTML_BYTES = 5_000_000


@dataclass(frozen=True)
class QmdDocument:
    path: Path
    front_matter: dict[str, Any]
    body: str
    body_start_line: int


@dataclass(frozen=True)
class PythonFence:
    start_line: int
    end_line: int
    code: str


@dataclass(frozen=True)
class TextLine:
    line_number: int
    text: str
    source: str


@dataclass(frozen=True)
class NotebookLink:
    document: QmdDocument
    line_number: int
    target: str
    source: str


class HtmlAnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and name.lower() in {"id", "name"}:
                self.anchors.add(html.unescape(value))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


@dataclass(frozen=True)
class CatalogNotebook:
    slug: str
    section_type: str | None


@dataclass(frozen=True)
class RuffCodeFile:
    path: Path
    document: QmdDocument
    fence: PythonFence


@dataclass(frozen=True)
class RuffCheckSourceMap:
    path: Path
    document: QmdDocument
    generated_to_qmd_line: dict[int, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Tidy3D notebook source root. Defaults to the parent of scripts/.",
    )
    parser.add_argument(
        "--changed-files-file",
        type=Path,
        help="Repository-relative changed-file list. Changed QMDs get spellchecked and Ruff-checked.",
    )
    parser.add_argument(
        "--notebooks",
        nargs="*",
        default=None,
        help="Explicit QMD paths or slugs to spellcheck and Ruff-check.",
    )
    parser.add_argument(
        "--all-notebooks",
        action="store_true",
        help="Spellcheck and Ruff-check every QMD file.",
    )
    parser.add_argument(
        "--skip-spellcheck",
        action="store_true",
        help="Skip spelling checks.",
    )
    parser.add_argument(
        "--skip-ruff-code",
        action="store_true",
        help="Skip Ruff syntax checks for QMD Python code fences.",
    )
    parser.add_argument(
        "--skip-linkcheck",
        action="store_true",
        help="Skip reachability checks for links in selected QMD files.",
    )
    parser.add_argument(
        "--fix-ruff-code",
        action="store_true",
        help="Apply Ruff fixes to selected QMD Python code fences and write them back.",
    )
    parser.add_argument(
        "--ruff-select",
        default=None,
        help=(
            "Comma-separated Ruff rules for QMD Python code checks. Defaults to the "
            "tidy3d-notebooks Ruff profile, or E with --fix-ruff-code. With "
            "--fix-ruff-code, only E selectors are allowed."
        ),
    )
    parser.add_argument(
        "--reference-threshold",
        type=int,
        default=3,
        help="Ignore words that appear in at least this many other QMD files.",
    )
    parser.add_argument(
        "--link-timeout",
        type=float,
        default=DEFAULT_LINKCHECK_TIMEOUT_SECONDS,
        help="Per-request timeout in seconds for HTTP link checks.",
    )
    parser.add_argument(
        "--link-workers",
        type=int,
        default=DEFAULT_LINKCHECK_WORKERS,
        help="Maximum concurrent HTTP link checks.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    args = parser.parse_args()
    if args.skip_ruff_code and args.fix_ruff_code:
        parser.error("--skip-ruff-code cannot be used with --fix-ruff-code")
    return args


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print(f"\nFound {len(errors)} notebook lint issue(s):\n")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)


def read_yaml_file(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def parse_qmd(path: Path) -> QmdDocument:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")

    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML front matter")

    raw_front_matter = text[4:end]
    body_start = end + len("\n---")
    body_start_line = text[:body_start].count("\n") + 1
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
        body_start_line += 1

    try:
        parsed = yaml.safe_load(raw_front_matter) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML front matter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("front matter must be a YAML mapping")
    return QmdDocument(
        path=path,
        front_matter=parsed,
        body=text[body_start:],
        body_start_line=body_start_line,
    )


def load_qmd_documents(root: Path) -> dict[str, QmdDocument]:
    documents: dict[str, QmdDocument] = {}
    errors: list[str] = []
    for path in sorted(root.glob("*.qmd")):
        try:
            documents[path.stem] = parse_qmd(path)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
    fail(errors)
    return documents


def validate_front_matter(root: Path, documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    for slug, document in documents.items():
        metadata = document.front_matter
        prefix = document.path.name

        unknown_notebook_metadata = DISALLOWED_FRONT_MATTER_KEYS & metadata.keys()
        if unknown_notebook_metadata:
            fields = ", ".join(sorted(unknown_notebook_metadata))
            errors.append(f"{prefix}: remove migrated notebook JSON metadata keys: {fields}")

        title = metadata.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{prefix}: front matter must define a non-empty title")

        jupyter = metadata.get("jupyter")
        if jupyter is not None and jupyter != "python3":
            errors.append(
                f"{prefix}: front matter jupyter may be omitted, but if present must use "
                "scalar 'jupyter: python3'"
            )

        for key in TEXT_FRONT_MATTER_KEYS - {"title"}:
            value = metadata.get(key)
            if value is not None and not isinstance(value, str):
                errors.append(f"{prefix}: {key} must be a string when present")

        for key in LIST_FRONT_MATTER_KEYS:
            value = metadata.get(key)
            if value is None:
                continue
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                errors.append(f"{prefix}: {key} must be a list of non-empty strings")

        feature_image = metadata.get("feature_image")
        if isinstance(feature_image, str) and feature_image.strip():
            image_path = Path(feature_image)
            if image_path.is_absolute() or ".." in image_path.parts:
                errors.append(f"{prefix}: feature_image must be relative to the notebook root")
            elif not (root / image_path).is_file():
                errors.append(f"{prefix}: feature_image does not exist: {feature_image}")

        if not SLUG_RE.match(slug):
            errors.append(f"{prefix}: QMD slug contains unsupported characters")

    return errors


def validate_quarto_project(root: Path, documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    config = read_yaml_file(root / "_quarto.yml")
    if not isinstance(config, dict):
        return ["_quarto.yml: project.render must be a list of QMD files"]

    project = config.get("project")
    if not isinstance(project, dict):
        return ["_quarto.yml: project.render must be a list of QMD files"]

    render = project.get("render")
    if not isinstance(render, list) or not all(isinstance(item, str) for item in render):
        return ["_quarto.yml: project.render must be a list of QMD files"]

    rendered = set(render)
    expected = {f"{slug}.qmd" for slug in documents}
    for filename in sorted(rendered - expected):
        errors.append(f"_quarto.yml: render entry has no QMD file: {filename}")
    for filename in sorted(expected - rendered):
        errors.append(f"_quarto.yml: missing render entry for {filename}")
    return errors


def collect_catalog_notebooks(
    node: dict[str, Any],
    errors: list[str],
    path: str = "_publication.yml",
    inherited_type: str | None = None,
) -> list[CatalogNotebook]:
    notebooks: list[CatalogNotebook] = []
    section_type = node.get("type", inherited_type)
    if section_type is not None and not isinstance(section_type, str):
        errors.append(f"{path}: type must be a string")
        section_type = inherited_type

    child_notebooks = node.get("notebooks", [])
    if child_notebooks:
        if not isinstance(child_notebooks, list):
            errors.append(f"{path}: notebooks must be a list")
        else:
            for notebook in child_notebooks:
                if isinstance(notebook, str):
                    notebooks.append(CatalogNotebook(notebook, section_type))
                else:
                    errors.append(f"{path}: notebook entries must be strings")

    child_sections = node.get("sections", [])
    if child_sections:
        if not isinstance(child_sections, list):
            errors.append(f"{path}: sections must be a list")
        else:
            for index, section in enumerate(child_sections):
                if not isinstance(section, dict):
                    errors.append(f"{path}.sections[{index}]: section must be a mapping")
                    continue
                title = section.get("title", f"section-{index}")
                notebooks.extend(
                    collect_catalog_notebooks(
                        section,
                        errors,
                        f"{path}.sections[{title!r}]",
                        section_type,
                    )
                )

    return notebooks


def validate_publication_catalog(root: Path, documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    catalog = read_yaml_file(root / "_publication.yml")
    if not isinstance(catalog, dict):
        return ["_publication.yml: expected a YAML mapping"]

    notebooks = collect_catalog_notebooks(catalog, errors)
    seen: set[str] = set()
    duplicates: set[str] = set()
    outside_corpus: list[str] = []
    for entry in notebooks:
        slug = entry.slug
        if not SLUG_RE.match(slug):
            errors.append(f"_publication.yml: unsupported notebook slug: {slug}")
        if slug in seen:
            duplicates.add(slug)
        seen.add(slug)
        if slug not in documents and slug not in KNOWN_EXTERNAL_CATALOG_SLUGS:
            outside_corpus.append(slug)

    for slug in sorted(duplicates):
        errors.append(f"_publication.yml: duplicate notebook slug: {slug}")

    for entry in notebooks:
        document = documents.get(entry.slug)
        if document is None or entry.section_type != "example-library":
            continue
        feature_image = document.front_matter.get("feature_image")
        if not isinstance(feature_image, str) or not feature_image.strip():
            errors.append(
                f"{document.path.name}: example-library notebooks must define feature_image"
            )

    uncataloged = sorted(set(documents) - seen)
    if outside_corpus:
        logging.warning(
            "_publication.yml references %d notebook(s) outside this QMD corpus: %s",
            len(outside_corpus),
            ", ".join(outside_corpus),
        )
    if uncataloged:
        logging.warning(
            "QMD files not present in _publication.yml: %s",
            ", ".join(uncataloged),
        )

    return errors


def load_import_mapping(root: Path) -> dict[str, list[str]]:
    path = root / "misc" / "import_file_mapping.json"
    content = path.read_text(encoding="utf-8")
    if content.startswith(GIT_LFS_POINTER_PREFIX):
        raise ValueError(IMPORT_MAPPING_LFS_MESSAGE)
    mapping = json.loads(content)
    if not isinstance(mapping, dict):
        raise ValueError("import_file_mapping.json must be an object")
    return mapping


def is_write_context(content: str, match_start: int) -> bool:
    lookback = content[max(0, match_start - 200) : match_start]
    if any(re.search(rf"\.?{re.escape(method)}\s*\([^)]*$", lookback) for method in WRITE_METHODS):
        return True
    return any(
        re.search(rf"{re.escape(var_pattern)}\s*=\s*(?:Path\()?[\"](?:\./)?$", lookback)
        or re.search(rf"{re.escape(var_pattern)}\s*=\s*(?:Path\()?['](?:\./)?$", lookback)
        for var_pattern in WRITE_VAR_PATTERNS
    )


def find_misc_references(document: QmdDocument) -> set[str]:
    references: set[str] = set()
    content = document.path.read_text(encoding="utf-8")
    for match in MISC_REF_RE.finditer(content):
        filename = match.group(1).strip()
        if (
            not filename
            or filename.startswith(".")
            or filename.endswith("_")
            or filename in WRITE_FILE_WHITELIST
            or is_write_context(content, match.start())
        ):
            continue
        references.add(filename)
    return references


def validate_import_mapping(root: Path, documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    misc_dir = root / "misc"
    misc_files = {
        path.relative_to(misc_dir).as_posix() for path in misc_dir.rglob("*") if path.is_file()
    }

    try:
        mapping = load_import_mapping(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"misc/import_file_mapping.json: {exc}"]

    validated_mapping: dict[str, set[str]] = {}
    for key, files in sorted(mapping.items()):
        if not key.endswith(".qmd"):
            errors.append(f"misc/import_file_mapping.json: mapping key must be QMD: {key}")
            continue
        slug = Path(key).stem
        if slug not in documents:
            errors.append(f"misc/import_file_mapping.json: mapping key has no QMD: {key}")
        if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
            errors.append(f"misc/import_file_mapping.json: {key} must map to a list of files")
            continue
        validated_mapping[key] = set(files)
        for filename in files:
            relative_path = PurePosixPath(filename)
            if (
                not filename
                or relative_path.is_absolute()
                or "." in relative_path.parts
                or ".." in relative_path.parts
            ):
                errors.append(f"misc/import_file_mapping.json: {key} uses invalid path: {filename}")
            elif relative_path.as_posix() not in misc_files:
                errors.append(
                    f"misc/import_file_mapping.json: {key} references missing file: {filename}"
                )

    for slug, document in documents.items():
        references = find_misc_references(document)
        if not references:
            continue
        declared_files = validated_mapping.get(f"{slug}.qmd", set())
        for filename in sorted(references):
            if filename not in misc_files:
                errors.append(f"{document.path.name}: references missing misc/{filename}")
            elif filename not in declared_files:
                errors.append(
                    f"{document.path.name}: misc/{filename} is not declared in import_file_mapping.json"
                )

    return errors


def strip_front_matter_and_code_fences(document: QmdDocument) -> list[TextLine]:
    lines = document.body.splitlines()
    text_lines: list[TextLine] = []
    in_code = False
    for index, line in enumerate(lines, start=1):
        if PYTHON_FENCE_RE.match(line):
            in_code = True
            continue
        if in_code:
            if FENCE_END_RE.match(line):
                in_code = False
            continue
        if line.strip().startswith("```"):
            in_code = True
            continue
        text_lines.append(
            TextLine(
                line_number=document.body_start_line + index - 1,
                text=markdown_to_text(line),
                source=line,
            )
        )
    return text_lines


def markdown_to_text(line: str) -> str:
    line = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    line = re.sub(r"https?://\S+", " ", line)
    line = re.sub(r"`[^`]+`", " ", line)
    line = re.sub(r"\$[^$]+\$", " ", line)
    line = re.sub(r"<[^>]+>", " ", line)
    line = html.unescape(line)
    return line


def extract_python_fences(document: QmdDocument) -> list[PythonFence]:
    fences: list[PythonFence] = []
    lines = document.body.splitlines()
    in_code = False
    start_line = 0
    current: list[str] = []

    for index, line in enumerate(lines, start=1):
        if not in_code and PYTHON_FENCE_RE.match(line):
            in_code = True
            start_line = document.body_start_line + index
            current = []
            continue
        if in_code and FENCE_END_RE.match(line):
            fences.append(
                PythonFence(
                    start_line=start_line,
                    end_line=document.body_start_line + index - 1,
                    code="\n".join(current),
                )
            )
            in_code = False
            current = []
            continue
        if in_code:
            current.append(line)

    return fences


def validate_python_fences(documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    for document in documents.values():
        in_code = False
        opening_line = 0
        for index, line in enumerate(document.body.splitlines(), start=1):
            if not in_code and PYTHON_FENCE_RE.match(line):
                in_code = True
                opening_line = document.body_start_line + index - 1
                continue
            if in_code and FENCE_END_RE.match(line):
                in_code = False
                opening_line = 0
        if in_code:
            errors.append(f"{document.path.name}:{opening_line}: unclosed Python code fence")
    return errors


def is_markdown_paragraph_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("#", ">", "|", "```", ":::", "$$")):
        return False
    if LIST_ITEM_RE.match(stripped):
        return False
    return not re.fullmatch(r"[-*_]{3,}", stripped)


def validate_list_spacing(documents: dict[str, QmdDocument]) -> list[str]:
    errors: list[str] = []
    for document in documents.values():
        previous_source_line = ""
        in_code = False
        for index, line in enumerate(document.body.splitlines(), start=1):
            line_number = document.body_start_line + index - 1
            stripped = line.strip()

            if in_code:
                if FENCE_END_RE.match(line):
                    in_code = False
                    previous_source_line = line
                continue

            if stripped.startswith("```"):
                in_code = True
                previous_source_line = line
                continue

            if ORDERED_LIST_START_RE.match(line) and is_markdown_paragraph_line(
                previous_source_line
            ):
                errors.append(
                    f"{document.path.name}:{line_number}: insert a blank line before "
                    f"ordered list item: {line.strip()}"
                )

            previous_source_line = line

    return errors


def iter_non_code_body_lines(document: QmdDocument) -> list[TextLine]:
    lines: list[TextLine] = []
    in_code = False
    in_html_comment = False
    for index, line in enumerate(document.body.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        uncommented_line, in_html_comment = remove_html_comments(line, in_html_comment)
        if not uncommented_line.strip():
            continue
        lines.append(
            TextLine(
                line_number=document.body_start_line + index - 1,
                text=strip_inline_code_spans(uncommented_line),
                source=line,
            )
        )
    return lines


def remove_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    chunks: list[str] = []
    index = 0
    while index < len(line):
        if in_comment:
            end = line.find("-->", index)
            if end == -1:
                return "".join(chunks), True
            index = end + len("-->")
            in_comment = False
            continue

        start = line.find("<!--", index)
        if start == -1:
            chunks.append(line[index:])
            break
        chunks.append(line[index:start])
        index = start + len("<!--")
        in_comment = True
    return "".join(chunks), in_comment


def strip_inline_code_spans(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def extract_links_from_qmd(document: QmdDocument) -> list[NotebookLink]:
    links: list[NotebookLink] = []
    seen: set[tuple[int, str]] = set()
    for text_line in iter_non_code_body_lines(document):
        line = text_line.text
        consumed_spans: list[tuple[int, int]] = []

        for regex in (MARKDOWN_LINK_RE, REFERENCE_LINK_RE):
            for match in regex.finditer(line):
                raw_target = next((group for group in match.groups() if group is not None), "")
                target = normalize_link_target(raw_target)
                add_link_if_new(document, text_line, target, links, seen)
                consumed_spans.append(match.span())

        for tag_match in HTML_TAG_RE.finditer(line):
            for match in HTML_LINK_ATTR_RE.finditer(tag_match.group(0)):
                raw_target = next((group for group in match.groups() if group is not None), "")
                target = normalize_link_target(raw_target)
                add_link_if_new(document, text_line, target, links, seen)
                consumed_spans.append(
                    (
                        tag_match.start() + match.start(),
                        tag_match.start() + match.end(),
                    )
                )

        for match in BARE_HTTP_LINK_RE.finditer(line):
            if any(spans_overlap(match.span(), span) for span in consumed_spans):
                continue
            target = strip_trailing_url_punctuation(match.group(0))
            add_link_if_new(document, text_line, target, links, seen)

    return links


def add_link_if_new(
    document: QmdDocument,
    text_line: TextLine,
    target: str,
    links: list[NotebookLink],
    seen: set[tuple[int, str]],
) -> None:
    key = (text_line.line_number, target)
    if key in seen:
        return
    seen.add(key)
    links.append(
        NotebookLink(
            document=document,
            line_number=text_line.line_number,
            target=target,
            source=text_line.source,
        )
    )


def normalize_link_target(raw_target: str) -> str:
    target = html.unescape(raw_target.strip())
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    if any(character.isspace() for character in target):
        target = target.split(maxsplit=1)[0]
    return target.strip()


def strip_trailing_url_punctuation(url: str) -> str:
    while url and url[-1] in ".,;:":
        url = url[:-1]
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    while url.endswith("]") and url.count("[") < url.count("]"):
        url = url[:-1]
    return url


def spans_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def check_links(
    root: Path,
    documents: dict[str, QmdDocument],
    selected_slugs: list[str],
    *,
    timeout: float,
    workers: int,
) -> list[str]:
    if not selected_slugs:
        print("No changed QMD files selected for link checks.")
        return []

    links = [
        link
        for slug in selected_slugs
        for link in extract_links_from_qmd(documents[slug])
        if should_check_link_target(link.target)
    ]
    errors: list[str] = []
    http_checks: list[tuple[NotebookLink, str]] = []
    for link in links:
        if not link.target:
            errors.append(format_link_error(link, "empty link target"))
            continue
        scheme = urlsplit(link.target).scheme.lower()
        if scheme in {"http", "https"}:
            http_checks.append((link, link.target))
            continue
        local_error = check_local_link(root, documents, link.document, link.target)
        if local_error:
            published_url = published_docs_url_for_relative_link(link.document, link.target)
            if published_url:
                http_checks.append((link, published_url))
                continue
            errors.append(format_link_error(link, local_error))

    http_results = check_http_links(
        {checked_target for _, checked_target in http_checks},
        timeout=timeout,
        workers=workers,
    )
    for link, checked_target in http_checks:
        http_error = http_results.get(checked_target)
        if http_error:
            if checked_target != link.target:
                http_error = f"{http_error} when resolved as {checked_target}"
            errors.append(format_link_error(link, http_error))

    return errors


def should_check_link_target(target: str) -> bool:
    if target.startswith("#"):
        return False
    scheme = urlsplit(target).scheme.lower()
    return scheme not in IGNORED_LINK_SCHEMES


def check_local_link(
    root: Path,
    documents: dict[str, QmdDocument],
    document: QmdDocument,
    target: str,
) -> str | None:
    split_target = urlsplit(target)
    if split_target.scheme:
        return f"unsupported link scheme: {split_target.scheme}"
    if split_target.netloc:
        return "protocol-relative links must use https://"
    if not split_target.path:
        return None

    raw_path = unquote(split_target.path)
    if raw_path.startswith("/"):
        return "site-root links must use an absolute URL"
    candidate = (document.path.parent / raw_path).resolve()
    if candidate.exists():
        return None

    path = Path(raw_path)
    if path.suffix == ".html":
        qmd_candidate = candidate.with_suffix(".qmd")
        if qmd_candidate.exists():
            return None

    root_candidate = (root / raw_path).resolve()
    if root_candidate.exists():
        return None

    return f"local link target does not exist: {target}"


def published_docs_url_for_relative_link(document: QmdDocument, target: str) -> str | None:
    split_target = urlsplit(target)
    if split_target.scheme or split_target.netloc or not split_target.path:
        return None
    raw_path = unquote(split_target.path)
    if raw_path.startswith("/") or not should_resolve_against_published_docs(raw_path):
        return None
    if PurePosixPath(raw_path).suffix == ".rst":
        split_target = split_target._replace(
            path=str(PurePosixPath(split_target.path).with_suffix(".html"))
        )
    base_url = f"{TIDY3D_NOTEBOOK_DOCS_BASE_URL}{document.path.stem}.html"
    return urljoin(base_url, split_target.geturl())


def should_resolve_against_published_docs(path: str) -> bool:
    relative_path = PurePosixPath(path)
    return (
        path.startswith("../")
        and "notebooks" not in relative_path.parts
        and relative_path.suffix in {".html", ".rst"}
    )


def check_http_links(
    targets: set[str],
    *,
    timeout: float,
    workers: int,
) -> dict[str, str | None]:
    if not targets:
        return {}
    targets_by_page: dict[str, list[str]] = {}
    for target in sorted(targets):
        targets_by_page.setdefault(http_url_without_fragment(target), []).append(target)

    max_workers = max(1, min(workers, len(targets_by_page)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_targets = {
            executor.submit(
                check_http_link_group, tuple(page_targets), timeout=timeout
            ): page_targets
            for page_targets in targets_by_page.values()
        }
        results: dict[str, str | None] = {}
        for future in concurrent.futures.as_completed(future_to_targets):
            page_targets = future_to_targets[future]
            try:
                results.update(future.result())
            except Exception as exc:  # pragma: no cover - defensive guard for CI linting
                for target in page_targets:
                    results[target] = f"HTTP link check failed unexpectedly: {exc}"
        return results


def check_http_link(url: str, *, timeout: float) -> str | None:
    return check_http_link_group((url,), timeout=timeout)[url]


def check_http_link_group(
    urls: tuple[str, ...],
    *,
    timeout: float,
) -> dict[str, str | None]:
    last_error: str | None = None
    base_url = http_url_without_fragment(urls[0])
    fragments = {url: unquote(urlsplit(url).fragment) for url in urls}
    needs_body = any(fragments.values())
    request_plan = [("HEAD", False), ("GET", needs_body)]
    while request_plan:
        method, fetch_body = request_plan.pop(0)
        request = Request(
            base_url,
            method=method,
            headers=http_link_headers(method, fetch_body=fetch_body),
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                status = response.getcode()
                if is_reachable_http_status(status):
                    if method == "HEAD" and needs_body:
                        continue
                    return http_link_results(
                        fragments,
                        response,
                        assume_valid_for_non_html=(
                            status not in REACHABLE_WITH_LIMITED_ACCESS_HTTP_STATUSES
                        ),
                    )
                last_error = f"HTTP {status}"
        except HTTPError as exc:
            if method == "HEAD":
                last_error = f"HTTP {exc.code}"
                continue
            if is_reachable_http_status(exc.code):
                return http_link_results(
                    fragments,
                    exc,
                    assume_valid_for_non_html=(
                        exc.code not in REACHABLE_WITH_LIMITED_ACCESS_HTTP_STATUSES
                    ),
                )
            if exc.code == 416 and request.get_header("Range"):
                last_error = f"HTTP {exc.code}: {exc.reason}"
                request_plan.insert(0, ("GET", True))
                continue
            error = f"HTTP {exc.code}: {exc.reason}"
            return dict.fromkeys(urls, error)
        except TimeoutError as exc:
            last_error = f"timeout: {exc}"
            if method == "HEAD":
                continue
        except (URLError, OSError) as exc:
            last_error = f"request failed: {format_url_error(exc)}"
            if method == "HEAD":
                continue
    return dict.fromkeys(urls, last_error)


def http_link_headers(method: str, *, fetch_body: bool = False) -> dict[str, str]:
    headers = {
        "Accept": "*/*",
        "User-Agent": LINKCHECK_USER_AGENT,
    }
    if method == "GET" and not fetch_body:
        headers["Range"] = "bytes=0-0"
    return headers


def http_link_results(
    fragments: dict[str, str],
    response: Any,
    *,
    assume_valid_for_non_html: bool = True,
) -> dict[str, str | None]:
    if not any(fragments.values()):
        return dict.fromkeys(fragments)

    headers = getattr(response, "headers", None)
    content_type = headers.get("Content-Type", "") if headers else ""
    if content_type and "html" not in content_type.lower() and "xml" not in content_type.lower():
        if assume_valid_for_non_html:
            return dict.fromkeys(fragments)
        anchors: set[str] = set()
    else:
        parser = HtmlAnchorCollector()
        try:
            body = response.read(MAX_FRAGMENT_HTML_BYTES)
        except (OSError, ValueError):
            body = b""
        if isinstance(body, str):
            parser.feed(body)
        else:
            parser.feed(body.decode("utf-8", errors="ignore"))
        anchors = parser.anchors

    return {
        target: (
            None if not fragment or fragment in anchors else f"missing URL fragment: #{fragment}"
        )
        for target, fragment in fragments.items()
    }


def is_reachable_http_status(status: int) -> bool:
    return 200 <= status < 400 or status in REACHABLE_WITH_LIMITED_ACCESS_HTTP_STATUSES


def format_url_error(exc: URLError | OSError) -> str:
    if isinstance(exc, URLError):
        return str(exc.reason)
    return str(exc)


def http_url_without_fragment(url: str) -> str:
    split_url = urlsplit(url)
    return urlunsplit(
        (
            split_url.scheme,
            split_url.netloc,
            split_url.path,
            split_url.query,
            "",
        )
    )


def format_link_error(link: NotebookLink, message: str) -> str:
    return (
        f"{link.document.path.name}:{link.line_number}: link: {message}: "
        f"{link.target} in {truncate_line(link.source.strip())}"
    )


def truncate_line(line: str, limit: int = 180) -> str:
    if len(line) <= limit:
        return line
    return f"{line[: limit - 3]}..."


def extract_identifiers_from_code(source: str) -> set[str]:
    identifiers: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return identifiers

    raw_identifiers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            raw_identifiers.add(node.id)
        elif isinstance(node, ast.Attribute):
            raw_identifiers.add(node.attr)
        elif isinstance(node, ast.arg):
            raw_identifiers.add(node.arg)
        elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            raw_identifiers.add(node.name)

    for identifier in raw_identifiers:
        words = re.sub("_", " ", identifier)
        words = re.sub(r"([a-z])([A-Z])", r"\1 \2", words)
        identifiers.update(word.lower() for word in words.split() if word)

    return identifiers


def extract_text_from_code(source: str) -> list[tuple[int, str, str]]:
    text_nodes: list[tuple[int, str, str]] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token_type, token_value, start, _, _ in tokens:
            row = start[0]
            if token_type == tokenize.STRING:
                try:
                    value = ast.literal_eval(token_value)
                except (MemoryError, SyntaxError, TypeError, ValueError):
                    value = token_value
                if isinstance(value, str):
                    text_nodes.append((row, value, token_value))
            elif token_type == tokenize.COMMENT:
                text_nodes.append((row, token_value.lstrip("#").strip(), token_value))
    except (IndentationError, SyntaxError, tokenize.TokenError):
        return []
    return text_nodes


def extract_text_from_qmd(document: QmdDocument) -> tuple[list[TextLine], set[str]]:
    texts: list[TextLine] = []
    identifiers: set[str] = set()

    for key in [
        "title",
        "seo_title",
        "description",
        "tags",
        "applications",
        "features",
    ]:
        value = document.front_matter.get(key)
        if isinstance(value, str):
            texts.append(TextLine(line_number=1, text=value, source=f"{key}: {value}"))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    texts.append(TextLine(line_number=1, text=item, source=f"{key}: {item}"))

    texts.extend(strip_front_matter_and_code_fences(document))
    for fence in extract_python_fences(document):
        identifiers.update(extract_identifiers_from_code(fence.code))
        for relative_line, text, source in extract_text_from_code(fence.code):
            texts.append(
                TextLine(
                    line_number=fence.start_line + relative_line - 1,
                    text=text,
                    source=source,
                )
            )

    return texts, identifiers


def get_all_words(document: QmdDocument) -> set[str]:
    texts, identifiers = extract_text_from_qmd(document)
    words = {word.lower() for word in identifiers}
    for text_line in texts:
        words.update(extract_words(text_line.text))
    return words


def build_reference_word_set(
    documents: dict[str, QmdDocument],
    selected_slugs: set[str],
    threshold: int,
) -> set[str]:
    if threshold <= 0:
        return set()

    word_counts: Counter[str] = Counter()
    for slug, document in documents.items():
        if slug in selected_slugs:
            continue
        word_counts.update(get_all_words(document))
    return {word for word, count in word_counts.items() if count >= threshold}


def extract_words(text: str) -> set[str]:
    if "\\" in text:
        return set()
    cleaned = re.sub(r"[\u2018\u2019]", "'", text)
    return {
        word.lower()
        for word in WORD_RE.findall(cleaned)
        if not word.isupper() and len(word.strip("'")) > 1
    }


def _has_close_correction(spell: SpellChecker, word: str) -> bool:
    """A word is an obvious typo only if a real dictionary word sits within the
    checker's edit-distance radius; novel jargon has no close neighbour."""
    candidates = spell.candidates(word)
    return bool(candidates) and candidates != {word}


def check_spelling(
    documents: dict[str, QmdDocument],
    selected_slugs: list[str],
    reference_threshold: int,
) -> list[str]:
    if not selected_slugs:
        print("No changed QMD files selected for spellcheck.")
        return []

    reference_words = build_reference_word_set(documents, set(selected_slugs), reference_threshold)
    base_spell = SpellChecker()
    if CUSTOM_DICT_PATH.is_file():
        base_spell.word_frequency.load_dictionary(str(CUSTOM_DICT_PATH))
    base_spell.word_frequency.load_words(reference_words)

    errors: list[str] = []
    for slug in selected_slugs:
        document = documents[slug]
        texts, identifiers = extract_text_from_qmd(document)
        notebook_spell = SpellChecker(language=None, distance=1)
        notebook_spell.word_frequency.load_words(base_spell.word_frequency.words())
        notebook_spell.word_frequency.load_words(identifiers)

        for text_line in texts:
            words = extract_words(text_line.text)
            if not words:
                continue
            unknown = notebook_spell.unknown(words)
            misspelled = sorted(
                word for word in unknown if _has_close_correction(notebook_spell, word)
            )
            if misspelled:
                errors.append(
                    f"{document.path.name}:{text_line.line_number}: spelling: "
                    f"{', '.join(misspelled)} in {text_line.source.strip()}"
                )

    return errors


def normalize_code_for_ruff(code: str) -> str:
    return (
        "\n".join(
            normalize_line_for_ruff(line_number, line)
            for line_number, line in enumerate(code.splitlines(), start=1)
        )
        + "\n"
    )


def normalize_line_for_ruff(line_number: int, line: str) -> str:
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]
    if is_quarto_cell_metadata_line(stripped):
        return f"{indent}# {QUARTO_METADATA_SENTINEL_PREFIX}{line_number}"
    if is_ipython_syntax_line(stripped):
        return f"{indent}# {IPYTHON_SENTINEL_PREFIX}{line_number}"
    return line


def is_quarto_cell_metadata_line(stripped_line: str) -> bool:
    return stripped_line.startswith("#|")


def is_ipython_syntax_line(stripped_line: str) -> bool:
    if not stripped_line or stripped_line.startswith("#"):
        return False
    if stripped_line.startswith(("!", "%", "?")):
        return True
    return is_ipython_help_syntax_line(stripped_line)


def is_ipython_help_syntax_line(stripped_line: str) -> bool:
    """Return whether a line looks like IPython object help syntax, e.g. `obj?`."""
    if not stripped_line.endswith("?") or python_source_parses(stripped_line):
        return False
    help_target = stripped_line.rstrip("?").rstrip()
    if not help_target:
        return False
    return python_source_parses(help_target)


def python_source_parses(source: str) -> bool:
    try:
        ast.parse(source)
    except (SyntaxError, ValueError):
        return False
    return True


def restore_qmd_code_from_ruff(original_code: str, fixed_code: str) -> tuple[str, bool]:
    """Map fixed Ruff temp source back to QMD code, restoring IPython syntax."""
    original_magic_lines: dict[str, str] = {}
    normalized_original_lines = normalize_code_for_ruff(original_code).rstrip("\n").splitlines()
    fixed_lines = fixed_code.rstrip("\n").splitlines()
    for line_number, line in enumerate(original_code.splitlines(), start=1):
        normalized = normalize_line_for_ruff(line_number, line)
        if normalized != line:
            original_magic_lines[normalized] = line

    original_magic_positions = magic_positions_in_non_blank_lines(
        normalized_original_lines,
        original_magic_lines,
    )
    fixed_magic_positions = magic_positions_in_non_blank_lines(
        fixed_lines,
        original_magic_lines,
    )
    if original_magic_positions != fixed_magic_positions:
        return "", False

    restored: list[str] = []
    restored_magic_lines: set[str] = set()
    duplicate_magic_lines: set[str] = set()
    for line in fixed_lines:
        original_line = original_magic_lines.get(line)
        if original_line is not None:
            if line in restored_magic_lines:
                duplicate_magic_lines.add(line)
            restored_magic_lines.add(line)
            restored.append(original_line)
        else:
            restored.append(line)

    all_magic_lines_restored = set(original_magic_lines) == restored_magic_lines
    return "\n".join(restored), all_magic_lines_restored and not duplicate_magic_lines


def magic_positions_in_non_blank_lines(
    lines: list[str],
    original_magic_lines: dict[str, str],
) -> list[tuple[int, str]]:
    """Return sentinel positions while ignoring Ruff-inserted blank separators."""
    positions: list[tuple[int, str]] = []
    non_blank_index = 0
    for line in lines:
        if not line.strip():
            continue
        if line in original_magic_lines:
            positions.append((non_blank_index, line))
        non_blank_index += 1
    return positions


def write_back_ruff_code_fixes(code_files: list[RuffCodeFile]) -> bool:
    """Write fixed Ruff temp files back into their original QMD Python fences."""
    files_by_document: dict[Path, list[tuple[PythonFence, str]]] = {}
    unsafe_fixes: list[str] = []
    for code_file in code_files:
        fixed_code = code_file.path.read_text(encoding="utf-8")
        original_code = normalize_code_for_ruff(code_file.fence.code)
        if fixed_code == original_code:
            continue
        restored_code, restored_safe = restore_qmd_code_from_ruff(
            code_file.fence.code,
            fixed_code,
        )
        if not restored_safe:
            unsafe_fixes.append(
                f"{code_file.document.path.name}:{code_file.fence.start_line}: "
                "Ruff produced fixes for a cell containing IPython syntax; edit manually."
            )
            continue
        files_by_document.setdefault(code_file.document.path, []).append(
            (code_file.fence, restored_code)
        )

    if unsafe_fixes:
        for message in unsafe_fixes:
            print(message, file=sys.stderr)
        return False

    for path, fixes in files_by_document.items():
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for fence, fixed_code in sorted(fixes, key=lambda item: item[0].start_line, reverse=True):
            replacement = [f"{line}\n" for line in fixed_code.splitlines()]
            start_index = fence.start_line - 1
            end_index = fence.end_line - 1
            lines[start_index:end_index] = replacement
        path.write_text("".join(lines), encoding="utf-8")
        print(f"Wrote Ruff fixes to {path}")

    return True


def write_notebook_code_for_ruff_check(document: QmdDocument, path: Path) -> RuffCheckSourceMap:
    """Write one normalized Python source file for all code fences in a notebook."""
    lines: list[str] = []
    generated_to_qmd_line: dict[int, int] = {}

    def append_line(line: str, qmd_line: int) -> None:
        lines.append(line)
        generated_to_qmd_line[len(lines)] = qmd_line

    for fence in extract_python_fences(document):
        if lines:
            append_line("", fence.start_line)
        append_line(
            f"# QMD cell starts at {display_path(document.path)}:{fence.start_line}",
            fence.start_line,
        )
        for offset, line in enumerate(
            normalize_code_for_ruff(fence.code).rstrip("\n").splitlines()
        ):
            append_line(line, fence.start_line + offset)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return RuffCheckSourceMap(
        path=path,
        document=document,
        generated_to_qmd_line=generated_to_qmd_line,
    )


def write_cell_code_for_ruff_fix(
    document: QmdDocument,
    temp_dir: Path,
) -> list[RuffCodeFile]:
    """Write one normalized Python source file per code fence for safe writeback."""
    code_files: list[RuffCodeFile] = []
    for index, fence in enumerate(extract_python_fences(document), start=1):
        path = temp_dir / f"{document.path.stem}_cell_{index}_line_{fence.start_line}.py"
        path.write_text(normalize_code_for_ruff(fence.code), encoding="utf-8")
        code_files.append(
            RuffCodeFile(
                path=path,
                document=document,
                fence=fence,
            )
        )
    return code_files


def check_python_code_with_ruff(
    documents: dict[str, QmdDocument],
    selected_slugs: list[str],
    *,
    fix: bool,
    ruff_select: str,
    use_default_ignores: bool = False,
) -> int:
    if not selected_slugs:
        print("No changed QMD files selected for Ruff code checks.")
        return 0

    if fix:
        unsafe_selectors = unsafe_ruff_writeback_selectors(ruff_select)
        if unsafe_selectors:
            print(
                "--fix-ruff-code only supports isolated-cell-safe Ruff selectors "
                f"(E). Rejected: {', '.join(unsafe_selectors)}",
                file=sys.stderr,
            )
            return 2
    with tempfile.TemporaryDirectory(prefix="tidy3d-qmd-ruff-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        cell_dir = temp_dir / "cells"
        notebook_dir = temp_dir / "notebooks"
        cell_dir.mkdir()
        notebook_dir.mkdir()
        code_files: list[RuffCodeFile] = []
        source_maps: dict[Path, RuffCheckSourceMap] = {}
        for slug in selected_slugs:
            document = documents[slug]
            code_files.extend(write_cell_code_for_ruff_fix(document, cell_dir))
            if not fix:
                source_map = write_notebook_code_for_ruff_check(
                    document,
                    notebook_dir / f"{slug}.py",
                )
                source_maps[source_map.path] = source_map

        if not code_files:
            return 0

        ruff_args = ruff_check_args(
            ruff_select,
            fix=fix,
            use_default_ignores=use_default_ignores,
        )
        if fix:
            ruff_args.append("--fix")
            ruff_args.append(cell_dir.as_posix())
        else:
            ruff_args.append("--output-format=concise")
            ruff_args.append(notebook_dir.as_posix())

        result = run_ruff(ruff_args, replay=fix)
        if not fix:
            replay_translated_ruff_output(result, source_maps)
        if fix and not write_back_ruff_code_fixes(code_files):
            return 1
        return result.returncode


def run_ruff(args: list[str], *, replay: bool = True) -> subprocess.CompletedProcess[str]:
    """Run Ruff from the pinned script environment, with PATH Ruff as a fallback."""
    pinned_result = subprocess.run(
        [sys.executable, "-m", "ruff", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if ruff_module_invocation_failed(pinned_result):
        ruff_path = shutil.which("ruff")
        if ruff_path:
            print(
                "Pinned Ruff module invocation failed; retrying with Ruff from PATH.",
                file=sys.stderr,
            )
            fallback_result = subprocess.run(
                [ruff_path, *args],
                check=False,
                capture_output=True,
                text=True,
            )
            if replay:
                replay_completed_process_output(fallback_result)
            return fallback_result

    if replay:
        replay_completed_process_output(pinned_result)
    return pinned_result


def replay_translated_ruff_output(
    result: subprocess.CompletedProcess[str],
    source_maps: dict[Path, RuffCheckSourceMap],
) -> None:
    if result.stdout:
        print(
            translate_ruff_concise_output(result.stdout, source_maps),
            end="",
            file=sys.stdout,
        )
    if result.stderr:
        print(
            translate_ruff_concise_output(result.stderr, source_maps),
            end="",
            file=sys.stderr,
        )


def translate_ruff_concise_output(
    output: str,
    source_maps: dict[Path, RuffCheckSourceMap],
) -> str:
    translated: list[str] = []
    for line in output.splitlines():
        match = RUFF_CONCISE_LOCATION_RE.match(line)
        if not match:
            translated.append(line)
            continue

        source_map = source_maps.get(Path(match.group("path")))
        if source_map is None:
            translated.append(line)
            continue

        generated_line = int(match.group("line"))
        qmd_line = source_map.generated_to_qmd_line.get(generated_line)
        if qmd_line is None:
            translated.append(line)
            continue

        translated.append(
            f"{display_path(source_map.document.path)}:"
            f"{qmd_line}:{match.group('column')}: {match.group('message')}"
        )
    return "\n".join(translated) + ("\n" if output.endswith("\n") else "")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def ruff_check_args(
    ruff_select: str,
    *,
    fix: bool = False,
    use_default_ignores: bool = False,
) -> list[str]:
    """Return Ruff args matching the legacy tidy3d-notebooks profile."""
    args = [
        "check",
        "--isolated",
        "--target-version",
        NOTEBOOK_RUFF_TARGET_VERSION,
        "--line-length",
        NOTEBOOK_RUFF_LINE_LENGTH,
        "--select",
        ruff_select,
    ]
    ignore_codes: list[str] = []
    if use_default_ignores:
        ignore_codes.extend(DEFAULT_RUFF_IGNORE_CODES)
    if fix:
        ignore_codes.extend(NOTEBOOK_RUFF_FIX_IGNORE_CODES)
    ignore_codes = list(dict.fromkeys(ignore_codes))
    if ignore_codes:
        args.extend(["--ignore", ",".join(ignore_codes)])
    if fix:
        args.append("--preview")
    return args


def ruff_module_invocation_failed(result: subprocess.CompletedProcess[str]) -> bool:
    """Return whether `python -m ruff` failed before Ruff handled the request."""
    if result.returncode == 0:
        return False
    stderr = result.stderr or ""
    return "No module named ruff" in stderr or ("FileNotFoundError" in stderr and "ruff" in stderr)


def replay_completed_process_output(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="", file=sys.stdout)
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def effective_ruff_select(ruff_select: str | None, *, fix: bool) -> str:
    """Return the Ruff selector implied by CLI defaults."""
    if ruff_select is not None:
        return ruff_select
    if fix:
        return DEFAULT_FIX_RUFF_SELECT
    return DEFAULT_RUFF_SELECT


def unsafe_ruff_writeback_selectors(ruff_select: str) -> list[str]:
    """Return Ruff selectors that are unsafe for isolated-cell QMD writeback."""
    selectors = [selector.strip() for selector in ruff_select.split(",") if selector.strip()]
    return [
        selector
        for selector in selectors
        if (
            not RUFF_WRITEBACK_SAFE_SELECTOR_RE.fullmatch(selector)
            or selector in RUFF_WRITEBACK_UNSAFE_SELECTORS
        )
    ]


def selected_slugs_from_args(
    root: Path,
    documents: dict[str, QmdDocument],
    changed_files_file: Path | None,
    notebooks: list[str] | None,
    all_notebooks: bool,
) -> list[str]:
    if all_notebooks:
        return sorted(documents)

    selected: set[str] = set()
    if notebooks:
        for notebook in notebooks:
            path = Path(notebook)
            selected.add(path.stem)

    if changed_files_file:
        root_relative = Path("flex/public/tidy3d/notebooks")
        for raw_line in changed_files_file.read_text(encoding="utf-8").splitlines():
            if not raw_line.strip() or not raw_line.endswith(".qmd"):
                continue
            path = Path(raw_line.strip())
            if path.parent == root_relative:
                selected.add(path.stem)
                continue
            if path.is_absolute() and path.parent == root:
                selected.add(path.stem)

    unknown = sorted(selected - set(documents))
    if unknown:
        raise ValueError(f"selected QMD files do not exist: {', '.join(unknown)}")
    return sorted(selected)


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    root = args.root.resolve()
    documents = load_qmd_documents(root)
    selected_slugs = selected_slugs_from_args(
        root=root,
        documents=documents,
        changed_files_file=args.changed_files_file,
        notebooks=args.notebooks,
        all_notebooks=args.all_notebooks,
    )

    errors: list[str] = []
    errors.extend(validate_front_matter(root, documents))
    errors.extend(validate_quarto_project(root, documents))
    errors.extend(validate_publication_catalog(root, documents))
    errors.extend(validate_import_mapping(root, documents))
    errors.extend(validate_python_fences(documents))
    errors.extend(validate_list_spacing(documents))
    fail(errors)

    print(f"Structural notebook checks passed for {len(documents)} QMD files.")
    if selected_slugs:
        print("Changed QMDs selected for spellcheck/Ruff/link checks: " + ", ".join(selected_slugs))

    if not args.skip_spellcheck:
        fail(check_spelling(documents, selected_slugs, args.reference_threshold))

    if not args.skip_ruff_code:
        ruff_exit = check_python_code_with_ruff(
            documents,
            selected_slugs,
            fix=args.fix_ruff_code,
            ruff_select=effective_ruff_select(args.ruff_select, fix=args.fix_ruff_code),
            use_default_ignores=args.ruff_select is None,
        )
        if ruff_exit:
            raise SystemExit(ruff_exit)

    if not args.skip_linkcheck:
        fail(
            check_links(
                root,
                documents,
                selected_slugs,
                timeout=args.link_timeout,
                workers=args.link_workers,
            )
        )

    print("Tidy3D notebook lint passed.")


if __name__ == "__main__":
    main()
