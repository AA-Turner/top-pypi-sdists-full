"""Module providing data_prep functionality."""

import logging
import os
import json
import time
import random
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from typing import Any, Dict, List, Tuple, Optional
import yaml
from collections import defaultdict
import threading
import cv2
import shutil
import uuid
from PIL import Image
from urllib.parse import urlparse
from matrice.data_processing.server_utils import (
    download_file,
    chunk_items,
    get_number_of_dataset_batches,
    get_data_prep_batch_video_dataset_items,
    get_batch_dataset_items
)
from matrice.data_processing.pipeline import (
    Pipeline,
)


def dataset_items_producer(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    pipeline_queue: Queue,
    request_batch_size: int = 1000,
    processing_batch_size: int = 10,
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Dataset version
        pipeline_queue: Queue to add items to
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
    """
    try:
        number_of_dataset_pages = get_number_of_dataset_batches(
            rpc, dataset_id, dataset_version, request_batch_size
        )
        if number_of_dataset_pages == 0:
            logging.warning(
                "No items found for dataset %s version %s",
                dataset_id,
                dataset_version,
            )
            return []

        def process_page(page_number: int) -> int:
            try:
                items = get_batch_dataset_items(
                    rpc, dataset_id, dataset_version, page_number, request_batch_size
                )
                for batch in chunk_items(items, processing_batch_size):
                    pipeline_queue.put(batch)
            except Exception as e:
                logging.error(f"Error processing page {page_number}: {str(e)}")
                return 0

        # Process pages in parallel and count total items
        with ThreadPoolExecutor() as executor:
            total_items = sum(
                executor.map(process_page, range(number_of_dataset_pages))
            )

        logging.info(
            "Successfully fetched %d items for dataset version %s",
            total_items,
            dataset_version,
        )

    except Exception as exc:
        logging.error(
            "Error processing dataset version %s: %s",
            dataset_version,
            exc,
        )
        raise

def video_dataset_items_producer(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    pipeline_queue: Queue,
    request_batch_size: int = 50,
    processing_batch_size: int = 1,
    input_type: str = "davis",
) -> None:
    """Get items for a partition and add them to the pipeline queue.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Dataset version
        pipeline_queue: Queue to add items to
        request_batch_size: Number of items to fetch per API request
        processing_batch_size: Size of batches to add to pipeline queue
        input_type: Type of input data format
    """
    try:
        number_of_dataset_pages = get_number_of_dataset_batches(
            rpc, dataset_id, dataset_version, request_batch_size
        )
        if number_of_dataset_pages == 0:
            logging.warning(
                "No items found for dataset %s version %s",
                dataset_id,
                dataset_version,
            )
            return []

        def process_page(page_number: int) -> int:
            try:
                items = get_data_prep_batch_video_dataset_items(
                    rpc,
                    dataset_id,
                    dataset_version,
                    page_number,
                    request_batch_size,
                    input_type,
                )
                for batch in chunk_items(items, processing_batch_size):
                    pipeline_queue.put(batch)
                return len(items)
            except Exception as e:
                logging.error(f"Error processing page {page_number}: {str(e)}")
                return 0

        # Process pages in parallel and count total items
        with ThreadPoolExecutor() as executor:
            total_items = sum(
                executor.map(process_page, range(number_of_dataset_pages))
            )

        logging.info(
            "Successfully fetched %d items for dataset version %s",
            total_items,
            dataset_version,
        )

    except Exception as exc:
        logging.error(
            "Error processing dataset version %s: %s",
            dataset_version,
            exc,
        )
        raise


def process_final_annotations(
    dataset_items: List[List[Dict]],
    base_dataset_path: str,
    input_format: str,
    dataset_version: str,
) -> None:
    """Process final annotations after pipeline completion.

    Args:
        dataset_items: List of dataset items to process
        base_dataset_path: Base path to save dataset files
        input_format: Format of annotations (YOLO/COCO)
        dataset_version: Dataset version
    """
    if not dataset_items:
        logging.warning("No items to process for annotations")
        return
    dataset_items = [item for batch in dataset_items for item in batch]
    logging.info(
        "Processing final annotations for %d items",
        len(dataset_items),
    )
    logging.debug("Base dataset path: %s", base_dataset_path)
    logging.debug("Input format: %s", input_format)
    input_format = input_format.lower()
    if input_format == "yolo":
        logging.info("Writing YOLO format labels")
        write_yolo_labels(
            base_dataset_path,
            dataset_items,
            dataset_version,
        )
    elif input_format == 'kinetics':
        write_kinetics_labels(
            base_dataset_path,
            dataset_items,
            dataset_version,
        )
    elif input_format == 'mscoco_video':
        write_video_coco_annotations(
            base_dataset_path,
            dataset_items,
            dataset_version,
        )
    
    elif input_format=='davis':
        write_davis_yolo_annotations(
            base_dataset_path,
            dataset_items,
            dataset_version,
        )
    elif input_format in ["mscoco", "coco"]:
        logging.info("Writing MSCOCO format annotations")
        write_mscoco_annotation_files(
            base_dataset_path,
            dataset_items,
            dataset_version,
        )
    logging.info("DATA PREP SUCCESS")


def get_item_set_type(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> str:
    """Get the set type (train/test/val) for a dataset item."""
    for info in dataset_item["versionInfo"]:
        if info["version"] == dataset_version:
            return info.get("itemSetType", "unassigned")
    return "unassigned"

def get_video_item_set_type(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> str:
    """Get the set type (train/test/val) for a dataset item."""
    for info in dataset_item["annotationInfo"]:
        if info["version"] == dataset_version:
            return info.get("itemSetType", "unassigned")
    return "unassigned"


def get_image_annotations(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> List[Dict]:
    """Get annotations for a dataset item."""
    for info in dataset_item["versionInfo"]:
        if info["version"] == dataset_version:
            return info.get("annotation", [])
    return []

def get_kinetics_annotations(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> List[Dict]:
    """Get annotations for a dataset item."""
    # Handle Kinetics-style: annotations directly under dataset_item
    if "annotationInfo" in dataset_item:
        return dataset_item["annotationInfo"]

    # Standard handling via versionInfo
    for info in dataset_item.get("versionInfo", []):
        if info.get("version") == dataset_version:
            return info.get("annotation", [])
    
    return []

def get_kinetics_category_name(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> str:
    """Get category name from dataset item annotations."""
    annotations = get_kinetics_annotations(dataset_item, dataset_version)
    if annotations:
        return annotations[0].get("video")[0].get("category")
    return None


def get_category_name(
    dataset_item: Dict,
    dataset_version: str = "v1.0",
) -> str:
    """Get category name from dataset item annotations."""
    annotations = get_image_annotations(dataset_item, dataset_version)
    if annotations:
        return annotations[0]["category"]
    return None

def get_video_save_path(
    base_dataset_path: str,
    dataset_item: Dict,
    input_format: str,
    dataset_version: str,
) -> str:
    """Get save path for an image or video.

    Args:
        base_dataset_path: Base path to save dataset
        dataset_item: Dataset item containing media info
        input_format: Format of dataset
        dataset_version: Dataset version

    Returns:
        Full path where media should be saved
    """
    item_set_type = get_video_item_set_type(dataset_item, dataset_version)

    if input_format in ["kinetics"]:
        image_name = dataset_item.get("fileInfo", {})[0].get("video", {}).get("filename", "").split("/")[-1]
    else:
        image_name = dataset_item.get("filename", "").split("/")[-1]

    if not image_name or item_set_type not in ["train", "test", "val", "unassigned"]:
        return None

    if input_format=='kinetics':
        category = get_kinetics_category_name(dataset_item, dataset_version)
        if not category:
            return None
    
        save_path = os.path.dirname(
            f"{base_dataset_path}/videos/{item_set_type}/{category}/{image_name}"
        )
    elif input_format=='mscoco_video':
        save_path = os.path.dirname(
            f"{base_dataset_path}/videos/{item_set_type}/{image_name}"
        )
    os.makedirs(save_path, exist_ok=True)
    return os.path.join(save_path, image_name)


def get_image_path(
    base_dataset_path: str,
    dataset_item: Dict,
    input_format: str,
    dataset_version: str,
) -> str:
    """Get save path for an image.

    Args:
        base_dataset_path: Base path to save dataset
        dataset_item: Dataset item containing image info
        input_format: Format of dataset
        dataset_version: Dataset version

    Returns:
        Full path where image should be saved
    """
    item_set_type = get_item_set_type(dataset_item, dataset_version)
    image_name = dataset_item["filename"].split("/")[-1]
    if item_set_type not in [
        "train",
        "test",
        "val",
    ]:
        return None
    if "imagenet" in input_format.lower():
        category = get_category_name(dataset_item, dataset_version)
        if not category:
            return None
        save_path = os.path.dirname(
            f"{base_dataset_path}/images/{item_set_type}/{category}/{image_name}"
        )
    else:
        save_path = os.path.dirname(f"{base_dataset_path}/images/{item_set_type}/{image_name}")
    os.makedirs(save_path, exist_ok=True)
    return os.path.join(save_path, image_name)


def map_frames_to_split(response_dict):
    """
    Given a dictionary with keys 'fileInfoResponse' and 'annotationResponse',
    return a mapping from unique frame key to its split.

    Unique frame key format: "<_idDataset>_<idVideoDatasetItem>_<sequenceNum>_<frameNum>"

    Args:
        response_dict (dict): {
            "fileInfoResponse": [dict, ...],
            "annotationResponse": [dict, ...]
        }

    Returns:
        dict: Mapping from unique frame ID to split (e.g., 'train', 'val', 'test').
    """
    annotation_responses = response_dict.get("annotationInfo", [])
    frame_split_lookup = {}

    for annotation in annotation_responses:
        dataset_id = annotation["_idDataset"]
        video_id = annotation["_idVideoDatasetItem"]
        sequence_num = annotation["sequenceNum"]
        split = annotation.get("itemSetType", "unknown")

        frames = annotation.get("frames", {})
        for frame_num in frames:
            unique_frame_key = f"{dataset_id}_{video_id}_{sequence_num}_{frame_num}"
            frame_split_lookup[unique_frame_key] = split

    # Print all unique splits
    unique_splits = set(frame_split_lookup.values())
    logging.debug("Unique splits from map: %s", unique_splits)

    return frame_split_lookup

def download_davis_yolo_frames(
    dataset_item: Dict,
    base_dataset_path: str,
    dataset_version: str,
    frame_split_map: Optional[Dict[Tuple[str, str], str]] = None
) -> None:
    frame_to_split = map_frames_to_split(dataset_item)
    dataset_id = dataset_item.get("_idDataset", "")
    file_info_list = dataset_item.get("fileInfo", [])
    annotation_info_list = dataset_item.get("annotationInfo", [])  # Now a list
    item_id = dataset_item.get("_id", "")
    item_set_type = get_video_item_set_type(dataset_item, dataset_version)
    split_set = set()
    # Aggregate all frame annotations into one dict: {frame_id: [annotations]}
    annotations = {}
    for entry in annotation_info_list:
        frames = entry.get("frames", {})
        for frame_id, ann_list in frames.items():
            if frame_id not in annotations:
                annotations[frame_id] = []
            annotations[frame_id].extend(ann_list)

    for file_info in file_info_list:
        frames = file_info.get("frames", {})
        sequence_num = file_info.get("sequenceNum", "")
        for frame_id, frame_data in frames.items():
            frame_annotations = annotations.get(frame_id, [])
            filename = os.path.splitext(frame_data.get("filename", ""))[0]
            cloud_path = frame_data.get("fileLocation")

            if not filename or not cloud_path:
                continue

            split = frame_to_split.get(f"{dataset_id}_{item_id}_{sequence_num}_{frame_id}", item_set_type)
            split_set.add(split)
            # You'll need to decide how to derive categories if not explicitly present
            categories = {ann.get("category", "unknown") for ann in frame_annotations}

            for category in categories:
                renamed_filename = f"{filename}_{category}.jpg"
                save_dir = os.path.join(base_dataset_path, "images", split)
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, renamed_filename)

                try:
                    download_file(cloud_path, save_path)
                    logging.info(f"Downloaded {renamed_filename} to {save_path}")
                except Exception as e:
                    logging.error(f"Failed to download {renamed_filename}: {e}")
    logging.debug("Unique splits: %s", split_set)


def extract_video_name_from_url(url: str) -> str:
    """Extracts video name from the frame's URL path."""
    path_parts = urlparse(url).path.split('/')
    try:
        # Assuming path format: .../<split>/<video_name>/<frame>.jpg
        return path_parts[-2]  # second last part of the path
    except IndexError:
        logging.warning(f"Unexpected URL format: {url}")
        return "unknown_video"


def download_frame_with_retry(
    cloud_path: str, 
    local_path: str, 
    frame_num: int, 
    max_retries: int = 5,
    timeout: int = 60
) -> Optional[str]:
    """
    Download a frame with retry logic and enhanced validation.
    
    Args:
        cloud_path: Cloud storage path
        local_path: Local destination path
        frame_num: Frame number for logging
        max_retries: Maximum number of retry attempts
        timeout: Timeout for download in seconds
    
    Returns:
        Local path if successful, None otherwise
    """
    result = None
    if os.path.exists(local_path):
        logging.warning(f"Frame {frame_num}: File already exists at {local_path}, skipping")
        return local_path
    try:
        result = download_file(cloud_path, local_path, max_retries=max_retries, timeout=timeout)
        
        # Validate file exists and has content
        if not os.path.exists(result) or os.path.getsize(result) == 0:
            raise Exception(f"Frame {frame_num}: Downloaded file is empty or missing")
        
        # PIL validation - verify image integrity
        try:
            with Image.open(result) as img:
                if img is None:
                    raise Exception(f"Frame {frame_num}: PIL Image.open() returned None")
                
                # Verify file integrity
                img.verify()
                
            # Load image data with fresh PIL object to check dimensions
            with Image.open(result) as fresh_img:
                fresh_img.load()
                width, height = fresh_img.size
                
                if width <= 0 or height <= 0:
                    raise Exception(f"Frame {frame_num}: Invalid PIL dimensions {width}x{height}")
                
                    
        except Exception as pil_error:
            raise Exception(f"Frame {frame_num}: PIL validation failed - {pil_error}")

        # OpenCV validation
        try:
            test_img = cv2.imread(result)
            if test_img is None or test_img.size == 0:
                raise Exception(f"Frame {frame_num}: OpenCV could not read image")
                
            if test_img.shape[0] <= 0 or test_img.shape[1] <= 0:
                raise Exception(f"Frame {frame_num}: Invalid OpenCV dimensions {test_img.shape}")
                                 
        except Exception as cv_error:
            raise Exception(f"Frame {frame_num}: OpenCV validation failed - {cv_error}")
        
        return result
        
    except Exception as e:
        logging.error(f"Failed to download/validate frame {frame_num}: {e}")
        
        # Clean up corrupted file
        if result and os.path.exists(result):
            try:
                os.remove(result)
                logging.debug(f"Removed corrupted file: {result}")
            except Exception as cleanup_error:
                logging.warning(f"Failed to remove corrupted frame {frame_num}: {cleanup_error}")
                
        return None


def get_optimal_video_params(target_width: int, target_height: int, fps: float) -> dict:
    """
    Get optimal video encoding parameters based on dimensions and FPS.
    
    Args:
        target_width: Video width
        target_height: Video height
        fps: Frames per second
        
    Returns:
        Dictionary with optimal video parameters
    """
    # Validate and fix dimensions
    if target_width <= 1 or target_height <= 1:
        target_width = 640  # Default width
        target_height = 480  # Default height
        logging.warning(f"Invalid dimensions detected, using defaults: {target_width}x{target_height}")
    
    # Ensure dimensions are even (required by many codecs)
    if target_width % 2 != 0:
        target_width += 1
    if target_height % 2 != 0:
        target_height += 1
    
    # Validate and fix FPS
    if not fps or fps <= 0:
        fps = 30.0
        logging.warning(f"Invalid FPS detected, using default: {fps}")

    # Default parameters
    params = {
        'fourcc': None,
        'fps': fps,
        'frame_size': (target_width, target_height)
    }
    
    # Try different codecs in order of preference
    codecs_to_try = [
        ('mp4v', 'mp4v'),  # MPEG-4 - usually most compatible
        ('XVID', 'XVID'),  # Xvid codec
        ('MJPG', 'MJPG'),  # Motion JPEG - fallback option
        ('avc1', 'avc1'),  # H.264
        ('H264', 'H264'),  # Alternative H.264
    ]
    
    # Add platform-specific codecs
    if os.name == 'nt':  # Windows
        codecs_to_try.append(('DIVX', 'DIVX'))
    
    for codec_name, codec_chars in codecs_to_try:
        try:
            # Try to initialize the codec
            fourcc = cv2.VideoWriter_fourcc(*codec_chars)
            
            # Test codec compatibility with a temporary video writer
            temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"test_{codec_name}.mp4")
            test_writer = cv2.VideoWriter(
                temp_path,
                fourcc,
                params['fps'],
                params['frame_size'],
                True  # isColor parameter
            )
            
            if test_writer.isOpened():
                test_writer.release()
                # Clean up test file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                params['fourcc'] = fourcc
                logging.info(f"Successfully initialized {codec_name} codec")
                return params
            else:
                test_writer.release()
                logging.debug(f"Could not initialize {codec_name} codec")
                
        except Exception as e:
            logging.debug(f"Failed to initialize {codec_name} codec: {e}")
            continue
    
    # If all else fails, use a basic codec without testing
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        params['fourcc'] = fourcc
        logging.warning("All codec tests failed, using mp4v without validation")
        return params
    except Exception as e:
        logging.error(f"Failed to initialize any codec including mp4v: {e}")
    
    # Final fallback - try MJPG which is usually available
    try:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        params['fourcc'] = fourcc
        logging.warning("Using MJPG codec as final fallback")
        return params
    except Exception as e:
        logging.error(f"Failed to initialize MJPG fallback codec: {e}")
    
    raise RuntimeError("Failed to initialize any video codec")


