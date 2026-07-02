try:
    from bravado.exception import HTTPBadGateway, HTTPInternalServerError, HTTPNotFound
except ImportError:
    pass  # this tools do not work with the OpenAPI client / AA 5
else:

    from datetime import datetime
    from unittest.mock import Mock

    from app_utils.esi_testing import (
        SIDE_EFFECT_DEFAULT,
        BravadoOperationStub,
        BravadoResponseStub,
        EsiClientStub,
        EsiEndpoint,
    )
    from app_utils.testing import NoSocketsTestCase

    class TestBravadoResponseStub(NoSocketsTestCase):
        def test_create(self):
            # when
            obj = BravadoResponseStub(404, "dummy")
            # then
            self.assertEqual(obj.status_code, 404)
            self.assertEqual(obj.reason, "dummy")
            self.assertEqual(obj.text, "")
            self.assertDictEqual(obj.headers, {})
            self.assertIsNone(obj.raw_bytes)

        def test_str(self):
            obj = BravadoResponseStub(404, "dummy")
            self.assertEqual(str(obj), "404 dummy")

    class TestBravadoOperationStub(NoSocketsTestCase):
        def test_should_return_data_only(self):
            # given
            data = [1, 2, 3]
            obj = BravadoOperationStub(data)
            # when
            result = obj.result()
            # then
            self.assertEqual(result, data)

        def test_should_return_data_and_response(self):
            # given
            data = [1, 2, 3]
            obj = BravadoOperationStub(data, also_return_response=True)
            # when
            result, response = obj.result()
            # then
            self.assertEqual(result, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.reason, "OK")

        def test_should_return_data_and_response_with_custom_status(self):
            # given
            data = [1, 2, 3]
            obj = BravadoOperationStub(
                data, also_return_response=True, status_code=404, reason="NOT FOUND"
            )
            # when
            result, response = obj.result()
            # then
            self.assertEqual(result, data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.reason, "NOT FOUND")

        def test_should_return_data_and_response_with_headers(self):
            # given
            data = [1, 2, 3]
            obj = BravadoOperationStub(
                data, also_return_response=True, headers={"alpha": 1}
            )
            # when
            result, response = obj.result()
            # then
            self.assertEqual(result, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers, {"alpha": 1})

    class TestEsiClientStub(NoSocketsTestCase):
        def setUp(self) -> None:
            self.testdata = {
                "Alpha": {
                    "get_cake": {"1": "cheesecake", "2": "strawberry_cake"},
                    "get_details": {"1": {"appointment": "2015-03-24T11:37:00Z"}},
                    "get_secret": {"1": "blue secret", "2": "red secret"},
                    "get_simple": "steak",
                    "get_double_impact": {"1": {"A": "Madrid", "B": "Tokyo"}},
                }
            }
            self.endpoints = [
                EsiEndpoint("Alpha", "get_cake", "cake_id"),
                EsiEndpoint("Alpha", "get_secret", "secret_id", needs_token=True),
                EsiEndpoint("Alpha", "get_simple"),
                EsiEndpoint("Alpha", "get_double_impact", ("first_id", "second_id")),
            ]
            self.stub = EsiClientStub(self.testdata, self.endpoints)

        def test_can_create_endpoint(self):
            self.assertTrue(hasattr(self.stub, "Alpha"))
            self.assertTrue(hasattr(self.stub.Alpha, "get_cake"))
            self.assertEqual(
                self.stub.Alpha.get_cake(cake_id=1).results(), "cheesecake"
            )
            self.assertEqual(
                self.stub.Alpha.get_cake(cake_id=2).results(), "strawberry_cake"
            )
            self.assertEqual(self.stub.Alpha.get_simple().results(), "steak")
            self.assertEqual(
                self.stub.Alpha.get_double_impact(
                    first_id="1", second_id="B"
                ).results(),
                "Tokyo",
            )

        def test_raises_exception_on_wrong_pk(self):
            with self.assertRaises(ValueError):
                self.stub.Alpha.get_cake(fruit_id=1).results()

        def test_raises_exception_on_missing_pk(self):
            with self.assertRaises(ValueError):
                self.stub.Alpha.get_cake().results()

        def test_raises_exception_on_missing_data(self):
            with self.assertRaises(HTTPNotFound):
                self.stub.Alpha.get_cake(cake_id=3).results()

        def test_raises_exception_on_missing_token_if_required(self):
            with self.assertRaises(ValueError):
                self.stub.Alpha.get_secret(secret_id=1).results()

        def test_raises_exception_when_trying_to_refine_same_endpoint(self):
            with self.assertRaises(ValueError):
                EsiClientStub(
                    self.testdata,
                    [
                        EsiEndpoint("Alpha", "get_cake", "cake_id"),
                        EsiEndpoint("Alpha", "get_cake", "cake_id"),
                    ],
                )

        def test_raises_exception_when_trying_to_refine_endpoint_without_data(self):
            with self.assertRaises(ValueError):
                EsiClientStub(
                    self.testdata,
                    [
                        EsiEndpoint("Alpha", "get_fruit_id", "fruit_id"),
                    ],
                )

        def test_can_convert_datetimes(self):
            stub = EsiClientStub(
                self.testdata,
                [
                    EsiEndpoint("Alpha", "get_details", "id"),
                ],
            )
            results = stub.Alpha.get_details(id=1).results()
            self.assertIsInstance(results["appointment"], datetime)

        def test_create_stub_from_endpoints(self):
            # given
            endpoints = [
                EsiEndpoint(
                    "Alpha",
                    "get_details",
                    "id",
                    data={"1": "dummy"},
                )
            ]
            # when
            stub = EsiClientStub.create_from_endpoints(endpoints)
            # then
            self.assertEqual(stub.Alpha.get_details(id=1).results(), "dummy")

        def test_should_replace_endpoints(self):
            # given
            endpoints = [
                EsiEndpoint(
                    "Alpha",
                    "get_details",
                    "id",
                    data={"1": "dummy"},
                ),
                EsiEndpoint("Alpha", "get_simple", data="simple"),
            ]
            stub_1 = EsiClientStub.create_from_endpoints(endpoints)
            # when
            stub_2 = stub_1.replace_endpoints(
                [
                    EsiEndpoint(
                        "Alpha",
                        "get_details",
                        "id",
                        data={"1": "replaced"},
                    )
                ]
            )
            # then
            self.assertEqual(stub_2.Alpha.get_simple().results(), "simple")
            self.assertEqual(stub_2.Alpha.get_details(id=1).results(), "replaced")
            self.assertNotEqual(stub_1, stub_2)

        def test_should_raise_http_error(self):
            # given
            endpoints = [EsiEndpoint("Alpha", "get_simple", http_error_code=404)]
            stub = EsiClientStub.create_from_endpoints(endpoints)
            # when
            with self.assertRaises(HTTPNotFound):
                self.assertEqual(stub.Alpha.get_simple().results())

        def test_should_return_result_from_side_effect(self):
            # given
            my_mock = Mock()
            my_mock.return_value = "my mock was called"
            endpoints = [EsiEndpoint("Alpha", "get_simple", side_effect=my_mock)]
            stub = EsiClientStub.create_from_endpoints(endpoints)
            # when
            result = stub.Alpha.get_simple().results()
            # then
            self.assertEqual(result, "my mock was called")

        def test_should_return_default_from_side_effect(self):
            # given
            def my_side_effect(**kwargs):
                if kwargs["id"] == 2:
                    return "special"
                return SIDE_EFFECT_DEFAULT

            endpoints = [
                EsiEndpoint(
                    "Alpha",
                    "get_details",
                    "id",
                    data={"1": "alpha", "2": "bravo"},
                    side_effect=my_side_effect,
                )
            ]
            # when
            stub = EsiClientStub.create_from_endpoints(endpoints)
            # then
            self.assertEqual(stub.Alpha.get_details(id=1).results(), "alpha")
            self.assertEqual(stub.Alpha.get_details(id=2).results(), "special")

        def test_raises_http_error_500_on_any_endpoint(self):
            # given
            error_stub = EsiClientStub(self.testdata, self.endpoints, http_error=True)
            # when
            with self.assertRaises(HTTPInternalServerError):
                error_stub.Alpha.get_cake(cake_id=1).results()

        def test_raises_custom_http_error_on_any_endpoint(self):
            # given
            error_stub = EsiClientStub(self.testdata, self.endpoints, http_error=502)
            # when
            with self.assertRaises(HTTPBadGateway):
                error_stub.Alpha.get_cake(cake_id=1).results()

    class TestEsiClientStub2(NoSocketsTestCase):
        def test_can_initialize_with_empty_test_data(self):
            # given
            endpoints = [EsiEndpoint("Alpha", "get_simple", data=[])]
            # when
            stub = EsiClientStub.create_from_endpoints(endpoints)
            # then
            self.assertListEqual(stub.Alpha.get_simple().results(), [])
