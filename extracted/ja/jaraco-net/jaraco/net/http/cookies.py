import pathlib
import collections
import http.cookiejar
import contextlib

import jsonpickle


class Shelf(collections.abc.MutableMapping):
    """
    Similar to Python's shelve.Shelf, implements a persistent
    dictionary using jsonpickle.

    >>> fn = getfixture('tmp_path') / 'shelf.json'
    >>> shelf = Shelf(fn)
    >>> shelf['foo'] = 'bar'
    >>> copy = Shelf(fn)
    >>> copy['foo']
    'bar'
    >>> shelf['bar'] = 'baz'
    >>> Shelf(fn)['bar']
    'baz'
    """

    def __init__(self, filename):
        self.filename = pathlib.Path(filename)
        self.store = dict()
        # ensure stricter, non-YAML backend is selected (jsonpickle/jsonpickle#550)
        self.backend = jsonpickle.backend.JSONBackend(fallthrough=False)
        with contextlib.suppress(Exception):
            self._load()

    def _load(self):
        self.store = jsonpickle.decode(
            self.filename.read_text(encoding='utf-8'), backend=self.backend
        )

    def _save(self):
        self.filename.write_text(
            jsonpickle.encode(self.store, backend=self.backend), encoding='utf-8'
        )

    def __getitem__(self, *args, **kwargs):
        return self.store.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        self.store.__setitem__(*args, **kwargs)
        self._save()

    def __delitem__(self, *args, **kwargs):
        self.store.__delitem__(*args, **kwargs)
        self._save()

    def __iter__(self):
        return self.store.__iter__()

    def __len__(self):
        return self.store.__len__()


class ShelvedCookieJar(http.cookiejar.CookieJar):
    """
    Cookie jar backed by a shelf.

    Automatically persists cookies to disk.
    """

    def __init__(self, shelf: Shelf, **kwargs):
        super().__init__(**kwargs)
        self._cookies = self.shelf = shelf

    @classmethod
    def create(cls, root: pathlib.Path = pathlib.Path(), name='cookies.json', **kwargs):
        return cls(Shelf(root / name), **kwargs)

    def set_cookie(self, cookie):
        with self._cookies_lock:
            self.shelf.setdefault(cookie.domain, {}).setdefault(cookie.path, {})[
                cookie.name
            ] = cookie
            self.shelf._save()

    def clear(self, domain=None, path=None, name=None):
        super().clear(domain, path, name)
        if path is not None or name is not None:
            self.shelf._save()

    def get(self, name, default=None):
        matches = (
            cookie.value
            for domain in self.shelf
            for path in self.shelf[domain]
            for cookie in self.shelf[domain][path].values()
            if cookie.name == name
        )
        return next(matches, default)
