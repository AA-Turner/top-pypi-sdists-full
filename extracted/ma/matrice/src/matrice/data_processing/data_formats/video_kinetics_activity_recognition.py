"""Module providing video_kinetics_activity_recognition functionality."""

import logging
import os
import csv
import tempfile
from uuid import uuid4
import cv2
import requests
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def get_kinetics_annotations(annotation_paths):
    """Process Kinetics-style dataset and return video annotations grouped by video and split."""
    complete_videos = {}
    for csv_path in annotation_paths:
        if not os.path.exists(csv_path):
            logging.warning(
                "Annotation file not found: %s",
                csv_path,
            )
            continue
        with open(
            csv_path,
            "r",
            newline="",
            encoding="utf-8",
        ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                label = row["label"]
                youtube_id = row["youtube_id"]
                split = row.get("split", "unassigned").strip().lower()
                try:
                    time_start = float(row["time_start"])
                    time_end = float(row["time_end"])
                except ValueError:
                    logging.warning(
                        "Invalid duration values for %s",
                        youtube_id,
                    )
                    continue
                annotation = {
                    "id": str(generate_short_uuid()),
                    "segmentation": [],
                    "isCrowd": [],
                    "confidence": 0.0,
                    "bbox": [],
                    "height": 0.0,
                    "width": 0.0,
                    "center": [],
                    "area": 0.0,
                    "category": label,
                    "masks": [],
                    "duration": [
                        time_start,
                        time_end,
                    ],
                }
                if youtube_id not in complete_videos:
                    complete_videos[youtube_id] = {
                        "train": None,
                        "test": None,
                        "val": None,
                        "unassigned": None,
                    }
                if complete_videos[youtube_id][split] is None:
                    complete_videos[youtube_id][split] = {
                        "sequence_name": youtube_id,
                        "annotations": [],
                    }
                complete_videos[youtube_id][split]["annotations"].append(annotation)
    return complete_videos


def get_kinetics_dataset_item_details(image_path):
    """Get split and category from image path.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (split, category)
    """
    parts = os.path.normpath(image_path).split(os.sep)
    split = get_corresponding_split_type(image_path)
    category = parts[-2]
    return split, category


def get_video_metadata(presigned_url):
    """
    Downloads a video from a presigned URL, extracts its dimensions (width, height),
    FPS, and duration, and saves the first frame as an image locally.

    Args:
        presigned_url (str): The presigned URL of the video.

    Returns:
        dict: {
            "width": video_width,
            "height": video_height,
            "fps": rounded_fps,
            "first_frame_path": path_to_saved_image
        }
    """
    try:
        logging.info(f'attempting to extarct information from the presigned url {presigned_url}')
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
            success, frame = cap.read()
            if not success:
                raise Exception("Failed to read first frame")
            frame_filename = f"first_frame_{uuid4().hex}.jpg"
            logging.info(f"Saving first frame to {frame_filename}")
            cv2.imwrite(frame_filename, frame)
            cap.release()
        rounded_fps = int(fps + 0.5)
        logging.info(f'hieght extracted from presigned url is {height}, width is {width}, fps is {fps}, first frame path is { os.path.abspath(frame_filename)}')
        return {
            "width": width,
            "height": height,
            "fps": rounded_fps,
            "first_frame_path": os.path.abspath(frame_filename),
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return None


def add_kinetics_dataset_items_details(batch_dataset_items, frames_details):
    """Add details to kinetics dataset items.

    Args:
        batch_dataset_items: Batch of dataset items to process
        frames_details: Details of frames from annotations

    Returns:
        List of processed dataset items
    """
    processed_batch = []
    logging.debug(
        "Batch dataset items: %s",
        batch_dataset_items,
    )
    c=0
    for dataset_item in batch_dataset_items:
        if c==0:
            logging.info(f'kinetics dataset item for add kinetics dataset items queue is {dataset_item}')
            c+=1
        video_info = dataset_item.get("fileInfoResponse", {})[0].get("video")
        if not video_info:
            logging.warning(
                "No video info found in dataset item: %s",
                dataset_item,
            )
            continue
        file_location = video_info.get("fileLocation")
        file_name = video_info.get("filename")
        file_name = os.path.splitext(file_name)[0]
        presigned_url = video_info.get("fileLocation")
        if not file_location or not file_name or not presigned_url:
            logging.warning(
                "Missing file location, filename, or presigned URL in video info: %s",
                video_info,
            )
            continue
        video_metadata = get_video_metadata(presigned_url)
        logging.info(f'video metadata is {video_metadata}')
        video_height = video_metadata.get("height")
        video_width = video_metadata.get("width")
        fps = video_metadata.get("fps")
        first_frame_path = video_metadata.get("first_frame_path")
        if first_frame_path:
            new_first_frame_path = first_frame_path.lstrip("/")
        dataset_id = dataset_item.get("_idDataset")
        bucket_upload_first_frame_path = f"{dataset_id}/{new_first_frame_path}"
        logging.info(
            "First frame path: %s",
            first_frame_path,
        )
        logging.info(
            "Bucket upload first frame path: %s",
            bucket_upload_first_frame_path,
        )
        split_dataset_item, category = get_kinetics_dataset_item_details(file_location)
        all_video_data = frames_details.get(file_name)
        if not all_video_data:
            logging.warning(
                "No annotation data found for video file %s",
                file_name,
            )
            continue
        split_data = all_video_data.get(split_dataset_item)
        if not split_data:
            logging.warning(
                "No annotation data found for split %s in video %s",
                split_dataset_item,
                file_name,
            )
            continue
        split_video_annotation_data = split_data.get("annotations", [])
        dataset_item.update(
            {
                "splitType": split_dataset_item,
                "category": category,
                "annotations": split_video_annotation_data,
                "video_height": video_height,
                "video_width": video_width,
                "frame_rate": fps,
                "first_frame_path": first_frame_path,
                "bucket_upload_first_frame_path": bucket_upload_first_frame_path,
            }
        
        )
        logging.info(f'first_frame_path: {first_frame_path}')
        logging.info(f'bucket_upload_first_frame_path: {bucket_upload_first_frame_path}')
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
