"""Module providing client functionality."""

import os
from queue import Queue
import logging
from matrice.data_processing.pipeline import Pipeline
from concurrent.futures import ThreadPoolExecutor, as_completed
from matrice.data_processing.client_utils import (
    ANNOTATION_PARTITION_TYPE,
    SAMPLES_PARTITION_TYPE,
    scan_dataset,
    get_annotations_partition,
    get_images_partitions,
    get_youtube_bb_partitions,
    get_cloud_file_path,
    update_annotation_bucket_url,
    get_batch_pre_signed_upload_urls,
    upload_file,
    compress_annotation_files,
    update_partitions_numbers,
    create_partition_stats,
    get_youtube_bb_relative_path,
    get_mot_partitions,
    get_video_mot_cloud_file_path,
    get_video_mscoco_cloud_file_path,
    get_davis_partitions,
    get_davis_relative_path,
    get_video_imagenet_partitions,
    get_kinetics_partitions,
    get_video_mscoco_partitions,
    create_video_blank_dataset_items,
    extract_frames_from_videos,
    restructure_davis_dataset
)


def get_partition_status(base_path, skip_annotation_partition=False):
    logging.info("Getting partition status")
    annotation_partition, images_partitions = (
        None,
        [],
    )
    annotation_files, image_files = scan_dataset(base_path)
    if annotation_files:
        logging.debug("Debug - annotation_files length: %s", len(annotation_files))
    if image_files:
        logging.debug("Debug - image_files length: %s", len(image_files))
    if not skip_annotation_partition:
        annotation_partition = get_annotations_partition(annotation_files)
    images_partitions = get_images_partitions(image_files)
    if annotation_partition:
        logging.debug("Debug - annotation_partition length: %s", len(annotation_partition))
    else:
        logging.debug("Debug - annotation_partition is None")
    if images_partitions:
        logging.debug("Debug - images_partitions length: %s", len(images_partitions))
    else:
        logging.debug("Debug - images_partitions is None")
    return annotation_partition, images_partitions


def get_video_partition_status(
    base_path,
    skip_annotation_partition=False,
    get_partitions=get_youtube_bb_partitions,
    rename_annotation_files=False,
    input_type=None,
):
    logging.info(
        "Getting partition %s status with base path %s",
        input_type,
        base_path,
    )
    annotation_partition, images_partitions = (
        None,
        [],
    )
    annotation_files, image_files = scan_dataset(
        base_path,
        rename_annotation_files,
        input_type,
    )
    if not skip_annotation_partition:
        annotation_partition = get_annotations_partition(annotation_files)
    unique_videos=None
    images_partitions, unique_videos = get_partitions(image_files)
    return annotation_partition, images_partitions, unique_videos


def get_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    files = partition["files"]

    def create_file_info(file_path):
        file_name = os.path.basename(file_path)
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": file_name,
            "cloud_file_path": get_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    if len(files) <= batch_size:
        return [[create_file_info(f) for f in files]]
    batches = []
    num_batches = (len(files) + batch_size - 1) // batch_size
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, len(files))
        batch_files = files[start_idx:end_idx]
        batches.append([create_file_info(f) for f in batch_files])
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    return batches


def get_video_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]

    def create_file_info(file_path, transformed_frame_number):
        file_name = os.path.basename(file_path)
        video_identifier, frame_number = file_name.rsplit("_", 1)
        frame_number = int(frame_number.split(".")[0])
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": file_name,
            "video_identifier": video_identifier,
            "frame_number": frame_number,
            "transformed_frame_number": transformed_frame_number,
            "cloud_file_path": get_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []
    for video_files in videos:
        if not video_files:
            continue
        video_info = [create_file_info(file, idx) for idx, file in enumerate(video_files)]
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "batches from get_video_partition_batches: %s",
        batches,
    )
    return batches


def get_video_mot_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]
    logging.debug("batch_size is %s", batch_size)

    def create_file_info(file_path):
        os.path.basename(os.path.dirname(file_path))
        video_identifier = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        path_parts = file_path.split(os.sep)[::-1]
        split = "unlabeled"
        for part in path_parts:
            if part.lower() in {
                "train",
                "test",
                "val",
            }:
                split = part
                break
        file_name = os.path.basename(file_path)
        frame_number = int(os.path.splitext(file_name)[0])
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": file_name,
            "video_identifier": video_identifier,
            "frame_number": frame_number,
            "cloud_file_path": get_video_mot_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
            "split": split,
        }

    batches = []
    current_batch = []
    for video_files in videos:
        if not video_files:
            continue
        video_info = [create_file_info(file) for file in video_files]
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "batches from get_video_partition_batches: %s",
        batches,
    )
    return batches


