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


class Error(dict):
    __slots__ = ()

    @overload
    def __init__(self, code: int, text: str): ...

    def __init__(self, code, text, _='error', **kwargs):
        kwargs['code'] = code
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def code(self) -> int:
        return self['code']

    @property
    def text(self) -> str:
        return self['text']


class InputPeerEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPeerEmpty'):
        dict.__init__(self, _=_)


class InputPeerSelf(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPeerSelf'):
        dict.__init__(self, _=_)


class InputPeerChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='inputPeerChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class InputPeerUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, access_hash: int): ...

    def __init__(self, user_id, access_hash, _='inputPeerUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputPeerChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, access_hash: int): ...

    def __init__(self, channel_id, access_hash, _='inputPeerChannel', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputPeerUserFromMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, user_id: int): ...

    def __init__(self, peer, msg_id, user_id, _='inputPeerUserFromMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def user_id(self) -> int:
        return self['user_id']


class InputPeerChannelFromMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, channel_id: int): ...

    def __init__(self, peer, msg_id, channel_id, _='inputPeerChannelFromMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def channel_id(self) -> int:
        return self['channel_id']


class InputUserEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputUserEmpty'):
        dict.__init__(self, _=_)


class InputUserSelf(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputUserSelf'):
        dict.__init__(self, _=_)


class InputUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, access_hash: int): ...

    def __init__(self, user_id, access_hash, _='inputUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputUserFromMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, user_id: int): ...

    def __init__(self, peer, msg_id, user_id, _='inputUserFromMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def user_id(self) -> int:
        return self['user_id']


class InputPhoneContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, client_id: int, phone: str, first_name: str, last_name: str, note: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, client_id, phone, first_name, last_name, _='inputPhoneContact', **kwargs):
        kwargs['client_id'] = client_id
        kwargs['phone'] = phone
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def client_id(self) -> int:
        return self['client_id']

    @property
    def phone(self) -> str:
        return self['phone']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def note(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['note'])


class InputFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, parts: int, name: str, md5_checksum: str): ...

    def __init__(self, id, parts, name, md5_checksum, _='inputFile', **kwargs):
        kwargs['id'] = id
        kwargs['parts'] = parts
        kwargs['name'] = name
        kwargs['md5_checksum'] = md5_checksum
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def parts(self) -> int:
        return self['parts']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def md5_checksum(self) -> str:
        return self['md5_checksum']


class InputFileBig(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, parts: int, name: str): ...

    def __init__(self, id, parts, name, _='inputFileBig', **kwargs):
        kwargs['id'] = id
        kwargs['parts'] = parts
        kwargs['name'] = name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def parts(self) -> int:
        return self['parts']

    @property
    def name(self) -> str:
        return self['name']


class InputFileStoryDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument): ...

    def __init__(self, id, _='inputFileStoryDocument', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])


class InputMediaEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMediaEmpty'):
        dict.__init__(self, _=_)


class InputMediaUploadedPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, file: aliases.AnyInputFile, spoiler: Optional[bool] = ..., stickers: Optional[list[aliases.AnyInputDocument]] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, file, _='inputMediaUploadedPhoto', **kwargs):
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def stickers(self) -> Optional[list[aliases.AnyInputDocument]]:
        return build_object(self['stickers'])

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class InputMediaPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPhoto, spoiler: Optional[bool] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, id, _='inputMediaPhoto', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def id(self) -> aliases.AnyInputPhoto:
        return build_object(self['id'])

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class InputMediaGeoPoint(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint): ...

    def __init__(self, geo_point, _='inputMediaGeoPoint', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])


class InputMediaContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, first_name: str, last_name: str, vcard: str): ...

    def __init__(self, phone_number, first_name, last_name, vcard, _='inputMediaContact', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['vcard'] = vcard
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def vcard(self) -> str:
        return self['vcard']


class InputMediaUploadedDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, file: aliases.AnyInputFile, mime_type: str, attributes: list[aliases.AnyDocumentAttribute], nosound_video: Optional[bool] = ..., force_file: Optional[bool] = ..., spoiler: Optional[bool] = ..., thumb: Optional[aliases.AnyInputFile] = ..., stickers: Optional[list[aliases.AnyInputDocument]] = ..., video_cover: Optional[aliases.AnyInputPhoto] = ..., video_timestamp: Optional[int] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, file, mime_type, attributes, _='inputMediaUploadedDocument', **kwargs):
        kwargs['file'] = file
        kwargs['mime_type'] = mime_type
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def nosound_video(self) -> Optional[bool]:
        return self['nosound_video']

    @property
    def force_file(self) -> Optional[bool]:
        return self['force_file']

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def file(self) -> aliases.AnyInputFile:
        return build_object(self['file'])

    @property
    def thumb(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['thumb'])

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def attributes(self) -> list[aliases.AnyDocumentAttribute]:
        return build_object(self['attributes'])

    @property
    def stickers(self) -> Optional[list[aliases.AnyInputDocument]]:
        return build_object(self['stickers'])

    @property
    def video_cover(self) -> Optional[aliases.AnyInputPhoto]:
        return build_object(self['video_cover'])

    @property
    def video_timestamp(self) -> Optional[int]:
        return self['video_timestamp']

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class InputMediaDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument, spoiler: Optional[bool] = ..., video_cover: Optional[aliases.AnyInputPhoto] = ..., video_timestamp: Optional[int] = ..., ttl_seconds: Optional[int] = ..., query: Optional[str] = ...): ...

    def __init__(self, id, _='inputMediaDocument', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])

    @property
    def video_cover(self) -> Optional[aliases.AnyInputPhoto]:
        return build_object(self['video_cover'])

    @property
    def video_timestamp(self) -> Optional[int]:
        return self['video_timestamp']

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']

    @property
    def query(self) -> Optional[str]:
        return self['query']


class InputMediaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, title: str, address: str, provider: str, venue_id: str, venue_type: str): ...

    def __init__(self, geo_point, title, address, provider, venue_id, venue_type, _='inputMediaVenue', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['title'] = title
        kwargs['address'] = address
        kwargs['provider'] = provider
        kwargs['venue_id'] = venue_id
        kwargs['venue_type'] = venue_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def address(self) -> str:
        return self['address']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def venue_id(self) -> str:
        return self['venue_id']

    @property
    def venue_type(self) -> str:
        return self['venue_type']


class InputMediaPhotoExternal(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, spoiler: Optional[bool] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, url, _='inputMediaPhotoExternal', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class InputMediaDocumentExternal(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, spoiler: Optional[bool] = ..., ttl_seconds: Optional[int] = ..., video_cover: Optional[aliases.AnyInputPhoto] = ..., video_timestamp: Optional[int] = ...): ...

    def __init__(self, url, _='inputMediaDocumentExternal', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']

    @property
    def video_cover(self) -> Optional[aliases.AnyInputPhoto]:
        return build_object(self['video_cover'])

    @property
    def video_timestamp(self) -> Optional[int]:
        return self['video_timestamp']


class InputMediaGame(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputGame): ...

    def __init__(self, id, _='inputMediaGame', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputGame:
        return build_object(self['id'])


class InputMediaInvoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, invoice: aliases.AnyInvoice, payload: bytes, provider_data: aliases.AnyDataJSON, photo: Optional[aliases.AnyInputWebDocument] = ..., provider: Optional[str] = ..., start_param: Optional[str] = ..., extended_media: Optional[aliases.AnyInputMedia] = ...): ...

    def __init__(self, title, description, invoice, payload, provider_data, _='inputMediaInvoice', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['payload'] = payload
        kwargs['provider_data'] = provider_data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyInputWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def payload(self) -> bytes:
        return self['payload']

    @property
    def provider(self) -> Optional[str]:
        return self['provider']

    @property
    def provider_data(self) -> aliases.AnyDataJSON:
        return build_object(self['provider_data'])

    @property
    def start_param(self) -> Optional[str]:
        return self['start_param']

    @property
    def extended_media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['extended_media'])


class InputMediaGeoLive(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, stopped: Optional[bool] = ..., heading: Optional[int] = ..., period: Optional[int] = ..., proximity_notification_radius: Optional[int] = ...): ...

    def __init__(self, geo_point, _='inputMediaGeoLive', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stopped(self) -> Optional[bool]:
        return self['stopped']

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def heading(self) -> Optional[int]:
        return self['heading']

    @property
    def period(self) -> Optional[int]:
        return self['period']

    @property
    def proximity_notification_radius(self) -> Optional[int]:
        return self['proximity_notification_radius']


class InputMediaPoll(dict):
    __slots__ = ()

    @overload
    def __init__(self, poll: aliases.AnyPoll, correct_answers: Optional[list[bytes]] = ..., solution: Optional[str] = ..., solution_entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, poll, _='inputMediaPoll', **kwargs):
        kwargs['poll'] = poll
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def poll(self) -> aliases.AnyPoll:
        return build_object(self['poll'])

    @property
    def correct_answers(self) -> Optional[list[bytes]]:
        return self['correct_answers']

    @property
    def solution(self) -> Optional[str]:
        return self['solution']

    @property
    def solution_entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['solution_entities'])


class InputMediaDice(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='inputMediaDice', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class InputMediaStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, id: int): ...

    def __init__(self, peer, id, _='inputMediaStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']


class InputMediaWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, force_large_media: Optional[bool] = ..., force_small_media: Optional[bool] = ..., optional: Optional[bool] = ...): ...

    def __init__(self, url, _='inputMediaWebPage', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force_large_media(self) -> Optional[bool]:
        return self['force_large_media']

    @property
    def force_small_media(self) -> Optional[bool]:
        return self['force_small_media']

    @property
    def optional(self) -> Optional[bool]:
        return self['optional']

    @property
    def url(self) -> str:
        return self['url']


class InputMediaPaidMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars_amount: int, extended_media: list[aliases.AnyInputMedia], payload: Optional[str] = ...): ...

    def __init__(self, stars_amount, extended_media, _='inputMediaPaidMedia', **kwargs):
        kwargs['stars_amount'] = stars_amount
        kwargs['extended_media'] = extended_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars_amount(self) -> int:
        return self['stars_amount']

    @property
    def extended_media(self) -> list[aliases.AnyInputMedia]:
        return build_object(self['extended_media'])

    @property
    def payload(self) -> Optional[str]:
        return self['payload']


class InputMediaTodo(dict):
    __slots__ = ()

    @overload
    def __init__(self, todo: aliases.AnyTodoList): ...

    def __init__(self, todo, _='inputMediaTodo', **kwargs):
        kwargs['todo'] = todo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def todo(self) -> aliases.AnyTodoList:
        return build_object(self['todo'])


class InputMediaStakeDice(dict):
    __slots__ = ()

    @overload
    def __init__(self, game_hash: str, ton_amount: int, client_seed: bytes): ...

    def __init__(self, game_hash, ton_amount, client_seed, _='inputMediaStakeDice', **kwargs):
        kwargs['game_hash'] = game_hash
        kwargs['ton_amount'] = ton_amount
        kwargs['client_seed'] = client_seed
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def game_hash(self) -> str:
        return self['game_hash']

    @property
    def ton_amount(self) -> int:
        return self['ton_amount']

    @property
    def client_seed(self) -> bytes:
        return self['client_seed']


class InputChatPhotoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputChatPhotoEmpty'):
        dict.__init__(self, _=_)


class InputChatUploadedPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, file: Optional[aliases.AnyInputFile] = ..., video: Optional[aliases.AnyInputFile] = ..., video_start_ts: Optional[float] = ..., video_emoji_markup: Optional[aliases.AnyVideoSize] = ...): ...

    def __init__(self, _='inputChatUploadedPhoto', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['file'])

    @property
    def video(self) -> Optional[aliases.AnyInputFile]:
        return build_object(self['video'])

    @property
    def video_start_ts(self) -> Optional[float]:
        return self['video_start_ts']

    @property
    def video_emoji_markup(self) -> Optional[aliases.AnyVideoSize]:
        return build_object(self['video_emoji_markup'])


class InputChatPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPhoto): ...

    def __init__(self, id, _='inputChatPhoto', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputPhoto:
        return build_object(self['id'])


class InputGeoPointEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputGeoPointEmpty'):
        dict.__init__(self, _=_)


class InputGeoPoint(dict):
    __slots__ = ()

    @overload
    def __init__(self, lat: float, long: float, accuracy_radius: Optional[int] = ...): ...

    def __init__(self, lat, long, _='inputGeoPoint', **kwargs):
        kwargs['lat'] = lat
        kwargs['long'] = long
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lat(self) -> float:
        return self['lat']

    @property
    def long(self) -> float:
        return self['long']

    @property
    def accuracy_radius(self) -> Optional[int]:
        return self['accuracy_radius']


class InputPhotoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPhotoEmpty'):
        dict.__init__(self, _=_)


class InputPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes): ...

    def __init__(self, id, access_hash, file_reference, _='inputPhoto', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']


class InputFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, volume_id: int, local_id: int, secret: int, file_reference: bytes): ...

    def __init__(self, volume_id, local_id, secret, file_reference, _='inputFileLocation', **kwargs):
        kwargs['volume_id'] = volume_id
        kwargs['local_id'] = local_id
        kwargs['secret'] = secret
        kwargs['file_reference'] = file_reference
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def volume_id(self) -> int:
        return self['volume_id']

    @property
    def local_id(self) -> int:
        return self['local_id']

    @property
    def secret(self) -> int:
        return self['secret']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']


class InputEncryptedFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputEncryptedFileLocation', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputDocumentFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes, thumb_size: str): ...

    def __init__(self, id, access_hash, file_reference, thumb_size, _='inputDocumentFileLocation', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['thumb_size'] = thumb_size
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']

    @property
    def thumb_size(self) -> str:
        return self['thumb_size']


class InputSecureFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputSecureFileLocation', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputTakeoutFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputTakeoutFileLocation'):
        dict.__init__(self, _=_)


class InputPhotoFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes, thumb_size: str): ...

    def __init__(self, id, access_hash, file_reference, thumb_size, _='inputPhotoFileLocation', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['thumb_size'] = thumb_size
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']

    @property
    def thumb_size(self) -> str:
        return self['thumb_size']


class InputPhotoLegacyFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes, volume_id: int, local_id: int, secret: int): ...

    def __init__(self, id, access_hash, file_reference, volume_id, local_id, secret, _='inputPhotoLegacyFileLocation', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['volume_id'] = volume_id
        kwargs['local_id'] = local_id
        kwargs['secret'] = secret
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']

    @property
    def volume_id(self) -> int:
        return self['volume_id']

    @property
    def local_id(self) -> int:
        return self['local_id']

    @property
    def secret(self) -> int:
        return self['secret']


class InputPeerPhotoFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, photo_id: int, big: Optional[bool] = ...): ...

    def __init__(self, peer, photo_id, _='inputPeerPhotoFileLocation', **kwargs):
        kwargs['peer'] = peer
        kwargs['photo_id'] = photo_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def big(self) -> Optional[bool]:
        return self['big']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def photo_id(self) -> int:
        return self['photo_id']


class InputStickerSetThumb(dict):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, thumb_version: int): ...

    def __init__(self, stickerset, thumb_version, _='inputStickerSetThumb', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['thumb_version'] = thumb_version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def thumb_version(self) -> int:
        return self['thumb_version']


class InputGroupCallStream(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, time_ms: int, scale: int, video_channel: Optional[int] = ..., video_quality: Optional[int] = ...): ...

    def __init__(self, call, time_ms, scale, _='inputGroupCallStream', **kwargs):
        kwargs['call'] = call
        kwargs['time_ms'] = time_ms
        kwargs['scale'] = scale
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def time_ms(self) -> int:
        return self['time_ms']

    @property
    def scale(self) -> int:
        return self['scale']

    @property
    def video_channel(self) -> Optional[int]:
        return self['video_channel']

    @property
    def video_quality(self) -> Optional[int]:
        return self['video_quality']


class PeerUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int): ...

    def __init__(self, user_id, _='peerUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']


class PeerChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='peerChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class PeerChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int): ...

    def __init__(self, channel_id, _='peerChannel', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']


class UserEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='userEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class User(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, self_: Optional[bool] = ..., contact: Optional[bool] = ..., mutual_contact: Optional[bool] = ..., deleted: Optional[bool] = ..., bot: Optional[bool] = ..., bot_chat_history: Optional[bool] = ..., bot_nochats: Optional[bool] = ..., verified: Optional[bool] = ..., restricted: Optional[bool] = ..., min: Optional[bool] = ..., bot_inline_geo: Optional[bool] = ..., support: Optional[bool] = ..., scam: Optional[bool] = ..., apply_min_photo: Optional[bool] = ..., fake: Optional[bool] = ..., bot_attach_menu: Optional[bool] = ..., premium: Optional[bool] = ..., attach_menu_enabled: Optional[bool] = ..., bot_can_edit: Optional[bool] = ..., close_friend: Optional[bool] = ..., stories_hidden: Optional[bool] = ..., stories_unavailable: Optional[bool] = ..., contact_require_premium: Optional[bool] = ..., bot_business: Optional[bool] = ..., bot_has_main_app: Optional[bool] = ..., bot_forum_view: Optional[bool] = ..., bot_forum_can_manage_topics: Optional[bool] = ..., access_hash: Optional[int] = ..., first_name: Optional[str] = ..., last_name: Optional[str] = ..., username: Optional[str] = ..., phone: Optional[str] = ..., photo: Optional[aliases.AnyUserProfilePhoto] = ..., status: Optional[aliases.AnyUserStatus] = ..., bot_info_version: Optional[int] = ..., restriction_reason: Optional[list[aliases.AnyRestrictionReason]] = ..., bot_inline_placeholder: Optional[str] = ..., lang_code: Optional[str] = ..., emoji_status: Optional[aliases.AnyEmojiStatus] = ..., usernames: Optional[list[aliases.AnyUsername]] = ..., stories_max_id: Optional[aliases.AnyRecentStory] = ..., color: Optional[aliases.AnyPeerColor] = ..., profile_color: Optional[aliases.AnyPeerColor] = ..., bot_active_users: Optional[int] = ..., bot_verification_icon: Optional[int] = ..., send_paid_messages_stars: Optional[int] = ...): ...

    def __init__(self, id, _='user', **kwargs):
        kwargs['id'] = id
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def self_(self) -> Optional[bool]:
        return self['self']

    @property
    def contact(self) -> Optional[bool]:
        return self['contact']

    @property
    def mutual_contact(self) -> Optional[bool]:
        return self['mutual_contact']

    @property
    def deleted(self) -> Optional[bool]:
        return self['deleted']

    @property
    def bot(self) -> Optional[bool]:
        return self['bot']

    @property
    def bot_chat_history(self) -> Optional[bool]:
        return self['bot_chat_history']

    @property
    def bot_nochats(self) -> Optional[bool]:
        return self['bot_nochats']

    @property
    def verified(self) -> Optional[bool]:
        return self['verified']

    @property
    def restricted(self) -> Optional[bool]:
        return self['restricted']

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def bot_inline_geo(self) -> Optional[bool]:
        return self['bot_inline_geo']

    @property
    def support(self) -> Optional[bool]:
        return self['support']

    @property
    def scam(self) -> Optional[bool]:
        return self['scam']

    @property
    def apply_min_photo(self) -> Optional[bool]:
        return self['apply_min_photo']

    @property
    def fake(self) -> Optional[bool]:
        return self['fake']

    @property
    def bot_attach_menu(self) -> Optional[bool]:
        return self['bot_attach_menu']

    @property
    def premium(self) -> Optional[bool]:
        return self['premium']

    @property
    def attach_menu_enabled(self) -> Optional[bool]:
        return self['attach_menu_enabled']

    @property
    def bot_can_edit(self) -> Optional[bool]:
        return self['bot_can_edit']

    @property
    def close_friend(self) -> Optional[bool]:
        return self['close_friend']

    @property
    def stories_hidden(self) -> Optional[bool]:
        return self['stories_hidden']

    @property
    def stories_unavailable(self) -> Optional[bool]:
        return self['stories_unavailable']

    @property
    def contact_require_premium(self) -> Optional[bool]:
        return self['contact_require_premium']

    @property
    def bot_business(self) -> Optional[bool]:
        return self['bot_business']

    @property
    def bot_has_main_app(self) -> Optional[bool]:
        return self['bot_has_main_app']

    @property
    def bot_forum_view(self) -> Optional[bool]:
        return self['bot_forum_view']

    @property
    def bot_forum_can_manage_topics(self) -> Optional[bool]:
        return self['bot_forum_can_manage_topics']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> Optional[int]:
        return self['access_hash']

    @property
    def first_name(self) -> Optional[str]:
        return self['first_name']

    @property
    def last_name(self) -> Optional[str]:
        return self['last_name']

    @property
    def username(self) -> Optional[str]:
        return self['username']

    @property
    def phone(self) -> Optional[str]:
        return self['phone']

    @property
    def photo(self) -> Optional[aliases.AnyUserProfilePhoto]:
        return build_object(self['photo'])

    @property
    def status(self) -> Optional[aliases.AnyUserStatus]:
        return build_object(self['status'])

    @property
    def bot_info_version(self) -> Optional[int]:
        return self['bot_info_version']

    @property
    def restriction_reason(self) -> Optional[list[aliases.AnyRestrictionReason]]:
        return build_object(self['restriction_reason'])

    @property
    def bot_inline_placeholder(self) -> Optional[str]:
        return self['bot_inline_placeholder']

    @property
    def lang_code(self) -> Optional[str]:
        return self['lang_code']

    @property
    def emoji_status(self) -> Optional[aliases.AnyEmojiStatus]:
        return build_object(self['emoji_status'])

    @property
    def usernames(self) -> Optional[list[aliases.AnyUsername]]:
        return build_object(self['usernames'])

    @property
    def stories_max_id(self) -> Optional[aliases.AnyRecentStory]:
        return build_object(self['stories_max_id'])

    @property
    def color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['color'])

    @property
    def profile_color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['profile_color'])

    @property
    def bot_active_users(self) -> Optional[int]:
        return self['bot_active_users']

    @property
    def bot_verification_icon(self) -> Optional[int]:
        return self['bot_verification_icon']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']


class UserProfilePhotoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='userProfilePhotoEmpty'):
        dict.__init__(self, _=_)


class UserProfilePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo_id: int, dc_id: int, has_video: Optional[bool] = ..., personal: Optional[bool] = ..., stripped_thumb: Optional[bytes] = ...): ...

    def __init__(self, photo_id, dc_id, _='userProfilePhoto', **kwargs):
        kwargs['photo_id'] = photo_id
        kwargs['dc_id'] = dc_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_video(self) -> Optional[bool]:
        return self['has_video']

    @property
    def personal(self) -> Optional[bool]:
        return self['personal']

    @property
    def photo_id(self) -> int:
        return self['photo_id']

    @property
    def stripped_thumb(self) -> Optional[bytes]:
        return self['stripped_thumb']

    @property
    def dc_id(self) -> int:
        return self['dc_id']


class UserStatusEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='userStatusEmpty'):
        dict.__init__(self, _=_)


class UserStatusOnline(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int): ...

    def __init__(self, expires, _='userStatusOnline', **kwargs):
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']


class UserStatusOffline(dict):
    __slots__ = ()

    @overload
    def __init__(self, was_online: int): ...

    def __init__(self, was_online, _='userStatusOffline', **kwargs):
        kwargs['was_online'] = was_online
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def was_online(self) -> int:
        return self['was_online']


class UserStatusRecently(dict):
    __slots__ = ()

    @overload
    def __init__(self, by_me: Optional[bool] = ...): ...

    def __init__(self, _='userStatusRecently', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def by_me(self) -> Optional[bool]:
        return self['by_me']


class UserStatusLastWeek(dict):
    __slots__ = ()

    @overload
    def __init__(self, by_me: Optional[bool] = ...): ...

    def __init__(self, _='userStatusLastWeek', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def by_me(self) -> Optional[bool]:
        return self['by_me']


class UserStatusLastMonth(dict):
    __slots__ = ()

    @overload
    def __init__(self, by_me: Optional[bool] = ...): ...

    def __init__(self, _='userStatusLastMonth', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def by_me(self) -> Optional[bool]:
        return self['by_me']


class ChatEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='chatEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class Chat(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: str, photo: aliases.AnyChatPhoto, participants_count: int, date: int, version: int, creator: Optional[bool] = ..., left: Optional[bool] = ..., deactivated: Optional[bool] = ..., call_active: Optional[bool] = ..., call_not_empty: Optional[bool] = ..., noforwards: Optional[bool] = ..., migrated_to: Optional[aliases.AnyInputChannel] = ..., admin_rights: Optional[aliases.AnyChatAdminRights] = ..., default_banned_rights: Optional[aliases.AnyChatBannedRights] = ...): ...

    def __init__(self, id, title, photo, participants_count, date, version, _='chat', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['photo'] = photo
        kwargs['participants_count'] = participants_count
        kwargs['date'] = date
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def left(self) -> Optional[bool]:
        return self['left']

    @property
    def deactivated(self) -> Optional[bool]:
        return self['deactivated']

    @property
    def call_active(self) -> Optional[bool]:
        return self['call_active']

    @property
    def call_not_empty(self) -> Optional[bool]:
        return self['call_not_empty']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def photo(self) -> aliases.AnyChatPhoto:
        return build_object(self['photo'])

    @property
    def participants_count(self) -> int:
        return self['participants_count']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def version(self) -> int:
        return self['version']

    @property
    def migrated_to(self) -> Optional[aliases.AnyInputChannel]:
        return build_object(self['migrated_to'])

    @property
    def admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['admin_rights'])

    @property
    def default_banned_rights(self) -> Optional[aliases.AnyChatBannedRights]:
        return build_object(self['default_banned_rights'])


class ChatForbidden(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: str): ...

    def __init__(self, id, title, _='chatForbidden', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']


class Channel(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: str, photo: aliases.AnyChatPhoto, date: int, creator: Optional[bool] = ..., left: Optional[bool] = ..., broadcast: Optional[bool] = ..., verified: Optional[bool] = ..., megagroup: Optional[bool] = ..., restricted: Optional[bool] = ..., signatures: Optional[bool] = ..., min: Optional[bool] = ..., scam: Optional[bool] = ..., has_link: Optional[bool] = ..., has_geo: Optional[bool] = ..., slowmode_enabled: Optional[bool] = ..., call_active: Optional[bool] = ..., call_not_empty: Optional[bool] = ..., fake: Optional[bool] = ..., gigagroup: Optional[bool] = ..., noforwards: Optional[bool] = ..., join_to_send: Optional[bool] = ..., join_request: Optional[bool] = ..., forum: Optional[bool] = ..., stories_hidden: Optional[bool] = ..., stories_hidden_min: Optional[bool] = ..., stories_unavailable: Optional[bool] = ..., signature_profiles: Optional[bool] = ..., autotranslation: Optional[bool] = ..., broadcast_messages_allowed: Optional[bool] = ..., monoforum: Optional[bool] = ..., forum_tabs: Optional[bool] = ..., access_hash: Optional[int] = ..., username: Optional[str] = ..., restriction_reason: Optional[list[aliases.AnyRestrictionReason]] = ..., admin_rights: Optional[aliases.AnyChatAdminRights] = ..., banned_rights: Optional[aliases.AnyChatBannedRights] = ..., default_banned_rights: Optional[aliases.AnyChatBannedRights] = ..., participants_count: Optional[int] = ..., usernames: Optional[list[aliases.AnyUsername]] = ..., stories_max_id: Optional[aliases.AnyRecentStory] = ..., color: Optional[aliases.AnyPeerColor] = ..., profile_color: Optional[aliases.AnyPeerColor] = ..., emoji_status: Optional[aliases.AnyEmojiStatus] = ..., level: Optional[int] = ..., subscription_until_date: Optional[int] = ..., bot_verification_icon: Optional[int] = ..., send_paid_messages_stars: Optional[int] = ..., linked_monoforum_id: Optional[int] = ...): ...

    def __init__(self, id, title, photo, date, _='channel', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['photo'] = photo
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def left(self) -> Optional[bool]:
        return self['left']

    @property
    def broadcast(self) -> Optional[bool]:
        return self['broadcast']

    @property
    def verified(self) -> Optional[bool]:
        return self['verified']

    @property
    def megagroup(self) -> Optional[bool]:
        return self['megagroup']

    @property
    def restricted(self) -> Optional[bool]:
        return self['restricted']

    @property
    def signatures(self) -> Optional[bool]:
        return self['signatures']

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def scam(self) -> Optional[bool]:
        return self['scam']

    @property
    def has_link(self) -> Optional[bool]:
        return self['has_link']

    @property
    def has_geo(self) -> Optional[bool]:
        return self['has_geo']

    @property
    def slowmode_enabled(self) -> Optional[bool]:
        return self['slowmode_enabled']

    @property
    def call_active(self) -> Optional[bool]:
        return self['call_active']

    @property
    def call_not_empty(self) -> Optional[bool]:
        return self['call_not_empty']

    @property
    def fake(self) -> Optional[bool]:
        return self['fake']

    @property
    def gigagroup(self) -> Optional[bool]:
        return self['gigagroup']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def join_to_send(self) -> Optional[bool]:
        return self['join_to_send']

    @property
    def join_request(self) -> Optional[bool]:
        return self['join_request']

    @property
    def forum(self) -> Optional[bool]:
        return self['forum']

    @property
    def stories_hidden(self) -> Optional[bool]:
        return self['stories_hidden']

    @property
    def stories_hidden_min(self) -> Optional[bool]:
        return self['stories_hidden_min']

    @property
    def stories_unavailable(self) -> Optional[bool]:
        return self['stories_unavailable']

    @property
    def signature_profiles(self) -> Optional[bool]:
        return self['signature_profiles']

    @property
    def autotranslation(self) -> Optional[bool]:
        return self['autotranslation']

    @property
    def broadcast_messages_allowed(self) -> Optional[bool]:
        return self['broadcast_messages_allowed']

    @property
    def monoforum(self) -> Optional[bool]:
        return self['monoforum']

    @property
    def forum_tabs(self) -> Optional[bool]:
        return self['forum_tabs']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> Optional[int]:
        return self['access_hash']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def username(self) -> Optional[str]:
        return self['username']

    @property
    def photo(self) -> aliases.AnyChatPhoto:
        return build_object(self['photo'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def restriction_reason(self) -> Optional[list[aliases.AnyRestrictionReason]]:
        return build_object(self['restriction_reason'])

    @property
    def admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['admin_rights'])

    @property
    def banned_rights(self) -> Optional[aliases.AnyChatBannedRights]:
        return build_object(self['banned_rights'])

    @property
    def default_banned_rights(self) -> Optional[aliases.AnyChatBannedRights]:
        return build_object(self['default_banned_rights'])

    @property
    def participants_count(self) -> Optional[int]:
        return self['participants_count']

    @property
    def usernames(self) -> Optional[list[aliases.AnyUsername]]:
        return build_object(self['usernames'])

    @property
    def stories_max_id(self) -> Optional[aliases.AnyRecentStory]:
        return build_object(self['stories_max_id'])

    @property
    def color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['color'])

    @property
    def profile_color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['profile_color'])

    @property
    def emoji_status(self) -> Optional[aliases.AnyEmojiStatus]:
        return build_object(self['emoji_status'])

    @property
    def level(self) -> Optional[int]:
        return self['level']

    @property
    def subscription_until_date(self) -> Optional[int]:
        return self['subscription_until_date']

    @property
    def bot_verification_icon(self) -> Optional[int]:
        return self['bot_verification_icon']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']

    @property
    def linked_monoforum_id(self) -> Optional[int]:
        return self['linked_monoforum_id']


class ChannelForbidden(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, title: str, broadcast: Optional[bool] = ..., megagroup: Optional[bool] = ..., monoforum: Optional[bool] = ..., until_date: Optional[int] = ...): ...

    def __init__(self, id, access_hash, title, _='channelForbidden', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcast(self) -> Optional[bool]:
        return self['broadcast']

    @property
    def megagroup(self) -> Optional[bool]:
        return self['megagroup']

    @property
    def monoforum(self) -> Optional[bool]:
        return self['monoforum']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def until_date(self) -> Optional[int]:
        return self['until_date']


class ChatFull(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, about: str, participants: aliases.AnyChatParticipants, notify_settings: aliases.AnyPeerNotifySettings, can_set_username: Optional[bool] = ..., has_scheduled: Optional[bool] = ..., translations_disabled: Optional[bool] = ..., chat_photo: Optional[aliases.AnyPhoto] = ..., exported_invite: Optional[aliases.AnyExportedChatInvite] = ..., bot_info: Optional[list[aliases.AnyBotInfo]] = ..., pinned_msg_id: Optional[int] = ..., folder_id: Optional[int] = ..., call: Optional[aliases.AnyInputGroupCall] = ..., ttl_period: Optional[int] = ..., groupcall_default_join_as: Optional[aliases.AnyPeer] = ..., theme_emoticon: Optional[str] = ..., requests_pending: Optional[int] = ..., recent_requesters: Optional[list[int]] = ..., available_reactions: Optional[aliases.AnyChatReactions] = ..., reactions_limit: Optional[int] = ...): ...

    def __init__(self, id, about, participants, notify_settings, _='chatFull', **kwargs):
        kwargs['id'] = id
        kwargs['about'] = about
        kwargs['participants'] = participants
        kwargs['notify_settings'] = notify_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_set_username(self) -> Optional[bool]:
        return self['can_set_username']

    @property
    def has_scheduled(self) -> Optional[bool]:
        return self['has_scheduled']

    @property
    def translations_disabled(self) -> Optional[bool]:
        return self['translations_disabled']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def about(self) -> str:
        return self['about']

    @property
    def participants(self) -> aliases.AnyChatParticipants:
        return build_object(self['participants'])

    @property
    def chat_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['chat_photo'])

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])

    @property
    def exported_invite(self) -> Optional[aliases.AnyExportedChatInvite]:
        return build_object(self['exported_invite'])

    @property
    def bot_info(self) -> Optional[list[aliases.AnyBotInfo]]:
        return build_object(self['bot_info'])

    @property
    def pinned_msg_id(self) -> Optional[int]:
        return self['pinned_msg_id']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def call(self) -> Optional[aliases.AnyInputGroupCall]:
        return build_object(self['call'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']

    @property
    def groupcall_default_join_as(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['groupcall_default_join_as'])

    @property
    def theme_emoticon(self) -> Optional[str]:
        return self['theme_emoticon']

    @property
    def requests_pending(self) -> Optional[int]:
        return self['requests_pending']

    @property
    def recent_requesters(self) -> Optional[list[int]]:
        return self['recent_requesters']

    @property
    def available_reactions(self) -> Optional[aliases.AnyChatReactions]:
        return build_object(self['available_reactions'])

    @property
    def reactions_limit(self) -> Optional[int]:
        return self['reactions_limit']


class ChannelFull(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, about: str, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, chat_photo: aliases.AnyPhoto, notify_settings: aliases.AnyPeerNotifySettings, bot_info: list[aliases.AnyBotInfo], pts: int, can_view_participants: Optional[bool] = ..., can_set_username: Optional[bool] = ..., can_set_stickers: Optional[bool] = ..., hidden_prehistory: Optional[bool] = ..., can_set_location: Optional[bool] = ..., has_scheduled: Optional[bool] = ..., can_view_stats: Optional[bool] = ..., blocked: Optional[bool] = ..., can_delete_channel: Optional[bool] = ..., antispam: Optional[bool] = ..., participants_hidden: Optional[bool] = ..., translations_disabled: Optional[bool] = ..., stories_pinned_available: Optional[bool] = ..., view_forum_as_messages: Optional[bool] = ..., restricted_sponsored: Optional[bool] = ..., can_view_revenue: Optional[bool] = ..., paid_media_allowed: Optional[bool] = ..., can_view_stars_revenue: Optional[bool] = ..., paid_reactions_available: Optional[bool] = ..., stargifts_available: Optional[bool] = ..., paid_messages_available: Optional[bool] = ..., participants_count: Optional[int] = ..., admins_count: Optional[int] = ..., kicked_count: Optional[int] = ..., banned_count: Optional[int] = ..., online_count: Optional[int] = ..., exported_invite: Optional[aliases.AnyExportedChatInvite] = ..., migrated_from_chat_id: Optional[int] = ..., migrated_from_max_id: Optional[int] = ..., pinned_msg_id: Optional[int] = ..., stickerset: Optional[aliases.AnyStickerSet] = ..., available_min_id: Optional[int] = ..., folder_id: Optional[int] = ..., linked_chat_id: Optional[int] = ..., location: Optional[aliases.AnyChannelLocation] = ..., slowmode_seconds: Optional[int] = ..., slowmode_next_send_date: Optional[int] = ..., stats_dc: Optional[int] = ..., call: Optional[aliases.AnyInputGroupCall] = ..., ttl_period: Optional[int] = ..., pending_suggestions: Optional[list[str]] = ..., groupcall_default_join_as: Optional[aliases.AnyPeer] = ..., theme_emoticon: Optional[str] = ..., requests_pending: Optional[int] = ..., recent_requesters: Optional[list[int]] = ..., default_send_as: Optional[aliases.AnyPeer] = ..., available_reactions: Optional[aliases.AnyChatReactions] = ..., reactions_limit: Optional[int] = ..., stories: Optional[aliases.AnyPeerStories] = ..., wallpaper: Optional[aliases.AnyWallPaper] = ..., boosts_applied: Optional[int] = ..., boosts_unrestrict: Optional[int] = ..., emojiset: Optional[aliases.AnyStickerSet] = ..., bot_verification: Optional[aliases.AnyBotVerification] = ..., stargifts_count: Optional[int] = ..., send_paid_messages_stars: Optional[int] = ..., main_tab: Optional[aliases.AnyProfileTab] = ...): ...

    def __init__(self, id, about, read_inbox_max_id, read_outbox_max_id, unread_count, chat_photo, notify_settings, bot_info, pts, _='channelFull', **kwargs):
        kwargs['id'] = id
        kwargs['about'] = about
        kwargs['read_inbox_max_id'] = read_inbox_max_id
        kwargs['read_outbox_max_id'] = read_outbox_max_id
        kwargs['unread_count'] = unread_count
        kwargs['chat_photo'] = chat_photo
        kwargs['notify_settings'] = notify_settings
        kwargs['bot_info'] = bot_info
        kwargs['pts'] = pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_view_participants(self) -> Optional[bool]:
        return self['can_view_participants']

    @property
    def can_set_username(self) -> Optional[bool]:
        return self['can_set_username']

    @property
    def can_set_stickers(self) -> Optional[bool]:
        return self['can_set_stickers']

    @property
    def hidden_prehistory(self) -> Optional[bool]:
        return self['hidden_prehistory']

    @property
    def can_set_location(self) -> Optional[bool]:
        return self['can_set_location']

    @property
    def has_scheduled(self) -> Optional[bool]:
        return self['has_scheduled']

    @property
    def can_view_stats(self) -> Optional[bool]:
        return self['can_view_stats']

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def can_delete_channel(self) -> Optional[bool]:
        return self['can_delete_channel']

    @property
    def antispam(self) -> Optional[bool]:
        return self['antispam']

    @property
    def participants_hidden(self) -> Optional[bool]:
        return self['participants_hidden']

    @property
    def translations_disabled(self) -> Optional[bool]:
        return self['translations_disabled']

    @property
    def stories_pinned_available(self) -> Optional[bool]:
        return self['stories_pinned_available']

    @property
    def view_forum_as_messages(self) -> Optional[bool]:
        return self['view_forum_as_messages']

    @property
    def restricted_sponsored(self) -> Optional[bool]:
        return self['restricted_sponsored']

    @property
    def can_view_revenue(self) -> Optional[bool]:
        return self['can_view_revenue']

    @property
    def paid_media_allowed(self) -> Optional[bool]:
        return self['paid_media_allowed']

    @property
    def can_view_stars_revenue(self) -> Optional[bool]:
        return self['can_view_stars_revenue']

    @property
    def paid_reactions_available(self) -> Optional[bool]:
        return self['paid_reactions_available']

    @property
    def stargifts_available(self) -> Optional[bool]:
        return self['stargifts_available']

    @property
    def paid_messages_available(self) -> Optional[bool]:
        return self['paid_messages_available']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def about(self) -> str:
        return self['about']

    @property
    def participants_count(self) -> Optional[int]:
        return self['participants_count']

    @property
    def admins_count(self) -> Optional[int]:
        return self['admins_count']

    @property
    def kicked_count(self) -> Optional[int]:
        return self['kicked_count']

    @property
    def banned_count(self) -> Optional[int]:
        return self['banned_count']

    @property
    def online_count(self) -> Optional[int]:
        return self['online_count']

    @property
    def read_inbox_max_id(self) -> int:
        return self['read_inbox_max_id']

    @property
    def read_outbox_max_id(self) -> int:
        return self['read_outbox_max_id']

    @property
    def unread_count(self) -> int:
        return self['unread_count']

    @property
    def chat_photo(self) -> aliases.AnyPhoto:
        return build_object(self['chat_photo'])

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])

    @property
    def exported_invite(self) -> Optional[aliases.AnyExportedChatInvite]:
        return build_object(self['exported_invite'])

    @property
    def bot_info(self) -> list[aliases.AnyBotInfo]:
        return build_object(self['bot_info'])

    @property
    def migrated_from_chat_id(self) -> Optional[int]:
        return self['migrated_from_chat_id']

    @property
    def migrated_from_max_id(self) -> Optional[int]:
        return self['migrated_from_max_id']

    @property
    def pinned_msg_id(self) -> Optional[int]:
        return self['pinned_msg_id']

    @property
    def stickerset(self) -> Optional[aliases.AnyStickerSet]:
        return build_object(self['stickerset'])

    @property
    def available_min_id(self) -> Optional[int]:
        return self['available_min_id']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def linked_chat_id(self) -> Optional[int]:
        return self['linked_chat_id']

    @property
    def location(self) -> Optional[aliases.AnyChannelLocation]:
        return build_object(self['location'])

    @property
    def slowmode_seconds(self) -> Optional[int]:
        return self['slowmode_seconds']

    @property
    def slowmode_next_send_date(self) -> Optional[int]:
        return self['slowmode_next_send_date']

    @property
    def stats_dc(self) -> Optional[int]:
        return self['stats_dc']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def call(self) -> Optional[aliases.AnyInputGroupCall]:
        return build_object(self['call'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']

    @property
    def pending_suggestions(self) -> Optional[list[str]]:
        return self['pending_suggestions']

    @property
    def groupcall_default_join_as(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['groupcall_default_join_as'])

    @property
    def theme_emoticon(self) -> Optional[str]:
        return self['theme_emoticon']

    @property
    def requests_pending(self) -> Optional[int]:
        return self['requests_pending']

    @property
    def recent_requesters(self) -> Optional[list[int]]:
        return self['recent_requesters']

    @property
    def default_send_as(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['default_send_as'])

    @property
    def available_reactions(self) -> Optional[aliases.AnyChatReactions]:
        return build_object(self['available_reactions'])

    @property
    def reactions_limit(self) -> Optional[int]:
        return self['reactions_limit']

    @property
    def stories(self) -> Optional[aliases.AnyPeerStories]:
        return build_object(self['stories'])

    @property
    def wallpaper(self) -> Optional[aliases.AnyWallPaper]:
        return build_object(self['wallpaper'])

    @property
    def boosts_applied(self) -> Optional[int]:
        return self['boosts_applied']

    @property
    def boosts_unrestrict(self) -> Optional[int]:
        return self['boosts_unrestrict']

    @property
    def emojiset(self) -> Optional[aliases.AnyStickerSet]:
        return build_object(self['emojiset'])

    @property
    def bot_verification(self) -> Optional[aliases.AnyBotVerification]:
        return build_object(self['bot_verification'])

    @property
    def stargifts_count(self) -> Optional[int]:
        return self['stargifts_count']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']

    @property
    def main_tab(self) -> Optional[aliases.AnyProfileTab]:
        return build_object(self['main_tab'])


class ChatParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, inviter_id: int, date: int, rank: Optional[str] = ...): ...

    def __init__(self, user_id, inviter_id, date, _='chatParticipant', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['inviter_id'] = inviter_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def inviter_id(self) -> int:
        return self['inviter_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChatParticipantCreator(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, rank: Optional[str] = ...): ...

    def __init__(self, user_id, _='chatParticipantCreator', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChatParticipantAdmin(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, inviter_id: int, date: int, rank: Optional[str] = ...): ...

    def __init__(self, user_id, inviter_id, date, _='chatParticipantAdmin', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['inviter_id'] = inviter_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def inviter_id(self) -> int:
        return self['inviter_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChatParticipantsForbidden(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, self_participant: Optional[aliases.AnyChatParticipant] = ...): ...

    def __init__(self, chat_id, _='chatParticipantsForbidden', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def self_participant(self) -> Optional[aliases.AnyChatParticipant]:
        return build_object(self['self_participant'])


class ChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, participants: list[aliases.AnyChatParticipant], version: int): ...

    def __init__(self, chat_id, participants, version, _='chatParticipants', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['participants'] = participants
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def participants(self) -> list[aliases.AnyChatParticipant]:
        return build_object(self['participants'])

    @property
    def version(self) -> int:
        return self['version']


class ChatPhotoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='chatPhotoEmpty'):
        dict.__init__(self, _=_)


class ChatPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo_id: int, dc_id: int, has_video: Optional[bool] = ..., stripped_thumb: Optional[bytes] = ...): ...

    def __init__(self, photo_id, dc_id, _='chatPhoto', **kwargs):
        kwargs['photo_id'] = photo_id
        kwargs['dc_id'] = dc_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_video(self) -> Optional[bool]:
        return self['has_video']

    @property
    def photo_id(self) -> int:
        return self['photo_id']

    @property
    def stripped_thumb(self) -> Optional[bytes]:
        return self['stripped_thumb']

    @property
    def dc_id(self) -> int:
        return self['dc_id']


class MessageEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, id, _='messageEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer_id'])


class Message(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, peer_id: aliases.AnyPeer, date: int, message: str, out: Optional[bool] = ..., mentioned: Optional[bool] = ..., media_unread: Optional[bool] = ..., silent: Optional[bool] = ..., post: Optional[bool] = ..., from_scheduled: Optional[bool] = ..., legacy: Optional[bool] = ..., edit_hide: Optional[bool] = ..., pinned: Optional[bool] = ..., noforwards: Optional[bool] = ..., invert_media: Optional[bool] = ..., offline: Optional[bool] = ..., video_processing_pending: Optional[bool] = ..., paid_suggested_post_stars: Optional[bool] = ..., paid_suggested_post_ton: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., from_boosts_applied: Optional[int] = ..., from_rank: Optional[str] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ..., fwd_from: Optional[aliases.AnyMessageFwdHeader] = ..., via_bot_id: Optional[int] = ..., via_business_bot_id: Optional[int] = ..., reply_to: Optional[aliases.AnyMessageReplyHeader] = ..., media: Optional[aliases.AnyMessageMedia] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., views: Optional[int] = ..., forwards: Optional[int] = ..., replies: Optional[aliases.AnyMessageReplies] = ..., edit_date: Optional[int] = ..., post_author: Optional[str] = ..., grouped_id: Optional[int] = ..., reactions: Optional[aliases.AnyMessageReactions] = ..., restriction_reason: Optional[list[aliases.AnyRestrictionReason]] = ..., ttl_period: Optional[int] = ..., quick_reply_shortcut_id: Optional[int] = ..., effect: Optional[int] = ..., factcheck: Optional[aliases.AnyFactCheck] = ..., report_delivery_until_date: Optional[int] = ..., paid_message_stars: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ..., schedule_repeat_period: Optional[int] = ..., summary_from_language: Optional[str] = ...): ...

    def __init__(self, id, peer_id, date, message, _='message', **kwargs):
        kwargs['id'] = id
        kwargs['peer_id'] = peer_id
        kwargs['date'] = date
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def mentioned(self) -> Optional[bool]:
        return self['mentioned']

    @property
    def media_unread(self) -> Optional[bool]:
        return self['media_unread']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def post(self) -> Optional[bool]:
        return self['post']

    @property
    def from_scheduled(self) -> Optional[bool]:
        return self['from_scheduled']

    @property
    def legacy(self) -> Optional[bool]:
        return self['legacy']

    @property
    def edit_hide(self) -> Optional[bool]:
        return self['edit_hide']

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def offline(self) -> Optional[bool]:
        return self['offline']

    @property
    def video_processing_pending(self) -> Optional[bool]:
        return self['video_processing_pending']

    @property
    def paid_suggested_post_stars(self) -> Optional[bool]:
        return self['paid_suggested_post_stars']

    @property
    def paid_suggested_post_ton(self) -> Optional[bool]:
        return self['paid_suggested_post_ton']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def from_boosts_applied(self) -> Optional[int]:
        return self['from_boosts_applied']

    @property
    def from_rank(self) -> Optional[str]:
        return self['from_rank']

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def fwd_from(self) -> Optional[aliases.AnyMessageFwdHeader]:
        return build_object(self['fwd_from'])

    @property
    def via_bot_id(self) -> Optional[int]:
        return self['via_bot_id']

    @property
    def via_business_bot_id(self) -> Optional[int]:
        return self['via_business_bot_id']

    @property
    def reply_to(self) -> Optional[aliases.AnyMessageReplyHeader]:
        return build_object(self['reply_to'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def media(self) -> Optional[aliases.AnyMessageMedia]:
        return build_object(self['media'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def views(self) -> Optional[int]:
        return self['views']

    @property
    def forwards(self) -> Optional[int]:
        return self['forwards']

    @property
    def replies(self) -> Optional[aliases.AnyMessageReplies]:
        return build_object(self['replies'])

    @property
    def edit_date(self) -> Optional[int]:
        return self['edit_date']

    @property
    def post_author(self) -> Optional[str]:
        return self['post_author']

    @property
    def grouped_id(self) -> Optional[int]:
        return self['grouped_id']

    @property
    def reactions(self) -> Optional[aliases.AnyMessageReactions]:
        return build_object(self['reactions'])

    @property
    def restriction_reason(self) -> Optional[list[aliases.AnyRestrictionReason]]:
        return build_object(self['restriction_reason'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']

    @property
    def quick_reply_shortcut_id(self) -> Optional[int]:
        return self['quick_reply_shortcut_id']

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def factcheck(self) -> Optional[aliases.AnyFactCheck]:
        return build_object(self['factcheck'])

    @property
    def report_delivery_until_date(self) -> Optional[int]:
        return self['report_delivery_until_date']

    @property
    def paid_message_stars(self) -> Optional[int]:
        return self['paid_message_stars']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])

    @property
    def schedule_repeat_period(self) -> Optional[int]:
        return self['schedule_repeat_period']

    @property
    def summary_from_language(self) -> Optional[str]:
        return self['summary_from_language']


class MessageService(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, peer_id: aliases.AnyPeer, date: int, action: aliases.AnyMessageAction, out: Optional[bool] = ..., mentioned: Optional[bool] = ..., media_unread: Optional[bool] = ..., reactions_are_possible: Optional[bool] = ..., silent: Optional[bool] = ..., post: Optional[bool] = ..., legacy: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ..., reply_to: Optional[aliases.AnyMessageReplyHeader] = ..., reactions: Optional[aliases.AnyMessageReactions] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, id, peer_id, date, action, _='messageService', **kwargs):
        kwargs['id'] = id
        kwargs['peer_id'] = peer_id
        kwargs['date'] = date
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def mentioned(self) -> Optional[bool]:
        return self['mentioned']

    @property
    def media_unread(self) -> Optional[bool]:
        return self['media_unread']

    @property
    def reactions_are_possible(self) -> Optional[bool]:
        return self['reactions_are_possible']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def post(self) -> Optional[bool]:
        return self['post']

    @property
    def legacy(self) -> Optional[bool]:
        return self['legacy']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def reply_to(self) -> Optional[aliases.AnyMessageReplyHeader]:
        return build_object(self['reply_to'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def action(self) -> aliases.AnyMessageAction:
        return build_object(self['action'])

    @property
    def reactions(self) -> Optional[aliases.AnyMessageReactions]:
        return build_object(self['reactions'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class MessageMediaEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageMediaEmpty'):
        dict.__init__(self, _=_)


class MessageMediaPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, spoiler: Optional[bool] = ..., photo: Optional[aliases.AnyPhoto] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, _='messageMediaPhoto', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class MessageMediaGeo(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint): ...

    def __init__(self, geo, _='messageMediaGeo', **kwargs):
        kwargs['geo'] = geo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])


class MessageMediaContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, first_name: str, last_name: str, vcard: str, user_id: int): ...

    def __init__(self, phone_number, first_name, last_name, vcard, user_id, _='messageMediaContact', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['vcard'] = vcard
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def vcard(self) -> str:
        return self['vcard']

    @property
    def user_id(self) -> int:
        return self['user_id']


class MessageMediaUnsupported(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageMediaUnsupported'):
        dict.__init__(self, _=_)


class MessageMediaDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, nopremium: Optional[bool] = ..., spoiler: Optional[bool] = ..., video: Optional[bool] = ..., round: Optional[bool] = ..., voice: Optional[bool] = ..., document: Optional[aliases.AnyDocument] = ..., alt_documents: Optional[list[aliases.AnyDocument]] = ..., video_cover: Optional[aliases.AnyPhoto] = ..., video_timestamp: Optional[int] = ..., ttl_seconds: Optional[int] = ...): ...

    def __init__(self, _='messageMediaDocument', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def nopremium(self) -> Optional[bool]:
        return self['nopremium']

    @property
    def spoiler(self) -> Optional[bool]:
        return self['spoiler']

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def round(self) -> Optional[bool]:
        return self['round']

    @property
    def voice(self) -> Optional[bool]:
        return self['voice']

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def alt_documents(self) -> Optional[list[aliases.AnyDocument]]:
        return build_object(self['alt_documents'])

    @property
    def video_cover(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['video_cover'])

    @property
    def video_timestamp(self) -> Optional[int]:
        return self['video_timestamp']

    @property
    def ttl_seconds(self) -> Optional[int]:
        return self['ttl_seconds']


class MessageMediaWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, webpage: aliases.AnyWebPage, force_large_media: Optional[bool] = ..., force_small_media: Optional[bool] = ..., manual: Optional[bool] = ..., safe: Optional[bool] = ...): ...

    def __init__(self, webpage, _='messageMediaWebPage', **kwargs):
        kwargs['webpage'] = webpage
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def force_large_media(self) -> Optional[bool]:
        return self['force_large_media']

    @property
    def force_small_media(self) -> Optional[bool]:
        return self['force_small_media']

    @property
    def manual(self) -> Optional[bool]:
        return self['manual']

    @property
    def safe(self) -> Optional[bool]:
        return self['safe']

    @property
    def webpage(self) -> aliases.AnyWebPage:
        return build_object(self['webpage'])


class MessageMediaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint, title: str, address: str, provider: str, venue_id: str, venue_type: str): ...

    def __init__(self, geo, title, address, provider, venue_id, venue_type, _='messageMediaVenue', **kwargs):
        kwargs['geo'] = geo
        kwargs['title'] = title
        kwargs['address'] = address
        kwargs['provider'] = provider
        kwargs['venue_id'] = venue_id
        kwargs['venue_type'] = venue_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def address(self) -> str:
        return self['address']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def venue_id(self) -> str:
        return self['venue_id']

    @property
    def venue_type(self) -> str:
        return self['venue_type']


class MessageMediaGame(dict):
    __slots__ = ()

    @overload
    def __init__(self, game: aliases.AnyGame): ...

    def __init__(self, game, _='messageMediaGame', **kwargs):
        kwargs['game'] = game
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def game(self) -> aliases.AnyGame:
        return build_object(self['game'])


class MessageMediaInvoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, currency: str, total_amount: int, start_param: str, shipping_address_requested: Optional[bool] = ..., test: Optional[bool] = ..., photo: Optional[aliases.AnyWebDocument] = ..., receipt_msg_id: Optional[int] = ..., extended_media: Optional[aliases.AnyMessageExtendedMedia] = ...): ...

    def __init__(self, title, description, currency, total_amount, start_param, _='messageMediaInvoice', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['start_param'] = start_param
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shipping_address_requested(self) -> Optional[bool]:
        return self['shipping_address_requested']

    @property
    def test(self) -> Optional[bool]:
        return self['test']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def receipt_msg_id(self) -> Optional[int]:
        return self['receipt_msg_id']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def start_param(self) -> str:
        return self['start_param']

    @property
    def extended_media(self) -> Optional[aliases.AnyMessageExtendedMedia]:
        return build_object(self['extended_media'])


class MessageMediaGeoLive(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint, period: int, heading: Optional[int] = ..., proximity_notification_radius: Optional[int] = ...): ...

    def __init__(self, geo, period, _='messageMediaGeoLive', **kwargs):
        kwargs['geo'] = geo
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def heading(self) -> Optional[int]:
        return self['heading']

    @property
    def period(self) -> int:
        return self['period']

    @property
    def proximity_notification_radius(self) -> Optional[int]:
        return self['proximity_notification_radius']


class MessageMediaPoll(dict):
    __slots__ = ()

    @overload
    def __init__(self, poll: aliases.AnyPoll, results: aliases.AnyPollResults): ...

    def __init__(self, poll, results, _='messageMediaPoll', **kwargs):
        kwargs['poll'] = poll
        kwargs['results'] = results
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def poll(self) -> aliases.AnyPoll:
        return build_object(self['poll'])

    @property
    def results(self) -> aliases.AnyPollResults:
        return build_object(self['results'])


class MessageMediaDice(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: int, emoticon: str, game_outcome: Optional[aliases.AnyMessagesEmojiGameOutcome] = ...): ...

    def __init__(self, value, emoticon, _='messageMediaDice', **kwargs):
        kwargs['value'] = value
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> int:
        return self['value']

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def game_outcome(self) -> Optional[aliases.AnyMessagesEmojiGameOutcome]:
        return build_object(self['game_outcome'])


class MessageMediaStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, id: int, via_mention: Optional[bool] = ..., story: Optional[aliases.AnyStoryItem] = ...): ...

    def __init__(self, peer, id, _='messageMediaStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_mention(self) -> Optional[bool]:
        return self['via_mention']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def story(self) -> Optional[aliases.AnyStoryItem]:
        return build_object(self['story'])


class MessageMediaGiveaway(dict):
    __slots__ = ()

    @overload
    def __init__(self, channels: list[int], quantity: int, until_date: int, only_new_subscribers: Optional[bool] = ..., winners_are_visible: Optional[bool] = ..., countries_iso2: Optional[list[str]] = ..., prize_description: Optional[str] = ..., months: Optional[int] = ..., stars: Optional[int] = ...): ...

    def __init__(self, channels, quantity, until_date, _='messageMediaGiveaway', **kwargs):
        kwargs['channels'] = channels
        kwargs['quantity'] = quantity
        kwargs['until_date'] = until_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def only_new_subscribers(self) -> Optional[bool]:
        return self['only_new_subscribers']

    @property
    def winners_are_visible(self) -> Optional[bool]:
        return self['winners_are_visible']

    @property
    def channels(self) -> list[int]:
        return self['channels']

    @property
    def countries_iso2(self) -> Optional[list[str]]:
        return self['countries_iso2']

    @property
    def prize_description(self) -> Optional[str]:
        return self['prize_description']

    @property
    def quantity(self) -> int:
        return self['quantity']

    @property
    def months(self) -> Optional[int]:
        return self['months']

    @property
    def stars(self) -> Optional[int]:
        return self['stars']

    @property
    def until_date(self) -> int:
        return self['until_date']


class MessageMediaGiveawayResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, launch_msg_id: int, winners_count: int, unclaimed_count: int, winners: list[int], until_date: int, only_new_subscribers: Optional[bool] = ..., refunded: Optional[bool] = ..., additional_peers_count: Optional[int] = ..., months: Optional[int] = ..., stars: Optional[int] = ..., prize_description: Optional[str] = ...): ...

    def __init__(self, channel_id, launch_msg_id, winners_count, unclaimed_count, winners, until_date, _='messageMediaGiveawayResults', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['launch_msg_id'] = launch_msg_id
        kwargs['winners_count'] = winners_count
        kwargs['unclaimed_count'] = unclaimed_count
        kwargs['winners'] = winners
        kwargs['until_date'] = until_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def only_new_subscribers(self) -> Optional[bool]:
        return self['only_new_subscribers']

    @property
    def refunded(self) -> Optional[bool]:
        return self['refunded']

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def additional_peers_count(self) -> Optional[int]:
        return self['additional_peers_count']

    @property
    def launch_msg_id(self) -> int:
        return self['launch_msg_id']

    @property
    def winners_count(self) -> int:
        return self['winners_count']

    @property
    def unclaimed_count(self) -> int:
        return self['unclaimed_count']

    @property
    def winners(self) -> list[int]:
        return self['winners']

    @property
    def months(self) -> Optional[int]:
        return self['months']

    @property
    def stars(self) -> Optional[int]:
        return self['stars']

    @property
    def prize_description(self) -> Optional[str]:
        return self['prize_description']

    @property
    def until_date(self) -> int:
        return self['until_date']


class MessageMediaPaidMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars_amount: int, extended_media: list[aliases.AnyMessageExtendedMedia]): ...

    def __init__(self, stars_amount, extended_media, _='messageMediaPaidMedia', **kwargs):
        kwargs['stars_amount'] = stars_amount
        kwargs['extended_media'] = extended_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars_amount(self) -> int:
        return self['stars_amount']

    @property
    def extended_media(self) -> list[aliases.AnyMessageExtendedMedia]:
        return build_object(self['extended_media'])


class MessageMediaToDo(dict):
    __slots__ = ()

    @overload
    def __init__(self, todo: aliases.AnyTodoList, completions: Optional[list[aliases.AnyTodoCompletion]] = ...): ...

    def __init__(self, todo, _='messageMediaToDo', **kwargs):
        kwargs['todo'] = todo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def todo(self) -> aliases.AnyTodoList:
        return build_object(self['todo'])

    @property
    def completions(self) -> Optional[list[aliases.AnyTodoCompletion]]:
        return build_object(self['completions'])


class MessageMediaVideoStream(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, rtmp_stream: Optional[bool] = ...): ...

    def __init__(self, call, _='messageMediaVideoStream', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def rtmp_stream(self) -> Optional[bool]:
        return self['rtmp_stream']

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class MessageActionEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionEmpty'):
        dict.__init__(self, _=_)


class MessageActionChatCreate(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, users: list[int]): ...

    def __init__(self, title, users, _='messageActionChatCreate', **kwargs):
        kwargs['title'] = title
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def users(self) -> list[int]:
        return self['users']


class MessageActionChatEditTitle(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str): ...

    def __init__(self, title, _='messageActionChatEditTitle', **kwargs):
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']


class MessageActionChatEditPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo: aliases.AnyPhoto): ...

    def __init__(self, photo, _='messageActionChatEditPhoto', **kwargs):
        kwargs['photo'] = photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])


class MessageActionChatDeletePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionChatDeletePhoto'):
        dict.__init__(self, _=_)


class MessageActionChatAddUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[int]): ...

    def __init__(self, users, _='messageActionChatAddUser', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[int]:
        return self['users']


class MessageActionChatDeleteUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int): ...

    def __init__(self, user_id, _='messageActionChatDeleteUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']


class MessageActionChatJoinedByLink(dict):
    __slots__ = ()

    @overload
    def __init__(self, inviter_id: int): ...

    def __init__(self, inviter_id, _='messageActionChatJoinedByLink', **kwargs):
        kwargs['inviter_id'] = inviter_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inviter_id(self) -> int:
        return self['inviter_id']


class MessageActionChannelCreate(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str): ...

    def __init__(self, title, _='messageActionChannelCreate', **kwargs):
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']


class MessageActionChatMigrateTo(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int): ...

    def __init__(self, channel_id, _='messageActionChatMigrateTo', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']


class MessageActionChannelMigrateFrom(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, chat_id: int): ...

    def __init__(self, title, chat_id, _='messageActionChannelMigrateFrom', **kwargs):
        kwargs['title'] = title
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class MessageActionPinMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionPinMessage'):
        dict.__init__(self, _=_)


class MessageActionHistoryClear(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionHistoryClear'):
        dict.__init__(self, _=_)


class MessageActionGameScore(dict):
    __slots__ = ()

    @overload
    def __init__(self, game_id: int, score: int): ...

    def __init__(self, game_id, score, _='messageActionGameScore', **kwargs):
        kwargs['game_id'] = game_id
        kwargs['score'] = score
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def game_id(self) -> int:
        return self['game_id']

    @property
    def score(self) -> int:
        return self['score']


class MessageActionPaymentSentMe(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, total_amount: int, payload: bytes, charge: aliases.AnyPaymentCharge, recurring_init: Optional[bool] = ..., recurring_used: Optional[bool] = ..., info: Optional[aliases.AnyPaymentRequestedInfo] = ..., shipping_option_id: Optional[str] = ..., subscription_until_date: Optional[int] = ...): ...

    def __init__(self, currency, total_amount, payload, charge, _='messageActionPaymentSentMe', **kwargs):
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['payload'] = payload
        kwargs['charge'] = charge
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def recurring_init(self) -> Optional[bool]:
        return self['recurring_init']

    @property
    def recurring_used(self) -> Optional[bool]:
        return self['recurring_used']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def payload(self) -> bytes:
        return self['payload']

    @property
    def info(self) -> Optional[aliases.AnyPaymentRequestedInfo]:
        return build_object(self['info'])

    @property
    def shipping_option_id(self) -> Optional[str]:
        return self['shipping_option_id']

    @property
    def charge(self) -> aliases.AnyPaymentCharge:
        return build_object(self['charge'])

    @property
    def subscription_until_date(self) -> Optional[int]:
        return self['subscription_until_date']


class MessageActionPaymentSent(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, total_amount: int, recurring_init: Optional[bool] = ..., recurring_used: Optional[bool] = ..., invoice_slug: Optional[str] = ..., subscription_until_date: Optional[int] = ...): ...

    def __init__(self, currency, total_amount, _='messageActionPaymentSent', **kwargs):
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def recurring_init(self) -> Optional[bool]:
        return self['recurring_init']

    @property
    def recurring_used(self) -> Optional[bool]:
        return self['recurring_used']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def invoice_slug(self) -> Optional[str]:
        return self['invoice_slug']

    @property
    def subscription_until_date(self) -> Optional[int]:
        return self['subscription_until_date']


class MessageActionPhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call_id: int, video: Optional[bool] = ..., reason: Optional[aliases.AnyPhoneCallDiscardReason] = ..., duration: Optional[int] = ...): ...

    def __init__(self, call_id, _='messageActionPhoneCall', **kwargs):
        kwargs['call_id'] = call_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def call_id(self) -> int:
        return self['call_id']

    @property
    def reason(self) -> Optional[aliases.AnyPhoneCallDiscardReason]:
        return build_object(self['reason'])

    @property
    def duration(self) -> Optional[int]:
        return self['duration']


class MessageActionScreenshotTaken(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionScreenshotTaken'):
        dict.__init__(self, _=_)


class MessageActionCustomAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str): ...

    def __init__(self, message, _='messageActionCustomAction', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> str:
        return self['message']


class MessageActionBotAllowed(dict):
    __slots__ = ()

    @overload
    def __init__(self, attach_menu: Optional[bool] = ..., from_request: Optional[bool] = ..., domain: Optional[str] = ..., app: Optional[aliases.AnyBotApp] = ...): ...

    def __init__(self, _='messageActionBotAllowed', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attach_menu(self) -> Optional[bool]:
        return self['attach_menu']

    @property
    def from_request(self) -> Optional[bool]:
        return self['from_request']

    @property
    def domain(self) -> Optional[str]:
        return self['domain']

    @property
    def app(self) -> Optional[aliases.AnyBotApp]:
        return build_object(self['app'])


class MessageActionSecureValuesSentMe(dict):
    __slots__ = ()

    @overload
    def __init__(self, values_: list[aliases.AnySecureValue], credentials: aliases.AnySecureCredentialsEncrypted): ...

    def __init__(self, values_, credentials, _='messageActionSecureValuesSentMe', **kwargs):
        kwargs['values'] = values_
        kwargs['credentials'] = credentials
        if 'values_' in kwargs:
            kwargs['values'] = kwargs.pop('values_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def values_(self) -> list[aliases.AnySecureValue]:
        return build_object(self['values'])

    @property
    def credentials(self) -> aliases.AnySecureCredentialsEncrypted:
        return build_object(self['credentials'])


class MessageActionSecureValuesSent(dict):
    __slots__ = ()

    @overload
    def __init__(self, types: list[aliases.AnySecureValueType]): ...

    def __init__(self, types, _='messageActionSecureValuesSent', **kwargs):
        kwargs['types'] = types
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def types(self) -> list[aliases.AnySecureValueType]:
        return build_object(self['types'])


class MessageActionContactSignUp(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionContactSignUp'):
        dict.__init__(self, _=_)


class MessageActionGeoProximityReached(dict):
    __slots__ = ()

    @overload
    def __init__(self, from_id: aliases.AnyPeer, to_id: aliases.AnyPeer, distance: int): ...

    def __init__(self, from_id, to_id, distance, _='messageActionGeoProximityReached', **kwargs):
        kwargs['from_id'] = from_id
        kwargs['to_id'] = to_id
        kwargs['distance'] = distance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def to_id(self) -> aliases.AnyPeer:
        return build_object(self['to_id'])

    @property
    def distance(self) -> int:
        return self['distance']


class MessageActionGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, duration: Optional[int] = ...): ...

    def __init__(self, call, _='messageActionGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def duration(self) -> Optional[int]:
        return self['duration']


class MessageActionInviteToGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, users: list[int]): ...

    def __init__(self, call, users, _='messageActionInviteToGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def users(self) -> list[int]:
        return self['users']


class MessageActionSetMessagesTTL(dict):
    __slots__ = ()

    @overload
    def __init__(self, period: int, auto_setting_from: Optional[int] = ...): ...

    def __init__(self, period, _='messageActionSetMessagesTTL', **kwargs):
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> int:
        return self['period']

    @property
    def auto_setting_from(self) -> Optional[int]:
        return self['auto_setting_from']


class MessageActionGroupCallScheduled(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, schedule_date: int): ...

    def __init__(self, call, schedule_date, _='messageActionGroupCallScheduled', **kwargs):
        kwargs['call'] = call
        kwargs['schedule_date'] = schedule_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def schedule_date(self) -> int:
        return self['schedule_date']


class MessageActionSetChatTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, theme: aliases.AnyChatTheme): ...

    def __init__(self, theme, _='messageActionSetChatTheme', **kwargs):
        kwargs['theme'] = theme
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def theme(self) -> aliases.AnyChatTheme:
        return build_object(self['theme'])


class MessageActionChatJoinedByRequest(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='messageActionChatJoinedByRequest'):
        dict.__init__(self, _=_)


class MessageActionWebViewDataSentMe(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, data: str): ...

    def __init__(self, text, data, _='messageActionWebViewDataSentMe', **kwargs):
        kwargs['text'] = text
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def data(self) -> str:
        return self['data']


class MessageActionWebViewDataSent(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str): ...

    def __init__(self, text, _='messageActionWebViewDataSent', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']


class MessageActionGiftPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, amount: int, days: int, crypto_currency: Optional[str] = ..., crypto_amount: Optional[int] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, currency, amount, days, _='messageActionGiftPremium', **kwargs):
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['days'] = days
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def days(self) -> int:
        return self['days']

    @property
    def crypto_currency(self) -> Optional[str]:
        return self['crypto_currency']

    @property
    def crypto_amount(self) -> Optional[int]:
        return self['crypto_amount']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class MessageActionTopicCreate(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, icon_color: int, title_missing: Optional[bool] = ..., icon_emoji_id: Optional[int] = ...): ...

    def __init__(self, title, icon_color, _='messageActionTopicCreate', **kwargs):
        kwargs['title'] = title
        kwargs['icon_color'] = icon_color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title_missing(self) -> Optional[bool]:
        return self['title_missing']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_color(self) -> int:
        return self['icon_color']

    @property
    def icon_emoji_id(self) -> Optional[int]:
        return self['icon_emoji_id']


class MessageActionTopicEdit(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: Optional[str] = ..., icon_emoji_id: Optional[int] = ..., closed: Optional[bool] = ..., hidden: Optional[bool] = ...): ...

    def __init__(self, _='messageActionTopicEdit', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def icon_emoji_id(self) -> Optional[int]:
        return self['icon_emoji_id']

    @property
    def closed(self) -> Optional[bool]:
        return self['closed']

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']


class MessageActionSuggestProfilePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo: aliases.AnyPhoto): ...

    def __init__(self, photo, _='messageActionSuggestProfilePhoto', **kwargs):
        kwargs['photo'] = photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])


class MessageActionRequestedPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, button_id: int, peers: list[aliases.AnyPeer]): ...

    def __init__(self, button_id, peers, _='messageActionRequestedPeer', **kwargs):
        kwargs['button_id'] = button_id
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def button_id(self) -> int:
        return self['button_id']

    @property
    def peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['peers'])


class MessageActionSetChatWallPaper(dict):
    __slots__ = ()

    @overload
    def __init__(self, wallpaper: aliases.AnyWallPaper, same: Optional[bool] = ..., for_both: Optional[bool] = ...): ...

    def __init__(self, wallpaper, _='messageActionSetChatWallPaper', **kwargs):
        kwargs['wallpaper'] = wallpaper
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def same(self) -> Optional[bool]:
        return self['same']

    @property
    def for_both(self) -> Optional[bool]:
        return self['for_both']

    @property
    def wallpaper(self) -> aliases.AnyWallPaper:
        return build_object(self['wallpaper'])


class MessageActionGiftCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, days: int, slug: str, via_giveaway: Optional[bool] = ..., unclaimed: Optional[bool] = ..., boost_peer: Optional[aliases.AnyPeer] = ..., currency: Optional[str] = ..., amount: Optional[int] = ..., crypto_currency: Optional[str] = ..., crypto_amount: Optional[int] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, days, slug, _='messageActionGiftCode', **kwargs):
        kwargs['days'] = days
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_giveaway(self) -> Optional[bool]:
        return self['via_giveaway']

    @property
    def unclaimed(self) -> Optional[bool]:
        return self['unclaimed']

    @property
    def boost_peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['boost_peer'])

    @property
    def days(self) -> int:
        return self['days']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def currency(self) -> Optional[str]:
        return self['currency']

    @property
    def amount(self) -> Optional[int]:
        return self['amount']

    @property
    def crypto_currency(self) -> Optional[str]:
        return self['crypto_currency']

    @property
    def crypto_amount(self) -> Optional[int]:
        return self['crypto_amount']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class MessageActionGiveawayLaunch(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: Optional[int] = ...): ...

    def __init__(self, _='messageActionGiveawayLaunch', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars(self) -> Optional[int]:
        return self['stars']


class MessageActionGiveawayResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, winners_count: int, unclaimed_count: int, stars: Optional[bool] = ...): ...

    def __init__(self, winners_count, unclaimed_count, _='messageActionGiveawayResults', **kwargs):
        kwargs['winners_count'] = winners_count
        kwargs['unclaimed_count'] = unclaimed_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars(self) -> Optional[bool]:
        return self['stars']

    @property
    def winners_count(self) -> int:
        return self['winners_count']

    @property
    def unclaimed_count(self) -> int:
        return self['unclaimed_count']


class MessageActionBoostApply(dict):
    __slots__ = ()

    @overload
    def __init__(self, boosts: int): ...

    def __init__(self, boosts, _='messageActionBoostApply', **kwargs):
        kwargs['boosts'] = boosts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def boosts(self) -> int:
        return self['boosts']


class MessageActionRequestedPeerSentMe(dict):
    __slots__ = ()

    @overload
    def __init__(self, button_id: int, peers: list[aliases.AnyRequestedPeer]): ...

    def __init__(self, button_id, peers, _='messageActionRequestedPeerSentMe', **kwargs):
        kwargs['button_id'] = button_id
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def button_id(self) -> int:
        return self['button_id']

    @property
    def peers(self) -> list[aliases.AnyRequestedPeer]:
        return build_object(self['peers'])


class MessageActionPaymentRefunded(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, currency: str, total_amount: int, charge: aliases.AnyPaymentCharge, payload: Optional[bytes] = ...): ...

    def __init__(self, peer, currency, total_amount, charge, _='messageActionPaymentRefunded', **kwargs):
        kwargs['peer'] = peer
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['charge'] = charge
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def payload(self) -> Optional[bytes]:
        return self['payload']

    @property
    def charge(self) -> aliases.AnyPaymentCharge:
        return build_object(self['charge'])


class MessageActionGiftStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, amount: int, stars: int, crypto_currency: Optional[str] = ..., crypto_amount: Optional[int] = ..., transaction_id: Optional[str] = ...): ...

    def __init__(self, currency, amount, stars, _='messageActionGiftStars', **kwargs):
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def crypto_currency(self) -> Optional[str]:
        return self['crypto_currency']

    @property
    def crypto_amount(self) -> Optional[int]:
        return self['crypto_amount']

    @property
    def transaction_id(self) -> Optional[str]:
        return self['transaction_id']


class MessageActionPrizeStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, transaction_id: str, boost_peer: aliases.AnyPeer, giveaway_msg_id: int, unclaimed: Optional[bool] = ...): ...

    def __init__(self, stars, transaction_id, boost_peer, giveaway_msg_id, _='messageActionPrizeStars', **kwargs):
        kwargs['stars'] = stars
        kwargs['transaction_id'] = transaction_id
        kwargs['boost_peer'] = boost_peer
        kwargs['giveaway_msg_id'] = giveaway_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unclaimed(self) -> Optional[bool]:
        return self['unclaimed']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def transaction_id(self) -> str:
        return self['transaction_id']

    @property
    def boost_peer(self) -> aliases.AnyPeer:
        return build_object(self['boost_peer'])

    @property
    def giveaway_msg_id(self) -> int:
        return self['giveaway_msg_id']


class MessageActionStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, name_hidden: Optional[bool] = ..., saved: Optional[bool] = ..., converted: Optional[bool] = ..., upgraded: Optional[bool] = ..., refunded: Optional[bool] = ..., can_upgrade: Optional[bool] = ..., prepaid_upgrade: Optional[bool] = ..., upgrade_separate: Optional[bool] = ..., auction_acquired: Optional[bool] = ..., message: Optional[aliases.AnyTextWithEntities] = ..., convert_stars: Optional[int] = ..., upgrade_msg_id: Optional[int] = ..., upgrade_stars: Optional[int] = ..., from_id: Optional[aliases.AnyPeer] = ..., peer: Optional[aliases.AnyPeer] = ..., saved_id: Optional[int] = ..., prepaid_upgrade_hash: Optional[str] = ..., gift_msg_id: Optional[int] = ..., to_id: Optional[aliases.AnyPeer] = ..., gift_num: Optional[int] = ...): ...

    def __init__(self, gift, _='messageActionStarGift', **kwargs):
        kwargs['gift'] = gift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name_hidden(self) -> Optional[bool]:
        return self['name_hidden']

    @property
    def saved(self) -> Optional[bool]:
        return self['saved']

    @property
    def converted(self) -> Optional[bool]:
        return self['converted']

    @property
    def upgraded(self) -> Optional[bool]:
        return self['upgraded']

    @property
    def refunded(self) -> Optional[bool]:
        return self['refunded']

    @property
    def can_upgrade(self) -> Optional[bool]:
        return self['can_upgrade']

    @property
    def prepaid_upgrade(self) -> Optional[bool]:
        return self['prepaid_upgrade']

    @property
    def upgrade_separate(self) -> Optional[bool]:
        return self['upgrade_separate']

    @property
    def auction_acquired(self) -> Optional[bool]:
        return self['auction_acquired']

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])

    @property
    def convert_stars(self) -> Optional[int]:
        return self['convert_stars']

    @property
    def upgrade_msg_id(self) -> Optional[int]:
        return self['upgrade_msg_id']

    @property
    def upgrade_stars(self) -> Optional[int]:
        return self['upgrade_stars']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer'])

    @property
    def saved_id(self) -> Optional[int]:
        return self['saved_id']

    @property
    def prepaid_upgrade_hash(self) -> Optional[str]:
        return self['prepaid_upgrade_hash']

    @property
    def gift_msg_id(self) -> Optional[int]:
        return self['gift_msg_id']

    @property
    def to_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['to_id'])

    @property
    def gift_num(self) -> Optional[int]:
        return self['gift_num']


class MessageActionStarGiftUnique(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, upgrade: Optional[bool] = ..., transferred: Optional[bool] = ..., saved: Optional[bool] = ..., refunded: Optional[bool] = ..., prepaid_upgrade: Optional[bool] = ..., assigned: Optional[bool] = ..., from_offer: Optional[bool] = ..., craft: Optional[bool] = ..., can_export_at: Optional[int] = ..., transfer_stars: Optional[int] = ..., from_id: Optional[aliases.AnyPeer] = ..., peer: Optional[aliases.AnyPeer] = ..., saved_id: Optional[int] = ..., resale_amount: Optional[aliases.AnyStarsAmount] = ..., can_transfer_at: Optional[int] = ..., can_resell_at: Optional[int] = ..., drop_original_details_stars: Optional[int] = ..., can_craft_at: Optional[int] = ...): ...

    def __init__(self, gift, _='messageActionStarGiftUnique', **kwargs):
        kwargs['gift'] = gift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def upgrade(self) -> Optional[bool]:
        return self['upgrade']

    @property
    def transferred(self) -> Optional[bool]:
        return self['transferred']

    @property
    def saved(self) -> Optional[bool]:
        return self['saved']

    @property
    def refunded(self) -> Optional[bool]:
        return self['refunded']

    @property
    def prepaid_upgrade(self) -> Optional[bool]:
        return self['prepaid_upgrade']

    @property
    def assigned(self) -> Optional[bool]:
        return self['assigned']

    @property
    def from_offer(self) -> Optional[bool]:
        return self['from_offer']

    @property
    def craft(self) -> Optional[bool]:
        return self['craft']

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def can_export_at(self) -> Optional[int]:
        return self['can_export_at']

    @property
    def transfer_stars(self) -> Optional[int]:
        return self['transfer_stars']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer'])

    @property
    def saved_id(self) -> Optional[int]:
        return self['saved_id']

    @property
    def resale_amount(self) -> Optional[aliases.AnyStarsAmount]:
        return build_object(self['resale_amount'])

    @property
    def can_transfer_at(self) -> Optional[int]:
        return self['can_transfer_at']

    @property
    def can_resell_at(self) -> Optional[int]:
        return self['can_resell_at']

    @property
    def drop_original_details_stars(self) -> Optional[int]:
        return self['drop_original_details_stars']

    @property
    def can_craft_at(self) -> Optional[int]:
        return self['can_craft_at']


class MessageActionPaidMessagesRefunded(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, stars: int): ...

    def __init__(self, count, stars, _='messageActionPaidMessagesRefunded', **kwargs):
        kwargs['count'] = count
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def count(self) -> int:
        return self['count']

    @property
    def stars(self) -> int:
        return self['stars']


class MessageActionPaidMessagesPrice(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, broadcast_messages_allowed: Optional[bool] = ...): ...

    def __init__(self, stars, _='messageActionPaidMessagesPrice', **kwargs):
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def broadcast_messages_allowed(self) -> Optional[bool]:
        return self['broadcast_messages_allowed']

    @property
    def stars(self) -> int:
        return self['stars']


class MessageActionConferenceCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call_id: int, missed: Optional[bool] = ..., active: Optional[bool] = ..., video: Optional[bool] = ..., duration: Optional[int] = ..., other_participants: Optional[list[aliases.AnyPeer]] = ...): ...

    def __init__(self, call_id, _='messageActionConferenceCall', **kwargs):
        kwargs['call_id'] = call_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def missed(self) -> Optional[bool]:
        return self['missed']

    @property
    def active(self) -> Optional[bool]:
        return self['active']

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def call_id(self) -> int:
        return self['call_id']

    @property
    def duration(self) -> Optional[int]:
        return self['duration']

    @property
    def other_participants(self) -> Optional[list[aliases.AnyPeer]]:
        return build_object(self['other_participants'])


class MessageActionTodoCompletions(dict):
    __slots__ = ()

    @overload
    def __init__(self, completed: list[int], incompleted: list[int]): ...

    def __init__(self, completed, incompleted, _='messageActionTodoCompletions', **kwargs):
        kwargs['completed'] = completed
        kwargs['incompleted'] = incompleted
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def completed(self) -> list[int]:
        return self['completed']

    @property
    def incompleted(self) -> list[int]:
        return self['incompleted']


class MessageActionTodoAppendTasks(dict):
    __slots__ = ()

    @overload
    def __init__(self, list: list[aliases.AnyTodoItem]): ...

    def __init__(self, list, _='messageActionTodoAppendTasks', **kwargs):
        kwargs['list'] = list
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def list(self) -> list[aliases.AnyTodoItem]:
        return build_object(self['list'])


class MessageActionSuggestedPostApproval(dict):
    __slots__ = ()

    @overload
    def __init__(self, rejected: Optional[bool] = ..., balance_too_low: Optional[bool] = ..., reject_comment: Optional[str] = ..., schedule_date: Optional[int] = ..., price: Optional[aliases.AnyStarsAmount] = ...): ...

    def __init__(self, _='messageActionSuggestedPostApproval', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def rejected(self) -> Optional[bool]:
        return self['rejected']

    @property
    def balance_too_low(self) -> Optional[bool]:
        return self['balance_too_low']

    @property
    def reject_comment(self) -> Optional[str]:
        return self['reject_comment']

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def price(self) -> Optional[aliases.AnyStarsAmount]:
        return build_object(self['price'])


class MessageActionSuggestedPostSuccess(dict):
    __slots__ = ()

    @overload
    def __init__(self, price: aliases.AnyStarsAmount): ...

    def __init__(self, price, _='messageActionSuggestedPostSuccess', **kwargs):
        kwargs['price'] = price
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def price(self) -> aliases.AnyStarsAmount:
        return build_object(self['price'])


class MessageActionSuggestedPostRefund(dict):
    __slots__ = ()

    @overload
    def __init__(self, payer_initiated: Optional[bool] = ...): ...

    def __init__(self, _='messageActionSuggestedPostRefund', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def payer_initiated(self) -> Optional[bool]:
        return self['payer_initiated']


class MessageActionGiftTon(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, amount: int, crypto_currency: str, crypto_amount: int, transaction_id: Optional[str] = ...): ...

    def __init__(self, currency, amount, crypto_currency, crypto_amount, _='messageActionGiftTon', **kwargs):
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['crypto_currency'] = crypto_currency
        kwargs['crypto_amount'] = crypto_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def crypto_currency(self) -> str:
        return self['crypto_currency']

    @property
    def crypto_amount(self) -> int:
        return self['crypto_amount']

    @property
    def transaction_id(self) -> Optional[str]:
        return self['transaction_id']


class MessageActionSuggestBirthday(dict):
    __slots__ = ()

    @overload
    def __init__(self, birthday: aliases.AnyBirthday): ...

    def __init__(self, birthday, _='messageActionSuggestBirthday', **kwargs):
        kwargs['birthday'] = birthday
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def birthday(self) -> aliases.AnyBirthday:
        return build_object(self['birthday'])


class MessageActionStarGiftPurchaseOffer(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, price: aliases.AnyStarsAmount, expires_at: int, accepted: Optional[bool] = ..., declined: Optional[bool] = ...): ...

    def __init__(self, gift, price, expires_at, _='messageActionStarGiftPurchaseOffer', **kwargs):
        kwargs['gift'] = gift
        kwargs['price'] = price
        kwargs['expires_at'] = expires_at
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def accepted(self) -> Optional[bool]:
        return self['accepted']

    @property
    def declined(self) -> Optional[bool]:
        return self['declined']

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def price(self) -> aliases.AnyStarsAmount:
        return build_object(self['price'])

    @property
    def expires_at(self) -> int:
        return self['expires_at']


class MessageActionStarGiftPurchaseOfferDeclined(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, price: aliases.AnyStarsAmount, expired: Optional[bool] = ...): ...

    def __init__(self, gift, price, _='messageActionStarGiftPurchaseOfferDeclined', **kwargs):
        kwargs['gift'] = gift
        kwargs['price'] = price
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expired(self) -> Optional[bool]:
        return self['expired']

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def price(self) -> aliases.AnyStarsAmount:
        return build_object(self['price'])


class MessageActionNewCreatorPending(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_creator_id: int): ...

    def __init__(self, new_creator_id, _='messageActionNewCreatorPending', **kwargs):
        kwargs['new_creator_id'] = new_creator_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_creator_id(self) -> int:
        return self['new_creator_id']


class MessageActionChangeCreator(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_creator_id: int): ...

    def __init__(self, new_creator_id, _='messageActionChangeCreator', **kwargs):
        kwargs['new_creator_id'] = new_creator_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_creator_id(self) -> int:
        return self['new_creator_id']


class MessageActionNoForwardsToggle(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: bool, new_value: bool): ...

    def __init__(self, prev_value, new_value, _='messageActionNoForwardsToggle', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> bool:
        return self['prev_value']

    @property
    def new_value(self) -> bool:
        return self['new_value']


class MessageActionNoForwardsRequest(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: bool, new_value: bool, expired: Optional[bool] = ...): ...

    def __init__(self, prev_value, new_value, _='messageActionNoForwardsRequest', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expired(self) -> Optional[bool]:
        return self['expired']

    @property
    def prev_value(self) -> bool:
        return self['prev_value']

    @property
    def new_value(self) -> bool:
        return self['new_value']


class Dialog(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, unread_reactions_count: int, notify_settings: aliases.AnyPeerNotifySettings, pinned: Optional[bool] = ..., unread_mark: Optional[bool] = ..., view_forum_as_messages: Optional[bool] = ..., pts: Optional[int] = ..., draft: Optional[aliases.AnyDraftMessage] = ..., folder_id: Optional[int] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, peer, top_message, read_inbox_max_id, read_outbox_max_id, unread_count, unread_mentions_count, unread_reactions_count, notify_settings, _='dialog', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_message'] = top_message
        kwargs['read_inbox_max_id'] = read_inbox_max_id
        kwargs['read_outbox_max_id'] = read_outbox_max_id
        kwargs['unread_count'] = unread_count
        kwargs['unread_mentions_count'] = unread_mentions_count
        kwargs['unread_reactions_count'] = unread_reactions_count
        kwargs['notify_settings'] = notify_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def unread_mark(self) -> Optional[bool]:
        return self['unread_mark']

    @property
    def view_forum_as_messages(self) -> Optional[bool]:
        return self['view_forum_as_messages']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_message(self) -> int:
        return self['top_message']

    @property
    def read_inbox_max_id(self) -> int:
        return self['read_inbox_max_id']

    @property
    def read_outbox_max_id(self) -> int:
        return self['read_outbox_max_id']

    @property
    def unread_count(self) -> int:
        return self['unread_count']

    @property
    def unread_mentions_count(self) -> int:
        return self['unread_mentions_count']

    @property
    def unread_reactions_count(self) -> int:
        return self['unread_reactions_count']

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])

    @property
    def pts(self) -> Optional[int]:
        return self['pts']

    @property
    def draft(self) -> Optional[aliases.AnyDraftMessage]:
        return build_object(self['draft'])

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class DialogFolder(dict):
    __slots__ = ()

    @overload
    def __init__(self, folder: aliases.AnyFolder, peer: aliases.AnyPeer, top_message: int, unread_muted_peers_count: int, unread_unmuted_peers_count: int, unread_muted_messages_count: int, unread_unmuted_messages_count: int, pinned: Optional[bool] = ...): ...

    def __init__(self, folder, peer, top_message, unread_muted_peers_count, unread_unmuted_peers_count, unread_muted_messages_count, unread_unmuted_messages_count, _='dialogFolder', **kwargs):
        kwargs['folder'] = folder
        kwargs['peer'] = peer
        kwargs['top_message'] = top_message
        kwargs['unread_muted_peers_count'] = unread_muted_peers_count
        kwargs['unread_unmuted_peers_count'] = unread_unmuted_peers_count
        kwargs['unread_muted_messages_count'] = unread_muted_messages_count
        kwargs['unread_unmuted_messages_count'] = unread_unmuted_messages_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def folder(self) -> aliases.AnyFolder:
        return build_object(self['folder'])

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_message(self) -> int:
        return self['top_message']

    @property
    def unread_muted_peers_count(self) -> int:
        return self['unread_muted_peers_count']

    @property
    def unread_unmuted_peers_count(self) -> int:
        return self['unread_unmuted_peers_count']

    @property
    def unread_muted_messages_count(self) -> int:
        return self['unread_muted_messages_count']

    @property
    def unread_unmuted_messages_count(self) -> int:
        return self['unread_unmuted_messages_count']


class PhotoEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='photoEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class Photo(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes, date: int, sizes: list[aliases.AnyPhotoSize], dc_id: int, has_stickers: Optional[bool] = ..., video_sizes: Optional[list[aliases.AnyVideoSize]] = ...): ...

    def __init__(self, id, access_hash, file_reference, date, sizes, dc_id, _='photo', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['date'] = date
        kwargs['sizes'] = sizes
        kwargs['dc_id'] = dc_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_stickers(self) -> Optional[bool]:
        return self['has_stickers']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def sizes(self) -> list[aliases.AnyPhotoSize]:
        return build_object(self['sizes'])

    @property
    def video_sizes(self) -> Optional[list[aliases.AnyVideoSize]]:
        return build_object(self['video_sizes'])

    @property
    def dc_id(self) -> int:
        return self['dc_id']


class PhotoSizeEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str): ...

    def __init__(self, type, _='photoSizeEmpty', **kwargs):
        kwargs['type'] = type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']


class PhotoSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, w: int, h: int, size: int): ...

    def __init__(self, type, w, h, size, _='photoSize', **kwargs):
        kwargs['type'] = type
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['size'] = size
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def size(self) -> int:
        return self['size']


class PhotoCachedSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, w: int, h: int, bytes: bytes): ...

    def __init__(self, type, w, h, bytes, _='photoCachedSize', **kwargs):
        kwargs['type'] = type
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class PhotoStrippedSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, bytes: bytes): ...

    def __init__(self, type, bytes, _='photoStrippedSize', **kwargs):
        kwargs['type'] = type
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class PhotoSizeProgressive(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, w: int, h: int, sizes: list[int]): ...

    def __init__(self, type, w, h, sizes, _='photoSizeProgressive', **kwargs):
        kwargs['type'] = type
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['sizes'] = sizes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def sizes(self) -> list[int]:
        return self['sizes']


class PhotoPathSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, bytes: bytes): ...

    def __init__(self, type, bytes, _='photoPathSize', **kwargs):
        kwargs['type'] = type
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class GeoPointEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='geoPointEmpty'):
        dict.__init__(self, _=_)


class GeoPoint(dict):
    __slots__ = ()

    @overload
    def __init__(self, long: float, lat: float, access_hash: int, accuracy_radius: Optional[int] = ...): ...

    def __init__(self, long, lat, access_hash, _='geoPoint', **kwargs):
        kwargs['long'] = long
        kwargs['lat'] = lat
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def long(self) -> float:
        return self['long']

    @property
    def lat(self) -> float:
        return self['lat']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def accuracy_radius(self) -> Optional[int]:
        return self['accuracy_radius']


class InputNotifyPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='inputNotifyPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class InputNotifyUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputNotifyUsers'):
        dict.__init__(self, _=_)


class InputNotifyChats(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputNotifyChats'):
        dict.__init__(self, _=_)


class InputNotifyBroadcasts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputNotifyBroadcasts'):
        dict.__init__(self, _=_)


class InputNotifyForumTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, top_msg_id: int): ...

    def __init__(self, peer, top_msg_id, _='inputNotifyForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_msg_id'] = top_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> int:
        return self['top_msg_id']


class InputPeerNotifySettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, show_previews: Optional[bool] = ..., silent: Optional[bool] = ..., mute_until: Optional[int] = ..., sound: Optional[aliases.AnyNotificationSound] = ..., stories_muted: Optional[bool] = ..., stories_hide_sender: Optional[bool] = ..., stories_sound: Optional[aliases.AnyNotificationSound] = ...): ...

    def __init__(self, _='inputPeerNotifySettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def show_previews(self) -> Optional[bool]:
        return self['show_previews']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def mute_until(self) -> Optional[int]:
        return self['mute_until']

    @property
    def sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['sound'])

    @property
    def stories_muted(self) -> Optional[bool]:
        return self['stories_muted']

    @property
    def stories_hide_sender(self) -> Optional[bool]:
        return self['stories_hide_sender']

    @property
    def stories_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['stories_sound'])


class PeerNotifySettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, show_previews: Optional[bool] = ..., silent: Optional[bool] = ..., mute_until: Optional[int] = ..., ios_sound: Optional[aliases.AnyNotificationSound] = ..., android_sound: Optional[aliases.AnyNotificationSound] = ..., other_sound: Optional[aliases.AnyNotificationSound] = ..., stories_muted: Optional[bool] = ..., stories_hide_sender: Optional[bool] = ..., stories_ios_sound: Optional[aliases.AnyNotificationSound] = ..., stories_android_sound: Optional[aliases.AnyNotificationSound] = ..., stories_other_sound: Optional[aliases.AnyNotificationSound] = ...): ...

    def __init__(self, _='peerNotifySettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def show_previews(self) -> Optional[bool]:
        return self['show_previews']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def mute_until(self) -> Optional[int]:
        return self['mute_until']

    @property
    def ios_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['ios_sound'])

    @property
    def android_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['android_sound'])

    @property
    def other_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['other_sound'])

    @property
    def stories_muted(self) -> Optional[bool]:
        return self['stories_muted']

    @property
    def stories_hide_sender(self) -> Optional[bool]:
        return self['stories_hide_sender']

    @property
    def stories_ios_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['stories_ios_sound'])

    @property
    def stories_android_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['stories_android_sound'])

    @property
    def stories_other_sound(self) -> Optional[aliases.AnyNotificationSound]:
        return build_object(self['stories_other_sound'])


class PeerSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, report_spam: Optional[bool] = ..., add_contact: Optional[bool] = ..., block_contact: Optional[bool] = ..., share_contact: Optional[bool] = ..., need_contacts_exception: Optional[bool] = ..., report_geo: Optional[bool] = ..., autoarchived: Optional[bool] = ..., invite_members: Optional[bool] = ..., request_chat_broadcast: Optional[bool] = ..., business_bot_paused: Optional[bool] = ..., business_bot_can_reply: Optional[bool] = ..., geo_distance: Optional[int] = ..., request_chat_title: Optional[str] = ..., request_chat_date: Optional[int] = ..., business_bot_id: Optional[int] = ..., business_bot_manage_url: Optional[str] = ..., charge_paid_message_stars: Optional[int] = ..., registration_month: Optional[str] = ..., phone_country: Optional[str] = ..., name_change_date: Optional[int] = ..., photo_change_date: Optional[int] = ...): ...

    def __init__(self, _='peerSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def report_spam(self) -> Optional[bool]:
        return self['report_spam']

    @property
    def add_contact(self) -> Optional[bool]:
        return self['add_contact']

    @property
    def block_contact(self) -> Optional[bool]:
        return self['block_contact']

    @property
    def share_contact(self) -> Optional[bool]:
        return self['share_contact']

    @property
    def need_contacts_exception(self) -> Optional[bool]:
        return self['need_contacts_exception']

    @property
    def report_geo(self) -> Optional[bool]:
        return self['report_geo']

    @property
    def autoarchived(self) -> Optional[bool]:
        return self['autoarchived']

    @property
    def invite_members(self) -> Optional[bool]:
        return self['invite_members']

    @property
    def request_chat_broadcast(self) -> Optional[bool]:
        return self['request_chat_broadcast']

    @property
    def business_bot_paused(self) -> Optional[bool]:
        return self['business_bot_paused']

    @property
    def business_bot_can_reply(self) -> Optional[bool]:
        return self['business_bot_can_reply']

    @property
    def geo_distance(self) -> Optional[int]:
        return self['geo_distance']

    @property
    def request_chat_title(self) -> Optional[str]:
        return self['request_chat_title']

    @property
    def request_chat_date(self) -> Optional[int]:
        return self['request_chat_date']

    @property
    def business_bot_id(self) -> Optional[int]:
        return self['business_bot_id']

    @property
    def business_bot_manage_url(self) -> Optional[str]:
        return self['business_bot_manage_url']

    @property
    def charge_paid_message_stars(self) -> Optional[int]:
        return self['charge_paid_message_stars']

    @property
    def registration_month(self) -> Optional[str]:
        return self['registration_month']

    @property
    def phone_country(self) -> Optional[str]:
        return self['phone_country']

    @property
    def name_change_date(self) -> Optional[int]:
        return self['name_change_date']

    @property
    def photo_change_date(self) -> Optional[int]:
        return self['photo_change_date']


class WallPaper(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, slug: str, document: aliases.AnyDocument, creator: Optional[bool] = ..., default: Optional[bool] = ..., pattern: Optional[bool] = ..., dark: Optional[bool] = ..., settings: Optional[aliases.AnyWallPaperSettings] = ...): ...

    def __init__(self, id, access_hash, slug, document, _='wallPaper', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['slug'] = slug
        kwargs['document'] = document
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def default(self) -> Optional[bool]:
        return self['default']

    @property
    def pattern(self) -> Optional[bool]:
        return self['pattern']

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def document(self) -> aliases.AnyDocument:
        return build_object(self['document'])

    @property
    def settings(self) -> Optional[aliases.AnyWallPaperSettings]:
        return build_object(self['settings'])


class WallPaperNoFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, default: Optional[bool] = ..., dark: Optional[bool] = ..., settings: Optional[aliases.AnyWallPaperSettings] = ...): ...

    def __init__(self, id, _='wallPaperNoFile', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def default(self) -> Optional[bool]:
        return self['default']

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def settings(self) -> Optional[aliases.AnyWallPaperSettings]:
        return build_object(self['settings'])


class InputReportReasonSpam(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonSpam'):
        dict.__init__(self, _=_)


class InputReportReasonViolence(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonViolence'):
        dict.__init__(self, _=_)


class InputReportReasonPornography(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonPornography'):
        dict.__init__(self, _=_)


class InputReportReasonChildAbuse(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonChildAbuse'):
        dict.__init__(self, _=_)


class InputReportReasonOther(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonOther'):
        dict.__init__(self, _=_)


class InputReportReasonCopyright(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonCopyright'):
        dict.__init__(self, _=_)


class InputReportReasonGeoIrrelevant(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonGeoIrrelevant'):
        dict.__init__(self, _=_)


class InputReportReasonFake(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonFake'):
        dict.__init__(self, _=_)


class InputReportReasonIllegalDrugs(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonIllegalDrugs'):
        dict.__init__(self, _=_)


class InputReportReasonPersonalDetails(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputReportReasonPersonalDetails'):
        dict.__init__(self, _=_)


class UserFull(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, settings: aliases.AnyPeerSettings, notify_settings: aliases.AnyPeerNotifySettings, common_chats_count: int, blocked: Optional[bool] = ..., phone_calls_available: Optional[bool] = ..., phone_calls_private: Optional[bool] = ..., can_pin_message: Optional[bool] = ..., has_scheduled: Optional[bool] = ..., video_calls_available: Optional[bool] = ..., voice_messages_forbidden: Optional[bool] = ..., translations_disabled: Optional[bool] = ..., stories_pinned_available: Optional[bool] = ..., blocked_my_stories_from: Optional[bool] = ..., wallpaper_overridden: Optional[bool] = ..., contact_require_premium: Optional[bool] = ..., read_dates_private: Optional[bool] = ..., sponsored_enabled: Optional[bool] = ..., can_view_revenue: Optional[bool] = ..., bot_can_manage_emoji_status: Optional[bool] = ..., display_gifts_button: Optional[bool] = ..., noforwards_my_enabled: Optional[bool] = ..., noforwards_peer_enabled: Optional[bool] = ..., about: Optional[str] = ..., personal_photo: Optional[aliases.AnyPhoto] = ..., profile_photo: Optional[aliases.AnyPhoto] = ..., fallback_photo: Optional[aliases.AnyPhoto] = ..., bot_info: Optional[aliases.AnyBotInfo] = ..., pinned_msg_id: Optional[int] = ..., folder_id: Optional[int] = ..., ttl_period: Optional[int] = ..., theme: Optional[aliases.AnyChatTheme] = ..., private_forward_name: Optional[str] = ..., bot_group_admin_rights: Optional[aliases.AnyChatAdminRights] = ..., bot_broadcast_admin_rights: Optional[aliases.AnyChatAdminRights] = ..., wallpaper: Optional[aliases.AnyWallPaper] = ..., stories: Optional[aliases.AnyPeerStories] = ..., business_work_hours: Optional[aliases.AnyBusinessWorkHours] = ..., business_location: Optional[aliases.AnyBusinessLocation] = ..., business_greeting_message: Optional[aliases.AnyBusinessGreetingMessage] = ..., business_away_message: Optional[aliases.AnyBusinessAwayMessage] = ..., business_intro: Optional[aliases.AnyBusinessIntro] = ..., birthday: Optional[aliases.AnyBirthday] = ..., personal_channel_id: Optional[int] = ..., personal_channel_message: Optional[int] = ..., stargifts_count: Optional[int] = ..., starref_program: Optional[aliases.AnyStarRefProgram] = ..., bot_verification: Optional[aliases.AnyBotVerification] = ..., send_paid_messages_stars: Optional[int] = ..., disallowed_gifts: Optional[aliases.AnyDisallowedGiftsSettings] = ..., stars_rating: Optional[aliases.AnyStarsRating] = ..., stars_my_pending_rating: Optional[aliases.AnyStarsRating] = ..., stars_my_pending_rating_date: Optional[int] = ..., main_tab: Optional[aliases.AnyProfileTab] = ..., saved_music: Optional[aliases.AnyDocument] = ..., note: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, id, settings, notify_settings, common_chats_count, _='userFull', **kwargs):
        kwargs['id'] = id
        kwargs['settings'] = settings
        kwargs['notify_settings'] = notify_settings
        kwargs['common_chats_count'] = common_chats_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def phone_calls_available(self) -> Optional[bool]:
        return self['phone_calls_available']

    @property
    def phone_calls_private(self) -> Optional[bool]:
        return self['phone_calls_private']

    @property
    def can_pin_message(self) -> Optional[bool]:
        return self['can_pin_message']

    @property
    def has_scheduled(self) -> Optional[bool]:
        return self['has_scheduled']

    @property
    def video_calls_available(self) -> Optional[bool]:
        return self['video_calls_available']

    @property
    def voice_messages_forbidden(self) -> Optional[bool]:
        return self['voice_messages_forbidden']

    @property
    def translations_disabled(self) -> Optional[bool]:
        return self['translations_disabled']

    @property
    def stories_pinned_available(self) -> Optional[bool]:
        return self['stories_pinned_available']

    @property
    def blocked_my_stories_from(self) -> Optional[bool]:
        return self['blocked_my_stories_from']

    @property
    def wallpaper_overridden(self) -> Optional[bool]:
        return self['wallpaper_overridden']

    @property
    def contact_require_premium(self) -> Optional[bool]:
        return self['contact_require_premium']

    @property
    def read_dates_private(self) -> Optional[bool]:
        return self['read_dates_private']

    @property
    def sponsored_enabled(self) -> Optional[bool]:
        return self['sponsored_enabled']

    @property
    def can_view_revenue(self) -> Optional[bool]:
        return self['can_view_revenue']

    @property
    def bot_can_manage_emoji_status(self) -> Optional[bool]:
        return self['bot_can_manage_emoji_status']

    @property
    def display_gifts_button(self) -> Optional[bool]:
        return self['display_gifts_button']

    @property
    def noforwards_my_enabled(self) -> Optional[bool]:
        return self['noforwards_my_enabled']

    @property
    def noforwards_peer_enabled(self) -> Optional[bool]:
        return self['noforwards_peer_enabled']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def about(self) -> Optional[str]:
        return self['about']

    @property
    def settings(self) -> aliases.AnyPeerSettings:
        return build_object(self['settings'])

    @property
    def personal_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['personal_photo'])

    @property
    def profile_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['profile_photo'])

    @property
    def fallback_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['fallback_photo'])

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])

    @property
    def bot_info(self) -> Optional[aliases.AnyBotInfo]:
        return build_object(self['bot_info'])

    @property
    def pinned_msg_id(self) -> Optional[int]:
        return self['pinned_msg_id']

    @property
    def common_chats_count(self) -> int:
        return self['common_chats_count']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']

    @property
    def theme(self) -> Optional[aliases.AnyChatTheme]:
        return build_object(self['theme'])

    @property
    def private_forward_name(self) -> Optional[str]:
        return self['private_forward_name']

    @property
    def bot_group_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['bot_group_admin_rights'])

    @property
    def bot_broadcast_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['bot_broadcast_admin_rights'])

    @property
    def wallpaper(self) -> Optional[aliases.AnyWallPaper]:
        return build_object(self['wallpaper'])

    @property
    def stories(self) -> Optional[aliases.AnyPeerStories]:
        return build_object(self['stories'])

    @property
    def business_work_hours(self) -> Optional[aliases.AnyBusinessWorkHours]:
        return build_object(self['business_work_hours'])

    @property
    def business_location(self) -> Optional[aliases.AnyBusinessLocation]:
        return build_object(self['business_location'])

    @property
    def business_greeting_message(self) -> Optional[aliases.AnyBusinessGreetingMessage]:
        return build_object(self['business_greeting_message'])

    @property
    def business_away_message(self) -> Optional[aliases.AnyBusinessAwayMessage]:
        return build_object(self['business_away_message'])

    @property
    def business_intro(self) -> Optional[aliases.AnyBusinessIntro]:
        return build_object(self['business_intro'])

    @property
    def birthday(self) -> Optional[aliases.AnyBirthday]:
        return build_object(self['birthday'])

    @property
    def personal_channel_id(self) -> Optional[int]:
        return self['personal_channel_id']

    @property
    def personal_channel_message(self) -> Optional[int]:
        return self['personal_channel_message']

    @property
    def stargifts_count(self) -> Optional[int]:
        return self['stargifts_count']

    @property
    def starref_program(self) -> Optional[aliases.AnyStarRefProgram]:
        return build_object(self['starref_program'])

    @property
    def bot_verification(self) -> Optional[aliases.AnyBotVerification]:
        return build_object(self['bot_verification'])

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']

    @property
    def disallowed_gifts(self) -> Optional[aliases.AnyDisallowedGiftsSettings]:
        return build_object(self['disallowed_gifts'])

    @property
    def stars_rating(self) -> Optional[aliases.AnyStarsRating]:
        return build_object(self['stars_rating'])

    @property
    def stars_my_pending_rating(self) -> Optional[aliases.AnyStarsRating]:
        return build_object(self['stars_my_pending_rating'])

    @property
    def stars_my_pending_rating_date(self) -> Optional[int]:
        return self['stars_my_pending_rating_date']

    @property
    def main_tab(self) -> Optional[aliases.AnyProfileTab]:
        return build_object(self['main_tab'])

    @property
    def saved_music(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['saved_music'])

    @property
    def note(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['note'])


class Contact(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, mutual: bool): ...

    def __init__(self, user_id, mutual, _='contact', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['mutual'] = mutual
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def mutual(self) -> bool:
        return self['mutual']


class ImportedContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, client_id: int): ...

    def __init__(self, user_id, client_id, _='importedContact', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['client_id'] = client_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def client_id(self) -> int:
        return self['client_id']


class ContactStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, status: aliases.AnyUserStatus): ...

    def __init__(self, user_id, status, _='contactStatus', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['status'] = status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def status(self) -> aliases.AnyUserStatus:
        return build_object(self['status'])


class InputMessagesFilterEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterEmpty'):
        dict.__init__(self, _=_)


class InputMessagesFilterPhotos(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterPhotos'):
        dict.__init__(self, _=_)


class InputMessagesFilterVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterVideo'):
        dict.__init__(self, _=_)


class InputMessagesFilterPhotoVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterPhotoVideo'):
        dict.__init__(self, _=_)


class InputMessagesFilterDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterDocument'):
        dict.__init__(self, _=_)


class InputMessagesFilterUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterUrl'):
        dict.__init__(self, _=_)


class InputMessagesFilterGif(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterGif'):
        dict.__init__(self, _=_)


class InputMessagesFilterVoice(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterVoice'):
        dict.__init__(self, _=_)


class InputMessagesFilterMusic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterMusic'):
        dict.__init__(self, _=_)


class InputMessagesFilterChatPhotos(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterChatPhotos'):
        dict.__init__(self, _=_)


class InputMessagesFilterPhoneCalls(dict):
    __slots__ = ()

    @overload
    def __init__(self, missed: Optional[bool] = ...): ...

    def __init__(self, _='inputMessagesFilterPhoneCalls', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def missed(self) -> Optional[bool]:
        return self['missed']


class InputMessagesFilterRoundVoice(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterRoundVoice'):
        dict.__init__(self, _=_)


class InputMessagesFilterRoundVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterRoundVideo'):
        dict.__init__(self, _=_)


class InputMessagesFilterMyMentions(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterMyMentions'):
        dict.__init__(self, _=_)


class InputMessagesFilterGeo(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterGeo'):
        dict.__init__(self, _=_)


class InputMessagesFilterContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterContacts'):
        dict.__init__(self, _=_)


class InputMessagesFilterPinned(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagesFilterPinned'):
        dict.__init__(self, _=_)


class UpdateNewMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage, pts: int, pts_count: int): ...

    def __init__(self, message, pts, pts_count, _='updateNewMessage', **kwargs):
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateMessageID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, random_id: int): ...

    def __init__(self, id, random_id, _='updateMessageID', **kwargs):
        kwargs['id'] = id
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def random_id(self) -> int:
        return self['random_id']


class UpdateDeleteMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, messages: list[int], pts: int, pts_count: int): ...

    def __init__(self, messages, pts, pts_count, _='updateDeleteMessages', **kwargs):
        kwargs['messages'] = messages
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateUserTyping(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, action: aliases.AnySendMessageAction, top_msg_id: Optional[int] = ...): ...

    def __init__(self, user_id, action, _='updateUserTyping', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def action(self) -> aliases.AnySendMessageAction:
        return build_object(self['action'])


class UpdateChatUserTyping(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, from_id: aliases.AnyPeer, action: aliases.AnySendMessageAction): ...

    def __init__(self, chat_id, from_id, action, _='updateChatUserTyping', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['from_id'] = from_id
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def action(self) -> aliases.AnySendMessageAction:
        return build_object(self['action'])


class UpdateChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, participants: aliases.AnyChatParticipants): ...

    def __init__(self, participants, _='updateChatParticipants', **kwargs):
        kwargs['participants'] = participants
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participants(self) -> aliases.AnyChatParticipants:
        return build_object(self['participants'])


class UpdateUserStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, status: aliases.AnyUserStatus): ...

    def __init__(self, user_id, status, _='updateUserStatus', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['status'] = status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def status(self) -> aliases.AnyUserStatus:
        return build_object(self['status'])


class UpdateUserName(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, first_name: str, last_name: str, usernames: list[aliases.AnyUsername]): ...

    def __init__(self, user_id, first_name, last_name, usernames, _='updateUserName', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['usernames'] = usernames
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def usernames(self) -> list[aliases.AnyUsername]:
        return build_object(self['usernames'])


class UpdateNewAuthorization(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, unconfirmed: Optional[bool] = ..., date: Optional[int] = ..., device: Optional[str] = ..., location: Optional[str] = ...): ...

    def __init__(self, hash, _='updateNewAuthorization', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unconfirmed(self) -> Optional[bool]:
        return self['unconfirmed']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def date(self) -> Optional[int]:
        return self['date']

    @property
    def device(self) -> Optional[str]:
        return self['device']

    @property
    def location(self) -> Optional[str]:
        return self['location']


class UpdateNewEncryptedMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyEncryptedMessage, qts: int): ...

    def __init__(self, message, qts, _='updateNewEncryptedMessage', **kwargs):
        kwargs['message'] = message
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyEncryptedMessage:
        return build_object(self['message'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateEncryptedChatTyping(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='updateEncryptedChatTyping', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class UpdateEncryption(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat: aliases.AnyEncryptedChat, date: int): ...

    def __init__(self, chat, date, _='updateEncryption', **kwargs):
        kwargs['chat'] = chat
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat(self) -> aliases.AnyEncryptedChat:
        return build_object(self['chat'])

    @property
    def date(self) -> int:
        return self['date']


class UpdateEncryptedMessagesRead(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, max_date: int, date: int): ...

    def __init__(self, chat_id, max_date, date, _='updateEncryptedMessagesRead', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['max_date'] = max_date
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def max_date(self) -> int:
        return self['max_date']

    @property
    def date(self) -> int:
        return self['date']


class UpdateChatParticipantAdd(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: int, inviter_id: int, date: int, version: int): ...

    def __init__(self, chat_id, user_id, inviter_id, date, version, _='updateChatParticipantAdd', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['inviter_id'] = inviter_id
        kwargs['date'] = date
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def inviter_id(self) -> int:
        return self['inviter_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def version(self) -> int:
        return self['version']


class UpdateChatParticipantDelete(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: int, version: int): ...

    def __init__(self, chat_id, user_id, version, _='updateChatParticipantDelete', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def version(self) -> int:
        return self['version']


class UpdateDcOptions(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_options: list[aliases.AnyDcOption]): ...

    def __init__(self, dc_options, _='updateDcOptions', **kwargs):
        kwargs['dc_options'] = dc_options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_options(self) -> list[aliases.AnyDcOption]:
        return build_object(self['dc_options'])


class UpdateNotifySettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyNotifyPeer, notify_settings: aliases.AnyPeerNotifySettings): ...

    def __init__(self, peer, notify_settings, _='updateNotifySettings', **kwargs):
        kwargs['peer'] = peer
        kwargs['notify_settings'] = notify_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyNotifyPeer:
        return build_object(self['peer'])

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])


class UpdateServiceNotification(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, message: str, media: aliases.AnyMessageMedia, entities: list[aliases.AnyMessageEntity], popup: Optional[bool] = ..., invert_media: Optional[bool] = ..., inbox_date: Optional[int] = ...): ...

    def __init__(self, type, message, media, entities, _='updateServiceNotification', **kwargs):
        kwargs['type'] = type
        kwargs['message'] = message
        kwargs['media'] = media
        kwargs['entities'] = entities
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def popup(self) -> Optional[bool]:
        return self['popup']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def inbox_date(self) -> Optional[int]:
        return self['inbox_date']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def media(self) -> aliases.AnyMessageMedia:
        return build_object(self['media'])

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])


class UpdatePrivacy(dict):
    __slots__ = ()

    @overload
    def __init__(self, key: aliases.AnyPrivacyKey, rules: list[aliases.AnyPrivacyRule]): ...

    def __init__(self, key, rules, _='updatePrivacy', **kwargs):
        kwargs['key'] = key
        kwargs['rules'] = rules
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> aliases.AnyPrivacyKey:
        return build_object(self['key'])

    @property
    def rules(self) -> list[aliases.AnyPrivacyRule]:
        return build_object(self['rules'])


class UpdateUserPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, phone: str): ...

    def __init__(self, user_id, phone, _='updateUserPhone', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def phone(self) -> str:
        return self['phone']


class UpdateReadHistoryInbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, max_id: int, still_unread_count: int, pts: int, pts_count: int, folder_id: Optional[int] = ..., top_msg_id: Optional[int] = ...): ...

    def __init__(self, peer, max_id, still_unread_count, pts, pts_count, _='updateReadHistoryInbox', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['still_unread_count'] = still_unread_count
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def still_unread_count(self) -> int:
        return self['still_unread_count']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateReadHistoryOutbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, max_id: int, pts: int, pts_count: int): ...

    def __init__(self, peer, max_id, pts, pts_count, _='updateReadHistoryOutbox', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, webpage: aliases.AnyWebPage, pts: int, pts_count: int): ...

    def __init__(self, webpage, pts, pts_count, _='updateWebPage', **kwargs):
        kwargs['webpage'] = webpage
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def webpage(self) -> aliases.AnyWebPage:
        return build_object(self['webpage'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateReadMessagesContents(dict):
    __slots__ = ()

    @overload
    def __init__(self, messages: list[int], pts: int, pts_count: int, date: Optional[int] = ...): ...

    def __init__(self, messages, pts, pts_count, _='updateReadMessagesContents', **kwargs):
        kwargs['messages'] = messages
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def date(self) -> Optional[int]:
        return self['date']


class UpdateChannelTooLong(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, pts: Optional[int] = ...): ...

    def __init__(self, channel_id, _='updateChannelTooLong', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def pts(self) -> Optional[int]:
        return self['pts']


class UpdateChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int): ...

    def __init__(self, channel_id, _='updateChannel', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']


class UpdateNewChannelMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage, pts: int, pts_count: int): ...

    def __init__(self, message, pts, pts_count, _='updateNewChannelMessage', **kwargs):
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateReadChannelInbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, max_id: int, still_unread_count: int, pts: int, folder_id: Optional[int] = ...): ...

    def __init__(self, channel_id, max_id, still_unread_count, pts, _='updateReadChannelInbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['max_id'] = max_id
        kwargs['still_unread_count'] = still_unread_count
        kwargs['pts'] = pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def max_id(self) -> int:
        return self['max_id']

    @property
    def still_unread_count(self) -> int:
        return self['still_unread_count']

    @property
    def pts(self) -> int:
        return self['pts']


class UpdateDeleteChannelMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, messages: list[int], pts: int, pts_count: int): ...

    def __init__(self, channel_id, messages, pts, pts_count, _='updateDeleteChannelMessages', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['messages'] = messages
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateChannelMessageViews(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, id: int, views: int): ...

    def __init__(self, channel_id, id, views, _='updateChannelMessageViews', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['id'] = id
        kwargs['views'] = views
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def views(self) -> int:
        return self['views']


class UpdateChatParticipantAdmin(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: int, is_admin: bool, version: int): ...

    def __init__(self, chat_id, user_id, is_admin, version, _='updateChatParticipantAdmin', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['is_admin'] = is_admin
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def is_admin(self) -> bool:
        return self['is_admin']

    @property
    def version(self) -> int:
        return self['version']


class UpdateNewStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyMessagesStickerSet): ...

    def __init__(self, stickerset, _='updateNewStickerSet', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyMessagesStickerSet:
        return build_object(self['stickerset'])


class UpdateStickerSetsOrder(dict):
    __slots__ = ()

    @overload
    def __init__(self, order: list[int], masks: Optional[bool] = ..., emojis: Optional[bool] = ...): ...

    def __init__(self, order, _='updateStickerSetsOrder', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def order(self) -> list[int]:
        return self['order']


class UpdateStickerSets(dict):
    __slots__ = ()

    @overload
    def __init__(self, masks: Optional[bool] = ..., emojis: Optional[bool] = ...): ...

    def __init__(self, _='updateStickerSets', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']


class UpdateSavedGifs(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateSavedGifs'):
        dict.__init__(self, _=_)


class UpdateBotInlineQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, query: str, offset: str, geo: Optional[aliases.AnyGeoPoint] = ..., peer_type: Optional[aliases.AnyInlineQueryPeerType] = ...): ...

    def __init__(self, query_id, user_id, query, offset, _='updateBotInlineQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['query'] = query
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def query(self) -> str:
        return self['query']

    @property
    def geo(self) -> Optional[aliases.AnyGeoPoint]:
        return build_object(self['geo'])

    @property
    def peer_type(self) -> Optional[aliases.AnyInlineQueryPeerType]:
        return build_object(self['peer_type'])

    @property
    def offset(self) -> str:
        return self['offset']


class UpdateBotInlineSend(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, query: str, id: str, geo: Optional[aliases.AnyGeoPoint] = ..., msg_id: Optional[aliases.AnyInputBotInlineMessageID] = ...): ...

    def __init__(self, user_id, query, id, _='updateBotInlineSend', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['query'] = query
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def query(self) -> str:
        return self['query']

    @property
    def geo(self) -> Optional[aliases.AnyGeoPoint]:
        return build_object(self['geo'])

    @property
    def id(self) -> str:
        return self['id']

    @property
    def msg_id(self) -> Optional[aliases.AnyInputBotInlineMessageID]:
        return build_object(self['msg_id'])


class UpdateEditChannelMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage, pts: int, pts_count: int): ...

    def __init__(self, message, pts, pts_count, _='updateEditChannelMessage', **kwargs):
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateBotCallbackQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, peer: aliases.AnyPeer, msg_id: int, chat_instance: int, data: Optional[bytes] = ..., game_short_name: Optional[str] = ...): ...

    def __init__(self, query_id, user_id, peer, msg_id, chat_instance, _='updateBotCallbackQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['chat_instance'] = chat_instance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def chat_instance(self) -> int:
        return self['chat_instance']

    @property
    def data(self) -> Optional[bytes]:
        return self['data']

    @property
    def game_short_name(self) -> Optional[str]:
        return self['game_short_name']


class UpdateEditMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage, pts: int, pts_count: int): ...

    def __init__(self, message, pts, pts_count, _='updateEditMessage', **kwargs):
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateInlineBotCallbackQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, msg_id: aliases.AnyInputBotInlineMessageID, chat_instance: int, data: Optional[bytes] = ..., game_short_name: Optional[str] = ...): ...

    def __init__(self, query_id, user_id, msg_id, chat_instance, _='updateInlineBotCallbackQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['msg_id'] = msg_id
        kwargs['chat_instance'] = chat_instance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def msg_id(self) -> aliases.AnyInputBotInlineMessageID:
        return build_object(self['msg_id'])

    @property
    def chat_instance(self) -> int:
        return self['chat_instance']

    @property
    def data(self) -> Optional[bytes]:
        return self['data']

    @property
    def game_short_name(self) -> Optional[str]:
        return self['game_short_name']


class UpdateReadChannelOutbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, max_id: int): ...

    def __init__(self, channel_id, max_id, _='updateReadChannelOutbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def max_id(self) -> int:
        return self['max_id']


class UpdateDraftMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, draft: aliases.AnyDraftMessage, top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, peer, draft, _='updateDraftMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['draft'] = draft
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def draft(self) -> aliases.AnyDraftMessage:
        return build_object(self['draft'])


class UpdateReadFeaturedStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateReadFeaturedStickers'):
        dict.__init__(self, _=_)


class UpdateRecentStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateRecentStickers'):
        dict.__init__(self, _=_)


class UpdateConfig(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateConfig'):
        dict.__init__(self, _=_)


class UpdatePtsChanged(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updatePtsChanged'):
        dict.__init__(self, _=_)


class UpdateChannelWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, webpage: aliases.AnyWebPage, pts: int, pts_count: int): ...

    def __init__(self, channel_id, webpage, pts, pts_count, _='updateChannelWebPage', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['webpage'] = webpage
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def webpage(self) -> aliases.AnyWebPage:
        return build_object(self['webpage'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateDialogPinned(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyDialogPeer, pinned: Optional[bool] = ..., folder_id: Optional[int] = ...): ...

    def __init__(self, peer, _='updateDialogPinned', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def peer(self) -> aliases.AnyDialogPeer:
        return build_object(self['peer'])


class UpdatePinnedDialogs(dict):
    __slots__ = ()

    @overload
    def __init__(self, folder_id: Optional[int] = ..., order: Optional[list[aliases.AnyDialogPeer]] = ...): ...

    def __init__(self, _='updatePinnedDialogs', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def order(self) -> Optional[list[aliases.AnyDialogPeer]]:
        return build_object(self['order'])


class UpdateBotWebhookJSON(dict):
    __slots__ = ()

    @overload
    def __init__(self, data: aliases.AnyDataJSON): ...

    def __init__(self, data, _='updateBotWebhookJSON', **kwargs):
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def data(self) -> aliases.AnyDataJSON:
        return build_object(self['data'])


class UpdateBotWebhookJSONQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, data: aliases.AnyDataJSON, timeout: int): ...

    def __init__(self, query_id, data, timeout, _='updateBotWebhookJSONQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['data'] = data
        kwargs['timeout'] = timeout
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def data(self) -> aliases.AnyDataJSON:
        return build_object(self['data'])

    @property
    def timeout(self) -> int:
        return self['timeout']


class UpdateBotShippingQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, payload: bytes, shipping_address: aliases.AnyPostAddress): ...

    def __init__(self, query_id, user_id, payload, shipping_address, _='updateBotShippingQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['payload'] = payload
        kwargs['shipping_address'] = shipping_address
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def payload(self) -> bytes:
        return self['payload']

    @property
    def shipping_address(self) -> aliases.AnyPostAddress:
        return build_object(self['shipping_address'])


class UpdateBotPrecheckoutQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, payload: bytes, currency: str, total_amount: int, info: Optional[aliases.AnyPaymentRequestedInfo] = ..., shipping_option_id: Optional[str] = ...): ...

    def __init__(self, query_id, user_id, payload, currency, total_amount, _='updateBotPrecheckoutQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['payload'] = payload
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def payload(self) -> bytes:
        return self['payload']

    @property
    def info(self) -> Optional[aliases.AnyPaymentRequestedInfo]:
        return build_object(self['info'])

    @property
    def shipping_option_id(self) -> Optional[str]:
        return self['shipping_option_id']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']


class UpdatePhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_call: aliases.AnyPhoneCall): ...

    def __init__(self, phone_call, _='updatePhoneCall', **kwargs):
        kwargs['phone_call'] = phone_call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_call(self) -> aliases.AnyPhoneCall:
        return build_object(self['phone_call'])


class UpdateLangPackTooLong(dict):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str): ...

    def __init__(self, lang_code, _='updateLangPackTooLong', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class UpdateLangPack(dict):
    __slots__ = ()

    @overload
    def __init__(self, difference: aliases.AnyLangPackDifference): ...

    def __init__(self, difference, _='updateLangPack', **kwargs):
        kwargs['difference'] = difference
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def difference(self) -> aliases.AnyLangPackDifference:
        return build_object(self['difference'])


class UpdateFavedStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateFavedStickers'):
        dict.__init__(self, _=_)


class UpdateChannelReadMessagesContents(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, messages: list[int], top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, channel_id, messages, _='updateChannelReadMessagesContents', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def messages(self) -> list[int]:
        return self['messages']


class UpdateContactsReset(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateContactsReset'):
        dict.__init__(self, _=_)


class UpdateChannelAvailableMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, available_min_id: int): ...

    def __init__(self, channel_id, available_min_id, _='updateChannelAvailableMessages', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['available_min_id'] = available_min_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def available_min_id(self) -> int:
        return self['available_min_id']


class UpdateDialogUnreadMark(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyDialogPeer, unread: Optional[bool] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, peer, _='updateDialogUnreadMark', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unread(self) -> Optional[bool]:
        return self['unread']

    @property
    def peer(self) -> aliases.AnyDialogPeer:
        return build_object(self['peer'])

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])


class UpdateMessagePoll(dict):
    __slots__ = ()

    @overload
    def __init__(self, poll_id: int, results: aliases.AnyPollResults, poll: Optional[aliases.AnyPoll] = ...): ...

    def __init__(self, poll_id, results, _='updateMessagePoll', **kwargs):
        kwargs['poll_id'] = poll_id
        kwargs['results'] = results
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def poll_id(self) -> int:
        return self['poll_id']

    @property
    def poll(self) -> Optional[aliases.AnyPoll]:
        return build_object(self['poll'])

    @property
    def results(self) -> aliases.AnyPollResults:
        return build_object(self['results'])


class UpdateChatDefaultBannedRights(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, default_banned_rights: aliases.AnyChatBannedRights, version: int): ...

    def __init__(self, peer, default_banned_rights, version, _='updateChatDefaultBannedRights', **kwargs):
        kwargs['peer'] = peer
        kwargs['default_banned_rights'] = default_banned_rights
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def default_banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['default_banned_rights'])

    @property
    def version(self) -> int:
        return self['version']


class UpdateFolderPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, folder_peers: list[aliases.AnyFolderPeer], pts: int, pts_count: int): ...

    def __init__(self, folder_peers, pts, pts_count, _='updateFolderPeers', **kwargs):
        kwargs['folder_peers'] = folder_peers
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_peers(self) -> list[aliases.AnyFolderPeer]:
        return build_object(self['folder_peers'])

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdatePeerSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, settings: aliases.AnyPeerSettings): ...

    def __init__(self, peer, settings, _='updatePeerSettings', **kwargs):
        kwargs['peer'] = peer
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def settings(self) -> aliases.AnyPeerSettings:
        return build_object(self['settings'])


class UpdatePeerLocated(dict):
    __slots__ = ()

    @overload
    def __init__(self, peers: list[aliases.AnyPeerLocated]): ...

    def __init__(self, peers, _='updatePeerLocated', **kwargs):
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peers(self) -> list[aliases.AnyPeerLocated]:
        return build_object(self['peers'])


class UpdateNewScheduledMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='updateNewScheduledMessage', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class UpdateDeleteScheduledMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, messages: list[int], sent_messages: Optional[list[int]] = ...): ...

    def __init__(self, peer, messages, _='updateDeleteScheduledMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def sent_messages(self) -> Optional[list[int]]:
        return self['sent_messages']


class UpdateTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, theme: aliases.AnyTheme): ...

    def __init__(self, theme, _='updateTheme', **kwargs):
        kwargs['theme'] = theme
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def theme(self) -> aliases.AnyTheme:
        return build_object(self['theme'])


class UpdateGeoLiveViewed(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='updateGeoLiveViewed', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class UpdateLoginToken(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateLoginToken'):
        dict.__init__(self, _=_)


class UpdateMessagePollVote(dict):
    __slots__ = ()

    @overload
    def __init__(self, poll_id: int, peer: aliases.AnyPeer, options: list[bytes], qts: int): ...

    def __init__(self, poll_id, peer, options, qts, _='updateMessagePollVote', **kwargs):
        kwargs['poll_id'] = poll_id
        kwargs['peer'] = peer
        kwargs['options'] = options
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def poll_id(self) -> int:
        return self['poll_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def options(self) -> list[bytes]:
        return self['options']

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateDialogFilter(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, filter: Optional[aliases.AnyDialogFilter] = ...): ...

    def __init__(self, id, _='updateDialogFilter', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def filter(self) -> Optional[aliases.AnyDialogFilter]:
        return build_object(self['filter'])


class UpdateDialogFilterOrder(dict):
    __slots__ = ()

    @overload
    def __init__(self, order: list[int]): ...

    def __init__(self, order, _='updateDialogFilterOrder', **kwargs):
        kwargs['order'] = order
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order(self) -> list[int]:
        return self['order']


class UpdateDialogFilters(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateDialogFilters'):
        dict.__init__(self, _=_)


class UpdatePhoneCallSignalingData(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_call_id: int, data: bytes): ...

    def __init__(self, phone_call_id, data, _='updatePhoneCallSignalingData', **kwargs):
        kwargs['phone_call_id'] = phone_call_id
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_call_id(self) -> int:
        return self['phone_call_id']

    @property
    def data(self) -> bytes:
        return self['data']


class UpdateChannelMessageForwards(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, id: int, forwards: int): ...

    def __init__(self, channel_id, id, forwards, _='updateChannelMessageForwards', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['id'] = id
        kwargs['forwards'] = forwards
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def forwards(self) -> int:
        return self['forwards']


class UpdateReadChannelDiscussionInbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, top_msg_id: int, read_max_id: int, broadcast_id: Optional[int] = ..., broadcast_post: Optional[int] = ...): ...

    def __init__(self, channel_id, top_msg_id, read_max_id, _='updateReadChannelDiscussionInbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['top_msg_id'] = top_msg_id
        kwargs['read_max_id'] = read_max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def top_msg_id(self) -> int:
        return self['top_msg_id']

    @property
    def read_max_id(self) -> int:
        return self['read_max_id']

    @property
    def broadcast_id(self) -> Optional[int]:
        return self['broadcast_id']

    @property
    def broadcast_post(self) -> Optional[int]:
        return self['broadcast_post']


class UpdateReadChannelDiscussionOutbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, top_msg_id: int, read_max_id: int): ...

    def __init__(self, channel_id, top_msg_id, read_max_id, _='updateReadChannelDiscussionOutbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['top_msg_id'] = top_msg_id
        kwargs['read_max_id'] = read_max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def top_msg_id(self) -> int:
        return self['top_msg_id']

    @property
    def read_max_id(self) -> int:
        return self['read_max_id']


class UpdatePeerBlocked(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, blocked: Optional[bool] = ..., blocked_my_stories_from: Optional[bool] = ...): ...

    def __init__(self, peer_id, _='updatePeerBlocked', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def blocked_my_stories_from(self) -> Optional[bool]:
        return self['blocked_my_stories_from']

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])


class UpdateChannelUserTyping(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, from_id: aliases.AnyPeer, action: aliases.AnySendMessageAction, top_msg_id: Optional[int] = ...): ...

    def __init__(self, channel_id, from_id, action, _='updateChannelUserTyping', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['from_id'] = from_id
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def action(self) -> aliases.AnySendMessageAction:
        return build_object(self['action'])


class UpdatePinnedMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, messages: list[int], pts: int, pts_count: int, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, messages, pts, pts_count, _='updatePinnedMessages', **kwargs):
        kwargs['peer'] = peer
        kwargs['messages'] = messages
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdatePinnedChannelMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, messages: list[int], pts: int, pts_count: int, pinned: Optional[bool] = ...): ...

    def __init__(self, channel_id, messages, pts, pts_count, _='updatePinnedChannelMessages', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['messages'] = messages
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']


class UpdateChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int): ...

    def __init__(self, chat_id, _='updateChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class UpdateGroupCallParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, participants: list[aliases.AnyGroupCallParticipant], version: int): ...

    def __init__(self, call, participants, version, _='updateGroupCallParticipants', **kwargs):
        kwargs['call'] = call
        kwargs['participants'] = participants
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def participants(self) -> list[aliases.AnyGroupCallParticipant]:
        return build_object(self['participants'])

    @property
    def version(self) -> int:
        return self['version']


class UpdateGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyGroupCall, live_story: Optional[bool] = ..., peer: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, call, _='updateGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def live_story(self) -> Optional[bool]:
        return self['live_story']

    @property
    def peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer'])

    @property
    def call(self) -> aliases.AnyGroupCall:
        return build_object(self['call'])


class UpdatePeerHistoryTTL(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, ttl_period: Optional[int] = ...): ...

    def __init__(self, peer, _='updatePeerHistoryTTL', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class UpdateChatParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, date: int, actor_id: int, user_id: int, qts: int, prev_participant: Optional[aliases.AnyChatParticipant] = ..., new_participant: Optional[aliases.AnyChatParticipant] = ..., invite: Optional[aliases.AnyExportedChatInvite] = ...): ...

    def __init__(self, chat_id, date, actor_id, user_id, qts, _='updateChatParticipant', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['date'] = date
        kwargs['actor_id'] = actor_id
        kwargs['user_id'] = user_id
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def actor_id(self) -> int:
        return self['actor_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def prev_participant(self) -> Optional[aliases.AnyChatParticipant]:
        return build_object(self['prev_participant'])

    @property
    def new_participant(self) -> Optional[aliases.AnyChatParticipant]:
        return build_object(self['new_participant'])

    @property
    def invite(self) -> Optional[aliases.AnyExportedChatInvite]:
        return build_object(self['invite'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateChannelParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, date: int, actor_id: int, user_id: int, qts: int, via_chatlist: Optional[bool] = ..., prev_participant: Optional[aliases.AnyChannelParticipant] = ..., new_participant: Optional[aliases.AnyChannelParticipant] = ..., invite: Optional[aliases.AnyExportedChatInvite] = ...): ...

    def __init__(self, channel_id, date, actor_id, user_id, qts, _='updateChannelParticipant', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['date'] = date
        kwargs['actor_id'] = actor_id
        kwargs['user_id'] = user_id
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_chatlist(self) -> Optional[bool]:
        return self['via_chatlist']

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def actor_id(self) -> int:
        return self['actor_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def prev_participant(self) -> Optional[aliases.AnyChannelParticipant]:
        return build_object(self['prev_participant'])

    @property
    def new_participant(self) -> Optional[aliases.AnyChannelParticipant]:
        return build_object(self['new_participant'])

    @property
    def invite(self) -> Optional[aliases.AnyExportedChatInvite]:
        return build_object(self['invite'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateBotStopped(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, date: int, stopped: bool, qts: int): ...

    def __init__(self, user_id, date, stopped, qts, _='updateBotStopped', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['date'] = date
        kwargs['stopped'] = stopped
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def stopped(self) -> bool:
        return self['stopped']

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateGroupCallConnection(dict):
    __slots__ = ()

    @overload
    def __init__(self, params: aliases.AnyDataJSON, presentation: Optional[bool] = ...): ...

    def __init__(self, params, _='updateGroupCallConnection', **kwargs):
        kwargs['params'] = params
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def presentation(self) -> Optional[bool]:
        return self['presentation']

    @property
    def params(self) -> aliases.AnyDataJSON:
        return build_object(self['params'])


class UpdateBotCommands(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, bot_id: int, commands: list[aliases.AnyBotCommand]): ...

    def __init__(self, peer, bot_id, commands, _='updateBotCommands', **kwargs):
        kwargs['peer'] = peer
        kwargs['bot_id'] = bot_id
        kwargs['commands'] = commands
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def commands(self) -> list[aliases.AnyBotCommand]:
        return build_object(self['commands'])


class UpdatePendingJoinRequests(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, requests_pending: int, recent_requesters: list[int]): ...

    def __init__(self, peer, requests_pending, recent_requesters, _='updatePendingJoinRequests', **kwargs):
        kwargs['peer'] = peer
        kwargs['requests_pending'] = requests_pending
        kwargs['recent_requesters'] = recent_requesters
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def requests_pending(self) -> int:
        return self['requests_pending']

    @property
    def recent_requesters(self) -> list[int]:
        return self['recent_requesters']


class UpdateBotChatInviteRequester(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, date: int, user_id: int, about: str, invite: aliases.AnyExportedChatInvite, qts: int): ...

    def __init__(self, peer, date, user_id, about, invite, qts, _='updateBotChatInviteRequester', **kwargs):
        kwargs['peer'] = peer
        kwargs['date'] = date
        kwargs['user_id'] = user_id
        kwargs['about'] = about
        kwargs['invite'] = invite
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def about(self) -> str:
        return self['about']

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateMessageReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int, reactions: aliases.AnyMessageReactions, top_msg_id: Optional[int] = ..., saved_peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, peer, msg_id, reactions, _='updateMessageReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def saved_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_peer_id'])

    @property
    def reactions(self) -> aliases.AnyMessageReactions:
        return build_object(self['reactions'])


class UpdateAttachMenuBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateAttachMenuBots'):
        dict.__init__(self, _=_)


class UpdateWebViewResultSent(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int): ...

    def __init__(self, query_id, _='updateWebViewResultSent', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']


class UpdateBotMenuButton(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, button: aliases.AnyBotMenuButton): ...

    def __init__(self, bot_id, button, _='updateBotMenuButton', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['button'] = button
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def button(self) -> aliases.AnyBotMenuButton:
        return build_object(self['button'])


class UpdateSavedRingtones(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateSavedRingtones'):
        dict.__init__(self, _=_)


class UpdateTranscribedAudio(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int, transcription_id: int, text: str, pending: Optional[bool] = ...): ...

    def __init__(self, peer, msg_id, transcription_id, text, _='updateTranscribedAudio', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['transcription_id'] = transcription_id
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pending(self) -> Optional[bool]:
        return self['pending']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def transcription_id(self) -> int:
        return self['transcription_id']

    @property
    def text(self) -> str:
        return self['text']


class UpdateReadFeaturedEmojiStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateReadFeaturedEmojiStickers'):
        dict.__init__(self, _=_)


class UpdateUserEmojiStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, emoji_status: aliases.AnyEmojiStatus): ...

    def __init__(self, user_id, emoji_status, _='updateUserEmojiStatus', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['emoji_status'] = emoji_status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def emoji_status(self) -> aliases.AnyEmojiStatus:
        return build_object(self['emoji_status'])


class UpdateRecentEmojiStatuses(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateRecentEmojiStatuses'):
        dict.__init__(self, _=_)


class UpdateRecentReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateRecentReactions'):
        dict.__init__(self, _=_)


class UpdateMoveStickerSetToTop(dict):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: int, masks: Optional[bool] = ..., emojis: Optional[bool] = ...): ...

    def __init__(self, stickerset, _='updateMoveStickerSetToTop', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def masks(self) -> Optional[bool]:
        return self['masks']

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def stickerset(self) -> int:
        return self['stickerset']


class UpdateMessageExtendedMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int, extended_media: list[aliases.AnyMessageExtendedMedia]): ...

    def __init__(self, peer, msg_id, extended_media, _='updateMessageExtendedMedia', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['extended_media'] = extended_media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def extended_media(self) -> list[aliases.AnyMessageExtendedMedia]:
        return build_object(self['extended_media'])


class UpdateUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int): ...

    def __init__(self, user_id, _='updateUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']


class UpdateAutoSaveSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateAutoSaveSettings'):
        dict.__init__(self, _=_)


class UpdateStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, story: aliases.AnyStoryItem): ...

    def __init__(self, peer, story, _='updateStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['story'] = story
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def story(self) -> aliases.AnyStoryItem:
        return build_object(self['story'])


class UpdateReadStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, max_id: int): ...

    def __init__(self, peer, max_id, _='updateReadStories', **kwargs):
        kwargs['peer'] = peer
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def max_id(self) -> int:
        return self['max_id']


class UpdateStoryID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, random_id: int): ...

    def __init__(self, id, random_id, _='updateStoryID', **kwargs):
        kwargs['id'] = id
        kwargs['random_id'] = random_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def random_id(self) -> int:
        return self['random_id']


class UpdateStoriesStealthMode(dict):
    __slots__ = ()

    @overload
    def __init__(self, stealth_mode: aliases.AnyStoriesStealthMode): ...

    def __init__(self, stealth_mode, _='updateStoriesStealthMode', **kwargs):
        kwargs['stealth_mode'] = stealth_mode
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stealth_mode(self) -> aliases.AnyStoriesStealthMode:
        return build_object(self['stealth_mode'])


class UpdateSentStoryReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, story_id: int, reaction: aliases.AnyReaction): ...

    def __init__(self, peer, story_id, reaction, _='updateSentStoryReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['story_id'] = story_id
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def story_id(self) -> int:
        return self['story_id']

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class UpdateBotChatBoost(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, boost: aliases.AnyBoost, qts: int): ...

    def __init__(self, peer, boost, qts, _='updateBotChatBoost', **kwargs):
        kwargs['peer'] = peer
        kwargs['boost'] = boost
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def boost(self) -> aliases.AnyBoost:
        return build_object(self['boost'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateChannelViewForumAsMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, enabled: bool): ...

    def __init__(self, channel_id, enabled, _='updateChannelViewForumAsMessages', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['enabled'] = enabled
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def enabled(self) -> bool:
        return self['enabled']


class UpdatePeerWallpaper(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, wallpaper_overridden: Optional[bool] = ..., wallpaper: Optional[aliases.AnyWallPaper] = ...): ...

    def __init__(self, peer, _='updatePeerWallpaper', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def wallpaper_overridden(self) -> Optional[bool]:
        return self['wallpaper_overridden']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def wallpaper(self) -> Optional[aliases.AnyWallPaper]:
        return build_object(self['wallpaper'])


class UpdateBotMessageReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int, date: int, actor: aliases.AnyPeer, old_reactions: list[aliases.AnyReaction], new_reactions: list[aliases.AnyReaction], qts: int): ...

    def __init__(self, peer, msg_id, date, actor, old_reactions, new_reactions, qts, _='updateBotMessageReaction', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['date'] = date
        kwargs['actor'] = actor
        kwargs['old_reactions'] = old_reactions
        kwargs['new_reactions'] = new_reactions
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def actor(self) -> aliases.AnyPeer:
        return build_object(self['actor'])

    @property
    def old_reactions(self) -> list[aliases.AnyReaction]:
        return build_object(self['old_reactions'])

    @property
    def new_reactions(self) -> list[aliases.AnyReaction]:
        return build_object(self['new_reactions'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateBotMessageReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, msg_id: int, date: int, reactions: list[aliases.AnyReactionCount], qts: int): ...

    def __init__(self, peer, msg_id, date, reactions, qts, _='updateBotMessageReactions', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['date'] = date
        kwargs['reactions'] = reactions
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def reactions(self) -> list[aliases.AnyReactionCount]:
        return build_object(self['reactions'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateSavedDialogPinned(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyDialogPeer, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, _='updateSavedDialogPinned', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyDialogPeer:
        return build_object(self['peer'])


class UpdatePinnedSavedDialogs(dict):
    __slots__ = ()

    @overload
    def __init__(self, order: Optional[list[aliases.AnyDialogPeer]] = ...): ...

    def __init__(self, _='updatePinnedSavedDialogs', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def order(self) -> Optional[list[aliases.AnyDialogPeer]]:
        return build_object(self['order'])


class UpdateSavedReactionTags(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateSavedReactionTags'):
        dict.__init__(self, _=_)


class UpdateSmsJob(dict):
    __slots__ = ()

    @overload
    def __init__(self, job_id: str): ...

    def __init__(self, job_id, _='updateSmsJob', **kwargs):
        kwargs['job_id'] = job_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def job_id(self) -> str:
        return self['job_id']


class UpdateQuickReplies(dict):
    __slots__ = ()

    @overload
    def __init__(self, quick_replies: list[aliases.AnyQuickReply]): ...

    def __init__(self, quick_replies, _='updateQuickReplies', **kwargs):
        kwargs['quick_replies'] = quick_replies
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def quick_replies(self) -> list[aliases.AnyQuickReply]:
        return build_object(self['quick_replies'])


class UpdateNewQuickReply(dict):
    __slots__ = ()

    @overload
    def __init__(self, quick_reply: aliases.AnyQuickReply): ...

    def __init__(self, quick_reply, _='updateNewQuickReply', **kwargs):
        kwargs['quick_reply'] = quick_reply
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def quick_reply(self) -> aliases.AnyQuickReply:
        return build_object(self['quick_reply'])


class UpdateDeleteQuickReply(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int): ...

    def __init__(self, shortcut_id, _='updateDeleteQuickReply', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']


class UpdateQuickReplyMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='updateQuickReplyMessage', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class UpdateDeleteQuickReplyMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, messages: list[int]): ...

    def __init__(self, shortcut_id, messages, _='updateDeleteQuickReplyMessages', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def messages(self) -> list[int]:
        return self['messages']


class UpdateBotBusinessConnect(dict):
    __slots__ = ()

    @overload
    def __init__(self, connection: aliases.AnyBotBusinessConnection, qts: int): ...

    def __init__(self, connection, qts, _='updateBotBusinessConnect', **kwargs):
        kwargs['connection'] = connection
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection(self) -> aliases.AnyBotBusinessConnection:
        return build_object(self['connection'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateBotNewBusinessMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str, message: aliases.AnyMessage, qts: int, reply_to_message: Optional[aliases.AnyMessage] = ...): ...

    def __init__(self, connection_id, message, qts, _='updateBotNewBusinessMessage', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['message'] = message
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def reply_to_message(self) -> Optional[aliases.AnyMessage]:
        return build_object(self['reply_to_message'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateBotEditBusinessMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str, message: aliases.AnyMessage, qts: int, reply_to_message: Optional[aliases.AnyMessage] = ...): ...

    def __init__(self, connection_id, message, qts, _='updateBotEditBusinessMessage', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['message'] = message
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def reply_to_message(self) -> Optional[aliases.AnyMessage]:
        return build_object(self['reply_to_message'])

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateBotDeleteBusinessMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str, peer: aliases.AnyPeer, messages: list[int], qts: int): ...

    def __init__(self, connection_id, peer, messages, qts, _='updateBotDeleteBusinessMessage', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['peer'] = peer
        kwargs['messages'] = messages
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def messages(self) -> list[int]:
        return self['messages']

    @property
    def qts(self) -> int:
        return self['qts']


class UpdateNewStoryReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, story_id: int, peer: aliases.AnyPeer, reaction: aliases.AnyReaction): ...

    def __init__(self, story_id, peer, reaction, _='updateNewStoryReaction', **kwargs):
        kwargs['story_id'] = story_id
        kwargs['peer'] = peer
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def story_id(self) -> int:
        return self['story_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class UpdateStarsBalance(dict):
    __slots__ = ()

    @overload
    def __init__(self, balance: aliases.AnyStarsAmount): ...

    def __init__(self, balance, _='updateStarsBalance', **kwargs):
        kwargs['balance'] = balance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def balance(self) -> aliases.AnyStarsAmount:
        return build_object(self['balance'])


class UpdateBusinessBotCallbackQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, query_id: int, user_id: int, connection_id: str, message: aliases.AnyMessage, chat_instance: int, reply_to_message: Optional[aliases.AnyMessage] = ..., data: Optional[bytes] = ...): ...

    def __init__(self, query_id, user_id, connection_id, message, chat_instance, _='updateBusinessBotCallbackQuery', **kwargs):
        kwargs['query_id'] = query_id
        kwargs['user_id'] = user_id
        kwargs['connection_id'] = connection_id
        kwargs['message'] = message
        kwargs['chat_instance'] = chat_instance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])

    @property
    def reply_to_message(self) -> Optional[aliases.AnyMessage]:
        return build_object(self['reply_to_message'])

    @property
    def chat_instance(self) -> int:
        return self['chat_instance']

    @property
    def data(self) -> Optional[bytes]:
        return self['data']


class UpdateStarsRevenueStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, status: aliases.AnyStarsRevenueStatus): ...

    def __init__(self, peer, status, _='updateStarsRevenueStatus', **kwargs):
        kwargs['peer'] = peer
        kwargs['status'] = status
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def status(self) -> aliases.AnyStarsRevenueStatus:
        return build_object(self['status'])


class UpdateBotPurchasedPaidMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, payload: str, qts: int): ...

    def __init__(self, user_id, payload, qts, _='updateBotPurchasedPaidMedia', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['payload'] = payload
        kwargs['qts'] = qts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def payload(self) -> str:
        return self['payload']

    @property
    def qts(self) -> int:
        return self['qts']


class UpdatePaidReactionPrivacy(dict):
    __slots__ = ()

    @overload
    def __init__(self, private: aliases.AnyPaidReactionPrivacy): ...

    def __init__(self, private, _='updatePaidReactionPrivacy', **kwargs):
        kwargs['private'] = private
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def private(self) -> aliases.AnyPaidReactionPrivacy:
        return build_object(self['private'])


class UpdateSentPhoneCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, sent_code: aliases.AnyAuthSentCode): ...

    def __init__(self, sent_code, _='updateSentPhoneCode', **kwargs):
        kwargs['sent_code'] = sent_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sent_code(self) -> aliases.AnyAuthSentCode:
        return build_object(self['sent_code'])


class UpdateGroupCallChainBlocks(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, sub_chain_id: int, blocks: list[bytes], next_offset: int): ...

    def __init__(self, call, sub_chain_id, blocks, next_offset, _='updateGroupCallChainBlocks', **kwargs):
        kwargs['call'] = call
        kwargs['sub_chain_id'] = sub_chain_id
        kwargs['blocks'] = blocks
        kwargs['next_offset'] = next_offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def sub_chain_id(self) -> int:
        return self['sub_chain_id']

    @property
    def blocks(self) -> list[bytes]:
        return self['blocks']

    @property
    def next_offset(self) -> int:
        return self['next_offset']


class UpdateReadMonoForumInbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, saved_peer_id: aliases.AnyPeer, read_max_id: int): ...

    def __init__(self, channel_id, saved_peer_id, read_max_id, _='updateReadMonoForumInbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['saved_peer_id'] = saved_peer_id
        kwargs['read_max_id'] = read_max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def saved_peer_id(self) -> aliases.AnyPeer:
        return build_object(self['saved_peer_id'])

    @property
    def read_max_id(self) -> int:
        return self['read_max_id']


class UpdateReadMonoForumOutbox(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, saved_peer_id: aliases.AnyPeer, read_max_id: int): ...

    def __init__(self, channel_id, saved_peer_id, read_max_id, _='updateReadMonoForumOutbox', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['saved_peer_id'] = saved_peer_id
        kwargs['read_max_id'] = read_max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def saved_peer_id(self) -> aliases.AnyPeer:
        return build_object(self['saved_peer_id'])

    @property
    def read_max_id(self) -> int:
        return self['read_max_id']


class UpdateMonoForumNoPaidException(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, saved_peer_id: aliases.AnyPeer, exception: Optional[bool] = ...): ...

    def __init__(self, channel_id, saved_peer_id, _='updateMonoForumNoPaidException', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['saved_peer_id'] = saved_peer_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exception(self) -> Optional[bool]:
        return self['exception']

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def saved_peer_id(self) -> aliases.AnyPeer:
        return build_object(self['saved_peer_id'])


class UpdateGroupCallMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, message: aliases.AnyGroupCallMessage): ...

    def __init__(self, call, message, _='updateGroupCallMessage', **kwargs):
        kwargs['call'] = call
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def message(self) -> aliases.AnyGroupCallMessage:
        return build_object(self['message'])


class UpdateGroupCallEncryptedMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, from_id: aliases.AnyPeer, encrypted_message: bytes): ...

    def __init__(self, call, from_id, encrypted_message, _='updateGroupCallEncryptedMessage', **kwargs):
        kwargs['call'] = call
        kwargs['from_id'] = from_id
        kwargs['encrypted_message'] = encrypted_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def encrypted_message(self) -> bytes:
        return self['encrypted_message']


class UpdatePinnedForumTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, topic_id: int, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, topic_id, _='updatePinnedForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['topic_id'] = topic_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def topic_id(self) -> int:
        return self['topic_id']


class UpdatePinnedForumTopics(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, order: Optional[list[int]] = ...): ...

    def __init__(self, peer, _='updatePinnedForumTopics', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def order(self) -> Optional[list[int]]:
        return self['order']


class UpdateDeleteGroupCallMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall, messages: list[int]): ...

    def __init__(self, call, messages, _='updateDeleteGroupCallMessages', **kwargs):
        kwargs['call'] = call
        kwargs['messages'] = messages
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])

    @property
    def messages(self) -> list[int]:
        return self['messages']


class UpdateStarGiftAuctionState(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int, state: aliases.AnyStarGiftAuctionState): ...

    def __init__(self, gift_id, state, _='updateStarGiftAuctionState', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['state'] = state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def state(self) -> aliases.AnyStarGiftAuctionState:
        return build_object(self['state'])


class UpdateStarGiftAuctionUserState(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int, user_state: aliases.AnyStarGiftAuctionUserState): ...

    def __init__(self, gift_id, user_state, _='updateStarGiftAuctionUserState', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['user_state'] = user_state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def user_state(self) -> aliases.AnyStarGiftAuctionUserState:
        return build_object(self['user_state'])


class UpdateEmojiGameInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, info: aliases.AnyMessagesEmojiGameInfo): ...

    def __init__(self, info, _='updateEmojiGameInfo', **kwargs):
        kwargs['info'] = info
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def info(self) -> aliases.AnyMessagesEmojiGameInfo:
        return build_object(self['info'])


class UpdateStarGiftCraftFail(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updateStarGiftCraftFail'):
        dict.__init__(self, _=_)


class UpdateChatParticipantRank(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, user_id: int, rank: str, version: int): ...

    def __init__(self, chat_id, user_id, rank, version, _='updateChatParticipantRank', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['user_id'] = user_id
        kwargs['rank'] = rank
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def rank(self) -> str:
        return self['rank']

    @property
    def version(self) -> int:
        return self['version']


class UpdatesTooLong(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='updatesTooLong'):
        dict.__init__(self, _=_)


class UpdateShortMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, user_id: int, message: str, pts: int, pts_count: int, date: int, out: Optional[bool] = ..., mentioned: Optional[bool] = ..., media_unread: Optional[bool] = ..., silent: Optional[bool] = ..., fwd_from: Optional[aliases.AnyMessageFwdHeader] = ..., via_bot_id: Optional[int] = ..., reply_to: Optional[aliases.AnyMessageReplyHeader] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, id, user_id, message, pts, pts_count, date, _='updateShortMessage', **kwargs):
        kwargs['id'] = id
        kwargs['user_id'] = user_id
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def mentioned(self) -> Optional[bool]:
        return self['mentioned']

    @property
    def media_unread(self) -> Optional[bool]:
        return self['media_unread']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def fwd_from(self) -> Optional[aliases.AnyMessageFwdHeader]:
        return build_object(self['fwd_from'])

    @property
    def via_bot_id(self) -> Optional[int]:
        return self['via_bot_id']

    @property
    def reply_to(self) -> Optional[aliases.AnyMessageReplyHeader]:
        return build_object(self['reply_to'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class UpdateShortChatMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, from_id: int, chat_id: int, message: str, pts: int, pts_count: int, date: int, out: Optional[bool] = ..., mentioned: Optional[bool] = ..., media_unread: Optional[bool] = ..., silent: Optional[bool] = ..., fwd_from: Optional[aliases.AnyMessageFwdHeader] = ..., via_bot_id: Optional[int] = ..., reply_to: Optional[aliases.AnyMessageReplyHeader] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, id, from_id, chat_id, message, pts, pts_count, date, _='updateShortChatMessage', **kwargs):
        kwargs['id'] = id
        kwargs['from_id'] = from_id
        kwargs['chat_id'] = chat_id
        kwargs['message'] = message
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def mentioned(self) -> Optional[bool]:
        return self['mentioned']

    @property
    def media_unread(self) -> Optional[bool]:
        return self['media_unread']

    @property
    def silent(self) -> Optional[bool]:
        return self['silent']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def from_id(self) -> int:
        return self['from_id']

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def fwd_from(self) -> Optional[aliases.AnyMessageFwdHeader]:
        return build_object(self['fwd_from'])

    @property
    def via_bot_id(self) -> Optional[int]:
        return self['via_bot_id']

    @property
    def reply_to(self) -> Optional[aliases.AnyMessageReplyHeader]:
        return build_object(self['reply_to'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class UpdateShort(dict):
    __slots__ = ()

    @overload
    def __init__(self, update_: aliases.AnyUpdate, date: int): ...

    def __init__(self, update_, date, _='updateShort', **kwargs):
        kwargs['update'] = update_
        kwargs['date'] = date
        if 'update_' in kwargs:
            kwargs['update'] = kwargs.pop('update_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def update_(self) -> aliases.AnyUpdate:
        return build_object(self['update'])

    @property
    def date(self) -> int:
        return self['date']


class UpdatesCombined(dict):
    __slots__ = ()

    @overload
    def __init__(self, updates: list[aliases.AnyUpdate], users: list[aliases.AnyUser], chats: list[aliases.AnyChat], date: int, seq_start: int, seq: int): ...

    def __init__(self, updates, users, chats, date, seq_start, seq, _='updatesCombined', **kwargs):
        kwargs['updates'] = updates
        kwargs['users'] = users
        kwargs['chats'] = chats
        kwargs['date'] = date
        kwargs['seq_start'] = seq_start
        kwargs['seq'] = seq
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def updates(self) -> list[aliases.AnyUpdate]:
        return build_object(self['updates'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def seq_start(self) -> int:
        return self['seq_start']

    @property
    def seq(self) -> int:
        return self['seq']


class Updates(dict):
    __slots__ = ()

    @overload
    def __init__(self, updates: list[aliases.AnyUpdate], users: list[aliases.AnyUser], chats: list[aliases.AnyChat], date: int, seq: int): ...

    def __init__(self, updates, users, chats, date, seq, _='updates', **kwargs):
        kwargs['updates'] = updates
        kwargs['users'] = users
        kwargs['chats'] = chats
        kwargs['date'] = date
        kwargs['seq'] = seq
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def updates(self) -> list[aliases.AnyUpdate]:
        return build_object(self['updates'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])

    @property
    def chats(self) -> list[aliases.AnyChat]:
        return build_object(self['chats'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def seq(self) -> int:
        return self['seq']


class UpdateShortSentMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, pts: int, pts_count: int, date: int, out: Optional[bool] = ..., media: Optional[aliases.AnyMessageMedia] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., ttl_period: Optional[int] = ...): ...

    def __init__(self, id, pts, pts_count, date, _='updateShortSentMessage', **kwargs):
        kwargs['id'] = id
        kwargs['pts'] = pts
        kwargs['pts_count'] = pts_count
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def pts(self) -> int:
        return self['pts']

    @property
    def pts_count(self) -> int:
        return self['pts_count']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def media(self) -> Optional[aliases.AnyMessageMedia]:
        return build_object(self['media'])

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def ttl_period(self) -> Optional[int]:
        return self['ttl_period']


class DcOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, ip_address: str, port: int, ipv6: Optional[bool] = ..., media_only: Optional[bool] = ..., tcpo_only: Optional[bool] = ..., cdn: Optional[bool] = ..., static: Optional[bool] = ..., this_port_only: Optional[bool] = ..., secret: Optional[bytes] = ...): ...

    def __init__(self, id, ip_address, port, _='dcOption', **kwargs):
        kwargs['id'] = id
        kwargs['ip_address'] = ip_address
        kwargs['port'] = port
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ipv6(self) -> Optional[bool]:
        return self['ipv6']

    @property
    def media_only(self) -> Optional[bool]:
        return self['media_only']

    @property
    def tcpo_only(self) -> Optional[bool]:
        return self['tcpo_only']

    @property
    def cdn(self) -> Optional[bool]:
        return self['cdn']

    @property
    def static(self) -> Optional[bool]:
        return self['static']

    @property
    def this_port_only(self) -> Optional[bool]:
        return self['this_port_only']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def ip_address(self) -> str:
        return self['ip_address']

    @property
    def port(self) -> int:
        return self['port']

    @property
    def secret(self) -> Optional[bytes]:
        return self['secret']


class Config(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, expires: int, test_mode: bool, this_dc: int, dc_options: list[aliases.AnyDcOption], dc_txt_domain_name: str, chat_size_max: int, megagroup_size_max: int, forwarded_count_max: int, online_update_period_ms: int, offline_blur_timeout_ms: int, offline_idle_timeout_ms: int, online_cloud_timeout_ms: int, notify_cloud_delay_ms: int, notify_default_delay_ms: int, push_chat_period_ms: int, push_chat_limit: int, edit_time_limit: int, revoke_time_limit: int, revoke_pm_time_limit: int, rating_e_decay: int, stickers_recent_limit: int, channels_read_media_period: int, call_receive_timeout_ms: int, call_ring_timeout_ms: int, call_connect_timeout_ms: int, call_packet_timeout_ms: int, me_url_prefix: str, caption_length_max: int, message_length_max: int, webfile_dc_id: int, default_p2p_contacts: Optional[bool] = ..., preload_featured_stickers: Optional[bool] = ..., revoke_pm_inbox: Optional[bool] = ..., blocked_mode: Optional[bool] = ..., force_try_ipv6: Optional[bool] = ..., tmp_sessions: Optional[int] = ..., autoupdate_url_prefix: Optional[str] = ..., gif_search_username: Optional[str] = ..., venue_search_username: Optional[str] = ..., img_search_username: Optional[str] = ..., static_maps_provider: Optional[str] = ..., suggested_lang_code: Optional[str] = ..., lang_pack_version: Optional[int] = ..., base_lang_pack_version: Optional[int] = ..., reactions_default: Optional[aliases.AnyReaction] = ..., autologin_token: Optional[str] = ...): ...

    def __init__(self, date, expires, test_mode, this_dc, dc_options, dc_txt_domain_name, chat_size_max, megagroup_size_max, forwarded_count_max, online_update_period_ms, offline_blur_timeout_ms, offline_idle_timeout_ms, online_cloud_timeout_ms, notify_cloud_delay_ms, notify_default_delay_ms, push_chat_period_ms, push_chat_limit, edit_time_limit, revoke_time_limit, revoke_pm_time_limit, rating_e_decay, stickers_recent_limit, channels_read_media_period, call_receive_timeout_ms, call_ring_timeout_ms, call_connect_timeout_ms, call_packet_timeout_ms, me_url_prefix, caption_length_max, message_length_max, webfile_dc_id, _='config', **kwargs):
        kwargs['date'] = date
        kwargs['expires'] = expires
        kwargs['test_mode'] = test_mode
        kwargs['this_dc'] = this_dc
        kwargs['dc_options'] = dc_options
        kwargs['dc_txt_domain_name'] = dc_txt_domain_name
        kwargs['chat_size_max'] = chat_size_max
        kwargs['megagroup_size_max'] = megagroup_size_max
        kwargs['forwarded_count_max'] = forwarded_count_max
        kwargs['online_update_period_ms'] = online_update_period_ms
        kwargs['offline_blur_timeout_ms'] = offline_blur_timeout_ms
        kwargs['offline_idle_timeout_ms'] = offline_idle_timeout_ms
        kwargs['online_cloud_timeout_ms'] = online_cloud_timeout_ms
        kwargs['notify_cloud_delay_ms'] = notify_cloud_delay_ms
        kwargs['notify_default_delay_ms'] = notify_default_delay_ms
        kwargs['push_chat_period_ms'] = push_chat_period_ms
        kwargs['push_chat_limit'] = push_chat_limit
        kwargs['edit_time_limit'] = edit_time_limit
        kwargs['revoke_time_limit'] = revoke_time_limit
        kwargs['revoke_pm_time_limit'] = revoke_pm_time_limit
        kwargs['rating_e_decay'] = rating_e_decay
        kwargs['stickers_recent_limit'] = stickers_recent_limit
        kwargs['channels_read_media_period'] = channels_read_media_period
        kwargs['call_receive_timeout_ms'] = call_receive_timeout_ms
        kwargs['call_ring_timeout_ms'] = call_ring_timeout_ms
        kwargs['call_connect_timeout_ms'] = call_connect_timeout_ms
        kwargs['call_packet_timeout_ms'] = call_packet_timeout_ms
        kwargs['me_url_prefix'] = me_url_prefix
        kwargs['caption_length_max'] = caption_length_max
        kwargs['message_length_max'] = message_length_max
        kwargs['webfile_dc_id'] = webfile_dc_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def default_p2p_contacts(self) -> Optional[bool]:
        return self['default_p2p_contacts']

    @property
    def preload_featured_stickers(self) -> Optional[bool]:
        return self['preload_featured_stickers']

    @property
    def revoke_pm_inbox(self) -> Optional[bool]:
        return self['revoke_pm_inbox']

    @property
    def blocked_mode(self) -> Optional[bool]:
        return self['blocked_mode']

    @property
    def force_try_ipv6(self) -> Optional[bool]:
        return self['force_try_ipv6']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def test_mode(self) -> bool:
        return self['test_mode']

    @property
    def this_dc(self) -> int:
        return self['this_dc']

    @property
    def dc_options(self) -> list[aliases.AnyDcOption]:
        return build_object(self['dc_options'])

    @property
    def dc_txt_domain_name(self) -> str:
        return self['dc_txt_domain_name']

    @property
    def chat_size_max(self) -> int:
        return self['chat_size_max']

    @property
    def megagroup_size_max(self) -> int:
        return self['megagroup_size_max']

    @property
    def forwarded_count_max(self) -> int:
        return self['forwarded_count_max']

    @property
    def online_update_period_ms(self) -> int:
        return self['online_update_period_ms']

    @property
    def offline_blur_timeout_ms(self) -> int:
        return self['offline_blur_timeout_ms']

    @property
    def offline_idle_timeout_ms(self) -> int:
        return self['offline_idle_timeout_ms']

    @property
    def online_cloud_timeout_ms(self) -> int:
        return self['online_cloud_timeout_ms']

    @property
    def notify_cloud_delay_ms(self) -> int:
        return self['notify_cloud_delay_ms']

    @property
    def notify_default_delay_ms(self) -> int:
        return self['notify_default_delay_ms']

    @property
    def push_chat_period_ms(self) -> int:
        return self['push_chat_period_ms']

    @property
    def push_chat_limit(self) -> int:
        return self['push_chat_limit']

    @property
    def edit_time_limit(self) -> int:
        return self['edit_time_limit']

    @property
    def revoke_time_limit(self) -> int:
        return self['revoke_time_limit']

    @property
    def revoke_pm_time_limit(self) -> int:
        return self['revoke_pm_time_limit']

    @property
    def rating_e_decay(self) -> int:
        return self['rating_e_decay']

    @property
    def stickers_recent_limit(self) -> int:
        return self['stickers_recent_limit']

    @property
    def channels_read_media_period(self) -> int:
        return self['channels_read_media_period']

    @property
    def tmp_sessions(self) -> Optional[int]:
        return self['tmp_sessions']

    @property
    def call_receive_timeout_ms(self) -> int:
        return self['call_receive_timeout_ms']

    @property
    def call_ring_timeout_ms(self) -> int:
        return self['call_ring_timeout_ms']

    @property
    def call_connect_timeout_ms(self) -> int:
        return self['call_connect_timeout_ms']

    @property
    def call_packet_timeout_ms(self) -> int:
        return self['call_packet_timeout_ms']

    @property
    def me_url_prefix(self) -> str:
        return self['me_url_prefix']

    @property
    def autoupdate_url_prefix(self) -> Optional[str]:
        return self['autoupdate_url_prefix']

    @property
    def gif_search_username(self) -> Optional[str]:
        return self['gif_search_username']

    @property
    def venue_search_username(self) -> Optional[str]:
        return self['venue_search_username']

    @property
    def img_search_username(self) -> Optional[str]:
        return self['img_search_username']

    @property
    def static_maps_provider(self) -> Optional[str]:
        return self['static_maps_provider']

    @property
    def caption_length_max(self) -> int:
        return self['caption_length_max']

    @property
    def message_length_max(self) -> int:
        return self['message_length_max']

    @property
    def webfile_dc_id(self) -> int:
        return self['webfile_dc_id']

    @property
    def suggested_lang_code(self) -> Optional[str]:
        return self['suggested_lang_code']

    @property
    def lang_pack_version(self) -> Optional[int]:
        return self['lang_pack_version']

    @property
    def base_lang_pack_version(self) -> Optional[int]:
        return self['base_lang_pack_version']

    @property
    def reactions_default(self) -> Optional[aliases.AnyReaction]:
        return build_object(self['reactions_default'])

    @property
    def autologin_token(self) -> Optional[str]:
        return self['autologin_token']


class NearestDc(dict):
    __slots__ = ()

    @overload
    def __init__(self, country: str, this_dc: int, nearest_dc: int): ...

    def __init__(self, country, this_dc, nearest_dc, _='nearestDc', **kwargs):
        kwargs['country'] = country
        kwargs['this_dc'] = this_dc
        kwargs['nearest_dc'] = nearest_dc
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def country(self) -> str:
        return self['country']

    @property
    def this_dc(self) -> int:
        return self['this_dc']

    @property
    def nearest_dc(self) -> int:
        return self['nearest_dc']


class EncryptedChatEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='encryptedChatEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class EncryptedChatWaiting(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, _='encryptedChatWaiting', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']


class EncryptedChatRequested(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a: bytes, folder_id: Optional[int] = ...): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, g_a, _='encryptedChatRequested', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['g_a'] = g_a
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> Optional[int]:
        return self['folder_id']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def g_a(self) -> bytes:
        return self['g_a']


class EncryptedChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, g_a_or_b, key_fingerprint, _='encryptedChat', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['g_a_or_b'] = g_a_or_b
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def g_a_or_b(self) -> bytes:
        return self['g_a_or_b']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']


class EncryptedChatDiscarded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, history_deleted: Optional[bool] = ...): ...

    def __init__(self, id, _='encryptedChatDiscarded', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def history_deleted(self) -> Optional[bool]:
        return self['history_deleted']

    @property
    def id(self) -> int:
        return self['id']


class InputEncryptedChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, access_hash: int): ...

    def __init__(self, chat_id, access_hash, _='inputEncryptedChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class EncryptedFileEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='encryptedFileEmpty'):
        dict.__init__(self, _=_)


class EncryptedFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, size: int, dc_id: int, key_fingerprint: int): ...

    def __init__(self, id, access_hash, size, dc_id, key_fingerprint, _='encryptedFile', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['size'] = size
        kwargs['dc_id'] = dc_id
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']


class InputEncryptedFileEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputEncryptedFileEmpty'):
        dict.__init__(self, _=_)


class InputEncryptedFileUploaded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, parts: int, md5_checksum: str, key_fingerprint: int): ...

    def __init__(self, id, parts, md5_checksum, key_fingerprint, _='inputEncryptedFileUploaded', **kwargs):
        kwargs['id'] = id
        kwargs['parts'] = parts
        kwargs['md5_checksum'] = md5_checksum
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def parts(self) -> int:
        return self['parts']

    @property
    def md5_checksum(self) -> str:
        return self['md5_checksum']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']


class InputEncryptedFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputEncryptedFile', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputEncryptedFileBigUploaded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, parts: int, key_fingerprint: int): ...

    def __init__(self, id, parts, key_fingerprint, _='inputEncryptedFileBigUploaded', **kwargs):
        kwargs['id'] = id
        kwargs['parts'] = parts
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def parts(self) -> int:
        return self['parts']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']


class EncryptedMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, random_id: int, chat_id: int, date: int, bytes: bytes, file: aliases.AnyEncryptedFile): ...

    def __init__(self, random_id, chat_id, date, bytes, file, _='encryptedMessage', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['chat_id'] = chat_id
        kwargs['date'] = date
        kwargs['bytes'] = bytes
        kwargs['file'] = file
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bytes(self) -> bytes:
        return self['bytes']

    @property
    def file(self) -> aliases.AnyEncryptedFile:
        return build_object(self['file'])


class EncryptedMessageService(dict):
    __slots__ = ()

    @overload
    def __init__(self, random_id: int, chat_id: int, date: int, bytes: bytes): ...

    def __init__(self, random_id, chat_id, date, bytes, _='encryptedMessageService', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['chat_id'] = chat_id
        kwargs['date'] = date
        kwargs['bytes'] = bytes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bytes(self) -> bytes:
        return self['bytes']


class InputDocumentEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputDocumentEmpty'):
        dict.__init__(self, _=_)


class InputDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes): ...

    def __init__(self, id, access_hash, file_reference, _='inputDocument', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']


class DocumentEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='documentEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class Document(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, file_reference: bytes, date: int, mime_type: str, size: int, dc_id: int, attributes: list[aliases.AnyDocumentAttribute], thumbs: Optional[list[aliases.AnyPhotoSize]] = ..., video_thumbs: Optional[list[aliases.AnyVideoSize]] = ...): ...

    def __init__(self, id, access_hash, file_reference, date, mime_type, size, dc_id, attributes, _='document', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['file_reference'] = file_reference
        kwargs['date'] = date
        kwargs['mime_type'] = mime_type
        kwargs['size'] = size
        kwargs['dc_id'] = dc_id
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def file_reference(self) -> bytes:
        return self['file_reference']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def thumbs(self) -> Optional[list[aliases.AnyPhotoSize]]:
        return build_object(self['thumbs'])

    @property
    def video_thumbs(self) -> Optional[list[aliases.AnyVideoSize]]:
        return build_object(self['video_thumbs'])

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def attributes(self) -> list[aliases.AnyDocumentAttribute]:
        return build_object(self['attributes'])


class NotifyPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer): ...

    def __init__(self, peer, _='notifyPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])


class NotifyUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='notifyUsers'):
        dict.__init__(self, _=_)


class NotifyChats(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='notifyChats'):
        dict.__init__(self, _=_)


class NotifyBroadcasts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='notifyBroadcasts'):
        dict.__init__(self, _=_)


class NotifyForumTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, top_msg_id: int): ...

    def __init__(self, peer, top_msg_id, _='notifyForumTopic', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_msg_id'] = top_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_msg_id(self) -> int:
        return self['top_msg_id']


class SendMessageTypingAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageTypingAction'):
        dict.__init__(self, _=_)


class SendMessageCancelAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageCancelAction'):
        dict.__init__(self, _=_)


class SendMessageRecordVideoAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageRecordVideoAction'):
        dict.__init__(self, _=_)


class SendMessageUploadVideoAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageUploadVideoAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SendMessageRecordAudioAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageRecordAudioAction'):
        dict.__init__(self, _=_)


class SendMessageUploadAudioAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageUploadAudioAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SendMessageUploadPhotoAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageUploadPhotoAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SendMessageUploadDocumentAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageUploadDocumentAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SendMessageGeoLocationAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageGeoLocationAction'):
        dict.__init__(self, _=_)


class SendMessageChooseContactAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageChooseContactAction'):
        dict.__init__(self, _=_)


class SendMessageGamePlayAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageGamePlayAction'):
        dict.__init__(self, _=_)


class SendMessageRecordRoundAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageRecordRoundAction'):
        dict.__init__(self, _=_)


class SendMessageUploadRoundAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageUploadRoundAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SpeakingInGroupCallAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='speakingInGroupCallAction'):
        dict.__init__(self, _=_)


class SendMessageHistoryImportAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, progress: int): ...

    def __init__(self, progress, _='sendMessageHistoryImportAction', **kwargs):
        kwargs['progress'] = progress
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def progress(self) -> int:
        return self['progress']


class SendMessageChooseStickerAction(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='sendMessageChooseStickerAction'):
        dict.__init__(self, _=_)


class SendMessageEmojiInteraction(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str, msg_id: int, interaction: aliases.AnyDataJSON): ...

    def __init__(self, emoticon, msg_id, interaction, _='sendMessageEmojiInteraction', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['msg_id'] = msg_id
        kwargs['interaction'] = interaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def interaction(self) -> aliases.AnyDataJSON:
        return build_object(self['interaction'])


class SendMessageEmojiInteractionSeen(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='sendMessageEmojiInteractionSeen', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class SendMessageTextDraftAction(dict):
    __slots__ = ()

    @overload
    def __init__(self, random_id: int, text: aliases.AnyTextWithEntities): ...

    def __init__(self, random_id, text, _='sendMessageTextDraftAction', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def text(self) -> aliases.AnyTextWithEntities:
        return build_object(self['text'])


class InputPrivacyKeyStatusTimestamp(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyStatusTimestamp'):
        dict.__init__(self, _=_)


class InputPrivacyKeyChatInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyChatInvite'):
        dict.__init__(self, _=_)


class InputPrivacyKeyPhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyPhoneCall'):
        dict.__init__(self, _=_)


class InputPrivacyKeyPhoneP2P(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyPhoneP2P'):
        dict.__init__(self, _=_)


class InputPrivacyKeyForwards(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyForwards'):
        dict.__init__(self, _=_)


class InputPrivacyKeyProfilePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyProfilePhoto'):
        dict.__init__(self, _=_)


class InputPrivacyKeyPhoneNumber(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyPhoneNumber'):
        dict.__init__(self, _=_)


class InputPrivacyKeyAddedByPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyAddedByPhone'):
        dict.__init__(self, _=_)


class InputPrivacyKeyVoiceMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyVoiceMessages'):
        dict.__init__(self, _=_)


class InputPrivacyKeyAbout(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyAbout'):
        dict.__init__(self, _=_)


class InputPrivacyKeyBirthday(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyBirthday'):
        dict.__init__(self, _=_)


class InputPrivacyKeyStarGiftsAutoSave(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyStarGiftsAutoSave'):
        dict.__init__(self, _=_)


class InputPrivacyKeyNoPaidMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeyNoPaidMessages'):
        dict.__init__(self, _=_)


class InputPrivacyKeySavedMusic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyKeySavedMusic'):
        dict.__init__(self, _=_)


class PrivacyKeyStatusTimestamp(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyStatusTimestamp'):
        dict.__init__(self, _=_)


class PrivacyKeyChatInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyChatInvite'):
        dict.__init__(self, _=_)


class PrivacyKeyPhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyPhoneCall'):
        dict.__init__(self, _=_)


class PrivacyKeyPhoneP2P(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyPhoneP2P'):
        dict.__init__(self, _=_)


class PrivacyKeyForwards(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyForwards'):
        dict.__init__(self, _=_)


class PrivacyKeyProfilePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyProfilePhoto'):
        dict.__init__(self, _=_)


class PrivacyKeyPhoneNumber(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyPhoneNumber'):
        dict.__init__(self, _=_)


class PrivacyKeyAddedByPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyAddedByPhone'):
        dict.__init__(self, _=_)


class PrivacyKeyVoiceMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyVoiceMessages'):
        dict.__init__(self, _=_)


class PrivacyKeyAbout(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyAbout'):
        dict.__init__(self, _=_)


class PrivacyKeyBirthday(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyBirthday'):
        dict.__init__(self, _=_)


class PrivacyKeyStarGiftsAutoSave(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyStarGiftsAutoSave'):
        dict.__init__(self, _=_)


class PrivacyKeyNoPaidMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeyNoPaidMessages'):
        dict.__init__(self, _=_)


class PrivacyKeySavedMusic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyKeySavedMusic'):
        dict.__init__(self, _=_)


class InputPrivacyValueAllowContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueAllowContacts'):
        dict.__init__(self, _=_)


class InputPrivacyValueAllowAll(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueAllowAll'):
        dict.__init__(self, _=_)


class InputPrivacyValueAllowUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyInputUser]): ...

    def __init__(self, users, _='inputPrivacyValueAllowUsers', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])


class InputPrivacyValueDisallowContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueDisallowContacts'):
        dict.__init__(self, _=_)


class InputPrivacyValueDisallowAll(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueDisallowAll'):
        dict.__init__(self, _=_)


class InputPrivacyValueDisallowUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyInputUser]): ...

    def __init__(self, users, _='inputPrivacyValueDisallowUsers', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])


class InputPrivacyValueAllowChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, chats: list[int]): ...

    def __init__(self, chats, _='inputPrivacyValueAllowChatParticipants', **kwargs):
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chats(self) -> list[int]:
        return self['chats']


class InputPrivacyValueDisallowChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, chats: list[int]): ...

    def __init__(self, chats, _='inputPrivacyValueDisallowChatParticipants', **kwargs):
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chats(self) -> list[int]:
        return self['chats']


class InputPrivacyValueAllowCloseFriends(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueAllowCloseFriends'):
        dict.__init__(self, _=_)


class InputPrivacyValueAllowPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueAllowPremium'):
        dict.__init__(self, _=_)


class InputPrivacyValueAllowBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueAllowBots'):
        dict.__init__(self, _=_)


class InputPrivacyValueDisallowBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputPrivacyValueDisallowBots'):
        dict.__init__(self, _=_)


class PrivacyValueAllowContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueAllowContacts'):
        dict.__init__(self, _=_)


class PrivacyValueAllowAll(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueAllowAll'):
        dict.__init__(self, _=_)


class PrivacyValueAllowUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[int]): ...

    def __init__(self, users, _='privacyValueAllowUsers', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[int]:
        return self['users']


class PrivacyValueDisallowContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueDisallowContacts'):
        dict.__init__(self, _=_)


class PrivacyValueDisallowAll(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueDisallowAll'):
        dict.__init__(self, _=_)


class PrivacyValueDisallowUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[int]): ...

    def __init__(self, users, _='privacyValueDisallowUsers', **kwargs):
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[int]:
        return self['users']


class PrivacyValueAllowChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, chats: list[int]): ...

    def __init__(self, chats, _='privacyValueAllowChatParticipants', **kwargs):
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chats(self) -> list[int]:
        return self['chats']


class PrivacyValueDisallowChatParticipants(dict):
    __slots__ = ()

    @overload
    def __init__(self, chats: list[int]): ...

    def __init__(self, chats, _='privacyValueDisallowChatParticipants', **kwargs):
        kwargs['chats'] = chats
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chats(self) -> list[int]:
        return self['chats']


class PrivacyValueAllowCloseFriends(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueAllowCloseFriends'):
        dict.__init__(self, _=_)


class PrivacyValueAllowPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueAllowPremium'):
        dict.__init__(self, _=_)


class PrivacyValueAllowBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueAllowBots'):
        dict.__init__(self, _=_)


class PrivacyValueDisallowBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='privacyValueDisallowBots'):
        dict.__init__(self, _=_)


class AccountDaysTTL(dict):
    __slots__ = ()

    @overload
    def __init__(self, days: int): ...

    def __init__(self, days, _='accountDaysTTL', **kwargs):
        kwargs['days'] = days
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def days(self) -> int:
        return self['days']


class DocumentAttributeImageSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, w: int, h: int): ...

    def __init__(self, w, h, _='documentAttributeImageSize', **kwargs):
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']


class DocumentAttributeAnimated(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='documentAttributeAnimated'):
        dict.__init__(self, _=_)


class DocumentAttributeSticker(dict):
    __slots__ = ()

    @overload
    def __init__(self, alt: str, stickerset: aliases.AnyInputStickerSet, mask: Optional[bool] = ..., mask_coords: Optional[aliases.AnyMaskCoords] = ...): ...

    def __init__(self, alt, stickerset, _='documentAttributeSticker', **kwargs):
        kwargs['alt'] = alt
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def mask(self) -> Optional[bool]:
        return self['mask']

    @property
    def alt(self) -> str:
        return self['alt']

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def mask_coords(self) -> Optional[aliases.AnyMaskCoords]:
        return build_object(self['mask_coords'])


class DocumentAttributeVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self, duration: float, w: int, h: int, round_message: Optional[bool] = ..., supports_streaming: Optional[bool] = ..., nosound: Optional[bool] = ..., preload_prefix_size: Optional[int] = ..., video_start_ts: Optional[float] = ..., video_codec: Optional[str] = ...): ...

    def __init__(self, duration, w, h, _='documentAttributeVideo', **kwargs):
        kwargs['duration'] = duration
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def round_message(self) -> Optional[bool]:
        return self['round_message']

    @property
    def supports_streaming(self) -> Optional[bool]:
        return self['supports_streaming']

    @property
    def nosound(self) -> Optional[bool]:
        return self['nosound']

    @property
    def duration(self) -> float:
        return self['duration']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def preload_prefix_size(self) -> Optional[int]:
        return self['preload_prefix_size']

    @property
    def video_start_ts(self) -> Optional[float]:
        return self['video_start_ts']

    @property
    def video_codec(self) -> Optional[str]:
        return self['video_codec']


class DocumentAttributeAudio(dict):
    __slots__ = ()

    @overload
    def __init__(self, duration: int, voice: Optional[bool] = ..., title: Optional[str] = ..., performer: Optional[str] = ..., waveform: Optional[bytes] = ...): ...

    def __init__(self, duration, _='documentAttributeAudio', **kwargs):
        kwargs['duration'] = duration
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def voice(self) -> Optional[bool]:
        return self['voice']

    @property
    def duration(self) -> int:
        return self['duration']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def performer(self) -> Optional[str]:
        return self['performer']

    @property
    def waveform(self) -> Optional[bytes]:
        return self['waveform']


class DocumentAttributeFilename(dict):
    __slots__ = ()

    @overload
    def __init__(self, file_name: str): ...

    def __init__(self, file_name, _='documentAttributeFilename', **kwargs):
        kwargs['file_name'] = file_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def file_name(self) -> str:
        return self['file_name']


class DocumentAttributeHasStickers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='documentAttributeHasStickers'):
        dict.__init__(self, _=_)


class DocumentAttributeCustomEmoji(dict):
    __slots__ = ()

    @overload
    def __init__(self, alt: str, stickerset: aliases.AnyInputStickerSet, free: Optional[bool] = ..., text_color: Optional[bool] = ...): ...

    def __init__(self, alt, stickerset, _='documentAttributeCustomEmoji', **kwargs):
        kwargs['alt'] = alt
        kwargs['stickerset'] = stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def free(self) -> Optional[bool]:
        return self['free']

    @property
    def text_color(self) -> Optional[bool]:
        return self['text_color']

    @property
    def alt(self) -> str:
        return self['alt']

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])


class StickerPack(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str, documents: list[int]): ...

    def __init__(self, emoticon, documents, _='stickerPack', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def documents(self) -> list[int]:
        return self['documents']


class WebPageEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, url: Optional[str] = ...): ...

    def __init__(self, id, _='webPageEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def url(self) -> Optional[str]:
        return self['url']


class WebPagePending(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, date: int, url: Optional[str] = ...): ...

    def __init__(self, id, date, _='webPagePending', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def date(self) -> int:
        return self['date']


class WebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, url: str, display_url: str, hash: int, has_large_media: Optional[bool] = ..., video_cover_photo: Optional[bool] = ..., type: Optional[str] = ..., site_name: Optional[str] = ..., title: Optional[str] = ..., description: Optional[str] = ..., photo: Optional[aliases.AnyPhoto] = ..., embed_url: Optional[str] = ..., embed_type: Optional[str] = ..., embed_width: Optional[int] = ..., embed_height: Optional[int] = ..., duration: Optional[int] = ..., author: Optional[str] = ..., document: Optional[aliases.AnyDocument] = ..., cached_page: Optional[aliases.AnyPage] = ..., attributes: Optional[list[aliases.AnyWebPageAttribute]] = ...): ...

    def __init__(self, id, url, display_url, hash, _='webPage', **kwargs):
        kwargs['id'] = id
        kwargs['url'] = url
        kwargs['display_url'] = display_url
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_large_media(self) -> Optional[bool]:
        return self['has_large_media']

    @property
    def video_cover_photo(self) -> Optional[bool]:
        return self['video_cover_photo']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def display_url(self) -> str:
        return self['display_url']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def type(self) -> Optional[str]:
        return self['type']

    @property
    def site_name(self) -> Optional[str]:
        return self['site_name']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])

    @property
    def embed_url(self) -> Optional[str]:
        return self['embed_url']

    @property
    def embed_type(self) -> Optional[str]:
        return self['embed_type']

    @property
    def embed_width(self) -> Optional[int]:
        return self['embed_width']

    @property
    def embed_height(self) -> Optional[int]:
        return self['embed_height']

    @property
    def duration(self) -> Optional[int]:
        return self['duration']

    @property
    def author(self) -> Optional[str]:
        return self['author']

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def cached_page(self) -> Optional[aliases.AnyPage]:
        return build_object(self['cached_page'])

    @property
    def attributes(self) -> Optional[list[aliases.AnyWebPageAttribute]]:
        return build_object(self['attributes'])


class WebPageNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self, cached_page_views: Optional[int] = ...): ...

    def __init__(self, _='webPageNotModified', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def cached_page_views(self) -> Optional[int]:
        return self['cached_page_views']


class Authorization(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, device_model: str, platform: str, system_version: str, api_id: int, app_name: str, app_version: str, date_created: int, date_active: int, ip: str, country: str, region: str, current: Optional[bool] = ..., official_app: Optional[bool] = ..., password_pending: Optional[bool] = ..., encrypted_requests_disabled: Optional[bool] = ..., call_requests_disabled: Optional[bool] = ..., unconfirmed: Optional[bool] = ...): ...

    def __init__(self, hash, device_model, platform, system_version, api_id, app_name, app_version, date_created, date_active, ip, country, region, _='authorization', **kwargs):
        kwargs['hash'] = hash
        kwargs['device_model'] = device_model
        kwargs['platform'] = platform
        kwargs['system_version'] = system_version
        kwargs['api_id'] = api_id
        kwargs['app_name'] = app_name
        kwargs['app_version'] = app_version
        kwargs['date_created'] = date_created
        kwargs['date_active'] = date_active
        kwargs['ip'] = ip
        kwargs['country'] = country
        kwargs['region'] = region
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def current(self) -> Optional[bool]:
        return self['current']

    @property
    def official_app(self) -> Optional[bool]:
        return self['official_app']

    @property
    def password_pending(self) -> Optional[bool]:
        return self['password_pending']

    @property
    def encrypted_requests_disabled(self) -> Optional[bool]:
        return self['encrypted_requests_disabled']

    @property
    def call_requests_disabled(self) -> Optional[bool]:
        return self['call_requests_disabled']

    @property
    def unconfirmed(self) -> Optional[bool]:
        return self['unconfirmed']

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def device_model(self) -> str:
        return self['device_model']

    @property
    def platform(self) -> str:
        return self['platform']

    @property
    def system_version(self) -> str:
        return self['system_version']

    @property
    def api_id(self) -> int:
        return self['api_id']

    @property
    def app_name(self) -> str:
        return self['app_name']

    @property
    def app_version(self) -> str:
        return self['app_version']

    @property
    def date_created(self) -> int:
        return self['date_created']

    @property
    def date_active(self) -> int:
        return self['date_active']

    @property
    def ip(self) -> str:
        return self['ip']

    @property
    def country(self) -> str:
        return self['country']

    @property
    def region(self) -> str:
        return self['region']


class ReceivedNotifyMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='receivedNotifyMessage', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class ChatInviteExported(dict):
    __slots__ = ()

    @overload
    def __init__(self, link: str, admin_id: int, date: int, revoked: Optional[bool] = ..., permanent: Optional[bool] = ..., request_needed: Optional[bool] = ..., start_date: Optional[int] = ..., expire_date: Optional[int] = ..., usage_limit: Optional[int] = ..., usage: Optional[int] = ..., requested: Optional[int] = ..., subscription_expired: Optional[int] = ..., title: Optional[str] = ..., subscription_pricing: Optional[aliases.AnyStarsSubscriptionPricing] = ...): ...

    def __init__(self, link, admin_id, date, _='chatInviteExported', **kwargs):
        kwargs['link'] = link
        kwargs['admin_id'] = admin_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoked(self) -> Optional[bool]:
        return self['revoked']

    @property
    def permanent(self) -> Optional[bool]:
        return self['permanent']

    @property
    def request_needed(self) -> Optional[bool]:
        return self['request_needed']

    @property
    def link(self) -> str:
        return self['link']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def start_date(self) -> Optional[int]:
        return self['start_date']

    @property
    def expire_date(self) -> Optional[int]:
        return self['expire_date']

    @property
    def usage_limit(self) -> Optional[int]:
        return self['usage_limit']

    @property
    def usage(self) -> Optional[int]:
        return self['usage']

    @property
    def requested(self) -> Optional[int]:
        return self['requested']

    @property
    def subscription_expired(self) -> Optional[int]:
        return self['subscription_expired']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def subscription_pricing(self) -> Optional[aliases.AnyStarsSubscriptionPricing]:
        return build_object(self['subscription_pricing'])


class ChatInvitePublicJoinRequests(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='chatInvitePublicJoinRequests'):
        dict.__init__(self, _=_)


class ChatInviteAlready(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat: aliases.AnyChat): ...

    def __init__(self, chat, _='chatInviteAlready', **kwargs):
        kwargs['chat'] = chat
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat(self) -> aliases.AnyChat:
        return build_object(self['chat'])


class ChatInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, photo: aliases.AnyPhoto, participants_count: int, color: int, channel: Optional[bool] = ..., broadcast: Optional[bool] = ..., public: Optional[bool] = ..., megagroup: Optional[bool] = ..., request_needed: Optional[bool] = ..., verified: Optional[bool] = ..., scam: Optional[bool] = ..., fake: Optional[bool] = ..., can_refulfill_subscription: Optional[bool] = ..., about: Optional[str] = ..., participants: Optional[list[aliases.AnyUser]] = ..., subscription_pricing: Optional[aliases.AnyStarsSubscriptionPricing] = ..., subscription_form_id: Optional[int] = ..., bot_verification: Optional[aliases.AnyBotVerification] = ...): ...

    def __init__(self, title, photo, participants_count, color, _='chatInvite', **kwargs):
        kwargs['title'] = title
        kwargs['photo'] = photo
        kwargs['participants_count'] = participants_count
        kwargs['color'] = color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> Optional[bool]:
        return self['channel']

    @property
    def broadcast(self) -> Optional[bool]:
        return self['broadcast']

    @property
    def public(self) -> Optional[bool]:
        return self['public']

    @property
    def megagroup(self) -> Optional[bool]:
        return self['megagroup']

    @property
    def request_needed(self) -> Optional[bool]:
        return self['request_needed']

    @property
    def verified(self) -> Optional[bool]:
        return self['verified']

    @property
    def scam(self) -> Optional[bool]:
        return self['scam']

    @property
    def fake(self) -> Optional[bool]:
        return self['fake']

    @property
    def can_refulfill_subscription(self) -> Optional[bool]:
        return self['can_refulfill_subscription']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def about(self) -> Optional[str]:
        return self['about']

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])

    @property
    def participants_count(self) -> int:
        return self['participants_count']

    @property
    def participants(self) -> Optional[list[aliases.AnyUser]]:
        return build_object(self['participants'])

    @property
    def color(self) -> int:
        return self['color']

    @property
    def subscription_pricing(self) -> Optional[aliases.AnyStarsSubscriptionPricing]:
        return build_object(self['subscription_pricing'])

    @property
    def subscription_form_id(self) -> Optional[int]:
        return self['subscription_form_id']

    @property
    def bot_verification(self) -> Optional[aliases.AnyBotVerification]:
        return build_object(self['bot_verification'])


class ChatInvitePeek(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat: aliases.AnyChat, expires: int): ...

    def __init__(self, chat, expires, _='chatInvitePeek', **kwargs):
        kwargs['chat'] = chat
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat(self) -> aliases.AnyChat:
        return build_object(self['chat'])

    @property
    def expires(self) -> int:
        return self['expires']


class InputStickerSetEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetEmpty'):
        dict.__init__(self, _=_)


class InputStickerSetID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputStickerSetID', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputStickerSetShortName(dict):
    __slots__ = ()

    @overload
    def __init__(self, short_name: str): ...

    def __init__(self, short_name, _='inputStickerSetShortName', **kwargs):
        kwargs['short_name'] = short_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def short_name(self) -> str:
        return self['short_name']


class InputStickerSetAnimatedEmoji(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetAnimatedEmoji'):
        dict.__init__(self, _=_)


class InputStickerSetDice(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='inputStickerSetDice', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class InputStickerSetAnimatedEmojiAnimations(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetAnimatedEmojiAnimations'):
        dict.__init__(self, _=_)


class InputStickerSetPremiumGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetPremiumGifts'):
        dict.__init__(self, _=_)


class InputStickerSetEmojiGenericAnimations(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetEmojiGenericAnimations'):
        dict.__init__(self, _=_)


class InputStickerSetEmojiDefaultStatuses(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetEmojiDefaultStatuses'):
        dict.__init__(self, _=_)


class InputStickerSetEmojiDefaultTopicIcons(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetEmojiDefaultTopicIcons'):
        dict.__init__(self, _=_)


class InputStickerSetEmojiChannelDefaultStatuses(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetEmojiChannelDefaultStatuses'):
        dict.__init__(self, _=_)


class InputStickerSetTonGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputStickerSetTonGifts'):
        dict.__init__(self, _=_)


class StickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, title: str, short_name: str, count: int, hash: int, archived: Optional[bool] = ..., official: Optional[bool] = ..., masks: Optional[bool] = ..., emojis: Optional[bool] = ..., text_color: Optional[bool] = ..., channel_emoji_status: Optional[bool] = ..., creator: Optional[bool] = ..., installed_date: Optional[int] = ..., thumbs: Optional[list[aliases.AnyPhotoSize]] = ..., thumb_dc_id: Optional[int] = ..., thumb_version: Optional[int] = ..., thumb_document_id: Optional[int] = ...): ...

    def __init__(self, id, access_hash, title, short_name, count, hash, _='stickerSet', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['title'] = title
        kwargs['short_name'] = short_name
        kwargs['count'] = count
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def archived(self) -> Optional[bool]:
        return self['archived']

    @property
    def official(self) -> Optional[bool]:
        return self['official']

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
    def channel_emoji_status(self) -> Optional[bool]:
        return self['channel_emoji_status']

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def installed_date(self) -> Optional[int]:
        return self['installed_date']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def thumbs(self) -> Optional[list[aliases.AnyPhotoSize]]:
        return build_object(self['thumbs'])

    @property
    def thumb_dc_id(self) -> Optional[int]:
        return self['thumb_dc_id']

    @property
    def thumb_version(self) -> Optional[int]:
        return self['thumb_version']

    @property
    def thumb_document_id(self) -> Optional[int]:
        return self['thumb_document_id']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def hash(self) -> int:
        return self['hash']


class BotCommand(dict):
    __slots__ = ()

    @overload
    def __init__(self, command: str, description: str): ...

    def __init__(self, command, description, _='botCommand', **kwargs):
        kwargs['command'] = command
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def command(self) -> str:
        return self['command']

    @property
    def description(self) -> str:
        return self['description']


class BotInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, has_preview_medias: Optional[bool] = ..., user_id: Optional[int] = ..., description: Optional[str] = ..., description_photo: Optional[aliases.AnyPhoto] = ..., description_document: Optional[aliases.AnyDocument] = ..., commands: Optional[list[aliases.AnyBotCommand]] = ..., menu_button: Optional[aliases.AnyBotMenuButton] = ..., privacy_policy_url: Optional[str] = ..., app_settings: Optional[aliases.AnyBotAppSettings] = ..., verifier_settings: Optional[aliases.AnyBotVerifierSettings] = ...): ...

    def __init__(self, _='botInfo', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_preview_medias(self) -> Optional[bool]:
        return self['has_preview_medias']

    @property
    def user_id(self) -> Optional[int]:
        return self['user_id']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def description_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['description_photo'])

    @property
    def description_document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['description_document'])

    @property
    def commands(self) -> Optional[list[aliases.AnyBotCommand]]:
        return build_object(self['commands'])

    @property
    def menu_button(self) -> Optional[aliases.AnyBotMenuButton]:
        return build_object(self['menu_button'])

    @property
    def privacy_policy_url(self) -> Optional[str]:
        return self['privacy_policy_url']

    @property
    def app_settings(self) -> Optional[aliases.AnyBotAppSettings]:
        return build_object(self['app_settings'])

    @property
    def verifier_settings(self) -> Optional[aliases.AnyBotVerifierSettings]:
        return build_object(self['verifier_settings'])


class KeyboardButton(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, _='keyboardButton', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']


class KeyboardButtonUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, url, _='keyboardButtonUrl', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def url(self) -> str:
        return self['url']


class KeyboardButtonCallback(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, data: bytes, requires_password: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, data, _='keyboardButtonCallback', **kwargs):
        kwargs['text'] = text
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def requires_password(self) -> Optional[bool]:
        return self['requires_password']

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def data(self) -> bytes:
        return self['data']


class KeyboardButtonRequestPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, _='keyboardButtonRequestPhone', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']


class KeyboardButtonRequestGeoLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, _='keyboardButtonRequestGeoLocation', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']


class KeyboardButtonSwitchInline(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, query: str, same_peer: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ..., peer_types: Optional[list[aliases.AnyInlineQueryPeerType]] = ...): ...

    def __init__(self, text, query, _='keyboardButtonSwitchInline', **kwargs):
        kwargs['text'] = text
        kwargs['query'] = query
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def same_peer(self) -> Optional[bool]:
        return self['same_peer']

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def query(self) -> str:
        return self['query']

    @property
    def peer_types(self) -> Optional[list[aliases.AnyInlineQueryPeerType]]:
        return build_object(self['peer_types'])


class KeyboardButtonGame(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, _='keyboardButtonGame', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']


class KeyboardButtonBuy(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, _='keyboardButtonBuy', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']


class KeyboardButtonUrlAuth(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str, button_id: int, style: Optional[aliases.AnyKeyboardButtonStyle] = ..., fwd_text: Optional[str] = ...): ...

    def __init__(self, text, url, button_id, _='keyboardButtonUrlAuth', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['button_id'] = button_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def fwd_text(self) -> Optional[str]:
        return self['fwd_text']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def button_id(self) -> int:
        return self['button_id']


class InputKeyboardButtonUrlAuth(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str, bot: aliases.AnyInputUser, request_write_access: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ..., fwd_text: Optional[str] = ...): ...

    def __init__(self, text, url, bot, _='inputKeyboardButtonUrlAuth', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['bot'] = bot
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def request_write_access(self) -> Optional[bool]:
        return self['request_write_access']

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def fwd_text(self) -> Optional[str]:
        return self['fwd_text']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])


class KeyboardButtonRequestPoll(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ..., quiz: Optional[bool] = ...): ...

    def __init__(self, text, _='keyboardButtonRequestPoll', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def quiz(self) -> Optional[bool]:
        return self['quiz']

    @property
    def text(self) -> str:
        return self['text']


class InputKeyboardButtonUserProfile(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, user_id: aliases.AnyInputUser, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, user_id, _='inputKeyboardButtonUserProfile', **kwargs):
        kwargs['text'] = text
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class KeyboardButtonUserProfile(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, user_id: int, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, user_id, _='keyboardButtonUserProfile', **kwargs):
        kwargs['text'] = text
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def user_id(self) -> int:
        return self['user_id']


class KeyboardButtonWebView(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, url, _='keyboardButtonWebView', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def url(self) -> str:
        return self['url']


class KeyboardButtonSimpleWebView(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, url, _='keyboardButtonSimpleWebView', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def url(self) -> str:
        return self['url']


class KeyboardButtonRequestPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, button_id: int, peer_type: aliases.AnyRequestPeerType, max_quantity: int, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, button_id, peer_type, max_quantity, _='keyboardButtonRequestPeer', **kwargs):
        kwargs['text'] = text
        kwargs['button_id'] = button_id
        kwargs['peer_type'] = peer_type
        kwargs['max_quantity'] = max_quantity
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def button_id(self) -> int:
        return self['button_id']

    @property
    def peer_type(self) -> aliases.AnyRequestPeerType:
        return build_object(self['peer_type'])

    @property
    def max_quantity(self) -> int:
        return self['max_quantity']


class InputKeyboardButtonRequestPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, button_id: int, peer_type: aliases.AnyRequestPeerType, max_quantity: int, name_requested: Optional[bool] = ..., username_requested: Optional[bool] = ..., photo_requested: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, button_id, peer_type, max_quantity, _='inputKeyboardButtonRequestPeer', **kwargs):
        kwargs['text'] = text
        kwargs['button_id'] = button_id
        kwargs['peer_type'] = peer_type
        kwargs['max_quantity'] = max_quantity
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name_requested(self) -> Optional[bool]:
        return self['name_requested']

    @property
    def username_requested(self) -> Optional[bool]:
        return self['username_requested']

    @property
    def photo_requested(self) -> Optional[bool]:
        return self['photo_requested']

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def button_id(self) -> int:
        return self['button_id']

    @property
    def peer_type(self) -> aliases.AnyRequestPeerType:
        return build_object(self['peer_type'])

    @property
    def max_quantity(self) -> int:
        return self['max_quantity']


class KeyboardButtonCopy(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, copy_text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def __init__(self, text, copy_text, _='keyboardButtonCopy', **kwargs):
        kwargs['text'] = text
        kwargs['copy_text'] = copy_text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def style(self) -> Optional[aliases.AnyKeyboardButtonStyle]:
        return build_object(self['style'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def copy_text(self) -> str:
        return self['copy_text']


class KeyboardButtonRow(dict):
    __slots__ = ()

    @overload
    def __init__(self, buttons: list[aliases.AnyKeyboardButton]): ...

    def __init__(self, buttons, _='keyboardButtonRow', **kwargs):
        kwargs['buttons'] = buttons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def buttons(self) -> list[aliases.AnyKeyboardButton]:
        return build_object(self['buttons'])


class ReplyKeyboardHide(dict):
    __slots__ = ()

    @overload
    def __init__(self, selective: Optional[bool] = ...): ...

    def __init__(self, _='replyKeyboardHide', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def selective(self) -> Optional[bool]:
        return self['selective']


class ReplyKeyboardForceReply(dict):
    __slots__ = ()

    @overload
    def __init__(self, single_use: Optional[bool] = ..., selective: Optional[bool] = ..., placeholder: Optional[str] = ...): ...

    def __init__(self, _='replyKeyboardForceReply', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def single_use(self) -> Optional[bool]:
        return self['single_use']

    @property
    def selective(self) -> Optional[bool]:
        return self['selective']

    @property
    def placeholder(self) -> Optional[str]:
        return self['placeholder']


class ReplyKeyboardMarkup(dict):
    __slots__ = ()

    @overload
    def __init__(self, rows: list[aliases.AnyKeyboardButtonRow], resize: Optional[bool] = ..., single_use: Optional[bool] = ..., selective: Optional[bool] = ..., persistent: Optional[bool] = ..., placeholder: Optional[str] = ...): ...

    def __init__(self, rows, _='replyKeyboardMarkup', **kwargs):
        kwargs['rows'] = rows
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def resize(self) -> Optional[bool]:
        return self['resize']

    @property
    def single_use(self) -> Optional[bool]:
        return self['single_use']

    @property
    def selective(self) -> Optional[bool]:
        return self['selective']

    @property
    def persistent(self) -> Optional[bool]:
        return self['persistent']

    @property
    def rows(self) -> list[aliases.AnyKeyboardButtonRow]:
        return build_object(self['rows'])

    @property
    def placeholder(self) -> Optional[str]:
        return self['placeholder']


class ReplyInlineMarkup(dict):
    __slots__ = ()

    @overload
    def __init__(self, rows: list[aliases.AnyKeyboardButtonRow]): ...

    def __init__(self, rows, _='replyInlineMarkup', **kwargs):
        kwargs['rows'] = rows
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def rows(self) -> list[aliases.AnyKeyboardButtonRow]:
        return build_object(self['rows'])


class MessageEntityUnknown(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityUnknown', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityMention(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityMention', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityHashtag(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityHashtag', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityBotCommand(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityBotCommand', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityUrl', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityEmail(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityEmail', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityBold(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityBold', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityItalic(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityItalic', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityCode', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityPre(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, language: str): ...

    def __init__(self, offset, length, language, _='messageEntityPre', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['language'] = language
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def language(self) -> str:
        return self['language']


class MessageEntityTextUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, url: str): ...

    def __init__(self, offset, length, url, _='messageEntityTextUrl', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def url(self) -> str:
        return self['url']


class MessageEntityMentionName(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, user_id: int): ...

    def __init__(self, offset, length, user_id, _='messageEntityMentionName', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def user_id(self) -> int:
        return self['user_id']


class InputMessageEntityMentionName(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, user_id: aliases.AnyInputUser): ...

    def __init__(self, offset, length, user_id, _='inputMessageEntityMentionName', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class MessageEntityPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityPhone', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityCashtag(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityCashtag', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityUnderline(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityUnderline', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityStrike(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityStrike', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityBankCard(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntityBankCard', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntitySpoiler(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int): ...

    def __init__(self, offset, length, _='messageEntitySpoiler', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityCustomEmoji(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, document_id: int): ...

    def __init__(self, offset, length, document_id, _='messageEntityCustomEmoji', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def document_id(self) -> int:
        return self['document_id']


class MessageEntityBlockquote(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, collapsed: Optional[bool] = ...): ...

    def __init__(self, offset, length, _='messageEntityBlockquote', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collapsed(self) -> Optional[bool]:
        return self['collapsed']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']


class MessageEntityFormattedDate(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, length: int, date: int, relative: Optional[bool] = ..., short_time: Optional[bool] = ..., long_time: Optional[bool] = ..., short_date: Optional[bool] = ..., long_date: Optional[bool] = ..., day_of_week: Optional[bool] = ...): ...

    def __init__(self, offset, length, date, _='messageEntityFormattedDate', **kwargs):
        kwargs['offset'] = offset
        kwargs['length'] = length
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def relative(self) -> Optional[bool]:
        return self['relative']

    @property
    def short_time(self) -> Optional[bool]:
        return self['short_time']

    @property
    def long_time(self) -> Optional[bool]:
        return self['long_time']

    @property
    def short_date(self) -> Optional[bool]:
        return self['short_date']

    @property
    def long_date(self) -> Optional[bool]:
        return self['long_date']

    @property
    def day_of_week(self) -> Optional[bool]:
        return self['day_of_week']

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def length(self) -> int:
        return self['length']

    @property
    def date(self) -> int:
        return self['date']


class InputChannelEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputChannelEmpty'):
        dict.__init__(self, _=_)


class InputChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, access_hash: int): ...

    def __init__(self, channel_id, access_hash, _='inputChannel', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputChannelFromMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int, channel_id: int): ...

    def __init__(self, peer, msg_id, channel_id, _='inputChannelFromMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def channel_id(self) -> int:
        return self['channel_id']


class MessageRange(dict):
    __slots__ = ()

    @overload
    def __init__(self, min_id: int, max_id: int): ...

    def __init__(self, min_id, max_id, _='messageRange', **kwargs):
        kwargs['min_id'] = min_id
        kwargs['max_id'] = max_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def min_id(self) -> int:
        return self['min_id']

    @property
    def max_id(self) -> int:
        return self['max_id']


class ChannelMessagesFilterEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelMessagesFilterEmpty'):
        dict.__init__(self, _=_)


class ChannelMessagesFilter(dict):
    __slots__ = ()

    @overload
    def __init__(self, ranges: list[aliases.AnyMessageRange], exclude_new_messages: Optional[bool] = ...): ...

    def __init__(self, ranges, _='channelMessagesFilter', **kwargs):
        kwargs['ranges'] = ranges
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def exclude_new_messages(self) -> Optional[bool]:
        return self['exclude_new_messages']

    @property
    def ranges(self) -> list[aliases.AnyMessageRange]:
        return build_object(self['ranges'])


class ChannelParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, date: int, subscription_until_date: Optional[int] = ..., rank: Optional[str] = ...): ...

    def __init__(self, user_id, date, _='channelParticipant', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def subscription_until_date(self) -> Optional[int]:
        return self['subscription_until_date']

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelParticipantSelf(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, inviter_id: int, date: int, via_request: Optional[bool] = ..., subscription_until_date: Optional[int] = ..., rank: Optional[str] = ...): ...

    def __init__(self, user_id, inviter_id, date, _='channelParticipantSelf', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['inviter_id'] = inviter_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_request(self) -> Optional[bool]:
        return self['via_request']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def inviter_id(self) -> int:
        return self['inviter_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def subscription_until_date(self) -> Optional[int]:
        return self['subscription_until_date']

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelParticipantCreator(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, admin_rights: aliases.AnyChatAdminRights, rank: Optional[str] = ...): ...

    def __init__(self, user_id, admin_rights, _='channelParticipantCreator', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['admin_rights'] = admin_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def admin_rights(self) -> aliases.AnyChatAdminRights:
        return build_object(self['admin_rights'])

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelParticipantAdmin(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, promoted_by: int, date: int, admin_rights: aliases.AnyChatAdminRights, can_edit: Optional[bool] = ..., self_: Optional[bool] = ..., inviter_id: Optional[int] = ..., rank: Optional[str] = ...): ...

    def __init__(self, user_id, promoted_by, date, admin_rights, _='channelParticipantAdmin', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['promoted_by'] = promoted_by
        kwargs['date'] = date
        kwargs['admin_rights'] = admin_rights
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_edit(self) -> Optional[bool]:
        return self['can_edit']

    @property
    def self_(self) -> Optional[bool]:
        return self['self']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def inviter_id(self) -> Optional[int]:
        return self['inviter_id']

    @property
    def promoted_by(self) -> int:
        return self['promoted_by']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_rights(self) -> aliases.AnyChatAdminRights:
        return build_object(self['admin_rights'])

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelParticipantBanned(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, kicked_by: int, date: int, banned_rights: aliases.AnyChatBannedRights, left: Optional[bool] = ..., rank: Optional[str] = ...): ...

    def __init__(self, peer, kicked_by, date, banned_rights, _='channelParticipantBanned', **kwargs):
        kwargs['peer'] = peer
        kwargs['kicked_by'] = kicked_by
        kwargs['date'] = date
        kwargs['banned_rights'] = banned_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def left(self) -> Optional[bool]:
        return self['left']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def kicked_by(self) -> int:
        return self['kicked_by']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['banned_rights'])

    @property
    def rank(self) -> Optional[str]:
        return self['rank']


class ChannelParticipantLeft(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer): ...

    def __init__(self, peer, _='channelParticipantLeft', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])


class ChannelParticipantsRecent(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelParticipantsRecent'):
        dict.__init__(self, _=_)


class ChannelParticipantsAdmins(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelParticipantsAdmins'):
        dict.__init__(self, _=_)


class ChannelParticipantsKicked(dict):
    __slots__ = ()

    @overload
    def __init__(self, q: str): ...

    def __init__(self, q, _='channelParticipantsKicked', **kwargs):
        kwargs['q'] = q
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']


class ChannelParticipantsBots(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelParticipantsBots'):
        dict.__init__(self, _=_)


class ChannelParticipantsBanned(dict):
    __slots__ = ()

    @overload
    def __init__(self, q: str): ...

    def __init__(self, q, _='channelParticipantsBanned', **kwargs):
        kwargs['q'] = q
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']


class ChannelParticipantsSearch(dict):
    __slots__ = ()

    @overload
    def __init__(self, q: str): ...

    def __init__(self, q, _='channelParticipantsSearch', **kwargs):
        kwargs['q'] = q
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']


class ChannelParticipantsContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self, q: str): ...

    def __init__(self, q, _='channelParticipantsContacts', **kwargs):
        kwargs['q'] = q
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> str:
        return self['q']


class ChannelParticipantsMentions(dict):
    __slots__ = ()

    @overload
    def __init__(self, q: Optional[str] = ..., top_msg_id: Optional[int] = ...): ...

    def __init__(self, _='channelParticipantsMentions', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def q(self) -> Optional[str]:
        return self['q']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']


class InputBotInlineMessageMediaAuto(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, invert_media: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, _='inputBotInlineMessageMediaAuto', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageText(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, _='inputBotInlineMessageText', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageMediaGeo(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, heading: Optional[int] = ..., period: Optional[int] = ..., proximity_notification_radius: Optional[int] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, geo_point, _='inputBotInlineMessageMediaGeo', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def heading(self) -> Optional[int]:
        return self['heading']

    @property
    def period(self) -> Optional[int]:
        return self['period']

    @property
    def proximity_notification_radius(self) -> Optional[int]:
        return self['proximity_notification_radius']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageMediaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, geo_point, title, address, provider, venue_id, venue_type, _='inputBotInlineMessageMediaVenue', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['title'] = title
        kwargs['address'] = address
        kwargs['provider'] = provider
        kwargs['venue_id'] = venue_id
        kwargs['venue_type'] = venue_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def address(self) -> str:
        return self['address']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def venue_id(self) -> str:
        return self['venue_id']

    @property
    def venue_type(self) -> str:
        return self['venue_type']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageMediaContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, phone_number, first_name, last_name, vcard, _='inputBotInlineMessageMediaContact', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['vcard'] = vcard
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def vcard(self) -> str:
        return self['vcard']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageGame(dict):
    __slots__ = ()

    @overload
    def __init__(self, reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, _='inputBotInlineMessageGame', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageMediaInvoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, invoice: aliases.AnyInvoice, payload: bytes, provider: str, provider_data: aliases.AnyDataJSON, photo: Optional[aliases.AnyInputWebDocument] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, title, description, invoice, payload, provider, provider_data, _='inputBotInlineMessageMediaInvoice', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['invoice'] = invoice
        kwargs['payload'] = payload
        kwargs['provider'] = provider
        kwargs['provider_data'] = provider_data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyInputWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice(self) -> aliases.AnyInvoice:
        return build_object(self['invoice'])

    @property
    def payload(self) -> bytes:
        return self['payload']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def provider_data(self) -> aliases.AnyDataJSON:
        return build_object(self['provider_data'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineMessageMediaWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, url: str, invert_media: Optional[bool] = ..., force_large_media: Optional[bool] = ..., force_small_media: Optional[bool] = ..., optional: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, url, _='inputBotInlineMessageMediaWebPage', **kwargs):
        kwargs['message'] = message
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def force_large_media(self) -> Optional[bool]:
        return self['force_large_media']

    @property
    def force_small_media(self) -> Optional[bool]:
        return self['force_small_media']

    @property
    def optional(self) -> Optional[bool]:
        return self['optional']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def url(self) -> str:
        return self['url']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class InputBotInlineResult(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, type: str, send_message: aliases.AnyInputBotInlineMessage, title: Optional[str] = ..., description: Optional[str] = ..., url: Optional[str] = ..., thumb: Optional[aliases.AnyInputWebDocument] = ..., content: Optional[aliases.AnyInputWebDocument] = ...): ...

    def __init__(self, id, type, send_message, _='inputBotInlineResult', **kwargs):
        kwargs['id'] = id
        kwargs['type'] = type
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def thumb(self) -> Optional[aliases.AnyInputWebDocument]:
        return build_object(self['thumb'])

    @property
    def content(self) -> Optional[aliases.AnyInputWebDocument]:
        return build_object(self['content'])

    @property
    def send_message(self) -> aliases.AnyInputBotInlineMessage:
        return build_object(self['send_message'])


class InputBotInlineResultPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, type: str, photo: aliases.AnyInputPhoto, send_message: aliases.AnyInputBotInlineMessage): ...

    def __init__(self, id, type, photo, send_message, _='inputBotInlineResultPhoto', **kwargs):
        kwargs['id'] = id
        kwargs['type'] = type
        kwargs['photo'] = photo
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def photo(self) -> aliases.AnyInputPhoto:
        return build_object(self['photo'])

    @property
    def send_message(self) -> aliases.AnyInputBotInlineMessage:
        return build_object(self['send_message'])


class InputBotInlineResultDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, type: str, document: aliases.AnyInputDocument, send_message: aliases.AnyInputBotInlineMessage, title: Optional[str] = ..., description: Optional[str] = ...): ...

    def __init__(self, id, type, document, send_message, _='inputBotInlineResultDocument', **kwargs):
        kwargs['id'] = id
        kwargs['type'] = type
        kwargs['document'] = document
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def document(self) -> aliases.AnyInputDocument:
        return build_object(self['document'])

    @property
    def send_message(self) -> aliases.AnyInputBotInlineMessage:
        return build_object(self['send_message'])


class InputBotInlineResultGame(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, short_name: str, send_message: aliases.AnyInputBotInlineMessage): ...

    def __init__(self, id, short_name, send_message, _='inputBotInlineResultGame', **kwargs):
        kwargs['id'] = id
        kwargs['short_name'] = short_name
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def send_message(self) -> aliases.AnyInputBotInlineMessage:
        return build_object(self['send_message'])


class BotInlineMessageMediaAuto(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, invert_media: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, _='botInlineMessageMediaAuto', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageText(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, _='botInlineMessageText', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageMediaGeo(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint, heading: Optional[int] = ..., period: Optional[int] = ..., proximity_notification_radius: Optional[int] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, geo, _='botInlineMessageMediaGeo', **kwargs):
        kwargs['geo'] = geo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def heading(self) -> Optional[int]:
        return self['heading']

    @property
    def period(self) -> Optional[int]:
        return self['period']

    @property
    def proximity_notification_radius(self) -> Optional[int]:
        return self['proximity_notification_radius']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageMediaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint, title: str, address: str, provider: str, venue_id: str, venue_type: str, reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, geo, title, address, provider, venue_id, venue_type, _='botInlineMessageMediaVenue', **kwargs):
        kwargs['geo'] = geo
        kwargs['title'] = title
        kwargs['address'] = address
        kwargs['provider'] = provider
        kwargs['venue_id'] = venue_id
        kwargs['venue_type'] = venue_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def address(self) -> str:
        return self['address']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def venue_id(self) -> str:
        return self['venue_id']

    @property
    def venue_type(self) -> str:
        return self['venue_type']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageMediaContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, first_name: str, last_name: str, vcard: str, reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, phone_number, first_name, last_name, vcard, _='botInlineMessageMediaContact', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['vcard'] = vcard
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def vcard(self) -> str:
        return self['vcard']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageMediaInvoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, currency: str, total_amount: int, shipping_address_requested: Optional[bool] = ..., test: Optional[bool] = ..., photo: Optional[aliases.AnyWebDocument] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, title, description, currency, total_amount, _='botInlineMessageMediaInvoice', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['currency'] = currency
        kwargs['total_amount'] = total_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shipping_address_requested(self) -> Optional[bool]:
        return self['shipping_address_requested']

    @property
    def test(self) -> Optional[bool]:
        return self['test']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def total_amount(self) -> int:
        return self['total_amount']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineMessageMediaWebPage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, url: str, invert_media: Optional[bool] = ..., force_large_media: Optional[bool] = ..., force_small_media: Optional[bool] = ..., manual: Optional[bool] = ..., safe: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., reply_markup: Optional[aliases.AnyReplyMarkup] = ...): ...

    def __init__(self, message, url, _='botInlineMessageMediaWebPage', **kwargs):
        kwargs['message'] = message
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def force_large_media(self) -> Optional[bool]:
        return self['force_large_media']

    @property
    def force_small_media(self) -> Optional[bool]:
        return self['force_small_media']

    @property
    def manual(self) -> Optional[bool]:
        return self['manual']

    @property
    def safe(self) -> Optional[bool]:
        return self['safe']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def url(self) -> str:
        return self['url']

    @property
    def reply_markup(self) -> Optional[aliases.AnyReplyMarkup]:
        return build_object(self['reply_markup'])


class BotInlineResult(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, type: str, send_message: aliases.AnyBotInlineMessage, title: Optional[str] = ..., description: Optional[str] = ..., url: Optional[str] = ..., thumb: Optional[aliases.AnyWebDocument] = ..., content: Optional[aliases.AnyWebDocument] = ...): ...

    def __init__(self, id, type, send_message, _='botInlineResult', **kwargs):
        kwargs['id'] = id
        kwargs['type'] = type
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def thumb(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['thumb'])

    @property
    def content(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['content'])

    @property
    def send_message(self) -> aliases.AnyBotInlineMessage:
        return build_object(self['send_message'])


class BotInlineMediaResult(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, type: str, send_message: aliases.AnyBotInlineMessage, photo: Optional[aliases.AnyPhoto] = ..., document: Optional[aliases.AnyDocument] = ..., title: Optional[str] = ..., description: Optional[str] = ...): ...

    def __init__(self, id, type, send_message, _='botInlineMediaResult', **kwargs):
        kwargs['id'] = id
        kwargs['type'] = type
        kwargs['send_message'] = send_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def send_message(self) -> aliases.AnyBotInlineMessage:
        return build_object(self['send_message'])


class ExportedMessageLink(dict):
    __slots__ = ()

    @overload
    def __init__(self, link: str, html: str): ...

    def __init__(self, link, html, _='exportedMessageLink', **kwargs):
        kwargs['link'] = link
        kwargs['html'] = html
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def link(self) -> str:
        return self['link']

    @property
    def html(self) -> str:
        return self['html']


class MessageFwdHeader(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, imported: Optional[bool] = ..., saved_out: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., from_name: Optional[str] = ..., channel_post: Optional[int] = ..., post_author: Optional[str] = ..., saved_from_peer: Optional[aliases.AnyPeer] = ..., saved_from_msg_id: Optional[int] = ..., saved_from_id: Optional[aliases.AnyPeer] = ..., saved_from_name: Optional[str] = ..., saved_date: Optional[int] = ..., psa_type: Optional[str] = ...): ...

    def __init__(self, date, _='messageFwdHeader', **kwargs):
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def imported(self) -> Optional[bool]:
        return self['imported']

    @property
    def saved_out(self) -> Optional[bool]:
        return self['saved_out']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def from_name(self) -> Optional[str]:
        return self['from_name']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def channel_post(self) -> Optional[int]:
        return self['channel_post']

    @property
    def post_author(self) -> Optional[str]:
        return self['post_author']

    @property
    def saved_from_peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_from_peer'])

    @property
    def saved_from_msg_id(self) -> Optional[int]:
        return self['saved_from_msg_id']

    @property
    def saved_from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['saved_from_id'])

    @property
    def saved_from_name(self) -> Optional[str]:
        return self['saved_from_name']

    @property
    def saved_date(self) -> Optional[int]:
        return self['saved_date']

    @property
    def psa_type(self) -> Optional[str]:
        return self['psa_type']


class InputBotInlineMessageID(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int, id: int, access_hash: int): ...

    def __init__(self, dc_id, id, access_hash, _='inputBotInlineMessageID', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputBotInlineMessageID64(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int, owner_id: int, id: int, access_hash: int): ...

    def __init__(self, dc_id, owner_id, id, access_hash, _='inputBotInlineMessageID64', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['owner_id'] = owner_id
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def owner_id(self) -> int:
        return self['owner_id']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InlineBotSwitchPM(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, start_param: str): ...

    def __init__(self, text, start_param, _='inlineBotSwitchPM', **kwargs):
        kwargs['text'] = text
        kwargs['start_param'] = start_param
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def start_param(self) -> str:
        return self['start_param']


class TopPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, rating: float): ...

    def __init__(self, peer, rating, _='topPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['rating'] = rating
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def rating(self) -> float:
        return self['rating']


class TopPeerCategoryBotsPM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryBotsPM'):
        dict.__init__(self, _=_)


class TopPeerCategoryBotsInline(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryBotsInline'):
        dict.__init__(self, _=_)


class TopPeerCategoryCorrespondents(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryCorrespondents'):
        dict.__init__(self, _=_)


class TopPeerCategoryGroups(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryGroups'):
        dict.__init__(self, _=_)


class TopPeerCategoryChannels(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryChannels'):
        dict.__init__(self, _=_)


class TopPeerCategoryPhoneCalls(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryPhoneCalls'):
        dict.__init__(self, _=_)


class TopPeerCategoryForwardUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryForwardUsers'):
        dict.__init__(self, _=_)


class TopPeerCategoryForwardChats(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryForwardChats'):
        dict.__init__(self, _=_)


class TopPeerCategoryBotsApp(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='topPeerCategoryBotsApp'):
        dict.__init__(self, _=_)


class TopPeerCategoryPeers(dict):
    __slots__ = ()

    @overload
    def __init__(self, category: aliases.AnyTopPeerCategory, count: int, peers: list[aliases.AnyTopPeer]): ...

    def __init__(self, category, count, peers, _='topPeerCategoryPeers', **kwargs):
        kwargs['category'] = category
        kwargs['count'] = count
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def category(self) -> aliases.AnyTopPeerCategory:
        return build_object(self['category'])

    @property
    def count(self) -> int:
        return self['count']

    @property
    def peers(self) -> list[aliases.AnyTopPeer]:
        return build_object(self['peers'])


class DraftMessageEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: Optional[int] = ...): ...

    def __init__(self, _='draftMessageEmpty', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> Optional[int]:
        return self['date']


class DraftMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, date: int, no_webpage: Optional[bool] = ..., invert_media: Optional[bool] = ..., reply_to: Optional[aliases.AnyInputReplyTo] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., media: Optional[aliases.AnyInputMedia] = ..., effect: Optional[int] = ..., suggested_post: Optional[aliases.AnySuggestedPost] = ...): ...

    def __init__(self, message, date, _='draftMessage', **kwargs):
        kwargs['message'] = message
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def no_webpage(self) -> Optional[bool]:
        return self['no_webpage']

    @property
    def invert_media(self) -> Optional[bool]:
        return self['invert_media']

    @property
    def reply_to(self) -> Optional[aliases.AnyInputReplyTo]:
        return build_object(self['reply_to'])

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def media(self) -> Optional[aliases.AnyInputMedia]:
        return build_object(self['media'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def effect(self) -> Optional[int]:
        return self['effect']

    @property
    def suggested_post(self) -> Optional[aliases.AnySuggestedPost]:
        return build_object(self['suggested_post'])


class StickerSetCovered(dict):
    __slots__ = ()

    @overload
    def __init__(self, set: aliases.AnyStickerSet, cover: aliases.AnyDocument): ...

    def __init__(self, set, cover, _='stickerSetCovered', **kwargs):
        kwargs['set'] = set
        kwargs['cover'] = cover
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def set(self) -> aliases.AnyStickerSet:
        return build_object(self['set'])

    @property
    def cover(self) -> aliases.AnyDocument:
        return build_object(self['cover'])


class StickerSetMultiCovered(dict):
    __slots__ = ()

    @overload
    def __init__(self, set: aliases.AnyStickerSet, covers: list[aliases.AnyDocument]): ...

    def __init__(self, set, covers, _='stickerSetMultiCovered', **kwargs):
        kwargs['set'] = set
        kwargs['covers'] = covers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def set(self) -> aliases.AnyStickerSet:
        return build_object(self['set'])

    @property
    def covers(self) -> list[aliases.AnyDocument]:
        return build_object(self['covers'])


class StickerSetFullCovered(dict):
    __slots__ = ()

    @overload
    def __init__(self, set: aliases.AnyStickerSet, packs: list[aliases.AnyStickerPack], keywords: list[aliases.AnyStickerKeyword], documents: list[aliases.AnyDocument]): ...

    def __init__(self, set, packs, keywords, documents, _='stickerSetFullCovered', **kwargs):
        kwargs['set'] = set
        kwargs['packs'] = packs
        kwargs['keywords'] = keywords
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def set(self) -> aliases.AnyStickerSet:
        return build_object(self['set'])

    @property
    def packs(self) -> list[aliases.AnyStickerPack]:
        return build_object(self['packs'])

    @property
    def keywords(self) -> list[aliases.AnyStickerKeyword]:
        return build_object(self['keywords'])

    @property
    def documents(self) -> list[aliases.AnyDocument]:
        return build_object(self['documents'])


class StickerSetNoCovered(dict):
    __slots__ = ()

    @overload
    def __init__(self, set: aliases.AnyStickerSet): ...

    def __init__(self, set, _='stickerSetNoCovered', **kwargs):
        kwargs['set'] = set
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def set(self) -> aliases.AnyStickerSet:
        return build_object(self['set'])


class MaskCoords(dict):
    __slots__ = ()

    @overload
    def __init__(self, n: int, x: float, y: float, zoom: float): ...

    def __init__(self, n, x, y, zoom, _='maskCoords', **kwargs):
        kwargs['n'] = n
        kwargs['x'] = x
        kwargs['y'] = y
        kwargs['zoom'] = zoom
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def n(self) -> int:
        return self['n']

    @property
    def x(self) -> float:
        return self['x']

    @property
    def y(self) -> float:
        return self['y']

    @property
    def zoom(self) -> float:
        return self['zoom']


class InputStickeredMediaPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputPhoto): ...

    def __init__(self, id, _='inputStickeredMediaPhoto', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputPhoto:
        return build_object(self['id'])


class InputStickeredMediaDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: aliases.AnyInputDocument): ...

    def __init__(self, id, _='inputStickeredMediaDocument', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> aliases.AnyInputDocument:
        return build_object(self['id'])


class Game(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, short_name: str, title: str, description: str, photo: aliases.AnyPhoto, document: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, id, access_hash, short_name, title, description, photo, _='game', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['short_name'] = short_name
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['photo'] = photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])


class InputGameID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputGameID', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputGameShortName(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: aliases.AnyInputUser, short_name: str): ...

    def __init__(self, bot_id, short_name, _='inputGameShortName', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['short_name'] = short_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> aliases.AnyInputUser:
        return build_object(self['bot_id'])

    @property
    def short_name(self) -> str:
        return self['short_name']


class HighScore(dict):
    __slots__ = ()

    @overload
    def __init__(self, pos: int, user_id: int, score: int): ...

    def __init__(self, pos, user_id, score, _='highScore', **kwargs):
        kwargs['pos'] = pos
        kwargs['user_id'] = user_id
        kwargs['score'] = score
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pos(self) -> int:
        return self['pos']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def score(self) -> int:
        return self['score']


class TextEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='textEmpty'):
        dict.__init__(self, _=_)


class TextPlain(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str): ...

    def __init__(self, text, _='textPlain', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']


class TextBold(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textBold', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextItalic(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textItalic', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextUnderline(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textUnderline', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextStrike(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textStrike', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextFixed(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textFixed', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, url: str, webpage_id: int): ...

    def __init__(self, text, url, webpage_id, _='textUrl', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['webpage_id'] = webpage_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def url(self) -> str:
        return self['url']

    @property
    def webpage_id(self) -> int:
        return self['webpage_id']


class TextEmail(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, email: str): ...

    def __init__(self, text, email, _='textEmail', **kwargs):
        kwargs['text'] = text
        kwargs['email'] = email
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def email(self) -> str:
        return self['email']


class TextConcat(dict):
    __slots__ = ()

    @overload
    def __init__(self, texts: list[aliases.AnyRichText]): ...

    def __init__(self, texts, _='textConcat', **kwargs):
        kwargs['texts'] = texts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def texts(self) -> list[aliases.AnyRichText]:
        return build_object(self['texts'])


class TextSubscript(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textSubscript', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextSuperscript(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textSuperscript', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextMarked(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='textMarked', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class TextPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, phone: str): ...

    def __init__(self, text, phone, _='textPhone', **kwargs):
        kwargs['text'] = text
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def phone(self) -> str:
        return self['phone']


class TextImage(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int, w: int, h: int): ...

    def __init__(self, document_id, w, h, _='textImage', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']


class TextAnchor(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, name: str): ...

    def __init__(self, text, name, _='textAnchor', **kwargs):
        kwargs['text'] = text
        kwargs['name'] = name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def name(self) -> str:
        return self['name']


class PageBlockUnsupported(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='pageBlockUnsupported'):
        dict.__init__(self, _=_)


class PageBlockTitle(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockTitle', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockSubtitle(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockSubtitle', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockAuthorDate(dict):
    __slots__ = ()

    @overload
    def __init__(self, author: aliases.AnyRichText, published_date: int): ...

    def __init__(self, author, published_date, _='pageBlockAuthorDate', **kwargs):
        kwargs['author'] = author
        kwargs['published_date'] = published_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def author(self) -> aliases.AnyRichText:
        return build_object(self['author'])

    @property
    def published_date(self) -> int:
        return self['published_date']


class PageBlockHeader(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockHeader', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockSubheader(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockSubheader', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockParagraph(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockParagraph', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockPreformatted(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, language: str): ...

    def __init__(self, text, language, _='pageBlockPreformatted', **kwargs):
        kwargs['text'] = text
        kwargs['language'] = language
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def language(self) -> str:
        return self['language']


class PageBlockFooter(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockFooter', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockDivider(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='pageBlockDivider'):
        dict.__init__(self, _=_)


class PageBlockAnchor(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str): ...

    def __init__(self, name, _='pageBlockAnchor', **kwargs):
        kwargs['name'] = name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']


class PageBlockList(dict):
    __slots__ = ()

    @overload
    def __init__(self, items_: list[aliases.AnyPageListItem]): ...

    def __init__(self, items_, _='pageBlockList', **kwargs):
        kwargs['items'] = items_
        if 'items_' in kwargs:
            kwargs['items'] = kwargs.pop('items_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def items_(self) -> list[aliases.AnyPageListItem]:
        return build_object(self['items'])


class PageBlockBlockquote(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, caption: aliases.AnyRichText): ...

    def __init__(self, text, caption, _='pageBlockBlockquote', **kwargs):
        kwargs['text'] = text
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def caption(self) -> aliases.AnyRichText:
        return build_object(self['caption'])


class PageBlockPullquote(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, caption: aliases.AnyRichText): ...

    def __init__(self, text, caption, _='pageBlockPullquote', **kwargs):
        kwargs['text'] = text
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def caption(self) -> aliases.AnyRichText:
        return build_object(self['caption'])


class PageBlockPhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo_id: int, caption: aliases.AnyPageCaption, url: Optional[str] = ..., webpage_id: Optional[int] = ...): ...

    def __init__(self, photo_id, caption, _='pageBlockPhoto', **kwargs):
        kwargs['photo_id'] = photo_id
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photo_id(self) -> int:
        return self['photo_id']

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def webpage_id(self) -> Optional[int]:
        return self['webpage_id']


class PageBlockVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self, video_id: int, caption: aliases.AnyPageCaption, autoplay: Optional[bool] = ..., loop: Optional[bool] = ...): ...

    def __init__(self, video_id, caption, _='pageBlockVideo', **kwargs):
        kwargs['video_id'] = video_id
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def autoplay(self) -> Optional[bool]:
        return self['autoplay']

    @property
    def loop(self) -> Optional[bool]:
        return self['loop']

    @property
    def video_id(self) -> int:
        return self['video_id']

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockCover(dict):
    __slots__ = ()

    @overload
    def __init__(self, cover: aliases.AnyPageBlock): ...

    def __init__(self, cover, _='pageBlockCover', **kwargs):
        kwargs['cover'] = cover
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def cover(self) -> aliases.AnyPageBlock:
        return build_object(self['cover'])


class PageBlockEmbed(dict):
    __slots__ = ()

    @overload
    def __init__(self, caption: aliases.AnyPageCaption, full_width: Optional[bool] = ..., allow_scrolling: Optional[bool] = ..., url: Optional[str] = ..., html: Optional[str] = ..., poster_photo_id: Optional[int] = ..., w: Optional[int] = ..., h: Optional[int] = ...): ...

    def __init__(self, caption, _='pageBlockEmbed', **kwargs):
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def full_width(self) -> Optional[bool]:
        return self['full_width']

    @property
    def allow_scrolling(self) -> Optional[bool]:
        return self['allow_scrolling']

    @property
    def url(self) -> Optional[str]:
        return self['url']

    @property
    def html(self) -> Optional[str]:
        return self['html']

    @property
    def poster_photo_id(self) -> Optional[int]:
        return self['poster_photo_id']

    @property
    def w(self) -> Optional[int]:
        return self['w']

    @property
    def h(self) -> Optional[int]:
        return self['h']

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockEmbedPost(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, webpage_id: int, author_photo_id: int, author: str, date: int, blocks: list[aliases.AnyPageBlock], caption: aliases.AnyPageCaption): ...

    def __init__(self, url, webpage_id, author_photo_id, author, date, blocks, caption, _='pageBlockEmbedPost', **kwargs):
        kwargs['url'] = url
        kwargs['webpage_id'] = webpage_id
        kwargs['author_photo_id'] = author_photo_id
        kwargs['author'] = author
        kwargs['date'] = date
        kwargs['blocks'] = blocks
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def webpage_id(self) -> int:
        return self['webpage_id']

    @property
    def author_photo_id(self) -> int:
        return self['author_photo_id']

    @property
    def author(self) -> str:
        return self['author']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def blocks(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['blocks'])

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockCollage(dict):
    __slots__ = ()

    @overload
    def __init__(self, items_: list[aliases.AnyPageBlock], caption: aliases.AnyPageCaption): ...

    def __init__(self, items_, caption, _='pageBlockCollage', **kwargs):
        kwargs['items'] = items_
        kwargs['caption'] = caption
        if 'items_' in kwargs:
            kwargs['items'] = kwargs.pop('items_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def items_(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['items'])

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockSlideshow(dict):
    __slots__ = ()

    @overload
    def __init__(self, items_: list[aliases.AnyPageBlock], caption: aliases.AnyPageCaption): ...

    def __init__(self, items_, caption, _='pageBlockSlideshow', **kwargs):
        kwargs['items'] = items_
        kwargs['caption'] = caption
        if 'items_' in kwargs:
            kwargs['items'] = kwargs.pop('items_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def items_(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['items'])

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel: aliases.AnyChat): ...

    def __init__(self, channel, _='pageBlockChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> aliases.AnyChat:
        return build_object(self['channel'])


class PageBlockAudio(dict):
    __slots__ = ()

    @overload
    def __init__(self, audio_id: int, caption: aliases.AnyPageCaption): ...

    def __init__(self, audio_id, caption, _='pageBlockAudio', **kwargs):
        kwargs['audio_id'] = audio_id
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def audio_id(self) -> int:
        return self['audio_id']

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PageBlockKicker(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageBlockKicker', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageBlockTable(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: aliases.AnyRichText, rows: list[aliases.AnyPageTableRow], bordered: Optional[bool] = ..., striped: Optional[bool] = ...): ...

    def __init__(self, title, rows, _='pageBlockTable', **kwargs):
        kwargs['title'] = title
        kwargs['rows'] = rows
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bordered(self) -> Optional[bool]:
        return self['bordered']

    @property
    def striped(self) -> Optional[bool]:
        return self['striped']

    @property
    def title(self) -> aliases.AnyRichText:
        return build_object(self['title'])

    @property
    def rows(self) -> list[aliases.AnyPageTableRow]:
        return build_object(self['rows'])


class PageBlockOrderedList(dict):
    __slots__ = ()

    @overload
    def __init__(self, items_: list[aliases.AnyPageListOrderedItem]): ...

    def __init__(self, items_, _='pageBlockOrderedList', **kwargs):
        kwargs['items'] = items_
        if 'items_' in kwargs:
            kwargs['items'] = kwargs.pop('items_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def items_(self) -> list[aliases.AnyPageListOrderedItem]:
        return build_object(self['items'])


class PageBlockDetails(dict):
    __slots__ = ()

    @overload
    def __init__(self, blocks: list[aliases.AnyPageBlock], title: aliases.AnyRichText, open: Optional[bool] = ...): ...

    def __init__(self, blocks, title, _='pageBlockDetails', **kwargs):
        kwargs['blocks'] = blocks
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def open(self) -> Optional[bool]:
        return self['open']

    @property
    def blocks(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['blocks'])

    @property
    def title(self) -> aliases.AnyRichText:
        return build_object(self['title'])


class PageBlockRelatedArticles(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: aliases.AnyRichText, articles: list[aliases.AnyPageRelatedArticle]): ...

    def __init__(self, title, articles, _='pageBlockRelatedArticles', **kwargs):
        kwargs['title'] = title
        kwargs['articles'] = articles
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> aliases.AnyRichText:
        return build_object(self['title'])

    @property
    def articles(self) -> list[aliases.AnyPageRelatedArticle]:
        return build_object(self['articles'])


class PageBlockMap(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo: aliases.AnyGeoPoint, zoom: int, w: int, h: int, caption: aliases.AnyPageCaption): ...

    def __init__(self, geo, zoom, w, h, caption, _='pageBlockMap', **kwargs):
        kwargs['geo'] = geo
        kwargs['zoom'] = zoom
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['caption'] = caption
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def zoom(self) -> int:
        return self['zoom']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def caption(self) -> aliases.AnyPageCaption:
        return build_object(self['caption'])


class PhoneCallDiscardReasonMissed(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='phoneCallDiscardReasonMissed'):
        dict.__init__(self, _=_)


class PhoneCallDiscardReasonDisconnect(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='phoneCallDiscardReasonDisconnect'):
        dict.__init__(self, _=_)


class PhoneCallDiscardReasonHangup(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='phoneCallDiscardReasonHangup'):
        dict.__init__(self, _=_)


class PhoneCallDiscardReasonBusy(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='phoneCallDiscardReasonBusy'):
        dict.__init__(self, _=_)


class PhoneCallDiscardReasonMigrateConferenceCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='phoneCallDiscardReasonMigrateConferenceCall', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class DataJSON(dict):
    __slots__ = ()

    @overload
    def __init__(self, data: str): ...

    def __init__(self, data, _='dataJSON', **kwargs):
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def data(self) -> str:
        return self['data']


class LabeledPrice(dict):
    __slots__ = ()

    @overload
    def __init__(self, label: str, amount: int): ...

    def __init__(self, label, amount, _='labeledPrice', **kwargs):
        kwargs['label'] = label
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def label(self) -> str:
        return self['label']

    @property
    def amount(self) -> int:
        return self['amount']


class Invoice(dict):
    __slots__ = ()

    @overload
    def __init__(self, currency: str, prices: list[aliases.AnyLabeledPrice], test: Optional[bool] = ..., name_requested: Optional[bool] = ..., phone_requested: Optional[bool] = ..., email_requested: Optional[bool] = ..., shipping_address_requested: Optional[bool] = ..., flexible: Optional[bool] = ..., phone_to_provider: Optional[bool] = ..., email_to_provider: Optional[bool] = ..., recurring: Optional[bool] = ..., max_tip_amount: Optional[int] = ..., suggested_tip_amounts: Optional[list[int]] = ..., terms_url: Optional[str] = ..., subscription_period: Optional[int] = ...): ...

    def __init__(self, currency, prices, _='invoice', **kwargs):
        kwargs['currency'] = currency
        kwargs['prices'] = prices
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def test(self) -> Optional[bool]:
        return self['test']

    @property
    def name_requested(self) -> Optional[bool]:
        return self['name_requested']

    @property
    def phone_requested(self) -> Optional[bool]:
        return self['phone_requested']

    @property
    def email_requested(self) -> Optional[bool]:
        return self['email_requested']

    @property
    def shipping_address_requested(self) -> Optional[bool]:
        return self['shipping_address_requested']

    @property
    def flexible(self) -> Optional[bool]:
        return self['flexible']

    @property
    def phone_to_provider(self) -> Optional[bool]:
        return self['phone_to_provider']

    @property
    def email_to_provider(self) -> Optional[bool]:
        return self['email_to_provider']

    @property
    def recurring(self) -> Optional[bool]:
        return self['recurring']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def prices(self) -> list[aliases.AnyLabeledPrice]:
        return build_object(self['prices'])

    @property
    def max_tip_amount(self) -> Optional[int]:
        return self['max_tip_amount']

    @property
    def suggested_tip_amounts(self) -> Optional[list[int]]:
        return self['suggested_tip_amounts']

    @property
    def terms_url(self) -> Optional[str]:
        return self['terms_url']

    @property
    def subscription_period(self) -> Optional[int]:
        return self['subscription_period']


class PaymentCharge(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, provider_charge_id: str): ...

    def __init__(self, id, provider_charge_id, _='paymentCharge', **kwargs):
        kwargs['id'] = id
        kwargs['provider_charge_id'] = provider_charge_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def provider_charge_id(self) -> str:
        return self['provider_charge_id']


class PostAddress(dict):
    __slots__ = ()

    @overload
    def __init__(self, street_line1: str, street_line2: str, city: str, state: str, country_iso2: str, post_code: str): ...

    def __init__(self, street_line1, street_line2, city, state, country_iso2, post_code, _='postAddress', **kwargs):
        kwargs['street_line1'] = street_line1
        kwargs['street_line2'] = street_line2
        kwargs['city'] = city
        kwargs['state'] = state
        kwargs['country_iso2'] = country_iso2
        kwargs['post_code'] = post_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def street_line1(self) -> str:
        return self['street_line1']

    @property
    def street_line2(self) -> str:
        return self['street_line2']

    @property
    def city(self) -> str:
        return self['city']

    @property
    def state(self) -> str:
        return self['state']

    @property
    def country_iso2(self) -> str:
        return self['country_iso2']

    @property
    def post_code(self) -> str:
        return self['post_code']


class PaymentRequestedInfo(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: Optional[str] = ..., phone: Optional[str] = ..., email: Optional[str] = ..., shipping_address: Optional[aliases.AnyPostAddress] = ...): ...

    def __init__(self, _='paymentRequestedInfo', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> Optional[str]:
        return self['name']

    @property
    def phone(self) -> Optional[str]:
        return self['phone']

    @property
    def email(self) -> Optional[str]:
        return self['email']

    @property
    def shipping_address(self) -> Optional[aliases.AnyPostAddress]:
        return build_object(self['shipping_address'])


class PaymentSavedCredentialsCard(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, title: str): ...

    def __init__(self, id, title, _='paymentSavedCredentialsCard', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']


class WebDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, access_hash: int, size: int, mime_type: str, attributes: list[aliases.AnyDocumentAttribute]): ...

    def __init__(self, url, access_hash, size, mime_type, attributes, _='webDocument', **kwargs):
        kwargs['url'] = url
        kwargs['access_hash'] = access_hash
        kwargs['size'] = size
        kwargs['mime_type'] = mime_type
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def attributes(self) -> list[aliases.AnyDocumentAttribute]:
        return build_object(self['attributes'])


class WebDocumentNoProxy(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, size: int, mime_type: str, attributes: list[aliases.AnyDocumentAttribute]): ...

    def __init__(self, url, size, mime_type, attributes, _='webDocumentNoProxy', **kwargs):
        kwargs['url'] = url
        kwargs['size'] = size
        kwargs['mime_type'] = mime_type
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def attributes(self) -> list[aliases.AnyDocumentAttribute]:
        return build_object(self['attributes'])


class InputWebDocument(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, size: int, mime_type: str, attributes: list[aliases.AnyDocumentAttribute]): ...

    def __init__(self, url, size, mime_type, attributes, _='inputWebDocument', **kwargs):
        kwargs['url'] = url
        kwargs['size'] = size
        kwargs['mime_type'] = mime_type
        kwargs['attributes'] = attributes
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def mime_type(self) -> str:
        return self['mime_type']

    @property
    def attributes(self) -> list[aliases.AnyDocumentAttribute]:
        return build_object(self['attributes'])


class InputWebFileLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, access_hash: int): ...

    def __init__(self, url, access_hash, _='inputWebFileLocation', **kwargs):
        kwargs['url'] = url
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputWebFileGeoPointLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyInputGeoPoint, access_hash: int, w: int, h: int, zoom: int, scale: int): ...

    def __init__(self, geo_point, access_hash, w, h, zoom, scale, _='inputWebFileGeoPointLocation', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['access_hash'] = access_hash
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['zoom'] = zoom
        kwargs['scale'] = scale
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyInputGeoPoint:
        return build_object(self['geo_point'])

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def zoom(self) -> int:
        return self['zoom']

    @property
    def scale(self) -> int:
        return self['scale']


class InputWebFileAudioAlbumThumbLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, small: Optional[bool] = ..., document: Optional[aliases.AnyInputDocument] = ..., title: Optional[str] = ..., performer: Optional[str] = ...): ...

    def __init__(self, _='inputWebFileAudioAlbumThumbLocation', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def small(self) -> Optional[bool]:
        return self['small']

    @property
    def document(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['document'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def performer(self) -> Optional[str]:
        return self['performer']


class InputPaymentCredentialsSaved(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, tmp_password: bytes): ...

    def __init__(self, id, tmp_password, _='inputPaymentCredentialsSaved', **kwargs):
        kwargs['id'] = id
        kwargs['tmp_password'] = tmp_password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def tmp_password(self) -> bytes:
        return self['tmp_password']


class InputPaymentCredentials(dict):
    __slots__ = ()

    @overload
    def __init__(self, data: aliases.AnyDataJSON, save: Optional[bool] = ...): ...

    def __init__(self, data, _='inputPaymentCredentials', **kwargs):
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def save(self) -> Optional[bool]:
        return self['save']

    @property
    def data(self) -> aliases.AnyDataJSON:
        return build_object(self['data'])


class InputPaymentCredentialsApplePay(dict):
    __slots__ = ()

    @overload
    def __init__(self, payment_data: aliases.AnyDataJSON): ...

    def __init__(self, payment_data, _='inputPaymentCredentialsApplePay', **kwargs):
        kwargs['payment_data'] = payment_data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def payment_data(self) -> aliases.AnyDataJSON:
        return build_object(self['payment_data'])


class InputPaymentCredentialsGooglePay(dict):
    __slots__ = ()

    @overload
    def __init__(self, payment_token: aliases.AnyDataJSON): ...

    def __init__(self, payment_token, _='inputPaymentCredentialsGooglePay', **kwargs):
        kwargs['payment_token'] = payment_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def payment_token(self) -> aliases.AnyDataJSON:
        return build_object(self['payment_token'])


class ShippingOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, title: str, prices: list[aliases.AnyLabeledPrice]): ...

    def __init__(self, id, title, prices, _='shippingOption', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['prices'] = prices
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def prices(self) -> list[aliases.AnyLabeledPrice]:
        return build_object(self['prices'])


class InputStickerSetItem(dict):
    __slots__ = ()

    @overload
    def __init__(self, document: aliases.AnyInputDocument, emoji: str, mask_coords: Optional[aliases.AnyMaskCoords] = ..., keywords: Optional[str] = ...): ...

    def __init__(self, document, emoji, _='inputStickerSetItem', **kwargs):
        kwargs['document'] = document
        kwargs['emoji'] = emoji
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document(self) -> aliases.AnyInputDocument:
        return build_object(self['document'])

    @property
    def emoji(self) -> str:
        return self['emoji']

    @property
    def mask_coords(self) -> Optional[aliases.AnyMaskCoords]:
        return build_object(self['mask_coords'])

    @property
    def keywords(self) -> Optional[str]:
        return self['keywords']


class InputPhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputPhoneCall', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class PhoneCallEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='phoneCallEmpty', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class PhoneCallWaiting(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, protocol: aliases.AnyPhoneCallProtocol, video: Optional[bool] = ..., receive_date: Optional[int] = ...): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, protocol, _='phoneCallWaiting', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])

    @property
    def receive_date(self) -> Optional[int]:
        return self['receive_date']


class PhoneCallRequested(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_hash: bytes, protocol: aliases.AnyPhoneCallProtocol, video: Optional[bool] = ...): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, g_a_hash, protocol, _='phoneCallRequested', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['g_a_hash'] = g_a_hash
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def g_a_hash(self) -> bytes:
        return self['g_a_hash']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])


class PhoneCallAccepted(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_b: bytes, protocol: aliases.AnyPhoneCallProtocol, video: Optional[bool] = ...): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, g_b, protocol, _='phoneCallAccepted', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['g_b'] = g_b
        kwargs['protocol'] = protocol
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def g_b(self) -> bytes:
        return self['g_b']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])


class PhoneCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int, protocol: aliases.AnyPhoneCallProtocol, connections: list[aliases.AnyPhoneConnection], start_date: int, p2p_allowed: Optional[bool] = ..., video: Optional[bool] = ..., conference_supported: Optional[bool] = ..., custom_parameters: Optional[aliases.AnyDataJSON] = ...): ...

    def __init__(self, id, access_hash, date, admin_id, participant_id, g_a_or_b, key_fingerprint, protocol, connections, start_date, _='phoneCall', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['date'] = date
        kwargs['admin_id'] = admin_id
        kwargs['participant_id'] = participant_id
        kwargs['g_a_or_b'] = g_a_or_b
        kwargs['key_fingerprint'] = key_fingerprint
        kwargs['protocol'] = protocol
        kwargs['connections'] = connections
        kwargs['start_date'] = start_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def p2p_allowed(self) -> Optional[bool]:
        return self['p2p_allowed']

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def conference_supported(self) -> Optional[bool]:
        return self['conference_supported']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def participant_id(self) -> int:
        return self['participant_id']

    @property
    def g_a_or_b(self) -> bytes:
        return self['g_a_or_b']

    @property
    def key_fingerprint(self) -> int:
        return self['key_fingerprint']

    @property
    def protocol(self) -> aliases.AnyPhoneCallProtocol:
        return build_object(self['protocol'])

    @property
    def connections(self) -> list[aliases.AnyPhoneConnection]:
        return build_object(self['connections'])

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def custom_parameters(self) -> Optional[aliases.AnyDataJSON]:
        return build_object(self['custom_parameters'])


class PhoneCallDiscarded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, need_rating: Optional[bool] = ..., need_debug: Optional[bool] = ..., video: Optional[bool] = ..., reason: Optional[aliases.AnyPhoneCallDiscardReason] = ..., duration: Optional[int] = ...): ...

    def __init__(self, id, _='phoneCallDiscarded', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def need_rating(self) -> Optional[bool]:
        return self['need_rating']

    @property
    def need_debug(self) -> Optional[bool]:
        return self['need_debug']

    @property
    def video(self) -> Optional[bool]:
        return self['video']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def reason(self) -> Optional[aliases.AnyPhoneCallDiscardReason]:
        return build_object(self['reason'])

    @property
    def duration(self) -> Optional[int]:
        return self['duration']


class PhoneConnection(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, ip: str, ipv6: str, port: int, peer_tag: bytes, tcp: Optional[bool] = ...): ...

    def __init__(self, id, ip, ipv6, port, peer_tag, _='phoneConnection', **kwargs):
        kwargs['id'] = id
        kwargs['ip'] = ip
        kwargs['ipv6'] = ipv6
        kwargs['port'] = port
        kwargs['peer_tag'] = peer_tag
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def tcp(self) -> Optional[bool]:
        return self['tcp']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def ip(self) -> str:
        return self['ip']

    @property
    def ipv6(self) -> str:
        return self['ipv6']

    @property
    def port(self) -> int:
        return self['port']

    @property
    def peer_tag(self) -> bytes:
        return self['peer_tag']


class PhoneConnectionWebrtc(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, ip: str, ipv6: str, port: int, username: str, password: str, turn: Optional[bool] = ..., stun: Optional[bool] = ...): ...

    def __init__(self, id, ip, ipv6, port, username, password, _='phoneConnectionWebrtc', **kwargs):
        kwargs['id'] = id
        kwargs['ip'] = ip
        kwargs['ipv6'] = ipv6
        kwargs['port'] = port
        kwargs['username'] = username
        kwargs['password'] = password
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def turn(self) -> Optional[bool]:
        return self['turn']

    @property
    def stun(self) -> Optional[bool]:
        return self['stun']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def ip(self) -> str:
        return self['ip']

    @property
    def ipv6(self) -> str:
        return self['ipv6']

    @property
    def port(self) -> int:
        return self['port']

    @property
    def username(self) -> str:
        return self['username']

    @property
    def password(self) -> str:
        return self['password']


class PhoneCallProtocol(dict):
    __slots__ = ()

    @overload
    def __init__(self, min_layer: int, max_layer: int, library_versions: list[str], udp_p2p: Optional[bool] = ..., udp_reflector: Optional[bool] = ...): ...

    def __init__(self, min_layer, max_layer, library_versions, _='phoneCallProtocol', **kwargs):
        kwargs['min_layer'] = min_layer
        kwargs['max_layer'] = max_layer
        kwargs['library_versions'] = library_versions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def udp_p2p(self) -> Optional[bool]:
        return self['udp_p2p']

    @property
    def udp_reflector(self) -> Optional[bool]:
        return self['udp_reflector']

    @property
    def min_layer(self) -> int:
        return self['min_layer']

    @property
    def max_layer(self) -> int:
        return self['max_layer']

    @property
    def library_versions(self) -> list[str]:
        return self['library_versions']


class CdnPublicKey(dict):
    __slots__ = ()

    @overload
    def __init__(self, dc_id: int, public_key: str): ...

    def __init__(self, dc_id, public_key, _='cdnPublicKey', **kwargs):
        kwargs['dc_id'] = dc_id
        kwargs['public_key'] = public_key
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def public_key(self) -> str:
        return self['public_key']


class CdnConfig(dict):
    __slots__ = ()

    @overload
    def __init__(self, public_keys: list[aliases.AnyCdnPublicKey]): ...

    def __init__(self, public_keys, _='cdnConfig', **kwargs):
        kwargs['public_keys'] = public_keys
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def public_keys(self) -> list[aliases.AnyCdnPublicKey]:
        return build_object(self['public_keys'])


class LangPackString(dict):
    __slots__ = ()

    @overload
    def __init__(self, key: str, value: str): ...

    def __init__(self, key, value, _='langPackString', **kwargs):
        kwargs['key'] = key
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> str:
        return self['key']

    @property
    def value(self) -> str:
        return self['value']


class LangPackStringPluralized(dict):
    __slots__ = ()

    @overload
    def __init__(self, key: str, other_value: str, zero_value: Optional[str] = ..., one_value: Optional[str] = ..., two_value: Optional[str] = ..., few_value: Optional[str] = ..., many_value: Optional[str] = ...): ...

    def __init__(self, key, other_value, _='langPackStringPluralized', **kwargs):
        kwargs['key'] = key
        kwargs['other_value'] = other_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> str:
        return self['key']

    @property
    def zero_value(self) -> Optional[str]:
        return self['zero_value']

    @property
    def one_value(self) -> Optional[str]:
        return self['one_value']

    @property
    def two_value(self) -> Optional[str]:
        return self['two_value']

    @property
    def few_value(self) -> Optional[str]:
        return self['few_value']

    @property
    def many_value(self) -> Optional[str]:
        return self['many_value']

    @property
    def other_value(self) -> str:
        return self['other_value']


class LangPackStringDeleted(dict):
    __slots__ = ()

    @overload
    def __init__(self, key: str): ...

    def __init__(self, key, _='langPackStringDeleted', **kwargs):
        kwargs['key'] = key
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> str:
        return self['key']


class LangPackDifference(dict):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, from_version: int, version: int, strings: list[aliases.AnyLangPackString]): ...

    def __init__(self, lang_code, from_version, version, strings, _='langPackDifference', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['from_version'] = from_version
        kwargs['version'] = version
        kwargs['strings'] = strings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def from_version(self) -> int:
        return self['from_version']

    @property
    def version(self) -> int:
        return self['version']

    @property
    def strings(self) -> list[aliases.AnyLangPackString]:
        return build_object(self['strings'])


class LangPackLanguage(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, native_name: str, lang_code: str, plural_code: str, strings_count: int, translated_count: int, translations_url: str, official: Optional[bool] = ..., rtl: Optional[bool] = ..., beta: Optional[bool] = ..., base_lang_code: Optional[str] = ...): ...

    def __init__(self, name, native_name, lang_code, plural_code, strings_count, translated_count, translations_url, _='langPackLanguage', **kwargs):
        kwargs['name'] = name
        kwargs['native_name'] = native_name
        kwargs['lang_code'] = lang_code
        kwargs['plural_code'] = plural_code
        kwargs['strings_count'] = strings_count
        kwargs['translated_count'] = translated_count
        kwargs['translations_url'] = translations_url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def official(self) -> Optional[bool]:
        return self['official']

    @property
    def rtl(self) -> Optional[bool]:
        return self['rtl']

    @property
    def beta(self) -> Optional[bool]:
        return self['beta']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def native_name(self) -> str:
        return self['native_name']

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def base_lang_code(self) -> Optional[str]:
        return self['base_lang_code']

    @property
    def plural_code(self) -> str:
        return self['plural_code']

    @property
    def strings_count(self) -> int:
        return self['strings_count']

    @property
    def translated_count(self) -> int:
        return self['translated_count']

    @property
    def translations_url(self) -> str:
        return self['translations_url']


class ChannelAdminLogEventActionChangeTitle(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: str, new_value: str): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeTitle', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> str:
        return self['prev_value']

    @property
    def new_value(self) -> str:
        return self['new_value']


class ChannelAdminLogEventActionChangeAbout(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: str, new_value: str): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeAbout', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> str:
        return self['prev_value']

    @property
    def new_value(self) -> str:
        return self['new_value']


class ChannelAdminLogEventActionChangeUsername(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: str, new_value: str): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeUsername', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> str:
        return self['prev_value']

    @property
    def new_value(self) -> str:
        return self['new_value']


class ChannelAdminLogEventActionChangePhoto(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_photo: aliases.AnyPhoto, new_photo: aliases.AnyPhoto): ...

    def __init__(self, prev_photo, new_photo, _='channelAdminLogEventActionChangePhoto', **kwargs):
        kwargs['prev_photo'] = prev_photo
        kwargs['new_photo'] = new_photo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_photo(self) -> aliases.AnyPhoto:
        return build_object(self['prev_photo'])

    @property
    def new_photo(self) -> aliases.AnyPhoto:
        return build_object(self['new_photo'])


class ChannelAdminLogEventActionToggleInvites(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleInvites', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionToggleSignatures(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleSignatures', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionUpdatePinned(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='channelAdminLogEventActionUpdatePinned', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class ChannelAdminLogEventActionEditMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_message: aliases.AnyMessage, new_message: aliases.AnyMessage): ...

    def __init__(self, prev_message, new_message, _='channelAdminLogEventActionEditMessage', **kwargs):
        kwargs['prev_message'] = prev_message
        kwargs['new_message'] = new_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_message(self) -> aliases.AnyMessage:
        return build_object(self['prev_message'])

    @property
    def new_message(self) -> aliases.AnyMessage:
        return build_object(self['new_message'])


class ChannelAdminLogEventActionDeleteMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='channelAdminLogEventActionDeleteMessage', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class ChannelAdminLogEventActionParticipantJoin(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelAdminLogEventActionParticipantJoin'):
        dict.__init__(self, _=_)


class ChannelAdminLogEventActionParticipantLeave(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelAdminLogEventActionParticipantLeave'):
        dict.__init__(self, _=_)


class ChannelAdminLogEventActionParticipantInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, participant: aliases.AnyChannelParticipant): ...

    def __init__(self, participant, _='channelAdminLogEventActionParticipantInvite', **kwargs):
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['participant'])


class ChannelAdminLogEventActionParticipantToggleBan(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_participant: aliases.AnyChannelParticipant, new_participant: aliases.AnyChannelParticipant): ...

    def __init__(self, prev_participant, new_participant, _='channelAdminLogEventActionParticipantToggleBan', **kwargs):
        kwargs['prev_participant'] = prev_participant
        kwargs['new_participant'] = new_participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['prev_participant'])

    @property
    def new_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['new_participant'])


class ChannelAdminLogEventActionParticipantToggleAdmin(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_participant: aliases.AnyChannelParticipant, new_participant: aliases.AnyChannelParticipant): ...

    def __init__(self, prev_participant, new_participant, _='channelAdminLogEventActionParticipantToggleAdmin', **kwargs):
        kwargs['prev_participant'] = prev_participant
        kwargs['new_participant'] = new_participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['prev_participant'])

    @property
    def new_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['new_participant'])


class ChannelAdminLogEventActionChangeStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_stickerset: aliases.AnyInputStickerSet, new_stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, prev_stickerset, new_stickerset, _='channelAdminLogEventActionChangeStickerSet', **kwargs):
        kwargs['prev_stickerset'] = prev_stickerset
        kwargs['new_stickerset'] = new_stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['prev_stickerset'])

    @property
    def new_stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['new_stickerset'])


class ChannelAdminLogEventActionTogglePreHistoryHidden(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionTogglePreHistoryHidden', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionDefaultBannedRights(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_banned_rights: aliases.AnyChatBannedRights, new_banned_rights: aliases.AnyChatBannedRights): ...

    def __init__(self, prev_banned_rights, new_banned_rights, _='channelAdminLogEventActionDefaultBannedRights', **kwargs):
        kwargs['prev_banned_rights'] = prev_banned_rights
        kwargs['new_banned_rights'] = new_banned_rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['prev_banned_rights'])

    @property
    def new_banned_rights(self) -> aliases.AnyChatBannedRights:
        return build_object(self['new_banned_rights'])


class ChannelAdminLogEventActionStopPoll(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='channelAdminLogEventActionStopPoll', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class ChannelAdminLogEventActionChangeLinkedChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: int, new_value: int): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeLinkedChat', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> int:
        return self['prev_value']

    @property
    def new_value(self) -> int:
        return self['new_value']


class ChannelAdminLogEventActionChangeLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyChannelLocation, new_value: aliases.AnyChannelLocation): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeLocation', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyChannelLocation:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyChannelLocation:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionToggleSlowMode(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: int, new_value: int): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionToggleSlowMode', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> int:
        return self['prev_value']

    @property
    def new_value(self) -> int:
        return self['new_value']


class ChannelAdminLogEventActionStartGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='channelAdminLogEventActionStartGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class ChannelAdminLogEventActionDiscardGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, call: aliases.AnyInputGroupCall): ...

    def __init__(self, call, _='channelAdminLogEventActionDiscardGroupCall', **kwargs):
        kwargs['call'] = call
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def call(self) -> aliases.AnyInputGroupCall:
        return build_object(self['call'])


class ChannelAdminLogEventActionParticipantMute(dict):
    __slots__ = ()

    @overload
    def __init__(self, participant: aliases.AnyGroupCallParticipant): ...

    def __init__(self, participant, _='channelAdminLogEventActionParticipantMute', **kwargs):
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participant(self) -> aliases.AnyGroupCallParticipant:
        return build_object(self['participant'])


class ChannelAdminLogEventActionParticipantUnmute(dict):
    __slots__ = ()

    @overload
    def __init__(self, participant: aliases.AnyGroupCallParticipant): ...

    def __init__(self, participant, _='channelAdminLogEventActionParticipantUnmute', **kwargs):
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participant(self) -> aliases.AnyGroupCallParticipant:
        return build_object(self['participant'])


class ChannelAdminLogEventActionToggleGroupCallSetting(dict):
    __slots__ = ()

    @overload
    def __init__(self, join_muted: bool): ...

    def __init__(self, join_muted, _='channelAdminLogEventActionToggleGroupCallSetting', **kwargs):
        kwargs['join_muted'] = join_muted
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def join_muted(self) -> bool:
        return self['join_muted']


class ChannelAdminLogEventActionParticipantJoinByInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite, via_chatlist: Optional[bool] = ...): ...

    def __init__(self, invite, _='channelAdminLogEventActionParticipantJoinByInvite', **kwargs):
        kwargs['invite'] = invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def via_chatlist(self) -> Optional[bool]:
        return self['via_chatlist']

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])


class ChannelAdminLogEventActionExportedInviteDelete(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite): ...

    def __init__(self, invite, _='channelAdminLogEventActionExportedInviteDelete', **kwargs):
        kwargs['invite'] = invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])


class ChannelAdminLogEventActionExportedInviteRevoke(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite): ...

    def __init__(self, invite, _='channelAdminLogEventActionExportedInviteRevoke', **kwargs):
        kwargs['invite'] = invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])


class ChannelAdminLogEventActionExportedInviteEdit(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_invite: aliases.AnyExportedChatInvite, new_invite: aliases.AnyExportedChatInvite): ...

    def __init__(self, prev_invite, new_invite, _='channelAdminLogEventActionExportedInviteEdit', **kwargs):
        kwargs['prev_invite'] = prev_invite
        kwargs['new_invite'] = new_invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['prev_invite'])

    @property
    def new_invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['new_invite'])


class ChannelAdminLogEventActionParticipantVolume(dict):
    __slots__ = ()

    @overload
    def __init__(self, participant: aliases.AnyGroupCallParticipant): ...

    def __init__(self, participant, _='channelAdminLogEventActionParticipantVolume', **kwargs):
        kwargs['participant'] = participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def participant(self) -> aliases.AnyGroupCallParticipant:
        return build_object(self['participant'])


class ChannelAdminLogEventActionChangeHistoryTTL(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: int, new_value: int): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeHistoryTTL', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> int:
        return self['prev_value']

    @property
    def new_value(self) -> int:
        return self['new_value']


class ChannelAdminLogEventActionParticipantJoinByRequest(dict):
    __slots__ = ()

    @overload
    def __init__(self, invite: aliases.AnyExportedChatInvite, approved_by: int): ...

    def __init__(self, invite, approved_by, _='channelAdminLogEventActionParticipantJoinByRequest', **kwargs):
        kwargs['invite'] = invite
        kwargs['approved_by'] = approved_by
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def invite(self) -> aliases.AnyExportedChatInvite:
        return build_object(self['invite'])

    @property
    def approved_by(self) -> int:
        return self['approved_by']


class ChannelAdminLogEventActionToggleNoForwards(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleNoForwards', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionSendMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='channelAdminLogEventActionSendMessage', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class ChannelAdminLogEventActionChangeAvailableReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyChatReactions, new_value: aliases.AnyChatReactions): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeAvailableReactions', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyChatReactions:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyChatReactions:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionChangeUsernames(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: list[str], new_value: list[str]): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeUsernames', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> list[str]:
        return self['prev_value']

    @property
    def new_value(self) -> list[str]:
        return self['new_value']


class ChannelAdminLogEventActionToggleForum(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleForum', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionCreateTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, topic: aliases.AnyForumTopic): ...

    def __init__(self, topic, _='channelAdminLogEventActionCreateTopic', **kwargs):
        kwargs['topic'] = topic
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def topic(self) -> aliases.AnyForumTopic:
        return build_object(self['topic'])


class ChannelAdminLogEventActionEditTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_topic: aliases.AnyForumTopic, new_topic: aliases.AnyForumTopic): ...

    def __init__(self, prev_topic, new_topic, _='channelAdminLogEventActionEditTopic', **kwargs):
        kwargs['prev_topic'] = prev_topic
        kwargs['new_topic'] = new_topic
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_topic(self) -> aliases.AnyForumTopic:
        return build_object(self['prev_topic'])

    @property
    def new_topic(self) -> aliases.AnyForumTopic:
        return build_object(self['new_topic'])


class ChannelAdminLogEventActionDeleteTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, topic: aliases.AnyForumTopic): ...

    def __init__(self, topic, _='channelAdminLogEventActionDeleteTopic', **kwargs):
        kwargs['topic'] = topic
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def topic(self) -> aliases.AnyForumTopic:
        return build_object(self['topic'])


class ChannelAdminLogEventActionPinTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_topic: Optional[aliases.AnyForumTopic] = ..., new_topic: Optional[aliases.AnyForumTopic] = ...): ...

    def __init__(self, _='channelAdminLogEventActionPinTopic', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_topic(self) -> Optional[aliases.AnyForumTopic]:
        return build_object(self['prev_topic'])

    @property
    def new_topic(self) -> Optional[aliases.AnyForumTopic]:
        return build_object(self['new_topic'])


class ChannelAdminLogEventActionToggleAntiSpam(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleAntiSpam', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionChangePeerColor(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyPeerColor, new_value: aliases.AnyPeerColor): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangePeerColor', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyPeerColor:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyPeerColor:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionChangeProfilePeerColor(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyPeerColor, new_value: aliases.AnyPeerColor): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeProfilePeerColor', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyPeerColor:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyPeerColor:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionChangeWallpaper(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyWallPaper, new_value: aliases.AnyWallPaper): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeWallpaper', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyWallPaper:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyWallPaper:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionChangeEmojiStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_value: aliases.AnyEmojiStatus, new_value: aliases.AnyEmojiStatus): ...

    def __init__(self, prev_value, new_value, _='channelAdminLogEventActionChangeEmojiStatus', **kwargs):
        kwargs['prev_value'] = prev_value
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_value(self) -> aliases.AnyEmojiStatus:
        return build_object(self['prev_value'])

    @property
    def new_value(self) -> aliases.AnyEmojiStatus:
        return build_object(self['new_value'])


class ChannelAdminLogEventActionChangeEmojiStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_stickerset: aliases.AnyInputStickerSet, new_stickerset: aliases.AnyInputStickerSet): ...

    def __init__(self, prev_stickerset, new_stickerset, _='channelAdminLogEventActionChangeEmojiStickerSet', **kwargs):
        kwargs['prev_stickerset'] = prev_stickerset
        kwargs['new_stickerset'] = new_stickerset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['prev_stickerset'])

    @property
    def new_stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['new_stickerset'])


class ChannelAdminLogEventActionToggleSignatureProfiles(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleSignatureProfiles', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionParticipantSubExtend(dict):
    __slots__ = ()

    @overload
    def __init__(self, prev_participant: aliases.AnyChannelParticipant, new_participant: aliases.AnyChannelParticipant): ...

    def __init__(self, prev_participant, new_participant, _='channelAdminLogEventActionParticipantSubExtend', **kwargs):
        kwargs['prev_participant'] = prev_participant
        kwargs['new_participant'] = new_participant
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def prev_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['prev_participant'])

    @property
    def new_participant(self) -> aliases.AnyChannelParticipant:
        return build_object(self['new_participant'])


class ChannelAdminLogEventActionToggleAutotranslation(dict):
    __slots__ = ()

    @overload
    def __init__(self, new_value: bool): ...

    def __init__(self, new_value, _='channelAdminLogEventActionToggleAutotranslation', **kwargs):
        kwargs['new_value'] = new_value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def new_value(self) -> bool:
        return self['new_value']


class ChannelAdminLogEventActionParticipantEditRank(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, prev_rank: str, new_rank: str): ...

    def __init__(self, user_id, prev_rank, new_rank, _='channelAdminLogEventActionParticipantEditRank', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['prev_rank'] = prev_rank
        kwargs['new_rank'] = new_rank
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def prev_rank(self) -> str:
        return self['prev_rank']

    @property
    def new_rank(self) -> str:
        return self['new_rank']


class ChannelAdminLogEvent(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, date: int, user_id: int, action: aliases.AnyChannelAdminLogEventAction): ...

    def __init__(self, id, date, user_id, action, _='channelAdminLogEvent', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['user_id'] = user_id
        kwargs['action'] = action
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def action(self) -> aliases.AnyChannelAdminLogEventAction:
        return build_object(self['action'])


class ChannelAdminLogEventsFilter(dict):
    __slots__ = ()

    @overload
    def __init__(self, join: Optional[bool] = ..., leave: Optional[bool] = ..., invite: Optional[bool] = ..., ban: Optional[bool] = ..., unban: Optional[bool] = ..., kick: Optional[bool] = ..., unkick: Optional[bool] = ..., promote: Optional[bool] = ..., demote: Optional[bool] = ..., info: Optional[bool] = ..., settings: Optional[bool] = ..., pinned: Optional[bool] = ..., edit: Optional[bool] = ..., delete: Optional[bool] = ..., group_call: Optional[bool] = ..., invites: Optional[bool] = ..., send: Optional[bool] = ..., forums: Optional[bool] = ..., sub_extend: Optional[bool] = ..., edit_rank: Optional[bool] = ...): ...

    def __init__(self, _='channelAdminLogEventsFilter', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def join(self) -> Optional[bool]:
        return self['join']

    @property
    def leave(self) -> Optional[bool]:
        return self['leave']

    @property
    def invite(self) -> Optional[bool]:
        return self['invite']

    @property
    def ban(self) -> Optional[bool]:
        return self['ban']

    @property
    def unban(self) -> Optional[bool]:
        return self['unban']

    @property
    def kick(self) -> Optional[bool]:
        return self['kick']

    @property
    def unkick(self) -> Optional[bool]:
        return self['unkick']

    @property
    def promote(self) -> Optional[bool]:
        return self['promote']

    @property
    def demote(self) -> Optional[bool]:
        return self['demote']

    @property
    def info(self) -> Optional[bool]:
        return self['info']

    @property
    def settings(self) -> Optional[bool]:
        return self['settings']

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def edit(self) -> Optional[bool]:
        return self['edit']

    @property
    def delete(self) -> Optional[bool]:
        return self['delete']

    @property
    def group_call(self) -> Optional[bool]:
        return self['group_call']

    @property
    def invites(self) -> Optional[bool]:
        return self['invites']

    @property
    def send(self) -> Optional[bool]:
        return self['send']

    @property
    def forums(self) -> Optional[bool]:
        return self['forums']

    @property
    def sub_extend(self) -> Optional[bool]:
        return self['sub_extend']

    @property
    def edit_rank(self) -> Optional[bool]:
        return self['edit_rank']


class PopularContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, client_id: int, importers: int): ...

    def __init__(self, client_id, importers, _='popularContact', **kwargs):
        kwargs['client_id'] = client_id
        kwargs['importers'] = importers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def client_id(self) -> int:
        return self['client_id']

    @property
    def importers(self) -> int:
        return self['importers']


class RecentMeUrlUnknown(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='recentMeUrlUnknown', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class RecentMeUrlUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, user_id: int): ...

    def __init__(self, url, user_id, _='recentMeUrlUser', **kwargs):
        kwargs['url'] = url
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def user_id(self) -> int:
        return self['user_id']


class RecentMeUrlChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, chat_id: int): ...

    def __init__(self, url, chat_id, _='recentMeUrlChat', **kwargs):
        kwargs['url'] = url
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def chat_id(self) -> int:
        return self['chat_id']


class RecentMeUrlChatInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, chat_invite: aliases.AnyChatInvite): ...

    def __init__(self, url, chat_invite, _='recentMeUrlChatInvite', **kwargs):
        kwargs['url'] = url
        kwargs['chat_invite'] = chat_invite
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def chat_invite(self) -> aliases.AnyChatInvite:
        return build_object(self['chat_invite'])


class RecentMeUrlStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, set: aliases.AnyStickerSetCovered): ...

    def __init__(self, url, set, _='recentMeUrlStickerSet', **kwargs):
        kwargs['url'] = url
        kwargs['set'] = set
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def set(self) -> aliases.AnyStickerSetCovered:
        return build_object(self['set'])


class InputSingleMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, media: aliases.AnyInputMedia, random_id: int, message: str, entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, media, random_id, message, _='inputSingleMedia', **kwargs):
        kwargs['media'] = media
        kwargs['random_id'] = random_id
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> aliases.AnyInputMedia:
        return build_object(self['media'])

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])


class WebAuthorization(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, bot_id: int, domain: str, browser: str, platform: str, date_created: int, date_active: int, ip: str, region: str): ...

    def __init__(self, hash, bot_id, domain, browser, platform, date_created, date_active, ip, region, _='webAuthorization', **kwargs):
        kwargs['hash'] = hash
        kwargs['bot_id'] = bot_id
        kwargs['domain'] = domain
        kwargs['browser'] = browser
        kwargs['platform'] = platform
        kwargs['date_created'] = date_created
        kwargs['date_active'] = date_active
        kwargs['ip'] = ip
        kwargs['region'] = region
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def domain(self) -> str:
        return self['domain']

    @property
    def browser(self) -> str:
        return self['browser']

    @property
    def platform(self) -> str:
        return self['platform']

    @property
    def date_created(self) -> int:
        return self['date_created']

    @property
    def date_active(self) -> int:
        return self['date_active']

    @property
    def ip(self) -> str:
        return self['ip']

    @property
    def region(self) -> str:
        return self['region']


class InputMessageID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='inputMessageID', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class InputMessageReplyTo(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='inputMessageReplyTo', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class InputMessagePinned(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputMessagePinned'):
        dict.__init__(self, _=_)


class InputMessageCallbackQuery(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, query_id: int): ...

    def __init__(self, id, query_id, _='inputMessageCallbackQuery', **kwargs):
        kwargs['id'] = id
        kwargs['query_id'] = query_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def query_id(self) -> int:
        return self['query_id']


class InputDialogPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='inputDialogPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class InputDialogPeerFolder(dict):
    __slots__ = ()

    @overload
    def __init__(self, folder_id: int): ...

    def __init__(self, folder_id, _='inputDialogPeerFolder', **kwargs):
        kwargs['folder_id'] = folder_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> int:
        return self['folder_id']


class DialogPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer): ...

    def __init__(self, peer, _='dialogPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])


class DialogPeerFolder(dict):
    __slots__ = ()

    @overload
    def __init__(self, folder_id: int): ...

    def __init__(self, folder_id, _='dialogPeerFolder', **kwargs):
        kwargs['folder_id'] = folder_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def folder_id(self) -> int:
        return self['folder_id']


class FileHash(dict):
    __slots__ = ()

    @overload
    def __init__(self, offset: int, limit: int, hash: bytes): ...

    def __init__(self, offset, limit, hash, _='fileHash', **kwargs):
        kwargs['offset'] = offset
        kwargs['limit'] = limit
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offset(self) -> int:
        return self['offset']

    @property
    def limit(self) -> int:
        return self['limit']

    @property
    def hash(self) -> bytes:
        return self['hash']


class InputClientProxy(dict):
    __slots__ = ()

    @overload
    def __init__(self, address: str, port: int): ...

    def __init__(self, address, port, _='inputClientProxy', **kwargs):
        kwargs['address'] = address
        kwargs['port'] = port
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def address(self) -> str:
        return self['address']

    @property
    def port(self) -> int:
        return self['port']


class InputSecureFileUploaded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, parts: int, md5_checksum: str, file_hash: bytes, secret: bytes): ...

    def __init__(self, id, parts, md5_checksum, file_hash, secret, _='inputSecureFileUploaded', **kwargs):
        kwargs['id'] = id
        kwargs['parts'] = parts
        kwargs['md5_checksum'] = md5_checksum
        kwargs['file_hash'] = file_hash
        kwargs['secret'] = secret
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def parts(self) -> int:
        return self['parts']

    @property
    def md5_checksum(self) -> str:
        return self['md5_checksum']

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def secret(self) -> bytes:
        return self['secret']


class InputSecureFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputSecureFile', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class SecureFileEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureFileEmpty'):
        dict.__init__(self, _=_)


class SecureFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, size: int, dc_id: int, date: int, file_hash: bytes, secret: bytes): ...

    def __init__(self, id, access_hash, size, dc_id, date, file_hash, secret, _='secureFile', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['size'] = size
        kwargs['dc_id'] = dc_id
        kwargs['date'] = date
        kwargs['file_hash'] = file_hash
        kwargs['secret'] = secret
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def secret(self) -> bytes:
        return self['secret']


class SecureData(dict):
    __slots__ = ()

    @overload
    def __init__(self, data: bytes, data_hash: bytes, secret: bytes): ...

    def __init__(self, data, data_hash, secret, _='secureData', **kwargs):
        kwargs['data'] = data
        kwargs['data_hash'] = data_hash
        kwargs['secret'] = secret
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def data(self) -> bytes:
        return self['data']

    @property
    def data_hash(self) -> bytes:
        return self['data_hash']

    @property
    def secret(self) -> bytes:
        return self['secret']


class SecurePlainPhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone: str): ...

    def __init__(self, phone, _='securePlainPhone', **kwargs):
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone(self) -> str:
        return self['phone']


class SecurePlainEmail(dict):
    __slots__ = ()

    @overload
    def __init__(self, email: str): ...

    def __init__(self, email, _='securePlainEmail', **kwargs):
        kwargs['email'] = email
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def email(self) -> str:
        return self['email']


class SecureValueTypePersonalDetails(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypePersonalDetails'):
        dict.__init__(self, _=_)


class SecureValueTypePassport(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypePassport'):
        dict.__init__(self, _=_)


class SecureValueTypeDriverLicense(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeDriverLicense'):
        dict.__init__(self, _=_)


class SecureValueTypeIdentityCard(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeIdentityCard'):
        dict.__init__(self, _=_)


class SecureValueTypeInternalPassport(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeInternalPassport'):
        dict.__init__(self, _=_)


class SecureValueTypeAddress(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeAddress'):
        dict.__init__(self, _=_)


class SecureValueTypeUtilityBill(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeUtilityBill'):
        dict.__init__(self, _=_)


class SecureValueTypeBankStatement(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeBankStatement'):
        dict.__init__(self, _=_)


class SecureValueTypeRentalAgreement(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeRentalAgreement'):
        dict.__init__(self, _=_)


class SecureValueTypePassportRegistration(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypePassportRegistration'):
        dict.__init__(self, _=_)


class SecureValueTypeTemporaryRegistration(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeTemporaryRegistration'):
        dict.__init__(self, _=_)


class SecureValueTypePhone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypePhone'):
        dict.__init__(self, _=_)


class SecureValueTypeEmail(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='secureValueTypeEmail'):
        dict.__init__(self, _=_)


class SecureValue(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, hash: bytes, data: Optional[aliases.AnySecureData] = ..., front_side: Optional[aliases.AnySecureFile] = ..., reverse_side: Optional[aliases.AnySecureFile] = ..., selfie: Optional[aliases.AnySecureFile] = ..., translation: Optional[list[aliases.AnySecureFile]] = ..., files: Optional[list[aliases.AnySecureFile]] = ..., plain_data: Optional[aliases.AnySecurePlainData] = ...): ...

    def __init__(self, type, hash, _='secureValue', **kwargs):
        kwargs['type'] = type
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def data(self) -> Optional[aliases.AnySecureData]:
        return build_object(self['data'])

    @property
    def front_side(self) -> Optional[aliases.AnySecureFile]:
        return build_object(self['front_side'])

    @property
    def reverse_side(self) -> Optional[aliases.AnySecureFile]:
        return build_object(self['reverse_side'])

    @property
    def selfie(self) -> Optional[aliases.AnySecureFile]:
        return build_object(self['selfie'])

    @property
    def translation(self) -> Optional[list[aliases.AnySecureFile]]:
        return build_object(self['translation'])

    @property
    def files(self) -> Optional[list[aliases.AnySecureFile]]:
        return build_object(self['files'])

    @property
    def plain_data(self) -> Optional[aliases.AnySecurePlainData]:
        return build_object(self['plain_data'])

    @property
    def hash(self) -> bytes:
        return self['hash']


class InputSecureValue(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, data: Optional[aliases.AnySecureData] = ..., front_side: Optional[aliases.AnyInputSecureFile] = ..., reverse_side: Optional[aliases.AnyInputSecureFile] = ..., selfie: Optional[aliases.AnyInputSecureFile] = ..., translation: Optional[list[aliases.AnyInputSecureFile]] = ..., files: Optional[list[aliases.AnyInputSecureFile]] = ..., plain_data: Optional[aliases.AnySecurePlainData] = ...): ...

    def __init__(self, type, _='inputSecureValue', **kwargs):
        kwargs['type'] = type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def data(self) -> Optional[aliases.AnySecureData]:
        return build_object(self['data'])

    @property
    def front_side(self) -> Optional[aliases.AnyInputSecureFile]:
        return build_object(self['front_side'])

    @property
    def reverse_side(self) -> Optional[aliases.AnyInputSecureFile]:
        return build_object(self['reverse_side'])

    @property
    def selfie(self) -> Optional[aliases.AnyInputSecureFile]:
        return build_object(self['selfie'])

    @property
    def translation(self) -> Optional[list[aliases.AnyInputSecureFile]]:
        return build_object(self['translation'])

    @property
    def files(self) -> Optional[list[aliases.AnyInputSecureFile]]:
        return build_object(self['files'])

    @property
    def plain_data(self) -> Optional[aliases.AnySecurePlainData]:
        return build_object(self['plain_data'])


class SecureValueHash(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, hash: bytes): ...

    def __init__(self, type, hash, _='secureValueHash', **kwargs):
        kwargs['type'] = type
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def hash(self) -> bytes:
        return self['hash']


class SecureValueErrorData(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, data_hash: bytes, field: str, text: str): ...

    def __init__(self, type, data_hash, field, text, _='secureValueErrorData', **kwargs):
        kwargs['type'] = type
        kwargs['data_hash'] = data_hash
        kwargs['field'] = field
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def data_hash(self) -> bytes:
        return self['data_hash']

    @property
    def field(self) -> str:
        return self['field']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorFrontSide(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: bytes, text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorFrontSide', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorReverseSide(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: bytes, text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorReverseSide', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorSelfie(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: bytes, text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorSelfie', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: bytes, text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorFile', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorFiles(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: list[bytes], text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorFiles', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> list[bytes]:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueError(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, hash: bytes, text: str): ...

    def __init__(self, type, hash, text, _='secureValueError', **kwargs):
        kwargs['type'] = type
        kwargs['hash'] = hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def hash(self) -> bytes:
        return self['hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorTranslationFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: bytes, text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorTranslationFile', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> bytes:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureValueErrorTranslationFiles(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, file_hash: list[bytes], text: str): ...

    def __init__(self, type, file_hash, text, _='secureValueErrorTranslationFiles', **kwargs):
        kwargs['type'] = type
        kwargs['file_hash'] = file_hash
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])

    @property
    def file_hash(self) -> list[bytes]:
        return self['file_hash']

    @property
    def text(self) -> str:
        return self['text']


class SecureCredentialsEncrypted(dict):
    __slots__ = ()

    @overload
    def __init__(self, data: bytes, hash: bytes, secret: bytes): ...

    def __init__(self, data, hash, secret, _='secureCredentialsEncrypted', **kwargs):
        kwargs['data'] = data
        kwargs['hash'] = hash
        kwargs['secret'] = secret
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def data(self) -> bytes:
        return self['data']

    @property
    def hash(self) -> bytes:
        return self['hash']

    @property
    def secret(self) -> bytes:
        return self['secret']


class SavedPhoneContact(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone: str, first_name: str, last_name: str, date: int): ...

    def __init__(self, phone, first_name, last_name, date, _='savedPhoneContact', **kwargs):
        kwargs['phone'] = phone
        kwargs['first_name'] = first_name
        kwargs['last_name'] = last_name
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone(self) -> str:
        return self['phone']

    @property
    def first_name(self) -> str:
        return self['first_name']

    @property
    def last_name(self) -> str:
        return self['last_name']

    @property
    def date(self) -> int:
        return self['date']


class PasswordKdfAlgoUnknown(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='passwordKdfAlgoUnknown'):
        dict.__init__(self, _=_)


class PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow(dict):
    __slots__ = ()

    @overload
    def __init__(self, salt1: bytes, salt2: bytes, g: int, p: bytes): ...

    def __init__(self, salt1, salt2, g, p, _='passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow', **kwargs):
        kwargs['salt1'] = salt1
        kwargs['salt2'] = salt2
        kwargs['g'] = g
        kwargs['p'] = p
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def salt1(self) -> bytes:
        return self['salt1']

    @property
    def salt2(self) -> bytes:
        return self['salt2']

    @property
    def g(self) -> int:
        return self['g']

    @property
    def p(self) -> bytes:
        return self['p']


class SecurePasswordKdfAlgoUnknown(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='securePasswordKdfAlgoUnknown'):
        dict.__init__(self, _=_)


class SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(dict):
    __slots__ = ()

    @overload
    def __init__(self, salt: bytes): ...

    def __init__(self, salt, _='securePasswordKdfAlgoPBKDF2HMACSHA512iter100000', **kwargs):
        kwargs['salt'] = salt
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def salt(self) -> bytes:
        return self['salt']


class SecurePasswordKdfAlgoSHA512(dict):
    __slots__ = ()

    @overload
    def __init__(self, salt: bytes): ...

    def __init__(self, salt, _='securePasswordKdfAlgoSHA512', **kwargs):
        kwargs['salt'] = salt
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def salt(self) -> bytes:
        return self['salt']


class SecureSecretSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, secure_algo: aliases.AnySecurePasswordKdfAlgo, secure_secret: bytes, secure_secret_id: int): ...

    def __init__(self, secure_algo, secure_secret, secure_secret_id, _='secureSecretSettings', **kwargs):
        kwargs['secure_algo'] = secure_algo
        kwargs['secure_secret'] = secure_secret
        kwargs['secure_secret_id'] = secure_secret_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def secure_algo(self) -> aliases.AnySecurePasswordKdfAlgo:
        return build_object(self['secure_algo'])

    @property
    def secure_secret(self) -> bytes:
        return self['secure_secret']

    @property
    def secure_secret_id(self) -> int:
        return self['secure_secret_id']


class InputCheckPasswordEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputCheckPasswordEmpty'):
        dict.__init__(self, _=_)


class InputCheckPasswordSRP(dict):
    __slots__ = ()

    @overload
    def __init__(self, srp_id: int, A: bytes, M1: bytes): ...

    def __init__(self, srp_id, A, M1, _='inputCheckPasswordSRP', **kwargs):
        kwargs['srp_id'] = srp_id
        kwargs['A'] = A
        kwargs['M1'] = M1
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def srp_id(self) -> int:
        return self['srp_id']

    @property
    def A(self) -> bytes:
        return self['A']

    @property
    def M1(self) -> bytes:
        return self['M1']


class SecureRequiredType(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: aliases.AnySecureValueType, native_names: Optional[bool] = ..., selfie_required: Optional[bool] = ..., translation_required: Optional[bool] = ...): ...

    def __init__(self, type, _='secureRequiredType', **kwargs):
        kwargs['type'] = type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def native_names(self) -> Optional[bool]:
        return self['native_names']

    @property
    def selfie_required(self) -> Optional[bool]:
        return self['selfie_required']

    @property
    def translation_required(self) -> Optional[bool]:
        return self['translation_required']

    @property
    def type(self) -> aliases.AnySecureValueType:
        return build_object(self['type'])


class SecureRequiredTypeOneOf(dict):
    __slots__ = ()

    @overload
    def __init__(self, types: list[aliases.AnySecureRequiredType]): ...

    def __init__(self, types, _='secureRequiredTypeOneOf', **kwargs):
        kwargs['types'] = types
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def types(self) -> list[aliases.AnySecureRequiredType]:
        return build_object(self['types'])


class InputAppEvent(dict):
    __slots__ = ()

    @overload
    def __init__(self, time: float, type: str, peer: int, data: aliases.AnyJSONValue): ...

    def __init__(self, time, type, peer, data, _='inputAppEvent', **kwargs):
        kwargs['time'] = time
        kwargs['type'] = type
        kwargs['peer'] = peer
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def time(self) -> float:
        return self['time']

    @property
    def type(self) -> str:
        return self['type']

    @property
    def peer(self) -> int:
        return self['peer']

    @property
    def data(self) -> aliases.AnyJSONValue:
        return build_object(self['data'])


class JsonObjectValue(dict):
    __slots__ = ()

    @overload
    def __init__(self, key: str, value: aliases.AnyJSONValue): ...

    def __init__(self, key, value, _='jsonObjectValue', **kwargs):
        kwargs['key'] = key
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def key(self) -> str:
        return self['key']

    @property
    def value(self) -> aliases.AnyJSONValue:
        return build_object(self['value'])


class JsonNull(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='jsonNull'):
        dict.__init__(self, _=_)


class JsonBool(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: bool): ...

    def __init__(self, value, _='jsonBool', **kwargs):
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> bool:
        return self['value']


class JsonNumber(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: float): ...

    def __init__(self, value, _='jsonNumber', **kwargs):
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> float:
        return self['value']


class JsonString(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: str): ...

    def __init__(self, value, _='jsonString', **kwargs):
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> str:
        return self['value']


class JsonArray(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: list[aliases.AnyJSONValue]): ...

    def __init__(self, value, _='jsonArray', **kwargs):
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> list[aliases.AnyJSONValue]:
        return build_object(self['value'])


class JsonObject(dict):
    __slots__ = ()

    @overload
    def __init__(self, value: list[aliases.AnyJSONObjectValue]): ...

    def __init__(self, value, _='jsonObject', **kwargs):
        kwargs['value'] = value
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def value(self) -> list[aliases.AnyJSONObjectValue]:
        return build_object(self['value'])


class PageTableCell(dict):
    __slots__ = ()

    @overload
    def __init__(self, header: Optional[bool] = ..., align_center: Optional[bool] = ..., align_right: Optional[bool] = ..., valign_middle: Optional[bool] = ..., valign_bottom: Optional[bool] = ..., text: Optional[aliases.AnyRichText] = ..., colspan: Optional[int] = ..., rowspan: Optional[int] = ...): ...

    def __init__(self, _='pageTableCell', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def header(self) -> Optional[bool]:
        return self['header']

    @property
    def align_center(self) -> Optional[bool]:
        return self['align_center']

    @property
    def align_right(self) -> Optional[bool]:
        return self['align_right']

    @property
    def valign_middle(self) -> Optional[bool]:
        return self['valign_middle']

    @property
    def valign_bottom(self) -> Optional[bool]:
        return self['valign_bottom']

    @property
    def text(self) -> Optional[aliases.AnyRichText]:
        return build_object(self['text'])

    @property
    def colspan(self) -> Optional[int]:
        return self['colspan']

    @property
    def rowspan(self) -> Optional[int]:
        return self['rowspan']


class PageTableRow(dict):
    __slots__ = ()

    @overload
    def __init__(self, cells: list[aliases.AnyPageTableCell]): ...

    def __init__(self, cells, _='pageTableRow', **kwargs):
        kwargs['cells'] = cells
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def cells(self) -> list[aliases.AnyPageTableCell]:
        return build_object(self['cells'])


class PageCaption(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText, credit: aliases.AnyRichText): ...

    def __init__(self, text, credit, _='pageCaption', **kwargs):
        kwargs['text'] = text
        kwargs['credit'] = credit
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])

    @property
    def credit(self) -> aliases.AnyRichText:
        return build_object(self['credit'])


class PageListItemText(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyRichText): ...

    def __init__(self, text, _='pageListItemText', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageListItemBlocks(dict):
    __slots__ = ()

    @overload
    def __init__(self, blocks: list[aliases.AnyPageBlock]): ...

    def __init__(self, blocks, _='pageListItemBlocks', **kwargs):
        kwargs['blocks'] = blocks
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocks(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['blocks'])


class PageListOrderedItemText(dict):
    __slots__ = ()

    @overload
    def __init__(self, num: str, text: aliases.AnyRichText): ...

    def __init__(self, num, text, _='pageListOrderedItemText', **kwargs):
        kwargs['num'] = num
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def num(self) -> str:
        return self['num']

    @property
    def text(self) -> aliases.AnyRichText:
        return build_object(self['text'])


class PageListOrderedItemBlocks(dict):
    __slots__ = ()

    @overload
    def __init__(self, num: str, blocks: list[aliases.AnyPageBlock]): ...

    def __init__(self, num, blocks, _='pageListOrderedItemBlocks', **kwargs):
        kwargs['num'] = num
        kwargs['blocks'] = blocks
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def num(self) -> str:
        return self['num']

    @property
    def blocks(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['blocks'])


class PageRelatedArticle(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, webpage_id: int, title: Optional[str] = ..., description: Optional[str] = ..., photo_id: Optional[int] = ..., author: Optional[str] = ..., published_date: Optional[int] = ...): ...

    def __init__(self, url, webpage_id, _='pageRelatedArticle', **kwargs):
        kwargs['url'] = url
        kwargs['webpage_id'] = webpage_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def webpage_id(self) -> int:
        return self['webpage_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def photo_id(self) -> Optional[int]:
        return self['photo_id']

    @property
    def author(self) -> Optional[str]:
        return self['author']

    @property
    def published_date(self) -> Optional[int]:
        return self['published_date']


class Page(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, blocks: list[aliases.AnyPageBlock], photos: list[aliases.AnyPhoto], documents: list[aliases.AnyDocument], part: Optional[bool] = ..., rtl: Optional[bool] = ..., v2: Optional[bool] = ..., views: Optional[int] = ...): ...

    def __init__(self, url, blocks, photos, documents, _='page', **kwargs):
        kwargs['url'] = url
        kwargs['blocks'] = blocks
        kwargs['photos'] = photos
        kwargs['documents'] = documents
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def part(self) -> Optional[bool]:
        return self['part']

    @property
    def rtl(self) -> Optional[bool]:
        return self['rtl']

    @property
    def v2(self) -> Optional[bool]:
        return self['v2']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def blocks(self) -> list[aliases.AnyPageBlock]:
        return build_object(self['blocks'])

    @property
    def photos(self) -> list[aliases.AnyPhoto]:
        return build_object(self['photos'])

    @property
    def documents(self) -> list[aliases.AnyDocument]:
        return build_object(self['documents'])

    @property
    def views(self) -> Optional[int]:
        return self['views']


class PollAnswer(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: aliases.AnyTextWithEntities, option: bytes): ...

    def __init__(self, text, option, _='pollAnswer', **kwargs):
        kwargs['text'] = text
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> aliases.AnyTextWithEntities:
        return build_object(self['text'])

    @property
    def option(self) -> bytes:
        return self['option']


class Poll(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, question: aliases.AnyTextWithEntities, answers: list[aliases.AnyPollAnswer], closed: Optional[bool] = ..., public_voters: Optional[bool] = ..., multiple_choice: Optional[bool] = ..., quiz: Optional[bool] = ..., close_period: Optional[int] = ..., close_date: Optional[int] = ...): ...

    def __init__(self, id, question, answers, _='poll', **kwargs):
        kwargs['id'] = id
        kwargs['question'] = question
        kwargs['answers'] = answers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def closed(self) -> Optional[bool]:
        return self['closed']

    @property
    def public_voters(self) -> Optional[bool]:
        return self['public_voters']

    @property
    def multiple_choice(self) -> Optional[bool]:
        return self['multiple_choice']

    @property
    def quiz(self) -> Optional[bool]:
        return self['quiz']

    @property
    def question(self) -> aliases.AnyTextWithEntities:
        return build_object(self['question'])

    @property
    def answers(self) -> list[aliases.AnyPollAnswer]:
        return build_object(self['answers'])

    @property
    def close_period(self) -> Optional[int]:
        return self['close_period']

    @property
    def close_date(self) -> Optional[int]:
        return self['close_date']


class PollAnswerVoters(dict):
    __slots__ = ()

    @overload
    def __init__(self, option: bytes, voters: int, chosen: Optional[bool] = ..., correct: Optional[bool] = ...): ...

    def __init__(self, option, voters, _='pollAnswerVoters', **kwargs):
        kwargs['option'] = option
        kwargs['voters'] = voters
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chosen(self) -> Optional[bool]:
        return self['chosen']

    @property
    def correct(self) -> Optional[bool]:
        return self['correct']

    @property
    def option(self) -> bytes:
        return self['option']

    @property
    def voters(self) -> int:
        return self['voters']


class PollResults(dict):
    __slots__ = ()

    @overload
    def __init__(self, min: Optional[bool] = ..., results: Optional[list[aliases.AnyPollAnswerVoters]] = ..., total_voters: Optional[int] = ..., recent_voters: Optional[list[aliases.AnyPeer]] = ..., solution: Optional[str] = ..., solution_entities: Optional[list[aliases.AnyMessageEntity]] = ...): ...

    def __init__(self, _='pollResults', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def results(self) -> Optional[list[aliases.AnyPollAnswerVoters]]:
        return build_object(self['results'])

    @property
    def total_voters(self) -> Optional[int]:
        return self['total_voters']

    @property
    def recent_voters(self) -> Optional[list[aliases.AnyPeer]]:
        return build_object(self['recent_voters'])

    @property
    def solution(self) -> Optional[str]:
        return self['solution']

    @property
    def solution_entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['solution_entities'])


class ChatOnlines(dict):
    __slots__ = ()

    @overload
    def __init__(self, onlines: int): ...

    def __init__(self, onlines, _='chatOnlines', **kwargs):
        kwargs['onlines'] = onlines
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def onlines(self) -> int:
        return self['onlines']


class StatsURL(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='statsURL', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class ChatAdminRights(dict):
    __slots__ = ()

    @overload
    def __init__(self, change_info: Optional[bool] = ..., post_messages: Optional[bool] = ..., edit_messages: Optional[bool] = ..., delete_messages: Optional[bool] = ..., ban_users: Optional[bool] = ..., invite_users: Optional[bool] = ..., pin_messages: Optional[bool] = ..., add_admins: Optional[bool] = ..., anonymous: Optional[bool] = ..., manage_call: Optional[bool] = ..., other: Optional[bool] = ..., manage_topics: Optional[bool] = ..., post_stories: Optional[bool] = ..., edit_stories: Optional[bool] = ..., delete_stories: Optional[bool] = ..., manage_direct_messages: Optional[bool] = ..., manage_ranks: Optional[bool] = ...): ...

    def __init__(self, _='chatAdminRights', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def change_info(self) -> Optional[bool]:
        return self['change_info']

    @property
    def post_messages(self) -> Optional[bool]:
        return self['post_messages']

    @property
    def edit_messages(self) -> Optional[bool]:
        return self['edit_messages']

    @property
    def delete_messages(self) -> Optional[bool]:
        return self['delete_messages']

    @property
    def ban_users(self) -> Optional[bool]:
        return self['ban_users']

    @property
    def invite_users(self) -> Optional[bool]:
        return self['invite_users']

    @property
    def pin_messages(self) -> Optional[bool]:
        return self['pin_messages']

    @property
    def add_admins(self) -> Optional[bool]:
        return self['add_admins']

    @property
    def anonymous(self) -> Optional[bool]:
        return self['anonymous']

    @property
    def manage_call(self) -> Optional[bool]:
        return self['manage_call']

    @property
    def other(self) -> Optional[bool]:
        return self['other']

    @property
    def manage_topics(self) -> Optional[bool]:
        return self['manage_topics']

    @property
    def post_stories(self) -> Optional[bool]:
        return self['post_stories']

    @property
    def edit_stories(self) -> Optional[bool]:
        return self['edit_stories']

    @property
    def delete_stories(self) -> Optional[bool]:
        return self['delete_stories']

    @property
    def manage_direct_messages(self) -> Optional[bool]:
        return self['manage_direct_messages']

    @property
    def manage_ranks(self) -> Optional[bool]:
        return self['manage_ranks']


class ChatBannedRights(dict):
    __slots__ = ()

    @overload
    def __init__(self, until_date: int, view_messages: Optional[bool] = ..., send_messages: Optional[bool] = ..., send_media: Optional[bool] = ..., send_stickers: Optional[bool] = ..., send_gifs: Optional[bool] = ..., send_games: Optional[bool] = ..., send_inline: Optional[bool] = ..., embed_links: Optional[bool] = ..., send_polls: Optional[bool] = ..., change_info: Optional[bool] = ..., invite_users: Optional[bool] = ..., pin_messages: Optional[bool] = ..., manage_topics: Optional[bool] = ..., send_photos: Optional[bool] = ..., send_videos: Optional[bool] = ..., send_roundvideos: Optional[bool] = ..., send_audios: Optional[bool] = ..., send_voices: Optional[bool] = ..., send_docs: Optional[bool] = ..., send_plain: Optional[bool] = ..., edit_rank: Optional[bool] = ...): ...

    def __init__(self, until_date, _='chatBannedRights', **kwargs):
        kwargs['until_date'] = until_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def view_messages(self) -> Optional[bool]:
        return self['view_messages']

    @property
    def send_messages(self) -> Optional[bool]:
        return self['send_messages']

    @property
    def send_media(self) -> Optional[bool]:
        return self['send_media']

    @property
    def send_stickers(self) -> Optional[bool]:
        return self['send_stickers']

    @property
    def send_gifs(self) -> Optional[bool]:
        return self['send_gifs']

    @property
    def send_games(self) -> Optional[bool]:
        return self['send_games']

    @property
    def send_inline(self) -> Optional[bool]:
        return self['send_inline']

    @property
    def embed_links(self) -> Optional[bool]:
        return self['embed_links']

    @property
    def send_polls(self) -> Optional[bool]:
        return self['send_polls']

    @property
    def change_info(self) -> Optional[bool]:
        return self['change_info']

    @property
    def invite_users(self) -> Optional[bool]:
        return self['invite_users']

    @property
    def pin_messages(self) -> Optional[bool]:
        return self['pin_messages']

    @property
    def manage_topics(self) -> Optional[bool]:
        return self['manage_topics']

    @property
    def send_photos(self) -> Optional[bool]:
        return self['send_photos']

    @property
    def send_videos(self) -> Optional[bool]:
        return self['send_videos']

    @property
    def send_roundvideos(self) -> Optional[bool]:
        return self['send_roundvideos']

    @property
    def send_audios(self) -> Optional[bool]:
        return self['send_audios']

    @property
    def send_voices(self) -> Optional[bool]:
        return self['send_voices']

    @property
    def send_docs(self) -> Optional[bool]:
        return self['send_docs']

    @property
    def send_plain(self) -> Optional[bool]:
        return self['send_plain']

    @property
    def edit_rank(self) -> Optional[bool]:
        return self['edit_rank']

    @property
    def until_date(self) -> int:
        return self['until_date']


class InputWallPaper(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputWallPaper', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputWallPaperSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputWallPaperSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class InputWallPaperNoFile(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='inputWallPaperNoFile', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class CodeSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, allow_flashcall: Optional[bool] = ..., current_number: Optional[bool] = ..., allow_app_hash: Optional[bool] = ..., allow_missed_call: Optional[bool] = ..., allow_firebase: Optional[bool] = ..., unknown_number: Optional[bool] = ..., logout_tokens: Optional[list[bytes]] = ..., token: Optional[str] = ..., app_sandbox: Optional[bool] = ...): ...

    def __init__(self, _='codeSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def allow_flashcall(self) -> Optional[bool]:
        return self['allow_flashcall']

    @property
    def current_number(self) -> Optional[bool]:
        return self['current_number']

    @property
    def allow_app_hash(self) -> Optional[bool]:
        return self['allow_app_hash']

    @property
    def allow_missed_call(self) -> Optional[bool]:
        return self['allow_missed_call']

    @property
    def allow_firebase(self) -> Optional[bool]:
        return self['allow_firebase']

    @property
    def unknown_number(self) -> Optional[bool]:
        return self['unknown_number']

    @property
    def logout_tokens(self) -> Optional[list[bytes]]:
        return self['logout_tokens']

    @property
    def token(self) -> Optional[str]:
        return self['token']

    @property
    def app_sandbox(self) -> Optional[bool]:
        return self['app_sandbox']


class WallPaperSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, blur: Optional[bool] = ..., motion: Optional[bool] = ..., background_color: Optional[int] = ..., second_background_color: Optional[int] = ..., third_background_color: Optional[int] = ..., fourth_background_color: Optional[int] = ..., intensity: Optional[int] = ..., rotation: Optional[int] = ..., emoticon: Optional[str] = ...): ...

    def __init__(self, _='wallPaperSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blur(self) -> Optional[bool]:
        return self['blur']

    @property
    def motion(self) -> Optional[bool]:
        return self['motion']

    @property
    def background_color(self) -> Optional[int]:
        return self['background_color']

    @property
    def second_background_color(self) -> Optional[int]:
        return self['second_background_color']

    @property
    def third_background_color(self) -> Optional[int]:
        return self['third_background_color']

    @property
    def fourth_background_color(self) -> Optional[int]:
        return self['fourth_background_color']

    @property
    def intensity(self) -> Optional[int]:
        return self['intensity']

    @property
    def rotation(self) -> Optional[int]:
        return self['rotation']

    @property
    def emoticon(self) -> Optional[str]:
        return self['emoticon']


class AutoDownloadSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, photo_size_max: int, video_size_max: int, file_size_max: int, video_upload_maxbitrate: int, small_queue_active_operations_max: int, large_queue_active_operations_max: int, disabled: Optional[bool] = ..., video_preload_large: Optional[bool] = ..., audio_preload_next: Optional[bool] = ..., phonecalls_less_data: Optional[bool] = ..., stories_preload: Optional[bool] = ...): ...

    def __init__(self, photo_size_max, video_size_max, file_size_max, video_upload_maxbitrate, small_queue_active_operations_max, large_queue_active_operations_max, _='autoDownloadSettings', **kwargs):
        kwargs['photo_size_max'] = photo_size_max
        kwargs['video_size_max'] = video_size_max
        kwargs['file_size_max'] = file_size_max
        kwargs['video_upload_maxbitrate'] = video_upload_maxbitrate
        kwargs['small_queue_active_operations_max'] = small_queue_active_operations_max
        kwargs['large_queue_active_operations_max'] = large_queue_active_operations_max
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def disabled(self) -> Optional[bool]:
        return self['disabled']

    @property
    def video_preload_large(self) -> Optional[bool]:
        return self['video_preload_large']

    @property
    def audio_preload_next(self) -> Optional[bool]:
        return self['audio_preload_next']

    @property
    def phonecalls_less_data(self) -> Optional[bool]:
        return self['phonecalls_less_data']

    @property
    def stories_preload(self) -> Optional[bool]:
        return self['stories_preload']

    @property
    def photo_size_max(self) -> int:
        return self['photo_size_max']

    @property
    def video_size_max(self) -> int:
        return self['video_size_max']

    @property
    def file_size_max(self) -> int:
        return self['file_size_max']

    @property
    def video_upload_maxbitrate(self) -> int:
        return self['video_upload_maxbitrate']

    @property
    def small_queue_active_operations_max(self) -> int:
        return self['small_queue_active_operations_max']

    @property
    def large_queue_active_operations_max(self) -> int:
        return self['large_queue_active_operations_max']


class EmojiKeyword(dict):
    __slots__ = ()

    @overload
    def __init__(self, keyword: str, emoticons: list[str]): ...

    def __init__(self, keyword, emoticons, _='emojiKeyword', **kwargs):
        kwargs['keyword'] = keyword
        kwargs['emoticons'] = emoticons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def keyword(self) -> str:
        return self['keyword']

    @property
    def emoticons(self) -> list[str]:
        return self['emoticons']


class EmojiKeywordDeleted(dict):
    __slots__ = ()

    @overload
    def __init__(self, keyword: str, emoticons: list[str]): ...

    def __init__(self, keyword, emoticons, _='emojiKeywordDeleted', **kwargs):
        kwargs['keyword'] = keyword
        kwargs['emoticons'] = emoticons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def keyword(self) -> str:
        return self['keyword']

    @property
    def emoticons(self) -> list[str]:
        return self['emoticons']


class EmojiKeywordsDifference(dict):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str, from_version: int, version: int, keywords: list[aliases.AnyEmojiKeyword]): ...

    def __init__(self, lang_code, from_version, version, keywords, _='emojiKeywordsDifference', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['from_version'] = from_version
        kwargs['version'] = version
        kwargs['keywords'] = keywords
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']

    @property
    def from_version(self) -> int:
        return self['from_version']

    @property
    def version(self) -> int:
        return self['version']

    @property
    def keywords(self) -> list[aliases.AnyEmojiKeyword]:
        return build_object(self['keywords'])


class EmojiURL(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str): ...

    def __init__(self, url, _='emojiURL', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']


class EmojiLanguage(dict):
    __slots__ = ()

    @overload
    def __init__(self, lang_code: str): ...

    def __init__(self, lang_code, _='emojiLanguage', **kwargs):
        kwargs['lang_code'] = lang_code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def lang_code(self) -> str:
        return self['lang_code']


class Folder(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: str, autofill_new_broadcasts: Optional[bool] = ..., autofill_public_groups: Optional[bool] = ..., autofill_new_correspondents: Optional[bool] = ..., photo: Optional[aliases.AnyChatPhoto] = ...): ...

    def __init__(self, id, title, _='folder', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def autofill_new_broadcasts(self) -> Optional[bool]:
        return self['autofill_new_broadcasts']

    @property
    def autofill_public_groups(self) -> Optional[bool]:
        return self['autofill_public_groups']

    @property
    def autofill_new_correspondents(self) -> Optional[bool]:
        return self['autofill_new_correspondents']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def photo(self) -> Optional[aliases.AnyChatPhoto]:
        return build_object(self['photo'])


class InputFolderPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, folder_id: int): ...

    def __init__(self, peer, folder_id, _='inputFolderPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['folder_id'] = folder_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def folder_id(self) -> int:
        return self['folder_id']


class FolderPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, folder_id: int): ...

    def __init__(self, peer, folder_id, _='folderPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['folder_id'] = folder_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def folder_id(self) -> int:
        return self['folder_id']


class UrlAuthResultRequest(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyUser, domain: str, request_write_access: Optional[bool] = ..., request_phone_number: Optional[bool] = ..., match_codes_first: Optional[bool] = ..., browser: Optional[str] = ..., platform: Optional[str] = ..., ip: Optional[str] = ..., region: Optional[str] = ..., match_codes: Optional[list[str]] = ..., user_id_hint: Optional[int] = ...): ...

    def __init__(self, bot, domain, _='urlAuthResultRequest', **kwargs):
        kwargs['bot'] = bot
        kwargs['domain'] = domain
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def request_write_access(self) -> Optional[bool]:
        return self['request_write_access']

    @property
    def request_phone_number(self) -> Optional[bool]:
        return self['request_phone_number']

    @property
    def match_codes_first(self) -> Optional[bool]:
        return self['match_codes_first']

    @property
    def bot(self) -> aliases.AnyUser:
        return build_object(self['bot'])

    @property
    def domain(self) -> str:
        return self['domain']

    @property
    def browser(self) -> Optional[str]:
        return self['browser']

    @property
    def platform(self) -> Optional[str]:
        return self['platform']

    @property
    def ip(self) -> Optional[str]:
        return self['ip']

    @property
    def region(self) -> Optional[str]:
        return self['region']

    @property
    def match_codes(self) -> Optional[list[str]]:
        return self['match_codes']

    @property
    def user_id_hint(self) -> Optional[int]:
        return self['user_id_hint']


class UrlAuthResultAccepted(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: Optional[str] = ...): ...

    def __init__(self, _='urlAuthResultAccepted', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> Optional[str]:
        return self['url']


class UrlAuthResultDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='urlAuthResultDefault'):
        dict.__init__(self, _=_)


class ChannelLocationEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='channelLocationEmpty'):
        dict.__init__(self, _=_)


class ChannelLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, geo_point: aliases.AnyGeoPoint, address: str): ...

    def __init__(self, geo_point, address, _='channelLocation', **kwargs):
        kwargs['geo_point'] = geo_point
        kwargs['address'] = address
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo_point'])

    @property
    def address(self) -> str:
        return self['address']


class PeerLocated(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, expires: int, distance: int): ...

    def __init__(self, peer, expires, distance, _='peerLocated', **kwargs):
        kwargs['peer'] = peer
        kwargs['expires'] = expires
        kwargs['distance'] = distance
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def distance(self) -> int:
        return self['distance']


class PeerSelfLocated(dict):
    __slots__ = ()

    @overload
    def __init__(self, expires: int): ...

    def __init__(self, expires, _='peerSelfLocated', **kwargs):
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def expires(self) -> int:
        return self['expires']


class RestrictionReason(dict):
    __slots__ = ()

    @overload
    def __init__(self, platform: str, reason: str, text: str): ...

    def __init__(self, platform, reason, text, _='restrictionReason', **kwargs):
        kwargs['platform'] = platform
        kwargs['reason'] = reason
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def platform(self) -> str:
        return self['platform']

    @property
    def reason(self) -> str:
        return self['reason']

    @property
    def text(self) -> str:
        return self['text']


class InputTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputTheme', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputThemeSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputThemeSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class Theme(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, slug: str, title: str, creator: Optional[bool] = ..., default: Optional[bool] = ..., for_chat: Optional[bool] = ..., document: Optional[aliases.AnyDocument] = ..., settings: Optional[list[aliases.AnyThemeSettings]] = ..., emoticon: Optional[str] = ..., installs_count: Optional[int] = ...): ...

    def __init__(self, id, access_hash, slug, title, _='theme', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['slug'] = slug
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def default(self) -> Optional[bool]:
        return self['default']

    @property
    def for_chat(self) -> Optional[bool]:
        return self['for_chat']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def settings(self) -> Optional[list[aliases.AnyThemeSettings]]:
        return build_object(self['settings'])

    @property
    def emoticon(self) -> Optional[str]:
        return self['emoticon']

    @property
    def installs_count(self) -> Optional[int]:
        return self['installs_count']


class BaseThemeClassic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='baseThemeClassic'):
        dict.__init__(self, _=_)


class BaseThemeDay(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='baseThemeDay'):
        dict.__init__(self, _=_)


class BaseThemeNight(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='baseThemeNight'):
        dict.__init__(self, _=_)


class BaseThemeTinted(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='baseThemeTinted'):
        dict.__init__(self, _=_)


class BaseThemeArctic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='baseThemeArctic'):
        dict.__init__(self, _=_)


class InputThemeSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, base_theme: aliases.AnyBaseTheme, accent_color: int, message_colors_animated: Optional[bool] = ..., outbox_accent_color: Optional[int] = ..., message_colors: Optional[list[int]] = ..., wallpaper: Optional[aliases.AnyInputWallPaper] = ..., wallpaper_settings: Optional[aliases.AnyWallPaperSettings] = ...): ...

    def __init__(self, base_theme, accent_color, _='inputThemeSettings', **kwargs):
        kwargs['base_theme'] = base_theme
        kwargs['accent_color'] = accent_color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message_colors_animated(self) -> Optional[bool]:
        return self['message_colors_animated']

    @property
    def base_theme(self) -> aliases.AnyBaseTheme:
        return build_object(self['base_theme'])

    @property
    def accent_color(self) -> int:
        return self['accent_color']

    @property
    def outbox_accent_color(self) -> Optional[int]:
        return self['outbox_accent_color']

    @property
    def message_colors(self) -> Optional[list[int]]:
        return self['message_colors']

    @property
    def wallpaper(self) -> Optional[aliases.AnyInputWallPaper]:
        return build_object(self['wallpaper'])

    @property
    def wallpaper_settings(self) -> Optional[aliases.AnyWallPaperSettings]:
        return build_object(self['wallpaper_settings'])


class ThemeSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, base_theme: aliases.AnyBaseTheme, accent_color: int, message_colors_animated: Optional[bool] = ..., outbox_accent_color: Optional[int] = ..., message_colors: Optional[list[int]] = ..., wallpaper: Optional[aliases.AnyWallPaper] = ...): ...

    def __init__(self, base_theme, accent_color, _='themeSettings', **kwargs):
        kwargs['base_theme'] = base_theme
        kwargs['accent_color'] = accent_color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message_colors_animated(self) -> Optional[bool]:
        return self['message_colors_animated']

    @property
    def base_theme(self) -> aliases.AnyBaseTheme:
        return build_object(self['base_theme'])

    @property
    def accent_color(self) -> int:
        return self['accent_color']

    @property
    def outbox_accent_color(self) -> Optional[int]:
        return self['outbox_accent_color']

    @property
    def message_colors(self) -> Optional[list[int]]:
        return self['message_colors']

    @property
    def wallpaper(self) -> Optional[aliases.AnyWallPaper]:
        return build_object(self['wallpaper'])


class WebPageAttributeTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, documents: Optional[list[aliases.AnyDocument]] = ..., settings: Optional[aliases.AnyThemeSettings] = ...): ...

    def __init__(self, _='webPageAttributeTheme', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def documents(self) -> Optional[list[aliases.AnyDocument]]:
        return build_object(self['documents'])

    @property
    def settings(self) -> Optional[aliases.AnyThemeSettings]:
        return build_object(self['settings'])


class WebPageAttributeStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, id: int, story: Optional[aliases.AnyStoryItem] = ...): ...

    def __init__(self, peer, id, _='webPageAttributeStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def id(self) -> int:
        return self['id']

    @property
    def story(self) -> Optional[aliases.AnyStoryItem]:
        return build_object(self['story'])


class WebPageAttributeStickerSet(dict):
    __slots__ = ()

    @overload
    def __init__(self, stickers: list[aliases.AnyDocument], emojis: Optional[bool] = ..., text_color: Optional[bool] = ...): ...

    def __init__(self, stickers, _='webPageAttributeStickerSet', **kwargs):
        kwargs['stickers'] = stickers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emojis(self) -> Optional[bool]:
        return self['emojis']

    @property
    def text_color(self) -> Optional[bool]:
        return self['text_color']

    @property
    def stickers(self) -> list[aliases.AnyDocument]:
        return build_object(self['stickers'])


class WebPageAttributeUniqueStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift): ...

    def __init__(self, gift, _='webPageAttributeUniqueStarGift', **kwargs):
        kwargs['gift'] = gift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])


class WebPageAttributeStarGiftCollection(dict):
    __slots__ = ()

    @overload
    def __init__(self, icons: list[aliases.AnyDocument]): ...

    def __init__(self, icons, _='webPageAttributeStarGiftCollection', **kwargs):
        kwargs['icons'] = icons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def icons(self) -> list[aliases.AnyDocument]:
        return build_object(self['icons'])


class WebPageAttributeStarGiftAuction(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, end_date: int): ...

    def __init__(self, gift, end_date, _='webPageAttributeStarGiftAuction', **kwargs):
        kwargs['gift'] = gift
        kwargs['end_date'] = end_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def end_date(self) -> int:
        return self['end_date']


class BankCardOpenUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, name: str): ...

    def __init__(self, url, name, _='bankCardOpenUrl', **kwargs):
        kwargs['url'] = url
        kwargs['name'] = name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def name(self) -> str:
        return self['name']


class DialogFilter(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: aliases.AnyTextWithEntities, pinned_peers: list[aliases.AnyInputPeer], include_peers: list[aliases.AnyInputPeer], exclude_peers: list[aliases.AnyInputPeer], contacts: Optional[bool] = ..., non_contacts: Optional[bool] = ..., groups: Optional[bool] = ..., broadcasts: Optional[bool] = ..., bots: Optional[bool] = ..., exclude_muted: Optional[bool] = ..., exclude_read: Optional[bool] = ..., exclude_archived: Optional[bool] = ..., title_noanimate: Optional[bool] = ..., emoticon: Optional[str] = ..., color: Optional[int] = ...): ...

    def __init__(self, id, title, pinned_peers, include_peers, exclude_peers, _='dialogFilter', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['pinned_peers'] = pinned_peers
        kwargs['include_peers'] = include_peers
        kwargs['exclude_peers'] = exclude_peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def non_contacts(self) -> Optional[bool]:
        return self['non_contacts']

    @property
    def groups(self) -> Optional[bool]:
        return self['groups']

    @property
    def broadcasts(self) -> Optional[bool]:
        return self['broadcasts']

    @property
    def bots(self) -> Optional[bool]:
        return self['bots']

    @property
    def exclude_muted(self) -> Optional[bool]:
        return self['exclude_muted']

    @property
    def exclude_read(self) -> Optional[bool]:
        return self['exclude_read']

    @property
    def exclude_archived(self) -> Optional[bool]:
        return self['exclude_archived']

    @property
    def title_noanimate(self) -> Optional[bool]:
        return self['title_noanimate']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])

    @property
    def emoticon(self) -> Optional[str]:
        return self['emoticon']

    @property
    def color(self) -> Optional[int]:
        return self['color']

    @property
    def pinned_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['pinned_peers'])

    @property
    def include_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['include_peers'])

    @property
    def exclude_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['exclude_peers'])


class DialogFilterDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='dialogFilterDefault'):
        dict.__init__(self, _=_)


class DialogFilterChatlist(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: aliases.AnyTextWithEntities, pinned_peers: list[aliases.AnyInputPeer], include_peers: list[aliases.AnyInputPeer], has_my_invites: Optional[bool] = ..., title_noanimate: Optional[bool] = ..., emoticon: Optional[str] = ..., color: Optional[int] = ...): ...

    def __init__(self, id, title, pinned_peers, include_peers, _='dialogFilterChatlist', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['pinned_peers'] = pinned_peers
        kwargs['include_peers'] = include_peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_my_invites(self) -> Optional[bool]:
        return self['has_my_invites']

    @property
    def title_noanimate(self) -> Optional[bool]:
        return self['title_noanimate']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])

    @property
    def emoticon(self) -> Optional[str]:
        return self['emoticon']

    @property
    def color(self) -> Optional[int]:
        return self['color']

    @property
    def pinned_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['pinned_peers'])

    @property
    def include_peers(self) -> list[aliases.AnyInputPeer]:
        return build_object(self['include_peers'])


class DialogFilterSuggested(dict):
    __slots__ = ()

    @overload
    def __init__(self, filter: aliases.AnyDialogFilter, description: str): ...

    def __init__(self, filter, description, _='dialogFilterSuggested', **kwargs):
        kwargs['filter'] = filter
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def filter(self) -> aliases.AnyDialogFilter:
        return build_object(self['filter'])

    @property
    def description(self) -> str:
        return self['description']


class StatsDateRangeDays(dict):
    __slots__ = ()

    @overload
    def __init__(self, min_date: int, max_date: int): ...

    def __init__(self, min_date, max_date, _='statsDateRangeDays', **kwargs):
        kwargs['min_date'] = min_date
        kwargs['max_date'] = max_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def min_date(self) -> int:
        return self['min_date']

    @property
    def max_date(self) -> int:
        return self['max_date']


class StatsAbsValueAndPrev(dict):
    __slots__ = ()

    @overload
    def __init__(self, current: float, previous: float): ...

    def __init__(self, current, previous, _='statsAbsValueAndPrev', **kwargs):
        kwargs['current'] = current
        kwargs['previous'] = previous
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def current(self) -> float:
        return self['current']

    @property
    def previous(self) -> float:
        return self['previous']


class StatsPercentValue(dict):
    __slots__ = ()

    @overload
    def __init__(self, part: float, total: float): ...

    def __init__(self, part, total, _='statsPercentValue', **kwargs):
        kwargs['part'] = part
        kwargs['total'] = total
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def part(self) -> float:
        return self['part']

    @property
    def total(self) -> float:
        return self['total']


class StatsGraphAsync(dict):
    __slots__ = ()

    @overload
    def __init__(self, token: str): ...

    def __init__(self, token, _='statsGraphAsync', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']


class StatsGraphError(dict):
    __slots__ = ()

    @overload
    def __init__(self, error: str): ...

    def __init__(self, error, _='statsGraphError', **kwargs):
        kwargs['error'] = error
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def error(self) -> str:
        return self['error']


class StatsGraph(dict):
    __slots__ = ()

    @overload
    def __init__(self, json: aliases.AnyDataJSON, zoom_token: Optional[str] = ...): ...

    def __init__(self, json, _='statsGraph', **kwargs):
        kwargs['json'] = json
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def json(self) -> aliases.AnyDataJSON:
        return build_object(self['json'])

    @property
    def zoom_token(self) -> Optional[str]:
        return self['zoom_token']


class VideoSize(dict):
    __slots__ = ()

    @overload
    def __init__(self, type: str, w: int, h: int, size: int, video_start_ts: Optional[float] = ...): ...

    def __init__(self, type, w, h, size, _='videoSize', **kwargs):
        kwargs['type'] = type
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['size'] = size
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def type(self) -> str:
        return self['type']

    @property
    def w(self) -> int:
        return self['w']

    @property
    def h(self) -> int:
        return self['h']

    @property
    def size(self) -> int:
        return self['size']

    @property
    def video_start_ts(self) -> Optional[float]:
        return self['video_start_ts']


class VideoSizeEmojiMarkup(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoji_id: int, background_colors: list[int]): ...

    def __init__(self, emoji_id, background_colors, _='videoSizeEmojiMarkup', **kwargs):
        kwargs['emoji_id'] = emoji_id
        kwargs['background_colors'] = background_colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoji_id(self) -> int:
        return self['emoji_id']

    @property
    def background_colors(self) -> list[int]:
        return self['background_colors']


class VideoSizeStickerMarkup(dict):
    __slots__ = ()

    @overload
    def __init__(self, stickerset: aliases.AnyInputStickerSet, sticker_id: int, background_colors: list[int]): ...

    def __init__(self, stickerset, sticker_id, background_colors, _='videoSizeStickerMarkup', **kwargs):
        kwargs['stickerset'] = stickerset
        kwargs['sticker_id'] = sticker_id
        kwargs['background_colors'] = background_colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stickerset(self) -> aliases.AnyInputStickerSet:
        return build_object(self['stickerset'])

    @property
    def sticker_id(self) -> int:
        return self['sticker_id']

    @property
    def background_colors(self) -> list[int]:
        return self['background_colors']


class StatsGroupTopPoster(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, messages: int, avg_chars: int): ...

    def __init__(self, user_id, messages, avg_chars, _='statsGroupTopPoster', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['messages'] = messages
        kwargs['avg_chars'] = avg_chars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def messages(self) -> int:
        return self['messages']

    @property
    def avg_chars(self) -> int:
        return self['avg_chars']


class StatsGroupTopAdmin(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, deleted: int, kicked: int, banned: int): ...

    def __init__(self, user_id, deleted, kicked, banned, _='statsGroupTopAdmin', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['deleted'] = deleted
        kwargs['kicked'] = kicked
        kwargs['banned'] = banned
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def deleted(self) -> int:
        return self['deleted']

    @property
    def kicked(self) -> int:
        return self['kicked']

    @property
    def banned(self) -> int:
        return self['banned']


class StatsGroupTopInviter(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, invitations: int): ...

    def __init__(self, user_id, invitations, _='statsGroupTopInviter', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['invitations'] = invitations
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def invitations(self) -> int:
        return self['invitations']


class GlobalPrivacySettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, archive_and_mute_new_noncontact_peers: Optional[bool] = ..., keep_archived_unmuted: Optional[bool] = ..., keep_archived_folders: Optional[bool] = ..., hide_read_marks: Optional[bool] = ..., new_noncontact_peers_require_premium: Optional[bool] = ..., display_gifts_button: Optional[bool] = ..., noncontact_peers_paid_stars: Optional[int] = ..., disallowed_gifts: Optional[aliases.AnyDisallowedGiftsSettings] = ...): ...

    def __init__(self, _='globalPrivacySettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def archive_and_mute_new_noncontact_peers(self) -> Optional[bool]:
        return self['archive_and_mute_new_noncontact_peers']

    @property
    def keep_archived_unmuted(self) -> Optional[bool]:
        return self['keep_archived_unmuted']

    @property
    def keep_archived_folders(self) -> Optional[bool]:
        return self['keep_archived_folders']

    @property
    def hide_read_marks(self) -> Optional[bool]:
        return self['hide_read_marks']

    @property
    def new_noncontact_peers_require_premium(self) -> Optional[bool]:
        return self['new_noncontact_peers_require_premium']

    @property
    def display_gifts_button(self) -> Optional[bool]:
        return self['display_gifts_button']

    @property
    def noncontact_peers_paid_stars(self) -> Optional[int]:
        return self['noncontact_peers_paid_stars']

    @property
    def disallowed_gifts(self) -> Optional[aliases.AnyDisallowedGiftsSettings]:
        return build_object(self['disallowed_gifts'])


class MessageViews(dict):
    __slots__ = ()

    @overload
    def __init__(self, views: Optional[int] = ..., forwards: Optional[int] = ..., replies: Optional[aliases.AnyMessageReplies] = ...): ...

    def __init__(self, _='messageViews', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def views(self) -> Optional[int]:
        return self['views']

    @property
    def forwards(self) -> Optional[int]:
        return self['forwards']

    @property
    def replies(self) -> Optional[aliases.AnyMessageReplies]:
        return build_object(self['replies'])


class MessageReplyHeader(dict):
    __slots__ = ()

    @overload
    def __init__(self, reply_to_scheduled: Optional[bool] = ..., forum_topic: Optional[bool] = ..., quote: Optional[bool] = ..., reply_to_msg_id: Optional[int] = ..., reply_to_peer_id: Optional[aliases.AnyPeer] = ..., reply_from: Optional[aliases.AnyMessageFwdHeader] = ..., reply_media: Optional[aliases.AnyMessageMedia] = ..., reply_to_top_id: Optional[int] = ..., quote_text: Optional[str] = ..., quote_entities: Optional[list[aliases.AnyMessageEntity]] = ..., quote_offset: Optional[int] = ..., todo_item_id: Optional[int] = ...): ...

    def __init__(self, _='messageReplyHeader', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reply_to_scheduled(self) -> Optional[bool]:
        return self['reply_to_scheduled']

    @property
    def forum_topic(self) -> Optional[bool]:
        return self['forum_topic']

    @property
    def quote(self) -> Optional[bool]:
        return self['quote']

    @property
    def reply_to_msg_id(self) -> Optional[int]:
        return self['reply_to_msg_id']

    @property
    def reply_to_peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['reply_to_peer_id'])

    @property
    def reply_from(self) -> Optional[aliases.AnyMessageFwdHeader]:
        return build_object(self['reply_from'])

    @property
    def reply_media(self) -> Optional[aliases.AnyMessageMedia]:
        return build_object(self['reply_media'])

    @property
    def reply_to_top_id(self) -> Optional[int]:
        return self['reply_to_top_id']

    @property
    def quote_text(self) -> Optional[str]:
        return self['quote_text']

    @property
    def quote_entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['quote_entities'])

    @property
    def quote_offset(self) -> Optional[int]:
        return self['quote_offset']

    @property
    def todo_item_id(self) -> Optional[int]:
        return self['todo_item_id']


class MessageReplyStoryHeader(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, story_id: int): ...

    def __init__(self, peer, story_id, _='messageReplyStoryHeader', **kwargs):
        kwargs['peer'] = peer
        kwargs['story_id'] = story_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def story_id(self) -> int:
        return self['story_id']


class MessageReplies(dict):
    __slots__ = ()

    @overload
    def __init__(self, replies: int, replies_pts: int, comments: Optional[bool] = ..., recent_repliers: Optional[list[aliases.AnyPeer]] = ..., channel_id: Optional[int] = ..., max_id: Optional[int] = ..., read_max_id: Optional[int] = ...): ...

    def __init__(self, replies, replies_pts, _='messageReplies', **kwargs):
        kwargs['replies'] = replies
        kwargs['replies_pts'] = replies_pts
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def comments(self) -> Optional[bool]:
        return self['comments']

    @property
    def replies(self) -> int:
        return self['replies']

    @property
    def replies_pts(self) -> int:
        return self['replies_pts']

    @property
    def recent_repliers(self) -> Optional[list[aliases.AnyPeer]]:
        return build_object(self['recent_repliers'])

    @property
    def channel_id(self) -> Optional[int]:
        return self['channel_id']

    @property
    def max_id(self) -> Optional[int]:
        return self['max_id']

    @property
    def read_max_id(self) -> Optional[int]:
        return self['read_max_id']


class PeerBlocked(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, date: int): ...

    def __init__(self, peer_id, date, _='peerBlocked', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def date(self) -> int:
        return self['date']


class GroupCallDiscarded(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, duration: int): ...

    def __init__(self, id, access_hash, duration, _='groupCallDiscarded', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['duration'] = duration
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def duration(self) -> int:
        return self['duration']


class GroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, participants_count: int, unmuted_video_limit: int, version: int, join_muted: Optional[bool] = ..., can_change_join_muted: Optional[bool] = ..., join_date_asc: Optional[bool] = ..., schedule_start_subscribed: Optional[bool] = ..., can_start_video: Optional[bool] = ..., record_video_active: Optional[bool] = ..., rtmp_stream: Optional[bool] = ..., listeners_hidden: Optional[bool] = ..., conference: Optional[bool] = ..., creator: Optional[bool] = ..., messages_enabled: Optional[bool] = ..., can_change_messages_enabled: Optional[bool] = ..., min: Optional[bool] = ..., title: Optional[str] = ..., stream_dc_id: Optional[int] = ..., record_start_date: Optional[int] = ..., schedule_date: Optional[int] = ..., unmuted_video_count: Optional[int] = ..., invite_link: Optional[str] = ..., send_paid_messages_stars: Optional[int] = ..., default_send_as: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, id, access_hash, participants_count, unmuted_video_limit, version, _='groupCall', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['participants_count'] = participants_count
        kwargs['unmuted_video_limit'] = unmuted_video_limit
        kwargs['version'] = version
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def join_muted(self) -> Optional[bool]:
        return self['join_muted']

    @property
    def can_change_join_muted(self) -> Optional[bool]:
        return self['can_change_join_muted']

    @property
    def join_date_asc(self) -> Optional[bool]:
        return self['join_date_asc']

    @property
    def schedule_start_subscribed(self) -> Optional[bool]:
        return self['schedule_start_subscribed']

    @property
    def can_start_video(self) -> Optional[bool]:
        return self['can_start_video']

    @property
    def record_video_active(self) -> Optional[bool]:
        return self['record_video_active']

    @property
    def rtmp_stream(self) -> Optional[bool]:
        return self['rtmp_stream']

    @property
    def listeners_hidden(self) -> Optional[bool]:
        return self['listeners_hidden']

    @property
    def conference(self) -> Optional[bool]:
        return self['conference']

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def messages_enabled(self) -> Optional[bool]:
        return self['messages_enabled']

    @property
    def can_change_messages_enabled(self) -> Optional[bool]:
        return self['can_change_messages_enabled']

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def participants_count(self) -> int:
        return self['participants_count']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def stream_dc_id(self) -> Optional[int]:
        return self['stream_dc_id']

    @property
    def record_start_date(self) -> Optional[int]:
        return self['record_start_date']

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']

    @property
    def unmuted_video_count(self) -> Optional[int]:
        return self['unmuted_video_count']

    @property
    def unmuted_video_limit(self) -> int:
        return self['unmuted_video_limit']

    @property
    def version(self) -> int:
        return self['version']

    @property
    def invite_link(self) -> Optional[str]:
        return self['invite_link']

    @property
    def send_paid_messages_stars(self) -> Optional[int]:
        return self['send_paid_messages_stars']

    @property
    def default_send_as(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['default_send_as'])


class InputGroupCall(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputGroupCall', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputGroupCallSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputGroupCallSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class InputGroupCallInviteMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int): ...

    def __init__(self, msg_id, _='inputGroupCallInviteMessage', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class GroupCallParticipant(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, date: int, source: int, muted: Optional[bool] = ..., left: Optional[bool] = ..., can_self_unmute: Optional[bool] = ..., just_joined: Optional[bool] = ..., versioned: Optional[bool] = ..., min: Optional[bool] = ..., muted_by_you: Optional[bool] = ..., volume_by_admin: Optional[bool] = ..., self_: Optional[bool] = ..., video_joined: Optional[bool] = ..., active_date: Optional[int] = ..., volume: Optional[int] = ..., about: Optional[str] = ..., raise_hand_rating: Optional[int] = ..., video: Optional[aliases.AnyGroupCallParticipantVideo] = ..., presentation: Optional[aliases.AnyGroupCallParticipantVideo] = ..., paid_stars_total: Optional[int] = ...): ...

    def __init__(self, peer, date, source, _='groupCallParticipant', **kwargs):
        kwargs['peer'] = peer
        kwargs['date'] = date
        kwargs['source'] = source
        if 'self_' in kwargs:
            kwargs['self'] = kwargs.pop('self_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def muted(self) -> Optional[bool]:
        return self['muted']

    @property
    def left(self) -> Optional[bool]:
        return self['left']

    @property
    def can_self_unmute(self) -> Optional[bool]:
        return self['can_self_unmute']

    @property
    def just_joined(self) -> Optional[bool]:
        return self['just_joined']

    @property
    def versioned(self) -> Optional[bool]:
        return self['versioned']

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def muted_by_you(self) -> Optional[bool]:
        return self['muted_by_you']

    @property
    def volume_by_admin(self) -> Optional[bool]:
        return self['volume_by_admin']

    @property
    def self_(self) -> Optional[bool]:
        return self['self']

    @property
    def video_joined(self) -> Optional[bool]:
        return self['video_joined']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def active_date(self) -> Optional[int]:
        return self['active_date']

    @property
    def source(self) -> int:
        return self['source']

    @property
    def volume(self) -> Optional[int]:
        return self['volume']

    @property
    def about(self) -> Optional[str]:
        return self['about']

    @property
    def raise_hand_rating(self) -> Optional[int]:
        return self['raise_hand_rating']

    @property
    def video(self) -> Optional[aliases.AnyGroupCallParticipantVideo]:
        return build_object(self['video'])

    @property
    def presentation(self) -> Optional[aliases.AnyGroupCallParticipantVideo]:
        return build_object(self['presentation'])

    @property
    def paid_stars_total(self) -> Optional[int]:
        return self['paid_stars_total']


class InlineQueryPeerTypeSameBotPM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypeSameBotPM'):
        dict.__init__(self, _=_)


class InlineQueryPeerTypePM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypePM'):
        dict.__init__(self, _=_)


class InlineQueryPeerTypeChat(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypeChat'):
        dict.__init__(self, _=_)


class InlineQueryPeerTypeMegagroup(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypeMegagroup'):
        dict.__init__(self, _=_)


class InlineQueryPeerTypeBroadcast(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypeBroadcast'):
        dict.__init__(self, _=_)


class InlineQueryPeerTypeBotPM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inlineQueryPeerTypeBotPM'):
        dict.__init__(self, _=_)


class ChatInviteImporter(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, date: int, requested: Optional[bool] = ..., via_chatlist: Optional[bool] = ..., about: Optional[str] = ..., approved_by: Optional[int] = ...): ...

    def __init__(self, user_id, date, _='chatInviteImporter', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def requested(self) -> Optional[bool]:
        return self['requested']

    @property
    def via_chatlist(self) -> Optional[bool]:
        return self['via_chatlist']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def about(self) -> Optional[str]:
        return self['about']

    @property
    def approved_by(self) -> Optional[int]:
        return self['approved_by']


class ChatAdminWithInvites(dict):
    __slots__ = ()

    @overload
    def __init__(self, admin_id: int, invites_count: int, revoked_invites_count: int): ...

    def __init__(self, admin_id, invites_count, revoked_invites_count, _='chatAdminWithInvites', **kwargs):
        kwargs['admin_id'] = admin_id
        kwargs['invites_count'] = invites_count
        kwargs['revoked_invites_count'] = revoked_invites_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def admin_id(self) -> int:
        return self['admin_id']

    @property
    def invites_count(self) -> int:
        return self['invites_count']

    @property
    def revoked_invites_count(self) -> int:
        return self['revoked_invites_count']


class GroupCallParticipantVideoSourceGroup(dict):
    __slots__ = ()

    @overload
    def __init__(self, semantics: str, sources: list[int]): ...

    def __init__(self, semantics, sources, _='groupCallParticipantVideoSourceGroup', **kwargs):
        kwargs['semantics'] = semantics
        kwargs['sources'] = sources
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def semantics(self) -> str:
        return self['semantics']

    @property
    def sources(self) -> list[int]:
        return self['sources']


class GroupCallParticipantVideo(dict):
    __slots__ = ()

    @overload
    def __init__(self, endpoint: str, source_groups: list[aliases.AnyGroupCallParticipantVideoSourceGroup], paused: Optional[bool] = ..., audio_source: Optional[int] = ...): ...

    def __init__(self, endpoint, source_groups, _='groupCallParticipantVideo', **kwargs):
        kwargs['endpoint'] = endpoint
        kwargs['source_groups'] = source_groups
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def paused(self) -> Optional[bool]:
        return self['paused']

    @property
    def endpoint(self) -> str:
        return self['endpoint']

    @property
    def source_groups(self) -> list[aliases.AnyGroupCallParticipantVideoSourceGroup]:
        return build_object(self['source_groups'])

    @property
    def audio_source(self) -> Optional[int]:
        return self['audio_source']


class BotCommandScopeDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botCommandScopeDefault'):
        dict.__init__(self, _=_)


class BotCommandScopeUsers(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botCommandScopeUsers'):
        dict.__init__(self, _=_)


class BotCommandScopeChats(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botCommandScopeChats'):
        dict.__init__(self, _=_)


class BotCommandScopeChatAdmins(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botCommandScopeChatAdmins'):
        dict.__init__(self, _=_)


class BotCommandScopePeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='botCommandScopePeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class BotCommandScopePeerAdmins(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='botCommandScopePeerAdmins', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class BotCommandScopePeerUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, user_id: aliases.AnyInputUser): ...

    def __init__(self, peer, user_id, _='botCommandScopePeerUser', **kwargs):
        kwargs['peer'] = peer
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])


class ChatTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='chatTheme', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class ChatThemeUniqueGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, theme_settings: list[aliases.AnyThemeSettings]): ...

    def __init__(self, gift, theme_settings, _='chatThemeUniqueGift', **kwargs):
        kwargs['gift'] = gift
        kwargs['theme_settings'] = theme_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def theme_settings(self) -> list[aliases.AnyThemeSettings]:
        return build_object(self['theme_settings'])


class SponsoredMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, random_id: bytes, url: str, title: str, message: str, button_text: str, recommended: Optional[bool] = ..., can_report: Optional[bool] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., photo: Optional[aliases.AnyPhoto] = ..., media: Optional[aliases.AnyMessageMedia] = ..., color: Optional[aliases.AnyPeerColor] = ..., sponsor_info: Optional[str] = ..., additional_info: Optional[str] = ..., min_display_duration: Optional[int] = ..., max_display_duration: Optional[int] = ...): ...

    def __init__(self, random_id, url, title, message, button_text, _='sponsoredMessage', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['url'] = url
        kwargs['title'] = title
        kwargs['message'] = message
        kwargs['button_text'] = button_text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def recommended(self) -> Optional[bool]:
        return self['recommended']

    @property
    def can_report(self) -> Optional[bool]:
        return self['can_report']

    @property
    def random_id(self) -> bytes:
        return self['random_id']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])

    @property
    def media(self) -> Optional[aliases.AnyMessageMedia]:
        return build_object(self['media'])

    @property
    def color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['color'])

    @property
    def button_text(self) -> str:
        return self['button_text']

    @property
    def sponsor_info(self) -> Optional[str]:
        return self['sponsor_info']

    @property
    def additional_info(self) -> Optional[str]:
        return self['additional_info']

    @property
    def min_display_duration(self) -> Optional[int]:
        return self['min_display_duration']

    @property
    def max_display_duration(self) -> Optional[int]:
        return self['max_display_duration']


class SearchResultsCalendarPeriod(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, min_msg_id: int, max_msg_id: int, count: int): ...

    def __init__(self, date, min_msg_id, max_msg_id, count, _='searchResultsCalendarPeriod', **kwargs):
        kwargs['date'] = date
        kwargs['min_msg_id'] = min_msg_id
        kwargs['max_msg_id'] = max_msg_id
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def min_msg_id(self) -> int:
        return self['min_msg_id']

    @property
    def max_msg_id(self) -> int:
        return self['max_msg_id']

    @property
    def count(self) -> int:
        return self['count']


class SearchResultPosition(dict):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int, date: int, offset: int): ...

    def __init__(self, msg_id, date, offset, _='searchResultPosition', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['date'] = date
        kwargs['offset'] = offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def offset(self) -> int:
        return self['offset']


class ReactionCount(dict):
    __slots__ = ()

    @overload
    def __init__(self, reaction: aliases.AnyReaction, count: int, chosen_order: Optional[int] = ...): ...

    def __init__(self, reaction, count, _='reactionCount', **kwargs):
        kwargs['reaction'] = reaction
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chosen_order(self) -> Optional[int]:
        return self['chosen_order']

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])

    @property
    def count(self) -> int:
        return self['count']


class MessageReactions(dict):
    __slots__ = ()

    @overload
    def __init__(self, results: list[aliases.AnyReactionCount], min: Optional[bool] = ..., can_see_list: Optional[bool] = ..., reactions_as_tags: Optional[bool] = ..., recent_reactions: Optional[list[aliases.AnyMessagePeerReaction]] = ..., top_reactors: Optional[list[aliases.AnyMessageReactor]] = ...): ...

    def __init__(self, results, _='messageReactions', **kwargs):
        kwargs['results'] = results
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def can_see_list(self) -> Optional[bool]:
        return self['can_see_list']

    @property
    def reactions_as_tags(self) -> Optional[bool]:
        return self['reactions_as_tags']

    @property
    def results(self) -> list[aliases.AnyReactionCount]:
        return build_object(self['results'])

    @property
    def recent_reactions(self) -> Optional[list[aliases.AnyMessagePeerReaction]]:
        return build_object(self['recent_reactions'])

    @property
    def top_reactors(self) -> Optional[list[aliases.AnyMessageReactor]]:
        return build_object(self['top_reactors'])


class AvailableReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, reaction: str, title: str, static_icon: aliases.AnyDocument, appear_animation: aliases.AnyDocument, select_animation: aliases.AnyDocument, activate_animation: aliases.AnyDocument, effect_animation: aliases.AnyDocument, inactive: Optional[bool] = ..., premium: Optional[bool] = ..., around_animation: Optional[aliases.AnyDocument] = ..., center_icon: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, reaction, title, static_icon, appear_animation, select_animation, activate_animation, effect_animation, _='availableReaction', **kwargs):
        kwargs['reaction'] = reaction
        kwargs['title'] = title
        kwargs['static_icon'] = static_icon
        kwargs['appear_animation'] = appear_animation
        kwargs['select_animation'] = select_animation
        kwargs['activate_animation'] = activate_animation
        kwargs['effect_animation'] = effect_animation
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inactive(self) -> Optional[bool]:
        return self['inactive']

    @property
    def premium(self) -> Optional[bool]:
        return self['premium']

    @property
    def reaction(self) -> str:
        return self['reaction']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def static_icon(self) -> aliases.AnyDocument:
        return build_object(self['static_icon'])

    @property
    def appear_animation(self) -> aliases.AnyDocument:
        return build_object(self['appear_animation'])

    @property
    def select_animation(self) -> aliases.AnyDocument:
        return build_object(self['select_animation'])

    @property
    def activate_animation(self) -> aliases.AnyDocument:
        return build_object(self['activate_animation'])

    @property
    def effect_animation(self) -> aliases.AnyDocument:
        return build_object(self['effect_animation'])

    @property
    def around_animation(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['around_animation'])

    @property
    def center_icon(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['center_icon'])


class MessagePeerReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, date: int, reaction: aliases.AnyReaction, big: Optional[bool] = ..., unread: Optional[bool] = ..., my: Optional[bool] = ...): ...

    def __init__(self, peer_id, date, reaction, _='messagePeerReaction', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['date'] = date
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def big(self) -> Optional[bool]:
        return self['big']

    @property
    def unread(self) -> Optional[bool]:
        return self['unread']

    @property
    def my(self) -> Optional[bool]:
        return self['my']

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class GroupCallStreamChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel: int, scale: int, last_timestamp_ms: int): ...

    def __init__(self, channel, scale, last_timestamp_ms, _='groupCallStreamChannel', **kwargs):
        kwargs['channel'] = channel
        kwargs['scale'] = scale
        kwargs['last_timestamp_ms'] = last_timestamp_ms
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel(self) -> int:
        return self['channel']

    @property
    def scale(self) -> int:
        return self['scale']

    @property
    def last_timestamp_ms(self) -> int:
        return self['last_timestamp_ms']


class AttachMenuBotIconColor(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, color: int): ...

    def __init__(self, name, color, _='attachMenuBotIconColor', **kwargs):
        kwargs['name'] = name
        kwargs['color'] = color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']

    @property
    def color(self) -> int:
        return self['color']


class AttachMenuBotIcon(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, icon: aliases.AnyDocument, colors: Optional[list[aliases.AnyAttachMenuBotIconColor]] = ...): ...

    def __init__(self, name, icon, _='attachMenuBotIcon', **kwargs):
        kwargs['name'] = name
        kwargs['icon'] = icon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']

    @property
    def icon(self) -> aliases.AnyDocument:
        return build_object(self['icon'])

    @property
    def colors(self) -> Optional[list[aliases.AnyAttachMenuBotIconColor]]:
        return build_object(self['colors'])


class AttachMenuBot(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, short_name: str, icons: list[aliases.AnyAttachMenuBotIcon], inactive: Optional[bool] = ..., has_settings: Optional[bool] = ..., request_write_access: Optional[bool] = ..., show_in_attach_menu: Optional[bool] = ..., show_in_side_menu: Optional[bool] = ..., side_menu_disclaimer_needed: Optional[bool] = ..., peer_types: Optional[list[aliases.AnyAttachMenuPeerType]] = ...): ...

    def __init__(self, bot_id, short_name, icons, _='attachMenuBot', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['short_name'] = short_name
        kwargs['icons'] = icons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def inactive(self) -> Optional[bool]:
        return self['inactive']

    @property
    def has_settings(self) -> Optional[bool]:
        return self['has_settings']

    @property
    def request_write_access(self) -> Optional[bool]:
        return self['request_write_access']

    @property
    def show_in_attach_menu(self) -> Optional[bool]:
        return self['show_in_attach_menu']

    @property
    def show_in_side_menu(self) -> Optional[bool]:
        return self['show_in_side_menu']

    @property
    def side_menu_disclaimer_needed(self) -> Optional[bool]:
        return self['side_menu_disclaimer_needed']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def peer_types(self) -> Optional[list[aliases.AnyAttachMenuPeerType]]:
        return build_object(self['peer_types'])

    @property
    def icons(self) -> list[aliases.AnyAttachMenuBotIcon]:
        return build_object(self['icons'])


class AttachMenuBotsNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuBotsNotModified'):
        dict.__init__(self, _=_)


class AttachMenuBots(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, bots: list[aliases.AnyAttachMenuBot], users: list[aliases.AnyUser]): ...

    def __init__(self, hash, bots, users, _='attachMenuBots', **kwargs):
        kwargs['hash'] = hash
        kwargs['bots'] = bots
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def bots(self) -> list[aliases.AnyAttachMenuBot]:
        return build_object(self['bots'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class AttachMenuBotsBot(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyAttachMenuBot, users: list[aliases.AnyUser]): ...

    def __init__(self, bot, users, _='attachMenuBotsBot', **kwargs):
        kwargs['bot'] = bot
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyAttachMenuBot:
        return build_object(self['bot'])

    @property
    def users(self) -> list[aliases.AnyUser]:
        return build_object(self['users'])


class WebViewResultUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, fullsize: Optional[bool] = ..., fullscreen: Optional[bool] = ..., query_id: Optional[int] = ...): ...

    def __init__(self, url, _='webViewResultUrl', **kwargs):
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def fullsize(self) -> Optional[bool]:
        return self['fullsize']

    @property
    def fullscreen(self) -> Optional[bool]:
        return self['fullscreen']

    @property
    def query_id(self) -> Optional[int]:
        return self['query_id']

    @property
    def url(self) -> str:
        return self['url']


class WebViewMessageSent(dict):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: Optional[aliases.AnyInputBotInlineMessageID] = ...): ...

    def __init__(self, _='webViewMessageSent', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> Optional[aliases.AnyInputBotInlineMessageID]:
        return build_object(self['msg_id'])


class BotMenuButtonDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botMenuButtonDefault'):
        dict.__init__(self, _=_)


class BotMenuButtonCommands(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botMenuButtonCommands'):
        dict.__init__(self, _=_)


class BotMenuButton(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str): ...

    def __init__(self, text, url, _='botMenuButton', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def url(self) -> str:
        return self['url']


class NotificationSoundDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='notificationSoundDefault'):
        dict.__init__(self, _=_)


class NotificationSoundNone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='notificationSoundNone'):
        dict.__init__(self, _=_)


class NotificationSoundLocal(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, data: str): ...

    def __init__(self, title, data, _='notificationSoundLocal', **kwargs):
        kwargs['title'] = title
        kwargs['data'] = data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def data(self) -> str:
        return self['data']


class NotificationSoundRingtone(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='notificationSoundRingtone', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class AttachMenuPeerTypeSameBotPM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuPeerTypeSameBotPM'):
        dict.__init__(self, _=_)


class AttachMenuPeerTypeBotPM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuPeerTypeBotPM'):
        dict.__init__(self, _=_)


class AttachMenuPeerTypePM(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuPeerTypePM'):
        dict.__init__(self, _=_)


class AttachMenuPeerTypeChat(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuPeerTypeChat'):
        dict.__init__(self, _=_)


class AttachMenuPeerTypeBroadcast(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='attachMenuPeerTypeBroadcast'):
        dict.__init__(self, _=_)


class InputInvoiceMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, msg_id: int): ...

    def __init__(self, peer, msg_id, _='inputInvoiceMessage', **kwargs):
        kwargs['peer'] = peer
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class InputInvoiceSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputInvoiceSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class InputInvoicePremiumGiftCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyInputStorePaymentPurpose, option: aliases.AnyPremiumGiftCodeOption): ...

    def __init__(self, purpose, option, _='inputInvoicePremiumGiftCode', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])

    @property
    def option(self) -> aliases.AnyPremiumGiftCodeOption:
        return build_object(self['option'])


class InputInvoiceStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, purpose, _='inputInvoiceStars', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class InputInvoiceChatInviteSubscription(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: str): ...

    def __init__(self, hash, _='inputInvoiceChatInviteSubscription', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> str:
        return self['hash']


class InputInvoiceStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, gift_id: int, hide_name: Optional[bool] = ..., include_upgrade: Optional[bool] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, peer, gift_id, _='inputInvoiceStarGift', **kwargs):
        kwargs['peer'] = peer
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hide_name(self) -> Optional[bool]:
        return self['hide_name']

    @property
    def include_upgrade(self) -> Optional[bool]:
        return self['include_upgrade']

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class InputInvoiceStarGiftUpgrade(dict):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, keep_original_details: Optional[bool] = ...): ...

    def __init__(self, stargift, _='inputInvoiceStarGiftUpgrade', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def keep_original_details(self) -> Optional[bool]:
        return self['keep_original_details']

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])


class InputInvoiceStarGiftTransfer(dict):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift, to_id: aliases.AnyInputPeer): ...

    def __init__(self, stargift, to_id, _='inputInvoiceStarGiftTransfer', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['to_id'] = to_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])

    @property
    def to_id(self) -> aliases.AnyInputPeer:
        return build_object(self['to_id'])


class InputInvoicePremiumGiftStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, months: int, message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, user_id, months, _='inputInvoicePremiumGiftStars', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['months'] = months
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def months(self) -> int:
        return self['months']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class InputInvoiceBusinessBotTransferStars(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot: aliases.AnyInputUser, stars: int): ...

    def __init__(self, bot, stars, _='inputInvoiceBusinessBotTransferStars', **kwargs):
        kwargs['bot'] = bot
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> aliases.AnyInputUser:
        return build_object(self['bot'])

    @property
    def stars(self) -> int:
        return self['stars']


class InputInvoiceStarGiftResale(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str, to_id: aliases.AnyInputPeer, ton: Optional[bool] = ...): ...

    def __init__(self, slug, to_id, _='inputInvoiceStarGiftResale', **kwargs):
        kwargs['slug'] = slug
        kwargs['to_id'] = to_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def ton(self) -> Optional[bool]:
        return self['ton']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def to_id(self) -> aliases.AnyInputPeer:
        return build_object(self['to_id'])


class InputInvoiceStarGiftPrepaidUpgrade(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, hash: str): ...

    def __init__(self, peer, hash, _='inputInvoiceStarGiftPrepaidUpgrade', **kwargs):
        kwargs['peer'] = peer
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def hash(self) -> str:
        return self['hash']


class InputInvoicePremiumAuthCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, purpose: aliases.AnyInputStorePaymentPurpose): ...

    def __init__(self, purpose, _='inputInvoicePremiumAuthCode', **kwargs):
        kwargs['purpose'] = purpose
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def purpose(self) -> aliases.AnyInputStorePaymentPurpose:
        return build_object(self['purpose'])


class InputInvoiceStarGiftDropOriginalDetails(dict):
    __slots__ = ()

    @overload
    def __init__(self, stargift: aliases.AnyInputSavedStarGift): ...

    def __init__(self, stargift, _='inputInvoiceStarGiftDropOriginalDetails', **kwargs):
        kwargs['stargift'] = stargift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stargift(self) -> aliases.AnyInputSavedStarGift:
        return build_object(self['stargift'])


class InputInvoiceStarGiftAuctionBid(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int, bid_amount: int, hide_name: Optional[bool] = ..., update_bid: Optional[bool] = ..., peer: Optional[aliases.AnyInputPeer] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, gift_id, bid_amount, _='inputInvoiceStarGiftAuctionBid', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['bid_amount'] = bid_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hide_name(self) -> Optional[bool]:
        return self['hide_name']

    @property
    def update_bid(self) -> Optional[bool]:
        return self['update_bid']

    @property
    def peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['peer'])

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def bid_amount(self) -> int:
        return self['bid_amount']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class InputStorePaymentPremiumSubscription(dict):
    __slots__ = ()

    @overload
    def __init__(self, restore: Optional[bool] = ..., upgrade: Optional[bool] = ...): ...

    def __init__(self, _='inputStorePaymentPremiumSubscription', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def restore(self) -> Optional[bool]:
        return self['restore']

    @property
    def upgrade(self) -> Optional[bool]:
        return self['upgrade']


class InputStorePaymentGiftPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, currency: str, amount: int): ...

    def __init__(self, user_id, currency, amount, _='inputStorePaymentGiftPremium', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class InputStorePaymentPremiumGiftCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: list[aliases.AnyInputUser], currency: str, amount: int, boost_peer: Optional[aliases.AnyInputPeer] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, users, currency, amount, _='inputStorePaymentPremiumGiftCode', **kwargs):
        kwargs['users'] = users
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> list[aliases.AnyInputUser]:
        return build_object(self['users'])

    @property
    def boost_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['boost_peer'])

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class InputStorePaymentPremiumGiveaway(dict):
    __slots__ = ()

    @overload
    def __init__(self, boost_peer: aliases.AnyInputPeer, random_id: int, until_date: int, currency: str, amount: int, only_new_subscribers: Optional[bool] = ..., winners_are_visible: Optional[bool] = ..., additional_peers: Optional[list[aliases.AnyInputPeer]] = ..., countries_iso2: Optional[list[str]] = ..., prize_description: Optional[str] = ...): ...

    def __init__(self, boost_peer, random_id, until_date, currency, amount, _='inputStorePaymentPremiumGiveaway', **kwargs):
        kwargs['boost_peer'] = boost_peer
        kwargs['random_id'] = random_id
        kwargs['until_date'] = until_date
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def only_new_subscribers(self) -> Optional[bool]:
        return self['only_new_subscribers']

    @property
    def winners_are_visible(self) -> Optional[bool]:
        return self['winners_are_visible']

    @property
    def boost_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['boost_peer'])

    @property
    def additional_peers(self) -> Optional[list[aliases.AnyInputPeer]]:
        return build_object(self['additional_peers'])

    @property
    def countries_iso2(self) -> Optional[list[str]]:
        return self['countries_iso2']

    @property
    def prize_description(self) -> Optional[str]:
        return self['prize_description']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def until_date(self) -> int:
        return self['until_date']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class InputStorePaymentStarsTopup(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, currency: str, amount: int, spend_purpose_peer: Optional[aliases.AnyInputPeer] = ...): ...

    def __init__(self, stars, currency, amount, _='inputStorePaymentStarsTopup', **kwargs):
        kwargs['stars'] = stars
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def spend_purpose_peer(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['spend_purpose_peer'])


class InputStorePaymentStarsGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: aliases.AnyInputUser, stars: int, currency: str, amount: int): ...

    def __init__(self, user_id, stars, currency, amount, _='inputStorePaymentStarsGift', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['stars'] = stars
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> aliases.AnyInputUser:
        return build_object(self['user_id'])

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class InputStorePaymentStarsGiveaway(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, boost_peer: aliases.AnyInputPeer, random_id: int, until_date: int, currency: str, amount: int, users: int, only_new_subscribers: Optional[bool] = ..., winners_are_visible: Optional[bool] = ..., additional_peers: Optional[list[aliases.AnyInputPeer]] = ..., countries_iso2: Optional[list[str]] = ..., prize_description: Optional[str] = ...): ...

    def __init__(self, stars, boost_peer, random_id, until_date, currency, amount, users, _='inputStorePaymentStarsGiveaway', **kwargs):
        kwargs['stars'] = stars
        kwargs['boost_peer'] = boost_peer
        kwargs['random_id'] = random_id
        kwargs['until_date'] = until_date
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['users'] = users
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def only_new_subscribers(self) -> Optional[bool]:
        return self['only_new_subscribers']

    @property
    def winners_are_visible(self) -> Optional[bool]:
        return self['winners_are_visible']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def boost_peer(self) -> aliases.AnyInputPeer:
        return build_object(self['boost_peer'])

    @property
    def additional_peers(self) -> Optional[list[aliases.AnyInputPeer]]:
        return build_object(self['additional_peers'])

    @property
    def countries_iso2(self) -> Optional[list[str]]:
        return self['countries_iso2']

    @property
    def prize_description(self) -> Optional[str]:
        return self['prize_description']

    @property
    def random_id(self) -> int:
        return self['random_id']

    @property
    def until_date(self) -> int:
        return self['until_date']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def users(self) -> int:
        return self['users']


class InputStorePaymentAuthCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str, currency: str, amount: int, restore: Optional[bool] = ...): ...

    def __init__(self, phone_number, phone_code_hash, currency, amount, _='inputStorePaymentAuthCode', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def restore(self) -> Optional[bool]:
        return self['restore']

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class PaymentFormMethod(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, title: str): ...

    def __init__(self, url, title, _='paymentFormMethod', **kwargs):
        kwargs['url'] = url
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def title(self) -> str:
        return self['title']


class EmojiStatusEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='emojiStatusEmpty'):
        dict.__init__(self, _=_)


class EmojiStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int, until: Optional[int] = ...): ...

    def __init__(self, document_id, _='emojiStatus', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']

    @property
    def until(self) -> Optional[int]:
        return self['until']


class EmojiStatusCollectible(dict):
    __slots__ = ()

    @overload
    def __init__(self, collectible_id: int, document_id: int, title: str, slug: str, pattern_document_id: int, center_color: int, edge_color: int, pattern_color: int, text_color: int, until: Optional[int] = ...): ...

    def __init__(self, collectible_id, document_id, title, slug, pattern_document_id, center_color, edge_color, pattern_color, text_color, _='emojiStatusCollectible', **kwargs):
        kwargs['collectible_id'] = collectible_id
        kwargs['document_id'] = document_id
        kwargs['title'] = title
        kwargs['slug'] = slug
        kwargs['pattern_document_id'] = pattern_document_id
        kwargs['center_color'] = center_color
        kwargs['edge_color'] = edge_color
        kwargs['pattern_color'] = pattern_color
        kwargs['text_color'] = text_color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collectible_id(self) -> int:
        return self['collectible_id']

    @property
    def document_id(self) -> int:
        return self['document_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def pattern_document_id(self) -> int:
        return self['pattern_document_id']

    @property
    def center_color(self) -> int:
        return self['center_color']

    @property
    def edge_color(self) -> int:
        return self['edge_color']

    @property
    def pattern_color(self) -> int:
        return self['pattern_color']

    @property
    def text_color(self) -> int:
        return self['text_color']

    @property
    def until(self) -> Optional[int]:
        return self['until']


class InputEmojiStatusCollectible(dict):
    __slots__ = ()

    @overload
    def __init__(self, collectible_id: int, until: Optional[int] = ...): ...

    def __init__(self, collectible_id, _='inputEmojiStatusCollectible', **kwargs):
        kwargs['collectible_id'] = collectible_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collectible_id(self) -> int:
        return self['collectible_id']

    @property
    def until(self) -> Optional[int]:
        return self['until']


class ReactionEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='reactionEmpty'):
        dict.__init__(self, _=_)


class ReactionEmoji(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='reactionEmoji', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class ReactionCustomEmoji(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int): ...

    def __init__(self, document_id, _='reactionCustomEmoji', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']


class ReactionPaid(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='reactionPaid'):
        dict.__init__(self, _=_)


class ChatReactionsNone(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='chatReactionsNone'):
        dict.__init__(self, _=_)


class ChatReactionsAll(dict):
    __slots__ = ()

    @overload
    def __init__(self, allow_custom: Optional[bool] = ...): ...

    def __init__(self, _='chatReactionsAll', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def allow_custom(self) -> Optional[bool]:
        return self['allow_custom']


class ChatReactionsSome(dict):
    __slots__ = ()

    @overload
    def __init__(self, reactions: list[aliases.AnyReaction]): ...

    def __init__(self, reactions, _='chatReactionsSome', **kwargs):
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reactions(self) -> list[aliases.AnyReaction]:
        return build_object(self['reactions'])


class EmailVerifyPurposeLoginSetup(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone_number: str, phone_code_hash: str): ...

    def __init__(self, phone_number, phone_code_hash, _='emailVerifyPurposeLoginSetup', **kwargs):
        kwargs['phone_number'] = phone_number
        kwargs['phone_code_hash'] = phone_code_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def phone_code_hash(self) -> str:
        return self['phone_code_hash']


class EmailVerifyPurposeLoginChange(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='emailVerifyPurposeLoginChange'):
        dict.__init__(self, _=_)


class EmailVerifyPurposePassport(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='emailVerifyPurposePassport'):
        dict.__init__(self, _=_)


class EmailVerificationCode(dict):
    __slots__ = ()

    @overload
    def __init__(self, code: str): ...

    def __init__(self, code, _='emailVerificationCode', **kwargs):
        kwargs['code'] = code
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def code(self) -> str:
        return self['code']


class EmailVerificationGoogle(dict):
    __slots__ = ()

    @overload
    def __init__(self, token: str): ...

    def __init__(self, token, _='emailVerificationGoogle', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']


class EmailVerificationApple(dict):
    __slots__ = ()

    @overload
    def __init__(self, token: str): ...

    def __init__(self, token, _='emailVerificationApple', **kwargs):
        kwargs['token'] = token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def token(self) -> str:
        return self['token']


class PremiumSubscriptionOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, months: int, currency: str, amount: int, bot_url: str, current: Optional[bool] = ..., can_purchase_upgrade: Optional[bool] = ..., transaction: Optional[str] = ..., store_product: Optional[str] = ...): ...

    def __init__(self, months, currency, amount, bot_url, _='premiumSubscriptionOption', **kwargs):
        kwargs['months'] = months
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['bot_url'] = bot_url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def current(self) -> Optional[bool]:
        return self['current']

    @property
    def can_purchase_upgrade(self) -> Optional[bool]:
        return self['can_purchase_upgrade']

    @property
    def transaction(self) -> Optional[str]:
        return self['transaction']

    @property
    def months(self) -> int:
        return self['months']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def bot_url(self) -> str:
        return self['bot_url']

    @property
    def store_product(self) -> Optional[str]:
        return self['store_product']


class SendAsPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, premium_required: Optional[bool] = ...): ...

    def __init__(self, peer, _='sendAsPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def premium_required(self) -> Optional[bool]:
        return self['premium_required']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])


class MessageExtendedMediaPreview(dict):
    __slots__ = ()

    @overload
    def __init__(self, w: Optional[int] = ..., h: Optional[int] = ..., thumb: Optional[aliases.AnyPhotoSize] = ..., video_duration: Optional[int] = ...): ...

    def __init__(self, _='messageExtendedMediaPreview', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def w(self) -> Optional[int]:
        return self['w']

    @property
    def h(self) -> Optional[int]:
        return self['h']

    @property
    def thumb(self) -> Optional[aliases.AnyPhotoSize]:
        return build_object(self['thumb'])

    @property
    def video_duration(self) -> Optional[int]:
        return self['video_duration']


class MessageExtendedMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, media: aliases.AnyMessageMedia): ...

    def __init__(self, media, _='messageExtendedMedia', **kwargs):
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def media(self) -> aliases.AnyMessageMedia:
        return build_object(self['media'])


class StickerKeyword(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int, keyword: list[str]): ...

    def __init__(self, document_id, keyword, _='stickerKeyword', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['keyword'] = keyword
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']

    @property
    def keyword(self) -> list[str]:
        return self['keyword']


class Username(dict):
    __slots__ = ()

    @overload
    def __init__(self, username: str, editable: Optional[bool] = ..., active: Optional[bool] = ...): ...

    def __init__(self, username, _='username', **kwargs):
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def editable(self) -> Optional[bool]:
        return self['editable']

    @property
    def active(self) -> Optional[bool]:
        return self['active']

    @property
    def username(self) -> str:
        return self['username']


class ForumTopicDeleted(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='forumTopicDeleted', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class ForumTopic(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, date: int, peer: aliases.AnyPeer, title: str, icon_color: int, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, unread_reactions_count: int, from_id: aliases.AnyPeer, notify_settings: aliases.AnyPeerNotifySettings, my: Optional[bool] = ..., closed: Optional[bool] = ..., pinned: Optional[bool] = ..., short: Optional[bool] = ..., hidden: Optional[bool] = ..., title_missing: Optional[bool] = ..., icon_emoji_id: Optional[int] = ..., draft: Optional[aliases.AnyDraftMessage] = ...): ...

    def __init__(self, id, date, peer, title, icon_color, top_message, read_inbox_max_id, read_outbox_max_id, unread_count, unread_mentions_count, unread_reactions_count, from_id, notify_settings, _='forumTopic', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['peer'] = peer
        kwargs['title'] = title
        kwargs['icon_color'] = icon_color
        kwargs['top_message'] = top_message
        kwargs['read_inbox_max_id'] = read_inbox_max_id
        kwargs['read_outbox_max_id'] = read_outbox_max_id
        kwargs['unread_count'] = unread_count
        kwargs['unread_mentions_count'] = unread_mentions_count
        kwargs['unread_reactions_count'] = unread_reactions_count
        kwargs['from_id'] = from_id
        kwargs['notify_settings'] = notify_settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def my(self) -> Optional[bool]:
        return self['my']

    @property
    def closed(self) -> Optional[bool]:
        return self['closed']

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def short(self) -> Optional[bool]:
        return self['short']

    @property
    def hidden(self) -> Optional[bool]:
        return self['hidden']

    @property
    def title_missing(self) -> Optional[bool]:
        return self['title_missing']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_color(self) -> int:
        return self['icon_color']

    @property
    def icon_emoji_id(self) -> Optional[int]:
        return self['icon_emoji_id']

    @property
    def top_message(self) -> int:
        return self['top_message']

    @property
    def read_inbox_max_id(self) -> int:
        return self['read_inbox_max_id']

    @property
    def read_outbox_max_id(self) -> int:
        return self['read_outbox_max_id']

    @property
    def unread_count(self) -> int:
        return self['unread_count']

    @property
    def unread_mentions_count(self) -> int:
        return self['unread_mentions_count']

    @property
    def unread_reactions_count(self) -> int:
        return self['unread_reactions_count']

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def notify_settings(self) -> aliases.AnyPeerNotifySettings:
        return build_object(self['notify_settings'])

    @property
    def draft(self) -> Optional[aliases.AnyDraftMessage]:
        return build_object(self['draft'])


class DefaultHistoryTTL(dict):
    __slots__ = ()

    @overload
    def __init__(self, period: int): ...

    def __init__(self, period, _='defaultHistoryTTL', **kwargs):
        kwargs['period'] = period
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> int:
        return self['period']


class ExportedContactToken(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, expires: int): ...

    def __init__(self, url, expires, _='exportedContactToken', **kwargs):
        kwargs['url'] = url
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def url(self) -> str:
        return self['url']

    @property
    def expires(self) -> int:
        return self['expires']


class RequestPeerTypeUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot: Optional[bool] = ..., premium: Optional[bool] = ...): ...

    def __init__(self, _='requestPeerTypeUser', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot(self) -> Optional[bool]:
        return self['bot']

    @property
    def premium(self) -> Optional[bool]:
        return self['premium']


class RequestPeerTypeChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, creator: Optional[bool] = ..., bot_participant: Optional[bool] = ..., has_username: Optional[bool] = ..., forum: Optional[bool] = ..., user_admin_rights: Optional[aliases.AnyChatAdminRights] = ..., bot_admin_rights: Optional[aliases.AnyChatAdminRights] = ...): ...

    def __init__(self, _='requestPeerTypeChat', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def bot_participant(self) -> Optional[bool]:
        return self['bot_participant']

    @property
    def has_username(self) -> Optional[bool]:
        return self['has_username']

    @property
    def forum(self) -> Optional[bool]:
        return self['forum']

    @property
    def user_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['user_admin_rights'])

    @property
    def bot_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['bot_admin_rights'])


class RequestPeerTypeBroadcast(dict):
    __slots__ = ()

    @overload
    def __init__(self, creator: Optional[bool] = ..., has_username: Optional[bool] = ..., user_admin_rights: Optional[aliases.AnyChatAdminRights] = ..., bot_admin_rights: Optional[aliases.AnyChatAdminRights] = ...): ...

    def __init__(self, _='requestPeerTypeBroadcast', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def creator(self) -> Optional[bool]:
        return self['creator']

    @property
    def has_username(self) -> Optional[bool]:
        return self['has_username']

    @property
    def user_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['user_admin_rights'])

    @property
    def bot_admin_rights(self) -> Optional[aliases.AnyChatAdminRights]:
        return build_object(self['bot_admin_rights'])


class EmojiListNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='emojiListNotModified'):
        dict.__init__(self, _=_)


class EmojiList(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, document_id: list[int]): ...

    def __init__(self, hash, document_id, _='emojiList', **kwargs):
        kwargs['hash'] = hash
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def hash(self) -> int:
        return self['hash']

    @property
    def document_id(self) -> list[int]:
        return self['document_id']


class EmojiGroup(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, icon_emoji_id: int, emoticons: list[str]): ...

    def __init__(self, title, icon_emoji_id, emoticons, _='emojiGroup', **kwargs):
        kwargs['title'] = title
        kwargs['icon_emoji_id'] = icon_emoji_id
        kwargs['emoticons'] = emoticons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_emoji_id(self) -> int:
        return self['icon_emoji_id']

    @property
    def emoticons(self) -> list[str]:
        return self['emoticons']


class EmojiGroupGreeting(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, icon_emoji_id: int, emoticons: list[str]): ...

    def __init__(self, title, icon_emoji_id, emoticons, _='emojiGroupGreeting', **kwargs):
        kwargs['title'] = title
        kwargs['icon_emoji_id'] = icon_emoji_id
        kwargs['emoticons'] = emoticons
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_emoji_id(self) -> int:
        return self['icon_emoji_id']

    @property
    def emoticons(self) -> list[str]:
        return self['emoticons']


class EmojiGroupPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, icon_emoji_id: int): ...

    def __init__(self, title, icon_emoji_id, _='emojiGroupPremium', **kwargs):
        kwargs['title'] = title
        kwargs['icon_emoji_id'] = icon_emoji_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_emoji_id(self) -> int:
        return self['icon_emoji_id']


class TextWithEntities(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, entities: list[aliases.AnyMessageEntity]): ...

    def __init__(self, text, entities, _='textWithEntities', **kwargs):
        kwargs['text'] = text
        kwargs['entities'] = entities
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def entities(self) -> list[aliases.AnyMessageEntity]:
        return build_object(self['entities'])


class AutoSaveSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, photos: Optional[bool] = ..., videos: Optional[bool] = ..., video_max_size: Optional[int] = ...): ...

    def __init__(self, _='autoSaveSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def photos(self) -> Optional[bool]:
        return self['photos']

    @property
    def videos(self) -> Optional[bool]:
        return self['videos']

    @property
    def video_max_size(self) -> Optional[int]:
        return self['video_max_size']


class AutoSaveException(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, settings: aliases.AnyAutoSaveSettings): ...

    def __init__(self, peer, settings, _='autoSaveException', **kwargs):
        kwargs['peer'] = peer
        kwargs['settings'] = settings
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def settings(self) -> aliases.AnyAutoSaveSettings:
        return build_object(self['settings'])


class InputBotAppID(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int): ...

    def __init__(self, id, access_hash, _='inputBotAppID', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']


class InputBotAppShortName(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: aliases.AnyInputUser, short_name: str): ...

    def __init__(self, bot_id, short_name, _='inputBotAppShortName', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['short_name'] = short_name
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> aliases.AnyInputUser:
        return build_object(self['bot_id'])

    @property
    def short_name(self) -> str:
        return self['short_name']


class BotAppNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='botAppNotModified'):
        dict.__init__(self, _=_)


class BotApp(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, access_hash: int, short_name: str, title: str, description: str, photo: aliases.AnyPhoto, hash: int, document: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, id, access_hash, short_name, title, description, photo, hash, _='botApp', **kwargs):
        kwargs['id'] = id
        kwargs['access_hash'] = access_hash
        kwargs['short_name'] = short_name
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['photo'] = photo
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def access_hash(self) -> int:
        return self['access_hash']

    @property
    def short_name(self) -> str:
        return self['short_name']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def photo(self) -> aliases.AnyPhoto:
        return build_object(self['photo'])

    @property
    def document(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['document'])

    @property
    def hash(self) -> int:
        return self['hash']


class InlineBotWebView(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, url: str): ...

    def __init__(self, text, url, _='inlineBotWebView', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def url(self) -> str:
        return self['url']


class ReadParticipantDate(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, date: int): ...

    def __init__(self, user_id, date, _='readParticipantDate', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def date(self) -> int:
        return self['date']


class InputChatlistDialogFilter(dict):
    __slots__ = ()

    @overload
    def __init__(self, filter_id: int): ...

    def __init__(self, filter_id, _='inputChatlistDialogFilter', **kwargs):
        kwargs['filter_id'] = filter_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def filter_id(self) -> int:
        return self['filter_id']


class ExportedChatlistInvite(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, url: str, peers: list[aliases.AnyPeer]): ...

    def __init__(self, title, url, peers, _='exportedChatlistInvite', **kwargs):
        kwargs['title'] = title
        kwargs['url'] = url
        kwargs['peers'] = peers
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def peers(self) -> list[aliases.AnyPeer]:
        return build_object(self['peers'])


class MessagePeerVote(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, option: bytes, date: int): ...

    def __init__(self, peer, option, date, _='messagePeerVote', **kwargs):
        kwargs['peer'] = peer
        kwargs['option'] = option
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def option(self) -> bytes:
        return self['option']

    @property
    def date(self) -> int:
        return self['date']


class MessagePeerVoteInputOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, date: int): ...

    def __init__(self, peer, date, _='messagePeerVoteInputOption', **kwargs):
        kwargs['peer'] = peer
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def date(self) -> int:
        return self['date']


class MessagePeerVoteMultiple(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, options: list[bytes], date: int): ...

    def __init__(self, peer, options, date, _='messagePeerVoteMultiple', **kwargs):
        kwargs['peer'] = peer
        kwargs['options'] = options
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def options(self) -> list[bytes]:
        return self['options']

    @property
    def date(self) -> int:
        return self['date']


class StoryViews(dict):
    __slots__ = ()

    @overload
    def __init__(self, views_count: int, has_viewers: Optional[bool] = ..., forwards_count: Optional[int] = ..., reactions: Optional[list[aliases.AnyReactionCount]] = ..., reactions_count: Optional[int] = ..., recent_viewers: Optional[list[int]] = ...): ...

    def __init__(self, views_count, _='storyViews', **kwargs):
        kwargs['views_count'] = views_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def has_viewers(self) -> Optional[bool]:
        return self['has_viewers']

    @property
    def views_count(self) -> int:
        return self['views_count']

    @property
    def forwards_count(self) -> Optional[int]:
        return self['forwards_count']

    @property
    def reactions(self) -> Optional[list[aliases.AnyReactionCount]]:
        return build_object(self['reactions'])

    @property
    def reactions_count(self) -> Optional[int]:
        return self['reactions_count']

    @property
    def recent_viewers(self) -> Optional[list[int]]:
        return self['recent_viewers']


class StoryItemDeleted(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int): ...

    def __init__(self, id, _='storyItemDeleted', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']


class StoryItemSkipped(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, date: int, expire_date: int, close_friends: Optional[bool] = ..., live: Optional[bool] = ...): ...

    def __init__(self, id, date, expire_date, _='storyItemSkipped', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['expire_date'] = expire_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def close_friends(self) -> Optional[bool]:
        return self['close_friends']

    @property
    def live(self) -> Optional[bool]:
        return self['live']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def expire_date(self) -> int:
        return self['expire_date']


class StoryItem(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, date: int, expire_date: int, media: aliases.AnyMessageMedia, pinned: Optional[bool] = ..., public: Optional[bool] = ..., close_friends: Optional[bool] = ..., min: Optional[bool] = ..., noforwards: Optional[bool] = ..., edited: Optional[bool] = ..., contacts: Optional[bool] = ..., selected_contacts: Optional[bool] = ..., out: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., fwd_from: Optional[aliases.AnyStoryFwdHeader] = ..., caption: Optional[str] = ..., entities: Optional[list[aliases.AnyMessageEntity]] = ..., media_areas: Optional[list[aliases.AnyMediaArea]] = ..., privacy: Optional[list[aliases.AnyPrivacyRule]] = ..., views: Optional[aliases.AnyStoryViews] = ..., sent_reaction: Optional[aliases.AnyReaction] = ..., albums: Optional[list[int]] = ...): ...

    def __init__(self, id, date, expire_date, media, _='storyItem', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['expire_date'] = expire_date
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def public(self) -> Optional[bool]:
        return self['public']

    @property
    def close_friends(self) -> Optional[bool]:
        return self['close_friends']

    @property
    def min(self) -> Optional[bool]:
        return self['min']

    @property
    def noforwards(self) -> Optional[bool]:
        return self['noforwards']

    @property
    def edited(self) -> Optional[bool]:
        return self['edited']

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def selected_contacts(self) -> Optional[bool]:
        return self['selected_contacts']

    @property
    def out(self) -> Optional[bool]:
        return self['out']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def fwd_from(self) -> Optional[aliases.AnyStoryFwdHeader]:
        return build_object(self['fwd_from'])

    @property
    def expire_date(self) -> int:
        return self['expire_date']

    @property
    def caption(self) -> Optional[str]:
        return self['caption']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def media(self) -> aliases.AnyMessageMedia:
        return build_object(self['media'])

    @property
    def media_areas(self) -> Optional[list[aliases.AnyMediaArea]]:
        return build_object(self['media_areas'])

    @property
    def privacy(self) -> Optional[list[aliases.AnyPrivacyRule]]:
        return build_object(self['privacy'])

    @property
    def views(self) -> Optional[aliases.AnyStoryViews]:
        return build_object(self['views'])

    @property
    def sent_reaction(self) -> Optional[aliases.AnyReaction]:
        return build_object(self['sent_reaction'])

    @property
    def albums(self) -> Optional[list[int]]:
        return self['albums']


class StoryView(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, date: int, blocked: Optional[bool] = ..., blocked_my_stories_from: Optional[bool] = ..., reaction: Optional[aliases.AnyReaction] = ...): ...

    def __init__(self, user_id, date, _='storyView', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def blocked_my_stories_from(self) -> Optional[bool]:
        return self['blocked_my_stories_from']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def reaction(self) -> Optional[aliases.AnyReaction]:
        return build_object(self['reaction'])


class StoryViewPublicForward(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage, blocked: Optional[bool] = ..., blocked_my_stories_from: Optional[bool] = ...): ...

    def __init__(self, message, _='storyViewPublicForward', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def blocked_my_stories_from(self) -> Optional[bool]:
        return self['blocked_my_stories_from']

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class StoryViewPublicRepost(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, story: aliases.AnyStoryItem, blocked: Optional[bool] = ..., blocked_my_stories_from: Optional[bool] = ...): ...

    def __init__(self, peer_id, story, _='storyViewPublicRepost', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['story'] = story
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def blocked(self) -> Optional[bool]:
        return self['blocked']

    @property
    def blocked_my_stories_from(self) -> Optional[bool]:
        return self['blocked_my_stories_from']

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def story(self) -> aliases.AnyStoryItem:
        return build_object(self['story'])


class InputReplyToMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, reply_to_msg_id: int, top_msg_id: Optional[int] = ..., reply_to_peer_id: Optional[aliases.AnyInputPeer] = ..., quote_text: Optional[str] = ..., quote_entities: Optional[list[aliases.AnyMessageEntity]] = ..., quote_offset: Optional[int] = ..., monoforum_peer_id: Optional[aliases.AnyInputPeer] = ..., todo_item_id: Optional[int] = ...): ...

    def __init__(self, reply_to_msg_id, _='inputReplyToMessage', **kwargs):
        kwargs['reply_to_msg_id'] = reply_to_msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reply_to_msg_id(self) -> int:
        return self['reply_to_msg_id']

    @property
    def top_msg_id(self) -> Optional[int]:
        return self['top_msg_id']

    @property
    def reply_to_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['reply_to_peer_id'])

    @property
    def quote_text(self) -> Optional[str]:
        return self['quote_text']

    @property
    def quote_entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['quote_entities'])

    @property
    def quote_offset(self) -> Optional[int]:
        return self['quote_offset']

    @property
    def monoforum_peer_id(self) -> Optional[aliases.AnyInputPeer]:
        return build_object(self['monoforum_peer_id'])

    @property
    def todo_item_id(self) -> Optional[int]:
        return self['todo_item_id']


class InputReplyToStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, story_id: int): ...

    def __init__(self, peer, story_id, _='inputReplyToStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['story_id'] = story_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def story_id(self) -> int:
        return self['story_id']


class InputReplyToMonoForum(dict):
    __slots__ = ()

    @overload
    def __init__(self, monoforum_peer_id: aliases.AnyInputPeer): ...

    def __init__(self, monoforum_peer_id, _='inputReplyToMonoForum', **kwargs):
        kwargs['monoforum_peer_id'] = monoforum_peer_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def monoforum_peer_id(self) -> aliases.AnyInputPeer:
        return build_object(self['monoforum_peer_id'])


class ExportedStoryLink(dict):
    __slots__ = ()

    @overload
    def __init__(self, link: str): ...

    def __init__(self, link, _='exportedStoryLink', **kwargs):
        kwargs['link'] = link
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def link(self) -> str:
        return self['link']


class StoriesStealthMode(dict):
    __slots__ = ()

    @overload
    def __init__(self, active_until_date: Optional[int] = ..., cooldown_until_date: Optional[int] = ...): ...

    def __init__(self, _='storiesStealthMode', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def active_until_date(self) -> Optional[int]:
        return self['active_until_date']

    @property
    def cooldown_until_date(self) -> Optional[int]:
        return self['cooldown_until_date']


class MediaAreaCoordinates(dict):
    __slots__ = ()

    @overload
    def __init__(self, x: float, y: float, w: float, h: float, rotation: float, radius: Optional[float] = ...): ...

    def __init__(self, x, y, w, h, rotation, _='mediaAreaCoordinates', **kwargs):
        kwargs['x'] = x
        kwargs['y'] = y
        kwargs['w'] = w
        kwargs['h'] = h
        kwargs['rotation'] = rotation
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def x(self) -> float:
        return self['x']

    @property
    def y(self) -> float:
        return self['y']

    @property
    def w(self) -> float:
        return self['w']

    @property
    def h(self) -> float:
        return self['h']

    @property
    def rotation(self) -> float:
        return self['rotation']

    @property
    def radius(self) -> Optional[float]:
        return self['radius']


class MediaAreaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, geo: aliases.AnyGeoPoint, title: str, address: str, provider: str, venue_id: str, venue_type: str): ...

    def __init__(self, coordinates, geo, title, address, provider, venue_id, venue_type, _='mediaAreaVenue', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['geo'] = geo
        kwargs['title'] = title
        kwargs['address'] = address
        kwargs['provider'] = provider
        kwargs['venue_id'] = venue_id
        kwargs['venue_type'] = venue_type
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def title(self) -> str:
        return self['title']

    @property
    def address(self) -> str:
        return self['address']

    @property
    def provider(self) -> str:
        return self['provider']

    @property
    def venue_id(self) -> str:
        return self['venue_id']

    @property
    def venue_type(self) -> str:
        return self['venue_type']


class InputMediaAreaVenue(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, query_id: int, result_id: str): ...

    def __init__(self, coordinates, query_id, result_id, _='inputMediaAreaVenue', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['query_id'] = query_id
        kwargs['result_id'] = result_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def query_id(self) -> int:
        return self['query_id']

    @property
    def result_id(self) -> str:
        return self['result_id']


class MediaAreaGeoPoint(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, geo: aliases.AnyGeoPoint, address: Optional[aliases.AnyGeoPointAddress] = ...): ...

    def __init__(self, coordinates, geo, _='mediaAreaGeoPoint', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['geo'] = geo
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def geo(self) -> aliases.AnyGeoPoint:
        return build_object(self['geo'])

    @property
    def address(self) -> Optional[aliases.AnyGeoPointAddress]:
        return build_object(self['address'])


class MediaAreaSuggestedReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, reaction: aliases.AnyReaction, dark: Optional[bool] = ..., flipped: Optional[bool] = ...): ...

    def __init__(self, coordinates, reaction, _='mediaAreaSuggestedReaction', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def dark(self) -> Optional[bool]:
        return self['dark']

    @property
    def flipped(self) -> Optional[bool]:
        return self['flipped']

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class MediaAreaChannelPost(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, channel_id: int, msg_id: int): ...

    def __init__(self, coordinates, channel_id, msg_id, _='mediaAreaChannelPost', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['channel_id'] = channel_id
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class InputMediaAreaChannelPost(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, channel: aliases.AnyInputChannel, msg_id: int): ...

    def __init__(self, coordinates, channel, msg_id, _='inputMediaAreaChannelPost', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['channel'] = channel
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def channel(self) -> aliases.AnyInputChannel:
        return build_object(self['channel'])

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class MediaAreaUrl(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, url: str): ...

    def __init__(self, coordinates, url, _='mediaAreaUrl', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def url(self) -> str:
        return self['url']


class MediaAreaWeather(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, emoji: str, temperature_c: float, color: int): ...

    def __init__(self, coordinates, emoji, temperature_c, color, _='mediaAreaWeather', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['emoji'] = emoji
        kwargs['temperature_c'] = temperature_c
        kwargs['color'] = color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def emoji(self) -> str:
        return self['emoji']

    @property
    def temperature_c(self) -> float:
        return self['temperature_c']

    @property
    def color(self) -> int:
        return self['color']


class MediaAreaStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, coordinates: aliases.AnyMediaAreaCoordinates, slug: str): ...

    def __init__(self, coordinates, slug, _='mediaAreaStarGift', **kwargs):
        kwargs['coordinates'] = coordinates
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def coordinates(self) -> aliases.AnyMediaAreaCoordinates:
        return build_object(self['coordinates'])

    @property
    def slug(self) -> str:
        return self['slug']


class PeerStories(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, stories: list[aliases.AnyStoryItem], max_read_id: Optional[int] = ...): ...

    def __init__(self, peer, stories, _='peerStories', **kwargs):
        kwargs['peer'] = peer
        kwargs['stories'] = stories
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def max_read_id(self) -> Optional[int]:
        return self['max_read_id']

    @property
    def stories(self) -> list[aliases.AnyStoryItem]:
        return build_object(self['stories'])


class PremiumGiftCodeOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: int, months: int, currency: str, amount: int, store_product: Optional[str] = ..., store_quantity: Optional[int] = ...): ...

    def __init__(self, users, months, currency, amount, _='premiumGiftCodeOption', **kwargs):
        kwargs['users'] = users
        kwargs['months'] = months
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def users(self) -> int:
        return self['users']

    @property
    def months(self) -> int:
        return self['months']

    @property
    def store_product(self) -> Optional[str]:
        return self['store_product']

    @property
    def store_quantity(self) -> Optional[int]:
        return self['store_quantity']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class PrepaidGiveaway(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, months: int, quantity: int, date: int): ...

    def __init__(self, id, months, quantity, date, _='prepaidGiveaway', **kwargs):
        kwargs['id'] = id
        kwargs['months'] = months
        kwargs['quantity'] = quantity
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def months(self) -> int:
        return self['months']

    @property
    def quantity(self) -> int:
        return self['quantity']

    @property
    def date(self) -> int:
        return self['date']


class PrepaidStarsGiveaway(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, stars: int, quantity: int, boosts: int, date: int): ...

    def __init__(self, id, stars, quantity, boosts, date, _='prepaidStarsGiveaway', **kwargs):
        kwargs['id'] = id
        kwargs['stars'] = stars
        kwargs['quantity'] = quantity
        kwargs['boosts'] = boosts
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def quantity(self) -> int:
        return self['quantity']

    @property
    def boosts(self) -> int:
        return self['boosts']

    @property
    def date(self) -> int:
        return self['date']


class Boost(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, date: int, expires: int, gift: Optional[bool] = ..., giveaway: Optional[bool] = ..., unclaimed: Optional[bool] = ..., user_id: Optional[int] = ..., giveaway_msg_id: Optional[int] = ..., used_gift_slug: Optional[str] = ..., multiplier: Optional[int] = ..., stars: Optional[int] = ...): ...

    def __init__(self, id, date, expires, _='boost', **kwargs):
        kwargs['id'] = id
        kwargs['date'] = date
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> Optional[bool]:
        return self['gift']

    @property
    def giveaway(self) -> Optional[bool]:
        return self['giveaway']

    @property
    def unclaimed(self) -> Optional[bool]:
        return self['unclaimed']

    @property
    def id(self) -> str:
        return self['id']

    @property
    def user_id(self) -> Optional[int]:
        return self['user_id']

    @property
    def giveaway_msg_id(self) -> Optional[int]:
        return self['giveaway_msg_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def used_gift_slug(self) -> Optional[str]:
        return self['used_gift_slug']

    @property
    def multiplier(self) -> Optional[int]:
        return self['multiplier']

    @property
    def stars(self) -> Optional[int]:
        return self['stars']


class MyBoost(dict):
    __slots__ = ()

    @overload
    def __init__(self, slot: int, date: int, expires: int, peer: Optional[aliases.AnyPeer] = ..., cooldown_until_date: Optional[int] = ...): ...

    def __init__(self, slot, date, expires, _='myBoost', **kwargs):
        kwargs['slot'] = slot
        kwargs['date'] = date
        kwargs['expires'] = expires
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slot(self) -> int:
        return self['slot']

    @property
    def peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def expires(self) -> int:
        return self['expires']

    @property
    def cooldown_until_date(self) -> Optional[int]:
        return self['cooldown_until_date']


class StoryFwdHeader(dict):
    __slots__ = ()

    @overload
    def __init__(self, modified: Optional[bool] = ..., from_: Optional[aliases.AnyPeer] = ..., from_name: Optional[str] = ..., story_id: Optional[int] = ...): ...

    def __init__(self, _='storyFwdHeader', **kwargs):
        if 'from_' in kwargs:
            kwargs['from'] = kwargs.pop('from_')
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def modified(self) -> Optional[bool]:
        return self['modified']

    @property
    def from_(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from'])

    @property
    def from_name(self) -> Optional[str]:
        return self['from_name']

    @property
    def story_id(self) -> Optional[int]:
        return self['story_id']


class PostInteractionCountersMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int, views: int, forwards: int, reactions: int): ...

    def __init__(self, msg_id, views, forwards, reactions, _='postInteractionCountersMessage', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['views'] = views
        kwargs['forwards'] = forwards
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']

    @property
    def views(self) -> int:
        return self['views']

    @property
    def forwards(self) -> int:
        return self['forwards']

    @property
    def reactions(self) -> int:
        return self['reactions']


class PostInteractionCountersStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, story_id: int, views: int, forwards: int, reactions: int): ...

    def __init__(self, story_id, views, forwards, reactions, _='postInteractionCountersStory', **kwargs):
        kwargs['story_id'] = story_id
        kwargs['views'] = views
        kwargs['forwards'] = forwards
        kwargs['reactions'] = reactions
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def story_id(self) -> int:
        return self['story_id']

    @property
    def views(self) -> int:
        return self['views']

    @property
    def forwards(self) -> int:
        return self['forwards']

    @property
    def reactions(self) -> int:
        return self['reactions']


class PublicForwardMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='publicForwardMessage', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class PublicForwardStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, story: aliases.AnyStoryItem): ...

    def __init__(self, peer, story, _='publicForwardStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['story'] = story
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def story(self) -> aliases.AnyStoryItem:
        return build_object(self['story'])


class PeerColor(dict):
    __slots__ = ()

    @overload
    def __init__(self, color: Optional[int] = ..., background_emoji_id: Optional[int] = ...): ...

    def __init__(self, _='peerColor', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def color(self) -> Optional[int]:
        return self['color']

    @property
    def background_emoji_id(self) -> Optional[int]:
        return self['background_emoji_id']


class PeerColorCollectible(dict):
    __slots__ = ()

    @overload
    def __init__(self, collectible_id: int, gift_emoji_id: int, background_emoji_id: int, accent_color: int, colors: list[int], dark_accent_color: Optional[int] = ..., dark_colors: Optional[list[int]] = ...): ...

    def __init__(self, collectible_id, gift_emoji_id, background_emoji_id, accent_color, colors, _='peerColorCollectible', **kwargs):
        kwargs['collectible_id'] = collectible_id
        kwargs['gift_emoji_id'] = gift_emoji_id
        kwargs['background_emoji_id'] = background_emoji_id
        kwargs['accent_color'] = accent_color
        kwargs['colors'] = colors
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collectible_id(self) -> int:
        return self['collectible_id']

    @property
    def gift_emoji_id(self) -> int:
        return self['gift_emoji_id']

    @property
    def background_emoji_id(self) -> int:
        return self['background_emoji_id']

    @property
    def accent_color(self) -> int:
        return self['accent_color']

    @property
    def colors(self) -> list[int]:
        return self['colors']

    @property
    def dark_accent_color(self) -> Optional[int]:
        return self['dark_accent_color']

    @property
    def dark_colors(self) -> Optional[list[int]]:
        return self['dark_colors']


class InputPeerColorCollectible(dict):
    __slots__ = ()

    @overload
    def __init__(self, collectible_id: int): ...

    def __init__(self, collectible_id, _='inputPeerColorCollectible', **kwargs):
        kwargs['collectible_id'] = collectible_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collectible_id(self) -> int:
        return self['collectible_id']


class StoryReaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, date: int, reaction: aliases.AnyReaction): ...

    def __init__(self, peer_id, date, reaction, _='storyReaction', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['date'] = date
        kwargs['reaction'] = reaction
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])


class StoryReactionPublicForward(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: aliases.AnyMessage): ...

    def __init__(self, message, _='storyReactionPublicForward', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> aliases.AnyMessage:
        return build_object(self['message'])


class StoryReactionPublicRepost(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer_id: aliases.AnyPeer, story: aliases.AnyStoryItem): ...

    def __init__(self, peer_id, story, _='storyReactionPublicRepost', **kwargs):
        kwargs['peer_id'] = peer_id
        kwargs['story'] = story
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer_id(self) -> aliases.AnyPeer:
        return build_object(self['peer_id'])

    @property
    def story(self) -> aliases.AnyStoryItem:
        return build_object(self['story'])


class SavedDialog(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, top_message: int, pinned: Optional[bool] = ...): ...

    def __init__(self, peer, top_message, _='savedDialog', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_message'] = top_message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pinned(self) -> Optional[bool]:
        return self['pinned']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_message(self) -> int:
        return self['top_message']


class MonoForumDialog(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_reactions_count: int, unread_mark: Optional[bool] = ..., nopaid_messages_exception: Optional[bool] = ..., draft: Optional[aliases.AnyDraftMessage] = ...): ...

    def __init__(self, peer, top_message, read_inbox_max_id, read_outbox_max_id, unread_count, unread_reactions_count, _='monoForumDialog', **kwargs):
        kwargs['peer'] = peer
        kwargs['top_message'] = top_message
        kwargs['read_inbox_max_id'] = read_inbox_max_id
        kwargs['read_outbox_max_id'] = read_outbox_max_id
        kwargs['unread_count'] = unread_count
        kwargs['unread_reactions_count'] = unread_reactions_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def unread_mark(self) -> Optional[bool]:
        return self['unread_mark']

    @property
    def nopaid_messages_exception(self) -> Optional[bool]:
        return self['nopaid_messages_exception']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def top_message(self) -> int:
        return self['top_message']

    @property
    def read_inbox_max_id(self) -> int:
        return self['read_inbox_max_id']

    @property
    def read_outbox_max_id(self) -> int:
        return self['read_outbox_max_id']

    @property
    def unread_count(self) -> int:
        return self['unread_count']

    @property
    def unread_reactions_count(self) -> int:
        return self['unread_reactions_count']

    @property
    def draft(self) -> Optional[aliases.AnyDraftMessage]:
        return build_object(self['draft'])


class SavedReactionTag(dict):
    __slots__ = ()

    @overload
    def __init__(self, reaction: aliases.AnyReaction, count: int, title: Optional[str] = ...): ...

    def __init__(self, reaction, count, _='savedReactionTag', **kwargs):
        kwargs['reaction'] = reaction
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reaction(self) -> aliases.AnyReaction:
        return build_object(self['reaction'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def count(self) -> int:
        return self['count']


class OutboxReadDate(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int): ...

    def __init__(self, date, _='outboxReadDate', **kwargs):
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']


class SmsJob(dict):
    __slots__ = ()

    @overload
    def __init__(self, job_id: str, phone_number: str, text: str): ...

    def __init__(self, job_id, phone_number, text, _='smsJob', **kwargs):
        kwargs['job_id'] = job_id
        kwargs['phone_number'] = phone_number
        kwargs['text'] = text
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def job_id(self) -> str:
        return self['job_id']

    @property
    def phone_number(self) -> str:
        return self['phone_number']

    @property
    def text(self) -> str:
        return self['text']


class BusinessWeeklyOpen(dict):
    __slots__ = ()

    @overload
    def __init__(self, start_minute: int, end_minute: int): ...

    def __init__(self, start_minute, end_minute, _='businessWeeklyOpen', **kwargs):
        kwargs['start_minute'] = start_minute
        kwargs['end_minute'] = end_minute
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def start_minute(self) -> int:
        return self['start_minute']

    @property
    def end_minute(self) -> int:
        return self['end_minute']


class BusinessWorkHours(dict):
    __slots__ = ()

    @overload
    def __init__(self, timezone_id: str, weekly_open: list[aliases.AnyBusinessWeeklyOpen], open_now: Optional[bool] = ...): ...

    def __init__(self, timezone_id, weekly_open, _='businessWorkHours', **kwargs):
        kwargs['timezone_id'] = timezone_id
        kwargs['weekly_open'] = weekly_open
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def open_now(self) -> Optional[bool]:
        return self['open_now']

    @property
    def timezone_id(self) -> str:
        return self['timezone_id']

    @property
    def weekly_open(self) -> list[aliases.AnyBusinessWeeklyOpen]:
        return build_object(self['weekly_open'])


class BusinessLocation(dict):
    __slots__ = ()

    @overload
    def __init__(self, address: str, geo_point: Optional[aliases.AnyGeoPoint] = ...): ...

    def __init__(self, address, _='businessLocation', **kwargs):
        kwargs['address'] = address
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def geo_point(self) -> Optional[aliases.AnyGeoPoint]:
        return build_object(self['geo_point'])

    @property
    def address(self) -> str:
        return self['address']


class InputBusinessRecipients(dict):
    __slots__ = ()

    @overload
    def __init__(self, existing_chats: Optional[bool] = ..., new_chats: Optional[bool] = ..., contacts: Optional[bool] = ..., non_contacts: Optional[bool] = ..., exclude_selected: Optional[bool] = ..., users: Optional[list[aliases.AnyInputUser]] = ...): ...

    def __init__(self, _='inputBusinessRecipients', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def existing_chats(self) -> Optional[bool]:
        return self['existing_chats']

    @property
    def new_chats(self) -> Optional[bool]:
        return self['new_chats']

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def non_contacts(self) -> Optional[bool]:
        return self['non_contacts']

    @property
    def exclude_selected(self) -> Optional[bool]:
        return self['exclude_selected']

    @property
    def users(self) -> Optional[list[aliases.AnyInputUser]]:
        return build_object(self['users'])


class BusinessRecipients(dict):
    __slots__ = ()

    @overload
    def __init__(self, existing_chats: Optional[bool] = ..., new_chats: Optional[bool] = ..., contacts: Optional[bool] = ..., non_contacts: Optional[bool] = ..., exclude_selected: Optional[bool] = ..., users: Optional[list[int]] = ...): ...

    def __init__(self, _='businessRecipients', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def existing_chats(self) -> Optional[bool]:
        return self['existing_chats']

    @property
    def new_chats(self) -> Optional[bool]:
        return self['new_chats']

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def non_contacts(self) -> Optional[bool]:
        return self['non_contacts']

    @property
    def exclude_selected(self) -> Optional[bool]:
        return self['exclude_selected']

    @property
    def users(self) -> Optional[list[int]]:
        return self['users']


class BusinessAwayMessageScheduleAlways(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='businessAwayMessageScheduleAlways'):
        dict.__init__(self, _=_)


class BusinessAwayMessageScheduleOutsideWorkHours(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='businessAwayMessageScheduleOutsideWorkHours'):
        dict.__init__(self, _=_)


class BusinessAwayMessageScheduleCustom(dict):
    __slots__ = ()

    @overload
    def __init__(self, start_date: int, end_date: int): ...

    def __init__(self, start_date, end_date, _='businessAwayMessageScheduleCustom', **kwargs):
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def end_date(self) -> int:
        return self['end_date']


class InputBusinessGreetingMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, recipients: aliases.AnyInputBusinessRecipients, no_activity_days: int): ...

    def __init__(self, shortcut_id, recipients, no_activity_days, _='inputBusinessGreetingMessage', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['recipients'] = recipients
        kwargs['no_activity_days'] = no_activity_days
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def recipients(self) -> aliases.AnyInputBusinessRecipients:
        return build_object(self['recipients'])

    @property
    def no_activity_days(self) -> int:
        return self['no_activity_days']


class BusinessGreetingMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, recipients: aliases.AnyBusinessRecipients, no_activity_days: int): ...

    def __init__(self, shortcut_id, recipients, no_activity_days, _='businessGreetingMessage', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['recipients'] = recipients
        kwargs['no_activity_days'] = no_activity_days
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def recipients(self) -> aliases.AnyBusinessRecipients:
        return build_object(self['recipients'])

    @property
    def no_activity_days(self) -> int:
        return self['no_activity_days']


class InputBusinessAwayMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, schedule: aliases.AnyBusinessAwayMessageSchedule, recipients: aliases.AnyInputBusinessRecipients, offline_only: Optional[bool] = ...): ...

    def __init__(self, shortcut_id, schedule, recipients, _='inputBusinessAwayMessage', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['schedule'] = schedule
        kwargs['recipients'] = recipients
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offline_only(self) -> Optional[bool]:
        return self['offline_only']

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def schedule(self) -> aliases.AnyBusinessAwayMessageSchedule:
        return build_object(self['schedule'])

    @property
    def recipients(self) -> aliases.AnyInputBusinessRecipients:
        return build_object(self['recipients'])


class BusinessAwayMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, schedule: aliases.AnyBusinessAwayMessageSchedule, recipients: aliases.AnyBusinessRecipients, offline_only: Optional[bool] = ...): ...

    def __init__(self, shortcut_id, schedule, recipients, _='businessAwayMessage', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['schedule'] = schedule
        kwargs['recipients'] = recipients
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def offline_only(self) -> Optional[bool]:
        return self['offline_only']

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def schedule(self) -> aliases.AnyBusinessAwayMessageSchedule:
        return build_object(self['schedule'])

    @property
    def recipients(self) -> aliases.AnyBusinessRecipients:
        return build_object(self['recipients'])


class Timezone(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, name: str, utc_offset: int): ...

    def __init__(self, id, name, utc_offset, _='timezone', **kwargs):
        kwargs['id'] = id
        kwargs['name'] = name
        kwargs['utc_offset'] = utc_offset
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def utc_offset(self) -> int:
        return self['utc_offset']


class QuickReply(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int, shortcut: str, top_message: int, count: int): ...

    def __init__(self, shortcut_id, shortcut, top_message, count, _='quickReply', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['shortcut'] = shortcut
        kwargs['top_message'] = top_message
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']

    @property
    def shortcut(self) -> str:
        return self['shortcut']

    @property
    def top_message(self) -> int:
        return self['top_message']

    @property
    def count(self) -> int:
        return self['count']


class InputQuickReplyShortcut(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut: str): ...

    def __init__(self, shortcut, _='inputQuickReplyShortcut', **kwargs):
        kwargs['shortcut'] = shortcut
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut(self) -> str:
        return self['shortcut']


class InputQuickReplyShortcutId(dict):
    __slots__ = ()

    @overload
    def __init__(self, shortcut_id: int): ...

    def __init__(self, shortcut_id, _='inputQuickReplyShortcutId', **kwargs):
        kwargs['shortcut_id'] = shortcut_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def shortcut_id(self) -> int:
        return self['shortcut_id']


class ConnectedBot(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, recipients: aliases.AnyBusinessBotRecipients, rights: aliases.AnyBusinessBotRights): ...

    def __init__(self, bot_id, recipients, rights, _='connectedBot', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['recipients'] = recipients
        kwargs['rights'] = rights
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def recipients(self) -> aliases.AnyBusinessBotRecipients:
        return build_object(self['recipients'])

    @property
    def rights(self) -> aliases.AnyBusinessBotRights:
        return build_object(self['rights'])


class Birthday(dict):
    __slots__ = ()

    @overload
    def __init__(self, day: int, month: int, year: Optional[int] = ...): ...

    def __init__(self, day, month, _='birthday', **kwargs):
        kwargs['day'] = day
        kwargs['month'] = month
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def day(self) -> int:
        return self['day']

    @property
    def month(self) -> int:
        return self['month']

    @property
    def year(self) -> Optional[int]:
        return self['year']


class BotBusinessConnection(dict):
    __slots__ = ()

    @overload
    def __init__(self, connection_id: str, user_id: int, dc_id: int, date: int, disabled: Optional[bool] = ..., rights: Optional[aliases.AnyBusinessBotRights] = ...): ...

    def __init__(self, connection_id, user_id, dc_id, date, _='botBusinessConnection', **kwargs):
        kwargs['connection_id'] = connection_id
        kwargs['user_id'] = user_id
        kwargs['dc_id'] = dc_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def disabled(self) -> Optional[bool]:
        return self['disabled']

    @property
    def connection_id(self) -> str:
        return self['connection_id']

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def dc_id(self) -> int:
        return self['dc_id']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def rights(self) -> Optional[aliases.AnyBusinessBotRights]:
        return build_object(self['rights'])


class InputBusinessIntro(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, sticker: Optional[aliases.AnyInputDocument] = ...): ...

    def __init__(self, title, description, _='inputBusinessIntro', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def sticker(self) -> Optional[aliases.AnyInputDocument]:
        return build_object(self['sticker'])


class BusinessIntro(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, description: str, sticker: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, title, description, _='businessIntro', **kwargs):
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def description(self) -> str:
        return self['description']

    @property
    def sticker(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['sticker'])


class InputCollectibleUsername(dict):
    __slots__ = ()

    @overload
    def __init__(self, username: str): ...

    def __init__(self, username, _='inputCollectibleUsername', **kwargs):
        kwargs['username'] = username
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def username(self) -> str:
        return self['username']


class InputCollectiblePhone(dict):
    __slots__ = ()

    @overload
    def __init__(self, phone: str): ...

    def __init__(self, phone, _='inputCollectiblePhone', **kwargs):
        kwargs['phone'] = phone
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def phone(self) -> str:
        return self['phone']


class InputBusinessBotRecipients(dict):
    __slots__ = ()

    @overload
    def __init__(self, existing_chats: Optional[bool] = ..., new_chats: Optional[bool] = ..., contacts: Optional[bool] = ..., non_contacts: Optional[bool] = ..., exclude_selected: Optional[bool] = ..., users: Optional[list[aliases.AnyInputUser]] = ..., exclude_users: Optional[list[aliases.AnyInputUser]] = ...): ...

    def __init__(self, _='inputBusinessBotRecipients', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def existing_chats(self) -> Optional[bool]:
        return self['existing_chats']

    @property
    def new_chats(self) -> Optional[bool]:
        return self['new_chats']

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def non_contacts(self) -> Optional[bool]:
        return self['non_contacts']

    @property
    def exclude_selected(self) -> Optional[bool]:
        return self['exclude_selected']

    @property
    def users(self) -> Optional[list[aliases.AnyInputUser]]:
        return build_object(self['users'])

    @property
    def exclude_users(self) -> Optional[list[aliases.AnyInputUser]]:
        return build_object(self['exclude_users'])


class BusinessBotRecipients(dict):
    __slots__ = ()

    @overload
    def __init__(self, existing_chats: Optional[bool] = ..., new_chats: Optional[bool] = ..., contacts: Optional[bool] = ..., non_contacts: Optional[bool] = ..., exclude_selected: Optional[bool] = ..., users: Optional[list[int]] = ..., exclude_users: Optional[list[int]] = ...): ...

    def __init__(self, _='businessBotRecipients', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def existing_chats(self) -> Optional[bool]:
        return self['existing_chats']

    @property
    def new_chats(self) -> Optional[bool]:
        return self['new_chats']

    @property
    def contacts(self) -> Optional[bool]:
        return self['contacts']

    @property
    def non_contacts(self) -> Optional[bool]:
        return self['non_contacts']

    @property
    def exclude_selected(self) -> Optional[bool]:
        return self['exclude_selected']

    @property
    def users(self) -> Optional[list[int]]:
        return self['users']

    @property
    def exclude_users(self) -> Optional[list[int]]:
        return self['exclude_users']


class ContactBirthday(dict):
    __slots__ = ()

    @overload
    def __init__(self, contact_id: int, birthday: aliases.AnyBirthday): ...

    def __init__(self, contact_id, birthday, _='contactBirthday', **kwargs):
        kwargs['contact_id'] = contact_id
        kwargs['birthday'] = birthday
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def contact_id(self) -> int:
        return self['contact_id']

    @property
    def birthday(self) -> aliases.AnyBirthday:
        return build_object(self['birthday'])


class MissingInvitee(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, premium_would_allow_invite: Optional[bool] = ..., premium_required_for_pm: Optional[bool] = ...): ...

    def __init__(self, user_id, _='missingInvitee', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def premium_would_allow_invite(self) -> Optional[bool]:
        return self['premium_would_allow_invite']

    @property
    def premium_required_for_pm(self) -> Optional[bool]:
        return self['premium_required_for_pm']

    @property
    def user_id(self) -> int:
        return self['user_id']


class InputBusinessChatLink(dict):
    __slots__ = ()

    @overload
    def __init__(self, message: str, entities: Optional[list[aliases.AnyMessageEntity]] = ..., title: Optional[str] = ...): ...

    def __init__(self, message, _='inputBusinessChatLink', **kwargs):
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def title(self) -> Optional[str]:
        return self['title']


class BusinessChatLink(dict):
    __slots__ = ()

    @overload
    def __init__(self, link: str, message: str, views: int, entities: Optional[list[aliases.AnyMessageEntity]] = ..., title: Optional[str] = ...): ...

    def __init__(self, link, message, views, _='businessChatLink', **kwargs):
        kwargs['link'] = link
        kwargs['message'] = message
        kwargs['views'] = views
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def link(self) -> str:
        return self['link']

    @property
    def message(self) -> str:
        return self['message']

    @property
    def entities(self) -> Optional[list[aliases.AnyMessageEntity]]:
        return build_object(self['entities'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def views(self) -> int:
        return self['views']


class RequestedPeerUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, user_id: int, first_name: Optional[str] = ..., last_name: Optional[str] = ..., username: Optional[str] = ..., photo: Optional[aliases.AnyPhoto] = ...): ...

    def __init__(self, user_id, _='requestedPeerUser', **kwargs):
        kwargs['user_id'] = user_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def user_id(self) -> int:
        return self['user_id']

    @property
    def first_name(self) -> Optional[str]:
        return self['first_name']

    @property
    def last_name(self) -> Optional[str]:
        return self['last_name']

    @property
    def username(self) -> Optional[str]:
        return self['username']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])


class RequestedPeerChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, chat_id: int, title: Optional[str] = ..., photo: Optional[aliases.AnyPhoto] = ...): ...

    def __init__(self, chat_id, _='requestedPeerChat', **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def chat_id(self) -> int:
        return self['chat_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])


class RequestedPeerChannel(dict):
    __slots__ = ()

    @overload
    def __init__(self, channel_id: int, title: Optional[str] = ..., username: Optional[str] = ..., photo: Optional[aliases.AnyPhoto] = ...): ...

    def __init__(self, channel_id, _='requestedPeerChannel', **kwargs):
        kwargs['channel_id'] = channel_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def channel_id(self) -> int:
        return self['channel_id']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def username(self) -> Optional[str]:
        return self['username']

    @property
    def photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['photo'])


class SponsoredMessageReportOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, option: bytes): ...

    def __init__(self, text, option, _='sponsoredMessageReportOption', **kwargs):
        kwargs['text'] = text
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def option(self) -> bytes:
        return self['option']


class ReactionNotificationsFromContacts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='reactionNotificationsFromContacts'):
        dict.__init__(self, _=_)


class ReactionNotificationsFromAll(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='reactionNotificationsFromAll'):
        dict.__init__(self, _=_)


class ReactionsNotifySettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, sound: aliases.AnyNotificationSound, show_previews: bool, messages_notify_from: Optional[aliases.AnyReactionNotificationsFrom] = ..., stories_notify_from: Optional[aliases.AnyReactionNotificationsFrom] = ...): ...

    def __init__(self, sound, show_previews, _='reactionsNotifySettings', **kwargs):
        kwargs['sound'] = sound
        kwargs['show_previews'] = show_previews
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def messages_notify_from(self) -> Optional[aliases.AnyReactionNotificationsFrom]:
        return build_object(self['messages_notify_from'])

    @property
    def stories_notify_from(self) -> Optional[aliases.AnyReactionNotificationsFrom]:
        return build_object(self['stories_notify_from'])

    @property
    def sound(self) -> aliases.AnyNotificationSound:
        return build_object(self['sound'])

    @property
    def show_previews(self) -> bool:
        return self['show_previews']


class AvailableEffect(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, emoticon: str, effect_sticker_id: int, premium_required: Optional[bool] = ..., static_icon_id: Optional[int] = ..., effect_animation_id: Optional[int] = ...): ...

    def __init__(self, id, emoticon, effect_sticker_id, _='availableEffect', **kwargs):
        kwargs['id'] = id
        kwargs['emoticon'] = emoticon
        kwargs['effect_sticker_id'] = effect_sticker_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def premium_required(self) -> Optional[bool]:
        return self['premium_required']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def emoticon(self) -> str:
        return self['emoticon']

    @property
    def static_icon_id(self) -> Optional[int]:
        return self['static_icon_id']

    @property
    def effect_sticker_id(self) -> int:
        return self['effect_sticker_id']

    @property
    def effect_animation_id(self) -> Optional[int]:
        return self['effect_animation_id']


class FactCheck(dict):
    __slots__ = ()

    @overload
    def __init__(self, hash: int, need_check: Optional[bool] = ..., country: Optional[str] = ..., text: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, hash, _='factCheck', **kwargs):
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def need_check(self) -> Optional[bool]:
        return self['need_check']

    @property
    def country(self) -> Optional[str]:
        return self['country']

    @property
    def text(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['text'])

    @property
    def hash(self) -> int:
        return self['hash']


class StarsTransactionPeerUnsupported(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerUnsupported'):
        dict.__init__(self, _=_)


class StarsTransactionPeerAppStore(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerAppStore'):
        dict.__init__(self, _=_)


class StarsTransactionPeerPlayMarket(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerPlayMarket'):
        dict.__init__(self, _=_)


class StarsTransactionPeerPremiumBot(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerPremiumBot'):
        dict.__init__(self, _=_)


class StarsTransactionPeerFragment(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerFragment'):
        dict.__init__(self, _=_)


class StarsTransactionPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer): ...

    def __init__(self, peer, _='starsTransactionPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])


class StarsTransactionPeerAds(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerAds'):
        dict.__init__(self, _=_)


class StarsTransactionPeerAPI(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starsTransactionPeerAPI'):
        dict.__init__(self, _=_)


class StarsTopupOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, currency: str, amount: int, extended: Optional[bool] = ..., store_product: Optional[str] = ...): ...

    def __init__(self, stars, currency, amount, _='starsTopupOption', **kwargs):
        kwargs['stars'] = stars
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def extended(self) -> Optional[bool]:
        return self['extended']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def store_product(self) -> Optional[str]:
        return self['store_product']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class StarsTransaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, amount: aliases.AnyStarsAmount, date: int, peer: aliases.AnyStarsTransactionPeer, refund: Optional[bool] = ..., pending: Optional[bool] = ..., failed: Optional[bool] = ..., gift: Optional[bool] = ..., reaction: Optional[bool] = ..., stargift_upgrade: Optional[bool] = ..., business_transfer: Optional[bool] = ..., stargift_resale: Optional[bool] = ..., posts_search: Optional[bool] = ..., stargift_prepaid_upgrade: Optional[bool] = ..., stargift_drop_original_details: Optional[bool] = ..., phonegroup_message: Optional[bool] = ..., stargift_auction_bid: Optional[bool] = ..., offer: Optional[bool] = ..., title: Optional[str] = ..., description: Optional[str] = ..., photo: Optional[aliases.AnyWebDocument] = ..., transaction_date: Optional[int] = ..., transaction_url: Optional[str] = ..., bot_payload: Optional[bytes] = ..., msg_id: Optional[int] = ..., extended_media: Optional[list[aliases.AnyMessageMedia]] = ..., subscription_period: Optional[int] = ..., giveaway_post_id: Optional[int] = ..., stargift: Optional[aliases.AnyStarGift] = ..., floodskip_number: Optional[int] = ..., starref_commission_permille: Optional[int] = ..., starref_peer: Optional[aliases.AnyPeer] = ..., starref_amount: Optional[aliases.AnyStarsAmount] = ..., paid_messages: Optional[int] = ..., premium_gift_months: Optional[int] = ..., ads_proceeds_from_date: Optional[int] = ..., ads_proceeds_to_date: Optional[int] = ...): ...

    def __init__(self, id, amount, date, peer, _='starsTransaction', **kwargs):
        kwargs['id'] = id
        kwargs['amount'] = amount
        kwargs['date'] = date
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def refund(self) -> Optional[bool]:
        return self['refund']

    @property
    def pending(self) -> Optional[bool]:
        return self['pending']

    @property
    def failed(self) -> Optional[bool]:
        return self['failed']

    @property
    def gift(self) -> Optional[bool]:
        return self['gift']

    @property
    def reaction(self) -> Optional[bool]:
        return self['reaction']

    @property
    def stargift_upgrade(self) -> Optional[bool]:
        return self['stargift_upgrade']

    @property
    def business_transfer(self) -> Optional[bool]:
        return self['business_transfer']

    @property
    def stargift_resale(self) -> Optional[bool]:
        return self['stargift_resale']

    @property
    def posts_search(self) -> Optional[bool]:
        return self['posts_search']

    @property
    def stargift_prepaid_upgrade(self) -> Optional[bool]:
        return self['stargift_prepaid_upgrade']

    @property
    def stargift_drop_original_details(self) -> Optional[bool]:
        return self['stargift_drop_original_details']

    @property
    def phonegroup_message(self) -> Optional[bool]:
        return self['phonegroup_message']

    @property
    def stargift_auction_bid(self) -> Optional[bool]:
        return self['stargift_auction_bid']

    @property
    def offer(self) -> Optional[bool]:
        return self['offer']

    @property
    def id(self) -> str:
        return self['id']

    @property
    def amount(self) -> aliases.AnyStarsAmount:
        return build_object(self['amount'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def peer(self) -> aliases.AnyStarsTransactionPeer:
        return build_object(self['peer'])

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def description(self) -> Optional[str]:
        return self['description']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def transaction_date(self) -> Optional[int]:
        return self['transaction_date']

    @property
    def transaction_url(self) -> Optional[str]:
        return self['transaction_url']

    @property
    def bot_payload(self) -> Optional[bytes]:
        return self['bot_payload']

    @property
    def msg_id(self) -> Optional[int]:
        return self['msg_id']

    @property
    def extended_media(self) -> Optional[list[aliases.AnyMessageMedia]]:
        return build_object(self['extended_media'])

    @property
    def subscription_period(self) -> Optional[int]:
        return self['subscription_period']

    @property
    def giveaway_post_id(self) -> Optional[int]:
        return self['giveaway_post_id']

    @property
    def stargift(self) -> Optional[aliases.AnyStarGift]:
        return build_object(self['stargift'])

    @property
    def floodskip_number(self) -> Optional[int]:
        return self['floodskip_number']

    @property
    def starref_commission_permille(self) -> Optional[int]:
        return self['starref_commission_permille']

    @property
    def starref_peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['starref_peer'])

    @property
    def starref_amount(self) -> Optional[aliases.AnyStarsAmount]:
        return build_object(self['starref_amount'])

    @property
    def paid_messages(self) -> Optional[int]:
        return self['paid_messages']

    @property
    def premium_gift_months(self) -> Optional[int]:
        return self['premium_gift_months']

    @property
    def ads_proceeds_from_date(self) -> Optional[int]:
        return self['ads_proceeds_from_date']

    @property
    def ads_proceeds_to_date(self) -> Optional[int]:
        return self['ads_proceeds_to_date']


class FoundStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, story: aliases.AnyStoryItem): ...

    def __init__(self, peer, story, _='foundStory', **kwargs):
        kwargs['peer'] = peer
        kwargs['story'] = story
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def story(self) -> aliases.AnyStoryItem:
        return build_object(self['story'])


class GeoPointAddress(dict):
    __slots__ = ()

    @overload
    def __init__(self, country_iso2: str, state: Optional[str] = ..., city: Optional[str] = ..., street: Optional[str] = ...): ...

    def __init__(self, country_iso2, _='geoPointAddress', **kwargs):
        kwargs['country_iso2'] = country_iso2
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def country_iso2(self) -> str:
        return self['country_iso2']

    @property
    def state(self) -> Optional[str]:
        return self['state']

    @property
    def city(self) -> Optional[str]:
        return self['city']

    @property
    def street(self) -> Optional[str]:
        return self['street']


class StarsRevenueStatus(dict):
    __slots__ = ()

    @overload
    def __init__(self, current_balance: aliases.AnyStarsAmount, available_balance: aliases.AnyStarsAmount, overall_revenue: aliases.AnyStarsAmount, withdrawal_enabled: Optional[bool] = ..., next_withdrawal_at: Optional[int] = ...): ...

    def __init__(self, current_balance, available_balance, overall_revenue, _='starsRevenueStatus', **kwargs):
        kwargs['current_balance'] = current_balance
        kwargs['available_balance'] = available_balance
        kwargs['overall_revenue'] = overall_revenue
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def withdrawal_enabled(self) -> Optional[bool]:
        return self['withdrawal_enabled']

    @property
    def current_balance(self) -> aliases.AnyStarsAmount:
        return build_object(self['current_balance'])

    @property
    def available_balance(self) -> aliases.AnyStarsAmount:
        return build_object(self['available_balance'])

    @property
    def overall_revenue(self) -> aliases.AnyStarsAmount:
        return build_object(self['overall_revenue'])

    @property
    def next_withdrawal_at(self) -> Optional[int]:
        return self['next_withdrawal_at']


class InputStarsTransaction(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, refund: Optional[bool] = ...): ...

    def __init__(self, id, _='inputStarsTransaction', **kwargs):
        kwargs['id'] = id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def refund(self) -> Optional[bool]:
        return self['refund']

    @property
    def id(self) -> str:
        return self['id']


class StarsGiftOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, currency: str, amount: int, extended: Optional[bool] = ..., store_product: Optional[str] = ...): ...

    def __init__(self, stars, currency, amount, _='starsGiftOption', **kwargs):
        kwargs['stars'] = stars
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def extended(self) -> Optional[bool]:
        return self['extended']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def store_product(self) -> Optional[str]:
        return self['store_product']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']


class BotPreviewMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, media: aliases.AnyMessageMedia): ...

    def __init__(self, date, media, _='botPreviewMedia', **kwargs):
        kwargs['date'] = date
        kwargs['media'] = media
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def media(self) -> aliases.AnyMessageMedia:
        return build_object(self['media'])


class StarsSubscriptionPricing(dict):
    __slots__ = ()

    @overload
    def __init__(self, period: int, amount: int): ...

    def __init__(self, period, amount, _='starsSubscriptionPricing', **kwargs):
        kwargs['period'] = period
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def period(self) -> int:
        return self['period']

    @property
    def amount(self) -> int:
        return self['amount']


class StarsSubscription(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, peer: aliases.AnyPeer, until_date: int, pricing: aliases.AnyStarsSubscriptionPricing, canceled: Optional[bool] = ..., can_refulfill: Optional[bool] = ..., missing_balance: Optional[bool] = ..., bot_canceled: Optional[bool] = ..., chat_invite_hash: Optional[str] = ..., title: Optional[str] = ..., photo: Optional[aliases.AnyWebDocument] = ..., invoice_slug: Optional[str] = ...): ...

    def __init__(self, id, peer, until_date, pricing, _='starsSubscription', **kwargs):
        kwargs['id'] = id
        kwargs['peer'] = peer
        kwargs['until_date'] = until_date
        kwargs['pricing'] = pricing
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def canceled(self) -> Optional[bool]:
        return self['canceled']

    @property
    def can_refulfill(self) -> Optional[bool]:
        return self['can_refulfill']

    @property
    def missing_balance(self) -> Optional[bool]:
        return self['missing_balance']

    @property
    def bot_canceled(self) -> Optional[bool]:
        return self['bot_canceled']

    @property
    def id(self) -> str:
        return self['id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def until_date(self) -> int:
        return self['until_date']

    @property
    def pricing(self) -> aliases.AnyStarsSubscriptionPricing:
        return build_object(self['pricing'])

    @property
    def chat_invite_hash(self) -> Optional[str]:
        return self['chat_invite_hash']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def photo(self) -> Optional[aliases.AnyWebDocument]:
        return build_object(self['photo'])

    @property
    def invoice_slug(self) -> Optional[str]:
        return self['invoice_slug']


class MessageReactor(dict):
    __slots__ = ()

    @overload
    def __init__(self, count: int, top: Optional[bool] = ..., my: Optional[bool] = ..., anonymous: Optional[bool] = ..., peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, count, _='messageReactor', **kwargs):
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def top(self) -> Optional[bool]:
        return self['top']

    @property
    def my(self) -> Optional[bool]:
        return self['my']

    @property
    def anonymous(self) -> Optional[bool]:
        return self['anonymous']

    @property
    def peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer_id'])

    @property
    def count(self) -> int:
        return self['count']


class StarsGiveawayOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, yearly_boosts: int, currency: str, amount: int, winners: list[aliases.AnyStarsGiveawayWinnersOption], extended: Optional[bool] = ..., default: Optional[bool] = ..., store_product: Optional[str] = ...): ...

    def __init__(self, stars, yearly_boosts, currency, amount, winners, _='starsGiveawayOption', **kwargs):
        kwargs['stars'] = stars
        kwargs['yearly_boosts'] = yearly_boosts
        kwargs['currency'] = currency
        kwargs['amount'] = amount
        kwargs['winners'] = winners
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def extended(self) -> Optional[bool]:
        return self['extended']

    @property
    def default(self) -> Optional[bool]:
        return self['default']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def yearly_boosts(self) -> int:
        return self['yearly_boosts']

    @property
    def store_product(self) -> Optional[str]:
        return self['store_product']

    @property
    def currency(self) -> str:
        return self['currency']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def winners(self) -> list[aliases.AnyStarsGiveawayWinnersOption]:
        return build_object(self['winners'])


class StarsGiveawayWinnersOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, users: int, per_user_stars: int, default: Optional[bool] = ...): ...

    def __init__(self, users, per_user_stars, _='starsGiveawayWinnersOption', **kwargs):
        kwargs['users'] = users
        kwargs['per_user_stars'] = per_user_stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def default(self) -> Optional[bool]:
        return self['default']

    @property
    def users(self) -> int:
        return self['users']

    @property
    def per_user_stars(self) -> int:
        return self['per_user_stars']


class StarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, sticker: aliases.AnyDocument, stars: int, convert_stars: int, limited: Optional[bool] = ..., sold_out: Optional[bool] = ..., birthday: Optional[bool] = ..., require_premium: Optional[bool] = ..., limited_per_user: Optional[bool] = ..., peer_color_available: Optional[bool] = ..., auction: Optional[bool] = ..., availability_remains: Optional[int] = ..., availability_total: Optional[int] = ..., availability_resale: Optional[int] = ..., first_sale_date: Optional[int] = ..., last_sale_date: Optional[int] = ..., upgrade_stars: Optional[int] = ..., resell_min_stars: Optional[int] = ..., title: Optional[str] = ..., released_by: Optional[aliases.AnyPeer] = ..., per_user_total: Optional[int] = ..., per_user_remains: Optional[int] = ..., locked_until_date: Optional[int] = ..., auction_slug: Optional[str] = ..., gifts_per_round: Optional[int] = ..., auction_start_date: Optional[int] = ..., upgrade_variants: Optional[int] = ..., background: Optional[aliases.AnyStarGiftBackground] = ...): ...

    def __init__(self, id, sticker, stars, convert_stars, _='starGift', **kwargs):
        kwargs['id'] = id
        kwargs['sticker'] = sticker
        kwargs['stars'] = stars
        kwargs['convert_stars'] = convert_stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def limited(self) -> Optional[bool]:
        return self['limited']

    @property
    def sold_out(self) -> Optional[bool]:
        return self['sold_out']

    @property
    def birthday(self) -> Optional[bool]:
        return self['birthday']

    @property
    def require_premium(self) -> Optional[bool]:
        return self['require_premium']

    @property
    def limited_per_user(self) -> Optional[bool]:
        return self['limited_per_user']

    @property
    def peer_color_available(self) -> Optional[bool]:
        return self['peer_color_available']

    @property
    def auction(self) -> Optional[bool]:
        return self['auction']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def sticker(self) -> aliases.AnyDocument:
        return build_object(self['sticker'])

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def availability_remains(self) -> Optional[int]:
        return self['availability_remains']

    @property
    def availability_total(self) -> Optional[int]:
        return self['availability_total']

    @property
    def availability_resale(self) -> Optional[int]:
        return self['availability_resale']

    @property
    def convert_stars(self) -> int:
        return self['convert_stars']

    @property
    def first_sale_date(self) -> Optional[int]:
        return self['first_sale_date']

    @property
    def last_sale_date(self) -> Optional[int]:
        return self['last_sale_date']

    @property
    def upgrade_stars(self) -> Optional[int]:
        return self['upgrade_stars']

    @property
    def resell_min_stars(self) -> Optional[int]:
        return self['resell_min_stars']

    @property
    def title(self) -> Optional[str]:
        return self['title']

    @property
    def released_by(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['released_by'])

    @property
    def per_user_total(self) -> Optional[int]:
        return self['per_user_total']

    @property
    def per_user_remains(self) -> Optional[int]:
        return self['per_user_remains']

    @property
    def locked_until_date(self) -> Optional[int]:
        return self['locked_until_date']

    @property
    def auction_slug(self) -> Optional[str]:
        return self['auction_slug']

    @property
    def gifts_per_round(self) -> Optional[int]:
        return self['gifts_per_round']

    @property
    def auction_start_date(self) -> Optional[int]:
        return self['auction_start_date']

    @property
    def upgrade_variants(self) -> Optional[int]:
        return self['upgrade_variants']

    @property
    def background(self) -> Optional[aliases.AnyStarGiftBackground]:
        return build_object(self['background'])


class StarGiftUnique(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, gift_id: int, title: str, slug: str, num: int, attributes: list[aliases.AnyStarGiftAttribute], availability_issued: int, availability_total: int, require_premium: Optional[bool] = ..., resale_ton_only: Optional[bool] = ..., theme_available: Optional[bool] = ..., burned: Optional[bool] = ..., crafted: Optional[bool] = ..., owner_id: Optional[aliases.AnyPeer] = ..., owner_name: Optional[str] = ..., owner_address: Optional[str] = ..., gift_address: Optional[str] = ..., resell_amount: Optional[list[aliases.AnyStarsAmount]] = ..., released_by: Optional[aliases.AnyPeer] = ..., value_amount: Optional[int] = ..., value_currency: Optional[str] = ..., value_usd_amount: Optional[int] = ..., theme_peer: Optional[aliases.AnyPeer] = ..., peer_color: Optional[aliases.AnyPeerColor] = ..., host_id: Optional[aliases.AnyPeer] = ..., offer_min_stars: Optional[int] = ..., craft_chance_permille: Optional[int] = ...): ...

    def __init__(self, id, gift_id, title, slug, num, attributes, availability_issued, availability_total, _='starGiftUnique', **kwargs):
        kwargs['id'] = id
        kwargs['gift_id'] = gift_id
        kwargs['title'] = title
        kwargs['slug'] = slug
        kwargs['num'] = num
        kwargs['attributes'] = attributes
        kwargs['availability_issued'] = availability_issued
        kwargs['availability_total'] = availability_total
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def require_premium(self) -> Optional[bool]:
        return self['require_premium']

    @property
    def resale_ton_only(self) -> Optional[bool]:
        return self['resale_ton_only']

    @property
    def theme_available(self) -> Optional[bool]:
        return self['theme_available']

    @property
    def burned(self) -> Optional[bool]:
        return self['burned']

    @property
    def crafted(self) -> Optional[bool]:
        return self['crafted']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def gift_id(self) -> int:
        return self['gift_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def slug(self) -> str:
        return self['slug']

    @property
    def num(self) -> int:
        return self['num']

    @property
    def owner_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['owner_id'])

    @property
    def owner_name(self) -> Optional[str]:
        return self['owner_name']

    @property
    def owner_address(self) -> Optional[str]:
        return self['owner_address']

    @property
    def attributes(self) -> list[aliases.AnyStarGiftAttribute]:
        return build_object(self['attributes'])

    @property
    def availability_issued(self) -> int:
        return self['availability_issued']

    @property
    def availability_total(self) -> int:
        return self['availability_total']

    @property
    def gift_address(self) -> Optional[str]:
        return self['gift_address']

    @property
    def resell_amount(self) -> Optional[list[aliases.AnyStarsAmount]]:
        return build_object(self['resell_amount'])

    @property
    def released_by(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['released_by'])

    @property
    def value_amount(self) -> Optional[int]:
        return self['value_amount']

    @property
    def value_currency(self) -> Optional[str]:
        return self['value_currency']

    @property
    def value_usd_amount(self) -> Optional[int]:
        return self['value_usd_amount']

    @property
    def theme_peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['theme_peer'])

    @property
    def peer_color(self) -> Optional[aliases.AnyPeerColor]:
        return build_object(self['peer_color'])

    @property
    def host_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['host_id'])

    @property
    def offer_min_stars(self) -> Optional[int]:
        return self['offer_min_stars']

    @property
    def craft_chance_permille(self) -> Optional[int]:
        return self['craft_chance_permille']


class MessageReportOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, text: str, option: bytes): ...

    def __init__(self, text, option, _='messageReportOption', **kwargs):
        kwargs['text'] = text
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def text(self) -> str:
        return self['text']

    @property
    def option(self) -> bytes:
        return self['option']


class ReportResultChooseOption(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: str, options: list[aliases.AnyMessageReportOption]): ...

    def __init__(self, title, options, _='reportResultChooseOption', **kwargs):
        kwargs['title'] = title
        kwargs['options'] = options
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def title(self) -> str:
        return self['title']

    @property
    def options(self) -> list[aliases.AnyMessageReportOption]:
        return build_object(self['options'])


class ReportResultAddComment(dict):
    __slots__ = ()

    @overload
    def __init__(self, option: bytes, optional: Optional[bool] = ...): ...

    def __init__(self, option, _='reportResultAddComment', **kwargs):
        kwargs['option'] = option
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def optional(self) -> Optional[bool]:
        return self['optional']

    @property
    def option(self) -> bytes:
        return self['option']


class ReportResultReported(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='reportResultReported'):
        dict.__init__(self, _=_)


class BotAppSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, placeholder_path: Optional[bytes] = ..., background_color: Optional[int] = ..., background_dark_color: Optional[int] = ..., header_color: Optional[int] = ..., header_dark_color: Optional[int] = ...): ...

    def __init__(self, _='botAppSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def placeholder_path(self) -> Optional[bytes]:
        return self['placeholder_path']

    @property
    def background_color(self) -> Optional[int]:
        return self['background_color']

    @property
    def background_dark_color(self) -> Optional[int]:
        return self['background_dark_color']

    @property
    def header_color(self) -> Optional[int]:
        return self['header_color']

    @property
    def header_dark_color(self) -> Optional[int]:
        return self['header_dark_color']


class StarRefProgram(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, commission_permille: int, duration_months: Optional[int] = ..., end_date: Optional[int] = ..., daily_revenue_per_user: Optional[aliases.AnyStarsAmount] = ...): ...

    def __init__(self, bot_id, commission_permille, _='starRefProgram', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['commission_permille'] = commission_permille
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def commission_permille(self) -> int:
        return self['commission_permille']

    @property
    def duration_months(self) -> Optional[int]:
        return self['duration_months']

    @property
    def end_date(self) -> Optional[int]:
        return self['end_date']

    @property
    def daily_revenue_per_user(self) -> Optional[aliases.AnyStarsAmount]:
        return build_object(self['daily_revenue_per_user'])


class ConnectedBotStarRef(dict):
    __slots__ = ()

    @overload
    def __init__(self, url: str, date: int, bot_id: int, commission_permille: int, participants: int, revenue: int, revoked: Optional[bool] = ..., duration_months: Optional[int] = ...): ...

    def __init__(self, url, date, bot_id, commission_permille, participants, revenue, _='connectedBotStarRef', **kwargs):
        kwargs['url'] = url
        kwargs['date'] = date
        kwargs['bot_id'] = bot_id
        kwargs['commission_permille'] = commission_permille
        kwargs['participants'] = participants
        kwargs['revenue'] = revenue
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def revoked(self) -> Optional[bool]:
        return self['revoked']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def commission_permille(self) -> int:
        return self['commission_permille']

    @property
    def duration_months(self) -> Optional[int]:
        return self['duration_months']

    @property
    def participants(self) -> int:
        return self['participants']

    @property
    def revenue(self) -> int:
        return self['revenue']


class StarsAmount(dict):
    __slots__ = ()

    @overload
    def __init__(self, amount: int, nanos: int): ...

    def __init__(self, amount, nanos, _='starsAmount', **kwargs):
        kwargs['amount'] = amount
        kwargs['nanos'] = nanos
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def nanos(self) -> int:
        return self['nanos']


class StarsTonAmount(dict):
    __slots__ = ()

    @overload
    def __init__(self, amount: int): ...

    def __init__(self, amount, _='starsTonAmount', **kwargs):
        kwargs['amount'] = amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def amount(self) -> int:
        return self['amount']


class BotVerifierSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, icon: int, company: str, can_modify_custom_description: Optional[bool] = ..., custom_description: Optional[str] = ...): ...

    def __init__(self, icon, company, _='botVerifierSettings', **kwargs):
        kwargs['icon'] = icon
        kwargs['company'] = company
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def can_modify_custom_description(self) -> Optional[bool]:
        return self['can_modify_custom_description']

    @property
    def icon(self) -> int:
        return self['icon']

    @property
    def company(self) -> str:
        return self['company']

    @property
    def custom_description(self) -> Optional[str]:
        return self['custom_description']


class BotVerification(dict):
    __slots__ = ()

    @overload
    def __init__(self, bot_id: int, icon: int, description: str): ...

    def __init__(self, bot_id, icon, description, _='botVerification', **kwargs):
        kwargs['bot_id'] = bot_id
        kwargs['icon'] = icon
        kwargs['description'] = description
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bot_id(self) -> int:
        return self['bot_id']

    @property
    def icon(self) -> int:
        return self['icon']

    @property
    def description(self) -> str:
        return self['description']


class StarGiftAttributeModel(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, document: aliases.AnyDocument, rarity: aliases.AnyStarGiftAttributeRarity, crafted: Optional[bool] = ...): ...

    def __init__(self, name, document, rarity, _='starGiftAttributeModel', **kwargs):
        kwargs['name'] = name
        kwargs['document'] = document
        kwargs['rarity'] = rarity
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def crafted(self) -> Optional[bool]:
        return self['crafted']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def document(self) -> aliases.AnyDocument:
        return build_object(self['document'])

    @property
    def rarity(self) -> aliases.AnyStarGiftAttributeRarity:
        return build_object(self['rarity'])


class StarGiftAttributePattern(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, document: aliases.AnyDocument, rarity: aliases.AnyStarGiftAttributeRarity): ...

    def __init__(self, name, document, rarity, _='starGiftAttributePattern', **kwargs):
        kwargs['name'] = name
        kwargs['document'] = document
        kwargs['rarity'] = rarity
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']

    @property
    def document(self) -> aliases.AnyDocument:
        return build_object(self['document'])

    @property
    def rarity(self) -> aliases.AnyStarGiftAttributeRarity:
        return build_object(self['rarity'])


class StarGiftAttributeBackdrop(dict):
    __slots__ = ()

    @overload
    def __init__(self, name: str, backdrop_id: int, center_color: int, edge_color: int, pattern_color: int, text_color: int, rarity: aliases.AnyStarGiftAttributeRarity): ...

    def __init__(self, name, backdrop_id, center_color, edge_color, pattern_color, text_color, rarity, _='starGiftAttributeBackdrop', **kwargs):
        kwargs['name'] = name
        kwargs['backdrop_id'] = backdrop_id
        kwargs['center_color'] = center_color
        kwargs['edge_color'] = edge_color
        kwargs['pattern_color'] = pattern_color
        kwargs['text_color'] = text_color
        kwargs['rarity'] = rarity
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name(self) -> str:
        return self['name']

    @property
    def backdrop_id(self) -> int:
        return self['backdrop_id']

    @property
    def center_color(self) -> int:
        return self['center_color']

    @property
    def edge_color(self) -> int:
        return self['edge_color']

    @property
    def pattern_color(self) -> int:
        return self['pattern_color']

    @property
    def text_color(self) -> int:
        return self['text_color']

    @property
    def rarity(self) -> aliases.AnyStarGiftAttributeRarity:
        return build_object(self['rarity'])


class StarGiftAttributeOriginalDetails(dict):
    __slots__ = ()

    @overload
    def __init__(self, recipient_id: aliases.AnyPeer, date: int, sender_id: Optional[aliases.AnyPeer] = ..., message: Optional[aliases.AnyTextWithEntities] = ...): ...

    def __init__(self, recipient_id, date, _='starGiftAttributeOriginalDetails', **kwargs):
        kwargs['recipient_id'] = recipient_id
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def sender_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['sender_id'])

    @property
    def recipient_id(self) -> aliases.AnyPeer:
        return build_object(self['recipient_id'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])


class SavedStarGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, gift: aliases.AnyStarGift, name_hidden: Optional[bool] = ..., unsaved: Optional[bool] = ..., refunded: Optional[bool] = ..., can_upgrade: Optional[bool] = ..., pinned_to_top: Optional[bool] = ..., upgrade_separate: Optional[bool] = ..., from_id: Optional[aliases.AnyPeer] = ..., message: Optional[aliases.AnyTextWithEntities] = ..., msg_id: Optional[int] = ..., saved_id: Optional[int] = ..., convert_stars: Optional[int] = ..., upgrade_stars: Optional[int] = ..., can_export_at: Optional[int] = ..., transfer_stars: Optional[int] = ..., can_transfer_at: Optional[int] = ..., can_resell_at: Optional[int] = ..., collection_id: Optional[list[int]] = ..., prepaid_upgrade_hash: Optional[str] = ..., drop_original_details_stars: Optional[int] = ..., gift_num: Optional[int] = ..., can_craft_at: Optional[int] = ...): ...

    def __init__(self, date, gift, _='savedStarGift', **kwargs):
        kwargs['date'] = date
        kwargs['gift'] = gift
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name_hidden(self) -> Optional[bool]:
        return self['name_hidden']

    @property
    def unsaved(self) -> Optional[bool]:
        return self['unsaved']

    @property
    def refunded(self) -> Optional[bool]:
        return self['refunded']

    @property
    def can_upgrade(self) -> Optional[bool]:
        return self['can_upgrade']

    @property
    def pinned_to_top(self) -> Optional[bool]:
        return self['pinned_to_top']

    @property
    def upgrade_separate(self) -> Optional[bool]:
        return self['upgrade_separate']

    @property
    def from_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['from_id'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])

    @property
    def msg_id(self) -> Optional[int]:
        return self['msg_id']

    @property
    def saved_id(self) -> Optional[int]:
        return self['saved_id']

    @property
    def convert_stars(self) -> Optional[int]:
        return self['convert_stars']

    @property
    def upgrade_stars(self) -> Optional[int]:
        return self['upgrade_stars']

    @property
    def can_export_at(self) -> Optional[int]:
        return self['can_export_at']

    @property
    def transfer_stars(self) -> Optional[int]:
        return self['transfer_stars']

    @property
    def can_transfer_at(self) -> Optional[int]:
        return self['can_transfer_at']

    @property
    def can_resell_at(self) -> Optional[int]:
        return self['can_resell_at']

    @property
    def collection_id(self) -> Optional[list[int]]:
        return self['collection_id']

    @property
    def prepaid_upgrade_hash(self) -> Optional[str]:
        return self['prepaid_upgrade_hash']

    @property
    def drop_original_details_stars(self) -> Optional[int]:
        return self['drop_original_details_stars']

    @property
    def gift_num(self) -> Optional[int]:
        return self['gift_num']

    @property
    def can_craft_at(self) -> Optional[int]:
        return self['can_craft_at']


class InputSavedStarGiftUser(dict):
    __slots__ = ()

    @overload
    def __init__(self, msg_id: int): ...

    def __init__(self, msg_id, _='inputSavedStarGiftUser', **kwargs):
        kwargs['msg_id'] = msg_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def msg_id(self) -> int:
        return self['msg_id']


class InputSavedStarGiftChat(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer, saved_id: int): ...

    def __init__(self, peer, saved_id, _='inputSavedStarGiftChat', **kwargs):
        kwargs['peer'] = peer
        kwargs['saved_id'] = saved_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])

    @property
    def saved_id(self) -> int:
        return self['saved_id']


class InputSavedStarGiftSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputSavedStarGiftSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class PaidReactionPrivacyDefault(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='paidReactionPrivacyDefault'):
        dict.__init__(self, _=_)


class PaidReactionPrivacyAnonymous(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='paidReactionPrivacyAnonymous'):
        dict.__init__(self, _=_)


class PaidReactionPrivacyPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyInputPeer): ...

    def __init__(self, peer, _='paidReactionPrivacyPeer', **kwargs):
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def peer(self) -> aliases.AnyInputPeer:
        return build_object(self['peer'])


class RequirementToContactEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='requirementToContactEmpty'):
        dict.__init__(self, _=_)


class RequirementToContactPremium(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='requirementToContactPremium'):
        dict.__init__(self, _=_)


class RequirementToContactPaidMessages(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars_amount: int): ...

    def __init__(self, stars_amount, _='requirementToContactPaidMessages', **kwargs):
        kwargs['stars_amount'] = stars_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def stars_amount(self) -> int:
        return self['stars_amount']


class BusinessBotRights(dict):
    __slots__ = ()

    @overload
    def __init__(self, reply: Optional[bool] = ..., read_messages: Optional[bool] = ..., delete_sent_messages: Optional[bool] = ..., delete_received_messages: Optional[bool] = ..., edit_name: Optional[bool] = ..., edit_bio: Optional[bool] = ..., edit_profile_photo: Optional[bool] = ..., edit_username: Optional[bool] = ..., view_gifts: Optional[bool] = ..., sell_gifts: Optional[bool] = ..., change_gift_settings: Optional[bool] = ..., transfer_and_upgrade_gifts: Optional[bool] = ..., transfer_stars: Optional[bool] = ..., manage_stories: Optional[bool] = ...): ...

    def __init__(self, _='businessBotRights', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def reply(self) -> Optional[bool]:
        return self['reply']

    @property
    def read_messages(self) -> Optional[bool]:
        return self['read_messages']

    @property
    def delete_sent_messages(self) -> Optional[bool]:
        return self['delete_sent_messages']

    @property
    def delete_received_messages(self) -> Optional[bool]:
        return self['delete_received_messages']

    @property
    def edit_name(self) -> Optional[bool]:
        return self['edit_name']

    @property
    def edit_bio(self) -> Optional[bool]:
        return self['edit_bio']

    @property
    def edit_profile_photo(self) -> Optional[bool]:
        return self['edit_profile_photo']

    @property
    def edit_username(self) -> Optional[bool]:
        return self['edit_username']

    @property
    def view_gifts(self) -> Optional[bool]:
        return self['view_gifts']

    @property
    def sell_gifts(self) -> Optional[bool]:
        return self['sell_gifts']

    @property
    def change_gift_settings(self) -> Optional[bool]:
        return self['change_gift_settings']

    @property
    def transfer_and_upgrade_gifts(self) -> Optional[bool]:
        return self['transfer_and_upgrade_gifts']

    @property
    def transfer_stars(self) -> Optional[bool]:
        return self['transfer_stars']

    @property
    def manage_stories(self) -> Optional[bool]:
        return self['manage_stories']


class DisallowedGiftsSettings(dict):
    __slots__ = ()

    @overload
    def __init__(self, disallow_unlimited_stargifts: Optional[bool] = ..., disallow_limited_stargifts: Optional[bool] = ..., disallow_unique_stargifts: Optional[bool] = ..., disallow_premium_gifts: Optional[bool] = ..., disallow_stargifts_from_channels: Optional[bool] = ...): ...

    def __init__(self, _='disallowedGiftsSettings', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def disallow_unlimited_stargifts(self) -> Optional[bool]:
        return self['disallow_unlimited_stargifts']

    @property
    def disallow_limited_stargifts(self) -> Optional[bool]:
        return self['disallow_limited_stargifts']

    @property
    def disallow_unique_stargifts(self) -> Optional[bool]:
        return self['disallow_unique_stargifts']

    @property
    def disallow_premium_gifts(self) -> Optional[bool]:
        return self['disallow_premium_gifts']

    @property
    def disallow_stargifts_from_channels(self) -> Optional[bool]:
        return self['disallow_stargifts_from_channels']


class SponsoredPeer(dict):
    __slots__ = ()

    @overload
    def __init__(self, random_id: bytes, peer: aliases.AnyPeer, sponsor_info: Optional[str] = ..., additional_info: Optional[str] = ...): ...

    def __init__(self, random_id, peer, _='sponsoredPeer', **kwargs):
        kwargs['random_id'] = random_id
        kwargs['peer'] = peer
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def random_id(self) -> bytes:
        return self['random_id']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def sponsor_info(self) -> Optional[str]:
        return self['sponsor_info']

    @property
    def additional_info(self) -> Optional[str]:
        return self['additional_info']


class StarGiftAttributeIdModel(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int): ...

    def __init__(self, document_id, _='starGiftAttributeIdModel', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']


class StarGiftAttributeIdPattern(dict):
    __slots__ = ()

    @overload
    def __init__(self, document_id: int): ...

    def __init__(self, document_id, _='starGiftAttributeIdPattern', **kwargs):
        kwargs['document_id'] = document_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def document_id(self) -> int:
        return self['document_id']


class StarGiftAttributeIdBackdrop(dict):
    __slots__ = ()

    @overload
    def __init__(self, backdrop_id: int): ...

    def __init__(self, backdrop_id, _='starGiftAttributeIdBackdrop', **kwargs):
        kwargs['backdrop_id'] = backdrop_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def backdrop_id(self) -> int:
        return self['backdrop_id']


class StarGiftAttributeCounter(dict):
    __slots__ = ()

    @overload
    def __init__(self, attribute: aliases.AnyStarGiftAttributeId, count: int): ...

    def __init__(self, attribute, count, _='starGiftAttributeCounter', **kwargs):
        kwargs['attribute'] = attribute
        kwargs['count'] = count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def attribute(self) -> aliases.AnyStarGiftAttributeId:
        return build_object(self['attribute'])

    @property
    def count(self) -> int:
        return self['count']


class PendingSuggestion(dict):
    __slots__ = ()

    @overload
    def __init__(self, suggestion: str, title: aliases.AnyTextWithEntities, description: aliases.AnyTextWithEntities, url: str): ...

    def __init__(self, suggestion, title, description, url, _='pendingSuggestion', **kwargs):
        kwargs['suggestion'] = suggestion
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['url'] = url
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def suggestion(self) -> str:
        return self['suggestion']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])

    @property
    def description(self) -> aliases.AnyTextWithEntities:
        return build_object(self['description'])

    @property
    def url(self) -> str:
        return self['url']


class TodoItem(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, title: aliases.AnyTextWithEntities): ...

    def __init__(self, id, title, _='todoItem', **kwargs):
        kwargs['id'] = id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])


class TodoList(dict):
    __slots__ = ()

    @overload
    def __init__(self, title: aliases.AnyTextWithEntities, list: list[aliases.AnyTodoItem], others_can_append: Optional[bool] = ..., others_can_complete: Optional[bool] = ...): ...

    def __init__(self, title, list, _='todoList', **kwargs):
        kwargs['title'] = title
        kwargs['list'] = list
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def others_can_append(self) -> Optional[bool]:
        return self['others_can_append']

    @property
    def others_can_complete(self) -> Optional[bool]:
        return self['others_can_complete']

    @property
    def title(self) -> aliases.AnyTextWithEntities:
        return build_object(self['title'])

    @property
    def list(self) -> list[aliases.AnyTodoItem]:
        return build_object(self['list'])


class TodoCompletion(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, completed_by: aliases.AnyPeer, date: int): ...

    def __init__(self, id, completed_by, date, _='todoCompletion', **kwargs):
        kwargs['id'] = id
        kwargs['completed_by'] = completed_by
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> int:
        return self['id']

    @property
    def completed_by(self) -> aliases.AnyPeer:
        return build_object(self['completed_by'])

    @property
    def date(self) -> int:
        return self['date']


class SuggestedPost(dict):
    __slots__ = ()

    @overload
    def __init__(self, accepted: Optional[bool] = ..., rejected: Optional[bool] = ..., price: Optional[aliases.AnyStarsAmount] = ..., schedule_date: Optional[int] = ...): ...

    def __init__(self, _='suggestedPost', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def accepted(self) -> Optional[bool]:
        return self['accepted']

    @property
    def rejected(self) -> Optional[bool]:
        return self['rejected']

    @property
    def price(self) -> Optional[aliases.AnyStarsAmount]:
        return build_object(self['price'])

    @property
    def schedule_date(self) -> Optional[int]:
        return self['schedule_date']


class StarsRating(dict):
    __slots__ = ()

    @overload
    def __init__(self, level: int, current_level_stars: int, stars: int, next_level_stars: Optional[int] = ...): ...

    def __init__(self, level, current_level_stars, stars, _='starsRating', **kwargs):
        kwargs['level'] = level
        kwargs['current_level_stars'] = current_level_stars
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def level(self) -> int:
        return self['level']

    @property
    def current_level_stars(self) -> int:
        return self['current_level_stars']

    @property
    def stars(self) -> int:
        return self['stars']

    @property
    def next_level_stars(self) -> Optional[int]:
        return self['next_level_stars']


class StarGiftCollection(dict):
    __slots__ = ()

    @overload
    def __init__(self, collection_id: int, title: str, gifts_count: int, hash: int, icon: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, collection_id, title, gifts_count, hash, _='starGiftCollection', **kwargs):
        kwargs['collection_id'] = collection_id
        kwargs['title'] = title
        kwargs['gifts_count'] = gifts_count
        kwargs['hash'] = hash
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def collection_id(self) -> int:
        return self['collection_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['icon'])

    @property
    def gifts_count(self) -> int:
        return self['gifts_count']

    @property
    def hash(self) -> int:
        return self['hash']


class StoryAlbum(dict):
    __slots__ = ()

    @overload
    def __init__(self, album_id: int, title: str, icon_photo: Optional[aliases.AnyPhoto] = ..., icon_video: Optional[aliases.AnyDocument] = ...): ...

    def __init__(self, album_id, title, _='storyAlbum', **kwargs):
        kwargs['album_id'] = album_id
        kwargs['title'] = title
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def album_id(self) -> int:
        return self['album_id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def icon_photo(self) -> Optional[aliases.AnyPhoto]:
        return build_object(self['icon_photo'])

    @property
    def icon_video(self) -> Optional[aliases.AnyDocument]:
        return build_object(self['icon_video'])


class SearchPostsFlood(dict):
    __slots__ = ()

    @overload
    def __init__(self, total_daily: int, remains: int, stars_amount: int, query_is_free: Optional[bool] = ..., wait_till: Optional[int] = ...): ...

    def __init__(self, total_daily, remains, stars_amount, _='searchPostsFlood', **kwargs):
        kwargs['total_daily'] = total_daily
        kwargs['remains'] = remains
        kwargs['stars_amount'] = stars_amount
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def query_is_free(self) -> Optional[bool]:
        return self['query_is_free']

    @property
    def total_daily(self) -> int:
        return self['total_daily']

    @property
    def remains(self) -> int:
        return self['remains']

    @property
    def wait_till(self) -> Optional[int]:
        return self['wait_till']

    @property
    def stars_amount(self) -> int:
        return self['stars_amount']


class ProfileTabPosts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabPosts'):
        dict.__init__(self, _=_)


class ProfileTabGifts(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabGifts'):
        dict.__init__(self, _=_)


class ProfileTabMedia(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabMedia'):
        dict.__init__(self, _=_)


class ProfileTabFiles(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabFiles'):
        dict.__init__(self, _=_)


class ProfileTabMusic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabMusic'):
        dict.__init__(self, _=_)


class ProfileTabVoice(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabVoice'):
        dict.__init__(self, _=_)


class ProfileTabLinks(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabLinks'):
        dict.__init__(self, _=_)


class ProfileTabGifs(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='profileTabGifs'):
        dict.__init__(self, _=_)


class InputChatThemeEmpty(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='inputChatThemeEmpty'):
        dict.__init__(self, _=_)


class InputChatTheme(dict):
    __slots__ = ()

    @overload
    def __init__(self, emoticon: str): ...

    def __init__(self, emoticon, _='inputChatTheme', **kwargs):
        kwargs['emoticon'] = emoticon
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def emoticon(self) -> str:
        return self['emoticon']


class InputChatThemeUniqueGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputChatThemeUniqueGift', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class StarGiftUpgradePrice(dict):
    __slots__ = ()

    @overload
    def __init__(self, date: int, upgrade_stars: int): ...

    def __init__(self, date, upgrade_stars, _='starGiftUpgradePrice', **kwargs):
        kwargs['date'] = date
        kwargs['upgrade_stars'] = upgrade_stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def date(self) -> int:
        return self['date']

    @property
    def upgrade_stars(self) -> int:
        return self['upgrade_stars']


class GroupCallMessage(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: int, from_id: aliases.AnyPeer, date: int, message: aliases.AnyTextWithEntities, from_admin: Optional[bool] = ..., paid_message_stars: Optional[int] = ...): ...

    def __init__(self, id, from_id, date, message, _='groupCallMessage', **kwargs):
        kwargs['id'] = id
        kwargs['from_id'] = from_id
        kwargs['date'] = date
        kwargs['message'] = message
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def from_admin(self) -> Optional[bool]:
        return self['from_admin']

    @property
    def id(self) -> int:
        return self['id']

    @property
    def from_id(self) -> aliases.AnyPeer:
        return build_object(self['from_id'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def message(self) -> aliases.AnyTextWithEntities:
        return build_object(self['message'])

    @property
    def paid_message_stars(self) -> Optional[int]:
        return self['paid_message_stars']


class GroupCallDonor(dict):
    __slots__ = ()

    @overload
    def __init__(self, stars: int, top: Optional[bool] = ..., my: Optional[bool] = ..., peer_id: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, stars, _='groupCallDonor', **kwargs):
        kwargs['stars'] = stars
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def top(self) -> Optional[bool]:
        return self['top']

    @property
    def my(self) -> Optional[bool]:
        return self['my']

    @property
    def peer_id(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['peer_id'])

    @property
    def stars(self) -> int:
        return self['stars']


class RecentStory(dict):
    __slots__ = ()

    @overload
    def __init__(self, live: Optional[bool] = ..., max_id: Optional[int] = ...): ...

    def __init__(self, _='recentStory', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def live(self) -> Optional[bool]:
        return self['live']

    @property
    def max_id(self) -> Optional[int]:
        return self['max_id']


class AuctionBidLevel(dict):
    __slots__ = ()

    @overload
    def __init__(self, pos: int, amount: int, date: int): ...

    def __init__(self, pos, amount, date, _='auctionBidLevel', **kwargs):
        kwargs['pos'] = pos
        kwargs['amount'] = amount
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pos(self) -> int:
        return self['pos']

    @property
    def amount(self) -> int:
        return self['amount']

    @property
    def date(self) -> int:
        return self['date']


class StarGiftAuctionStateNotModified(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starGiftAuctionStateNotModified'):
        dict.__init__(self, _=_)


class StarGiftAuctionState(dict):
    __slots__ = ()

    @overload
    def __init__(self, version: int, start_date: int, end_date: int, min_bid_amount: int, bid_levels: list[aliases.AnyAuctionBidLevel], top_bidders: list[int], next_round_at: int, last_gift_num: int, gifts_left: int, current_round: int, total_rounds: int, rounds: list[aliases.AnyStarGiftAuctionRound]): ...

    def __init__(self, version, start_date, end_date, min_bid_amount, bid_levels, top_bidders, next_round_at, last_gift_num, gifts_left, current_round, total_rounds, rounds, _='starGiftAuctionState', **kwargs):
        kwargs['version'] = version
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        kwargs['min_bid_amount'] = min_bid_amount
        kwargs['bid_levels'] = bid_levels
        kwargs['top_bidders'] = top_bidders
        kwargs['next_round_at'] = next_round_at
        kwargs['last_gift_num'] = last_gift_num
        kwargs['gifts_left'] = gifts_left
        kwargs['current_round'] = current_round
        kwargs['total_rounds'] = total_rounds
        kwargs['rounds'] = rounds
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def version(self) -> int:
        return self['version']

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def end_date(self) -> int:
        return self['end_date']

    @property
    def min_bid_amount(self) -> int:
        return self['min_bid_amount']

    @property
    def bid_levels(self) -> list[aliases.AnyAuctionBidLevel]:
        return build_object(self['bid_levels'])

    @property
    def top_bidders(self) -> list[int]:
        return self['top_bidders']

    @property
    def next_round_at(self) -> int:
        return self['next_round_at']

    @property
    def last_gift_num(self) -> int:
        return self['last_gift_num']

    @property
    def gifts_left(self) -> int:
        return self['gifts_left']

    @property
    def current_round(self) -> int:
        return self['current_round']

    @property
    def total_rounds(self) -> int:
        return self['total_rounds']

    @property
    def rounds(self) -> list[aliases.AnyStarGiftAuctionRound]:
        return build_object(self['rounds'])


class StarGiftAuctionStateFinished(dict):
    __slots__ = ()

    @overload
    def __init__(self, start_date: int, end_date: int, average_price: int, listed_count: Optional[int] = ..., fragment_listed_count: Optional[int] = ..., fragment_listed_url: Optional[str] = ...): ...

    def __init__(self, start_date, end_date, average_price, _='starGiftAuctionStateFinished', **kwargs):
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        kwargs['average_price'] = average_price
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def start_date(self) -> int:
        return self['start_date']

    @property
    def end_date(self) -> int:
        return self['end_date']

    @property
    def average_price(self) -> int:
        return self['average_price']

    @property
    def listed_count(self) -> Optional[int]:
        return self['listed_count']

    @property
    def fragment_listed_count(self) -> Optional[int]:
        return self['fragment_listed_count']

    @property
    def fragment_listed_url(self) -> Optional[str]:
        return self['fragment_listed_url']


class StarGiftAuctionUserState(dict):
    __slots__ = ()

    @overload
    def __init__(self, acquired_count: int, returned: Optional[bool] = ..., bid_amount: Optional[int] = ..., bid_date: Optional[int] = ..., min_bid_amount: Optional[int] = ..., bid_peer: Optional[aliases.AnyPeer] = ...): ...

    def __init__(self, acquired_count, _='starGiftAuctionUserState', **kwargs):
        kwargs['acquired_count'] = acquired_count
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def returned(self) -> Optional[bool]:
        return self['returned']

    @property
    def bid_amount(self) -> Optional[int]:
        return self['bid_amount']

    @property
    def bid_date(self) -> Optional[int]:
        return self['bid_date']

    @property
    def min_bid_amount(self) -> Optional[int]:
        return self['min_bid_amount']

    @property
    def bid_peer(self) -> Optional[aliases.AnyPeer]:
        return build_object(self['bid_peer'])

    @property
    def acquired_count(self) -> int:
        return self['acquired_count']


class StarGiftAuctionAcquiredGift(dict):
    __slots__ = ()

    @overload
    def __init__(self, peer: aliases.AnyPeer, date: int, bid_amount: int, round: int, pos: int, name_hidden: Optional[bool] = ..., message: Optional[aliases.AnyTextWithEntities] = ..., gift_num: Optional[int] = ...): ...

    def __init__(self, peer, date, bid_amount, round, pos, _='starGiftAuctionAcquiredGift', **kwargs):
        kwargs['peer'] = peer
        kwargs['date'] = date
        kwargs['bid_amount'] = bid_amount
        kwargs['round'] = round
        kwargs['pos'] = pos
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def name_hidden(self) -> Optional[bool]:
        return self['name_hidden']

    @property
    def peer(self) -> aliases.AnyPeer:
        return build_object(self['peer'])

    @property
    def date(self) -> int:
        return self['date']

    @property
    def bid_amount(self) -> int:
        return self['bid_amount']

    @property
    def round(self) -> int:
        return self['round']

    @property
    def pos(self) -> int:
        return self['pos']

    @property
    def message(self) -> Optional[aliases.AnyTextWithEntities]:
        return build_object(self['message'])

    @property
    def gift_num(self) -> Optional[int]:
        return self['gift_num']


class StarGiftActiveAuctionState(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift: aliases.AnyStarGift, state: aliases.AnyStarGiftAuctionState, user_state: aliases.AnyStarGiftAuctionUserState): ...

    def __init__(self, gift, state, user_state, _='starGiftActiveAuctionState', **kwargs):
        kwargs['gift'] = gift
        kwargs['state'] = state
        kwargs['user_state'] = user_state
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift(self) -> aliases.AnyStarGift:
        return build_object(self['gift'])

    @property
    def state(self) -> aliases.AnyStarGiftAuctionState:
        return build_object(self['state'])

    @property
    def user_state(self) -> aliases.AnyStarGiftAuctionUserState:
        return build_object(self['user_state'])


class InputStarGiftAuction(dict):
    __slots__ = ()

    @overload
    def __init__(self, gift_id: int): ...

    def __init__(self, gift_id, _='inputStarGiftAuction', **kwargs):
        kwargs['gift_id'] = gift_id
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def gift_id(self) -> int:
        return self['gift_id']


class InputStarGiftAuctionSlug(dict):
    __slots__ = ()

    @overload
    def __init__(self, slug: str): ...

    def __init__(self, slug, _='inputStarGiftAuctionSlug', **kwargs):
        kwargs['slug'] = slug
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def slug(self) -> str:
        return self['slug']


class Passkey(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, name: str, date: int, software_emoji_id: Optional[int] = ..., last_usage_date: Optional[int] = ...): ...

    def __init__(self, id, name, date, _='passkey', **kwargs):
        kwargs['id'] = id
        kwargs['name'] = name
        kwargs['date'] = date
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def software_emoji_id(self) -> Optional[int]:
        return self['software_emoji_id']

    @property
    def last_usage_date(self) -> Optional[int]:
        return self['last_usage_date']


class InputPasskeyResponseRegister(dict):
    __slots__ = ()

    @overload
    def __init__(self, client_data: aliases.AnyDataJSON, attestation_data: bytes): ...

    def __init__(self, client_data, attestation_data, _='inputPasskeyResponseRegister', **kwargs):
        kwargs['client_data'] = client_data
        kwargs['attestation_data'] = attestation_data
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def client_data(self) -> aliases.AnyDataJSON:
        return build_object(self['client_data'])

    @property
    def attestation_data(self) -> bytes:
        return self['attestation_data']


class InputPasskeyResponseLogin(dict):
    __slots__ = ()

    @overload
    def __init__(self, client_data: aliases.AnyDataJSON, authenticator_data: bytes, signature: bytes, user_handle: str): ...

    def __init__(self, client_data, authenticator_data, signature, user_handle, _='inputPasskeyResponseLogin', **kwargs):
        kwargs['client_data'] = client_data
        kwargs['authenticator_data'] = authenticator_data
        kwargs['signature'] = signature
        kwargs['user_handle'] = user_handle
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def client_data(self) -> aliases.AnyDataJSON:
        return build_object(self['client_data'])

    @property
    def authenticator_data(self) -> bytes:
        return self['authenticator_data']

    @property
    def signature(self) -> bytes:
        return self['signature']

    @property
    def user_handle(self) -> str:
        return self['user_handle']


class InputPasskeyCredentialPublicKey(dict):
    __slots__ = ()

    @overload
    def __init__(self, id: str, raw_id: str, response: aliases.AnyInputPasskeyResponse): ...

    def __init__(self, id, raw_id, response, _='inputPasskeyCredentialPublicKey', **kwargs):
        kwargs['id'] = id
        kwargs['raw_id'] = raw_id
        kwargs['response'] = response
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def raw_id(self) -> str:
        return self['raw_id']

    @property
    def response(self) -> aliases.AnyInputPasskeyResponse:
        return build_object(self['response'])


class InputPasskeyCredentialFirebasePNV(dict):
    __slots__ = ()

    @overload
    def __init__(self, pnv_token: str): ...

    def __init__(self, pnv_token, _='inputPasskeyCredentialFirebasePNV', **kwargs):
        kwargs['pnv_token'] = pnv_token
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def pnv_token(self) -> str:
        return self['pnv_token']


class StarGiftBackground(dict):
    __slots__ = ()

    @overload
    def __init__(self, center_color: int, edge_color: int, text_color: int): ...

    def __init__(self, center_color, edge_color, text_color, _='starGiftBackground', **kwargs):
        kwargs['center_color'] = center_color
        kwargs['edge_color'] = edge_color
        kwargs['text_color'] = text_color
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def center_color(self) -> int:
        return self['center_color']

    @property
    def edge_color(self) -> int:
        return self['edge_color']

    @property
    def text_color(self) -> int:
        return self['text_color']


class StarGiftAuctionRound(dict):
    __slots__ = ()

    @overload
    def __init__(self, num: int, duration: int): ...

    def __init__(self, num, duration, _='starGiftAuctionRound', **kwargs):
        kwargs['num'] = num
        kwargs['duration'] = duration
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def num(self) -> int:
        return self['num']

    @property
    def duration(self) -> int:
        return self['duration']


class StarGiftAuctionRoundExtendable(dict):
    __slots__ = ()

    @overload
    def __init__(self, num: int, duration: int, extend_top: int, extend_window: int): ...

    def __init__(self, num, duration, extend_top, extend_window, _='starGiftAuctionRoundExtendable', **kwargs):
        kwargs['num'] = num
        kwargs['duration'] = duration
        kwargs['extend_top'] = extend_top
        kwargs['extend_window'] = extend_window
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def num(self) -> int:
        return self['num']

    @property
    def duration(self) -> int:
        return self['duration']

    @property
    def extend_top(self) -> int:
        return self['extend_top']

    @property
    def extend_window(self) -> int:
        return self['extend_window']


class StarGiftAttributeRarity(dict):
    __slots__ = ()

    @overload
    def __init__(self, permille: int): ...

    def __init__(self, permille, _='starGiftAttributeRarity', **kwargs):
        kwargs['permille'] = permille
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def permille(self) -> int:
        return self['permille']


class StarGiftAttributeRarityUncommon(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starGiftAttributeRarityUncommon'):
        dict.__init__(self, _=_)


class StarGiftAttributeRarityRare(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starGiftAttributeRarityRare'):
        dict.__init__(self, _=_)


class StarGiftAttributeRarityEpic(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starGiftAttributeRarityEpic'):
        dict.__init__(self, _=_)


class StarGiftAttributeRarityLegendary(dict):
    __slots__ = ()

    @overload
    def __init__(self): ...

    def __init__(self, _='starGiftAttributeRarityLegendary'):
        dict.__init__(self, _=_)


class KeyboardButtonStyle(dict):
    __slots__ = ()

    @overload
    def __init__(self, bg_primary: Optional[bool] = ..., bg_danger: Optional[bool] = ..., bg_success: Optional[bool] = ..., icon: Optional[int] = ...): ...

    def __init__(self, _='keyboardButtonStyle', **kwargs):
        kwargs['_'] = _
        dict.__init__(self, **kwargs)

    @property
    def bg_primary(self) -> Optional[bool]:
        return self['bg_primary']

    @property
    def bg_danger(self) -> Optional[bool]:
        return self['bg_danger']

    @property
    def bg_success(self) -> Optional[bool]:
        return self['bg_success']

    @property
    def icon(self) -> Optional[int]:
        return self['icon']
