from ocsf.events.discovery import Discovery

from ocsf.objects.actor import Actor
from ocsf.objects.device import Device
from ocsf.objects.cis_benchmark_result import CISBenchmarkResult


class DeviceConfigState(Discovery):
    """
    Device Config State events report device configuration data and CIS Benchmark
    results.
    """

    class_uid: int = 5002
    class_name: str = 'Device Config State'

    device: Device # The device that is being discovered by an inventory process.

    # Recommended:
    cis_benchmark_result: CISBenchmarkResult | None = None

    # Optional:
    actor: Actor | None = None
