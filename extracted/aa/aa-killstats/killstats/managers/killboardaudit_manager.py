# Django
from django.db import models

# AA Killstats
from killstats.providers import logger


class CorporationsAuditQuerySet(models.QuerySet):
    def visible_to(self, user):
        # pylint: disable=import-outside-toplevel
        # AA Killstats
        from killstats.models.general import General

        # superusers and admins get all visible
        if General.objects.has_management_access(user):
            logger.debug("Returning all corps for Admin %s.", user)
            return self

        try:
            char = user.profile.main_character
            assert char
            query = models.Q(corporation__corporation_id=char.corporation_id)

            logger.debug("Returning Main Corporation for %s", user)

            return self.filter(query)
        except AssertionError:
            logger.debug("User %s has no main character. Nothing visible.", user)
            return self.none()


class CorporationsAuditManager(models.Manager):
    def get_queryset(self):
        return CorporationsAuditQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        return self.get_queryset().visible_to(user)


CorporationManager = CorporationsAuditManager.from_queryset(CorporationsAuditQuerySet)


class AlliancesAuditQuerySet(models.QuerySet):
    def visible_to(self, user):
        # pylint: disable=import-outside-toplevel
        # AA Killstats
        from killstats.models.general import General

        # superusers and admins get all visible
        if General.objects.has_management_access(user):
            logger.debug("Returning all allys for Admin %s.", user)
            return self

        try:
            char = user.profile.main_character
            assert char
            query = models.Q(alliance__alliance_id=char.alliance_id)

            logger.debug("Returning Main Alliance for %s", user)

            return self.filter(query)
        except AssertionError:
            logger.debug("User %s has no main character. Nothing visible.", user)
            return self.none()


class AlliancesAuditManager(models.Manager):
    def get_queryset(self):
        return AlliancesAuditQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        return self.get_queryset().visible_to(user)


AllianceManager = AlliancesAuditManager.from_queryset(AlliancesAuditQuerySet)
