"""Type stubs for LOG disk endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Disk:
    """Disk log operations."""
    anomaly: DiskAnomaly
    app_ctrl: DiskAppCtrl
    cifs: DiskCifs
    dlp: DiskDlp
    dns: DiskDns
    emailfilter: DiskEmailfilter
    event: DiskEvent
    file_filter: DiskFileFilter
    gtp: DiskGtp
    ips: DiskIps
    ssh: DiskSsh
    ssl: DiskSsl
    traffic: DiskTraffic
    virus: DiskVirus
    voip: DiskVoip
    waf: DiskWaf
    webfilter: DiskWebfilter

    def __init__(self, client: IHTTPClient) -> None: ...


class DiskAnomaly:
    """Log data for the given log type (and subtype)."""
    raw: DiskAnomalyRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get anomaly logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskAppCtrl:
    """Log data for the given log type (and subtype)."""
    archive: DiskAppCtrlArchive
    raw: DiskAppCtrlRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get app_ctrl logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskCifs:
    """Log data for the given log type (and subtype)."""
    raw: DiskCifsRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get cifs logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskDlp:
    """Log data for the given log type (and subtype)."""
    raw: DiskDlpRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get dlp logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskDns:
    """Log data for the given log type (and subtype)."""
    raw: DiskDnsRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get dns logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEmailfilter:
    """Log data for the given log type (and subtype)."""
    raw: DiskEmailfilterRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get emailfilter logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEvent:
    """DiskEvent log category."""
    compliance_check: DiskEventComplianceCheck
    connector: DiskEventConnector
    endpoint: DiskEventEndpoint
    fortiextender: DiskEventFortiextender
    ha: DiskEventHa
    router: DiskEventRouter
    security_rating: DiskEventSecurityRating
    system: DiskEventSystem
    user: DiskEventUser
    vpn: DiskEventVpn
    wad: DiskEventWad
    wireless: DiskEventWireless

    def __init__(self, client: IHTTPClient) -> None: ...

class DiskFileFilter:
    """Log data for the given log type (and subtype)."""
    raw: DiskFileFilterRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get file_filter logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskGtp:
    """Log data for the given log type (and subtype)."""
    raw: DiskGtpRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get gtp logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskIps:
    """Log data for the given log type (and subtype)."""
    archive: DiskIpsArchive
    raw: DiskIpsRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ips logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskSsh:
    """Log data for the given log type (and subtype)."""
    raw: DiskSshRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ssh logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskSsl:
    """Log data for the given log type (and subtype)."""
    raw: DiskSslRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ssl logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTraffic:
    """DiskTraffic log category."""
    fortiview: DiskTrafficFortiview
    forward: DiskTrafficForward
    local: DiskTrafficLocal
    multicast: DiskTrafficMulticast
    sniffer: DiskTrafficSniffer
    threat: DiskTrafficThreat

    def __init__(self, client: IHTTPClient) -> None: ...

class DiskVirus:
    """Log data for the given log type (and subtype)."""
    archive: DiskVirusArchive
    raw: DiskVirusRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get virus logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskVoip:
    """Log data for the given log type (and subtype)."""
    raw: DiskVoipRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get voip logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskWaf:
    """Log data for the given log type (and subtype)."""
    raw: DiskWafRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get waf logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskWebfilter:
    """Log data for the given log type (and subtype)."""
    raw: DiskWebfilterRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get webfilter logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskAnomalyRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get anomaly raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskAppCtrlArchive:
    """Return a list of archived items for the desired type."""
    download: DiskAppCtrlArchiveDownload

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get app_ctrl archive logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskAppCtrlRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get app_ctrl raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskCifsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get cifs raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskDlpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get dlp raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskDnsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get dns raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEmailfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get emailfilter raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventComplianceCheck:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventComplianceCheckRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event compliance_check logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventConnector:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventConnectorRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event connector logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventEndpoint:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventEndpointRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event endpoint logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventFortiextender:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventFortiextenderRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event fortiextender logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventHa:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventHaRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event ha logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventRouter:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventRouterRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event router logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventSecurityRating:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventSecurityRatingRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event security_rating logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventSystem:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventSystemRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event system logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventUser:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventUserRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event user logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventVpn:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventVpnRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event vpn logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventWad:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventWadRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event wad logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventWireless:
    """Log data for the given log type (and subtype)."""
    raw: DiskEventWirelessRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event wireless logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskFileFilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get file_filter raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskGtpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get gtp raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskIpsArchive:
    """Return a list of archived items for the desired type."""
    download: DiskIpsArchiveDownload

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ips archive logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskIpsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ips raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskSshRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ssh raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskSslRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ssl raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficFortiview:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficFortiviewRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic fortiview logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficForward:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficForwardRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic forward logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficLocal:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficLocalRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic local logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficMulticast:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficMulticastRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic multicast logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficSniffer:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficSnifferRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic sniffer logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficThreat:
    """Log data for the given log type (and subtype)."""
    raw: DiskTrafficThreatRaw

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic threat logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskVirusArchive:
    """Return a description of the quarantined virus file."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get virus archive logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskVirusRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get virus raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskVoipRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get voip raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskWafRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get waf raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskWebfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get webfilter raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskAppCtrlArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get app_ctrl archive download logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventComplianceCheckRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event compliance_check raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventConnectorRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event connector raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventEndpointRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event endpoint raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventFortiextenderRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event fortiextender raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventHaRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event ha raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventRouterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event router raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventSecurityRatingRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event security_rating raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventSystemRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event system raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventUserRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event user raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventVpnRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event vpn raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventWadRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event wad raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskEventWirelessRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get event wireless raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskIpsArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get ips archive download logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficFortiviewRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic fortiview raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficForwardRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic forward raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficLocalRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic local raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficMulticastRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic multicast raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficSnifferRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic sniffer raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...

class DiskTrafficThreatRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: IHTTPClient) -> None: ...

    def get(
        self,
        *,
        rows: int | None = None,
        session_id: int | None = None,
        serial_no: str | None = None,
        is_ha_member: bool | None = None,
        filter: str | None = None,
        extra: str | None = None,
        vdom: str | None = None,
    ) -> FortiObjectList:
        """
        Get traffic threat raw logs.

        Args:
            rows: Number of rows to return
            session_id: Session ID for paginated retrieval
            serial_no: Retrieve logs from specific device
            is_ha_member: Whether the device is an HA member
            filter: Filter expression
            extra: Extra data flags
            vdom: Virtual domain

        Returns:
            FortiObjectList containing log records
        """
        ...
