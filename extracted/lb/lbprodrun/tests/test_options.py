###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
from copy import deepcopy

import pytest

from LbProdRun.models import read_jobspec

BASE_JOB_SPEC = {
    "spec_version": 1,
    "application": {
        "name": "DaVinci",
        "version": "v45r8",
        "data_pkgs": ["AppConfig v3r405"],
        "number_of_processors": 2,
    },
    "options": {
        "format": "Merge",
        "files": [
            "$APPCONFIGOPTS/Merging/DVMergeDST.py",
            "$APPCONFIGOPTS/DaVinci/DataType-2017.py",
            "$APPCONFIGOPTS/Merging/WriteFSR.py",
            "$APPCONFIGOPTS/Merging/MergeFSR.py",
            "$APPCONFIGOPTS/Persistency/Compression-LZMA-4.py",
            "$APPCONFIGOPTS/DaVinci/Simulation.py",
        ],
        "gaudi_extra_options": "pass",
    },
    "input": {
        "files": [
            "LFN:/lhcb/MC/2018/D02HHLL.STRIP.MDST/00145917/0000/00145917_00000643_7.D02hhll.Strip.mdst",
            "LFN:/lhcb/MC/2018/D02HHLL.STRIP.MDST/00145917/0000/00145917_00000335_7.D02hhll.Strip.mdst",
        ],
        "xml_summary_file": "summaryDaVinci_00145918_00000004_1.xml",
        "xml_file_catalog": "pool_xml_catalog.xml",
    },
    "output": {
        "prefix": "00145918_00000004_1",
        "types": ["d02hhll.strip.mdst"],
    },
    "db_tags": {
        "dddb_tag": "dddb-20170721-3",
        "conddb_tag": "sim-20190430-vc-md100",
    },
}


def _write_job_spec(tmp_path, to_change):
    tmp_path = tmp_path / "prod_spec.json"
    job_spec = deepcopy(BASE_JOB_SPEC)
    for full_key, value in to_change.items():
        *parent_keys, final_key = full_key.split(".")
        obj = job_spec
        for key in parent_keys:
            obj = obj.setdefault(key, {})
        obj[final_key] = value
    tmp_path.write_text(json.dumps(job_spec))
    return tmp_path


@pytest.mark.parametrize(
    "to_change,expected",
    [
        [{}, ["gaudirun.py", "-T"]],
        [{"options.command": ["gaudirun.py"]}, ["gaudirun.py"]],
        [{"options.command": None}, ["gaudirun.py", "-T"]],
        [{"options.command": ["python"]}, ["python"]],
    ],
)
def test_options_command(tmp_path, to_change, expected):
    fn = _write_job_spec(tmp_path, to_change)
    parsed = read_jobspec(fn)
    assert parsed.options.command == expected
