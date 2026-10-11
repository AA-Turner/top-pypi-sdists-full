"""Schema operations for DealCloud (matching real SDK API)."""

from pathlib import Path
from typing import List, Optional, Union

from ..base.dealcloud_base import DealCloudBase
from ..constants.field_types import get_field_type_name
from ..models.schema import (
    Field, FieldUnit, Mapping, MappingsType, Object, ObjectWithFields,
    Schema, Timezone, User,
)
from ..utils.schema_cache import get_schema_cache
from ..utils.process_response_errors import DealCloudValidationError, with_error_handling

_SCHEMA_NO_FIELD_MSG = "Schema API returned no field data (field may not exist)."


def _merge_field_lists(existing: list[Field], incoming: list[Field]) -> list[Field]:
    """Union field lists by field id; first occurrence wins, then append unseen ids from incoming."""
    seen: set[int] = {f.id for f in existing if f.id is not None}
    merged = list(existing)
    for f in incoming:
        fid = f.id
        if fid is None:
            merged.append(f)
            continue
        if fid not in seen:
            seen.add(fid)
            merged.append(f)
    return merged


class DealCloudSchema(DealCloudBase):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Schema Endpoint Methods.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In-memory cache for get_fields(); schema is static per object.
        self._fields_cache: dict[str, list[Field]] = {}

    @with_error_handling
    def get_users(self, active_only: bool = False) -> list[User]:
        """
        Get all users or active users from DealCloud.
        
        Args:
            active_only: If True, return only active users
        
        Returns:
            List of DealCloud users
        """
        url = f"{self._schema_url}/users?activeOnly={str(active_only).lower()}"
        response = self._client.get(url)
        return [User(**obj) for obj in response]

    def get_user_map(self, active_only: bool = False) -> dict[str, int]:
        """
        Get user email to ID mapping.
        
        Args:
            active_only: If True, include only active users
        
        Returns:
            Dict mapping lowercase email addresses to user IDs
        
        Example:
            user_map = dc.get_user_map()
            user_id = user_map.get("john.doe@example.com")
        """
        users = self.get_users(active_only=active_only)
        return {u.email.lower(): u.id for u in users if u.email}

    @with_error_handling
    def get_currencies(self) -> list[str]:
        """
        Get all enabled currency codes.
        
        Returns:
            List of currency codes (e.g., ["USD", "GBP", "EUR"])
        """
        url = f"{self._schema_url}/currencies"
        return self._client.get(url)

    @with_error_handling
    def get_objects(self) -> list[Object]:
        """
        Get all configured objects.
        
        Returns:
            List of DealCloud objects
        """
        url = f"{self._schema_url}/entryTypes"
        response = self._client.get(url)
        return [Object(**obj) for obj in response]

    def get_attachment_object_id(self) -> Union[int, str]:
        """
        Find the attachment object ID (apiName or id) for this site.

        The attachment object is the entry type used for file attachments
        (e.g. upload_attachment, download_attachment). It is identified by
        entryListType == 7 in get_objects(). Site object names are configurable;
        the default is often "Attachment".

        - If exactly one object has entryListType == 7, that object's apiName (or id) is returned.
        - If multiple objects have entryListType == 7, get_fields() is used to disambiguate:
          the object that has fields with apiName "Title", "FileType", and "Size" is chosen.
        - If none have all three fields, the first candidate is returned (best effort).

        Returns:
            Object apiName (str) or id (int) suitable for upload_attachment(object_id=...),
            delete_data(object_id, ...), etc.

        Raises:
            ValueError: If no object with entryListType == 7 is found.

        Example:
            >>> object_id = dc.get_attachment_object_id()
            >>> result = dc.upload_attachment(object_id, content, "file.pdf")
        """
        ATTACHMENT_ENTRY_LIST_TYPE = 7
        REQUIRED_FIELD_NAMES = {"Title", "FileType", "Size"}

        objects = self.get_objects()
        candidates = [o for o in objects if getattr(o, "entryListType", None) == ATTACHMENT_ENTRY_LIST_TYPE]

        if not candidates:
            raise ValueError(
                f"No object with entryListType=={ATTACHMENT_ENTRY_LIST_TYPE} (attachment) found. "
                "Check schema/entryTypes for an object with entryListType 7."
            )

        def _object_id(obj: Object) -> Union[int, str]:
            return obj.apiName if obj.apiName is not None else obj.id

        if len(candidates) == 1:
            out = _object_id(candidates[0])
            if out is None:
                raise ValueError("Attachment object has neither apiName nor id.")
            return out

        # Disambiguate by required fields: Title, FileType, Size
        for obj in candidates:
            object_id = _object_id(obj)
            if object_id is None:
                continue
            fields = self.get_fields(object_id)
            api_names = {getattr(f, "apiName", None) for f in fields if getattr(f, "apiName", None)}
            if REQUIRED_FIELD_NAMES.issubset(api_names):
                return object_id

        # Fallback: return first candidate
        out = _object_id(candidates[0])
        if out is None:
            raise ValueError("Attachment object has neither apiName nor id.")
        return out

    def clear_fields_cache(self, object_id: Optional[Union[int, str]] = None) -> None:
        """
        Clear cached schema for get_fields().

        Schema is cached per object so repeated insert_data/validate_field_mapping
        for the same object does not refetch. Call this if the DealCloud schema
        has changed (e.g. new field added in the UI) and you need fresh data.

        Args:
            object_id: If provided, clear only this object's cached fields.
                If None, clear the entire fields cache.

        Example:
            >>> dc.clear_fields_cache()           # clear all
            >>> dc.clear_fields_cache("Company") # clear only Company
        """
        if object_id is None:
            self._fields_cache.clear()
        else:
            key = f"obj:{object_id}"
            self._fields_cache.pop(key, None)

    def clear_schema_cache(self) -> None:
        """
        Clear all schema-related caches on this client.

        Clears the fields cache used by get_fields(). Use after schema
        changes in DealCloud so the next get_fields() (or insert_data, etc.)
        fetches fresh data.

        Example:
            >>> dc.clear_schema_cache()
        """
        self.clear_fields_cache()

    @with_error_handling
    def get_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
        field_id: Optional[int] = None,
        *,
        editable: Optional[bool] = None,
        entry_form: Optional[bool] = None,
    ) -> list[Field]:
        """
        Get fields configured in DealCloud.

        Results are cached per object (and for field_id / allfields) so
        repeated calls do not refetch. Use clear_fields_cache() or
        clear_schema_cache() to force a refresh.

        Args:
            object_id: Object ID or API name to filter by
            field_id: Specific field ID to retrieve
            editable: When ``object_id`` is set, optional query filter for
                editable vs non-editable fields (schema ``editable``).
            entry_form: When ``object_id`` is set, optional query filter for
                fields shown on the entry form (schema ``entryForm``).

        Returns:
            List of DealCloud fields

        Note:
            Only one of object_id or field_id can be specified.
            If ``editable`` or ``entry_form`` is set, the request must use
            ``object_id``; that call does not read or write the fields cache.
        """
        if object_id and field_id:
            raise AttributeError("Cannot specify both object_id and field_id")

        has_entry_filters = editable is not None or entry_form is not None
        if has_entry_filters and field_id:
            raise AttributeError(
                "Cannot use editable or entry_form together with field_id"
            )
        if has_entry_filters and not object_id:
            raise AttributeError(
                "editable and entry_form are only valid with object_id"
            )

        skip_cache = bool(object_id and has_entry_filters)

        if object_id:
            cache_key = f"obj:{object_id}"
            base_url = f"{self._schema_url}/entryTypes/{object_id}/fields"
            if has_entry_filters:
                query_parts = []
                if editable is not None:
                    query_parts.append(f"editable={str(editable).lower()}")
                if entry_form is not None:
                    query_parts.append(f"entryForm={str(entry_form).lower()}")
                url = f"{base_url}?{'&'.join(query_parts)}"
            else:
                url = base_url
        elif field_id:
            cache_key = f"field:{field_id}"
            url = f"{self._schema_url}/fields/{field_id}"
        else:
            cache_key = "allfields"
            url = f"{self._schema_url}/allfields"

        if not skip_cache and cache_key in self._fields_cache:
            return self._fields_cache[cache_key]

        response = self._client.get(url)

        if (
            response is None
            or (isinstance(response, str) and response.strip().lower() == "null")
            or (
                isinstance(response, list)
                and response
                and all(item is None for item in response)
            )
        ):
            raise DealCloudValidationError(_SCHEMA_NO_FIELD_MSG, status_code=404)

        if isinstance(response, list):
            fields = [Field.from_api(field) for field in response if field is not None]
        else:
            fields = [Field.from_api(response)]

        if skip_cache:
            return fields

        self._fields_cache[cache_key] = _merge_field_lists(
            self._fields_cache.get(cache_key, []), fields
        )
        return self._fields_cache[cache_key]

    @with_error_handling
    def get_field(self, field_id: Union[int, str]) -> Field:
        """
        Get a single field by ID or API name.

        Calls GET schema/fields/{fieldId} (swagger: Get field by Id or ApiName).

        Args:
            field_id: Field ID (int) or API name (str).

        Returns:
            Field instance.

        Example:
            >>> field = dc.get_field(12345)
            >>> field = dc.get_field("CompanyName")
        """
        url = f"{self._schema_url}/fields/{field_id}"
        response = self._client.get(url)

        if (
            response is None
            or (isinstance(response, str) and response.strip().lower() == "null")
            or (
                isinstance(response, list)
                and response
                and all(item is None for item in response)
            )
        ):
            raise DealCloudValidationError(_SCHEMA_NO_FIELD_MSG, status_code=404)

        return Field.from_api(response)

    @with_error_handling
    def get_fields_by_ids(self, field_ids: List[int]) -> List[Field]:
        """
        Get multiple fields by their IDs in a single request.
        
        Args:
            field_ids: List of field IDs to retrieve
        
        Returns:
            List of Field objects
        
        Example:
            >>> fields = dc.get_fields_by_ids([12345, 12346, 12347])
            >>> for field in fields:
            ...     print(f"{field.name}: {field.fieldType}")
        
        Note:
            This is more efficient than multiple get_fields(field_id=...) calls
            when you need to retrieve several fields.
        """
        if not field_ids:
            return []
        
        # Build query string with repeated fieldIds parameters
        query_params = "&".join(f"fieldIds={fid}" for fid in field_ids)
        url = f"{self._schema_url}/fields?{query_params}"
        
        response = self._client.get(url)
        
        if isinstance(response, list):
            return [Field.from_api(field) for field in response]
        else:
            return [Field.from_api(response)]

    @with_error_handling
    def get_field_types(self, use_cache: bool = True) -> List[dict]:
        """
        Get all available field types in DealCloud.
        
        Field types are static metadata that rarely change, so results
        are cached by default for 5 minutes.
        
        Args:
            use_cache: If True (default), use cached results if available.
                      Set to False to force a fresh API call.
        
        Returns:
            List of field type definitions with id and name
        
        Example:
            >>> field_types = dc.get_field_types()
            >>> for ft in field_types:
            ...     print(f"{ft['id']}: {ft['name']}")
            1: Text
            2: Number
            3: Date
            ...
        
        Note:
            This is primarily useful for building dynamic schema editors
            or validation. For most use cases, the field type is already
            available in Field.fieldType from get_fields().
        """
        cache_key = "field_types"
        cache = get_schema_cache()
        
        # Check cache first
        if use_cache:
            cached = cache.get(self._site, cache_key)
            if cached is not None:
                return cached
        
        url = f"{self._schema_url}/fieldtypes"
        response = self._client.get(url)
        
        # Cache the result
        cache.set(self._site, cache_key, response)
        
        return response

    _system_field_types_cache: Optional[List[dict]] = None

    @with_error_handling
    def get_system_field_types(self, use_cache: bool = True) -> List[dict]:
        """
        Get system field types (e.g., Entry ID, Created Date, Modified Date).
        
        System field types are immutable metadata, so results are cached
        in memory for the lifetime of the client instance.
        
        Args:
            use_cache: If True (default), use cached results if available.
                      Set to False to force a fresh API call.
        
        Returns:
            List of system field type definitions with id and name
        
        Example:
            >>> system_types = dc.get_system_field_types()
            >>> for st in system_types:
            ...     print(f"{st['id']}: {st['name']}")
            
            >>> # Find modification-related system fields
            >>> mod_fields = [f for f in system_types if 'modified' in f.get('name', '').lower()]
        """
        if use_cache and self._system_field_types_cache is not None:
            return self._system_field_types_cache
        
        url = f"{self._schema_url}/systemfieldtypes"
        response = self._client.get(url)
        
        # Cache as instance variable
        self._system_field_types_cache = response
        
        return response

    _system_entry_types_cache: Optional[List[dict]] = None

    @with_error_handling
    def get_system_entry_types(self, use_cache: bool = True) -> List[dict]:
        """
        Get system entry types (User, Currency, etc.).
        
        System entry types are immutable metadata, so results are cached
        in memory for the lifetime of the client instance.
        
        Args:
            use_cache: If True (default), use cached results if available.
                      Set to False to force a fresh API call.
        
        Returns:
            List of system entry type definitions with id and name
        
        Example:
            >>> entry_types = dc.get_system_entry_types()
            >>> for et in entry_types:
            ...     print(f"{et['id']}: {et['name']}")
        """
        if use_cache and self._system_entry_types_cache is not None:
            return self._system_entry_types_cache
        
        url = f"{self._schema_url}/systementrytypes"
        response = self._client.get(url)
        
        # Cache as instance variable
        self._system_entry_types_cache = response
        
        return response

    @with_error_handling
    def get_filter_operations(self) -> List[dict]:
        """
        Get available filter operations for query building.
        
        Filter operations define the operators available for filtering
        data (e.g., Equals, Contains, GreaterThan) and which field types
        each operator is compatible with.
        
        Returns:
            List of filter operation definitions
        
        Example:
            >>> operations = dc.get_filter_operations()
            >>> for op in operations:
            ...     print(f"{op['id']}: {op['name']}")
            
            >>> # Find text-compatible operations
            >>> text_ops = [op for op in operations 
            ...             if 'text' in str(op.get('applicableTo', [])).lower()]
        
        Note:
            Results are not cached as filter operations may be updated.
        """
        url = f"{self._schema_url}/filteroperations"
        return self._client.get(url)

    @with_error_handling
    def get_entry_type(
        self,
        entry_type_id: Union[int, str],
    ) -> Object:
        """
        Get properties for a single entry type by ID or API name.
        
        Args:
            entry_type_id: Entry type ID (int) or API name (str)
        
        Returns:
            Object describing the entry type
        
        Example:
            >>> obj = dc.get_entry_type("Company")
            >>> print(f"{obj.apiName}: {obj.singularName}")
        """
        url = f"{self._schema_url}/entryTypes/{entry_type_id}"
        response = self._client.get(url)
        return Object(**response)

    @with_error_handling
    def get_mappings_types(self) -> List[MappingsType]:
        """
        Get all object mappings types.
        
        Mappings types define the categories of object-to-object mappings
        available in the site (e.g., external system mappings).
        
        Returns:
            List of mappings type definitions
        
        Example:
            >>> mapping_types = dc.get_mappings_types()
            >>> for mt in mapping_types:
            ...     print(f"{mt.id}: {mt.name}")
        """
        url = f"{self._schema_url}/mappingstypes"
        response = self._client.get(url)
        return [MappingsType(**item) for item in response]

    @with_error_handling
    def get_mappings(self, mappings_type_id: int) -> List[Mapping]:
        """
        Get all object mappings for a given mappings type.
        
        Args:
            mappings_type_id: The mappings type ID to retrieve mappings for.
                             Use get_mappings_types() to discover available types.
        
        Returns:
            List of mapping definitions
        
        Example:
            >>> # First, get available mapping types
            >>> types = dc.get_mappings_types()
            >>> # Then get mappings for a specific type
            >>> mappings = dc.get_mappings(types[0].id)
            >>> for m in mappings:
            ...     print(f"{m.id}: {m.name}")
        """
        url = f"{self._schema_url}/mappings/{mappings_type_id}"
        response = self._client.get(url)
        return [Mapping(**item) for item in response]

    @with_error_handling
    def get_contract(self, schema_contract_global_id: str) -> str:
        """
        Get a schema contract by its global ID.
        
        Schema contracts define the structure and validation rules
        for a particular schema version.
        
        Args:
            schema_contract_global_id: The UUID of the schema contract
        
        Returns:
            Schema contract content as a string
        
        Example:
            >>> contract = dc.get_contract("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
            >>> print(contract)
        """
        url = f"{self._schema_url}/contracts/{schema_contract_global_id}"
        return self._client.get(url)

    @with_error_handling
    def append_choice_values(
        self,
        field_id: Union[int, str],
        choice_values: Union[List[str], List[dict]],
    ) -> list:
        """
        Append choice values to a choice field.

        Adds new choice options to an existing choice field without
        removing or modifying existing choices. The API expects an array
        of strings; dicts are converted to their "name" value.

        Args:
            field_id: The field ID or API name of the choice field
            choice_values: List of choice value strings to append, or list of
                dicts with at least a "name" key. The API expects an array of
                strings; dicts are converted to their "name" value.

        Returns:
            API response with the updated choice values

        Example:
            >>> dc.append_choice_values(
            ...     field_id=12345,
            ...     choice_values=["New Option A", "New Option B"],
            ... )
            >>> # or with dicts (converted to name):
            >>> dc.append_choice_values(
            ...     field_id=12345,
            ...     choice_values=[{"name": "New Option A"}, {"name": "New Option B"}],
            ... )
        """
        url = f"{self._schema_url}/choiceFieldValues/{field_id}"
        payload = [
            (item if isinstance(item, str) else item.get("name", ""))
            for item in choice_values
        ]
        return self._client.post(url, json=payload)

    @with_error_handling
    def get_field_units(self) -> List[FieldUnit]:
        """
        Get all available field units.
        
        Field units define the measurement units that can be assigned
        to numeric fields (e.g., percentage, currency denominations).
        
        Returns:
            List of field unit definitions
        
        Example:
            >>> units = dc.get_field_units()
            >>> for unit in units:
            ...     print(f"{unit.id}: {unit.name}")
        """
        url = f"{self._schema_url}/fieldunits"
        response = self._client.get(url)
        return [FieldUnit(**item) for item in response]

    @with_error_handling
    def get_timezones(self) -> List[Timezone]:
        """
        Get all available timezones.
        
        Returns the list of timezones configured in the DealCloud site,
        which can be used for date/time field configuration.
        
        Returns:
            List of timezone definitions
        
        Example:
            >>> timezones = dc.get_timezones()
            >>> for tz in timezones:
            ...     print(f"{tz.id}: {tz.displayName}")
        """
        url = f"{self._schema_url}/timezones"
        response = self._client.get(url)
        return [Timezone(**item) for item in response]

    def get_field_by_name(
        self,
        object_id: Union[int, str],
        display_name: str,
    ) -> Optional[Field]:
        """
        Get a field by its display name.
        
        Args:
            object_id: Object ID or API name
            display_name: The field's display name (e.g., "Full Name")
        
        Returns:
            Field object if found, None otherwise
        
        Example:
            field = dc.get_field_by_name("User", "Full Name")
            if field:
                print(f"API name: {field.apiName}")  # "FullName"
        """
        fields = self.get_fields(object_id=object_id)
        for f in fields:
            if f.name == display_name:
                return f
        return None

    def get_field_by_api_name(
        self,
        object_id: Union[int, str],
        api_name: str,
    ) -> Optional[Field]:
        """
        Get a field by its API name.
        
        Args:
            object_id: Object ID or API name
            api_name: The field's API name (e.g., "FullName")
        
        Returns:
            Field object if found, None otherwise
        """
        fields = self.get_fields(object_id=object_id)
        for f in fields:
            if f.apiName == api_name:
                return f
        return None

    def get_field_lookup(
        self,
        object_id: Union[int, str],
    ) -> dict[int, dict[str, str]]:
        """
        Map field id → display name and API name for one object.

        Uses cached schema fields (same source as :meth:`get_field_map`).

        Args:
            object_id: Object API name or numeric id.

        Returns:
            ``{field_id: {"name": display_name, "apiName": api_name}}``

        Example:
            lookup = dc.get_field_lookup("Company")
            meta = lookup.get(2060083)
            print(meta["name"], meta["apiName"])
        """
        from ..utils.error_enrichment import field_lookup_from_fields

        return field_lookup_from_fields(self.get_fields(object_id=object_id))

    def get_field_map(
        self,
        object_names: Optional[list[str]] = None,
    ) -> dict[str, dict[str, dict]]:
        """
        Get field map in the format expected by import tools.
        
        This is the standard id_map structure used across tools for
        field metadata lookups.
        
        Args:
            object_names: List of object API names to include.
                         If None, includes all objects.
        
        Returns:
            Nested dict: {object_name: {field_api_name: {metadata}}}
        
        Example:
            field_map = dc.get_field_map(["Company", "Contact"])
            
            # Access field metadata
            company_name = field_map["Company"]["Name"]
            print(company_name["id"])        # Field ID
            print(company_name["name"])      # Display name
            print(company_name["type"])      # "Text", "Reference", etc.
            print(company_name["apiName"])   # API name
            print(company_name["choices"])   # {choice_name: choice_id}
            print(company_name["references"]) # [list_id, ...]
        """
        schema = self.get_schema()
        field_map = {}
        
        for obj_name, obj_data in schema.objects.items():
            # Filter to requested objects if specified
            if object_names and obj_name not in object_names:
                continue
            
            field_map[obj_name] = {}
            
            for field in obj_data.fields.values():
                field_map[obj_name][field.apiName] = {
                    "id": field.id,
                    "name": field.name,
                    "type": get_field_type_name(field.fieldType) if field.fieldType else "Unknown",
                    "apiName": field.apiName,
                    "isRequired": field.isRequired or False,
                    "isCalculated": field.isCalculated or False,
                    "isMultiSelect": field.isMultiSelect or False,
                    "isMoney": field.isMoney or False,
                    "choices": {cv.name: cv.id for cv in (field.choiceValues or [])},
                    "references": list(field.entryLists or []),
                }
        
        return field_map

    def get_name_to_api_map(
        self,
        object_id: Union[int, str],
    ) -> dict[str, str]:
        """
        Get mapping from display names to API names for an object.
        
        Args:
            object_id: Object ID or API name
        
        Returns:
            Dict mapping display names to API names
        
        Example:
            name_map = dc.get_name_to_api_map("User")
            api_name = name_map.get("Full Name")  # "FullName"
        """
        fields = self.get_fields(object_id=object_id)
        return {f.name: f.apiName for f in fields if f.name and f.apiName}

    def get_api_to_name_map(
        self,
        object_id: Union[int, str],
    ) -> dict[str, str]:
        """
        Get mapping from API names to display names for an object.
        
        Args:
            object_id: Object ID or API name
        
        Returns:
            Dict mapping API names to display names
        
        Example:
            api_map = dc.get_api_to_name_map("User")
            display_name = api_map.get("FullName")  # "Full Name"
        """
        fields = self.get_fields(object_id=object_id)
        return {f.apiName: f.name for f in fields if f.name and f.apiName}

    def get_schema(self, key_type: str = "api") -> Schema:
        """
        Get full DealCloud schema.
        
        Args:
            key_type: Key type for schema dict:
                - "api": Use API names as keys (default)
                - "display": Use display names as keys
                - "id": Use object/field IDs as keys
        
        Returns:
            Full DealCloud schema with objects and fields
        """
        objects = self.get_objects()
        fields = self.get_fields()
        
        schema = {}
        for o in objects:
            object_fields = [f for f in fields if f.entryListId == o.id]
            
            if key_type == "api":
                filtered_fields = {f.apiName: f for f in object_fields}
                schema[o.apiName] = ObjectWithFields(object=o, fields=filtered_fields)
            elif key_type == "display":
                filtered_fields = {f.name: f for f in object_fields}
                schema[o.name] = ObjectWithFields(object=o, fields=filtered_fields)
            elif key_type == "id":
                filtered_fields = {str(f.id): f for f in object_fields}
                schema[str(o.id)] = ObjectWithFields(object=o, fields=filtered_fields)
            else:
                raise AttributeError('key_type must be one of "api", "display", "id".')
        
        return Schema(objects=schema)

    def export_schema_to_excel(
        self,
        filepath: Union[str, Path],
        objects: Optional[List[str]] = None,
        include_summary: bool = True,
        include_relationships: bool = True,
    ) -> Path:
        """
        Export the DealCloud schema to an Excel workbook.
        
        Creates a multi-sheet Excel file with:
        - Summary sheet: Overview of all objects
        - One sheet per object: Detailed field information
        - Relationships sheet (optional): Object-to-object reference mappings
        
        Args:
            filepath: Output Excel file path (.xlsx)
            objects: Optional list of object API names to include.
                    If None, exports all objects.
            include_summary: If True (default), include summary sheet
            include_relationships: If True (default), include relationships sheet
        
        Returns:
            Path to the created Excel file
        
        Example:
            >>> # Export full schema
            >>> path = dc.export_schema_to_excel("full_schema.xlsx")
            >>> 
            >>> # Export specific objects
            >>> path = dc.export_schema_to_excel(
            ...     "crm_schema.xlsx",
            ...     objects=["Company", "Contact", "Deal"]
            ... )
        """
        import pandas as pd
        from ..utils.excel_utils import export_to_excel, sanitize_sheet_name
        
        filepath = Path(filepath)
        schema = self.get_schema(key_type="api")
        
        # Filter to requested objects
        if objects:
            filtered_objects = {k: v for k, v in schema.objects.items() if k in objects}
        else:
            filtered_objects = schema.objects
        
        if not filtered_objects:
            raise ValueError("No objects found matching the specified filter")
        
        # Build sheets dict
        sheets: dict[str, pd.DataFrame] = {}
        
        # Summary sheet
        if include_summary:
            summary_data = []
            for obj_name, obj_data in filtered_objects.items():
                obj = obj_data.object
                field_count = len(obj_data.fields) if obj_data.fields else 0
                summary_data.append({
                    "Object ID": obj.id,
                    "API Name": obj.apiName,
                    "Display Name (Singular)": obj.singularName,
                    "Display Name (Plural)": obj.pluralName,
                    "Field Count": field_count,
                    "Entry List Type": obj.entryListType,
                    "Entry List Sub-Type": obj.entryListSubType,
                })
            sheets["Summary"] = pd.DataFrame(summary_data)
        
        # Object field sheets
        for obj_name, obj_data in filtered_objects.items():
            fields_data = []
            for field in (obj_data.fields or {}).values():
                # Get human-readable field type
                field_type_name = get_field_type_name(field.fieldType) if field.fieldType else "Unknown"
                
                # Format choice values
                choice_values = ""
                if field.choiceValues:
                    choice_values = "; ".join([cv.name for cv in field.choiceValues if cv.name])
                
                # Format reference objects
                reference_objects = ""
                if field.entryLists:
                    # Look up object names for the entry list IDs
                    ref_names = []
                    for ref_id in field.entryLists:
                        for ref_obj_name, ref_obj_data in schema.objects.items():
                            if ref_obj_data.object and ref_obj_data.object.id == ref_id:
                                ref_names.append(ref_obj_name)
                                break
                        else:
                            ref_names.append(f"ID:{ref_id}")
                    reference_objects = "; ".join(ref_names)
                
                fields_data.append({
                    "Field ID": field.id,
                    "API Name": field.apiName,
                    "Display Name": field.name,
                    "Field Type": field_type_name,
                    "Field Type ID": field.fieldType,
                    "Required": "Yes" if field.isRequired else "No",
                    "Multi-Select": "Yes" if field.isMultiSelect else "No",
                    "Calculated": "Yes" if field.isCalculated else "No",
                    "Money": "Yes" if field.isMoney else "No",
                    "Is Key": "Yes" if field.isKey else "No",
                    "Is Attachment": "Yes" if field.isAttachment else "No",
                    "System Field Type": field.systemFieldType or "",
                    "Description": field.description or "",
                    "Choice Values": choice_values,
                    "Reference Objects": reference_objects,
                    "Formula": field.formula or "",
                })
            
            # Create DataFrame and sort by field type, then name
            df = pd.DataFrame(fields_data)
            if not df.empty:
                df = df.sort_values(by=["Field Type", "Display Name"])
            
            # Sanitize sheet name (max 31 chars, no special chars)
            sheet_name = sanitize_sheet_name(obj_name)
            sheets[sheet_name] = df
        
        # Relationships sheet
        if include_relationships:
            relationships_data = []
            for obj_name, obj_data in filtered_objects.items():
                for field in (obj_data.fields or {}).values():
                    if field.entryLists and field.fieldType == 5:  # Reference field
                        for ref_id in field.entryLists:
                            # Look up object name
                            ref_obj_name = f"ID:{ref_id}"
                            for lookup_name, lookup_data in schema.objects.items():
                                if lookup_data.object and lookup_data.object.id == ref_id:
                                    ref_obj_name = lookup_name
                                    break
                            
                            relationships_data.append({
                                "Source Object": obj_name,
                                "Field API Name": field.apiName,
                                "Field Display Name": field.name,
                                "Target Object": ref_obj_name,
                                "Multi-Select": "Yes" if field.isMultiSelect else "No",
                                "Is Attachment": "Yes" if field.isAttachment else "No",
                            })
            
            if relationships_data:
                sheets["Relationships"] = pd.DataFrame(relationships_data)
        
        # Export to Excel
        return export_to_excel(sheets, filepath, index=False)
