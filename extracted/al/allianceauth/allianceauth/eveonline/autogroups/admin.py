import logging
from typing import Any
from collections import OrderedDict

from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from .models import AutogroupsConfig, ManagedAllianceGroup, ManagedCorpGroup

logger = logging.getLogger(__name__)


def _sync_user_groups(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: "models.QuerySet[AutogroupsConfig]") -> None:
    for agc in queryset:
        logger.debug(f"update_all_states_group_membership for {agc}")
        agc.update_all_states_group_membership()


@admin.register(AutogroupsConfig)
class AutogroupsConfigAdmin(admin.ModelAdmin):
    formfield_overrides = {models.CharField: {'strip': False}}

    def get_readonly_fields(self, request, obj=None) -> list[str] | list[Any]:
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return [
                'corp_group_prefix', 'corp_name_source', 'alliance_group_prefix', 'alliance_name_source',
                'replace_spaces', 'replace_spaces_with'
            ]
        else:
            return []

    def get_actions(self, request) -> OrderedDict[Any, Any]:
        actions = super().get_actions(request)
        actions['sync_user_groups'] = (
            _sync_user_groups,
            'sync_user_groups',
            'Sync all users groups for this Autogroup Config'
        )
        return actions


admin.site.register(ManagedCorpGroup)
admin.site.register(ManagedAllianceGroup)
