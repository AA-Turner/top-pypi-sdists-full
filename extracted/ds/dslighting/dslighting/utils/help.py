"""Help and documentation utilities for DSLighting."""


def show_help():
    """Show DSLighting 2.0 help and quick start guide."""
    print("=" * 70)
    print("DSLighting 2.0 - Data Science Agent Framework")
    print("=" * 70)
    print()
    print("🚀 Quick Start:")
    print("-" * 70)
    print("""
# Scenario 1: One-liner (simplest)
from dslighting import run_agent
result = run_agent(task_id="bike-sharing-demand")

# Scenario 2: Use Agent with preset workflow
from dslighting import Agent
agent = Agent(workflow="aide")
result = agent.run(data="path/to/data")

# Scenario 3: Custom agent with patterns
from dslighting import IterativeAgent, PromptBuilder

agent = IterativeAgent(operators, services, agent_config)
await agent.solve(description, io_instructions, data_dir, output_path)
""")

    print("\n📋 Available Workflows (from DSAT):")
    print("-" * 70)
    print("""
Manual Workflows:
  1. AIDE              - Adaptive Iteration & Debugging Enhancement
  2. AutoKaggle        - Advanced competition solver
  3. DataInterpreter   - Data analysis and exploration
  4. DeepAnalyze       - Analysis-focused workflow
  5. DSAgent           - Structured operator-based workflow

Search Workflows:
  6. AutoMind          - Planning + reasoning with knowledge base
  7. AFlow             - Meta-optimization workflow selector
""")

    print("\n🧱 Five Layer Architecture:")
    print("-" * 70)
    print("""
  1. 🧠 agents/     - BaseAgent, SimpleAgent, IterativeAgent, presets, strategies
  2. 💪 operators/  - LLM, code, data, orchestration (Pipeline, Parallel)
  3. ⚙️ services/   - LLMService, SandboxService, WorkspaceService
  4. 📝 state/      - JournalState, Experience, MemoryManager
  5. 🗣️ prompts/    - PromptBuilder, templates
""")

    print("\n📚 Documentation:")
    print("-" * 70)
    print("""
  GitHub:  https://github.com/usail-hkust/dslighting
  PyPI:    https://pypi.org/project/dslighting/
""")


def list_workflows():
    """List all available workflows."""
    print("=" * 70)
    print("DSLighting 2.0 Workflows (from DSAT)")
    print("=" * 70)
    print()

    workflows = [
        ("AIDE", "Adaptive Iteration & Debugging Enhancement",
         "Most data science tasks", "gpt-4o"),
        ("AutoKaggle", "Competition-solving agent",
         "Kaggle competitions, benchmarks", "gpt-4o"),
        ("DataInterpreter", "Data analysis and exploration",
         "Data exploration, EDA", "gpt-4o-mini"),
        ("DeepAnalyze", "Analysis-focused workflow",
         "Deep analysis tasks", "gpt-4o"),
        ("DSAgent", "Structured operator-based workflow",
         "Tasks with logging", "gpt-4o"),
        ("AutoMind", "Planning + reasoning with knowledge base",
         "Tasks requiring RAG", "gpt-4o"),
        ("AFlow", "Meta-optimization workflow selector",
         "Automated workflow selection", "gpt-4o"),
    ]

    for name, full_name, use_case, model in workflows:
        print(f"  {name}")
        print(f"    Full Name: {full_name}")
        print(f"    Use Case: {use_case}")
        print(f"    Default Model: {model}")
        print()


def show_example(workflow_name: str):
    """Show workflow example code."""
    examples = {
        "aide": """
from dslighting import Agent

agent = Agent(workflow="aide", model="gpt-4o")
result = agent.run(data="path/to/data")
print(f"Success: {result.success}")
""",
        "autokaggle": """
from dslighting import Agent

agent = Agent(workflow="autokaggle", model="gpt-4o")
result = agent.run(data="path/to/data")
print(f"Success: {result.success}")
""",
        "data_interpreter": """
from dslighting import Agent

agent = Agent(workflow="data_interpreter", model="gpt-4o")
result = agent.run(data="path/to/data")
print(f"Success: {result.success}")
""",
    }

    if workflow_name.lower() in examples:
        print(examples[workflow_name.lower()])
    else:
        print(f"Unknown workflow: {workflow_name}")
        print(f"Available: {', '.join(examples.keys())}")


def explore():
    """Interactive exploration of DSLighting components."""
    print("=" * 80)
    print("DSLighting 2.0 - Component Explorer")
    print("=" * 80)
    print()

    # Prompts
    print("\n🗣️  Available Prompts")
    print("-" * 80)
    prompts = list_prompts()
    for category, functions in prompts.items():
        if functions:
            print(f"\n{category.upper()} ({len(functions)} items):")
            for func in functions[:5]:  # Show first 5
                print(f"  - {func}")
            if len(functions) > 5:
                print(f"  ... and {len(functions) - 5} more")

    # Operators
    print("\n\n💪 Available Operators")
    print("-" * 80)
    operators = list_operators()
    for category, names in operators.items():
        if names:
            print(f"\n{category.upper()} ({len(names)} items):")
            for name in names[:5]:  # Show first 5
                print(f"  - {name}")
            if len(names) > 5:
                print(f"  ... and {len(names) - 5} more")

    # Workflows
    print("\n\n🚀 Available Workflows")
    print("-" * 80)
    print("""
  AIDE              - Adaptive Iteration & Debugging Enhancement
  AutoKaggle        - Competition-solving agent
  DataInterpreter   - Data analysis and exploration
  DeepAnalyze       - Analysis-focused workflow
  DSAgent           - Structured operator-based workflow
  AutoMind          - Planning + reasoning with knowledge base
  AFlow             - Meta-optimization workflow selector
    """)

    print("\n" + "=" * 80)
    print("For more information:")
    print("  - dslighting.help()              - Show quick start guide")
    print("  - dslighting.list_workflows()    - List all workflows")
    print("  - dslighting.list_prompts()      - List all prompts")
    print("  - dslighting.list_operators()    - List all operators")
    print("=" * 80)


def list_prompts():
    """Dummy function - real implementation in prompts module."""
    return {}


def list_operators():
    """Dummy function - real implementation in operators module."""
    return {}
