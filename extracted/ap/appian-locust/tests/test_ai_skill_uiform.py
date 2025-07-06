import json
import unittest
from unittest.mock import patch, MagicMock
from appian_locust.uiform import AISkillUiForm
from appian_locust._rdo_interactor import _RDOInteractor

from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet

RDO_HOST = "https://ai-skill-server.net"
AI_SKILL_ID = "id"


class TestAISkillUiForm(unittest.TestCase):
    bff_token_response = read_mock_file("bff_token_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        self.task_set.on_start()

        self.custom_locust.set_response("/suite/rfx/bff-token", 200, self.bff_token_response)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/DesignObjects/InterfaceAuthentication/v1", 200, "{}")

        self.rdo_interactor: _RDOInteractor = _RDOInteractor(self.task_set.appian._interactor, RDO_HOST)

    @patch('appian_locust._rdo_interactor._RDOInteractor.save_ai_skill_ui_request')
    def test_save_ai_skill(self, save_ui_mock: MagicMock) -> None:
        pre_save_state = json.loads(read_mock_file("ai_skill_pre_save_state.json"))
        patch_resp = json.dumps({"uuid": "6151d568-5e9c-4881-82fb-a3b2d8b333bf", "name": "AI_Skill_Name"})
        ai_skill_uiform = AISkillUiForm(rdo_interactor=self.rdo_interactor, rdo_state=pre_save_state, ai_skill_id=AI_SKILL_ID)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/ai-skill/{AI_SKILL_ID}", 200, patch_resp)

        ai_skill_uiform.save_ai_skill_changes()

        _, kwargs = save_ui_mock.call_args_list[0]
        ai_skill_value = kwargs["value"]["aiSkill"]

        self.assertEqual(ai_skill_value, patch_resp)

    @patch('appian_locust._rdo_interactor._RDOInteractor.upload_document_to_ai_skill_server')
    @patch('appian_locust._rdo_interactor._RDOInteractor.upload_document_to_mlas_field')
    def test_upload_documents_to_multiple_file_upload_field(self, upload_doc_mlas_mock: MagicMock, upload_doc_server: MagicMock) -> None:
        file_paths = ["path/to/doc1.pdf", "path/to/doc2.pdf"]
        file_upload_form = json.loads(read_mock_file('mlas_file_upload_form.json'))
        upload_doc_server.side_effect = [(1, 100), (2, 50)]
        expected_file_infos = [
            {
                "file_name": "doc1.pdf",
                "file_id": 1,
                "file_size": 100
            },
            {
                "file_name": "doc2.pdf",
                "file_id": 2,
                "file_size": 50
            }
        ]
        ai_skill_uiform = AISkillUiForm(rdo_interactor=self.rdo_interactor, rdo_state=file_upload_form, ai_skill_id=AI_SKILL_ID)

        ai_skill_uiform.upload_documents_to_multiple_file_upload_field("Unused Label", file_paths)

        _, kwargs = upload_doc_mlas_mock.call_args_list[0]
        file_infos = kwargs["file_infos"]
        self.assertEqual(file_infos, expected_file_infos)
        self.assertEqual(upload_doc_server.call_count, len(file_paths))
