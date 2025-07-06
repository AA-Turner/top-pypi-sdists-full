"""Module providing server functionality."""

import logging
import os
import time
import traceback
from queue import Queue
from typing import Any, Dict, List, Optional
import requests
from PIL import Image
from matrice.data_processing.data_formats.mscoco_detection import (
    get_msococo_images_details,
    add_mscoco_dataset_items_details,
)
from matrice.data_processing.data_formats.imagenet_classification import (
    add_imagenet_dataset_items_details,
)
from matrice.data_processing.data_formats.pascalvoc_detection import (
    get_pascalvoc_image_details,
    add_pascalvoc_dataset_items_details,
)
from matrice.data_processing.data_formats.labelbox_detection import (
    get_labelbox_image_details,
    add_labelbox_dataset_items_details,
    add_labelbox_dataset_item_local_file_path,
    download_labelbox_dataset_items,
)
from matrice.data_processing.data_formats.labelbox_classification import (
    get_labelbox_classification_image_details,
    add_labelbox_classification_dataset_items_details,
    add_labelbox_classification_dataset_item_local_file_path,
)
from matrice.data_processing.data_formats.yolo_detection import (
    get_yolo_image_details,
    add_yolo_dataset_items_details,
    convert_payload_to_coco_format,
)
from matrice.data_processing.data_formats.unlabelled import (
    add_unlabelled_dataset_items_details,
)
from matrice.data_processing.server_utils import (
    download_file,
    rpc_get_call,
    get_batch_pre_signed_download_urls,
    get_filename_from_url,
    update_partition_status,
    update_video_frame_partition_status,
    get_unprocessed_partitions,
    extract_dataset,
    get_partition_items,
    chunk_items,
    handle_source_url_dataset_download,
    get_video_frame_partition_items,
)
from matrice.data_processing.client_utils import (
    scan_folder,
)
from matrice.data_processing.pipeline import (
    Pipeline,
)
from matrice.data_processing.data_formats.video_youtube_bb_tracking import (
    get_youtube_bb_video_frame_details,
    add_youtube_bb_dataset_items_details,
)
from matrice.data_processing.data_formats.video_mot_tracking import (
    get_mot_annotations,
    add_mot_dataset_items_details,
)
from matrice.data_processing.data_formats.video_davis_segmentation import (
    get_davis_annotations,
    add_davis_dataset_items_details,
)
from matrice.data_processing.data_formats.video_imagenet_classification import (
    add_video_imagenet_dataset_items_details,
)
from matrice.data_processing.data_formats.video_kinetics_activity_recognition import (
    get_kinetics_annotations,
    add_kinetics_dataset_items_details,
)
from matrice.data_processing.data_formats.video_detection_mscoco import (
    add_video_mscoco_dataset_items_details,
    get_video_mscoco_annotations,
)

TMP_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tmp",
)
os.makedirs(TMP_FOLDER, exist_ok=True)
logging.info("Created temporary folder at %s", TMP_FOLDER)


def download_labelbox_dataset(dataset_id, rpc, dataset_version, source_url):
    """Download a dataset from Labelbox.

    Args:
        dataset_id: ID of the dataset
        rpc: RPC client for making API calls
        dataset_version: Version of the dataset
        source_url: Optional source URL to download from

    Returns:
        Path to the downloaded dataset
    """
    if source_url:
        dataset_path = handle_source_url_dataset_download(source_url)
    else:
        logging.info("Downloading annotation file for labelbox dataset")
        dataset_path = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            False,
        )[0]
    logging.info("Downloading dataset from labelbox")
    dataset_path = download_labelbox_dataset_items(dataset_id, dataset_path)
    return dataset_path


