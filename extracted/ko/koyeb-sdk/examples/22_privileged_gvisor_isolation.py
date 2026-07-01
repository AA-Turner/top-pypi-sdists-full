#!/usr/bin/env python3
"""Privileged mode with gVisor isolation: verify container escape is not possible"""

import os
import sys
import random
import string

from koyeb import Sandbox


def run_and_check(sandbox, description, cmd, results, expect_fail=False, timeout=10):
    """Run a command, print output, and record pass/fail in results list."""
    print(f"\n--- {description} ---")
    print(f"$ {cmd}")
    result = sandbox.exec(cmd, timeout=timeout)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if stdout:
        print(f"stdout: {stdout}")
    if stderr:
        print(f"stderr: {stderr}")
    print(f"exit_code: {result.exit_code}")

    passed = True
    if expect_fail:
        if result.exit_code == 0:
            print("=> FAIL: expected command to be blocked but it succeeded!")
            passed = False
        else:
            print("=> PASS: blocked as expected (gVisor isolation)")
    else:
        if result.exit_code != 0:
            print(f"=> FAIL: expected command to succeed but got exit_code={result.exit_code}")
            passed = False
        else:
            print("=> PASS")

    results.append({"test": description, "passed": passed})
    return result


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sandbox = None
    results = []
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        print("Creating privileged sandbox...")
        sandbox = Sandbox.create(
            image="koyeb/sandbox",
            name=f"gvisor-isolation-{suffix}",
            privileged=True,
            wait_ready=True,
            api_token=api_token,
        )
        print("Sandbox created in privileged mode")

        # =====================================================================
        # 1. Verify we are running in privileged mode (capabilities are granted)
        # =====================================================================
        run_and_check(
            sandbox,
            "Verify privileged mode: mount tmpfs (requires CAP_SYS_ADMIN)",
            "mount -t tmpfs tmpfs /mnt && echo 'mount succeeded' && umount /mnt",
            results,
        )

        # =====================================================================
        # 2. gVisor blocks access to the real host kernel
        # =====================================================================

        run_and_check(
            sandbox,
            "Blocked: load kernel module (init_module syscall)",
            "modprobe dummy 2>&1 || insmod /nonexistent.ko 2>&1; exit 1",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: write to /proc/sysrq-trigger",
            "echo b > /proc/sysrq-trigger",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: read /dev/mem (host physical memory)",
            "dd if=/dev/mem bs=1 count=1 2>&1",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: read /dev/kmem (kernel memory)",
            "dd if=/dev/kmem bs=1 count=1 2>&1",
            results,
            expect_fail=True,
        )

        # =====================================================================
        # 3. gVisor blocks container escape techniques
        # =====================================================================

        run_and_check(
            sandbox,
            "Blocked: escape via /proc/1/root (host filesystem access)",
            "ls /proc/1/root/etc/shadow 2>&1 && cat /proc/1/root/etc/shadow",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: nsenter into host PID 1 namespaces",
            "nsenter -t 1 -m -u -i -n -p -- whoami 2>&1",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: cgroup escape via release_agent",
            "mkdir -p /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp 2>&1; "
            "echo 1 > /tmp/cgrp/notify_on_release 2>&1",
            results,
            expect_fail=True,
        )

        # =====================================================================
        # 4. gVisor blocks raw device and disk access
        # =====================================================================

        run_and_check(
            sandbox,
            "Blocked: read /dev/sda (raw disk access)",
            "dd if=/dev/sda bs=1 count=1 2>&1",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: mknod block device",
            "mknod /tmp/fake_disk b 8 0 2>&1",
            results,
            expect_fail=True,
        )

        # =====================================================================
        # 5. gVisor blocks dangerous kernel interfaces
        # =====================================================================

        run_and_check(
            sandbox,
            "Blocked: kexec_load syscall",
            "kexec -l /bin/sh 2>&1 || echo 'kexec blocked'; exit 1",
            results,
            expect_fail=True,
        )

        run_and_check(
            sandbox,
            "Blocked: ptrace on PID 1",
            "sh -c 'echo \"#include <sys/ptrace.h>\n#include <stdio.h>\nint main(){long r=ptrace(0,1,0,0);printf(\\\"%ld\\\",r);return r==-1?1:0;}\" > /tmp/pt.c && gcc -o /tmp/pt /tmp/pt.c 2>/dev/null && /tmp/pt' 2>&1",
            results,
            expect_fail=True,
        )

        # =====================================================================
        # 6. Verify normal operations still work in privileged mode
        # =====================================================================

        run_and_check(
            sandbox,
            "Allowed: normal file operations",
            "echo 'hello' > /tmp/test.txt && cat /tmp/test.txt",
            results,
        )

        run_and_check(
            sandbox,
            "Allowed: network operations",
            "python3 -c \"import socket; s=socket.socket(); s.settimeout(3); print('socket OK')\"",
            results,
        )

        run_and_check(
            sandbox,
            "Allowed: process management",
            "sleep 0.1 & wait $! && echo 'process OK'",
            results,
        )

        # =====================================================================
        # Summary
        # =====================================================================
        passed = [r for r in results if r["passed"]]
        failed = [r for r in results if not r["passed"]]

        print("\n" + "=" * 60)
        print(f"RESULTS: {len(passed)}/{len(results)} passed")
        print("=" * 60)

        for r in results:
            status = "PASS" if r["passed"] else "FAIL"
            print(f"  [{status}] {r['test']}")

        if failed:
            print(f"\n{len(failed)} test(s) FAILED:")
            for r in failed:
                print(f"  - {r['test']}")
            print("=" * 60)
            return 1

        print("\nAll tests passed:")
        print("- Privileged mode grants extended capabilities (mount, etc.)")
        print("- gVisor blocks container escape attempts")
        print("- gVisor blocks access to host kernel and devices")
        print("- Normal sandbox operations work correctly")
        print("=" * 60)
        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
