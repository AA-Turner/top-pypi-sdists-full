"""
FortiManager Proxy Response Models

Data classes for FMG proxy responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeviceResult:
    """
    Result from a single device in a proxy response.
    
    Attributes:
        target: Device name (e.g., "firewall-01")
        response: The FortiOS API response dict
        status: FMG status dict with code and message
    """
    target: str
    response: dict[str, Any]
    # All fields with defaults must come after required fields
    status: dict[str, Any] = field(default_factory=lambda: {"code": 0, "message": "OK"})
    fmg_proxy_status_code: int | None = None
    fmg_proxy_status_message: str | None = None
    fmg_proxy_target: str | None = None
    fmg_proxy_url: str | None = None
    fmg_url: str | None = None
    fmg_status_code: int | None = None
    fmg_status_message: str | None = None
    fmg_id: int | None = None
    fmg_raw: dict[str, Any] | None = None
    
    @property
    def success(self) -> bool:
        """Check if the request was successful."""
        return self.status.get("code") == 0
    
    @property
    def failed(self) -> bool:
        """Check if the request failed."""
        return not self.success
    
    @property
    def http_status(self) -> int | None:
        """HTTP status code from the FortiOS response."""
        return self.response.get("http_status")
    
    @property
    def results(self) -> Any:
        """Results data from the FortiOS response."""
        return self.response.get("results")


@dataclass
class ProxyResponse:
    fmg_raw: dict[str, Any] | None = None
    """
    Response from a FortiManager proxy request.
    
    Contains results from one or more devices.
    
    Attributes:
        data: List of DeviceResult objects
        status: Overall FMG status
        url: The FMG API URL used
    """
    data: list[DeviceResult] = field(default_factory=list)
    status: dict[str, Any] = field(default_factory=lambda: {"code": 0, "message": "OK"})
    url: str = "/sys/proxy/json"
    # FMG proxy fields (top-level)
    fmg_proxy_status_code: int | None = None
    fmg_proxy_status_message: str | None = None
    fmg_proxy_url: str | None = None
    fmg_url: str | None = None
    fmg_id: int | None = None
    
    def __iter__(self):
        """Iterate over device results."""
        return iter(self.data)
    
    def __len__(self) -> int:
        """Number of device results."""
        return len(self.data)
    
    def __getitem__(self, index: int) -> DeviceResult:
        """Get device result by index."""
        return self.data[index]
    
    @property
    def success(self) -> bool:
        """Check if all device requests were successful."""
        return self.status.get("code") == 0 and all(d.success for d in self.data)
    
    @property
    def success_count(self) -> int:
        """Count of successful device results."""
        return sum(1 for d in self.data if d.success)
    
    @property
    def failed_count(self) -> int:
        """Count of failed device results."""
        return sum(1 for d in self.data if d.failed)
    
    @property
    def first(self) -> DeviceResult | None:
        """Get the first device result (convenience for single-device requests)."""
        return self.data[0] if self.data else None
    
    @classmethod
    def from_fmg_response(cls, response: dict[str, Any]) -> "ProxyResponse":
        """
        Parse a FortiManager JSON-RPC response into a ProxyResponse.
        Args:
            response: Raw FMG response dict
        Returns:
            ProxyResponse object
        """
        result = response.get("result", [{}])[0]
        fmg_id = response.get("id")
        fmg_proxy_status = result.get("status", {})
        fmg_proxy_status_code = fmg_proxy_status.get("code")
        fmg_proxy_status_message = fmg_proxy_status.get("message")
        device_results = []
        fmg_proxy_url = result.get("url", "/sys/proxy/json")
        fmg_url = None
        for item in result.get("data", []):
            raw_response = item.get("response", {})
            # Handle non-dict responses (e.g., HTML error pages from FortiGate)
            if isinstance(raw_response, str):
                if raw_response.strip().startswith("<!DOCTYPE") or raw_response.strip().startswith("<html"):
                    raw_response = {
                        "status": "error",
                        "http_status": 404,
                        "error": "Endpoint not found",
                        "message": "The FortiGate returned an HTML error page. This endpoint may not exist on this device or firmware version.",
                        "raw_html": raw_response,
                        "results": [],
                    }
                else:
                    raw_response = {
                        "status": "error",
                        "http_status": 500,
                        "error": "Unexpected response format",
                        "message": raw_response,
                        "results": [],
                    }
            elif not isinstance(raw_response, dict):
                raw_response = {
                    "status": "error",
                    "http_status": 500,
                    "error": "Unexpected response type",
                    "message": str(raw_response),
                    "results": [],
                }
            # FMG status for this device
            device_status = item.get("status", {"code": -1, "message": "Unknown"})
            device_result = DeviceResult(
                target=item.get("target", "unknown"),
                response=raw_response,
                status=device_status,
                fmg_proxy_status_code=fmg_proxy_status_code,
                fmg_proxy_status_message=fmg_proxy_status_message,
                fmg_proxy_target=item.get("target"),
                fmg_proxy_url=fmg_proxy_url,
                fmg_url=item.get("url"),
                fmg_status_code=device_status.get("code"),
                fmg_status_message=device_status.get("message"),
                fmg_id=fmg_id,
                fmg_raw=item,
            )
            device_results.append(device_result)
            if not fmg_url and item.get("url"):
                fmg_url = item.get("url")
        return cls(
            data=device_results,
            status=fmg_proxy_status,
            url=fmg_proxy_url,
            fmg_proxy_status_code=fmg_proxy_status_code,
            fmg_proxy_status_message=fmg_proxy_status_message,
            fmg_proxy_url=fmg_proxy_url,
            fmg_url=fmg_url,
            fmg_id=fmg_id,
            fmg_raw=response,
        )
