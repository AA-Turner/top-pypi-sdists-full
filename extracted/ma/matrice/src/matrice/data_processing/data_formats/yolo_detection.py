"""Module providing yolo_detection functionality."""

import logging
import os
import re
import traceback
import yaml
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def yolo_to_coco_bbox(yolo_bbox, img_width, img_height):
    """Convert YOLO bbox format to MS COCO format.

    Args:
        yolo_bbox: List containing [x_center, y_center, width, height] (normalized)
        img_width: Image width in pixels
        img_height: Image height in pixels

    Returns:
        Tuple containing:
        - coco_bbox: List [x_min, y_min, width, height]
        - coco_bbox_height: Height in absolute pixels
        - coco_bbox_width: Width in absolute pixels
        - coco_bbox_center: List [x_center, y_center] in absolute pixels
        - coco_bbox_area: Area in square pixels
    """
    x_center, y_center, width, height = yolo_bbox
    x_min = (x_center - width / 2) * img_width
    y_min = (y_center - height / 2) * img_height
    width = width * img_width
    height = height * img_height
    coco_x_center = x_min + width / 2
    coco_y_center = y_min + height / 2
    area = width * height
    return (
        [x_min, y_min, width, height],
        height,
        width,
        [coco_x_center, coco_y_center],
        area,
    )


def convert_payload_to_coco_format(payload):
    """Convert YOLO bbox format in payload to MS COCO format.

    Args:
        payload: The original payload containing YOLO bbox details

    Returns:
        Updated payload with COCO bbox format
    """
    for item in payload["items"]:
        img_width = item["width"]
        img_height = item["height"]
        updated_annotations = []
        for annotation in item["annotations"]:
            yolo_bbox = annotation["bbox"]
            (
                coco_bbox,
                coco_height,
                coco_width,
                coco_center,
                coco_area,
            ) = yolo_to_coco_bbox(yolo_bbox, img_width, img_height)
            updated_annotation = {
                "id": annotation["id"],
                "segmentation": annotation["segmentation"],
                "isCrowd": annotation["isCrowd"],
                "confidence": annotation["confidence"],
                "bbox": coco_bbox,
                "height": float(coco_height),
                "width": float(coco_width),
                "center": coco_center,
                "area": float(coco_area),
                "category": annotation["category"],
                "masks": annotation["masks"],
            }
            updated_annotations.append(updated_annotation)
        item["annotations"] = updated_annotations
    return payload


def get_yolo_image_details(annotation_files):
    """Process YOLO annotation files and extract image details.

    Args:
        annotation_files: List of paths to YOLO annotation files (.txt) and data.yaml

    Returns:
        Tuple containing:
        - Dictionary of image details indexed by file location
        - List of image filenames missing annotations
        - Dictionary of class-wise splits from data.yaml
    """
    complete_images = {}
    missing_annotations = []
    classwise_splits = {}
    logging.info(
        "Processing %d annotation files",
        len(annotation_files),
    )
    if not annotation_files:
        logging.warning("No annotation files provided")
        return (
            complete_images,
            missing_annotations,
            classwise_splits,
        )
    txt_files = [f for f in annotation_files if f.lower().endswith(".txt")]
    yaml_files = [f for f in annotation_files if f.lower().endswith(".yaml")]
    class_names = []
    if yaml_files:
        yaml_file = yaml_files[0]
        try:
            with open(yaml_file, "r", encoding="utf-8") as file_obj:
                yaml_data = yaml.safe_load(file_obj)
                class_names = yaml_data.get("names", [])
                for name in class_names:
                    if re.search("[-\\d:]", name):
                        logging.warning(
                            "Class name '%s' appears to be incorrectly formatted. Please recheck.",
                            name,
                        )
                classwise_splits = {
                    name: {
                        "train": 0,
                        "val": 0,
                        "test": 0,
                        "unassigned": 0,
                    }
                    for name in class_names
                }
        except Exception as err:
            logging.error(
                "Error reading YAML file %s: %s",
                yaml_file,
                err,
            )
    else:
        logging.warning("No data.yaml file found. Class splits will not be initialized.")
    for file_index, txt_file in enumerate(txt_files, 1):
        logging.debug(
            "\nProcessing file %d/%d: %s",
            file_index,
            len(txt_files),
            txt_file,
        )
        if not os.path.exists(txt_file):
            logging.warning("File not found: %s", txt_file)
            continue
        try:
            filename = ".".join(os.path.basename(txt_file).split(".")[:-1])
            split_type = get_corresponding_split_type(txt_file)
            if filename.lower().startswith("readme"):
                continue
            annotations = []
            processed = 0
            skipped = 0
            with open(txt_file, "r", encoding="utf-8") as file_obj:
                for line_num, line in enumerate(file_obj, 1):
                    try:
                        parts = line.strip().split()
                        if len(parts) < 5:
                            skipped += 1
                            continue
                        class_id = int(parts[0])
                        bbox = [float(x) for x in parts[1:5]]
                        if not all(0 <= x <= 1 for x in bbox):
                            logging.warning(
                                "Invalid bbox values in %s, line %d",
                                txt_file,
                                line_num,
                            )
                            skipped += 1
                            continue
                        category = (
                            class_names[class_id] if class_id < len(class_names) else str(class_id)
                        )
                        bbox_center = [
                            bbox[0],
                            bbox[1],
                        ]
                        bbox_width = bbox[2]
                        bbox_height = bbox[3]
                        bbox_area = bbox_width * bbox_height
                        annotation_json = {
                            "id": str(generate_short_uuid()),
                            "segmentation": [],
                            "isCrowd": [],
                            "confidence": 0.0,
                            "bbox": bbox,
                            "height": float(bbox_height),
                            "width": float(bbox_width),
                            "center": bbox_center,
                            "area": float(bbox_area),
                            "category": str(category),
                            "masks": [],
                        }
                        annotations.append(annotation_json)
                        if category in classwise_splits:
                            classwise_splits[category][split_type] += 1
                        processed += 1
                    except Exception as err:
                        logging.error(
                            "Error processing line %d in %s: %s",
                            line_num,
                            txt_file,
                            err,
                        )
                        skipped += 1
                        continue
            if annotations:
                key = f"{filename}"
                complete_images[key] = {
                    "splitType": split_type,
                    "file_name": filename,
                    "annotations": annotations,
                }
            else:
                missing_annotations.append(filename)
        except Exception as err:
            logging.error(
                "Error processing file %s: %s",
                txt_file,
                err,
            )
            traceback.print_exc()
            continue
    for (
        category,
        counts,
    ) in classwise_splits.items():
        counts["total"] = sum(counts.values())
    logging.info("\nFinal summary:")
    logging.info(
        "Complete images: %d",
        len(complete_images),
    )
    logging.info(
        "Missing annotations: %d",
        len(missing_annotations),
    )
    return (
        complete_images,
        missing_annotations,
        classwise_splits,
    )


def add_yolo_dataset_items_details(batch_dataset_items, images_details):
    """Add image details to batch dataset items.

    Args:
        batch_dataset_items: List of dataset items to process
        images_details: Dictionary of image details indexed by filename

    Returns:
        List of processed dataset items with added details
    """
    processed_batch = []
    for dataset_item in batch_dataset_items:
        image_key = ".".join(dataset_item.get("filename").split(".")[:-1])
        if image_key not in images_details:
            logging.warning(
                "'%s' not found in images_details",
                image_key,
            )
            continue
        dataset_item.update(images_details[image_key])
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None
                    for k in [
                        "image_height",
                        "image_width",
                    ]
                ),
            }
        )
    return processed_batch
