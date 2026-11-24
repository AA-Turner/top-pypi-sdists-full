"""Both client upload doors take a PERSON pathway from upload metadata, by one rule.

A browser upload names its pathway as ``file_pathway`` in the upload metadata (resumable TUS and the
buffered ``POST /files/upload`` alike). The name is popped off the row metadata and stamped on the row
only when it is a declared PERSON pathway; automated pathways are server-only. Before this, the
buffered door kept ``file_pathway`` as a plain metadata key and never stamped the row.
Placement registry PLAN § 4.2a / S5.
"""

from __future__ import annotations

from pathlib import Path

import matrx_files
from matrx_files.placement import client_person_pathway

# The INSTALLED package, never a path relative to this file: the independence gate runs
# these tests from a copy of tests/ in an empty directory against a bare-venv install.
PKG = Path(matrx_files.__file__).resolve().parent


def test_person_pathway_is_popped_and_returned() -> None:
    meta = {"file_pathway": "files.user_upload", "origin": "x"}
    assert client_person_pathway(meta) == "files.user_upload"
    assert meta == {"origin": "x"}


def test_automated_and_undeclared_names_are_dropped() -> None:
    for name in ("files.variant", "no.such_pathway"):
        meta = {"file_pathway": name}
        assert client_person_pathway(meta) is None
        assert "file_pathway" not in meta


def test_no_name_is_none() -> None:
    assert client_person_pathway(None) is None
    assert client_person_pathway({"a": 1}) is None


def test_both_client_doors_use_the_one_rule() -> None:
    router = (PKG / "api/router_files.py").read_text()
    tus = (PKG / "cloud_sync/transports/tus.py").read_text()
    # The buffered door reads the client's metadata through the ONE rule (``client_upload_pathway``, which calls
    # ``client_person_pathway`` first); the literal it checked before the rule grew a path fallback went stale.
    assert "client_upload_pathway(parsed_meta" in router
    assert router.count("pathway=client_pathway") == 2, "buffered upload must pass the pathway to both write calls"
    assert "client_person_pathway(" in tus
