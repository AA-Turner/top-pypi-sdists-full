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
import logging
from typing import Optional, Tuple

from requests import Response, Session

from ...file_upload_size_monitor import UploadSizeMonitor
from .base_helper import MultipartUploadMetadata, S3MultipartBaseHelper
from .file_parts import (
    PartsCollector,
    PartsUploadScheduler,
    RetryingPartSender,
    SerialPartsUploadScheduler,
    open_parts_source,
)
from .file_parts.part_types import PartMetadata  # noqa: F401  (kept importable here)
from .file_parts_strategy import BaseFilePartsStrategy
from .upload_error import S3UploadError

LOGGER = logging.getLogger(__name__)


class S3MultipartUploader(object):
    """Drives one multipart upload: start, send every part, complete.

    How the parts are actually sent is not this class's concern. It receives a
    scheduler, which is serial unless a parts pool was supplied further up, and a
    sender, which owns the retry behaviour. That keeps the start/complete
    handshake identical for both the serial and the parallel paths.
    """

    def __init__(
        self,
        file_parts_strategy: BaseFilePartsStrategy,
        s3_helper: S3MultipartBaseHelper,
        scheduler: PartsUploadScheduler,
        part_sender: RetryingPartSender,
    ):
        """Prefer create(). Both collaborators are required here so that this class
        holds no opinion about which scheduler or sender is the default."""
        self.s3_helper = s3_helper
        self.file_parts_strategy = file_parts_strategy
        self._scheduler = scheduler
        self._part_sender = part_sender
        self._collector = PartsCollector()

    @classmethod
    def create(
        cls,
        file_parts_strategy: BaseFilePartsStrategy,
        s3_helper: S3MultipartBaseHelper,
        scheduler: Optional[PartsUploadScheduler] = None,
    ) -> "S3MultipartUploader":
        """Builds an uploader with the sender derived from the helper it was given.

        Omitting the scheduler gives the serial one, which is the behaviour that
        shipped before per-part parallelism.
        """
        return cls(
            file_parts_strategy=file_parts_strategy,
            s3_helper=s3_helper,
            scheduler=(
                scheduler if scheduler is not None else SerialPartsUploadScheduler()
            ),
            part_sender=RetryingPartSender(
                retry_strategy=s3_helper.upload_retry_strategy_op,
                file_name=file_parts_strategy.file,
            ),
        )

    @property
    def bytes_read(self) -> int:
        return self._collector.bytes_read

    def upload(
        self, session: Session, monitor: Optional[UploadSizeMonitor] = None
    ) -> Tuple[int, Response]:
        parts_number = self.file_parts_strategy.calculate()
        multipart_info = self.s3_helper.start_multipart_upload(
            session=session, parts_number=parts_number
        )
        self._collector = PartsCollector(monitor=monitor)
        return self._do_upload(session=session, multipart_info=multipart_info)

    def _do_upload(
        self, session: Session, multipart_info: MultipartUploadMetadata
    ) -> Tuple[int, Response]:
        try:
            with open_parts_source(
                strategy=self.file_parts_strategy,
                parts_urls=multipart_info.parts_urls,
                # So the progress display moves while parts are in flight rather
                # than only as each one lands.
                on_part_progress=self._collector.on_part_progress,
            ) as source:
                self._scheduler.upload(
                    source=source,
                    sender=self._part_sender,
                    collector=self._collector,
                )
        except Exception as ex:
            LOGGER.error(
                "Failed to upload file parts to S3, Comet request ID: %r",
                multipart_info.request_id,
                exc_info=True,
            )
            # complete upload with error status
            if isinstance(ex, S3UploadError) and not ex.due_connection_error:
                self.s3_helper.complete_multipart_upload(
                    session=session,
                    upload_metadata=multipart_info,
                    parts=[],
                    succeed=False,
                    file_size=-1,
                )
            raise ex

        # complete upload with collected parts and success status
        bytes_read = self._collector.bytes_read
        response = self.s3_helper.complete_multipart_upload(
            session=session,
            upload_metadata=multipart_info,
            parts=self._collector.completed_parts(),
            succeed=True,
            file_size=bytes_read,
        )
        return bytes_read, response
