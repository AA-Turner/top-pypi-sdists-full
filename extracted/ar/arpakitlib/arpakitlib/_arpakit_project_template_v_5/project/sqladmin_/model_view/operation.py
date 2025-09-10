import sqlalchemy
from sqladmin.fields import SelectField

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class OperationMV(SimpleMV, model=OperationDBM):
    name = OperationDBM.get_cls_entity_name()
    name_plural = OperationDBM.get_cls_entity_name_plural()
    icon = "fa-solid fa-gears"
    column_list = OperationDBM.get_column_and_relationship_names_()
    column_details_list = OperationDBM.get_column_and_relationship_names_() + OperationDBM.get_sd_property_names()
    form_columns = OperationDBM.get_column_and_relationship_names_(include_column_pk=False)
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
    column_formatters = {
        **SimpleMV.get_default_column_formatters(),
        OperationDBM.execution_start_dt: lambda m, _: format_datetime_(m.execution_start_dt),
        OperationDBM.execution_finish_dt: lambda m, _: format_datetime_(m.execution_finish_dt),
        OperationDBM.input_data: lambda m, a: format_json_for_preview_(m.input_data),
        OperationDBM.output_data: lambda m, a: format_json_for_preview_(m.output_data),
        OperationDBM.error_data: lambda m, a: format_json_for_preview_(m.error_data),
    }
    column_formatters_detail = {
        **SimpleMV.get_default_column_formatters_detail(),
        OperationDBM.execution_start_dt: lambda m, _: format_datetime_(m.execution_start_dt),
        OperationDBM.execution_finish_dt: lambda m, _: format_datetime_(m.execution_finish_dt),
        OperationDBM.input_data: lambda m, a: format_json_(m.input_data),
        OperationDBM.output_data: lambda m, a: format_json_(m.output_data),
        OperationDBM.error_data: lambda m, a: format_json_(m.error_data),
    }
