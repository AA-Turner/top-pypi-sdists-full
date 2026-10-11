"""Typed data operations using Pydantic models."""

from typing import TYPE_CHECKING, AsyncIterator, Iterator, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ValidationError

from .models import BatchResult, ReferenceCache, ReferenceFormat
from . import read, references, streaming, write

if TYPE_CHECKING:
    import polars as pl
    from .dealcloud_data import DealCloudData

# Type variable for Pydantic model generic methods
T = TypeVar("T", bound=BaseModel)


def typed_read_data(
    self: "DealCloudData",
    model: Type[T],
    object_id: Optional[Union[int, str]] = None,
    view_id: Optional[Union[int, str]] = None,
    query: Optional[str] = None,
    fields: Optional[List[str]] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    skip_validation_errors: bool = False,
    **kwargs,
) -> List[T]:
    """
    Read data as typed Pydantic models.
    
    Typed wrapper around read_data() - returns List[T] instead of 
    list[dict] or DataFrame. Customer defines their own Pydantic models
    matching their DealCloud schema.
    
    Args:
        self: DealCloudData instance
        model: Pydantic model class to deserialize into
        object_id: Object API name or ID
        view_id: View ID (alternative to object_id)
        query: Optional DealCloud query string
        fields: Fields to fetch (default: auto-detect from model)
        reference_format: How to format reference fields (ID, NAME, or None for full)
        reference_cache: Optional cache for reference name lookups
        skip_validation_errors: If True, skip rows that fail validation
                               (logs warning). If False (default), raises.
        **kwargs: Additional args passed to read_data()
    
    Returns:
        List of model instances
    
    Example:
        >>> from pydantic import BaseModel
        >>> from typing import Optional
        >>> 
        >>> class Company(BaseModel):
        ...     EntryId: int
        ...     Name: str
        ...     Industry: Optional[str] = None
        ...     Revenue: Optional[float] = None
        >>> 
        >>> # Read from object
        >>> companies = dc.typed_read_data(Company, object_id="Company")
        >>> for c in companies:
        ...     print(f"{c.Name}: {c.Industry}")  # Full autocomplete!
        >>> 
        >>> # Read from view
        >>> deals = dc.typed_read_data(DealSummary, view_id="Active Deals")
        >>> 
        >>> # With query filter and reference names
        >>> active = dc.typed_read_data(
        ...     Company,
        ...     object_id="Company",
        ...     query="Status = 'Active'",
        ...     reference_format=ReferenceFormat.NAME
        ... )
    """
    # Auto-detect fields from model if not specified
    if fields is None:
        fields = list(model.model_fields.keys())
    
    data = read.read_data(
        self,
        object_id=object_id,
        view_id=view_id,
        output="list",  # Always list for Pydantic parsing
        fields=fields,
        query=query,
        reference_format=reference_format,
        reference_cache=reference_cache,
        **kwargs,
    )
    
    results = []
    for row in data:
        try:
            results.append(model.model_validate(row))
        except ValidationError as e:
            entry_id = row.get("EntryId") or row.get("entryId")
            if skip_validation_errors:
                self._logger.warning(
                    f"Validation error for EntryId {entry_id}, skipping: {e}"
                )
            else:
                # Re-raise model_validate's ValidationError (Pydantic v2 has no string-only constructor).
                raise
    
    return results


def typed_read_data_polars(
    self: "DealCloudData",
    model: Type[T],
    object_id: Optional[Union[int, str]] = None,
    view_id: Optional[Union[int, str]] = None,
    query: Optional[str] = None,
    fields: Optional[List[str]] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    lazy: bool = False,
    **kwargs,
) -> Union["pl.DataFrame", "pl.LazyFrame"]:
    """
    Read data as a Polars DataFrame with schema derived from Pydantic model.
    
    Combines the performance of Polars with the type documentation of Pydantic
    models. The model defines which fields to fetch and documents the expected
    types, but data is returned as a Polars DataFrame for efficient processing.
    
    Args:
        self: DealCloudData instance
        model: Pydantic model class (used for field selection, not validation)
        object_id: Object API name or ID
        view_id: View ID (alternative to object_id)
        query: Optional DealCloud query string
        fields: Fields to fetch (default: auto-detect from model)
        reference_format: How to format reference fields (ID, NAME, or None for full)
        reference_cache: Optional cache for reference name lookups
        lazy: If True, return LazyFrame for deferred execution
        **kwargs: Additional args passed to read_data()
    
    Returns:
        Polars DataFrame (or LazyFrame if lazy=True)
    
    Example:
        >>> from pydantic import BaseModel
        >>> 
        >>> class Company(BaseModel):
        ...     EntryId: int
        ...     Name: str
        ...     Revenue: float
        >>> 
        >>> # Get polars DataFrame with model-defined fields
        >>> df = dc.typed_read_data_polars(Company, object_id="Company")
        >>> 
        >>> # Fast Polars operations
        >>> high_revenue = df.filter(pl.col("Revenue") > 1000000)
        >>> 
        >>> # LazyFrame for query optimization
        >>> lf = dc.typed_read_data_polars(Company, object_id="Company", lazy=True)
        >>> result = lf.filter(pl.col("Revenue") > 1000000).collect()
    
    Note:
        Unlike typed_read_data(), this does NOT validate data against the model.
        The model is only used for field selection and documentation.
        For validation, use typed_read_data() instead.
    """
    # Auto-detect fields from model if not specified
    if fields is None:
        fields = list(model.model_fields.keys())
    
    output_format = "polars_lazy" if lazy else "polars"
    
    return read.read_data(
        self,
        object_id=object_id,
        view_id=view_id,
        output=output_format,
        fields=fields,
        query=query,
        reference_format=reference_format,
        reference_cache=reference_cache,
        **kwargs,
    )


