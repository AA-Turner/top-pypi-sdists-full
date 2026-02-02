"""
模拟用户的 workflow 完整调用链，找到问题所在
"""
import sys
import logging
import asyncio
from pathlib import Path

# 添加 AdvancedDSAgent 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "AdvancedDSAgent" / "src"))

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s - %(message)s'
)

async def test_user_workflow():
    """测试用户的完整 workflow 调用"""

    print("=" * 80)
    print("测试用户的 Workflow 调用链")
    print("=" * 80)

    try:
        # 1. 导入 Factory
        from advanced_ds_agent.factory import DataInsightsAIDEWorkflowFactory

        print("\n1. 创建 Factory...")
        factory = DataInsightsAIDEWorkflowFactory(
            model="gpt-4o",
            api_key="test",
            api_base="https://api.test.com",
            temperature=0.7
        )

        # 2. 模拟 MLETaskLoader 的输出
        print("\n2. 模拟 MLETaskLoader.load_task()...")
        from dslighting.tasks import MLETaskLoader

        loader = MLETaskLoader()
        description, io_instructions, data_dir, output_path = loader.load_task("bike-sharing-demand")

        print(f"\n✓ MLETaskLoader 输出:")
        print(f"  - description 长度: {len(description)}")
        print(f"  - io_instructions 长度: {len(io_instructions)}")
        print(f"  - io_instructions 前200字符: {io_instructions[:200]}")
        print(f"  - 包含 'CRITICAL I/O': {'CRITICAL I/O' in io_instructions}")

        # 3. 创建 Agent
        print("\n3. 创建 Agent...")
        agent = factory.create_agent(max_iterations=1)

        # 4. 构建 task_context（模拟 workflow 的操作）
        print("\n4. 构建 task_context...")
        task_context = {
            "goal_and_data": description,
            "io_instructions": io_instructions
        }

        print(f"\n✓ task_context:")
        print(f"  - goal_and_data 长度: {len(task_context['goal_and_data'])}")
        print(f"  - io_instructions 长度: {len(task_context['io_instructions'])}")
        print(f"  - io_instructions 前200字符: {task_context['io_instructions'][:200]}")

        # 5. 测试 create_draft_prompt
        print("\n5. 测试 create_draft_prompt()...")
        from dsat.prompts.common import create_draft_prompt

        memory_summary = "No successful solutions have been found yet."
        insights_context = None

        prompt = create_draft_prompt(
            task_context,
            memory_summary,
            extra_context=insights_context
        )

        print(f"\n✓ 生成的 prompt 长度: {len(prompt)}")

        # 检查 prompt 中的关键部分
        print("\n6. 检查 prompt 内容...")

        # 提取 "CRITICAL I/O REQUIREMENTS" 部分
        import re
        match = re.search(
            r'CRITICAL I/O REQUIREMENTS.*?(?=\n\n[A-Z]|\nInstructions:|\Z)',
            prompt,
            re.DOTALL
        )

        if match:
            critical_io_section = match.group(0)
            print(f"\n✓ 找到 CRITICAL I/O REQUIREMENTS 部分:")
            print(f"  长度: {len(critical_io_section)}")
            print(f"  内容前300字符:")
            print("-" * 80)
            print(critical_io_section[:300])
            print("-" * 80)

            # 检查是否只有 "target"
            if critical_io_section.strip() == "target":
                print("\n❌ 问题确认: CRITICAL I/O REQUIREMENTS 只包含 'target'!")
            else:
                print("\n✓ CRITICAL I/O REQUIREMENTS 内容正常")
        else:
            print("\n❌ 未找到 CRITICAL I/O REQUIREMENTS 部分!")

        # 保存 prompt 到文件供检查
        output_file = Path("/tmp/test_workflow_prompt.txt")
        output_file.write_text(prompt, encoding='utf-8')
        print(f"\n✓ 完整 prompt 已保存到: {output_file}")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_user_workflow())
    sys.exit(0 if success else 1)
