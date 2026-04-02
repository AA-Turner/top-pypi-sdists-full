"""Custom managers for Eve Universe models."""

from .entities import EveEntityManager
from .sde import (
    EveIndustryActivityDurationManager,
    EveIndustryActivityMaterialManager,
    EveIndustryActivityProductManager,
    EveIndustryActivitySkillManager,
    EveTypeMaterialManager,
)
from .universe import (
    EveAsteroidBeltManager,
    EveMarketPriceManager,
    EveMoonManager,
    EvePlanetManager,
    EveStargateManager,
    EveTypeManager,
)

__all__ = [
    "EveEntityManager",
    "EveIndustryActivityDurationManager",
    "EveIndustryActivityMaterialManager",
    "EveIndustryActivityProductManager",
    "EveIndustryActivitySkillManager",
    "EveTypeMaterialManager",
    "EveAsteroidBeltManager",
    "EveMarketPriceManager",
    "EveMoonManager",
    "EvePlanetManager",
    "EveStargateManager",
    "EveTypeManager",
    "EveUniverseEntityModelManager",
]
