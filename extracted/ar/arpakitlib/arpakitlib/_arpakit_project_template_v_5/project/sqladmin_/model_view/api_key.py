import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


class ApiKeyMV(SimpleMV, model=ApiKeyDBM):
    name = ApiKeyDBM.get_cls_entity_name()
    name_plural = ApiKeyDBM.get_cls_entity_name_plural()
    icon = "fa-solid fa-key"
    column_list = ApiKeyDBM.get_column_and_relationship_names_()
    column_details_list = ApiKeyDBM.get_column_and_relationship_names_() + ApiKeyDBM.get_sd_property_names()
    form_columns = ApiKeyDBM.get_column_and_relationship_names_(include_column_pk=False)
    column_sortable_list = sqlalchemy.inspect(ApiKeyDBM).columns
    column_searchable_list = SimpleMV.get_default_column_searchable_list() + [
        ApiKeyDBM.value,
    ]
