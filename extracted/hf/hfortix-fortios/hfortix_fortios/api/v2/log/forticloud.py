"""
FortiOS LOG API - Forticloud

Log query endpoints for forticloud logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They use nested classes to represent path parameters.

Example Usage:
    >>> fgt.api.log.forticloud.anomaly.get(rows=100)
    >>> fgt.api.log.forticloud.app_ctrl.get(rows=100)
    >>> fgt.api.log.forticloud.cifs.get(rows=100)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Forticloud:
    """Forticloud log operations.
    
    Provides access to forticloud log endpoints with nested classes
    for different log types and subtypes.
    """

    def __init__(self, client: "IHTTPClient"):
        """Initialize Forticloud endpoint."""
        self._client = client
        self.anomaly = ForticloudAnomaly(client)
        self.app_ctrl = ForticloudAppCtrl(client)
        self.cifs = ForticloudCifs(client)
        self.dlp = ForticloudDlp(client)
        self.dns = ForticloudDns(client)
        self.emailfilter = ForticloudEmailfilter(client)
        self.event = ForticloudEvent(client)
        self.file_filter = ForticloudFileFilter(client)
        self.gtp = ForticloudGtp(client)
        self.ips = ForticloudIps(client)
        self.ssh = ForticloudSsh(client)
        self.ssl = ForticloudSsl(client)
        self.traffic = ForticloudTraffic(client)
        self.virus = ForticloudVirus(client)
        self.voip = ForticloudVoip(client)
        self.waf = ForticloudWaf(client)
        self.webfilter = ForticloudWebfilter(client)


class ForticloudAnomaly:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAnomaly."""
        self._client = client
        self.raw = ForticloudAnomalyRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.anomaly.get(rows=100)
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

        result = self._client.get("log", "forticloud/anomaly", params=params if params else None)
        return result

class ForticloudAppCtrl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAppCtrl."""
        self._client = client
        self.archive = ForticloudAppCtrlArchive(client)
        self.raw = ForticloudAppCtrlRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.app_ctrl.get(rows=100)
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

        result = self._client.get("log", "forticloud/app-ctrl", params=params if params else None)
        return result

class ForticloudCifs:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudCifs."""
        self._client = client
        self.raw = ForticloudCifsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.cifs.get(rows=100)
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

        result = self._client.get("log", "forticloud/cifs", params=params if params else None)
        return result

class ForticloudDlp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDlp."""
        self._client = client
        self.raw = ForticloudDlpRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.dlp.get(rows=100)
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

        result = self._client.get("log", "forticloud/dlp", params=params if params else None)
        return result

class ForticloudDns:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDns."""
        self._client = client
        self.raw = ForticloudDnsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.dns.get(rows=100)
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

        result = self._client.get("log", "forticloud/dns", params=params if params else None)
        return result

class ForticloudEmailfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEmailfilter."""
        self._client = client
        self.raw = ForticloudEmailfilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.emailfilter.get(rows=100)
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

        result = self._client.get("log", "forticloud/emailfilter", params=params if params else None)
        return result

class ForticloudEvent:
    """ForticloudEvent log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEvent."""
        self._client = client
        self.compliance_check = ForticloudEventComplianceCheck(client)
        self.connector = ForticloudEventConnector(client)
        self.endpoint = ForticloudEventEndpoint(client)
        self.fortiextender = ForticloudEventFortiextender(client)
        self.ha = ForticloudEventHa(client)
        self.router = ForticloudEventRouter(client)
        self.security_rating = ForticloudEventSecurityRating(client)
        self.system = ForticloudEventSystem(client)
        self.user = ForticloudEventUser(client)
        self.vpn = ForticloudEventVpn(client)
        self.wad = ForticloudEventWad(client)
        self.wireless = ForticloudEventWireless(client)

class ForticloudFileFilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudFileFilter."""
        self._client = client
        self.raw = ForticloudFileFilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.file_filter.get(rows=100)
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

        result = self._client.get("log", "forticloud/file-filter", params=params if params else None)
        return result

