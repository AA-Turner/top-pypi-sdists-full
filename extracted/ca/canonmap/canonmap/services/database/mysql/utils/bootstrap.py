import importlib.resources
import subprocess
import os

def run_sql_resource(sql_filename, mysql_user, mysql_pass, mysql_db, mysql_host="localhost"):
    with importlib.resources.path("canonmap.services.db_mysql.resources", sql_filename) as sql_path:
        cmd = [
            "mysql",
            "-u", mysql_user,
            f"-p{mysql_pass}",
            "-h", mysql_host,
            mysql_db,
            "-e", f"source {sql_path}"
        ]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {sql_filename}: {result.stderr}")
        return result.returncode == 0

def run_install_udfs_sh(mysql_user, mysql_db, mysql_host, mysql_pass):
    with importlib.resources.path("canonmap.services.db_mysql.resources", "install_udfs.sh") as script_path:
        cmd = [
            "bash",
            str(script_path),
            mysql_user,
            mysql_db,
            mysql_host,
            mysql_pass
        ]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running install_udfs.sh: {result.stderr}")
        return result.returncode == 0