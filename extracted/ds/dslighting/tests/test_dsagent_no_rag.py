"""
Test script for DS-Agent RAG disable feature - config flow only

This test verifies that enable_rag parameter flows through correctly
for DS-Agent workflow (similar to AutoMind).
"""

from dotenv import load_dotenv
load_dotenv()

import dslighting
from dslighting.core.config_builder import ConfigBuilder

def test_dsagent_config_flow():
    """Test that enable_rag parameter flows through config correctly for DS-Agent"""
    print("=" * 70)
    print("Test 1: DS-Agent - enable_rag=False")
    print("=" * 70)

    config_builder = ConfigBuilder()
    config = config_builder.build_config(
        workflow="dsagent",
        dsagent={"enable_rag": False}
    )

    print(f"✓ Workflow name: {config.workflow.name}")
    print(f"✓ enable_rag in params: {config.workflow.params.get('enable_rag')}")

    assert config.workflow.name == "dsagent", "Workflow should be dsagent"
    assert config.workflow.params.get("enable_rag") == False, "enable_rag should be False"

    print("\n✅ Test 1 PASSED\n")


def test_dsagent_agent_api():
    """Test the user-facing Agent API for DS-Agent"""
    print("=" * 70)
    print("Test 2: DS-Agent API - enable_rag parameter")
    print("=" * 70)

    # Test with enable_rag=False
    agent = dslighting.Agent(
        workflow="dsagent",
        model="gpt-4o-mini",
        dsagent={"enable_rag": False}
    )

    config = agent.get_config()
    print(f"✓ Agent created with workflow: {config.workflow.name}")
    print(f"✓ enable_rag in config: {config.workflow.params.get('enable_rag')}")

    assert config.workflow.params.get("enable_rag") == False, "Agent should pass enable_rag=False to config"

    print("\n✅ Test 2 PASSED\n")


def test_both_workflows():
    """Test that both AutoMind and DS-Agent support enable_rag"""
    print("=" * 70)
    print("Test 3: Both AutoMind and DS-Agent support enable_rag")
    print("=" * 70)

    # Test AutoMind
    agent_automind = dslighting.Agent(
        workflow="automind",
        automind={"enable_rag": False}
    )
    config_automind = agent_automind.get_config()
    print(f"✓ AutoMind enable_rag: {config_automind.workflow.params.get('enable_rag')}")

    # Test DS-Agent
    agent_dsagent = dslighting.Agent(
        workflow="dsagent",
        dsagent={"enable_rag": False}
    )
    config_dsagent = agent_dsagent.get_config()
    print(f"✓ DS-Agent enable_rag: {config_dsagent.workflow.params.get('enable_rag')}")

    assert config_automind.workflow.params.get("enable_rag") == False
    assert config_dsagent.workflow.params.get("enable_rag") == False

    print("\n✅ Test 3 PASSED - Both workflows support enable_rag\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DSLighting v1.9.7 - DS-Agent RAG Disable Feature Tests")
    print("=" * 70 + "\n")

    try:
        test_dsagent_config_flow()
        test_dsagent_agent_api()
        test_both_workflows()

        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nBoth AutoMind and DS-Agent now support enable_rag parameter:")
        print("  • AutoMind (v1.9.6)")
        print("  • DS-Agent (v1.9.7)")
        print("\nUsage:")
        print("  # AutoMind")
        print("  agent = dslighting.Agent(")
        print("      workflow='automind',")
        print("      automind={'enable_rag': False}")
        print("  )")
        print()
        print("  # DS-Agent")
        print("  agent = dslighting.Agent(")
        print("      workflow='dsagent',")
        print("      dsagent={'enable_rag': False}")
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
