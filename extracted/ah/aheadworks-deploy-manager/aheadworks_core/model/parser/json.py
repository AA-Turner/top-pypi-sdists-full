import json


class Json:

    def __init__(self):
        self.composer_by_path = {}

    def get_variable_from_file(self, var_name, file):
        if file in self.composer_by_path:
            composer = self.composer_by_path[file]
        else:
            with open(file) as f:
                composer = json.load(f)
            self.composer_by_path[file] = composer

        if var_name in composer:
            var_value = composer[var_name]
        else:
            raise Exception('Var name not found.')

        return var_value
