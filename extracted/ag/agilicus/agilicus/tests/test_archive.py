"""Tests for the organisation archive command (agilicus.archive)."""

import json

import pytest

from agilicus.archive import archive as archive_module


class FakeResponse:
    """Minimal stand-in for a generated list response model."""

    def __init__(self, **fields):
        self._fields = fields
        self.attribute_map = {key: key for key in fields}

    def get(self, key, default=None):
        return self._fields.get(key, default)


class FakeEndpoint:
    """Minimal stand-in for a generated API endpoint."""

    def __init__(self, func, params=("org_id",)):
        self._func = func
        self.params_map = {"all": list(params)}

    def __call__(self, **kwargs):
        return self._func(**kwargs)


class FakeApi:
    def __init__(self, **methods):
        for name, endpoint in methods.items():
            setattr(self, name, endpoint)


class FakeClient:
    pass


def _endpoint(func, params=("org_id",)):
    return FakeEndpoint(func, params=params)


def _build_client(orgs=None, suborgs=None):
    orgs = orgs or {}
    suborgs = suborgs or {}
    calls = []

    def get_org(org_id):
        calls.append(("get_org", org_id))
        return orgs[org_id]

    def list_sub_orgs(org_id, limit=None):
        calls.append(("list_sub_orgs", org_id))
        return FakeResponse(orgs=[{"id": i} for i in suborgs.get(org_id, [])])

    def list_users(org_id, limit=None):
        calls.append(("list_users", org_id))
        return FakeResponse(users=[{"id": "{}-user-1".format(org_id), "org_id": org_id}])

    def list_applications(org_id, limit=None):
        return FakeResponse(
            applications=[{"id": "{}-app-1".format(org_id), "org_id": org_id}]
        )

    def list_roles(app_id, org_id=None, limit=None):
        return FakeResponse(roles=[{"id": "{}-role".format(app_id)}])

    def list_rules(app_id, org_id=None, limit=None):
        return FakeResponse(rules=[{"id": "{}-rule".format(app_id)}])

    def list_totp(user_id, limit=None):
        return FakeResponse(totp=[{"metadata": {"id": "{}-totp".format(user_id)}}])

    def list_webauthn(user_id, limit=None):
        return FakeResponse(webauthn=[])

    def empty(org_id=None, **kwargs):
        return FakeResponse()

    client = FakeClient()
    client.org_api = FakeApi(
        get_org=_endpoint(get_org, params=("org_id",)),
        list_sub_orgs=_endpoint(list_sub_orgs, params=("org_id", "limit")),
        list_email_domains=_endpoint(lambda org_id: FakeResponse(domains=[])),
        get_system_options=_endpoint(lambda org_id: {"org_id": org_id, "kind": "sys"}),
        get_org_features=_endpoint(lambda org_id: {"features": []}),
        get_org_status=_endpoint(lambda org_id: {"status": "ok"}),
        get_inherent_capabilities=_endpoint(lambda org_id: {"capabilities": []}),
    )
    client.user_api = FakeApi(
        list_users=_endpoint(list_users, params=("org_id", "limit")),
    )
    client.application_api = FakeApi(
        list_applications=_endpoint(list_applications, params=("org_id", "limit")),
        list_roles=_endpoint(list_roles, params=("app_id", "org_id", "limit")),
        list_rules=_endpoint(list_rules, params=("app_id", "org_id", "limit")),
    )
    client.challenges_api = FakeApi(
        list_totp_enrollment=_endpoint(list_totp, params=("user_id", "limit")),
        list_webauthn_enrollments=_endpoint(list_webauthn, params=("user_id", "limit")),
    )
    return client, calls


def _patch(monkeypatch, client):
    monkeypatch.setattr(
        archive_module.context, "get_apiclient", lambda ctx, *a, **k: client
    )
    monkeypatch.setattr(archive_module, "output_if_console", lambda *a, **k: None)


def test_archive_writes_objects_named_by_guid(tmp_path, monkeypatch):
    client, _ = _build_client(orgs={"root": {"id": "root", "organisation": "Root"}})
    _patch(monkeypatch, client)

    result = archive_module.archive_org(
        object(), org_id="root", directory=str(tmp_path), recursive=False
    )

    assert (tmp_path / "org-root" / "organisations" / "root.json").exists()
    assert (tmp_path / "org-root" / "users" / "root-user-1.json").exists()
    assert (tmp_path / "org-root" / "applications" / "root-app-1.json").exists()
    assert (
        tmp_path / "org-root" / "application-roles" / "root-app-1-role.json"
    ).exists()
    assert (
        tmp_path / "org-root" / "totp-enrollments" / "root-user-1-totp.json"
    ).exists()
    assert (tmp_path / "org-root" / "system-options" / "root.json").exists()

    data = json.loads((tmp_path / "org-root" / "users" / "root-user-1.json").read_text())
    assert data["org_id"] == "root"

    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert manifest["counts"]["users"] == 1
    assert manifest["counts"]["applications"] == 1
    assert "firewall-rules" not in result.counts
    # The manifest carries per-organisation counts and directory.
    (org_entry,) = [
        entry for entry in manifest["organisations"] if entry["id"] == "root"
    ]
    assert org_entry["directory"] == "org-root"
    assert org_entry["counts"]["users"] == 1


