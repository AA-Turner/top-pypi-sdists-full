from dataclasses import dataclass, field
from typing import Any, Optional

from nsj_rest_lib2.compiler.compiler import EDLCompiler
from nsj_rest_lib2.compiler.compiler_structures import PropertiesCompilerStructure
from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import PrimitiveTypes, PropertyType
from nsj_rest_lib2.compiler.migration_compiler_util import MigrationCompilerUtil
from nsj_rest_lib2.compiler.migration_compiler_create_table import (
    MigrationCompilerCreateTable,
)
from nsj_rest_lib2.compiler.migration_compiler_alter_table import (
    MigrationCompilerAlterTable,
)
from nsj_rest_lib2.compiler.migration_compiler_create_table import (
    MigrationCompilerCreateTable,
)
from nsj_rest_lib2.compiler.migration_compiler_alter_table import (
    MigrationCompilerAlterTable,
)
from nsj_rest_lib2.compiler.util.relation_ref import RelationRef, RelationRefParser


class DiffAction:
    ADD_COLUMN = "add_column"
    ALTER_COLUMN = "alter_column"
    DROP_COLUMN = "drop_column"


# TODO Tratar criação e remoção de FKs


@dataclass
class DiffProperty:
    action: str
    property_name: str
    entity_name_old: Optional[str] = None
    entity_name: Optional[str] = None
    old_datatype: Optional[PropertyType] = None
    new_datatype: Optional[PropertyType] = None
    old_required: Optional[bool] = None
    new_required: Optional[bool] = None
    new_description: Optional[str] = None
    new_default: Any = None
    old_pk: Optional[bool] = None
    new_pk: Optional[bool] = None
    new_max_length: Optional[int] = None
    new_check: list[Any] = field(default_factory=list)
    renamed: bool = False
    datatype_changed: bool = False
    required_changed: bool = False
    default_changed: bool = False
    pk_changed: bool = False
    max_length_changed: bool = False
    check_changed: bool = False


