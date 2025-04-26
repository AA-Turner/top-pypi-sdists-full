import json

import pytest

# from requests import delete, get, post, put

"""
This is a WIP

Using this module for internal testing example:

def internal_sdk_function():
    response = get('https://api.example.com/resource')
    # Process the response

Example 1:
@pytest.fixture(autouse=True)
def mock_api_calls(mocker):
    mocker.patch('requests.get', side_effect=mock_requests_get)
    mocker.patch('requests.post', side_effect=mock_requests_post)

def test_internal_function_with_mocked_api_call(mock_api_calls):
    internal_function()

    # Assertions or additional checks
    # ...

def test_another_function_with_mocked_api_call(mock_api_calls):
    response = post('https://api.example.com/resource', data={'key': 'value'})
    # Assertions or additional checks
    # ...

Example 2:
def test_yet_another_function_with_mocked_api_call(mocker):
    # Mock the API call
    mocker.patch('requests.get', return_value=MockResponse({'message': 'Mocked Response'}, 200))

    # Call the function under test
    my_function()

    # Assertions or additional checks
    # ...

"""


class MockResponse:
    """Mocked response for API calls during testing.

    This class provides a mock response object that can be used to simulate API responses
    during testing. It allows developers to define the JSON data and status code for the response.

    Args:
        json_data (dict): The JSON data to be returned by the `json` method of the mock response.
        status_code (int): The status code to be returned by the `status_code` attribute of the mock response.

    Attributes:
        json_data (dict): The JSON data to be returned by the `json` method of the mock response.
        status_code (int): The status code to be returned by the `status_code` attribute of the mock response.

    Examples:
        Creating a mock response with JSON data and status code:

        ```python
        response_data = {'message': 'Success'}
        status_code = 200
        response = MockResponse(response_data, status_code)
        ```

        Retrieving the JSON data and status code from a mock response:

        ```python
        json_data = response.json()
        status_code = response.status_code
        ```

    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Return the JSON data of the mock response.

        Returns:
            dict: The JSON data of the mock response.

        """
        return self.json_data

    @property
    def text(self):
        return json.dumps(self.json_data)

    def __repr__(self):
        """Return the string representation of the mock response.

        Returns:
            str: The string representation of the mock response.

        """
        return f"MockResponse(json_data={self.json_data}, status_code={self.status_code})"


@pytest.fixture(autouse=True)
def mock_requests(mocker):
    mocker.patch('requests.get', side_effect=mock_requests_get)
    mocker.patch('requests.post', side_effect=mock_requests_post)
    mocker.patch('requests.put', side_effect=mock_requests_put)
    mocker.patch('requests.delete', side_effect=mock_requests_delete)


def mock_requests_get(*args, **kwargs):
    # Provide a sample response here
    response_data = {'message': 'Success'}
    status_code = 200

    # Create a mock response object
    response = MockResponse(response_data, status_code)

    return response


def mock_requests_post(*args, **kwargs):
    # Provide a sample response here
    response_data = {'message': 'Created'}
    status_code = 201

    # Create a mock response object
    response = MockResponse(response_data, status_code)

    return response


def mock_requests_put(*args, **kwargs):
    # Provide a sample response here
    response_data = {'message': 'Updated'}
    status_code = 200

    # Create a mock response object
    response = MockResponse(response_data, status_code)

    return response


def mock_requests_delete(*args, **kwargs):
    # Provide a sample response here
    response_data = {'message': 'Deleted'}
    status_code = 204

    # Create a mock response object
    response = MockResponse(response_data, status_code)

    return response
