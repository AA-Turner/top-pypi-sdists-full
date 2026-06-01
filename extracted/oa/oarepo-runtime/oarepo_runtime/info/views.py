#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see https://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Resource for serving machine-readable information about the repository."""

from __future__ import annotations

import importlib
import logging
import os
import re
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, cast
from urllib.parse import urljoin, urlparse, urlunparse

import marshmallow as ma
from flask import Blueprint, Flask, current_app, request, url_for
from flask_resources import (
    ResourceConfig,
    from_conf,
    request_parser,
    resource_requestctx,
    response_handler,
    route,
)
from flask_resources.resources import Resource as BaseResource
from invenio_base import invenio_url_for
from invenio_base.utils import obj_or_import_string
from invenio_jsonschemas import current_jsonschemas
from invenio_records_resources.proxies import (
    current_transfer_registry,
)
from werkzeug.routing import BuildError

from oarepo_runtime.proxies import current_runtime

if TYPE_CHECKING:
    from invenio_records.systemfields import ConstantField
    from invenio_records_resources.records.api import Record

    from oarepo_runtime import Model

logger = logging.getLogger("oarepo_runtime.info")


class InfoComponent(Protocol):
    """Info component protocol."""

    def __init__(self, resource: InfoResource) -> None:
        """Create the component."""

    def repository(self, data: dict) -> None:
        """Modify repository info endpoint data."""

    def model(self, data: list[dict]) -> None:
        """Modify model info endpoint data."""


class InfoConfig(ResourceConfig):
    """Info resource config."""

    blueprint_name = "oarepo_runtime_info"
    url_prefix = "/.well-known/repository"

    schema_view_args: ClassVar[dict[str, ma.fields.Str]] = {"schema": ma.fields.Str()}
    model_view_args: ClassVar[dict[str, ma.fields.Str]] = {"model": ma.fields.Str()}

    def __init__(self, app: Flask):
        """Initialize Info config."""
        self.app = app

    @cached_property
    def components(self) -> tuple[type[InfoComponent], ...]:
        """Get the components for the info resource from config."""
        return tuple(
            cast("type[InfoComponent]", obj_or_import_string(x))
            for x in self.app.config.get("INFO_ENDPOINT_COMPONENTS", [])
        )


schema_view_args = request_parser(from_conf("schema_view_args"), location="view_args")
model_view_args = request_parser(from_conf("model_view_args"), location="view_args")


