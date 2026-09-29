"""template_census.py - census of the boilerplate 'Observable | UQFF Prediction | SM / Experiment | Source | Alignment'
table across whitepapers/ (EXTERNAL_CONTACT_AUDIT.md section 3). Run from the repository root."""
import re, glob, collections
hdr = re.compile(r'^\|\s*Observable\s*\|\s*UQFF Prediction\s*\|\s*SM\s*/\s*Experiment\s*\|\s*Source\s*\|\s*Alignment', re.I)
papers = 0; rows = []
for f in sorted(glob.glob('whitepapers/PAPER_*.md')):
    L = open(f, encoding='utf-8', errors='replace').read().split('\n')
    for i, l in enumerate(L):
        if hdr.match(l):
            papers += 1; j = i + 2
            while j < len(L) and L[j].startswith('|'):
                c = [x.strip() for x in L[j].strip('|').split('|')]
                if len(c) >= 5: rows.append((f, c[0], c[1], c[2], c[3], c[4]))
                j += 1
            break
print('papers with template table:', papers, 'rows:', len(rows))
print(collections.Counter(r[1] for r in rows).most_common(12))
print(collections.Counter(re.sub(r'[\*\s]+', ' ', r[5]).strip()[:28] for r in rows).most_common(15))
print('numeric % alignments:', sum(1 for r in rows if re.search(r'\d+(\.\d+)?\s*%', r[5])))
print('PASS', sum(1 for r in rows if 'PASS' in r[5].upper()), 'Testable', sum(1 for r in rows if 'testable' in r[5].lower()))
print('four boilerplate rows:', sum(1 for r in rows if r[1].lower().startswith(('cosmological', 'proton decay', 'buoyancy', 'fine structure'))))
