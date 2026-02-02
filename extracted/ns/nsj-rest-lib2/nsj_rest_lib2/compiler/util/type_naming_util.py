import hashlib
import uuid
from typing import Iterable, Iterator, Optional

from nsj_rest_lib2.compiler.model import CompilerResult
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil


def compile_namespace_keys(
    tenant: str | int | None, grupo_empresarial: str | uuid.UUID | None
) -> tuple[str, str, str]:
    grupo_key = f"tenant_{tenant}.ge_{grupo_empresarial}"
    tenant_key = f"tenant_{tenant}"
    default_key = "default"

    return (grupo_key, tenant_key, default_key)


def resolve_namespace_key(
    tenant: str | int | None, grupo_empresarial: str | uuid.UUID | None
) -> str:
    grupo_key, tenant_key, default_key = compile_namespace_keys(
        tenant,
        grupo_empresarial,
    )

    if (
        tenant
        and tenant != 0
        and grupo_empresarial
        and str(grupo_empresarial) != "00000000-0000-0000-0000-000000000000"
    ):
        return grupo_key
    if tenant and tenant != 0:
        return tenant_key
    return default_key


def build_entity_hash(compiler_result: CompilerResult) -> str:
    hasher = hashlib.sha256()

    for content in _iter_hash_chunks(
        compiler_result.dto_code,
        compiler_result.entity_code,
        compiler_result.insert_function_name,
        compiler_result.update_function_name,
        compiler_result.get_function_name,
        compiler_result.list_function_name,
        compiler_result.delete_function_name,
        compiler_result.source_insert_function,
        compiler_result.source_update_function,
        compiler_result.source_get_function_type,
        compiler_result.source_list_function_type,
        compiler_result.source_delete_function_type,
        compiler_result.post_response_dto_class_name,
        compiler_result.put_response_dto_class_name,
        compiler_result.patch_response_dto_class_name,
        str(compiler_result.retrieve_after_insert),
        str(compiler_result.retrieve_after_update),
        str(compiler_result.retrieve_after_partial_update),
        str(compiler_result.custom_json_post_response),
        str(compiler_result.custom_json_put_response),
        str(compiler_result.custom_json_patch_response),
        str(compiler_result.custom_json_get_response),
        str(compiler_result.custom_json_list_response),
        str(compiler_result.custom_json_delete_response),
        compiler_result.service_account,
    ):
        hasher.update(content)

    return hasher.hexdigest()


def _iter_hash_chunks(*chunks: Optional[str]) -> Iterator[bytes]:
    for chunk in chunks:
        if chunk:
            yield chunk.encode("utf-8")


def compile_dto_class_name(entity_id: str, prefx_class_name: str = "") -> str:
    return f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}{CompilerStrUtil.to_pascal_case(entity_id)}DTO"


def compile_response_dto_class_name(
    entity_id: str, prefx_class_name: str, verb: str
) -> str:
    verb = (verb or "").lower()
    suffix_map = {
        "post": "PostResponseDTO",
        "put": "PutResponseDTO",
        "patch": "PatchResponseDTO",
    }
    suffix = suffix_map.get(
        verb, f"{CompilerStrUtil.to_pascal_case(verb)}ResponseDTO"
    )
    return (
        f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}"
        f"{CompilerStrUtil.to_pascal_case(entity_id)}"
        f"{suffix}"
    )


def compile_entity_class_name(entity_id: str, prefx_class_name: str = "") -> str:
    return f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}{CompilerStrUtil.to_pascal_case(entity_id)}Entity"


def compile_function_class_name(
    entity_id: str,
    prefx_class_name: str,
    path_parts: Iterable[str],
    operation: str,
) -> str:
    """
    Gera o nome da classe para FunctionTypes (insert/update),
    incorporando o caminho dos relacionamentos (quando houver).
    """

    operation = (operation or "").lower()
    suffix_map = {
        "insert": "InsertType",
        "update": "UpdateType",
        "get": "GetType",
        "list": "ListType",
        "delete": "DeleteType",
    }
    suffix = suffix_map.get(
        operation, f"{CompilerStrUtil.to_pascal_case(operation)}Type"
    )
    path_suffix = "".join(CompilerStrUtil.to_pascal_case(part) for part in path_parts)
    return (
        f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}"
        f"{CompilerStrUtil.to_pascal_case(entity_id)}"
        f"{path_suffix}"
        f"{suffix}"
    )


def compile_function_params_dto_class_name(
    entity_id: str,
    prefx_class_name: str,
    verb: str,
) -> str:
    """
    Gera o nome da classe DTO usada como envelope de parâmetros para funções
    de GET, LIST e DELETE.
    """

    verb = (verb or "").lower()
    if verb == "get":
        suffix = "GetParamsDTO"
    elif verb == "list":
        suffix = "ListParamsDTO"
    elif verb == "delete":
        suffix = "DeleteParamsDTO"
    else:
        suffix = f"{CompilerStrUtil.to_pascal_case(verb)}ParamsDTO"

    return (
        f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}"
        f"{CompilerStrUtil.to_pascal_case(entity_id)}"
        f"{suffix}"
    )
