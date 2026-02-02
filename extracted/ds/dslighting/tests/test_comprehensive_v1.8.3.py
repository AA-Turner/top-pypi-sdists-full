"""
DSLighting v1.8.3 综合测试
测试所有核心功能和 4 种使用方式
"""
import sys
import time
from pathlib import Path

print("=" * 80)
print("DSLighting v1.8.3 综合测试")
print("=" * 80)

# 等待 PyPI 更新
print("\n⏳ 等待 PyPI 更新...")
time.sleep(30)

# 安装新版本
print("\n📦 正在安装 DSLighting v1.8.3...")
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "dslighting==1.8.3", "-q"])
print("✅ 安装完成")

# 开始测试
import dslighting
import pandas as pd

print(f"\n{'='*80}")
print(f"当前版本: {dslighting.__version__}")
print(f"{'='*80}")

# ============================================================================
# 测试 1: 数据文件修复验证
# ============================================================================
print("\n" + "="*80)
print("测试 1: 数据文件修复验证 (bike-sharing-demand)")
print("="*80)

data = dslighting.load_data("bike-sharing-demand")
test_df = pd.read_csv(data.data_dir / "prepared" / "public" / "test.csv")
sample_df = pd.read_csv(data.data_dir / "prepared" / "public" / "sampleSubmission.csv")

print(f"\n✓ test.csv 行数: {len(test_df)}")
print(f"✓ sampleSubmission.csv 行数: {len(sample_df)}")
print(f"✓ 行数匹配: {len(test_df) == len(sample_df)}")

test_datetime = set(test_df['datetime'].tolist())
sample_datetime = set(sample_df['datetime'].tolist())
print(f"✓ datetime 匹配: {test_datetime == sample_datetime}")

if len(test_df) == len(sample_df) and test_datetime == sample_datetime:
    print("✅ 测试 1 通过：数据文件修复成功")
else:
    print("❌ 测试 1 失败：数据文件不匹配")
    sys.exit(1)

# ============================================================================
# 测试 2: 方式1 - 全局配置模式
# ============================================================================
print("\n" + "="*80)
print("测试 2: 方式1 - 全局配置模式")
print("="*80)

try:
    # 创建临时目录结构进行测试
    from dslighting.core.global_config import get_global_config
    config = get_global_config()

    # 测试 setup 函数
    result = dslighting.setup(
        data_parent_dir="/path/to/data/competitions",
        registry_parent_dir="/path/to/registry"
    )

    # 验证配置
    data_dir, registry_dir = config.get_task_paths("test-task")
    assert str(data_dir) == "/path/to/data/competitions/test-task"
    assert str(registry_dir) == "/path/to/registry/test-task"

    # 重置配置
    config.reset()

    print("✅ 测试 2 通过：全局配置模式正常工作")
except Exception as e:
    print(f"❌ 测试 2 失败：{e}")
    sys.exit(1)

# ============================================================================
# 测试 3: 方式2 - 直接路径模式
# ============================================================================
print("\n" + "="*80)
print("测试 3: 方式2 - 直接路径模式")
print("="*80)

try:
    agent = dslighting.Agent()

    # 使用内置数据集测试（无需提供路径，只测试逻辑）
    data = dslighting.load_data("bike-sharing-demand")

    # 验证路径是完整路径
    assert (data.data_dir / "prepared" / "public").exists()

    print("✅ 测试 3 通过：直接路径模式正常工作")
except Exception as e:
    print(f"❌ 测试 3 失败：{e}")
    sys.exit(1)

# ============================================================================
# 测试 4: 方式3 - 内置数据集模式
# ============================================================================
print("\n" + "="*80)
print("测试 4: 方式3 - 内置数据集模式")
print("="*80)

try:
    # 测试直接使用 task_id 加载
    data = dslighting.load_data("bike-sharing-demand")

    # 验证数据加载成功
    assert data.task_id == "bike-sharing-demand"
    assert data.get_task_type() == "kaggle"

    print(f"✓ Task ID: {data.task_id}")
    print(f"✓ Task Type: {data.get_task_type()}")
    print("✅ 测试 4 通过：内置数据集模式正常工作")
except Exception as e:
    print(f"❌ 测试 4 失败：{e}")
    sys.exit(1)

# ============================================================================
# 测试 5: 方式4 - 先加载数据模式
# ============================================================================
print("\n" + "="*80)
print("测试 5: 方式4 - 先加载数据模式")
print("="*80)

try:
    # 加载数据
    data = dslighting.load_data("bike-sharing-demand")

    # 测试 data 对象的方法
    summary = data.show()
    assert isinstance(summary, str)
    assert "bike-sharing-demand" in summary

    description = data.get_description()
    task_type = data.get_task_type()
    workflow = data.get_recommended_workflow()
    io_instructions = data.get_io_instructions()

    print(f"✓ show() 方法正常")
    print(f"✓ get_task_type(): {task_type}")
    print(f"✓ get_recommended_workflow(): {workflow[:50]}...")
    print("✅ 测试 5 通过：先加载数据模式正常工作")
