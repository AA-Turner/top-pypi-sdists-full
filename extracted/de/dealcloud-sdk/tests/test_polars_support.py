"""Tests for Polars DataFrame support."""

from datetime import datetime

import pytest
from unittest.mock import MagicMock, patch
from typing import Optional

import pandas as pd

# Try to import polars - tests will skip if not available
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None

from pydantic import BaseModel

from dealcloud_sdk.cells.dealcloud_cells import DealCloudCells
from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.converters import convert_to_polars
from dealcloud_sdk.data.models import ModifiedEntry
from dealcloud_sdk.utils.data_utils import format_data


# Skip all tests if polars is not installed
pytestmark = pytest.mark.skipif(
    not POLARS_AVAILABLE,
    reason="Polars not installed"
)


# Test model
class Company(BaseModel):
    EntryId: int
    Name: str
    Revenue: Optional[float] = None


class TestPolarsOutputFormats:
    """Tests for output='polars' and output='polars_lazy' in read_data()."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock REST client."""
        client = MagicMock()
        client.get.return_value = {
            "rows": [
                {"EntryId": 1, "Name": "Acme Corp", "Revenue": 1000000},
                {"EntryId": 2, "Name": "Beta Inc", "Revenue": 500000},
            ],
            "totalRecords": 2,
        }
        return client
    
    @pytest.fixture
    def dc_data(self, mock_client):
        """Create DealCloudData instance with mocked client."""
        # Use MagicMock() without spec so _rows_url and other instance attrs can be set.
        dc = MagicMock()
        dc._client = mock_client
        dc._rows_url = "/api/rest/v4/data/entrydata/rows"
        dc._query_url = "/api/rest/v4/data/entrydata/rows/query"
        dc._views_url = "/api/rest/v4/data/views"
        dc.page_size = 1000
        dc.read_concurrency = 4
        dc._logger = MagicMock()

        # read_data -> read_object -> read_data_streaming -> _client.get_paginated
        mock_client.get_paginated.return_value = iter([
            [
                {"EntryId": 1, "Name": "Acme Corp", "Revenue": 1000000},
                {"EntryId": 2, "Name": "Beta Inc", "Revenue": 500000},
            ],
        ])

        dc.read_data = DealCloudData.read_data.__get__(dc, DealCloudData)
        dc._get_reference_fields = MagicMock(return_value=[])
        dc._apply_reference_format = MagicMock(side_effect=lambda rows, **kw: rows)

        return dc
    
    def test_read_data_polars_output(self, dc_data):
        """Test read_data with output='polars' returns Polars DataFrame."""
        result = dc_data.read_data(object_id="Company", output="polars")
        
        assert isinstance(result, pl.DataFrame)
        assert result.shape == (2, 3)
        assert result.columns == ["EntryId", "Name", "Revenue"]
        assert result["Name"].to_list() == ["Acme Corp", "Beta Inc"]
    
    def test_read_data_polars_lazy_output(self, dc_data):
        """Test read_data with output='polars_lazy' returns Polars LazyFrame."""
        result = dc_data.read_data(object_id="Company", output="polars_lazy")
        
        assert isinstance(result, pl.LazyFrame)
        
        # Collect to verify data
        df = result.collect()
        assert df.shape == (2, 3)
        assert df["Name"].to_list() == ["Acme Corp", "Beta Inc"]
    
    def test_read_data_polars_lazy_query_optimization(self, dc_data):
        """Test that LazyFrame allows query optimization."""
        result = dc_data.read_data(object_id="Company", output="polars_lazy")
        
        # Apply filter (lazy - not executed yet)
        filtered = result.filter(pl.col("Revenue") > 750000)
        
        # Now collect
        df = filtered.collect()
        assert df.shape == (1, 3)
        assert df["Name"].to_list() == ["Acme Corp"]
    
    def test_read_data_polars_empty_result(self, dc_data):
        """Test polars output with empty result."""
        dc_data._client.get_paginated.return_value = iter([[]])

        result = dc_data.read_data(object_id="Company", output="polars")

        assert isinstance(result, pl.DataFrame)
        assert result.shape[0] == 0
    
    def test_read_data_invalid_output_raises(self, dc_data):
        """Test that invalid output format raises ValueError."""
        with pytest.raises(ValueError, match="output must be one of"):
            dc_data.read_data(object_id="Company", output="invalid")
    
    def test_read_data_output_required(self, dc_data):
        """Test that output parameter is required."""
        with pytest.raises(ValueError, match="output.*parameter is required"):
            dc_data.read_data(object_id="Company")


