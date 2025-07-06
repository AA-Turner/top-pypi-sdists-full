import pytest

from cnvrgv2.errors import CnvrgArgumentsError, CnvrgFileError
from cnvrgv2.modules.dataset import Dataset
from cnvrgv2.modules.flows.flow import Flow
from cnvrgv2.modules.flows.flows_client import FlowsClient
from cnvrgv2.proxy import Proxy


class TestFlows:

    def test_flow_toggle_webhook_success(self, mocker, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        mocked_toggle = mocker.patch.object(Proxy, 'call_api')
        flow.toggle_webhook(True)
        assert mocked_toggle.call_count == 1

    def test_flow_toggle_webhook_wrong_argument_type(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.toggle_webhook("on")

    def test_flow_toggle_dataset_update_success(self, mocker, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        dataset = Dataset(context=empty_context, slug="dataset-slug")
        mocked_toggle = mocker.patch.object(Proxy, 'call_api')
        flow.toggle_dataset_update(True, dataset=dataset)
        assert mocked_toggle.call_count == 1

    def test_flow_toggle_dataset_update_wrong_toggle_argument_type(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.toggle_dataset_update("on")

    def test_flow_toggle_dataset_update_wrong_dataset_argument_type(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.toggle_dataset_update(True, "dataset")

    def test_flow_toggle_dataset_update_wrong_toggle_and_dataset_argument_types(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.toggle_dataset_update("on", "dataset")

    def test_flow_set_schedule_value_success(self, mocker, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        mocked_toggle = mocker.patch.object(Proxy, 'call_api')
        flow.set_schedule("59 12 25 3 4")
        assert mocked_toggle.call_count == 1

    def test_flow_set_illegal_schedule_value_fail(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.set_schedule("1000 1000 * * *")

    def test_flow_set_insufficient_schedule_arguments_fail(self, empty_context):
        flow = Flow(context=empty_context, slug="flow-slug")
        with pytest.raises(CnvrgArgumentsError):
            flow.set_schedule("20 10")

    def test_flow_create_return_error_wrong_yaml_path_fail(self, empty_context):
        with pytest.raises(CnvrgFileError):
            FlowsClient.create(self, yaml_path="bad/yaml/path")

    def test_flow_create_return_error_wrong_yaml_string_fail(self, empty_context):
        with pytest.raises(CnvrgArgumentsError):
            FlowsClient.create(self, yaml_string={})

    def test_flow_create_return_error_both_wrong_yaml_params_fail(self, empty_context):
        with pytest.raises(CnvrgArgumentsError):
            FlowsClient.create(self, yaml_string="string", yaml_path='/path')
