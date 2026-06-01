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

import re

from typing import overload
from collections.abc import Awaitable, Callable


from .types import EventType, EVENT_ROUTER, NcoreRawUpdate
from .types.events.context import _current_client, _current_raw, _current_middle


class HandlerMeta:
    __slots__ = ("func", "arg_instructions", "custom_filter")

    def __init__(self, func, args_mapping, custom_filter):
        self.func = func

        if args_mapping:
            self.arg_instructions = tuple(
                (g_name, arg_name, conv) for g_name, (arg_name, conv) in args_mapping.items()
            )
        else:
            self.arg_instructions = None

        self.custom_filter = custom_filter


class RouteNode:
    __slots__ = ("regex", "handlers_meta", "generic_handlers")

    def __init__(self, regex, handlers_meta, generic_handlers=None):
        self.regex = regex
        self.handlers_meta = handlers_meta
        self.generic_handlers = generic_handlers or []


class Router:
    __slots__ = ("_raw_registrations", "_routes", "_tag_parser", "prefixes", "client")

    def __init__(self, prefixes: list[str]=["/"]):
        self._raw_registrations = []
        self._routes = {}
        self._tag_parser = re.compile(r"^<(!?)([a-zA-Z0-9_]+):\s*(int|str|float|bool)>$")
        self.prefixes = sorted(prefixes, key=len, reverse=True)

    @overload
    def add(self, command: str, event_type: set[str] | None=None, filter: Callable[[dict], Awaitable[bool]] | None=None):
        ...

    @overload
    def add(self, event_type: set[str], command: str | None=None, filter: Callable[[dict], Awaitable[bool]] | None=None):
        ...

    def add(self, arg1: str | set[str], arg2: str | set[str] | None=None, filter: Callable[[dict], Awaitable[bool]] | None=None):
        def decorator(func):
            command_pattern = None
            event_types = set()

            for arg in [arg1, arg2]:
                if isinstance(arg, str):
                    command_pattern = arg
                elif isinstance(arg, set):
                    event_types = arg

            if not event_types:
                event_types = EventType.NewMessage

            self._raw_registrations.append({
                "func": func,
                "cmd": command_pattern,
                "types": frozenset(event_types),
                "filter": filter
            })
            return func
        return decorator

    def _convert_bool(self, val):
        return val.lower() in {"1", "true", "on", "yes", "enable"}

    def _compile_cmd_pattern(self, command, handler_uid):
        arg_idx = 0
        final_pattern = ""
        args_map = {}
        parts = [p.strip(" ") for p in re.split(r"(<[^>]+>)", command) if p.strip(" ")]

        for i, part in enumerate(parts):
            part_regex = ""
            is_optional_param = False
            tag_match = self._tag_parser.match(part)

            if tag_match:
                req_mark, name, typ = tag_match.groups()
                is_optional_param = not (req_mark == "!")
                g_name = f"{handler_uid}_a{arg_idx}"
                arg_idx += 1

                if typ == "int":
                    ptn = r"\d+"
                    cnv = int
                elif typ == "float":
                    ptn = r"\d+(?:\.\d+)?" 
                    cnv = float
                elif typ == "str":
                    ptn = r".+?"
                    cnv = str
                elif typ == 'bool':
                    ptn = r"(?i:1|0|true|false|on|off|yes|no|да|нет)"
                    cnv = self._convert_bool
                else:
                    ptn = r"\S+"
                    cnv = str

                part_regex = f"(?P<{g_name}>{ptn})"
                args_map[g_name] = (name, cnv)
            elif part.isspace():
                continue
            else:
                part_regex = re.escape(part)

            if i == 0:
                if is_optional_param:
                    final_pattern += f"(?:{part_regex})?"
                else:
                    final_pattern += part_regex
            else:
                space_str = r"[^\S\r\n]+" if not (not self._tag_parser.match(parts[i-1]) and parts[i-1].isspace()) else re.escape(parts[i-1])
                if is_optional_param:
                    final_pattern += f"(?:{space_str}{part_regex})?"
                else:
                    final_pattern += f"{space_str}{part_regex}"

        return final_pattern, args_map

    def finalize(self, client):
        self.client = client
        prefix_regex = ""
        if self.prefixes:
            prefix_regex = f"(?:{'|'.join(re.escape(p) for p in self.prefixes)})\\s*"

        grouped_by_event = {}
        for reg in self._raw_registrations:
            for event_type_str in reg["types"]:
                if event_type_str not in grouped_by_event:
                    grouped_by_event[event_type_str] = []
                grouped_by_event[event_type_str].append(reg)

        for event_type_str, handlers in grouped_by_event.items():
            regex_opts = []
            meta_map = {}
            specific = []
            generics = []

            for h in handlers:
                (specific if h["cmd"] else generics).append(h)

            generic_meta = []
            for h in generics:
                generic_meta.append(HandlerMeta(h["func"], None, h["filter"]))

            def clean_cmd_len(cmd_str):
                return len(re.sub(r"<[^>]+>", "", cmd_str))

            specific.sort(key=lambda x: clean_cmd_len(x["cmd"]), reverse=True)

            for i, h in enumerate(specific):
                uid = f"h{i}"
                p_str, args = self._compile_cmd_pattern(h["cmd"], uid)
                regex_opts.append(f"(?P<{uid}>^{prefix_regex}{p_str}$)")
                meta_map[uid] = HandlerMeta(h["func"], args, h["filter"])

            full_regex = None
            if regex_opts:
                full_regex = re.compile("|".join(regex_opts), re.DOTALL | re.IGNORECASE)
                group_index_map = full_regex.groupindex

                for uid, meta in meta_map.items():
                    if meta.arg_instructions:
                        new_instructions = []
                        for g_name, arg_name, conv in meta.arg_instructions:
                            g_idx = group_index_map.get(g_name)
                            new_instructions.append((g_idx, arg_name, conv))
                        meta.arg_instructions = tuple(new_instructions)

            self._routes[event_type_str] = RouteNode(full_regex, meta_map, generic_meta)

        del self._raw_registrations

    async def _process_update(self, update, full_context, middle=None):
        if update["_"] not in self._routes:
            return False
 
        node = self._routes[update["_"]]

        if node.generic_handlers:
            for meta in node.generic_handlers:
                if meta.custom_filter and not await meta.custom_filter(full_context):
                    continue

                _current_client.set(self.client)
                _current_raw.set(full_context)
                _current_middle.set(middle)

                await meta.func(EVENT_ROUTER.get(update["_"], NcoreRawUpdate)(**update))
            return True

        if "message" not in update or "message" not in update["message"]:
            return False

        match = node.regex.match(update["message"]["message"])
        if not match:
            return False

        meta = node.handlers_meta[match.lastgroup]
        if meta.custom_filter and not await meta.custom_filter(full_context):
            return False

        if meta.arg_instructions is None:
            _current_client.set(self.client)
            _current_raw.set(full_context)
            _current_middle.set(middle)

            await meta.func(EVENT_ROUTER.get(update["_"], NcoreRawUpdate)(**update))
            return True

        kwargs = {}
        for g_idx, arg_name, conv in meta.arg_instructions:
            val = match.group(g_idx)
            kwargs[arg_name] = None if val is None else conv(val)

        _current_client.set(self.client)
        _current_raw.set(full_context)
        _current_middle.set(middle)

        await meta.func(EVENT_ROUTER.get(update["_"], NcoreRawUpdate)(**update), **kwargs)
        return True
