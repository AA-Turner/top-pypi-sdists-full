import asyncio
import pytest
from navconfig import BASE_DIR
from pandas import DataFrame
from flowtask.tests import BaseTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'QueryToPandas'
    yield cp

pytestmark = pytest.mark.asyncio

class TestQuerySimple(BaseTestCase):
    """Query SQL from string
    """
    arguments: dict = {
        "query": "SELECT store_id, store_name, street_address, launch_date FROM walmart.stores"
    }
    expected_result_type = DataFrame

class TestQueryFile(BaseTestCase):
    """Query SQL from File
    """
    arguments: dict = {
        "file_sql": BASE_DIR.joinpath('tests', 'sql', 'get_stores.sql')
    }
    expected_result_type = DataFrame


class TestQuerySlug(BaseTestCase):
    """Query SQL from Slug
    """
    arguments: dict = {
        "query_slug": "walmart_stores",
        "conditions": {
          "fields": [
            "territory_name", "region_name", "market_name", "store_id", "store_name"
          ],
          "firstdate": "2022-01-31",
          "where_cond": {"region_name": "Jose Arcay"},
          "querylimit": 1,
          "refresh": "True"
        }
    }
    expected_result_type = DataFrame

# class TestQueryRaw(BaseTestCase):
#     """Query Dictionary format RAW
#     """
#     arguments: dict = {
#         "raw_result": True,
#         "masks": {
#             "{today}": ["current_date", {"mask": "%Y-%m-%d"}],
#             "firstdate": ["date_diff", { "value": "current_date", "diff": 8, "mode": "days", "mask": "%Y-%m-%d" }],
#             "lastdate": ["yesterday", { "mask": "%Y-%m-%d" }]
#         },
#         "query_slug": {
#             "microsite": {
#             "slug":"echelon_customer_overview_cdr_fixed",
#             "conditions": {
#                 "fields":[
#                     "count(session_id) as total_clicks",
#                     "sum(engagement) as engagements",
#                     "to_char((ceil(troc_percent(sum(duration), count(session_id))) || ' second')::interval, 'MI:SS') as avg_session_duration"
#                     ],
#                 "lastdate": "",
#                 "firstdate": "",
#                 "where_cond": {}
#             }
#             }
#         }
#     }
#     expected_result_type = dict

class TestQueryFile2(BaseTestCase):
    """Query SQL from File
    """
    arguments: dict = {
        "raw_result": True,
        "file_sql": BASE_DIR.joinpath('tests', 'sql', 'get_stores.sql')
    }
    expected_result_type = list

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