def test_archive_recurses_into_sub_orgs(tmp_path, monkeypatch):
    client, _ = _build_client(
        orgs={
            "root": {"id": "root", "organisation": "Root"},
            "child": {"id": "child", "organisation": "Child"},
        },
        suborgs={"root": ["child"], "child": []},
    )
    _patch(monkeypatch, client)

    result = archive_module.archive_org(
        object(), org_id="root", directory=str(tmp_path), recursive=True
    )

    assert (tmp_path / "org-child" / "users" / "child-user-1.json").exists()
    assert {org["id"] for org in result.organisations} == {"root", "child"}
    assert result.counts["organisations"] == 2
    assert set(result.visited) == {"root", "child"}


def test_archive_records_errors_and_continues(tmp_path, monkeypatch):
    client, _ = _build_client(orgs={"root": {"id": "root", "organisation": "Root"}})
    _patch(monkeypatch, client)

    def boom(org_id, limit=None):
        raise RuntimeError("nope")

    client.user_api.list_users = FakeEndpoint(boom, params=("org_id", "limit"))

    result = archive_module.archive_org(
        object(), org_id="root", directory=str(tmp_path), recursive=False
    )

    assert any(error["type"] == "users" for error in result.errors)
    # Other types still archived.
    assert (tmp_path / "org-root" / "applications" / "root-app-1.json").exists()


def test_object_filename_sanitizes_and_hashes():
    assert archive_module.object_filename({"id": "abc-123"}) == "abc-123"
    assert archive_module.object_filename({"id": "a/b c"}) == "a_b_c"
    hashed = archive_module.object_filename({"unidentifiable": True})
    assert hashed.startswith("sha1-")


def test_first_list_picks_list_field():
    assert archive_module._first_list(FakeResponse(users=[1, 2], limit=3)) == [1, 2]
    assert archive_module._first_list({"things": [1]}) == [1]
    assert archive_module._first_list([1, 2, 3]) == [1, 2, 3]
    assert archive_module._first_list(None) == []


def test_list_all_paginates_page_at_id():
    pages = {None: (["a", "b"], "b"), "b": (["c"], None)}

    def method(org_id=None, limit=None, page_at_id=None):
        items, next_page = pages[page_at_id]
        return FakeResponse(things=items, page_at_id=next_page)

    method.params_map = {"all": ["org_id", "limit", "page_at_id"]}

    assert archive_module.list_all(method, org_id="o") == ["a", "b", "c"]


def test_list_all_paginates_previous_email():
    pages = {None: (["a"], "b"), "b": (["c"], None)}

    def method(org_id=None, limit=None, previous_email=None):
        items, next_page = pages[previous_email]
        return FakeResponse(groups=items, next_page_email=next_page)

    method.params_map = {"all": ["org_id", "limit", "previous_email"]}

    assert archive_module.list_all(method, org_id="o") == ["a", "c"]


class UnhashableToken:
    """Mimics generated primitive models (NextPageEmail): __eq__, no __hash__."""

    __hash__ = None

    def __init__(self, value):
        self.value = value

    def to_str(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, UnhashableToken) and self.value == other.value


def test_list_all_paginates_with_unhashable_token():
    pages = {None: (["a"], "b"), "b": (["c"], None)}
    received = []

    def method(org_id=None, limit=None, previous_email=None):
        received.append(previous_email)
        if previous_email is None:
            key = None
        elif isinstance(previous_email, str):
            key = previous_email
        else:
            key = previous_email.value
        items, next_page = pages[key]
        token = None if next_page is None else UnhashableToken(next_page)
        return FakeResponse(groups=items, next_page_email=token)

    method.params_map = {"all": ["org_id", "limit", "previous_email"]}

    assert archive_module.list_all(method, org_id="o") == ["a", "c"]
    # The unhashable model token must not be passed back to the endpoint; the
    # primitive value is, because previous_email is typed as a different class.
    assert received[0] is None
    assert received[1] == "b"
    assert isinstance(received[1], str)


