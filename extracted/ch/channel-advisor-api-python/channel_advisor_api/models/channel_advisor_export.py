from functools import cached_property
import zipfile
from channel_advisor_api.utils.logger import get_logger
from pydantic import BaseModel, Field
from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient
from typing import Optional
import requests
import pandas as pd
from io import BytesIO

logger = get_logger(__name__)


class ProductExportResponse(BaseModel):
    id: str = Field(alias="$id")
    token: str = Field(alias="Token")
    status: str = Field(alias="Status")
    started_on_utc: str = Field(alias="StartedOnUtc")
    response_file_url: Optional[str] = Field(None, alias="ResponseFileUrl")


class ProductExportS3Location(BaseModel):
    s3_bucket: str
    s3_key: str


class ChannelAdvisorExport(BaseModel):
    _base_uri = "ProductExport"
    _client: ChannelAdvisorClient

    def __init__(self, client: ChannelAdvisorClient = None):
        super().__init__()
        self._client = client or ChannelAdvisorClient()

    @cached_property
    def client(self) -> ChannelAdvisorClient:
        return self._client

    def request_export(self, filter: str = None) -> ProductExportResponse:
        params = {"filter": filter} if filter else {}
        response = self.client.request("POST", self._base_uri, params=params)
        logger.info(f"Export request response: {response.json()}")
        return ProductExportResponse(**response.json())

    def get_export_status(self, token: str) -> ProductExportResponse:
        params = {"token": token}
        response = self.client.request("GET", self._base_uri, params=params)
        logger.info(f"Export status response: {response.json()}")
        return ProductExportResponse(**response.json())

    def export_is_complete(self, token: str) -> bool:
        status = self.get_export_status(token).status
        for failure_status in ["Error", "Failed", "Aborted"]:
            if failure_status in status:
                raise ValueError(f"Export token {token} failed with status: {status}")
        logger.info(f"Export token {token} status is: {status}")
        return status == "Complete"

    def export_to_df(self, token: str) -> pd.DataFrame:
        url = self.get_export_status(token).response_file_url
        if not url:
            raise ValueError("Export file URL not available")

        # download export using requests with streaming enabled
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Try to read as zip file
        with zipfile.ZipFile(BytesIO(response.content), "r") as zip_ref:
            # Find the first .txt file in the zip
            txt_files = [f for f in zip_ref.namelist() if f.endswith(".txt")]
            if not txt_files:
                raise ValueError("No .txt file found in zip archive")

            with zip_ref.open(txt_files[0]) as file:
                # First read to get column names
                header_df = pd.read_csv(file, sep="\t", nrows=0)
                columns = header_df.columns

                # Reset file pointer to beginning
                file.seek(0)

                # Identify datetime columns
                date_columns = [
                    col
                    for col in columns
                    if any(time_word in col.lower() for time_word in ["date", "time", "created", "modified", "updated"])
                ]

                # Identify boolean columns (common boolean column names)
                bool_columns = [
                    col
                    for col in columns
                    if any(
                        bool_word in col.lower()
                        for bool_word in ["is", "has", "can", "allow", "enabled", "active", "visible"]
                    )
                ]

                # First read everything as string to identify columns with boolean values
                temp_df = pd.read_csv(file, sep="\t", dtype=str, nrows=1000)
                file.seek(0)  # Reset file pointer again

                # Find additional boolean columns by checking content
                for col in columns:
                    if col not in bool_columns:
                        unique_vals = set(temp_df[col].dropna().unique())
                        if unique_vals.issubset({"True", "False", ""}) and len(unique_vals) > 0:
                            bool_columns.append(col)

                # Identify columns that must always be strings
                string_columns = [
                    col
                    for col in columns
                    if any(id_word in col.lower() for id_word in ["sku", "id", "code", "number", "upc", "ean", "isbn"])
                ]

                # Read CSV with specific data types
                df = pd.read_csv(
                    file,
                    sep="\t",
                    dtype={
                        **{col: str for col in columns},  # default all to string
                        **{col: str for col in string_columns},  # ensure ID-like columns are strings
                        **{
                            col: "Int64"  # Use nullable integer type
                            for col in columns
                            if ("Quantity" in col or "Qty" in col)
                            and "Suggestion" not in col
                            and col not in date_columns
                            and col not in bool_columns
                            and col not in string_columns  # exclude string columns from integer conversion
                        },
                        **{
                            col: float
                            for col in columns
                            if ("Cost" in col or "Price" in col)
                            and "Competitor" not in col
                            and "Dealer" not in col
                            and "SalePrice" not in col
                            and col not in date_columns
                            and col not in bool_columns
                            and col not in string_columns  # exclude string columns from float conversion
                        },
                    },
                    parse_dates=date_columns,  # Convert date columns to datetime
                    na_values=["", "nan", "NaN", "NULL"],
                    keep_default_na=False,
                )

                # Fill NA values based on column type
                for col in df.columns:
                    if df[col].dtype == "Int64":
                        df[col] = df[col].fillna(0)
                    elif df[col].dtype == "float64":
                        df[col] = df[col].fillna(0.0)
                    elif col not in date_columns:  # Don't fill NA in date columns
                        df[col] = df[col].fillna("")

                # Convert boolean columns after handling NA values
                for col in bool_columns:
                    df[col] = df[col].map({"True": True, "False": False, "": False})

                return df


def transform_attributes(ca_catalog: pd.DataFrame) -> pd.DataFrame:
    # Create a list of attribute pairs (name and value columns)
    attribute_pairs = [(f"Attribute{i}Name", f"Attribute{i}Value") for i in range(1, 142)]

    # Initialize an empty dictionary to store the transformed data
    transformed_data = {}

    # Iterate through each attribute pair
    for name_col, value_col in attribute_pairs:
        # Get unique attribute names from the name column
        attr_names = ca_catalog[name_col].dropna().unique()

        # For each unique attribute name, create a new column with the corresponding values
        for attr_name in attr_names:
            if pd.notna(attr_name):  # Skip empty/null attribute names
                # Create column name with 'attr:' prefix
                new_col_name = f"attr:{attr_name}"
                # Get values where attribute name matches
                mask = ca_catalog[name_col] == attr_name
                transformed_data[new_col_name] = ca_catalog[value_col].where(mask, "").fillna("").astype(str)

    # Create a new dataframe with the transformed attributes
    attr_df = pd.DataFrame(transformed_data)

    # Combine with original dataframe (excluding the original attribute columns)
    original_cols = [col for col in ca_catalog.columns if not col.startswith("Attribute")]
    result_df = pd.concat([ca_catalog[original_cols], attr_df], axis=1)
    return result_df
