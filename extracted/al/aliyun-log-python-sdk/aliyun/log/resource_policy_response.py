#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Alibaba Cloud Computing
# All rights reserved.

from .logresponse import LogResponse
from .util import Util

__all__ = [
    "PutResourcePolicyResponse",
    "GetResourcePolicyResponse",
    "DeleteResourcePolicyResponse",
]


class PutResourcePolicyResponse(LogResponse):
    """The response of the put_resource_policy API."""

    def __init__(self, header, resp=""):
        LogResponse.__init__(self, header, resp)


class GetResourcePolicyResponse(LogResponse):
    """The response of the get_resource_policy API."""

    def __init__(self, resp, header):
        LogResponse.__init__(self, header, resp)
        self.resource_type = Util.convert_unicode_to_str(resp["resourceType"])
        self.resource_name = Util.convert_unicode_to_str(resp.get("resourceName", ""))
        self.policy_document = Util.convert_unicode_to_str(resp["policyDocument"])
        self.revision = int(resp["revision"])
        self.create_time = int(resp["createTime"])
        self.update_time = int(resp["updateTime"])

    def get_resource_type(self):
        return self.resource_type

    def get_resource_name(self):
        return self.resource_name

    def get_policy_document(self):
        return self.policy_document

    def get_revision(self):
        return self.revision

    def get_create_time(self):
        return self.create_time

    def get_update_time(self):
        return self.update_time

    def log_print(self):
        print("GetResourcePolicyResponse:")
        print("headers:", self.get_all_headers())
        print("resource_type:", self.resource_type)
        print("resource_name:", self.resource_name)
        print("policy_document:", self.policy_document)
        print("revision:", self.revision)
        print("create_time:", self.create_time)
        print("update_time:", self.update_time)


class DeleteResourcePolicyResponse(LogResponse):
    """The response of the delete_resource_policy API."""

    def __init__(self, header, resp=""):
        LogResponse.__init__(self, header, resp)
