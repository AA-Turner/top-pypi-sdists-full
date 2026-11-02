"""Opt-in LIBERO HTTP client; no changes to Dreamscale's existing robot transport.

Keep the same request identity after a timeout and use get_result. Neither
client retries inference automatically. Server owns rotation and preprocessing.
"""

from __future__ import annotations

import base64
import io
import math
import re
import time
from urllib.parse import urlsplit
from uuid import UUID

import httpx
import numpy as np
from dreamscale_transport import catalog
from PIL import Image

from dreamscale.errors import from_payload
from dreamscale.model_names import internal_model

# The models hosted inference serves (the catalog's hosted_inference): each one's actions
# per request, and the model a deployment or response naming none means.
_ACTION_STEPS = {entry.id: entry.hosted_inference.action_steps
                 for entry in catalog.hosted_inference_models()}
_DEFAULT_MODEL = catalog.hosted_inference_default()


def _integer(value, name, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [0, {maximum}]")
    return value


def _deployment_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,96}", value):
        raise ValueError("invalid deployment ID")
    return value


def _vector(value, size):
    array = np.asarray(value)
    if array.shape != (size,) or array.dtype.kind not in "fi" or not np.isfinite(array).all():
        raise ValueError(f"expected a finite {size}-element numeric vector")
    return array.astype(float).tolist()


def action_request(
    *,
    deployment_id: str,
    robot_slot: int,
    sequence: int,
    request_id: UUID | str,
    episode_id: str,
    noise_seed: int,
    instruction: str,
    observation: dict,
) -> dict:
    """Encode unmodified raw RGB simulator frames; no resize, rotation or merging."""
    _deployment_id(deployment_id)
    if not isinstance(instruction, str) or not instruction.strip() or len(instruction) > 2048:
        raise ValueError("instruction must be nonblank and at most 2048 characters")
    if not isinstance(episode_id, str) or not 1 <= len(episode_id) <= 128:
        raise ValueError("invalid episode ID")
    payload = {}
    for key in ("agentview_image", "robot0_eye_in_hand_image"):
        image = np.asarray(observation[key])
        if (
            image.dtype != np.uint8
            or image.ndim != 3
            or image.shape[2] != 3
            or not all(0 < n <= 2048 for n in image.shape[:2])
        ):
            raise ValueError("images must be raw RGB uint8 within 2048x2048")
        encoded = io.BytesIO()
        Image.fromarray(image).save(encoded, format="PNG")
        if encoded.tell() > 2 * 1024**2:
            raise ValueError("PNG exceeds 2 MiB; do not silently resize the observation")
        payload[key] = {
            "encoding": "png",
            "data": base64.b64encode(encoded.getvalue()).decode("ascii"),
        }
    payload["robot0_eef_pos"] = _vector(observation["robot0_eef_pos"], 3)
    quaternion = _vector(observation["robot0_eef_quat"], 4)
    if abs(math.fsum(x * x for x in quaternion) - 1) > 0.001:
        raise ValueError("expected normalized xyzw robot0_eef_quat")
    payload["robot0_eef_quat_xyzw"] = quaternion
    payload["robot0_gripper_qpos"] = _vector(observation["robot0_gripper_qpos"], 2)
    return {
        "deployment_id": deployment_id,
        "robot_slot": _integer(robot_slot, "robot_slot", 127),
        "sequence": _integer(sequence, "sequence", 2**63 - 1),
        "request_id": str(UUID(str(request_id))),
        "episode_id": episode_id,
        "noise_seed": _integer(noise_seed, "noise_seed", 2**63 - 1),
        "instruction": instruction,
        "observation": payload,
    }


def _options(api_key, api_base, timeout, transport, event_hooks):
    if api_key is None or api_base is None:
        from dreamscale.config import load_config

        config = load_config()
        api_key = config.api_key if api_key is None else api_key
        api_base = config.control_plane_url if api_base is None else api_base
    if not isinstance(api_base, str):
        raise ValueError("api_base must be an HTTPS origin")
    url = urlsplit(api_base)
    if (
        url.scheme != "https"
        or not url.hostname
        or url.username
        or url.password
        or url.query
        or url.fragment
        or url.path not in ("", "/")
    ):
        raise ValueError("api_base must be an HTTPS origin without credentials or a path")
    if not isinstance(api_key, str) or not api_key or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("API key and positive finite timeout are required")
    return {
        "base_url": api_base,
        "headers": {"Authorization": f"Bearer {api_key}"},
        "timeout": httpx.Timeout(timeout, connect=min(5.0, timeout)),
        "follow_redirects": False,
        "trust_env": False,
        "transport": transport,
        "event_hooks": event_hooks or {},
    }


