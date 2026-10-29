from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class ImpersonationLog(models.Model):
    """Audit record of a superuser impersonating another user.

    Usernames are copied so the record survives either user being deleted.
    """
    impersonator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name=_('impersonator')
    )
    impersonator_username = models.CharField(_('impersonator username'), max_length=150)
    target = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name=_('impersonated user')
    )
    target_username = models.CharField(_('impersonated username'), max_length=150)
    started = models.DateTimeField(_('started'), auto_now_add=True, db_index=True)
    ended = models.DateTimeField(_('ended'), null=True, blank=True)

    class Meta:
        verbose_name = _('impersonation log')
        verbose_name_plural = _('impersonation logs')
        ordering = ['-started']
        default_permissions = ('view',)

    def __str__(self) -> str:
        return f'{self.impersonator_username} -> {self.target_username} ({self.started:%Y-%m-%d %H:%M})'
