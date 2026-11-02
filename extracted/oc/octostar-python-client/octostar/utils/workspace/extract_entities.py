import json
import logging
from typing import List, Optional
from urllib.parse import urlparse, unquote_plus

# Set up logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)  # Adjust level as needed

_DEFAULT_ACTION = "view"


def parse_hash(hash_str: str) -> dict:
    """
    # Parse the hash part of a URL to extract the action, entity_id, entity_type, and entity_label

    ## Arguments
    - `hash_str`: The hash string from a URL (e.g., '#view/123/user#label')

    ## Returns
    A dictionary with keys 'action', 'entity_id', 'entity_type', and 'entity_label'
    """
    hash_str = hash_str.strip()
    if hash_str.startswith("#"):
        hash_str = hash_str[1:]

    if not hash_str:
        return {
            "action": _DEFAULT_ACTION,
            "entity_id": "",
            "entity_type": "os_thing",
            "entity_label": "",
        }
    main_part, *label_parts = hash_str.split("#")
    entity_label = "#".join(label_parts) if label_parts else ""

    parts = main_part.split("/")

    if len(parts) == 3:
        action, entity_id, entity_type = parts
    elif len(parts) == 2:
        action, entity_id = None, parts[0]
        entity_type = parts[1]
    else:
        action, entity_id, entity_type = None, parts[0], "os_thing"

    return {
        "action": unquote_plus(action or _DEFAULT_ACTION),
        "entity_id": unquote_plus(entity_id),
        "entity_type": unquote_plus(entity_type),
        "entity_label": unquote_plus(entity_label),
    }


def get_entity_from_url(url_string: str) -> Optional[dict]:
    """
    # Extract an entity from a URL

    ## Arguments
    - `url_string`: The URL containing the entity information in the hash part

    ## Returns
    A dictionary representing the entity, or None if extraction fails
    """
    try:
        url = urlparse(url_string)
        if not url.fragment:
            return None

        parsed_hash = parse_hash(url.fragment)
        if not parsed_hash["entity_id"]:
            return None

        # Return the dictionary without the 'action' field
        return {
            "entity_id": parsed_hash["entity_id"],
            "entity_type": parsed_hash["entity_type"],
            "entity_label": parsed_hash.get("entity_label", ""),
        }
    except Exception as e:
        _logger.error(f"Error parsing URL {url_string}: {e}")
        return None


def get_entities_from_urls(urls: str) -> List[dict]:
    """
    # Extract entities from multiple URLs provided as a multi-line string

    ## Arguments
    - `urls`: A string with each URL on a new line

    ## Returns
    A list of dictionaries, each representing an entity
    """
    return [
        entity
        for entity in (get_entity_from_url(url.strip()) for url in urls.splitlines())
        if entity
    ]


def is_valid_entity(obj: dict) -> bool:
    """
    # Check if a dictionary is a valid entity

    ## Arguments
    - `obj`: The dictionary to check

    ## Returns
    True if the dictionary has 'entity_id' and 'entity_type', False otherwise
    """
    return isinstance(obj, dict) and "entity_id" in obj and "entity_type" in obj


def extract_entities(text: str) -> List[dict]:
    """
    # Extract entities from a JSON string or plain text containing URLs

    ## Arguments
    - `text`: The input text, which can be a JSON string or plain text

    ## Returns
    A list of dictionaries, each representing an entity. If the input is invalid, an empty list is returned
    """
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return get_entities_from_urls(text)

    if isinstance(parsed, list):
        return [item for item in parsed if is_valid_entity(item)]

    if isinstance(parsed, dict) and is_valid_entity(parsed):
        return [parsed]

    if isinstance(parsed, str):
        return get_entities_from_urls(parsed)

    _logger.debug(f"No entities found in input: {text}")
    return []
