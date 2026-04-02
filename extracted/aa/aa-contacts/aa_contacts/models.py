from typing import ClassVar

from collections import defaultdict

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo
from esi.models import Token


class General(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('manage_alliance_contacts', 'Can manage alliance contacts'),
            ('manage_corporation_contacts', 'Can manage corporation contacts'),
            ('view_alliance_notes', 'Can view notes on alliance contacts'),
            ('view_corporation_notes', 'Can view notes on corporation contacts'),
        )


class ContactTokenQueryset(models.QuerySet):
    def with_valid_tokens(self):
        valid_tokens = Token.objects.all().require_valid()
        return self.filter(token__in=valid_tokens)


class ContactTokenManager(models.Manager):
    def get_queryset(self):
        return ContactTokenQueryset(self.model, using=self._db)

    def with_valid_tokens(self):
        return self.get_queryset().with_valid_tokens()


class ContactQueryset(models.QuerySet):
    def about(self, user_filter, only_main):
        base_query = CharacterOwnership.objects.filter(user=user_filter)
        if only_main:
            base_query = base_query.filter(character=models.F('user__profile__main_character'))

        user_characters = base_query.values('character__character_id')

        user_alliances = (
            base_query
            .filter(character__alliance_id__isnull=False)
            .values('character__alliance_id')
        )

        user_corps = base_query.values('character__corporation_id')

        user_factions = (
            base_query
            .filter(character__faction_id__isnull=False)
            .values('character__faction_id')
        )

        return self.filter(
            models.Q(contact_id__in=user_characters, contact_type=Contact.ContactTypeOptions.CHARACTER) |
            models.Q(contact_id__in=user_corps, contact_type=Contact.ContactTypeOptions.CORPORATION) |
            models.Q(contact_id__in=user_alliances, contact_type=Contact.ContactTypeOptions.ALLIANCE) |
            models.Q(contact_id__in=user_factions, contact_type=Contact.ContactTypeOptions.FACTION)
        )

    def with_contact_name(self):
        return self.annotate(
            contact_name_annotation=models.Case(
                models.When(
                    contact_type=Contact.ContactTypeOptions.CHARACTER,
                    then=models.Subquery(
                        EveCharacter.objects
                        .filter(character_id=models.OuterRef('contact_id'))
                        .values('character_name')
                    )
                ),
                models.When(
                    contact_type=Contact.ContactTypeOptions.CORPORATION,
                    then=models.Subquery(
                        EveCorporationInfo.objects
                        .filter(corporation_id=models.OuterRef('contact_id'))
                        .values('corporation_name')
                    )
                ),
                models.When(
                    contact_type=Contact.ContactTypeOptions.ALLIANCE,
                    then=models.Subquery(
                        EveAllianceInfo.objects
                        .filter(alliance_id=models.OuterRef('contact_id'))
                        .values('alliance_name')
                    )
                ),
                models.When(
                    contact_type=Contact.ContactTypeOptions.FACTION,
                    then=models.Subquery(
                        EveFactionInfo.objects
                        .filter(faction_id=models.OuterRef('contact_id'))
                        .values('faction_name')
                    )
                ),
                default=models.Value(''),
            )
        )


class ContactManager(models.Manager):
    def get_queryset(self):
        return ContactQueryset(self.model, using=self._db)

    def about(self, user_filter, only_main):
        return self.get_queryset().about(user_filter, only_main)

    def with_contact_name(self):
        return self.get_queryset().with_contact_name()


class ContactLabel(models.Model):
    label_id = models.BigIntegerField()
    label_name = models.CharField(max_length=255)

    class Meta:
        abstract = True
        default_permissions = ()


