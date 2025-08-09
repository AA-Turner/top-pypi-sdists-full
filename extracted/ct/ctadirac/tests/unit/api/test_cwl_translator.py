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
    StepInputExpressionRequirement,
    WorkflowStepInput,
    WorkflowOutputParameter,
)
from cwl_utils.parser import save

from CTADIRAC.Interfaces.Utilities.CWLTranslator import CWLTranslator
from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    LFN_PREFIX,
    LFN_DIRAC_PREFIX,
    LOCAL_PREFIX,
)

CVMFS_BASE_PATH = Path("/cvmfs/ctao.dpps.test")
DOCKER_PYTHON_TAG = "harbor/python:tag"


def test_init_class(mocker):
    cwl_workflow = "tests/resources/cwl/single_command_line_tool/process_dl0_dl1.cwl"
    cwl_inputs = (
        "tests/resources/cwl/single_command_line_tool/inputs_process_dl0_dl1.yaml"
    )

    mocker_load_document = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWLTranslator.load_document"
    )
    mocker_load_inputfile = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWLTranslator.load_inputfile"
    )

    CWLTranslator(cwl_workflow, cwl_inputs)
    mocker_load_document.assert_called_once()
    mocker_load_inputfile.assert_called_once()


def test_translate(mocker):
    # Check if translate method calls the right methods (CLT or Workflow)
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    # --------------------------------------------
    # Test CommandLineTool
    cwl_translator.transformed_cwl = CommandLineTool.__new__(CommandLineTool)
    mock_translate_clt = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWLTranslator.CWLTranslator._translate_clt"
    )

    cwl_translator.translate(CVMFS_BASE_PATH, [])
    mock_translate_clt.assert_called_once_with(CVMFS_BASE_PATH, [])

    # --------------------------------------------
    # Test Workflow
    cwl_translator.transformed_cwl = Workflow.__new__(Workflow)
    mock_translate_workflow = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWLTranslator.CWLTranslator._translate_workflow"
    )

    cwl_translator.translate(CVMFS_BASE_PATH, [])
    mock_translate_workflow.assert_called_once_with(CVMFS_BASE_PATH, [])


def test_translate_clt(mocker):
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_obj = CommandLineTool(
        inputs=[],
        outputs=[],
        hints=[DockerRequirement(dockerPull=DOCKER_PYTHON_TAG)],
        baseCommand="python",
    )
    cwl_translator.original_inputs = {}
    cwl_translator.transformed_cwl = cwl_obj
    cwl_translator.transformed_inputs = {}
    cwl_translator.output_data = []
    cwl_translator.output_sandbox = []
    mock_extract_output_files = mocker.patch(
        "CTADIRAC.Interfaces.Utilities.CWLTranslator.CWLTranslator._extract_output_files"
    )

    cwl_translator._translate_clt(CVMFS_BASE_PATH, [])
    assert cwl_translator.transformed_cwl == cwl_obj
    assert cwl_translator.transformed_inputs == {}
    assert cwl_translator.output_data == []
    assert cwl_translator.output_sandbox == []
    mock_extract_output_files.assert_called_once_with(
        cwl_translator.transformed_cwl, cwl_translator.transformed_inputs
    )


def test_translate_workflow():
    def create_workflow(requirement=False):
        return Workflow(
            steps=[
                WorkflowStep(
                    id="/some/path#step_1",
                    in_=[],
                    out=[],
                    run=CommandLineTool(
                        inputs=[],
                        outputs=[],
                        baseCommand="echo CLT1",
                        hints=[DockerRequirement(dockerPull=DOCKER_PYTHON_TAG)],
                    ),
                ),
                WorkflowStep(
                    id="/some/path#step_2",
                    in_=[WorkflowStepInput(id="/some/path#step_4", valueFrom="value")]
                    if requirement
                    else [],
                    out=[],
                    run=CommandLineTool(
                        inputs=[],
                        outputs=[],
                        baseCommand=["echo CLT2"],
                        hints=[DockerRequirement(dockerPull=DOCKER_PYTHON_TAG)],
                    ),
                ),
                WorkflowStep(
                    id="/some/path#step_3",
                    in_=[WorkflowStepInput(id="/some/path#step_5", valueFrom="value")]
                    if requirement
                    else [],
                    out=[],
                    run=CommandLineTool(
                        inputs=[], outputs=[], baseCommand=["echo CLT3"]
                    ),
                ),
            ],
            inputs=[],
            outputs=[],
            requirements=[StepInputExpressionRequirement()] if requirement else [],
        )

    def test_workflow(cwl_workflow):
        cwl_translator.transformed_cwl = cwl_workflow

        cwl_translator._translate_workflow(CVMFS_BASE_PATH, [])

        assert cwl_translator.transformed_cwl == cwl_workflow
        assert cwl_translator.transformed_inputs == {}
        assert cwl_translator.output_data == []
        assert cwl_translator.output_sandbox == []

    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_translator.original_inputs = {}
    cwl_translator.transformed_inputs = {}
    cwl_translator.output_data = []
    cwl_translator.output_sandbox = []

    # No requirements workflow
    cwl_workflow = create_workflow()

    # Requirements workflow
    cwl_workflow_req = create_workflow(True)

    test_workflow(cwl_workflow)
    test_workflow(cwl_workflow_req)


