import unittest
from collections import OrderedDict
import re
import os
import time
from ddt import ddt, data, unpack
from elifearticle import utils


@ddt
class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_repl(self):
        string = "&#x2022;"
        matches = re.match(r"&#x(....);", string)
        self.assertEqual(utils.repl(matches), "\u2022")

    def test_entity_to_unicode(self):
        passes = []
        passes.append(
            (
                "N-terminal &#x03B1;-helix into the heterodimer interface",
                "N-terminal \u03b1-helix into the heterodimer interface",
            )
        )

        passes.append(
            (
                "N-terminal &alpha;-helix into the heterodimer interface",
                "N-terminal \u03b1-helix into the heterodimer interface",
            )
        )

        passes.append(
            (
                (
                    "&#x00A0; &#x00C5; &#x00D7; &#x00EF; &#x0394; &#x03B1; &#x03B2; &#x03B3;"
                    " &#x03BA; &#x03BB; &#x2212; &#x223C; &alpha; &amp; &beta; &epsilon; &iuml;"
                    " &ldquo; &ordm; &rdquo;"
                ),
                (
                    "\xa0 \xc5 \xd7 \xef \u0394 \u03b1 \u03b2 \u03b3"
                    " \u03ba \u03bb \u2212 \u223c \u03b1 &amp; \u03b2 \u03b5 \xcf "
                    '" \xba "'
                ),
            )
        )

        for string_input, string_output in passes:
            self.assertEqual(utils.entity_to_unicode(string_input), string_output)

    def test_remove_tag(self):
        self.assertEqual(utils.remove_tag("i", "<i>test</i>"), "test")
        self.assertEqual(utils.remove_tag("i", None), None)

    def test_replace_tags(self):
        self.assertEqual(utils.replace_tags("<i>"), "<italic>")

    def test_version_from_xml_filename(self):
        self.assertEqual(utils.version_from_xml_filename(None), None)
        self.assertEqual(utils.version_from_xml_filename("elife-00666.xml"), None)
        self.assertEqual(utils.version_from_xml_filename("elife-02935-v2.xml"), 2)
        self.assertEqual(
            utils.version_from_xml_filename(
                os.path.join("test-folder", "elife-02935-v2.xml")
            ),
            2,
        )
        self.assertEqual(utils.version_from_xml_filename("bmjopen-4-e003269.xml"), None)
        self.assertEqual(
            utils.version_from_xml_filename("elife-preprint-84364-v2.xml"), 2
        )

    def test_calculate_journal_volume(self):
        "for test coverage"
        self.assertEqual(utils.calculate_journal_volume(None, None), None)
        pub_date = time.strptime("2017-01-01", "%Y-%m-%d")
        self.assertEqual(utils.calculate_journal_volume(pub_date, 2017), "1")
        self.assertEqual(utils.calculate_journal_volume(pub_date, None), None)

    def test_get_last_commit_to_master(self):
        self.assertIsNotNone(utils.get_last_commit_to_master())

    def test_get_last_commit_to_master_no_path(self):
        git_path = "not_a_path"
        last_commit = ""
        expected = "None"
        last_commit = utils.get_last_commit_to_master(git_path)
        self.assertEqual(last_commit, expected)

    @unpack
    @data(
        (None, None, None, None, ""),
        ("", None, None, None, ""),
        ("One", "Two", "Three", "Four", "One, Two, Three, Four"),
        ("One", "Two", None, "Four", "One, Two, Four"),
        ("One", "Two", "", "Four", "One, Two, Four"),
    )
    def test_text_from_affiliation_elements(
        self, department, institution, city, country, expected
    ):
        self.assertEqual(
            utils.text_from_affiliation_elements(
                department, institution, city, country
            ),
            expected,
            "{expected} not found testing {department}, {institution}, {city}, {country}".format(
                expected=expected,
                department=department,
                institution=institution,
                city=city,
                country=country,
            ),
        )


class TestUtilsAttr(unittest.TestCase):
    def setUp(self):
        self.attr_map = {"foo": "& bar", "more": '"complicated"'}

    def test_attr_names(self):
        self.assertEqual(utils.attr_names(self.attr_map), ["foo", "more"])

    def test_attr_names_blank(self):
        self.assertEqual(utils.attr_names(None), [])

    def test_attr_string(self):
        expected = ' foo="&amp; bar" more="&quot;complicated&quot;"'
        self.assertEqual(utils.attr_string(self.attr_map), expected)

    def test_attr_blank(self):
        self.assertEqual(utils.attr_string(None), "")


class TestLicenseDataByUrl(unittest.TestCase):
    "tests for license_data_by_url()"

    def test_cc_by(self):
        "test CC-BY URL to get license data"
        license_url = "http://creativecommons.org/licenses/by/4.0/"
        expected = "https://creativecommons.org/licenses/by/4.0/"
        # invoke
        result = utils.license_data_by_url(license_url)
        # assert
        self.assertEqual(result.get("href"), expected)

    def test_cc_by_https(self):
        "test CC-BY HTTPS URL to get license data"
        license_url = "https://creativecommons.org/licenses/by/4.0/"
        # invoke
        result = utils.license_data_by_url(license_url)
        # assert
        self.assertEqual(result.get("href"), license_url)

    def test_cc_0(self):
        "test CC-0 URL to get license data"
        license_url = "http://creativecommons.org/publicdomain/zero/1.0/"
        expected = "https://creativecommons.org/publicdomain/zero/1.0/"
        # invoke
        result = utils.license_data_by_url(license_url)
        # assert
        self.assertEqual(result.get("href"), expected)

    def test_cc_0_https(self):
        "test CC-0 HTTPS URL to get license data"
        license_url = "https://creativecommons.org/publicdomain/zero/1.0/"
        # invoke
        result = utils.license_data_by_url(license_url)
        # assert
        self.assertEqual(result.get("href"), license_url)

    def test_no_match(self):
        "test if the license_url is not supported"
        self.assertEqual(
            utils.license_data_by_url("https://example.org/"), OrderedDict()
        )

    def test_none(self):
        "test if the license_url is None"
        self.assertEqual(utils.license_data_by_url(None), OrderedDict())
