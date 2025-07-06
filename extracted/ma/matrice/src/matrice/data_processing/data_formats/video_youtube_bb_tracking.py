"""Module providing video_youtube_bb_tracking functionality."""

import logging
import os
import re
from io import BytesIO
import pandas as pd
import requests
from PIL import Image
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def calculate_mot_bbox_properties(bbox):
    """Calculate properties for MOT bounding box.

    Args:
        bbox: List containing [x, y, width, height]

    Returns:
        Dictionary containing bbox properties (bbox, height, width, center, area)
    """
    x_coord, y_coord, width, height = bbox
    return {
        "bbox": bbox,
        "height": height,
        "width": width,
        "center": [
            x_coord + width / 2,
            y_coord + height / 2,
        ],
        "area": width * height,
    }


def get_image_dimensions_from_url(presigned_url):
    """Get image dimensions from a URL.

    Args:
        presigned_url: URL of the image to analyze

    Returns:
        Tuple containing height and width or (None, None) on failure
    """
    try:
        response = requests.get(presigned_url, timeout=30)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        return height, width
    except Exception as err:
        logging.error(
            "Error getting image dimensions: %s",
            err,
        )
        return None, None


def get_youtube_bb_video_frame_details(
    dataset_path,
):
    """Process YouTube Bounding Box dataset and extract details for each video sequence.

    Args:
        dataset_path: List of paths to CSV annotation files

    Returns:
        Tuple containing:
        - Dictionary of video details indexed by youtube_id
        - List of frames missing annotations
        - Dictionary of class-wise statistics
    """
    complete_videos = {}
    missing_annotations = []
    classwise_stats = {}
    if not isinstance(dataset_path, list) or not all(
        os.path.exists(path) for path in dataset_path
    ):
        logging.error(
            "Invalid dataset paths provided: %s",
            dataset_path,
        )
        return (
            complete_videos,
            missing_annotations,
            classwise_stats,
        )
    for csv_file in dataset_path:
        if not csv_file.lower().endswith(".csv"):
            logging.warning(
                "Skipping non-CSV file: %s",
                csv_file,
            )
            continue
        try:
            annotations = pd.read_csv(csv_file)
        except Exception as err:
            logging.error(
                "Error reading CSV file %s: %s",
                csv_file,
                err,
            )
            continue
        split_match = re.search(
            "(train|test|val)",
            os.path.basename(csv_file).lower(),
        )
        split = split_match.group(0) if split_match else "unknown"
        grouped = annotations.groupby("youtube_id")
        for youtube_id, group in grouped:
            group = group.sort_values(by="timestamp_ms").reset_index(drop=True)
            frame_rate = 30
            metadata = {
                "sequence_name": youtube_id,
                "splitType": split,
                "total_frames": len(group),
                "frame_rate": frame_rate,
                "duration_seconds": len(group) / frame_rate,
                "annotation": {},
            }
            expected_frames = {
                i: {
                    "frame_id": i,
                    "file_name": f"{youtube_id}_{i}.jpg",
                    "file_path": os.path.join(
                        os.path.dirname(csv_file),
                        youtube_id,
                        f"{youtube_id}_{i}.jpg",
                    ),
                    "has_annotations": False,
                }
                for i in range(len(group))
            }
            for i, row in group.iterrows():
                class_name = row["class_name"]
                bbox = [
                    row["xmin"],
                    row["ymin"],
                    row["xmax"] - row["xmin"],
                    row["ymax"] - row["ymin"],
                ]
                annotation_json = {
                    "id": str(generate_short_uuid()),
                    "order": i,
                    "file_name": expected_frames[i]["file_name"],
                    "file_location": expected_frames[i]["file_path"],
                    "bbox": bbox,
                    "height": bbox[3],
                    "width": bbox[2],
                    "center": [
                        bbox[0] + bbox[2] / 2,
                        bbox[1] + bbox[3] / 2,
                    ],
                    "area": bbox[2] * bbox[3],
                    "confidence": row["object_presence"],
                    "category": class_name,
                    "visibility": row["object_presence"],
                    "segmentation": [],
                    "isCrowd": [],
                    "masks": [],
                }
                frame_key = str(i)
                if frame_key not in metadata["annotation"]:
                    metadata["annotation"][frame_key] = []
                metadata["annotation"][frame_key].append(annotation_json)
                expected_frames[i]["has_annotations"] = True
                if class_name not in classwise_stats:
                    classwise_stats[class_name] = {
                        "train": 0,
                        "test": 0,
                        "val": 0,
                    }
                classwise_stats[class_name][split] += 1
            for (
                frame_id,
                frame_info,
            ) in expected_frames.items():
                if not frame_info["has_annotations"]:
                    missing_annotations.append(frame_info["file_path"])
                frame_key = str(frame_id)
                if frame_key not in metadata["annotation"]:
                    metadata["annotation"][frame_key] = []
            complete_videos[youtube_id] = metadata
    for (
        category,
        counts,
    ) in classwise_stats.items():
        counts["total"] = sum(counts.values())
    logging.info(
        "Complete video sequences: %d",
        len(complete_videos),
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


def extract_video_identifier(file_name):
    """Extract video identifier from a filename.

    Args:
        file_name: Filename to extract the identifier from

    Returns:
        Video identifier string (part before the last underscore)
    """
    return file_name.rsplit("_", 1)[0]


def preprocess_frames_details(frames_details):
    """Preprocess frames details into a lookup structure.

    Args:
        frames_details: Dictionary of frame details by video identifier

    Returns:
        Lookup dictionary mapping (video_id, frame_id) tuples to frame data
    """
    lookup = {}
    for video_data in frames_details.values():
        for (
            frame_id,
            annotations,
        ) in video_data.get("annotation", {}).items():
            if annotations:
                video_identifier = extract_video_identifier(annotations[0].get("file_name", ""))
                if video_identifier:
                    lookup[video_identifier, frame_id] = (video_data, annotations)
    return lookup


def add_youtube_bb_dataset_items_details(batch_dataset_items, frames_details):
    """
    Enhance batch dataset items with corresponding frame annotations.

    Args:
        batch_dataset_items: List of dataset items to enhance
        frames_details: Dictionary of frame details by video identifier

    Returns:
        Processed batch with added details
    """
    logging.info("Adding YouTube BB dataset items details for %d items", len(batch_dataset_items))

    processed_batch = []

    lookup = preprocess_frames_details(frames_details)

    for dataset_item in batch_dataset_items:
        logging.debug("Processing YTBB dataset item: %s", dataset_item)
        video_high_level_data = {}

        file_info_response_list = dataset_item.get("fileInfoResponse", [])
        for file_info in file_info_response_list:
            frames = file_info.get("frames", {})
            for fileinfo_frame_key, fileinfo_frame_value in frames.items():
                get_corresponding_split_type(fileinfo_frame_value.get("fileLocation"))
                file_name = fileinfo_frame_value.get("filename")
                dataset_video_identifier = extract_video_identifier(file_name)
                key = (dataset_video_identifier, fileinfo_frame_key)

                if key in lookup:
                    video_high_level_data, annotations = lookup[key]
                    fileinfo_frame_value["annotations"] = annotations
                    logging.debug("File info updated")
                else:
                    logging.warning("'%s' not found in frames_details", file_name)

        # Assume the last frame from the last file_info entry is used for dimension extraction
        if file_info_response_list:
            last_file_info = file_info_response_list[-1]
            last_frames = last_file_info.get("frames", {})
            if last_frames:
                last_frame_key = sorted(last_frames.keys())[-1]
                last_frame = last_frames[last_frame_key]
                cloud_path = last_frame.get("cloudPath", last_frame.get("fileLocation", ""))
                video_height, video_width = get_image_dimensions_from_url(cloud_path)
            else:
                video_height, video_width = 0, 0
        else:
            video_height, video_width = 0, 0

        dataset_item.update({k: v for k, v in video_high_level_data.items() if k != "annotation"})
        dataset_item.update({
            "video_height": video_height,
            "video_width": video_width,
        })

        processed_batch.append({
            "sample_details": dataset_item,
            "is_complete": all(dataset_item.get(k) is not None for k in ["video_height", "video_width"]),
        })

    return processed_batch

