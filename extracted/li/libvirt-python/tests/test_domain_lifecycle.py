import unittest
import uuid
import libvirt


class TestLibvirtDomainLifecycle(unittest.TestCase):
    """Domain lifecycle operations test coverage"""

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testDomainStateReturnsValidTuple(self):
        """check state() returns values"""
        state_info = self.dom.state()

        self.assertIsInstance(state_info, (tuple, list))
        self.assertEqual(len(state_info), 2)

        state, reason = state_info
        self.assertIsInstance(state, int)
        self.assertIsInstance(reason, int)

        self.assertGreaterEqual(state, 0)
        self.assertLessEqual(state, 7)

    def testDomainIsActiveReturnsBool(self):
        """test if isActive() returns a boolean value"""
        result = self.dom.isActive()
        self.assertIsInstance(result, (bool, int))
        self.assertIn(result, [0, 1, True, False])

    def testDomainIsPersistentReturnsBool(self):
        result = self.dom.isPersistent()
        self.assertIsInstance(result, (bool, int))
        self.assertIn(result, [0, 1, True, False])

    # domain info tests
    def testDomainInfoReturnsValidTuple(self):
        """check info() returns value, 5-tuple with types"""
        info = self.dom.info()

        # expected tuple of (state, maxMem, memory, nrVirtCpu, cpuTime)
        self.assertIsInstance(info, (tuple, list))
        self.assertEqual(len(info), 5)

        state, maxMem, memory, nrVirtCpu, cpuTime = info

        self.assertIsInstance(state, int)
        self.assertIsInstance(maxMem, int)
        self.assertIsInstance(memory, int)
        self.assertIsInstance(nrVirtCpu, int)
        self.assertIsInstance(cpuTime, int)

        self.assertGreaterEqual(state, 0)
        self.assertGreater(maxMem, 0)
        self.assertGreater(memory, 0)
        self.assertGreater(nrVirtCpu, 0)
        self.assertGreaterEqual(cpuTime, 0)

    def testDomainNameReturnsString(self):
        name = self.dom.name()

        self.assertIsInstance(name, str)
        self.assertEqual(name, "test")
        self.assertGreater(len(name), 0)

    def testDomainUUIDStringReturnsValidFormat(self):
        uuid_str = self.dom.UUIDString()

        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)

        try:
            uuid_obj = uuid.UUID(uuid_str)
            self.assertEqual(str(uuid_obj), uuid_str)
        except ValueError:
            self.fail(f"Invalid UUID format: {uuid_str}")

    def testDomainIDReturnsValidValue(self):
        dom_id = self.dom.ID()

        # In test:///default driver, the test domain is always active with ID >= 0
        self.assertIsInstance(dom_id, int)
        self.assertGreaterEqual(dom_id, 0)

    # domain control tests
    def testDomainCreateDestroyCycle(self):
        if self.dom.isActive():
            ret = self.dom.destroy()
            self.assertEqual(ret, 0)
        self.assertFalse(self.dom.isActive())

        ret = self.dom.create()
        self.assertEqual(ret, 0)

        # is the domain active now?
        self.assertTrue(self.dom.isActive())
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_RUNNING)

        ret = self.dom.destroy()
        self.assertEqual(ret, 0)

        # is the domain inactive now?
        self.assertFalse(self.dom.isActive())

    def testDomainDestroyWhenInactive(self):
        """Test that destroying an inactive domain raises an error."""
        if self.dom.isActive():
            self.dom.destroy()

        # try destroy already inactive domain, expected: libvirt.libvirtError
        with self.assertRaises(libvirt.libvirtError):
            self.dom.destroy()

    def testDomainCreateWhenActive(self):
        if not self.dom.isActive():
            self.dom.create()

        with self.assertRaises(libvirt.libvirtError):
            self.dom.create()

        self.dom.destroy()

    def testDomainShutdown(self):
        """We can't verify the domain is actually shut down because shutdown
        asynchronous nature of shutdown()
        """
        if not self.dom.isActive():
            self.dom.create()

        ret = self.dom.shutdown()
        self.assertEqual(ret, 0)

        if self.dom.isActive():
            self.dom.destroy()

    def testDomainReboot(self):
        """Test reboot() sends reboot request."""
        if not self.dom.isActive():
            self.dom.create()

        # test:///default driver supports reboot
        ret = self.dom.reboot(0)
        self.assertEqual(ret, 0)

        if self.dom.isActive():
            self.dom.destroy()

    # test fomain states
    def testDomainStateWithIsActive(self):
        if self.dom.isActive():
            self.dom.destroy()

        self.assertFalse(self.dom.isActive())
        state, _ = self.dom.state()
        self.assertIn(state, [libvirt.VIR_DOMAIN_SHUTOFF, libvirt.VIR_DOMAIN_SHUTDOWN])

        self.dom.create()
        self.assertTrue(self.dom.isActive())
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_RUNNING)

        self.dom.destroy()

    def testDomainInfoStateConsistentWithState(self):
        """check if info()[0] matches state()[0]"""
        state_from_state, _ = self.dom.state()
        state_from_info = self.dom.info()[0]

        self.assertEqual(state_from_state, state_from_info)

    # domain ID tests
    def testDomainIDChangesWithActivation(self):
        """domain ID changes from -1 when domain becomes active
        expected states are as follow: -1 -> id>0 -> -1
        """
        if self.dom.isActive():
            self.dom.destroy()

        self.assertEqual(self.dom.ID(), -1)

        self.dom.create()
        self.assertGreaterEqual(self.dom.ID(), 0)

        self.dom.destroy()
        self.assertEqual(self.dom.ID(), -1)


