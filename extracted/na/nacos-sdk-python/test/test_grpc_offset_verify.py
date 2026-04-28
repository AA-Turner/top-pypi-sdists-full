"""
Verify: when gRPC is unreachable (wrong port offset) but HTTP is fine,
Skill download still works via HTTP.

Setup:
  - gRPC port offset = 9000  →  tries 8848+9000 = 17848 (unreachable)
  - HTTP still connects to 8848 (normal)

Usage:
  cd nacos-sdk-python && python -m test.test_grpc_offset_verify
"""
import asyncio
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from v2.nacos.common.client_config import GRPCConfig
from v2.nacos.common.client_config_builder import ClientConfigBuilder
from v2.nacos.ai.nacos_ai_service import NacosAIService
from v2.nacos.ai.model.ai_param import DownloadSkillParam, GetPromptParam


SERVER_ADDR = os.getenv("NACOS_SERVER_ADDR", "localhost:8848")
USERNAME = os.getenv("NACOS_USERNAME", "nacos")
PASSWORD = os.getenv("NACOS_PASSWORD", "nacos")
WRONG_GRPC_OFFSET = 9000  # gRPC → 8848+9000=17848 (unreachable)

SKILL_NAME = "test-skill-e2e"
PROMPT_KEY = "test-prompt-e2e"


async def main():
    passed = 0
    failed = 0

    # ── Build client config with wrong gRPC offset ──
    grpc_config = GRPCConfig(port_offset=WRONG_GRPC_OFFSET)
    client_config = (
        ClientConfigBuilder()
        .server_address(SERVER_ADDR)
        .username(USERNAME)
        .password(PASSWORD)
        .grpc_config(grpc_config)
        .build()
    )

    print(f"gRPC port offset = {WRONG_GRPC_OFFSET}")
    print(f"gRPC will try port {8848 + WRONG_GRPC_OFFSET} (should be unreachable)")
    print(f"HTTP will use port 8848 (should be fine)")
    print()

    # ================================================================
    #  Test 1: create_ai_service with wrong gRPC offset
    # ================================================================
    print("Test 1: create_ai_service with wrong gRPC offset...")
    ai_service = None
    try:
        ai_service = await NacosAIService.create_ai_service(client_config)
        print(f"  PASS - AIService created, type={type(ai_service).__name__}")
        passed += 1
    except Exception as e:
        print(f"  FAIL - Could not create AIService: {type(e).__name__}: {e}")
        traceback.print_exc()
        failed += 1
        print("\nCannot proceed without ai_service. Exiting.")
        print(f"\nResults: passed={passed}, failed={failed}")
        return

    # ================================================================
    #  Test 2: download_skill_zip via HTTP (should work)
    # ================================================================
    print("\nTest 2: download_skill_zip via HTTP (should work)...")
    try:
        zip_bytes = await ai_service.download_skill_zip(
            DownloadSkillParam(skill_name=SKILL_NAME))
        print(f"  PASS - Downloaded {len(zip_bytes)} bytes")
        passed += 1
    except Exception as e:
        print(f"  FAIL - {type(e).__name__}: {e}")
        traceback.print_exc()
        failed += 1

    # ================================================================
    #  Test 3: get_prompt via gRPC (should fail - port unreachable)
    # ================================================================
    print("\nTest 3: get_prompt via gRPC (should fail)...")
    try:
        result = await ai_service.get_prompt(
            GetPromptParam(prompt_key=PROMPT_KEY))
        print(f"  UNEXPECTED PASS - Got prompt: promptKey={result.promptKey}")
        failed += 1
    except Exception as e:
        print(f"  PASS (expected error) - {type(e).__name__}: {e}")
        passed += 1

    # ================================================================
    #  Cleanup & Summary
    # ================================================================
    try:
        await ai_service.shutdown()
    except Exception:
        pass

    print(f"\n{'='*60}")
    print(f"  Results: passed={passed}, failed={failed}")
    total = passed + failed
    if failed == 0:
        print("  ALL TESTS PASSED!")
    else:
        print(f"  {failed}/{total} TEST(S) FAILED")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
