#!/usr/bin/env python

"""Tests for `acdh_xml_pyutils.xml` module."""

import glob
import os
import unittest

import collections

from acdh_xml_pyutils.xml import XMLReader

FILES = glob.glob("./acdh_xml_pyutils/files/*.xml", recursive=False)

# XML_URL = "https://id.acdh.oeaw.ac.at/thun/editions/szeberinyi-an-thun-1859-11-29-a3-xxi-d529.xml?format=raw"

XML_URLS = [
    "https://raw.githubusercontent.com/KONDE-AT/thun-data/master/editions/ansichten-ueber-waisenvermoegen-von-walter-1857-08-22-a3-xxi-d430.xml",  # noqa: E501
    "http://gams.uni-graz.at/o:aled.1/TEI_SOURCE",
]

XML_STRINGS = [
    """
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <p>Some text here.</p>
      </body>
  </text>
</TEI>
""",
    """<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <p>Some text here.</p>
      </body>
  </text>
</TEI>
""",
]

DEFAULT_XSL = os.path.join(os.path.dirname(__file__), "test.xsl")


class TestAcdh_xml_pyutils(unittest.TestCase):
    """Tests for `acdh_xml_pyutils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""
        for x in glob.glob("./*.xml"):
            os.remove(x)

    def test_001_parse_from_file(self):
        for x in FILES:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_002_parse_from_url(self):
        for x in XML_URLS:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_003_parse_str(self):
        for x in XML_STRINGS:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_004_parse_all(self):
        items = XML_URLS + XML_STRINGS + FILES
        for x in items:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.return_string(), str)
            self.assertIsInstance(doc.return_byte_like_object(), bytes)

    def test_004_write_to_file(self):
        doc = XMLReader(xml=XML_STRINGS[0])
        res = doc.tree_to_file()
        self.assertTrue(res.startswith("2"))
        self.assertTrue(res.endswith(".xml"))
        self.assertTrue(os.path.isfile(res))
        os.remove(res)
        res = doc.tree_to_file(file="hansi.xml")
        self.assertTrue(res.startswith("hansi"))
        self.assertTrue(res.endswith(".xml"))
        self.assertTrue(os.path.isfile(res))
        os.remove(res)

    def test_004a_without_declaration(self):
        doc = XMLReader(xml=XML_STRINGS[0])
        res = doc.tree_to_file()
        res = doc.tree_to_file(file="hansi.xml", xml_declaration=False)
        with open(res, "r") as f:
            text = f.read()
            self.assertTrue(text.startswith("<TEI"))
        os.remove(res)
        res = doc.tree_to_file(file="hansi.xml")
        with open(res, "r") as f:
            text = f.read()
            self.assertTrue(text.startswith("<?xml"))
        os.remove(res)

    def test_005_get_elements(self):
        doc = XMLReader(xml=XML_STRINGS[0])
        els = doc.get_elements()
        self.assertIsInstance(els, list)

    def test_006_get_element_stats(self):
        doc = XMLReader(xml=XML_STRINGS[0])
        els = doc.get_element_stats()
        self.assertIsInstance(els, collections.Counter)
        self.assertTrue("{http://www.tei-c.org/ns/1.0}TEI" in els.keys())

    def test_007_transform(self):
        doc = XMLReader(xml=XML_STRINGS[0], xsl=DEFAULT_XSL)
        els = doc.get_elements()
        self.assertTrue("{http://www.tei-c.org/ns/1.0}hansi" in els)
