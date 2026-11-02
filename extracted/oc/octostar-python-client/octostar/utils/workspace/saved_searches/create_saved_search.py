from typing import List, Optional, Any, Union, TypedDict
import logging
import uuid

_logger = logging.getLogger(__name__)

from .. import upsert_entity
from ...ontology import fetch_ontology_data
from ....client import Client


class SupersetFilter(TypedDict):
    pass


class SimpleSupersetFilter(SupersetFilter):
    """
    # Represents a primitive superset filter using a (col, op, val) tuple.

    ## Attributes:
    - **col** (`str`): The timbr column involved in the filter as the first operand.
    - **op** (`str`): The operator name, e.g. `"=="`, `"IN"`, `"LIKE"`.
    - **val** (`Any`, `List[Any]`): The value (or values) involved in the filter as the second operand.
    """

    col: str
    op: str
    val: Union[Any, List[Any]]


class ComplexSupersetFilter(SupersetFilter):
    """
    # Represents a nested superset filter combined via a logical boolean operator.

    ## Attributes:
    - **operator** (`str`): The SQL logical operator to apply to all operands, e.g. `AND`, `OR`.
    - **operands** (`List[SupersetFilter]`): A list of superset filters onto which the logical operator is applied.
    """

    operator: str
    operands: List[SupersetFilter]
    operator: str
    operands: List[SupersetFilter]


def sync(
    os_workspace: str,
    name: str,
    entity_type: str,
    filter: List[SupersetFilter],
    path: str = None,
    os_entity_uid: Optional[str] = None,
    fields: dict = {},
    client: Optional[Client] = None,
):
    """
    # Create or update a local saved search in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID
    - `name`: The name for the saved search
    - `entity_type`: The entity type for which to apply the filter
    - `filter`: The superset filter for the saved search
    - `path`: The path to the saved search file in the workspace, excluding the saved search filename
    - `os_entity_uid`: The unique identifier for the saved search
    - `fields`: Additional fields to include in the entity record
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The created/updated entity record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If the operation was unsuccessful on the server
    """
    icon = None
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())
    try:
        ontology = fetch_ontology_data.sync(client=client)
        curr_concept = ontology["concepts"][entity_type]
        while not icon:
            icon = curr_concept["tags"].get("icon")
            if not icon:
                curr_concept = ontology["concepts"][curr_concept["parents"][0]]
    except Exception:
        logging.warning("Warning: Could not assign icon to saved search!")
    return upsert_entity.sync(
        os_workspace=os_workspace,
        os_entity_type="os_wsfs_object",
        os_entity_uid=os_entity_uid,
        fields={
            **fields,
            "os_item_content_type": "os_saved_search",
            "os_item_name": name,
            "os_icon": icon,
            "os_item_content": {
                "concept": entity_type,
                "crossFilters": [
                    {
                        "id": str(uuid.uuid4()),
                        "extraFormData": {
                            "filters": filter,
                        },
                        "filterState": {},
                        "ownState": {},
                    }
                ],
                "filters": [],
                "datasourcesInScope": {},
            },
            "os_parent_folder": os_workspace,
            "#os_path": path or "",
        },
        client=client,
    )


async def asyncio(
    os_workspace: str,
    name: str,
    entity_type: str,
    filter: List[SupersetFilter],
    path: str = None,
    os_entity_uid: Optional[str] = None,
    fields: dict = {},
    client: Optional[Client] = None,
):
    """
    # Create or update asynchronously a local saved search in a workspace

    ## Arguments
    (Same as sync function)

    ## Returns
    The created/updated entity record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If the operation was unsuccessful on the server
    """
    icon = None
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())
    try:
        ontology = fetch_ontology_data.sync(client=client)
        curr_concept = ontology["concepts"][entity_type]
        while not icon:
            icon = curr_concept["tags"].get("icon")
            if not icon:
                curr_concept = ontology["concepts"][curr_concept["parents"][0]]
    except Exception:
        logging.warning("Warning: Could not assign icon to saved search!")

    return upsert_entity.sync(
        os_workspace=os_workspace,
        os_entity_type="os_wsfs_object",
        os_entity_uid=os_entity_uid,
        fields={
            **fields,
            "os_item_content_type": "os_saved_search",
            "os_item_name": name,
            "os_icon": icon,
            "os_item_content": {
                "concept": entity_type,
                "crossFilters": [
                    {
                        "id": str(uuid.uuid4()),
                        "extraFormData": {
                            "filters": filter,
                        },
                        "filterState": {},
                        "ownState": {},
                    }
                ],
                "filters": [],
                "datasourcesInScope": {},
            },
            "os_parent_folder": os_workspace,
            "#os_path": path or "",
        },
        client=client,
    )
