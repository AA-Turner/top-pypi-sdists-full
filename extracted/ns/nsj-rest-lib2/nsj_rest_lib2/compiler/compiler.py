from typing import Any

from nsj_rest_lib2.compiler.compiler_structures import (
    ComponentsCompilerStructure,
    IndexCompilerStructure,
    PropertiesCompilerStructure,
)
from nsj_rest_lib2.compiler.dto_compiler import DTOCompiler
from nsj_rest_lib2.compiler.function_insert_update_compiler import (
    FunctionInsertUpdateCompiler,
    inject_function_bindings,
)
from nsj_rest_lib2.compiler.function_get_delete_compiler import (
    FunctionGetDeleteCompiler,
)
from nsj_rest_lib2.compiler.function_model import (
    FunctionBindingConfig,
    FunctionCompilationOutput,
)
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.entity_model_root import EntityModelRoot
from nsj_rest_lib2.compiler.entity_compiler import EntityCompiler
from nsj_rest_lib2.compiler.model import CompilerResult, RelationDependency
from nsj_rest_lib2.compiler.property_compiler import EDLPropertyCompiler

from nsj_rest_lib2.compiler.util.type_naming_util import (
    compile_dto_class_name,
    compile_entity_class_name,
    compile_namespace_keys,
)
from nsj_rest_lib2.compiler.response_dto_compiler import ResponseDTOCompiler
from nsj_rest_lib2.compiler.util.relation_ref import RelationRefParser

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel

from nsj_rest_lib2.settings import get_logger
from nsj_rest_lib2.dto.escopo_dto import EscopoDTO


