import os
import sys


from .DependencyFileFinderAgent import DependencyFileFinderAgent
from .DependencyTaskPlanner import DependencyTaskPlanner
from .DependencyCheckAgent import DependencyCheckAgent
from .DependencyCheckCLIAgent import DependencyCheckCLIAgent


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.system.CommandRunner import CommandRunner
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
logger = get_logger(__name__)

HOME_DIRECTORY = os.path.expanduser('~')
HIDDEN_ZINLEY_FOLDER = '.zinley'

class DependencyControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.project = ProjectManager(repo)
        self.fileFinder = DependencyFileFinderAgent(repo)
        self.taskPlanner = DependencyTaskPlanner(repo)
        self.command = CommandRunner(repo)
        self.CLI = DependencyCheckCLIAgent(repo)
        self.checker = DependencyCheckAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.directory_path = self.repo.get_repo_path()


    async def guider_pipeline(self, user_prompt):
        """Pipeline for regular coding tasks."""
        logger.info(" #### `SnowX` is initiating the guider pipeline.")

        while True:
            user_prompt_json = input("Do you need more help with dependency?: ")
            guide = await self.guider.get_guider_plans(user_prompt_json)
            finalPrompt = guide['processed_prompt']
            pipeline = guide['pipeline']
            explainer = guide['explainer']

            if pipeline == "0":
                break
            elif pipeline == "1":
                logger.info(explainer)
            elif pipeline == "2":
                logger.info(guide)
                await self.start_dependency_installation_process(user_prompt)
                break


    async def start_dependency_installation_process(self, instruction, file_attachments=None, focused_files=None):
        
        logger.info(instruction)
        logger.info(" #### In order to complete this run, I will need to install some dependencies.")

        os_architecture = self.repo.return_os()
        file_result = await self.fileFinder.get_dependency_file_plannings()
        dependency_files = file_result.get('dependency_files', [])
        all_files = set(file_result.get('dependency_files', []))
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")

        logger.info(" #### `SnowX` is preparing to execute the finalized plan.")
        task = await self.taskPlanner.get_task_plan(instruction, dependency_files, os_architecture)
        await self.command.execute_steps(task, dependency_files)
        commits = task.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")
        logger.info(f" #### `SnowX` has completed the task")

        logger.info("-------------------------------------------------")


    async def start_dependency_installation_process_normal(self, instruction, file_attachments=None, focused_files=None):
        os_architecture = self.repo.return_os()
        file_result = await self.fileFinder.get_dependency_file_plannings()
        dependency_files = file_result.get('dependency_files', [])

        all_files = set(file_result.get('dependency_files', []))
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")

        image_result = await self.imageAgent.process_image_links(instruction)
        assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []
        
        logger.info(" #### `SnowX` is preparing to execute the plan.")
        task = await self.taskPlanner.get_task_plan(instruction, dependency_files, os_architecture)
        await self.command.execute_steps(task, dependency_files)
        commits = task.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")
        logger.info(f" #### `SnowX` has completed the task")

        logger.info("-------------------------------------------------")


    async def get_started(self, user_prompt, file_attachments=None, focused_files=None):
        """Start the processing of the user prompt."""
        logger.info(" #### `SnowX` is beginning to process the user request.")

        await self.start_dependency_installation_process_normal(user_prompt, file_attachments, focused_files)

        logger.info(f" #### `SnowX` has completed processing the request")
        logger.info("-------------------------------------------------")


    async def get_started_coding_pipeline(self, user_prompt, file_attachments=None, focused_files=None):
        logger.info("-------------------------------------------------")
        logger.debug(" #### `SnowX` is assigned.")
        """Start the processing of the user prompt."""

        await self.start_dependency_installation_process(user_prompt, file_attachments, focused_files)

        logger.info(" #### `SnowX` has installed all required dependencies. ")
        logger.info("-------------------------------------------------")
