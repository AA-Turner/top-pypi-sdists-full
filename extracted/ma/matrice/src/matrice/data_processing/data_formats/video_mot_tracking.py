"""Module providing video_mot_tracking functionality."""

import configparser
import logging
import os
from collections import defaultdict


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


def parse_seqinfo(seqinfo_path):
    """Parse seqinfo.ini file to extract video metadata.

    Args:
        seqinfo_path: Path to the seqinfo.ini file

    Returns:
        Dictionary containing video metadata or empty dict if parsing fails
    """
    config = configparser.ConfigParser()
    try:
        config.read(seqinfo_path)
        return {
            "sequence_name": config.get("Sequence", "name"),
            "frame_rate": config.getint("Sequence", "frameRate"),
            "total_frames": config.getint("Sequence", "seqLength"),
            "video_width": config.getint("Sequence", "imWidth"),
            "video_height": config.getint("Sequence", "imHeight"),
        }
    except FileNotFoundError:
        logging.error(
            "Seqinfo file not found: %s",
            seqinfo_path,
        )
        return {}
    except (
        configparser.NoSectionError,
        configparser.NoOptionError,
        ValueError,
    ) as err:
        logging.error(
            "Error parsing seqinfo file %s: %s",
            seqinfo_path,
            str(err),
        )
        return {}


