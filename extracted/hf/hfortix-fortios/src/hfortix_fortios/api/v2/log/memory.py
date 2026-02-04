"""
FortiOS LOG API - Memory

Log query endpoints for memory logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They use nested classes to represent path parameters.

Example Usage:
    >>> fgt.api.log.memory.anomaly.get(rows=100)
    >>> fgt.api.log.memory.app_ctrl.get(rows=100)
    >>> fgt.api.log.memory.cifs.get(rows=100)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient

from hfortix_fortios.models import FortiObjectList


class Memory:
    """Memory log operations.
    
    Provides access to memory log endpoints with nested classes
    for different log types and subtypes.
    """

    def __init__(self, client: "IHTTPClient"):
        """Initialize Memory endpoint."""
        self._client = client
        self.anomaly = MemoryAnomaly(client)
        self.app_ctrl = MemoryAppCtrl(client)
        self.cifs = MemoryCifs(client)
        self.dlp = MemoryDlp(client)
        self.dns = MemoryDns(client)
        self.emailfilter = MemoryEmailfilter(client)
        self.event = MemoryEvent(client)
        self.file_filter = MemoryFileFilter(client)
        self.gtp = MemoryGtp(client)
        self.ips = MemoryIps(client)
        self.ssh = MemorySsh(client)
        self.ssl = MemorySsl(client)
        self.traffic = MemoryTraffic(client)
        self.virus = MemoryVirus(client)
        self.voip = MemoryVoip(client)
        self.waf = MemoryWaf(client)
        self.webfilter = MemoryWebfilter(client)


class MemoryAnomaly:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAnomaly."""
        self._client = client
        self.raw = MemoryAnomalyRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.anomaly.get(rows=100)
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

        result = self._client.get("log", "memory/anomaly", params=params if params else None)
        return result

class MemoryAppCtrl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAppCtrl."""
        self._client = client
        self.archive = MemoryAppCtrlArchive(client)
        self.raw = MemoryAppCtrlRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.app_ctrl.get(rows=100)
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

        result = self._client.get("log", "memory/app-ctrl", params=params if params else None)
        return result

class MemoryCifs:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryCifs."""
        self._client = client
        self.raw = MemoryCifsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.cifs.get(rows=100)
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

        result = self._client.get("log", "memory/cifs", params=params if params else None)
        return result

class MemoryDlp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDlp."""
        self._client = client
        self.raw = MemoryDlpRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.dlp.get(rows=100)
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

        result = self._client.get("log", "memory/dlp", params=params if params else None)
        return result

class MemoryDns:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDns."""
        self._client = client
        self.raw = MemoryDnsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.dns.get(rows=100)
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

        result = self._client.get("log", "memory/dns", params=params if params else None)
        return result

class MemoryEmailfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEmailfilter."""
        self._client = client
        self.raw = MemoryEmailfilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.emailfilter.get(rows=100)
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

        result = self._client.get("log", "memory/emailfilter", params=params if params else None)
        return result

class MemoryEvent:
    """MemoryEvent log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEvent."""
        self._client = client
        self.compliance_check = MemoryEventComplianceCheck(client)
        self.connector = MemoryEventConnector(client)
        self.endpoint = MemoryEventEndpoint(client)
        self.fortiextender = MemoryEventFortiextender(client)
        self.ha = MemoryEventHa(client)
        self.router = MemoryEventRouter(client)
        self.security_rating = MemoryEventSecurityRating(client)
        self.system = MemoryEventSystem(client)
        self.user = MemoryEventUser(client)
        self.vpn = MemoryEventVpn(client)
        self.wad = MemoryEventWad(client)
        self.wireless = MemoryEventWireless(client)

class MemoryFileFilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryFileFilter."""
        self._client = client
        self.raw = MemoryFileFilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.file_filter.get(rows=100)
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

        result = self._client.get("log", "memory/file-filter", params=params if params else None)
        return result

class MemoryGtp:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryGtp."""
        self._client = client
        self.raw = MemoryGtpRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.gtp.get(rows=100)
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

        result = self._client.get("log", "memory/gtp", params=params if params else None)
        return result

class MemoryIps:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryIps."""
        self._client = client
        self.archive = MemoryIpsArchive(client)
        self.raw = MemoryIpsRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.ips.get(rows=100)
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

        result = self._client.get("log", "memory/ips", params=params if params else None)
        return result

class MemorySsh:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySsh."""
        self._client = client
        self.raw = MemorySshRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.ssh.get(rows=100)
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

        result = self._client.get("log", "memory/ssh", params=params if params else None)
        return result

class MemorySsl:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySsl."""
        self._client = client
        self.raw = MemorySslRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.ssl.get(rows=100)
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

        result = self._client.get("log", "memory/ssl", params=params if params else None)
        return result

