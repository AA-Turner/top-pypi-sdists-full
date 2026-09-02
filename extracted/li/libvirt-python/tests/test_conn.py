import unittest
import libvirt
import tempfile
import contextlib
import os


class TestLibvirtConn(unittest.TestCase):
    def setUp(self):
        self.conn = libvirt.open("test:///default")

    def tearDown(self):
        self.conn = None

    def testConnDomainList(self):
        doms = self.conn.listAllDomains()
        self.assertEqual(len(doms), 1)
        self.assertEqual(type(doms[0]), libvirt.virDomain)
        self.assertEqual(doms[0].name(), "test")


class TestLibvirtConnMetadata(unittest.TestCase):
    """Connection metadata and lifecycle tests"""

    def setUp(self):
        self.conn = libvirt.open("test:///default")

    def tearDown(self):
        self.conn = None

    def testConnGetURI(self):
        uri = self.conn.getURI()

        self.assertIsInstance(uri, str)
        self.assertEqual(uri, "test:///default")

    def testConnGetHostname(self):
        hostname = self.conn.getHostname()

        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)

    def testConnGetLibVersion(self):
        version = self.conn.getLibVersion()

        self.assertIsInstance(version, int)
        self.assertGreater(version, 0)

    def testConnGetVersion(self):
        """test driver reports hypervisor version 2"""
        version = self.conn.getVersion()

        self.assertIsInstance(version, int)
        self.assertEqual(version, 2)

    def testConnGetType(self):
        """test driver reports type TEST"""
        hv_type = self.conn.getType()

        self.assertIsInstance(hv_type, str)
        self.assertEqual(hv_type, "TEST")

    def testConnIsAlive(self):
        self.assertTrue(self.conn.isAlive())

    def testConnIsEncrypted(self):
        result = self.conn.isEncrypted()

        self.assertIsInstance(result, (bool, int))
        self.assertFalse(result)

    def testConnIsSecure(self):
        result = self.conn.isSecure()

        self.assertIsInstance(result, (bool, int))
        self.assertTrue(result)

    def testConnClose(self):
        self.assertTrue(self.conn.isAlive())

        ret = self.conn.close()
        self.assertEqual(ret, 0)

        with self.assertRaises(libvirt.libvirtError):
            self.conn.isAlive()

    def testConnContextManager(self):
        with libvirt.open("test:///default") as conn:
            self.assertEqual(conn.getURI(), "test:///default")
            self.assertTrue(conn.isAlive())

        with self.assertRaises(libvirt.libvirtError):
            conn.isAlive()


class TestLibvirtConnOpenNegative(unittest.TestCase):
    """Connection open failure for an invalid URI"""

    def testOpenFails(self):
        with self.assertRaises(libvirt.libvirtError) as ctx:
            libvirt.open("not-a-valid-libvirt-uri")

        self.assertIsNotNone(ctx.exception.get_error_message())


