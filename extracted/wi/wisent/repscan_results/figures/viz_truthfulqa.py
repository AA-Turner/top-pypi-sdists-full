"""Hero figure for TruthfulQA Custom — one clean visual."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

BG = "#0d1117"
CARD = "#161b22"
TEXT = "#c9d1d9"
GRID = "#30363d"
BLUE = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#d29922"
PURPLE = "#bc8cff"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
    "xtick.color": TEXT, "ytick.color": TEXT,
    "text.color": TEXT, "grid.color": GRID,
    "font.size": 11,
})

# ── Data ────────────────────────────────────────────────────
labels = [
    "Llama-3.2-1B", "Qwen3-8B", "Llama-2-7B", "GPT-oss-20B"
]
colors = [BLUE, GREEN, ORANGE, PURPLE]

categories = [
    "Signal\nStrength", "Linear\nProbe", "Stability",
    "Consistency", "CAA\nAlignment", "Pair\nAlignment",
]
data = {
    "Llama-3.2-1B": [0.715, 0.736, 0.983, 0.394, 0.797, 0.840],
    "Qwen3-8B":     [0.739, 0.824, 0.990, 0.424, 0.756, 0.887],
    "Llama-2-7B":   [0.703, 0.788, 0.987, 0.406, 0.822, 0.857],
    "GPT-oss-20B":  [0.735, 0.821, 0.995, 0.445, 0.438, 0.734],
}
rec = {
    "Llama-3.2-1B": ("CAA", 0.75, True),
    "Qwen3-8B":     ("TECZA", 0.85, True),
    "Llama-2-7B":   ("CAA", 1.00, False),
    "GPT-oss-20B":  ("CAA", 1.00, False),
}

# ── Radar setup ─────────────────────────────────────────────
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

fig = plt.figure(figsize=(10, 10))
gs = GridSpec(1, 1, figure=fig,
              left=0.08, right=0.92, top=0.88, bottom=0.08)
ax = fig.add_subplot(gs[0, 0], polar=True)

# Title
fig.text(0.50, 0.95,
         "TruthfulQA Custom — Zwiad Protocol",
         ha="center", fontsize=18, fontweight="bold", color=TEXT)
fig.text(0.50, 0.915,
         "Cross-model geometry comparison  |  "
         "700 / 700 / 580 / 500 contrastive pairs  |  "
         "All pass signal test (p < 0.001)",
         ha="center", fontsize=9, color=GRID)

# Plot each model
for i, name in enumerate(labels):
    vals = data[name] + [data[name][0]]
    ax.plot(angles, vals, "o-", linewidth=2.2, color=colors[i],
            markersize=6, label=name, zorder=3)
    ax.fill(angles, vals, alpha=0.10, color=colors[i])

# Style the radar
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight="bold")
ax.set_ylim(0, 1.05)
ax.set_rticks([0.25, 0.50, 0.75, 1.0])
ax.set_yticklabels(["0.25", "0.50", "0.75", "1.0"],
                    fontsize=8, color=GRID)
ax.spines["polar"].set_color(GRID)
ax.grid(color=GRID, alpha=0.4)

# Legend with recommendation annotations
legend_lines = []
for i, name in enumerate(labels):
    method, conf, frag = rec[name]
    tag = f"{name}  →  {method} ({conf:.0%})"
    if frag:
        tag += "  [fragmented]"
    legend_lines.append(
        ax.plot([], [], "o-", color=colors[i], lw=2.2,
                markersize=6, label=tag)[0]
    )

ax.legend(handles=legend_lines, loc="upper left",
          bbox_to_anchor=(-0.15, -0.08), fontsize=10,
          frameon=False, ncol=2, columnspacing=2.0)

# Annotate the consistency dip
cons_angle = angles[3]
ax.annotate("consistency\ndip across\nall models",
            xy=(cons_angle, 0.42), fontsize=8,
            ha="center", va="bottom", color=ORANGE,
            fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=ORANGE,
                            lw=1.5),
            xytext=(cons_angle + 0.35, 0.18))

# Annotate GPT-oss CAA weakness
caa_angle = angles[4]
ax.annotate("GPT-oss-20B\nlow CAA align",
            xy=(caa_angle, 0.44), fontsize=8,
            ha="center", va="top", color=PURPLE,
            fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=PURPLE,
                            lw=1.5),
            xytext=(caa_angle - 0.45, 0.20))

# ── Save ────────────────────────────────────────────────────
out = "zwiad_results/figures/truthfulqa_custom_hero.png"
fig.savefig(out, dpi=200, bbox_inches="tight")
print(f"Saved -> {out}")
plt.close()
