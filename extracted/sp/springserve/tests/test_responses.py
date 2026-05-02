
from . import mock_spring, _MockResponse, format_url, reset_mock

import json
from mock import MagicMock
from unittest import TestCase

class TestSingleResponse(TestCase):
    """
    Tests that given a proper response from the API it appropriately handles:

        1. set attribute
        2. Tab Completion
        3. save
    """

    def setUp(self):
        reset_mock()
        self.path_params = "path"
        self.query_params = {"query":"something"}
        self.response_data = {"this": "that", "foo": "bar", "id": 1,
                              "account_id": 1}
        self.response = mock_spring._VDAPISingleResponse(
                                    mock_spring.mock_service, 
                                    self.response_data, 
                                    self.path_params,
                                    self.query_params,
                                    True)
        self.bad_response = mock_spring._VDAPISingleResponse(
                                    mock_spring.mock_service, 
                                    self.response_data, 
                                    self.path_params,
                                    self.query_params,
                                    False)

                                    
    
    def test_tab_completion(self):
        
        self.assertTrue(isinstance(self.response, mock_spring._TabComplete))
        self.assertEquals(self.response._tab_completions(),
                          list(self.response_data.keys()))

    def test_save(self):
        self.response.this = "not_that"
        self.response.save()

        api = mock_spring.API()
        api.put.assert_called_with(format_url("/" +
                                              mock_spring.mock_service.__API__
                                              ,self.response_data['id']),
                                   params={"account_id": 1},
                                   data = json.dumps(self.response.raw))
    
    def test_get_attribute(self):
        self.assertEquals(self.response.this, "that")
        self.assertEquals(self.response.foo, "bar")

    def test_set_attribute(self):
        self.assertEquals(self.response.this, "that")
        self.response.this = "not_that"
        self.assertEquals(self.response.this, "not_that")
        self.assertEquals(self.response._raw_response['this'], "not_that")

    def test_ok(self):
        self.assertTrue(self.response.ok)
        self.assertFalse(self.bad_response.ok)

    
class TestMultiResponse(TestCase):
    """
    Tests that given a proper response from the API it appropriately handles:

        1. Pagenation/Iteration
        2. Caching
        3. selection 
    """

    def setUp(self):
        reset_mock()
        self.path_params = "path"
        self.query_params = {"query":"something"}
        self.response_data = [{"this1": "that1", "foo": "bar"}, 
                              {"this1": "that1", "foo": "bar"}] 
        self.response = mock_spring._VDAPIMultiResponse(
                                    mock_spring.mock_service, 
                                    self.response_data, 
                                    self.path_params,
                                    self.query_params,
                                    _MockResponse,
                                    True)
        self.bad_response = mock_spring._VDAPIMultiResponse(
                                    mock_spring.mock_service, 
                                    self.response_data, 
                                    self.path_params,
                                    self.query_params,
                                    _MockResponse,
                                    False)
    
    def test_iteration(self):
        #make it so it doesn't get the next page
        self.response._all_pages_gotten=True

        data = [x for x in self.response]
        self.assertTrue(all([isinstance(x, _MockResponse) for x in data]))
        self.assertTrue(all([x.this1 == 'that1' for x in data]))

    def test_pagenation(self):
        
        mock_spring.mock_service.get_raw = MagicMock()
        mock_response = MagicMock()
        mock_response.json = [{"this3": "that3", "foo": "bar"}, 
                                           {"this3": "that3", "foo": "bar"}]
        mock_spring.mock_service.get_raw.side_effect = [mock_response, None]
        data = [x for x in self.response]
        
        mock_spring.mock_service.get_raw.call_count=2
        self.assertEquals(len(data), 4)

    def test_selection(self):
        self.assertEquals(self.response[0].raw, self.response_data[0])
        self.assertEquals(self.response[1].raw, self.response_data[1])

    def test_ok(self):
        assert self.response.ok
        assert not self.bad_response.ok