def check_image_validity(local_filename: str, frame_num: int) -> Optional[str]:
    """
    Helper function to validate downloaded image files.
    
    Args:
        local_filename: Path to the downloaded file
        frame_num: Frame number for logging
        
    Returns:
        Local filename if valid, None otherwise
    """
    try:
        # Basic validation - check if file exists and has reasonable size
        if not os.path.exists(local_filename):
            logging.warning(f"Frame {frame_num}: Downloaded file does not exist at {local_filename}")
            return None
            
        file_size = os.path.getsize(local_filename)
        if file_size == 0:
            logging.warning(f"Frame {frame_num}: Downloaded file is empty")
            if os.path.exists(local_filename):
                os.remove(local_filename)
            return None
        
        # Check for common image file signatures (magic bytes)
        try:
            with open(local_filename, 'rb') as f:
                header = f.read(12)  # Read first 12 bytes
                
            # Check for common image format signatures
            is_valid_image = False
            if header.startswith(b'\xFF\xD8\xFF'):  # JPEG
                is_valid_image = True
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                is_valid_image = True
            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):  # GIF
                is_valid_image = True
            elif header.startswith(b'RIFF') and b'WEBP' in header:  # WebP
                is_valid_image = True
            elif header.startswith(b'BM'):  # BMP
                is_valid_image = True
            else:
                is_valid_image = False

            if not is_valid_image:
                # Check if it's HTML error page
                if header.lower().startswith(b'<!doctype') or header.lower().startswith(b'<html'):
                    logging.warning(f"Frame {frame_num}: Downloaded HTML instead of image (likely 403/404 error)")
                else:
                    logging.warning(f"Frame {frame_num}: Downloaded file does not have valid image signature")
                
                if os.path.exists(local_filename):
                    os.remove(local_filename)
                return None
                
        except Exception as e:
            logging.warning(f"Frame {frame_num}: Could not read file header for validation: {e}")
            if os.path.exists(local_filename):
                os.remove(local_filename)
            return None
        
        # Additional PIL validation for image integrity
        try:
            with Image.open(local_filename) as img:
                img.verify()  # Verify image integrity
                
            # Load image data with fresh PIL object to check dimensions
            with Image.open(local_filename) as fresh_img:
                fresh_img.load()
                width, height = fresh_img.size
                
                if width <= 0 or height <= 0:
                    logging.warning(f"Frame {frame_num}: Invalid PIL dimensions {width}x{height}")
                    if os.path.exists(local_filename):
                        os.remove(local_filename)
                    return None
                
                if width < 10 or height < 10:
                    logging.warning(f"Frame {frame_num}: Suspiciously small dimensions {width}x{height}")
                    if os.path.exists(local_filename):
                        os.remove(local_filename)
                    return None
                    
        except Exception as pil_error:
            logging.warning(f"Frame {frame_num}: PIL validation failed - {pil_error}")
            if os.path.exists(local_filename):
                os.remove(local_filename)
            return None
        
        return local_filename
        
    except Exception as e:
        logging.error(f"Frame {frame_num}: Unexpected error during validation: {e}")
        if os.path.exists(local_filename):
            try:
                os.remove(local_filename)
            except Exception:
                pass
        return None


