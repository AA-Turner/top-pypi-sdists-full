# Copyright 2026 zovdev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import TYPE_CHECKING, overload, Optional


from ..builder import build_object
from . import aliases


if TYPE_CHECKING:
    from ..types import *


class StorageFileUnknown(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileUnknown'):
        dict.__init__(self, _=_)


class StorageFilePartial(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.filePartial'):
        dict.__init__(self, _=_)


class StorageFileJpeg(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileJpeg'):
        dict.__init__(self, _=_)


class StorageFileGif(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileGif'):
        dict.__init__(self, _=_)


class StorageFilePng(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.filePng'):
        dict.__init__(self, _=_)


class StorageFilePdf(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.filePdf'):
        dict.__init__(self, _=_)


class StorageFileMp3(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileMp3'):
        dict.__init__(self, _=_)


class StorageFileMov(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileMov'):
        dict.__init__(self, _=_)


class StorageFileMp4(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileMp4'):
        dict.__init__(self, _=_)


class StorageFileWebp(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='storage.fileWebp'):
        dict.__init__(self, _=_)
