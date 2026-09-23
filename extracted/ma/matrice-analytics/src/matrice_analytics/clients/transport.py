"""GET a platform route on an authenticated session, and say what went wrong.

This module owns the *call*: which base URL to try, in what order, and how to turn a
reply that never arrived into a named failure. Reading a reply that *did* arrive is
:mod:`.response`'s job, and the two are separate because they fail for different
reasons -- a call fails because of the network, a route or a credential, an envelope
fails because the producer said so.

**Everything here raises :class:`~.response.CallFailure` and nothing else.** This
package is an import leaf: it may import ``matrice_common`` and the standard library,
never ``matrice_analytics.runtime``. ``AppBundleError`` lives in ``runtime`` and is
therefore unreachable from here by design, so a caller in ``runtime`` that needs its
own exception type translates at its own boundary rather than reaching across.

The session itself is not opened here -- see :mod:`.bootstrap`. A session arrives as an
argument, which is what makes every function in this module testable with a stub that
has a ``rpc`` attribute and nothing else.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Mapping, Optional

from .response import CallFailure

logger = logging.getLogger(__name__)

#: Overrides the derived backend address. Set it when a deployment's backend is not where
#: the ``ENV`` stage name would put it.
ENV_API_BASE = "MATRICE_APP_BUNDLE_API_BASE"

#: Route prefixes the local gateway serves from an **on-prem** service instead of proxying to the
#: cloud (``location /v1/inference -> api_inference``). For these the session's own base URL is the
#: authority, and :func:`backend_base_url` is not a fallback but a wrong answer -- see
#: :func:`_bases_for`.
LOCAL_AUTHORITY_PREFIXES = ("/v1/inference/",)


def backend_base_url(env: Optional[Mapping[str, str]] = None) -> str:
    """The backend's own address, for a route the session's base URL will not serve.

    Deployments set ``MATRICE_BASE_URL`` to a local gateway (``http://localhost``). That gateway
    proxies the route prefixes it knows -- ``/v1/inference/*`` among them, which is why
    ``PostProcessingConfigClient`` has always worked -- and 302s anything else out to the real
    backend. ``matrice_common``'s client has ``follow_redirects=True``, and httpx drops the
    ``Authorization`` header when a redirect crosses origin, so a redirected call arrives
    unauthenticated and be-application answers 404. Observed in production on 0.1.428:
    ``http://localhost/v1/applications/.../usecase/download`` -> 302 -> prod -> 404, while the same
    path with a direct base URL returns 200.

    Derived the same way ``matrice_common`` derives its own default, so an on-prem or non-prod
    deployment still lands on its own backend; ``$MATRICE_APP_BUNDLE_API_BASE`` overrides it.
    """
    environ = os.environ if env is None else env
    explicit = (environ.get(ENV_API_BASE) or "").strip()
    if explicit:
        return explicit.rstrip("/")
    stage = ((environ.get("ENV") or "").strip() or "prod").lower()
    return f"https://{stage}.backend.app.matrice.ai"


def _bases_for(path: str, env: Optional[Mapping[str, str]] = None) -> tuple:
    """The base URLs worth trying for ``path``, in order.

    Two bases for a **cloud-only** route, because the local gateway 302s those out and httpx drops
    the ``Authorization`` header across the origin change -- the case :func:`backend_base_url`
    exists for.

    One base for a route in :data:`LOCAL_AUTHORITY_PREFIXES`, because retrying those against the
    cloud is not a fallback, it is a category error, and an expensive one (ANLY-15):

    * The gateway proxies ``/v1/inference/*`` to the on-prem ``api_inference``. That service, not
      the cloud, owns the answer -- on an ``accessScale: "local"`` deployment the document exists
      in the on-prem mongo and *nowhere else*, so the cloud has nothing to return even in
      principle.
    * The retry cannot authenticate anyway. Tokens are minted against ``$MATRICE_BASE_URL``
      (``token_auth.py`` ``VALIDATE_ACCESS_KEY_URL`` / ``REFRESH_TOKEN_URL``), i.e. the local
      gateway's ``api_user``, so a direct-to-cloud call presents a JWT that the cloud never issued
      and is refused ``401 Invalid authentication token``. Going direct also bypasses the
      gateway's ``cloud_egress`` listener, which is the *only* sanctioned crossing: it strips
      ``Authorization`` and substitutes the deployment's ``X-License-Key``. This module already
      does the crossing correctly for the one route that needs it -- see ``_mint_via_license``.
    * ``rpc``'s 401 handler then re-mints (against the gateway, successfully) and retries into the
      same refusal, so each attempt costs two cloud round trips plus a re-auth, logs a full error
      block, and cannot ever succeed.
    """
    if path.startswith(LOCAL_AUTHORITY_PREFIXES):
        return (None,)
    return (None, backend_base_url(env))


def _describe(response: Any) -> str:
    """Say something useful about a failed response, including one that is not ours at all.

    ``message`` is absent whenever the body did not come from the platform -- an edge proxy
    returning its own error page, for instance. Reporting ``None`` in that case sends whoever reads
    the log hunting for a bug in the API call rather than in the network path, so name the shape.
    """
    if not isinstance(response, dict):
        return f"non-dict response {type(response).__name__}: {str(response)[:120]}"
    for key in ("message", "detail", "title", "error_name"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return f"{key}={value.strip()[:160]!r}"
    return f"no message; response keys were {sorted(response)[:12]}"


def _rpc(session: Any) -> Any:
    """The authenticated RPC off a session, or a named error.

    ``session.rpc`` is the same handle ``PostProcessingConfigClient`` uses, already signed with the
    container's access keys -- nothing here builds its own auth.
    """
    try:
        return session.rpc
    except Exception as exc:  # pragma: no cover - a session whose rpc property raises
        raise CallFailure(f"Session has no usable RPC handle: {exc}") from exc


def _rpc_data(
    session: Any,
    path: str,
    *,
    what: str,
    env: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """GET ``path`` on the authenticated session and return ``data`` as a dict.

    Tries the session's own base URL first -- where the gateway does proxy the route, that is one
    call and the right one. Only if that fails does it retry against
    :func:`backend_base_url`, because the most likely reason for the first failure is a
    cross-origin redirect that stripped the auth header rather than anything wrong with the request.
    A locally-owned route gets no such retry; :func:`_bases_for` says why.

    A 404 is deliberately *not* short-circuited here, unlike in the post-processing fetchers: on a
    cloud-only route it is the signature of the redirect having stripped the auth header, which is
    precisely the case the second base exists to rescue.

    A successful envelope whose ``data`` is not an object is **reported, not coerced**. An earlier
    version returned ``{}`` there, which a caller cannot tell apart from a route that genuinely
    answered with no fields -- so a producer changing a payload's shape showed up as every field
    quietly going missing, at the call site rather than here. It is not retried against the second
    base either: the call succeeded, so another base would answer the same way.
    """
    attempts: list[str] = []
    for base in _bases_for(path, env):
        try:
            rpc = _rpc(session)
            response = rpc.get(path) if base is None else rpc.get(path, base_url=base)
        except CallFailure as exc:
            # Recorded rather than re-raised so the final message still names the path. A session
            # with no usable rpc fails the same way twice, which is fine -- the cause is in the list.
            attempts.append(f"{base or 'session base url'}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - every transport error is one failed attempt
            attempts.append(f"{base or 'session base url'}: {type(exc).__name__}: {exc}")
            continue

        if isinstance(response, dict) and response.get("success"):
            if base is not None:
                logger.info(
                    "app bundle: %s served from %s -- the session's base URL did not serve it (%s)",
                    path,
                    base,
                    attempts[0] if attempts else "no detail",
                )
            data = response.get("data")
            if not isinstance(data, dict):
                raise CallFailure(
                    f"GET {path} succeeded while resolving {what}, but its data field was "
                    f"{type(data).__name__}, not an object. The route's payload shape has "
                    f"changed, or this path does not return a single document.",
                    response=response,
                )
            return data
        attempts.append(f"{base or 'session base url'}: {_describe(response)}")

    raise CallFailure(
        f"GET {path} did not succeed while resolving {what}. Tried: " + "; ".join(attempts) + ". "
        "A 404 here usually means the request lost its Authorization header on a redirect out of "
        "the local gateway; a 401/403 means the container's credentials are not accepted on this "
        "route. Set $MATRICE_APP_BUNDLE_API_BASE to the backend that should serve it."
    )
