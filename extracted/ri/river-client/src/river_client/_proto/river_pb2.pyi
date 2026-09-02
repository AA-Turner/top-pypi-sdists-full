import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AsyncResponse(_message.Message):
    __slots__ = ("request_id", "type")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    type: str
    def __init__(self, request_id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class TensorData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class ModelInputChunk(_message.Message):
    __slots__ = ("encoded_text", "image", "image_asset_pointer")
    ENCODED_TEXT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ASSET_POINTER_FIELD_NUMBER: _ClassVar[int]
    encoded_text: EncodedTextChunk
    image: ImageChunk
    image_asset_pointer: ImageAssetPointerChunk
    def __init__(self, encoded_text: _Optional[_Union[EncodedTextChunk, _Mapping]] = ..., image: _Optional[_Union[ImageChunk, _Mapping]] = ..., image_asset_pointer: _Optional[_Union[ImageAssetPointerChunk, _Mapping]] = ...) -> None: ...

class EncodedTextChunk(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, tokens: _Optional[_Iterable[int]] = ...) -> None: ...

class ImageChunk(_message.Message):
    __slots__ = ("data", "format", "expected_tokens")
    DATA_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    format: str
    expected_tokens: int
    def __init__(self, data: _Optional[bytes] = ..., format: _Optional[str] = ..., expected_tokens: _Optional[int] = ...) -> None: ...

class ImageAssetPointerChunk(_message.Message):
    __slots__ = ("location", "format", "expected_tokens")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    location: str
    format: str
    expected_tokens: int
    def __init__(self, location: _Optional[str] = ..., format: _Optional[str] = ..., expected_tokens: _Optional[int] = ...) -> None: ...

class ModelInput(_message.Message):
    __slots__ = ("chunks",)
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    chunks: _containers.RepeatedCompositeFieldContainer[ModelInputChunk]
    def __init__(self, chunks: _Optional[_Iterable[_Union[ModelInputChunk, _Mapping]]] = ...) -> None: ...

class LoraConfig(_message.Message):
    __slots__ = ("rank", "seed", "train_unembed", "train_mlp", "train_attn", "alpha")
    RANK_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    TRAIN_UNEMBED_FIELD_NUMBER: _ClassVar[int]
    TRAIN_MLP_FIELD_NUMBER: _ClassVar[int]
    TRAIN_ATTN_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    rank: int
    seed: int
    train_unembed: bool
    train_mlp: bool
    train_attn: bool
    alpha: float
    def __init__(self, rank: _Optional[int] = ..., seed: _Optional[int] = ..., train_unembed: bool = ..., train_mlp: bool = ..., train_attn: bool = ..., alpha: _Optional[float] = ...) -> None: ...

class AdamParams(_message.Message):
    __slots__ = ("learning_rate", "beta1", "beta2", "eps", "weight_decay", "grad_clip_norm")
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    BETA1_FIELD_NUMBER: _ClassVar[int]
    BETA2_FIELD_NUMBER: _ClassVar[int]
    EPS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_DECAY_FIELD_NUMBER: _ClassVar[int]
    GRAD_CLIP_NORM_FIELD_NUMBER: _ClassVar[int]
    learning_rate: float
    beta1: float
    beta2: float
    eps: float
    weight_decay: float
    grad_clip_norm: float
    def __init__(self, learning_rate: _Optional[float] = ..., beta1: _Optional[float] = ..., beta2: _Optional[float] = ..., eps: _Optional[float] = ..., weight_decay: _Optional[float] = ..., grad_clip_norm: _Optional[float] = ...) -> None: ...

class Datum(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class Checkpoint(_message.Message):
    __slots__ = ("checkpoint_id", "checkpoint_type", "time", "river_path", "size_bytes", "public", "training_run_id")
    CHECKPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    RIVER_PATH_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    checkpoint_id: str
    checkpoint_type: str
    time: _timestamp_pb2.Timestamp
    river_path: str
    size_bytes: int
    public: bool
    training_run_id: str
    def __init__(self, checkpoint_id: _Optional[str] = ..., checkpoint_type: _Optional[str] = ..., time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., river_path: _Optional[str] = ..., size_bytes: _Optional[int] = ..., public: bool = ..., training_run_id: _Optional[str] = ...) -> None: ...

class TrainingRun(_message.Message):
    __slots__ = ("training_run_id", "base_model", "model_owner", "is_lora", "corrupted", "lora_rank", "last_request_time", "last_checkpoint", "last_inference_checkpoint", "user_metadata")
    class UserMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_OWNER_FIELD_NUMBER: _ClassVar[int]
    IS_LORA_FIELD_NUMBER: _ClassVar[int]
    CORRUPTED_FIELD_NUMBER: _ClassVar[int]
    LORA_RANK_FIELD_NUMBER: _ClassVar[int]
    LAST_REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    LAST_INFERENCE_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    USER_METADATA_FIELD_NUMBER: _ClassVar[int]
    training_run_id: str
    base_model: str
    model_owner: str
    is_lora: bool
    corrupted: bool
    lora_rank: int
    last_request_time: _timestamp_pb2.Timestamp
    last_checkpoint: Checkpoint
    last_inference_checkpoint: Checkpoint
    user_metadata: _containers.ScalarMap[str, str]
    def __init__(self, training_run_id: _Optional[str] = ..., base_model: _Optional[str] = ..., model_owner: _Optional[str] = ..., is_lora: bool = ..., corrupted: bool = ..., lora_rank: _Optional[int] = ..., last_request_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_checkpoint: _Optional[_Union[Checkpoint, _Mapping]] = ..., last_inference_checkpoint: _Optional[_Union[Checkpoint, _Mapping]] = ..., user_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class GetServerCapabilitiesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SupportedModel(_message.Message):
    __slots__ = ("model_name",)
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    def __init__(self, model_name: _Optional[str] = ...) -> None: ...

class GetServerCapabilitiesResponse(_message.Message):
    __slots__ = ("supported_models",)
    SUPPORTED_MODELS_FIELD_NUMBER: _ClassVar[int]
    supported_models: _containers.RepeatedCompositeFieldContainer[SupportedModel]
    def __init__(self, supported_models: _Optional[_Iterable[_Union[SupportedModel, _Mapping]]] = ...) -> None: ...

class CreateSessionRequest(_message.Message):
    __slots__ = ("tags", "sdk_version", "user_metadata")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class UserMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    USER_METADATA_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    sdk_version: str
    user_metadata: _containers.ScalarMap[str, str]
    def __init__(self, tags: _Optional[_Mapping[str, str]] = ..., sdk_version: _Optional[str] = ..., user_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateSessionResponse(_message.Message):
    __slots__ = ("session_id", "info_message", "warning_message", "error_message")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    INFO_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WARNING_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    info_message: str
    warning_message: str
    error_message: str
    def __init__(self, session_id: _Optional[str] = ..., info_message: _Optional[str] = ..., warning_message: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class SessionHeartbeatRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class SessionHeartbeatResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CreateModelRequest(_message.Message):
    __slots__ = ("session_id", "model_seq_id", "base_model", "lora_config", "user_metadata", "training_data_attestation_id")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    LORA_CONFIG_FIELD_NUMBER: _ClassVar[int]
    USER_METADATA_FIELD_NUMBER: _ClassVar[int]
    TRAINING_DATA_ATTESTATION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    model_seq_id: int
    base_model: str
    lora_config: LoraConfig
    user_metadata: _struct_pb2.Struct
    training_data_attestation_id: str
    def __init__(self, session_id: _Optional[str] = ..., model_seq_id: _Optional[int] = ..., base_model: _Optional[str] = ..., lora_config: _Optional[_Union[LoraConfig, _Mapping]] = ..., user_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., training_data_attestation_id: _Optional[str] = ...) -> None: ...

class TrainingDataArtifact(_message.Message):
    __slots__ = ("name", "expected_sha256", "content")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_SHA256_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    expected_sha256: str
    content: bytes
    def __init__(self, name: _Optional[str] = ..., expected_sha256: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class AttestedTrainingDataArtifact(_message.Message):
    __slots__ = ("name", "sha256", "size_bytes")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    name: str
    sha256: str
    size_bytes: int
    def __init__(self, name: _Optional[str] = ..., sha256: _Optional[str] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class CreateTrainingDataAttestationRequest(_message.Message):
    __slots__ = ("session_id", "artifacts")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    artifacts: _containers.RepeatedCompositeFieldContainer[TrainingDataArtifact]
    def __init__(self, session_id: _Optional[str] = ..., artifacts: _Optional[_Iterable[_Union[TrainingDataArtifact, _Mapping]]] = ...) -> None: ...

class CreateTrainingDataAttestationResponse(_message.Message):
    __slots__ = ("training_data_attestation_id", "artifacts")
    TRAINING_DATA_ATTESTATION_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    training_data_attestation_id: str
    artifacts: _containers.RepeatedCompositeFieldContainer[AttestedTrainingDataArtifact]
    def __init__(self, training_data_attestation_id: _Optional[str] = ..., artifacts: _Optional[_Iterable[_Union[AttestedTrainingDataArtifact, _Mapping]]] = ...) -> None: ...

class GetInfoRequest(_message.Message):
    __slots__ = ("model_id",)
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    def __init__(self, model_id: _Optional[str] = ...) -> None: ...

class ModelData(_message.Message):
    __slots__ = ("arch", "model_name", "tokenizer_id")
    ARCH_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_ID_FIELD_NUMBER: _ClassVar[int]
    arch: str
    model_name: str
    tokenizer_id: str
    def __init__(self, arch: _Optional[str] = ..., model_name: _Optional[str] = ..., tokenizer_id: _Optional[str] = ...) -> None: ...

class GetInfoResponse(_message.Message):
    __slots__ = ("type", "model_data", "model_id", "is_lora", "lora_rank", "model_name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_DATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    IS_LORA_FIELD_NUMBER: _ClassVar[int]
    LORA_RANK_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    type: str
    model_data: ModelData
    model_id: str
    is_lora: bool
    lora_rank: int
    model_name: str
    def __init__(self, type: _Optional[str] = ..., model_data: _Optional[_Union[ModelData, _Mapping]] = ..., model_id: _Optional[str] = ..., is_lora: bool = ..., lora_rank: _Optional[int] = ..., model_name: _Optional[str] = ...) -> None: ...

class UnloadModelRequest(_message.Message):
    __slots__ = ("model_id", "seq_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ...) -> None: ...

class ForwardBackwardInput(_message.Message):
    __slots__ = ("data", "loss_fn", "loss_fn_config", "gradient_accumulation", "init_gradients", "compute_expert_flip_metric", "force_routing_replay")
    class LossFnConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOSS_FN_FIELD_NUMBER: _ClassVar[int]
    LOSS_FN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GRADIENT_ACCUMULATION_FIELD_NUMBER: _ClassVar[int]
    INIT_GRADIENTS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_EXPERT_FLIP_METRIC_FIELD_NUMBER: _ClassVar[int]
    FORCE_ROUTING_REPLAY_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Datum]
    loss_fn: str
    loss_fn_config: _containers.ScalarMap[str, float]
    gradient_accumulation: bool
    init_gradients: bool
    compute_expert_flip_metric: bool
    force_routing_replay: str
    def __init__(self, data: _Optional[_Iterable[_Union[Datum, _Mapping]]] = ..., loss_fn: _Optional[str] = ..., loss_fn_config: _Optional[_Mapping[str, float]] = ..., gradient_accumulation: bool = ..., init_gradients: bool = ..., compute_expert_flip_metric: bool = ..., force_routing_replay: _Optional[str] = ...) -> None: ...

class ForwardRequest(_message.Message):
    __slots__ = ("model_id", "seq_id", "forward_input")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    FORWARD_INPUT_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    forward_input: ForwardBackwardInput
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ..., forward_input: _Optional[_Union[ForwardBackwardInput, _Mapping]] = ...) -> None: ...

class ForwardBackwardRequest(_message.Message):
    __slots__ = ("model_id", "seq_id", "forward_backward_input", "upload_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    FORWARD_BACKWARD_INPUT_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    forward_backward_input: ForwardBackwardInput
    upload_id: str
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ..., forward_backward_input: _Optional[_Union[ForwardBackwardInput, _Mapping]] = ..., upload_id: _Optional[str] = ...) -> None: ...

class CreateUploadRequest(_message.Message):
    __slots__ = ("model_id", "total_size", "chunk_count")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    total_size: int
    chunk_count: int
    def __init__(self, model_id: _Optional[str] = ..., total_size: _Optional[int] = ..., chunk_count: _Optional[int] = ...) -> None: ...

class CreateUploadResponse(_message.Message):
    __slots__ = ("upload_id", "max_parallelism")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_PARALLELISM_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    max_parallelism: int
    def __init__(self, upload_id: _Optional[str] = ..., max_parallelism: _Optional[int] = ...) -> None: ...

class UploadChunkRequest(_message.Message):
    __slots__ = ("upload_id", "chunk_index", "data")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    chunk_index: int
    data: bytes
    def __init__(self, upload_id: _Optional[str] = ..., chunk_index: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class UploadChunkResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OptimStepRequest(_message.Message):
    __slots__ = ("model_id", "seq_id", "adam_params")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    ADAM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    adam_params: AdamParams
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ..., adam_params: _Optional[_Union[AdamParams, _Mapping]] = ...) -> None: ...

class LoadWeightsRequest(_message.Message):
    __slots__ = ("model_id", "seq_id", "path", "optimizer")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZER_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    path: str
    optimizer: bool
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ..., path: _Optional[str] = ..., optimizer: bool = ...) -> None: ...

class SaveWeightsRequest(_message.Message):
    __slots__ = ("model_id", "seq_id", "path", "mode", "ttl_seconds")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    seq_id: int
    path: str
    mode: str
    ttl_seconds: int
    def __init__(self, model_id: _Optional[str] = ..., seq_id: _Optional[int] = ..., path: _Optional[str] = ..., mode: _Optional[str] = ..., ttl_seconds: _Optional[int] = ...) -> None: ...

class RetrieveFutureRequest(_message.Message):
    __slots__ = ("request_id", "model_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    model_id: str
    def __init__(self, request_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class RetrieveFutureResponse(_message.Message):
    __slots__ = ("try_again", "failed", "create_model", "forward_backward", "optim_step", "load_weights", "save_weights", "unload_model", "inference", "chat_complete")
    TRY_AGAIN_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    CREATE_MODEL_FIELD_NUMBER: _ClassVar[int]
    FORWARD_BACKWARD_FIELD_NUMBER: _ClassVar[int]
    OPTIM_STEP_FIELD_NUMBER: _ClassVar[int]
    LOAD_WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    SAVE_WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    UNLOAD_MODEL_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_FIELD_NUMBER: _ClassVar[int]
    CHAT_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    try_again: TryAgainResponse
    failed: RequestFailedResponse
    create_model: CreateModelResponse
    forward_backward: ForwardBackwardOutput
    optim_step: OptimStepResponse
    load_weights: LoadWeightsResponse
    save_weights: SaveWeightsResponse
    unload_model: UnloadModelResponse
    inference: InferenceResponse
    chat_complete: ChatCompleteResponse
    def __init__(self, try_again: _Optional[_Union[TryAgainResponse, _Mapping]] = ..., failed: _Optional[_Union[RequestFailedResponse, _Mapping]] = ..., create_model: _Optional[_Union[CreateModelResponse, _Mapping]] = ..., forward_backward: _Optional[_Union[ForwardBackwardOutput, _Mapping]] = ..., optim_step: _Optional[_Union[OptimStepResponse, _Mapping]] = ..., load_weights: _Optional[_Union[LoadWeightsResponse, _Mapping]] = ..., save_weights: _Optional[_Union[SaveWeightsResponse, _Mapping]] = ..., unload_model: _Optional[_Union[UnloadModelResponse, _Mapping]] = ..., inference: _Optional[_Union[InferenceResponse, _Mapping]] = ..., chat_complete: _Optional[_Union[ChatCompleteResponse, _Mapping]] = ...) -> None: ...

class TryAgainResponse(_message.Message):
    __slots__ = ("request_id", "queue_state")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    QUEUE_STATE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    queue_state: str
    def __init__(self, request_id: _Optional[str] = ..., queue_state: _Optional[str] = ...) -> None: ...

class RequestFailedResponse(_message.Message):
    __slots__ = ("error_category", "message", "details")
    ERROR_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    error_category: str
    message: str
    details: _struct_pb2.Struct
    def __init__(self, error_category: _Optional[str] = ..., message: _Optional[str] = ..., details: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateModelResponse(_message.Message):
    __slots__ = ("type", "model_id", "training_run_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    model_id: str
    training_run_id: str
    def __init__(self, type: _Optional[str] = ..., model_id: _Optional[str] = ..., training_run_id: _Optional[str] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens", "training_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TRAINING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    training_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ..., training_tokens: _Optional[int] = ...) -> None: ...

class ForwardBackwardOutput(_message.Message):
    __slots__ = ("type", "loss_fn_output_type", "loss_fn_outputs", "metrics", "usage")
    class LossFnOutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TensorData
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TensorData, _Mapping]] = ...) -> None: ...
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LOSS_FN_OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOSS_FN_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    loss_fn_output_type: str
    loss_fn_outputs: _containers.MessageMap[str, TensorData]
    metrics: _containers.ScalarMap[str, float]
    usage: Usage
    def __init__(self, type: _Optional[str] = ..., loss_fn_output_type: _Optional[str] = ..., loss_fn_outputs: _Optional[_Mapping[str, TensorData]] = ..., metrics: _Optional[_Mapping[str, float]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

class OptimStepResponse(_message.Message):
    __slots__ = ("type", "metrics")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    type: str
    metrics: _containers.ScalarMap[str, float]
    def __init__(self, type: _Optional[str] = ..., metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class LoadWeightsResponse(_message.Message):
    __slots__ = ("type", "path")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    type: str
    path: str
    def __init__(self, type: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class SaveWeightsResponse(_message.Message):
    __slots__ = ("type", "path")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    type: str
    path: str
    def __init__(self, type: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class UnloadModelResponse(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class InferencePrompt(_message.Message):
    __slots__ = ("prompt", "max_tokens", "temperature", "top_p", "top_k", "stop", "seed", "logprobs", "return_prompt_logprobs", "images", "return_expert_routing", "input_ids")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    RETURN_PROMPT_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    RETURN_EXPERT_ROUTING_FIELD_NUMBER: _ClassVar[int]
    INPUT_IDS_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    top_k: int
    stop: _containers.RepeatedScalarFieldContainer[str]
    seed: int
    logprobs: int
    return_prompt_logprobs: bool
    images: _containers.RepeatedScalarFieldContainer[bytes]
    return_expert_routing: bool
    input_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, prompt: _Optional[str] = ..., max_tokens: _Optional[int] = ..., temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., top_k: _Optional[int] = ..., stop: _Optional[_Iterable[str]] = ..., seed: _Optional[int] = ..., logprobs: _Optional[int] = ..., return_prompt_logprobs: bool = ..., images: _Optional[_Iterable[bytes]] = ..., return_expert_routing: bool = ..., input_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class SampleFromTrainingRequest(_message.Message):
    __slots__ = ("model_id", "prompts", "metrics_type")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    METRICS_TYPE_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    prompts: _containers.RepeatedCompositeFieldContainer[InferencePrompt]
    metrics_type: str
    def __init__(self, model_id: _Optional[str] = ..., prompts: _Optional[_Iterable[_Union[InferencePrompt, _Mapping]]] = ..., metrics_type: _Optional[str] = ...) -> None: ...

class InferenceGenerateRequest(_message.Message):
    __slots__ = ("base_model", "prompts", "metrics_type")
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    METRICS_TYPE_FIELD_NUMBER: _ClassVar[int]
    base_model: str
    prompts: _containers.RepeatedCompositeFieldContainer[InferencePrompt]
    metrics_type: str
    def __init__(self, base_model: _Optional[str] = ..., prompts: _Optional[_Iterable[_Union[InferencePrompt, _Mapping]]] = ..., metrics_type: _Optional[str] = ...) -> None: ...

class SampleFromCheckpointRequest(_message.Message):
    __slots__ = ("checkpoint_path", "base_model", "prompts", "metrics_type")
    CHECKPOINT_PATH_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    METRICS_TYPE_FIELD_NUMBER: _ClassVar[int]
    checkpoint_path: str
    base_model: str
    prompts: _containers.RepeatedCompositeFieldContainer[InferencePrompt]
    metrics_type: str
    def __init__(self, checkpoint_path: _Optional[str] = ..., base_model: _Optional[str] = ..., prompts: _Optional[_Iterable[_Union[InferencePrompt, _Mapping]]] = ..., metrics_type: _Optional[str] = ...) -> None: ...

class InferenceResult(_message.Message):
    __slots__ = ("text", "token_logprobs", "tokens", "prompt_token_logprobs", "token_ids", "prompt_token_ids", "top_logprobs", "prompt_top_logprobs", "expert_routing", "metrics")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKEN_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    TOP_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOP_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    EXPERT_ROUTING_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    text: str
    token_logprobs: _containers.RepeatedScalarFieldContainer[float]
    tokens: _containers.RepeatedScalarFieldContainer[str]
    prompt_token_logprobs: _containers.RepeatedScalarFieldContainer[float]
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    prompt_token_ids: _containers.RepeatedScalarFieldContainer[int]
    top_logprobs: _containers.RepeatedCompositeFieldContainer[TopLogprobsPosition]
    prompt_top_logprobs: _containers.RepeatedCompositeFieldContainer[TopLogprobsPosition]
    expert_routing: ExpertRouting
    metrics: _containers.ScalarMap[str, float]
    def __init__(self, text: _Optional[str] = ..., token_logprobs: _Optional[_Iterable[float]] = ..., tokens: _Optional[_Iterable[str]] = ..., prompt_token_logprobs: _Optional[_Iterable[float]] = ..., token_ids: _Optional[_Iterable[int]] = ..., prompt_token_ids: _Optional[_Iterable[int]] = ..., top_logprobs: _Optional[_Iterable[_Union[TopLogprobsPosition, _Mapping]]] = ..., prompt_top_logprobs: _Optional[_Iterable[_Union[TopLogprobsPosition, _Mapping]]] = ..., expert_routing: _Optional[_Union[ExpertRouting, _Mapping]] = ..., metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ExpertRouting(_message.Message):
    __slots__ = ("num_tokens", "num_decoder_layers", "top_k", "layer_indices", "topk_ids", "topk_weights", "routing_handle")
    NUM_TOKENS_FIELD_NUMBER: _ClassVar[int]
    NUM_DECODER_LAYERS_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    LAYER_INDICES_FIELD_NUMBER: _ClassVar[int]
    TOPK_IDS_FIELD_NUMBER: _ClassVar[int]
    TOPK_WEIGHTS_FIELD_NUMBER: _ClassVar[int]
    ROUTING_HANDLE_FIELD_NUMBER: _ClassVar[int]
    num_tokens: int
    num_decoder_layers: int
    top_k: int
    layer_indices: _containers.RepeatedScalarFieldContainer[int]
    topk_ids: bytes
    topk_weights: bytes
    routing_handle: str
    def __init__(self, num_tokens: _Optional[int] = ..., num_decoder_layers: _Optional[int] = ..., top_k: _Optional[int] = ..., layer_indices: _Optional[_Iterable[int]] = ..., topk_ids: _Optional[bytes] = ..., topk_weights: _Optional[bytes] = ..., routing_handle: _Optional[str] = ...) -> None: ...

class TopLogprob(_message.Message):
    __slots__ = ("logprob", "token_id", "token")
    LOGPROB_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    logprob: float
    token_id: int
    token: str
    def __init__(self, logprob: _Optional[float] = ..., token_id: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class TopLogprobsPosition(_message.Message):
    __slots__ = ("candidates",)
    CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    candidates: _containers.RepeatedCompositeFieldContainer[TopLogprob]
    def __init__(self, candidates: _Optional[_Iterable[_Union[TopLogprob, _Mapping]]] = ...) -> None: ...

class InferenceResponse(_message.Message):
    __slots__ = ("results", "usage", "metrics")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[InferenceResult]
    usage: Usage
    metrics: _containers.ScalarMap[str, float]
    def __init__(self, results: _Optional[_Iterable[_Union[InferenceResult, _Mapping]]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ..., metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class ChatCompleteFromBaseRequest(_message.Message):
    __slots__ = ("base_model", "request_json")
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_JSON_FIELD_NUMBER: _ClassVar[int]
    base_model: str
    request_json: str
    def __init__(self, base_model: _Optional[str] = ..., request_json: _Optional[str] = ...) -> None: ...

class ChatCompleteFromCheckpointRequest(_message.Message):
    __slots__ = ("checkpoint_path", "base_model", "request_json")
    CHECKPOINT_PATH_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_JSON_FIELD_NUMBER: _ClassVar[int]
    checkpoint_path: str
    base_model: str
    request_json: str
    def __init__(self, checkpoint_path: _Optional[str] = ..., base_model: _Optional[str] = ..., request_json: _Optional[str] = ...) -> None: ...

class ChatCompleteFromTrainingRequest(_message.Message):
    __slots__ = ("model_id", "request_json")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_JSON_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    request_json: str
    def __init__(self, model_id: _Optional[str] = ..., request_json: _Optional[str] = ...) -> None: ...

class ChatCompleteResponse(_message.Message):
    __slots__ = ("response_json", "status_code", "usage")
    RESPONSE_JSON_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    response_json: str
    status_code: int
    usage: Usage
    def __init__(self, response_json: _Optional[str] = ..., status_code: _Optional[int] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...
