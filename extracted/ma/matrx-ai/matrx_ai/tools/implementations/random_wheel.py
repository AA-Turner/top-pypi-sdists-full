"""``random_wheel`` — a true-random entropy-injection tool.

Why this exists (it is not a toy): an LLM with a fixed-ish starting context
converges — same priors, same attractors, same answers. This tool deliberately
perturbs the starting point with entropy the model cannot fake:

* a **cryptographically true-random** pick (``matrx_utils.secure_random``, backed by
  ``os.urandom`` — non-seedable, non-reproducible) over a labeled set, forcing the
  model onto a branch it would not have chosen, and
* optionally **fresh external content** (a random phrase → recent web search, or a
  random word → a real stock image) the model has never seen, dropped into context
  before it answers.

The pick is the engine; *what you do with the pick* is a swappable RESOLVER
(``register_resolver``). v1 ships ``list`` (pure pick), ``web`` (recent search) and
``image`` (Unsplash). Adding ``wikipedia`` / ``number`` / etc. is one registration.

Streaming choreography (the frontend renders a spinning wheel):
1. compute display candidates + the winning index + a randomized spin duration,
2. emit a ``spin`` step event carrying all three so the FE can animate deterministically,
3. ``asyncio.sleep`` for the spin duration (the dramatize delay) — running any
   resolver fetch CONCURRENTLY — then return. The model only ever sees the returned
   ``output``; the spin duration is also the gate that keeps the result from reaching
   the model before the animation lands.
"""
from __future__ import annotations

import asyncio
import time
import traceback
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import secure_choice, secure_randint, secure_sample, vcprint

from matrx_ai.tools.kinds.wheel import WheelChoice, WheelImage, WheelSpinResult
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.streaming import ToolStreamManager

# ── Tuning constants (CAPS — change behavior with a code push, never an env flag) ──
SPIN_MIN_MS = 1500
SPIN_MAX_MS = 4000
DEFAULT_DISPLAY = 18
MAX_DISPLAY = 28
WEB_FRESHNESS_DEFAULT = "pw"  # Brave "past week" — fresh by default
WEB_RESULTS = 6
IMAGE_PER_PAGE = 8

DEFAULT_TITLES = {
    "list": "Spin the wheel",
    "web": "Spin for a fresh angle",
    "image": "Spin for an image",
}

# ── Built-in entropy pools — let a bare/argument-light call still delight ──────
# Curated for DIVERSITY (the whole point is to scatter the starting point).
IDEA_TOPICS: tuple[str, ...] = (
    "A constraint you've never tried", "The opposite of the obvious answer",
    "What a curious 8-year-old would ask", "A lesson from nature",
    "Something from a totally different field", "The version with zero budget",
    "The version with unlimited budget", "What would break this?",
    "Who is this NOT for?", "The 10-years-from-now take",
    "A historical parallel", "The contrarian view",
    "What if it had to be tiny?", "What if it had to be enormous?",
    "Remove the most important part", "Combine it with its rival",
    "Explain it as a story", "Explain it as a recipe",
    "The ethical edge case", "The laziest possible solution",
    "A first-principles rebuild", "What a skeptic would say",
    "The emotional angle", "The data angle",
    "What everyone is too polite to mention", "The five-minute version",
    "The luxury version", "The open-source version",
    "What would surprise an expert", "The cross-cultural take",
)
WEB_PHRASES: tuple[str, ...] = (
    "surprising recent discoveries", "unexpected breakthroughs this week",
    "weird news today", "counterintuitive research findings",
    "emerging trends people are missing", "strange but true recent events",
    "underrated tools released recently", "what changed this week",
    "recent design experiments", "fascinating data released recently",
    "overlooked science stories", "recent surprising statistics",
    "new ideas gaining traction", "things that got cheaper recently",
    "recent failures worth learning from", "quietly important news",
    "recent creative collaborations", "what experts changed their mind about",
    "recent unusual inventions", "stories that should be bigger",
)
IMAGE_WORDS: tuple[str, ...] = (
    "bioluminescence", "brutalist architecture", "desert at dawn",
    "vintage typewriter", "northern lights", "tide pools",
    "neon signs at night", "ancient library", "foggy forest",
    "street market", "geometric staircase", "coral reef",
    "old world map", "rainy city window", "wildflower meadow",
    "abandoned factory", "spiral galaxy", "hot air balloons",
    "japanese garden", "stormy ocean", "cobblestone alley",
    "mountain reflection", "macro of a leaf", "lantern festival",
    "snow-covered pines", "mid-century interior", "salt flats",
    "graffiti wall", "lighthouse at dusk", "origami",
)

