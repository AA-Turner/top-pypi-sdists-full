import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_, format_json_for_preview_
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


class ApiKeyMV(SimpleMV, model=ApiKeyDBM):
    name = "ApiKey"
    name_plural = "ApiKeys"
    icon = "fa-solid fa-key"
    column_list = [
        ApiKeyDBM.id,
        ApiKeyDBM.long_id,
        ApiKeyDBM.slug,
        ApiKeyDBM.creation_dt,
        ApiKeyDBM.title,
        ApiKeyDBM.value,
        ApiKeyDBM.is_active,
        ApiKeyDBM.extra_data
    ]
    column_details_list = [
        ApiKeyDBM.id,
        ApiKeyDBM.long_id,
        ApiKeyDBM.slug,
        ApiKeyDBM.creation_dt,
        ApiKeyDBM.title,
        ApiKeyDBM.value,
        ApiKeyDBM.is_active,
        ApiKeyDBM.extra_data
    ]
    form_columns = [
        ApiKeyDBM.slug,
        ApiKeyDBM.title,
        ApiKeyDBM.value,
        ApiKeyDBM.is_active,
    ]
    column_sortable_list = sqlalchemy.inspect(ApiKeyDBM).columns
    column_default_sort = [
        (ApiKeyDBM.creation_dt, True)
    ]
    column_searchable_list = [
        ApiKeyDBM.id,
        ApiKeyDBM.long_id,
        ApiKeyDBM.value,
    ]
    column_formatters = {
        ApiKeyDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        ApiKeyDBM.extra_data: lambda m, a: format_json_for_preview_(m.extra_data),
    }
    column_formatters_detail = {
        ApiKeyDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        ApiKeyDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
