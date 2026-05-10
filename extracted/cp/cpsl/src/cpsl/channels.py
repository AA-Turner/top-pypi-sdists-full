"""Channel transport declarations.

Web chat is always enabled implicitly — you never need to declare it.
The ``channels=`` parameter is only for external integrations::

    @app.cls(
        channels=[cpsl.Channel("my-telegram-bot")],
    )

External channels are named resources created via ``capsule channel create``
or the dashboard. Reference them by name with ``cpsl.Channel("name")``.

The old inline credential classes (``Telegram``, ``Slack``, ``WhatsApp``)
are deprecated and will be removed in a future release.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, fields
from typing import Union

from .secret import Secret

CredentialValue = Union[str, Secret, None]


def _serialize_credential(v: CredentialValue) -> str | dict | None:
    if v is None or v == "":
        return None
    if isinstance(v, Secret):
        return v.to_dict()
    return v


@dataclass
class Chat:
    """Built-in web chat — always enabled implicitly.

    You do not need to include this in your ``channels=`` list.
    It exists for backward compatibility only.
    """

    type: str = "chat"

    def to_dict(self) -> dict:
        return {"type": self.type}


class ChannelRef:
    """Reference to a named channel resource created via CLI/dashboard.

    Usage::

        @app.cls(channels=[cpsl.Channel("my-telegram-bot")])
    """

    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> dict:
        return {"type": "_resource", "name": self.name}


# Convenience alias
Channel = ChannelRef


@dataclass
class _DeprecatedChannel:
    """Base for deprecated inline credential channels."""

    type: str = ""

    def to_dict(self) -> dict:
        warnings.warn(
            f"Inline {self.__class__.__name__}(...) is deprecated. "
            f'Use cpsl.Channel("<name>") with a channel resource created via '
            f"'capsule channel create'. See docs for migration.",
            DeprecationWarning,
            stacklevel=3,
        )
        d: dict = {"type": self.type}
        for f in fields(self):
            if f.name == "type":
                continue
            v = getattr(self, f.name)
            serialized = _serialize_credential(v)
            if serialized is not None:
                d[f.name] = serialized
        return d


@dataclass
class Telegram(_DeprecatedChannel):
    """Telegram Bot API. **Deprecated** — use Channel("name") instead."""

    type: str = "telegram"
    bot_token: CredentialValue = None


@dataclass
class Slack(_DeprecatedChannel):
    """Slack Events API. **Deprecated** — use Channel("name") instead."""

    type: str = "slack"
    bot_token: CredentialValue = None
    signing_secret: CredentialValue = None


@dataclass
class WhatsApp(_DeprecatedChannel):
    """WhatsApp Cloud API. **Deprecated** — use Channel("name") instead."""

    type: str = "whatsapp"
    access_token: CredentialValue = None
    phone_number_id: CredentialValue = None
    verify_token: CredentialValue = None


@dataclass
class API:
    """REST API transport. Synchronous request/response."""

    type: str = "api"

    def to_dict(self) -> dict:
        return {"type": self.type}
