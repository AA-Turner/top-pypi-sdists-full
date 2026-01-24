import logging
from inspect import getmembers

from rest_framework import serializers
from rest_framework.reverse import reverse

from wbcore.metadata.utils import prefix_key
from wbcore.signals import (
    add_additional_resource,
    add_dynamic_button,
    add_instance_additional_resource,
)
from wbcore.utils.importlib import parse_signal_received_for_module

from .mixins import WBCoreSerializerFieldMixin
from .text import StringRelatedField
from .types import WBCoreType

logger = logging.getLogger(__name__)


def register_resource():
    def decorator(func):
        func._is_additional_resource = True
        return func

    return decorator


def register_only_instance_resource():
    def decorator(func):
        func._is_instance_additional_resource = True
        return func

    return decorator


def _is_additional_resource(attr):
    return hasattr(attr, "_is_additional_resource")


def _is_instance_additional_resource(attr):
    return hasattr(attr, "_is_instance_additional_resource")


def register_dynamic_button():
    def decorator(func):
        func._is_dynamic_button = True
        return func

    return decorator


def register_only_instance_dynamic_button():
    def decorator(func):
        func._is_instance_dynamic_button = True
        return func

    return decorator


def _is_dynamic_button(attr):
    return hasattr(attr, "_is_dynamic_button")


def _is_instance_dynamic_button(attr):
    return hasattr(attr, "_is_instance_dynamic_button")


class DynamicButtonField(WBCoreSerializerFieldMixin, serializers.ReadOnlyField):
    field_type = "_dynamic_buttons"

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        buttons = list()
        if request := self.parent.context.get("request"):
            for _, button_func in getmembers(self.parent.__class__, _is_dynamic_button):
                btns = button_func(self.parent, instance=value, request=request, user=request.user)
                buttons.extend([btn.serialize(request) for btn in btns])
            dynamic_buttons = parse_signal_received_for_module(
                add_dynamic_button.send(
                    sender=self.parent.__class__,
                    serializer=self.parent,
                    instance=value,
                    request=request,
                    user=request.user,
                    view=self.parent.context.get("view", None),
                )
            )
            for prefix, btns in dynamic_buttons:
                for btn in btns:
                    btn.prefix_key = prefix
                    buttons.append(btn.serialize(request))
            if (view := self.parent.context.get("view", None)) and not (getattr(view, "action", "list") == "list"):
                for _, button_func in getmembers(self.parent.__class__, _is_instance_dynamic_button):
                    btns = button_func(self.parent, instance=value, request=request, user=request.user)
                    buttons.extend([btn.serialize(request) for btn in btns])

        return buttons


class AdditionalResourcesField(WBCoreSerializerFieldMixin, serializers.ReadOnlyField):
    field_type = "_additional_resources"

    def get_attribute(self, instance):
        return instance

    @property
    def serializer_class_for_remote_additional_resources(self):
        return getattr(self.parent, "SERIALIZER_CLASS_FOR_REMOTE_ADDITIONAL_RESOURCES", self.parent.__class__)

    def to_representation(self, value):
        resources = dict()
        if (request := self.parent.context.get("request")) and (view := self.parent.context.get("view", None)):
            for _, function in getmembers(self.parent.__class__, _is_additional_resource):
                _d = function(self.parent, instance=value, request=request, user=request.user)
                resources.update(_d)

            is_list = getattr(view, "action", "list") == "list"
            remote_resources = parse_signal_received_for_module(
                add_additional_resource.send(
                    sender=self.serializer_class_for_remote_additional_resources,
                    serializer=self.parent,
                    instance=value,
                    request=request,
                    user=request.user,
                    view=view,
                    is_list=is_list,
                )
            )
            for prefix, response in remote_resources:
                for key, remote_resource in response.items():
                    resources[prefix_key(key, prefix)] = remote_resource
            if not is_list:
                for _, function in getmembers(self.parent.__class__, _is_instance_additional_resource):
                    _d = function(self.parent, instance=value, request=request, user=request.user, view=view)
                    resources.update(_d)
                remote_resources = parse_signal_received_for_module(
                    add_instance_additional_resource.send(
                        sender=self.serializer_class_for_remote_additional_resources,
                        serializer=self.parent,
                        instance=value,
                        request=request,
                        user=request.user,
                        view=view,
                        is_list=False,
                    )
                )
                for prefix, response in remote_resources:
                    for key, remote_resource in response.items():
                        resources[prefix_key(key, prefix)] = remote_resource
        return resources


class HyperlinkField(WBCoreSerializerFieldMixin, serializers.ReadOnlyField):
    field_type = WBCoreType.HYPERLINK.value

    def __init__(self, *args, **kwargs):
        self.reverse_name = kwargs.pop("reverse_name")
        self.id_field_name = kwargs.pop("id_field_name", "id")
        super().__init__(*args, **kwargs)

    def get_attribute(self, obj):
        request = self.context.get("request", None)
        if obj:
            obj_id = getattr(obj, self.id_field_name, obj.pk)
            if request:
                return reverse(self.reverse_name, args=[obj_id], request=request)
            return reverse(self.reverse_name, args=[obj_id])


class ReadOnlyField(WBCoreSerializerFieldMixin, serializers.ReadOnlyField):
    field_type = WBCoreType.TEXT.value


class SlugRelatedField(WBCoreSerializerFieldMixin, serializers.SlugRelatedField):
    field_type = WBCoreType.TEXT.value


class SerializerMethodField(WBCoreSerializerFieldMixin, serializers.SerializerMethodField):
    def __init__(self, method_name=None, field_class=StringRelatedField, percent=None, **kwargs):
        self.field_class = field_class
        self.initkwargs = kwargs.copy()
        if percent:
            self.initkwargs["percent"] = percent
        super().__init__(method_name, **kwargs)

    def get_representation(self, request, field_name):
        field_name, rep = super().get_representation(request, field_name)
        field_name, field_rep = self.field_class(**self.initkwargs).get_representation(request, field_name)

        rep.update(field_rep)
        return field_name, rep