def create_video_from_frames_mscoco(
    dataset_item: Dict,
    base_dataset_path: str,
    dataset_version: str
) -> None:
    """
    Creates a video for each dataset item using its frames with safe threading and unique naming.
    
    This function handles cases where multiple dataset items share the same video name but belong 
    to different splits by incorporating the dataset item ID into the filename for uniqueness.
    It also implements thread-safe operations to prevent race conditions during concurrent processing.

    Args:
        dataset_item (Dict): Contains '_id', 'fileInfo', etc.
        base_dataset_path (str): Base path to save videos.
        dataset_version (str): Version of the dataset used to determine split type.
    """
    
    def get_frames_info(file_info_list: List[Dict]) -> Dict[int, Dict]:
        """Extract frame information from file info list."""
        frames_info: Dict[int, Dict] = {}

        for file_info in file_info_list:
            frames = file_info.get("frames", {})
            for frame_id, frame_data in frames.items():
                filename = frame_data.get("filename", "")
                cloud_path = frame_data.get("fileLocation", "")
                if not filename or not cloud_path:
                    continue
                try:
                    frame_num = int(os.path.splitext(filename)[0])
                    frames_info[frame_num] = {"cloud_path": cloud_path, "filename": filename}
                except ValueError:
                    logging.warning(f"Invalid frame number in filename: {filename}")

        if not frames_info:
            logging.warning("No valid frames found in dataset_item")
            return {}
        return frames_info

    def prepare_video_save_path(frames_info: Dict[int, Dict], base_dataset_path: str, dataset_version: str) -> Tuple[str, str, str]:
        """Prepare video save path and temporary directory."""
        video_name = f"{extract_video_name_from_url(list(frames_info.values())[0]['cloud_path'])}.mp4"
        split_type = get_video_item_set_type(dataset_item, dataset_version)
        video_path = os.path.join(base_dataset_path,
                                "videos",
                                split_type,
                                video_name)
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        
        # Skip if video already exists
        if os.path.exists(video_path):
            logging.info(f"Video already exists at: {video_path}, skipping")
            return None, None, None

        # Create temporary frame folder with unique naming to avoid conflicts
        video_name_without_ext = os.path.splitext(video_name)[0]
        temp_dir = os.path.join(base_dataset_path, "temp_frames", split_type, video_name_without_ext)
        os.makedirs(temp_dir, exist_ok=True)
        
        return video_name, video_path, temp_dir

    def download_frames(frames_info: Dict[int, Dict], temp_dir: str) -> Dict[int, str]:
        """Download frames in parallel with validation."""
        # Prepare frames for download
        frames_with_paths = [(frame_num, frame_data['cloud_path']) for frame_num, frame_data in frames_info.items()]

        # Download frames and create video
        frame_files_dict = {}
    
        # Download frames in parallel
        max_workers = min(50, len(frames_with_paths) // 20)
        logging.info(f"Starting download of {len(frames_with_paths)} frames with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_frame = {
                executor.submit(
                    download_frame_with_retry,
                    cloud_path,
                    os.path.join(temp_dir, f"{frame_num:06d}.jpg"),
                    frame_num
                ): (frame_num, cloud_path)
                for frame_num, cloud_path in frames_with_paths
            }
            
            for future in as_completed(future_to_frame):
                frame_num, _ = future_to_frame[future]
                try:
                    local_filename = future.result()
                    if local_filename:
                        frame_files_dict[frame_num] = local_filename
                        
                        # Additional validation check # TODO: Enable this
                        # validated_filename = check_image_validity(local_filename, frame_num)
                        # if validated_filename:
                        #     last_valid_frame = local_filename
                        #     frame_files_dict[frame_num] = validated_filename
                        
                    # else: # TODO: Enable this after testing that frames are not corrupted
                    #     if last_valid_frame:
                    #         logging.error(f"Failed to download frame {frame_num}, will use the last valid frame")
                    #         frame_files_dict[frame_num] = last_valid_frame                            
                        
                except Exception as e:
                    logging.error(f"Failed to process frame {frame_num}: {e}")

        if not frame_files_dict:
            logging.warning(f"No frames were downloaded for video in temp directory: {temp_dir}")
            return {}

        return frame_files_dict
    
    def create_video_file(frame_files_dict: Dict[int, str], video_path: str, temp_dir: str, dataset_item: Dict) -> bool:
        """Create the actual video file from downloaded frames with thread-safe operations."""
        try:
            # Double-check if video already exists (thread safety)
            if os.path.exists(video_path):
                logging.info(f"Video already exists at: {video_path}, skipping creation")
                return True
            # Determine video dimensions from the first valid frame
            target_width = None
            target_height = None
            first_frame = None
            
            for frame_path in frame_files_dict.values():
                first_frame = cv2.imread(frame_path)
                if first_frame is not None:
                    target_height, target_width = first_frame.shape[:2]
                    logging.info(f"Frame dimensions detected: {target_width}x{target_height}")
                    break
            
            if first_frame is None:
                logging.error("Could not read any valid frames")
                return False
                
            if target_width is None or target_height is None or target_width <= 1 or target_height <= 1:
                target_width = 640
                target_height = 480
                logging.warning(f"Invalid dimensions detected, using defaults: {target_width}x{target_height}")

            # Get FPS from dataset item
            try:
                fps = float(dataset_item.get("fps", 30.0))
            except (TypeError, ValueError):
                fps = 30.0
                logging.warning("Invalid or missing fps, defaulting to 30.0")
            
            # Get optimal video parameters
            try:
                video_params = get_optimal_video_params(target_width, target_height, fps)
            except RuntimeError as e:
                logging.error(f"Failed to get video parameters: {e}")
                return False

            logging.info(f"Creating video: {video_path} (width={target_width}, height={target_height}, fps={video_params['fps']})")
            
            # Create a temporary video file
            video_name = os.path.basename(video_path)
            temp_video_path = os.path.join(temp_dir, video_name)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(temp_video_path), exist_ok=True)
            
            # Create video writer with better error handling
            out = None
            try:
                out = cv2.VideoWriter(
                    temp_video_path,
                    video_params['fourcc'],
                    video_params['fps'],
                    video_params['frame_size'],
                    True  # isColor
                )
                
                if not out or not out.isOpened():
                    logging.error(f"Failed to create video writer for {temp_video_path}")
                    logging.error(f"Video parameters: fourcc={video_params['fourcc']}, fps={video_params['fps']}, size={video_params['frame_size']}")
                    return False

                # Process frames sequentially
                sorted_frame_nums = sorted(frame_files_dict.keys())
                frames_written = 0
                
                for frame_num in sorted_frame_nums:
                    frame_path = frame_files_dict[frame_num]
                    
                    if not os.path.exists(frame_path):
                        logging.warning(f"Frame file not found: {frame_path}")
                        continue
                        
                    file_size = os.path.getsize(frame_path)
                    if file_size == 0:
                        logging.warning(f"Frame file is empty: {frame_path}")
                        continue
                    
                    img = cv2.imread(frame_path)
                    
                    if img is None:
                        logging.warning(f"Could not read frame {frame_num} at path: {frame_path} (size: {file_size} bytes)")
                        continue
                    
                    # Resize frame if needed
                    if img.shape[:2] != (target_height, target_width):
                        try:
                            img = cv2.resize(img, (target_width, target_height))
                        except Exception as e:
                            logging.warning(f"Failed to resize frame {frame_num}: {e}")
                            continue
                    
                    # Write frame to video
                    try:
                        out.write(img)
                        frames_written += 1
                    except Exception as e:
                        logging.error(f"Failed to write frame {frame_num} to video: {e}")
                        continue
                    
                    if frames_written % 100 == 0:
                        logging.info(f"Processed {frames_written}/{len(sorted_frame_nums)} frames")
                
                if frames_written == 0:
                    logging.error("No frames were written to video")
                    return False
                
                logging.info(f"Successfully wrote {frames_written} frames to video")
                
            finally:
                if out:
                    out.release()
            
            # Verify the created video
            if not os.path.exists(temp_video_path):
                logging.error(f"Temporary video file was not created: {temp_video_path}")
                return False
                
            file_size = os.path.getsize(temp_video_path)
            if file_size == 0:
                logging.error(f"Created video file is empty: {temp_video_path}")
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                return False
            
            cap = cv2.VideoCapture(temp_video_path)
            if not cap.isOpened():
                logging.error("Failed to verify created video")
                cap.release()
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                return False
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            
            if frame_count == 0:
                logging.error("Created video has no frames")
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                return False
            
            # Move temp video to final location
            try:
                shutil.move(temp_video_path, video_path)
                logging.info(f"Successfully created video with {frame_count} frames at: {video_path}")
                return True
            except Exception as e:
                logging.error(f"Failed to move video from {temp_video_path} to {video_path}: {e}")
                return False
                
        except Exception as e:
            logging.error(f"Error creating video: {e}")
            # Clean up temporary video if it exists
            temp_video_path = os.path.join(temp_dir, os.path.basename(video_path))
            if os.path.exists(temp_video_path):
                try:
                    os.remove(temp_video_path)
                except Exception:
                    pass
            return False
    
    # Main execution flow
    frames_info = get_frames_info(dataset_item.get("fileInfo", []))
    if not frames_info:
        logging.warning("No frames found for dataset item")
        return
    
    video_name, video_path, temp_dir = prepare_video_save_path(frames_info, base_dataset_path, dataset_version)
    if not video_path:  # Video already exists
        return

    try:
        frame_files_dict = download_frames(frames_info, temp_dir)
        if not frame_files_dict:
            logging.error(f"Failed to download frames for video {video_name}")
            return
        
        logging.info(f"Successfully downloaded {len(frame_files_dict)} out of {len(frames_info)} frames")

        # Create the video file
        success = create_video_file(frame_files_dict, video_path, temp_dir, dataset_item)
        if not success:
            logging.error(f"Failed to create video {video_name}")
            
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            logging.warning(f"Failed to remove temporary directory {temp_dir}: {e}")
  
