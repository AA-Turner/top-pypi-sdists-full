###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from enum import Enum, StrEnum
from typing import Any, Literal, Annotated, Union

from pydantic import (
    ConfigDict,
    StringConstraints,
    BaseModel as _BaseModel,
    field_validator,
    model_validator,
    Field,
    PositiveInt,
    TypeAdapter,
)

from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from typing import Annotated


FILETYPE_PATTERN = r"[A-Z0-9\.]+"


class ProductionStates(str, Enum):
    NEW = "New"
    ACTIVE = "Active"
    SUBMITTED = "Submitted"
    PPG_OK = "PPG OK"
    TECH_OK = "Tech OK"
    ACCEPTED = "Accepted"
    DONE = "Done"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"


class BaseModel(_BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProductionStep(BaseModel):
    id: PositiveInt | None = None
    name: str
    processing_pass: str

    class GaudirunOptions(BaseModel):
        command: Annotated[list[str], Field(min_items=1)] | None = None
        files: list[str]
        format: str | None = None
        gaudi_extra_options: str | None = None
        processing_pass: str | None = None

    class LbExecOptions(BaseModel):
        entrypoint: str
        extra_options: dict[str, Any]
        extra_args: list[str] = []

    options: list[str] | GaudirunOptions | LbExecOptions  # TODO the list of str is for legacy compatibility
    options_format: str | None = None  # TODO This should be merged into options
    visible: bool
    multicore: bool = False
    ready: bool = True
    obsolete: bool = False

    class Application(BaseModel):
        name: str
        version: str
        nightly: str | None = None
        binary_tag: str | None = None

    application: Application

    class DataPackage(BaseModel):
        name: str
        version: str

    data_pkgs: list[DataPackage] = []

    class DBTags(BaseModel):
        DDDB: str | None = None
        CondDB: str | None = None
        DQTag: str | None = None

    dbtags: DBTags | None = None

    class FileType(BaseModel):
        type: Annotated[str, StringConstraints(pattern=FILETYPE_PATTERN)]
        visible: bool

    class InputFileType(FileType):
        step_idx: int | None = None

    input: list[InputFileType]
    output: Annotated[list[FileType], Field(min_length=1)]

    @field_validator("input", "output", mode="before")
    @classmethod
    def filetype_default(cls, filetypes, values):  # pylint: disable=no-self-argument
        """Expand a list of file types into the explicit form.

        This is to allow for a convenient list of input types to be specified.
        For example::

          input:
            - type: ["STREAM1.DST", "STREAM2.MDST"]
              visible: true
            - type: STREAM3.DST
              visible: false

        becomes::

          input:
            - type: STREAM1.DST
              visible: true
            - type: STREAM2.MDST
              visible: true
            - type: STREAM3.MDST
              visible: false
        """
        cleaned_filetypes = []
        for filetype in filetypes:
            if isinstance(filetype["type"], list):
                cleaned_filetypes.extend({"type": t, "visible": filetype["visible"]} for t in filetype["type"])
            else:
                cleaned_filetypes.append(filetype)
        return cleaned_filetypes

    @field_validator("input", mode="after")
    @classmethod
    def set_default_input_step_idx(cls, input):
        for idx, input_file in enumerate(input):
            if input_file.step_idx is None:
                input_file.step_idx = idx
        return input

    @field_validator("application", mode="before")
    @classmethod
    def application_default(cls, application, values):  # pylint: disable=no-self-argument
        if isinstance(application, str):
            name, version = application.rsplit("/", 2)
            application = {"name": name, "version": version}
        return application

    @field_validator("data_pkgs", mode="before")
    @classmethod
    def data_pkgs_default(cls, data_pkgs, values):  # pylint: disable=no-self-argument
        cleaned_data_pkgs = []
        for data_pkg in data_pkgs:
            if isinstance(data_pkg, str):
                name, version = data_pkg.rsplit(".", 2)
                cleaned_data_pkgs.append({"name": name, "version": version})
            else:
                cleaned_data_pkgs.append(data_pkg)
        return cleaned_data_pkgs


class InvalidStep(Exception):
    pass


class TransformationDescription(BaseModel):
    type: str
    steps: list[int]
    output_se: str
    input_plugin: str
    group_size: int
    input_data_policy: Literal["protocol"] | Literal["download"]
    output_mode: Literal["Local"] | Literal["Run"] | Literal["Any"]

    output_file_mask: str = ""
    multicore: bool = True
    events: int = -1
    ancestor_depth: int = 0
    cpu: str = "1000000"
    priority: int = 2
    remove_inputs_flags: bool = False
    processors: tuple[int, int] = (0, 0)


class ProductionBase(BaseModel):
    type: str
    id: PositiveInt | None = None
    author: str = Field(default_factory=lambda: returnValueOrRaise(getProxyInfo())["username"])
    priority: Annotated[str, Field(pattern=r"^[12][ab]$")]
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=128)]
    inform: list[Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50)]] = []
    # TODO: I'm inclined to hardcode the list of known working groups
    wg: str
    comment: str = ""
    state: ProductionStates = ProductionStates.NEW

    steps: Annotated[list[ProductionStep], Field(min_length=1)]

    class SubmissionInfo(BaseModel):
        transforms: list[TransformationDescription]

    # TODO: will eventually be mandatory
    submission_info: SubmissionInfo | None = None

    @model_validator(mode="after")
    def validate_steps(cls, values):  # pylint: disable=no-self-argument
        current_leaves = {ft.type for ft in values.steps[0].output}
        for step in values.steps[1:]:
            for input_filetype in step.input:
                if input_filetype.type not in current_leaves:
                    raise InvalidStep(f"Failed to find input {input_filetype.type!r} for {step!r}")
                current_leaves.remove(input_filetype.type)

            for output_filetype in step.output:
                if output_filetype.type in current_leaves:
                    raise InvalidStep(
                        f"Found producer for {output_filetype.type!r} despite previous instance having not been consumed"
                    )
                current_leaves.add(output_filetype.type)
        return values


