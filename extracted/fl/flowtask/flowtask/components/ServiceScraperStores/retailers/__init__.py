from .base import RetailerStrategy
from .verizon import VerizonStrategy
from .tractor_supply import TractorSupplyStrategy
from .costco import CostcoStrategy

#: Registered retailer key -> RetailerStrategy subclass. Add a new
#: retailer by writing a strategy module next to verizon.py and
#: registering it here - no changes needed to scraper.py.
RETAILERS = {
    "verizon": VerizonStrategy,
    "tractorsupply": TractorSupplyStrategy,
    "costco": CostcoStrategy,
}

__all__ = (
    "RetailerStrategy",
    "RETAILERS",
)