def get_video_davis_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]
    partition_type = partition["type"]  # train, val, or test
    logging.debug("batch_size is %s", batch_size)

    def create_file_info(file_path):
        video_dir = os.path.dirname(file_path)                     # .../partition_type/video_name
        video_name = os.path.basename(video_dir)                  # video_1
        partition_dir = os.path.basename(os.path.dirname(video_dir))  # train / val / test
        video_identifier = f"{partition_dir}_{video_name}"        # e.g., train_video_1
        file_name = os.path.basename(file_path)
        frame_number = int(os.path.splitext(file_name)[0])
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition_type,
            "local_file_path": file_path,
            "file_name": file_name,
            "video_identifier": video_identifier,
            "frame_number": frame_number,
            "cloud_file_path": get_video_mot_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []
    for video_files in videos:
        if not video_files:
            continue
        video_info = [create_file_info(file) for file in video_files]
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)

    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "batches from get_video_partition_batches: %s",
        batches,
    )
    return batches


def get_video_imagenet_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]
    logging.debug("Batch size is %s", batch_size)
    logging.debug(
        "In-get_video_imagenet_partition_batches-videos are %s",
        videos,
    )

    def create_file_info(file_path):
        video_name = os.path.basename(file_path)
        class_folder = os.path.basename(os.path.dirname(file_path))
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": video_name,
            "video_identifier": class_folder,
            "cloud_file_path": get_video_mot_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []
    for video_file in videos:
        if not video_file:
            continue
        video_info = create_file_info(video_file)
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "Batches from get_video_davis_partition_batches: %s",
        batches,
    )
    return batches


def get_video_kinetics_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]
    logging.debug("Batch size is %s", batch_size)
    logging.debug(
        "In-get_video_kinetics_partition_batches-videos are %s",
        videos,
    )

    def create_file_info(file_path):
        video_name = os.path.basename(file_path)
        class_folder = os.path.basename(os.path.dirname(file_path))
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": video_name,
            "video_identifier": class_folder,
            "cloud_file_path": get_video_mot_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []
    for video_file in videos:
        if not video_file:
            continue
        video_info = create_file_info(video_file)
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "Batches from get_video_davis_partition_batches: %s",
        batches,
    )
    return batches


def get_video_mscoco_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]
    partition_type = partition["type"]  # train, val, test
    logging.debug("Batch size is %s", batch_size)

    def create_file_info(file_path):
        file_name = os.path.basename(file_path)                   # e.g., 000111.jpg
        video_dir = os.path.dirname(file_path)                    # .../test/video_003
        video_name = os.path.basename(video_dir)                  # video_003
        partition_dir = os.path.basename(os.path.dirname(video_dir))  # test
        video_identifier = f"{partition_dir}/{video_name}"        # e.g., test/video_003
        frame_number = int(os.path.splitext(file_name)[0])        # e.g., 111

        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition_type,
            "local_file_path": file_path,
            "file_name": file_name,
            "video_identifier": video_identifier,
            "frame_number": frame_number,
            "cloud_file_path": get_video_mscoco_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []

    for video_file in videos:
        if not video_file:
            continue
        video_info = [create_file_info(video_path) for video_path in video_file]
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)

    if current_batch:
        batches.append(current_batch)

    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "Batches from get_video_mscoco_partition_batches: %s",
        batches,
    )
    return batches



def get_video_youtube_bb_partition_batches(
    partition,
    batch_size,
    dataset_id,
    dataset_version,
    base_dataset_path,
    include_version_in_cloud_path=False,
):
    videos = partition["files"]

    def create_file_info(file_path, transformed_frame_number):
        file_name = os.path.basename(file_path)
        video_identifier, frame_number = file_name.rsplit("_", 1)
        frame_number = int(frame_number.split(".")[0])
        return {
            "partition_num": partition["partitionNum"],
            "partition_type": partition["type"],
            "local_file_path": file_path,
            "file_name": file_name,
            "video_identifier": video_identifier,
            "frame_number": frame_number,
            "transformed_frame_number": transformed_frame_number,
            "cloud_file_path": get_video_mot_cloud_file_path(
                dataset_id,
                dataset_version,
                base_dataset_path,
                file_path,
                include_version_in_cloud_path,
            ),
        }

    batches = []
    current_batch = []
    for video_files in videos:
        if not video_files:
            continue
        video_info = [create_file_info(file, idx) for idx, file in enumerate(video_files)]
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
        current_batch.append(video_info)
    if current_batch:
        batches.append(current_batch)
    logging.info(
        "Created %s batches for partition %s",
        len(batches),
        partition["partitionNum"],
    )
    logging.debug(
        "batches from get_video_partition_batches: %s",
        batches,
    )
    return batches


def add_batch_presigned_upload_urls(
    batch,
    rpc,
    partition_type,
    bucket_alias="",
    account_number="",
    project_id=None,
):
    logging.debug("batch to add presigned urls: %s", batch)
    cloud_paths_presigned_url_dict = get_batch_pre_signed_upload_urls(
        [file_info["cloud_file_path"] for file_info in batch],
        rpc,
        partition_type,
        bucket_alias,
        account_number,
        project_id=project_id,
    )
    for file_info in batch:
        file_info["presigned_url"] = cloud_paths_presigned_url_dict.get(
            file_info["cloud_file_path"], None
        )
    return batch


