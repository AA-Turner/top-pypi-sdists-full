import json
import logging
import os
import warnings
from collections import defaultdict
from enum import Enum
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    Optional,
    Type,
    TypeVar,
)

import attrs
import cbor2 as cbor2
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from grazie.api.client._common import UnknownMetadataResponse
from grazie.api.client.chat.prompt import ChatPrompt as ChatPromptV6
from grazie.api.client.chat.response import ChatResponse as ChatResponseV6
from grazie.api.client.chat.response import ChatResponseStream as ChatResponseStreamV6
from grazie.api.client.chat.response import LLMChatEvent as LLMChatEventV6
from grazie.api.client.chat.response import LLMChatEventTypeV6, LLMChatEventV5
from grazie.api.client.completion.prompt import CompletionPrompt as CompletionPromptV3
from grazie.api.client.completion.response import (
    CompletionResponse as CompletionResponseV3,
)
from grazie.api.client.completion.response import (
    CompletionResponseStream as CompletionResponseStreamV3,
)
from grazie.api.client.completion.response import LLMCompleteEventV3
from grazie.api.client.emb.request import EmbeddingRequest, LLMEmbeddingRequest
from grazie.api.client.emb.response import EmbeddingResponse
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.llm_parameters import LLMParameters as LLMParametersV6
from grazie.api.client.parameters import Parameters
from grazie.api.client.profiles import LLMProfile, Profile
from grazie.api.client.qna.request import PrioritizedSource
from grazie.api.client.qna.response import AnswerStreamV2, RetrieveResponse
from grazie.api.client.quota.response import Quota, QuotaResponse
from grazie.api.client.v8.chat.response import (
    ChatContentStreamChunk,
    ChatFinishMetadataResponse,
)
from grazie.api.client.v8.chat.response import ChatPrompt as ChatPromptV8
from grazie.api.client.v8.chat.response import ChatResponse as ChatResponseV8
from grazie.api.client.v8.chat.response import (
    ChatResponseStream as ChatResponseStreamV8,
)
from grazie.api.client.v8.chat.response import (
    ChatSingleResponse,
    ChatToolCallStreamChunk,
    ChatToolResponse,
    IndexableStreamChunk,
)
from grazie.api.client.v8.completion.prompt import (
    CompletionPrompt as CompletionPromptV8,
)
from grazie.api.client.v8.completion.response import (
    CompletionContentStreamChunk,
    CompletionFinishMetadataResponse,
)
from grazie.api.client.v8.completion.response import (
    CompletionResponse as CompletionResponseV8,
)
from grazie.api.client.v8.completion.response import CompletionResponseStream
from grazie.api.client.v8.llm_parameters import LLMParameters as LLMParametersV8
from grazie.api.client.v8.parameters import Parameters as ParametersV8

G_LOG = logging.getLogger(__name__)


@attrs.define(auto_attribs=True, frozen=True)
class GrazieAgent:
    name: str
    version: str


class GrazieHeaders(str, Enum):
    AUTH_TOKEN = "Grazie-Authenticate-JWT"
    ORIGINAL_USER_TOKEN = "Grazie-Original-User-JWT"
    ORIGINAL_APPLICATION_TOKEN = "Grazie-Original-Application-JWT"
    ORIGINAL_SERVICE_TOKEN = "Grazie-Original-Service-JWT"
    ORIGINAL_USER_IP = "Grazie-Original-User-IP"
    AGENT = "Grazie-Agent"
    QUOTA_METADATA = "Grazie-Quota-Metadata"


class AuthType(str, Enum):
    SERVICE = "service"
    USER = "user"
    APPLICATION = "application"


class SseResponseParseException(Exception):
    """Exception occurring during parsing of sse response.

    Can occur, for example, if api gets changed without client update."""


class RequestFailedException(Exception):
    """Exception which occurs when we receive non 200 response code from api gateway."""


