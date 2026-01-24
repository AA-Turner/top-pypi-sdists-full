import asyncio
import pytest
from apimatic_core_interfaces.http.request import Request

from apimatic_core.adapters.request_adapter import (
    to_unified_request_async,            # async core
    to_unified_request,       # sync wrapper
    _as_listdict,                  # helper (public in module)
)


# -----------------------
# Shared duck-typed helpers
# -----------------------

class MultiDictStub:
    def __init__(self, mapping):
        self._m = {k: (list(v) if isinstance(v, (list, tuple)) else [v])
                   for k, v in mapping.items()}
    def getlist(self, key):
        return list(self._m.get(key, []))
    def keys(self):
        return list(self._m.keys())


class MappingStub:
    """Plain mapping (no getlist) with .keys and __getitem__."""
    def __init__(self, mapping):
        self._m = dict(mapping)
    def keys(self):
        return list(self._m.keys())
    def __getitem__(self, k):
        return self._m[k]


class MappingWithNonCallableGetlist(MappingStub):
    """Has a non-callable attribute named 'getlist' to exercise callable(getlist) == False."""
    getlist = 42  # not callable


# -------- Starlette/FastAPI-like duck types --------

class URLStub:
    def __init__(self, url: str, path: str):
        self._url = url
        self.path = path
    def __str__(self):
        return self._url


class UploadFileLike:
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self._data = data
    async def read(self):
        return self._data
    read = read


class FormDataStarletteLike:
    def __init__(self, mapping):
        self._m = {k: list(v) for k, v in mapping.items()}
    def keys(self):
        return list(self._m.keys())
    def getlist(self, key):
        return list(self._m.get(key, []))


class StarletteRequestLikeStub:
    def __init__(
        self,
        *,
        method="POST",
        url="https://ex.com/submit?a=1&a=2",
        path="/submit",
        headers=None,
        body=b"",
        query_params=None,
        cookies=None,
        formdata=None,
    ):
        self.method = method
        self.url = URLStub(url, path)
        self.headers = headers or {}
        self._body = body
        self.query_params = query_params or {}
        self.cookies = cookies or {}
        self._formdata = formdata
    async def body(self):
        return bytes(self._body)
    async def form(self):
        return self._formdata


# -------- Flask/Werkzeug-like duck types --------

class FlaskRequestLikeStub:
    def __init__(
        self,
        *,
        method="POST",
        path="/p",
        url="http://localhost/p?q=x&q=y",
        headers=None,
        data=b"payload",
        args=None,
        cookies=None,
        form=None,
    ):
        self.method = method
        self.path = path
        self.url = url
        self.headers = headers or {}
        self._data = data
        self.args = args or {}
        self.cookies = cookies or {}
        self.form = form or {}
    def get_data(self, cache=True):
        return bytes(self._data)


# -------- Django-like duck types --------

class DjangoRequestLikeStub:
    def __init__(
        self,
        *,
        method="POST",
        path="/post",
        headers=None,
        meta=None,
        body=b"",
        GET=None,
        COOKIES=None,
        POST=None,
        absolute="http://testserver/post?page=1&page=2",
    ):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.META = meta or {}
        self.body = body
        self.GET = GET or {}
        self.COOKIES = COOKIES or {}
        self.POST = POST or {}
        self._abs = absolute
    def build_absolute_uri(self):
        return self._abs


# -------- LocalProxy-like un-wrapper duck type --------

class LocalProxyLike:
    def __init__(self, target):
        self._target = target
    def _get_current_object(self):
        return self._target


class LocalProxyRaising(DjangoRequestLikeStub):
    """
    Duck-typed LocalProxy that *has* _get_current_object but it raises.
    We subclass DjangoRequestLikeStub so that even if unwrapping fails,
    the returned object still structurally satisfies the Django Protocol,
    letting the adapter proceed and exercising the 'except' branch.
    """
    def _get_current_object(self):
        raise RuntimeError("boom")


# =======================
# Pytest class wrapper
# =======================

