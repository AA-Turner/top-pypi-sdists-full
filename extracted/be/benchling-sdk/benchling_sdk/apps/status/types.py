from typing import Union

from benchling_sdk.models import (
    AaSequence,
    Blob,
    Box,
    Container,
    CustomEntity,
    DnaOligo,
    DnaSequence,
    Entry,
    Folder,
    Location,
    Mixture,
    Molecule,
    Plate,
    Request,
    RnaOligo,
    RnaSequence,
    WorkflowOutput,
    WorkflowTask,
)

# Taken from CHIP_SUPPORTED_COLUMN_TYPES in Benchling server
# Anything we miss, they can still embed the ID themselves in a message
ReferencedSessionLinkType = Union[
    AaSequence,
    Blob,
    Box,
    Container,
    CustomEntity,
    DnaSequence,
    DnaOligo,
    Entry,
    Folder,
    Location,
    Mixture,
    Plate,
    RnaOligo,
    Molecule,
    RnaSequence,
    Request,
    WorkflowOutput,
    WorkflowTask,
]
