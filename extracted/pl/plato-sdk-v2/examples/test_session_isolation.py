#!/usr/bin/env python3
"""Test session network isolation: VMs in different sessions should NOT communicate.

This script tests the session isolation architecture:
1. Create 2 sessions, each with 2 VMs
2. VMs within the same session CAN communicate (positive test)
3. VMs in different sessions CANNOT communicate (negative test)

Architecture:
- Each session gets a unique subnet (10.{100+worker_idx}.x.x)
- VMs in the same session can reach each other via /etc/hosts aliases
- VMs in different sessions should NOT be able to reach each other
- nftables rules enforce session isolation

Usage:
    export PLATO_API_KEY=your-key
    python test_session_isolation.py
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

from plato.v2.async_ import Plato
from plato.v2.types import Env, SimConfigCompute

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def cat_etc_hosts(env, name: str) -> str:
    """Cat /etc/hosts on a VM and return the content."""
    result = await env.execute("cat /etc/hosts", timeout=10)
    logger.info(f"  {name} /etc/hosts:\n{result.stdout}")
    return result.stdout


async def test_ping(env, target: str, name: str, should_succeed: bool) -> bool:
    """Test ping from env to target, expecting success or failure."""
    result = await env.execute(f"ping -c 2 -W 3 {target}", timeout=15)
    success = result.exit_code == 0

    if should_succeed:
        if success:
            logger.info(f"  OK: {name} -> {target} ping succeeded (expected)")
            return True
        else:
            logger.error(f"  FAIL: {name} -> {target} ping failed (expected success)")
            logger.error(f"    stdout: {result.stdout}")
            logger.error(f"    stderr: {result.stderr}")
            return False
    else:
        if not success:
            logger.info(f"  OK: {name} -> {target} ping failed (expected - isolation working)")
            return True
        else:
            logger.error(f"  FAIL: {name} -> {target} ping succeeded (expected failure - isolation BROKEN!)")
            return False


async def get_mesh_ip(env) -> str | None:
    """Get the mesh IP from /etc/hosts for a VM."""
    result = await env.execute("grep '.plato.internal' /etc/hosts | head -1 | awk '{print $1}'", timeout=10)
    ip = result.stdout.strip()
    return ip if ip else None


async def main():
    # Check environment
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        logger.error("PLATO_API_KEY not set")
        return 1

    logger.info("=" * 70)
    logger.info("SESSION ISOLATION TEST: Cross-Session Communication Should FAIL")
    logger.info("=" * 70)
    logger.info("")

    plato = Plato()
    session1 = None
    session2 = None

    results = {
        # Positive tests (same session - should work)
        "session1_vm1_to_vm2": False,
        "session1_vm2_to_vm1": False,
        "session2_vm3_to_vm4": False,
        "session2_vm4_to_vm3": False,
        # Negative tests (cross-session - should FAIL to connect)
        "session1_vm1_to_session2_vm3": False,
        "session1_vm1_to_session2_vm4": False,
        "session2_vm3_to_session1_vm1": False,
        "session2_vm3_to_session1_vm2": False,
    }

    try:
        # =====================================================================
        # 1. Create two sessions with 2 VMs each (in parallel)
        # =====================================================================
        logger.info("[1/5] Creating two sessions with 2 VMs each (in parallel)...")

        vm_config = SimConfigCompute(cpus=1, memory=1024, disk=10000)

        # Create both sessions in parallel
        session1_task = plato.sessions.create(
            envs=[
                Env.resource("s1-vm1", sim_config=vm_config, alias="vm1"),
                Env.resource("s1-vm2", sim_config=vm_config, alias="vm2"),
            ],
            timeout=600,
        )
        session2_task = plato.sessions.create(
            envs=[
                Env.resource("s2-vm3", sim_config=vm_config, alias="vm3"),
                Env.resource("s2-vm4", sim_config=vm_config, alias="vm4"),
            ],
            timeout=600,
        )

        session1, session2 = await asyncio.gather(session1_task, session2_task)

        logger.info(f"  Session 1 ID: {session1.session_id}")
        logger.info(f"  Session 2 ID: {session2.session_id}")

        # Get env references by alias
        s1_vm1 = next(e for e in session1.envs if e.alias == "vm1")
        s1_vm2 = next(e for e in session1.envs if e.alias == "vm2")
        s2_vm3 = next(e for e in session2.envs if e.alias == "vm3")
        s2_vm4 = next(e for e in session2.envs if e.alias == "vm4")

        logger.info(f"  Session 1: vm1={s1_vm1.job_id}, vm2={s1_vm2.job_id}")
        logger.info(f"  Session 2: vm3={s2_vm3.job_id}, vm4={s2_vm4.job_id}")

        # =====================================================================
        # 2. Cat /etc/hosts on all VMs (in parallel)
        # =====================================================================
        logger.info("[2/5] Showing /etc/hosts on all VMs...")

        hosts_tasks = [
            cat_etc_hosts(s1_vm1, "Session1/vm1"),
            cat_etc_hosts(s1_vm2, "Session1/vm2"),
            cat_etc_hosts(s2_vm3, "Session2/vm3"),
            cat_etc_hosts(s2_vm4, "Session2/vm4"),
        ]
        await asyncio.gather(*hosts_tasks)

        # =====================================================================
        # 3. Get mesh IPs for cross-session tests (in parallel)
        # =====================================================================
        logger.info("[3/5] Getting mesh IPs for cross-session tests...")

        # Get mesh IPs from /etc/hosts - each VM's own IP isn't listed,
        # but we can get peer IPs and derive from that
        ip_tasks = [
            s1_vm1.execute("hostname -I | awk '{print $1}'", timeout=10),
            s1_vm2.execute("hostname -I | awk '{print $1}'", timeout=10),
            s2_vm3.execute("hostname -I | awk '{print $1}'", timeout=10),
            s2_vm4.execute("hostname -I | awk '{print $1}'", timeout=10),
        ]
        await asyncio.gather(*ip_tasks)

        # Get the mesh IPs from /etc/hosts (the IP assigned to this VM in the mesh)
        mesh_ip_tasks = [
            s1_vm2.execute("grep vm1 /etc/hosts | awk '{print $1}'", timeout=10),  # vm1's IP from vm2's hosts
            s1_vm1.execute("grep vm2 /etc/hosts | awk '{print $1}'", timeout=10),  # vm2's IP from vm1's hosts
            s2_vm4.execute("grep vm3 /etc/hosts | awk '{print $1}'", timeout=10),  # vm3's IP from vm4's hosts
            s2_vm3.execute("grep vm4 /etc/hosts | awk '{print $1}'", timeout=10),  # vm4's IP from vm3's hosts
        ]
        mesh_results = await asyncio.gather(*mesh_ip_tasks)

        s1_vm1_mesh_ip = mesh_results[0].stdout.strip()
        s1_vm2_mesh_ip = mesh_results[1].stdout.strip()
        s2_vm3_mesh_ip = mesh_results[2].stdout.strip()
        s2_vm4_mesh_ip = mesh_results[3].stdout.strip()

        logger.info(f"  Session 1: vm1={s1_vm1_mesh_ip}, vm2={s1_vm2_mesh_ip}")
        logger.info(f"  Session 2: vm3={s2_vm3_mesh_ip}, vm4={s2_vm4_mesh_ip}")

        # =====================================================================
        # 4. Test SAME-SESSION connectivity (should succeed)
        # =====================================================================
        logger.info("[4/5] Testing SAME-SESSION connectivity (should succeed)...")

        # Test all same-session pings in parallel
        same_session_tasks = [
            test_ping(s1_vm1, "vm2", "s1/vm1", should_succeed=True),
            test_ping(s1_vm2, "vm1", "s1/vm2", should_succeed=True),
            test_ping(s2_vm3, "vm4", "s2/vm3", should_succeed=True),
            test_ping(s2_vm4, "vm3", "s2/vm4", should_succeed=True),
        ]
        same_session_results = await asyncio.gather(*same_session_tasks)

        results["session1_vm1_to_vm2"] = same_session_results[0]
        results["session1_vm2_to_vm1"] = same_session_results[1]
        results["session2_vm3_to_vm4"] = same_session_results[2]
        results["session2_vm4_to_vm3"] = same_session_results[3]

        # =====================================================================
        # 5. Test CROSS-SESSION connectivity (should FAIL - isolation)
        # =====================================================================
        logger.info("[5/5] Testing CROSS-SESSION connectivity (should FAIL - isolation)...")

        if not s2_vm3_mesh_ip or not s2_vm4_mesh_ip or not s1_vm1_mesh_ip or not s1_vm2_mesh_ip:
            logger.error("  Could not get mesh IPs, skipping cross-session tests")
        else:
            # Test cross-session pings in parallel (all should fail)
            cross_session_tasks = [
                test_ping(s1_vm1, s2_vm3_mesh_ip, "s1/vm1->s2/vm3", should_succeed=False),
                test_ping(s1_vm1, s2_vm4_mesh_ip, "s1/vm1->s2/vm4", should_succeed=False),
                test_ping(s2_vm3, s1_vm1_mesh_ip, "s2/vm3->s1/vm1", should_succeed=False),
                test_ping(s2_vm3, s1_vm2_mesh_ip, "s2/vm3->s1/vm2", should_succeed=False),
            ]
            cross_session_results = await asyncio.gather(*cross_session_tasks)

            results["session1_vm1_to_session2_vm3"] = cross_session_results[0]
            results["session1_vm1_to_session2_vm4"] = cross_session_results[1]
            results["session2_vm3_to_session1_vm1"] = cross_session_results[2]
            results["session2_vm3_to_session1_vm2"] = cross_session_results[3]

        # =====================================================================
        # Summary
        # =====================================================================
        logger.info("")
        logger.info("=" * 70)
        logger.info("TEST RESULTS")
        logger.info("=" * 70)
        logger.info(f"Session 1 ID: {session1.session_id}")
        logger.info(f"Session 2 ID: {session2.session_id}")
        logger.info("")

        logger.info("Same-Session Tests (should PASS - connectivity works):")
        logger.info(f"  s1/vm1 -> s1/vm2:  {'PASS' if results['session1_vm1_to_vm2'] else 'FAIL'}")
        logger.info(f"  s1/vm2 -> s1/vm1:  {'PASS' if results['session1_vm2_to_vm1'] else 'FAIL'}")
        logger.info(f"  s2/vm3 -> s2/vm4:  {'PASS' if results['session2_vm3_to_vm4'] else 'FAIL'}")
        logger.info(f"  s2/vm4 -> s2/vm3:  {'PASS' if results['session2_vm4_to_vm3'] else 'FAIL'}")
        logger.info("")

        logger.info("Cross-Session Tests (should PASS - isolation blocks traffic):")
        logger.info(f"  s1/vm1 -> s2/vm3:  {'PASS' if results['session1_vm1_to_session2_vm3'] else 'FAIL'}")
        logger.info(f"  s1/vm1 -> s2/vm4:  {'PASS' if results['session1_vm1_to_session2_vm4'] else 'FAIL'}")
        logger.info(f"  s2/vm3 -> s1/vm1:  {'PASS' if results['session2_vm3_to_session1_vm1'] else 'FAIL'}")
        logger.info(f"  s2/vm3 -> s1/vm2:  {'PASS' if results['session2_vm3_to_session1_vm2'] else 'FAIL'}")
        logger.info("")

        all_same_session_passed = all(
            [
                results["session1_vm1_to_vm2"],
                results["session1_vm2_to_vm1"],
                results["session2_vm3_to_vm4"],
                results["session2_vm4_to_vm3"],
            ]
        )

        all_cross_session_passed = all(
            [
                results["session1_vm1_to_session2_vm3"],
                results["session1_vm1_to_session2_vm4"],
                results["session2_vm3_to_session1_vm1"],
                results["session2_vm3_to_session1_vm2"],
            ]
        )

        all_passed = all_same_session_passed and all_cross_session_passed

        if all_passed:
            logger.info("OVERALL: ALL TESTS PASSED")
            logger.info("  - Same-session connectivity: WORKING")
            logger.info("  - Cross-session isolation: WORKING")
        else:
            if not all_same_session_passed:
                logger.error("OVERALL: SAME-SESSION CONNECTIVITY BROKEN")
            if not all_cross_session_passed:
                logger.error("OVERALL: CROSS-SESSION ISOLATION BROKEN (SECURITY ISSUE!)")

        logger.info("=" * 70)

        return 0 if all_passed else 1

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        # Close both sessions in parallel
        close_tasks = []
        if session1:
            logger.info("Closing session 1...")
            close_tasks.append(session1.close())
        if session2:
            logger.info("Closing session 2...")
            close_tasks.append(session2.close())

        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)

        await plato.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
