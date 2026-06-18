from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from picsellia.types.enums import (
    AnnotationStatus,
    AssignmentStatus,
    CampaignStepType,
    DataType,
    DataUploadStatus,
    ExperimentStatus,
    Framework,
    InferenceType,
    JobRunStatus,
    JobStatus,
    LogType,
    ProcessingType,
    TagTarget,
)


class DaoSchema(BaseModel):
    # Might not be defined if refresh is done manually
    id: UUID | None = None


class DatalakeSchema(DaoSchema):
    name: str
    connector_id: UUID | None = None


class OrganizationSchema(DaoSchema):
    name: str
    default_connector_id: UUID | None = None


class DatasetSchema(DaoSchema):
    name: str


class DatasetVersionSchema(DaoSchema):
    name: str = Field(alias="origin_name")
    origin_id: UUID = Field(alias="origin_id")
    annotation_campaign_id: UUID | None = None
    version: str
    type: InferenceType


class AnnotationCampaignSchema(DaoSchema):
    dataset_version_id: UUID


class ReviewCampaignSchema(DaoSchema):
    deployment_id: UUID


class CampaignStepSchema(DaoSchema):
    name: str
    order: int
    type: CampaignStepType


class DatasetVersionStats(BaseModel):
    label_repartition: dict[str, int]
    nb_objects: int
    nb_annotations: int


class ModelSchema(DaoSchema):
    name: str
    private: bool


class ModelVersionSchema(DaoSchema):
    origin: ModelSchema
    name: str
    version: int
    labels: dict | None = None
    type: InferenceType
    framework: Framework


class ModelDataSchema(DaoSchema):
    name: str
    version_id: UUID
    repartition: dict


class ModelContextSchema(DaoSchema):
    experiment_id: UUID | None = None
    datas: list[ModelDataSchema]
    parameters: dict


class ModelFileSchema(DaoSchema):
    name: str
    object_name: str
    filename: str
    large: bool
    url: str | None = Field(alias="presigned_url", default=None)


class ProjectSchema(DaoSchema):
    name: str


class DeploymentSchema(DaoSchema):
    name: str
    type: InferenceType
    oracle_host: str | None = None
    serving_host: str | None = None
    review_campaign_id: UUID | None = None


class TargetDatalakeConnectorSchema(DaoSchema):
    id: UUID
    client_type: str
    bucket_name: str


class ImageMetaSchema(BaseModel):
    width: int
    height: int


class VideoMetaSchema(BaseModel):
    width: int
    height: int


class DataSchema(DaoSchema):
    object_name: str
    filename: str
    type: DataType
    content_type: str
    upload_status: DataUploadStatus
    url: str | None = Field(alias="presigned_url", default=None)
    metadata: dict | None = None
    custom_metadata: dict | None = None


class ImageSchema(DataSchema):
    meta: ImageMetaSchema


class VideoSchema(DataSchema):
    meta: VideoMetaSchema


# It's a partial DataSchema
class AssignmentDataSchema(DaoSchema):
    id: UUID
    filename: str
    object_name: str
    url: str | None = Field(alias="presigned_url", default=None)


class AssignmentSchema(DaoSchema):
    asset_id: UUID
    user_id: UUID | None = Field(alias="assigned_user_id", default=None)
    step_id: UUID
    status: AssignmentStatus
    data: AssignmentDataSchema


class DataProjectionSchema(DaoSchema):
    name: str | None = None
    object_name: str | None = None
    filename: str | None = None
    compute_status: DataUploadStatus
    url: str | None = Field(alias="presigned_url", default=None)
    infos: dict | None = None


class DataSourceSchema(DaoSchema):
    name: str


class AssetSchema(DaoSchema):
    data: ImageSchema | VideoSchema


class PredictedAssetSchema(DaoSchema):
    data: ImageSchema
    oracle_prediction_id: UUID


class ExperimentSchema(DaoSchema):
    name: str
    project_id: UUID
    status: ExperimentStatus


class FastTrainingSchema(DaoSchema):
    job_id: UUID
    job_run_id: UUID
    status: JobRunStatus
    experiment_id: UUID
    experiment_name: str


class EvaluationSchema(DaoSchema):
    asset_id: UUID


class UserSchema(DaoSchema):
    username: str


class WorkerSchema(DaoSchema):
    username: str
    user_id: UUID


class ArtifactSchema(DaoSchema):
    name: str
    object_name: str
    filename: str
    large: bool
    url: str | None = Field(alias="presigned_url", default=None)


class LoggingFileSchema(DaoSchema):
    object_name: str
    url: str | None = Field(alias="presigned_url", default=None)


LogDataType = list | dict | float | int | str


class LogSchema(DaoSchema):
    name: str
    type: LogType
    data: LogDataType


class TagSchema(DaoSchema):
    name: str
    target_type: TagTarget


class LabelSchema(DaoSchema):
    name: str
    group_id: UUID | None = None


class LabelGroupSchema(DaoSchema):
    name: str
    parent_id: UUID | None = None


class AnnotationSchema(DaoSchema):
    duration: float
    status: AnnotationStatus
    attributes: dict[str, Any] | None = None


class ShapeSchema(DaoSchema):
    label: LabelSchema
    text: str | None = None
    attributes: dict[str, Any] | None = None


class RectangleSchema(ShapeSchema):
    x: int
    y: int
    w: int
    h: int


class PolygonSchema(ShapeSchema):
    coords: list = Field(alias="polygon")


class LineSchema(ShapeSchema):
    coords: list = Field(alias="line")


class PointSchema(ShapeSchema):
    coords: list = Field(alias="point")


class ClassificationSchema(ShapeSchema):
    pass


class JobSchema(DaoSchema):
    status: JobStatus


class JobRunSchema(DaoSchema):
    status: JobRunStatus


class ProcessingSchema(DaoSchema):
    name: str
    type: ProcessingType
    docker_image: str
    docker_tag: str


# helpers
class CloudProjectionObject(BaseModel):
    name: str
    object_name: str


class CloudObject(BaseModel):
    metadata: dict | None = None
    custom_metadata: dict | None = None
    tags: list[str] = Field(default_factory=list)
    data_source: str | None = None
