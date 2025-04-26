# coding: utf-8
"""
PyUnit unit tests
"""
import logging
import unittest
import sys
import tempfile
import locale
try:
    import json
except ImportError:
    import simplejson as json
import json_diff
from io import StringIO
import codecs

from .test_strings import ARRAY_DIFF, ARRAY_NEW, ARRAY_OLD, \
    NESTED_DIFF, NESTED_DIFF_EXCL, NESTED_DIFF_INCL, NESTED_NEW, NESTED_OLD, \
    NO_JSON_NEW, NO_JSON_OLD, SIMPLE_ARRAY_DIFF, SIMPLE_ARRAY_NEW, \
    NESTED_DIFF_IGNORING, \
    SIMPLE_ARRAY_OLD, SIMPLE_DIFF, SIMPLE_DIFF_HTML, SIMPLE_NEW, SIMPLE_OLD

log = logging.getLogger('test_json_diff')

class OptionsClass(object):
    def __init__(self, inc=None, exc=None, ign=None):
        self.exclude = exc
        self.include = inc
        self.ignore_append = ign


class OurTestCase(unittest.TestCase):
    def _run_test(self, oldf, newf, difff, msg=u"", opts=None):
        diffator = json_diff.Comparator(oldf, newf, opts)
        diff = diffator.compare_dicts()
        expected = json.load(difff)
        self.assertEqual(json.dumps(diff, sort_keys=True),
                         json.dumps(expected, sort_keys=True),
                         msg + "\n\nexpected = %s\n\nobserved = %s" %
                         (json.dumps(expected, sort_keys=True, indent=4,
                                     ensure_ascii=False),
                          json.dumps(diff, sort_keys=True, indent=4,
                                     ensure_ascii=False)))

    def _run_test_strings(self, olds, news, diffs, msg=u"", opts=None):
        # log.debug('olds = %s (%s), news = %s (%s), diffs = %s (%s), msg = %s (%s), opts = %s (%s)', olds, type(olds), news, type(news), diffs, type(diffs), msg, type(msg), opts, type(opts))
        self._run_test(StringIO(olds), StringIO(news), StringIO(diffs),
                       msg, opts)

    @unittest.skip("HTMLFormatter doesn't keep order of elements.")
    def _run_test_formatted(self, oldf, newf, difff, msg=u"", opts=None):
        diffator = json_diff.Comparator(oldf, newf, opts)
        diff = ("\n".join([line.strip()
                for line in str(
                    json_diff.HTMLFormatter(diffator.compare_dicts())).
                split("\n")])).strip()
        expected = ("\n".join([line.strip() for line in difff if line])).\
            strip()
        self.assertEqual(diff, expected, msg +
                         "\n\nexpected = %s\n\nobserved = %s" %
                         (expected, diff))


class TestBasicJSON(OurTestCase):
    maxDiff = None

    def test_empty(self):
        diffator = json_diff.Comparator({}, {})
        diff = diffator.compare_dicts()
        self.assertEqual(json.dumps(diff).strip(), "{}",
                         "Empty objs diff.\n\nexpected = %s\n\nobserved = %s" %
                         ({}, diff))

    def test_null(self):
        self._run_test_strings(u'{"a": null}', u'{"a": null}',
                               u'{}', "Nulls")

    def test_null_to_string(self):
        self._run_test_strings(u'{"a": null}', u'{"a": "something"}',
                               u'{"_update": {"a": "something"}}',
                               "Null changed to string")

    def test_boolean(self):
        self._run_test_strings(u'{"a": true}', u'{"a": false}',
                               u'{"_update": {"a": false}}', "Booleans")

    def test_integer(self):
        self._run_test_strings(u'{"a": 1}', u'{"a": 2}',
                               u'{"_update": {"a": 2}}', "Integers")

    def test_float(self):
        self._run_test_strings(u'{"a": 1.0}', u'{"a": 1.1}',
                               u'{"_update": {"a": 1.1}}', "Floats")

    def test_int_to_float(self):
        self._run_test_strings(u'{"a": 1}', u'{"a": 1.0}',
                               u'{"_update": {"a": 1.0}}',
                               "Integer changed to float")

    def test_simple(self):
        self._run_test_strings(SIMPLE_OLD, SIMPLE_NEW, SIMPLE_DIFF,
                               "All-scalar objects diff.")

    def test_simple_formatted(self):
        self._run_test_formatted(StringIO(SIMPLE_OLD), StringIO(SIMPLE_NEW),
                                 StringIO(SIMPLE_DIFF_HTML),
                                 "All-scalar objects diff (formatted).")

    def test_simple_array(self):
        self._run_test_strings(SIMPLE_ARRAY_OLD, SIMPLE_ARRAY_NEW,
                               SIMPLE_ARRAY_DIFF, "Simple array objects diff.")

    def test_another_array(self):
        self._run_test_strings(ARRAY_OLD, ARRAY_NEW,
                               ARRAY_DIFF, "Array objects diff.")


