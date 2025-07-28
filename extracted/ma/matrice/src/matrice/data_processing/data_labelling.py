"""Module providing data_labelling functionality."""

from matrice.deploy.client import MatriceDeployClient
from matrice.data_processing.data_prep import (
    dataset_items_producer,
    get_item_set_type,
)
from matrice.data_processing.server import (
    batch_update_dataset_items,
)
from matrice.data_processing.server_utils import (
    generate_short_uuid,
    get_number_of_dataset_batches,
)
from matrice.data_processing.pipeline import (
    Pipeline,
)
from matrice.deployment import Deployment
from queue import Queue
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Union
from matrice.projects import Projects
import time
from PIL import Image
import os


def _create_test_image() -> None:
    """Create a simple test image for prediction"""
    try:
        image = Image.new("RGB", (200, 100), (255, 0, 0))
        image.save("simple_image.png")
        logging.debug("Created test image successfully")
    except Exception as e:
        logging.error(
            "Failed to create test image: %s",
            str(e),
        )
        raise


def test_model_prediction(
    session: Any,
    deployment_class: Any,
    max_tries: int = 5,
    initial_wait: int = 180,
    retry_wait: int = 180,
) -> Union[MatriceDeployClient, Deployment]:
    """Test model prediction with retries

    Args:
        session: Session object
        deployment_class: Model deployment object
        max_tries: Maximum number of prediction attempts
        initial_wait: Initial wait time in seconds
        retry_wait: Wait time between retries in seconds

    Returns:
        Optional[MatriceDeployClient]: Deploy client if successful, None otherwise
    """
    _create_test_image()
    logging.info(
        "Waiting %s seconds before first prediction attempt...",
        initial_wait,
    )
    time.sleep(initial_wait)
    
    for try_num in range(max_tries):
        prediction_successful = False
        
        try:
            logging.info(
                "Prediction attempt %s/%s",
                try_num + 1,
                max_tries,
            )
            
            # Try with deployment class first
            try:
                _ = deployment_class.get_prediction("simple_image.png")
                logging.info("Prediction successful with deployment class")
                prediction_successful = True
                if os.path.exists("simple_image.png"):
                    os.remove("simple_image.png")
                return deployment_class
            except Exception as e:
                logging.error(
                    "Error using deployment class: %s",
                    str(e),
                )
            
            # Try with deployment client if first attempt failed
            try:
                deployment_client = MatriceDeployClient(
                    session,
                    deployment_class.deployment_id,
                    "",
                )
                deployment_client.get_prediction(input_path="simple_image.png")
                logging.info("Prediction successful with deployment client")
                prediction_successful = True
                if os.path.exists("simple_image.png"):
                    os.remove("simple_image.png")
                return deployment_client
            except Exception as e:
                logging.error(
                    "Error using deploy client: %s",
                    str(e),
                )
            
            # If we reach here, both attempts failed for this try
            if not prediction_successful:
                if try_num == max_tries - 1:
                    logging.error(
                        "All %s prediction attempts failed",
                        max_tries,
                    )
                    if os.path.exists("simple_image.png"):
                        os.remove("simple_image.png")
                    return None
                else:
                    logging.warning(
                        "Prediction attempt %s failed, retrying...",
                        try_num + 1,
                    )
                    logging.info(
                        "Waiting %s seconds before next attempt...",
                        retry_wait,
                    )
                    time.sleep(retry_wait)
                    
        except Exception as e:
            logging.error(
                "Unexpected error in prediction attempt %s: %s",
                try_num + 1,
                str(e),
            )
            if try_num == max_tries - 1:
                if os.path.exists("simple_image.png"):
                    os.remove("simple_image.png")
                return None
            time.sleep(retry_wait)
    
    # Fallback - should not reach here
    if os.path.exists("simple_image.png"):
        os.remove("simple_image.png")
    return None