def add_video_batch_presigned_upload_urls(
    batch,
    rpc,
    partition_type,
    bucket_alias="",
    account_number="",
):
    frames = [file_info for video in batch for file_info in video]
    logging.debug("batch to add presigned urls: %s", frames)
    cloud_paths_presigned_url_dict = get_batch_pre_signed_upload_urls(
        [file_info["cloud_file_path"] for file_info in frames],
        rpc,
        partition_type,
        bucket_alias,
        account_number,
    )
    for file_info in frames:
        file_info["presigned_url"] = cloud_paths_presigned_url_dict.get(
            file_info["cloud_file_path"], None
        )
    logging.debug(
        "final batch for add_video_batch_presigned_upload_urls: %s",
        batch,
    )
    return batch


def add_video_imagenet_presigned_upload_urls(
    batch,
    rpc,
    partition_type,
    bucket_alias="",
    account_number="",
):
    videos = [video for video in batch]
    logging.debug("batch to add presigned urls: %s", videos)
    cloud_paths_presigned_url_dict = get_batch_pre_signed_upload_urls(
        [file_info["cloud_file_path"] for file_info in videos],
        rpc,
        partition_type,
        bucket_alias,
        account_number,
    )
    for file_info in videos:
        file_info["presigned_url"] = cloud_paths_presigned_url_dict.get(
            file_info["cloud_file_path"], None
        )
    logging.debug(
        "final batch for add_video_batch_presigned_upload_urls: %s",
        batch,
    )
    return batch


def upload_batch_files(batch, max_attempts=5):
    for file_info in batch:
        success = upload_file(
            file_info["local_file_path"],
            file_info["presigned_url"],
            max_attempts,
        )
        file_info["upload_success"] = success
    return batch


def upload_video_batch_files(batch, max_attempts=5):
    logging.debug(
        "upload_video_batch_files with max_attempts %s",
        max_attempts,
    )
    # Flatten the batch in one line
    frames = [file_info for video in batch for file_info in video]
    
    # Process all files in the batch using multithreading
    def upload_single_file(file_info):
        success = upload_file(
            file_info["local_file_path"],
            file_info["presigned_url"],
            max_attempts,
        )
        file_info["upload_success"] = success
        return file_info
    
    # Use ThreadPoolExecutor to parallelize uploads
    with ThreadPoolExecutor(max_workers=min(10, len(frames))) as executor:
        # Submit all upload tasks
        future_to_file = {executor.submit(upload_single_file, file_info): file_info for file_info in frames}
        
        # Process results as they complete
        for future in as_completed(future_to_file):
            try:
                future.result()
            except Exception as exc:
                file_info = future_to_file[future]
                logging.error(f"File upload failed for {file_info['local_file_path']}: {exc}")
                file_info["upload_success"] = False
        
    logging.debug(
        "final batch for add_video_batch_presigned_upload_urls: %s",
        batch,
    )
    return batch


def upload_video_imagenet_batch_files(batch, max_attempts=5):
    logging.debug(
        "batch received in upload_video_imagenet_batch_files: %s",
        batch,
    )
    logging.debug(
        "upload_video_batch_files with max_attempts %s",
        max_attempts,
    )
    
    # Use ThreadPoolExecutor to parallelize uploads
    with ThreadPoolExecutor(max_workers=min(10, len(batch))) as executor:
        # Define upload function for a single file
        def upload_single_file(file_info):
            success = upload_file(
                file_info["local_file_path"],
                file_info["presigned_url"],
                max_attempts,
            )
            file_info["upload_success"] = success
            return file_info
        
        # Submit all upload tasks
        future_to_file = {executor.submit(upload_single_file, file_info): file_info for file_info in batch}
        
        # Process results as they complete
        for future in as_completed(future_to_file):
            try:
                future.result()
            except Exception as exc:
                file_info = future_to_file[future]
                logging.error(f"File upload failed for {file_info['local_file_path']}: {exc}")
                file_info["upload_success"] = False
    
    logging.debug(
        "final batch for add_video_batch_presigned_upload_urls: %s",
        batch,
    )
    return batch


def upload_video_mot_batch_files(batch, max_attempts=5):
    frames = [file_info for video in batch for file_info in video]
    for file_info in frames:
        success = upload_file(
            file_info["cloud_file_path"],
            file_info["presigned_url"],
            max_attempts,
        )
        file_info["upload_success"] = success
    logging.debug(
        "final batch for add_video_batch_presigned_upload_urls: %s",
        batch,
    )
    return batch


def batch_create_dataset_items(batch, dataset_id, dataset_version, rpc):
    logging.debug("batch to create dataset items: %s", batch)
    payload = {
        "datasetId": dataset_id,
        "partitionNumber": batch[0]["partition_num"],
        "version": dataset_version,
        "files": [
            {
                "fileName": item["file_name"],
                "fileLocation": item["cloud_file_path"],
            }
            for item in batch
        ],
    }
    resp = rpc.post(
        "/v2/dataset/add_dataset_items",
        payload=payload,
    )
    logging.info(
        "Response from create dataset items: %s",
        resp,
    )
    return batch


