from typing import override

from bir_mcp.git_lab.prompts import get_prompts
from bir_mcp.git_lab.sonarqube import SonarQube
from bir_mcp.git_lab.tools import GitLabTools


class GitLab(GitLabTools):
    @override
    def get_prompts(self):
        return get_prompts()
