from device_detector.enums import AppType

from . import BaseClientParser


class VPNProxy(BaseClientParser):
    __slots__ = ()
    APP_TYPE = AppType.VpnProxy

    fixture_files = ('local/client/vpnproxy.yml',)


__all__ = [
    'VPNProxy',
]
