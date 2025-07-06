"""Module providing unlabelled functionality."""

import logging


def add_unlabelled_dataset_items_details(
    batch_dataset_items,
):
    """Add empty details to unlabelled dataset items.

    Args:
        batch_dataset_items: List of dataset items to process

    Returns:
        List of processed dataset items with empty annotation details
    """
    processed_batch = []
    logging.debug(
        "Batch dataset items: %s",
        batch_dataset_items,
    )
    for dataset_item in batch_dataset_items:
        split, category, annotations = (
            "unassigned",
            "",
            [],
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
