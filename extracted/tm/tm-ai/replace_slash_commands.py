import re

file_path = "/Users/jkm/Projects/cvc/cvc/agent/renderer.py"
with open(file_path, "r") as f:
    content = f.read()

commands = [
    "/add-dir", "/agent", "/agents", "/allowed-tools", "/analytics", "/autopilot",
    "/branch", "/branches", "/cd", "/checkout", "/clear", "/commit", "/compact",
    "/config", "/context", "/continue", "/copy", "/cost", "/diff", "/docsearch",
    "/doctor", "/documents", "/exit", "/export", "/fast", "/files", "/fork", "/git",
    "/health", "/help", "/hive", "/hooks", "/image", "/ingest", "/init", "/init-rules",
    "/log", "/memory", "/merge", "/model", "/new", "/paste", "/permissions", "/plan",
    "/plan-mode", "/provider", "/quit", "/release-notes", "/rename", "/restore",
    "/retry", "/rewind", "/search", "/serve", "/sessions", "/settings", "/skills",
    "/smartsearch", "/stats", "/status", "/summary", "/tasks", "/think", "/trust",
    "/undo", "/web", "/plugins", "/q", "/perms", "/allowedtools", "/effort", "/skill", "/plugin"
]

commands = sorted(list(set(commands)))

formatted_lines = []
current_line = "    "
for cmd in commands:
    cmd_str = f'"{cmd}", '
    if len(current_line) + len(cmd_str) > 80:
        formatted_lines.append(current_line.rstrip())
        current_line = "    " + cmd_str
    else:
        current_line += cmd_str
if current_line.strip():
    formatted_lines.append(current_line.rstrip())

list_str = "SLASH_COMMANDS = [\n" + "\n".join(formatted_lines) + "\n]"

pattern = r"SLASH_COMMANDS\s*=\s*\[(.*?)\]"

new_content = re.sub(pattern, list_str, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(new_content)

print("Updated SLASH_COMMANDS")
