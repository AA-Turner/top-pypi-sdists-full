###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Test for Production Models"""
import pytest
import yaml
from pathlib import Path

from DIRAC import S_OK
from LHCbDIRAC.ProductionManagementSystem.Utilities.Models import parse_obj
from LHCbDIRAC.ProductionManagementSystem.Utilities.ModelCompatibility import (
    step_to_step_manager_dict,
    runs_to_input_query,
)

EXAMPLE_YAML_FILES = list((Path(__file__).parent / "example_yamls").glob("*.yaml"))


@pytest.mark.parametrize("yaml_path", EXAMPLE_YAML_FILES)
def test_models(yaml_path, monkeypatch):
    monkeypatch.setattr(
        "LHCbDIRAC.ProductionManagementSystem.Utilities.Models.getProxyInfo", lambda: S_OK({"username": "test_user"})
    )

    for pr in yaml.safe_load(yaml_path.read_text()):
        assert parse_obj(pr)


sprucing_expected_step_info = {
    "ApplicationName": "Moore",
    "ApplicationVersion": "v54r15",
    "CONDDB": "",
    "DDDB": "",
    "DQTag": "",
    "OptionFiles": (
        '{"entrypoint":"Hlt2Conf.Sprucing_production:pass_spruce_production",'
        '"extra_options":{"input_raw_format":0.5,"input_type":'
        '"RAW","simulation":false,"data_type":"Upgrade",'
        '"geometry_version":"trunk","conditions_version":"master",'
        '"compression":"ZSTD:1","output_type":"ROOT",'
        '"input_process":"Hlt2","process":"Spruce"},'
        '"extra_args":[]}'
    ),
    "ExtraPackages": "",
    "ProcessingPass": "SprucingPass23",
    "StepName": "Passthrough sprucing",
    "isMulticore": "N",
    "Visible": "Y",
    "mcTCK": "",
    "Usable": "Yes",
    "SystemConfig": "",
}


@pytest.mark.parametrize("yaml_path", EXAMPLE_YAML_FILES)
def test_step_to_step_manager_dict(yaml_path, monkeypatch):
    monkeypatch.setattr(
        "LHCbDIRAC.ProductionManagementSystem.Utilities.Models.getProxyInfo", lambda: S_OK({"username": "test_user"})
    )

    for pr in yaml.safe_load(yaml_path.read_text()):
        p = parse_obj(pr)
        for j, step in enumerate(p.steps, start=1):
            step_info = step_to_step_manager_dict(j, step)
            if step.processing_pass == "SprucingPass23":
                assert step_info["Step"] == sprucing_expected_step_info
                assert step_info["InputFileTypes"] == [
                    {"FileType": "MDF", "Visible": "Y"},
                ]
                assert step_info["OutputFileTypes"] == [
                    {"FileType": "SL.DST", "Visible": "N"},
                    {"FileType": "CHARM.DST", "Visible": "N"},
                    {"FileType": "B2CC.DST", "Visible": "N"},
                    {"FileType": "RD.DST", "Visible": "N"},
                    {"FileType": "BANDQ.DST", "Visible": "N"},
                    {"FileType": "QEE.DST", "Visible": "N"},
                    {"FileType": "B2OC.DST", "Visible": "N"},
                    {"FileType": "BNOC.DST", "Visible": "N"},
                ]


@pytest.mark.parametrize(
    "runs, expected",
    [
        ([], ""),
        ([1], "1"),
        (["34"], "34"),
        (["34", "35"], "34,35"),
        (["34:36"], "34,35,36"),
        (["34:36", "38"], "34,35,36,38"),
        (["34:36", "38:40"], "34,35,36,38,39,40"),
    ],
)
def test_runs_to_input_query(runs, expected):
    assert ",".join(runs_to_input_query(runs)) == expected