class Contact(models.Model):
    contact_id = models.BigIntegerField()

    class ContactTypeOptions(models.TextChoices):
        CHARACTER = 'character'
        CORPORATION = 'corporation'
        ALLIANCE = 'alliance'
        FACTION = 'faction'

    contact_type = models.CharField(max_length=11, choices=ContactTypeOptions.choices)
    standing = models.FloatField()
    notes = models.TextField(blank=True, default='')

    objects: ClassVar[ContactManager] = ContactManager()

    class Meta:
        abstract = True
        default_permissions = ()

    @property
    def image_src(self) -> str:
        if self.contact_type == self.ContactTypeOptions.CHARACTER:
            return EveCharacter.generic_portrait_url(self.contact_id)
        if self.contact_type == self.ContactTypeOptions.CORPORATION:
            return EveCorporationInfo.generic_logo_url(self.contact_id)
        if self.contact_type == self.ContactTypeOptions.ALLIANCE:
            return EveAllianceInfo.generic_logo_url(self.contact_id)
        if self.contact_type == self.ContactTypeOptions.FACTION:
            return EveFactionInfo.generic_logo_url(self.contact_id)
        return ''

    @property
    def _load_contact_name(self) -> str:
        if self.contact_type == self.ContactTypeOptions.CHARACTER:
            try:
                res = EveCharacter.objects.get(character_id=self.contact_id).character_name
            except EveCharacter.DoesNotExist:
                char = EveCharacter.objects.create_character(self.contact_id)
                res = char.character_name
        elif self.contact_type == self.ContactTypeOptions.CORPORATION:
            try:
                res = EveCorporationInfo.objects.get(corporation_id=self.contact_id).corporation_name
            except EveCorporationInfo.DoesNotExist:
                corp = EveCorporationInfo.objects.create_corporation(self.contact_id)
                res = corp.corporation_name
        elif self.contact_type == self.ContactTypeOptions.ALLIANCE:
            try:
                res = EveAllianceInfo.objects.get(alliance_id=self.contact_id).alliance_name
            except EveAllianceInfo.DoesNotExist:
                alliance = EveAllianceInfo.objects.create_alliance(self.contact_id)
                res = alliance.alliance_name
        elif self.contact_type == self.ContactTypeOptions.FACTION:
            try:
                res = EveFactionInfo.objects.get(faction_id=self.contact_id).faction_name
            except EveFactionInfo.DoesNotExist:
                faction = EveFactionInfo.provider.get_faction(self.contact_id)
                EveFactionInfo.objects.create(faction_id=faction.id, faction_name=faction.name)
                res = faction.name
        else:
            raise ValueError(f"Unknown contact type: {self.contact_type}")

        return res

    @property
    def contact_name(self) -> str:
        if (
            not hasattr(self, 'contact_name_annotation')
            or self.contact_name_annotation is None
            or self.contact_name_annotation == ''
        ):
            return self._load_contact_name
        else:
            return self.contact_name_annotation

    @classmethod
    def filter_missing_contact_name(cls, pk_list: list[int]) -> list[int]:
        return list(
            cls.objects
            .filter(pk__in=pk_list)
            .annotate(
                has_object=models.Case(
                    models.When(
                        contact_type=cls.ContactTypeOptions.CHARACTER,
                        then=models.Exists(EveCharacter.objects.filter(character_id=models.OuterRef('contact_id')))
                    ),
                    models.When(
                        contact_type=cls.ContactTypeOptions.CORPORATION,
                        then=models.Exists(EveCorporationInfo.objects.filter(corporation_id=models.OuterRef('contact_id')))
                    ),
                    models.When(
                        contact_type=cls.ContactTypeOptions.ALLIANCE,
                        then=models.Exists(EveAllianceInfo.objects.filter(alliance_id=models.OuterRef('contact_id')))
                    ),
                    models.When(
                        contact_type=cls.ContactTypeOptions.FACTION,
                        then=models.Exists(EveFactionInfo.objects.filter(faction_id=models.OuterRef('contact_id')))
                    ),
                    default=models.Value(False),
                    output_field=models.BooleanField()
                )
            )
            .filter(has_object=False)
            .values_list('pk', flat=True)
        )

    @classmethod
    def can_view_notes(cls, user: User) -> bool:
        raise NotImplementedError("Please implement in subclass")

    @classmethod
    def can_edit_notes(cls, user: User) -> bool:
        raise NotImplementedError("Please implement in subclass")


class ContactToken(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='+')

    last_update = models.DateTimeField(default=timezone.now)

    objects: ClassVar[ContactTokenManager] = ContactTokenManager()

    class Meta:
        abstract = True
        default_permissions = ()


class AllianceContactLabel(ContactLabel):
    alliance = models.ForeignKey(EveAllianceInfo, on_delete=models.RESTRICT, related_name='contact_labels')

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"{self.alliance} - {self.label_name}"


