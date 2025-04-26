import os
import sys
import json
import asyncio
import aiofiles
from .CodingAgent import CodingAgent
from .FileManagerAgent import FileManagerAgent
from .IdeaDevelopment import IdeaDevelopment
from .PrePromptAgent import PrePromptAgent
from .TaskPlanner import TaskPlanner
from .ContextPrepareAgent import ContextPrepareAgent
from .SearchAgent import SearchAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.ImageAgent.ImageControllerAgent import ImageControllerAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.MainOperation.ProjectsRunner import ProjectsRunner
from fsd.system.FileContentManager import FileContentManager
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.dependency.DependencyControllerAgent import DependencyControllerAgent
from fsd.Deployment.DeploymentControllerAgent import DeploymentControllerAgent 
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.coding_agent.ContextBugAgent import ContextBugAgent
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
from fsd.compile.compileControllerAgent import CompileControllerAgent
from fsd.coding_agent.LintPlanner import LintPlanner
from fsd.coding_agent.BugTaskPlanner import BugTaskPlanner
from fsd.system.linter import Linter
import shutil
from git import Repo
from fsd.coding_agent.InitNewProjectAgent import InitNewProjectAgent


logger = get_logger(__name__)

class ControllerAgent:
    def __init__(self, repo, explainer_controller):
        self.repo = repo
        directory_path = self.repo.get_repo_path()
        self.directory_path = directory_path
        self.bugPlanner = LintPlanner(repo)
        self.explainer_controller = explainer_controller
        self.idea = IdeaDevelopment(repo)
        self.preprompt = PrePromptAgent(repo)
        self.coder = CodingAgent(repo)
        self.project = ProjectManager(repo)
        self.image = ImageControllerAgent(repo)
        self.compile = CompileControllerAgent(repo)
        self.runner = ProjectsRunner(repo)
        self.fileManager = FileManagerAgent(repo)
        self.deploy = DeploymentControllerAgent(repo)
        self.code_manager = FileContentManager(repo)  # Initialize CodeManager in the constructor
        self.crawler = CrawlerAgent()
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.dependency = DependencyControllerAgent(repo)
        self.context = ContextPrepareAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.contextFinder = ContextBugAgent(repo)
        self.taskPlanner = TaskPlanner(repo)
        self.bugTaskPlanner = BugTaskPlanner(repo)
        self.init_project_agent = InitNewProjectAgent(repo)
        self.searchAgent = SearchAgent()
        
        # Initialize linter with proper error handling
        try:
            self.linter = Linter(root=self.repo.get_repo_path())
        except Exception as e:
            logger.warning(f"Error initializing linter: {str(e)}")
            # Create empty linter class that returns no errors
            from types import SimpleNamespace
            self.linter = SimpleNamespace()
            self.linter.lint_files = lambda file_paths: {fname: {"error": False, "text": "", "lines": []} for fname in file_paths}
        
        self.explainer_controller.initial_setup()

    async def get_fixing_requests(
        self, instructions, context, file_lists, context_files,
        role, crawl_logs,file_attachments, assets_link
    ):
        """Generate coding requests based on instructions and context."""
        logger.info("#### `SnowX` is preparing the task.")
        plan = await self.bugTaskPlanner.get_task_plans(instructions['Implementation_plan'], file_lists)
        commits = plan.get('commits', "")
        logger.info("-------------------------------------------------")
        logger.info("#### `SnowX` is starting to fix")
        
        # Create a single BugFixingAgent for all tasks
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


    async def get_coding_requests(self, instructions, context, file_lists, context_files, role, crawl_logs, file_attachments, assets_link):
        """Generate coding requests based on instructions and context."""

        logger.info("#### `SnowX` is preparing the task.")
        file_count = len(file_lists)
        if file_count <= 3:
            logger.info(f"#### Starting with {file_count} files. This'll be quick! ⚡")
        elif file_count <= 10:
            logger.info(f"#### Starting with {file_count} files. Won't take long! 🚀")
        elif file_count <= 20:
            logger.info(f"#### Starting with {file_count} files. Grab a coffee, I got this! ☕")
        else:
            logger.info(f"#### Starting with {file_count} files. Might take a bit, but it'll be worth it! 🌟")

        final_instructions = ""

        try:
            logger.debug(f"Processing instructions with keys: {list(instructions.keys())}")
            if 'original_prompt' in instructions and instructions['original_prompt'] != "":
                final_instructions = instructions['original_prompt'] + "\n\n" + instructions['Implementation_plan']
            else:
                final_instructions = instructions['Implementation_plan']
            logger.debug(f"Final instructions prepared with length: {len(final_instructions)}")
        except KeyError as ke:
            logger.error(f"KeyError while processing instructions: {str(ke)}")
            logger.debug(f"Available keys in instructions: {list(instructions.keys())}")
            final_instructions = instructions.get('Implementation_plan', "")
        except Exception as e:
            logger.error(f"Unexpected error while preparing instructions: {str(e)}")
            final_instructions = instructions.get('Implementation_plan', "")

        self.coder.initial_setup(context_files, final_instructions, context, crawl_logs, file_attachments, assets_link)

        logger.info("#### `SnowX` is preparing to code.")
        plan = await self.get_taskPlanner(instructions['Implementation_plan'], file_lists)
        commits = plan.get('commits', "")
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


    async def log_result(self, main_path: str, result: str):
        """
        Asynchronously log the result to a file, appending new entries and separating them.

        :param log_path: The name of the log file (e.g., 'log1.txt')
        :param main_path: The main path of the current operation
        :param result: The result to be logged
        """
        full_log_path = os.path.join(self.repo.get_repo_path(), "log1.txt")
        
        try:
            async with aiofiles.open(full_log_path, 'a') as log_file:
                await log_file.write(f"\n\n-----------------\n")
                await log_file.write(f"Main Path: {main_path}\n")
                await log_file.write(f"Result:\n{result}\n")
            
            logger.info(f" #### Successfully appended log to {full_log_path}")
        except Exception as e:
            logger.error(f"  Error writing to log file {full_log_path}: {str(e)}")



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

    async def get_prompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.prompt.get_prompt_plans(user_prompt)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)
    
    async def get_taskPlanner(self, instruction, file_lists):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlanner.get_task_plans(instruction, file_lists)

    async def get_idea_plans(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.idea.get_idea_plans(user_prompt)

    async def get_bugs_plans(self, files, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.bug_scanner.get_idea_plans(files, user_prompt)

    async def get_long_idea_plans(self, files, user_prompt, is_first):
        """Generate idea plans based on user prompt and available files."""
        return await self.long.get_idea_plans(files, user_prompt, is_first)

    async def get_file_planning(self, idea_plan):
        """Generate file planning based on idea plan and directory tree."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def get_adding_file_planning(self, idea_plan, tree, file_attachments):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_adding_file_plannings(idea_plan, tree, file_attachments)

    async def get_moving_file_planning(self, idea_plan, tree, file_attachments):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_moving_file_plannings(idea_plan, tree, file_attachments)

    async def run_requests(self, request_list, role, file_attachments, focused_files):
        """Run project requests."""
        return await self.runner.run_project(request_list, role, file_attachments, focused_files)


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

    async def process_moving(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_moving'):
            processes = data.get('Moving_files', [])
            await self.project.execute_files_creation(processes)

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


    async def build_and_fix_compile_error(self, file_list, role, file_attachments, focused_files):
        """Build project and fix compile errors."""
        await self.run_requests(file_list, role, file_attachments, focused_files)


    async def fix_compile_error_pipeline(self,file_list, role, file_attachments, focused_files):
        """Pipeline for fixing compile errors."""
        logger.info("-------------------------------------------------")
        await self.build_and_fix_compile_error(file_list, role, file_attachments, focused_files)
        logger.info("-------------------------------------------------")


    async def add_files_folders_pipeline(self, finalPrompt, role, file_attachments):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug(" #### Initiating add_files_folders_pipeline")
        logger.info(" #### `SnowX` is processing files.")
        file_result = await self.get_adding_file_planning(finalPrompt, self.repo.print_tree(), file_attachments)
        await self.process_creation(file_result)
        commits = file_result.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")

        logger.info("-------------------------------------------------")

    async def move_files_folders_pipeline(self, finalPrompt, role, file_attachments):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug("\n #### Initiating move_files_folders_pipeline")
        logger.info(" #### `SnowX` is processing files.")
        file_result = await self.get_moving_file_planning(finalPrompt, self.repo.print_tree(), file_attachments)
        await self.process_moving(file_result)
        commits = file_result.get('commits', "")
        if commits:
            self.repo.add_all_files(f"{commits}")
        logger.info("-------------------------------------------------")

    async def explainer_code_task_pipeline(self, tier, solution, role, file_attachments, assets_link):
        """Pipeline for regular coding tasks."""
        try:
            logger.info("-------------------------------------------------")
            logger.debug("#### Initiating regular_code_task_pipeline")
            crawl_logs = []

            logger.debug(" #### `SnowX` is performing dependency checks.")
            await self.dependency.get_started_coding_pipeline(solution, [], [])
            logger.debug(" #### `SnowX` has finished with dependency checks.")
            logger.debug("-------------------------------------------------")

            logger.info(" #### `SnowX` is processing files.")
            file_result = await self.get_file_planning(solution)
            await self.process_creation(file_result)
            add = file_result.get('Adding_new_files', [])
            move = file_result.get('Moving_files', [])
            if add or move:
                commits = file_result.get('commits', "")
                if commits:
                    self.repo.add_all_files(f"{commits}")
            logger.debug("\n #### `SnowX` has completed processing files.")
            logger.debug("-------------------------------------------------")
            
            logger.debug(file_result)
            existing_files = file_result.get('Existing_files', [])
            new_adding_files = [item['Parameters']['full_path'] for item in file_result.get('Adding_new_files', [])]
            new_moving_files = [item['Parameters']['new_full_path'] for item in file_result.get('Moving_files', [])]
            context_files = []

            # Create a dictionary of basename to full path for new_moving_files
            new_moving_dict = {os.path.basename(path): path for path in new_moving_files}

            # Prioritize new_moving_files over existing_files with the same basename
            final_working_files = set()
            for file in existing_files:
                basename = os.path.basename(file)
                if basename in new_moving_dict:
                    final_working_files.add(new_moving_dict[basename])
                else:
                    final_working_files.add(file)

            # Add new_adding_files
            final_working_files.update(new_adding_files)

            final_working_files = self.filter_non_asset_files(final_working_files)
            all_context = await self.build_existing_context(list(final_working_files))

            final_request = {"original_prompt": "", "Implementation_plan": solution}
            commits = await self.get_coding_requests(
                final_request, all_context, list(final_working_files), context_files, role, crawl_logs, file_attachments, assets_link
            )

            self.repo.add_all_files(f"{commits}")

            await self.lintCheck(list(final_working_files), file_attachments, [])

            self.idea.clear_conversation_history()
            self.coder.clear_conversation_history()

            await self.image.get_started_image_generation(tier, solution)
        except:
            logger.debug(" #### `SnowX` has encountered some bugs. We apologize for the inconvenience. Please try again!")

    async def regular_code_task_pipeline(self, tier, finalPrompt, role, file_attachments, focused_files):
        try:
            """Pipeline for regular coding tasks."""
            logger.info("-------------------------------------------------")
            logger.debug("#### Initiating regular_code_task_pipeline")  

            await self.init_project_agent.get_initNewProject_plans(finalPrompt)

            await self.codingProgress(tier, finalPrompt, role, file_attachments, focused_files)

            logger.info(" #### `SnowX` has completed the coding phase.")
            logger.info("-------------------------------------------------")
        except Exception as e:
            logger.debug(f" #### `SnowX` has encountered an error: {str(e)}. We apologize for the inconvenience. Please try again!")

    async def codingProgress(self, tier, finalPrompt, role, file_attachments, focused_files):
        crawl_logs = []
        idea_plan = ""

        while True:
            self.idea.clear_conversation_history()

            logger.info(" #### `SnowX` is gathering context and preparing relevant data...")

            image_result = await self.imageAgent.process_image_links(finalPrompt)
            assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []

            context = await self.context.get_file_planning(finalPrompt, file_attachments, focused_files, assets_link)
            all_files = set(context.get('working_files', []))
            if file_attachments:
                all_files.update(file_attachments)
            if focused_files:
                all_files.update(focused_files)
            if all_files:
                files_list = "\n".join([f"  - {file}" for file in all_files])
                logger.info(f" #### `SnowX` is reading files:\n{files_list}")
            logger.info("#### Thinking completed.")

            self.idea.initial_setup(role, crawl_logs, context, file_attachments, assets_link)

            if idea_plan:
                logger.info(" #### `SnowX` is updating implementation plan.")
            else:
                logger.info(" #### `SnowX` is creating implementation plan.")

            idea_plan = await self.get_idea_plans(finalPrompt)

            if idea_plan:
                break

        if "#### DONE: *** - D***" in str(idea_plan) or "#### DONE: *** - D*** I**" in str(idea_plan):
            await self.dependency.get_started_coding_pipeline(idea_plan, file_attachments, focused_files)
            logger.debug(" #### `SnowX` has finished with dependency checks.")
            logger.debug("-------------------------------------------------")

        logger.info(" #### `SnowX` is processing files.")
        file_result = await self.get_file_planning(idea_plan)
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
        
        final_request = {"original_prompt": finalPrompt, "Implementation_plan": idea_plan}

        commits = await self.get_coding_requests(
            final_request, all_context, list(final_working_files), context_files, role, crawl_logs, file_attachments, assets_link
        )
        
        await self.lintCheck(list(final_working_files), file_attachments, focused_files)

        self.repo.add_all_files(f"{commits}")

        self.idea.clear_conversation_history()
        self.coder.clear_conversation_history()
            
        await self.image.get_started_image_generation(tier, idea_plan)

        return final_working_files
    
    async def lintCheck(self, working_files, file_attachments, focused_files):
        """
        Check working files for linting errors and fix them if found.
        Implements smart linting to detect and skip false positives.
        """
        totalfile = set()
        optimization_related_files = set()
        retries = 0
        max_retries = 1
        
        # Track previous errors to detect false positives
        previous_errors = {}

        # Initialize linter with repo path
        while retries < max_retries:
            try:
                # Safely check if linter is working
                if not hasattr(self.linter, 'lint_files'):
                    logger.warning("Linter is not properly initialized, skipping lint check")
                    return list(totalfile)
                
                # Run linter on all working files
                try:
                    lint_results = self.linter.lint_files(list(working_files))
                except Exception as e:
                    logger.warning(f"Error during lint_files: {str(e)}")
                    return list(totalfile)
                
                # Check if any files have errors
                files_with_errors = {
                    fname: result for fname, result in lint_results.items() 
                    if result["error"]
                }
                
                if not files_with_errors:
                    logger.info(" #### `SnowX` found no errors - code quality check passed")
                    return list(totalfile)
                
                # Filter out false positives by comparing with previous errors
                real_errors = {}
                for fname, result in files_with_errors.items():
                    if fname not in previous_errors or previous_errors[fname] != result:
                        real_errors[fname] = result
                        previous_errors[fname] = result
                
                if not real_errors:
                    logger.info(" #### `SnowX` detected only false positives - code quality check passed")
                    return list(totalfile)
                
                # Format error messages for context
                error_message = "The following files have linting errors:\n\n"
                for fname, result in real_errors.items():
                    rel_path = os.path.relpath(fname, self.repo.get_repo_path())
                    error_message += f"File: {rel_path}\n{result['text']}\n\n"

                logger.info(" #### `SnowX` has detected linting issues and will commence optimization")
                # Get repo structure for context
                overview = self.repo.print_tree()

                context = await self.contextFinder.get_file_planning(error_message)

                # Update files to optimize
                optimization_related_files.update(working_files)
                optimization_related_files.update(totalfile)
                optimization_related_files.update(context.get('working_files', []))
                
                if optimization_related_files:
                    files_list = "\n".join([f"- {file}" for file in optimization_related_files])
                    logger.info(f" #### `SnowX` is reading files:\n{files_list}")

                logger.info(" #### Completed reading files")
            
                fix_plans = await self.bugPlanner.get_bugFixed_suggest_requests(
                    error_message, list(optimization_related_files), overview)

                if "#### DONE: *** - F****" in fix_plans:
                    logger.info(" #### `OptimizationPlanner` has detected potential false positives - optimization complete")
                    return list(totalfile)

                logger.info(" #### `OptimizationPlanner` has completed analysis and created optimization plan")

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

                final_request = {"original_prompt": "Optimizing code", "Implementation_plan": fix_plans}

                commits = await self.get_fixing_requests(
                    final_request, all_context, list(final_working_files), context_files, "top expert code optimizer", [], file_attachments, []
                )

                self.repo.add_all_files(f"{commits}")
                logger.info(" #### `SnowX` has successfully applied optimizations")

                # Check if errors were actually fixed
                new_lint_results = self.linter.lint_files(list(working_files))
                if any(result["error"] for result in new_lint_results.values()):
                    # If errors remain, increment retry counter and continue loop
                    retries += 1
                    if retries < max_retries:
                        logger.info(f" #### Optimization attempt {retries}/{max_retries} did not fix all issues, retrying...")
                        continue
                    else:
                        logger.warning(f" #### Maximum retries ({max_retries}) reached with remaining linting issues")
                        break
                else:
                    # All errors fixed, exit loop
                    logger.info(" #### All linting issues have been resolved")
                    break

            except Exception as e:
                logger.error(f"  `SnowX` encountered an error during the linting process: {str(e)}")
                retries += 1
                if retries >= max_retries:
                    logger.error(f" #### Maximum retries ({max_retries}) reached after encountering errors")
                    break
                logger.info(f" #### Retrying optimization attempt {retries}/{max_retries}")
                continue

        logger.info(" #### `SnowX` has completed its work")
        return list(totalfile)

    async def get_started(self, user_prompt, tier, file_attachments, focused_files):
        """Process the user prompt."""
        logger.info("-------------------------------------------------")
        logger.info(" #### `SnowX` will now begin processing your request.")

        prePrompt = await self.get_prePrompt(user_prompt)
        role = prePrompt['role']
        pipeline = prePrompt['pipeline']
        realtime_data_needed = prePrompt['realtime_data_needed']

        search_results = ""
        if realtime_data_needed:
            search_queries = prePrompt['search_queries']
            search_results = await self.searchAgent.get_search_plan(search_queries)

        
        if search_results != "":
            user_prompt = "Original user prompt:\n" + user_prompt + "\n\n" + "Here are the search data in the context, including content, citations and images. For images, prefer using the original source URLs here to make the product better and more accurate and comprehensive. Citations are provided to reference where the content was obtained from. Please leverage this data comprehensively and efficiently:\n\n" + search_results

        if pipeline in ["2", 2]:
            await self.add_files_folders_pipeline(user_prompt, role, file_attachments)
        elif pipeline in ["3", 3]:
            await self.move_files_folders_pipeline(user_prompt, role, file_attachments)
        elif pipeline in ["4", 4]:
            user_prompt += "I don't accept any ugly or bad code, please make sure the code is clean and readable. For UI/UX, please make it beautiful and user-friendly, elegant and professional, and make it responsive and adaptive to different screen sizes."
            await self.regular_code_task_pipeline(tier, user_prompt, role, file_attachments, focused_files)
        elif pipeline in ["7", 7]:
            await self.deploy.get_started_deploy_pipeline()
        elif pipeline in ["5", 5]:
            await self.dependency.get_started(user_prompt, file_attachments, focused_files)
        elif pipeline in ["6", 6]:
            await self.compile.get_started(user_prompt, file_attachments, focused_files)
        elif pipeline in ["8", 8]:
            await self.explainer_controller.get_started(user_prompt, file_attachments, focused_files)
        else:
            logger.error(user_prompt)

        logger.info("#### `SnowX` has verified that all requested tasks have been completed.")
        logger.info("-------------------------------------------------")
