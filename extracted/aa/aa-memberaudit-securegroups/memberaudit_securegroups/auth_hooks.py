"""Hook into Alliance Auth"""

from allianceauth import hooks

from memberaudit_securegroups.models import (
    ActivityFilter,
    AgeFilter,
    AssetFilter,
    ComplianceFilter,
    CorporationRoleFilter,
    CorporationTitleFilter,
    HomeStationFilter,
    SkillPointFilter,
    SkillSetFilter,
    TimeInCorporationFilter,
)


@hooks.register("secure_group_filters")
def filters() -> list:
    """Return list of secure group filters."""

    return [
        ActivityFilter,
        AgeFilter,
        AssetFilter,
        ComplianceFilter,
        CorporationRoleFilter,
        CorporationTitleFilter,
        HomeStationFilter,
        SkillPointFilter,
        SkillSetFilter,
        TimeInCorporationFilter,
    ]
