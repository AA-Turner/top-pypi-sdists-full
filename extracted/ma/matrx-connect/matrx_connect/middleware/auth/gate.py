"""The HTTP organization admission gate."""

from __future__ import annotations


from matrx_utils import vcprint
from starlette.requests import HTTPConnection, Request

from matrx_connect.context.app_context import AppContext

from .types import (
    _ADMISSION_REASON_CODES,
    _matches_organization_exempt,
    is_authenticated_resource_route,
    ADMIN_LANE_AUDIT_UNAVAILABLE,
    ADMIN_LANE_UNVERIFIABLE,
    _admission_failure,
)


class OrganizationGate:
    """Mixin on ``AuthMiddleware``: identity present + no organization + not exempt -> refused."""

    def _is_organization_exempt(self, path: str) -> bool:
        """Match an exemption at a SEGMENT boundary, never as raw text.

        A bare ``startswith`` made ``/health`` exempt ``/healthcare/patients``:
        an exemption list that silently widens itself is worse than no list,
        because it reads as narrow. A plain entry matches the path exactly, or
        the path continues with ``/``; a ``{parameter}`` entry matches ONE
        route exactly and is never a prefix.

        The matching RULE lives in ``_matches_organization_exempt`` so the
        module-level ``is_organization_exempt_path`` (what hosts and guard
        tests ask) can never drift from what the request path actually does.
        """
        return _matches_organization_exempt(
            path,
            self._organization_exempt_paths,
            self._organization_exempt_patterns,
            getattr(self, "_organization_required_patterns", ()),
        )

    def _is_authenticated_resource_route(self, request: Request) -> bool:
        return is_authenticated_resource_route(
            request.method,
            request.url.path,
            self._authenticated_resource_routes,
            raw_path=request.scope.get("raw_path"),
        )

    def _organization_admission_reason(
        self, request: Request | HTTPConnection, ctx: AppContext
    ) -> str | None:
        """The one rule: identity present + no organization + not exempt.

        Shared by the HTTP path (``_organization_admission_failure``, which
        wraps this in a 400 JSON response) and the WebSocket path
        (``_admit_websocket``, which wraps this in an ASGI ``websocket.close``)
        so there is exactly one place the admission RULE is stated — only the
        transport-specific refusal shape differs.

        Returns a short machine reason string, or None to admit the request.
        """
        if not getattr(ctx, "user_id", None):
            # No identity at all — the route's own auth requirement answers
            # this with a 401 (or, for WS, its own handshake refusal).
            # Telling an anonymous caller "organization required" would send
            # them to fix the wrong thing.
            return None
        if getattr(ctx, "auth_type", None) in ("fingerprint", "cookie"):
            # Lanes that CANNOT name an organization are admitted, not gated.
            # A fingerprint guest has no iam.memberships row to verify — guest
            # work is guest-scoped by construction, and demanding a header
            # they can never legitimately send turns every anonymous surface
            # into a 400. The file-session cookie lane is stricter still: it
            # authenticates <img>/<video> byte GETs, and a browser tag cannot
            # attach ANY header — gating it silently killed every private
            # media render. The organization admission rule is for callers
            # with tenant membership (JWT / API key), who can and must state
            # the organization they act in.
            return None
        if getattr(ctx, "organization_id", None):
            return None
        if isinstance(request, Request) and self._is_authenticated_resource_route(request):
            return None
        if self._is_organization_exempt(request.url.path):
            return None
        # The machine reason NAMES the situation. It used to be the single
        # string "organization_required" for four different worlds, which is
        # what made the sentence below wrong in three of them.
        failure = _admission_failure(ctx)
        if failure and getattr(ctx, "organization_admission", None) == "unverifiable":
            return failure
        return _ADMISSION_REASON_CODES.get(
            getattr(ctx, "organization_admission", "none") or "none",
            "organization_required",
        )

    @staticmethod
    def _organization_admission_words(ctx: AppContext) -> tuple[str, str, str]:
        """(code, message, user_message) for THIS request's admission failure.

        🚨 V-CORRECTNESS F1 (2026-09-07). One sentence answered four different
        situations: no header at all, a real organization the caller is not in,
        an id for no organization, and a value that is not an id. Three of the
        four were told "This request carried an identity but no organization …
        Choose the organization you're working in" — advice that is
        unactionable for somebody who DID choose one — and a permanent
        non-membership was told to "try again" exactly like a transient
        resolver outage. The information to say the right thing was already on
        the context: this campaign added `organization_admission` and
        `claimed_organization_id` and then never read either. This is the read.

        Every sentence names what is wrong AND what to do about it, and the
        `user_message` is the one a person sees — never the generic fallback.
        """
        admission = getattr(ctx, "organization_admission", "none") or "none"
        claimed = getattr(ctx, "claimed_organization_id", None)
        # The id itself rides the envelope's `claimed_organization_id`, never the sentence: a
        # message is words a person reads (TABLE-API-1 / VERIFIER-31 D2).
        named = "the organization in X-Organization-Id" if claimed else "an organization"

        if admission == "denied":
            return (
                "organization_forbidden",
                f"This request named {named} and you are not a member of it. "
                "Membership is checked on every request and is never inferred; "
                "nothing here is retryable until it changes.",
                "You are not a member of that organization, so this cannot run in "
                "it. Switch to an organization you belong to, or ask one of its "
                "administrators to add you.",
            )
        if admission == "unknown":
            return (
                "organization_not_found",
                f"This request named {named}, and no such organization exists.",
                "That organization doesn't exist — it may have been deleted, or the "
                "link you followed is out of date. Pick your organization again.",
            )
        if admission == "archived":
            return (
                "organization_archived",
                f"This request named {named}, and that organization is archived. "
                "An archived organization admits no request until its owner "
                "restores it; nothing is retryable until then.",
                "That organization is archived. Restore it to keep working in it, "
                "or switch to another organization.",
            )
        if admission == "malformed":
            return (
                "organization_id_invalid",
                "The X-Organization-Id this request sent is not an organization id. "
                "Nothing was looked up.",
                "The organization this request named isn't a valid one. Reload the "
                "page and choose your organization again.",
            )
        failure = _admission_failure(ctx) if admission == "unverifiable" else None
        if failure == ADMIN_LANE_AUDIT_UNAVAILABLE:
            return (
                ADMIN_LANE_AUDIT_UNAVAILABLE,
                f"Your platform-admin access to {named} was verified, but the admin "
                "audit log could not record this admission, and admin work never runs "
                "unrecorded, so it was refused. Your membership and access are not the "
                "problem; the audit log is.",
                "The admin audit log is unavailable right now. Your admin access is "
                "fine, but admin work is never done without a record, and the record "
                "could not be written. Try again in a moment; if it keeps happening, "
                "tell support the admin audit log is failing.",
            )
        if failure == ADMIN_LANE_UNVERIFIABLE:
            return (
                ADMIN_LANE_UNVERIFIABLE,
                f"This request asked to act in {named} as a platform admin, and the "
                "platform could not confirm your admin access (the admin check "
                "failed). Nothing was decided about you.",
                "We couldn't confirm your admin access just now. This is on us, not "
                "on you. Try again in a moment; if it keeps happening, tell support "
                "the admin access check is failing.",
            )
        if admission == "unverifiable":
            return (
                "organization_unverifiable",
                f"This request named {named} and the platform could not verify your "
                "membership (the membership lookup failed). It is NOT demoted to "
                "no-organization: resolving anyway would silently run in a different "
                "scope than the one you asked for.",
                "We couldn't confirm your organization just now — this is on us, not "
                "on you. Try again in a moment; if it keeps happening, tell support "
                "the membership lookup is failing.",
            )
        return (
            "organization_required",
            "This request carried an identity but no organization. Send the "
            "X-Organization-Id header naming the organization you are acting "
            "in; the server verifies your membership and never chooses one "
            "for you.",
            "Choose the organization you're working in, then try again.",
        )

    def _organization_admission_failure(self, request: Request, ctx: AppContext):
        """Refuse an authenticated request that names no organization.

        Identity has always been undeniable on this platform because it is
        resolved HERE, at the top, and nothing routes without it. Organization
        was not: it was resolved only when a caller happened to send one, and
        each route was left to invent its own late check — which is why the
        same missing organization surfaced as a 400 deep inside one feature, a
        silently mis-tenanted write in the next, and nothing at all in a third.

        An organization is a per-request fact, exactly like the bearer token,
        and it is admitted on the same line. A request carrying an identity but
        no organization does not reach feature code.

        It is deliberately NOT resolved for the caller here: a server that
        picks an organization when the caller forgot one is how work lands in
        the wrong tenant (see common-docs/systems/architecture/database/projects/no-db-assigned-org/PLAN.md). The
        caller states it; the middleware verifies membership; nobody guesses.

        Returns a Starlette response to send, or None to admit the request.
        """
        if self._organization_admission_reason(request, ctx) is None:
            return None
        path = request.url.path

        from starlette.responses import JSONResponse

        code, message, user_message = self._organization_admission_words(ctx)

        vcprint(
            f"[AUTH][REJECT] {request.method} {path} — {code} "
            f"(user={ctx.user_id}, claimed="
            f"{getattr(ctx, 'claimed_organization_id', None)})",
            color="yellow",
            # This is an intentional 400 caller denial, not an application
            # failure.  ERROR feeds the production repair safety net and
            # turns normal control flow into a false incident family.
            log_level="WARNING",
        )
        # 🚨 THE REASON MUST BE WHERE A CLIENT READS IT (2026-09-14).
        #
        # `require_organization_context` raises `HTTPException(400, detail={...})`
        # and the app's error handler HOISTS that detail dict's keys to the
        # ROOT of the response — `{error, message, user_message, details,
        # request_id, ...extras}`. This middleware sits ABOVE the exception
        # handlers, so it builds its own response; it used to build the
        # PRE-hoist shape, `{"detail": {...}}`, and called that "the same
        # envelope". It is not the same WIRE shape, and a client reading
        # `body.user_message` / `body.message` off the root found neither:
        # every organization admission refusal arrived at a person as "The
        # server refused this request and sent no reason with it" — the exact
        # sentence matrx-frontend prints when a body carries no readable
        # reason (GET /seo/brands/{id}/strategy for a brand in another org,
        # ops.app_log 2026-09-14 22:48). The words were always computed; they
        # simply never reached the screen.
        #
        # So the envelope is emitted HOISTED, matching what the error handler
        # produces for the identical refusal raised from a route. The STATUS
        # stays 400 for every shape: it is the same admission gate and existing
        # clients branch on it. `code` still says which of the five situations
        # this is, so a client can retry the retryable one and only that one.
        #
        # EXCEPT `unverifiable` (2026-09-25): that is not the caller's mistake,
        # it is the server failing to look the membership up. A 400 tells the
        # client "your request is wrong, do not retry"; 503 + Retry-After is
        # the honest status. No client branched on 400 for this code.
        # The admin-lane failures ride the same marker: the server could not
        # decide, so they are 503 + Retry-After too, with their own words.
        unverifiable = getattr(ctx, "organization_admission", None) == "unverifiable"
        return JSONResponse(
            status_code=503 if unverifiable else 400,
            headers={"Retry-After": "5"} if unverifiable else None,
            content={
                "error": code,
                "code": code,
                "message": message,
                "user_message": user_message,
                "details": None,
                "organization_admission": getattr(ctx, "organization_admission", "none"),
                "claimed_organization_id": getattr(ctx, "claimed_organization_id", None),
                "request_id": getattr(ctx, "request_id", None) or "",
            },
        )
