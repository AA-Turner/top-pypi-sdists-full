import json

from typing import Any, Callable

from flask import Flask, request

from nsj_rest_lib.settings import APP_NAME

from nsj_gcf_utils.rest_error_util import format_json_error

from nsj_multi_database_lib.decorator.multi_database import multi_database

from nsj_rest_lib.controller.controller_util import DEFAULT_RESP_HEADERS
from nsj_rest_lib.controller.delete_route import DeleteRoute
from nsj_rest_lib.controller.get_route import GetRoute
from nsj_rest_lib.controller.list_route import ListRoute
from nsj_rest_lib.controller.patch_route import PatchRoute
from nsj_rest_lib.controller.post_route import PostRoute
from nsj_rest_lib.controller.put_route import PutRoute

from nsj_rest_lib2.exception import MissingEntityConfigException
from nsj_rest_lib2.service.entity_loader import EntityLoader


def _get_query_args() -> tuple[str, str, bool]:
    # Tentando ler do query args
    query_args = request.args
    tenant = query_args.get("tenant")
    grupo_empresarial = query_args.get("grupo_empresarial")
    force_reload = query_args.get("force_reload", "false").lower() == "true"

    # Tentando ler do corpo da requisição
    try:
        body_str = request.data.decode("utf-8")
        body_json = json.loads(body_str)

        if not tenant:
            tenant = body_json.get("tenant")
        if not grupo_empresarial:
            grupo_empresarial = body_json.get("grupo_empresarial")
    except:
        pass

    return (str(tenant), str(grupo_empresarial), force_reload)


def _endpoint_name(func: Any, multidb: bool, root: str) -> str:
    suffix = "_mb" if multidb else ""
    return f"{root}_{func.__name__}{suffix}"