class ForticloudGtp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudGtp."""
        self._client = client
        self.raw = ForticloudGtpRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.gtp.get(rows=100)
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

        result = self._client.get("log", "forticloud/gtp", params=params if params else None)
        return result

class ForticloudIps:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudIps."""
        self._client = client
        self.archive = ForticloudIpsArchive(client)
        self.raw = ForticloudIpsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.ips.get(rows=100)
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

        result = self._client.get("log", "forticloud/ips", params=params if params else None)
        return result

class ForticloudSsh:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSsh."""
        self._client = client
        self.raw = ForticloudSshRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.ssh.get(rows=100)
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

        result = self._client.get("log", "forticloud/ssh", params=params if params else None)
        return result

class ForticloudSsl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSsl."""
        self._client = client
        self.raw = ForticloudSslRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.ssl.get(rows=100)
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

        result = self._client.get("log", "forticloud/ssl", params=params if params else None)
        return result

class ForticloudTraffic:
    """ForticloudTraffic log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTraffic."""
        self._client = client
        self.fortiview = ForticloudTrafficFortiview(client)
        self.forward = ForticloudTrafficForward(client)
        self.local = ForticloudTrafficLocal(client)
        self.multicast = ForticloudTrafficMulticast(client)
        self.sniffer = ForticloudTrafficSniffer(client)
        self.threat = ForticloudTrafficThreat(client)

class ForticloudVirus:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVirus."""
        self._client = client
        self.archive = ForticloudVirusArchive(client)
        self.raw = ForticloudVirusRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.virus.get(rows=100)
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

        result = self._client.get("log", "forticloud/virus", params=params if params else None)
        return result

class ForticloudVoip:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVoip."""
        self._client = client
        self.raw = ForticloudVoipRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.voip.get(rows=100)
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

        result = self._client.get("log", "forticloud/voip", params=params if params else None)
        return result

class ForticloudWaf:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWaf."""
        self._client = client
        self.raw = ForticloudWafRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.waf.get(rows=100)
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

        result = self._client.get("log", "forticloud/waf", params=params if params else None)
        return result

class ForticloudWebfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWebfilter."""
        self._client = client
        self.raw = ForticloudWebfilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.webfilter.get(rows=100)
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

        result = self._client.get("log", "forticloud/webfilter", params=params if params else None)
        return result

class ForticloudAnomalyRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAnomalyRaw."""
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
            >>> logs = fgt.api.log.forticloud.anomaly.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/anomaly/raw", params=params if params else None)
        return result

class ForticloudAppCtrlArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAppCtrlArchive."""
        self._client = client
        self.download = ForticloudAppCtrlArchiveDownload(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.app_ctrl.archive.get(rows=100)
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

        result = self._client.get("log", "forticloud/app-ctrl/archive", params=params if params else None)
        return result

class ForticloudAppCtrlRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAppCtrlRaw."""
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
            >>> logs = fgt.api.log.forticloud.app_ctrl.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/app-ctrl/raw", params=params if params else None)
        return result

class ForticloudCifsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudCifsRaw."""
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
            >>> logs = fgt.api.log.forticloud.cifs.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/cifs/raw", params=params if params else None)
        return result

class ForticloudDlpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDlpRaw."""
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
            >>> logs = fgt.api.log.forticloud.dlp.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/dlp/raw", params=params if params else None)
        return result

class ForticloudDnsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudDnsRaw."""
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
            >>> logs = fgt.api.log.forticloud.dns.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/dns/raw", params=params if params else None)
        return result

class ForticloudEmailfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEmailfilterRaw."""
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
            >>> logs = fgt.api.log.forticloud.emailfilter.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/emailfilter/raw", params=params if params else None)
        return result

class ForticloudEventComplianceCheck:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventComplianceCheck."""
        self._client = client
        self.raw = ForticloudEventComplianceCheckRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.compliance_check.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/compliance-check", params=params if params else None)
        return result

class ForticloudEventConnector:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventConnector."""
        self._client = client
        self.raw = ForticloudEventConnectorRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.connector.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/connector", params=params if params else None)
        return result

class ForticloudEventEndpoint:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventEndpoint."""
        self._client = client
        self.raw = ForticloudEventEndpointRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.endpoint.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/endpoint", params=params if params else None)
        return result

class ForticloudEventFortiextender:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventFortiextender."""
        self._client = client
        self.raw = ForticloudEventFortiextenderRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.fortiextender.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/fortiextender", params=params if params else None)
        return result

class ForticloudEventHa:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventHa."""
        self._client = client
        self.raw = ForticloudEventHaRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.ha.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/ha", params=params if params else None)
        return result

class ForticloudEventRouter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventRouter."""
        self._client = client
        self.raw = ForticloudEventRouterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.router.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/router", params=params if params else None)
        return result

class ForticloudEventSecurityRating:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventSecurityRating."""
        self._client = client
        self.raw = ForticloudEventSecurityRatingRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.security_rating.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/security-rating", params=params if params else None)
        return result

class ForticloudEventSystem:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventSystem."""
        self._client = client
        self.raw = ForticloudEventSystemRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.system.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/system", params=params if params else None)
        return result

class ForticloudEventUser:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventUser."""
        self._client = client
        self.raw = ForticloudEventUserRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.user.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/user", params=params if params else None)
        return result

class ForticloudEventVpn:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventVpn."""
        self._client = client
        self.raw = ForticloudEventVpnRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.vpn.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/vpn", params=params if params else None)
        return result

class ForticloudEventWad:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventWad."""
        self._client = client
        self.raw = ForticloudEventWadRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.wad.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/wad", params=params if params else None)
        return result

class ForticloudEventWireless:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventWireless."""
        self._client = client
        self.raw = ForticloudEventWirelessRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.event.wireless.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/wireless", params=params if params else None)
        return result

class ForticloudFileFilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudFileFilterRaw."""
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
            >>> logs = fgt.api.log.forticloud.file_filter.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/file-filter/raw", params=params if params else None)
        return result

class ForticloudGtpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudGtpRaw."""
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
            >>> logs = fgt.api.log.forticloud.gtp.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/gtp/raw", params=params if params else None)
        return result

class ForticloudIpsArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudIpsArchive."""
        self._client = client
        self.download = ForticloudIpsArchiveDownload(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.ips.archive.get(rows=100)
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

        result = self._client.get("log", "forticloud/ips/archive", params=params if params else None)
        return result

class ForticloudIpsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudIpsRaw."""
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
            >>> logs = fgt.api.log.forticloud.ips.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/ips/raw", params=params if params else None)
        return result

class ForticloudSshRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSshRaw."""
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
            >>> logs = fgt.api.log.forticloud.ssh.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/ssh/raw", params=params if params else None)
        return result

class ForticloudSslRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudSslRaw."""
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
            >>> logs = fgt.api.log.forticloud.ssl.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/ssl/raw", params=params if params else None)
        return result

class ForticloudTrafficFortiview:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficFortiview."""
        self._client = client
        self.raw = ForticloudTrafficFortiviewRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.fortiview.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/fortiview", params=params if params else None)
        return result

class ForticloudTrafficForward:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficForward."""
        self._client = client
        self.raw = ForticloudTrafficForwardRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.forward.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/forward", params=params if params else None)
        return result

class ForticloudTrafficLocal:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficLocal."""
        self._client = client
        self.raw = ForticloudTrafficLocalRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.local.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/local", params=params if params else None)
        return result

class ForticloudTrafficMulticast:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficMulticast."""
        self._client = client
        self.raw = ForticloudTrafficMulticastRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.multicast.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/multicast", params=params if params else None)
        return result

class ForticloudTrafficSniffer:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficSniffer."""
        self._client = client
        self.raw = ForticloudTrafficSnifferRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.sniffer.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/sniffer", params=params if params else None)
        return result

class ForticloudTrafficThreat:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficThreat."""
        self._client = client
        self.raw = ForticloudTrafficThreatRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.forticloud.traffic.threat.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/threat", params=params if params else None)
        return result

class ForticloudVirusArchive:
    """Return a description of the quarantined virus file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVirusArchive."""
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
            >>> logs = fgt.api.log.forticloud.virus.archive.get(rows=100)
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

        result = self._client.get("log", "forticloud/virus/archive", params=params if params else None)
        return result

class ForticloudVirusRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVirusRaw."""
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
            >>> logs = fgt.api.log.forticloud.virus.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/virus/raw", params=params if params else None)
        return result

class ForticloudVoipRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudVoipRaw."""
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
            >>> logs = fgt.api.log.forticloud.voip.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/voip/raw", params=params if params else None)
        return result

class ForticloudWafRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWafRaw."""
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
            >>> logs = fgt.api.log.forticloud.waf.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/waf/raw", params=params if params else None)
        return result

class ForticloudWebfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudWebfilterRaw."""
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
            >>> logs = fgt.api.log.forticloud.webfilter.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/webfilter/raw", params=params if params else None)
        return result

class ForticloudAppCtrlArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudAppCtrlArchiveDownload."""
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
            >>> logs = fgt.api.log.forticloud.app_ctrl.archive.download.get(rows=100)
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

        result = self._client.get("log", "forticloud/app-ctrl/archive/download", params=params if params else None)
        return result

class ForticloudEventComplianceCheckRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventComplianceCheckRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.compliance_check.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/compliance-check/raw", params=params if params else None)
        return result

class ForticloudEventConnectorRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventConnectorRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.connector.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/connector/raw", params=params if params else None)
        return result

class ForticloudEventEndpointRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventEndpointRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.endpoint.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/endpoint/raw", params=params if params else None)
        return result

class ForticloudEventFortiextenderRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventFortiextenderRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.fortiextender.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/fortiextender/raw", params=params if params else None)
        return result

class ForticloudEventHaRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventHaRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.ha.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/ha/raw", params=params if params else None)
        return result

class ForticloudEventRouterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventRouterRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.router.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/router/raw", params=params if params else None)
        return result

class ForticloudEventSecurityRatingRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventSecurityRatingRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.security_rating.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/security-rating/raw", params=params if params else None)
        return result

class ForticloudEventSystemRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventSystemRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.system.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/system/raw", params=params if params else None)
        return result

class ForticloudEventUserRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventUserRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.user.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/user/raw", params=params if params else None)
        return result

class ForticloudEventVpnRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventVpnRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.vpn.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/vpn/raw", params=params if params else None)
        return result

class ForticloudEventWadRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventWadRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.wad.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/wad/raw", params=params if params else None)
        return result

class ForticloudEventWirelessRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudEventWirelessRaw."""
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
            >>> logs = fgt.api.log.forticloud.event.wireless.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/event/wireless/raw", params=params if params else None)
        return result

class ForticloudIpsArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudIpsArchiveDownload."""
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
            >>> logs = fgt.api.log.forticloud.ips.archive.download.get(rows=100)
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

        result = self._client.get("log", "forticloud/ips/archive/download", params=params if params else None)
        return result

class ForticloudTrafficFortiviewRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficFortiviewRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.fortiview.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/fortiview/raw", params=params if params else None)
        return result

class ForticloudTrafficForwardRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficForwardRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.forward.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/forward/raw", params=params if params else None)
        return result

class ForticloudTrafficLocalRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficLocalRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.local.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/local/raw", params=params if params else None)
        return result

class ForticloudTrafficMulticastRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficMulticastRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.multicast.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/multicast/raw", params=params if params else None)
        return result

class ForticloudTrafficSnifferRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficSnifferRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.sniffer.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/sniffer/raw", params=params if params else None)
        return result

class ForticloudTrafficThreatRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize ForticloudTrafficThreatRaw."""
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
            >>> logs = fgt.api.log.forticloud.traffic.threat.raw.get(rows=100)
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

        result = self._client.get("log", "forticloud/traffic/threat/raw", params=params if params else None)
        return result
