# coding: utf-8
from __future__ import print_function, unicode_literals

import importlib
import sys
import xml.etree.ElementTree as ET

from .__init__ import PY2

class BadXML(Exception):
    pass


def get_ET()  :
    pn = "xml.etree.ElementTree"
    cn = "_elementtree"

    cmod = sys.modules.pop(cn, None)
    if not cmod:
        return ET.XMLParser  # type: ignore

    pmod = sys.modules.pop(pn)
    sys.modules[cn] = None  # type: ignore

    ret = importlib.import_module(pn)
    for name, mod in ((pn, pmod), (cn, cmod)):
        if mod:
            sys.modules[name] = mod
        else:
            sys.modules.pop(name, None)

    sys.modules["xml.etree"].ElementTree = pmod  # type: ignore
    ret.ParseError = ET.ParseError  # type: ignore
    return ret.XMLParser  # type: ignore


XMLParser  = get_ET()


class _DXMLParser(XMLParser):  # type: ignore
    def __init__(self)  :
        tb = ET.TreeBuilder()
        super(DXMLParser, self).__init__(target=tb)

        p = self._parser if PY2 else self.parser
        p.StartDoctypeDeclHandler = self.nope
        p.EntityDeclHandler = self.nope
        p.UnparsedEntityDeclHandler = self.nope
        p.ExternalEntityRefHandler = self.nope

    def nope(self, *a , **ka )  :
        raise BadXML("{}, {}".format(a, ka))


class _NG(XMLParser):  # type: ignore
    def __int__(self)  :
        raise BadXML("dxml selftest failed")


DXMLParser = _DXMLParser


def parse_xml(txt )  :
    """
    Parse XML into an xml.etree.ElementTree.Element while defusing some unsafe parts.
    """
    parser = DXMLParser()
    parser.feed(txt)
    return parser.close()  # type: ignore


def selftest()  :
    qbe = r"""<!DOCTYPE d [
<!ENTITY a "nice_bakuretsu">
]>
<root>&a;&a;&a;</root>"""

    emb = r"""<!DOCTYPE d [
<!ENTITY a SYSTEM "file:///etc/hostname">
]>
<root>&a;</root>"""

    # future-proofing; there's never been any known vulns
    # regarding DTDs and ET.XMLParser, but might as well
    # block them since webdav-clients don't use them
    dtd = r"""<!DOCTYPE d SYSTEM "a.dtd">
<root>a</root>"""

    for txt in (qbe, emb, dtd):
        try:
            parse_xml(txt)
            t = "WARNING: dxml selftest failed:\n%s\n"
            print(t % (txt,), file=sys.stderr)
            return False
        except BadXML:
            pass

    return True


DXML_OK = selftest()
if not DXML_OK:
    DXMLParser = _NG


def mktnod(name , text )  :
    el = ET.Element(name)
    el.text = text
    return el


def mkenod(name , sub_el  = None)  :
    el = ET.Element(name)
    if sub_el is not None:
        el.append(sub_el)
    return el
