import os
import asyncio
import re
from pbxproj import XcodeProject
from pbxproj.pbxextensions import FileOptions
import shutil
from datetime import datetime
import string
import random
import subprocess
import platform
from typing import List, Dict, Optional
import ntpath

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ProjectManager:
    def __init__(self, repo):
        self.repo = repo
        self.is_windows = platform.system() == 'Windows'

    @staticmethod
    def get_current_time_formatted() -> str:
        return datetime.now().strftime("%m/%d/%y")

    async def create_and_add_file_to_xcodeproj(self, full_path: str) -> Optional[str]:
        if not self._validate_inputs(full_path):
            return None

        # Normalize path for cross-platform compatibility
        full_path = os.path.normpath(full_path)
        base_project_dir = os.path.dirname(full_path)
        file_name = os.path.basename(full_path)
        relative_path = os.path.relpath(os.path.dirname(full_path), base_project_dir)
        app_name = self._extract_app_name(relative_path)

        if os.path.exists(full_path):
            logger.debug(f"File '{file_name}' already exists in {os.path.dirname(full_path)}. Skipping creation.")
            return None

        self._create_file_with_content(full_path, app_name)
        xcodeproj_path = self._find_xcodeproj(base_project_dir)

        if not xcodeproj_path:
            logger.debug(f"No .xcodeproj file found in {base_project_dir}.")
            return None

        self._add_file_to_xcode_project(xcodeproj_path, full_path, relative_path)
        logger.info(f"Added file `{file_name}` to Xcode project.\n")
        return full_path

    async def create_file_or_folder(self, full_path: str) -> Optional[str]:
        if not self._validate_inputs(full_path):
            return None

        # Normalize path for cross-platform compatibility
        full_path = os.path.normpath(full_path)
        if os.path.exists(full_path):
            logger.debug(f"File '{os.path.basename(full_path)}' already exists. Skipping creation.")
            return None

        self._create_empty_file(full_path)
        logger.info(f"File `{os.path.basename(full_path)}` created successfully.\n")
        return full_path

    async def move_file_within_xcodeproj(self, old_full_path: str, new_full_path: str) -> Optional[str]:
        # Normalize paths for cross-platform compatibility
        old_full_path = os.path.normpath(old_full_path)
        new_full_path = os.path.normpath(new_full_path)

        if not os.path.exists(old_full_path):
            logger.debug(f"File to move '{os.path.basename(old_full_path)}' not found.")
            return None

        if os.path.exists(new_full_path):
            logger.debug(f"Destination file '{os.path.basename(new_full_path)}' already exists. Skipping relocation.")
            return None

        self._move_file(old_full_path, new_full_path)
        xcodeproj_path = self._find_xcodeproj(os.path.dirname(new_full_path))

        if not xcodeproj_path:
            logger.debug(f"No .xcodeproj file found in {os.path.dirname(new_full_path)}.")
            return None

        relative_path = os.path.relpath(os.path.dirname(new_full_path), os.path.dirname(xcodeproj_path))
        self._update_xcode_project(xcodeproj_path, old_full_path, new_full_path, relative_path)
        logger.info(f"File moved successfully: `{os.path.relpath(old_full_path)}` -> `{os.path.relpath(new_full_path)}`.\n")
        return new_full_path

    async def move_file(self, old_full_path: str, new_full_path: str) -> Optional[str]:
        # Normalize paths for cross-platform compatibility
        old_full_path = os.path.normpath(old_full_path)
        new_full_path = os.path.normpath(new_full_path)

        if not os.path.exists(old_full_path):
            logger.debug(f"File to move '{os.path.basename(old_full_path)}' not found.")
            return None

        if os.path.exists(new_full_path):
            logger.debug(f"Destination file '{os.path.basename(new_full_path)}' already exists. Skipping relocation.")
            return None

        self._move_file(old_full_path, new_full_path)
        logger.info(f"File moved successfully: `{os.path.relpath(old_full_path)}` -> `{os.path.relpath(new_full_path)}`.\n")
        return new_full_path

    async def execute_files_creation(self, instructions: List[Dict]) -> None:
        # Open folder in default file explorer before processing instructions
        repo_path = os.path.normpath(self.repo.get_repo_path())
            
        for instruction in instructions:
            logger.debug("Initiating a new task.")
            self._log_instruction(instruction)

            parameters = instruction["Parameters"]
            function_name = instruction["Function_to_call"]
            pipeline = instruction["Pipeline"]

            await self._execute_instruction(function_name, pipeline, parameters)

        if self.is_windows:
            os.startfile(repo_path)
        else:  # macOS
            subprocess.run(['open', repo_path])

    def _validate_inputs(self, full_path: str) -> bool:
        return True

    @staticmethod
    def _extract_app_name(relative_path: str) -> str:
        return relative_path.split('/')[0] if relative_path else 'UnknownApp'

    def _create_file_with_content(self, full_path: str, app_name: str) -> None:
        file_content = f"""// \n//  {os.path.basename(full_path)} \n//  {app_name} \n// \n//  Created by Zinley on {self.get_current_time_formatted()} \n// \n"""
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(file_content)
        logger.debug(f"Created '{os.path.basename(full_path)}' in {os.path.dirname(full_path)}.")

    @staticmethod
    def _find_xcodeproj(base_project_dir: str) -> Optional[str]:
        return next((os.path.join(base_project_dir, item) for item in os.listdir(base_project_dir) if item.endswith('.xcodeproj')), None)

    def _add_file_to_xcode_project(self, xcodeproj_path: str, full_path: str, relative_path: str) -> None:
        project = XcodeProject.load(os.path.join(xcodeproj_path, "project.pbxproj"))
        file_options = FileOptions(create_build_files=True)

        parent_group = self._get_or_create_groups(project, relative_path)

        project.add_file(full_path, file_options=file_options, force=False, parent=parent_group)
        project.save()
        logger.debug(f"Added '{os.path.basename(full_path)}' to the Xcode project.")

    @staticmethod
    def _get_or_create_groups(project: XcodeProject, relative_path: str) -> Optional[object]:
        if not relative_path:
            return None
        parent_group = project.get_or_create_group(relative_path.split('/')[0])
        for part in relative_path.split('/')[1:]:
            parent_group = project.get_or_create_group(part, parent=parent_group)
        return parent_group

    def _create_empty_file(self, full_path: str) -> None:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        open(full_path, 'a').close()
        logger.debug(f"Created an empty file '{os.path.basename(full_path)}' in {os.path.dirname(full_path)}.")

    def _move_file(self, existing_file_path: str, new_full_path: str) -> None:
        os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
        os.rename(existing_file_path, new_full_path)
        logger.debug(f"Relocated '{os.path.basename(new_full_path)}' to {os.path.dirname(new_full_path)}.")

    def _update_xcode_project(self, xcodeproj_path: str, existing_file_path: str, new_full_path: str, new_relative_path: str) -> None:
        project = XcodeProject.load(os.path.join(xcodeproj_path, "project.pbxproj"))
        file_options = FileOptions(create_build_files=True)

        existing_file_refs = project.get_files_by_path(existing_file_path)
        for file_ref in existing_file_refs:
            project.remove_file_by_id(file_ref.get_id())
            logger.debug(f"Removed old file reference: {file_ref}")

        parent_group = self._get_or_create_groups(project, new_relative_path) or project.root_group

        project.add_file(new_full_path, file_options=file_options, force=False, parent=parent_group)
        project.save()
        logger.debug(f"Added '{os.path.basename(new_full_path)}' to the Xcode project at the new location: {new_full_path}")

    @staticmethod
    def _log_instruction(instruction: Dict) -> None:
        try:
            logger.debug(f"Executing Step {instruction}")
        except KeyError:
            logger.debug(f"Issue with instruction: {instruction}")

    async def _execute_instruction(self, function_name: str, pipeline: str, parameters: Dict) -> None:
        if "create_and_add_file" in function_name:
            if pipeline == "1" or pipeline == 1:
                await self.create_and_add_file_to_xcodeproj(**parameters)
            elif pipeline == "2" or pipeline == 2:
                await self.create_file_or_folder(**parameters)
            else:
                logger.debug(f"Unknown creation pipeline: {pipeline}")
        elif "move_file" in function_name:
            if pipeline == "1" or pipeline == 1:
                await self.move_file_within_xcodeproj(**parameters)
            elif pipeline == "2" or pipeline == 2:
                await self.move_file(**parameters)
            else:
                logger.debug(f"Unknown moving pipeline: {pipeline}")
        else:
            logger.debug(f"Unknown function: {function_name}")




# Usage example:
# manager = XcodeProjectManager("/path/to/project")
# asyncio.run(manager.execute_instructions(instructions))