def partition_items_producer(
    rpc: Any,
    dataset_id: str,
    partition: int,
    pipeline_queue: Queue,
    download_images_required: bool = False,
    request_batch_size: int = 1000,
    processing_batch_size: int = 10,
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        partition: Partition number
        pipeline_queue: Queue to add items to
        download_images_required: Whether to get presigned URLs for images
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
    """
    try:
        all_dataset_items = get_partition_items(
            rpc,
            dataset_id,
            partition,
            download_images_required,
            request_batch_size,
        )
        processing_batches = chunk_items(
            all_dataset_items,
            processing_batch_size,
        )
        for batch in processing_batches:
            pipeline_queue.put(batch)
        logging.info(
            "Successfully fetched %s items for partition %s",
            len(all_dataset_items),
            partition,
        )
    except Exception as e:
        logging.error(
            "Error processing partition %s: %s",
            partition,
            e,
        )
        traceback.print_exc()


def video_frame_partition_items_producer(
    rpc: Any,
    dataset_id: str,
    partition: int,
    pipeline_queue: Queue,
    download_images_required: bool = False,
    request_batch_size: int = 1000,
    processing_batch_size: int = 10,
    isFileInfoRequired: bool = True,
    input_type: str = "mscoco_video",    
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        partition: Partition number
        pipeline_queue: Queue to add items to
        download_images_required: Whether to get presigned URLs for images
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
    """
    try:
        all_dataset_items = get_video_frame_partition_items(
            rpc,
            dataset_id,
            partition,
            download_images_required,
            request_batch_size,
            isFileInfoRequired,
            input_type
        )
        processing_batches = chunk_items(
            all_dataset_items,
            processing_batch_size,
        )
        for batch in processing_batches:
            pipeline_queue.put(batch)
        logging.info(
            "Successfully fetched %s items for partition %s",
            len(all_dataset_items),
            partition,
        )
    except Exception as e:
        logging.error(
            "Error processing partition %s: %s",
            partition,
            e,
        )
        traceback.print_exc()


def download_samples(
    image_details: Dict[str, Any],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Download sample and update sample details.

    Args:
        image_details: Dictionary containing image metadata
        rpc: RPC client for making API calls
        bucket_alias: Bucket alias
        account_number: Account number

    Returns:
        Updated sample details dictionary
    """
    if image_details.get("is_complete"):
        return image_details
    dataset_item = image_details.get("sample_details")
    try:
        if not dataset_item.get("cloudPath"):
            dataset_item["cloudPath"] = get_batch_pre_signed_download_urls(
                dataset_item.get("fileLocation"),
                rpc,
                bucket_alias,
                account_number,
                project_id=project_id,
            )[dataset_item.get("fileLocation")]
        if not dataset_item.get("local_file_path"):
            dataset_item["local_file_path"] = os.path.join(
                TMP_FOLDER,
                dataset_item["filename"],
            )
        os.makedirs(
            os.path.dirname(dataset_item["local_file_path"]),
            exist_ok=True,
        )
        download_file(
            dataset_item["cloudPath"],
            dataset_item["local_file_path"],
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }
    except Exception as e:
        logging.error(
            "Error downloading image %s: %s",
            dataset_item.get("filename"),
            e,
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }


def get_pre_signed_upload_urls(
    cloud_file_paths,
    rpc,
    file_type,
    bucket_alias="",
    account_number="",
):
    """Get pre-signed upload URLs for files.

    Args:
        cloud_file_paths: Paths of files in cloud storage
        rpc: RPC client for making API calls
        file_type: Type of files
        bucket_alias: Bucket alias
        account_number: Account number

    Returns:
        Response from API containing pre-signed URLs
    """
    logging.debug(
        "Getting presigned URLs for %d files",
        len(cloud_file_paths),
    )
    logging.debug(
        "cloud_file_paths for upload: %s",
        cloud_file_paths,
    )
    if not isinstance(cloud_file_paths, list):
        cloud_file_paths = [cloud_file_paths]
    logging.debug(
        "final cloud_file_paths for upload: %s",
        cloud_file_paths,
    )
    payload_get_presigned_url = {
        "fileNames": cloud_file_paths,
        "type": "samples",
        "isPrivateBucket": (True if bucket_alias else False),
        "bucketAlias": bucket_alias,
        "accountNumber": account_number,
    }
    resp = rpc.post(
        "/v2/dataset/get_batch_pre_signed_upload_urls",
        payload=payload_get_presigned_url,
    )
    logging.debug(
        "payload for getting the presigned urls for first frames: %s",
        payload_get_presigned_url,
    )
    if resp["success"]:
        logging.debug(
            "presiged urls for upload: %s",
            resp["data"],
        )
        return resp["data"]
    else:
        logging.error(
            "Failed to get presigned URLs: %s",
            resp["message"],
        )
        return resp["message"]

def download_video_samples(
    image_details: Dict[str, Any],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Download sample and update sample details.

    Args:
        image_details: Dictionary containing image metadata
        rpc: RPC client for making API calls
        bucket_alias: Bucket alias
        account_number: Account number

    Returns:
        Updated sample details dictionary
    """
    logging.debug(
        "keys of image details are %s",
        image_details.keys(),
    )
    logging.debug("%s", image_details.get("is_complete"))
    logging.debug(
        "image details for download: %s",
        image_details,
    )
    if image_details.get("is_complete"):
        return image_details
    dataset_item = image_details.get("sample_details")
    logging.debug("dataset item is %s", dataset_item)
    file_info_frames = dataset_item["fileInfoResponse"]["frames"]
    _, file_info = next(iter(file_info_frames.items()))
    logging.debug("file info is %s", file_info)
    try:
        if not file_info.get("cloudPath"):
            file_info["cloudPath"] = get_batch_pre_signed_download_urls(
                file_info.get("fileLocation"),
                rpc,
                bucket_alias,
                account_number,
                project_id=project_id
            )[file_info.get("fileLocation")]
        if not dataset_item.get("local_file_path"):
            dataset_item["local_file_path"] = os.path.join(
                TMP_FOLDER,
                file_info["filename"],
            )
        os.makedirs(
            os.path.dirname(dataset_item["local_file_path"]),
            exist_ok=True,
        )
        download_file(
            file_info["cloudPath"],
            dataset_item["local_file_path"],
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }
    except Exception as e:
        logging.error(
            "Error downloading image %s: %s",
            dataset_item.get("filename"),
            e,
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }


def upload_file(local_path, presigned_url, max_attempts=5):
    """Upload a file to a presigned URL.

    Args:
        local_path: Local path of the file to upload
        presigned_url: Pre-signed URL to upload to
        max_attempts: Maximum number of upload attempts

    Returns:
        Boolean indicating success of upload
    """
    logging.debug(
        "Uploading %s to %s",
        local_path,
        presigned_url,
    )
    for attempt in range(max_attempts):
        try:
            with open(local_path, "rb") as f:
                response = requests.put(
                    presigned_url,
                    data=f,
                    allow_redirects=True,
                    timeout=30,
                )
                logging.info(f"response from uploading is {response}")
                if response.status_code == 200:
                    logging.info(
                        "Successfully uploaded %s to %s",
                        local_path,
                        presigned_url,
                    )
                    return True
                else:
                    logging.warning(
                        "Failed to upload %s (status: %s), attempt %s/%s",
                        local_path,
                        response.status_code,
                        attempt + 1,
                        max_attempts,
                    )
                    response.raise_for_status()
        except Exception as e:
            if attempt == max_attempts - 1:
                logging.error(
                    "Failed to upload %s after %s attempts. Error: %s",
                    local_path,
                    max_attempts,
                    e,
                )
                return False
            else:
                logging.warning(
                    "Attempt %s/%s failed for %s. Retrying... Error: %s",
                    attempt + 1,
                    max_attempts,
                    local_path,
                    e,
                )


def upload_video_samples(
    image_details: Dict[str, Any],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
) -> Dict[str, Any]:
    """Upload video samples to storage.

    Args:
        image_details: Dictionary with sample details
        rpc: RPC client for API calls
        bucket_alias: Bucket alias for private storage
        account_number: Account number for private storage

    Returns:
        Updated image details
    """
    dataset_item = image_details.get("sample_details")
    is_complete = image_details.get("is_complete")
    logging.debug(
        "dataset item is %s for upload",
        dataset_item,
    )
    try:
        logging.debug(
            "dataset item key for before fetching url and uploading- %s",
            dataset_item.get("first_frame_upload_cloud_path"),
        )
        if not dataset_item.get("first_frame_upload_cloud_path"):
            logging.debug(
                "getting presigned url by updating the key first_frame_upload_cloud_path %s",
                dataset_item.get("first_frame_upload_cloud_path"),
            )
            cloud_paths_presigned_url_dict = get_pre_signed_upload_urls(
                dataset_item.get("bucket_upload_first_frame_path"),
                rpc,
                bucket_alias,
                account_number,
            )
            logging.info(f"presigned url for upload dictionary is-:{cloud_paths_presigned_url_dict}"),
            dataset_item.update(
                {
                    "first_frame_upload_cloud_path": cloud_paths_presigned_url_dict.get(
                        dataset_item.get("bucket_upload_first_frame_path")
                    )
                }
            )
            logging.info(f"The first frame upload url is {dataset_item.get('first_frame_upload_cloud_path')}")
        upload_file(
            dataset_item["first_frame_path"],
            dataset_item["first_frame_upload_cloud_path"],
        )
        return {
            "sample_details": dataset_item,
            "is_complete": is_complete,
        }
    except Exception as e:
        logging.error(
            "Error uploading sample %s: %s",
            dataset_item.get("filename", "unknown"),
            e,
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }


def batch_download_samples(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Download a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries
        rpc: RPC client for making API calls

    Returns:
        List of updated sample details
    """
    logging.debug(
        "Processing batch of %s samples for download",
        len(batch_image_details),
    )
    return [
        download_samples(
            image_details,
            rpc,
            bucket_alias,
            account_number,
            project_id=project_id
        )
        for image_details in batch_image_details
    ]


def batch_upload_video_samples(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
) -> List[Dict[str, Any]]:
    """Download a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries
        rpc: RPC client for making API calls

    Returns:
        List of updated sample details
    """
    logging.debug(
        "Processing batch of %s samples for upload",
        len(batch_image_details),
    )
    return [
        upload_video_samples(
            image_details,
            rpc,
            bucket_alias,
            account_number,
        )
        for image_details in batch_image_details
    ]

def batch_download_video_samples(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Download a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries
        rpc: RPC client for making API calls

    Returns:
        List of updated sample details
    """
    logging.debug(
        "Processing batch of %s samples for download",
        len(batch_image_details),
    )
    return [
        download_video_samples(
            image_details,
            rpc,
            bucket_alias,
            account_number,
            project_id=project_id,
        )
        for image_details in batch_image_details
    ]


def calculate_image_properties(
    image_details: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate properties of an image.

    Args:
        image_details: Dictionary containing image metadata

    Returns:
        Updated image details with calculated properties
    """
    if image_details.get("is_complete"):
        return image_details
    dataset_item = image_details.get("sample_details")
    try:
        with Image.open(dataset_item["local_file_path"]) as image:
            width, height = image.size
            dataset_item.update(
                {
                    "image_height": height,
                    "image_width": width,
                    "image_area": height * width,
                }
            )
            os.remove(dataset_item["local_file_path"])
            return {
                "sample_details": dataset_item,
                "is_complete": True,
            }
    except Exception as e:
        logging.error(
            "Error processing image %s: %s",
            dataset_item.get("filename"),
            e,
        )
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }


def batch_calculate_sample_properties(
    batch_sample_details: List[Dict[str, Any]],
    properties_calculation_fn: callable,
) -> List[Dict[str, Any]]:
    """Calculate properties for a batch of samples.

    Args:
        batch_image_details: List of image details dictionaries

    Returns:
        List of processed image details
    """
    logging.debug(
        "Processing batch of %s samples for property calculation",
        len(batch_sample_details),
    )
    processed_batch = []
    for dataset_item in batch_sample_details:
        dataset_item = properties_calculation_fn(dataset_item)
        if dataset_item.get("is_complete"):
            processed_batch.append(dataset_item["sample_details"])
    return processed_batch

def batch_update_video_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    project_id: str,
    attempts: int = 3,
) -> List[Dict[str, Any]]:
    """Update video dataset items' metadata and annotations in batch with multithreading.
    
    Args:
        batch_image_details: List of dictionaries containing video details
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        project_id: Project ID for segment annotations
        attempts: Number of retry attempts
        
    Returns:
        Updated batch image details with processing status
    """
    from concurrent.futures import ThreadPoolExecutor
    
    def update_metadata():
        """Update high-level video metadata for all items in batch."""
        high_level_items = []
        processed_ids = set()
        
        for item in batch_image_details:
            if not item.get("fileInfoResponse"):
                continue
                
            file_info = item.get("fileInfoResponse")[0]  # Use first fileInfo for metadata
            dataset_item_id = str(file_info.get("_idVideoDatasetItem"))
            
            if dataset_item_id in processed_ids:
                continue
                
            processed_ids.add(dataset_item_id)
            high_level_items.append({
                "datasetItemId": dataset_item_id,
                "version": version,
                "height": item.get("video_height"),
                "width": item.get("video_width"),
                "area": int(item.get("video_height", 0)) * int(item.get("video_width", 0)),
                "fps": item.get("frame_rate"),
            })
        
        if not high_level_items:
            return True
            
        payload = {
            "datasetId": dataset_id,
            "items": high_level_items,
        }

        logging.debug("Sending metadata update payload with %d items", len(high_level_items))
        resp = rpc.put(
            path="/v2/dataset/update-video-dataset-items/",
            payload=payload,
        )
        
        if not resp or not resp.get("success"):
            logging.error("Failed metadata update: %s", resp.get("data") if resp else "No response")
            return False
            
        return True
    
    def process_segment_chunk(dataset_item_id, file_info_id, sequence_num, split_type, frame_chunk):
        """Process a chunk of frames and return segment data."""
        annotations = {}
        logging.debug("processing frame chunk %s", frame_chunk)
        for frame_id, frame_data in frame_chunk:
            anns=frame_data.get("annotations", [])
            frame_annotations=[]
            for ann in anns:
                ann_dict={
                    "id": ann.get("id"),
                    "segmentation": ann.get("segmentation", []),
                    "isCrowd": ann.get("isCrowd", []),
                    "confidence": 0.0,
                    "bbox": [
                        ann["bbox"][0],
                        ann["bbox"][1],
                        ann["bbox"][2] + ann["bbox"][0],
                        ann["bbox"][3] + ann["bbox"][1],
                    ],
                    "height": ann.get("height"),
                    "width": ann.get("width"),
                    "center": ann.get("center", []),
                    "area": ann.get("area", 0),
                    "category": ann.get("category"),
                    "masks": ann.get("masks", []),
                }
                frame_annotations.append(ann_dict)
            annotations[frame_id] = frame_annotations
            
            
        return {
            "_idFileInfo": file_info_id,
            "itemSetType": split_type,
            "sequenceNum": sequence_num,
            "annotations": annotations,
        }
    
    def update_segments_for_item(item):
        """Update all segments for a single dataset item."""
        file_infos = item.get("fileInfoResponse", [])
        split_type = item.get("splitType")
        
        for file_info in file_infos:
            dataset_item_id = str(file_info.get("_idVideoDatasetItem"))
            file_info_id = str(file_info.get("_id"))
            sequence_num = file_info.get("sequenceNum")
            frames = file_info.get("frames", {})
            
            # Sort frames by ID for consistent chunking
            frame_items = sorted(frames.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0])
            
            # Process frames in chunks of 16
            chunk_size = 16
            segment_chunk_size = 10
            all_segments = []
            
            # Create segments from frame chunks
            for i in range(0, len(frame_items), chunk_size):
                chunk = frame_items[i:i+chunk_size]
                segment = process_segment_chunk(
                    dataset_item_id, file_info_id, sequence_num, split_type, chunk
                )
                all_segments.append(segment)
            
            # Send segments in batches of 10
            for j in range(0, len(all_segments), segment_chunk_size):
                segment_batch = all_segments[j:j+segment_chunk_size]
                segment_payload = {
                    "datasetItemId": dataset_item_id,
                    "version": version,
                    "segments": segment_batch,
                }
                
                logging.debug(
                    "Processing segments %d to %d for item %s",
                    j, min(j+segment_chunk_size, len(all_segments)), dataset_item_id
                )
                
                # Try to update segments with retries
                for attempt in range(3):
                    try:
                        seg_resp = rpc.post(
                            path=f"/v2/dataset/add-video-segment-annotation-items?projectId={project_id}",
                            payload=segment_payload,
                        )
                        
                        if seg_resp and seg_resp.get("success"):
                            break
                        
                        logging.error(
                            "Failed to update segments for item %s (attempt %d/3): %s",
                            dataset_item_id, attempt+1, seg_resp.get("data") if seg_resp else "No response"
                        )
                        
                        if attempt == 2:  # Last attempt failed
                            return False
                            
                        time.sleep(0.5)  # Short delay before retry
                        
                    except Exception as e:
                        logging.error(
                            "Error updating segments for item %s (attempt %d/3): %s",
                            dataset_item_id, attempt+1, e
                        )
                        if attempt == 2:  # Last attempt failed
                            return False
                        time.sleep(0.5)
        
        return True
    
    # Main processing logic with retries
    retry_count = 0
    while retry_count < attempts:
        try:
            # Step 1: Update metadata for all items
            if not update_metadata():
                retry_count += 1
                time.sleep(1)
                continue
                
            # Step 2: Process segments for all items in parallel
            results = []
            with ThreadPoolExecutor(max_workers=min(10, len(batch_image_details))) as executor:
                future_to_item = {executor.submit(update_segments_for_item, item): item 
                                 for item in batch_image_details}
                
                for future in future_to_item:
                    item = future_to_item[future]
                    try:
                        success = future.result()
                        item["status"] = "processed" if success else "errored"
                        results.append(item)
                    except Exception as e:
                        logging.error("Thread exception for item: %s", e)
                        item["status"] = "errored"
                        results.append(item)
            
            # Check if all items were processed successfully
            if all(item["status"] == "processed" for item in batch_image_details):
                return batch_image_details
                
            # If some items failed, retry the whole batch
            retry_count += 1
            
        except Exception as e:
            logging.error("Error in batch update (attempt %d/%d): %s", 
                         retry_count + 1, attempts, e)
            logging.debug("Error traceback: %s", traceback.format_exc())
            retry_count += 1
            time.sleep(1)
    
    # If we've exhausted all attempts, mark remaining items as errored
    for item in batch_image_details:
        if item.get("status") != "processed":
            item["status"] = "errored"
            
    return batch_image_details


# def batch_update_video_dataset_items(
#     batch_image_details: List[Dict[str, Any]],
#     rpc: Any,
#     dataset_id: str,
#     version: str,
#     attempts: int = 3,
#     is_yolo: bool = False,
# ) -> List[Dict[str, Any]]:
#     """Update video dataset items in batch.

#     Args:
#         batch_image_details: List of dictionaries containing image details
#         rpc: RPC client for making API calls
#         dataset_id: ID of the dataset
#         version: Version of the dataset
#         attempts: Number of retry attempts
#         is_yolo: Whether using YOLO format
# wa
#     Returns:
#         Updated batch image details
#     """
#     retry_count = 0
#     logging.debug(
#         "Batch image details are %s",
#         batch_image_details,
#     )
#     while retry_count < attempts:
#         try:
#             logging.debug(
#                 "Attempting to update batch of %s items (attempt %s/%s)",
#                 len(batch_image_details),
#                 retry_count + 1,
#                 attempts,
#             )
#             items = []
#             count_dataset_item=0
#             for dataset_item in batch_image_details:
#                 count_dataset_item+=1
#                 logging.debug(
#                     "Processing dataset item for updating-: %s",
#                     dataset_item,
#                 )
#                 frame_annotations = {}
#                 file_info = dataset_item.get("fileInfoResponse", {})
#                 frames = file_info.get("frames", {})
#                 for (
#                     frame_id,
#                     ann,
#                 ) in frames.items():
#                     frame_annotations[frame_id] = []
#                     frame_annotations[frame_id].append(
#                         {
#                             "id": ann.get("id"),
#                             "segmentation": ann.get("segmentation", []),
#                             "isCrowd": ann.get("isCrowd", []),
#                             "confidence": 0.0,
#                             "bbox": [
#                                 ann["bbox"][0],
#                                 ann["bbox"][1],
#                                 ann["bbox"][2] + ann["bbox"][0],
#                                 ann["bbox"][3] + ann["bbox"][1],
#                             ],
#                             "height": ann.get("height"),
#                             "width": ann.get("width"),
#                             "center": ann.get("center", []),
#                             "area": ann.get("area", 0),
#                             "category": ann.get("category"),
#                             "masks": ann.get("masks", []),
#                         }
#                     )
#                 item = {
#                     "datasetItemId": str(file_info.get("_idVideoDatasetItem")),
#                     "version": str(version),
#                     "splitType": str(dataset_item.get("splitType")),
#                     "frameWiseAnnotations": frame_annotations,
#                     "height": dataset_item.get("video_height"),
#                     "width": dataset_item.get("video_width"),
#                     "area": int(dataset_item.get("video_height"))
#                     * int(dataset_item.get("video_width")),
#                     "fps": dataset_item.get("frame_rate"),
#                 }
#                 items.append(item)
#             payload = {
#                 "datasetId": str(dataset_id),
#                 "items": items,
#             }
#             resp = rpc.put(
#                 path="/v2/dataset/update-video-dataset-items/",
#                 payload=payload,
#             )
#             logging.debug(
#                 "Update dataset items payload: %s",
#                 payload,
#             )
#             if resp.get("success"):
#                 logging.debug(
#                     "Successfully updated batch of %s items",
#                     len(batch_image_details),
#                 )
#                 logging.debug("successfully updated %s number of dataset items",
#                               count_dataset_item)
#                 for item in batch_image_details:
#                     item["status"] = "processed"
#                 return batch_image_details
#             logging.error(
#                 "Failed to update batch: %s",
#                 resp.get("data"),
#             )
#             retry_count += 1
#         except Exception as e:
#             logging.error("Error updating batch: %s", e)
#             retry_count += 1
#     for item in batch_image_details:
#         item["status"] = "errored"
#     return batch_image_details


def batch_update_video_mot_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    project_id: str,
    attempts: int = 3,
    segments_per_request: int = 10,
) -> List[Dict[str, Any]]:
    retry_count = 0

    while retry_count < attempts:
        try:
            # STEP 1: Batch update high-level video metadata
            high_level_items = []
            for item in batch_image_details:
                logging.debug("Processing dataset item for updating: %s", item)
                if item.get("fileInfoResponse"):
                    file_info = item.get("fileInfoResponse")[0]
                high_level_items.append({
                    "datasetItemId": str(file_info.get("_idVideoDatasetItem")),
                    "version": version,
                    "height": item.get("video_height"),
                    "width": item.get("video_width"),
                    "area": int(item.get("video_height")) * int(item.get("video_width")),
                    "fps": item.get("frame_rate"),
                })

            metadata_payload = {
                "datasetId": dataset_id,
                "items": high_level_items,
            }

            resp = rpc.put("/v2/dataset/update-video-dataset-items/", payload=metadata_payload)
            if not resp or not resp.get("success"):
                logging.error("Metadata update failed: %s", resp)
                retry_count += 1
                continue

            # STEP 2: Upload annotations per fileInfo in 16-frame chunks, 10 segments per request
            for item in batch_image_details:
                file_infos = item.get("fileInfoResponse", [])
                split_type = item.get("splitType")
                logging.debug("Processing fileinfos %s", file_infos)
                for file_info in file_infos:
                    dataset_item_id = str(file_info.get("_idVideoDatasetItem"))
                    sequence_num = file_info.get("sequenceNum")
                    frames = file_info.get("frames", {})

                    frame_ids = list(frames.keys())
                    total_frames = len(frame_ids)
                    chunk_size = 16  # Number of frames per segment
                    all_segments = []

                    for i in range(0, total_frames, chunk_size):
                        chunk_frames = frame_ids[i:i + chunk_size]
                        annotations = {}

                        for fid in chunk_frames:
                            frame_data = frames.get(fid, {})
                            anns = frame_data.get("annotations", [])
                            annotations[fid] = []
                            for ann in anns:
                                annotations[fid].append({
                                    "id": ann.get("id"),
                                    "segmentation": ann.get("segmentation", []),
                                    "isCrowd": ann.get("isCrowd", []),
                                    "confidence": ann.get("confidence", 0.5),
                                    "bbox": [
                                        ann["bbox"][0],
                                        ann["bbox"][1],
                                        ann["bbox"][0] + ann["bbox"][2],
                                        ann["bbox"][1] + ann["bbox"][3]
                                    ],
                                    "height": ann.get("height"),
                                    "width": ann.get("width"),
                                    "center": ann.get("center", []),
                                    "area": ann.get("area", 0),
                                    "category": ann.get("category"),
                                    "masks": ann.get("masks", []),
                                })

                        all_segments.append({
                            "_idFileInfo": str(file_info["_id"]),
                            "itemSetType": split_type,
                            "sequenceNum": sequence_num,
                            "annotations": annotations,
                        })

                    # Send segments in batches
                    for j in range(0, len(all_segments), segments_per_request):
                        segment_payload = {
                            "datasetItemId": dataset_item_id,
                            "version": version,
                            "segments": all_segments[j:j + segments_per_request],
                        }

                        logging.debug("payload for segment update: %s", segment_payload)
                        seg_resp = rpc.post(
                            path=f"/v2/dataset/add-video-segment-annotation-items?projectId={project_id}",
                            payload=segment_payload
                        )

                        if not seg_resp or not seg_resp.get("success"):
                            logging.error(
                                "Segment update failed for item %s: %s",
                                dataset_item_id, seg_resp
                            )
                            raise Exception("Segment update failed")

                item["status"] = "processed"

            return batch_image_details

        except Exception as e:
            logging.error("Error during batch update attempt %d: %s", retry_count + 1, e)
            retry_count += 1
            time.sleep(1)

    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details



import time
import logging
from typing import List, Dict, Any

def batch_update_video_davis_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    project_id: str,
    attempts: int = 3,
    batch_segment_limit: int = 10,
    frames_per_segment: int = 16,
) -> List[Dict[str, Any]]:
    """Update high-level video info and segment-wise annotations for DAVIS-style datasets."""

    def create_annotation_payload(annotations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = []
        for ann in annotations:
            if len(ann.get("bbox", [])) >= 4:
                filtered.append({
                    "id": ann.get("id"),
                    "segmentation": ann.get("segmentation", []),
                    "isCrowd": ann.get("isCrowd", []),
                    "confidence": ann.get("confidence", 0.5),
                    "bbox": ann["bbox"][:4],
                    "height": ann.get("height"),
                    "width": ann.get("width"),
                    "center": ann.get("center", []),
                    "area": ann.get("area", 0),
                    "category": ann.get("category"),
                    "masks": ann.get("masks", []),
                })
        if len(filtered) < len(annotations):
            logging.warning("Some annotations were skipped due to invalid bbox.")
        return filtered

    retry_count = 0
    while retry_count < attempts:
        try:
            # Step 1: Batch high-level metadata update
            high_level_items = []
            seen_dataset_item_ids = set()
            for item in batch_image_details:
                logging.debug("Processing dataset item for updating: %s", item)
                file_info = item.get("fileInfoResponse")[0]
                dataset_item_id = str(file_info.get("_idVideoDatasetItem"))
                if dataset_item_id not in seen_dataset_item_ids:
                    seen_dataset_item_ids.add(dataset_item_id)
                    high_level_items.append({
                    "datasetItemId": dataset_item_id,
                    "version": version,
                    "height": item.get("video_height", 0),
                    "width": item.get("video_width", 0),
                    "area": item.get("video_height", 0) * item.get("video_width", 0),
                    "fps": item.get("frame_rate", 0),
                    })

            payload_high_level = {
            "datasetId": dataset_id,
            "items": high_level_items,
            }
            
            logging.debug("High-level metadata update payload: %s", payload_high_level)

            resp = rpc.put("/v2/dataset/update-video-dataset-items/", payload=payload_high_level)
            if not resp or not resp.get("success"):
                logging.error("High-level metadata update failed: %s", resp)
                retry_count += 1
                continue

            # Step 2: Segment-wise annotation update
            for item in batch_image_details:
                item_success = True
                file_info_list = item.get("fileInfoResponse", [])
                split_type = item.get("splitType")

                for file_info in file_info_list:
                    frames = file_info.get("frames", {})
                    sorted_frame_items = sorted(frames.items(), key=lambda x: int(x[0]))
                    segments = []
                    sequence_num = file_info.get("sequenceNum")

                    for i in range(0, len(sorted_frame_items), frames_per_segment):
                        chunk = sorted_frame_items[i: i + frames_per_segment]
                        annotations_dict = {
                            frame_id: create_annotation_payload(frame_data.get("annotations", []))
                            for frame_id, frame_data in chunk
                        }

                        segments.append({
                            "_idFileInfo": str(file_info["_id"]),
                            "itemSetType": split_type,
                            "sequenceNum": sequence_num,
                            "annotations": annotations_dict,
                        })

                        if len(segments) == batch_segment_limit or (i + frames_per_segment >= len(sorted_frame_items)):
                            payload_segments = {
                                "datasetItemId": str(file_info["_idVideoDatasetItem"]),
                                "version": version,
                                "segments": segments,
                            }

                            try:
                                logging.debug("Sending segment annotation update: %s", payload_segments)
                                seg_resp = rpc.post(
                                    f"/v2/dataset/add-video-segment-annotation-items?projectId={project_id}",
                                    payload=payload_segments,
                                )

                                if not seg_resp or not seg_resp.get("success"):
                                    logging.error("Segment update failed for item %s: %s", item.get("_id"), seg_resp)
                                    item_success = False
                                    break

                            except Exception as err:
                                logging.error("Segment update exception for item %s: %s", item.get("_id"), err)
                                item_success = False
                                break

                            segments = []

                item["status"] = "processed" if item_success else "errored"

            return batch_image_details

        except Exception as e:
            logging.error("Batch update attempt %d failed: %s", retry_count + 1, e)
            retry_count += 1
            time.sleep(1)

    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details



def batch_update_video_imagenet_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    is_yolo: bool = False,
    batch_size: int = 30,
) -> List[Dict[str, Any]]:
    """Update dataset items in batch, processing frames in groups of 30.

    Args:
        batch_image_details: List of image details to update
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        is_yolo: Whether the dataset is in YOLO format
        batch_size: Number of frames to process in one API call

    Returns:
        List of updated dataset items
    """
    retry_count = 0
    logging.debug(
        "Batch image %s details are %s",
        dataset_id,
        batch_image_details,
    )
    while retry_count < attempts:
        try:
            logging.debug(
                "Attempting to update batch of %s items (attempt %s/%s)",
                len(batch_image_details),
                retry_count + 1,
                attempts,
            )
            batch_payload_items = []
            for dataset_item in batch_image_details:
                logging.debug(
                    "Processing dataset item for updating: %s",
                    dataset_item,
                )
                frame_annotations = []
                file_info = dataset_item.get("fileInfoResponse", {})[0]
                segment_annotations = dataset_item.get("annotations", [])
                frame_annotations = [
                    {
                        "id": ann.get("id"),
                        "segment": dataset_item.get("segment_duration"),
                        "segmentation": ann.get("segmentation", []),
                        "isCrowd": ann.get("isCrowd", []),
                        "confidence": ann.get("confidence", 0.5),
                        "bbox": ann.get("bbox", []),
                        "height": ann.get("height"),
                        "width": ann.get("width"),
                        "center": ann.get("center", []),
                        "area": ann.get("area", 0),
                        "category": ann.get("category"),
                        "masks": ann.get("masks", []),
                    }
                    for ann in segment_annotations
                ]
                logging.debug(
                    "preview_cloud_path is- %s",
                    dataset_item.get("bucket_upload_first_frame_path"),
                )
                batch_payload_items.append(
                    {
                        "datasetItemId": str(file_info.get("_idVideoDatasetItem")),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "previewFileCloudPath": dataset_item.get("bucket_upload_first_frame_path"),
                        "segmentWiseAnnotations": frame_annotations,
                        "height": dataset_item.get("video_height"),
                        "width": dataset_item.get("video_width"),
                        "area": int(dataset_item.get("video_height", 0))
                        * int(dataset_item.get("video_width", 0)),
                        "fps": dataset_item.get("frame_rate"),
                    }
                )
            payload = {
                "datasetId": str(dataset_id),
                "items": batch_payload_items,
            }
            try:
                logging.debug(
                    "Sending update for frames with payload: %s",
                    payload,
                )
                resp = rpc.put(
                    path="/v2/dataset/update-video-dataset-items/",
                    payload=payload,
                )
                logging.debug(
                    "Response from update-video-dataset-items: %s",
                    resp,
                )
                if resp and resp.get("success"):
                    logging.debug("Successfully updated dataset items!!")
                    for dataset_item in batch_image_details:
                        dataset_item["status"] = "processed"
                    return batch_image_details
                else:
                    error_msg = resp.get("data") if resp else "No response from server"
                    logging.error(
                        "Failed to update dataset items: %s",
                        error_msg,
                    )
            except Exception as rpc_err:
                logging.error(
                    "RPC call failed for dataset batch: %s",
                    rpc_err,
                )
        except Exception as e:
            logging.error("Error updating batch: %s", e)
        retry_count += 1
    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details


def batch_update_kinetics_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    is_yolo: bool = False,
    batch_size: int = 30,
) -> List[Dict[str, Any]]:
    """Update dataset items in batch, processing frames in groups of 30.

    Args:
        batch_image_details: List of image details to update
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        is_yolo: Whether the dataset is in YOLO format
        batch_size: Number of frames to process in one API call

    Returns:
        List of updated dataset items
    """
    retry_count = 0
    logging.debug(
        "Batch image details are %s",
        batch_image_details,
    )
    while retry_count < attempts:
        try:
            logging.debug(
                "Attempting to update batch of %s items (attempt %s/%s)",
                len(batch_image_details),
                retry_count + 1,
                attempts,
            )
            batch_payload_items = []
            for dataset_item in batch_image_details:
                logging.debug(
                    "Processing dataset item for updating: %s",
                    dataset_item,
                )
                frame_annotations = []
                file_info = dataset_item.get("fileInfoResponse", {})[0]
                segment_annotations = dataset_item.get("annotations", [])
                for ann in segment_annotations:
                    frame_annotations.append(
                        {
                            "id": ann.get("id"),
                            "segment": ann.get("duration"),
                            "segmentation": ann.get("segmentation", []),
                            "isCrowd": ann.get("isCrowd", []),
                            "confidence": ann.get("confidence", 0.5),
                            "bbox": ann.get("bbox", []),
                            "order_id": 0,
                            "height": ann.get("height"),
                            "width": ann.get("width"),
                            "center": ann.get("center", []),
                            "area": ann.get("area", 0),
                            "category": ann.get("category"),
                            "masks": ann.get("masks", []),
                        }
                    )
                logging.debug(
                    "preview_cloud_path is- %s",
                    dataset_item.get("bucket_upload_first_frame_path"),
                )
                batch_payload_items.append(
                    {
                        "datasetItemId": str(file_info.get("_idVideoDatasetItem")),
                        "previewFileCloudPath": dataset_item.get("bucket_upload_first_frame_path"),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "segmentWiseAnnotations": frame_annotations,
                        "height": dataset_item.get("video_height"),
                        "width": dataset_item.get("video_width"),
                        "area": int(dataset_item.get("video_height", 0))
                        * int(dataset_item.get("video_width", 0)),
                        "fps": dataset_item.get("frame_rate"),
                    }
                )
            payload = {
                "datasetId": str(dataset_id),
                "items": batch_payload_items,
            }
            try:
                logging.debug(
                    "Sending update for frames with payload: %s",
                    payload,
                )
                resp = rpc.put(
                    path="/v2/dataset/update-video-dataset-items/",
                    payload=payload,
                )
                logging.debug(
                    "Response from update-video-dataset-items: %s",
                    resp,
                )
                if resp and resp.get("success"):
                    logging.debug("Successfully updated dataset items!!")
                    for dataset_item in batch_image_details:
                        dataset_item["status"] = "processed"
                    return batch_image_details
                else:
                    error_msg = resp.get("data") if resp else "No response from server"
                    logging.error(
                        "Failed to update dataset items: %s",
                        error_msg,
                    )
            except Exception as rpc_err:
                logging.error(
                    "RPC call failed for dataset batch: %s",
                    rpc_err,
                )
        except Exception as e:
            logging.error("Error updating batch: %s", e)
        retry_count += 1
    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details

def batch_update_video_mscoco_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    project_id: str,
    attempts: int = 3,
    frames_per_segment: int = 16,
    batch_segment_limit: int = 10,
) -> List[Dict[str, Any]]:
    """Update video metadata and segment-wise annotations in MSCOCO to match DAVIS format."""

    def create_annotation_payload(annotations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter and format valid annotations with proper bounding boxes."""
        filtered = []
        for ann in annotations:
            if len(ann.get("bbox", [])) >= 4:
                filtered.append({
                    "id": ann.get("id"),
                    "segmentation": ann.get("segmentation", []),
                    "isCrowd": ann.get("isCrowd", []),
                    "confidence": ann.get("confidence", 0.5),
                    "bbox": ann["bbox"][:4],
                    "height": ann.get("height"),
                    "width": ann.get("width"),
                    "center": ann.get("center", []),
                    "area": ann.get("area", 0),
                    "category": ann.get("category"),
                    "masks": ann.get("masks", []),
                })
        
        if len(filtered) < len(annotations):
            logging.warning("Some annotations were skipped due to invalid bbox.")
        return filtered

    def update_metadata():
        """Update high-level video metadata for all items in batch."""
        high_level_items = []
        seen_ids = set()
        
        for item in batch_image_details:
            if not item.get("fileInfoResponse"):
                continue
                
            file_info = item.get("fileInfoResponse")[0]
            dataset_item_id = str(file_info.get("_idVideoDatasetItem"))
            
            if dataset_item_id in seen_ids:
                continue
                
            seen_ids.add(dataset_item_id)
            high_level_items.append({
                "datasetItemId": dataset_item_id,
                "version": version,
                "height": item.get("video_height", 0),
                "width": item.get("video_width", 0),
                "area": item.get("video_height", 0) * item.get("video_width", 0),
                "fps": int(item.get("frame_rate", 0)),
            })
        
        if not high_level_items:
            return True
            
        payload = {
            "datasetId": dataset_id,
            "items": high_level_items,
        }
        
        logging.debug("Sending high-level metadata update: %s", payload)
        resp = rpc.put("/v2/dataset/update-video-dataset-items/", payload=payload)
        
        return resp and resp.get("success")

    def process_segments(item):
        """Process segments for a single item."""
        file_info_list = item.get("fileInfoResponse", [])
        split_type = item.get("splitType")
        
        for file_info in file_info_list:
            frames = file_info.get("frames", {})
            sorted_frame_items = sorted(frames.items(), key=lambda x: int(x[0]))
            sequence_num = file_info.get("sequenceNum")
            dataset_item_id = str(file_info["_idVideoDatasetItem"])
            
            for i in range(0, len(sorted_frame_items), frames_per_segment):
                segment_batch = []
                chunk = sorted_frame_items[i:i + frames_per_segment]
                
                annotations_dict = {
                    frame_id: create_annotation_payload(frame_data.get("annotations", []))
                    for frame_id, frame_data in chunk
                }
                
                segment_batch.append({
                    "_idFileInfo": str(file_info["_id"]),
                    "itemSetType": split_type,
                    "sequenceNum": sequence_num,
                    "annotations": annotations_dict,
                })
                
                segment_payload = {
                    "datasetItemId": dataset_item_id,
                    "version": version,
                    "segments": segment_batch,
                }
                
                logging.debug(
                    "Processing segments %d to %d for item %s with payload %s",
                    i, min(i + frames_per_segment, len(sorted_frame_items)),
                    dataset_item_id,
                    segment_payload,
                )
                
                try:
                    seg_resp = rpc.post(
                        f"/v2/dataset/add-video-segment-annotation-items?projectId={project_id}",
                        payload=segment_payload,
                    )
                    if not seg_resp or not seg_resp.get("success"):
                        logging.error("Segment update failed: %s", seg_resp)
                        return False
                except Exception as err:
                    logging.error("Segment update exception: %s", err)
                    return False
                    
        return True

    # Main execution flow
    retry_count = 0
    while retry_count < attempts:
        try:
            # Step 1: Update metadata
            if not update_metadata():
                retry_count += 1
                time.sleep(1)
                continue
            
            # Step 2: Process segments for all items
            for item in batch_image_details:
                success = process_segments(item)
                item["status"] = "processed" if success else "errored"
                
                if not success:
                    break
            
            # Check if all items were processed successfully
            if all(item.get("status") == "processed" for item in batch_image_details):
                return batch_image_details
                
            # If some items failed, retry
            retry_count += 1
            time.sleep(1)
            
        except Exception as e:
            logging.error("Batch update attempt %d failed: %s", retry_count + 1, e)
            logging.debug("Full error traceback: %s", traceback.format_exc())
            retry_count += 1
            time.sleep(1)

    # Mark all remaining items as errored after exhausting retries
    for item in batch_image_details:
        if item.get("status") != "processed":
            item["status"] = "errored"
            
    return batch_image_details


def batch_update_dataset_items(
    batch_image_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    is_yolo: bool = False,
) -> List[Dict[str, Any]]:
    """Update dataset items in batch.

    Args:
        batch_image_details: List of dictionaries containing image details
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        is_yolo: Whether using YOLO format

    Returns:
        Updated batch image details
    """
    retry_count = 0
    max_retries = attempts
    while retry_count < max_retries:
        try:
            payload = {
                "datasetId": str(dataset_id),
                "items": [
                    {
                        "datasetItemId": str(dataset_item.get("_id")),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "annotations": dataset_item.get("annotations"),
                        "height": int(
                            dataset_item.get(
                                "image_height",
                                dataset_item.get("height"),
                            )
                        ),
                        "width": int(
                            dataset_item.get(
                                "image_width",
                                dataset_item.get("width"),
                            )
                        ),
                        "area": int(
                            dataset_item.get(
                                "image_area",
                                dataset_item.get("area"),
                            )
                        ),
                    }
                    for dataset_item in batch_image_details
                ],
            }
            if is_yolo:
                payload = convert_payload_to_coco_format(payload)
            response = rpc.put(
                path="/v2/dataset/update-dataset-items/",
                payload=payload,
            )
            logging.debug(
                "Update dataset items payload: %s",
                payload,
            )
            if response.get("success"):
                logging.debug(
                    "Successfully updated batch of %s items",
                    len(batch_image_details),
                )
                for item in batch_image_details:
                    item["status"] = "processed"
                return batch_image_details
            return batch_image_details
        except Exception as e:
            retry_count += 1
            logging.error(
                "Error updating items (attempt %d/%d): %s",
                retry_count,
                max_retries,
                str(e),
            )
            if retry_count >= max_retries:
                logging.error(
                    "Failed to update items after %d attempts",
                    max_retries,
                )
                return batch_image_details
    for item in batch_image_details:
        item["status"] = "errored"
    return batch_image_details


def submit_partition_status(
    dataset_items_batches: List[List[Dict[str, Any]]],
    rpc: Any,
    action_record_id: str,
    dataset_id: str,
    version: str,
    annotation_type: str,
) -> None:
    """Submit status of processed partition.

    Args:
        dataset_items_batches: List of batches of dataset items
        rpc: RPC client for making API calls
        action_record_id: ID of the action record
        dataset_id: ID of the dataset
        version: Version of the dataset
        annotation_type: Type of annotation
    """
    logging.info(
        "Submitting partition status for dataset %s version %s",
        dataset_id,
        version,
    )
    try:
        partitions_status = {}
        partition_items = {}
        for batch in dataset_items_batches:
            for item in batch:
                partition_num = item.get("partition")
                status = item.get("status")
                if partition_num not in partition_items:
                    partition_items[partition_num] = []
                partition_items[partition_num].append(item)
                if status == "errored":
                    partitions_status[partition_num] = "errored"
                    logging.error(
                        "Partition %s errored",
                        partition_num,
                    )
                elif status == "processed" and partition_num not in partitions_status:
                    partitions_status[partition_num] = "processed"
                    logging.info(
                        "Partition %s processed successfully",
                        partition_num,
                    )
        logging.info(
            "Updating status for %s partitions",
            len(partitions_status),
        )
        for (
            partition_num,
            status,
        ) in partitions_status.items():
            logging.debug(
                "Updating partition %s with status %s and %s items",
                partition_num,
                status,
                len(partition_items[partition_num]),
            )
            update_partition_status(
                rpc,
                action_record_id,
                dataset_id,
                version,
                partition_num,
                status,
                partition_items[partition_num],
                annotation_type,
            )
        logging.debug("Successfully updated partition status")
    except Exception as e:
        logging.error(
            "Error updating partition status: %s",
            e,
        )
        logging.debug(
            "Error details: %s",
            traceback.format_exc(),
        )


def submit_video_frame_partition_status(
    dataset_items_batches: List[List[Dict[str, Any]]],
    rpc: Any,
    action_record_id: str,
    dataset_id: str,
    version: str,
    annotation_type: str,
    sample_stats: Optional[Dict[str, Any]] = None,
) -> None:
    """Submit status updates for processed partitions.

    Args:
        dataset_items_batches: List of processed dataset item batches
        rpc: RPC client for making API calls
        action_record_id: ID of the action record
        dataset_id: ID of the dataset
        version: Version of the dataset
        annotation_type: Type of annotations
    """
    logging.info(
        "Submitting partition status for dataset %s version %s",
        dataset_id,
        version,
    )
    try:
        partitions_status = {}
        partition_items = {}
        for batch in dataset_items_batches:
            for item in batch:
                partition_num = item.get("partition")
                status = item.get("status")
                if partition_num not in partition_items:
                    partition_items[partition_num] = []
                partition_items[partition_num].append(item)
                if status == "errored":
                    partitions_status[partition_num] = "errored"
                    logging.error(
                        "Partition %s errored",
                        partition_num,
                    )
                elif status == "processed" and partition_num not in partitions_status:
                    partitions_status[partition_num] = "processed"
                    logging.info(
                        "Partition %s processed successfully",
                        partition_num,
                    )
        logging.info(
            "Updating status for %s partitions",
            len(partitions_status),
        )
        for (
            partition_num,
            status,
        ) in partitions_status.items():
            logging.debug(
                "Updating partition %s with status %s and %s items",
                partition_num,
                status,
                len(partition_items[partition_num]),
            )
            update_video_frame_partition_status(
                rpc,
                action_record_id,
                dataset_id,
                version,
                partition_num,
                status,
                partition_items[partition_num],
                annotation_type,
                sample_stats,
            )
            logging.info(
                "Successfully marked partition %s as %s",
                partition_num,
                status,
            )
    except Exception as e:
        logging.error(
            "Failed to submit partition status: %s",
            e,
        )
        logging.debug(
            "Full error traceback: %s",
            traceback.format_exc(),
        )


def get_annotation_files(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    is_annotations_compressed: bool = False,
) -> List[str]:
    """Download and return paths to annotation files.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        is_annotations_compressed: Whether annotations are in compressed format

    Returns:
        List of local paths to downloaded annotation files
    """
    logging.info(
        "Getting annotation files for dataset %s",
        dataset_id,
    )
    response = rpc_get_call(
        rpc,
        f"/v2/dataset/list-annotation-files/{dataset_id}/{dataset_version}",
        {},
    )
    annotation_files = []
    annotation_dir = os.path.join(TMP_FOLDER, "annotations")
    os.makedirs(annotation_dir, exist_ok=True)
    for s3_url in response:
        try:
            file_name = get_filename_from_url(s3_url)
            file_path = os.path.join(annotation_dir, file_name)
            os.makedirs(
                os.path.dirname(file_path),
                exist_ok=True,
            )
            download_file(s3_url, file_path)
            if is_annotations_compressed:
                annotation_files.extend(scan_folder(extract_dataset(file_path)))
            else:
                annotation_files.append(file_path)
            logging.debug(
                "Downloaded annotation file %s",
                annotation_files,
            )
        except Exception as e:
            logging.error(
                "Error downloading annotation file %s: %s",
                s3_url,
                e,
            )
    logging.info(
        "Found %s annotation files: %s",
        len(annotation_files),
        annotation_files,
    )
    return annotation_files


def get_mscoco_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing MSCOCO image details")
        images_details = get_msococo_images_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_mscoco_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise


def get_imagenet_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id:str="",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_imagenet_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise


def get_pascalvoc_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str="",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=True,
        )
        logging.info("Processing Pascal image details")
        (
            images_details,
            missing_annotations,
            classwise_splits,
        ) = get_pascalvoc_image_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_pascalvoc_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_labelbox_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing Labelbox image details")
        (
            images_details,
            missing_annotations,
            classwise_splits,
        ) = get_labelbox_image_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_labelbox_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Add Dataset Item Local File Path",
            process_fn=add_labelbox_dataset_item_local_file_path,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"base_dataset_path": dataset_id},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise


def get_labelbox_classification_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing Labelbox image details")
        (
            images_details,
            missing_annotations,
            classwise_splits,
        ) = get_labelbox_classification_image_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_labelbox_classification_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Add Dataset Item Local File Path",
            process_fn=add_labelbox_classification_dataset_item_local_file_path,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={"base_dataset_path": dataset_id},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise


def get_yolo_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
):
    """Create and configure the processing pipeline.
    Args:

        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=True,
        )
        logging.info("Processing Pascal image details")
        (
            images_details,
            missing_annotations,
            classwise_splits,
        ) = get_yolo_image_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_yolo_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "is_yolo": True,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_unlabelled_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_unlabelled_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise


