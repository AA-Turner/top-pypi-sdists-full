import datetime
import json
from contextlib import suppress
from functools import partial
from typing import Any, Dict

import factory
from django.db import models
from django.forms.models import model_to_dict
from factory import Factory
from factory.base import StubObject
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.authentication.models import Token

from .signals import (
    custom_update_data_from_factory,
    custom_update_kwargs,
    get_custom_serializer,
)


def get_all_subclasses(klass):
    for subclass in klass.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


def get_model_factory(model):
    # mf = [cls for cls in factory.django.DjangoModelFactory.__subclasses__() if cls._meta.model == model]
    mfs = [cls for cls in all_subclasses(factory.django.DjangoModelFactory) if cls._meta.model == model]
    if is_empty(mfs) or model is None:
        return None
    else:
        mf = [mf for mf in mfs if (hasattr(mf, "__name__") and mf.__name__ == model.__name__ + "Factory")]
        if not is_empty(mf):
            return mf[0]
        else:
            return mfs[0]


def get_data_from_factory(instance, viewset, delete=False, update=False, superuser=None, factory=None):  # noqa: C901
    """
    Our goal here is to get the serializer dynamically based on the viewset, use this serializer to generate data for the post and update test.
    """
    obj_factory = instance
    if delete and factory:
        instance = factory()
    kwargs = getattr(viewset, "kwargs", {})
    kwargs["pk"] = instance.pk
    viewset.kwargs = kwargs
    mvs = viewset()

    request = APIRequestFactory().get("")
    if superuser:
        request.user = superuser
        request.parser_context = {"view": mvs}
        _request = request
    else:
        _request = Request(request)
    mvs.request = request
    """
        TODO
        request = mvs.initialize_request(request)
        object has no attribute 'action_map'
        action_map is filled according to the parameter given to as_view
        Need to find better approch
    """

    if delete:
        mvs.action = "create"
    elif update:
        mvs.action = "update"
    else:
        mvs.action = "list"
    my_serializer = mvs.get_serializer_class()
    if custom_serializer := get_custom_serializer.send(viewset):
        my_serializer = custom_serializer[0][1]
    my_model = my_serializer.Meta.model

    # fields_models = [m.name for m in my_model._meta.get_fields()]
    dict_fields_models = {}
    for m in my_model._meta.get_fields():
        dict_fields_models[m.name] = m
    data = {}
    for key, value in my_serializer(instance, context={"request": _request}).data.items():
        if key in dict_fields_models.keys() and key != "frontend_settings" and key != "id":
            if key == "auth_token":
                data[key], _ = Token.objects.get_or_create(user=instance)
            elif dict_fields_models[key].get_internal_type() in ["FileField", "ImageField"]:
                """
                # Create a sample test file on the fly
                fpath = "testfile.txt"
                f = open(fpath, "w")
                f.write("Hello World")
                f.close()
                data[key] = open(fpath, "r")
                data[key] = document.file.open(mode='rb')
                """
                pass  # data[key] = open(value.replace("http://testserver/",""), 'rb')
            elif isinstance(value, tuple):
                data[key] = f"{value[0]},{value[1]}"
            else:
                data[key] = value
            # Related objects with cascading on_delete will be deleted. we create a new related object and override the id of the deleted object
            if delete and (_field := dict_fields_models[key]):
                if (
                    _field.is_relation
                    and not _field.null
                    and _field.many_to_one
                    and (_related_fields := _field.related_fields)
                ):
                    with suppress(Exception):
                        lh_field, rh_field = _related_fields[0]
                        if isinstance(lh_field, models.fields.AutoField) or isinstance(
                            rh_field, models.fields.AutoField
                        ):
                            data[key] = get_model_factory(dict_fields_models[key].related_model).id
    if update or delete:
        _kwargs = {"user": superuser, "obj_factory": obj_factory}
        if delete:
            _kwargs.update({"obj_pre_deleted": instance})
        if custom_data := custom_update_data_from_factory.send(viewset, **_kwargs):
            data.update(custom_data[0][1])
    # delete object for create with post method
    if delete:
        my_model.objects.filter(pk=instance.pk).delete()
    data = {k: v for k, v in data.items() if v is not None}  # Filter out keys with `None` values
    return data


def get_kwargs(instance, viewset, request, data=None):
    """
    Get the kwargs needed for a ViewSet, handling related fields
    """
    viewset.kwargs = {"pk": instance.pk}  # set kwargs attribute to viewset
    kwargs = {"user": request.user, "profile": getattr(request.user, "profile", None), "obj_factory": instance}
    if isinstance(data, str):
        # Convert JSON string to dictionary if necessary
        data = json.loads(data)
    data = data or model_to_dict(instance)
    # Add related field IDs to kwargs
    for field in viewset.get_model()._meta.get_fields():
        if field.is_relation and field.many_to_one and (related_field_id := data.get(field.name)):
            kwargs[f"{field.name}_id"] = related_field_id

    # Add custom kwargs, if any, from signal handler
    if custom_kwargs := custom_update_kwargs.send(viewset, **kwargs):
        kwargs.update(custom_kwargs[0][1])
    return kwargs


def generate_dict_factory(factory: Factory):
    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)


# check if an element of a list is present in the other
def contains(lst1, lst2):
    return any(elt in lst1 for elt in lst2)


def is_intermediate_table_m2m(model):
    if "_" in model.__qualname__ and not is_empty(model._meta.unique_together):
        list_models = [elt.lower() for elt in model.__qualname__.split("_")]
        list_models_id = [elt.lower() + "_id" for elt in model.__qualname__.split("_")]
        if (
            contains(list_models, model._meta.unique_together[0])
            and contains(list_models, model.__dict__.keys())
            and contains(list_models_id, model.__dict__.keys())
        ):
            return True
    return False


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def get_factory_custom_user():
    list_models = [
        m
        for m in get_all_subclasses(models.Model)
        if m.__name__ == ("User")
        and not m.__module__.startswith(("wbcore", "django", "rest_framework", "dynamic_preferences", "eventtools"))
        and not m._meta.abstract
        and not is_intermediate_table_m2m(m)
    ]
    userfactory = [
        get_model_factory(modl) for modl in list(dict.fromkeys(list_models)) if get_model_factory(modl) is not None
    ]
    if not is_empty(userfactory):
        return userfactory[0]
    return None


def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f"{number:,.{decimal}{'%' if is_pourcent else 'f'}}"


# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable?page=1&tab=votes#tab-top
def datetime_converter(o):
    if isinstance(o, (datetime.date, datetime.datetime, datetime.time)):
        return o.isoformat()


def get_or_create_superuser():
    return UserFactory.create(is_active=True, is_superuser=True)