# A big, deliberately diverse pool of GENERATIVE topics — each one a springboard a
# show-off agent can build a whole gallery around (flashcards, quiz, diagram,
# recipe, timeline, chart…). The wheel samples a handful to display, so it feels
# fresh every spin. Add a pool via register_pool(...) — never hard-code a list at a
# call site.
SHOWCASE_TOPICS: tuple[str, ...] = (
    # Science & nature
    "Bioluminescent deep-sea life", "How the immune system works", "Photosynthesis",
    "The water cycle", "Plate tectonics", "The secret life of honeybees",
    "Coral reefs", "The human brain", "DNA and genetics", "The periodic table",
    "Quantum entanglement", "The physics of light", "How weather works",
    "Volcanoes", "Earthquakes", "The deep ocean", "Bird migration",
    "The fungi kingdom", "Symbiosis in nature", "The carbon cycle",
    "The science of sleep", "Caffeine", "The science of taste",
    "How sound works", "Magnetism", "Fractals in nature", "The Fibonacci sequence",
    "Crystals and minerals", "The science of fire", "Glaciers",
    # Space
    "Black holes", "Mars exploration", "The Moon landings", "The solar system",
    "Exoplanets", "The life cycle of a star", "Galaxies", "The Big Bang",
    "Comets and asteroids", "The Voyager probes", "Dark matter",
    "The northern lights", "Telescopes through history", "The search for alien life",
    "Living on the Space Station",
    # History & civilization
    "The Silk Road", "Ancient Egypt", "The Roman Empire", "The Renaissance",
    "The printing press", "The Industrial Revolution", "The Library of Alexandria",
    "The Maya civilization", "Viking voyages", "The Age of Exploration",
    "The history of money", "The history of writing", "Ancient Greek philosophy",
    "The Great Wall of China", "Samurai culture", "The history of medicine",
    "Women who changed science", "The space race", "The history of the internet",
    "Lost cities of the world",
    # Art & culture
    "The history of jazz", "Impressionist painting", "Street art and graffiti",
    "The architecture of cathedrals", "Origami", "The Japanese tea ceremony",
    "The evolution of cinema", "Greek mythology", "World folktales",
    "The history of photography", "Typography and fonts", "Color theory",
    "Dance around the world", "How an orchestra works", "The history of hip-hop",
    "Video game design", "The art of animation", "The craft of storytelling",
    "Famous heists", "The Beatles",
    # Food & drink
    "The science of fermentation", "The history of chocolate", "Coffee around the world",
    "The art of bread", "The spice trade", "Sushi", "How cheese is made",
    "Tea cultures of the world", "Street food around the globe",
    "The chemistry of cooking", "Hot peppers and capsaicin", "Honey",
    "The history of pizza", "Molecular gastronomy", "The world of wine",
    # Tech & engineering
    "How artificial intelligence works", "How the internet works", "Cryptography",
    "Robotics", "Renewable energy", "The history of computing", "Electric vehicles",
    "3D printing", "Virtual reality", "How GPS works", "The history of flight",
    "How bridges stay up", "Skyscrapers", "Self-driving cars", "How batteries work",
    # Mind & body
    "The psychology of habits", "How memory works", "Optical illusions",
    "The science of emotions", "Body language", "The science of happiness",
    "How we make decisions", "The roots of creativity", "Dreams",
    "The placebo effect", "Mindfulness", "The science of exercise", "Longevity",
    "Why we procrastinate", "The psychology of color",
    # Animals & plants
    "Octopus intelligence", "Monarch butterfly migration", "Wolves and the pack",
    "The secret life of trees", "Elephants", "Dolphins", "Ants and their colonies",
    "Penguins", "Sharks", "The world of insects", "Carnivorous plants",
    "Giant sequoias", "Why birds sing", "Animal camouflage", "Slowest vs fastest animals",
    # Earth & places
    "The Amazon rainforest", "Antarctica", "The Sahara", "The Himalayas",
    "The Great Barrier Reef", "Iceland's geology", "The world's great rivers",
    "Caves and caverns", "National parks", "How climate is changing",
    # Fun & curious
    "The history of board games", "The mathematics of music", "Secret codes and ciphers",
    "Famous unsolved mysteries", "The physics of roller coasters", "How magic tricks work",
    "The science of fireworks", "The world of perfume", "The history of toys",
    "How we measure time", "Maps and cartography", "Luck and probability",
    "The art of negotiation", "The psychology of first impressions",
)

