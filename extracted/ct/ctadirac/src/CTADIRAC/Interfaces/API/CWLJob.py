"""DIRAC Job API to execute CWL with cwltool."""

import tempfile
from pathlib import Path

from cwl_utils.pack import pack
from cwl_utils.parser import load_document, save
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Interfaces.API.Job import Job
from cwl_utils.parser.utils import load_inputfile
from ruamel.yaml import YAML

from CTADIRAC.Interfaces.Utilities.CWL_utils import (
    translate_cwl_workflow,
)


class CWLJob(Job):
    """Job class for CWL jobs.
    Submits CommandLineTool using cwltool executable.

    Attrs:
        cwl_workflow: a Path to the local CWL workflow file
        cwl_inputs: a Path to the local CWL inputs file
        cvmfs_base_path: the CVMFS base Path
        apptainer_options: additional apptainer options (default: [])
    """

    def __init__(
        self,
        cwl_workflow: Path,
        cwl_inputs: Path,
        cvmfs_base_path: Path,
        output_se=None,
        apptainer_options: list | None = None,
    ) -> None:
        super().__init__()

        self.cwl_workflow_path = Path(cwl_workflow)
        self.cwl_inputs_path = Path(cwl_inputs)

        self.cvmfs_base_path = cvmfs_base_path
        self.apptainer_options = apptainer_options if apptainer_options else []
        self._output_se = output_se

        self.original_cwl = load_document(pack(str(self.cwl_workflow_path)))
        self.original_inputs = load_inputfile(
            self.original_cwl.cwlVersion, self.cwl_inputs_path.read_text()
        )

        cwl_dict = translate_cwl_workflow(
            self.original_cwl,
            self.original_inputs,
            self.cvmfs_base_path,
            self.apptainer_options,
        )

        self.transformed_cwl = cwl_dict["CWLDesc"]
        self.output_sandbox = cwl_dict.get("OutputSandbox", [])
        self.output_data = cwl_dict.get("OutputData", [])

        self.transformed_inputs = cwl_dict["InputDesc"]
        self.input_data = cwl_dict.get("InputData", [])
        self.input_sandbox = cwl_dict.get("InputSandbox", [])

    def submit(self):
        """Submit the CWL job to DIRAC.

        Treat local input and output files as sandbox,
        files starting with 'lfn://' are treated as input/output data
        and translate docker requirements.
        """
        dirac = Dirac()
        yaml = YAML()

        # Create the modified Dirac compliant CWL workflow and inputs files to submit
        with tempfile.NamedTemporaryFile(
            suffix=f"_{self.cwl_workflow_path.name}"
        ) as temp_workflow:
            yaml.dump(save(self.transformed_cwl), temp_workflow)
            temp_workflow.flush()

            with tempfile.NamedTemporaryFile(
                suffix=f"_{self.cwl_inputs_path.name}"
            ) as temp_inputs:
                yaml.dump(save(self.transformed_inputs), temp_inputs)
                temp_inputs.flush()

                self.setInputSandbox(
                    [str(temp_workflow.file.name), str(temp_inputs.name)]
                    + self.input_sandbox
                )
                if self.output_sandbox:
                    self.setOutputSandbox(self.output_sandbox)
                if self.input_data:
                    self.setInputData(self.input_data)
                if self.output_data:
                    self.setOutputData(self.output_data, outputSE=self._output_se)

                arguments_str = (
                    f"{Path(temp_workflow.name).name} {Path(temp_inputs.name).name}"
                )

                self.setExecutable(
                    "cwltool", arguments=arguments_str, logFile=f"{self.name}.log"
                )
                res = dirac.submitJob(self)
        return res
