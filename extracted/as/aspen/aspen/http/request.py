from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import PY2, text_type as str
from six.moves.urllib.parse import parse_qs, unquote, unquote_plus

from .mapping import Mapping


def _decode(o, errors='strict'):
    return o.decode('utf8', errors=errors) if isinstance(o, bytes) else o


def path_decode(bs):
    return _decode(unquote(bs.encode('ascii') if PY2 else bs))


class PathPart(str):
    """Represents a segment of a URL path.

    Attributes:
        params (Mapping): extra data attached to this segment
    """

    __slots__ = ['params']

    def __new__(cls, value, params=None):
        obj = super(PathPart, cls).__new__(cls, value)
        obj.params = params
        return obj

    def __repr__(self):
        return '%s(%r, params=%r)' % (self.__class__.__name__, str(self), self.params)


def extract_rfc2396_params(path):
    """This function implements parsing URL path parameters, per `section 3.3 of RFC2396`_.

    * path should be raw so we don't split or operate on a decoded character
    * output is decoded

    Example:

    >>> path = '/frisbee;color=red;size=small/logo;sponsor=w3c;color=black/image.jpg'
    >>> extract_rfc2396_params(path) == [
    ...     PathPart('frisbee', params={'color': ['red'], 'size': ['small']}),
    ...     PathPart('logo', params={'sponsor': ['w3c'], 'color': ['black']}),
    ...     PathPart('image.jpg', params={})
    ... ]
    True

    .. _Section 3.3 of RFC2396: https://tools.ietf.org/html/rfc3986#section-3.3
    """
    pathsegs = path.lstrip('/').split('/')
    segments_with_params = []
    for component in pathsegs:
        parts = component.split(';')
        params = Mapping()
        segment = path_decode(parts[0])
        for p in parts[1:]:
            if '=' in p:
                k, v = p.split('=', 1)
            else:
                k, v = p, ''
            params.add(path_decode(k), path_decode(v))
        segments_with_params.append(PathPart(segment, params))
    return segments_with_params


def split_path_no_params(path):
    """This splits a path into parts on "/" only (no split on ";" or ",").
    """
    return [PathPart(path_decode(s)) for s in path.lstrip('/').split('/')]


class Path(Mapping):
    """Represent the path of a resource.

    Attributes:
        raw: the unparsed form of the path - :class:`bytes`
        decoded: the decoded form of the path - :class:`str`
        parts: the segments of the path - :class:`list` of :class:`PathPart` objects
    """

    def __init__(self, raw, split_path=extract_rfc2396_params):
        self.raw = raw
        self.decoded = path_decode(raw)
        self.parts = split_path(raw)


class Querystring(Mapping):
    """Represent an HTTP querystring.

    Attributes:
        raw: the unparsed form of the querystring - :class:`bytes`
        decoded: the decoded form of the querystring - :class:`str`
    """

    def __init__(self, raw, errors='replace'):
        """Takes a string of type application/x-www-form-urlencoded.
        """
        # urllib needs bytestrings in py2 and unicode strings in py3
        raw_str = raw.encode('ascii') if PY2 else raw

        self.decoded = _decode(unquote_plus(raw_str), errors=errors)
        self.raw = raw

        common_kw = dict(keep_blank_values=True, strict_parsing=False)
        if PY2:
            # in python 2 parse_qs does its own unquote_plus'ing ...
            as_dict = parse_qs(raw_str, **common_kw)
            # ... but doesn't decode to unicode.
            for k, vals in list(as_dict.items()):
                as_dict[_decode(k, errors=errors)] = [
                    _decode(v, errors=errors) for v in vals
                ]
        else:
            # in python 3 parse_qs does the decoding
            as_dict = parse_qs(raw_str, errors=errors, **common_kw)

        Mapping.__init__(self, as_dict)
