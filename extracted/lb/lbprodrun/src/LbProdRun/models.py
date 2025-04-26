###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

import typer
from packaging.version import Version
from pydantic import BaseModel as _BaseModel
from pydantic import Field, TypeAdapter, ValidationError, field_validator
from typer import colors as c


class BaseModel(_BaseModel, extra="forbid", validate_assignment=True):
    pass


def _parse_version(version: str) -> Union[Version, bool]:
    """Parse a version string into a Version object

    If this fails, it will return a bool indicating a safe default value
    for if an application supports modern features or not.
    """
    try:
        parsed_version = Version(re.sub(r"[^\d]+", ".", version).strip("."))
    except Exception:  # pylint: disable=broad-except
        typer.secho(f"Failed to parse {version!r}", fg="red")
        if version == "HEAD":
            return True
        return False
    return parsed_version


class BaseApplication(BaseModel):
    name: str
    version: str
    event_timeout: Optional[float] = None
    number_of_processors: int = 1

    @property
    def is_lbexec(self) -> bool:
        """Determine if a given application/version combination should use lbexec"""
        parsed_version = _parse_version(self.version)
        if isinstance(parsed_version, bool):
            return parsed_version

        version_compatibility: dict[str, Union[bool, Version]] = {
            "Analysis": Version("40"),
            "DaVinci": Version("60"),
            "Lbcom": Version("33"),
            "LHCb": Version("53"),
            "Moore": Version("53"),
            "Rec": Version("34"),
            # New-style only applications
            "Allen": True,
            "Detector": True,
            # Old-style only applications
            "Brunel": False,
            "Castelao": False,
            "Gauss": False,
            "Boole": False,
        }

        if self.is_lbconda:
            return True

        is_new_style = version_compatibility.get(self.name)
        if is_new_style is None:
            typer.secho(
                f"Unknown application {self.name!r}, assuming old-style", fg="yellow"
            )
            is_new_style = False
        if isinstance(is_new_style, bool):
            return is_new_style
        return is_new_style < parsed_version

    @property
    def supports_input_run_number(self) -> bool:
        """The application is lbexec and supports the input_run_number

        Was added in https://gitlab.cern.ch/lhcb/LHCb/-/merge_requests/4934
        """
        parsed_version = _parse_version(self.version)
        if isinstance(parsed_version, bool):
            return parsed_version

        version_compatibility: dict[str, Version] = {
            "DaVinci": Version("65.1"),
            "LHCb": Version("56.3"),
            "Moore": Version("56.2"),
        }

        if self.is_lbconda:
            return False
        min_version = version_compatibility.get(self.name)
        if min_version is None:
            return False
        return parsed_version >= min_version

    @property
    def uses_gaudi_mp(self) -> bool:
        parsed_version = _parse_version(self.version)
        if isinstance(parsed_version, bool):
            return parsed_version

        # Gauss v60+ supports multi-threading despite still using ProdConf
        if self.name == "Gauss":
            return parsed_version < Version("60")

        # Otherwise assume only lbexec-style applications support native multi-threading
        return self.is_lbexec

    @property
    def is_lbconda(self):
        """Check whether an lb-conda environment is requested, return the name and version else None."""

        if not self.name.startswith("lb-conda/"):
            return None

        env_name = self.name.split("/", 1)[1]

        return env_name, self.version


class JobSpecV1(BaseModel):
    spec_version: Literal[1]

    class ReleaseApplication(BaseApplication):
        data_pkgs: list[str] = []
        binary_tag: str = "best"
        nightly: Optional[str] = None

    class LbDevApplication(BaseApplication):
        project_base: Path
        binary_tag: str

    class FullDevApplication(BaseApplication):
        run_script: Path

    # It would be nice to use Discriminated Unions here to get better error
    # messages but that requires an new JobSpec version as there would need to
    # be a required ``Literal`` property on each ``BaseApplication`` subclass
    application: Union[ReleaseApplication, LbDevApplication, FullDevApplication]

    class LegacyOptions(BaseModel):
        command: Annotated[
            list[str],
            Field(default_factory=lambda: ["gaudirun.py", "-T"], min_length=1),
        ] = []
        # FIXME: Ideally this should be annotated however there are too many buggy steps
        # files: Annotated[list[str], Field(min_length=1)]
        files: list[str]
        format: Optional[str] = None
        gaudi_extra_options: Optional[str] = None
        processing_pass: Optional[str] = None

        @field_validator("command", mode="before")
        @classmethod
        def set_command(cls, command):  # noqa: B902  # pylint: disable=no-self-argument
            return command or ["gaudirun.py", "-T"]

    class LbExecOptions(BaseModel):
        entrypoint: str
        extra_options: dict[str, Any]
        extra_args: list[str] = []

    options: Union[LegacyOptions, LbExecOptions]

    class Input(BaseModel):
        files: Optional[list[str]] = None
        xml_summary_file: Optional[str] = None
        xml_file_catalog: Optional[str] = None
        run_number: Optional[int] = None
        tck: Optional[str] = None
        n_of_events: int = -1
        first_event_number: Optional[int] = None

    input: Input = Input()

    class Output(BaseModel):
        prefix: str
        types: list[str]
        histogram_file: Optional[str] = None
        compression: Optional[str] = None

    output: Output

    class DBTags(BaseModel):
        dddb_tag: Optional[str] = None
        conddb_tag: Optional[str] = None
        dq_tag: Optional[str] = None

    db_tags: DBTags = DBTags()


def read_jobspec(spec_file: Path):
    JobSpec = Annotated[Union[JobSpecV1], Field(discriminator="spec_version")]
    JobSpecAdapter = TypeAdapter(JobSpec)

    try:
        return JobSpecAdapter.validate_json(spec_file.read_text())
    except ValidationError as e:
        errors = e.errors()
        typer.secho(
            f"Found {len(errors)} error{'s' if len(errors) > 1 else ''} "
            f"when validating {spec_file}:",
            fg=c.RED,
        )
        for error in e.errors():
            if error["type"] == "value_error.missing":
                message = f"Field {'.'.join(map(str, error['loc']))!r} is required"
            else:
                message = f"{'.'.join(map(str, error['loc']))}: {error['msg']}"
            typer.secho(f"  * {message}", fg=c.RED)
        raise typer.Exit(101) from e
