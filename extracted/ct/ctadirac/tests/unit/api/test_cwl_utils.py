from pathlib import Path

import pytest
from cwl_utils.parser.cwl_v1_2 import (
    CommandLineTool,
    CommandOutputArraySchema,
    CommandOutputBinding,
    CommandOutputParameter,
    DockerRequirement,
    File,
    Workflow,
    WorkflowStep,
)
from cwl_utils.parser import save

from CTADIRAC.Interfaces.Utilities.CWL_utils import (
    LFN_DIRAC_PREFIX,
    LFN_PREFIX,
    LOCAL_PREFIX,
    extract_and_translate_input_files,
    extract_output_files,
    set_input_file_basename,
    translate_clt,
    translate_cwl_workflow,
    translate_docker_hints,
    translate_sandboxes_and_lfns,
    translate_workflow,
    verify_cwl_output_type,
)


CVMFS_BASE_PATH = Path("/cvmfs/ctao.dpps.test")


@pytest.mark.parametrize(
    ("file_input", "expected_result", "expected_lfn"),
    [
        (
            File(path=LFN_PREFIX + "/ctao/test_lfn_file.txt"),
            LFN_DIRAC_PREFIX + "/ctao/test_lfn_file.txt",
            True,
        ),
        (
            File(path=LOCAL_PREFIX + "/home/user/test_local_file.txt"),
            "/home/user/test_local_file.txt",
            False,
        ),
        (
            LFN_PREFIX + "/ctao/test_lfn_str.txt",
            LFN_DIRAC_PREFIX + "/ctao/test_lfn_str.txt",
            True,
        ),
        (
            LOCAL_PREFIX + "/home/user/test_local_str.txt",
            "/home/user/test_local_str.txt",
            False,
        ),
        (File(), None, False),  # This will raise an exception
    ],
)
def test_translate_sandboxes_and_lfns(file_input, expected_result, expected_lfn):
    if expected_result is None:
        with pytest.raises(KeyError, match="File path is not defined."):
            translate_sandboxes_and_lfns(file_input)
    else:
        result, is_lfn = translate_sandboxes_and_lfns(file_input)
        assert result == expected_result
        assert is_lfn == expected_lfn


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {"input1": File(path=LFN_PREFIX + "/ctao/test_lfn_file.txt")},
            {
                "InputDesc": {"input1": File(path="test_lfn_file.txt")},
                "InputSandbox": [],
                "InputData": [LFN_DIRAC_PREFIX + "/ctao/test_lfn_file.txt"],
            },
        ),
        (
            {"input1": File(path=LOCAL_PREFIX + "test_local_file.txt")},
            {
                "InputDesc": {"input1": File(path="test_local_file.txt")},
                "InputSandbox": ["test_local_file.txt"],
                "InputData": [],
            },
        ),
        (
            {
                "input1": [
                    File(path=LFN_PREFIX + "/ctao/test_lfn_file1.txt"),
                    File(path=LOCAL_PREFIX + "test_local_file1.txt"),
                ]
            },
            {
                "InputDesc": {
                    "input1": [
                        File(path="test_lfn_file1.txt"),
                        File(path="test_local_file1.txt"),
                    ]
                },
                "InputSandbox": ["test_local_file1.txt"],
                "InputData": [LFN_DIRAC_PREFIX + "/ctao/test_lfn_file1.txt"],
            },
        ),
        (
            {
                "input1": File(path=LFN_PREFIX + "/ctao/test_lfn_file2.txt"),
                "input2": File(path=LOCAL_PREFIX + "test_local_file2.txt"),
                "input3": [
                    File(path=LFN_PREFIX + "/ctao/test_lfn_file3.txt"),
                    File(path=LOCAL_PREFIX + "test_local_file3.txt"),
                ],
            },
            {
                "InputDesc": {
                    "input1": File(path="test_lfn_file2.txt"),
                    "input2": File(path="test_local_file2.txt"),
                    "input3": [
                        File(path="test_lfn_file3.txt"),
                        File(path="test_local_file3.txt"),
                    ],
                },
                "InputSandbox": ["test_local_file2.txt", "test_local_file3.txt"],
                "InputData": [
                    LFN_DIRAC_PREFIX + "/ctao/test_lfn_file2.txt",
                    LFN_DIRAC_PREFIX + "/ctao/test_lfn_file3.txt",
                ],
            },
        ),
        (
            {
                "input1": [
                    File(path="some/path/test_local_file1.txt"),
                ]
            },
            {
                "InputDesc": {
                    "input1": [
                        File(path="test_local_file1.txt"),
                    ]
                },
                "InputSandbox": ["some/path/test_local_file1.txt"],
                "InputData": [],
            },
        ),
        (
            {
                "input1": File(path="some/path/test_local_file1.txt"),
            },
            {
                "InputDesc": {
                    "input1": File(path="test_local_file1.txt"),
                },
                "InputSandbox": ["some/path/test_local_file1.txt"],
                "InputData": [],
            },
        ),
    ],
)
def test_extract_and_translate_input_files(input_data, expected_result):
    result = extract_and_translate_input_files(input_data)
    assert save(result) == save(expected_result)


ARRAY_FILE_OUTPUT = CommandOutputArraySchema(items="test.txt", type_="File")
ARRAY_ARRAY_OUTPUT = CommandOutputArraySchema(
    items=["test.txt", "test2.txt"], type_="array"
)


