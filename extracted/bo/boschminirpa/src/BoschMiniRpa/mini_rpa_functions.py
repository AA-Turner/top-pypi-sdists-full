import os
import io
from email.utils import formataddr

import pandas as pd

from mini_rpa_hrs_customized_functions import *
from BoschRpaMagicBox.remote_excel_functions import *
from BoschRpaMagicBox.helper_functions import *
from mini_rpa_sap_automation import *


class MiniRpaFunction(MiniRPACore):
    """This class is used to process single RPA task"""

    def __init__(self, user_name: str, user_password: str, server_name: str, share_name: str, port: int,
                 from_period: str, to_period: str, report_save_path: str, report_process_folder_path: str, report_period_type: str,
                 process_number: int, process_dict: dict, delivery_dict: dict, sap_operation_list: list, database_operation_list: list, update_file_condition_setting: list,
                 from_file_condition_setting: list, data_type_dict: dict, download_data=False, process_data: bool = False, delivery_data: bool = False,
                 process_database: bool = False, file_name_suffix_format='YearMonthDay', common_field_dict=None):
        """This function is used to initial parameters

        Args:
            user_name(str): This is the username
            user_password(str): This is the password
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            port(int): This is the port number of the server name
            from_period(str):This is the start month
            to_period(str): This is the end month
            report_process_folder_path(str): This is the file path for process Excel
            report_period_type(str): This is the report period type. e.g. period, current_date
            report_save_path(str): This is the folder path for original data
            delivery_data(bool): This is the indicator whether to delivery files to folders, receivers or api
            download_data(bool): This is the indicator whether to do sap operation
            process_data(bool): This is the indicator whether to process data
            data_type_dict(dict): This is the dict that save the data type
            sap_operation_list: This is the list of sap operation
            process_number(int): This is the number of process
            process_dict(dict): This is the dict that save the process logic data
            delivery_dict(dict): This is the dict that save the delivery logic data
            update_file_condition_setting(list): This is the list of update file condition setting
            from_file_condition_setting(list): This is the list of from file condition setting
            common_field_dict(dict): This is the dict that save the common field data
        """
        super().__init__(user_name, user_password, server_name, share_name, port, from_period, to_period, report_save_path,
                         report_process_folder_path, report_period_type, process_number, process_dict, delivery_dict,
                         sap_operation_list, database_operation_list, update_file_condition_setting, from_file_condition_setting, data_type_dict, download_data, process_data,
                         delivery_data, process_database, file_name_suffix_format, common_field_dict)

    def keep(self, from_file_path: str, from_file_name: str, from_sheet_name: str, process_number: int, is_save: bool, has_from_file_condition: bool) \
            -> None:
        """This function is used to remove data from loaded file

        Args:
            from_file_path(str): This is the file path of target Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            process_number(int): This is the process number
            is_save(bool): This is indicator whether to save processed data
            from_file_name(str): This is the file name of current file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
        """

        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, keep_data, keep_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            self.save_file(process_number, from_file_name, keep_dtype_dict, keep_data, 'keep', from_sheet_name, is_save)
            del keep_data

    def vlookup(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_column_by: str, update_file_path: str,
                update_file_name: str, update_sheet_name: str, update_column_name: str, update_column_by: str, has_from_file_condition: bool, has_update_file_condition: bool,
                is_save: bool) -> None:
        """This function is used to vlookup data between two Excel sheets

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target excel file that is vlookuped
            from_file_name(str): This is the file name of excel file that is vlookuped
            from_sheet_name(str): This is the sheet name of excel file that is vlookuped
            from_column_name(str): This is the column name to be vlookuped of from file
            from_column_by(str): This is the by column of from file
            update_file_path(str): This is the file path of target excel file that vlookup
            update_file_name(str): This is the file name of excel file that vlookup
            update_sheet_name(str): This is the sheet name of excel file that vlookup
            update_column_name(str): This is the column name to be created in update file
            update_column_by(str): This is the by column of update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            has_update_file_condition(bool): This is the syntax dict for update file
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        is_update_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port)

        vlookup_data = None
        if is_from_file_exist and is_update_file_exist:
            original_update_data, update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, has_update_file_condition,
                                                                                                'update_file')
            original_from_data, from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            from_column_list = from_column_name.replace('，', ',').split(',')
            update_column_list = update_column_name.replace('，', ',').split(',')
            if from_column_by != update_column_by and from_column_by in update_data.columns:
                from_data = from_data.rename(columns={from_column_by: f'From_{from_column_by}'})
                from_column_by = f'From_{from_column_by}'
            column_rename_dict = dict(zip(from_column_list, update_column_list))
            from_data = from_data.loc[:, [from_column_by, *from_column_list]]
            from_data = from_data.rename(columns=column_rename_dict)
            from_data = from_data.drop_duplicates(subset=[from_column_by])
            update_data['index_bk'] = update_data.index
            vlookup_data = pd.merge(update_data, from_data, how='left', left_on=update_column_by, right_on=from_column_by)
            vlookup_data.set_index('index_bk', inplace=True, drop=False)
            vlookup_data = vlookup_data.drop(['index_bk'], axis=1)
            if update_column_by != from_column_by:
                vlookup_data = vlookup_data.drop([from_column_by], axis=1)

            vlookup_data = self.update_dataframe(original_update_data, vlookup_data)
            self.save_file(process_number, update_file_name, update_dtype_dict, vlookup_data, 'vlookup', update_sheet_name, is_save)

        elif is_update_file_exist:
            original_update_data, update_data, update_dtype_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, has_update_file_condition,
                                                                                                'update_file')
            vlookup_data = update_data
            update_column_list = update_column_name.replace('，', ',').split(',')
            for column in update_column_list:
                vlookup_data[column] = ''

            vlookup_data = self.update_dataframe(original_update_data, vlookup_data)
            self.save_file(process_number, update_file_name, update_dtype_dict, vlookup_data, 'vlookup', update_sheet_name, is_save)
        del vlookup_data

    def rename_column_names(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, update_column_name: str,
                            is_save: bool) -> None:
        """This function is used to vlookup data between two Excel sheets

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target excel file that is vlookuped
            from_file_name(str): This is the file name of excel file that is vlookuped
            from_sheet_name(str): This is the sheet name of excel file that is vlookuped
            from_column_name(str): This is the column name to be vlookuped of from file
            update_column_name(str): This is the column name to be created in update file
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)

        if is_from_file_exist:
            _, from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, False, 'from_file')

            from_column_list = from_column_name.replace('，', ',').split(',')
            update_column_list = update_column_name.replace('，', ',').split(',')
            column_rename_dict = dict(zip(from_column_list, update_column_list))
            column_rename_data = from_data.rename(columns=column_rename_dict)
            self.save_file(process_number, from_file_name, from_dtype_dict, column_rename_data, 'rename_column_names', from_sheet_name, is_save)

            del column_rename_data

    def copy_to_new(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, update_file_name: str,
                    update_sheet_name: str, update_column_name: str, has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to copy data and paste to new created file

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file that is copied
            from_file_name(str): This is the file name of Excel file that is copied
            from_sheet_name(str): This is the sheet name of Excel file that is copied
            from_column_name(str): This is the column name to be copied of from file
            update_file_name(str): This is the file name of Excel file that need copied data
            update_sheet_name(str): This is the sheet name of Excel file that vlookup
            update_column_name(str): This is the column name to be created in update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_copy_data, copy_data, copy_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            update_column_list = update_column_name.replace('，', ',').split(',')
            from_column_list = from_column_name.replace('，', ',').split(',')
            column_dict = dict(zip(from_column_list, update_column_list))
            copy_data = copy_data.loc[:, from_column_list]
            copy_data = copy_data.rename(columns=column_dict)
            self.save_file(process_number, update_file_name, copy_dtype_dict, copy_data, 'copy to new', update_sheet_name, is_save)
            del copy_data

    def replace(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, original_value: str,
                replace_value: str, has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to replace values with new values in specific columns

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file
            from_file_name(str): This is the file name of Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            from_column_name(str): This is the column name of from file whose value will be replaced
            original_value(str): This is the value or regular expression
            replace_value(str): This is the value to replace original value
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_replace_data, replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition,
                                                                                                   'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')
            if not replace_value:
                replace_value = ''
            for column in from_column_list:
                replace_data[column] = replace_data[column].str.replace(original_value, replace_value, regex=True)

            replace_data = self.update_dataframe(original_replace_data, replace_data)
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'replace', from_sheet_name, is_save)
            del replace_data

    def replace_empty_value(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                            replace_value: str, has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to replace empty values with new values in specific columns

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file
            from_file_name(str): This is the file name of Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            from_column_name(str): This is the column name of from file whose empty values will be replaced
            replace_value(str): This is the value to replace original value
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save(bool): This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_replace_data, replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition,
                                                                                                   'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')

            for column in from_column_list:
                replace_data[column] = replace_data[column].fillna(replace_value)
                empty_value_data_flag = replace_data[column] == ''
                replace_data.loc[empty_value_data_flag, column] = replace_value

            replace_data = self.update_dataframe(original_replace_data, replace_data)
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'replace empty value', from_sheet_name, is_save)
            del replace_data

    def combine_new_column(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                           new_column_name: str, has_from_file_condition: bool, is_save: bool, separator='') -> None:
        """This function is used to create a new column by combine target column or columns

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be combined into new_column
            new_column_name: This is the new column that is combined from from_column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data
            separator(str): This is the separator to be used for combining values, default is empty string
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_combine_data, combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition,
                                                                                                   'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')

            # fill missing, convert to str, join with separator
            combine_data[new_column_name] = combine_data[from_column_list].fillna('').astype(str).agg(separator.join, axis=1)

            # combine_data[new_column_name] = ''
            # for column_index, column_name in enumerate(from_column_list):
            #     temp_column_name = f'{column_name}_temp'
            #     # combine_data[column_name] = combine_data[column_name].fillna('')
            #     combine_data[temp_column_name] = combine_data[column_name]
            #     combine_data[temp_column_name] = combine_data[temp_column_name].astype(str)
            #     combine_data[temp_column_name] = combine_data[temp_column_name].fillna('')
            #
            #     if column_index == 0:
            #         combine_data[new_column_name] = combine_data[new_column_name] + combine_data[temp_column_name]
            #     else:
            #         combine_data[new_column_name] = combine_data[new_column_name] + separator + combine_data[temp_column_name]
            #
            # for column_name in from_column_list:
            #     temp_column_name = f'{column_name}_temp'
            #     if temp_column_name in combine_data.columns:
            #         combine_data = combine_data.drop([temp_column_name], axis=1)

            combine_data = self.update_dataframe(original_combine_data, combine_data)
            self.save_file(process_number, from_file_name, combine_dtype_dict, combine_data, 'combine new column', from_sheet_name, is_save)
            del combine_data

    def create_new_columns(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, new_column_name: str, is_save: bool) -> None:
        """This function is used to create a new column

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            new_column_name: This is the new column that is combined from from_column
            is_save: This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, new_column_data, new_column_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, False,
                                                                                     'from_file')

            new_column_name_list = new_column_name.replace('，', ',').strip().split(',')
            existed_column_set = set(list(new_column_data.columns))
            for column_name in new_column_name_list:
                if column_name not in existed_column_set:
                    new_column_data[column_name] = ''
            self.save_file(process_number, from_file_name, new_column_dtype_dict, new_column_data, 'create new column', from_sheet_name, is_save)
            del new_column_data

    def delete_excel_file_columns(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, delete_column_name: str, is_save: bool) -> None:
        """This function is used to create a new column

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            delete_column_name: This is the new column that will be deleted
            is_save: This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, delete_column_data, delete_column_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, False,
                                                                                           'from_file')

            delete_column_name_list = delete_column_name.replace('，', ',').strip().split(',')
            existed_column_set = set(list(delete_column_data.columns))
            for column_name in delete_column_name_list:
                if column_name in existed_column_set:
                    delete_column_data = delete_column_data.drop([column_name], axis=1)
            self.save_file(process_number, from_file_name, delete_column_dtype_dict, delete_column_data, 'delete column', from_sheet_name, is_save)
            del delete_column_data

    def delete_excel_file_rows(self, process_number: int, from_file_path: str, from_sheet_name: str, row_number: str) -> None:
        """This function is used to create a new column

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_sheet_name: This is the sheet name of Excel file
            row_number: This is the row number that will be deleted, e.g. 1,2,3
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            row_number_list = row_number.replace('，', ',').strip().split(',')
            row_number_list = [int(row) for row in row_number_list if row.strip().isdigit()]
            if row_number_list:
                delete_excel_rows(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, from_sheet_name, row_number_list, 445)

    def assign_value_to_target_column(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, assign_value_type: str,
                                      copy_column_name: str, constant_value: str, has_from_file_condition: bool, is_save: bool):
        """ This function is used to assign a value to target column

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be filled
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data
            assign_value_type(str): copy_column_value or constant_value
            copy_column_name(str): This is the column name to be copied if assign_value_type is copy_column_value
            constant_value(str): This is the constant value to be assigned if assign_value_type is constant_value
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_assign_value_data, assign_value_data, assign_value_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name,
                                                                                                                  has_from_file_condition, 'from_file')
            if assign_value_type == 'copy_column_value':
                assign_value_data[from_column_name] = assign_value_data[copy_column_name]
            elif assign_value_type == 'constant_value':
                assign_value_data[from_column_name] = constant_value

            assign_value_data = self.update_dataframe(original_assign_value_data, assign_value_data)
            self.save_file(process_number, from_file_name, assign_value_dtype_dict, assign_value_data, 'assign value to target column', from_sheet_name, is_save)
            del assign_value_data

    def split_to_new_file(self, from_file_path: str, from_file_name: str, from_sheet_name: str, from_group_by_column: str, process_number: int,
                          has_from_file_condition: bool) -> None:
        """This function is used to split data into different files according to key columns

        Args:
           from_file_path: This is the file path of target Excel file
           from_file_name: This is the file name of Excel file
           from_sheet_name: This is the sheet name of Excel file
           from_group_by_column: This is the column name to be used as group by key
           process_number: This is the process number
           has_from_file_condition: This indicates whether current process has additional condition settings

        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, split_data, split_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            split_data[from_group_by_column] = split_data[from_group_by_column].fillna('')
            split_data = split_data.groupby(by=[from_group_by_column])
            for split_column, split_column_data in split_data:
                split_file_name = from_file_name.split('.')[0] + f'_{split_column[0]}.xlsx'
                split_file_path = from_file_path.split('.')[0] + f'_{split_column[0]}.xlsx'
                smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, split_file_path, self.port)

                self.save_file(process_number, split_file_name, split_dtype_dict, split_column_data, 'split to new file', from_sheet_name, True)
            del split_data

    def column_calculate(self, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, new_column_name: str, process_number: int,
                         has_from_file_condition: bool, is_save: bool, function_type: str, calculate_value: str = '') -> None:
        """This function is used to process values of different columns and create a new column to save result

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name of from file whose values will be calculated into new_column
            new_column_name: This is the new column that is combined by from_column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: whether to save file
            function_type: This is the function type, e.g. add, minus
            calculate_value(str): This is the value to be + - * /
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_combine_data, combine_data, combine_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition,
                                                                                                   'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')
            combine_data[new_column_name] = combine_data[from_column_list[0]]
            calculate_value_list = [value.strip() for value in calculate_value.replace('，', ',').split(',') if value.strip()]

            # calculation among columns
            for column in from_column_list[1:]:
                if function_type == 'column_addition':
                    combine_data[new_column_name] = combine_data[new_column_name].add(combine_data[column], fill_value=0)
                if function_type == 'column_deduction':
                    combine_data[new_column_name] = combine_data[new_column_name].sub(combine_data[column], fill_value=0)
                if function_type == 'column_multiply':
                    combine_data[new_column_name] = combine_data[new_column_name].multiply(combine_data[column], fill_value=1)
                if function_type == 'column_divide':
                    combine_data[new_column_name] = combine_data[new_column_name].divide(combine_data[column], fill_value=1)

            # calculation with fixed value
            if calculate_value_list:
                for str_calculate_value in calculate_value_list:
                    try:
                        float_calculate_value = round(float(str_calculate_value), 2)
                        if function_type == 'column_addition':
                            combine_data[new_column_name] = combine_data[new_column_name] + float_calculate_value
                        if function_type == 'column_deduction':
                            combine_data[new_column_name] = combine_data[new_column_name] - float_calculate_value
                        if function_type == 'column_multiply':
                            combine_data[new_column_name] = combine_data[new_column_name] * float_calculate_value
                        if function_type == 'column_divide':
                            float_calculate_value = float_calculate_value if float_calculate_value else 1
                            combine_data[new_column_name] = combine_data[new_column_name] / float_calculate_value
                    except ValueError:
                        pass

            combine_data = self.update_dataframe(original_combine_data, combine_data)
            self.save_file(process_number, from_file_name, combine_dtype_dict, combine_data, function_type, from_sheet_name, is_save)
            del combine_data

    def copy_to_exist(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, update_file_path: str,
                      update_sheet_name: str, update_column_name: str, has_from_file_condition: bool):
        """This function is used to copy target column to existed Excel file

        Args:
            process_number(int): This is the process number
            from_file_path(str): This is the file path of target Excel file path that is copied
            from_file_name(str): This is the file name of Excel file that is copied
            from_sheet_name(str): This is the sheet name of Excel file that is copied
            from_column_name(str): This is the column name to be copied of from file
            update_column_name(str): This is the column name to be located in update file
            has_from_file_condition(bool): This indicates whether current process has additional condition settings
            update_file_path(str):This is the file path of  Excel file path that save copy columns
            update_sheet_name(str): This is the sheet name of Excel file that save copy data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        is_update_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port)

        if is_from_file_exist and is_update_file_exist:
            original_from_data, from_data, from_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            from_column_list = [column.strip() for column in from_column_name.replace('，', ',').split(',')]
            update_column_list = [column.strip() for column in update_column_name.replace('，', ',').split(',')]
            print(f'---------------copy to exist result of process no {process_number}---------------')

            from_data_columns = set(list(from_data.columns))
            for column_name, column_type in from_dtype_dict.items():
                if column_name in from_data_columns:
                    from_data[column_name] = from_data[column_name].astype(column_type)

            column_name_dict = dict(zip(from_column_list, update_column_list))
            append_flexible_dataframe_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path,
                                                 update_sheet_name, from_data, column_name_dict, self.port, True, True)
            self.save_file(process_number, from_file_name, from_dtype_dict, original_from_data, 'copy_to_exist', from_sheet_name)
            del from_data

    def date_transfer(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                      has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to transfer date format


        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be transferred into date format
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data

        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_date_data, date_data, date_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            if date_data is not None and not date_data.empty:
                from_column_list = from_column_name.replace('，', ',').split(',')
                for column in from_column_list:
                    date_data[column] = date_data[column].fillna('')
                    date_data[column] = date_data[column].astype(str).str.strip()
                    date_data[column] = date_data[column].apply(self.string_date_parser)

                # date_data = self.update_dataframe(original_date_data, date_data)
                self.save_file(process_number, from_file_name, date_dtype_dict, date_data, 'date_transfer', from_sheet_name, is_save)
                del date_data

    def date_transfer_date_format(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                                  has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to transfer date format


        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name whose values will be transferred into date format
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data

        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_date_data, date_data, date_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            if date_data is not None and not date_data.empty:
                from_column_list = from_column_name.replace('，', ',').split(',')
                for column in from_column_list:
                    date_data[column] = date_data[column].fillna('')
                    date_data[column] = date_data[column].astype(str).str.strip()
                    date_data[column] = date_data[column].apply(self.prepare_date_info)

                # date_data = self.update_dataframe(original_date_data, date_data)
                self.save_file(process_number, from_file_name, date_dtype_dict, date_data, 'date_transfer_date_format', from_sheet_name, is_save)
                del date_data

    def remove_duplicates(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                          has_from_file_condition: bool, keep_config: Union[str, bool], is_save: bool) -> None:
        """This function is used to remove duplicate values

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose values will be removed duplicates
            has_from_file_condition(bool):This indicates whether current process has additional condition settings
            is_save:This is indicator whether to save processed data
            keep_config(Union[str, False]): first, last or False
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, duplicate_data, duplicate_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')
            duplicate_data = duplicate_data.drop_duplicates(subset=from_column_list, keep=keep_config)
            self.save_file(process_number, from_file_name, duplicate_dtype_dict, duplicate_data, 'remove_duplicates', from_sheet_name, is_save)
            del duplicate_data

    def sort_values(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                    has_from_file_condition: bool, is_ascending: bool, is_save: bool) -> None:
        """This function is used to sort values

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose value will be sorted
            has_from_file_condition(bool):This indicates whether current process has additional condition settings
            is_save:This is indicator whether to save processed data
            is_ascending(bool): This is the indicator whether to sort values in ascending order
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, sort_values_data, sort_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')
            sort_values_data = sort_values_data.sort_values(by=from_column_list, ascending=is_ascending)

            self.save_file(process_number, from_file_name, sort_dtype_dict, sort_values_data, 'sort_values', from_sheet_name, is_save)
            del sort_values_data

    def contain_condition_replace(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_contain_column: str,
                                  original_value: str, replace_value: str, has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to replace values with new values in specific columns after filtering data by using string contain function

        Args:
             process_number: This is the process number
             from_file_path: This is the file path of target Excel file path that is processed
             from_file_name: This is the file name of Excel file that is processed
             from_sheet_name: This is the sheet name of Excel file that is processed
             from_column_name: This is the column name to be processed of from file
             from_contain_column: This is the column name to be used for filtering
             original_value: This is the value or regular expression
             replace_value: This is the value to replace original value
             has_from_file_condition: This indicates whether current process has additional condition settings
             is_save: This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_replace_data, replace_data, replace_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition,
                                                                                                   'from_file')
            replace_data_status = replace_data[from_contain_column].str.contains(original_value, na=False, regex=False)
            replace_data.loc[replace_data_status, from_column_name] = replace_value

            replace_data = self.update_dataframe(original_replace_data, replace_data)
            self.save_file(process_number, from_file_name, replace_dtype_dict, replace_data, 'condition replace', from_sheet_name, is_save)
            del replace_data

    def group_by(self, process_number: int, from_file_path: str, from_file_name: str, update_file_name: str, from_sheet_name: str, update_sheet_name: str,
                 from_column_name: str, from_group_by_column: str, group_by_config: str, has_from_file_condition: bool, is_save: bool) -> None:
        """This function is used to aggregate data according to condition

        Args:
            process_number: This is the process number
            from_file_path: This is the file path of target Excel file
            from_file_name: This is the file name of Excel file
            update_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            update_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name to be vlookuped of from file
            from_group_by_column: This is the column name to be used fill in from column
            has_from_file_condition: This indicates whether current process has additional condition settings
            is_save: This is indicator whether to save processed data
            group_by_config(str): sum or count
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, group_by_data, group_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            from_column_list = from_column_name.replace('，', ',').split(',')
            from_column_by_list = from_group_by_column.replace('，', ',').split(',')
            group_by_data = group_by_data.loc[:, from_column_by_list + from_column_list]
            if group_by_config == 'sum':
                group_by_data = group_by_data.groupby(by=from_column_by_list, as_index=False, dropna=False).sum()
            elif group_by_config == 'count':
                group_by_data = group_by_data.groupby(by=from_column_by_list, as_index=False, dropna=False).count()

            for from_column_name in from_column_list:
                if from_column_name not in group_by_data.columns:
                    group_by_data[from_column_name] = ''

            self.save_file(process_number, update_file_name, group_dtype_dict, group_by_data, 'group_by', update_sheet_name, is_save)
            del group_by_data

    def column_compare(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, from_compare_column: str,
                       has_from_file_condition: bool, new_column_name: str, compare_result_value: str, is_save: bool) -> None:
        """This function is used to compare values of two different columns and create new column to record compare result

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name whose value will be compared with from_compare_column
            has_from_file_condition:This indicates whether current process has additional condition settings
            new_column_name: This is the new column that will record compare result
            is_save:This is indicator whether to save processed data
            from_compare_column: This is the column name to be compared
            compare_result_value: This is the value to be updated in new_column
        """
        compare_result_value = compare_result_value.replace('，', ',')
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_column_compare_data, column_compare_data, column_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name,
                                                                                                                has_from_file_condition, 'from_file')
            positive_result = compare_result_value.replace('，', ',').split(',')[0]
            negative_result = compare_result_value.replace('，', ',').split(',')[1]
            positive_compare_flag = column_compare_data[from_compare_column] == column_compare_data[from_column_name]
            negative_compare_flag = column_compare_data[from_compare_column] != column_compare_data[from_column_name]
            column_compare_data.loc[positive_compare_flag, new_column_name] = positive_result
            column_compare_data.loc[negative_compare_flag, new_column_name] = negative_result

            column_compare_data = self.update_dataframe(original_column_compare_data, column_compare_data)
            self.save_file(process_number, from_file_name, column_dtype_dict, column_compare_data, 'column_compare', from_sheet_name, is_save)
            del column_compare_data

    def calculate_anniversary_duration(self, process_number: int, from_file_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str,
                                       has_from_file_condition: bool, new_column_name: str, is_save: bool) -> None:
        """This function is used to calculate time difference between values of from column and today (anniversary duration)

        Args:
            process_number:This is the process number
            from_file_path:This is the file path of target Excel file
            from_file_name:This is the file name of Excel file
            from_sheet_name:This is the sheet name of Excel file
            from_column_name:This is the column name
            has_from_file_condition:This indicates whether current process has additional condition settings
            new_column_name: This is the new column that will record compare result
            is_save:This is indicator whether to save processed data
        """
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            original_time_data, time_data, time_dtype_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')
            time_data = hrs_calculate_duration(time_data, from_column_name, self.from_period, new_column_name)

            time_data = self.update_dataframe(original_time_data, time_data)
            self.save_file(process_number, from_file_name, time_dtype_dict, time_data, 'calculate_anniversary_duration', from_sheet_name, is_save)
            del time_data

    def hrs_copy_excel_files(self, from_folder_path: str, from_file_name: str, update_folder_path: str):
        """This function is used to copy files from from_folder or sub_folder of from folder to update folder

        Args:
            from_folder_path: This is the from_folder_path
            from_file_name: This is the file name that contains common file name fragment
            update_folder_path: This is the target folder path

        """
        traverse_result_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, from_folder_path, self.port)
        sub_folder_list = [folder_item for folder_item in traverse_result_list if folder_item['is_folder']]

        sub_folder_list.sort(key=lambda folder_item: folder_item['creation_time'])
        sub_folder_list = [folder_item['name'] for folder_item in sub_folder_list]

        print(f'--------------- copy files ---------------')
        if sub_folder_list:
            if self.from_period:
                transformed_date = MiniRPACore.prepare_date_info(self.from_period)
                if transformed_date is not None:
                    transformed_year = transformed_date.year
                    transformed_month = str(transformed_date.month).rjust(2, '0')
                    target_folder_path = from_folder_path + os.sep + f'{transformed_year}.{transformed_month}'
                else:
                    target_folder_path = from_folder_path + os.sep + sub_folder_list[-1]
            else:
                target_folder_path = from_folder_path + os.sep + sub_folder_list[-1]
            file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, target_folder_path, self.port)
            target_file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]
            for file_name in target_file_name_list:
                upper_file_name = file_name.upper()
                if from_file_name.upper() in upper_file_name and '.XLS' in upper_file_name:
                    print(f'--------------- copy file for {target_folder_path + os.sep + file_name} ---------------')
                    from_file_path = target_folder_path + os.sep + file_name
                    update_file_path = update_folder_path + os.sep + file_name
                    from_file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
                    smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, from_file_obj, self.port)
        else:
            print('Target folder is not found！')

    def combine_excel_files(self, from_folder_path: str, from_file_name: str, from_sheet_name: str, update_folder_path: str, update_file_name: str, update_sheet_name: str,
                            process_number: int):
        """This function is used to combine files from from_folder or sub_folder of from folder ,then save to update folder

        Args:
            from_folder_path: This is the from_folder_path
            from_file_name: This is the file name that contains common file name fragment
            update_folder_path: This is the target folder path
            from_sheet_name: This is the sheet name of from_file
            update_file_name: This is the file name of update file
            update_sheet_name:This is the sheet name to be saved
            process_number: This is the process number
        """
        file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, from_folder_path, self.port)
        target_file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]
        combine_data_list = []
        from_sheet_list = from_sheet_name.replace('，', ',').split(',')
        for file_name in target_file_name_list:
            upper_file_name = file_name.upper()
            if from_file_name.upper() in upper_file_name and '.XLS' in upper_file_name:
                file_path = from_folder_path + os.sep + file_name
                for from_sheet_name in from_sheet_list:
                    try:
                        file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
                        from_file_data = pd.read_excel(file_obj, sheet_name=from_sheet_name, dtype=str)
                    except ValueError:
                        pass
                    else:
                        combine_data_list.append(from_file_data)
                        break
        print(f'--------------- combine files ---------------')
        if combine_data_list:
            combine_data = pd.concat(combine_data_list, ignore_index=True)
            combine_data_save_path = update_folder_path + os.sep + f'{process_number}_combine_excel_files_{update_file_name}'

            file_obj = BytesIO()
            with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
                combine_data.to_excel(writer, index=False, float_format='%.2f', sheet_name=update_sheet_name)
            file_obj.seek(0)
            smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, combine_data_save_path, file_obj, self.port)
            del combine_data

    def copy_value_to_range(self, process_number: int, from_folder_path: str, from_file_name: str, from_sheet_name: str, from_column_name: str, has_from_file_condition: bool,
                            update_folder_path: str, update_file_name: str, update_sheet_name: str, update_range: str) -> None:
        """This function is used to copy dataframe value to range/ranges of Excel file

        Args:
            process_number: This is the process number
            from_folder_path: This is the folder path of target Excel file
            from_file_name: This is the file name of Excel file
            update_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            from_column_name: This is the column name to be saved in update_file_sheet
            has_from_file_condition: This indicates whether current process has additional condition settings
            update_folder_path: This is the folder path where update file is located
            update_file_name: This is the file name of update file
            update_sheet_name: This is the sheet name of update file
            update_range: This is the range name in the update sheet. e.g. A1, B1

        """
        from_file_path = from_folder_path + os.sep + from_file_name
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, target_data, target_data_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            from_column_list = from_column_name.replace('，', ',').split(',')
            new_target_data = target_data.loc[:, from_column_list]
            for column_name, column_type in target_data_dict.items():
                if column_name in new_target_data.columns and column_type == str:
                    new_target_data[column_name] = "'" + new_target_data[column_name]

            update_file_path = update_folder_path + os.sep + update_file_name
            save_dataframe_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, update_sheet_name, new_target_data,
                                      update_range, False, self.port)
            del target_data

    def delete_files(self, all_from_file_name):
        """This function is used to delete file

        Args:
            all_from_file_name(str): This is the file name who will be deleted.It is seperated by ','
        """
        file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, self.report_save_path, self.port)
        file_name_list = [file_item['name'] for file_item in file_name_list if file_item['is_file']]

        for from_file_name in all_from_file_name.replace('，', ',').split(','):
            from_file_name = from_file_name.strip()
            if from_file_name:
                for existed_file_name in file_name_list:
                    if from_file_name in existed_file_name:
                        file_path = self.report_save_path + os.sep + existed_file_name
                        try:
                            smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
                            print(f'-----{file_path} is deleted successfully!-----')
                        except:
                            print(f'Failed to delete： {file_path}')

    def send_email(self, email_account: str, email_password: str, email_address: str, email_body: str, email_header: str, email_subject: str, email_to: list, email_cc: list,
                   attachment_name_list: list, email_bcc: list = None):
        """This function is used to send emails

        Args:
            email_account(str): This is the email account
            email_password(str): This is the email password for nt account
            email_address(str): This is the email address of nt account
            email_body(str): This is the email content
            email_header(str): This is the customized sender name instead of actual user nt
            email_subject(str): This is the email subject
            email_to(list): This is the list of to emails
            email_cc(list): This is the list of cc emails
            attachment_name_list(list): This is the list of attachment name.
            email_bcc(list): This is the list of bcc emails
        """
        mail_host = 'rb-smtp-auth.rbesz01.com'
        mail_user = email_account
        mail_pass = email_password
        sender = email_address

        try:
            smtp_obj = smtplib.SMTP(mail_host, 25)
            smtp_obj.starttls()
            smtp_obj.login(mail_user, mail_pass)
            receivers = ','.join(email_to)
            ccs = ','.join(email_cc)

            message = MIMEMultipart()
            if email_header.strip():
                message["From"] = Header(email_header, "utf-8")
            else:
                message['From'] = formataddr((str(Header(email_header, 'utf-8')), sender))

            message['To'] = receivers
            message['Cc'] = ccs

            message['Subject'] = email_subject
            content = MIMEText(email_body, 'html', 'utf-8')
            message.attach(content)

            send_email = True
            for attachment_name in attachment_name_list:
                attachment_file_path = self.report_save_path + os.sep + attachment_name
                is_attachment_exist, attachment_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, attachment_file_path,
                                                                           self.port)
                if is_attachment_exist:
                    email_attachment = MIMEApplication(attachment_obj.getvalue())
                    email_attachment.add_header('Content-Disposition', 'attachment', filename=attachment_name)
                    message.attach(email_attachment)
                else:
                    print(f'Attachment file {attachment_name} is not found in {self.report_save_path}.')
                    send_email = False

            if send_email and not email_bcc:
                smtp_obj.sendmail(from_addr=sender, to_addrs=email_to + email_cc, msg=message.as_string())
                print(f'-----email is sent successfully!-----')
            elif send_email and email_bcc:
                smtp_obj.sendmail(from_addr=sender, to_addrs=email_to + email_cc + email_bcc, msg=message.as_string())
                print(f'-----email is sent successfully!-----')
            else:
                print('Email is not sent due to attachment file is not found!')
            smtp_obj.quit()
        except:
            print('Mail sent failed.')
            print(traceback.format_exc())
            raise
            # create_error_log(error_log_folder_path, traceback.format_exc())

    def upload_file_by_api(self, file_path: str, api: str, api_add_token: bool, api_token: str, api_bearer: str):
        """This function is used to upload file by api

        Args:
            file_path(str): This is the file path that need to be uploaded
            api(str): This is the api that is used to upload file
            api_add_token(bool): This is the indicator  whether to use token
            api_token(str): This is the token value
            api_bearer(str): This is the bearer value
        """
        is_file_exist, file_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port)
        if is_file_exist:
            files = {'file': file_obj}
            headers = {}
            if api_add_token:
                headers = {
                    'Bearer': api_bearer,
                    'Token': api_token
                }
            res = requests.post(api, files=files, headers=headers, verify=False)
            if int(res.status_code) == 200:
                res_json = res.json()
                if res_json['isSuccess']:
                    print(f'-----{file_path} is uploaded successfully!-----')
                else:
                    print(f'{file_path} is failed to upload!')
            else:
                print(f'There is un error to upload {file_path}!')

    def merge_excel_files_to_sheets(self, from_folder_path: str, from_file_name: str, update_folder_path: str, update_file_name: str, update_sheet_name: str,
                                    process_number: int):
        """This function is used to merge files from from_folder or sub_folder of from folder to update folder

        Args:
            from_folder_path(str): This is the from_folder_path
            from_file_name(str): This is the file name that contains common file name fragment
            update_folder_path(str): This is the target folder path
            update_file_name(str): This is the file name of update file
            update_sheet_name(str): This is the sheet name of update file
            process_number(int): This is the process number
        """
        print(f'--------------- merge_excel_files_to_sheets ---------------')
        update_sheet_name_list = [str(sheet_name).strip() for sheet_name in update_sheet_name.replace('，', ',').split(',')]
        from_file_name_list = from_file_name.replace('，', ',').split(',')
        from_file_name_list = [self.prepare_file_name(str(file_name).strip()) for file_name in from_file_name_list]
        from_file_update_sheet_dict = dict(zip(from_file_name_list, update_sheet_name_list))
        update_file_name = self.prepare_file_name(str(update_file_name).strip())
        update_file_path = update_folder_path + os.sep + update_file_name

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for new_from_file_name, new_update_sheet_name in from_file_update_sheet_dict.items():
                from_file_path = from_folder_path + os.sep + new_from_file_name
                is_from_file_exist, from_file_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
                if is_from_file_exist:
                    from_file_data = pd.read_excel(from_file_obj)
                    new_update_sheet_name = new_update_sheet_name[:31]
                    from_file_data.to_excel(writer, sheet_name=new_update_sheet_name, index=False)

        output.seek(0)
        smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, output, self.port)

    def clear_existed_files(self, report_save_path, exception_str='Common'):
        """ This function is used to clear existed files and screenshots.

        Args:
            report_save_path(str): This is the folder path of save folder
            exception_str(str): This is the string to exclude when file name or folder name contains current string
        """
        smb_traverse_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, report_save_path, exception_str=exception_str)

    def clear_existed_files_by_keywords(self, report_save_path, deletion_keyword=''):
        """ This function is used to clear existed files and screenshots.

        Args:
            report_save_path(str): This is the folder path of save folder
            deletion_keyword(str): This is the keyword to delete files
        """
        smb_traverse_delete_file_by_keyword(self.user_name, self.user_password, self.server_name, self.share_name, report_save_path, deletion_keyword=deletion_keyword)

    def create_new_public_folder(self, public_folder_path):
        """ This function is used to create new public folder.

        Args:
            public_folder_path(str): This is the folder path of save folder
        """
        smb_create_folder(self.user_name, self.user_password, self.server_name, self.share_name, public_folder_path)

    def copy_file_cross_public_folders(self, from_server_name, from_share_name, from_folder_path, from_file_name, update_server_name, update_share_name, update_folder_path,
                                       update_file_name):
        """ This function is used to copy file between public folder.

        Args:
            from_server_name(str): This is the server name of source folder
            from_share_name(str): This is the share name of source folder
            from_folder_path(str): This is the folder path of source folder
            from_file_name(str): This is the file name of source folder
            update_server_name(str): This is the server name of target folder
            update_share_name(str): This is the share name of target folder
            update_folder_path(str): This is the folder path of target folder
            update_file_name(str): This is the file name of target folder
        """
        from_file_path = from_folder_path + os.sep + from_file_name
        to_file_path = update_folder_path + os.sep + update_file_name
        is_from_file_exist, from_file_obj = smb_check_file_exist(self.user_name, self.user_password, from_server_name, from_share_name, from_file_path, self.port)
        if is_from_file_exist:
            smb_store_remote_file_by_obj(self.user_name, self.user_password, update_server_name, update_share_name, to_file_path, from_file_obj, self.port)
            print(f'-----{from_file_path} is copied to {to_file_path} successfully!-----')
        else:
            print(f'File {from_file_path} does not exist!')

    def hrs_copy_cell_values_to_template(self, from_folder_path: str, from_file_name: str, from_sheet_name: str, split_column_name: str, has_from_file_condition: bool,
                                         template_file_name: str, template_sheet_name: str, copy_value_columns: str, copy_value_locations: str,
                                         need_pdf_version: bool = False) -> None:
        """This function is used to copy dataframe value to range/ranges of Excel file

        Args:
            from_folder_path: This is the folder path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            split_column_name: This is the column name which will be used to split data into multiple files
            template_file_name(str): This is the template file name, e.g. 'HRS-Template.xlsx'
            template_sheet_name(str): This is the template sheet name, e.g. 'Template'
            has_from_file_condition: This indicates whether current process has additional condition settings
            copy_value_columns(str): This is the column name or names to be copied, e.g. 'Name,ID,Age'
            copy_value_locations(str): This is the range or ranges to be copied, e.g. 'A1,B2,C3'
            need_pdf_version(bool): This indicates whether the PDF version is needed, default is False

        """
        from_file_path = from_folder_path + os.sep + from_file_name
        template_file_path = from_folder_path + os.sep + template_file_name
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, target_data, target_data_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            copy_value_columns_list = copy_value_columns.replace('，', ',').split(',')
            copy_value_locations_list = copy_value_locations.replace('，', ',').split(',')
            copy_value_locations_columns_dict = dict(zip(copy_value_locations_list, copy_value_columns_list))

            new_target_data = target_data.loc[:, [split_column_name, *copy_value_columns_list]]
            for column_name, column_type in target_data_dict.items():
                if column_name in new_target_data.columns and column_type == str:
                    new_target_data[column_name] = "'" + new_target_data[column_name]

            target_data = target_data.drop_duplicates(subset=[split_column_name], keep='first')
            split_column_values = list(target_data[split_column_name].to_list())

            for split_column_value in split_column_values:
                split_data = new_target_data[new_target_data[split_column_name] == split_column_value]
                if not split_data.empty:
                    split_row_data = split_data.loc[split_data.index[0]]
                    saved_data_range_dict = {}
                    for location, column_name in copy_value_locations_columns_dict.items():
                        saved_data_range_dict[location] = split_row_data[column_name]

                    raw_template_file_name, template_file_ext = os.path.splitext(template_file_name)
                    new_template_file_name = f'{raw_template_file_name}_{split_column_value}{template_file_ext}'
                    new_template_file_path = from_folder_path + os.sep + new_template_file_name
                    is_template_file_exist, template_file_obj = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, template_file_path,
                                                                                     self.port)
                    if is_template_file_exist:
                        smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, new_template_file_path, template_file_obj, self.port)
                        save_cell_values_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, new_template_file_path, template_sheet_name,
                                                    saved_data_range_dict, self.port, False, False)
                        if need_pdf_version:
                            export_excel_sheet_as_pdf(self.user_name, self.user_password, self.server_name, self.share_name, new_template_file_path, template_sheet_name, self.port)

            del target_data

    def export_excel_sheet_as_pdf(self, from_folder_path: str, from_file_name: str, from_sheet_name: str, export_match_type: str) -> None:
        """This function is used to export Excel sheet as PDF file

        Args:
            from_folder_path: This is the folder path of target Excel file
            from_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            export_match_type(str): This is the type of export, e.g. 'exact_match' or 'blur_match'
        """
        from_file_name_upper = from_file_name.upper()

        if export_match_type == 'blur_match':
            traverse_result_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, from_folder_path, self.port)
            for result_item in traverse_result_list:
                if result_item['is_file']:
                    file_name = result_item['name']
                    if from_file_name_upper in file_name.upper() and '.XLS' in file_name.upper():
                        from_file_path = from_folder_path + os.sep + file_name
                        export_excel_sheet_as_pdf(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, from_sheet_name, self.port)
        else:
            from_file_path = from_folder_path + os.sep + self.prepare_file_name(from_file_name)
            is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
            if is_from_file_exist:
                export_excel_sheet_as_pdf(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, from_sheet_name, self.port)

    def hrs_copy_first_row_to_ranges(self, from_folder_path: str, from_file_name: str, from_sheet_name: str,
                                     has_from_file_condition: bool, update_folder_path: str, update_file_name: str, update_sheet_name: str, update_column_name: str,
                                     update_row_number: int) -> None:
        """This function is used to copy dataframe value to range/ranges of Excel file

        Args:
            from_folder_path: This is the folder path of target Excel file
            from_file_name: This is the file name of Excel file
            update_file_name: This is the file name of Excel file
            from_sheet_name: This is the sheet name of Excel file
            has_from_file_condition: This indicates whether current process has additional condition settings
            update_folder_path: This is the folder path where update file is located
            update_file_name: This is the file name of update file
            update_sheet_name: This is the sheet name of update file
            update_column_name(str): The name of the column to search for empty cells.
            update_row_number(int): The row number to start searching from (default is 1).

        """
        from_file_path = from_folder_path + os.sep + from_file_name
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        if is_from_file_exist:
            _, target_data, target_data_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, has_from_file_condition, 'from_file')

            if not target_data.empty:

                for column_name, column_type in target_data_dict.items():
                    if column_name in target_data.columns and column_type == str:
                        target_data[column_name] = "'" + target_data[column_name]

                first_row_data = target_data.loc[[target_data.index[0]]]

                update_file_path = update_folder_path + os.sep + update_file_name
                update_range = locate_first_empty_cell_in_target_column(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port,
                                                                        update_sheet_name, update_column_name, update_row_number)
                print('update_range: ', update_range)
                save_dataframe_into_excel(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, update_sheet_name, first_row_data,
                                          update_range, False, self.port)
            del target_data

    def hrs_merge_weekly_rehiring_data(self, rehiring_folder_path, rehiring_sheet_name, text_column_names):
        """ This function is used to merge weekly rehiring data from multiple files and save it to a specified folder.

        Args:
            rehiring_folder_path(str): This is the folder path where weekly rehiring files are located.
            rehiring_sheet_name(str): This is the sheet name of the rehiring files to be merged.
            text_column_names(str): This is the list of column names that should be treated as text.
        """
        hrs_merge_weekly_rehiring_data(self.user_name, self.user_password, self.server_name, self.share_name, rehiring_folder_path, rehiring_sheet_name, self.report_save_path,
                                       self.port, text_column_names)

    def hrs_collect_row_value_diffs(self, from_folder_path: str, from_file_name: str, from_sheet_name: str, from_column_by: str, update_folder_path: str, update_file_name: str,
                                    update_sheet_name: str, update_column_by: str, config_folder_path: str, config_file_name: str, config_sheet_name: str,
                                    compare_result_file_name: str) -> None:
        """This function is used to compare column data in Excel file and save the result to a new column

        Args:
            from_folder_path(str): This is the folder path of target Excel file
            from_file_name(str): This is the file name of Excel file
            from_sheet_name(str): This is the sheet name of Excel file
            from_column_by(str): This is the key column name for comparison
            update_folder_path(str): This is the folder path where update file is located
            update_file_name(str): This is the file name of update file
            update_sheet_name(str): This is the sheet name of update file
            update_column_by(str): This is the key column name in the update file
            config_folder_path(str): This is the folder path where config file is located
            config_file_name(str): This is the file name of config file
            config_sheet_name(str): This is the sheet name of config file
            compare_result_file_name(str): This is the file name of compare result file

        """
        from_file_path = from_folder_path + os.sep + from_file_name
        update_file_path = update_folder_path + os.sep + update_file_name
        is_from_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, from_file_path, self.port)
        is_update_file_exist, _ = smb_check_file_exist(self.user_name, self.user_password, self.server_name, self.share_name, update_file_path, self.port)
        if is_from_file_exist and is_update_file_exist:
            _, from_file_data, from_file_dict = self.get_from_or_update_data(from_file_path, from_file_name, from_sheet_name, False, 'from_file')
            _, update_file_data, update_file_dict = self.get_from_or_update_data(update_file_path, update_file_name, update_sheet_name, False, 'update_file')
            compare_result_df = hrs_compare_excel_data(self.user_name, self.user_password, self.server_name, self.share_name, from_file_data, from_column_by, update_file_data,
                                                       update_column_by, config_folder_path, config_file_name, config_sheet_name, self.port)
            if not compare_result_df.empty:
                compare_file_path = self.report_save_path + os.sep + compare_result_file_name
                file_obj = BytesIO()

                with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
                    compare_result_df.to_excel(writer, index=False, float_format='%.2f', sheet_name='Sheet1')
                file_obj.seek(0)
                smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, compare_file_path, file_obj, self.port)
        else:
            raise ValueError(f'File {from_file_name} or {update_file_name} does not exist in the specified folder.')
