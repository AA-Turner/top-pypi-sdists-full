"""
Datatables views for Alliance Auth AFAT app.
"""

# Django
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef, QuerySet
from django.http import HttpRequest
from django.utils import timezone

# Alliance Auth
from allianceauth.framework.datatables import DataTablesView
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.models import FatLink, Log
from afat.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


class FatLinksTableView(PermissionRequiredMixin, DataTablesView):
    """
    Datatables view for FatLinks.
    """

    permission_required = "afat.basic_access"
    model = FatLink
    columns = [
        ("fleet", "afat/partials/datatables/fatlinks/column-fleetname.html"),
        ("fleet_type", "{{ row.fleet_type }}"),
        ("doctrine", "{{ row.doctrine }}"),
        (
            "creator__profile__main_character__character_name",
            "{{ row.creator.profile.main_character }}",
        ),
        ("created", "afat/partials/datatables/fatlinks/column-date.html"),
        ("", "{{ row.number_of_fats }}"),
        ("", "afat/partials/datatables/fatlinks/column-actions.html"),
    ]

    logger.debug("FatLinksTableView initialized with columns: %s", columns)

    def get_model_qs(
        self, request: HttpRequest, *args, **kwargs  # pylint: disable=unused-argument
    ) -> QuerySet:
        """
        Get the queryset for the model.

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        qs = (
            self.model.objects.select_related_default().filter(
                created__year=kwargs.get("year", timezone.now().year)
            )
            # .annotate_fats_count()
        )

        return qs


class LogsTableView(PermissionRequiredMixin, DataTablesView):
    """
    Datatables view for FatLinks.
    """

    permission_required = ("afat.manage_afat", "afat.log_view")  # Either permission
    model = Log
    columns = [
        ("log_time", "afat/partials/datatables/logs/log-time.html"),
        (
            "user__profile__main_character__character_name",
            "afat/partials/datatables/logs/user.html",
        ),
        ("fatlink_hash", "afat/partials/datatables/logs/fatlink-hash.html"),
        ("log_text", "{{ row.log_text }}"),
    ]

    logger.debug("LogsTableView initialized with columns: %s", columns)

    def has_permission(self):
        """
        Check if the user has any of the required permissions.

        :return:
        :rtype:
        """

        perms = self.get_permission_required()
        user = self.request.user

        if isinstance(perms, str):
            return user.has_perm(perms)

        return any(user.has_perm(p) for p in perms)

    def get_model_qs(
        self, request: HttpRequest, *args, **kwargs  # pylint: disable=unused-argument
    ) -> QuerySet:
        """
        Get the queryset for the model.

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        qs = self.model.objects.select_related(
            "user", "user__profile__main_character"
        ).annotate(
            fatlink_exists=Exists(FatLink.objects.filter(hash=OuterRef("fatlink_hash")))
        )

        return qs
