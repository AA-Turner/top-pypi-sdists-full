from typing import Optional
import logging

_logger = logging.getLogger(__name__)

from ...api.ontology import fetch_ontology_data
from ...client import Client, get_default_client
from ..exceptions import ApiConnectionError


def _align_ontology(ontology):
    """Convert the optimized API format into the established SDK format.

    The API now returns an optimized structure with three top-level dicts
    (concepts, relationships, properties).  SDK consumers expect the legacy
    shape with:
      - concepts keyed by name, each with parents (self at [0]),
        primaryKeys, labelKeys, inheritanceLevel, allProperties (list of
        dicts), properties (direct-only list of dicts), tags, relationships
      - relationships as a flat list of dicts
    """
    opt_properties = ontology.get("properties", {})

    # ── Convert concepts ──────────────────────────────────────────────────
    for concept_name, concept_dict in ontology.get("concepts", {}).items():
        # parents: insert self at index 0 (legacy SDK convention)
        concept_dict["parents"].insert(0, concept_name)

        # Rename / synthesise legacy fields
        concept_dict["labelKeys"] = concept_dict.get("label_keys", [])
        concept_dict["inheritanceLevel"] = concept_dict.get("inheritance_level", 0)

        # allProperties: full inherited list as dicts
        concept_dict["allProperties"] = [
            {
                "property_name": pname,
                "property_type": opt_properties[pname]["property_type"],
            }
            for pname in concept_dict.get("properties", [])
            if pname in opt_properties
        ]

        # properties: direct-only as dicts
        concept_dict["properties"] = [
            {
                "property_name": pname,
                "property_type": opt_properties[pname]["property_type"],
            }
            for pname in concept_dict.get("direct_properties", [])
            if pname in opt_properties
        ]

    # ── Convert relationships dict → flat list ────────
    relationships_list = []
    for rname, rdata in ontology.get("relationships", {}).items():
        relationships_list.append(
            {
                "relationship_name": rname,
                "is_mtm": rdata.get("is_mtm", False),
                "concept": rdata.get("source_concept", ""),
                "source_concept": rdata.get("source_concept", ""),
                "target_concept": rdata.get("target_concept", ""),
                "source_properties": ",".join(rdata.get("source_properties", [])),
                "target_properties": ",".join(rdata.get("target_properties", [])),
                "inverse_name": rdata.get("inverse_name"),
                "inverse": rdata.get("is_inverse", False),
            }
        )
    ontology["relationships"] = relationships_list

    return ontology


def sync(ontology_name: Optional[str] = None, client: Optional[Client] = None):
    """
    # Query Ontology Structure

    Retrieves the structure of an ontology.

    ## Arguments
    - `ontology_name`: The name of the ontology.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A dictionary containing a list of concepts and a list of relationships.
    Each of these entries is in itself a dictionary.

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology.
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not ontology_name:
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "Only the client ontology is currently supported for this method!"
        )
    response = fetch_ontology_data.sync_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("fetch_ontology_data", response, client)
    if response.parsed is None:
        raise ApiConnectionError("fetch_ontology_data", response, client)
    ontology = response.parsed.additional_properties
    return _align_ontology(ontology)


async def asyncio(ontology_name: Optional[str] = None, client: Optional[Client] = None):
    """
    # Query Ontology Structure Asynchronously

    Asynchronously retrieves the structure of an ontology.

    ## Arguments
    - `ontology_name`: The name of the ontology.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A dictionary containing a list of concepts and a list of relationships.
    Each of these entries is in itself a dictionary.

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology.
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    if not ontology_name:
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "Only the active ontology is currently supported for this method!"
        )
    response = await fetch_ontology_data.asyncio_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("fetch_ontology_data", response, client)
    if response.parsed is None:
        raise ApiConnectionError("fetch_ontology_data", response, client)
    ontology = response.parsed.additional_properties
    return _align_ontology(ontology)
