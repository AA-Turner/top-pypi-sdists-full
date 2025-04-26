import os
import sys
import aiohttp
import asyncio
import json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
import platform

logger = get_logger(__name__)

class LintPlanner:
    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, role):
        """Set up the initial prompt for the bug analysis agent."""
        prompt = (
            f"You are a top expert bug analysis agent for software. Analyze the project files and provide a focused bug fix plan. Follow these guidelines:\n\n"
            f"User OS: {platform.system()}\n"
            f"Project root path: {self.repo.get_repo_path()}\n\n"
            
            "For each bug:\n"
            "1. Core Issue:\n"
            "- Identify the exact bug and affected files\n"
            "- List all files that need changes (with full paths from project root)\n"
            "- If this is a common lint error, indicate if it's a false positive\n\n"
            
            "2. Fix Plan:\n"
            "- Describe specifically what needs to be fixed in each file\n"
            "- Note any critical considerations or potential risks when fixing\n"
            "- List any new dependencies required\n\n"
            
            "Important:\n"
            "- Focus only on what needs to be fixed\n"
            "- Include minimal code snippets only if essential to explain the fix\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Testing plans or verification steps\n"
            "- Implementation details unless critical\n"
            "- Anything not directly related to fixing the bug\n"
            "- Summary sections or overview text\n"
            "- Any form of bug report summaries\n\n"
            
            "Keep responses focused strictly on what needs to be fixed.\n\n"
            
            "If this is a common lint error and appears to be a false positive, end your response with: #### DONE: *** - F****"
        )

        self.conversation_history.append({"role": "system", "content": prompt})

    async def get_bugFixed_suggest_request(self, bug_logs, all_file_contents, overview, file_attachments=None, focused_files=None):
        """Get bug fix suggestions based on logs and files."""
        error_prompt = (
            f"Current working file:\n{all_file_contents}\n\n"
            f"Tree:\n{self.repo.print_tree()}\n\n"
            f"Project overview:\n{overview}\n\n"
            f"Bug logs:\n{bug_logs}\n\n"
            "Analyze the bugs and provide a focused fix plan.\n\n"
            "ABSOLUTELY CRITICAL - File Path Requirements:\n"
            "- You MUST ALWAYS provide COMPLETE, ABSOLUTE file paths starting from project root\n" 
            "- NEVER use relative paths or filenames alone\n"
            "- Example REQUIRED format: /full/path/from/project/root/src/components/file.js\n"
            "- Any file paths not following this format will be REJECTED\n\n"
            "IMPORTANT: Focus only on:\n"
            "- Exact issues that need to be fixed\n"
            "- MANDATORY: Full absolute file paths (from project root) for ALL files needing changes\n"
            "- Critical considerations or risks when implementing fixes\n\n"
            "DO NOT include:\n"
            "- Testing plans or verification steps\n"
            "- Implementation details unless critical for explaining the fix\n"
            "- Anything not directly related to fixing the bug\n"
            "- Summary sections or overview text\n"
            "- Any form of bug report summaries\n"
            "- Partial file paths or standalone filenames\n\n"
            "Keep the plan strictly focused on what needs to be fixed.\n"
            f"REMINDER: ALL file paths MUST start from project root: {self.repo.get_repo_path()}"
        )

        file_attachments = file_attachments or []
        focused_files = focused_files or []
        
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            error_prompt += f"\nUser has attached files for reference: {all_attachment_file_contents}"

        if all_focused_files_contents:
            error_prompt += f"\nFocused files requiring special attention: {all_focused_files_contents}"

        self.conversation_history.append({"role": "user", "content": error_prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"BugPlanner: Failed to get bug fix suggestion: {e}")
            return f"Error: {str(e)}"

    async def get_bugFixed_suggest_requests(self, bug_logs, files, overview, file_attachments=None, focused_files=None):
        """Get bug fix suggestions for multiple files."""
        filtered_lists = [file for file in files if file]

        logger.debug("BugPlanner: Initiating file scan for bug analysis")

        all_file_contents = ""

        for file_path in filtered_lists:
            try:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {os.path.relpath(file_path)}\n{file_content}"
            except Exception as e:
                all_file_contents += f"\n\nBugPlanner: Failed to read file {file_path}: {str(e)}"

        plan = await self.get_bugFixed_suggest_request(bug_logs, all_file_contents, overview, file_attachments, focused_files)
        return plan