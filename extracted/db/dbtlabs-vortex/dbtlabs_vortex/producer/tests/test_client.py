import os
import threading
import time
from io import StringIO
from unittest.mock import ANY, patch

import pytest
from dbtlabs.proto.public.v1.events.vscode_pb2 import ExtensionActivated

from dbtlabs_vortex.common.exceptions import ProducerError
from dbtlabs_vortex.producer.client import ErrorMode, VortexProducerClient
from dbtlabs_vortex.producer.ddtrace import has_ddtrace_dependency


class TestVortexProducerClient:
    def test_client_initialization(self):
        try:
            VortexProducerClient._initialize()
            queue = VortexProducerClient.queue
            assert queue is not None
            VortexProducerClient._initialize()
            # log a message here to ensure that ddtrace has started up whatever background
            # threads it wants
            VortexProducerClient.log_proto(ExtensionActivated())
            # these should be the same instance! make sure a second queue
            # is not created
            assert queue == VortexProducerClient.queue
            # vortex producer should always be running 2 threads: main thread and one
            # background thread. depending on the package versions installed, there
            # may be other threads running: e.g. ddtrace runs different number of threads
            # depending on the version.
            #
            # what we want to test here is that calling _initialize() multiple times
            # in a row doesn't result in leaking threads.
            start_thread_count = threading.active_count()
            assert threading.active_count() == start_thread_count

            VortexProducerClient._initialize()
            VortexProducerClient._initialize()
            VortexProducerClient._initialize()
            assert threading.active_count() == start_thread_count

            VortexProducerClient._reset()
            VortexProducerClient._initialize()
            assert threading.active_count() == start_thread_count

        finally:
            VortexProducerClient._reset()

    def test_client_shutdown(self):
        try:
            VortexProducerClient._initialize()
            VortexProducerClient.shutdown()
            assert VortexProducerClient.queue_closed
        finally:
            VortexProducerClient._reset()

    def test_client_send_message(self):
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                VortexProducerClient.log_proto(ExtensionActivated())
                VortexProducerClient.shutdown()
                assert VortexProducerClient.queue_closed
                mock_post.assert_called_once()
        finally:
            VortexProducerClient._reset()

    def test_dev_mode(self):
        def mock_os_getenv_side_effect(key: str) -> str:
            if key == "VORTEX_DEV_MODE":
                return "true"
            return ""

        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                with patch("os.getenv") as mock_os_getenv:
                    mock_os_getenv.side_effect = mock_os_getenv_side_effect
                    VortexProducerClient.log_proto(ExtensionActivated())
                    VortexProducerClient.shutdown()
                    mock_post.assert_not_called()
        finally:
            VortexProducerClient._reset()

    def test_custom_base_url(self):
        vortex_service_name = "vortex-client-python-test"
        vortex_service_version = "1.0.0"

        def mock_get_import_version_side_effect(package_name: str) -> str:
            if package_name == "dbtlabs-vortex":
                return "0.1.5"
            if package_name == "dbt-protos":
                return "1.0.279"
            return "0.0.0"

        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                with patch.dict(
                    os.environ,
                    {
                        "VORTEX_BASE_URL": "http://vortex-api.dbt-cloud.svc.cluster.local:8083",
                        "VORTEX_INGEST_ENDPOINT": "/internal/v1/ingest/protobuf",
                        "DD_SERVICE": vortex_service_name,
                        "DD_VERSION": vortex_service_version,
                    },
                ):
                    with patch(
                        "dbtlabs_vortex.producer.client._get_import_version"
                    ) as mock_get_import_version:
                        mock_get_import_version.side_effect = mock_get_import_version_side_effect
                        VortexProducerClient.log_proto(ExtensionActivated())
                        VortexProducerClient.shutdown()
                        assert VortexProducerClient.queue_closed
                        mock_post.assert_called_once()
                        mock_post.assert_called_once_with(
                            "http://vortex-api.dbt-cloud.svc.cluster.local:8083/internal/v1/ingest/protobuf",
                            headers={
                                "Content-Type": "application/vnd.google.protobuf",
                                "X-Vortex-Client-Platform": f"{vortex_service_name}/{vortex_service_version} vortex-client-python/0.1.5 proto-python/1.0.279",
                            },
                            data=ANY,
                        )
        finally:
            VortexProducerClient._reset()

    def test_client_send_message_error(self):
        # the client will not raise an exception, only log it, if the service is down:
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                mock_post.side_effect = Exception("Test error")
                VortexProducerClient.log_proto(ExtensionActivated())
                VortexProducerClient.shutdown()
                assert VortexProducerClient.queue_closed
                mock_post.assert_called_once()
        finally:
            VortexProducerClient._reset()

    def test_client_send_does_not_block(self):
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                # uh oh -- the thread has shut down, but the client still thinks
                # it's running!
                VortexProducerClient._initialize()
                VortexProducerClient.shutdown()
                VortexProducerClient.initialized = True
                VortexProducerClient.queue_closed = False

                # make sure this succeeds and doesn't block even if the thread is dead
                VortexProducerClient.log_proto(ExtensionActivated())

                mock_post.assert_not_called()
        finally:
            VortexProducerClient._reset()

    def test_client_send_does_not_block_with_dead_queue(self):
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                # uh oh -- the thread has shut down, but the client still thinks
                # it's running!
                VortexProducerClient._initialize()

                # simulate queue shutting down
                VortexProducerClient.queue.put(None)
                VortexProducerClient.thread.join()

                # make sure this succeeds and doesn't block even if the thread is dead
                VortexProducerClient.log_proto(
                    ExtensionActivated(),
                    error_mode=ErrorMode.LOG_AND_CONTINUE,
                )

                # with a different error mode, this should raise an exception
                with pytest.raises(ProducerError):
                    VortexProducerClient.log_proto(
                        ExtensionActivated(),
                        error_mode=ErrorMode.LOG_AND_RAISE,
                    )

                mock_post.assert_not_called()
        finally:
            VortexProducerClient._reset()

    def test_client_send_does_not_block_with_full_queue(self):
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                # uh oh -- the thread has shut down, but the client still thinks
                # it's running!
                VortexProducerClient._initialize(1)
                print("initialized")
                VortexProducerClient.shutdown()
                print("shutdown")
                VortexProducerClient.initialized = True
                VortexProducerClient.queue_closed = False

                start = time.time()
                print("logging proto 1")
                VortexProducerClient.log_proto(ExtensionActivated())
                print("logging proto 2")
                VortexProducerClient.log_proto(ExtensionActivated())
                end = time.time()
                assert end - start < 0.1
                mock_post.assert_not_called()

        finally:
            print("resetting")
            VortexProducerClient._reset()

    def test_client_send_does_block_with_full_queue(self):
        try:
            with patch("dbtlabs_vortex.producer.client.requests.post") as mock_post:
                # uh oh -- the thread has shut down, but the client still thinks
                # it's running!
                VortexProducerClient._initialize(1)
                print("initialized")
                VortexProducerClient.shutdown()
                print("shutdown")
                VortexProducerClient.initialized = True
                VortexProducerClient.queue_closed = False

                start = time.time()
                print("logging proto 1")
                VortexProducerClient.log_proto(ExtensionActivated())
                print("logging proto 2")
                VortexProducerClient.log_proto(
                    ExtensionActivated(),
                    wait_seconds=0.1,
                )
                end = time.time()
                assert end - start > 0.1
                mock_post.assert_not_called()

        finally:
            print("resetting")
            VortexProducerClient._reset()

    def test_log_settings(self):
        """
        Test that the client can turn off logging, in particular from ddtrace!
        """
        if not has_ddtrace_dependency():
            pytest.skip("ddtrace is not installed")

        # set up a mock logger
        import logging

        log_capture = StringIO()
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(log_capture))

        try:
            with patch("ddtrace.vendor.psutil.swap_memory") as mock_swap_memory:
                # Simulate FileNotFoundError when trying to access /proc/meminfo
                mock_swap_memory.side_effect = FileNotFoundError(
                    "[Errno 2] No such file or directory: '/proc/meminfo'"
                )

                # This should not raise an exception
                VortexProducerClient._initialize()

                # try logging directly to ddtrace
                from ddtrace.internal.logger import get_logger

                dd_logger = get_logger("ddtrace.settings.profiling")
                dd_logger.warning("SENTINEL")

                # try logging by calling the bad function
                from ddtrace.settings.profiling import (
                    ProfilingConfig,
                    _derive_default_heap_sample_size,
                )

                config = ProfilingConfig.heap()
                _derive_default_heap_sample_size(config)

                # Get the captured output
                output = log_capture.getvalue()

                assert "SENTINEL" not in output
                assert "Unable to get total memory available" not in output

        finally:
            VortexProducerClient._reset()