def typed_read_data_streaming(
    self: "DealCloudData",
    model: Type[T],
    object_id: Optional[Union[int, str]] = None,
    view_id: Optional[Union[int, str]] = None,
    query: Optional[str] = None,
    fields: Optional[List[str]] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    skip_validation_errors: bool = False,
    **kwargs,
) -> Iterator[T]:
    """
    Stream data as typed Pydantic models (memory-efficient).
    
    Typed wrapper around read_data_streaming() - yields model instances
    one at a time instead of dicts.
    
    Args:
        self: DealCloudData instance
        model: Pydantic model class
        object_id: Object API name or ID
        view_id: View ID (alternative to object_id)
        query: Optional DealCloud query string
        fields: Fields to fetch (default: auto-detect from model)
        reference_format: How to format reference fields
        reference_cache: Optional cache for reference name lookups
        skip_validation_errors: If True, skip invalid rows
        **kwargs: Additional args passed to read_data_streaming()
    
    Yields:
        Model instances one at a time
    
    Example:
        >>> for company in dc.typed_read_data_streaming(Company, object_id="Company"):
        ...     process(company)  # Memory-efficient for large datasets
    """
    # Auto-detect fields from model if not specified
    if fields is None:
        fields = list(model.model_fields.keys())
    
    for batch in streaming.read_data_streaming(
        self,
        object_id=object_id,
        view_id=view_id,
        fields=fields,
        **kwargs,
    ):
        for row in batch:
            # Apply reference format if specified
            if reference_format is not None and object_id:
                row = references.apply_reference_format(
                    self, [row], object_id, reference_format, reference_cache
                )[0]
            
            try:
                yield model.model_validate(row)
            except ValidationError as e:
                entry_id = row.get("EntryId") or row.get("entryId")
                if skip_validation_errors:
                    self._logger.warning(
                        f"Validation error for EntryId {entry_id}, skipping: {e}"
                    )
                else:
                    raise


async def typed_aread_data_streaming(
    self: "DealCloudData",
    model: Type[T],
    object_id: Optional[Union[int, str]] = None,
    view_id: Optional[Union[int, str]] = None,
    query: Optional[str] = None,
    fields: Optional[List[str]] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    skip_validation_errors: bool = False,
    **kwargs,
) -> AsyncIterator[T]:
    """
    Async stream data as typed Pydantic models.
    
    Typed wrapper around aread_data_streaming() - async yields model
    instances one at a time.
    
    Args:
        self: DealCloudData instance
        model: Pydantic model class
        object_id: Object API name or ID
        view_id: View ID (alternative to object_id)
        query: Optional DealCloud query string
        fields: Fields to fetch (default: auto-detect from model)
        reference_format: How to format reference fields
        reference_cache: Optional cache for reference name lookups
        skip_validation_errors: If True, skip invalid rows
        **kwargs: Additional args passed to aread_data_streaming()
    
    Yields:
        Model instances one at a time (async)
    
    Example:
        >>> async for company in dc.typed_aread_data_streaming(Company, object_id="Company"):
        ...     await process_async(company)
    """
    # Auto-detect fields from model if not specified
    if fields is None:
        fields = list(model.model_fields.keys())
    
    async for batch in streaming.aread_data_streaming(
        self,
        object_id=object_id,
        view_id=view_id,
        fields=fields,
        **kwargs,
    ):
        for row in batch:
            # Apply reference format if specified
            if reference_format is not None and object_id:
                row = references.apply_reference_format(
                    self, [row], object_id, reference_format, reference_cache
                )[0]
            
            try:
                yield model.model_validate(row)
            except ValidationError as e:
                entry_id = row.get("EntryId") or row.get("entryId")
                if skip_validation_errors:
                    self._logger.warning(
                        f"Validation error for EntryId {entry_id}, skipping: {e}"
                    )
                else:
                    raise


