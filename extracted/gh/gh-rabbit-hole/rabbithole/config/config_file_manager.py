import json
import os


class ConfigFileManager:
    """
    A class responsible for managing the reading and writing of configuration files.

    Attributes:
        directory (str): The directory path where the configuration file is stored.
        filename (str): The name of the configuration file.
    """

    def __init__(self, directory, filename):
        """
        Initializes a new instance of the ConfigFileManager class.

        Args:
            directory (str): The directory path where the configuration file will be stored.
            filename (str): The name of the configuration file to manage.
        """
        self.directory = directory
        self.filename = filename
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """
        Ensures that the directory specified exists, creating it if necessary.
        """
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_full_path(self):
        """
        Gets the full file path of the configuration file.

        Returns:
            str: The full path combining the directory and filename.
        """
        return os.path.join(self.directory, self.filename)

    def load(self):
        """
        Loads the configuration from a file. If the file doesn't exist, returns None.

        Returns:
            dict or None: The configuration loaded from the file as a dictionary, or None if the file doesn't exist.
        """
        full_path = self.get_full_path()
        if not os.path.isfile(
            full_path
        ):  # Se il file non esiste, restituisci None o un valore di default
            return None  # Oppure potresti restituire self.default_config se ha senso per il tuo caso d'uso

        with open(full_path, "r") as file:
            return json.load(file)

    def save(self, config):
        """
        Saves the provided configuration to a file.

        Args:
            config (dict): The configuration to save.
        """
        with open(self.get_full_path(), "w") as file:
            json.dump(config, file, indent=4)
