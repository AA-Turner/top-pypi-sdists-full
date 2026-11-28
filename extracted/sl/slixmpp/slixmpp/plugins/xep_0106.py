
# Slixmpp: The Slick XMPP Library
# Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

from slixmpp.jid import escape_node, unescape_node
from slixmpp.plugins import BasePlugin, register_plugin


class XEP_0106(BasePlugin):

    name = 'xep_0106'
    description = 'XEP-0106: JID Escaping'
    dependencies = {'xep_0030'}

    def session_bind(self, jid):
        self.xmpp.plugin['xep_0030'].add_feature(feature='jid\\20escaping')

    def plugin_end(self):
        self.xmpp.plugin['xep_0030'].del_feature(feature='jid\\20escaping')

    @staticmethod
    def escape(node: str) -> str:
        return escape_node(node)

    @staticmethod
    def unescape(node: str) -> str:
        return unescape_node(node)


register_plugin(XEP_0106)
