from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from pytest import raises, mark

from aspen.request_processor import ConfigurationError, RequestProcessor
from aspen.testing import chdir


def test_defaults_to_defaults(harness):
    os.chdir(harness.fs.www.root)
    rp = RequestProcessor()
    actual = ( rp.project_root
             , rp.www_root

             , rp.changes_reload
             , rp.charset_static
             , rp.encode_output_as
             , rp.indices
             , rp.media_type_default
             , rp.media_type_json
             , rp.renderer_default
              )
    expected = ( None, os.getcwd(), False, None, 'UTF-8'
               , ['index.html', 'index.json', 'index', 'index.html.spt', 'index.json.spt', 'index.spt']
               , 'text/plain', 'application/json', 'stdlib_percent'
                )
    assert actual == expected

@mark.skipif(sys.platform == 'win32',
             reason="Windows file locking makes this fail")
def test_ConfigurationError_raised_if_no_cwd(harness):
    FSFIX = harness.fs.project.resolve('')
    os.chdir(FSFIX)
    os.rmdir(FSFIX)
    raises(ConfigurationError, RequestProcessor)

@mark.skipif(sys.platform == 'win32',
             reason="Windows file locking makes this fail")
def test_ConfigurationError_NOT_raised_if_no_cwd_but_do_have__www_root(harness):
    project_root = harness.fs.project.root
    www_root = harness.fs.www.root
    with chdir(project_root):
        os.rmdir(project_root)
        rp = RequestProcessor(www_root=www_root)
        assert rp.www_root == www_root

def test_processor_sees_root_option(harness):
    rp = RequestProcessor(www_root=harness.fs.project.resolve(''))
    expected = harness.fs.project.root
    actual = rp.www_root
    assert actual == expected

def test_user_can_set_renderer_default(harness):
    SIMPLATE = """
[----]
name="program"
[----]
Greetings, {name}!
    """
    harness.fs.www.mk(('index.html.spt', SIMPLATE),)
    harness.hydrate_request_processor(renderer_default="stdlib_format")
    actual = harness.simple(filepath=None, uripath='/', want='output.text')
    assert actual == 'Greetings, program!\n'
