###############################################################################
# (c) Copyright 2025 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import ast
import json
import os
import re
import sys
from pathlib import Path
from subprocess import run

import pytest
import zstandard

EXAMPLES_DIR = Path(__file__).parent / "examples"
EXPECTED_DUMPS_DIR = Path(__file__).parent / "expected_dumps"

pytestmark = pytest.mark.slow


@pytest.mark.parametrize(
    "conf_fn, dump_fn",
    [
        ("prodConf_Moore_00241952_00148016_1.json", "00241952_00148016_1_dump.json"),
        ("prodConf_Moore_00153508_00000001_2.json", "00153508_00000001_2_dump.py"),
    ],
)
def test_dry_run(monkeypatch, tmp_path, conf_fn, dump_fn):
    monkeypatch.chdir(tmp_path)

    conf_path = EXAMPLES_DIR / conf_fn
    dump_path = EXPECTED_DUMPS_DIR / f"{dump_fn}.zst"
    expected_dump_raw = zstandard.decompress(dump_path.read_bytes())

    cmd = [sys.executable, "-m", "LbProdRun", "--gaudi-dry-run", str(conf_path)]
    env = os.environ | {"LBPRODRUN_OPTIONS_DUMP_DIR": str(tmp_path)}
    proc = run(cmd, capture_output=True, check=False, env=env)

    assert proc.returncode == 0, (proc.stdout, proc.stderr)

    match dump_path.suffixes[0]:
        case ".json":
            # Only appears for lbexec-style applications
            assert b"Not starting the application as this is a dry-run." in proc.stderr

            expected_dump = json.loads(expected_dump_raw)
            actual_dump = json.loads((tmp_path / dump_fn).read_text())
            # HltANNSvc.Repositories ends up depending on the current working directory
            # so remove it
            expected_dump.pop("HltANNSvc.Repositories", None)
            actual_dump.pop("HltANNSvc.Repositories", None)
            # The dumps are massive so make the error a bit more helpful
            assert set(actual_dump) - set(expected_dump) == set()
            assert set(expected_dump) - set(actual_dump) == set()
            for key in set(expected_dump) | set(actual_dump):
                assert expected_dump[key] == actual_dump[key]
        case ".py":
            # Convert the Python code to be Python 3 compatible:
            #   * 12L -> 12
            cleaner = re.compile(rb"(: \d+)L([,}])")
            expected_dump = ast.literal_eval(cleaner.sub(rb"\1\2", expected_dump_raw))
            actual_dump = ast.literal_eval(cleaner.sub(rb"\1\2", tmp_path / dump_fn))
            assert expected_dump == actual_dump
        case _:
            raise NotImplementedError(f"Unsupported dump file format: {dump_fn}")
