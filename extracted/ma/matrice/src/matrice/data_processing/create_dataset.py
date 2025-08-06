from matrice.dataset import (
    get_dataset_size_in_mb_from_url,
)
from matrice.data_processing.client import (
    handle_client_processing_pipelines,
    handle_client_video_processing_pipelines,
    get_partition_status,
    get_video_partition_status,
)
from matrice.data_processing.client_utils import (
    get_size_mb,
    upload_compressed_dataset,
    is_file_compressed,
    complete_dataset_items_upload,
    get_youtube_bb_partitions,
    get_mot_partitions,
    get_davis_partitions,
    get_video_imagenet_partitions,
    get_kinetics_partitions,
    get_video_mscoco_partitions,
    extract_frames_from_videos,
    scan_dataset,
)
from matrice.dataset import Dataset
import logging


def create_dataset(
    session,
    project_id,
    account_number,
    dataset_name,
    project_type='detection',
    dataset_type="detection",
    input_type="MSCOCO",
    dataset_path="",
    source_url="",
    url_type="",
    bucket_alias="",
    compute_alias="",
    target_cloud_storage="",
    source_credential_alias="",
    bucket_alias_service_provider="auto",
):
    """
    Create a new dataset.

    Parameters
    ----------
    session : Session
        The session object used for API interactions.
    project_id : str
        The ID of the project.
    account_number : str
        The account number associated with the session.
    project_type : str
        The type of project.
    dataset_name : str
        The name of the dataset.
    dataset_type : str, optional
        The type of dataset (default is "detection")
    input_type : str, optional
        The input type for the dataset (default is "MSCOCO")
    dataset_path : str, optional
        Local path to dataset files (default is "")
    source_url : str, optional
        URL to dataset source (default is "")
    url_type : str, optional
        Type of URL source (default is "")
    bucket_alias : str, optional
        Alias for cloud storage bucket (default is "")
    compute_alias : str, optional
        Alias for compute resources (default is "")
    target_cloud_storage : str, optional
        Target cloud storage location (default is "")
    source_credential_alias : str, optional
        Alias for source credentials (default is "")
    bucket_alias_service_provider : str, optional
        Service provider for bucket alias (default is "auto")

    Returns
    -------
    Dataset
        A Dataset object for the created dataset.

    Example
    -------
    >>> dataset = project._create_dataset(
    ...     dataset_name="MyDataset",
    ...     dataset_path="/path/to/data",
    ...     dataset_type="detection"
    ... )
    >>> print(f"Dataset created: {dataset}")
    """
    logging.info("Creating dataset: %s", dataset_name)
    if not (source_url or dataset_path):
        raise ValueError("Either source_url or dataset_path must be provided")
    dataset_version = "v1.0"
    source_type = "lu" if dataset_path else "url" if source_url else None
    dataset_size = get_size_mb(dataset_path) if source_type == "lu" else 0.0
    partition_stats = []
    is_dataset_compressed = is_file_compressed(dataset_path) if dataset_path else False
    rename_annotation_files = False
    if source_type == "lu":
        logging.info("Processing local dataset upload")
        if not is_dataset_compressed:
            skip_annotation_pipeline = (
                input_type
                in [
                    "imagenet",
                    "unlabeled",
                    "video_imagenet",
                ]
                or "labelbox" in input_type
            )
            if dataset_type.lower() in [
                "video_detection",
                "frames",
                "video",
            ]:
                logging.info("Processing video detection dataset")
                if input_type.lower() == "youtube_bb":
                    get_partitions_fn = get_youtube_bb_partitions
                elif input_type.lower() == "mot":
                    get_partitions_fn = get_mot_partitions
                    rename_annotation_files = True
                elif input_type.lower() == "davis":
                    rename_annotation_files = True
                    # restructure_davis_dataset(dataset_path)
                    get_partitions_fn = get_davis_partitions
                elif input_type.lower() == "video_imagenet":
                    get_partitions_fn = get_video_imagenet_partitions
                elif input_type.lower() == "kinetics":
                    get_partitions_fn = get_kinetics_partitions
                elif input_type.lower() == "mscoco_video":
                    ann_paths, im_paths = scan_dataset(dataset_path)
                    paths = ann_paths + im_paths
                    extract_frames_from_videos(paths)
                    get_partitions_fn = get_video_mscoco_partitions
                logging.debug(
                    "calling get_video_partition_status with input_type: %s",
                    input_type,
                )
                (annotation_partition, images_partitions, unique_videos) = (
                    get_video_partition_status(
                        dataset_path,
                        skip_annotation_pipeline,
                        get_partitions_fn,
                        rename_annotation_files=rename_annotation_files,
                        input_type=input_type.lower(),
                    )
                )
                partition_stats = (
                    [*images_partitions]
                    if annotation_partition is None
                    else [
                        annotation_partition,
                        *images_partitions,
                    ]
                )
                logging.debug(
                    "partition stats: %s",
                    partition_stats,
                )
            else:
                logging.info("Processing image dataset")
                (
                    annotation_partition,
                    images_partitions,
                ) = get_partition_status(
                    dataset_path,
                    skip_annotation_pipeline,
                )
                partition_stats = (
                    [*images_partitions]
                    if annotation_partition is None
                    else [
                        annotation_partition,
                        *images_partitions,
                    ]
                )
                logging.debug(
                    "partition stats: %s",
                    partition_stats,
                )
        else:
            logging.info("Processing compressed dataset")
            source_url = upload_compressed_dataset(
                session.rpc, dataset_path, project_id=project_id
            )
    elif source_type == "url":
        try:
            dataset_size, err, msg = get_dataset_size_in_mb_from_url(
                session,
                source_url,
                project_id,
            )
            if err:
                dataset_size = 0
                logging.warning(
                    "Could not get dataset size: %s",
                    msg,
                )
        except Exception as e:
            logging.error(
                "Error getting dataset size: %s",
                e,
            )
            dataset_size = 0
    create_dataset_request = {
        "name": dataset_name,
        "datasetDescription": "",
        "_idProject": project_id,
        "_idUser": "",
        "accountNumber": account_number,
        "type": project_type,
        "isUnlabeled": (True if input_type == "unlabeled" else False),
        "isCreateNew": True,
        "datasetType": dataset_type,
        "source": source_type,
        "isCompressedFileProvided": is_dataset_compressed,
        "sourceUrl": source_url,
        "urlType": url_type,
        "inputType": input_type,
        "datasetSize": dataset_size,
        "newDatasetVersion": dataset_version,
        "partitionsInfo": {
            "totalSizeMB": dataset_size,
            "partitionStats": [
                {
                    "partitionNum": p["partitionNum"],
                    "sampleCount": p["sampleCount"],
                    "diskSizeMB": p["diskSizeMB"],
                    "type": p["type"],
                }
                for p in partition_stats
            ],
        },
        "computeAlias": compute_alias,
        "targetCloudStorage": target_cloud_storage,
        "bucketAlias": bucket_alias,
        "bucketAliasServiceProvider": bucket_alias_service_provider,
        "sourceCredentialAlias": source_credential_alias,
    }
    path = f"/v2/dataset/create/new?projectId={project_id}"
    headers = {"Content-Type": "application/json"}
    logging.debug(
        "Create dataset request: %s",
        create_dataset_request,
    )
    if input_type in ["youtube_bb", "mot", "davis", "mscoco_video"]:
        create_dataset_request["segmentLength"] = 16
    resp = session.rpc.post(
        path=path,
        headers=headers,
        payload=create_dataset_request,
    )
    logging.debug("Create dataset response: %s", resp)
    if not resp["success"]:
        error_msg = resp.get("message", "Unknown error")
        logging.error(
            "Dataset creation failed: %s",
            error_msg,
        )
        raise Exception(f"Dataset creation failed: {error_msg}")
    dataset_id = resp["data"]["_id"]
    logging.info(
        "Dataset created successfully with ID: %s",
        dataset_id,
    )
    if source_type == "lu" and not is_dataset_compressed:
        if dataset_type.lower() in [
            "video_detection",
            "frames",
            "video",
        ]:
            logging.debug(
                "handle_client_video_processing_pipelines with input type: %s",
                input_type,
            )
            handle_client_video_processing_pipelines(
                project_id=project_id,
                rpc=session.rpc,
                dataset_id=dataset_id,
                source_dataset_version="",
                target_dataset_version=dataset_version,
                input_type=input_type,
                source_URL=source_url,
                dataset_path=dataset_path,
                destination_bucket_alias=bucket_alias,
                account_number=account_number,
                skip_partition_status=True,
                annotation_partition_status=annotation_partition,
                images_partition_status=images_partitions,
                unique_videos=unique_videos,
            )
        else:
            handle_client_processing_pipelines(
                rpc=session.rpc,
                dataset_id=dataset_id,
                source_dataset_version="",
                target_dataset_version=dataset_version,
                input_type=input_type,
                source_URL=source_url,
                dataset_path=dataset_path,
                destination_bucket_alias=bucket_alias,
                account_number=account_number,
                skip_partition_status=True,
                annotation_partition_status=annotation_partition,
                images_partition_status=images_partitions,
                project_id=project_id,
            )
        complete_dataset_items_upload(
            rpc=session.rpc,
            dataset_id=dataset_id,
            partition_stats=partition_stats,
        )
        logging.info("Dataset items uploaded successfully")
    return Dataset(session, dataset_id=dataset_id)
