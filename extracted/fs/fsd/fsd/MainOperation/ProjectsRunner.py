import os
import aiohttp
import asyncio
import json
import sys
import subprocess
import time
import requests
import re

from fsd.util import utils
from fsd.util.utils import parse_payload

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.FileManagerAgent import FileManagerAgent
from fsd.coding_agent.CodingAgent import CodingAgent
from fsd.coding_agent.BugTaskPlanner import BugTaskPlanner
from fsd.coding_agent.LintPlanner import LintPlanner
from fsd.coding_agent.ContextBugAgent import ContextBugAgent
from fsd.util.utils import get_preferred_simulator_uuid
from .ProjectManager import ProjectManager
from .MainBuilderAgent import MainBuilderAgent
from fsd.system.FileContentManager import FileContentManager
from fsd.log.logger_config import get_logger
from fsd.compile.compileControllerAgent import CompileControllerAgent
logger = get_logger(__name__)
from fsd.util.utils import read_file_content

class ProjectsRunner:
    def __init__(self, repo):
        self.repo = repo
        self.directory_path = self.repo.get_repo_path()
        self.coder = CodingAgent(repo)
        self.BugTaskPlanner = BugTaskPlanner(repo)
        self.bugPlanner = LintPlanner(repo)
        self.project = ProjectManager(repo)
        self.fileManager = FileManagerAgent(repo)
        self.builderAgent = MainBuilderAgent(repo)
        self.compile = CompileControllerAgent(repo)
        self.code_manager = FileContentManager(repo)
        self.contextFinder = ContextBugAgent(repo)
    
    async def run_project(self, basename, role,file_attachments, focused_files, max_retries=20):
        result = await self.builderAgent.get_pipeline_plans(basename)
        logger.info(" #### `SnowX` is initiating work.")
        pipeline = result["pipeline"]

        if pipeline == "1" or pipeline == 1:
            return await self.run_xcode_project(basename, role, file_attachments, focused_files)
        elif pipeline == "2" or pipeline == 2:
            return await self.compile.start_CLI_compile_process("Run this project in the simplest way possible. Use default configurations and assume all dependencies are installed.", basename,file_attachments, focused_files)
        else:
            logger.info(" #### The `ProjectsRunner` is requesting manual project execution and feedback.")

        return []
       

    async def run_xcode_project(self, basename, role, file_attachments, focused_files, max_retries=10):
        """
        Builds and runs an Xcode project using xcodebuild.

        Parameters:
        - basename (list): The base name list to update.
        - scheme (str): The scheme to build and run.
        - max_retries (int): Maximum number of retries for building the project.

        Returns:
        - output (str): The output of the xcodebuild command or an error message if the build fails.
        """
        scheme = self.repo.get_project_name()
        project_directory = self.repo.get_repo_path()
        os.chdir(project_directory)

        # Get the preferred simulator UUID
        preferred_simulator_uuid = get_preferred_simulator_uuid()

        totalfile = set()
        fixing_related_files = set()

        xcodebuild_command = [
            'xcodebuild',
            '-scheme', scheme,
            '-destination', f'platform=iOS Simulator,id={preferred_simulator_uuid}',
            'build'
        ]
        logger.info(f" #### Full build command: {' '.join(xcodebuild_command)}")

        retries = 0
        cleaned = False
        bugFixed = False

        while retries < max_retries:
            self.bugPlanner.clear_conversation_history()

            self.bugPlanner.initial_setup(role)

            try:
                if retries > 0 and not cleaned:
                    # Clean the build folder and reset the builder on subsequent retries
                    subprocess.run(['xcodebuild', 'clean', '-scheme', scheme], check=True, text=True, capture_output=True)
                    build_folder_path = os.path.join(project_directory, 'build')
                    if os.path.exists(build_folder_path):
                        subprocess.run(['rm', '-rf', build_folder_path], check=True)
                    subprocess.run(['xcodebuild', '-scheme', scheme, 'clean'], check=True, text=True, capture_output=True)
                    cleaned = True

                subprocess.run(xcodebuild_command, check=True, text=True, capture_output=True)

                self.bugPlanner.clear_conversation_history()

                if retries > 0:
                    logger.info(f" #### `SnowX` is reporting successful build after {retries + 1} attempts.")
                else:
                    logger.info(" #### `SnowX` is reporting successful build on first attempt.")
                
                bugFixed = True
                break

            except subprocess.CalledProcessError as e:
                logger.info(" #### `SnowX` is initiating repair process.")

                bug_log_content = e.stdout if e.stdout else e.stderr
                
                if 'Select a development team in the Signing & Capabilities editor.' in bug_log_content:
                    logger.info(" #### `SnowX` has detected a signing issue.")
                    logger.info(" #### Please go to Xcode and select a development team in the Signing & Capabilities editor.")
                    logger.info(" #### After fixing this, please try again to help Zinley build and activate self-healing.")
                    return

                overview = self.repo.print_tree()
                damagefile, output_string = self.log_errors(bug_log_content)

                if not damagefile:
                    logger.info(" #### `SnowX` has encountered a self-healing issue.")
                    logger.info(" #### Unable to locate damaged files. Please double-check your Xcode setup and try again.")
                    return
                
                context = await self.contextFinder.get_file_planning(output_string)

                # Ensure basename list is updated without duplicates
                fixing_related_files.update(list(context.get('working_files', [])))
                fixing_related_files.update(damagefile)
                fixing_related_files.update(list(totalfile))
                if fixing_related_files:
                    files_list = "\n".join([f"  - {file}" for file in fixing_related_files])
                    logger.info(f" #### `SnowX` is reading files:\n{files_list}")

                try:
                    logger.info(" #### `SnowX` is analyzing bugs and creating fix plan.")
                    fix_plans = await self.bugPlanner.get_bugFixed_suggest_requests(output_string, list(fixing_related_files), overview, file_attachments, focused_files)
                    logger.info(" #### `SnowX` has completed analysis and plan creation.")

                    logger.info(" #### `SnowX` is processing files.")
                    file_result = await self.get_file_planning(fix_plans)
                    await self.process_creation(file_result)
                    add = file_result.get('Adding_new_files', [])
                    move = file_result.get('Moving_files', [])
                    if add or move:
                        commits = file_result.get('commits', "")
                        if commits:
                            self.repo.add_all_files(f"{commits}")
                    logger.debug("\n #### `SnowX` has completed processing files.")

                    logger.debug("-------------------------------------------------")
                    
                    existing_files = file_result.get('Existing_files', [])
                    new_adding_files = [item['Parameters']['full_path'] for item in file_result.get('Adding_new_files', [])]
                    new_moving_files = [item['Parameters']['new_full_path'] for item in file_result.get('Moving_files', [])]
                    totalcontext = context.get('working_files', [])
                    context_files = [file for file in totalcontext if file not in existing_files]

                    new_moving_dict = {os.path.basename(path): path for path in new_moving_files}

                    final_working_files = set()
                    for file in existing_files:
                        basename = os.path.basename(file)
                        if basename in new_moving_dict:
                            final_working_files.add(new_moving_dict[basename])
                        else:
                            final_working_files.add(file)

                    final_working_files.update(new_adding_files)

                    final_working_files = self.filter_non_asset_files(final_working_files)
                    all_context = await self.build_existing_context(list(final_working_files))

                    final_request = {"original_prompt": "Fixing bugs", "Implementation_plan": fix_plans}

                    commits = await self.get_fixing_requests(
                        final_request, all_context, list(final_working_files), context_files, role, [], "", file_attachments, []
                    )

                    self.repo.add_all_files(f"{commits}")

                except requests.exceptions.HTTPError as http_error:
                    if http_error.response.status_code == 429:
                        wait_time = 2 ** retries
                        logger.info(f" #### `SnowX` is pausing due to rate limit.")
                        time.sleep(wait_time)  # Exponential backoff
                    else:
                        raise

                retries += 1

        self.bugPlanner.clear_conversation_history()

        if not bugFixed:
            logger.info(" #### `SnowX` is reporting build failure after max retries.")
        

    def log_errors(self, error_log):
        error_lines = []
        damaged_files = set()
        error_details = []

        # Regular expression to match file path and error line details
        error_regex = re.compile(r'(/[^:]+\.swift):(\d+):(\d+): error: (.+)')

        lines = error_log.split('\n')

        for line in lines:
            if "error:" in line.lower():
                error_lines.append(line)
                match = error_regex.search(line)
                if match:
                    full_file_path = match.group(1)
                    file_name = os.path.basename(full_file_path)  # Extract the filename
                    line_number = int(match.group(2))
                    column_number = int(match.group(3))
                    error_message = match.group(4)

                    damaged_files.add(file_name)

                    # Read the damaged file to get the specific line with the error
                    try:
                        with open(full_file_path, 'r') as swift_file:
                            swift_lines = swift_file.readlines()

                        if line_number <= len(swift_lines):
                            damaged_code = swift_lines[line_number - 1].strip()
                        else:
                            damaged_code = "Line number exceeds file length."

                        # Get additional context around the error line
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': damaged_code
                        })
                    except FileNotFoundError:
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': "File not found."
                        })
                else:
                    # If the error couldn't be parsed, add the original line
                    error_details.append({
                        'file': 'unknown',
                        'line': 'unknown',
                        'column': 'unknown',
                        'message': line.strip(),
                        'code': 'N/A'
                    })

        output_string = ""
        for error in error_details:
            output_string += f"Damaged code: {error['code']} - Error: {error['message']} - File path: {error['file']}\n"
            output_string += "\n" + "-"*80 + "\n\n"  # Adds a separator between errors

        damaged_files_list = list(damaged_files)  # Convert set to list before returning

        logger.info(f"All possible damaged files: {damaged_files_list}.")

        return damaged_files_list, output_string

    async def get_file_planning(self, idea_plan):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def process_creation(self, data):
        """Process the creation and moving of files based on provided data."""
        # Process creation of new files
        if data.get('Is_creating'):
            new_files = data.get('Adding_new_files', [])
            if new_files:
                await self.project.execute_files_creation(new_files)
            else:
                logger.debug(" #### `FileCreationManager`: No new files need to be created.")
        else:
            logger.debug(" #### `FileCreationManager`: Creation flag is not set.")

        # Process moving of files
        moving_processes = data.get('Moving_files', [])
        if moving_processes:
            logger.debug(" #### `FileCreationManager`: about to moving files")
            logger.debug(moving_processes)
            await self.project.execute_files_creation(moving_processes)
        else:
            logger.debug(" #### `FileCreationManager`: No files need to be moved this time.")

        # If no files to create or move
        if not data.get('Is_creating') and not moving_processes:
            logger.debug(" #### `FileCreationManager`: No new files need to be added or moved at this time.")


    async def get_fixing_requests(
        self, instructions, context, file_lists, context_files,
        role, crawl_logs,file_attachments, assets_link
    ):
        """Generate coding requests based on instructions and context."""
        logger.info("#### `SnowX` is preparing the task.")
        plan = await self.BugTaskPlanner.get_task_plans(instructions['Implementation_plan'], file_lists)
        commits = plan.get('commits', "")
        logger.info("-------------------------------------------------")
        logger.info("#### `SnowX` is starting to fix")
        
        self.coder.initial_setup(context_files, instructions, context, crawl_logs, file_attachments, assets_link)
        
        for step in plan.get('steps', []):
            file_name = step.get('file_name')
            if self.is_coding_file(file_name):
                main_path = file_name
                if main_path:
                    logger.info("-------------------------------------------------")
                    logger.info(f"#### `SnowX` is editing file: `{os.path.relpath(file_name, self.directory_path)}`.")

                    try:
                        result = await self.coder.get_coding_request(file_name)

                        await self.code_manager.handle_coding_agent_response(main_path, result)

                        logger.info(f" #### `SnowX` finished successfully: `{os.path.relpath(file_name, self.directory_path)}`.")
                    except Exception as e:
                        logger.error(f"  Error processing file `{file_name}`: {str(e)}")
                else:
                    logger.debug(f" #### File not found: `{file_name}`")

        self.coder.clear_conversation_history()
        return commits
    

    def filter_non_asset_files(self, file_set):
        # Define a set of non-code file extensions (assets and binary files)
        non_code_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
            # Audio
            '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',
            # Video
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
            # Fonts
            '.ttf', '.otf', '.woff', '.woff2', '.eot',
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            # Other binary formats
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
            # Database files
            '.db', '.sqlite', '.mdb',
        }

        # Use a set comprehension to filter out non-code files
        code_files = {file for file in file_set if not any(file.lower().endswith(ext) for ext in non_code_extensions)}

        return code_files

    def is_coding_file(self, filename):
        # Define a set of non-code file extensions (assets and binary files)
        non_code_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
            # Audio
            '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',
            # Video
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
            # Fonts
            '.ttf', '.otf', '.woff', '.woff2', '.eot',
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            # Other binary formats
            '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
            # Database files
            '.db', '.sqlite', '.mdb',
        }

        # Get the file extension
        _, extension = os.path.splitext(filename.lower())

        # If the file has no extension or its extension is not in the non-code list, consider it a code file
        return extension not in non_code_extensions
    
    async def build_existing_context(self, existing_files):
        """Build and return the context of existing files."""
        all_context = ""
        for path in existing_files:
            file_context = read_file_content(path)
            if file_context:
                all_context += f"\n\nFile: {path}:\n{file_context}"
            else:
                all_context += f"\n\nFile: {path}: This file is currently empty, content is \"\", this is just a note, not content"

        return all_context