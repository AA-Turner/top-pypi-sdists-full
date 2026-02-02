"""
追踪数据流，找到 data_report 丢失的地方
"""
import sys
import logging
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "AdvancedDSAgent" / "src"))

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s:%(lineno)d - %(message)s'
)

async def test_data_flow():
    """追踪数据从 MLETaskLoader 到 create_draft_prompt 的完整流程"""

    print("=" * 80)
    print("追踪数据流")
    print("=" * 80)

    # 1. MLETaskLoader 输出
    from dslighting.tasks import MLETaskLoader
    loader = MLETaskLoader()
    description, io_instructions, data_dir, output_path = loader.load_task("bike-sharing-demand")

    print(f"\n1. MLETaskLoader.load_task() 输出:")
    print(f"   description 长度: {len(description)}")
    print(f"   description 是否包含 'Directory Structure': {'Directory Structure' in description}")
    print(f"   description 是否包含 'Data Schema': {'Data Schema' in description}")
    print(f"   io_instructions 长度: {len(io_instructions)}")

    # 检查 description 的组成部分
    if "Directory Structure" in description:
        idx = description.index("Directory Structure")
        print(f"\n   ✓ description 包含 data_report (从位置 {idx} 开始)")
        print(f"   前 {idx} 字符是原始 description.md")
    else:
        print(f"\n   ❌ description 不包含 data_report!")
        print(f"   只有原始的 description.md 内容")

    # 2. 模拟 workflow 构建 task_context
    task_context = {
        "goal_and_data": description,
        "io_instructions": io_instructions
    }

    print(f"\n2. workflow 构建 task_context:")
    print(f"   goal_and_data 长度: {len(task_context['goal_and_data'])}")
    print(f"   goal_and_data 是否包含 'Directory Structure': {'Directory Structure' in task_context['goal_and_data']}")

    # 3. 调用 create_draft_prompt
    from dsat.prompts.common import create_draft_prompt
    memory_summary = "No successful solutions have been found yet."

    print(f"\n3. 调用 create_draft_prompt()...")
    prompt = create_draft_prompt(
        task_context,
        memory_summary,
        extra_context=None
    )

    # 4. 分析生成的 prompt
    print(f"\n4. 分析生成的 prompt:")
    print(f"   prompt 总长度: {len(prompt)}")

    # 提取 "Task Goal and Data Overview" 部分
    import re
    match = re.search(
        r'Task Goal and Data Overview: (.+?)(?=\n\n(?:CRITICAL I/O|Memory of Past|Retrieved Knowledge|Additional Context|Instructions:|\Z))',
        prompt,
        re.DOTALL
    )

    if match:
        task_goal_section = match.group(1).strip()
        print(f"\n   ✓ 找到 'Task Goal and Data Overview' 部分:")
        print(f"      长度: {len(task_goal_section)}")
        print(f"      是否包含 'Directory Structure': {'Directory Structure' in task_goal_section}")
        print(f"      是否包含 'Data Schema': {'Data Schema' in task_goal_section}")

        # 显示前 500 字符
        print(f"\n      前 500 字符:")
        print("-" * 80)
        print(task_goal_section[:500])
        print("-" * 80)

        if len(task_goal_section) < 3000:
            print(f"\n   ❌ 问题确认: 'Task Goal and Data Overview' 只有 {len(task_goal_section)} 字符")
            print(f"      应该有 {len(description)} 字符")
            print(f"      丢失了 {len(description) - len(task_goal_section)} 字符 (data_report)")
            return False
    else:
        print(f"\n   ❌ 未找到 'Task Goal and Data Overview' 部分!")
        return False

    # 检查 CRITICAL I/O REQUIREMENTS 部分
    match2 = re.search(
        r'CRITICAL I/O REQUIREMENTS \(MUST BE FOLLOWED\): (.+?)(?=\n\n(?:Memory of Past|Retrieved Knowledge|Additional Context|Instructions:|\Z))',
        prompt,
        re.DOTALL
    )

    if match2:
        io_section = match2.group(1).strip()
        print(f"\n   ✓ 找到 'CRITICAL I/O REQUIREMENTS' 部分:")
        print(f"      长度: {len(io_section)}")
        print(f"      前 200 字符:")
        print("-" * 80)
        print(io_section[:200])
        print("-" * 80)

        if len(io_section) < 100:
            print(f"\n   ❌ 问题确认: 'CRITICAL I/O REQUIREMENTS' 太短！")
            return False

    return True

if __name__ == "__main__":
    success = asyncio.run(test_data_flow())
    sys.exit(0 if success else 1)
