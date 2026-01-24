import importlib
import re
from contextlib import suppress
from functools import cached_property

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializer
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.display.instance_display import Display
from wbcore.metadata.configs.display.instance_display.shortcuts import (
    create_simple_display,
)
from wbcore.signals.instance_buttons import add_extra_button
from wbcore.utils.models import MergeMixin as ModelMergeMixin
from wbcore.utils.models import merge_as_task


def parse_query_parameters_list(list_str):
    try:
        return list(set(map(lambda x: int(x), filter(None, list_str.split(",")))))
    except ValueError:
        return ""


def set_identifier(identifier):
    def decorator(func):
        func.identifier = identifier
        return func

    return decorator


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_endpoints_root(request, format=None):
    try:
        endpoints = dict()
        for wb_endpoint in settings.WB_ENDPOINTS:
            try:
                endpoints[wb_endpoint] = reverse(f"{wb_endpoint}:api-root", request=request, format=format)
            except NoReverseMatch:
                pass

        return Response(endpoints)

    except AttributeError:
        return Response({"error": "No Endpoints specified."}, status=status.HTTP_400_BAD_REQUEST)


class CloneMixin:
    """
    This Mixin can be used to inherit the clone functionality out of the box. This mixin will register the additional resources
    and the appropriate button to allow user to clone a given instance
    """

    def get_clone_button_serializer_class(self, instance):
        return self.get_serializer_class()

    def get_clone_button_instance_display(self) -> Display | None:
        """
        Return the instance display to show in the clone action button. Default to return None (i.e. No form)
        """
        return None

    @action(methods=["PATCH"], detail=True)
    def clone(self, request, pk=None):
        instance = get_object_or_404(self.queryset.model, pk=pk)
        if (clone_fct := getattr(instance, "clone", None)) and callable(clone_fct):
            kwargs = {}
            if request.data:
                serializer = self.get_clone_button_serializer_class(instance)(data=request.data)
                serializer.is_valid(raise_exception=False)
                kwargs = serializer.data
            cloned_obj = clone_fct(user=request.user, **kwargs)
            if (
                cloned_obj
                and (clone_id := getattr(cloned_obj, "id", None))
                and (endpoint_config_class := getattr(self, "endpoint_config_class", None))
            ):
                endpoint_config = endpoint_config_class(self, request, cloned_obj)
                if endpoint := endpoint_config.get_instance_endpoint():
                    return Response(
                        {
                            "endpoint": re.sub(
                                pattern=r"[^\/]+(?=\/$|$)",
                                repl=str(clone_id),
                                string=endpoint,
                            )
                        }
                    )
        return Response({})


@receiver(add_extra_button)
def add_clone_extra_button(sender, instance, request, view, pk=None, **kwargs):
    if instance and pk and issubclass(view.__class__, CloneMixin):
        object = view.get_object()
        if getattr(object, "is_cloneable", True) and (endpoint_basename := object.get_endpoint_basename()):
            endpoint = reverse(f"{endpoint_basename}-clone", args=[pk], request=request)
            identifier = getattr(view, "IDENTIFIER", "{0.app_label}:{0.model}".format(view.get_content_type()))
            return bt.ActionButton(
                method=RequestType.PATCH,
                identifiers=(identifier,),
                endpoint=endpoint,
                action_label=_("Clone"),
                title=_("Clone"),
                label=_("Clone"),
                description_fields=_('<strong>Clone {}</strong> "{}"').format(object._meta.verbose_name, object),
                icon=WBIcon.COPY.icon,
                serializer=view.get_clone_button_serializer_class(object),
                instance_display=view.get_clone_button_instance_display(),
            )


class MergeMixin:
    """
    This Mixin can be used to inherit the clone functionality out of the box. This mixin will register the additional resources
    and the appropriate button to allow user to merge a given instance
    """

    @cached_property
    def model(self):
        return self.queryset.model

    def has_merge_permission(self, user) -> bool:
        return user.has_perm(f"administrate_{self.model._meta.model_name}")

    def get_merged_object_representation_serializer(self):
        """
        Return the representation serializer used for the action button merged object field. Default to the model representation endpoint serializer
        """
        view_func = resolve(reverse(self.model.get_representation_endpoint())).func
        module = importlib.import_module(view_func.__module__)
        view = getattr(module, view_func.__name__)
        return view.serializer_class

    def get_merged_object_representation_serializer_filter_params(self) -> dict[str, str]:
        """
        Return the representation serializer filter kwargs. Default to an empty dict
        """
        return dict()

    def add_extra_buttons(self, request):
        if self.has_merge_permission(request.user) and (pk := self.kwargs.get("pk")):
            object = self.get_object()
            if (
                isinstance(object, ModelMergeMixin)
                and object.is_mergeable
                and (endpoint_basename := object.get_endpoint_basename())
            ):
                endpoint = reverse(f"{endpoint_basename}-merge", args=[pk], request=request)

                class MergeSerializer(wb_serializer.ModelSerializer):
                    merged_object = wb_serializer.PrimaryKeyRelatedField(
                        queryset=self.model.objects.all(), label="Merged with"
                    )
                    _merged_object = self.get_merged_object_representation_serializer()(
                        source="merged_object",
                        filter_params=self.get_merged_object_representation_serializer_filter_params(),
                    )

                    class Meta:
                        model = self.model
                        fields = [
                            "id",
                            "merged_object",
                            "_merged_object",
                        ]

                return {
                    bt.ActionButton(
                        method=RequestType.PATCH,
                        endpoint=endpoint,
                        action_label=_("Merge"),
                        title=_("Merge"),
                        label=_("Merge"),
                        icon=WBIcon.MERGE.icon,
                        serializer=MergeSerializer,
                        instance_display=create_simple_display([["merged_object"]]),
                    ),
                }

    @action(methods=["PATCH"], detail=True)
    def merge(self, request, pk=None):
        if self.has_merge_permission(request.user):
            if pk and hasattr(self.model, "merge"):
                instance = get_object_or_404(self.queryset.model, pk=pk)
                merged_instance = get_object_or_404(self.queryset.model, pk=request.POST.get("merged_object", None))
                with suppress(ContentType.DoesNotExist):
                    content_type = ContentType.objects.get_for_model(self.model)
                    merge_as_task.delay(content_type.id, instance.id, merged_instance.id)
                    return Response({"status": "Merged ongoing"})
            return Response({}, status=400)
        return Response({"_detail": "User does not have the permission to merge"}, status=status.HTTP_403_FORBIDDEN)
