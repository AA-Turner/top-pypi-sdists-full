# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import parameterized
import unittest

from pyanzo import (
    AnzoClient,
    QueryResult,
    TableResult,
)

from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD
)


class TestIntegratedQueryFuzz(unittest.TestCase):
    graphmart = GRAPHMART

    # Templated verions of the queries to allow for different SELECT vars and LIMITs  # noqa
    simple_select_query_template = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT {} WHERE {{
            ?s a data:Person ;
                data:Person_City ?city .
        }} ORDER BY ?city LIMIT {}
    """  # noqa

    query_with_optional_template = """
        PREFIX data: <http://cambridgesemantics.com/ont/autogen/a69a/PyAnzo_Dictionary/PyAnzo_Datasource#>

        SELECT {} WHERE {{
          ?s a data:Person ;
             data:Person_Name ?name ;
             data:Person_City ?city ;
             data:Person_Age ?age .

          # person height is not a property and
          # will be unbound by design (for testing)
          OPTIONAL {{ ?s  data:Person_Height  ?height }}

            }} ORDER BY ?city LIMIT {}
    """  # noqa

    QueryResult_select_star = QueryResult("""{
        "head": {"vars": ["s", "name", "city", "age", "height"]},
        "results":
            {"bindings": [
                {"age": {"datatype": "http://www.w3.org/2001/XMLSchema#long",
                         "type": "literal",
                         "value": "60"},
                 "city": {"type": "literal", "value": "Boston"},
                 "name": {"type": "literal", "value": "Diego"},
                 "s": {"type": "uri",
                       "value": "http://csi.com/Person/879d629b-1015-45b9-8457-7271c0f2a9f0"}
                },
                {"age": {"datatype": "http://www.w3.org/2001/XMLSchema#long",
                         "type": "literal",
                         "value": "33"},
                 "city": {"type": "literal", "value": "Cambridge"},
                 "name": {"type": "literal", "value": "Bob"},
                 "s": {"type": "uri",
                       "value": "http://csi.com/Person/c2ee95a3-d5b1-40d8-8243-9c7d541853f7"}
                },
                {"age": {"datatype": "http://www.w3.org/2001/XMLSchema#long",
                         "type": "literal",
                         "value": "70"},
                 "city": {"type": "literal", "value": "Medford"},
                 "name": {"type": "literal", "value": "Eve"},
                 "s": {"type": "uri",
                       "value": "http://csi.com/Person/ffbe9982-7491-42da-9398-e4c22fab5711"}
                },
                {"age": {"datatype": "http://www.w3.org/2001/XMLSchema#int",
                         "type": "literal",
                         "value": "30"},
                 "city": {"type": "literal", "value": "Somerville"},
                 "name": {"type": "literal", "value": "Alice"},
                 "s": {"type": "uri",
                       "value": "http://csi.com/Person/a153b0aa-5583-40ff-8710-f94c8a25df3d"}
                },
                {"age": {"datatype": "http://www.w3.org/2001/XMLSchema#long",
                         "type": "literal",
                         "value": "50"},
                 "city": {"type": "literal", "value": "Watertown"},
                 "name": {"type": "literal", "value": "Carlos"},
                 "s": {"type": "uri",
                       "value": "http://csi.com/Person/0c391c0f-340d-4f08-9fa6-13a1793c35cb"}
                }
            ]
           }
        }""") # noqa

    # The test docstrings are convenient when looking at the code, but
    # they make the verbose testing view look cluttered. This function
    # removes comments/descriptions from the verbose test view.
    def shortDescription(self):
        return None

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME,
            password=PASSWORD, port=PORT
        )

    @parameterized.parameterized.expand([
        ("SELECT_CITY_HEIGHT", "?city ?height", ["city", "height"]),
        ("SELECT_*", "*", ["*"]),
        ("SELECT_CITY", "?city", ["city"]),
        ("SELECT_CITY_AGE_NAME", "?city ?age ?name", ["city", "name", "age"])
    ])
    def test_graphmart_query_various_selects(self,
                                             test_name,
                                             select_vars,
                                             select_vars_list):
        """Test querying a graphmart with different combinations of
           select variables"""

        # attempts a query based on the specified select vars
        query_string = self.query_with_optional_template.format(select_vars, 5)

        result = self.anzo_client.query_graphmart(
            self.graphmart, query_string=query_string
        ).as_table_results()

        self.assertEqual(
            result.as_record_dictionaries(),

            # QueryResult_select_star is the result of selecting all variables
            # Here we are filtering out the vars not in our select in order to
            #   check for equality
            [
                {key: val for key, val in solution_dict.items()
                    if key in select_vars_list or select_vars == "*"}
                for solution_dict in self.QueryResult_select_star.as_table_results().as_record_dictionaries()
            ]
        )

    @parameterized.parameterized.expand([
        ("LIST", TableResult.as_list),
        ("DICT", TableResult.as_record_dictionaries),
        # Need to convert iter to list in order to compare results
        ("LIST_ITER", lambda x: list(TableResult.as_list_iter(x)))
    ])
    def test_graphmart_query_result_length(self,
                                           test_name,
                                           query_result_method) -> None:
        """Test that the length of the query result is current (<= LIMIT)"""

        for limit in range(5):
            query_string = self.simple_select_query_template.format("*", limit)
            result = self.anzo_client.query_graphmart(
                self.graphmart, query_string=query_string
            ).as_table_results()

            self.assertLessEqual(len(query_result_method(result)), limit)
