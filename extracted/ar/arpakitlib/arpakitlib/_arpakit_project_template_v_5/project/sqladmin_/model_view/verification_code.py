from __future__ import annotations

import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view import SimpleMV
from project.sqlalchemy_db_.sqlalchemy_model import VerificationCodeDBM, UserDBM


class VerificationCodeMV(SimpleMV, model=VerificationCodeDBM):
    name = VerificationCodeDBM.get_cls_entity_name()
    name_plural = VerificationCodeDBM.get_cls_entity_name_plural()
    icon = "fa-solid fa-shield"
    column_list = VerificationCodeDBM.get_column_and_relationship_names_()
    column_details_list = VerificationCodeDBM.get_column_and_relationship_names_() + VerificationCodeDBM.get_sd_property_names()
    form_columns = VerificationCodeDBM.get_column_and_relationship_names_(include_column_pk=False)
    form_overrides = {
        VerificationCodeDBM.type.key: SelectField
    }
    form_args = {
        VerificationCodeDBM.type.key: {
            "choices": [(status, status) for status in VerificationCodeDBM.Types.values_list()],
            "description": f"Choose {VerificationCodeDBM.type.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(VerificationCodeDBM).columns
    column_searchable_list = SimpleMV.get_default_column_searchable_list() + [
        VerificationCodeDBM.recipient
    ]
    form_ajax_refs = {
        VerificationCodeDBM.user.key: {
            "fields": [UserDBM.id.key, UserDBM.email.key, UserDBM.username.key],
            "minimum_input_length": 1,
            "page_size": 10,
        }
    }
