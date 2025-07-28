"""Module providing data_augmentation functionality."""

import os
import cv2
import logging
from typing import Any, List, Dict
from queue import Queue
from matrice.data_processing.pipeline import (
    Pipeline,
)
from matrice.data_processing.data_prep import (
    dataset_items_producer,
)
from matrice.data_processing.client import (
    add_batch_presigned_upload_urls,
    upload_batch_files,
)
from matrice.data_processing.server_utils import (
    download_file,
    generate_short_uuid,
)
from matrice.data_processing.client_utils import (
    update_partitions_numbers,
    create_partition_stats,
    SAMPLES_PARTITION_TYPE,
)
from matrice.data_processing.image_augmentations import (
    get_augmentation_compose,
)


def create_augmentation_fns(
    augmentation_configs: Dict,
) -> List[callable]:
    """Create a function to perform data augmentation.

    Args:
        augmentation_configs: Dictionary containing augmentation parameters

    Returns:
        List of augmentation functions
    """
    augmentations = []
    for augmentation_config in augmentation_configs:
        augmentations.append(get_augmentation_compose(augmentation_config))
    return augmentations


def load_image(dataset_item):
    image = cv2.imread(dataset_item["filename"])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def load_bboxes(dataset_item):
    bboxes = []
    for info in dataset_item["versionInfo"]:
        for annotation in info["annotations"]:
            bboxes.append(annotation["bbox"])
    return bboxes


def augment_dataset_items(batch_dataset_items, augmentation_fns):
    augmented_dataset_items = []
    for dataset_item in batch_dataset_items:
        if not dataset_item:
            continue
        for augmentation_fn in augmentation_fns:
            augmented_dataset_item = dataset_item.copy()
            image = load_image(dataset_item)
            bboxes = load_bboxes(dataset_item)
            augmented_dataset_item["augmentation_result"] = augmentation_fn(
                image=image,
                bboxes=bboxes,
                class_labels=[None for _ in range(len(bboxes))],
            )
            augmented_dataset_items.append(augmented_dataset_item)
    return augmented_dataset_items


def save_augmented_images(batch_dataset_items, dataset_id):
    for item in batch_dataset_items:
        new_filename = f"{generate_short_uuid()}.{os.path.splitext(item['filename'])[-1]}"
        augmentation_result = item["augmentation_result"]
        cv2.imwrite(
            new_filename,
            augmentation_result["image"],
        )
        item["filename"] = new_filename
        item["local_file_path"] = new_filename
        item["cloud_file_path"] = f"{dataset_id}/{new_filename}"
        for i in range(len(augmentation_result["bboxes"])):
            item["versionInfo"][0]["annotation"][i]["bbox"] = augmentation_result["bboxes"][i]
    return batch_dataset_items


def filter_dataset_items(
    batch_dataset_items: Dict[str, List],
    dataset_version: str = "v1.0",
) -> List[Dict]:
    """Filter dataset items based on the set type (train/test/val).

    Args:
        dataset_items: Dictionary containing version info and items
        dataset_version: Version string to filter by

    Returns:
        List of training items for the specified version
    """
    filtered_dataset_items = []
    for item in batch_dataset_items:
        for info in item["versionInfo"]:
            if info["version"] == dataset_version and info["itemSetType"] == "train":
                item["versionInfo"] = [info]
                filtered_dataset_items.append(item)
    return filtered_dataset_items


def download_images(
    dataset_items: List[Dict],
) -> List[Dict]:
    """Download images for dataset items.

    Args:
        dataset_items: List of dataset items containing file locations and names

    Returns:
        List of successfully downloaded items
    """
    downloaded_images = []
    for dataset_item in dataset_items:
        try:
            download_file(
                dataset_item["fileLocation"],
                dataset_item["filename"],
            )
            downloaded_images.append(dataset_item)
        except Exception as e:
            logging.error(
                "Error downloading image %s: %s",
                dataset_item["filename"],
                str(e),
            )
    return downloaded_images


def batch_insert_dataset_items(batch, dataset_id, rpc):
    logging.debug("batch to insert: %s", batch)
    payload = {
        "datasetId": dataset_id,
        "datasetItems": batch,
    }
    resp = rpc.post(
        "/v2/dataset/insert_dataset_items",
        payload=payload,
    )
    logging.info("Response from insert: %s", resp)
    return batch


def calculate_partition_stats(
    dataset_items: List[Dict],
) -> List[Dict]:
    """Calculate partition statistics for dataset items.

    Args:
        dataset_items: List of dataset items
    """
    partition_stats = {}
    for item in dataset_items:
        if item["partitionNumber"] not in partition_stats:
            partition_stats[item["partitionNumber"]] = {
                "partitionNum": item["partitionNumber"],
                "sampleCount": 0,
                "diskSizeMB": 0,
                "type": SAMPLES_PARTITION_TYPE,
            }
        partition_stats[item["partitionNumber"]]["sampleCount"] += 1
        partition_stats[item["partitionNumber"]]["diskSizeMB"] += os.path.getsize(
            item["local_file_path"]
        ) / (1024 * 1024)
    return list(partition_stats.values())