class InfoResource(BaseResource):
    """Info resource."""

    def create_url_rules(self) -> list[dict[str, Any]]:
        """Create the URL rules for the info resource."""
        return [
            route("GET", "/", self.repository),
            route("GET", "/models", self.models),
            route("GET", "/schema/<path:schema>", self.schema),
        ]

    def call_components(self, method_name: str, **kwargs: Any) -> None:
        """Call components for the given method name."""
        for component in self.components:
            if hasattr(component, method_name):
                getattr(component, method_name)(**kwargs)

    @cached_property
    def components(self) -> list[Any]:
        """Get the components for the info resource from config."""
        return [x(self) for x in self.config.components]

    @response_handler(many=True)
    def models(self) -> tuple[list[dict], int]:
        """Models endpoint."""
        return self.model_data + self.vocabulary_data, 200

    @schema_view_args
    @response_handler()
    def schema(self) -> tuple[dict, int]:
        """Return jsonschema for the current schema."""
        schema = resource_requestctx.view_args["schema"]
        return current_jsonschemas.get_schema(schema, resolved=True), 200

    def _get_model_content_types(self, model: Model) -> list[dict]:
        """Get the content types supported by the model.

        Returns a list of:

        content_type="application/json",
        name="Invenio RDM JSON",
        description="Invenio RDM JSON as described in",
        schema=url / "schemas" / "records" / "record-v6.0.0.json",
        can_export=True,
        can_deposit=True,
        """
        content_types: list[dict] = []
        # export content types
        for model_export in model.exports:
            curr_item = {
                "content_type": model_export.mimetype,
                "code": model_export.code,
                "name": model_export.name,
                "description": model_export.description,
                "can_export": True,
                "can_deposit": model_export.mimetype == "application/json",
            }
            if model_export.mimetype == "application/json":
                curr_item["schema"] = url_for(
                    "oarepo_runtime_info.schema",
                    schema=model.record_json_schema.replace("local://", ""),
                    _external=True,
                )
            content_types.append(curr_item)
        return content_types

    def _get_model_features(self, model: Model) -> list[str]:
        """Get a list of features supported by the model.

        model.features look like:

        {'records': {'version': '8.6.0.785321'},
        'files': {'version': '8.6.0.785321'},
        'drafts-records': {'version': '7.2.0.284413'},
        'drafts-files': {'version': '7.2.0.284413'},
        'ui': {'version': '8.6.0.785321'},
        'ui-links': {'version': '6.0.0dev22'},
        'relations': {'version': '8.6.0.785321'}}
        """
        feature_keys = []
        model_features = model.features or {}
        if model_features.get("requests", {}):
            feature_keys.append("requests")
        if model_features.get("drafts-records", {}):
            feature_keys.append("drafts")
        if model_features.get("files", {}):
            feature_keys.append("files")
        if model_features.get("relations", {}):
            feature_keys.append("relations")
        return feature_keys

    # TODO: this should be done differently - we should add this to the model
    def _get_model_html_endpoint(self, model: Model) -> Any:
        base = self._get_model_api_endpoint(model)
        if not base:
            return None
        suffix = model.resource_config.url_prefix or ""
        return urljoin(base, suffix)

    def _get_model_api_endpoint(self, model: Model) -> str | None:
        try:
            alias = model.api_blueprint_name
            return model.api_url("search", type=alias)
        except BuildError:  # pragma: no cover
            logger.exception("Failed to get model api endpoint")
            return None

    def _get_model_draft_endpoint(self, model: Model) -> str | None:
        try:
            alias = model.api_blueprint_name
            return model.api_url("search_user_records", type=alias)
        except BuildError:
            logger.exception("Failed to get model draft endpoint")
            return None

    @cached_property
    def model_data(self) -> list[dict]:
        """Get the model data."""
        data: list[dict] = []
        # iterate entrypoint oarepo.models
        for model in current_runtime.rdm_models:
            service = model.service
            service_class = model.service.__class__
            if not service or not isinstance(service, service_class):
                continue  # pragma: no cover - sanity check

            model_features = self._get_model_features(model)

            links: dict[str, str | None] = {
                "html": self._get_model_html_endpoint(model),
                "records": self._get_model_api_endpoint(model),
                "deposit": self._get_model_api_endpoint(model),
            }

            if "drafts" in model_features:
                links["drafts"] = self._get_model_draft_endpoint(model)

            data.append(
                {
                    "schema": model.record_json_schema,
                    "type": model.code,
                    "name": model.name,
                    "description": model.description,
                    "version": model.version,
                    "features": model_features,
                    "links": links,
                    "content_types": self._get_model_content_types(model),
                    # rdm models always have metadata element
                    "metadata": True,
                }
            )
        self.call_components("model", data=data)
        data.sort(key=lambda x: x["type"])
        return data

    @cached_property
    def vocabulary_data(self) -> list[dict]:
        """Get the vocabulary data."""
        ret: list[dict] = []
        try:
            from invenio_vocabularies.contrib.affiliations.api import Affiliation
            from invenio_vocabularies.contrib.awards.api import Award
            from invenio_vocabularies.contrib.funders.api import Funder
            from invenio_vocabularies.contrib.names.api import Name
            from invenio_vocabularies.contrib.subjects.api import Subject
            from invenio_vocabularies.records.api import Vocabulary
            from invenio_vocabularies.records.models import VocabularyType
        except ImportError:  # pragma: no cover
            return ret

        def _generate_rdm_vocabulary(  # noqa: PLR0913 more attributes
            base_url: str,
            record: type[Record],
            vocabulary_type: str,
            vocabulary_name: str,
            vocabulary_description: str,
            special: bool,
            can_export: bool = True,
            can_deposit: bool = False,
        ) -> dict:
            schema_field = cast("ConstantField | None", getattr(record, "schema", None))
            if schema_field is not None:
                schema_field_value = schema_field.value
                schema_path = base_url + schema_field_value.replace("local://", "")
            else:
                raise ValueError(f"Record {record} has no schema field")  # pragma: no cover

            if not base_url.endswith("/"):
                base_url += "/"
            url_prefix = base_url + "api" if special else base_url + "api/vocabularies"
            links = {
                "records": f"{url_prefix}/{vocabulary_type}",
            }
            if can_deposit:
                links["deposit"] = f"{url_prefix}/{vocabulary_type}"

            return {
                "schema": schema_field_value,
                "type": vocabulary_type,
                "name": vocabulary_name,
                "description": vocabulary_description,
                "version": "unknown",
                "features": ["rdm", "vocabulary"],
                "links": links,
                "content_types": [
                    {
                        "content_type": "application/json",
                        "name": "Invenio RDM JSON",
                        "description": "Vocabulary JSON",
                        "schema": schema_path,
                        "can_export": can_export,
                        "can_deposit": can_deposit,
                    }
                ],
                "metadata": False,
            }

        base_url = invenio_url_for("vocabularies.search", type="languages")
        base_url = replace_path_in_url(base_url, "/")
        ret = [
            _generate_rdm_vocabulary(base_url, Affiliation, "affiliations", "Affiliations", "", special=True),
            _generate_rdm_vocabulary(base_url, Award, "awards", "Awards", "", special=True),
            _generate_rdm_vocabulary(base_url, Funder, "funders", "Funders", "", special=True),
            _generate_rdm_vocabulary(base_url, Subject, "subjects", "Subjects", "", special=True),
            _generate_rdm_vocabulary(base_url, Name, "names", "Names", "", special=True),
            _generate_rdm_vocabulary(
                base_url,
                Affiliation,
                "affiliations-vocab",
                "Affiliations",
                "Specialized vocabulary for affiliations",
                special=False,
                can_deposit=True,
            ),
            _generate_rdm_vocabulary(
                base_url,
                Award,
                "awards-vocab",
                "Awards",
                "Specialized vocabulary for awards",
                special=False,
                can_deposit=True,
            ),
            _generate_rdm_vocabulary(
                base_url,
                Funder,
                "funders-vocab",
                "Funders",
                "Specialized vocabulary for funders",
                special=False,
                can_deposit=True,
            ),
            _generate_rdm_vocabulary(
                base_url,
                Subject,
                "subjects-vocab",
                "Subjects",
                "Specialized vocabulary for subjects",
                special=False,
                can_deposit=True,
            ),
            _generate_rdm_vocabulary(
                base_url,
                Name,
                "names-vocab",
                "Names",
                "Specialized vocabulary for names",
                special=False,
                can_deposit=True,
            ),
        ]

        vc_types = {vc.id for vc in cast("Any", VocabularyType).query.all()}
        vocab_type_metadata = current_app.config.get("INVENIO_VOCABULARY_TYPE_METADATA", {})
        vc_types.update(vocab_type_metadata.keys())

        for vc in sorted(vc_types):
            vc_metadata = vocab_type_metadata.get(vc, {})
            ret.append(
                _generate_rdm_vocabulary(
                    base_url,
                    Vocabulary,
                    vc,
                    to_current_language(vc_metadata.get("name")) or vc,
                    to_current_language(vc_metadata.get("description")) or "",
                    special=False,
                    can_export=True,
                    can_deposit=True,
                )
            )

        return ret

    @response_handler()
    def repository(self) -> tuple[dict, int]:
        """Repository endpoint."""
        endpoint = request.endpoint
        self_url = url_for(endpoint, _external=True) if endpoint else request.url
        links = {
            "self": self_url,
            "api": replace_path_in_url(self_url, "/api"),
            "models": url_for("oarepo_runtime_info.models", _external=True),
        }
        try:
            import invenio_requests  # noqa

            links["requests"] = invenio_url_for("requests.search")
        except ImportError:  # pragma: no cover
            pass

        ret = {
            "schema": "local://introspection-v1.0.0",
            "name": current_app.config.get("THEME_SITENAME", ""),
            "description": current_app.config.get("REPOSITORY_DESCRIPTION", ""),
            "version": os.environ.get("DEPLOYMENT_VERSION", "local development"),
            "invenio_version": get_package_version("oarepo"),
            "transfers": list(current_transfer_registry.get_transfer_types()),
            "links": links,
            "features": [
                *_add_feature_if_can_import("drafts", "invenio_drafts_resources"),
                *_add_feature_if_can_import("workflows", "oarepo_workflows"),
                *_add_feature_if_can_import("requests", "invenio_requests"),
                *_add_feature_if_can_import("communities", "invenio_communities"),
                *_add_feature_if_can_import("request_types", "oarepo_requests"),
            ],
        }
        if len(self.model_data) == 1:
            ret["default_model"] = self.model_data[0]["name"]

        self.call_components("repository", data=ret)
        return ret, 200


