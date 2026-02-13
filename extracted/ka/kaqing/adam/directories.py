import os
from adam.config_holder import ConfigHolder

_dirs_created = set()

def local_q_dir():
    return creating_dir(Directories.local_q_dir())

def local_downloads_dir():
    return creating_dir(Directories.local_downloads_dir())

def local_log_dir():
    return creating_dir(Directories.local_log_dir())

def local_db_dir():
    return creating_dir(Directories.local_db_dir())

def creating_dir(dir):
    if dir not in _dirs_created:
        _dirs_created.add(dir)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    return dir

class Directories:
    def local_q_dir():
        if not ConfigHolder().config:
            # during bootstrapping
            return '/tmp/qing-db/q'

        return ConfigHolder().config.get('local-q-dir', '/tmp/qing-db/q')

    def local_downloads_dir():
        return ConfigHolder().config.get('local-downloads-dir', '/tmp/qing-db/q/downloads')

    def local_log_dir():
        return ConfigHolder().config.get('log-dir', '/tmp/qing-db/q/logs')

    def local_db_dir():
        return ConfigHolder().config.get('export.sqlite.local-db-dir', '/tmp/qing-db/q/export/db')

    def local_export_log_dir():
        return ConfigHolder().config.get('export.log-dir', '/tmp/qing-db/q/export/logs')

    def export_csv_dir():
        return ConfigHolder().config.get('export.csv_dir', '/c3/cassandra/tmp')

    def remote_q_dir():
        return ConfigHolder().config.get('remote-q-dir', '/tmp/q')

    def remote_export_table_log_dir():
        return ConfigHolder().config.get('export.remote.log-dir', '/tmp/q/export/logs')

    def remote_log_dir():
        return ConfigHolder().config.get('pod-log-dir', '/tmp/q/logs')