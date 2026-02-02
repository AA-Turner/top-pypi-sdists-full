"""
直接测试 MLETaskLoader 的输出
"""
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

try:
    from dslighting.tasks import MLETaskLoader
    from pathlib import Path

    print("=" * 80)
    print("测试 MLETaskLoader")
    print("=" * 80)

    loader = MLETaskLoader()

    print("\n调用 load_task()...")
    desc, io_ins, data_dir, output_path = loader.load_task("bike-sharing-demand")

    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    print(f"Description type: {type(desc)}")
    print(f"Description length: {len(desc)}")
    print(f"\nDescription first 500 chars:")
    print(desc[:500])
    print(f"\nDescription last 500 chars:")
    print(desc[-500:])

    print(f"\n{'='*80}")
    print(f"IO Instructions type: {type(io_ins)}")
    print(f"IO Instructions length: {len(io_ins)}")
    print(f"\nIO Instructions:")
    print(io_ins)
    print(f"{'='*80}")

    print(f"\nData dir: {data_dir}")
    print(f"Output path: {output_path}")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
