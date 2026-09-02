from datetime import datetime

from eumdac.token import AccessToken
from eumdac.datastore import DataStore
from eumdac.product import Product
from .base import DataServiceTestCase


class TestProduct(DataServiceTestCase):
    collection_id = "EO:EUM:DAT:MSG:HRSEVIRI"
    product_id = "MSG4-SEVI-MSG15-0100-NA-20221010104242.601000000Z-NA"
    product_manifest = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<informationPackage xmlns="http://www.eumetsat.int/sip">
    <dataSection>
        <dataObject ID="MSG4-SEVI-MSG15-0100-NA-20221010104242.601000000Z-NA.nat">
            <fileType>Data</fileType>
            <format>Native</format>
            <size>271175723</size>
            <path>MSG4-SEVI-MSG15-0100-NA-20221010104242.601000000Z-NA.nat</path>
        </dataObject>
    </dataSection>
    <eopmetadataSection>
        <path>EOPMetadata.xml</path>
    </eopmetadataSection>
</informationPackage>
"""

    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datastore = DataStore(token=self.token)
        self.product = Product(self.collection_id, self.product_id, self.datastore)

    def test_string_representation(self):
        self.assertEqual(self.product_id, str(self.product))
        self.assertTrue(self.product_id in repr(self.product))

    def test_download_entry(self):
        with self.product.open("manifest.xml") as file:
            filename = file.name
            content = file.read()
        self.assertEqual(filename, "manifest.xml")
        self.assertEqual(content, self.product_manifest)

    def test_properties(self):
        collection = self.product.collection
        self.assertEqual(str(collection), self.collection_id)
        self.assertIsInstance(self.product.sensing_start, datetime)
        self.assertIsInstance(self.product.sensing_end, datetime)
        self.assertTrue(self.product.satellite.startswith("MSG"))
        self.assertEqual(self.product.instrument, "SEVIRI")
        self.assertIsInstance(self.product.size, int)
        self.assertIsInstance(self.product.metadata, dict)
        self.assertIn("properties", self.product.metadata)
        self.assertIn("manifest.xml", self.product.entries)
        self.assertIsInstance(self.product.acronym, str)
        self.assertIsInstance(self.product.product_type, str)
        self.assertEqual(self.product.product_type, self.product.acronym)
        self.assertEqual(self.product.timeliness, "NOMINAL")
        self.assertIsInstance(self.product.md5, str)
        self.assertIsInstance(self.product.processingTime, str)
        self.assertIsInstance(self.product.processorVersion, str)
        self.assertIsInstance(self.product.format, str)
        self.assertIsInstance(self.product.qualityStatus, str)
        self.assertIsInstance(self.product.ingested, datetime)
        self.assertIsInstance(self.product.orbit_type, str)
        self.assertIsInstance(self.product.orbit_is_LEO, bool)
        self.assertIsInstance(self.product.url, str)
        # These are none for GEO products
        self.assertIsNone(self.product.orbit_number)
        self.assertIsNone(self.product.orbit_direction)
        self.assertIsNone(self.product.relative_orbit)
        self.assertIsNone(self.product.cycle_number)

    def test_camparison(self):
        seviri_rss = Product(
            "EO:EUM:DAT:MSG:MSG15-RSS",
            "MSG2-SEVI-MSG15-0100-NA-20211013140918.098000000Z-NA",
            self.datastore,
        )
        avhrr_l1 = Product(
            "EO:EUM:DAT:METOP:AVHRRL1",
            "AVHR_xxx_1B_M01_20211014082503Z_20211014100403Z_N_O_20211014091048Z",
            self.datastore,
        )
        avhrr_l1_other = Product(
            "EO:EUM:DAT:METOP:AVHRRL1",
            "AVHR_xxx_1B_M01_20210206061303Z_20210206075503Z_N_O_20210206065931Z",
            self.datastore,
        )
        self.assertLess(avhrr_l1, seviri_rss)
        self.assertNotEqual(avhrr_l1, seviri_rss)
        self.assertLess(avhrr_l1_other, avhrr_l1)
        self.assertNotEqual(avhrr_l1_other, avhrr_l1)
