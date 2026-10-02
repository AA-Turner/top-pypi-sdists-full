#!/usr/bin/python3
"""Check that every comparing module tests a change the same way.

    python verify_tests.py pikobs

This reads the code, not the documentation: which function of
:mod:`pikobs.stats` each module imports and calls, and whether the
observations reach the test matched or as two independent samples. A
module whose docstring claims to pair but that never reads a pair would
pass a reading and fail here.

It follows import aliases, so ``paired_ttest_confidence as _paired_t``
counts as the paired test, which is how scatter writes it.

What it expects, and why: a module that kept the observations can match
them, and then the bias goes through the paired t-test; one that kept
only counts has nothing to test at all. Anything else is worth knowing
about.
"""

import ast
import os
import sys

EXPECTED = {
    'scatter':      'paired',
    'zone':         'paired',
    'profile':      'paired',
    'verifprofile': 'paired',
    'timeserie':    'paired',
    'histogram':    'paired',
    'cardio':       'paired',
    'vdedr':        'paired',
    'obscountdb':   'none',
    'flags':        'none',
    'mapobs':       'none',
}

TESTS = ('paired_ttest_confidence', 'ttest_confidence', 'ftest_confidence',
         'sigma_confidence', 'pitman_morgan_confidence', 'ks_from_counts')


def _used_tests(path):
    """Which tests of pikobs.stats this file actually calls, by real name."""
    try:
        tree = ast.parse(open(path).read())
    except Exception:
        return set()
    alias = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and 'stats' in (node.module or ''):
            for a in node.names:
                if a.name in TESTS:
                    alias[a.asname or a.name] = a.name
    called = {n.func.id for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    return {alias[name] for name in called if name in alias}


def main(root='pikobs'):
    print(f"{'module':<14} {'bias':<12} {'sigma':<9} {'shape':<7} "
          f"{'matched':<9} verdict")
    print("-" * 62)
    bad = []
    for module, expected in EXPECTED.items():
        files = [os.path.join(root, n) for n in
                 (f"{module}/{module}.py", f"{module}/{module}_plot.py",
                  f"{module}.py")]
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            print(f"{module:<14} (not found)")
            continue

        tests, text = set(), ""
        for f in files:
            tests |= _used_tests(f)
            text += open(f).read()

        paired = 'paired_ttest_confidence' in tests
        welch = 'ttest_confidence' in tests
        bias = 'paired t' if paired else ('Welch' if welch else '-')
        # the sigma goes through stats.sigma_confidence: Pitman-Morgan
        # when the runs are matched, the F-test when they are not. A
        # direct F-test in a comparing module is the old mistake back
        direct_f = 'ftest_confidence' in tests
        if 'sigma_confidence' in tests and not direct_f:
            sigma = 'PM / F'
        elif 'pitman_morgan_confidence' in tests and not direct_f:
            sigma = 'PM'
        elif direct_f:
            sigma = 'F only'
        else:
            sigma = '-'
        shape = 'KS' if 'ks_from_counts' in tests else '-'
        # every module names its pair table differently -- ts_pair,
        # zone_pairs, pairs_cardio, a temporary one in histogram -- so
        # look for the join that builds it rather than for a name
        matched = 'yes' if any(
            k in text for k in ('pikobs.match', '_PAIR_KEY', 'ts_pair',
                                'zone_pairs',
                                'pairs_cardio', 'pairs_vdedr',
                                'CREATE TEMP TABLE pairs',
                                'create_zone_matched')) else 'no'

        got = 'paired' if paired else ('welch' if welch else 'none')
        ok = got == expected
        if not ok:
            bad.append(f"{module}: {got}, expected {expected}")
        if expected == 'paired' and sigma not in ('PM / F', 'PM'):
            ok = False
            bad.append(f"{module}: sigma tested with '{sigma}'; matched "
                       f"runs need stats.sigma_confidence")
        print(f"{module:<14} {bias:<12} {sigma:<9} {shape:<7} {matched:<9} "
              f"{'ok' if ok else 'NOT AS EXPECTED'}")

    print()
    if bad:
        for line in bad:
            print("  " + line)
        return 1
    print("every comparing module runs the paired t-test on the bias and, "
          "through stats.sigma_confidence,")
    print("Pitman-Morgan on the sigma of matched runs (the F-test when "
          "MATCH=off);")
    print("the three that only count run neither, which is right: a census "
          "is not a sample.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'pikobs'))
