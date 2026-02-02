#!/usr/bin/env python3
"""
简化的单个 Workflow 测试脚本
使用 .env 文件配置 API key
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 加载环境变量（从 .env 文件）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有 dotenv，手动读取 .env 文件
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

import dslighting

# ============================================================================
# 配置
# ============================================================================
WORKFLOW_NAME = "aide"  # 可选: aide, autokaggle, data_interpreter, automind, dsagent, deepanalyze
MODEL = "openai/deepseek-ai/DeepSeek-V3.1-Terminus"
TEMPERATURE = 0.7
MAX_ITERATIONS = 1

# ============================================================================
# 主测试流程
# ============================================================================
def main():
    print("=" * 80)
    print(f"DSLighting 单 Workflow 测试")
    print("=" * 80)
    print(f"Workflow: {WORKFLOW_NAME}")
    print(f"Model: {MODEL}")
    print(f"Max Iterations: {MAX_ITERATIONS}")
    print(f"开始时间: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    # 检查 API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未检测到 OPENAI_API_KEY 环境变量")
        print("   请在 .env 文件中配置: OPENAI_API_KEY=your-key-here")
        print()
        response = input("是否继续测试？(y/N): ")
        if response.lower() != 'y':
            print("测试取消")
            sys.exit(1)
    print()

    # 1. 加载数据集信息
    print("步骤 1: 加载数据集信息...")
    print("-" * 80)
    try:
        info = dslighting.datasets.load_bike_sharing_demand()
        print(f"✓ 数据目录: {info['data_dir']}")
        print(f"✓ 任务 ID: {info['task_id']}")
        print()
    except Exception as e:
        print(f"✗ 加载数据集信息失败: {e}")
        sys.exit(1)

    # 2. 加载数据
    print("步骤 2: 加载数据...")
    print("-" * 80)
    try:
        data = dslighting.load_data(info['data_dir'])
        print(f"✓ 数据已加载")
        print(f"  - 任务类型: {data.task_type}")
        print(f"  - 任务 ID: {data.task_id}")
        print()
    except Exception as e:
        print(f"✗ 加载数据失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. 创建 Agent
    print(f"步骤 3: 创建 {WORKFLOW_NAME} Agent...")
    print("-" * 80)
    try:
        agent = dslighting.Agent(
            workflow=WORKFLOW_NAME,
            model=MODEL,
            temperature=TEMPERATURE,
            max_iterations=MAX_ITERATIONS,
            keep_workspace=True
        )
        print(f"✓ Agent 创建成功")
        print()
    except Exception as e:
        print(f"✗ 创建 Agent 失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 4. 运行 Agent
    print("步骤 4: 运行 Agent...")
    print("-" * 80)
    print("⏳ 开始执行任务（这可能需要几分钟）...")
    print()

    import time
    start_time = time.time()

    try:
        result = agent.run(data)

        duration = time.time() - start_time

        print()
        print("=" * 80)
        print("执行结果")
        print("=" * 80)
        print(f"✓ Success: {result.success}")
        print(f"✓ Score: {result.score}")
        print(f"✓ Cost: ${result.cost:.4f}")
        print(f"✓ Duration: {duration:.1f}s")
        print(f"✓ Workspace: {result.workspace_path}")

        if result.error:
            print(f"✗ Error: {result.error}")

        print()

        # 判断是否真正成功
        if result.score is not None:
            print("✅✅✅ 测试成功！✅✅✅")
            print(f"   Agent 成功完成任务并获得分数: {result.score}")
            success_status = "SUCCESS"
        elif result.success:
            print("⚠️  部分成功")
            print("   Agent 运行完成但没有获得分数")
            print("   可能原因: API key 未配置或 LLM 调用失败")
            success_status = "PARTIAL"
        else:
            print("❌ 测试失败")
            print(f"   Agent 执行失败: {result.error}")
            success_status = "FAILED"

        print()
        print("=" * 80)

        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = Path(f"test_result_{WORKFLOW_NAME}_{timestamp}.txt")

        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"DSLighting Workflow 测试结果\n")
            f.write(f"=" * 80 + "\n\n")
            f.write(f"测试时间: {datetime.now().isoformat()}\n")
            f.write(f"Workflow: {WORKFLOW_NAME}\n")
            f.write(f"Model: {MODEL}\n")
            f.write(f"Task: {data.task_id}\n")
            f.write(f"Max Iterations: {MAX_ITERATIONS}\n\n")
            f.write(f"执行结果:\n")
            f.write(f"  Success: {result.success}\n")
            f.write(f"  Score: {result.score}\n")
            f.write(f"  Cost: ${result.cost:.4f}\n")
            f.write(f"  Duration: {duration:.1f}s\n")
            f.write(f"  Workspace: {result.workspace_path}\n")
            if result.error:
                f.write(f"  Error: {result.error}\n")
            f.write(f"\n状态: {success_status}\n")
            f.write(f"\nOutput:\n{result.output}\n")

        print(f"✓ 结果已保存: {result_file}")
        print()

        # 返回退出码
        if result.score is not None:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        duration = time.time() - start_time
        print()
        print("=" * 80)
        print("执行错误")
        print("=" * 80)
        print(f"✗ Error Type: {type(e).__name__}")
        print(f"✗ Error Message: {str(e)}")
        print(f"✗ Duration: {duration:.1f}s")
        print()

        import traceback
        traceback.print_exc()

        # 保存错误报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_file = Path(f"test_error_{WORKFLOW_NAME}_{timestamp}.md")

        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"# 错误报告: {WORKFLOW_NAME}\n\n")
            f.write(f"**测试时间**: {datetime.now().isoformat()}\n")
            f.write(f"**Workflow**: {WORKFLOW_NAME}\n")
            f.write(f"**Model**: {MODEL}\n\n")
            f.write(f"## 错误信息\n\n")
            f.write(f"**类型**: `{type(e).__name__}`\n\n")
            f.write(f"**消息**: {str(e)}\n\n")
            f.write(f"## 完整堆栈\n\n")
            f.write(f"```\n")
            f.write(traceback.format_exc())
            f.write(f"\n```\n")

        print(f"✓ 错误报告已保存: {error_file}")
        print()
        sys.exit(2)


if __name__ == "__main__":
    main()
