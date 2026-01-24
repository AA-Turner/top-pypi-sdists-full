import json
from typing import Callable

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from termcolor import colored

from wbcore.messages import InMemoryMessageStorage
from wbcore.signals import add_additional_resource

from .signals import get_custom_factory
from .utils import (
    get_data_from_factory,
    get_kwargs,
    get_model_factory,
    get_or_create_superuser,
)


class TestModel:
    def __init__(self, _model):
        self.model = _model
        self.factory = get_model_factory(self.model)

    def _raise_warning(self, name_test):
        model_name = self.model.__name__ if self.model else None
        print(  # noqa: T201
            f"- {self.__class__.__name__}:{name_test}",
            colored(
                f"WARNING - {model_name} has no attribute {name_test}",
                "yellow",
            ),
        )

    def _successful_test(self, name_test):
        print(f"- {self.__class__.__name__}:{name_test}", colored("PASSED", "green"))  # noqa: T201

    def test_endpoint_basename(self):
        if not hasattr(self.model, "get_endpoint_basename"):
            self._raise_warning("get_endpoint_basename")
        else:
            assert isinstance(self.model.get_endpoint_basename, Callable), "endpoint basename should be Callable"
            assert reverse(
                f"{self.model.get_endpoint_basename()}-list", request=APIRequestFactory().get("")
            ), "endpoint basename should not be None"
            self._successful_test("test_endpoint_basename")

    def test_representation_endpoint(self):
        if not hasattr(self.model, "get_representation_endpoint"):
            self._raise_warning("get_representation_endpoint")
        else:
            assert isinstance(
                self.model.get_representation_endpoint, Callable
            ), "representation endpoint should be Callable"
            if not self.model.get_representation_endpoint():
                print(  # noqa: T201
                    f"- {self.__class__.__name__}:get_representation_endpoint",
                    colored("ERROR - representation_value_endpoint should not be None. ", "red"),
                    colored("WARNING - representation_value_endpoint should not be None", "yellow"),
                )
            else:
                assert reverse(
                    f"{self.model.get_representation_endpoint()}", request=APIRequestFactory().get("")
                ), "representation endpoint should not be None"
                self._successful_test("test_representation_endpoint")

    def test_representation_value_key(self):
        if not hasattr(self.model, "get_representation_value_key"):
            self._raise_warning("get_representation_value_key")
        else:
            assert self.model.get_representation_value_key(), "representation_value_key should not be None"
            self._successful_test("test_representation_value_key")

    def test_representation_label_key(self):
        if not hasattr(self.model, "get_representation_label_key"):
            self._raise_warning("get_representation_label_key")
        else:
            assert self.model.get_representation_label_key(), "representation_label_key should not be None"
            self._successful_test("test_representation_label_key")

    def test_str(self):
        if self.factory is None:
            print(  # noqa: T201
                f"- {self.__class__.__name__}:test_str",
                colored(f"WARNING - factory not found for {self.model.__name__ if self.model else None}", "yellow"),
            )
        else:
            obj = self.factory()
            assert str(obj), "str() function should return a string"
            assert isinstance(str(obj), str), "str() function should return a string"
            self._successful_test("test_str")

    def execute_test(self):
        print("\n")  # noqa: T201
        self.test_endpoint_basename()
        self.test_representation_endpoint()
        self.test_representation_value_key()
        self.test_representation_label_key()
        self.test_str()