class TestLibvirtDomainPersistence(unittest.TestCase):
    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        self.dom_xml = self.dom.XMLDesc(0)

    def tearDown(self):
        try:
            self.conn.lookupByName("test")
        except libvirt.libvirtError:
            self.conn.defineXML(self.dom_xml)

        self.dom = None
        self.conn = None

    def testDomainIsPersistent(self):
        self.assertTrue(self.dom.isPersistent())

    def testDomainXMLDescReturnsValidXML(self):
        """check if XMLDesc() returns valid XML string"""
        xml = self.dom.XMLDesc(0)

        self.assertIsInstance(xml, str)
        self.assertGreater(len(xml), 0)

        self.assertIn("<domain", xml)
        self.assertIn("</domain>", xml)
        self.assertIn("test", xml)

    def testDomainUndefineRemovesPersistence(self):
        """this test modifies the test domain, but tearDown will restore
        it to original state
        """

        if self.dom.isActive():
            self.dom.destroy()

        ret = self.dom.undefine()
        self.assertEqual(ret, 0)

        # domain should no longer be found by name
        with self.assertRaises(libvirt.libvirtError):
            self.conn.lookupByName("test")

    def testDomainDefineCreatesDefinition(self):
        """create domain from XML and check its persistance"""
        new_dom_xml = """
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

        new_dom = self.conn.defineXML(new_dom_xml)
        self.assertIsNotNone(new_dom)
        self.assertEqual(new_dom.name(), "test-define-temp")
        self.assertTrue(new_dom.isPersistent())

        self.assertFalse(new_dom.isActive())

        new_dom.undefine()


class TestLibvirtDomainLookup(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testLookupDomainByName(self):
        dom = self.conn.lookupByName("test")

        self.assertIsNotNone(dom)
        self.assertEqual(dom.name(), "test")
        self.assertIsInstance(dom, libvirt.virDomain)

    def testLookupByNameWithInvalidName(self):
        with self.assertRaises(libvirt.libvirtError) as ctx:
            self.conn.lookupByName("nonexistent-domain-12345")
        err = ctx.exception
        self.assertIsNotNone(err)

    def testLookupDomainByUUID(self):
        """libvirt C API function virDomainLookupByUUID() expects a raw 16-byte UUID,
        not a UUID string. UUIDs are 128 bits = 16 bytes after '-' removal.
        """
        uuid_str = self.dom.UUIDString()

        # convert UUID string to bytes (16 bytes)
        uuid_bytes = bytes.fromhex(uuid_str.replace("-", ""))

        dom = self.conn.lookupByUUID(uuid_bytes)
        self.assertIsNotNone(dom)
        self.assertEqual(dom.name(), "test")
        self.assertEqual(dom.UUIDString(), uuid_str)

    def testLookupDomainByUUIDString(self):
        uuid_str = self.dom.UUIDString()

        dom = self.conn.lookupByUUIDString(uuid_str)
        self.assertIsNotNone(dom)
        self.assertEqual(dom.name(), "test")
        self.assertEqual(dom.UUIDString(), uuid_str)

    def testLookupDomainByID(self):
        if not self.dom.isActive():
            self.dom.create()

        dom_id = self.dom.ID()
        self.assertGreaterEqual(dom_id, 0)

        dom = self.conn.lookupByID(dom_id)
        self.assertIsNotNone(dom)
        self.assertEqual(dom.name(), "test")
        self.assertEqual(dom.ID(), dom_id)

        if self.dom.isActive():
            self.dom.destroy()

    def testLookupByIDForInactiveDomain(self):
        """lookupByID() should fail for inactive domain"""
        if self.dom.isActive():
            self.dom.destroy()

        # expected -1 for inactive domain
        self.assertEqual(self.dom.ID(), -1)

        # cannot lookup by ID=-1
        with self.assertRaises(libvirt.libvirtError):
            self.conn.lookupByID(-1)


class TestLibvirtDomainListOperations(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")

    def tearDown(self):
        self.conn = None

    def testListAllDomainsReturnsList(self):
        domains = self.conn.listAllDomains()

        self.assertIsInstance(domains, list)
        self.assertGreater(len(domains), 0)

        # all items should be virDomain type objects
        for dom in domains:
            self.assertIsInstance(dom, libvirt.virDomain)
            self.assertIsInstance(dom.name(), str)

    def testListAllDomains(self):
        """it is expected that "test" domain will be within the list"""
        domains = self.conn.listAllDomains()
        names = [dom.name() for dom in domains]

        self.assertIn("test", names)

    def testListAllActiveDomains(self):
        dom = self.conn.lookupByName("test")

        if not dom.isActive():
            dom.create()

        # list only active domains
        active_domains = self.conn.listAllDomains(
            libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE
        )

        self.assertIsInstance(active_domains, list)
        self.assertGreater(len(active_domains), 0)

        for d in active_domains:
            self.assertTrue(d.isActive())

        names = [d.name() for d in active_domains]
        self.assertIn("test", names)

        if dom.isActive():
            dom.destroy()

    def testListAllInactiveDomains(self):
        dom = self.conn.lookupByName("test")

        if dom.isActive():
            dom.destroy()

        # list only inactive domains
        inactive_domains = self.conn.listAllDomains(
            libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE
        )

        self.assertIsInstance(inactive_domains, list)
        self.assertGreater(len(inactive_domains), 0)

        for d in inactive_domains:
            self.assertFalse(d.isActive())

        names = [d.name() for d in inactive_domains]
        self.assertIn("test", names)

    def testListAllPersistentDomains(self):
        persistent_domains = self.conn.listAllDomains(
            libvirt.VIR_CONNECT_LIST_DOMAINS_PERSISTENT
        )

        self.assertIsInstance(persistent_domains, list)
        self.assertGreater(len(persistent_domains), 0)

        for d in persistent_domains:
            self.assertTrue(d.isPersistent())

        names = [d.name() for d in persistent_domains]
        self.assertIn("test", names)


if __name__ == "__main__":
    unittest.main()
