from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpRequest

from esi.exceptions import HTTPClientError, HTTPNotModified

from allianceauth.eveonline.models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
)
from allianceauth.eveonline.providers import open_api_provider
from allianceauth.eveonline.tasks import (
    update_all_factions, update_alliance, update_character, update_corp,
)


class EveEntityExistsError(forms.ValidationError):
    def __init__(self, entity_type_name, id) -> None:
        super().__init__(message=f'{entity_type_name} with ID {id} already exists.')


class EveEntityNotFoundError(forms.ValidationError):
    def __init__(self, entity_type_name, id) -> None:
        super().__init__(message=f'{entity_type_name} with ID {id} not found.')


class EveEntityForm(forms.ModelForm):
    id = forms.IntegerField(min_value=1)
    entity_model_class = None

    def clean_id(self):
        raise NotImplementedError()

    def save(self, commit=True):
        raise NotImplementedError()

    def save_m2m(self):
        pass


def get_faction_choices() -> list[tuple[int, str]]:
    # restrict to only those factions a player can join for faction warfare
    factions, response = open_api_provider.get_all_factions()
    player_factions = [x for x in factions if x.militia_corporation_id]
    return [(x.faction_id, x.name) for x in player_factions]


class EveFactionForm(EveEntityForm):
    entity_type_name = 'faction'
    id = forms.ChoiceField(
        choices=get_faction_choices,
        label="Name"
    )

    def clean_id(self) -> int:
        try:
            open_api_provider.get_faction(int(self.cleaned_data['id']))
        except (AssertionError, HTTPClientError) as e:
            raise EveEntityNotFoundError(self.entity_type_name, self.cleaned_data['id']) from e
        except HTTPNotModified:
            pass  # If ETAG It exists its a valid faction right?

        if self.Meta.model.objects.filter(faction_id=int(self.cleaned_data['id'])).exists():
            raise EveEntityExistsError(self.entity_type_name, self.cleaned_data['id'])

        return int(self.cleaned_data['id'])

    def save(self, commit=True) -> EveFactionInfo:
        return self.Meta.model.objects.create_faction(faction_id=self.clean_id())

    class Meta:
        fields = ['id']
        model = EveFactionInfo


class EveCharacterForm(EveEntityForm):
    entity_type_name = 'character'

    def clean_id(self) -> int:
        try:
            open_api_provider.get_character(int(self.cleaned_data['id']))
        except (AssertionError, HTTPClientError) as e:
            raise EveEntityNotFoundError(self.entity_type_name, self.cleaned_data['id']) from e
        except HTTPNotModified:
            pass  # If ETAG It exists its a valid character right?

        if self.Meta.model.objects.filter(character_id=int(self.cleaned_data['id'])).exists():
            raise EveEntityExistsError(self.entity_type_name, self.cleaned_data['id'])

        return int(self.cleaned_data['id'])

    def save(self, commit=True) -> EveCharacter:
        return self.Meta.model.objects.create_character(character_id=self.clean_id())

    class Meta:
        fields = ['id']
        model = EveCharacter


class EveCorporationForm(EveEntityForm):
    entity_type_name = 'corporation'

    def clean_id(self) -> int:
        try:
            open_api_provider.get_corporation(int(self.cleaned_data['id']))
        except (AssertionError, HTTPClientError) as e:
            raise EveEntityNotFoundError(self.entity_type_name, self.cleaned_data['id']) from e
        except HTTPNotModified:
            pass  # If ETAG It exists its a valid corporation right?

        if self.Meta.model.objects.filter(corporation_id=int(self.cleaned_data['id'])).exists():
            raise EveEntityExistsError(self.entity_type_name, self.cleaned_data['id'])

        return int(self.cleaned_data['id'])

    def save(self, commit=True) -> EveCorporationInfo:
        return self.Meta.model.objects.create_corporation(corporation_id=self.clean_id())

    class Meta:
        fields = ['id']
        model = EveCorporationInfo


