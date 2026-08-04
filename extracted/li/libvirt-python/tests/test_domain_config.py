import unittest
import libvirt


class TestLibvirtDomainAttributes(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testOSType(self):
        os_type = self.dom.OSType()
        self.assertIsInstance(os_type, str)
        self.assertEqual(os_type, "linux")

    def testHostname(self):
        hostname = self.dom.hostname()
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)

    def testSecurityLabel(self):
        label = self.dom.securityLabel()
        self.assertIsInstance(label, (list, tuple))
        self.assertEqual(len(label), 2)
        self.assertIsInstance(label[0], str)
        self.assertIsInstance(label[1], (bool, int))

    def testControlInfo(self):
        info = self.dom.controlInfo()
        self.assertIsInstance(info, (list, tuple))
        self.assertEqual(len(info), 3)
        for v in info:
            self.assertIsInstance(v, int)

    def testIsUpdated(self):
        result = self.dom.isUpdated()
        self.assertIsInstance(result, int)
        self.assertIn(result, [0, 1])

    def testHasManagedSaveImage(self):
        result = self.dom.hasManagedSaveImage()
        self.assertIsInstance(result, int)
        self.assertIn(result, [0, 1])

    def testGetTime(self):
        time_info = self.dom.getTime()
        self.assertIsInstance(time_info, dict)
        self.assertIn("seconds", time_info)
        self.assertIn("nseconds", time_info)
        self.assertIsInstance(time_info["seconds"], int)
        self.assertIsInstance(time_info["nseconds"], int)


