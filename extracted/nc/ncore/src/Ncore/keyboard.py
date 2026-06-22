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

from typing import Optional, overload


from .base.types import aliases
from .base.types import ReplyInlineMarkup, ReplyKeyboardMarkup


class InlineKeyboard(ReplyInlineMarkup):
    __slots__ = ("__idx", "__max_idx", "__current_buttons")

    def __init__(self, rows: list[aliases.AnyKeyboardButtonRow] | None=None):
        self['_'] = 'replyInlineMarkup'

        if not rows:
            self['rows'] = [{"buttons": [], '_': "keyboardButtonRow"}]
            self.__max_idx = 0
            self.__idx = 0
        else:
            self['rows'] = rows
            self.__max_idx = len(rows) - 1
            self.__idx = self.__max_idx

        self.__current_buttons = self["rows"][self.__idx]["buttons"]

    def row(self, current_row: int | None=None):
        if current_row is not None:
            if current_row < 0 or current_row > self.__max_idx:
                raise ValueError("current_row должен быть меньше или равен максимальному количеству рядов")
            self.__idx = current_row
            self.__current_buttons = self["rows"][self.__idx]["buttons"]
            return self

        self.__idx += 1

        if self.__idx > self.__max_idx:
            self["rows"].append({"buttons": [], '_': "keyboardButtonRow"})
            self.__max_idx += 1

        self.__current_buttons = self["rows"][self.__idx]["buttons"]
        return self

    @overload
    def url(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def url(self, text, url, _='keyboardButtonUrl', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def callback(self, text: str, data: bytes, requires_password: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def callback(self, text, data, _='keyboardButtonCallback', **kwargs):
        kwargs['text'] = text
        kwargs['data'] = data
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def switch_inline(self, text: str, query: str, same_peer: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ..., peer_types: Optional[list[aliases.AnyInlineQueryPeerType]] = ...): ...

    def switch_inline(self, text, query, _='keyboardButtonSwitchInline', **kwargs):
        kwargs['text'] = text
        kwargs['query'] = query
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def game(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def game(self, text, _='keyboardButtonGame', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def buy(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def buy(self, text, _='keyboardButtonBuy', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def url_auth(self, text: str, url: str, bot: aliases.AnyInputUser, request_write_access: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ..., fwd_text: Optional[str] = ...): ...

    def url_auth(self, text, url, bot, _='inputKeyboardButtonUrlAuth', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['bot'] = bot
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def web_view(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def web_view(self, text, url, _='keyboardButtonWebView', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def copy_button(self, text: str, copy_text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def copy_button(self, text, copy_text, _='keyboardButtonCopy', **kwargs):
        kwargs['text'] = text
        kwargs['copy_text'] = copy_text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def user_profile(self, text: str, user_id: aliases.AnyInputUser, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def user_profile(self, text, user_id, _='inputKeyboardButtonUserProfile', **kwargs):
        kwargs['text'] = text
        kwargs['user_id'] = user_id
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self


class ReplyKeyboard(ReplyKeyboardMarkup):
    __slots__ = ("__idx", "__max_idx", "__current_buttons")

    @overload
    def __init__(self, rows: Optional[list[aliases.AnyKeyboardButtonRow]] = None, resize: Optional[bool] = ..., single_use: Optional[bool] = ..., selective: Optional[bool] = ..., persistent: Optional[bool] = ..., placeholder: Optional[str] = ...): ...

    def __init__(self, rows=None, **kwargs):
        self.update(kwargs)

        self['_'] = 'replyKeyboardMarkup'

        if not rows:
            self['rows'] = [{"buttons": [], '_': "keyboardButtonRow"}]
            self.__max_idx = 0
            self.__idx = 0
        else:
            self['rows'] = rows
            self.__max_idx = len(rows) - 1
            self.__idx = self.__max_idx

        self.__current_buttons = self["rows"][self.__idx]["buttons"]

    def row(self, current_row: int | None=None):
        if current_row is not None:
            if current_row < 0 or current_row > self.__max_idx:
                raise ValueError("current_row должен быть в диапазоне [0 ... max_row]")
            self.__idx = current_row
            self.__current_buttons = self["rows"][self.__idx]["buttons"]
            return self

        self.__idx += 1

        if self.__idx > self.__max_idx:
            self["rows"].append({"buttons": [], '_': "keyboardButtonRow"})
            self.__max_idx += 1

        self.__current_buttons = self["rows"][self.__idx]["buttons"]
        return self

    @overload
    def button(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def button(self, text, _='keyboardButton', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def request_phone(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def request_phone(self, text, _='keyboardButtonRequestPhone', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def request_geo_location(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def request_geo_location(self, text, _='keyboardButtonRequestGeoLocation', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def request_poll(self, text: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ..., quiz: Optional[bool] = ...): ...

    def request_poll(self, text, _='keyboardButtonRequestPoll', **kwargs):
        kwargs['text'] = text
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def request_peer(self, text: str, button_id: int, peer_type: aliases.AnyRequestPeerType, max_quantity: int, name_requested: Optional[bool] = ..., username_requested: Optional[bool] = ..., photo_requested: Optional[bool] = ..., style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def request_peer(self, text, button_id, peer_type, max_quantity, _='inputKeyboardButtonRequestPeer', **kwargs):
        kwargs['text'] = text
        kwargs['button_id'] = button_id
        kwargs['peer_type'] = peer_type
        kwargs['max_quantity'] = max_quantity
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self

    @overload
    def simple_web_view(self, text: str, url: str, style: Optional[aliases.AnyKeyboardButtonStyle] = ...): ...

    def simple_web_view(self, text, url, _='keyboardButtonSimpleWebView', **kwargs):
        kwargs['text'] = text
        kwargs['url'] = url
        kwargs['_'] = _

        self.__current_buttons.append(kwargs)
        return self


__all__ = ["InlineKeyboard", "ReplyKeyboard"]
