import libvirt
import unittest

from unittest.mock import patch, MagicMock


class TestLibvirtDomainMigrationMocked(unittest.TestCase):
    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3LiveMigrationSuccess(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        # A small hack to make virDomainFree work with mocked objects,
        # the same applies to all tests in this set that return a domain pointer.
        # Transfer ownership of the raw C pointer to the mock return value by
        # setting _o to None so dst_dom.__del__ won't also call virDomainFree on it.
        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        params = {
            libvirt.VIR_MIGRATE_PARAM_URI: "qemu+ssh://desthost/system",
            libvirt.VIR_MIGRATE_PARAM_BANDWIDTH: 1024,
        }
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PERSIST_DEST

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)

        mock_migrate3.assert_called_once()
        call_args = mock_migrate3.call_args
        self.assertEqual(call_args[0][0], self.dom._o)
        self.assertEqual(call_args[0][1], dst_conn._o)
        self.assertEqual(call_args[0][3], flags)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrateToURI3")
    def testMigrateToURI3PeerToPeerSuccess(self, mock_migrateToURI3):
        mock_migrateToURI3.return_value = 0

        dest_uri = "qemu+ssh://desthost/system"
        params = {
            libvirt.VIR_MIGRATE_PARAM_BANDWIDTH: 2048,
            libvirt.VIR_MIGRATE_PARAM_DEST_NAME: "migrated-vm",
        }
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PEER2PEER

        result = self.dom.migrateToURI3(dest_uri, params, flags)

        self.assertEqual(result, 0)

        mock_migrateToURI3.assert_called_once()
        call_args = mock_migrateToURI3.call_args
        self.assertEqual(call_args[0][0], self.dom._o)
        self.assertEqual(call_args[0][1], dest_uri)
        self.assertEqual(call_args[0][3], flags)

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3OfflineMigration(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        # domain must be inactive
        if self.dom.isActive():
            self.dom.destroy()

        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        params = {}
        flags = libvirt.VIR_MIGRATE_OFFLINE | libvirt.VIR_MIGRATE_PERSIST_DEST

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)
        call_args = mock_migrate3.call_args
        self.assertTrue(call_args[0][3] & libvirt.VIR_MIGRATE_OFFLINE)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3WithCompressionParameters(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        params = {
            libvirt.VIR_MIGRATE_PARAM_BANDWIDTH: 1024,
            libvirt.VIR_MIGRATE_PARAM_COMPRESSION: "mt",
            libvirt.VIR_MIGRATE_PARAM_COMPRESSION_MT_LEVEL: 9,
            libvirt.VIR_MIGRATE_PARAM_COMPRESSION_MT_THREADS: 4,
            libvirt.VIR_MIGRATE_PARAM_COMPRESSION_MT_DTHREADS: 2,
        }
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_COMPRESSED

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)
        mock_migrate3.assert_called_once()
        call_args = mock_migrate3.call_args
        self.assertTrue(call_args[0][3] & libvirt.VIR_MIGRATE_COMPRESSED)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrateToURI3")
    def testMigrateToURI3WithAutoConverge(self, mock_migrateToURI3):
        mock_migrateToURI3.return_value = 0

        params = {
            libvirt.VIR_MIGRATE_PARAM_AUTO_CONVERGE_INITIAL: 20,
            libvirt.VIR_MIGRATE_PARAM_AUTO_CONVERGE_INCREMENT: 10,
        }
        flags = (
            libvirt.VIR_MIGRATE_LIVE
            | libvirt.VIR_MIGRATE_PEER2PEER
            | libvirt.VIR_MIGRATE_AUTO_CONVERGE
        )

        result = self.dom.migrateToURI3("qemu+ssh://dest/system", params, flags)

        self.assertEqual(result, 0)
        mock_migrateToURI3.assert_called_once()
        call_args = mock_migrateToURI3.call_args
        self.assertTrue(call_args[0][3] & libvirt.VIR_MIGRATE_AUTO_CONVERGE)

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3WithTLSParameters(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        params = {
            libvirt.VIR_MIGRATE_PARAM_URI: "qemu+ssh://desthost/system",
            libvirt.VIR_MIGRATE_PARAM_TLS_DESTINATION: "desthost.example.com",
        }
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_TLS

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)
        call_args = mock_migrate3.call_args
        self.assertTrue(call_args[0][3] & libvirt.VIR_MIGRATE_TLS)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrateToURI3")
    def testMigrateToURI3WithParallelConnections(self, mock_migrateToURI3):
        mock_migrateToURI3.return_value = 0

        params = {
            libvirt.VIR_MIGRATE_PARAM_PARALLEL_CONNECTIONS: 4,
            libvirt.VIR_MIGRATE_PARAM_BANDWIDTH: 4096,
        }
        flags = (
            libvirt.VIR_MIGRATE_LIVE
            | libvirt.VIR_MIGRATE_PEER2PEER
            | libvirt.VIR_MIGRATE_PARALLEL
        )

        result = self.dom.migrateToURI3("qemu+ssh://dest/system", params, flags)

        self.assertEqual(result, 0)

        call_args = mock_migrateToURI3.call_args
        self.assertTrue(call_args[0][3] & libvirt.VIR_MIGRATE_PARALLEL)

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3EmptyParameterDict(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        # Empty params dict
        params = {}
        flags = libvirt.VIR_MIGRATE_LIVE

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)
        mock_migrate3.assert_called_once()

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3MultipleFlags(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate3.return_value = dst_dom._o
        dst_dom._o = None

        params = {
            libvirt.VIR_MIGRATE_PARAM_BANDWIDTH: 1024,
        }

        flags = (
            libvirt.VIR_MIGRATE_LIVE
            | libvirt.VIR_MIGRATE_PERSIST_DEST
            | libvirt.VIR_MIGRATE_UNDEFINE_SOURCE
            | libvirt.VIR_MIGRATE_COMPRESSED
            | libvirt.VIR_MIGRATE_AUTO_CONVERGE
        )

        result = self.dom.migrate3(dst_conn, params, flags)

        self.assertIsInstance(result, libvirt.virDomain)

        call_args = mock_migrate3.call_args
        passed_flags = call_args[0][3]
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_LIVE)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_PERSIST_DEST)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_UNDEFINE_SOURCE)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_COMPRESSED)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_AUTO_CONVERGE)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate3")
    def testMigrate3Failure(self, mock_migrate3):
        dst_conn = libvirt.open("test:///default")

        mock_migrate3.return_value = None

        params = {}
        flags = libvirt.VIR_MIGRATE_LIVE

        # raise exception when C layer returns None
        with self.assertRaises(libvirt.libvirtError) as ctx:
            self.dom.migrate3(dst_conn, params, flags)

        self.assertIn("virDomainMigrate3() failed", str(ctx.exception))

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrateToURI3")
    def testMigrateToURI3Failure(self, mock_migrateToURI3):
        mock_migrateToURI3.return_value = -1

        params = {}
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PEER2PEER

        # raise exception on failure
        with self.assertRaises(libvirt.libvirtError):
            self.dom.migrateToURI3("qemu+ssh://dest/system", params, flags)


