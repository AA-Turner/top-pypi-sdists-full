"""
Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
import json
from copy import deepcopy
from typing import Literal

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

# DIRAC imports
from CTADIRAC.Core.Utilities.tool_box import get_dataset_MQ
from CTADIRAC.Interfaces.API.CTAJob import MetadataDict
from CTADIRAC.Interfaces.API.CtapipeApplyModelsJob import CtapipeApplyModelsJob
from CTADIRAC.Interfaces.API.CtapipeMergeJob import CtapipeMergeJob
from CTADIRAC.Interfaces.API.CtapipeProcessJob import CtapipeProcessJob
from CTADIRAC.Interfaces.API.CtapipeTrainClassifierJob import CtapipeTrainClassifierJob
from CTADIRAC.Interfaces.API.CtapipeTrainEnergyJob import CtapipeTrainEnergyJob
from CTADIRAC.Interfaces.API.MCPipeJob import MCPipeJob
from CTADIRAC.Interfaces.API.MCSimTelProcessJob import MCSimTelProcessJob
from CTADIRAC.Interfaces.API.SimPipeJob import SimPipeJob


class WorkflowElementTypes:
    allowed_simulation_types: list[str] = ["mcsimulation", "simpipe"]
    allowed_processing_types: list[str] = [
        "simtelprocessing",
        "ctapipeprocessing",
        "evndispprocessing",
        "merging",
        "ctapipetrainenergy",
        "ctapipetrainclassifier",
        "ctapipeapplymodels",
    ]
    we_types: list[str] = allowed_simulation_types + allowed_processing_types


class WorkflowElementDefinition:
    """Defines variables depending on WorkflowElement type"""

    def __init__(self, we_type: str) -> None:
        self.allowed_simulation_types: list[
            str
        ] = WorkflowElementTypes.allowed_simulation_types
        self.allowed_processing_types: list[
            str
        ] = WorkflowElementTypes.allowed_processing_types
        self.mandatory_keys: set[str] = {"MCCampaign", "configuration_id", "version"}
        self.constrained_input_keys: set[str] = {
            "pointing_dir",
            "zenith_angle",
            "moon",
            "sct",
            "div_ang",
        }
        self.constrained_job_keys: set[str] = {
            "catalogs",
            "group_size",
            "destination",
            "cpu_time",
            "tag",
            "nb_processors",
            "input_sandbox",
        }
        self.file_meta_fields: set[str] = {"nsb", "div_ang"}
        self.mandatory_job_config_keys: dict = {}
        self.we_type: Literal(WorkflowElementTypes.we_types) = we_type
        self.prod_step = ProductionStep()
        self.prod_step.Type = "DataReprocessing"
        self.moon_nsb_dict = {
            "dark": 1,
            "half": 5,
            "full": 19,
        }
        self.initialize()

    def initialize(self) -> None:
        """Initialize variables depending on WE type"""
        if self.we_type == "mcsimulation":
            self.job = MCPipeJob()
            self.prod_step.Type = "MCSimulation"
            self.prod_step.Name = "MCSimulation"
            self.constrained_job_keys.update(
                [
                    "version",
                    "sct",
                    "particle",
                    "pointing_dir",
                    "layout",
                    "moon",
                    "only_corsika",
                    "magic",
                    "div_ang",
                    "sequential",
                    "random_mono_probability",
                    "instrument_random_seeds",
                ]
            )
        elif self.we_type == "simpipe":
            self.job = SimPipeJob()
            self.prod_step.Type = "MCSimulation"
            self.prod_step.Name = "MCSimulation"
            self.constrained_job_keys.update(
                [
                    "version",
                    "simpipe_config",
                ]
            )
            self.mandatory_job_config_keys = {"simpipe_config"}
        elif self.we_type == "simtelprocessing":
            self.job = MCSimTelProcessJob()
            self.prod_step.Name = "SimTelProcessing"
            self.constrained_job_keys.update(
                [
                    "version",
                    "sct",
                    "moon",
                    "div_ang",
                    "random_mono_probability",
                    "instrument_random_seeds",
                    "systematic_uncertainty_to_test",
                ]
            )
        elif self.we_type == "ctapipeprocessing":
            self.job = CtapipeProcessJob()
            self.prod_step.Name = "CtapipeProcessing"
            self.mandatory_job_config_keys = {"data_level", "output_extension"}
            self.file_meta_fields.add("split")

        elif self.we_type == "evndispprocessing":
            from CTADIRAC.Interfaces.API.EvnDispJob import EvnDispJob

            self.job = EvnDispJob()
            self.prod_step.Name = "EvnDisp"

        elif self.we_type == "merging":
            self.job = CtapipeMergeJob()
            self.prod_step.Type = "Merging"
            self.prod_step.Name = "Merging"
            self.mandatory_job_config_keys = {"output_extension"}
            self.file_meta_fields.add("split")

        elif self.we_type == "ctapipetrainenergy":
            self.job = CtapipeTrainEnergyJob()
            self.prod_step.Type = "Training"
            self.prod_step.Name = "CtapipeTrainEnergy"

        elif self.we_type == "ctapipetrainclassifier":
            self.job = CtapipeTrainClassifierJob()
            self.prod_step.Type = "Training"
            self.prod_step.Name = "CtapipeTrainClassifier"

        elif self.we_type == "ctapipeapplymodels":
            self.job = CtapipeApplyModelsJob()
            self.prod_step.Type = "ApplyModel"
            self.prod_step.Name = "CtapipeApplyModels"
            self.file_meta_fields.add("split")
        else:
            self.job = Job()
            self.mandatory_keys = {}


class WorkflowElement(WorkflowElementDefinition):
    """Composite class for workflow element (production step + job)"""

    def __init__(self, parent_prod_step: int, we_type: str) -> None:
        WorkflowElementDefinition.__init__(self, we_type)
        self.prod_step.ParentStep = parent_prod_step
        self.fc = FileCatalogClient()

    def set_constrained_job_attribute(self, key, value) -> None:
        """Set job attribute with constraints"""
        if key == "catalogs":
            # remove whitespaces between catalogs if there are some and separate between commas
            setattr(self.job, key, json.dumps(value.replace(", ", ",").split(sep=",")))
        elif key == "destination":
            self.job.setDestination(value)
        elif key == "input_sandbox":
            self.job.setInputSandbox(
                value if "," not in value else value.replace(", ", ",").split(sep=",")
            )
        elif key == "cpu_time":
            self.job.setCPUTime(value)
        elif key == "tag":
            self.job.setTag(value)
        elif key == "nb_processors":
            self.job.setNumberOfProcessors(minNumberOfProcessors=value)
        elif key == "version":
            if "-sc" not in str(
                value
            ):  # if the version has not already been set by 'sct'
                self.job.version = str(value)
        elif key == "particle":
            self.job.set_particle(value)
        elif key == "pointing_dir":
            self.job.set_pointing_dir(value)
        elif key == "layout":
            self.job.set_layout(value)
        elif key == "sct":
            self.job.set_sct(value)
        elif key == "moon":
            self.job.set_moon(
                value if "," not in value else value.replace(", ", ",").split(sep=",")
            )
        elif key == "only_corsika":
            self.job.set_only_corsika(value)
        elif key == "magic":
            self.job.set_magic(value)
        elif key == "sequential":
            self.job.set_sequential_mode(value)
        elif key == "div_ang":
            self.job.set_div_ang(value)
        elif key == "random_mono_probability":
            self.job.set_random_mono_probability(value)
        elif key == "instrument_random_seeds":
            self.job.set_instrument_random_seeds(value)
        elif key == "systematic_uncertainty_to_test":
            self.job.set_systematic_uncertainty_to_test(value)
        elif key == "group_size":
            setattr(self.job, key, value)
            self.prod_step.GroupSize = self.job.group_size
        elif key == "simpipe_config":
            self.job.set_simpipe_config(value)
        else:
            setattr(self.job, key, value)

    def set_constrained_input_query(self, key, value) -> None:
        """Set input meta query with constraints"""
        if self.we_type in self.allowed_processing_types:
            self.set_constrained_processing_input_query(key, value)
        else:
            self.prod_step.Inputquery[key] = value

    def set_constrained_processing_input_query(self, key, value) -> None:
        """Set processing input meta query with constraints"""
        if key == "pointing_dir":
            if value == "North":
                self.prod_step.Inputquery["phiP"] = 180
            elif value == "South":
                self.prod_step.Inputquery["phiP"] = 0
        elif key == "zenith_angle":
            self.prod_step.Inputquery["thetaP"] = float(value)
        elif key == "sct":
            self.prod_step.Inputquery["sct"] = str(value)
        elif key == "moon":
            self.prod_step.Inputquery["nsb"] = self.moon_nsb_dict[value]
        elif key == "div_ang":
            self.prod_step.Inputquery["div_ang"] = str(value)

    def build_job_attributes_from_job_config(self, workflow_step) -> None:
        """Build job attributes with job_config values"""
        for key in self.mandatory_job_config_keys:
            if key not in workflow_step["job_config"]:
                DIRAC.gLogger.error(f"{key} is mandatory")
                DIRAC.exit(-1)
        for key, value in workflow_step["job_config"].items():
            if value is not None:
                if key in self.constrained_job_keys:
                    self.set_constrained_job_attribute(key, value)
                elif key in self.file_meta_fields:
                    self.job.output_file_metadata[key] = value
                else:
                    setattr(self.job, key, value)
            elif key in self.mandatory_keys:
                DIRAC.gLogger.error(f"{key} is mandatory")
                DIRAC.exit(-1)
        for key in self.mandatory_keys:
            if key not in self.job.__dict__:
                DIRAC.gLogger.error(f"{key} is mandatory")
                DIRAC.exit(-1)

    def build_job_attributes_from_common(self, workflow_config) -> None:
        """Build job attributes concerning the whole production"""
        for key, value in workflow_config["Common"].items():
            if value is not None:
                setattr(self.job, key, value)
            elif key in self.mandatory_keys:
                DIRAC.gLogger.error(f"{key} is mandatory")
                DIRAC.exit(-1)

    def build_job_attributes_from_input(self) -> None:
        """Set job attributes from input meta query"""
        for key, value in self.prod_step.Inputquery.items():
            if key in self.file_meta_fields:
                try:
                    self.job.output_file_metadata[key] = value["="]
                except (KeyError, TypeError):
                    self.job.output_file_metadata[key] = value
                except Exception as e:
                    print(f"Unexpected exception for key {key}: {e}")
                    raise
            else:
                self.set_attribute(self.job, key, value, "=")

    def set_attribute(self, obj, key, value, sym) -> None:
        try:
            setattr(obj, key, value[f"{sym}"])
        except (KeyError, TypeError):
            setattr(obj, key, value)
        except Exception as e:
            print(f"Unexpected exception for key {key}: {e}")
            raise

    def build_job_attributes(self, workflow_config, workflow_step) -> None:
        """Set job attributes"""
        self.build_job_attributes_from_input()
        self.build_job_attributes_from_common(workflow_config)
        self.build_job_attributes_from_job_config(workflow_step)

    def build_input_data(self, workflow_step) -> None:
        """Build input data"""
        self.prod_step.Inputquery = {}
        if self.we_type not in self.allowed_simulation_types:
            if self.prod_step.ParentStep:
                self.prod_step.Inputquery = self.prod_step.ParentStep.Outputquery
            else:
                if workflow_step["input_meta_query"].get("dataset"):
                    self.prod_step.Inputquery = get_dataset_MQ(
                        workflow_step["input_meta_query"]["dataset"]
                    )

            self.refine_input_MQ(workflow_step)

    def refine_input_MQ(self, workflow_step) -> None:
        """refine input MQ by adding extra specification if needed"""
        for key, value in workflow_step["input_meta_query"].items():
            if value is not None:
                if key in self.constrained_input_keys:
                    self.set_constrained_input_query(key, value)
                elif (key != "dataset") and (key != "parentID"):
                    self.prod_step.Inputquery[key] = value

    def build_job_input_data(self, mode) -> None:
        """Limit the nb of input data to process (for testing purpose)"""
        if self.we_type not in self.allowed_simulation_types:
            res = self.fc.findFilesByMetadata(dict(self.prod_step.Inputquery))
            if not res["OK"]:
                DIRAC.gLogger.error(res["Message"])
                DIRAC.exit(-1)
            input_data_limit = self.job.input_limit
            input_data = res["Value"][:input_data_limit]
            if mode.lower() in ["wms", "local"]:
                self.job.setInputData(input_data)
            if not input_data and mode.lower() == "wms":
                DIRAC.gLogger.error("No job submitted: job must have input data")
                DIRAC.exit(-1)
            if mode.lower() == "ps" and self.job.input_limit:
                f = open("test_input_data.list", "w")
                for lfn in input_data:
                    f.write(lfn + "\n")
                f.close()
                DIRAC.gLogger.notice(
                    f"\t\tInput limit found: {len(input_data)} files dumped to test_input_data.list"
                )
                self.prod_step.Inputquery = {}

    def build_element_config(self, workflow_step) -> None:
        """Set job and production step attributes specific to the configuration"""
        if self.we_type in ["evndispprocessing", "merging"]:
            self.prod_step.GroupSize = self.job.group_size
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()
        if "name" in workflow_step:
            self.prod_step.Name = workflow_step["name"]

    def build_job_output_data(self, workflow_step) -> None:
        """Build job output meta data"""
        if self.we_type in self.allowed_processing_types:
            metadata = deepcopy(self.prod_step.Inputquery)
            for key, value in workflow_step["job_config"].items():
                if key == "moon":
                    metadata["nsb"] = self.moon_nsb_dict[value]
                elif key == "instrument_random_seeds":
                    continue
                else:
                    metadata[key] = value
            if self.we_type == "merging":
                merged = self.get_merging_level()
                metadata["merged"] = merged
            self.job.set_output_metadata(metadata)
        elif self.we_type in self.allowed_simulation_types:
            if self.we_type == "mcsimulation":
                phi_p = 180 if self.job.pointing_dir == "North" else 0
            elif self.we_type == "simpipe":
                phi_p = float(round((float(self.job.azimuth_angle) + 180) % 360, 2))

            metadata: MetadataDict = MetadataDict(
                array_layout=self.job.array_layout,
                site=self.job.site,
                particle=self.job.particle,
                phiP=phi_p,
                thetaP=float(self.job.zenith_angle),
                sct="True" if self.job.sct else "False",
                outputType=self.job.output_type,
            )
            self.job.set_output_metadata(metadata)

    def get_merging_level(self) -> int:
        """Get the merging level from parent step or from the user query"""
        if self.prod_step.ParentStep:
            try:
                merged = self.prod_step.ParentStep.Outputquery["merged"]
            except KeyError:
                merged = 0
        else:
            merged = self.job.merged
        return merged

    def build_output_data(self) -> None:
        """Build output data from the job metadata and the metadata added on the files"""
        self.prod_step.Outputquery = deepcopy(self.job.output_metadata)
        for key, value in self.job.output_file_metadata.items():
            if isinstance(value, list):
                if len(value) > 1:
                    self.prod_step.Outputquery[key] = {"in": value}
                else:
                    self.prod_step.Outputquery[key] = value[0]
            else:
                self.prod_step.Outputquery[key] = value
