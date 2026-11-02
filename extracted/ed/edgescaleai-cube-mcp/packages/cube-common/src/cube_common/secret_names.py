"""Which names and values are secret, and the placeholder shown in their place.

One predicate, every renderer. It lives in cube_common rather than in cube-cloud's
`tools/modules.py` (where it was written) because `apollo_models.format_entity_health`
renders entity config and has to mask the same names module variables are masked by:
a Teleport agent's `authToken` is the same credential whether it reaches tool output
as a module variable or inside the entity config that module rendered.
`tools/modules.py` re-exports these under their original private names.
"""

from __future__ import annotations

import json
import re

# Names whose VALUES are never printed. `expose`/`unexpose` mint a fresh Teleport
# join token and pass it as `authToken`, and tool output that listed it verbatim
# emitted it into (a) the MCP tool response and its agent transcript, (b) the S3
# telemetry archive, and (c) the console's unexpose response, i.e. the browser.
#
# Matched on the NAME, not by scanning the rendered text for secret-shaped
# strings: a name test is decidable and fails toward masking, whereas a regex
# over prose is the redaction approach this repo deliberately avoids.
SECRET_NAME_HINTS = (
    # Credentials by any common spelling.
    "token", "secret", "password", "passwd", "pwd", "credential", "creds",
    "apikey", "api_key", "key", "privatekey", "jwt", "bearer", "pw",
    # Material that IS a credential in encoded form.
    "pem", "sasl",
    # Connection strings embed `user:pass@host`, so the whole value is sensitive
    # even though the name says nothing about secrets.
    "dsn", "connectionstring", "databaseurl", "dburl",
)

# Names that MATCH a hint above but whose values are not secret. Needed because the
# hints are substrings: `key` catches `keyspace` and `publicKey`, and `token` catches
# `maxTokens` — plausible here, since litellm runs on this fleet. `maxNumBatchedTokens`
# is vLLM's, in the AI tab's catalog, which refuses secret-named keys by this rule.
#
# Over-masking is not silent (the write paths refuse a masked placeholder rather
# than storing it), but it still costs an operator a real value they cannot read back,
# so precision is worth having in both directions. Matched on the FULL lowercased name,
# not a substring, so this list can never accidentally unmask something.
NEVER_SECRET_NAMES = frozenset({
    "maxtokens", "maxtoken", "maxnumbatchedtokens", "tokenttl", "tokenurl", "tokenendpoint",
    "keyspace", "keyname", "publickey", "keycloakurl", "keystoneurl",
    "apikeyname", "sshkeypath", "secretname", "secretkeyref", "credentialmode",
})

# A URL carrying userinfo — `scheme://user:pass@host` — is entirely sensitive no matter
# what it is called. Name matching cannot enumerate every service that does this
# (`redisUrl`, `amqpUrl`, `mongoUri`, ...), so this is checked on the VALUE.
#
# This is a structural check for a specific URL grammar, not a scan of free text for
# secret-shaped strings — the approach AGENTS.md rules out. It answers "does this value
# contain credentials by construction", which a name never can.
#
# The USER part excludes `:`, and that is what keeps this linear. With `:` allowed on
# both sides of the split, `a://!:!:…` with no `@` is retried at every colon —
# quadratic (~3s on 64 KB, CodeQL py/polynomial-redos). The input is caller-chosen
# text on the event loop: module-variable values in tool output
# (`modules._display_variable`) and in the telemetry archive (`telemetry/redaction.py`,
# the `variables` argument only), and every value of an entity's config
# (`entity_config.mask_secrets`), which a caller wrote. It is also the RFC 3986
# reading: the first colon in userinfo ends the user, so a password containing `:`
# still matches. The user part may be EMPTY (`*`, not `+`): `redis://:password@host`
# is the normal Redis form, since Redis has no username before ACLs, and `+` printed
# that password verbatim. A class that excludes `:` still has one split point
# whether it is `*` or `+`, so this stays linear.
URL_WITH_USERINFO_RE = re.compile(r"^[a-z][a-z0-9+.-]*://[^/\s@:]*:[^/\s@]+@", re.I)

# The exact shape `mask` emits. Shared so the write-path guards recognize precisely
# what the read path produced — not a lookalike regex.
MASK_RE = re.compile(r"^<hidden, \d+ chars>$")


def is_secret_name(name: str) -> bool:
    lowered = (name or "").lower()
    if lowered in NEVER_SECRET_NAMES:
        return False
    return any(hint in lowered for hint in SECRET_NAME_HINTS)


def value_is_sensitive(value: object) -> bool:
    """True when the VALUE is credential-bearing regardless of its name."""
    return isinstance(value, str) and bool(URL_WITH_USERINFO_RE.match(value.strip()))


def mask(value: object) -> str:
    """The placeholder shown instead of a secret value.

    The length is reported so an operator can still tell "it was set" from "it was
    set to the empty string", which is the only diagnostic the value provided here.
    """
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return f"<hidden, {len(text)} chars>"


def is_masked_placeholder(value: object) -> bool:
    return isinstance(value, str) and bool(MASK_RE.match(value.strip()))
