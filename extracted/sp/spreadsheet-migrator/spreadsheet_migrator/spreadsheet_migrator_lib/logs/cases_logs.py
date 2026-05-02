from typing import Dict, List, Any


class CasesLogs:
    def __init__(self):
        self.created: Dict[int, Dict] = {}
        self.found: Dict[int, Dict] = {}
        self.lack_data: List[Dict[str, Any]] = []
