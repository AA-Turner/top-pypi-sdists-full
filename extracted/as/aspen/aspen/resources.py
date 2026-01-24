from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import stat


class Entry(object):
    """An entry in a resource cache.
    """
    __slots__ = ('fspath', 'mtime', 'resource')

    def __init__(self, fspath, mtime, resource):
        #: The filesystem path [string]
        self.fspath = fspath
        #: The timestamp of the last change [int]
        self.mtime = mtime
        #: The loaded resource [Static or Dynamic]
        self.resource = resource


class Resources(object):
    """This class implements loading resources, and caching them.
    """

    __slots__ = ('request_processor', 'cache')

    def __init__(self, request_processor):
        self.request_processor = request_processor
        self.cache = {}

    def get(self, fspath):
        """Return a resource object, with caching.
        """

        # Get a cache Entry object.
        entry = self.cache.get(fspath)

        # Process the resource.
        if not entry or self.request_processor.changes_reload:
            mtime = os.stat(fspath)[stat.ST_MTIME]
            if getattr(entry, 'mtime', None) != mtime:  # cache miss
                resource = self.load(fspath)
                entry = self.cache[fspath] = Entry(fspath, mtime, resource)

        return entry.resource

    def load(self, fspath):
        """Create and return a resource object, without caching.
        """
        Class = self.request_processor.get_resource_class(fspath)
        return Class(self.request_processor, fspath)
