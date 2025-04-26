###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging

import pytest

from DIRAC.Core.Base.AgentModule import AgentModule

from LHCbDIRAC.ProductionManagementSystem.Agent import HistogramMergingAgent as hma_module
from LHCbDIRAC.ProductionManagementSystem.Agent.HistogramMergingAgent import HistogramMergingAgent, AGENT_NAME

NUM_FILES = 10


def example_transformations():
    return [
        {
            "TransformationID": 1234,
            "TransformationFamily": "567",
            "Type": "MCSimulation",
            "Body": """<Workflow>
            <Parameter name="configName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ConfigName"><value><![CDATA[MC]]></value></Parameter>
            <Parameter name="configVersion" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ConfigVersion"><value><![CDATA[2018]]></value></Parameter>
            <Parameter name="eventType" type="string" linked_module="" linked_parameter="" in="True" out="False" description="Event Type of the production"><value><![CDATA[13264021]]></value></Parameter>
            <StepInstance>
            <name>Gauss_1</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Gauss]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            </Workflow>
            """,  # noqa # pylint: disable=line-too-long
        },
        {
            "TransformationID": 1235,
            "TransformationFamily": "567",
            "Type": "MCReconstruction",
            "Body": """<Workflow>
            <Parameter name="configName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ConfigName"><value><![CDATA[MC]]></value></Parameter>
            <Parameter name="configVersion" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ConfigVersion"><value><![CDATA[2018]]></value></Parameter>
            <Parameter name="eventType" type="string" linked_module="" linked_parameter="" in="True" out="False" description="Event Type of the production"><value><![CDATA[13264021]]></value></Parameter>
            <StepInstance>
            <name>Boole_1</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Boole]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>Moore_2</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Moore]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[l0app]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>Moore_3</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Moore]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>Moore_4</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Moore]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>Brunel_5</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[Brunel]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>DaVinci_6</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[DaVinci]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[Tesla]]></value></Parameter>
            </StepInstance>
            <StepInstance>
            <name>DaVinci_7</name>
            <Parameter name="applicationName" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ApplicationName"><value><![CDATA[DaVinci]]></value></Parameter>
            <Parameter name="optionsFormat" type="string" linked_module="" linked_parameter="" in="True" out="False" description="ProdConf configuration"><value><![CDATA[]]></value></Parameter>
            </StepInstance>
            </Workflow>
            """,  # noqa # pylint: disable=line-too-long
        },
    ]


STEPS = {
    "MCSimulation": ["Gauss"],
    "MCReconstruction": [
        "Boole",
        "Moore",  # L0
        "Moore",  # Hlt1
        "Moore",  # Hlt2
        "Brunel",
        "DaVinci",  # Turbo
        "DaVinci",  # Stripping
    ],
}

EXPECTED_YAML_FILES = {
    "MCSimulation": [
        "1-GAUSSHIST.yml",
    ],
    "MCReconstruction": [
        "1-BOOLEHIST.yml",
        "2-L0APPHIST.yml",
        "3-MOOREHIST.yml",
        "4-MOOREHIST.yml",
        "5-BRUNELHIST.yml",
        "6-TESLAHIST.yml",
        "7-DAVINCIHIST.yml",
    ],
}


def expected_modified_transformations():
    return [
        {
            "TransformationID": 1234,
            "TransformationFamily": "567",
            "Type": "MCSimulation",
            "Parameters": {
                "configName": "MC",
                "configVersion": "2018",
                "eventType": "13264021",
            },
            "Steps": {
                "Gauss_1": {
                    "applicationName": "Gauss",
                    "optionsFormat": None,
                }
            },
            "HistogramMerging": {
                "1-GAUSSHIST": {
                    "InputLFNs": [
                        f"/lhcb/MC/2018/GAUSSHIST/00001234/0000/Gauss_00001234_{job:08}_1.Hist.root"
                        for job in range(NUM_FILES)
                    ],
                    "InputPFNs": [
                        "root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2018/GAUSSHIST/00001234/0000/"
                        f"Gauss_00001234_{job:08}_1.Hist.root"
                        for job in range(NUM_FILES)
                    ],
                    "OutputLFN": "/lhcb/MC/2018/GAUSSHISTMERGED/00001234/0000/Gauss_00001234_0_1.Hist.root",
                },
            },
        },
        {
            "TransformationID": 1235,
            "TransformationFamily": "567",
            "Type": "MCReconstruction",
            "Parameters": {
                "configName": "MC",
                "configVersion": "2018",
                "eventType": "13264021",
            },
            "Steps": {
                "Boole_1": {
                    "applicationName": "Boole",
                    "optionsFormat": None,
                },
                "Moore_2": {
                    "applicationName": "Moore",
                    "optionsFormat": "l0app",
                },
                "Moore_3": {
                    "applicationName": "Moore",
                    "optionsFormat": None,
                },
                "Moore_4": {
                    "applicationName": "Moore",
                    "optionsFormat": None,
                },
                "Brunel_5": {
                    "applicationName": "Brunel",
                    "optionsFormat": None,
                },
                "DaVinci_6": {
                    "applicationName": "DaVinci",
                    "optionsFormat": "Tesla",
                },
                "DaVinci_7": {
                    "applicationName": "DaVinci",
                    "optionsFormat": None,
                },
            },
            "HistogramMerging": {
                f"{step_index}-{app.upper()}HIST": {
                    "InputLFNs": [
                        f"/lhcb/MC/2018/{app.upper()}HIST/00001235/0000/{app}_00001235_{job:08}_{step_index}.Hist.root"
                        for job in range(NUM_FILES)
                    ],
                    "InputPFNs": [
                        f"root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2018/{app.upper()}HIST/00001235/0000/"
                        f"{app}_00001235_{job:08}_{step_index}.Hist.root"
                        for job in range(NUM_FILES)
                    ],
                    "OutputLFN": f"/lhcb/MC/2018/{app.upper()}HISTMERGED/00001235/0000/"
                    f"{app}_00001235_0_{step_index}.Hist.root",
                }
                for step_index, app in enumerate(STEPS["MCReconstruction"], start=1)
            },
        },
    ]


