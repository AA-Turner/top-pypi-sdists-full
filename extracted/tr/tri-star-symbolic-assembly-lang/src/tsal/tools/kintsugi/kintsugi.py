from pathlib import Path
from tsal.tools.brian.optimizer import analyze_and_repair

def kintsugi_repair(file_path: str) -> list[str]:
    """Run repair, and label damage as unique evolution."""
    try:
        output = analyze_and_repair(file_path, repair=True)
        if output:
            return [f"✨ [r]evolution vector: {line}" for line in output]
        return ["✅ Already coherent."]
    except Exception as e:
        return [
            f"💀 Damage recognized: {e}",
            "⚡ Marking as potential Kintsugi Vector.",
        ]