class AllianceContact(Contact):
    alliance = models.ForeignKey(EveAllianceInfo, on_delete=models.RESTRICT, related_name='contacts')

    labels = models.ManyToManyField(AllianceContactLabel, blank=True, related_name='contacts')

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"{self.alliance} - {self.contact_name}"

    @classmethod
    def can_view_notes(cls, user: User) -> bool:
        return user.has_perm('aa_contacts.view_alliance_notes')

    @classmethod
    def can_edit_notes(cls, user: User) -> bool:
        return user.has_perm('aa_contacts.manage_alliance_contacts') and cls.can_view_notes(user)


class AllianceToken(ContactToken):
    alliance = models.OneToOneField(EveAllianceInfo, on_delete=models.RESTRICT, related_name='+')

    class Meta:
        default_permissions = ()

    def __str__(self) -> str:
        return f"{self.alliance} Token"

    @classmethod
    def visible_for(cls, user):
        if user.is_superuser:
            return cls.objects.all()

        return cls.objects.filter(
            alliance__alliance_id__in=CharacterOwnership.objects
            .filter(user=user)
            .values('character__alliance_id')
        )


class CorporationContactLabel(ContactLabel):
    corporation = models.ForeignKey(EveCorporationInfo, on_delete=models.RESTRICT, related_name='contact_labels')

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"{self.corporation} - {self.label_name}"


class CorporationContact(Contact):
    corporation = models.ForeignKey(EveCorporationInfo, on_delete=models.RESTRICT, related_name='contacts')

    labels = models.ManyToManyField(CorporationContactLabel, blank=True, related_name='contacts')

    is_watched = models.BooleanField(null=True, blank=True, default=None)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"{self.corporation} - {self.contact_name}"

    @classmethod
    def can_view_notes(cls, user: User) -> bool:
        return user.has_perm('aa_contacts.view_corporation_notes')

    @classmethod
    def can_edit_notes(cls, user: User) -> bool:
        return user.has_perm('aa_contacts.manage_corporation_contacts') and cls.can_view_notes(user)


class CorporationToken(ContactToken):
    corporation = models.OneToOneField(EveCorporationInfo, on_delete=models.RESTRICT, related_name='+')

    class Meta:
        default_permissions = ()

    def __str__(self) -> str:
        return f"{self.corporation} Token"

    @classmethod
    def visible_for(cls, user):
        if user.is_superuser:
            return cls.objects.all()

        return cls.objects.filter(
            corporation__corporation_id__in=CharacterOwnership.objects
            .filter(user=user)
            .values('character__corporation_id')
        )

# Secure Groups integration


class BaseFilter(models.Model):
    name = models.CharField(max_length=500)  # This is the filters name shown to the admin
    description = models.CharField(max_length=500)  # this is what is shown to the user

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}: {self.description}"

    def process_filter(self, user: User):  # Single User Pass Fail system
        raise NotImplementedError("Please Create a filter!")

    def audit_filter(self, users):  # Bulk check system that also advises the user with simple messages
        raise NotImplementedError("Please Create an audit function!")


