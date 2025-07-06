import json
from typing import Any, Dict, List, Optional
from .._rdo_interactor import _RDOInteractor
from .._interactor import _Interactor
from ..uiform import SailUiForm, KEY_CONTEXT, KEY_UUID
from ..utilities import find_component_by_attribute_in_dict, extract_all_by_label


class AISkillUiForm(SailUiForm):

    def __init__(self, rdo_interactor: _RDOInteractor, rdo_state: Dict[str, Any], ai_skill_id: str, breadcrumb: str = "AISkillUi"):
        self.rdo_interactor = rdo_interactor
        self.ai_skill_id = ai_skill_id
        super().__init__(self.rdo_interactor, rdo_state, breadcrumb)

    def save_ai_skill_changes(self, locust_request_label: Optional[str] = None) -> 'AISkillUiForm':
        """
       Saves an AI Skill Object. This is done in two parts:
        1. Clicking on the Save Changes button which creates an LCP request.
        2. Persisting the model to the RDO Server

       Args:
           locust_request_label (str): Label used to identify the request for locust statistics

       Returns (AISkillUiForm): The latest state of the AI Skill UiForm

       Example:

           >>> form.save_ai_skill_changes()

       """
        locust_request_label = locust_request_label or f"{self.breadcrumb}.SaveChanges"
        component = find_component_by_attribute_in_dict("#t", "SailEventManager", self._state)
        context = self._state[KEY_CONTEXT]
        uuid = self._state[KEY_UUID]
        persist_response_json = self.rdo_interactor.persist_ai_skill_changes_to_rdo(ai_skill_id=self.ai_skill_id, state=self._state, locust_request_label=f"{locust_request_label}.Persist")
        value = {
            "#t": "Map",
            "actionList": [],
            "aiSkill": json.dumps(persist_response_json),
            "saveCounter": 0
        }
        state = self.rdo_interactor.save_ai_skill_ui_request(component, context, uuid, value=value, locust_request_label=locust_request_label)
        self._reconcile_state(state)
        return self

    def upload_documents_to_multiple_file_upload_field(self, label: str, file_paths: List[str], index: int = 1,
                                                       locust_request_label: Optional[str] = None) -> 'AISkillUiForm':
        """
       Uploads multiple documents to an MLAS upload field.

       Args:
           label(str): Currently Unused
           file_paths(list): List of document file paths in string form

       Keyword Args:
           locust_request_label(str): Label used to identify the request for locust statistics

       Returns (AISkillUiForm): The latest state of the AI Skill UiForm

       Example:

           >>> form.upload_document_to_multiple_file_upload_field(["/usr/local/appian/File1.pdf", "/usr/local/appian/File2.pdf"])

       """
        model_id = extract_all_by_label(obj=self._state, label="modelId")[0]
        file_infos = []
        for file_path in file_paths:
            file_name = file_path.split("/")[-1]
            locust_request_label = f"AiSkill.FileServerUpload.{file_name}"
            file_id, file_size = self.rdo_interactor.upload_document_to_ai_skill_server(
                file_path=file_path,
                ai_skill_id=self.ai_skill_id,
                model_id=model_id,
                locust_request_label=locust_request_label)
            file_info = {
                "file_name": file_name,
                "file_id": file_id,
                "file_size": file_size
            }
            file_infos.append(file_info)
        component = find_component_by_attribute_in_dict(
            '#t', "MLASFileUpload", self._state)
        if component.get('#t') != 'MLASFileUpload' and 'contents' in component:
            component = component['contents']
        locust_request_label = f"AISkill.MultiFileUpload.MLASFileUpload"
        new_state = self.rdo_interactor.upload_document_to_mlas_field(
            upload_field=component,
            context=self.context,
            uuid=self.uuid,
            file_infos=file_infos,
            locust_label=locust_request_label
        )
        if not new_state:
            raise Exception(
                f"No response returned when trying to upload file(s) to field MLASFileUpload")
        self._reconcile_state(new_state)
        return self
