"""Tests verifying module accessors return the same instance every time."""

from smplkit.client import AsyncSmplClient, SmplClient


class TestSingletonAccessorsSync:
    def test_config_is_same_instance(self):
        client = SmplClient(api_key="sk_test", environment="test")
        assert client.config is client.config

    def test_flags_is_same_instance(self):
        client = SmplClient(api_key="sk_test", environment="test")
        assert client.flags is client.flags

    def test_logging_is_same_instance(self):
        client = SmplClient(api_key="sk_test", environment="test")
        assert client.logging is client.logging


class TestSingletonAccessorsAsync:
    def test_config_is_same_instance(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test")
        assert client.config is client.config

    def test_flags_is_same_instance(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test")
        assert client.flags is client.flags

    def test_logging_is_same_instance(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test")
        assert client.logging is client.logging
