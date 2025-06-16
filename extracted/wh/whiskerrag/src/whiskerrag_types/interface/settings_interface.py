from abc import ABC, abstractmethod


class SettingsInterface(ABC):
    WEB_URL: str
    KNOWLEDGE_TABLE_NAME: str
    CHUNK_TABLE_NAME: str
    TASK_TABLE_NAME: str
    ACTION_TABLE_NAME: str
    TENANT_TABLE_NAME: str
    SPACE_TABLE_NAME: str
    API_KEY_TABLE_NAME: str
    LOG_DIR: str
    PLUGIN_ENV = dict

    @abstractmethod
    def load_plugin_dir_env(self, plugin_env_path: str) -> dict:
        pass

    @abstractmethod
    def get_env(self, name: str, defaultValue: str) -> None:
        pass
