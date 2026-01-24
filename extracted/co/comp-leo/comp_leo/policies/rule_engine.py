"""Policy and rule engine for compliance frameworks."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class RuleEngine:
    """
    Manages compliance rules and policy packs.
    
    Loads rules from JSON definitions and maps them to compliance frameworks
    like NIST 800-53, ISO 27001, PCI-DSS, GDPR, etc.
    """
    
    def __init__(self):
        self.rules: Dict[str, Dict[str, Any]] = {}
        self.policy_packs: Dict[str, Dict[str, Any]] = {}
        self.current_policy_pack: Optional[str] = None
    
    def load_policy_pack(self, pack_name: str) -> None:
        """Load a policy pack by name."""
        pack_file = Path(__file__).parent / f"{pack_name}.json"
        
        if not pack_file.exists():
            # Fall back to aleo-baseline if pack not found
            pack_file = Path(__file__).parent / "aleo-baseline.json"
        
        with open(pack_file, 'r') as f:
            pack_data = json.load(f)
        
        self.policy_packs[pack_name] = pack_data
        self.current_policy_pack = pack_name
        
        # Load rules
        for rule in pack_data.get("rules", []):
            self.rules[rule["id"]] = rule
    
    def get_enabled_rules(self) -> List[Dict[str, Any]]:
        """Get all enabled rules for current policy pack."""
        if not self.current_policy_pack:
            return []
        
        pack = self.policy_packs[self.current_policy_pack]
        enabled_rule_ids = pack.get("enabled_rules", [])
        
        if not enabled_rule_ids:  # If empty, enable all rules
            return list(self.rules.values())
        
        return [self.rules[rid] for rid in enabled_rule_ids if rid in self.rules]
    
    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific rule by ID."""
        return self.rules.get(rule_id)
    
    def get_policy_pack(self, pack_name: str) -> Optional[Dict[str, Any]]:
        """Get policy pack metadata."""
        return self.policy_packs.get(pack_name)
