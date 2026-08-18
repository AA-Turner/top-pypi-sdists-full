######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-17T19:44:19.594813                                                            #
######################################################################################################

from __future__ import annotations


from .s3util import aws_retry as aws_retry
from .s3util import get_s3_client as get_s3_client

class S3Tail(object, metaclass=type):
    def __init__(self, s3url):
        ...
    def reset_client(self, hard_reset = False):
        ...
    def clone(self, s3url):
        ...
    @property
    def bytes_read(self):
        ...
    @property
    def tail(self):
        ...
    def __iter__(self):
        ...
    def _make_range_request(self, *args, **kwargs):
        ...
    ...

