"""Mutations behind the console's JSON API (docs/console-spec.md §4.2, §4.4b).

Separate from `reads.py` on purpose. That module is the read layer and nothing in
it mutates; keeping the mutating operations out of it means "does this file
change cube state" is answerable by filename rather than by audit.

**Three rules govern the cube-mutating half of this module** (`expose_app`,
`unexpose_app`). `submit_feedback` below is deliberately exempt from all three —
it touches no cube, no Apollo, and no tenancy boundary, so there is no state to
verify structurally and no company-scoped write path to reuse-rather-than-
reimplement. It calls straight into `tools/feedback.py` and lets `FeedbackError`
propagate to the route.

1. **Reuse the tool's write path, never reimplement it.** `tools/expose.py::unexpose`
   holds the company-scoping rule, the non-enumerable "does not exist or you do not
   have permission" response, the read-merge-resend against Apollo's full-replace
   update, and the teardown of the module once no apps remain. Reimplementing any
   of that here would fork a tenancy boundary — the specific mistake AGENTS.md
   warns about. This module resolves authorization, calls the tool, and verifies.

2. **Verify the outcome structurally, not by reading the tool's message.** The tool
   returns operator-facing prose. Rather than pattern-matching it, the module's
   `apps` variable is re-read afterward and success is "the app is no longer there".
   That also produces the fresh list the UI needs, so a successful unexpose costs
   the client no follow-up request.

3. **Authorization is inherent, as in `reads.py`.** The cube is resolved out of
   `_visible_environments`, which is already RBAC-filtered, so a cube the caller
   holds no Apollo role on is simply not found. There is no separate access check
   at this layer for a future edit to forget or reorder — and the expensive write
   is never attempted for a cube the caller cannot see.
"""

from __future__ import annotations

import asyncio
import logging

from cube_common.apollo_client import ApolloClient
from cube_cloud.auth.app_companies import app_companies, reads_stored_sets
from cube_cloud.console import reads

logger = logging.getLogger(__name__)

# A refusal the caller is allowed to see. Deliberately identical whether the app
# never existed or belongs to another company — the same non-enumerability rule the
# `unexpose` tool enforces, restated here because this layer chooses the wording.
NOT_FOUND_MESSAGE = (
    "That app is not exposed on this cube, or you do not have permission to manage it."
)

# Distinct from NOT_FOUND_MESSAGE on purpose: "we could not read the state" needs a
# different response from an operator than "that app is not yours", and conflating
# them is what let a failed read look like a successful removal.
# The console authorized one environment and the tool would act on another. Refusing
# is the only safe answer — acting would remove an app from, or publish one to, a cube
# the operator did not choose.
AMBIGUOUS_CUBE_MESSAGE = (
    "This cube's name is ambiguous — it resolves to a different environment than the "
    "one you are viewing, so nothing was changed. Use the expose and unexpose tools "
    "with an unambiguous name or RID."
)

# Expose refuses a URI the console did not itself enumerate. `expose` accepts any
# `app_uri` from an MCP caller, but the console is an enumerated-args surface
# (AGENTS.md console rule 2): only what `cube_services` offered can be published, so a
# crafted body cannot point a public hostname at an arbitrary in-cluster address.
UNKNOWN_URI_MESSAGE = (
    "That target is not one of this cube's discovered services, so nothing was "
    "changed. Reload the expose options and pick a listed port."
)

# The qualified name already serves something. `expose`'s upsert would REPOINT that
# public URL in place, which is a different and more surprising act than publishing
# something new, so the console makes the caller say so.
ALREADY_EXPOSED_MESSAGE = (
    "An app is already exposed under that name on this cube. Re-exposing would "
    "repoint its public URL. Unexpose it first, or choose a different name."
)

# Same collision, but the app belongs to a company this caller cannot see, so
# "unexpose it first" would be advice they cannot act on. Says the name is taken and
# nothing else — not the owner, the URI, or the public address.
NAME_TAKEN_MESSAGE = (
    "That name is already in use on this cube. Choose a different name."
)

# The caller named an app company its profile does not hold. The console only ever
# offers held companies, so this is a stale page or a hand-built request.
COMPANY_NOT_HELD_MESSAGE = (
    "You can't share apps with that company from this account, so nothing was changed."
)

UNREADABLE_MESSAGE = (
    "Could not read this cube's exposed apps, so nothing was changed. The Teleport "
    "module's app list may be unreadable — check it with the list_exposed tool."
)


# How long to keep re-reading before reporting the removal as merely *pending*.
# Three reads about a second apart: enough to absorb Apollo's read-after-write lag
# without making the request feel hung.
_CONFIRM_ATTEMPTS = 3
_CONFIRM_DELAY_SECONDS = 1.0
# Attempt 0 reads immediately, so only ATTEMPTS-1 sleeps actually elapse. The
# audit line quotes this, and quoting 3.0s for a 2.0s wait is a small lie in
# the one record an operator uses to reconstruct what happened.
_CONFIRM_BUDGET_SECONDS = (_CONFIRM_ATTEMPTS - 1) * _CONFIRM_DELAY_SECONDS


# Line labels whose value is a list of every app on the shared Teleport module —
# i.e. other companies' inventory. `expose` emits the first; matched case-insensitively
# on the label because the payload is prose rather than an assignment. Extend this
# when a tool grows another such line.
_CROSS_TENANT_LINE_PREFIXES = ("apps on this module:",)


