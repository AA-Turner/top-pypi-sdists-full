"""Instruction-based simulator SDK generator.

Generates simple helper packages for sims that don't need OpenAPI clients.
These sims provide setup instructions and environment variable helpers.
"""

import importlib.resources
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


@dataclass
class ServiceConfig:
    """Configuration for a named service endpoint."""

    port: int
    description: str = ""


@dataclass
class EnvVarConfig:
    """Configuration for an environment variable."""

    description: str = ""
    template: str | None = None  # Template with {service:NAME} placeholders
    default: str | None = None  # Static default value
    env_key: str | None = None  # Read from another env var


@dataclass
class InstructionConfig:
    """Parsed instruction configuration from instructions.yaml."""

    env_prefix: str
    services: dict[str, ServiceConfig] = field(default_factory=dict)
    env_vars: dict[str, EnvVarConfig] = field(default_factory=dict)
    instructions: str = ""
    title: str = ""
    description: str = ""
    version: str = "0.1.0"

    @classmethod
    def from_yaml(cls, path: Path) -> "InstructionConfig":
        """Parse instruction config from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        if data.get("type") != "instruction":
            raise ValueError(f"Expected type: instruction, got: {data.get('type')}")

        env_prefix = data.get("env_prefix", "")
        title = data.get("title", "")
        description = data.get("description", "")
        version = data.get("version", "0.1.0")

        # Parse services
        services = {}
        for name, svc_data in data.get("services", {}).items():
            services[name] = ServiceConfig(
                port=svc_data["port"],
                description=svc_data.get("description", ""),
            )

        # Parse env vars
        env_vars = {}
        for name, var_data in data.get("env_vars", {}).items():
            env_vars[name] = EnvVarConfig(
                description=var_data.get("description", ""),
                template=var_data.get("template"),
                default=var_data.get("default"),
                env_key=var_data.get("env_key"),
            )

        instructions = data.get("instructions", "")

        return cls(
            env_prefix=env_prefix,
            services=services,
            env_vars=env_vars,
            instructions=instructions,
            title=title,
            description=description,
            version=version,
        )


class InstructionGenerator:
    """Generates instruction-based simulator SDK packages."""

    def __init__(
        self,
        config: InstructionConfig,
        output_path: Path,
        package_name: str,
        generator_version: str | None = None,
    ):
        self.config = config
        self.output = output_path
        self.package_name = package_name
        self.generator_version = generator_version

        # Get template directory using importlib.resources
        template_ref = importlib.resources.files("plato._sims_generator") / "templates" / "instruction"
        # For filesystem templates, we need the actual path
        self.template_dir = Path(str(template_ref))

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self):
        """Generate the instruction-based SDK package."""
        # Create output structure
        self.output.mkdir(parents=True, exist_ok=True)

        # Generate helpers.py
        self._generate_helpers()

        # Generate __init__.py
        self._generate_init()

        # Copy instructions.yaml to output
        self._copy_instructions_yaml()

        # Generate py.typed marker
        self._generate_py_typed()

        # Format with ruff
        self._format()

    def _generate_helpers(self):
        """Generate the helpers module."""
        template = self.env.get_template("helpers.py.jinja")
        content = template.render(
            config=self.config,
            package_name=self.package_name,
            generator_version=self.generator_version,
        )
        (self.output / "helpers.py").write_text(content)

    def _generate_init(self):
        """Generate package __init__.py."""
        template = self.env.get_template("init.py.jinja")
        content = template.render(
            config=self.config,
            package_name=self.package_name,
            generator_version=self.generator_version,
        )
        (self.output / "__init__.py").write_text(content)

    def _copy_instructions_yaml(self):
        """Bundle the instructions.yaml config with the package."""
        # We'll generate a cleaned version of the config
        env_vars: dict[str, dict[str, str | int]] = {}
        config_data: dict[str, str | dict] = {
            "type": "instruction",
            "env_prefix": self.config.env_prefix,
            "title": self.config.title,
            "description": self.config.description,
            "version": self.config.version,
            "services": {
                name: {"port": svc.port, "description": svc.description} for name, svc in self.config.services.items()
            },
            "env_vars": env_vars,
            "instructions": self.config.instructions,
        }

        for name, var in self.config.env_vars.items():
            var_data: dict = {"description": var.description}
            if var.template:
                var_data["template"] = var.template
            if var.default:
                var_data["default"] = var.default
            if var.env_key:
                var_data["env_key"] = var.env_key
            env_vars[name] = var_data

        with open(self.output / "instructions.yaml", "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

    def _generate_py_typed(self):
        """Generate py.typed marker for PEP 561 compliance."""
        (self.output / "py.typed").write_text("")

    def _format(self):
        """Format generated code with ruff."""
        try:
            subprocess.run(
                ["ruff", "check", str(self.output), "--fix", "--quiet"],
                capture_output=True,
            )
            subprocess.run(
                ["ruff", "format", str(self.output), "--quiet"],
                capture_output=True,
            )
        except FileNotFoundError:
            pass  # ruff not installed, skip formatting
