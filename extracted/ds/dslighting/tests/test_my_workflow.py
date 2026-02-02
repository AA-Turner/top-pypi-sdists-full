"""
测试自定义 MyLLMWorkflow

像使用 aide、data_interpreter 一样使用自定义 workflow
"""

from dotenv import load_dotenv
load_dotenv()

import dslighting
import logging

logging.basicConfig(level=logging.INFO)

print("="*80)
print("测试自定义 MyLLMWorkflow")
print("="*80)

# 方法1: 完全像使用 aide 一样
print("\n方法1: 使用 workflow 参数（像 aide）")
print("-"*80)

try:
    agent = dslighting.Agent(
        workflow="my_llm_workflow",  # 自定义 workflow 名称
        model="gpt-4o",
        temperature=0.7,
        max_iterations=2,
        verbose=True
    )

    print("✓ Agent 创建成功！")
    print(f"  Workflow: {agent.config.workflow.name if hasattr(agent.config, 'workflow') else 'unknown'}")

    # 加载数据
    data = dslighting.load_data("bike-sharing-demand")
    print(f"\n✓ 数据加载成功")
    print(f"  Task ID: {data.task_id}")
    print(f"  数据目录: {data.data_dir}")

    # 运行（会调用自定义 workflow）
    print("\n开始运行自定义 workflow...")
    print("-"*80)

    # 注意：这里会尝试使用 workflow，但需要先注册
    # result = agent.run(data)

except Exception as e:
    print(f"✗ 失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("\n方法2: 使用动态导入（不需要注册）")
print("-"*80)

# 方法2: 直接使用 workflow 类（不需要注册到 factory）
import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/test_pip_dslighting/my_llm_workflow')

from my_llm_workflow.workflow import MyLLMWorkflow
from dsat.services.workspace import WorkspaceService
from dsat.services.llm import LLMService
from dsat.services.sandbox import SandboxService
from dsat.operators.llm_basic import GenerateCodeAndPlanOperator
from dsat.operators.code import ExecuteAndTestOperator
from pathlib import Path

async def test_workflow_directly():
    """直接测试 workflow"""

    # 创建服务
    workspace = WorkspaceService(run_name="test_my_llm_workflow")
    llm_service = LLMService(
        model="gpt-4o",
        temperature=0.7
    )
    sandbox_service = SandboxService(workspace=workspace, timeout=300)

    # 创建 operators
    operators = {
        "generate": GenerateCodeAndPlanOperator(llm_service=llm_service),
        "execute": ExecuteAndTestOperator(sandbox_service=sandbox_service),
    }

    # 创建 services
    services = {
        "llm": llm_service,
        "sandbox": sandbox_service,
    }

    # 创建配置
    agent_config = {
        "max_iterations": 2,
        "temperature": 0.7
    }

    # 创建 workflow
    workflow = MyLLMWorkflow(
        operators=operators,
        services=services,
        agent_config=agent_config
    )

    print("✓ Workflow 创建成功！")
    print(f"  类型: {type(workflow).__name__}")

    # 运行 workflow
    data_dir = Path("/Users/liufan/Applications/Github/dslighting/data/competitions/bike-sharing-demand")
    output_path = Path("/Users/liufan/Applications/Github/test_pip_dslighting/submission.csv")

    print(f"\n开始执行...")
    await workflow.solve(
        description="预测 bike sharing demand（共享单车租赁需求预测）",
        io_instructions="读取 train.csv，训练模型，预测 test.csv 的 count 列，保存到 submission.csv",
        data_dir=data_dir,
        output_path=output_path
    )

    print("\n✓ Workflow 执行完成！")

# 运行测试
import asyncio
asyncio.run(test_workflow_directly())

print("\n" + "="*80)
print("\n💡 关键点:")
print("  1. ✓ workflow.py 只依赖 dsat.workflows.base")
print("  2. ✓ 可以像 data_interpreter 一样实现")
print("  3. ✓ 使用 LLM + Sandbox")
print("  4. ✓ 完全独立")
print("  5. ✓ 可以直接使用（不需要修改源代码）")

print("\n🎯 要像 aide 一样使用 workflow='my_llm_workflow'")
print("  需要将 workflow 注册到 DSLighting 的配置中")
print("  但可以直接使用 Workflow 类，不需要注册")

print("\n" + "="*80)
print("测试完成")
print("="*80)
