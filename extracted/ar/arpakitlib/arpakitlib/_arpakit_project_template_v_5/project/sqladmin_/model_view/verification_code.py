from __future__ import annotations

import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import VerificationCodeDBM, UserDBM


class VerificationCodeMV(SimpleMV, model=VerificationCodeDBM):
    name = "VerificationCode"
    name_plural = "VerificationCodes"
    icon = "fa-solid fa-envelope"
    column_list = [
        VerificationCodeDBM.id,
        VerificationCodeDBM.long_id,
        VerificationCodeDBM.slug,
        VerificationCodeDBM.creation_dt,
        VerificationCodeDBM.type,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
        VerificationCodeDBM.user,
        VerificationCodeDBM.is_active,
        VerificationCodeDBM.detail_data,
        VerificationCodeDBM.extra_data
    ]
    column_details_list = [
        VerificationCodeDBM.id,
        VerificationCodeDBM.long_id,
        VerificationCodeDBM.slug,
        VerificationCodeDBM.creation_dt,
        VerificationCodeDBM.type,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
        VerificationCodeDBM.user,
        VerificationCodeDBM.is_active,
        VerificationCodeDBM.detail_data,
        VerificationCodeDBM.extra_data
    ]
    form_columns = [
        VerificationCodeDBM.slug,
        VerificationCodeDBM.type,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
        VerificationCodeDBM.user,
        VerificationCodeDBM.is_active,
        VerificationCodeDBM.detail_data,
        VerificationCodeDBM.extra_data
    ]
    form_overrides = {
        VerificationCodeDBM.type.key: SelectField
    }
    form_args = {
        VerificationCodeDBM.type.key: {
            "choices": [(v, v) for v in VerificationCodeDBM.Types.values_list()],
            "description": f"Choose {VerificationCodeDBM.type.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(VerificationCodeDBM).columns
    column_default_sort = [
        (VerificationCodeDBM.creation_dt, True)
    ]
    column_searchable_list = [
        VerificationCodeDBM.id,
        VerificationCodeDBM.long_id,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient
    ]
    column_formatters = {
        VerificationCodeDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        VerificationCodeDBM.detail_data: lambda m, _: format_json_for_preview_(m.detail_data),
        VerificationCodeDBM.extra_data: lambda m, _: format_json_for_preview_(m.extra_data)
    }
    column_formatters_detail = {
        VerificationCodeDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        VerificationCodeDBM.detail_data: lambda m, _: format_json_for_preview_(m.detail_data),
        VerificationCodeDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
    form_ajax_refs = {
        VerificationCodeDBM.user.key: {
            "fields": [UserDBM.id.key, UserDBM.email.key, UserDBM.username.key],
            "placeholder": "Search by id or email",
            "minimum_input_length": 1,
            "page_size": 10,
        }
    }