def _loggable(detail: str) -> str:
    """Strip the cross-tenant payload out of a tool's operator-facing message.

    Withholding the prose from the browser and then logging it whole was
    self-defeating: `unexpose` rewrites the shared module's full `apps` list and its
    message quotes that list — every app on the cube, including other companies',
    with URIs and public addresses. A `lear-dev` click put conagra's inventory in
    CloudWatch at INFO. `_display_variable` masks `authToken` by NAME; `apps` is not
    a secret name, so it was never covered.

    The console's sibling read already logs `type(e).__name__` only for exactly this
    reason (AGENTS.md console rule 3). This keeps the operator-useful lines — the
    outcome, the module RID, the rollout state — and drops any line carrying the
    variable payload.

    **`expose` leaks the same inventory through a line that has no `=`.** Its message
    ends with `  Apps on this module: <every name on the cube>`, so the
    assignment-shaped rule above kept it verbatim — the defect this function exists to
    prevent, reintroduced by the other tool's phrasing. Line prefixes that carry a
    cross-tenant list are therefore dropped by name as well. Both rules are
    allowlist-shaped in the safe direction: an unrecognized line is kept only if it
    looks like neither.
    """
    kept: list[str] = []
    for line in (detail or "").splitlines():
        stripped = line.strip()
        # Lines whose CONTENT is a list of every app on the shared module. Matched on
        # the label because the payload is prose, not an assignment.
        if stripped.lower().startswith(_CROSS_TENANT_LINE_PREFIXES):
            head = stripped.split(":", 1)[0].strip()
            kept.append(f"{head}: <omitted>")
            continue
        # Any line assigning a variable value is dropped wholesale. `apps = [...]` is
        # the cross-tenant one; the others are masked already but carry no signal.
        if "=" in stripped and not stripped.startswith(("RID:", "State:")):
            head = stripped.split("=", 1)[0].strip()
            if head and " " not in head:
                kept.append(f"{head} = <omitted>")
                continue
        kept.append(line)
    return "\n".join(kept)


# `expose` returns a STRING for failures that happen before it submits anything to
# Apollo, so an unconfirmed result can mean either "the write is still landing" or
# "no write was ever issued". These are the tool's pre-write bail-outs, in its own
# words: tbot unavailable, the company-scoping refusal, `_resolve_environment`
# raising, an unminted join token, and an unreadable `apps` variable.
_TOOL_PRE_WRITE_REFUSALS = (
    "tbot credentials not ready",
    "expose refused:",
    "expose failed:",
    "unexpose refused:",
    "unexpose failed:",
    "error: apps variable",
)

# The tool's success preamble. Present only once the module write has been SUBMITTED
# — `update_module_variables`' own error string is appended after it — so its presence
# means a write was attempted regardless of what follows.
_TOOL_WROTE_PREFIX = "exposed '"

# Shown when the tool refused outright. The refusals are infrastructure conditions
# (tbot, Apollo, a corrupt module variable), none of which an operator can fix from
# this form, and the tool's own words are withheld for the usual tenancy reason.
TOOL_REFUSED_MESSAGE = (
    "The cube refused the change, so nothing was published. Try again in a moment; "
    "if it persists, an admin can see why with the expose tool."
)
TOOL_UNEXPOSE_REFUSED_MESSAGE = (
    "The cube refused the change, so nothing was removed. Try again in a moment; "
    "if it persists, an admin can see why with the unexpose tool."
)


def _refused_before_writing(detail: str) -> bool:
    """True when the tool's message shows it bailed out before submitting a write.

    **This does not violate rule 2.** Success is still decided structurally by
    `_confirm_present` re-reading Apollo; nothing here can turn a failure into a
    success. This runs only on a result already known to be unconfirmed, and only to
    choose between two ways of reporting it.

    **It fails toward `pending`, deliberately.** Both conditions must hold: the message
    matches a known pre-write bail-out AND it does not carry the success preamble. A
    refusal string this list has not caught yet is reported as `pending` — mildly wrong
    but harmless. The opposite default, inferring "nothing was written" from the
    absence of a success preamble, would claim no write happened for one that had, and
    that is the claim an operator acts on.
    """
    text = (detail or "").strip().lower()
    if not text or text.startswith(_TOOL_WROTE_PREFIX):
        return False
    return text.startswith(_TOOL_PRE_WRITE_REFUSALS)


