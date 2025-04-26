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
import os
import shlex
import shutil
from pathlib import Path
from pprint import pformat

import typer
import yaml
from LbEnv.ProjectEnv.lookup import findDataPackage  # type: ignore
from LbEnv.ProjectEnv.script import decodePkg  # type: ignore

from .models import JobSpecV1, read_jobspec


def run_job(
    spec_file: Path,
    *,
    dry_run=False,
    gaudi_dry_run=False,
    verbose=False,
    interactive=False,
    prmon=False,
):
    job_spec = read_jobspec(spec_file)
    if verbose:
        typer.secho("Expanded spec file as:", fg=typer.colors.GREEN)
        typer.secho(pformat(job_spec.model_dump()))
    execute(
        job_spec,
        dry_run=dry_run,
        gaudi_dry_run=gaudi_dry_run,
        interactive=interactive,
        prmon=prmon,
    )


def _write_prod_conf_options(job_spec, path: Path, verbose=False):
    """Write an options file for the ProdConf data package"""
    data = {
        "Application": job_spec.application.name,
        "AppVersion": job_spec.application.version,
        "OptionFormat": job_spec.options.format,
        "InputFiles": job_spec.input.files,
        "OutputFilePrefix": job_spec.output.prefix,
        "OutputFileTypes": job_spec.output.types,
        "XMLSummaryFile": job_spec.input.xml_summary_file,
        "XMLFileCatalog": job_spec.input.xml_file_catalog,
        "HistogramFile": job_spec.output.histogram_file,
        "DDDBTag": job_spec.db_tags.dddb_tag,
        "CondDBTag": job_spec.db_tags.conddb_tag,
        "DQTag": job_spec.db_tags.dq_tag,
        "NOfEvents": job_spec.input.n_of_events,
        "RunNumber": job_spec.input.run_number,
        "FirstEventNumber": job_spec.input.first_event_number,
        "TCK": job_spec.input.tck,
        "ProcessingPass": job_spec.options.processing_pass,
    }
    if job_spec.application.uses_gaudi_mp:
        data["NThreads"] = 1
    else:
        data["NThreads"] = job_spec.application.number_of_processors

    lines = ["from ProdConf import ProdConf", ""]
    lines += ["ProdConf("]
    lines += [f"    {k}={v!r}," for k, v in data.items() if v is not None]
    lines += [")"]
    string = "\n".join(lines)

    if verbose:
        typer.secho(f"Going to write in {path}", fg=typer.colors.GREEN)
        typer.secho(string)
    path.write_text(string)


