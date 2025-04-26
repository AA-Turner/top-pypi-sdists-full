#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import trafaret as t

from datarobot.models.api_object import APIObject


@dataclass
class FeatureCountByType:
    """
    Contains information about a feature type and how many features in the dataset are of this type.

    Attributes
    ----------
    feature_type : str
        The feature type grouped in this count.
    count : int
        The number of features of this type.
    """

    feature_type: str
    count: int


FEATURE_COUNT_BY_TYPE_TRAFARET = t.Dict(
    {
        t.Key("feature_type"): t.String(),
        t.Key("count"): t.Int(),
    }
).ignore_extra("*")


@dataclass
class User:
    """
    Contains information about a user.

    Attributes
    ----------
    Id : str
        Id of the user.
    full_name : Optional[str]
        Full name of the user.
    email : Optional[str]
        Email address of the user.
    user_hash : Optional[str]
        User's gravatar hash.
    user_name : Optional[str]
        Username of the user.
    """

    id: str
    full_name: Optional[str]
    email: Optional[str] = None
    user_hash: Optional[str] = None
    user_name: Optional[str] = None


USER_TRAFARET = t.Dict(
    {
        t.Key("id"): t.String(),
        t.Key("full_name", optional=True): t.String(),
        t.Key("email", optional=True): t.String(),
        t.Key("userhash", optional=True): t.String(),
        t.Key("username", optional=True): t.String(),
    }
).ignore_extra("*")


@dataclass
class ReferencedInUseCase:
    """
    Contains information about the reference of a dataset in an Use Case.

    Attributes
    ----------
    added_to_use_case_by : User
        User who added the dataset to the Use Case.
    added_to_use_case_at : datetime.datetime
        Time when the dataset was added to the Use Case.
    """

    added_to_use_case_by: User
    added_to_use_case_at: datetime


REFERENCED_IN_USE_CASE_TRAFARET = t.Dict(
    {
        t.Key("added_to_use_case_by"): USER_TRAFARET,
        t.Key("added_to_use_case_at"): t.String(),
    }
).ignore_extra("*")


@dataclass()
class DatasetInfo:
    """
    Contains information about the dataset.

    Attributes
    ----------
    dataset_name : str
        Dataset name.
    dataset_version_id : str
        Dataset version Id.
    dataset_id : str
        Dataset Id.
    number_of_rows : int
        Number of rows in the dataset.
    file_size : int
        Size of the dataset as a CSV file, in bytes.
    number_of_features : int
        Number of features in the dataset.
    number_of_feature_by_type : List[FeatureCountByType]
        Number of features in the dataset, grouped by feature type.
    referenced_in_use_case : Optional[ReferencedInUseCase]
        Information about the reference of this dataset in the Use Case. This
        information will only be present if the use_case_id was passed to
        ``ModelLineage.get``.
    """

    dataset_name: str
    dataset_version_id: str
    dataset_id: str
    number_of_rows: int
    file_size: int
    number_of_features: int
    number_of_feature_by_type: List[FeatureCountByType]
    referenced_in_use_case: Optional[ReferencedInUseCase] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(dataset_name={self.dataset_name}, "
            f"dataset_id={self.dataset_id}, "
            f"dataset_version_id={self.dataset_version_id})"
        )


DATASET_INFO_TRAFARET = t.Dict(
    {
        t.Key("dataset_name"): t.String(),
        t.Key("dataset_version_id"): t.String(),
        t.Key("dataset_id"): t.String(),
        t.Key("number_of_rows"): t.Int(),
        t.Key("file_size"): t.Int(),
        t.Key("number_of_features"): t.Int(),
        t.Key("number_of_feature_by_type"): t.List(FEATURE_COUNT_BY_TYPE_TRAFARET),
        t.Key("referenced_in_use_case", optional=True): REFERENCED_IN_USE_CASE_TRAFARET,
    }
).ignore_extra("*")


@dataclass
class FeatureWithMissingValues:
    """
    Contains information about the number of missing values for one feature.

    Attributes
    ----------
    feature_name : str
        Name of the feature.
    number_of_missing_values : int
        Number of missing values for this feature.
    """

    feature_name: str
    number_of_missing_values: int


FEATURE_WITH_MISSING_VALUES_TRAFARET = t.Dict(
    {
        t.Key("feature_name"): t.String(),
        t.Key("number_of_missing_values"): t.Int(),
    }
).ignore_extra("*")