def get_video_youtube_bb_tracking_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=False,
        )
        logging.debug(
            "Annotation files: %s",
            annotation_files,
        )
        logging.info("Processing Youtube BB Frames details")
        (
            images_details,
            missing_annotations,
            classwise_splits,
        ) = get_youtube_bb_video_frame_details(annotation_files)
        logging.debug(
            "Annotation details: %s",
            images_details,
        )
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                    "isFileInfoRequired": True,
                    "input_type": "youtube_bb",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_youtube_bb_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"frames_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "project_id": project_id
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Youtube BB pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_video_mot_tracking_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=True,
        )
        logging.debug(
            "Annotation files: %s",
            annotation_files,
        )
        logging.info("Processing MOT Frames details")
        images_details, sample_stats = get_mot_annotations(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                    "isFileInfoRequired": True,
                    "input_type": "mot",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_mot_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"frames_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_mot_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "project_id": project_id
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "object_tracking",
                "sample_stats": sample_stats,
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_video_davis_segmentation_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=True,
        )
        logging.debug(
            "Annotation files: %s",
            annotation_files,
        )
        logging.info("Processing MOT Frames details")
        images_details, davis_sample_stats = get_davis_annotations(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                    "isFileInfoRequired": True,
                    "input_type": "davis",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_davis_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"frames_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_davis_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "project_id": project_id
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "segmentation",
                "sample_stats": davis_sample_stats,
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_video_imagenet_classification_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        upload_first_frame_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                    "isFileInfoRequired": True,
                    "input_type": "video_imagenet",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_video_imagenet_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=upload_first_frame_queue,
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Upload First frame",
            process_fn=batch_upload_video_samples,
            pull_queue=upload_first_frame_queue,
            push_queue=download_images_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_imagenet_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "classification",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_kinetics_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=False,
        )
        logging.debug(
            "Annotation files: %s",
            annotation_files,
        )
        logging.info("Processing Kinetics Frames details")
        images_details = get_kinetics_annotations(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        upload_first_frame_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": True,
                    "isFileInfoRequired": True,
                    "input_type": "kinetics",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_kinetics_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=upload_first_frame_queue,
            process_params={"frames_details": images_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Upload First frame",
            process_fn=batch_upload_video_samples,
            pull_queue=upload_first_frame_queue,
            push_queue=download_images_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_kinetics_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "kinetics",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise


def get_video_mscoco_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(
            rpc,
            dataset_id,
            dataset_version,
            is_annotations_compressed=False,
        )
        logging.debug(
            "Annotation files: %s",
            annotation_files,
        )
        logging.info("Processing MSCOCO Frames details")
        images_details, _, _ = get_video_mscoco_annotations(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        upload_first_frame_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=video_frame_partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                    "isFileInfoRequired": True,
                    "input_type": "mscoco_video",
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_video_mscoco_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"frames_details": images_details},
            num_threads=5,
        )
        
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=batch_download_video_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=10,
        )
        pipeline.add_stage(
            stage_name="Calculate Image Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_image_properties},
            num_threads=10,
        )

        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_mscoco_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "project_id": project_id,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_video_frame_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection_mscoco",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(
            "Error setting up Pascal VOC pipeline: %s",
            e,
        )
        traceback.print_exc()
        raise
