"""Offline resource-shape tests for native IAP configuration."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import pulumi
import pulumi.runtime
import pytest


class Mocks(pulumi.runtime.Mocks):
    def __init__(self):
        self.resources = []

    def new_resource(self, args):
        self.resources.append(args)
        return args.name, {
            **args.inputs,
            "name": args.inputs.get("name", args.name),
            "email": "runtime@example.com",
            "address": "192.0.2.1",
        }

    def call(self, args):
        return {**args.args, "number": "123456789"}


def run_stack(extra):
    mocks = Mocks()
    pulumi.runtime.set_mocks(mocks, project="agent-chat-internal", stack="prod")
    pulumi.runtime.set_all_config(
        {
            "gcp:project": "test-project",
            "agent-chat-internal:server-image-tag": "test",
            "agent-chat-internal:playground-image-tag": "test",
            "agent-chat-internal:mtx-playground-image": "example.com/mtx:test",
            "agent-chat-internal:playground-agents": '[{"id":"test","persona":"test"}]',
            **{
                f"agent-chat-internal:{key}": json.dumps(value)
                for key, value in extra.items()
            },
        }
    )

    @pulumi.runtime.test
    def execute():
        runpy.run_path(str(Path(__file__).with_name("__main__.py")))

    execute()
    return mocks.resources


@pytest.mark.parametrize(
    "clients",
    [
        None,
        [],
        ["web.apps.googleusercontent.com"],
        [
            "web.apps.googleusercontent.com",
            "android.apps.googleusercontent.com",
            "ios.apps.googleusercontent.com",
            "android-release.apps.googleusercontent.com",
        ],
    ],
)
def test_mobile_settings(clients):
    config = {} if clients is None else {"mobile-iap-client-ids": clients}
    resources = run_stack(config)
    settings = [r for r in resources if r.typ == "gcp:iap/settings:Settings"]
    assert len(settings) == (4 if clients else 0)
    for resource in settings:
        assert resource.name in {
            "agui-server-mobile-iap-settings",
            "agui-server-preview-mobile-iap-settings",
            "agui-playground-mtx-mobile-iap-settings",
            "agui-playground-mtx-preview-mobile-iap-settings",
        }
        backend = resource.name.removesuffix("-mobile-iap-settings") + "-backend"
        assert resource.inputs == {
            "name": f"projects/123456789/iap_web/compute/services/{backend}",
            "accessSettings": {"oauthSettings": {"programmaticClients": clients}},
        }
    backends = [
        r for r in resources if r.typ == "gcp:compute/backendService:BackendService"
    ]
    assert len(backends) == 6
    assert all(
        r.inputs["iap"]
        == {"enabled": True, "oauth2ClientId": " ", "oauth2ClientSecret": " "}
        for r in backends
    )
    grants = [
        r
        for r in resources
        if r.typ == "gcp:iap/webBackendServiceIamMember:WebBackendServiceIamMember"
    ]
    assert len(grants) == 6
    assert all(r.inputs["member"] == "domain:airbyte.io" for r in grants)


@pytest.mark.parametrize("configured", [False, True])
def test_mobile_environment(configured):
    extra = (
        {
            "mobile-redirect-uris": ["ai.airbyte.internal.mtx://auth"],
            "allowed-email-domains": ["airbyte.io"],
        }
        if configured
        else {}
    )
    services = [
        r
        for r in run_stack(extra)
        if r.typ == "gcp:cloudrunv2/service:Service"
        and r.name in {"agui-server", "agui-server-preview"}
    ]
    assert len(services) == 2
    for service in services:
        envs = {
            e["name"]: e.get("value")
            for e in service.inputs["template"]["containers"][0]["envs"]
        }
        for name, value in (
            ("MOBILE_REDIRECT_URIS", "ai.airbyte.internal.mtx://auth"),
            ("ALLOWED_EMAIL_DOMAINS", "airbyte.io"),
        ):
            key = f"AIRBYTE_AGUI_SERVER_{name}"
            assert (envs.get(key) == value) if configured else key not in envs


@pytest.mark.parametrize("value", ["not-a-list", [""]])
def test_invalid_config(value):
    with pytest.raises(ValueError, match="must be a list of nonempty strings"):
        run_stack({"mobile-iap-client-ids": value})