def batch_create_video_youtube_bb_dataset_items(
    batch,
    dataset_id,
    dataset_version,
    project_id,
    rpc,
    input_type=None,
    num_dataset_items=0,
    dataset_item_ids=None,
):
    if not batch:
        logging.warning("Empty batch, nothing to process.")
        return batch

    logging.debug("Batch to create dataset items: %s", batch)

    for idx, video in enumerate(batch):
        total_frames = len(video)
        logging.debug("Total frames in video %d: %d", idx, total_frames)

        segment_length = 16
        logging.debug("Segment length for video %d: %d", idx, segment_length)

        # Ensure all frames share the same dataset_item_id
        dataset_item_id = video[0]["dataset_item_id"]
        for frame in video:
            if frame["dataset_item_id"] != dataset_item_id:
                raise ValueError(
                    f"Inconsistent dataset_item_id in video {idx}. Expected {dataset_item_id}, "
                    f"but got {frame['dataset_item_id']}"
                )

        segments = []
        current_segment = {}
        segment_id = 0

        for i, frame in enumerate(video):
            frame_num = frame["transformed_frame_number"]
            current_segment[frame_num] = {
                "fileLocation": frame["cloud_file_path"],
                "filename": frame["file_name"],
            }

            if len(current_segment) >= segment_length or i == total_frames - 1:
                segments.append(current_segment)
                current_segment = {}
                segment_id += 1


        logging.debug("Total segments created for video %d: %d", idx, len(segments))

        # STEP 2: Upload segments in chunks of 10
        for chunk_start in range(0, len(segments), 10):
            segment_chunk = segments[chunk_start:chunk_start + 10]
            frame_files_payload = {
                str(i): segment
                for i, segment in enumerate(segment_chunk, start=chunk_start)
            }

            payload = {
                "datasetId": dataset_id,
                "datasetItemId": dataset_item_id,
                "frameFiles": frame_files_payload,
            }
            
            logging.debug("Payload for uploading segments: %s", payload)

            logging.info("Uploading frame segments chunk for datasetItemId %s: %s",
                         dataset_item_id, list(frame_files_payload.keys()))

            resp = rpc.post(
                f"/v2/dataset/add_frame_segments?projectId={project_id}",
                payload=payload,
            )

            if not resp or not resp.get("success"):
                logging.warning("Failed to upload frame segments for chunk starting at segment %d", chunk_start)
            else:
                logging.info("Successfully uploaded segments %d–%d for datasetItemId %s",
                             chunk_start, chunk_start + len(segment_chunk) - 1, dataset_item_id)

    return batch


def batch_create_video_dataset_items(
    batch,
    dataset_id,
    dataset_version,
    project_id,
    rpc,
    input_type=None,
    num_dataset_items=0,
    dataset_item_ids=[]
):
    logging.debug("Creating batch_create_video_dataset_items with input_type %s", input_type)

    get_relative_path_fn = (
        get_davis_relative_path if input_type == "davis" else get_youtube_bb_relative_path
    )

    if not batch:
        logging.warning("Empty batch, nothing to process.")
        return batch

    logging.debug("Batch to create dataset items: %s", batch)

    segment_length = 16

    for idx, video in enumerate(batch):
        total_frames = len(video)
        logging.debug("Total frames in video %d: %d", idx, total_frames)

        dataset_item_id = video[0]["dataset_item_id"]

        # Validate dataset_item_id consistency
        for frame in video:
            if frame["dataset_item_id"] != dataset_item_id:
                raise ValueError(
                    f"Inconsistent dataset_item_id in video {idx}. "
                    f"Expected {dataset_item_id}, but got {frame['dataset_item_id']}"
                )

        segments = []
        current_segment = {}
        segment_id = 0

        for i, frame in enumerate(video):
            path = get_relative_path_fn(frame["local_file_path"])
            if path is None:
                path = frame["cloud_file_path"]

            if input_type == "mscoco_video":
                final_path= frame["cloud_file_path"]
            else:
                final_path = f"{dataset_id}/{path}"
            frame_num = frame["frame_number"]
            
            current_segment[frame_num] = {
                "fileLocation": final_path,
                "filename": frame["file_name"],
            }

            if len(current_segment) >= segment_length or i == total_frames - 1:
                segments.append(current_segment)
                current_segment = {}
                segment_id += 1

        logging.debug("Total segments created for video %d: %d", idx, len(segments))

        # Upload segments in chunks of 10
        for chunk_start in range(0, len(segments), 10):
            segment_chunk = segments[chunk_start:chunk_start + 10]
            frame_files_payload = {
                str(i): segment
                for i, segment in enumerate(segment_chunk, start=chunk_start)
            }

            payload = {
                "datasetId": dataset_id,
                "datasetItemId": dataset_item_id,
                "frameFiles": frame_files_payload,
            }

            logging.debug("Payload for uploading segments: %s", payload)
            logging.info("Uploading frame segments chunk for datasetItemId %s: %s",
                         dataset_item_id, list(frame_files_payload.keys()))

            resp = rpc.post(
                f"/v2/dataset/add_frame_segments?projectId={project_id}",
                payload=payload,
            )

            if not resp or not resp.get("success"):
                logging.warning("Failed to upload frame segments for chunk starting at segment %d", chunk_start)
            else:
                logging.info("Successfully uploaded segments %d–%d for datasetItemId %s",
                             chunk_start, chunk_start + len(segment_chunk) - 1, dataset_item_id)

    return batch


