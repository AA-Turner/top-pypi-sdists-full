import logging
from datetime import timedelta
from math import ceil
from typing import TYPE_CHECKING

from celery import shared_task

from django.utils import timezone

from .models import CallbackRedirect, Token

if TYPE_CHECKING:  # py3.14
    # Third Party
    from celery.result import AsyncResult

    # https://github.com/sbdchd/celery-types
    classes = [
        AsyncResult,
    ]

    for cls in classes:
        setattr(cls, "__class_getitem__", classmethod(lambda cls, *args, **kwargs: cls))  # noqa

logger = logging.getLogger(__name__)


@shared_task
def cleanup_callbackredirect(max_age: int = 300) -> None:
    """
    Delete old :model:`esi.CallbackRedirect` models.
    Accepts a max_age parameter, in seconds (default 300).
    """
    cutoff = timezone.now() - timedelta(seconds=max_age)
    logger.debug(
        "Deleting all callback redirects created before %s",
        cutoff.strftime("%b %d %Y %H:%M:%S")
    )
    CallbackRedirect.objects.filter(created__lte=cutoff).delete()


@shared_task
def cleanup_token() -> None:
    """
    Delete Orphaned Tokens, then refresh or delete expired :model:`esi.Token` models.
    """
    orphaned_tokens = Token.objects.filter(user__isnull=True)
    if orphaned_tokens.exists():
        logger.info("Deleting %d orphaned tokens.", orphaned_tokens.count())
        orphaned_tokens.delete()

    expired_tokens = Token.objects.exclude(user__isnull=True).get_expired()
    if expired_tokens.exists():
        logger.info(
            "Triggering bulk refresh of %d expired tokens.", expired_tokens.count()
        )
        for token_pk in (
            expired_tokens.filter(refresh_token__isnull=False)
            .values_list("pk", flat=True)
        ):
            refresh_or_delete_token.apply_async(args=(token_pk,), priority=8)


@shared_task
def cleanup_token_subset(fraction: int = 48) -> None:
    """
    Delete Orphaned Tokens, then refresh or delete a subset of expired :model:`esi.Token` models.

    This task operates on 1/fraction of the oldest tokens and can be called on a more regular schedule
    """
    orphaned_tokens = Token.objects.filter(user__isnull=True)
    if orphaned_tokens.exists():
        logger.info("Deleting %d orphaned tokens.", orphaned_tokens.count())
        orphaned_tokens.delete()

    expired_tokens = Token.objects.exclude(user__isnull=True).get_expired()
    expired_tokens_subset = expired_tokens.filter(
        refresh_token__isnull=False
    ).order_by("created")[:ceil(expired_tokens.count() / fraction)]

    if expired_tokens.exists():
        logger.info(
            f"Triggering bulk refresh of subset/possible {expired_tokens_subset.count()}/{expired_tokens.count()} expired tokens."
        )
        for token_pk in expired_tokens_subset.values_list("pk", flat=True):
            refresh_or_delete_token.apply_async(args=(token_pk,), priority=8)


@shared_task
def refresh_or_delete_token(token_pk: int) -> None:
    token = Token.objects.get(pk=token_pk)
    token.refresh_or_delete()