def example_lfns():
    return [
        "/".join(
            [
                "/lhcb",
                transform["Parameters"]["configName"],
                transform["Parameters"]["configVersion"],
                f"{app.upper()}HIST",
                f"{transform['TransformationID']:08}",
                "0000",
                f"{app}_{transform['TransformationID']:08}_{job:08}_{step_index}.Hist.root",
            ]
        )
        for transform in expected_modified_transformations()
        for step_index, app in enumerate(STEPS[transform["Type"]], start=1)
        for job in range(NUM_FILES)
    ]


def example_requests():
    return {
        567: {
            "RequestID": "567",
            "RequestName": "",
            "RequestWG": "",
            "SimCondition": "",
            "SimCondDetail": "",
            "ProPath": "",
            "Extra": "",
            "RetentionRate": "",
            "FastSimulationType": "",
        }
    }


@pytest.fixture
def hma(monkeypatch):
    monkeypatch.setattr(AgentModule, "__init__", lambda *a, **kw: None)
    monkeypatch.setattr(AgentModule, "log", logging, raising=False)
    monkeypatch.setattr(AgentModule, "am_getOption", lambda _self, _name, default_value: default_value)
    # Values of module-level global variables that we want to change for testing
    global_values = {
        "gStandAlone": True,
        "gLocalWorkDir": True,
        "gDoRealMerging": False,
        "gDoRealUpdate": False,
        "gUseGitRepo": True,  # Can remain True while SimDQ repo is public, but we may run into issue of authentication later
    }
    for var, value in global_values.items():
        monkeypatch.setattr(hma_module, var, value)
    # Patch some of the query functions
    patched_functions = {
        "_latest_lbconda_env_version": "latest",  # original has @property dectorator
        "_query_recent_transformations": lambda _self: example_transformations(),
        "_query_requests": lambda _self, _request_ids: example_requests(),
        "_query_input_lfns": lambda _self, _transform_ids: example_lfns(),
    }
    for name, func in patched_functions.items():
        monkeypatch.setattr(HistogramMergingAgent, name, func)
    # Initialise the agent
    _hma = HistogramMergingAgent(AGENT_NAME, AGENT_NAME)
    _hma.initialize()
    _hma.beginExecution()
    yield _hma


def test_grouping(hma):
    """Test HistogramMergingAgent._group_lfns_by_prod_and_type"""
    expected = {
        transform["TransformationID"]: {
            file_key: merge_info["InputLFNs"] for file_key, merge_info in transform["HistogramMerging"].items()
        }
        for transform in expected_modified_transformations()
    }
    actual = hma._group_lfns_by_prod_and_type(example_lfns())  # pylint: disable=protected-access
    assert actual == expected


@pytest.mark.parametrize(
    "transform, expected_transform", zip(example_transformations(), expected_modified_transformations())
)
def test_xml_parsing(hma, transform, expected_transform):
    """Test HistogramMergingAgent._get_transformation_parameters"""
    workflow = hma._parse_workflow_xml(transform["Body"])  # pylint: disable=protected-access
    actual = hma._get_transformation_parameters(workflow)  # pylint: disable=protected-access
    expected = expected_transform["Parameters"]
    assert actual == expected


@pytest.mark.parametrize("transform", expected_modified_transformations())
def test_output_lfn(hma, transform):
    """Test HistogramMergingAgent._format_output_lfn"""
    for file_key, merge_info in transform["HistogramMerging"].items():
        actual = hma._format_output_lfn(transform, file_key)  # pylint: disable=protected-access
        expected = merge_info["OutputLFN"]
        assert actual == expected


def test_fetch_transformations(hma):
    """Test HistogramMergingAgent._fetch_transformations"""
    actual = hma._fetch_transformations()  # pylint: disable=protected-access
    expected = expected_modified_transformations()
    assert actual == expected


@pytest.mark.parametrize(
    "transform, production_request",
    zip(
        expected_modified_transformations(),
        [example_requests()[int(t["TransformationFamily"])] for t in expected_modified_transformations()],
    ),
)
def test_handle_transformation(hma, transform, production_request):
    """Test HistogramMergingAgent._handle_transformation"""
    new_yaml_files = [
        hma._handle_transformation(transform, production_request, file_key)  # pylint: disable=protected-access
        for file_key in transform["HistogramMerging"]
    ]
    merge_dir = hma.simdq_dir / transform["TransformationFamily"].rjust(8, "0") / transform["Parameters"]["eventType"]
    for actual, expected_fn in zip(new_yaml_files, EXPECTED_YAML_FILES[transform["Type"]]):
        expected = merge_dir / expected_fn
        assert actual == expected
        # TODO: check the contents of the file?


def test_execute(hma):
    """Test HistogramMergingAgent.execute"""
    ret = hma.execute()
    assert ret["OK"]
    for transform in expected_modified_transformations():
        merge_dir = (
            hma.simdq_dir / transform["TransformationFamily"].rjust(8, "0") / transform["Parameters"]["eventType"]
        )
        for yaml_fn in EXPECTED_YAML_FILES[transform["Type"]]:
            yaml_file = merge_dir / yaml_fn
            assert yaml_file.exists()
    # TODO: check the output
