from enum import Enum


class OfferingTypeUpdateTypeEnum(str, Enum):
    MARKETPLACE_BASIC = "Marketplace.Basic"
    MARKETPLACE_SITEAGENT = "Marketplace.SiteAgent"
    MARKETPLACE_SLURM = "Marketplace.Slurm"

    def __str__(self) -> str:
        return str(self.value)
