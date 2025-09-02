"""
urllib2 HTTP caching support
inspired by http://code.activestate.com/recipes/491261/
"""

import email.utils
import pickle
import datetime
import logging
import io
from urllib import request

log = logging.getLogger(__name__)


class CacheHandler(request.BaseHandler):
    """
    Stores responses in a httplib2-style cache object.
    """

    def __init__(self, store):
        "construct a handler from a store"
        self.store = store

    def default_open(self, request):
        """
        Open the url specified in the request. If it's an HTTP GET, and
        the result is a valid cached value, return the cached version.
        """
        key = self._defrag_uri(request.get_full_url())
        if request.get_method() not in ('GET', 'HEAD'):
            # invalate this item if cached (RFC 2616 Section 13.10)
            self.store.delete(key)
        if request.get_method() != 'GET':
            # defer to other handlers
            return None

        self._convert_pragma(request.headers)

        # check the request cache-control header
        cc = self._parse_cache_control(request.headers)

        # check that the user-agent hasn't asked us to bypass the cache
        if 'no-cache' in cc:
            return None

        # get the cached response, or None if it's not found
        cached_resp = CachedResponse.load(self.store.get(key))
        if not cached_resp and 'only-if-cached' in cc:
            raise request.HTTPError(
                request.get_full_url(), 504, 'content is not cached', hdrs=None, fp=None
            )

        if cached_resp and not cached_resp.fresh_for(request.headers):
            log.debug('request is stale')
            self._add_stale_cache_request_headers(request, cached_resp)
            cached_resp = None

        return cached_resp

    @staticmethod
    def _add_stale_cache_request_headers(request, cached_resp):
        """
        The cached response is stale, so we need to re-validate it with
        the server. Add the `if-modified-since` and `if-none-match`
        headers to the request as appropriate.
        """

        if (
            'last-modified' in cached_resp.headers
            and 'if-modified-since' not in request.headers
        ):
            lm = cached_resp.headers['last-modified']
            request.headers['if-modified-since'] = lm

        if (
            'etag' in cached_resp.headers
            # and not self.ignore_etag
            and 'if-none-match' not in request.headers
        ):
            et = cached_resp.headers['etag']
            request.headers['if-none-match'] = et

    def http_response(self, request, response):
        """
        Handle a HTTP response.
        """
        return self._update_cache(request, response)

    @staticmethod
    def _convert_pragma(headers):
        """
        convert "pragma: no-cache" to "cache-control: no-cache" in the
        request.
        """
        if (
            'pragma' in headers
            and 'no-cache' in headers['pragma'].lower()
            and 'cache-control' not in headers
        ):
            headers['cache-control'] = 'no-cache'

    def _update_cache(self, request, response):
        """
        If it was a normal response (200 level) to
        a GET request, store it in the cache.
        """
        is_get = request.get_method() == 'GET'
        key = self._defrag_uri(request.get_full_url())
        if is_get and response.code == 304:
            # 304 - Not Modified, update the cached version
            log.debug('304 received - updating headers')
            new_headers = response.headers
            response = CachedResponse.load(self.store.get(key))
            response.update_headers(new_headers)
            self.store.set(key, response.save())
            return response
        cached_response_codes = [200, 203]
        cacheable_response = response.code in cached_response_codes
        if not is_get or not cacheable_response:
            return response

        if self.should_cache(response):
            response = CachedResponse.from_response(response)
            self.store.set(key, response.save())
        return response

    def should_cache(self, response):
        if 'vary' in response.headers:
            # for now, don't store requests that vary based on headers
            return False
        already_cached = getattr(response, 'cached', False)
        if already_cached:
            return False
        if 'range' in response.headers:
            # we don't support caching ranged requests
            return False
        return True

    @staticmethod
    def _defrag_uri(uri):
        main, sep, frag = uri.partition('#')
        return main

    @staticmethod
    def _parse_cache_control(headers):
        """
        Parse the cache-control header.

        >>> pcc = CacheHandler._parse_cache_control
        >>> sample = {'cache-control':'max-age=3, bar=baz, Foo'}
        >>> sorted(pcc(sample).items())
        [('bar', 'baz'), ('foo', None), ('max-age', '3')]

        >>> pcc({})
        {}
        """

        def parse_part(part):
            """
            Given a cache-control header spec, parse out its name and
            possible value.
            >>> parse_part('max-size=3')
            ('max-size', '3')
            >>> parse_part('No-Cache')
            ('no-cache', None)
            """
            name, sep, val = map(str.lower, map(str.strip, part.partition('=')))
            return name, (val or None)

        cc_header = headers.get('cache-control', '')
        return dict(parse_part(part) for part in cc_header.split(',') if part)