class EveAllianceForm(EveEntityForm):
    entity_type_name = 'alliance'

    def clean_id(self) -> int:
        try:
            open_api_provider.get_alliance(int(self.cleaned_data['id']))
        except (AssertionError, HTTPClientError) as e:
            raise EveEntityNotFoundError(self.entity_type_name, self.cleaned_data['id']) from e
        except HTTPNotModified:
            pass  # If ETAG It exists its a valid alliance right?

        if self.Meta.model.objects.filter(alliance_id=int(self.cleaned_data['id'])).exists():
            raise EveEntityExistsError(self.entity_type_name, self.cleaned_data['id'])

        return int(self.cleaned_data['id'])

    def save(self, commit=True) -> EveAllianceInfo:
        return self.Meta.model.objects.create_alliance(alliance_id=self.clean_id())

    class Meta:
        fields = ['id']
        model = EveAllianceInfo


@admin.action(description="Update from ESI (Browser)")
def update_factions_blocking(modeladmin: "EveFactionInfoAdmin", request: HttpRequest, queryset: QuerySet[EveFactionInfo]) -> None:
    EveFactionInfo.objects.update_factions()

    modeladmin.message_user(
        request, 'Update from ESI performed for all factions'
    )


@admin.action(description="Update from ESI (Celery)")
def update_factions_queued(modeladmin: "EveFactionInfoAdmin", request: HttpRequest, queryset: QuerySet[EveFactionInfo]) -> None:
    update_all_factions.delay()

    modeladmin.message_user(
        request, 'Update from ESI Celery Task queued for all factions'
    )


@admin.register(EveFactionInfo)
class EveFactionInfoAdmin(admin.ModelAdmin):
    search_fields = ['faction_name']
    list_display = ('faction_name', 'last_updated')
    ordering = ('faction_name',)
    actions = [update_factions_blocking, update_factions_queued]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def get_form(self, request, obj=None, change=False, **kwargs) -> type[forms.ModelForm]:
        if not obj or not obj.pk:
            return EveFactionForm
        return super().get_form(request, obj, change, **kwargs)


@admin.action(description="Update from ESI (Browser)")
def update_corporations_blocking(modeladmin: "EveCorporationInfoAdmin", request: HttpRequest, queryset: QuerySet[EveCorporationInfo]) -> None:
    tasks_count = 0
    for obj in queryset:
        obj.update_corporation()
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} corporations'
    )


@admin.action(description="Update from ESI (Browser) - Clear ETag/Cache")
def update_corporations_blocking_forcerefresh(modeladmin: "EveCorporationInfoAdmin", request: HttpRequest, queryset: QuerySet[EveCorporationInfo]) -> None:
    # This task is provided as Synchronous only as being mid celery queue would have unexpected behaviour
    tasks_count = 0
    for obj in queryset:
        obj.update_corporation(force_refresh=True)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} corporations, clearing their ETags and Cache, please use responsibly'
    )


@admin.action(description="Update from ESI (Celery)")
def update_corporations_queued(modeladmin: "EveCorporationInfoAdmin", request: HttpRequest, queryset: QuerySet[EveCorporationInfo]) -> None:
    tasks_count = 0
    for obj in queryset:
        update_corp.delay(obj.corporation_id)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI Celery Task queued for {tasks_count} corporations'
    )


@admin.register(EveCorporationInfo)
class EveCorporationInfoAdmin(admin.ModelAdmin):
    search_fields = ['corporation_name']
    list_display = ('corporation_name', 'ticker', 'member_count', 'alliance', 'faction', 'last_updated')
    list_select_related = ('alliance',)
    list_filter = (
        ('alliance', admin.RelatedOnlyFieldListFilter),
        ('faction', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('corporation_name',)
    actions = [update_corporations_blocking, update_corporations_queued, update_corporations_blocking_forcerefresh]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def get_form(self, request, obj=None, change=False, **kwargs) -> type[forms.ModelForm]:
        if not obj or not obj.pk:
            return EveCorporationForm
        return super().get_form(request, obj, change, **kwargs)


@admin.action(description="Update from ESI (Browser)")
def update_alliances_blocking(modeladmin: "EveAllianceInfoAdmin", request: HttpRequest, queryset: QuerySet[EveAllianceInfo]) -> None:
    tasks_count = 0
    for obj in queryset:
        obj.update_alliance()
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} alliances'
    )


