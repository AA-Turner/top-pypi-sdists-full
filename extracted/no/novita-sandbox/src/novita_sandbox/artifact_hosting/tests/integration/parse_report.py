#!/usr/bin/env python3
"""Parse JSON test report and generate a readable failure report.

Usage:
    python parse_report.py <json_report_file>
    python parse_report.py logs/test_report_20260202_182112.json
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def extract_http_logs(logs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Extract HTTP request/response from log entries."""
    http_logs = []
    for log in logs:
        msg = log.get("msg", "")
        if "HTTP Request:" in msg or "HTTP Response:" in msg:
            http_logs.append({
                "timestamp": log.get("asctime", ""),
                "level": log.get("levelname", ""),
                "message": msg,
            })
        elif "Request body:" in msg or "Response body:" in msg:
            http_logs.append({
                "timestamp": log.get("asctime", ""),
                "level": log.get("levelname", ""),
                "message": msg,
            })
    return http_logs


def format_test_failure(test: Dict[str, Any]) -> str:
    """Format a single test failure with all details."""
    lines = []
    
    # Header
    lines.append("=" * 80)
    lines.append(f"❌ Test Failed: {test['nodeid']}")
    lines.append("=" * 80)
    
    # Get the failure phase (setup, call, or teardown)
    for phase in ["setup", "call", "teardown"]:
        phase_data = test.get(phase, {})
        if phase_data.get("outcome") in ["failed", "error"]:
            lines.append(f"\n📍 Failure Phase: {phase}")
            lines.append(f"⏱️  Duration: {phase_data.get('duration', 0):.3f}s")
            
            # Crash info
            crash = phase_data.get("crash", {})
            if crash:
                lines.append(f"\n🔴 Error Details:")
                lines.append(f"   File: {crash.get('path', 'N/A')}")
                lines.append(f"   Line: {crash.get('lineno', 'N/A')}")
                lines.append(f"   Exception: {crash.get('message', 'N/A')}")
            
            # Traceback
            traceback = phase_data.get("traceback", [])
            if traceback:
                lines.append(f"\n📚 Call Stack:")
                for tb in traceback:
                    lines.append(f"   {tb.get('path', '')}:{tb.get('lineno', '')}")
                    if tb.get("message"):
                        lines.append(f"      → {tb['message']}")
            
            # HTTP Logs
            logs = phase_data.get("log", [])
            http_logs = extract_http_logs(logs)
            if http_logs:
                lines.append(f"\n📡 HTTP Request/Response:")
                for log in http_logs:
                    lines.append(f"   [{log['timestamp']}] {log['message'][:200]}")
            
            # SDK logs (non-HTTP)
            sdk_logs = [
                log for log in logs 
                if "novita_sandbox" in log.get("name", "") 
                and "HTTP" not in log.get("msg", "")
            ]
            if sdk_logs:
                lines.append(f"\n📝 SDK Logs:")
                for log in sdk_logs[-20:]:  # Last 20 logs
                    level = log.get("levelname", "INFO")
                    msg = log.get("msg", "")
                    if len(msg) > 150:
                        msg = msg[:150] + "..."
                    lines.append(f"   [{log.get('asctime', '')}] [{level}] {msg}")
            
            break
    
    lines.append("")
    return "\n".join(lines)


def parse_report(report_path: str) -> None:
    """Parse JSON report and print failure details."""
    with open(report_path) as f:
        data = json.load(f)
    
    # Summary
    summary = data.get("summary", {})
    print("\n" + "=" * 80)
    print("                    📊 Test Report Summary")
    print("=" * 80)
    print(f"  Total Tests: {summary.get('total', 0)}")
    print(f"  ✅ Passed: {summary.get('passed', 0)}")
    print(f"  ❌ Failed: {summary.get('failed', 0) + summary.get('error', 0)}")
    print(f"  ⏭️  Skipped: {summary.get('skipped', 0)}")
    print(f"  ⏱️  Duration: {data.get('duration', 0):.2f}s")
    
    # Environment
    env = data.get("environment", {})
    if env:
        print(f"\n  Environment Info:")
        print(f"    Python: {env.get('Python', 'N/A')}")
        print(f"    Platform: {env.get('Platform', 'N/A')}")
    
    # Passed tests
    passed = [t for t in data.get("tests", []) if t.get("outcome") == "passed"]
    if passed:
        print("\n" + "=" * 80)
        print("                    ✅ Passed Tests")
        print("=" * 80)
        for test in passed:
            duration = 0
            for phase in ["setup", "call", "teardown"]:
                duration += test.get(phase, {}).get("duration", 0)
            print(f"  ✓ {test['nodeid'].split('::')[-1]} ({duration:.3f}s)")
    
    # Failed tests
    failed = [
        t for t in data.get("tests", []) 
        if t.get("outcome") in ["failed", "error"]
    ]
    
    if failed:
        print("\n" + "=" * 80)
        print("                    ❌ Failed Test Details")
        print("=" * 80)
        
        for test in failed:
            print(format_test_failure(test))
    
    print("\n" + "=" * 80)
    print("                         End of Report")
    print("=" * 80 + "\n")


def main():
    if len(sys.argv) < 2:
        # Find the latest report
        logs_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "logs"
        reports = sorted(logs_dir.glob("test_report_*.json"), reverse=True)
        if reports:
            report_path = str(reports[0])
            print(f"Using latest report: {report_path}")
        else:
            print("Usage: python parse_report.py <json_report_file>")
            sys.exit(1)
    else:
        report_path = sys.argv[1]
    
    parse_report(report_path)


if __name__ == "__main__":
    main()
