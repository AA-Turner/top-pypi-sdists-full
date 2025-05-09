# coding: utf-8

"""
    PowerBot - Webservice for algotrading

    # TERMS AND CONDITIONS The PowerBot system provides B2B services for trading at intraday power markets. By using the PowerBot service, each user agrees to the terms and conditions of this licence: 1. The user confirms that they are familiar with the exchanges trading system and all relevant rules, is professionally qualified and in possession of a trading license for the relevant exchange. 2. The user will comply with the exchanges market rules (e.g. [EPEX Spot Market Rules](https://www.epexspot.com/en/downloads#rules-fees-processes) or [Nord Pool Market Rules](https://www.nordpoolgroup.com/trading/Rules-and-regulations/)) and will not endanger the exchange system at any time with heavy load from trading algorithms or by other use. 3. The user is aware of limits imposed by the exchange. 4. The user is solely liable for actions resulting from the use of PowerBot.   # INTRODUCTION PowerBot is a web-based software service enabling algorithmic trading on intraday power exchanges such as EPEX, Nord Pool, HUPX, BSP Southpool, TGE, OPCOM or ETPA. The service is straightforward to integrate in an existing software environment and provides a variety of programming interfaces for development of individual trading algorithms and software tools. Besides enabling fully automated intraday trading, it can be used to create tools for human traders providing relevant information and trading opportunities or can be integrated in existing software tools. For further details see https://www.powerbot-trading.com  ## Knowledge Base In addition to this API guide, please find the documentation at https://docs.powerbot-trading.com - the password will be provided by the PowerBot team. If not, please reach out to us at support@powerbot-trading.com  ## Endpoints The PowerBot service is available at the following REST endpoints:  | Instance      | Base URL for REST Endpoints                                      | |---------------|------------------------------------------------------------------| | EPEX          | https://staging.powerbot-trading.com/playground/epex/v2/api      | | Nord Pool     | https://staging.powerbot-trading.com/playground/nordpool/v2/api  | | HUPX          | https://staging.powerbot-trading.com/playground/hupx/v2/api      | | BSP Southpool | https://staging.powerbot-trading.com/playground/southpool/v2/api | | TGE           | https://staging.powerbot-trading.com/playground/tge/v2/api       | | IBEX          | https://staging.powerbot-trading.com/playground/ibex/v2/api      | | CROPEX        | https://staging.powerbot-trading.com/playground/cropex/v2/api    | | OPCOM         | https://staging.powerbot-trading.com/playground/opcom/v2/api     | | ETPA          | https://staging.powerbot-trading.com/playground/etpa/v2/api      | | BRM           | https://staging.powerbot-trading.com/playground/brm/v2/api       |  Access to endpoints is secured via an API Key, which needs to be passed as an \"api_key\" header in each request.   Notes on API Keys:  * API keys are specific to Test, Staging or Production.  * API keys are generated by the system administrator and need to be requested.  ## How to generate API clients (libraries) This OpenAPI specification can be used to generate API clients (programming libraries) for a wide range of programming languages using tools like [OpenAPI Generator](https://openapi-generator.tech/). A detailed guide can be found in the [knowledge base](https://docs.powerbot-trading.com/articles/getting-started/generating-clients/).  ## PowerBot Python client For Python, a ready-made client is also available on PyPI and can be downloaded locally via:  ```shell   pip install powerbot-client ```  ## Errors The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be in JSON format as follows:  ``` {   \"message\": \"... an error message ...\" } ```  ## Paging The API uses offset and limit parameters for paged operations. An X-Total-Count header is added to responses to indicate the total number of items in a paged response.  ## API Rate Limiting The API limits the number of concurrent calls to 50 - when that limit is reached, the client will receive 503 http status codes (service unavailable) with the following text:  ``` {   \"message\": \"API rate limit exceeded\" } ``` Clients should ensure that they stay within the limit for concurrent API calls.    ## Additional code samples Additional information and code samples demonstrating the use of the API can be found at in our [knowledge base](https://docs.powerbot-trading.com/docs/programmatic-access/)  # noqa: E501

    The version of the OpenAPI document: 2.22.1
    Contact: office@powerbot-trading.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from powerbot_client.api_client import ApiClient
from powerbot_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class SubscriptionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_subscription_endpoints(self, **kwargs):  # noqa: E501
        """List websocket endpoints  # noqa: E501

        Allows you to retrieve a list of all possible websockets endpoints you can subscribe to. Please note that you need to use a different technology to do this, this method only provides a list for information purposes. The response models can be found in the full openAPI specification. Each websocket message contains a sequence number within the header, which can be utilized to check for missing messages. This number resets on application restart. Note: Websocket connection will be terminated if websocket cache is full. This usually happens, if messages are not consumed fast enough. <p> You can test websocket subscriptions [here](https://websockets.powerbot-trading.com/)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_subscription_endpoints(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: list[SubscriptionEndpoint]
        """
        kwargs['_return_http_data_only'] = True
        return self.get_subscription_endpoints_with_http_info(**kwargs)  # noqa: E501

    def get_subscription_endpoints_with_http_info(self, **kwargs):  # noqa: E501
        """List websocket endpoints  # noqa: E501

        Allows you to retrieve a list of all possible websockets endpoints you can subscribe to. Please note that you need to use a different technology to do this, this method only provides a list for information purposes. The response models can be found in the full openAPI specification. Each websocket message contains a sequence number within the header, which can be utilized to check for missing messages. This number resets on application restart. Note: Websocket connection will be terminated if websocket cache is full. This usually happens, if messages are not consumed fast enough. <p> You can test websocket subscriptions [here](https://websockets.powerbot-trading.com/)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_subscription_endpoints_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(list[SubscriptionEndpoint], status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_subscription_endpoints" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_security']  # noqa: E501

        response_types_map = {
            200: "list[SubscriptionEndpoint]",
        }

        return self.api_client.call_api(
            '/subscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
