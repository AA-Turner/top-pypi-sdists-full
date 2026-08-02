# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression guard for filesystem ops that implicitly require Azure HNS.

PyArrow's ``AzureFileSystem`` probes the hierarchical-namespace endpoint
(``dfs.core.windows.net``) to choose between the DataLake and Blob APIs. The
probe fires not only on directory-semantic operations (``create_dir``,
``delete_dir``, ``delete_dir_contents``, ``delete_file``, ``move``) but also
when opening a stream for a write (``open_output_stream`` /
``open_append_stream`` decide create/overwrite semantics) — and the read-side
``open_input_stream`` / ``open_input_file`` go through the same filesystem. On
flat (non-HNS) accounts, or when that endpoint is unreachable, the probe fails
and aborts the operation even though the equivalent blob op would have
succeeded (GEN-645). Object stores have implicit directories, so these calls
are unnecessary on cloud stores and are only genuinely needed on local
filesystems.

This test fails if a new direct callsite for any forbidden op appears under
``src/geneva``. Checkpoint sidecar I/O routes through the Lance ``object_store``
session (``LanceFileSession.upload_file`` / ``download_file`` / ``delete_file``
/ ``contains``), which talks to the blob endpoint only and never probes HNS —
prefer that path. ``session.<op>(`` calls share these names but are blob-only,
so they are not violations. A site that genuinely needs the PyArrow filesystem
op — and tolerates the probe failure itself (e.g. a guarded best-effort delete,
or a read that does not trigger the directory probe) — must carry an opt-out
marker ``# hns-ok: <reason>`` on the call line or the line directly above it.
"""

import pathlib

_GENEVA_SRC = pathlib.Path(__file__).resolve().parents[1] / "geneva"
_MARKER = "hns-ok"
_FORBIDDEN = (
    ".create_dir(",
    ".delete_dir(",
    ".delete_dir_contents(",
    ".delete_file(",
    ".move(",
    ".open_output_stream(",
    ".open_append_stream(",
    ".open_input_stream(",
    ".open_input_file(",
)


def _code_part(line: str) -> str:
    """Return the line with any trailing comment stripped.

    A forbidden token that only appears inside a comment (prose or the
    opt-out marker itself) must not count as a callsite.
    """
    return line.split("#", 1)[0]


def test_no_unguarded_hns_filesystem_ops() -> None:
    violations: list[str] = []
    for path in sorted(_GENEVA_SRC.rglob("*.py")):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            code = _code_part(line)
            # LanceFileSession exposes some of the same method names but is
            # blob-only and never probes HNS, so `session.<op>(` is allowed.
            if not any(
                tok in code and ("session" + tok) not in code for tok in _FORBIDDEN
            ):
                continue
            prev = lines[i - 1] if i > 0 else ""
            if _MARKER in line or _MARKER in prev:
                continue
            rel = path.relative_to(_GENEVA_SRC.parent)
            violations.append(f"{rel}:{i + 1}: {line.strip()}")

    assert not violations, (
        "PyArrow filesystem op(s) that implicitly probe Azure HNS "
        "(create_dir/delete_dir/delete_dir_contents/delete_file/move/"
        "open_output_stream/open_append_stream/open_input_stream/"
        "open_input_file) must route through the Lance object_store session "
        "(LanceFileSession), or tolerate the dfs.core.windows.net probe failure "
        "and carry an opt-out comment '# hns-ok: <reason>':\n  "
        + "\n  ".join(violations)
    )
