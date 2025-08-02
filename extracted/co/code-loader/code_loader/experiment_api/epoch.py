from typing import List, Optional
from code_loader.experiment_api.experiment_context import ExperimentContext
from code_loader.experiment_api.types import Metrics
from code_loader.experiment_api.utils import to_api_metric_value, upload_file
from code_loader.experiment_api.api import LogExternalEpochDataRequest, GetUploadModelSignedUrlRequest, TagModelRequest


class Epoch:
    """
    Represents an epoch in an experiment.

    Attributes:
        experiment (ExperimentContext): The context of the experiment.
        epoch (int): The epoch number.
        metrics (Metrics): The metrics associated with the epoch.
        default_tag (str): The default tag for the epoch.
        ctx (ExperimentContext): The context of the experiment.
    """

    def __init__(self, ctx: ExperimentContext, epoch: int, default_tag: str = 'latest'):
        """
        Initializes the Epoch instance.

        Args:
            ctx (ExperimentContext): The context of the experiment.
            epoch (int): The epoch number.
            default_tag (str): The default tag for the epoch. Defaults to 'latest', set to '' for no default tag.
        """
        self.experiment = ExperimentContext
        self.epoch = epoch
        self.metrics: Metrics = {}
        self.default_tag = default_tag
        self.ctx = ctx

    def add_metric(self, name: str, value: float) -> None:
        """
        Adds a metric to the epoch.

        Args:
            name (str): The name of the metric.
            value (float): The value of the metric.
        """
        self.metrics[name] = value

    def set_metrics(self, metrics: Metrics) -> None:
        """
        Sets the metrics for the epoch.

        Args:
            metrics (Metrics): The metrics to set for the epoch.
        """
        self.metrics = metrics

    def _upload_model(self, modelFilePath: str) -> None:
        """
        Uploads the model file for the epoch.

        Args:
            modelFilePath (str): The path to the model file.

        Raises:
            Exception: If the model file extension is not allowed.
        """
        allowed_extensions = ["h5", "onnx"]
        modelExtension = modelFilePath.split(".")[-1]
        if modelExtension not in allowed_extensions:
            raise Exception(f"Model file extension not allowed. Allowed extensions are {allowed_extensions}")
        url = self.ctx.api.get_uploaded_model_signed_url(GetUploadModelSignedUrlRequest(
            epoch=self.epoch,
            experimentId=self.ctx.experiment_id,
            versionId=self.ctx.version_id,
            projectId=self.ctx.project_id,
            fileType=modelExtension
        ))
        print(f"Uploading epoch({self.epoch}) model file")
        upload_file(url.url, modelFilePath)
        print("Model file uploaded")
    
    def _tag_model(self, tags: List[str]) -> None:
        """
        Tags the model file for the epoch.

        Args:
            tags (List[str]): The tags to associate with the model file.
        """
        print(f"Tagging epoch({self.epoch}) model")
        self.ctx.api.tag_model(TagModelRequest(
            experimentId=self.ctx.experiment_id,
            projectId=self.ctx.project_id,
            epoch=self.epoch,
            tags=tags
        ))

    def log(self, modelFilePath: Optional[str] = None, tags: Optional[List[str]] = None, override: bool = False) -> None:
        """
        Logs the epoch with optional model file and tags.

        Args:
            modelFilePath (Optional[str]): The path to the model file. Defaults to None.
            tags (Optional[List[str]]): A list of tags to associate with the epoch model. Will always include the default tag. Unless the default tag is set to '', all previous epoch model with the same tag will be removed
            override (bool): Whether to override the existing epoch model. Defaults to False.
        """
        if tags is None:
            tags = []

        if modelFilePath is not None:
            self._upload_model(modelFilePath)
        
        if len(self.default_tag) > 0 and self.default_tag not in tags:
            tags.append(self.default_tag)

        if len(tags) == 0 and modelFilePath is not None:
            raise Exception("No tags provided for the epoch model. Either provide tags or use default_tag")

        print(f"Add metrics for epoch({self.epoch}) model")
        api_metrics = {
            key: to_api_metric_value(value) for key, value in self.metrics.items()
        }
        self.ctx.api.log_external_epoch_data(LogExternalEpochDataRequest(
            experimentId=self.ctx.experiment_id,
            projectId=self.ctx.project_id,
            epoch=self.epoch,
            metrics=api_metrics,
            override=override
        ))
        if modelFilePath is not None and len(tags) > 0:
            self._tag_model(tags)