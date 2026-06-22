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

import sys
import hashlib
import inspect
import asyncio
import msgpack


from .router import Router
from .session import Session
from .connect import Connect
from .base import build_object
from .base.methods import TLMethod, ReturnT


class BaseClient:
    def info(self, txt):
        sys.stdout.write(f"\033[1;34m[ INFO ] [ {inspect.currentframe().f_back.f_code.co_name} ] {txt}\033[0m\n")

    def warn(self, txt):
        sys.stdout.write(f"\033[1;33m[ WARN ] [ {inspect.currentframe().f_back.f_code.co_name} ] {txt}\033[0m\n")

    def error(self, txt):
        sys.stdout.write(f"\033[1;31m[ ERROR ] [ {inspect.currentframe().f_back.f_code.co_name} ] {txt}\033[0m\n")

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        bot_token: str,
        loop: asyncio.AbstractEventLoop | None = None,
        connection: Connect = Connect(),
        storagename: str = "storage",
        device_model: str = "Ncore python",
        system_version: str = "10.0",
        app_version: str = "4.0",
        system_lang_code: str = "ru",
        lang_pack: str = "tdesktop",
        lang_code: str = "ru"
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.storagename = storagename
        self.loop = loop
        self._init_config = {
            "device_model": device_model,
            "system_version": system_version,
            "app_version": app_version,
            "system_lang_code": system_lang_code,
            "lang_pack": lang_pack,
            "lang_code": lang_code,
        }

        if self.storagename and self.storagename != ":memory:":
            sfbt = hashlib.sha256(self.bot_token.encode("utf-8")).hexdigest()

            try:
                with open(self.storagename, "rb") as f:
                    self.storage: dict = msgpack.load(f)
                if self.storage.get("bot_token", "") != sfbt:
                    raise ValueError("токен не совпадает")
                self.info(f"Сессия [{self.storagename}] загружена")
            except Exception:
                self.storage = {
                    "id": None,
                    "first_name": None,
                    "username": None,
                    "dc_id": 2,
                    "auth_key": None,
                    "bot_token": sfbt
                }
                self.save_storage()
                self.info(f"Сессия [{self.storagename}] создана")
        else:
            self.storage = {
                "id": None,
                "first_name": None,
                "username": None,
                "dc_id": 2,
                "auth_key": None
            }
            self.info("Сессия [:memory:] загружена")

        self.connection = connection
        self.connection.client = self

        self._pre_middleware = None
        self._post_middleware = None

    def save_storage(self):
        if not self.storagename or self.storagename == ":memory:":
            return
        try:
            with open(self.storagename, "wb") as f:
                msgpack.dump(self.storage, f)
        except Exception as ex:
            self.error(f"Ошибка сохранения сессии [{self.storagename}] -> {ex}")

    def set_pre_middleware(self, obj):
        self._pre_middleware = obj

    async def handle_updates(self, message):
        if self._pre_middleware is not None:
            if await self._pre_middleware(message) is False:
                return

        obj_type = message["_"]
        if obj_type in {"updates", "updatesCombined"}:
            [
                self.loop.create_task(self.router._process_update(update, full_context=message, middle=self._pre_middleware))
                for update in message["updates"]
            ]
        elif obj_type == "updateShort":
            self.loop.create_task(self.router._process_update(message["update"], full_context=message, middle=self._pre_middleware))
        else:
            self.loop.create_task(self.router._process_update(message, full_context=message, middle=self._pre_middleware))

    async def invoke(self, query: TLMethod[ReturnT], timeout=15, retrying=3, retry_delay=1.5) -> ReturnT:
        session = self.session
        msg = session.msg_factory.create(query)

        session.wait_packet[msg.msg_id] = session.loop.create_future()

        for attempt in range(retrying):
            session._batch_list.append(msg)
            session._batch_event.set()

            try:
                result = await session.wait_packet[msg.msg_id]
                if result is None:
                    raise ValueError("Ошибка отправки invoke. Сервер не ответил.")

                result = result.get("result", result)
                if "error_code" in result:
                    if result["error_code"] == 420:
                        wait = float(result["error_message"].replace("FLOOD_WAIT_", ""))
                        await asyncio.sleep(wait)
                        self.warn(f"Обнаружен флуд, ожидание {wait}")
                        continue
                return build_object(result)

            except asyncio.TimeoutError as exc:
                raise asyncio.TimeoutError() from exc
            except Exception as ex:
                if attempt < retrying:
                    self.warn(f"Ошибка отправки invoke -> {ex} ({result}). Попытка {attempt + 1}/{retrying}")
                    await asyncio.sleep(retry_delay)
                else:
                    raise TimeoutError(f"Ошибка отправки invoke, исчерпаны попытки({retrying}) -> {query} | {ex}")
            finally:
                session.wait_packet.pop(msg.msg_id, None)
        raise TimeoutError(f"Не удалось выполнить запрос {query} после {retrying} попыток")

    async def idle(self):
        self.stop_event = asyncio.Event()
        await self.stop_event.wait()

    async def stop(self):
        await self.session.stop(r=0)
        self.stop_event.set()

    async def start(
        self,
        router: Router | None=None,
        handle_updates: None=None,
        proxy: str | None=None,
        load_updates: bool = False
    ):
        self.loop = asyncio.get_running_loop()

        if handle_updates is not None:
            self.handle_updates = handle_updates

        if router is not None:
            router.finalize(self)
            self.router = router

        self.proxy = proxy
        self.session = Session(self)

        await self.session.start()
        await self.session.send({"_": "getState"})

    def run(
        self,
        router: Router | None=None,
        handle_updates=None,
        proxy: str | None=None,
        load_updates: bool = False
    ):
        if self.loop is None:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self.start(router=router, handle_updates=handle_updates, proxy=proxy, load_updates=load_updates))
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.session.stop(r=0))
            self.info("Бот остановлен пользователем (Ctrl+C)")