def get_data_augmentation_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    augmentation_configs: list,
    max_attempts: int = 5,
    bucket_alias: str = "",
    account_number: str = "",
) -> Pipeline:
    """Get the data augmentation pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: Dataset ID
        dataset_version: Dataset version
        augmentation_configs: List of augmentation configurations
        max_attempts: Maximum number of upload retry attempts
        bucket_alias: Storage bucket alias
        account_number: Account number for storage access

    Returns:
        Configured Pipeline object for data augmentation
    """
    dataset_items_queue = Queue()
    download_images_queue = Queue()
    dataset_items_augmentation_queue = Queue()
    update_dataset_items_queue = Queue()
    save_augmented_images_queue = Queue()
    upload_files_queue = Queue()
    insert_dataset_items_queue = Queue()
    pipeline = Pipeline()
    pipeline.add_producer(
        process_fn=dataset_items_producer,
        process_params={
            "rpc": rpc,
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "pipeline_queue": dataset_items_queue,
        },
    )
    pipeline.add_stage(
        stage_name="Filter Dataset Items",
        process_fn=filter_dataset_items,
        pull_queue=dataset_items_queue,
        push_queue=download_images_queue,
        process_params={"dataset_version": dataset_version},
        num_threads=1,
    )
    pipeline.add_stage(
        stage_name="Download Original Images",
        process_fn=download_images,
        pull_queue=download_images_queue,
        push_queue=dataset_items_augmentation_queue,
        num_threads=15,
    )
    pipeline.add_stage(
        stage_name="Augment Dataset Items",
        process_fn=augment_dataset_items,
        pull_queue=dataset_items_augmentation_queue,
        push_queue=update_dataset_items_queue,
        process_params={"augmentation_fns": create_augmentation_fns(augmentation_configs)},
        num_threads=10,
    )
    pipeline.add_stage(
        stage_name="Fetch Upload Presigned URLs",
        pull_queue=update_dataset_items_queue,
        push_queue=save_augmented_images_queue,
        process_fn=add_batch_presigned_upload_urls,
        process_params={
            "rpc": rpc,
            "partition_type": SAMPLES_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
        },
        num_threads=10,
    )
    pipeline.add_stage(
        stage_name="Save Augmented Images",
        pull_queue=save_augmented_images_queue,
        push_queue=upload_files_queue,
        process_fn=save_augmented_images,
        process_params={"dataset_id": dataset_id},
        num_threads=10,
    )
    pipeline.add_stage(
        stage_name="Upload Augmented Images",
        pull_queue=upload_files_queue,
        push_queue=insert_dataset_items_queue,
        process_fn=upload_batch_files,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )
    return pipeline


class DataAugmentation:
    """Class to handle dataset preparation."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataAugmentation.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
        """
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        url = f"/v1/project/action/{self.action_record_id}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_type = self.action_doc["action"]
        self.job_params = self.action_doc["jobParams"]
        self.dataset_id = self.job_params["dataset_id"]
        self.dataset_version = self.job_params["dataset_version"]
        self.augmentations = self.job_params["augmentations"]

    def update_status(
        self,
        stepCode: str,
        status: str,
        status_description: str,
    ) -> None:
        """Update status of data preparation.

        Args:
            stepCode: Code indicating current step
            status: Status of step
            status_description: Description of status
        """
        try:
            logging.info(status_description)
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            logging.error(
                "Exception in update_status: %s",
                str(e),
            )
            raise

    def start_processing(self) -> None:
        """Start dataset augmentation processing."""
        self.update_status(
            "DCKR_PROC",
            "OK",
            "Dataset started augmentation",
        )
        self.pipeline = get_data_augmentation_pipeline(
            rpc=self.rpc,
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            augmentation_configs=self.augmentations,
        )
        self.pipeline.start()
        self.pipeline.wait_to_finish_processing_and_stop()
        new_dataset_items = self.pipeline.get_all_items_from_last_stage()
        update_partitions_numbers(
            self.rpc,
            self.dataset_id,
            new_dataset_items,
            partition_key="partitionNumber",
        )
        create_partition_stats(
            rpc=self.rpc,
            dataset_id=self.dataset_id,
            source_version=self.dataset_version,
            target_version=self.dataset_version,
            partition_stats=calculate_partition_stats(new_dataset_items),
        )
        batch_insert_dataset_items(
            new_dataset_items,
            self.dataset_id,
            self.rpc,
        )
        self.update_status(
            "SUCCESS",
            "SUCCESS",
            "Dataset Augmentation completed",
        )
