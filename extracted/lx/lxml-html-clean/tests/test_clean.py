import base64
import gzip
import io
import unittest
import warnings

import lxml.html
from lxml_html_clean import AmbiguousURLWarning, Cleaner, clean_html, LXMLHTMLCleanWarning
from .utils import peak_memory_usage


class CleanerTest(unittest.TestCase):
    def test_allow_tags(self):
        html = """
            <html>
            <head>
            </head>
            <body>
            <p>some text</p>
            <table>
            <tr>
            <td>hello</td><td>world</td>
            </tr>
            <tr>
            <td>hello</td><td>world</td>
            </tr>
            </table>
            <img>
            </body>
            </html>
            """

        html_root = lxml.html.document_fromstring(html)
        cleaner = Cleaner(
            remove_unknown_tags = False,
            allow_tags = ['table', 'tr', 'td'])
        result = cleaner.clean_html(html_root)

        self.assertEqual(12-5+1, len(list(result.iter())))

    def test_allow_and_remove(self):
        with self.assertRaises(ValueError):
            Cleaner(allow_tags=['a'], remove_unknown_tags=True)

    def test_remove_unknown_tags(self):
        html = """<div><bun>lettuce, tomato, veggie patty</bun></div>"""
        clean_html = """<div>lettuce, tomato, veggie patty</div>"""
        cleaner = Cleaner(remove_unknown_tags=True)
        result = cleaner.clean_html(html)
        self.assertEqual(
            result,
            clean_html,
            msg="Unknown tags not removed. Got: %s" % result,
        )

    def test_safe_attrs_included(self):
        html = """<p><span style="color: #00ffff;">Cyan</span></p>"""

        safe_attrs=set(lxml.html.defs.safe_attrs)
        safe_attrs.add('style')

        cleaner = Cleaner(
            safe_attrs_only=True,
            safe_attrs=safe_attrs)
        result = cleaner.clean_html(html)

        self.assertEqual(html, result)

    def test_safe_attrs_excluded(self):
        html = """<p><span style="color: #00ffff;">Cyan</span></p>"""
        expected = """<p><span>Cyan</span></p>"""

        safe_attrs=set()

        cleaner = Cleaner(
            safe_attrs_only=True,
            safe_attrs=safe_attrs)
        result = cleaner.clean_html(html)

        self.assertEqual(expected, result)

    def test_clean_invalid_root_tag(self):
        # only testing that cleaning with invalid root tags works at all
        s = lxml.html.fromstring('parent <invalid tag>child</another>')
        self.assertEqual('parent child', clean_html(s).text_content())

        s = lxml.html.fromstring('<invalid tag>child</another>')
        self.assertEqual('child', clean_html(s).text_content())

    def test_clean_with_comments(self):
        html = """<p><span style="color: #00ffff;">Cy<!-- xx -->an</span><!-- XXX --></p>"""
        s = lxml.html.fragment_fromstring(html)

        self.assertEqual(
            b'<p><span>Cyan</span></p>',
            lxml.html.tostring(clean_html(s)))
        self.assertEqual(
            '<p><span>Cyan</span></p>',
            clean_html(html))

        cleaner = Cleaner(comments=False)
        result = cleaner.clean_html(s)
        self.assertEqual(
            b'<p><span>Cy<!-- xx -->an</span><!-- XXX --></p>',
            lxml.html.tostring(result))
        self.assertEqual(
            '<p><span>Cy<!-- xx -->an</span><!-- XXX --></p>',
            cleaner.clean_html(html))

    def test_sneaky_noscript_in_style(self):
        # This gets parsed as <noscript> -> <style>"...</noscript>..."</style>
        # thus passing the </noscript> through into the output.
        html = '<noscript><style><a title="</noscript><img src=x onerror=alert(1)>">'
        s = lxml.html.fragment_fromstring(html)

        self.assertEqual(
            b'<noscript><style>/* deleted */</style></noscript>',
            lxml.html.tostring(clean_html(s)))

    def test_sneaky_js_in_math_style(self):
        # This gets parsed as <math> -> <style>"..."</style>
        # thus passing any tag/script/whatever content through into the output.
        html = '<math><style><img src=x onerror=alert(1)></style></math>'
        s = lxml.html.fragment_fromstring(html)

        self.assertEqual(
            b'<math><style>/* deleted */</style></math>',
            lxml.html.tostring(clean_html(s)))

    def test_sneaky_js_in_style_comment_math_svg(self):
        for tag in "svg", "math":
            html = f'<{tag}><style>p {{color: red;}}/*<img src onerror=alert(origin)>*/h2 {{color: blue;}}</style></{tag}>'
            s = lxml.html.fragment_fromstring(html)

            expected = f'<{tag}><style>p {{color: red;}}/* deleted */h2 {{color: blue;}}</style></{tag}>'.encode()

            self.assertEqual(
                expected,
                lxml.html.tostring(clean_html(s)))

    def test_sneaky_js_in_style_comment_noscript(self):
        html = '<noscript><style>p {{color: red;}}/*</noscript><img src onerror=alert(origin)>*/h2 {{color: blue;}}</style></noscript>'
        s = lxml.html.fragment_fromstring(html)

        self.assertEqual(
            b'<noscript><style>p {{color: red;}}/* deleted */h2 {{color: blue;}}</style></noscript>',
            lxml.html.tostring(clean_html(s)))

    def test_sneaky_import_in_style(self):
        # Prevent "@@importimport" -> "@import" replacement etc.
        style_codes = [
            "@@importimport(extstyle.css)",
            "@ @  import import(extstyle.css)",
            "@ @ importimport(extstyle.css)",
            "@@  import import(extstyle.css)",
            "@ @import import(extstyle.css)",
            "@@importimport()",
            "@@importimport()  ()",
            "@/* ... */import()",
            "@im/* ... */port()",
            "@ @import/* ... */import()",
            "@    /* ... */      import()",
        ]
        for style_code in style_codes:
            html = '<style>%s</style>' % style_code
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                b'<style>/* deleted */</style>',
                cleaned,
                "%s  ->  %s" % (style_code, cleaned))

    def test_sneaky_schemes_in_style(self):
        style_codes = [
            "javasjavascript:cript:",
            "javascriptjavascript::",
            "javascriptjavascript:: :",
            "vbjavascript:cript:",
        ]
        for style_code in style_codes:
            html = '<style>%s</style>' % style_code
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                b'<style>/* deleted */</style>',
                cleaned,
                "%s  ->  %s" % (style_code, cleaned))

    def test_sneaky_urls_in_style(self):
        style_codes = [
            "url(data:image/svg+xml;base64,...)",
            "url(javasjavascript:cript:)",
            "url(javasjavascript:cript: ::)",
            "url(vbjavascript:cript:)",
            "url(vbjavascript:cript: :)",
        ]
        for style_code in style_codes:
            html = '<style>%s</style>' % style_code
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                b'<style>url()</style>',
                cleaned,
                "%s  ->  %s" % (style_code, cleaned))

    def test_svg_data_links(self):
        # Remove SVG images with potentially insecure content.
        svg = b'<svg onload="alert(123)" />'
        gzout = io.BytesIO()
        f = gzip.GzipFile(fileobj=gzout, mode='wb')
        f.write(svg)
        f.close()
        svgz = gzout.getvalue()
        svg_b64 = base64.b64encode(svg).decode('ASCII')
        svgz_b64 = base64.b64encode(svgz).decode('ASCII')
        urls = [
            "data:image/svg+xml;base64," + svg_b64,
            "data:image/svg+xml-compressed;base64," + svgz_b64,
        ]
        for url in urls:
            html = '<img src="%s">' % url
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                b'<img src="">',
                cleaned,
                "%s  ->  %s" % (url, cleaned))

    def test_image_data_links(self):
        data = b'123'
        data_b64 = base64.b64encode(data).decode('ASCII')
        urls = [
            "data:image/jpeg;base64," + data_b64,
            "data:image/apng;base64," + data_b64,
            "data:image/png;base64," + data_b64,
            "data:image/gif;base64," + data_b64,
            "data:image/webp;base64," + data_b64,
            "data:image/bmp;base64," + data_b64,
            "data:image/tiff;base64," + data_b64,
            "data:image/x-icon;base64," + data_b64,
        ]
        for url in urls:
            html = '<img src="%s">' % url
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                html.encode("UTF-8"),
                cleaned,
                "%s  ->  %s" % (url, cleaned))

    def test_image_data_links_in_style(self):
        data = b'123'
        data_b64 = base64.b64encode(data).decode('ASCII')
        urls = [
            "data:image/jpeg;base64," + data_b64,
            "data:image/apng;base64," + data_b64,
            "data:image/png;base64," + data_b64,
            "data:image/gif;base64," + data_b64,
            "data:image/webp;base64," + data_b64,
            "data:image/bmp;base64," + data_b64,
            "data:image/tiff;base64," + data_b64,
            "data:image/x-icon;base64," + data_b64,
        ]
        for url in urls:
            html = '<style> url(%s) </style>' % url
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(clean_html(s))
            self.assertEqual(
                html.encode("UTF-8"),
                cleaned,
                "%s  ->  %s" % (url, cleaned))

    def test_image_data_links_in_inline_style(self):
        safe_attrs = set(lxml.html.defs.safe_attrs)
        safe_attrs.add('style')

        cleaner = Cleaner(
            safe_attrs_only=True,
            safe_attrs=safe_attrs)

        data = b'123'
        data_b64 = base64.b64encode(data).decode('ASCII')
        url = "url(data:image/jpeg;base64,%s)" % data_b64
        styles = [
            "background: %s" % url,
            "background: %s; background-image: %s" % (url, url),
        ]
        for style in styles:
            html = '<div style="%s"></div>' % style
            s = lxml.html.fragment_fromstring(html)

            cleaned = lxml.html.tostring(cleaner.clean_html(s))
            self.assertEqual(
                html.encode("UTF-8"),
                cleaned,
                "%s  ->  %s" % (style, cleaned))

    def test_formaction_attribute_in_button_input(self):
        # The formaction attribute overrides the form's action and should be
        # treated as a malicious link attribute
        html = ('<form id="test"><input type="submit" formaction="javascript:alert(1)"></form>'
        '<button form="test" formaction="javascript:alert(1)">X</button>')
        expected = ('<div><form id="test"><input type="submit" formaction=""></form>'
        '<button form="test" formaction="">X</button></div>')
        cleaner = Cleaner(
            forms=False,
            safe_attrs_only=False,
        )
        self.assertEqual(
            expected,
            cleaner.clean_html(html))

    def test_host_whitelist_slash_type_confusion(self):
        # Regression test: Accidentally passing a string when a 1-tuple was intended
        # creates a host_whitelist of the empty string; a malformed triple-slash
        # URL has an "empty host" according to urlsplit, and `"" in ""` passes.
        # So, don't allow user to accidentally pass a string for host_whitelist.
        html = '<div><iframe src="https:///evil.com/page"></div>'
        with self.assertRaises(TypeError) as exc:
            # If this were the intended `("example.com",)` the expected
            # output would be '<div></div>'
            Cleaner(frames=False, host_whitelist=("example.com")).clean_html(html)

        self.assertEqual(("Expected a collection, got str: host_whitelist='example.com'",), exc.exception.args)

    def test_host_whitelist_valid(self):
        # Frame with valid hostname in src is allowed.
        html = '<div><iframe src="https://example.com/page"></div>'
        expected = '<div><iframe src="https://example.com/page"></iframe></div>'
        cleaner = Cleaner(frames=False, host_whitelist=["example.com"])
        self.assertEqual(expected, cleaner.clean_html(html))

    def test_host_whitelist_invalid(self):
        html = '<div><iframe src="https://evil.com/page"></div>'
        expected = '<div></div>'
        cleaner = Cleaner(frames=False, host_whitelist=["example.com"])
        self.assertEqual(expected, cleaner.clean_html(html))

    def test_host_whitelist_sneaky_userinfo(self):
        # Regression test: Don't be fooled by hostname and colon in userinfo.
        html = '<div><iframe src="https://example.com:@evil.com/page"></div>'
        expected = '<div></div>'
        cleaner = Cleaner(frames=False, host_whitelist=["example.com"])
        self.assertEqual(expected, cleaner.clean_html(html))

    def test_ascii_control_chars_removed(self):
        html = """<a href="java\x1bscript:alert()">Link</a>"""
        expected = """<a href="">Link</a>"""
        cleaner = Cleaner()
        self.assertEqual(expected, cleaner.clean_html(html))

    def test_ascii_control_chars_removed_from_bytes(self):
        html = b"""<a href="java\x1bscript:alert()">Link</a>"""
        expected = b"""<a href="">Link</a>"""
        cleaner = Cleaner()
        self.assertEqual(expected, cleaner.clean_html(html))

    def test_memory_usage_many_elements_with_long_tails(self):
        comment = "<!-- foo bar baz -->\n"
        empty_line = "\t" * 10 + "\n"
        element = comment + empty_line * 10
        content = element * 5_000
        html = f"<html>{content}</html>"

        cleaner = Cleaner()
        mem = peak_memory_usage(cleaner.clean_html, html)

        self.assertTrue(mem < 10, f"Used {mem} MiB memory, expected at most 10 MiB")

    def test_possibly_invalid_url_with_whitelist(self):
        cleaner = Cleaner(host_whitelist=['google.com'])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = cleaner.clean_html(r"<p><iframe src='http://example.com:\@google.com'>  </iframe></p>")
            self.assertGreaterEqual(len(w), 1)
            self.assertIs(w[-1].category, AmbiguousURLWarning)
            self.assertTrue(issubclass(w[-1].category, LXMLHTMLCleanWarning))
            self.assertIn("impossible to parse the hostname", str(w[-1].message))
        self.assertNotIn("google.com", result)
        self.assertNotIn("example.com", result)

    def test_possibly_invalid_url_without_whitelist(self):
        cleaner = Cleaner()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = cleaner.clean_html(r"<p><iframe src='http://example.com:\@google.com'>  </iframe></p>")
            self.assertEqual(len(w), 0)
        self.assertNotIn("google.com", result)
        self.assertNotIn("example.com", result)
