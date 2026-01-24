# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from pytest import raises, fixture

from aspen.exceptions import NegotiationFailure, NotFound
from aspen.http.resource import mimetypes
from aspen.simplates.simplate import _decode
from aspen.simplates.simplate import Simplate
from aspen.simplates.pagination import Page
from aspen.simplates.renderers.stdlib_template import Factory as TemplateFactory
from aspen.simplates.renderers.stdlib_percent import Factory as PercentFactory


@fixture
def make_simplate(harness):
    def get(fspath='index.spt', raw=b'[---]\n[---] text/plain via stdlib_template\n'):
        harness.fs.www.mk((fspath, raw, False))
        return Simplate(harness.request_processor, harness.fs.www.resolve(fspath))
    yield get


def test_dynamic_resource_is_instantiable(make_simplate):
    actual = make_simplate().__class__
    assert actual is Simplate


def test_duplicate_media_type_causes_SyntaxError(make_simplate):
    with raises(SyntaxError):
        make_simplate(raw=b"[---]\n[---] text/plain\n[---] text/plain\n")


# compile_page

def test_compile_page_compiles_empty_page(make_simplate):
    page = make_simplate().compile_page(Page('', 'text/html'))
    actual = page[0]({}), page[1]
    assert actual == ('', 'text/html')

def test_compile_page_compiles_page(make_simplate):
    page = make_simplate().compile_page(Page('foo bar', 'text/html'))
    actual = page[0]({}), page[1]
    assert actual == ('foo bar', 'text/html')


# _parse_specline

def test_parse_specline_parses_specline(make_simplate):
    factory, media_type = make_simplate()._parse_specline('media/type via stdlib_template')
    actual = (factory.__class__, media_type)
    assert actual == (TemplateFactory, 'media/type')

def test_parse_specline_doesnt_require_renderer(make_simplate):
    factory, media_type = make_simplate()._parse_specline('media/type')
    actual = (factory.__class__, media_type)
    assert actual == (PercentFactory, 'media/type')

def test_parse_specline_doesnt_require_media_type(harness, make_simplate):
    factory, media_type = make_simplate()._parse_specline('via stdlib_template')
    actual = (factory.__class__, media_type)
    assert actual == (TemplateFactory, harness.request_processor.media_type_default)

def test_parse_specline_raises_SyntaxError_if_renderer_is_malformed(make_simplate):
    with raises(SyntaxError):
        make_simplate()._parse_specline('stdlib_template media/type')

def test_parse_specline_raises_SyntaxError_if_media_type_is_malformed(make_simplate):
    with raises(SyntaxError):
        make_simplate()._parse_specline('media-type via stdlib_template')

def test_parse_specline_cant_mistake_malformed_media_type_for_renderer(make_simplate):
    with raises(SyntaxError):
        make_simplate()._parse_specline('media-type')

def test_parse_specline_cant_mistake_malformed_renderer_for_media_type(make_simplate):
    with raises(SyntaxError):
        make_simplate()._parse_specline('stdlib_template')

def test_parse_specline_enforces_order(make_simplate):
    with raises(SyntaxError):
        make_simplate()._parse_specline('stdlib_template via media/type')

def test_parse_specline_obeys_default_by_media_type(make_simplate):
    resource = make_simplate()
    resource.default_renderers_by_media_type['media/type'] = 'glubber'
    err = raises(ValueError, resource._parse_specline, 'media/type').value
    msg = err.args[0]
    assert msg.startswith("Unknown renderer for media/type: glubber."), msg

def test_parse_specline_obeys_default_by_media_type_default(make_simplate):
    resource = make_simplate()
    resource.default_renderers_by_media_type.default_factory = lambda: 'glubber'
    err = raises(ValueError, resource._parse_specline, 'media/type').value
    msg = err.args[0]
    assert msg.startswith("Unknown renderer for media/type: glubber.")

def test_get_renderer_factory_can_raise_syntax_error(make_simplate):
    resource = make_simplate()
    resource.default_renderers_by_media_type['media/type'] = 'glubber'
    err = raises( SyntaxError
                       , resource._get_renderer_factory
                       , 'media/type'
                       , 'oo*gle'
                        ).value
    msg = err.args[0]
    assert msg.startswith("Malformed renderer oo*gle. It must match")


# render

SIMPLATE = """\
[---]
[---] text/plain
Greetings, program!
[---] text/html
<h1>Greetings, program!</h1>
"""

def test_render_is_happy_not_to_negotiate(harness):
    output = harness.simple(filepath='index.spt', contents=SIMPLATE)
    assert output.text == "Greetings, program!\n"

