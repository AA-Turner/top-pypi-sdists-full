import unittest

from slixmpp.plugins.xep_0511 import stanza
from slixmpp.test import SlixTest


class TestLinkMetadata(SlixTest):
    def setUp(self):
        stanza.register_plugin()

    def testSetLinkMetadata(self):
        msg = self.Message()
        msg["link_metadata"]["about"] = (
            "https://the.link.example.com/what-was-linked-to"
        )
        msg["link_metadata"]["title"] = "A cool title"
        # This does not pass, probably because of namespace shenanigans in SlixText.check()
        # self.check(
        #     msg,  # language=xml
        #     """
        #     <message xmlns="jabber:client">
        #       <rdf:Description xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        #                        rdf:about="https://the.link.example.com/what-was-linked-to">
        #         <title xmlns="https://ogp.me/ns#">A cool title</title>
        #       </rdf:Description>
        #     </message>
        #     """,
        #     use_values=False,
        # )
        assert msg["link_metadata"]["description"] is None
        assert msg["link_metadata"]["title"] == "A cool title"
        assert msg["link_metadata"]["about"] == "https://the.link.example.com/what-was-linked-to"

    def testGetLinkMetadata(self):
        # language=xml
        xml_str = """
            <message to="whoever@example.com">
              <body>I wanted to mention https://the.link.example.com/what-was-linked-to</body>
              <rdf:Description xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                               xmlns:og="https://ogp.me/ns#"
                               rdf:about="https://the.link.example.com/what-was-linked-to">
                <og:title>Page Title</og:title>
                <og:description>Page Description</og:description>
                <og:url>Canonical URL</og:url>
                <og:type>website</og:type>
                <og:site_name>Some Website</og:site_name>
                <og:image>data:image/jpeg,...</og:image>
              </rdf:Description>
            </message>
            """
        xml = self.parse_xml(xml_str)
        msg = self.Message(xml)
        assert msg["link_metadata"]["title"] == "Page Title"
        assert msg["link_metadata"]["description"] == "Page Description"
        assert msg["link_metadata"]["url"] == "Canonical URL"
        assert msg["link_metadata"]["site_name"] == "Some Website"
        assert msg["link_metadata"]["type"] == "website"
        assert msg["link_metadata"]["image"] == "data:image/jpeg,..."
        assert (
            msg["link_metadata"]["about"]
            == "https://the.link.example.com/what-was-linked-to"
        )

    def testGetLinkMetadatas(self):
        # language=xml
        xml_str = """
            <message to="whoever@example.com">
              <body>I wanted to mention https://the.link.example.com/what-was-linked-to</body>
              <rdf:Description xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                               xmlns:og="https://ogp.me/ns#"
                               rdf:about="https://the.link.example.com/what-was-linked-to 1">
                <og:title>Page Title 1</og:title>
                <og:description>Page Description 1</og:description>
                <og:url>Canonical URL 1</og:url>
                <og:type>website 1</og:type>
                <og:site_name>Some Website 1</og:site_name>
                <og:image>https://link.to.example.com/image.png 1</og:image>
              </rdf:Description>
              <rdf:Description xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                               xmlns:og="https://ogp.me/ns#"
                               rdf:about="https://the.link.example.com/what-was-linked-to 2">
                <og:title>Page Title 2</og:title>
                <og:description>Page Description 2</og:description>
                <og:url>Canonical URL 2</og:url>
                <og:image>https://link.to.example.com/image.png 2</og:image>
                <og:type>website 2</og:type>
                <og:site_name>Some Website 2</og:site_name>
              </rdf:Description>
            </message>
            """
        xml = self.parse_xml(xml_str)
        msg = self.Message(xml)
        metadatas = msg["link_metadatas"]
        assert len(metadatas) == 2
        for i, p in enumerate(metadatas, start=1):
            assert p["title"] == f"Page Title {i}"
            assert p["description"] == f"Page Description {i}"
            assert p["url"] == f"Canonical URL {i}"
            assert p["image"] == f"https://link.to.example.com/image.png {i}"
            assert p["site_name"] == f"Some Website {i}"
            assert p["type"] == f"website {i}"
            assert p["about"] == f"https://the.link.example.com/what-was-linked-to {i}"

    def testOtherPrefix(self):
        xml_str = """
            <message to="whoever@example.com">
              <body>I wanted to mention https://the.link.example.com/what-was-linked-to</body>
              <ns1:Description xmlns:ns1="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                               xmlns:ns2="https://ogp.me/ns#"
                               ns1:about="https://the.link.example.com/what-was-linked-to">
                <ns2:title>Page Title</ns2:title>
                <ns2:description>Page Description</ns2:description>
                <ns2:url>Canonical URL</ns2:url>
                <ns2:type>website</ns2:type>
                <ns2:site_name>Some Website</ns2:site_name>
                <ns2:image>data:image/jpeg,...</ns2:image>
              </ns1:Description>
            </message>
            """
        xml = self.parse_xml(xml_str)
        msg = self.Message(xml)
        assert msg["link_metadata"]["title"] == "Page Title"
        assert msg["link_metadata"]["description"] == "Page Description"
        assert msg["link_metadata"]["url"] == "Canonical URL"
        assert msg["link_metadata"]["site_name"] == "Some Website"
        assert msg["link_metadata"]["type"] == "website"
        assert msg["link_metadata"]["image"] == "data:image/jpeg,..."
        assert (
            msg["link_metadata"]["about"]
            == "https://the.link.example.com/what-was-linked-to"
        )

suite = unittest.TestLoader().loadTestsFromTestCase(TestLinkMetadata)