async def _confirm_removed(
    client: ApolloClient, profile: str, env_id: str, app_name: str,
    known: list[dict], company: str | None = None,
) -> tuple[list[dict], bool]:
    """Re-read until the removal shows -> `(latest exposed list, confirmed)`.

    With ``company`` the removal took ONE company off the app, which may stay exposed to
    others: confirmed once the app is gone OR no longer carries that company. Without it
    (an admin removing the whole app) confirmed only once the app is gone.

    **Why this is not a single read.** An earlier version read once, immediately, and
    reported "Apollo did not apply the change" whenever the app was still listed —
    which was wrong twice over. `update_module_variables` submits a change request
    (the module goes to `UpdateRequested`, verified live on `cube-66odzn95`) and
    Apollo offers no read-your-write guarantee, so a sub-second read can miss a write
    that landed. A user then saw a hard failure for an unexpose that had in fact
    succeeded, and the app disappeared moments later.

    Not confirming is therefore reported as **pending**, never as failure. The only
    thing this function can establish is the positive: the app is gone.

    **A FAILED read is not evidence of removal.** `_exposed_apps` flattens every
    failure to `[]`, so reading absence off it treated "the read broke" as "the app is
    gone" — and reported `applied`, with an empty `exposed` list that made the client
    clear every row on the cube, for a write that was never issued. Concretely: a
    corrupt `apps` variable (real, on `cube-66odzn95`) makes `unexpose` refuse
    *before* mutating AND makes this read fail, so both halves went quiet at once.
    Hence `_exposed_apps_read`, whose boolean separates "empty" from "unknown".
    """
    # Seeded with the pre-write list, so if EVERY confirmation read fails the caller
    # still reports the last state actually observed. Returning `[]` here would make
    # the client clear every row on the cube — the same wrong outcome by a different
    # route than the fail-open bug this function was rewritten to fix.
    latest: list[dict] = list(known)
    for attempt in range(_CONFIRM_ATTEMPTS):
        if attempt:
            await asyncio.sleep(_CONFIRM_DELAY_SECONDS)
        # Unpack into a TEMPORARY. Assigning straight into `latest` overwrote the
        # seeded known-good list with the failed read's `[]` before the check below
        # could reject it — reinstating, by a back door, the empty `exposed` that
        # makes the client clear every row.
        fresh, ok = await reads._exposed_apps_read(client, profile, env_id)
        if not ok:
            # Unknown, not confirmed. Keep the previous known-good list so the client
            # is never handed an empty set it would read as "everything went away".
            logger.warning(
                "console unexpose: exposed-apps read FAILED while confirming %s on "
                "%s — treating as unconfirmed, not as removed", app_name, env_id,
            )
            continue
        latest = fresh
        entry = next((a for a in latest if a["name"] == app_name), None)
        if entry is None or (company is not None and company not in entry.get("companies", [])):
            return latest, True
    return latest, False


def _bare_app_name(qualified: str, cube: str) -> tuple[str, str]:
    """Recover the bare app name `unexpose` expects -> `(bare, error)`.

    `expose` stores `<app>-<env>`; `unexpose` re-derives that from a BARE name, so
    the console has to hand back what was originally passed in, not what is stored.

    The round trip is **verified rather than assumed**: the recovered name is
    re-qualified through the tool's own `_qualified_app_name` and must reproduce the
    stored name exactly. If it does not, the stored name is not the qualified form
    at all — which happens when an app was exposed with an explicit `public_addr` —
    and this refuses instead of guessing, because a near-miss here unexposes the
    wrong app or silently does nothing. `expose`'s own `_sanitize_label` runs on both
    halves, so the verification also catches any name whose characters do not
    survive that.
    """
    from cube_cloud.tools import expose as expose_tool

    # The stored name was built from `_sanitize_label(env)`, which LOWERCASES. Slicing
    # with the raw Apollo name refused every app on a cube whose name carries
    # uppercase (`Lear-Hammond-2` stores `sqlpad-lear-hammond-2`) — and since `expose`
    # lowercases both halves, the console could publish an app there and then never
    # remove it, telling the operator it "is not named for this cube". Sanitizing here
    # matches how the suffix was actually produced; the round-trip below still
    # verifies the result rather than trusting this.
    suffix = f"-{expose_tool._sanitize_label(cube)}"
    if not qualified.endswith(suffix) or len(qualified) <= len(suffix):
        return "", (
            f"'{qualified}' is not named for this cube, so the console cannot work "
            "out which app to remove. Use the unexpose tool directly."
        )
    bare = qualified[: -len(suffix)]
    round_tripped, err = expose_tool._qualified_app_name(bare, cube)
    if err or round_tripped != qualified:
        return "", (
            f"'{qualified}' does not round-trip to a bare app name, so the console "
            "cannot remove it safely. Use the unexpose tool directly."
        )
    return bare, ""


