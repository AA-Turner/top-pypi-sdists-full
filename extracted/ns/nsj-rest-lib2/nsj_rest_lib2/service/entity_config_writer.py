from __future__ import annotations

import json
from typing import Any, Dict

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.model import CompilerResult
from nsj_rest_lib2.compiler.util.type_naming_util import (
    build_entity_hash,
    resolve_namespace_key,
)
from nsj_rest_lib2.redis_config import set_redis
from nsj_rest_lib2.settings import ESCOPO_RESTLIB2


class EntityConfigWriter:
    """
    Serializa o resultado da compilacao e publica no Redis usando o mesmo
    layout consumido pelo EntityLoader.
    """

    def __init__(self, escopo: str = ESCOPO_RESTLIB2) -> None:
        self._escopo = escopo or ESCOPO_RESTLIB2

    def publish(
        self,
        entity_model: EntityModelBase,
        compiler_result: CompilerResult,
        *,
        entity_hash: str | None = None,
    ) -> Dict[str, Any]:
        """
        Serializa e grava o resultado da compilacao no Redis.

        Args:
            entity_model: Modelo EDL ja validado.
            compiler_result: Resultado retornado pelo compilador.
            entity_hash: Hash da versao compilada. Quando None, e calculado.

        Returns:
            Payload serializado (util para inspecao/testes).
        """
        payload = self.build_payload(
            entity_model, compiler_result, entity_hash=entity_hash
        )
        namespace_key = self._resolve_namespace_key(entity_model)
        resource = self._resolve_resource(entity_model)

        set_redis(
            "entity_config",
            self._escopo,
            namespace_key,
            resource,
            json.dumps(payload, ensure_ascii=False),
        )

        return payload

    def build_payload(
        self,
        entity_model: EntityModelBase,
        compiler_result: CompilerResult,
        *,
        entity_hash: str | None = None,
    ) -> Dict[str, Any]:
        """
        Constroi o dicionario serializavel da entidade compilada.

        Args:
            entity_model: Modelo EDL ja validado.
            compiler_result: Resultado retornado pelo compilador.
            entity_hash: Hash da versao compilada. Quando None, e calculado.

        Returns:
            Dicionario pronto para ser persistido em `entity_config`.
        """
        resource = self._resolve_resource(entity_model)
        relations = [rd.to_dict() for rd in (compiler_result.relations_dependencies or [])]

        return {
            "dto_class_name": compiler_result.dto_class_name,
            "entity_class_name": compiler_result.entity_class_name,
            "lut": bool(getattr(entity_model, "lut", False)),
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
            "entity_hash": entity_hash
            if entity_hash is not None
            else self._build_entity_hash(compiler_result),
            "api_expose": compiler_result.api_expose,
            "api_resource": resource,
            "api_verbs": compiler_result.api_verbs or [],
            "relations_dependencies": relations,
        }

    def _resolve_namespace_key(self, entity_model: EntityModelBase) -> str:
        """
        Resolve a chave de namespace com tenant e grupo empresarial.

        Args:
            entity_model: Modelo da entidade compilada.

        Returns:
            Namespace key no padrao usado pelo loader.
        """
        tenant = getattr(entity_model, "tenant", None)
        grupo_empresarial = getattr(entity_model, "grupo_empresarial", None)

        return resolve_namespace_key(tenant, grupo_empresarial)

    def _resolve_resource(self, entity_model: EntityModelBase) -> str:
        """
        Resolve o resource HTTP declarado no bloco `api`.

        Args:
            entity_model: Modelo da entidade compilada.

        Returns:
            Nome do resource da API dinamica.

        Raises:
            ValueError: Quando o modelo nao possui bloco `api.resource`.
        """
        if not isinstance(entity_model, EntityModel) or not entity_model.api:
            raise ValueError(
                "EntityModel precisa possuir bloco de API para publicacao no Redis."
            )
        if not entity_model.api.resource:
            raise ValueError("api.resource e obrigatorio para publicacao no Redis.")
        return entity_model.api.resource

    def _build_entity_hash(self, compiler_result: CompilerResult) -> str:
        """
        Gera hash deterministico da configuracao compilada.

        Args:
            compiler_result: Resultado retornado pelo compilador.

        Returns:
            Hash SHA-256 da entidade compilada.
        """
        return build_entity_hash(compiler_result)
