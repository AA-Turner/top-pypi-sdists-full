# ======================================== IMPORTS ========================================
from __future__ import annotations

import pyglet
import time
import functools
from contextlib import contextmanager
from typing import Callable

# ======================================== LOCAL THREAD ========================================
import threading
_active_profiler: threading.local = threading.local()


def _get_active() -> "Profiler | None":
    return getattr(_active_profiler, "profiler", None)

# ======================================== STATS ========================================
class _Stats:
    """Gestionnaire des statistiques du profiling"""
    __slots__ = ("samples",)

    def __init__(self):
        self.samples: list[float] = []

    def record(self, ms: float) -> None:
        """Démarre l'enregistrement"""
        self.samples.append(ms)

    @property
    def count(self) -> int:
        """Nombre d'enregistrements"""
        return len(self.samples)

    @property
    def total(self) -> float:
        """Durée totale de processing"""
        return sum(self.samples)

    @property
    def mean(self) -> float:
        """Moyenne de durée par section"""
        return self.total / len(self.samples) if self.samples else 0.0

    @property
    def peak(self) -> float:
        """Pique de processing"""
        return max(self.samples) if self.samples else 0.0

    @property
    def p95(self) -> float:
        """P95"""
        if not self.samples:
            return 0.0
        s = sorted(self.samples)
        idx = max(0, int(len(s) * 0.95) - 1)
        return s[idx]


