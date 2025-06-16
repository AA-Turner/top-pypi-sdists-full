from aheadworks_bitbucket_manager.model.ssh_manager import SshManager
from aheadworks_bitbucket_manager.model.parser.php import Php as PhpParser
from aheadworks_core.model.parser.json import Json as JsonParser
from dotenv import dotenv_values, set_key
import re
import ast
import os
import shutil

class VersionControlManager:

    def __init__(self):
        self.run_app_paths = {}
        self.ssh_manager = SshManager()
        self.php_parser = PhpParser()
        self.json_parser = JsonParser()

    def run_common_app(self, check_containers_arr, up_cmd, connection):
        command = 'docker ps -q'
        for container_name in check_containers_arr:
            command += ' -f name=' + container_name

        container_ids_arr = self.ssh_manager.run_ssh_command(command, connection)
        if container_ids_arr is None:
            container_ids_arr = []

        if len(container_ids_arr) != len(check_containers_arr):
            run_result = self.ssh_manager.run_ssh_command(up_cmd, connection)
            run_result = type(run_result) == list and '\n'.join(run_result)
        else:
            run_result = 'All Common App containers exists'

        return 'run_result:\n' + str(run_result)

    def run_app(
            self,
            path_to_versions,
            path_to_project,
            up_cmd,
            down_exclude_current,
            down_cmd,
            connection
    ):
        """
        :param path_to_versions: path to versions.
        :param path_to_project: path to project folder.
        :param up_cmd: command for run active apps.
        :param down_exclude_current: yes/no, down all app in project.
        :param down_cmd: command for down old apps.
        :param connection: dict with 'host', 'user' and 'port'.
        """
        print('path to versions: ' + path_to_versions)
        print('path to project with releases on server: ' + path_to_project)
        print('run app command: ' + up_cmd)
        print('down all released app in project folder exclude current: ' + down_exclude_current)
        print('kill app command: ' + down_cmd)

        version_config_item_name = ['VERSION', 'SAVE_VERSION']

        save_versions = []
        for var_name in version_config_item_name:
            var_value = self.php_parser.get_variable_from_file(var_name, path_to_versions).strip()
            if var_value:
                save_versions.append(var_value)

        print(f"save versions: {save_versions}")
        dir_items = self.ssh_manager.run_ssh_command('ls ' + path_to_project, connection)
        print(f"unsorted dir items: {dir_items}")
        # sort dirs by path by desc
        dir_items = self._sort_versions(dir_items)
        print(f"dir items: {dir_items}")

        kill_app_paths = []
        for item in dir_items:
            item = item.strip()
            item_arr = item.split('-')
            item_arr = len(item_arr) == 1 and item_arr.append('') or item_arr
            item_version, item_build = item_arr[:2]
            print("item version: {item_version}")
            if item_version in save_versions and item_version not in self.run_app_paths:
                self.run_app_paths[item_version] = item
            else:
                kill_app_paths.append(item)

        run_commands = []
        for key in self.run_app_paths:
            path_to_project_item = path_to_project + '/' + self.run_app_paths[key]
            run_commands.append(
                'cd ' + path_to_project_item
                + ' && ' + up_cmd
            )

        # down all app in project
        kill_result = ''
        down_command = ''
        if down_exclude_current == 'yes':
            kill_commands = []
            for item in kill_app_paths:
                path_to_project_item = path_to_project + '/' + item
                kill_commands.append(
                    'cd ' + path_to_project_item + '; '
                    + down_cmd + '; '
                    + 'rm -rf ' + path_to_project_item
                )

            if kill_commands:
                down_command = ' && '.join(kill_commands)
                kill_result = self.ssh_manager.run_ssh_command(down_command, connection)
                kill_result = type(kill_result) == list and '\n'.join(kill_result)

        # up all app in project
        run_result = ''
        run_command = ''
        if run_commands:
            run_command = ' && '.join(run_commands)
            run_result = self.ssh_manager.run_ssh_command(run_command, connection)
            run_result = type(run_result) == list and '\n'.join(run_result)

        return '\nrun commands:\n' + str(run_command) \
               + '\n\nkill commands:\n' + str(down_command) \
               + '\n\nrun_result:\n' + str(run_result) \
               + '\n\nkill_result:\n' + str(kill_result)

    def run_app_from_json_config(
            self,
            path_to_versions,
            path_to_project,
            path_to_json_config,
            down_exclude_current,
            connection
    ):
        config_run_commands = self.json_parser.get_variable_from_file('run_commands', path_to_json_config)
        stop_commands = self.json_parser.get_variable_from_file('stop_commands', path_to_json_config)

        run_commands = list()
        check_result = dict({'file': {'commands': list(), 'result': True}})
        for row in config_run_commands:
            command = row['command']
            if 'result' in row:
                result_to = row['result']['to']
                if result_to == 'file':
                    file_name = row['result'][result_to]['name']
                    command = '{} &> {}'.format(command, file_name)
                    check_result['file']['commands'].append(row)
            run_commands.append(command)

        run_commands = ';'.join(run_commands)
        stop_commands = ';'.join(stop_commands)
        run_app_result = self.run_app(
            path_to_versions,
            path_to_project,
            run_commands,
            down_exclude_current,
            stop_commands,
            connection
        )

        check_result_commands = check_result['file']['commands']
        for i, config in enumerate(check_result_commands):
            file = config['result']['file']['name']
            path_to_file = path_to_project + '/' + list(self.run_app_paths.values())[0] + '/' + file
            text_from_file = self.ssh_manager.run_ssh_command('cat ' + path_to_file, connection)
            index = len(text_from_file) - 1
            while index > 0:
                line_from_file = text_from_file[index].strip()
                if line_from_file:
                    if 'type' in config and config['type'] == 'mftf':
                        if 'OK' in line_from_file:
                            check_result_commands[i]['summary'] = dict({'status': True})
                        else:
                            print(text_from_file)
                            check_result_commands[i]['summary'] = dict({'status': False})
                            check_result['file']['result'] = False
                    break
                index = index - 1

        for result_type in check_result:
            if check_result[result_type]['result'] == False:
                raise Exception('Some commands returned an error!' + '\n\n' + run_app_result)

        return run_app_result

    # Deprecated
    def get_version_uid(self, version):
        version_uid = re.sub('[.]', '', version)

        return version_uid

    def get_traefik_version_query(self, path_to_versions):
        magento_version_control = self.php_parser.get_variable_from_file('MAGENTO_VERSION_CONTROL', path_to_versions)
        magento_version_control = magento_version_control \
            .replace('[', '{') \
            .replace(']', '}') \
            .replace('=>', ':') \
            .replace('\n', '')
        magento_version_control = ast.literal_eval(magento_version_control)

        app_curr_full_version = self.php_parser.get_variable_from_file('VERSION', path_to_versions)
        app_curr_major_version = app_curr_full_version.split('.')[0:-1]
        app_curr_major_version.append('*')
        app_curr_major_version = '.'.join(app_curr_major_version)
        app_version_map = [app_curr_full_version, app_curr_major_version]

        query = ''
        for module_version, app_version in magento_version_control.items():
            app_version = list(app_version)[0]
            if app_version in app_version_map:
                query = '&& Query(`version={version:' + module_version + '}`)' \
                        + ' || Query(`ver={ver:' + app_version + '}`)' \
                        + ' || HeadersRegexp(`referer`, `(.*)version=' + module_version + '`)' \
                        + ' || HeadersRegexp(`referer`, `(.*)ver=' + app_version + '`)'

        return query

    # --priority_type low or --priority_type height
    def get_free_priority(self, label_name, priority_type, connection):
        busy_priority = self.ssh_manager.run_ssh_command(
            'docker ps --format \'{{.Label "' + label_name + '"}}\'',
            connection
        )
        filtered_busy_priority = []
        for item in busy_priority:
            item = item.strip()
            if item:
                try:
                    filtered_busy_priority.append(int(item))
                except:
                    pass

        new_priority = 10
        if priority_type == 'low':
            while True:
                if new_priority not in filtered_busy_priority:
                    break
                new_priority += 1
        elif priority_type == 'height':
            if filtered_busy_priority:
                max_priority = max(filtered_busy_priority)
                new_priority = max_priority + 10

        return new_priority

    def get_free_port(self, connection):
        busy_ports = self.ssh_manager.run_ssh_command(
            'docker ps --format \'{{.Label "aw.apps.app_port_prefix"}}\'',
            connection
        )
        filtered_busy_ports = []
        for item in busy_ports:
            item = item.strip()
            if item:
                try:
                    filtered_busy_ports.append(int(item))
                except:
                    pass

        new_port = 10
        while True:
            if new_port not in filtered_busy_ports:
                break
            new_port += 1

        return new_port

    def modify_env(self, path, template):
        os.system('touch ' + path)
        with open(template, 'r') as f:
            original_lines = f.readlines()
        modify_lines = list()
        for line in original_lines:
            if line.find('=') != -1:
                split_line = line.split('=')
                param = split_line[0]
                value = split_line[1]
                pattern = "%(.*?)%"
                match_values = re.findall(pattern, value)
                match_params = re.findall(pattern, param)
                match_values = match_values + match_params
                if len(match_values):
                    for match_value in match_values:
                        match_value_arr = match_value.split(':-')
                        match_value_arr = len(match_value_arr) == 1 and match_value_arr.append('') or match_value_arr
                        match_value, match_value_default = match_value_arr[:2]
                        if match_value in os.environ and os.environ[match_value]:
                            line = re.sub(pattern, os.environ[match_value], line)
                        elif match_value_default:
                            if match_value_default[0] == '$':
                                match_value_default_env = match_value_default[1:]
                                if match_value_default_env in os.environ and os.environ[match_value_default_env]:
                                    line = re.sub(pattern, os.environ[match_value_default_env], line)
                                else:
                                    line = ''
                            else:
                                line = re.sub(pattern, match_value_default, line)
                        else:
                            line = ''
            modify_lines.append(line)
        nf = open(path, 'w')
        nf.writelines(item for item in modify_lines)
        nf.close()
        return

    def generate_env(self, source_file_path, target_file_path, verbose):
        """
        :param source_file_path: path to the sample .env file
        :param target_file_path: path to the .env file to create
        :param verbose: print all modified values
        """
        # let's copy the source config file first to keep the comments
        try:
            shutil.copy2(source_file_path, target_file_path)
        except FileNotFoundError:
            print("The file \"%s\" does not exist" % (source_file_path))
            raise
        else:
            saved_values = dotenv_values(source_file_path)
            overriden_values = {
                **dotenv_values(source_file_path),
                **os.environ,  # override loaded values with environment variables
            }
            # Now save parsed/overriden values into the target config
            for k,v in saved_values.items():
                new_value = overriden_values[k]
                if isinstance(new_value, str) and new_value.find(' ')!=-1:
                    quote_mode = 'always'
                else:
                    quote_mode = 'never'
                set_key(target_file_path, k, new_value, quote_mode)
                if verbose and v != new_value:
                    print("%s has been changed from \"%s\" to \"%s\"" % (k, v, new_value))

    def _sort_versions(self, items):
        versions = []
        build_versions = []
        for item in items:
            if item.find('-') == -1:
                versions.append(item)
            else:
                build_versions.append(item)
        try:
            versions = self._sort_version_string(versions)
        except Exception:
            versions = []

        try:
            build_versions = self._sort_version_string(build_versions)
        except Exception:
            build_versions = []

        return versions + build_versions

    def _sort_version_string(self, items):
        max_len = max([len(i.split('.')) for i in items])
        return sorted(items, key=lambda s: self._version_to_list(s, max_len), reverse=True)

    def _version_to_list(self, version_string, max_len):
        version = version_string.split('.')
        last = version[-1]
        # check if we have a build number
        if last.find('-') > -1:
            (last, build_num) = last.split('-')
        else:
            build_num = None
        version[-1] = last
        # pad versions so they are the same length
        while len(version)<max_len:
            version.append(0)
        # append a build number if any
        if build_num:
            version.append(build_num)
        # and now convert all items to int
        return [int(i) for i in version]
