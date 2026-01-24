# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import json
from typing import List, Iterator
from .quad_store import QuadStore, semantic_type_to_python_object


class TableResult:
    """Wraps the results from certain SPARQL queries and provides useful
    access methods.

    Attributes:
        dict_results: The exact results of the query parsed into a dictionary
            from the response json
        result_vars: The names of all variables returned from the query
        result_dicts: The variable bindings returned from the query

    Usage:
        # TableResults are created from QueryResults
        table_results = query_result.as_table_results()

        # There are multiple different ways to access the results of the table
        table_results.as_list()
        table_results.as_list_iter()
        table_results.as_as_record_dictionaries()
    """

    def __init__(self, json_string: str) -> None:
        self.dict_results = json.loads(json_string)
        self.result_vars = self.dict_results['head']['vars']
        self.result_dicts = self.dict_results['results']['bindings']

    def as_list(self) -> List[List[str]]:
        """
        Returns the query result as a list of lists.

        Convert a query result to a list of lists where each sublist
        represents a single solution to the query. If any variables are unbound
        (e.g. due to the use of OPTIONAL {...}), the corresponding value in the
        list will be an empty string. This means that all sublists will be of
        the same length.

        Returns:
            A list of lists of string values.
        """
        return list(self.as_list_iter())

    def as_list_iter(self) -> Iterator[List[str]]:
        """
        Returns the query result as an iterator containing lists.

        Converts a query result to an iterator containing lists where each
        sublist represents a single solution to the query. If any variables are
        unbound (e.g. due to the use of OPTIONAL {...}), the corresponding
        value in the list will be an empty string. This means that all sublists
        will be of the same length.

        Yields:
            A list string values representing one solution to the query

        """
        for result_dict in self.result_dicts:
            yield [
                result_dict.get(var, {'value': ''})['value']
                for var in self.result_vars
            ]

    def as_record_dictionaries(self) -> List[dict]:
        """
        Returns the query result as list of dictionaries.

        Convert a query result to a list of dictionaries where each dictionary
        represents a single solution to the query and maps each variable to its
        corresponding value within the solution. Any variables that are unbound
        (e.g. due to the use of OPTIONAL {...}) will still appear as keys in
        the dictionary but will map to the empty string. This means that all
        dictionaries will have the same number of keys.

        Returns:
            A list of dictionaries, each representing one solution to the
            query. The return format is perfectly suited to interface with
            pandas through the DataFrame, from_dict or from_records methods.
        """

        record_dicts = []
        for result_dict in self.result_dicts:
            record_dict = {}

            for var_name in self.result_vars:

                # Parse the information in the result dict, if this variable
                # exists. If it doesn't, then use these defaults
                val = ""
                val_datatype = ""

                if var_name in result_dict:
                    # result_dict[var_name] might look something like this:
                    # {'datatype': 'http://www.w3.org/2001/XMLSchema#int',
                    # 'type': 'literal', 'value': '30'}}

                    val = result_dict[var_name]['value']

                    # A datatype is not always provided, so default to
                    # the empty string
                    val_datatype = result_dict[var_name].get("datatype", "")

                # Convert the value to the python type. For example,
                # val might be "3" and the val_datatype might be xsd:int.
                # Then semantic_type_to_python_object(val, val_datatype)
                # would return the int 3.

                val_typed = semantic_type_to_python_object(val, val_datatype)
                record_dict[var_name] = val_typed

            record_dicts.append(record_dict)
        return record_dicts

    def __iter__(self):
        return self.as_list_iter()

    def __eq__(self, other) -> bool:
        return self.dict_results == other.dict_results

    def __str__(self) -> str:
        return f"<TableResult '{self.dict_results}'>"

    def __repr__(self) -> str:
        return str(self)


class QueryResult:
    """Dispatches a query result to a TableResult or QuadStore.

    This class handles the results of queries. And dispatches them
    to either a TableResult class or a QuadStore class. The former
    is for select and ask queries. The latter is for construct queries.

    Attributes:
        json_string: A json string that represents the results
            of a query.
    """

    def __init__(self, json_string: str) -> None:
        """Stores json_string from a query result.

        This method just stashes the json_string it is
        passed as an attibute.

        Args:
            json_string: A json_string representing the reuslts
                of a query
        """
        self.json_string = json_string

    def as_table_results(self) -> TableResult:
        """Returns the query result as a TableResult.

        """

        return TableResult(self.json_string)

    def as_quad_store(self) -> QuadStore:
        """Returns the query result as a QuadStore.

        """

        # Cover for an Anzo issue where an empty string,
        # not an empty JSON, is returned.
        if not self.json_string:
            return QuadStore()

        result_json = json.loads(self.json_string)
        return QuadStore.from_anzo_json_list(result_json)
