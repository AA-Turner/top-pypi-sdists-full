"""
Logs related views
"""

# Django
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Alliance Auth
from allianceauth.authentication.decorators import permissions_required
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.models import Setting
from afat.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.log_view"))
def overview(request: WSGIRequest) -> HttpResponse:
    """
    Logs view

    :param request:
    :type request:
    :return:
    :rtype:
    """

    logger.info(msg=f"Log view called by {request.user}")

    context = {"log_duration": Setting.get_setting(Setting.Field.DEFAULT_LOG_DURATION)}

    return render(
        request=request,
        template_name="afat/view/logs/logs-overview.html",
        context=context,
    )