def batch_create_video_imagenet_dataset_items(
    batch,
    dataset_id,
    dataset_version,
    project_id,
    rpc,
    input_type=None,
):
    logging.debug(
        "creating batch_create_video_dataset_items with input_type %s",
        input_type,
    )
    get_relative_path_fn = (
        get_davis_relative_path
        if input_type in ["davis", "mscoco_video"]
        else get_youtube_bb_relative_path
    )
    if not batch:
        logging.warning("Empty batch, nothing to process.")
        return batch
    logging.debug("batch to create dataset items: %s", batch)
    video_files = []
    for video in batch:
        video_dict = {}
        path = get_relative_path_fn(video["local_file_path"])
        if path is None:
            path = video["cloud_file_path"]
            video_dict = {
                "fileLocation": f"{path}",
                "filename": video["file_name"],
            }
        else:
            video_dict = {
                "fileLocation": f"{dataset_id}/{path}",
                "filename": video["file_name"],
            }
        video_files.append(video_dict)
    payload = {
        "datasetId": dataset_id,
        "partitionNumber": batch[0]["partition_num"],
        "version": dataset_version,
        "videoFiles": video_files,
    }
    logging.info(
        "Payload for create dataset items: %s",
        payload,
    )
    resp = rpc.post(
        f"/v2/dataset/add_video_dataset_items?projectId={project_id}",
        payload=payload,
    )
    logging.info(
        "Response from create dataset items: %s",
        resp,
    )
    return batch


def batch_create_video_imagenet_items(
    batch,
    dataset_id,
    dataset_version,
    project_id,
    rpc,
    input_type=None,
):
    logging.debug(
        "creating batch_create_video_dataset_items with input_type %s",
        input_type,
    )
    get_relative_path_fn = (
        get_davis_relative_path if input_type == "davis" else get_youtube_bb_relative_path
    )
    if not batch:
        logging.warning("Empty batch, nothing to process.")
        return batch
    logging.debug("batch to create dataset items: %s", batch)
    frame_files = []
    for video in batch:
        video_dict = {}
        for frame in video:
            path = get_relative_path_fn(frame["local_file_path"])
            if path is None:
                path = frame["cloud_file_path"]
            video_dict[frame["frame_number"]] = {
                "fileLocation": f"{dataset_id}/{path}",
                "filename": frame["file_name"],
            }
        frame_files.append(video_dict)
    payload = {
        "datasetId": dataset_id,
        "partitionNumber": batch[0][0]["partition_num"],
        "version": dataset_version,
        "frameFiles": frame_files,
    }
    logging.info(
        "Payload for create dataset items: %s",
        payload,
    )
    resp = rpc.post(
        f"/v2/dataset/add_video_dataset_items?projectId={project_id}",
        payload=payload,
    )
    logging.info(
        "Response from create dataset items: %s",
        resp,
    )
    return batch


def get_client_annotations_processing_pipeline(
    annotations_partition,
    dataset_id,
    dataset_version,
    base_dataset_path,
    rpc,
    compress_annotations=False,
    max_attempts=5,
    batch_size=16,
    bucket_alias="",
    account_number="",
    project_id=None,
):
    logging.info("Setting up annotations pipeline")
    stage_1_queue = Queue()
    stage_2_queue = Queue()
    annotations_client_pipeline = Pipeline()
    if compress_annotations:
        annotations_partition["files"] = [
            compress_annotation_files(
                annotations_partition["files"],
                base_dataset_path,
            )
        ]
    batches = get_partition_batches(
        annotations_partition,
        batch_size,
        dataset_id,
        dataset_version,
        base_dataset_path,
        include_version_in_cloud_path=True,
    )
    for batch in batches:
        stage_1_queue.put(batch)
    update_annotation_bucket_url(
        rpc,
        dataset_id,
        batches[0][0]["partition_num"],
        annotation_bucket_url=os.path.commonpath(
            ["/".join(item["cloud_file_path"].split("/")[:-1]) for item in batches[0]]
        ).replace(os.sep, "/"),
    )  

    annotations_client_pipeline.add_stage(
        stage_name="fetching_presigned_urls",
        process_fn=add_batch_presigned_upload_urls,
        pull_queue=stage_1_queue,
        push_queue=stage_2_queue,
        process_params={
            "rpc": rpc,
            "partition_type": ANNOTATION_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
            "project_id": project_id,
        },
        num_threads=10,
    )
    annotations_client_pipeline.add_stage(
        stage_name="uploading_files",
        pull_queue=stage_2_queue,
        process_fn=upload_batch_files,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )
    return annotations_client_pipeline


