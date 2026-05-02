import math
from urllib.parse import urljoin
import numpy as np
import orjson
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError, DataNotFound
from ..utils.transformations import to_snake_case


class AutoTask(HTTPService, FlowComponent):
    """
    AutoTask Component

        Overview

        This component retrieves data from AutoTask using the Autotask REST API.
        It supports filtering data based on a query or specific IDs, handles pagination, and converts picklist values to human-readable labels.

        :widths: auto

    |  credentials                    |   Yes    | Dictionary containing API credentials: "API_INTEGRATION_CODE", "USERNAME", and "SECRET". Credentials can be retrieved from environment variables. |
    |  zone                           |   Yes    | AutoTask zone (e.g., "na").                                                                                                                       |
    |  entity                         |   Yes    | AutoTask entity to query (e.g., "tickets").                                                                                                       |
    |  query_json                     |   No     | JSON object representing the AutoTask query filter (defaults to retrieving all items). Refer to AutoTask documentation for query syntax.          |
    |  id_column_name                 |   No     | Name of the column in the output DataFrame that should represent the AutoTask record ID (defaults to "id").                                       |
    |  ids                            |   No     | List of AutoTask record IDs to retrieve (overrides query_json filter if provided).                                                                |
    |  picklist_fields                |   No     | List of picklist fields in the entity to be converted to human-readable labels.                                                                   |
    |  user_defined_fields            |   No     | List of user-defined fields in the entity to extract (requires "userDefinedFields" field in the response).                                        |
    |  fillna_values                  |   No     | Default value to replace missing data (defaults to None).                                                                                         |
    |  map_field_type                 |   No     | Dictionary mapping field names to desired data types in the output DataFrame.                                                                     |
    | force_create_columns            |   No     | If True, ensures "IncludeFields" columns always exist, even if empty. Must be used with "IncludeFields" in "query_json".                          |

        Returns a pandas DataFrame containing the retrieved AutoTask data and additional columns for picklist labels (if applicable).



    Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          AutoTask:
          skipError: skip
          credentials:
          API_INTEGRATION_CODE: AUTOTASK_API_INTEGRATION_CODE
          USERNAME: AUTOTASK_USERNAME
          SECRET: AUTOTASK_SECRET
          entity: TicketNotes
          zone: webservices14
          id_column_name: ticket_note_id
          picklist_fields:
          - noteType
          - publish
          ids: []
          query_json:
          IncludeFields:
          - id
          - createDateTime
          - createdByContactID
          - creatorResourceID
          - description
          - impersonatorCreatorResourceID
          - impersonatorUpdaterResourceID
          - lastActivityDate
          - noteType
          - publish
          - ticketID
          - title
          Filter:
          - op: gte
          field: lastActivityDate
          value: '{two_days_ago}'
          masks:
          '{two_days_ago}':
          - date_diff
          - value: current_date
          diff: 48
          mode: hours
          mask: '%Y-%m-%d %H:%M:%S'
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {"API_INTEGRATION_CODE": str, "USERNAME": str, "SECRET": str}
    force_create_columns: bool = False

    async def start(self, **kwargs):
        self.headers = None
        self._proxies = None
        self.auth = ""
        self.auth_type = ""
        self.timeout = 180
        self.accept = "application/json"
        self.query_json = self.mask_replacement_recursively(self.query_json)
        self.processing_credentials()

        self._base_url = (
            f"https://{self.zone}.autotask.net/atservicesrest/v1.0/{self.entity}/"
        )

        self.headers = {
            "Content-Type": "application/json",
            "ApiIntegrationCode": self.credentials["API_INTEGRATION_CODE"],
            "UserName": self.credentials["USERNAME"],
            "Secret": self.credentials["SECRET"],
        }

        self.ids_chunks = []
        if self.previous:
            self.data = self.input

            self.ids_chunks = self.filter_ids(
                id_field=self.id_column_name,
                items=self.data,
                chunk_size=500,
            )
        elif getattr(self, "ids", None):
            self._logger.info("Dropping specified Filters. Using ids instead.")
            self.ids_chunks = [self.ids]

        return True

    async def run(self):
        if not self.ids_chunks:
            # Use the Filter specified in the task
            df_items = await self.get_dataframe_from_entity(
                payload=orjson.dumps(self.query_json),
                id_column_name=self.id_column_name,
            )
        else:
            # Use the ids from the previous component or from the ids argument
            df_items = pd.DataFrame()
            for ids_chunk in self.ids_chunks:
                self.query_json.update(
                    {
                        "Filter": [
                            {"op": "in", "field": "id", "value": ids_chunk.tolist()}
                        ]
                    }
                )

                items = await self.get_dataframe_from_entity(
                    payload=orjson.dumps(self.query_json),
                    id_column_name=self.id_column_name,
                )

                df_items = pd.concat([df_items, items], ignore_index=True)

        if not df_items.empty and self.picklist_fields:
            df_picklist_values = await self.get_picklist_values(self.picklist_fields)

            if not getattr(df_picklist_values, "empty", True):

                for column in [to_snake_case(field) for field in self.picklist_fields]:
                    df_filtered = df_picklist_values[df_picklist_values['field'] == column]

                    # Merge the label into df_items
                    df_items = df_items.merge(
                        df_filtered[['label', 'value']],
                        how='left',
                        left_on=column,
                        right_on='value'
                    )

                    # Rename the label column to reflect the original field
                    df_items.rename(columns={'label': f'{column}_label'}, inplace=True)

                    # Drop the 'value' column from the merge
                    df_items.drop(columns=['value'], inplace=True)

        if "IncludeFields" in self.query_json  and self.force_create_columns:
            required_columns = self._get_force_create_columns()

            if df_items.empty:
                # Create a DataFrame with one row filled with NaNs based on IncludeFields
                empty_dataset = {field: [pd.NA] for field in required_columns}
                df_items = pd.DataFrame(empty_dataset)
            else:
                df_items = df_items.reindex(columns=required_columns, fill_value=pd.NA)

        self._result = df_items
            # Add Debugging Block
        if self._debug is True:
            print("::: Printing Result Data === ")
            print("Data: ", self._result)
            for column, t in df_items.dtypes.items():
                print(column, "->", t, "->", df_items[column].iloc[0])
        return self._result

    async def close(self):
        pass

    def _get_force_create_columns(self):
            required_columns = list(map(to_snake_case, self.query_json["IncludeFields"]))

            try:
                idx = required_columns.index("id")
                required_columns[idx] = self.id_column_name
                
                return required_columns
            
            except ValueError:
                self.logger.error("The item 'id' was not found in the list.")

    def filter_ids(self, id_field: str, items: pd.DataFrame, chunk_size):
        data = items[id_field].dropna().unique().astype(int)

        if data.size > 0:
            split_n = math.ceil(data.size / chunk_size)

            # Split into chunks of n items
            return np.array_split(data, split_n)  # Convert to NumPy array and split

        return [data]

    def get_autotask_url(self, resource):
        return urljoin(self._base_url, resource)

    async def get_dataframe_from_entity(self, payload, id_column_name):
        args = {
            "url": self.get_autotask_url("query"),
            "method": "post",
            "data": payload,
        }

        results = []
        while True:
            result, error = await self.session(**args)

            if error:
                self._logger.error(f"{__name__}: Error getting {self.entity}")
                raise ComponentError(f"{__name__}: Error getting {self.entity}") from error

            if result is None:
                self._logger.error(f"API returned None or empty result for {args['url']}")
                raise ComponentError(f"API returned None or empty result for {args['url']}")

            if "items" not in result:
                self._logger.error(f"'items' not found in API response: {result}")
                raise ComponentError("'items' not found in API response")

            results.extend(result.get("items", []))

            args.update({"url": result["pageDetails"].get("nextPageUrl", None)})

            if not args["url"]:
                break
        try:
            df_results = await self.create_dataframe(results)
        except DataNotFound as e:
            if self.force_create_columns:
                return pd.DataFrame()
            
            raise e

        if not df_results.empty and "userDefinedFields" in df_results.columns:
            df_results_udf = df_results["userDefinedFields"].apply(self.extract_udf)
            df_results = df_results.drop("userDefinedFields", axis=1, errors="ignore").join(df_results_udf)

        df_results = (
            df_results.rename(columns=lambda x: to_snake_case(x))
            .rename(columns={"id": id_column_name})
        )

        return df_results

    @staticmethod
    def extract_udf(row):
        """ Extracts dictionary values into columns"""
        return pd.Series({d['name']: d['value'] for d in row})

    async def get_picklist_values(self, field_names: list[str]) -> pd.DataFrame:
        result, error = await self.session(
            url=self.get_autotask_url("entityInformation/fields"),
            method="get",
        )

        if error:
            self._logger.error(f"{__name__}: Error getting {self.entity}")
            raise ComponentError(f"{__name__}: Error getting {self.entity}") from error

        picklist_data = []

        for field_name in field_names:
            for field in result["fields"]:
                if field["name"] == field_name:
                    self._logger.info(f"Extracting picking list values for {field_name}")

                    if not field["picklistValues"]:
                        df = pd.DataFrame(columns=["label", "value"])
                    else:
                        df = await self.create_dataframe(field["picklistValues"])
                        df = df[["label", "value"]]

                    df["field"] = to_snake_case(field_name)
                    picklist_data.append(df)

        # Concatenate all DataFrames and reset the index
        combined_df = pd.concat(picklist_data).reset_index(drop=True).astype({"value": "int"})
        return combined_df[["field", "label", "value"]]
