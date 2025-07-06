"""Module providing video_detection_mscoco functionality."""

import os
import json
import logging
import tempfile
from collections import defaultdict
import cv2
import requests
from uuid import uuid4
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def get_video_mscoco_annotations(
    annotation_paths,
):
    """Process MSCOCO-style video dataset annotations and return frame-based annotations grouped
    by split and video, using nested dictionary structure similar to YouTube BB function."""
    complete_videos = {
        "train": {},
        "val": {},
        "test": {},
        "unassigned": {},
    }
    missing_annotations = []
    classwise_stats = {}
    
    for ann_path in annotation_paths:
        if not os.path.exists(ann_path):
            logging.warning(
                "Annotation file not found: %s",
                ann_path,
            )
            continue
            
        filename = os.path.basename(ann_path).lower()
        if "train" in filename:
            split = "train"
        elif "val" in filename:
            split = "val"
        elif "test" in filename:
            split = "test"
        elif "metadata" in filename:
            continue
        else:
            split = "unassigned"
            
        with open(ann_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        categories = {cat["id"]: cat["name"] for cat in data.get("categories", [])}
        video_meta = {video["id"]: video for video in data.get("videos", [])}
        
        annotations_by_video = defaultdict(list)
        for ann in data.get("annotations", []):
            annotations_by_video[ann["video_id"]].append(ann)
            
        for video_id, annotations in annotations_by_video.items():
            if video_id not in video_meta:
                logging.warning(
                    "Video ID %s not found in metadata.",
                    video_id,
                )
                continue
                
            video_info = video_meta[video_id]
            video_name = os.path.splitext(video_info["file_name"])[0]
            fps = video_info["fps"]
            video_width = video_info["width"]
            video_height = video_info["height"]
            total_frames = video_info["frames"]
            
            # Create video metadata similar to YouTube BB structure but organized by split
            if video_name not in complete_videos[split]:
                complete_videos[split][video_name] = {
                    "sequence_name": video_name,
                    "splitType": split,
                    "total_frames": total_frames,
                    "frame_rate": fps,
                    "duration_seconds": total_frames / fps,
                    "video_height": video_height,
                    "video_width": video_width,
                    "annotation": {},
                }
            
            # Sort annotations by frame
            annotations = sorted(
                annotations,
                key=lambda x: x["frame_id"],
            )
            
            # Track which frames have annotations
            frames_with_annotations = set()
            
            # Process annotations by frame
            for idx, ann in enumerate(annotations):
                frame_id = ann["frame_id"]
                category_id = ann["category_id"]
                category_name = categories.get(category_id, "unknown")
                
                # Update classwise stats
                if category_name not in classwise_stats:
                    classwise_stats[category_name] = {
                        "train": 0,
                        "val": 0,
                        "test": 0,
                        "unassigned": 0,
                    }
                classwise_stats[category_name][split] += 1
                
                # Calculate time info
                time_start = frame_id / fps
                if idx + 1 < len(annotations):
                    next_frame_id = annotations[idx + 1]["frame_id"]
                else:
                    next_frame_id = video_info["frames"]
                time_end = next_frame_id / fps
                
                # Create annotation similar to MSCOCO but organized by frame
                annotation = {
                    "id": str(generate_short_uuid()),
                    "segmentation": ann.get("segmentation", []),
                    "order_id": frame_id,
                    "file_name": f"{video_name}_{frame_id}.jpg",  # Similar to YouTube BB
                    "file_location": f"{os.path.dirname(ann_path)}/{video_name}/{video_name}_{frame_id}.jpg",  # Similar to YouTube BB
                    "isCrowd": [
                        (float(item) if isinstance(item, (int, float)) else 0)
                        for item in (
                            ann.get("iscrowd", [0])
                            if isinstance(
                                ann.get("iscrowd"),
                                list,
                            )
                            else [ann.get("iscrowd", 0)]
                        )
                    ],
                    "confidence": 0.0,
                    "bbox": ann.get("bbox", []),
                    "height": ann["bbox"][3] if "bbox" in ann and len(ann["bbox"]) > 3 else 0,
                    "width": ann["bbox"][2] if "bbox" in ann and len(ann["bbox"]) > 2 else 0,
                    "center": (
                        [
                            ann["bbox"][0] + ann["bbox"][2] / 2,
                            ann["bbox"][1] + ann["bbox"][3] / 2,
                        ]
                        if ann.get("bbox") and len(ann["bbox"]) > 3
                        else []
                    ),
                    "area": ann.get("area", 0.0),
                    "category": category_name,
                    "masks": [],
                    "visibility": 1.0,  # Similar to YouTube BB's object_presence
                    "duration": [
                        round(time_start, 4),
                        round(time_end, 4),
                    ],  # Keep MSCOCO's time information
                }
                
                # Store the annotation by frame_id as a string key (like YouTube BB)
                frame_key = str(frame_id)
                if frame_key not in complete_videos[split][video_name]["annotation"]:
                    complete_videos[split][video_name]["annotation"][frame_key] = []
                    
                complete_videos[split][video_name]["annotation"][frame_key].append(annotation)
                frames_with_annotations.add(frame_id)
            
            # Track missing annotations
            for frame_id in range(total_frames):
                if frame_id not in frames_with_annotations:
                    missing_file_path = f"{os.path.dirname(ann_path)}/{video_name}/{video_name}_{frame_id}.jpg"
                    missing_annotations.append(missing_file_path)
                    
                    # Add empty annotation list for frames without annotations (like YouTube BB)
                    frame_key = str(frame_id)
                    if frame_key not in complete_videos[split][video_name]["annotation"]:
                        complete_videos[split][video_name]["annotation"][frame_key] = []
    
    # Compute total stats across splits
    for category_name, split_counts in classwise_stats.items():
        split_counts["total"] = sum(v for k, v in split_counts.items() if k != "total")
    
    # Count total videos
    total_videos = sum(len(videos) for split, videos in complete_videos.items())
    
    logging.info(
        "Complete video sequences: %d",
        total_videos,
    )
    logging.info(
        "Frames missing annotations: %d",
        len(missing_annotations),
    )
    logging.info(
        "Class-wise statistics: %s",
        classwise_stats,
    )
    
    return (
        complete_videos,
        missing_annotations,
        classwise_stats,
    )


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
            cv2.imwrite(frame_filename, frame)
            cap.release()
        rounded_fps = int(fps + 0.5)
        return {
            "width": width,
            "height": height,
            "fps": rounded_fps,
            "first_frame_path": os.path.abspath(frame_filename),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_video_identifier(path):
    """Extract the video name from the file path.

    Args:
        path: File path to extract video identifier from

    Returns:
        Video identifier string or None if path is invalid
    """
    if not path:
        return None
    video_folder = os.path.dirname(path)
    video_name = os.path.basename(video_folder)
    return video_name

def add_video_mscoco_dataset_items_details(batch_dataset_items, frames_details):
    """Add MSCOCO video-style annotation details to frame-wise dataset items.

    Args:
        batch_dataset_items: List of dataset items to enhance
        frames_details: Complete videos dictionary from get_video_mscoco_annotations()

    Returns:
        List of processed dataset items with annotation and video metadata
    """
    if not batch_dataset_items or not frames_details:
        return []

    processed_batch = []

    logging.debug(
        "Processing %d dataset items with MSCOCO video annotations",
        len(batch_dataset_items),
    )

    for dataset_item in batch_dataset_items:
        file_info_list = dataset_item.get("fileInfoResponse", [])
        if not isinstance(file_info_list, list) or not file_info_list:
            logging.warning("Missing or invalid fileInfoResponse for dataset item")
            continue

        last_annotations_found = []
        for fileinfo in file_info_list:
            frames_dict = fileinfo.get("frames", {})
            if not isinstance(frames_dict, dict):
                logging.warning("Invalid frames data structure in fileInfoResponse")
                continue

            for frame_key, frame_value in frames_dict.items():
                file_location = frame_value.get("fileLocation")
                if not file_location:
                    logging.warning("Missing fileLocation for frame %s", frame_key)
                    continue

                split = get_corresponding_split_type(file_location)
                video_identifier = extract_video_identifier(file_location)

                if not video_identifier:
                    logging.warning(
                        "Could not extract video identifier from file location: %s",
                        file_location,
                    )
                    continue

                split_data = frames_details.get(split)
                if not split_data:
                    logging.warning("Split '%s' not found in frames_details", split)
                    continue

                video_data = split_data.get(video_identifier)
                if not video_data:
                    logging.warning(
                        "Video identifier '%s' not found in split '%s'",
                        video_identifier,
                        split,
                    )
                    
                    dataset_item.setdefault("splitType", split)
                    dataset_item.setdefault("video_height", 1)
                    dataset_item.setdefault("video_width", 1)
                    frame_value["annotations"] = []

                # Attach video-level metadata
                else:
                    dataset_item.update(
                        {k: v for k, v in video_data.items() if k != "annotation"}
                    )
                    frame_value["annotations"] = video_data.get("annotation", {}).get(frame_key, [])

        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None
                    for k in ["video_height", "video_width", "splitType"]
                ),
            }
        )
    logging.debug(
        "Successfully processed %d/%d dataset items with MSCOCO annotations",
        len(processed_batch),
        len(batch_dataset_items),
    )
    return processed_batch