async def expose_app(
    client: ApolloClient, profile: str, cube: str, app_name: str, app_uri: str,
    rewrite_host: str = "", rewrite_origin: str = "", company: str | None = None,
) -> dict | None:
    """Publish one in-cluster service through Teleport.

    Returns `None` when the caller cannot see the cube — the same non-enumerable 404
    the reads give. Otherwise the same shape as `unexpose_app`: `ok`, `state`
    (`applied` | `pending` | `refused`), `error` when refused, and `exposed`.

    **Three validations before anything is written**, all of them producing an inline
    message rather than a tool refusal the operator has to interpret:

    1. `app_name` must qualify. `expose` derives `<app>-<env>` and refuses a name that
       sanitizes to nothing or overflows the 63-char DNS label; checking here means the
       operator sees why while the form is still in front of them.
    2. `app_uri` must be one of the URIs `cube_services` enumerated for this cube. See
       `UNKNOWN_URI_MESSAGE` — this is the difference between an enumerated-args
       surface and a thin proxy for the tool. ONE exception: a join onto an app the
       caller can see, where `app_uri` is verified to equal that app's own stored
       target (`reads._same_target`), so nothing new is published.
    3. The qualified name must not already be serving something, because `expose`'s
       upsert silently REPOINTS an existing public URL -- except a JOIN on a `stored`
       stack: same target, no rewrite, adding a named company the app lacks.

    The expose picker PREDICTS this guard's outcomes, with `expose._plan_labels`', before
    the click (`console/web/src/CubePage.tsx::existingAppHint`): the rewrite, "must add a
    company" and see-it-or-probe rules here are its branches too. Change it with them; no
    test spans the two languages.

    Unlike `unexpose`, this is additive: it cannot remove another app's route. It does
    make something publicly reachable, which is what the UI's confirmation says.
    """
    from cube_cloud.tools import clusters as clusters_tool
    from cube_cloud.tools import expose as expose_tool

    envs, envs_truncated = await reads._visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console expose target cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED (OI-6 / issue 252).",
                cube, profile,
            )
        return None

    env_id = match.get("id") or ""

    # 1. Name has to survive the tool's own qualification.
    qualified, qual_err = expose_tool._qualified_app_name(app_name, cube)
    if qual_err or not qualified:
        logger.info("console expose refused on %s: %s", cube, qual_err)
        return {"ok": False, "state": "refused",
                "error": qual_err or "That app name cannot be used.", "exposed": []}

    # Who the app is exposed TO: a company the caller holds (default its home one).
    # Resolved by the tool's own rule so the two surfaces cannot disagree. Unreadable
    # companies are "could not read", not "not yours": the two need different responses.
    held = app_companies(profile)
    if held is None:
        logger.error("console expose refused on %s for profile=%s: its app companies are "
                     "unreadable", cube, profile)
        return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE, "exposed": []}
    target, company_err = expose_tool._resolve_company(profile, company)
    if company_err or not target:
        logger.info("console expose refused on %s for profile=%s: company %r not held",
                    cube, profile, company)
        return {"ok": False, "state": "refused", "error": COMPANY_NOT_HELD_MESSAGE,
                "exposed": []}

    # The company the result must carry. An admin naming none on an EXISTING app is
    # reconfiguring (`expose` keeps its label verbatim), so there is no company to wait
    # for: confirm on presence. Waiting for DEFAULT_COMPANY reported `pending` forever
    # after a write that had landed.
    # "" names no company, exactly as the tool reads it (`company or None`).
    confirm_company = None if (held.unscoped and not company) else target

    before, before_ok = await reads._exposed_apps_read(client, profile, env_id)
    if not before_ok:
        logger.error(
            "console expose refused on %s for profile=%s: the exposed-apps read "
            "failed, so a name collision cannot be ruled out", cube, profile,
        )
        return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                "exposed": []}

    # 3. Never repoint an existing public URL implicitly — INCLUDING one the caller
    # is not allowed to see. `_merge_app` upserts by name with no regard for
    # `labels.company`. The `expose` tool refuses a SCOPED caller that would overwrite an
    # app it cannot see, but on a `stored` stack lets any company on an app reconfigure it,
    # and never refuses an unscoped admin; this guard
    # also refuses a caller's OWN existing name (repointing its own URL must be
    # deliberate here), so both stay. Reading the company-filtered
    # `before` here made the guard blind in exactly the cross-tenant case that
    # motivates it. See `reads._exposed_names_read`.
    taken, taken_ok = await reads._exposed_names_read(client, env_id)
    if not taken_ok:
        logger.error(
            "console expose refused on %s for profile=%s: the exposed-names read "
            "failed, so a name collision cannot be ruled out", cube, profile,
        )
        return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                "exposed": before}
    own_target_join = probe_target_after_allowlist = False
    if qualified in taken:
        # On a "stored" stack an app already exposed at the SAME target can be JOINED:
        # the tool adds the caller's company and changes nothing else, so no URL is
        # repointed (`expose._plan_labels`). Anything else -- another target, or a
        # rewrite that would reconfigure it -- is still refused here.
        # A join must ADD a company. Re-exposing to a company already on the app (a retry,
        # a double submit, or an admin naming none) changes nothing, yet the tool would
        # still mint a token and roll the cube's app-service for every app on it.
        existing = next((a for a in before if a["name"] == qualified), None)
        adds = (confirm_company is not None
                and confirm_company not in ((existing or {}).get("companies") or []))
        joinable = False
        if reads_stored_sets() and adds and not (rewrite_host or rewrite_origin):
            if existing is not None and existing.get("reachable"):
                # An app the caller can SEE (the Visibility control): a join reuses its
                # own stored target, so it needs no allowlist -- which a target outside
                # the service picker (https://, an infra namespace, a hand-written URI
                # from the MCP tool) could never pass.
                same, same_ok = await reads._same_target(client, env_id, qualified, app_uri)
                if not same_ok:
                    return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                            "exposed": before}
                joinable = own_target_join = same
            else:
                # One it CANNOT see: its target is probed only with a URI this console
                # enumerated, i.e. after the allowlist below, so a failed guess cannot
                # confirm a target the picker never offers.
                joinable = probe_target_after_allowlist = True
        if not joinable:
            # Which message depends on whether the caller can REACH the app — telling
            # someone to "unexpose it first" for an app they cannot manage is a dead
            # end. Both admit the name is in use, which is a narrow existence oracle for
            # a name the caller supplied; neither reveals the owner, the URI, or the
            # address. That trade is deliberate: the alternative is repointing a live URL.
            mine = qualified in {a["name"] for a in before if a.get("reachable")}
            return {"ok": False, "state": "refused",
                    "error": ALREADY_EXPOSED_MESSAGE if mine else NAME_TAKEN_MESSAGE,
                    "exposed": before}

    # The tool must resolve `cube` to the SAME environment this request was
    # authorized against — the guard `unexpose_app` has and this path was missing.
    # The console matched `cube` case-SENSITIVELY against a cached RBAC-filtered list;
    # `_resolve_environment` is case-INSENSITIVE and takes Apollo's first match. With
    # two spellings present, `fetch_services` enumerates one cube's services and
    # `expose` publishes to it, while `_confirm_present` polls the other: the app
    # lands on a cube the operator was not looking at and the response is `pending`
    # forever. It also re-opens the collision guard above, which ran against this
    # cube's names. Checked BEFORE `fetch_services` so the URI allowlist is
    # enumerated from an environment we have verified.
    try:
        tool_env = await expose_tool._resolve_environment(client, cube)
    except Exception as e:
        logger.error(
            "console expose refused on %s: could not confirm the tool resolves the "
            "same environment (%s)", cube, type(e).__name__,
        )
        return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                "exposed": before}
    if (tool_env or {}).get("id") != env_id:
        logger.error(
            "console expose REFUSED on %s for profile=%s: the tool resolves that "
            "name to environment %s but this request was authorized against %s",
            cube, profile, (tool_env or {}).get("id"), env_id,
        )
        return {"ok": False, "state": "refused", "error": AMBIGUOUS_CUBE_MESSAGE,
                "exposed": before}

    # 2. The target must be one this console enumerated -- unless this is a join onto an
    # app the caller can see, at that app's own stored target (verified above).
    if not own_target_join:
        refusal = await _check_enumerated_target(client, cube, profile, app_uri, before)
        if refusal is not None:
            return refusal
    if probe_target_after_allowlist:
        same, same_ok = await reads._same_target(client, env_id, qualified, app_uri)
        if not same_ok:
            return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                    "exposed": before}
        if not same:
            return {"ok": False, "state": "refused", "error": NAME_TAKEN_MESSAGE,
                    "exposed": before}

    return await _expose_checked(client, profile, cube, env_id, app_name, qualified, app_uri,
                                 rewrite_host, rewrite_origin, company, confirm_company, before)


