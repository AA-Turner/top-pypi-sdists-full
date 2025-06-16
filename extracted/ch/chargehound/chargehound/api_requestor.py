from __future__ import unicode_literals

import chargehound
import requests
from chargehound.error import create_chargehound_error
from chargehound.version import VERSION
from chargehound.models import (
    ChargehoundObject, List, Dispute, Product,
    PastPayment, CorrespondenceItem, Response, HTTPResponse
)


class APIRequestor(object):
    @classmethod
    def _convert_list(cls, obj, key_name, model_class):
        return [model_class(item) for item in obj.get(key_name, [])]

    def convert(self, obj):
        if obj.get('object') == 'dispute':
            obj['products'] = \
                self._convert_list(obj, 'products', Product)
            obj['past_payments'] = \
                self._convert_list(obj, 'past_payments', PastPayment)
            obj['correspondence'] = \
                self._convert_list(obj, 'correspondence', CorrespondenceItem)
            return Dispute(obj)
        elif obj.get('object') == 'list':
            obj['data'] = [self.convert(item) for item in obj['data']]
            return List(obj)
        elif obj.get('object') == 'response':
            return Response(obj)
        else:
            return ChargehoundObject(obj)

    def parse_response(self, response):
        payload = response.json()
        if response.status_code < 400:
            model = self.convert(payload)
            setattr(model, 'response', HTTPResponse(response.status_code))
            return model
        else:
            raise create_chargehound_error(payload)

    def get_url(self, path):
        url = chargehound.protocol + chargehound.host
        if chargehound.port:
            url += ':' + chargehound.port
        url += chargehound.base_path + path
        return url

    def make_request(self, method, path, params=None, data=None,
                     callback=None):
        headers = {
            'accept': 'application/json',
            'user-agent': 'Chargehound/v1 PythonBindings/%s' % VERSION
        }

        if chargehound.version:
            headers['chargehound-version'] = chargehound.version

        auth = (chargehound.api_key or '', '')

        if method == 'get':
            return self.parse_response(requests.get(self.get_url(path),
                                       auth=auth,
                                       params=params,
                                       headers=headers,
                                       timeout=chargehound.timeout))
        elif method == 'post':
            return self.parse_response(requests.post(self.get_url(path),
                                       auth=auth,
                                       json=data,
                                       headers=headers,
                                       timeout=chargehound.timeout))

    def request(self, method, path, params=None, data=None, callback=None):
        if callback is None:
            return self.make_request(method, path, params, data)
        else:
            return self.make_request(method, path, params, data, callback)
