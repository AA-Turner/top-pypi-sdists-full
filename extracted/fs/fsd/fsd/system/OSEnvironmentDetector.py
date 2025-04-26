import platform
import os
import subprocess

class OSEnvironmentDetector:
    def __init__(self):
        self.os_data = ""

    def _gather_os_info(self):
        """
        Gathers basic OS information to support AI for dependency installation.
        """
        os_info = {
            "System": platform.system(),
            "Release": platform.release(), 
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Architecture": platform.architecture(),
            "Python Version": platform.python_version(),
            "OS Environment Variables": dict(os.environ),
            "User Home": os.path.expanduser('~'),
        }

        # Add package manager info
        os_info.update({
            "Package Managers": {
                "pip": self._get_version("pip"),
                "npm": self._get_version("npm"),
                "yarn": self._get_version("yarn"),
            },
            "Development Tools": {
                "git": self._get_version("git"),
                "docker": self._get_version("docker"),
            }
        })

        # Remove None values
        os_info["Package Managers"] = {k: v for k, v in os_info["Package Managers"].items() if v is not None}
        os_info["Development Tools"] = {k: v for k, v in os_info["Development Tools"].items() if v is not None}

        return os_info

    def _get_version(self, command):
        """Get version of a command-line tool."""
        try:
            result = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def get_os_info(self):
        """Returns dictionary with OS information."""
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return self.os_data

    def get_all_info(self):
        """Returns all OS information."""
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return self.os_data

    def __str__(self):
        """Returns formatted string of OS information."""
        if self.os_data == "":
            self.os_data = self._gather_os_info()
        return '\n'.join([f'{key}: {value}' for key, value in self.os_data.items()])
