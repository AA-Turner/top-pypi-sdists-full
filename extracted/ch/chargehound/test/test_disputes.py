import chargehound
import requests_mock
import unittest2
import json

from chargehound.version import VERSION
from chargehound.models import List, Dispute, Response


get_headers = {
    'accept': 'application/json',
    'authorization': 'Basic QVBJX0tFWTo=',
    'user-agent': 'Chargehound/v1 PythonBindings/' + VERSION
}

post_headers = {
    'accept': 'application/json',
    'authorization': 'Basic QVBJX0tFWTo=',
    'content-type': 'application/json',
    'user-agent': 'Chargehound/v1 PythonBindings/' + VERSION
}

product_info = [{'name': 'Saxophone',
                 'description': 'Alto saxophone, with carrying case',
                 'image': 'http://s3.amazonaws.com/chargehound/saxophone.png',
                 'sku': '17283001272',
                 'quantity': 1,
                 'amount': 20000,
                 'url': 'http://www.example.com', },
                {'name': 'Milk',
                 'description': 'Semi-skimmed Organic',
                 'image': 'http://s3.amazonaws.com/chargehound/milk.png',
                 'sku': '26377382910',
                 'quantity': '64oz',
                 'amount': 400,
                 'url': 'http://www.example.com'}]

correspondence_info = [{'to': 'customer@example.com',
                        'from': 'noreply@example.com',
                        'subject': 'Your Order',
                        'body': 'Your order was received.',
                        'caption': 'Order confirmation email.'},
                       {'to': 'customer@example.com',
                        'from': 'noreply@example.com',
                        'subject': 'Your Order',
                        'body': 'Your order was delivered.',
                        'caption': 'Delivery confirmation email.'}]

past_payments_info = [{'id': 'ch_1',
                       'amount': 20000,
                       'currency': 'usd',
                       'charged_at': '2019-09-10 11:09:41PM UTC'},
                      {'id': 'ch_2',
                       'amount': 50000,
                       'currency': 'usd',
                       'charged_at': '2019-09-03 11:09:41PM UTC'}]

dispute_response = {
  'id': 'dp_123',
  'fields': {'customer_name': 'Susie'},
  'products': [],
  'correspondence': [],
  'past_payments': [],
  'object': 'dispute'
}

dispute_products_response = {
  'id': 'dp_123',
  'object': 'dispute',
  'fields': {'customer_name': 'Susie'},
  'products': product_info,
  'correspondence': [],
  'past_payments': [],
}

dispute_correspondence_response = {
  'id': 'dp_123',
  'object': 'dispute',
  'fields': {'customer_name': 'Susie'},
  'correspondence': correspondence_info,
  'products': [],
  'past_payments': [],
}

dispute_past_payments_response = {
  'id': 'dp_123',
  'object': 'dispute',
  'fields': {'customer_name': 'Susie'},
  'past_payments': past_payments_info,
  'correspondence': [],
  'products': [],
}

dispute_list_response = {
  'object': 'list',
  'data': [{
    'id': 'dp_123',
    'fields': {'customer_name': 'Susie'},
    'products': [],
    'correspondence': [],
    'past_payments': [],
    'object': 'dispute'
  }]
}

response_response = {
  'dispute_id': 'dp_123',
  'object': 'response'
}


def is_json(response_body):
    """Can this HTTP response be parsed as JSON?"""
    try:
        json.loads(response_body)
        return True
    except:
        return False


def json_has_structure(response_body, expected_json):
    """Does the JSON this HTTP response match the expected structure?"""
    actual_json = json.loads(response_body)

    return actual_json == expected_json


