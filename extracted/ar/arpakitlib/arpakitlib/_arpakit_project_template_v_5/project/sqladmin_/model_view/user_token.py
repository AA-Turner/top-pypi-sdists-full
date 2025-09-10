import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM, UserDBM


class UserTokenMV(SimpleMV, model=UserTokenDBM):
    name = UserTokenDBM.get_cls_entity_name()
    name_plural = UserTokenDBM.get_cls_entity_name_plural()
    icon = "fa-solid fa-shield-halved"
    column_list = UserTokenDBM.get_column_and_relationship_names_()
    column_details_list = UserTokenDBM.get_column_and_relationship_names_() + UserTokenDBM.get_sd_property_names()
    form_columns = UserTokenDBM.get_column_and_relationship_names_(include_column_pk=False)
    column_sortable_list = sqlalchemy.inspect(UserTokenDBM).columns
    column_searchable_list = SimpleMV.get_default_column_searchable_list() + [
        UserTokenDBM.value,
    ]
    form_ajax_refs = {
        UserTokenDBM.user.key: {
            "fields": [UserDBM.id.key],
            "minimum_input_length": 1,
            "page_size": 10,
        }
    }
