"""
Helper functions for association between Auth user and EveCharacter
"""

# Django
from django.contrib.auth.models import User
from django.db.models import QuerySet

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter


def get_all_characters_with_fats_from_user(user: User) -> QuerySet[EveCharacter]:
    """
    Get all characters from a user

    :param user: The user
    :type user: User
    :return: A queryset of EveCharacter objects
    :rtype: QuerySet[EveCharacter]
    """

    return (
        EveCharacter.objects.select_related("character_ownership")
        .filter(character_ownership__user=user, afat_fats__isnull=False)
        .order_by("-userprofile", "character_name")
        .distinct()
    )
