import datetime
import json
import os
import re
import sys
import threading
import heapq
import types
from typing import Any

from redis.exceptions import RedisError
from nsj_rest_lib.settings import get_logger
from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase

import yaml

from nsj_rest_lib2.compiler.compiler import EDLCompiler
from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.model import CompilerResult, RelationDependency
from nsj_rest_lib2.compiler.util.type_naming_util import (
    build_entity_hash as build_entity_hash_util,
    compile_namespace_keys,
    resolve_namespace_key as resolve_namespace_key_util,
)
from nsj_rest_lib2.dto.escopo_dto import EscopoDTO
from nsj_rest_lib2.exception import (
    MissingDependencyConfigException,
    MissingEntityConfigException,
)
from nsj_rest_lib2.settings import (
    EDLS_FROM_REDIS,
    ESCOPO_RESTLIB2,
    MIN_TIME_SOURCE_REFRESH,
)


class LoadedEntity:
    def __init__(self):
        self.dto_class_name: str = ""
        self.entity_class_name: str = ""
        self.entity_hash: str = ""
        self.loaded_at: datetime.datetime = datetime.datetime.now()
        self.api_expose: bool = False
        self.api_verbs: list[str] = []
        self.relations_dependencies: list[RelationDependency] = []
        self.never_expire: bool = False
        self.service_account: str | None = None
        self.insert_function_class_name: str | None = None
        self.update_function_class_name: str | None = None
        self.insert_function_name: str | None = None
        self.update_function_name: str | None = None
        self.get_function_name: str | None = None
        self.list_function_name: str | None = None
        self.delete_function_name: str | None = None
        self.get_function_type_class_name: str | None = None
        self.list_function_type_class_name: str | None = None
        self.delete_function_type_class_name: str | None = None
        self.retrieve_after_insert: bool = False
        self.retrieve_after_update: bool = False
        self.retrieve_after_partial_update: bool = False
        self.post_response_dto_class_name: str | None = None
        self.put_response_dto_class_name: str | None = None
        self.patch_response_dto_class_name: str | None = None
        self.custom_json_post_response: bool = False
        self.custom_json_put_response: bool = False
        self.custom_json_patch_response: bool = False
        self.custom_json_get_response: bool = False
        self.custom_json_list_response: bool = False
        self.custom_json_delete_response: bool = False


class Namespace:
    def __init__(self):
        self.key: str = ""
        self.loaded_entities: dict[str, LoadedEntity] = {}
        self.entities_dict: dict = {}
        self.module: types.ModuleType = types.ModuleType("empty")


namespaces_dict: dict[str, Namespace] = {}


class _CircularDependencyLoadException(Exception):
    """
    Excecao interna para interromper somente o ramo recursivo com ciclo.
    """

    def __init__(self, loading_key: str):
        self.loading_key = loading_key
        super().__init__(f"Circular dependency detected while loading '{loading_key}'.")


