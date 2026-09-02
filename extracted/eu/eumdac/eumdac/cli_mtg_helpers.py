import re
from eumdac.logging import logger
from typing import Tuple, List


def is_collection_valid_for_coverage(collection: str) -> bool:
    cs = [
        "0662",
        "0665",
        "0672",
    ]
    for c in cs:
        if re.match(rf"EO\:EUM(IVV|VAL)?\:DAT\:{c}(:COM)?", collection):
            return True
    return False


def build_entries_from_coverage(coverage: str) -> Tuple[List[str], int]:
    entries = []
    expected = -1

    # Using if-elif to be python < 3.10 compliant
    if coverage == "FD":
        logger.info("Downloading all chunks inside the full disk: 01-40")
        entries.extend(["*_????_00[0-3][0-9].nc", "*_????_0040.nc"])
        expected = 40
    elif coverage == "H1":
        logger.info("Downloading chunks inside H1: 01-21")
        entries.extend(["*_????_000[1-9].nc", "*_????_001[0-9].nc", "*_????_002[0-1].nc"])
        expected = 21
    elif coverage == "H2":
        logger.info("Downloading chunks inside H2: 20-40")
        entries.extend(["*_????_002[0-9].nc", "*_????_003[0-9].nc", "*_????_0040.nc"])
        expected = 21
    elif coverage == "T1":
        logger.info("Downloading chunks inside T1: 01-16")
        entries.extend(["*_????_000[1-9].nc", "*_????_001[0-6].nc"])
        expected = 16
    elif coverage == "T2":
        logger.info("Downloading chunks inside T2: 13-27")
        entries.extend(["*_????_001[3-9].nc", "*_????_002[0-7].nc"])
        expected = 15
    elif coverage == "T3":
        logger.info("Downloading chunks inside T3: 26-40")
        entries.extend(["*_????_002[6-9].nc", "*_????_003[0-9].nc", "*_????_0040.nc"])
        expected = 15
    elif coverage == "Q1":
        logger.info("Downloading chunks inside Q1: 01-13")
        entries.extend(["*_????_000[0-9].nc", "*_????_001[0-3].nc"])
        expected = 13
    elif coverage == "Q2":
        logger.info("Downloading chunks inside Q2: 10-21")
        entries.extend(["*_????_001[0-9].nc", "*_????_002[0-1].nc"])
        expected = 12
    elif coverage == "Q3":
        logger.info("Downloading chunks inside Q3: 20-30")
        entries.extend(["*_????_002[0-9].nc", "*_????_0030.nc"])
        expected = 11
    elif coverage == "Q4":
        logger.info("Downloading chunks inside Q4: 29-40")
        entries.extend(["*_????_0029.nc", "*_????_003[0-9].nc", "*_????_0040.nc"])
        expected = 12

    # Include TRAIL file (chunk 41) in all areas
    entries.append("*_????_0041.nc")
    expected += 1

    return (entries, expected)


# Removes subdirectories for printing entries
def pretty_print_entry(entry: str) -> str:
    if entry.find("/") > -1:
        return entry.split("/")[1]
    else:
        return entry