def execute(
    job_spec, *, dry_run=False, gaudi_dry_run=False, interactive=False, prmon=False
):
    command = []

    if not prmon:
        pass
    elif interactive:
        typer.secho("Not using prmon as this is an interactive run!", fg="yellow")
    elif shutil.which("prmon") is None:
        typer.secho("Not using prmon as it wasn't found on $PATH!", fg="yellow")
    else:
        command += ["prmon"]
        command += ["--interval", os.environ.get("LBPRODRUN_PRMON_INTERVAL", "60")]
        command += ["--filename", f"prmon_{job_spec.output.prefix}.txt"]
        command += ["--json-summary", f"prmon_{job_spec.output.prefix}.json"]
        command += ["--"]

    if isinstance(job_spec.application, JobSpecV1.FullDevApplication):
        command += [str(job_spec.application.run_script.absolute())]
    elif (
        isinstance(job_spec.application, JobSpecV1.ReleaseApplication)
        and job_spec.application.is_lbconda
    ):
        env_name, env_version = job_spec.application.is_lbconda

        command += ["lb-conda"]
        command += [f"{env_name}/{env_version}"]

        if job_spec.application.data_pkgs:
            command += ["xenv"]
            for pkg_name, pkg_vers in map(decodePkg, job_spec.application.data_pkgs):
                xml_name = pkg_name.replace("/", "_") + ".xenv"
                xml_path = os.path.join(findDataPackage(pkg_name, pkg_vers), xml_name)
                if not os.path.exists(xml_path):
                    # fall back on the old conventional name
                    xml_path = xml_path[:-5] + "Environment.xml"
                # FIXME: xenv has got problems with unicode filenames
                command += [f"--xml={xml_path}"]
    else:
        command += ["lb-run"]
        command += ["--siteroot=/cvmfs/lhcb.cern.ch/lib/"]
        command += ["-c", f"{job_spec.application.binary_tag}"]
        for ep in job_spec.application.data_pkgs:
            command += [f"--use={ep}"]
        if not job_spec.application.is_lbexec:
            command += ["--use=ProdConf"]

        if isinstance(job_spec.application, JobSpecV1.ReleaseApplication):
            typer.secho(
                f"Executing application {job_spec.application.name} "
                f"{job_spec.application.version} for binary tag configuration "
                f"{job_spec.application.binary_tag}"
            )

            if job_spec.application.nightly:
                command += [f"--nightly={job_spec.application.nightly}"]

            app = job_spec.application.name
            if job_spec.application.version:
                app += "/" + job_spec.application.version
            command += [app]
        elif isinstance(job_spec.application, JobSpecV1.LbDevApplication):
            typer.secho(
                f"Executing custom application with {job_spec.application.run_script}"
            )

            command += ["--path-to-project"]
            command += [str(job_spec.application.project_base.absolute())]
        else:
            raise NotImplementedError(type(job_spec.application))

    if job_spec.application.is_lbexec:
        inner_command = _make_lbexec_command(job_spec, dry_run=gaudi_dry_run)
    else:
        inner_command = _make_gaudirun_command(job_spec, dry_run=gaudi_dry_run)

    if interactive:
        command += ["bash", "--norc", "--noprofile"]
        typer.secho("Starting application environment with:")
        typer.secho(shlex.join(command))
        typer.secho("#" * 80)
        typer.secho("Entering interactive mode, now run:", fg="green")
        typer.secho(shlex.join(inner_command))
        typer.secho("#" * 80)
    else:
        typer.secho("Executing command:", fg="green")
        command += inner_command
        typer.secho(shlex.join(command))
    if dry_run:
        typer.secho("Exiting early as this is a dry run!", fg="yellow")
        return
    os.execvpe(command[0], command, _prepare_env())


def _make_lbexec_command(job_spec, dry_run=False):
    if not isinstance(job_spec.options, JobSpecV1.LbExecOptions):
        raise NotImplementedError(
            "New-style options spec is required for "
            f"{job_spec.application.name}/{job_spec.application.version}"
        )

    options_yaml_fn = Path(f"lbexec_options_{job_spec.output.prefix}.yaml")
    _write_options_yaml(job_spec, options_yaml_fn, verbose=False)
    command = ["lbexec"]
    if dirname := os.environ.get("LBPRODRUN_OPTIONS_DUMP_DIR"):
        options_dump = Path(dirname) / f"{job_spec.output.prefix}_dump.json"
        command += ["--export", str(options_dump)]
    if dry_run:
        command += ["--dry-run"]
    command += [job_spec.options.entrypoint, str(options_yaml_fn)]
    return command + job_spec.options.extra_args


