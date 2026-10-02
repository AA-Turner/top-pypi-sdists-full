#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)

import threading
from django.http import HttpRequest


class GlobalRequestStorage(object):
    storage = threading.local()

    def get(self):
        if hasattr(self.storage, "request"):
            return self.storage.request
        else:
            return None

    def get_user(self, request=None):
        request = request or self.get()
        return getattr(request, "user", None)

    def set(self, request):
        self.storage.request = request

    def set_user(self, user, request=None):
        if request:
            self.storage.request = request
        if not hasattr(self.storage, "request"):
            self.storage.request = HttpRequest()
        if user:
            self.storage.request.user = user

    def recover(self, request=None, user=None):
        if hasattr(self.storage, "request"):
            del self.storage.request
        if request:
            self.storage.request = request
            if user:
                self.storage.request.user = user


GLOBAL_REQUEST_STORAGE = GlobalRequestStorage()


class GlobalRequest(object):
    def __init__(self, request=None, user=None):
        self.new_request = request or HttpRequest()
        self.new_user = user
        self.old_request = GLOBAL_REQUEST_STORAGE.get()
        self.old_user = GLOBAL_REQUEST_STORAGE.get_user(self.old_request)

    def set(self):
        GLOBAL_REQUEST_STORAGE.set_user(user=self.new_user, request=self.new_request)
        return GLOBAL_REQUEST_STORAGE.get()

    def reset(self):
        GLOBAL_REQUEST_STORAGE.recover(request=self.old_request, user=self.old_user)

    def __enter__(self):
        return self.set()

    def __exit__(self, *args, **kwargs):
        return self.reset()


class GlobalRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_flag = False
        global_request = GlobalRequest(request=request)
        try:
            global_request.set()
            reset_flag = True

            def streaming_content_wrapper(streaming_content):
                for chunk in streaming_content:
                    yield chunk
                global_request.reset()

            response = self.get_response(request)
            if hasattr(response, "streaming") and response.streaming:
                reset_flag = False
                response.streaming_content = streaming_content_wrapper(
                    response.streaming_content
                )
            return response
        finally:
            if reset_flag:
                global_request.reset()


def get_request():
    return GLOBAL_REQUEST_STORAGE.get()
