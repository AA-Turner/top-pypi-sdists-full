import random

import pytest

from wbcore import serializers as wb_serializers
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import (
    ActionButton,
    DropDownButton,
    HyperlinkButton,
    WidgetButton,
)
from wbcore.metadata.configs.buttons.enums import ButtonDefaultColor
from wbcore.metadata.configs.display.instance_display import create_simple_display
from wbcore.metadata.utils import prefix_key


class TestDropDownButton:
    @pytest.fixture()
    def button(self):
        return DropDownButton(
            icon=random.choice(list(WBIcon)).icon,
            title="Foo Bar",
            color=random.choice(list(ButtonDefaultColor)).value,
            buttons=[WidgetButton(key="Foo", label="Foo Bar")],
        )

    def test_serialize(self, rf, button):
        serialized_btn = button.serialize(rf)
        assert serialized_btn["icon"] == button.icon
        assert serialized_btn["title"] == button.title
        assert serialized_btn["color"] == button.color
        assert serialized_btn["buttons"] == [button.buttons[0].serialize(rf)]
        assert serialized_btn["type"] == DropDownButton.button_type.value

    @pytest.mark.parametrize("key_prefix", ["Foo"])
    def test_serialize_with_prefix(self, rf, button, key_prefix):
        serialized_btn = button.serialize(rf, key_prefix=key_prefix)
        nested_button = button.buttons[0]

        assert serialized_btn["icon"] == button.icon
        assert serialized_btn["title"] == button.title
        assert serialized_btn["color"] == button.color
        assert serialized_btn["buttons"] == [nested_button.serialize(rf, key_prefix=key_prefix)]
        assert serialized_btn["type"] == DropDownButton.button_type.value
        assert serialized_btn["buttons"][0]["key"] == prefix_key(nested_button.key, key_prefix)

    def test_hash(self, button):
        assert hash(button) == hash(button.title)


class TestWidgetButton:
    button_class = WidgetButton

    @pytest.fixture()
    def key_button(self):
        return self.button_class(
            icon=random.choice(list(WBIcon)).icon,
            title="Foo Bar",
            color=random.choice(list(ButtonDefaultColor)).value,
            key="Foo",
        )

    @pytest.fixture()
    def endpoint_button(self):
        return self.button_class(
            icon=random.choice(list(WBIcon)).icon,
            title="Foo Bar",
            color=random.choice(list(ButtonDefaultColor)).value,
            endpoint="www.foo.com",
        )

    def test_serialize(self, rf, key_button):
        serialized_btn = key_button.serialize(rf)
        assert serialized_btn["icon"] == key_button.icon
        assert serialized_btn["title"] == key_button.title
        assert serialized_btn["color"] == key_button.color
        assert serialized_btn["key"] == key_button.key
        assert serialized_btn["type"] == self.button_class.button_type.value

    @pytest.mark.parametrize("key_prefix", ["Foo"])
    def test_serialize_with_prefix(self, rf, key_button, key_prefix):
        serialized_btn = key_button.serialize(rf, key_prefix=key_prefix)

        assert serialized_btn["icon"] == key_button.icon
        assert serialized_btn["title"] == key_button.title
        assert serialized_btn["color"] == key_button.color
        assert serialized_btn["type"] == self.button_class.button_type.value
        assert serialized_btn["key"] == prefix_key(key_button.key, key_prefix)

    def test_key_hash(self, key_button):
        assert hash(key_button) == hash(key_button.key)

    def test_endpoint_hash(self, endpoint_button):
        assert hash(endpoint_button) == hash(endpoint_button.endpoint)

    def test_serialize_endpoint_button(self, rf, endpoint_button):
        serialized_btn = endpoint_button.serialize(rf)
        assert serialized_btn["icon"] == endpoint_button.icon
        assert serialized_btn["title"] == endpoint_button.title
        assert serialized_btn["color"] == endpoint_button.color
        assert serialized_btn["endpoint"] == endpoint_button.endpoint
        assert serialized_btn["type"] == self.button_class.button_type.value

        base_endpoint = endpoint_button.endpoint
        endpoint_button.new_mode = True
        serialized_btn = endpoint_button.serialize(rf)
        assert serialized_btn["endpoint"] == base_endpoint + "?new_mode=true"
        assert serialized_btn["new_mode"] is True


class TestHyperlinkButtonutton(TestWidgetButton):
    button_class = HyperlinkButton

    def test_serialize_endpoint_button(self, rf, endpoint_button):
        serialized_btn = endpoint_button.serialize(rf)
        assert serialized_btn["icon"] == endpoint_button.icon
        assert serialized_btn["title"] == endpoint_button.title
        assert serialized_btn["color"] == endpoint_button.color
        assert serialized_btn["endpoint"] == endpoint_button.endpoint
        assert serialized_btn["type"] == self.button_class.button_type.value

        # No new mode supported for hyperlink


class TestActionButtonButton(TestHyperlinkButtonutton):
    button_class = ActionButton

    @pytest.fixture()
    def key_button(self):
        class BaseSerializer(wb_serializers.Serializer):
            field = wb_serializers.CharField()

            class Meta:
                fields = ("field",)

        return ActionButton(
            icon=random.choice(list(WBIcon)).icon,
            title="Foo Bar",
            color=random.choice(list(ButtonDefaultColor)).value,
            key="Foo",
            method=random.choice(list(RequestType)),
            action_label="Foo",
            description_fields="Foo Bar",
            instance_display=create_simple_display([["field"]]),
            serializer=BaseSerializer,
            identifiers=("Foo",),
        )

    def test_serialize(self, rf, key_button):
        TestWidgetButton.test_serialize(self, rf, key_button)
        serialized_btn = key_button.serialize(rf)

        assert serialized_btn["action_label"] == key_button.action_label
        assert serialized_btn["method"] == key_button.method.value
        assert serialized_btn["description_fields"] == key_button.description_fields
        assert serialized_btn["confirm_config"] == key_button.confirm_config.serialize(rf)
        assert serialized_btn["cancel_config"] == key_button.cancel_config.serialize(rf)
        assert serialized_btn["identifiers"] == key_button.identifiers
        assert serialized_btn["instance_display"] == key_button.instance_display.serialize()
        assert (
            serialized_btn["fields"]["field"]
            == key_button.serializer().fields["field"].get_representation(rf, "field")[1]
        )