def typed_insert_data(
    self: "DealCloudData",
    object_id: Union[int, str],
    data: List[T],
    model: Type[T],
    **kwargs,
) -> List[T]:
    """
    Insert typed records into DealCloud.
    
    Typed wrapper around insert_data() - accepts and returns Pydantic
    model instances instead of dicts.
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        data: List of Pydantic model instances to insert
        model: Model class (for return type deserialization)
        **kwargs: Additional args passed to insert_data()
    
    Returns:
        List of inserted records as model instances (with EntryIds populated)
    
    Example:
        >>> from pydantic import BaseModel
        >>> from typing import Optional
        >>> 
        >>> class Company(BaseModel):
        ...     EntryId: Optional[int] = None
        ...     Name: str
        ...     Industry: Optional[str] = None
        >>> 
        >>> new_companies = [
        ...     Company(Name="Acme Corp", Industry="Technology"),
        ...     Company(Name="Beta Inc", Industry="Finance"),
        ... ]
        >>> 
        >>> inserted = dc.typed_insert_data("Company", new_companies, Company)
        >>> for c in inserted:
        ...     print(f"Created {c.Name} with ID {c.EntryId}")
    """
    # Convert models to dicts for API
    records = [item.model_dump(exclude_unset=True) for item in data]
    
    result = write.insert_data(self, object_id, records, **kwargs)
    
    # Handle BatchResult
    if isinstance(result, BatchResult):
        result_list = result.results if isinstance(result.results, list) else result.results
    else:
        result_list = result if isinstance(result, list) else result
    
    # Return typed results
    return [model.model_validate(row) for row in result_list]


def typed_update_data(
    self: "DealCloudData",
    object_id: Union[int, str],
    data: List[T],
    model: Type[T],
    **kwargs,
) -> List[T]:
    """
    Update typed records in DealCloud.
    
    Typed wrapper around update_data() - accepts and returns Pydantic
    model instances instead of dicts.
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        data: List of Pydantic models with EntryId set
        model: Model class (for return type deserialization)
        **kwargs: Additional args passed to update_data()
    
    Returns:
        List of updated records as model instances
    
    Example:
        >>> # Fetch, modify, update
        >>> companies = dc.typed_read_data(Company, object_id="Company", query="Industry = 'Tech'")
        >>> for c in companies:
        ...     c.Industry = "Technology"  # Standardize
        >>> 
        >>> updated = dc.typed_update_data("Company", companies, Company)
        >>> print(f"Updated {len(updated)} companies")
    """
    # Convert models to dicts for API
    records = [item.model_dump() for item in data]
    
    result = write.update_data(self, object_id, records, **kwargs)
    
    # Handle BatchResult
    if isinstance(result, BatchResult):
        result_list = result.results if isinstance(result.results, list) else result.results
    else:
        result_list = result if isinstance(result, list) else result
    
    # Return typed results
    return [model.model_validate(row) for row in result_list]


def typed_upsert_data(
    self: "DealCloudData",
    object_id: Union[int, str],
    data: List[T],
    model: Type[T],
    match_field: str,
    **kwargs,
) -> List[T]:
    """
    Upsert typed records (insert or update based on match field).
    
    Typed wrapper around upsert_data() - accepts and returns Pydantic
    model instances instead of dicts.
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        data: List of Pydantic model instances
        model: Model class (for return type deserialization)
        match_field: Field API name to match on (must be unique in DealCloud)
        **kwargs: Additional args passed to upsert_data()
    
    Returns:
        List of upserted records as model instances (with EntryIds)
    
    Example:
        >>> class Company(BaseModel):
        ...     EntryId: Optional[int] = None
        ...     Name: str
        ...     CrmId: str  # External system ID
        ...     Revenue: Optional[float] = None
        >>> 
        >>> # Sync from external CRM system
        >>> crm_companies = [
        ...     Company(Name="Acme Corp", CrmId="CRM-123", Revenue=1000000),
        ...     Company(Name="New Corp", CrmId="CRM-456", Revenue=500000),
        ... ]
        >>> 
        >>> result = dc.typed_upsert_data(
        ...     "Company",
        ...     crm_companies,
        ...     Company,
        ...     match_field="CrmId"  # Match on CRM ID
        ... )
        >>> 
        >>> for c in result:
        ...     print(f"{c.Name}: EntryId={c.EntryId}")
    """
    # Convert models to dicts for API (exclude_unset keeps insert-friendly)
    records = [item.model_dump(exclude_unset=True) for item in data]
    
    result = write.upsert_data(self, object_id, records, **kwargs)
    
    # Return typed results
    return [model.model_validate(row) for row in result]
