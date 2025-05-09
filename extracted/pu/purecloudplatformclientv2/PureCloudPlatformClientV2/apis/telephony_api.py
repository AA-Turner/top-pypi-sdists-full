# coding: utf-8

"""
TelephonyApi.py
Copyright 2016 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import absolute_import

import sys
import os
import re

from datetime import datetime
from datetime import date

from ..configuration import Configuration
from ..api_client import ApiClient
from ..utils import deprecated

from typing import List
from typing import Dict
from typing import Any

from ..models import Empty
from ..models import Callheader
from ..models import Callmessage
from ..models import ErrorBody
from ..models import MediaRegions
from ..models import SIPSearchPublicRequest
from ..models import SignedUrlResponse
from ..models import SipDownloadResponse
from ..models import SipSearchResult

class TelephonyApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def get_telephony_mediaregions(self, **kwargs) -> 'MediaRegions':
        """
        Retrieve the list of AWS regions media can stream through.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_telephony_mediaregions(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: MediaRegions
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_telephony_mediaregions" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/telephony/mediaregions'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='MediaRegions',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_telephony_sipmessages_conversation(self, conversation_id: str, **kwargs) -> 'Callmessage':
        """
        Get a SIP message.
        Get the raw form of the SIP message

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_telephony_sipmessages_conversation(conversation_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str conversation_id: Conversation id (required)
        :return: Callmessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['conversation_id']
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_telephony_sipmessages_conversation" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'conversation_id' is set
        if ('conversation_id' not in params) or (params['conversation_id'] is None):
            raise ValueError("Missing the required parameter `conversation_id` when calling `get_telephony_sipmessages_conversation`")


        resource_path = '/api/v2/telephony/sipmessages/conversations/{conversationId}'.replace('{format}', 'json')
        path_params = {}
        if 'conversation_id' in params:
            path_params['conversationId'] = params['conversation_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Callmessage',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_telephony_sipmessages_conversation_headers(self, conversation_id: str, **kwargs) -> 'Callheader':
        """
        Get SIP headers.
        Get parsed SIP headers. Returns specific headers if key query parameters are added.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_telephony_sipmessages_conversation_headers(conversation_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str conversation_id: Conversation id (required)
        :param list[str] keys: comma-separated list of header identifiers to query. e.g. ruri,to,from
        :return: Callheader
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['conversation_id', 'keys']
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_telephony_sipmessages_conversation_headers" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'conversation_id' is set
        if ('conversation_id' not in params) or (params['conversation_id'] is None):
            raise ValueError("Missing the required parameter `conversation_id` when calling `get_telephony_sipmessages_conversation_headers`")


        resource_path = '/api/v2/telephony/sipmessages/conversations/{conversationId}/headers'.replace('{format}', 'json')
        path_params = {}
        if 'conversation_id' in params:
            path_params['conversationId'] = params['conversation_id']

        query_params = {}
        if 'keys' in params:
            query_params['keys'] = params['keys']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Callheader',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_telephony_siptraces(self, date_start: datetime, date_end: datetime, **kwargs) -> 'SipSearchResult':
        """
        Fetch SIP metadata
        Fetch SIP metadata that matches a given parameter. If exactMatch is passed as a parameter only sip records that have exactly that value will be returned. For example, some records contain conversationId but not all relevant records for that call may contain the conversationId so only a partial view of the call will be reflected

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_telephony_siptraces(date_start, date_end, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param datetime date_start: Start date of the search. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z (required)
        :param datetime date_end: End date of the search. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z (required)
        :param str call_id: unique identification of the placed call
        :param str to_user: User to who the call was placed
        :param str from_user: user who placed the call
        :param str conversation_id: Unique identification of the conversation
        :return: SipSearchResult
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['date_start', 'date_end', 'call_id', 'to_user', 'from_user', 'conversation_id']
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_telephony_siptraces" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'date_start' is set
        if ('date_start' not in params) or (params['date_start'] is None):
            raise ValueError("Missing the required parameter `date_start` when calling `get_telephony_siptraces`")
        # verify the required parameter 'date_end' is set
        if ('date_end' not in params) or (params['date_end'] is None):
            raise ValueError("Missing the required parameter `date_end` when calling `get_telephony_siptraces`")


        resource_path = '/api/v2/telephony/siptraces'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'call_id' in params:
            query_params['callId'] = params['call_id']
        if 'to_user' in params:
            query_params['toUser'] = params['to_user']
        if 'from_user' in params:
            query_params['fromUser'] = params['from_user']
        if 'conversation_id' in params:
            query_params['conversationId'] = params['conversation_id']
        if 'date_start' in params:
            query_params['dateStart'] = params['date_start']
        if 'date_end' in params:
            query_params['dateEnd'] = params['date_end']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='SipSearchResult',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_telephony_siptraces_download_download_id(self, download_id: str, **kwargs) -> 'SignedUrlResponse':
        """
        Get signed S3 URL for a pcap download
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_telephony_siptraces_download_download_id(download_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str download_id: unique id for the downloaded file in S3 (required)
        :return: SignedUrlResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['download_id']
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_telephony_siptraces_download_download_id" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'download_id' is set
        if ('download_id' not in params) or (params['download_id'] is None):
            raise ValueError("Missing the required parameter `download_id` when calling `get_telephony_siptraces_download_download_id`")


        resource_path = '/api/v2/telephony/siptraces/download/{downloadId}'.replace('{format}', 'json')
        path_params = {}
        if 'download_id' in params:
            path_params['downloadId'] = params['download_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='SignedUrlResponse',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_telephony_siptraces_download(self, sip_search_public_request: 'SIPSearchPublicRequest', **kwargs) -> 'SipDownloadResponse':
        """
        Request a download of a pcap file to S3
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_telephony_siptraces_download(sip_search_public_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param SIPSearchPublicRequest sip_search_public_request:  (required)
        :return: SipDownloadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['sip_search_public_request']
        all_params.append('callback')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_telephony_siptraces_download" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'sip_search_public_request' is set
        if ('sip_search_public_request' not in params) or (params['sip_search_public_request'] is None):
            raise ValueError("Missing the required parameter `sip_search_public_request` when calling `post_telephony_siptraces_download`")


        resource_path = '/api/v2/telephony/siptraces/download'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'sip_search_public_request' in params:
            body_params = params['sip_search_public_request']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='SipDownloadResponse',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response
