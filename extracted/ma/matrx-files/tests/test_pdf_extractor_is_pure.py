"""The PDF text extractor stays pure (PDF-PLAN U2): bytes in, pages out, no database, no host.

Persistence - writing or reusing the ``docproc.processed_documents`` row - belongs to the CALLER
(``aidream/services/documents/persistence.py``). Two proofs: a source scan of the extraction
modules, and a run with the database layer made un-importable.
"""

from __future__ import annotations

import ast
import builtins
import importlib.util
import sys
from pathlib import Path

import pytest

_MATRX_FILES_SPEC = importlib.util.find_spec("matrx_files")
if _MATRX_FILES_SPEC is None or _MATRX_FILES_SPEC.origin is None:
    raise RuntimeError("matrx_files must be installed to inspect its PDF extractor source")
PDF_DIR = Path(_MATRX_FILES_SPEC.origin).resolve().parent / "specific_handlers" / "pdf"
#: Modules that extract text. None may reach a database, the ORM, storage or the host.
PURE_MODULES = [PDF_DIR / "extract" / "text.py", PDF_DIR / "extract" / "ocr.py"]
FORBIDDEN_ROOTS = {"matrx_orm", "aidream", "asyncpg", "psycopg", "psycopg2", "sqlalchemy", "supabase", "boto3", "db"}
FORBIDDEN_INTERNAL = ("matrx_files.db", "matrx_files.cloud_sync", "matrx_files.api", "matrx_files.storage")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            level = "." * node.level
            found.add(f"{level}{node.module or ''}")
    return found


@pytest.mark.parametrize("module", PURE_MODULES, ids=lambda p: p.name)
def test_the_extraction_modules_import_nothing_that_persists(module: Path) -> None:
    for name in _imports(module):
        assert name.split(".")[0] not in FORBIDDEN_ROOTS, f"{module.name} imports {name}"
        assert not name.startswith(FORBIDDEN_INTERNAL), f"{module.name} imports {name}"
        assert "persist" not in name.lower(), f"{module.name} imports {name}"


def test_extraction_runs_with_the_database_layer_unimportable(tmp_path, monkeypatch) -> None:
    pytest.importorskip("pikepdf")
    sys.path.insert(0, str(Path(__file__).parent))
    import _pdf_corpus as corpus  # noqa: PLC0415

    real_import = builtins.__import__

    def refuse(name, *args, **kwargs):
        if name.split(".")[0] in {"matrx_orm", "asyncpg"} or name.startswith("matrx_files.db"):
            raise AssertionError(f"the extractor imported {name} - extraction must not touch the database")
        return real_import(name, *args, **kwargs)

    from matrx_files.specific_handlers.pdf.extract.text import extract_text_pages

    item = corpus.digital()
    path = tmp_path / "d.pdf"
    path.write_bytes(item.data)
    monkeypatch.setattr(builtins, "__import__", refuse)
    pages = extract_text_pages(str(path))
    assert [corpus.collapse(p.text) for p in pages] == list(item.native_text)


def test_a_planted_database_import_in_an_extractor_is_caught(tmp_path) -> None:
    planted = tmp_path / "text.py"
    planted.write_text("from matrx_orm import transaction\n")
    assert any(name.split(".")[0] in FORBIDDEN_ROOTS for name in _imports(planted))
