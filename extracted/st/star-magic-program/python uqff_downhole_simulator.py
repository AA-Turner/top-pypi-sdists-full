#!/usr/bin/env python3
"""
UQFF QCALCGEOM – Standalone Deep-Well Quartz Simulator
Single file. No external project imports required.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from dataclasses import dataclass, field
from typing import List
import random
from datetime import datetime
from pathlib import Path
import csv

# ====================== ENGINE ======================

DEFAULT_TD_FT = 27500.0
DEFAULT_SENSOR_DEPTHS_FT = [1200, 4500, 7500, 9000, 10500, 14000, 18000, 22000, 25000, 27500]

@dataclass
class Sensor:
    depth_ft: float
    cal_offset_P: float = 0.0
    cal_offset_T: float = 0.0
    K_MEX: float = 1.15
    Phi_res: float = 0.93
    name: str = ""

@dataclass
class SimulatorConfig:
    td_ft: float = DEFAULT_TD_FT
    sensor_depths_ft: List[float] = field(default_factory=lambda: DEFAULT_SENSOR_DEPTHS_FT.copy())
    surface_temp_F: float = 75.0
    surface_pressure_psi: float = 14.7
    temp_gradient_F_per_ft: float = 0.018
    pressure_gradient_psi_per_ft: float = 0.465
    global_K_MEX: float = 1.15
    global_Phi_res: float = 0.93
    noise_scale: float = 1.0
    event_probability: float = 0.27
    history_length: int = 400

class UQFFDownholeEngine:
    def __init__(self, config=None):
        self.cfg = config or SimulatorConfig()
        self.time = 0.0
        self.sensors = []
        self._build_sensors()
        self.history_t = [0.0]
        self.history_P = []
        self.history_T = []
        self._init_state()

    def _build_sensors(self):
        self.sensors = []
        for i, d in enumerate(self.cfg.sensor_depths_ft):
            self.sensors.append(Sensor(
                depth_ft=float(d),
                K_MEX=self.cfg.global_K_MEX,
                Phi_res=self.cfg.global_Phi_res,
                name=f"S{i+1}"
            ))

    def _init_state(self):
        self.base_P = np.array([
            self.cfg.surface_pressure_psi + s.depth_ft * self.cfg.pressure_gradient_psi_per_ft
            for s in self.sensors
        ], dtype=float)
        self.base_T = np.array([
            self.cfg.surface_temp_F + s.depth_ft * self.cfg.temp_gradient_F_per_ft
            for s in self.sensors
        ], dtype=float)
        self.P = self.base_P.copy()
        self.T = self.base_T.copy()
        self.history_P = [self.P.copy()]
        self.history_T = [self.T.copy()]

    def compute_drift(self, sensor, temp_F, pressure_psi):
        temp_C = (temp_F - 32.0) * 5.0 / 9.0
        thermal_stress = max(0.0, (temp_C - 150.0) / 80.0) ** 1.15
        pressure_stress = max(0.0, (pressure_psi - 15000.0) / 5000.0) ** 0.9
        vacuum_stab = 0.58 + 0.32 * 0.90
        structural = 0.52 + 0.38 * sensor.K_MEX
        resonance = 0.68 + 0.27 * sensor.Phi_res
        suppression = max(vacuum_stab * structural * resonance, 0.35)
        base = 0.22
        drift = base * (1.0 + 0.55 * thermal_stress + 0.35 * pressure_stress) / suppression
        return float(np.clip(drift, 0.03, 0.55))

    def step(self, dt=0.12):
        self.time += dt
        n = len(self.sensors)
        drifts = np.array([self.compute_drift(s, self.T[i], self.P[i]) for i, s in enumerate(self.sensors)])
        suppression = np.clip(1.0 - (drifts / 0.28), 0.25, 1.0)
        noise_P = np.random.normal(0, 28 * self.cfg.noise_scale, n) * suppression
        noise_T = np.random.normal(0, 0.9 * self.cfg.noise_scale, n) * suppression
        event = 0.0
        if random.random() < self.cfg.event_probability:
            event = 110.0 * np.sin(self.time / 7.2) * float(np.mean(suppression))
        self.P = self.base_P + noise_P + event
        self.T = self.base_T + noise_T
        for i, s in enumerate(self.sensors):
            self.P[i] += s.cal_offset_P
            self.T[i] += s.cal_offset_T
        self.P = np.clip(self.P, 50, 28000)
        self.T = np.clip(self.T, 40, 550)
        self.history_t.append(self.time)
        self.history_P.append(self.P.copy())
        self.history_T.append(self.T.copy())
        if len(self.history_t) > self.cfg.history_length:
            self.history_t = self.history_t[-self.cfg.history_length:]
            self.history_P = self.history_P[-self.cfg.history_length:]
            self.history_T = self.history_T[-self.cfg.history_length:]

    def set_global_uqff(self, K_MEX, Phi_res):
        self.cfg.global_K_MEX = K_MEX
        self.cfg.global_Phi_res = Phi_res
        for s in self.sensors:
            s.K_MEX = K_MEX
            s.Phi_res = Phi_res

    def set_sensor_offset(self, index, offset_P=None, offset_T=None):
        if 0 <= index < len(self.sensors):
            if offset_P is not None:
                self.sensors[index].cal_offset_P = float(offset_P)
            if offset_T is not None:
                self.sensors[index].cal_offset_T = float(offset_T)

    def export_csv(self, path=None):
        if path is None:
            path = f"uqff_downhole_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        p = Path(path)
        with p.open("w", newline="") as f:
            writer = csv.writer(f)
            header = ["time_s"]
            for s in self.sensors:
                header += [f"P_{s.name}_{s.depth_ft:.0f}ft", f"T_{s.name}_{s.depth_ft:.0f}ft"]
            writer.writerow(header)
            for i, t in enumerate(self.history_t):
                row = [round(t, 3)]
                for j in range(len(self.sensors)):
                    row.append(round(float(self.history_P[i][j]), 2))
                    row.append(round(float(self.history_T[i][j]), 2))
                writer.writerow(row)
        print(f"Exported: {p.resolve()}")
        return p

    @property
    def depths_ft(self):
        return np.array([s.depth_ft for s in self.sensors])

    @property
    def current_drifts(self):
        return np.array([self.compute_drift(s, self.T[i], self.P[i]) for i, s in enumerate(self.sensors)])

# ====================== VISUALIZATION ======================

def run():
    cfg = SimulatorConfig()
    engine = UQFFDownholeEngine(cfg)

    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1])
    ax_well = fig.add_subplot(gs[:, 0])
    ax_p = fig.add_subplot(gs[0, 1])
    ax_t = fig.add_subplot(gs[1, 1])

    ax_well.set_xlim(-200, 220)
    ax_well.set_ylim(0, cfg.td_ft + 800)
    ax_well.invert_yaxis()
    ax_well.set_title("UQFF QCALCGEOM – 10 Sensor Array (Deep Well)")
    ax_well.set_ylabel("Depth (ft)")
    ax_well.grid(True, alpha=0.3)

    ax_well.add_patch(patches.FancyBboxPatch(
        (-25, 0), 50, cfg.td_ft,
        boxstyle="round,pad=0.02", linewidth=2.2,
        edgecolor="#64748b", facecolor="#334155", alpha=0.85
    ))

    scatter = ax_well.scatter(
        np.zeros(len(engine.sensors)), engine.depths_ft,
        c=engine.T, cmap="plasma", s=160, vmin=60, vmax=450,
        edgecolors="white", zorder=5
    )
    texts = []

    def update(frame):
        nonlocal texts
        engine.step(0.15)

        scatter.set_offsets(np.column_stack((np.zeros(len(engine.sensors)), engine.depths_ft)))
        scatter.set_array(engine.T)

        for t in texts:
            t.remove()
        texts = []
        for i, s in enumerate(engine.sensors):
            txt = ax_well.text(60, s.depth_ft,
                               f"{s.name}  {engine.P[i]:.0f} psi  {engine.T[i]:.1f}°F",
                               fontsize=8, va="center", color="#e0f2fe")
            texts.append(txt)

        t_hist = engine.history_t
        ax_p.clear()
        ax_t.clear()
        ax_p.grid(True, alpha=0.3)
        ax_t.grid(True, alpha=0.3)
        ax_p.set_ylabel("Pressure (psi)")
        ax_t.set_ylabel("Temperature (°F)")
        ax_t.set_xlabel("Time (s)")

        for i, s in enumerate(engine.sensors):
            p_series = [row[i] for row in engine.history_P]
            t_series = [row[i] for row in engine.history_T]
            ax_p.plot(t_hist, p_series, lw=1.5, label=f"{s.name} ({s.depth_ft:.0f} ft)")
            ax_t.plot(t_hist, t_series, lw=1.5, label=f"{s.name} ({s.depth_ft:.0f} ft)")

        ax_p.legend(fontsize=7, loc="upper right")
        ax_t.legend(fontsize=7, loc="upper right")

        avg_drift = float(np.mean(engine.current_drifts))
        fig.suptitle(
            f"UQFF Deep-Well Simulator  |  t={engine.time:.1f}s  |  "
            f"Avg Drift={avg_drift:.3f}% FS/yr  |  TD={cfg.td_ft:.0f} ft",
            fontsize=13, color="#67e8f9"
        )
        return []

    ani = FuncAnimation(fig, update, interval=120, blit=False, cache_frame_data=False)
    plt.tight_layout()
    plt.show()
    engine.export_csv()

if __name__ == "__main__":
    run()