class MigrationCompiler:
    def __init__(self, compiler: EDLCompiler):
        self._compiler = compiler
        self._create_table_compiler = MigrationCompilerCreateTable()
        self._alter_table_compiler = MigrationCompilerAlterTable()

    def compile(
        self,
        entity_model: EntityModelBase,
        entity_models: dict[str, EntityModel],
        entity_model_old: EntityModelBase | None = None,
    ) -> str:
        # Resolvendo a estrutura de propriedades da entidade nova
        properties_structure = PropertiesCompilerStructure()
        self._compiler._make_properties_structures(
            properties_structure, entity_model, entity_models
        )
        self._filter_properties_for_migration(properties_structure)

        # Resolvendo a estrutura de propriedades da versão antiga da mesma entidade (para detecção de rename)
        properties_structure_old = None
        if entity_model_old:
            properties_structure_old = PropertiesCompilerStructure()
            self._compiler._make_properties_structures(
                properties_structure_old, entity_model_old, entity_models
            )
            self._filter_properties_for_migration(properties_structure_old)

        table_name = entity_model.repository.map
        column_specs, fk_specs = self._build_column_and_fk_specs(
            entity_model, properties_structure, entity_models
        )
        rename_operations = (
            self._detect_renamed_columns(properties_structure, properties_structure_old)
            if properties_structure_old
            else []
        )
        pk_columns = [spec["column_name"] for spec in column_specs if spec["is_pk"]]

        create_table_sql = self._create_table_compiler.compile(
            table_name, column_specs, pk_columns, fk_specs
        )
        alter_block_sql = self._alter_table_compiler.compile(
            table_name, column_specs, pk_columns, rename_operations, fk_specs
        )

        block_lines = [
            "DO $MIGRATION$",
            "BEGIN",
            f"    IF exists_table('{table_name}') THEN",
        ]
        block_lines.extend(alter_block_sql)
        block_lines.append("    ELSE")
        block_lines.extend(MigrationCompilerUtil.indent_sql(create_table_sql, 8))
        block_lines.append("    END IF;")
        block_lines.append("END$MIGRATION$;")

        return "\n".join(block_lines)

    def _filter_properties_for_migration(
        self, properties_structure: PropertiesCompilerStructure
    ) -> None:
        """
        Remove propriedades herdadas via trait_from ou extends, pois as migrações
        dessas entidades devem ser conduzidas nos EDLs originais.
        """
        allowed_properties: dict[str, Any] = {}
        origins = getattr(properties_structure, "property_origins", {}) or {}
        for name, prop in properties_structure.properties.items():
            origin = origins.get(name, "self")
            if origin in {"trait", "extends"}:
                continue
            allowed_properties[name] = prop

        # Atualiza propriedades e coleções dependentes
        properties_structure.properties = allowed_properties
        allowed_names = set(allowed_properties.keys())
        properties_structure.required = [
            r for r in properties_structure.required if r in allowed_names
        ]
        properties_structure.partition_data = [
            p for p in properties_structure.partition_data if p in allowed_names
        ]
        properties_structure.search_properties = [
            s for s in properties_structure.search_properties if s in allowed_names
        ]
        properties_structure.metric_label = [
            m for m in properties_structure.metric_label if m in allowed_names
        ]
        properties_structure.entity_properties = {
            k: v
            for k, v in properties_structure.entity_properties.items()
            if k in allowed_names
        }

    # FIXME Comentado por hora (tentando confiar mais no BD do que nos EDLs)
    # def _compare_properties_structures(
    #     self,
    #     properties_structure: PropertiesCompilerStructure,
    #     properties_structure_old: PropertiesCompilerStructure,
    # ) -> tuple[list[DiffProperty], list[DiffProperty], list[DiffProperty]]:
    #     alter_properties: list[DiffProperty] = []
    #     add_properties: list[DiffProperty] = []
    #     drop_properties: list[DiffProperty] = []

    #     mapa_equivalencias_old_new: dict[str, str] = {}

    #     # Identificando as propriedades a serem alteradas
    #     for property_name_new in properties_structure.properties:
    #         # Guardando as propriedades da nova coluna
    #         property_new = properties_structure.properties[property_name_new]
    #         entity_mapping_new = properties_structure_old.entity_properties.get(
    #             property_name_new
    #         )
    #         entity_name_new = property_name_new
    #         if entity_mapping_new and entity_mapping_new.column:
    #             entity_name_new = entity_mapping_new.column

    #         # Tentando encontrar uma propriedade equivalente na versão antiga
    #         # É equivalente se tiver o mesmo nome de propriedade, ou se tiver o mesmo nome de coluna

    #         # Recuperando a coluna nova, se houver
    #         achou_property_equivalente = False
    #         property_name_old = None
    #         property_old = None
    #         entity_name_old = None

    #         if (
    #             properties_structure_old
    #             and property_name_new in properties_structure_old.properties
    #         ):
    #             achou_property_equivalente = True

    #             # Pelo nome da propriedade
    #             property_name_old = property_name_new
    #             property_old = properties_structure_old.properties[property_name_old]
    #             entity_mapping_old = properties_structure_old.entity_properties.get(
    #                 property_name_old
    #             )
    #             entity_name_old = property_name_old
    #             if entity_mapping_old and entity_mapping_old.column:
    #                 entity_name_old = entity_mapping_old.column

    #             # Guardando a equivalência para ajudar no drop
    #             mapa_equivalencias_old_new[property_name_old] = property_name_new

    #         elif properties_structure_old:
    #             # Buscando pelo nome da coluna
    #             for property_name_old in properties_structure_old.properties:
    #                 property_old = properties_structure_old.properties[
    #                     property_name_old
    #                 ]
    #                 entity_mapping_old = properties_structure_old.entity_properties.get(
    #                     property_name_old
    #                 )
    #                 entity_name_old = property_name_old
    #                 if entity_mapping_old and entity_mapping_old.column:
    #                     entity_name_old = entity_mapping_old.column

    #                 if entity_name_new == entity_name_old:
    #                     achou_property_equivalente = True

    #                     # Guardando a equivalência para ajudar no drop
    #                     mapa_equivalencias_old_new[property_name_old] = (
    #                         property_name_new
    #                     )

    #                     break

    #         if not achou_property_equivalente:
    #             # Construindo um objeto de adição de coluna
    #             mapped_values_new = []
    #             if property_new.domain_config:
    #                 mapped_values_new = [
    #                     v.mapped_value for v in property_new.domain_config
    #                 ]
    #                 mapped_values_new.sort(key=lambda x: x)

    #             add_properties.append(
    #                 DiffProperty(
    #                     action=DiffAction.ADD_COLUMN,
    #                     property_name=property_name_new,
    #                     entity_name=entity_name_new,
    #                     new_datatype=property_new.type,
    #                     new_required=property_name_new in properties_structure.required,
    #                     new_description=property_new.description,
    #                     new_default=property_new.default,
    #                     new_pk=property_new.pk,
    #                     new_max_length=property_new.max_length,
    #                     new_check=mapped_values_new,
    #                     datatype_changed=True,
    #                     required_changed=property_name_new
    #                     in properties_structure.required,
    #                     default_changed=property_new.default is not None,
    #                     pk_changed=bool(property_new.pk),
    #                     max_length_changed=property_new.max_length is not None,
    #                     check_changed=bool(mapped_values_new),
    #                 )
    #             )

    #         else:

    #             # Construindo um objeto de alteração (para ser usado, se necessário)
    #             persist_alter = False
    #             diff_property = DiffProperty(
    #                 action=DiffAction.ALTER_COLUMN,
    #                 property_name=property_name_new,
    #                 entity_name_old=entity_name_old,
    #                 entity_name=entity_name_new,
    #             )

    #             # Verificando se é alteração do nome da coluna
    #             if entity_name_old != entity_name_new:
    #                 persist_alter = True
    #                 diff_property.entity_name_old = entity_name_old
    #                 diff_property.renamed = True

    #             # Verificando se é alteração de tipo
    #             if property_old.type != property_new.type:
    #                 persist_alter = True
    #                 diff_property.old_datatype = property_old.type
    #                 diff_property.new_datatype = property_new.type
    #                 diff_property.datatype_changed = True

    #             # Verificando se houve alteração de nulidade
    #             required_new = property_name_new in properties_structure.required
    #             required_old = property_name_old in properties_structure_old.required
    #             if required_new != required_old:
    #                 persist_alter = True
    #                 diff_property.old_required = required_old
    #                 diff_property.new_required = required_new
    #                 diff_property.required_changed = True

    #             # Verificando se houve alteração de descrição
    #             if property_old.description != property_new.description:
    #                 persist_alter = True
    #                 diff_property.new_description = property_new.description

    #             # Verificando se houve alteração de valor default
    #             if property_old.default != property_new.default:
    #                 persist_alter = True
    #                 diff_property.new_default = property_new.default
    #                 diff_property.default_changed = True

    #             # Verificando se houve alteração de PK
    #             if property_old.pk != property_new.pk:
    #                 persist_alter = True
    #                 diff_property.old_pk = property_old.pk
    #                 diff_property.new_pk = property_new.pk
    #                 diff_property.pk_changed = True

    #             # Verificando se houve alteração de precisão
    #             if property_old.max_length != property_new.max_length:
    #                 persist_alter = True
    #                 diff_property.new_max_length = property_new.max_length
    #                 diff_property.max_length_changed = True

    #             # Constroi representação do check do enumerado old
    #             old_hash = None
    #             if property_old.domain_config:
    #                 mapped_values_old = [
    #                     v.mapped_value for v in property_old.domain_config
    #                 ]
    #                 mapped_values_old.sort(key=lambda x: x)
    #                 # Fazendo um hash da lista
    #                 old_hash = hash(tuple(mapped_values_old))

    #             # Constroi representação do check do enumerado new
    #             new_hash = None
    #             mapped_values_new = []
    #             if property_new.domain_config:
    #                 mapped_values_new = [
    #                     v.mapped_value for v in property_new.domain_config
    #                 ]
    #                 mapped_values_new.sort(key=lambda x: x)
    #                 # Fazendo um hash da lista
    #                 new_hash = hash(tuple(mapped_values_new))

    #             # Verificando se houve alteração de enumerado
    #             if old_hash != new_hash:
    #                 persist_alter = True
    #                 diff_property.new_check = mapped_values_new
    #                 diff_property.check_changed = True

    #             # Guardando a alteração, caso necessário
    #             if persist_alter:
    #                 alter_properties.append(diff_property)

    # FIXME Comentado por hora (para não suportar ainda o DROP de colunas)
    # Iterando as propriedades do objeto OLD, e verificando as que não existem no objeto NEW
    # (considera-se aqui também a equilência por nome da propriedade ou da coluna)
    # for property_name_old in properties_structure_old.properties:
    #     if property_name_old not in mapa_equivalencias_old_new:
    #         entity_mapping_old = properties_structure_old.entity_properties.get(
    #             property_name_old
    #         )
    #         entity_name_old = property_name_old
    #         if entity_mapping_old and entity_mapping_old.column:
    #             entity_name_old = entity_mapping_old.column

    #         property_old = properties_structure_old.properties[property_name_old]
    #         drop_properties.append(
    #             DiffProperty(
    #                 action=DiffAction.DROP_COLUMN,
    #                 property_name=property_name_old,
    #                 entity_name=entity_name_old,
    #                 old_datatype=property_old.type,
    #                 old_pk=property_old.pk,
    #             )
    #         )

    # return alter_properties, add_properties, drop_properties

    def _build_column_and_fk_specs(
        self,
        entity_model: EntityModelBase,
        properties_structure: PropertiesCompilerStructure,
        entity_models: dict[str, EntityModel],
    ) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        column_specs: list[dict[str, Any]] = []
        fk_specs: list[dict[str, str]] = []
        existing_columns: set[str] = set()

        for property_name, property_model in properties_structure.properties.items():
            if not isinstance(property_model.type, PrimitiveTypes):
                relation_ref = RelationRefParser.parse(property_model.type)
                target_model = relation_ref.resolve_model(entity_models) if relation_ref else None
                # Tenta identificar FK local a partir do relation_column
                entity_mapping = properties_structure.entity_properties.get(
                    property_name
                )
                relation_column = (
                    entity_mapping.relation_column if entity_mapping else None
                )
                if relation_column:
                    relation_column_ref, column_name = self._extract_relation_column_target(
                        relation_column, entity_model
                    )
                    # len >= 3 => <escopo>/<entidade>(/ ...)/<coluna>
                    if relation_column_ref and column_name:
                        # Coluna está na própria entidade
                        if relation_column_ref.target_id == entity_model.id:
                            column_spec = self._build_column_spec_for_relation(
                                property_name,
                                property_model,
                                column_name,
                                properties_structure,
                                target_model,
                            )
                            if column_spec["column_name"] not in existing_columns:
                                column_specs.append(column_spec)
                                existing_columns.add(column_spec["column_name"])
                            fk_specs.append(
                                self._build_fk_spec(
                                    entity_model,
                                    column_name,
                                    property_model,
                                    entity_models,
                                    target_model=target_model,
                                )
                            )
                continue
            entity_mapping = properties_structure.entity_properties.get(property_name)
            column_name = (
                entity_mapping.column
                if entity_mapping and entity_mapping.column
                else property_name
            )

            enum_values: list[Any] = []
            if property_model.domain_config:
                enum_values = [v.mapped_value for v in property_model.domain_config]
                enum_values.sort(key=lambda x: x)

            maximum_value = getattr(property_model, "maximum", None)

            column_specs.append(
                {
                    "property_name": property_name,
                    "column_name": column_name,
                    "datatype": property_model.type,
                    "sql_type": MigrationCompilerUtil.resolve_sql_type(
                        property_model.type, property_model.max_length
                    ),
                    "not_null": property_name in properties_structure.required,
                    "default": property_model.default,
                    "description": property_model.description,
                    "is_pk": bool(property_model.pk),
                    "enum_values": enum_values,
                    "max_length": property_model.max_length,
                    "maximum": maximum_value,
                    "is_numeric": MigrationCompilerUtil.is_numeric(property_model.type),
                }
            )

        # Verifica relacionamentos definidos em outras entidades que apontam colunas para a tabela atual
        for other_id, other_entity in entity_models.items():
            if other_id == f"{entity_model.escopo}/{entity_model.id}" or other_id == entity_model.id:
                continue
            for other_prop_name, other_prop_model in other_entity.properties.items():
                if isinstance(other_prop_model.type, PrimitiveTypes):
                    continue
                other_entity_mapping = other_entity.repository.properties.get(
                    other_prop_name
                )
                relation_column = (
                    other_entity_mapping.relation_column if other_entity_mapping else None
                )
                if not relation_column:
                    continue
                relation_column_ref, column_name = self._extract_relation_column_target(
                    relation_column, other_entity
                )
                if not relation_column_ref or not column_name:
                    continue
                if relation_column_ref.target_id != entity_model.id:
                    continue

                target_model = relation_column_ref.resolve_model(
                    entity_models, base_model=other_entity
                )
                reference_model = (
                    target_model
                    if target_model and target_model != entity_model
                    else other_entity
                )

                # A coluna mora na tabela atual, e referencia a entidade "dona" da propriedade (other_entity)
                pk_type = self._resolve_pk_type(reference_model)
                pk_column = self._resolve_pk_column(reference_model)

                if column_name not in existing_columns:
                    column_specs.append(
                        self._build_external_column_spec(column_name, pk_type)
                    )
                    existing_columns.add(column_name)
                fk_specs.append(
                    {
                        "column_name": column_name,
                        "ref_table": reference_model.repository.map,
                        "ref_column": pk_column,
                    }
                )

        return column_specs, fk_specs

    @staticmethod
    def _extract_relation_column_target(
        relation_column: str,
        base_model: EntityModelBase | None = None,
    ) -> tuple[RelationRef | None, str | None]:
        parts = [part for part in relation_column.split("/") if part]
        if len(parts) < 2:
            return None, None

        column_name = parts[-1]
        relation_path = "/".join(parts[:-1])

        relation_ref = RelationRefParser.parse(relation_path)
        if relation_ref:
            if not relation_ref.scope and base_model and getattr(base_model, "escopo", None):
                relation_ref.scope = base_model.escopo  # type: ignore
            return relation_ref, column_name

        # Fallback para o formato antigo <escopo>/<entidade>/<coluna>
        if len(parts) >= 3:
            return RelationRefParser.parse("/".join(parts[:-1])), column_name

        return None, column_name

    def _build_column_spec_for_relation(
        self,
        property_name: str,
        property_model: Any,
        local_column: str,
        properties_structure: PropertiesCompilerStructure,
        target_model: EntityModelBase | None,
    ) -> dict[str, Any]:
        # Descobre o tipo da PK da entidade referenciada
        pk_type = PrimitiveTypes.UUID
        if target_model:
            pk_prop = next(
                (p for p in target_model.properties if target_model.properties[p].pk),
                None,
            )
            if pk_prop:
                pk_type = target_model.properties[pk_prop].type

        enum_values: list[Any] = []
        maximum_value = None

        return {
            "property_name": property_name,
            "column_name": local_column,
            "datatype": pk_type,
            "sql_type": MigrationCompilerUtil.resolve_sql_type(pk_type, None),
            "not_null": property_name in properties_structure.required,
            "default": None,
            "description": None,
            "is_pk": False,
            "enum_values": enum_values,
            "max_length": None,
            "maximum": maximum_value,
            "is_numeric": MigrationCompilerUtil.is_numeric(pk_type),
        }

    def _build_fk_spec(
        self,
        entity_model: EntityModelBase,
        local_column: str,
        property_model: Any,
        entity_models: dict[str, EntityModel],
        target_model: EntityModelBase | None = None,
    ) -> dict[str, str]:
        ref_entity = target_model
        if ref_entity is None:
            ref_entity_id = property_model.type
            ref_entity = entity_models.get(ref_entity_id)
        ref_table = None
        ref_pk_column = None
        if ref_entity:
            ref_table = ref_entity.repository.map
            ref_pk_prop = next(
                (p for p in ref_entity.properties if ref_entity.properties[p].pk),
                None,
            )
            if ref_pk_prop:
                ref_pk_column = ref_pk_prop
                entity_mapping_ref = ref_entity.repository.properties.get(ref_pk_prop)
                if entity_mapping_ref and entity_mapping_ref.column:
                    ref_pk_column = entity_mapping_ref.column

        return {
            "column_name": local_column,
            "ref_table": ref_table or "",
            "ref_column": ref_pk_column or "id",
        }

    def _resolve_pk_type(self, entity_model: EntityModelBase) -> PrimitiveTypes:
        pk_prop = next(
            (p for p in entity_model.properties if entity_model.properties[p].pk), None
        )
        if not pk_prop:
            return PrimitiveTypes.UUID
        return entity_model.properties[pk_prop].type

    def _resolve_pk_column(self, entity_model: EntityModelBase) -> str:
        pk_prop = next(
            (p for p in entity_model.properties if entity_model.properties[p].pk), None
        )
        if not pk_prop:
            return "id"
        entity_mapping = entity_model.repository.properties.get(pk_prop)
        if entity_mapping and entity_mapping.column:
            return entity_mapping.column
        return pk_prop

    def _build_external_column_spec(
        self, column_name: str, pk_type: PrimitiveTypes
    ) -> dict[str, Any]:
        """
        Constrói especificação de coluna para FK definida em outra entidade,
        mas cuja coluna está na tabela atual.
        """
        return {
            "property_name": column_name,
            "column_name": column_name,
            "datatype": pk_type,
            "sql_type": MigrationCompilerUtil.resolve_sql_type(pk_type, None),
            "not_null": False,
            "default": None,
            "description": None,
            "is_pk": False,
            "enum_values": [],
            "max_length": None,
            "maximum": None,
            "is_numeric": MigrationCompilerUtil.is_numeric(pk_type),
        }

    def _detect_renamed_columns(
        self,
        properties_structure: PropertiesCompilerStructure,
        properties_structure_old: PropertiesCompilerStructure | None,
    ) -> list[tuple[str, str]]:
        """
        Retorna lista de tuplas (old_column, new_column) quando o mapeamento
        de uma propriedade mudou de nome de coluna.
        """
        if not properties_structure_old:
            return []

        rename_ops: list[tuple[str, str]] = []
        for prop_name, _ in properties_structure.properties.items():
            if prop_name not in properties_structure_old.properties:
                continue

            entity_mapping_new = properties_structure.entity_properties.get(prop_name)
            new_column = (
                entity_mapping_new.column
                if entity_mapping_new and entity_mapping_new.column
                else prop_name
            )

            entity_mapping_old = properties_structure_old.entity_properties.get(
                prop_name
            )
            old_column = (
                entity_mapping_old.column
                if entity_mapping_old and entity_mapping_old.column
                else prop_name
            )

            if old_column != new_column:
                rename_ops.append((old_column, new_column))

        return rename_ops
