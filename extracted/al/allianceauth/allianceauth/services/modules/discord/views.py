__lazy_modules__ = ["django.http"]

import logging
from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from allianceauth.services.views import superuser_test

from . import __title__
from .managers import DiscordUserAlreadyLinkedError
from .models import DiscordUser
from .utils import LoggerAddTag

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

logger = LoggerAddTag(logging.getLogger(__name__), __title__)

ACCESS_PERM = 'discord.access_discord'


@login_required
@permission_required(ACCESS_PERM)
def deactivate_discord(request: "HttpRequest") -> "HttpResponse":
    logger.debug("deactivate_discord called by user %s", request.user)
    if request.user.discord.delete_user(
        is_rate_limited=False, handle_api_exceptions=True
    ):
        logger.info("Successfully deactivated Discord for user %s", request.user)
        messages.success(request, _('Deactivated Discord account.'))
    else:
        logger.error(
            "Unsuccessful attempt to deactivate Discord for user %s", request.user
        )
        messages.error(
            request, _('An error occurred while processing your Discord account.')
        )
    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def reset_discord(request: "HttpRequest") -> "HttpResponse":
    logger.debug("reset_discord called by user %s", request.user)
    if request.user.discord.delete_user(
        is_rate_limited=False, handle_api_exceptions=True
    ):
        logger.info(
            "Successfully deleted Discord user for user %s - "
            "forwarding to Discord activation.",
            request.user
        )
        return redirect("discord:activate")

    logger.error(
        "Unsuccessful attempt to reset Discord for user %s", request.user
    )
    messages.error(
        request, _('An error occurred while processing your Discord account.')
    )
    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def activate_discord(request: "HttpRequest") -> "HttpResponse":
    logger.debug("activate_discord called by user %s", request.user)
    return redirect(DiscordUser.objects.generate_oauth_redirect_url())


@login_required
@permission_required(ACCESS_PERM)
def discord_callback(request: "HttpRequest") -> "HttpResponse":
    logger.debug(
        "Received Discord callback for activation of user %s", request.user
    )
    authorization_code = request.GET.get('code', None)
    if not authorization_code:
        logger.warning(
            "Did not receive OAuth code from callback for user %s", request.user
        )
        success = False
    else:
        try:
            linked = DiscordUser.objects.add_user(
                user=request.user,
                authorization_code=authorization_code,
                is_rate_limited=False
            )
        except DiscordUserAlreadyLinkedError:
            messages.error(
                request,
                _(
                    'This Discord account is already linked to another '
                    'Alliance Auth account. A Discord account can only be '
                    'linked to one Alliance Auth account.'
                )
            )
            return redirect("services:services")

        if linked:
            logger.info(
                "Successfully activated Discord account for user %s", request.user
            )
            success = True
        else:
            logger.error(
                "Failed to activate Discord account for user %s", request.user
            )
            success = False

    if success:
        messages.success(
            request, _('Your Discord account has been successfully activated.')
        )
    else:
        messages.error(
            request,
            _(
                'An error occurred while trying to activate your Discord account. '
                'Please try again.'
            )
        )

    return redirect("services:services")


@login_required
@user_passes_test(superuser_test)
def discord_add_bot(request: "HttpRequest") -> "HttpResponse":
    return redirect(DiscordUser.objects.generate_bot_add_url())
