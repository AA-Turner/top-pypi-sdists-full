from pathlib import Path
from typing import Any, Union
from copy import deepcopy

from cwl_utils.parser import (
    CommandLineTool,
    CommandOutputParameter,
    File,
    OutputArraySchema,
    Workflow,
    WorkflowStep,
    save,
)
from cwl_utils.expression import do_eval

LFN_PREFIX = "lfn://"
LFN_DIRAC_PREFIX = "LFN:"
LOCAL_PREFIX = "file://"


def set_input_file_basename(inputs):
    updated_inputs = deepcopy(inputs)
    for inp in updated_inputs.values():
        if isinstance(inp, File) and not inp.basename:
            inp.basename = Path(inp.path).name
    return updated_inputs


def fill_defaults(cwl: Union[Workflow, CommandLineTool], inputs: dict):
    """Fill in defaults into inputs.

    This is needed for evaluating expressions later on.

    Parameters
    ----------
    cwl: CommandLineTool
        The CWL definition
    inputs: dict
        user provided inputs.

    Returns
    -------
    inputs: dict
        inputs with additional values filled from CWL defaults
    """
    updated_inputs = deepcopy(inputs)

    def fill_input(step):
        for inp in step.inputs:
            key = inp.id.rpartition("#")[2].split("/")[-1]
            if key not in inputs and inp.default is not None:
                updated_inputs[key] = inp.default

    if isinstance(cwl, Workflow):
        for step in cwl.steps:
            fill_input(step.run)
    elif isinstance(cwl, CommandLineTool):
        fill_input(cwl)
    return updated_inputs


def translate_cwl_workflow(
    cwl_obj: Union[Workflow, CommandLineTool],
    cwl_inputs: dict[str, Any],
    cvmfs_base_path: Path,
    apptainer_options: list[Any],
) -> dict[str, Any]:
    """Translate the CWL workflow description into Dirac compliant execution.

    Args:
        cwl_obj: The CWL defintion.
        cwl_inputs: The user inputs.
        cvmfs_base_path (Path): The base path for CVMFS container repository.
        apptainer_options (list[Any]): A list of options for Apptainer.

    Returns:
        dict[str, Any]: A dictionary representing the translated workflow, compliant with Dirac.
    """

    cwl_dict = {
        "CWLDesc": cwl_obj,
        "OutputSandbox": [],
        "OutputData": [],
        "InputDesc": cwl_inputs,
        "InputSandbox": [],
        "InputData": [],
    }

    if isinstance(cwl_obj, CommandLineTool):
        return translate_clt(cwl_dict, cvmfs_base_path, apptainer_options)

    if isinstance(cwl_obj, Workflow):
        return translate_workflow(cwl_dict, cvmfs_base_path, apptainer_options)


def translate_clt(cwl_dict, cvmfs_base_path, apptainer_options):
    """Translate the CWL CommandLineTool description into Dirac compliant execution.

    Args:
        cwl_dict: A dictionary representing the translated workflow
        cvmfs_base_path (Path): The base path for CVMFS container repository.
        apptainer_options (list[Any]): A list of options for Apptainer.

    Returns:
        dict[str, Any]: A dictionary representing the translated workflow, compliant with Dirac.
    """
    inputs = deepcopy(cwl_dict["InputDesc"])
    cwl_desc = deepcopy(cwl_dict["CWLDesc"])
    if cwl_desc.hints:
        cwl_desc = translate_docker_hints(cwl_desc, cvmfs_base_path, apptainer_options)
    cwl_dict.update(extract_and_translate_input_files(inputs))
    _, output_sandbox, output_data = extract_output_files(cwl_desc, inputs)
    cwl_dict["OutputSandbox"] += output_sandbox
    cwl_dict["OutputData"] += output_data
    cwl_dict["CWLDesc"] = cwl_desc

    return cwl_dict


