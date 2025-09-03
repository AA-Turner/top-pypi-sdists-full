import sqlalchemy
from wtforms import SelectMultipleField

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class UserMV(SimpleMV, model=UserDBM):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [
        UserDBM.id,
        UserDBM.long_id,
        UserDBM.slug,
        UserDBM.creation_dt,
        UserDBM.fullname,
        UserDBM.email,
        UserDBM.username,
        UserDBM.roles,
        UserDBM.is_active,
        UserDBM.is_verified,
        UserDBM.password,
        UserDBM.tg_id,
        UserDBM.tg_data,
        UserDBM.tg_bot_last_action_dt,
        UserDBM.extra_data
    ]
    column_details_list = [
        UserDBM.id,
        UserDBM.long_id,
        UserDBM.slug,
        UserDBM.creation_dt,
        UserDBM.fullname,
        UserDBM.email,
        UserDBM.username,
        UserDBM.roles,
        UserDBM.is_active,
        UserDBM.is_verified,
        UserDBM.password,
        UserDBM.tg_id,
        UserDBM.tg_data,
        UserDBM.tg_bot_last_action_dt,
        UserDBM.extra_data
    ]
    form_columns = [
        UserDBM.slug,
        UserDBM.fullname,
        UserDBM.email,
        UserDBM.username,
        UserDBM.roles,
        UserDBM.is_active,
        UserDBM.is_verified,
        UserDBM.password,
        UserDBM.tg_id,
        UserDBM.tg_data,
        UserDBM.tg_bot_last_action_dt,
        UserDBM.extra_data
    ]
    form_overrides = {
        UserDBM.roles.key: SelectMultipleField
    }
    form_args = {
        UserDBM.roles.key: {
            "choices": [(v, v) for v in UserDBM.Roles.values_list()],
            "description": f"Choose {UserDBM.roles.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(UserDBM).columns
    column_default_sort = [
        (UserDBM.creation_dt, True)
    ]
    column_searchable_list = [
        UserDBM.id,
        UserDBM.long_id,
        UserDBM.fullname,
        UserDBM.email,
        UserDBM.username,
        UserDBM.tg_id
    ]
    column_formatters = {
        UserDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        UserDBM.tg_data: lambda m, a: format_json_for_preview_(m.tg_data),
        UserDBM.extra_data: lambda m, a: format_json_for_preview_(m.extra_data),
    }
    column_formatters_detail = {
        UserDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        UserDBM.tg_data: lambda m, a: format_json_for_preview_(m.tg_data),
        UserDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