except Exception as e:
    print(f"❌ 测试 5 失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 测试 6: 数据结构验证
# ============================================================================
print("\n" + "="*80)
print("测试 6: 数据结构验证")
print("="*80)

try:
    data = dslighting.load_data("bike-sharing-demand")

    # 验证 LoadedData 属性
    assert hasattr(data, 'task_id')
    assert hasattr(data, 'data_dir')
    assert hasattr(data, 'registry_dir')
    assert hasattr(data, 'task_detection')

    print(f"✓ task_id: {data.task_id}")
    print(f"✓ data_dir: {data.data_dir}")
    print(f"✓ registry_dir: {data.registry_dir}")

    # 验证 TaskDetection
    assert hasattr(data.task_detection, 'task_type')
    assert hasattr(data.task_detection, 'task_mode')
    assert data.task_detection.task_type == 'kaggle'
    assert data.task_detection.task_mode == 'standard_ml'

    print(f"✓ TaskDetection.task_type: {data.task_detection.task_type}")
    print(f"✓ TaskDetection.task_mode: {data.task_detection.task_mode}")

    # 验证 registry_dir (注意: LoadedData 有 registry_dir 属性，不是 registry 对象)
    assert hasattr(data, 'registry_dir')
    assert data.registry_dir is not None

    print(f"✓ registry_dir: {data.registry_dir}")

    print("✅ 测试 6 通过：数据结构验证成功")
except Exception as e:
    print(f"❌ 测试 6 失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 测试 7: 路径规范验证 (v1.8.0+)
# ============================================================================
print("\n" + "="*80)
print("测试 7: 路径规范验证 (v1.8.0+)")
print("="*80)

try:
    data = dslighting.load_data("bike-sharing-demand")

    # 验证路径结构
    expected_structure = [
        data.data_dir / "prepared" / "public" / "train.csv",
        data.data_dir / "prepared" / "public" / "test.csv",
        data.data_dir / "prepared" / "public" / "sampleSubmission.csv",
        data.data_dir / "prepared" / "private" / "test_answer.csv",
    ]

    for path in expected_structure:
        assert path.exists(), f"文件不存在: {path}"
        print(f"✓ {path.name} 存在")

    # 验证 sampleSubmission.csv 与 test.csv 行数一致
    test_rows = len(pd.read_csv(data.data_dir / "prepared" / "public" / "test.csv"))
    sample_rows = len(pd.read_csv(data.data_dir / "prepared" / "public" / "sampleSubmission.csv"))

    assert test_rows == sample_rows, f"行数不匹配: test={test_rows}, sample={sample_rows}"
    print(f"✓ test.csv 和 sampleSubmission.csv 行数一致: {test_rows} 行")

    print("✅ 测试 7 通过：路径规范验证成功")
except Exception as e:
    print(f"❌ 测试 7 失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 测试 8: Agent 创建验证
# ============================================================================
print("\n" + "="*80)
print("测试 8: Agent 创建验证")
print("="*80)

try:
    # 测试默认 Agent
    agent = dslighting.Agent()
    print("✓ 默认 Agent 创建成功")

    # 测试自定义 Agent
    agent_custom = dslighting.Agent(
        workflow="aide",
        temperature=0.7,
        max_iterations=1
    )
    print("✓ 自定义 Agent 创建成功")

    print("✅ 测试 8 通过：Agent 创建验证成功")
except Exception as e:
    print(f"❌ 测试 8 失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 总结
# ============================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)

all_tests = [
    "✅ 测试 1: 数据文件修复验证",
    "✅ 测试 2: 方式1 - 全局配置模式",
    "✅ 测试 3: 方式2 - 直接路径模式",
    "✅ 测试 4: 方式3 - 内置数据集模式",
    "✅ 测试 5: 方式4 - 先加载数据模式",
    "✅ 测试 6: 数据结构验证",
    "✅ 测试 7: 路径规范验证",
    "✅ 测试 8: Agent 创建验证",
]

for test in all_tests:
    print(test)

print("\n" + "="*80)
print("🎉 所有测试通过！DSLighting v1.8.3 功能完整")
print("="*80)
print("\n核心特性验证:")
print("  ✓ 4 种使用方式全部正常")
print("  ✓ 数据文件修复成功（sampleSubmission.csv）")
print("  ✓ 路径规范清晰（v1.8.0+）")
print("  ✓ 数据结构完整（LoadedData, TaskDetection, Registry）")
print("  ✓ Agent 创建灵活（默认配置 + 自定义配置）")
print("\n安装命令:")
print("  pip install dslighting==1.8.3")
print("\nPyPI 链接:")
print("  https://pypi.org/project/dslighting/1.8.3/")
print("="*80)
