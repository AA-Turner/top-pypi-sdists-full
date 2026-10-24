"""
Type annotations for sagemakertrainingsessionruntime service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemakertrainingsessionruntime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_sagemakertrainingsessionruntime.type_defs import AdamParamsConfigTypeDef

    data: AdamParamsConfigTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import IO, Any, Union

from aiobotocore.response import StreamingBody

from .literals import LossFnNameType, RequestStatusType, StopReasonType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AdamParamsConfigTypeDef",
    "BlobTypeDef",
    "ComputeLogprobsConfigTypeDef",
    "ComputeLogprobsResultTypeDef",
    "DatumTypeDef",
    "EncodedTextChunkTypeDef",
    "ExecuteSamplingOperationInputTypeDef",
    "ExecuteSamplingOperationOutputTypeDef",
    "ExecuteTrainingOperationInputTypeDef",
    "ExecuteTrainingOperationOutputTypeDef",
    "ForwardBackwardConfigTypeDef",
    "ForwardBackwardResultTypeDef",
    "ForwardConfigTypeDef",
    "ForwardResultTypeDef",
    "GetSamplingOperationResultInputTypeDef",
    "GetSamplingOperationResultOutputTypeDef",
    "GetTrainingOperationResultInputTypeDef",
    "GetTrainingOperationResultOutputTypeDef",
    "LoadStateConfigTypeDef",
    "LoadWeightsForSamplingConfigTypeDef",
    "ModelInputTypeDef",
    "OperationConfigTypeDef",
    "OperationResultTypeDef",
    "OptimizerStepConfigTypeDef",
    "OptimizerStepResultTypeDef",
    "ResponseMetadataTypeDef",
    "SampleConfigTypeDef",
    "SampleOperationConfigTypeDef",
    "SampleOperationResultTypeDef",
    "SampleResponseTypeDef",
    "SampleTokenUsageTypeDef",
    "SampleTrainingSessionInputTypeDef",
    "SampleTrainingSessionOutputTypeDef",
    "SampleTrainingSessionWithResponseStreamInputTypeDef",
    "SampleTrainingSessionWithResponseStreamOutputTypeDef",
    "SampledSequenceTypeDef",
    "SamplingParamsTypeDef",
    "SaveStateConfigTypeDef",
    "SaveStateResultTypeDef",
    "SaveWeightsConfigTypeDef",
    "SaveWeightsResultTypeDef",
    "TensorDataOutputTypeDef",
    "TensorDataTypeDef",
    "TensorDataUnionTypeDef",
    "TokenLogprobTypeDef",
    "TrainingTokenUsageTypeDef",
)


class AdamParamsConfigTypeDef(TypedDict):
    learningRate: float
    beta1: NotRequired[float]
    beta2: NotRequired[float]
    eps: NotRequired[float]
    weightDecay: NotRequired[float]
    gradClipNorm: NotRequired[float]
    loraPlusLrRatio: NotRequired[float]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ComputeLogprobsResultTypeDef(TypedDict):
    logprobs: list[float]


EncodedTextChunkTypeDef = TypedDict(
    "EncodedTextChunkTypeDef",
    {
        "tokens": Sequence[int],
        "type": Literal["encoded_text"],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TensorDataOutputTypeDef(TypedDict):
    data: dict[str, Any]
    dtype: str
    shape: NotRequired[list[int]]


class TrainingTokenUsageTypeDef(TypedDict):
    trainingTokens: NotRequired[int]


class GetSamplingOperationResultInputTypeDef(TypedDict):
    trainingSessionName: str
    operationId: str


class GetTrainingOperationResultInputTypeDef(TypedDict):
    trainingSessionName: str
    operationId: str


class LoadStateConfigTypeDef(TypedDict):
    modelPackageArn: str
    loadOptimizer: bool


class LoadWeightsForSamplingConfigTypeDef(TypedDict):
    modelPackageArn: str


class SaveStateConfigTypeDef(TypedDict):
    description: NotRequired[str]


class SaveWeightsConfigTypeDef(TypedDict):
    mergeWeights: NotRequired[bool]
    description: NotRequired[str]


class OptimizerStepResultTypeDef(TypedDict):
    metrics: NotRequired[dict[str, float]]


class SaveStateResultTypeDef(TypedDict):
    modelPackageArn: str


class SaveWeightsResultTypeDef(TypedDict):
    modelPackageArn: NotRequired[str]


class SamplingParamsTypeDef(TypedDict):
    maxTokens: int
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]
    seed: NotRequired[int]
    stop: NotRequired[Sequence[str]]


class TokenLogprobTypeDef(TypedDict):
    tokenId: int
    logprob: float


class SampleTokenUsageTypeDef(TypedDict):
    prefill: int
    decode: int


class TensorDataTypeDef(TypedDict):
    data: Mapping[str, Any]
    dtype: str
    shape: NotRequired[Sequence[int]]


class OptimizerStepConfigTypeDef(TypedDict):
    adamParamsConfig: AdamParamsConfigTypeDef


class SampleTrainingSessionInputTypeDef(TypedDict):
    trainingSessionName: str
    contentType: NotRequired[str]
    accept: NotRequired[str]
    modelPackageArn: NotRequired[str]
    body: NotRequired[BlobTypeDef]


class SampleTrainingSessionWithResponseStreamInputTypeDef(TypedDict):
    trainingSessionName: str
    contentType: NotRequired[str]
    accept: NotRequired[str]
    modelPackageArn: NotRequired[str]
    body: NotRequired[BlobTypeDef]


class ModelInputTypeDef(TypedDict):
    chunks: Sequence[EncodedTextChunkTypeDef]


class ExecuteSamplingOperationOutputTypeDef(TypedDict):
    operationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ExecuteTrainingOperationOutputTypeDef(TypedDict):
    operationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SampleTrainingSessionOutputTypeDef(TypedDict):
    contentType: str
    body: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class SampleTrainingSessionWithResponseStreamOutputTypeDef(TypedDict):
    contentType: str
    body: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ForwardBackwardResultTypeDef(TypedDict):
    lossFnOutputType: NotRequired[str]
    lossFnOutputs: NotRequired[list[dict[str, TensorDataOutputTypeDef]]]
    metrics: NotRequired[dict[str, float]]
    tokenUsage: NotRequired[TrainingTokenUsageTypeDef]


class ForwardResultTypeDef(TypedDict):
    lossFnOutputType: NotRequired[str]
    lossFnOutputs: NotRequired[list[dict[str, TensorDataOutputTypeDef]]]
    metrics: NotRequired[dict[str, float]]
    tokenUsage: NotRequired[TrainingTokenUsageTypeDef]


class SampledSequenceTypeDef(TypedDict):
    stopReason: StopReasonType
    tokens: list[int]
    logprobs: NotRequired[list[float]]
    tokenUsage: NotRequired[SampleTokenUsageTypeDef]


TensorDataUnionTypeDef = Union[TensorDataTypeDef, TensorDataOutputTypeDef]


class ComputeLogprobsConfigTypeDef(TypedDict):
    prompt: ModelInputTypeDef
    modelPackageArn: NotRequired[str]


class SampleConfigTypeDef(TypedDict):
    prompt: ModelInputTypeDef
    numSamples: int
    samplingParams: SamplingParamsTypeDef
    includePromptLogprobs: NotRequired[bool]
    topkPromptLogprobs: NotRequired[int]
    modelPackageArn: NotRequired[str]


class OperationResultTypeDef(TypedDict):
    forward: NotRequired[ForwardResultTypeDef]
    forwardBackward: NotRequired[ForwardBackwardResultTypeDef]
    optimizerStep: NotRequired[OptimizerStepResultTypeDef]
    saveWeights: NotRequired[SaveWeightsResultTypeDef]
    saveState: NotRequired[SaveStateResultTypeDef]
    loadState: NotRequired[dict[str, Any]]


class SampleResponseTypeDef(TypedDict):
    sequences: list[SampledSequenceTypeDef]
    promptLogprobs: NotRequired[list[float]]
    topkPromptLogprobs: NotRequired[list[list[TokenLogprobTypeDef]]]


class DatumTypeDef(TypedDict):
    modelInput: ModelInputTypeDef
    lossFnInputs: NotRequired[Mapping[str, TensorDataUnionTypeDef]]


class SampleOperationConfigTypeDef(TypedDict):
    sample: NotRequired[SampleConfigTypeDef]
    computeLogprobs: NotRequired[ComputeLogprobsConfigTypeDef]
    loadWeightsForSampling: NotRequired[LoadWeightsForSamplingConfigTypeDef]


class GetTrainingOperationResultOutputTypeDef(TypedDict):
    status: RequestStatusType
    operationResult: OperationResultTypeDef
    errorDetails: str
    tokenUsage: TrainingTokenUsageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SampleOperationResultTypeDef(TypedDict):
    sample: NotRequired[SampleResponseTypeDef]
    computeLogprobs: NotRequired[ComputeLogprobsResultTypeDef]
    loadWeightsForSampling: NotRequired[dict[str, Any]]


class ForwardBackwardConfigTypeDef(TypedDict):
    lossFnName: LossFnNameType
    datumList: Sequence[DatumTypeDef]
    lossFnConfig: NotRequired[Mapping[str, Any]]


class ForwardConfigTypeDef(TypedDict):
    lossFnName: LossFnNameType
    datumList: Sequence[DatumTypeDef]
    lossFnConfig: NotRequired[Mapping[str, Any]]


class ExecuteSamplingOperationInputTypeDef(TypedDict):
    trainingSessionName: str
    operationConfig: SampleOperationConfigTypeDef


class GetSamplingOperationResultOutputTypeDef(TypedDict):
    status: RequestStatusType
    operationResult: SampleOperationResultTypeDef
    errorDetails: str
    ResponseMetadata: ResponseMetadataTypeDef


class OperationConfigTypeDef(TypedDict):
    forward: NotRequired[ForwardConfigTypeDef]
    forwardBackward: NotRequired[ForwardBackwardConfigTypeDef]
    optimizerStep: NotRequired[OptimizerStepConfigTypeDef]
    saveWeights: NotRequired[SaveWeightsConfigTypeDef]
    saveState: NotRequired[SaveStateConfigTypeDef]
    loadState: NotRequired[LoadStateConfigTypeDef]


class ExecuteTrainingOperationInputTypeDef(TypedDict):
    trainingSessionName: str
    sequenceNumber: int
    operationConfig: OperationConfigTypeDef
    clientToken: NotRequired[str]
