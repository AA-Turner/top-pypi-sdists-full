from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from aspen.request_processor import RequestProcessor
from aspen.testing import chdir


def test_basic(harness):
    with chdir(harness.fs.www.root):
        rp = RequestProcessor()
        expected = os.getcwd()
        actual = rp.www_root
        assert actual == expected

def test_processor_can_process(harness):
    output = harness.simple('[---]\n[---]\nGreetings, program!', 'index.html.spt')
    assert output.text == 'Greetings, program!'

def test_user_can_influence_render_context(harness):
    assert harness.simple('[---]\n[---]\n%(foo)s', 'index.html.spt', foo='bar').text == 'bar'

def test_resources_can_import_from_project_root(harness):
    harness.fs.project.mk(('foo.py', 'bar = "baz"'))
    assert harness.simple( "from foo import bar\n[---]\n[---]\nGreetings, %(bar)s!"
                         , 'index.html.spt').text == "Greetings, baz!"