class TestSerializer:
    def __init__(self, _serializer):
        self.serializer = _serializer
        self.factory = get_model_factory(self.serializer.Meta.model) if self.serializer else None

    def test_serializer(self):
        if self.factory is None:
            print(  # noqa: T201
                f"\n- {self.__class__.__name__}:test_serializer: {self.serializer.__name__ if self.serializer else None}",
                colored(
                    "WARNING - factory not found for " + self.serializer.Meta.model.__name__
                    if self.serializer
                    else None,
                    "yellow",
                ),
            )
        else:
            request = APIRequestFactory().get("")
            request.user = get_or_create_superuser()
            request.parser_context = {}
            serializer = self.serializer(self.factory(), context={"request": request})
            assert serializer.data, str(serializer.data) + " should not be empty"
            print(  # noqa: T201
                f"\n- {self.__class__.__name__}:test_serializer {self.serializer.__name__ if self.serializer else None}",
                colored("PASSED", "green"),
            )

    def test_additional_resources(self):
        if self.factory is None:
            print(  # noqa: T201
                f"\n- {self.__class__.__name__}:test_serializer: {self.serializer.__name__ if self.serializer else None}",
                colored(
                    "WARNING - factory not found for " + self.serializer.Meta.model.__name__
                    if self.serializer
                    else None,
                    "yellow",
                ),
            )
        else:
            request = APIRequestFactory().get("")
            request.user = get_or_create_superuser()
            request.parser_context = {}
            instance = self.factory()
            self.serializer(instance, context={"request": request})
            add_additional_resource.send(
                sender=self.serializer.__class__,
                serializer=self.serializer,
                instance=instance,
                request=request,
                user=request.user,
            )
            # TODO

    def execute_test(self):
        self.test_serializer()
        # self.test_additional_resources()


class ParentViewset:
    def __init__(self, mvs, factory=None):
        self.mvs = mvs
        request = request = APIRequestFactory().get("")
        request.user = get_or_create_superuser()
        # self.model = mvs(kwargs=dict(), request=request).get_serializer_class().Meta.model if mvs else None
        self.model = mvs.get_model() if mvs else None
        self.factory = (
            factory
            if factory
            else custom_factory[0][1]
            if (custom_factory := get_custom_factory.send(self.mvs))
            else get_model_factory(self.model)
        )

    def _get_mixins_data(self, type="GET", dump_data=False, data=None):  # noqa: C901
        api_request = APIRequestFactory()
        superuser = get_or_create_superuser()
        kwargs = None
        obj = superuser if self.factory._meta.model.__name__ == "User" else self.factory()
        if type == "GET":
            request = api_request.get("")
        elif type == "OPTIONS":
            request = api_request.options("")
        elif type == "DELETE":
            request = api_request.delete("")
        elif type == "POST":
            if not data:
                data = get_data_from_factory(obj, self.mvs, superuser=superuser, delete=True, factory=self.factory)
            if dump_data:
                data = json.dumps(data)
                request = api_request.post("", data=data, content_type="application/json")
            else:
                try:
                    request = api_request.post("", data)
                except Exception:
                    try:
                        request = api_request.post("", data, format="json")
                    except TypeError:
                        try:
                            data = json.dumps(data)
                            request = api_request.post("", data=data, content_type="application/json")
                        except TypeError as e:
                            raise e
            request.user = superuser
            kwargs = get_kwargs(obj, self.mvs, request=request, data=data)
        else:  # "UPDATE", "PATCH"
            if not data:
                data = get_data_from_factory(obj, self.mvs, superuser=superuser, update=True)
            if type == "UPDATE":
                try:
                    request = api_request.put("", data)
                except Exception:
                    try:
                        request = api_request.put("", data, format="json")
                    except TypeError as e:
                        raise e
                if dump_data:
                    data = json.dumps(data)
                    request = api_request.put("", data=data, content_type="application/json")
            else:  # PATCH
                try:
                    request = api_request.patch("", data)
                except Exception:
                    try:
                        request = api_request.patch("", data, format="json")
                    except TypeError as e:
                        raise e
                if dump_data:
                    data = json.dumps(data)
                    request = api_request.patch("", data=data, content_type="application/json")
            request.user = superuser
            kwargs = get_kwargs(obj, self.mvs, request=request, data=data)
        request.user = superuser
        request.query_params = dict()
        kwargs = get_kwargs(obj, self.mvs, request) if kwargs is None else kwargs
        request._messages = InMemoryMessageStorage(request)
        return obj, request, kwargs, data

    def _raise_warning_factory(self, name_test):
        print(  # noqa: T201
            f"\n- {self.__class__.__name__}:{name_test}",
            colored(
                f"WARNING - factory not found for {self.model.__name__ if self.model else None}",
                "yellow",
            ),
        )

    def _get_endpoint_config(self, request, kwargs, obj=None):
        self.mvs.kwargs = kwargs
        if obj:
            self.mvs.kwargs.update({"pk": obj.pk})
        ep = self.mvs(request=request).endpoint_config_class(
            self.mvs(request=request), request=request, instance=False
        )
        if obj:
            ep.instance = obj
        return ep


