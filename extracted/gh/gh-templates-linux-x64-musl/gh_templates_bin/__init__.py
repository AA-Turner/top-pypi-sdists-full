import os, sys, subprocess, stat
def main():
    binary = os.path.join(os.path.dirname(__file__), 'gh-templates')
    if not os.path.exists(binary):
        print(f"Error: Binary not found at {binary}")
        sys.exit(1)
    # Ensure binary is executable
    os.chmod(binary, os.stat(binary).st_mode | stat.S_IEXEC)
    sys.exit(subprocess.run([binary] + sys.argv[1:]).returncode)
