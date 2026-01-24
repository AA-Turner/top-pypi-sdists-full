from adam.commands.devices.device import Device
from adam.commands.devices.device_app import DeviceApp
from adam.commands.devices.device_auit_log import DeviceAuditLog
from adam.commands.devices.device_cass import DeviceCass
from adam.commands.devices.device_export import DeviceExport
from adam.commands.devices.device_postgres import DevicePostgres
from adam.repl_state import ReplState

class Devices:
    def of(state: ReplState) -> Device:
        if state.device == ReplState.A:
            return DeviceApp()
        elif state.device == ReplState.C:
            return DeviceCass()
        elif state.device == ReplState.L:
            return DeviceAuditLog()
        elif state.device == ReplState.P:
            return DevicePostgres()
        elif state.device == ReplState.X:
            return DeviceExport()

        return DeviceCass()

    def all():
        return [DeviceApp(), DeviceCass(), DeviceAuditLog(), DevicePostgres(), DeviceExport()]