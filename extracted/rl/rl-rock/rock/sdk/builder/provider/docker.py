import os
import subprocess
import time
from pathlib import Path

from rock.logger import init_logger

logger = init_logger("rock.cli.sandbox")


class DockerCommand:
    """Class for executing docker commands using subprocess"""

    def __init__(self, docker_executable: str = "docker"):
        """
        Initialize DockerCommand

        Args:
            docker_executable: Path to docker executable, defaults to "docker"
        """
        self.docker_executable = docker_executable

    def _run_cmd(self, cmd, **kwargs):
        # Set default parameters
        default_kwargs = {
            "check": True,  # Raise exception if command fails
            "capture_output": False,  # Don't capture output by default, let users see real-time output
            "text": True,
        }
        default_kwargs.update(kwargs)

        try:
            logger.info(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, **default_kwargs)
            logger.info("Command executed successfully")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Docker executable not found: {self.docker_executable}")
            raise
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def login(self, image_repo_url: str, user_name: str, password: str):
        try:
            cmd = [self.docker_executable, "login", image_repo_url, "-u", user_name, "-p", password]
            logger.info(f"Executing command: {' '.join(cmd)}")
            return self._run_cmd(cmd)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def buildx_build(self, docker_file: str, context_path: str, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Execute docker buildx build command

        Args:
            context_path: Build context path
            *args: Additional command line arguments
            **kwargs: Additional parameters for subprocess.run

        Returns:
            subprocess.CompletedProcess: Command execution result
        """
        try:
            build_with_source = any(kwargs.get(key) for key in ("memory", "cpus"))
            if build_with_source:
                memory = kwargs.pop("memory", "8g")
                cpus = kwargs.pop("cpus", 2.0)
                cmd = [
                    self.docker_executable,
                    "buildx",
                    "create",
                    "--name",
                    "xrl-builder",
                    "--driver",
                    "docker-container",
                    "--driver-opt",
                    f"env.MOBY_CPUS={cpus},env.MOBY_MEMORY={memory}",
                    "--use",
                ]
                self._run_cmd(cmd, **kwargs)

                cmd = [self.docker_executable, "buildx", "use", "xrl-builder"]
                self._run_cmd(cmd, **kwargs)

            # Build base command
            cmd = [self.docker_executable, "buildx", "build", "-f", docker_file, context_path]

            # Add additional arguments
            if args:
                cmd.extend(args)

            logger.info(f"Executing command: {' '.join(cmd)}")
            t0 = time.time()
            result = self._run_cmd(cmd, capture_output=True, check=False, **kwargs)
            build_time = time.time() - t0
            self._record_build_result(context_path=context_path, result=result, build_time=build_time)
            if result.returncode != 0:
                logger.info(f"Executing command: {' '.join(cmd)}, stderr {result.stderr}")
                raise Exception(f"Start sandbox failed: {' '.join(cmd)}")
            return result
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise
        finally:
            if build_with_source:
                cmd = [self.docker_executable, "buildx", "rm", "xrl-builder"]
                self._run_cmd(cmd, **kwargs)

    def push_image(self, tag: str) -> subprocess.CompletedProcess:
        try:
            cmd = [self.docker_executable, "push", tag]
            logger.info(f"Executing command: {' '.join(cmd)}")
            return self._run_cmd(cmd)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def remove_image(self, tag: str) -> subprocess.CompletedProcess:
        try:
            cmd = [self.docker_executable, "rmi", tag]
            logger.info(f"Executing command: {' '.join(cmd)}")
            return self._run_cmd(cmd)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def manifest_inspect(self, tag: str) -> subprocess.CompletedProcess:
        try:
            cmd = [self.docker_executable, "manifest", "inspect", tag]
            logger.info(f"Executing command: {' '.join(cmd)}")
            return self._run_cmd(cmd, capture_output=True, check=False)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def run_command(self, subcommand: str, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Execute generic docker command

        Args:
            subcommand: Docker subcommand (e.g., "build", "run", "push", etc.)
            *args: Additional command line arguments
            **kwargs: Additional parameters for subprocess.run

        Returns:
            subprocess.CompletedProcess: Command execution result
        """
        cmd = [self.docker_executable, subcommand]

        if args:
            cmd.extend(args)

        logger.info(f"Executing command: {' '.join(cmd)}")

        default_kwargs = {"check": True, "capture_output": False, "text": True}
        default_kwargs.update(kwargs)

        try:
            logger.info(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, **default_kwargs)
            logger.info("Command executed successfully")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed: {e}")
            raise
        except FileNotFoundError:
            logger.error(
                f"Docker executable not found: \
                            {self.docker_executable}"
            )
            raise

    def _read_file(self, path: str):
        with open(path) as file:
            content = file.read()
            return content

    def _record_build_result(self, context_path: str, result, build_time):
        instance_id = context_path.strip("/").split("/")[-1]
        docker_file_content = self._read_file(f"{context_path}/Dockerfile")
        setup_env_content = self._read_file(f"{context_path}/setup_env.sh")
        setup_repo_content = self._read_file(f"{context_path}/setup_repo.sh")
        with open("/data/build_result.jsonl", "a") as f:
            build_result = {
                "instance_id": instance_id,
                "return_code": result.returncode,
                "build_time": round(build_time, 2),
                "docker_file": docker_file_content,
                "setup_env": setup_env_content,
                "setup_repo": setup_repo_content,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
            import json

            f.write(json.dumps(build_result) + os.linesep)


class Docker:
    docker_cmd = DockerCommand()
    dockerfile: str
    project_root: str
    tag: str
    params: dict = {}

    def __init__(
        self,
        tag: str,
        file: str = "Dockerfile",
        registry_url: str | None = None,
        user_name: str | None = None,
        password: str | None = None,
        *args,
        **kwargs,
    ):
        # If directory is a relative path (e.g., "iflow-cli"), \
        # look for it in the project root's docker directory
        project_root = Path(__file__).parent.parent.parent.parent
        self.project_root = str(project_root.absolute())
        self._dockerfile(file=file)
        self.tag = tag
        self.params = kwargs
        self.registry_url = registry_url
        self.user_name = user_name
        self.password = password

    def _dockerfile(self, file: str = "Dockerfile"):
        docker_root = Path(self.project_root) / "docker"
        if not os.path.isabs(file):
            self.dockerfile = str((docker_root / file).absolute())  # noqa
        else:
            self.dockerfile = file

    def build(self):
        docker_file = self.dockerfile
        print(
            f" => Building sandbox from dockerfile: \
              {docker_file} with tag: {self.tag} and params: {self.params}"
        )
        context_path = self.params.pop("context_path", self.project_root)
        self.docker_cmd.buildx_build(docker_file, context_path, "--tag", self.tag, **self.params)

    def hub_login(self):
        print(f" => Login to dockerhub: {self.registry_url} with user: {self.user_name} password: {self.password}")
        logger.info(
            f" => Login to dockerhub: {self.registry_url} with user: {self.user_name} password: {self.password}"
        )
        self.docker_cmd.login(self.registry_url, self.user_name, self.password)

    def push(self):
        print(f" => Pushing sandbox image: {self.tag}")
        logger.info(f" => Pushing sandbox image: {self.tag}")
        self.docker_cmd.push_image(self.tag)

    def remove(self):
        print(f" => Removing sandbox image: {self.tag}")
        logger.info(f" => Removing sandbox image: {self.tag}")
        self.docker_cmd.remove_image(self.tag)

    def manifest(self) -> str:
        print(f" => Manifest sandbox image: {self.tag}")
        logger.info(f" => Manifest sandbox image: {self.tag}")
        result = self.docker_cmd.manifest_inspect(self.tag)
        return result.stdout if result.returncode == 0 else result.stderr