def parse_gt(gt_path, img_dir):
    """Parse gt.txt file to extract annotations.

    Args:
        gt_path: Path to the ground truth file
        img_dir: Directory containing the images

    Returns:
        Dictionary mapping frame IDs to lists of annotations
    """
    annotations = defaultdict(list)
    try:
        with open(gt_path, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                parts = line.strip().split(",")
                if len(parts) != 9:
                    logging.warning(
                        "Skipping malformed line in %s: %s",
                        gt_path,
                        line.strip(),
                    )
                    continue
                (
                    frame_id,
                    track_id,
                    bb_left,
                    bb_top,
                    bb_width,
                    bb_height,
                    conf,
                    class_id,
                    visibility,
                ) = parts
                frame_id = int(frame_id)
                bbox = [
                    float(bb_left),
                    float(bb_top),
                    float(bb_width),
                    float(bb_height),
                ]
                file_ext = "jpg"
                file_name = f"{frame_id:06d}.{file_ext}"
                file_location = os.path.join(img_dir, file_name)
                annotation = {
                    "id": f"{track_id}_{frame_id}",
                    "order": frame_id,
                    **calculate_mot_bbox_properties(bbox),
                    "confidence": float(conf),
                    "category": class_id,
                    "visibility": float(visibility),
                    "segmentation": [],
                    "isCrowd": [],
                    "masks": [],
                    "file_name": file_name,
                    "file_location": file_location,
                    "track_id": track_id,
                }
                annotations[frame_id].append(annotation)
    except FileNotFoundError:
        logging.error(
            "Ground truth file not found: %s",
            gt_path,
        )
    except Exception as err:
        logging.error(
            "Error parsing ground truth file %s: %s",
            gt_path,
            str(err),
        )
    return annotations


def rename_mot_file(file_path):
    """Rename MOT dataset files to include split and video information.

    Args:
        file_path: Path to the file to rename

    Returns:
        New path after renaming

    Raises:
        ValueError: If video folder cannot be determined from path
    """
    logging.debug("Renaming file: %s", file_path)
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    if ext.lower() not in [".txt", ".ini"]:
        return file_path
    parts = file_path.split(os.sep)
    split_folders = {"train", "test", "val"}
    split_index = -1
    video_folder = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in split_folders:
            split_index = i
            break
    if split_index != -1 and split_index + 1 < len(parts):
        video_folder = parts[split_index + 1]
    else:
        raise ValueError("Could not determine video folder from path")
    split_type = parts[split_index]
    expected_suffix = f"_{split_type}_{video_folder}"
    if not name.endswith(expected_suffix):
        new_name = f"{name}{expected_suffix}{ext}"
    else:
        new_name = file_name
    new_path = os.path.join(dir_path, new_name)
    if new_path != file_path:
        os.rename(file_path, new_path)
    return new_path


def get_mot_annotations(dataset_paths):
    """Process MOT dataset and extract video annotations.

    Args:
        dataset_paths: List of paths to MOT dataset files

    Returns:
        Tuple containing:
        - Dictionary of complete video information by video name
        - Dictionary of class statistics
    """
    logging.debug("Starting to process MOT dataset...")
    dataset_paths = [rename_mot_file(path) for path in dataset_paths]
    complete_videos = {}
    seqinfo_map = {}
    class_stats = {}
    logging.debug("Extracting seqinfo.ini paths...")
    for path in dataset_paths:
        filename = os.path.basename(path)
        if "seqinfo_" in filename and filename.endswith(".ini"):
            parts = filename.split("_")
            split = parts[1]
            video_name = "_".join(parts[2:]).replace(".ini", "")
            seqinfo_map[split, video_name] = path
            logging.debug(
                "Found seqinfo for video '%s' in split '%s': %s",
                video_name,
                split,
                path,
            )
    logging.debug("Processing ground truth files...")
    for path in dataset_paths:
        filename = os.path.basename(path)
        if "gt_" in filename and filename.endswith(".txt"):
            parts = filename.split("_")
            split = parts[1]
            video_name = "_".join(parts[2:]).replace(".txt", "")
            logging.debug(
                "Processing ground truth for video '%s' in split '%s'",
                video_name,
                split,
            )
            seqinfo_path = seqinfo_map.get((split, video_name))
            if not seqinfo_path:
                logging.warning(
                    "Missing seqinfo.ini for %s (%s)",
                    video_name,
                    split,
                )
                continue
            img_dir = os.path.join(os.path.dirname(path), "img1")
            logging.debug(
                "Image directory set to: %s",
                img_dir,
            )
            metadata = parse_seqinfo(seqinfo_path)
            logging.debug(
                "Parsed metadata for %s: %s",
                video_name,
                metadata,
            )
            annotations = parse_gt(path, img_dir)
            logging.debug(
                "Parsed %d frames of annotations for %s",
                len(annotations),
                video_name,
            )
            video_data = {
                "sequence_name": video_name,
                "splitType": split,
                "total_frames": metadata["total_frames"],
                "frame_rate": metadata["frame_rate"],
                "duration_seconds": metadata["total_frames"] / metadata["frame_rate"],
                "video_height": metadata["video_height"],
                "video_width": metadata["video_width"],
                "annotation": {},
            }
            seen_objects = set()
            for frame_id in range(1, metadata["total_frames"] + 1):
                frame_annotations = annotations.get(frame_id, [])
                video_data["annotation"][str(frame_id)] = frame_annotations
                for ann in frame_annotations:
                    class_id = ann.get("category")
                    track_id = ann.get("track_id")
                    if class_id is None or track_id is None:
                        continue
                    unique_key = (
                        class_id,
                        track_id,
                    )
                    if unique_key not in seen_objects:
                        seen_objects.add(unique_key)
                        if class_id not in class_stats:
                            class_stats[class_id] = {
                                "train": 0,
                                "test": 0,
                                "val": 0,
                                "unassigned": 0,
                                "total": 0,
                            }
                        if split not in class_stats[class_id]:
                            split = "unassigned"
                        class_stats[class_id][split] += 1
                        class_stats[class_id]["total"] += 1
            complete_videos[video_name] = video_data
            logging.debug(
                "Completed processing for video '%s'",
                video_name,
            )
    logging.debug("Finished processing all videos.")
    logging.debug(
        "Classwise stats from mot annotations: %s",
        class_stats,
    )
    return complete_videos, class_stats


def extract_video_identifier(path):
    """Extract the video name from the file path.

    Args:
        path: File path to extract video identifier from

    Returns:
        Video identifier string or None if path is invalid
    """
    if not path:
        return None
    video_folder = os.path.dirname(os.path.dirname(path))
    video_name = os.path.basename(video_folder)
    return video_name


def add_mot_dataset_items_details(batch_dataset_items, frames_details):
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
    logging.debug(
        "Batch dataset items in add mot dataset items details: %s",
        batch_dataset_items,
    )

    for dataset_item in batch_dataset_items:
        file_info_list = dataset_item.get("fileInfoResponse", [])
        if not isinstance(file_info_list, list) or not file_info_list:
            continue

        has_valid_frame = False

        for fileinfo in file_info_list:
            frames = fileinfo.get("frames", {})
            if not isinstance(frames, dict):
                continue

            for fileinfo_frame_key, fileinfo_frame_value in frames.items():
                file_location = fileinfo_frame_value.get("fileLocation")
                dataset_video_identifier = extract_video_identifier(file_location)
                if not dataset_video_identifier:
                    logging.warning(
                        "Could not extract video identifier from file location: %s",
                        file_location,
                    )
                    continue

                video_data = frames_details.get(dataset_video_identifier)
                if not video_data:
                    logging.warning(
                        "Frame for file location '%s' not found in frames_details",
                        file_location,
                    )
                    continue

                dataset_item.update({k: v for k, v in video_data.items() if k != "annotation"})
                frame_annotations = video_data.get("annotation", {}).get(str(fileinfo_frame_key), [])
                if frame_annotations:
                    fileinfo_frame_value["annotations"] = frame_annotations
                    has_valid_frame = True

        if has_valid_frame:
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

    return processed_batch

