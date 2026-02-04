"""
FortiOS LOG API - Disk

Log query endpoints for disk logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They use nested classes to represent path parameters.

Example Usage:
    >>> fgt.api.log.disk.anomaly.get(rows=100)
    >>> fgt.api.log.disk.app_ctrl.get(rows=100)
    >>> fgt.api.log.disk.cifs.get(rows=100)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Disk:
    """Disk log operations.
    
    Provides access to disk log endpoints with nested classes
    for different log types and subtypes.
    """

    def __init__(self, client: "IHTTPClient"):
        """Initialize Disk endpoint."""
        self._client = client
        self.anomaly = DiskAnomaly(client)
        self.app_ctrl = DiskAppCtrl(client)
        self.cifs = DiskCifs(client)
        self.dlp = DiskDlp(client)
        self.dns = DiskDns(client)
        self.emailfilter = DiskEmailfilter(client)
        self.event = DiskEvent(client)
        self.file_filter = DiskFileFilter(client)
        self.gtp = DiskGtp(client)
        self.ips = DiskIps(client)
        self.ssh = DiskSsh(client)
        self.ssl = DiskSsl(client)
        self.traffic = DiskTraffic(client)
        self.virus = DiskVirus(client)
        self.voip = DiskVoip(client)
        self.waf = DiskWaf(client)
        self.webfilter = DiskWebfilter(client)


class DiskAnomaly:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAnomaly."""
        self._client = client
        self.raw = DiskAnomalyRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.anomaly.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/anomaly", params=params if params else None)
        return result

class DiskAppCtrl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAppCtrl."""
        self._client = client
        self.archive = DiskAppCtrlArchive(client)
        self.raw = DiskAppCtrlRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.app_ctrl.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/app-ctrl", params=params if params else None)
        return result

class DiskCifs:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskCifs."""
        self._client = client
        self.raw = DiskCifsRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.cifs.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/cifs", params=params if params else None)
        return result

class DiskDlp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDlp."""
        self._client = client
        self.raw = DiskDlpRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.dlp.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/dlp", params=params if params else None)
        return result

class DiskDns:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDns."""
        self._client = client
        self.raw = DiskDnsRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.dns.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/dns", params=params if params else None)
        return result

class DiskEmailfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEmailfilter."""
        self._client = client
        self.raw = DiskEmailfilterRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.emailfilter.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/emailfilter", params=params if params else None)
        return result

class DiskEvent:
    """DiskEvent log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEvent."""
        self._client = client
        self.compliance_check = DiskEventComplianceCheck(client)
        self.connector = DiskEventConnector(client)
        self.endpoint = DiskEventEndpoint(client)
        self.fortiextender = DiskEventFortiextender(client)
        self.ha = DiskEventHa(client)
        self.router = DiskEventRouter(client)
        self.security_rating = DiskEventSecurityRating(client)
        self.system = DiskEventSystem(client)
        self.user = DiskEventUser(client)
        self.vpn = DiskEventVpn(client)
        self.wad = DiskEventWad(client)
        self.wireless = DiskEventWireless(client)

class DiskFileFilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskFileFilter."""
        self._client = client
        self.raw = DiskFileFilterRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.file_filter.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/file-filter", params=params if params else None)
        return result

class DiskGtp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskGtp."""
        self._client = client
        self.raw = DiskGtpRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.gtp.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/gtp", params=params if params else None)
        return result

class DiskIps:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskIps."""
        self._client = client
        self.archive = DiskIpsArchive(client)
        self.raw = DiskIpsRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ips.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ips", params=params if params else None)
        return result

class DiskSsh:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSsh."""
        self._client = client
        self.raw = DiskSshRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ssh.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ssh", params=params if params else None)
        return result

class DiskSsl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSsl."""
        self._client = client
        self.raw = DiskSslRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ssl.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ssl", params=params if params else None)
        return result

class DiskTraffic:
    """DiskTraffic log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTraffic."""
        self._client = client
        self.fortiview = DiskTrafficFortiview(client)
        self.forward = DiskTrafficForward(client)
        self.local = DiskTrafficLocal(client)
        self.multicast = DiskTrafficMulticast(client)
        self.sniffer = DiskTrafficSniffer(client)
        self.threat = DiskTrafficThreat(client)

class DiskVirus:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVirus."""
        self._client = client
        self.archive = DiskVirusArchive(client)
        self.raw = DiskVirusRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.virus.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/virus", params=params if params else None)
        return result

class DiskVoip:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVoip."""
        self._client = client
        self.raw = DiskVoipRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.voip.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/voip", params=params if params else None)
        return result

