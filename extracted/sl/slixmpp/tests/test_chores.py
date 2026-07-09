import unittest
from pathlib import Path
from xml.etree import ElementTree

from slixmpp.pluginsdict import PluginsDict


class TestChores(unittest.TestCase):
    def test_doap(self) -> None:
        tree = ElementTree.fromstring((ROOT / "doap.xml").read_text())

        listed = set()
        for supported_xep in tree.findall(".//xmpp:SupportedXep", NAMESPACES):
            xep_element = supported_xep.find("xmpp:xep", NAMESPACES)
            if xep_element is not None and xep_element.get(
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
            ):
                xep_url = xep_element.get(
                    "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
                )
                assert xep_url
                listed.add(
                    xep_url.split("/")[-1].removeprefix("xep-").removesuffix(".html")
                )

        self.assertEqual(IMPLEMENTED - UNLISTED_DOAP_XEPS, listed - UNLISTED_DOAP_XEPS)

    def test_plugins_dict_completeness(self) -> None:
        listed_in_plugins_dict = {
            x.removeprefix("xep_")
            for x in PluginsDict.__required_keys__
            if x.startswith("xep_")
        }
        self.assertEqual(IMPLEMENTED, listed_in_plugins_dict)

    def test_plugins_dict_correctness(self) -> None:
        invalid = []
        for xep, cls in PluginsDict.__annotations__.items():
            if not xep.startswith("xep"):
                continue
            if cls.__name__.lower() != xep:
                invalid.append((xep, cls))
        self.assertFalse(invalid)


ROOT = Path(__file__).parent.parent
# some XEPs are implemented, but not as slixmpp plugins
UNLISTED_DOAP_XEPS = {
    "0175",  # SRV records for XMPP over TLS
    "0368",  # XMPP Compliance Suites 2016
    "0478",  # Stream Limits Advertisement
}
IMPLEMENTED = {
    x.stem.split("_")[-1] for x in (ROOT / "slixmpp" / "plugins").glob("xep_*")
}

NAMESPACES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "xmpp": "https://linkmauve.fr/ns/xmpp-doap#",
}


suite = unittest.TestLoader().loadTestsFromTestCase(TestChores)