def test_render_sets_media_type_when_it_doesnt_negotiate(harness):
    output = harness.simple(filepath='index.spt', contents=SIMPLATE)
    assert output.media_type == "text/plain"

def test_render_is_happy_not_to_negotiate_with_defaults(harness):
    output = harness.simple(filepath='index.spt', contents="[---]\n[---]\nGreetings, program!\n")
    assert output.text == "Greetings, program!\n"

def test_render_negotiates(harness):
    output = harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='text/html')
    assert output.text == "<h1>Greetings, program!</h1>\n"

def test_ignores_busted_accept(harness):
    output = harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='text/html/foo')
    assert output.text == "Greetings, program!\n"

def test_render_sets_media_type_when_it_negotiates(harness):
    output = harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='text/html')
    assert output.media_type == "text/html"

def test_render_raises_if_direct_negotiation_fails(harness):
    with raises(NegotiationFailure):
        harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='cheese/head')

def test_render_negotation_failures_include_available_types(harness):
    actual = raises(
        NegotiationFailure,
        harness.simple, filepath='index.spt', contents=SIMPLATE, accept_header='cheese/head'
    ).value.message
    expected = "Couldn't satisfy cheese/head. The following media types are available: " \
               "text/plain, text/html."
    assert actual == expected

def test_treat_media_type_variants_as_equivalent(harness):
    _guess_type = mimetypes.guess_type
    mimetypes.guess_type = lambda url, **kw: ('application/x-javascript' if url.endswith('.js') else '', None)
    try:
        output = harness.simple(
            filepath='foobar.spt',
            contents="[---]\n[---] application/javascript\n[---] text/plain\n",
            uripath='/foobar.js',
        )
        assert output.media_type == "application/javascript"
    finally:
        mimetypes.guess_type = _guess_type


from aspen.simplates.renderers import Renderer, Factory

class Glubber(Renderer):
    def render_content(self, context):
        return "glubber"

class GlubberFactory(Factory):
    Renderer = Glubber

class glubber:

    def __init__(self, harness):
        self.harness = harness

    def __enter__(self):
        Simplate.renderer_factories['glubber'] = GlubberFactory(self.harness.request_processor)
        self.__old = Simplate.default_renderers_by_media_type['text/plain']
        Simplate.default_renderers_by_media_type['text/plain'] = 'glubber'

    def __exit__(self, *a, **kw):
        del Simplate.renderer_factories['glubber']
        Simplate.default_renderers_by_media_type['text/plain'] = self.__old


def test_can_override_default_renderers_by_mimetype(harness):
    with glubber(harness):
        harness.fs.www.mk(('index.spt', SIMPLATE),)
        output = harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='text/plain')
        assert output.text == "glubber"

def test_can_override_default_renderer_entirely(harness):
    with glubber(harness):
        output = harness.simple(filepath='index.spt', contents=SIMPLATE, accept_header='text/plain')
        assert output.text == "glubber"


# indirect

INDIRECTLY_NEGOTIATED_SIMPLATE = """\
[-------]
foo = "program"
[-------] text/html
<h1>Greetings, %(foo)s!</h1>
[-------] text/plain
Greetings, %(foo)s!"""

def test_indirect_negotiation_sets_media_type(harness):
    output = harness.simple(INDIRECTLY_NEGOTIATED_SIMPLATE, '/foo.spt', '/foo.html')
    expected = "<h1>Greetings, program!</h1>\n"
    actual = output.text
    assert actual == expected

def test_indirect_negotiation_sets_media_type_to_secondary(harness):
    output = harness.simple(INDIRECTLY_NEGOTIATED_SIMPLATE, '/foo.spt', '/foo.txt')
    expected = "Greetings, program!"
    actual = output.text
    assert actual == expected

def test_indirect_negotiation_with_unsupported_media_type_is_an_error(harness):
    with raises(NotFound):
        harness.simple(INDIRECTLY_NEGOTIATED_SIMPLATE, '/foo.spt', '/foo.jpg')


SIMPLATE_VIRTUAL_PATH = """\
[-------]
foo = path['foo']
[-------] text/html
<h1>Greetings, %(foo)s!</h1>
[-------] text/plain
Greetings, %(foo)s!"""


def test_dynamic_resource_inside_virtual_path(harness):
    output = harness.simple(SIMPLATE_VIRTUAL_PATH, '/%foo/bar.spt', '/program/bar.txt')
    expected = "Greetings, program!"
    actual = output.text
    assert actual == expected