def get_client_images_processing_pipeline(
    images_partitions,
    dataset_id,
    dataset_version,
    base_dataset_path,
    rpc,
    max_attempts=5,
    batch_size=16,
    bucket_alias="",
    account_number="",
    project_id=None,
):
    logging.info("Setting up images pipeline")
    logging.debug(
        "images_partitions: %s, dataset_id: %s, dataset_version: %s, base_dataset_path: %s",
        images_partitions,
        dataset_id,
        dataset_version,
        base_dataset_path,
    )
    stage_1_queue = Queue()
    stage_2_queue = Queue()
    stage_3_queue = Queue()
    for partition in images_partitions:
        for batch in get_partition_batches(
            partition,
            batch_size,
            dataset_id,
            dataset_version,
            base_dataset_path,
        ):
            stage_1_queue.put(batch)
    images_client_pipeline = Pipeline()
    images_client_pipeline.add_stage(
        stage_name="fetching_presigned_urls",
        pull_queue=stage_1_queue,
        push_queue=stage_2_queue,
        process_fn=add_batch_presigned_upload_urls,
        process_params={
            "rpc": rpc,
            "partition_type": SAMPLES_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
            "project_id":project_id,
        },
        num_threads=10,
    )
    images_client_pipeline.add_stage(
        stage_name="uploading_files",
        pull_queue=stage_2_queue,
        push_queue=stage_3_queue,
        process_fn=upload_batch_files,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )
    images_client_pipeline.add_stage(
        stage_name="inserting_dataset_items",
        pull_queue=stage_3_queue,
        process_fn=batch_create_dataset_items,
        process_params={
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "rpc": rpc,
        },
        num_threads=10,
    )
    return images_client_pipeline


def get_client_video_processing_pipeline(
    images_partitions,
    dataset_id,
    dataset_version,
    base_dataset_path,
    rpc,
    project_id,
    max_attempts=5,
    batch_size=16,
    bucket_alias="",
    account_number="",
    input_type="youtube_bb",
    num_dataset_items=0,
):
    logging.info("Setting up images pipeline")
    logging.debug(
        "images_partitions: %s, dataset_id: %s, dataset_version: %s, base_dataset_path: %s",
        images_partitions,
        dataset_id,
        dataset_version,
        base_dataset_path,
    )
    num_partitions = len(images_partitions)
    stage_1_queue = Queue()
    stage_2_queue = Queue()
    stage_3_queue = Queue()

    # Track which partition numbers we've already initialized
    initialized_partitions = set()

    for partition in images_partitions:
        partition_num = partition["partitionNum"]
        num_dataset_items = len(partition["files"])
        logging.debug(
            "num_dataset_items: %s, partition_num: %s",
            num_dataset_items,
            partition_num,
        )
        # Only create blank dataset items if this partition hasn't been processed
        if input_type in ["youtube_bb", "mot", "davis", "mscoco_video"]:
            if partition_num not in initialized_partitions:
                dataset_item_ids=create_video_blank_dataset_items(
                    partition_num,
                    rpc,
                    dataset_id,
                    dataset_version,
                    num_dataset_items,
                    project_id,
                )
                initialized_partitions.add(partition_num)

        if input_type == "youtube_bb":
            batches=get_video_youtube_bb_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
        elif input_type == "mot":
            batches= get_video_mot_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
        elif input_type == "davis":
            batches= get_video_davis_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
                
        elif input_type == "video_imagenet":
            batches=get_video_imagenet_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
               
        elif input_type == "kinetics":
            batches=get_video_kinetics_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
        elif input_type == "mscoco_video":
            batches= get_video_mscoco_partition_batches(
                partition,
                batch_size,
                dataset_id,
                dataset_version,
                base_dataset_path,
            )
        
        video_index = 0
        for batch in batches:
            if input_type in ["youtube_bb", "mot", "davis", "mscoco_video"]:
                for video in batch:
                    dataset_item_id = dataset_item_ids[video_index]
                    for frame in video:
                        frame["dataset_item_id"] = dataset_item_id
                    video_index += 1
            stage_1_queue.put(batch)


                
    images_client_pipeline = Pipeline()
    add_video_batch_presigned_upload_urls_fn = (
        add_video_imagenet_presigned_upload_urls
        if input_type
        in [
            "video_imagenet",
            "kinetics"
        ]
        else add_video_batch_presigned_upload_urls
    )
    upload_video_batch_files_fn = (
        upload_video_imagenet_batch_files
        if input_type
        in [
            "video_imagenet",
            "kinetics"
        ]
        else upload_video_batch_files
    )
    images_client_pipeline.add_stage(
        stage_name="fetching_presigned_urls",
        pull_queue=stage_1_queue,
        push_queue=stage_2_queue,
        process_fn=add_video_batch_presigned_upload_urls_fn,
        process_params={
            "rpc": rpc,
            "partition_type": SAMPLES_PARTITION_TYPE,
            "bucket_alias": bucket_alias,
            "account_number": account_number,
        },
        num_threads=10,
    )
    images_client_pipeline.add_stage(
        stage_name="uploading_files",
        pull_queue=stage_2_queue,
        push_queue=stage_3_queue,
        process_fn=upload_video_batch_files_fn,
        process_params={"max_attempts": max_attempts},
        num_threads=10,
    )
    if input_type == "youtube_bb":
        insert_dataset_items_process_fn = batch_create_video_youtube_bb_dataset_items
        
    elif input_type in [
        "video_imagenet",
        "kinetics"
    ]:
        insert_dataset_items_process_fn = batch_create_video_imagenet_dataset_items
    else:
        insert_dataset_items_process_fn = batch_create_video_dataset_items
    process_params = {
        "dataset_id": dataset_id,
        "dataset_version": dataset_version,
        "rpc": rpc,
        "project_id": project_id,
        "input_type": input_type,
    }
    if input_type in ["youtube_bb", "davis", "mscoco_video"]:
        process_params["num_dataset_items"] = num_dataset_items
        process_params["dataset_item_ids"] = dataset_item_ids
    images_client_pipeline.add_stage(
        stage_name="inserting_dataset_items",
        pull_queue=stage_3_queue,
        process_fn=insert_dataset_items_process_fn,
        process_params=process_params,
        num_threads=10,
    )
    return images_client_pipeline