def create_model_deployment_client(
    session: Any,
    project_type: str,
    project_id: str,
    model_id: str = "",
    model_type: str = "pretrained",
    deployment_type: str = "regular",
    checkpoint_type: str = "pretrained",
    checkpoint_value: str = "",
    suggested_classes: List[str] = [],
    compute_alias: str = "",
    runtime_framework: str = "Pytorch",
    model_family: str = "",
    model_key: str = "",
) -> Union[MatriceDeployClient, Deployment]:
    """Create and test a model deployment

    Args:
        session: Session object
        project_type: Type of project
        project_id: ID of project
        model_id: ID of model
        model_type: Type of model
        deployment_type: Type of deployment
        checkpoint_type: Type of checkpoint
        checkpoint_value: Value of checkpoint
        suggested_classes: List of suggested classes
        compute_alias: Compute alias
        runtime_framework: Runtime framework
        model_family: Model family name
        model_key: Model key identifier

    Returns:
        MatriceDeployClient: Deployment client if successful

    Raises:
        Exception: If deployment fails
    """
    logging.info("Creating model deployment...")
    project = Projects(session, project_id=project_id)
    try:
        deployment, action = project._create_deployment(
            deployment_name=str(generate_short_uuid()),
            model_id=model_id,
            model_type=model_type,
            deployment_type=deployment_type,
            checkpoint_type=checkpoint_type,
            checkpoint_value=checkpoint_value,
            suggested_classes=suggested_classes,
            model_output=project_type,
            runtime_framework=runtime_framework,
            compute_alias=compute_alias,
            model_family=model_family,
            model_key=model_key,
            shutdown_threshold=15,
        )
        auth_key = deployment.create_auth_key(1)[0]["key"]
        deployment.set_auth_key(auth_key)
        logging.debug(
            "Deployment ID: %s, Action ID: %s",
            deployment.deployment_id,
            action.action_id,
        )
        deploy_client = test_model_prediction(session, deployment)
        if deploy_client:
            logging.info("Model deployment successful.")
            return deploy_client
        else:
            error_msg = "Model deployment failed"
            logging.error(error_msg)
            raise Exception(error_msg)
    except Exception as e:
        logging.error(
            "Error creating model deployment: %s",
            str(e),
        )
        raise


def convert_to_mscoco_format(
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
) -> List[float]:
    """Convert bounding box coordinates to MSCOCO format.

    Args:
        x_min: Minimum x coordinate
        y_min: Minimum y coordinate
        x_max: Maximum x coordinate
        y_max: Maximum y coordinate

    Returns:
        List[float]: [x_min, y_min, width, height]
    """
    width = x_max - x_min
    height = y_max - y_min
    return [x_min, y_min, width, height]


def add_dataset_item_annotations(
    dataset_item: Dict,
    prediction_result: Dict,
    project_type: str,
) -> Dict:
    """Add annotations to dataset item based on prediction results

    Args:
        dataset_item: Dataset item to annotate
        prediction_result: Prediction results
        project_type: Type of project (classification/detection/instance_segmentation)

    Returns:
        Dict: Annotated dataset item

    Raises:
        Exception: If annotation fails
    """
    try:
        base_annotation = {
            "id": str(generate_short_uuid()),
            "segmentation": [],
            "isCrowd": [0],
            "height": 0.0,
            "width": 0.0,
            "center": [],
            "area": 0.0,
            "masks": [],
            "confidence": 0.0,
            "bbox": [],
            "category": "Unknown",
        }
        if project_type == "classification":
            if not isinstance(prediction_result, dict):
                raise ValueError("Classification prediction_result must be a dictionary")
            dataset_item["annotations"] = [
                {
                    **base_annotation,
                    "confidence": float(prediction_result.get("confidence", 0.0)),
                    "category": str(prediction_result.get("category", "Unknown")),
                }
            ]
        elif project_type in [
            "detection",
            "instance_segmentation",
        ]:
            if not isinstance(prediction_result, (list, tuple)):
                raise ValueError(f"{project_type} prediction_result must be a list")
            dataset_item["annotations"] = []
            for prediction in prediction_result:
                if not isinstance(prediction, dict):
                    continue
                try:
                    bbox = convert_to_mscoco_format(
                        float(prediction["bounding_box"]["xmin"]),
                        float(prediction["bounding_box"]["ymin"]),
                        float(prediction["bounding_box"]["xmax"]),
                        float(prediction["bounding_box"]["ymax"]),
                    )
                    annotation = {
                        **base_annotation,
                        "confidence": float(prediction.get("confidence", 0.0)),
                        "bbox": bbox,
                        "height": bbox[3],
                        "width": bbox[2],
                        "area": bbox[2] * bbox[3],
                        "category": str(
                            prediction.get(
                                "category",
                                "Unknown",
                            )
                        ),
                    }
                    if project_type == "instance_segmentation":
                        masks = prediction.get(
                            "masks",
                            prediction.get("segmentation", []),
                        )
                        annotation.update(
                            {
                                "masks": masks,
                                "segmentation": masks,
                            }
                        )
                    dataset_item["annotations"].append(annotation)
                except (
                    KeyError,
                    TypeError,
                    ValueError,
                ) as e:
                    logging.warning(
                        "Skipping invalid prediction: %s",
                        e,
                    )
                    continue
        else:
            logging.warning(
                "Unknown project type: %s",
                project_type,
            )
        return dataset_item
    except Exception as e:
        logging.error("Error adding annotations: %s", str(e))
        raise