def _write_options_yaml(job_spec, path: Path, verbose=False):
    """Write an options file for lbexec"""
    options = job_spec.options.extra_options.copy()
    # FIXME: Can't actually use this option yet as it doesn't fail if the keys are missing
    # options["write_decoding_keys_to_git"] = False

    if job_spec.input.files:
        options["input_files"] = job_spec.input.files
    if job_spec.input.run_number and job_spec.application.supports_input_run_number:
        options["input_run_number"] = job_spec.input.run_number
    if job_spec.db_tags.dddb_tag:
        options["dddb_tag"] = job_spec.db_tags.dddb_tag
    if job_spec.db_tags.conddb_tag:
        options["conddb_tag"] = job_spec.db_tags.conddb_tag
    if job_spec.db_tags.dq_tag:
        options["dq_tag"] = job_spec.db_tags.dq_tag
    if job_spec.input.n_of_events > 0:
        options["evt_max"] = job_spec.input.n_of_events
    if job_spec.input.first_event_number:
        options["first_evt"] = job_spec.input.first_event_number
    if job_spec.output.histogram_file:
        options["histo_file"] = job_spec.output.histogram_file
    if job_spec.application.event_timeout:
        options["event_timeout"] = job_spec.application.event_timeout
    if job_spec.input.xml_summary_file:
        options["xml_summary_file"] = job_spec.input.xml_summary_file
    if job_spec.input.xml_file_catalog:
        options["xml_file_catalog"] = job_spec.input.xml_file_catalog
    if job_spec.output.compression:
        options["compression"] = job_spec.output.compression
    if job_spec.application.number_of_processors:
        options["n_threads"] = job_spec.application.number_of_processors

    prefix = job_spec.output.prefix
    output_filetypes = []
    for filetype in job_spec.output.types:
        if filetype.lower().endswith("hist"):
            if "histo_file" in options:
                raise NotImplementedError("Multiple histogram files found")
            options["histo_file"] = f"{prefix}.{filetype}"
        elif filetype.lower().endswith(".root") and not job_spec.application.is_lbconda:
            ntuple_file = f"{prefix}.{filetype}"
            if "ntuple_file" in options and ntuple_file != options["ntuple_file"]:
                raise NotImplementedError("Multiple ntuple files found")
            options["ntuple_file"] = ntuple_file
        else:
            output_filetypes.append(filetype)

    if len(output_filetypes) == 1:
        options["output_file"] = f"{prefix}.{output_filetypes[0]}"
    elif len(output_filetypes) > 1:
        split = [tuple(x.rsplit(".", 1)) for x in output_filetypes]
        lens = {len(s) for s in split}
        if len(lens) > 1:
            raise ValueError("Inconsistent values in OutputFileTypes")
        if lens.pop() != 2:  # no '.' in the OutputFileTypes
            raise ValueError("Different OutputFileTypes not supported")
        _, ext = list(zip(*split))
        if len(set(ext)) != 1:
            raise ValueError("Inconsistent extensions in OutputFileTypes")
        options["output_file"] = f"{prefix}.{{stream}}.{ext[0].lower()}"

    string = yaml.safe_dump(options)
    if verbose:
        typer.secho(f"Going to write in {path}", fg=typer.colors.GREEN)
        typer.secho(string)
    path.write_text(string)


def _make_gaudirun_command(job_spec, dry_run=False):
    if not isinstance(job_spec.options, JobSpecV1.LegacyOptions):
        raise NotImplementedError(
            "Old-style options spec is required for "
            f"{job_spec.application.name}/{job_spec.application.version}"
        )

    prod_conf_fn = Path(f"prodConf_{job_spec.output.prefix}.py")
    _write_prod_conf_options(job_spec, prod_conf_fn, verbose=False)

    command = []
    command += job_spec.options.command
    if job_spec.options.command[0] == "gaudirun.py":
        if dirname := os.environ.get("LBPRODRUN_OPTIONS_DUMP_DIR"):
            options_dump = Path(dirname) / f"{job_spec.output.prefix}_dump.py"
            command += ["--output", str(options_dump)]
    if dry_run:
        if job_spec.options.command[0] != "gaudirun.py":
            raise ValueError("Dry run is only supported for gaudirun.py")
        command += ["--dry-run"]
    if job_spec.application.uses_gaudi_mp:
        if job_spec.application.number_of_processors > 1:
            command += ["--ncpus", f"{job_spec.application.number_of_processors}"]
    command += job_spec.options.files
    command += [str(prod_conf_fn)]

    extra_options = job_spec.options.gaudi_extra_options or ""
    if job_spec.application.event_timeout:
        extra_options = "\n".join(
            [
                extra_options,
                "from Configurables import StalledEventMonitor",
                f"StalledEventMonitor(EventTimeout={job_spec.application.event_timeout})",
            ]
        )
    if extra_options:
        extra_options_path = Path("gaudi_extra_options.py")
        extra_options_path.write_text(extra_options, encoding="utf-8")
        command += [str(extra_options_path)]

    return command


def _prepare_env():
    """Get a dictionary containing the environment that should be used for the job"""
    env = os.environ.copy()
    # Versions of Brunel used for 2018 data use XGBoost which uses OpenMP to
    # provide parallelism and automatically spawns one thread for each CPU.
    # Use OMP_NUM_THREADS to force it to only use one thread
    env["OMP_NUM_THREADS"] = "1"
    return env
