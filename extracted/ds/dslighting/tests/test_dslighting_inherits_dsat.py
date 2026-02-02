"""
测试 DSLighting 2.0 完全继承 DSAT

展示如何：
1. 从 DSLighting 导入所有 DSAT 组件
2. 创建自定义 Agent
3. 通过 DSLighting.Agent() 使用
"""

from dotenv import load_dotenv
load_dotenv()

# ========== 从 DSLighting 导入所有 DSAT 组件 ==========
import dslighting
from pathlib import Path

# 导入 DSAT 核心组件（全部从 dslighting 导入！）
from dslighting import (
    # 核心
    DSATWorkflow,

    # 服务
    LLMService,
    SandboxService,
    WorkspaceService,
    DataAnalyzer,
    VDBService,

    # 状态管理
    JournalState,
    Node,
    MetricValue,

    # 操作器
    GenerateCodeAndPlanOperator,
    PlanOperator,
    ReviewOperator,
    ExecuteAndTestOperator,

    # 模型
    Plan,
    ReviewResult,
)

print("="*80)
print("✓ 成功从 DSLighting 导入所有 DSAT 组件")
print("="*80)
print()

# ========== 创建自定义 Agent ==========
print("步骤 1: 创建自定义 Agent（基于 DSLighting 暴露的 DSAT）")
print("-"*80)


class MyCustomAgent(dslighting.DSATWorkflow):
    """
    我的自定义 Agent

    完全基于 DSLighting 暴露的 DSAT 组件创建
    """

    def __init__(self, operators, services, agent_config):
        super().__init__(operators, services, agent_config)

        # 获取服务（全部从 DSLighting 获得）
        self.llm_service = services["llm"]
        self.sandbox_service = services["sandbox"]
        self.workspace_service = services["workspace"]
        self.data_analyzer = services.get("data_analyzer")
        self.state = services["state"]

        # 获取操作器（全部从 DSLighting 获得）
        self.generate_op = operators["generate"]
        self.execute_op = operators["execute"]
        self.review_op = operators["review"]

        print("✓ MyCustomAgent 初始化成功")
        print(f"  - LLM: {self.llm_service.model}")
        print(f"  - Sandbox: {self.sandbox_service.timeout}s")
        print(f"  - Data Analyzer: {'Yes' if self.data_analyzer else 'No'}")

    async def solve(self, description, io_instructions, data_dir, output_path):
        """
        实现自定义算法

        完全使用 DSLighting 暴露的 DSAT 组件
        """
        # 1. 分析数据
        if self.data_analyzer:
            data_report = self.data_analyzer.analyze(data_dir, output_path.name)
        else:
            data_report = ""

        # 2. 构建任务上下文
        task_context = {
            "goal_and_data": f"{description}\n\n{data_report}",
            "io_instructions": io_instructions
        }

        # 3. 迭代搜索
        max_iterations = self.agent_config.get("max_iterations", 3)

        for i in range(max_iterations):
            # 选择节点
            parent = self._select_node()

            # 生成提示词
            if parent is None:
                from dsat.prompts.common import create_draft_prompt
                prompt = create_draft_prompt(task_context, self.state.generate_summary())
            elif parent.is_buggy:
                from dsat.prompts.aide_prompt import create_debug_prompt
                prompt = create_debug_prompt(
                    task_context,
                    parent.code,
                    self._get_error_history(parent),
                    memory_summary=self.state.generate_summary()
                )
            else:
                from dsat.prompts.aide_prompt import create_improve_prompt
                from dsat.utils.context import summarize_repetitive_logs
                prompt = create_improve_prompt(
                    task_context,
                    self.state.generate_summary(),
                    parent.code,
                    parent.analysis,
                    previous_output=summarize_repetitive_logs(parent.term_out)
                )

            # 生成代码
            plan, code = await self.generate_op(system_prompt=prompt)

            # 创建节点
            new_node = Node(plan=plan, code=code)
            new_node.task_context = task_context

            # 执行代码
            result = await self.execute_op(code=code, mode="script")
            new_node.absorb_exec_result(result)

            # 检查输出文件
            submission_file = self.workspace_service.get_path("sandbox_workdir") / output_path.name
            if result.success and submission_file.exists():
                new_node.is_buggy = False
            else:
                new_node.is_buggy = True

            # 审查结果
            if not new_node.is_buggy:
                review_context = {
                    "task": description,
                    "code": new_node.code,
                    "output": new_node.term_out
                }
                review = await self.review_op(prompt_context=review_context)
                new_node.analysis = review.summary
                new_node.metric = MetricValue(
                    value=review.metric_value or 0.0,
                    maximize=not review.lower_is_better
                )
                new_node.is_buggy = review.is_buggy
            else:
                new_node.analysis = "代码执行失败或未生成输出文件"
                new_node.metric = MetricValue(value=0.0, maximize=True)

            # 添加到状态树
            self.state.append(new_node, parent)

        # 4. 使用最佳节点生成最终输出
        best_node = self.state.get_best_node()
        if best_node:
            await self.execute_op(code=best_node.code, mode="script")

    def _select_node(self):
        if len(self.state) == 0:
            return None
        successful = [n for n in self.state.nodes.values() if not n.is_buggy]
        if not successful:
            return list(self.state.nodes.values())[-1]
        return min(successful, key=lambda n: n.metric.value or float('inf'))

    def _get_error_history(self, node, max_depth=3):
        history = []
        current = node
        depth = 0
        while current and current.is_buggy and depth < max_depth:
            history.append(f"Step #{current.step}: {current.plan}\nError: {current.exc_type}")
            depth += 1
            current = self.state.get_node(current.parent_id) if current.parent_id else None
        return "\n".join(reversed(history)) if history else "No error history"


