__lazy_modules__ = ["django.contrib.auth.models", "django.http"]

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from .tasks import SmfTasks
from .urls import urlpatterns

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


class SmfService(ServicesHook):
    def __init__(self) -> None:
        ServicesHook.__init__(self)
        self.name = 'smf'
        self.urlpatterns = urlpatterns
        self.service_url = settings.SMF_URL
        self.access_perm = 'smf.access_smf'
        self.name_format = '{character_name}'

    @property
    def title(self) -> str:
        return 'SMF Forums'

    def delete_user(self, user: "User", notify_user: bool = False) -> bool:
        logger.debug(f'Deleting user {user} {self.name} account')
        return SmfTasks.delete_user(user, notify_user=notify_user)

    def validate_user(self, user: "User") -> None:
        logger.debug(f'Validating user {user} {self.name} account')
        if SmfTasks.has_account(user) and not self.service_active_for_user(user):
            self.delete_user(user)

    def update_groups(self, user: "User") -> None:
        logger.debug(f'Updating {self.name} groups for {user}')
        if SmfTasks.has_account(user):
            SmfTasks.update_groups.delay(user.pk)

    def sync_nickname(self, user: "User") -> None:
        logger.debug(f"Updating {self.name} displayed name for {user}")

        if SmfTasks.has_account(user):
            SmfTasks.update_display_name.apply_async(args=[user.pk], countdown=5) # cooldown on this task to ensure DB clean when syncing

    def update_all_groups(self) -> None:
        logger.debug(f'Update all {self.name} groups called')
        SmfTasks.update_all_groups.delay()

    def service_active_for_user(self, user: "User") -> bool:
        return user.has_perm(self.access_perm)

    def render_services_ctrl(self, request: "HttpRequest") -> str:
        urls = self.Urls()
        urls.auth_activate = 'smf:activate'
        urls.auth_deactivate = 'smf:deactivate'
        urls.auth_reset_password = 'smf:reset_password'
        urls.auth_set_password = 'smf:set_password'
        return render_to_string(self.service_ctrl_template, {
            'service_name': self.title,
            'urls': urls,
            'service_url': self.service_url,
            'username': request.user.smf.username if SmfTasks.has_account(request.user) else ''
        }, request=request)


@hooks.register('services_hook')
def register_service() -> SmfService:
    return SmfService()
