from typing import overload
from enum import IntEnum
import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.IO
import System.Runtime.InteropServices


class CriticalHandleMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self) -> None:
        ...


class SafeHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self, owns_handle: bool) -> None:
        ...


class SafeFileHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @property
    def type(self) -> System.IO.FileHandleType:
        ...

    @property
    def is_async(self) -> bool:
        ...

    @property
    def is_invalid(self) -> bool:
        ...

    @overload
    def __init__(self, preexisting_handle: System.IntPtr, owns_handle: bool) -> None:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @staticmethod
    @overload
    def create_anonymous_pipe(read_handle: typing.Optional[Microsoft.Win32.SafeHandles.SafeFileHandle], write_handle: typing.Optional[Microsoft.Win32.SafeHandles.SafeFileHandle], async_read: bool = False, async_write: bool = False) -> typing.Tuple[None, Microsoft.Win32.SafeHandles.SafeFileHandle, Microsoft.Win32.SafeHandles.SafeFileHandle]:
        ...

    @staticmethod
    @overload
    def create_anonymous_pipe(read_handle: typing.Optional[Microsoft.Win32.SafeHandles.SafeFileHandle], write_handle: typing.Optional[Microsoft.Win32.SafeHandles.SafeFileHandle], async_read: bool, async_write: bool) -> typing.Tuple[None, Microsoft.Win32.SafeHandles.SafeFileHandle, Microsoft.Win32.SafeHandles.SafeFileHandle]:
        ...

    def release_handle(self) -> bool:
        ...


class CriticalHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self) -> None:
        ...


class SafeWaitHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, existing_handle: System.IntPtr, owns_handle: bool) -> None:
        ...

    def release_handle(self) -> bool:
        ...


class SafeHandleMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self, owns_handle: bool) -> None:
        ...


