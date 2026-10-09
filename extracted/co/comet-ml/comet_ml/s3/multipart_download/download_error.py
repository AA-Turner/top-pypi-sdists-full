# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
from typing import Optional

from ..multipart_transfer.errors import S3PartsTransferError


class S3DownloadError(S3PartsTransferError):
    """A direct-S3 download that could not be completed.

    ``status_code`` is the last response S3 gave, when there was one, so that a
    caller can tell an expired presigned URL (403) from an object that changed
    while it was being read (412) without parsing the message.
    """

    def __init__(
        self,
        reason: str,
        due_connection_error: bool = False,
        status_code: Optional[int] = None,
    ):
        super().__init__(reason, due_connection_error)
        self.status_code = status_code

    def __str__(self):
        msg = "S3 file download failed, reason: %s, due connection error: %s"
        return msg % (self.reason, self.due_connection_error)
