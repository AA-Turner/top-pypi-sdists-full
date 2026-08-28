# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
from typing import Any, Dict

from ...config.config_constants import (
    S3_MULTIPART_EXPIRES_IN,
    S3_MULTIPART_PART_SIZE_DEFAULT,
    S3_MULTIPART_SIZE_THRESHOLD_DEFAULT,
)
from .file_parts import PartsUploadOptions
from .upload_types import DIRECT_S3_UPLOAD_TYPES


class MultipartUploadOptions:
    def __init__(
        self,
        file_size_threshold: int,
        upload_expires_in: int,
        direct_s3_upload_enabled: bool,
        parts_upload_options: PartsUploadOptions,
        part_size: int,
    ):
        """Prefer from_config() or defaults(). Every value is required here so
        that the defaults live in one place instead of at each layer."""
        self.file_size_threshold = file_size_threshold
        self.upload_expires_in = upload_expires_in
        self.direct_s3_upload_enabled = direct_s3_upload_enabled
        # How the asset is divided, as opposed to how many of those divisions are
        # sent at once. The two multiply into peak resident part data, so they are
        # chosen together even though they are configured separately.
        self.part_size = part_size
        # Carried as an object rather than as loose values so that changing how
        # per-part parallelism is configured does not ripple through the streamers.
        self.parts_upload_options = parts_upload_options

    @classmethod
    def from_config(
        cls, config: Any, direct_s3_upload_enabled: bool
    ) -> "MultipartUploadOptions":
        """Reads every S3 multipart setting. The only place that knows the keys."""
        return cls(
            file_size_threshold=config.get_int(
                None, "comet.s3_multipart.size_threshold"
            ),
            upload_expires_in=config.get_int(None, "comet.s3_multipart.expires_in"),
            direct_s3_upload_enabled=direct_s3_upload_enabled,
            parts_upload_options=PartsUploadOptions.from_config(config),
            part_size=config.get_int(None, "comet.s3_multipart.part_size"),
        )

    @classmethod
    def defaults(cls, **overrides: Any) -> "MultipartUploadOptions":
        """The built-in defaults, with anything the caller wants to pin."""
        values: Dict[str, Any] = {
            "file_size_threshold": S3_MULTIPART_SIZE_THRESHOLD_DEFAULT,
            "upload_expires_in": S3_MULTIPART_EXPIRES_IN,
            "direct_s3_upload_enabled": False,
            "parts_upload_options": PartsUploadOptions.defaults(),
            "part_size": S3_MULTIPART_PART_SIZE_DEFAULT,
        }
        values.update(overrides)
        return cls(**values)

    def has_direct_s3_upload_enabled_for(
        self, upload_type: str, file_size: int
    ) -> bool:
        if not self.direct_s3_upload_enabled:
            return False

        return (
            upload_type in DIRECT_S3_UPLOAD_TYPES
            and file_size >= self.file_size_threshold
        )