def label_dataset_items(
    batch_dataset_items: List[Dict],
    deploy_client: Union[MatriceDeployClient, Deployment],
    project_type: str,
    dataset_version: str,
) -> List[Dict]:
    """Label batch of dataset items using model predictions

    Args:
        batch_dataset_items: List of dataset items to label
        deploy_client: Deployment client
        project_type: Type of project
        dataset_version: Version of dataset

    Returns:
        List[Dict]: Labeled dataset items

    Raises:
        Exception: If labeling fails
    """
    try:
        logging.info(
            "Processing batch of %s items",
            len(batch_dataset_items),
        )
        with ThreadPoolExecutor(max_workers=len(batch_dataset_items)) as executor:
            futures = [
                executor.submit(
                    deploy_client.get_prediction,
                    input_url=item["fileLocation"],
                )
                for item in batch_dataset_items
            ]
            dataset_items_prediction_results = [future.result() for future in futures]
        for i, prediction_result in enumerate(dataset_items_prediction_results):
            batch_dataset_items[i] = add_dataset_item_annotations(
                batch_dataset_items[i],
                prediction_result,
                project_type,
            )
        logging.debug(
            "Successfully labeled batch: %s",
            batch_dataset_items,
        )
        logging.info("Successfully labeled batch")
        return update_dataset_items_keys(batch_dataset_items, dataset_version)
    except Exception as e:
        logging.error(
            "Error labeling dataset items: %s",
            str(e),
        )
        raise


def update_dataset_items_keys(
    dataset_items: List[Dict],
    dataset_version: str,
) -> List[Dict]:
    """Update dataset items keys

    Args:
        dataset_items: List of dataset items
        dataset_version: Version of dataset

    Returns:
        List[Dict]: Updated dataset items
    """
    for item in dataset_items:
        item["image_height"] = item["height"]
        item["image_width"] = item["width"]
        item["image_area"] = item["area"]
        item["splitType"] = get_item_set_type(item, dataset_version)
    return dataset_items


def get_dataset_labelling_pipeline(
    session: Any,
    dataset_id: str,
    dataset_version: str,
    deploy_client: MatriceDeployClient,
    project_type: str,
) -> Pipeline:
    """Create dataset labeling pipeline

    Args:
        session: Session object
        dataset_id: ID of dataset
        dataset_version: Version of dataset
        deploy_client: Deployment client for predictions
        project_type: Type of project

    Returns:
        Pipeline: Configured pipeline object

    Raises:
        Exception: If pipeline creation fails
    """
    try:
        logging.info("Creating dataset labeling pipeline...")
        rpc = session.rpc
        dataset_items_queue = Queue()
        update_dataset_items_queue = Queue()
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
            stage_name="Label Dataset Items",
            process_fn=label_dataset_items,
            pull_queue=dataset_items_queue,
            push_queue=update_dataset_items_queue,
            process_params={
                "deploy_client": deploy_client,
                "project_type": project_type,
                "dataset_version": dataset_version,
            },
        )
        pipeline.add_stage(
            stage_name="Update Dataset Items",
            process_fn=batch_update_dataset_items,
            pull_queue=update_dataset_items_queue,
            process_params={
                "rpc": rpc,
                "dataset_id": dataset_id,
                "version": dataset_version,
            },
            num_threads=10,
            is_last_stage=True,
        )
        logging.info("Pipeline created successfully")
        return pipeline
    except Exception as e:
        logging.error("Error creating pipeline: %s", str(e))
        raise