class MemoryTraffic:
    """MemoryTraffic log category."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTraffic."""
        self._client = client
        self.fortiview = MemoryTrafficFortiview(client)
        self.forward = MemoryTrafficForward(client)
        self.local = MemoryTrafficLocal(client)
        self.multicast = MemoryTrafficMulticast(client)
        self.sniffer = MemoryTrafficSniffer(client)
        self.threat = MemoryTrafficThreat(client)

class MemoryVirus:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVirus."""
        self._client = client
        self.archive = MemoryVirusArchive(client)
        self.raw = MemoryVirusRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.virus.get(rows=100)
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

        result = self._client.get("log", "memory/virus", params=params if params else None)
        return result

class MemoryVoip:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVoip."""
        self._client = client
        self.raw = MemoryVoipRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.voip.get(rows=100)
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

        result = self._client.get("log", "memory/voip", params=params if params else None)
        return result

class MemoryWaf:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWaf."""
        self._client = client
        self.raw = MemoryWafRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.waf.get(rows=100)
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

        result = self._client.get("log", "memory/waf", params=params if params else None)
        return result

class MemoryWebfilter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWebfilter."""
        self._client = client
        self.raw = MemoryWebfilterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.webfilter.get(rows=100)
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

        result = self._client.get("log", "memory/webfilter", params=params if params else None)
        return result

class MemoryAnomalyRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAnomalyRaw."""
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
            >>> logs = fgt.api.log.memory.anomaly.raw.get(rows=100)
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

        result = self._client.get("log", "memory/anomaly/raw", params=params if params else None)
        return result

class MemoryAppCtrlArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAppCtrlArchive."""
        self._client = client
        self.download = MemoryAppCtrlArchiveDownload(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.app_ctrl.archive.get(rows=100)
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

        result = self._client.get("log", "memory/app-ctrl/archive", params=params if params else None)
        return result

class MemoryAppCtrlRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAppCtrlRaw."""
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
            >>> logs = fgt.api.log.memory.app_ctrl.raw.get(rows=100)
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

        result = self._client.get("log", "memory/app-ctrl/raw", params=params if params else None)
        return result

class MemoryCifsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryCifsRaw."""
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
            >>> logs = fgt.api.log.memory.cifs.raw.get(rows=100)
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

        result = self._client.get("log", "memory/cifs/raw", params=params if params else None)
        return result

class MemoryDlpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDlpRaw."""
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
            >>> logs = fgt.api.log.memory.dlp.raw.get(rows=100)
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

        result = self._client.get("log", "memory/dlp/raw", params=params if params else None)
        return result

class MemoryDnsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryDnsRaw."""
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
            >>> logs = fgt.api.log.memory.dns.raw.get(rows=100)
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

        result = self._client.get("log", "memory/dns/raw", params=params if params else None)
        return result

class MemoryEmailfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEmailfilterRaw."""
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
            >>> logs = fgt.api.log.memory.emailfilter.raw.get(rows=100)
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

        result = self._client.get("log", "memory/emailfilter/raw", params=params if params else None)
        return result

class MemoryEventComplianceCheck:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventComplianceCheck."""
        self._client = client
        self.raw = MemoryEventComplianceCheckRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.compliance_check.get(rows=100)
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

        result = self._client.get("log", "memory/event/compliance-check", params=params if params else None)
        return result

class MemoryEventConnector:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventConnector."""
        self._client = client
        self.raw = MemoryEventConnectorRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.connector.get(rows=100)
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

        result = self._client.get("log", "memory/event/connector", params=params if params else None)
        return result

class MemoryEventEndpoint:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventEndpoint."""
        self._client = client
        self.raw = MemoryEventEndpointRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.endpoint.get(rows=100)
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

        result = self._client.get("log", "memory/event/endpoint", params=params if params else None)
        return result

class MemoryEventFortiextender:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventFortiextender."""
        self._client = client
        self.raw = MemoryEventFortiextenderRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.fortiextender.get(rows=100)
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

        result = self._client.get("log", "memory/event/fortiextender", params=params if params else None)
        return result

class MemoryEventHa:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventHa."""
        self._client = client
        self.raw = MemoryEventHaRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.ha.get(rows=100)
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

        result = self._client.get("log", "memory/event/ha", params=params if params else None)
        return result

class MemoryEventRouter:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventRouter."""
        self._client = client
        self.raw = MemoryEventRouterRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.router.get(rows=100)
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

        result = self._client.get("log", "memory/event/router", params=params if params else None)
        return result

class MemoryEventSecurityRating:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventSecurityRating."""
        self._client = client
        self.raw = MemoryEventSecurityRatingRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.security_rating.get(rows=100)
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

        result = self._client.get("log", "memory/event/security-rating", params=params if params else None)
        return result

class MemoryEventSystem:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventSystem."""
        self._client = client
        self.raw = MemoryEventSystemRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.system.get(rows=100)
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

        result = self._client.get("log", "memory/event/system", params=params if params else None)
        return result

class MemoryEventUser:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventUser."""
        self._client = client
        self.raw = MemoryEventUserRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.user.get(rows=100)
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

        result = self._client.get("log", "memory/event/user", params=params if params else None)
        return result

class MemoryEventVpn:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventVpn."""
        self._client = client
        self.raw = MemoryEventVpnRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.vpn.get(rows=100)
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

        result = self._client.get("log", "memory/event/vpn", params=params if params else None)
        return result

class MemoryEventWad:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventWad."""
        self._client = client
        self.raw = MemoryEventWadRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.wad.get(rows=100)
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

        result = self._client.get("log", "memory/event/wad", params=params if params else None)
        return result

class MemoryEventWireless:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventWireless."""
        self._client = client
        self.raw = MemoryEventWirelessRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.event.wireless.get(rows=100)
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

        result = self._client.get("log", "memory/event/wireless", params=params if params else None)
        return result

class MemoryFileFilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryFileFilterRaw."""
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
            >>> logs = fgt.api.log.memory.file_filter.raw.get(rows=100)
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

        result = self._client.get("log", "memory/file-filter/raw", params=params if params else None)
        return result

class MemoryGtpRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryGtpRaw."""
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
            >>> logs = fgt.api.log.memory.gtp.raw.get(rows=100)
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

        result = self._client.get("log", "memory/gtp/raw", params=params if params else None)
        return result

class MemoryIpsArchive:
    """Return a list of archived items for the desired type."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryIpsArchive."""
        self._client = client
        self.download = MemoryIpsArchiveDownload(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.ips.archive.get(rows=100)
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

        result = self._client.get("log", "memory/ips/archive", params=params if params else None)
        return result

class MemoryIpsRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryIpsRaw."""
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
            >>> logs = fgt.api.log.memory.ips.raw.get(rows=100)
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

        result = self._client.get("log", "memory/ips/raw", params=params if params else None)
        return result

class MemorySshRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySshRaw."""
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
            >>> logs = fgt.api.log.memory.ssh.raw.get(rows=100)
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

        result = self._client.get("log", "memory/ssh/raw", params=params if params else None)
        return result

class MemorySslRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemorySslRaw."""
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
            >>> logs = fgt.api.log.memory.ssl.raw.get(rows=100)
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

        result = self._client.get("log", "memory/ssl/raw", params=params if params else None)
        return result

class MemoryTrafficFortiview:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficFortiview."""
        self._client = client
        self.raw = MemoryTrafficFortiviewRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.fortiview.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/fortiview", params=params if params else None)
        return result

class MemoryTrafficForward:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficForward."""
        self._client = client
        self.raw = MemoryTrafficForwardRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.forward.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/forward", params=params if params else None)
        return result

class MemoryTrafficLocal:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficLocal."""
        self._client = client
        self.raw = MemoryTrafficLocalRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.local.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/local", params=params if params else None)
        return result

class MemoryTrafficMulticast:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficMulticast."""
        self._client = client
        self.raw = MemoryTrafficMulticastRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.multicast.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/multicast", params=params if params else None)
        return result

class MemoryTrafficSniffer:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficSniffer."""
        self._client = client
        self.raw = MemoryTrafficSnifferRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.sniffer.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/sniffer", params=params if params else None)
        return result

class MemoryTrafficThreat:
    """Log data for the given log type (and subtype)."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficThreat."""
        self._client = client
        self.raw = MemoryTrafficThreatRaw(client)

    def get(
        self,
        *,
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
            >>> logs = fgt.api.log.memory.traffic.threat.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/threat", params=params if params else None)
        return result

class MemoryVirusArchive:
    """Return a description of the quarantined virus file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVirusArchive."""
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
            >>> logs = fgt.api.log.memory.virus.archive.get(rows=100)
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

        result = self._client.get("log", "memory/virus/archive", params=params if params else None)
        return result

class MemoryVirusRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVirusRaw."""
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
            >>> logs = fgt.api.log.memory.virus.raw.get(rows=100)
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

        result = self._client.get("log", "memory/virus/raw", params=params if params else None)
        return result

class MemoryVoipRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryVoipRaw."""
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
            >>> logs = fgt.api.log.memory.voip.raw.get(rows=100)
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

        result = self._client.get("log", "memory/voip/raw", params=params if params else None)
        return result

class MemoryWafRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWafRaw."""
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
            >>> logs = fgt.api.log.memory.waf.raw.get(rows=100)
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

        result = self._client.get("log", "memory/waf/raw", params=params if params else None)
        return result

class MemoryWebfilterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryWebfilterRaw."""
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
            >>> logs = fgt.api.log.memory.webfilter.raw.get(rows=100)
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

        result = self._client.get("log", "memory/webfilter/raw", params=params if params else None)
        return result

class MemoryAppCtrlArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryAppCtrlArchiveDownload."""
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
            >>> logs = fgt.api.log.memory.app_ctrl.archive.download.get(rows=100)
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

        result = self._client.get("log", "memory/app-ctrl/archive/download", params=params if params else None)
        return result

class MemoryEventComplianceCheckRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventComplianceCheckRaw."""
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
            >>> logs = fgt.api.log.memory.event.compliance_check.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/compliance-check/raw", params=params if params else None)
        return result

class MemoryEventConnectorRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventConnectorRaw."""
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
            >>> logs = fgt.api.log.memory.event.connector.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/connector/raw", params=params if params else None)
        return result

class MemoryEventEndpointRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventEndpointRaw."""
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
            >>> logs = fgt.api.log.memory.event.endpoint.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/endpoint/raw", params=params if params else None)
        return result

class MemoryEventFortiextenderRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventFortiextenderRaw."""
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
            >>> logs = fgt.api.log.memory.event.fortiextender.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/fortiextender/raw", params=params if params else None)
        return result

class MemoryEventHaRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventHaRaw."""
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
            >>> logs = fgt.api.log.memory.event.ha.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/ha/raw", params=params if params else None)
        return result

class MemoryEventRouterRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventRouterRaw."""
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
            >>> logs = fgt.api.log.memory.event.router.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/router/raw", params=params if params else None)
        return result

class MemoryEventSecurityRatingRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventSecurityRatingRaw."""
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
            >>> logs = fgt.api.log.memory.event.security_rating.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/security-rating/raw", params=params if params else None)
        return result

class MemoryEventSystemRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventSystemRaw."""
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
            >>> logs = fgt.api.log.memory.event.system.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/system/raw", params=params if params else None)
        return result

class MemoryEventUserRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventUserRaw."""
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
            >>> logs = fgt.api.log.memory.event.user.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/user/raw", params=params if params else None)
        return result

class MemoryEventVpnRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventVpnRaw."""
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
            >>> logs = fgt.api.log.memory.event.vpn.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/vpn/raw", params=params if params else None)
        return result

class MemoryEventWadRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventWadRaw."""
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
            >>> logs = fgt.api.log.memory.event.wad.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/wad/raw", params=params if params else None)
        return result

class MemoryEventWirelessRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryEventWirelessRaw."""
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
            >>> logs = fgt.api.log.memory.event.wireless.raw.get(rows=100)
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

        result = self._client.get("log", "memory/event/wireless/raw", params=params if params else None)
        return result

class MemoryIpsArchiveDownload:
    """Download an archived file."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryIpsArchiveDownload."""
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
            >>> logs = fgt.api.log.memory.ips.archive.download.get(rows=100)
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

        result = self._client.get("log", "memory/ips/archive/download", params=params if params else None)
        return result

class MemoryTrafficFortiviewRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficFortiviewRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.fortiview.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/fortiview/raw", params=params if params else None)
        return result

class MemoryTrafficForwardRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficForwardRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.forward.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/forward/raw", params=params if params else None)
        return result

class MemoryTrafficLocalRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficLocalRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.local.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/local/raw", params=params if params else None)
        return result

class MemoryTrafficMulticastRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficMulticastRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.multicast.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/multicast/raw", params=params if params else None)
        return result

class MemoryTrafficSnifferRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficSnifferRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.sniffer.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/sniffer/raw", params=params if params else None)
        return result

class MemoryTrafficThreatRaw:
    """Log data for the given log type in raw format."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize MemoryTrafficThreatRaw."""
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
            >>> logs = fgt.api.log.memory.traffic.threat.raw.get(rows=100)
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

        result = self._client.get("log", "memory/traffic/threat/raw", params=params if params else None)
        return result
