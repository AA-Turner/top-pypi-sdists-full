import asyncio
import pytest
import pandas as pd
from flowtask.tests import PandasTestCase


@pytest.fixture(autouse=True, scope='session')
def component():
    cp = 'TransformRows'
    yield cp

pytestmark = pytest.mark.asyncio

# class TestTransForm(PandasTestCase):
#     file_test = 'HR Employees.csv'
#     arguments: dict = {
#         "replace_columns": True,
#         "fields": {
#            "associate_id": "Associate ID",
#            "display_name": "Payroll Name",
#            "file_number": "File Number",
#            "Hire Date": {"value": ["convert_to_date"]},
#            "Position Start Date": {"value": ["convert_to_datetime"]},
#            "Termination Date": {"value": ["convert_to_string"]},
#            "File Number": {"value": ["to_integer"]},
#            "First Name": {"value": ["trim"]},
#            "Last Name": {"value": ["capitalize"]},
#            "department": {"value": ["regex_match", {"column": "Location Description", "regex": "\\.([0-9]*)\\?"}]},
#            "name": {"value": [ "concat", { "columns": ["First Name", "Last Name"]}]},
#            "Position Status": {"value": ["convert_to_boolean", {"boolDict": {"Active": True, "Terminated": False, "": False}}]},
#            "weekday": {"value": ["datetime_format", {"column":"Position Start Date", "format":"%w"}]},
#            "Location Description": {"value": ["replace_regex", { "to_replace": "#", "value": ""}]},
#         }
#     }
#     renamed_cols: list = ['associate_id', 'display_name', 'file_number']

class TestTransform(PandasTestCase):
    file_test = 'employees.csv'
    arguments: dict = {
        "replace_columns": True,
        "fields": {
            "company_code": "Company Code",
            "employee_id": "Employee ID",
            "employee_name": "Name"
        }
    }
    renamed_cols: list = ["company_code", "employee_id", "employee_name"]

class TestTransformRowsSuffix(PandasTestCase):
    file_test = "employees.csv"
    renamed_cols: None
    arguments: dict = {
        "fields": {
            "Employee ID": {"value": ["suffix", {"suffix": "_employee"}]},
        },
    }

    expected_result_type = pd.DataFrame


class TestTransformRowsPreffix(PandasTestCase):
    file_test = "employees.csv"
    renamed_cols: None
    arguments: dict = {
        "fields": {
            "Employee ID": {"value": ["prefix", {"prefix": "employee_"}]},
        },
    }

    expected_result_type = pd.DataFrame

class TestTransformRowsConcat(PandasTestCase):
    file_test = "warehouses.csv"  # Input test file with a column 'name'
    renamed_cols = None  # No column renaming in this test case
    
    # Arguments for the transformation method
    arguments: dict = {
        "fields": {
            "concatenated_names": {
                "value": [
                    "concat_column_values", {"column": "name", "separator": ","}
                    ]
                },
        },
    }
    
    expected_result_type = pd.DataFrame


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
