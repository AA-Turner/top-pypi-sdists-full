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
from pathlib import Path

import typer

from . import run_job

app = typer.Typer()


@app.command()
def main(
    job_spec: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    dry_run: bool = False,
    gaudi_dry_run: bool = False,
    prmon: bool = False,
    verbose: bool = False,
    interactive: bool = False,
):
    typer.echo(f"Reading specification from {job_spec}")
    run_job(
        job_spec,
        dry_run=dry_run,
        gaudi_dry_run=gaudi_dry_run,
        prmon=prmon,
        verbose=verbose,
        interactive=interactive,
    )


if __name__ == "__main__":
    app()  # pragma: no cover
