from __future__ import print_function, unicode_literals

try:
    import coverage

    cov = coverage.coverage()
except ImportError:

    class DummyCoverage(object):
        def start(self):
            pass

        def stop(self):
            pass

        def save(self):
            pass

        def report(self, *a, **k):
            pass

    cov = DummyCoverage()

cov.start()
import sys
import os
import doctest
import unittest
import itertools
import re
import argparse
import json

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

HERE = os.path.abspath(os.path.dirname(__file__))
DOTDOT = os.path.abspath(os.path.join(HERE, ".."))

MATERIAL_PATH = os.path.join(HERE, "Material")

sys.path.insert(0, os.path.join(DOTDOT, "src"))
import json_delta


def gather_material(dr=MATERIAL_PATH):
    files = set(os.listdir(dr))
    i = 0
    for f in files.copy():
        if (
            re.search(r"^(?:(?:case|diff|target)_\d{2}.json|udiff_\d{2}.patch)$", f)
            is None
        ):
            files.discard(f)
    while True:
        out = i
        if not files:
            break
        for frame in (
            "case_%02d.json",
            "target_%02d.json",
            "diff_%02d.json",
            "udiff_%02d.patch",
        ):
            if frame % i not in files:
                out = None
            files.discard(frame % i)
        if out is not None:
            yield out
        i += 1


def load_material(category, index):
    util = json_delta._util
    ext = "patch" if category == "udiff" else "json"
    fn = os.path.join(MATERIAL_PATH, "{}_{:02d}.{}".format(category, index, ext))
    with open(fn) as f:
        bytestring = util.read_bytestring(f)
    if category == "udiff":
        if not bytestring:
            return b'""'
        encoding = util.sniff_encoding(bytestring, util.UDIFF_STARTS)
        udiff = bytestring.decode(encoding)
        bytestring = util.compact_json_dumps(udiff).encode(encoding)
    return bytestring


MODULES = (
    json_delta,
    json_delta._diff,
    json_delta._udiff,
    json_delta._patch,
    json_delta._upatch,
    json_delta._util,
)


class DocTestSuite(unittest.TestSuite):
    def __init__(self):
        return unittest.TestSuite.__init__(
            self, (doctest.DocTestSuite(mod) for mod in MODULES)
        )


class PerIndexCase(unittest.TestCase):
    def __init__(self, index):
        unittest.TestCase.__init__(self, "runTest")
        self.index = index
        self.attrs = {type(self).__name__[:-4], self.index}

    def __str__(self):
        return "{}, case {}".format(type(self).__name__, self.index)

    def setUp(self):
        for cat in self.cats:
            setattr(self, cat, load_material(cat, self.index))


class MinimalDiffCase(PerIndexCase):
    cats = ("case", "target")

    def runTest(self):
        diff = json_delta.load_and_diff(self.case, self.target, verbose=True)
        self.assertEquals(
            json_delta._util.decode_json(self.target),
            json_delta.patch(json_delta._util.decode_json(self.case), diff),
        )


class NonMinimalDiffCase(PerIndexCase):
    cats = ("case", "target")

    def runTest(self):
        diff = json_delta.load_and_diff(
            self.case, self.target, minimal=False, verbose=True
        )
        self.assertEquals(
            json_delta._util.decode_json(self.target),
            json_delta.patch(json_delta._util.decode_json(self.case), diff),
        )


class PatchCase(PerIndexCase):
    cats = ("case", "target", "diff")

    def runTest(self):
        self.assertEquals(
            json_delta._util.decode_json(self.target),
            json_delta.load_and_patch(self.case, self.diff),
        )


class UdiffCase(PerIndexCase):
    cats = ("case", "target")
    maxDiff = None

    def runTest(self):
        udiff = "\n".join(json_delta.load_and_udiff(self.case, self.target))
        self.assertEquals(
            json_delta._util.decode_json(self.target),
            json_delta.upatch(json_delta._util.decode_json(self.case), udiff),
        )


class UpatchCase(PerIndexCase):
    cats = ("case", "target", "udiff")

    def runTest(self):
        self.assertEquals(
            json_delta._util.decode_json(self.target),
            json_delta.load_and_upatch(self.case, self.udiff),
        )


class ReverseUpatchCase(PerIndexCase):
    cats = ("case", "target", "udiff")

    def runTest(self):
        self.assertEquals(
            json_delta._util.decode_json(self.case),
            json_delta.load_and_upatch(self.target, self.udiff, reverse=True),
        )


class LengthCase(PerIndexCase):
    def __init__(self, index):
        PerIndexCase.__init__(self, index)
        self.attrs = {"length"}

    def setUp(self):
        cat = self.cats[0]
        matter_path = os.path.join(
            MATERIAL_PATH, "{}_{:02}.json".format(cat, self.index)
        )
        with open(matter_path) as f:
            self.matter = json_delta._util.decode_json(f)


class JSONLengthCase(LengthCase):
    def runTest(self):
        baseline = json_delta._util.compact_json_dumps(self.matter)
        baseline = len(baseline.encode("UTF-8"))
        self.assertEquals(json_delta._util.json_length(self.matter), baseline)


