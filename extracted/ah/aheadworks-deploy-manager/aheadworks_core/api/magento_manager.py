from aheadworks_core.model.parser.json import Json as JsonParser
from aheadworks_core.model.cd import Cd as cd
from aheadworks_core.api.file_manager import FileManager
from aheadworks_core.model.parser.xml import Xml as XmlParser
import subprocess
import os
import stringcase


class MagentoManager:
    """manager for magento"""

    MODULE_XML_FILE = '/etc/module.xml'
    MODULE_COMPOSER_FILE = '/composer.json'
    PLATFORM_MODULE_DEPENDENCIES = {
        'aheadworks/module-onestepcheckout' : {
            'aheadworks/module-customer-attributes' : {
                'full_module_name' : 'aheadworks/module-customer-attributes',
                'module_name' : 'module-customer-attributes',
                'platform' : 'community'
            },
            'aheadworks/module-customer-attributes-relation' : {
                'full_module_name' : 'aheadworks/module-customer-attributes-relation',
                'module_name' : 'module-customer-attributes-relation',
                'platform' : 'enterprise'
            }
        }
    }

    def __init__(self):
        self.json_parser = JsonParser()
        self.file_manager = FileManager()
        self.xml_parser = XmlParser()

    def get_module_name(self, path_to_module):
        module_xml_file = path_to_module + self.MODULE_XML_FILE
        module_composer_file = path_to_module + self.MODULE_COMPOSER_FILE
        if os.path.isfile(module_xml_file):
            module_name = self.xml_parser.get_variable_from_file('module', 'name', module_xml_file)
        else:
            full_module_name = self.json_parser.get_variable_from_file('name', module_composer_file)
            owner_module_name, module_name = full_module_name.split('/')

            module_name = module_name.replace('module-', '')
            full_module_name_arr = [
                stringcase.titlecase(owner_module_name),
                stringcase.titlecase(module_name).replace(' ', '')
            ]
            module_name = '_'.join(full_module_name_arr)
        return module_name

    def get_module_version(self, path_to_module):
        module_composer_file = path_to_module + self.MODULE_COMPOSER_FILE
        return self.json_parser.get_variable_from_file('version', module_composer_file)

    def download_modules_from_git(self, path_to_module, tmp_dir_m2_modules, git_workspace='awm2ext'):
        try:
            dir_composer = tmp_dir_m2_modules + '/composer'
            dir_app_code = tmp_dir_m2_modules + '/app/code'

            list_of_module_paths = dict({
                'dir_composer': dir_composer,
                'dir_app_code': dir_app_code,
                'module_names': list(),
                'dir_composer_with_modules': dict(),
                'dir_app_code_with_modules': dict()
            })

            module_dependencies = self.get_module_dependencies(path_to_module)

            self.file_manager.create_dir_by_path(dir_composer)
            self.file_manager.create_dir_by_path(dir_app_code)
            with cd(dir_composer):
                for full_module_name, module in module_dependencies.items():
                    module_name = module['module_name']
                    module_version = module['version']

                    proc = subprocess.Popen(
                        ['git', 'clone', 'git@bitbucket.org:' + git_workspace + '/' + module_name + '.git']
                    )
                    proc.communicate()
                    if proc.returncode != 0:
                        raise Exception('Failed download module ' + module_name)
                    with cd(module_name):
                        proc = subprocess.Popen(['git', 'checkout', module_version])
                        proc.communicate()

                    self.file_manager.remove_files_and_dirs_ignore_case(
                        module_name,
                        ['bitbucket-pipelines.yml', 'readme.md', '.gitignore'],
                        ['.git']
                    )

            for item in os.listdir(dir_composer):
                full_composer_module_path = dir_composer + '/' + item
                module_name = self.get_module_name(full_composer_module_path)
                module_path = module_name.replace('_', '/')
                full_app_code_module_path = dir_app_code + '/' + module_path
                self.file_manager.create_dir_by_path(full_app_code_module_path)
                os.system('cp -r {}/* {}/'.format(full_composer_module_path, full_app_code_module_path))
                list_of_module_paths['module_names'].append(module_name)
        except Exception as error:
            os.system('rm -rf ' + tmp_dir_m2_modules)
            raise Exception(error)

        return list_of_module_paths

    def get_platform_module_dependencies(self, module_name):
        try:
            platform_dependencies = self.PLATFORM_MODULE_DEPENDENCIES[module_name]
        except Exception:
            platform_dependencies = dict()
        return platform_dependencies

    def get_module_dependencies(self, path_to_module):
        return self.get_module_dependencies_from_composer(path_to_module + self.MODULE_COMPOSER_FILE)

    def is_suggested_module(self, path_to_module, suggested_module_name):
        composer_file = path_to_module + self.MODULE_COMPOSER_FILE
        try:
            composer_suggests = self.json_parser.get_variable_from_file('suggests', composer_file)
        except Exception:
            composer_suggests = dict()
        return suggested_module_name in composer_suggests

    def get_module_dependencies_from_composer(self, composer_file):
        list_of_modules = dict()

        core_full_module_name = self.json_parser.get_variable_from_file('name', composer_file)
        core_version = self.json_parser.get_variable_from_file('version', composer_file)
        try:
            composer_requires = self.json_parser.get_variable_from_file('require', composer_file)
        except Exception:
            composer_requires = dict()
        try:
            composer_suggests = self.json_parser.get_variable_from_file('suggests', composer_file)
        except Exception:
            composer_suggests = dict()

        core_module_name = core_full_module_name.split('/')[1]
        list_of_modules[core_full_module_name] = dict(
            {
                'module_name': core_module_name,
                'full_module_name': core_full_module_name,
                'version': core_version.strip('><=')
            }
        )

        list_of_modules.update(self._get_valid_dependency('requires', composer_requires.items(), core_full_module_name))
        list_of_modules.update(self._get_valid_dependency('suggests', composer_suggests.items(), core_full_module_name))
        list_of_modules.update(self.get_platform_module_dependencies(core_full_module_name))

        return list_of_modules

    def _get_valid_dependency(self, type, items, core_full_module_name):
        list_of_modules = dict()

        for full_module_name, version in items:
            if self._is_valid_dependency(type, full_module_name, core_full_module_name):
                module_name = full_module_name.split('/')[1]
                list_of_modules[full_module_name] = dict(
                    {'module_name': module_name, 'full_module_name': full_module_name, 'version': version.strip('><=')}
                )
        return list_of_modules.items()

    def _is_valid_dependency(self, type, full_module_name, core_full_module_name):
        exclusion_modules = dict({'aheadworks/module-faq': ['aheadworks/module-chat-bot']})

        result = False
        if type == 'requires':
            result = full_module_name.find('aheadworks') != -1
        elif type == 'suggests':
            result = (core_full_module_name in exclusion_modules
                      and full_module_name in exclusion_modules[core_full_module_name]) \
                    or full_module_name.find(core_full_module_name) != -1

        return result