# def download_davis_yolo_frames(dataset_item: Dict, base_dataset_path: str, dataset_version: str) -> None:
#     frames = dataset_item.get("fileInfoResponse", {}).get("frames", {})
#     annotations = dataset_item.get("annotationResponse", {}).get("frames", {})
#     item_set_type = get_item_set_type(dataset_item, dataset_version)

#     logging.info(f"Processing dataset item for set type: {item_set_type}")

#     for frame_idx_str, frame_data in frames.items():
#         filename = os.path.splitext(frame_data.get("filename", ""))[0]  # e.g., "00012"
#         cloud_path = frame_data.get("cloudPath")

#         if not filename or not cloud_path:
#             logging.warning(f"Skipping frame {frame_idx_str} due to missing filename or cloud path.")
#             continue

#         frame_annotations = annotations.get(frame_idx_str, [])
#         categories = {ann["category"] for ann in frame_annotations if "category" in ann}

#         for category in categories:
#             renamed_filename = f"{filename}_{category}.jpg"
#             save_dir = os.path.join(base_dataset_path, "images", item_set_type)
#             os.makedirs(save_dir, exist_ok=True)

#             # Log folder creation
#             logging.info(f"Ensured directory exists: {save_dir}")

#             save_path = os.path.join(save_dir, renamed_filename)

#             try:
#                 download_file(cloud_path, save_path)
#                 logging.info(f"Downloaded and saved file: {save_path}")
#             except Exception as exc:
#                 logging.error(f"Failed to download YOLO frame {renamed_filename}: {exc}")


def download_segment_videos(
    dataset_items: List[Dict],
    input_format: str,
    base_dataset_path: str,
    dataset_version: str,
) -> List[Dict]:
    downloaded_items = []
    for dataset_item in dataset_items:
        try:
            if input_format == "davis":
                download_davis_yolo_frames(dataset_item, base_dataset_path, dataset_version)
                downloaded_items.append(dataset_item)
            elif input_format == "mscoco_video":
                create_video_from_frames_mscoco(dataset_item, base_dataset_path, dataset_version)
                downloaded_items.append(dataset_item)
            else:
                save_path = get_video_save_path(
                    base_dataset_path,
                    dataset_item,
                    input_format,
                    dataset_version,
                )
                file_location = dataset_item.get("fileInfo", {})[0].get("video", []).get("fileLocation")
                filename = dataset_item.get("fileInfo", {})[0].get("video", []).get("filename")

                if save_path and file_location:
                    download_file(file_location, save_path)
                    logging.info("Video file saved at: %s", save_path)
                    downloaded_items.append(dataset_item)
                else:
                    logging.warning("Skipping download for %s - Invalid path or missing URL", filename)
        except Exception as exc:
            logging.error("Error downloading dataset item: %s", str(exc))
    return downloaded_items


def download_images(
    dataset_items: List[Dict],
    input_format: str,
    base_dataset_path: str,
    dataset_version: str,
) -> List[Dict]:
    """Download images for dataset items.

    Args:
        dataset_items: List of dataset items
        input_format: Format of dataset
        base_dataset_path: Base path to save images
        dataset_version: Dataset version

    Returns:
        List of successfully downloaded items
    """
    downloaded_images = []
    for dataset_item in dataset_items:
        try:
            save_path = get_image_path(
                base_dataset_path,
                dataset_item,
                input_format,
                dataset_version,
            )
            if save_path and dataset_item.get("fileLocation"):
                download_file(
                    dataset_item["fileLocation"],
                    save_path,
                )
                downloaded_images.append(dataset_item)
            else:
                logging.warning(
                    "Skipping download for %s - Invalid path or missing URL",
                    dataset_item["filename"],
                )
        except Exception as exc:
            logging.error(
                "Error downloading image %s: %s",
                dataset_item["filename"],
                str(exc),
            )
    return downloaded_images


