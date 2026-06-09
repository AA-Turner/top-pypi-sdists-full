from slixmpp.plugins.base import register_plugin

from . import stanza
from .privilege import XEP_0356
from .stanza import Perm, Privilege

register_plugin(XEP_0356)

__all__ = ['stanza', 'XEP_0356', 'Perm', 'Privilege', 'XEP_0356']
