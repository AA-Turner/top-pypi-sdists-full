__lazy_modules__ = ["allianceauth.corputils.models", "django.contrib.auth.models"]

import logging
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from allianceauth.corputils.models import CorpStats  # noqa: F401

logger = logging.getLogger(__name__)


class CorpStatsQuerySet(models.QuerySet["CorpStats"]):
    def visible_to(self, user: "User") -> "CorpStatsQuerySet":
        # superusers get all visible
        if user.is_superuser:
            logger.debug(f'Returning all corpstats for superuser {user}.')
            return self

        try:
            char = user.profile.main_character
            assert char
            # build all accepted queries
            queries = [models.Q(token__user=user)]
            if user.has_perm('corputils.view_alliance_corpstats'):
                if char.alliance_id is not None:
                    queries.append(models.Q(corp__alliance__alliance_id=char.alliance_id))
                else:
                    queries.append(models.Q(corp__corporation_id=char.corporation_id))
            if user.has_perm('corputils.view_corp_corpstats'):
                if user.has_perm('corputils.view_alliance_corpstats'):
                    pass
                else:
                    queries.append(models.Q(corp__corporation_id=char.corporation_id))
            if user.has_perm('corputils.view_state_corpstats'):
                queries.append(models.Q(corp__in=user.profile.state.member_corporations.all()))
                queries.append(models.Q(corp__alliance__in=user.profile.state.member_alliances.all()))
            logger.debug(f'{len(queries)} queries for user {user} visible corpstats.')
            # filter based on queries
            query = queries.pop()
            for q in queries:
                query |= q
            return self.filter(query)
        except AssertionError:
            logger.debug(f'User {user} has no main character. No corpstats visible.')
            return self.none()


class CorpStatsManager(models.Manager["CorpStats"]):
    def get_queryset(self) -> CorpStatsQuerySet:
        return CorpStatsQuerySet(self.model, using=self._db)

    def visible_to(self, user: "User") -> CorpStatsQuerySet:
        return self.get_queryset().visible_to(user)
