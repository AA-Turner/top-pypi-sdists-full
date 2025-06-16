import os.path
from concurrent.futures import ThreadPoolExecutor

from .mini_rpa_functions import *
from .mini_rpa_hrs_customized_functions import hrs_send_anniversary_email
from .mini_rpa_database_functions import MiniRpaDatabaseAutomation


class MiniRpaManager(MiniRpaFunction):
    def __init__(self, user_name: str, user_password: str, server_name: str, share_name: str, port: int, from_period: str, to_period: str, report_save_path: str,
                 report_process_folder_path: str, report_period_type: str, process_number: int, process_dict: dict, delivery_dict: dict,
                 sap_operation_list: list, database_operation_list: list, update_file_condition_setting: list, from_file_condition_setting: list, data_type_dict: dict,
                 download_data=False, process_data: bool = False, delivery_data: bool = False, process_database: bool = False, file_name_suffix_format='YearMonthDay',
                 browser_screenshot_tag='', common_field_dict=None):
        """This function is used to initial parameters

        Args:
            user_name(str): This is the username
            user_password(str): This is the password
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            port(int): This is the port number of the server name
            from_period(str):This is the start month
            to_period(str): This is the end month
            report_process_folder_path(str): This is the file path for process excel
            report_save_path(str): This is the folder path for original data
            delivery_data(bool): This is the indicator whether to delivery files to folders, receivers or api
            download_data(bool): This is the indicator whether to do sap operation
            process_data(bool): This is the indicator whether to process data
            data_type_dict(dict): This is the dict that save the data type
            sap_operation_list: This is the list of sap operation
            database_operation_list(list): This is the list of database operation
            process_number(int): This is the number of process
            report_period_type(str): This is the report period type. e.g. period, current_date
            process_dict(dict): This is the dict that save the process logic data
            delivery_dict(dict): This is the dict that save the delivery logic data
            process_database(bool): This is the indicator whether to process data in database
            update_file_condition_setting(list): This is the list of update file condition setting
            from_file_condition_setting(list): This is the list of from file condition setting
            file_name_suffix_format(str): This is the file name suffix format
            browser_screenshot_tag(str): This is the tag for browser screenshot `
        """
        super().__init__(user_name, user_password, server_name, share_name, port, from_period, to_period, report_save_path, report_process_folder_path, report_period_type,
                         process_number, process_dict, delivery_dict, sap_operation_list, database_operation_list, update_file_condition_setting, from_file_condition_setting,
                         data_type_dict, download_data, process_data, delivery_data, process_database, file_name_suffix_format, common_field_dict)
        self.browser_screenshot_tag = browser_screenshot_tag

    @staticmethod
    def check_key_word_contains(target_string, key_word_list=None):
        """This function is used to check if the key word is in the list

        Args:
            target_string(str): The target string to check
            key_word_list(list): The list of key word
        """
        if key_word_list is None:
            key_word_list = ["folder_path", "report_save_path"]
        for key_word in key_word_list:
            if key_word in target_string:
                return True
        return False

    def prepare_sap_download_file_name(self, sap_operation_dict):
        """ This function is used to prepare the download file name

        Args:
            sap_operation_dict(dict): This is the dict that save the sap operation data
        """
        for field_key in sap_operation_dict.keys():
            if self.check_key_word_contains(field_key, ['file_name']):
                field_value = sap_operation_dict.get(field_key, '')
                sap_operation_dict[field_key] = self.prepare_file_name(field_value)
            elif self.check_key_word_contains(field_key):
                field_value = sap_operation_dict.get(field_key, '')
                sap_operation_dict[field_key] = self.replace_variables_in_string(field_value)

        # file_name = sap_operation_dict.get('file_name', '')
        # sap_operation_dict['file_name'] = self.prepare_file_name(file_name)

    def start_bot(self):
        """This function is used to collect all function and start to run bot

        """
        if self.download_data:
            # geckodriver_file_path = os.path.dirname(__file__) + os.sep + 'geckodriver'
            # save_folder_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "Download_Folder"
            geckodriver_file_path = '/opt/geckodriver'
            save_folder_path = "/opt/Download_Folder"

            if not os.path.exists(save_folder_path):
                os.mkdir(save_folder_path)

            sap_config_dict = {
                'has_save_folder': True,
                'save_folder_path': save_folder_path,
                'geckodriver_binary_location': geckodriver_file_path,
                'auto_get_screenshot': True,
                'browser_screenshot_tag': self.browser_screenshot_tag,
                'user_name': self.user_name,
                'user_password': self.user_password,
                'server_name': self.server_name,
                'share_name': self.share_name,
                'port': self.port,
                'from_period': self.from_period,
                'to_period': self.to_period,
                'report_save_path': self.report_save_path,
                'report_process_folder_path': self.report_process_folder_path,
                'report_period_type': self.report_period_type,
                'has_proxy': False,
                'timeout': 7200,
            }

            sap_automation = MiniRpaSapAutomation(**sap_config_dict)

            for process_step_dict in self.sap_operation_list:
                function_name = process_step_dict['process_name']
                sap_operation_dict = process_step_dict.get('process_step_variant_dict', {})
                self.prepare_sap_download_file_name(sap_operation_dict)

                print(f'---------- current sap function is {function_name} ----------')

                layout_name = sap_operation_dict.get('layout_name', '')
                field_values = sap_operation_dict.get('field_values', '').replace('，', ',').split(',')
                second_field_values = sap_operation_dict.get('second_field_values', '').replace('，', ',').split(',')
                is_enter = sap_operation_dict.get('is_enter', False)
                is_enter = is_enter if is_enter else False
                is_tab = sap_operation_dict.get('is_tab', False)
                is_tab = is_tab if is_tab else False
                need_click_tip = sap_operation_dict.get('need_click_tip', False)
                need_click_tip = True if need_click_tip else False
                shortcut_list = sap_operation_dict.get('shortcut_list', [])
                if shortcut_list:
                    shortcut_list = [getattr(Keys, str(shortcut).upper()) for shortcut in shortcut_list]

                if sap_automation.skip_download_process:
                    if not function_name.startswith('download'):
                        continue
                    else:
                        sap_automation.skip_download_process = False
                        continue

                if function_name == 'login_sap':
                    sap_automation.login_sap(sap_operation_dict['sap_system'], sap_operation_dict['username'], sap_operation_dict['password'], False, '')
                elif function_name == 'input_sap_t_code':
                    sap_automation.input_sap_t_code(sap_operation_dict['t_code'])
                elif function_name == 'input_se16_table_name':
                    sap_automation.input_se16_table_name(sap_operation_dict['table_name'])
                elif function_name == 'input_field_multiple_values':
                    sap_automation.input_field_multiple_values(int(sap_operation_dict['field_button_index']), int(sap_operation_dict['tab_index']), field_values,
                                                               second_field_values)
                elif function_name == 'input_query_field_multiple_values':
                    sap_automation.input_query_field_multiple_values(int(sap_operation_dict['field_button_index']), int(sap_operation_dict['tab_index']), field_values,
                                                                     second_field_values)
                elif function_name == 'input_field_single_value':
                    sap_automation.input_field_single_value(sap_operation_dict['field_title'], int(sap_operation_dict['field_index']), sap_operation_dict['field_value'],
                                                            is_enter,
                                                            is_tab, need_click_tip)
                elif function_name == 'click_execute_button':
                    sap_automation.click_execute_button()
                elif function_name == 'click_output_button':
                    sap_automation.click_output_button()
                elif function_name == 'click_payroll_button':
                    sap_automation.click_payroll_button()
                elif function_name == 'check_data_load_status':
                    sap_automation.check_data_load_status(sap_operation_dict['failed_load_message'])
                elif function_name == 'check_button_popup_and_click':
                    sap_automation.check_button_popup_and_click(sap_operation_dict['button_title'], int(sap_operation_dict.get('try_times', 5)))
                elif function_name == 'download_excel_by_click_spreadsheet_button':
                    sap_automation.download_excel_by_click_spreadsheet_button(sap_operation_dict['spreadsheet_title'], sap_operation_dict['file_name'])
                elif function_name == 'download_excel_by_click_print_preview':
                    sap_automation.download_excel_by_click_print_preview(sap_operation_dict['print_preview_title'], sap_operation_dict['spreadsheet_title'],
                                                                         sap_operation_dict['file_name'])
                elif function_name == 'download_excel_by_press_short_keys':
                    sap_automation.download_excel_by_press_short_keys(shortcut_list, sap_operation_dict['file_name'])
                elif function_name == 'save_screenshot':
                    sap_automation.save_screenshot(sap_operation_dict['screenshot_folder_path'], sap_operation_dict['screenshot_file_name_tag'],
                                                   sap_operation_dict['name_format'])
                elif function_name == 'download_excel_by_context_click':
                    sap_automation.download_excel_by_context_click(sap_operation_dict['column_name'], sap_operation_dict['context_menu_item_name'],
                                                                   sap_operation_dict['file_name'])
                elif function_name == 'download_excel_by_menu_click':
                    sap_automation.download_excel_by_menu_click(sap_operation_dict['file_name'])
                elif function_name == 'download_excel_by_views_button_click':
                    sap_automation.download_excel_by_views_button_click(sap_operation_dict['file_name'])
                elif function_name == 'select_layout_before_download_excel':
                    sap_automation.select_layout_before_download_excel(layout_name, shortcut_list)
                elif function_name == 'select_se16_layout_before_download_excel':
                    sap_automation.select_se16_layout_before_download_excel(layout_name, shortcut_list)
                elif function_name == 'click_button':
                    sap_automation.click_button(sap_operation_dict['button_title'])
                elif function_name == 'click_radio_checkbox':
                    sap_automation.click_radio_checkbox(sap_operation_dict['radio_checkbox_title'])
                elif function_name == 'input_reporting_period':
                    sap_automation.input_reporting_period(sap_operation_dict['reporting_period_name'], sap_operation_dict['reporting_start_date'],
                                                          sap_operation_dict['reporting_end_date'])
                elif function_name == 'input_query_values_from_existed_data':
                    (query_button_index,
                     query_value_input_method,
                     remote_folder_path,
                     query_value_columns,
                     file_name,
                     sheet_name,
                     tab_index) = (sap_operation_dict['query_button_index'],
                                   sap_operation_dict['query_value_input_method'],
                                   sap_operation_dict['remote_folder_path'],
                                   sap_operation_dict['query_value_columns'],
                                   sap_operation_dict['file_name'],
                                   sap_operation_dict['sheet_name'],
                                   sap_operation_dict['tab_index'])
                    query_value_columns = query_value_columns.split(',') if query_value_columns else None
                    sap_automation.input_query_values_from_existed_data(int(query_button_index), query_value_input_method, remote_folder_path, query_value_columns, file_name,
                                                                        sheet_name, int(tab_index))
                elif function_name == 'find_variant_by_name':
                    sap_automation.find_variant_by_name(sap_operation_dict['variant_name'])
                elif function_name == 'find_organization_data_by_company_code':
                    sap_automation.find_organization_data_by_company_code(sap_operation_dict['company_code'])
                elif function_name == 'back_to_home_page':
                    sap_automation.back_to_home_page()
                elif function_name == 'input_sap_query_name':
                    sap_automation.input_sap_query_name(sap_operation_dict['query_name'])
                elif function_name == 'input_sap_info_set':
                    sap_automation.input_sap_info_set(sap_operation_dict['info_set_name'])
                elif function_name == 'wait_invisibility_of_loading_window':
                    sap_automation.wait_invisibility_of_loading_window()
                elif function_name == 'expand_report_fully':
                    sap_automation.expand_report_fully(shortcut_list)
                elif function_name == 'select_y01k_report_left_menu_item':
                    sap_automation.select_y01k_report_left_menu_item(sap_operation_dict['report_name'])
                elif function_name == 'download_y01k_report_data':
                    sap_automation.download_y01k_report_data(sap_operation_dict['file_name'], shortcut_list)
                elif function_name == 'drag_and_drop_y01k_split_element':
                    sap_automation.drag_and_drop_y01k_split_element(sap_operation_dict['split_element_order'], sap_operation_dict['y_offset'])

            if sap_automation:
                sap_automation.web_rpa.quit_browser()

        if self.process_data:

            process_number = self.process_number
            function_name = self.process_dict['process_name']
            # is_save = self.process_dict.get('is_save', True)

            is_save = True

            from_file_path = self.process_dict.get('from_file_path', '')
            from_file_name = self.prepare_file_name(self.process_dict.get('from_file_name', ''))
            from_sheet_name = self.process_dict.get('from_sheet_name', 'Sheet1')
            from_server_name = self.process_dict.get('from_server_name', '')
            from_server_name = from_server_name if from_server_name else self.server_name
            from_share_name = self.process_dict.get('from_share_name', '')
            from_share_name = from_share_name if from_share_name else self.share_name
            from_folder_path = self.replace_variables_in_string(self.process_dict.get('from_folder_path', ''))
            from_column_name = self.process_dict.get('from_column_name', '')
            from_column_by = self.process_dict.get('from_column_by', '')
            from_compare_column = self.process_dict.get('from_compare_column', '')
            from_group_by_column = self.process_dict.get('from_group_by_column', '')
            from_contain_column = self.process_dict.get('from_contain_column', '')
            has_from_file_condition = self.process_dict.get('has_from_file_condition')
            has_from_file_condition = has_from_file_condition if has_from_file_condition else False
            all_from_delete_file_name = self.process_dict.get('all_from_delete_file_name', '')

            update_file_path = self.process_dict.get('update_file_path', '')
            update_file_name = self.prepare_file_name(self.process_dict.get('update_file_name', ''))
            update_sheet_name = self.process_dict.get('update_sheet_name', 'Sheet1')
            update_server_name = self.process_dict.get('update_server_name', '')
            update_server_name = update_server_name if update_server_name else self.server_name
            update_share_name = self.process_dict.get('update_share_name', '')
            update_share_name = update_share_name if update_share_name else self.share_name
            update_folder_path = self.replace_variables_in_string(self.process_dict.get('update_folder_path', ''))
            update_column_name = self.process_dict.get('update_column_name', '')
            update_column_by = self.process_dict.get('update_column_by', '')
            has_update_file_condition = self.process_dict.get('has_update_file_condition', False)
            has_update_file_condition = has_update_file_condition if has_update_file_condition else False
            update_range = self.process_dict.get('update_range', '')

            original_value = self.process_dict.get('original_value', '')
            replace_value = self.process_dict.get('replace_value', '')
            new_column_name = self.process_dict.get('new_column_name', '')
            compare_result_value = self.process_dict.get('compare_result_value', '')
            calculate_value = self.process_dict.get('calculate_value', '')
            keep_config = self.process_dict.get('keep_config', '')
            group_by_config = self.process_dict.get('group_by_config', '')
            is_ascending = self.process_dict.get('is_ascending', False)
            is_ascending = is_ascending if is_ascending else False
            function_type = self.process_dict.get('function_type', '')
            delete_column_name = self.process_dict.get('delete_column_name', '')
            assign_value_type = self.process_dict.get('assign_value_type', '')
            copy_column_name = self.process_dict.get('copy_column_name', '')
            constant_value = self.process_dict.get('constant_value', '')
            row_number = self.process_dict.get('row_number', '')
            split_column_name = self.process_dict.get('split_column_name', '')
            template_file_name = self.prepare_file_name(self.process_dict.get('template_file_name', ''))
            template_sheet_name = self.process_dict.get('template_sheet_name', 'Sheet1')
            copy_value_columns = self.process_dict.get('copy_value_columns', '')
            copy_value_locations = self.process_dict.get('copy_value_locations', '')
            need_pdf_version = self.process_dict.get('need_pdf_version', False)
            export_match_type = self.process_dict.get('export_match_type', '')
            update_row_number = self.process_dict.get('update_row_number', '')

            rehiring_folder_path = self.replace_variables_in_string(self.process_dict.get('rehiring_folder_path', ''))
            rehiring_folder_path = rehiring_folder_path if rehiring_folder_path else self.report_save_path
            rehiring_sheet_name = self.process_dict.get('rehiring_sheet_name', 'Sheet1')

            config_folder_path = self.replace_variables_in_string(self.process_dict.get('config_folder_path', ''))
            config_folder_path = config_folder_path if config_folder_path else self.report_save_path
            config_file_name = self.prepare_file_name(self.process_dict.get('config_file_name', ''))
            config_sheet_name = self.process_dict.get('config_sheet_name', 'Sheet1')
            compare_result_file_name = self.prepare_file_name(self.process_dict.get('compare_result_file_name', ''))

            public_folder_path = self.replace_variables_in_string(self.process_dict.get('public_folder_path', ''))
            report_save_path = self.replace_variables_in_string(self.process_dict.get('report_save_path', ''))
            exception_str = self.process_dict.get('exception_str', '')
            deletion_keyword = self.process_dict.get('deletion_keyword', '')
            separator = self.process_dict.get('separator', '')
            separator = separator if separator else ''

            from_folder_path = from_folder_path if from_folder_path else self.report_save_path
            from_file_path = from_folder_path + os.sep + from_file_name
            update_folder_path = update_folder_path if update_folder_path else self.report_save_path
            update_file_path = update_folder_path + os.sep + update_file_name

            print(f'---------- current process name {function_name} ----------')

            if function_name == 'keep':
                self.keep(self.from_file_path, self.from_file_name, self.from_sheet_name, process_number, is_save, has_from_file_condition)
            elif function_name == 'vlookup':
                self.vlookup(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_column_by,
                             self.update_file_path, self.update_file_name, self.update_sheet_name, update_column_name, update_column_by, has_from_file_condition,
                             has_update_file_condition, is_save)
            elif function_name == 'rename_column_names':
                self.rename_column_names(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, update_column_name, is_save)
            elif function_name == 'copy_as_new_file':
                copy_as_new_file(from_folder_path, self.from_file_name, update_folder_path, update_file_name, self.from_period, self.user_name, self.user_password,
                                 self.server_name, self.share_name, self.port)
            elif function_name == 'copy_to_new':
                self.copy_to_new(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, self.update_file_name,
                                 self.update_sheet_name,
                                 update_column_name, has_from_file_condition, is_save)
            elif function_name == 'replace':
                self.replace(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, original_value, replace_value,
                             has_from_file_condition, is_save)
            elif function_name == 'replace_empty_value':
                self.replace_empty_value(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, replace_value,
                                         has_from_file_condition, is_save)
            elif function_name == 'combine_new_column':
                self.combine_new_column(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name,
                                        has_from_file_condition, is_save, separator)
            elif function_name == 'split_to_new_file':
                self.split_to_new_file(self.from_file_path, self.from_file_name, self.from_sheet_name, from_group_by_column, process_number,
                                       has_from_file_condition)
            elif function_name == 'column_calculate':
                self.column_calculate(self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, new_column_name, process_number,
                                      has_from_file_condition, is_save, function_type, calculate_value)
            elif function_name == 'copy_to_exist':
                self.copy_to_exist(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, self.update_file_path,
                                   self.update_sheet_name, update_column_name, has_from_file_condition)
            elif function_name == 'date_transfer':
                self.date_transfer(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
                                   is_save)
            elif function_name == 'remove_duplicates':
                self.remove_duplicates(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
                                       keep_config, is_save)
            elif function_name == 'sort_values':
                self.sort_values(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
                                 is_ascending, is_save)
            elif function_name == 'contain_condition_replace':
                self.contain_condition_replace(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_contain_column,
                                               original_value, replace_value, has_from_file_condition, is_save)
            elif function_name == 'group_by':
                self.group_by(process_number, self.from_file_path, self.from_file_name, self.update_file_name, self.from_sheet_name, self.update_sheet_name, from_column_name,
                              from_group_by_column, group_by_config, has_from_file_condition, is_save)
            elif function_name == 'column_compare':
                self.column_compare(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, from_compare_column,
                                    has_from_file_condition, new_column_name, compare_result_value, is_save)
            elif function_name == 'calculate_anniversary_duration':
                self.calculate_anniversary_duration(process_number, self.from_file_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
                                                    new_column_name, is_save)
            elif function_name == 'hrs_copy_excel_files':
                self.hrs_copy_excel_files(from_folder_path, from_file_name, update_folder_path)
            elif function_name == 'combine_excel_files':
                from_file_name = self.replace_variables_in_string(self.process_dict.get('from_file_name', ''))
                self.combine_excel_files(from_folder_path, from_file_name, self.from_sheet_name, update_folder_path, self.update_file_name,
                                         self.update_sheet_name, process_number)
            elif function_name == 'merge_excel_files_to_sheets':
                self.merge_excel_files_to_sheets(from_folder_path, from_file_name, update_folder_path, update_file_name, update_sheet_name, process_number)
            elif function_name == 'copy_value_to_range':
                from_folder_path = from_folder_path if from_folder_path else self.report_save_path
                update_folder_path = update_folder_path if update_folder_path else self.report_save_path
                self.copy_value_to_range(process_number, from_folder_path, self.from_file_name, self.from_sheet_name, from_column_name, has_from_file_condition,
                                         update_folder_path, self.update_file_name, self.update_sheet_name, update_range)
            elif function_name == 'delete_files':
                self.delete_files(all_from_delete_file_name)
            elif function_name == 'clear_existed_files':
                report_save_path = report_save_path if report_save_path else self.report_save_path
                exception_str = exception_str if exception_str else 'Common'
                self.clear_existed_files(report_save_path, exception_str)
            elif function_name == 'clear_existed_files_by_keywords':
                report_save_path = report_save_path if report_save_path else self.report_save_path
                deletion_keyword = deletion_keyword if deletion_keyword else ''
                self.clear_existed_files_by_keywords(report_save_path, deletion_keyword)
            elif function_name == 'create_new_public_folder':
                public_folder_path = public_folder_path if public_folder_path else self.report_save_path
                self.create_new_public_folder(public_folder_path)
            elif function_name == 'copy_file_cross_public_folders':
                from_folder_path = from_folder_path if from_folder_path else self.report_save_path
                update_folder_path = update_folder_path if update_folder_path else self.report_save_path
                self.copy_file_cross_public_folders(from_server_name, from_share_name, from_folder_path, from_file_name, update_server_name, update_share_name, update_folder_path,
                                                    update_file_name)
            elif function_name == 'delete_excel_file_columns':
                self.delete_excel_file_columns(process_number, from_file_path, self.from_file_name, self.from_sheet_name, delete_column_name, is_save)
            elif function_name == 'assign_value_to_target_column':
                self.assign_value_to_target_column(process_number, from_file_path, from_file_name, self.from_sheet_name, from_column_name, assign_value_type, copy_column_name,
                                                   constant_value, has_from_file_condition, is_save)
            elif function_name == 'create_new_columns':
                self.create_new_columns(process_number, from_file_path, self.from_file_name, self.from_sheet_name, new_column_name, is_save)
            elif function_name == 'delete_excel_file_rows':
                self.delete_excel_file_rows(process_number, from_file_path, self.from_sheet_name, row_number)
            elif function_name == 'hrs_copy_cell_values_to_template':
                self.hrs_copy_cell_values_to_template(from_folder_path, from_file_name, from_sheet_name, split_column_name, has_from_file_condition, template_file_name,
                                                      template_sheet_name, copy_value_columns, copy_value_locations, need_pdf_version)
            elif function_name == 'export_excel_sheet_as_pdf':
                if export_match_type == 'blur_match':
                    from_file_name = self.process_dict.get('from_file_name', '')
                self.export_excel_sheet_as_pdf(from_folder_path, from_file_name, from_sheet_name, export_match_type)
            elif function_name == 'hrs_copy_first_row_to_ranges':
                self.hrs_copy_first_row_to_ranges(from_folder_path, from_file_name, from_sheet_name, has_from_file_condition, update_folder_path, update_file_name,
                                                  update_sheet_name, update_column_name, int(update_row_number))
            elif function_name == 'hrs_merge_weekly_rehiring_data':
                self.hrs_merge_weekly_rehiring_data(rehiring_folder_path, rehiring_sheet_name)
            elif function_name == 'hrs_collect_row_value_diffs':
                self.hrs_collect_row_value_diffs(from_folder_path, from_file_name, from_sheet_name, from_column_by, update_folder_path,
                                                 update_file_name, update_sheet_name, update_column_by, config_folder_path, config_file_name, config_sheet_name,
                                                 compare_result_file_name)

        if self.delivery_data:
            self.prepare_file_name_suffix()
            delivery_type = self.delivery_dict['process_name']

            print(f'---------- current process name {delivery_type} ----------')

            if delivery_type == 'send_email':
                # error_log_folder_path is the path on the server rather than the remote folder path
                email_fields = ['email_account', 'email_password', 'email_address', 'email_body', 'email_header', 'email_subject', 'email_to', 'email_cc', 'email_bcc',
                                'error_log_folder_path', 'file_name']
                email_values = {field: self.delivery_dict.get(field, '') for field in email_fields}
                attachment_name_list = email_values['file_name'].replace('，', ',').split(',')
                attachment_name_list = [self.prepare_file_name(file_name) for file_name in attachment_name_list if file_name.strip()]

                email_account = email_values['email_account']
                email_password = email_values['email_password']
                email_address = email_values['email_address']
                email_body = email_values['email_body']
                email_header = email_values['email_header']
                email_subject = email_values['email_subject']
                email_to = email_values['email_to'].split(';')
                email_cc = email_values['email_cc'].split(';')
                email_bcc = email_values['email_bcc'].split(';')
                # attachment_name_list = [self.prepare_file_name(file_name) for file_name in attachment_name_list]
                self.send_email(email_account, email_password, email_address, email_body, email_header, email_subject, email_to, email_cc, attachment_name_list, email_bcc)

            if delivery_type == 'hrs_send_email_by_file_name':
                # error_log_folder_path is the path on the server rather than the remote folder path
                email_fields = ['email_account', 'email_password', 'email_address', 'email_body', 'email_header', 'email_subject', 'email_cc', 'email_bcc', 'file_name']
                email_values = {field: self.delivery_dict.get(field, '') for field in email_fields}

                email_account = email_values['email_account']
                email_password = email_values['email_password']
                email_address = email_values['email_address']
                email_body = email_values['email_body']
                email_header = email_values['email_header']
                email_subject = email_values['email_subject']
                email_cc = email_values['email_cc'].split(';')
                email_bcc = email_values['email_bcc'].split(';')
                file_name_key_word = self.replace_variables_in_string(email_values['file_name']).upper()
                file_name_list = smb_traverse_remote_folder(self.user_name, self.user_password, self.server_name, self.share_name, self.report_save_path, self.port)
                with ThreadPoolExecutor(max_workers=10) as executor:
                    for file_name_dict in file_name_list:
                        if file_name_dict['is_file']:
                            file_name = file_name_dict['name']
                            if file_name_key_word in file_name.upper():
                                raw_file_name = os.path.splitext(file_name)[0]
                                to_nt_account = raw_file_name.split('_')[-1]
                                email_to = [f"{to_nt_account}@bosch.com"]
                                attachment_name_list = [file_name]
                                executor.submit(self.send_email, email_account, email_password, email_address, email_body, email_header, email_subject, email_to, email_cc,
                                                attachment_name_list, email_bcc)

            elif delivery_type == 'send_anniversary_email':
                email_fields = ['card_type', 'email_account', 'email_password', 'email_address', 'email_header', 'email_subject', 'email_cc', 'anniversary_file_name',
                                'template_folder_path', 'email_to_manager_column', 'manager_name_column', 'anniversary_year_column', 'email_to_column', 'user_name_column']
                email_values = {field: self.delivery_dict.get(field, '') for field in email_fields}

                email_account = email_values['email_account']
                email_password = email_values['email_password']
                email_address = email_values['email_address']
                email_header = email_values['email_header']
                email_subject = email_values['email_subject']
                email_cc = email_values['email_cc'].replace('；', ';').split(';')
                anniversary_file_name = email_values['anniversary_file_name']
                anniversary_file_name = self.prepare_file_name(anniversary_file_name)
                anniversary_file_path = self.report_save_path + os.sep + anniversary_file_name
                template_folder_path = self.replace_variables_in_string(email_values['template_folder_path'])
                # email_to_manager_column = email_values['email_to_manager_column']
                # manager_name_column = email_values['manager_name_column']
                anniversary_year_column = email_values['anniversary_year_column']
                email_to_column = email_values['email_to_column']
                user_name_column = email_values['user_name_column']
                birthday_year = str(self.prepare_date_info(self.from_period).year)
                card_type = email_values['card_type']

                hrs_send_anniversary_email(card_type, anniversary_year_column, email_to_column, user_name_column, email_cc,
                                           email_subject, email_header, email_account, email_password, email_address, anniversary_file_path, template_folder_path,
                                           birthday_year, self.user_name, self.user_password, self.server_name, self.share_name, self.port)

            elif delivery_type == 'save_file_to_fixed_folder':
                original_folder_path = self.replace_variables_in_string(self.delivery_dict.get('original_folder_path', '').strip())
                original_file_name = self.prepare_file_name(self.delivery_dict.get('original_file_name', ''))

                delivery_folder_path = self.replace_variables_in_string(self.delivery_dict.get('delivery_folder_path', '').strip())
                delivery_file_name = self.prepare_file_name(self.delivery_dict.get('delivery_file_name', ''))

                if not original_folder_path:
                    original_folder_path = self.report_save_path
                if not delivery_folder_path:
                    delivery_folder_path = self.report_save_path

                # delivery_file_name = self.prepare_file_name(self.delivery_dict.get('file_name', ''))
                # delivery_file_path = self.delivery_dict.get('delivery_file_path', '')
                # original_file_path = self.report_save_path + os.sep + delivery_file_name

                original_file_path = original_folder_path + os.sep + original_file_name
                delivery_file_path = delivery_folder_path + os.sep + delivery_file_name

                smb_delete_file(self.user_name, self.user_password, self.server_name, self.share_name, delivery_file_path, self.port)
                file_obj = smb_load_file_obj(self.user_name, self.user_password, self.server_name, self.share_name, original_file_path, self.port)
                smb_store_remote_file_by_obj(self.user_name, self.user_password, self.server_name, self.share_name, delivery_file_path, file_obj, self.port)
                print(f'-----{original_file_path} is copied successfully!-----')
            elif delivery_type == 'upload_file_by_api':
                api_fields = ['api', 'api_add_token', 'api_token', 'api_bearer', 'file_name']
                api_values = {field: self.delivery_dict.get(field, False if field == 'api_add_token' else '') for field in api_fields}

                api = api_values['api']
                api_add_token = api_values['api_add_token']
                api_token = api_values['api_token']
                api_bearer = api_values['api_bearer']
                api_file_name = self.prepare_file_name(api_values['file_name'])
                api_file_path = self.report_save_path + os.sep + api_file_name
                self.upload_file_by_api(api_file_path, api, api_add_token, api_token, api_bearer)
            elif delivery_type == 'clear_existed_files':
                report_save_path = self.replace_variables_in_string(self.delivery_dict.get('report_save_path', ''))
                exception_str = self.delivery_dict.get('exception_str', '')
                report_save_path = report_save_path if report_save_path else self.report_save_path
                exception_str = exception_str if exception_str else 'Common'
                self.clear_existed_files(report_save_path, exception_str)

            elif delivery_type == 'clear_existed_files_by_keywords':
                report_save_path = self.replace_variables_in_string(self.delivery_dict.get('report_save_path', ''))
                deletion_keyword = self.delivery_dict.get('deletion_keyword', '')
                report_save_path = report_save_path if report_save_path else self.report_save_path
                deletion_keyword = deletion_keyword if deletion_keyword else ''
                self.clear_existed_files_by_keywords(report_save_path, deletion_keyword)

            elif delivery_type == 'copy_file_cross_public_folders':
                from_server_name = self.delivery_dict.get('from_server_name', '')
                from_share_name = self.delivery_dict.get('from_share_name', '')
                from_folder_path = self.replace_variables_in_string(self.delivery_dict.get('from_folder_path', ''))
                from_file_name = self.prepare_file_name(self.delivery_dict.get('from_file_name', ''))

                update_server_name = self.delivery_dict.get('update_server_name', '')
                update_share_name = self.delivery_dict.get('update_share_name', '')
                update_folder_path = self.replace_variables_in_string(self.delivery_dict.get('update_folder_path', ''))
                update_file_name = self.prepare_file_name(self.delivery_dict.get('update_file_name', ''))

                from_server_name = from_server_name if from_server_name else self.server_name
                from_share_name = from_share_name if from_share_name else self.share_name
                from_folder_path = from_folder_path if from_folder_path else self.report_save_path
                update_server_name = update_server_name if update_server_name else self.server_name
                update_share_name = update_share_name if update_share_name else self.share_name
                update_folder_path = update_folder_path if update_folder_path else self.report_save_path

                self.copy_file_cross_public_folders(from_server_name, from_share_name, from_folder_path, from_file_name, update_server_name, update_share_name, update_folder_path,
                                                    update_file_name)

        if self.process_database:
            database_config_dict = {
                'user_name': self.user_name,
                'user_password': self.user_password,
                'server_name': self.server_name,
                'share_name': self.share_name,
                'port': self.port,
            }

            database_automation = MiniRpaDatabaseAutomation(**database_config_dict)

            for process_step_dict in self.database_operation_list:
                function_name = process_step_dict['process_name']
                database_operation_dict = process_step_dict.get('process_step_variant_dict', {})
                self.prepare_sap_download_file_name(database_operation_dict)

                print(f'---------- current database function is {function_name} ----------')

                if function_name == 'connect_to_mysql_server':
                    (database_host,
                     database_port,
                     database_user,
                     database_password,
                     database_name) = (
                        database_operation_dict.get('database_host', None),
                        database_operation_dict.get('database_port', None),
                        database_operation_dict.get('database_user', None),
                        database_operation_dict.get('database_password', None),
                        database_operation_dict.get('database_name', None))

                    database_port = int(database_port) if database_port else None
                    database_automation.connect_to_mysql_server(database_host, database_port, database_user, database_password, database_name)

                elif function_name == 'fetch_mysql_data_and_save_data':
                    sql_query = database_operation_dict.get('sql_query', '')
                    remote_folder_path = self.replace_variables_in_string(database_operation_dict.get('remote_folder_path', '').strip())
                    remote_folder_path = remote_folder_path if remote_folder_path else self.report_save_path
                    file_name = database_operation_dict.get('file_name', '')
                    file_path = remote_folder_path + os.sep + file_name
                    sheet_name = database_operation_dict.get('sheet_name', '')
                    sheet_name = sheet_name if sheet_name else 'Sheet1'

                    database_automation.fetch_mysql_data_and_save_data(sql_query, self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port,
                                                                       sheet_name)
                elif function_name == 'disconnect_from_mysql_server':
                    database_automation.disconnect_from_mysql_server()

                elif function_name == 'load_mysql_data_by_tech_account':

                    (database_host,
                     database_port,
                     database_user,
                     database_password,
                     database_name) = (
                        database_operation_dict.get('database_host', None),
                        database_operation_dict.get('database_port', None),
                        database_operation_dict.get('database_user', None),
                        database_operation_dict.get('database_password', None),
                        database_operation_dict.get('database_name', None))

                    database_port = int(database_port) if database_port else None
                    database_automation.connect_to_mysql_server(database_host, database_port, database_user, database_password, database_name)

                    sql_query = database_operation_dict.get('sql_query', '')
                    print('sql_query: ', sql_query)
                    sql_query_params = self.replace_date_in_string_list(database_operation_dict.get('sql_query_params', None))
                    remote_folder_path = self.replace_variables_in_string(database_operation_dict.get('remote_folder_path', '').strip())
                    remote_folder_path = remote_folder_path if remote_folder_path else self.report_save_path
                    file_name = database_operation_dict.get('file_name', '')
                    file_path = remote_folder_path + os.sep + file_name
                    sheet_name = database_operation_dict.get('sheet_name', '')
                    sheet_name = sheet_name if sheet_name else 'Sheet1'

                    if sql_query_params:
                        sql_query_params = tuple(sql_query_params)
                    database_automation.fetch_mysql_data_and_save_data(sql_query, self.user_name, self.user_password, self.server_name, self.share_name, file_path, self.port,
                                                                       sheet_name, sql_query_params)
                    database_automation.disconnect_from_mysql_server()

            if database_automation.mysql_connection:
                database_automation.disconnect_from_mysql_server()
