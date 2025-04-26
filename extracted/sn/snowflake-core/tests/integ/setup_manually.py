import subprocess
import time

import pytest


"""
Since the macos testing image doesn't have docker installed
We will create the image repo manually

run this by
```
pytest setup_manually.py --no-cov -s
```

!!! Make sure you update 'imagerepo' function in conftest.py !!!
"""

DATABASE = "TESTDB_PYTHON_AUTO"
SCHEMA = "TESTSCHEMA_AUTO"
AUTO_image_repo = "TEST_IMAGE_REPO_AUTO"


def test_setup_image(connection, db_parameters, setup_basic):
    with connection.cursor() as cursor:
        cursor.execute(f"USE DATABASE {DATABASE}")
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        cursor.execute(f"USE SCHEMA {SCHEMA}")

        check_docker_h_output = subprocess.getoutput("docker --help")
        if len(check_docker_h_output) < 50 or "command not found" in check_docker_h_output:
            raise Exception("Docker not installed")

        subprocess.run("docker pull --platform amd64 hello-world".split(" "))
        subprocess.run("docker pull --platform amd64 nginx".split(" "))

        cursor.execute(f"CREATE IMAGE REPOSITORY IF NOT EXISTS {AUTO_image_repo};")
        repo_url = cursor.execute(f"SHOW IMAGE REPOSITORIES LIKE '{AUTO_image_repo}';").fetchone()[4]
        host_name, _, _ = repo_url.partition("/")

        # Be careful with failures here not to print tokens.
        #  To avoid printing local variables use pytest.fail
        try:
            completed_process = subprocess.run(
                f"docker login {host_name} -u {db_parameters['user']} --password-stdin".split(" "),
                input=db_parameters["password"].encode() + b"\n",
                capture_output=True,
            )
            assert completed_process.returncode == 0
        except Exception:
            pytest.fail("Docker login failure")

        for image_name in ["hello-world", "nginx"]:
            subprocess.run(f"docker image tag {image_name} {repo_url}/{image_name}:latest".split(" "))
            upload_succ = False
            for _ in range(3):
                completed_process = subprocess.run(f"docker push {repo_url}/{image_name}:latest".split(" "))
                if completed_process.returncode != 0:
                    time.sleep(1)
                    continue
                upload_succ = True
                break
            assert upload_succ

        print("!!!!! Update Repo Url !!!!!")
        print(repo_url)
