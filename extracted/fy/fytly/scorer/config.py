import configparser
import importlib.resources

class GraderConfigs:
    def __init__(self):
        self.props = self._load_configs()

    def _load_configs(self, keywords_file='app.properties'):
        config = configparser.ConfigParser()
        props = {}

        try:
            with importlib.resources.open_text('scorer.configs', keywords_file) as f:
                config.read_string('[config]\n' + f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"{keywords_file} not found in scorer/configs.")

        for k, v in config['config'].items():
            props[k] = v
        return props
