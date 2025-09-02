from enum import Enum

STATE_OK = "ok"
STATE_FAILED = "failed"


class SensorType(Enum):
    """The sensor type class creates an enumeration of the supported sensors by YouLess."""
    WATER = "water"
    GAS = "gas"
    POWER_USAGE = "power_usage"
    POWER_METER = "power_meter"
    DELIVERY_METER = "delivery_meter"
    EXTRA_METER = "extra_meter"
    PHASE1 = "phase1"
    PHASE2 = "phase2"
    PHASE3 = "phase3"
    TARIFF = "tariff"
    MONTH_PEAK = "month_peak"
    MONTH_PEAK_TIME = "month_peak_time"
    POWER_AVERAGE = "power_average"
