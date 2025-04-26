# -*- coding: utf-8 -*-

"""
Objective Oriented Interface for AWS S3, similar to pathlib.
"""

from ._version import __version__

__short_description__ = "Objective Oriented Interface for AWS S3, similar to pathlib."
__license__ = "Apache License 2.0"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "sanhehu@amazon.com"
__github_username__ = "aws-samples"

try:
    from . import utils
    from .better_client import api
    from .aws import context
    from .core import S3Path
    from .content_type import ContentTypeEnum
    from .validate import validate_s3_bucket
    from .validate import validate_s3_key
    from .validate import validate_s3_uri
    from .validate import validate_s3_arn

    from iterproxy import and_, or_, not_
except ImportError:  # pragma: no cover
    pass
except:  # pragma: no cover
    raise
