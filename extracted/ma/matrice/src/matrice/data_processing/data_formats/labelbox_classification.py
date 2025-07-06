"""Module providing labelbox_classification functionality."""

import json
import logging
import os
import re
import shutil
import traceback
from urllib.parse import urlparse
import requests
from matrice.data_processing.server_utils import (
    generate_short_uuid,
    download_file,
)


def load_ndjson(file_path):
    """Read an NDJSON file and extract valid JSON objects.

    Args:
        file_path: Path to the NDJSON file

    Returns:
        List of parsed JSON objects
    """
    with open(file_path, "r", encoding="utf-8") as file_obj:
        raw_text = file_obj.read()
    json_objects = re.findall(
        "\\{.*?\\}(?=\\s*\\{|\\s*$)",
        raw_text,
        re.DOTALL,
    )
    parsed_data = []
    for obj in json_objects:
        try:
            parsed_data.append(json.loads(obj))
        except json.JSONDecodeError as err:
            logging.error("Invalid JSON entry: %s", err)
    return parsed_data


def get_labelbox_classification_image_details(
    annotation_files,
):
    """Process Labelbox NDJSON annotation files and extract image details.

    Args:
        annotation_files: List of paths to Labelbox NDJSON annotation files

    Returns:
        Tuple containing:
        - Dictionary of image details indexed by file location
        - List of image entries missing annotations
        - Dictionary of class-wise splits
    """
    complete_images = {}
    missing_annotations = []
    missing_dimensions = {}
    classwise_splits = {}
    logging.info(
        "Processing %d annotation files",
        len(annotation_files),
    )
    if not annotation_files:
        logging.error("No annotation files provided")
        return (
            complete_images,
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
        entries = load_ndjson(file_path)
        for entry in entries:
            try:
                row_data = entry.get("data_row", {}).get("row_data", "")
                parsed_url = urlparse(row_data)
                split_type = "unassigned"
                for segment in parsed_url.path.split("/"):
                    if segment in [
                        "train",
                        "val",
                        "test",
                    ]:
                        split_type = segment
                        break
                external_id = entry["data_row"].get("external_id", "unknown")
                media_attrs = entry.get("media_attributes", {})
                height = media_attrs.get("height", None)
                width = media_attrs.get("width", None)
                annotations = []
                for project in entry.get("projects", {}).values():
                    for label in project.get("labels", []):
                        for obj in label.get("annotations", {}).get("classifications", []):
                            category = obj.get("radio_answer").get("name")
                            if category not in classwise_splits:
                                classwise_splits[category] = {
                                    "train": 0,
                                    "val": 0,
                                    "test": 0,
                                    "unassigned": 0,
                                }
                            classwise_splits[category][split_type] += 1
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
                                "category": str(category),
                                "masks": [],
                            }
                            annotations.append(annotation)
                key = f"{external_id}"
                details = {
                    "splitType": split_type,
                    "file_name": external_id,
                    "image_url": row_data,
                    "annotations": annotations,
                }
                if height is not None and width is not None:
                    details.update(
                        {
                            "image_height": height,
                            "image_width": width,
                            "image_area": height * width,
                        }
                    )
                else:
                    missing_dimensions[key] = details
                if key in complete_images:
                    complete_images[key]["annotations"].extend(annotations)
                else:
                    complete_images[key] = details
            except Exception as err:
                logging.error(
                    "Error processing entry: %s",
                    err,
                )
                traceback.print_exc()
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
    logging.info(
        "Missing dimensions: %d",
        len(missing_dimensions),
    )
    return (
        {**complete_images, **missing_dimensions},
        missing_annotations,
        classwise_splits,
    )


def add_labelbox_classification_dataset_items_details(batch_dataset_items, images_details):
    """Add image details to batch dataset items.

    Args:
        batch_dataset_items: List of dataset items to process
        images_details: Dictionary of image details indexed by image filename

    Returns:
        List of processed dataset items with added details
    """
    processed_batch = []
    for dataset_item in batch_dataset_items:
        image_key = f"{dataset_item.get('filename')}"
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
                    k in images_details[image_key]
                    for k in [
                        "image_height",
                        "image_width",
                    ]
                ),
            }
        )
    return processed_batch


def add_labelbox_classification_dataset_item_local_file_path(
    batch_dataset_items, base_dataset_path
):
    """Add local file paths to dataset items and download missing images.

    Args:
        batch_dataset_items: List of dataset items to process
        base_dataset_path: Base path for dataset storage

    Returns:
        List of processed dataset items with local file paths
    """
    processed_batch = []
    for dataset_item in batch_dataset_items:
        if not dataset_item.get("is_complete"):
            image_path = f"{base_dataset_path}/images/{dataset_item.get('filename')}"
            if not os.path.exists(image_path):
                logging.warning(
                    "Image not found, will download it: %s",
                    image_path,
                )
                download_file(
                    dataset_item["sample_details"]["image_url"],
                    image_path,
                )
            dataset_item["sample_details"]["local_file_path"] = image_path
        processed_batch.append(dataset_item)
    return processed_batch


def download_labelbox_classification_images(images_path, labelbox_annotations_path):
    """Download Labelbox images from annotation file and save them.

    Args:
        images_path: Path to save downloaded images
        labelbox_annotations_path: Path to the annotations file
    """
    os.makedirs(images_path, exist_ok=True)
    annotations = load_ndjson(labelbox_annotations_path)
    for entry in annotations:
        try:
            data_row = entry.get("data_row", {})
            image_url = data_row.get("row_data")
            image_name = data_row.get("external_id")
            if not image_url or not image_name:
                continue
            image_path = os.path.join(images_path, image_name)
            if os.path.exists(image_path):
                continue
            try:
                response = requests.get(
                    image_url,
                    stream=True,
                    timeout=30,
                )
                response.raise_for_status()
                with open(image_path, "wb") as img_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        img_file.write(chunk)
                logging.debug(
                    "Downloaded %s successfully.",
                    image_name,
                )
            except requests.exceptions.RequestException as err:
                logging.error(
                    "Failed to download %s: %s",
                    image_name,
                    err,
                )
        except Exception as err:
            logging.error("Error processing entry: %s", err)


def download_labelbox_classification_dataset(dataset_id, labelbox_annotations_path):
    """Download Labelbox dataset and organize it into a structured format.

    Args:
        dataset_id: Identifier for the dataset
        labelbox_annotations_path: Path to the annotations file

    Returns:
        Dataset ID
    """
    annotations_dir = f"{dataset_id}/annotations/"
    images_dir = f"{dataset_id}/images"
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(annotations_dir, exist_ok=True)
    shutil.copy2(
        labelbox_annotations_path,
        os.path.join(
            annotations_dir,
            os.path.basename(labelbox_annotations_path),
        ),
    )
    logging.debug(
        "Copied annotation file from %s to %s",
        labelbox_annotations_path,
        annotations_dir,
    )
    download_labelbox_classification_images(images_dir, labelbox_annotations_path)
    return dataset_id
