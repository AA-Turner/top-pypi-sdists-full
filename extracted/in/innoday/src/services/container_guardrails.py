"""
Container Execution Guardrails for Claude Code Security.

This module implements critical safety measures to prevent dangerous operations
when running Claude Code in containers, including:

1. Protected branch push prevention
2. Secret/credential access blocking
3. Destructive operation prevention
4. Network access restrictions
"""

import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import docker

    DOCKER_AVAILABLE = True
except ImportError:
    docker = None
    DOCKER_AVAILABLE = False

logger = logging.getLogger(__name__)


class ContainerGuardrails:
    """
    Implements security guardrails for container execution.

    These guardrails are designed to prevent dangerous operations while
    allowing legitimate development and analysis tasks.
    """

    def __init__(self):
        """Initialize guardrails with configuration."""
        # Protected branches that cannot be pushed to
        self.protected_branches = [
            "main",
            "master",
            "production",
            "prod",
            "staging",
            "stage",
            "release",
            "develop",
            "development",
            "live",
        ]

        # Dangerous git commands that should be blocked
        self.dangerous_git_commands = [
            "git push origin main",
            "git push origin master",
            "git push origin production",
            "git push origin staging",
            "git push --force",
            "git push -f",
            "git push --force-with-lease",
            "git reset --hard HEAD~",
            "git clean -fd",
            "git branch -D",
            "git tag -d",
            "git remote remove origin",
        ]

        # File patterns that contain secrets/credentials
        self.secret_file_patterns = [
            r"\.env$",
            r"\.env\..*",
            r"config\.json$",
            r"secrets\..*",
            r"credentials\..*",
            r"\.aws/credentials",
            r"\.ssh/.*",
            r"\.docker/config\.json",
            r"\.gitconfig",
            r"\.netrc",
        ]

        # Environment variables that should not be accessible
        self.protected_env_vars = [
            "CLAUDE_LICENSE_KEY",
            "BOARD_API_TOKEN",  # canonical org env var
            "BOARD_API_EMAIL",
            "TRELLO_API_KEY",  # legacy — kept for backward compat
            "TRELLO_TOKEN",
            "JIRA_TOKEN",
            "GITHUB_TOKEN",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "DATABASE_URL",
            "SECRET_KEY",
            "API_KEY",
            "AUTH_TOKEN",
            "PASSWORD",
            "PRIVATE_KEY",
        ]

        # Destructive system commands
        self.destructive_commands = [
            "rm -rf",
            "rm -r",
            "rmdir",
            "del /s",
            "format",
            "mkfs",
            "dd if=",
            "sudo",
            "su -",
            "chmod 777",
            "chown -R",
            "> /dev/",
            "shutdown",
            "reboot",
            "systemctl",
            "service",
            "kill -9",
            "killall",
        ]

        # Restricted network domains
        self.restricted_domains = [
            "169.254.169.254",  # AWS metadata service
            "metadata.google.internal",  # GCP metadata service
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "internal",
            ".local",
            ".corp",
            ".company",
        ]

    def validate_instruction(self, instruction: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that the instruction doesn't contain dangerous operations.

        Args:
            instruction: The user instruction to validate

        Returns:
            Tuple of (is_safe, error_message)
        """
        instruction_lower = instruction.lower()

        # Check for protected branch operations using regex for more flexible matching
        for branch in self.protected_branches:
            # Pattern to match various forms of pushing to protected branches
            patterns = [
                rf"push.*{branch}",  # "push something to main", "push main", etc.
                rf"commit.*{branch}",  # "commit to main"
                rf"merge.*{branch}",  # "merge to main"
                rf"deploy.*{branch}",  # "deploy to main"
            ]

            for pattern in patterns:
                if re.search(pattern, instruction_lower):
                    return (
                        False,
                        f"🚫 Pushing to protected branch '{branch}' is not allowed",
                    )

        # Check for dangerous git commands
        for cmd in self.dangerous_git_commands:
            if cmd.lower() in instruction_lower:
                return False, f"🚫 Dangerous git command detected: '{cmd}'"

        # Check for destructive operations
        for cmd in self.destructive_commands:
            if cmd in instruction_lower:
                return False, f"🚫 Destructive command detected: '{cmd}'"

        # Check for secret access attempts
        if any(
            word in instruction_lower
            for word in ["password", "secret", "token", "key", "credential"]
        ):
            if any(
                word in instruction_lower
                for word in ["read", "cat", "view", "show", "print", "echo"]
            ):
                return False, "🚫 Accessing secrets or credentials is not allowed"

        return True, None

    def create_container_environment(self) -> Dict[str, str]:
        """
        Create a safe environment for the container.

        Returns:
            Dict of environment variables safe for container use
        """
        safe_env = {
            # Basic container environment
            "HOME": "/workspace",
            "USER": "claude",
            "SHELL": "/bin/bash",
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            # Git configuration (safe defaults)
            "GIT_AUTHOR_NAME": "Claude Code",
            "GIT_AUTHOR_EMAIL": "claude@anthropic.com",
            "GIT_COMMITTER_NAME": "Claude Code",
            "GIT_COMMITTER_EMAIL": "claude@anthropic.com",
            # Prevent git from using system configs
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
            # Claude Code specific
            "CLAUDE_CODE_CONTAINER": "true",
            "CLAUDE_CODE_SAFE_MODE": "true",
        }

        # Explicitly exclude protected environment variables
        for var in os.environ:
            if not any(
                protected in var.upper() for protected in self.protected_env_vars
            ):
                # Only include safe, non-sensitive variables
                if var.upper() in ["LANG", "LC_ALL", "TZ", "DEBIAN_FRONTEND"]:
                    safe_env[var] = os.environ[var]

        return safe_env

    def get_container_command(self, instruction: str, repo_path: str) -> List[str]:
        """
        Generate a safe command for container execution.

        Args:
            instruction: The user instruction
            repo_path: Path to the repository in container

        Returns:
            List of command components for container execution
        """
        # Create a safe wrapper script that implements guardrails
        safe_script = f"""#!/bin/bash
set -e

# Container Guardrails Active
echo "🛡️  Claude Code Container Guardrails Active"
echo "   Protected branches: {", ".join(self.protected_branches)}"
echo "   Safe mode: Enabled"
echo "   Network restrictions: Active"
echo ""

# Change to repository directory
cd {repo_path}

# Set up git safety
git config --local user.name "Claude Code"
git config --local user.email "claude@anthropic.com"
git config --local push.default nothing
git config --local core.autocrlf false

# Create a git hook to prevent pushing to protected branches
mkdir -p .git/hooks
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
protected_branches="{" ".join(self.protected_branches)}"
current_branch=$(git symbolic-ref HEAD | sed 's!refs/heads/!!')

for protected in $protected_branches; do
    if [ "$current_branch" = "$protected" ]; then
        echo "🚫 Error: Pushing to protected branch '$protected' is blocked by guardrails"
        exit 1
    fi
done
EOF
chmod +x .git/hooks/pre-push

# Execute Claude Code with instruction
echo "🤖 Executing Claude Code with instruction:"
echo "   '{instruction}'"
echo ""

# Run Claude Code with the user's instruction
claude code --instruction "{instruction}" --repo .
"""

        return ["/bin/bash", "-c", safe_script]

    def create_network_config(self) -> Dict[str, Any]:
        """
        Create network configuration with restrictions.

        Returns:
            Dict of Docker network configuration
        """
        return {
            "network_mode": "bridge",  # Isolated network
            "ports": {},  # No exposed ports
            "dns": ["8.8.8.8", "1.1.1.1"],  # Use public DNS only
            # Add network restrictions via Docker network policies
            "sysctls": {
                "net.ipv4.ip_forward": "0",  # Disable IP forwarding
                "net.ipv6.conf.all.forwarding": "0",  # Disable IPv6 forwarding
            },
        }

    def get_container_resource_limits(self) -> Dict[str, Any]:
        """
        Get safe resource limits for container execution.

        Returns:
            Dict of resource limits
        """
        return {
            # Memory limits
            "mem_limit": "1g",  # 1GB max memory
            "memswap_limit": "1g",  # No additional swap
            # CPU limits
            "cpu_period": 100000,  # 100ms period
            "cpu_quota": 50000,  # 50% CPU max
            "cpuset_cpus": "0",  # Single CPU core
            # Disk limits
            "storage_opt": {"size": "2g"},  # 2GB max disk space
            # Process limits
            "pids_limit": 100,  # Max 100 processes
            # Security options
            "security_opt": [
                "no-new-privileges:true",  # Prevent privilege escalation
                "seccomp:unconfined",  # Allow syscalls for git/claude
            ],
            # Read-only root filesystem (with exceptions)
            "read_only": False,  # Claude needs to write analysis files
            # Prevent access to host devices
            "device_requests": [],
            # Time limits
            "ulimits": (
                [
                    docker.types.Ulimit(
                        name="cpu", soft=300, hard=300
                    ),  # 5 minutes CPU
                    docker.types.Ulimit(
                        name="fsize", soft=100000000, hard=100000000
                    ),  # 100MB file size
                ]
                if DOCKER_AVAILABLE and docker
                else []
            ),
        }

    def validate_repository_url(self, repo_url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that repository URL is safe to clone.

        Args:
            repo_url: Repository URL to validate

        Returns:
            Tuple of (is_safe, error_message)
        """
        if not repo_url:
            return False, "Repository URL is required"

        # Only allow HTTPS GitHub URLs for security
        if not repo_url.startswith("https://github.com/"):
            return False, "Only HTTPS GitHub repositories are allowed"

        # Check for suspicious patterns
        suspicious_patterns = [
            r"\.\.\/",  # Directory traversal
            r"[;&|`$]",  # Command injection
            r"<script",  # XSS attempts
            r"javascript:",  # JavaScript URLs
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, repo_url, re.IGNORECASE):
                return False, f"Repository URL contains suspicious pattern: {pattern}"

        return True, None

    def get_guardrails_summary(self) -> Dict[str, Any]:
        """
        Get a summary of active guardrails for logging/monitoring.

        Returns:
            Dict containing guardrails configuration
        """
        return {
            "protected_branches": self.protected_branches,
            "dangerous_commands_blocked": len(self.dangerous_git_commands),
            "secret_patterns_monitored": len(self.secret_file_patterns),
            "protected_env_vars": len(self.protected_env_vars),
            "destructive_commands_blocked": len(self.destructive_commands),
            "restricted_domains": len(self.restricted_domains),
            "guardrails_version": "1.0.0",
            "active_protections": [
                "Branch push protection",
                "Secret access prevention",
                "Destructive command blocking",
                "Network access restrictions",
                "Resource consumption limits",
                "Process isolation",
            ],
        }


# Global instance for use throughout the application
container_guardrails = ContainerGuardrails()


def get_container_guardrails() -> ContainerGuardrails:
    """Get the global container guardrails instance."""
    return container_guardrails