def translate_workflow(cwl_dict, cvmfs_base_path, apptainer_options):
    """Translate the CWL Workflow description into Dirac compliant execution.

    Args:
        cwl_dict: A dictionary representing the translated workflow
        cvmfs_base_path (Path): The base path for CVMFS container repository.
        apptainer_options (list[Any]): A list of options for Apptainer.

    Returns:
        dict[str, Any]: A dictionary representing the translated workflow, compliant with Dirac.
    """
    inputs = deepcopy(cwl_dict["InputDesc"])
    cwl_desc = deepcopy(cwl_dict["CWLDesc"])

    # need to set the file basename for JSReq:
    inputs = set_input_file_basename(inputs)
    cwl_dict.update(extract_and_translate_input_files(inputs))

    step_input_expr_req = any(
        req.class_ == "StepInputExpressionRequirement"
        for req in cwl_desc.requirements or []
    )

    # TODO: since we "pack" locally the cwl, the cwltool file id are also local
    # -> need to find a workaround

    # Only the Workflow outputs must be evaluated
    wf_outputs = {}
    for output in cwl_desc.outputs:
        if isinstance(output.outputSource, list):
            for output_source in output.outputSource:
                step_name = output_source.rpartition("#")[2].split("/")[0]
                wf_outputs.setdefault(step_name, []).append(
                    output_source.rpartition("#")[2].split("/")[-1]
                )
        else:
            step_name = output.outputSource.rpartition("#")[2].split("/")[0]
            wf_outputs.setdefault(step_name, []).append(
                output.outputSource.rpartition("#")[2].split("/")[-1]
            )
    # TODO: here we need to change the whole packed workflow not the single step
    updated_inputs = deepcopy(inputs)
    for n, step in enumerate(cwl_desc.steps):
        step_name = step.id.rpartition("#")[2].split("/")[0]
        output_sandbox = []
        output_data = []
        if step.run.hints:
            cwl_desc.steps[n].run = translate_docker_hints(
                step.run, cvmfs_base_path, apptainer_options
            )
        if step_input_expr_req:
            # here we need to interprete the input expressions
            # to interprete potential output JS expressions
            # which needs inputs to be present in the input description...
            updated_inputs = evaluate_input_value_from(step, updated_inputs)
            (
                updated_inputs,
                output_sandbox,
                output_data,
            ) = extract_output_files(
                step.run,
                updated_inputs,
                wf_outputs.setdefault(step_name, []),
                update_inputs=True,
                always_resolve_output=True,
            )
        else:
            _, output_sandbox, output_data = extract_output_files(
                step.run, updated_inputs, wf_outputs.setdefault(step_name, [])
            )
        cwl_dict["OutputSandbox"] += output_sandbox
        cwl_dict["OutputData"] += output_data

    cwl_dict["CWLDesc"] = cwl_desc

    return cwl_dict


def translate_docker_hints(
    cwl_obj, cvmfs_base_path: Path, apptainer_options: list[Any]
):
    """Translate CWL DockerRequirement into Dirac compliant execution.

    Args:
        cwl_obj: The CWL defintion.
        cvmfs_base_path (Path): The base path for CVMFS.
        apptainer_options (list[Any]): A list of options for Apptainer.
    Returns:
        cwl_obj: the translated cwl object.
    """
    for index, hints in enumerate(cwl_obj.hints):
        if hints.class_ == "DockerRequirement":
            image = hints.dockerPull
            cmd = [
                "apptainer",
                "run",
                *apptainer_options,
                str(cvmfs_base_path / f"{image}"),
            ]
            if isinstance(cwl_obj.baseCommand, str):
                cmd.append(cwl_obj.baseCommand)
            else:
                cmd.extend(cwl_obj.baseCommand)
            cwl_obj.baseCommand = cmd
            del cwl_obj.hints[index]
            break
    return cwl_obj