def convert_bbox_coco2yolo(
    img_width: int,
    img_height: int,
    bbox: List[float],
) -> List[float]:
    """Convert COCO format bounding box to YOLO format.

    Args:
        img_width: Width of image
        img_height: Height of image
        bbox: Bounding box in COCO format [x,y,w,h]

    Returns:
        Bounding box in YOLO format [x_center,y_center,w,h]
    """
    if not all(isinstance(x, (int, float)) for x in bbox):
        raise ValueError("Invalid bbox format - all values must be numeric")
    x_tl, y_tl, w, h = bbox
    if img_width <= 0 or img_height <= 0:
        raise ValueError("Invalid image dimensions")
    dw = 1.0 / img_width
    dh = 1.0 / img_height
    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0
    x_coord = x_center * dw
    y_coord = y_center * dh
    w_norm = w * dw
    h_norm = h * dh
    return [x_coord, y_coord, w_norm, h_norm]


def detect_and_convert_bbox_format(
    img_width: int,
    img_height: int,
    bbox: List[float],
) -> List[float]:
    """Detect bbox format and convert to YOLO format.
    
    Supports multiple bbox formats:
    - COCO: [x, y, width, height] (top-left + size)
    - XYXY: [x1, y1, x2, y2] (two corners)
    - Already normalized: values between 0-1
    
    Args:
        img_width: Width of image
        img_height: Height of image
        bbox: Bounding box in any supported format
        
    Returns:
        Bounding box in YOLO format [x_center,y_center,w,h] (normalized)
    """
    if not bbox or len(bbox) != 4:
        raise ValueError("Bbox must have exactly 4 values")
        
    if not all(isinstance(x, (int, float)) for x in bbox):
        raise ValueError("Invalid bbox format - all values must be numeric")
        
    if img_width <= 0 or img_height <= 0:
        raise ValueError("Invalid image dimensions")
    
    x1, y1, x2, y2 = bbox
    
    # Check if already normalized (all values between 0-1)
    if all(0 <= val <= 1 for val in bbox):
        # Assume it's in YOLO format already, or normalized XYXY
        if x2 < x1 or y2 < y1:
            # Likely YOLO format [cx, cy, w, h] - return as is
            return bbox
        else:
            # Normalized XYXY format - convert to YOLO
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1
            return [cx, cy, w, h]
    
    # Check if it's XYXY format (x2 > x1 and y2 > y1)
    if x2 > x1 and y2 > y1:
        # XYXY format: [x1, y1, x2, y2]
        cx = ((x1 + x2) / 2) / img_width
        cy = ((y1 + y2) / 2) / img_height
        w = (x2 - x1) / img_width
        h = (y2 - y1) / img_height
        return [cx, cy, w, h]
    
    # Assume COCO format: [x, y, width, height]
    return convert_bbox_coco2yolo(img_width, img_height, bbox)


def write_data_yaml(
    categories_id_map: Dict[str, int],
    yaml_file_path: str,
) -> None:
    """Write category data to YAML file.

    Args:
        categories_id_map: Dictionary mapping categories to IDs
        yaml_file_path: Path to save YAML file
    """
    if not categories_id_map:
        raise ValueError("Categories dictionary is empty")
    data = {
        "train": "images/train",
        "test": "images/test",
        "val": "images/val",
        "nc": len(categories_id_map),
        "names": {v: k for k, v in categories_id_map.items()},
    }
    os.makedirs(
        os.path.dirname(yaml_file_path),
        exist_ok=True,
    )
    with open(yaml_file_path, "w", encoding="utf-8") as yaml_file:
        yaml.dump(
            data,
            yaml_file,
            default_flow_style=False,
        )

def write_kinetics_labels(
    local_path: str,
    dataset_items: List[Dict],
    dataset_version: str,
) -> None:
    """
    Write Kinetics format labels (CSV) for videos.

    Args:
        local_path: Base path to save annotations.
        dataset_items: List of dataset items (videos).
        dataset_version: Dataset version (e.g., v1.0).
    """
    os.makedirs(f"{local_path}/annotations", exist_ok=True)

    # Output CSV files for each split
    csv_paths = {
        "train": f"{local_path}/annotations/train.csv",
        "val": f"{local_path}/annotations/val.csv",
        "test": f"{local_path}/annotations/test.csv",
    }

    csv_files = {
        split: open(path, "w", newline='', encoding="utf-8")
        for split, path in csv_paths.items()
    }

    csv_writers = {
        split: csv.writer(file)
        for split, file in csv_files.items()
    }

    # Write headers
    for writer in csv_writers.values():
        writer.writerow(["label", "youtube_id", "time_start", "time_end", "split", "is_cc"])

    for video in dataset_items:
        item_version_info = next(
            (v for v in video.get("versionInfo", []) if v["version"] == dataset_version),
            None
        )
        if not item_version_info:
            logging.warning("Skipping video %s - no matching version info", video.get("_id"))
            continue


        annotations = video.get("annotationInfo", [])
        video_filename = video.get("fileInfo", [])[0].get("video", {}).get("filename", "")
        youtube_id = os.path.splitext(video_filename)[0]

        for annotation_obj in annotations:
            try:
                all_annotation=annotation_obj.get("video", [])
                split_type = annotation_obj.get("itemSetType")
                if split_type not in csv_writers:
                    logging.warning("Skipping video %s - invalid split type: %s", video.get("_id"), split_type)
                    continue
                for annotation in all_annotation:
                    label = annotation["category"]
                    time_start, time_end = annotation["segment"]
                    csv_writers[split_type].writerow([
                        label, youtube_id, time_start, time_end, split_type, 0  # is_cc = 0
                    ])
            except Exception as e:
                logging.error("Error processing annotation for video %s: %s", video.get("_id"), str(e))

    # Close CSV files and log saving locations
    for split, file in csv_files.items():
        file.close()
        logging.info("%s annotations saved to: %s", split.capitalize(), csv_paths[split])


def write_video_coco_annotations(
    local_path: str,
    dataset_items: List[Dict],
    dataset_version: str,
) -> None:
    # First pass: collect all categories across all splits
    all_categories = set()
    for video in dataset_items:
        for ann in video.get("annotationInfo", []):
            if ann.get("version") != dataset_version:
                continue
            for frame_data in ann.get("frames", {}).values():
                for frame_anns in frame_data:
                    category = frame_anns.get("category")
                    if category:
                        all_categories.add(category)
    
    # Create consistent category mapping
    category_to_index = {}
    for idx, cat in enumerate(sorted(all_categories), start=1):
        category_to_index[cat] = idx
    
    # Create category list for COCO format
    categories_list = [
        {
            "id": cat_id,
            "name": cat_name,
            "supercategory": "object"
        }
        for cat_name, cat_id in sorted(category_to_index.items(), key=lambda x: x[1])
    ]
    
    # Process each split
    for split in ["train", "val", "test"]:
        json_path = f"{local_path}/annotations/{split}.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        # Initialize data structure
        coco_data = {
            "annotations": [],
            "categories": categories_list,  # Same categories for all splits
            "videos": [],
            "info": {
                "contributor": "Converted from YouTube",
                "date_created": "2025-03-25",
                "description": f"YouTube Video Dataset MSCOCO format - {split}",
                "version": "1.0",
                "year": 2024
            }
        }
        
        annotation_counter = 1
        
        # Process videos
        for video in dataset_items:
            # Get video name from the first frame's file location
            first_frame_info = list(video.get("fileInfo")[0]['frames'].values())[0]
            video_name = extract_video_name_from_url(first_frame_info['fileLocation'])
            
            # Extract video ID from video name (e.g., "video_001" -> 1)
            try:
                video_id = int(video_name.split('_')[-1])
            except (ValueError, IndexError):
                logging.warning(f"Could not extract ID from video name: {video_name}")
                continue
            
            # Check if this video has annotations for this split
            has_split_annotations = False
            for ann in video.get("annotationInfo", []):
                if (ann.get("version") == dataset_version and 
                    ann.get("itemSetType") == split):
                    has_split_annotations = True
                    break
            
            if not has_split_annotations:
                continue
                
            # Add video entry once per video
            coco_data["videos"].append({
                "id": video_id,
                "file_name": video_name,
                "fps": video.get("fps", 24),
                "frames": len(video.get("fileInfo")[0].get("frames", [])),
                "height": video.get("height", 480),
                "width": video.get("width", 640),
            })
            
            # Process annotations for this video
            # Use a set to track unique annotations per frame
            seen_annotations = set()
            
            for ann in video.get("annotationInfo", []):
                if (ann.get("version") != dataset_version or 
                    ann.get("itemSetType") != split):
                    continue
                
                for frame_id, frame_data in ann.get("frames", {}).items():
                    # Ensure frame_data is iterable
                    if not isinstance(frame_data, list):
                        frame_data = [frame_data]
                    
                    for frame_anns in frame_data:
                        if not frame_anns.get("category"):
                            continue
                        
                        # Create unique identifier for this annotation
                        ann_key = (
                            video_id,
                            int(frame_id),
                            frame_anns.get("category"),
                            str(frame_anns.get("bbox", [])),
                            str(frame_anns.get("segmentation", []))
                        )
                        
                        if ann_key in seen_annotations:
                            continue
                        seen_annotations.add(ann_key)
                        
                        category = frame_anns["category"]
                        category_id = category_to_index[category]
                        
                        coco_data["annotations"].append({
                            "id": annotation_counter,
                            "video_id": video_id,
                            "category_id": category_id,
                            "bbox": frame_anns.get("bbox", []),
                            "segmentation": frame_anns.get("segmentation", []),
                            "area": frame_anns.get("area", 0),
                            "iscrowd": 0,
                            "frame_id": int(frame_id),
                        })
                        annotation_counter += 1
        
        # Write JSON file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(coco_data, f, indent=4)
        
        logging.info(f"Saved {split} annotations to {json_path}")

