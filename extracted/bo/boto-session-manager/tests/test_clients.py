# -*- coding: utf-8 -*-

from boto_session_manager.clients import ClientMixin

import boto3

from boto_session_manager.manager import BotoSesManager
from boto_session_manager.services import AwsServiceEnum


def test_one_property_per_service():
    """
    Every AwsServiceEnum member has its ``<name lower-cased>_client`` property.
    """
    for name in vars(AwsServiceEnum):
        if name.startswith("_"):
            continue
        prop = getattr(ClientMixin, f"{name.lower()}_client")
        assert isinstance(prop, property)


def test_property_returns_the_cached_client():
    """
    Each property creates the client of its service (offline, fake credentials).
    """
    bsm = BotoSesManager(
        aws_access_key_id="AKIAFAKE",
        aws_secret_access_key="fake-secret",
        region_name="us-east-1",
    )
    available = set(boto3.session.Session().get_available_services())
    for name, service_id in vars(AwsServiceEnum).items():
        if name.startswith("_") or service_id not in available:
            continue
        client = getattr(bsm, f"{name.lower()}_client")
        assert client is bsm.get_client(service_id)
        assert client.meta.service_model.service_name is not None


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.clients",
        preview=False,
    )
