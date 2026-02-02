"""
测试 DataInsightsAIDE Workflow

在 bike-sharing-demand 数据集上使用 deepseek-ai/DeepSeek-V3-Terminus 模型
"""

import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/test_pip_dslighting/AdvancedDSAgent/src')

from dotenv import load_dotenv
load_dotenv()

import dslighting
from advanced_ds_agent import DataInsightsAIDEWorkflowFactory

import asyncio
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """主测试函数"""

    print("\n" + "="*80)
    print("DataInsightsAIDE Workflow 测试")
    print("="*80)
    print("\n配置:")
    print("  - 数据集: bike-sharing-demand")
    print("  - 模型: openai/deepseek-ai/DeepSeek-V3.1-Terminus")
    print("  - 最大迭代: 1 (快速测试)")
    print("  - 数据洞察: 启用")
    print("\n" + "="*80 + "\n")

    # 1. 创建工厂
    print("📦 创建 Workflow Factory...")
    factory = DataInsightsAIDEWorkflowFactory(
        model="openai/deepseek-ai/DeepSeek-V3.1-Terminus",
        # api_key, api_base, temperature 会自动从 .env 的 LLM_MODEL_CONFIGS 中读取
        timeout=300,
        keep_workspace=True  # 保留工作空间便于调试
    )
    print("✓ Factory 创建完成\n")

    # 2. 创建 Agent
    print("🤖 创建 Agent...")
    agent = factory.create_agent(
        max_iterations=1,  # 快速测试，只迭代1次
        use_data_insights=True
    )
    print("✓ Agent 创建完成\n")

    # 3. 加载数据
    print("📊 加载数据...")
    data = dslighting.load_data("bike-sharing-demand")
    print("✓ 数据加载完成\n")

    # 4. 运行 Agent
    print("🚀 运行 DataInsightsAIDE Workflow...")
    print("="*80 + "\n")

    try:
        # ✅ 在 async context 中使用 await agent.solve()
        await agent.solve(
            description=data.description,
            io_instructions=data.io_instructions,
            data_dir=data.data_dir,
            output_path=data.output_path
        )

        print("\n" + "="*80)
        print("执行结果")
        print("="*80)
        print(f"✓ 任务完成")

        # TODO: 获取实际的结果指标（score, cost, duration 等）

    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        print(f"\n❌ 执行异常: {e}")

    finally:
        # 清理
        print("\n🧹 清理资源...")
        factory.cleanup()
        print("✓ 清理完成")

    print("\n" + "="*80)
    print("测试完成")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           DataInsightsAIDE Workflow - 测试脚本                      ║
║                                                                    ║
║  特点:                                                             ║
║  1. 数据洞察阶段 - 深入探索数据                                    ║
║  2. 迭代改进阶段 - 基于洞察生成和改进代码                          ║
║  3. 最终输出 - 生成 main.py                                        ║
║                                                                    ║
║  配置:                                                             ║
║  - 数据集: bike-sharing-demand                                    ║
║  - 模型: DeepSeek-V3.1-Terminus                                   ║
║  - 最大迭代: 1                                                    ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(main())
