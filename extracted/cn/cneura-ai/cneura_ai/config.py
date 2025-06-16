import os
import json
from pathlib import Path
import importlib.resources


class CLIConfig:
    VERSION = "0.2.0"

    # Load path to configs inside the package
    CONFIG_DIR = Path(__file__).parent / "configs"
    DEFAULT_RUN_CONFIG = CONFIG_DIR / "run.json"
    DEFAULT_RUN_CONFIG_TEMPLATE = CONFIG_DIR / "run.template.json"
    DEFAULT_INIT_CONFIG = CONFIG_DIR / "init.json"
    DEFAULT_INIT_CONFIG_TEMPLATE = CONFIG_DIR / "init.template.json"

    SECRET_KEY = os.getenv("SECRET_KEY", "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4")

    # External services
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "host.docker.internal")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
    LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://host.docker.internal:8765")
    REMOTE_URL = os.getenv("REMOTE_URL", "tcp://host.docker.internal:2375")
    REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://host.docker.internal:27017/")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "host.docker.internal")
    CHROMA_PORT = os.getenv("CHROMA_PORT", 8888)
    REDIS_URL = os.getenv("REDIS_URL", "redis://host.docker.internal:6379")
    WEBSOCKET_SERVER = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
    WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT", 8765)

    # Queues (same as before)
    CODE_SYNTH_INPUT = "tool.code.synth"
    CODE_SYNTH_OUTPUT = "tool.code.test"
    CODE_SYNTH_ERROR = "tool.synth.error"
    CODE_TEST_INPUT = "tool.code.test"
    CODE_TEST_OUTPUT = "tool.code.deps"
    CODE_TEST_ERROR = "tool.test.error"
    CODE_DEPS_INPUT = "tool.code.deps_in"
    CODE_DEPS_OUTPUT = "tool.code.exec"
    CODE_DEPS_OUT = "tool.code.deps_out"
    CODE_DEPS_ERROR = "tool.deps.error"
    CODE_EXE_INPUT = "tool.code.exec"
    CODE_EXE_OUTPUT = "tool.code.debug"
    CODE_EXE_OUT = "tool.code.deploy"
    CODE_EXE_ERROR = "tool.exec.error"
    CODE_DEBUG_INPUT = "tool.code.debug"
    CODE_DEBUG_OUTPUT = "tool.code.test"
    CODE_DEBUG_ERROR = "tool.debug.error"
    TOOL_DEPLOY_INPUT = "tool.code.deploy"
    TOOL_DEPLOY_OUTPUT = "meta.agent.in"
    TOOL_DEPLOY_ERROR = "tool.deploy.error"
    META_AGENT_INPUT = "meta.agent.in"
    META_AGENT_OUTPUT = "meta.agent.out"
    META_AGENT_ERROR = "meta.agent.error"
    AGENT_DESIGN_INPUT = "agent.design.in"
    AGENT_DESIGN_OUTPUT = "agent.design.out"
    AGENT_DESIGN_OUT = "tool.code.synth"
    AGENT_DESIGN_ERROR = "agent.design.error"
    AGENT_DEPLOY_INPUT = "agent.deploy.in"
    AGENT_DEPLOY_OUTPUT = "agent.deploy.out"
    AGENT_DEPLOY_ERROR = "agent.deploy.error"

    AGENT_ID = "agent"
    TOOL_MEMORY_NAMESPACE = "tool"
    KNOWLEDGE_BASE_MEMORY_NAMESPACE = "knowledge"
    AGENT_MEMORY_NAMESPACE = "agent"
    RESEARCH_API_URL = "http://host.docker.internal:8500/search"
    SHELL_EXEC_API_URL = "http://host.docker.internal:8600/command/run"
    TOOL_API_URL = "http://host.docker.internal:8800/tools/query"

    # Overrides
    run_config_override = None
    init_config_override = None

    IMMUTABLE_FIELDS = {
        "VERSION", "CONFIG_DIR", "DEFAULT_RUN_CONFIG", "DEFAULT_INIT_CONFIG"
    }

    @classmethod
    def ensure_paths(cls):
        # Only needed if you're generating config files dynamically.
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def apply_override(cls, override_path: str):
        path = Path(override_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Override config file not found: {path}")
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in override config: {e}")
        for key, value in data.items():
            if key in cls.IMMUTABLE_FIELDS:
                continue
            if hasattr(cls, key):
                setattr(cls, key, value)
