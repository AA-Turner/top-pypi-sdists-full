"""Tests for the audit forwarders management surface.

The httpx.MockTransport pattern is reused here — none of these tests
touch the network. Coverage target is 100% on every line in
``smplkit.audit.forwarders`` and the forwarder portion of
``smplkit.audit.models``.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from smplkit import Error, NotFoundError
from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient
from smplkit.audit import (
    AsyncForwarder,
    Forwarder,
    ForwarderEnvironment,
    ForwarderType,
    HttpConfiguration,
    HttpMethod,
    TransformType,
)
from smplkit.audit.clients import AuditClient


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
    forward_smplkit_events: bool = False,
) -> dict[str, Any]:
    # There is no top-level ``enabled`` on the wire anymore (ADR-056);
    # enablement is driven entirely by the per-environment overlay.
    return {
        "id": id_,
        "type": "forwarder",
        "attributes": {
            "name": name,
            "forwarder_type": forwarder_type,
            "forward_smplkit_events": forward_smplkit_events,
            "environments": environments if environments is not None else {},
            "description": description,
            "filter": filter_,
            "transform": transform,
            "transform_type": transform_type,
            "configuration": {
                "method": "POST",
                "url": "https://siem.example.com/in",
                "headers": {"DD-API-KEY": "dd-api-key-plaintext"},
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
# HttpConfiguration — base config (headers as a name→value object)
# ---------------------------------------------------------------------------


class TestHttpConfiguration:
    def test_round_trip(self):
        h = HttpConfiguration(
            method=HttpMethod.PUT,
            url="https://x.example/in",
            headers={"A": "1"},
            success_status="200",
        )
        d = h._to_dict()
        assert d["method"] == "PUT"
        assert d["url"] == "https://x.example/in"
        assert d["headers"] == {"A": "1"}
        again = HttpConfiguration._from_dict(d)
        assert again.method == "PUT"
        assert again.url == "https://x.example/in"
        assert again.headers == {"A": "1"}
        assert again.success_status == "200"

    def test_set_and_get_header(self):
        h = HttpConfiguration(url="https://x")
        assert h.get_header("A") is None
        h.set_header("A", "1")
        assert h.get_header("A") == "1"
        # set_header replaces in place.
        h.set_header("A", "2")
        assert h.get_header("A") == "2"
        assert h._to_dict()["headers"] == {"A": "2"}

    def test_from_dict_defaults(self):
        # Empty dict should produce a sane default HttpConfiguration.
        h = HttpConfiguration._from_dict({})
        assert h.method == HttpMethod.POST
        assert h.headers == {}
        assert h.url == ""
        assert h.success_status == "2xx"
        # Pre-existing forwarders persisted before the field landed must
        # read back as tls_verify=True so they keep their prior secure default.
        assert h.tls_verify is True
        assert h.ca_cert is None

    def test_round_trips_tls_fields(self):
        h = HttpConfiguration(
            url="https://x",
            tls_verify=False,
            ca_cert="-----BEGIN CERTIFICATE-----\nfoo\n-----END CERTIFICATE-----",
        )
        d = h._to_dict()
        assert d["tls_verify"] is False
        assert "BEGIN CERTIFICATE" in d["ca_cert"]
        again = HttpConfiguration._from_dict(d)
        assert again.tls_verify is False
        assert again.ca_cert == h.ca_cert

    def test_from_dict_falsey_tls_verify_is_preserved(self):
        # An explicit ``false`` on the wire must read back false, not the
        # secure default (which only applies when the field is absent).
        h = HttpConfiguration._from_dict({"url": "https://x", "tls_verify": False})
        assert h.tls_verify is False

    def test_accepts_raw_string_method(self):
        # ``HttpMethod`` is a ``str`` subclass, so callers passing the
        # literal still type-check and round-trip cleanly.
        h = HttpConfiguration._from_dict({"method": "PATCH", "url": "https://x"})
        assert h.method == HttpMethod.PATCH

    def test_repr(self):
        h = HttpConfiguration(url="https://x", method=HttpMethod.PUT)
        r = repr(h)
        assert "https://x" in r
        assert "PUT" in r


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TestEnums:
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


# ---------------------------------------------------------------------------
# ForwarderEnvironment — sparse per-environment override (ADR-056)
# ---------------------------------------------------------------------------


class TestForwarderEnvironment:
    def test_defaults_disabled_and_all_leaves_none(self):
        e = ForwarderEnvironment()
        assert e.enabled is False
        assert e.url is None
        assert e.method is None
        assert e.success_status is None
        assert e.tls_verify is None
        assert e.ca_cert is None
        assert e.headers == {}
        # An empty disabled override emits only ``enabled``.
        assert e._to_payload() == {"enabled": False}

    def test_reading_unset_leaf_returns_none_no_base_merge(self):
        # The SDK never merges the base value in — an unset leaf reads None.
        e = ForwarderEnvironment(enabled=True, url="https://prod")
        assert e.url == "https://prod"
        assert e.method is None
        assert e.success_status is None

    def test_set_and_get_header(self):
        e = ForwarderEnvironment(enabled=True)
        assert e.get_header("Auth") is None
        e.set_header("Auth", "Bearer prod")
        assert e.get_header("Auth") == "Bearer prod"
        e.set_header("Auth", "Bearer prod2")
        assert e.get_header("Auth") == "Bearer prod2"

    def test_to_payload_emits_only_set_leaves(self):
        e = ForwarderEnvironment(
            enabled=True,
            url="https://prod",
            method="PUT",
            success_status="200",
            tls_verify=False,
            ca_cert="-----BEGIN CERTIFICATE-----\nx\n-----END CERTIFICATE-----",
        )
        e.set_header("DD-API-KEY", "prod-secret")
        payload = e._to_payload()
        assert payload == {
            "enabled": True,
            "url": "https://prod",
            "method": "PUT",
            "success_status": "200",
            "tls_verify": False,
            "ca_cert": "-----BEGIN CERTIFICATE-----\nx\n-----END CERTIFICATE-----",
            "headers.DD-API-KEY": "prod-secret",
        }

    def test_to_payload_omits_unset_scalar_leaves(self):
        # Only ``enabled`` and ``url`` are set; the rest stay off the overlay.
        e = ForwarderEnvironment(enabled=True, url="https://prod")
        assert e._to_payload() == {"enabled": True, "url": "https://prod"}

    def test_from_dict_parses_flat_overlay(self):
        e = ForwarderEnvironment._from_dict(
            {
                "enabled": True,
                "url": "https://prod",
                "method": "PUT",
                "success_status": "204",
                "tls_verify": False,
                "ca_cert": "ca-pem",
                "headers.DD-API-KEY": "prod-secret",
            }
        )
        assert e.enabled is True
        assert e.url == "https://prod"
        assert e.method == "PUT"
        assert e.success_status == "204"
        assert e.tls_verify is False
        assert e.ca_cert == "ca-pem"
        assert e.headers == {"DD-API-KEY": "prod-secret"}

    def test_from_dict_first_dot_header_split_preserves_dotted_names(self):
        # ``headers.X-Foo.Bar`` parses on the FIRST dot, preserving the
        # dotted header name ``X-Foo.Bar``.
        e = ForwarderEnvironment._from_dict({"enabled": True, "headers.X-Foo.Bar": "v"})
        assert e.headers == {"X-Foo.Bar": "v"}

    def test_from_dict_ignores_unknown_leaves(self):
        # Forward compatibility: unknown leaves and a dotless ``headers`` key
        # are dropped without error.
        e = ForwarderEnvironment._from_dict(
            {"enabled": True, "url": "https://prod", "future_leaf": "x", "headers": "no-name"}
        )
        assert e.url == "https://prod"
        assert e.headers == {}
        assert e._to_payload() == {"enabled": True, "url": "https://prod"}

    def test_from_dict_empty_defaults_disabled(self):
        e = ForwarderEnvironment._from_dict({})
        assert e.enabled is False
        assert e._to_payload() == {"enabled": False}

    def test_from_dict_none_raw_defaults_disabled(self):
        # ``_from_dict`` tolerates a falsey ``raw`` (e.g. ``None``) via the
        # ``(raw or {})`` guard.
        e = ForwarderEnvironment._from_dict(None)  # type: ignore[arg-type]
        assert e.enabled is False

    def test_repr_lists_overridden_leaves_sorted(self):
        e = ForwarderEnvironment(enabled=True, url="https://prod", method="PUT")
        e.set_header("Auth", "x")
        r = repr(e)
        assert "enabled=True" in r
        # Overrides are sorted: headers.Auth, method, url.
        assert r.index("headers.Auth") < r.index("method") < r.index("url")


# ---------------------------------------------------------------------------
# Forwarder — model behavior (environment accessor, enabled rollup, parse)
# ---------------------------------------------------------------------------


class TestForwarderModel:
    def test_from_resource(self):
        f = Forwarder._from_resource(_forwarder_resource())
        assert f.id == FWD_ID
        assert f.name == "Datadog production"
        assert f.configuration.get_header("DD-API-KEY") == "dd-api-key-plaintext"
        assert f.version == 1
        assert f.deleted_at is None
        assert f.description is None
        assert f.transform_type is None
        # No environments by default → not enabled anywhere.
        assert f.enabled is False
        assert f.environments == {}
        # forward_smplkit_events defaults to false.
        assert f.forward_smplkit_events is False
        # No client attached when _from_resource is called bare.
        assert f._client is None

    def test_from_resource_returns_transform_type_enum(self):
        f = Forwarder._from_resource(_forwarder_resource(transform="$", transform_type="JSONATA"))
        assert f.transform == "$"
        assert f.transform_type is TransformType.JSONATA

    def test_from_resource_surfaces_forward_smplkit_events(self):
        f = Forwarder._from_resource(_forwarder_resource(forward_smplkit_events=True))
        assert f.forward_smplkit_events is True

    def test_from_resource_defaults_forward_smplkit_events_when_absent(self):
        # A forwarder persisted before the field landed has no
        # ``forward_smplkit_events`` on the wire — it must read back false.
        resource = _forwarder_resource()
        del resource["attributes"]["forward_smplkit_events"]
        f = Forwarder._from_resource(resource)
        assert f.forward_smplkit_events is False

    def test_from_resource_reads_sparse_environments(self):
        # Per-environment sparse overrides round-trip on read: enablement plus
        # only the leaves each environment overrides.
        f = Forwarder._from_resource(
            _forwarder_resource(
                environments={
                    "production": {"enabled": True},
                    "staging": {
                        "enabled": False,
                        "url": "https://staging.siem.example.com/in",
                        "headers.DD-API-KEY": "staging-secret",
                    },
                }
            )
        )
        assert f.environments["production"].enabled is True
        assert f.environments["production"].url is None
        assert f.environments["staging"].enabled is False
        assert f.environments["staging"].url == "https://staging.siem.example.com/in"
        assert f.environments["staging"].get_header("DD-API-KEY") == "staging-secret"

    def test_enabled_rollup_true_when_any_env_enabled(self):
        f = Forwarder._from_resource(
            _forwarder_resource(environments={"production": {"enabled": True}, "staging": {"enabled": False}})
        )
        assert f.enabled is True

    def test_enabled_rollup_false_when_no_env_enabled(self):
        f = Forwarder._from_resource(
            _forwarder_resource(environments={"production": {"enabled": False}, "staging": {"enabled": False}})
        )
        assert f.enabled is False

    def test_environment_accessor_lazily_creates_and_returns(self):
        f = Forwarder._from_resource(_forwarder_resource())
        assert f.environments == {}
        env = f.environment("production")
        assert isinstance(env, ForwarderEnvironment)
        # Inserted into the map on first access.
        assert f.environments["production"] is env
        # Second access returns the same instance.
        assert f.environment("production") is env
        # Mutating through the accessor drives the enabled rollup.
        assert f.enabled is False
        f.environment("production").enabled = True
        assert f.enabled is True

    def test_repr_shows_enabled_environments_only(self):
        f = Forwarder._from_resource(
            _forwarder_resource(environments={"production": {"enabled": True}, "staging": {"enabled": False}})
        )
        r = repr(f)
        assert "Datadog production" in r
        assert FWD_ID in r
        # Only environments where the forwarder is enabled show in the repr.
        assert "production" in r
        assert "staging" not in r

    def test_async_forwarder_shares_model_behavior(self):
        # AsyncForwarder shares the (non-async) model surface with Forwarder —
        # the async surface only differs on save()/delete().
        f = AsyncForwarder._from_resource(_forwarder_resource())
        assert isinstance(f, AsyncForwarder)
        f.environment("production").enabled = True
        f.environment("production").set_header("Auth", "x")
        assert f.enabled is True
        assert f.environments["production"].get_header("Auth") == "x"


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
                headers={"DD-API-KEY": "real-secret"},
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
        # Headers travel as a name→value object on the base configuration.
        assert "real-secret" in captured["body"]

    def test_new_with_environments_dict_round_trips_on_create(self):
        # The sparse environments overlay travels on create. A bare
        # ``{"enabled": True}`` dict is the lightweight form; per-env leaves
        # (``url``, ``headers``) travel as a flat sparse overlay.
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
                                "url": "https://staging.example.com/in",
                                "headers.X-Env": "x-env-plaintext",
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
                    "url": "https://staging.example.com/in",
                    "headers": {"X-Env": "staging-secret"},
                },
            },
        )
        fwd.save()
        # The overlay is on the wire, with the per-env leaf and header.
        assert '"environments"' in captured["body"]
        assert '"production"' in captured["body"]
        assert '"staging"' in captured["body"]
        assert "staging-secret" in captured["body"]
        assert "https://staging.example.com/in" in captured["body"]
        assert "headers.X-Env" in captured["body"]
        # Read-back populates the wrapper environments map.
        assert fwd.environments["production"].enabled is True
        assert fwd.environments["staging"].url == "https://staging.example.com/in"
        assert fwd.environments["staging"].get_header("X-Env") == "x-env-plaintext"

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

    def test_new_with_forward_smplkit_events_posts_field(self):
        # Opting in to platform change events sends forward_smplkit_events:true
        # on create and reads the server-truthful value back.
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = req.content.decode()
            return httpx.Response(201, json={"data": _forwarder_resource(forward_smplkit_events=True)})

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
            forward_smplkit_events=True,
        )
        assert fwd.forward_smplkit_events is True
        fwd.save()
        assert '"forward_smplkit_events":true' in captured["body"]
        # Server-truthful value is reflected back on the instance.
        assert fwd.forward_smplkit_events is True

    def test_new_without_forward_smplkit_events_omits_field(self):
        # The additive default (false) stays implicit: existing callers who
        # don't set it produce a body without the field.
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
        # Defaults to false on the unsaved instance.
        assert fwd.forward_smplkit_events is False
        fwd.save()
        assert "forward_smplkit_events" not in captured["body"]
        assert fwd.forward_smplkit_events is False

    def test_get_then_toggle_forward_smplkit_events_then_save_puts(self):
        # Get-mutate-put: flip forward_smplkit_events on an existing forwarder.
        captured: dict[str, Any] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["body"] = req.content.decode() if req.method == "PUT" else ""
            if req.method == "GET":
                return httpx.Response(200, json={"data": _forwarder_resource(forward_smplkit_events=False)})
            return httpx.Response(200, json={"data": _forwarder_resource(forward_smplkit_events=True)})

        c = _client_with_handler(handler)
        fwd = c.forwarders.get(FWD_ID)
        assert fwd.forward_smplkit_events is False
        fwd.forward_smplkit_events = True
        fwd.save()
        assert captured["method"] == "PUT"
        assert '"forward_smplkit_events":true' in captured["body"]
        # Server-truthful value back on the instance after PUT.
        assert fwd.forward_smplkit_events is True

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

    def test_list_without_forwarder_type_omits_filter(self):
        seen_urls: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_urls.append(str(req.url))
            return httpx.Response(200, json={"data": [], "meta": {"pagination": {"page": 1, "size": 1000}}})

        c = _client_with_handler(handler)
        c.forwarders.list()
        assert "filter%5Bforwarder_type%5D" not in seen_urls[0]
        assert "filter[forwarder_type]" not in seen_urls[0]

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
        assert len(first) == 1

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
        assert fwd.enabled is True
        fwd.environment("production").enabled = False
        fwd.save()
        assert captured["method"] == "PUT"
        assert FWD_ID in captured["url"]
        # The environments overlay travels in the body.
        assert '"environments"' in captured["body"]
        assert '"production"' in captured["body"]
        # Server-truthful environments map is back on the instance.
        assert fwd.environments["production"].enabled is False
        assert fwd.enabled is False

    def test_enable_via_environment_accessor_then_save(self):
        # The accessor lazily creates an override, which then travels on save.
        captured: dict[str, Any] = {}

        def handler(req):
            captured["body"] = req.content.decode()
            return httpx.Response(
                201, json={"data": _forwarder_resource(environments={"production": {"enabled": True}})}
            )

        c = _client_with_handler(handler)
        fwd = c.forwarders.new(
            FWD_ID,
            name="x",
            forwarder_type="http",
            configuration=HttpConfiguration(url="https://x"),
        )
        fwd.environment("production").enabled = True
        fwd.environment("production").set_header("DD-API-KEY", "prod-secret")
        assert fwd.enabled is True
        fwd.save()
        assert '"production"' in captured["body"]
        assert "headers.DD-API-KEY" in captured["body"]
        assert "prod-secret" in captured["body"]

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
    """The async audit client exposes the genuinely-async forwarders surface."""
    from smplkit.audit.clients import AsyncAuditClient
    from smplkit.audit.forwarders import AsyncForwardersClient

    auth = _AuditAuthClient(base_url="https://audit.example.com", token="sk_api_test")
    c = AsyncAuditClient(auth_client=auth)
    assert isinstance(c.forwarders, AsyncForwardersClient)
