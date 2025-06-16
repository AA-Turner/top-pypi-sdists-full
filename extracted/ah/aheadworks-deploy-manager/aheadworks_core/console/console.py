from aheadworks_core.model.parser.json import Json as JsonParser


class Console:
    """
    this application needed next env variables
    """

    def __init__(self):
        self.json_parser = JsonParser()

    # Parser
    # first level only. todo improve
    def get_variable_from_json_file(self, var_name, file):
        try:
            print(self.json_parser.get_variable_from_file(var_name, file))
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            exit_code = 1

        exit(exit_code)