def write_yolo_labels(
    local_path: str,
    dataset_items: List[Dict],
    dataset_version: str,
) -> None:
    """Write YOLO format labels for images.

    Args:
        local_path: Base path to save labels
        dataset_items: List of dataset items
        dataset_version: Dataset version
    """
    os.makedirs(f"{local_path}/labels", exist_ok=True)
    categories_id_map = get_categories_id_map(dataset_items, start_id=0)
    for image in dataset_items:
        img_name = image["filename"].split("/")[-1]
        item_set_type = get_item_set_type(image, dataset_version)
        if not item_set_type:
            logging.warning(
                "Skipping %s - no valid set type",
                img_name,
            )
            continue
        os.makedirs(
            f"{local_path}/labels/{item_set_type}",
            exist_ok=True,
        )
        anno_txt = f"{local_path}/labels/{item_set_type}/{'.'.join(img_name.split('.')[:-1])}.txt"
        with open(anno_txt, "w", encoding="utf-8") as file:
            for anno in get_image_annotations(image, dataset_version):
                try:
                    (
                        x_coord,
                        y_coord,
                        w_norm,
                        h_norm,
                    ) = convert_bbox_coco2yolo(
                        image["width"],
                        image["height"],
                        anno["bbox"],
                    )
                    category = anno["category"]
                    category_id = categories_id_map.get(category)
                    if category_id is None:
                        logging.warning(
                            "Unknown category %s in %s",
                            category,
                            img_name,
                        )
                        continue
                    file.write(
                        f"""{category_id} {x_coord:.6f} {y_coord:.6f} {w_norm:.6f} {h_norm:.6f}
"""
                    )
                    if "segmentation" in anno and anno.get("segmentation"):
                        segmentation_points_list = []
                        for segmentation in anno.get("segmentation", []):
                            if any(isinstance(point, str) for point in segmentation):
                                continue
                            segmentation_points = [
                                str(float(point) / image["width"]) for point in segmentation
                            ]
                            segmentation_points_list.append(" ".join(segmentation_points))
                        segmentation_points_string = " ".join(segmentation_points_list)
                        file.write(f"{category_id} {segmentation_points_string}\n")
                except Exception as exc:
                    logging.error(
                        "Error processing annotation in %s: %s",
                        img_name,
                        str(exc),
                    )
    write_data_yaml(
        categories_id_map,
        f"{local_path}/data.yaml",
    )

def segment_and_split_by_category(
    dataset_items: List[Dict],
    n_frames_per_segment: int = 2,
    split_ratios: Tuple[float, float, float] = (0.8, 0.1, 0.1),
    seed: int = 42
) -> Dict[str, str]:
    """
    Returns a mapping of frame IDs (video_id + frame_id) to split types.
    Groups frames category-wise into segments of n frames,
    then splits them into train/val/test.
    """
    random.seed(seed)
    category_to_frames = defaultdict(list)

    # Collect frames by category
    for video in dataset_items:
        video_id = video.get("_id", "")
        annotations = video.get("annotationResponse", {}).get("frames", {})
        for frame_id, anns in annotations.items():
            for ann in anns:
                category = ann.get("category")
                print('SSC', category)
                if category:
                    frame_key = (video_id, frame_id)
                    print('SSC', frame_key)
                    category_to_frames[category].append(frame_key)

    # Create segments and assign splits
    frame_split_map = {}
    for category, frames in category_to_frames.items():
        # Sort by (video_id, frame_id) to ensure continuity
        sorted_frames = sorted(frames, key=lambda x: (x[0], int(x[1])))
        print('SSC', sorted_frames)
        # Break into segments
        segments = [
            sorted_frames[i:i + n_frames_per_segment]
            for i in range(0, len(sorted_frames), n_frames_per_segment)
        ]
        random.shuffle(segments)

        n_total = len(segments)
        n_train = int(n_total * split_ratios[0])
        n_val = int(n_total * split_ratios[1])
        n_test = n_total - n_train - n_val

        split_assignments = (
            ["train"] * n_train + ["val"] * n_val + ["test"] * n_test
        )

        for segment, split in zip(segments, split_assignments):
            for frame_key in segment:
                frame_split_map[frame_key] = split

    return frame_split_map


def write_davis_yolo_annotations(
    local_path: str,
    dataset_items: List[Dict],
    dataset_version: str,
) -> None:
    split_category_map = defaultdict(set)
    category_seen_in_splits = defaultdict(set)
    frame_split_map = {}

    # Step 1: Track categories and splits
    logging.info("dataset_items: %s", dataset_items)
    for video in dataset_items:
        annotation_responses = video.get("annotationInfo", [])

        for ann in annotation_responses:
            if ann.get("version") != dataset_version:
                logging.warning("Skipping annotation - version mismatch")
                continue
            split_type = ann.get("itemSetType")
            logging.debug("Processing split type while writing label annotation files: %s", split_type)
            frames = ann.get("frames", {})
            for frame_id, frame_data in frames.items():
                for frame_annotations in frame_data:
                    cat = frame_annotations.get("category")
                    if cat:
                        if split_type not in category_seen_in_splits[cat]:
                            category_seen_in_splits[cat].add(split_type)
                            if len(category_seen_in_splits[cat]) > 1:
                                print(f"Category '{cat}' found in multiple splits: {category_seen_in_splits[cat]}")
                        split_category_map[split_type].add(cat)

    # Step 2: Create YOLO folders
    for split in ["train", "val", "test"]:
        os.makedirs(f"{local_path}/labels/{split}", exist_ok=True)
    os.makedirs(f"{local_path}/ImageSets", exist_ok=True)

    # Step 3: Build category index
    all_categories = set()
    for video in dataset_items:
        for ann in video.get("annotationInfo", []):
            if ann.get("version") != dataset_version:
                continue
            frames = ann.get("frames", {})
            for frame_id, frame_data in frames.items():
                for frame_anns in frame_data:
                    if frame_anns.get("category"):
                        all_categories.add(frame_anns["category"])

    category_to_index = {cat: idx for idx, cat in enumerate(sorted(all_categories))}
    logging.info("Categories collected: %s", category_to_index)

    # Step 4: Write annotations and prepare split lists
    split_files = defaultdict(list)
    for video in dataset_items:
        video_id = video.get("_id", "")
        annotation_lookup = {}
        fileinfo_lookup = {}

        for ann in video.get("annotationInfo", []):
            if ann.get("version") != dataset_version:
                continue
            split = ann.get("itemSetType")
            for frame_id, frame_anns in ann.get("frames", {}).items():
                annotation_lookup[frame_id] = (split, frame_anns)

        for file_info in video.get("fileInfo", []):
            for frame_id, frame_data in file_info.get("frames", {}).items():
                fileinfo_lookup[frame_id] = frame_data

        img_width = video.get("width", 366)
        img_height = video.get("height", 220)
        if img_height == 0:
            img_height = 220
        if img_width == 0:  
            img_width = 366

        for frame_id, frame_data in fileinfo_lookup.items():
            frame_filename = frame_data.get("filename")
            base_filename = os.path.basename(os.path.splitext(frame_filename)[0])
            if not frame_filename:
                continue

            split, frame_annotations = annotation_lookup.get(frame_id, (None, []))
            if not frame_annotations:
                continue

            for ann in frame_annotations:
                category = ann.get("category")
                if not category or category not in category_to_index:
                    logging.warning("Skipping annotation - invalid category: %s", category)
                    continue

                class_index = category_to_index[category]
                label_filename = f"{base_filename}_{category}.txt"
                label_path = f"{local_path}/labels/{split}/{label_filename}"

                with open(label_path, "w", encoding="utf-8") as f:
                    segments = ann.get("segmentation", [])
                    bbox = ann.get("bbox", [])

                    # Handle bounding box annotations
                    if not segments and len(bbox) == 4:
                        try:
                            # Validate image dimensions
                            if img_width <= 0 or img_height <= 0:
                                logging.warning(f"Invalid image dimensions for {base_filename}: {img_width}x{img_height}")
                                continue
                                
                            # Use the smart bbox format detection and conversion
                            yolo_bbox = detect_and_convert_bbox_format(img_width, img_height, bbox)
                            xc, yc, w_norm, h_norm = yolo_bbox
                            
                            # Validate normalized coordinates are within bounds
                            if not (0 <= xc <= 1 and 0 <= yc <= 1 and 0 <= w_norm <= 1 and 0 <= h_norm <= 1):
                                logging.warning(f"Normalized bbox out of bounds for {base_filename}: "
                                              f"center=({xc:.3f}, {yc:.3f}), size=({w_norm:.3f}, {h_norm:.3f})")
                                # Clamp values to valid range
                                xc = max(0, min(1, xc))
                                yc = max(0, min(1, yc))
                                w_norm = max(0, min(1, w_norm))
                                h_norm = max(0, min(1, h_norm))
                            
                            f.write(f"{class_index} {xc:.6f} {yc:.6f} {w_norm:.6f} {h_norm:.6f}\n")
                            
                        except Exception as e:
                            logging.error(f"Error converting bbox for {base_filename}: {e}")
                            logging.debug(f"bbox={bbox}, img_size=({img_width}, {img_height})")
                            continue
                    
                    # Handle segmentation annotations
                    elif segments:
                        for segment in segments:
                            if len(segment) < 4:
                                continue
                            try:
                                # Validate and normalize segmentation coordinates
                                normalized_coords = []
                                for i in range(0, len(segment), 2):
                                    if i + 1 < len(segment):
                                        x = float(segment[i]) / img_width
                                        y = float(segment[i + 1]) / img_height
                                        
                                        # Clamp coordinates to valid range
                                        x = max(0, min(1, x))
                                        y = max(0, min(1, y))
                                        
                                        normalized_coords.append(f"{x:.6f}")
                                        normalized_coords.append(f"{y:.6f}")
                                
                                if normalized_coords:
                                    f.write(f"{class_index} " + " ".join(normalized_coords) + "\n")
                                    
                            except Exception as e:
                                logging.error(f"Error processing segmentation for {base_filename}: {e}")
                                continue

                split_files[split].append(label_filename)

    # Step 5: Write split files
    for split, filenames in split_files.items():
        with open(f"{local_path}/ImageSets/{split}.txt", "w", encoding="utf-8") as f:
            for name in sorted(set(filenames)):
                f.write(f"{name}\n")
        logging.info("Saved split file for %s with %d entries", split, len(filenames))

    # Step 6: Write data.yaml
    yaml_path = f"{local_path}/data.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        # f.write(f"path: {local_path}\n")
        f.write("train: images/train\nval: images/val\ntest: images/test\n\n")
        f.write("names:\n")
        for cat, idx in category_to_index.items():
            f.write(f"  {idx}: {cat}\n")
    logging.info("Wrote data.yaml at %s", yaml_path)
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_contents = f.read()
    logging.debug("Contents of data.yaml:\n%s", yaml_contents)


