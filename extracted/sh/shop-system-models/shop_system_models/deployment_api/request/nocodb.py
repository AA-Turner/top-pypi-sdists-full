from typing import Optional

from pydantic import BaseModel


class NocoDBConfig(BaseModel):
    nocodb_project_id: Optional[str] = None
    nocodb_categories_table: Optional[str] = None
    nocodb_products_table: Optional[str] = None
    nocodb_orders_table: Optional[str] = None
    nocodb_status_table: Optional[str] = None
    nocodb_bot_commands_table: Optional[str] = None
    nocodb_options_table: Optional[str] = ""
    nocodb_options_category_table: Optional[str] = ""
