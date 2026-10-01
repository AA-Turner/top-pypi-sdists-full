#!/usr/bin/env python3
"""
Test whether merging two characters costs a treebank any distinction.

Crawled text and a treebank often spell the same thing differently:
Devanagari candrabindu against anusvara, Arabic yeh against Persian
yeh, a precomposed letter against a letter plus nukta.  Collapsing the
pair makes one well estimated representation out of two badly
estimated ones, but only if the treebank does not rely on the
difference.

    python merge_test.py UD_Bhojpuri-BHTB/*.conllu --merge 0901:0902
    python merge_test.py UD_Sindhi-*/*.conllu --merge 064A:06CC --merge 0643:06A9

Three questions are answered, in increasing order of what they cost:

  how many word types merge at all
  whether the merged types disagree about their tags
  how many tokens become ambiguous which were not ambiguous before

The last is the one that matters.  Types merging is expected and is
the point; a merge only costs accuracy when a form which used to
determine its tag stops determining it.
"""

import argparse
import sys
import unicodedata
from collections import Counter, defaultdict

def parse_merge(spec):
    """Read "0901:0902" or "ँ:ं" into a (from, to) pair of characters"""
    left, sep, right = spec.partition(":")
    if not sep:
        raise ValueError("--merge wants two characters separated by a colon, got %r" % spec)
    def one(s):
        s = s.strip()
        if len(s) == 1:
            return s
        try:
            return chr(int(s, 16))
        except ValueError:
            raise ValueError("could not read %r as a character or a hex codepoint" % s)
    return one(left), one(right)

def describe(ch):
    return "U+%04X %s" % (ord(ch), unicodedata.name(ch, "(unnamed)"))

def read_tokens(paths):
    """(form, upos, xpos, feats) for every word of every file"""
    tokens = []
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as fin:
            for line in fin:
                if line.startswith("#") or not line.strip():
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) < 6 or not f[0].isdigit():
                    continue
                tokens.append((f[1], f[3], f[4], f[5]))
    return tokens

def apply_merges(text, merges):
    for src, dst in merges:
        text = text.replace(src, dst)
    return text

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("conllu", nargs="+", help="treebank files, all splits ideally")
    parser.add_argument("--merge", action="append", required=True,
                        help='a pair to collapse, as "0901:0902" or as the characters themselves.  Repeatable')
    parser.add_argument("--tags", default="upos",
                        help="which annotation counts as the distinction: upos, xpos, feats, or all")
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    merges = [parse_merge(x) for x in args.merge]
    print("merging:")
    for src, dst in merges:
        print("   %s  ->  %s" % (describe(src), describe(dst)))

    tokens = read_tokens(args.conllu)
    if not tokens:
        print("no tokens read", file=sys.stderr)
        return 1
    index = {"upos": 1, "xpos": 2, "feats": 3}
    def tag_of(t):
        if args.tags == "all":
            return (t[1], t[2], t[3])
        return t[index[args.tags]]

    before_types = Counter(t[0] for t in tokens)
    after_types = Counter(apply_merges(t[0], merges) for t in tokens)
    affected = sum(n for f, n in before_types.items() if apply_merges(f, merges) != f)
    print("\ntokens %d, of which %d contain a merged character (%.1f%%)"
          % (len(tokens), affected, 100.0 * affected / len(tokens)))
    print("word types %d before, %d after" % (len(before_types), len(after_types)))

    # which original forms collapse together
    groups = defaultdict(set)
    for form in before_types:
        groups[apply_merges(form, merges)].add(form)
    collisions = {k: v for k, v in groups.items() if len(v) > 1}
    print("types which merge with another: %d groups" % len(collisions))

    # the tags each form and each merged form take
    tags_before = defaultdict(set)
    tags_after = defaultdict(set)
    for t in tokens:
        tags_before[t[0]].add(tag_of(t))
        tags_after[apply_merges(t[0], merges)].add(tag_of(t))

    disagreeing = []
    for merged, forms in collisions.items():
        tagsets = {f: tags_before[f] for f in forms}
        union = set().union(*tagsets.values())
        if any(tagsets[f] != union for f in forms):
            disagreeing.append((merged, tagsets))
    print("groups whose members disagree about %s: %d" % (args.tags, len(disagreeing)))

    for merged, tagsets in disagreeing[:args.top]:
        print("   %s" % merged)
        for form, tags in sorted(tagsets.items()):
            print("      %-18s %-5d %s" % (form, before_types[form], ", ".join(sorted(map(str, tags)))[:64]))

    # the number that matters: tokens which lose a decision they had
    newly = 0
    for t in tokens:
        merged = apply_merges(t[0], merges)
        if len(tags_before[t[0]]) == 1 and len(tags_after[merged]) > 1:
            newly += 1
    print("\ntokens which were unambiguous for %s and are not after merging: %d (%.3f%%)"
          % (args.tags, newly, 100.0 * newly / len(tokens)))
    if newly == 0:
        print("   the merge costs the treebank nothing it was using")
    return 0

if __name__ == "__main__":
    sys.exit(main())
