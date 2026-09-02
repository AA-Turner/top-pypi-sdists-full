from math import ceil
from typing import Any, Optional, Union

import numpy as np
import pandas as pd
from requests.exceptions import HTTPError

from dealcloud_sdk.constants import field_types
from dealcloud_sdk.constants.data import (
    DATA_READ_WORKER_COUNT,
    DELETION_PAGINATION_LIMIT,
    VIEW_READ_WORKER_COUNT,
)
from dealcloud_sdk.models.data import Rows
from dealcloud_sdk.models.schema import Field
from dealcloud_sdk.schema.dealcloud_schema import DealCloudSchema
from dealcloud_sdk.utils.common_argument_parse import parse_output_argument
from dealcloud_sdk.utils.data_utils import (
    calculate_pagination,
    divide_pages,
    flatten_nested_list,
    format_data,
    rows_query_payload_builder,
)
from dealcloud_sdk.utils.process_response_errors import process_errors
from dealcloud_sdk.utils.request_retry import (
    multi_threaded_request_with_retry,
    request_with_retry,
)
from dealcloud_sdk.utils.resolve_references import resolve_object


class DealCloudData(DealCloudSchema):
    """
    Data Endpoint Methods
    """

    def list_configured_views(self, is_private: Optional[bool] = None) -> Rows:
        """
        Return a summary of configured views
        Args:
            is_private (bool): returns only private views

        Returns:
            (Rows): a count of the total number of views, as well as the view information

        """
        url = f"{self._views_url}"
        if is_private:
            url = f"{url}?isprivate={is_private}"
        response = request_with_retry("GET", url, self._get_access_token)
        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError(
                f"Could not fetch DealCloud objects, response: {response.text}"
            )

        return Rows(**response.json())

    def _get_choice_reference_fields(self, object_id: Union[str, int]) -> list[Field]:
        """
        Pull all choice, reference and user fields for a given object
        Args:
            object_id(Union[str, int]): the object id or api name to query

        Returns:
            list[Field]: the configured choice, reference and user fields
        """
        fields = self.get_fields(object_id)
        return list(
            filter(
                lambda x: x.fieldType
                in [
                    field_types.REFERENCE,
                    field_types.CHOICE,
                    field_types.USER,
                ],
                [c for c in fields],
            )
        )

    def read_data(
        self,
        object_id: Union[int, str, None] = None,
        view_id: Union[int, str, None] = None,
        output: str = "pandas",
        resolve: Optional[str] = None,
        view_filter: Optional[list[dict]] = None,
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        include_nulls: bool = True,
        column_headers: str = "api",
    ) -> Union[list[dict], pd.DataFrame]:
        """
        Read data from a dealcloud object or view into a python dictionary or pandas dataframe.

        Note:
            only one of object_id or view_id can be populated

        Args:
            object_id (Union[int, str]): the object to pull data from
            view_id (Union[int, str]): the view to pull data from
            output (str): "pandas" or "list", decides the output format, "pandas" is default
            resolve (str): for pandas, where fields contain an object (choice, reference, user), resolve to the id or name
            view_filter (list[dict]): column queries to "supply value later" in views,
                see: https://api.docs.dealcloud.com/docs/data/rows/view_details
            fields (list[str]): if not none, return only fields in the list.
            query (str): a DealCloud rows query string to request specific information, see:
                https://api.docs.dealcloud.com/docs/data/rows/query
            include_nulls (bool): if true, null columns will also be returned
            column_headers (str): specifies the value type of the return field keys/column names.
                - api = API Name
                - name = Display name
                - id = field id

        Returns:
            (Union[list, pd.DataFrame]): the DealCloud object data
        """
        # check arguments
        if object_id and view_id:
            raise AttributeError('only one of "object_id" and "view_id" can be entered')
        if not object_id and not view_id:
            raise AttributeError('must pass one of "object_id" and "view_id"')
        if view_id:
            if isinstance(view_id, str):
                views = list(
                    filter(
                        lambda x: x.get("name") == view_id,
                        self.list_configured_views().rows,
                    )
                )
                if len(views) > 1:
                    raise AttributeError(
                        f"too many views with the name: {view_id}, please use a view id"
                    )
                if len(views) == 0:
                    raise AttributeError(f"no views found by the name: {view_id}")
                view_id = views[0].get("id")
                if include_nulls:
                    self._logger.warning(
                        "cannot include all null fields for a view as multiple objects can contribute to the view."
                    )
                include_nulls = False
        parse_output_argument(output)
        if output != "pandas" and resolve:
            self._logger.warning("resolve is only supported for pandas output.")
        if resolve not in ["id", "name", None]:
            raise AttributeError('resolve must be one of "id", "name" or None.')
        if column_headers not in ["id", "api", "name"]:
            raise AttributeError('column_headers must be one of "id", "api" or "name".')
        if view_id and column_headers != "api":
            self._logger.warning(
                "renamed column headers is not supported for reading views"
            )
        if fields:
            if not object_id:
                raise KeyError(
                    'argument: "object_id" must be passed when returning specific fields'
                )

            self._validate_field_mapping(str(object_id), set(fields))

        # first determine the number of rows in the object/view
        if object_id:
            if not query:
                url = f"{self._rows_url}/{object_id}?wrapIntoArrays=true&limit=1000"
                if fields:
                    url_fields = "&fields=".join(fields)
                    url = f"{url}&fields={url_fields}"
                method = "GET"
            else:
                url = f"{self._query_url}/{object_id}"
                method = "POST"
        else:
            url = f"{self._views_url}/{view_id}?wrapIntoArrays=true&limit=1000"
            method = "POST"

        if view_filter:
            request_body: Union[list, dict, None] = view_filter
        elif query:
            request_body = rows_query_payload_builder(query, fields)
        else:
            request_body = None

        response = request_with_retry(
            method, url, self._get_access_token, data=request_body
        )
        if response.status_code != 200:
            raise HTTPError(f"Could not fetch rows, response: {response.text}")
        rows_initial = Rows(**response.json())

        # if the total number of rows is over 1000, pull the data with a multi-threading approach
        if rows_initial.totalRecords > 1000:
            self._logger.debug("total records over 1000, pagination required.")

            # calculate number of pages
            pages = ceil(rows_initial.totalRecords / 1000)

            # refresh auth token
            self._auth()

            if query:
                # get request payloads
                payloads = list(
                    [
                        rows_query_payload_builder(
                            query=query, fields=fields, limit=1000, skip=(skip * 1000)
                        )
                        for skip in range(pages)
                    ]
                )

                result = multi_threaded_request_with_retry(
                    method,
                    url,
                    self._get_access_token,
                    data=payloads,
                    status_force_list=[400, 429],
                    iterate_urls_over_data=False,
                    max_workers=DATA_READ_WORKER_COUNT,
                )
            else:
                # get request urls
                urls = list(
                    [
                        (
                            f"{self._rows_url}/{object_id}?wrapIntoArrays=true&limit=1000&skip={skip * 1000}"
                            if object_id
                            else f"{self._views_url}/{view_id}?wrapIntoArrays=true&limit=1000&skip={skip * 1000}"
                        )
                        for skip in range(pages)
                    ]
                )

                result = multi_threaded_request_with_retry(
                    method,
                    urls,
                    self._get_access_token,
                    data=view_filter,
                    status_force_list=[400, 429],
                    max_workers=(
                        DATA_READ_WORKER_COUNT if object_id else VIEW_READ_WORKER_COUNT
                    ),
                )

            # process rows
            rows_nested = list([Rows(**r).rows for r in result])
            rows = flatten_nested_list(rows_nested)

        # otherwise, return the records from the original request
        else:
            rows = rows_initial.rows

        # if no rows are found return empty
        if len(rows) == 0:
            if object_id:
                self._logger.warning("no rows found", extra={"object_id": object_id})
            if view_id:
                self._logger.warning("no rows found", extra={"view_id": view_id})

            if output == "list":
                return []
            if output == "pandas":
                if fields:
                    df = pd.DataFrame(columns=fields)
                elif object_id and include_nulls and output == "pandas":
                    cols = list([c.apiName for c in self.get_fields(object_id)]) + [
                        "EntryId"
                    ]
                    df = pd.DataFrame(columns=cols)
                else:
                    return pd.DataFrame()
                return df

        # determine columns to return if include_nulls is True
        columns = list(
            [c.apiName for c in self.get_fields(object_id) if c.apiName is not None]
        ) + ["EntryId"]
        if fields and include_nulls:
            columns = fields + ["EntryId"]

        if output == "list":
            if include_nulls:
                for r in rows:
                    for c in columns:
                        if not r.get(c):
                            r[c] = None

            # rename keys if column_headers is not "api"

            return rows
        elif output == "pandas":
            # format the dict into a pandas dataframe
            if include_nulls:
                df = pd.DataFrame.from_records(data=rows, columns=columns).set_index(
                    "EntryId"
                )
            else:
                df = pd.DataFrame.from_records(data=rows).set_index("EntryId")
            if resolve:
                if object_id:
                    df = df.fillna("")
                    # always resolve name field as name
                    df[df.columns[0]] = df[df.columns[0]].apply(
                        lambda x: resolve_object(x, "name")
                    )
                    # identify fields that need to be resolved
                    choice_reference_fields = list(
                        filter(
                            lambda x: x.apiName in df.columns,
                            self._get_choice_reference_fields(object_id),
                        )
                    )

                    # resolve choice/reference fields
                    for choice_ref_field in choice_reference_fields:
                        df[choice_ref_field.apiName] = df[
                            choice_ref_field.apiName
                        ].apply(
                            lambda x: "; ".join(
                                [str(resolve_object(i, str(resolve))) for i in x]
                            )
                        )
                else:
                    self._logger.warning(
                        "resolve is not supported for reading data from views"
                    )
            # rename keys if column_headers is not "api"
            if column_headers != "api" and object_id:
                # generate mapping:
                if column_headers == "name":
                    rename_map = dict(
                        {
                            c.apiName: c.name
                            for c in self.get_fields(object_id)
                            if c.apiName in columns
                        }
                    )
                elif column_headers == "id":
                    rename_map = dict(
                        {
                            c.apiName: str(c.id)
                            for c in self.get_fields(object_id)
                            if c.apiName in columns
                        }
                    )
                else:
                    rename_map = {}

                rename_map["EntryId"] = "EntryId"

                df = df.rename(rename_map, axis=1)

            return df
        else:
            raise AttributeError('output must be one of "list" or "pandas".')

    def _read_data_as_list(
        self,
        object_id: Union[int, str, None] = None,
        view_id: Union[int, str, None] = None,
        resolve: Optional[str] = None,
        view_filter: Optional[list[dict]] = None,
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        include_nulls: bool = True,
        column_headers: str = "api",
    ) -> list[dict]:

        data = self.read_data(
            object_id=object_id,
            view_id=view_id,
            output="list",
            resolve=resolve,
            view_filter=view_filter,
            fields=fields,
            query=query,
            include_nulls=include_nulls,
            column_headers=column_headers,
        )
        if isinstance(data, pd.DataFrame):
            raise TypeError('"list" output incorrectly returned as DataFrame')

        return data

    def _resolve_field_value(
        self, object_name: str, field: Field, value
    ) -> Optional[Union[list[int], int]]:
        """
        Resolves a given field value into an ID that can be sent over the DealCloud API.

        Args:
            object_name (str): the object API name
            field (Field): the field containing the value to be resolved
            value: the field value to be resolved

        Returns:
            the resolved value
        """
        if not value:
            return None

        mapped_values: list[int] = []

        # parse choice field
        if field.fieldType == field_types.CHOICE:
            for v in str(value).split("; "):
                if field.choiceMap is None:
                    raise KeyError(f"choice map not found for field: {field.apiName}")

                mapped = field.choiceMap.get(v)
                if not mapped:
                    self._logger.error(
                        f"Choice mapping error on: {object_name}, {field.name}, could not find value: {v}"
                    )
                else:
                    mapped_values.append(int(mapped))

        # parse reference field
        elif field.fieldType == field_types.REFERENCE:
            id_maps: dict[Any, int] = {}
            if not field.entryLists:
                raise KeyError(f"no entry lists for field: {field.apiName}")
            for ref in field.entryLists:
                if not id_maps:
                    id_maps = self._id_map[ref]
                else:
                    id_maps.update(self._id_map[ref])
            for v in str(value).split("; "):
                mapped = id_maps.get(v)
                if not mapped:
                    self._logger.error(
                        f"Reference mapping error on: {object_name}, {field.name}, could not find value: {v}"
                    )
                else:
                    mapped_values.append(int(mapped))

        # parse user fields
        elif field.fieldType == field_types.USER:
            for v in str(value).split("; "):
                mapped = self._user_map.get(v.lower())
                if not mapped:
                    self._logger.error(
                        f"User mapping error on: {object_name}, {field.name}, could not find value: {v}"
                    )
                else:
                    mapped_values.append(int(mapped))

        elif field.fieldType == field_types.DATE:
            if value == "" or value == pd.NA or value == np.nan:
                return None

        # return resolved values
        if len(mapped_values) > 1:
            return mapped_values
        elif len(mapped_values) == 1:
            return mapped_values[0]
        else:
            return None

    def _validate_field_mapping(self, object_api_name: str, columns: set[str]):
        """
        Validates that the columns provided in a data set to be sent are all valid for the given object
        Args:
            object_api_name(str): the object API name for the columns to be validated against
            columns(set[Field]): a set of the columns being written to

        Returns:
            None: if invalid, a KeyError is raised, no value is returned otherwise.

        """
        fields = self.get_fields(object_api_name)
        column_names = list([i.apiName for i in fields if i.apiName is not None])
        column_names = ["EntryId"] + column_names
        invalid = list(filter(lambda x: x not in column_names, columns))
        if len(invalid) > 0:
            raise KeyError(f"mapping error, could not map: {invalid}")

    def _build_id_map(
        self,
        object_api_name: str,
        columns: set[Field],
        lookup_column: Optional[str],
        include_object: bool = False,
    ) -> list[Field]:
        """
        Builds an internal map of lookup IDs to DealCloud EntryIds

        Args:
            object_api_name(str): the api name of the object being interacted with
            columns(set[Field]): a set of the columns to build the id map for
            lookup_column(Optional[str]): the name of the lookup column
            include_object(bool): if True, include the object being interacted with in the ID map

        Returns:
            list[Field]: a list of the fields that need resolving with the ID map

        """
        self._logger.debug("building id map...")

        if include_object:
            object_data = self._read_data_as_list(object_api_name)
            de_duped = set([val.get(lookup_column) for val in object_data])
            if len(de_duped) != len(object_data):
                self._logger.warning(
                    f"Duplicated primary keys found in object: {object_api_name}, \
                    this will result in unexpected behaviour."
                )
            self._id_map[object_api_name] = dict(
                {
                    i.get(lookup_column): int(i[list(i.keys())[0]])
                    for i in self._read_data_as_list(object_api_name)
                }
            )

            # get fields to resolve
        resolve_fields = list(
            filter(
                lambda x: x.apiName in columns,
                self._get_choice_reference_fields(object_api_name),
            )
        )
        referenced_objects = set(
            flatten_nested_list(
                list(
                    [
                        i.entryLists
                        for i in filter(
                            lambda x: x.fieldType == field_types.REFERENCE,
                            resolve_fields,
                        )
                    ]
                )
            )
        )

        # build id map
        for referenced_object in referenced_objects:
            if lookup_column:
                self._id_map[referenced_object] = dict(
                    {
                        i.get(lookup_column): i[list(i.keys())[0]]
                        for i in self._read_data_as_list(referenced_object)
                    }
                )
            else:
                self._id_map[referenced_object] = dict(
                    {
                        i[list(i.keys())[1]]["name"]: i[list(i.keys())[0]]
                        for i in self._read_data_as_list(referenced_object)
                    }
                )

        return resolve_fields

    def insert_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
    ) -> Union[list[dict], pd.DataFrame]:
        """
        Insert data into a DealCloud site.

        Args:
            object_api_name (str): the object API name to write data to
            data (Union[list[dict], pd.DataFrame]): the data to be sent to DealCloud.
            use_dealcloud_ids (bool): if true, DealCloud EntryIds must be used to reference records and choice values.
                if false, use a column as a lookup, defined by the lookup_column argument.
            lookup_column (str): if use_dealcloud_ids is false, this defines the column to be used as a lookup.
            output (str): "list" or "pandas", defines the output format returned from the function

        Returns:
            (Union[list[dict], pd.DataFrame]): the data returned from the insert function
        """
        parse_output_argument(output)
        data, columns = format_data(data)
        self._validate_field_mapping(object_api_name, columns)
        payloads = calculate_pagination(data, columns)

        # prevent reference before assignment
        resolve_fields = []

        if not use_dealcloud_ids and self._refresh_id_maps:
            resolve_fields = self._build_id_map(object_api_name, columns, lookup_column)

        # add negative entry id for create new
        data_to_send = []
        for payload in payloads:
            payload_rows = []
            for idx, row in enumerate(payload):
                row["EntryId"] = -idx - 1
                if not use_dealcloud_ids:
                    for resolve_field in resolve_fields:
                        row[resolve_field.apiName] = self._resolve_field_value(
                            object_api_name,
                            resolve_field,
                            row.get(resolve_field.apiName),
                        )
                payload_rows.append(row)
            data_to_send.append(payload_rows)

        responses = multi_threaded_request_with_retry(
            "POST",
            f"{self._rows_url}/{object_api_name}",
            self._get_access_token,
            data_to_send,
            status_force_list=[429, 400],
            iterate_urls_over_data=False,
        )

        rows = flatten_nested_list(responses)

        process_errors(rows)

        if output == "list":
            return rows
        elif output == "pandas":
            # format the dict into a pandas dataframe
            df = pd.DataFrame.from_records(data=rows).set_index("EntryId")
            return df

        return rows

    def update_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
    ) -> Union[list[dict], pd.DataFrame]:
        """
        Updates data in a DealCloud site.

        Args:
            object_api_name (str): the object API name to write data to
            data (Union[list[dict], pd.DataFrame]): the data to be sent to DealCloud.
            use_dealcloud_ids (bool): if true, DealCloud EntryIds must be used to reference records and choice values.
                if false, use a column as a lookup, defined by the lookup_column argument.
            lookup_column (Optional[str]): if use_dealcloud_ids is false, this defines the column to be used as a lookup.
            output (str): "list" or "pandas", defines the output format returned from the function

        Returns:
            (Union[list[dict], pd.DataFrame]): the data returned from the insert function

        """
        parse_output_argument(output)
        data, columns = format_data(data)
        self._validate_field_mapping(object_api_name, columns)
        payloads = calculate_pagination(data, columns)

        # prevent reference before assignment
        resolve_fields = []
        id_maps: Optional[dict[Any, int]] = {}

        if not use_dealcloud_ids and self._refresh_id_maps:
            resolve_fields = self._build_id_map(
                object_api_name, columns, lookup_column, True
            )

            id_maps = self._id_map.get(object_api_name)
            if not id_maps:
                raise KeyError(f"Could not find {object_api_name}")

        # add negative entry id for create new
        data_to_send = []
        for payload in payloads:
            payload_rows = []
            for _, row in enumerate(payload):
                if not use_dealcloud_ids:
                    # determine EntryId
                    if not id_maps:
                        raise AttributeError(
                            "id_maps is required for referencing data with mapping"
                        )
                    row["EntryId"] = id_maps.get(row.get(lookup_column))
                    for resolve_field in resolve_fields:
                        row[resolve_field.apiName] = self._resolve_field_value(
                            object_api_name,
                            resolve_field,
                            row.get(resolve_field.apiName),
                        )

                if not row.get("EntryId"):
                    self._logger.error(
                        f"Primary Key error on object: {object_api_name}, record found without 'EntryId' field."
                    )
                    continue
                payload_rows.append(row)
            data_to_send.append(payload_rows)

        responses = multi_threaded_request_with_retry(
            "PUT",
            f"{self._rows_url}/{object_api_name}",
            self._get_access_token,
            data_to_send,
            status_force_list=[429, 400],
            iterate_urls_over_data=False,
        )

        rows = flatten_nested_list(responses)

        process_errors(rows)

        if output == "list":
            return rows
        elif output == "pandas":
            # format the dict into a pandas dataframe
            df = pd.DataFrame.from_records(data=rows).set_index("EntryId")
            return df

        return rows

    def upsert_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
    ) -> Union[list[dict], pd.DataFrame]:
        """
        Upserts data in a DealCloud site. If an id/lookup id exists, it will update the record,
            if not it will create the record.

        Args:
            object_api_name (str): the object API name to write data to
            data (Union[list[dict], pd.DataFrame]): the data to be sent to DealCloud.
            use_dealcloud_ids (bool): if true, DealCloud EntryIds must be used to reference records and choice values.
                if false, use a column as a lookup, defined by the lookup_column argument.
            lookup_column (str): if use_dealcloud_ids is false, this defines the column to be used as a lookup.
            output (str): "list" or "pandas", defines the output format returned from the function

        Returns:
            (Union[list[dict], pd.DataFrame]): the data returned from the insert function

        """
        parse_output_argument(output)
        data, columns = format_data(data)
        self._validate_field_mapping(object_api_name, columns)
        payloads = calculate_pagination(data, columns)

        # prevent reference before assignment
        resolve_fields = []
        id_maps: Optional[dict[Any, int]] = {}

        if not use_dealcloud_ids and self._refresh_id_maps:
            resolve_fields = self._build_id_map(
                object_api_name, columns, lookup_column, True
            )

            id_maps = self._id_map.get(object_api_name)
            if not id_maps:
                raise KeyError(f"Could not find {object_api_name}")

        # add negative entry id for create new
        data_to_post = []
        data_to_put = []
        for payload in payloads:
            post_payload_rows = []
            put_payload_rows = []
            for idx, row in enumerate(payload):
                if not use_dealcloud_ids:
                    # determine EntryId
                    if not id_maps:
                        raise AttributeError(
                            "id_maps is required for referencing data with mapping"
                        )
                    row["EntryId"] = id_maps.get(row.get(lookup_column))
                    for resolve_field in resolve_fields:
                        row[resolve_field.apiName] = self._resolve_field_value(
                            object_api_name,
                            resolve_field,
                            row.get(resolve_field.apiName),
                        )

                if not row.get("EntryId"):
                    row["EntryId"] = -idx - 1
                    post_payload_rows.append(row)
                else:
                    put_payload_rows.append(row)
            data_to_post.append(post_payload_rows)
            data_to_put.append(put_payload_rows)

        put_responses = multi_threaded_request_with_retry(
            "PUT",
            f"{self._rows_url}/{object_api_name}",
            self._get_access_token,
            data_to_put,
            status_force_list=[429],
            iterate_urls_over_data=False,
        )
        post_responses = multi_threaded_request_with_retry(
            "POST",
            f"{self._rows_url}/{object_api_name}",
            self._get_access_token,
            data_to_post,
            status_force_list=[429, 400],
            iterate_urls_over_data=False,
        )

        put_rows = flatten_nested_list(put_responses)
        post_rows = flatten_nested_list(post_responses)

        rows = put_rows + post_rows
        process_errors(rows)

        if output == "list":
            return rows
        elif output == "pandas":
            # format the dict into a pandas dataframe
            df = pd.DataFrame.from_records(data=rows).set_index("EntryId")
            return df

        return rows

    def delete_data(
        self,
        object_api_name: str,
        records: list[int],
        page_size: int = DELETION_PAGINATION_LIMIT,
    ) -> list[dict]:
        """
        Delete data from a DealCloud site

        Args:
            object_api_name (str): the object api name to delete data from
            records (list[int]): a list of entry ids to delete
            page_size (int): the number of records to be deleted in a single page, defaults to 10000

        Returns:
            (list[dict]): the response from the delete function

        """
        delete_records = list(divide_pages(records, page_size))
        delete_response = multi_threaded_request_with_retry(
            "DELETE",
            f"{self._entrydata_url}/{object_api_name}",
            self._get_access_token,
            delete_records,
            status_force_list=[429, 400, 500],
            iterate_urls_over_data=False,
            max_workers=8,
        )
        return delete_response

    def get_object_history(self): ...

    def download_files(self): ...

    def merge_entries(self): ...
