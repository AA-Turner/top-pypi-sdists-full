"""
threatwire.__main__
====================
CLI entry point: python -m threatwire  or  threatwire (after pip install)

Usage:
    threatwire capture --interface eth0 [--filter "tcp port 80"] [--output alerts.jsonl]
    threatwire analyze --pcap capture.pcap [--output report.json] [--min-severity medium]
    threatwire rules list
    threatwire rules test --pcap capture.pcap --rules /etc/threatwire/rules
"""

import argparse
import sys


def _cmd_capture(args):
    import logging

    from threatwire.core.pipeline import ThreatPipeline
    from threatwire.core.models import AlertSeverity
    from threatwire.handlers import FileHandler, LoggingHandler
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    pipeline = ThreatPipeline(
        interface=args.interface,
        bpf_filter=args.filter,
        enable_builtin_rules=True,
        min_alert_severity=AlertSeverity(args.min_severity),
    )

    if args.output:
        pipeline.bus.add_handler(FileHandler(args.output).handle, severity="info")

    pipeline.bus.add_handler(LoggingHandler().handle, severity=args.min_severity)

    print(f"threatwire capturing on {args.interface} (Ctrl-C to stop)")
    pipeline.run()


def _cmd_analyze(args):
    # Delegate to examples/analyze_pcap.py logic
    sys.argv = ["analyze_pcap", "--pcap", args.pcap,
                "--min-severity", args.min_severity]
    if args.output:
        sys.argv += ["--output", args.output]
    from examples.analyze_pcap import main
    main()


def _cmd_rules_list(args):
    from threatwire.rules.loader import RuleLoader
    rules = RuleLoader.load_builtin()
    print(f"\nBuilt-in rules ({len(rules)} total):\n")
    for r in sorted(rules, key=lambda x: x.severity.numeric, reverse=True):
        print(f"  [{r.severity.value.upper():8s}] {r.rule_id:20s} {r.name}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="threatwire",
        description="Real-time network threat detection pipeline",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # capture subcommand
    cap = sub.add_parser("capture", help="Live packet capture and threat detection")
    cap.add_argument("--interface", "-i", default="eth0")
    cap.add_argument("--filter", "-f", default="")
    cap.add_argument("--output", "-o", default="")
    cap.add_argument("--min-severity", default="medium",
                     choices=["info","low","medium","high","critical"])

    # analyze subcommand
    ana = sub.add_parser("analyze", help="Analyze a PCAP file offline")
    ana.add_argument("--pcap", "-p", required=True)
    ana.add_argument("--output", "-o", default="")
    ana.add_argument("--min-severity", default="low",
                     choices=["info","low","medium","high","critical"])

    # rules subcommand
    rules_cmd = sub.add_parser("rules", help="Rule management")
    rules_sub = rules_cmd.add_subparsers(dest="rules_command", required=True)
    rules_sub.add_parser("list", help="List all built-in rules")

    args = parser.parse_args()

    if args.command == "capture":
        _cmd_capture(args)
    elif args.command == "analyze":
        _cmd_analyze(args)
    elif args.command == "rules":
        if args.rules_command == "list":
            _cmd_rules_list(args)


if __name__ == "__main__":
    main()
