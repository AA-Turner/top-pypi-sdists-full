import docker
import os
import uuid
from typing import Tuple, List

class CodeExecutor:
    def __init__(self, remote_url: str, image: str = "python:3.12-slim", memory_limit_mb: int = 512):
        self.image = image
        self.memory_limit_mb = memory_limit_mb
        self.client = docker.DockerClient(base_url=remote_url)

    def execute(self, code: str, testcases: str, dependencies: List[str] = [], configs: dict = None) -> Tuple[int, str]:
        temp_dir = "/tmp/docker_temp"
        os.makedirs(temp_dir, exist_ok=True)

        script_path = os.path.join(temp_dir, "script.py")
        test_path = os.path.join(temp_dir, "test.py")
        requirements_path = os.path.join(temp_dir, "requirements.txt")
        config_path = os.path.join(temp_dir, "config.py")
        dockerfile_path = os.path.join(temp_dir, f"Dockerfile_{uuid.uuid4().hex}")

        try:
            # Write the main script
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)

            with open(test_path, "w", encoding="utf-8") as f:
                f.write(testcases)

    
            has_dependencies = bool(dependencies)
            if has_dependencies:
                with open(requirements_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(dependencies))

            with open(config_path, "w", encoding="utf-8") as f:
                f.write("import os\n\n")
                f.write("class Config:\n")
                if configs:
                    for key in configs:
                        f.write(f"    {key.upper()} = os.getenv('{key.upper()}')\n")
                else:
                    f.write("    pass\n")

            with open(dockerfile_path, "w", encoding="utf-8") as f:
                dockerfile_content = f"""\
                FROM {self.image}
                WORKDIR /app

                # Ensure pip is available
                RUN python -m ensurepip --default-pip
                RUN python -m pip install --upgrade pip setuptools wheel

                # Copy script and test file
                COPY ./script.py script.py
                COPY ./test.py test.py
                COPY ./config.py config.py
                """
                if has_dependencies:
                    dockerfile_content += """\
                COPY ./requirements.txt requirements.txt
                RUN pip install --no-cache-dir -r requirements.txt
                """

                dockerfile_content += """\
                CMD ["python", "-u", "test.py"]
                """
                f.write(dockerfile_content)

            image_name = f"dynamic_image_{uuid.uuid4().hex}"
            try:
                image, build_logs = self.client.images.build(path=temp_dir, dockerfile=dockerfile_path, tag=image_name)

                for log in build_logs:
                    if 'stream' in log:
                        print(log['stream'], end="")

            except docker.errors.BuildError as e:
                print(f"⚠️ Docker Build Error: {e}")
                return f"⚠️ Build failed: {str(e)}", None

            environment_vars = {key.upper(): value for key, value in (configs or {}).items()}

            container = self.client.containers.run(
                image_name,
                detach=True,
                mem_limit=f"{self.memory_limit_mb}m",
                cpu_shares=512,
                stdin_open=True,
                tty=True,
                environment=environment_vars
            )

            exit_status = container.wait()
            logs = container.logs(stdout=True, stderr=True).decode("utf-8").strip()

            container.remove()
            self.client.images.remove(image=image_name, force=True)
            return None, logs

        except Exception as e:
            return f"⚠️ Error: {e}", None
        finally:
            for file_path in [script_path, test_path, requirements_path, config_path, dockerfile_path]:
                if os.path.exists(file_path):
                    os.remove(file_path)
