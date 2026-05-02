from datetime import date
from typing import Dict, Any, List

from spotlight.api.sdr_source.__util import (
    _sdr_metadata_request_info,
    _sdr_upload_request_info,
    _sdr_download_request_info,
    _sdr_download_json_request_info,
    _sdr_cache_clear_file_request_info,
    _sdr_cache_clear_record_request_info,
    _sdr_cache_lookup_request_info,
    _sdr_status_request_info,
)
from spotlight.core.common.decorators import data_request
from spotlight.core.common.enum import AssetClass
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
)


@data_request()
def get_metadata(
    asset_class: AssetClass, from_date: date, to_date: date, reprocess: bool = True
) -> List[Dict[str, Any]]:
    """
    Get metadata between two dates.

    Args:
        asset_class (AssetClass): Asset class
        from_date (date): Start date
        to_date (date): End date
        reprocess (bool): Reprocess flag

    Returns:
        List[Dict[str, Any]]: Metadata response
    """
    request_info = _sdr_metadata_request_info(
        asset_class, from_date, to_date, reprocess
    )
    return __get_request(**request_info)


@data_request()
def upload_metadata(metadata: List[Dict[str, Any]]) -> None:
    """
    Upload sdr data for metadata.

    Args:
        metadata (List[Dict[str, Any]]): Metadata

    Returns:
        None
    """
    request_info = _sdr_upload_request_info(metadata)
    return __post_request(**request_info)


@data_request(processor=lambda r: r.text)
def download_csv(metadata: Dict[str, Any]) -> str:
    """
    Download CSV sdr data for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        str: CSV data
    """
    request_info = _sdr_download_request_info(metadata)
    return __post_request(**request_info)


@data_request()
def download_json(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Download JSON sdr data for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        List[Dict[str, Any]]: JSON data
    """
    request_info = _sdr_download_json_request_info(metadata)
    return __post_request(**request_info)


@data_request()
def clear_file_cache() -> None:
    """
    Clear file cache.

    Returns:
        None
    """
    request_info = _sdr_cache_clear_file_request_info()
    return __post_request(**request_info)


@data_request()
def clear_record_cache() -> None:
    """
    Clear record cache.

    Returns:
        None
    """
    request_info = _sdr_cache_clear_record_request_info()
    return __post_request(**request_info)


@data_request()
def lookup_cache(metadata: Dict[str, Any]) -> bool:
    """
    Lookup cache for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        bool: Exists in cache
    """
    request_info = _sdr_cache_lookup_request_info(metadata)
    return __post_request(**request_info)


@data_request()
def get_status() -> Dict[str, Any]:
    """
    Get scraper status.

    Returns:
        Dict[str, Any]: Health status
    """
    request_info = _sdr_status_request_info()
    return __get_request(**request_info)
