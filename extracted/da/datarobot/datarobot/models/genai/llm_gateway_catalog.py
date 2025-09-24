#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot._compat import TypedDict
from datarobot.models.api_object import APIObject
from datarobot.utils import from_api
from datarobot.utils.pagination import unpaginate


class LLMReferenceDict(TypedDict):
    """Dict representation of LlmReference."""

    name: str
    url: Optional[str]


class LLMGatewayCatalogEntryDict(TypedDict):
    """Dict representation of LlmGatewayCatalogEntry."""

    model: str
    llm_id: str
    name: str
    description: str
    provider: str
    creator: str
    context_size: int
    max_completion_tokens: int
    capabilities: Optional[List[str]]
    supported_languages: List[str]
    input_types: List[str]
    output_types: List[str]
    parameters: Dict[str, Any]
    documentation_link: str
    reference_links: List[LLMReferenceDict]
    date_added: date
    license: str
    is_preview: bool
    is_metered: bool
    retirement_date: Optional[date]
    suggested_replacement: Optional[str]
    is_deprecated: bool
    is_active: bool
    available_regions: List[str]


llm_reference_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("url", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

llm_gateway_catalog_entry_trafaret = t.Dict(
    {
        t.Key("model"): t.String,
        t.Key("llm_id"): t.String,
        t.Key("name"): t.String,
        t.Key("description"): t.String,
        t.Key("provider"): t.String,
        t.Key("creator"): t.String,
        t.Key("context_size"): t.Int,
        t.Key("max_completion_tokens"): t.Int,
        t.Key("capabilities", optional=True): t.Or(t.List(t.String), t.Null),
        t.Key("supported_languages"): t.List(t.String),
        t.Key("input_types"): t.List(t.String),
        t.Key("output_types"): t.List(t.String),
        t.Key("parameters"): t.Dict({}).allow_extra("*"),
        t.Key("documentation_link"): t.String,
        t.Key("reference_links"): t.List(llm_reference_trafaret),
        t.Key("date_added"): t.String,
        t.Key("license"): t.String,
        t.Key("is_preview"): t.Bool,
        t.Key("is_metered"): t.Bool,
        t.Key("retirement_date", optional=True): t.Or(t.String, t.Null),
        t.Key("suggested_replacement", optional=True): t.Or(t.String, t.Null),
        t.Key("is_deprecated"): t.Bool,
        t.Key("is_active"): t.Bool,
        t.Key("available_regions"): t.List(t.String),
    }
).ignore_extra("*")


class LLMReference(APIObject):
    """
    Reference link for an LLM.

    Attributes
    ----------
    name : str
        Description of the reference document.
    url : str or None
        URL of the reference document.
    """

    _converter = llm_reference_trafaret

    def __init__(self, name: str, url: Optional[str] = None):
        self.name = name
        self.url = url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def to_dict(self) -> LLMReferenceDict:
        return {"name": self.name, "url": self.url}


class LLMGatewayCatalogEntry(APIObject):
    """
    Metadata for an LLM Gateway catalog entry.

    Attributes
    ----------
    model : str
        The identifier of the model to use for chat completion.
    llm_id : str
        The internal identifier of the LLM.
    name : str
        The name of the LLM.
    description : str
        The description of the LLM.
    provider : str
        The name of the LLM provider.
    creator : str
        The creator of the LLM.
    context_size : int
        The context size of the LLM.
    max_completion_tokens : int
        The maximum number of tokens the LLM can generate.
    capabilities : list of str or None
        The capabilities of the LLM.
    supported_languages : list of str
        The languages supported by the LLM.
    input_types : list of str
        The input types supported by the LLM.
    output_types : list of str
        The supported output types by the LLM.
    parameters : dict
        The supported LLM completion parameters.
    documentation_link : str
        The link to the LLM documentation.
    reference_links : list of LlmReference
        The reference links.
    date_added : date
        The date the LLM was added to the catalog.
    license : str
        The license of the LLM.
    is_preview : bool
        Whether the LLM is part of fast-track LLMs.
    is_metered : bool
        Whether the LLM is metered for consumption-based pricing.
    retirement_date : date or None
        The date the LLM was/will be retired.
    suggested_replacement : str or None
        The suggested replacement for the LLM.
    is_deprecated : bool
        Whether the LLM is deprecated.
    is_active : bool
        Whether the LLM is active.
    available_regions : list of str
        The regions where the LLM is available.
    """

    _converter = llm_gateway_catalog_entry_trafaret

    def __init__(
        self,
        model: str,
        llm_id: str,
        name: str,
        description: str,
        provider: str,
        creator: str,
        context_size: int,
        max_completion_tokens: int,
        supported_languages: List[str],
        input_types: List[str],
        output_types: List[str],
        parameters: Dict[str, Any],
        documentation_link: str,
        reference_links: List[Dict[str, Any]],
        date_added: str,
        license: str,
        is_preview: bool,
        is_metered: bool,
        is_deprecated: bool,
        is_active: bool,
        available_regions: List[str],
        capabilities: Optional[List[str]] = None,
        retirement_date: Optional[str] = None,
        suggested_replacement: Optional[str] = None,
    ):
        self.model = model
        self.llm_id = llm_id
        self.name = name
        self.description = description
        self.provider = provider
        self.creator = creator
        self.context_size = context_size
        self.max_completion_tokens = max_completion_tokens
        self.capabilities = capabilities
        self.supported_languages = supported_languages
        self.input_types = input_types
        self.output_types = output_types
        self.parameters = parameters
        self.documentation_link = documentation_link
        self.reference_links = [LLMReference.from_server_data(ref) for ref in reference_links]
        self.date_added = (
            date.fromisoformat(date_added) if isinstance(date_added, str) else date_added
        )
        self.license = license
        self.is_preview = is_preview
        self.is_metered = is_metered
        self.retirement_date = date.fromisoformat(retirement_date) if retirement_date else None
        self.suggested_replacement = suggested_replacement
        self.is_deprecated = is_deprecated
        self.is_active = is_active
        self.available_regions = available_regions

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model}, name={self.name})"

    def to_dict(self) -> LLMGatewayCatalogEntryDict:
        return {
            "model": self.model,
            "llm_id": self.llm_id,
            "name": self.name,
            "description": self.description,
            "provider": self.provider,
            "creator": self.creator,
            "context_size": self.context_size,
            "max_completion_tokens": self.max_completion_tokens,
            "capabilities": self.capabilities,
            "supported_languages": self.supported_languages,
            "input_types": self.input_types,
            "output_types": self.output_types,
            "parameters": self.parameters,
            "documentation_link": self.documentation_link,
            "reference_links": [ref.to_dict() for ref in self.reference_links],
            "date_added": self.date_added,
            "license": self.license,
            "is_preview": self.is_preview,
            "is_metered": self.is_metered,
            "retirement_date": self.retirement_date,
            "suggested_replacement": self.suggested_replacement,
            "is_deprecated": self.is_deprecated,
            "is_active": self.is_active,
            "available_regions": self.available_regions,
        }