class TestRepresentationViewSet(ParentViewset):
    # Test "get": "list"
    def test_list_representation_viewset(self):
        if self.factory is None:
            self._raise_warning_factory("test_list_representation_viewset")
        else:
            _, request, kwargs, _ = self._get_mixins_data()
            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            print(  # noqa: T201
                f"\n- {self.__class__.__name__}:test_list_representation_viewset", colored("PASSED", "green")
            )

    # Test "get": "retrieve"
    def test_instance_representation_viewset(self):
        if self.factory is None:
            self._raise_warning_factory("test_instance_representation_viewset")
        else:
            obj, request, kwargs, _ = self._get_mixins_data()
            vs = self.mvs.as_view({"get": "retrieve"})
            response = vs(request, **kwargs, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            print(  # noqa: T201
                f"- {self.__class__.__name__}:test_instance_representation_viewset", colored("PASSED", "green")
            )

    def execute_test(self):
        self.test_list_representation_viewset()
        self.test_instance_representation_viewset()


class TestViewSet(ParentViewset):
    # test viewset Option request
    def test_option_request(self, is_instance=False):
        if self.factory is None:
            self._raise_warning_factory("test_option_request")
        else:
            obj, request, kwargs, _ = self._get_mixins_data("OPTIONS")
            if not is_instance:
                ep = self._get_endpoint_config(request, kwargs)
            else:
                ep = self._get_endpoint_config(request, kwargs, obj)
                if ep.get_instance_endpoint():
                    kwargs["pk"] = obj.pk
            vs = self.mvs.as_view({"options": "options"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            if "buttons" in response.data.keys():
                if "custom_instance" in response.data.get("buttons").keys():
                    assert (
                        list(response.data["buttons"]["custom_instance"])
                        or len(list(response.data["buttons"]["custom_instance"])) == 0
                    )
            assert response.data.get("fields"), str(response.data.get("fields")) + " should not be None"
            assert response.data.get("identifier"), str(response.data.get("identifier")) + " should not be None"
            # assert response.data.get("pagination")
            # assert response.data.get("pk")
            # assert response.data.get("type")
            # assert response.data.get("filterset_fields")
            # assert response.data.get("search_fields")
            # assert response.data.get("ordering_fields")
            # assert response.data.get("buttons"), str(response.data.get("buttons")) + " should not be None"  # TODO: Refactor - buttons can be none
            assert response.data.get("display"), str(response.data.get("display")) + " should not be None"
            assert response.data.get("titles"), str(response.data.get("titles")) + " should not be None"
            assert response.data.get("endpoints"), str(response.data.get("endpoints")) + " should not be None"
            # assert response.data.get("preview")
            print(f"- {self.__class__.__name__}:test_option_request", colored("PASSED", "green"))  # noqa: T201

    # ----- LIST ROUTE TEST ----- #
    # Test viewset "get": "list"
    def test_get_request(self):
        if self.factory is None:
            self._raise_warning_factory("test_get_request")
        else:
            _, request, kwargs, _ = self._get_mixins_data("GET")
            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            print(f"- {self.__class__.__name__}:test_get_request", colored("PASSED", "green"))  # noqa: T201

    # Test viewset "get": "list" -> aggregation
    def test_aggregation(self, name_field=None):
        if self.factory is None:
            self._raise_warning_factory("test_aggregation")
        else:
            _, request, kwargs, _ = self._get_mixins_data("GET")

            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            if not response.data.get("aggregates"):
                print(  # noqa: T201
                    f"- {self.__class__.__name__}:test_aggregation:" + self.mvs.__name__,
                    colored("WARNING - aggregates not found in " + self.mvs.__name__, "yellow"),
                )
            else:
                if name_field:
                    assert response.data.get("aggregates").get(name_field), name_field + "not found in aggregates"
            print(f"- {self.__class__.__name__}:test_aggregation", colored("PASSED", "green"))  # noqa: T201

    # Test viewset "get": "list" with client and endpoint
    def test_get_endpoint(self, client):
        if self.factory is None:
            self._raise_warning_factory("test_get_endpoint")
        else:
            _, request, kwargs, _ = self._get_mixins_data("GET")
            ep = self._get_endpoint_config(request, kwargs)
            client.force_login(request.user)
            if ep.get_endpoint():
                response = client.get(ep.get_endpoint())
            else:
                response = client.get(ep._get_list_endpoint())
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            print(f"- {self.__class__.__name__}:test_get_endpoint", colored("PASSED", "green"))  # noqa: T201

    # Test viewset "post": "create"
    def test_post_request(self, dump_data=False, data=None):
        if self.factory is None:
            self._raise_warning_factory("test_post_request")
        else:
            _, request, kwargs, _ = self._get_mixins_data("POST", dump_data=dump_data, data=data)
            vs = self.mvs.as_view({"post": "create"})
            ep = self._get_endpoint_config(request, kwargs)
            ep_create = ep.get_create_endpoint()
            response = vs(request, **kwargs)
            if ep_create:
                if response.status_code == status.HTTP_400_BAD_REQUEST:
                    try:
                        _, request, kwargs, _ = self._get_mixins_data(type="POST", dump_data=True, data=data)
                        vs = self.mvs.as_view({"post": "create"})
                        response2 = vs(request, **kwargs)
                        assert response2.status_code == status.HTTP_201_CREATED, (
                            str(response2.status_code)
                            + f" == 201 ({response2.data}). Result of first attempt[without dump_data]({response.data})"
                        )
                        response = response2
                    except TypeError:
                        assert response.status_code == status.HTTP_201_CREATED, (
                            str(response.status_code) + f" == 201 ({response.data})"
                        )
                else:
                    assert response.status_code == status.HTTP_201_CREATED, (
                        str(response.status_code) + f" == 201 ({response.data})"
                    )
                assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                    str(response.status_code) + f" == 405 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_post_request", colored("PASSED", "green"))  # noqa: T201

    # Test viewset "post": "create" with client and endpoint
    def test_post_endpoint(self, client, dump_data=False, data=None):
        if self.factory is None:
            self._raise_warning_factory("test_post_endpoint")
        else:
            _, request, kwargs, data = self._get_mixins_data("POST", dump_data=dump_data, data=data)
            ep = self._get_endpoint_config(request, kwargs)
            ep_create = ep.get_create_endpoint()
            client.force_login(request.user)
            response = client.post(ep_create, data)
            if ep_create:
                if response.status_code == status.HTTP_400_BAD_REQUEST:
                    try:
                        _, request, kwargs, data = self._get_mixins_data(type="POST", dump_data=True, data=data)
                        ep = self._get_endpoint_config(request, kwargs)
                        response2 = client.post(ep_create, data)
                        assert response2.status_code == status.HTTP_201_CREATED, (
                            str(response2.status_code)
                            + f" == 201 ({response2.data}). Result of first attempt[without dump_data]({response.data})"
                        )
                        response = response2
                    except TypeError:
                        assert response.status_code == status.HTTP_201_CREATED, (
                            str(response.status_code) + f" == 201 ({response.data})"
                        )
                else:
                    assert response.status_code == status.HTTP_201_CREATED, (
                        str(response.status_code) + f" == 201 ({response.data})"
                    )
                assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            else:
                assert response.status_code == status.HTTP_404_NOT_FOUND, (
                    str(response.status_code) + f" == 404 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_post_endpoint", colored("PASSED", "green"))  # noqa: T201

    # Test viewset "delete": "destroy_multiple"
    def test_destroy_multiple(self):
        if self.factory is None:
            self._raise_warning_factory("test_destroy_multiple")
        else:
            _, request, kwargs, _ = self._get_mixins_data("DELETE")
            for _ in range(4):
                self.factory()
            vs = self.mvs.as_view({"delete": "destroy_multiple"})
            ep = self._get_endpoint_config(request, kwargs)
            ep_delete = ep.get_delete_endpoint()
            response = vs(request, **kwargs)
            if ep_delete:
                assert response.status_code == status.HTTP_204_NO_CONTENT, (
                    str(response.status_code) + f" == 204 ({response.data})"
                )
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                    str(response.status_code) + f" == 405 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_destroy_multiple", colored("PASSED", "green"))  # noqa: T201

    # -------------- DETAIL ROUTE TEST ------------------#
    # Test viewset "get": "retrieve"
    def test_retrieve_request(self):
        if self.factory is None:
            self._raise_warning_factory("test_retrieve_request")
        else:
            obj, request, kwargs, _ = self._get_mixins_data("GET")
            vs = self.mvs.as_view({"get": "retrieve"})
            ep = self._get_endpoint_config(request, kwargs, obj)
            response = vs(request, **kwargs)
            if ep._get_instance_endpoint():
                assert response.status_code == status.HTTP_200_OK, (
                    str(response.status_code) + f" == 200 ({response.data})"
                )
                assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            print(f"- {self.__class__.__name__}:test_retrieve_request", colored("PASSED", "green"))  # noqa: T201

    # Test "delete": "destroy"
    def test_delete_request(self):
        if self.factory is None:
            self._raise_warning_factory("test_delete_request")
        else:
            obj, request, kwargs, _ = self._get_mixins_data("DELETE")
            vs = self.mvs.as_view({"delete": "destroy"})
            ep = self._get_endpoint_config(request, kwargs, obj)
            ep_delete = ep.get_delete_endpoint()
            response = vs(request, **kwargs)
            if ep_delete:
                assert response.status_code == status.HTTP_204_NO_CONTENT, (
                    str(response.status_code) + f" == 204 ({response.data})"
                )
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                    str(response.status_code) + f" == 405 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_delete_request", colored("PASSED", "green"))  # noqa: T201

    # Test "put": "update"
    def test_update_request(self, dump_data=False, data=None):
        if self.factory is None:
            self._raise_warning_factory("test_update_request")
        else:
            obj, request, kwargs, _ = self._get_mixins_data("UPDATE", dump_data=dump_data, data=data)
            vs = self.mvs.as_view({"put": "update"})
            ep = self._get_endpoint_config(request, kwargs, obj)
            ep_update = ep.get_update_endpoint()
            response = vs(request, **kwargs)
            if ep_update:
                if response.status_code == status.HTTP_400_BAD_REQUEST:
                    try:
                        obj, request, kwargs, _ = self._get_mixins_data(type="UPDATE", dump_data=True, data=data)
                        vs = self.mvs.as_view({"put": "update"})
                        ep = self._get_endpoint_config(request, kwargs, obj)
                        response2 = vs(request, **kwargs)
                        assert response2.status_code == status.HTTP_200_OK, (
                            str(response2.status_code)
                            + f" == 200 ({response2.data}). Result of first attempt[without dump_data]({response.data})"
                        )
                        response = response2
                    except TypeError:
                        assert response.status_code == status.HTTP_200_OK, (
                            str(response.status_code) + f" == 200 ({response.data})"
                        )
                else:
                    assert response.status_code == status.HTTP_200_OK, (
                        str(response.status_code) + f" == 200 ({response.data})"
                    )
                assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                    str(response.status_code) + f" == 405 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_update_request", colored("PASSED", "green"))  # noqa: T201

    # Test "patch": "partial_update",
    def test_patch_request(self, dump_data=False, data=None):
        if self.factory is None:
            self._raise_warning_factory("test_patch_request")
        else:
            obj, request, kwargs, data = self._get_mixins_data("PATCH", dump_data=dump_data, data=data)
            vs = self.mvs.as_view({"patch": "partial_update"})
            ep = self._get_endpoint_config(request, kwargs, obj)
            ep_instance = ep.get_instance_endpoint()
            ep_update = ep.get_update_endpoint()
            response = vs(request, **kwargs, data=data)
            if ep_instance and ep_update:
                if response.status_code == status.HTTP_400_BAD_REQUEST:
                    try:
                        obj, request, kwargs, data = self._get_mixins_data(type="PATCH", dump_data=True, data=data)
                        vs = self.mvs.as_view({"patch": "partial_update"})
                        ep = self._get_endpoint_config(request, kwargs, obj)
                        response2 = vs(request, **kwargs, data=data)
                        assert response2.status_code == status.HTTP_200_OK, (
                            str(response2.status_code)
                            + f" == 200 ({response2.data}). Result of first attempt[without dump_data]({response.data})"
                        )
                        response = response2
                    except TypeError:
                        assert response.status_code == status.HTTP_200_OK, (
                            str(response.status_code) + f" == 200 ({response.data})"
                        )
                else:
                    assert response.status_code == status.HTTP_200_OK, (
                        str(response.status_code) + f" == 200 ({response.data})"
                    )
                assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                    str(response.status_code) + f" == 405 ({response.data})"
                )
            print(f"- {self.__class__.__name__}:test_patch_request", colored("PASSED", "green"))  # noqa: T201

    # ----- LIST ROUTE TEST ----- #
    def execute_test_list_endpoint(self, client, aggregates=None):
        print("\n")  # noqa: T201
        self.test_option_request()
        self.test_get_request()
        self.test_aggregation(aggregates)
        # self.test_get_endpoint(client)
        self.test_post_request()
        # self.test_post_endpoint(client)
        self.test_destroy_multiple()

    # ----- DETAIL ROUTE TEST ----- #
    def execute_test_detail_endpoint(self):
        self.test_option_request(is_instance=True)
        self.test_retrieve_request()
        self.test_update_request()
        self.test_patch_request()
        self.test_delete_request()


