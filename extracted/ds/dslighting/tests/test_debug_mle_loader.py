"""
测试 MLETaskLoader 的输出，找到 io_instructions 为什么是 "target"
"""
import sys
import logging
from pathlib import Path

# 设置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s:%(lineno)d - %(message)s'
)

logger = logging.getLogger(__name__)

def test_mle_task_loader():
    """测试 MLETaskLoader.load_task() 的输出"""

    print("=" * 80)
    print("测试 MLETaskLoader")
    print("=" * 80)

    try:
        from dslighting.tasks import MLETaskLoader

        loader = MLETaskLoader()

        print("\n1. 调用 load_task('bike-sharing-demand')...")
        desc, io_ins, data_dir, output_path = loader.load_task("bike-sharing-demand")

        print("\n" + "=" * 80)
        print("输出结果:")
        print("=" * 80)
        print(f"Description 类型: {type(desc)}")
        print(f"Description 长度: {len(desc)}")
        print(f"\nDescription 前800字符:")
        print("-" * 80)
        print(desc[:800])
        print("-" * 80)

        print(f"\n\nI/O Instructions 类型: {type(io_ins)}")
        print(f"I/O Instructions 长度: {len(io_ins)}")
        print(f"\nI/O Instructions 完整内容:")
        print("-" * 80)
        print(io_ins)
        print("-" * 80)

        print(f"\n\nData 目录: {data_dir}")
        print(f"输出路径: {output_path}")
        print(f"输出路径类型: {type(output_path)}")
        print(f"输出路径是否为绝对路径: {output_path.is_absolute()}")

        # 检查问题
        print("\n" + "=" * 80)
        print("问题诊断:")
        print("=" * 80)

        if len(io_ins) < 100:
            print(f"❌ I/O Instructions 太短！只有 {len(io_ins)} 字符")
            print(f"   内容: '{io_ins}'")
            print(f"   这不正常！应该是几百字符的标准 I/O requirements")

        if "CRITICAL I/O" not in io_ins:
            print(f"❌ I/O Instructions 不包含 'CRITICAL I/O' 标志")
            print(f"   这意味着没有使用 DataAnalyzer.generate_io_instructions()")

        if "### 数据总览" not in desc and "## Directory Structure" not in desc:
            print(f"❌ Description 不包含 data_report")
            print(f"   只有原始的 description.md 内容")
            print(f"   这意味着 DataAnalyzer.analyze_data() 失败了")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

def test_data_analyzer_directly():
    """直接测试 DataAnalyzer"""

    print("\n\n" + "=" * 80)
    print("测试 DataAnalyzer")
    print("=" * 80)

    try:
        from dsat.services.data_analyzer import DataAnalyzer
        from pathlib import Path

        # 找到数据目录
        data_dir_candidates = [
            Path("/Users/liufan/Applications/Github/dslighting/data/competitions/bike-sharing-demand"),
            Path("/Users/liufan/Applications/Github/dslighting/benchmarks/mlebench/competitions/bike-sharing-demand"),
        ]

        data_dir = None
        for candidate in data_dir_candidates:
            if candidate.exists():
                data_dir = candidate
                print(f"✓ 找到数据目录: {data_dir}")
                break

        if not data_dir:
            print(f"❌ 未找到数据目录")
            return False

        analyzer = DataAnalyzer()

        print("\n2. 测试 analyze_data()...")
        data_report = analyzer.analyze_data(data_dir, task_type="kaggle")

        print(f"\nData Report 长度: {len(data_report)}")
        print(f"Data Report 前500字符:")
        print("-" * 80)
        print(data_report[:500])
        print("-" * 80)

        print("\n3. 测试 generate_io_instructions()...")
        io_ins = analyzer.generate_io_instructions("submission_test.csv", optimization_context=False)

        print(f"\nI/O Instructions 长度: {len(io_ins)}")
        print(f"I/O Instructions 完整内容:")
        print("-" * 80)
        print(io_ins)
        print("-" * 80)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success1 = test_mle_task_loader()
    success2 = test_data_analyzer_directly()

    print("\n\n" + "=" * 80)
    print("测试总结:")
    print("=" * 80)
    print(f"MLETaskLoader 测试: {'✓ 通过' if success1 else '❌ 失败'}")
    print(f"DataAnalyzer 测试: {'✓ 通过' if success2 else '❌ 失败'}")
    print("=" * 80)

    sys.exit(0 if (success1 and success2) else 1)