# Named built-in pools — the extension point. A new themed wheel is one
# register_pool(...) call (mirrors register_resolver for modes).
_POOLS: dict[str, tuple[str, ...]] = {}


def register_pool(name: str, topics: tuple[str, ...]) -> None:
    _POOLS[name.strip().lower()] = topics


register_pool("ideas", IDEA_TOPICS)
register_pool("showcase", SHOWCASE_TOPICS)


def _resolve_pool(name: str | None) -> tuple[str, ...]:
    """Pick a built-in pool by name; default to the brainstorming idea wheel.
    Unknown names fall back to ideas rather than erroring."""
    if not name:
        return IDEA_TOPICS
    return _POOLS.get(name.strip().lower(), IDEA_TOPICS)


@dataclass
class SeedResolution:
    """The output of a resolver: what a chosen seed turned into."""

    value: Any
    sources: list[dict[str, Any]] | None = None
    image: dict[str, Any] | None = None


Resolver = Callable[[str, "WheelPlan", ToolContext, ToolStreamManager], Awaitable[SeedResolution]]
_RESOLVERS: dict[str, Resolver] = {}


def register_resolver(mode: str, fn: Resolver) -> None:
    """Register the resolver that turns a chosen seed into a value for ``mode``.

    The platform extension point: a new wheel capability (e.g. a Wikipedia or
    number-range resolver) is one ``register_resolver(...)`` call plus a seed pool
    in ``_seed_pool`` — never a new tool or router.
    """
    _RESOLVERS[mode] = fn


@dataclass
class WheelPlan:
    mode: str
    title: str
    candidates: list[str]
    winner_index: int
    pool_size: int
    spin_ms: int
    # list mode resolves locally; web/image carry a seed + a resolver.
    chosen_value: Any = None
    seed: str | None = None
    freshness: str | None = None
    avoid: list[str] = field(default_factory=list)

    @property
    def winner_label(self) -> str:
        return self.candidates[self.winner_index]


def _normalize_items(items: list[Any]) -> list[dict[str, Any]]:
    """Accept ``{label, value?}`` dicts (or bare strings) → ``[{label, value}]``."""
    out: list[dict[str, Any]] = []
    for it in items:
        if isinstance(it, dict):
            label = str(it.get("label") or it.get("key") or it.get("name") or "").strip()
            if not label:
                continue
            value = it.get("value")
            if value is None:
                value = it.get("description")
            out.append({"label": label, "value": value if value is not None else label})
        elif isinstance(it, str):
            s = it.strip()
            if s:
                out.append({"label": s, "value": s})
    return out


def _pick_display(labels: list[str], display_count: int, avoid: list[str]) -> tuple[list[str], int]:
    """Sample the wheel faces uniformly from the pool (avoiding ``avoid`` when
    possible), then pick the winner uniformly among the faces. Both stages use the
    CSPRNG; the composition is uniform over the full pool."""
    avoid_set = {a.strip() for a in avoid if isinstance(a, str)}
    pool = [l for l in labels if l not in avoid_set] or list(labels)
    k = max(1, min(display_count, len(pool)))
    display = secure_sample(pool, k)
    winner_index = secure_randint(0, len(display) - 1)
    return display, winner_index


def _seed_pool(mode: str, plan_queries: list[str], plan_keywords: list[str]) -> list[str]:
    if mode == "web":
        seeds = plan_queries or list(WEB_PHRASES)
    else:  # image
        seeds = plan_keywords or list(IMAGE_WORDS)
    return [s for s in (str(x).strip() for x in seeds) if s]


