from copy import deepcopy
from pathlib import Path
from typing import Any

from cwl_utils.pack import pack
from cwl_utils.parser import load_document, WorkflowStep, save, load_document_by_uri
from cwl_utils.parser import (
    CommandLineTool,
    CommandOutputParameter,
    ExpressionTool,
    File,
    Workflow,
)
from cwl_utils.parser.utils import load_inputfile
from cwl_utils.expression import do_eval

from CTADIRAC.Interfaces.Utilities.CWLUtilities import (
    fill_defaults,
    verify_cwl_output_type,
    LFN_PREFIX,
    LOCAL_PREFIX,
    LFN_DIRAC_PREFIX,
    JS_REQ,
    get_current_step_obj,
    get_input_source,
)


class CWLTranslator:
    """Translator from CWL Workflow to DIRAC Job.
    Extract needed DIRAC job arguments from the CWL and inputs description.

    Args:
    -----
        cwl_workflow (str): Path to the local CWL workflow file
        cwl_inputs (str): Path to the local CWL inputs file
    """

    def __init__(
        self,
        cwl_workflow: str,
        cwl_inputs: str,
    ) -> None:
        self.cwl_workflow_path = Path(cwl_workflow)
        self.cwl_inputs_path = Path(cwl_inputs)

        self.original_cwl = load_document(pack(str(self.cwl_workflow_path)))
        self.unpacked_cwl = load_document_by_uri(self.cwl_workflow_path)
        self.original_inputs = load_inputfile(
            self.original_cwl.cwlVersion, self.cwl_inputs_path.read_text()
        )

        self.transformed_inputs = deepcopy(self.original_inputs)
        self.transformed_cwl = deepcopy(self.original_cwl)
        self.output_sandbox = []
        self.output_data = []
        self.input_sandbox = []
        self.input_data = []

    def translate(self, cvmfs_base_path: Path, apptainer_options: list[Any]) -> None:
        """Translate the CWL workflow description into Dirac compliant execution.

        Args:
        -----
            cvmfs_base_path (Path): The base path for CVMFS container repository.
            apptainer_options (list[Any]): A list of options for Apptainer.
        """

        if isinstance(self.transformed_cwl, CommandLineTool):
            self._translate_clt(cvmfs_base_path, apptainer_options)

        if isinstance(self.transformed_cwl, Workflow):
            self._translate_workflow(cvmfs_base_path, apptainer_options)

    def _translate_clt(
        self, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> None:
        """Translate the CWL CommandLineTool description into Dirac compliant execution.

        Args:
        -----
            cvmfs_base_path (Path): The base path for CVMFS container repository.
            apptainer_options (list[Any]): A list of options for Apptainer.
        """

        if self.transformed_cwl.hints:
            self.transformed_cwl = self._translate_docker_hints(
                self.transformed_cwl, cvmfs_base_path, apptainer_options
            )

        self._extract_and_translate_input_files()
        self._extract_output_files(self.transformed_cwl, self.original_inputs)

    def _translate_workflow(
        self, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> None:
        """Translate the CWL Workflow description into Dirac compliant execution.

        Args:
        -----
            cvmfs_base_path (Path): The base path for CVMFS container repository.
            apptainer_options (list[Any]): A list of options for Apptainer.
        """

        def evaluate_input_value_from(
            step: WorkflowStep, inputs: dict[str, Any]
        ) -> dict[str, Any]:
            """Evaluate inputs expression in Workflow steps.

            Args:
            -----
                step (WorkflowStep): Current WorkflowStep
                inputs (dict[str, Any]): User inputs.
            Returns:
            -----
                step_inputs (dict[str, Any]): Evaluated step inputs.
            """
            step_inputs = save(deepcopy(inputs))
            for inp in step.in_:
                if inp.valueFrom:
                    input_name = inp.id.rpartition("#")[2].split("/")[-1]
                    exp_filename = do_eval(
                        inp.valueFrom,
                        step_inputs,
                        outdir=None,
                        requirements=[JS_REQ],
                        tmpdir=None,
                        resources={},
                    )
                    step_inputs[input_name] = exp_filename
            return step_inputs

        # Need to set the file basename for JSReq:
        self._set_input_file_basename()
        self._extract_and_translate_input_files()

        step_input_expr_req = any(
            req.class_ == "StepInputExpressionRequirement"
            for req in self.transformed_cwl.requirements or []
        )

        # Only the Workflow outputs must be evaluated
        wf_outputs = self._get_workflow_outputs_id()

        # Add steps inputs to a temporary input yaml file, without modifying the original inputs
        # Used only for output files extraction from steps
        temp_inputs = deepcopy(self.transformed_inputs)
        exptool_outputs = None
        for n, wf_step in enumerate(self.transformed_cwl.steps):
            step_name = wf_step.id.rpartition("#")[2].split("/")[0]

            if isinstance(wf_step.run, ExpressionTool):
                exptool_outputs = self._evaluate_expression_tool_outputs(
                    self.unpacked_cwl, wf_step, temp_inputs, step_name
                )
                continue

            if wf_step.run.hints:
                self.transformed_cwl.steps[n].run = self._translate_docker_hints(
                    wf_step.run, cvmfs_base_path, apptainer_options
                )

            if exptool_outputs:
                unpacked_step = get_current_step_obj(self.unpacked_cwl, step_name)

                self._process_exptool_outputs(
                    wf_step,
                    unpacked_step,
                    temp_inputs,
                    exptool_outputs,
                    wf_outputs,
                    step_name,
                )

            elif step_input_expr_req:
                # here we need to interprete the input expressions
                # to interprete potential output JS expressions
                # which needs inputs to be present in the input description...
                temp_inputs = evaluate_input_value_from(wf_step, temp_inputs)
                temp_inputs = self._extract_output_files(
                    wf_step.run,
                    temp_inputs,
                    wf_outputs.setdefault(step_name, []),
                    update_inputs=True,
                    always_resolve_output=True,
                )
            else:
                self._extract_output_files(
                    wf_step.run, temp_inputs, wf_outputs.setdefault(step_name, [])
                )

    @staticmethod
    def _translate_docker_hints(
        cwl_object: CommandLineTool, cvmfs_base_path: Path, apptainer_options: list[Any]
    ) -> CommandLineTool:
        """Translate CWL DockerRequirement into Dirac compliant execution.

        Args:
        -----
            cwl_object (CommandLineTool): The CWL definition.
            cvmfs_base_path (Path): The base path for CVMFS container repository.
            apptainer_options (list[Any]): A list of options for Apptainer.
        Returns:
        -----
            cwl_object (CommandLineTool): The translated cwl object.
        """
        for index, hint in enumerate(cwl_object.hints):
            if hint.class_ == "DockerRequirement":
                image = hint.dockerPull
                image_path = str(cvmfs_base_path / f"{image}")

                cmd = [
                    "apptainer",
                    "run",
                    *apptainer_options,
                    image_path,
                ]

                if isinstance(cwl_object.baseCommand, str):
                    cmd.append(cwl_object.baseCommand)
                else:
                    cmd.extend(cwl_object.baseCommand)

                cwl_object.baseCommand = cmd
                del cwl_object.hints[index]
                break
        return cwl_object

    def _evaluate_expression_tool_outputs(
        self,
        unpacked_cwl_obj: Workflow,
        wf_step: WorkflowStep,
        cwl_inputs: dict,
        step_name: str,
    ):
        """Evaluate the ExpressionTool outputs.

        Args:
        -----
            unpacked_cwl_obj (Workflow): The unpacked CWL workflow.
            wf_step (WorkflowStep): The Workflow step.
            cwl_inputs (dict): The CWL inputs dict.
            step_name (str): The current step name.
        Returns:
        -----
            exptool_outputs (dict): A dictionary containing the evaluated ExpressionTool outputs.
        """
        for st in unpacked_cwl_obj.steps:
            if st.id.rpartition("#")[2].split("/")[0] == step_name:
                exp_tool_step = st

        expr_inputs = []
        if wf_step.scatter:
            # In the scattering case we need to verfify the input name
            expr_inputs = self._create_scatter_exptool_inputs(
                wf_step, cwl_inputs, exp_tool_step
            )
        else:
            # In the case where there is no scattering, we assume there is only one single input
            input_name = wf_step.run.inputs[0].id.rpartition("#")[2].split("/")[-1]
            source = exp_tool_step.in_[0].source.rpartition("#")[2].split("/")[-1]
            for inp, value in cwl_inputs.items():
                # Then we match the input name and the input value name
                if inp == source:
                    expr_inputs.append({input_name: value})

        # Finally we evaluate the JS expression
        exptool_outputs = {}
        for inp in expr_inputs:
            inp = fill_defaults(wf_step.run, inp)

            # Evaluate the JS expression
            eval_exp = do_eval(
                wf_step.run.expression,
                save(inp),
                outdir=None,
                requirements=[JS_REQ],
                tmpdir=None,
                resources={},
            )

            for key, val in eval_exp.items():
                exptool_outputs.setdefault(key, []).append(val)
        return exptool_outputs

    @staticmethod
    def _create_scatter_exptool_inputs(
        wf_step: WorkflowStep, inputs: dict, exp_tool_step: WorkflowStep
    ) -> list[dict]:
        """Create a list of inputs by matching the scatter input names
        and the names in the cwl inputs.

        Args:
        -----
            wf_step (WorkflowStep): The CWL Workflow step.
            inputs: The CWL inputs.
            exp_tool_step (WorkflowStep): The Expression Tool step from the unpacked CWL.
        Returns:
        -----
            expr_inputs (list[dict]): Expression Tool inputs list.
        """

        def find_source_in_exp_tool_step(
            exp_tool_step: WorkflowStep, scattered_inp: str
        ) -> str | None:
            """Find the source in the ExpressionTool step for a given scattered input.

            Args:
            -----
                exp_tool_step (WorkflowStep): The ExpressionTool step where inputs are defined.
                scattered_inp (str): The name of the scattered input to match.
            Returns:
            -----
                (str|None): The source of the input in the ExpressionTool step, or None if not found.
            """
            for inp in exp_tool_step.in_:
                # Extract the input ID and check if it matches the scattered input
                inp_id = inp.id.rpartition("#")[2].split("/")[-1]
                if inp_id == scattered_inp:
                    return inp.source.rpartition("#")[2].split("/")[-1]
            return None

        expr_inputs = []
        scattered_inp = wf_step.scatter.rpartition("#")[2].split("/")[-1]

        # Find the source corresponding to the scattered input
        source = find_source_in_exp_tool_step(exp_tool_step, scattered_inp)

        # Match the scatter input name with the input value name
        for inp, value in inputs.items():
            if inp == source:
                value = value if isinstance(value, list) else [value]
                expr_inputs.extend({scattered_inp: val} for val in value)

        return expr_inputs

    def _process_exptool_outputs(
        self,
        wf_step: WorkflowStep,
        unpacked_step: WorkflowStep,
        updated_inputs: dict,
        exptool_outputs: dict,
        wf_outputs: dict,
        step_name: str,
    ) -> None:
        """Process the Workflow step using ExpressionTool.

        Args:
        -----
            wf_step (WorkflowStep): The Workflow step object.
            unpacked_step (WorkflowStep): The unpacked Workflow step object.
            updated_inputs (dict): The (updated) CWL inputs.
            wf_outputs (dict): The Workflows outputs.
            step_name (str): The Workflow step name.
        """

        def update_input_from_exptool(
            unpacked_step: WorkflowStep,
            inputs: dict,
            exptool_outputs: dict,
            scatter_iter: int = 0,
        ) -> dict:
            """Update the CWL inputs with the evaluated ExpressionTool outputs.

            Args:
            -----
                unpacked_step (WorkflowStep): CWL unpacked Workflow step.
                inputs (dict): CWL inputs.
                exptool_outputs (dict): The evaluated ExpressionTool outputs.
                scatter_iter (int): The scatter input length iteration number.
            """
            updated_inputs = save(deepcopy(inputs))
            for key, source in get_input_source(unpacked_step, exptool_outputs).items():
                updated_inputs[key] = exptool_outputs[source][scatter_iter]

            return updated_inputs

        iterations = len(list(exptool_outputs.values())[0]) if wf_step.scatter else 1
        for i in range(iterations):
            exptool_inp = update_input_from_exptool(
                unpacked_step,
                updated_inputs,
                exptool_outputs,
                i if wf_step.scatter else 0,
            )

            self._extract_output_files(
                wf_step.run,
                exptool_inp,
                wf_outputs.setdefault(step_name, []),
                update_inputs=True,
                always_resolve_output=True,
            )

    def _get_workflow_outputs_id(self) -> dict[str, list[str]]:
        """Extract Workflow outputs ids.

        Returns:
        -----
            wf_outputs (dict[str, list[str]]): Workflow outputs ids.
        """
        wf_outputs: dict[str, list[str]] = {}

        def add_output(source: str) -> None:
            step_name = source.rpartition("#")[2].split("/")[0]
            output_id = source.rpartition("#")[2].split("/")[-1]
            wf_outputs.setdefault(step_name, []).append(output_id)

        for output in self.transformed_cwl.outputs:
            sources = output.outputSource
            if not isinstance(sources, list):
                sources = [sources]
            for source in sources:
                add_output(source)

        return wf_outputs

    def _set_input_file_basename(self) -> None:
        """Ensure input Files have basename set."""
        for inp in self.transformed_inputs.values():
            if isinstance(inp, File) and not inp.basename:
                inp.basename = Path(inp.path).name
            if isinstance(inp, list):
                for val in inp:
                    if isinstance(val, File) and not val.basename:
                        val.basename = Path(val.path).name

    def _extract_and_translate_input_files(self) -> None:
        """Extract input files from CWL inputs and rewrite file paths.
        If the file is a Sandbox, ensure there is no absolute path, and store it in the input sandbox list.
        If the file is a LFN, remove the lfn prefix and store it in the lfns list.
        """

        def rewrite_file_path(file: File | str) -> str:
            """Rewrite file path.

            Args:
            -----
                file (File | str): File which path should be rewritten.
            Returns:
            -----
                (str): The new file path.
            """
            path, is_lfn = self._translate_sandboxes_and_lfns(file)
            (self.input_data if is_lfn else self.input_sandbox).append(path)
            return Path(path.removeprefix(LFN_DIRAC_PREFIX)).name

        for key, input_value in self.transformed_inputs.items():
            if isinstance(input_value, list):
                for file in input_value:
                    if isinstance(file, File):
                        file.path = rewrite_file_path(file)
            elif isinstance(input_value, File):
                input_value.path = rewrite_file_path(input_value)
            elif isinstance(input_value, str) and input_value.startswith(LFN_PREFIX):
                self.transformed_inputs[key] = Path(
                    input_value.removeprefix(LFN_PREFIX)
                ).name

    def _translate_sandboxes_and_lfns(self, file: File | str) -> tuple[str, bool]:
        """Extract local files as sandboxes and lfns as input data.

        Args:
        -----
            file (File | str): Local file.
        Returns:
        -----
            (filename, is_lfn) (str, bool): A tuple containing a filename and a boolean if it's a lfn (True) or not (False).
        """
        filename = file.path if isinstance(file, File) else file
        if not filename:
            raise KeyError("File path is not defined.")

        is_lfn = filename.startswith(LFN_PREFIX)
        if is_lfn:
            filename = filename.replace(LFN_PREFIX, LFN_DIRAC_PREFIX)
        filename = filename.removeprefix(LOCAL_PREFIX)
        return filename, is_lfn

    def _extract_output_files(
        self,
        cwl_obj: CommandLineTool,
        cwl_inputs: dict,
        outputs_to_record: [list | None] = None,
        update_inputs: bool = False,
        always_resolve_output: bool = False,
    ) -> dict:
        """Translate output files into a DIRAC compliant usage.

        Extract local outputs and lfns.
        Remove outputs path prefix.

        Args:
        -----
            cwl_obj (CommandLineTool): The CWL definition.
            cwl_inputs (dict): CWL inputs.
            outputs_to_record (list|None): A list of outputs to record.
            update_inputs (bool): If True, update cwl inputs with output expression (Needed for interpreting JS requirements).
            always_resolve_output (bool): If True, resolve output expression even if not in the outputs list (Needed for interpreting JS requirements).
        Returns:
        -----
            inputs (dict): Inputs or updated inputs
        """
        inputs = fill_defaults(cwl_obj, cwl_inputs)

        for output in cwl_obj.outputs:
            if not verify_cwl_output_type(output.type_):
                continue

            output_id = (
                output.id.rpartition("#")[2].split("/")[-1] if output.id else None
            )
            if not output_id:
                continue

            glob_list = self._create_glob_list(output)
            for glob in glob_list:
                resolved_glob = self._process_glob(
                    inputs, glob, outputs_to_record, output_id, always_resolve_output
                )
                if update_inputs and output_id not in inputs:
                    inputs = self._update_input_with_output(
                        inputs, resolved_glob, output, output_id
                    )

        return inputs

    @staticmethod
    def _create_glob_list(output: CommandOutputParameter) -> list:
        """
        Create a list of glob expressions.

        Args:
        -----
            output (CommandOutputParameter): The output to process.
        Returns:
        -----
            (list): A list of glob expressions.
        """
        if not output.outputBinding:
            return []
        glob_expr = output.outputBinding.glob
        return [glob_expr] if isinstance(glob_expr, str) else glob_expr or []

    def _process_glob(
        self,
        inputs: dict,
        glob: str,
        outputs_to_record: list | None,
        output_id: str,
        always_resolve_output: bool,
    ) -> str:
        """Evaluate a glob expression and record it if needed.

        Args:
        -----
            inputs (dict): CWL inputs (with added defaults).
            glob (str): The glob expression.
            outputs_to_record (list): A list of outputs to record.
            output_id (str): The current output id.
            always_resolve_output (bool): If True, resolve output expression even if not in the outputs list (Needed for interpreting JS requirements).
        """
        should_record_output = (
            outputs_to_record is None or output_id in outputs_to_record
        )
        should_eval = (
            should_record_output or always_resolve_output
        ) and glob.startswith("$")
        if should_eval:
            glob = do_eval(
                glob,
                inputs,
                outdir=None,
                requirements=[],
                tmpdir=None,
                resources={},
            )

        if should_record_output:
            if glob.startswith(LFN_PREFIX):
                self.output_data.append(glob.replace(LFN_PREFIX, LFN_DIRAC_PREFIX))
            else:
                self.output_sandbox.append(glob)

        return glob

    @staticmethod
    def _update_input_with_output(
        inputs: dict, resolved_glob: str, output: CommandOutputParameter, output_id: str
    ) -> dict:
        """Inject resolved output value into inputs for JS/parameter expressions.

        Args:
        -----
            inputs (dict): CWL inputs (with added defaults).
            resolved_glob (str): The resolved glob expression.
            output: CommandOutputParameter: The output to process.
            output_id (str): The current output id.
        Returns:
            (dict): Updated inputs.
        """
        if output.type_ == "File":
            inputs[output_id] = {
                "class": "File",
                "path": resolved_glob,
                "basename": resolved_glob,
            }
        else:
            inputs[output_id] = resolved_glob
        return inputs