class TestLibvirtConnReadOnly(unittest.TestCase):
    """Read-only libvirt.openReadOnly() connection tests"""

    DEFINE_XML = """
        <domain type='test'>
          <name>test-define-temp</name>
          <uuid>12345678-1234-1234-1234-123456789abc</uuid>
          <memory unit='KiB'>524288</memory>
          <vcpu>1</vcpu>
          <os>
            <type>hvm</type>
          </os>
        </domain>
        """

    def setUp(self):
        self.conn = libvirt.openReadOnly("test:///default")

    def tearDown(self):
        self.conn = None

    def testOpenReadOnlySucceeds(self):
        self.assertIsNotNone(self.conn)
        self.assertTrue(self.conn.isAlive())

    def testReadOnlyGetURI(self):
        self.assertEqual(self.conn.getURI(), "test:///default")

    def testReadOnlyGetType(self):
        self.assertEqual(self.conn.getType(), "TEST")

    def testReadOnlyListDomains(self):
        domains = self.conn.listAllDomains()

        self.assertIsInstance(domains, list)
        self.assertGreater(len(domains), 0)
        self.assertIsInstance(domains[0], libvirt.virDomain)

    def testReadOnlyLookupAndInfo(self):
        dom = self.conn.lookupByName("test")

        self.assertEqual(dom.name(), "test")

        info = dom.info()
        self.assertIsInstance(info, (tuple, list))
        self.assertEqual(len(info), 5)

        state, _ = dom.state()
        self.assertIsInstance(state, int)

    def testReadOnlyXMLDesc(self):
        dom = self.conn.lookupByName("test")
        xml = dom.XMLDesc(0)

        self.assertIsInstance(xml, str)
        self.assertIn("<domain", xml)

    def testReadOnlyDefineXMLDenied(self):
        with self.assertRaises(libvirt.libvirtError) as ctx:
            self.conn.defineXML(self.DEFINE_XML)

        self.assertEqual(ctx.exception.get_error_code(),
                         libvirt.VIR_ERR_OPERATION_DENIED)

    def testReadOnlyDestroyDenied(self):
        dom = self.conn.lookupByName("test")

        with self.assertRaises(libvirt.libvirtError) as ctx:
            dom.destroy()

        self.assertEqual(ctx.exception.get_error_code(),
                         libvirt.VIR_ERR_OPERATION_DENIED)

    def testReadOnlyXMLDescSecureDenied(self):
        dom = self.conn.lookupByName("test")

        with self.assertRaises(libvirt.libvirtError) as ctx:
            dom.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)

        self.assertEqual(ctx.exception.get_error_code(),
                         libvirt.VIR_ERR_OPERATION_DENIED)

    def testReadOnlyContextManager(self):
        with libvirt.openReadOnly("test:///default") as conn:
            self.assertEqual(conn.getURI(), "test:///default")
            self.assertTrue(conn.isAlive())

        with self.assertRaises(libvirt.libvirtError):
            conn.isAlive()


class TestLibvirtConnAuth(unittest.TestCase):
    connXML = """
<node>
  <auth>
    <user password="2147483647">marin</user>
    <user password="87539319">srinivasa</user>
  </auth>
</node>"""
    def setUp(self):
        def noop(msg, opaque):
            pass
        libvirt.registerErrorHandler(noop, None)

    @contextlib.contextmanager
    def tempxmlfile(content):
        try:
            fp = tempfile.NamedTemporaryFile(delete=False,
                                             prefix="libvirt-python-test",
                                             suffix=".xml")
            fname = fp.name
            fp.write(content.encode("utf8"))
            fp.close()
            yield fname
        finally:
            os.unlink(fname)

    def authHelper(self, username, password):
        with TestLibvirtConnAuth.tempxmlfile(self.connXML) as fname:
            magic = 142857
            def authCB(creds, opaque):
                if opaque != magic:
                    return -1

                for cred in creds:
                    if (cred[0] == libvirt.VIR_CRED_AUTHNAME and
                        username is not None):
                        cred[4] = username
                        return 0
                    elif (cred[0] == libvirt.VIR_CRED_PASSPHRASE and
                          password is not None):
                        cred[4] = password
                        return 0
                    return -1
                return 0

            auth = [[libvirt.VIR_CRED_AUTHNAME,
                     libvirt.VIR_CRED_ECHOPROMPT,
                     libvirt.VIR_CRED_REALM,
                     libvirt.VIR_CRED_PASSPHRASE,
                     libvirt.VIR_CRED_NOECHOPROMPT,
                     libvirt.VIR_CRED_EXTERNAL],
                    authCB, magic]

            return libvirt.openAuth("test://" + fname,
                                    auth, 0)

    def testOpenAuthGood(self):
        conn = self.authHelper("srinivasa", "87539319")

    def testOpenAuthBad(self):
        try:
            conn = self.authHelper("srinivasa", "2147483647")
            raise Exception("Unexpected open success")
        except libvirt.libvirtError as ex:
            pass

    def testOpenAuthNone(self):
        try:
            conn = self.authHelper(None, None)
            raise Exception("Unexpected open success")
        except libvirt.libvirtError as ex:
            pass