def test_page_token_is_hashable_for_models():
    assert archive_module._page_token(UnhashableToken("abc")) == "abc"
    assert archive_module._page_token(None) is None
    assert archive_module._page_token("") == ""
    assert archive_module._page_token(5) == "5"
    assert archive_module._page_value(UnhashableToken("abc")) == "abc"
    assert archive_module._page_value(5) == 5


class RawResponse:
    def __init__(self, data):
        self.data = data


def test_list_all_falls_back_to_raw_when_model_cannot_parse():
    calls = []

    def method(org_id=None, limit=None, _preload_content=True, **kwargs):
        calls.append(_preload_content)
        if _preload_content:
            raise TypeError(
                "ListRoles._from_openapi_data() missing 1 required "
                "positional argument: 'limit'"
            )
        return RawResponse(b'{"limit": 500, "roles": [{"id": "r1"}, {"id": "r2"}]}')

    method.params_map = {"all": ["org_id", "limit"]}

    assert archive_module.list_all(method, org_id="o") == [{"id": "r1"}, {"id": "r2"}]
    assert calls == [True, False]


def test_list_all_does_not_swallow_unrelated_type_errors():
    def method(org_id=None, limit=None, **kwargs):
        raise TypeError("something else entirely")

    method.params_map = {"all": ["org_id", "limit"]}

    with pytest.raises(TypeError, match="something else"):
        archive_module.list_all(method, org_id="o")


def test_decode_raw():
    assert archive_module._decode_raw(RawResponse(b'{"a": 1}')) == {"a": 1}
    assert archive_module._decode_raw(RawResponse("")) == {}
    assert archive_module._decode_raw(RawResponse(b"not json")) == {}


class Forbidden(Exception):
    status = 403
    reason = "Forbidden"


def test_describe_error_is_concise():
    verbose = Forbidden(
        "Forbidden\nReason: Forbidden\nHTTP response headers: HTTPHeaderDict(...)\n"
        "HTTP response body: {'roleMatched': false}"
    )
    assert archive_module._describe_error(verbose) == "Forbidden: 403 Forbidden"


def test_record_error_captures_status():
    result = archive_module.ArchiveResult(directory="/tmp/x", org_id="o")
    archive_module._record_error(result, "users", "o", Forbidden("nope"))
    (error,) = result.errors
    assert error["type"] == "users"
    assert error["status"] == 403
    assert error["error"] == "Forbidden: 403 Forbidden"


def test_print_errors_groups_and_truncates(capsys):
    from agilicus.archive import archive_main

    class Ctx:
        obj = {"output_format": "console"}

    result = archive_module.ArchiveResult(directory="/tmp/x", org_id="o")
    for index in range(10):
        archive_module._record_error(
            result, "type{}".format(index), "orgA", Forbidden("nope")
        )
    archive_main._print_errors(Ctx(), result)
    out = capsys.readouterr().out
    assert "orgA: 10 type(s) could not be read" in out
    assert "and 2 more" in out


def test_archive_include_child_collects_parent(tmp_path, monkeypatch):
    client, _ = _build_client(orgs={"root": {"id": "root", "organisation": "Root"}})
    _patch(monkeypatch, client)

    archive_module.archive_org(
        object(),
        org_id="root",
        directory=str(tmp_path),
        recursive=False,
        include_types=("totp-enrollments",),
    )

    # The parent ``users`` collection is fetched so the fan-out can run, but
    # only the requested child type needs to be written.
    assert (
        tmp_path / "org-root" / "totp-enrollments" / "root-user-1-totp.json"
    ).exists()


def test_cli_archive_org_invokes_archive(tmp_path, monkeypatch):
    from click.testing import CliRunner

    from agilicus.archive import archive_main

    captured = {}

    class FakeResult:
        directory = str(tmp_path)
        counts = {"users": 1}
        organisations = [{"id": "root"}]
        visited = ["root"]
        errors = []

        def to_dict(self):
            return {"org_id": "root"}

    def fake_archive(ctx, org_id, directory, **kwargs):
        captured["org_id"] = org_id
        captured["directory"] = directory
        captured["kwargs"] = kwargs
        return FakeResult()

    monkeypatch.setattr(archive_main.archive, "archive_org", fake_archive)
    runner = CliRunner()
    result = runner.invoke(
        archive_main.cli_command_archive_org,
        ["root", "-d", str(tmp_path)],
        obj={"output_format": "console"},
    )
    assert result.exit_code == 0, result.output
    assert captured["org_id"] == "root"
    assert captured["directory"] == str(tmp_path)
    assert "users" in result.output
