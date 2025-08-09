import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from cwl_utils.parser import save
from CTADIRAC.Interfaces.API.CWLJob import CWLJob
from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    LFN_DIRAC_PREFIX,
    LFN_PREFIX,
)

INPUT_DATA = ["/ctao/user/MC/prod.sim", "/ctao/user/MC/prod2.sim"]
INPUT_SANDBOX = ["/a/local/MC/simulation.py", "/path/to/MC.prod3.sim"]
CWL_INPUTS_EXAMPLE = f"""
local_script:
  - class: File
    path: {INPUT_SANDBOX[0]}
input_as_lfn:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[0]}
input_as_lfn_2:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[1]}
  - class: File
    path: {INPUT_SANDBOX[1]}
dataset: "dataset://path/to/data"
input_param: "a random param"
"""
OUTPUT_DATA = ["/ctao/user/MC/fit*.out", "/ctao/usr/MC/data.sim"]
OUTPUT_SANDBOX = ["/path/to/test*.out", "/path/to/data_2.sim", "*.txt"]
BASE_COMMAND = "python"
IMAGE = "harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim"
CWL_WORKFLOW_EXAMPLE = f"""
cwlVersion: v1.2
class: CommandLineTool
doc: |
      Test using local input/output data treated as Dirac
      input/output sandboxes.

inputs:
  local_script:
    type: File
    inputBinding:
      position: 1
  input_as_lfn:
    type: File?
    inputBinding:
      position: 2
  input_as_lfn_2:
    type: File[]
    inputBinding:
      position: 3
  dataset:
    type: [File, string]
    inputBinding:
      position: 4
  input_param:
    type: string
    inputBinding:
      position: 5

outputs:
  output_as_sb:
    type: File[]?
    outputBinding:
      glob: ["{OUTPUT_SANDBOX[0]}"]
  output_as_lfn:
    type: File?
    label: "LFN wildcards"
    outputBinding:
      glob: "{LFN_PREFIX}{OUTPUT_DATA[0]}"
  output_as_lfn_2:
    type: File[]
    label: "LFN files list"
    outputBinding:
      glob:
        - {LFN_PREFIX}{OUTPUT_DATA[1]}
        - {OUTPUT_SANDBOX[1]}
  output_as_array:
    type:
      type: array
      items: File
    outputBinding:
      glob: "{OUTPUT_SANDBOX[2]}"

baseCommand: ["{BASE_COMMAND}"]

hints:
  DockerRequirement:
    dockerPull: {IMAGE}
"""

CWL_WORKFLOW_EXAMPLE_NO_INPUT = """
cwlVersion: v1.2
class: CommandLineTool
doc: |
      Test using local input/output data treated as Dirac
      input/output sandboxes.

inputs:
  local_script:
    type: string
    inputBinding:
      position: 1

outputs:
  output_as_sb:
    type: File[]?
    outputBinding:
      glob: ["/path/to/output_1.txt"]

baseCommand: ["base_command"]
"""
CWL_WORKFLOW_EXAMPLE_NO_INPUT_INPUTS = """
local_script: "test"
"""
CVMFS_BASE_PATH = Path("/cvmfs/ctao.dpps.test/")

# Input files
INPUT_1 = "gamma_1.dl1_img.h5"
INPUT_2 = "gamma_2.dl1_img.h5"

# Output files
MERGED_OUTPUT = "merged.dl1.h5"  # merged_output
MERGE_LOG = "ctapipe-merge.log"  # merge_log
MERGE_PROVENANCE_LOG = "ctapipe-merge.provenance.log"  # merge_provenance_log
INTERMEDIATE_LOG = "gamma_1.dl1.h5.log"  # intermediate_log
INTERMEDIATE_PROVENANCE_LOG = "gamma_1.dl1.h5.provlog"  # intermediate_log_provenance
INTERMEDIATE_LOG_2 = "gamma_2.dl1.h5.log"
INTERMEDIATE_PROVENANCE_LOG_2 = "gamma_2.dl1.h5.provlog"


@pytest.fixture
def mock_submit_job(mocker):
    return mocker.patch(
        "CTADIRAC.Interfaces.API.CWLJob.Dirac.submitJob",
        side_effect=lambda self: self._toXML(),
    )


