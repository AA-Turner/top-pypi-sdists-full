from typing import Any, Dict
import yaml
import os

class components:
    
    def __init__(self):
        config_path = os.path.join(os.getcwd(), 'config.yaml')
        config = self.load_yaml_file(config_path)
        self.data = self.load_yaml_file(config)

        self.ASD = 'a'

    def load_yaml_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data