class TestHappyPath(OurTestCase):
    def test_realFile(self):
        with open("test/old.json") as oldF, open("test/new.json") as newF, \
                open("test/diff.json") as diffF:
            self._run_test(oldF, newF, diffF,
                           "Simply nested objects (from file) diff.")

    def test_nested(self):
        self._run_test_strings(NESTED_OLD, NESTED_NEW, NESTED_DIFF,
                               "Nested objects diff.")

    def test_nested_formatted(self):
        with open("test/old.json") as oldF, open("test/new.json") as newF, \
                open("test/nested_html_output.html", "r", encoding="utf-8") as outF:
            self._run_test_formatted(oldF, newF, outF,
                                     "Simply nested objects (from file) " +
                                     "diff formatted as HTML.")

    def test_nested_excluded(self):
        self._run_test_strings(NESTED_OLD, NESTED_NEW, NESTED_DIFF_EXCL,
                               "Nested objects diff with exclusion.",
                               OptionsClass(exc=["nome"]))

    def test_nested_included(self):
        self._run_test_strings(NESTED_OLD, NESTED_NEW, NESTED_DIFF_INCL,
                               "Nested objects diff.",
                               OptionsClass(inc=["nome"]))

    def test_nested_ignoring_append(self):
        self._run_test_strings(NESTED_OLD, NESTED_NEW, NESTED_DIFF_IGNORING,
                               "Nested objects diff.",
                               OptionsClass(ign=True))

    # bug /6cf
    @unittest.skip('Not finished yet.')
    def test_large_recursive_file(self):
        self._run_test(open("test/DMS_1121_1.json.1.out"),
                       open("test/DMS_1121_1.json.2.out"),
                       open("test/diff.json"),
                       "Simply nested objects (from file) diff.")


class TestBadPath(OurTestCase):
    def test_no_JSON(self):
        self.assertRaises(json_diff.BadJSONError,
                          json_diff.Comparator, StringIO(NO_JSON_OLD),
                          StringIO(NO_JSON_NEW))

    def test_bad_JSON_no_hex(self):
        self.assertRaises(json_diff.BadJSONError, self._run_test_strings,
                          u'{"a": 0x1}', u'{"a": 2}', u'{"_update": {"a": 2}}',
                          u"Hex numbers not supported")

    def test_bad_JSON_no_octal(self):
        self.assertRaises(json_diff.BadJSONError, self._run_test_strings,
                          u'{"a": 01}', u'{"a": 2}', u'{"_update": {"a": 2}}',
                          u"Octal numbers not supported")


class TestPiglitData(OurTestCase):
    def test_piglit_result_only(self):
        with open('test/old-testing-data.json') as oldF, \
                open('test/new-testing-data.json') as newF, \
                open('test/diff-result-only-testing-data.json') as diffF:
            self._run_test(oldF, newF, diffF,
                           u"Large piglit reports diff (just resume field).",
                           OptionsClass(inc=["result"]))

#    def test_piglit_results(self):
#        self._run_test(open("test/old-testing-data.json"),
#            open("test/new-testing-data.json"),
#            open("test/diff-testing-data.json"), "Large piglit results diff.")


class TestMainArgsMgmt(unittest.TestCase):
    def test_args_help(self):
        save_stdout = StringIO()
        sys.stdout = save_stdout

        try:
            json_diff.main(["./test_json_diff.py", "-h"])
        except SystemExit:
            save_stdout.seek(0)
            sys.stdout = sys.__stdout__
            expected = "usage:"
            observed = save_stdout.read().lower()

        self.assertEqual(observed[:len(expected)], expected,
                          "testing -h usage message" +
                          "\n\nexpected = %s\n\nobserved = %s" %
                          (expected, observed))

    def test_args_run_same(self):
        save_stdout = StringIO()
        sys.stdout = save_stdout
        cur_loc = locale.getlocale()
        locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")

        res = json_diff.main(["./test_json_diff.py",
                             "test/old.json", "test/old.json"])

        sys.stdout = sys.__stdout__
        locale.setlocale(locale.LC_ALL, cur_loc)
        self.assertEqual(res, 0, "comparing same file" +
                          "\n\nexpected = %d\n\nobserved = %d" %
                          (0, res))

    def test_args_run_different(self):
        with StringIO() as save_stdout:
            sys.stdout = save_stdout
            cur_loc = locale.getlocale()
            locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")

            res = json_diff.main(["./test_json_diff.py",
                                 "test/old.json", "test/new.json"])
        sys.stdout = sys.__stdout__
        locale.setlocale(locale.LC_ALL, cur_loc)
        # log.debug('res = %s (%s)', res, type(res))
        self.assertEqual(res, 1, "comparing different files" +
                         "\n\nexpected = %d\n\nobserved = %d" %
                         (1, res))

    def test_args_run_output(self):
        save_stdout = tempfile.NamedTemporaryFile(prefix="json_diff_")
        cur_loc = locale.getlocale()
        locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")

        json_diff.main(["./test_json_diff.py",
                        "-o", save_stdout.name,
                        "test/old.json", "test/new.json"])

        save_stdout.seek(0)
        observed = save_stdout.read().decode()
        save_stdout.close()

        with open("test/diff.json") as expected_file:
            expected = json.load(expected_file)

        locale.setlocale(locale.LC_ALL, cur_loc)
        try:
            obs_dict = json.loads(observed)
        except:
            log.debug('observed:\n%s\n', observed)
        self.assertEqual(expected, obs_dict, "non-stdout output file" +
                         "\n\nexpected = %s\n\nobserved = %s" %
                         (expected, observed))

add_tests_from_class = unittest.TestLoader().loadTestsFromTestCase

suite = unittest.TestSuite()
suite.addTest(add_tests_from_class(TestBasicJSON))
suite.addTest(add_tests_from_class(TestHappyPath))
suite.addTest(add_tests_from_class(TestBadPath))
suite.addTest(add_tests_from_class(TestPiglitData))
suite.addTest(add_tests_from_class(TestMainArgsMgmt))

if __name__ == "__main__":
    unittest.main()
