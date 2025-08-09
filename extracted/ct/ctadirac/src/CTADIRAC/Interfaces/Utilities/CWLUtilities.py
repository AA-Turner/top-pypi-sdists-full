from copy import deepcopy
from typing import Union

from cwl_utils.parser import (
    OutputArraySchema,
    Workflow,
    CommandLineTool,
    ExpressionTool,
)

from CTADIRAC.ProductionSystem.CWL.CWLWorkflowStep import WorkflowStep

LFN_PREFIX = "lfn://"
LFN_DIRAC_PREFIX = "LFN:"
LOCAL_PREFIX = "file://"
JS_REQ = {"class": "InlineJavascriptRequirement"}


def verify_cwl_output_type(
    output_type: Union[str, OutputArraySchema, list[Union[str, OutputArraySchema]]]
) -> bool:
    """Check if output type is a "File" str or OutputArraySchema (or a list containing them).

    Args:
        output_type (Union[str, OutputArraySchema, List[Union[str, OutputArraySchema]]]): The output type.
    """
    if isinstance(output_type, list):
        return any(t == "File" or isinstance(t, OutputArraySchema) for t in output_type)
    return output_type == "File" or isinstance(output_type, OutputArraySchema)


def get_current_step_obj(cwl_obj: Workflow, step_name: str):
    """Get the current step object by step name.

    Args:
    -----
        cwl_obj (Workflow): The CWL workflow object containing steps.
        step_name (str): The name of the step to retrieve.
    Returns:
    -----
        step: The matched step object, or None if not found.
    """
    for step in cwl_obj.steps:
        if step.id.rpartition("#")[2].split("/")[0] == step_name:
            return step
    return None


def get_input_source(step: WorkflowStep, outputs: dict) -> dict[str, str]:
    """Map the CWL step input id and input source.

    Args:
    -----
        step (WorkflowStep): Workflow step.
        outputs (dict): The evaluated ExpressionTool outputs.
    Returns:
    -----
        dict[str, str]: Mapping of input ID to source.
    """
    source_id_mapping = {}
    for inp in step.in_:
        inp_id = inp.id.rpartition("#")[2].split("/")[-1]
        source_full = inp.source.rpartition("#")[2].split("/")

        # Make sure to not overwrite an initially present input value
        if len(source_full) > 1:
            source = source_full[-1]
            source_step = source_full[0]
            if source in outputs and source_step:
                source_id_mapping[inp_id] = source

    return source_id_mapping


def fill_defaults(cwl: Union[Workflow, CommandLineTool, ExpressionTool], inputs: dict):
    """Fill defaults from CWL inputs into inputs dict.
    This is needed for evaluating expressions later on.

    Args:
        cwl (Union[Workflow, CommandLineTool, ExpressionTool]) : The CWL definition
        inputs (dict): User provided inputs.
    Returns:
        inputs (dict): Inputs with additional values filled from CWL defaults
    """
    updated_inputs = deepcopy(inputs)

    def fill_input_inputs(step):
        for inp in step.inputs:
            key = inp.id.rpartition("#")[2].split("/")[-1]
            if key not in updated_inputs and inp.default is not None:
                updated_inputs[key] = inp.default

    if isinstance(cwl, Workflow):
        for step in cwl.steps:
            fill_input_inputs(step.run)
    elif isinstance(cwl, (CommandLineTool, ExpressionTool)):
        fill_input_inputs(cwl)

    return updated_inputs
