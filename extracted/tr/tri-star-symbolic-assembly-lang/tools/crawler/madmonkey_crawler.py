from pathlib import Path
from tsal.core.spiral_vector import SpiralVector
from tsal.tools.brian.optimizer import analyze_and_repair


def crawl_and_inject_to_madmonkey(base="src/tsal", repair=False):
    results = []
    for file in Path(base).rglob("*.py"):
        print(f"🐒 Crawling: {file}")
        try:
            output = analyze_and_repair(str(file), repair=repair)
            results.append((str(file), output))
        except Exception as e:
            results.append((str(file), f"💀 ANTISPIRAL: {e}"))
    return results