class EntityLoader:
    def __init__(self, edls_path: str | None = None) -> types.NoneType:
        self._lock = threading.Lock()
        if edls_path:
            self._load_edls_from_disk(edls_path)

    def load_entity_source(
        self,
        entity_resource: str,
        tenant: str | None,
        grupo_empresarial: str | None,
        escopo: str = ESCOPO_RESTLIB2,
        force_reload: bool = False,
        _loading_chain: set[str] | None = None,
    ) -> tuple[
        str,
        str,
        dict,
        bool,
        list[str],
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        bool,
        bool,
        bool,
        str | None,
        str | None,
        str | None,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ]:
        # Assumindo o escopo default se necessário
        if not escopo:
            escopo = ESCOPO_RESTLIB2

        if _loading_chain is None:
            _loading_chain = set()

        # Guarda o caminho atual para detectar ciclos durante carga recursiva.
        loading_key = (
            f"{escopo}/{entity_resource}"
            f"|tenant={tenant}|grupo_empresarial={grupo_empresarial}"
        )
        if loading_key in _loading_chain:
            raise _CircularDependencyLoadException(loading_key)
        _loading_chain.add(loading_key)

        # Montando as chaves dos namespaces
        grupo_key, tenant_key, default_key = compile_namespace_keys(
            tenant, grupo_empresarial
        )

        result = self._search_entity_namespace_in_memory(
            entity_resource, grupo_key, tenant_key, default_key
        )

        # Se conseguiu localizar na memória, verifica se houve alteração no hash, em relação ao redis
        if result is not None:
            # Desempacotando o result e recuperando informações do namespace
            (
                entity_config_key,
                namespace,
            ) = result

            loaded_entity = namespace.loaded_entities[entity_resource]
            dto_class_name = loaded_entity.dto_class_name
            entity_class_name = loaded_entity.entity_class_name
            entities_dict = namespace.entities_dict
            api_expose = loaded_entity.api_expose
            api_verbs = loaded_entity.api_verbs
            service_account = loaded_entity.service_account
            relations_dependencies = loaded_entity.relations_dependencies
            insert_function_class_name = loaded_entity.insert_function_class_name
            update_function_class_name = loaded_entity.update_function_class_name
            insert_function_name = loaded_entity.insert_function_name
            update_function_name = loaded_entity.update_function_name
            get_function_name = loaded_entity.get_function_name
            list_function_name = loaded_entity.list_function_name
            delete_function_name = loaded_entity.delete_function_name
            get_function_type_class_name = (
                loaded_entity.get_function_type_class_name
            )
            list_function_type_class_name = (
                loaded_entity.list_function_type_class_name
            )
            delete_function_type_class_name = (
                loaded_entity.delete_function_type_class_name
            )

            cached_result = (
                dto_class_name,
                entity_class_name,
                entities_dict,
                api_expose,
                api_verbs,
                service_account,
                insert_function_class_name,
                update_function_class_name,
                insert_function_name,
                update_function_name,
                get_function_name,
                list_function_name,
                delete_function_name,
                get_function_type_class_name,
                list_function_type_class_name,
                delete_function_type_class_name,
                loaded_entity.retrieve_after_insert,
                loaded_entity.retrieve_after_update,
                loaded_entity.retrieve_after_partial_update,
                loaded_entity.post_response_dto_class_name,
                loaded_entity.put_response_dto_class_name,
                loaded_entity.patch_response_dto_class_name,
                loaded_entity.custom_json_post_response,
                loaded_entity.custom_json_put_response,
                loaded_entity.custom_json_patch_response,
                loaded_entity.custom_json_get_response,
                loaded_entity.custom_json_list_response,
                loaded_entity.custom_json_delete_response,
            )

            # Verificando se alguma de suas dependências precisariam ser recarregadas
            for rd in relations_dependencies:
                if rd.entity_resource is None or rd.entity_scope is None:
                    raise RuntimeError(
                        f"Erro: Dependência de entidade mal formada na entidade {entity_resource}."
                    )

                try:
                    self.load_entity_source(
                        rd.entity_resource,
                        str(rd.tenant),
                        str(rd.grupo_empresarial),
                        rd.entity_scope,
                        force_reload=force_reload,
                        _loading_chain=_loading_chain,
                    )
                except _CircularDependencyLoadException as exc:
                    # Em ciclo A->B->A, a dependencia ja esta em processo de carga.
                    get_logger().debug(
                        f"Ciclo de dependência ignorado durante carregamento: {exc.loading_key}"
                    )
                    continue
                except MissingDependencyConfigException as exc:
                    # Preserva a causa original, atualizando o contexto da entidade atual.
                    raise MissingDependencyConfigException(
                        entity_resource=entity_resource,
                        dependency_resource=exc.dependency_resource,
                        dependency_scope=exc.dependency_scope,
                        dependency_tenant=exc.dependency_tenant,
                        dependency_grupo_empresarial=exc.dependency_grupo_empresarial,
                    ) from exc
                except MissingEntityConfigException as exc:
                    # Converte falha generica da dependencia para erro especializado.
                    raise MissingDependencyConfigException(
                        entity_resource=entity_resource,
                        dependency_resource=rd.entity_resource,
                        dependency_scope=rd.entity_scope,
                        dependency_tenant=rd.tenant,
                        dependency_grupo_empresarial=(
                            str(rd.grupo_empresarial)
                            if rd.grupo_empresarial
                            else None
                        ),
                    ) from exc

            if loaded_entity.never_expire or not EDLS_FROM_REDIS:
                return cached_result

            # Se o tempo entre o carregamento e agora for maior do que MIN_TIME_SOURCE_REFRESH minutos,
            # verifica se precisa de refresh
            time_diff = datetime.datetime.now() - loaded_entity.loaded_at

            if (
                time_diff.total_seconds() >= MIN_TIME_SOURCE_REFRESH * 60
                or force_reload
            ):
                # Renovando o tempo de refresh
                loaded_entity.loaded_at = datetime.datetime.now()

                # Recuperando do Redis direto pela key (faz uma só chamada ao redis)
                try:
                    loaded_config = self._load_entity_config_from_redis(
                        entity_resource,
                        grupo_key,
                        tenant_key,
                        default_key,
                        entity_config_key,
                        escopo=escopo,
                    )

                    if not loaded_config and entity_config_key is not None:
                        loaded_config = self._load_entity_config_from_redis(
                            entity_resource,
                            grupo_key,
                            tenant_key,
                            default_key,
                            None,
                            escopo=escopo,
                        )
                except RedisError as exc:
                    get_logger().warning(
                        "Redis unavailable while refreshing entity cache "
                        f"for '{entity_resource}'. Keeping in-memory version. Error: {exc}"
                    )
                    return cached_result
                # Se não achar no redis, remove cache stale em memória e
                # sinaliza que a entidade não está mais disponível.
                if not loaded_config:
                    self._evict_entity_from_memory(
                        entity_resource=entity_resource,
                        entity_config_key=entity_config_key,
                        grupo_key=grupo_key,
                        tenant_key=tenant_key,
                        default_key=default_key,
                    )
                    raise MissingEntityConfigException()

                # Desempacotando resultado
                entity_config_key, entity_config_str = loaded_config

                # Executando o código da entidade, só se houver mudança no hash
                result_execute = self._execute_entity_source(
                    entity_config_str,
                    entity_config_key,
                    entity_resource,
                    check_refresh=True,
                    _loading_chain=_loading_chain,
                )

                # Se não carregou novo código, usa o que estava em memória
                if result_execute is None:
                    return cached_result
                else:
                    (
                        dto_class_name,
                        entity_class_name,
                        namespace,
                        api_expose,
                        api_verbs,
                        service_account,
                        insert_function_class_name,
                        update_function_class_name,
                        insert_function_name,
                        update_function_name,
                        get_function_name,
                        list_function_name,
                        delete_function_name,
                        get_function_type_class_name,
                        list_function_type_class_name,
                        delete_function_type_class_name,
                        retrieve_after_insert,
                        retrieve_after_update,
                        retrieve_after_partial_update,
                        post_response_dto_class_name,
                        put_response_dto_class_name,
                        patch_response_dto_class_name,
                        custom_json_post_response,
                        custom_json_put_response,
                        custom_json_patch_response,
                        custom_json_get_response,
                        custom_json_list_response,
                        custom_json_delete_response,
                    ) = result_execute
                    return (
                        dto_class_name,
                        entity_class_name,
                        namespace.entities_dict,
                        api_expose,
                        api_verbs,
                        service_account,
                        insert_function_class_name,
                        update_function_class_name,
                        insert_function_name,
                        update_function_name,
                        get_function_name,
                        list_function_name,
                        delete_function_name,
                        get_function_type_class_name,
                        list_function_type_class_name,
                        delete_function_type_class_name,
                        retrieve_after_insert,
                        retrieve_after_update,
                        retrieve_after_partial_update,
                        post_response_dto_class_name,
                        put_response_dto_class_name,
                        patch_response_dto_class_name,
                        custom_json_post_response,
                        custom_json_put_response,
                        custom_json_patch_response,
                        custom_json_get_response,
                        custom_json_list_response,
                        custom_json_delete_response,
                    )
            else:
                # Se não deu o intervalo de verificação do refresh, retorna o que está em memória
                return cached_result

        if not EDLS_FROM_REDIS:
            raise MissingEntityConfigException()

        # Se não conseguir recuperar a entidade, procura no redis:
        loaded_config = self._load_entity_config_from_redis(
            entity_resource,
            grupo_key,
            tenant_key,
            default_key,
            None,
            escopo=escopo,
        )

        # Se também não achar no redis, lanca exceção
        if not loaded_config:
            raise MissingEntityConfigException()

        # Desempacotando resultado
        entity_config_key, entity_config_str = loaded_config

        # Executando o código da entidade
        result_execute = self._execute_entity_source(
            entity_config_str,
            entity_config_key,
            entity_resource,
            _loading_chain=_loading_chain,
        )

        if result_execute is None:
            raise RuntimeError(
                f"Erro desconhecido carregando entidade: {entity_resource}"
            )
        (
            dto_class_name,
            entity_class_name,
            namespace,
            api_expose,
            api_verbs,
            service_account,
            insert_function_class_name,
            update_function_class_name,
            insert_function_name,
            update_function_name,
            get_function_name,
            list_function_name,
            delete_function_name,
            get_function_type_class_name,
            list_function_type_class_name,
            delete_function_type_class_name,
            retrieve_after_insert,
            retrieve_after_update,
            retrieve_after_partial_update,
            post_response_dto_class_name,
            put_response_dto_class_name,
            patch_response_dto_class_name,
            custom_json_post_response,
            custom_json_put_response,
            custom_json_patch_response,
            custom_json_get_response,
            custom_json_list_response,
            custom_json_delete_response,
        ) = result_execute

        return (
            dto_class_name,
            entity_class_name,
            namespace.entities_dict,
            api_expose,
            api_verbs,
            service_account,
            insert_function_class_name,
            update_function_class_name,
            insert_function_name,
            update_function_name,
            get_function_name,
            list_function_name,
            delete_function_name,
            get_function_type_class_name,
            list_function_type_class_name,
            delete_function_type_class_name,
            retrieve_after_insert,
            retrieve_after_update,
            retrieve_after_partial_update,
            post_response_dto_class_name,
            put_response_dto_class_name,
            patch_response_dto_class_name,
            custom_json_post_response,
            custom_json_put_response,
            custom_json_patch_response,
            custom_json_get_response,
            custom_json_list_response,
            custom_json_delete_response,
        )

    def clear_namespaces(self):
        """
        Clears all loaded namespaces from memory.

        This method removes all entries from the namespaces_dict, effectively resetting
        the in-memory cache of loaded entities and their associated namespaces.
        """
        with self._lock:
            namespaces_dict.clear()

    def _load_edls_from_disk(self, edls_path: str) -> None:
        if namespaces_dict:
            return

        resolved_path = self._resolve_edls_path(edls_path)
        if not resolved_path:
            return

        if os.path.isdir(resolved_path):
            edl_files = self._list_edl_files(resolved_path)
        elif os.path.isfile(resolved_path) and self._is_edl_file(resolved_path):
            edl_files = [resolved_path]
        else:
            return

        if not edl_files:
            return

        compiler = EDLCompiler()
        entities: dict[str, EntityModelBase] = {}
        dependencies_map: dict[str, list[str]] = {}
        order_hint: list[str] = []
        for file_path in edl_files:
            edl_json = self._read_edl_file(file_path)
            if not isinstance(edl_json, dict):
                continue

            dependencies, entity_model = compiler.list_dependencies(edl_json)
            complete_entity_id = f"{entity_model.escopo}/{entity_model.id}"
            if complete_entity_id in entities:
                get_logger().warning(
                    f"Entidade duplicada encontrada em EDLs: '{complete_entity_id}'. Usando a última ocorrência."
                )
            entities[complete_entity_id] = entity_model
            dependencies_map[complete_entity_id] = dependencies
            order_hint.append(complete_entity_id)

        if not entities:
            return

        escopos: dict[str, EscopoDTO] = {}
        for entity_model in entities.values():
            if entity_model.escopo not in escopos:
                escopos[entity_model.escopo] = EscopoDTO(
                    codigo=entity_model.escopo,
                    service_account=None,
                )

        dependencies = list(entities.items())

        ordered_entity_ids = self._order_entities_by_dependency(
            entities, dependencies_map, order_hint
        )

        for entity_id in ordered_entity_ids:
            entity_model = entities[entity_id]
            escopo_dto = escopos.get(entity_model.escopo)
            if escopo_dto is None:
                continue

            compiler_result = compiler.compile_model(
                entity_model,
                dependencies,
                escopo=escopo_dto,
            )
            if not compiler_result:
                continue

            entity_config = self._build_entity_payload(
                entity_model,
                compiler_result,
            )
            entity_resource = entity_config.get("api_resource")
            if not entity_resource:
                continue

            entity_config_key = self._resolve_namespace_key(entity_model)
            self._execute_entity_source(
                json.dumps(entity_config, ensure_ascii=False),
                entity_config_key,
                entity_resource,
                from_disk=True,
                # Durante bootstrap por EDL em disco, depend?ncias devem ser resolvidas
                # pela ordena??o dos EDLs carregados, sem fallback para Redis.
                skip_dependency_load=True,
            )

    def _order_entities_by_dependency(
        self,
        entities: dict[str, EntityModelBase],
        dependencies_map: dict[str, list[str]],
        order_hint: list[str],
    ) -> list[str]:
        # Base order: maintain file order, then append any missing keys
        base_order: list[str] = []
        seen: set[str] = set()
        for key in order_hint:
            if key in entities and key not in seen:
                base_order.append(key)
                seen.add(key)
        for key in entities.keys():
            if key not in seen:
                base_order.append(key)
                seen.add(key)

        order_index = {key: idx for idx, key in enumerate(base_order)}

        # Build dependency graph (edges: dep -> entity)
        forward: dict[str, set[str]] = {key: set() for key in entities}
        in_degree: dict[str, int] = {key: 0 for key in entities}
        missing_deps: dict[str, set[str]] = {}

        for key, deps in dependencies_map.items():
            for dep in deps or []:
                if dep not in entities:
                    missing_deps.setdefault(key, set()).add(dep)
                    continue
                if dep == key:
                    continue
                if key not in forward[dep]:
                    forward[dep].add(key)
                    in_degree[key] += 1

        if missing_deps:
            missing_str = ", ".join(
                f"{k} -> {sorted(list(v))}" for k, v in missing_deps.items()
            )
            get_logger().warning(
                f"Dependências externas não encontradas nos EDLs locais: {missing_str}"
            )

        heap: list[tuple[int, str]] = [
            (order_index.get(key, 0), key)
            for key, deg in in_degree.items()
            if deg == 0
        ]
        heapq.heapify(heap)

        ordered: list[str] = []
        while heap:
            _, key = heapq.heappop(heap)
            ordered.append(key)
            for dependent in forward.get(key, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    heapq.heappush(
                        heap, (order_index.get(dependent, 0), dependent)
                    )

        if len(ordered) != len(entities):
            ordered_set = set(ordered)
            remaining = [key for key in base_order if key not in ordered_set]
            get_logger().warning(
                "Não foi possível resolver a ordem completa das dependências. "
                "Mantendo ordem topológica parcial e anexando o restante na ordem original."
            )
            return ordered + remaining

        return ordered

    def _resolve_edls_path(self, edls_path: str) -> str | None:
        edls_path = edls_path.strip()
        if not edls_path:
            return None
        if os.path.isabs(edls_path):
            return edls_path
        return os.path.join(os.getcwd(), edls_path)

    def _is_edl_file(self, file_path: str) -> bool:
        lower_name = file_path.lower()
        return lower_name.endswith(".json") or lower_name.endswith(
            ".yml"
        ) or lower_name.endswith(".yaml")

    def _list_edl_files(self, root_path: str) -> list[str]:
        edl_files: list[str] = []
        for current_root, _, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(current_root, file_name)
                if self._is_edl_file(file_path):
                    edl_files.append(file_path)
        edl_files.sort()
        return edl_files

    def _read_edl_file(self, file_path: str) -> dict[str, Any] | None:
        with open(file_path, "r", encoding="utf-8") as file_handler:
            if file_path.lower().endswith(".json"):
                return json.load(file_handler)
            return yaml.safe_load(file_handler)

    def _resolve_namespace_key(self, entity_model: EntityModelBase) -> str:
        tenant = getattr(entity_model, "tenant", None)
        grupo_empresarial = getattr(entity_model, "grupo_empresarial", None)

        return resolve_namespace_key_util(tenant, grupo_empresarial)

    def _build_entity_payload(
        self,
        entity_model: EntityModelBase,
        compiler_result: CompilerResult,
    ) -> dict[str, Any]:
        api_resource = compiler_result.api_resource
        if not api_resource:
            if isinstance(entity_model, EntityModel) and entity_model.api:
                api_resource = entity_model.api.resource
        if not api_resource:
            raise ValueError("api.resource é obrigatório para carregar EDLs.")

        relations = [
            rd.to_dict()
            for rd in (compiler_result.relations_dependencies or [])
        ]

        return {
            "dto_class_name": compiler_result.dto_class_name,
            "entity_class_name": compiler_result.entity_class_name,
            "service_account": compiler_result.service_account,
            "insert_function_class_name": compiler_result.insert_function_class_name,
            "insert_function_name": compiler_result.insert_function_name,
            "source_insert_function": compiler_result.source_insert_function,
            "update_function_class_name": compiler_result.update_function_class_name,
            "update_function_name": compiler_result.update_function_name,
            "source_update_function": compiler_result.source_update_function,
            "get_function_name": compiler_result.get_function_name,
            "list_function_name": compiler_result.list_function_name,
            "delete_function_name": compiler_result.delete_function_name,
            "get_function_type_class_name": compiler_result.get_function_type_class_name,
            "list_function_type_class_name": compiler_result.list_function_type_class_name,
            "delete_function_type_class_name": compiler_result.delete_function_type_class_name,
            "source_get_function_type": compiler_result.source_get_function_type,
            "source_list_function_type": compiler_result.source_list_function_type,
            "source_delete_function_type": compiler_result.source_delete_function_type,
            "retrieve_after_insert": compiler_result.retrieve_after_insert,
            "retrieve_after_update": compiler_result.retrieve_after_update,
            "retrieve_after_partial_update": compiler_result.retrieve_after_partial_update,
            "post_response_dto_class_name": compiler_result.post_response_dto_class_name,
            "put_response_dto_class_name": compiler_result.put_response_dto_class_name,
            "patch_response_dto_class_name": compiler_result.patch_response_dto_class_name,
            "custom_json_post_response": compiler_result.custom_json_post_response,
            "custom_json_put_response": compiler_result.custom_json_put_response,
            "custom_json_patch_response": compiler_result.custom_json_patch_response,
            "custom_json_get_response": compiler_result.custom_json_get_response,
            "custom_json_list_response": compiler_result.custom_json_list_response,
            "custom_json_delete_response": compiler_result.custom_json_delete_response,
            "source_dto": compiler_result.dto_code,
            "source_entity": compiler_result.entity_code,
            "entity_hash": self._build_entity_hash(compiler_result),
            "api_expose": compiler_result.api_expose,
            "api_resource": api_resource,
            "api_verbs": compiler_result.api_verbs or [],
            "relations_dependencies": relations,
        }

    def _build_entity_hash(self, compiler_result: CompilerResult) -> str:
        return build_entity_hash_util(compiler_result)

    def _ensure_dynamic_package(self):
        """
        Garante que exista um pacote 'dynamic' em sys.modules.
        """
        pkg = sys.modules.get("dynamic")
        if pkg is None:
            pkg = types.ModuleType("dynamic")
            pkg.__path__ = []  # marca como pacote
            pkg.__package__ = "dynamic"
            sys.modules["dynamic"] = pkg
        return pkg

    def _execute_entity_source(
        self,
        entity_config_str: str,
        entity_config_key: str,
        entity_resource: str,
        check_refresh: bool = False,
        from_disk: bool = False,
        skip_dependency_load: bool = False,
        _loading_chain: set[str] | None = None,
    ) -> tuple[
        str,
        str,
        Namespace,
        bool,
        list[str],
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        bool,
        bool,
        bool,
        str | None,
        str | None,
        str | None,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] | None:
        # Interpretando o json de configuração da entidade
        try:
            entity_config = json.loads(entity_config_str)

            dto_class_name = entity_config["dto_class_name"]
            entity_class_name = entity_config["entity_class_name"]
            source_dto = entity_config["source_dto"]
            source_entity = entity_config["source_entity"]
            entity_hash = entity_config["entity_hash"]

            api_expose = entity_config["api_expose"]
            # api_resource = entity_config["api_resource"]
            api_verbs = entity_config["api_verbs"]
            service_account = entity_config.get("service_account")
            insert_function_class_name = entity_config.get(
                "insert_function_class_name"
            )
            insert_function_name = entity_config.get("insert_function_name")
            insert_function_code = entity_config.get("source_insert_function")
            update_function_class_name = entity_config.get(
                "update_function_class_name"
            )
            update_function_name = entity_config.get("update_function_name")
            update_function_code = entity_config.get("source_update_function")
            get_function_name = entity_config.get("get_function_name")
            list_function_name = entity_config.get("list_function_name")
            delete_function_name = entity_config.get("delete_function_name")
            get_function_type_class_name = entity_config.get(
                "get_function_type_class_name"
            )
            list_function_type_class_name = entity_config.get(
                "list_function_type_class_name"
            )
            delete_function_type_class_name = entity_config.get(
                "delete_function_type_class_name"
            )
            retrieve_after_insert = entity_config.get(
                "retrieve_after_insert", False
            )
            retrieve_after_update = entity_config.get(
                "retrieve_after_update", False
            )
            retrieve_after_partial_update = entity_config.get(
                "retrieve_after_partial_update", False
            )
            post_response_dto_class_name = entity_config.get(
                "post_response_dto_class_name"
            )
            put_response_dto_class_name = entity_config.get(
                "put_response_dto_class_name"
            )
            patch_response_dto_class_name = entity_config.get(
                "patch_response_dto_class_name"
            )
            custom_json_post_response = entity_config.get(
                "custom_json_post_response", False
            )
            custom_json_put_response = entity_config.get(
                "custom_json_put_response", False
            )
            custom_json_patch_response = entity_config.get(
                "custom_json_patch_response", False
            )
            custom_json_get_response = entity_config.get(
                "custom_json_get_response", False
            )
            custom_json_list_response = entity_config.get(
                "custom_json_list_response", False
            )
            custom_json_delete_response = entity_config.get(
                "custom_json_delete_response", False
            )
            get_function_code = entity_config.get("source_get_function_type")
            list_function_code = entity_config.get("source_list_function_type")
            delete_function_code = entity_config.get("source_delete_function_type")
            relations_dependencies = [
                RelationDependency().from_dict(rd)
                for rd in entity_config.get("relations_dependencies", [])
            ]
        except json.JSONDecodeError as e:
            if not check_refresh:
                raise RuntimeError(
                    f"Erro ao decodificar JSON da entidade {entity_resource}; na chave {entity_config_key}: {e}"
                )
            else:
                get_logger().error(
                    f"Erro ao decodificar JSON da entidade {entity_resource}; na chave {entity_config_key}: {e}"
                )
                return None

        # Verificando se a entidade precisa ou não de refresh
        if check_refresh:
            loaded_namespace = namespaces_dict.get(entity_config_key)
            if not loaded_namespace:
                return None

            loaded_entity = loaded_namespace.loaded_entities.get(entity_resource)
            if not loaded_entity:
                return None

            if loaded_entity.entity_hash == entity_hash:
                return None

        # Imprimindo alerta de load no log
        get_logger().debug(
            f"Carregando entidade {entity_resource} no namespace {entity_config_key}."
        )

        # Publica a Entity real antes de recursar nas dependências. Em ciclos
        # A->B->A, isso evita que descritores de DTO observem apenas um
        # placeholder de Entity sem `pk_field`/`fields_map` resolvidos.
        with self._lock:
            namespace = self._ensure_namespace_module(entity_config_key)
            assert namespace.entities_dict is not None

            get_logger().debug(
                f"Executando o código da entidade {entity_resource} no namespace {entity_config_key}. Código:"
            )
            get_logger().debug(f"Entity source:\n{source_entity}")
            get_logger().debug(f"DTO source:\n{source_dto}")

            self._safe_exec(source_entity, namespace.entities_dict, "Entity source")

            # Em ciclo A->B->A, a dependência precisa ao menos enxergar o DTO
            # atual como placeholder para que o import dinâmico não falhe.
            if dto_class_name:
                self._ensure_dynamic_placeholder(dto_class_name, namespace.entities_dict)

        # Verificando se alguma de suas dependências precisariam ser carregadas (ou recarregadas)
        if not skip_dependency_load:
            for rd in relations_dependencies:
                if rd.entity_resource is None or rd.entity_scope is None:
                    raise RuntimeError(
                        f"Erro: Dependência de entidade mal formada na entidade {entity_resource}."
                    )

                try:
                    self.load_entity_source(
                        rd.entity_resource,
                        str(rd.tenant),
                        str(rd.grupo_empresarial),
                        rd.entity_scope,
                        _loading_chain=_loading_chain,
                    )
                except _CircularDependencyLoadException as exc:
                    # Em ciclo A->B->A, a dependência já está em processo de carga.
                    get_logger().debug(
                        f"Ciclo de dependência ignorado durante carregamento: {exc.loading_key}"
                    )
                    continue
                except MissingDependencyConfigException as exc:
                    # Preserva a causa original, atualizando o contexto da entidade atual.
                    raise MissingDependencyConfigException(
                        entity_resource=entity_resource,
                        dependency_resource=exc.dependency_resource,
                        dependency_scope=exc.dependency_scope,
                        dependency_tenant=exc.dependency_tenant,
                        dependency_grupo_empresarial=exc.dependency_grupo_empresarial,
                    ) from exc
                except MissingEntityConfigException as exc:
                    # Converte falha genérica da dependência para erro especializado.
                    raise MissingDependencyConfigException(
                        entity_resource=entity_resource,
                        dependency_resource=rd.entity_resource,
                        dependency_scope=rd.entity_scope,
                        dependency_tenant=rd.tenant,
                        dependency_grupo_empresarial=(
                            str(rd.grupo_empresarial)
                            if rd.grupo_empresarial
                            else None
                        ),
                    ) from exc

        # Carregando DTO e function types no namespace
        with self._lock:
            namespace = self._ensure_namespace_module(entity_config_key)
            assert namespace.entities_dict is not None

            if insert_function_code:
                self._safe_exec(
                    insert_function_code,
                    namespace.entities_dict,
                    "Insert Function source",
                )

            if update_function_code:
                self._safe_exec(
                    update_function_code,
                    namespace.entities_dict,
                    "Update Function source",
                )

            if get_function_code:
                self._safe_exec(
                    get_function_code,
                    namespace.entities_dict,
                    "Get FunctionType source",
                )

            if list_function_code:
                self._safe_exec(
                    list_function_code,
                    namespace.entities_dict,
                    "List FunctionType source",
                )

            if delete_function_code:
                self._safe_exec(
                    delete_function_code,
                    namespace.entities_dict,
                    "Delete FunctionType source",
                )

            dynamic_import_symbols = self._collect_dynamic_import_symbols(source_dto)
            for symbol in dynamic_import_symbols:
                self._ensure_dynamic_placeholder(symbol, namespace.entities_dict)

            # Autorreferencias podem nao gerar import; garantimos placeholder local para o proprio DTO.
            if dto_class_name:
                self._ensure_dynamic_placeholder(dto_class_name, namespace.entities_dict)

            self._safe_exec(source_dto, namespace.entities_dict, "DTO source")
            self._resolve_dynamic_placeholders(namespace.entities_dict)

            # Gravando a entidade no dict de entidades carregadas
            loaded_entity = LoadedEntity()
            loaded_entity.dto_class_name = dto_class_name
            loaded_entity.entity_class_name = entity_class_name
            loaded_entity.entity_hash = entity_hash
            loaded_entity.api_expose = api_expose
            loaded_entity.api_verbs = api_verbs
            loaded_entity.service_account = service_account
            loaded_entity.relations_dependencies = relations_dependencies
            loaded_entity.never_expire = from_disk
            loaded_entity.insert_function_class_name = insert_function_class_name
            loaded_entity.update_function_class_name = update_function_class_name
            loaded_entity.insert_function_name = insert_function_name
            loaded_entity.update_function_name = update_function_name
            loaded_entity.get_function_name = get_function_name
            loaded_entity.list_function_name = list_function_name
            loaded_entity.delete_function_name = delete_function_name
            loaded_entity.get_function_type_class_name = (
                get_function_type_class_name
            )
            loaded_entity.list_function_type_class_name = (
                list_function_type_class_name
            )
            loaded_entity.delete_function_type_class_name = (
                delete_function_type_class_name
            )
            loaded_entity.retrieve_after_insert = bool(retrieve_after_insert)
            loaded_entity.retrieve_after_update = bool(retrieve_after_update)
            loaded_entity.retrieve_after_partial_update = bool(
                retrieve_after_partial_update
            )
            loaded_entity.post_response_dto_class_name = (
                post_response_dto_class_name
            )
            loaded_entity.put_response_dto_class_name = (
                put_response_dto_class_name
            )
            loaded_entity.patch_response_dto_class_name = (
                patch_response_dto_class_name
            )
            loaded_entity.custom_json_post_response = bool(
                custom_json_post_response
            )
            loaded_entity.custom_json_put_response = bool(
                custom_json_put_response
            )
            loaded_entity.custom_json_patch_response = bool(
                custom_json_patch_response
            )
            loaded_entity.custom_json_get_response = bool(
                custom_json_get_response
            )
            loaded_entity.custom_json_list_response = bool(
                custom_json_list_response
            )
            loaded_entity.custom_json_delete_response = bool(
                custom_json_delete_response
            )

            namespace.loaded_entities[entity_resource] = loaded_entity

        return (
            dto_class_name,
            entity_class_name,
            namespace,
            api_expose,
            api_verbs,
            service_account,
            insert_function_class_name,
            update_function_class_name,
            insert_function_name,
            update_function_name,
            get_function_name,
            list_function_name,
            delete_function_name,
            get_function_type_class_name,
            list_function_type_class_name,
            delete_function_type_class_name,
            bool(retrieve_after_insert),
            bool(retrieve_after_update),
            bool(retrieve_after_partial_update),
            post_response_dto_class_name,
            put_response_dto_class_name,
            patch_response_dto_class_name,
            bool(custom_json_post_response),
            bool(custom_json_put_response),
            bool(custom_json_patch_response),
            bool(custom_json_get_response),
            bool(custom_json_list_response),
            bool(custom_json_delete_response),
        )

    def _collect_dynamic_import_symbols(self, source_code: str) -> set[str]:
        symbols: set[str] = set()
        pattern = re.compile(
            r"^from\s+dynamic\.[A-Za-z0-9_]+\s+import\s+([A-Za-z0-9_]+)",
            re.MULTILINE,
        )
        for match in pattern.finditer(source_code):
            symbols.add(match.group(1))
        return symbols

    def _ensure_namespace_module(self, entity_config_key: str) -> Namespace:
        self._ensure_dynamic_package()

        namespace = namespaces_dict.get(entity_config_key)
        if namespace is None:
            namespace = Namespace()
            namespace.key = entity_config_key
            namespaces_dict[entity_config_key] = namespace

        full_name = f"dynamic.{entity_config_key}"
        module = sys.modules.get(full_name)
        if not module:
            module = types.ModuleType(full_name)
            module.__package__ = "dynamic"
            module.__dict__["__builtins__"] = __builtins__
            sys.modules[full_name] = module

            parent = sys.modules["dynamic"]
            setattr(parent, entity_config_key, module)

        namespace.module = module
        namespace.entities_dict = module.__dict__
        return namespace

    def _ensure_dynamic_placeholder(self, symbol: str, context: dict[str, Any]) -> None:
        if not symbol or symbol in context:
            return

        base_type = None
        attrs: dict[str, Any] = {"__dynamic_placeholder__": True}
        if symbol.endswith("DTO"):
            base_type = DTOBase
            attrs.update(
                {
                    "resume_fields": set(),
                    "partition_fields": set(),
                    "fields_map": {},
                    "insert_function_field_lookup": {},
                    "update_function_field_lookup": {},
                    "get_function_field_lookup": {},
                    "list_function_field_lookup": {},
                    "delete_function_field_lookup": {},
                    "list_fields_map": {},
                    "integrity_check_fields_map": {},
                    "left_join_fields_map": {},
                    "left_join_fields_map_to_query": {},
                    "sql_join_fields_map": {},
                    "sql_join_fields_map_to_query": {},
                    "sql_read_only_fields": [],
                    "sql_no_update_fields": set(),
                    "object_fields_map": {},
                    "one_to_one_fields_map": {},
                    "field_filters_map": {},
                    "aggregator_fields_map": {},
                    "search_fields": set(),
                    "uniques": {},
                    "candidate_keys": [],
                    "fixed_filters": {},
                    "data_override_group": [],
                    "data_override_fields": [],
                    "pk_field": "id",
                }
            )
        elif symbol.endswith("Entity"):
            base_type = EntityBase

        if base_type is None:
            return

        context[symbol] = type(symbol, (base_type,), attrs)

    def _resolve_dynamic_placeholders(self, context: dict[str, Any]) -> None:
        def resolve_attr(target: Any, attr_name: str) -> Any:
            value = getattr(target, attr_name, None)
            if not isinstance(value, type):
                return None
            if not getattr(value, "__dynamic_placeholder__", False):
                return None

            resolved = context.get(value.__name__)
            if (
                isinstance(resolved, type)
                and not getattr(resolved, "__dynamic_placeholder__", False)
            ):
                setattr(target, attr_name, resolved)
                return resolved
            return None

        for obj in list(context.values()):
            if not isinstance(obj, type):
                continue
            if getattr(obj, "__dynamic_placeholder__", False):
                continue
            if not issubclass(obj, DTOBase):
                continue

            annotations = getattr(obj, "__annotations__", {})

            for field_name, descriptor in getattr(obj, "one_to_one_fields_map", {}).items():
                resolved_expected = resolve_attr(descriptor, "expected_type")
                if resolved_expected is not None:
                    annotations[field_name] = resolved_expected
                resolve_attr(descriptor, "entity_type")

            for map_name in ("list_fields_map", "object_fields_map", "left_join_fields_map"):
                for descriptor in getattr(obj, map_name, {}).values():
                    resolve_attr(descriptor, "dto_type")
                    resolve_attr(descriptor, "entity_type")

    def _safe_exec(self, source_code, context, description):
        try:
            exec(source_code, context)
        except Exception as e:
            get_logger().error(f"Error executing {description}: {e}")
            raise

    def _load_entity_config_from_redis(
        self,
        entity_resource: str,
        grupo_key: str,
        tenant_key: str,
        default_key: str,
        entity_config_key: str | None,
        escopo: str,
    ) -> tuple[str, str] | None:
        """
        Carrega a configuracao da entidade no Redis com fallback de namespace.

        Ordem de busca:
            1) entity_config_key informado
            2) grupo_key
            3) tenant_key
            4) default_key

        Args:
            entity_resource: Resource da entidade.
            grupo_key: Namespace de grupo empresarial.
            tenant_key: Namespace de tenant.
            default_key: Namespace default.
            entity_config_key: Namespace preferencial (quando conhecido).
            escopo: Escopo da entidade no Redis.

        Returns:
            Tupla (namespace_key, entity_config_json) quando encontrado.
            Retorna None quando nao existir no Redis.
        """
        if not EDLS_FROM_REDIS:
            return None

        from nsj_rest_lib2.redis_config import get_redis

        get_logger().debug(
            f"Procurando a configuração da entidade {entity_resource} no redis. Tenant key: {tenant_key} e Grupo key: {grupo_key}"
        )

        if entity_config_key is not None:
            entity_config_str = get_redis(
                "entity_config", escopo, entity_config_key, entity_resource
            )

        else:
            entity_config_key = grupo_key
            entity_config_str = get_redis(
                "entity_config", escopo, grupo_key, entity_resource
            )
            if entity_config_str is None:
                entity_config_key = tenant_key
                entity_config_str = get_redis(
                    "entity_config", escopo, tenant_key, entity_resource
                )
            if entity_config_str is None:
                entity_config_key = default_key
                entity_config_str = get_redis(
                    "entity_config", escopo, default_key, entity_resource
                )

        # Se não encontrar no redis, retorna None
        if entity_config_str is None:
            return None

        return (entity_config_key, entity_config_str)

    def _search_entity_namespace_in_memory(
        self,
        entity_resource: str,
        grupo_key: str,
        tenant_key: str,
        default_key: str,
    ) -> tuple[str, Namespace] | None:
        namespace = None
        entity_config_key = None

        # Pesquisando a entidade no namespace mais específico (grupo_empresarial)
        grupo_namespace = namespaces_dict.get(grupo_key)
        if grupo_namespace and entity_resource in grupo_namespace.loaded_entities:
            entity_config_key = grupo_key
            namespace = grupo_namespace

        # Pesquisando a entidade no namespace intermediário (tenant)
        tenant_namespace = namespaces_dict.get(tenant_key)
        if tenant_namespace and entity_resource in tenant_namespace.loaded_entities:
            entity_config_key = tenant_key
            namespace = tenant_namespace

        # Pesquisando a entidade no namespace padrão (default)
        default_namespace = namespaces_dict.get(default_key)
        if default_namespace and entity_resource in default_namespace.loaded_entities:
            entity_config_key = default_key
            namespace = default_namespace

        if namespace and entity_config_key:
            return (entity_config_key, namespace)
        else:
            return None

    def _evict_entity_from_memory(
        self,
        entity_resource: str,
        entity_config_key: str | None,
        grupo_key: str,
        tenant_key: str,
        default_key: str,
    ) -> None:
        """
        Remove a entidade carregada de todos os namespaces de memoria.

        Args:
            entity_resource: Resource da entidade.
            entity_config_key: Namespace originalmente utilizado (quando conhecido).
            grupo_key: Namespace de grupo empresarial.
            tenant_key: Namespace de tenant.
            default_key: Namespace default.

        Returns:
            None.
        """
        # Remove a entidade de todos os namespaces possíveis para evitar
        # reaproveitamento de código dinâmico obsoleto.
        keys = [grupo_key, tenant_key, default_key]
        if entity_config_key:
            keys.insert(0, entity_config_key)

        for key in keys:
            namespace = namespaces_dict.get(key)
            if namespace is None:
                continue
            namespace.loaded_entities.pop(entity_resource, None)
