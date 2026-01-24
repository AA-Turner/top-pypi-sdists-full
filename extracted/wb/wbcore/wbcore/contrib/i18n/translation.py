from copy import deepcopy
from typing import TYPE_CHECKING, Any, Iterator

from celery import shared_task
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Field
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from modeltrans.fields import TranslatedVirtualField

from wbcore.contrib.ai.llm.utils import run_llm
from wbcore.workers import Queue

if TYPE_CHECKING:
    from django.db.models import Model


def get_base_prompt(from_language: str, to_language: str) -> list["BaseMessage"]:
    """
    Creates a base prompt for translation with system instructions.

    Args:
        from_language: ISO2 code of the source language
        to_language: ISO2 code of the target language

    Returns:
        list[BaseMessage]: A list containing the system message for translation
    """
    return [
        SystemMessage(f"""
    You are a highly skilled translator with expertise in accurately translating content between languages.
    Your task is to translate the provided content from ISO2={from_language} to ISO2={to_language}.

    Please adhere to the following guidelines:
    - Maintain the original meaning, tone, and style of the content.
    - Preserve any formatting, including line breaks and special characters.
    - Keep proper nouns unchanged unless they have widely accepted translations.
    - Do not add, remove, or alter any information in the content.
    - Provide only the translated text without any additional explanations or notes.
    """)
    ]


def _is_translated_field(field: Field | TranslatedVirtualField) -> bool:
    """
    Determines if a field is a translated field that needs processing.

    Args:
        field: The field to check

    Returns:
        bool: True if the field is a TranslatedVirtualField with a non-default language
    """
    return (
        isinstance(field, TranslatedVirtualField)
        and field.language is not None
        and field.language != settings.LANGUAGE_CODE
    )


def _get_translation_fields(
    fields: list[Field | TranslatedVirtualField | Any],
) -> Iterator[TranslatedVirtualField]:
    """
    Filters a list of fields to only include translated fields.

    Args:
        fields: List of model fields to filter

    Returns:
        Iterator[TranslatedVirtualField]: Iterator yielding only the translated virtual fields
    """
    yield from filter(_is_translated_field, fields)  # type: ignore


def translate_string(content: str, language: str) -> str:
    prompt = get_base_prompt(settings.LANGUAGE_CODE, language)
    prompt.append(HumanMessage(content))
    return str(run_llm(prompt)[0])


def translate_dict(content: dict, language: str) -> dict:
    new_content = deepcopy(content)

    for key, value in content.items():
        if isinstance(value, dict):
            new_content[key] = translate_dict(value, language)
        elif isinstance(value, str):
            new_content[key] = translate_string(value, language)

    return new_content


def translate_model(model: "Model", override: bool = False):
    """
    Translates all translatable fields in a model instance.

    Processes all fields in the model that are marked for translation,
    generates translations using an LLM, and saves the model with
    the translated content.

    Args:
        model: The Django model instance to translate
        override: If True, do not set the translated value if there is already content
    """
    for field in _get_translation_fields(model._meta.get_fields()):
        original_content = getattr(model, field.original_field.name)
        if field.language is None or (field is not None and not override):
            continue

        if custom_translation := getattr(model, f"_translate_{field.original_field.name}", None):
            setattr(model, field.name, custom_translation(field.language))
        else:
            match original_content:
                case str():
                    setattr(
                        model,
                        field.name,
                        translate_string(original_content, field.language),
                    )
                case dict():
                    setattr(model, field.name, translate_dict(original_content, field.language))

    model.save()


@shared_task(queue=Queue.DEFAULT.value)
def translate_model_as_task(content_type_id: int, pk: Any, override: bool = False):
    """
    Celery task for asynchronous translation of a model instance.

    Retrieves the model class from the content type ID, loads the
    specific instance by primary key, and translates its fields.

    Args:
        content_type_id: ID of the ContentType for the model to translate
        pk: Primary key of the specific model instance to translate
    """
    if mc := ContentType.objects.get(id=content_type_id).model_class():
        model = mc.objects.get(pk=pk)
        translate_model(model, override)