@pytest.mark.parametrize(
    ("output_type", "expected_result"),
    [
        ("File", True),
        (ARRAY_FILE_OUTPUT, True),
        (ARRAY_ARRAY_OUTPUT, True),
        (["File"], True),
        (["null", "File"], True),
        (["null", ARRAY_FILE_OUTPUT], True),
        (["null", ARRAY_ARRAY_OUTPUT], True),
        ("string", False),
        (["null", "string"], False),
    ],
)
def test_verify_cwl_output_type(output_type, expected_result):
    result = verify_cwl_output_type(output_type)
    assert result is expected_result


@pytest.mark.parametrize(
    ("outputs", "expected_output_sandbox", "expected_output_data"),
    [
        (
            [
                CommandOutputParameter(
                    type_="File",
                    outputBinding=CommandOutputBinding(glob="/path/to/output1.txt"),
                )
            ],
            ["/path/to/output1.txt"],
            [],
        ),
        (
            [
                CommandOutputParameter(
                    type_="File",
                    outputBinding=CommandOutputBinding(
                        glob=LFN_PREFIX + "/path/to/output1.txt"
                    ),
                )
            ],
            [],
            [LFN_DIRAC_PREFIX + "/path/to/output1.txt"],
        ),
        (
            [
                CommandOutputParameter(
                    type_=CommandOutputArraySchema(type_="array", items=File),
                    outputBinding=CommandOutputBinding(
                        glob=[
                            LFN_PREFIX + "/path/to/output1.txt",
                            "/path/to/output2.txt",
                        ]
                    ),
                )
            ],
            ["/path/to/output2.txt"],
            [LFN_DIRAC_PREFIX + "/path/to/output1.txt"],
        ),
    ],
)
def test_extract_output_files(outputs, expected_output_sandbox, expected_output_data):
    cwl_obj = CommandLineTool(inputs={}, outputs=outputs)
    _, output_sandbox, output_data = extract_output_files(cwl_obj, {})

    assert output_sandbox == expected_output_sandbox
    assert output_data == expected_output_data


@pytest.mark.parametrize(
    ("hints", "base_command", "expected_hints", "expected_base_command"),
    [
        (
            [DockerRequirement(dockerPull="harbor/python:tag")],
            "python",
            [],
            ["apptainer", "run", str(CVMFS_BASE_PATH / "harbor/python:tag"), "python"],
        )
    ],
)
def test_translate_docker_hints(
    hints, base_command, expected_hints, expected_base_command
):
    cwl_obj = CommandLineTool(
        inputs=None, outputs=None, hints=hints, baseCommand="python"
    )
    result = translate_docker_hints(cwl_obj, CVMFS_BASE_PATH, [])
    assert result.hints == expected_hints
    assert result.baseCommand == expected_base_command


def test_translate_clt():
    cwl_obj = CommandLineTool(
        inputs=[],
        outputs=[],
        hints=[DockerRequirement(dockerPull="harbor/python:tag")],
        baseCommand="python",
    )
    cwl_dict = {
        "CWLDesc": cwl_obj,
        "OutputSandbox": [],
        "OutputData": [],
        "InputDesc": {},
        "InputSandbox": [],
        "InputData": [],
    }
    result = translate_clt(
        cwl_dict=cwl_dict,
        cvmfs_base_path=CVMFS_BASE_PATH,
        apptainer_options=[],
    )

    assert result == cwl_dict


def test_translate_workflow():
    cwl_obj = Workflow(
        steps=[
            WorkflowStep(
                id="/some/path#step_1",
                in_=[],
                out=[],
                run=CommandLineTool(inputs=[], outputs=[], baseCommand="echo CLT1"),
            ),
            WorkflowStep(
                id="/some/path#step_2",
                in_=[],
                out=[],
                run=CommandLineTool(inputs=[], outputs=[], baseCommand="echo CLT2"),
            ),
        ],
        inputs=[],
        outputs=[],
    )
    cwl_dict = {
        "CWLDesc": cwl_obj,
        "OutputSandbox": [],
        "OutputData": [],
        "InputDesc": {},
        "InputSandbox": [],
        "InputData": [],
    }
    result = translate_workflow(
        cwl_dict=cwl_dict,
        cvmfs_base_path=CVMFS_BASE_PATH,
        apptainer_options=[],
    )

    assert result == cwl_dict


def test_translate_cwl_workflow(mocker):
    # Test CommandLineTool
    cwl_obj = CommandLineTool(
        inputs=[],
        outputs=[],
        baseCommand="python",
    )
    mock_translate_clt = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWL_utils.translate_clt"
    )
    cwl_dict = {
        "CWLDesc": cwl_obj,
        "OutputSandbox": [],
        "OutputData": [],
        "InputDesc": {},
        "InputSandbox": [],
        "InputData": [],
    }
    translate_cwl_workflow(cwl_obj, {}, CVMFS_BASE_PATH, [])
    mock_translate_clt.assert_called_once_with(cwl_dict, CVMFS_BASE_PATH, [])

    # Test Workflow
    cwl_obj = Workflow(inputs=[], outputs=[], steps=[])
    mock_translate_workflow = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWL_utils.translate_workflow"
    )
    cwl_dict = {
        "CWLDesc": cwl_obj,
        "OutputSandbox": [],
        "OutputData": [],
        "InputDesc": {},
        "InputSandbox": [],
        "InputData": [],
    }
    translate_cwl_workflow(cwl_obj, {}, CVMFS_BASE_PATH, [])
    mock_translate_workflow.assert_called_once_with(cwl_dict, CVMFS_BASE_PATH, [])


def test_set_input_file_basename():
    inputs = {"input": File(path="/some/file/basename")}
    inputs_new = set_input_file_basename(inputs)
    assert inputs_new["input"].basename == "basename"
