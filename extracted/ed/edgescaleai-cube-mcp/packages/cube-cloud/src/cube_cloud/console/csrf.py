"""CSRF token derivation for console mutations (docs/console-spec.md §4.2).

The token is `HMAC-SHA256(csrf_secret, key_id)`, where `key_id` is the stored API
key hash already on `request.state` — non-reversible, per-session, and never sent
to the browser itself. Stateless on purpose: there is no server-side token store
to share across ECS tasks, so any task can mint and verify.

`verify()` is the gate on the console's one mutating route
(`routes.py::guard_write`, `POST /console/api/cubes/{cube}/unexpose`) and fails
closed — a `None` secret yields a `None` token and a False verification, so a stack
that never provisioned the secret cannot mutate at all. Reads do not use it.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from cube_cloud.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _secret() -> str | None:
    """Read the console CSRF secret from Secrets Manager (cached per process).

    Note the cache also memoizes a None result, so a failed read is not retried
    on every page load. The trade-off is that a task which starts before the
    secret exists stays token-less for its lifetime; ECS recycles tasks, and the
    alternative — an AWS call per request — is worse on a read path.

    Returns None — rather than raising — when the secret is absent or malformed,
    so a missing secret degrades the console to "no token minted" instead of
    500ing the whole UI. Callers must treat None as fatal for *verification*
    (fail closed); it is merely a warning for minting.

    Secret value is JSON: `{"secret": "<random string>"}`.
    """
    # The resolved Secrets Manager identifier is deliberately NEVER logged below.
    #
    # It is only a resource name ("cube-mcp-dev/console/csrf-secret"), so logging
    # it would be safe — but CodeQL's py/clear-text-logging-sensitive-data taints
    # everything flowing out of `settings.console_csrf_secret` (it classifies by
    # the config field name, not by the local's name, so renaming the local does
    # not help). Echoing it would mean a standing high-severity alert on every PR
    # that touches this file, for no real benefit.
    #
    # The diagnostic value is preserved by naming the ENV VAR in the messages
    # instead — a static string, and better guidance anyway, since it tells an
    # operator exactly which setting to inspect rather than echoing a value they
    # would then have to trace back to its source.
    ref = settings.console_csrf_secret
    if not ref:
        logger.error(
            "CUBE_CLOUD_CONSOLE_CSRF_SECRET is not set — mutating console routes "
            "will fail closed. Terraform sets it on ECS; set it explicitly for any "
            "other runtime."
        )
        return None

    # Fetch and parse are split so the broad catch covers only the AWS call, where
    # no secret value exists yet (the call failed) and the error text is safe and
    # diagnostically useful.
    try:
        client = boto3.client("secretsmanager", region_name=settings.aws_region)
        resp = client.get_secret_value(SecretId=ref)
    except Exception as e:  # noqa: BLE001 - this must never raise; see below
        # Broad on purpose. The contract here is "return None, never raise",
        # because this runs on the read path that renders the console: an
        # exception would 500 the session endpoint and blank the whole UI over a
        # secret that only *mutations* need.
        #
        # `ClientError` alone is not enough — botocore raises several errors that
        # are not ClientError subclasses (NoCredentialsError, NoRegionError,
        # EndpointConnectionError, MissingDependencyException), and client
        # construction itself can throw. A missing-credentials failure taking down
        # the console was a real bug found by running this locally.
        logger.error(
            "console CSRF secret unavailable (%s: %s) — check "
            "CUBE_CLOUD_CONSOLE_CSRF_SECRET and the task role's secretsmanager "
            "grant; mutating console routes will fail closed until it resolves",
            type(e).__name__, e,
        )
        return None

    # Parsing is caught separately and logs the exception TYPE ONLY, never its
    # message. A decode failure here means the fetched SecretString was malformed
    # — and that string is the secret material, so anything derived from it (a
    # JSONDecodeError's document, a KeyError's key) must stay out of the log.
    try:
        value = json.loads(resp["SecretString"]).get("secret")
    except Exception as e:  # noqa: BLE001 - same never-raise contract
        logger.error(
            "console CSRF secret is malformed (%s) — the value at "
            "CUBE_CLOUD_CONSOLE_CSRF_SECRET must be JSON of the form "
            '{"secret": "<random>"}; mutating console routes will fail closed',
            type(e).__name__,
        )
        return None

    if not value:
        logger.error(
            "console CSRF secret has no 'secret' field — check the value at "
            "CUBE_CLOUD_CONSOLE_CSRF_SECRET; mutating console routes will fail closed"
        )
        return None
    return value


def issue(key_id: str) -> str | None:
    """Mint the CSRF token for a session, or None if the secret is unavailable."""
    secret = _secret()
    if not secret or not key_id:
        return None
    return hmac.new(secret.encode(), key_id.encode(), hashlib.sha256).hexdigest()


def verify(key_id: str, presented: str | None) -> bool:
    """Constant-time check of a presented token. Fails closed on anything missing.

    Not yet called — the Phase 4 mutation routes are its only consumers. Kept
    here with `issue` so the two derivations can never drift apart.
    """
    if not presented:
        return False
    expected = issue(key_id)
    if not expected:
        return False
    # Compare BYTES, not str: `hmac.compare_digest` refuses str operands holding
    # non-ASCII, and Starlette decodes headers as latin-1 — so a single 0xE1 byte
    # in the X-Console-CSRF header would raise TypeError and turn a 403 into an
    # unhandled 500 once the Phase 4 mutation routes call this.
    try:
        return hmac.compare_digest(expected.encode("utf-8"), presented.encode("utf-8"))
    except (UnicodeEncodeError, TypeError):
        return False
