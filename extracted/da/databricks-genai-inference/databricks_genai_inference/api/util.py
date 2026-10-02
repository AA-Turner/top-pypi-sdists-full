"""Utils for the API.
"""
from enum import Enum

import httpx
import requests
from tenacity import retry, retry_if_result, stop_after_attempt, wait_random_exponential


class EmbeddingModel(Enum):
    """Supported embedding models.
    """
    BGE_LARGE_ENG = 'bge-large-en'


class CompletionModel(Enum):
    """Supported completion models.
    """
    MPT_7B_INSTRUCT = 'mpt-7b-instruct'
    MPT_30B_INSTRUCT = 'mpt-30b-instruct'


class ChatCompletionModel(Enum):
    """Supported chat completion models.
    """
    LLAMA_2_70B_CHAT = 'llama-2-70b-chat'
    MIXTRAL_8X7B_CHAT = 'mixtral-8x7b-instruct'
    DBRX_INSTRUCT = 'dbrx-instruct'


def send_request(client: requests.Session, url, headers, json, timeout):
    if client:
        return client.post(url=url, headers=headers, json=json, timeout=timeout)
    else:
        return requests.post(url=url, headers=headers, json=json, timeout=timeout)


async def asend_request(client: httpx.AsyncClient, url, headers, json, timeout):
    return await client.post(url=url, headers=headers, json=json, timeout=timeout)


def is_internal_server_error(response: requests.Response):
    return response.status_code >= 500
