from .generic_crud import GenericCRUD


class GenericCrudMysql(GenericCRUD):
    # def __init__(self, *, default_schema_name: str,
    #              default_table_name: str = None,
    #              default_view_table_name: str = None,
    #              default_view_with_deleted_and_test_data: str = None,
    #              default_column_name: str = None,
    #              default_select_clause_value: str = "*",
    #              default_where: str = None, is_test_data: bool = False) -> None:
    #     # TODO I'm not sure this is the right solution for backward compatability, I think we should rename the existing class to the new name and create new class with the original name.
    #     super()
    pass
