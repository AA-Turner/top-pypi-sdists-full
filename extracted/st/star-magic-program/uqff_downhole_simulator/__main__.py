"""Headless CLI for the UQFF Downhole Simulator (v1.6.0 extension).

    python -m uqff_downhole_simulator run          --steps 200 --out run.csv
    python -m uqff_downhole_simulator service-life --years 5 --out curves.csv
    python -m uqff_downhole_simulator telemetry    --hours 24 --seed 11 --out field.csv
    python -m uqff_downhole_simulator case-study   --td 25000 --out case.md

Shared options (all subcommands): --gauges N, --td FT, --profile CSV,
--spec PRESET|JSON, --kickoff FT --inclination DEG (deviation).
No display needed anywhere; every subcommand writes a file and prints a
one-line summary.
"""

from __future__ import annotations

import argparse
import json
import sys


def _add_well_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--well", type=str, default=None,
                   help="MEASURED catalogue assembly (ktb_hb, site_1027, ...): base P/T "
                        "come from the archived well, not gradient templates; overrides --td/--profile")
    p.add_argument("--td", type=float, default=None, help="total depth (MD), ft")
    p.add_argument("--gauges", type=int, default=None, help="number of gauges (evenly spaced)")
    p.add_argument("--profile", type=str, default=None, help="well profile CSV (depth_ft,pressure_psi,temp_F; TVD-indexed)")
    p.add_argument("--spec", type=str, default=None, help="gauge spec: preset name or a datasheet JSON path")
    p.add_argument("--kickoff", type=float, default=None, help="deviation: kickoff MD, ft")
    p.add_argument("--inclination", type=float, default=None, help="deviation: tangent inclination, deg from vertical")


