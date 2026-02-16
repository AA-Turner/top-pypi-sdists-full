from datetime import datetime
import os
import re
import threading
from typing import TextIO

from adam.directories import local_log_dir
from adam.utils_global import thread_local
from adam.utils_log import log_exc

class Job:
    _last_job: 'Job' = None
    _job_scheduler: 'Job' = None
    _node_scheduler: 'Job' = None

    _jobs: dict[str, 'Job'] = {}
    _pod_log_cnts_by_job_id: dict[str, int] = {}
    lock = threading.Lock()

    def local_log_file(command: str, job_id: str = None, err = False, dir: str = None, extra: dict[str, str] = {}):
        with log_exc():
            job: Job = Job.create(job_id, command, extra)

            return job._local_log_file(dir, err=err)

    def pod_log_file(command: str,
                     pod_name: str = None,
                     job_id: str = None,
                     pod_suffix: str = None,
                     suffix = '.log',
                     err = False,
                     dir: str = None,
                     extra: dict[str, str] = {}):
        with log_exc():
            # for export, local file creates the last file, then pods will try to create the last file again
            job: Job = Job.create(job_id, command, extra, replace_last_file = False)

            if pod_suffix is None:
                pod_suffix = '{pod}'
                if pod_name:
                    pod_suffix = pod_name
                    if groups := re.match(r'.*-(.*)', pod_name):
                        pod_suffix = f'-{groups[1]}'

            log_file = job._pod_log_file(dir, pod_suffix=pod_suffix, suffix=suffix, err=err)

            pod_log_cnt = 0
            with Job.lock:
                if job_id not in Job._pod_log_cnts_by_job_id:
                    Job._pod_log_cnts_by_job_id[job_id] = pod_log_cnt
                else:
                    pod_log_cnt = Job._pod_log_cnts_by_job_id[job_id]

                Job._pod_log_cnts_by_job_id[job_id] = pod_log_cnt + 1

            return log_file, pod_log_cnt

    def create(job_id: str, command: str, extra: dict[str, str], replace_last_file = True):
        if not job_id:
            job_id = Job.new_id()

        if job_id in Job.jobs():
            return Job.jobs()[job_id]

        job = Job(command=command, job_id=job_id, extra=extra)
        if command:
            if command not in ['job-scheduler']:
                if Job.write_last_job(job, replace=replace_last_file):
                    Job._last_job = job
                    Job._jobs[job_id] = job

            if (tks := command.split(' ')) and tks[0] == 'restart' and tks[1] in ['cassandra']:
                Job._node_scheduler = job
            elif command == 'job-scheduler':
                Job._job_scheduler = job

        # print('SEAN job create', job, job.job_id, job.command)

        return job

    def new_id(dt: datetime = None, cmd: str = None):
        if not dt:
            dt = datetime.now()

        # print('SEAN Job.new_id', cmd)

        id = dt.strftime("%d%H%M%S")
        if not cmd or cmd not in ['job-scheduler']:
            Job._last_job = Job(job_id=id)

        return id

    def last_job(job_id: str = None):
        if job_id:
            if job_id in Job._jobs:
                return Job._jobs[job_id]

            return None
        else:
            if job := Job._last_job:
                return job

            job = Job.read_last_job()
            Job._last_job = job

            return job

    def jobs():
        return Job._jobs

    def job(job_id):
        with Job.lock:
            if job_id in Job._jobs:
                return Job._jobs[job_id]

            return None

    def node_scheduler():
        return Job._node_scheduler

    def job_scheduler():
        return Job._job_scheduler

    def write_last_job(cmd: 'Job', replace = True):
        file = f'{local_log_dir()}/last'

        if not replace and os.path.exists(file):
            return False

        with open(file, 'wt') as f:
            cmd.write(f)

        return True

    def read_last_job() -> 'Job':
        path = f'{local_log_dir()}/last'
        with open(path, 'rt') as f:
            return Job.read(f)

    def read(f: TextIO):
        job_id = None
        command = None
        raw_command = ''
        extra: dict[str, str] = {}
        with log_exc():
            job_id = f.readline().strip(' \r\n')
            command = f.readline().strip(' \r\n')
            raw_command = f.readline().strip(' \r\n')
            while(e := f.readline().strip(' \r\n')):
                if groups := re.match(r'(.*?):(.*)', e):
                    extra[groups[1]] = groups[2].strip(' \r\n')

        return Job(command, raw_command, job_id, extra)

    def __init__(self, command: str = None, raw_command: str = None, job_id: str = None, extra: dict[str, str] = {}):
        self.command = command

        self.raw_command = raw_command
        if hasattr(thread_local, 'cmd'):
            self.raw_command = thread_local.cmd
        if self.raw_command is None:
            self.raw_command = ''

        self.scheduled_command = ''
        if hasattr(thread_local, 'scheduled_command'):
            self.scheduled_command = thread_local.scheduled_command

        self.job_id = job_id
        self.extra = extra
        # print('SEAN Job init', self.job_id, self.command)

    def write(self, f: TextIO):
        f.write(self.job_id)
        f.write('\n')
        f.write(self.command)
        f.write('\n')
        f.write(self.raw_command)
        if self.extra:
            for k, v in self.extra.items():
                f.write('\n')
                f.write(f'{k}: {v}')

    def _local_log_file(self, dir: str = None, err = False):
        if not dir:
            dir = local_log_dir()

        return f'{dir}/{self.job_id}{self.command_suffix()}.{"err" if err else "log"}'

    def _pod_log_file(self, dir: str, pod_suffix: str = None, suffix: str = None, err = False):
        if not dir:
            dir = local_log_dir()

        if suffix:
            return f'{dir}/{self.job_id}{self.command_suffix()}{pod_suffix}{suffix}'

        return f'{dir}/{self.job_id}{self.command_suffix()}{pod_suffix}.{"err" if err else "log"}'

    def command_suffix(self):
        suffix = ''

        if self.command and self.command.startswith('nodetool '):
            suffix = self.command.strip(' &')
            suffix = suffix.split(' ')[-1]
            if suffix:
                suffix = f'-{suffix}'

        return suffix