def get_client_processing_pipelines(
    rpc,
    dataset_id,
    dataset_version,
    images_partition_status: list,
    annotation_partition_status: list,
    dataset_path: str,
    is_annotations_compressed: bool,
    destination_bucket_alias: str,
    account_number: str,
    project_id=None,
):
    annotation_pipeline, images_pipeline = (
        None,
        None,
    )
    if annotation_partition_status:
        logging.info("Setting up client annotations pipeline")
        annotation_pipeline = get_client_annotations_processing_pipeline(
            annotations_partition=annotation_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            compress_annotations=is_annotations_compressed,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
            project_id=project_id,
        )
    if images_partition_status:
        logging.info("Setting up client images pipeline")
        images_pipeline = get_client_images_processing_pipeline(
            images_partitions=images_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
            project_id=project_id,
        )
    return annotation_pipeline, images_pipeline


def get_client_video_processing_pipelines(
    project_id,
    rpc,
    dataset_id,
    dataset_version,
    images_partition_status: list,
    annotation_partition_status: list,
    dataset_path: str,
    is_annotations_compressed: bool,
    destination_bucket_alias: str,
    account_number: str,
    input_type: str = "youtube_bb",
    num_dataset_items: int = 0,
):
    logging.debug(
        "get_client_video_processing_pipelines with input_type %s",
        input_type,
    )
    annotation_pipeline, images_pipeline = (
        None,
        None,
    )
    if annotation_partition_status:
        annotation_pipeline = get_client_annotations_processing_pipeline(
            annotations_partition=annotation_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            compress_annotations=is_annotations_compressed,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
            project_id=project_id,
        )
    if images_partition_status:
        images_pipeline = get_client_video_processing_pipeline(
            images_partitions=images_partition_status,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            base_dataset_path=dataset_path,
            rpc=rpc,
            project_id=project_id,
            bucket_alias=destination_bucket_alias,
            account_number=account_number,
            input_type=input_type,
            num_dataset_items=num_dataset_items,
        )
    return annotation_pipeline, images_pipeline


def handle_partition_stats(
    rpc,
    dataset_id,
    source_dataset_version,
    target_dataset_version,
    dataset_path,
    skip_annotation_pipeline,
):
    partition_stats = []
    (
        annotation_partition_status,
        images_partition_status,
    ) = get_partition_status(
        base_path=dataset_path,
        skip_annotation_partition=skip_annotation_pipeline,
    )
    logging.debug("Debug - annotation_partition_status: %s", annotation_partition_status)
    logging.debug("Debug - images_partition_status: %s", images_partition_status)
    if annotation_partition_status:
        partition_stats.append(annotation_partition_status)
    if images_partition_status:
        partition_stats.extend(images_partition_status)
    partition_stats = update_partitions_numbers(rpc, dataset_id, partition_stats)
    create_partition_stats(
        rpc,
        partition_stats,
        dataset_id,
        target_dataset_version,
        source_dataset_version,
    )
    return (
        annotation_partition_status,
        images_partition_status,
    )


def handle_video_partition_stats(
    rpc,
    dataset_id,
    source_dataset_version,
    target_dataset_version,
    dataset_path,
    skip_annotation_pipeline,
    input_type="youtube_bb",
):
    partition_stats = []
    rename_annotation_files = False
    if input_type == "youtube_bb":
        get_partitions_fn = get_youtube_bb_partitions
    elif input_type == "mot":
        get_partitions_fn = get_mot_partitions
        rename_annotation_files = True
    elif input_type == "davis":
        #restructure_davis_dataset(dataset_path)
        get_partitions_fn = get_davis_partitions
        rename_annotation_files = True
    elif input_type == "video_imagenet":
        get_partitions_fn = get_video_imagenet_partitions
    elif input_type == "kinetics":
        get_partitions_fn = get_kinetics_partitions
    elif input_type == "mscoco_video":
        ann_paths, im_paths = scan_dataset(dataset_path)
        paths = ann_paths + im_paths
        extract_frames_from_videos(paths)
        get_partitions_fn = get_video_mscoco_partitions
    (
        annotation_partition_status,
        images_partition_status,
        unique_videos
    ) = get_video_partition_status(
        base_path=dataset_path,
        skip_annotation_partition=skip_annotation_pipeline,
        get_partitions=get_partitions_fn,
        rename_annotation_files=rename_annotation_files,
        input_type=input_type.lower(),
    )
    if annotation_partition_status:
        partition_stats.append(annotation_partition_status)
    if images_partition_status:
        partition_stats.extend(images_partition_status)
    partition_stats = update_partitions_numbers(rpc, dataset_id, partition_stats)
    create_partition_stats(
        rpc,
        partition_stats,
        dataset_id,
        target_dataset_version,
        source_dataset_version,
    )
    return (
        annotation_partition_status,
        images_partition_status,
        unique_videos
    )