def get_list(xml, name):
    element = xml.find(f".//Parameter[@name='{name}']/value")
    if element is None or element.text is None:
        return []
    return element.text.split(";")


@pytest.mark.parametrize(
    (
        "cwl_worflow",
        "cwl_inputs",
        "expected_input_data",
        "expected_input_sandbox",
        "expected_output_data",
        "expected_output_sandbox",
    ),
    [
        (
            CWL_WORKFLOW_EXAMPLE,
            CWL_INPUTS_EXAMPLE,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in INPUT_DATA],
            INPUT_SANDBOX,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in OUTPUT_DATA],
            OUTPUT_SANDBOX,
        ),
        (
            CWL_WORKFLOW_EXAMPLE_NO_INPUT,
            CWL_WORKFLOW_EXAMPLE_NO_INPUT_INPUTS,
            [],
            [],
            [],
            ["/path/to/output_1.txt"],
        ),
    ],
)
def test_cwl_job_submit(
    mock_submit_job,
    tmp_path,
    cwl_worflow,
    cwl_inputs,
    expected_input_data,
    expected_input_sandbox,
    expected_output_data,
    expected_output_sandbox,
):
    cwl_workflow_example = tmp_path / "cwl_workflow_example.cwl"
    cwl_workflow_example.write_text(cwl_worflow)
    cwl_inputs_example = tmp_path / "cwl_inputs_example.cwl"
    cwl_inputs_example.write_text(cwl_inputs)

    job = CWLJob(
        cwl_workflow=cwl_workflow_example,
        cwl_inputs=cwl_inputs_example,
        cvmfs_base_path=CVMFS_BASE_PATH,
        output_se="TEST_SE",
    )

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert input_data == expected_input_data

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert set(expected_output_sandbox).issubset(output_sandbox)

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert set(expected_input_sandbox).issubset(input_sandbox)

    output_data = get_list(result_xml, "OutputData")
    assert output_data == expected_output_data

    if expected_output_data:
        output_se_parameter = result_xml.find(".//Parameter[@name='OutputSE']")
        assert output_se_parameter is not None
        output_se = output_se_parameter.find("value")
        assert output_se is not None
        assert output_se.text == "TEST_SE"

    if executable := result_xml.find(
        ".//StepInstance/Parameter[@name='executable']/value"
    ):
        executable = executable.text
        assert executable == "cwltool"


def test_datapipe_cwl_job(mock_submit_job):
    job = CWLJob(
        "tests/resources/cwl/single_command_line_tool/process_dl0_dl1.cwl",
        "tests/resources/cwl/single_command_line_tool/inputs_process_dl0_dl1.yaml",
        cvmfs_base_path=CVMFS_BASE_PATH,
    )

    # these are set via inputs
    assert len(job.input_data) == 1
    assert (
        job.input_data[0]
        == "LFN:/ctao/simpipe/prod6/gamma-diffuse/010xxx/gamma_cone10_run010000.simtel.zst"
    )

    assert save(job.transformed_inputs) == {
        "dl0": {"class": "File", "path": "gamma_cone10_run010000.simtel.zst"},
        "processing_config": {"class": "File", "path": "process_config.yaml"},
        "dl1_filename": "test.dl1.h5",
    }

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert len(input_data) == 1
    assert (
        input_data[0]
        == "LFN:/ctao/simpipe/prod6/gamma-diffuse/010xxx/gamma_cone10_run010000.simtel.zst"
    )

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert len(input_sandbox) == 3
    assert "process_config.yaml" in input_sandbox[-1]

    output_data = get_list(result_xml, "OutputData")
    assert len(output_data) == 1
    assert output_data[0] == "LFN:/ctao/datapipe/test.dl1.h5"

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert len(output_sandbox) == 2
    assert output_sandbox == [
        "ctapipe-process.log",
        "ctapipe-process_dl0_dl1.provenance.log",
    ]


