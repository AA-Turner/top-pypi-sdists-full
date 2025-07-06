import json
from typing import List, Tuple, Dict, Optional
from importlib import resources

def tokenize_to_flowchart(
    source_lines: List[str], schema_path: Optional[str] = None
) -> Tuple[List[Dict], List[Dict]]:
    """Turns code into flowchart nodes using language schema."""
    if schema_path is None:
        schema_file = resources.files("tsal.schemas").joinpath("python.json")
        ops = json.loads(schema_file.read_text())["ops"]
    else:
        with open(schema_path) as f:
            ops = json.load(f)["ops"]
    triggers = {op["keyword"]: op for op in ops}
    nodes: List[Dict] = []
    edges: List[Dict] = []
    for i, line in enumerate(source_lines):
        tokens = line.strip().split()
        if tokens and tokens[0] in triggers:
            nodes.append({"id": i, "type": tokens[0], "raw": line})
            if len(nodes) > 1:
                edges.append({"from": nodes[-2]["id"], "to": nodes[-1]["id"]})
    return nodes, edges
