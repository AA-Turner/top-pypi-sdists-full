from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TypeVar

from pydantic import BaseModel


@dataclass
class WSDisconnected:
    error_message: str | None = None


@dataclass
class SwitchCLIChat:
    new_chat_uuid: str


REMOTE_EXECUTION_CLIENT_EXIT_INFO = WSDisconnected | SwitchCLIChat

TModel = TypeVar("TModel", bound=BaseModel)

cli_uuid = uuid.uuid4()
