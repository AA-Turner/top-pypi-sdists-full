import unittest
from xml.etree import ElementTree as ET

from slixmpp import Iq
from slixmpp.plugins import xep_0462
from slixmpp.plugins.xep_0004.stanza import Form, FormField
from slixmpp.plugins.xep_0030.stanza.items import DiscoItems
from slixmpp.test import SlixTest
from slixmpp.xmlstream import register_stanza_plugin


class TestPubsubTypeFiltering(SlixTest):
    def setUp(self):
        register_stanza_plugin(Iq, DiscoItems)
        register_stanza_plugin(Form, FormField, iterable=True)
        xep_0462.stanza.register_plugin()

    def test_setting(self):
        iq = Iq()
        iq["disco_items"]["filter"]["included_types"] = ["t1", "t2"]
        assert iq["disco_items"]["filter"]["included_types"] == ["t1", "t2"]
        self.check(
            iq,
            """
            <iq id='0'>
              <query xmlns='http://jabber.org/protocol/disco#items'>
                <filter xmlns='urn:xmpp:pubsub-filter:0'>
                  <x xmlns='jabber:x:data' type='submit'>
                    <field var='FORM_TYPE' type='hidden'>
                      <value>urn:xmpp:pubsub-filter:0</value>
                    </field>
                    <field var='included-types'>
                      <value>t1</value>
                      <value>t2</value>
                    </field>
                  </x>
                </filter>
              </query>
            </iq>
            """,
        )

        iq["disco_items"]["filter"]["included_types"] = ["t2", "t3"]
        self.assertEqual(iq["disco_items"]["filter"]["included_types"], ["t2", "t3"])
        self.check(
            iq,
            """
            <iq id='0'>
              <query xmlns='http://jabber.org/protocol/disco#items'>
                <filter xmlns='urn:xmpp:pubsub-filter:0'>
                  <x xmlns='jabber:x:data' type='submit'>
                    <field var='FORM_TYPE' type='hidden'>
                      <value>urn:xmpp:pubsub-filter:0</value>
                    </field>
                    <field var='included-types'>
                      <value>t2</value>
                      <value>t3</value>
                    </field>
                  </x>
                </filter>
              </query>
            </iq>
            """,
        )

    def test_parsing(self):
        iq = Iq(
            xml=ET.fromstring("""
            <iq type='get'
              from='rosa@com.int/desktop'
              to='news.commons.social'
              id='disco1'>
              <query xmlns='http://jabber.org/protocol/disco#items'>
                <filter xmlns='urn:xmpp:pubsub-filter:0'>
                  <x xmlns='jabber:x:data' type='submit'>
                    <field var='FORM_TYPE' type='hidden'>
                      <value>urn:xmpp:pubsub-filter:0</value>
                    </field>
                    <field type='list-multi' var='included-types'>
                      <value>urn:xmpp:microblog:0</value>
                    </field>
                  </x>
                </filter>
              </query>
            </iq>
            """)
        )
        self.assertEqual(
            iq["disco_items"]["filter"]["included_types"], ["urn:xmpp:microblog:0"]
        )

    def test_parsing_empty(self):
        iq = Iq(
            xml=ET.fromstring("""
            <iq type='get'
              from='rosa@com.int/desktop'
              to='news.commons.social'
              id='disco1'>
              <query xmlns='http://jabber.org/protocol/disco#items'>
                <filter xmlns='urn:xmpp:pubsub-filter:0' />
              </query>
            </iq>
            """)
        )
        self.assertEqual(iq["disco_items"]["filter"]["included_types"], [])


suite = unittest.TestLoader().loadTestsFromTestCase(TestPubsubTypeFiltering)
