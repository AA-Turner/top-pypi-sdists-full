import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class OperationMV(SimpleMV, model=OperationDBM):
    name = "Operation"
    name_plural = "Operations"
    icon = "fa-solid fa-gears"
    column_list = [
        OperationDBM.id,
        OperationDBM.long_id,
        OperationDBM.slug,
        OperationDBM.creation_dt,
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.title,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data,
        OperationDBM.extra_data,

        "duration"
    ]
    column_details_list = [
        OperationDBM.id,
        OperationDBM.long_id,
        OperationDBM.slug,
        OperationDBM.creation_dt,
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.title,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data,
        OperationDBM.extra_data,

        "duration"
    ]
    form_columns = [
        OperationDBM.slug,
        OperationDBM.status,
        OperationDBM.type,
        OperationDBM.title,
        OperationDBM.execution_start_dt,
        OperationDBM.execution_finish_dt,
        OperationDBM.input_data,
        OperationDBM.output_data,
        OperationDBM.error_data,
        OperationDBM.extra_data
    ]
    form_overrides = {
        OperationDBM.status.key: SelectField,
        OperationDBM.type.key: SelectField
    }
    form_args = {
        OperationDBM.status.key: {
            "choices": [(v, v) for v in OperationDBM.Statuses.values_list()],
            "description": f"Choose {OperationDBM.status.key}"
        },
        OperationDBM.type.key: {
            "choices": [(v, v) for v in OperationDBM.Types.values_list()],
            "description": f"Choose {OperationDBM.type.key}"
        }
    }
    column_sortable_list = sqlalchemy.inspect(OperationDBM).columns
    column_default_sort = [
        (OperationDBM.creation_dt, True)
    ]
    column_searchable_list = [
        OperationDBM.id,
        OperationDBM.long_id
    ]
    column_formatters = {
        OperationDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        OperationDBM.execution_start_dt: lambda m, _: format_datetime_(m.execution_start_dt),
        OperationDBM.execution_finish_dt: lambda m, _: format_datetime_(m.execution_finish_dt),
        OperationDBM.input_data: lambda m, a: format_json_for_preview_(m.input_data),
        OperationDBM.output_data: lambda m, a: format_json_for_preview_(m.output_data),
        OperationDBM.error_data: lambda m, a: format_json_for_preview_(m.error_data),
        OperationDBM.extra_data: lambda m, a: format_json_for_preview_(m.extra_data),
        "duration": lambda m, a: m.duration,
    }
    column_formatters_detail = {
        OperationDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        OperationDBM.input_data: lambda m, a: format_json_(m.input_data),
        OperationDBM.output_data: lambda m, a: format_json_(m.output_data),
        OperationDBM.error_data: lambda m, a: format_json_(m.error_data),
        OperationDBM.extra_data: lambda m, a: format_json_(m.extra_data),
        "duration": lambda m, a: m.duration,
    }
