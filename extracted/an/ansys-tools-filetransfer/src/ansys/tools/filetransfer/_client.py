# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# Copyright 2022 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The high-level Python client for the FileTransfer Tool.

This module implements the high-level Python client for interacting with
the Ansys FileTransfer Tool Server via gRPC.
"""
from collections.abc import Generator
import hashlib
import os
import stat

import grpc

from ansys.api.tools.filetransfer.v1 import (
    file_transfer_service_pb2,
    file_transfer_service_pb2_grpc,
)

from ._log import LOGGER


class Client:
    """Provides the high-level Python client for the FileTransfer Tool.

    You use this client's high-level API to upload and download files to
    the FileTransfer Tool Server.
    """

    def __init__(self, channel: grpc.Channel, max_message_length: int | None = None):
        """Initialize the client.

        Parameters
        ----------
        channel :
            gRPC channel on which the client communicates with the
            server.
        max_message_length :
            Maximum message size that is configured on the given
            channel. Note that this does **not** change the channel
            configuration. This parameter is used to check that the
            ``chunk_size`` parameter used for upload and download fits
            within the maximum message length, with some slack.
        """
        self._channel = channel
        if max_message_length is None:
            # Set the max_message_length to 4GB if it is not set.
            # This is the technical limit. For more information, see
            # https://groups.google.com/g/google-cloud-endpoints/c/sYT4BopjohI.
            self._max_message_length = 1 << 32
        else:
            self._max_message_length = max_message_length
        self._filetransfer_stub = file_transfer_service_pb2_grpc.FileTransferServiceStub(
            self._channel
        )

    @classmethod
    def from_server_address(
        cls,
        server_address: str,
        *,
        max_message_length: int = 1 << 17,
    ) -> "Client":
        """Initialize the client from a server URL.

        Parameters
        ----------
        server_address :
            IPv4/IPv6 address and port of the server to connect to. For example, ``10.0.0.42:12345``.
        max_message_length :
            Maximum message length in bytes to send over the channel.

        Returns
        -------
        :
            Instantiated FileTransfer client.
        """
        if not server_address:
            raise ValueError("No server address was given.")

        channel = grpc.insecure_channel(
            server_address,
            options=[
                ("grpc.max_send_message_length", max_message_length),
                ("grpc.max_receive_message_length", max_message_length),
            ],
        )
        return cls(channel=channel, max_message_length=max_message_length)

    def _log_progress(
        self, call: str, progress: file_transfer_service_pb2.ProgressResponse
    ) -> None:
        LOGGER.debug("[%s] progress : %d %%" % (call, progress.state))

    def _check_chunk_size(self, chunk_size: int) -> None:
        if chunk_size > self._max_message_length:
            raise ValueError(
                f"The chunk size '{chunk_size}' exceeds the maximum message length "
                f"'{self._max_message_length}' of the gRPC channel."
            )
        elif (2 * chunk_size) > self._max_message_length:
            LOGGER.warning(
                f"The chunk size '{chunk_size}' is close to the maximum message length "
                f"'{self._max_message_length}' of the gRPC channel."
            )

    def download_file(
        self,
        remote_filename: str,
        local_filename: str,
        chunk_size: int = 1 << 16,
        compute_sha1_checksum: bool = True,
    ) -> None:
        """Download a file from the server.

        Parameters
        ----------
        remote_filename :
            Name of the remote file to download.
        local_filename :
            Name of the local file to create.
        chunk_size :
            Maximum size in bytes of a chunk of data to transfer per request.
        compute_sha1_checksum :
            Whether to compute the SHA1-checksum of the file to be downloaded on the
            server-side.

        Raises
        ------
        RuntimeError :
            If a response indicates an error on the server-side.
        ValueError :
            If the checksums between the downloaded file and remote file do not match.

        """
        self._check_chunk_size(chunk_size)

        sha1sum = "0"
        n_bytes_received = 0

        # download iterator
        def download_file_iterator() -> (
            Generator[file_transfer_service_pb2.DownloadFileRequest, None, None]
        ):
            # 1) send info
            yield file_transfer_service_pb2.DownloadFileRequest(
                initialize=file_transfer_service_pb2.DownloadFileRequest.Initialize(
                    filename=remote_filename,
                    chunk_size=chunk_size,
                    compute_sha1_checksum=compute_sha1_checksum,
                )
            )
            # 2) receive data
            yield file_transfer_service_pb2.DownloadFileRequest(
                receive_data=file_transfer_service_pb2.DownloadFileRequest.ReceiveData()
            )
            # 3) finalize
            yield file_transfer_service_pb2.DownloadFileRequest(
                finalize=file_transfer_service_pb2.DownloadFileRequest.Finalize()
            )

        # stream data
        with open(local_filename, "wb") as f:
            for response in self._filetransfer_stub.DownloadFile(download_file_iterator()):
                # self._check_result(response.result)
                self._log_progress("download_file", response.progress)
                if response.WhichOneof("sub_step") == "file_info":
                    # file_size = int(response.file_info.size)
                    sha1sum = str(response.file_info.sha1.hex_digest)
                elif response.WhichOneof("sub_step") == "file_data":
                    f.write(response.file_data.data)
                    n_bytes_received += len(response.file_data.data)
                else:
                    pass

        # size_of_file_in_bytes = os.stat(local_filename)[stat.ST_SIZE]
        if compute_sha1_checksum:
            hexdigest = _get_file_hash(local_filename, "sha1")
            if hexdigest != sha1sum:
                raise ValueError(
                    "Checksum mismatch (%s != %s) exists between local and remote files. Download failed."
                    % (hexdigest, sha1sum)
                )

    def upload_file(
        self, local_filename: str, remote_filename: str, chunk_size: int = 1 << 16
    ) -> None:
        """Upload a file to the server.

        Parameters
        ----------
        local_filename :
            Name of the local file to upload.
        remote_filename :
            Name of the remote file to create.
        chunk_size :
            Maximum size in bytes of a chunk of data to transfer per request.

        Raises
        ------
        RuntimeError :
            If a response indicates an error on the server-side.

        """
        self._check_chunk_size(chunk_size)

        # prepare
        size_of_file_in_bytes = os.stat(local_filename)[stat.ST_SIZE]
        sha1sum = _get_file_hash(local_filename, "sha1")

        # upload iterator
        def upload_file_iterator() -> (
            Generator[file_transfer_service_pb2.UploadFileRequest, None, None]
        ):
            # 1) send info
            yield file_transfer_service_pb2.UploadFileRequest(
                initialize=file_transfer_service_pb2.UploadFileRequest.Initialize(
                    file_info=file_transfer_service_pb2.FileInfo(
                        name=remote_filename,
                        size=size_of_file_in_bytes,
                        sha1=file_transfer_service_pb2.SHA1(hex_digest=sha1sum),
                    )
                )
            )
            # 2) stream file content in chunks
            with open(local_filename, "rb") as f:
                offset = 0
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    assert len(chunk) > 0  # should be caught by the sentinel value in 'iter'
                    # send data
                    yield file_transfer_service_pb2.UploadFileRequest(
                        send_data=file_transfer_service_pb2.UploadFileRequest.SendData(
                            file_data=file_transfer_service_pb2.FileChunk(offset=offset, data=chunk)
                        )
                    )
                    offset += len(chunk)
            if offset != size_of_file_in_bytes:
                raise RuntimeError(
                    "File transfer failed: The size of the file has changed during upload."
                )
            # 3) finalize
            yield file_transfer_service_pb2.UploadFileRequest(
                finalize=file_transfer_service_pb2.UploadFileRequest.Finalize()
            )

        # stream data
        for response in self._filetransfer_stub.UploadFile(upload_file_iterator()):
            self._log_progress("upload_file", response.progress)


def _get_file_hash(filename: str, algorithm: str = "md5") -> str:
    """Get the hash checksum of a file.

    Parameters
    ----------
    filename :
        Name of the file to process.
    algorithm :
        Hash algorithm to use.

    Returns
    -------
    :
        Hash of the file.
    """
    method = hashlib.new(algorithm)
    with open(filename, "rb") as f:
        chunkSize = 128 * method.block_size
        for chunk in iter(lambda: f.read(chunkSize), ""):
            if len(chunk) == 0:
                break
            method.update(chunk)
    return method.hexdigest()
