"""Smoke test each HeyLead MCP tool with minimal args. Reports OK, EXPECTED (e.g. setup required), or FAIL."""
from __future__ import annotations

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Use temp heylead home so we don't touch real data
tmp_home = Path(tempfile.mkdtemp(prefix="heylead_smoke_"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import heylead.config as config
config._heylead_home = lambda: tmp_home
config.ensure_dirs()

# Ensure DB exists
from heylead.db.schema import get_db
get_db().close()

def run(coro):
    return asyncio.run(coro)

results = []

def test(name: str, coro, expected_contains: list[str] | None = None):
    """Run tool coro; record OK, EXPECTED (if result contains any of expected_contains), or FAIL."""
    try:
        out = run(coro)
        if not isinstance(out, str):
            out = str(out)
        if expected_contains and any(s in out for s in expected_contains):
            results.append((name, "EXPECTED", out[:200]))
        else:
            results.append((name, "OK", out[:200]))
    except ImportError as e:
        results.append((name, "IMPORT_ERROR", str(e)))
    except Exception as e:
        results.append((name, "FAIL", f"{type(e).__name__}: {e}"))

# ─── Tests (minimal/safe args) ───
test("show_status", 
     __import__("heylead.tools.show_status", fromlist=["run_show_status"]).run_show_status(""),
     expected_contains=["Setup required", "No campaign", "campaign", "Campaign"])
test("scheduler_status",
     __import__("heylead.tools.scheduler_status", fromlist=["run_scheduler_status"]).run_scheduler_status())
test("emergency_stop",
     __import__("heylead.tools.emergency_stop", fromlist=["run_emergency_stop"]).run_emergency_stop())
test("compare_campaigns",
     __import__("heylead.tools.compare_campaigns", fromlist=["run_compare_campaigns"]).run_compare_campaigns(""))
test("campaign_report",
     __import__("heylead.tools.campaign_report", fromlist=["run_campaign_report"]).run_campaign_report(""),
     expected_contains=["No campaign", "campaign", "Campaign", "setup"])
test("suggest_next_action",
     __import__("heylead.tools.suggest_next_action", fromlist=["run_suggest_next_action"]).run_suggest_next_action(""),
     expected_contains=["Setup", "setup", "campaign", "No ", "next"])
test("toggle_scheduler",
     __import__("heylead.tools.scheduler_status", fromlist=["run_toggle_scheduler"]).run_toggle_scheduler(False))
test("retry_failed",
     __import__("heylead.tools.retry_failed", fromlist=["run_retry_failed"]).run_retry_failed(""),
     expected_contains=["No campaign", "retry", "error", "campaign"])
test("export_campaign",
     __import__("heylead.tools.export_campaign", fromlist=["run_export_campaign"]).run_export_campaign(""),
     expected_contains=["No campaign", "campaign", "Campaign"])
test("pause_campaign",
     __import__("heylead.tools.campaign_control", fromlist=["run_pause_campaign"]).run_pause_campaign(""),
     expected_contains=["No campaign", "campaign", "Campaign", "Pause"])
test("resume_campaign",
     __import__("heylead.tools.campaign_control", fromlist=["run_resume_campaign"]).run_resume_campaign(""),
     expected_contains=["No campaign", "campaign", "Campaign", "Resume"])
test("archive_campaign",
     __import__("heylead.tools.archive_campaign", fromlist=["run_archive_campaign"]).run_archive_campaign(""),
     expected_contains=["No campaign", "campaign", "Campaign"])
test("check_replies",
     __import__("heylead.tools.check_replies", fromlist=["run_check_replies"]).run_check_replies(),
     expected_contains=["Setup", "setup", "replies", "No ", "account"])
test("unlink_account",
     __import__("heylead.tools.unlink_account", fromlist=["run_unlink_account"]).run_unlink_account())

# These require backend/setup or specific IDs; we expect graceful messages
test("list_linkedin_accounts",
     __import__("heylead.tools.switch_account", fromlist=["run_list_linkedin_accounts"]).run_list_linkedin_accounts(),
     expected_contains=["Setup", "setup", "account", "Backend", "No ", "LinkedIn"])
test("switch_account",
     __import__("heylead.tools.switch_account", fromlist=["run_switch_account"]).run_switch_account(),
     expected_contains=["Setup", "setup", "account", "Backend", "No ", "LinkedIn"])
test("switch_account_to",
     __import__("heylead.tools.switch_account", fromlist=["run_switch_account_to"]).run_switch_account_to("dummy-id"),
     expected_contains=["Setup", "setup", "account", "Backend", "No ", "not found", "Invalid"])

test("generate_icp",
     __import__("heylead.tools.generate_icp", fromlist=["run_generate_icp"]).run_generate_icp("CTOs at startups", "", ""),
     expected_contains=["Setup", "setup", "LLM", "api_key", "limit", "ICP", "persona"])

test("create_campaign",
     __import__("heylead.tools.create_campaign", fromlist=["run_create_campaign"]).run_create_campaign(
         "CTOs at fintech", "", "", ""),
     expected_contains=["Setup", "setup", "First campaign", "company_context", "No LinkedIn"])

test("generate_and_send",
     __import__("heylead.tools.generate_send", fromlist=["run_generate_and_send"]).run_generate_and_send("", "copilot"),
     expected_contains=["Setup", "setup", "campaign", "No campaign", "Select"])
test("send_followup",
     __import__("heylead.tools.send_followup", fromlist=["run_send_followup"]).run_send_followup("", "", "copilot"),
     expected_contains=["Setup", "setup", "campaign", "No ", "follow"])
test("reply_to_prospect",
     __import__("heylead.tools.reply_to_prospect", fromlist=["run_reply_to_prospect"]).run_reply_to_prospect("", "copilot"),
     expected_contains=["Setup", "setup", "outreach", "No ", "pending"])
test("engage_prospect",
     __import__("heylead.tools.engage_prospect", fromlist=["run_engage_prospect"]).run_engage_prospect("", "", "auto", "copilot"),
     expected_contains=["Setup", "setup", "campaign", "No ", "outreach"])
test("approve_outreach",
     __import__("heylead.tools.approve_outreach", fromlist=["run_approve_outreach"]).run_approve_outreach("skip"),
     expected_contains=["Setup", "setup", "pending", "No ", "skip"])
test("skip_prospect",
     __import__("heylead.tools.skip_prospect", fromlist=["run_skip_prospect"]).run_skip_prospect("", ""),
     expected_contains=["No campaign", "campaign", "outreach"])
test("show_conversation",
     __import__("heylead.tools.show_conversation", fromlist=["run_show_conversation"]).run_show_conversation("dummy"),
     expected_contains=["outreach", "not found", "Invalid", "No "])
test("edit_campaign",
     __import__("heylead.tools.edit_campaign", fromlist=["run_edit_campaign"]).run_edit_campaign("", "", "", "", "", "", "", ""),
     expected_contains=["No campaign", "campaign", "Campaign"])
test("close_outreach",
     __import__("heylead.tools.close_outreach", fromlist=["run_close_outreach"]).run_close_outreach("", "lost", ""),
     expected_contains=["outreach", "not found", "No ", "hot_lead"])
test("delete_campaign",
     __import__("heylead.tools.delete_campaign", fromlist=["run_delete_campaign"]).run_delete_campaign("", False),
     expected_contains=["No campaign", "campaign", "confirm", "Campaign"])

# setup_profile without JWT: may ask for token or fail gracefully
test("setup_profile",
     __import__("heylead.tools.setup_profile", fromlist=["run_setup_profile"]).run_setup_profile("", "gemini", "", ""),
     expected_contains=["token", "Sign in", "connect", "URL", "backend_jwt"])

# ─── Consolidated dispatcher tests ───
test("account(list)",
     __import__("heylead.tools.account", fromlist=["run_account"]).run_account("list"),
     expected_contains=["Setup", "setup", "account", "Backend", "No ", "LinkedIn"])
test("account(switch_to)",
     __import__("heylead.tools.account", fromlist=["run_account"]).run_account("switch_to", "dummy"),
     expected_contains=["Setup", "setup", "account", "Backend", "No ", "not found", "Invalid"])
test("account(bad_action)",
     __import__("heylead.tools.account", fromlist=["run_account"]).run_account("bad"),
     expected_contains=["Unknown action"])
test("campaign(pause)",
     __import__("heylead.tools.campaign", fromlist=["run_campaign"]).run_campaign("pause"),
     expected_contains=["No campaign", "campaign", "Campaign", "Pause"])
test("campaign(emergency_stop)",
     __import__("heylead.tools.campaign", fromlist=["run_campaign"]).run_campaign("emergency_stop"))
test("campaign(retry_failed)",
     __import__("heylead.tools.campaign", fromlist=["run_campaign"]).run_campaign("retry_failed"),
     expected_contains=["No campaign", "retry", "error", "campaign"])
test("send_message(followup)",
     __import__("heylead.tools.send_message", fromlist=["run_send_message"]).run_send_message("followup"),
     expected_contains=["Setup", "setup", "campaign", "No ", "follow"])
test("send_message(reply)",
     __import__("heylead.tools.send_message", fromlist=["run_send_message"]).run_send_message("reply"),
     expected_contains=["Setup", "setup", "outreach", "No ", "pending"])
test("prospect(skip)",
     __import__("heylead.tools.prospect", fromlist=["run_prospect"]).run_prospect("skip"),
     expected_contains=["No campaign", "campaign", "outreach"])
test("prospect(close)",
     __import__("heylead.tools.prospect", fromlist=["run_prospect"]).run_prospect("close", outcome="lost"),
     expected_contains=["outreach", "not found", "No ", "hot_lead", "Setup"])
test("prospect(conversation)",
     __import__("heylead.tools.prospect", fromlist=["run_prospect"]).run_prospect("conversation"),
     expected_contains=["outreach_id", "required", "Error"])
test("analytics(report)",
     __import__("heylead.tools.analytics", fromlist=["run_analytics"]).run_analytics("report"),
     expected_contains=["No campaign", "campaign", "Campaign", "setup"])
test("analytics(export)",
     __import__("heylead.tools.analytics", fromlist=["run_analytics"]).run_analytics("export"),
     expected_contains=["No campaign", "campaign", "Campaign"])
test("analytics(compare)",
     __import__("heylead.tools.analytics", fromlist=["run_analytics"]).run_analytics("compare"))
test("signals(show)",
     __import__("heylead.tools.signals", fromlist=["run_signals"]).run_signals("show"))
test("scheduler(status)",
     __import__("heylead.tools.scheduler", fromlist=["run_scheduler"]).run_scheduler("status"))
test("scheduler(toggle)",
     __import__("heylead.tools.scheduler", fromlist=["run_scheduler"]).run_scheduler("toggle", enabled=False))

# Print report
print("\n" + "="*70)
print("HeyLead MCP tools smoke test report")
print("="*70)
ok = [r for r in results if r[1] == "OK"]
expected = [r for r in results if r[1] == "EXPECTED"]
fail = [r for r in results if r[1] == "FAIL"]
imp = [r for r in results if r[1] == "IMPORT_ERROR"]
for name, status, msg in results:
    sym = "✓" if status in ("OK", "EXPECTED") else "✗"
    print(f"  {sym} {name}: {status}")
print()
print("WORKING (OK or EXPECTED graceful message):", len(ok) + len(expected))
print("FAIL / IMPORT_ERROR:", len(fail) + len(imp))
if fail or imp:
    print("\n--- Details for FAIL / IMPORT_ERROR ---")
    for name, status, msg in fail + imp:
        print(f"  {name} ({status}): {msg[:300]}")
print("="*70)
