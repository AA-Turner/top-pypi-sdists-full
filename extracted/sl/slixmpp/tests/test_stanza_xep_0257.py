import unittest
from slixmpp.test import SlixTest
import slixmpp.plugins.xep_0257 as xep_0257


class TestSaslCertStanza(SlixTest):

    def setUp(self):
        xep_0257.stanza.register_plugins()

    def testAppend(self):
        append = """
            <iq type='set' from='toto@example' id='append'>
                <append xmlns='urn:xmpp:saslcert:1'>
                    <name>Mobile</name>
                    <x509cert>toto</x509cert>
                </append>
            </iq>
        """

        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'append'
        iq['from'] = 'toto@example'
        iq['sasl_cert_append']['name'] = 'Mobile'
        iq['sasl_cert_append']['x509cert'] = 'toto'

        self.check(iq, append)

    def testRevoke(self):
        revoke = """
            <iq type='set' from='toto@example' id='revoke'>
                <revoke xmlns='urn:xmpp:saslcert:1'>
                    <name>Mobile</name>
                </revoke >
            </iq>
        """

        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'revoke'
        iq['from'] = 'toto@example'
        iq['sasl_cert_revoke']['name'] = 'Mobile'

        self.check(iq, revoke)

    def testDisable(self):
        disable = """
            <iq type='set' from='toto@example' id='disable'>
                <disable xmlns='urn:xmpp:saslcert:1'>
                    <name>Mobile</name>
                </disable>
            </iq>
        """

        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'disable'
        iq['from'] = 'toto@example'
        iq['sasl_cert_disable']['name'] = 'Mobile'

        self.check(iq, disable)

    def testCertItems(self):
        result = """
        <iq type='result'
            to='toto@example'
            id='items'>
          <items xmlns='urn:xmpp:saslcert:1'>
            <item>
              <name>a</name>
              <x509cert>1</x509cert>
            </item>
            <item>
              <name>b</name>
              <x509cert>2</x509cert>
              <users>
                <resource>x</resource>
                <resource>y</resource>
              </users>
            </item>
          </items>
        </iq>
        """

        iq = self.Iq()
        iq['type'] = 'result'
        iq['id'] = 'items'
        iq['to'] = 'toto@example'
        for name, cert, users in (('a', '1', []), ('b', '2', ['x', 'y'])):
            item = xep_0257.stanza.CertItem()
            item['name'] = name
            item['x509cert'] = cert
            item['users'] = users
            iq['sasl_certs'].append(item)

        self.check(iq, result)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSaslCertStanza)
