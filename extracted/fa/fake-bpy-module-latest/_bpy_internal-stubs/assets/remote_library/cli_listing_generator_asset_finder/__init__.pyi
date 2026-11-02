import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

class FileVersionInfo:
    """Version information of a single blend file.It contains information not just based on the file itself, but also based
    on the other discovered files. For example, asset.blend will get a
    blender_version_until = (6, 0) when a file asset@b6_0.blend is found.
    """

    blender_version_min: typing.Any
    blender_version_until: typing.Any

def filenames_group_by_version_metadata(paths) -> None:
    """Determine min/until versions for the given filenames."""

def list_assets(blendfile_version_info, asset_library_root) -> None: ...
