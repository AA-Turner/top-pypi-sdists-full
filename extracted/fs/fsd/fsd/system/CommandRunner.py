import subprocess
import os
import sys
import psutil
import threading
import json
from log.logger_config import get_logger
from .FileContentManager import FileContentManager
from .ConfigAgent import ConfigAgent
from .TaskErrorPlanner import TaskErrorPlanner
import time
import signal
from typing import Tuple, List
from pathlib import Path
import os
import platform
logger = get_logger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import parse_payload

class CommandRunner:
    def __init__(self, repo):
        """
        Initializes the CommandRunner.
        """
        self.repo = repo
        self.config = ConfigAgent(repo)
        self.errorPlanner = TaskErrorPlanner(repo)
        self.config_manager = FileContentManager(repo)  # Initialize CodeManager in the constructor
        self.directory_path = repo.get_repo_path()
        self.max_retry_attempts = 3  # Set a maximum number of retry attempts

    async def get_config_requests(self, instructions, file_name):
        """Generate coding requests based on instructions and context."""

        main_path = file_name
        logger.debug(f" #### `SnowX` is initiating the processing of file: {file_name} in {main_path}")
        logger.info(f" #### `SnowX` has been assigned the following task: {instructions}")
        result = await self.config.get_config_requests(instructions, main_path)
        if main_path:
            await self.config_manager.handle_coding_agent_response(main_path, result)
            logger.info(f" #### `SnowX` has successfully completed its work on {file_name}")
        else:
            logger.debug(f" #### `SnowX` encountered an issue: Unable to locate the file: {file_name}")

    async def get_error_planner_requests(self, error, config_context, os_architecture, compile_files):
        """Generate coding requests based on instructions and context."""
        result = await self.errorPlanner.get_task_plans(error, config_context, os_architecture, compile_files)
        return result

    def run_command(self, command: str, is_localhost_command: str, method: str = 'bash', inactivity_timeout: int = 7, use_timeout: bool = True) -> Tuple[int, List[str]]:
        """
        Runs a given command using the specified method.
        Shows real-time output during execution within a Bash markdown block.
        Returns a tuple of (return_code, all_output).
        Implements an optional inactivity timeout to determine command completion.
        
        Parameters:
        - command (str): The shell command to execute.
        - method (str): The shell method to use (default is 'bash').
        - inactivity_timeout (int): Seconds to wait for new output before considering done.
        - use_timeout (bool): Whether to enforce the inactivity timeout.
        """
        # Give more time for install commands and package managers
        if is_localhost_command == "0" and any(cmd_keyword in command for cmd_keyword in ['install', 'update', 'upgrade']):
            inactivity_timeout = 120  # 2 minutes for installation commands
        elif is_localhost_command == "1":
            inactivity_timeout = 7
        else:
            inactivity_timeout = 5
    
        markdown_block_open = False  # Flag to track if markdown block is open
        process = None  # Initialize process variable
        terminated_by_timeout = False  # Flag to track if process was terminated by timeout

        try:
            # Set shell and executable based on platform
            shell = True
            if platform.system() == 'Windows':
                executable = None  # Use default cmd.exe on Windows
            else:
                executable = '/bin/bash'

            # Check if the command is a 'cd' command
            if command.startswith('cd '):
                # Extract directory path and handle both quoted and unquoted paths
                new_dir = command[3:].strip().strip("'\"")  # Strip both spaces and quotes
                
                try:
                    os.chdir(new_dir)
                    logger.info(
                        f"#### Directory Change\n"
                        f"```bash\nChanged directory to: {new_dir}\n```\n"
                        f"----------------------------------------"
                    )
                    return 0, [f"Changed directory to: {new_dir}"]
                except Exception as e:
                    error_msg = f"Failed to change directory: {str(e)}"
                    logger.error(error_msg)
                    return 1, [error_msg]

            # Log the current working directory and the command to be executed
            current_path = os.getcwd()
            logger.info(
                f"#### Executing Command\n"
                f"```bash\n{command}\n```\n"
                f"**In Directory:** `{current_path}`\n"
                f"#### Command Output\n```bash"
            )
            markdown_block_open = True  # Code block is now open

            # Convert Unix-style commands to Windows if needed
            if platform.system() == 'Windows':
                # Convert forward slashes to backslashes
                command = command.replace('/', '\\')
                # Handle common Unix commands
                command = command.replace('clear', 'cls')
                command = command.replace('rm -rf', 'rmdir /s /q')
                command = command.replace('rm', 'del')
                command = command.replace('cp', 'copy')
                command = command.replace('mv', 'move')
                command = command.replace('ls', 'dir')
                command = command.replace('mkdir -p', 'mkdir')
                command = command.replace('touch', 'type nul >')

            # Start the process with platform-specific settings
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == 'Windows' else 0
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=current_path,
                creationflags=creation_flags
            )

            # Use psutil to handle process and its children
            parent = psutil.Process(process.pid)

            # Initialize output list
            output = []

            # Variable to track the last time output was received
            last_output_time = time.time()

            # Lock for thread-safe updates to last_output_time
            lock = threading.Lock()

            # Function to read output
            def read_output(stream, output_list):
                nonlocal markdown_block_open, last_output_time
                for line in iter(stream.readline, ''):
                    line = line.rstrip()
                    output_list.append(line)
                    logger.info(line)
                    with lock:
                        last_output_time = time.time()
                stream.close()

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_output, args=(process.stdout, output))
            stderr_thread = threading.Thread(target=read_output, args=(process.stderr, output))
            stdout_thread.start()
            stderr_thread.start()

            # Monitoring loop
            while True:
                if process.poll() is not None:
                    # Process has finished
                    break
                if use_timeout:
                    with lock:
                        time_since_last_output = time.time() - last_output_time
                    if time_since_last_output > inactivity_timeout:
                        # No output received within the inactivity timeout
                        logger.info(f"No output received for {inactivity_timeout} seconds. Assuming command completion.")
                        terminated_by_timeout = True
                        break
                time.sleep(0.1)  # Prevent busy waiting

            # If the process is still running, attempt to terminate it gracefully
            if process.poll() is None:
                try:
                    logger.info(f"Attempting to terminate the subprocess after inactivity timeout of {inactivity_timeout} seconds.")
                    if platform.system() == 'Windows':
                        process.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        process.terminate()

                    try:
                        process.wait(timeout=5)
                        logger.info("Subprocess terminated gracefully.")
                        terminated_by_timeout = True
                    except subprocess.TimeoutExpired:
                        logger.info("Subprocess did not terminate in time; killing it.")
                        process.kill()
                        terminated_by_timeout = True

                except Exception as e:
                    logger.error(f"Error terminating the subprocess: {e}")

            # Wait for threads to finish reading
            stdout_thread.join()
            stderr_thread.join()

            # Close the markdown code block if it's open
            if markdown_block_open:
                logger.info("```")  # Close the markdown block
                markdown_block_open = False

            return_code = process.returncode
            # If process was terminated by timeout, return success code
            if terminated_by_timeout:
                return_code = 0
                
            logger.info(
                f"#### Command Finished.\n"
                f"----------------------------------------"
            )
            logger.info("`SnowX` has completed the current step and is proceeding to the next one.")
            return return_code, output

        except Exception as e:
            logger.error(f"An error occurred while running the command: {e}")
            # Ensure that the subprocess is terminated in case of an exception
            if process and process.poll() is None:
                try:
                    logger.info("Attempting to terminate the subprocess due to an exception.")
                    if platform.system() == 'Windows':
                        process.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.info("Subprocess did not terminate in time; killing it.")
                        process.kill()
                except Exception as terminate_error:
                    logger.error(f"Failed to terminate subprocess after exception: {terminate_error}")
            return -1, [f"An error occurred: {e}"]

    def update_file(self, file_name, content):
        """
        Updates the content of a file.
        """
        try:
            with open(file_name, 'a') as file:
                file.write(content + '\n')
            logger.info(f" #### `SnowX` has successfully updated the file: {file_name}")
            return f"Successfully updated {file_name}"
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error while attempting to update {file_name}: {str(e)}")
            return f"Failed to update {file_name}: {str(e)}"
        
    def open_terminal(self, bash_commands):
        """
        Opens a terminal window, navigates to the project path, and runs the specified bash commands.
        Cross-platform implementation for Windows, macOS, and Linux.

        Parameters:
            bash_commands (list): List of bash commands to execute in the terminal.
        """
        # Join commands with semicolon for Windows, && for others
        if platform.system() == 'Windows':
            bash_command = "; ".join(bash_commands)
        else:
            bash_command = " && ".join(bash_commands)

        # Retrieve the project path
        project_path = self.repo.get_repo_path()
        logger.info(f"#### Project Path: `{project_path}`")
        logger.info(f" #### Bash Commands: `{bash_command}`")

        # Ensure the project path exists
        if not Path(project_path).exists():
            logger.error(f"The project path does not exist: {project_path}")
            raise FileNotFoundError(f"The project path does not exist: {project_path}")

        # Detect the operating system
        current_os = platform.system()
        logger.info(f" #### Operating System Detected: {current_os}")

        try:
            if current_os == 'Windows':
                # For Windows, use PowerShell with semicolons
                # Convert forward slashes to backslashes for Windows paths
                project_path = project_path.replace('/', '\\')
                # Use semicolons and wrap each command in curly braces for PowerShell
                ps_commands = "; ".join([f"{{{cmd}}}" for cmd in bash_commands])
                cmd = f'start powershell.exe -NoExit -Command "Set-Location \'{project_path}\'; {ps_commands}"'
                subprocess.Popen(cmd, shell=True)
                logger.info("#### `PowerShell` opened successfully.")
            elif current_os == 'Darwin':  # macOS
                # For macOS, use Terminal.app
                apple_script = f'''
                tell application "Terminal"
                    activate
                    do script "cd \\"{project_path}\\"; {bash_command}"
                end tell
                '''
                subprocess.Popen(['osascript', '-e', apple_script])
                logger.info("#### `Terminal.app` opened successfully.")
            elif current_os == 'Linux':
                # For Linux, try to detect the default terminal
                terminals = ['gnome-terminal', 'xterm', 'konsole', 'terminator']
                terminal_found = False
                
                for terminal in terminals:
                    try:
                        if subprocess.run(['which', terminal], capture_output=True).returncode == 0:
                            if terminal == 'gnome-terminal':
                                subprocess.Popen([terminal, '--', 'bash', '-c', f'cd "{project_path}" && {bash_command}; exec bash'])
                            else:
                                subprocess.Popen([terminal, '-e', f'bash -c \'cd "{project_path}" && {bash_command}; exec bash\''])
                            logger.info(f"#### `{terminal}` opened successfully.")
                            terminal_found = True
                            break
                    except Exception:
                        continue
                
                if not terminal_found:
                    logger.error("No suitable terminal emulator found on Linux system")
                    raise EnvironmentError("No suitable terminal emulator found")
            else:
                logger.error(f"Unsupported Operating System: {current_os}")
                raise NotImplementedError(f"OS '{current_os}' is not supported.")
                
        except Exception as e:
            logger.exception(f"Failed to open terminal: {e}")
            raise

    async def execute_steps(self, steps_json, compile_files):
        """
        Executes a series of steps provided in JSON format.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']
        bash_commands = []

        for step in steps:
            is_localhost_command = step.get('is_localhost_command', "0")
            if step['method'] == 'bash':
                logger.info(f"#### `Command Runner`: {step['prompt']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f"#### `Command Runner`:")
                logger.info(f"```yaml\n{step['prompt']}\n```")


            if step['method'] == 'bash' and (step['command'].strip().startswith('sudo ') or step['command'].strip().lower().startswith('runas ')):
                logger.info(
                    f"#### `SnowX` detected a command requiring elevated privileges: `{step['command']}`\n"
                    "This command requires your permission and password to execute.\n" 
                    "We will open your terminal to run this command securely.\n"
                    "After entering your password and completing the command, please return here to continue with the next steps."
                )
                logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                user_run = input()

                user_select_run, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                user_select_run = user_select_run.lower()
                if user_select_run == 'a':
                    self.open_terminal(list(step['command']))
            else:
                if step['method'] == 'bash' and (step['command'].strip().startswith('sudo ') or step['command'].strip().lower().startswith('runas ')):
                    logger.info(
                        f"#### `SnowX` detected a command requiring elevated privileges: `{step['command']}`\n"
                        "This command requires your permission and password to execute.\n" 
                        "We will open your terminal to run this command securely.\n"
                        "After entering your password and completing the command, please return here to continue with the next steps."
                    )
                    logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                    user_run = input()

                    user_select_run, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                    user_select_run = user_select_run.lower()
                    if user_select_run == 'a':
                        self.open_terminal(list(step['command']))
                else:
                    logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                    user_permission = input()

                    user_prompt, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
                    user_prompt = user_prompt.lower()

                    if user_prompt == 'exit':
                        logger.info(" #### The user has chosen to exit. `SnowX` is halting execution.")
                        return "Execution stopped by user"
                    elif user_prompt == 's':
                        logger.info(" #### The user has chosen to skip this step.")
                        continue

                    logger.info(f" #### `SnowX` is now executing the following step: {step['prompt']}")

                    retry_count = 0
                    while retry_count < self.max_retry_attempts:
                        if step['method'] == 'bash':
                            # Run the command and get the return code and output
                            # Check if command is a cd command and handle spaces in path
                            if step['command'].startswith('cd '):
                                path = step['command'][3:].strip()
                                if ' ' in path:
                                    step['command'] = f'cd "{path}"'

                            return_code, command_output = self.run_command(step['command'], is_localhost_command)

                            # Check for errors based on the return code
                            if return_code != 0 and return_code != None:
                                error_message = ','.join(command_output)
                                logger.error(f"  `SnowX` reports: Command execution failed with return code {return_code}: {error_message}")
                                
                                # Check if the error suggests an alternative command
                                if "Did you mean" in error_message:
                                    suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                                    logger.info(f" #### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                                    logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                                    user_choice = input()

                                    user_select, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                                    user_select = user_select.lower()
                                    
                                    if user_select == 'a':
                                        logger.info(f" #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                        return_code, command_output = self.run_command(suggested_command, is_localhost_command)
                                        if return_code == 0 or return_code == None:
                                            if is_localhost_command == "1" or is_localhost_command == 1:
                                                logger.info(
                                                    f"#### `SnowX` believes this is localhost `{suggested_command}`. "
                                                    "It has run successfully, so there is potentially no error. "
                                                    "However, I have already shut it down. We can open it separately in your terminal."
                                                )
                                                logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                                                user_run = input()

                                                user_select_run, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                                                user_select_run = user_select_run.lower()
                                                if user_select_run == 'a':
                                                    bash_commands.append(suggested_command)
                                                    self.open_terminal(bash_commands)
                                                break
                                            else:
                                                bash_commands.append(step['command'])
                                                break  # Command executed successfully
                                        else:
                                            # Update error_message with new command output
                                            error_message = ','.join(command_output)
                                            logger.error(
                                                f"#### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                                    elif user_select == 'exit':
                                        logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                        return "Execution stopped by user"
                                    else:
                                        logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")
                                
                                # Proceed to handle the error
                                fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.repo.return_os(), compile_files)
                                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files)
                                if fixing_result == "Execution stopped by user":
                                    logger.info(" #### The user has chosen to exit during the fixing steps. `SnowX` is skipping the current step.")
                                    break
                                elif fixing_result == "All fixing steps completed successfully":
                                    logger.info(" #### `SnowX` has fixed the issues. Moving to the next step.")
                                    continue  # Skip reporting failure and move to the next step
                                retry_count += 1
                            else:
                                if is_localhost_command == "1" or is_localhost_command == 1:
                                    logger.info(
                                        f"#### `SnowX` believes this is localhost `{step['command']}`. "
                                        "It has run successfully, so there is potentially no error. "
                                        "However, I have already shut it down. We can open it separately in your terminal."
                                    )
                                    logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                                    user_run = input()

                                    user_select_run, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                                    user_select_run = user_select_run.lower()
                                    if user_select_run == 'a':
                                        bash_commands.append(step['command'])
                                        self.open_terminal(bash_commands)
                                    break
                                else:
                                    bash_commands.append(step['command'])
                                    break
                        elif step['method'] == 'update':
                            file_name = step.get('file_name', '')
                            if file_name != 'N/A':
                                await self.get_config_requests(step['prompt'], file_name)
                                logger.info(f" #### `SnowX` has successfully updated the file: {file_name}")
                            else:
                                logger.debug("\n #### `SnowX` reports: Update method specified but no file name provided.")
                            break
                        else:
                            logger.error(f"  `SnowX` encountered an unknown method: {step['method']}")
                            break

                    if retry_count == self.max_retry_attempts:
                        logger.error(f"  `SnowX` reports: Step failed after {self.max_retry_attempts} attempts: {step['prompt']}")
                        error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"
                        fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.repo.return_os(), compile_files)
                        fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files)
                        if fixing_result == "Execution stopped by user":
                            logger.info(" #### The user has chosen to exit during the fixing steps. `SnowX` is skipping the current step.")
                            continue
                        elif fixing_result == "All fixing steps completed successfully":
                            logger.info(" #### `SnowX` has fixed the issues. Moving to the next step.")
                            continue  # Skip reporting failure and move to the next step
                        return f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"

                    logger.info(" #### `SnowX` has completed the current step and is proceeding to the next one.")

        logger.info(" #### `SnowX` has successfully completed all steps")
        return "All steps completed successfully"

    async def execute_fixing_steps(self, steps_json, compile_files):
        """
        Executes a series of steps provided in JSON format to fix dependency issues.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:

            if step['method'] == 'bash':
                logger.info(f" #### `Command Runner`: {step['error_resolution']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f" #### `Command Runner`:")
                logger.info(f"```yaml\n{step['error_resolution']}\n```")
           
            logger.info("")

            if step['method'] == 'bash' and (step['command'].strip().startswith('sudo ') or step['command'].strip().lower().startswith('runas ')):
                logger.info(
                    f"#### `SnowX` detected a command requiring elevated privileges: `{step['command']}`\n"
                    "This command requires your permission and password to execute.\n" 
                    "We will open your terminal to run this command securely.\n"
                    "After entering your password and completing the command, please return here to continue with the next steps."
                )
                logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                user_run = input()

                user_select_run, _, _, _ = parse_payload(self.repo.get_repo_path(), user_run)
                user_select_run = user_select_run.lower()
                if user_select_run == 'a':
                    self.open_terminal(list(step['command']))
            else:
                logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                user_permission = input()

                user_prompt, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
                user_prompt = user_prompt.lower()

                if user_prompt == 'exit':
                    logger.info(" #### The user has chosen to exit. `SnowX` is halting execution.")
                    return "Execution stopped by user"
                elif user_prompt == 's':
                    logger.info(" #### The user has chosen to skip this step.")
                    continue

                logger.info(f" #### `SnowX` is now executing the following fixing step: {step['error_resolution']}")

                retry_count = 0
                while retry_count < self.max_retry_attempts:
                    if step['method'] == 'bash':
                        # Run the command and get the return code and output
                        return_code, command_output = self.run_command(step['command'], "0")
                        
                        # Check for errors based on the return code
                        if return_code != 0:
                            error_message = ','.join(command_output)
                            logger.error(f"  `SnowX` reports: Command execution failed with return code {return_code}: {error_message}")

                            # Check if the error suggests an alternative command
                            if "Did you mean" in error_message:
                                suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                                logger.info(f" #### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                                logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                                user_choice = input()

                                user_select, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                                user_select = user_select.lower()
                                
                                if user_select == 'a':
                                    logger.info(f" #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                    return_code, command_output = self.run_command(suggested_command, "0") 
                                    if return_code == 0:
                                        break  # Command executed successfully
                                    else:
                                        # Update error_message with new command output
                                        error_message = ','.join(command_output)
                                        logger.error(
                                            f"\n #### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                                elif user_select == 'exit':
                                    logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                    return "Execution stopped by user"
                                else:
                                    logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")
                            
                            # Proceed to handle the error
                            fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files)
                            fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files)
                            if fixing_result == "Execution stopped by user":
                                return "Execution stopped by user"
                            elif fixing_result == "All fixing steps completed successfully":
                                logger.info(" #### `SnowX` has fixed the issues. Moving to the next step.")
                                continue  # Skip reporting failure and move to the next step
                            retry_count += 1
                        else:
                            break  # Command executed successfully without errors
                    elif step['method'] == 'update':
                        file_name = step.get('file_name', '')
                        if file_name != 'N/A':
                            await self.get_config_requests(step['error_resolution'], file_name)
                            logger.info(f" #### `SnowX` has successfully updated the file: {file_name}")
                        else:
                            logger.debug("\n #### `SnowX` reports: Update method specified but no file name provided.")
                        break
                    else:
                        logger.error(f"  `SnowX` encountered an unknown method: {step['method']}")
                        break

                if retry_count == self.max_retry_attempts:
                    logger.error(f"  `SnowX` reports: Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}")
                    error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"
                    fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.repo.return_os(), compile_files)
                    fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files)
                    if fixing_result == "Execution stopped by user":
                        return "Execution stopped by user"
                    elif fixing_result == "All fixing steps completed successfully":
                        logger.info(" #### `SnowX` has fixed the issues. Moving to the next step.")
                        continue  # Skip reporting failure and move to the next step
                    return f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"

                logger.info(" #### `SnowX` has completed the current fixing step and is proceeding to the next one.")

        logger.info(" #### `SnowX` has successfully completed all fixing steps")
        return "All fixing steps completed successfully"