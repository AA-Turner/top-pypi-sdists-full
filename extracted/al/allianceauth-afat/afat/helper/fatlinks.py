"""
Helper functions for fat links view
"""

# Django
from django.db.models import Prefetch, QuerySet

# Alliance Auth
from allianceauth.authentication.admin import User

# Alliance Auth AFAT
from afat.app_settings import use_fittings_module_for_doctrines
from afat.models import FatLink


def get_esi_fleet_information_by_user(
    user: User,
) -> dict[str, bool | list[dict[int, FatLink]]]:
    """
    Get ESI fleet information by a given FC (user)

    :param user:
    :type user:
    :return:
    :rtype:
    """

    has_open_esi_fleets = False
    open_esi_fleets_list = []
    open_esi_fleets = (
        FatLink.objects.select_related_default()
        .filter(creator=user, is_esilink=True, is_registered_on_esi=True)
        .order_by("character__character_name")
    )

    if open_esi_fleets.count() > 0:
        has_open_esi_fleets = True

        for open_esi_fleet in open_esi_fleets:
            open_esi_fleets_list.append(open_esi_fleet)

    return {
        "has_open_esi_fleets": has_open_esi_fleets,
        "open_esi_fleets_list": open_esi_fleets_list,
    }


def get_doctrines() -> QuerySet:
    """
    Get all enabled doctrines

    :return:
    :rtype:
    """

    if use_fittings_module_for_doctrines() is True:
        # Third Party
        from fittings.models import (  # pylint: disable=import-outside-toplevel
            Doctrine,
            Fitting,
        )

        cls = Doctrine.objects

        doctrines = (
            cls.prefetch_related("category")
            .prefetch_related(
                Prefetch(
                    lookup="fittings",
                    queryset=Fitting.objects.select_related("ship_type"),
                )
            )
            .union(
                cls.prefetch_related("category").prefetch_related(
                    Prefetch(
                        lookup="fittings",
                        queryset=Fitting.objects.select_related("ship_type"),
                    )
                )
            )
            .order_by("name")
        )
    else:
        # Alliance Auth AFAT
        from afat.models import Doctrine  # pylint: disable=import-outside-toplevel

        doctrines = Doctrine.objects.filter(is_enabled=True).distinct().order_by("name")

    return doctrines
