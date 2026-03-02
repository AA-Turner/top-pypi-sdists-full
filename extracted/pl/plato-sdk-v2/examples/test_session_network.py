#!/usr/bin/env python3
"""Test session network: VM-to-VM connectivity and host mode (gateway SSH).

This script tests the session network architecture:
1. VM-to-VM connectivity via mesh IPs (host-level WireGuard, no WG inside VMs)
2. Host mode connectivity via gateway (SSH through HAProxy/WireGuard gateway)

Architecture:
- Workers have a single wgworker0 interface (not per-VM interfaces)
- VMs communicate using mesh IPs (10.{100+worker_idx}.x.x)
- Host-level nftables handles DNAT/SNAT between mesh IPs and tap IPs
- Gateway provides external SSH access via TLS/SNI routing
- /etc/hosts is automatically configured with peer aliases

Usage:
    export PLATO_API_KEY=your-key
    export PLATO_PROXY_HOST=gateway.plato.so  # Optional, for host mode test
    export PLATO_PROXY_PORT=443               # Optional
    python test_session_network.py
"""

import logging
import os
import subprocess
import sys
import time

from dotenv import load_dotenv

from plato.v2 import Env, Plato
from plato.v2.types import SimConfigCompute

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def test_gateway_ssh(job_id: str, proxy_host: str, proxy_port: int) -> bool:
    """Test SSH connection via gateway (host mode).

    The gateway uses TLS/SNI routing to direct traffic to VMs.
    SNI format: {job_id}--{port}.{proxy_host}
    """
    sni = f"{job_id}--22.{proxy_host}"

    logger.info(f"  Testing TLS connection to {proxy_host}:{proxy_port}")
    logger.info(f"  SNI: {sni}")

    cmd = [
        "openssl",
        "s_client",
        "-connect",
        f"{proxy_host}:{proxy_port}",
        "-servername",
        sni,
        "-verify_quiet",
    ]

    try:
        result = subprocess.run(
            cmd,
            input=b"",
            capture_output=True,
            timeout=10,
        )
        if b"CONNECTED" in result.stderr or result.returncode == 0:
            logger.info("  OK: TLS connection successful")
            return True
        else:
            logger.error(f"  FAIL: TLS connection failed: {result.stderr.decode()[:200]}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("  FAIL: TLS connection timed out")
        return False
    except Exception as e:
        logger.error(f"  FAIL: TLS connection error: {e}")
        return False


def main():
    # Check environment
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        logger.error("PLATO_API_KEY not set")
        return 1

    proxy_host = os.environ.get("PLATO_PROXY_HOST", "gateway.plato.so")
    proxy_port = int(os.environ.get("PLATO_PROXY_PORT", "443"))
    skip_gateway_test = os.environ.get("SKIP_GATEWAY_TEST", "").lower() == "true"

    logger.info("=" * 70)
    logger.info("SESSION NETWORK TEST: VM-to-VM + Host Mode (Gateway SSH)")
    logger.info("=" * 70)
    logger.info(f"Gateway: {proxy_host}:{proxy_port}")
    logger.info("")

    plato = Plato()
    session = None

    results = {
        "vm_to_vm_ping": False,
        "vm_to_vm_tcp": False,
        "gateway_ssh_vm1": False,
        "gateway_ssh_vm2": False,
    }

    try:
        # =====================================================================
        # 1. Create session with two VMs
        # =====================================================================
        logger.info("[1/5] Creating session with two VMs...")

        vm_config = SimConfigCompute(cpus=1, memory=1024, disk=10000)

        session = plato.sessions.create(
            envs=[
                Env.resource("vm1", sim_config=vm_config, alias="vm1"),
                Env.resource("vm2", sim_config=vm_config, alias="vm2"),
            ],
            timeout=600,
        )

        logger.info(f"  Session ID: {session.session_id}")

        # Get env references by alias
        vm1 = next(e for e in session.envs if e.alias == "vm1")
        vm2 = next(e for e in session.envs if e.alias == "vm2")

        logger.info(f"  VM1: job_id={vm1.job_id}")
        logger.info(f"  VM2: job_id={vm2.job_id}")

        # =====================================================================
        # 2. Network is already connected (connect_network=True by default)
        # =====================================================================
        logger.info("[2/5] Network connected automatically during session creation")

        # =====================================================================
        # 3. Test host mode (gateway SSH) - run first to test immediately after connect
        # =====================================================================
        logger.info("[3/5] Testing host mode (gateway SSH)...")

        if skip_gateway_test:
            logger.info("  Skipping gateway test (SKIP_GATEWAY_TEST=true)")
        else:
            logger.info("  Testing VM1 SSH via gateway...")
            results["gateway_ssh_vm1"] = test_gateway_ssh(vm1.job_id, proxy_host, proxy_port)

            logger.info("  Testing VM2 SSH via gateway...")
            results["gateway_ssh_vm2"] = test_gateway_ssh(vm2.job_id, proxy_host, proxy_port)

        # =====================================================================
        # 4. Test VM-to-VM ping connectivity (using aliases)
        # =====================================================================
        logger.info("[4/5] Testing VM-to-VM ping connectivity...")

        # VM1 -> VM2 ping using alias
        logger.info("  VM1 -> VM2 (vm2)...")
        ping_result = vm1.execute("ping -c 3 -W 5 vm2", timeout=30)

        if ping_result.exit_code == 0:
            logger.info("  OK: VM1 -> VM2 ping successful")
            results["vm_to_vm_ping"] = True
        else:
            logger.error("  FAIL: VM1 -> VM2 ping failed")
            logger.error(f"    stdout: {ping_result.stdout}")
            logger.error(f"    stderr: {ping_result.stderr}")

        # VM2 -> VM1 ping using alias
        logger.info("  VM2 -> VM1 (vm1)...")
        ping_result = vm2.execute("ping -c 3 -W 5 vm1", timeout=30)

        if ping_result.exit_code == 0:
            logger.info("  OK: VM2 -> VM1 ping successful")
        else:
            logger.error("  FAIL: VM2 -> VM1 ping failed")
            results["vm_to_vm_ping"] = False

        # =====================================================================
        # 5. Test VM-to-VM TCP connectivity (Redis)
        # =====================================================================
        logger.info("[5/5] Testing VM-to-VM TCP connectivity with Redis...")

        # Install Redis on both VMs
        logger.info("  Installing Redis on both VMs...")
        vm1.execute("apt-get update -qq && apt-get install -y -qq redis-server redis-tools", timeout=120)
        vm2.execute("apt-get update -qq && apt-get install -y -qq redis-server redis-tools", timeout=120)

        # Start Redis servers bound to all interfaces
        logger.info("  Starting Redis servers...")
        vm1.execute("redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes", timeout=10)
        vm2.execute("redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes", timeout=10)
        time.sleep(2)

        # Set keys on each VM
        logger.info("  Setting keys on each Redis server...")
        vm1.execute("redis-cli SET message 'Hello from VM1'", timeout=10)
        vm2.execute("redis-cli SET message 'Hello from VM2'", timeout=10)

        # Test VM1 -> VM2: Read VM2's key from VM1
        logger.info("  VM1 reading from VM2's Redis (vm2:6379)...")
        result1 = vm1.execute("redis-cli -h vm2 GET message", timeout=10)

        if "Hello from VM2" in result1.stdout:
            logger.info("  OK: VM1 -> VM2 Redis connection successful")
            logger.info(f"    Received: {result1.stdout.strip()}")
            results["vm_to_vm_tcp"] = True
        else:
            logger.error("  FAIL: VM1 -> VM2 Redis connection failed")
            logger.error(f"    stdout: {result1.stdout}")
            logger.error(f"    stderr: {result1.stderr}")

        # Test VM2 -> VM1: Read VM1's key from VM2
        logger.info("  VM2 reading from VM1's Redis (vm1:6379)...")
        result2 = vm2.execute("redis-cli -h vm1 GET message", timeout=10)

        if "Hello from VM1" in result2.stdout:
            logger.info("  OK: VM2 -> VM1 Redis connection successful")
            logger.info(f"    Received: {result2.stdout.strip()}")
        else:
            logger.error("  FAIL: VM2 -> VM1 Redis connection failed")
            logger.error(f"    stdout: {result2.stdout}")
            logger.error(f"    stderr: {result2.stderr}")
            results["vm_to_vm_tcp"] = False

        # =====================================================================
        # Summary
        # =====================================================================
        logger.info("")
        logger.info("=" * 70)
        logger.info("TEST RESULTS")
        logger.info("=" * 70)
        logger.info(f"Session ID:     {session.session_id}")
        logger.info(f"VM1 job_id:     {vm1.job_id}")
        logger.info(f"VM2 job_id:     {vm2.job_id}")
        logger.info("")
        logger.info("Test Results:")
        logger.info(f"  VM-to-VM Ping:      {'PASS' if results['vm_to_vm_ping'] else 'FAIL'}")
        logger.info(f"  VM-to-VM TCP:       {'PASS' if results['vm_to_vm_tcp'] else 'FAIL'}")
        logger.info(
            f"  Gateway SSH (VM1):  {'PASS' if results['gateway_ssh_vm1'] else 'FAIL' if not skip_gateway_test else 'SKIP'}"
        )
        logger.info(
            f"  Gateway SSH (VM2):  {'PASS' if results['gateway_ssh_vm2'] else 'FAIL' if not skip_gateway_test else 'SKIP'}"
        )
        logger.info("")

        all_passed = all(
            [
                results["vm_to_vm_ping"],
                results["vm_to_vm_tcp"],
                skip_gateway_test or results["gateway_ssh_vm1"],
                skip_gateway_test or results["gateway_ssh_vm2"],
            ]
        )

        if all_passed:
            logger.info("OVERALL: ALL TESTS PASSED")
        else:
            logger.error("OVERALL: SOME TESTS FAILED")

        logger.info("=" * 70)

        return 0 if all_passed else 1

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        breakpoint()
        if session:
            logger.info("Closing session...")
            session.close()
        plato.close()


if __name__ == "__main__":
    sys.exit(main())
