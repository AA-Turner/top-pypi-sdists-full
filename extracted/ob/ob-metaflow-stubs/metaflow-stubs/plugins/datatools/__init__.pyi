######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.898462                                                            #
######################################################################################################

from __future__ import annotations


from . import local as local
from .local import MetaflowLocalNotFound as MetaflowLocalNotFound
from .local import MetaflowLocalURLException as MetaflowLocalURLException
from .local import Local as Local
from . import s3 as s3
from .s3.s3 import MetaflowS3Exception as MetaflowS3Exception
from .s3.s3 import S3 as S3

def read_in_chunks(dst, src, src_sz, max_chunk_size):
    ...

