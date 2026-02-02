from nsj_rest_lib2.compiler.edl_model.column_meta_model import ColumnMetaModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.index_model import IndexModel
from nsj_rest_lib2.compiler.edl_model.property_meta_model import PropertyMetaModel
from nsj_rest_lib2.compiler.edl_model.trait_property_meta_model import (
    ExtendsPropertyMetaModel,
    TraitPropertyMetaModel,
)


class IndexCompilerStructure:
    def __init__(self, index_model: IndexModel, inherited: bool) -> None:
        self.index_model: IndexModel = index_model
        self.inherited: bool = inherited


class PropertiesCompilerStructure:
    def __init__(self) -> None:
        self.properties: dict[str, PropertyMetaModel] = {}
        self.main_properties: list[str] = []
        self.main_resume_fields: dict[str, list[str]] = {}
        self.required: list[str] = []
        self.partition_data: list[str] = []
        self.search_properties: list[str] = []
        self.metric_label: list[str] = []
        self.entity_properties: dict[str, ColumnMetaModel] = {}
        self.trait_properties: dict[str, TraitPropertyMetaModel] = {}
        self.extends_properties: dict[str, ExtendsPropertyMetaModel] = {}
        self.composed_properties: dict[str, list[str]] = {}
        self.property_origins: dict[str, str] = {}


class ComponentsCompilerStructure:
    def __init__(self) -> None:
        self.components: dict[str, EntityModelBase] = {}
