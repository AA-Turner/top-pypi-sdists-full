import docker
import json
import os
import cneura_ai
from docker.models.containers import Container
from typing import List, Dict, Optional
import click
from yaspin import yaspin
from yaspin.spinners import Spinners


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.running_containers: Dict[str, Container] = {}
        self.package_root = os.path.dirname(cneura_ai.__file__)

    def pull_image(self, image_name: str) -> None:
        click.echo(f"📦 Pulling image: {image_name}")
        self.client.images.pull(image_name)

    def build_image(self, dockerfile_path: str, tag: str) -> None:
        build_path = os.path.join(self.package_root, dockerfile_path)
        build_path = os.path.abspath(build_path)

        if not os.path.isdir(build_path):
            click.echo(f"❌ Build path is not a directory: {build_path}")
            return

        click.echo(f"📦 Building image from path: {build_path} with tag: {tag}")
        with yaspin(Spinners.dots, text=f"🔨 Building image: {tag}", color="cyan") as spinner:
            try:
                self.client.images.build(path=build_path, tag=tag)
                spinner.ok("✅")
            except Exception as e:
                spinner.fail(f"❌ Build failed: {e}")
                click.echo(f"❌ Build error: {e}")

    def run_container(self, image: str, name: Optional[str] = None,
                  ports: Optional[Dict[str, int]] = None,
                  env: Optional[Dict[str, str]] = None,
                  detach: bool = True) -> Optional[Container]:
        container = None
        try:
            container = self.client.containers.get(name)
            container.reload()

            if container.status != "running":
                click.echo(f"🔄 Restarting container: {name}")
                container.start()
            else:
                click.echo(f"✅ Container already running: {name}")

        except docker.errors.NotFound:
            try:
                with yaspin(Spinners.dots, text=f"🚀 Starting container: {name}", color="cyan") as spinner:
                    container = self.client.containers.run(
                        image=image,
                        name=name,
                        ports=ports,
                        environment=env,
                        detach=detach
                    )
                    spinner.ok("✅")
            except Exception as e:
                spinner.fail("💥")
                click.echo(f"❌ Failed to start new container '{name}': {e}")
                return None  # Prevent reference to unassigned 'container'

        except Exception as e:
            click.echo(f"❌ Failed to get or start existing container '{name}': {e}")
            return None

        if container:
            self.running_containers[container.id] = container
        return container

    def bulk_run_containers(self, image: str, count: int,
                            base_name: str = "bulk_container",
                            port_start: int = 8000,
                            ports: Optional[Dict[str, int]] = None,
                            env: Optional[Dict[str, str]] = None) -> List[Container]:
        click.echo(f"📦 Launching {count} container(s) from image: {image}")
        containers = []

        for i in range(count):
            name = f"{base_name}_{i}"

            container = self.run_container(
                image=image,
                name=name,
                ports=ports,
                env=env
            )
            if container:
                containers.append(container)

        return containers

    def load_from_config(self, json_path: str, default_port_start: int = 8000) -> None:
        if not os.path.exists(json_path):
            click.echo(f"❌ Config file {json_path} not found.")
            return

        with open(json_path, 'r') as f:
            configs = json.load(f)

        port_counter = default_port_start

        for cfg in configs:
            name = cfg.get("name", "container")
            image = cfg.get("image")
            dockerfile_path = cfg.get("dockerfile_path")
            tag = cfg.get("tag", f"{name}_tag")
            ports = cfg.get("ports", {})
            env = cfg.get("env", {})
            count = cfg.get("count", 1)
            if dockerfile_path:
                self.build_image(dockerfile_path, tag)
                image = tag
            elif image:
                self.pull_image(image)

            self.bulk_run_containers(
                image=image,
                count=count,
                base_name=name,
                port_start=port_counter,
                ports=ports,
                env=env
            )

            port_counter += count

    def stop_all(self):
        """Stop and remove all running containers."""
        containers = self.client.containers.list()
        for container in containers:
            try:
                container.stop()

                container.remove(force=True)
                click.echo(f"✅ Stopped and removed container: {container.name}")
            except Exception as e:
                click.echo(f"❌ Failed to stop/remove {container.name}: {e}")

    def delete_container(self, name: str):
        """Stop and remove a container by name."""
        try:
            container = self.client.containers.get(name)
            container.stop()
            container.remove()
            click.echo(f"🗑️ Deleted container: {name}")
        except docker.errors.NotFound:
            click.echo(f"⚠️ Container '{name}' not found.")
        except Exception as e:
            click.echo(f"❌ Error deleting '{name}': {e}")

    def list_running_containers(self) -> list:
        """Return a list of running containers."""
        containers = self.client.containers.list()
        return [{
            "name": container.name,
            "status": container.status,
            "ports": container.attrs.get("NetworkSettings", {}).get("Ports", {})
        } for container in containers]
