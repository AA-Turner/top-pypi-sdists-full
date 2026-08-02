"""Install the native Pysae Codex plugin (skills + MCP marketplace) as a Tool.

Registry entry point: exposes the ``tool`` instance the meta-installer manages
(``pysae-ai-tools tools install codex-plugin``). The deployment logic and the
state/install/configure/uninstall skeleton live in the assistant-parameterized
:class:`~.common.skills_deploy.SkillsDeployTool`.
"""

from .common.assistants import CODEX
from .common.skills_deploy import SkillsDeployTool

tool = SkillsDeployTool(CODEX, "codex-plugin")