class TestLibvirtDomainMigrateLegacyMocked(unittest.TestCase):
    """Tests for the legacy virDomainMigrate and virDomainMigrate2 APIs.

    Both virDomainMigrate and virDomainMigrate2 call independent C functionas
    (libvirtmod.virDomainMigrate and libvirtmod.virDomainMigrate2) and have
    their own wrapping logic, so they are tested separately from migrate3.
    """

    def setUp(self):
        self.conn = libvirt.open("test:///default")
        self.dom = self.conn.lookupByName("test")

    def tearDown(self):
        self.dom = None
        self.conn = None

    @patch("libvirtmod.virDomainMigrate")
    def testMigrateSuccess(self, mock_migrate):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate.return_value = dst_dom._o
        dst_dom._o = None

        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PERSIST_DEST
        result = self.dom.migrate(dst_conn, flags, dname="migrated-vm",
                                  uri="qemu+ssh://desthost/system", bandwidth=1024)

        self.assertIsInstance(result, libvirt.virDomain)
        mock_migrate.assert_called_once()
        call_args = mock_migrate.call_args
        self.assertEqual(call_args[0][0], self.dom._o)
        self.assertEqual(call_args[0][1], dst_conn._o)
        self.assertEqual(call_args[0][2], flags)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate")
    def testMigrateWithFlags(self, mock_migrate):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate.return_value = dst_dom._o
        dst_dom._o = None

        flags = (
            libvirt.VIR_MIGRATE_LIVE
            | libvirt.VIR_MIGRATE_PERSIST_DEST
            | libvirt.VIR_MIGRATE_UNDEFINE_SOURCE
        )
        result = self.dom.migrate(dst_conn, flags)

        self.assertIsInstance(result, libvirt.virDomain)
        call_args = mock_migrate.call_args
        passed_flags = call_args[0][2]
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_LIVE)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_PERSIST_DEST)
        self.assertTrue(passed_flags & libvirt.VIR_MIGRATE_UNDEFINE_SOURCE)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate")
    def testMigrateFailure(self, mock_migrate):
        dst_conn = libvirt.open("test:///default")

        mock_migrate.return_value = None

        with self.assertRaises(libvirt.libvirtError) as ctx:
            self.dom.migrate(dst_conn, libvirt.VIR_MIGRATE_LIVE)

        self.assertIn("virDomainMigrate() failed", str(ctx.exception))

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate2")
    def testMigrate2Success(self, mock_migrate2):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate2.return_value = dst_dom._o
        dst_dom._o = None

        dxml = "<domain type='test'><name>migrated-vm</name></domain>"
        flags = libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PERSIST_DEST
        result = self.dom.migrate2(dst_conn, dxml=dxml, flags=flags,
                                   dname="migrated-vm")

        self.assertIsInstance(result, libvirt.virDomain)
        mock_migrate2.assert_called_once()
        call_args = mock_migrate2.call_args
        self.assertEqual(call_args[0][0], self.dom._o)
        self.assertEqual(call_args[0][1], dst_conn._o)
        self.assertEqual(call_args[0][2], dxml)
        self.assertEqual(call_args[0][3], flags)

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate2")
    def testMigrate2WithoutXML(self, mock_migrate2):
        dst_conn = libvirt.open("test:///default")
        dst_dom = dst_conn.lookupByName("test")

        mock_migrate2.return_value = dst_dom._o
        dst_dom._o = None

        flags = libvirt.VIR_MIGRATE_LIVE
        result = self.dom.migrate2(dst_conn, flags=flags)

        self.assertIsInstance(result, libvirt.virDomain)
        call_args = mock_migrate2.call_args
        self.assertIsNone(call_args[0][2])

        dst_conn.close()

    @patch("libvirtmod.virDomainMigrate2")
    def testMigrate2Failure(self, mock_migrate2):
        dst_conn = libvirt.open("test:///default")

        mock_migrate2.return_value = None

        with self.assertRaises(libvirt.libvirtError) as ctx:
            self.dom.migrate2(dst_conn, flags=libvirt.VIR_MIGRATE_LIVE)

        self.assertIn("virDomainMigrate2() failed", str(ctx.exception))

        dst_conn.close()


if __name__ == "__main__":
    unittest.main()
