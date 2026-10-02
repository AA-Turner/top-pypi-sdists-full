# Copyright 2024 Agnostiq Inc.
"""Tests around deploying services"""
from contextlib import contextmanager
from unittest.mock import Mock, patch

import pytest

import covalent_cloud as cc
from covalent_cloud.function_serve.assets import AssetsMediator
from covalent_cloud.function_serve.deployment import deploy
from covalent_cloud.function_serve.models import Deployment
from covalent_cloud.function_serve.service_class import FunctionService
from covalent_cloud.shared.classes.api import DeploymentAPI


def sample_func(x, /, y, *args, foo="default", k, bar="kw_default", **kwargs):
    """
    Sample service to test deployment
    """
    return {"x": x, "y": y, "args": args, "foo": foo, "k": k, "bar": bar, "kwargs": kwargs}


sample_service = cc.service(
    sample_func, executor=Mock(memory=20_480)  # will break real deployment attempt
)


@contextmanager
def mock_deploy_to_cloud():
    """Patch everything inside the deploy wrapper"""
    with patch.object(DeploymentAPI, "post"), patch.object(
        FunctionService, "get_model"
    ), patch.object(AssetsMediator, "hydrate_assets_from_model"), patch.object(
        AssetsMediator, "upload_all"
    ), patch.object(
        Deployment, "from_function_record"
    ), patch.object(
        Deployment, "attach_route_methods"
    ):

        yield


@pytest.mark.parametrize(
    "args, kwargs",
    [
        # x, y, ... (minimum args & kwargs)
        ((1, 2), {"k": 99.9}),
        # x, y, ... (everything except bar)
        ((1, 2), {"k": 99.9, "foo": "dog", "extra_kw1": "value-1", "extra_kw2": "value-2"}),
        # x, y, foo="dog", ...
        ((1, 2, "dog"), {"k": 99.9, "bar": "cat", "extra_kw1": "value-1", "extra_kw2": "value-2"}),
        # x, y, foo, *args
        (
            (1, 2, "dog", 4, 5, 6),
            {"k": 99.9, "bar": "cat", "extra_kw1": "value-1", "extra_kw2": "value-2"},
        ),
    ],
)
def test_deploy_signature_valid(args, kwargs):
    """All calls here should pass the signature check."""

    sample_func(*args, **kwargs)  # NOTE: test validation

    with mock_deploy_to_cloud():
        deploy(sample_service)(*args, **kwargs)


@pytest.mark.parametrize(
    "args, kwargs",
    [
        # x, y, ... (missing k)
        ((1, 2), {"foo": "dog"}),
        # x, y, ... (missing k)
        ((1, 2), {"foo": "dog", "extra_kw1": "value-1", "extra_kw2": "value-2"}),
        # x ... (missing y)
        ((1,), {"k": 99.9, "bar": "cat", "extra_kw1": "value-1", "extra_kw2": "value-2"}),
        # x, y, foo, *args
        ((1, 2, "dog"), {"bar": "cat", "extra_kw1": "value-1", "extra_kw2": "value-2"}),
        # totally wrong
        ((exec,), {"order": 66}),
        # empty
        ((), {}),
        # no kwargs  (missing k)
        ((1, 2, "dog", 4, 5, 6), {}),
        # x not positional-only
        ((2,), {"x": 1, "k": 99.9}),
    ],
)
def test_deploy_signature_invalid(args, kwargs):
    """All calls here should fail the signature check."""
    with pytest.raises(TypeError):
        sample_func(*args, **kwargs)  # NOTE: test validation

    with mock_deploy_to_cloud():
        with pytest.raises(TypeError):
            deploy(sample_service)(*args, **kwargs)
