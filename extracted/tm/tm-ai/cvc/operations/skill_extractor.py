"""
cvc.operations.skill_extractor — Automatic Skill Extraction from Commit Patterns.

When CCLE detects 3+ similar learning extracts (via pattern clustering),
this module synthesizes a reusable skill.md with full Merkle hash provenance
linking back to the source commits.

Unlike upstream (single-session skill creation), CVC creates skills from
*cross-session patterns* — a skill only materializes after the agent has
demonstrated the pattern repeatedly across multiple commits.

Each generated skill includes:
  - Markdown content with YAML frontmatter (compatible with cvc.agent.skills)
  - Provenance chain: list of source commit hashes that evidenced the pattern
  - Confidence score derived from cluster coherence
  - Auto-invoke regex pattern for prompt matching
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from cvc.core.learning_extractor import LearnedSkill, LearningExtract

logger = logging.getLogger("cvc.skill_extractor")

# Minimum similar extracts needed to trigger skill generation
MIN_CLUSTER_SIZE = 3

# Minimum aggregate confidence to generate a skill
MIN_CONFIDENCE_THRESHOLD = 0.6

# Template for generated skill files
SKILL_TEMPLATE = """\
---
name: {name}
description: {description}
tools: {tools}
auto_invoke: {auto_invoke}
confidence: {confidence:.2f}
source_commits: {source_commits}
generated_at: {timestamp}
extraction_method: ccle_cluster
---

# {title}

{description}

## When to Use

{when_to_use}

## Instructions

{instructions}

## Provenance

This skill was auto-extracted from {commit_count} cognitive commits:
{provenance_list}

Confidence: {confidence:.0%} (based on {cluster_size} similar patterns)
"""

SYNTHESIS_PROMPT = """\
You are a skill synthesis engine. Given multiple learning extracts that share \
a common pattern, synthesize a single reusable skill definition.

## Similar Learning Extracts
{extracts_json}

## Instructions
Create a unified skill from these related patterns. The skill should be:
1. General enough to apply to future similar situations
2. Specific enough to be actionable
3. Include clear trigger conditions (when to use this skill)

