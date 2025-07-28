"""Module providing server_utils functionality."""

import os
import requests
import shutil
import logging
import zipfile
import tarfile
import uuid
import base64
import traceback
import math
from collections import defaultdict
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import (
    List,
    Dict,
    Any,
    Optional,
    Tuple,
)
from matrice.data_processing.client_utils import (
    is_file_compressed,
)
import time


def get_corresponding_split_type(path: str, include_year: bool = False) -> str:
    """
    Get the split type (train/val/test) from a file path.

    Args:
        path: File path to analyze
        include_year: Whether to include year in split type

    Returns:
        Split type string
    """
    split_types = ["train", "val", "test"]
    text_parts = path.split(os.sep)
    split_type = next(
        (key for part in text_parts for key in split_types if key in part.lower()),
        "unassigned",
    )
    if split_type != "unassigned" and include_year:
        year = "".join(filter(str.isdigit, path))
        return f"{split_type}{year}" if year else split_type
    return split_type


def construct_relative_path(
    dataset_id: str,
    folder_name: str,
    file_name: str,
) -> str:
    """
    Construct relative path from components.

    Args:
        dataset_id: Dataset identifier
        folder_name: Name of folder
        file_name: Name of file

    Returns:
        Constructed relative path
    """
    return f"{dataset_id}/images/{folder_name}/{file_name}"


def download_file(
    url: str,
    file_path: str,
    timeout: int = 60,
    chunk_size: int = 8192,
    max_retries: int = 1,
) -> str:
    """
    Download file from URL to specified path with improved reliability.

    Args:
        url: URL to download from
        file_path: Path to save file to
        timeout: Request timeout in seconds
        chunk_size: Size of chunks to download

    Returns:
        Path where file was saved

    Raises:
        Exception: If download fails
    """
    for _ in range(max_retries):
        try:
            # Create parent directory if it doesn't exist
            parent_dir = os.path.dirname(file_path)
            if parent_dir:
                try:
                    os.makedirs(parent_dir, exist_ok=True)
                except Exception as err:
                    logging.error(f"Error creating directory {parent_dir}: {str(err)}")
                    raise

            # Use a session for better connection reuse
            with requests.Session() as session:
                # Set timeouts to prevent hanging downloads
                response = session.get(url, stream=True, timeout=timeout)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                # Determine optimal chunk size based on file size
                adaptive_chunk_size = chunk_size
                if file_size > 100 * 1024 * 1024:  # If file is larger than 100MB
                    adaptive_chunk_size = 1024 * 1024  # Use 1MB chunks

                # Download with progress tracking
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=adaptive_chunk_size):
                        if not chunk:
                            continue

                        file.write(chunk)
                        downloaded += len(chunk)

            # Verify file was downloaded correctly
            if not os.path.exists(file_path):
                raise Exception(f"Downloaded file does not exist: {file_path}")
            if os.path.getsize(file_path) == 0:
                raise Exception(f"Downloaded file is empty: {file_path}")
            return file_path

        except requests.exceptions.Timeout:
            logging.warning(
                f"Timeout downloading file from {url} after {timeout}s to {file_path}"
            )
        except requests.exceptions.ConnectionError as err:
            logging.warning(f"Connection error downloading file from {url}: {str(err)}")
        except requests.exceptions.HTTPError as err:
            logging.warning(
                f"HTTP error {err.response.status_code} downloading file from {url} to {file_path}"
            )
        except Exception as err:
            logging.warning(
                f"Error downloading file from {url} to {file_path}: {str(err)}"
            )
    logging.error(
        f"Failed to download file from {url} to {file_path} after {max_retries} attempts"
    )
    raise Exception(
        f"Failed to download file from {url} to {file_path} after {max_retries} attempts"
    )


def get_batch_pre_signed_download_urls(
    cloud_file_paths: List[str],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: Optional[str] = None,
) -> Dict:
    """
    Get batch of pre-signed download URLs.

    Args:
        cloud_file_paths: List of cloud file paths
        rpc: RPC client
        bucket_alias: Optional bucket alias
        account_number: Optional account number

    Returns:
        Response data or error message
    """
    if not isinstance(cloud_file_paths, list):
        cloud_file_paths = [cloud_file_paths]
    resp = rpc.post(
        f"/v2/dataset/get_batch_pre_signed_download_urls?projectId={project_id}" if project_id else "",
        payload={
            "fileNames": cloud_file_paths,
            "type": "samples",
            "isPrivateBucket": bool(bucket_alias),
            "bucketAlias": bucket_alias,
            "accountNumber": account_number,
        },
    )
    if resp["success"]:
        return resp["data"]
    logging.error(
        "Failed to get presigned URLs: %s",
        resp["message"],
    )
    return resp["message"]


