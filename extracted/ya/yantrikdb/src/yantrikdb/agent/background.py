"""Background cognition — periodic think loop, instinct evaluation, urge management."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yantrikdb.agent.companion import CompanionService

log = logging.getLogger("yantrik.background")


class BackgroundCognition:
    """Manages periodic background tasks for the companion."""

    def __init__(self, service: CompanionService):
        self.service = service
        self._think_task: asyncio.Task | None = None
        self._expiry_task: asyncio.Task | None = None
        self._running = False

    async def start(self):
        self._running = True
        self._think_task = asyncio.create_task(self._think_loop())
        self._expiry_task = asyncio.create_task(self._urge_expiry_loop())
        log.info("Background cognition started")

    async def stop(self):
        self._running = False
        for task in (self._think_task, self._expiry_task):
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        log.info("Background cognition stopped")

    def _get_interval(self) -> int:
        """Get think interval based on whether session is active."""
        config = self.service.config.cognition
        idle_secs = time.time() - self.service.last_interaction_ts

        if idle_secs < config.think_interval_active_minutes * 60:
            return config.think_interval_active_minutes * 60
        elif idle_secs < 3600:  # within 1 hour
            return config.think_interval_minutes * 60
        else:
            return config.idle_think_interval_minutes * 60

    async def _think_loop(self):
        # Initial delay — let the service fully start
        await asyncio.sleep(30)

        while self._running:
            interval = self._get_interval()
            await asyncio.sleep(interval)

            if not self._running:
                break

            try:
                await self._run_think_cycle()
            except Exception as e:
                log.error("Think cycle failed: %s", e, exc_info=True)

    async def _run_think_cycle(self):
        log.info("Running background think cycle")
        start = time.time()

        # 1. Run YantrikDB think()
        try:
            think_result = self.service.db.think()
        except Exception as e:
            log.error("YantrikDB think() failed: %s", e)
            think_result = {"triggers": []}

        triggers = think_result.get("triggers", [])

        # 2. Cache triggers for instinct use
        self.service._pending_triggers = triggers

        # 3. Get active patterns
        try:
            patterns = self.service.db.get_patterns(status="active", limit=10)
            self.service._active_patterns = patterns
        except Exception:
            patterns = []

        # 4. Get open conflicts count
        try:
            conflicts = self.service.db.get_conflicts(status="open", limit=100)
            self.service._open_conflicts_count = len(conflicts)
        except Exception:
            pass

        # 5. Extract valence trend from triggers
        for t in triggers:
            if t.get("trigger_type") == "valence_trend":
                ctx = t.get("context", {})
                self.service._recent_valence_avg = ctx.get("recent_avg")

        # 6. Evaluate all instincts
        state = self.service.build_state()
        urge_count = 0
        for instinct in self.service.instincts:
            try:
                specs = instinct.evaluate(state)
                for spec in specs:
                    if self.service.urge_queue.push(spec):
                        urge_count += 1
            except Exception as e:
                log.error("Instinct %s evaluate failed: %s", instinct.name, e)

        # 7. Check reminder-domain memories for due reminders
        await self._check_reminders(state)

        # 8. Check if any urge should trigger proactive message
        threshold = self.service.config.cognition.proactive_urgency_threshold
        proactive_urges = self.service.urge_queue.pop_due(threshold=threshold)
        if proactive_urges:
            await self._generate_proactive_message(proactive_urges)

        duration = time.time() - start
        log.info(
            "Think cycle complete in %.1fs: %d triggers, %d new urges, %d patterns",
            duration, len(triggers), urge_count, len(patterns),
        )

    async def _check_reminders(self, state):
        """Check for reminder-domain memories coming due."""
        try:
            results = self.service.db.recall(
                query="reminder due soon",
                top_k=10,
                domain="reminder",
                skip_reinforce=True,
            )
            now = time.time()
            from yantrikdb.agent.instincts.protocol import UrgeSpec

            for mem in results:
                meta = mem.get("metadata", {})
                if isinstance(meta, str):
                    import json
                    try:
                        meta = json.loads(meta)
                    except (json.JSONDecodeError, TypeError):
                        continue

                remind_at = meta.get("remind_at")
                if remind_at and isinstance(remind_at, (int, float)):
                    time_until = remind_at - now
                    if 0 < time_until < 3600:  # due within 1 hour
                        urgency = max(0.6, 1.0 - (time_until / 3600))
                        self.service.urge_queue.push(UrgeSpec(
                            instinct_name="reminder",
                            reason=f"Reminder: {mem.get('text', '')}",
                            urgency=urgency,
                            context={"memory_rid": mem.get("rid"), "time_until": time_until},
                            cooldown_key=f"reminder:{mem.get('rid', '')}",
                        ))
        except Exception as e:
            log.debug("Reminder check failed: %s", e)

    async def _generate_proactive_message(self, urges: list[dict]):
        """Use LLM to craft a proactive message from high-urgency urges."""
        urge_text = "\n".join(
            f"- {u.get('reason', '')} (urgency: {u.get('urgency', 0):.1f})"
            for u in urges[:3]
        )

        user_name = self.service.config.user_name
        messages = [
            {"role": "system", "content": self.service.config.personality.system_prompt},
            {"role": "system", "content": (
                f"You want to say something proactively to {user_name}. "
                f"These are the things on your mind:\n{urge_text}\n\n"
                "Craft a brief, natural message addressing the most important item. "
                "Keep it under 2 sentences. Be warm but not pushy."
            )},
        ]

        try:
            resp = await self.service.llm.chat(messages, max_tokens=150)
            self.service.proactive_message = {
                "text": resp.content,
                "urge_ids": [u.get("urge_id", "") for u in urges],
                "generated_at": time.time(),
            }
            log.info("Generated proactive message: %s", resp.content[:80])
        except Exception as e:
            log.warning("Proactive message generation failed: %s", e)

    async def _urge_expiry_loop(self):
        """Expire old urges periodically."""
        await asyncio.sleep(300)  # initial 5min delay
        while self._running:
            await asyncio.sleep(3600)  # every hour
            try:
                self.service.urge_queue.expire_old()
            except Exception as e:
                log.warning("Urge expiry failed: %s", e)