class StandingFilter(BaseFilter):
    class ComparisonOptions(models.TextChoices):
        GREATER_THAN = '>'
        GREATER_OR_EQUAL = '>='
        LESS_THAN = '<'
        LESS_OR_EQUAL = '<='
        EQUAL = '='

    comparison = models.CharField(max_length=2, choices=ComparisonOptions.choices)
    standing = models.FloatField()

    class CheckTypeOptions(models.TextChoices):
        AT_LEAST_ONE_CHARACTER = 'any'
        ALL_CHARACTERS = 'all'
        NO_CHARACTER = 'no'

    check_type = models.CharField(max_length=3, choices=CheckTypeOptions.choices, default=CheckTypeOptions.AT_LEAST_ONE_CHARACTER)
    only_main = models.BooleanField(default=False, help_text="Only consider the main character of the user")

    corporations = models.ManyToManyField(EveCorporationInfo, blank=True, related_name='corp_standing_filters', help_text="The corporations that have set the standings")
    alliances = models.ManyToManyField(EveAllianceInfo, blank=True, related_name='alliance_standing_filters', help_text="The alliances that have set the standings")

    class Meta:
        verbose_name = "Smart Filter: User Standings"
        verbose_name_plural = verbose_name
        default_permissions = ()

    @property
    def _standing_lookup(self):
        if self.comparison == self.ComparisonOptions.GREATER_THAN:
            return models.Q(standing__gt=self.standing)
        elif self.comparison == self.ComparisonOptions.GREATER_OR_EQUAL:
            return models.Q(standing__gte=self.standing)
        elif self.comparison == self.ComparisonOptions.LESS_THAN:
            return models.Q(standing__lt=self.standing)
        elif self.comparison == self.ComparisonOptions.LESS_OR_EQUAL:
            return models.Q(standing__lte=self.standing)
        else:
            return models.Q(standing=self.standing)

    def _corp_query(self, user_filter):
        return (
            CorporationContact.objects
            .about(user_filter, self.only_main)
            .filter(
                self._standing_lookup,
                corporation__in=self.corporations.all()
            )
        )

    def _alliance_query(self, user_filter):
        return (
            AllianceContact.objects
            .about(user_filter, self.only_main)
            .filter(
                self._standing_lookup,
                alliance__in=self.alliances.all()
            )
        )

    def process_filter(self, user: User) -> bool:
        return self.audit_filter(User.objects.filter(pk=user.pk))[user.pk]['check']

    def audit_filter(self, users):
        output = defaultdict(lambda: {"message": "", "check": False})

        if self.check_type == StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER:
            annotated_query = users.annotate(
                check=models.Exists(
                    self._corp_query(models.OuterRef(models.OuterRef('pk')))
                ) | models.Exists(
                    self._alliance_query(models.OuterRef(models.OuterRef('pk')))
                )
            )

            for user in annotated_query.values('pk', 'check'):
                output[user['pk']] = {
                    "message": "User has a character, corporation, alliance or faction that meets the filter" if user['check'] else "User does not meet the filter",
                    "check": user['check']
                }
        elif self.check_type == StandingFilter.CheckTypeOptions.NO_CHARACTER:
            annotated_query = users.annotate(
                check=~(
                    models.Exists(
                        self._corp_query(models.OuterRef(models.OuterRef('pk')))
                    ) | models.Exists(
                        self._alliance_query(models.OuterRef(models.OuterRef('pk')))
                    )
                )
            )

            for user in annotated_query.values('pk', 'check'):
                output[user['pk']] = {
                    "message": "User has all characters that meet the filter" if user['check'] else "User does not meet the filter",
                    "check": user['check']
                }
        else:
            base_query = CharacterOwnership.objects.filter(user=models.OuterRef('pk'))
            if self.only_main:
                base_query = base_query.filter(character=models.F('user__profile__main_character'))

            chars = (
                base_query.filter(
                    models.Exists(
                        CorporationContact.objects.filter(
                            self._standing_lookup,
                            models.Q(
                                contact_id=models.OuterRef('character__character_id'),
                                contact_type=Contact.ContactTypeOptions.CHARACTER
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__corporation_id'),
                                contact_type=Contact.ContactTypeOptions.CORPORATION
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__alliance_id'),
                                contact_type=Contact.ContactTypeOptions.ALLIANCE
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__faction_id'),
                                contact_type=Contact.ContactTypeOptions.FACTION
                            ),
                            corporation__in=self.corporations.all()
                        )
                    ) |
                    models.Exists(
                        AllianceContact.objects.filter(
                            self._standing_lookup,
                            models.Q(
                                contact_id=models.OuterRef('character__character_id'),
                                contact_type=Contact.ContactTypeOptions.CHARACTER
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__corporation_id'),
                                contact_type=Contact.ContactTypeOptions.CORPORATION
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__alliance_id'),
                                contact_type=Contact.ContactTypeOptions.ALLIANCE
                            ) |
                            models.Q(
                                contact_id=models.OuterRef('character__faction_id'),
                                contact_type=Contact.ContactTypeOptions.FACTION
                            ),
                            alliance__in=self.alliances.all()
                        )
                    )
                )
                .values('user')
                .annotate(count=models.Count('*'))
                .values('count')
            )

            annotated_query = (
                users
                .annotate(count_valid=models.Subquery(chars))
                .annotate(total=models.Subquery(
                    base_query
                    .values('user')
                    .annotate(count=models.Count('*'))
                    .values('count')
                ))
            )

            for user in annotated_query.values('pk', 'count_valid', 'total'):
                passed = user['count_valid'] == user['total']
                output[user['pk']] = {
                    "message": "User has all characters that meet the filter" if passed else "User does not meet the filter",
                    "check": passed
                }

        return output