def _decode(response):
    value = response.json()
    if not 200 <= response.status_code < 300:
        raise from_payload(value)
    if not isinstance(value, dict):
        raise ValueError("invalid inference response envelope")
    return value


def _capacity(robots):
    if type(robots) is not int or not 8 <= robots <= 128 or robots % 8:
        raise ValueError("capacity must be a multiple of eight robots between 8 and 128")
    return robots


def _creation(
    idempotency_key, warm_robots, max_robots, robots_per_replica=8, model=_DEFAULT_MODEL
):
    if not isinstance(idempotency_key, str) or not re.fullmatch(
        r"[\x21-\x7e]{1,128}", idempotency_key
    ):
        raise ValueError("idempotency key must be 1–128 visible ASCII characters")
    if _capacity(warm_robots) > _capacity(max_robots):
        raise ValueError("warm capacity exceeds maximum capacity")
    if type(robots_per_replica) is not int or robots_per_replica not in (8, 16):
        raise ValueError("robots_per_replica must be 8 or 16")
    if (
        warm_robots % robots_per_replica
        or max_robots % robots_per_replica
        or max_robots // robots_per_replica > 8
    ):
        raise ValueError("capacity must align with density and use at most eight H100s")
    if internal_model(model) not in _ACTION_STEPS:
        raise ValueError("unsupported pooled model")
    body = dict(model=model, warm_robots=warm_robots, max_robots=max_robots)
    if robots_per_replica != 8:
        body["robots_per_replica"] = robots_per_replica
    return body


def _actions(response, identity):
    value = _decode(response)
    if any(
        value.get(key) != identity[key]
        for key in ("deployment_id", "robot_slot", "request_id", "sequence", "episode_id")
        if key in identity
    ):
        raise ValueError("inference response identity mismatch")
    if response.status_code == 202:
        if value.get("status") != "pending" or "actions" in value:
            raise ValueError("invalid pending inference response")
        return value
    actions = value.get("actions")
    steps = _ACTION_STEPS.get(internal_model(value.get("model", _DEFAULT_MODEL)))
    if steps is None or not isinstance(actions, list) or len(actions) != steps:
        raise ValueError("expected finite 10x7 actions")
    for row in actions:
        if (
            not isinstance(row, list)
            or len(row) != 7
            or any(type(x) not in (int, float) or not math.isfinite(x) for x in row)
        ):
            raise ValueError("expected finite 10x7 actions")
    return value


def _result_identity(deployment_id, robot_slot, request_id, sequence=None):
    _deployment_id(deployment_id)
    return {
        "deployment_id": deployment_id,
        "robot_slot": _integer(robot_slot, "robot_slot", 127),
        "request_id": str(UUID(str(request_id))),
        **({"sequence": _integer(sequence, "sequence", 2**63 - 1)} if sequence is not None else {}),
    }


def _resolution_identity(deployment_id, robot_slot, request_id, sequence, episode_id):
    if not isinstance(episode_id, str) or not 1 <= len(episode_id) <= 128:
        raise ValueError("invalid episode ID")
    _integer(sequence, "sequence", 2**63 - 1)
    return {
        **_result_identity(deployment_id, robot_slot, request_id, sequence),
        "episode_id": episode_id,
    }


def _resolution(response, identity):
    if response.status_code == 422:
        value = response.json()
        if isinstance(value, dict) and value.get("status") == "failed":
            if (
                any(value.get(k) != v for k, v in identity.items())
                or "actions" in value
                or not isinstance(value.get("error"), dict)
                or value["error"].get("code")
                not in ("request_not_admitted", "expired", "preprocessing_failed")
            ):
                raise ValueError("invalid terminal inference resolution")
            return value
    return _actions(response, identity)


def _connection(response, *, api_origin=None):
    value = _decode(response)
    origin = value.get("api_base")
    if (
        not isinstance(origin, str)
        or "\\" in origin
        or any(char.isspace() or ord(char) < 32 for char in origin)
    ):
        raise ValueError("invalid gateway connection origin")
    url = urlsplit(origin)
    expires = value.get("expires_at")
    if (
        url.scheme != "https"
        or url.username is not None
        or url.password is not None
        or url.port not in (None, 443)
        or url.path not in ("", "/")
        or url.query
        or url.fragment
        or not (
            re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)*\.modal\.host", url.hostname or "")
            or (
                api_origin is not None
                and (url.scheme, url.hostname, url.port or 443)
                == (api_origin.scheme, api_origin.host, api_origin.port or 443)
            )
        )
        or type(expires) is not int
        or expires <= time.time()
        or not isinstance(value.get("instance_id"), str)
        or not value["instance_id"]
    ):
        raise ValueError("invalid or expired gateway connection")
    return origin.rstrip("/"), expires