def _gate_safe_text(value: str | None, fallback: str | None) -> str | None:
    """Neutralize a TOP-LEVEL output string that would trip ToolResult.output's
    stringified-structure gate (models.py). ``title``/``seed`` are display text —
    never stringified dicts — but a model could pass JSON-looking text; fall back
    to a safe value rather than let the gate turn a successful spin into an error."""
    if value is None:
        return None
    t = value.strip()
    if len(t) >= 2 and t[0] in "{[" and t[-1] in "}]":
        return fallback
    return value


# ── Resolvers ─────────────────────────────────────────────────────────────────


async def _resolve_web(
    seed: str, plan: WheelPlan, ctx: ToolContext, stream: ToolStreamManager
) -> SeedResolution:
    from matrx_scraper.features.quick_search import search_web_mcp_quick

    res = await search_web_mcp_quick(
        queries=[seed],
        freshness=plan.freshness or WEB_FRESHNESS_DEFAULT,
        count=WEB_RESULTS,
        emitter=ctx.emitter,
        call_id=ctx.call_id,
    )
    text = ""
    if isinstance(res, dict) and res.get("status") == "success":
        text = res.get("result", "") or ""
    if not text.strip():
        return SeedResolution(value=f"(No fresh results found for “{seed}”.)", sources=[])
    return SeedResolution(value=text, sources=None)


async def _resolve_image(
    seed: str, plan: WheelPlan, ctx: ToolContext, stream: ToolStreamManager
) -> SeedResolution:
    from matrx_scraper.features.stock_image_search import search_stock_images

    api_keys = ctx.api_keys
    key = api_keys.get("unsplash") or api_keys.get("UNSPLASH_ACCESS_KEY")
    res = await search_stock_images(seed, api_key=key, per_page=IMAGE_PER_PAGE)
    images = res.get("images") or []
    if not images:
        note = f" {res['error']}" if res.get("error") else ""
        return SeedResolution(value=f"(No image found for “{seed}”.{note})", image=None, sources=[])

    # Random image among the results → extra entropy (a different photo each spin).
    pick = secure_choice(images)
    image = {
        "url": pick.get("url_regular") or pick.get("url_full") or pick.get("url_thumb") or "",
        "thumb": pick.get("url_thumb") or "",
        "photographer_name": pick.get("photographer_name"),
        "photographer_url": pick.get("photographer_url"),
        "description": pick.get("description"),
        "source": "unsplash",
    }
    photog = image.get("photographer_name")
    caption = f"{seed}" + (f" — photo by {photog} on Unsplash" if photog else "")
    return SeedResolution(value=caption, image=image, sources=None)


register_resolver("web", _resolve_web)
register_resolver("image", _resolve_image)


# ── Planning ───────────────────────────────────────────────────────────────────


def _build_plan(parsed: Any) -> WheelPlan | str:
    """Return a ``WheelPlan`` or an error message string."""
    mode = parsed.mode
    display_count = max(2, min(int(parsed.display_count), MAX_DISPLAY))
    # Guard the (LLM-controlled) title so a JSON-looking value can't trip the
    # ToolResult.output stringified-structure gate; fall back to the default.
    title = _gate_safe_text((parsed.title or "").strip(), "") or DEFAULT_TITLES.get(
        mode, "Spin the wheel"
    )

    if mode == "list":
        items = _normalize_items(parsed.items)
        if not items:
            # No caller items → spin a built-in pool (named via `pool`, else ideas).
            items = [{"label": t, "value": t} for t in _resolve_pool(parsed.pool)]
        # Dedupe by label: each distinct label is ONE face (first value wins), so a
        # repeated label can't get double selection weight or collapse to the wrong
        # value when landed on.
        labels: list[str] = []
        value_by_label: dict[str, Any] = {}
        for it in items:
            if it["label"] not in value_by_label:
                labels.append(it["label"])
            value_by_label.setdefault(it["label"], it["value"])
        display, winner_index = _pick_display(labels, display_count, parsed.avoid)
        plan = WheelPlan(
            mode=mode, title=title, candidates=display, winner_index=winner_index,
            pool_size=len(labels), spin_ms=0, avoid=list(parsed.avoid),
        )
        plan.chosen_value = value_by_label.get(plan.winner_label, plan.winner_label)
        return plan

    if mode in ("web", "image"):
        seeds = _seed_pool(mode, list(parsed.queries), list(parsed.keywords))
        if not seeds:
            return f"{mode} mode needs at least one seed phrase."
        display, winner_index = _pick_display(seeds, display_count, parsed.avoid)
        return WheelPlan(
            mode=mode, title=title, candidates=display, winner_index=winner_index,
            pool_size=len(seeds), spin_ms=0, seed=display[winner_index],
            freshness=parsed.freshness, avoid=list(parsed.avoid),
        )

    return f"Unknown mode: {mode!r}."