def evaluate_input_value_from(
    step: WorkflowStep, inputs: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate inputs expression in Workflow.

    Args:
        step: WorkflowStep
        inputs: The user inputs.
    Returns:
        updated_inputs: the evaluated inputs.
    """
    updated_inputs = deepcopy(inputs)
    updated_inputs = save(updated_inputs)
    js_req = {"class": "InlineJavascriptRequirement"}
    for inp in step.in_:
        if inp.valueFrom:
            input_name = inp.id.rpartition("#")[2].split("/")[-1]
            exp = inp.valueFrom
            exp_filename = do_eval(
                exp,
                updated_inputs,
                outdir=None,
                requirements=[js_req],
                tmpdir=None,
                resources={},
            )
            updated_inputs[input_name] = exp_filename
    return updated_inputs


def collect_outputs(cwl, inputs, requirements: list = []) -> list[str]:
    """Collect evaluated output filenames.

    Parameters
    ----------
    cwl: dict
        The CWL definition
    inputs: dict
        user provided inputs.

    Returns
    -------
    outputs: list[str]
        The output filenames of this workflow given
        the provided inputs and defaults.
    """

    outputs = []
    if cwl.outputs is None:
        return outputs
    for output in cwl.outputs:
        if glob := output.outputBinding.glob:
            result = do_eval(
                glob,
                inputs,
                outdir=None,
                requirements=requirements,
                tmpdir=None,
                resources={},
            )
            outputs.append(result)

    return outputs


def extract_output_files(
    cwl_obj: CommandLineTool,
    inputs: dict,
    outputs_to_record: [list | None] = None,
    update_inputs: bool = False,
    always_resolve_output: bool = False,
):
    """Translate output files into a DIRAC compliant usage.

    Extract local outputs and lfns.
    Remove outputs path prefix.

    Args:
        cwl_obj: The CWL defintion.
        cwl_inputs: The user inputs.
        outputs_to_record: The list of outputs to record
        update_inputs: if True, update cwl inputs with output expression
                        (Needed for interpreting JS requirements)
        always_resolve_output: if True, resolve output expression even if not in the outputs list.
                        (Needed for interpreting JS requirements)
    Returns: tuple
        inputs: inputs or updated inputs
        output_sandbox: list of evaluated output sandbox
        output_data: list of evaluated output data
    """
    output_lfns = []
    output_sandboxes = []
    inputs = fill_defaults(cwl_obj, inputs)

    def process_glob(inputs: dict, glob: str, should_record_output: bool):
        if should_record_output or always_resolve_output:
            glob = resolve_glob(inputs, glob)
        if should_record_output:
            record_output(glob, output_sandboxes, output_lfns)
        return glob

    def process_output(inputs: dict, output: CommandOutputParameter):
        output_id = output.id.rpartition("#")[2].split("/")[-1] if output.id else None
        should_record_output = (
            outputs_to_record is None or output_id in outputs_to_record
        )

        glob_exp = output.outputBinding.glob if output.outputBinding else None
        glob_list = [glob_exp] if isinstance(glob_exp, str) else glob_exp

        for glob in glob_list:
            glob = process_glob(inputs, glob, should_record_output)
            if update_inputs and output_id not in inputs:
                inputs = update_input(inputs, glob, output, output_id)

    for output in cwl_obj.outputs:
        if not verify_cwl_output_type(output.type_):
            continue
        process_output(inputs, output)

    return inputs, output_sandboxes, output_lfns


def resolve_glob(inputs: dict, glob: str):
    if glob.startswith("$"):
        glob = do_eval(
            glob,
            inputs,
            outdir=None,
            requirements=[],
            tmpdir=None,
            resources={},
        )
    return glob


def record_output(glob: str, output_sandboxes: list, output_lfns: list):
    if glob.startswith(LFN_PREFIX):
        output_lfns.append(glob.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
    else:
        output_sandboxes.append(glob)


def update_input(
    inputs: dict, glob: str, output: CommandOutputParameter, output_id: str
):
    """Saving the interpreted output in the inputs
    so that we can interprete JS and parameter reference."""
    inputs[output_id] = (
        {"class": "File", "path": glob, "basename": glob}
        if output.type_ == "File"
        else glob
    )
    return inputs


def verify_cwl_output_type(output_type) -> bool:
    """Verify the cwl output type.

    File or OutputArraySchema
    or a list of 'null' and File/OutputArraySchema.
    Args:
        output_type: the cwl output type.
    Returns:
        bool
    """
    if isinstance(output_type, list):
        for type_ in output_type:
            if type_ == "File" or isinstance(type_, OutputArraySchema):
                return True
    if output_type == "File" or isinstance(output_type, OutputArraySchema):
        return True
    return False


def extract_and_translate_input_files(cwl_inputs) -> dict[str, Any]:
    """Extract input files from CWL inputs, rewrite file prefix.

    If the file is a Sandbox, ensure there is no absolute path,
    and store it in the input sandbox list.
    If the file is a LFN, remove the lfn prefix and store it in the lfns list.

    Args:
        cwl_inputs: User CWL inputs.
    Returns:
        dict: CWL inputs, input sandbox and input data list
    """

    def update_inputs(value):
        path, lfn = translate_sandboxes_and_lfns(value)
        if lfn:
            input_lfns.append(path)
        else:
            input_sandboxes.append(path)
        return Path(path.removeprefix(LFN_DIRAC_PREFIX)).name

    input_sandboxes = []
    input_lfns = []
    cwl_inputs = deepcopy(cwl_inputs)

    for key, input_value in cwl_inputs.items():
        if isinstance(input_value, list):
            for file in input_value:
                if isinstance(file, File):
                    file.path = update_inputs(file)

        elif isinstance(input_value, File):
            input_value.path = update_inputs(input_value)

    return {
        "InputDesc": cwl_inputs,
        "InputSandbox": input_sandboxes,
        "InputData": input_lfns,
    }


def translate_sandboxes_and_lfns(file: File | str) -> tuple[str, bool]:
    """Extract local files as sandboxes and lfns as input data.

    Args:
        file: (File | str)
    Returns:
        tuple: file name (str), lfn (bool)
    """
    if isinstance(file, File):
        if not file.path:
            raise KeyError("File path is not defined.")
        path = file.path
    elif isinstance(file, str):
        path = file

    lfn = False
    if path.startswith(LFN_PREFIX):
        path = path.replace(LFN_PREFIX, LFN_DIRAC_PREFIX)
        lfn = True
    path = path.removeprefix(LOCAL_PREFIX)
    return path, lfn
