"""Module providing video_imagenet_classification functionality."""

import os
import logging
import tempfile
import cv2
import requests
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
)
from matrice.data_processing.server_utils import (
    generate_short_uuid,
)


import os
import cv2
import requests
import tempfile
import logging
from uuid import uuid4

def get_video_metadata(presigned_url):
    """
    Downloads a video from a presigned URL, extracts its dimensions (width, height),
    FPS, duration, and saves the first frame as an image locally.

    Args:
        presigned_url (str): The presigned URL of the video.

    Returns:
        dict: {
            "width": video_width,
            "height": video_height,
            "fps": rounded_fps,
            "duration": [0, duration],  # Video duration in seconds
            "first_frame_path": path_to_saved_image
        }
    """
    try:
        response = requests.get(presigned_url, stream=True, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Failed to download video: {response.status_code}")
        
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video:
            for chunk in response.iter_content(chunk_size=8192):
                temp_video.write(chunk)
            temp_video.flush()

            cap = cv2.VideoCapture(temp_video.name)
            if not cap.isOpened():
                raise Exception("Failed to open video file")

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0

            success, frame = cap.read()
            if not success:
                raise Exception("Failed to read first frame")

            frame_filename = f"first_frame_{uuid4().hex}.jpg"
            logging.info(f"Saving first frame to {frame_filename}")
            cv2.imwrite(frame_filename, frame)

            cap.release()

        rounded_fps = int(fps + 0.5)
        return {
            "width": width,
            "height": height,
            "fps": rounded_fps,
            "duration": [0, round(duration, 2)],
            "first_frame_path": os.path.abspath(frame_filename),
        }

    except Exception as e:
        print(f"Error: {e}")
        return None



def add_video_imagenet_dataset_items_details(
    batch_dataset_items,
):
    """Add details to video imagenet dataset items.

    Args:
        batch_dataset_items: Batch of dataset items to process

    Returns:
        List of processed dataset items
    """
    processed_batch = []
    logging.debug(
        "Batch dataset items: %s",
        batch_dataset_items,
    )
    for dataset_item in batch_dataset_items:
        video_info = dataset_item.get("fileInfoResponse", {})[0].get("video")
        if not video_info:
            continue
        file_location = video_info.get("fileLocation")
        presigned_url = video_info.get("fileLocation")
        if not file_location or not presigned_url:
            continue
        split, category, annotations = get_imagenet_dataset_item_details(file_location)
        metadata = get_video_metadata(presigned_url)
        first_frame_path = metadata.get("first_frame_path")
        if first_frame_path:
            new_first_frame_path = first_frame_path.lstrip("/")
        dataset_id = dataset_item.get("_idDataset")
        bucket_upload_first_frame_path = f"{dataset_id}/{new_first_frame_path}"
        dataset_item.update(
            {
                "splitType": split,
                "category": category,
                "annotations": annotations,
                "video_height": metadata.get("height"),
                "video_width": metadata.get("width"),
                "frame_rate": metadata.get("fps"),
                "segment_duration": metadata.get("duration"),
                "first_frame_path": first_frame_path,
                "bucket_upload_first_frame_path": bucket_upload_first_frame_path,
            }
        )
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None
                    for k in [
                        "video_height",
                        "video_width",
                    ]
                ),
            }
        )
    logging.debug("Processed batch: %s", processed_batch)
    return processed_batch


def get_imagenet_dataset_item_details(image_path):
    """Extract details from image path for ImageNet dataset.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (split, category, annotations)
    """
    parts = os.path.normpath(image_path).split(os.sep)
    split = get_corresponding_split_type(image_path)
    category = parts[-2]
    annotations = [
        {
            "id": str(generate_short_uuid()),
            "segmentation": [],
            "isCrowd": [],
            "confidence": 0.0,
            "bbox": [],
            "height": 0.0,
            "width": 0.0,
            "center": [],
            "area": 0.0,
            "category": str(category),
            "masks": [],
        }
    ]
    if split == "unassigned":
        logging.warning(
            "No split type for image: %s, category: %s",
            image_path,
            category,
        )
    return split, category, annotations
