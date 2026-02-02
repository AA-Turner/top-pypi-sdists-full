"""
展示 DSLighting Task Loader 架构

演示 Task Layer, Workflow Layer, Registry Layer 的职责分离
"""

import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           DSLighting Task Loader - 架构演示                         ║
║                                                                    ║
║  架构分层:                                                         ║
║  ┌──────────────────────────────────────────────────────────┐     ║
║  │ Task Layer (tasks/)        - 任务加载                     │     ║
║  │   ├── MLETaskLoader.load_task()                          │     ║
║  │   └── 未来: KaggleTaskLoader, QATaskLoader...             │     ║
║  └──────────────────────────────────────────────────────────┘     ║
║                          ↓                                       ║
║  ┌──────────────────────────────────────────────────────────┐     ║
║  │ Workflow Layer (workflows/) - 工作流管理                │     ║
║  │   └── BaseWorkflowFactory.run_with_task_id()            │     ║
║  └──────────────────────────────────────────────────────────┘     ║
║                          ↓                                       ║
║  ┌──────────────────────────────────────────────────────────┐     ║
║  │ Registry Layer (registry/)  - 任务配置                   │     ║
║  │   └── load_task_config(task_id)                          │     ║
║  └──────────────────────────────────────────────────────────┘     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")

async def demo_task_loader():
    """演示 Task Layer - 直接使用 TaskLoader"""
    print("\n" + "="*80)
    print("演示 1: Task Layer - 直接使用 MLETaskLoader")
    print("="*80)

    from dslighting.tasks import MLETaskLoader

    # ✅ 创建 TaskLoader
    loader = MLETaskLoader()

    print("\n✓ 创建 MLETaskLoader")

    # ✅ 加载任务
    description, io_instructions, data_dir, output_path = loader.load_task(
        task_id="bike-sharing-demand"
    )

    print(f"\n✓ 任务加载完成:")
    print(f"  - Description: {len(description)} 字符")
    print(f"  - I/O Instructions: {len(io_instructions)} 字符")
    print(f"  - Data Directory: {data_dir}")
    print(f"  - Output Path: {output_path}")

    print("\n📝 Description 预览 (前 200 字符):")
    print(description[:200] + "...")

    print("\n📝 I/O Instructions 预览 (前 200 字符):")
    print(io_instructions[:200] + "...")


async def demo_workflow_factory():
    """演示 Workflow Layer - 使用 BaseWorkflowFactory"""
    print("\n" + "="*80)
    print("演示 2: Workflow Layer - BaseWorkflowFactory 使用 TaskLoader")
    print("="*80)

    from dslighting import BaseWorkflowFactory
    from dslighting.operators import GenerateCodeAndPlanOperator
    from dslighting.state import JournalState

    # ✅ 定义一个简单的 Workflow Factory
    class SimpleFactory(BaseWorkflowFactory):
        """简单的工厂，只是为了演示"""

        def create_agent(self, **kwargs):
            print("\n  ✓ create_agent() 被调用")
            print(f"    - kwargs: {kwargs}")
            # 实际使用中会创建真实的 workflow
            return None

    print("\n✓ 创建 SimpleFactory（继承 BaseWorkflowFactory）")
    factory = SimpleFactory(model="gpt-4o")

    print("\n✓ BaseWorkflowFactory 提供的服务:")
    print(f"  - llm_service: {type(factory.llm_service).__name__}")
    print(f"  - sandbox_service: {type(factory.sandbox_service).__name__}")
    print(f"  - workspace_service: {type(factory.workspace_service).__name__}")

    print("\n✓ 现在可以使用 run_with_task_id()，它会自动:")
    print("  1. 使用 MLETaskLoader 加载任务配置")
    print("  2. 调用 create_agent() 创建 agent")
    print("  3. 运行 workflow")

    print("\n💡 完整使用示例:")
    print("""
    # 创建工厂
    factory = MyFactory(model="gpt-4o")

    # ✨ 一行代码运行！
    await factory.run_with_task_id("bike-sharing-demand")

    # 内部流程:
    # 1. BaseWorkflowFactory 使用 MLETaskLoader 加载任务
    # 2. 调用用户的 create_agent() 创建 workflow
    # 3. 运行 workflow.solve()
    """)


async def demo_custom_task_loader():
    """演示如何使用自定义 TaskLoader"""
    print("\n" + "="*80)
    print("演示 3: 插件化 - 使用自定义 TaskLoader")
    print("="*80)

    from dslighting import BaseWorkflowFactory

    # ✅ 定义自定义 TaskLoader
    class CustomTaskLoader:
        """自定义任务加载器（示例）"""
        def load_task(self, task_id, data_dir=None):
            print(f"\n  ✓ CustomTaskLoader.load_task('{task_id}')")
            return "custom description", "custom io", data_dir or Path("."), Path("output.csv")

    print("\n✅ 可以创建不同类型的 TaskLoader:")
    print("  - MLETaskLoader (MLE 标准格式)")
    print("  - KaggleTaskLoader (Kaggle 格式，未来)")
    print("  - QATaskLoader (QA 格式，未来)")
    print("  - CustomTaskLoader (自定义)")

    print("\n✅ 使用方式:")
    print("""
    # 使用默认的 MLETaskLoader
    await factory.run_with_task_id("bike-sharing-demand")

    # 使用自定义 TaskLoader
    await factory.run_with_task_id(
        "custom-task",
        task_loader=CustomTaskLoader()  # ✅ 插件化
    )
    """)

    print("\n🎯 优势:")
    print("  - 职责分离: Task Layer 专门处理任务加载")
    print("  - 可扩展: 轻松添加新的任务类型")
    print("  - 可复用: TaskLoader 可以在多处使用")
    print("  - 可测试: 独立的 TaskLoader 易于单元测试")


async def main():
    """主函数"""
    print("\n🚀 DSLighting Task Loader - 架构演示\n")

    # 演示 1: Task Layer
    await demo_task_loader()

    # 演示 2: Workflow Layer
    await demo_workflow_factory()

    # 演示 3: 插件化
    await demo_custom_task_loader()

    print("\n" + "="*80)
    print("演示完成")
    print("="*80)

    print("\n📚 相关文档:")
    print("  - 架构设计: PIP_DOC/TASK_LOADER_ARCHITECTURE.md")
    print("  - BaseWorkflowFactory: PIP_DOC/BASE_WORKFLOW_FACTORY_GUIDE.md")
    print("  - MLE 标准格式: PIP_DOC/BEST_PRACTICES_EXTRA_CONTEXT.md")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
