"""Module providing data_processor functionality."""

import logging
from matrice.data_processing.pipeline import (
    Pipeline,
)
from matrice.data_processing.server import (
    get_mscoco_server_processing_pipeline,
    get_imagenet_server_processing_pipeline,
    get_pascalvoc_server_processing_pipeline,
    get_labelbox_server_processing_pipeline,
    get_yolo_server_processing_pipeline,
    get_unlabelled_server_processing_pipeline,
    get_labelbox_classification_server_processing_pipeline,
    handle_source_url_dataset_download,
    download_labelbox_dataset,
    get_video_youtube_bb_tracking_server_processing_pipeline,
    get_video_mot_tracking_server_processing_pipeline,
    get_video_davis_segmentation_server_processing_pipeline,
    get_video_imagenet_classification_server_processing_pipeline,
    get_kinetics_server_processing_pipeline,
    get_video_mscoco_server_processing_pipeline,
)
from matrice.data_processing.client import (
    handle_client_processing_pipelines,
    handle_client_video_processing_pipelines,
)
from matrice.data_processing.server_utils import (
    get_number_of_dataset_batches,
)


class DataProcessor:
    """Class for processing data through various pipelines."""

    def __init__(self, session, action_record_id):
        """Initialize DataProcessor with session and action record ID."""
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        url = f"/v1/project/action/{self.action_record_id}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_type = self.action_doc["action"]
        self.project_id = self.action_doc["_idProject"]
        logging.info("Action doc: %s", self.action_doc)
        self.action_details = self.action_doc["actionDetails"]
        logging.info(
            "Action details: %s",
            self.action_details,
        )
        self.job_params = self.action_doc["jobParams"]
        logging.info("Job params: %s", self.job_params)
        self.account_number = self.action_doc.get("account_number", "")
        logging.info(
            "Account number: %s",
            self.account_number,
        )
        self.update_status(
            "DCKR_ACK",
            "ACK",
            "Action is acknowledged by data processing microservice",
        )
        self.dataset_id = self.job_params["dataset_id"]
        self.source = self.job_params["source"]
        self.source_url = self.job_params["source_URL"]
        self.input_type = self.job_params["input_type"].lower()
        self.source_version = self.job_params["source_version"]
        self.target_version = self.job_params["target_version"]
        self.destination_bucket_alias = self.job_params.get("destination_bucket_alias", "")
        self.source_bucket_alias = self.job_params.get("source_bucket_alias", "")
        self.processing_pipelines = {
            "mscoco": get_mscoco_server_processing_pipeline,
            "imagenet": get_imagenet_server_processing_pipeline,
            "pascalvoc": get_pascalvoc_server_processing_pipeline,
            "labelbox": get_labelbox_server_processing_pipeline,
            "labelbox_classification": get_labelbox_classification_server_processing_pipeline,
            "yolo": get_yolo_server_processing_pipeline,
            "unlabeled": get_unlabelled_server_processing_pipeline,
        }
        self.video_processing_pipelines = {
            "youtube_bb": get_video_youtube_bb_tracking_server_processing_pipeline,
            "mot": get_video_mot_tracking_server_processing_pipeline,
            "davis": get_video_davis_segmentation_server_processing_pipeline,
            "video_imagenet": get_video_imagenet_classification_server_processing_pipeline,
            "kinetics": get_kinetics_server_processing_pipeline,
            "mscoco_video": get_video_mscoco_server_processing_pipeline,
        }
        logging.info(
            "Processing pipelines: %s", 
            self.processing_pipelines.keys(),
        )

    def update_status(
        self,
        step_code,
        status,
        status_description,
        sample_count=None,
    ):
        """Update the status of the data processing job."""
        try:
            logging.info(status_description)
            url = "/v1/project/action"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": step_code,
                "status": status,
                "statusDescription": status_description,
            }
            if sample_count:
                self.job_params["sample_count"] = sample_count
                payload["jobParams"] = self.job_params
            self.rpc.put(path=url, payload=payload)
        except Exception as exc:
            logging.error(
                "Exception in update_status: %s",
                str(exc),
            )

    def get_server_processing_pipeline(
        self,
    ) -> Pipeline:
        """Get the appropriate server processing pipeline based on input type."""
        if self.input_type in self.processing_pipelines:
            logging.info(
                "Processing %s dataset",
                self.input_type,
            )
            server_processing_pipeline = self.processing_pipelines[self.input_type](
                self.rpc,
                self.dataset_id,
                self.target_version,
                self.action_record_id,
                self.destination_bucket_alias,
                self.account_number,
                self.project_id,
            )
        elif self.input_type in self.video_processing_pipelines:
            logging.info(
                "Processing %s dataset",
                self.input_type,
            )
            if self.input_type in ["youtube_bb", "mot", "davis", "mscoco_video"]:
                server_processing_pipeline = self.video_processing_pipelines[self.input_type](
                    self.rpc,
                    self.dataset_id,
                    self.target_version,
                    self.action_record_id,
                    self.destination_bucket_alias,
                    self.account_number,
                    self.project_id
                )
            else:
                server_processing_pipeline = self.video_processing_pipelines[self.input_type](
                    self.rpc,
                    self.dataset_id,
                    self.target_version,
                    self.action_record_id,
                    self.destination_bucket_alias,
                    self.account_number,
                    self.project_id
                )
        else:
            error_msg = f"Unsupported input type: {self.input_type}. Only mscoco, imagenet, pascalvoc and labelbox are supported for now."
            logging.error(error_msg)
            raise ValueError(error_msg)
        return server_processing_pipeline

    def start_processing(self):
        """Start the data processing pipeline."""
        if "labelbox" in self.input_type:
            dataset_path = download_labelbox_dataset(
                self.dataset_id,
                self.rpc,
                self.target_version,
                self.source_url,
            )
        elif self.source_url:
            logging.info("Downloading dataset from source to start client processing")
            dataset_path = handle_source_url_dataset_download(self.source_url)
        else:
            dataset_path = ""
        
        logging.info("Dataset path: %s", dataset_path)
        logging.debug("Debug - input_type: '%s'", self.input_type)
        logging.debug("Debug - input_type in processing_pipelines: %s", self.input_type in self.processing_pipelines)
        logging.debug("Debug - input_type in video_processing_pipelines: %s", self.input_type in self.video_processing_pipelines)
        logging.debug("Debug - dataset_path truthy: %s", bool(dataset_path))
        logging.debug("Debug - processing_pipelines keys: %s", list(self.processing_pipelines.keys()))
        
        # Client processing should happen when we have a source_URL and extracted dataset        
        if self.input_type in self.processing_pipelines and dataset_path:
            logging.info("Handling client processing pipelines for %s dataset", self.input_type)
            handle_client_processing_pipelines(
                rpc = self.rpc,
                dataset_id = self.dataset_id,
                source_dataset_version = self.source_version,
                target_dataset_version = self.target_version,
                input_type = self.input_type,
                source_URL = self.source_url,
                dataset_path = dataset_path,
                destination_bucket_alias = self.destination_bucket_alias,
                account_number = self.account_number,
                skip_partition_status = False,
                annotation_partition_status = None,
                images_partition_status = None,
                project_id = self.project_id,
            )
        elif self.input_type in self.video_processing_pipelines and dataset_path:
            logging.info("Handling client video processing pipelines for %s dataset", self.input_type)
            handle_client_video_processing_pipelines(
                self.project_id,
                self.rpc,
                self.dataset_id,
                self.source_version,
                self.target_version,
                self.input_type,
                self.source_url,
                dataset_path,
                self.destination_bucket_alias,
                self.account_number,
            )
        self.update_status(
            "DCKR_PROC",
            "OK",
            "Dataset processing started",
            sample_count=get_number_of_dataset_batches(
                self.rpc,
                self.dataset_id,
                self.target_version,
            ),
        )
        self.server_processing_pipeline = self.get_server_processing_pipeline()
        logging.info("Starting server processing pipeline")
        self.server_processing_pipeline.start()
        logging.info("Waiting for server processing pipeline to complete")
        self.server_processing_pipeline.wait_to_finish_processing_and_stop()
        self.update_status(
            "SUCCESS",
            "SUCCESS",
            "Dataset processed successfully",
        )
