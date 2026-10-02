# Copyright 2024 Agnostiq Inc.
"""Test behavior while waiting for deployments"""

import time
import unittest
from unittest.mock import patch

import covalent_cloud as cc
from covalent_cloud.function_serve.common import ACTIVE_DEPLOYMENT_POLL_INTERVAL as POLL_FREQ
from covalent_cloud.function_serve.common import ServiceStatus
from covalent_cloud.function_serve.models import Deployment
from covalent_cloud.shared.classes.api import APIClient


class DeploymentResponse:
    """Response from which a deployment can be created."""

    def __init__(self, deployment: Deployment):
        self.deployment = deployment

    def json(self) -> dict:
        return {
            "id": self.deployment.function_id,
            "description": self.deployment.description,
            "invoke_url": self.deployment.address,
            "title": self.deployment.name,
            "endpoints": [],
            "tags": self.deployment.tags,
            "status": self.deployment.status,
            "inference_keys": [],
            "auth": False,
            "error": None,
            "stderr": None,
        }


class TestGetDeploymentWait(unittest.TestCase):
    """Test waiting behavior."""

    def _get_deployment_kwargs(self, **kwargs) -> dict:
        return {
            "function_id": "1234567890",
            "address": "http://fake-address.com",
            "name": "Fake Service for Testing",
            "description": "A fake service for testing purposes.",
            "routes": [],
            "status": ServiceStatus.ACTIVE,
            "tags": ["fake-tag-1", "fake-tag-2"],
            **kwargs,
        }

    def setUp(self) -> None:
        self.deployment = Deployment(**self._get_deployment_kwargs())

    def test_get_deployment_without_wait(self):
        """Test without waiting for deployment to be active."""

        def _mock_deployment_client_get(*_, **__):
            return DeploymentResponse(_mock_deployment_client_get.deployment)

        for status in ServiceStatus:
            dep = Deployment(**self._get_deployment_kwargs(status=status))
            _mock_deployment_client_get.deployment = dep
            with patch.object(APIClient, "get", new=_mock_deployment_client_get):
                t0 = time.monotonic()
                cc.get_deployment(dep, wait=False)
                tf = time.monotonic()
                assert (tf - t0) < POLL_FREQ, f"Status {status!s} should not wait if wait=False"

    def test_get_deployment_invalid_wait(self):
        """Test without waiting for deployment to be active."""

        def _mock_deployment_client_get(*_, **__):
            return DeploymentResponse(self.deployment)

        with patch.object(APIClient, "get", new=_mock_deployment_client_get):

            with self.assertRaises(ValueError):
                cc.get_deployment(self.deployment, wait="a string is invalid")

            with self.assertRaises(ValueError):
                cc.get_deployment(self.deployment, wait=["nor", "a", "list"])

            with self.assertRaises(ValueError):
                cc.get_deployment(self.deployment, wait={"not": "a", "dict": "either"})

            with self.assertRaises(ValueError):
                cc.get_deployment(self.deployment, wait=-1)  # negatives too, not allowed
