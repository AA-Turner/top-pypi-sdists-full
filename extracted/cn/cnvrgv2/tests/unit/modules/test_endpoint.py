from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.workflows.endpoint.endpoint import Endpoint
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.json_api_format import JAF


class TestEndpoint:
    def test_stopped_endpoint_update_replicas_error(self, empty_context):
        pass
        # e = Endpoint(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
        # with pytest.raises(CnvrgError) as exception_info:
        #     e.update_replicas(2, 2)
        # assert 'not running' in str(exception_info.value)

    def test_stopped_endpoint_restart_attribute(self, empty_context):
        try:
            e = Endpoint(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.restart()
        except AttributeError as err:
            assert "'Endpoint' object has no attribute 'restart'" in str(err)

    def test_send_logs_wrong_type(self, empty_context):
        try:
            e = Endpoint(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.log(logs="test", log_level="wrong_type")
        except CnvrgArgumentsError as err:
            assert "Wrong attribute type, expected logs level enum, got wrong_type" in str(err)

    def test_send_logs_wrong_message_type(self, empty_context):
        try:
            e = Endpoint(context=empty_context, slug="end-slug", attributes={'status': 'stopped'})
            e.log(logs=1)
        except CnvrgArgumentsError as err:
            assert "Wrong attribute type, expected str, got <class 'int'>" in str(err)

    def test_endpoint_get_predictions(self, mocker, empty_context):
        def mock_response(*args, **kwargs):
            data = {'predictions': [{'model': '1',
                                     'start_time': '2023-01-02 10:34:59',
                                     'input': 'your_input_params',
                                     'output': 'your_input_params',
                                     'elapsed_time': 3,
                                     'offset': 1672655699815},
                                    {'model': '1',
                                     'start_time': '2023-01-02 10:35:59',
                                     'input': 'your_input_params1',
                                     'output': 'your_input_params1',
                                     'elapsed_time': 3,
                                     'offset': 1672655699511},
                                    ], 'offset': 1672655698141, 'total': 2}

            return JAF(response={"data": {"attributes": data}})

        mocker.patch.object(Proxy, 'call_api', side_effect=mock_response)
        e = Endpoint(context=empty_context, slug="end-slug")
        res = e.get_predictions()

        assert res["total"] == 2
