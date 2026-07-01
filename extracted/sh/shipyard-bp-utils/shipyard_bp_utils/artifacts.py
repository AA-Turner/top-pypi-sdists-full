import os
import pickle
from shipyard_templates import ShipyardLogger

from . import files

logger = ShipyardLogger.get_logger()


class Artifact:
    class SubFolder:
        def __init__(self, path):
            self.path = path

        def read(self, filename, file_type):
            if file_type == "json":
                return self.read_json(filename)
            elif file_type == "pickle":
                return self.read_pickle(filename)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        def write(self, filename, file_type, data):
            if file_type == "json":
                return self.write_json(filename, data)
            elif file_type == "pickle":
                return self.create_pickle(filename, data)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        def create_pickle(self, filename, data):
            logger.debug(f"Creating pickle file: {filename}...")
            pickle_file_name = os.path.join(self.path, f"{filename}.pickle")
            with open(pickle_file_name, "wb") as f:
                pickle.dump(data, f)
            logger.debug("Pickle file created.")

        def write_json(self, filename, data):
            logger.debug(f"Writing JSON file: {filename}...")
            json_file_name = os.path.join(self.path, f"{filename}.json")
            files.write_json_to_file(data, json_file_name)
            logger.debug("JSON file written.")

        def read_pickle(self, filename):
            logger.debug(f"Reading pickle file: {filename}...")
            pickle_file_name = os.path.join(self.path, f"{filename}.pickle")
            with open(pickle_file_name, "rb") as f:
                data = pickle.load(f)
            logger.debug(f"Pickle file read. Data: {data}")
            return data

        def read_json(self, filename):
            logger.debug(f"Reading JSON file: {filename}...")
            json_file_name = os.path.join(self.path, f"{filename}.json")
            data = files.read_json_file(json_file_name)
            logger.debug(f"JSON file read. Data: {data}")
            return data

    def __init__(self, vendor):
        self.vendor = vendor
        self.base_folder = self.determine_base_artifact_folder()
        self.variables = self.SubFolder(self.create_folder("variables"))
        self.responses = self.SubFolder(self.create_folder("responses"))
        self.logs = self.SubFolder(self.create_folder("logs"))

    def determine_base_artifact_folder(self):
        """
        Creates the base folder structure for storing artifacts.
        Uses USER to support local runs.
        """
        artifact_folder_default = f'{os.environ.get("USER")}-artifacts'
        base_folder = os.getenv("SHIPYARD_ARTIFACTS_DIRECTORY", artifact_folder_default)
        base_folder = os.path.join(base_folder, f"{self.vendor}-blueprints")

        return os.path.normpath(base_folder)

    def create_folder(self, folder_name):
        """
        Creates a folder  if it does not already exist.

        Args:
        folder_name (str): The name of the destination folder to be created.

        Returns: The path of the created folder.
        """
        logger.debug(f"Creating folder: {folder_name}...")
        folder_path = os.path.join(self.base_folder, folder_name)
        folder_path = os.path.normpath(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
