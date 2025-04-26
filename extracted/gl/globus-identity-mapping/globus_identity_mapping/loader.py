from __future__ import annotations

import importlib.metadata
import logging
import sys
import typing as t

from .errors import InvalidMappingError
from .protocol import IdentityMappingProtocol

log = logging.getLogger(__name__)


def load_mappers(
    mappings_list: t.Iterable[dict | IdentityMappingProtocol] | None,
    connector: str | None = None,
    storage_gateway: str | None = None,
) -> list[IdentityMappingProtocol]:
    """
    Dynamically instantiate IdentityMapping objects based on the passed
    configuration documents.

    An IdentityMapping configuration document is just a dictionary with a
    structure as outlined in Globus Connect Server's Identity Mapping Guide
    documentation[1].  That's basically a structure:

        {
            "DATA_TYPE": "<class_name>#<version>"
            "further": [
                "structure per the specific class' specification"
                " and needs"
            ]
        }

    An example use of this helper function might look like:

        def get_mappers_from_application_specific_config(...):
            config_doc_path = pathlib.Path("path/to/identity_config.json")
            config_document_texts = config_doc_path.read_text()
            config_documents = json.loads(config_document_texts)
            return load_mappers(config_documents, connector_id, storage_gateway_id)

    A list of Globus-specific Connector Identifiers is also available in the
    Identity Mapping Guide[1].  (See "Command Line Options")

    After loading, the mappers may each be queried to determine a context-
    appropriate username.  That might look like:

        for mapper in mappers:
            username = mapper.map_identity(globus_identity_object)

    [1] https://docs.globus.org/globus-connect-server/v5.4/identity-mapping-guide/
    """
    mappings: list[IdentityMappingProtocol] = []
    for ndx, map_or_config in enumerate(mappings_list or []):
        if isinstance(map_or_config, dict):
            data_type: str | None = map_or_config.get("DATA_TYPE")
            if not data_type:
                raise InvalidMappingError(f"Invalid map config (index: {ndx})")

            mapping_identifier = data_type.split("#", 1)[0]
            mapper = None
            eps = importlib.metadata.entry_points()
            if sys.version_info < (3, 10):
                gim_lib = eps.get("globus_identity_mapping", [])
            else:
                gim_lib = eps.select(group="globus_identity_mapping")
            for ep in gim_lib:
                if ep.name == mapping_identifier:
                    entry_point = ep.load()
                    mapper = entry_point.from_mapping_document(
                        map_or_config,
                        connector=connector,
                        storage_gateway=storage_gateway,
                    )
                    break
            if mapper:
                mappings.append(mapper)
                continue
            log.warning(f"No identity mapper found for: {data_type} (index: {ndx})")

        elif hasattr(map_or_config, "map_identity"):
            mappings.append(map_or_config)
        else:
            raise InvalidMappingError(f"Invalid mapping or map config (index: {ndx})")

    return mappings


__all__ = ("load_mappers",)
