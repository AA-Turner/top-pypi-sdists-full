import ast
import datetime
import uuid

from nsj_rest_lib2.compiler.compiler_structures import (
    IndexCompilerStructure,
    PropertiesCompilerStructure,
)
from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import (
    BasicTypes,
    CardinalityTypes,
    PrimitiveTypes,
    STR_BASED_TYPES,
)
from nsj_rest_lib2.compiler.edl_model.property_meta_model import PropertyMetaModel
from nsj_rest_lib2.compiler.function_model import FunctionBindingConfig
from nsj_rest_lib2.compiler.edl_model.trait_property_meta_model import (
    TraitPropertyMetaModel,
)
from nsj_rest_lib2.compiler.model import RelationDependency
from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil
from nsj_rest_lib2.compiler.util.type_naming_util import (
    compile_dto_class_name,
    compile_entity_class_name,
    compile_namespace_keys,
)
from nsj_rest_lib2.compiler.util.type_util import TypeUtil
from nsj_rest_lib2.compiler.util.relation_ref import RelationRef, RelationRefParser


class EDLPropertyCompiler:

    def compile(
        self,
        properties_structure: PropertiesCompilerStructure,
        map_unique_by_property: dict[str, IndexCompilerStructure],
        escopo: str,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        prefx_class_name: str,
        function_bindings: FunctionBindingConfig | None = None,
    ) -> tuple[
        list[ast.stmt],
        list[ast.stmt],
        list[str],
        list[ast.stmt],
        list[tuple[str, str, str]],
        list[RelationDependency],
        list[tuple[str, BasicTypes]],
    ]:
        # Descobrindo os atributos marcados como PK (e recuperando a chave primária)
        # TODO Verificar se devemos manter essa verificação
        pk_keys = []
        for pkey in properties_structure.properties:
            prop = properties_structure.properties[pkey]

            if isinstance(prop.type, PrimitiveTypes):
                if prop.pk:
                    pk_keys.append(pkey)

        is_partial_extension = isinstance(entity_model, EntityModel) and bool(
            entity_model.partial_of
        )

        if not entity_model.mixin:
            if len(pk_keys) > 1:
                raise Exception(
                    f"Entidade '{entity_model.id}' possui mais de uma chave primária (ainda não suportado): {pk_keys}"
                )
            elif len(pk_keys) == 0 and not is_partial_extension:
                raise Exception(
                    f"Entidade '{entity_model.id}' não tem nenhuma chave primária (ainda não suportado)"
                )

        # pk_key = pk_keys[0]

        function_bindings = function_bindings or FunctionBindingConfig()
        self._function_bindings = function_bindings

        # Instanciando as listas de retorno
        ast_dto_attributes = []
        ast_entity_attributes = []
        props_pk = []
        aux_classes = []
        related_imports = []
        relations_dependencies = []
        fixed_filters = []

        if properties_structure.properties is None:
            return (ast_dto_attributes, ast_entity_attributes, props_pk, aux_classes)

        trait_fixed_filters = self._merge_trait_extends_properties(
            properties_structure
        )

        composed_properties = properties_structure.composed_properties or {}

        aggregator_class_names: dict[str, str] = {}
        aggregator_dto_attributes: dict[str, list[ast.stmt]] = {}
        aggregated_property_to_group: dict[str, str] = {}

        for composed_key, composed_list in composed_properties.items():
            if not composed_list:
                continue

            composed_class_name = (
                f"{CompilerStrUtil.to_pascal_case(escopo)}"
                f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}"
                f"{CompilerStrUtil.to_pascal_case(entity_model.id)}"
                f"{CompilerStrUtil.to_pascal_case(composed_key)}AggregatorDTO"
            )

            aggregator_class_names[composed_key] = composed_class_name
            aggregator_dto_attributes[composed_key] = []

            for composed_property in composed_list:
                if composed_property in aggregated_property_to_group:
                    raise Exception(
                        f"Propriedade '{composed_property}' da entidade '{entity_model.id}' está associada a mais de um composed_property."
                    )

                if composed_property not in properties_structure.properties:
                    raise Exception(
                        f"Propriedade '{composed_property}' referenciada no composed_property '{composed_key}' não encontrada na entidade '{entity_model.id}'."
                    )

                aggregated_property_to_group[composed_property] = composed_key

        for pkey in properties_structure.properties:
            prop = properties_structure.properties[pkey]

            composed_key = aggregated_property_to_group.get(pkey)
            if composed_key:
                if prop.pk:
                    raise Exception(
                        f"Propriedade '{pkey}' não pode ser utilizada em composed_properties por ser chave primária."
                    )
                target_dto_attributes = aggregator_dto_attributes[composed_key]
            else:
                target_dto_attributes = ast_dto_attributes

            # DTO
            if isinstance(prop.type, PrimitiveTypes):
                # Tratando propriedade simples (não array, não object)
                self._compile_simple_property(
                    properties_structure,
                    map_unique_by_property,
                    escopo,
                    entity_model,
                    target_dto_attributes,
                    ast_entity_attributes,
                    props_pk,
                    aux_classes,
                    pkey,
                    prop,
                    prefx_class_name,
                )

                if pkey in trait_fixed_filters:
                    fixed_filters.append((pkey, trait_fixed_filters[pkey]))

            elif isinstance(prop.type, str):
                relation_ref = RelationRefParser.parse(prop.type)
                if not relation_ref:
                    raise Exception(
                        f"Tipo da propriedade '{pkey}' não suportado: {prop.type}"
                    )

                if relation_ref.is_external:
                    self._compile_external_relation(
                        relation_ref,
                        entity_model,
                        entity_models,
                        properties_structure,
                        target_dto_attributes,
                        ast_entity_attributes,
                        related_imports,
                        relations_dependencies,
                        pkey,
                        prop,
                    )

                elif relation_ref.ref_type == "internal":
                    self._compile_internal_relation(
                        relation_ref,
                        entity_model,
                        properties_structure,
                        target_dto_attributes,
                        ast_entity_attributes,
                        pkey,
                        prop,
                        prefx_class_name,
                    )
                else:
                    raise Exception(
                        f"Tipo da propriedade '{pkey}' não suportado: {prop.type}"
                    )

        for composed_key, class_name in aggregator_class_names.items():
            dto_attributes = aggregator_dto_attributes.get(composed_key, [])

            aux_classes.append(
                self._build_aggregator_class_ast(
                    class_name=class_name,
                    dto_attributes=dto_attributes,
                )
            )

            ast_dto_attributes.append(
                self._build_dto_aggregator_ast(
                    name=composed_key,
                    class_name=class_name,
                )
            )

        return (
            ast_dto_attributes,
            ast_entity_attributes,
            props_pk,
            aux_classes,
            related_imports,
            relations_dependencies,
            fixed_filters,
        )

    def _build_aggregator_class_ast(
        self,
        class_name: str,
        dto_attributes: list[ast.stmt],
    ):
        body = dto_attributes if dto_attributes else [ast.Pass()]

        return ast.ClassDef(
            name=class_name,
            bases=[ast.Name(id="DTOBase", ctx=ast.Load())],
            keywords=[],
            decorator_list=[
                ast.Call(
                    func=ast.Name(id="DTO", ctx=ast.Load()),
                    args=[],
                    keywords=[],
                )
            ],
            body=body,
        )

    def _build_dto_aggregator_ast(
        self,
        name: str,
        class_name: str,
    ):
        return ast.AnnAssign(
            target=ast.Name(
                id=CompilerStrUtil.to_snake_case(name),
                ctx=ast.Store(),
            ),
            annotation=ast.Name(
                id=class_name,
                ctx=ast.Load(),
            ),
            value=ast.Call(
                func=ast.Name(id="DTOAggregator", ctx=ast.Load()),
                args=[ast.Name(id=class_name, ctx=ast.Load())],
                keywords=[],
            ),
            simple=1,
        )

    def _compile_external_relation(
        self,
        relation_ref: RelationRef,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        properties_structure: PropertiesCompilerStructure,
        ast_dto_attributes: list[ast.stmt],
        ast_entity_attributes: list[ast.stmt],
        related_imports: list[tuple[str, str, str]],
        relations_dependencies: list[RelationDependency],
        pkey: str,
        prop: PropertyMetaModel,
    ):
        related_entity_key = relation_ref.entity_key
        if not related_entity_key:
            raise Exception(
                f"Entidade '{entity_model.id}' possui uma referência externa inválida em '{pkey}': {prop.type}"
            )

        related_entity = entity_models.get(related_entity_key)
        if not related_entity:
            raise Exception(
                f"Entidade '{entity_model.id}' possui uma referência externa para uma entidade inexistente: '{related_entity_key}', por meio da propriedade: '{pkey}'."
            )

        related_dto_class_name, related_entity_class_name = (
            self._resolve_related_class_names(relation_ref)
        )

        tenant = related_entity.tenant
        grupo_empresarial = related_entity.grupo_empresarial
        grupo_key, tenant_key, default_key = compile_namespace_keys(
            tenant, grupo_empresarial
        )

        if (
            tenant
            and tenant != 0
            and grupo_empresarial
            and grupo_empresarial != "00000000-0000-0000-0000-000000000000"
        ):
            related_import = grupo_key
        elif tenant and tenant != 0:
            related_import = tenant_key
        else:
            related_import = default_key

        related_imports.append(
            (
                related_import,
                related_dto_class_name,
                related_entity_class_name,
            )
        )

        # Gravando a dependência de relacionamento
        relation_dependency = RelationDependency()
        relation_dependency.entity_resource = related_entity.api.resource
        relation_dependency.entity_scope = related_entity.escopo
        relation_dependency.tenant = tenant
        relation_dependency.grupo_empresarial = grupo_empresarial
        relations_dependencies.append(relation_dependency)

        # Instanciando o ast
        if prop.cardinality == CardinalityTypes.C1_N:
            # Para relacionamentos 1_N
            self._build_ast_1_N(
                properties_structure,
                ast_dto_attributes,
                pkey,
                related_dto_class_name,
                related_entity_class_name,
                prop,
            )

        elif prop.cardinality == CardinalityTypes.C1_1:
            self._build_ast_1_1(
                properties_structure,
                ast_dto_attributes,
                ast_entity_attributes,
                pkey,
                related_dto_class_name,
                related_entity_class_name,
                prop,
                relation_type="AGGREGATION",
            )

        elif prop.cardinality == CardinalityTypes.CN_N:
            # TODO
            pass
        else:
            raise Exception(
                f"Propriedade '{pkey}' da entidade '{entity_model.id}' possui cardinalidade inválida ou não suportada: {prop.cardinality}"
            )

    def _resolve_related_class_names(
        self, relation_ref: RelationRef
    ) -> tuple[str, str]:
        prefix = relation_ref.prefx_class_name
        target_id = relation_ref.target_id

        return (
            compile_dto_class_name(target_id, prefix),
            compile_entity_class_name(target_id, prefix),
        )

    def _compile_internal_relation(
        self,
        relation_ref: RelationRef,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        ast_dto_attributes: list[ast.stmt],
        ast_entity_attributes: list[ast.stmt],
        pkey: str,
        prop: PropertyMetaModel,
        prefx_class_name: str,
    ):
        # Resolvendo o nome das classes de DTO e Entity
        related_dto_class_name = compile_dto_class_name(
            relation_ref.entity, f"{prefx_class_name}_{entity_model.id}"
        )
        related_entity_class_name = compile_entity_class_name(
            relation_ref.entity, f"{prefx_class_name}_{entity_model.id}"
        )

        # Instanciando o ast
        if prop.cardinality == CardinalityTypes.C1_N:
            # Para relacionamentos 1_N
            self._build_ast_1_N(
                properties_structure,
                ast_dto_attributes,
                pkey,
                related_dto_class_name,
                related_entity_class_name,
                prop,
            )

        elif prop.cardinality == CardinalityTypes.C1_1:
            self._build_ast_1_1(
                properties_structure,
                ast_dto_attributes,
                ast_entity_attributes,
                pkey,
                related_dto_class_name,
                related_entity_class_name,
                prop,
                relation_type="COMPOSITION",
            )

        elif prop.cardinality == CardinalityTypes.CN_N:
            # TODO
            pass
        else:
            raise Exception(
                f"Propriedade '{pkey}' da entidade '{entity_model.id}' possui cardinalidade inválida ou não suportada: {prop.cardinality}"
            )

    def _build_ast_1_N(
        self,
        properties_structure: PropertiesCompilerStructure,
        ast_dto_attributes: list[ast.stmt],
        pkey: str,
        related_dto_class_name: str,
        related_entity_class_name: str,
        prop: PropertyMetaModel,
    ):
        # TODO Verificar uso da propriedade relation_key_field do Rest_lib_1

        # Propriedade do property descriptor
        keywords = [
            ast.keyword(
                arg="dto_type",
                value=ast.Name(id=related_dto_class_name, ctx=ast.Load()),
            ),
            ast.keyword(
                arg="entity_type",
                value=ast.Name(id=related_entity_class_name, ctx=ast.Load()),
            ),
        ]

        insert_binding = self._function_bindings.insert_relations.get(pkey)
        if insert_binding:
            if (
                insert_binding.field_name
                and insert_binding.field_name != CompilerStrUtil.to_snake_case(pkey)
            ):
                keywords.append(
                    ast.keyword(
                        arg="insert_function_field",
                        value=ast.Constant(value=insert_binding.field_name),
                    )
                )
            if insert_binding.function_type_class:
                keywords.append(
                    ast.keyword(
                        arg="insert_function_type",
                        value=ast.Name(
                            id=insert_binding.function_type_class, ctx=ast.Load()
                        ),
                    )
                )

        update_binding = self._function_bindings.update_relations.get(pkey)
        if update_binding:
            if (
                update_binding.field_name
                and update_binding.field_name != CompilerStrUtil.to_snake_case(pkey)
            ):
                keywords.append(
                    ast.keyword(
                        arg="update_function_field",
                        value=ast.Constant(value=update_binding.field_name),
                    )
                )
            if update_binding.function_type_class:
                keywords.append(
                    ast.keyword(
                        arg="update_function_type",
                        value=ast.Name(
                            id=update_binding.function_type_class, ctx=ast.Load()
                        ),
                    )
                )

        # Tratando das opções básicas do descritor de propriedade
        if properties_structure.required and pkey in properties_structure.required:
            keywords.append(ast.keyword(arg="not_null", value=ast.Constant(True)))

        if prop.max_length:
            keywords.append(ast.keyword(arg="max", value=ast.Constant(prop.max_length)))
        if prop.min_length:
            keywords.append(ast.keyword(arg="min", value=ast.Constant(prop.min_length)))

        if prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Name(prop.validator, ctx=ast.Load()),
                )
            )

        resume_fields = properties_structure.main_resume_fields.get(pkey)
        if resume_fields:
            keywords.append(
                ast.keyword(
                    arg="resume_fields",
                    value=ast.List(
                        elts=[ast.Constant(value=field) for field in resume_fields],
                        ctx=ast.Load(),
                    ),
                )
            )

        # Resolvendo a coluna usada no relacionamento
        if (
            not properties_structure.entity_properties
            or pkey not in properties_structure.entity_properties
            or not properties_structure.entity_properties[pkey].relation_column
        ):
            raise Exception(
                f"Propriedade '{pkey}' possui um relacionamento, mas nenhuma coluna de relacioanamento foi apontada na propriedade correspondente no repository."
            )

        relation_column_ref = properties_structure.entity_properties[
            pkey
        ].relation_column
        relation_column = str(relation_column_ref).split("/")[-1]

        keywords.append(
            ast.keyword(
                arg="related_entity_field",
                value=ast.Constant(value=relation_column),
            )
        )

        ast_attr = ast.AnnAssign(
            target=ast.Name(id=CompilerStrUtil.to_snake_case(pkey), ctx=ast.Store()),
            annotation=ast.Name(
                id="list",
                ctx=ast.Load(),
            ),
            value=ast.Call(
                func=ast.Name(id="DTOListField", ctx=ast.Load()),
                args=[],
                keywords=keywords,
            ),
            simple=1,
        )

        ast_dto_attributes.append(ast_attr)

    def _build_ast_1_1(
        self,
        properties_structure: PropertiesCompilerStructure,
        ast_dto_attributes: list[ast.stmt],
        ast_entity_attributes: list[ast.stmt],
        pkey: str,
        related_dto_class_name: str,
        related_entity_class_name: str,
        prop: PropertyMetaModel,
        relation_type: str,
    ):
        # Keywords for DTOOneToOneField
        keywords = [
            ast.keyword(
                arg="entity_type",
                value=ast.Name(id=related_entity_class_name, ctx=ast.Load()),
            ),
        ]

        insert_binding = self._function_bindings.insert_relations.get(pkey)
        if insert_binding:
            if (
                insert_binding.field_name
                and insert_binding.field_name != CompilerStrUtil.to_snake_case(pkey)
            ):
                keywords.append(
                    ast.keyword(
                        arg="insert_function_field",
                        value=ast.Constant(value=insert_binding.field_name),
                    )
                )
            if insert_binding.function_type_class:
                keywords.append(
                    ast.keyword(
                        arg="insert_function_type",
                        value=ast.Name(
                            id=insert_binding.function_type_class, ctx=ast.Load()
                        ),
                    )
                )

        update_binding = self._function_bindings.update_relations.get(pkey)
        if update_binding:
            if (
                update_binding.field_name
                and update_binding.field_name != CompilerStrUtil.to_snake_case(pkey)
            ):
                keywords.append(
                    ast.keyword(
                        arg="update_function_field",
                        value=ast.Constant(value=update_binding.field_name),
                    )
                )
            if update_binding.function_type_class:
                keywords.append(
                    ast.keyword(
                        arg="update_function_type",
                        value=ast.Name(
                            id=update_binding.function_type_class, ctx=ast.Load()
                        ),
                    )
                )

        # Tratando das opções básicas do descritor de propriedade
        if properties_structure.required and pkey in properties_structure.required:
            keywords.append(ast.keyword(arg="not_null", value=ast.Constant(True)))

        # 'resume' now belongs to the inner DTOField (matches desired format)
        if (
            properties_structure.main_properties
            and pkey in properties_structure.main_properties
        ):
            keywords.append(ast.keyword(arg="resume", value=ast.Constant(True)))

        # Resolvendo a coluna usada no relacionamento
        if (
            not properties_structure.entity_properties
            or pkey not in properties_structure.entity_properties
            or not properties_structure.entity_properties[pkey].relation_column
        ):
            raise Exception(
                f"Propriedade '{pkey}' possui um relacionamento, mas nenhuma coluna de relacioanamento foi apontada na propriedade correspondente no repository."
            )

        relation_column = str(
            properties_structure.entity_properties[pkey].relation_column
        )

        owner_relation = False
        if "/" in relation_column:
            owner_relation = True
            relation_column = relation_column.split("/")[-1]
        

        keywords.append(
            ast.keyword(
                arg="relation_type",
                value=ast.Attribute(
                    value=ast.Name(id="OTORelationType", ctx=ast.Load()),
                    attr=relation_type,
                    ctx=ast.Load(),
                ),
            )
        )
            
        # Build the inner field descriptor with the entity column mapping
        keywords.append(
            ast.keyword(
                arg="entity_field",
                value=ast.Constant(value=relation_column),
            )
        )

        if not owner_relation:
            keywords.append(
                ast.keyword(
                    arg="entity_relation_owner",
                    value=ast.Attribute(
                        value=ast.Name(id="EntityRelationOwner", ctx=ast.Load()),
                        attr="OTHER",
                        ctx=ast.Load(),
                    ),
                )
            )
        else:
            # Dono da relação: informa explicitamente como SELF e garante o atributo na Entity
            keywords.append(
                ast.keyword(
                    arg="entity_relation_owner",
                    value=ast.Attribute(
                        value=ast.Name(id="EntityRelationOwner", ctx=ast.Load()),
                        attr="SELF",
                        ctx=ast.Load(),
                    ),
                )
            )
            # Adicionando propriedade no Entity para a coluna de relação
            ast_entity_attributes.append(
                self._build_entity_property_ast(relation_column, PrimitiveTypes.UUID)
            )

        # Adicionando a propriedade em si do relacionamento, no DTO
        ast_attr = ast.AnnAssign(
            target=ast.Name(id=CompilerStrUtil.to_snake_case(pkey), ctx=ast.Store()),
            annotation=ast.Name(
                id=related_dto_class_name,
                ctx=ast.Load(),
            ),
            value=ast.Call(
                func=ast.Name(id="DTOOneToOneField", ctx=ast.Load()),
                args=[],
                keywords=keywords,
            ),
            simple=1,
        )

        ast_dto_attributes.append(ast_attr)

    def _build_dto_property_ast(
        self,
        name: str,
        type: PrimitiveTypes | str,
        keywords: list[ast.keyword] = [],
    ):
        if isinstance(type, PrimitiveTypes):
            type_str = TypeUtil.property_type_to_python_type(type)
        else:
            type_str = type

        return ast.AnnAssign(
            target=ast.Name(
                id=CompilerStrUtil.to_snake_case(name),
                ctx=ast.Store(),
            ),
            annotation=ast.Name(
                id=type_str,
                ctx=ast.Load(),
            ),
            value=ast.Call(
                func=ast.Name(id="DTOField", ctx=ast.Load()),
                args=[],
                keywords=keywords,
            ),
            simple=1,
        )

    def _build_entity_property_ast(
        self,
        name: str,
        type: PrimitiveTypes,
    ):
        return ast.AnnAssign(
            target=ast.Name(
                id=CompilerStrUtil.to_snake_case(name),
                ctx=ast.Store(),
            ),
            annotation=ast.Name(
                id=TypeUtil.property_type_to_python_type(type),
                ctx=ast.Load(),
            ),
            value=ast.Constant(value=None),
            simple=1,
        )

    def _compile_simple_property(
        self,
        properties_structure,
        map_unique_by_property,
        escopo,
        entity_model,
        ast_dto_attributes,
        ast_entity_attributes,
        props_pk,
        aux_classes,
        pkey,
        prop,
        prefx_class_name: str,
    ):
        enum_class_name = None
        keywords = []

        if prop.pk:
            keywords.append(ast.keyword(arg="pk", value=ast.Constant(True)))
            props_pk.append(pkey)

        if prop.key_alternative:
            keywords.append(ast.keyword(arg="candidate_key", value=ast.Constant(True)))

        if (
            properties_structure.main_properties
            and pkey in properties_structure.main_properties
        ):
            keywords.append(ast.keyword(arg="resume", value=ast.Constant(True)))

        if properties_structure.required and pkey in properties_structure.required:
            keywords.append(ast.keyword(arg="not_null", value=ast.Constant(True)))

        if (
            properties_structure.partition_data
            and pkey in properties_structure.partition_data
        ):
            keywords.append(ast.keyword(arg="partition_data", value=ast.Constant(True)))

        if pkey in map_unique_by_property:
            unique = map_unique_by_property[pkey].index_model
            keywords.append(
                ast.keyword(
                    arg="unique",
                    value=ast.Constant(unique.name),
                )
            )

        if prop.trim:
            keywords.append(ast.keyword(arg="strip", value=ast.Constant(True)))

        max = None
        min = None
        if prop.type in [PrimitiveTypes.STRING, PrimitiveTypes.EMAIL]:
            if prop.max_length:
                max = prop.max_length
            if prop.min_length:
                min = prop.min_length
        elif prop.type in [PrimitiveTypes.INTEGER, PrimitiveTypes.NUMBER]:
            if prop.minimum:
                min = prop.minimum
            if prop.maximum:
                max = prop.maximum

        if max:
            keywords.append(ast.keyword(arg="max", value=ast.Constant(max)))
        if min:
            keywords.append(ast.keyword(arg="min", value=ast.Constant(min)))

        if (
            properties_structure.search_properties
            and pkey in properties_structure.search_properties
        ):
            keywords.append(ast.keyword(arg="search", value=ast.Constant(True)))
        else:
            keywords.append(ast.keyword(arg="search", value=ast.Constant(False)))

        if (
            properties_structure.metric_label
            and pkey in properties_structure.metric_label
        ):
            keywords.append(ast.keyword(arg="metric_label", value=ast.Constant(True)))

        if prop.type == PrimitiveTypes.CPF and not prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="DTOFieldValidators", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                        attr="validate_cpf",
                        ctx=ast.Load(),
                    ),
                )
            )
        elif prop.type == PrimitiveTypes.CNPJ and not prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="DTOFieldValidators", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                        attr="validate_cnpj",
                        ctx=ast.Load(),
                    ),
                )
            )
        elif prop.type == PrimitiveTypes.CPF_CNPJ and not prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="DTOFieldValidators", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                        attr="validate_cpf_or_cnpj",
                        ctx=ast.Load(),
                    ),
                )
            )
        elif prop.type == PrimitiveTypes.EMAIL and not prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="DTOFieldValidators", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                        attr="validate_email",
                        ctx=ast.Load(),
                    ),
                )
            )
        elif prop.validator:
            keywords.append(
                ast.keyword(
                    arg="validator",
                    value=ast.Name(prop.validator, ctx=ast.Load()),
                )
            )

        if prop.immutable:
            keywords.append(ast.keyword(arg="read_only", value=ast.Constant(True)))

        if prop.on_save:
            keywords.append(
                ast.keyword(
                    arg="convert_to_entity",
                    value=ast.Name(prop.on_save, ctx=ast.Load()),
                )
            )

        if prop.on_retrieve:
            keywords.append(
                ast.keyword(
                    arg="convert_from_entity",
                    value=ast.Name(id=prop.on_retrieve, ctx=ast.Load()),
                )
            )

        if prop.domain_config:
            result = self._compile_domain_config(
                pkey, prop, escopo, entity_model, prefx_class_name
            )
            if not result:
                raise Exception(f"Erro desconhecido ao compilar a propriedade {pkey}")

            enum_class_name, ast_enum_class = result
            aux_classes.append(ast_enum_class)

        default_value_ast = self._build_default_value_ast(pkey, prop, enum_class_name)
        if default_value_ast is not None:
            keywords.append(
                ast.keyword(
                    arg="default_value",
                    value=default_value_ast,
                )
            )

        insert_binding = self._function_bindings.insert_fields.get(pkey)
        if insert_binding:
            keywords.append(
                ast.keyword(
                    arg="insert_function_field",
                    value=ast.Constant(value=insert_binding),
                )
            )

        update_binding = self._function_bindings.update_fields.get(pkey)
        if update_binding:
            keywords.append(
                ast.keyword(
                    arg="update_function_field",
                    value=ast.Constant(value=update_binding),
                )
            )

        # Resolvendo o nome da propriedade no Entity
        if (
            properties_structure.entity_properties
            and pkey in properties_structure.entity_properties
        ):
            entity_field_name = properties_structure.entity_properties[pkey].column
        else:
            entity_field_name = pkey

        # Escrevendo, se necessário, o alias para o nome da entity
        if entity_field_name != pkey:
            keywords.append(
                ast.keyword(
                    arg="entity_field",
                    value=ast.Constant(value=entity_field_name),
                )
            )

        # Instanciando o atributo AST
        if enum_class_name:
            prop_type = enum_class_name
        else:
            prop_type = TypeUtil.property_type_to_python_type(prop.type)

        ast_attr = self._build_dto_property_ast(pkey, prop_type, keywords)
        ast_dto_attributes.append(ast_attr)

        # Entity
        ast_entity_attr = self._build_entity_property_ast(entity_field_name, prop.type)

        ast_entity_attributes.append(ast_entity_attr)

    def _build_default_value_ast(
        self,
        pkey: str,
        prop: PropertyMetaModel,
        enum_class_name: str | None,
    ) -> ast.expr | None:
        default_value = prop.default
        if default_value is None:
            return None

        if prop.domain_config and enum_class_name:
            return self._build_enum_default_value_ast(
                pkey, prop, enum_class_name, default_value
            )

        if not isinstance(prop.type, PrimitiveTypes):
            raise ValueError(
                f"Propriedade '{pkey}' não suporta valor default para relacionamentos."
            )

        return self._build_primitive_default_value_ast(pkey, prop, default_value)

    def _build_enum_default_value_ast(
        self,
        pkey: str,
        prop: PropertyMetaModel,
        enum_class_name: str,
        default_value: object,
    ) -> ast.expr:
        target_option = None
        for option in prop.domain_config or []:
            if option.value == default_value:
                target_option = option
                break

            if option.mapped_value is not None and option.mapped_value == default_value:
                target_option = option
                break

        if not target_option:
            raise ValueError(
                f"Propriedade '{pkey}' possui valor default '{default_value}' que não corresponde a nenhuma opção do enum."
            )

        enum_member_name = CompilerStrUtil.to_enum_member_name(target_option.value)

        return ast.Attribute(
            value=ast.Name(id=enum_class_name, ctx=ast.Load()),
            attr=enum_member_name,
            ctx=ast.Load(),
        )

    def _merge_trait_extends_properties(
        self, properties_structure: PropertiesCompilerStructure
    ) -> dict[str, BasicTypes]:
        fixed_filters: dict[str, BasicTypes] = {}

        trait_sources = (
            properties_structure.trait_properties or {},
            properties_structure.extends_properties or {},
        )

        for prop_dict in trait_sources:
            for pkey, tprop in prop_dict.items():
                if not isinstance(tprop.type, PrimitiveTypes):
                    raise ValueError(
                        f"Propriedade '{pkey}' definida em trait/extends precisa ser um tipo primitivo."
                    )

                base_prop = properties_structure.properties.get(pkey)

                if base_prop:
                    if base_prop.type != tprop.type:
                        raise ValueError(
                            f"Tipo da propriedade '{pkey}' em trait/extends não coincide com a definição existente."
                        )

                    base_prop.default = tprop.value

                    if tprop.domain_config and not base_prop.domain_config:
                        base_prop.domain_config = tprop.domain_config
                else:
                    base_prop = PropertyMetaModel(
                        type=tprop.type,
                        default=tprop.value,
                        domain_config=tprop.domain_config,
                    )
                    properties_structure.properties[pkey] = base_prop

                fixed_filters[pkey] = tprop.value

        return fixed_filters

    def _build_primitive_default_value_ast(
        self,
        pkey: str,
        prop: PropertyMetaModel,
        default_value: object,
    ) -> ast.expr:
        primitive_type = prop.type

        if isinstance(default_value, str):
            expression_ast = self._build_python_expression_from_string(default_value)
            if expression_ast is not None:
                return expression_ast

        if primitive_type in STR_BASED_TYPES:
            if not isinstance(default_value, str):
                raise ValueError(
                    f"Propriedade '{pkey}' exige valor default textual, recebido '{default_value}'."
                )
            return ast.Constant(value=default_value)

        if primitive_type == PrimitiveTypes.BOOLEAN:
            if isinstance(default_value, bool):
                return ast.Constant(value=default_value)
            raise ValueError(
                f"Propriedade '{pkey}' exige valor default booleano, recebido '{default_value}'."
            )

        if primitive_type == PrimitiveTypes.INTEGER:
            return self._build_numeric_constant_default_ast(
                pkey,
                default_value,
                int,
                "inteiro",
                forbid_fraction=True,
            )

        if primitive_type in (
            PrimitiveTypes.NUMBER,
            PrimitiveTypes.CURRENCY,
            PrimitiveTypes.QUANTITY,
        ):
            return self._build_numeric_constant_default_ast(
                pkey,
                default_value,
                float,
                "numérico",
            )

        if primitive_type == PrimitiveTypes.UUID:
            return self._build_uuid_default_ast(pkey, default_value)

        if primitive_type == PrimitiveTypes.DATE:
            return self._build_iso_datetime_default_ast(
                pkey,
                default_value,
                target="date",
            )

        if primitive_type == PrimitiveTypes.DATETIME:
            return self._build_iso_datetime_default_ast(
                pkey,
                default_value,
                target="datetime",
            )

        raise ValueError(
            f"Propriedade '{pkey}' não suporta valor default para o tipo '{primitive_type.value}'."
        )

    def _build_numeric_constant_default_ast(
        self,
        pkey: str,
        default_value: object,
        cast_type: type,
        type_label: str,
        *,
        forbid_fraction: bool = False,
    ) -> ast.expr:
        if isinstance(default_value, bool):
            raise ValueError(
                f"Propriedade '{pkey}' exige valor default {type_label}, recebido '{default_value}'."
            )

        value_to_convert = (
            default_value.strip() if isinstance(default_value, str) else default_value
        )

        if forbid_fraction and isinstance(value_to_convert, float):
            if not value_to_convert.is_integer():
                raise ValueError(
                    f"Propriedade '{pkey}' exige valor default inteiro, recebido '{default_value}'."
                )

        try:
            converted_value = cast_type(value_to_convert)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Propriedade '{pkey}' exige valor default {type_label}, recebido '{default_value}'."
            ) from exc

        if forbid_fraction and isinstance(value_to_convert, float):
            converted_value = int(converted_value)

        return ast.Constant(value=converted_value)

    def _build_uuid_default_ast(
        self,
        pkey: str,
        default_value: object,
    ) -> ast.expr:
        if isinstance(default_value, uuid.UUID):
            uuid_value = str(default_value)
        elif isinstance(default_value, str):
            try:
                uuid_value = str(uuid.UUID(default_value))
            except ValueError as exc:
                raise ValueError(
                    f"Propriedade '{pkey}' exige UUID válido ou expressão Python, recebido '{default_value}'."
                ) from exc
        else:
            raise ValueError(
                f"Propriedade '{pkey}' exige UUID válido ou expressão Python, recebido '{default_value}'."
            )

        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="uuid", ctx=ast.Load()),
                attr="UUID",
                ctx=ast.Load(),
            ),
            args=[ast.Constant(value=uuid_value)],
            keywords=[],
        )

    def _build_iso_datetime_default_ast(
        self,
        pkey: str,
        default_value: object,
        *,
        target: str,
    ) -> ast.expr:
        if target == "date":
            parser = datetime.date
        else:
            parser = datetime.datetime

        if isinstance(default_value, parser):
            iso_value = default_value.isoformat()
        elif isinstance(default_value, str):
            iso_value = default_value.strip()
        else:
            raise ValueError(
                f"Propriedade '{pkey}' exige {target} em formato ISO ou expressão Python, recebido '{default_value}'."
            )

        try:
            parser.fromisoformat(iso_value)
        except ValueError as exc:
            raise ValueError(
                f"Propriedade '{pkey}' exige {target} em formato ISO ou expressão Python, recebido '{default_value}'."
            ) from exc

        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="datetime", ctx=ast.Load()),
                    attr=target,
                    ctx=ast.Load(),
                ),
                attr="fromisoformat",
                ctx=ast.Load(),
            ),
            args=[ast.Constant(value=iso_value)],
            keywords=[],
        )

    def _build_python_expression_from_string(self, expression: str) -> ast.expr | None:
        try:
            parsed_expr = ast.parse(expression, mode="eval").body
        except SyntaxError:
            return None

        if self._is_safe_python_expression(parsed_expr):
            return parsed_expr

        return None

    def _is_safe_python_expression(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return True
        if isinstance(node, ast.Attribute):
            return self._is_safe_python_expression(node.value)
        if isinstance(node, ast.Call):
            if node.keywords or node.args:
                return False
            return self._is_safe_python_expression(node.func)
        return False

    def _compile_domain_config(
        self,
        pkey: str,
        prop: PropertyMetaModel | TraitPropertyMetaModel,
        escopo: str,
        entity_model: EntityModelBase,
        prefx_class_name: str,
    ) -> tuple[str, ast.stmt] | None:
        if not prop.domain_config:
            return None

        # Verificando se deveria usar o mapped_value
        use_mapped_value = False
        for value in prop.domain_config:
            if value.mapped_value:
                use_mapped_value = True
                break

        # Compilando as opções do enum
        ast_values = []
        for value in prop.domain_config:
            value_name = CompilerStrUtil.to_enum_member_name(value.value)

            if use_mapped_value and value.mapped_value is None:
                raise Exception(
                    f"Propriedade '{pkey}' possui domain_config com value '{value.value}' mas sem mapped_value"
                )

            if value.mapped_value is not None:
                ast_value = ast.Assign(
                    targets=[ast.Name(id=value_name, ctx=ast.Store())],
                    value=ast.Tuple(
                        elts=[
                            ast.Constant(value=value.value),
                            ast.Constant(value=value.mapped_value),
                        ],
                        ctx=ast.Load(),
                    ),
                )
            else:
                ast_value = ast.Assign(
                    targets=[ast.Name(id=value_name, ctx=ast.Store())],
                    value=ast.Constant(value=value.value),
                )

            ast_values.append(ast_value)

        # Instanciando o atributo AST
        enum_class_name = f"{CompilerStrUtil.to_pascal_case(escopo)}{CompilerStrUtil.to_pascal_case(prefx_class_name)}{CompilerStrUtil.to_pascal_case(entity_model.id)}{CompilerStrUtil.to_pascal_case(pkey)}Enum"
        ast_enum_class = ast.ClassDef(
            name=enum_class_name,
            bases=[
                ast.Attribute(
                    value=ast.Name(id="enum", ctx=ast.Load()),
                    attr="Enum",
                    ctx=ast.Load(),
                )
            ],
            keywords=[],
            decorator_list=[],
            body=ast_values,
        )

        return enum_class_name, ast_enum_class
