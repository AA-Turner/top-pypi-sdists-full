import json
import unittest
from unittest.mock import patch, MagicMock, mock_open

from appian_locust import AppianTaskSet
from appian_locust.utilities import logger
from appian_locust._rdo_interactor import _RDOInteractor
from locust import Locust, TaskSet

from .mock_client import CustomLocust
from .mock_reader import read_mock_file

log = logger.getLogger(__name__)

RDO_HOST = "https://ai-skill-server.net"


class TestRDOInteractor(unittest.TestCase):
    bff_token_response = read_mock_file("bff_token_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "credentials", [["", ""]])
        setattr(parent_task_set, "auth", ["", ""])

        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.on_start()

        self.custom_locust.set_response("/suite/rfx/bff-token", 200, self.bff_token_response)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/DesignObjects/InterfaceAuthentication/v1", 200, "{}")

        self.rdo_interactor: _RDOInteractor = _RDOInteractor(self.task_set.appian._interactor, RDO_HOST)

    def test_fetch_jwt_token(self) -> None:
        _, csrf = self.rdo_interactor.fetch_jwt_token()
        self.assertEqual(csrf, "75db686f-f8b3-4848-9485-e870deae0544")

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_v1_request(self, post_page_mock: MagicMock) -> None:
        self.rdo_interactor.v1_post_request("jwt", "csrf")

        post_page_mock.assert_called_once()
        _, kwargs = post_page_mock.call_args_list[0]
        headers = kwargs["headers"]
        self.assertEqual(headers["cookie"], "XSRF-TOKEN=csrf; JWT_TOKEN=jwt")

    @patch('appian_locust._rdo_interactor._RDOInteractor.v1_post_request')
    @patch('appian_locust._interactor._Interactor.post_page')
    def test_post_page(self, post_page_mock: MagicMock, v1_request_mock: MagicMock) -> None:
        self.rdo_interactor.last_auth_time = float(0)
        post_page_mock.return_value = self.custom_locust.client.make_response(200, self.bff_token_response, "/anywhere")

        self.rdo_interactor.post_page("/whatever")

        v1_request_mock.assert_called_once()
        self.assertEqual(post_page_mock.call_count, 2)

    @patch('appian_locust._rdo_interactor._RDOInteractor.post_page')
    def test_fetch_ai_skill_creation_dialog_json(self, rdo_post_page_mock: MagicMock) -> None:
        ui_creation_endpoint = f"{RDO_HOST}/sail-server/SYSTEM_SYSRULES_aiSkillCreateDialog/ui"
        self.rdo_interactor.jwt_token = "jwt"
        self.rdo_interactor.rdo_csrf_token = "csrf"
        rdo_post_page_mock.return_value = self.custom_locust.client.make_response(200, "{}", "/anywhere")

        self.rdo_interactor.fetch_ai_skill_creation_dialog_json("prefix")

        rdo_post_page_mock.assert_called_once()
        _, kwargs = rdo_post_page_mock.call_args_list[0]
        headers = kwargs["headers"]
        payload = kwargs["payload"]
        self.assertEqual(headers["cookie"], "XSRF-TOKEN=csrf; JWT_TOKEN=jwt")
        self.assertEqual(headers["x-http-method-override"], "PUT")
        self.assertEqual(payload["initialBindings"], {"flow!jwt": "jwt", "flow!applicationPrefix": "prefix"})
        self.assertEqual(kwargs["uri"], ui_creation_endpoint)

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_fetch_ai_skill_creation_save_dialog_json(self, post_page_mock: MagicMock) -> None:
        post_page_mock.return_value = self.custom_locust.client.make_response(200, "{}", "/anywhere")
        reeval_url = "https://normal_server.net"
        state = {
            "links": [
                {
                    "rel": "update",
                    "href": reeval_url
                }
            ],
            "ui": {
                "testLabel": "customCreateDialog",
                "saveInto": "wherever",
                "_cId": "12"
            },
            "context": "whatever",
            "uuid": "whatever"
        }
        rdo_state = {
            "newObjectUuid": "11"
        }

        self.rdo_interactor.fetch_ai_skill_creation_save_dialog_json(state, rdo_state)

        post_page_mock.assert_called_once()
        _, kwargs = post_page_mock.call_args_list[0]
        payload = kwargs["payload"]
        self.assertEqual(payload["updates"]["#v"][0]["value"]["#v"],
                         "{\"action\":\"COMPLETE_SAVE\",\"objectUuid\":\"11\"}")
        self.assertEqual(kwargs["uri"], reeval_url)

    @patch('appian_locust._rdo_interactor._RDOInteractor.put_page')
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_file_server_upload(self, _open_patch: MagicMock, put_page_mock: MagicMock) -> None:
        ai_skill_id = "ID"
        model_id = "MODEL"
        presigned_url = "https://a_url.net"
        aws_key_id = "key_id"
        expected_data_id = 2
        presigned_url_resp_dict = {
            "presigned_url": presigned_url,
            "headers": {
                "x-amz-server-side-encryption-aws-kms-key-id": aws_key_id
            },
            "data_id": expected_data_id
        }
        presigned_url_resp = json.dumps(presigned_url_resp_dict)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/ai-skill/{ai_skill_id}/doc-classification/{model_id}/actions/get-presigned-url", 200, presigned_url_resp)
        put_page_mock.return_value = self.custom_locust.client.make_response(200, "{}", "/anywhere")

        data_id, _ = self.rdo_interactor.upload_document_to_ai_skill_server(file_path="path/to/doc", ai_skill_id=ai_skill_id, model_id=model_id)

        self.assertEqual(data_id, expected_data_id)
        put_page_mock.assert_called_once()
        _, kwargs = put_page_mock.call_args_list[0]
        self.assertEqual(kwargs["headers"]["x-amz-server-side-encryption-aws-kms-key-id"], aws_key_id)
        self.assertEqual(kwargs["uri"], presigned_url)

    @patch('appian_locust._rdo_interactor._RDOInteractor.post_page')
    def test_file_field_upload(self, post_page_mock: MagicMock) -> None:
        file_infos = [
            {
                "file_name": "file_1",
                "file_size": 100,
                "file_id": 1
            },
            {
                "file_name": "file_2",
                "file_size": 100,
                "file_id": 2
            }
        ]
        expected_file_state = [
            {
                "fileName": "file_1",
                "fileSize": 100,
                "createdAt": 23893457,
                "uploadPosition": 1,
                "fileId": 1,
                "ignored": "false",
                "progress": 100,
                "validation": {
                    "duplicate": "",
                    "fileType": "",
                    "maxFileSize": "",
                    "ok": "true",
                    "isError": ""
                }
            },
            {
                "fileName": "file_2",
                "fileSize": 100,
                "createdAt": 23893457,
                "uploadPosition": 2,
                "fileId": 2,
                "ignored": "false",
                "progress": 100,
                "validation": {
                    "duplicate": "",
                    "fileType": "",
                    "maxFileSize": "",
                    "ok": "true",
                    "isError": ""
                }
            }
        ]
        upload_field_component = {
            "contents": {"saveInto": "anything"},
            "_cId": "ID"
        }

        self.rdo_interactor.upload_document_to_mlas_field(upload_field=upload_field_component, context={}, uuid="uuid", file_infos=file_infos)

        post_page_mock.assert_called_once()
        _, kwargs = post_page_mock.call_args_list[0]
        file_state_used_in_call = kwargs["payload"]["updates"]["#v"][0]["value"]["#v"]["filesState"]
        self.assertEqual(file_state_used_in_call, expected_file_state)

    @patch('appian_locust._rdo_interactor._RDOInteractor.patch_page')
    def test_persist_ai_skill_changes(self, patch_page_mock: MagicMock) -> None:
        ai_skill_id = "id"
        state = {
            "actionList": [
                {
                    "key": {
                        "#t": "type",
                        "#v": "value"
                    }
                }
            ]
        }

        self.rdo_interactor.persist_ai_skill_changes_to_rdo(ai_skill_id=ai_skill_id, state=state)

        patch_page_mock.assert_called_once()
        _, kwargs = patch_page_mock.call_args_list[0]
        self.assertEqual(kwargs["payload"], [{"key": "value"}])
        self.assertEqual(kwargs["uri"], f"{RDO_HOST}/rdo-server/ai-skill/{ai_skill_id}")

    def test_ai_skill_ui_save(self) -> None:
        sail_event_manager_component = {
            "contents": {"saveInto": "anything"},
            "_cId": "ID"
        }
        success_dict = {
            "it": "worked"
        }
        self.custom_locust.set_response(f"{RDO_HOST}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui", 200, json.dumps(success_dict))

        response = self.rdo_interactor.save_ai_skill_ui_request(component=sail_event_manager_component, context={}, uuid="uuid", value={})

        self.assertEqual(success_dict, response)