class DiskWaf:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWaf."""
        self._client = client
        self.raw = DiskWafRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.waf.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/waf", params=params if params else None)
        return result

class DiskWebfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWebfilter."""
        self._client = client
        self.raw = DiskWebfilterRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.webfilter.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/webfilter", params=params if params else None)
        return result

class DiskAnomalyRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAnomalyRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.anomaly.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/anomaly/raw", params=params if params else None)
        return result

class DiskAppCtrlArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAppCtrlArchive."""
        self._client = client
        self.download = DiskAppCtrlArchiveDownload(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.app_ctrl.archive.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/app-ctrl/archive", params=params if params else None)
        return result

class DiskAppCtrlRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAppCtrlRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.app_ctrl.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/app-ctrl/raw", params=params if params else None)
        return result

class DiskCifsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskCifsRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.cifs.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/cifs/raw", params=params if params else None)
        return result

class DiskDlpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDlpRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.dlp.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/dlp/raw", params=params if params else None)
        return result

class DiskDnsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskDnsRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.dns.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/dns/raw", params=params if params else None)
        return result

class DiskEmailfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEmailfilterRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.emailfilter.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/emailfilter/raw", params=params if params else None)
        return result

class DiskEventComplianceCheck:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventComplianceCheck."""
        self._client = client
        self.raw = DiskEventComplianceCheckRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.compliance_check.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/compliance-check", params=params if params else None)
        return result

class DiskEventConnector:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventConnector."""
        self._client = client
        self.raw = DiskEventConnectorRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.connector.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/connector", params=params if params else None)
        return result

class DiskEventEndpoint:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventEndpoint."""
        self._client = client
        self.raw = DiskEventEndpointRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.endpoint.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/endpoint", params=params if params else None)
        return result

class DiskEventFortiextender:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventFortiextender."""
        self._client = client
        self.raw = DiskEventFortiextenderRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.fortiextender.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/fortiextender", params=params if params else None)
        return result

class DiskEventHa:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventHa."""
        self._client = client
        self.raw = DiskEventHaRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.ha.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/ha", params=params if params else None)
        return result

class DiskEventRouter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventRouter."""
        self._client = client
        self.raw = DiskEventRouterRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.router.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/router", params=params if params else None)
        return result

class DiskEventSecurityRating:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventSecurityRating."""
        self._client = client
        self.raw = DiskEventSecurityRatingRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.security_rating.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/security-rating", params=params if params else None)
        return result

class DiskEventSystem:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventSystem."""
        self._client = client
        self.raw = DiskEventSystemRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.system.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/system", params=params if params else None)
        return result

class DiskEventUser:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventUser."""
        self._client = client
        self.raw = DiskEventUserRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.user.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/user", params=params if params else None)
        return result

class DiskEventVpn:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventVpn."""
        self._client = client
        self.raw = DiskEventVpnRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.vpn.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/vpn", params=params if params else None)
        return result

class DiskEventWad:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventWad."""
        self._client = client
        self.raw = DiskEventWadRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.wad.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/wad", params=params if params else None)
        return result