def start_client_processing_pipelines(
    rpc,
    dataset_id,
    dataset_version,
    images_partition_status,
    annotation_partition_status,
    dataset_path,
    is_annotations_compressed,
    destination_bucket_alias,
    account_number,
    project_id=None,
):
    annotation_pipeline, images_pipeline = get_client_processing_pipelines(
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
        project_id=project_id,
    )
    if annotation_pipeline:
        logging.info("Starting annotation pipeline")
        annotation_pipeline.start()
        logging.info("Waiting for annotation pipeline to complete")
        annotation_pipeline.wait_to_finish_processing_and_stop()
    if images_pipeline:
        logging.info("Starting images pipeline")
        images_pipeline.start()
        logging.info("Waiting for images pipeline to complete")
        images_pipeline.wait_to_finish_processing_and_stop()


def start_client_video_processing_pipelines(
    project_id,
    rpc,
    dataset_id,
    dataset_version,
    images_partition_status,
    annotation_partition_status,
    dataset_path,
    is_annotations_compressed,
    destination_bucket_alias,
    account_number,
    input_type,
    num_dataset_items,
):
    annotation_pipeline, images_pipeline = get_client_video_processing_pipelines(
        project_id=project_id,
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
        input_type=input_type.lower(),
        num_dataset_items=num_dataset_items,
    )
    if annotation_pipeline:
        logging.info("Starting annotation pipeline")
        annotation_pipeline.start()
        logging.info("Waiting for annotation pipeline to complete")
        annotation_pipeline.wait_to_finish_processing_and_stop()
    if images_pipeline:
        logging.info("Starting images pipeline")
        images_pipeline.start()
        logging.info("Waiting for images pipeline to complete")
        images_pipeline.wait_to_finish_processing_and_stop()


def handle_client_processing_pipelines(
    rpc,
    dataset_id,
    source_dataset_version,
    target_dataset_version,
    input_type,
    source_URL="",
    dataset_path="",
    destination_bucket_alias="",
    account_number="",
    skip_partition_status=False,
    annotation_partition_status=None,
    images_partition_status=None,
    project_id=None,
):
    is_annotations_compressed = input_type in [
        "pascalvoc",
        "pascal_voc",
        "yolo",
    ]
    skip_annotation_pipeline = (
        input_type in ["imagenet", "unlabeled"]
        or input_type == "labelbox"
        and not source_URL
        or input_type == "labelbox_classification"
        and not source_URL
    )
    logging.debug("Debug - skip_partition_status: %s", skip_partition_status)
    if not skip_partition_status:
        (
            annotation_partition_status,
            images_partition_status,
        ) = handle_partition_stats(
            rpc=rpc,
            dataset_id=dataset_id,
            source_dataset_version=source_dataset_version,
            target_dataset_version=target_dataset_version,
            dataset_path=dataset_path,
            skip_annotation_pipeline=skip_annotation_pipeline,
        )
    logging.info("Starting client processing pipelines for %s dataset", input_type)
    start_client_processing_pipelines(
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=target_dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
        project_id=project_id,
    )


def handle_client_video_processing_pipelines(
    project_id,
    rpc,
    dataset_id,
    source_dataset_version,
    target_dataset_version,
    input_type,
    source_URL="",
    dataset_path="",
    destination_bucket_alias="",
    account_number="",
    skip_partition_status=False,
    annotation_partition_status=None,
    images_partition_status=None,
    unique_videos=0,
):
    is_annotations_compressed = input_type in [
        "davis",
        "mot",
    ]
    skip_annotation_pipeline = (
        input_type
        in [
            "imagenet",
            "unlabeled",
            "video_imagenet",
        ]
        or input_type == "labelbox"
        and not source_URL
        or input_type == "labelbox_classification"
        and not source_URL
    )
    if not skip_partition_status:
        (
            annotation_partition_status,
            images_partition_status,
            unique_videos,
        ) = handle_video_partition_stats(
            rpc=rpc,
            dataset_id=dataset_id,
            source_dataset_version=source_dataset_version,
            target_dataset_version=target_dataset_version,
            dataset_path=dataset_path,
            skip_annotation_pipeline=skip_annotation_pipeline,
            input_type=input_type.lower(),
        )
    start_client_video_processing_pipelines(
        project_id=project_id,
        rpc=rpc,
        dataset_id=dataset_id,
        dataset_version=target_dataset_version,
        images_partition_status=images_partition_status,
        annotation_partition_status=annotation_partition_status,
        dataset_path=dataset_path,
        is_annotations_compressed=is_annotations_compressed,
        destination_bucket_alias=destination_bucket_alias,
        account_number=account_number,
        input_type=input_type.lower(),
        num_dataset_items=unique_videos
    )