class TestRequestAdapter:

    # ------- Starlette / FastAPI branch -------

    def test_starlette_non_form_skips_form_and_snapshots_body(self):
        req = StarletteRequestLikeStub(
            method="GET",
            url="https://ex.com/fast-json/42?q=ok",
            path="/fast-json/42",
            headers={"Accept": "application/json"},
            body=b'{"msg":"hello"}',
            query_params=MultiDictStub({"q": ["ok"]}),
            cookies={"sid": "abc"},
            formdata=FormDataStarletteLike({"ignored": ["x"]}),
        )
        snap: Request = asyncio.run(to_unified_request_async(req))
        assert snap.method == "GET"
        assert snap.path == "/fast-json/42"
        assert snap.url == "https://ex.com/fast-json/42?q=ok"
        assert snap.query == {"q": ["ok"]}
        assert snap.cookies == {"sid": "abc"}
        assert snap.form == {}  # no Content-Type => skip form parsing
        assert snap.raw_body == b'{"msg":"hello"}'

    def test_starlette_form_multipart_parses_text_and_ignores_files(self):
        form = FormDataStarletteLike({
            "user": ["alice", "bob"],
            "upload": [UploadFileLike("a.bin", b"AAAA")],  # should be ignored
        })
        req = StarletteRequestLikeStub(
            method="POST",
            url="https://ex.com/fast-mp/9?z=ok",
            path="/fast-mp/9",
            headers={"Content-Type": "multipart/form-data; boundary=xyz"},
            body=b"--xyz...",
            query_params=MultiDictStub({"z": ["ok"]}),
            cookies={"c": "1"},
            formdata=form,
        )
        snap: Request = asyncio.run(to_unified_request_async(req))
        assert snap.method == "POST"
        assert snap.path == "/fast-mp/9"
        assert snap.query == {"z": ["ok"]}
        assert snap.cookies == {"c": "1"}
        assert snap.form == {"user": ["alice", "bob"]}
        assert "upload" not in snap.form

    def test_starlette_form_urlencoded_parses_scalars_and_lists(self):
        form = FormDataStarletteLike({
            "name": ["Sufyan"],
            "roles": ["admin", "editor"],
        })
        req = StarletteRequestLikeStub(
            method="POST",
            url="https://ex.com/fast-form/1?x=1",
            path="/fast-form/1",
            headers={"content-type": "application/x-www-form-urlencoded"},
            body=b"a=1",
            query_params=MultiDictStub({"x": ["1"]}),
            cookies={"c": "2"},
            formdata=form,
        )
        snap: Request = asyncio.run(to_unified_request_async(req))
        assert snap.method == "POST"
        assert snap.path == "/fast-form/1"
        assert snap.query == {"x": ["1"]}
        assert snap.cookies == {"c": "2"}
        assert snap.form == {"name": ["Sufyan"], "roles": ["admin", "editor"]}

    # ------- Flask branch -------

    def test_flask_basic_and_cookie_header_fallback(self):
        headers = {"X-Test": "1", "Cookie": "sid=abc; theme=light"}
        args = MultiDictStub({"q": ["x", "y"]})
        form = MultiDictStub({"name": "Sufyan"})
        req = FlaskRequestLikeStub(
            method="POST",
            path="/flask-form/5",
            url="http://localhost/flask-form/5?q=x&q=y",
            headers=headers,
            data=b"a=1&b=2",
            args=args,
            cookies={},  # force header fallback
            form=form,
        )
        snap: Request = to_unified_request(req)
        assert snap.method == "POST"
        assert snap.path == "/flask-form/5"
        assert snap.url.endswith("/flask-form/5?q=x&q=y")
        assert snap.headers.get("X-Test") == "1"
        assert snap.query == {"q": ["x", "y"]}
        assert snap.cookies["sid"] == "abc" and snap.cookies["theme"] == "light"
        assert snap.form == {"name": ["Sufyan"]}
        assert snap.raw_body == b"a=1&b=2"

    def test_flask_uses_cookie_jar_when_present_no_header_needed(self):
        headers = {"x": "y", "cookie": "ignored=1"}  # lowercase 'cookie' shouldn't be used
        req = FlaskRequestLikeStub(
            method="GET",
            path="/flask-cookies/1",
            url="http://localhost/flask-cookies/1",
            headers=headers,
            data=b"",
            args=MultiDictStub({}),
            cookies={"sid": "JAR"},
            form=MultiDictStub({}),
        )
        snap: Request = to_unified_request(req)
        assert snap.cookies == {"sid": "JAR"}  # header fallback not used

    # ------- Django branch -------

    def test_django_headers_meta_fallback_and_basic_mapping(self):
        meta = {"HTTP_X_H": "v", "SOME_OTHER": "ignored"}
        req = DjangoRequestLikeStub(
            method="POST",
            path="/django-form/7",
            headers={},  # triggers META fallback
            meta=meta,
            body=b"payload",
            GET=MultiDictStub({"x": ["1", "2"]}),
            COOKIES={"csrftoken": "t"},
            POST=MultiDictStub({"a": "1", "b": "2"}),
            absolute="http://testserver/django-form/7?x=1&x=2",
        )
        snap: Request = to_unified_request(req)
        assert snap.method == "POST"
        assert snap.path == "/django-form/7"
        assert snap.url.startswith("http://testserver/django-form/7?")
        assert snap.headers.get("X-H") == "v"
        assert snap.cookies == {"csrftoken": "t"}
        assert snap.query == {"x": ["1", "2"]}
        assert snap.form == {"a": ["1"], "b": ["2"]}
        assert snap.raw_body == b"payload"

    def test_django_headers_present_no_meta_fallback(self):
        req = DjangoRequestLikeStub(
            method="GET",
            path="/h",
            headers={"X-Direct": "yes"},
            meta={"HTTP_X_META": "nope"},
            body=b"",
            GET=MultiDictStub({"p": "1"}),
            COOKIES={"c": "v"},
            POST=MultiDictStub({}),
            absolute="http://testserver/h?p=1",
        )
        snap: Request = to_unified_request(req)
        assert snap.headers == {"X-Direct": "yes"}  # no META fallback used

    # ------- Sync wrapper LocalProxy unwrapping -------

    def test_sync_wrapper_unwraps_localproxy_duck_type(self):
        inner = DjangoRequestLikeStub(
            method="GET",
            path="/p",
            headers={"X": "1"},
            body=b"",
            GET=MultiDictStub({"q": "ok"}),
            COOKIES={"sid": "abc"},
            POST=MultiDictStub({}),
            absolute="http://testserver/p?q=ok",
        )
        proxy = LocalProxyLike(inner)
        snap: Request = to_unified_request(proxy)
        assert snap.method == "GET"
        assert snap.path == "/p"
        assert snap.query == {"q": ["ok"]}
        assert snap.cookies == {"sid": "abc"}

    def test_sync_wrapper_unwrap_localproxy_raises_and_uses_original_object(self):
        # This object has a raising _get_current_object(), so _unwrap_local_proxy
        # should hit the except path and return the object itself. Because the object
        # also satisfies the Django-like Protocol, the adapter can still convert it.
        proxy = LocalProxyRaising(
            method="GET",
            path="/ex",
            headers={"X": "1"},
            body=b"",
            GET=MultiDictStub({"q": "ok"}),
            COOKIES={"sid": "abc"},
            POST=MultiDictStub({}),
            absolute="http://testserver/ex?q=ok",
        )
        snap = to_unified_request(proxy)
        assert snap.method == "GET"
        assert snap.path == "/ex"
        assert snap.query == {"q": ["ok"]}
        assert snap.cookies == {"sid": "abc"}

    def test_sync_wrapper_plain_object_pass_through(self):
        # Ensures _unwrap_local_proxy returns obj when there's no _get_current_object
        req = DjangoRequestLikeStub(
            method="GET",
            path="/plain",
            headers={"A": "B"},
            body=b"",
            GET=MultiDictStub({}),
            COOKIES={},
            POST=MultiDictStub({}),
            absolute="http://testserver/plain",
        )
        snap = to_unified_request(req)
        assert snap.path == "/plain"
        assert snap.headers == {"A": "B"}

    # ------- Error branch -------

    def test_async_adapter_rejects_unsupported_type(self):
        class Unknown:
            pass
        with pytest.raises(TypeError):
            asyncio.run(to_unified_request_async(Unknown()))

    # ------- _as_listdict coverage -------

    def test_empty_object_returns_empty_dict(self):
        # Path 1: 'if not obj' → True
        assert _as_listdict({}) == {}
        assert _as_listdict(None) == {}

    def test_multidict_path_uses_getlist_and_copies_lists(self):
        # Path 2: callable(getlist) → True
        md = MultiDictStub({"a": ["1", "2"], "b": "x"})
        out = _as_listdict(md)
        assert out == {"a": ["1", "2"], "b": ["x"]}
        # ensure we returned *copies*, not the same underlying lists
        assert out["a"] is not md.getlist("a")

    def test_plain_mapping_path_wraps_scalar_values_in_lists(self):
        # Path 3: callable(getlist) → False (no getlist attr)
        mp = MappingStub({"a": "1", "b": "x"})
        out = _as_listdict(mp)
        assert out == {"a": ["1"], "b": ["x"]}

    def test_plain_mapping_even_with_noncallable_getlist(self):
        # Still Path 3: callable(getlist) → False (attr exists but not callable)
        mp = MappingWithNonCallableGetlist({"k": "v"})
        out = _as_listdict(mp)
        assert out == {"k": ["v"]}
