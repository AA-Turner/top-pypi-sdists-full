import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM, UserDBM


class UserTokenMV(SimpleMV, model=UserTokenDBM):
    name = "UserToken"
    name_plural = "UserTokens"
    icon = "fa-solid fa-fingerprint"
    column_list = [
        UserTokenDBM.id,
        UserTokenDBM.long_id,
        UserTokenDBM.slug,
        UserTokenDBM.creation_dt,
        UserTokenDBM.value,
        UserTokenDBM.user,
        UserTokenDBM.is_active,
        UserTokenDBM.extra_data,
    ]
    column_details_list = [
        UserTokenDBM.id,
        UserTokenDBM.long_id,
        UserTokenDBM.slug,
        UserTokenDBM.creation_dt,
        UserTokenDBM.value,
        UserTokenDBM.user,
        UserTokenDBM.is_active,
        UserTokenDBM.extra_data,
    ]
    form_columns = [
        UserTokenDBM.slug,
        UserTokenDBM.creation_dt,
        UserTokenDBM.value,
        UserTokenDBM.user,
        UserTokenDBM.is_active,
        UserTokenDBM.extra_data
    ]
    column_sortable_list = sqlalchemy.inspect(UserTokenDBM).columns
    column_default_sort = [
        (UserTokenDBM.creation_dt, True)
    ]
    column_searchable_list = [
        UserTokenDBM.id,
        UserTokenDBM.long_id,
        UserTokenDBM.value,
    ]
    column_formatters = {
        UserTokenDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        UserTokenDBM.extra_data: lambda m, a: format_json_for_preview_(m.extra_data),
    }
    column_formatters_detail = {
        UserTokenDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        UserTokenDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
    form_ajax_refs = {
        UserTokenDBM.user.key: {
            "fields": [UserDBM.id.key, UserDBM.email.key, UserDBM.username.key],
            "placeholder": "Search by id or email",
            "minimum_input_length": 1,
            "page_size": 10,
        }
    }
