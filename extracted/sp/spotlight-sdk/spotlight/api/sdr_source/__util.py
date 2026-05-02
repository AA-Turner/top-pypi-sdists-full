from datetime import date
from typing import Dict, Any, List

from spotlight.core.common.enum import AssetClass


def _sdr_metadata_request_info(
    asset_class: AssetClass, from_date: date, to_date: date, reprocess: bool = True
) -> Dict[str, Any]:
    endpoint = f"sdr-source/sdr/{asset_class.lower()}/metadata"
    params = {
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "reprocess": str(reprocess).lower(),
    }
    return {"endpoint": endpoint, "params": params}


def _sdr_upload_request_info(metadata: List[Dict[str, Any]]) -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/upload"
    return {"endpoint": endpoint, "data": metadata}


def _sdr_download_request_info(metadata: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/download"
    return {"endpoint": endpoint, "json": metadata}


def _sdr_download_json_request_info(metadata: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/download?json"
    return {"endpoint": endpoint, "json": metadata}


def _sdr_cache_clear_file_request_info() -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/cache/clear?file"
    return {"endpoint": endpoint}


def _sdr_cache_clear_record_request_info() -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/cache/clear?record"
    return {"endpoint": endpoint}


def _sdr_cache_lookup_request_info(metadata: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/cache/lookup"
    return {"endpoint": endpoint, "json": metadata}


def _sdr_status_request_info() -> Dict[str, Any]:
    endpoint = "sdr-source/sdr/status"
    return {"endpoint": endpoint}
