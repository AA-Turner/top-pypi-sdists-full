import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def svg(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    filter_glob: str | None = "*.svg",
    directory: str | None = "",
    files=None,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Load a SVG file

    :param filepath: File Path, Filepath used for importing the file (optional, never None)
    :param filter_glob: filter_glob, (optional, never None)
    :param directory: directory, (optional, never None)
    :param files: File Path, (optional)
    :return: Result of the operator call.
    """
