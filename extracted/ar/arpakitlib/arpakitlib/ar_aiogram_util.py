# arpakit

import asyncio
import logging
from typing import Optional, Any, Callable

from aiogram import types
from aiogram.exceptions import AiogramError
from aiogram.filters import CommandObject
from pydantic import BaseModel

from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import BadCommandFormat, parse_command
from arpakitlib.ar_type_util import raise_for_types

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class BadTgCommandFormat(BadCommandFormat):
    pass


class BaseTgCommandParam(BaseModel):
    key: str


class TgCommandFlagParam(BaseTgCommandParam):
    pass


class TgCommandKeyValueParam(BaseTgCommandParam):
    need_type: str
    index: Optional[int] = None
    required: bool = False
    default: Optional[Any] = None

    @property
    def has_index(self) -> bool:
        return False if self.index is None else True


def as_tg_command(
        *params: TgCommandFlagParam | TgCommandKeyValueParam,
        desc: str | None = None,
        passwd_validator: Callable | str | None = None,
        remove_message_after_correct_passwd: bool = True
):
    _PASSWD_KEY = "passwd"
    _HELP_FLAG = "help"

    params = list(params)

    if passwd_validator is not None:
        raise_for_types(passwd_validator, [Callable, str])
        params.append(TgCommandKeyValueParam(key=_PASSWD_KEY, required=True, index=None, need_type=NeedTypes.str_))

    params.append(TgCommandFlagParam(key=_HELP_FLAG))

    _were_keys = set()
    for param in params:
        if param.key in _were_keys:
            raise ValueError(f"key={param.key} is duplicated")
        _were_keys.add(param.key)
    _were_keys.clear()

    _were_indexes = set()
    for param in params:
        if not isinstance(param, TgCommandKeyValueParam) or not param.has_index:
            continue
        if param.index in _were_indexes:
            raise ValueError(f"index={param.index} is duplicated")
        _were_indexes.add(param.index)

    def decorator(handler):

        async def new_handler(*args, **kwargs):
            message: types.Message = args[0]
            if not isinstance(message, types.Message):
                raise TypeError("not isinstance(message, types.Message)")

            command: CommandObject = kwargs["command"]

            try:
                parsed_command = parse_command(command.text)
                kwargs["parsed_command"] = parsed_command

                if (
                        not parsed_command.values_without_key
                        and len(parsed_command.flags) == 1
                        and parsed_command.has_flag(_HELP_FLAG)
                ):
                    text = f"<b>Command</b> /{command.command}"
                    if desc is not None:
                        text += "\n\n" + desc
                    text += "\n\n"

                    if passwd_validator is not None:
                        text += "Passwd is required\n\n"

                    text += "<b>Keys:</b>\n"
                    tg_command_key_value_params = list(filter(lambda p: isinstance(p, TgCommandKeyValueParam), params))
                    if tg_command_key_value_params:
                        for i, _param in enumerate(tg_command_key_value_params):
                            text += f"{i + 1}. <code>{_param.key}</code>"
                            if _param.has_index:
                                text += f", {_param.index}"
                            text += f", {_param.need_type}"
                            if _param.required is True:
                                text += ", <b>required</b>"
                            else:
                                text += ", not required"
                            if _param.default is not None:
                                text += f", <code>{_param.default}</code>"
                            text = text.strip()
                            text += "\n"
                    else:
                        text += "<i>No keys</i>"
                    text = text.strip()
                    text += "\n\n"

                    text += "<b>Flags:</b>\n"
                    tg_command_flag_params = list(filter(lambda p: isinstance(p, TgCommandFlagParam), params))
                    if tg_command_flag_params:
                        for i, _param in enumerate(tg_command_flag_params):
                            text += f"{i + 1}. <code>-{_param.key}</code>\n"
                    else:
                        text += "<i>No flags</i>"
                    text = text.strip()
                    text += "\n\n"

                    text += f"<code>/{command.command} -{_HELP_FLAG}</code>"
                    text += f"\n<code>/{command.command}</code>"

                    await message.answer(text=text.strip())
                    return

                if passwd_validator is not None:
                    passwd_ = parsed_command.get_value_by_key(_PASSWD_KEY)
                    if not passwd_:
                        is_passwd_correct = False
                    elif isinstance(passwd_validator, Callable):
                        is_passwd_correct = passwd_validator(
                            passwd=passwd_, message=message, parsed_command=parsed_command
                        )
                    elif isinstance(passwd_validator, str):
                        is_passwd_correct = (passwd_validator == passwd_)
                    else:
                        raise TypeError("check_passwd is not not Callable and not str")
                    if not is_passwd_correct:
                        await message.answer("Passwd is incorrect")
                        return
                    if remove_message_after_correct_passwd:
                        try:
                            await message.delete()
                        except AiogramError as e:
                            _logger.error(e)
                    try:
                        await message.answer("Passwd is ok")
                    except AiogramError as e:
                        _logger.error(e)

                for _param in params:
                    if isinstance(_param, TgCommandFlagParam):
                        kwargs[_param.key] = parsed_command.has_flag(_param.key)

                    elif isinstance(_param, TgCommandKeyValueParam):
                        if _param.key in kwargs.keys():
                            raise BadTgCommandFormat(f"{_param.key} already in {kwargs.keys()}")

                        value_by_key: Optional[str] = parsed_command.get_value_by_key(_param.key)

                        value_by_index: Optional[str] = None
                        if _param.has_index:
                            value_by_index = parsed_command.get_value_by_index(_param.index)

                        if value_by_key is not None and value_by_index is not None:
                            raise BadTgCommandFormat(
                                f"Value was found by key={_param.key} and index={_param.index}"
                            )

                        value = value_by_key if value_by_key is not None else value_by_index

                        if value is None:
                            if _param.default is not None:
                                value = _param.default
                            elif _param.required is True:
                                raise BadTgCommandFormat(
                                    f"Value (key={_param.key}, index={_param.index}) is required"
                                )
                        else:
                            value = parse_need_type(value=value, need_type=_param.need_type, allow_none=False)

                        kwargs[_param.key] = value

                    else:
                        raise TypeError(f"bad type for param, {type(_param)}")

            except BadCommandFormat as e:
                await message.answer(
                    f"<b>Bad command usage</b> /{command.command}\n\n"

                    "<b>Error</b>\n"
                    f"{e}\n\n"

                    f"Use <code>/{command.command} -{_HELP_FLAG}</code> for getting help info"
                )
                return

            return await handler(*args, **kwargs)

        return new_handler

    return decorator


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
