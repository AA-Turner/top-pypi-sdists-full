from .utils import auto_repr


@auto_repr
class Output(object):
    """The result of rendering a resource.
    """

    __slots__ = ('body', 'media_type', 'charset')

    def __init__(self, body=None, media_type=None, charset=None):
        self.body = body
        self.media_type = media_type
        self.charset = charset

    @property
    def text(self):
        return self.body.decode(self.charset) if self.charset else None