class TestLibvirtDomainAutostart(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom.setAutostart(0)
        self.dom = None
        self.conn = None

    def testAutostartDefaultOff(self):
        self.assertEqual(self.dom.autostart(), 0)

    def testSetAutostartOn(self):
        self.dom.setAutostart(1)
        self.assertEqual(self.dom.autostart(), 1)

    def testSetAutostartOff(self):
        self.dom.setAutostart(1)
        self.assertEqual(self.dom.autostart(), 1)

        self.dom.setAutostart(0)
        self.assertEqual(self.dom.autostart(), 0)

    def testSetAutostartRoundTrip(self):
        original = self.dom.autostart()

        self.dom.setAutostart(1)
        self.assertEqual(self.dom.autostart(), 1)

        self.dom.setAutostart(0)
        self.assertEqual(self.dom.autostart(), 0)

        self.dom.setAutostart(original)
        self.assertEqual(self.dom.autostart(), original)


class TestLibvirtDomainScheduler(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        self.original_params = self.dom.schedulerParameters()

    def tearDown(self):
        self.dom.setSchedulerParameters(self.original_params)
        self.dom = None
        self.conn = None

    def testSchedulerType(self):
        sched_type, nparams = self.dom.schedulerType()
        self.assertIsInstance(sched_type, str)
        self.assertIsInstance(nparams, int)
        self.assertGreater(len(sched_type), 0)
        self.assertGreater(nparams, 0)

    def testSchedulerParametersReturnsDict(self):
        params = self.dom.schedulerParameters()
        self.assertIsInstance(params, dict)
        self.assertGreater(len(params), 0)
        self.assertIn("weight", params)

    def testSchedulerParametersRoundTrip(self):
        params = self.dom.schedulerParameters()
        original_weight = params["weight"]

        params["weight"] = 50
        ret = self.dom.setSchedulerParameters(params)
        self.assertEqual(ret, 0)

        updated = self.dom.schedulerParameters()
        self.assertEqual(updated["weight"], 50)

        params["weight"] = original_weight
        self.dom.setSchedulerParameters(params)


class TestLibvirtDomainMemory(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        if not self.dom.isActive():
            self.dom.create()

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testMaxMemory(self):
        max_mem = self.dom.maxMemory()
        self.assertIsInstance(max_mem, int)
        self.assertGreater(max_mem, 0)

    def testMemoryStats(self):
        stats = self.dom.memoryStats()
        self.assertIsInstance(stats, dict)
        self.assertIn("actual", stats)
        self.assertIsInstance(stats["actual"], int)
        self.assertGreater(stats["actual"], 0)

    def testMemoryParameters(self):
        params = self.dom.memoryParameters()
        self.assertIsInstance(params, dict)
        self.assertIn("hard_limit", params)
        self.assertIn("soft_limit", params)
        self.assertIn("swap_hard_limit", params)

    def testSetMemory(self):
        info = self.dom.info()
        original_mem = info[2]

        new_mem = 262144
        ret = self.dom.setMemory(new_mem)
        self.assertEqual(ret, 0)

        info = self.dom.info()
        self.assertEqual(info[2], new_mem)

        self.dom.setMemory(original_mem)

    def testSetMaxMemoryFailsOnActiveDomain(self):
        self.assertTrue(self.dom.isActive())
        with self.assertRaises(libvirt.libvirtError):
            self.dom.setMaxMemory(1048576)


class TestLibvirtDomainVcpus(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        if not self.dom.isActive():
            self.dom.create()

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testMaxVcpus(self):
        max_vcpus = self.dom.maxVcpus()
        self.assertIsInstance(max_vcpus, int)
        self.assertGreater(max_vcpus, 0)

    def testVcpusFlags(self):
        count = self.dom.vcpusFlags()
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def testVcpus(self):
        vcpu_info, vcpu_pinning = self.dom.vcpus()

        self.assertIsInstance(vcpu_info, (list, tuple))
        self.assertGreater(len(vcpu_info), 0)

        for entry in vcpu_info:
            self.assertEqual(len(entry), 4)
            vcpu_num, state, cpu_time, cpu = entry
            self.assertIsInstance(vcpu_num, int)
            self.assertIsInstance(state, int)
            self.assertIsInstance(cpu_time, int)
            self.assertIsInstance(cpu, int)

        self.assertIsInstance(vcpu_pinning, (list, tuple))
        self.assertEqual(len(vcpu_pinning), len(vcpu_info))

    def testVcpuPinInfo(self):
        pin_info = self.dom.vcpuPinInfo()
        self.assertIsInstance(pin_info, (list, tuple))
        self.assertGreater(len(pin_info), 0)

        for cpu_map in pin_info:
            self.assertIsInstance(cpu_map, (list, tuple))
            for pinned in cpu_map:
                self.assertIn(pinned, [True, False])

    def testSetVcpus(self):
        original = self.dom.vcpusFlags()
        ret = self.dom.setVcpus(1)
        self.assertEqual(ret, 0)

        self.assertEqual(self.dom.vcpusFlags(), 1)

        self.dom.setVcpus(original)

    def testEmulatorPinInfo(self):
        pin_info = self.dom.emulatorPinInfo()
        self.assertIsInstance(pin_info, (list, tuple))
        for pinned in pin_info:
            self.assertIn(pinned, [True, False])


class TestLibvirtDomainBlockAndNetwork(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        if not self.dom.isActive():
            self.dom.create()

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testBlockInfo(self):
        info = self.dom.blockInfo("vda")
        self.assertIsInstance(info, (list, tuple))
        self.assertEqual(len(info), 3)
        capacity, allocation, physical = info
        self.assertIsInstance(capacity, int)
        self.assertIsInstance(allocation, int)
        self.assertIsInstance(physical, int)
        self.assertGreater(capacity, 0)

    def testBlockStats(self):
        stats = self.dom.blockStats("vda")
        self.assertIsInstance(stats, (list, tuple))
        self.assertEqual(len(stats), 5)
        rd_req, rd_bytes, wr_req, wr_bytes, errors = stats
        for v in stats:
            self.assertIsInstance(v, int)
            self.assertGreaterEqual(v, 0)

    def testBlockInfoInvalidDisk(self):
        with self.assertRaises(libvirt.libvirtError):
            self.dom.blockInfo("nonexistent")

    def testInterfaceAddresses(self):
        addrs = self.dom.interfaceAddresses(0)
        self.assertIsInstance(addrs, dict)
        self.assertGreater(len(addrs), 0)

        for iface_name, iface_data in addrs.items():
            self.assertIsInstance(iface_name, str)
            self.assertIn("addrs", iface_data)
            self.assertIn("hwaddr", iface_data)
            self.assertIsInstance(iface_data["hwaddr"], str)

    def testInterfaceStatsInvalidInterface(self):
        with self.assertRaises(libvirt.libvirtError):
            self.dom.interfaceStats("nonexistent")


class TestLibvirtDomainCPUStats(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        if not self.dom.isActive():
            self.dom.create()

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testGetCPUStatsTotal(self):
        stats = self.dom.getCPUStats(True)
        self.assertIsInstance(stats, list)
        self.assertEqual(len(stats), 1)

        total = stats[0]
        self.assertIsInstance(total, dict)
        self.assertIn("cpu_time", total)
        self.assertIn("user_time", total)
        self.assertIn("system_time", total)

        for key in ("cpu_time", "user_time", "system_time"):
            self.assertIsInstance(total[key], int)
            self.assertGreaterEqual(total[key], 0)

    def testGetCPUStatsPerCpu(self):
        stats = self.dom.getCPUStats(False)
        self.assertIsInstance(stats, list)
        self.assertGreater(len(stats), 0)

        for cpu_stat in stats:
            self.assertIsInstance(cpu_stat, dict)
            self.assertIn("cpu_time", cpu_stat)
            self.assertIsInstance(cpu_stat["cpu_time"], int)


class TestLibvirtDomainSuspendResume(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")
        if not self.dom.isActive():
            self.dom.create()

    def tearDown(self):
        if self.dom.info()[0] == libvirt.VIR_DOMAIN_PAUSED:
            self.dom.resume()
        self.dom = None
        self.conn = None

    def testSuspend(self):
        ret = self.dom.suspend()
        self.assertEqual(ret, 0)

        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_PAUSED)

    def testResume(self):
        self.dom.suspend()
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_PAUSED)

        ret = self.dom.resume()
        self.assertEqual(ret, 0)

        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_RUNNING)

    def testSuspendResumeCycle(self):
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_RUNNING)

        self.dom.suspend()
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_PAUSED)

        self.dom.resume()
        state, _ = self.dom.state()
        self.assertEqual(state, libvirt.VIR_DOMAIN_RUNNING)


class TestLibvirtDomainMetadata(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        try:
            self.dom.setMetadata(
                libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None, None, None
            )
        except libvirt.libvirtError:
            pass
        self.dom = None
        self.conn = None

    def testSetAndGetDescription(self):
        desc = "test domain description"
        ret = self.dom.setMetadata(
            libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, desc, None, None
        )
        self.assertEqual(ret, 0)

        result = self.dom.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None)
        self.assertEqual(result, desc)

    def testMetadataNotFoundRaisesError(self):
        with self.assertRaises(libvirt.libvirtError):
            self.dom.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None)

    def testSetAndGetTitle(self):
        title = "My Test Domain"
        ret = self.dom.setMetadata(libvirt.VIR_DOMAIN_METADATA_TITLE, title, None, None)
        self.assertEqual(ret, 0)

        result = self.dom.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE, None)
        self.assertEqual(result, title)

    def testClearDescription(self):
        self.dom.setMetadata(
            libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, "temp", None, None
        )
        result = self.dom.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None)
        self.assertEqual(result, "temp")

        self.dom.setMetadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None, None, None)

        with self.assertRaises(libvirt.libvirtError):
            self.dom.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None)


class TestLibvirtDomainBlkioAndNuma(unittest.TestCase):

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    def testBlkioParameters(self):
        params = self.dom.blkioParameters()
        self.assertIsInstance(params, dict)
        self.assertIn("weight", params)
        self.assertIsInstance(params["weight"], int)

    def testNumaParameters(self):
        params = self.dom.numaParameters()
        self.assertIsInstance(params, dict)
        self.assertIn("numa_mode", params)
        self.assertIn("numa_nodeset", params)

    def testPerfEvents(self):
        events = self.dom.perfEvents()
        self.assertIsInstance(events, dict)
        for key, value in events.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, bool)


if __name__ == "__main__":
    unittest.main()
