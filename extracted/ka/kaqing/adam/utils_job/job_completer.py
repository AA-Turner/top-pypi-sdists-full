from prompt_toolkit.completion import WordCompleter

from adam.utils_job.job import Job

def job_completer():
    job_ids = list(reversed(sorted(Job.jobs().keys())))
    meta_dict = {}
    for job_id, command in Job.jobs().items():
        if command and (command := command.command):
            if command.startswith('pg '):
                command = command[3:]
            elif command.startswith('cql '):
                command = command[4:]
            elif command.startswith('audit ') and command.strip(' ') != 'audit':
                command = command[6:]

            meta_dict[job_id] = command
    return WordCompleter(job_ids, meta_dict=meta_dict)