async def _check_enumerated_target(client, cube: str, profile: str, app_uri: str,
                                   before: list[dict]) -> dict | None:
    """Refusal unless ``app_uri`` is one this console enumerated (console rule 2)."""
    from cube_cloud.tools import clusters as clusters_tool

    services, _env_name, _hidden, svc_err = await clusters_tool.fetch_services(
        client, cube, None, profile
    )
    if svc_err:
        # NOT logged. `fetch_services` composes `error` for an MCP operator and embeds
        # the ApolloError text (the raw GraphQL body of a query that selected every
        # module's variable values) or raw kubectl stderr — the `list_services` tool
        # may show that, CloudWatch may not. Same containment `reads.cube_services`
        # applies on the read side.
        logger.warning(
            "console expose refused on %s for profile=%s: the services read failed "
            "— detail withheld; reproduce with the list_services tool.", cube, profile,
        )
        return {"ok": False, "state": "refused",
                "error": "Could not read this cube's services, so nothing was "
                         "changed. Try again in a moment.",
                "exposed": before}
    # Built through the SAME serializer the picker was populated from, so the accepted
    # set cannot drift from the offered one. Filtering inline here instead let the two
    # diverge: `_service_candidate` also drops a port with no number, which this did
    # not, so a URI the console never offered was nonetheless acceptable.
    # Both schemes the picker can offer, from the SAME serializer that populated
    # it, so the accepted set cannot drift from the offered one.
    known_uris = {
        uri
        for svc in services
        for p in reads._service_candidate(svc)["ports"]
        for uri in (p["app_uri"], p.get("app_uri_tcp"))
        if uri
    }
    if app_uri not in known_uris:
        logger.warning(
            "console expose refused on %s for profile=%s: target %r is not among the "
            "%d discovered service URIs", cube, profile, app_uri, len(known_uris),
        )
        return {"ok": False, "state": "refused", "error": UNKNOWN_URI_MESSAGE,
                "exposed": before}
    return None


async def _expose_checked(
    client: ApolloClient, profile: str, cube: str, env_id: str, app_name: str,
    qualified: str, app_uri: str, rewrite_host: str, rewrite_origin: str,
    company: str | None, confirm_company: str | None, before: list[dict],
) -> dict:
    """The write and its confirmation, once every check in `expose_app` has passed."""
    from cube_cloud.tools import expose as expose_tool

    logger.warning(
        "console expose STARTING: profile=%s cube=%s app=%s (qualified=%s) uri=%s",
        profile, cube, app_name, qualified, app_uri,
    )
    # Compose the two named fields into the header list the tool takes. Order is
    # fixed here rather than by the client, and the values are validated by the
    # TOOL's own `_validate_rewrite_headers` (called inside `expose`), not by a
    # second implementation here — the same discipline that has the URI allowlist
    # reuse `reads._service_candidate`.
    #
    # Note which half takes which form: `Host` is a bare host, `Origin` is a full
    # URL with scheme. Getting them backwards fails only on the WebSocket
    # upgrade, long after the page appears to work.
    rewrite_headers: list[str] | None = None
    if rewrite_host or rewrite_origin:
        rewrite_headers = []
        if rewrite_host:
            rewrite_headers.append(f"Host: {rewrite_host}")
        if rewrite_origin:
            rewrite_headers.append(f"Origin: {rewrite_origin}")

    logger.warning(
        "console expose rewrite: cube=%s app=%s headers=%d",
        cube, qualified, len(rewrite_headers or []),
    )
    detail = await expose_tool.expose(
        client, environment=cube, app_name=app_name, app_uri=app_uri, profile=profile,
        rewrite_headers=rewrite_headers, company=company,
    )

    after, ok = await _confirm_present(client, profile, env_id, qualified, before, confirm_company)
    if ok:
        logger.warning(
            "console expose SUCCEEDED: profile=%s cube=%s app=%s", profile, cube, qualified
        )
        logger.info(
            "console expose detail (cube=%s app=%s): %s",
            cube, qualified, _loggable(detail),
        )
        return {"ok": True, "state": "applied", "exposed": after}

    if _refused_before_writing(detail):
        # The tool bailed out before submitting anything to Apollo. Reporting that as
        # `pending` told the UI to poll for an app that will never appear, and since
        # `detail` is deliberately not forwarded, the operator was never told why —
        # a spinner that resolves to nothing.
        logger.error(
            "console expose REFUSED BY THE TOOL before any write: profile=%s cube=%s "
            "app=%s — tool said: %s", profile, cube, qualified, _loggable(detail),
        )
        return {"ok": False, "state": "refused", "error": TOOL_REFUSED_MESSAGE,
                "exposed": after}

    logger.error(
        "console expose NOT CONFIRMED after %.1fs: profile=%s cube=%s app=%s — "
        "tool said: %s", _CONFIRM_BUDGET_SECONDS, profile, cube, qualified,
        _loggable(detail),
    )
    return {"ok": True, "state": "pending", "exposed": after}


