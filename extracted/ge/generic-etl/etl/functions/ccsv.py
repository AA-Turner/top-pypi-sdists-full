import csv
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def read_csv_generator(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def intersection():
    csv1 = read_csv_generator("csv1.csv")
    csv1_dict = {row["id"]: row for row in csv1}

    intersections = []
    for row in read_csv_generator("csv2.csv"):
        if row["id"] in csv1_dict:
            intersections.append(row)
    return intersections


def custom_intersection(
    csv_one: str,
    csv_two: str,
    out_dir: str,
    column: int,
    inverse: bool = False,
    **_
) -> None:
    csv_one_column = str(Path(out_dir) / f"csv1_col{column}.txt")
    csv_two_column = str(Path(out_dir) / f"csv2_col{column}.txt")
    intersections = str(Path(out_dir) / "intersections.txt")
    intersections_one = str(Path(out_dir) / "intersections_one.txt")
    intersections_two = str(Path(out_dir) / "intersections_two.txt")
    final_intersections = str(Path(out_dir) / "final_intersections.txt")

    flag = "-Ff" if not inverse else "-vFf"

    pipeline = {
        f"Cutting column {column} from {csv_one}": {"cmd": ["cut", "-d,", f"-f{column}", csv_one], "output": csv_one_column},
        f"Cutting column {column} from {csv_two}": {"cmd": ["cut", "-d,", f"-f{column}", csv_two], "output": csv_two_column},
        "Getting inital intersection": {
            "cmd": ["grep", "-Fxf", csv_one_column, csv_two_column],
            "output": intersections,
        },
        f"Saving all intersection for {csv_one}": {
            "cmd": ["grep", flag, intersections, csv_one],
            "output": intersections_one,
        },
        f"Saving all intersections for {csv_two}": {
            "cmd": ["grep", flag, intersections, csv_two],
            "output": intersections_two,
        },
        f"Deleting header row from {intersections_two}": {
            "cmd": ["sed", "-i", "1d", intersections_two]
        },
        "Running paste": {
            #"cmd": ["paste", intersections_one, intersections_two],
            "cmd": ["cat", intersections_one, intersections_two],
            "output": final_intersections
        },
    }

    for key, value in pipeline.items():
        logger.info("%s" % key)
        cmd, out = (value.get("cmd"), value.get("output"))
        if out:
            with open(out, "w") as outfile:
                subprocess.run(cmd, stdout=outfile)
        else:
            subprocess.run(cmd)
