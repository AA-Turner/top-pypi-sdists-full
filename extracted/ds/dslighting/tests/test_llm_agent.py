"""
测试真正的 LLM Agent

这个测试展示了如何使用 IntelligentLLMAgentWorkflow
- LLM 做决策
- Sandbox 执行
- 标准 I/O
- 工具调度
"""

import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/test_pip_dslighting/intelligent_llm_agent')

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG)

from intelligent_llm_agent.workflow import IntelligentLLMAgentWorkflow

from dsat.services.workspace import WorkspaceService
from dsat.services.llm import LLMService
from dsat.services.sandbox import SandboxService
from dsat.operators.llm_basic import GenerateCodeAndPlanOperator, ReviewOperator
from dsat.operators.code import ExecuteAndTestOperator
from dsat.services.states.journal import JournalState
from pathlib import Path

# 创建配置
class MockConfig:
    """模拟配置"""
    def __init__(self):
        self.llm = type('obj', (object,), {
            'model': 'gpt-4o',
            'temperature': 0.7,
            'api_key': None
        })()
        self.sandbox = type('obj', (object,), {'timeout': 300})()
        self.run = type('obj', (object,), {'name': 'test_run'})()

def test_llm_agent():
    """测试 LLM Agent"""
    print("="*80)
    print("测试 Intelligent LLM Agent")
    print("="*80)

    # 创建配置
    config = MockConfig()

    # 创建服务
    workspace = WorkspaceService(run_name="test_intelligent_agent")
    llm_service = LLMService(config=config.llm)
    sandbox_service = SandboxService(workspace=workspace, timeout=config.sandbox.timeout)
    state = JournalState()

    # 创建 operators
    operators = {
        "generate": GenerateCodeAndPlanOperator(llm_service=llm_service),
        "execute": ExecuteAndTestOperator(sandbox_service=sandbox_service),
        "review": ReviewOperator(llm_service=llm_service),
    }

    # 创建 services
    services = {
        "llm": llm_service,
        "sandbox": sandbox_service,
        "state": state,
        "workspace": workspace,
    }

    # 创建 agent config
    agent_config = {
        "max_iterations": 3,
        "temperature": 0.7
    }

    # 创建 workflow
    workflow = IntelligentLLMAgentWorkflow(
        operators=operators,
        services=services,
        agent_config=agent_config
    )

    # 运行（异步）
    import asyncio

    async def run_workflow():
        data_dir = Path("/Users/liufan/Applications/Github/dslighting/data/competitions/bike-sharing-demand")
        output_path = Path("/Users/liufan/Applications/Github/test_pip_dslighting/submission.csv")

        await workflow.solve(
            description="预测 bike sharing demand",
            io_instructions="读取 train.csv，训练模型，预测 test.csv，保存到 submission.csv",
            data_dir=data_dir,
            output_path=output_path
        )

    # 运行
    asyncio.run(run_workflow())

    print("\n✓ 测试完成")


if __name__ == "__main__":
    test_llm_agent()
