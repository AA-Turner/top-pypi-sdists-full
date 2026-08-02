from tests import common
from hglib.util import b

class test_grep(common.basetest):
    def test_basic(self):
        self.append('a', 'x\n')
        self.append('b', 'xy\n')
        self.client.commit(b('first'), addremove=True)

        # no match
        self.assertEquals(list(self.client.grep(b('c'))), [])

        if self.client.version >= (5, 2):
            self.assertEquals(list(self.client.grep(b('x'))),
                              [(b('a'), b('x')), (b('b'), b('xy'))])
            self.assertEquals(list(self.client.grep(b('x'), b('a'))),
                              [(b('a'), b('x'))])

            self.assertEquals(list(self.client.grep(b('y'))),
                              [(b('b'), b('xy'))])
        else:
            self.assertEquals(list(self.client.grep(b('x'))),
                              [(b('a'), b('0'), b('x')), (b('b'), b('0'), b('xy'))])
            self.assertEquals(list(self.client.grep(b('x'), b('a'))),
                              [(b('a'), b('0'), b('x'))])
            self.assertEquals(list(self.client.grep(b('y'))),
                              [(b('b'), b('0'), b('xy'))])

    def test_options(self):
        self.append('a', 'x\n')
        self.append('b', 'xy\n')
        rev, node = self.client.commit(b('first'), addremove=True)

        self.assertEquals([(b('a'), b('0'), b('+'), b('x')),
                           (b('b'), b('0'), b('+'), b('xy'))],
                          list(self.client.grep(b('x'), all=True)))

        if self.client.version >= (5, 2):
            self.assertEquals([(b('a'),), (b('b'),)],
                              list(self.client.grep(b('x'), fileswithmatches=True)))

            self.assertEquals([(b('a'), b('1'), b('x')), (b('b'), b('1'), b('xy'))],
                              list(self.client.grep(b('x'), line=True)))

            self.assertEquals([(b('a'), b('test'), b('x')),
                               (b('b'), b('test'), b('xy'))],
                              list(self.client.grep(b('x'), user=True)))
        else:
            self.assertEquals([(b('a'), b('0')), (b('b'), b('0'))],
                              list(self.client.grep(b('x'), fileswithmatches=True)))

            self.assertEquals([(b('a'), b('0'), b('1'), b('x')),
                               (b('b'), b('0'), b('1'), b('xy'))],
                              list(self.client.grep(b('x'), line=True)))

            self.assertEquals([(b('a'), b('0'), b('test'), b('x')),
                               (b('b'), b('0'), b('test'), b('xy'))],
                              list(self.client.grep(b('x'), user=True)))

        self.assertEquals([(b('a'), b('0'), b('1'), b('+'), b('test')),
                           (b('b'), b('0'), b('1'), b('+'), b('test'))],
                          list(self.client.grep(b('x'), all=True, user=True,
                                                line=True,
                                                fileswithmatches=True)))
