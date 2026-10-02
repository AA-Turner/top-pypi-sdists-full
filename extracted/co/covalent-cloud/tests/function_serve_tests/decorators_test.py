# Copyright 2024 Agnostiq Inc.

"""Unit tests for function serve decorators module."""

import pytest

import covalent_cloud as cc
from covalent_cloud.function_serve.decorators import service
from covalent_cloud.shared.classes.exceptions import InsufficientMemoryError
from covalent_cloud.shared.classes.settings import settings


def test_insufficient_memory_error():
    """Test insufficient memory error."""

    insufficient_memory = (settings.function_serve.min_executor_memory_gb - 1) * 1024
    executor = cc.CloudExecutor(
        num_cpus=4, memory=insufficient_memory, env="default", validate_environment=False
    )

    with pytest.raises(InsufficientMemoryError):
        service(executor=executor)
