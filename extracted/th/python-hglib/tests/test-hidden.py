from tests import common
import hglib, datetime
from hglib.error import CommandError
from hglib.util import b

class test_obsolete_reference(common.basetest):
    """make sure obsolete changesets are disabled"""
    def test_debugobsolete_failure(self):
        f = open('gna1','w')
        f.write('g')
        f.close()
        self.client.add(b('gna1'))
        cs = self.client.commit(b('gna1'))[1] #get id
        self.assertRaises(CommandError,
                          self.client.rawcommand, [b('debugobsolete'), cs])


class test_obsolete_baselib(common.basetest):
    """base test class with obsolete changesets enabled"""
    def setUp(self):
        #create an extension which only activates obsolete
        super(test_obsolete_baselib, self).setUp()
        self.append('.hg/obs.py',
                    "import mercurial.obsolete\n"
                    "# 3.2 and later\n"
                    "mercurial.obsolete.isenabled = lambda r, opt: True\n"
                    "# Dropped in 5.1\n"
                    "mercurial.obsolete._enabled = True")
        self.append('.hg/hgrc','\n[extensions]\nobs=.hg/obs.py')

class test_obsolete_client(test_obsolete_baselib):
    """check client methods with obsolete changesets enabled"""
    def test_debugobsolete_success(self):
        """check the obsolete extension is available"""
        self.append('gna1','ga')
        self.client.add(b('gna1'))
        cs = self.client.commit(b('gna1'))[1] #get id
        self.client.rawcommand([b('debugobsolete'), cs])

    def test_obsolete_in(self):
        """test the 'hidden' keyword with the 'in' method"""
        if self.client.version < (2, 9, 0):
            return
        self.append('gna1','ga')
        self.client.add(b('gna1'))
        cs0 = self.client.commit(b('gna1'))[1] #get id
        self.append('gna2','gaaa')
        self.client.add(b('gna2'))
        cs1 = self.client.commit(b('gna2'))[1] #get id
        self.client.rawcommand([b('debugobsolete'), cs1])
        self.client.update(cs0)
        self.assertFalse(cs1 in self.client)
        self.assertTrue(cs0 in self.client)
        self.client.hidden = True
        self.assertTrue(cs1 in self.client)

class test_hidden_context(test_obsolete_baselib):
    """test the "hidden" context method with obsolete changesets enabled on
    hidden and visible changesets"""
    def test_hidden(self):
        if self.client.version < (2, 9, 0):
            return
        self.append('gna1','ga')
        self.client.add(b('gna1'))
        cs0 = self.client.commit(b('gna1'))[1] #get id
        ctx0 = self.client[cs0]
        self.append('gna2','gaaa')
        self.client.add(b('gna2'))
        cs1 = self.client.commit(b('gna2'))[1] #get id
        ctx1 = self.client[cs1]
        self.client.rawcommand([b('debugobsolete'), cs1])
        self.client.update(cs0)
        self.assertTrue(ctx1.hidden())
        self.assertFalse(ctx0.hidden())
