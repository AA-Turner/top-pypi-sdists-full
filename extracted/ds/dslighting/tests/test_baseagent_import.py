"""
Test BaseAgent import from PyPI package
"""

print("=" * 80)
print("Testing BaseAgent Import")
print("=" * 80)

# Test 1: Check if BaseAgent is None
print("\nTest 1: from dslighting import BaseAgent")
try:
    from dslighting import BaseAgent
    print(f"✓ BaseAgent imported successfully")
    print(f"  BaseAgent = {BaseAgent}")
    print(f"  Type: {type(BaseAgent)}")

    if BaseAgent is None:
        print("  ⚠️  WARNING: BaseAgent is None!")
    else:
        print(f"  ✓ BaseAgent is not None")
        print(f"  Module: {BaseAgent.__module__}")
except ImportError as e:
    print(f"✗ Failed to import: {e}")

# Test 2: Try from dslighting.agents
print("\nTest 2: from dslighting.agents import BaseAgent")
try:
    from dslighting.agents import BaseAgent
    print(f"✓ BaseAgent imported from agents")
    print(f"  BaseAgent = {BaseAgent}")
except ImportError as e:
    print(f"✗ Failed: {e}")

# Test 3: Try direct DSAT import
print("\nTest 3: from dsat.workflows.base import BaseWorkflow")
try:
    from dsat.workflows.base import BaseWorkflow
    print(f"✓ BaseWorkflow imported from dsat")
    print(f"  BaseWorkflow = {BaseWorkflow}")
except ImportError as e:
    print(f"✗ Failed: {e}")

# Test 4: Check dslighting.agents module
print("\nTest 4: Check dslighting.agents module")
try:
    import dslighting.agents
    print(f"✓ dslighting.agents module loaded")
    print(f"  __file__: {dslighting.agents.__file__}")
    print(f"  __all__: {dslighting.agents.__all__}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 80)