class SimulationProduction(ProductionBase):
    type: Literal["Simulation"]
    mc_config_version: str
    sim_condition: str
    fast_simulation_type: Annotated[str, Field(strip_whitespace=True, min_length=4, max_length=32)] = "None"
    # TODO This should move to EventType
    retention_rate: Annotated[float, Field(gt=0, le=1)] = 1
    override_processing_pass: str | None = None

    class EventType(BaseModel):
        id: Annotated[str, Field(pattern=r"[0-9]{8}")]
        num_events: PositiveInt
        num_test_events: PositiveInt = 10

    event_types: Annotated[list[EventType], Field(min_length=1)]


class DataProduction(ProductionBase):
    type: Literal["Sprucing", "AnalysisProduction", "Stripping", "Reconstruction"]

    class InputDataset(BaseModel):
        class BookkeepingQuery(BaseModel):
            configName: str
            configVersion: str
            inFileType: str
            inProPass: str
            # TODO: Accept None and lists on these
            inDataQualityFlag: str = "OK"
            inExtendedDQOK: Annotated[list[str], Field(min_items=1)] | None = None
            inProductionID: str = "ALL"
            inTCKs: str = "ALL"
            inSMOG2State: Annotated[list[str], Field(min_items=1)] | None = None

        conditions_dict: BookkeepingQuery
        conditions_description: str
        event_type: Annotated[str, StringConstraints(pattern=r"[0-9]{8}")]

        class LaunchParameters(BaseModel):
            """Extra info which is currently needed when making transformations from a request"""

            run_numbers: list[str] | None = None
            sample_max_md5: Annotated[str, StringConstraints(pattern=r"[A-Z0-9]{32}")] | None = None
            sample_seed_md5: Annotated[str, StringConstraints(pattern=r"[A-Z0-9]{32}")] | None = None
            start_run: int | None = None
            end_run: int | None = None

        launch_parameters: Annotated[LaunchParameters, Field(default_factory=LaunchParameters)]

    input_dataset: InputDataset


Production = Annotated[Union[SimulationProduction, DataProduction], Field(discriminator="type")]


def parse_obj(obj: Any) -> Production:
    adapter = TypeAdapter(Production)
    return adapter.validate_python(obj)