@admin.action(description="Update from ESI (Browser) - Clear ETag/Cache")
def update_alliances_blocking_forcerefresh(modeladmin: "EveAllianceInfoAdmin", request: HttpRequest, queryset: QuerySet[EveAllianceInfo]) -> None:
    # This task is provided as Synchronous only as being mid celery queue would have unexpected behaviour
    tasks_count = 0
    for obj in queryset:
        obj.update_alliance(force_refresh=True)
        obj.populate_alliance(force_refresh=True)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} alliances, clearing their ETags and Cache, please use responsibly'
    )


@admin.action(description="Update Alliances from ESI (queued task)")
def update_alliances_queued(modeladmin: "EveAllianceInfoAdmin", request: HttpRequest, queryset: QuerySet[EveAllianceInfo]) -> None:
    tasks_count = 0
    for obj in queryset:
        update_alliance.delay(obj.alliance_id)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI queued for {tasks_count} alliances'
    )


@admin.register(EveAllianceInfo)
class EveAllianceInfoAdmin(admin.ModelAdmin):
    search_fields = ['alliance_name', 'ticker']
    list_display = ('alliance_name', 'ticker', "faction", 'last_updated')
    ordering = ('alliance_name',)
    list_filter = (
        ('faction', admin.RelatedOnlyFieldListFilter),
    )
    actions = [update_alliances_blocking, update_alliances_queued, update_alliances_blocking_forcerefresh]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def get_form(self, request, obj=None, change=False, **kwargs) -> type[forms.ModelForm]:
        if not obj or not obj.pk:
            return EveAllianceForm
        return super().get_form(request, obj, change, **kwargs)


@admin.action(description="Update from ESI (Browser)")
def update_characters_blocking(modeladmin: "EveCharacterAdmin", request: HttpRequest, queryset: QuerySet[EveCharacter]) -> None:
    tasks_count = 0
    for obj in queryset:
        obj.update_character()
        obj.update_character_other()
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} characters'
    )


@admin.action(description="Update from ESI (Browser) - Clear ETag/Cache")
def update_characters_blocking_forcerefresh(modeladmin: "EveCharacterAdmin", request: HttpRequest, queryset: QuerySet[EveCharacter]) -> None:
    # This task is provided as Synchronous only as being mid celery queue would have unexpected behaviour
    tasks_count = 0
    for obj in queryset:
        obj.update_character()
        obj.update_character_other(force_refresh=True)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI performed for {tasks_count} characters, clearing their ETags and Cache, please use responsibly'
    )


@admin.action(description="Update from ESI (Celery)")
def update_characters_queued(modeladmin: "EveCharacterAdmin", request: HttpRequest, queryset: QuerySet[EveCharacter]) -> None:
    tasks_count = 0
    for obj in queryset:
        update_character.delay(obj.character_id)
        tasks_count += 1

    modeladmin.message_user(
        request, f'Update from ESI Celery Task queued for {tasks_count} characters'
    )


@admin.register(EveCharacter)
class EveCharacterAdmin(admin.ModelAdmin):
    search_fields = [
        'character_name',
        'corporation_name',
        'alliance_name',
        'character_ownership__user__username'
    ]
    list_display = (
        'character_name',
        'corporation_name',
        'alliance_name',
        'faction_name',
        'user',
        'main_character',
        'last_updated_affiliations',
        'last_updated_other',
    )
    list_select_related = (
        'character_ownership', 'character_ownership__user__profile__main_character'
    )
    list_filter = (
        'corporation_name',
        'alliance_name',
        ('alliance_name', admin.EmptyFieldListFilter),
        'faction_name',
        ('faction_name', admin.EmptyFieldListFilter),
        (
            'character_ownership__user__profile__main_character',
            admin.RelatedOnlyFieldListFilter
        ),
    )
    ordering = ('character_name', )
    actions = [update_characters_blocking, update_characters_queued, update_characters_blocking_forcerefresh]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    @staticmethod
    def user(obj) -> User | None:
        try:
            return obj.character_ownership.user
        except (AttributeError, ObjectDoesNotExist):
            return None

    @staticmethod
    def main_character(obj) -> EveCharacter | None:
        try:
            return obj.character_ownership.user.profile.main_character
        except (AttributeError, ObjectDoesNotExist):
            return None

    def get_form(self, request, obj=None, change=False, **kwargs) -> type[forms.ModelForm]:
        if not obj or not obj.pk:
            return EveCharacterForm
        return super().get_form(request, obj, change, **kwargs)
