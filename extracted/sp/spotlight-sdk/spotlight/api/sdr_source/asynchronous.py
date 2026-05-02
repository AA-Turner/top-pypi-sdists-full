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
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.enum import AssetClass
from spotlight.core.common.requests import (
    __async_get_request,
    __async_post_request,
)


@async_data_request()
async def async_get_metadata(
    asset_class: AssetClass, from_date: date, to_date: date, reprocess: bool = True
) -> List[Dict[str, Any]]:
    """
    Asynchronously get metadata between two dates.

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
    return await __async_get_request(**request_info)


@async_data_request()
async def async_upload_metadata(metadata: List[Dict[str, Any]]) -> None:
    """
    Asynchronously upload sdr data for metadata.

    Args:
        metadata (List[Dict[str, Any]]): Metadata

    Returns:
        None
    """
    request_info = _sdr_upload_request_info(metadata)
    return await __async_post_request(**request_info)


@async_data_request(processor=lambda r: r.text)
async def async_download_csv(metadata: Dict[str, Any]) -> str:
    """
    Asynchronously download CSV sdr data for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        str: CSV data
    """
    request_info = _sdr_download_request_info(metadata)
    return await __async_post_request(**request_info)


@async_data_request()
async def async_download_json(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Asynchronously download JSON sdr data for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        List[Dict[str, Any]]: JSON data
    """
    request_info = _sdr_download_json_request_info(metadata)
    return await __async_post_request(**request_info)


@async_data_request()
async def async_clear_file_cache() -> None:
    """
    Asynchronously clear file cache.

    Returns:
        None
    """
    request_info = _sdr_cache_clear_file_request_info()
    return await __async_post_request(**request_info)


@async_data_request()
async def async_clear_record_cache() -> None:
    """
    Asynchronously clear record cache.

    Returns:
        None
    """
    request_info = _sdr_cache_clear_record_request_info()
    return await __async_post_request(**request_info)


@async_data_request()
async def async_lookup_cache(metadata: Dict[str, Any]) -> bool:
    """
    Asynchronously lookup cache for metadata.

    Args:
        metadata (Dict[str, Any]): Metadata

    Returns:
        bool: Exists in cache
    """
    request_info = _sdr_cache_lookup_request_info(metadata)
    return await __async_post_request(**request_info)


@async_data_request()
async def async_get_status() -> Dict[str, Any]:
    """
    Asynchronously get scraper status.

    Returns:
        Dict[str, Any]: Health status
    """
    request_info = _sdr_status_request_info()
    return await __async_get_request(**request_info)
