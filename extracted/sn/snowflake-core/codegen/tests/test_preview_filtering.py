"""Integration tests for preview feature filtering."""

import pytest
from datetime import datetime


class TestGAEndpoints:
    def test_ga_endpoints_exist(self, default_api_class):
        assert hasattr(default_api_class, "get_resource")
        assert hasattr(default_api_class, "create_resource")
        assert hasattr(default_api_class, "get_resource_advanced")

        assert callable(getattr(default_api_class, "get_resource"))
        assert callable(getattr(default_api_class, "create_resource"))
        assert callable(getattr(default_api_class, "get_resource_advanced"))


class TestPreviewEndpoints:
    def test_preview_endpoints_not_exist(self, default_api_class):
        assert not hasattr(default_api_class, "get_preview_feature")
        assert not hasattr(default_api_class, "create_experimental_feature")
        assert not hasattr(default_api_class, "get_experimental_shared")
        assert not hasattr(default_api_class, "create_composed_preview")


class TestGAModels:
    def test_ga_models_exist(self, models_module):
        assert hasattr(models_module, "Resource")
        assert hasattr(models_module, "CreateResourceRequest")
        assert hasattr(models_module, "SharedModel")


class TestPreviewModels:
    def test_preview_models_not_exist(self, models_module):
        assert not hasattr(models_module, "PreviewFeatureResponse")
        assert not hasattr(models_module, "ExperimentalRequest")
        assert not hasattr(models_module, "ExperimentalResponse")

    def test_nested_preview_models_not_exist(self, models_module):
        assert not hasattr(models_module, "NestedPreviewModel")
        assert not hasattr(models_module, "DeeplyNestedPreviewModel")

    def test_allof_preview_models_not_exist(self, models_module):
        assert not hasattr(models_module, "ComposedPreviewRequest")
        assert not hasattr(models_module, "ComposedPreviewResponse")
        assert not hasattr(models_module, "PreviewBaseModel")
        assert not hasattr(models_module, "AnotherPreviewBase")


class TestModelFunctionality:
    def test_create_resource_request(self, models_module):
        CreateResourceRequest = models_module.CreateResourceRequest

        request = CreateResourceRequest(name="my_resource")
        assert request.name == "my_resource"
        assert request.description is None

        request_full = CreateResourceRequest(name="my_resource", description="Test resource")
        assert request_full.name == "my_resource"
        assert request_full.description == "Test resource"

    def test_resource_model(self, models_module):
        Resource = models_module.Resource

        resource = Resource(name="test_db", status="active", created_at="2024-01-01T00:00:00Z")

        assert resource.name == "test_db"
        assert resource.status == "active"
        assert isinstance(resource.created_at, datetime)
        assert resource.created_at.year == 2024
        assert resource.created_at.month == 1
        assert resource.created_at.day == 1

    def test_shared_model(self, models_module):
        SharedModel = models_module.SharedModel

        model = SharedModel(shared_field="test_value")
        assert model.shared_field == "test_value"