SIMPLATE_STARTYPE = """\
[-------]
foo = path['foo']
[-------] */*
Unknown request type, %(foo)s!
[-------] text/html
<h1>Greetings, %(foo)s!</h1>
[-------] text/*
Greetings, %(foo)s!"""

def test_dynamic_resource_inside_virtual_path_with_startypes_present(harness):
    output = harness.simple(SIMPLATE_STARTYPE, '/%foo/bar.spt', '/program/bar.html')
    actual = output.text
    assert '<h1>' in actual

def test_dynamic_resource_inside_virtual_path_with_startype_partial_match(harness):
    output = harness.simple(SIMPLATE_STARTYPE, '/%foo/bar.spt', '/program/bar.txt')
    expected = "Greetings, program!"
    actual = output.text
    assert actual == expected

def test_dynamic_resource_inside_virtual_path_with_startype_fallback(harness):
    output = harness.simple(SIMPLATE_STARTYPE, '/%foo/bar.spt', '/program/bar.jpg')
    expected = "Unknown request type, program!"
    actual = output.text.strip()
    assert actual == expected


def test_default_media_type_works(harness):
    output = harness.simple("""
[---]
[---]
plaintext""")
    assert "plaintext" in output.text


def test_but_python_sections_exhibit_module_scoping_behavior(harness):
    output = harness.simple("""[---]
bar = 'baz'
def foo():
    return bar
foo = foo()
[---] text/html via stdlib_format
{foo}""")
    assert output.text == 'baz'


def test_one_page_works(harness):
    output = harness.simple("Template")
    assert output.text == 'Template'


def test_two_pages_works(harness):
    output = harness.simple("""
foo = 'Template'
[---] via stdlib_format
{foo}""")
    assert output.text == 'Template'


def test_three_pages_one_python_works(harness):
    output = harness.simple("""
foo = 'Template'
[---] text/plain via stdlib_format
{foo}
[---] text/xml
<foo>{foo}</foo>""", filepath='index.spt')
    assert output.text.strip() == 'Template'


def test_three_pages_two_python_works(harness):
    output = harness.simple("""[---]
python_code = True
[---]
Template""")
    assert output.text == 'Template'


# _decode

def test_decode_can_take_encoding_from_first_line():
    actual = _decode("""\
    # -*- coding: utf8 -*-
    text = u'א'
    """.encode('utf8'))
    expected = """\
    # encoding set to utf8
    text = u'א'
    """
    assert actual == expected

def test_decode_can_take_encoding_from_second_line():
    actual = _decode("""\
    #!/blah/blah
    # -*- coding: utf8 -*-
    text = u'א'
    """.encode('utf8'))
    expected = """\
    #!/blah/blah
    # encoding set to utf8
    text = u'א'
    """
    assert actual == expected

def test_decode_prefers_first_line_to_second():
    actual = _decode("""\
    # -*- coding: utf8 -*-
    # -*- coding: ascii -*-
    text = u'א'
    """.encode('utf8'))
    expected = """\
    # encoding set to utf8
    # encoding NOT set to ascii
    text = u'א'
    """
    assert actual == expected

def test_decode_ignores_third_line():
    actual = _decode("""\
    # -*- coding: utf8 -*-
    # -*- coding: ascii -*-
    # -*- coding: cornnuts -*-
    text = u'א'
    """.encode('utf8'))
    expected = """\
    # encoding set to utf8
    # encoding NOT set to ascii
    # -*- coding: cornnuts -*-
    text = u'א'
    """
    assert actual == expected

formats = [ '-*- coding: utf8 -*-'
          , '-*- encoding: utf8 -*-'
          , 'coding: utf8'
          , '  coding: utf8'
          , '\tencoding: utf8'
          , '\t flubcoding=utf8'
           ]
@pytest.mark.parametrize('fmt', formats)
def test_decode_can_take_encoding_from_various_line_formats(fmt):
    actual = _decode("""\
    # {0}
    text = u'א'
    """.format(fmt).encode('utf8'))
    expected = """\
    # encoding set to utf8
    text = u'א'
    """
    assert actual == expected

formats = [ '-*- coding : utf8 -*-'
          , 'foo = 0 -*- encoding: utf8 -*-'
          , '  coding : utf8'
          , 'encoding : utf8'
          , '  flubcoding =utf8'
          , 'coding: '
           ]
@pytest.mark.parametrize('fmt', formats)
def test_decode_cant_take_encoding_from_bad_line_formats(fmt):
    def test():
        raw = """\
        # {0}
        text = u'א'
        """.format(fmt).encode('utf8')
        raises(UnicodeDecodeError, _decode, raw)
