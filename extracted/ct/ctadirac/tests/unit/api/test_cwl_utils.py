import pytest
from cwl_utils.parser.cwl_v1_2 import (
    CommandOutputArraySchema,
    CommandLineTool,
    Workflow,
    WorkflowStep,
    CommandInputParameter,
)

from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    verify_cwl_output_type,
    fill_defaults,
)

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
    ("cwl", "inputs", "expected_inputs"),
    [
        (
            CommandLineTool(
                inputs=[
                    CommandInputParameter(
                        id="/some/path#step_1",
                        type_="string",
                    )
                ],
                outputs={},
            ),
            {"input1": "input1", "input2": "input2"},
            {"input1": "input1", "input2": "input2"},
        ),
        (
            Workflow(
                steps=[
                    WorkflowStep(
                        id="/some/path#step_1",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_1",
                                    type_="string",
                                    default="defaultInputStep1",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT1",
                        ),
                    ),
                    WorkflowStep(
                        id="/some/path#step_2",
                        in_=[],
                        out=[],
                        run=CommandLineTool(
                            inputs=[
                                CommandInputParameter(
                                    id="/some/path#step_2",
                                    type_="string",
                                    default="defaultInputStep2",
                                )
                            ],
                            outputs=[],
                            baseCommand="echo CLT2",
                        ),
                    ),
                ],
                inputs={},
                outputs={},
            ),
            {"input1": "input1", "input2": "input2"},
            {
                "input1": "input1",
                "input2": "input2",
                "step_1": "defaultInputStep1",
                "step_2": "defaultInputStep2",
            },
        ),
    ],
)
def test_fill_defaults(cwl, inputs, expected_inputs):
    result = fill_defaults(cwl, inputs)
    assert result == expected_inputs