class EDLCompiler:
    def __init__(self) -> None:
        self._properties_compiler = EDLPropertyCompiler()
        self._dto_compiler = DTOCompiler()
        self._entity_compiler = EntityCompiler()
        self._function_compiler = FunctionInsertUpdateCompiler()
        self._function_get_delete_compiler = FunctionGetDeleteCompiler()

    def compile_models(
        self,
        entity_models: dict[str, EntityModel],
        escopos: dict[str, EscopoDTO],
    ) -> list[CompilerResult]:

        compiler_results = []
        for entity_model_id in entity_models:
            entity_model = entity_models[entity_model_id]
            escopo_dto = escopos.get(entity_model.escopo)
            if escopo_dto is None:
                raise Exception(
                    f"EscopoDTO não informado para o escopo: {entity_model.escopo}."
                )
            compiler_result = self._compile_model(
                entity_model,
                entity_models,
                escopo=escopo_dto,
            )
            if compiler_result:
                compiler_results.append(compiler_result)

        return compiler_results

    def compile_model_from_edl(
        self,
        edl_json: dict[str, Any],
        dependencies_edls: list[dict[str, Any]],
        escopo: EscopoDTO,
    ) -> CompilerResult | None:
        entity_model = EntityModel(**edl_json)

        entity_models = []
        for dependency_edl in dependencies_edls:
            if "mixin" in dependency_edl and dependency_edl["mixin"]:
                dependency_entity_model = EntityModelRoot(**dependency_edl)
            else:
                dependency_entity_model = EntityModel(**dependency_edl)
            entity_models.append(dependency_entity_model)

        return self.compile_model(entity_model, entity_models, escopo=escopo)

    def compile_model(
        self,
        entity_model: EntityModelBase,
        dependencies_models: list[tuple[str, EntityModelBase]],
        escopo: EscopoDTO,
    ) -> CompilerResult | None:
        entity_models = {}
        for dependency_entity_model in dependencies_models:
            complete_entity_id = dependency_entity_model[0]
            entity_models[complete_entity_id] = dependency_entity_model[1]

        return self._compile_model(entity_model, entity_models, escopo=escopo)

    def _compile_model(
        self,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        escopo: EscopoDTO | None,
        prefx_class_name: str = "",
    ) -> CompilerResult | None:
        if entity_model.mixin:
            return None

        if escopo is None:
            raise Exception(
                f"EscopoDTO não informado para a entidade: {getattr(entity_model, 'id', '<unknown>')}."
            )
        escopo_codigo = escopo.codigo

        # Tratando dos dados base para a extensão parcial
        partial_metadata: dict[str, str] | None = None
        partial_base_model: EntityModel | None = None
        if isinstance(entity_model, EntityModel) and entity_model.partial_of:
            if entity_model.partial_of not in entity_models:
                raise Exception(
                    f"Entidade base '{entity_model.partial_of}' não encontrada para a extensão parcial '{entity_model.id}'."
                )

            base_model_candidate = entity_models[entity_model.partial_of]
            if not isinstance(base_model_candidate, EntityModel):
                raise Exception(
                    f"Entidade base '{entity_model.partial_of}' da extensão parcial '{entity_model.id}' é inválida."
                )

            self._validate_partial_model(
                entity_model, base_model_candidate, entity_models
            )
            partial_metadata = self._build_partial_metadata(
                entity_model, base_model_candidate
            )
            partial_base_model = base_model_candidate

        # Criando um mapa de índices por nome de property
        # TODO Implementar tratamento dos índices de apoio às query (não de unicidade)
        map_indexes_by_property: dict[str, list[IndexCompilerStructure]] = {}
        map_unique_by_property: dict[str, IndexCompilerStructure] = {}
        self._make_unique_map_by_property(
            map_indexes_by_property, map_unique_by_property, entity_model, entity_models
        )

        # Criando uma cópia das coleções necessárias à compilação das properties
        # (a ideia é ser possível alterar as coleções sem afetar a entidade modelo,
        # o que será necessário para o tratamento de traits, etc - os quais serão
        # uma classe nova, resultado da união dessas propriedades).
        properties_structure = PropertiesCompilerStructure()
        self._make_properties_structures(
            properties_structure, entity_model, entity_models
        )

        function_bindings = FunctionBindingConfig()
        insert_output = FunctionCompilationOutput()
        update_output = FunctionCompilationOutput()
        insert_function_code = ""
        update_function_code = ""
        get_function_code = ""
        list_function_code = ""
        delete_function_code = ""
        get_function_type_class = None
        list_function_type_class = None
        delete_function_type_class = None
        get_function_name = None
        list_function_name = None
        delete_function_name = None
        handlers: dict[str, Any] = {}
        post_handler = None
        put_handler = None
        patch_handler = None

        if isinstance(entity_model, EntityModel) and entity_model.api:
            if entity_model.api.handlers:
                handlers = {
                    (verb or "").lower(): handler
                    for verb, handler in entity_model.api.handlers.items()
                    if handler
                }

            post_handler = handlers.get("post")
            put_handler = handlers.get("put")
            patch_handler = handlers.get("patch")

            insert_output = self._function_compiler.compile_insert(
                entity_model,
                properties_structure,
                post_handler,
                prefx_class_name,
            )
            update_output = self._function_compiler.compile_update(
                entity_model,
                properties_structure,
                put_handler,
                prefx_class_name,
            )
            get_handler = handlers.get("get")
            list_handler = handlers.get("list")
            delete_handler = handlers.get("delete")

            get_function_name = get_handler.function_ref if get_handler else None
            list_function_name = list_handler.function_ref if list_handler else None
            delete_function_name = (
                delete_handler.function_ref if delete_handler else None
            )

            inject_function_bindings(
                function_bindings,
                insert_output,
                update_output,
            )

            if insert_output.code:
                insert_function_code += insert_output.code + "\n\n"
            if update_output.code:
                update_function_code += update_output.code + "\n\n"

            # Gerando FunctionTypes para GET/LIST/DELETE (quando configuradas)
            get_output = self._function_get_delete_compiler.compile(
                entity_model,
                properties_structure,
                get_handler,
                prefx_class_name,
                verb="get",
            )
            if get_output.class_name and get_output.code:
                get_function_type_class = get_output.class_name
                get_function_code = get_output.code
            if get_output.function_name:
                get_function_name = get_output.function_name

            list_output = self._function_get_delete_compiler.compile(
                entity_model,
                properties_structure,
                list_handler,
                prefx_class_name,
                verb="list",
            )
            if list_output.class_name and list_output.code:
                list_function_type_class = list_output.class_name
                list_function_code = list_output.code
            if list_output.function_name:
                list_function_name = list_output.function_name

            delete_output = self._function_get_delete_compiler.compile(
                entity_model,
                properties_structure,
                delete_handler,
                prefx_class_name,
                verb="delete",
            )
            if delete_output.class_name and delete_output.code:
                delete_function_type_class = delete_output.class_name
                delete_function_code = delete_output.code
            if delete_output.function_name:
                delete_function_name = delete_output.function_name

        # Criando a lista de atributos do DTO e da Entity; e recuperando as chaves primarias
        (
            ast_dto_attributes,
            ast_entity_attributes,
            props_pk,
            aux_classes,
            related_imports,
            relations_dependencies,
            fixed_filters,
        ) = self._properties_compiler.compile(
            properties_structure,
            map_unique_by_property,
            escopo_codigo,
            entity_model,
            entity_models,
            prefx_class_name,
            function_bindings=function_bindings,
        )

        # Adicionando os imports da extensão parcial
        if partial_metadata:
            related_imports.append(
                (
                    partial_metadata["module"],
                    partial_metadata["dto_class"],
                    partial_metadata["entity_class"],
                )
            )

        related_imports = self._deduplicate_related_imports(related_imports)

        # Gerando o buffer para os códigos de DTO e Entity
        dto_code = ""
        entity_code = ""
        relations_dependencies_complete = []

        # Carregando a estrutura de compilação dos components
        components_structure = ComponentsCompilerStructure()
        self._make_components_structures(
            components_structure, entity_model, entity_models
        )

        # Gerando o código das entidades filhas (components)
        for component_key in components_structure.components:
            component = components_structure.components[component_key]
            component_compiled = self._compile_model(
                component,
                entity_models,
                escopo,
                prefx_class_name=f"{prefx_class_name}_{entity_model.id}",
            )

            if not component_compiled:
                raise Exception(
                    f"Erro ao compilar o component '{component_key}' da entidade '{entity_model.id}'. Gerou saída None, como se fosse um mixin."
                )

            # Guardando o código gerado no buffer
            if component_compiled.dto_code:
                dto_code += component_compiled.dto_code + "\n\n"
            if component_compiled.entity_code:
                entity_code += component_compiled.entity_code + "\n\n"
            if component_compiled.relations_dependencies:
                relations_dependencies_complete.extend(
                    component_compiled.relations_dependencies
                )
            if component_compiled.source_insert_function:
                insert_function_code += (
                    component_compiled.source_insert_function + "\n\n"
                )
            if component_compiled.source_update_function:
                update_function_code += (
                    component_compiled.source_update_function + "\n\n"
                )

        # Gerando o código do DTO
        dto_class_name, code_dto = self._dto_compiler.compile(
            entity_model,
            ast_dto_attributes,
            aux_classes,
            related_imports,
            fixed_filters,
            prefx_class_name,
            partial_metadata,
        )

        # Gerando o código da Entity
        entity_class_name, code_entity = self._entity_compiler.compile(
            entity_model,
            ast_entity_attributes,
            props_pk,
            prefx_class_name,
            partial_metadata,
        )

        # Extendendo os buffers com os códigos gerados
        dto_code += code_dto
        entity_code += code_entity

        # Adicionando as dependências das relações
        relations_dependencies_complete.extend(relations_dependencies)

        response_dto_compiler = ResponseDTOCompiler(
            dto_compiler=self._dto_compiler,
            entity_model=entity_model,
            prefx_class_name=prefx_class_name,
            ast_dto_attributes=ast_dto_attributes,
            aux_classes=aux_classes,
            related_imports=related_imports,
            fixed_filters=fixed_filters,
        )

        # Adicionando as dependências da extensão parcial
        if partial_metadata and partial_base_model:
            relation_dependency = RelationDependency()
            if not partial_base_model.api or not partial_base_model.api.resource:
                raise Exception(
                    f"Entidade base '{partial_base_model.id}' não possui configuração de API necessária para extensão parcial."
                )
            relation_dependency.entity_resource = partial_base_model.api.resource
            relation_dependency.entity_scope = partial_base_model.escopo
            relation_dependency.tenant = partial_base_model.tenant
            relation_dependency.grupo_empresarial = partial_base_model.grupo_empresarial
            relations_dependencies_complete.append(relation_dependency)

        post_expected = "empty"
        put_expected = "empty"
        patch_expected = "empty"
        get_expected = "empty"
        list_expected = "empty"
        delete_expected = "empty"
        post_properties = None
        put_properties = None
        patch_properties = None
        if isinstance(entity_model, EntityModel) and entity_model.api:
            post_expected, post_properties = (
                response_dto_compiler.handler_result_details(post_handler)
            )
            put_expected, put_properties = (
                response_dto_compiler.handler_result_details(put_handler)
            )
            patch_expected, patch_properties = (
                response_dto_compiler.handler_result_details(patch_handler)
            )
            get_expected, _ = response_dto_compiler.handler_result_details(
                get_handler
            )
            list_expected, _ = response_dto_compiler.handler_result_details(
                list_handler
            )
            delete_expected, _ = response_dto_compiler.handler_result_details(
                delete_handler
            )

        if post_expected == "partial_row":
            post_class_name, post_code = (
                response_dto_compiler.compile_partial_response_dto(
                    "post", post_properties or []
                )
            )
            compiler_result_post_class = post_class_name
            dto_code += "\n\n" + post_code
        else:
            compiler_result_post_class = None

        if put_expected == "partial_row":
            put_class_name, put_code = (
                response_dto_compiler.compile_partial_response_dto(
                    "put", put_properties or []
                )
            )
            compiler_result_put_class = put_class_name
            dto_code += "\n\n" + put_code
        else:
            compiler_result_put_class = None

        if patch_expected == "partial_row":
            patch_class_name, patch_code = (
                response_dto_compiler.compile_partial_response_dto(
                    "patch", patch_properties or []
                )
            )
            compiler_result_patch_class = patch_class_name
            dto_code += "\n\n" + patch_code
        else:
            compiler_result_patch_class = None

        # Construindo o resultado
        compiler_result = CompilerResult()
        compiler_result.entity_class_name = entity_class_name
        compiler_result.entity_code = entity_code
        compiler_result.dto_class_name = dto_class_name
        compiler_result.dto_code = dto_code
        compiler_result.relations_dependencies = relations_dependencies_complete
        compiler_result.insert_function_class_name = insert_output.class_name
        compiler_result.insert_function_name = insert_output.function_name
        compiler_result.update_function_class_name = update_output.class_name
        compiler_result.update_function_name = update_output.function_name
        compiler_result.get_function_name = get_function_name
        compiler_result.list_function_name = list_function_name
        compiler_result.delete_function_name = delete_function_name
        compiler_result.get_function_type_class_name = get_function_type_class
        compiler_result.list_function_type_class_name = list_function_type_class
        compiler_result.delete_function_type_class_name = delete_function_type_class
        compiler_result.source_get_function_type = get_function_code.strip() or None
        compiler_result.source_list_function_type = list_function_code.strip() or None
        compiler_result.source_delete_function_type = (
            delete_function_code.strip() or None
        )
        compiler_result.retrieve_after_insert = post_expected == "entity_row"
        compiler_result.retrieve_after_update = put_expected == "entity_row"
        compiler_result.retrieve_after_partial_update = (
            patch_expected == "entity_row"
        )
        compiler_result.post_response_dto_class_name = compiler_result_post_class
        compiler_result.put_response_dto_class_name = compiler_result_put_class
        compiler_result.patch_response_dto_class_name = (
            compiler_result_patch_class
        )
        compiler_result.custom_json_post_response = (
            post_expected == "custom_json"
        )
        compiler_result.custom_json_put_response = (
            put_expected == "custom_json"
        )
        compiler_result.custom_json_patch_response = (
            patch_expected == "custom_json"
        )
        compiler_result.custom_json_get_response = (
            get_expected == "custom_json"
        )
        compiler_result.custom_json_list_response = (
            list_expected == "custom_json"
        )
        compiler_result.custom_json_delete_response = (
            delete_expected == "custom_json"
        )

        insert_code_compiled = insert_function_code.strip()
        update_code_compiled = update_function_code.strip()
        compiler_result.source_insert_function = (
            insert_code_compiled if insert_code_compiled else None
        )
        compiler_result.source_update_function = (
            update_code_compiled if update_code_compiled else None
        )

        # Compilando questões das APIs
        if isinstance(entity_model, EntityModel):
            compiler_result.api_expose = entity_model.api.expose
            compiler_result.api_resource = entity_model.api.resource
            compiler_result.api_verbs = entity_model.api.verbs
        compiler_result.service_account = escopo.service_account

        get_logger().debug(f"código gerado para a entidade: {entity_model.id}")
        get_logger().debug("DTO Code:")
        get_logger().debug(f"\n{dto_code}")
        get_logger().debug("Entity Code:")
        get_logger().debug(f"\n{entity_code}")

        return compiler_result

    def _validate_partial_model(
        self,
        partial_model: EntityModel,
        base_model: EntityModel,
        entity_models: dict[str, EntityModel],
    ) -> None:
        base_properties_structure = PropertiesCompilerStructure()
        self._make_properties_structures(
            base_properties_structure,
            base_model,
            entity_models,
        )
        aggregated_base_properties = set(base_properties_structure.properties.keys())

        duplicated_properties = aggregated_base_properties.intersection(
            set(partial_model.properties.keys())
        )
        if duplicated_properties:
            raise Exception(
                f"Extensão parcial '{partial_model.id}' redefine propriedades da entidade base '{base_model.id}': {sorted(duplicated_properties)}."
            )

        lists_to_check = {
            "required": partial_model.required,
            "main_properties": partial_model.main_properties,
            "partition_data": partial_model.partition_data,
            "search_properties": partial_model.search_properties,
            "metric_label": partial_model.metric_label,
        }

        for list_name, values in lists_to_check.items():
            if not values:
                continue

            conflicts = [
                value
                for value in values
                if isinstance(value, str) and value in aggregated_base_properties
            ]
            if conflicts:
                raise Exception(
                    f"Extensão parcial '{partial_model.id}' utiliza propriedades da entidade base '{base_model.id}' em '{list_name}': {conflicts}."
                )

        link = partial_model.repository.link_to_base
        if not link:
            raise Exception(
                f"Extensão parcial '{partial_model.id}' requer configuração 'link_to_base' no bloco 'repository'."
            )

        if not link.base_property:
            raise Exception(
                f"Extensão parcial '{partial_model.id}' requer 'base_property' definido em 'link_to_base'."
            )

        if not link.column:
            raise Exception(
                f"Extensão parcial '{partial_model.id}' requer 'column' definido em 'link_to_base'."
            )

        if link.base_property not in aggregated_base_properties:
            raise Exception(
                f"'base_property' '{link.base_property}' não corresponde a uma propriedade da entidade base '{base_model.id}'."
            )

        # if not base_model.api or not base_model.api.resource:
        #     raise Exception(
        #         f"Entidade base '{base_model.id}' não possui configuração de API compatível com extensões parciais."
        #     )

    def _build_partial_metadata(
        self, partial_model: EntityModel, base_model: EntityModel
    ) -> dict[str, str]:
        link = partial_model.repository.link_to_base
        if link is None:
            raise Exception(
                f"Extensão parcial '{partial_model.id}' está sem configuração 'link_to_base'."
            )

        grupo_key, tenant_key, default_key = compile_namespace_keys(
            base_model.tenant, base_model.grupo_empresarial
        )
        namespace = self._resolve_namespace_key(
            base_model.tenant,
            base_model.grupo_empresarial,
            grupo_key,
            tenant_key,
            default_key,
        )

        return {
            "module": namespace,
            "dto_class": compile_dto_class_name(base_model.id),
            "entity_class": compile_entity_class_name(base_model.id),
            "relation_field": link.column,
            "related_entity_field": link.base_property,
        }

    def _resolve_namespace_key(
        self,
        tenant: str | int | None,
        grupo_empresarial,
        grupo_key: str,
        tenant_key: str,
        default_key: str,
    ) -> str:
        has_tenant = tenant not in (None, 0, "0")
        has_grupo = (
            grupo_empresarial
            and str(grupo_empresarial) != "00000000-0000-0000-0000-000000000000"
        )

        if has_tenant and has_grupo:
            return grupo_key
        if has_tenant:
            return tenant_key
        return default_key

    def _deduplicate_related_imports(
        self, related_imports: list[tuple[str, str, str]]
    ) -> list[tuple[str, str, str]]:
        deduped: list[tuple[str, str, str]] = []
        seen: set[tuple[str, str, str]] = set()

        for import_tuple in related_imports:
            if import_tuple in seen:
                continue
            seen.add(import_tuple)
            deduped.append(import_tuple)

        return deduped

    def _make_components_structures(
        self,
        components_structure: ComponentsCompilerStructure,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
    ):
        if not entity_model:
            return

        # Populando com os components da superclasse (extends)
        if entity_model.extends:
            super_model = entity_models[entity_model.extends]

            self._make_components_structures(
                components_structure,
                super_model,
                entity_models,
            )

        # Populando com os components do trait
        if entity_model.trait_from:
            trait_model = entity_models[entity_model.trait_from]

            self._make_components_structures(
                components_structure,
                trait_model,
                entity_models,
            )

        # Populando com os components da entidade atual
        if entity_model.components:
            components_structure.components.update(entity_model.components)

    def _make_properties_structures(
        self,
        properties_structure: PropertiesCompilerStructure,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        relation_type: str = "self",
    ):
        if not entity_model:
            return

        # Populando com as propriedades dos mixins
        if entity_model.mixins:
            for mixin_id in entity_model.mixins:
                if mixin_id not in entity_models:
                    raise Exception(f"Mixin '{mixin_id}' não encontrado.")

                mixin_model = entity_models[mixin_id]
                self._make_properties_structures(
                    properties_structure,
                    mixin_model,
                    entity_models,
                    relation_type="mixin",
                )

        # Populando com as propriedades da superclasse (extends)
        if entity_model.extends:
            super_model = entity_models[entity_model.extends]

            self._make_properties_structures(
                properties_structure,
                super_model,
                entity_models,
                relation_type="extends",
            )

        # Populando com as propriedades do trait
        if entity_model.trait_from:
            trait_model = entity_models[entity_model.trait_from]

            self._make_properties_structures(
                properties_structure,
                trait_model,
                entity_models,
                relation_type="trait",
            )

        # Populando com as propriedades da entidade atual
        properties_structure.properties.update(entity_model.properties)
        for prop_name in entity_model.properties or {}:
            # Preferimos não sobrescrever quando já marcado como 'self'
            if (
                prop_name not in properties_structure.property_origins
                or relation_type == "self"
            ):
                properties_structure.property_origins[prop_name] = relation_type
        if entity_model.main_properties:
            for main_property in entity_model.main_properties:
                if not isinstance(main_property, str):
                    continue

                if "/" in main_property:
                    path_parts = [
                        part.strip() for part in main_property.split("/") if part
                    ]
                    if len(path_parts) < 2 or not path_parts[0]:
                        raise Exception(
                            f"Propriedade resumo inválida '{main_property}' na entidade '{entity_model.id}'."
                        )

                    relation_name = path_parts[0]
                    resume_path_parts = path_parts[1:]
                    resume_field = ".".join(resume_path_parts)

                    if relation_name not in properties_structure.main_properties:
                        properties_structure.main_properties.append(relation_name)

                    resume_fields = properties_structure.main_resume_fields.setdefault(
                        relation_name, []
                    )

                    if resume_field and resume_field not in resume_fields:
                        resume_fields.append(resume_field)
                else:
                    if main_property not in properties_structure.main_properties:
                        properties_structure.main_properties.append(main_property)
        if entity_model.required:
            properties_structure.required.extend(entity_model.required)
        if entity_model.partition_data:
            properties_structure.partition_data.extend(entity_model.partition_data)
        if entity_model.search_properties:
            properties_structure.search_properties.extend(
                entity_model.search_properties
            )
        if entity_model.metric_label:
            properties_structure.metric_label.extend(entity_model.metric_label)

        if entity_model.trait_properties:
            properties_structure.trait_properties.update(entity_model.trait_properties)

        if entity_model.extends_properties:
            properties_structure.extends_properties.update(
                entity_model.extends_properties
            )

        if entity_model.composed_properties:
            properties_structure.composed_properties.update(
                entity_model.composed_properties
            )

        if entity_model.repository.properties:
            properties_structure.entity_properties.update(
                entity_model.repository.properties
            )

    def _make_unique_map_by_property(
        self,
        map_indexes_by_property: dict[str, list[IndexCompilerStructure]],
        map_unique_by_property: dict[str, IndexCompilerStructure],
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        deep: int = 1,
    ):

        if not entity_model:
            return

        # Populando com as uniques da superclasse (extends)
        if entity_model.extends:
            super_model = entity_models[entity_model.extends]

            self._make_unique_map_by_property(
                map_indexes_by_property,
                map_unique_by_property,
                super_model,
                entity_models,
                deep=deep + 1,
            )

        # Populando com as uniques do trait
        if entity_model.trait_from:
            trait_model = entity_models[entity_model.trait_from]

            self._make_unique_map_by_property(
                map_indexes_by_property,
                map_unique_by_property,
                trait_model,
                entity_models,
                deep=deep + 1,
            )

        # Varrendo e organizando os índices
        if entity_model.repository.indexes:
            for index in entity_model.repository.indexes:
                for pkey in index.columns:
                    if index.unique:
                        if pkey in map_unique_by_property:
                            if deep > 1:
                                get_logger().warning(
                                    f"Propriedade '{pkey}' possui mais de um índice de unicidade (sendo um herdado). Por isso a replicação (herdada) será ignorada."
                                )
                                continue
                            else:
                                raise Exception(
                                    f"Propriedade '{pkey}' possui mais de um índice de unicidade."
                                )  # TODO Verificar esse modo de tratar erros

                        map_unique_by_property[pkey] = IndexCompilerStructure(
                            index, deep > 1
                        )
                    else:
                        list_index = map_indexes_by_property.setdefault(pkey, [])
                        list_index.append(IndexCompilerStructure(index, deep > 1))

    def list_dependencies(
        self, edl_json: dict[str, Any]
    ) -> tuple[list[str], EntityModelBase]:
        if edl_json.get("mixin", False):
            entity_model = EntityModelRoot(**edl_json)
        else:
            entity_model = EntityModel(**edl_json)

        return (self._list_dependencies(entity_model), entity_model)

    def _list_dependencies(self, entity_model: EntityModelBase) -> list[str]:
        entities: list[str] = []

        # Adicionando dependências por mixins
        if entity_model.mixins:
            entities.extend(entity_model.mixins)

        # Adicionando dependências por traits
        if entity_model.extends:
            entities.append(entity_model.extends)

        # Adicionando dependências por traits
        if entity_model.trait_from:
            entities.append(entity_model.trait_from)

        # Adicionando dependências por classes parciais
        if isinstance(entity_model, EntityModel) and entity_model.partial_of:
            entities.append(entity_model.partial_of)

        # Populando com as dependências de propriedades de relacionamento
        relations = self._list_dependencies_relations(entity_model)

        components_dependency_list = []
        if entity_model.components is not None:
            for component in entity_model.components:
                components_dependency_list.extend(
                    self._list_dependencies(entity_model.components[component])
                )

        relations.extend(components_dependency_list)

        entities.extend(relations)

        return entities

    def _list_dependencies_relations(self, entity_model) -> list[str]:
        entities = []

        # Relacionamento 1_N
        for pkey in entity_model.properties:
            prop = entity_model.properties[pkey]

            if isinstance(prop.type, str):
                relation_ref = RelationRefParser.parse(prop.type)
                if relation_ref and relation_ref.is_external:
                    if relation_ref.entity_key:
                        entities.append(relation_ref.entity_key)

        return entities


