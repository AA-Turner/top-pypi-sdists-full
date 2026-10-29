import logging

from hijack.signals import hijack_ended, hijack_started

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from .models import ImpersonationLog
from .utils import get_impersonator_pk

logger = logging.getLogger(__name__)


def _close_log(impersonator_pk, target_pk) -> None:
    log = (
        ImpersonationLog.objects
        .filter(impersonator_id=impersonator_pk, target_id=target_pk, ended__isnull=True)
        .order_by('-started')
        .first()
    )
    if log:
        log.ended = timezone.now()
        log.save(update_fields=['ended'])


@receiver(hijack_started)
def impersonation_started(sender, hijacker, hijacked, request, **kwargs):
    logger.warning("Impersonation started: %s is acting as %s", hijacker, hijacked)
    ImpersonationLog.objects.create(
        impersonator=hijacker,
        impersonator_username=hijacker.get_username(),
        target=hijacked,
        target_username=hijacked.get_username(),
    )


@receiver(hijack_ended)
def impersonation_ended(sender, hijacker, hijacked, request, **kwargs):
    logger.warning("Impersonation ended: %s stopped acting as %s", hijacker, hijacked)
    _close_log(hijacker.pk, hijacked.pk)


@receiver(user_logged_out)
def impersonation_logged_out(sender, request, user, **kwargs):
    # Logging out while impersonating ends the session without passing through release
    impersonator_pk = get_impersonator_pk(request) if request else None
    if impersonator_pk and user:
        logger.warning("Impersonation ended by logout: user %s stopped acting as %s", impersonator_pk, user)
        _close_log(impersonator_pk, user.pk)
