######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.18                                                                                #
# Generated on 2026-02-05T18:18:14.313379                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
import abc
if typing.TYPE_CHECKING:
    import _io
    import abc
    import typing
    import tarfile
    import metaflow.packaging_sys.backend

from .backend import PackagingBackend as PackagingBackend

class TarPackagingBackend(metaflow.packaging_sys.backend.PackagingBackend, metaclass=abc.ABCMeta):
    @classmethod
    def get_extract_commands(cls, archive_name: str, dest_dir: str) -> typing.List[str]:
        ...
    def __init__(self):
        ...
    def create(self):
        ...
    def add_file(self, filename: str, arcname: str | None = None):
        ...
    def add_data(self, data: _io.BytesIO, arcname: str):
        ...
    def close(self):
        ...
    def get_blob(self) -> bytes | bytearray | None:
        ...
    @classmethod
    def cls_open(cls, content: typing.IO[bytes]) -> tarfile.TarFile:
        ...
    @classmethod
    def cls_member_name(cls, member: tarfile.TarInfo | str) -> str:
        """
        Returns the name of the member as a string.
        """
        ...
    @classmethod
    def cls_has_member(cls, archive: tarfile.TarFile, name: str) -> bool:
        ...
    @classmethod
    def cls_get_member(cls, archive: tarfile.TarFile, name: str) -> bytes | None:
        ...
    @classmethod
    def cls_extract_members(cls, archive: tarfile.TarFile, members: typing.List[typing.Any] | None = None, dest_dir: str = '.'):
        ...
    @classmethod
    def cls_list_members(cls, archive: tarfile.TarFile) -> typing.List[tarfile.TarInfo] | None:
        ...
    @classmethod
    def cls_list_names(cls, archive: tarfile.TarFile) -> typing.List[str] | None:
        ...
    ...

