"""The heavy stacks are optional extras (matrx_files._extras): the slim install imports and serves,
and a feature that needs an extra fails naming it.

The slim install is simulated in a fresh interpreter where every extra module is unimportable
(``sys.modules[name] = None`` makes ``import name`` raise ImportError), so this runs in the full
dev environment too.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

from matrx_files._extras import EXTRAS, MissingExtraError, require

PACKAGE = Path(__file__).resolve().parent.parent

#: Every module a slim host reaches: the package, its service, the scraper's PDF door, the image
#: pipeline, video, thumbnails, Office and the PDF subsystem.
SLIM_IMPORTS = [
    "matrx_files",
    "matrx_files.service",
    "matrx_files.specific_handlers.pdf",
    "matrx_files.specific_handlers.image_handler",
    "matrx_files.specific_handlers.image_ops",
    "matrx_files.specific_handlers.image_ops.bg_remove",
    "matrx_files.specific_handlers.image_ops.inpaint",
    "matrx_files.specific_handlers.image_ops.detect",
    "matrx_files.specific_handlers.image_ops.geometry",
    "matrx_files.specific_handlers.video_compose",
    "matrx_files.specific_handlers.video_handler",
    "matrx_files.specific_handlers.thumbnail_source",
    "matrx_files.specific_handlers.page_photos",
    "matrx_files.specific_handlers.office",
    "matrx_files.specific_handlers.pdf.extract",
    "matrx_files.specific_handlers.pdf.extract.text",
    "matrx_files.specific_handlers.pdf.extract.ocr",
]

SCRIPT = """
import importlib, json, sys
blocked = json.loads(sys.argv[1])
for name in blocked:
    sys.modules[name] = None
failed = {}
for mod in json.loads(sys.argv[2]):
    try:
        importlib.import_module(mod)
    except Exception as exc:
        failed[mod] = f"{type(exc).__name__}: {exc}"
from matrx_files._extras import require, MissingExtraError
from matrx_files.specific_handlers.pdf.internal import load_pymupdf
messages = {}
for extra, modules in json.loads(sys.argv[3]).items():
    try:
        require(modules[0], extra, "Feature")
    except MissingExtraError as exc:
        messages[extra] = str(exc)
try:
    load_pymupdf()
except MissingExtraError as exc:
    messages["load_pymupdf"] = str(exc)
print(json.dumps({"failed": failed, "messages": messages}))
"""


def _slim_run() -> dict[str, dict[str, str]]:
    blocked = sorted({m for mods in EXTRAS.values() for m in mods} | {"fitz", "pymatting", "scipy", "numba", "pandas"})
    out = subprocess.run(
        [sys.executable, "-c", SCRIPT, json.dumps(blocked), json.dumps(SLIM_IMPORTS), json.dumps(EXTRAS)],
        capture_output=True, text=True, check=True, timeout=120,
    )  # fmt: skip
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_slim_install_imports_every_surface_without_an_extra() -> None:
    assert _slim_run()["failed"] == {}


def test_a_missing_extra_is_named() -> None:
    messages = _slim_run()["messages"]
    for extra in EXTRAS:
        assert f"matrx-files[{extra}]" in messages[extra]
    assert "matrx-files[pdf]" in messages["load_pymupdf"]


def test_missing_extra_is_still_an_import_error() -> None:
    try:
        require("matrx_files_no_such_module", "media", "Test")
    except ImportError as exc:
        assert isinstance(exc, MissingExtraError)
        assert "matrx-files[media]" in str(exc)
    else:
        raise AssertionError("require() returned for a missing module")


def test_core_dependencies_carry_no_heavy_stack() -> None:
    project = tomllib.loads((PACKAGE / "pyproject.toml").read_text())["project"]
    heavy = ("rembg", "onnxruntime", "opencv", "numpy", "scipy", "numba", "pandas", "pymupdf", "imageio-ffmpeg",
             "pillow-heif", "pillow-avif", "pytesseract")  # fmt: skip
    core = [d.split(">")[0].split("=")[0].split("[")[0].strip().lower() for d in project["dependencies"]]
    assert not [d for d in core if d.startswith(heavy)], core
    extras = project["optional-dependencies"]
    for extra in ("pdf", "ocr", "media", "all"):
        assert extra in extras
