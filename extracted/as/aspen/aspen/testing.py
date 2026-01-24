"""
This module provides helpers for testing applications that use Aspen.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from contextlib import contextmanager
import os
import sys

from filesystem_tree import FilesystemTree

from .http.request import Path, Querystring
from .request_processor import RequestProcessor
from .request_processor.dispatcher import TestDispatcher


CWD = os.getcwd()


def teardown():
    """Standard teardown function.

    - reset the current working directory
    - remove FSFIX = %{tempdir}/fsfix
    - clear out sys.path_importer_cache

    """
    os.chdir(CWD)
    # Reset some process-global caches. Hrm ...
    sys.path_importer_cache = {} # see test_weird.py

teardown() # start clean


def resolve_want(available, want):
    if '.' in want:
        attr_path = want.split('.')
        base, attr_path = attr_path[0], attr_path[1:]
    else:
        base, attr_path = want, None
    try:
        out = available[base]
    except KeyError as e:
        raise KeyError('%r not found. available = %r' % (e, available))
    if attr_path:
        try:
            for name in attr_path:
                out = getattr(out, name)
        except AttributeError as e:
            raise AttributeError('%r not found. out = %r' % (e, out))
    return out


class FileSystem(object):
    __slots__ = ('project', 'www')

    def __init__(self):
        self.project = FilesystemTree()
        self.www = FilesystemTree()


class Harness(object):
    """A harness to be used in the Aspen test suite itself. Probably not useful to you.
    """

    def __init__(self):
        self.fs = FileSystem()
        self._request_processor = None

    def teardown(self):
        self.fs.www.remove()
        self.fs.project.remove()

    def hydrate_request_processor(self, **kwargs):
        if (self._request_processor is None) or kwargs:
            _kwargs = { 'www_root': self.fs.www.root
                      , 'project_root': self.fs.project.root
                      , 'dispatcher_class': TestDispatcher
                       }
            _kwargs.update(kwargs)
            self._request_processor = RequestProcessor(**_kwargs)
        return self._request_processor

    request_processor = property(hydrate_request_processor)

    def simple(self, contents='Greetings, program!', filepath='index.html.spt', uripath=None,
            querystring='', request_processor_configuration=None, **kw):
        """A helper to create a file and hit it through our machinery.
        """
        if filepath is not None:
            if isinstance(contents, tuple):
                contents, encoding = contents
            else:
                encoding = 'utf8'
            self.fs.www.mk((filepath, contents, True, encoding))
            if self._request_processor:
                # Rebuild the dispatch tree since we've just added a file
                self._request_processor.dispatcher.build_dispatch_tree()
        if request_processor_configuration is not None:
            self.hydrate_request_processor(**request_processor_configuration)

        if uripath is None:
            if filepath is None:
                uripath = '/'
            else:
                uripath = '/' + filepath
                if uripath.endswith('.spt'):
                    uripath = uripath[:-len('.spt')]
                for indexname in self.request_processor.indices:
                    if uripath.endswith(indexname):
                        uripath = uripath[:-len(indexname)]
                        break

        return self.hit(uripath, querystring, **kw)

    def hit(self, path, querystring='', accept_header=None, want=None, **context):
        path = context['path'] = Path(path)
        querystring = Querystring(querystring)
        dispatch_result, resource, output = self.request_processor.process(
            path, querystring, accept_header, context
        )
        if want is None:
            return output
        return resolve_want(locals(), want)


@contextmanager
def chdir(path):
    """A context manager that temporarily changes the working directory.
    """
    back_to = os.getcwd()
    os.chdir(path)
    try:
        yield back_to
    finally:
        os.chdir(back_to)
