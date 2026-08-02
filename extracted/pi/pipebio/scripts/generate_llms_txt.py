#!/usr/bin/env python3
"""Generate AI-context artifacts for the PipeBio Python SDK.

This walks the public SDK surface (the service classes, helper functions and
model enums) by introspection and emits two files into the ``pipebio`` package:

* ``pipebio/llms.txt`` - a concise index: one entry per public class / method /
  function with its signature and the first line of its docstring.
* ``pipebio/llms-full.txt`` - the full reference: signatures plus complete
  docstrings.

Both files are bundled into the published wheel/sdist (see
``[tool.setuptools.package-data]`` in ``pyproject.toml``) so that, once a
customer runs ``pip install pipebio``, an AI coding agent working in their
project can read them directly from ``site-packages`` with no repository access.

Usage (from the repository root):

    python scripts/generate_llms_txt.py          # regenerate the files
    python scripts/generate_llms_txt.py --check   # fail if they are out of date

The package must be importable (e.g. ``uv pip install ".[dev,build]"``) because
the generator imports the modules to read their real signatures and docstrings.
"""

import argparse
import enum
import importlib
import inspect
import sys
from pathlib import Path
from typing import Any, List

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = REPO_ROOT / "pipebio"
INDEX_PATH = PACKAGE_DIR / "llms.txt"
FULL_PATH = PACKAGE_DIR / "llms-full.txt"

# The curated public surface. Internal helpers (leading underscore) and modules
# not listed here are intentionally excluded - this mirrors the customer-facing
# focus documented in agent.md.
PUBLIC_MODULES: List[str] = [
    "pipebio.pipebio_client",
    "pipebio.entities",
    "pipebio.jobs",
    "pipebio.sequences",
    "pipebio.workflows",
    "pipebio.shareables",
    "pipebio.organization_lists",
    "pipebio.uploader",
    "pipebio.multipart_upload",
    "pipebio.column",
    "pipebio.models.job_type",
    "pipebio.models.job_status",
    "pipebio.models.job_filter",
    "pipebio.models.entity_types",
    "pipebio.models.export_format",
    "pipebio.models.table_column_type",
    "pipebio.models.render_codes",
    "pipebio.models.sort",
]

HEADER = """\
# PipeBio Python SDK

> A Python SDK for the PipeBio platform - an integrated bioinformatics platform
> for large molecule and peptide discovery. This file is auto-generated from the
> SDK source by scripts/generate_llms_txt.py; do not edit by hand.

## Getting started

- Install: `pip install pipebio` (or `uv pip install pipebio`).
- Authenticate: set the `PIPE_API_KEY` environment variable (get a key from the
  `me` page of your PipeBio instance), or place it in a local `.env` file.
- Create a client and call resource services:

    from pipebio.pipebio_client import PipebioClient
    client = PipebioClient(url="https://app.pipebio.com")
    client.entities.get(entity_id)

- Escape hatch: for endpoints not yet wrapped by the SDK, use the authenticated
  `client.session` directly, e.g. `client.session.get("me")`.
"""


def _first_line(doc: str | None) -> str:
    """Return the first non-empty line of a docstring, or a placeholder."""
    if not doc:
        return "(no description)"
    for line in doc.strip().splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "(no description)"


def _signature(obj: Any) -> str:
    """Return a best-effort ``inspect.signature`` string, or ``()`` on failure."""
    try:
        return str(inspect.signature(obj))
    except (ValueError, TypeError):
        return "(...)"


def _public_methods(cls: type) -> List[tuple[str, Any, bool]]:
    """Return the public methods/properties of a class, sorted by name.

    Each entry is ``(name, func, is_property)`` where ``func`` is the underlying
    callable (the getter for properties) and ``is_property`` marks attribute-style
    access so it can be rendered without a call signature.
    """
    members = []
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if inspect.isfunction(member) or inspect.ismethod(member):
            members.append((name, member, False))
        elif isinstance(member, property):
            members.append((name, member.fget, True))
    return sorted(members, key=lambda item: item[0])


