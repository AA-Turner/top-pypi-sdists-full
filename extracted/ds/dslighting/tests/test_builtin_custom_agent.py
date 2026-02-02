"""
测试通过 DSLighting 使用自定义 Agent

展示如何：
1. 通过 DSLighting.Agent(workflow="my_custom_agent") 使用自定义 Agent
2. 像使用内置 workflow 一样使用自定义 Agent
3. 完全集成到 DSLighting 系统中
"""

from dotenv import load_dotenv
load_dotenv()

import dslighting
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def main():
    print("\n" + "="*80)
    print("测试通过 DSLighting 使用自定义 Agent")
    print("="*80)

    # ========== 方式 1: 使用 DSLighting.Agent ==========
    print("\n方式 1: 使用 DSLighting.Agent(workflow='my_custom_agent')")
    print("-"*80)

    agent = dslighting.Agent(
        workflow="my_custom_agent",  # ← 使用自定义 Agent！
        model="gpt-4o",
        temperature=0.7,
        max_iterations=3,  # 少量迭代以节省成本
        keep_workspace=True,  # 保留工作区以便调试
        verbose=True
    )

    print("✓ Agent 创建成功")
    print(f"  Workflow: {agent.config.workflow.name}")
    print(f"  Model: {agent.config.llm.model}")

    # ========== 方式 2: 在真实数据集上运行 ==========
    print("\n方式 2: 在 bike-sharing-demand 上运行")
    print("-"*80)

    data_dir = Path("/Users/liufan/Applications/Github/dslighting/data/competitions/bike-sharing-demand")

    if not data_dir.exists():
        print(f"✗ 数据目录不存在: {data_dir}")
        print("\n请确保数据目录存在，或修改 data_dir 为有效路径")
        return

    print(f"✓ 数据目录: {data_dir}")

    # 运行 Agent
    print("\n开始运行自定义 Agent...")
    print("="*80)
    print()

    result = agent.run(
        data=data_dir,
        description="预测 bike sharing demand（共享单车租赁需求预测）",
        output_path="submission.csv"
    )

    # ========== 显示结果 ==========
    print("\n" + "="*80)
    print("执行完成！")
    print("="*80)

    print(f"\n结果:")
    print(f"  Success: {result.success}")
    print(f"  Score: {result.score}")
    print(f"  Cost: ${result.cost:.4f}")
    print(f"  Duration: {result.duration:.1f}s")
    print(f"  Workspace: {result.workspace_path}")
    print(f"  Artifacts: {result.artifacts_path}")

    if result.success:
        print(f"\n✓ 任务成功完成！")
        if result.output:
            print(f"  Output: {result.output}")
    else:
        print(f"\n✗ 任务失败")
        if result.error:
            print(f"  Error: {result.error}")

    # ========== 显示如何访问内部组件 ==========
    print("\n" + "="*80)
    print("访问底层 DSAT 组件（高级用法）")
    print("="*80)

    config = agent.get_config()
    print(f"\nConfig:")
    print(f"  Workflow: {config.workflow.name}")
    print(f"  Model: {config.llm.model}")
    print(f"  Temperature: {config.llm.temperature}")

    runner = agent.get_runner()
    if runner:
        print(f"\nRunner:")
        print(f"  Factory: {type(runner.factory).__name__}")
        print(f"  Available workflows: {', '.join(runner.factories.keys())}")

    print("\n" + "="*80)
    print("\n💡 关键要点:")
    print("  1. ✓ 自定义 Agent 已完全集成到 DSLighting")
    print("  2. ✓ 可以像使用内置 workflow 一样使用")
    print("  3. ✓ 通过 workflow='my_custom_agent' 调用")
    print("  4. ✓ 完全基于 DSAT 框架实现")
    print("  5. ✓ 可以使用所有 DSAT 组件")

    print("\n📁 文件位置:")
    print("  - Workflow: /Users/liufan/Applications/Github/dslighting/dsat/workflows/manual/my_custom_agent_workflow.py")
    print("  - Factory: /Users/liufan/Applications/Github/dslighting/dsat/workflows/factory.py")
    print("  - Registry: /Users/liufan/Applications/Github/dslighting/dsat/runner.py")

    print("\n🔧 添加自己的 Agent:")
    print("  1. 在 dsat/workflows/manual/ 或 dsat/workflows/search/ 创建 workflow.py")
    print("  2. 在 dsat/workflows/factory.py 创建 Factory 类")
    print("  3. 在 dsat/workflows/__init__.py 导出 Factory")
    print("  4. 在 dsat/runner.py 的 WORKFLOW_FACTORIES 注册")
    print("  5. 通过 DSLighting.Agent(workflow='your_agent_name') 使用")

    print("\n" + "="*80)
    print("完成！")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
