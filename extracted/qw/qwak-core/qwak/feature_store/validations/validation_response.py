import ast
from abc import ABC
from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING, List

from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import (
    Feature as ProtoFeature,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2 import (
    GetValidationResultResponse as ProtoGetValidationResultResponse,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_pb2 import (
    SparkColumnDescription as ProtoSparkColumnDescription,
    ValidationFailureResponse as ProtoValidationFailureResponse,
    ValidationSuccessResponse as ProtoValidationSuccessResponse,
)
from qwak.exceptions import QwakException

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass

_VALIDATION_RESPONSE_TYPE_SUCCESS = "success_response"
_VALIDATION_RESPONSE_TYPE_FAILURE = "failure_response"
_VALIDATION_RESPONSE_TYPE_TIMEOUT = "not_ready_response"


class ValidationResponse(ABC):
    pass


@dataclass
class TimeoutValidationResponse(ValidationResponse):
    pass


@dataclass
class FailureValidationResponse(ValidationResponse):
    phase: str
    message: str
    stdout: str
    stderr: str


@dataclass
class SuccessValidationResponse(ValidationResponse):
    sample: "pd.DataFrame"
    features: List[ProtoFeature]
    stdout: str
    stderr: str


class ValidationResponseFactory:
    @staticmethod
    def _get_features(
        spark_columns_description: List[ProtoSparkColumnDescription],
    ) -> List[ProtoFeature]:
        spark_features = []
        for spark_column in spark_columns_description:
            feature_col_name_list = str(spark_column.column_name).split(".")
            feature_name = (
                feature_col_name_list[1]
                if feature_col_name_list.__len__() == 2
                else spark_column.column_name
            )
            spark_features.append(
                ProtoFeature(
                    feature_name=feature_name,
                    feature_type=spark_column.spark_type,
                )
            )
        return spark_features

    @staticmethod
    def from_proto(
        validation_response: ProtoGetValidationResultResponse,
    ) -> ValidationResponse:
        try:
            import pandas as pd
        except ImportError:
            raise QwakException("Missing required Pandas dependency")

        validation_type: str = validation_response.WhichOneof("type")
        if validation_type == _VALIDATION_RESPONSE_TYPE_SUCCESS:
            success: ProtoValidationSuccessResponse = (
                validation_response.success_response
            )

            pd_sample: pd.DataFrame = pd.read_json(
                path_or_buf=StringIO(ast.literal_eval(success.sample)),
                dtype=success.spark_column_description,
            )

            features = ValidationResponseFactory._get_features(
                success.spark_column_description
            )
            return SuccessValidationResponse(
                sample=pd_sample,
                features=features,
                stdout=success.outputs.stdout,
                stderr=success.outputs.stderr,
            )
        elif validation_type == _VALIDATION_RESPONSE_TYPE_FAILURE:
            failure: ProtoValidationFailureResponse = (
                validation_response.failure_response
            )
            return FailureValidationResponse(
                phase=failure.phase,
                message=failure.error_message,
                stdout=failure.outputs.stdout,
                stderr=failure.outputs.stderr,
            )
        elif validation_type == _VALIDATION_RESPONSE_TYPE_TIMEOUT:
            return TimeoutValidationResponse()

        raise QwakException(f"Got unsupported response type: {validation_type}")
