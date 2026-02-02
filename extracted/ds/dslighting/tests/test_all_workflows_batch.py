#!/usr/bin/env python3
"""
批量测试所有 DSLighting Workflows
使用 .env 文件配置 API key
"""

import os
import sys
import time
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
MODEL = "openai/deepseek-ai/DeepSeek-V3.1-Terminus"
TEMPERATURE = 0.7
MAX_ITERATIONS = 1

# 所有 workflow 列表
WORKFLOWS = [
    "aide",
    "autokaggle",
    "data_interpreter",
    "automind",
    "dsagent",
    "deepanalyze"
]

# ============================================================================
# 测试函数
# ============================================================================
def test_workflow(workflow_name, data):
    """测试单个 workflow"""
    print(f"\n{'='*80}")
    print(f"测试: {workflow_name}")
    print(f"{'='*80}\n")

    result = {
        "workflow": workflow_name,
        "success": False,
        "score": None,
        "cost": 0.0,
        "duration": 0.0,
        "error": None
    }

    try:
        # 创建 agent
        print(f"创建 {workflow_name} Agent...")
        agent = dslighting.Agent(
            workflow=workflow_name,
            model=MODEL,
            temperature=TEMPERATURE,
            max_iterations=MAX_ITERATIONS,
            keep_workspace=True
        )
        print("✓ Agent 创建成功\n")

        # 运行
        print(f"运行 {workflow_name}...")
        start_time = time.time()

        agent_result = agent.run(data)

        duration = time.time() - start_time

        # 记录结果
        result["success"] = agent_result.success
        result["score"] = agent_result.score
        result["cost"] = agent_result.cost
        result["duration"] = duration
        result["error"] = agent_result.error

        # 打印结果
        print(f"\n{'='*80}")
        print(f"结果:")
        print(f"{'='*80}")
        print(f"✓ Success: {agent_result.success}")
        print(f"✓ Score: {agent_result.score}")
        print(f"✓ Cost: ${agent_result.cost:.4f}")
        print(f"✓ Duration: {duration:.1f}s")

        if agent_result.error:
            print(f"✗ Error: {agent_result.error}")

        if agent_result.score is not None:
            print(f"\n✅ 成功！获得分数: {agent_result.score}")
        else:
            print(f"\n⚠️  警告: 未获得分数")

    except Exception as e:
        result["error"] = str(e)
        print(f"\n✗ 测试失败: {e}")

    return result


# ============================================================================
# 主函数
# ============================================================================
def main():
    print("=" * 80)
    print("DSLighting 批量 Workflow 测试")
    print("=" * 80)
    print(f"Model: {MODEL}")
    print(f"Max Iterations: {MAX_ITERATIONS}")
    print(f"开始时间: {datetime.now().isoformat()}")
    print("=" * 80)

    # 检查 API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  警告: 未检测到 OPENAI_API_KEY 环境变量")
        print("   请在 .env 文件中配置: OPENAI_API_KEY=your-key-here")
        print()
        response = input("是否继续测试？(y/N): ")
        if response.lower() != 'y':
            print("测试取消")
            sys.exit(1)

    print()

    # 1. 加载数据
    print("步骤 1: 加载数据...")
    print("-" * 80)
    try:
        info = dslighting.datasets.load_bike_sharing_demand()
        print(f"✓ 任务 ID: {info['task_id']}")
        print(f"✓ 数据目录: {info['data_dir']}")

        data = dslighting.load_data(info['data_dir'])
        print(f"✓ 数据已加载: {data.task_id}")
        print()
    except Exception as e:
        print(f"✗ 加载数据失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 2. 测试所有 workflows
    print("步骤 2: 批量测试所有 Workflows...")
    print("-" * 80)
    print(f"共 {len(WORKFLOWS)} 个 workflow 待测试\n")

    results = {}
    for i, workflow in enumerate(WORKFLOWS, 1):
        print(f"\n进度: [{i}/{len(WORKFLOWS)}]")
        result = test_workflow(workflow, data)
        results[workflow] = result

    # 3. 生成报告
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)

    # 统计
    total = len(results)
    success_with_score = sum(1 for r in results.values() if r['score'] is not None)
    success_no_score = sum(1 for r in results.values() if r['success'] and r['score'] is None)
    failed = sum(1 for r in results.values() if not r['success'])

    print(f"\n总测试数: {total}")
    print(f"✅ 成功 (有分数): {success_with_score}")
    print(f"⚠️  部分成功 (无分数): {success_no_score}")
    print(f"❌ 失败: {failed}")

    # 详细结果
    print(f"\n{'='*80}")
    print("详细结果")
    print(f"{'='*80}\n")

    for workflow, result in results.items():
        status = "✅" if result['score'] is not None else ("⚠️ " if result['success'] else "❌")
        score_str = f"{result['score']:.4f}" if result['score'] is not None else "N/A"
        print(f"{status} {workflow:20} Score: {score_str:10} Cost: ${result['cost']:.4f}  Time: {result['duration']:.1f}s")

    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Path(f"test_report_batch_{timestamp}.md")

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# DSLighting 批量测试报告\n\n")
        f.write(f"**测试时间**: {datetime.now().isoformat()}\n")
        f.write(f"**Model**: {MODEL}\n")
        f.write(f"**Max Iterations**: {MAX_ITERATIONS}\n\n")

        f.write("## 测试总结\n\n")
        f.write(f"- **总测试数**: {total}\n")
        f.write(f"- **成功 (有分数)**: {success_with_score}\n")
        f.write(f"- **部分成功 (无分数)**: {success_no_score}\n")
        f.write(f"- **失败**: {failed}\n\n")

        f.write("## 详细结果\n\n")
        f.write("| Workflow | Status | Score | Cost ($) | Time (s) | Error |\n")
        f.write("|----------|--------|-------|----------|----------|-------|\n")

        for workflow, result in results.items():
            status = "✅" if result['score'] is not None else ("⚠️" if result['success'] else "❌")
            score_str = f"{result['score']:.4f}" if result['score'] is not None else "N/A"
            error_str = result['error'][:50] if result['error'] else "-"
            f.write(f"| {workflow} | {status} | {score_str} | ${result['cost']:.4f} | {result['duration']:.1f} | {error_str} |\n")

    print(f"\n✓ 报告已保存: {report_file}")
    print()

    # 返回退出码
    if success_with_score == total:
        print("🎉 所有测试成功！")
        sys.exit(0)
    elif success_with_score > 0:
        print(f"⚠️  部分测试成功 ({success_with_score}/{total})")
        sys.exit(1)
    else:
        print("❌ 所有测试失败")
        sys.exit(2)


if __name__ == "__main__":
    main()
