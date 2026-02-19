import re

from adam.commands.postgres.postgres_databases import PostgresDatabases
from adam.commands.postgres.utils_postgres import ops
from adam.config import Config
from adam.utils_context import NULL
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_local import local_exec
from adam.utils_repl.repl_state import ReplState

def get_container_version(state: ReplState, ctx = NULL) -> tuple[str, int, str]:
    # #!/usr/bin/env python
    # # -*- coding: utf-8 -*-

    # __version__ = "2.0.296"  #: the working version
    # __release__ = "1.0.0"  #: the release version

    with ops(state) as pod:
        version_py_path = Config().get('pod.version-py', '/usr/local/lib/python3.10/dist-packages/adam/version.py')
        r = pod.exec(f'cat {version_py_path}', ctx=ctx.copy(show_out=False))
        if isinstance(r, PodExecResult):
            if r.exit_code():
                return None, r.exit_code(), r.stdout + '\n' + r.stderr
            else:
                for line in r.stdout.split('\n'):
                    if line and (group := re.match(r'__version__ = "(.*)"', line.strip(' \r'))):
                        return group[1], 0, r.stderr
                return None, 0, f'Could not locate version line from {version_py_path}.'

        return None, 0, 'Cannot locate postgres agent or ops pod.'

def get_latest_version():
    repo = Config().get('pod.image-repository', 'https://hub.docker.com/v2/repositories/seanahnsf/kaqing')
    excludes = ' | '.join([f"grep -v '{x}'" for x in ['latest', 'buildcache']])
    curl = f"curl -s '{repo}/tags' -H 'Content-Type: application/json' | jq -r '.results[].name' | {excludes} | sort -r | head -n 1"
    r = local_exec(['bash', '-c', curl])

    return r.stdout.strip(' \r\n')

# inject get_latest_version due to circular dependencies
PostgresDatabases.get_latest_version = get_latest_version
