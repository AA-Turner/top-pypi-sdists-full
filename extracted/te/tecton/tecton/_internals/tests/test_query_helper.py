from datetime import datetime
from io import BytesIO
from typing import Optional
from unittest import TestCase

import numpy
import pandas
import requests
from google.protobuf.struct_pb2 import Struct
from google.protobuf.struct_pb2 import Value
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal

from tecton._internals.query_helper import _QueryHelper
from tecton_core import errors
from tecton_proto.api.featureservice.feature_service__client_pb2 import FeatureServerComplexDataType
from tecton_proto.api.featureservice.feature_service__client_pb2 import FeatureServerDataType
from tecton_proto.api.featureservice.feature_service__client_pb2 import GetFeaturesResponse
from tecton_proto.api.featureservice.feature_service__client_pb2 import GetFeaturesResult
from tecton_proto.api.featureservice.feature_service__client_pb2 import Metadata
from tecton_proto.api.featureservice.feature_service__client_pb2 import QueryFeaturesResponse


def data_type(type_enum: int, element_type_enum: Optional[int] = None) -> FeatureServerComplexDataType:
    complex_type = FeatureServerComplexDataType()
    complex_type.type = type_enum
    if element_type_enum is not None:
        complex_type.element_type.type = element_type_enum
    return complex_type


def value_proto(value) -> Value:
    # Structs must be created from a top-level dictionary.
    wrapper_dict = {"k": value}
    s = Struct()
    s.update(wrapper_dict)
    return s.fields["k"]


