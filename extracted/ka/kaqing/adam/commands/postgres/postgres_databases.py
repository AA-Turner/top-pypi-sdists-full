import functools
import re
import subprocess

from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_context import Context
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.secrets import Secrets
from adam.utils import Color, ExecResult, log2, log_exc
from adam.utils_local import LocalExecResult

class ConnectionDetails:
    def __init__(self, state: ReplState, namespace: str, host: str):
        self.state = state
        self.namespace = namespace
        self.host = host

    def endpoint(self):
        return PostgresDatabases._connection_property(self.state, 'pg.secret.endpoint-key', 'postgres-db-endpoint', host=self.host)

    def port(self):
        return PostgresDatabases._connection_property(self.state, 'pg.secret.port-key', 'postgres-db-port', host=self.host)

    def username(self):
        return PostgresDatabases._connection_property(self.state, 'pg.secret.username-key', 'postgres-admin-username', host=self.host)

    def password(self):
        return PostgresDatabases._connection_property(self.state, 'pg.secret.password-key', 'postgres-admin-password', host=self.host)

class PostgresDatabases:
    def hosts(state: ReplState, namespace: str = None):
        if not namespace:
            namespace = state.namespace

        return [ConnectionDetails(state, namespace, host) for host in PostgresDatabases.host_names(namespace)]

    @functools.lru_cache()
    def host_names(namespace: str):
        ss = Secrets.list_secrets(namespace, name_pattern=Config().get('pg.name-pattern', '^{namespace}.*k8spg.*'))

        def excludes(name: str):
            exs = Config().get('pg.excludes', '.helm., -admin-secret')
            if exs:
                for ex in exs.split(','):
                    if ex.strip(' ') in name:
                        return True

            return False

        return [s for s in ss if not excludes(s)]

    def databases(state: ReplState, default_owner = False):
        dbs = []
        #  List of databases
        #                  Name                  |  Owner   | Encoding |   Collate   |    Ctype    | ICU Locale | Locale Provider |   Access privileges
        # ---------------------------------------+----------+----------+-------------+-------------+------------+-----------------+-----------------------
        #  postgres                              | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |            | libc            |
        #  stgawsscpsr_c3_c3                     | postgres | UTF8     | C           | C           |            | libc            |
        #  template1                             | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |            | libc            | =c/postgres          +
        #                                        |          |          |             |             |            |                 | postgres=CTc/postgres
        # (48 rows)
        if r := PostgresDatabases.run_sql(state, '\l', ctx=Context.new(background=False, show_out=False)):
            s = 0
            for line in r.stdout.split('\n'):
                line: str = line.strip(' \r')
                if s == 0:
                    if 'List of databases' in line:
                        s = 1
                elif s == 1:
                    if 'Name' in line and 'Owner' in line and 'Encoding' in line:
                        s = 2
                elif s == 2:
                    if line.startswith('---------'):
                        s = 3
                elif s == 3:
                    groups = re.match(r'^\s*(\S*)\s*\|\s*(\S*)\s*\|.*', line)
                    if groups and groups[1] != '|':
                        dbs.append({'name': groups[1], 'owner': groups[2]})

        if default_owner:
            dbs = [db for db in dbs if db['owner'] == PostgresDatabases.default_owner()]

        return dbs

    def tables(state: ReplState, default_schema = False):
        dbs = []
        #                                            List of relations
        #   Schema  |                            Name                            | Type  |     Owner
        # ----------+------------------------------------------------------------+-------+---------------
        #  postgres | c3_2_admin_aclpriv                                         | table | postgres
        #  postgres | c3_2_admin_aclpriv_a                                       | table | postgres
        if r := PostgresDatabases.run_sql(state, '\dt', ctx=Context.new(background=False, show_out=False)):
            s = 0
            for line in r.stdout.split('\n'):
                line: str = line.strip(' \r')
                if s == 0:
                    if 'List of relations' in line:
                        s = 1
                elif s == 1:
                    if 'Schema' in line and 'Name' in line and 'Type' in line:
                        s = 2
                elif s == 2:
                    if line.startswith('---------'):
                        s = 3
                elif s == 3:
                    groups = re.match(r'^\s*(\S*)\s*\|\s*(\S*)\s*\|.*', line)
                    if groups and groups[1] != '|':
                        dbs.append({'schema': groups[1], 'name': groups[2]})

        if default_schema:
            dbs = [db for db in dbs if db["schema"] == PostgresDatabases.default_schema()]

        return dbs

    def run_sql(state: ReplState, sql: str, database: str = None, ctx: Context = Context.NULL) -> ExecResult:
        if not database:
            database = PostgresDatabases.database(state)
        if not database:
            database = PostgresDatabases.default_db()

        username = PostgresDatabases.username(state)
        password = PostgresDatabases.password(state)
        endpoint = PostgresDatabases.endpoint(state)

        r: ExecResult = None
        if KubeContext.in_cluster():
            cmd1 = f'env PGPASSWORD={password} psql -h {endpoint} -p {PostgresDatabases.port()} -U {username} {database} --pset pager=off -c'
            ctx.log2(f'{cmd1} "{sql}"')
            # remove double quotes from the sql argument
            cmd = cmd1.split(' ') + [sql]

            p = subprocess.run(cmd, capture_output=not ctx.background, text=True)
            r = LocalExecResult.from_completed_process(cmd, p)

            ctx.log2(r.stdout)
            ctx.log2(r.stderr)
        else:
            pod_name, container_name = PostgresDatabases.pod_and_container(state.namespace)
            if not pod_name:
                return

            cmd = f'psql -h {endpoint} -p {PostgresDatabases.port(state)} -U {username} {database} --pset pager=off -c "{sql}"'
            env_prefix = f'PGPASSWORD="{password}"'

            ctx.log2(cmd, text_color=Color.gray)

            r = Pods.exec(pod_name, container_name, state.namespace, cmd, env_prefix=env_prefix, ctx=ctx)

        return r

    @functools.lru_cache()
    def pod_and_container(namespace: str):
        container_name = Config().get('pg.agent.name', 'ops-pg-agent')

        if Config().get('pg.agent.just-in-time', False):
            if not PostgresDatabases.deploy_pg_agent(container_name, namespace):
                return None

        pod_name = container_name
        try:
            # try with dedicated pg agent pod name configured
            Pods.get(namespace, container_name)
        except:
            try:
                # try with the ops pod
                container_name = Config().get('pod.name', 'ops')
                pod_name = Pods.get_with_selector(namespace, label_selector = Config().get('pod.label-selector', 'run=ops')).metadata.name
            except:
                log2(f"Could not locate {container_name} pod.")
                return None

        return pod_name, container_name

    def deploy_pg_agent(pod_name: str, namespace: str) -> str:
        image = Config().get('pg.agent.image', 'seanahnsf/kaqing')
        timeout = Config().get('pg.agent.timeout', 3600)
        try:
            Pods.create(namespace, pod_name, image, ['sleep', f'{timeout}'], env={'NAMESPACE': namespace}, sa_name='c3')
        except Exception as e:
            if e.status == 409:
                if Pods.completed(namespace, pod_name):
                    with log_exc(lambda e2: "Exception when calling BatchV1Api->create_pod: %s\n" % e2):
                        Pods.delete(pod_name, namespace)
                        Pods.create(namespace, pod_name, image, ['sleep', f'{timeout}'], env={'NAMESPACE': namespace}, sa_name='c3')

                        return
            else:
                log2("Exception when calling BatchV1Api->create_pod: %s\n" % e)

                return

        Pods.wait_for_running(namespace, pod_name)

        return pod_name

    def undeploy_pg_agent(pod_name: str, namespace: str):
        Pods.delete(pod_name, namespace, grace_period_seconds=0)

    def endpoint(state: ReplState):
        return PostgresDatabases._connection_property(state, 'pg.secret.endpoint-key', 'postgres-db-endpoint')

    def port(state: ReplState):
        return PostgresDatabases._connection_property(state, 'pg.secret.port-key', 'postgres-db-port')

    def username(state: ReplState):
        return PostgresDatabases._connection_property(state, 'pg.secret.username-key', 'postgres-admin-username')

    def password(state: ReplState):
        return PostgresDatabases._connection_property(state, 'pg.secret.password-key', 'postgres-admin-password')

    def _connection_property(state: ReplState, config_key: str, default: str, host: str = None, database: str = None):
        with pg_path(state, host=host, database=database) as (host, _):
            if not (conn := PostgresDatabases.conn_details(state.namespace, host)):
                return ''

            key = Config().get(config_key, default)
            return conn[key] if key in conn else ''

    def default_db():
        return Config().get('pg.default-db', 'postgres')

    def default_owner():
        return Config().get('pg.default-owner', 'postgres')

    def default_schema():
        return Config().get('pg.default-schema', 'postgres')

    def host(state: ReplState):
        if not state.pg_path:
            return None

        return state.pg_path.split('/')[0]

    def database(state: ReplState):
        if not state.pg_path:
            return None

        tokens = state.pg_path.split('/')
        if len(tokens) > 1:
            return tokens[1]

        return None

    @functools.lru_cache()
    def conn_details(namespace: str, host: str):
        return Secrets.get_data(namespace, host)

class PostgresPathHandler:
    def __init__(self, state: ReplState, host: str = None, database: str = None):
        self.state = state
        self.host = host
        self.database = database

    def __enter__(self) -> tuple[str, str]:
        if self.state and self.state.pg_path:
            host_n_db = self.state.pg_path.split('/')
            if not self.host:
                self.host = host_n_db[0]
            if not self.database and len(host_n_db) > 1:
                self.database = host_n_db[1]

        return self.host, self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def pg_path(state: ReplState, host: str = None, database: str = None):
    return PostgresPathHandler(state, host=host, database=database)
