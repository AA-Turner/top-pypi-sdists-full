"""
Admin pages configuration
"""

# Third Party
from solo.admin import SingletonModelAdmin

# Django
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

# Alliance Auth AFAT
from afat.app_settings import securegroups_installed
from afat.forms import DoctrineAdminForm, SettingAdminForm
from afat.models import (
    Doctrine,
    Fat,
    FatLink,
    FatsInTimeFilter,
    FleetType,
    Log,
    Setting,
)


# Register your models here.
@admin.register(FatLink)
class AFatLinkAdmin(admin.ModelAdmin):
    """
    Config for the FAT link model
    """

    list_display = (
        "created",
        "creator",
        "fleet",
        "fleet_type",
        "is_esilink",
        "hash",
        "number_of_fats",
    )
    list_filter = ("is_esilink", "fleet_type")
    ordering = ("-created",)
    search_fields = (
        "fleet_type",
        "hash",
        "fleet",
        "creator__profile__main_character__character_name",
        "creator__username",
    )
    exclude = ("link_type", "character")

    def get_queryset(self, request):
        """
        Get the queryset

        :param request:
        :type request:
        :return:
        :rtype:
        """

        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _number_of_fats=Count(expression="afat_fats", distinct=True)
        )

        return queryset

    @admin.display(ordering="_number_of_fats")
    def number_of_fats(self, obj):
        """
        Return the number of FATs per FAT link

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return getattr(obj, "_number_of_fats", None)


@admin.register(Fat)
class AFatAdmin(admin.ModelAdmin):
    """
    Config for fat model
    """

    list_display = ("character", "system", "shiptype", "fatlink")
    list_filter = ("character", "system", "shiptype")
    ordering = ("-character",)
    search_fields = (
        "character__character_name",
        "system",
        "shiptype",
        "fatlink__fleet",
        "fatlink__hash",
    )


@admin.register(FleetType)
class AFatLinkTypeAdmin(admin.ModelAdmin):
    """
    Config for the FAT link type model
    """

    list_display = ("id", "_name", "_is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)

    @admin.display(description=_("Fleet type"), ordering="name")
    def _name(self, obj):
        """
        Rewrite name

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @admin.display(description=_("Is enabled"), boolean=True, ordering="is_enabled")
    def _is_enabled(self, obj):
        """
        Rewrite is_enabled

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.is_enabled

    actions = ("activate", "deactivate")

    @admin.action(description=_("Activate selected fleet types"))
    def activate(self, request, queryset):
        """
        Mark fleet type as active

        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = True
                obj.save()

                notifications_count += 1
            except Exception:  # pylint: disable=broad-exception-caught
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    singular="Failed to activate {failed} fleet type",
                    plural="Failed to activate {failed} fleet types",
                    number=failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    singular="Activated {notifications_count} fleet type",
                    plural="Activated {notifications_count} fleet types",
                    number=notifications_count,
                ).format(notifications_count=notifications_count),
            )

    @admin.action(description=_("Deactivate selected fleet types"))
    def deactivate(self, request, queryset):
        """
        Mark fleet type as inactive

        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = False
                obj.save()

                notifications_count += 1
            except Exception:  # pylint: disable=broad-exception-caught
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    singular="Failed to deactivate {failed} fleet type",
                    plural="Failed to deactivate {failed} fleet types",
                    number=failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    singular="Deactivated {notifications_count} fleet type",
                    plural="Deactivated {notifications_count} fleet types",
                    number=notifications_count,
                ).format(notifications_count=notifications_count),
            )


@admin.register(Log)
class AFatLogAdmin(admin.ModelAdmin):
    """
    Config for the admin log model
    """

    list_display = ("log_time", "log_event", "user", "fatlink_hash", "log_text")
    ordering = ("-log_time",)
    readonly_fields = ("log_time", "log_event", "user", "fatlink_hash", "log_text")
    list_filter = ("log_event",)
    search_fields = (
        "fatlink_hash",
        "user__profile__main_character__character_name",
        "user__username",
    )


@admin.register(Setting)
class SettingAdmin(SingletonModelAdmin):
    """
    Setting Admin
    """

    form = SettingAdminForm


@admin.register(Doctrine)
class DoctrineAdmin(admin.ModelAdmin):
    """
    Doctrine Admin
    """

    form = DoctrineAdminForm

    # Display all fields in the admin page
    list_display = [field.name for field in Doctrine._meta.get_fields()]


class FatsInTimeFilterAdmin(admin.ModelAdmin):
    """
    Config for the FATs in time filter model
    """

    list_display = (
        "name",
        "description",
        "days",
        "fats_needed",
        "get_fleet_types",
        "get_ship_classes",
    )
    filter_horizontal = (
        "fleet_types",
        "ship_classes",
    )

    select_related = True

    @admin.display(description=_("Fleet types"))
    def get_fleet_types(self, obj):
        """
        Get fleet types

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return ", ".join([fleet_type.name for fleet_type in obj.fleet_types.all()])

    @admin.display(description=_("Ship classes"))
    def get_ship_classes(self, obj):
        """
        Get ship classes

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return ", ".join([ship_class.name for ship_class in obj.ship_classes.all()])


if securegroups_installed():
    admin.site.register(FatsInTimeFilter, FatsInTimeFilterAdmin)
