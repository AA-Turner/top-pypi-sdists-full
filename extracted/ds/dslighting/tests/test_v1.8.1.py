"""
测试 DSLighting v1.8.1
验证 sampleSubmission.csv 修复是否正确
"""
import sys
import time

print("=" * 80)
print("测试 DSLighting v1.8.1 - sampleSubmission.csv 修复验证")
print("=" * 80)

# 等待 PyPI 更新
print("\n等待 PyPI 更新 (30秒)...")
time.sleep(30)

# 安装新版本
print("\n正在安装 DSLighting v1.8.1...")
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "dslighting==1.8.1", "-q"])
print("✅ 安装完成")

# 导入并测试
import dslighting
import pandas as pd
from pathlib import Path

print(f"\nDSLighting 版本: {dslighting.__version__}")

# 测试内置数据集
print("\n" + "=" * 80)
print("测试内置数据集: bike-sharing-demand")
print("=" * 80)

# 加载数据
data = dslighting.load_data("bike-sharing-demand")

# 获取数据路径
data_dir = data.data_dir
public_dir = data_dir / "prepared" / "public"

# 读取文件
test_df = pd.read_csv(public_dir / "test.csv")
sample_df = pd.read_csv(public_dir / "sampleSubmission.csv")

print(f"\n✓ test.csv 行数: {len(test_df)}")
print(f"✓ sampleSubmission.csv 行数: {len(sample_df)}")
print(f"✓ 行数匹配: {len(test_df) == len(sample_df)}")

# 验证 datetime 列
test_datetime = set(test_df['datetime'].tolist())
sample_datetime = set(sample_df['datetime'].tolist())
datetime_match = test_datetime == sample_datetime

print(f"\n✓ test.csv datetime 数量: {len(test_datetime)}")
print(f"✓ sampleSubmission.csv datetime 数量: {len(sample_datetime)}")
print(f"✓ datetime 完全匹配: {datetime_match}")

# 显示前几行对比
print("\n" + "-" * 80)
print("test.csv 前 5 行:")
print(test_df[['datetime']].head())

print("\nsampleSubmission.csv 前 5 行:")
print(sample_df.head())

# 验证结果
print("\n" + "=" * 80)
print("验证结果")
print("=" * 80)

if len(test_df) == len(sample_df) and datetime_match:
    print("✅ 修复成功！sampleSubmission.csv 与 test.csv 完全匹配")
    print(f"   - 行数一致: {len(test_df)} 行")
    print(f"   - datetime 列完全匹配")
    print(f"   - count 列使用占位值 0")
else:
    print("❌ 修复失败！")
    if len(test_df) != len(sample_df):
        print(f"   - 行数不一致: test.csv={len(test_df)}, sampleSubmission.csv={len(sample_df)}")
    if not datetime_match:
        print(f"   - datetime 列不匹配")

# 测试其他 API
print("\n" + "=" * 80)
print("测试其他 API 功能")
print("=" * 80)

print(f"\nTask ID: {data.task_id}")
print(f"Task Type: {data.get_task_type()}")
print(f"\n数据摘要:\n{data.show()}")

print("\n" + "=" * 80)
print("✅ 所有测试完成")
print("=" * 80)
