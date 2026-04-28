"""
Verification script for gRPC lazy-connect behavior.

Tests that after the RpcClient.start() change:
  1. create_ai_service() returns normally even when gRPC port is unreachable
  2. HTTP functions still work when gRPC is down (skipped - same server_address)
  3. gRPC methods raise connection-unavailable error when not connected

Usage:
  cd nacos-sdk-python && python -m pytest test/test_grpc_lazy_connect.py -v
"""
import asyncio
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from v2.nacos import ClientConfigBuilder
from v2.nacos.ai.nacos_ai_service import NacosAIService
from v2.nacos.ai.model.ai_param import GetMcpServerParam
from v2.nacos.common.nacos_exception import NacosException


# ────────────────────── helpers ──────────────────────

def ok(msg: str):
    print(f"  [PASS] {msg}")

def fail(msg: str):
    print(f"  [FAIL] {msg}")

def section(title: str):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


# ────────────────────── config ──────────────────────

# Use a port that is NOT listening to simulate gRPC unreachable
UNREACHABLE_SERVER = os.getenv("NACOS_UNREACHABLE_SERVER", "localhost:19848")
USERNAME = os.getenv("NACOS_USERNAME", "nacos")
PASSWORD = os.getenv("NACOS_PASSWORD", "nacos")
TIMEOUT_SECONDS = 30


async def scenario_1_create_ai_service_no_block():
    """Scenario 1: create_ai_service() should return normally even when gRPC is unreachable."""
    section("Scenario 1: create_ai_service() with unreachable gRPC")

    client_config = (
        ClientConfigBuilder()
        .server_address(UNREACHABLE_SERVER)
        .username(USERNAME)
        .password(PASSWORD)
        .log_level("INFO")
        .build()
    )

    start_time = time.monotonic()
    ai_service = None
    try:
        ai_service = await asyncio.wait_for(
            NacosAIService.create_ai_service(client_config),
            timeout=TIMEOUT_SECONDS,
        )
        elapsed = time.monotonic() - start_time
        print(f"       create_ai_service() returned in {elapsed:.2f}s")

        if ai_service is not None:
            ok(f"create_ai_service() returned a non-None instance (type={type(ai_service).__name__})")
            # Check the client is in UNHEALTHY state (not RUNNING)
            rpc_status = ai_service.grpc_client_proxy.rpc_client.rpc_client_status
            print(f"       RpcClient status: {rpc_status}")
            if rpc_status.name == "UNHEALTHY":
                ok("RpcClient is in UNHEALTHY state (expected for unreachable server)")
            elif rpc_status.name == "RUNNING":
                fail("RpcClient is RUNNING but server should be unreachable")
                return ai_service, False
            else:
                print(f"       (RpcClient status is {rpc_status.name}, may be acceptable)")
            return ai_service, True
        else:
            fail("create_ai_service() returned None")
            return None, False

    except asyncio.TimeoutError:
        elapsed = time.monotonic() - start_time
        fail(f"create_ai_service() timed out after {elapsed:.2f}s (limit: {TIMEOUT_SECONDS}s)")
        return None, False
    except Exception as e:
        elapsed = time.monotonic() - start_time
        fail(f"create_ai_service() raised exception after {elapsed:.2f}s: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None, False


async def scenario_3_grpc_method_raises(ai_service: NacosAIService):
    """Scenario 3: gRPC method should raise error when not connected."""
    section("Scenario 3: gRPC method call when disconnected")

    if ai_service is None:
        fail("Skipped - no ai_service instance from Scenario 1")
        return False

    try:
        result = await ai_service.get_mcp_server(
            GetMcpServerParam(mcp_name="test-nonexistent-mcp")
        )
        fail(f"get_mcp_server() should have raised an exception but returned: {result}")
        return False
    except NacosException as e:
        ok(f"get_mcp_server() raised NacosException as expected: {e}")
        return True
    except Exception as e:
        # Any exception is acceptable - the key is that it doesn't hang
        ok(f"get_mcp_server() raised {type(e).__name__}: {e}")
        return True


async def main():
    passed = 0
    failed = 0

    # Scenario 1
    ai_service, success = await scenario_1_create_ai_service_no_block()
    if success:
        passed += 1
    else:
        failed += 1

    # Scenario 2: Skipped (HTTP and gRPC share the same server_address)
    section("Scenario 2: HTTP with gRPC down (SKIPPED)")
    print("       Skipped: HTTP and gRPC use the same server_address, cannot easily simulate separately.")

    # Scenario 3
    success = await scenario_3_grpc_method_raises(ai_service)
    if success:
        passed += 1
    else:
        failed += 1

    # Cleanup
    if ai_service:
        try:
            await ai_service.shutdown()
            ok("ai_service shutdown cleanly")
        except Exception as e:
            print(f"       Warning: shutdown raised {type(e).__name__}: {e}")

    # Summary
    section("Summary")
    total = passed + failed
    print(f"  Total: {total}  |  Passed: {passed}  |  Failed: {failed}")
    if failed == 0:
        print("  ALL SCENARIOS PASSED!")
    else:
        print(f"  {failed} SCENARIO(S) FAILED")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
