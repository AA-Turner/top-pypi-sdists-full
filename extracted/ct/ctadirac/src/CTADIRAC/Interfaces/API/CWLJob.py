"""DIRAC Job API to execute CWL with cwltool."""

import tempfile
from pathlib import Path

from cwl_utils.parser import save
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Interfaces.API.Job import Job
from ruamel.yaml import YAML

from CTADIRAC.Interfaces.Utilities.CWLTranslator import CWLTranslator


class CWLJob(Job, CWLTranslator):
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
        cwl_workflow: str,
        cwl_inputs: str,
        cvmfs_base_path: Path,
        output_se=None,
        apptainer_options: list | None = None,
    ) -> None:
        Job.__init__(self)
        CWLTranslator.__init__(self, cwl_workflow, cwl_inputs)

        self.cvmfs_base_path = cvmfs_base_path
        self.apptainer_options = apptainer_options if apptainer_options else []
        self._output_se = output_se

        self.translate(self.cvmfs_base_path, self.apptainer_options)

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
