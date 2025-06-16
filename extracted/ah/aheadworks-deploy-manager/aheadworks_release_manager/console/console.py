import os
from aheadworks_release_manager.api.release_manager import ReleaseManager
from aheadworks_release_manager.api.pipeline_manager import PipelineManager
from aheadworks_core.model.data.teamwork import TeamworkConfig
import traceback

class Console:
    """
    this application needed next env variables
    TEAMWORK_TOKEN
    """

    def __init__(self):
        teamwork_config = TeamworkConfig('ravedigital', os.getenv('TEAMWORK_TOKEN'))
        self.release_manager = ReleaseManager(teamwork_config)
        self.pipeline_manager = PipelineManager()

    def teamwork_release(self, jira_project_key, composer_file, discord_bot_url, path_to_files, assign_to):
        try:
            self.release_manager.teamwork_release(
                jira_project_key,
                composer_file,
                discord_bot_url,
                path_to_files,
                assign_to
            )
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            exit_code = 1

        exit(exit_code)

    def build_swagger_web_api_doc(
            self,
            path_to_module,
            magento_url,
            magento_path_on_server='/var/www/html'
    ):
        try:
            result = self.release_manager.build_swagger_web_api_doc(
                path_to_module,
                magento_url,
                magento_path_on_server
            )
            print(result)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)

    def build_ecommerce_pack(self, bitbucket_workspace, bitbucket_repo_slug):
        try:
            self.release_manager.build_ecommerce_pack(bitbucket_workspace, bitbucket_repo_slug)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)

    def build_mm_pack(self):
        try:
            self.release_manager.build_mm_pack()
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)

    def build_metapackage_pack(self, bitbucket_workspace, bitbucket_repo_slug, artifacts_dir=None):
        try:
            self.release_manager.build_metapackage_pack(bitbucket_workspace, bitbucket_repo_slug, artifacts_dir)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)

    def send_pipelines_to_workspace(self, bitbucket_workspace):
        try:
            self.pipeline_manager.send_pipelines_to_workspace(bitbucket_workspace)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1
        exit(exit_code)
