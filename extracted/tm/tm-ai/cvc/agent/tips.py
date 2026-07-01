import json
import random
from pathlib import Path
from rich.text import Text

TIPS = [
    "Use [bold]/help[/bold] to see all available slash commands.",
    "Try [bold]/context show[/bold] to see your current memory context.",
    "Use [bold]/commit[/bold] to forcefully checkpoint your work into the CVC graph.",
    "Run [bold]/branch my-feature[/bold] to switch contexts cleanly without losing memory.",
    "Use [bold]/timeline[/bold] to travel back to previous thoughts and checkpoints.",
    "If you made a mistake, use [bold]/undo[/bold] to revert the AI's last action.",
    "You can drop files directly into the prompt using [bold]/add file.py[/bold].",
    "Switch LLM providers instantly using [bold]/model provider/model_id[/bold].",
    "Check your system usage with [bold]/stats[/bold].",
    "Set autopilot mode using [bold]/autopilot[/bold] for unattended coding.",
    "Use [bold]/search[/bold] to find previous thoughts and code blocks in your memory.",
    "Type [bold]/export[/bold] to save your CVC session context into a Markdown file."
]

def get_next_tip() -> str:
    tips_file = Path.home() / ".cvc" / "seen_tips.json"
    
    seen = []
    if tips_file.exists():
        try:
            seen = json.loads(tips_file.read_text(encoding="utf-8"))
        except:
            pass
            
    unseen_tips = [t for t in TIPS if t not in seen]
    
    if not unseen_tips:
        # Reset if all seen
        unseen_tips = TIPS
        seen = []
        
    tip = random.choice(unseen_tips)
    seen.append(tip)
    
    try:
        tips_file.parent.mkdir(parents=True, exist_ok=True)
        tips_file.write_text(json.dumps(seen), encoding="utf-8")
    except:
        pass
        
    return tip