# def write_davis_yolo_annotations(
#     local_path: str,
#     dataset_items: List[Dict],
#     dataset_version: str,
# ) -> None:
#     # Create directories
#     for split in ["train", "val", "test"]:
#         split_label_dir = f"{local_path}/labels/{split}"
#         split_image_dir = f"{local_path}/images/{split}"
#         os.makedirs(split_label_dir, exist_ok=True)
#         os.makedirs(split_image_dir, exist_ok=True)
#         logging.info("Created directories: %s and %s", split_label_dir, split_image_dir)

#     imageset_dir = f"{local_path}/ImageSets"
#     os.makedirs(imageset_dir, exist_ok=True)
#     logging.info("Created directory: %s", imageset_dir)

#     # Initialize split lists
#     splits = {"train": [], "val": [], "test": []}

#     # Collect all unique categories
#     all_categories = set()
#     for video in dataset_items:
#         for frame_annotations in video.get("annotationResponse", {}).get("frames", {}).values():
#             for annotation in frame_annotations:
#                 category = annotation.get("category")
#                 if category:
#                     all_categories.add(category)

#     category_to_index = {category: idx for idx, category in enumerate(sorted(all_categories))}
#     logging.info("Collected categories: %s", category_to_index)

#     for video in dataset_items:
#         item_version_info = next(
#             (v for v in video.get("versionInfo", []) if v["version"] == dataset_version),
#             None
#         )
#         if not item_version_info:
#             logging.warning("Skipping video %s - no matching version info", video.get("_id"))
#             continue

#         split_type = item_version_info.get("itemSetType")
#         if split_type not in splits:
#             logging.warning("Skipping video %s - invalid split type: %s", video.get("_id"), split_type)
#             continue

#         annotation_response = video.get("annotationResponse", {})
#         frames_info = video.get("fileInfoResponse", {}).get("frames", {})

#         for frame_id, frame_info in frames_info.items():
#             frame_filename = frame_info.get("filename")
#             if not frame_filename:
#                 continue

#             frame_annotations = annotation_response.get("frames", {}).get(frame_id, [])
#             if not frame_annotations:
#                 continue

#             base_filename = os.path.splitext(frame_filename)[0]

#             for annotation in frame_annotations:
#                 segments = annotation.get("segmentation", [])
#                 category = annotation.get("category")
#                 if not category or category not in category_to_index or not segments:
#                     continue

#                 class_index = category_to_index[category]
#                 img_width = video.get("width", 1)
#                 img_height = video.get("height", 1)

#                 renamed_filename = f"{base_filename}_{category}"
#                 annotation_path = f"{local_path}/labels/{split_type}/{renamed_filename}.txt"

#                 try:
#                     with open(annotation_path, "w", encoding="utf-8") as f:
#                         for segment in segments:
#                             if len(segment) < 4:
#                                 continue
#                             line = f"{class_index}"
#                             for i in range(0, len(segment), 2):
#                                 if i + 1 < len(segment):
#                                     x = segment[i] / img_width
#                                     y = segment[i + 1] / img_height
#                                     line += f" {x:.6f} {y:.6f}"
#                             f.write(f"{line}\n")
#                     logging.info("Wrote annotation: %s", annotation_path)
#                 except Exception as e:
#                     logging.error("Error processing annotation for frame %s in video %s: %s", frame_id, video.get("_id"), str(e))

#                 # Save the label name to the split file list
#                 splits[split_type].append(renamed_filename)

#     for split_name, file_basenames in splits.items():
#         split_file_path = f"{local_path}/ImageSets/{split_name}.txt"
#         with open(split_file_path, "w", encoding="utf-8") as f:
#             for basename in sorted(set(file_basenames)):
#                 f.write(f"{basename}\n")
#         logging.info("Wrote split file: %s with %d entries", split_file_path, len(file_basenames))

#     yaml_path = f"{local_path}/data.yaml"
#     with open(yaml_path, "w", encoding="utf-8") as f:
#         f.write(f"path: {local_path}\n")
#         f.write(f"train: images/train\n")
#         f.write(f"val: images/val\n")
#         f.write(f"test: images/test\n\n")
#         f.write("# Classes\n")
#         f.write("names:\n")
#         for category, idx in category_to_index.items():
#             f.write(f"  {idx}: {category}\n")
#     logging.info("Wrote data.yaml at: %s", yaml_path)


def get_categories_id_map(dataset_items: List[Dict], start_id: int = 0) -> Dict[str, int]:
    """Get mapping of categories to IDs.

    Args:
        dataset_items: List of dataset items
        start_id: Starting ID for categories

    Returns:
        Dictionary mapping category names to IDs
    """
    categories_id_map = {}
    category_num = start_id
    for image in dataset_items:
        for anno in get_image_annotations(image):
            category = anno.get("category")
            if not category:
                continue
            if category not in categories_id_map:
                categories_id_map[category] = category_num
                category_num += 1
    logging.info("Categories ID map: %s", categories_id_map)
    return categories_id_map


def get_mscoco_categories(
    categories_id_map: Dict[str, int],
) -> List[Dict]:
    """Extract MSCOCO categories from dataset items.

    Args:
        categories_id_map: Dictionary mapping categories to IDs

    Returns:
        List of category dictionaries in MSCOCO format
    """
    categories = []
    for (
        category_name,
        category_id,
    ) in categories_id_map.items():
        categories.append(
            {
                "id": category_id,
                "name": category_name,
                "supercategory": "",
            }
        )
    return categories


