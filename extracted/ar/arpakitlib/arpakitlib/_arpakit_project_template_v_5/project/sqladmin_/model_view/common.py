import datetime as dt
import io
import json
from typing import Any, List

import starlette.responses
from openpyxl import Workbook
from sqladmin import ModelView

from arpakitlib.ar_datetime_util import now_utc_dt


class SimpleMV(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    page_size = 50
    page_size_options = [50, 100, 200, 500, 750, 1000]
    save_as = True
    save_as_continue = True
    export_types = ["xlsx"]
    form_include_pk = True

    async def export_data(
            self,
            data: List[Any],
            export_type: str = "csv",
    ) -> starlette.responses.StreamingResponse:
        if export_type == "xlsx":
            return await self.export_data_into_xlsx(data=data)
        else:
            return await super().export_data(data=data, export_type=export_type)

    async def export_data_into_xlsx(self, data: list[Any]) -> starlette.responses.StreamingResponse:
        wb = Workbook()
        wb.active.title = f"{self.model.__name__}"
        wb.active.append(self.get_list_columns())

        for d in data:
            wb.active.append([
                self._serialize_value_for_export_data_into_xlsx(getattr(d, column_name, ""))
                for column_name in self.get_list_columns()
            ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        filename = f"{self.model.__name__}_export_{now_utc_dt().strftime("%d.%m.%YT%H-%M-%S-%Z%z")}.xlsx"

        return starlette.responses.StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\""
            },
        )

    def _serialize_value_for_export_data_into_xlsx(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, dt.datetime):
            return value.strftime("%d.%m.%Y %H:%M:%S %Z%z")
        if isinstance(value, dt.date):
            return value.strftime("%d.%m.%Y")
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, default=str)
        return str(value)


def get_simple_mv_class() -> type[SimpleMV]:
    from project.sqladmin_.model_view import SimpleMV
    return SimpleMV


if __name__ == '__main__':
    for model_view in get_simple_mv_class().__subclasses__():
        print(model_view)
