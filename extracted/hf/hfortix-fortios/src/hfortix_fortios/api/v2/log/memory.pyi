"""Type stubs for LOG memory endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Memory:
    """Memory log operations."""
    anomaly: MemoryAnomaly
    app_ctrl: MemoryAppCtrl
    cifs: MemoryCifs
    dlp: MemoryDlp
    dns: MemoryDns
    emailfilter: MemoryEmailfilter
    event: MemoryEvent
    file_filter: MemoryFileFilter
    gtp: MemoryGtp
    ips: MemoryIps
    ssh: MemorySsh
    ssl: MemorySsl
    traffic: MemoryTraffic
    virus: MemoryVirus
    voip: MemoryVoip
    waf: MemoryWaf
    webfilter: MemoryWebfilter

    def __init__(self, client: IHTTPClient) -> None: ...


class MemoryAnomaly:
    """Log data for the given log type (and subtype)."""
    raw: MemoryAnomalyRaw

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

class MemoryAppCtrl:
    """Log data for the given log type (and subtype)."""
    archive: MemoryAppCtrlArchive
    raw: MemoryAppCtrlRaw

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

class MemoryCifs:
    """Log data for the given log type (and subtype)."""
    raw: MemoryCifsRaw

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

class MemoryDlp:
    """Log data for the given log type (and subtype)."""
    raw: MemoryDlpRaw

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

class MemoryDns:
    """Log data for the given log type (and subtype)."""
    raw: MemoryDnsRaw

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

class MemoryEmailfilter:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEmailfilterRaw

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

class MemoryEvent:
    """MemoryEvent log category."""
    compliance_check: MemoryEventComplianceCheck
    connector: MemoryEventConnector
    endpoint: MemoryEventEndpoint
    fortiextender: MemoryEventFortiextender
    ha: MemoryEventHa
    router: MemoryEventRouter
    security_rating: MemoryEventSecurityRating
    system: MemoryEventSystem
    user: MemoryEventUser
    vpn: MemoryEventVpn
    wad: MemoryEventWad
    wireless: MemoryEventWireless

    def __init__(self, client: IHTTPClient) -> None: ...

class MemoryFileFilter:
    """Log data for the given log type (and subtype)."""
    raw: MemoryFileFilterRaw

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

class MemoryGtp:
    """Log data for the given log type (and subtype)."""
    raw: MemoryGtpRaw

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

class MemoryIps:
    """Log data for the given log type (and subtype)."""
    archive: MemoryIpsArchive
    raw: MemoryIpsRaw

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

class MemorySsh:
    """Log data for the given log type (and subtype)."""
    raw: MemorySshRaw

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

class MemorySsl:
    """Log data for the given log type (and subtype)."""
    raw: MemorySslRaw

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

class MemoryTraffic:
    """MemoryTraffic log category."""
    fortiview: MemoryTrafficFortiview
    forward: MemoryTrafficForward
    local: MemoryTrafficLocal
    multicast: MemoryTrafficMulticast
    sniffer: MemoryTrafficSniffer
    threat: MemoryTrafficThreat

    def __init__(self, client: IHTTPClient) -> None: ...

class MemoryVirus:
    """Log data for the given log type (and subtype)."""
    archive: MemoryVirusArchive
    raw: MemoryVirusRaw

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

class MemoryVoip:
    """Log data for the given log type (and subtype)."""
    raw: MemoryVoipRaw

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

class MemoryWaf:
    """Log data for the given log type (and subtype)."""
    raw: MemoryWafRaw

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

class MemoryWebfilter:
    """Log data for the given log type (and subtype)."""
    raw: MemoryWebfilterRaw

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

class MemoryAnomalyRaw:
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

class MemoryAppCtrlArchive:
    """Return a list of archived items for the desired type."""
    download: MemoryAppCtrlArchiveDownload

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

class MemoryAppCtrlRaw:
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

class MemoryCifsRaw:
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

class MemoryDlpRaw:
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

class MemoryDnsRaw:
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

class MemoryEmailfilterRaw:
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

class MemoryEventComplianceCheck:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventComplianceCheckRaw

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

class MemoryEventConnector:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventConnectorRaw

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

class MemoryEventEndpoint:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventEndpointRaw

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

class MemoryEventFortiextender:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventFortiextenderRaw

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

class MemoryEventHa:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventHaRaw

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

class MemoryEventRouter:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventRouterRaw

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

class MemoryEventSecurityRating:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventSecurityRatingRaw

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

class MemoryEventSystem:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventSystemRaw

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

class MemoryEventUser:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventUserRaw

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

class MemoryEventVpn:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventVpnRaw

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

class MemoryEventWad:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventWadRaw

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

class MemoryEventWireless:
    """Log data for the given log type (and subtype)."""
    raw: MemoryEventWirelessRaw

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

class MemoryFileFilterRaw:
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

class MemoryGtpRaw:
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

class MemoryIpsArchive:
    """Return a list of archived items for the desired type."""
    download: MemoryIpsArchiveDownload

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

class MemoryIpsRaw:
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

class MemorySshRaw:
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

class MemorySslRaw:
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

class MemoryTrafficFortiview:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficFortiviewRaw

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

class MemoryTrafficForward:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficForwardRaw

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

class MemoryTrafficLocal:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficLocalRaw

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

class MemoryTrafficMulticast:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficMulticastRaw

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

class MemoryTrafficSniffer:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficSnifferRaw

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

class MemoryTrafficThreat:
    """Log data for the given log type (and subtype)."""
    raw: MemoryTrafficThreatRaw

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

class MemoryVirusArchive:
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

class MemoryVirusRaw:
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

class MemoryVoipRaw:
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

class MemoryWafRaw:
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

class MemoryWebfilterRaw:
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

class MemoryAppCtrlArchiveDownload:
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

class MemoryEventComplianceCheckRaw:
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

class MemoryEventConnectorRaw:
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

class MemoryEventEndpointRaw:
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

class MemoryEventFortiextenderRaw:
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

class MemoryEventHaRaw:
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

class MemoryEventRouterRaw:
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

class MemoryEventSecurityRatingRaw:
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

class MemoryEventSystemRaw:
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

class MemoryEventUserRaw:
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

class MemoryEventVpnRaw:
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

class MemoryEventWadRaw:
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

class MemoryEventWirelessRaw:
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

class MemoryIpsArchiveDownload:
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

class MemoryTrafficFortiviewRaw:
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

class MemoryTrafficForwardRaw:
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

class MemoryTrafficLocalRaw:
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

class MemoryTrafficMulticastRaw:
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

class MemoryTrafficSnifferRaw:
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

class MemoryTrafficThreatRaw:
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
