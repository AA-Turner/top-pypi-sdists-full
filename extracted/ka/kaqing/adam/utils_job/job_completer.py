from prompt_toolkit.completion import WordCompleter

from adam.utils_job.job import Job

def job_completer(retriable=False):
    # job_ids = list(reversed(sorted(Job.jobs().keys())))

    job_ids = []
    meta_dict = {}
    for job_id, job in Job.jobs().items():
        if retriable and not job.retriable:
            continue

        if job:
            job_ids.append(job_id)

            if cmd := job.command:
                if cmd.startswith('pg '):
                    cmd = cmd[3:]
                elif cmd.startswith('cql '):
                    cmd = cmd[4:]
                elif cmd.startswith('audit ') and cmd.strip(' ') != 'audit':
                    cmd = cmd[6:]

                meta_dict[job_id] = cmd
    return WordCompleter(reversed(sorted(job_ids)), meta_dict=meta_dict)