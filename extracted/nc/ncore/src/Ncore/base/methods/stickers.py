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

class StickersCreateStickerSet(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, title: str, short_name: str, stickers: list[aliases.AnyInputStickerSetItem], masks: Optional[bool] = ..., emojis: Optional[bool] = ..., text_color: Optional[bool] = ..., thumb: Optional[aliases.AnyInputDocument] = ..., software: Optional[str] = ...): ...

    def __init__(self, user_id, title, short_name, stickers, _='stickers.createStickerSet', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['title'] = title
        kwargs['short_name'] = short_name
        kwargs['stickers'] = stickers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def text_color(self) -> Optional[bool]:
        return self['text_color']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def thumb(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['thumb'])

    @property
    def stickers(self) -> list[aliases.AnyInputStickerSetItem]:
        return build_object(self['stickers'])

    @property
    def software(self) -> Optional[str]:
        return self['software']


class StickersRemoveStickerFromSet(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, sticker: aliases.AnyInputDocument): ...

    def __init__(self, sticker, _='stickers.removeStickerFromSet', **kwargs):
        kwargs['sticker'] = sticker
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sticker(self) -> aliases.AnyInputDocument:
        return build_object(self['sticker'])


class StickersChangeStickerPosition(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, sticker: aliases.AnyInputDocument, position: int): ...

    def __init__(self, sticker, position, _='stickers.changeStickerPosition', **kwargs):
        kwargs['sticker'] = sticker
        kwargs['position'] = position
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sticker(self) -> aliases.AnyInputDocument:
        return build_object(self['sticker'])

    @property
    def position(self) -> int:
        return self['position']


class StickersAddStickerToSet(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, sticker: aliases.AnyInputStickerSetItem): ...

    def __init__(self, stickerset, sticker, _='stickers.addStickerToSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['sticker'] = sticker
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def sticker(self) -> aliases.AnyInputStickerSetItem:
        return build_object(self['sticker'])


class StickersSetStickerSetThumb(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, thumb: Optional[aliases.AnyInputDocument] = ..., thumb_document_id: Optional[int] = ...): ...

    def __init__(self, stickerset, _='stickers.setStickerSetThumb', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def thumb(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['thumb'])

    @property
    def thumb_document_id(self) -> Optional[int]:
        return self['thumb_document_id']


class StickersCheckShortName(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, short_name: str): ...

    def __init__(self, short_name, _='stickers.checkShortName', **kwargs):
        kwargs['short_name'] = short_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def short_name(self) -> str:
        return self['short_name']


class StickersSuggestShortName(TLMethod[aliases.AnyStickersSuggestedShortName]):
    __slots__ = ()

    @overload
    def __init__(self, title: str): ...

    def __init__(self, title, _='stickers.suggestShortName', **kwargs):
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']


class StickersChangeSticker(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, sticker: aliases.AnyInputDocument, emoji: Optional[str] = ..., mask_coords: Optional[aliases.AnyMaskCoords] = ..., keywords: Optional[str] = ...): ...

    def __init__(self, sticker, _='stickers.changeSticker', **kwargs):
        kwargs['sticker'] = sticker
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sticker(self) -> aliases.AnyInputDocument:
        return build_object(self['sticker'])

    @property
    def emoji(self) -> Optional[str]:
        return self['emoji']

    @property
    def mask_coords(self) -> Optional[aliases.AnyMaskCoords]:
        return build_object(self['mask_coords'])

    @property
    def keywords(self) -> Optional[str]:
        return self['keywords']


class StickersRenameStickerSet(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, title: str): ...

    def __init__(self, stickerset, title, _='stickers.renameStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def title(self) -> str:
        return self['title']


class StickersDeleteStickerSet(TLMethod[bool]):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, stickerset, _='stickers.deleteStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])


class StickersReplaceSticker(TLMethod[aliases.AnyMessagesStickerSet]):
    __slots__ = ()

    @overload
    def __init__(self, sticker: aliases.AnyInputDocument, new_sticker: aliases.AnyInputStickerSetItem): ...

    def __init__(self, sticker, new_sticker, _='stickers.replaceSticker', **kwargs):
        kwargs['sticker'] = sticker
        kwargs['new_sticker'] = new_sticker
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sticker(self) -> aliases.AnyInputDocument:
        return build_object(self['sticker'])

    @property
    def new_sticker(self) -> aliases.AnyInputStickerSetItem:
        return build_object(self['new_sticker'])