class DisputeTest(unittest2.TestCase):

    def setUp(self):
        super(DisputeTest, self).setUp()
        chargehound.api_key = 'API_KEY'

    @requests_mock.mock()
    def test_create_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes',
                  status_code=200,
                  request_headers=post_headers,
                  json=dispute_response)
        chargehound.Disputes.create({'id': 'dp_123'})
        assert mock.called

    @requests_mock.mock()
    def test_retrieve_dispute(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes/dp_123',
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_response)
        chargehound.Disputes.retrieve('dp_123')
        assert mock.called

    @requests_mock.mock()
    def test_retrieve_dispute_response(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes/dp_123/response',
                 status_code=200,
                 request_headers=get_headers,
                 json=response_response)
        res = chargehound.Disputes.response('dp_123')

        assert mock.called
        assert isinstance(res, Response)
        assert res.dispute_id == 'dp_123'

    @requests_mock.mock()
    def test_list_all_disputes(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes',
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_list_response)
        chargehound.Disputes.list()
        assert mock.called

    @requests_mock.mock()
    def test_list_disputes_filter_state(self, mock):
        url = 'https://api.chargehound.com/v1/disputes?state=needs_response'
        mock.get(url,
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_list_response)
        chargehound.Disputes.list(state='needs_response')
        assert mock.called

    @requests_mock.mock()
    def test_list_disputes_filter_multiple_states(self, mock):
        url = 'https://api.chargehound.com/v1/disputes' +\
            '?state=needs_response&state=warning_needs_response'
        mock.get(url,
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_list_response)
        chargehound.Disputes.list(
          state=['needs_response', 'warning_needs_response']
        )
        assert mock.called

    @requests_mock.mock()
    def test_submit_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json=dispute_response)
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'})

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'}})

    @requests_mock.mock()
    def test_submit_dispute_with_product_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json=dispute_products_response)
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    products=product_info)

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'products': product_info})

    @requests_mock.mock()
    def test_submit_dispute_with_correspondence_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json=dispute_correspondence_response)
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    correspondence=correspondence_info)

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'correspondence': correspondence_info})

    @requests_mock.mock()
    def test_submit_dispute_with_past_payments_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/submit',
                  status_code=201,
                  json=dispute_past_payments_response)
        chargehound.Disputes.submit('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    past_payments=past_payments_info)

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'past_payments': past_payments_info})

    @requests_mock.mock()
    def test_update_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123',
                  status_code=200,
                  json=dispute_response)
        chargehound.Disputes.update('dp_123',
                                    fields={'customer_name': 'Susie'})

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'}})

    @requests_mock.mock()
    def test_update_dispute_with_product_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123',
                  status_code=200,
                  json=dispute_products_response)
        chargehound.Disputes.update('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    products=product_info)

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'products': product_info})

    @requests_mock.mock()
    def test_update_dispute_with_correspondence_info(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123',
                  status_code=200,
                  json=dispute_correspondence_response)
        chargehound.Disputes.update('dp_123',
                                    fields={'customer_name': 'Susie'},
                                    correspondence=correspondence_info)

        assert mock.called

        response = mock.request_history[0].body
        try:
            response = response.decode()
        except AttributeError:
            pass

        assert response
        assert is_json(response)
        assert json_has_structure(response,
                                  {'fields': {'customer_name': 'Susie'},
                                   'correspondence': correspondence_info})

    @requests_mock.mock()
    def test_typed_responses(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes',
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_list_response)
        li = chargehound.Disputes.list()
        assert mock.called
        assert isinstance(li, List)
        assert isinstance(li.data[0], Dispute)

    @requests_mock.mock()
    def test_typed_responses_can_be_jsonified(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes',
                 status_code=200,
                 request_headers=get_headers,
                 json=dispute_list_response)
        li = chargehound.Disputes.list()

        response = {
          'object': 'list',
          'data': [{
            'id': 'dp_123',
            'fields': {'customer_name': 'Susie'},
            'object': 'dispute',
            'products': [],
            'past_payments': [],
            'correspondence': []
          }],
          'response': [200]
        }

        assert mock.called
        assert json.dumps(response, sort_keys=True) \
            == json.dumps(li, sort_keys=True)

    @requests_mock.mock()
    def test_accept_dispute(self, mock):
        mock.post('https://api.chargehound.com/v1/disputes/dp_123/accept',
                  status_code=200,
                  json=dispute_response)
        chargehound.Disputes.accept('dp_123')

        assert mock.called