Respond with ONLY valid JSON:
{{
  "name": "kebab-case-skill-name",
  "title": "Human Readable Title",
  "description": "One-line description",
  "when_to_use": "Paragraph explaining trigger conditions",
  "instructions": "Step-by-step instructions for the agent",
  "tools": ["list", "of", "relevant", "tool", "names"],
  "auto_invoke": ["regex_pattern_1", "regex_pattern_2"],
  "confidence": 0.0
}}
"""


class SkillExtractor:
    """
    Monitors learning extracts and auto-generates skills when patterns cluster.

    Works with the existing cvc.agent.skills framework — generated skills
    are saved to .cvc/skills/ in the standard YAML frontmatter format.
    """

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self.skills_dir = cvc_root / "skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self._generated_skills_index = cvc_root / "skills" / "_generated_index.json"

    def find_skill_clusters(
        self,
        extracts: list[LearningExtract],
    ) -> list[list[LearnedSkill]]:
        """
        Group similar learned skills across extracts by name similarity.

        Uses simple keyword overlap for clustering (no external ML dependency).
        For ChromaDB-based semantic clustering, use find_skill_clusters_semantic().
        """
        # Collect all skills from all extracts
        all_skills: list[tuple[LearnedSkill, str]] = []  # (skill, extract_id)
        for ext in extracts:
            for skill in ext.skills:
                all_skills.append((skill, ext.extract_id))

        if not all_skills:
            return []

        # Simple keyword-based clustering
        clusters: list[list[LearnedSkill]] = []
        used: set[int] = set()

        for i, (skill_a, _) in enumerate(all_skills):
            if i in used:
                continue
            cluster = [skill_a]
            used.add(i)
            keywords_a = set(skill_a.name.lower().replace("-", " ").split())
            keywords_a |= set(skill_a.description.lower().split()[:10])

            for j, (skill_b, _) in enumerate(all_skills):
                if j in used:
                    continue
                keywords_b = set(skill_b.name.lower().replace("-", " ").split())
                keywords_b |= set(skill_b.description.lower().split()[:10])
                overlap = len(keywords_a & keywords_b)
                total = len(keywords_a | keywords_b)
                if total > 0 and overlap / total >= 0.3:  # Jaccard ≥ 0.3
                    cluster.append(skill_b)
                    used.add(j)

            if len(cluster) >= MIN_CLUSTER_SIZE:
                clusters.append(cluster)

        return clusters

    def build_synthesis_prompt(self, cluster: list[LearnedSkill]) -> str:
        """Build the LLM prompt for skill synthesis from a cluster."""
        extracts_data = []
        for skill in cluster:
            extracts_data.append(
                {
                    "name": skill.name,
                    "description": skill.description,
                    "trigger_pattern": skill.trigger_pattern,
                    "confidence": skill.confidence,
                    "source_commits": skill.source_commits,
                }
            )

        return SYNTHESIS_PROMPT.format(extracts_json=json.dumps(extracts_data, indent=2))

    def parse_synthesis_response(self, response_text: str) -> dict[str, Any] | None:
        """Parse the LLM synthesis response."""
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse skill synthesis response")
            return None

    def generate_skill_file(
        self,
        synthesis: dict[str, Any],
        cluster: list[LearnedSkill],
    ) -> Path | None:
        """
        Write a skill.md file from a synthesis result.

        Returns the path to the created skill file, or None on failure.
        """
        name = synthesis.get("name", "unnamed-skill")

        # Check if skill already exists
        skill_dir = self.skills_dir / name
        if skill_dir.exists():
            logger.info("Skill '%s' already exists, skipping generation", name)
            return None

        # Collect all source commits from the cluster
        all_commits: list[str] = []
        for skill in cluster:
            all_commits.extend(skill.source_commits)
        unique_commits = list(dict.fromkeys(all_commits))  # Deduplicate, preserve order

        # Build the skill file
        tools_list = synthesis.get("tools", [])
        auto_invoke = synthesis.get("auto_invoke", [])

        content = SKILL_TEMPLATE.format(
            name=name,
            title=synthesis.get("title", name),
            description=synthesis.get("description", ""),
            tools=json.dumps(tools_list),
            auto_invoke=json.dumps(auto_invoke),
            confidence=float(synthesis.get("confidence", 0.5)),
            source_commits=json.dumps(unique_commits[:10]),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            when_to_use=synthesis.get("when_to_use", ""),
            instructions=synthesis.get("instructions", ""),
            commit_count=len(unique_commits),
            provenance_list="\n".join(f"- `{h[:12]}`" for h in unique_commits[:10]),
            cluster_size=len(cluster),
        )

        # Write to .cvc/skills/<name>/skill.md
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_path = skill_dir / "skill.md"
        skill_path.write_text(content, encoding="utf-8")

        # Update the generated skills index
        self._update_index(name, unique_commits, float(synthesis.get("confidence", 0.5)))

        logger.info(
            "Generated skill '%s' from %d patterns across %d commits",
            name,
            len(cluster),
            len(unique_commits),
        )
        return skill_path

    def _update_index(self, name: str, source_commits: list[str], confidence: float) -> None:
        """Track generated skills in an index for deduplication."""
        index: list[dict[str, Any]] = []
        if self._generated_skills_index.exists():
            try:
                index = json.loads(self._generated_skills_index.read_text(encoding="utf-8"))
            except Exception:
                index = []

        index.append(
            {
                "name": name,
                "source_commits": source_commits[:10],
                "confidence": confidence,
                "generated_at": time.time(),
            }
        )

        self._generated_skills_index.write_text(
            json.dumps(index, indent=2),
            encoding="utf-8",
        )

    def get_generated_skill_names(self) -> set[str]:
        """Return names of all previously generated skills."""
        if not self._generated_skills_index.exists():
            return set()
        try:
            index = json.loads(self._generated_skills_index.read_text(encoding="utf-8"))
            return {entry["name"] for entry in index}
        except Exception:
            return set()
