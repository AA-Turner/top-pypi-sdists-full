from typing import Iterable

from django.contrib.messages import get_messages
from django.contrib.staticfiles import finders
from django.db import IntegrityError
from django.db.models import F, Model, QuerySet
from django.db.models.expressions import OrderBy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.utils.functional import cached_property
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin as OriginalCreateModelMixin
from rest_framework.mixins import DestroyModelMixin as OriginalDestroyModelMixin
from rest_framework.mixins import ListModelMixin as OriginalListModelMixin
from rest_framework.mixins import RetrieveModelMixin as OriginalRetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin as OriginalUpdateModelMixin
from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_409_CONFLICT,
)

from wbcore.filters import DjangoFilterBackend
from wbcore.messages import InMemoryMessageStorage


def map_ordering(order_str: str) -> OrderBy:
    asc_desc = "desc" if order_str[0] == "-" else "asc"
    remove_strings = ["-", "__nulls_last", "__nulls_first"]
    clean_order_str = order_str
    for string in remove_strings:
        clean_order_str = clean_order_str.replace(string, "")
    asc_desc_function = getattr(F(clean_order_str), asc_desc)
    if "__nulls_last" in order_str:
        return asc_desc_function(nulls_last=True)
    elif "__nulls_first" in order_str:
        return asc_desc_function(nulls_first=True)
    return asc_desc_function()


class WBCoreOrderingFilter(OrderingFilter):
    def get_mandatory_ordering_fields(self, queryset, view) -> list[str]:
        """
        Given the queryset and the view, extract the mandatory field for the final ordering. Default to ["id"]

        To keep it simple, we assume that all view have a id field defined in the serializer. If this is not the case, we expect the dev to override this method and return an empty list.
        """
        if (fct := getattr(view, "get_mandatory_ordering_fields", None)) and callable(fct):
            fields = fct()
        else:
            fields = ["id"]
        return fields

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        mandatory_ordering_fields = self.get_mandatory_ordering_fields(queryset, view)
        if ordering or mandatory_ordering_fields:
            return queryset.order_by(*map(map_ordering, ordering), *mandatory_ordering_fields)

        return queryset

    def get_valid_fields(self, queryset, view, context: dict | None = None):
        if context is None:
            context = {}
        valid_fields = view.get_ordering_fields()
        if valid_fields is None:
            # Default to allowing filtering on serializer fields
            return self.get_default_valid_fields(queryset, view, context)

        elif valid_fields == "__all__":
            # View explicitly allows filtering on any model field
            valid_fields = [(field.name, field.verbose_name) for field in queryset.model._meta.fields]
            valid_fields += [(key, key.title().split("__")) for key in queryset.query.annotations]
        else:
            valid_fields = [(item, item) if isinstance(item, str) else item for item in valid_fields]
        return valid_fields


class FilterMixin:
    filter_backends = (DjangoFilterBackend, SearchFilter, WBCoreOrderingFilter)
    filterset_fields = {}
    search_fields = []
    ordering_fields = ordering = ("id",)


class DocumentationMixin:
    def _get_documentation_url(self, detail):
        instance_documentation = getattr(self, "INSTANCE_DOCUMENTATION", None)
        list_documentation = getattr(self, "LIST_DOCUMENTATION", None)
        doc = instance_documentation if detail else list_documentation

        if doc and finders.find(doc):
            return static(doc)
        return None


class ActionMixin:
    kwargs: dict
    request: Request
    action: str

    def get_action(self) -> str:
        if self.action == "metadata":
            if bool(self.request.GET.get("new_mode")):
                return "create-metadata"
            if bool(self.kwargs.get("pk")):
                return "retrieve-metadata"
            else:
                return "list-metadata"
        return self.action


class MessageMixin:
    def add_messages(
        self,
        request: Request,
        queryset: QuerySet | None = None,
        paginated_queryset: BasePagination | None = None,
        instance: Model | None = None,
        initial: bool = False,
    ): ...

    def _get_messages(
        self,
        request: Request,
        queryset: QuerySet | None = None,
        paginated_queryset: BasePagination | None = None,
        instance: Model | None = None,
        initial: bool = False,
    ) -> Iterable[dict[str, str]]:
        # We call add_messages to collect messages from the view which weren't created at other places
        # because they might need some more information under which circumstances they are being called
        self.add_messages(
            request=request,
            queryset=queryset,
            paginated_queryset=paginated_queryset,
            instance=instance,
            initial=initial,
        )

        # We get the storage backend and yield all messages in a serialized form
        # This only works if the storage backend is our custom InMemoryMessageStorage
        # We inject request._request purely for typing, as request will defer attribute
        # lookup to its internal getattribute method. But the get_messages method only
        # accepts a HttpRequest object which is DRF request simply wraps
        storage = get_messages(request._request)
        if isinstance(storage, InMemoryMessageStorage):
            yield from storage.serialize_messages()


