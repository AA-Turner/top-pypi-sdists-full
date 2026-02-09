from prompt_toolkit.completion import WordCompleter

from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.utils_job_results import show_last_results

class ShowJobResults(Command):
    COMMAND = 'show job result'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowJobResults, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowJobResults.COMMAND

    def aliases(self):
        return [':?']

    def run(self, cmd: str, state: ReplState):
        if not (args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            show_last_results(state, args, ctx=self.context())

            return state

    def completion(self, state: ReplState):
        def job_completer():
            job_ids = list(reversed(sorted(Job.commands().keys())))
            meta_dict = {}
            for job_id, command in Job.commands().items():
                if command and (command := command.command):
                    if command.startswith('pg '):
                        command = command[3:]
                    elif command.startswith('cql '):
                        command = command[4:]
                    elif command.startswith('audit ') and command.strip(' ') != 'audit':
                        command = command[6:]

                    meta_dict[job_id] = command
            return WordCompleter(job_ids, meta_dict=meta_dict)

        return super().completion(state, job_completer())

    def help(self, state: ReplState):
        return super().help(state, 'show results of last background job', args='[job_id]')