class TestPolarsInputFormats:
    """Tests for accepting Polars DataFrames as input to write operations."""
    
    def test_format_data_polars_dataframe(self):
        """Test format_data converts Polars DataFrame to list of dicts."""
        df = pl.DataFrame({
            "EntryId": [1, 2],
            "Name": ["Acme", "Beta"],
            "Revenue": [1000, 2000],
        })
        
        data, columns = format_data(df)
        
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0] == {"EntryId": 1, "Name": "Acme", "Revenue": 1000}
        assert columns == {"EntryId", "Name", "Revenue"}
    
    def test_format_data_pandas_dataframe(self):
        """Test format_data still works with pandas DataFrame."""
        df = pd.DataFrame({
            "EntryId": [1, 2],
            "Name": ["Acme", "Beta"],
        })
        
        data, columns = format_data(df)
        
        assert isinstance(data, list)
        assert len(data) == 2
        assert columns == {"EntryId", "Name"}
    
    def test_format_data_list_of_dicts(self):
        """Test format_data passes through list of dicts."""
        original = [{"Name": "Acme"}, {"Name": "Beta"}]
        
        data, columns = format_data(original)
        
        assert data == original
        assert columns == {"Name"}


class TestTypedMethodsPolars:
    """Tests for typed methods with Polars support."""
    
    @pytest.fixture
    def mock_dc(self):
        """Create a mock DealCloudData instance."""
        dc = MagicMock()
        dc._logger = MagicMock()
        dc._rows_url = "/api/rest/v4/data/entrydata/rows"
        return dc

    @patch("dealcloud_sdk.data.typed.read.read_data")
    def test_typed_read_data_polars(self, mock_read_data, mock_dc):
        """Test typed_read_data_polars returns Polars DataFrame."""
        mock_read_data.return_value = pl.DataFrame({
            "EntryId": [1, 2],
            "Name": ["Acme", "Beta"],
            "Revenue": [1000.0, 2000.0],
        })

        mock_dc.typed_read_data_polars = DealCloudData.typed_read_data_polars.__get__(
            mock_dc, DealCloudData
        )

        result = mock_dc.typed_read_data_polars(Company, object_id="Company")

        assert isinstance(result, pl.DataFrame)
        mock_read_data.assert_called_once()
        call_kwargs = mock_read_data.call_args[1]
        assert call_kwargs["output"] == "polars"
        assert set(call_kwargs["fields"]) == {"EntryId", "Name", "Revenue"}

    @patch("dealcloud_sdk.data.typed.read.read_data")
    def test_typed_read_data_polars_lazy(self, mock_read_data, mock_dc):
        """Test typed_read_data_polars with lazy=True returns LazyFrame."""
        mock_read_data.return_value = pl.DataFrame({
            "EntryId": [1],
            "Name": ["Test"],
            "Revenue": [1000.0],
        }).lazy()

        mock_dc.typed_read_data_polars = DealCloudData.typed_read_data_polars.__get__(
            mock_dc, DealCloudData
        )

        result = mock_dc.typed_read_data_polars(Company, object_id="Company", lazy=True)

        assert isinstance(result, pl.LazyFrame)
        call_kwargs = mock_read_data.call_args[1]
        assert call_kwargs["output"] == "polars_lazy"


class TestConvertToPolars:
    """Tests for convert_to_polars helper (dealcloud_sdk.data.converters)."""
    
    def test_convert_empty_list(self):
        """Test converting empty list to Polars DataFrame."""
        result = convert_to_polars([], "polars")
        
        assert isinstance(result, pl.DataFrame)
        assert result.shape[0] == 0
    
    def test_convert_empty_list_lazy(self):
        """Test converting empty list to Polars LazyFrame."""
        result = convert_to_polars([], "polars_lazy")
        
        assert isinstance(result, pl.LazyFrame)
    
    def test_convert_list_of_dicts(self):
        """Test converting list of dicts to Polars DataFrame."""
        rows = [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"},
        ]
        
        result = convert_to_polars(rows, "polars")
        
        assert isinstance(result, pl.DataFrame)
        assert result.shape == (2, 2)
        assert result.columns == ["id", "name"]
    
    def test_convert_to_lazyframe(self):
        """Test converting to LazyFrame."""
        rows = [{"id": 1}]
        
        result = convert_to_polars(rows, "polars_lazy")
        
        assert isinstance(result, pl.LazyFrame)
        # Collect to verify data
        df = result.collect()
        assert df.shape == (1, 1)


