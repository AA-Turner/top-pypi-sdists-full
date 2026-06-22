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

from random import getrandbits
from typing import overload

from .context import _current_client, _current_raw, _current_middle
from ...base import (
    UpdateNewMessage, UpdateBotChatInviteRequester,
    AnyInputPeer, AnyMessageEntity, AnyInputReplyTo, AnyReplyMarkup, AnySuggestedPost, AnyInputQuickReplyShortcut
)


class NcoreRawUpdate:
    __slots__ = ("update")

    def __init__(self, **update):
        self.update = update

    @property
    def client(self):
        return _current_client.get()

    @property
    def raw_update(self):
        return _current_raw.get()

    @property
    def middle(self):
        return _current_middle.get()


class NcoreUpdateNewMessage(UpdateNewMessage):
    __slots__ = ()

    @property
    def client(self):
        return _current_client.get()

    @property
    def raw_update(self):
        return _current_raw.get()

    @property
    def middle(self):
        return _current_middle.get()

    @overload
    async def answer(
            self,
            message: str,
            entities: list[AnyMessageEntity] = ...,
            reply_to: AnyInputReplyTo = ...,
            reply_markup: AnyReplyMarkup = ...,
            no_webpage: bool = ...,
            silent: bool = ...,
            background: bool = ...,
            clear_draft: bool = ...,
            noforwards: bool = ...,
            update_stickersets_order: bool = ...,
            invert_media: bool = ...,
            allow_paid_floodskip: bool = ...,
            schedule_date: int = ...,
            send_as: AnyInputPeer = ...,
            quick_reply_shortcut: AnyInputQuickReplyShortcut = ...,
            effect: int = ...,
            allow_paid_stars: int = ...,
            suggested_post: AnySuggestedPost = ...,
    ):
        """Ответить на сообщение"""
        ...

    async def answer(self, message: str, **kwargs):
        """Ответить на сообщение"""
        cid = self.message["peer_id"]

        if cid["_"] == "peerUser":
            for t in self.raw_update["users"]:
                if t["id"] == cid["user_id"]:
                    break
            else:
                self.client.error("Юзер для ответа не найден")
                raise ValueError("Юзер для ответа не найден")
            cid = {
                "_": "inputPeerUser",
                "user_id": t["id"],
                "access_hash": t["access_hash"]
            }
        elif cid["_"] == "peerChannel":
            for t in self.raw_update["chats"]:
                if t["id"] == cid["channel_id"]:
                    break
            else:
                self.client.error("Чат для ответа не найден")
                raise ValueError("Чат для ответа не найден")
            cid = {
                "_": "inputPeerChannel",
                "channel_id": t["id"],
                "access_hash": t["access_hash"]
            }
        elif cid["_"] == "peerChat":
            cid = {
                "_": "inputPeerChat",
                "chat_id": cid["chat_id"]
            }

        if "reply_to" not in kwargs and self.message["reply_to"] and self.message["reply_to"]["forum_topic"]:
            if self.message["reply_to"]["reply_to_top_id"]:
                kwargs["reply_to"] = {
                    "_": "inputReplyToMessage",
                    "reply_to_msg_id": self.message["reply_to"]["reply_to_top_id"]
                }
            elif self.message["reply_to"]["reply_to_msg_id"]:
                kwargs["reply_to"] = {
                    "_": "inputReplyToMessage",
                    "reply_to_msg_id": self.message["reply_to"]["reply_to_msg_id"]
                }

        return await self.client.send_message(
            message=message,
            peer=cid,
            random_id=getrandbits(60),
            **kwargs
        )


class NcoreUpdateBotChatInviteRequester(UpdateBotChatInviteRequester):
    __slots__ = ()

    @property
    def client(self):
        return _current_client.get()

    @property
    def raw_update(self):
        return _current_raw.get()

    @property
    def middle(self):
        return _current_middle.get()

    def _get_peer_user(self):
        for t in self.raw_update["users"]:
            if t["id"] == self["user_id"]:
                break
        else:
            self.client.error("Юзер для ответа не найден")
            raise ValueError("Юзер для ответа не найден")

        return {
            "_": "inputPeerUser",
            "user_id": t["id"],
            "access_hash": t["access_hash"]
        }

    def _get_peer_chat(self):
        raw_peer = self["peer"]

        chat_access_hash = 0
        if "chats" in self.raw_update:
            target_id = raw_peer.get("channel_id") or raw_peer.get("chat_id")

            for i in self.raw_update["chats"]:
                if i["id"] == target_id:
                    chat_access_hash = i.get("access_hash", 0)
                    break

        if raw_peer["_"] == "peerChannel":
            return {
                "_": "inputPeerChannel",
                "channel_id": raw_peer["channel_id"],
                "access_hash": chat_access_hash
            }
        elif raw_peer["_"] == "peerChat":
            return {
                "_": "inputPeerChat",
                "chat_id": raw_peer["chat_id"],
            }

    @overload
    async def answer(
            self,
            message: str,
            entities: list[AnyMessageEntity] = ...,
            reply_to: AnyInputReplyTo = ...,
            reply_markup: AnyReplyMarkup = ...,
            no_webpage: bool = ...,
            silent: bool = ...,
            background: bool = ...,
            clear_draft: bool = ...,
            noforwards: bool = ...,
            update_stickersets_order: bool = ...,
            invert_media: bool = ...,
            allow_paid_floodskip: bool = ...,
            schedule_date: int = ...,
            send_as: AnyInputPeer = ...,
            quick_reply_shortcut: AnyInputQuickReplyShortcut = ...,
            effect: int = ...,
            allow_paid_stars: int = ...,
            suggested_post: AnySuggestedPost = ...,
    ):
        ...

    async def answer(self, message: str, **kwargs):
        cid = self._get_peer_user()

        return await self.client.send_message(
            message=message,
            peer=cid,
            random_id=getrandbits(60),
            **kwargs
        )

    async def approved(self):
        peer = self._get_peer_chat()
        cid = self._get_peer_user()

        return self.client.invoke(
            {
                "_": "messages.hideChatJoinRequest",
                "peer": peer,
                "user_id": cid,
                "approved": True
            }
        )

    async def depproved(self):
        peer = self._get_peer_chat()
        cid = self._get_peer_user()

        return self.client.invoke(
            {
                "_": "messages.hideChatJoinRequest",
                "peer": peer,
                "user_id": cid,
                "approved": False
            }
        )
