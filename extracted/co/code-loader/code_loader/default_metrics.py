# mypy: ignore-errors

from enum import Enum
from typing import List, Tuple
import numpy as np

from code_loader.contract.datasetclasses import ConfusionMatrixElement  # type: ignore
from code_loader.contract.enums import ConfusionMatrixValue, MetricDirection  # type: ignore


class Metric(Enum):
    MeanSquaredError = 'MeanSquaredError'
    MeanSquaredLogarithmicError = 'MeanSquaredLogarithmicError'
    MeanAbsoluteError = 'MeanAbsoluteError'
    MeanAbsolutePercentageError = 'MeanAbsolutePercentageError'
    Accuracy = 'Accuracy'
    ConfusionMatrixClassification = 'ConfusionMatrixClassification'
    CategoricalCrossentropy = 'CategoricalCrossentropy'
    BinaryCrossentropy = 'BinaryCrossentropy'


def binary_crossentropy(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    epsilon = 1e-07
    prediction = np.clip(prediction, epsilon, 1.0 - epsilon)
    return -(ground_truth * np.log(prediction) + (1 - ground_truth) *
             np.log(1 - prediction)).sum(axis=1).astype(np.float32)


def categorical_crossentropy(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    prediction = prediction / np.sum(prediction, axis=1)
    epsilon = 1e-07
    prediction = np.clip(prediction, epsilon, 1.0 - epsilon)
    return -(ground_truth * np.log(prediction)).sum(axis=1).astype(np.float32)

def accuracy_reduced(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    return np.mean((np.round(prediction).astype(np.bool_) == ground_truth.astype(np.bool_)), axis=1)


def mean_squared_error_dimension_reduced(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    return ((ground_truth - prediction) ** 2).mean(axis=1).astype(np.float32)


def mean_absolute_error_dimension_reduced(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    return np.abs(ground_truth - prediction).mean(axis=1).astype(np.float32)


def mean_absolute_percentage_error_dimension_reduced(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    return (np.abs(ground_truth - prediction) / np.abs(ground_truth)).mean(axis=1).astype(np.float32)


def mean_squared_logarithmic_error_dimension_reduced(ground_truth: np.array, prediction: np.array) -> np.array:
    ground_truth, prediction = flatten_non_batch_dims(ground_truth, prediction)
    return np.mean((np.log(1 + ground_truth) - np.log(1 + prediction)) ** 2, axis=1).astype(np.float32)


def flatten_non_batch_dims(ground_truth: np.array, prediction: np.array) -> Tuple[np.array, np.array]:
    batch_size = ground_truth.shape[0]
    ground_truth = np.reshape(ground_truth, (batch_size, -1))
    prediction = np.reshape(prediction, (batch_size, -1))
    return ground_truth, prediction


def confusion_matrix_classification_metric(ground_truth, prediction) -> List[List[ConfusionMatrixElement]]:
    num_labels = prediction.shape[-1]
    labels = [str(i) for i in range(num_labels)]
    if len(labels) == 1:
        labels = ['0', '1']
        ground_truth = np.concatenate([1 - ground_truth, ground_truth], axis=1)
        prediction = np.concatenate([1 - prediction, prediction], axis=1)

    ret = []
    for batch_i in range(ground_truth.shape[0]):
        one_hot_vec = list(ground_truth[batch_i])
        pred_vec = list(prediction[batch_i])
        confusion_matrix_elements = []
        for i, label in enumerate(labels):
            expected_outcome = ConfusionMatrixValue.Positive if int(
                one_hot_vec[i]) == 1 else ConfusionMatrixValue.Negative
            cm_element = ConfusionMatrixElement(label, expected_outcome, float(pred_vec[i]))
            confusion_matrix_elements.append(cm_element)
        ret.append(confusion_matrix_elements)
    return ret


metrics_names_to_functions_and_direction = {
    Metric.MeanSquaredError.name: (mean_squared_error_dimension_reduced, MetricDirection.Downward),
    Metric.MeanSquaredLogarithmicError.name: (
        mean_squared_logarithmic_error_dimension_reduced, MetricDirection.Downward),
    Metric.MeanAbsoluteError.name: (mean_absolute_error_dimension_reduced, MetricDirection.Downward),
    Metric.MeanAbsolutePercentageError.name: (
        mean_absolute_percentage_error_dimension_reduced, MetricDirection.Downward),
    Metric.Accuracy.name: (accuracy_reduced, MetricDirection.Upward),
    Metric.ConfusionMatrixClassification.name: (confusion_matrix_classification_metric, None),
    Metric.CategoricalCrossentropy.name: (categorical_crossentropy, MetricDirection.Downward),
    Metric.BinaryCrossentropy.name: (binary_crossentropy, MetricDirection.Downward)
}