def get_files_from_directory(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".json") or file.endswith(".yml") or file.endswith(".yaml"):
            files.append(os.path.join(directory, file))
    return files


if __name__ == "__main__":
    import argparse
    import json
    import os
    import yaml

    parser = argparse.ArgumentParser(
        description="Compila arquivos EDL para classes Python"
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Diretório com arquivos .json para compilar",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    files = get_files_from_directory(args.directory)

    entities = {}
    for file in files:
        with open(file, "r") as f:
            if file.endswith(".json"):
                edl = json.load(f)
            else:
                edl = yaml.safe_load(f)

        # Instanciando o objeto de modelo de entidade a partir do JSON,
        # e já realizando as validações básicas de tipo e estrutura.
        print(f"Validando arquivo: {file}")
        if edl.get("mixin", False):
            entity_model = EntityModelRoot(**edl)
        else:
            entity_model = EntityModel(**edl)

        complete_entity_id = f"{entity_model.escopo}/{entity_model.id}"
        entities[complete_entity_id] = entity_model

    compiler = EDLCompiler()
    escopos = {}
    for entity_model in entities.values():
        if entity_model.escopo not in escopos:
            escopos[entity_model.escopo] = EscopoDTO(
                codigo=entity_model.escopo,
                service_account=None,
            )
    compiler_results = compiler.compile_models(entities, escopos)

    with open("output_compilacao_local.py", "w") as f:
        for compiler_result in compiler_results:
            f.write("==========================================================\n")
            f.write(f"Entity: {compiler_result.entity_class_name}\n")
            f.write(f"{compiler_result.entity_code}\n")
            f.write("\n")
            f.write("==========================================================\n")
            f.write(f"DTO: {compiler_result.dto_class_name}\n")
            f.write(f"{compiler_result.dto_code}\n")
            f.write("\n")
            if compiler_result.insert_function_class_name:
                f.write("==========================================================\n")
                f.write(
                    f"Insert Function Type: {compiler_result.insert_function_class_name}\n"
                )
                f.write(f"{compiler_result.source_insert_function or ''}\n")
            if compiler_result.update_function_class_name:
                f.write("==========================================================\n")
                f.write(
                    f"Update Function Type: {compiler_result.update_function_class_name}\n"
                )
                f.write(f"{compiler_result.source_update_function or ''}\n")
            f.write("\n")
            f.write("==========================================================\n")
            f.write(f"API Expose: {compiler_result.api_expose}\n")
            f.write(f"API Route Path: {compiler_result.api_resource}\n")
            f.write(f"API Verbs: {compiler_result.api_verbs}\n")
            f.write("==========================================================\n")
            f.write("\n")
