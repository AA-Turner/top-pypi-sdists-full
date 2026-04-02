"""SDE related models for Eve Universe."""

from django.db import models

from eveuniverse.managers import (
    EveIndustryActivityDurationManager,
    EveIndustryActivityMaterialManager,
    EveIndustryActivityProductManager,
    EveIndustryActivitySkillManager,
    EveTypeMaterialManager,
)

from .base import EveUniverseInlineModel
from .universe_1 import EveType


class EveIndustryActivity(EveUniverseInlineModel):
    """An industry activity in Eve Online."""

    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=30)

    class _EveUniverseMeta:
        load_order = 101


class EveIndustryActivityDuration(EveUniverseInlineModel):
    """Number of seconds it takes to create a blueprint product."""

    eve_type = models.ForeignKey(
        EveType,
        on_delete=models.CASCADE,
        help_text="Blueprint type",
        related_name="industry_durations",
    )
    activity = models.ForeignKey(EveIndustryActivity, on_delete=models.CASCADE)
    time = models.PositiveIntegerField()

    objects = EveIndustryActivityDurationManager()

    class _EveUniverseMeta:
        load_order = 136

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_type", "activity"],
                name="fpk_eveindustryactivity",
            )
        ]


class EveIndustryActivityMaterial(EveUniverseInlineModel):
    """The materials and amounts required to create a blueprint product."""

    eve_type = models.ForeignKey(
        EveType,
        on_delete=models.CASCADE,
        help_text="Blueprint type",
        related_name="industry_materials",
    )
    activity = models.ForeignKey(EveIndustryActivity, on_delete=models.CASCADE)
    material_eve_type = models.ForeignKey(
        EveType,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Material required type",
    )
    quantity = models.PositiveIntegerField()

    objects = EveIndustryActivityMaterialManager()

    class _EveUniverseMeta:
        load_order = 137

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "eve_type",
                    "material_eve_type",
                    "activity",
                ],
                name="fpk_eveindustryactivitymaterial",
            )
        ]


class EveIndustryActivityProduct(EveUniverseInlineModel):
    """Quantities of products for blueprints."""

    eve_type = models.ForeignKey(
        EveType,
        on_delete=models.CASCADE,
        help_text="Blueprint type",
        related_name="industry_products",
    )
    activity = models.ForeignKey(EveIndustryActivity, on_delete=models.CASCADE)
    product_eve_type = models.ForeignKey(
        EveType, on_delete=models.CASCADE, related_name="+", help_text="Result type"
    )
    quantity = models.PositiveIntegerField()

    objects = EveIndustryActivityProductManager()

    class _EveUniverseMeta:
        load_order = 138

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "eve_type",
                    "product_eve_type",
                    "activity",
                ],
                name="fpk_eveindustryactivityproduct",
            )
        ]


class EveIndustryActivitySkill(EveUniverseInlineModel):
    """Levels of skills required for blueprint run."""

    eve_type = models.ForeignKey(
        EveType,
        on_delete=models.CASCADE,
        help_text="Blueprint type",
        related_name="industry_skills",
    )
    activity = models.ForeignKey(EveIndustryActivity, on_delete=models.CASCADE)
    skill_eve_type = models.ForeignKey(
        EveType, on_delete=models.CASCADE, related_name="+", help_text="Skill book type"
    )

    level = models.PositiveIntegerField(db_index=True)

    objects = EveIndustryActivitySkillManager()

    class _EveUniverseMeta:
        load_order = 139

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_type", "skill_eve_type", "activity"],
                name="fpk_eveindustryactivityskill",
            )
        ]


class EveTypeMaterial(EveUniverseInlineModel):
    """Material type for an Eve online type"""

    eve_type = models.ForeignKey(
        EveType, on_delete=models.CASCADE, related_name="materials"
    )
    material_eve_type = models.ForeignKey(
        EveType, on_delete=models.CASCADE, related_name="material_types"
    )
    quantity = models.PositiveIntegerField()

    objects = EveTypeMaterialManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_type", "material_eve_type"],
                name="fpk_evetypematerial",
            )
        ]

    class _EveUniverseMeta:
        load_order = 135

    def __str__(self) -> str:
        return f"{self.eve_type}-{self.material_eve_type}"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"eve_type={repr(self.eve_type)}, "
            f"material_eve_type={repr(self.material_eve_type)}, "
            f"quantity={self.quantity}"
            ")"
        )
