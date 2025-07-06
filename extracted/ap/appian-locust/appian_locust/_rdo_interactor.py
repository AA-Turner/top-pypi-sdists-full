from typing import Any, Dict, Optional, Tuple, List
from requests import Response
from ._interactor import _Interactor
from ._locust_error_handler import test_response_for_error
from ._save_request_builder import save_builder
from .utilities.helper import find_component_by_attribute_in_dict, extract_all_by_label, get_username, remove_type_info
from locust.clients import ResponseContextManager
import time
import base64
import json
import sys


class _RDOInteractor(_Interactor):
    def __init__(self, interactor: _Interactor, rdo_host: str):
        super().__init__(interactor.client, interactor.host, interactor.portals_mode, interactor._request_timeout)
        self.rdo_host = rdo_host
        self.last_auth_time = float(0)
        self.auth = interactor.auth
        self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
        self.v1_post_request(jwt_token=self.jwt_token, rdo_csrf_token=self.rdo_csrf_token)

    def get_interaction_host(self) -> str:
        return self.rdo_host

    def fetch_jwt_token(self) -> Tuple:
        uri_full = f"{self.host}/suite/rfx/bff-token"
        payload = {
            "resource": "aiSkill"
        }
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en_US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "origin": self.host,
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-APPIAN-CSRF-TOKEN": self.client.cookies.get("__appianCsrfToken", "")
        }
        resp = super().post_page(uri=uri_full, headers=headers, payload=payload)
        self.last_auth_time = time.time()
        jwt_token = resp.json()["token"]
        jwt_token_split = jwt_token.split('.')[1] + '=='
        string_decoded_jwt = base64.b64decode(s=jwt_token_split).decode('utf-8')
        rdo_csrf_token = json.loads(string_decoded_jwt)['csrf']
        return jwt_token, rdo_csrf_token

    def v1_post_request(self, jwt_token: str, rdo_csrf_token: str) -> Any:
        v1_uri = f"{self.rdo_host}/rdo-server/DesignObjects/InterfaceAuthentication/v1"
        v1_payload = f"access_token={jwt_token}"
        v1_headers = {
            "authority": f"{self.rdo_host}",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en_US,en;q=0.9",
            "origin": self.host,
            "referer": f"{self.host}/",
            "cookie": f"XSRF-TOKEN={rdo_csrf_token}; JWT_TOKEN={jwt_token}",
            "content-type": "application/x-www-form-urlencoded"
        }
        v1_response = super().post_page(uri=v1_uri, payload=v1_payload, headers=v1_headers)
        v1_response.raise_for_status()
        return None

    def setup_rdo_ui_request_headers(self) -> dict:
        ui_headers = {
            "authority": f"{self.rdo_host}",
            "accept": "application/vnd.appian.tv.ui+json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/vnd.appian.tv+json",
            "origin": f"{self.rdo_host}",
            "cookie": f"XSRF-TOKEN={self.rdo_csrf_token}; JWT_TOKEN={self.jwt_token}",
            "x-appian-csrf-token": self.rdo_csrf_token,
            "x-appian-ui-state": "stateful",
            "x-appian-features": self.client.feature_flag,
            "x-appian-features-extended": self.client.feature_flag_extended,
            "x-appian-suppress-www-authenticate": "true",
            "x-client-mode": "SAIL_LIBRARY",
            "x-appian-user-locale": "en_US",
            "x-appian-user-timezone": "",
            "x-appian-user-calendar": "",
            "x-appian-initial-form-factor": "PHONE",
            "x-xsrf-token": self.rdo_csrf_token
        }
        return ui_headers

    def setup_mlas_file_upload_headers(self, kms_id: str) -> dict:
        headers = self.setup_rdo_ui_request_headers()
        headers["accept"] = "*/*"
        headers["content-type"] = "application/pdf"
        headers["x-amz-server-side-encryption"] = "aws:kms"
        headers["x-amz-server-side-encryption-aws-kms-key-id"] = kms_id
        return headers

    # move to fetch method if not used anywhere else by the end of RDO Epic
    def ai_skill_creation_payload(self, jwt_token: str, app_prefix: str) -> dict:
        payload = {
            "initialBindings": {"flow!jwt": f"{jwt_token}", "flow!applicationPrefix": f"{app_prefix}"},
            "#t": "Map"
        }
        return payload

    def ai_skill_creation_save_payload(self, state: Dict[str, Any], object_uuid: str) -> dict:
        component = find_component_by_attribute_in_dict(attribute="testLabel", value="customCreateDialog", component_tree=state)
        value = {
            "#t": "Text",
            "#v": "{\"action\":\"COMPLETE_SAVE\",\"objectUuid\":\"" + object_uuid + "\"}"
        }
        context = state["context"]
        uuid = state["uuid"]
        payload = save_builder() \
            .component(component) \
            .value(value) \
            .context(context) \
            .uuid(uuid) \
            .build()
        return payload

    def post_page(
            self,
            uri: str,
            payload: Any = {},
            headers: Optional[Dict[str, Any]] = None,
            label: Optional[str] = None,
            files: Optional[dict] = None,
            raise_error: bool = True,
            check_login: bool = True) -> Response:
        if time.time() - self.last_auth_time > 10:
            self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
            self.v1_post_request(self.jwt_token, self.rdo_csrf_token)
        if headers is None:
            headers = self.setup_rdo_ui_request_headers()
        return super().post_page(uri, payload, headers, label, files, raise_error, False)

    def put_page(
            self,
            uri: str,
            payload: Any = {},
            headers: Optional[Dict[str, Any]] = None,
            label: Optional[str] = None,
            files: Optional[dict] = None,
            raise_error: bool = True) -> Response:
        if time.time() - self.last_auth_time > 25:
            self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
            self.v1_post_request(self.jwt_token, self.rdo_csrf_token)
        username = get_username(self.auth)
        if headers is None:
            headers = self.setup_rdo_ui_request_headers()
        if files:  # When a file is specified, don't send any data in the 'data' field
            post_payload = None
        elif isinstance(payload, dict):
            post_payload = json.dumps(payload).encode()
        elif isinstance(payload, str):
            post_payload = payload.encode()
        else:
            raise Exception("Cannot PUT a payload that is not of type dict or string")
        with self.client.put(
                uri,
                data=post_payload,
                headers=headers,
                timeout=self._request_timeout,
                name=label,
                files=files,
                catch_response=True) as resp:  # type: ResponseContextManager
            try:
                test_response_for_error(resp, uri, raise_error=raise_error, username=username)
            except Exception as e:
                raise e
            else:
                if raise_error:
                    resp.raise_for_status()
            return resp

    def patch_page(self, uri: str,
                   payload: Any = {},
                   headers: Optional[Dict[str, Any]] = None,
                   label: Optional[str] = None,
                   files: Optional[dict] = None,
                   raise_error: bool = True) -> Response:
        if time.time() - self.last_auth_time > 25:
            self.jwt_token, self.rdo_csrf_token = self.fetch_jwt_token()
            self.v1_post_request(self.jwt_token, self.rdo_csrf_token)
        username = get_username(self.auth)
        if headers is None:
            headers = self.setup_rdo_ui_request_headers()
        if files:  # When a file is specified, don't send any data in the 'data' field
            post_payload = None
        elif isinstance(payload, dict) or isinstance(payload, list):
            post_payload = json.dumps(payload).encode()
        elif isinstance(payload, str):
            post_payload = payload.encode()
        else:
            raise Exception("Cannot PATCH a payload that is not of type dict, list or string")
        with self.client.patch(uri, data=post_payload, headers=headers, timeout=self._request_timeout, name=label, files=files,
                               catch_response=True) as resp:  # type: ResponseContextManager
            try:
                test_response_for_error(resp, uri, raise_error=raise_error, username=username)
            except Exception as e:
                raise e
            else:
                if raise_error:
                    resp.raise_for_status()
            return resp

    def fetch_ai_skill_creation_dialog_json(self, app_prefix: str, locust_request_label: str = "AISkill.CreateDialog") -> Dict[str, Any]:
        headers = self.setup_rdo_ui_request_headers()
        headers["x-http-method-override"] = "PUT"
        payload = self.ai_skill_creation_payload(jwt_token=self.jwt_token, app_prefix=app_prefix)
        uri = f"{self.rdo_host}/sail-server/SYSTEM_SYSRULES_aiSkillCreateDialog/ui"
        return self.post_page(uri=uri, payload=payload, headers=headers, label=locust_request_label).json()

    def fetch_ai_skill_creation_save_dialog_json(self, state: Dict[str, Any], rdo_state: Dict[str, Any], locust_request_label: str = "AISkill.CreationSaveDialog") -> Dict[str, Any]:
        object_uuid = extract_all_by_label(obj=rdo_state, label="newObjectUuid")[0]
        payload = self.ai_skill_creation_save_payload(state=state, object_uuid=object_uuid)
        list_of_links = state["links"]
        for link_object in list_of_links:
            if link_object.get("rel") == "update":
                reeval_url = link_object.get("href", "")
                break
        headers = super().setup_sail_headers()
        headers["X-client-mode"] = "DESIGN"
        return super().post_page(
            uri=reeval_url,
            payload=payload,
            headers=headers,
            label=locust_request_label
        ).json()

    def fetch_ai_skill_designer_json(self, ai_skill_id: str, locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        locust_request_label = locust_request_label or f"Designer.AiSkill.{ai_skill_id}"
        headers = self.setup_rdo_ui_request_headers()
        headers["x-http-method-override"] = "PUT"
        payload = {
            "#t": "Map",
            "initialBindings": {
                "aiskill!aiSkillId": ai_skill_id,
                "aiskill!readOnly": "false",
            }
        }
        return self.post_page(
            uri=f"{self.rdo_host}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui",
            payload=payload,
            headers=headers,
            label=locust_request_label
        ).json()

    def save_ai_skill_ui_request(
            self,
            component: Dict[str, Any],
            context: Dict[str, Any],
            uuid: str,
            value: Dict[str, Any],
            locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        uri = f"{self.rdo_host}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui"
        headers = self.setup_rdo_ui_request_headers()
        payload = save_builder() \
            .component(component) \
            .context(context) \
            .uuid(uuid) \
            .value(value) \
            .build()
        label = locust_request_label or "AISkill.SaveChangesUI"
        return self.post_page(
            uri=uri,
            payload=payload,
            headers=headers,
            label=label
        ).json()

    def persist_ai_skill_changes_to_rdo(self, ai_skill_id: str, state: Dict[str, Any], locust_request_label: Optional[str] = None) -> Dict[str, Any]:
        uri = f"{self.rdo_host}/rdo-server/ai-skill/{ai_skill_id}"
        headers = self.setup_rdo_ui_request_headers()
        headers["accept"] = "*/*"
        headers["content-type"] = "application/json"
        action_list = extract_all_by_label(state, "actionList")[0]
        payload = remove_type_info(action_list)
        label = locust_request_label or "AISkill.PersistModels"
        return self.patch_page(
            uri=uri,
            payload=payload,
            headers=headers,
            label=label
        ).json()

    def get_presigned_url(self, ai_skill_id: str, model_id: str) -> dict:
        uri = f"{self.rdo_host}/rdo-server/ai-skill/{ai_skill_id}/doc-classification/{model_id}/actions/get-presigned-url"
        headers = self.setup_rdo_ui_request_headers()
        return self.post_page(uri=uri, headers=headers, label="Fetch.PresignedUrl").json()

    def upload_document_to_ai_skill_server(self, file_path: str, ai_skill_id: str, model_id: str, locust_request_label: Optional[str] = None) -> Tuple[Any, int]:
        presigned_url_resp = self.get_presigned_url(ai_skill_id=ai_skill_id, model_id=model_id)
        uri = presigned_url_resp["presigned_url"]
        kms_id = presigned_url_resp["headers"]["x-amz-server-side-encryption-aws-kms-key-id"]
        data_id = presigned_url_resp["data_id"]
        locust_request_label = locust_request_label or f"AiSkill.FileServerUpload.{data_id}"
        headers = self.setup_mlas_file_upload_headers(kms_id=kms_id)
        with open(file_path, 'rb') as f:
            files = {"file": f}
            response = self.put_page(uri=uri, headers=headers, files=files, label=locust_request_label)
            file_size = 10  # dummy file size
            response.raise_for_status()
            return (data_id, file_size)

    def upload_document_to_mlas_field(self, upload_field: Dict[str, Any],
                                      context: Dict[str, Any], uuid: str, file_infos: List[Dict[str, Any]], locust_label: Optional[str] = None) -> Dict[str, Any]:
        new_value = {
            "#t": "Map",
            "#v": {
                "filesState":
                [self._make_mlas_file_metadata(file_info["file_id"], file_info["file_size"], position, file_name=file_info["file_name"]) for position, file_info in enumerate(file_infos, 1)],
                "message": None
            }
        }
        payload = save_builder() \
            .component(upload_field) \
            .context(context) \
            .uuid(uuid) \
            .value(new_value) \
            .build()
        locust_label = locust_label or "MLASUploadField.Upload"
        post_url = f"{self.rdo_host}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui"
        resp = self.post_page(post_url, payload=payload, label=locust_label)
        return resp.json()

    def _make_mlas_file_metadata(self, id: int, doc_size: int, position: int, file_name: str) -> dict:
        """Produces a file metadata object to use for multifile upload fields"""
        return {
            "fileName": file_name,
            "fileSize": doc_size,
            "createdAt": 23893457,
            "uploadPosition": position,
            "fileId": id,
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