@pytest.mark.parametrize(
    ("hints", "base_command", "expected_hints", "expected_base_command"),
    [
        (
            [DockerRequirement(dockerPull=DOCKER_PYTHON_TAG)],
            "python",
            [],
            ["apptainer", "run", str(CVMFS_BASE_PATH / DOCKER_PYTHON_TAG), "python"],
        )
    ],
)
def test_translate_docker_hints(
    hints, base_command, expected_hints, expected_base_command
):
    cwl_translator = CWLTranslator.__new__(CWLTranslator)
    cwl_obj = CommandLineTool(
        inputs=None, outputs=None, hints=hints, baseCommand=base_command
    )

    result = cwl_translator._translate_docker_hints(cwl_obj, CVMFS_BASE_PATH, [])

    assert result.hints == expected_hints
    assert result.baseCommand == expected_base_command


@pytest.mark.parametrize(
    ["outputs", "expected_outputs_ids"],
    [
        (
            [
                WorkflowOutputParameter(
                    id="1", type_="File", outputSource="dl0_to_dl1/dl1"
                ),
                WorkflowOutputParameter(
                    id="2", type_="File", outputSource="dl1_to_dl2/dl1.5"
                ),
                WorkflowOutputParameter(
                    id="3", type_="File", outputSource="dl1_to_dl2/dl2"
                ),
            ],
            {"dl0_to_dl1": ["dl1"], "dl1_to_dl2": ["dl1.5", "dl2"]},
        )
    ],
)
def test_get_workflow_outputs_id(outputs, expected_outputs_ids):
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_translator.transformed_cwl = Workflow(steps={}, inputs={}, outputs=outputs)

    outputs_ids = cwl_translator._get_workflow_outputs_id()

    assert outputs_ids == expected_outputs_ids


@pytest.mark.parametrize(
    ("input_file", "expected_basename"),
    [
        ({"input1": File(path="test_lfn_file.txt")}, "test_lfn_file.txt"),
        (
            {"input1": File(path="test_local_file.txt", basename="local_file")},
            "local_file",
        ),
    ],
)
def test_set_input_file_basename(input_file, expected_basename):
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_translator.transformed_inputs = input_file

    cwl_translator._set_input_file_basename()
    assert cwl_translator.transformed_inputs["input1"].basename == expected_basename


@pytest.mark.parametrize(
    ("input_cwl", "expected_results"),
    [
        (
            {"input1": File(path=LFN_PREFIX + "/ctao/test_lfn_file.txt")},
            {
                "transformed_inputs": {"input1": File(path="test_lfn_file.txt")},
                "input_sandbox": [],
                "input_data": [LFN_DIRAC_PREFIX + "/ctao/test_lfn_file.txt"],
            },
        ),
        (
            {"input1": File(path=LOCAL_PREFIX + "test_local_file.txt")},
            {
                "transformed_inputs": {"input1": File(path="test_local_file.txt")},
                "input_sandbox": ["test_local_file.txt"],
                "input_data": [],
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
                "transformed_inputs": {
                    "input1": [
                        File(path="test_lfn_file1.txt"),
                        File(path="test_local_file1.txt"),
                    ]
                },
                "input_sandbox": ["test_local_file1.txt"],
                "input_data": [LFN_DIRAC_PREFIX + "/ctao/test_lfn_file1.txt"],
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
                "transformed_inputs": {
                    "input1": File(path="test_lfn_file2.txt"),
                    "input2": File(path="test_local_file2.txt"),
                    "input3": [
                        File(path="test_lfn_file3.txt"),
                        File(path="test_local_file3.txt"),
                    ],
                },
                "input_sandbox": ["test_local_file2.txt", "test_local_file3.txt"],
                "input_data": [
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
                "transformed_inputs": {
                    "input1": [
                        File(path="test_local_file1.txt"),
                    ]
                },
                "input_sandbox": ["some/path/test_local_file1.txt"],
                "input_data": [],
            },
        ),
        (
            {
                "input1": File(path="some/path/test_local_file1.txt"),
            },
            {
                "transformed_inputs": {
                    "input1": File(path="test_local_file1.txt"),
                },
                "input_sandbox": ["some/path/test_local_file1.txt"],
                "input_data": [],
            },
        ),
        # Test that a input string containing "lfn" is correctly treated.
        (
            {
                "input1": File(path="some/path/test_local_file1.txt"),
                "input2": f"{LFN_PREFIX}/ctao/path/test.h5",
            },
            {
                "transformed_inputs": {
                    "input1": File(path="test_local_file1.txt"),
                    "input2": "test.h5",
                },
                "input_sandbox": ["some/path/test_local_file1.txt"],
                "input_data": [],
            },
        ),
    ],
)
def test_extract_and_translate_input_files(input_cwl, expected_results):
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_translator.input_data = []
    cwl_translator.input_sandbox = []
    cwl_translator.transformed_inputs = input_cwl

    cwl_translator._extract_and_translate_input_files()

    assert save(cwl_translator.transformed_inputs) == save(
        expected_results["transformed_inputs"]
    )
    assert cwl_translator.input_sandbox == expected_results["input_sandbox"]
    assert cwl_translator.input_data == expected_results["input_data"]


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
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    if expected_result is None:
        with pytest.raises(KeyError, match="File path is not defined."):
            cwl_translator._translate_sandboxes_and_lfns(file_input)
    else:
        result, is_lfn = cwl_translator._translate_sandboxes_and_lfns(file_input)
        assert result == expected_result
        assert is_lfn == expected_lfn


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
    cwl_translator = CWLTranslator.__new__(CWLTranslator)

    cwl_obj = CommandLineTool(inputs={}, outputs=outputs)
    cwl_translator.output_sandbox = []
    cwl_translator.output_data = []

    _ = cwl_translator._extract_output_files(cwl_obj, {})

    assert cwl_translator.output_sandbox == expected_output_sandbox
    assert cwl_translator.output_data == expected_output_data