@dataclass
class FeaturelistInfo:
    """
    Contains information about the featurelist.

    Attributes
    ----------
    featurelist_name : str
        Featurelist name.
    featurelist_id : str
        Featurelist Id.
    number_of_features : int
        Number of features in the featurelist.
    number_of_feature_by_type : List[FeatureCountByType]
        Number of features in the featurelist, grouped by feature type.
    number_of_features_with_missing_values : int
        Number of features in the featurelist with at least one missing value.
    number_of_missing_values : int
        Number of missing values across all features of the featurelist.
    features_with_most_missing_values : List[FeatureWithMissingValues]
        List of features with the most missing values.
    description: str
        Description of the featurelist.
    """

    featurelist_name: str
    featurelist_id: str
    number_of_features: int
    number_of_feature_by_type: List[FeatureCountByType]
    number_of_features_with_missing_values: int
    number_of_missing_values: int
    features_with_most_missing_values: List[FeatureWithMissingValues]
    description: str

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(featurelist_name={self.featurelist_name}, "
            f"featurelist_id={self.featurelist_id})"
        )


FEATURELIST_INFO_TRAFARET = t.Dict(
    {
        t.Key("featurelist_name"): t.String(),
        t.Key("featurelist_id"): t.String(),
        t.Key("number_of_features"): t.Int(),
        t.Key("number_of_feature_by_type"): t.List(FEATURE_COUNT_BY_TYPE_TRAFARET),
        t.Key("number_of_features_with_missing_values"): t.Int(),
        t.Key("number_of_missing_values"): t.Int(),
        t.Key("features_with_most_missing_values"): t.List(FEATURE_WITH_MISSING_VALUES_TRAFARET),
        t.Key("featurelist_id"): t.String(),
        t.Key("description"): t.String(),
    }
).ignore_extra("*")


@dataclass
class TargetInfo:
    """
    Contains information about the target.

    Attributes
    ----------
    name : str
        Name of the target feature.
    target_type : str
        Project type resulting from selected target.
    positive_class_label : Optional[Union[str, int, float]]
        Positive class label. For every project type except Binary Classification, this value
        will be null.
    mean : Optional[float]
        Mean of the target. This field will only be available for Binary Classification,
        Regression, and Min Inflated projects.
    """

    name: str
    target_type: str
    positive_class_label: Optional[Union[str, int, float]] = None
    mean: Optional[float] = None


TARGET_INFO_TRAFARET = t.Dict(
    {
        t.Key("name"): t.String(),
        t.Key("target_type"): t.String(),
        t.Key("positive_class_label", optional=True): t.Or(t.String(), t.Float(), t.Int()),
        t.Key("mean", optional=True): t.Float(),
    }
).ignore_extra("*")


@dataclass
class PartitionInfo:
    """
    Contains information about project partitioning.

    Attributes
    ----------
    validation_type : str
        Either CV for cross-validation or TVH for train-validation-holdout split.
    cv_method : str
        Partitioning method used.
    holdout_pct : float
        Percentage of the dataset reserved for the holdout set.
    datetime_col : Optional[str]
        If a date partition column was used, the name of the column. Note that datetime_col applies
        to an old partitioning method no longer supported for new projects, as of API version v2.0.
    datetime_partition_column : Optional[str]
        If a datetime partition column was used, the name of the column.
    validation_pct : Optional[float]
        If train-validation-holdout split was used, the percentage of the dataset used for the
        validation set.
    reps: Optional[float]
        If cross validation was used, the number of folds to use.
    cv_holdout_level : Optional[Union[str, float, int]]
        If a user partition column was used with cross validation, the value assigned to the
        holdout set.
    holdout_level : Optional[Union[str, float, int]]
        If a user partition column was used with train-validation-holdout split, the value assigned
        to the holdout set.
    user_partition_col : Optional[str]
        If a user partition column was used, the name of the column.
    training_level : Optional[Union[str, float, int]]
        If a user partition column was used with train-validation-holdout split, the value assigned
        to the training set.
    partition_key_cols : Optional[List[str]]
        A list containing a single string - the name of the group partition column.
    validation_level : Optional[Union[str, float, int]]
        If a user partition column was used with train-validation-holdout split, the value assigned
        to the validation set.
    use_time_series : Optional[bool]
        A boolean value indicating whether a time series project was created by using datetime
        partitioning. Otherwise, datetime partitioning created an OTV project.
    """

    validation_type: str
    cv_method: str
    holdout_pct: float
    datetime_col: Optional[str] = None
    datetime_partition_column: Optional[str] = None
    validation_pct: Optional[float] = None
    reps: Optional[float] = None
    cv_holdout_level: Optional[Union[str, float, int]] = None
    holdout_level: Optional[Union[str, float, int]] = None
    user_partition_col: Optional[str] = None
    training_level: Optional[Union[str, float, int]] = None
    partition_key_cols: Optional[List[str]] = None
    validation_level: Optional[Union[str, float, int]] = None
    use_time_series: Optional[bool] = None