class DataLabelling:
    """Class to handle dataset labelling."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataLabelling.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record

        Raises:
            Exception: If initialization fails
        """
        try:
            self.session = session
            self.rpc = session.rpc
            self.action_record_id = action_record_id
            url = f"/v1/project/action/{self.action_record_id}/details"
            self.action_doc = self.rpc.get(url)["data"]
            self.action_type = self.action_doc["action"]
            self.project_id = self.action_doc["_idProject"]
            self.job_params = self.action_doc["jobParams"]
            self.dataset_id = self.job_params["dataset_id"]
            self.dataset_version = self.job_params["version"]
            self.project_type = self.job_params["project_type"]
            self.candidate_classes = self.job_params["labels"]
            self.checkpoint_type = self.job_params["checkpointType"]
            self.model_family = self.job_params["model_family"]
            self.model_key = self.job_params["model_key"]
            logging.info(
                "Initialized DataLabelling for action %s",
                action_record_id,
            )
        except Exception as e:
            logging.error(
                "Error initializing DataLabelling: %s",
                str(e),
            )
            raise

    def update_status(
        self,
        stepCode: str,
        status: str,
        status_description: str,
        sample_count: int = None,
    ) -> None:
        """Update status of data labelling.

        Args:
            stepCode: Code indicating current step
            status: Status of step
            status_description: Description of status

        Raises:
            Exception: If status update fails
        """
        try:
            logging.info(
                "Updating status: %s - %s - %s",
                stepCode,
                status,
                status_description,
            )
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            if sample_count:
                self.job_params["sample_count"] = sample_count
                payload["jobParams"] = self.job_params
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            logging.error(
                "Exception in update_status: %s",
                str(e),
            )

    def create_model_deployment(
        self,
    ) -> MatriceDeployClient:
        """Create model deployment

        Returns:
            MatriceDeployClient: Deployment client

        Raises:
            Exception: If deployment creation fails
        """
        try:
            logging.info("Creating model deployment...")
            self.deploy_client = create_model_deployment_client(
                session=self.session,
                project_type=self.project_type,
                project_id=self.project_id,
                checkpoint_type=self.checkpoint_type,
                suggested_classes=self.candidate_classes,
                model_family=self.model_family,
                model_key=self.model_key,
            )
            return self.deploy_client
        except Exception as e:
            logging.error(
                "Error creating model deployment: %s",
                str(e),
            )
            raise

    def mark_dataset_as_labelled(self) -> None:
        """Mark dataset as labelled

        Raises:
            Exception: If marking dataset as labelled fails
        """
        try:
            url = f"/v2/dataset/annotation/complete-labeling/{self.dataset_id}/{self.dataset_version}"
            resp = self.rpc.put(url)
            logging.info(
                "Dataset %s marked as labelled, response: %s",
                self.dataset_id,
                resp,
            )
        except Exception as e:
            logging.error(
                "Error marking dataset as labelled: %s",
                str(e),
            )
            raise

    def start_processing(self) -> None:
        """Start dataset labelling processing.

        Raises:
            Exception: If processing fails
        """
        try:
            self.update_status(
                "DCKR_PROC",
                "OK",
                "Dataset labelling started",
                sample_count=get_number_of_dataset_batches(
                    self.rpc,
                    self.dataset_id,
                    self.dataset_version,
                ),
            )
            logging.info("Starting dataset labeling pipeline...")
            self.pipeline = get_dataset_labelling_pipeline(
                session=self.session,
                dataset_id=self.dataset_id,
                dataset_version=self.dataset_version,
                deploy_client=self.deploy_client,
                project_type=self.project_type,
            )
            self.pipeline.start()
            self.pipeline.wait_to_finish_processing_and_stop()
            self.mark_dataset_as_labelled()
            self.update_status(
                "SUCCESS",
                "SUCCESS",
                "Dataset Labelling completed",
            )
            logging.info("Dataset labeling completed successfully")
        except Exception as e:
            error_msg = f"Error in start_processing: {str(e)}"
            logging.error(error_msg)
            self.update_status(
                "FAILED",
                "FAILED",
                f"Dataset labelling failed: {str(e)}",
            )
            raise