class DiskEventWireless:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventWireless."""
        self._client = client
        self.raw = DiskEventWirelessRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.wireless.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/wireless", params=params if params else None)
        return result

class DiskFileFilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskFileFilterRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.file_filter.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/file-filter/raw", params=params if params else None)
        return result

class DiskGtpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskGtpRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.gtp.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/gtp/raw", params=params if params else None)
        return result

class DiskIpsArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskIpsArchive."""
        self._client = client
        self.download = DiskIpsArchiveDownload(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ips.archive.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ips/archive", params=params if params else None)
        return result

class DiskIpsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskIpsRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ips.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ips/raw", params=params if params else None)
        return result

class DiskSshRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSshRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ssh.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ssh/raw", params=params if params else None)
        return result

class DiskSslRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskSslRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ssl.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ssl/raw", params=params if params else None)
        return result

class DiskTrafficFortiview:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficFortiview."""
        self._client = client
        self.raw = DiskTrafficFortiviewRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.fortiview.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/fortiview", params=params if params else None)
        return result

class DiskTrafficForward:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficForward."""
        self._client = client
        self.raw = DiskTrafficForwardRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.forward.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/forward", params=params if params else None)
        return result

class DiskTrafficLocal:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficLocal."""
        self._client = client
        self.raw = DiskTrafficLocalRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.local.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/local", params=params if params else None)
        return result

class DiskTrafficMulticast:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficMulticast."""
        self._client = client
        self.raw = DiskTrafficMulticastRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.multicast.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/multicast", params=params if params else None)
        return result

class DiskTrafficSniffer:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficSniffer."""
        self._client = client
        self.raw = DiskTrafficSnifferRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.sniffer.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/sniffer", params=params if params else None)
        return result

class DiskTrafficThreat:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficThreat."""
        self._client = client
        self.raw = DiskTrafficThreatRaw(client)

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.threat.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/threat", params=params if params else None)
        return result

class DiskVirusArchive:
    """Return a description of the quarantined virus file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVirusArchive."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.virus.archive.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/virus/archive", params=params if params else None)
        return result

class DiskVirusRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVirusRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.virus.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/virus/raw", params=params if params else None)
        return result

class DiskVoipRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskVoipRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.voip.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/voip/raw", params=params if params else None)
        return result

class DiskWafRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWafRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.waf.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/waf/raw", params=params if params else None)
        return result

class DiskWebfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskWebfilterRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.webfilter.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/webfilter/raw", params=params if params else None)
        return result

class DiskAppCtrlArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskAppCtrlArchiveDownload."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.app_ctrl.archive.download.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/app-ctrl/archive/download", params=params if params else None)
        return result

class DiskEventComplianceCheckRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventComplianceCheckRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.compliance_check.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/compliance-check/raw", params=params if params else None)
        return result

class DiskEventConnectorRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventConnectorRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.connector.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/connector/raw", params=params if params else None)
        return result

class DiskEventEndpointRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventEndpointRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.endpoint.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/endpoint/raw", params=params if params else None)
        return result

class DiskEventFortiextenderRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventFortiextenderRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.fortiextender.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/fortiextender/raw", params=params if params else None)
        return result

class DiskEventHaRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventHaRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.ha.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/ha/raw", params=params if params else None)
        return result

class DiskEventRouterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventRouterRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.router.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/router/raw", params=params if params else None)
        return result

class DiskEventSecurityRatingRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventSecurityRatingRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.security_rating.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/security-rating/raw", params=params if params else None)
        return result

class DiskEventSystemRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventSystemRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.system.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/system/raw", params=params if params else None)
        return result

class DiskEventUserRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventUserRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.user.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/user/raw", params=params if params else None)
        return result

class DiskEventVpnRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventVpnRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.vpn.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/vpn/raw", params=params if params else None)
        return result

class DiskEventWadRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventWadRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.wad.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/wad/raw", params=params if params else None)
        return result

class DiskEventWirelessRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskEventWirelessRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.event.wireless.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/event/wireless/raw", params=params if params else None)
        return result

class DiskIpsArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskIpsArchiveDownload."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.ips.archive.download.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/ips/archive/download", params=params if params else None)
        return result

class DiskTrafficFortiviewRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficFortiviewRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.fortiview.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/fortiview/raw", params=params if params else None)
        return result

class DiskTrafficForwardRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficForwardRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.forward.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/forward/raw", params=params if params else None)
        return result

class DiskTrafficLocalRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficLocalRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.local.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/local/raw", params=params if params else None)
        return result

class DiskTrafficMulticastRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficMulticastRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.multicast.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/multicast/raw", params=params if params else None)
        return result

class DiskTrafficSnifferRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficSnifferRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.sniffer.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/sniffer/raw", params=params if params else None)
        return result

class DiskTrafficThreatRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize DiskTrafficThreatRaw."""
        self._client = client

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
            rows: Number of rows to return (default: server decides)
            session_id: Session ID for paginated retrieval (from previous response)
            serial_no: Retrieve logs from specific device serial number
            is_ha_member: Whether the device is an HA member
            filter: Filter expression (e.g., "srcip==192.168.1.1")
            extra: Extra data flags [reverse_lookup|country_id]
            vdom: Virtual domain (if not using default)

        Returns:
            FortiObjectList containing log records with metadata

        Example:
            >>> logs = fgt.api.log.disk.traffic.threat.raw.get(rows=100)
            >>> for log in logs:
            ...     print(log.srcip, log.dstip)
        """
        params: dict[str, Any] = {}
        if rows is not None:
            params["rows"] = rows
        if session_id is not None:
            params["session_id"] = session_id
        if serial_no is not None:
            params["serial_no"] = serial_no
        if is_ha_member is not None:
            params["is_ha_member"] = is_ha_member
        if filter is not None:
            params["filter"] = filter
        if extra is not None:
            params["extra"] = extra
        if vdom is not None:
            params["vdom"] = vdom

        result = self._client.get("log", "disk/traffic/threat/raw", params=params if params else None)
        return result
