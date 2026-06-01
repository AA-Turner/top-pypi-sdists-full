"""Lightweight base class for service-layer components.

``BaseService`` provides:

* Accessor helpers for the current request context (user claims, hit-id)
  via ``csrd.context``.
* A thin wrapper so subclasses can declare their repositories / delegates
  as plain constructor params — no magic, just a convenient base.

For logging, compose with ``LoggingMixin`` from ``csrd.logging``::

    from csrd.logging import LoggingMixin

    class OrderService(BaseService, LoggingMixin, auto_log=True):
        def __init__(self, repo: OrderRepository, payments: PaymentsDelegate):
            super().__init__()
            self._repo = repo
            self._payments = payments

        async def place_order(self, cart: Cart) -> Order:
            order = await self._repo.create(cart)
            try:
                await self._payments.charge(order)
            except HTTPException as exc:
                raise DownstreamError(
                    "Payment failed", detail=str(exc.detail), cause=exc
                ) from exc
            return order
"""

from typing import TYPE_CHECKING

from csrd.context import get_hit_id
from csrd.context.platform import user_info_context

if TYPE_CHECKING:
    from csrd.models.claims import UserClaims


class BaseService:
    """Base class for service-layer components.

    Provides contextual accessors for the current request.  For logging,
    compose with :class:`csrd.logging.LoggingMixin`.

    Subclasses should accept their repositories and delegates via
    ``__init__`` — ``BaseService`` intentionally knows nothing about
    those Tier-2 types so that it stays in Tier 2 itself.
    """

    # ── Context helpers ──────────────────────────────────────────────────

    @staticmethod
    def current_user() -> "UserClaims | None":
        """Return the authenticated user's claims for the current request, or ``None``."""
        return user_info_context.get()  # type: ignore[return-value]

    @staticmethod
    def current_request_id() -> str | None:
        """Return the current request's hit-id, or ``None``."""
        return get_hit_id()


__all__ = ("BaseService",)
