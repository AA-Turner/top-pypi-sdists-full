"""Module providing testing functionality."""

import json
import math
import os
import shutil
import tarfile
import zipfile
from io import BytesIO
from typing import List
import requests
import yaml
from PIL import Image, ImageDraw
from pycocotools.coco import COCO
from pydantic import BaseModel
from matrice.session import Session


class SplitMetricStruct(BaseModel):
    """This is a private class used internally to store split metrics.

    Attributes
    ----------
    splitType : str
        Type of the dataset split (e.g., 'train', 'val', 'test').
    metricName : str
        Name of the evaluation metric (e.g., 'accuracy', 'precision').
    metricValue : float
        Value of the metric for the given split.
    """

    """This is a private class used internally."""
    splitType: str
    metricName: str
    metricValue: float


class dotdict(dict):
    """A dictionary subclass that provides dot notation access to attributes.

    Attributes
    ----------
    __getattr__ : function
        Allows accessing dictionary keys as object attributes.
    __setattr__ : function
        Allows setting dictionary keys as object attributes.
    __delattr__ : function
        Allows deleting dictionary keys as object attributes.
    """

    """This is a private class used internally."""
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TestingActionTracker:
    """Handles logging, dataset preparation, and configuration management for model testing actions.

    Parameters
    ----------
    model_family_info_path : str
        Path to the model family information file.
    model_info_path : str
        Path to the model information file.
    config_path : str
        Path to the action configuration file.
    """

    """This is a private class used internally."""

    def __init__(
        self,
        model_family_info_path,
        model_info_path,
        config_path,
    ):
        """Initializes the TestingActionTracker class, loading model family info, model info,
        and configurations.

        Parameters
        ----------
        model_family_info_path : str
            Path to the model family information JSON file.
        model_info_path : str
            Path to the model information JSON file.
        config_path : str
            Path to the action configuration file.
        """
        self.logs = []
        self.testing_logs_folder_path = "./testing_logs"
        os.makedirs(
            self.testing_logs_folder_path,
            exist_ok=True,
        )
        self.model_family_info_path = model_family_info_path
        self.model_info_path = model_info_path
        self.config_path = config_path
        session = Session()
        self.rpc = session.rpc
        self.load_model_family_info()
        self.load_model_info()
        self.load_action_config()
        self.action_doc = self.mock_action_doc()
        self.action_details = self.action_doc["actionDetails"]
        self.checkpoint_path, self.pretrained = self.get_checkpoint_path()
        self.prepare_dataset()

    def get_main_action_logs_path(self):
        """Determines the appropriate log file path based on the action type (train, export, eval).

        Returns
        -------
        str
            Path to the main log file for the current action.
        """
        if "train" in self.config_path:
            return os.path.join(
                self.testing_logs_folder_path,
                "train.json",
            )
        elif "export" in self.config_path:
            return os.path.join(
                self.testing_logs_folder_path,
                os.path.basename(self.config_path).replace("-config", ""),
            )
        elif "eval" in self.config_path:
            return os.path.join(
                self.testing_logs_folder_path,
                "eval.json",
            )

    def log_to_json(self, file_path, payload):
        """Logs data to a JSON file, appending the payload if the file exists.

        Parameters
        ----------
        file_path : str
            Path to the JSON log file.
        payload : dict
            The data to log in the JSON file.
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.append(payload)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_logs(self, step, status, description):
        """Adds a log entry for a specific step, including status and description.

        Parameters
        ----------
        step : str
            The step or action being logged (e.g., 'load_model').
        status : str
            The status of the step (e.g., 'SUCCESS', 'ERROR').
        description : str
            A description or error message related to the step.
        """
        self.logs.append(
            {
                "step": step,
                "status": status,
                "description": description,
            }
        )
        self.log_to_json(
            self.get_main_action_logs_path(),
            {
                "step": step,
                "status": status,
                "description": description,
            },
        )

    def log_decorator(func):

        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.add_logs(
                    func.__name__,
                    "SUCCESS",
                    "SUCCESS",
                )
                return result
            except Exception as e:
                print(f"ERROR occurred in: {func.__name__} : {str(e)}")
                self.add_logs(func.__name__, "ERROR", str(e))
                raise e

        return wrapper

    @log_decorator
    def load_model_family_info(self):
        """Loads model family information from the specified file.

        Returns
        -------
        dict
            The loaded model family information.
        """
        with open(self.model_family_info_path) as f:
            self.model_family_info = json.load(f)
        self.input_type = self.model_family_info["modelInputs"].lower()
        self.output_type = self.model_family_info["modelOutputs"].lower()
        self.models_family_name = self.model_family_info["modelFamily"]

    @log_decorator
    def load_model_info(self):
        """Loads model information from the specified file.

        Returns
        -------
        dict
            The loaded model information.
        """
        with open(self.model_info_path) as f:
            self.model_info = json.load(f)
        self.model_key = self.model_info["modelKey"]
        self.model_name = self.model_info["modelName"]

    @log_decorator
    def mock_action_doc(self):
        """Creates a mock action document with dataset and model details.

        Returns
        -------
        dict
            A mock document containing action and model information.
        """
        api_url = (
            f"/v1/system/get_dataset_url?inputType={self.input_type}&outputType={self.output_type}"
        )
        response = self.rpc.get(
            path=api_url,
            params={
                "inputType": self.input_type,
                "outputType": self.output_type,
            },
        )
        if response and "data" in response:
            mock_dataset = response["data"]
        else:
            raise ValueError("Invalid response from the API call")
        action_details = {
            "_idModel": "mocked_model_id",
            "runtimeFramework": "Pytorch",
            "datasetVersion": "v1.0",
            "dataset_url": mock_dataset,
            "project_type": self.output_type,
            "input_type": self.input_type,
            "output_type": self.output_type,
        }
        self._idModel = action_details["_idModel"]
        return {
            "actionDetails": action_details,
            "action": self.action_type,
            "serviceName": "mocked_service_name",
            "_idProject": "mocked_project_id",
        }

    @log_decorator
    def get_checkpoint_path(self):
        """Finds and returns the path to the latest model checkpoint.

        Returns
        -------
        tuple
            Path to the checkpoint file and a boolean indicating whether it exists.
        """
        checkpoint_dir = "./checkpoints"
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
            print(f"Created checkpoint directory: {checkpoint_dir}")
            return None, False
        checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith(".pt")]
        if not checkpoint_files:
            print("No checkpoint files found in the checkpoints directory.")
            return None, False
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_files[0])
        print(f"Found checkpoint: {checkpoint_path}")
        return checkpoint_path, True

    @log_decorator
    def load_action_config(self):
        """Loads action configuration based on the config path (train, export, eval).

        Raises
        ------
        Exception
            If the config path is not valid or cannot be loaded.
        """
        self.model_config = {}
        if "train" in self.config_path and self.config_path.endswith("-config.json"):
            self.action_type = "model_train"
            with open(self.config_path, "r") as config_file:
                self.config_file = json.load(config_file)
            print(f"Loaded train config for model {self.model_name}: {self.config_file}")
            for config in self.config_file.get("actionConfig", []):
                key_name = config.get("keyName")
                default_value = config.get("defaultValue")
                if key_name and default_value is not None:
                    self.model_config[key_name] = self.cast_value(
                        config.get("valueType"),
                        default_value,
                    )
            print(f"Model config: {self.model_config}")
        elif "export" in self.config_path and self.config_path.endswith("-config.json"):
            self.action_type = "model_export"
            with open(self.config_path, "r") as config_file:
                self.config_file = json.load(config_file)
            self.action_details["exportFormats"] = [self.config_file["exportFormat"]]
            for config in self.config_file.get("actionConfig", []):
                key_name = config.get("keyName")
                default_value = config.get("defaultValue")
                if key_name and default_value is not None:
                    self.model_config[key_name] = self.cast_value(
                        config.get("valueType"),
                        default_value,
                    )
            print(f"Model config: {self.model_config}")
            print(f"Loaded export config for format {self.action_details['exportFormats']}")
        elif "eval" in self.config_path:
            self.action_type = "model_eval"
            self.model_config["split_types"] = [
                "vel",
                "test",
            ]
            print(f"Model config: {self.model_config}")
        else:
            raise Exception(
                "Couldn't load action config, Make sure config path is one of [train-config.json, export-export_format-config, eval]"
            )

    def cast_value(self, value_type, value):
        """Casts a value to its specified type (int, float, string, bool).

        Parameters
        ----------
        value_type : str
            The type to cast the value to (e.g., 'int32', 'float32').
        value : any
            The value to be cast.

        Returns
        -------
        any
            The casted value.
        """
        if value_type == "int32":
            return int(value)
        elif value_type == "float32":
            return float(value)
        elif value_type == "string":
            return str(value)
        elif value_type == "bool":
            return bool(value)
        else:
            return value

    def update_status(self, stepCode, status, status_description):
        """Mocks the status update for a given step, adding it to logs.

        Parameters
        ----------
        stepCode : str
            The code for the current step.
        status : str
            The current status (e.g., 'SUCCESS', 'ERROR').
        status_description : str
            Description or details about the step status.
        """
        print(f"Mock update status: {stepCode}, {status}, {status_description}")
        self.add_logs(stepCode, status, status_description)

    @log_decorator
    def upload_checkpoint(
        self,
        checkpoint_path,
        model_type="trained",
    ):
        """Uploads a checkpoint to a remote location (mocked behavior).

        Parameters
        ----------
        checkpoint_path : str
            Path to the checkpoint file to be uploaded.
        model_type : str, optional
            Type of model (default is 'trained').
        """
        print(f"Mock upload checkpoint: {checkpoint_path}, {model_type}")
        file_path, ext = os.path.splitext(checkpoint_path)
        if model_type == "trained":
            new_name = os.path.join(
                self.testing_logs_folder_path,
                "model_" + model_type + ext,
            )
        elif model_type == "exported":
            new_name = os.path.join(
                self.testing_logs_folder_path,
                "model_" + self.action_details["exportFormats"][0] + model_type + ext,
            )
        shutil.move(checkpoint_path, new_name)
        return True

    @log_decorator
    def download_model(
        self,
        model_path,
        model_type="trained",
        runtime_framework="",
    ):
        """Downloads a model from a remote location (mocked behavior).

        Parameters
        ----------
        model_path : str
            Path to download the model to.
        model_type : str, optional
            Type of model (default is 'trained').
        runtime_framework : str, optional
            Framework used for the model (default is '').
        """
        print(f"Mock download model to: {model_path}, {model_type}")
        file_path, ext = os.path.splitext(model_path)
        if model_type == "trained":
            local_model_file = [
                path
                for path in os.listdir(self.testing_logs_folder_path)
                if path.endswith(f"{model_type}{ext}")
            ][0]
        elif model_type == "exported":
            local_model_file = [
                path
                for path in os.listdir(self.testing_logs_folder_path)
                if path.endswith(f"{model_type}{ext}")
            ][0]
        local_model_file = self.testing_logs_folder_path + "/" + local_model_file
        print(f"Local model file: {local_model_file}")
        with open(local_model_file, "rb") as src, open(model_path, "wb") as dest:
            dest.write(src.read())
        return True

    @log_decorator
    def get_job_params(self):
        """Generates and returns job parameters for model testing.

        Returns
        -------
        dict
            A dictionary containing dataset and model configuration parameters.
        """
        dataset_path = "dataset"
        model_config = dotdict(
            {
                "dataset_path": dataset_path,
                "data": f"workspace/{dataset_path}/images",
                "arch": self.model_key,
                "pretrained": self.pretrained,
                "model_key": self.model_key,
                "model_name": self.model_name,
                "checkpoint_path": self.checkpoint_path,
            }
        )
        self.model_config = dotdict(
            {
                **model_config,
                **{k: v for k, v in self.model_config.items() if k not in model_config},
            }
        )
        return self.model_config

    @log_decorator
    def add_index_to_category(self, indexToCat):
        """Adds an index-to-category mapping to the log files.

        Parameters
        ----------
        indexToCat : dict
            Dictionary mapping category indexes to class names.

        Returns
        -------
        dict
            The index-to-category mapping.
        """
        print(f"Mock add index to category: {indexToCat}")
        file_path = os.path.join(
            self.testing_logs_folder_path,
            "index_to_category.json",
        )
        with open(file_path, "w") as file:
            json.dump(indexToCat, file, indent=4)
        return indexToCat

    @log_decorator
    def get_index_to_category(self, is_exported=False):
        """Retrieves the index-to-category mapping from the log files.

        Parameters
        ----------
        is_exported : bool, optional
            Indicates whether the model is exported (default is False).

        Returns
        -------
        dict
            The index-to-category mapping.
        """
        file_path = os.path.join(
            self.testing_logs_folder_path,
            "index_to_category.json",
        )
        with open(file_path, "r") as file:
            return json.load(file)

    @log_decorator
    def log_epoch_results(
        self,
        epoch,
        epoch_result_list: List[SplitMetricStruct],
    ):
        """Logs the results of an epoch during model training.

        Parameters
        ----------
        epoch : int
            The current epoch number.
        epoch_result_list : List[SplitMetricStruct]
            List of metrics for the current epoch.
        """
        epoch_result_list = self.validate_metrics_structure(epoch_result_list)
        epoch_result_list = self.round_metrics(epoch_result_list)
        model_log_payload = {
            "epoch": epoch,
            "epochDetails": epoch_result_list,
        }
        file_path = os.path.join(
            self.testing_logs_folder_path,
            "epochs_results.json",
        )
        self.log_to_json(file_path, model_log_payload)

    @log_decorator
    def save_evaluation_results(
        self,
        list_of_result_dicts: List[SplitMetricStruct],
    ):
        """Saves evaluation results to the log files.

        Parameters
        ----------
        list_of_result_dicts : List[SplitMetricStruct]
            List of evaluation metrics and results.
        """
        list_of_result_dicts = self.validate_metrics_structure(list_of_result_dicts)
        print(f"Mock save evaluation results: {list_of_result_dicts}")
        file_path = os.path.join(
            self.testing_logs_folder_path,
            "evaluation_results.json",
        )
        with open(file_path, "w") as file:
            json.dump(
                list_of_result_dicts,
                file,
                indent=4,
            )

    def validate_metrics_structure(
        self,
        metrics_list: List[SplitMetricStruct],
    ):
        """Validates the structure of a list of metrics.

        Parameters
        ----------
        metrics_list : List[SplitMetricStruct]
            List of metrics to be validated.

        Returns
        -------
        List[SplitMetricStruct]
            The validated metrics.
        """
        return [SplitMetricStruct.model_validate(x).model_dump() for x in metrics_list]

    def round_metrics(self, epoch_result_list):
        """Rounds the metric values to four decimal places, replacing NaN or inf with 0.

        Parameters
        ----------
        epoch_result_list : List[dict]
            List of metrics with values to be rounded.

        Returns
        -------
        List[dict]
            List of metrics with rounded values.
        """
        for metric in epoch_result_list:
            if (
                metric["metricValue"] is None
                or math.isinf(metric["metricValue"])
                or math.isnan(metric["metricValue"])
            ):
                metric["metricValue"] = 0
            metric["metricValue"] = round(metric["metricValue"], 4)
            if metric["metricValue"] == 0:
                metric["metricValue"] = 0.0001
        return epoch_result_list

    @log_decorator
    def prepare_dataset(self):
        """Prepares the dataset for training or evaluation by downloading and formatting it."""
        dataset_images_dir = "workspace/dataset"
        if os.path.exists(dataset_images_dir):
            print(
                f"Dataset directory {dataset_images_dir} already exists. Skipping download and preparation."
            )
        else:
            dataset_url = self.action_details.get("dataset_url")
            project_type = self.action_details.get("project_type")
            input_type = self.action_details.get("input_type")
            output_type = self.action_details.get("output_type")
            print(
                f"Preparing dataset from {dataset_url} for project type {project_type} with input type {input_type} and output type {output_type}"
            )
            dataset_dir = "workspace/dataset"
            os.makedirs(dataset_dir, exist_ok=True)
            self.download_and_extract_dataset(dataset_url, dataset_dir)
            if project_type == "classification":
                self.prepare_classification_dataset(dataset_dir)
            elif project_type == "detection":
                if "yolo" in self.model_name.lower():
                    self.prepare_yolo_dataset(dataset_dir)
                else:
                    self.prepare_detection_dataset(dataset_dir)
            else:
                print(f"Unsupported project type: {project_type}")

    def download_and_extract_dataset(self, dataset_url, dataset_dir):
        """Downloads and extracts a dataset from a given URL.

        Parameters
        ----------
        dataset_url : str
            The URL from which to download the dataset.
        dataset_dir : str
            The directory where the dataset should be extracted.
        """
        file_name = os.path.basename(dataset_url)
        local_file_path = os.path.join(dataset_dir, file_name)
        try:
            with requests.get(
                dataset_url,
                stream=True,
                timeout=30,
            ) as r:
                r.raise_for_status()
                print(f"Response status code: {r.status_code}")
                print(f"Response headers: {r.headers}")
                content_type = r.headers.get("Content-Type", "Unknown")
                print(f"Content-Type: {content_type}")
                with open(local_file_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
            print(f"File downloaded successfully from {dataset_url}")
            print(f"Saved as: {local_file_path}")
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(local_file_path, "r") as zip_ref:
                    zip_ref.extractall(dataset_dir)
                print("Zip file extracted successfully")
            elif file_name.endswith(".tar.gz") or file_name.endswith(".tgz"):
                with tarfile.open(local_file_path, "r:gz") as tar:
                    tar.extractall(path=dataset_dir)
                print("Tar.gz file extracted successfully")
            else:
                print(f"Unsupported file format: {file_name}")
                return
            os.remove(local_file_path)
            print(f"Removed the compressed file: {local_file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading dataset from {dataset_url}: {e}")
        except (
            zipfile.BadZipFile,
            tarfile.TarError,
        ) as e:
            print(f"Error extracting dataset from {local_file_path}: {e}")

    def get_file_extension(self, content_type):
        """Returns the appropriate file extension based on content type.

        Parameters
        ----------
        content_type : str
            The content type of the file.

        Returns
        -------
        str
            The file extension (e.g., '.zip', '.tar').
        """
        content_type = content_type.lower()
        if "zip" in content_type:
            return ".zip"
        elif "gzip" in content_type or "x-gzip" in content_type:
            return ".gz"
        elif "tar" in content_type:
            return ".tar"
        elif "octet-stream" in content_type:
            return ""
        else:
            return ""

    def prepare_classification_dataset(self, dataset_dir):
        """Prepares a dataset for classification tasks.

        Parameters
        ----------
        dataset_dir : str
            The directory where the dataset is located.
        """
        print("Preparing classification dataset...")
        sub_dirs = [
            os.path.join(dataset_dir, d)
            for d in os.listdir(dataset_dir)
            if os.path.isdir(os.path.join(dataset_dir, d))
        ]
        if len(sub_dirs) != 1:
            raise ValueError("Expected a single subdirectory in the dataset directory")
        vehicle_dir = sub_dirs[0]
        print(f"Main Sub directory: {vehicle_dir}")
        images_dir = os.path.join(dataset_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        print(f"Images directory: {images_dir}")
        class_names = set()
        split_info = {}
        for split in ["train", "val", "test"]:
            split_dir = os.path.join(vehicle_dir, split)
            dst_split_dir = os.path.join(images_dir, split)
            os.makedirs(dst_split_dir, exist_ok=True)
            split_info[split] = {}
            for class_name in os.listdir(split_dir):
                class_dir = os.path.join(split_dir, class_name)
                if os.path.isdir(class_dir):
                    class_names.add(class_name)
                    dst_class_dir = os.path.join(dst_split_dir, class_name)
                    os.makedirs(
                        dst_class_dir,
                        exist_ok=True,
                    )
                    for img in os.listdir(class_dir):
                        src_path = os.path.join(class_dir, img)
                        dst_path = os.path.join(dst_class_dir, img)
                        shutil.copy2(src_path, dst_path)
                        if class_name not in split_info[split]:
                            split_info[split][class_name] = []
                        split_info[split][class_name].append(dst_path)
        self.num_classes = len(class_names)
        self.class_names = list(class_names)
        print(f"Number of classes: {self.num_classes}")
        print(f"Class names: {self.class_names}")
        with open(
            os.path.join(dataset_dir, "split_info.json"),
            "w",
        ) as f:
            json.dump(split_info, f, indent=4)

    def prepare_detection_dataset(self, dataset_dir):
        """Prepares a dataset for object detection tasks.

        Parameters
        ----------
        dataset_dir : str
            The directory where the dataset is located.
        """
        print("Preparing detection dataset...")
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [
            d
            for d in contents
            if os.path.isdir(os.path.join(dataset_dir, d)) and d not in ("images", "annotations")
        ]
        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return
        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")
        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")
        src_images_dir = os.path.join(downloaded_dir, "images")
        src_annotations_dir = os.path.join(downloaded_dir, "annotations")
        dst_images_dir = os.path.join(dataset_dir, "images")
        dst_annotations_dir = os.path.join(dataset_dir, "annotations")
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(
                src_annotations_dir,
                dst_annotations_dir,
            )
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")
        print("Dataset preparation completed.")

    def convert_bbox_to_yolo(self, size, box):
        """Converts bounding box coordinates to YOLO format.

        Parameters
        ----------
        size : tuple
            The width and height of the image.
        box : list
            Bounding box coordinates in the format [x, y, width, height].

        Returns
        -------
        tuple
            Converted bounding box in YOLO format.
        """
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]
        x = (box[0] + box[2] / 2.0) * dw
        y = (box[1] + box[3] / 2.0) * dh
        w = box[2] * dw
        h = box[3] * dh
        return x, y, w, h

    def create_data_yaml(self, dataset_dir, class_names):
        """Creates a data.yaml file for the YOLO model from the dataset.

        Parameters
        ----------
        dataset_dir : str
            The directory where the dataset is located.
        class_names : list
            List of class names in the dataset.
        """
        data_yaml = {
            "path": dataset_dir,
            "train": "images/train2017",
            "val": "images/val2017",
            "test": "images/test2017",
            "names": class_names,
        }
        yaml_path = os.path.join(dataset_dir, "data.yaml")
        with open(yaml_path, "w") as file:
            yaml.dump(
                data_yaml,
                file,
                default_flow_style=False,
            )
        print(f"Created data.yaml file at {yaml_path}")

    def prepare_yolo_dataset(self, dataset_dir):
        """Prepares the dataset for YOLO model training.

        Parameters
        ----------
        dataset_dir : str
            The directory where the dataset is located.
        """
        print("Preparing YOLO dataset...")
        root_dir = os.path.abspath(os.path.join(dataset_dir, os.pardir, os.pardir))
        datasets_dir = os.path.join(root_dir, "datasets")
        if not os.path.exists(datasets_dir):
            os.makedirs(datasets_dir)
        workspace_dir = os.path.basename(os.path.dirname(dataset_dir))
        new_workspace_dir = os.path.join(datasets_dir, workspace_dir)
        if not os.path.exists(new_workspace_dir):
            os.makedirs(new_workspace_dir)
        new_dataset_dir = os.path.join(
            new_workspace_dir,
            os.path.basename(dataset_dir),
        )
        if os.path.exists(new_dataset_dir):
            shutil.rmtree(new_dataset_dir)
        shutil.move(dataset_dir, new_dataset_dir)
        dataset_dir = new_dataset_dir
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [
            d
            for d in contents
            if os.path.isdir(os.path.join(dataset_dir, d)) and d not in ("images", "annotations")
        ]
        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return
        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")
        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")
        src_images_dir = os.path.join(downloaded_dir, "images")
        src_annotations_dir = os.path.join(downloaded_dir, "annotations")
        dst_images_dir = os.path.join(dataset_dir, "images")
        dst_annotations_dir = os.path.join(dataset_dir, "annotations")
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(
                src_annotations_dir,
                dst_annotations_dir,
            )
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")
        class_names = self.create_yolo_labels_from_mscoco_ann(
            dataset_dir,
            dst_images_dir,
            dst_annotations_dir,
            os.path.join(
                dst_annotations_dir,
                "instances_train2017.json",
            ),
        )
        self.create_yolo_labels_from_mscoco_ann(
            dataset_dir,
            dst_images_dir,
            dst_annotations_dir,
            os.path.join(
                dst_annotations_dir,
                "instances_val2017.json",
            ),
        )
        self.create_yolo_labels_from_mscoco_ann(
            dataset_dir,
            dst_images_dir,
            dst_annotations_dir,
            os.path.join(
                dst_annotations_dir,
                "instances_test2017.json",
            ),
        )
        self.create_data_yaml(dataset_dir, class_names)
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")
        print("Dataset preparation completed.")

    def create_yolo_labels_from_mscoco_ann(
        self,
        dataset_dir,
        dst_images_dir,
        dst_annotations_dir,
        annotation_file,
    ):
        """Creates YOLO labels from MSCOCO annotations.

        Parameters
        ----------
        dataset_dir : str
            Directory where the dataset is stored.
        dst_images_dir : str
            Directory where images are stored.
        dst_annotations_dir : str
            Directory where annotations are stored.
        annotation_file : str
            Path to the MSCOCO annotation file.

        Returns
        -------
        list
            List of class names from the annotations.
        """
        coco = COCO(annotation_file)
        ann_dir = os.path.join(dataset_dir, "labels")
        if not os.path.exists(ann_dir):
            os.makedirs(ann_dir)
        label_dirs = {
            "train": os.path.join(ann_dir, "train2017"),
            "val": os.path.join(ann_dir, "val2017"),
            "test": os.path.join(ann_dir, "test2017"),
        }
        for dir_path in label_dirs.values():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        categories = coco.loadCats(coco.getCatIds())
        class_names = [category["name"] for category in categories]
        for img_id in coco.getImgIds():
            img_info = coco.loadImgs(img_id)[0]
            img_filename = img_info["file_name"]
            img_width = img_info["width"]
            img_height = img_info["height"]
            ann_ids = coco.getAnnIds(imgIds=img_id)
            anns = coco.loadAnns(ann_ids)
            if "train" in annotation_file:
                label_path = os.path.join(
                    label_dirs["train"],
                    img_filename.replace(".jpg", ".txt"),
                )
            elif "val" in annotation_file:
                label_path = os.path.join(
                    label_dirs["val"],
                    img_filename.replace(".jpg", ".txt"),
                )
            elif "test" in annotation_file:
                label_path = os.path.join(
                    label_dirs["test"],
                    img_filename.replace(".jpg", ".txt"),
                )
            with open(label_path, "w") as f:
                for ann in anns:
                    bbox = ann["bbox"]
                    yolo_bbox = self.convert_bbox_to_yolo(
                        (
                            img_width,
                            img_height,
                        ),
                        bbox,
                    )
                    category_id = ann["category_id"] - 1
                    f.write(f"{category_id} {' '.join(map(str, yolo_bbox))}\n")
        if "train" in annotation_file:
            return class_names

    @log_decorator
    def get_model_train(self, is_exported=False):
        """Mock function to retrieve the model training document.

        This mock version simulates the retrieval of the model training document without making
            actual API calls.

        Parameters
        ----------
        is_exported : bool, optional
            If True, retrieves the model train document by export ID (default is False).

        Returns
        -------
        dict
            A mock model training document.

        Raises
        ------
        Exception
            If there is an error in fetching the model training document.
        """
        try:
            if is_exported:
                print(f"Mock fetching model train by export ID: {self._idModel_str}")
            else:
                print(f"Mock fetching model train by model ID: {self._idModel_str}")
                ("/v1/model/model_train/" + str(self._idModel_str))
            model_train_doc = {
                "model_id": self._idModel_str,
                "training_status": "completed",
                "training_accuracy": 0.95,
                "model_exported": is_exported,
            }
            print(f"Mocked model training document: {model_train_doc}")
            return model_train_doc
        except Exception as e:
            print(f"Exception in get_model_train: {str(e)}")
            self.update_status(
                "error",
                "error",
                "Failed to get mock model train",
            )
            raise e


class ModelDownloadMock:
    """Mock class for downloading models in the testing pipeline."""

    def __init__(self):
        """Initializes the ModelDownloadMock class and sets up the testing logs folder path."""
        self.testing_logs_folder_path = "./testing_logs"

    def download_model(
        self,
        model_path,
        model_type="trained",
        runtime_framework="",
    ):
        """Mock method to download a model file and copy it to the specified path.

        Parameters
        ----------
        model_path : str
            Path where the model should be downloaded.
        model_type : str, optional
            Type of model to download ('trained' or 'exported'). Default is 'trained'.
        runtime_framework : str, optional
            Runtime framework used for the model (default is '').

        Returns
        -------
        bool
            Returns True after successfully copying the model file.
        """
        print(f"Mock download model to: {model_path}, {model_type}")
        file_path, ext = os.path.splitext(model_path)
        if model_type == "trained":
            local_model_file = [
                path
                for path in os.listdir(self.testing_logs_folder_path)
                if path.endswith(f"{model_type}{ext}")
            ][0]
        elif model_type == "exported":
            local_model_file = [
                path
                for path in os.listdir(self.testing_logs_folder_path)
                if path.endswith(f"{model_type}{ext}")
            ][0]
        with open(local_model_file, "rb") as src, open(model_path, "wb") as dest:
            dest.write(src.read())
        return True


class TestingMatriceDeploy:
    """Class to handle deployment and inference of models for testing purposes.

    This class handles model downloading, logging, and running inference with a provided model.

    Parameters
    ----------
    load_model : function
        Function to load a model during testing.
    predict : function
        Function to make predictions using the loaded model.
    """

    def __init__(self, load_model, predict):
        """Initializes the TestingMatriceDeploy class, setting up logs and triggering inference.

        Parameters
        ----------
        load_model : function
            Function that loads a model for inference.
        predict : function
            Function to perform prediction with the loaded model.
        """
        self.logs = []
        self.testing_logs_folder_path = "./testing_logs"
        os.makedirs(
            self.testing_logs_folder_path,
            exist_ok=True,
        )
        self.main_action_logs_path = os.path.join(
            self.testing_logs_folder_path,
            "deploy.json",
        )
        self.model_downloader = ModelDownloadMock()
        self.load_model = lambda model_downloader: load_model(model_downloader)
        self.predict = lambda model, image: predict(model, image)
        self.model = None
        self.inference(self.create_image_bytes())

    def log_to_json(self, file_path, payload):
        """Logs data to a JSON file, appending the payload if the file exists.

        Parameters
        ----------
        file_path : str
            Path to the JSON log file.
        payload : dict
            The data to log in the JSON file.
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.append(payload)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_logs(self, step, status, description):
        """Adds a log entry for a specific step, including status and description.

        Parameters
        ----------
        step : str
            The step or action being logged (e.g., 'inference').
        status : str
            The status of the step (e.g., 'SUCCESS', 'ERROR').
        description : str
            A description or error message related to the step.
        """
        self.logs.append(
            {
                "step": step,
                "status": status,
                "description": description,
            }
        )
        self.log_to_json(
            self.main_action_logs_path,
            {
                "step": step,
                "status": status,
                "description": description,
            },
        )

    def log_decorator(func):
        """A decorator to log the execution status of a function."""

        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.add_logs(
                    func.__name__,
                    "SUCCESS",
                    "SUCCESS",
                )
                return result
            except Exception as e:
                print(f"ERROR occurred in: {func.__name__} : {str(e)}")
                self.add_logs(func.__name__, "ERROR", str(e))
                raise e

        return wrapper

    @log_decorator
    def load_predictor_model(self):
        """Loads the predictor model using the model downloader."""
        self.model = self.load_model(self.model_downloader)

    @log_decorator
    def inference(self, image):
        """Runs inference on an image using the loaded model.

        Parameters
        ----------
        image : bytes
            Image data in bytes to be used for inference.

        Returns
        -------
        tuple
            Inference results and a success flag.
        """
        if self.model is None:
            self.load_predictor_model()
        results = self.predict(self.model, image)
        return results, True

    def create_image_bytes(self):
        """Creates a simple test image in memory as a byte stream.

        Returns
        -------
        bytes
            Image data in JPEG format.
        """
        image = Image.new("RGB", (224, 224), color="blue")
        draw = ImageDraw.Draw(image)
        draw.text((50, 100), "Test", fill="white")
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format="JPEG")
        image_bytes_io.seek(0)
        return image_bytes_io.read()
