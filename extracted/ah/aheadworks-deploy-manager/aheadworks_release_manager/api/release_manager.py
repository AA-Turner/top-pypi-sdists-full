from aheadworks_bitbucket_manager.api.bitbucket_api_manager import BitbucketApiManager
from aheadworks_bitbucket_manager.model.data.bitbucket import BitbucketConfig
from aheadworks_core.api.composer_manager import ComposerManager
from aheadworks_core.api.teamwork_manager import TeamworkManager
from aheadworks_core.api.discord_api_manager import DiscordApiManager
from aheadworks_core.api.magento_manager import MagentoManager
from aheadworks_core.api.file_manager import FileManager
from aheadworks_core.model.parser.json import Json as JsonParser
from datetime import datetime
import boto3
import json
import os
import re
import shutil
import subprocess
import requests

class ReleaseManager:
    """api manager for release"""

    RELEASE_PACK_TASK_LABEL = 'RELEASE-PACK'
    PD_TASK_LABEL = 'PD'
    TEST_TASK_LABEL = 'TEST'

    def __init__(self, api_config):
        self.teamwork_manager = TeamworkManager(api_config)
        self.discord_api_manager = DiscordApiManager()
        self.magento_manager = MagentoManager()
        self.file_manager = FileManager()
        self.json_parser = JsonParser()
        self.aws_s3 = boto3.resource('s3')

    def teamwork_release(self, project_id, composer_file, discord_bot_url, path_to_files, assign_to):
        module_version = self.json_parser.get_variable_from_file('version', composer_file)

        print(f"project id: {project_id}")
        print(f"module version: '{module_version}'")
        print(f"discord bot url: {discord_bot_url}")
        print(f"path to files: {path_to_files}")
        print(f"assign to, account id: {assign_to}")

        if not project_id:
            print('project_id is empty, skip teamwork release.')
            return False

        links = self.teamwork_manager.find_tasks_by_tags([f"{project_id}-{module_version}"])
        release_list = self.teamwork_manager.find_tasks_by_tags([f"{project_id}-{module_version}", self.RELEASE_PACK_TASK_LABEL])
        pd_list = self.teamwork_manager.find_tasks_by_tags([f"{project_id}-{module_version}", self.PD_TASK_LABEL])
        test_list = self.teamwork_manager.find_tasks_by_tags([f"{project_id}-{module_version}", self.TEST_TASK_LABEL])
        release_tasks_count = len(release_list) + len(pd_list) + len(test_list)
        if release_tasks_count != 3:
            print(f"release: {release_list}")
            print(f"test: {test_list}")
            print(f"pd: {pd_list}")
            raise Exception(f'There should be exactly 3 release tasks, got {release_tasks_count}.')

        release_task_id = release_list[0]['id']
        test_task_id = test_list[0]['id']
        pd_task_id = pd_list[0]['id']

        tasklist_id = release_list[0]['tasklistId']
        tasklist = self.teamwork_manager.get_tasklist(tasklist_id)
        project_id = str(tasklist['tasklist']['projectId'])
        project_name = tasklist['included']['projects'][project_id]['name']

        # add attachments to the task RELEASE-PACK
        file_names = [os.path.join(path_to_files, file) for file in os.listdir(path_to_files)]
        self.teamwork_manager.add_attachments_to_task(release_task_id, file_names)

        # assign release pack to user
        if (not assign_to == "TEAMWORK_ACCOUNT_ID"):
            self.teamwork_manager.reassign(release_task_id, assign_to)

        module_dependencies = self.magento_manager.get_module_dependencies_from_composer(composer_file)
        composer_package_name = ','.join(list(map(lambda x: x['full_module_name'], module_dependencies.values())))
        self.teamwork_manager.add_comment(release_task_id, f'Composer Package Name:\n{composer_package_name}')

        # Set PD and TEST to Done
        self.teamwork_manager.close_issue(pd_task_id)
        self.teamwork_manager.close_issue(test_task_id)

        release_link = self.teamwork_manager.get_issue_url(release_task_id)
        test_link = self.teamwork_manager.get_issue_url(test_task_id)
        pd_link = self.teamwork_manager.get_issue_url(pd_task_id)

        msg = '{} {}\n'.format(project_name, module_version)
        msg += f'\n{self.RELEASE_PACK_TASK_LABEL}: {release_link}\n{self.TEST_TASK_LABEL}: {test_link}\n{self.PD_TASK_LABEL}: {pd_link}'
        print(msg)

        # ????? msg += '\n' + self.jira_api_manager.get_release_report_all_issues_url(jira_project_key, version.id)
        self.discord_api_manager.send_msg(discord_bot_url, msg)

        return True

    def build_swagger_web_api_doc(
            self,
            path_to_module,
            magento_url,
            magento_path_on_server='/var/www/html'
    ):
        subprocess.check_call("nginx -g \"daemon on;\" & docker-php-entrypoint php-fpm -R &", shell=True)
        aws_bucket_name = 'aheadworks_cdn'
        aws_swagger_web_api_doc_path = 'swagger_web_api_doc/'
        vendor_path = "/var/www/html/vendor/aheadworks/"
        parent_composer = path_to_module + "composer.json"

        # here we define name from /etc/module.xml
        parent_module_name_from_xml = self.magento_manager.get_module_name(path_to_module)
        # in module_list will be added all modules from suggests
        module_list = parent_module_name_from_xml
        if not os.path.isfile(f"{path_to_module}/etc/webapi.xml"):
            return f'Skip Web API doc generation: file etc/webapi.xml has been not found for module {parent_module_name_from_xml}'
        try:
            with open(parent_composer) as f:
                composer = json.load(f)

            parent_module_name = composer['name']
            parent_module_version = composer['version']
            os.chdir(magento_path_on_server)
            os.system(f"composer require {parent_module_name}:{parent_module_version}")
            # fast fix: some modules have no modules in suggests
            if 'suggests' in composer:
                try:
                    for name, version in composer['suggests'].items():
                        os.system(f"composer require {name}:{version}")
                        name_wo_aheadworks = name.split('/')[1]
                        vendor_module_path = vendor_path + name_wo_aheadworks
                        # get names from /etc/module.xml
                        module_name_from_xml = self.magento_manager.get_module_name(vendor_module_path)
                        # add names to list
                        module_list += "," + module_name_from_xml
                except Exception as error:
                    raise Exception(error)
            # generate url for main and suggests modules
            magento_request_url = '/generate_web_api_json.php?module_names={}'.format(module_list)
            swagger_json_page = magento_url + magento_request_url
            # this action need because first call swagger script return error output(maybe modules cant loaded to fast)
            requests.get(swagger_json_page)
            # here we get json output from main and suggests modules
            swagger_json = requests.get(swagger_json_page).text

            try:
                json.loads(swagger_json)
            except Exception as error:
                print(f"Invalid response from Swagger:\n{swagger_json}\n\n")
                raise Exception(error)

            s3_result = self.aws_s3.Bucket(aws_bucket_name).put_object(
                Key=f"{aws_swagger_web_api_doc_path}{parent_module_name_from_xml.lower()}_latest.json",
                Body=swagger_json,
                ACL='public-read'
            )
        except Exception as error:
            raise Exception(error)

        result = f'Web Api Doc Path: https://media.aheadworks.com/{s3_result.key}\n'
        result += f'Magento Request Url: {magento_request_url}\n'
        return result

    def build_ecommerce_pack(self, bitbucket_workspace, bitbucket_repo_slug):
        ComposerManager.init_extra_repos()

        build_dir = os.getcwd()
        relative_path = "/app/code/Aheadworks"
        self.file_manager.create_empty_dir(f"{build_dir}/community{relative_path}")
        self.file_manager.create_empty_dir(f"{build_dir}/enterprise{relative_path}")

        artifacts_dir = "/build_archives"
        self.file_manager.create_empty_dir(artifacts_dir)

        composer = self._load_composer_file(bitbucket_repo_slug, '.')
        core_module_name = composer['name']
        core_module_version = composer['version']
        # check if composer have version that is in composer.json
        print("If you see an error just below, then the composer does not see the version of the package.")
        print("Did you tag latest release?")
        subprocess.run(["composer", "show", "-a", core_module_name, core_module_version], check=True)

        module_dependencies = self.magento_manager.get_module_dependencies('./')
        ComposerManager.require_magento_module(core_module_name, composer['version'])

        # @todo use self.magento_manager.download_modules_from_git(path_to_module, tmp_dir_m2_modules)
        magento_module_info = dict()
        artifacts = list()
        # Preinstall suggested modules with composer into /var/www/html/vendor/aheadworks
        platform_dependencies = self.magento_manager.get_platform_module_dependencies(core_module_name).keys()
        for full_module_name, module_item in module_dependencies.items():
            if self.magento_manager.is_suggested_module(build_dir, full_module_name) or full_module_name in platform_dependencies:
                ComposerManager.require_magento_module(full_module_name)

        # full_module_name          vendor/module-name
        # module_name               module-name
        # magento_package_name      ModuleName
        for full_module_name, module_item in module_dependencies.items():
            module_name = module_item['module_name']
            composer_install_path = f"/var/www/html/vendor/aheadworks/{module_name}"
            magento_package_name = self._get_magento_package_name(full_module_name, composer_install_path)
            magento_module_info[full_module_name] = magento_package_name
            module_composer = self._load_composer_file(full_module_name, composer_install_path)

            print(f"Building {full_module_name} from {composer_install_path} as {module_name}...")
            self._prepare_for_publishing(
                composer_install_path,
                magento_package_name,
                module_composer["version"]
            )
            artifacts.append(
                self._pack_module(composer_install_path, f"{artifacts_dir}/{module_name}.zip")
            )

            # 'community' 'enterprise' or 'any'
            module_plaftorm = module_item.get('platform', 'any')
            for platform in ['community', 'enterprise']:
                if module_plaftorm == 'any' or module_plaftorm == platform:
                    target_module_path = f"{build_dir}/{platform}{relative_path}/{magento_package_name}"
                    shutil.copytree(composer_install_path, target_module_path)

        # Now build store packages
        for platform in ['community', 'enterprise']:
            filename = f"aw_m2_{magento_module_info[core_module_name]}-{composer['version']}.{platform}_edition.zip"
            artifacts.append(
                self._pack_module(f"{build_dir}/{platform}", f"{artifacts_dir}/{filename}", "app")
            )

        self._upload_artifacts(bitbucket_workspace, bitbucket_repo_slug, artifacts)

    # Sample metapackage product: https://bitbucket.org/awm2ext/b2b-suite/
    def build_metapackage_pack(self, bitbucket_workspace, bitbucket_repo_slug, artifacts_dir):
        upload_env = f"REPO_URL={os.getenv('AW_COMPOSER_API_URL')} REPO_LOGIN={os.getenv('AW_COMPOSER_API_LOGIN')} REPO_TOKEN={os.getenv('AW_COMPOSER_API_PASSWORD')}"
        conflicted_module = "aheadworks/module-ui-components"

        # prepare FS
        build_dir = os.getcwd()
        if not artifacts_dir:
            artifacts_dir = "/build_archives"
        self.file_manager.create_empty_dir(artifacts_dir)

        path = f"{build_dir}/app/code/Aheadworks"
        self.file_manager.create_empty_dir(path)

        # Get dependent packages list
        composer = self._load_composer_file(bitbucket_repo_slug, '.')

        # Install dependent packages via Composer first
        for full_module_name in composer["require"]:
            ComposerManager.require_magento_module(full_module_name)

        artifacts = []
        for full_module_name in composer["require"]:
            module = full_module_name.split('/')[1]
            composer_install_path = f"/var/www/html/vendor/aheadworks/{module}"
            module_composer = self._load_composer_file(full_module_name, composer_install_path)
            magento_package_name = self._get_magento_package_name(full_module_name, composer_install_path)
            module_path = f"{path}/{magento_package_name}"

            print(f"Building {full_module_name} as {module} in {module_path}...")
            self._prepare_for_publishing(
                composer_install_path,
                magento_package_name,
                module_composer['version']
            )
            shutil.copytree(composer_install_path, module_path)

            # changing modules name in module_folder in parent directory(build directory)
            old_name = module_composer['name']
            if old_name != conflicted_module and bitbucket_repo_slug != "b2b-suite":
                metapackage_module_name = f"{module}-{bitbucket_repo_slug}-subscription"
                new_name = f"{module_composer['name']}-{bitbucket_repo_slug}-subscription"
                module_composer['name'] = new_name
                print(f"\t\u21E8 Renaming {old_name} to {new_name}...")
            elif old_name != conflicted_module and bitbucket_repo_slug == "b2b-suite":
                metapackage_module_name = f"{module}-{bitbucket_repo_slug}"
                new_name = f"{module_composer['name']}-{bitbucket_repo_slug}"
                module_composer['name'] = new_name
                print(f"\t\u21E8 Renaming {old_name} to {new_name}...")
            else:
                metapackage_module_name = f"{module}"

            with open(f"{module_path}/composer.json", 'w') as f:
                json.dump(module_composer, f, indent=4)

            # changing module names in require
            self._replace_dependencies(f"{module_path}/composer.json", composer["require"], bitbucket_repo_slug)
            # all packs except b2b-suite needs -subscription
            if bitbucket_repo_slug != "b2b-suite":
                composer = self._load_composer_file(bitbucket_repo_slug, '.')
                self._replace_dependencies(f"{module_path}/composer.json", composer["require"], "subscription")

            zip_package_path = f"{artifacts_dir}/{metapackage_module_name}.zip"
            artifacts.append(
                self._pack_module(module_path, zip_package_path)
            )
            upload_as = f"{metapackage_module_name}-{module_composer['version']}.zip"
            os.system(
                f"echo '{upload_env} python3 -m aheadworks_composer_manager send-package --filename={upload_as} {zip_package_path}' >> {artifacts_dir}/upload")
            # ??? Why we upload to Composer server in this noobish manner instead of using API ???
            composer_server_base_path = f"{os.getenv('AW_COMPOSER_PACKAGES_ROOT')}/aheadworks"
            os.system(
                f"ssh -T {os.getenv('AW_COMPOSER_SSH_URL')} 'mkdir -p {composer_server_base_path}/{metapackage_module_name}'")
            os.system(
                f"scp {zip_package_path} {os.getenv('AW_COMPOSER_SSH_URL')}:{composer_server_base_path}/{metapackage_module_name}/{upload_as}")

        # Here we update parent composer.json
        # modules, that download from marketplace should be with -subscription
        if bitbucket_repo_slug != "b2b-suite":
            subscription_suffix = f"-{bitbucket_repo_slug}-subscription"
            with open('composer.json') as f:
                composer = json.load(f)
                old_name = composer["name"]
                new_name = old_name + "-subscription"
                composer["name"] = new_name
            with open('composer.json', 'w') as f:
                json.dump(composer, f, indent=4)
        else:
            subscription_suffix = f"-{bitbucket_repo_slug}"

        data = self._load_composer_file(bitbucket_repo_slug, '.')
        core_version = composer['version']

        # in dict, we're adding name and version from require and then update with it composer.json
        updated_require = {}
        for key, value in data['require'].items():
            if 'aheadworks/module' in key and conflicted_module not in key:
                updated_key = key + subscription_suffix
                updated_require[updated_key] = value
            else:
                updated_require[key] = value

        data['require'] = updated_require

        with open('composer.json', 'w') as f:
            json.dump(data, f, indent=4)

        # build marketplace package
        if bitbucket_repo_slug == "b2b-suite":
            artifacts.append(
                self._pack_module(".", f"{artifacts_dir}/{bitbucket_repo_slug}.zip", "composer.json")
            )
        else:
            artifacts.append(
                self._pack_module(".", f"{artifacts_dir}/{bitbucket_repo_slug}-subscription.zip", "composer.json")
            )

        # store package
        for platform in ['community', 'enterprise']:
            filename = f"aw_m2_{bitbucket_repo_slug}-{core_version}.{platform}_edition.zip"
            artifacts.append(
                self._pack_module(build_dir, f"{artifacts_dir}/{filename}", "app")
            )

        self._upload_artifacts(bitbucket_workspace, bitbucket_repo_slug, artifacts)

    def build_mm_pack(self):
        # basically marketplace pack is an ecommerce pack where all modules have -subscription postfix in their names,
        # so we assume that the ecommerce pack has been built so far
        prebuilt_packages_dir = "/build_archives"
        working_dir = "/tmp/unpack"
        package_dir = "/tmp/packages"
        self.file_manager.create_empty_dir(working_dir)
        self.file_manager.create_empty_dir(package_dir)
        os.system(f"ls -l {prebuilt_packages_dir}")
        # Extract all packages first
        for filename in os.listdir(prebuilt_packages_dir):
            package_fullpath = os.path.join(prebuilt_packages_dir, filename)
            # TODO: process *.zip only
            if os.path.isfile(package_fullpath):
                sources_dir = os.path.join(working_dir, filename)
                print(package_fullpath)
                os.system(f"unzip -q {package_fullpath} -d {sources_dir}")

        # Now gather module names
        module_names = []
        composer_files = self.file_manager.find_all('composer.json', working_dir)
        print(composer_files) # debug
        for composer_file in composer_files:
            package_name = self.json_parser.get_variable_from_file('name', composer_file)
            if not package_name in module_names:
                module_names.append(package_name)

        print(module_names) # debug
        # Replace all found modules names from "vendor/module_name" to "vendor/module_name-subscription"
        # across all composer.json (this includes requires/suggests sections and possibly even more)
        for composer_file in composer_files:
            self._replace_dependencies(composer_file, module_names, "subscription")

        # Create '-subscription' packages
        for originalname in os.listdir(working_dir):
            sources_fullpath = os.path.join(working_dir, originalname)

            split_name, split_extension = os.path.splitext(originalname)
            target_filename = f"{split_name}-subscription{split_extension}"
            target_fullpath = os.path.join(package_dir, target_filename)
            print(target_fullpath) # debug
            self._pack_module(sources_fullpath, target_fullpath)

        # Copy newly built -subscription packages to /build_archives
        os.system(f"cp {package_dir}/* {prebuilt_packages_dir}")

    def _replace_dependencies(self, path_to_composer, module_names, slug):
        fin = open(path_to_composer, "rt")
        data = fin.read()
        fin.close()
        conflicted_module = "aheadworks/module-ui-components"

        for module_name in module_names:
            # we intentionally quote vendor/package_name string to be "vendor/package_name".
            # otherwise vendor/package_name_subname could be renamed
            # into vendor/package_name-subscription_subname
            # instead of vendor/package_name_subname-subscription
            # Do not rename service module module-ui-components
            # to avoid conflicts with non-b2b modules that are also using it
            if slug == "b2b-suite" and module_name == conflicted_module:
                continue
            data = data.replace(f'"{module_name}"', f'"{module_name}-{slug}"')

        fin = open(path_to_composer, "wt")
        fin.write(data)
        fin.close()

    def _pack_module(self, source_module_path, target_package_path, base_dir="."):
        print(f"\t\u21E8 Packing {source_module_path} into {target_package_path}\n")
        base_name, extension = os.path.splitext(target_package_path)
        shutil.make_archive(base_name, extension.lstrip('.'), source_module_path, base_dir)
        return target_package_path

    def _load_composer_file(self, full_module_name, module_path):
        path_to_composer = f"{module_path}/composer.json"
        if not os.path.isfile(path_to_composer):
            os.system(f"ls {module_path}")
            raise Exception(f"Can not build module {full_module_name}: composer.json is missing")

        with open(path_to_composer) as f:
            return json.load(f)

    def _get_magento_package_name(self, full_module_name, module_path):
        if not os.path.isfile(f"{module_path}/registration.php"):
            os.system(f"ls {module_path}")
            raise Exception(f"Can not build module {full_module_name}: registration.php is missing")

        with open(f"{module_path}/registration.php") as reg:
            l = reg.readlines()
            for line in l:
                if line.find("Aheadworks_") != -1:
                    m = re.search("Aheadworks_([^\"']+)", line)
                    return m.group(1)
        return ""

    def _prepare_for_publishing(self, module_path, magento_package_name, module_version):
        print("\t\u21E8 Cleanup filesystem...")
        self.file_manager.remove_files_and_dirs_ignore_case(
            module_path,
            ['bitbucket-pipelines.yml', 'readme.md', '.gitignore'],
            ['.git']
        )

        print("\t\u21E8 Writing license headers...")
        self.file_manager.add_license_to_php_files(module_path, magento_package_name, module_version)
        os.system(f"echo See https://aheadworks.com/end-user-license-agreement/ >> {module_path}/license.txt")

    def _upload_artifacts(self, bitbucket_workspace, bitbucket_repo_slug, filepath):
        print(f"\nUploading artifacts\n{filepath}...\n")
        bitbucket_manager = BitbucketApiManager(
            BitbucketConfig(
                bitbucket_workspace=bitbucket_workspace,
                bitbucket_repo_slug=bitbucket_repo_slug
            )
        )
        print(bitbucket_manager.upload_artifacts(filepath))
