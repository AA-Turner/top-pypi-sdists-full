from enum import StrEnum

class ManagedAgentsModelCostPriceResponseCurrency(StrEnum):
    USD = "USD"

    def __str__(self) -> str:
        return str(self.value)
