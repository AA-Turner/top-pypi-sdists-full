"""Tests for the audit forwarders management surface.

The httpx.MockTransport pattern is reused here — none of these tests
touch the network. Coverage target is 100% on every line in
``smplkit.management.audit``.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from smplkit import Error, NotFoundError
from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient
from smplkit.audit import (
    Forwarder,
    ForwarderEnvironment,
    ForwarderType,
    HttpConfiguration,
    HttpHeader,
    HttpMethod,
    TransformType,
)
from smplkit.management.audit import AuditClient


JSONAPI = "application/vnd.api+json"

FWD_ID = "datadog-prod"


def _forwarder_resource(
    *,
    id_: str = FWD_ID,
    name: str = "Datadog production",
    description: str | None = None,
    forwarder_type: str = "datadog",
    filter_: dict[str, Any] | None = None,
    transform: Any = None,
    transform_type: str | None = None,
    environments: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # The base ``enabled`` is server-pinned false (ADR-055); the audit
    # service always returns it false regardless of per-environment state.
    return {
        "id": id_,
        "type": "forwarder",
        "attributes": {
            "name": name,
            "forwarder_type": forwarder_type,
            "enabled": False,
            "environments": environments if environments is not None else {},
            "description": description,
            "filter": filter_,
            "transform": transform,
            "transform_type": transform_type,
            "configuration": {
                "method": "POST",
                "url": "https://siem.example.com/in",
                "headers": [{"name": "DD-API-KEY", "value": "<redacted>"}],
                "success_status": "2xx",
            },
            "created_at": "2026-05-07T12:00:00+00:00",
            "updated_at": "2026-05-07T12:00:00+00:00",
            "deleted_at": None,
            "version": 1,
        },
    }


def _client_with_handler(handler) -> AuditClient:
    auth = _AuditAuthClient(base_url="https://audit.example.com", token="sk_api_test")
    auth.set_httpx_client(
        httpx.Client(
            transport=httpx.MockTransport(handler),
            base_url="https://audit.example.com",
        )
    )
    return AuditClient(auth_client=auth)


# ---------------------------------------------------------------------------
# Models — round-trip and edge cases
# ---------------------------------------------------------------------------


class TestModels:
    def test_http_header_to_dict(self):
        h = HttpHeader(name="X-K", value="v")
        assert h._to_dict() == {"name": "X-K", "value": "v"}

    def test_http_configuration_round_trip(self):
        h = HttpConfiguration(
            method=HttpMethod.PUT,
            url="https://x.example/in",
            headers=[HttpHeader(name="A", value="1")],
            success_status="200",
        )
        d = h._to_dict()
        assert d["method"] == "PUT"
        again = HttpConfiguration._from_dict(d)
        assert again == h
        assert isinstance(again.method, HttpMethod)

    def test_http_configuration_from_dict_defaults(self):
        # Empty dict should produce a sane default HttpConfiguration.
        h = HttpConfiguration._from_dict({})
        assert h.method == HttpMethod.POST
        assert h.headers == []
        assert h.success_status == "2xx"
        # Pre-existing forwarders persisted before the field landed must
        # read back as tls_verify=True so they keep their prior secure default.
        assert h.tls_verify is True
        assert h.ca_cert is None

    def test_http_configuration_round_trips_tls_fields(self):
        h = HttpConfiguration(
            url="https://x",
            tls_verify=False,
            ca_cert="-----BEGIN CERTIFICATE-----\nfoo\n-----END CERTIFICATE-----",
        )
        d = h._to_dict()
        assert d["tls_verify"] is False
        assert "BEGIN CERTIFICATE" in d["ca_cert"]
        again = HttpConfiguration._from_dict(d)
        assert again == h

    def test_http_configuration_accepts_raw_string_method(self):
        # ``HttpMethod`` is a ``str`` subclass, so callers passing the
        # literal still type-check and round-trip cleanly.
        h = HttpConfiguration._from_dict({"method": "PATCH", "url": "https://x"})
        assert h.method == HttpMethod.PATCH

    def test_http_method_enum_members_are_alphabetical(self):
        names = [m.name for m in HttpMethod]
        assert names == sorted(names)

    def test_transform_type_enum_only_jsonata(self):
        # The audit spec pins ``transform_type`` to a single value today;
        # the SDK enum must mirror that so adding new members is a
        # deliberate, type-checkable change.
        assert [m.name for m in TransformType] == ["JSONATA"]
        assert TransformType.JSONATA.value == "JSONATA"
        # ``str`` subclassing keeps interop with raw strings transparent.
        assert TransformType.JSONATA == "JSONATA"

    def test_forwarder_from_resource_returns_transform_type_enum(self):
        f = Forwarder._from_resource(_forwarder_resource(transform="$", transform_type="JSONATA"))
        assert f.transform == "$"
        assert f.transform_type is TransformType.JSONATA

    def test_forwarder_from_resource(self):
        f = Forwarder._from_resource(_forwarder_resource())
        assert f.id == FWD_ID
        assert f.name == "Datadog production"
        assert f.configuration.headers[0].value == "<redacted>"
        assert f.version == 1
        assert f.deleted_at is None
        assert f.description is None
        assert f.transform_type is None
        # Base ``enabled`` is server-pinned false; no environments by default.
        assert f.enabled is False
        assert f.environments == {}
        # No client attached when _from_resource is called bare.
        assert f._client is None

    def test_forwarder_from_resource_reads_environments(self):
        # Per-environment overrides round-trip on read: enablement plus an
        # optional configuration override (redacted headers, like the base).
        f = Forwarder._from_resource(
            _forwarder_resource(
                environments={
                    "production": {"enabled": True},
                    "staging": {
                        "enabled": False,
                        "configuration": {
                            "method": "POST",
                            "url": "https://staging.siem.example.com/in",
                            "headers": [{"name": "DD-API-KEY", "value": "<redacted>"}],
                            "success_status": "2xx",
                        },
                    },
                }
            )
        )
        assert f.environments["production"].enabled is True
        assert f.environments["production"].configuration is None
        assert f.environments["staging"].enabled is False
        assert f.environments["staging"].configuration is not None
        assert f.environments["staging"].configuration.url == "https://staging.siem.example.com/in"
        assert f.environments["staging"].configuration.headers[0].value == "<redacted>"

    def test_forwarder_repr_shows_enabled_environments(self):
        f = Forwarder._from_resource(
            _forwarder_resource(environments={"production": {"enabled": True}, "staging": {"enabled": False}})
        )
        r = repr(f)
        assert "Datadog production" in r
        assert FWD_ID in r
        # Only environments where the forwarder is enabled show in the repr.
        assert "production" in r
        assert "staging" not in r


# ---------------------------------------------------------------------------
# Forwarders CRUD
# ---------------------------------------------------------------------------


class TestForwardersCrud:
    def test_new_returns_unsaved_forwarder(self):
        c = _client_with_handler(lambda req: httpx.Response(204))
        fwd = c.forwarders.new(
            FWD_ID,
            name="Datadog production",
            forwarder_type="datadog",
            configuration=HttpConfiguration(url="https://x"),
        )
        assert isinstance(fwd, Forwarder)
        assert fwd.id == FWD_ID
        assert fwd.created_at is None
        assert fwd._client is c.forwarders

    def test_new_defaults_name_to_id(self):
        c = _client_with_handler(lambda req: httpx.Response(204))
        fwd = c.forwarders.new(
            FWD_ID,
            forwarder_type="datadog",
            configuration=HttpConfiguration(url="https://x"),
        )
        assert fwd.name == FWD_ID

    def test_new_then_save_posts(self):
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["url"] = str(req.url)
            captured["body"] = req.content.decode()
            return httpx.Response(201, json={"data": _forwarder_resource()}, headers={"content-type": JSONAPI})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="Datadog production",
            forwarder_type="datadog",
            configuration=HttpConfiguration(
                url="https://siem.example.com/in",
                headers=[HttpHeader(name="DD-API-KEY", value="real-secret")],
            ),
            description="Forwards user.* events.",
            filter={"==": [{"var": "event_type"}, "user.created"]},
            transform="$",
            transform_type=TransformType.JSONATA,
        )
        fwd.save()
        # Server-truthful fields are refreshed on the original instance.
        assert fwd.id == FWD_ID
        assert fwd.created_at is not None
        assert fwd.version == 1
        assert captured["method"] == "POST"
        assert "/api/v1/forwarders" in captured["url"]
        # The customer-supplied key travels in the JSON:API data.id field.
        assert f'"id":"{FWD_ID}"' in captured["body"]
        assert "user.created" in captured["body"]
        assert "Forwards user.* events." in captured["body"]
        assert "JSONATA" in captured["body"]

    def test_new_with_environments_dict_round_trips_on_create(self):
        # The environments map travels on create. A bare ``{"enabled": True}``
        # dict is the lightweight form; a per-env configuration override is
        # sent as a full plaintext HttpConfiguration (like the base).
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = req.content.decode()
            return httpx.Response(
                201,
                json={
                    "data": _forwarder_resource(
                        environments={
                            "production": {"enabled": True},
                            "staging": {
                                "enabled": True,
                                "configuration": {
                                    "method": "POST",
                                    "url": "https://staging.example.com/in",
                                    "headers": [{"name": "X-Env", "value": "<redacted>"}],
                                    "success_status": "2xx",
                                },
                            },
                        }
                    )
                },
            )

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://prod.example.com/in"),
            environments={
                "production": {"enabled": True},
                "staging": {
                    "enabled": True,
                    "configuration": HttpConfiguration(
                        url="https://staging.example.com/in",
                        headers=[HttpHeader(name="X-Env", value="staging-secret")],
                    ),
                },
            },
        )
        fwd.save()
        # The map is on the wire, with the per-env override's plaintext header.
        assert '"environments"' in captured["body"]
        assert '"production"' in captured["body"]
        assert '"staging"' in captured["body"]
        assert "staging-secret" in captured["body"]
        assert "https://staging.example.com/in" in captured["body"]
        # Read-back populates the wrapper environments map.
        assert fwd.environments["production"].enabled is True
        assert fwd.environments["staging"].configuration.url == "https://staging.example.com/in"

    def test_new_with_forwarder_environment_instances(self):
        # The map also accepts ForwarderEnvironment instances directly.
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = req.content.decode()
            return httpx.Response(
                201,
                json={"data": _forwarder_resource(environments={"production": {"enabled": True}})},
            )

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
            environments={"production": ForwarderEnvironment(enabled=True)},
        )
        fwd.save()
        assert '"production"' in captured["body"]
        assert fwd.environments["production"].enabled is True

    def test_new_without_environments_omits_map(self):
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = req.content.decode()
            return httpx.Response(201, json={"data": _forwarder_resource()})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
        )
        fwd.save()
        # An empty/omitted environments map is not advertised on the wire.
        assert '"environments"' not in captured["body"]

    def test_list_does_not_send_filter_enabled(self):
        # ADR-055 removed filter[enabled] on list forwarders. The wrapper no
        # longer exposes the param and must not put it on the wire.
        seen_urls: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_urls.append(str(req.url))
            return httpx.Response(200, json={"data": [], "meta": {"pagination": {"page": 1, "size": 1000}}})

        c = _client_with_handler(handler)
        c.forwarders.list(forwarder_type="datadog")
        assert seen_urls, "list should have issued a request"
        assert "filter%5Benabled%5D" not in seen_urls[0]
        assert "filter[enabled]" not in seen_urls[0]
        # The retained forwarder_type filter is still threaded through.
        assert "filter%5Bforwarder_type%5D=datadog" in seen_urls[0] or "filter[forwarder_type]=datadog" in seen_urls[0]

    def test_new_requires_transform_type_when_transform_provided(self):
        c = _client_with_handler(lambda req: httpx.Response(204))
        with pytest.raises(ValueError, match="must be specified together"):
            c.forwarders.new(
                FWD_ID,
                name="x",
                forwarder_type="http",
                configuration=HttpConfiguration(url="https://x"),
                transform="$",
            )

    def test_new_requires_transform_when_transform_type_provided(self):
        c = _client_with_handler(lambda req: httpx.Response(204))
        with pytest.raises(ValueError, match="must be specified together"):
            c.forwarders.new(
                FWD_ID,
                name="x",
                forwarder_type="http",
                configuration=HttpConfiguration(url="https://x"),
                transform_type=TransformType.JSONATA,
            )

    def test_new_rejects_non_string_transform_for_jsonata(self):
        # JSONata templates are strings; the SDK must refuse other
        # shapes client-side rather than letting the server return a
        # 400.
        c = _client_with_handler(lambda req: httpx.Response(204))
        with pytest.raises(ValueError, match="must be a string when transform_type is JSONATA"):
            c.forwarders.new(
                FWD_ID,
                name="x",
                forwarder_type="http",
                configuration=HttpConfiguration(url="https://x"),
                transform={"wrap": "$"},
                transform_type=TransformType.JSONATA,
            )

    def test_new_without_transform_omits_transform_type(self):
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = req.content.decode()
            return httpx.Response(201, json={"data": _forwarder_resource()})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
        )
        fwd.save()
        # Neither field should be present in the request body when the
        # caller didn't supply a transform.
        assert "transform_type" not in captured["body"]
        assert '"transform":' not in captured["body"]

    def test_save_with_no_client_raises(self):
        fwd = Forwarder(
            None,
            id=FWD_ID,
            name="x",
            forwarder_type=ForwarderType("http"),
            configuration=HttpConfiguration(url="https://x"),
        )
        with pytest.raises(RuntimeError, match="without a client"):
            fwd.save()

    def test_create_without_id_raises(self):
        # Manually constructing a Forwarder without an id and then
        # save()-ing it must fail client-side — the audit service
        # requires a customer-supplied data.id on create.
        c = _client_with_handler(lambda req: httpx.Response(201, json={"data": _forwarder_resource()}))
        fwd = Forwarder(
            c.forwarders,
            name="x",
            forwarder_type=ForwarderType("http"),
            configuration=HttpConfiguration(url="https://x"),
        )
        with pytest.raises(ValueError, match="id is required"):
            fwd.save()

    def test_list_paginates(self):
        pages = [
            {
                "data": [_forwarder_resource(id_="a", name="A")],
                "meta": {"pagination": {"page": 1, "size": 1, "total": 2, "total_pages": 2}},
            },
            {
                "data": [_forwarder_resource(id_="b", name="B")],
                "meta": {"pagination": {"page": 2, "size": 1, "total": 2, "total_pages": 2}},
            },
        ]
        call_count = [0]

        def handler(req):
            page = pages[call_count[0]]
            call_count[0] += 1
            return httpx.Response(200, json=page)

        c = _client_with_handler(handler)
        first = c.forwarders.list(
            page_size=1,
            page_number=1,
            meta_total=True,
            forwarder_type="datadog",
        )
        assert len(first.forwarders) == 1
        # Listed forwarders are client-bound — save()/delete() on them works.
        assert first.forwarders[0]._client is c.forwarders
        assert first.pagination["total"] == 2
        assert first.pagination["page"] == 1
        iterated = list(first)
        assert len(iterated) == 1

        second = c.forwarders.list(page_size=1, page_number=2, meta_total=True)
        assert second.pagination["page"] == 2

    def test_get(self):
        def handler(req):
            assert FWD_ID in req.url.path
            return httpx.Response(200, json={"data": _forwarder_resource()})

        c = _client_with_handler(handler)
        fwd = c.forwarders.get(FWD_ID)
        assert fwd.id == FWD_ID
        # Bound to the client so save()/delete() works.
        assert fwd._client is c.forwarders

    def test_get_then_toggle_environment_then_save_puts(self):
        # Get-mutate-put on the environments map: disable a forwarder in an
        # environment by flipping that environment's ``enabled``.
        captured: dict[str, Any] = {}

        def handler(req):
            captured["method"] = req.method
            captured["url"] = str(req.url)
            captured["body"] = req.content.decode() if req.method == "PUT" else ""
            if req.method == "GET":
                return httpx.Response(
                    200,
                    json={"data": _forwarder_resource(environments={"production": {"enabled": True}})},
                )
            return httpx.Response(
                200,
                json={"data": _forwarder_resource(environments={"production": {"enabled": False}})},
            )

        c = _client_with_handler(handler)
        fwd = c.forwarders.get(FWD_ID)
        assert fwd.environments["production"].enabled is True
        fwd.environments["production"].enabled = False
        fwd.save()
        assert captured["method"] == "PUT"
        assert FWD_ID in captured["url"]
        # The environments map travels in the body; base ``enabled`` is
        # server-pinned false and not driven by the wrapper.
        assert '"environments"' in captured["body"]
        assert '"production"' in captured["body"]
        # Server-truthful environments map is back on the instance.
        assert fwd.environments["production"].enabled is False

    def test_enabled_is_read_only_and_ignored_on_save(self):
        # Setting the base ``enabled`` to True must not flip the wire value:
        # the base is server-pinned false and enablement is per-environment.
        captured: dict[str, Any] = {}

        def handler(req):
            captured["body"] = req.content.decode()
            return httpx.Response(201, json={"data": _forwarder_resource()})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
        )
        fwd.enabled = True  # attempt to enable via the read-only base field
        fwd.save()
        # The body never advertises enabled:true — the wrapper does not send
        # the base ``enabled`` as a writable enablement signal.
        assert '"enabled":true' not in captured["body"]
        # And the server-truthful value (always false) is reflected back.
        assert fwd.enabled is False

    def test_update_internal_with_no_id_raises(self):
        c = _client_with_handler(lambda req: httpx.Response(204))
        fwd = Forwarder(
            c.forwarders,
            name="x",
            forwarder_type=ForwarderType("http"),
            configuration=HttpConfiguration(url="https://x"),
            created_at=None,
        )
        # Manually mark as 'persisted' but leave id None to exercise the
        # update-path guard (id is None → save() routes to _update via
        # created_at, which then refuses).
        from datetime import datetime, timezone

        fwd.created_at = datetime.now(timezone.utc)
        with pytest.raises(ValueError, match="no id"):
            fwd.save()

    def test_forwarder_delete_removes_via_id(self):
        captured: dict[str, str] = {}

        def handler(req):
            captured["method"] = req.method
            captured["path"] = req.url.path
            return httpx.Response(204)

        c = _client_with_handler(handler)
        fwd = Forwarder._from_resource(_forwarder_resource(), client=c.forwarders)
        fwd.delete()
        assert captured["method"] == "DELETE"
        assert FWD_ID in captured["path"]

    def test_forwarder_delete_without_id_raises(self):
        # An unsaved Forwarder built manually (skipping new()) with no
        # id cannot be deleted — exercises the id-None guard.
        c = _client_with_handler(lambda req: httpx.Response(204))
        fwd = Forwarder(
            c.forwarders,
            name="x",
            forwarder_type=ForwarderType("http"),
            configuration=HttpConfiguration(url="https://x"),
        )
        with pytest.raises(RuntimeError, match="without a client or id"):
            fwd.delete()

    def test_forwarder_delete_without_client_raises(self):
        fwd = Forwarder._from_resource(_forwarder_resource())  # no client
        with pytest.raises(RuntimeError, match="without a client or id"):
            fwd.delete()

    def test_client_delete_by_id(self):
        captured: dict[str, str] = {}

        def handler(req):
            captured["method"] = req.method
            captured["path"] = req.url.path
            return httpx.Response(204)

        c = _client_with_handler(handler)
        c.forwarders.delete(FWD_ID)
        assert captured["method"] == "DELETE"
        assert FWD_ID in captured["path"]

    def test_delete_404_raises_not_found(self):
        def handler(req):
            return httpx.Response(404, json={"errors": []})

        c = _client_with_handler(handler)
        with pytest.raises(NotFoundError):
            c.forwarders.delete(FWD_ID)

    def test_delete_unexpected_2xx_raises_error(self):
        # Defensive: delete expects 204; a 200 response (server bug)
        # surfaces as a generic Error rather than passing silently.
        def handler(req):
            return httpx.Response(200, json={})

        c = _client_with_handler(handler)
        with pytest.raises(Error):
            c.forwarders.delete(FWD_ID)

    def test_save_unexpected_2xx_status_raises_error(self):
        def handler(req):
            return httpx.Response(200, json={})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
        )
        with pytest.raises(Error):
            fwd.save()


def test_async_client_exposes_forwarders():
    """The management ``AsyncAuditClient`` mirrors the sync one — the
    forwarders surface must reach async callers."""
    from smplkit.management.audit import AsyncAuditClient

    auth = _AuditAuthClient(base_url="https://audit.example.com", token="sk_api_test")
    c = AsyncAuditClient(auth_client=auth)
    assert c.forwarders is not None