class LLMGatewayCatalog(APIObject):
    """
    LLM Gateway catalog management for listing and validating available LLMs.

    This class provides convenient methods for interacting with the LLM Gateway catalog,
    including filtering for active, non-deprecated models and validating model availability.
    """

    _path = "genai/llmgw/catalog/"

    @classmethod
    def list(
        cls,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        llm_id: Optional[str] = None,
        only_active: bool = True,
        only_non_deprecated: bool = True,
    ) -> List[LLMGatewayCatalogEntry]:
        """
        List LLMs available in the LLM Gateway catalog.

        Parameters
        ----------
        offset : int, optional
            Skip the specified number of values.
        limit : int, optional
            Retrieve only the specified number of values.
        llm_id : str, optional
            Get the catalog entries for a specific LLM ID.
        only_active : bool, default True
            If True, only return active LLMs.
        only_non_deprecated : bool, default True
            If True, only return non-deprecated LLMs.

        Returns
        -------
        list of LlmGatewayCatalogEntry
            A list of LLM Gateway catalog entries.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            # List all active, non-deprecated LLMs
            llms = dr.LlmGatewayCatalog.list()

            # List all LLMs (including deprecated and inactive)
            all_llms = dr.LlmGatewayCatalog.list(
                only_active=False,
                only_non_deprecated=False
            )

            # Get specific LLM
            gpt4_models = dr.LlmGatewayCatalog.list(llm_id="azure-openai-gpt-4")

            # Get as dictionaries instead
            llms_dict = dr.LlmGatewayCatalog.list_as_dict()
        """
        params: Dict[str, Union[int, str]] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if llm_id is not None:
            params["llmId"] = llm_id

        url = f"{cls._client.domain}/api/v2/{cls._path}"
        r_data = unpaginate(url, params, cls._client)

        # Create catalog entry objects
        catalog_entries = []
        for item in r_data:
            # Convert camelCase to snake_case for the constructor
            converted_data = from_api(item)
            catalog_entries.append(LLMGatewayCatalogEntry.from_server_data(converted_data))

        # Apply filtering
        if only_active:
            catalog_entries = [entry for entry in catalog_entries if entry.is_active]
        if only_non_deprecated:
            catalog_entries = [entry for entry in catalog_entries if not entry.is_deprecated]

        return catalog_entries

    @classmethod
    def list_as_dict(
        cls,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        llm_id: Optional[str] = None,
        only_active: bool = True,
        only_non_deprecated: bool = True,
    ) -> List[LLMGatewayCatalogEntryDict]:
        """
        List LLMs available in the LLM Gateway catalog as dictionaries.

        This is a type-safe version that returns dictionaries instead of objects.

        Parameters
        ----------
        offset : int, optional
            Skip the specified number of values.
        limit : int, optional
            Retrieve only the specified number of values.
        llm_id : str, optional
            Get the catalog entries for a specific LLM ID.
        only_active : bool, default True
            If True, only return active LLMs.
        only_non_deprecated : bool, default True
            If True, only return non-deprecated LLMs.

        Returns
        -------
        list of LlmGatewayCatalogEntryDict
            A list of LLM Gateway catalog entries as dictionaries.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            # Get as dictionaries for raw data access
            llms_dict = dr.LlmGatewayCatalog.list_as_dict()
            for llm in llms_dict:
                print(f"Model: {llm['model']}, Active: {llm['is_active']}")
        """
        entries = cls.list(
            offset=offset,
            limit=limit,
            llm_id=llm_id,
            only_active=only_active,
            only_non_deprecated=only_non_deprecated,
        )
        return [entry.to_dict() for entry in entries]

    @classmethod
    def get_available_models(
        cls,
        include_preview: bool = False,
        only_active: bool = True,
        only_non_deprecated: bool = True,
    ) -> List[str]:
        """
        Get a list of available model identifiers.

        Parameters
        ----------
        include_preview : bool, default False
            If True, include preview models.
        only_active : bool, default True
            If True, only return active models.
        only_non_deprecated : bool, default True
            If True, only return non-deprecated models.

        Returns
        -------
        list of str
            A list of available model identifiers.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            # Get production-ready models
            models = dr.LlmGatewayCatalog.get_available_models()

            # Get all models including preview
            all_models = dr.LlmGatewayCatalog.get_available_models(
                include_preview=True,
                only_active=False,
                only_non_deprecated=False
            )
        """
        catalog_entries = cls.list(
            only_active=only_active,
            only_non_deprecated=only_non_deprecated,
        )

        if not include_preview:
            catalog_entries = [entry for entry in catalog_entries if not entry.is_preview]

        return [entry.model for entry in catalog_entries]

    @classmethod
    def verify_model_availability(cls, model_id: str) -> LLMGatewayCatalogEntry:
        """
        Validate that a model is available and active in the catalog.

        Parameters
        ----------
        model_id : str
            The model identifier to validate. Can be either 'model' or 'llmId'.

        Returns
        -------
        LlmGatewayCatalogEntry
            The catalog entry for the validated model.

        Raises
        ------
        ValueError
            If the model is not found, not active, or is deprecated.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            # Validate a model is available
            try:
                model_entry = dr.LlmGatewayCatalog.verify_model_availability("azure-openai-gpt-4")
                print(f"Model {model_entry.name} is available")
            except ValueError as e:
                print(f"Model validation failed: {e}")
        """
        # Get all models (including inactive and deprecated for validation)
        all_models = cls.list(only_active=False, only_non_deprecated=False)

        # Find matching models by either model or llm_id
        matched_models = [model for model in all_models if model_id in (model.model, model.llm_id)]

        if not matched_models:
            # Get list of available models for error message
            available_models = cls.get_available_models(include_preview=True)
            model_list = "\n.   - ".join(available_models)
            raise ValueError(
                f"Model '{model_id}' not found in catalog. Available models: {model_list}"
            )

        if len(matched_models) > 1:
            raise ValueError(f"Multiple models found for '{model_id}' in catalog. {matched_models}")

        model_entry = matched_models[0]

        if not model_entry.is_active or model_entry.is_deprecated:
            # Get list of available models for error message
            available_models = cls.get_available_models(include_preview=True)
            model_list = "\n.   - ".join(available_models)
            raise ValueError(
                f"Model '{model_id}' is not active or is deprecated. Available models: {model_list}"
            )

        return model_entry

    @classmethod
    def get_model_by_id(cls, model_id: str) -> Optional[LLMGatewayCatalogEntry]:
        """
        Get a specific model by its identifier.

        Parameters
        ----------
        model_id : str
            The model identifier. Can be either 'model' or 'llmId'.

        Returns
        -------
        LlmGatewayCatalogEntry or None
            The catalog entry for the model, or None if not found.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            model_entry = dr.LlmGatewayCatalog.get_model_by_id("azure-openai-gpt-4")
            if model_entry:
                print(f"Found model: {model_entry.name}")
            else:
                print("Model not found")
        """
        try:
            model_entry = cls.verify_model_availability(model_id)
            return model_entry
        except ValueError:
            return None