PARTITION_INFO_TRAFARET = t.Dict(
    {
        t.Key("validation_type"): t.String(),
        t.Key("cv_method"): t.String(),
        t.Key("holdout_pct"): t.Float(),
        t.Key("datetime_col", optional=True): t.String(),
        t.Key("datetime_partition_column", optional=True): t.String(),
        t.Key("validation_pct", optional=True): t.Float(),
        t.Key("reps", optional=True): t.Float(),
        t.Key("cv_holdout_level", optional=True): t.Or(t.String(), t.Float(), t.Int()),
        t.Key("holdout_level", optional=True): t.Or(t.String(), t.Float(), t.Int()),
        t.Key("user_partition_col", optional=True): t.String(),
        t.Key("training_level", optional=True): t.Or(t.String(), t.Float(), t.Int()),
        t.Key("partition_key_cols", optional=True): t.List(t.String()),
        t.Key("validation_level", optional=True): t.Or(t.String(), t.Float(), t.Int()),
        t.Key("use_time_series", optional=True): t.Bool(),
    }
).ignore_extra("*")


@dataclass
class ProjectInfo:
    """
    Contains information about the project.

    Attributes
    ----------
    project_name : str
        Name of the project.
    project_id : str
        Project Id.
    partition : PartitionInfo
        Partitioning settings of the project.
    metric : str
        Project metric used to select the best-performing models.
    created_by : User
        User who created the project.
    created_at : Optional[datetime.datetime]
        Time when the project was created.
    target : Optional[TargetInfo]
        Information about the target.
    """

    project_name: str
    project_id: str
    partition: PartitionInfo
    metric: str
    created_by: User
    created_at: Optional[datetime] = None
    target: Optional[TargetInfo] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(project_name={self.project_name}, "
            f"project_id={self.project_id})"
        )


PROJECT_INFO_TRAFARET = t.Dict(
    {
        t.Key("project_name"): t.String(),
        t.Key("project_id"): t.String,
        t.Key("partition"): PARTITION_INFO_TRAFARET,
        t.Key("metric"): t.String(),
        t.Key("created_by"): USER_TRAFARET,
        t.Key("created_at", optional=True): t.String(),
        t.Key("target", optional=True): TARGET_INFO_TRAFARET,
    }
).ignore_extra("*")


@dataclass
class ModelInfo:
    """
    Contains information about the model.

    Attributes
    ----------
    blueprint_tasks : List[str]
        Tasks that make up the blueprint.
    blueprint_id : str
        Blueprint Id.
    model_type : str
        Model type.
    sample_size : Optional[int]
        Number of rows this model was trained on.
    sample_percentage : Optional[float]
        Percentage of the dataset the model was trained on.
    milliseconds_to_predict_1000_rows : Optional[float]
        Estimate of how many millisecond it takes to predict 1000 rows. The estimate is based on
        the time it took to predict the holdout set.'
    serialized_blueprint_file_size : Optional[int]
        Size of the serialized blueprint, in bytes.
    """

    blueprint_tasks: List[str]
    blueprint_id: str
    model_type: str
    sample_size: Optional[int]
    sample_percentage: Optional[float] = None
    milliseconds_to_predict_1000_rows: Optional[float] = None
    serialized_blueprint_file_size: Optional[int] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(model_type={self.model_type}, "
            f"blueprint_id={self.blueprint_id})"
        )


MODEL_INFO_TRAFARET = t.Dict(
    {
        t.Key("blueprint_tasks"): t.List(t.String()),
        t.Key("blueprint_id"): t.String(),
        t.Key("model_type"): t.String(),
        t.Key("sample_size", optional=True): t.Int(),
        t.Key("sample_percentage", optional=True): t.Float(),
        t.Key("milliseconds_to_predict_1000_rows", optional=True): t.Float(),
        t.Key("serialized_blueprint_file_size", optional=True): t.Int(),
    }
).ignore_extra("*")


