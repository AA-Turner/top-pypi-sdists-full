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

from typing import overload


from ..base.types import AnyInputPeer, AnyMessageEntity, AnyInputReplyTo, AnyReplyMarkup, AnyInputQuickReplyShortcut, AnySuggestedPost


class SendMessage:
    @overload
    async def send_message(
        self,
        message: str,
        peer: AnyInputPeer,
        random_id: int,
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
    ) -> dict:
        ...

    async def send_message(self, message: str, peer: AnyInputPeer, random_id: int, **params) -> dict:
        params["_"] = "messages.sendMessage"
        params["message"] = message
        params["peer"] = peer
        params["random_id"] = random_id
        return await self.invoke(params)
