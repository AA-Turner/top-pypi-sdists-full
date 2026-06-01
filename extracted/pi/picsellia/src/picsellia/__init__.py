__version__ = "6.32.0"

import logging.config
import os

from picsellia.client import Client
from picsellia.sdk.annotation import Annotation
from picsellia.sdk.artifact import Artifact
from picsellia.sdk.asset import Asset
from picsellia.sdk.classification import Classification
from picsellia.sdk.data import Data
from picsellia.sdk.data_projection import DataProjection
from picsellia.sdk.datalake import Datalake
from picsellia.sdk.dataset import Dataset
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.sdk.datasource import DataSource
from picsellia.sdk.deployment import Deployment
from picsellia.sdk.experiment import Experiment
from picsellia.sdk.job import Job
from picsellia.sdk.label import Label
from picsellia.sdk.line import Line
from picsellia.sdk.log import Log
from picsellia.sdk.logging_file import LoggingFile
from picsellia.sdk.model import Model
from picsellia.sdk.model_context import ModelContext
from picsellia.sdk.model_file import ModelFile
from picsellia.sdk.model_version import ModelVersion
from picsellia.sdk.point import Point
from picsellia.sdk.polygon import Polygon
from picsellia.sdk.project import Project
from picsellia.sdk.rectangle import Rectangle
from picsellia.sdk.tag import Tag
from picsellia.sdk.worker import Worker
from picsellia.services.error_manager import ErrorManager
from picsellia.types.schemas import CloudObject, CloudProjectionObject

__all__ = [
    "Client",
    "Annotation",
    "Artifact",
    "Asset",
    "Classification",
    "Data",
    "Datalake",
    "Dataset",
    "DatasetVersion",
    "DataSource",
    "DataProjection",
    "Deployment",
    "Experiment",
    "Job",
    "Label",
    "Line",
    "Log",
    "LoggingFile",
    "Model",
    "ModelContext",
    "ModelFile",
    "ModelVersion",
    "Point",
    "Polygon",
    "Project",
    "Rectangle",
    "Tag",
    "Worker",
    "ErrorManager",
    "CloudObject",
    "CloudProjectionObject",
]

logger = logging.getLogger("picsellia")
logger.addHandler(logging.NullHandler())

custom_logging = os.getenv("PICSELLIA_SDK_CUSTOM_LOGGING", False)

if not custom_logging:
    try:
        DEFAULT_LOGGING_CONFIG = {
            "version": 1,
            "formatters": {
                "standard": {"format": "%(message)s"},
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "picsellia": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    except Exception:
        print("Error while loading conf file for logging. No logging done.")
