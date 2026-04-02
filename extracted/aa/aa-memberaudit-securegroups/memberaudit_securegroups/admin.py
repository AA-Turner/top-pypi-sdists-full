"""
Admin pages
"""

# Standard Library
from typing import Any

# Third Party
import humanize

# Django
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

# Member Audit
from memberaudit.models import CharacterRole

# Memberaudit Securegroups
from memberaudit_securegroups.models import (
    ActivityFilter,
    AgeFilter,
    AssetFilter,
    ComplianceFilter,
    CorporationRoleFilter,
    CorporationTitleFilter,
    SkillPointFilter,
    SkillSetFilter,
    TimeInCorporationFilter,
)


class SingletonModelAdmin(admin.ModelAdmin):
    """
    Prevents Django admin users deleting the singleton or adding extra rows.
    """

    actions = None  # Removes the default delete action.

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return self.model.objects.all().count() == 0


@admin.register(ActivityFilter)
class ActivityFilterAdmin(admin.ModelAdmin):
    """
    ActivityFilterAdmin
    """

    list_display = ("description", "_inactivity_threshold")

    def _inactivity_threshold(self, obj):
        inactivity_threshold = obj.inactivity_threshold

        return_value = ngettext(
            f"{inactivity_threshold:d} day",
            f"{inactivity_threshold:d} days",
            inactivity_threshold,
        )

        return return_value


@admin.register(AgeFilter)
class AgeFilterAdmin(admin.ModelAdmin):
    """
    AgeFilterAdmin
    """

    list_display = ("description", "_age_threshold")

    def _age_threshold(self, obj):
        return f"{obj.age_threshold:d} days"


@admin.register(AssetFilter)
class AssetFilterAdmin(admin.ModelAdmin):
    """
    AssetFilterAdmin
    """

    list_display = ("description", "_assets")
    autocomplete_fields = ["assets"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)

        return qs.prefetch_related("assets")

    @admin.display()
    def _assets(self, obj) -> str:
        objs = obj.assets.all()

        return ", ".join(sorted([obj.name for obj in objs]))


@admin.register(ComplianceFilter)
class ComplianceFilterAdmin(SingletonModelAdmin):
    """
    ComplianceFilterAdmin
    """

    list_display = ("description",)


class CorporationRoleListFilter(admin.SimpleListFilter):
    title = _("corporation role")
    parameter_name = "corporation_role"

    def lookups(self, request, model_admin):
        """
        Return lookups with used roles only.
        """

        roles = set(model_admin.get_queryset(request).values_list("role", flat=True))
        result = [(role, CharacterRole.Role(role).label) for role in roles]

        return sorted(result, key=lambda o: o[1])

    def queryset(self, request, queryset):
        """
        Return queryset for selected role.
        """

        if value := self.value():
            return queryset.filter(role=value)


@admin.register(CorporationRoleFilter)
class CorporationRoleFilterAdmin(admin.ModelAdmin):
    """
    CorporationRoleFilterAdmin
    """

    list_display = ("description", "role", "_corporations")
    list_filter = (CorporationRoleListFilter,)
    filter_horizontal = ("corporations",)
    fields = ("description", "role", "corporations", "include_alts")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)

        return qs.prefetch_related("corporations")

    @admin.display()
    def _corporations(self, obj) -> str:
        objs = obj.corporations.all()

        return ", ".join(sorted([obj.corporation_name for obj in objs]))


@admin.register(CorporationTitleFilter)
class CorporationTitleFilterAdmin(admin.ModelAdmin):
    """
    CorporationTitleFilterAdmin
    """

    list_display = ("description", "title", "_corporations")
    filter_horizontal = ("corporations",)
    fields = ("description", "title", "corporations", "include_alts")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)

        return qs.prefetch_related("corporations")

    @admin.display()
    def _corporations(self, obj) -> str:
        objs = obj.corporations.all()

        return ", ".join(sorted([obj.corporation_name for obj in objs]))


@admin.register(SkillPointFilter)
class SkillPointFilterAdmin(admin.ModelAdmin):
    """
    SkillPointFilterAdmin
    """

    list_display = ("description", "_skill_point_threshold")

    def _skill_point_threshold(self, obj):
        skillpoints = humanize.intword(obj.skill_point_threshold)

        return f"{skillpoints} skill points"


@admin.register(SkillSetFilter)
class SkillSetFilterAdmin(admin.ModelAdmin):
    """
    SkillSetFilterAdmin
    """

    list_display = ("description", "_skill_sets", "character_type")
    filter_horizontal = ("skill_sets",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)

        return qs.prefetch_related("skill_sets")

    @admin.display()
    def _skill_sets(self, obj) -> str:
        objs = obj.skill_sets.all()

        return ", ".join(sorted([obj.name for obj in objs]))


@admin.register(TimeInCorporationFilter)
class TimeInCorporationFilterAdmin(admin.ModelAdmin):
    """
    TimeInCorporationFilterAdmin
    """

    list_display = ("description", "minimum_days")
