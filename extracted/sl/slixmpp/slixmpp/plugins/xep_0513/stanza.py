"""
Stanza interfaces for XEP-0513: Intentional Mention Markup (v0.1.1)

Basic usage:

>>> register_plugin()  # automatically done if you use this plugin
>>> msg = Message()
>>> msg["body"] = "Hello, Alice!"
>>> msg["markup"]["span"]["start"] = 7
>>> msg["markup"]["span"]["end"] = 12
>>> msg["markup"]["span"]["mention"]["type"] = "occupant"
>>> msg["markup"]["span"]["mention"]["target"] = "alice@occupant-id"
>>> msg.pretty_print()
<message xmlns="jabber:client">
  <body>Hello, Alice!</body>
  <markup xmlns="urn:xmpp:markup:0">
    <span start="7" end="12">
      <mention xmlns="urn:xmpp:mentions:0" type="urn:xmpp:mentions:0#occupant" target="alice@occupant-id" />
    </span>
  </markup>
</message>
"""

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
from typing import ClassVar, Literal

import slixmpp.plugins.xep_0394.stanza
from slixmpp.jid import JID
from slixmpp.stanza.message import Message
from slixmpp.xmlstream import ElementBase, register_stanza_plugin

MentionTypeLiteral = Literal[
    "occupant",
    "channel",
    "moderators",
    "participants",
    "visitors",
    "owners",
    "admins",
    "members",
    "none",
    "hats",
]


NAMESPACE = "urn:xmpp:mentions:0"


class Mention(ElementBase):
    name = "mention"
    namespace = NAMESPACE
    plugin_attrib = "mention"
    plugin_multi_attrib = "mentions"
    interfaces: ClassVar[set[str]] = {"type", "target", "active"}

    def set_type(self, value: MentionTypeLiteral | str) -> None:
        """
        Short names ("occupant") expand to the full type URI.

        :param value:
        """
        if "#" not in value and ":" not in value:
            value = f"{self.namespace}#{value}"
        self._set_attr("type", value)

    def get_type(self) -> str | None:
        return self._get_attr("type") or None

    def set_target(self, target: JID | str) -> None:
        self._set_attr("target", str(target))

    def get_target(self) -> str | None:
        return self._get_attr("target") or None

    def set_active(self, active: bool) -> None:
        self._set_attr("active", "true" if active else None)

    def get_active(self) -> bool:
        return self._get_attr("active") in ("true", "1")


def register_plugin() -> None:
    register_stanza_plugin(Message, slixmpp.plugins.xep_0394.stanza.Markup)
    register_stanza_plugin(slixmpp.plugins.xep_0394.stanza.Span, Mention, iterable=True)


log = logging.getLogger(__name__)
