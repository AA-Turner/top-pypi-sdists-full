"""ExampleMixin, Client's methods for the caller's live example: a workspace, project and
experiment the server makes, and the stages read off what exists there (twin: app/projects/example)."""

from __future__ import annotations

#: The route: always the CALLER's own example, so it carries no id.
EXAMPLE_PATH = "/v1/onboarding/example"
#: The person keeps it (agent-prompt install PR4b).
EXAMPLE_KEEP_PATH = "/v1/onboarding/example/keep"


class ExampleMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def start_example(self, *, profile: str | None = None, session_id: str | None = None) -> dict:
        """``POST /v1/onboarding/example``: start the caller's live example, or answer the live one
        (idempotent). ``profile`` (`full` | `runs`) replaces what the example recorded; omitted, it
        is kept. ``session_id`` (the install chat) is recorded only while the example has none:
        the first chat keeps it (the answer's ``session_id`` says which). Slugs may be numbered:
        read them from the answer. 402 ``LimitReachedError`` at the plan's project limit."""
        body = {key: value for key, value in (("profile", profile), ("session_id", session_id)) if value}
        return self.transport.post(EXAMPLE_PATH, body)

    def get_example(self) -> dict:
        """``GET /v1/onboarding/example``: the live example, its stages and the facts behind them.
        ``NotFoundError`` (``no_example``) when there is none."""
        return self.transport.get(EXAMPLE_PATH)

    def keep_example(self) -> dict:
        """``POST /v1/onboarding/example/keep``: the caller keeps their live example; the answer's
        ``kept_at`` says since when (a second keep changes nothing). ``NotFoundError``
        (``no_example``) when there is none."""
        return self.transport.post(EXAMPLE_KEEP_PATH, idempotent=True)

    def delete_example(self) -> None:
        """``DELETE /v1/onboarding/example``: the example workspace and everything in it, for good.
        ``ConflictError`` (``example_has_your_work``, naming the items) when it holds anything that
        is not the example's; nothing is deleted then."""
        self.transport.delete(EXAMPLE_PATH)