def _replica_connection(response, scope):
    origin, expires = _connection(response)
    value = response.json()
    token = value.get("access_token")
    if (
        (value.get("deployment_id"), value.get("robot_slot")) != scope
        or type(value.get("robot_slot")) is not int
        or not isinstance(token, str)
        or len(token) > 2041
        or not re.fullmatch(r"dbir1\.[A-Za-z0-9_-]+\.[a-f0-9]{64}", token)
        or not re.fullmatch(r"[a-f0-9]{32}", value.get("replica_id", ""))
    ):
        raise ValueError("invalid or out-of-scope replica connection")
    return origin, expires, token


def _enable_replica(scopes, connections, deployment_id, robot_slot):
    scope = _deployment_id(deployment_id), _integer(robot_slot, "robot_slot", 127)
    if scope not in scopes and len(scopes) >= 128:
        raise ValueError("one inference client supports at most 128 replica scopes")
    scopes.add(scope)
    connections.pop(scope, None)
    return scope


class InferenceClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        timeout=5.0,
        transport=None,
        event_hooks=None,
    ):
        self._http = httpx.Client(**_options(api_key, api_base, timeout, transport, event_hooks))
        self._direct, self._expires, self._connect_enabled = None, 0, False
        self._replica_scopes, self._replicas = set(), {}

    def connect(self):
        """Discover a live direct gateway; status always uses the stable origin."""
        self._connect_enabled, self._direct = True, None
        self._direct, self._expires = _connection(
            self._http.get("/v1/connection"), api_origin=self._http.base_url
        )

    def connect_replica(self, *, deployment_id, robot_slot):
        """Dev-only diagnostic route; never send the API key to the worker."""
        scope = _enable_replica(self._replica_scopes, self._replicas, deployment_id, robot_slot)
        response = self._http.get(
            "/v1/replica-connection",
            params=dict(deployment_id=deployment_id, robot_slot=robot_slot),
        )
        self._replicas[scope] = _replica_connection(response, scope)

    def predict(self, request: dict) -> dict:
        scope = request.get("deployment_id"), request.get("robot_slot")
        replica = None
        if scope in self._replica_scopes:
            replica = self._replicas.get(scope)
            if replica is None or time.time() + 1 >= replica[1]:
                self.connect_replica(deployment_id=scope[0], robot_slot=scope[1])
                replica = self._replicas[scope]
        elif self._connect_enabled and (self._direct is None or time.time() >= self._expires):
            self.connect()
        try:
            response = self._http.post(
                (replica[0] if replica else self._direct or "") + "/v1/actions",
                json=request,
                headers={"Authorization": "Bearer " + replica[2]} if replica else None,
                extensions={"dropbear_request_id": request.get("request_id")},
            )
        except httpx.TransportError:
            self._direct = None
            self._replicas.pop(scope, None)
            raise  # An unknown POST is never repeated, even after rediscovery.
        if response.status_code >= 500:
            self._direct = None
        if response.status_code in (401, 403) or response.status_code >= 500:
            self._replicas.pop(scope, None)
        return _actions(response, request)

    def get_result(self, *, deployment_id, robot_slot, request_id, sequence=None):
        identity = _result_identity(deployment_id, robot_slot, request_id, sequence)
        return _actions(
            self._http.get(
                f"/v1/actions/{identity['request_id']}",
                params={k: v for k, v in identity.items() if k != "request_id"},
                extensions={"dropbear_request_id": identity["request_id"]},
            ),
            identity,
        )

    def resolve_request(self, *, deployment_id, robot_slot, request_id, sequence, episode_id):
        """Close only unadmitted work; running work stays pending. Never replay inference."""
        identity = _resolution_identity(deployment_id, robot_slot, request_id, sequence, episode_id)
        return _resolution(
            self._http.post(
                f"/v1/actions/{identity['request_id']}/resolve",
                json=identity,
                extensions={"dropbear_request_id": identity["request_id"]},
            ),
            identity,
        )

    def create_deployment(
        self,
        *,
        idempotency_key,
        warm_robots=8,
        max_robots=64,
        robots_per_replica=8,
        model=_DEFAULT_MODEL,
    ):
        body = _creation(idempotency_key, warm_robots, max_robots, robots_per_replica, model)
        return _decode(
            self._http.post(
                "/v1/inference/deployments",
                headers={"Idempotency-Key": idempotency_key},
                json=body,
            )
        )

    def deployment(self, deployment_id):
        return _decode(self._http.get(f"/v1/inference/deployments/{_deployment_id(deployment_id)}"))

    def warm(self, deployment_id, robots):
        _deployment_id(deployment_id)
        return _decode(
            self._http.patch(
                f"/v1/inference/deployments/{deployment_id}",
                json={"warm_robots": _capacity(robots)},
            )
        )

    def stop(self, deployment_id):
        _deployment_id(deployment_id)
        return _decode(self._http.delete(f"/v1/inference/deployments/{deployment_id}"))

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class AsyncInferenceClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        timeout=5.0,
        transport=None,
        event_hooks=None,
    ):
        self._http = httpx.AsyncClient(
            **_options(api_key, api_base, timeout, transport, event_hooks)
        )
        self._direct, self._expires, self._connect_enabled = None, 0, False
        self._replica_scopes, self._replicas = set(), {}

    async def connect(self):
        """Discover a live direct gateway; status always uses the stable origin."""
        self._connect_enabled, self._direct = True, None
        self._direct, self._expires = _connection(
            await self._http.get("/v1/connection"), api_origin=self._http.base_url
        )

    async def connect_replica(self, *, deployment_id, robot_slot):
        """Dev-only diagnostic route; stable origin retains status recovery."""
        scope = _enable_replica(self._replica_scopes, self._replicas, deployment_id, robot_slot)
        response = await self._http.get(
            "/v1/replica-connection",
            params=dict(deployment_id=deployment_id, robot_slot=robot_slot),
        )
        self._replicas[scope] = _replica_connection(response, scope)

    async def predict(self, request: dict) -> dict:
        scope = request.get("deployment_id"), request.get("robot_slot")
        replica = None
        if scope in self._replica_scopes:
            replica = self._replicas.get(scope)
            if replica is None or time.time() + 1 >= replica[1]:
                await self.connect_replica(deployment_id=scope[0], robot_slot=scope[1])
                replica = self._replicas[scope]
        elif self._connect_enabled and (self._direct is None or time.time() >= self._expires):
            await self.connect()
        try:
            response = await self._http.post(
                (replica[0] if replica else self._direct or "") + "/v1/actions",
                json=request,
                headers={"Authorization": "Bearer " + replica[2]} if replica else None,
                extensions={"dropbear_request_id": request.get("request_id")},
            )
        except httpx.TransportError:
            self._direct = None
            self._replicas.pop(scope, None)
            raise
        if response.status_code >= 500:
            self._direct = None
        if response.status_code in (401, 403) or response.status_code >= 500:
            self._replicas.pop(scope, None)
        return _actions(response, request)

    async def get_result(self, *, deployment_id, robot_slot, request_id, sequence=None):
        identity = _result_identity(deployment_id, robot_slot, request_id, sequence)
        return _actions(
            await self._http.get(
                f"/v1/actions/{identity['request_id']}",
                params={k: v for k, v in identity.items() if k != "request_id"},
                extensions={"dropbear_request_id": identity["request_id"]},
            ),
            identity,
        )

    async def resolve_request(self, *, deployment_id, robot_slot, request_id, sequence, episode_id):
        """Close only unadmitted work; running work stays pending. Never replay inference."""
        identity = _resolution_identity(deployment_id, robot_slot, request_id, sequence, episode_id)
        return _resolution(
            await self._http.post(
                f"/v1/actions/{identity['request_id']}/resolve",
                json=identity,
                extensions={"dropbear_request_id": identity["request_id"]},
            ),
            identity,
        )

    async def create_deployment(
        self,
        *,
        idempotency_key,
        warm_robots=8,
        max_robots=64,
        robots_per_replica=8,
        model=_DEFAULT_MODEL,
    ):
        body = _creation(idempotency_key, warm_robots, max_robots, robots_per_replica, model)
        return _decode(
            await self._http.post(
                "/v1/inference/deployments",
                headers={"Idempotency-Key": idempotency_key},
                json=body,
            )
        )

    async def deployment(self, deployment_id):
        return _decode(
            await self._http.get(f"/v1/inference/deployments/{_deployment_id(deployment_id)}")
        )

    async def warm(self, deployment_id, robots):
        return _decode(
            await self._http.patch(
                f"/v1/inference/deployments/{_deployment_id(deployment_id)}",
                json={"warm_robots": _capacity(robots)},
            )
        )

    async def stop(self, deployment_id):
        return _decode(
            await self._http.delete(f"/v1/inference/deployments/{_deployment_id(deployment_id)}")
        )

    async def close(self):
        await self._http.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.close()
