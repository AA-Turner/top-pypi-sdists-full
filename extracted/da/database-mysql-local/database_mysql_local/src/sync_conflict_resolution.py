# TODO Move everything related to sync to separate directory called sync_data_source (preferable with it's own src and tests directories)
from datetime import datetime

from .constants_src import UpdateStatus
from .generic_crud import GenericCRUD

# TODO Which packages are using it google-contact? contact-csv?
# TODO: use meta logger


class SyncConflictResolution(GenericCRUD):
    def __init__(self, default_schema_name: str = None, default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_column_name: str = None,
                 default_select_clause_value: str = "updated_timestamp",
                 default_where: str = None):
        super().__init__(default_schema_name=default_schema_name, default_table_name=default_table_name,
                         default_view_table_name=default_view_table_name,
                         default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
                         default_column_name=default_column_name,
                         default_select_clause_value=default_select_clause_value, default_where=default_where)

    def get_update_status_by_where(self, *, schema_name: str = None, view_table_name: str = None,
                                   where: str = None, params: tuple, select_clause_value: str = None,
                                   remote_last_modified_timestamp: str) -> UpdateStatus:
        """
        Get the status of the update by the where clause
        :param remote_last_modified_timestamp str
        :param params tuple
        :param schema_name str
        :param view_table_name str
        :param where str
        :param select_clause_value str
        :return str
        """
        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        where = where or self.default_where
        if not view_table_name or not where or not schema_name:
            self.logger.error("view_table_name, where or schema was not provided")
            return "error"  # TODO: why not raise?
        local_updated_timestamp = self.select_one_value_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params)
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp,
                                                                     '%Y-%m-%d %H:%M:%S')
        if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
            return UpdateStatus.UPDATE_CIRCLEZ
        elif remote_last_modified_timestamp < local_updated_timestamp:
            return UpdateStatus.UPDATE_DATA_SOURCE
        else:
            return UpdateStatus.DONT_UPDATE

    def get_update_status_by_id(self, *, schema_name: str = None, view_table_name: str = None,
                                column_name: str = None, column_value: str = None,
                                remote_last_modified_timestamp: str,
                                select_clause_value: str = None) -> UpdateStatus:
        """
        Get the status of the update by the id
        :param remote_last_modified_timestamp: str
        :param schema_name str
        :param view_table_name str
        :param column_name str
        :param column_value str
        :param select_clause_value str
        :return str
        """
        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        column_name = column_name or self.default_column_name
        if not view_table_name or not column_name or not schema_name:
            self.logger.error("view_table_name, column_name or schema was not provided")
            return "error"  # TODO: why not raise?
        local_updated_timestamp = self.select_one_value_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value)
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp,
                                                                     '%Y-%m-%d %H:%M:%S')
        if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
            return UpdateStatus.UPDATE_CIRCLEZ
        elif remote_last_modified_timestamp < local_updated_timestamp:
            return UpdateStatus.UPDATE_DATA_SOURCE
        else:
            return UpdateStatus.DONT_UPDATE

    # TODO: complete this
    def get_update_status_and_information_by_where(self, *, schema_name: str = None, view_table_name: str = None,
                                                   where: str = None, params: tuple, select_clause_value: str = "*",
                                                   remote_last_modified_timestamp: str,
                                                   local_last_modified_column_name: str) -> dict:
        """
        Get the status of the update by the where clause
        :param remote_last_modified_timestamp str
        :param params tuple
        :param schema_name str
        :param view_table_name str
        :param where str
        :param select_clause_value str
        :return dict
        """
        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        where = where or self.default_where
        if not view_table_name or not where or not schema_name:
            self.logger.error("view_table_name, where or schema was not provided")
            raise ValueError("view_table_name, where or schema was not provided")
        row_dict = self.select_one_dict_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params)
        result_dict = row_dict
        local_updated_timestamp = row_dict.get(local_last_modified_column_name)
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp,
                                                                     '%Y-%m-%d %H:%M:%S')
        if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
            result_dict["update_status"] = UpdateStatus.UPDATE_CIRCLEZ
        elif remote_last_modified_timestamp < local_updated_timestamp:
            result_dict["update_status"] = UpdateStatus.UPDATE_DATA_SOURCE
        else:
            result_dict["update_status"] = UpdateStatus.DONT_UPDATE
        return result_dict

    def get_update_status_and_information_list_by_where(self, *, schema_name: str = None,
                                                        view_table_name: str = None, where: str = None,
                                                        params: tuple, select_clause_value: str = "*",
                                                        remote_last_modified_timestamp: str,
                                                        local_last_modified_column_name: str) -> list[dict]:
        """
        Get the status of the update by the where clause
        :param remote_last_modified_timestamp str
        :param params tuple
        :param schema_name str
        :param view_table_name str
        :param where str
        :param select_clause_value str
        :return dict
        """
        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp,
                                                                     '%Y-%m-%d %H:%M:%S')
        where = where or self.default_where
        if not view_table_name or not where or not schema_name:
            self.logger.error("view_table_name, where or schema was not provided")
            raise ValueError("view_table_name, where or schema was not provided")
        row_dict_list: list[dict] = self.select_multi_dict_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params)
        result_dict_list: list[dict] = row_dict_list
        for result_dict in result_dict_list:
            local_updated_timestamp = result_dict.get(local_last_modified_column_name)
            if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
                result_dict["update_status"] = UpdateStatus.UPDATE_CIRCLEZ
            elif remote_last_modified_timestamp < local_updated_timestamp:
                result_dict["update_status"] = UpdateStatus.UPDATE_DATA_SOURCE
            else:
                result_dict["update_status"] = UpdateStatus.DONT_UPDATE
        return result_dict_list
