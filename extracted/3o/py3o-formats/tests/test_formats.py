__author__ = 'faide'

import unittest

from nose.tools import raises

from py3o.formats import UnkownFormatException
from py3o.formats import Formats
from py3o.formats import Format
from py3o.formats import FORMAT_PDF


class TestFormats(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        self.formats = Formats()

    def test_valid_format(self):
        """test that a valid format can be found"""
        res = self.formats.get_format(FORMAT_PDF)
        assert isinstance(res, Format)

        assert res.name == "pdf"
        assert res.odfname == "writer_pdf_Export"
        assert res.mimetype == "application/pdf"

    @raises(UnkownFormatException)
    def test_invalid(self):
        self.formats.get_format('invalidformat')

    def test_get_format_names(self):
        names = self.formats.get_known_format_names()
        assert FORMAT_PDF in names
