from __future__ import annotations

import abc
from typing import TYPE_CHECKING

# import numpy as np
from bec_lib.logger import bec_logger
from bec_lib.signature_serializer import signature_to_dict

if TYPE_CHECKING:
    from bec_lib.client import BECClient


logger = bec_logger.logger


class DAPError(Exception):
    pass


class DAPServiceBase(abc.ABC):
    """
    Base class for data processing services. For most services, the user should
    override the configure and process methods. The configure method is called
    when the service is initialized and the process method is called when the
    service is requested to process data. The process method should return a
    tuple of (stream_output, metadata) and the return value should be serializable.

    For services that require continuous data processing, the user should override
    the on_scan_status_update method. The underlying service manager will call this
    method when a scan status update is received.
    """

    AUTO_FIT_SUPPORTED = False

    def __init__(self, *args, client: BECClient, **kwargs) -> None:
        super().__init__()
        self.client = client
        self.scans = None
        self.scan_id = None
        self.current_scan_item = None

    @classmethod
    def get_class_doc_string(cls, *args, **kwargs):
        """
        Get the public doc string.
        """
        return cls.configure.__doc__ or cls.__init__.__doc__

    @classmethod
    def get_run_doc_string(cls, *args, **kwargs):
        """
        Get the fit doc string.
        """
        return cls.configure.__doc__

    @classmethod
    def get_user_friendly_run_name(cls):
        """
        Get the user friendly run name.
        """
        return "run"

    @classmethod
    def describe_service(cls, *args, **kwargs):
        """
        Describe the service.
        """
        return {
            "class": cls.__name__,
            "user_friendly_name": cls.get_user_friendly_name(),
            "class_doc": cls.get_class_doc_string(),
            "run_doc": cls.get_run_doc_string(),
            "run_name": cls.get_user_friendly_run_name(),
            "signature": cls.get_signature(),
            "params": cls.get_parameters(),
            "auto_run_supported": getattr(cls, "AUTO_FIT_SUPPORTED", False),
            "class_args": [],
            "class_kwargs": {},
        }

    @classmethod
    def get_provided_services(cls):
        """
        Get the information about the provided services by the class.
        """
        return {cls.__name__: cls.describe_service()}

    @classmethod
    def get_parameters(cls, *args, **kwargs):
        """
        Get the parameters for the service.
        """
        return {}

    @classmethod
    def get_signature(cls, *args, **kwargs):
        """
        Get the signature for the service.
        """
        return signature_to_dict(cls.configure)

    @classmethod
    def get_user_friendly_name(cls, *args, **kwargs):
        """
        Get the user friendly name for the service.
        """
        return cls.__name__

    def _update_scan_id_and_item(self, status: dict):
        """
        Update the scan ID and the current scan item with the provided scan status.

        Args:
            status (dict): Scan status
        """
        scan_id = status.get("scan_id")
        if scan_id != self.scan_id:
            self.current_scan_item = self.client.queue.scan_storage.find_scan_by_ID(scan_id)
        self.scan_id = scan_id

    def _process_scan_status_update(self, status: dict, metadata: dict):
        """
        Process a scan status update. This method is called by the service manager and
        should not be overridden or invoked directly.

        Args:
            status (dict): Scan status
            metadata (dict): Scan metadata
        """
        self._update_scan_id_and_item(status)
        self.on_scan_status_update(status, metadata)

    def on_scan_status_update(self, status: dict, metadata: dict):
        """
        Override this method to process a continuous dap request.
        The underlying service manager will call this method when a
        scan status update is received.

        Args:
            status (dict): Scan status
            metadata (dict): Scan metadata

        Example:
            >>> def on_scan_status_update(self, status: dict, metadata: dict):
            >>>     if status.get("status") == "closed":
            >>>         self.process()
        """

    def configure(self, *args, **kwargs):
        """
        Configure the service using the provided parameters by the user.
        The process request's config dictionary will be passed to this method.
        """

    def process(self):
        """
        Process the data and return the result. Ensure that the return value
        is a tuple of (stream_output, metadata) and that it is serializable.
        """