class TestPandasView(TestViewSet):
    def test_get_request(self):
        if self.factory is None:
            self._raise_warning_factory("test_get_request")
        else:
            _, request, kwargs, _ = self._get_mixins_data("GET")
            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            print(f"- {self.__class__.__name__}:test_get_request", colored("PASSED", "green"))  # noqa: T201

    def execute_test(self):
        print("\n")  # noqa: T201
        self.test_get_request()


class TestChartViewSet(TestViewSet):
    def test_option_request(self, is_instance=False):
        if self.factory is None:
            self._raise_warning_factory("test_option_request")
        else:
            obj, request, kwargs, _ = self._get_mixins_data("OPTIONS")
            if not is_instance:
                ep = self._get_endpoint_config(request, kwargs)
            else:
                ep = self._get_endpoint_config(request, kwargs, obj)
                if ep.get_instance_endpoint():
                    kwargs["pk"] = obj.pk

            vs = self.mvs.as_view({"options": "options"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data, str(response.data) + " should not be empty"
            if "buttons" in response.data.keys():
                if "custom_instance" in response.data.get("buttons").keys():
                    assert (
                        list(response.data["buttons"]["custom_instance"])
                        or len(list(response.data["buttons"]["custom_instance"])) == 0
                    )
            assert response.data.get("identifier"), str(response.data.get("identifier")) + " should not be None"
            assert response.data.get("type") == "chart", "type of view should be chart"
            assert response.data.get("buttons"), str(response.data.get("buttons")) + " should not be None"
            assert response.data.get("display"), str(response.data.get("display")) + " should not be None"
            assert response.data.get("titles"), str(response.data.get("titles")) + " should not be None"
            assert response.data.get("endpoints"), str(response.data.get("endpoints")) + " should not be None"
            print(f"- {self.__class__.__name__}:test_option_request", colored("PASSED", "green"))  # noqa: T201

    def execute_test(self):
        print("\n")  # noqa: T201
        self.test_option_request()
        self.test_get_request()
