# Slixmpp: The Slick XMPP Library
# Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.
from typing import ClassVar

from slixmpp.plugins import BasePlugin
from slixmpp.xmlstream import StanzaBase
from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath

from . import stanza


class XEP_0513(BasePlugin):
    """
    This plugin adds support for XEP-0513: Intentional Mention Markup.

    Mentions are carried in XEP-0394 markup spans. A ``mention`` event is
    emitted for each incoming message containing at least one mention.
    """

    name = "xep_0513"
    description = "XEP-0513: Intentional Mention Markup"
    dependencies: ClassVar[set[str]] = {"xep_0030", "xep_0394"}
    stanza = stanza

    def plugin_init(self) -> None:
        stanza.register_plugin()
        self.xmpp.register_handler(
            Callback(
                "Intentional Mention",
                StanzaPath("message/markup/span/mention"),
                self._handle_mention,
            )
        )
        self.xmpp.plugin["xep_0030"].add_feature(stanza.NAMESPACE)

    def plugin_end(self) -> None:
        self.xmpp.remove_handler("Intentional Mention")
        self.xmpp["xep_0030"].del_feature(feature=stanza.NAMESPACE)

    def _handle_mention(self, msg: StanzaBase) -> None:
        self.xmpp.event("mention", msg)
