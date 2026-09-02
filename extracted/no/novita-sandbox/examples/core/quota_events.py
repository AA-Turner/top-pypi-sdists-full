import os
from datetime import datetime

from dotenv import load_dotenv

from novita_sandbox.core import Sandbox

load_dotenv()


def main():
    try:
        print("[1] Querying recent sandbox events (last 10)")
        result = Sandbox.get_events(limit=10)
        print(f"    total: {result.total}, has_more: {result.has_more}")
        for evt in result.items:
            ts = datetime.fromtimestamp(evt.record_at).isoformat()
            print(f"    event_id:       {evt.event_id}")
            print(f"    record_at:      {ts}")
            print(f"    template_id:    {evt.template_id}")
            print(f"    template_name:  {evt.template_name}")
            print(f"    sandbox_id:     {evt.sandbox_id}")
            print(f"    event_name:     {evt.event_name}")
            print(f"    state:          {evt.state}")
            print(f"    error_msg:      {evt.error_msg}")
            print(f"    status_code:    {evt.status_code}")
            print()

        print("\n[2] Querying create/pause/resume events for a specific sandbox")
        sandbox_id = os.getenv("SANDBOX_ID")
        if sandbox_id:
            filtered = Sandbox.get_events(
                sandbox_id=sandbox_id,
                events="create,pause,resume",
                limit=20,
                order_asc=True,
            )
            print(f"    total: {filtered.total}, has_more: {filtered.has_more}")
            for evt in filtered.items:
                ts = datetime.fromtimestamp(evt.record_at).isoformat()
                print(f"    event_id:       {evt.event_id}")
                print(f"    record_at:      {ts}")
                print(f"    template_id:    {evt.template_id}")
                print(f"    template_name:  {evt.template_name}")
                print(f"    sandbox_id:     {evt.sandbox_id}")
                print(f"    event_name:     {evt.event_name}")
                print(f"    state:          {evt.state}")
                print(f"    error_msg:      {evt.error_msg}")
                print(f"    status_code:    {evt.status_code}")
                print()
        else:
            print("    Set SANDBOX_ID env var to filter by sandbox.")

        print("\n[3] Querying sandbox quota")
        quota = Sandbox.get_quota()
        print("    Limit:")
        print(f"      concurrent_instances: {quota.limit.concurrent_instances}")
        print(f"      concurrent_vcpu:      {quota.limit.concurrent_vcpu}")
        print(f"      concurrent_ram_mb:    {quota.limit.concurrent_ram_mb}")
        print(f"      max_length_hours:     {quota.limit.max_length_hours}")
        print(f"      disk_mb:              {quota.limit.disk_mb}")
        print(f"      max_vcpu:             {quota.limit.max_vcpu}")
        print(f"      max_ram_mb:           {quota.limit.max_ram_mb}")
        print("    Usage:")
        print(f"      concurrent_instances: {quota.usage.concurrent_instances}")
        print(f"      concurrent_vcpu:      {quota.usage.concurrent_vcpu}")
        print(f"      concurrent_ram_mb:    {quota.usage.concurrent_ram_mb}")

        print("\n=== All steps completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
