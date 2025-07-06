"""Module providing local_test functionality."""

import os
import subprocess


class LocalTest:
    """
    A class to manage the execution of model-related scripts such as training, evaluation,
    deployment, and export based on configuration files.

    This class is designed to be part of a package, allowing users to create an instance
    and execute desired actions without modifying the package code.

    Example Usage:
        ```python
        from your_package_name import LocalTest

        # Define the path to the configuration directory
        config_directory = "/path/to/models_configs"

        # Create an instance of LocalTest
        local_test = LocalTest(config_directory)

        # Define the model info file and the actions to perform
        model_info = "model_A_info.json"
        actions_to_run = ["train", "eval", "export"]

        # Execute the specified actions for the selected model
        local_test.execute(
            model_info_path=os.path.join(config_directory, model_info),
            actions=actions_to_run
        )

        # To execute all actions for all models in the configuration directory:
        # local_test.execute_all()

        ```
    """

    def __init__(self, repo_configs_and_info_folder_path):
        """
        Initializes the LocalTest class with the path to the configuration files.

        Parameters:
            repo_configs_and_info_folder_path (str):
                Path to the directory containing model family, model info, and
                configuration JSON files.

        Example:
            ```python
            config_directory = "/path/to/models_configs"
            local_test = LocalTest(config_directory)
            ```
        """
        self.repo_configs_and_info_folder_path = repo_configs_and_info_folder_path

    def run_script(
        self,
        python_script,
        family_info_path,
        model_info_path,
        config_path,
    ):
        """
        Executes a specified Python script with the given model family and model info paths.

        Parameters:
            python_script (str):
                Name of the Python script to execute (e.g., "train.py", "eval.py",
                "deploy.py", "export.py").
            family_info_path (str):
                Path to the JSON file containing model family information.
            model_info_path (str):
                Path to the JSON file containing model-specific information.
            config_path (str):
                Path to the configuration file relevant to the script.

        Example:
            ```python
            local_test.run_script(
                python_script="train.py",
                family_info_path="/path/to/family_info.json",
                model_info_path="/path/to/model_A_info.json",
                config_path="/path/to/train-config.json"
            )
            ```

        Raises:
            subprocess.CalledProcessError: If the subprocess call fails.
        """
        if "deploy" not in python_script:
            command = [
                "python",
                python_script,
                "Testing",
                family_info_path,
                model_info_path,
                config_path,
            ]
        else:
            local_port = 8000
            command = [
                "python",
                python_script,
                "Testing",
                str(local_port),
                family_info_path,
                model_info_path,
                config_path,
            ]
        try:
            print(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)
            print(f"Successfully executed {python_script} with config {config_path}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command {' '.join(command)}. Error: {e}\n")

    def execute(self, model_info_path, actions):
        """
        Executes specified actions (train, eval, deploy, export) for a given model.

        The method locates the necessary configuration files within the repository
        configuration directory and runs the corresponding scripts.

        Parameters:
            model_info_path (str):
                Path to the JSON file containing model-specific information.
            actions (list of str):
                List of actions to perform. Valid actions are 'train', 'eval',
                'deploy', and 'export'.

        Example:
            ```python
            local_test.execute(
                model_info_path="/path/to/model_A_info.json",
                actions=["train", "eval", "export"]
            )
            ```

        Raises:
            ValueError: If an invalid action is specified.
            FileNotFoundError: If essential configuration files are missing.
        """
        valid_actions = {
            "train",
            "eval",
            "deploy",
            "export",
        }
        if not set(actions).issubset(valid_actions):
            invalid = set(actions) - valid_actions
            raise ValueError(f"Invalid actions specified: {invalid}")
        family_info_path = os.path.join(
            self.repo_configs_and_info_folder_path,
            "family_info.json",
        )
        if not os.path.isfile(family_info_path):
            raise FileNotFoundError(
                f"family_info.json not found in {self.repo_configs_and_info_folder_path}"
            )
        action_mapping = {
            "train": {
                "script": "train.py",
                "config": "train-config.json",
            },
            "eval": {
                "script": "eval.py",
                "config": "eval-config.json",
            },
            "deploy": {
                "script": "deploy.py",
                "config": "deploy-config.json",
            },
            "export": {
                "script": "export.py",
                "config_prefix": "export-",
            },
        }
        for action in actions:
            if action in {
                "train",
                "eval",
                "deploy",
            }:
                script = action_mapping[action]["script"]
                config_filename = action_mapping[action]["config"]
                config_path = os.path.join(
                    self.repo_configs_and_info_folder_path,
                    config_filename,
                )
                if not os.path.isfile(config_path):
                    print(
                        f"Configuration file {config_path} for action '{action}' not found. Skipping."
                    )
                    continue
                self.run_script(
                    python_script=script,
                    family_info_path=family_info_path,
                    model_info_path=model_info_path,
                    config_path=config_path,
                )
            elif action == "export":
                export_configs = [
                    f
                    for f in os.listdir(self.repo_configs_and_info_folder_path)
                    if f.startswith(action_mapping[action]["config_prefix"])
                    and f.endswith(".json")
                ]
                if not export_configs:
                    print("No export configuration files found. Skipping 'export' action.\n")
                    continue
                for export_config in export_configs:
                    export_config_path = os.path.join(
                        self.repo_configs_and_info_folder_path,
                        export_config,
                    )
                    self.run_script(
                        python_script=action_mapping[action]["script"],
                        family_info_path=family_info_path,
                        model_info_path=model_info_path,
                        config_path=export_config_path,
                    )

    def execute_all(self):
        """
        Executes all standard actions (train, eval, deploy, export) for all models
        found in the configuration directory.

        This method automatically detects all model info files and executes all
        actions using the default configuration files.

        Example:
            ```python
            local_test.execute_all()
            ```

        Raises:
            FileNotFoundError: If essential configuration files are missing.
        """
        models_info_paths = []
        export_config_files = []
        family_info_path = os.path.join(
            self.repo_configs_and_info_folder_path,
            "family_info.json",
        )
        if not os.path.isfile(family_info_path):
            raise FileNotFoundError(
                f"family_info.json not found in {self.repo_configs_and_info_folder_path}"
            )
        for filename in os.listdir(self.repo_configs_and_info_folder_path):
            file_path = os.path.join(
                self.repo_configs_and_info_folder_path,
                filename,
            )
            if not filename.endswith(".json"):
                continue
            if filename in {
                "family_info.json",
                "train-config.json",
                "eval-config.json",
                "deploy-config.json",
            }:
                continue
            if filename.startswith("export-"):
                export_config_files.append(file_path)
            else:
                models_info_paths.append(file_path)
        for model_info_path in models_info_paths:
            print(f"Processing model info: {model_info_path}")
            self.execute(
                model_info_path=model_info_path,
                actions=[
                    "train",
                    "eval",
                    "deploy",
                    "export",
                ],
            )
