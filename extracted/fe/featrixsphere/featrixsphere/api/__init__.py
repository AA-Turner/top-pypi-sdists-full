#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
FeatrixSphere New API

A clean, object-oriented API for interacting with FeatrixSphere.

Usage:
    from featrixsphere.api import FeatrixSphere

    featrix = FeatrixSphere("https://sphere-api.featrix.com")

    # Create foundational model
    fm = featrix.create_foundational_model(
        name="my_model",
        data_file="data.csv"
    )
    fm.wait_for_training()

    # Create a binary classifier
    predictor = fm.create_binary_classifier(
        target_column="target",
        name="my_classifier"
    )
    predictor.wait_for_training()

    # Or a multiclass classifier
    predictor = fm.create_multi_classifier(
        target_column="category",
        name="my_multiclass"
    )
    predictor.wait_for_training()

    # Make predictions
    result = predictor.predict({"feature1": "value1"})
    print(result.predicted_class)
    print(result.confidence)
"""

from .exceptions import (
    FeatrixAuthenticationError,
    FeatrixPredictionError,
    LoadFailedError,
    LoadTimeoutError,
    ModelNotLoadingError,
    TrainingStatusUnavailableError,
    SessionNotFoundError,
)
from .client import FeatrixSphere
from .foundational_model import FoundationalModel
from .predictor import Predictor
from .published_predictor import LoadStatus, PublishedPredictor
from .published_prediction_network import (
    PublishedPredictionNetwork,
    PredictionNetworkResult,
    PredictionNetworkTraceEntry,
)
from .prediction_result import PredictionResult, PredictionFeedback
from .prediction_grid import PredictionGrid
from .vector_database import VectorDatabase
from .vector_view import VectorView
from .reference_record import ReferenceRecord
from .api_endpoint import APIEndpoint
from .event_group import EventGroup
from .notebook_helper import FeatrixNotebookHelper
from .label_utils import find_similar_labels, collapse_similar_labels
from .null_distribution import compute_null_distribution

__all__ = [
    'FeatrixAuthenticationError',
    'FeatrixPredictionError',
    'LoadFailedError',
    'LoadStatus',
    'LoadTimeoutError',
    'ModelNotLoadingError',
    'TrainingStatusUnavailableError',
    'SessionNotFoundError',
    'FeatrixSphere',
    'FoundationalModel',
    'Predictor',
    'PublishedPredictor',
    'PublishedPredictionNetwork',
    'PredictionNetworkResult',
    'PredictionNetworkTraceEntry',
    'PredictionResult',
    'PredictionFeedback',
    'PredictionGrid',
    'VectorDatabase',
    'VectorView',
    'ReferenceRecord',
    'APIEndpoint',
    'EventGroup',
    'FeatrixNotebookHelper',
    'find_similar_labels',
    'collapse_similar_labels',
    'compute_null_distribution',
]
