"""Module providing video_davis_segmentation functionality."""

import os
import logging
from collections import defaultdict
import cv2
import numpy as np
from matrice.data_processing.server_utils import (
    generate_short_uuid,
    get_corresponding_split_type
)


def read_dataset_splits(dataset_paths):
    """Reads train.txt, val.txt, and test.txt to map videos to dataset splits.

    Args:
        dataset_paths: List of paths to dataset files

    Returns:
        Dictionary mapping video names to their respective splits
    """
    dataset_splits = {}
    split_files = {
        "train.txt": None,
        "val.txt": None,
        "test.txt": None,
    }
    for path in dataset_paths:
        filename = os.path.basename(path)
        if filename in split_files:
            split_files[filename.replace(".txt", "")] = path
    for split, path in split_files.items():
        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    for line in file:
                        video_name = line.strip()
                        dataset_splits[video_name] = split
            except FileNotFoundError:
                logging.error(
                    "Dataset split file not found: %s",
                    path,
                )
    return dataset_splits


def extract_objects_from_mask(mask_path, video_name):
    """Extract object bounding boxes, polygon segmentations, and properties from a grayscale mask.

    Args:
        mask_path: Path to the segmentation mask image

    Returns:
        Tuple containing:
        - List of annotation objects
        - Video height
        - Video width

    Raises:
        ValueError: If the mask image cannot be loaded
    """
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError(f"Failed to load mask image from {mask_path}")
    video_height, video_width = mask.shape
    objects = np.unique(mask)
    objects = objects[objects > 0]
    annotations = []
    for obj_id in objects:
        obj_mask = (mask == obj_id).astype(np.uint8)
        contours, _ = cv2.findContours(
            obj_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        if contours:
            x_coord, y_coord, width, height = cv2.boundingRect(np.vstack(contours))
            center_x, center_y = (
                x_coord + width / 2,
                y_coord + height / 2,
            )
            area = np.sum(obj_mask)
            polygons = []
            for contour in contours:
                if len(contour) >= 6:
                    polygons.append(contour.flatten().tolist())
            annotation = {
                "id": str(generate_short_uuid()),
                "bbox": [
                    int(x_coord),
                    int(y_coord),
                    int(width),
                    int(height),
                ],
                "width": int(width),
                "height": int(height),
                "center": [
                    float(center_x),
                    float(center_y),
                ],
                "area": float(area),
                "category": video_name,
                "segmentation": polygons,
                "masks": polygons,
                "iscrowd": [0],
                "visibility": 1.0,
                "confidence": 1.0,
            }
            annotations.append(annotation)
    return annotations, video_height, video_width


def rename_davis_file(file_path):
    """Rename Davis dataset files to a standardized format.

    Args:
        file_path: Path to the file to rename

    Returns:
        New path after renaming
    """
    logging.debug("Renaming file: %s", file_path)
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    if ext.lower() != ".png":
        return file_path
    parent_folder = os.path.basename(os.path.dirname(file_path))
    new_name = f"{name}_{parent_folder}{ext}"
    new_path = os.path.join(dir_path, new_name)
    logging.debug("New path constructed: %s", new_path)
    if new_path != file_path:
        os.rename(file_path, new_path)
        logging.debug(
            "Renamed %s to %s",
            file_path,
            new_path,
        )
    return new_path


def get_davis_annotations(dataset_paths):
    """Process DAVIS dataset and extract video annotations.

    Args:
        dataset_paths: List of paths to dataset files

    Returns:
        Tuple containing:
        - Dictionary of complete video information indexed by video name
        - Dictionary of video counts by split
    """
    dataset_paths = [rename_davis_file(path) for path in dataset_paths]
    dataset_splits = read_dataset_splits(dataset_paths)
    logging.debug("Final dataset paths: %s", dataset_paths)
    logging.debug("Dataset splits: %s", dataset_splits)
    complete_videos = {}
    video_counts = defaultdict(
        lambda: {
            "train": 0,
            "test": 0,
            "val": 0,
            "unassigned": 0,
            "total": 0,
        }
    )
    for path in dataset_paths:
        if path.endswith(".png"):
            filename = os.path.basename(path)
            logging.debug(
                "Processing file for get_davis_annotations: %s",
                filename,
            )
            frame_number, video_name = filename.split("_", 1)
            frame_number = int(frame_number)
            video_name = video_name.replace(".png", "")
            split = dataset_splits.get(video_name)
            if not split:
                logging.warning(
                    "Skipping %s with frame %s, not found in dataset splits.",
                    video_name,
                    frame_number,
                )
                split = "unassigned"
            video_counts[video_name][split] += 1
            video_counts[video_name]["total"] += 1
            (
                annotations,
                video_height,
                video_width,
            ) = extract_objects_from_mask(path, video_name)
            if video_name not in complete_videos:
                has_multiple_splits = (
                    video_counts[video_name]["train"] > 0 and video_counts[video_name]["test"] > 0
                )
                complete_videos[video_name] = {
                    "sequence_name": video_name,
                    "splitType": None,
                    "frame_rate": 30,
                    "video_height": video_height,
                    "video_width": video_width,
                    "annotation": {},
                }
            complete_videos[video_name]["annotation"][str(frame_number)] = annotations
    return complete_videos, dict(video_counts)


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


def add_davis_dataset_items_details(batch_dataset_items, frames_details):
    """Enhance batch dataset items with corresponding frame annotations.

    Args:
        batch_dataset_items: List of dataset items to enhance
        frames_details: Dictionary of frame details by video identifier

    Returns:
        Processed batch with added details
    """
    if not batch_dataset_items or not frames_details:
        return []

    processed_batch = []
    logging.debug("batch_dataset_items in add davis dataset items details: %s", batch_dataset_items)

    for dataset_item in batch_dataset_items:
        file_info_list = dataset_item.get("fileInfoResponse", [])
        if not isinstance(file_info_list, list) or not file_info_list:
            continue

        has_valid_frame = False

        for fileinfo in file_info_list:
            frames_dict = fileinfo.get("frames", {})
            if not isinstance(frames_dict, dict):
                continue

            for frame_key, frame_value in frames_dict.items():
                file_location = frame_value.get("fileLocation")
                split=get_corresponding_split_type(file_location)
                logging.debug("file_location %s", file_location)
                logging.debug("split from add function is %s", split)
                dataset_video_identifier = extract_video_identifier(file_location)

                if not dataset_video_identifier:
                    logging.warning(
                        "Could not extract video identifier from file location: %s",
                        file_location,
                    )
                    continue

                video_data = frames_details.get(dataset_video_identifier)
                video_data["splitType"] = split
                if not video_data:
                    logging.warning(
                        "Frame for file location '%s' not found in frames_details",
                        file_location,
                    )
                    continue

                dataset_item.update({k: v for k, v in video_data.items() if k != "annotation"})
                frame_annotations = video_data.get("annotation", {}).get(str(frame_key), [])
                if frame_annotations:
                    frame_value["annotations"] = frame_annotations
                    has_valid_frame = True

        if has_valid_frame:
            processed_batch.append(
                {
                    "sample_details": dataset_item,
                    "is_complete": all(
                        dataset_item.get(k) is not None
                        for k in ["video_height", "video_width", "splitType"]
                    ),
                }
            )

    return processed_batch