# ======================================== DECORATOR ========================================
def profile_section(name: str):
    """
    Décorateur optionnel pour instrumenter manuellement une méthode.

    Exemple :
        class Renderer:
            @profile_section("renderer.draw_sprites")
            def draw(self): ...

    Si aucun profiler n'est actif, la méthode s'exécute normalement (no-op).
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            prof = _get_active()
            if prof is None:
                return fn(*args, **kwargs)
            with prof.track(name):
                return fn(*args, **kwargs)
        return wrapper
    return decorator

# ======================================== PROFILER ========================================
class Profiler:
    """Accumulateur de timings par section"""

    def __init__(self):
        self._sections: dict[str, _Stats] = {}
        self._frame_count: int = 0
        self._frame_start: float = 0.0
        self._frame_times: list[float] = []

    # ======================================== CONTEXT ========================================
    @contextmanager
    def track(self, name: str):
        t0 = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - t0) * 1_000
            if name not in self._sections:
                self._sections[name] = _Stats()
            self._sections[name].record(elapsed_ms)

    # ======================================== FRAME BOUNDARIES ========================================
    def begin_frame(self):
        self._frame_start = time.perf_counter()

    def end_frame(self):
        self._frame_count += 1
        self._frame_times.append((time.perf_counter() - self._frame_start) * 1_000)

    # ======================================== REPORT ========================================
    def report(self, group_by_prefix: bool = True) -> str:
        """Génère un rapport de profiling"""
        if not self._frame_times:
            return "No frames recorded."

        n = self._frame_count
        total_time = sum(self._frame_times)
        mean_frame = total_time / n
        peak_frame = max(self._frame_times)
        p95_frame  = sorted(self._frame_times)[max(0, int(n * 0.95) - 1)]
        fps_mean   = 1_000 / mean_frame if mean_frame > 0 else 0

        W = 80
        def row(*cols, widths):
            parts = []
            for i, (col, w) in enumerate(zip(cols, widths)):
                parts.append(f"{col:<{w}}" if i == 0 else f"{col:>{w}}")
            return f"│  {'  '.join(parts)}  │"

        COL_W = [30, 9, 9, 9, 7]

        lines: list[str] = [""]
        lines.append("┌" + "─" * (W - 2) + "┐")
        lines.append(f"│{'ENGINE PROFILER REPORT':^{W-2}}│")
        lines.append("├" + "─" * (W - 2) + "┤")
        lines.append(f"│  Frames : {n:<8}  Mean : {mean_frame:>7.3f} ms   P95 : {p95_frame:>7.3f} ms   FPS : {fps_mean:>7.1f}  │")
        lines.append(f"│  Peak frame : {peak_frame:>7.3f} ms{' ' * (W - 34)}│")
        lines.append("├" + "─" * (W - 2) + "┤")
        lines.append(row("Section", "Mean ms", "Peak ms", "P95 ms", "% frame", widths=COL_W))
        lines.append("├" + "─" * (W - 2) + "┤")

        if group_by_prefix:
            tree: dict = {}
            for name, stats in self._sections.items():
                node = tree
                parts = name.split(".")
                for part in parts[:-1]:
                    node = node.setdefault(part, [None, {}])[1]
                leaf = parts[-1]
                if leaf not in node:
                    node[leaf] = [None, {}]
                node[leaf][0] = stats

            def t_mean(nd): s, ch = nd; return (s.mean if s else 0.0) + sum(t_mean(c) for c in ch.values())
            def t_peak(nd): s, ch = nd; return max([(s.peak if s else 0.0)] + [t_peak(c) for c in ch.values()])
            def t_p95 (nd): s, ch = nd; return max([(s.p95  if s else 0.0)] + [t_p95 (c) for c in ch.values()])

            def render(name: str, node, depth: int, last: bool, ancestor_lasts: list) -> None:
                _, children = node
                pct = (t_mean(node) / mean_frame * 100) if mean_frame > 0 else 0

                if depth == 0:
                    indent = "▸ " if children else ""
                else:
                    continuation = "".join(
                        "     " if was_last else "  │  "
                        for was_last in ancestor_lasts[1:]
                    )
                    connector = "╰" if last else "├"
                    indent = continuation + f"  {connector}─ "

                bar = _mini_bar(pct, ch="█" if depth == 0 else "░")
                lines.append(row(
                    f"{indent}{name}",
                    f"{t_mean(node):.3f}", f"{t_peak(node):.3f}", f"{t_p95(node):.3f}",
                    f"{pct:.1f}% {bar}",
                    widths=COL_W,
                ))

                sorted_children = sorted(children.items(), key=lambda kv: t_mean(kv[1]), reverse=True)
                for i, (child_name, child_node) in enumerate(sorted_children):
                    is_last = i == len(sorted_children) - 1
                    render(child_name, child_node, depth + 1, is_last, ancestor_lasts + [last])

            sorted_top = sorted(tree.items(), key=lambda kv: t_mean(kv[1]), reverse=True)
            for top_name, top_node in sorted_top:
                if top_node[1]:
                    lines.append("├" + "─" * (W - 2) + "┤")
                render(top_name, top_node, depth=0, last=True, ancestor_lasts=[])

        else:
            for name, stats in sorted(self._sections.items(), key=lambda kv: kv[1].mean, reverse=True):
                pct = (stats.mean / mean_frame * 100) if mean_frame > 0 else 0
                lines.append(row(
                    name,
                    f"{stats.mean:.3f}", f"{stats.peak:.3f}", f"{stats.p95:.3f}",
                    f"{pct:.1f}% {_mini_bar(pct)}",
                    widths=COL_W,
                ))

        lines.append("└" + "─" * (W - 2) + "┘")
        lines.append("")
        return "\n".join(lines)

    def export(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.report())
        print(f"[Profiler] Report exported → {path}")

# ======================================== HELPERS ========================================
def _mini_bar(pct: float, width: int = 6, ch: str = "█") -> str:
    """Barre de progression ASCII proportionnelle à pct (0-100)."""
    filled = min(width, round(pct / 100 * width))
    empty  = width - filled
    return ch * filled + "·" * empty

# ======================================== RUN CONFIGURATION ========================================
class ProfiledRun:
    """Wrapper autour de engine.run() qui instrumente la boucle principale.

    Args:
        engine: module engine
        on_update: callback utilisateur habituel
        on_draw: callback utilisateur pour le dessin
        duration: durée de profiling en secondes
        export_path: chemin du fichier de sortie (None = console seulement)
    """

    def __init__(
        self,
        engine,
        on_update: Callable[[float], None] = None,
        on_draw: Callable[[], None] = None,
        duration: float = 10,
        export_path: str | None = "profile_report.txt",
    ):
        self._engine = engine
        self._user_update = on_update
        self._user_draw = on_draw
        self._duration = duration
        self._export_path = export_path
        self._profiler = Profiler()

    # ======================================== ENTRY POINT ========================================
    def run(self) -> None:
        eng  = self._engine
        prof = self._profiler

        pipeline = eng._pipeline
        if pipeline is None:
            raise RuntimeError("No window set. Call engine.set_window() before ProfiledRun.run()")

        managers = list(eng._context_manager)
        _active_profiler.profiler = prof

        native_window = pipeline.window.native

        _draw_ms: list[float] = [0.0]

        @native_window.event
        def on_draw():
            t0 = time.perf_counter()
            pipeline.window.clear()
            eng.scene.draw(pipeline)
            if self._user_draw is not None:
                self._user_draw()
            _draw_ms[0] = (time.perf_counter() - t0) * 1_000

        def _update(raw_dt: float):
            prof.begin_frame()

            dt = eng.time.tick(raw_dt)

            for manager in managers:
                manager.update(dt)

            eng.scene.update(dt)

            if self._user_update is not None:
                self._user_update(dt)

            for manager in managers:
                manager.flush()

            prof.end_frame()

            if prof._frame_times:
                prof._frame_times[-1] += _draw_ms[0]

        eng.time.schedule(_update)
        eng.time.after(self._duration, self._finish)

        try:
            pyglet.app.run(eng.time.target_dt if eng.time.target_dt is not None else 1 / 9999)
        except Exception as e:
            print(f"[Profiler] pyglet exception: {e}")
        finally:
            self._finish()

    def _finish(self) -> None:
        if _active_profiler.profiler is None:
            return
        _active_profiler.profiler = None

        report = self._profiler.report()
        print(report)

        if self._export_path:
            try:
                self._profiler.export(self._export_path)
            except OSError as e:
                print(f"[Profiler] Could not write file: {e}")

        try:
            self._engine.stop()
        except Exception:
            pass

# ======================================== EXPORTS ========================================
__all__ = [
    "profile_section",
    "Profiler",
    "ProfiledRun",
]