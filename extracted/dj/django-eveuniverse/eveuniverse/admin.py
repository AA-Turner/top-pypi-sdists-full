"""Admin site for Eve Universe."""

from django.contrib import admin

from .models import (
    EveCategory,
    EveConstellation,
    EveGroup,
    EveMoon,
    EvePlanet,
    EveRegion,
    EveSolarSystem,
    EveType,
)


class EveUniverseEntityModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    ordering = ["name"]
    search_fields = ["name"]


@admin.register(EveCategory)
class EveCategoryAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveConstellation)
class EveConstellationAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveGroup)
class EveGroupAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveMoon)
class EveMoonAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveRegion)
class EveRegionAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EvePlanet)
class EvePlanetAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveSolarSystem)
class EveSolarSystemAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveType)
class EveTypeAdmin(EveUniverseEntityModelAdmin):
    pass