def setup_dynamic_routes(
    flask_app: Flask,
    multidb: bool = True,
    dynamic_root_path: str = "edl1",
    injector_factory: Any = None,
    escopo_in_url: bool = False,
    edls_path: str | None = None,
) -> None:

    if not escopo_in_url:
        COLLECTION_DYNAMIC_ROUTE = f"/{APP_NAME}/{dynamic_root_path}/<entity_resource>"
        ONE_DYNAMIC_ROUTE = f"/{APP_NAME}/{dynamic_root_path}/<entity_resource>/<id>"
    else:
        COLLECTION_DYNAMIC_ROUTE = (
            f"/{APP_NAME}/{dynamic_root_path}/<entity_escopo>/<entity_resource>"
        )
        ONE_DYNAMIC_ROUTE = (
            f"/{APP_NAME}/{dynamic_root_path}/<entity_escopo>/<entity_resource>/<id>"
        )

    entity_loader = EntityLoader(edls_path=edls_path)

    def _dynamic_route_wrapper(
        route_builder: Callable[[tuple[Any, ...]], Callable[..., Any]],
        endpoint_suffix: str | None = None,
    ) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if "entity_resource" not in kwargs:
                msg = "Faltando parâmetro identificador da entidade na URL."
                return (format_json_error(msg), 400, {**DEFAULT_RESP_HEADERS})
            entity_resource = kwargs.pop("entity_resource")

            entity_escopo = kwargs.pop("entity_escopo", "")

            tenant, grupo_empresarial, force_reload = _get_query_args()

            try:
                entity_config = entity_loader.load_entity_source(
                    entity_resource,
                    tenant,
                    grupo_empresarial,
                    escopo=entity_escopo,
                    force_reload=force_reload,
                )
            except MissingEntityConfigException:
                msg = f"Entity configuration for {entity_resource} not found."
                return (format_json_error(msg), 412, {**DEFAULT_RESP_HEADERS})

            (
                _,
                _,
                _,
                _,
                _,
                service_account,
                *rest,
            ) = entity_config

            route_handler = route_builder(entity_config)

            if multidb:
                route_handler = multi_database(service_account)(route_handler)

            return route_handler(*args, **kwargs)

        wrapper.__name__ = endpoint_suffix or f"{route_builder.__name__}_wrapper"
        return wrapper

    def list_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            _insert_function_class_name,
            _update_function_class_name,
            _insert_function_name,
            _update_function_name,
            _get_function_name,
            list_function_name,
            _delete_function_name,
            _get_function_type_class_name,
            list_function_type_class_name,
            _delete_function_type_class_name,
            *_,
            _custom_json_get_response,
            custom_json_list_response,
            _custom_json_delete_response,
        ) = entity_config

        def list_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "GET" not in api_verbs:
                return ("", 405, {})

            route = ListRoute(
                url=COLLECTION_DYNAMIC_ROUTE,
                http_method="GET",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                list_function_name=list_function_name,
                list_function_type_class=etities_dict.get(
                    list_function_type_class_name
                ),
                custom_json_response=bool(custom_json_list_response),
            )

            return route.handle_request(*args, **kwargs)

        return list_dynamic

    def get_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            _insert_function_class_name,
            _update_function_class_name,
            _insert_function_name,
            _update_function_name,
            get_function_name,
            _list_function_name,
            _delete_function_name,
            get_function_type_class_name,
            _list_function_type_class_name,
            _delete_function_type_class_name,
            *_,
            custom_json_get_response,
            _custom_json_list_response,
            _custom_json_delete_response,
        ) = entity_config

        def get_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "GET" not in api_verbs:
                return ("", 405, {})

            route = GetRoute(
                url=ONE_DYNAMIC_ROUTE,
                http_method="GET",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                get_function_name=get_function_name,
                get_function_type_class=etities_dict.get(get_function_type_class_name),
                custom_json_response=bool(custom_json_get_response),
            )

            return route.handle_request(*args, **kwargs)

        return get_dynamic

    def post_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            insert_function_class_name,
            _update_function_class_name,
            insert_function_name,
            _update_function_name,
            _get_function_name,
            _list_function_name,
            _delete_function_name,
            _get_function_type_class_name,
            _list_function_type_class_name,
            _delete_function_type_class_name,
            retrieve_after_insert,
            _retrieve_after_update,
            _retrieve_after_partial_update,
            post_response_dto_class_name,
            _put_response_dto_class_name,
            _patch_response_dto_class_name,
            custom_json_post_response,
            _custom_json_put_response,
            _custom_json_patch_response,
            _custom_json_get_response,
            _custom_json_list_response,
            _custom_json_delete_response,
        ) = entity_config

        def post_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "POST" not in api_verbs:
                return ("", 405, {})

            insert_function_type_class = (
                etities_dict.get(insert_function_class_name)
                if insert_function_class_name
                else None
            )

            dto_response_class = (
                etities_dict.get(post_response_dto_class_name)
                if post_response_dto_class_name
                else None
            )

            route = PostRoute(
                url=COLLECTION_DYNAMIC_ROUTE,
                http_method="POST",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                insert_function_type_class=insert_function_type_class,
                insert_function_name=insert_function_name,
                dto_response_class=dto_response_class,
                retrieve_after_insert=retrieve_after_insert,
                custom_json_response=bool(custom_json_post_response),
            )

            return route.handle_request(*args, **kwargs)

        return post_dynamic

    def put_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            _insert_function_class_name,
            update_function_class_name,
            _insert_function_name,
            update_function_name,
            _get_function_name,
            _list_function_name,
            _delete_function_name,
            _get_function_type_class_name,
            _list_function_type_class_name,
            _delete_function_type_class_name,
            _retrieve_after_insert,
            retrieve_after_update,
            _retrieve_after_partial_update,
            _post_response_dto_class_name,
            put_response_dto_class_name,
            _patch_response_dto_class_name,
            _custom_json_post_response,
            custom_json_put_response,
            _custom_json_patch_response,
            _custom_json_get_response,
            _custom_json_list_response,
            _custom_json_delete_response,
        ) = entity_config

        dto_response_class = (
            etities_dict.get(put_response_dto_class_name)
            if put_response_dto_class_name
            else None
        )

        def put_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "PUT" not in api_verbs:
                return ("", 405, {})

            update_function_type_class = (
                etities_dict.get(update_function_class_name)
                if update_function_class_name
                else None
            )

            route = PutRoute(
                url=ONE_DYNAMIC_ROUTE,
                http_method="PUT",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                update_function_type_class=update_function_type_class,
                update_function_name=update_function_name,
                dto_response_class=dto_response_class,
                retrieve_after_update=retrieve_after_update,
                custom_json_response=bool(custom_json_put_response),
            )

            return route.handle_request(*args, **kwargs)

        return put_dynamic

    def patch_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            _insert_function_class_name,
            _update_function_class_name,
            _insert_function_name,
            _update_function_name,
            _get_function_name,
            _list_function_name,
            _delete_function_name,
            _get_function_type_class_name,
            _list_function_type_class_name,
            _delete_function_type_class_name,
            _retrieve_after_insert,
            _retrieve_after_update,
            retrieve_after_partial_update,
            _post_response_dto_class_name,
            _put_response_dto_class_name,
            patch_response_dto_class_name,
            _custom_json_post_response,
            _custom_json_put_response,
            custom_json_patch_response,
            _custom_json_get_response,
            _custom_json_list_response,
            _custom_json_delete_response,
        ) = entity_config

        def patch_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "PATCH" not in api_verbs:
                return ("", 405, {})

            dto_response_class = (
                etities_dict.get(patch_response_dto_class_name)
                if patch_response_dto_class_name
                else None
            )

            route = PatchRoute(
                url=ONE_DYNAMIC_ROUTE,
                http_method="PATCH",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                dto_response_class=dto_response_class,
                retrieve_after_partial_update=retrieve_after_partial_update,
                custom_json_response=bool(custom_json_patch_response),
            )

            return route.handle_request(*args, **kwargs)

        return patch_dynamic

    def delete_dynamic_builder(entity_config: tuple[Any, ...]) -> Callable[..., Any]:
        (
            dto_class_name,
            entity_class_name,
            etities_dict,
            api_expose,
            api_verbs,
            _service_account,
            _insert_function_class_name,
            _update_function_class_name,
            _insert_function_name,
            _update_function_name,
            _get_function_name,
            _list_function_name,
            delete_function_name,
            _get_function_type_class_name,
            _list_function_type_class_name,
            delete_function_type_class_name,
            *_,
            _custom_json_get_response,
            _custom_json_list_response,
            custom_json_delete_response,
        ) = entity_config

        def delete_dynamic(*args: Any, **kwargs: Any) -> Any:
            if not api_expose or "DELETE" not in api_verbs:
                return ("", 405, {})

            route = DeleteRoute(
                url=ONE_DYNAMIC_ROUTE,
                http_method="DELETE",
                dto_class=etities_dict[dto_class_name],
                entity_class=etities_dict[entity_class_name],
                injector_factory=injector_factory,
                delete_function_name=delete_function_name,
                delete_function_type_class=etities_dict.get(
                    delete_function_type_class_name
                ),
                custom_json_response=bool(custom_json_delete_response),
            )

            return route.handle_request(*args, **kwargs)

        return delete_dynamic

    list_dynamic = _dynamic_route_wrapper(
        list_dynamic_builder, endpoint_suffix="list_dynamic"
    )
    get_dynamic = _dynamic_route_wrapper(
        get_dynamic_builder, endpoint_suffix="get_dynamic"
    )
    post_dynamic = _dynamic_route_wrapper(
        post_dynamic_builder, endpoint_suffix="post_dynamic"
    )
    put_dynamic = _dynamic_route_wrapper(
        put_dynamic_builder, endpoint_suffix="put_dynamic"
    )
    patch_dynamic = _dynamic_route_wrapper(
        patch_dynamic_builder, endpoint_suffix="patch_dynamic"
    )
    delete_dynamic = _dynamic_route_wrapper(
        delete_dynamic_builder, endpoint_suffix="delete_dynamic"
    )

    # Registrando as rotas no flask
    flask_app.add_url_rule(
        COLLECTION_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(list_dynamic, multidb, dynamic_root_path),
        view_func=list_dynamic,
        methods=["GET"],
    )
    flask_app.add_url_rule(
        ONE_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(get_dynamic, multidb, dynamic_root_path),
        view_func=get_dynamic,
        methods=["GET"],
    )
    flask_app.add_url_rule(
        COLLECTION_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(post_dynamic, multidb, dynamic_root_path),
        view_func=post_dynamic,
        methods=["POST"],
    )
    flask_app.add_url_rule(
        ONE_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(put_dynamic, multidb, dynamic_root_path),
        view_func=put_dynamic,
        methods=["PUT"],
    )
    flask_app.add_url_rule(
        ONE_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(patch_dynamic, multidb, dynamic_root_path),
        view_func=patch_dynamic,
        methods=["PATCH"],
    )
    flask_app.add_url_rule(
        ONE_DYNAMIC_ROUTE,
        endpoint=_endpoint_name(delete_dynamic, multidb, dynamic_root_path),
        view_func=delete_dynamic,
        methods=["DELETE"],
    )
