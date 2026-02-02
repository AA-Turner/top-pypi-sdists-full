"""Type stubs for LOG forticloud endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Forticloud:
    """Forticloud log operations."""
    anomaly: ForticloudAnomaly
    app_ctrl: ForticloudAppCtrl
    cifs: ForticloudCifs
    dlp: ForticloudDlp
    dns: ForticloudDns
    emailfilter: ForticloudEmailfilter
    event: ForticloudEvent
    file_filter: ForticloudFileFilter
    gtp: ForticloudGtp
    ips: ForticloudIps
    ssh: ForticloudSsh
    ssl: ForticloudSsl
    traffic: ForticloudTraffic
    virus: ForticloudVirus
    voip: ForticloudVoip
    waf: ForticloudWaf
    webfilter: ForticloudWebfilter

    def __init__(self, client: IHTTPClient) -> None: ...


class ForticloudAnomaly:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudAnomalyRaw

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

class ForticloudAppCtrl:
    """Log data for the given log type (and subtype)."""
    archive: ForticloudAppCtrlArchive
    raw: ForticloudAppCtrlRaw

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

class ForticloudCifs:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudCifsRaw

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

class ForticloudDlp:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudDlpRaw

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

class ForticloudDns:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudDnsRaw

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

class ForticloudEmailfilter:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEmailfilterRaw

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

class ForticloudEvent:
    """ForticloudEvent log category."""
    compliance_check: ForticloudEventComplianceCheck
    connector: ForticloudEventConnector
    endpoint: ForticloudEventEndpoint
    fortiextender: ForticloudEventFortiextender
    ha: ForticloudEventHa
    router: ForticloudEventRouter
    security_rating: ForticloudEventSecurityRating
    system: ForticloudEventSystem
    user: ForticloudEventUser
    vpn: ForticloudEventVpn
    wad: ForticloudEventWad
    wireless: ForticloudEventWireless

    def __init__(self, client: IHTTPClient) -> None: ...

class ForticloudFileFilter:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudFileFilterRaw

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

class ForticloudGtp:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudGtpRaw

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

class ForticloudIps:
    """Log data for the given log type (and subtype)."""
    archive: ForticloudIpsArchive
    raw: ForticloudIpsRaw

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

class ForticloudSsh:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudSshRaw

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

class ForticloudSsl:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudSslRaw

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

class ForticloudTraffic:
    """ForticloudTraffic log category."""
    fortiview: ForticloudTrafficFortiview
    forward: ForticloudTrafficForward
    local: ForticloudTrafficLocal
    multicast: ForticloudTrafficMulticast
    sniffer: ForticloudTrafficSniffer
    threat: ForticloudTrafficThreat

    def __init__(self, client: IHTTPClient) -> None: ...

class ForticloudVirus:
    """Log data for the given log type (and subtype)."""
    archive: ForticloudVirusArchive
    raw: ForticloudVirusRaw

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

class ForticloudVoip:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudVoipRaw

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

class ForticloudWaf:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudWafRaw

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

class ForticloudWebfilter:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudWebfilterRaw

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

class ForticloudAnomalyRaw:
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

class ForticloudAppCtrlArchive:
    """Return a list of archived items for the desired type."""
    download: ForticloudAppCtrlArchiveDownload

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

class ForticloudAppCtrlRaw:
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

class ForticloudCifsRaw:
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

class ForticloudDlpRaw:
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

class ForticloudDnsRaw:
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

class ForticloudEmailfilterRaw:
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

class ForticloudEventComplianceCheck:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventComplianceCheckRaw

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

class ForticloudEventConnector:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventConnectorRaw

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

class ForticloudEventEndpoint:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventEndpointRaw

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

class ForticloudEventFortiextender:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventFortiextenderRaw

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

class ForticloudEventHa:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventHaRaw

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

class ForticloudEventRouter:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventRouterRaw

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

class ForticloudEventSecurityRating:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventSecurityRatingRaw

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

class ForticloudEventSystem:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventSystemRaw

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

class ForticloudEventUser:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventUserRaw

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

class ForticloudEventVpn:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventVpnRaw

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

class ForticloudEventWad:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventWadRaw

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

class ForticloudEventWireless:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudEventWirelessRaw

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

class ForticloudFileFilterRaw:
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

class ForticloudGtpRaw:
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

class ForticloudIpsArchive:
    """Return a list of archived items for the desired type."""
    download: ForticloudIpsArchiveDownload

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

class ForticloudIpsRaw:
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

class ForticloudSshRaw:
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

class ForticloudSslRaw:
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

class ForticloudTrafficFortiview:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficFortiviewRaw

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

class ForticloudTrafficForward:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficForwardRaw

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

class ForticloudTrafficLocal:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficLocalRaw

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

class ForticloudTrafficMulticast:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficMulticastRaw

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

class ForticloudTrafficSniffer:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficSnifferRaw

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

class ForticloudTrafficThreat:
    """Log data for the given log type (and subtype)."""
    raw: ForticloudTrafficThreatRaw

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

class ForticloudVirusArchive:
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

class ForticloudVirusRaw:
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

class ForticloudVoipRaw:
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

class ForticloudWafRaw:
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

class ForticloudWebfilterRaw:
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

class ForticloudAppCtrlArchiveDownload:
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

class ForticloudEventComplianceCheckRaw:
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

class ForticloudEventConnectorRaw:
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

class ForticloudEventEndpointRaw:
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

class ForticloudEventFortiextenderRaw:
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

class ForticloudEventHaRaw:
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

class ForticloudEventRouterRaw:
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

class ForticloudEventSecurityRatingRaw:
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

class ForticloudEventSystemRaw:
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

class ForticloudEventUserRaw:
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

class ForticloudEventVpnRaw:
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

class ForticloudEventWadRaw:
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

class ForticloudEventWirelessRaw:
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

class ForticloudIpsArchiveDownload:
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

class ForticloudTrafficFortiviewRaw:
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

class ForticloudTrafficForwardRaw:
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

class ForticloudTrafficLocalRaw:
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

class ForticloudTrafficMulticastRaw:
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

class ForticloudTrafficSnifferRaw:
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

class ForticloudTrafficThreatRaw:
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