def _return_annotation(obj: Any) -> str:
    """Return ``' -> Type'`` for a callable's return annotation, or ``''``."""
    try:
        signature = inspect.signature(obj)
    except (ValueError, TypeError):
        return ""
    if signature.return_annotation is inspect.Signature.empty:
        return ""
    return f" -> {inspect.formatannotation(signature.return_annotation)}"


def _module_members(module: Any) -> tuple[list[type], list[Any]]:
    """Return classes and functions *defined in* the given module."""
    classes = []
    functions = []
    for name, member in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        if getattr(member, "__module__", None) != module.__name__:
            continue
        if inspect.isclass(member):
            classes.append(member)
        elif inspect.isfunction(member):
            functions.append(member)
    classes.sort(key=lambda c: c.__name__)
    functions.sort(key=lambda f: f.__name__)
    return classes, functions


def _render(full: bool) -> str:
    """Render the index (``full=False``) or full (``full=True``) document."""
    lines: List[str] = [HEADER, "## API reference\n"]

    for module_name in PUBLIC_MODULES:
        module = importlib.import_module(module_name)
        classes, functions = _module_members(module)
        if not classes and not functions:
            continue

        lines.append(f"### {module_name}\n")

        for cls in classes:
            if issubclass(cls, enum.Enum):
                values = ", ".join(member.name for member in cls)
                lines.append(f"- enum `{cls.__name__}`: {_first_line(cls.__doc__)}")
                lines.append(f"  - values: {values}")
                if full and cls.__doc__:
                    lines.append("")
                    lines.append(_indent(inspect.cleandoc(cls.__doc__), "    "))
                lines.append("")
                continue

            lines.append(f"- class `{cls.__name__}`: {_first_line(cls.__doc__)}")
            if full and cls.__doc__:
                lines.append("")
                lines.append(_indent(inspect.cleandoc(cls.__doc__), "    "))
                lines.append("")
            for name, method, is_property in _public_methods(cls):
                doc = method.__doc__
                if is_property:
                    rendered = f"  - property `{cls.__name__}.{name}{_return_annotation(method)}`"
                else:
                    rendered = f"  - `{cls.__name__}.{name}{_signature(method)}`"
                lines.append(f"{rendered}: {_first_line(doc)}")
                if full and doc:
                    lines.append("")
                    lines.append(_indent(inspect.cleandoc(doc), "      "))
                    lines.append("")
            lines.append("")

        for func in functions:
            signature = _signature(func)
            doc = func.__doc__
            lines.append(f"- `{func.__name__}{signature}`: {_first_line(doc)}")
            if full and doc:
                lines.append("")
                lines.append(_indent(inspect.cleandoc(doc), "    "))
                lines.append("")
        lines.append("")

    # Collapse trailing whitespace and guarantee a single trailing newline.
    text = "\n".join(lines).rstrip() + "\n"
    return text


def _indent(text: str, prefix: str) -> str:
    """Indent every line of ``text`` with ``prefix``."""
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed files differ from freshly generated ones.",
    )
    args = parser.parse_args()

    # Ensure the repo root is importable when run directly.
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    index_text = _render(full=False)
    full_text = _render(full=True)

    if args.check:
        stale = []
        for path, expected in ((INDEX_PATH, index_text), (FULL_PATH, full_text)):
            actual = path.read_text(encoding="utf-8") if path.exists() else None
            if actual != expected:
                stale.append(path.name)
        if stale:
            print(
                f"AI-context artifacts are out of date: {', '.join(stale)}. "
                f"Run `python scripts/generate_llms_txt.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("AI-context artifacts are up to date.")
        return 0

    INDEX_PATH.write_text(index_text, encoding="utf-8")
    FULL_PATH.write_text(full_text, encoding="utf-8")
    print(f"Wrote {INDEX_PATH.relative_to(REPO_ROOT)} and {FULL_PATH.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
