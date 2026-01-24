from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import Factory
from .json_dump import Renderer as JsonRenderer

import re

CALLBACK_RE = re.compile(r'[^_a-zA-Z0-9]')


class Renderer(JsonRenderer):
    """A JSON renderer that also supports JSONP.

    .. note:: This renderer needs access to the HTTP querystring. It expects a
              dict-like object stored as :obj:`'querystring'` in the context.

    .. warning:: JSONP can lead to information disclosure vulnerabilities
                 (`example <https://hackerone.com/reports/361951>`_).

    """

    def render_content(self, context):
        # get the jsonp callback
        qs = context['querystring']
        callback = qs.get('callback', qs.get('jsonp', None))

        # get the json
        json = JsonRenderer.render_content(self, context)

        # return the json if no callback requested
        if callback is None:
            return json

        output = context['output']

        # jsonp requested; fix the content-type
        output.media_type = 'application/javascript'

        # sanify/sanitize the callback by nuking invalid characters
        callback = CALLBACK_RE.sub('', callback)

        # return the wrapped json
        # (preceding comment block prevent a Rosetta-Flash based attack)
        return "/**/ " + callback + "(" + json + ");"


class Factory(Factory):
    Renderer = Renderer
