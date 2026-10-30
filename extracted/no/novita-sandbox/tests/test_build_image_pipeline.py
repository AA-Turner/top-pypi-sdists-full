"""Exercise actual build entrypoints without a prior dry-run serialization."""
import json
import httpx
import pytest
from novita_sandbox import core
from novita_sandbox.core.api.client.client import AuthenticatedClient
from novita_sandbox.core.template.main import TemplateBase


@pytest.mark.asyncio
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_build_inherits_image_config_without_prior_serialization(
    monkeypatch, asynchronous
):
    builds = []

    def handle(request):
        if request.url.host == "registry.example.test":
            if "/manifests/" in request.url.path:
                return httpx.Response(200, json={"config": {"digest": "sha256:c"}})
            return httpx.Response(
                200,
                json={
                    "config": {
                        "Env": ["PATH=/opt/gs/bin:/usr/bin", "GS_IMAGE=enabled"],
                        "WorkingDir": "/workspace",
                        "Entrypoint": ["/opt/gs/bin/start"],
                    }
                },
            )
        assert request.method == "POST"
        if request.url.path == "/v3/templates":
            return httpx.Response(
                202,
                json={
                    "templateID": "template-id",
                    "buildID": "build-id",
                    "tags": [],
                    "aliases": [],
                    "names": ["gs-template"],
                    "public": False,
                },
            )
        assert request.url.path == "/v2/templates/template-id/builds/build-id"
        builds.append(json.loads(request.content))
        return httpx.Response(202)

    transport = httpx.MockTransport(handle)
    real_init = httpx.Client.__init__

    def init(self, *args, **kwargs):
        kwargs["transport"] = transport
        real_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", init)
    client = AuthenticatedClient(base_url="https://api.gs.example.test", token="key")
    template = TemplateBase().from_image("registry.example.test/team/image:1")
    with httpx.Client(base_url=client._base_url, transport=transport) as sync_client:
        async with httpx.AsyncClient(
            base_url=client._base_url, transport=transport
        ) as async_client:
            client.set_httpx_client(sync_client)
            client.set_async_httpx_client(async_client)
            if asynchronous:
                await core.AsyncTemplate._build(client, template, "gs-template")
            else:
                core.Template._build(client, template, "gs-template")

    assert len(builds) == 1
    body = builds[0]
    assert body["startCmd"] == "/opt/gs/bin/start"
    assert any(
        step["type"] == "WORKDIR" and step["args"] == ["/workspace"]
        for step in body["steps"]
    )
    assert any(
        ".novita-image-env.sh" in " ".join(step["args"]) for step in body["steps"]
    )
