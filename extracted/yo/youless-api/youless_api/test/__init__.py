
URI_ELOGIC = '/e'
URI_DEVICE_INFO = '/d'
URI_GENERIC = '/a?f=j'
URI_PHASES = '/f'


class MockResponse:

    def __init__(self):
        self._ok = False
        self._json = lambda: 0
        self._headers = {}
        self._text = ''

    def setup(self, ok, json, text, headers):
        self._ok = ok
        self._json = json
        self._text = text
        self._headers = headers

    @property
    def ok(self):
        return self._ok

    def json(self):
        return self._json()

    @property
    def headers(self):
        return self._headers
