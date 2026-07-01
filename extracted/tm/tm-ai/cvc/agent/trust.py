import json
from pathlib import Path

def is_workspace_trusted(workspace: Path) -> bool:
    trust_file = Path.home() / ".cvc" / "trusted_workspaces.json"
    if not trust_file.exists():
        return False
    try:
        data = json.loads(trust_file.read_text(encoding="utf-8"))
        return str(workspace.resolve()) in data
    except:
        return False

def trust_workspace(workspace: Path) -> None:
    trust_file = Path.home() / ".cvc" / "trusted_workspaces.json"
    data = []
    if trust_file.exists():
        try:
            data = json.loads(trust_file.read_text(encoding="utf-8"))
        except:
            pass
    ws_str = str(workspace.resolve())
    if ws_str not in data:
        data.append(ws_str)
        try:
            trust_file.parent.mkdir(parents=True, exist_ok=True)
            trust_file.write_text(json.dumps(data), encoding="utf-8")
        except:
            pass
