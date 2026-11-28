
# slixmpp.xmlstream.matcher.id
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Part of Slixmpp: The Slick XMPP Library
# :copyright: (c) 2011 Nathanael C. Fritz
# :license: MIT, see LICENSE for more details

from slixmpp.xmlstream.matcher.base import MatcherBase
from slixmpp.xmlstream.stanzabase import StanzaBase
from slixmpp.jid import JID
from slixmpp.types import TypedDict


class CriteriaType(TypedDict):
    self: JID
    peer: JID
    id: str


class MatchIDSender(MatcherBase):

    """
    The IDSender matcher selects stanzas that have the same stanza 'id'
    interface value as the desired ID, and that the 'from' value is one
    of a set of approved entities that can respond to a request.

    It takes a dictionary with "self" and "peer" keys mapped to JID objects,
    respectively for our own JID or the peer JID, and an "id" key for the
    identifier to match.
    """
    _criteria: tuple[str, dict[str | JID, bool]]

    def __init__(self, criteria: CriteriaType) -> None:
        # Take a dict for backwards compatibility
        selfjid = criteria['self']
        peerjid = criteria['peer']

        # Pre-emptively allocate the dict so that it is reused on each match
        allowed: dict[str, bool] = {}
        allowed[''] = True
        allowed[selfjid.bare] = True
        allowed[selfjid.domain] = True
        allowed[peerjid.full] = True
        allowed[peerjid.bare] = True
        allowed[peerjid.domain] = True
        super().__init__((
            criteria['id'],
            allowed,
        ))

    def match(self, xml: StanzaBase) -> bool:
        """Compare the given stanza's ``'id'`` attribute to the stored
        ``id`` value, and verify the sender's JID.

        :param xml: The :class:`~slixmpp.xmlstream.stanzabase.StanzaBase`
                    stanza to compare against.
        """

        _id, allowed = self._criteria
        _from = xml.get_toplevel_attr('from', default='')

        try:
            return xml.get_toplevel_attr('id', '') == _id and allowed[_from]
        except KeyError:
            return False
