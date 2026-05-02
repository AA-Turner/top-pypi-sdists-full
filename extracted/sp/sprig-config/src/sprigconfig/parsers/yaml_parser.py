import yaml

class YamlParser:
    def parse(self, text: str):
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise ValueError(str(e))
