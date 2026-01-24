from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import Renderer, Factory
from .. import json_

class Renderer(Renderer):

    def render_content(self, context):
        output = context['output']
        if not output.media_type:
            output.media_type = context['request_processor'].media_type_json
        r = json_.dumps(eval(self.compiled, globals(), context))
        if isinstance(r, bytes):
            r = r.decode('ascii')
        return r


class Factory(Factory):
    Renderer = Renderer

