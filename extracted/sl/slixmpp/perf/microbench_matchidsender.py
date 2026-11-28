#!/usr/bin/env python3
"""
Microbenchmark for the "MatchIDSender" matcher.

At the time of writing on one specific computer:

Proposed optimization branch: 1000 loops, best of 5: 251 usec per loop
Master branch: 50 loops, best of 5: 4.52 msec per loop

Changing the number of matchers keeps the same magnitude of improvement.

"""
from slixmpp import Iq, JID
from slixmpp.xmlstream.matcher import MatchIDSender


matchers = [
    MatchIDSender({
        'id': f'stanza-id-{n}',
        'peer': JID(f'tototo{n}@example'),
        'self': JID('me@example'),
    })
    for n in range(1000)
]

stanza = Iq()


def run_match():
    """Simulate a run where a stanza is received and checked"""
    m = [h for h in matchers if h.match(stanza)]
    return m


if __name__ == '__main__':
    import sys
    from os import chdir
    from os.path import dirname
    from subprocess import run
    directory = dirname(sys.argv[0])
    if directory:
        chdir(directory)

    run([
        'python3', '-m', 'timeit', '-s', 'import microbench_matchidsender',
        'microbench_matchidsender.run_match()',
    ])

