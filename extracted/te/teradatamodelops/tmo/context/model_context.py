import os


class DatasetInfo(object):

    def __init__(
        self,
        sql: str = None,
        entity_key: str = None,
        feature_names: list = None,
        target_names: list = None,
        feature_metadata: dict = None,
        predictions: dict = None,
        legacy_data_conf: dict = None,
        **kwargs,  # noqa
    ):
        self.sql = sql
        self.entity_key = entity_key
        self.feature_names = feature_names
        self.target_names = target_names
        self.legacy_data_conf = legacy_data_conf

        if feature_metadata:
            self.feature_metadata_database = feature_metadata.get("database")
            self.feature_metadata_table = feature_metadata.get("table")
            self.feature_metadata_monitoring_group = feature_metadata.get(
                "monitoringGroup", "default"
            )

        if predictions:
            self.predictions_database = predictions.get("database")
            self.predictions_table = predictions.get("table")

    @classmethod
    def from_dict(cls, rendered_dataset: dict):
        if "type" in rendered_dataset and rendered_dataset["type"] == "CatalogBody":
            return cls(
                sql=rendered_dataset.get("sql"),
                entity_key=rendered_dataset.get("entityKey"),
                feature_names=rendered_dataset.get("featureNames"),
                feature_metadata=rendered_dataset.get("featureMetadata"),
                predictions=rendered_dataset.get("predictions"),
                target_names=rendered_dataset.get("targetNames"),
            )
        else:
            # set dict and legacy
            return cls(
                feature_metadata=rendered_dataset.get("featureMetadata"),
                legacy_data_conf=rendered_dataset,
            )

    def get_feature_metadata_fqtn(self):
        if self.feature_metadata_database and self.feature_metadata_table:
            return f"{self.feature_metadata_database}.{self.feature_metadata_table}"
        else:
            return None

    def get_predictions_metadata_fqtn(self):
        return f"{self.predictions_database}.{self.predictions_table}"

    def is_legacy(self):
        return self.legacy_data_conf is not None


class ModelContext(object):

    def __init__(
        self,
        hyperparams: dict,
        dataset_info: DatasetInfo,
        artifact_output_path: str = None,
        artifact_input_path: str = None,
        **kwargs,
    ):

        self.hyperparams = hyperparams
        self.artifact_output_path = artifact_output_path
        self.artifact_input_path = artifact_input_path
        self.dataset_info = dataset_info

        valid_var_keys = {
            "project_id",
            "model_id",
            "model_version",
            "job_id",
            "model_table",
        }
        for key in kwargs:
            if key in valid_var_keys:
                setattr(self, key, kwargs.get(key))

    @property
    def artifact_output_path(self):
        return self.__artefact_output_path

    @artifact_output_path.setter
    def artifact_output_path(self, artifact_output_path):
        if artifact_output_path and not os.path.isdir(artifact_output_path):
            raise ValueError(
                f"artefact_output_path ({artifact_output_path}) does not exist"
            )

        self.__artefact_output_path = artifact_output_path

    @property
    def artifact_input_path(self):
        return self.__artefact_input_path

    @artifact_input_path.setter
    def artifact_input_path(self, artifact_input_path):
        if artifact_input_path and not os.path.isdir(artifact_input_path):
            raise ValueError(
                f"artefact_input_path ({artifact_input_path}) does not exist"
            )

        self.__artefact_input_path = artifact_input_path