def _build_config(a):
    from . import (SimulatorConfig, load_well_profile_csv, make_sensor_string,
                   GAUGE_SPECS, load_gauge_spec_json, DEFAULT_TD_FT)
    from .uqff_deviation import DeviationSurvey
    if getattr(a, "well", None):
        from . import demo_config, GAUGE_SPECS as _GS
        kw2 = {}
        if a.spec:
            kw2["gauge_spec"] = (_GS[a.spec] if a.spec in _GS
                                 else load_gauge_spec_json(a.spec))
        cfg = demo_config(a.well, n_gauges=(a.gauges or 6), **kw2)
        print(f"[well] {a.well}: profile '{cfg.profile.name}' - "
              f"{len(cfg.sensor_depths_ft)} gauges inside the measured window "
              f"{cfg.profile.depths_ft[0]:.0f}-{cfg.profile.depths_ft[-1]:.0f} ft")
        return cfg
    td = a.td if a.td is not None else DEFAULT_TD_FT
    kw = {"td_ft": td}
    if a.gauges is not None:
        kw["sensor_depths_ft"] = make_sensor_string(a.gauges, td_ft=td)
    if a.profile:
        kw["profile"] = load_well_profile_csv(a.profile)
    if a.spec:
        kw["gauge_spec"] = (GAUGE_SPECS[a.spec] if a.spec in GAUGE_SPECS
                            else load_gauge_spec_json(a.spec))
    if a.kickoff is not None or a.inclination is not None:
        if a.kickoff is None or a.inclination is None:
            raise SystemExit("--kickoff and --inclination must be given together")
        kw["deviation"] = DeviationSurvey.from_kickoff(a.kickoff, a.inclination, td)
    return SimulatorConfig(**kw)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="uqff_downhole_simulator",
                                 description="UQFF Downhole Simulator - headless CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="run the engine, export the P/T history CSV")
    _add_well_args(p_run)
    p_run.add_argument("--steps", type=int, default=200)
    p_run.add_argument("--out", type=str, default="uqff_downhole_run.csv")

    p_sl = sub.add_parser("service-life", help="accumulate twin-leg drift, export divergence curves")
    _add_well_args(p_sl)
    p_sl.add_argument("--years", type=float, default=5.0)
    p_sl.add_argument("--recal", type=float, default=None, help="recalibration interval, years")
    p_sl.add_argument("--seed", type=int, default=None)
    p_sl.add_argument("--out", type=str, default="uqff_service_life.csv")

    p_tm = sub.add_parser("telemetry", help="field-telemetry acquisition, export historian CSV")
    _add_well_args(p_tm)
    p_tm.add_argument("--hours", type=float, default=24.0)
    p_tm.add_argument("--seed", type=int, default=None)
    p_tm.add_argument("--out", type=str, default="uqff_telemetry.csv")

    p_in = sub.add_parser("ingest", help="ingest a live-stream file through a port (read-only)")
    p_in.add_argument("--file", type=str, required=True, help="source file (historian CSV or LAS)")
    p_in.add_argument("--port", type=str, default="historian_csv",
                      help="port name from PORT_REGISTRY (historian_csv | las2 | site plug-ins)")

    p_w = sub.add_parser("wells", help="list the MEASURED catalogue assemblies (--well targets)")
    p_rep = sub.add_parser("report", help="generate the client survey report (Part 7)")
    p_rep.add_argument("--out", default="survey_report", help="output directory")

    sub.add_parser("operator", help="launch the operator GUI (requires PyQt6+matplotlib)")

    sub.add_parser("accept", help="run the simulator ACCEPTANCE suite (product gate)")

    p_b = sub.add_parser("bench", help="bench-test analysis per BENCH_TEST_PROTOCOL.md (or --selftest)")
    p_b.add_argument("--uqff-csv", type=str, default=None, help="UQFF-leg historian CSV (time_s + pressure column)")
    p_b.add_argument("--conv-csv", type=str, default=None, help="conventional-leg historian CSV")
    p_b.add_argument("--full-scale", type=float, default=30000.0)
    p_b.add_argument("--selftest", action="store_true", help="SIMULATION_SELF_TEST: verify the analysis arithmetic on synthetic legs")

    p_g = sub.add_parser("gamma", help="lithology-from-GR on a catalogue entry (measured API curves only)")
    p_g.add_argument("--catalog", type=str, default=None, help="catalogue entry (omit to list gamma-bearing entries)")
    p_g.add_argument("--channel", type=str, default=None)
    p_g.add_argument("--cutoff", type=float, default=0.5)
    p_g.add_argument("--gr-clean", type=float, default=None)
    p_g.add_argument("--gr-shale", type=float, default=None)

    p_rc = sub.add_parser("reconcile", help="two-stream reconciliation: live file vs closed-stream prediction")
    _add_well_args(p_rc)
    p_rc.add_argument("--file", type=str, default=None, help="live-stream file (historian CSV)")
    p_rc.add_argument("--live-catalog", type=str, default=None,
                      help="catalogue production entry as the live leg (measured downhole P)")
    p_rc.add_argument("--live-well", type=str, default=None, help="well tag inside the entry (e.g. 15/9-F-12)")
    p_rc.add_argument("--station-md", type=float, default=None,
                      help="gauge MD ft for the catalogue live leg (caller-supplied; not in the archived excerpt)")
    p_rc.add_argument("--port", type=str, default="historian_csv")

    p_cs = sub.add_parser("case-study", help="depth sweep, write the one-page markdown case")
    _add_well_args(p_cs)
    p_cs.add_argument("--points", type=int, default=12)
    p_cs.add_argument("--name", type=str, default="case-study well")
    p_cs.add_argument("--horizon", type=float, default=5.0)
    p_cs.add_argument("--out", type=str, default="uqff_downhole_case_study.md")

    a = ap.parse_args(argv)

    from . import (UQFFDownholeEngine, ServiceLifeConfig, ServiceLifeSimulator,
                   TelemetryConfig, TelemetryRecorder, CaseStudyConfig,
                   case_study, write_markdown, GAUGE_SPECS, load_gauge_spec_json,
                   load_well_profile_csv, DEFAULT_TD_FT)

    if a.cmd == "run":
        eng = UQFFDownholeEngine(_build_config(a))
        for _ in range(a.steps):
            eng.step()
        out = eng.export_csv(a.out)
        s = eng.summary()
        print(f"run: {s['sensors']} gauges x {a.steps} steps -> {out} "
              f"(avg drift {s['avg_drift_pct']} %FS/yr, suppression {s['canonical_suppression_at_unity_trims']})")
    elif a.cmd == "service-life":
        eng = UQFFDownholeEngine(_build_config(a))
        cfg = ServiceLifeConfig(years=a.years, recalibration_interval_years=a.recal, seed=a.seed)
        sim = ServiceLifeSimulator(engine=eng, config=cfg).run()
        out = sim.export_csv(a.out)
        d = sim.divergence_summary()
        print(f"service-life: {a.years:g} yr -> {out} "
              f"(sep {d['predicted_separation_rate_psi_yr']} psi/yr, ratio pred {d['predicted_ratio_suppression']})")
    elif a.cmd == "telemetry":
        eng = UQFFDownholeEngine(_build_config(a))
        rec = TelemetryRecorder(engine=eng, config=TelemetryConfig(duration_hours=a.hours, seed=a.seed)).run()
        out = rec.export_csv(a.out)
        s = rec.telemetry_summary()
        print(f"telemetry: {s['samples']} samples -> {out} "
              f"(uptime {s['uptime_pct']}%, stuck P/R {s['stuck_score']['precision']}/{s['stuck_score']['recall']})")
    elif a.cmd == "ingest":
        from . import ingest as _ingest
        st = _ingest(a.file, port=a.port)
        import json as _json
        print(_json.dumps(st.summary(), indent=1))
    elif a.cmd == "bench":
        import json as _json
        from .uqff_bench import bench_analysis, bench_selftest
        if a.selftest:
            print(_json.dumps(bench_selftest(), indent=1))
        elif a.uqff_csv and a.conv_csv:
            from . import ingest as _ingest
            import numpy as _np
            def _leg(path):
                st = _ingest(path, port="historian_csv")
                pc = [c for c in st.channels if "P" in c.upper()]
                if not pc:
                    raise SystemExit(f"{path}: no pressure channel found")
                return st.index, st.channels[pc[0]].values
            tu, pu = _leg(a.uqff_csv)
            tc, pc_ = _leg(a.conv_csv)
            print(_json.dumps(bench_analysis(tu, pu, tc, pc_, full_scale_psi=a.full_scale), indent=1))
        else:
            raise SystemExit("bench needs --uqff-csv AND --conv-csv, or --selftest")
    elif a.cmd == "gamma":
        import json as _json
        from .uqff_gamma import gamma_entries, gamma_report
        if not a.catalog:
            for n, chans in sorted(gamma_entries().items()):
                print(f"{n}: {', '.join(chans)}")
            return 0
        print(_json.dumps(gamma_report(a.catalog, channel=a.channel, cutoff=a.cutoff,
                                       gr_clean=a.gr_clean, gr_shale=a.gr_shale), indent=1))
    elif a.cmd == "accept":
        from .acceptance_tests import main as _accept
        return _accept()
    elif a.cmd == "operator":
        from .uqff_operator_app import launch_operator_app
        return launch_operator_app()
    elif a.cmd == "report":
        from .uqff_project import generate_report
        r = generate_report(a.out)
        print("report:", r["report_path"])
        for k, v in r["renders"].items():
            print("  %s: %s" % (k, v))
    elif a.cmd == "wells":
        from . import BUILTIN_ASSEMBLIES
        for name, maker in sorted(BUILTIN_ASSEMBLIES.items()):
            try:
                asm = maker()
            except Exception:
                # operator-tier assemblies on machines without the private
                # data: listed honestly, never crashing the listing (v1.77.0)
                print(f"{name}: OPERATOR-TIER assembly - private data not "
                      "present on this machine (tier is per-machine, never required)")
                continue
            roles = {r: f"{c.entry}/{c.channel} {c.coverage()[0]:.0f}-{c.coverage()[1]:.0f} m"
                     for r, c in asm.components.items()}
            bridge = "engine-ready" if "temperature" in asm.components else \
                     "no measured T (bridge refuses; lookups still live)"
            print(f"{name}: {asm.site}")
            for r, d in roles.items():
                print(f"    {r:12s} {d}")
            if asm.attachments:
                print(f"    attachments: {', '.join(sorted(asm.attachments))}")
            print(f"    [{bridge}]")
    elif a.cmd == "reconcile":
        from . import ingest as _ingest, Reconciler
        station_map = None
        if a.live_catalog:
            from . import production_live_stream
            if not a.live_well or a.station_md is None:
                raise SystemExit("--live-catalog needs --live-well and --station-md "
                                 "(the archived excerpt does not state the gauge depth; "
                                 "the CLI will not invent one)")
            stream, station_map = production_live_stream(a.live_catalog, a.live_well, a.station_md)
            print(f"[live] {stream.name} | {len(stream.index)} samples | "
                  f"NaN days dropped: {stream.meta.get('nan_days_dropped')}")
        elif a.file:
            stream = _ingest(a.file, port=a.port)
        else:
            raise SystemExit("reconcile needs --file OR --live-catalog")
        rep = Reconciler(_build_config(a)).reconcile(stream, station_map=station_map)
        import json as _json
        print(_json.dumps(rep, indent=1))
    elif a.cmd == "case-study":
        from .uqff_deviation import DeviationSurvey
        if getattr(a, "well", None):
            from . import demo_config
            _cfg = demo_config(a.well)
            td = _cfg.td_ft
            kw = {"td_ft": td, "n_depth_points": a.points,
                  "well_name": a.well, "horizon_years": a.horizon,
                  "profile": _cfg.profile}
        else:
            td = a.td if a.td is not None else DEFAULT_TD_FT
            kw = {"td_ft": td, "n_depth_points": a.points, "well_name": a.name, "horizon_years": a.horizon}
        if a.profile and "profile" not in kw:
            kw["profile"] = load_well_profile_csv(a.profile)
        if a.spec:
            kw["gauge_spec"] = (GAUGE_SPECS[a.spec] if a.spec in GAUGE_SPECS
                                else load_gauge_spec_json(a.spec))
        if a.kickoff is not None and a.inclination is not None:
            kw["deviation"] = DeviationSurvey.from_kickoff(a.kickoff, a.inclination, td)
        out = write_markdown(case_study(CaseStudyConfig(**kw)), a.out)
        print(f"case-study: -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
