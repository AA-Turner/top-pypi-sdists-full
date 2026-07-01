"""
cvc.operations.cognitive_hooks — Wiring harness for advanced cognitive features.

This module connects the advanced features (F1–F10) into the CVCEngine's
lifecycle as post-commit callbacks, session-start/stop actions, and
periodic triggers.

Integration points:
  - post_commit:     F1 (CCLE), F2 (Skill Extraction check), F8 (Skill Graph)
  - session_start:   F3 (User Model injection), F7 (Predictive Preloader)
  - session_stop:    F3 (User Model update), F4 (Prompt Evolution check),
                     F5 (Dreaming trigger), F10 (Metacognition persist)
  - post_tool_use:   F10 (Metacognitive Monitor tick)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cvc.adapters.base import BaseAdapter
    from cvc.operations.engine import CVCEngine

logger = logging.getLogger("cvc.operations.cognitive_hooks")


class CognitiveHookManager:
    """
    Lifecycle manager for advanced cognitive features.

    Instantiated once per session, attaches to the CVCEngine and fires
    feature modules at the appropriate times.
    """

    def __init__(
        self,
        engine: CVCEngine,
        adapter: BaseAdapter | None = None,
        original_goal: str = "",
    ) -> None:
        self.engine = engine
        self.adapter = adapter
        self.cvc_root = engine.config.cvc_root
        self._commit_count = 0

        # Lazy-init feature modules (only created when first needed)
        self._learning_extractor: Any = None
        self._skill_extractor: Any = None
        self._user_model: Any = None
        self._prompt_evolution: Any = None
        self._dreaming: Any = None
        self._skill_graph: Any = None
        self._predictive_loader: Any = None
        self._metacognitive_monitor: Any = None

        # Init metacognitive monitor eagerly (it tracks from the start)
        if original_goal:
            self._init_metacognition(original_goal)

    # -- Lazy initializers -------------------------------------------------

    def _get_learning_extractor(self) -> Any:
        if self._learning_extractor is None:
            try:
                from cvc.core.learning_extractor import CognitiveLearnExtractor

                self._learning_extractor = CognitiveLearnExtractor(self.cvc_root)
            except Exception as e:
                logger.debug("CCLE not available: %s", e)
        return self._learning_extractor

    def _get_skill_extractor(self) -> Any:
        if self._skill_extractor is None:
            try:
                from cvc.operations.skill_extractor import SkillExtractor

                self._skill_extractor = SkillExtractor(self.cvc_root)
            except Exception as e:
                logger.debug("SkillExtractor not available: %s", e)
        return self._skill_extractor

    def _get_user_model(self) -> Any:
        if self._user_model is None:
            try:
                from cvc.core.user_model import UserModelManager

                self._user_model = UserModelManager(self.cvc_root)
            except Exception as e:
                logger.debug("UserModelManager not available: %s", e)
        return self._user_model

    def _get_prompt_evolution(self) -> Any:
        if self._prompt_evolution is None:
            try:
                from cvc.operations.prompt_evolution import PromptEvolutionEngine

                self._prompt_evolution = PromptEvolutionEngine(self.cvc_root)
            except Exception as e:
                logger.debug("PromptEvolutionEngine not available: %s", e)
        return self._prompt_evolution

    def _get_dreaming(self) -> Any:
        if self._dreaming is None:
            try:
                from cvc.operations.dreaming import DreamingEngine

                self._dreaming = DreamingEngine(self.cvc_root)
            except Exception as e:
                logger.debug("DreamingEngine not available: %s", e)
        return self._dreaming

    def _get_skill_graph(self) -> Any:
        if self._skill_graph is None:
            try:
                from cvc.core.skill_graph import CausalSkillGraph

                self._skill_graph = CausalSkillGraph(self.cvc_root)
            except Exception as e:
                logger.debug("CausalSkillGraph not available: %s", e)
        return self._skill_graph

    def _get_predictive_loader(self) -> Any:
        if self._predictive_loader is None:
            try:
                from cvc.agent.predictive_loader import PredictiveContextPreloader

                self._predictive_loader = PredictiveContextPreloader(self.cvc_root)
            except Exception as e:
                logger.debug("PredictiveContextPreloader not available: %s", e)
        return self._predictive_loader

    def _init_metacognition(self, original_goal: str) -> None:
        try:
            from cvc.agent.metacognition import MetacognitiveMonitor

            self._metacognitive_monitor = MetacognitiveMonitor(
                original_goal=original_goal,
                cvc_root=self.cvc_root,
            )
        except Exception as e:
            logger.debug("MetacognitiveMonitor not available: %s", e)

    # ======================================================================
    # Lifecycle hooks
    # ======================================================================

    async def on_session_start(self) -> dict[str, str]:
        """
        Called at the beginning of a session.

        Returns a dict of context injections (key → text) that the agent
        should prepend to the system prompt.
        """
        injections: dict[str, str] = {}

        # F3: User Model — inject personality/preference context
        um = self._get_user_model()
        if um:
            try:
                model = um.load_current_model()
                # V1: technical preferences (coding style, tools)
                injection = um.get_system_prompt_injection(model)
                if injection:
                    injections["user_model"] = injection
                # V2: soul narrative — identity, values, people, emotional tone.
                # This is what makes a brain transplant (switching LLMs) feel
                # continuous. The new brain immediately knows who it's working
                # with — not just their tool preferences, but their essence.
                soul = um.get_soul_narrative(model)
                if soul:
                    injections["soul"] = soul
            except Exception as e:
                logger.debug("User model injection failed: %s", e)

        # F7: Predictive Preloader — inject predicted context
        pl = self._get_predictive_loader()
        if pl:
            try:
                commits = self.engine.db.index.list_commits(limit=50)
                pl.analyze_commits(commits)
                predicted = pl.predict_context()
                if predicted:
                    injections["predictive_context"] = predicted
            except Exception as e:
                logger.debug("Predictive loading failed: %s", e)

        return injections

    async def on_post_commit(
        self,
        commit_hash: str,
        active_skills: list[str] | None = None,
        task_type: str = "general",
        success: bool = True,
    ) -> None:
        """
        Called after each successful commit.

        Runs F1 (learning extraction) and F8 (skill graph update).
        Also checks if F2 (skill auto-extraction) should trigger.
        """
        self._commit_count += 1

        # F1: CCLE — extract learnings from the commit
        if self.adapter:
            extractor = self._get_learning_extractor()
            if extractor:
                try:
                    commit = self.engine.db.index.get_commit(commit_hash)
                    if commit:
                        blob = self.engine.db.retrieve_blob(commit_hash)
                        if blob:
                            prompt = extractor.build_extraction_prompt(commit, blob)
                            from cvc.core.models import ChatCompletionRequest, ChatMessage

                            response = await self.adapter.complete(
                                ChatCompletionRequest(
                                    model=self.engine.config.model,
                                    messages=[ChatMessage(role="user", content=prompt)],
                                    max_tokens=1000,
                                )
                            )
                            if response.choices:
                                extract = extractor.parse_llm_response(
                                    response.choices[0].message.content
                                )
                                extractor.persist_extract(extract, commit_hash)
                except Exception as e:
                    logger.debug("CCLE extraction failed (non-fatal): %s", e)

        # F8: Skill Graph — record outcome
        sg = self._get_skill_graph()
        if sg:
            try:
                sg.record_commit_outcome(
                    active_skills=active_skills or [],
                    task_type=task_type,
                    success=success,
                )
                sg.save()
            except Exception as e:
                logger.debug("Skill graph update failed (non-fatal): %s", e)

        # F2: Skill auto-extraction — check every 10 commits
        if self._commit_count % 10 == 0:
            se = self._get_skill_extractor()
            if se and self.adapter:
                try:
                    extractor = self._get_learning_extractor()
                    if extractor:
                        all_extracts = extractor.load_all_extracts()
                        skills = [s for e in all_extracts for s in e.get("skills", [])]
                        if len(skills) >= 3:
                            clusters = se.find_skill_clusters(skills)
                            for cluster in clusters[:3]:  # Max 3 new skills per trigger
                                prompt = se.build_synthesis_prompt(cluster)
                                from cvc.core.models import (
                                    ChatCompletionRequest,
                                    ChatMessage,
                                )

                                response = await self.adapter.complete(
                                    ChatCompletionRequest(
                                        model=self.engine.config.model,
                                        messages=[ChatMessage(role="user", content=prompt)],
                                        max_tokens=1500,
                                    )
                                )
                                if response.choices:
                                    result = se.parse_synthesis_response(
                                        response.choices[0].message.content
                                    )
                                    if result:
                                        se.generate_skill_file(
                                            result["name"],
                                            result["description"],
                                            result["content"],
                                            result.get("tools", []),
                                        )
                except Exception as e:
                    logger.debug("Skill auto-extraction failed (non-fatal): %s", e)

    async def on_session_stop(self, session_summary: dict[str, Any] | None = None) -> None:
        """
        Called when a session ends.

        Runs F3 (user model update), F4 (prompt evolution check),
        and F10 (metacognition persist).
        """
        # F3: User Model — update from session interactions
        if self.adapter and session_summary:
            um = self._get_user_model()
            if um:
                try:
                    model = um.load_current_model()
                    # ── H2 Heuristic pre-pass ──────────────────────────────
                    # Run cheap deterministic classifiers BEFORE the LLM
                    # call. Guarantees that even if the LLM is down or
                    # the soul-reasoning prompt fails, the soul still
                    # captures emotional context + entity mentions.
                    # The LLM pass below can refine, never overrides.
                    try:
                        from cvc.operations.emotional_classifier import classify_session
                        from cvc.operations.entity_extractor import (
                            extract_from_session,
                            merge_into_snapshot,
                        )
                        from cvc.core.user_model import EmotionalContext
                        msgs = (
                            session_summary.get("messages", [])
                            if isinstance(session_summary, dict)
                            else []
                        )
                        emo_class = classify_session(msgs)
                        if emo_class.mood != "neutral" or emo_class.intensity > 0.1:
                            model.emotional_context.append(
                                EmotionalContext(
                                    mood=emo_class.mood,
                                    intensity=emo_class.intensity,
                                    trigger=emo_class.trigger,
                                    timestamp=__import__("time").time(),
                                )
                            )
                            # Cap at 200 to prevent unbounded growth
                            if len(model.emotional_context) > 200:
                                model.emotional_context = model.emotional_context[-200:]
                            um.save_model(model, trigger="auto_emotion")
                        extracted = extract_from_session(msgs)
                        if extracted:
                            added = merge_into_snapshot(extracted, model)
                            if added:
                                um.save_model(model, trigger="auto_entity")
                    except Exception as heu_exc:
                        logger.debug("H2 heuristic pass failed (non-fatal): %s", heu_exc)
                    # ── Existing LLM-based user model update ────────────────
                    # V1: technical preferences reasoning
                    prompt = um.build_reasoning_prompt(model, session_summary)
                    from cvc.core.models import ChatCompletionRequest, ChatMessage

                    response = await self.adapter.complete(
                        ChatCompletionRequest(
                            model=self.engine.config.model,
                            messages=[ChatMessage(role="user", content=prompt)],
                            max_tokens=800,
                        )
                    )
                    if response.choices:
                        raw_response = response.choices[0].message.content
                        updated = um.apply_reasoning_response(
                            model, raw_response,
                            source_commits=[self.engine.config.model],
                        )
                        # V2: soul-layer reasoning — entities, values,
                        # emotions, temporal facts, life events, narrative.
                        # Uses a SECOND LLM call with the soul prompt so
                        # the model gets both technical + personal updates.
                        # This is the call that makes the soul learn WHO
                        # the user is, not just what tools they use.
                        try:
                            soul_prompt = um.build_soul_reasoning_prompt(
                                updated, session_summary,
                            )
                            soul_response = await self.adapter.complete(
                                ChatCompletionRequest(
                                    model=self.engine.config.model,
                                    messages=[ChatMessage(role="user", content=soul_prompt)],
                                    max_tokens=1000,
                                )
                            )
                            if soul_response.choices:
                                updated = um.apply_soul_reasoning_response(
                                    updated,
                                    soul_response.choices[0].message.content,
                                    source_commits=[self.engine.config.model],
                                )
                        except Exception as soul_exc:
                            logger.debug("Soul reasoning failed (non-fatal): %s", soul_exc)

                        um.save_model(updated)
                except Exception as e:
                    logger.debug("User model update failed (non-fatal): %s", e)

        # F4: Prompt Evolution — check if system prompt should evolve
        pe = self._get_prompt_evolution()
        if pe:
            try:
                commits = self.engine.db.index.list_commits(limit=30)
                metrics = pe.compute_quality_metrics(commits)
                if pe.should_evolve(metrics):
                    logger.info("Prompt evolution triggered — metrics: %s", metrics)
                elif pe.should_revert(metrics):
                    logger.info("Prompt regression detected — reverting to previous variant")
            except Exception as e:
                logger.debug("Prompt evolution check failed (non-fatal): %s", e)

        # F10: Metacognition — persist session snapshots
        if self._metacognitive_monitor:
            try:
                self._metacognitive_monitor.persist_snapshots()
            except Exception as e:
                logger.debug("Metacognition persist failed (non-fatal): %s", e)

    def on_post_tool_use(self, tool_name: str) -> str | None:
        """
        Called after each tool use. Updates the metacognitive monitor.

        Returns an intervention message if the monitor triggers one,
        or None if everything is normal.
        """
        if self._metacognitive_monitor:
            self._metacognitive_monitor.record_tool_call(tool_name)
            # We don't do full LLM assessment here (too expensive per tool call).
            # Instead, just check the counter. The actual assessment is triggered
            # by the agent loop when should_assess() returns True.
            if self._metacognitive_monitor.should_assess():
                return "__METACOGNITION_CHECK__"
        return None

    async def run_metacognitive_check(self, recent_context: str = "") -> str | None:
        """
        Run a full metacognitive assessment (called by agent when flagged).

        Returns an intervention message or None.
        """
        if not self._metacognitive_monitor or not self.adapter:
            return None

        try:
            prompt = self._metacognitive_monitor.build_assessment_prompt(recent_context)
            from cvc.core.models import ChatCompletionRequest, ChatMessage

            response = await self.adapter.complete(
                ChatCompletionRequest(
                    model=self.engine.config.model,
                    messages=[ChatMessage(role="user", content=prompt)],
                    max_tokens=500,
                )
            )
            if response.choices:
                snapshot = self._metacognitive_monitor.parse_assessment_response(
                    response.choices[0].message.content
                )
                self._metacognitive_monitor.record_snapshot(snapshot)
                return self._metacognitive_monitor.get_intervention_message(snapshot)
        except Exception as e:
            logger.debug("Metacognitive check failed (non-fatal): %s", e)

        return None

    async def trigger_dreaming(self) -> str | None:
        """
        Manually trigger the dreaming process (F5).

        Typically called via CLI command or scheduled cron.
        Returns a summary of the dream or None.
        """
        de = self._get_dreaming()
        if not de or not self.adapter:
            return None

        try:
            commits = self.engine.db.index.list_commits(limit=100)
            dream = await de.run_dream_cycle(
                commits=commits,
                adapter=self.adapter,
                model=self.engine.config.model,
            )
            if dream:
                summary = (
                    f"Dream complete: {dream.candidate_count} candidates processed, "
                    f"{len(dream.concept_tags)} concepts, "
                    f"{len(dream.insights)} insights"
                )
                if dream.contradictions:
                    summary += f", {len(dream.contradictions)} contradictions detected"
                logger.info("dreaming: %s", summary)
                return summary
            return "Not enough commits to dream yet (need ≥3)."
        except Exception as e:
            logger.debug("Dreaming failed (non-fatal): %s", e)

        return None

    def get_skill_recommendations(self, task_type: str) -> list[tuple[str, float]]:
        """Get skill recommendations from the causal graph for a task type."""
        sg = self._get_skill_graph()
        if sg:
            return sg.recommend_skills(task_type)
        return []

    def get_capability_summary(self) -> str:
        """Get a natural-language summary of the agent's capabilities."""
        sg = self._get_skill_graph()
        if sg:
            return sg.get_capability_summary()
        return "No capability data available."