async def _confirm_present(
    client: ApolloClient, profile: str, env_id: str, app_name: str,
    known: list[dict], company: str | None = None,
) -> tuple[list[dict], bool]:
    """Mirror of `_confirm_removed`: re-read until the app APPEARS -- and, with
    ``company``, until it carries that company (joining an existing app changes only its
    audience, so presence alone would confirm a join that has not landed).

    Same discipline, same reason. A failed read is not evidence either way, so it is
    skipped rather than treated as "not there yet" — and `known` seeds the list so a
    total read failure reports the last observed state instead of an empty one.
    """
    latest: list[dict] = list(known)
    for attempt in range(_CONFIRM_ATTEMPTS):
        if attempt:
            await asyncio.sleep(_CONFIRM_DELAY_SECONDS)
        fresh, ok = await reads._exposed_apps_read(client, profile, env_id)
        if not ok:
            logger.warning(
                "console expose: exposed-apps read FAILED while confirming %s on %s "
                "— treating as unconfirmed", app_name, env_id,
            )
            continue
        latest = fresh
        entry = next((a for a in latest if a["name"] == app_name), None)
        if entry is not None and (company is None or company in entry.get("companies", [])):
            return latest, True
    return latest, False


async def unexpose_app(
    client: ApolloClient, profile: str, cube: str, app_name: str, company: str | None = None,
) -> dict | None:
    """Remove one exposed app from a cube.

    Returns `None` when the caller cannot see the cube (the route 404s, matching
    `cube_detail`'s non-enumerable response). Otherwise a dict with:

      * `ok`            — the request was accepted (NOT "the app is already gone")
      * `state`         — `applied` | `pending` | `refused`. `applied` means Apollo no
                          longer lists the app — NOT that the cube has stopped serving
                          it; that is `rollout_settled`.
    Nothing here reports the ROLLOUT. Removing the app changes Apollo's declared
    state; the Teleport app-service Helm release then has to roll out before the app
    stops answering (2–3 minutes, measured on `cube-66odzn95`). That is established by polling
    `cube_exposed`, whose `rollout_settled` reads the entity's plan/rollout status —
    the module installation's own `state` is NOT a rollout signal and reports
    `Installed` throughout.
      * `error`         — present only when `state` is `refused`, and always a message
                          this module composed
      * `exposed`       — the cube's remaining exposed apps, so the UI can settle
                          without a second request

    **The tool's own message is never returned.** It is logged, and only logged. Two
    independent reasons, either sufficient:

      1. **Tenancy.** `unexpose` rewrites the shared module's full `apps` list, and
         its message quotes that list — every app on the cube, including other
         companies'. `list_exposed` filters those out so their names, URIs and
         addresses never reach a scoped caller; forwarding this prose would undo
         that. (This is a defect an earlier revision of this file shipped.)
      2. **It is not a user-facing message.** It carries module RIDs, a merge note,
         and the serialized variable payload. A person who clicked "Unexpose" needs
         one sentence, not an operator transcript.

    A rollout follows the module update, so `exposed` reflects Apollo's *declared*
    state immediately; the app stops answering a moment later. The UI says so rather
    than implying the change has already taken effect in-cluster.
    """
    from cube_cloud.tools import expose as expose_tool

    envs, envs_truncated = await reads._visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console unexpose target cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED — see OI-6 / issue 252.",
                cube, profile,
            )
        return None

    env_id = match.get("id") or ""

    # Refuse before touching Apollo if the app is not one this caller can manage.
    # `unexpose` enforces this itself; checking here means the common typo costs no
    # write attempt, and the message is this layer's rather than scraped from prose.
    before, before_ok = await reads._exposed_apps_read(client, profile, env_id)
    if not before_ok:
        # Fail closed, and say so accurately: this is not "that app is not yours",
        # it is "the cube's exposed state could not be read", which needs a different
        # action from the operator.
        logger.error(
            "console unexpose refused on %s for profile=%s: the exposed-apps read "
            "failed, so the manageable set is unknown", cube, profile,
        )
        return {
            "ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
            "exposed": [],
        }
    entry = next((a for a in before if a["name"] == app_name and a.get("reachable")), None)
    if entry is None:
        logger.info(
            "console unexpose refused on %s for profile=%s: %r is not in the caller's "
            "manageable set", cube, profile, app_name,
        )
        return {"ok": False, "state": "refused", "error": NOT_FOUND_MESSAGE,
                "exposed": before}

    # Which company comes off: one the caller holds (default its home one). An admin
    # naming none removes the app outright, as before (`target` None).
    from cube_cloud.auth.app_companies import app_companies as _app_companies
    held = _app_companies(profile)
    target: str | None = company
    if held is None or not held.unscoped:
        target, company_err = expose_tool._resolve_company(profile, company)
        if company_err or not target:
            return {"ok": False, "state": "refused", "error": COMPANY_NOT_HELD_MESSAGE,
                    "exposed": before}
    if target is not None and target not in entry.get("companies", []):
        return {"ok": False, "state": "refused",
                "error": f"That app is not shared with {target}, so nothing was changed.",
                "exposed": before}

    # `unexpose` takes the BARE app name and qualifies it itself — it computes
    # `_qualified_app_name(app_name, env)` unless `public_addr` is set. The console
    # holds the already-qualified stored name (`mov-sqlpad-cube-66odzn95`), so
    # passing it straight through made the tool append the cube a SECOND time
    # (`mov-sqlpad-cube-66odzn95-cube-66odzn95`), match nothing, and refuse. That
    # shipped because the tests mocked `unexpose` and asserted the call was made
    # with the qualified name — the mock encoded the wrong contract, so
    # `test_console_unexpose_integration.py` now drives the real function.
    bare, strip_err = _bare_app_name(app_name, cube)
    if strip_err:
        logger.error("console unexpose refused on %s: %s", cube, strip_err)
        return {"ok": False, "state": "refused", "error": strip_err,
                "exposed": before}

    logger.warning(
        "console unexpose STARTING: profile=%s cube=%s app=%s (bare=%s)",
        profile, cube, app_name, bare,
    )
    # Guard against the tool resolving `cube` to a DIFFERENT environment than the one
    # authorized here. This layer matched `cube` case-SENSITIVELY against a cached
    # RBAC-filtered list and kept `match["id"]` for every read; the tool re-resolves
    # the NAME via `environments._resolve_environment`, which is case-INSENSITIVE with
    # a substring fallback against a fresh list. With `Lear-Hammond-2` and
    # `lear-hammond-2` both present, the write lands on one and the confirmation reads
    # the other — reported `pending` forever, wrong cube's app removed. RBAC is not
    # crossed (the tool re-checks), but the target is.
    #
    # `_bare_app_name`'s round-trip cannot catch this: `_sanitize_label` lowercases,
    # so both spellings qualify identically.
    try:
        tool_env = await expose_tool._resolve_environment(client, cube)
    except Exception as e:
        logger.error(
            "console unexpose refused on %s: could not confirm the tool resolves the "
            "same environment (%s)", cube, type(e).__name__,
        )
        return {"ok": False, "state": "refused", "error": UNREADABLE_MESSAGE,
                "exposed": before}
    if (tool_env or {}).get("id") != env_id:
        logger.error(
            "console unexpose REFUSED on %s for profile=%s: the tool resolves that "
            "name to environment %s but this request was authorized against %s",
            cube, profile, (tool_env or {}).get("id"), env_id,
        )
        return {"ok": False, "state": "refused", "error": AMBIGUOUS_CUBE_MESSAGE,
                "exposed": before}

    detail = await expose_tool.unexpose(
        client, environment=cube, app_name=bare, profile=profile, company=company,
    )

    # Structural confirmation. The tool's message is reported but never parsed — if
    # the app is gone from the module variable, the write landed.
    after, ok = await _confirm_removed(client, profile, env_id, app_name, before, target)
    if ok:
        logger.warning(
            "console unexpose SUCCEEDED: profile=%s cube=%s app=%s", profile, cube, app_name
        )
        # `detail` is deliberately NOT returned on success. It is the tool's full
        # prose (module RID, changed variables, rollout note) — noise in a browser,
        # and the less that crosses this boundary the better. It IS logged.
        logger.info(
            "console unexpose detail (cube=%s app=%s): %s",
            cube, app_name, _loggable(detail),
        )
        # `applied` means Apollo no longer LISTS the app — NOT that the cube stopped
        # serving it. That takes a Helm rollout of the Teleport app-service release,
        # measured at 2–3 minutes on cube-66odzn95, and the client establishes it by polling
        # `/exposed` rather than this response claiming it.
        return {"ok": True, "state": "applied", "exposed": after}

    if _refused_before_writing(detail):
        # The tool bailed out before writing (a busy cube, an app-exposure service still
        # being removed): `pending` would poll for a removal that is never coming.
        logger.error(
            "console unexpose REFUSED BY THE TOOL before any write: profile=%s cube=%s "
            "app=%s — tool said: %s", profile, cube, app_name, _loggable(detail),
        )
        return {"ok": False, "state": "refused", "error": TOOL_UNEXPOSE_REFUSED_MESSAGE,
                "exposed": after}

    # On failure `detail` is the ONLY thing that says why. `update_module_variables`
    # returns its errors as a STRING rather than raising, so `_apply_removal` reports
    # "Removed '<app>'" with the failure appended — which is exactly why success here
    # is decided by re-reading Apollo and not by reading that message. Surfacing the
    # message is what turns "did not apply the change" into something actionable.
    #
    # Safe to log and return since `modules._display_variable` masks secret-named
    # variable values at the source: `expose`/`unexpose` put a live Teleport join
    # token in `authToken`, and this text used to carry it verbatim.
    logger.error(
        "console unexpose NOT CONFIRMED after %.1fs: profile=%s cube=%s app=%s — "
        "tool said: %s", _CONFIRM_BUDGET_SECONDS, profile, cube, app_name,
        _loggable(detail),
    )
    # `detail` stays in the log line above and goes no further — see the docstring.
    # NOT reported as a failure. The write may well have landed — see
    # `_confirm_removed` — and claiming "Apollo did not apply the change" when it
    # did is the bug this replaced. `ok` is true because the request was accepted;
    # `state` is what says whether it is visible yet.
    # `after` here is the last SUCCESSFUL read (a failed one is skipped above), so it
    # is never a spurious empty set.
    return {"ok": True, "state": "pending", "exposed": after}


