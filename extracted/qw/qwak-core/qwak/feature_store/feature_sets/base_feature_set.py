import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Tuple

from _qwak_proto.qwak.feature_store.entities.entity_pb2 import (
    EntityDefinition,
    EntitySpec,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSetSpec
from qwak.feature_store._common.feature_set_utils import generate_key_unique_name
from qwak.feature_store.entities.entity import Entity
from qwak.feature_store.validations.validation_response import SuccessValidationResponse

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass

from qwak.clients.feature_store import FeatureRegistryClient
from qwak.exceptions import QwakException
from qwak.feature_store.validations.validation_options import (
    FeatureSetValidationOptions,
)


@dataclass
class BaseFeatureSet(ABC):
    name: str
    data_sources: List[str]
    entity: str = str()
    key: str = str()
    repository: Optional[str] = None
    __instance_module_path__: Optional[str] = None

    def _validate(self):
        self._validate_feature_set_name()

    def _validate_feature_set_name(self):
        """
        Verifies that the name follows these rules (rfc 1123):
        * A name can start or end with a letter or a number
        * A name MUST NOT start or end with a '-' (dash)
        * A name MUST NOT consist of all numeric values
        * A name can be up to 63 characters
        """
        regex = re.compile(r"^(?![_-])\D[a-zA-Z0-9_-]{0,61}[a-zA-Z0-9](?![_-])$")
        if not regex.match(self.name):
            raise QwakException(
                f"feature set name: {self.name} is invalid, name must follow these conditions:"
                f"can start or end with a letter or a number"
                f"name MUST NOT start or end with a '-' (dash)"
                f"name MUST NOT consist of all numeric values"
            )

    def _get_entity_definition(
        self, feature_registry: FeatureRegistryClient
    ) -> EntityDefinition:
        # fs has a key def but not an entity def, return an entity that is valid but not registered
        # This is done mainly for the validation flow/get sample, to avoid registering temporary entities for keys
        if self.key and not self.entity:
            new_key_name: str = generate_key_unique_name(self.name)

            new_key_spec: EntitySpec = Entity(
                name=new_key_name,
                description=f"Key of feature set {self.name}",
                key=self.key,
            )._to_proto()

            # return new entity def with no id
            entity_definition: EntityDefinition = EntityDefinition(
                entity_spec=new_key_spec
            )
        else:
            feature_set_entity = feature_registry.get_entity_by_name(self.entity)

            if not feature_set_entity:
                raise QwakException(
                    f"Trying to register a feature set with a non existing entity or bad key configuration-: {self.entity}"
                )

            entity_definition: EntityDefinition = (
                feature_set_entity.entity.entity_definition
            )

        return entity_definition

    @staticmethod
    @abstractmethod
    def _from_proto(cls, proto: FeatureSetSpec):
        pass

    @abstractmethod
    def _to_proto(
        self,
        git_commit,
        features,
        feature_registry,
        artifact_url: Optional[str] = None,
        **kwargs,
    ) -> Tuple[FeatureSetSpec, Optional[str]]:
        pass

    def get_sample(
        self,
        number_of_rows: int = 10,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> "pd.DataFrame":
        """
        Fetches a sample of the Feature set transformation by loading requested sample of data from the data source
        and executing the transformation on that data.

        :param number_of_rows: number of rows requests
        :param validation_options: validation options
        :returns Sample Pandas Dataframe

        Example:

        ... code-block:: python
            @batch.feature_set(entity="users", data_sources=["snowflake_users_table"])
            @batch.backfill(start_date=datetime(2022, 1, 1))
            def user_features():
                return SparkSqlTransformation("SELECT user_id, age FROM data_source")

            sample_features = user_features.get_sample()
            print(sample_feature)
            #	    user_id	         timestamp	        user_features.age
            # 0	      1	        2021-01-02 17:00:00	              23
            # 1	      1	        2021-01-01 12:00:00	              51
            # 2	      2	        2021-01-02 12:00:00	              66
            # 3	      2	        2021-01-01 18:00:00	              34
        """
        from qwak.feature_store.validations.validator import FeaturesOperatorValidator

        v = FeaturesOperatorValidator()

        response, _ = v.validate_featureset(
            featureset=self,
            sample_size=number_of_rows,
            validation_options=validation_options,
            silence_specific_exceptions=False,
        )

        if isinstance(response, SuccessValidationResponse):
            return response.sample
        else:
            raise QwakException(f"Sampling failed: \n{response}")  # noqa: E231
