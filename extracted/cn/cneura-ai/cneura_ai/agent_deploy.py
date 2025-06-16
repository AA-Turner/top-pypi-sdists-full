import os
import docker
import cneura_ai
from jinja2 import Environment, FileSystemLoader
from docker.errors import BuildError, APIError, ContainerError
from cneura_ai.agent_registry import AgentRegistry

class AgentDeployer:
    def __init__(
        self,
        agent_registry: AgentRegistry,
        remote_url: str = None,
        tls_config: docker.tls.TLSConfig = None,
        verbose: bool = True
    ):
        """
        Initialize the AgentDeployer.
        """
        self.template_dir = os.path.join(os.path.dirname(cneura_ai.__file__), 'templates')
        self.agent_registry = agent_registry
        self.verbose = verbose
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

        try:
            if remote_url:
                self.docker_client = docker.DockerClient(base_url=remote_url, tls=tls_config)
                self._log(f"[+] Connected to remote Docker at {remote_url}")
            else:
                self.docker_client = docker.from_env()
                self._log("[+] Connected to local Docker")
        except Exception as e:
            raise RuntimeError(f"[-] Failed to connect to Docker: {e}")

    def _log(self, message: str):
        if self.verbose:
            print(message)

    def render_templates(self, agent_context: dict, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        for template_name in self.env.list_templates():
            template = self.env.get_template(template_name)
            rendered_content = template.render(agent=agent_context)
            output_file = os.path.join(output_dir, template_name.replace(".j2", ""))
            with open(output_file, "w") as f:
                f.write(rendered_content)
            print(f"[+] Rendered template: {template_name} -> {output_file}")

    def build_image(self, tag: str, build_path: str):
        """
        Build a Docker image.
        """
        self._log(f"[+] Building Docker image: {tag}")
        try:
            image, logs = self.docker_client.images.build(path=build_path, tag=tag)
            for chunk in logs:
                if 'stream' in chunk:
                    self._log(chunk['stream'].strip())
            return image
        except BuildError as e:
            raise RuntimeError(f"[-] Docker build failed: {e}")
        except Exception as e:
            raise RuntimeError(f"[-] Unexpected error during build: {e}")

    def run_container(
        self,
        image_tag: str,
        env_vars: dict,
        ports: dict = None,
        name: str = None,
        agent_info=None,
        volumes: dict = None,
        mem_limit: str = None,
        cpu_shares: int = None
    ):
        """
        Run a Docker container and register the agent.
        """
        self._log(f"[+] Running container from image: {image_tag}")
        try:
            container = self.docker_client.containers.run(
                image=image_tag,
                detach=True,
                environment=env_vars,
                ports=ports,
                name=name,
                volumes=volumes,
                mem_limit=mem_limit,
                cpu_shares=cpu_shares
            )
            agent_id = self.agent_registry.register(agent_info=agent_info)
            self._log(f"[+] Container '{container.name}' is running with agent ID: {agent_id}")
            return container, agent_id
        except ContainerError as e:
            raise RuntimeError(f"[-] Failed to start container: {e}")
        except APIError as e:
            raise RuntimeError(f"[-] Docker API error: {e}")
        except Exception as e:
            raise RuntimeError(f"[-] Unexpected error while running container: {e}")

    def deploy(self, output_path: str, image_tag: str, container_name: str,
           context: dict, ports: dict = None):
        agent_context = context.get('agent', {})
        env_vars = context.get('env', {})

        self.render_templates(agent_context, output_path)
        self.build_image(tag=image_tag, build_path=output_path)
        return self.run_container(image_tag, env_vars, ports, name=container_name, agent_info=agent_context)

    def cleanup(self, container_id: str, remove_image: bool = False):
        """
        Stop and remove a container, optionally remove the image.
        """
        try:
            container = self.docker_client.containers.get(container_id)
            container.stop()
            container.remove()
            self._log(f"[+] Container '{container.name}' stopped and removed.")
            if remove_image:
                self.docker_client.images.remove(container.image.id)
                self._log(f"[+] Image '{container.image.tags[0]}' removed.")
        except Exception as e:
            self._log(f"[-] Cleanup failed: {e}")
