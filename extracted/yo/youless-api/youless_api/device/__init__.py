from datetime import datetime
from typing import Optional

from youless_api.gateway import fetch_enologic_api, fetch_generic_api, fetch_phase_api
from youless_api.youless_sensor import YoulessSensor, PowerMeter, DeliveryMeter, ExtraMeter, Phase
from youless_api.const import SensorType


def ls110(host, authentication):
    """The device wrapper for the LS110, will return a function to fetch the latest information."""
    def update() -> Optional[dict]:
        """The actual method to refresh the data."""
        dataset = fetch_generic_api(host, authentication)
        if dataset is None:
            return None

        return {
            SensorType.POWER_METER: PowerMeter(
                YoulessSensor(None, None),
                YoulessSensor(None, None),
                YoulessSensor(dataset['cnt'], 'kWh')
            ),
            SensorType.POWER_USAGE: YoulessSensor(dataset['pwr'], 'W'),
            SensorType.EXTRA_METER: ExtraMeter(
                YoulessSensor(dataset['cs0'], 'kWh'),
                YoulessSensor(dataset['ps0'], 'W')
            )
        }

    return update


def ls120(host, authentication, device_info):
    """The device wrapper for the LS120, will return a function to fetch the latest information."""
    supports_phases = False
    if 'fw' in device_info:
        supports_phases = float(device_info['fw'][0:3]) >= 1.5

    def update() -> Optional[dict]:
        """The actual method to refresh the data."""
        dataset = fetch_enologic_api(host, authentication)
        phase_info = fetch_phase_api(host, authentication) if supports_phases else {}

        if dataset is None:
            return None

        return {
            SensorType.GAS: YoulessSensor(dataset['gas'], 'm3'),
            SensorType.WATER: YoulessSensor(dataset['wtr'], 'm3'),
            SensorType.POWER_USAGE: YoulessSensor(dataset['pwr'], 'W'),
            SensorType.POWER_METER: PowerMeter(
                YoulessSensor(dataset['p1'], 'kWh'),
                YoulessSensor(dataset['p2'], 'kWh'),
                YoulessSensor(dataset['net'], 'kWh')
            ),
            SensorType.DELIVERY_METER: DeliveryMeter(
                YoulessSensor(dataset['n1'], 'kWh'),
                YoulessSensor(dataset['n2'], 'kWh')
            ),
            SensorType.EXTRA_METER: ExtraMeter(
                YoulessSensor(dataset['cs0'], 'kWh'),
                YoulessSensor(dataset['ps0'], 'W')
            ),
            SensorType.PHASE1: Phase(
                YoulessSensor(phase_info['i1'], 'A'),
                YoulessSensor(phase_info['v1'], 'V'),
                YoulessSensor(phase_info['l1'], 'W')) if 'i1' in phase_info else None,
            SensorType.PHASE2: Phase(
                YoulessSensor(phase_info['i2'], 'A'),
                YoulessSensor(phase_info['v2'], 'V'),
                YoulessSensor(phase_info['l2'], '')) if 'i2' in phase_info else None,
            SensorType.PHASE3: Phase(
                YoulessSensor(phase_info['i3'], 'A'),
                YoulessSensor(phase_info['v3'], 'V'),
                YoulessSensor(phase_info['l3'], 'W')) if 'i3' in phase_info else None,
            SensorType.TARIFF: phase_info['tr'] if phase_info else None,
            SensorType.MONTH_PEAK: YoulessSensor(phase_info['pp'], 'W') if 'pp' in phase_info else None,
            SensorType.POWER_AVERAGE: YoulessSensor(phase_info['pa'], 'W') if 'pa' in phase_info else None,
            SensorType.MONTH_PEAK_TIME: datetime.strptime(str(phase_info['pts']), '%y%m%d%H%M') if 'pts' in phase_info and phase_info['pts'] > 0 else None,
        }

    return update

