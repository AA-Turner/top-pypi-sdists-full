import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM


class StoryLogMV(SimpleMV, model=StoryLogDBM):
    name = "StoryLog"
    name_plural = "StoryLogs"
    icon = "fa-solid fa-history"
    column_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
        StoryLogDBM.slug,
        StoryLogDBM.creation_dt,
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.extra_data
    ]
    column_details_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
        StoryLogDBM.slug,
        StoryLogDBM.creation_dt,
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.extra_data
    ]
    form_columns = [
        StoryLogDBM.slug,
        StoryLogDBM.level,
        StoryLogDBM.type,
        StoryLogDBM.title,
        StoryLogDBM.extra_data
    ]
    form_overrides = {
        StoryLogDBM.level.key: SelectField,
        StoryLogDBM.type.key: SelectField,
    }
    form_args = {
        StoryLogDBM.level.key: {
            "choices": [(v, v) for v in StoryLogDBM.Levels.values_list()],
            "description": f"Choose {StoryLogDBM.level.key}"
        },
        StoryLogDBM.type.key: {
            "choices": [(v, v) for v in StoryLogDBM.Types.values_list()],
            "description": f"Choose {StoryLogDBM.type.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(StoryLogDBM).columns
    column_default_sort = [
        (StoryLogDBM.creation_dt, True)
    ]
    column_searchable_list = [
        StoryLogDBM.id,
        StoryLogDBM.long_id,
    ]
    column_formatters = {
        StoryLogDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        StoryLogDBM.extra_data: lambda m, a: format_json_for_preview_(m.extra_data),
    }
    column_formatters_detail = {
        StoryLogDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        StoryLogDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