# The console's feedback types, and the MCP tool's — the same pair.
#
# NOT `feedback_tool.FEEDBACK_TYPES`, which is the JIRA MODULE's own form set
# (`bug` / `feature`) and now backs only the Jira submission path. Nothing routes to
# its `bug` form any more; it is left in place so restoring a Jira bug path would be a
# routing change rather than a re-derivation of field ids the credential cannot
# introspect.
#
# `support` replaced `bug` when the form's wording became "Have a problem or
# question?" — a problem or a question is not a bug report, and routing it to a
# helpdesk rather than a product backlog is the point. The MCP tool moved with it
# (`feedback.SEND_FEEDBACK_TYPES` is the same pair), so the two surfaces agree; a
# pre-rename agent's `bug` is bridged at dispatch by
# `feedback.normalize_feedback_type`, never here.
SUPPORT_TYPE = "support"
CONSOLE_FEEDBACK_TYPES = (SUPPORT_TYPE, "feature")


async def submit_feedback(
    profile: str,
    feedback_type: str,
    summary: str,
    details: str,
    business_impact: str,
    cube: str | None,
):
    """Route the console's feedback form to the right system, and return a reference.

    **Two destinations, on purpose.** `support` ("Have a problem or question?") files a
    Freshservice ticket, because that is a support interaction and Freshservice has the
    agent queue, SLAs and requester portal behind it. `feature` still raises a customer
    request on the Jira CF board, which is a product-feedback backlog rather than a
    helpdesk. Sending both to one system would put "my cube is down" and "it would be
    nice if…" in the same queue with the same triage.

    The dispatch lives HERE rather than as a second route, deliberately: the console's
    mutating surface is a fixed set of routes and
    `test_console_routes.py` fails when that set changes, so growing it is a decision
    someone makes on purpose rather than a side effect of adding a form option.

    Neither error is caught here — `FeedbackError` and `FreshserviceError` both
    propagate to `routes.submit_feedback`, which is where they become a JSON response.
    """
    from cube_cloud.tools import feedback as feedback_tool
    from cube_cloud.tools import freshservice as freshservice_tool

    logger.info(
        "console feedback: profile=%s type=%s cube=%s", profile, feedback_type, cube,
    )

    if feedback_type == SUPPORT_TYPE:
        return await freshservice_tool.submit_support_request_from_console(
            profile=profile,
            summary=summary,
            details=details,
            business_impact=business_impact,
            cube=cube,
        )

    return await feedback_tool.submit_feedback_from_console(
        feedback_type=feedback_type,
        summary=summary,
        details=details,
        business_impact=business_impact,
        cube=cube,
    )