def get_filename_from_url(url: str) -> str:
    """
    Extract filename from URL.

    Args:
        url: URL to parse

    Returns:
        Extracted filename
    """
    parsed_url = urlparse(url)
    return parsed_url.path.split("/")[-1]


def rpc_get_call(
    rpc: Any,
    path: str,
    params: Optional[Dict] = None,
) -> Optional[Dict]:
    """
    Make RPC GET call.

    Args:
        rpc: RPC client
        path: API path
        params: Optional query parameters

    Returns:
        Response data or None on failure
    """
    if params is None:
        params = {}
    resp = rpc.get(path=path, params=params)
    if resp["success"]:
        return resp["data"]
    logging.error(
        "Failed to get response for path: %s , response: %s",
        path,
        resp,
    )
    return None


def update_partition_status(
    rpc: Any,
    action_record_id: str,
    dataset_id: str,
    version: str,
    partition: int,
    status: str,
    partition_items: List[Dict],
    annotation_type: str,
) -> Optional[Dict]:
    """
    Update partition processing status.

    Args:
        rpc: RPC client
        action_record_id: Action record identifier
        dataset_id: Dataset identifier
        version: Dataset version
        partition: Partition number
        status: Status to set
        partition_items: Items in partition
        annotation_type: Type of annotation

    Returns:
        Response data or None on failure

    Raises:
        Exception: If update fails
    """
    logging.debug(
        "Updating partition status for partition items %s",
        partition_items,
    )
    try:
        class_stats = get_classwise_splits(partition_items, annotation_type)
        status_update_payload = {
            "classStat": class_stats,
            "actionRecordId": action_record_id,
            "targetVersion": version,
            "partitionNumber": partition,
            "status": status,
        }
        logging.debug(
            "Updating partition status for partition %s to %s",
            partition,
            status_update_payload,
        )
        resp = rpc.put(
            path=f"/v2/dataset/update-partition-status/{dataset_id}",
            payload=status_update_payload,
        )
        logging.debug(
            "Payload sent to update-partition-status: %s",
            status_update_payload,
        )
        logging.debug("response from update-partition-status: %s", resp)
        if resp["success"]:
            logging.info(
                "Successfully updated partition status for partition %s to %s, response: %s",
                partition,
                status,
                resp,
            )
            return resp["data"]
        error_msg = f"Failed to update partition status: {resp}"
        logging.error(error_msg)
        return None
    except Exception as err:
        logging.error(
            "Error updating partition status: %s",
            str(err),
        )
        raise


def update_video_frame_partition_status(
    rpc: Any,
    action_record_id: str,
    dataset_id: str,
    version: str,
    partition: int,
    status: str,
    partition_items: List[Dict],
    annotation_type: str,
    sample_stats: Optional[Dict] = None,
) -> Optional[Dict]:
    """
    Update video frame partition processing status.

    Args:
        rpc: RPC client
        action_record_id: Action record identifier
        dataset_id: Dataset identifier
        version: Dataset version
        partition: Partition number
        status: Status to set
        partition_items: Items in partition
        annotation_type: Type of annotation
        sample_stats: Optional sample statistics

    Returns:
        Response data or None on failure

    Raises:
        Exception: If update fails
    """
    logging.debug(
        "Updating partition status for partition items %s",
        partition_items,
    )
    try:
        class_stats, unique_video_stats = get_classwise_frame_splits(
            partition_items,
            annotation_type,
            sample_stats,
        )
        class_stats = dict(class_stats)
        status_update_payload = {
            "uniqueVideoStats": unique_video_stats,
            "classStat": class_stats,
            "actionRecordId": action_record_id,
            "targetVersion": version,
            "partitionNumber": partition,
            "status": status,
        }
        logging.debug(
            "Updating partition status for partition %s to %s",
            partition,
            status_update_payload,
        )
        resp = rpc.put(
            path=f"/v2/dataset/update-partition-status/{dataset_id}",
            payload=status_update_payload,
        )
        logging.debug(
            "Payload sent to update-partition-status: %s",
            status_update_payload,
        )
        if resp["success"]:
            logging.info(
                "Successfully updated partition status for partition %s to %s, response: %s",
                partition,
                status,
                resp,
            )
            return resp["data"]
        error_msg = f"Failed to update partition status: {resp}"
        logging.error(error_msg)
        return None
    except Exception as err:
        logging.error(
            "Error updating partition status: %s",
            str(err),
        )
        raise


def get_unprocessed_partitions(rpc: Any, dataset_id: str, version: str) -> List[int]:
    """
    Get list of unprocessed partition numbers.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        version: Dataset version

    Returns:
        List of unprocessed partition numbers
    """
    unprocessed_partitions_response = rpc_get_call(
        rpc,
        f"/v2/dataset/get_unprocessed_partitions/{dataset_id}/version/{str(version)}",
        params={},
    )
    if unprocessed_partitions_response is None:
        return []
    unprocessed_partitions = list(set(x["partitionNum"] for x in unprocessed_partitions_response))
    logging.info(
        "Found %s unprocessed partitions: %s",
        len(unprocessed_partitions),
        unprocessed_partitions,
    )
    return unprocessed_partitions