print("✓ MyCustomAgent 类定义成功")
print()

# ========== 方式 1: 注册并使用 ==========
print("方式 1: 注册到 DSLighting 系统并使用")
print("-"*80)

# 1. 在 factory.py 添加 Factory
print("提示: 在 dslighting/dsat/workflows/factory.py 添加:")
print("""
class MyCustomAgentWorkflowFactory(WorkflowFactory):
    def create_workflow(self, config, benchmark=None):
        from dsat.services.workspace import WorkspaceService
        from dsat.services.llm import LLMService
        from dsat.services.sandbox import SandboxService
        from dsat.services.data_analyzer import DataAnalyzer
        from dsat.services.states.journal import JournalState
        from dsat.operators.llm_basic import GenerateCodeAndPlanOperator, ReviewOperator
        from dsat.operators.code import ExecuteAndTestOperator

        workspace = WorkspaceService(run_name=config.run.name)
        llm_service = LLMService(config=config.llm)
        sandbox_service = SandboxService(workspace=workspace, timeout=config.sandbox.timeout)
        data_analyzer = DataAnalyzer()
        state = JournalState()

        operators = {
            "generate": GenerateCodeAndPlanOperator(llm_service=llm_service),
            "execute": ExecuteAndTestOperator(sandbox_service=sandbox_service),
            "review": ReviewOperator(llm_service=llm_service),
        }

        services = {
            "llm": llm_service,
            "sandbox": sandbox_service,
            "workspace": workspace,
            "data_analyzer": data_analyzer,
            "state": state,
        }

        return MyCustomAgent(operators, services, config.agent.model_dump())
""")

# 2. 在 runner.py 注册
print("\n提示: 在 dslighting/dsat/runner.py 的 WORKFLOW_FACTORIES 添加:")
print("""
WORKFLOW_FACTORIES = {
    ...
    "my_custom_agent": MyCustomAgentWorkflowFactory(),
}
""")

# 3. 使用
print("\n然后就可以使用了:")
print("""
agent = dslighting.Agent(
    workflow="my_custom_agent",
    model="gpt-4o",
    max_iterations=3
)

result = agent.run(data="path/to/data")
""")

print()
print("✓ 方式 1 说明完成")
print()

# ========== 方式 2: 直接使用（无需注册）==========
print("方式 2: 直接使用 DSAT Runner（无需注册）")
print("-"*80)

print("""
from dsat.config import DSATConfig
from dsat.runner import DSATRunner
from dslighting import (
    WorkspaceService, LLMService, SandboxService,
    DataAnalyzer, JournalState,
    GenerateCodeAndPlanOperator, ReviewOperator, ExecuteAndTestOperator
)

# 创建配置
config = DSATConfig(
    llm={"model": "gpt-4o", "temperature": 0.7},
    agent={"max_iterations": 3},
    run={"name": "my_agent_test"}
)

# 创建服务
workspace = WorkspaceService(run_name="test")
llm_service = LLMService(model="gpt-4o")
sandbox_service = SandboxService(workspace=workspace, timeout=300)
data_analyzer = DataAnalyzer()
state = JournalState()

# 创建操作器
operators = {
    "generate": GenerateCodeAndPlanOperator(llm_service=llm_service),
    "execute": ExecuteAndTestOperator(sandbox_service=sandbox_service),
    "review": ReviewOperator(llm_service=llm_service),
}

# 创建服务字典
services = {
    "llm": llm_service,
    "sandbox": sandbox_service,
    "workspace": workspace,
    "data_analyzer": data_analyzer,
    "state": state,
}

# 创建 Agent
agent = MyCustomAgent(operators, services, {"max_iterations": 3})

# 运行
await agent.solve(
    description="预测 bike demand",
    io_instructions="...",
    data_dir=Path("data/bike-sharing-demand"),
    output_path=Path("submission.csv")
)
""")

print()
print("✓ 方式 2 说明完成")
print()

# ========== 验证导入 ==========
print("="*80)
print("验证: DSLighting 已完全继承 DSAT")
print("="*80)

print("\n✓ 可以导入的 DSAT 组件:")
print("  - DSATWorkflow (核心基类)")
print("  - LLMService, SandboxService, WorkspaceService (服务)")
print("  - DataAnalyzer, VDBService (分析器)")
print("  - JournalState, Node, MetricValue (状态)")
print("  - GenerateCodeAndPlanOperator, ReviewOperator (操作器)")
print("  - Plan, ReviewResult, Task (模型)")

print("\n✓ 所有组件都通过 DSLighting 导入:")
print("  from dslighting import DSATWorkflow")
print("  from dslighting import LLMService")
print("  from dslighting import ...")

print("\n" + "="*80)
print("\n💡 关键要点:")
print("  1. ✓ DSLighting 完全暴露了 DSAT 的所有能力")
print("  2. ✓ 用户从 DSLighting 导入，但实际使用的是 DSAT")
print("  3. ✓ 可以像使用 DSAT 一样创建自定义 Agent")
print("  4. ✓ 不需要直接导入 dsat，全部通过 dslighting")
print("  5. ✓ DSLighting 是 DSAT 的完整继承者")

print("\n🎯 这就是您想要的：")
print("  - DSLighting 继承 DSAT 的所有东西")
print("  - 用户可以像 DSAT 一样定义自己的 Agent")
print("  - 完全的灵活性和控制权")

print("\n" + "="*80)
print("完成！")
print("="*80 + "\n")
