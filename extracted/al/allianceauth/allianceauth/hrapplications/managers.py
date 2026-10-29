__lazy_modules__ = ["allianceauth.authentication.models", "allianceauth.hrapplications.models"]

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from allianceauth.authentication.models import User
    from allianceauth.hrapplications.models import Application  # noqa: F401


class ApplicationManager(models.Manager["Application"]):

    def pending_requests_count_for_user(self, user: "User") -> int | None:
        """Returns the number of pending group requests for the given user"""
        if user.is_superuser:
            return self.filter(approved__isnull=True).count()
        elif user.has_perm("auth.human_resources"):
            main_character = user.profile.main_character
            if main_character:
                return (
                    self
                    .select_related("form__corp")
                    .filter(form__corp__corporation_id=main_character.corporation_id)
                    .filter(approved__isnull=True)
                    .count()
                )
            else:
                return None
        else:
            return None
