from typing import Any, List

from tinybird.datafile.common import Datafile

DATAFILE_NEW_LINE = "\n"
DATAFILE_INDENT = " " * 4


def format_description(file_parts: List[str], doc: Any) -> List[str]:
    description = doc.description if doc.description is not None else ""
    if description:
        file_parts.append("DESCRIPTION >")
        file_parts.append(DATAFILE_NEW_LINE)
        [
            file_parts.append(f"{DATAFILE_INDENT}{d.strip()}\n")  # type: ignore
            for d in description.split(DATAFILE_NEW_LINE)
            if d.strip()
        ]
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_maintainer(file_parts: List[str], doc: Datafile) -> List[str]:
    maintainer = doc.maintainer if doc.maintainer is not None else ""
    if maintainer:
        file_parts.append(f"MAINTAINER {maintainer}")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tokens(file_parts: List[str], doc: Datafile) -> List[str]:
    for token in doc.tokens:
        file_parts.append(f'TOKEN "{token["token_name"]}" {token["permissions"]}')
        file_parts.append(DATAFILE_NEW_LINE)
    if len(doc.tokens):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tags(file_parts: List[str], doc: Datafile) -> List[str]:
    if doc.filtering_tags:
        file_parts.append(f'TAGS "{", ".join(doc.filtering_tags)}"')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_include(file_parts: List[str], doc: Datafile, unroll_includes: bool = False) -> List[str]:
    if unroll_includes:
        return file_parts

    assert doc.raw is not None

    include = [line for line in doc.raw if "INCLUDE" in line and ".incl" in line]
    if include:
        file_parts.append(include[0])
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts
