import ast
import sys
import textwrap
import docker
import hashlib
import socket 
from stdlib_list import stdlib_list
from pathlib import Path
from typing import List
import shutil
from cneura_ai.tool_registry import ToolRegistry
from cneura_ai.logger import logger


class ToolDeployer:
    def __init__(self, script_content: str, remote_url: str, mongo_uri: str, name: str, description: dict, configs: dict = None):
        self.script_content = script_content
        self.remote_url = remote_url
        self.name = name
        self.description = description
        self.registry = ToolRegistry(mongo_uri=mongo_uri)
        self.script_hash = hashlib.sha256(script_content.encode()).hexdigest()[:8]
        self.base_dir = Path(f"./generated/tool_{self.script_hash}")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.docker_client = docker.DockerClient(base_url=remote_url)
        self.imports, self.classes = self.extract_imports_and_classes(script_content)
        self.configs = configs

    def extract_imports_and_classes(self, source: str):
        """Extract import statements and classes with __call__ and zero-arg __init__."""
        tree = ast.parse(source)
        imports = []
        class_defs = []

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))
            elif isinstance(node, ast.ClassDef):
                has_call = False
                init_args_valid = True

                for body_item in node.body:
                    if isinstance(body_item, ast.FunctionDef):
                        if body_item.name == "__call__":
                            has_call = True
                        elif body_item.name == "__init__":
                            args = body_item.args
                            params = args.args[1:]
                            defaults = args.defaults
                            num_required = len(params) - len(defaults)

                            if num_required > 0:
                                init_args_valid = False

                if has_call and init_args_valid:
                    class_defs.append({
                        "name": node.name,
                        "code": ast.get_source_segment(source, node)
                    })

        return imports, class_defs


    def extract_libraries_from_imports(self, imports: List[str]) -> List[str]:
        """Extract third-party libraries from the import statements."""
        libraries = set()

        for imp in imports:
            if "import" in imp:
                parts = imp.strip().split(" ")
                if len(parts) > 1:
                    libraries.add(parts[1].split(".")[0])
            elif "from" in imp:
                parts = imp.strip().split(" ")
                if len(parts) > 1:
                    libraries.add(parts[1].split(".")[0])

        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        standard_libs = set(stdlib_list(version))
        return [lib for lib in libraries if lib not in standard_libs]

    def write_tool_file(self):
        """Write the class and its imports to a new Python file."""
        with open(self.base_dir / "tool.py", "w") as f:
            for imp in self.imports:
                f.write(imp + "\n")
            f.write("\n")
            for cls in self.classes:
                f.write(cls["code"] + "\n")

    def write_config_file(self):
        """Write the class and its imports to a new Python file."""
        with open(self.base_dir / "config.py", "w") as f:
            f.write("import os\n\n")
            f.write("class Config:\n")
            if self.configs:
                for key in self.configs:
                    f.write(f"    {key.upper()} = os.getenv('{key.upper()}')\n")
            else:
                f.write("    pass\n")

    def write_main_api(self):
        """Write the FastAPI application using the extracted class."""
        class_name = self.classes[0]["name"]

        lines = [
            "from fastapi import FastAPI",
            "from pydantic import BaseModel",
            f"from tool import {class_name}",
            "from typing import Any",
            "from inspect import signature, Parameter",
            "",
            "app = FastAPI()",
            "",
            f"tool = {class_name}()",
            "",
            "sig = signature(tool.__call__)",
            "fields = {}",
            "annotations = {}",
            "for name, param in sig.parameters.items():",
            "    if name != 'self':",
            "        annotations[name] = param.annotation if param.annotation != Parameter.empty else Any",
            "        fields[name] = (annotations[name], param.default if param.default != Parameter.empty else ...)",
            "",
            "InputModel = type('InputModel', (BaseModel,), {'__annotations__': annotations})",
            "",
            "@app.post('/run')",
            "def run_tool(input_data: InputModel):",
            "    return { 'result': tool(**input_data.dict()) }",
            "",
            "@app.get('/info')",
            "def info():",
            "    return {",
            f"        'tool': '{self.name}',",
            f"        'description': {self.description},",
            "        'parameters': list(fields.keys())",
            "    }",
        ]

        content = "\n".join(lines)

        with open(self.base_dir / "main.py", "w") as f:
            f.write(content)


    def write_requirements(self):
        """Write a requirements.txt with third-party libraries."""
        libraries = self.extract_libraries_from_imports(self.imports)
        with open(self.base_dir / "requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\n")
            for lib in libraries:
                f.write(f"{lib}\n")

    def write_dockerfile(self):
        """Write a Dockerfile to build and run the FastAPI application."""
        dockerfile = f"""
        FROM python:3.11-slim

        WORKDIR /app
        COPY . /app

        RUN pip install --no-cache-dir -r requirements.txt

        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
        """
        with open(self.base_dir / "Dockerfile", "w") as f:
            f.write(textwrap.dedent(dockerfile))

    def build_image_remote(self):
        """Build the Docker image remotely using Docker SDK."""
        image_tag = f"{self.name}-{self.script_hash}"
        logger.info(f"🔨 Building Docker image '{image_tag}' on remote engine...")

        image, logs = self.docker_client.images.build(
            path=str(self.base_dir),
            tag=image_tag
        )
        for chunk in logs:
            if 'stream' in chunk:
                print(chunk['stream'].strip())

        logger.info(f"🧹 Removing temporary folder: {self.base_dir}")
        shutil.rmtree(self.base_dir, ignore_errors=True)
        return image_tag
    
    def _get_free_port(self):
        """Find a free port on the host machine."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0)) 
            return s.getsockname()[1]

    def run_container_remote(self, image_tag: str):
        """Run the Docker container remotely using Docker SDK with a random unique port."""
        container_name = f"{image_tag}-container"
        host_port = self._get_free_port()

        logger.info(f"🚀 Running container '{container_name}' on port {host_port}...")

        try:
            existing = self.docker_client.containers.get(container_name)
            logger.info("🗑️ Removing existing container...")
            existing.remove(force=True)
        except docker.errors.NotFound:
            pass

        self.docker_client.containers.run(
            image=image_tag,
            name=container_name,
            ports={"8000/tcp": host_port},
            detach=True
        )

        logger.info(f"✅ Container '{container_name}' is running at port {host_port}")
        return host_port

    def deploy(self):
        """Deploy the tool as a FastAPI application with Docker and register it."""
        self.write_tool_file()
        self.write_main_api()
        self.write_requirements()
        self.write_dockerfile()
        image_tag = self.build_image_remote()
        port = self.run_container_remote(image_tag)

        register_id = self.registry.register({
            "name": image_tag,
            "container_name": f"{image_tag}-container",
            "port": port,
            "run": f"http://localhost:{port}/run",
            "doc": f"http://localhost:{port}/info",
        })

        from inspect import signature

        tool_code = compile(self.script_content, "<string>", "exec")
        namespace = {}
        exec(tool_code, namespace)

        tool_class_name = self.classes[0]["name"]
        tool_instance = namespace[tool_class_name]()
        sig = signature(tool_instance.__call__)
        parameters = [name for name in sig.parameters if name != 'self']

        return str(register_id), f"http://localhost:{port}/run", f"http://localhost:{port}/info", parameters


        