class GrazieApiGatewayClient:
    def __init__(
        self,
        grazie_agent: GrazieAgent = GrazieAgent(name="default", version="dev"),
        url: str = GrazieApiGatewayUrls.PRODUCTION,
        auth_type: AuthType = AuthType.SERVICE,
        grazie_jwt_token: Optional[str] = None,
    ):
        """Creates and instance of a gateway client.

        Parameters
        ----------
        grazie_agent: meaningful identifier of the application or user which is using the api.
          It can later be used to calculate statistics on the server side, so make sure to set the correct version and update it accordingly.
          If you don't care about statistics, just use "dev" as a version, i.e. GrazieAgent(name="llm-eval", version="dev")
        url: address of the service, default points to staging, to get prod one, replace stgn with prod in url.
        auth_type: authorization type which should be set to service if you write a service, it's fine to use user for local testing and evaluation.
        grazie_jwt_token: JWT token which is used for authorization, user token can be obtained with Grazie Playground (try.ai.intellij.net).
          If you write an application and need service auth_type, contact Vladislav Tankov and he will issue the service token.
        """
        if grazie_jwt_token is None and "GRAZIE_JWT_TOKEN" not in os.environ:
            if "GRAZIE_USER_JWT_TOKEN" in os.environ:
                auth_type = AuthType.USER
            elif "GRAZIE_SERVICE_JWT_TOKEN" in os.environ:
                auth_type = AuthType.SERVICE
            else:
                raise ValueError(
                    """
                    Cannot set jwt token. Either pass it as a constructor param or set GRAZIE_JWT_TOKEN environment variable.
                    You can obtain user jwt token by going to https://play.stgn.grazie.ai/ and copying it by pressing a button in a top left corner.
                """
                )

        self._api_gateway_url = url
        self._auth_type = auth_type
        self._grazie_jwt_token = (
            grazie_jwt_token
            or os.environ.get("GRAZIE_JWT_TOKEN")
            or os.environ.get("GRAZIE_USER_JWT_TOKEN")
            or os.environ["GRAZIE_SERVICE_JWT_TOKEN"]
        )
        self._grazie_agent = json.dumps(attrs.asdict(grazie_agent))
        self.v8 = self.Ver8(self)

    def _generate_headers(self, user_headers: Optional[Dict[str, str]] = None):
        return {
            GrazieHeaders.AUTH_TOKEN: self._grazie_jwt_token,
            GrazieHeaders.AGENT: self._grazie_agent,
            "Content-Type": "application/json",
            **(user_headers if user_headers else {}),
        }

    def complete(
        self,
        prompt: CompletionPromptV3,
        profile: LLMProfile,
        parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> CompletionResponseV3:
        chunks: List[str] = []
        for stream_response in self.complete_stream(
            prompt, profile=profile, parameters=parameters, headers=headers
        ):
            chunks.append(stream_response.chunk)

        return CompletionResponseV3(prompt=prompt, completion="".join(chunks))

    def complete_stream(
        self,
        prompt: CompletionPromptV3,
        profile: LLMProfile,
        parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[CompletionResponseStreamV3]:
        request_data: Dict[str, Any] = {
            "prompt": prompt.message,
            "profile": profile.name,
            "postfix": prompt.suffix,
        }

        if parameters:
            request_data["parameters"] = self._create_parameters_json(parameters, profile)

        response = requests.post(
            f"{self._api_gateway_url}/{self._auth_type.value}/v5/llm/complete/stream/v3",
            headers=self._generate_headers(headers),
            json=request_data,
            timeout=300,
            stream=True,
        )

        self._raise_if_error(response)

        for chunk in _decode_llm_sse(
            self._parse_sse_response(response.iter_lines()), LLMCompleteEventV3
        ):
            yield CompletionResponseStreamV3(chunk=chunk.current)

    def chat(
        self,
        chat: ChatPromptV6,
        profile: LLMProfile,
        prompt_id: str = "unknown",
        parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ChatResponseV6:
        """
        Calls chat api endpoint

        :param chat: chat history, usually ending with user message, some models also support system messages
        :param profile: which model to use, i.e., chatGPT, Vicuna, ...
        :param prompt_id: id of your prompt or feature which can be used to track expenses
        :param parameters: parameters to use during generation, supported parameters are located in LLMParameters
        Example:
            self.chat(
                chat=ChatPrompt()
                    .add_system("You are a helpful assistant.")
                    .add_user("Who won the world series in 2020?"),
                profile=Profile.OPENAI_CHAT_GPT,
                prompt_id="my-world-series-app",
                parameters={
                    LLMParameters.Temperature: Parameters.FloatValue(0.0)
                }
            )
        """
        function_call = None
        updated = None
        spent = None

        chunks: List[ChatResponseStreamV6] = []
        for stream_response in self.chat_stream(
            chat,
            profile=profile,
            prompt_id=prompt_id,
            parameters=parameters,
            headers=headers,
        ):
            chunks.append(stream_response)
            if stream_response.function_call:
                function_call = stream_response.function_call
            if stream_response.updated:
                updated = stream_response.updated
            if stream_response.spent:
                spent = stream_response.spent

        return ChatResponseV6(
            prompt=chat,
            content="".join(c.chunk for c in chunks),
            function_call=function_call,
            updated=updated,
            spent=spent,
        )

    def chat_stream(
        self,
        chat: ChatPromptV6,
        profile: LLMProfile,
        prompt_id: str = "unknown",
        parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[MutableMapping[str, str]] = None,
    ) -> Iterator[ChatResponseStreamV6]:
        """
        Calls chat api endpoint in a streaming mode.

        :param chat: chat history, usually ending with user message, some models also support system messages
        :param profile: which model to use, i.e., chatGPT, Vicuna, ...
        :param prompt_id: id of your prompt or feature which can be used to track expenses
        :param parameters: parameters to use during generation, supported parameters are located in LLMParameters
        Example:
            self.chat_stream(
                chat=ChatPrompt()
                    .add_system("You are a helpful assistant.")
                    .add_user("Who won the world series in 2020?"),
                profile=Profile.OPENAI_CHAT_GPT,
                prompt_id="my-world-series-app",
                parameters={
                    LLMParameters.Temperature: Parameters.FloatValue(0.0)
                }
            )
        """
        request_data: Dict[str, Any] = {
            "chat": {"messages": chat.get_messages()},
            "prompt": prompt_id,
            "profile": profile.name,
        }

        if parameters:
            request_data["parameters"] = self._create_parameters_json(parameters, profile)

        response = requests.post(
            url=f"{self._api_gateway_url}/{self._auth_type.value}/v5/llm/chat/stream/v6",
            headers=self._generate_headers(headers),
            json=request_data,
            timeout=300,
            stream=True,
            proxies=proxies,
        )

        self._raise_if_error(response)

        for event in _decode_llm_sse(
            self._parse_sse_response(response.iter_lines()), LLMChatEventV6
        ):
            event: LLMChatEventV6

            if event.type is LLMChatEventTypeV6.Content:
                yield ChatResponseStreamV6(chunk=event.content)
            elif event.type is LLMChatEventTypeV6.FunctionCall:
                yield ChatResponseStreamV6(chunk=event.content, function_call=event.name)
            elif event.type is LLMChatEventTypeV6.QuotaMetadata:
                yield ChatResponseStreamV6(chunk="", spent=event.spent, updated=event.updated)
            else:
                raise ValueError(f"Unsupported event type {event.type!r}")

    def quota(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, Quota]:
        with requests.Session() as s:
            s.mount(
                f"{self._api_gateway_url}",
                HTTPAdapter(
                    max_retries=Retry(
                        3,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504],
                    )
                ),
            )
            response = requests.post(
                f"{self._api_gateway_url}/{self._auth_type.value}/v5/quota/get",
                headers=self._generate_headers(headers),
                timeout=300,
            )

        self._raise_if_error(response)
        return {q_name: Quota(**q) for q_name, q in response.json().items()}

    def embed(
        self, request: EmbeddingRequest, headers: Optional[Dict[str, str]] = None
    ) -> EmbeddingResponse:
        request_options = []
        if request.format_cbor:
            request_options.append("format=cbor")
        if request.normalize:
            request_options.append("normalize=true")
        request_data: Dict[str, Any] = {
            "texts": request.texts,
            "options": request_options,
        }
        if request.model:
            request_data["model"] = request.model
        with requests.Session() as s:
            s.mount(
                f"{self._api_gateway_url}",
                HTTPAdapter(
                    max_retries=Retry(
                        3,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504],
                    )
                ),
            )
            response = requests.post(
                f"{self._api_gateway_url}/{self._auth_type.value}/v5/meta/emb/embed",
                headers=self._generate_headers(headers),
                json=request_data,
                timeout=300,
            )

        self._raise_if_error(response)

        body: Dict
        if response.headers["Content-Type"] == "application/cbor":
            body = cbor2.loads(response.content)
        else:
            body = json.loads(response.content)
        embeddings = [e["values"] for e in body["embeddings"]]
        return EmbeddingResponse(embeddings=embeddings)

    def llm_embed(
        self, request: LLMEmbeddingRequest, headers: Optional[Dict[str, str]] = None
    ) -> EmbeddingResponse:
        request_data: Dict[str, Any] = {"texts": request.texts, "profile": request.profile.name}

        if request.dimensions:
            parameters: Dict[Parameters.Key, Parameters.Value] = {
                LLMParametersV6.Dimension: Parameters.IntValue(request.dimensions)
            }
            request_data["parameters"] = self._create_parameters_json(parameters, request.profile)

        with requests.Session() as s:
            s.mount(
                f"{self._api_gateway_url}",
                HTTPAdapter(
                    max_retries=Retry(
                        3, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504]
                    )
                ),
            )
            response = requests.post(
                f"{self._api_gateway_url}/{self._auth_type.value}/v5/llm/embedding/v2",
                headers=self._generate_headers(headers),
                json=request_data,
                timeout=300,
            )

        self._raise_if_error(response)

        body: Dict[str, List[Dict]] = cbor2.loads(response.content)
        embeddings = [e["values"] for e in body["embeddings"]]

        return EmbeddingResponse(embeddings=embeddings)

    def retrieve(
        self,
        query: str,
        data_source: str,
        profile: Optional[LLMProfile] = None,
        size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> RetrieveResponse:
        request_data: Dict[str, Any] = {
            "query": query,
            "dataSource": data_source,
        }
        if size is not None:
            request_data["size"] = size
        if profile is not None:
            request_data["llmProfile"] = profile.name

        with requests.Session() as s:
            s.mount(
                f"{self._api_gateway_url}",
                HTTPAdapter(
                    max_retries=Retry(
                        3, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504]
                    )
                ),
            )
            response = requests.post(
                url=f"{self._api_gateway_url}/{self._auth_type.value}/v5/meta/qa/retrieve/v1",
                headers=self._generate_headers(headers),
                json=request_data,
                timeout=300,
                stream=True,
            )

        self._raise_if_error(response)

        body: Dict[str, List[Dict]] = json.loads(response.content)
        return RetrieveResponse(documents=body["documents"])

    def retrieve_v2(
        self,
        query: str,
        config_name: str,
        data_source_lists: List[List[PrioritizedSource]],
        profile: Optional[LLMProfile] = None,
        size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> RetrieveResponse:
        request_data: Dict[str, Any] = {
            "query": query,
            "config": config_name,
            "prioritizedSources": [
                [attrs.asdict(source) for source in source_list]
                for source_list in data_source_lists
            ],
        }
        if size is not None:
            request_data["size"] = size
        if profile is not None:
            request_data["llmProfile"] = profile.name

        with requests.Session() as s:
            s.mount(
                f"{self._api_gateway_url}",
                HTTPAdapter(
                    max_retries=Retry(
                        3, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504]
                    )
                ),
            )
            response = requests.post(
                url=f"{self._api_gateway_url}/{self._auth_type.value}/v5/meta/qa/retrieve/v2",
                headers=self._generate_headers(headers),
                json=request_data,
                timeout=300,
                stream=False,
            )

        self._raise_if_error(response)

        body: Dict[str, List[Dict]] = json.loads(response.content)
        return RetrieveResponse(documents=body["documents"])

    def answer_stream(
        self,
        query: str,
        data_source: str,
        profile: LLMProfile = Profile.OPENAI_GPT_4_TURBO,
        size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[AnswerStreamV2]:
        request_data: Dict[str, Any] = {
            "query": query,
            "dataSource": data_source,
            "llmProfile": profile.name,
        }
        if size is not None:
            request_data["size"] = size

        response = requests.post(
            url=f"{self._api_gateway_url}/{self._auth_type.value}/v5/meta/qa/answer/v2",
            headers=self._generate_headers(headers),
            json=request_data,
            timeout=300,
            stream=True,
        )

        yield from _decode_llm_sse(self._parse_sse_response(response.iter_lines()), AnswerStreamV2)

    def _raise_if_error(self, response: requests.Response):
        if response.status_code != 200:
            raise RequestFailedException(
                f"{response.status_code} Error: {response.reason}. {response.text}"
            )

    @staticmethod
    def _create_parameters_json(
        parameters: Dict[Parameters.Key, Parameters.Value], llm_profile: LLMProfile
    ) -> Dict[str, Any]:
        return {"data": Parameters.serialize(parameters)}

    @staticmethod
    def _parse_sse_response(lines: Iterable[bytes]) -> Iterable[Dict[str, Any]]:
        for line in lines:
            line = line.decode()
            if len(line.strip()) == 0:
                continue

            if not line.startswith("data:"):
                raise SseResponseParseException(
                    "Got non-data part in sse response. The client should be updated to the latest api version."
                )

            content = line[5:].strip()
            if content == "end":
                return

            content_data = json.loads(content)

            event_type = content_data["event_type"]
            if event_type == "data":
                content_data.pop("event_type")
                yield content_data
            elif event_type == "error":
                error_message = f"Server error"
                if "error_message" in content_data:
                    error_message += error_message + ": " + content_data["error_message"]
                raise RequestFailedException(error_message)
            else:
                raise SseResponseParseException(
                    f"Expected all data parts of sse response to be of event_type data or error, but got {event_type}. "
                    "The client should be updated to the latest api version."
                )

        raise SseResponseParseException(
            'Expected "data: end" at the end of response, but not found.'
        )

    class Ver8:
        def __init__(self, parent):
            self._parent = parent

        def profiles(self, headers: Optional[Dict[str, str]] = None):
            response = requests.get(
                url=f"{self._parent._api_gateway_url}/{self._parent._auth_type.value}/v5/llm/profiles/v8",
                headers=self._parent._generate_headers(headers),
                timeout=300,
            )
            response.raise_for_status()
            return response.json()

        def chat(
            self,
            chat: ChatPromptV8,
            profile: LLMProfile,
            prompt_id: str = "unknown",
            parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
            headers: Optional[Dict[str, str]] = None,
        ) -> ChatResponseV8:
            """
            Calls chat api endpoint

            :param chat: chat history, usually ending with user message, some models also support system messages
            :param profile: which model to use, i.e., chatGPT, Vicuna, ...
            :param prompt_id: id of your prompt or feature which can be used to track expenses
            :param parameters: parameters to use during generation, supported parameters are located in LLMParameters
            Example:
                self.chat(
                    chat=ChatPrompt()
                        .add_system("You are a helpful assistant.")
                        .add_user("Who won the world series in 2020?"),
                    profile=Profile.OPENAI_CHAT_GPT,
                    prompt_id="my-world-series-app",
                    parameters={
                        LLMParameters.Temperature: Parameters.FloatValue(0.0)
                    }
                )
            """
            indexable_chunks: List[IndexableStreamChunk] = []
            responses: List[ChatSingleResponse] = []
            quota: QuotaResponse = QuotaResponse()
            unknown_metadata = None

            for stream_response in self.chat_stream(
                chat,
                profile=profile,
                prompt_id=prompt_id,
                parameters=parameters,
                headers=headers,
            ):
                if isinstance(stream_response, IndexableStreamChunk):
                    indexable_chunks.append(stream_response)
                elif isinstance(stream_response, QuotaResponse):
                    quota = stream_response
                elif isinstance(stream_response, UnknownMetadataResponse):
                    unknown_metadata = stream_response
                else:
                    raise ValueError(f"Unsupported stream chunk type {type(stream_response)}")

            has_multiple_choices = (
                parameters
                and LLMParametersV8.NumberOfChoices in parameters
                and parameters[LLMParametersV8.NumberOfChoices].value > 1  # pyright: ignore
            )

            if has_multiple_choices:
                choices: Dict[int, List[IndexableStreamChunk]] = defaultdict(list)

                for chunk in indexable_chunks:
                    if chunk.choiceIndex is not None:
                        choices[chunk.choiceIndex].append(chunk)
                for choice in choices.values():
                    responses.append(build_single_response(choice))
            else:
                responses = [build_single_response(indexable_chunks)]

            return ChatResponseV8(
                responses=responses,
                prompt=chat,
                quota=quota,
                unknown_metadata=unknown_metadata,
            )

        def chat_stream(
            self,
            chat: ChatPromptV8,
            profile: LLMProfile,
            prompt_id: str = "unknown",
            parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
            headers: Optional[Dict[str, str]] = None,
            proxies: Optional[MutableMapping[str, str]] = None,
        ) -> Iterator[ChatResponseStreamV8]:
            """
            Calls chat api endpoint in a streaming mode.

            :param chat: chat history, usually ending with user message, some models also support system messages
            :param profile: which model to use, i.e., chatGPT, Vicuna, ...
            :param prompt_id: id of your prompt or feature which can be used to track expenses
            :param parameters: parameters to use during generation, supported parameters are located in LLMParameters
            Example:
                self.chat_stream(
                    chat=ChatPrompt()
                        .add_system("You are a helpful assistant.")
                        .add_user("Who won the world series in 2020?"),
                    profile=Profile.OPENAI_CHAT_GPT,
                    prompt_id="my-world-series-app",
                    parameters={
                        LLMParameters.Temperature: Parameters.FloatValue(0.0)
                    }
                )
            """
            request_data: Dict[str, Any] = {
                "chat": {"messages": chat.get_messages()},
                "prompt": prompt_id,
                "profile": profile.name,
            }

            if parameters:
                request_data["parameters"] = self._create_parameters_json(parameters, profile)

            response = requests.post(
                url=f"{self._parent._api_gateway_url}/{self._parent._auth_type.value}/v5/llm/chat/stream/v8",
                headers=self._parent._generate_headers(headers),
                json=request_data,
                timeout=300,
                stream=True,
                proxies=proxies,
            )

            self._parent._raise_if_error(response)

            for event in self._parent._parse_sse_response(response.iter_lines()):
                event_type = event.pop("type")

                if event_type == "Content":
                    yield ChatContentStreamChunk(**event)
                elif event_type == "ToolCall":
                    yield ChatToolCallStreamChunk(**event)
                elif event_type == "FinishMetadata":
                    yield ChatFinishMetadataResponse(**event)
                elif event_type == "QuotaMetadata":
                    yield QuotaResponse(**event)
                elif event_type == "UnknownMetadata":
                    yield UnknownMetadataResponse(**event)
                else:
                    raise ValueError(f"Unsupported event type {event_type}")

        def complete(
            self,
            profile: LLMProfile,
            prompt: CompletionPromptV8,
            prompt_id: str = "unknown",
            parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
            headers: Optional[Dict[str, str]] = None,
        ) -> CompletionResponseV8:
            warnings.warn(
                "Deprecated: Usage of `complete` endpoint is discouraged. Use `chat` instead to get chat completion.",
                DeprecationWarning,
                stacklevel=2,
            )
            content: List[str] = []
            stop_reason: Optional[str] = None
            quota: QuotaResponse = QuotaResponse()
            unknown_metadata = None

            for stream_response in self.complete_stream(
                profile=profile,
                prompt=prompt,
                prompt_id=prompt_id,
                parameters=parameters,
                headers=headers,
            ):
                if isinstance(stream_response, CompletionContentStreamChunk):
                    content.append(stream_response.content)
                elif isinstance(stream_response, CompletionFinishMetadataResponse):
                    stop_reason = stream_response.reason
                elif isinstance(stream_response, QuotaResponse):
                    quota = stream_response
                elif isinstance(stream_response, UnknownMetadataResponse):
                    unknown_metadata = stream_response
                else:
                    raise ValueError(f"Unsupported stream chunk type {type(stream_response)}")

            return CompletionResponseV8(
                prompt=prompt,
                content="".join(content),
                stop_reason=stop_reason,
                quota=quota,
                unknown_metadata=unknown_metadata,
            )

        def complete_stream(
            self,
            profile: LLMProfile,
            prompt: CompletionPromptV8,
            prompt_id: str = "unknown",
            parameters: Optional[Dict[Parameters.Key, Parameters.Value]] = None,
            headers: Optional[Dict[str, str]] = None,
        ) -> Iterator[CompletionResponseStream]:
            warnings.warn(
                "Deprecated: Usage of `complete_stream` endpoint is discouraged. Use `chat_stream` instead to get chat completion stream.",
                DeprecationWarning,
                stacklevel=2,
            )

            request_data: Dict[str, Any] = {
                "prompt": prompt_id,
                "prefix": prompt.prefix,
                "suffix": prompt.suffix,
                "profile": profile.name,
            }

            if parameters:
                request_data["parameters"] = self._create_parameters_json(parameters, profile)

            response = requests.post(
                f"{self._parent._api_gateway_url}/{self._parent._auth_type.value}/v5/llm/complete/stream/v8",
                headers=self._parent._generate_headers(headers),
                json=request_data,
                timeout=300,
                stream=True,
            )

            self._parent._raise_if_error(response)

            for event in self._parent._parse_sse_response(response.iter_lines()):
                event_type = event.pop("type")

                if event_type == "Content":
                    yield CompletionContentStreamChunk(**event)
                elif event_type == "FinishMetadata":
                    yield CompletionFinishMetadataResponse(**event)
                elif event_type == "QuotaMetadata":
                    yield QuotaResponse(**event)
                elif event_type == "UnknownMetadata":
                    yield UnknownMetadataResponse(**event)
                else:
                    raise ValueError(f"Unsupported event type {event_type}")

        @staticmethod
        def _create_parameters_json(
            parameters: Dict[ParametersV8.Key, ParametersV8.Value], llm_profile: LLMProfile
        ) -> Dict[str, Any]:
            return {"data": ParametersV8.serialize(parameters)}


T = TypeVar("T", LLMChatEventV6, LLMChatEventV5, LLMCompleteEventV3, AnswerStreamV2)


def _decode_llm_sse(events: Iterable[Dict[str, Any]], response_type: Type[T]) -> Iterable[T]:
    yield from (response_type(**event) for event in events)


def build_single_response(chunks: List[IndexableStreamChunk]) -> ChatSingleResponse:
    def get_first_or_none(chunks, attr_name):
        return next(
            (getattr(item, attr_name) for item in chunks if bool(getattr(item, attr_name, None))),
            None,
        )

    def aggregate_stream_responses(tool_chunks: List[ChatToolCallStreamChunk]) -> ChatToolResponse:
        content = "".join(chunk.content for chunk in tool_chunks)

        tool_id = get_first_or_none(tool_chunks, "id")
        tool_name = get_first_or_none(tool_chunks, "name")
        parallel_tool_index = get_first_or_none(tool_chunks, "parallelToolIndex")

        return ChatToolResponse(
            id=tool_id,
            name=tool_name,
            content=content,
            parallelToolIndex=parallel_tool_index,
        )

    text_chunks = [chunk for chunk in chunks if isinstance(chunk, ChatContentStreamChunk)]
    tool_chunks = [chunk for chunk in chunks if isinstance(chunk, ChatToolCallStreamChunk)]
    stop_reason = next(
        (chunk.reason for chunk in chunks if isinstance(chunk, ChatFinishMetadataResponse)), None
    )

    text = "".join(chunk.content for chunk in text_chunks) if text_chunks else None

    if tool_chunks:
        if all(hasattr(chunk, "parallelToolIndex") for chunk in tool_chunks):
            grouped_chunks: Dict[int, List[ChatToolCallStreamChunk]] = defaultdict(list)
            for chunk in tool_chunks:
                if chunk.parallelToolIndex is not None:
                    grouped_chunks[chunk.parallelToolIndex].append(chunk)
            tool_calls = [aggregate_stream_responses(group) for group in grouped_chunks.values()]
        else:
            tool_calls = [aggregate_stream_responses(tool_chunks)]
    else:
        tool_calls = []

    return ChatSingleResponse(content=text, tool_calls=tool_calls, stop_reason=stop_reason)