class TestPolarsImportError:
    """Tests for handling missing polars installation."""

    def test_convert_to_polars_import_error(self):
        """Test helpful error when polars is not installed."""
        import builtins
        real_import = builtins.__import__

        def raise_for_polars(name, *args, **kwargs):
            if name == "polars":
                raise ImportError("No module named 'polars'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=raise_for_polars):
            with pytest.raises(ImportError, match="pip install dealcloud-sdk\\[polars\\]"):
                convert_to_polars([], "polars")


class TestPolarsIntegration:
    """Integration tests for Polars with real data operations."""
    
    def test_polars_operations_chain(self):
        """Test that Polars operations work correctly on SDK output."""
        # Simulate SDK output
        data = [
            {"EntryId": 1, "Name": "Acme", "Revenue": 1000000, "Industry": "Tech"},
            {"EntryId": 2, "Name": "Beta", "Revenue": 500000, "Industry": "Finance"},
            {"EntryId": 3, "Name": "Gamma", "Revenue": 750000, "Industry": "Tech"},
        ]
        
        df = pl.DataFrame(data)
        
        # Group by and aggregate
        result = df.group_by("Industry").agg([
            pl.col("Revenue").sum().alias("TotalRevenue"),
            pl.col("Name").count().alias("Count"),
        ]).sort("Industry")
        
        assert result.shape == (2, 3)
        assert result.filter(pl.col("Industry") == "Tech")["TotalRevenue"].to_list()[0] == 1750000
    
    def test_polars_lazy_optimization(self):
        """Test that LazyFrame allows query optimization."""
        data = [
            {"EntryId": i, "Value": i * 100}
            for i in range(1000)
        ]
        
        lf = pl.LazyFrame(data)
        
        # Build complex query (lazy - not executed)
        result = (
            lf
            .filter(pl.col("Value") > 50000)
            .select([pl.col("EntryId"), pl.col("Value") * 2])
        )
        
        # Execute
        df = result.collect()
        
        assert df.shape[0] == 499  # Values > 500 (i.e., i > 500)
        assert df.columns == ["EntryId", "Value"]
    
    def test_polars_to_pandas_conversion(self):
        """Test converting between Polars and pandas."""
        # This test requires pyarrow for conversion
        try:
            import pyarrow
        except ImportError:
            pytest.skip("pyarrow required for polars<->pandas conversion")
        
        df_polars = pl.DataFrame({
            "Name": ["Acme", "Beta"],
            "Revenue": [1000, 2000],
        })
        
        # Convert to pandas
        df_pandas = df_polars.to_pandas()
        
        assert isinstance(df_pandas, pd.DataFrame)
        assert df_pandas.shape == (2, 2)
        
        # Convert back to polars
        df_back = pl.from_pandas(df_pandas)
        
        assert isinstance(df_back, pl.DataFrame)
        assert df_back.shape == (2, 2)


class TestPolarsWriteOutput:
    """Tests for insert_data / update_data / upsert_data with output='polars'."""

    @pytest.fixture
    def dc_write(self):
        mock_client = MagicMock()
        mock_client.post.return_value = [{"EntryId": 101, "Name": "N", "Revenue": 1.0}]
        mock_client.put.return_value = [{"EntryId": 102, "Name": "U", "Revenue": 2.0}]
        dc = MagicMock()
        dc._client = mock_client
        dc._rows_url = "/api/rest/v4/data/entrydata/rows"
        dc.cell_pagination_limit = 10**9
        dc.create_concurrency = 4
        dc._logger = MagicMock()
        dc.insert_data = DealCloudData.insert_data.__get__(dc, DealCloudData)
        dc.update_data = DealCloudData.update_data.__get__(dc, DealCloudData)
        dc.upsert_data = DealCloudData.upsert_data.__get__(dc, DealCloudData)
        return dc

    @patch("dealcloud_sdk.data.write.validate_field_mapping")
    def test_insert_data_polars_output(self, mock_vf, dc_write):
        """insert_data with output='polars' returns Polars DataFrame."""
        mock_vf.return_value = True
        result = dc_write.insert_data(
            "Company", [{"Name": "N", "Revenue": 1.0}], output="polars"
        )
        assert isinstance(result, pl.DataFrame)
        assert result["EntryId"].to_list() == [101]

    @patch("dealcloud_sdk.data.write.validate_field_mapping")
    def test_update_data_polars_output(self, mock_vf, dc_write):
        """update_data with output='polars' returns Polars DataFrame."""
        mock_vf.return_value = True
        result = dc_write.update_data(
            "Company",
            [{"EntryId": 102, "Name": "U", "Revenue": 2.0}],
            output="polars",
        )
        assert isinstance(result, pl.DataFrame)
        assert result["EntryId"].to_list() == [102]

    @patch("dealcloud_sdk.data.write.validate_field_mapping")
    def test_upsert_data_polars_output(self, mock_vf, dc_write):
        """upsert_data with output='polars' returns Polars DataFrame."""
        mock_vf.return_value = True
        result = dc_write.upsert_data(
            "Company",
            [{"EntryId": 102, "Name": "Up"}],
            output="polars",
        )
        assert isinstance(result, pl.DataFrame)
        assert result["EntryId"].to_list() == [102]


class TestSyncDeltaPolarsOutput:
    """Tests for sync_delta with polars / polars_lazy output."""

    @patch("dealcloud_sdk.data.read.read_data")
    @patch("dealcloud_sdk.data.delta_sync.get_modified_entries")
    def test_sync_delta_polars_output(self, mock_get, mock_read):
        mock_get.return_value = [
            ModifiedEntry(entry_id=1, modified_date=datetime.now(), is_deleted=False)
        ]
        mock_read.return_value = pl.DataFrame({"EntryId": [1], "Name": ["A"]})

        dc = MagicMock()
        dc._data_url = "https://test.dealcloud.com/api/rest/v4/data"
        dc.sync_delta = DealCloudData.sync_delta.__get__(dc, DealCloudData)

        result = dc.sync_delta("Company", datetime.now(), output="polars")
        assert isinstance(result.modified_data, pl.DataFrame)
        assert result.modified_data["EntryId"].to_list() == [1]

    @patch("dealcloud_sdk.data.read.read_data")
    @patch("dealcloud_sdk.data.delta_sync.get_modified_entries")
    def test_sync_delta_polars_lazy_output(self, mock_get, mock_read):
        mock_get.return_value = [
            ModifiedEntry(entry_id=1, modified_date=datetime.now(), is_deleted=False)
        ]
        mock_read.return_value = pl.DataFrame({"EntryId": [1], "Name": ["A"]}).lazy()

        dc = MagicMock()
        dc._data_url = "https://test.dealcloud.com/api/rest/v4/data"
        dc.sync_delta = DealCloudData.sync_delta.__get__(dc, DealCloudData)

        result = dc.sync_delta("Company", datetime.now(), output="polars_lazy")
        assert isinstance(result.modified_data, pl.LazyFrame)


class TestWriteCellsDataFrameInput:
    """write_cells accepts pandas and Polars DataFrames."""

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_write_cells_polars_input_create(self, mock_client_class, mock_get_field):
        mock_client = MagicMock()
        mock_client.post.return_value = [
            {"entryId": -1, "fieldId": 10, "rowId": 1001, "value": "New Company"}
        ]
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        df = pl.DataFrame({"EntryId": [-1], "Name": ["New Company"]})
        result = cells.write_cells("Company", df, mode="create")
        assert len(result) == 1
        mock_client.post.assert_called_once()

    @patch("dealcloud_sdk.cells.dealcloud_cells.DealCloudCells.get_field_by_api_name")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_write_cells_pandas_input_create(self, mock_client_class, mock_get_field):
        mock_client = MagicMock()
        mock_client.post.return_value = [
            {"entryId": -1, "fieldId": 10, "rowId": 1001, "value": "New Company"}
        ]
        mock_client_class.return_value = mock_client
        mock_get_field.return_value = MagicMock(id=10)

        cells = DealCloudCells(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        df = pd.DataFrame({"EntryId": [-1], "Name": ["New Company"]})
        result = cells.write_cells("Company", df, mode="create")
        assert len(result) == 1
        mock_client.post.assert_called_once()

