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


class S3PartsTransferError(Exception):
    """A multipart transfer to or from S3 that could not be completed.

    The base of S3UploadError and S3DownloadError, and what the shared scheduler
    raises itself for a part it gave up on without ever running it. A caller that
    must tell a failed transfer from any other exception checks for this type, so
    that such a part is treated the same as one that failed in flight.
    """

    def __init__(self, reason: str, due_connection_error: bool = False):
        super().__init__(reason)
        self.reason = reason
        self.due_connection_error = due_connection_error

    def __str__(self):
        msg = "S3 file transfer failed, reason: %s, due connection error: %s"
        return msg % (self.reason, self.due_connection_error)