def generate_short_uuid() -> str:
    """
    Generate a shortened UUID.

    Returns:
        Short UUID string
    """
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b"=").decode("utf-8")


def delete_tmp_folder(
    tmp_folder_path: str,
) -> None:
    """
    Delete temporary folder.

    Args:
        tmp_folder_path: Path to temporary folder
    """
    logging.info(
        "Attempting to delete temporary folder: %s",
        tmp_folder_path,
    )
    if os.path.exists(tmp_folder_path):
        shutil.rmtree(tmp_folder_path)
        logging.info(
            "Temporary folder %s has been deleted.",
            tmp_folder_path,
        )
        print(f"Temporary folder {tmp_folder_path} has been deleted.")


def extract_dataset(dataset_path: str, get_inner_dir: bool = False) -> str:
    """
    Extract compressed dataset.

    Args:
        dataset_path: Path to compressed dataset
        get_inner_dir: Whether to return inner directory path

    Returns:
        Path to extracted dataset

    Raises:
        ValueError: If archive format is unsupported
        Exception: If extraction fails
    """
    logging.info("Extracting dataset from %s", dataset_path)
    extract_dir = os.path.splitext(dataset_path)[0]
    os.makedirs(extract_dir, exist_ok=True)
    try:
        if dataset_path.endswith(".zip"):
            logging.debug("Extracting ZIP archive")
            with zipfile.ZipFile(dataset_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
        elif dataset_path.endswith(
            (
                ".tar",
                ".tar.gz",
                ".tar.bz2",
                ".tar.xz",
            )
        ):
            logging.debug("Extracting TAR archive")
            mode = "r:*"
            with tarfile.open(dataset_path, mode) as tar_ref:
                tar_ref.extractall(extract_dir)
        else:
            raise ValueError(f"Unsupported archive format for file: {dataset_path}")
        if get_inner_dir:
            extracted_path = os.path.join(
                extract_dir,
                [
                    path
                    for path in os.listdir(extract_dir)
                    if not (path.startswith("_") or path.startswith("."))
                ][0],
            )
        else:
            extracted_path = extract_dir
        logging.info(
            "Successfully extracted dataset to: %s",
            extracted_path,
        )
        return extracted_path
    except Exception as err:
        logging.error(
            "Error extracting dataset: %s",
            str(err),
        )
        raise


def get_classwise_splits(
    partition_items: List[Dict],
    annotation_type: str = "classification",
) -> Dict:
    """
    Get class-wise split statistics.

    Args:
        partition_items: List of partition items
        annotation_type: Type of annotation

    Returns:
        Dictionary of class-wise split statistics
    """
    logging.debug(
        "Getting classwise splits for %s items with annotation type: %s",
        len(partition_items),
        annotation_type,
    )
    classwise_splits = defaultdict(
        lambda: {
            "train": 0,
            "test": 0,
            "val": 0,
            "unassigned": 0,
            "total": 0,
        }
    )
    for item in partition_items:
        logging.debug(
            "Processing item for get_classwise_splits: %s",
            item,
        )
        split_type = item.get("splitType")
        annotations = item.get("annotations")
        try:
            if not annotations:
                continue
            if annotation_type == "detection":
                for annotation in annotations:
                    category = annotation.get("category")
                    if category and split_type:
                        classwise_splits[category][split_type] += 1
            elif annotation_type == "classification":
                category = annotations[0].get("category")
                if category and split_type:
                    classwise_splits[category][split_type] += 1
        except Exception as err:
            logging.error(
                "Error processing item %s: %s",
                item,
                str(err),
            )
    if not classwise_splits:
        logging.warning("No classes found in partition items")
        return {}
    for (
        category,
        counts,
    ) in classwise_splits.items():
        counts["total"] = sum(counts.values())
    logging.debug(
        "Final classwise splits: %s",
        dict(classwise_splits),
    )
    return classwise_splits

def extract_davis_video_name(file_path: str) -> str:
    # Normalize the path to use the OS-specific separator
    norm_path = os.path.normpath(file_path)
    parts = norm_path.split(os.sep)
    
    if len(parts) < 2:
        raise ValueError("Path does not contain enough components to extract video name.")
    
    # The second last element is the folder containing the image (i.e., video name)
    return parts[-2]

from collections import defaultdict
from typing import Dict, List, Optional, Tuple
import logging

def get_classwise_frame_splits(
    partition_items: List[Dict],
    annotation_type: str = "detection",
    sample_stats: Optional[Dict] = None,
) -> Tuple[Dict, Dict]:
    """
    Get class-wise split statistics for video frames.

    Args:
        partition_items: List of partition items
        annotation_type: Type of annotation
        sample_stats: Optional sample statistics

    Returns:
        Tuple of class-wise split statistics and unique video statistics
    """
    logging.debug(
        "Getting classwise splits for %s items with annotation type: %s",
        len(partition_items),
        annotation_type,
    )
    logging.debug("Sample stats are %s", sample_stats)
    
    seen_categories_info = []
    classwise_splits = defaultdict(
        lambda: {
            "train": 0,
            "test": 0,
            "val": 0,
            "unassigned": 0,
            "total": 0,
        }
    )
    unique_videos_splits = {
        "train": 0,
        "test": 0,
        "val": 0,
        "unassigned": 0,
        "total": 0,
    }

    for item in partition_items:
        logging.debug("Processing item for get_classwise_splits: %s", item)
        split_type = item.get("splitType")
        logging.debug("Split type is %s", split_type)
        unique_videos_splits[split_type] += 1

        annotations = {}
        try:
            if annotation_type in ["detection", "object_tracking", "segmentation", "detection_mscoco"]:
                for fileinfo in item.get("fileInfoResponse", []):
                    frames = fileinfo.get("frames", {})
                    if isinstance(frames, dict):
                        annotations.update(frames)
            elif annotation_type in ["classification", "kinetics"]:
                annotations = item.get("annotations", {})
            
            if not annotations:
                continue

            logging.debug("Annotations for getting classwise splits are %s", annotations)

            if annotation_type == "detection":
                for frame_id, frame_items in annotations.items():
                    annotation_list= frame_items.get("annotations", [])
                    for annotations in annotation_list:
                        category = annotations.get("category")
                        if category and split_type:
                            classwise_splits[category][split_type] += 1

            elif annotation_type == "object_tracking":
                for frame_items, annotation in annotations.items():
                    new_annotations = annotation.get("annotations", [])
                    for annotations_items in new_annotations:
                        category = annotations_items.get('category')
                        if category not in seen_categories_info:
                            seen_categories_info.append(category)
                classwise_splits = sample_stats

            elif annotation_type == "classification":
                category = item.get("category")
                if category and split_type:
                    classwise_splits[category][split_type] += 1

            elif annotation_type == "segmentation":
                # for frame_items, annotation in annotations.items():
                #     fileLocation = annotation.get("fileLocation")
                #     video_name = extract_davis_video_name(fileLocation)
                #     seen_categories_info.append(video_name)
                # logging.debug(f'seen categories are {seen_categories_info}')
                # classwise_splits = sample_stats
                for frame_id, frame_items in annotations.items():
                    annotation_list= frame_items.get("annotations", [])
                    for annotations in annotation_list:
                        category = annotations.get("category")
                        if category and split_type:
                            classwise_splits[category][split_type] += 1

            elif annotation_type == "kinetics":
                annotation_items = item.get("annotations", [])
                for ann in annotation_items:
                    category = ann.get("category")
                    if category and split_type:
                        classwise_splits[category][split_type] += 1

            elif annotation_type == "detection_mscoco":
                for frame_id, frame_items in annotations.items():
                    annotation_list= frame_items.get("annotations", [])
                    for annotations in annotation_list:
                        category = annotations.get("category")
                        if category and split_type:
                            classwise_splits[category][split_type] += 1

        except Exception as err:
            logging.error("Error processing item %s: %s", item, str(err))

    logging.debug(f'seen categories are {seen_categories_info}')
    logging.debug(f'classwise splits before seen updates {classwise_splits}')

    seen_categories_info = [str(seen_categories) for seen_categories in seen_categories_info]

    if annotation_type in ["object_tracking"]:
        classwise_splits = {str(key): value for key, value in classwise_splits.items()}
        for category in list(classwise_splits.keys()):
            if category not in seen_categories_info:
                del classwise_splits[category]

    logging.debug(f'New classwise stats after seen update {classwise_splits}')

    if not classwise_splits:
        logging.warning("No classes found in partition items")
        return {}

    if annotation_type not in ["object_tracking"]:
        for category, counts in classwise_splits.items():
            counts["total"] = sum(v for k, v in counts.items() if k != "total")

    unique_videos_splits["total"] = (
        unique_videos_splits["train"]
        + unique_videos_splits["test"]
        + unique_videos_splits["val"]
        + unique_videos_splits["unassigned"]
    )
    
    

    if annotation_type == 'object_tracking':
        classwise_splits = {f"class_{key}": value for key, value in classwise_splits.items()}

    logging.debug("Final classwise splits: %s", dict(classwise_splits))
    logging.debug("Unique videos across splits: %s", unique_videos_splits)
    print(f"Final classwise splits: {dict(classwise_splits)}")
    print(f"Unique videos across splits: {unique_videos_splits}")
    return (
        dict(classwise_splits),
        unique_videos_splits,
    )


def update_action_status(
    action_record_id: str,
    action_type: str,
    step_code: str,
    status: str,
    status_description: str,
    rpc: Any,
) -> None:
    """
    Update action status.

    Args:
        action_record_id: Action record identifier
        action_type: Type of action
        step_code: Code for current step
        status: Status to set
        status_description: Description of status
        rpc: RPC client
    """
    url = "/v1/actions"
    payload = {
        "_id": action_record_id,
        "stepCode": step_code,
        "status": status,
        "statusDescription": status_description,
        "serviceName": "be-dataset",
        "action": action_type,
        "subAction": action_type,
    }
    rpc.put(url, payload)


def log_error(
    action_record_id: str,
    exception: Exception,
    filename: str,
    function_name: str,
    rpc: Any,
) -> None:
    """
    Log error to system.

    Args:
        action_record_id: Action record identifier
        exception: Exception that occurred
        filename: Name of file where error occurred
        function_name: Name of function where error occurred
        rpc: RPC client
    """
    traceback_str = traceback.format_exc().rstrip()
    log_err = {
        "actionRecordID": action_record_id,
        "serviceName": "Data-Processing",
        "stackTrace": traceback_str,
        "errorType": "Internal",
        "description": str(exception),
        "fileName": filename,
        "functionName": function_name,
        "moreInfo": {},
    }
    error_logging_route = "/v1/system/log_error"
    rpc.post(url=error_logging_route, data=log_err)
    print("An exception occurred. Logging the exception information:")


def chunk_items(items: List[Dict[str, Any]], chunk_size: int) -> List[List[Dict[str, Any]]]:
    """
    Chunk items into smaller batches.

    Args:
        items: List of items to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunked item batches
    """
    if not items:
        logging.warning("No valid items to chunk")
        return []
    len_items = len(items)
    return [items[i : min(i + chunk_size, len_items)] for i in range(0, len_items, chunk_size)]


def fetch_items(
    rpc: Any,
    path: str,
    request_batch_size: int,
    page_number: Optional[int] = None,
    download_images_required: bool = False,
) -> List[Dict[str, Any]]:
    """
    Fetch items from the dataset API.

    Args:
        rpc: RPC client for making API calls
        path: API path to fetch items
        request_batch_size: Number of items to fetch per page
        page_number: Page number to fetch
        download_images_required: Whether to get presigned URLs for images

    Returns:
        List of dataset items
    """
    if page_number is not None:
        path += f"?isPresignedURLRequired={'true' if download_images_required else 'false'}&pageNumber={page_number}&pageSize={request_batch_size}"
    response = rpc_get_call(rpc=rpc, path=path)
    if not response:
        logging.error(
            "Failed to get response for path: %s",
            path,
        )
        return []
    return response.get("items", [])


def fetch_video_frame_items(
    rpc: Any,
    path: str,
    request_batch_size: int,
    page_number: Optional[int] = None,
    download_images_required: bool = False,
    is_file_info_required: bool = False,
) -> List[Dict[str, Any]]:
    """
    Fetch video frame items from the dataset API.

    Args:
        rpc: RPC client for making API calls
        path: API path to fetch items
        request_batch_size: Number of items to fetch per page
        page_number: Page number to fetch
        download_images_required: Whether to get presigned URLs for images
        is_file_info_required: Whether file info is required

    Returns:
        List of dataset items
    """
    if page_number is not None:
        path += f"?isPresignedURLRequired={'true' if download_images_required else 'false'}&pageNumber={page_number}&pageSize={request_batch_size}&isFileInfoRequired={'true' if is_file_info_required else 'false'}"
    logging.debug(
        "Fetching video frame items from path: %s",
        path,
    )
    logging.debug(
        "is download_images_required: %s",
        download_images_required,
    )
    response = rpc_get_call(rpc=rpc, path=path)
    if not response:
        logging.error(
            "Failed to get response for path: %s",
            path,
        )
        return []
    return response.get("items", [])

def fetch_data_prep_video_frame_items(
    rpc: Any,
    path: str,
    request_batch_size: int,
    page_number: Optional[int] = None,
    download_images_required: bool = True,
    is_file_info_required: bool = True,
    isAnnotationInfoRequired: bool = True
) -> List[Dict[str, Any]]:
    """
    Fetch video frame items from the dataset API.

    Args:
        rpc: RPC client for making API calls
        path: API path to fetch items
        request_batch_size: Number of items to fetch per page
        page_number: Page number to fetch
        download_images_required: Whether to get presigned URLs for images
        is_file_info_required: Whether file info is required

    Returns:
        List of dataset items
    """
    if page_number is not None:
        path += f"?isPresignedURLRequired={'true' if download_images_required else 'false'}&pageNumber={page_number}&pageSize={request_batch_size}&isFileInfoRequired={'true' if is_file_info_required else 'false'}&isAnnotationInfoRequiredString={'true' if isAnnotationInfoRequired else 'false'}"
    logging.debug(
        "Fetching video frame items from path: %s",
        path,
    )
    logging.debug(
        "is download_images_required: %s",
        download_images_required,
    )
    response = rpc_get_call(rpc=rpc, path=path)
    if not response:
        logging.error(
            "Failed to get response for path: %s",
            path,
        )
        return []
    return response.get("items", [])


def get_batch_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    page_number: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Get a batch of items from a specific partition page.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        partition: Partition number
        page_number: Page number to fetch
        download_images_required: Whether to get presigned URLs
        request_batch_size: Number of items per batch

    Returns:
        List of partition items
    """
    path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}"
    batch_items = fetch_items(
        rpc,
        path,
        request_batch_size,
        page_number,
        download_images_required,
    )
    return [{**item, "partition": partition} for item in batch_items if item]


def get_video_frame_batch_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    page_number: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
    is_file_info_required: bool = False,
    input_type: str = "mscoco_video",
) -> List[Dict[str, Any]]:
    """
    Get a batch of video frame items from a specific partition page.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        partition: Partition number
        page_number: Page number to fetch
        download_images_required: Whether to get presigned URLs
        request_batch_size: Number of items per batch
        is_file_info_required: Whether file info is required

    Returns:
        List of partition items with added file info and presigned URLs if requested
    """
    # Get the base partition items first (API no longer accepts additional parameters)
    if input_type in ['mscoco_video', 'davis', 'mot', 'youtube_bb', 'kinetics', 'video_imagenet']:
            path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}?pageSize={request_batch_size}&pageNumber={page_number}"
            logging.debug("Fetching base partition items from path: %s", path)
            
            response = rpc_get_call(rpc=rpc, path=path)
            if not response:
                logging.error("Failed to get response for path: %s", path)
                return []
            
            items = response.get("items", [])
            if not items:
                return []
            logging.debug("items fetched from path %s are %s", path, items)
            # Add partition number to each item
            items = [{**item, "partition": partition} for item in items if item]

            # If file info is required, fetch it for each item
            if is_file_info_required:
                items = enrich_items_with_file_info(rpc, items, download_images_required)
            
            return items
    else:
        path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}"
        batch_items = fetch_video_frame_items(
            rpc,
            path,
            request_batch_size,
            page_number,
            download_images_required,
            is_file_info_required,
        )
        return [{**item, "partition": partition} for item in batch_items if item]

def enrich_items_with_file_info(
    rpc: Any,
    items: List[Dict[str, Any]],
    download_images_required: bool = False,
) -> List[Dict[str, Any]]:
    """
    Enriches dataset items with file and annotation information, including presigned URLs if requested.
    
    Args:
        rpc: RPC client for making API calls
        items: List of dataset items to enrich
        download_images_required: Whether to get presigned URLs for images
    
    Returns:
        List of enriched dataset items
    """
    enriched_items = []

    for item in items:
        item_id = item.get("_id")
        if not item_id:
            logging.warning("Item is missing _id, skipping file info enrichment")
            enriched_items.append(item)
            continue

        # Use the updated fetch_all_file_info function
        file_info_list = fetch_file_info(rpc, item_id, download_images_required)
        if file_info_list:
            item["fileInfoResponse"] = file_info_list
            item["annotationResponse"] = []
        # Fetch all annotation info if version is available
        version_info = item.get("versionInfo", [])
        # if version_info and isinstance(version_info, list) and len(version_info) > 0:
        #     version = version_info[0].get("version")
        #     if version:
        #         try:
        #             annotation_info_list = fetch_annotation_info(rpc, item_id, version)
        #             if annotation_info_list:
        #                 item["annotationResponse"] = annotation_info_list
        #         except Exception as err:
        #             logging.warning(
        #                 "Failed to fetch annotation info for item %s, version %s: %s",
        #                 item_id,
        #                 version,
        #                 str(err),
        #             )
        #             
            
                    

        enriched_items.append(item)

    logging.debug("Enriched items: %s", enriched_items)
    return enriched_items


def fetch_file_info(
    rpc: Any,
    dataset_item_id: str,
    download_images_required: bool = False,
    page_size: int = 10,
) -> List[Dict[str, Any]]:
    """
    Fetches all file information for a specific dataset item across pages.
    
    Args:
        rpc: RPC client for making API calls
        dataset_item_id: Dataset item identifier
        download_images_required: Whether to get presigned URLs
        page_size: Number of items per page
    
    Returns:
        A list of all file information items
    """
    all_items = []
    page_number = 0

    while True:
        path = (
            f"/v2/dataset/list-file-info/{dataset_item_id}"
            f"?pageNumber={page_number}&pageSize={page_size}"
            f"&isPresignedURLRequired={'true' if download_images_required else 'false'}"
        )
        logging.debug("Fetching file info from path: %s", path)
        response = rpc_get_call(rpc=rpc, path=path)

        if not response:
            logging.error("Failed to get file info for item: %s", dataset_item_id)
            break

        items = response.get("items", [])
        if not items:
            logging.debug("No more file info found on page %s for item: %s", page_number, dataset_item_id)
            break

        logging.debug("Fetched %d items from page %d for dataset item id %s", len(items), page_number, dataset_item_id)
        all_items.extend(items)
        page_number += 1

    return all_items


def fetch_annotation_info(
    rpc: Any,
    dataset_item_id: str,
    version: str,
    page_size: int = 10,
) -> List[Dict[str, Any]]:
    """
    Fetches all annotation information for a specific dataset item and version across pages.
    
    Args:
        rpc: RPC client for making API calls
        dataset_item_id: Dataset item identifier
        version: Version identifier
        page_size: Number of items per page
    
    Returns:
        A list of all annotation information items
    """
    all_items = []
    page_number = 0

    while True:
        path = (
            f"/v2/dataset/list-annotation-files/{dataset_item_id}/{version}"
            f"?pageNumber={page_number}&pageSize={page_size}"
        )
        logging.debug("Fetching annotation info from path: %s", path)
        response = rpc_get_call(rpc=rpc, path=path)

        if not response:
            logging.error("Failed to get annotation info for item: %s, version: %s", dataset_item_id, version)
            break

        items = response.get("items", [])
        if not items:
            logging.debug("No more annotation info found on page %s for item: %s, version: %s", page_number, dataset_item_id, version)
            break

        logging.debug("Fetched %d annotation items from page %d for dataset item id %s", len(items), page_number, dataset_item_id)
        all_items.extend(items)
        page_number += 1

    return all_items


def get_number_of_partition_batches(
    rpc: Any,
    dataset_id: str,
    partition: int,
    request_batch_size: int = 1,
) -> int:
    """
    Calculate total number of pages for a partition.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        partition: Partition number
        request_batch_size: Number of items per batch

    Returns:
        Number of pages
    """
    path = f"/v2/dataset/list-partition-items/{dataset_id}/{partition}"
    response = rpc_get_call(rpc=rpc, path=path)
    if not response:
        logging.error(
            "Failed to get total items for partition %s",
            partition,
        )
        return 0
    total_items = response.get("total", 0)
    return math.ceil(total_items / request_batch_size)


def get_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Get all items for a partition.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        partition: Partition number
        download_images_required: Whether to get presigned URLs
        request_batch_size: Number of items per batch

    Returns:
        List of all partition items
    """
    number_of_partition_pages = get_number_of_partition_batches(
        rpc,
        dataset_id,
        partition,
        request_batch_size,
    )
    if number_of_partition_pages == 0:
        logging.warning(
            "No items found for partition %s",
            partition,
        )
        return []
    all_dataset_items = []
    with ThreadPoolExecutor(max_workers=number_of_partition_pages) as executor:
        futures = [
            executor.submit(
                get_batch_partition_items,
                rpc,
                dataset_id,
                partition,
                page_number,
                download_images_required,
                request_batch_size,
            )
            for page_number in range(number_of_partition_pages)
        ]
        for future in futures:
            try:
                all_dataset_items.extend(future.result())
            except Exception as err:
                logging.error(
                    "Error getting batch for partition %s: %s",
                    partition,
                    err,
                )
    return all_dataset_items


def get_video_frame_partition_items(
    rpc: Any,
    dataset_id: str,
    partition: int,
    download_images_required: bool = False,
    request_batch_size: int = 100,
    is_file_info_required: bool = True,
    input_type: str = "mscoco_video",
) -> List[Dict[str, Any]]:
    """
    Get all video frame items for a partition.

    Args:
        rpc: RPC client
        dataset_id: Dataset identifier
        partition: Partition number
        download_images_required: Whether to get presigned URLs
        request_batch_size: Number of items per batch
        is_file_info_required: Whether file info is required

    Returns:
        List of all partition items
    """
    number_of_partition_pages = get_number_of_partition_batches(
        rpc,
        dataset_id,
        partition,
        request_batch_size,
    )
    if number_of_partition_pages == 0:
        logging.warning(
            "No items found for partition %s",
            partition,
        )
        return []
    all_dataset_items = []
    with ThreadPoolExecutor(max_workers=number_of_partition_pages) as executor:
        futures = [
            executor.submit(
                get_video_frame_batch_partition_items,
                rpc,
                dataset_id,
                partition,
                page_number,
                download_images_required,
                request_batch_size,
                is_file_info_required,
                input_type
            )
            for page_number in range(number_of_partition_pages)
        ]
        for future in futures:
            try:
                all_dataset_items.extend(future.result())
            except Exception as err:
                logging.error(
                    "Error getting batch for partition %s: %s",
                    partition,
                    err,
                )
    return all_dataset_items


def get_batch_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    page_number: int,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get a batch of items from a specific dataset version page."""
    path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
    return fetch_items(rpc, path, request_batch_size, page_number)

def get_batch_video_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    page_number: int,
    request_batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Get a batch of items from a specific dataset version page."""
    path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
    return fetch_video_frame_items(rpc, path, request_batch_size, page_number, True, True)


def get_data_prep_batch_video_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    page_number: int,
    request_batch_size: int = 100,
    input_type: str = "davis",
) -> List[Dict[str, Any]]:
    """
    Fetch dataset items and enrich with file info and annotation info.
    """
    if input_type in ['davis', 'mscoco_video', 'kinetics']:
        base_items = fetch_base_dataset_items(
            rpc, dataset_id, dataset_version, page_number, request_batch_size
        )

        enriched_items = []
        def enrich_item(item, rpc, dataset_version):
            dataset_item_id = item["_id"]
            file_info = fetch_all_file_info(rpc, dataset_item_id)
            annotation_info = fetch_all_annotations(rpc, dataset_item_id, dataset_version)
            item["fileInfo"] = file_info
            item["annotationInfo"] = annotation_info
            return item

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(enrich_item, item, rpc, dataset_version)
                for item in base_items
            ]
            enriched_items = [future.result() for future in as_completed(futures)]

        logging.debug(f"Enriched items: {enriched_items}")
        return enriched_items
    else:
        path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
        return fetch_data_prep_video_frame_items(rpc, path, request_batch_size, page_number, True, True, True)

