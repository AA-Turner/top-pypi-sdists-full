import yaml

class PodExecResult:
    # {
    #   'metadata': {},
    #   'status': 'Failure',
    #   'message': 'command terminated with non-zero exit code: error executing command [/bin/sh -c cqlsh -u cs-9834d85c68-superuser -p 07uV-5ogoDro9e7NDXvN  -e "select name"], exit code 2',
    #   'reason': 'NonZeroExitCode',
    #   'details': {
    #     'causes': [
    #       {
    #         'reason': 'ExitCode',
    #         'message': '2'
    #       }
    #     ]
    #   }
    # }
    def __init__(self, stdout: str, stderr: str, command: str = None, error_output: str = None):
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.command: str = command
        if error_output:
            self.error = yaml.safe_load(error_output)

    def exit_code(self) -> int:
        code = 0

        try:
            code = self.error['details']['causes'][0]['message']
        except:
            pass

        return code