######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.20                                                                                #
# Generated on 2026-02-26T21:59:51.275927                                                            #
######################################################################################################

from __future__ import annotations

import typing
import abc
if typing.TYPE_CHECKING:
    import typing
    import abc
    import _io


class PackagingBackend(abc.ABC, metaclass=abc.ABCMeta):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        ...
    @classmethod
    def get_backend(cls, name: str) -> "PackagingBackend":
        ...
    @classmethod
    def backend_type(cls) -> str:
        ...
    @classmethod
    def get_extract_commands(cls, archive_name: str, dest_dir: str) -> typing.List[str]:
        ...
    def __init__(self):
        ...
    def create(self) -> "PackagingBackend":
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
    def cls_open(cls, content: typing.IO[bytes]) -> typing.Any:
        """
        Open the archive from the given content.
        """
        ...
    @classmethod
    def cls_member_name(cls, member: typing.Any | str) -> str:
        """
        Returns the name of the member as a string.
        This is used to ensure consistent naming across different archive formats.
        """
        ...
    @classmethod
    def cls_has_member(cls, archive: typing.Any, name: str) -> bool:
        ...
    @classmethod
    def cls_get_member(cls, archive: typing.Any, name: str) -> bytes | None:
        ...
    @classmethod
    def cls_extract_members(cls, archive: typing.Any, members: typing.List[typing.Any] | None = None, dest_dir: str = '.'):
        ...
    @classmethod
    def cls_list_names(cls, archive: typing.Any) -> typing.List[str] | None:
        ...
    @classmethod
    def cls_list_members(cls, archive: typing.Any) -> typing.List[typing.Any] | None:
        """
        List all members in the archive.
        """
        ...
    def has_member(self, name: str) -> bool:
        ...
    def get_member(self, name: str) -> bytes | None:
        ...
    def extract_members(self, members: typing.List[typing.Any] | None = None, dest_dir: str = '.'):
        ...
    def list_names(self) -> typing.List[str] | None:
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    ...

