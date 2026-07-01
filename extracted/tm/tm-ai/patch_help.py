import sys
with open("/Users/jkm/projects/cvc/cvc/cli.py", "r") as f:
    content = f.read()

new_cmds = """            ("doctor", "Health check your environment"),
            ("update", "Update CVC to the latest version"),
            ("config set", "Set a configuration value"),
            ("ignore <path>", "Add path to .cvcignore"),
            ("open / ui", "Open CVC dashboard in browser"),
            ("clean", "Purge cache and temporary data"),
            ("uninstall", "Completely remove CVC"),"""

content = content.replace('            ("doctor", "Health check your environment"),', new_cmds)

with open("/Users/jkm/projects/cvc/cvc/cli.py", "w") as f:
    f.write(content)
