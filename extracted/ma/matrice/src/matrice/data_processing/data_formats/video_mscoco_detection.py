"""Module providing video_mscoco_detection functionality."""

import json
import logging
import os
import traceback
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def calculate_bbox_properties(bbox):
    """Calculate properties for a bounding box.

    Args:
        bbox: Bounding box in format [x_min, y_min, width, height]

    Returns:
        Dictionary containing height, width, center coordinates, and area

    Raises:
        ValueError: If bbox doesn't have exactly 4 elements
    """
    if len(bbox) != 4:
        raise ValueError("Bounding box must be in the format [x_min, y_min, width, height].")
    x_min, y_min, width, height = bbox
    center_x = x_min + width / 2
    center_y = y_min + height / 2
    area = width * height
    return {
        "height": float(height),
        "width": float(width),
        "center": [
            float(center_x),
            float(center_y),
        ],
        "area": float(area),
    }


def get_msococo_videos_details(annotation_files):
    """Process MSCOCO video annotation files and extract video details.

    Args:
        annotation_files: List of paths to MSCOCO video annotation JSON files

    Returns:
        Tuple containing:
        - Dictionary of video details indexed by file location
        - List of video IDs missing annotations
        - Dictionary of class-wise split counts
    """
    complete_videos = {}
    missing_annotations = []
    missing_metadata = {}
    classwise_splits = {}
    logging.info(
        "Processing %d video annotation files",
        len(annotation_files),
    )
    if not annotation_files:
        logging.error("No annotation files provided")
        return (
            complete_videos,
            missing_annotations,
            classwise_splits,
        )
    for file_index, file_path in enumerate(annotation_files, 1):
        logging.debug(
            "\nProcessing file %d/%d: %s",
            file_index,
            len(annotation_files),
            file_path,
        )
        if not os.path.exists(file_path):
            logging.error("File not found: %s", file_path)
            continue
        try:
            with open(file_path, encoding="utf-8") as file_obj:
                try:
                    data = json.load(file_obj)
                except json.JSONDecodeError as err:
                    logging.error(
                        "Invalid JSON in %s: %s",
                        file_path,
                        err,
                    )
                    continue
                videos = data.get("videos", [])
                categories = data.get("categories", [])
                annotations = data.get("annotations", [])
            if not videos or not annotations:
                logging.error(
                    "Missing videos or annotations in %s",
                    file_path,
                )
                continue
            video_info = {
                vid["id"]: vid for vid in videos if isinstance(vid, dict) and "id" in vid
            }
            category_map = {
                cat["id"]: cat["name"]
                for cat in categories
                if isinstance(cat, dict) and "id" in cat
            }
            for category_name in category_map.values():
                if category_name not in classwise_splits:
                    classwise_splits[str(category_name)] = {
                        "train": 0,
                        "test": 0,
                        "val": 0,
                        "unassigned": 0,
                    }
            video_annotations = {}
            for annotation in annotations:
                if not isinstance(annotation, dict):
                    continue
                video_id = annotation.get("video_id")
                frame_id = annotation.get("frame_id")
                if video_id is None or frame_id is None:
                    continue
                if video_id not in video_annotations:
                    video_annotations[video_id] = {}
                if frame_id not in video_annotations[video_id]:
                    video_annotations[video_id][frame_id] = []
                video_annotations[video_id][frame_id].append(annotation)
            processed = 0
            skipped = 0
            for (
                video_id,
                frame_annotations,
            ) in video_annotations.items():
                video = video_info.get(video_id)
                if not video:
                    skipped += 1
                    continue
                try:
                    split_type = get_corresponding_split_type(
                        file_path,
                        include_year=False,
                    )
                    file_name = video.get("file_name", "unknown")
                    
                    # Create a base path for file locations (in practice, would use actual base path)
                    base_path = os.path.join(
                        os.path.dirname(file_path),
                        split_type,
                    )
                    file_location = os.path.join(base_path, file_name)
                    
                    details = {
                        "splitType": split_type,
                        "file_name": file_name,
                        "file_location": file_location,
                        "fps": float(video.get("fps", 0.0)),
                        "total_frames": int(video.get("frames", 0)),
                        "duration_seconds": float(video.get("duration", 0.0)),
                        "annotation": {},  # Changed to a dictionary keyed by frame_id
                    }
                    
                    # Add video resolution if available
                    if "height" in video and "width" in video:
                        details.update({
                            "video_height": int(video["height"]),
                            "video_width": int(video["width"]),
                        })
                    
                    # Process annotations by frame
                    for frame_id, frame_anns in frame_annotations.items():
                        frame_key = str(frame_id)
                        if frame_key not in details["annotation"]:
                            details["annotation"][frame_key] = []
                        
                        for annotation in frame_anns:
                            bbox = [float(coord) for coord in annotation.get("bbox", [])]
                            if not bbox or len(bbox) != 4:
                                continue
                            
                            bbox_properties = calculate_bbox_properties(bbox)
                            
                            # Generate frame-specific filename
                            frame_file_name = f"{os.path.splitext(file_name)[0]}_{frame_id}.jpg"
                            frame_file_path = os.path.join(base_path, frame_file_name)
                            
                            annotation_json = {
                                "id": str(generate_short_uuid()),
                                "frame_id": int(frame_id),
                                "file_name": frame_file_name,
                                "file_location": frame_file_path,
                                "segmentation": [
                                    [float(coord) for coord in segment]
                                    for segment in annotation.get(
                                        "segmentation",
                                        [],
                                    )
                                    if isinstance(
                                        segment,
                                        list,
                                    )
                                ],
                                "isCrowd": [
                                    (
                                        float(item)
                                        if isinstance(
                                            item,
                                            (
                                                int,
                                                float,
                                            ),
                                        )
                                        else 0
                                    )
                                    for item in (
                                        annotation.get(
                                            "iscrowd",
                                            [0],
                                        )
                                        if isinstance(
                                            annotation.get("iscrowd"),
                                            list,
                                        )
                                        else [
                                            annotation.get(
                                                "iscrowd",
                                                0,
                                            )
                                        ]
                                    )
                                ],
                                "confidence": float(
                                    annotation.get(
                                        "confidence",
                                        0.0,
                                    )
                                ),
                                "bbox": bbox,
                                "height": bbox_properties["height"],
                                "width": bbox_properties["width"],
                                "center": bbox_properties["center"],
                                "area": float(
                                    annotation.get(
                                        "area",
                                        bbox_properties["area"],
                                    )
                                ),
                                "category": str(
                                    category_map.get(
                                        annotation.get("category_id"),
                                        "Unknown",
                                    )
                                ),
                                "masks": annotation.get(
                                    "segmentation",
                                    [],
                                ),
                            }
                            details["annotation"][frame_key].append(annotation_json)
                            classwise_splits[annotation_json["category"]][details["splitType"]] += 1
                    
                    key = f"{details['splitType']}/{details['file_name']}"
                    if key in complete_videos:
                        # Merge annotations if the video already exists
                        for frame_key, frame_anns in details["annotation"].items():
                            if frame_key not in complete_videos[key]["annotation"]:
                                complete_videos[key]["annotation"][frame_key] = []
                            complete_videos[key]["annotation"][frame_key].extend(frame_anns)
                    else:
                        complete_videos[key] = details
                    
                    processed += 1
                except Exception as err:
                    logging.error(
                        "Error processing video annotation: %s",
                        err,
                    )
                    skipped += 1
                    continue
            if not annotations:
                missing_annotations.extend(
                    vid["id"] for vid in videos if isinstance(vid, dict) and "id" in vid
                )
        except Exception as err:
            logging.error(
                "Error processing file %s: %s",
                file_path,
                err,
            )
            traceback.print_exc()
    logging.info("\nFinal summary:")
    logging.info(
        "Complete videos: %d",
        len(complete_videos),
    )
    logging.info(
        "Missing annotations: %d",
        len(missing_annotations),
    )
    logging.info(
        "Missing metadata: %d",
        len(missing_metadata),
    )
    for (
        category,
        counts,
    ) in classwise_splits.items():
        counts["total"] = sum(counts.values())
    return (
        {**complete_videos, **missing_metadata},
        missing_annotations,
        classwise_splits,
    )

