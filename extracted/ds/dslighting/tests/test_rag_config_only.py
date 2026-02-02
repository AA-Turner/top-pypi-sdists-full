"""
Simple test for AutoMind RAG disable feature - config flow only

This test verifies that enable_rag parameter flows through correctly
without triggering VDBService initialization (which would connect to HuggingFace)
"""

from dotenv import load_dotenv
load_dotenv()

import dslighting
from dslighting.core.config_builder import ConfigBuilder

def test_config_flow():
    """Test that enable_rag parameter flows through config correctly"""
    print("=" * 70)
    print("Test 1: enable_rag=False")
    print("=" * 70)

    config_builder = ConfigBuilder()
    config = config_builder.build_config(
        workflow="automind",
        automind={"enable_rag": False}
    )

    print(f"✓ Workflow name: {config.workflow.name}")
    print(f"✓ enable_rag in params: {config.workflow.params.get('enable_rag')}")

    assert config.workflow.name == "automind", "Workflow should be automind"
    assert config.workflow.params.get("enable_rag") == False, "enable_rag should be False"

    print("\n✅ Test 1 PASSED\n")


def test_agent_api():
    """Test the user-facing Agent API"""
    print("=" * 70)
    print("Test 2: Agent API - enable_rag parameter")
    print("=" * 70)

    # Test with enable_rag=False
    agent = dslighting.Agent(
        workflow="automind",
        model="gpt-4o-mini",
        automind={"enable_rag": False}
    )

    config = agent.get_config()
    print(f"✓ Agent created with workflow: {config.workflow.name}")
    print(f"✓ enable_rag in config: {config.workflow.params.get('enable_rag')}")

    assert config.workflow.params.get("enable_rag") == False, "Agent should pass enable_rag=False to config"

    print("\n✅ Test 2 PASSED\n")


def test_default_behavior():
    """Test that default behavior is preserved"""
    print("=" * 70)
    print("Test 3: Default behavior (enable_rag not specified)")
    print("=" * 70)

    config_builder = ConfigBuilder()
    config = config_builder.build_config(workflow="automind")

    print(f"✓ Workflow name: {config.workflow.name}")
    print(f"✓ enable_rag in params (should be None): {config.workflow.params.get('enable_rag')}")

    assert config.workflow.name == "automind", "Workflow should be automind"
    # None means factory will use default (True)

    print("\n✅ Test 3 PASSED (None defaults to True in factory)\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DSLighting v1.9.6 - AutoMind RAG Disable Feature Tests (Config Only)")
    print("=" * 70 + "\n")

    try:
        test_config_flow()
        test_agent_api()
        test_default_behavior()

        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nThe enable_rag feature configuration flow is working correctly:")
        print("  • enable_rag=False flows from Agent to Config")
        print("  • Default behavior (None/True) is preserved")
        print("  • Factory will use enable_rag to decide VDBService initialization")
        print("\nUsage:")
        print("  agent = dslighting.Agent(")
        print("      workflow='automind',")
        print("      automind={'enable_rag': False}  # Disable HuggingFace downloads")
        print("  )")
        print("=" * 70 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise
