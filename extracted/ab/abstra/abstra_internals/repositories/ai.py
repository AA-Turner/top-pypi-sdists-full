from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any

import requests

from abstra_internals.cloud_api import get_session_path, get_tunnel_secret_key
from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.contracts_generated import (
    CloudApiCliAgentsPostRequestBody,
    CloudApiCliAiV2AbortRequest,
    CloudApiCliAiV2ConversationPostRequest,
    CloudApiCliAiV2ConversationPostResponse,
    CloudApiCliAiV2PromptPostRequest,
    CloudApiCliAiV2QueueClearRequest,
    CloudApiCliAiV2QueuePostRequest,
    CloudApiCliAiV2QueueRemoveRequest,
    CloudApiCliAiV2StreamRequest,
)
from abstra_internals.credentials import resolve_headers
from abstra_internals.environment import REQUEST_TIMEOUT


class AIRepository(ABC):
    def __init__(self, client: "HTTPClient") -> None:
        self.client = client

    @abstractmethod
    def prompt(self, prompt_request_body: CloudApiCliAiV2PromptPostRequest):
        raise NotImplementedError()

    @abstractmethod
    def parse_document(self, model: str, file_content: bytes, mime_type: str):
        raise NotImplementedError()

    @abstractmethod
    def get_ai_messages(
        self,
        req: CloudApiCliAiV2StreamRequest,
        user_jwt=None,
    ):
        raise NotImplementedError()

    @abstractmethod
    def get_history(
        self,
        headers: dict,
        limit: int,
        offset: int,
        summary=False,
        conversation_id=None,
    ):
        raise NotImplementedError()

    @abstractmethod
    def create_thread(self, headers: dict) -> CloudApiCliAiV2ConversationPostResponse:
        raise NotImplementedError()

    @abstractmethod
    def delete_thread(self, headers: dict, thread_id: str):
        raise NotImplementedError()

    @abstractmethod
    def abort_thread(self, headers: dict, thread_id: str):
        raise NotImplementedError()

    @abstractmethod
    def start_conversation(
        self, secret_key: str, tunnel_session_path: str, user_jwt=None
    ):
        raise NotImplementedError()

    @abstractmethod
    def compact_conversation(self, headers: dict, conversation_id: str) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def queue_message(
        self, headers: dict, body: CloudApiCliAiV2QueuePostRequest
    ) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def list_queued_messages(self, headers: dict, conversation_id: str) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def remove_queued_message(
        self, headers: dict, body: CloudApiCliAiV2QueueRemoveRequest
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear_queued_messages(
        self, headers: dict, body: CloudApiCliAiV2QueueClearRequest
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def run_agent(
        self,
        body: CloudApiCliAgentsPostRequestBody,
    ) -> dict[str, Any]:
        raise NotImplementedError()


class ProductionAIRepository(AIRepository):
    def prompt(self, prompt_request_body: CloudApiCliAiV2PromptPostRequest):
        response = self.client.post(
            endpoint="/ai-v2/prompt",
            json=prompt_request_body.to_dict(),
        )

        try:
            response = response.json()
            return response
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON: {response.text}")

    def parse_document(self, model: str, file_content: bytes, mime_type: str):
        response = self.client.post(
            endpoint=f"/ai-v2/parse-document/{model}",
            headers={"Content-Type": mime_type},
            data=file_content,
        )

        if not response.ok:
            # raise_for_status() drops the response body, leaving the user with
            # a generic message like "502 Server Error: Bad Gateway". For
            # parse-document failures, cloud-api returns a JSON {"error": "..."}
            # describing the actual issue (e.g. "Invalid date format: ..."),
            # which is actionable. Surface it in the exception message.
            try:
                body = response.json()
                detail = body.get("error") if isinstance(body, dict) else None
            except ValueError:
                detail = None
            if not detail:
                detail = response.text or response.reason
            raise requests.HTTPError(
                f"{response.status_code} {response.reason}: {detail}",
                response=response,
            )

        return response.json()

    def get_ai_messages(
        self,
        req: CloudApiCliAiV2StreamRequest,
        user_jwt=None,
    ):
        raise NotImplementedError()

    def get_history(
        self,
        headers: dict,
        limit: int,
        offset: int,
        summary=False,
        conversation_id=None,
    ):
        raise NotImplementedError()

    def create_thread(self, headers: dict):
        raise NotImplementedError()

    def abort_thread(self, headers: dict, thread_id: str):
        raise NotImplementedError()

    def start_conversation(
        self, secret_key: str, tunnel_session_path: str, user_jwt=None
    ):
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def delete_thread(self, headers: dict, thread_id: str):
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def compact_conversation(self, headers: dict, conversation_id: str) -> dict:
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def queue_message(
        self, headers: dict, body: CloudApiCliAiV2QueuePostRequest
    ) -> dict:
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def list_queued_messages(self, headers: dict, conversation_id: str) -> list[dict]:
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def remove_queued_message(
        self, headers: dict, body: CloudApiCliAiV2QueueRemoveRequest
    ) -> None:
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def clear_queued_messages(
        self, headers: dict, body: CloudApiCliAiV2QueueClearRequest
    ) -> None:
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def get_user_info(self):
        raise NotImplementedError(
            "This method is not implemented in ProductionAIRepository."
        )

    def run_agent(
        self,
        body: CloudApiCliAgentsPostRequestBody,
    ) -> dict[str, Any]:
        response = self.client.post(
            endpoint="/agents",
            json=body.to_dict(),
            timeout=600,
        )

        if not response.ok:
            # raise_for_status() drops the response body, leaving the user with
            # a generic message like "403 Client Error: Forbidden for url: ...".
            # cloud-api returns {"error": "...", "code": "...", "details": {...}}
            # for things like consumption-blocking; surface the actual message.
            try:
                payload = response.json()
                detail = payload.get("error") if isinstance(payload, dict) else None
            except ValueError:
                detail = None
            if not detail:
                detail = response.text or response.reason
            raise requests.HTTPError(
                f"{response.status_code} {response.reason}: {detail}",
                response=response,
            )

        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception(f"Error parsing agent response: {response.text}")


class LocalAIRepository(AIRepository):
    def prompt(self, prompt_request_body: CloudApiCliAiV2PromptPostRequest):
        response = self.client.post("/ai-v2/prompt", json=prompt_request_body.to_dict())

        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON: {response.text}")

    def parse_document(self, model: str, file_content: bytes, mime_type: str):
        headers = resolve_headers()
        if headers is None:
            raise Exception("You must be logged in to use AI")
        response = self.client.post(
            f"/ai-v2/parse-document/{model}",
            headers={**headers, "Content-Type": mime_type},
            data=file_content,
        )

        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception(f"Error parsing JSON: {response.text}")

    def get_ai_messages(
        self,
        req: CloudApiCliAiV2StreamRequest,
        user_jwt=None,
    ):
        url = "/ai-v2/stream"
        body = req.to_dict()
        headers = resolve_headers()
        if headers is None:
            raise Exception("You must be logged in to use AI")
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        response = self.client.post(url, headers=headers, json=body, stream=True)
        if response.status_code != 200:
            response.raise_for_status()

        return response.iter_content(chunk_size=None)

    def get_history(
        self,
        headers: dict,
        limit: int,
        offset: int,
        summary=False,
        conversation_id=None,
    ):
        url = "/ai-v2/history"
        params: dict = {"limit": limit, "offset": offset}
        if summary:
            params["summary"] = "true"
        if conversation_id:
            params["conversationId"] = conversation_id
        r = self.client.get(
            url,
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def create_thread(self, headers: dict):
        url = "/ai-v2/conversation"
        r = self.client.post(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            json=CloudApiCliAiV2ConversationPostRequest(
                tunnel_session_path=get_session_path(),
                secret_key=get_tunnel_secret_key(),
            ).to_dict(),
        )
        r.raise_for_status()
        return CloudApiCliAiV2ConversationPostResponse.from_dict(r.json())

    def abort_thread(self, headers: dict, thread_id: str):
        response = self.client.post(
            endpoint="/ai-v2/abort",
            headers=headers,
            json=CloudApiCliAiV2AbortRequest(conversation_id=thread_id).to_dict(),
        )
        response.raise_for_status()

    def start_conversation(
        self, secret_key: str, tunnel_session_path: str, user_jwt=None
    ):
        """
        Start a new conversation with the AI.

        This method initializes a new conversation thread with the AI service.

        Args:
            secret_key (str): The secret key for authentication.
            tunnel_session_path (str): The session path for the tunnel.
            user_jwt: Optional JWT token for web-editor user identification.

        Returns:
            dict: The response containing the conversation details.
        """
        url = "/ai-v2/conversation"
        body = CloudApiCliAiV2ConversationPostRequest(
            tunnel_session_path=tunnel_session_path,
            secret_key=secret_key,
        ).to_dict()
        headers = {}
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        response = self.client.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()

    def compact_conversation(self, headers: dict, conversation_id: str) -> dict:
        response = self.client.post(
            "/ai-v2/compact",
            headers=headers,
            json={"conversationId": conversation_id},
        )
        response.raise_for_status()
        return response.json()

    def queue_message(
        self, headers: dict, body: CloudApiCliAiV2QueuePostRequest
    ) -> dict:
        response = self.client.post(
            "/ai-v2/queue", headers=headers, json=body.to_dict()
        )
        response.raise_for_status()
        return response.json()

    def list_queued_messages(self, headers: dict, conversation_id: str) -> list[dict]:
        response = self.client.get(
            "/ai-v2/queue",
            headers=headers,
            params={"conversationId": conversation_id},
        )
        response.raise_for_status()
        return response.json()

    def remove_queued_message(
        self, headers: dict, body: CloudApiCliAiV2QueueRemoveRequest
    ) -> None:
        response = self.client.post(
            "/ai-v2/queue/remove", headers=headers, json=body.to_dict()
        )
        response.raise_for_status()

    def clear_queued_messages(
        self, headers: dict, body: CloudApiCliAiV2QueueClearRequest
    ) -> None:
        response = self.client.post(
            "/ai-v2/queue/clear", headers=headers, json=body.to_dict()
        )
        response.raise_for_status()

    def delete_thread(self, headers: dict, thread_id: str):
        """
        Delete a conversation thread.

        Args:
            headers (dict): The headers for the request, including authentication.
            thread_id (str): The ID of the thread to delete.

        Returns:
            None: The method does not return any value.
        """
        url = f"/ai-v2/conversation/{thread_id}"
        response = self.client.delete(url, headers=headers)
        response.raise_for_status()

    def run_agent(
        self,
        body: CloudApiCliAgentsPostRequestBody,
    ) -> dict[str, Any]:
        headers = resolve_headers()
        if headers is None:
            raise Exception("You must be logged in to run an agent")

        response = self.client.post(
            "/agents",
            headers=headers,
            json=body.to_dict(),
            timeout=600,
        )

        if not response.ok:
            # raise_for_status() drops the response body — bad UX when cloud-api
            # returns a meaningful {"error": "...", "code": "..."} (e.g. for
            # consumption blocking). Surface the actual message.
            try:
                payload = response.json()
                detail = payload.get("error") if isinstance(payload, dict) else None
            except ValueError:
                detail = None
            if not detail:
                detail = response.text or response.reason
            raise requests.HTTPError(
                f"{response.status_code} {response.reason}: {detail}",
                response=response,
            )

        return response.json()
