# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .experiment import Experiment

__all__ = ["ExperimentRetrieveResponse"]


class ExperimentRetrieveResponse(BaseModel):
    experiment: Experiment