# ── Entry point ────────────────────────────────────────────────────────────────


async def random_wheel(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    from matrx_ai.tools._generated_declarations import RandomWheelArgs

    stream = ToolStreamManager(ctx.emitter, ctx.call_id, "random_wheel")
    try:
        parsed = RandomWheelArgs(**args)
        plan = _build_plan(parsed)
        if isinstance(plan, str):
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation", message=plan,
                    suggested_action="Provide items (list mode) or seed phrases (web/image).",
                ),
                started_at=started_at, completed_at=time.time(),
                tool_name="random_wheel", call_id=ctx.call_id,
            )

        plan.spin_ms = secure_randint(SPIN_MIN_MS, SPIN_MAX_MS) if parsed.dramatize else 0

        # Tell the FE everything it needs to animate the spin deterministically.
        await stream.step(
            "spin",
            f"Spinning — {len(plan.candidates)} on the wheel…",
            data={
                "candidates": plan.candidates,
                "winner_index": plan.winner_index,
                "spin_duration_ms": plan.spin_ms,
                "title": plan.title,
                "mode": plan.mode,
                "pool_size": plan.pool_size,
            },
        )

        resolver = _RESOLVERS.get(plan.mode)
        resolution: SeedResolution | None = None

        async def _settle() -> None:
            if plan.spin_ms:
                await asyncio.sleep(plan.spin_ms / 1000)

        if resolver is not None and plan.seed is not None:
            await stream.step("resolve", f"The wheel landed on “{plan.seed}”. Fetching…")
            # Fetch CONCURRENTLY with the dramatize delay → total time = max(spin, fetch).
            settle_task = asyncio.create_task(_settle())
            try:
                resolution = await resolver(plan.seed, plan, ctx, stream)
            finally:
                await settle_task
            plan.chosen_value = resolution.value
        else:
            await _settle()

        # KindModel result (KIND_TOOL_LEDGER): the spin envelope is a declared
        # shape; `chosen.value` stays open by the resolver contract.
        image = resolution.image if resolution else None
        output = WheelSpinResult(
            mode=plan.mode,
            title=plan.title,  # already gate-safe (guarded in _build_plan)
            chosen=WheelChoice(label=plan.winner_label, value=plan.chosen_value),
            candidates=plan.candidates,
            winner_index=plan.winner_index,
            pool_size=plan.pool_size,
            display_count=len(plan.candidates),
            spin_duration_ms=plan.spin_ms,
            seed=_gate_safe_text(plan.seed, None),
            sources=resolution.sources if resolution else None,
            image=WheelImage(**image) if image else None,
        ).model_dump(mode="json")
        return ToolResult(
            success=True,
            output=output,
            output_preview={"chosen": plan.winner_label, "mode": plan.mode},
            started_at=started_at, completed_at=time.time(),
            tool_name="random_wheel", call_id=ctx.call_id,
        )

    except Exception as exc:  # noqa: BLE001 — surfaced as a structured tool error
        vcprint(
            f"random_wheel failed: {exc}\n{traceback.format_exc()}",
            "[random_wheel] Unhandled exception",
            color="red",
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"Random wheel failed: {exc}",
                traceback=traceback.format_exc(),
                is_retryable=True,
            ),
            started_at=started_at, completed_at=time.time(),
            tool_name="random_wheel", call_id=ctx.call_id,
        )
