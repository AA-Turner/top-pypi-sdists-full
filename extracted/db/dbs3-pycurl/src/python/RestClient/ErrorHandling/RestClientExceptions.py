class ClientAuthException(Exception):
    def __init__(self, msg):
        self._msg = msg
        super(ClientAuthException, self).__init__(self, "ClientAuthException %s" % self._msg)

    def __repr__(self):
        return ('%s %r' % (self.__class__.__name__, self._msg))

    def __str__(self):
        return repr(self._msg)

class HTTPError(Exception):
    def __init__(self, url, code, msg, header, body, server_code=0):
        """
        HTTPError class represents generic HTTPError used by DBS and WMcore
        :param url: url of the client HTTP request
        :param code: HTTP code
        :param msg: message associated with error
        :param header: HTTP response header
        :param body: HTTP response body
        :param server_code: HTTP back-end server code, e.g. HTTP server may response with
        400 Bad request, but actual HTTP server (DBS) code may be something different
        to indicate actual problem. This parameter is made optional for backward compatibility.
        """
        self.url = url
        self.code = code
        self.server_code = server_code
        self.msg = msg
        self.header = header
        self.body = body
        super(HTTPError, self).__init__(self, "HTTPError %d (server code %s)" % (self.code, self.server_code))

    def __repr__(self):
        return ('%s %r, server code %s' % (self.__class__.__name__, self.code, self.server_code))

    def __str__(self):
        return ('HTTP Error %d: %s' % (self.code, self.msg))
