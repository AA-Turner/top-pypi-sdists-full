"""
测试 MLETaskLoader 的输出
"""
import asyncio
from pathlib import Path
from dslighting.tasks import MLETaskLoader

async def test_mle_loader():
    """测试 MLETaskLoader 是否生成了正确的 description 和 io_instructions"""

    # 创建 loader
    loader = MLETaskLoader()

    # 加载任务
    description, io_instructions, data_dir, output_path = loader.load_task("bike-sharing-demand")

    print("=" * 80)
    print("DESCRIPTION:")
    print("=" * 80)
    print(description[:500])  # 打印前500字符
    print("\n...")

    print("\n" + "=" * 80)
    print("IO INSTRUCTIONS:")
    print("=" * 80)
    print(io_instructions)

    print("\n" + "=" * 80)
    print("DATA DIR:", data_dir)
    print("OUTPUT PATH:", output_path)
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_mle_loader())