class CachedResponse(io.BytesIO):
    """
    A response object compatible with urllib.request.response objects but for
    cached responses.
    """

    cached = True

    @classmethod
    def from_response(cls, response):
        cr = cls(response.read())
        cr.seek(0)
        cr.headers = response.info()
        cr.url = response.url
        cr.code = response.code
        cr.msg = response.msg
        return cr

    def save(self):
        "Produce a serialized version of this response"
        self.headers['x-urllib-cache'] = 'Stored'
        return pickle.dumps(vars(self))

    @classmethod
    def load(cls, payload):
        "Construct a CachedResponse from a serialized payload"
        if payload is None:
            return None
        result = cls()
        result.__dict__.update(pickle.loads(payload))
        result.headers['x-urllib-cache'] = 'Cached'
        return result

    def info(self):
        return self.headers

    def geturl(self):
        return self.url

    def reload(self, store):
        """
        Force a reload of this response
        """
        opener = request.build_opener()
        cr = self.from_response(opener.open(self.url))
        self.__dict__.update(vars(cr))
        store.set(self.url, self.save())

    @property
    def age(self):
        "Return the age of this response, guaranteed >= 0"
        date = datetime_from_email(self.headers['date'])
        now = datetime.datetime.now(datetime.timezone.utc)
        zero = datetime.timedelta()
        return max(zero, now - date)

    def fresh(self):
        """
        Check the max-age and expires headers on this response. Return
        True if this response has not expired.
        """
        cc = CacheHandler._parse_cache_control(self.headers)
        if 'no-cache' in cc:
            return False
        if self.exceeds_max_age(cc):
            return False
        if 'expires' in cc:
            try:
                expires = datetime_from_email(self.headers['expires'])
                now = datetime.datetime.now(datetime.timezone.utc)
                if expires < now:
                    return False
            except ValueError:
                pass
        return True

    def fresh_for(self, req_headers):
        """
        Check if this response is fresh in its own right and with
        respect to the request headers.
        """
        cc = CacheHandler._parse_cache_control(req_headers)
        return self.fresh() and not self.exceeds_max_age(cc)

    def exceeds_max_age(self, cache_control):
        if 'max-age' not in cache_control:
            # If max-age is not indicated, it can't be exceeded
            return False
        if 'date' not in self.headers:
            return True
        # user-agent might have a 'min-fresh' directive indicating the
        #  client will only accept a cached request if it will still be
        #  fresh min-fresh seconds from now.
        try:
            min_fresh = datetime.timedelta(seconds=int(cache_control['min-fresh']))
        except (KeyError, ValueError):
            min_fresh = datetime.timedelta()
        try:
            max_age = datetime.timedelta(seconds=int(cache_control['max-age']))
            if self.age + min_fresh > max_age:
                return True
        except ValueError:
            pass
        return False

    def update_headers(self, new_headers):
        for header in get_endpoint_headers(new_headers):
            self.headers[header] = new_headers[header]


def get_endpoint_headers(headers):
    """
    Given a dictionary-like headers object, return the names of all
    headers in that set which represent end-to-end (and not intermediate
    or connection headers).
    """
    intermediate_headers = [
        'connection',
        'keep-alive',
        'proxy-authenticate',
        'proxy-authorization',
        'te',
        'trailers',
        'transfer-encoding',
        'upgrade',
    ]
    intermediate_headers.extend(
        header.strip() for header in headers.get('connection', '')
    )
    return set(headers.keys()) - set(intermediate_headers)


def _make_aware(dt):
    """
    email.utils will create naive datetimes for -0000; make them aware.
    """
    return dt.replace(tzinfo=dt.tzinfo or datetime.timezone.utc)


def datetime_from_email(str):
    return _make_aware(email.utils.parsedate_to_datetime(str))


def quick_test():
    """Quick test/example of CacheHandler"""
    from httplib2 import FileCache

    logging.basicConfig(level=logging.DEBUG)
    store = FileCache(".cache")
    opener = request.build_opener(CacheHandler(store))
    request.install_opener(opener)
    response = request.urlopen("http://www.google.com/")
    print(response.headers)
    print("Response:", response.read()[:100], '...\n')

    response.reload(store)
    print(response.headers)
    print("After reload:", response.read()[:100], '...\n')


if __name__ == "__main__":
    quick_test()