class ModelLineage(APIObject):
    """
    Contains information about the lineage of a model.

    Attributes
    ----------
    dataset : DatasetInfo
        Information about the dataset this model was created with.
    featurelist : FeaturelistInfo
        Information about the featurelist used to train this model.
    project : ProjectInfo
        Information about the project this model was created in.
    model : ModelInfo
        Information about the model itself.
    """

    _converter = t.Dict(
        {
            t.Key("dataset", optional=True): DATASET_INFO_TRAFARET,
            t.Key("featurelist"): FEATURELIST_INFO_TRAFARET,
            t.Key("project"): PROJECT_INFO_TRAFARET,
            t.Key("model"): MODEL_INFO_TRAFARET,
        }
    ).ignore_extra("*")

    def __init__(
        self,
        featurelist: Dict[str, Any],
        project: Dict[str, Any],
        model: Dict[str, Any],
        dataset: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.featurelist = self._construct_featurelist_info(featurelist)
        self.project = self._construct_project_info(project)
        self.model = self._construct_model_info(model)
        self.dataset = self._construct_dataset_info(dataset)

    @classmethod
    def get(cls, model_id: str, use_case_id: Optional[str] = None) -> "ModelLineage":
        """
        Retrieve lineage information about a trained model. If you pass the optional
        ``use_case_id`` parameter, this class will contain additional information.

        Parameters
        ----------
        model_id : str
            Model Id.
        use_case_id : Optional[str]
            Use Case Id.

        Returns
        -------
        ModelLineage
        """
        url = f"models/{model_id}/lineage/"
        params = {}
        if use_case_id is not None:
            params["use_case_id"] = use_case_id
        return cls.from_location(url, params=params)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ModelLineage)
            and self.dataset == other.dataset
            and self.project == other.project
            and self.featurelist == other.featurelist
            and self.model == other.model
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(project={self.project}, dataset={self.dataset}, "
            f"featurelist={self.featurelist}, model={self.model})"
        )

    @staticmethod
    def _construct_featurelist_info(featurelist: Dict[str, Any]) -> FeaturelistInfo:
        return FeaturelistInfo(
            featurelist_name=featurelist["featurelist_name"],
            featurelist_id=featurelist["featurelist_id"],
            number_of_features=featurelist["number_of_features"],
            number_of_feature_by_type=[
                FeatureCountByType(**t) for t in featurelist["number_of_feature_by_type"]
            ],
            number_of_features_with_missing_values=featurelist[
                "number_of_features_with_missing_values"
            ],
            number_of_missing_values=featurelist["number_of_missing_values"],
            features_with_most_missing_values=[
                FeatureWithMissingValues(**f)
                for f in featurelist["features_with_most_missing_values"]
            ],
            description=featurelist["description"],
        )

    @classmethod
    def _construct_project_info(cls, project: Dict[str, Any]) -> ProjectInfo:
        target = project.get("target")
        created_at = project.get("created_at")
        if created_at is not None:
            created_at = pd.to_datetime(created_at).to_pydatetime()
        return ProjectInfo(
            project_name=project["project_name"],
            project_id=project["project_id"],
            partition=PartitionInfo(**project["partition"]),
            metric=project["metric"],
            created_by=cls._construct_user_from_api_data(project["created_by"]),
            created_at=created_at,
            target=TargetInfo(**target) if target else None,
        )

    @staticmethod
    def _construct_user_from_api_data(user_data: Dict[str, Any]) -> User:
        user = User(
            id=user_data["id"],
            full_name=user_data.get("full_name"),
            email=user_data.get("email"),
            user_hash=user_data.get("userhash"),
            user_name=user_data.get("username"),
        )
        return user

    @classmethod
    def _construct_dataset_info(
        cls, dataset: Optional[Dict[str, Any]] = None
    ) -> Optional[DatasetInfo]:
        """
        Construct a dataset_info object.
        """
        if dataset is None:
            return None

        referenced_in_use_case = dataset.get("referenced_in_use_case")
        _referenced_in_use_case = None
        if referenced_in_use_case is not None:
            _referenced_in_use_case = ReferencedInUseCase(
                added_to_use_case_by=cls._construct_user_from_api_data(
                    referenced_in_use_case["added_to_use_case_by"]
                ),
                added_to_use_case_at=pd.to_datetime(
                    referenced_in_use_case["added_to_use_case_at"]
                ).to_pydatetime(),
            )

        return DatasetInfo(
            dataset_name=dataset["dataset_name"],
            dataset_version_id=dataset["dataset_version_id"],
            dataset_id=dataset["dataset_id"],
            number_of_rows=dataset["number_of_rows"],
            file_size=dataset["file_size"],
            number_of_features=dataset["number_of_features"],
            number_of_feature_by_type=[
                FeatureCountByType(**t) for t in dataset["number_of_feature_by_type"]
            ],
            referenced_in_use_case=_referenced_in_use_case,
        )

    @staticmethod
    def _construct_model_info(model: Dict[str, Any]) -> ModelInfo:
        return ModelInfo(
            blueprint_tasks=model["blueprint_tasks"],
            blueprint_id=model["blueprint_id"],
            model_type=model["model_type"],
            sample_size=model.get("sample_size"),
            sample_percentage=model.get("sample_percentage"),
            milliseconds_to_predict_1000_rows=model.get("milliseconds_to_predict_1000_rows"),
            serialized_blueprint_file_size=model.get("serialized_blueprint_file_size"),
        )