def fetch_base_dataset_items(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    page_number: int,
    page_size: int
) -> List[Dict[str, Any]]:
    path = (
        f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
        f"?pageNumber={page_number}&pageSize={page_size}&sortBy=&sortOrder=asc&isPresignedURLRequired=true"
    )
    logging.debug(f"Fetching base dataset items: {path}")
    response = rpc_get_call(rpc=rpc, path=path)
    logging.debug(f"Response for base dataset items: {response}")
    return response.get("items", []) if response else []

def fetch_all_file_info(rpc: Any, dataset_item_id: str) -> List[Dict[str, Any]]:
    path_template = (
        f"/v2/dataset/list-file-info/{dataset_item_id}"
        f"?isPresignedURLRequired=true&pageSize=100&pageNumber={{page}}"
    )
    return paginate_all(rpc, path_template)

def fetch_all_annotations(rpc: Any, dataset_item_id: str, version: str) -> List[Dict[str, Any]]:
    path_template = (
        f"/v2/dataset/list-annotation-info/{dataset_item_id}/{version}"
        f"?pageNumber={{page}}&pageSize=100&sortBy=&sortOrder=asc&isPresignedURLRequired=false"
    )
    return paginate_all(rpc, path_template)

def paginate_all(rpc: Any, path_template: str) -> List[Dict[str, Any]]:
    results = []
    page = 0
    while True:
        path = path_template.format(page=page)
        logging.debug(f"Paginated fetch: {path}")
        response = rpc_get_call(rpc=rpc, path=path)
        logging.debug(f"Response for paginated fetch for path {path}: {response}")
        if not response:
            break

        items = response.get("items", [])
        results.extend(items)

        if len(items) < response.get("pageSize", 100):
            break
        page += 1
    return results


def get_number_of_dataset_batches(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    request_batch_size: int = 1,
) -> int:
    """Calculate total number of pages for a dataset."""
    path = f"/v2/dataset/item/{dataset_id}/version/{dataset_version}"
    response = rpc_get_call(rpc=rpc, path=path)
    if not response:
        logging.error(
            "Failed to get total items for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        return 0
    total_items = response.get("total", 0)
    logging.debug(f'Total items are {total_items}')
    return math.ceil(total_items / request_batch_size)


def handle_source_url_dataset_download(
    source_url,
) -> str:
    """Handle dataset download from source URL."""
    logging.info(
        "Processing dataset from URL: %s",
        source_url,
    )
    dataset_path = download_file(
        source_url,
        source_url.split("?")[0].split("/")[-1],
    )
    if is_file_compressed(dataset_path):
        dataset_path = extract_dataset(dataset_path, get_inner_dir=True)
    logging.info("Dataset path: %s", dataset_path)
    return dataset_path
