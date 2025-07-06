"""Module providing video_server functionality."""

from matrice.data_processing.data_formats.yolo_detection import (
    convert_payload_to_coco_format,
)
from matrice.data_processing.data_formats.video_mscoco_detection import (
    get_msococo_videos_details,
    add_mscoco_video_dataset_items_details,
)
from matrice.data_processing.server_utils import (
    get_unprocessed_partitions,
)
from matrice.data_processing.pipeline import (
    Pipeline,
)
from matrice.data_processing.server import (
    get_annotation_files,
    partition_items_producer,
    batch_download_samples,
    batch_calculate_sample_properties,
    submit_partition_status,
)
import os
import traceback
import logging
from queue import Queue
from typing import List, Dict, Any, Optional

TMP_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tmp",
)
os.makedirs(TMP_FOLDER, exist_ok=True)
logging.info("Created temporary folder at %s", TMP_FOLDER)


def calculate_video_properties(
    video_details: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate properties of a video.

    Args:
        video_details: Dictionary containing video metadata

    Returns:
        Updated video details with calculated properties
    """
    import cv2
    if video_details.get("is_complete"):
        return video_details
    dataset_item = video_details.get("sample_details")
    try:
        cap = cv2.VideoCapture(dataset_item["local_file_path"])
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {dataset_item['local_file_path']}")
        try:
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = float(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames <= 0:
                total_frames = 0
                while cap.isOpened():
                    ret, _ = cap.read()
                    if not ret:
                        break
                    total_frames += 1
            if width <= 0 or height <= 0 or fps <= 0:
                ret, frame = cap.read()
                if ret:
                    height, width = frame.shape[:2]
                    if fps <= 0:
                        fps = 30.0
                        logging.warning(
                            "Invalid FPS for %s, using default value: 30.0",
                            dataset_item.get("filename"),
                        )
            dataset_item.update(
                {
                    "video_height": height,
                    "video_width": width,
                    "fps": round(fps, 2),
                    "total_frames": total_frames,
                    "duration_seconds": (round(total_frames / fps, 2) if fps > 0 else 0),
                }
            )
            is_complete = all(
                dataset_item.get(k, 0) > 0
                for k in [
                    "video_height",
                    "video_width",
                    "fps",
                    "total_frames",
                ]
            )
            if not is_complete:
                logging.warning(
                    "Some video properties are invalid for %s: height=%s, width=%s, fps=%s, frames=%s",
                    dataset_item.get("filename"),
                    height,
                    width,
                    fps,
                    total_frames,
                )
        finally:
            cap.release()
        os.remove(dataset_item["local_file_path"])
        return {
            "sample_details": dataset_item,
            "is_complete": is_complete,
        }
    except Exception as e:
        logging.error(
            "Error processing video %s: %s",
            dataset_item.get("filename"),
            e,
        )
        if "cap" in locals() and cap is not None:
            cap.release()
        return {
            "sample_details": dataset_item,
            "is_complete": False,
        }


def _group_annotations_by_frame(
    annotations: List[Dict[str, Any]],
) -> Dict[int, List[Dict[str, Any]]]:
    """Group annotations by frame ID for efficient processing.

    Args:
        annotations: List of annotation dictionaries

    Returns:
        Dictionary mapping frame IDs to lists of annotations
    """
    frame_annotations = {}
    for annotation in annotations:
        frame_id = annotation.get("frame_id")
        if frame_id is not None:
            if frame_id not in frame_annotations:
                frame_annotations[frame_id] = []
            frame_annotations[frame_id].append(annotation)
    return frame_annotations


def batch_update_video_dataset_items(
    batch_video_details: List[Dict[str, Any]],
    rpc: Any,
    dataset_id: str,
    version: str,
    attempts: int = 3,
    is_yolo: bool = False,
) -> List[Dict[str, Any]]:
    """Update video dataset items in batch.

    Args:
        batch_video_details: List of video details to update
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        version: Version of the dataset
        attempts: Number of retry attempts
        is_yolo: Whether the dataset is in YOLO format

    Returns:
        List of updated dataset items
    """
    retry_count = 0
    while retry_count < attempts:
        try:
            logging.debug(
                "Attempting to update batch of %s video items (attempt %s/%s)",
                len(batch_video_details),
                retry_count + 1,
                attempts,
            )
            payload = {
                "datasetId": str(dataset_id),
                "items": [
                    {
                        "datasetItemId": str(dataset_item.get("_id")),
                        "version": str(version),
                        "splitType": str(dataset_item.get("splitType")),
                        "annotations": dataset_item.get("annotations"),
                        "height": int(dataset_item.get("video_height")),
                        "width": int(dataset_item.get("video_width")),
                        "fps": float(dataset_item.get("fps")),
                        "total_frames": int(dataset_item.get("total_frames")),
                        "duration_seconds": float(
                            dataset_item.get(
                                "duration_seconds",
                                0.0,
                            )
                        ),
                        "frame_annotations": _group_annotations_by_frame(
                            dataset_item.get("annotations", [])
                        ),
                    }
                    for dataset_item in batch_video_details
                ],
            }
            if is_yolo:
                payload = convert_payload_to_coco_format(payload)
            resp = rpc.put(
                path="/v2/dataset/update-video-dataset-items/",
                payload=payload,
            )
            logging.debug(
                "Update video dataset items payload: %s",
                payload,
            )
            if resp.get("success"):
                logging.debug(
                    "Successfully updated batch of %s video items",
                    len(batch_video_details),
                )
                for item in batch_video_details:
                    item["status"] = "processed"
                return batch_video_details
            logging.error(
                "Failed to update batch: %s",
                resp.get("data"),
            )
            retry_count += 1
        except Exception as e:
            logging.error("Error updating batch: %s", e)
            retry_count += 1
    for item in batch_video_details:
        item["status"] = "errored"
    return batch_video_details


def get_mscoco_video_server_processing_pipeline(
    rpc: Any,
    dataset_id: str,
    dataset_version: str,
    action_record_id: str,
    bucket_alias: str = "",
    account_number: str = "",
    project_id: str = "",
) -> Optional[Pipeline]:
    """Create and configure the processing pipeline.

    Args:
        rpc: RPC client for making API calls
        dataset_id: ID of the dataset
        dataset_version: Version number of the dataset
        action_record_id: ID of the action record

    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info(
            "Setting up processing pipeline for dataset %s version %s",
            dataset_id,
            dataset_version,
        )
        annotation_files = get_annotation_files(rpc, dataset_id, dataset_version)
        logging.info("Processing MSCOCO image details")
        (
            videos_details,
            missing_annotations,
            classwise_splits,
        ) = get_msococo_videos_details(annotation_files)
        unprocessed_partitions = get_unprocessed_partitions(rpc, dataset_id, dataset_version)
        logging.info(
            "Found %s unprocessed partitions",
            len(unprocessed_partitions),
        )
        dataset_items_queue = Queue()
        download_images_queue = Queue()
        calculate_image_properties_queue = Queue()
        update_dataset_items_queue = Queue()
        pipeline = Pipeline()
        for partition in unprocessed_partitions:
            pipeline.add_producer(
                process_fn=partition_items_producer,
                process_params={
                    "rpc": rpc,
                    "dataset_id": dataset_id,
                    "partition": partition,
                    "pipeline_queue": dataset_items_queue,
                    "download_images_required": False,
                },
                partition_num=partition,
            )
        logging.info("Configuring pipeline stages")
        pipeline.add_stage(
            stage_name="Add Dataset Items Details",
            process_fn=add_mscoco_video_dataset_items_details,
            pull_queue=dataset_items_queue,
            push_queue=download_images_queue,
            process_params={"images_details": videos_details},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Download Videos",
            process_fn=batch_download_samples,
            pull_queue=download_images_queue,
            push_queue=calculate_image_properties_queue,
            process_params={
                "rpc": rpc,
                "bucket_alias": bucket_alias,
                "account_number": account_number,
                "project_id":project_id,
            },
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Calculate Video Properties",
            process_fn=batch_calculate_sample_properties,
            pull_queue=calculate_image_properties_queue,
            push_queue=update_dataset_items_queue,
            process_params={"properties_calculation_fn": calculate_video_properties},
            num_threads=5,
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_video_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        pipeline.add_stop_callback(
            callback=submit_partition_status,
            process_params={
                "rpc": rpc,
                "action_record_id": action_record_id,
                "dataset_id": dataset_id,
                "version": dataset_version,
                "annotation_type": "detection",
            },
        )
        logging.info("Pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error("Error setting up pipeline: %s", e)
        traceback.print_exc()
        raise