# def add_mscoco_video_dataset_items_details(batch_dataset_items, videos_details):
#     """Add video details to batch dataset items.

#     Args:
#         batch_dataset_items: List of dataset items containing video information
#         videos_details: Dictionary of video details indexed by split type and filename

#     Returns:
#         List of processed dataset items with video details and completion status
#     """
#     processed_batch = []
#     for dataset_item in batch_dataset_items:
#         video_key = f"{get_corresponding_split_type(dataset_item.get('fileLocation'))}/{dataset_item.get('filename')}"
#         if video_key not in videos_details:
#             logging.warning(
#                 "'%s' not found in videos_details",
#                 video_key,
#             )
#             continue
#         dataset_item.update(videos_details[video_key])
#         processed_batch.append(
#             {
#                 "sample_details": dataset_item,
#                 "is_complete": all(
#                     dataset_item.get(k) is not None
#                     for k in [
#                         "video_height",
#                         "video_width",
#                         "fps",
#                         "total_frames",
#                         "duration_seconds",
#                     ]
#                 ),
#             }
#         )
#     return processed_batch

def add_mscoco_dataset_items_details(batch_dataset_items, frames_details):
    """Enhance batch dataset items with corresponding frame annotations.

    Args:
        batch_dataset_items: List of dataset items to enhance
        frames_details: Dictionary of frame details by video identifier

    Returns:
        Processed batch with added details
    """
    logging.info("Adding MSCOCO dataset items details for %d items", len(batch_dataset_items))

    processed_batch = []
    
    # Process frames_details for easier lookup, similar to YouTube BB function
    lookup = {}
    for video_key, video_data in frames_details.items():
        video_high_level_data = {
            k: v for k, v in video_data.items() 
            if k != "annotation"
        }
        
        if "annotation" in video_data:
            for frame_id, annotations in video_data["annotation"].items():
                lookup[(video_data.get("file_name"), frame_id)] = (
                    video_high_level_data,
                    annotations
                )

    for dataset_item in batch_dataset_items:
        video_high_level_data = {}
        
        for (
            fileinfo_frame_key,
            fileinfo_frame_value,
        ) in dataset_item["fileInfoResponse"]["frames"].items():
            file_name = fileinfo_frame_value.get("filename")
            key = (file_name, fileinfo_frame_key)
            
            if key in lookup:
                (
                    video_high_level_data,
                    annotations,
                ) = lookup[key]
                fileinfo_frame_value.update(annotations[0])
                logging.debug("File info updated")
            else:
                logging.warning(
                    "'%s' with frame %s not found in frames_details",
                    file_name,
                    fileinfo_frame_key,
                )
        
        dataset_item.update(
            {k: v for k, v in video_high_level_data.items()}
        )
        dataset_item.update(
            {
                "splitType": split_dataset_item,
                "annotations": split_video_annotation_data,
                "video_height": video_height,
                "video_width": video_width,
                "frame_rate": rounded_fps,
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
                        "fps",
                        "total_frames",
                        "duration_seconds",
                    ]
                ),
            }
        )

    return processed_batch