def create_wellknown_blueprint(app: Flask) -> Blueprint:
    """Create an info blueprint."""
    info_endpoint_config = app.config.get("INFO_ENDPOINT_CONFIG")
    config_class = (
        cast("type[InfoConfig]", obj_or_import_string(info_endpoint_config)) if info_endpoint_config else InfoConfig
    )

    return InfoResource(config=config_class(app)).as_blueprint()


def get_package_version(package_name: str) -> str | None:
    """Get package version."""
    from pkg_resources import get_distribution

    return re.sub(r"\+.*", "", get_distribution(package_name).version)


def replace_path_in_url(url: str, path: str) -> str:
    """Replace the path in a URL."""
    # Parse the URL into its components
    parsed_url = urlparse(url)

    # Replace the path with '/api'
    new_parsed_url = parsed_url._replace(path=path)

    # Return the reconstructed URL with the new path
    return str(urlunparse(new_parsed_url))


def _add_feature_if_can_import(feature: str, module: str) -> list[str]:
    try:
        importlib.import_module(module)
    except ImportError:
        return []
    else:
        return [feature]


def to_current_language(data: dict | Any) -> Any:
    """Convert data to current language."""
    if isinstance(data, dict):
        from flask_babel import get_locale

        current_locale = get_locale()
        if current_locale:
            return data.get(current_locale.language)
    return data
