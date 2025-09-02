import functools
import re
import subprocess

from adam.config import Config
from adam.k8s_utils.kube_context import KubeContext
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.secrets import Secrets
from adam.utils import log2

class PostgresSession:
    def __init__(self, ns: str, path: str):
        self.namespace = ns
        self.conn_details = None
        self.host = None
        self.db = None

        if path:
            tks = path.split('/')
            hn = tks[0].split('@')
            self.host = hn[0]
            if len(hn) > 1 and not ns:
                self.namespace = hn[1]

            if len(tks) > 1:
                self.db = tks[1]

    # work for databases()
    def __eq__(self, other: 'PostgresSession'):
        return self.host == other.host

    def __hash__(self):
        return hash(self.host)

    def find_namespace(self, arg: str):
        if arg:
            tks = arg.split('@')
            if len(tks) > 1:
                return tks[1]

        return None

    def directory(self, arg: str = None):
        if arg:
            if arg == '..':
                if self.db:
                    self.db = None
                else:
                    self.host = None
            else:
                tks = arg.split('@')
                arg = tks[0]
                if not self.host:
                    self.host = arg
                else:
                    self.db = arg

        if not self.host:
            return None

        d = self.host
        if not self.db:
            return d

        return f'{self.host}/{self.db}'

    def hosts(ns: str):
        return PostgresSession.hosts_for_namespace(ns)

    @functools.lru_cache()
    def hosts_for_namespace(ns: str):
        ss = Secrets.list_secrets(ns, name_pattern=Config().get('pg.name-pattern', '^{namespace}.*k8spg.*'))

        def excludes(name: str):
            exs = Config().get('pg.excludes', '.helm., -admin-secret')
            if exs:
                for ex in exs.split(','):
                    if ex.strip(' ') in name:
                        return True

            return False

        return [s for s in ss if not excludes(s)]

    @functools.lru_cache()
    def databases(self):
        dbs = []
        #  List of databases
        #                  Name                  |  Owner   | Encoding |   Collate   |    Ctype    | ICU Locale | Locale Provider |   Access privileges
        # ---------------------------------------+----------+----------+-------------+-------------+------------+-----------------+-----------------------
        #  postgres                              | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |            | libc            |
        #  stgawsscpsr_c3_c3                     | postgres | UTF8     | C           | C           |            | libc            |
        #  template1                             | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |            | libc            | =c/postgres          +
        #                                        |          |          |             |             |            |                 | postgres=CTc/postgres
        # (48 rows)
        r = self.run_sql('\l', show_out=False)
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

        return dbs

    def tables(self):
        dbs = []
        #                                            List of relations
        #   Schema  |                            Name                            | Type  |     Owner
        # ----------+------------------------------------------------------------+-------+---------------
        #  postgres | c3_2_admin_aclpriv                                         | table | postgres
        #  postgres | c3_2_admin_aclpriv_a                                       | table | postgres
        r = self.run_sql('\dt', show_out=False)
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

        return dbs

    def run_sql(self, sql: str, show_out = True):
        db = self.db if self.db else PostgresSession.default_db()

        if KubeContext.in_cluster():
            cmd1 = f'env PGPASSWORD={self.password()} psql -h {self.endpoint()} -p {self.port()} -U {self.username()} {db} --pset pager=off -c'
            log2(f'{cmd1} "{sql}"')
            # remove double quotes from the sql argument
            cmd = cmd1.split(' ') + [sql]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if show_out:
                log2(r.stdout)
                log2(r.stderr)

            return r
        else:
            ns = self.namespace
            image = Config().get('pg.agent.image', 'seanahnsf/kaqing')
            pod_name = Config().get('pg.agent.name', 'kaqing-agent')
            timeout = Config().get('pg.agent.timeout', 3600)

            try:
                Pods.create(ns, pod_name, image, ['sleep', f'{timeout}'], env={'NAMESPACE': ns}, sa_name='c3')
            except Exception as e:
                if e.status == 409:
                    if Pods.completed(ns, pod_name):
                        try:
                            Pods.delete(pod_name, ns)
                            Pods.create(ns, pod_name, image, ['sleep', f'{timeout}'], env={'NAMESPACE': ns}, sa_name='c3')
                        except Exception as e2:
                            log2("Exception when calling BatchV1Api->create_pod: %s\n" % e2)

                            return
                else:
                    log2("Exception when calling BatchV1Api->create_pod: %s\n" % e)

                    return

            Pods.wait_for_running(ns, pod_name)

            cmd = f'PGPASSWORD="{self.password()}" psql -h {self.endpoint()} -p {self.port()} -U {self.username()} {db} --pset pager=off -c "{sql}"'

            return Pods.exec(pod_name, pod_name, ns, cmd, show_out=show_out)

    def endpoint(self):
        if not self.conn_details:
            self.conn_details = Secrets.get_data(self.namespace, self.host)

        endpoint_key = Config().get('pg.secret.endpoint-key', 'postgres-db-endpoint')

        return self.conn_details[endpoint_key] if endpoint_key in self.conn_details else ''

    def port(self):
        if not self.conn_details:
            self.conn_details = Secrets.get_data(self.namespace, self.host)

        port_key = Config().get('pg.secret.port-key', 'postgres-db-port')

        return  self.conn_details[port_key] if port_key in self.conn_details else ''

    def username(self):
        if not self.conn_details:
            self.conn_details = Secrets.get_data(self.namespace, self.host)

        username_key = Config().get('pg.secret.username-key', 'postgres-admin-username')

        return  self.conn_details[username_key] if username_key in self.conn_details else ''

    def password(self):
        if not self.conn_details:
            self.conn_details = Secrets.get_data(self.namespace, self.host)

        password_key = Config().get('pg.secret.password-key', 'postgres-admin-password')

        return  self.conn_details[password_key] if password_key in self.conn_details else ''

    def default_db():
        return Config().get('pg.default-db', 'postgres')

    def default_owner():
        return Config().get('pg.default-owner', 'postgres')

    def default_schema():
        return Config().get('pg.default-schema', 'postgres')