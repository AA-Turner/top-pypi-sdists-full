# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .shared_params.model_parameters import ModelParameters

__all__ = [
    "CompletionCreateParamsBase",
    "Image",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[
        Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ]
    ]
    """The ID of the model to use for completions.

    Users have two options:

    - Option 1: Use one of the supported models from the dropdown.
    - Option 2: Enter the ID of a custom model.

    Note: For custom models we currently only support models finetuned using using
    the Scale-hosted LLM-Engine API.
    """

    prompt: Required[str]
    """Prompt for which to generate the completion.

    Good prompt engineering is crucial to getting performant results from the model.
    If you are having trouble getting the model to perform well, try writing a more
    specific prompt here before trying more expensive techniques such as swapping in
    other models or finetuning the underlying LLM.
    """

    account_id: str
    """The account ID to use for usage tracking. This will be gradually enforced."""

    images: Iterable[Image]
    """List of image urls to be used for image based completions.

    Leave empty for text based completions.
    """

    model_parameters: ModelParameters
    """
    Configuration parameters for the completion model, such as temperature,
    max_tokens, and stop_sequences.

    If not specified, the default value are:

    - temperature: 0.2
    - max_tokens: None (limited by the model's max tokens)
    - stop_sequences: None
    """


class Image(TypedDict, total=False):
    image_url: Required[str]
    """Image URL to run image completion on."""

    detail: str
    """Detail to run image completion with. Defaults to auto"""


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
