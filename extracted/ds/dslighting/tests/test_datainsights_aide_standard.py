"""
测试 DataInsightsAIDE Workflow - 使用标准 MLE 格式

使用 run_with_task_id() 方法，自动从 registry 加载标准配置
"""

import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/test_pip_dslighting/AdvancedDSAgent/src')

from dotenv import load_dotenv
load_dotenv()

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
    print("DataInsightsAIDE Workflow 测试 - 标准 MLE 格式")
    print("="*80)
    print("\n配置:")
    print("  - 数据集: bike-sharing-demand")
    print("  - 模型: openai/deepseek-ai/DeepSeek-V3.1-Terminus")
    print("  - 最大迭代: 1 (快速测试)")
    print("  - 数据洞察: 启用")
    print("  - 格式: 标准 MLE 格式（从 registry 自动加载）")
    print("\n" + "="*80 + "\n")

    # 1. 创建工厂
    print("📦 创建 Workflow Factory...")
    factory = DataInsightsAIDEWorkflowFactory(
        model="openai/deepseek-ai/DeepSeek-V3.1-Terminus",
        timeout=300,
        keep_workspace=True  # 保留工作空间便于调试
    )
    print("✓ Factory 创建完成\n")

    # 2. ✨ 使用新的 run_with_task_id() 方法（推荐）
    print("🚀 运行 DataInsightsAIDE Workflow...")
    print("="*80 + "\n")

    try:
        # ✅ 自动从 registry 加载标准 MLE 格式配置
        await factory.run_with_task_id(
            task_id="bike-sharing-demand",  # 只需提供 task_id！
            max_iterations=1,  # 快速测试
            use_data_insights=True
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
║           DataInsightsAIDE Workflow - 测试脚本（标准格式）          ║
║                                                                    ║
║  特点:                                                             ║
║  1. ✅ 自动从 registry 加载标准 MLE 格式配置                       ║
║  2. ✅ 使用 analyzer 生成完整的数据报告和 I/O 指令                  ║
║  3. ✅ 数据洞察阶段 - 深入探索数据                                 ║
║  4. ✅ 迭代改进阶段 - 基于洞察生成和改进代码                       ║
║  5. ✅ 最终输出 - 生成 main.py                                     ║
║                                                                    ║
║  配置:                                                             ║
║  - 数据集: bike-sharing-demand                                    ║
║  - 模型: DeepSeek-V3.1-Terminus                                   ║
║  - 最大迭代: 1                                                    ║
║                                                                    ║
║  用法:                                                             ║
║  factory = DataInsightsAIDEWorkflowFactory(model="...")            ║
║  await factory.run_with_task_id("bike-sharing-demand")            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(main())