# ---------------------------------------------------------------------------
# AI tab: deploy and remove catalog models (docs/ai-reactor-deploy-spec.md §5)
# ---------------------------------------------------------------------------

def _ai_result(result, cube: str) -> dict:
    """The response body for an AI write. Messages are composed in `reactor.service`;
    no Apollo text ever reaches it."""
    return {
        "ok": result.ok,
        "outcome": result.outcome,
        "message": result.message,
        "steps": list(result.steps),
        "ai": reads.ai_payload(result.state, cube) if result.state is not None else None,
    }


async def ai_deploy(
    client: ApolloClient, profile: str, cube: str, model_id: str, replace: str | None = None,
) -> dict | None:
    """Send a catalog model to a cube. None when the caller cannot see the cube.

    The environment comes from the caller's RBAC-filtered list and is passed to the
    reactor layer as a resolved row (`id`, `spaceId`, `namespaceId`), so nothing below
    re-resolves the cube by name — the case-insensitive re-resolution `expose_app` has
    to guard against does not arise here.
    """
    from cube_cloud.reactor import service as reactor

    env = await reads._ai_environment(client, profile, cube)
    if env is None:
        return None
    result = await reactor.deploy(
        client, env, model_id, replace=replace, can_write=reads.ai_can_write(profile),
        profile=profile,
    )
    logger.info(
        "console ai deploy %s on %s by profile=%s: %s (%s)",
        model_id, cube, profile, result.outcome, ", ".join(result.steps) or "no steps",
    )
    return _ai_result(result, cube)


async def ai_remove(client: ApolloClient, profile: str, cube: str, model_id: str) -> dict | None:
    """Remove an Edgeport-managed model from a cube. None when the caller cannot see it."""
    from cube_cloud.reactor import service as reactor

    env = await reads._ai_environment(client, profile, cube)
    if env is None:
        return None
    result = await reactor.remove(
        client, env, model_id, can_write=reads.ai_can_write(profile), profile=profile,
    )
    logger.info(
        "console ai remove %s on %s by profile=%s: %s (%s)",
        model_id, cube, profile, result.outcome, ", ".join(result.steps) or "no steps",
    )
    return _ai_result(result, cube)