class PaddedLengthCase(LengthCase):
    @staticmethod
    def b_whitespace_count(obj, indent=1, margin=1):
        """Brute-force version of :py:func:`json_delta._util.whitespace_count`.

        Dumps ``obj`` to a JSON string and then counts the spaces and
        newlines (not including spaces within JSON strings).

        """
        d = json.dumps(obj, indent=indent)
        d = d.replace("\n", "\n{}".format(" " * margin))
        d = "{}{}".format(" " * margin, d)
        point = 0
        count = 0
        while point < len(d):
            char = d[point]
            if char in " \n":
                count += 1

            if char == '"':
                point = json_delta._util.skip_string(d, point)
            else:
                point += 1
        return count

    def runTest(self):
        self.assertEquals(
            json_delta._util.whitespace_count(self.matter),
            self.b_whitespace_count(self.matter),
        )


class CaseLengthCase(JSONLengthCase):
    cats = ("case",)


class TargetLengthCase(JSONLengthCase):
    cats = ("target",)


class DiffLengthCase(JSONLengthCase):
    cats = ("diff",)


class CasePaddedLengthCase(PaddedLengthCase):
    cats = ("case",)


class TargetPaddedLengthCase(PaddedLengthCase):
    cats = ("target",)


class DiffPaddedLengthCase(PaddedLengthCase):
    cats = ("diff",)


class DiffFunctionWarningTest(unittest.TestCase):
    def setUp(self):
        self.err_stream = StringIO()
        self.stderr_save = sys.stderr
        sys.stderr = self.err_stream

    def runTest(self):
        self.assertEqual(
            json_delta.diff([], [], minimal=True, common_key_threshold=0.5), []
        )
        self.assertEqual(
            self.err_stream.getvalue(),
            """Warning: arguments contradict one another!  Using the following parms:
\tarray_align: {0}
\tcompare_lengths: {0}
\tcommon_key_threshold: 0.5
""".format(
                True
            ),
        )

    def tearDown(self):
        sys.stderr = self.stderr_save


class ReconstructAlignmentRegressionTest(unittest.TestCase):
    case = []
    target = ["foo", "bar"]
    diff = [[[0], "bar", "i"], [[0], "foo", "i"]]

    def runTest(self):
        self.assertEquals(
            json_delta.patch(self.case, self.diff, in_place=False), self.target
        )
        udiff = "\n".join(json_delta.udiff(self.case, self.target, patch=self.diff))
        comparand = json_delta.upatch(self.case, udiff, in_place=False)
        self.assertEquals(self.target, comparand)


INDICES = [x for x in gather_material()]
INDEX_CASES = [
    MinimalDiffCase,
    UdiffCase,
    NonMinimalDiffCase,
    PatchCase,
    UpatchCase,
    ReverseUpatchCase,
    CaseLengthCase,
    TargetLengthCase,
    DiffLengthCase,
    CasePaddedLengthCase,
    TargetPaddedLengthCase,
    DiffPaddedLengthCase,
]


def desired_attr_sets(attr_args):
    out = set()
    for attrs in attr_args:
        attr_set = set()
        for attr in attrs:
            if re.search("^[A-Za-z-]+$", attr):
                attr_set.add(attr)
            elif re.search("^[0-9]+(?:,[0-9]+)*$", attr):
                attr_set.update((int(x) for x in attr.split(",")))
            else:
                mat = re.search("^([0-9]+)-([0-9]+)$", attr)
                if mat is not None:
                    attr_set.update(range(int(mat.group(1)), int(mat.group(2)) + 1))
        out.add(frozenset(attr_set))
    return out


def generate_test_cases(attr_check=lambda x: True):
    for case_class, case_no in itertools.product(INDEX_CASES, INDICES):
        case = case_class(case_no)
        if case is not None and attr_check(case.attrs):
            yield case
    if attr_check({"doctest"}):
        for module in MODULES:
            yield doctest.DocTestSuite(module)
        yield DiffFunctionWarningTest()
    if attr_check({"regression"}):
        yield ReconstructAlignmentRegressionTest()


def build_test_suite(attr_check=lambda x: True):
    return unittest.TestSuite(generate_test_cases(attr_check))


def check_attr_sets(case_attrs, attr_sets):
    if attr_sets == set():
        return True
    for attr_set in attr_sets:
        if attr_set.issubset(case_attrs):
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attribute", "-a", nargs="+", action="append", default=[])
    parser.add_argument("--verbose", "-v", action="count", default=0)
    opts = parser.parse_args()
    attr_sets = desired_attr_sets(opts.attribute)

    def attr_check(attrs):
        return check_attr_sets(attrs, attr_sets)

    suite = build_test_suite(attr_check)
    unittest.TextTestRunner(descriptions=False, verbosity=opts.verbose + 1).run(suite)


if __name__ == "__main__":
    main()
    cov.stop()
    cov.save()
    cov.report(MODULES)
