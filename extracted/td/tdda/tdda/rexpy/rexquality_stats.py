# -*- coding: utf-8 -*-

"""
Standalone script to generate CSV tables of rexpy quality metrics
(len, fp, fn, fpr, fgr, fnr) for a set of named regexes, scored
against a given evaluator (a ConcreteRexMetric).

fp, fpr and fgr can be CountRanges (when a pattern's alternation
leaves genuine overlap uncertainty), so each is written as two
columns, min and max; these coincide when the value is an exact
scalar.
"""

import csv
import os

import polars as pl

from tdda.rexpy.quality import ConcreteRexMetric, CountRange
from tdda.rexpy import testrexquality as trq


def _min_max(value):
    """Split a value that may be an int/float or a CountRange into
    a (min, max) pair, so both shapes fit the same CSV columns.

    Args:
        value (int, float or CountRange): the value to split.

    Returns:
        tuple: (min, max), equal to each other when value is a
            scalar.
    """
    if isinstance(value, CountRange):
        return (value.lower, value.upper)
    return (value, value)


FIELDNAMES = [
    'domain', 'evaluation_data', 'name', 'regex', 'len',
    'fp_min', 'fp_max', 'fn', 'fpr_min', 'fpr_max', 'fgr_min',
    'fgr_max', 'fnr',
]


def write_quality_stats(
    named_regexes, evaluator, path, domain, evaluation_data,
    append=False,
):
    """Score each of `named_regexes` against `evaluator` and write
    the resulting metrics to a CSV file at `path`.

    Args:
        named_regexes (list): list of (name, regex) pairs.
        evaluator (ConcreteRexMetric): scorer to call `.evaluate()`
            on for each regex.
        path (str): destination path for the CSV file.
        domain (str): name of the domain being evaluated (e.g.
            'postcodes'), written to every row.
        evaluation_data (str): name of the dataset or regex spec
            `evaluator` was built from, written to every row.
        append (bool): if True, append to an existing file (no
            header row) instead of overwriting it with a fresh one.
            Lets several evaluations land in a single CSV.

    Returns:
        None
    """
    mode = 'a' if append else 'w'
    with open(path, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not append:
            writer.writeheader()
        print(f'Scoring against {evaluation_data} ...', flush=True)
        for name, regex in named_regexes:
            print(f'  {name} ...', end=' ', flush=True)
            score = evaluator.evaluate(regex)
            print('done', flush=True)
            fp_min, fp_max = _min_max(score.fp)
            fpr_min, fpr_max = _min_max(score.fpr)
            fgr_min, fgr_max = _min_max(score.fgr)
            writer.writerow({
                'domain': domain,
                'evaluation_data': evaluation_data,
                'name': name,
                'regex': regex,
                'len': score.len,
                'fp_min': fp_min,
                'fp_max': fp_max,
                'fn': score.fn,
                'fpr_min': fpr_min,
                'fpr_max': fpr_max,
                'fgr_min': fgr_min,
                'fgr_max': fgr_max,
                'fnr': score.fnr,
            })


POSTCODE_REGEXES = [
    ('group1', trq.POSTCODE_RE_1),
    ('group2', trq.POSTCODE_RE_2),
    ('group3', trq.POSTCODE_RE_3),
    ('group4', trq.POSTCODE_RE_4),
    ('group4b', trq.POSTCODE_RE_4B),
    ('group4c', trq.POSTCODE_RE_4C),
    ('group5', trq.POSTCODE_RE_5),
    ('group6', trq.POSTCODE_RE_6),
    ('group7', trq.POSTCODE_RE_7),
    ('group8', trq.POSTCODE_RE_8),
    ('group9', trq.POSTCODE_RE_9),
    ('group10', trq.POSTCODE_RE_10),
    ('tight1', trq.POSTCODE_RE_TIGHT1),
    ('tight2', trq.POSTCODE_RE_TIGHT2),
    ('tight3', trq.POSTCODE_RE_TIGHT3),
]

POSTCODE_ALPHABET = trq.TestCountStringsPostcodeAlphabet.ALPHABET


def postcodes_e_subset_evaluator():
    """Build a ConcreteRexMetric for the 55 real 'E...1AA' postcodes
    shipped in testdata/postcode-subset-e.txt.

    Returns:
        ConcreteRexMetric
    """
    path = os.path.join(trq.TESTDATADIR, 'postcode-subset-e.txt')
    with open(path) as f:
        positives = [line.rstrip('\n') for line in f if line.strip()]
    return ConcreteRexMetric(positives, alphabet=POSTCODE_ALPHABET)


def full_postcodes_evaluator():
    """Build a ConcreteRexMetric for the full ~2.5M-row UK postcode
    dataset. Only usable when that (unshipped) dataset is present
    locally -- see `full_postcode_data_available()`.

    Returns:
        ConcreteRexMetric
    """
    positives = pl.read_parquet(
        trq.FULL_POSTCODES_PATH
    )['Postcode'].to_list()
    return ConcreteRexMetric(positives, alphabet=POSTCODE_ALPHABET)


def xerpy_tight3_evaluator(weighted):
    """Build a ConcreteRexMetric using POSTCODE_RE_TIGHT3 as an
    xerpy-sampled ground-truth spec, rather than a real dataset (see
    TestConcreteRexMetricPostcodesViaXerpy). Preferred over TIGHT2,
    which over-generates London districts with 2 digits plus a
    subdistrict letter -- a combination real data never has.

    `weighted` (bool): if True, samples (both the ground-truth
    positives and, for each candidate, the fp-checking sample) are
    drawn with alternation branches weighted by cardinality, rather
    than uniformly -- e.g. GIR/NPT are correctly treated as
    vanishingly rare rather than each as likely as the whole general
    area/digit shape, which is what real data actually looks like
    here. If False, alternation branches are chosen uniformly,
    matching `Xerpy`'s own default.

    Args:
        weighted (bool): see above.

    Returns:
        ConcreteRexMetric
    """
    return ConcreteRexMetric(
        trq.POSTCODE_RE_TIGHT3, alphabet=POSTCODE_ALPHABET,
        weighted=weighted,
    )


def main():
    """Write quality stats for the postcode regex progression,
    scored against the 55-postcode 'E' subset, the xerpy-sampled
    TIGHT3 spec, and (if available) the full ~2.5M-row postcode
    dataset, into a single CSV.

    Returns:
        None
    """
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'postcode_quality_stats.csv',
    )
    write_quality_stats(
        POSTCODE_REGEXES, postcodes_e_subset_evaluator(), path,
        'postcodes', 'postcode-subset-e.txt',
    )
    write_quality_stats(
        POSTCODE_REGEXES, xerpy_tight3_evaluator(weighted=True), path,
        'postcodes', 'xerpy:tight3w', append=True,
    )
    write_quality_stats(
        POSTCODE_REGEXES, xerpy_tight3_evaluator(weighted=False), path,
        'postcodes', 'xerpy:tight3u', append=True,
    )
    if trq.full_postcode_data_available():
        write_quality_stats(
            POSTCODE_REGEXES, full_postcodes_evaluator(), path,
            'postcodes', 'postcodes-full.parquet', append=True,
        )


if __name__ == '__main__':
    main()
