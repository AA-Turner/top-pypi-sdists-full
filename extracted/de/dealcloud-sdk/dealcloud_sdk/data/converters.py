"""Output format conversion utilities."""

from typing import TYPE_CHECKING, List, Literal, Union
import pandas as pd

if TYPE_CHECKING:
    import polars as pl

OutputFormat = Literal["list", "pandas", "polars", "polars_lazy", "write_result"]


def convert_to_output_format(
    rows: List[dict], 
    output: OutputFormat
) -> Union[List[dict], pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"]:
    """
    Convert rows to the requested output format.
    
    Args:
        rows: List of row dictionaries
        output: Target output format
        
    Returns:
        Data in the requested format
    """
    if output == "list":
        return rows
    elif output == "pandas":
        return pd.DataFrame(rows) if rows else pd.DataFrame()
    elif output in ("polars", "polars_lazy"):
        return convert_to_polars(rows, output)
    else:
        raise ValueError(f"Unknown output format: {output}")


def convert_to_polars(
    rows: List[dict], 
    output: Literal["polars", "polars_lazy"]
) -> Union["pl.DataFrame", "pl.LazyFrame"]:
    """
    Convert rows to Polars DataFrame or LazyFrame.
    
    Args:
        rows: List of row dictionaries
        output: "polars" for DataFrame, "polars_lazy" for LazyFrame
    
    Returns:
        Polars DataFrame or LazyFrame
    
    Raises:
        ImportError: If polars is not installed
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "Polars is not installed. Install with: pip install dealcloud-sdk[polars]"
        )
    
    if not rows:
        # Return empty DataFrame/LazyFrame with no schema
        if output == "polars_lazy":
            return pl.LazyFrame()
        return pl.DataFrame()
    
    # Convert list of dicts to Polars DataFrame
    df = pl.DataFrame(rows)
    
    if output == "polars_lazy":
        return df.lazy()
    
    return df
