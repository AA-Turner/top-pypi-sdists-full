from .generic_crud_ml import GenericCRUDML
from mysql.connector import ProgrammingError

from .utils import generate_id_column_name  # noqa: E402

# TODO Check the number of records in the begging and in the end in all tables involved

# is_safe mode, if not, then if null or columns don't exist then we assume test data and delete
# doubel pointing, recursive pointing

# Need to implement recursive deleting in order for this to work
DEFAULT_MAX_ROWS_TO_DELETE = 999999  # Maximum number of rows to delete at once


class DeleteTestData(GenericCRUDML):

    # the same method witht the same name in the OurOpenSearch Class
    # TODO Should not delete the line with the lowest id (i.e. we want to keep the campaign with the lowest id which is is_test_data as this campaign is used for message-send-local-python)  # noqa: E501
    def delete_test_data(self,
                         entity_name: str,
                         schema_name: str = None,
                         table_name: str = None,
                         is_safe_mode: bool = True,
                         is_interactive: bool = True):
        # TODO Shall we user self.default_schema_name or entity_name
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        print(f"Deleting test data from table_name={table_name}")
        if is_safe_mode:
            MAX_ROWS_TO_DELETE = 1
            print("Safe mode is on. Setting MAX_ROWS_TO_DELETE=" + str(MAX_ROWS_TO_DELETE))
        else:
            MAX_ROWS_TO_DELETE = DEFAULT_MAX_ROWS_TO_DELETE
            print("Safe mode is off. Setting MAX_ROWS_TO_DELETE=" + str(MAX_ROWS_TO_DELETE))
        # print('THIS IS THE CORRECT CODE')
        self.is_interactive = is_interactive
        if not self.is_interactive:
            is_safe_mode = True  # safe mode is to make sure that we delete in child tables ONLY recodres with is_test_data = 1

        gcrml = GenericCRUDML(default_entity_name=entity_name,
                              default_schema_name=schema_name,
                              default_table_name=table_name)
        # original_schema_name = self.default_schema_name
        # original_table_name = self.default_table_name
        # get a list of all the rows in the table which contain test data

        id_column_name = generate_id_column_name(table_name)
        test_data_list = gcrml.select_multi_value_by_column_and_value(select_clause_value=id_column_name,
                                                                      column_name='is_test_data',
                                                                      column_value=1,
                                                                      limit=MAX_ROWS_TO_DELETE,)

        # get a list of all the referenced tables of the main table

        select_query = """
            SELECT
              TABLE_SCHEMA,
              TABLE_NAME,
              COLUMN_NAME,
              CONSTRAINT_NAME,
              REFERENCED_TABLE_NAME,
              REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
              REFERENCED_TABLE_NAME LIKE %s
              AND REFERENCED_COLUMN_NAME = %s
              AND TABLE_NAME != %s
        """

        # params = (f'{schema_name}_table', id_column_name)
        params = (table_name, id_column_name, table_name)
        self.connection.commit()  # Ensure the connection is committed
        results = None
        try:
            self.cursor.execute(select_query, params)
            results = self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

        for row_id in test_data_list:
            for result in results:
                # print(f"Changing the schema name to {result[0]}")
                if not isinstance(result[1], str) and isinstance(result[1], bytearray):
                    result_table_name = result[1].decode()
                else:
                    result_table_name = result[1]

                if not isinstance(result[0], str) and isinstance(result[0], bytearray):
                    result_schema_name = result[0].decode()
                else:
                    result_schema_name = result[0]

                gcrml1 = GenericCRUDML(default_entity_name=entity_name,
                                       default_schema_name=result_schema_name,
                                       default_table_name=result_table_name)
                # rint(f"Changing the table name to {result[1]}")
                gcrml1.default_table_name = result_table_name
                if result_table_name.endswith('table'):
                    gcrml1.default_view_table_name = result_table_name.replace("table", "with_deleted_and_test_data_view")
                if result_table_name.endswith('old'):
                    continue
                if is_safe_mode:
                    global to_delete
                    try:
                        id_column_name = generate_id_column_name(result_table_name)
                        to_delete = gcrml1.select_multi_value_by_column_and_value(
                            select_clause_value="is_test_data",
                            column_name=id_column_name,
                            column_value=row_id,
                            view_table_name=gcrml1.default_view_table_name,
                            limit=MAX_ROWS_TO_DELETE,)
                    except ProgrammingError as e:
                        if e.errno == 1054:
                            print(
                                f"The column is_test_data does not exist in {gcrml1.default_table_name}. This column will be added to the table now.")
                            try:
                                gcrml1.create_column(schema_name=gcrml1.default_schema_name,
                                                     table_name=gcrml1.default_table_name,
                                                     column_name='is_test_data',
                                                     data_type='TINYINT',
                                                     default_value=0)
                            except ProgrammingError as e:
                                try:
                                    print("exception: ", e)
                                    gcrml1.create_view()
                                except ProgrammingError as e:
                                    print("exception: ", e)
                                    continue

                            to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value="is_test_data",
                                                                                      column_name=id_column_name,
                                                                                      column_value=row_id,
                                                                                      view_table_name=gcrml1.default_view_table_name,
                                                                                      limit=MAX_ROWS_TO_DELETE,)
                            continue
                        elif e.errno == 1146:
                            # print(f"At this point the default_schema_name is {gcrml1.default_schema_name}")
                            gcrml1.create_view(
                                schema_name=gcrml1.default_schema_name,
                                table_name=gcrml1.default_table_name,
                                view_name=gcrml1.default_view_table_name,
                            )
                            # print(f"view_created: {gcrml1.default_view_table_name}")
                            to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value="is_test_data",
                                                                                      column_name=id_column_name,
                                                                                      column_value=row_id,
                                                                                      view_table_name=gcrml1.default_view_table_name,
                                                                                      limit=MAX_ROWS_TO_DELETE,)
                            continue
                    for entry in to_delete:
                        if entry == 1:
                            delete_query = f"""
                            DELETE from {result_schema_name}.{result_table_name}
                            WHERE {result[2]} = {row_id} and is_test_data = 1;
                            """
                            if self.is_interactive:
                                if self.ask_user_confirmation(delete_query) == 'yes':
                                    self.cursor.execute(delete_query)
                            else:
                                # print(delete_query)
                                self.cursor.execute(delete_query)

                            # self.delete_test_data(
                            #     schema_name=result[0],
                            #     table_name=result[1],
                            #     is_safe_mode=True,
                            #     is_interactive=is_interactive,
                            # )
                        else:
                            print("ERROR: Trying to delete non-test-data")
                else:
                    to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value=id_column_name,
                                                                              column_name=id_column_name,
                                                                              column_value=row_id,
                                                                              view_table_name=gcrml1.default_view_table_name,
                                                                              limit=MAX_ROWS_TO_DELETE,)

                for entry in to_delete:
                    id_column_name = generate_id_column_name(result_table_name)
                    delete_query = f"""
                    DELETE from {result_schema_name}.{result_table_name}
                    WHERE {id_column_name} = {row_id};
                    """
                    # WHERE {original_schema_name}_id = {row_id};

                    if self.is_interactive:
                        if self.ask_user_confirmation(delete_query) == 'yes':
                            self.cursor.execute(delete_query)
                    else:
                        self.cursor.execute(delete_query)
            # If no errors, delete from the original table
            # delete_query = f"""DELETE from {original_schema_name}.{original_table_name} Where {original_schema_name}_id = {row_id};"""
            id_column_name = generate_id_column_name(table_name)
            delete_query = f"""DELETE from {schema_name}.{table_name} Where {id_column_name} = {row_id};"""
            if self.is_interactive:
                if self.ask_user_confirmation(delete_query) == 'yes':
                    self.cursor.execute(delete_query)
            else:
                # print(delete_query)
                self.cursor.execute(delete_query)
        self.connection.commit()

        delete_results = {}
        delete_results['schema_name'] = schema_name
        delete_results['table_name'] = table_name
        delete_results['deleted_rows'] = len(test_data_list)

        print(f"Deleted {delete_results['deleted_rows']} rows from {delete_results['schema_name']}.{delete_results['table_name']}")
        return delete_results

    def ask_user_confirmation(self, sql_query):
        global user_preference
        print(f"SQL Query:\n{sql_query}")
        user_choice = input("Do you want to execute this query? (yes/no/all): ").strip().lower()
        if user_choice in ['yes', 'no']:
            user_preference = (user_choice == 'yes')
            return user_preference
        elif user_choice in ['all']:
            self.is_interactive = False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            message = self.ask_user_confirmation(sql_query)
            return message