def test_datapipe_cwl_workflow_job(mock_submit_job):
    job = CWLJob(
        "tests/resources/cwl/scatter_feat_requirement/process_dl0_dl1_multiple.cwl",
        "tests/resources/cwl/scatter_feat_requirement/inputs_dl0_dl1_multiple.yaml",
        cvmfs_base_path=CVMFS_BASE_PATH,
    )
    assert len(job.input_data) == 0

    assert len(job.input_sandbox) == 2
    assert INPUT_1 in job.input_sandbox[0]
    assert INPUT_2 in job.input_sandbox[1]

    assert len(job.output_data) == 0
    assert job.output_sandbox == [
        MERGED_OUTPUT,
        MERGE_LOG,
        MERGE_PROVENANCE_LOG,
    ]

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert input_data == []

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert len(input_sandbox) == 4  # cwl + inputs + input_sandbox

    output_data = get_list(result_xml, "OutputData")
    assert len(output_data) == 0

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert len(output_sandbox) == 3
    assert output_sandbox[0] == MERGED_OUTPUT


# TODO: parametrize with the above test?
def test_datapipe_dl0_dl2_workflow(mock_submit_job):
    """Handling JS requirements."""
    job = CWLJob(
        "tests/resources/cwl/step_input_requirement/workflow_dl0_to_dl2.cwl",
        "tests/resources/cwl/step_input_requirement/inputs_workflow_dl0_to_dl2.yaml",
        cvmfs_base_path=CVMFS_BASE_PATH,
    )
    assert len(job.input_data) == 1
    assert job.input_data == [
        "LFN:/ctao/simpipe/prod6/gamma-diffuse/010xxx/gamma_prod5.simtel.zst"
    ]

    assert len(job.input_sandbox) == 0  # if no processing config

    assert len(job.output_data) == 0

    assert job.output_sandbox == ["gamma_prod5.dl1.h5", "gamma_prod5.dl2.h5"]

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert input_data == [
        "LFN:/ctao/simpipe/prod6/gamma-diffuse/010xxx/gamma_prod5.simtel.zst"
    ]

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert len(input_sandbox) == 2  # cwl + inputs

    output_data = get_list(result_xml, "OutputData")
    assert len(output_data) == 0

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert output_sandbox == ["gamma_prod5.dl1.h5", "gamma_prod5.dl2.h5"]


def test_scattered_expression_tool(mock_submit_job):
    job = CWLJob(
        "tests/resources/cwl/expression_tool_scatter/process_dl0_dl1_multiple.cwl",
        "tests/resources/cwl/expression_tool_scatter/inputs_process_multiple.yaml",
        cvmfs_base_path=CVMFS_BASE_PATH,
    )

    assert len(job.input_data) == 0

    assert len(job.input_sandbox) == 2
    assert INPUT_1 in job.input_sandbox[0]
    assert INPUT_2 in job.input_sandbox[1]

    assert len(job.output_data) == 0
    assert set(job.output_sandbox) == {
        MERGED_OUTPUT,
        MERGE_LOG,
        MERGE_PROVENANCE_LOG,
        INTERMEDIATE_LOG,
        INTERMEDIATE_LOG_2,
        INTERMEDIATE_PROVENANCE_LOG,
        INTERMEDIATE_PROVENANCE_LOG_2,
    }

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert input_data == []

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert len(input_sandbox) == 4  # cwl + inputs + input_sandbox

    output_data = get_list(result_xml, "OutputData")
    assert len(output_data) == 0

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert len(output_sandbox) == 7


def test_expression_tool(mock_submit_job):
    job = CWLJob(
        "tests/resources/cwl/expression_tool/process_dl0_dl1_multiple.cwl",
        "tests/resources/cwl/expression_tool/inputs_process_multiple.yaml",
        cvmfs_base_path=CVMFS_BASE_PATH,
    )

    assert len(job.input_data) == 0

    assert len(job.input_sandbox) == 1
    assert INPUT_1 in job.input_sandbox[0]

    assert len(job.output_data) == 0
    assert set(job.output_sandbox) == {
        MERGED_OUTPUT,
        MERGE_LOG,
        MERGE_PROVENANCE_LOG,
        INTERMEDIATE_LOG,
        INTERMEDIATE_PROVENANCE_LOG,
    }

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)

    input_data = get_list(result_xml, "InputData")
    assert input_data == []

    input_sandbox = get_list(result_xml, "InputSandbox")
    assert len(input_sandbox) == 3  # cwl + inputs + input_sandbox

    output_data = get_list(result_xml, "OutputData")
    assert len(output_data) == 0

    output_sandbox = get_list(result_xml, "OutputSandbox")
    assert len(output_sandbox) == 5
