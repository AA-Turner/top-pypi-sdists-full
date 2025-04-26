
import json 

from unittest import TestCase

from . import mock_spring, reset_mock, format_url, _MockResponse

class TestServices(TestCase):
    """
    Test's that we call the different requests with the right information
    to the underlying http request library.  
    
    Each should also wrap any response in the proper Response Object, in this
    case it's _MockResponse
    """

    def setUp(self):

        reset_mock()
        self.param = "test"
        self.end_point = "/" + mock_spring.mock_service.__API__ 
    
    def test_services_exist(self):
        assert hasattr(mock_spring, 'supply_tags')
        assert hasattr(mock_spring, 'supply_partners')
        assert hasattr(mock_spring, 'domain_lists')
        assert hasattr(mock_spring, 'demand_tags')
        assert hasattr(mock_spring, 'demand_partners')
        assert hasattr(mock_spring, 'accounts')
        assert hasattr(mock_spring, 'users')

    def assert_response_type(self, resp):
        """
        Check that it is using the correct type of response wrapper
        """
        assert isinstance(resp, _MockResponse)

    def build_path(path=None, query=None):
        if path:
            return  "/" + mock_spring.mock_service.__API__ + "/" + path

    def test_get_no_query(self):
        api = mock_spring.API()

        resp = mock_spring.mock_service.get(self.param)        
        api.get.assert_called_with(format_url(self.end_point, self.param),
                                   params={})
        self.assert_response_type(resp)

    def test_get_query(self):
        api = mock_spring.API()
        resp = mock_spring.mock_service.get(self.param, that="this")        
        api.get.assert_called_with(format_url(self.end_point, self.param),
                                              params = {'that': 'this'})
        self.assert_response_type(resp)

    def test_post_no_query(self):
        payload = {"name":"blah"}
        resp = mock_spring.mock_service.post(payload)        

        api = mock_spring.API()
        api.post.assert_called_with(format_url(self.end_point),
                                    params={},
                                   data = json.dumps(payload))
        self.assert_response_type(resp)

    def test_post_query(self):
        payload = {"name":"blah"}
        resp = mock_spring.mock_service.post(payload, self.param, this="that")        

        api = mock_spring.API()
        api.post.assert_called_with(format_url(self.end_point, self.param),
                                    params = {"this": "that"},
                                   data = json.dumps(payload))
        self.assert_response_type(resp)

    def test_put_no_query(self):
        payload = {"name":"blah"}
        resp = mock_spring.mock_service.put(self.param, payload)        

        api = mock_spring.API()
        api.put.assert_called_with(format_url(self.end_point, self.param),
                                    params={},
                                   data = json.dumps(payload))
        self.assert_response_type(resp)

    def test_put_query(self):
        payload = {"name":"blah"}
        resp =  mock_spring.mock_service.put(self.param, payload, this="that")        

        api = mock_spring.API()
        api.put.assert_called_with(format_url(self.end_point, self.param),
                                   params = {"this": "that"},
                                   data = json.dumps(payload))
    
        self.assert_response_type(resp)

    def test_new(self):
        payload = {"name":"blah"}
        resp = mock_spring.mock_service.new(payload)        

        api = mock_spring.API()
        api.post.assert_called_with(format_url(self.end_point, None, {}),
                                    params={},
                                   data = json.dumps(payload))

        self.assert_response_type(resp)
