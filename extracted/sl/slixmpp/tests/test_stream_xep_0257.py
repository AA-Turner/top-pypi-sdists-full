import unittest
from slixmpp.test import SlixTest


class TestStreamSaslCert(SlixTest):

    def test_get_certs(self):
        """
        Try fetching certs from a server.
        """
        self.stream_start(mode='client', plugins=['xep_0257'])

        fut = self.xmpp.wrap(self.xmpp.plugin['xep_0257'].get_certs())
        self.wait_()

        self.send("""
<iq type="get" id="1">
  <items xmlns='urn:xmpp:saslcert:1'/>
</iq>""")

        self.recv("""
<iq type='result'
    id='1'>
  <items xmlns='urn:xmpp:saslcert:1'>
    <item>
      <name>Mobile Client</name>
      <x509cert>cert 1</x509cert>
      <users>
        <resource>Phone</resource>
      </users>
    </item>
    <item>
      <name>Laptop</name>
      <x509cert>cert 2</x509cert>
    </item>
  </items>
</iq>
""")
        self.wait_()
        items = {
            ('Mobile Client', 'cert 1', ('Phone',)),
            ('Laptop', 'cert 2', tuple())
        }

        self.assertEqual(fut.result(), items)

    def test_add_cert(self):
        """Try adding a new cert"""
        self.stream_start(mode='client', plugins=['xep_0257'])

        if self.xmpp is None:
            self.assertTrue(False)
            return
        fut = self.xmpp.wrap(
            self.xmpp.plugin['xep_0257'].add_cert(
                name="toto", cert="my very real cert", allow_management=False
            )
        )
        self.wait_()
        self.send("""
<iq type="set" id="1">
  <append xmlns='urn:xmpp:saslcert:1'>
    <name>toto</name>
    <no-cert-management/>
    <x509cert>my very real cert</x509cert>
  </append>
</iq>""")

        self.recv("""
<iq type='result'
    id='1' />
""")
        iq = self.Iq()
        iq['id'] = '1'
        iq['type'] = 'result'

        self.wait_()
        self.assertEqual(fut.result(), iq)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamSaslCert)
