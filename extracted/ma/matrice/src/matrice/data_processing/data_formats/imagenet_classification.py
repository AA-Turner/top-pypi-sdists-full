"""Module providing imagenet_classification functionality."""

import logging
import os
from collections import defaultdict
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
)
from matrice.data_processing.server_utils import (
    generate_short_uuid,
)


def add_imagenet_dataset_items_details(
    batch_dataset_items,
):
    """Add ImageNet-specific details to dataset items.

    Args:
        batch_dataset_items: List of dataset items to process

    Returns:
        List of processed dataset items with added details
    """
    processed_batch = []
    logging.debug(
        "Batch dataset items: %s",
        batch_dataset_items,
    )
    for dataset_item in batch_dataset_items:
        split, category, annotations = get_imagenet_dataset_item_details(
            dataset_item.get("fileLocation")
        )
        dataset_item.update(
            {
                "splitType": split,
                "category": category,
                "annotations": annotations,
            }
        )
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    k in dataset_item
                    for k in [
                        "image_height",
                        "image_width",
                    ]
                ),
            }
        )
    logging.debug("Processed batch: %s", processed_batch)
    return processed_batch


def get_imagenet_dataset_item_details(image_path):
    """Extract details from an ImageNet image path.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple containing:
        - split: Dataset split (train, val, test, or unassigned)
        - category: Image category
        - annotations: List of annotation objects
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


def get_classwise_splits_imagenet(
    dataset_items_batches,
):
    """Count images per category and split in ImageNet dataset.

    Args:
        dataset_items_batches: Batches of dataset items

    Returns:
        Dictionary of class-wise split counts or None if no classes found
    """
    classwise_splits = defaultdict(
        lambda: {
            "train": 0,
            "test": 0,
            "val": 0,
            "unassigned": 0,
        }
    )
    logging.debug(
        "Dataset items batches: %s",
        dataset_items_batches,
    )
    for batch in dataset_items_batches:
        for item in batch:
            category = item.get("category")
            split_type = item.get("splitType")
            if category is not None and split_type is not None:
                classwise_splits[category][split_type] += 1
    if not classwise_splits:
        return None
    for (
        category,
        counts,
    ) in classwise_splits.items():
        counts["total"] = sum(counts.values())
    return classwise_splits
