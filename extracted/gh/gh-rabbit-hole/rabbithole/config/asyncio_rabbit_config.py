import json
from rabbithole.config import ConfigFileManager

DEFAULT_CONFIG = {
    "amqp_url": "amqp://guest:guest@localhost:5672/",
    "sending_queue": "my_sending_queue",
    "listening_queue": "my_listening_queue",
    "sending_exchange": "my_exchange",
    "reconnect_delay": 5,
    "max_reconnect_attempts": 3,
}

REQUIRED_KEYS = [
    {"key": "amqp_url", "type": str},
    {"key": "sending_queue", "type": str},
    {"key": "listening_queue", "type": str},
    {"key": "sending_exchange", "type": str},
    {"key": "reconnect_delay", "type": int},
    {"key": "max_reconnect_attempts", "type": int},
]


class RabbitConfig:
    """
    RabbitConfig manages the configuration settings for RabbitMQ connections and interactions.
    It ensures that all required configuration settings are present and correctly typed,
    and provides methods to load, validate, update, and save the configuration.
    
    Attributes:
        config_file_manager (ConfigFileManager): Manages the loading and saving of the config file.
        config (dict): A dictionary containing the current configuration settings.
    """
    def __init__(
        self,
        config_file_manager: ConfigFileManager = ConfigFileManager(
            "app_config", "config.json"
        ),
        required_keys: list = REQUIRED_KEYS,
        default_config: dict = DEFAULT_CONFIG,
    ):
        """
        Initializes a new instance of the RabbitConfig class.

        Args:
            config_file_manager (ConfigFileManager): The manager responsible for loading and saving configuration files.
            required_keys (list): A list of required keys and their types that the configuration should contain.
            default_config (dict): The default configuration to use if no user-provided configuration is found.
        """
        self.config_file_manager = config_file_manager
        self._default_config = default_config
        self.__required_keys = required_keys
        self.config: dict = self.load_or_initialize_config()

    def load_or_initialize_config(self):
        """
        Loads the configuration from a file using the ConfigFileManager. If the file does not exist or is empty,
        initializes the configuration with the default settings and saves it.

        Returns:
            dict: The loaded or initialized configuration.
        """
        config = self.config_file_manager.load()
        if config is None:  # Se il file di configurazione non esiste o è vuoto
            config = self._default_config
            config_to_save = self.__check_config(config)
            self.config_file_manager.save(
                config_to_save
            )  # Crea un file di configurazione di default
            return config_to_save
        else:
            return self.__check_config(config)

    def __check_config(self, config):
        """
        Checks if the provided configuration contains all required keys with the correct types.
        Fills in missing keys with default values if necessary.

        Args:
            config (dict): The configuration dictionary to validate.

        Returns:
            dict: The validated and possibly augmented configuration.

        Raises:
            ValueError: If a required key is missing or a value has the wrong type.
        """        
        default = self._default_config

        for required in self.__required_keys:
            key, required_type = required["key"], required["type"]

            # Verifica la presenza della chiave
            if key not in config:
                if key in default:
                    config[key] = default[key]
                else:
                    raise ValueError(
                        f"La chiave di configurazione obbligatoria '{key}' manca."
                    )

            # Verifica il tipo della chiave
            if not isinstance(config[key], required_type):
                raise ValueError(
                    f"La chiave '{key}' deve essere di tipo {required_type.__name__}"
                )

        return config

    def update_config(self, new_config):
        """
        Updates the current configuration with new settings and saves the updated configuration.

        Args:
            new_config (dict): A dictionary containing the new configuration settings.
        """
        validated_config = self.__check_config(new_config)
        if validated_config is None:
            return
        for key, value in validated_config.items():
            if key in self.config:
                self.config[key] = value

        self.config_file_manager.save(self.config)

    def get_config(self):
        """
        Retrieves the current configuration settings.

        Returns:
            dict: The current configuration settings.
        """
        return self.config

    def save_config(self, save_path):
        """
        Saves the current configuration settings to a specified path.

        Args:
            save_path (str): The file path where the configuration should be saved.
        """
        save_config = self.config.copy()
        with open(save_path, "w") as config_file:
            json.dump(save_config, config_file, indent=4)
