import json
from datetime import datetime

import click
from spoton_soozaccess import SoozAccess, daterange

from .datagenerator import DataGenerator
from .group import Group
from .logger import Logger


@click.command()
@click.option(
    "-f", "--filename", type=str, help="path to json data file.", required=True
)
@click.option(
    "-s", "--samples", type=int, help="number of samples to generate", required=True
)
@click.option(
    "-h", "--host", type=str, help="url to host", default="http://localhost:3000"
)
@click.option(
    "-v", "--verbose", count=True, help="show results and interface", default=False
)
@click.option(
    "-d",
    "--startdate",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="start date to generate data for",
)
def generator(
    filename: str,
    host: str,
    samples: int,
    verbose: bool,
    startdate: datetime,
):
    """Main entry for SooZ data generator."""

    # create log instance
    Logger.verbose = verbose

    # import group personas from json file
    with open(filename, "r") as f:
        group = Group.load(json.load(f))

    # prepare database
    # SoozAccess.verbose = verbose
    # SoozAccess.host = host
    # SoozAccess.prepare_users(group.name, group.user_names)

    # display
    Logger.write(
        f"[{'GENERATOR':10s}] Imported group '{group.name}' with {len(group.people)} people from {len(group.personas)} personas."
    )

    # data generation
    for p in group.personas:
        for rating in p.ratings:
            Logger.write(f"[{'GENERATOR':10s}] {p.name}. rating id: {rating.id}")

            datagen = DataGenerator(startdate, rating, samples)
            datagen.fill()
            datagen.show(p)

            # with SoozAccess(p.name, p.name) as user:
            #     for day in daterange(startdate, samples):
            #         user.put_response(2, 2, 3, day.strftime("%Y-%m-%d"))


if __name__ == "__main__":
    generator()