def get_mscoco_images(
    dataset_items: List[Dict],
) -> List[Dict]:
    """Extract MSCOCO images from dataset items.

    Args:
        dataset_items: List of dataset items

    Returns:
        List of image dictionaries in MSCOCO format
    """
    images = []
    image_id_counter = 1
    logging.info("Getting Image file")
    for image in dataset_items:
        if not all(
            key in image
            for key in [
                "width",
                "height",
                "filename",
            ]
        ):
            logging.warning(
                "Skipping image with missing required fields: %s",
                image,
            )
            continue
        image_info = {
            "id": image_id_counter,
            "width": image["width"],
            "height": image["height"],
            "file_name": image["filename"].split("/")[-1],
            "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        image_id_counter += 1
        images.append(image_info)
    logging.info("Returning Image file")
    return images


def get_mscoco_annotations(
    dataset_items: List[Dict],
    categories_id_map: Dict[str, int],
) -> List[Dict]:
    """Extract MSCOCO annotations from dataset items.

    Args:
        dataset_items: List of dataset items
        categories_id_map: Dictionary mapping categories to IDs

    Returns:
        List of annotation dictionaries in MSCOCO format
    """
    annotations = []
    annotation_id_counter = 1
    image_id_counter = 1
    logging.info("Getting Annotation file")
    for image in dataset_items:
        for bbox_info in get_image_annotations(image):
            try:
                category = bbox_info.get("category")
                if not category:
                    continue
                category_id = categories_id_map.get(category)
                if category_id is None:
                    continue
                bbox = bbox_info.get("bbox")
                if not bbox or len(bbox) != 4:
                    continue
                annotation_info = {
                    "id": annotation_id_counter,
                    "image_id": image_id_counter,
                    "category_id": category_id,
                    "segmentation": bbox_info.get("segmentation", []),
                    "area": bbox[2] * bbox[3],
                    "bbox": bbox,
                    "iscrowd": 0,
                }
                annotation_id_counter += 1
                annotations.append(annotation_info)
            except Exception as exc:
                logging.error(
                    "Error processing annotation: %s",
                    str(exc),
                )
        image_id_counter += 1
    logging.info("Returning Annotation file")
    return annotations


def write_mscoco_annotation_file(
    dataset_items: List[Dict],
    categories_id_map: Dict[str, int],
    ann_json_path: str,
) -> None:
    """Write MSCOCO annotation file in COCO format.

    Args:
        dataset_items: List of dataset items
        categories_id_map: Dictionary mapping categories to IDs
        ann_json_path: Path to save annotation file
    """
    logging.info("Writing Annotation file")
    coco_format_data = {
        "info": {},
        "licenses": [],
        "images": get_mscoco_images(dataset_items),
        "annotations": get_mscoco_annotations(dataset_items, categories_id_map),
        "categories": get_mscoco_categories(categories_id_map),
    }
    logging.info("Writing Annotation file complete")
    os.makedirs(
        os.path.dirname(ann_json_path),
        exist_ok=True,
    )
    with open(ann_json_path, "w", encoding="utf-8") as file:
        json.dump(coco_format_data, file, indent=2)


def write_mscoco_annotation_files(
    local_path: str,
    dataset_items: List[Dict],
    dataset_version: str,
) -> None:
    """Write MSCOCO annotation files for different itemSetTypes.

    Args:
        local_path: Base path to save annotation files
        dataset_items: List of dataset items
        dataset_version: Dataset version
    """
    labels_path = f"{local_path}/annotations"
    os.makedirs(labels_path, exist_ok=True)
    train_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "train"
    ]
    test_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "test"
    ]
    val_dataset_items = [
        x for x in dataset_items if get_item_set_type(x, dataset_version) == "val"
    ]
    categories_id_map = get_categories_id_map(dataset_items, start_id=1)
    if train_dataset_items:
        logging.info("Creating mscoco train.json")
        write_mscoco_annotation_file(
            train_dataset_items,
            categories_id_map,
            f"{local_path}/annotations/train.json",
        )
        logging.info("Created mscoco train.json")
    if test_dataset_items:
        logging.info("Creating mscoco test.json")
        write_mscoco_annotation_file(
            test_dataset_items,
            categories_id_map,
            f"{local_path}/annotations/test.json",
        )
        logging.info("Created mscoco test.json")
    if val_dataset_items:
        logging.info("Creating mscoco val.json")
        write_mscoco_annotation_file(
            val_dataset_items,
            categories_id_map,
            f"{local_path}/annotations/val.json",
        )
        logging.info("Created mscoco val.json")


def get_data_prep_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    input_format: str,
    base_dataset_path: str,
) -> Pipeline:
    """Get the data prep pipeline.

    Args:
        rpc: RPC client
        dataset_id: Dataset ID
        dataset_version: Dataset version
        input_format: Format of annotations
        base_dataset_path: Base path to save dataset

    Returns:
        Configured Pipeline object
    """
    dataset_items_queue = Queue()
    pipeline = Pipeline()
    pipeline.add_producer(
        process_fn=dataset_items_producer,
        process_params={
            "rpc": rpc,
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "pipeline_queue": dataset_items_queue,
        },
    )
    pipeline.add_stage(
        stage_name="Download Images",
        process_fn=download_images,
        pull_queue=dataset_items_queue,
        process_params={
            "input_format": input_format,
            "base_dataset_path": base_dataset_path,
            "dataset_version": dataset_version,
        },
        num_threads=15,
        is_last_stage=True,
    )
    pipeline.add_stop_callback(
        callback=process_final_annotations,
        process_params={
            "base_dataset_path": base_dataset_path,
            "input_format": input_format,
            "dataset_version": dataset_version,
        },
    )
    return pipeline

def get_video_data_prep_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    input_format: str,
    base_dataset_path: str,
) -> Pipeline:
    """Get the data prep pipeline.

    Args:
        rpc: RPC client
        dataset_id: Dataset ID
        dataset_version: Dataset version
        input_format: Format of annotations
        base_dataset_path: Base path to save dataset

    Returns:
        Configured Pipeline object
    """
    dataset_items_queue = Queue()
    pipeline = Pipeline()
    pipeline.add_producer(
        process_fn=video_dataset_items_producer,
        process_params={
            "rpc": rpc,
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "pipeline_queue": dataset_items_queue,
            "input_type": input_format,
        },
    )
    pipeline.add_stage(
        stage_name="Download Images",
        process_fn=download_segment_videos,
        pull_queue=dataset_items_queue,
        process_params={
            "input_format": input_format,
            "base_dataset_path": base_dataset_path,
            "dataset_version": dataset_version,
        },
        num_threads=15,
        is_last_stage=True,
    )
    pipeline.add_stop_callback(
        callback=process_final_annotations,
        process_params={
            "base_dataset_path": base_dataset_path,
            "input_format": input_format,
            "dataset_version": dataset_version,
        },
    )
    return pipeline


class DataPrep:
    """Class to handle dataset preparation."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataPrep.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
        """
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        url = f"/v1/project/action/{self.action_record_id}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_type = self.action_doc["action"]
        self.job_params = self.action_doc["jobParams"]
        self.dataset_id = self.job_params["dataset_id"]
        self.dataset_version = self.job_params["dataset_version"]
        self.input_format = self.job_params["input_formats"][0]
        self.local_path = (
            f"{str(self.dataset_id)}-{str(self.dataset_version)}-{str(self.input_format).lower()}"
        )
        self.update_status(
            "DCKR_ACK",
            "ACK",
            "Action is acknowledged by data processing service",
            str(
                os.path.join(
                    "/usr/src/workspace",
                    self.local_path,
                )
            ),
        )

    def update_status(
        self,
        step_code: str,
        status: str,
        status_description: str,
        dataset_path: str = None,
        sample_count: int = None,
    ) -> None:
        """Update status of data preparation.

        Args:
            step_code: Code indicating current step
            status: Status of step
            status_description: Description of status
            dataset_path: Optional path to dataset
            sample_count: Optional count of samples
        """
        try:
            logging.info(status_description)
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": step_code,
                "status": status,
                "statusDescription": status_description,
            }
            if dataset_path:
                self.job_params["dataset_path"] = dataset_path
            if sample_count:
                self.job_params["sample_count"] = sample_count
            if sample_count or dataset_path:
                payload["jobParams"] = self.job_params
            self.rpc.put(path=url, payload=payload)
        except Exception as exc:
            logging.error(
                "Exception in update_status: %s",
                str(exc),
            )

    def start_processing(self) -> None:
        """Start dataset preparation processing."""
        try:
            self.update_status(
                "DCKR_PROC",
                "OK",
                "Dataset preparation started",
                sample_count=get_number_of_dataset_batches(
                    self.rpc,
                    self.dataset_id,
                    self.dataset_version,
                ),
            )
            if self.input_format.lower() in ["kinetics", "mscoco_video", "davis"]:
                self.pipeline = get_video_data_prep_pipeline(
                    self.rpc,
                    self.dataset_id,
                    self.dataset_version,
                    self.input_format.lower(),
                    self.local_path,
                )
            
            else:
                self.pipeline = get_data_prep_pipeline(
                self.rpc,
                self.dataset_id,
                self.dataset_version,
                self.input_format,
                self.local_path,
            )
            self.pipeline.start()
            self.pipeline.wait_to_finish_processing_and_stop()
            self.update_status(
                "SUCCESS",
                "SUCCESS",
                "Dataset Preparation completed",
            )
        except Exception as exc:
            logging.error(
                "Error in start_processing: %s",
                str(exc),
            )
            self.update_status(
                "FAILED",
                "FAILED",
                f"Dataset preparation failed: {str(exc)}",
            )
            raise
