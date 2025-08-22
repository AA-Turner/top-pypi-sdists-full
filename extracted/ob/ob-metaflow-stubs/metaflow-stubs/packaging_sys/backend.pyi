######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.17.1.0+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-21T23:31:59.702142                                                            #
######################################################################################################

from __future__ import annotations

import abc
import typing
if typing.TYPE_CHECKING:
    import abc
    import io
    import typing


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
    def add_file(self, filename: str, arcname: typing.Optional[str] = None):
        ...
    def add_data(self, data: io.BytesIO, arcname: str):
        ...
    def close(self):
        ...
    def get_blob(self) -> typing.Union[bytes, bytearray, None]:
        ...
    @classmethod
    def cls_open(cls, content: typing.IO[bytes]) -> typing.Any:
        """
        Open the archive from the given content.
        """
        ...
    @classmethod
    def cls_member_name(cls, member: typing.Union[typing.Any, str]) -> str:
        """
        Returns the name of the member as a string.
        This is used to ensure consistent naming across different archive formats.
        """
        ...
    @classmethod
    def cls_has_member(cls, archive: typing.Any, name: str) -> bool:
        ...
    @classmethod
    def cls_get_member(cls, archive: typing.Any, name: str) -> typing.Optional[bytes]:
        ...
    @classmethod
    def cls_extract_members(cls, archive: typing.Any, members: typing.Optional[typing.List[typing.Any]] = None, dest_dir: str = '.'):
        ...
    @classmethod
    def cls_list_names(cls, archive: typing.Any) -> typing.Optional[typing.List[str]]:
        ...
    @classmethod
    def cls_list_members(cls, archive: typing.Any) -> typing.Optional[typing.List[typing.Any]]:
        """
        List all members in the archive.
        """
        ...
    def has_member(self, name: str) -> bool:
        ...
    def get_member(self, name: str) -> typing.Optional[bytes]:
        ...
    def extract_members(self, members: typing.Optional[typing.List[typing.Any]] = None, dest_dir: str = '.'):
        ...
    def list_names(self) -> typing.Optional[typing.List[str]]:
        ...
    def __enter__(self):
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    ...

