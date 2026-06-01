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
from typing import TYPE_CHECKING, overload, Optional, Union, Generic, TypeVar, TypeAlias


from ..builder import build_object
from ..types import aliases
from . import TLMethod, ReturnT


if TYPE_CHECKING:
    from ..types import *
    from ..methods import *

class FoldersEditPeerFolders(TLMethod[aliases.AnyUpdates]):
    __slots__ = ()

    @overload
    def __init__(self, folder_peers: list[aliases.AnyInputFolderPeer]): ...

    def __init__(self, folder_peers, _='folders.editPeerFolders', **kwargs):
        kwargs['folder_peers'] = folder_peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_peers(self) -> list[aliases.AnyInputFolderPeer]:
        return build_object(self['folder_peers'])
