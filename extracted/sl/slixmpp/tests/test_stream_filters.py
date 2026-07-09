from slixmpp import Message
import unittest
import base64
from xml.etree import ElementTree as ET
from slixmpp.test import SlixTest


class TestFilters(SlixTest):

    """
    Test using incoming and outgoing filters.
    """

    def setUp(self):
        self.stream_start()

    def testIncoming(self):

        data = []

        def in_filter(stanza):
            if isinstance(stanza, Message):
                if stanza['body'] == 'testing':
                    stanza['subject'] = stanza['body'] + ' filter'
                    print('>>> %s' % stanza['subject'])
            return stanza

        def on_message(msg):
            print('<<< %s' % msg['subject'])
            data.append(msg['subject'])

        self.xmpp.add_filter('in', in_filter)
        self.xmpp.add_event_handler('message', on_message)

        self.recv("""
          <message>
            <body>no filter</body>
          </message>
        """)

        self.recv("""
          <message>
            <body>testing</body>
          </message>
        """)

        self.assertEqual(data, [None, 'testing filter'],
                'Incoming filter did not apply %s' % data)

    def testOutgoing(self):

        def out_filter(stanza):
            if isinstance(stanza, Message):
                if stanza['body'] == 'testing':
                    stanza['body'] = 'changed!'
            return stanza

        self.xmpp.add_filter('out', out_filter)

        m1 = self.Message()
        m1['body'] = 'testing'
        m1.send()

        m2 = self.Message()
        m2['body'] = 'blah'
        m2.send()

        self.send("""
          <message>
            <body>changed!</body>
          </message>
        """)

        self.send("""
          <message>
            <body>blah</body>
          </message>
        """)

    def test_out_sce(self):
        def out(stanza):
            if isinstance(stanza, Message):
                stanza['body'] += ' fixed'
            return stanza

        def out_sce(stanza):
            if isinstance(stanza, Message):
                secure = base64.b32encode(stanza['body'].encode()).decode()
                stanza.append(ET.fromstring('<secret>%s</secret>' % secure))
                del stanza['body']
            return stanza

        self.xmpp.add_filter('out_sce', out_sce)
        # make sure "out" filters still apply before sce
        self.xmpp.add_filter('out', out)

        m1 = self.Message()
        m1['body'] = 'Test 1'
        m1.send()
        # Check that the body was properly generated
        # base32 here is 'Test 1 fixed'
        # use_values is False because it is an ad-hoc element
        self.send("""
            <message>
                <secret>KRSXG5BAGEQGM2LYMVSA====</secret>
            </message>
        """, use_values=False)


suite = unittest.TestLoader().loadTestsFromTestCase(TestFilters)