class ListModelMixin(MessageMixin, OriginalListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["messages"] = list(
                self._get_messages(
                    request, queryset=queryset, paginated_queryset=page, initial=self._paginator.is_initial()
                )
            )

            if hasattr(self, "get_aggregates"):
                response.data["aggregates"] = self.get_aggregates(queryset=queryset, paginated_queryset=page)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
            response.data = {"results": response.data}

            response.data["messages"] = list(self._get_messages(request, queryset=queryset, initial=True))

            if hasattr(self, "get_aggregates"):
                response.data["aggregates"] = self.get_aggregates(queryset=queryset, paginated_queryset=queryset)

        return response


class RetrieveModelMixin(MessageMixin, OriginalRetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        # TODO Check if this is necessary but will trigger a lot of loic's test error
        # if self.endpoint_config_class(view=self, request=self.request, instance=True)._get_instance_endpoint() is None:
        #     return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        response = super().retrieve(request, *args, **kwargs)
        response.data = {"instance": response.data}
        try:
            instance = self.get_object()
        except Http404:
            instance = None
        response.data["messages"] = list(self._get_messages(request, instance=instance))
        return response


class CreateModelMixin(OriginalCreateModelMixin):
    def create(self, request, *args, **kwargs):
        # If not create endpoint is defined then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=False)._get_create_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        response = super().create(request, *args, **kwargs)
        response.data = {"instance": response.data, "messages": list(self._get_messages(request))}
        return response


class UpdateModelMixin(OriginalUpdateModelMixin):
    def update(self, request, *args, **kwargs):
        # If no instance endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=True)._get_update_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        response = super().update(request, *args, **kwargs)
        response.data = {"instance": response.data}
        try:
            instance = self.get_object()
        except Http404:
            instance = None
        response.data["messages"] = list(self._get_messages(request, instance=instance))
        return response


class DestroyModelMixin(OriginalDestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        # If no delete endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=True)._get_delete_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class DestroyMultipleModelMixin:
    def destroy_multiple(self, request, *args, **kwargs):
        # If no delete endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=False)._get_delete_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        model = self.get_serializer_class().Meta.model
        app_label = model._meta.app_label

        queryset = model.objects.filter(id__in=request.data)
        destroyed = self.perform_destroy_multiple(queryset)
        return Response({"count": destroyed[1].get(f"{app_label}.{model.__name__}", 0)}, status=HTTP_204_NO_CONTENT)

    def perform_destroy_multiple(self, queryset):
        return queryset.delete()


class OrderableMixin:
    # This mixin will not work if the viewset model does not inherit from ordered_model.models.OrderedModel

    ordering = ("order",)

    @action(methods=["PATCH"], detail=True)
    def reorder(self, request: Request, pk=None, **kwargs) -> Response:
        instance = self.get_object()
        order = request.data.get("order")
        if order is None:
            return Response("No order received", status=HTTP_400_BAD_REQUEST)
        instance.to(int(order))
        return Response("Reordering Successful", status=HTTP_200_OK)


class ReparentMixin:
    PARENT_FIELD: str
    PARENT_MODEL: type[Model]

    @property
    def parent_field(self) -> str:
        return self.PARENT_FIELD

    @cached_property
    def model(self):
        return self.queryset.model

    @action(methods=["PATCH"], detail=True)
    def reparent(self, request: Request, pk=None, **kwargs) -> Response:
        instance = self.get_object()
        new_parent = get_object_or_404(self.PARENT_MODEL, pk=request.data.get("new_parent"))
        old_parent = getattr(instance, self.parent_field)
        if old_parent != new_parent:
            setattr(instance, self.parent_field, new_parent)
            try:
                instance.save()
            except IntegrityError:
                return Response("Cannot reparent due to conflict", status=HTTP_409_CONFLICT)
        return Response("Reparenting Successful", status=HTTP_200_OK)