class QueryHelperTest(TestCase):
    def setUp(self) -> None:
        self.query_helper = _QueryHelper("", feature_service_name="test1")

    def test_response_to_feature_vector(self):
        test_features = [
            ("f1", data_type(FeatureServerDataType.int64), value_proto("3")),
            ("f2", data_type(FeatureServerDataType.string), value_proto("three")),
            ("f3", data_type(FeatureServerDataType.float64), value_proto(33.3)),
            # The feature service JSON response uses strings for special float values (e.g. "NaN" and "Infinity").
            ("f4", data_type(FeatureServerDataType.float64), value_proto("Infinity")),
            ("f5", data_type(FeatureServerDataType.boolean), value_proto(True)),
            (
                "f6",
                data_type(FeatureServerDataType.array, FeatureServerDataType.string),
                value_proto(["one", "two", None]),
            ),
            ("f7", data_type(FeatureServerDataType.array, FeatureServerDataType.int64), value_proto(["1", "2", None])),
            (
                "f8",
                data_type(FeatureServerDataType.array, FeatureServerDataType.float32),
                value_proto([1.1, "Infinity", None]),
            ),
        ]
        response = GetFeaturesResponse()
        for f in test_features:
            feature = response.metadata.features.add()
            feature.name = f[0]
            feature.data_type.CopyFrom(f[1])
            response.result.features.extend([f[2]])

        actual_fv = self.query_helper._response_to_feature_vector(response, True, {"jk1": "abc"})
        actual_dict = actual_fv.to_dict()
        expected_dict = {
            "f1": 3,
            "f2": "three",
            "f3": 33.3,
            "f4": float("inf"),
            "f5": True,
            "f6": ["one", "two", None],
            "f7": [1, 2, None],
            "f8": [1.1, float("inf"), None],
            "jk1": "abc",
        }
        self.assertEqual(actual_dict, expected_dict)

        actual_pd = actual_fv.to_pandas()
        expected_pd = pandas.DataFrame(
            [
                [
                    "abc",
                    3,
                    "three",
                    33.3,
                    float("inf"),
                    True,
                    ["one", "two", None],
                    [1, 2, None],
                    [1.1, float("inf"), None],
                ]
            ],
            columns=["jk1", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"],
        )
        assert_frame_equal(actual_pd, expected_pd)

        actual_np = actual_fv.to_numpy()
        expected_np = numpy.array(
            ["abc", 3, "three", 33.3, float("inf"), True, ["one", "two", None], [1, 2, None], [1.1, float("inf"), None]]
        )
        assert_array_equal(actual_np, expected_np)

    def test_response_to_feature_vector_with_metadata(self):
        test_features = [
            ("f1", data_type(FeatureServerDataType.int64), value_proto("3"), 10000),
            ("f2", data_type(FeatureServerDataType.string), value_proto("three"), 100000),
            ("f3", data_type(FeatureServerDataType.float64), value_proto(33.3), 1000000),
            (
                "f4",
                data_type(FeatureServerDataType.array, FeatureServerDataType.string),
                value_proto(["one", "two", None]),
                10000000,
            ),
        ]
        response = GetFeaturesResponse()
        response.metadata.slo_info.slo_eligible = True
        for f in test_features:
            feature = response.metadata.features.add()
            feature.name = f[0]
            feature.data_type.CopyFrom(f[1])
            feature.effective_time.seconds = f[3]
            response.result.features.extend([f[2]])

        actual_fv = self.query_helper._response_to_feature_vector(response, True, {"jk1": "abc"})
        date1 = datetime.utcfromtimestamp(10000)
        date2 = datetime.utcfromtimestamp(100000)
        date3 = datetime.utcfromtimestamp(1000000)
        date4 = datetime.utcfromtimestamp(10000000)

        actual_dict = actual_fv.to_dict(return_effective_times=True)
        expected_dict = {
            "f1": {"value": 3, "effective_time": date1},
            "f2": {"value": "three", "effective_time": date2},
            "f3": {"value": 33.3, "effective_time": date3},
            "f4": {"value": ["one", "two", None], "effective_time": date4},
            "jk1": {"value": "abc", "effective_time": None},
        }
        self.assertEqual(actual_dict, expected_dict)

        actual_pd = actual_fv.to_pandas(return_effective_times=True)
        expected_pd = pandas.DataFrame(
            [
                ["jk1", "abc", None],
                ["f1", 3, date1],
                ["f2", "three", date2],
                ["f3", 33.3, date3],
                ["f4", ["one", "two", None], date4],
            ],
            columns=["name", "value", "effective_time"],
        )
        assert_frame_equal(actual_pd, expected_pd)

        actual_np = actual_fv.to_numpy(return_effective_times=True)
        expected_np = numpy.array([["abc", 3, "three", 33.3, ["one", "two", None]], [None, date1, date2, date3, date4]])
        assert_array_equal(actual_np, expected_np)

    def test_features_dict(self):
        result = GetFeaturesResult()
        meta = Metadata()

        feature = meta.features.add()
        feature.name = "race_track"
        feature.data_type.type = FeatureServerDataType.string
        result.features.extend([value_proto("silverstone")])

        wildcard_join_key = meta.join_keys.add()
        wildcard_join_key.name = "race_id"
        wildcard_join_key.data_type.type = FeatureServerDataType.int64
        result.join_keys.extend([value_proto("5")])

        actual = self.query_helper._feature_dict(result, meta)
        expected = {"race_track": "silverstone", "race_id": 5}
        self.assertEqual(actual, expected)

    def test_query_response_to_pandas(self):
        query_response = QueryFeaturesResponse()

        feature = query_response.metadata.features.add()
        feature.name = "race_track"
        feature.data_type.type = FeatureServerDataType.string
        wildcard_join_key = query_response.metadata.join_keys.add()
        wildcard_join_key.name = "race_id"
        wildcard_join_key.data_type.type = FeatureServerDataType.int64
        for i, val in enumerate([value_proto("silverstone"), value_proto("monza")]):
            result = query_response.results.add()
            feature_result = result.features.extend([val])
            join_key_result = result.join_keys.extend([value_proto(str(i))])

        actual = self.query_helper._query_response_to_pandas(query_response, {"race_season": 2020})
        expected = pandas.DataFrame(
            {
                "race_season": [2020, 2020],
                "race_track": ["silverstone", "monza"],
                "race_id": [0, 1],
            }
        )
        assert_frame_equal(actual, expected)

    def test_detailed_http_raise_for_status(self):
        def http_response(msg="OK", status=200, grpcCode=0):
            r = requests.Response()
            r.status_code = status
            r.raw = BytesIO(bytes(f'{{"message": "{msg}", "code": {grpcCode}}}', encoding="utf-8"))
            return r

        test_err_responses = [
            (http_response(msg="bad request", status=400), errors.TectonValidationError, "bad request"),
            (http_response(msg="no authN", status=401), errors.TectonValidationError, "no authN"),
            (http_response(msg="no authZ", status=403), errors.TectonValidationError, "no authZ"),
            (http_response(msg="not found", status=404), errors.TectonNotFoundError, "not found"),
            (http_response(msg="internal", status=500), errors.TectonInternalError, "internal"),
        ]

        # err responses
        for tr in test_err_responses:
            with self.assertRaisesRegex(tr[1], tr[2]) as e:
                self.query_helper._detailed_http_raise_for_status(tr[0])

        # ok response
        try:
            self.query_helper._detailed_http_raise_for_status(http_response())
        except Exception:
            self.assertTrue(False)
