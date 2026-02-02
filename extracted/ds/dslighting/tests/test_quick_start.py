#!/usr/bin/env python3
"""
DSLighting 快速测试脚本 - 用于调试评分系统
只运行一次 iteration，快速迭代
"""

# 加载 .env 文件（必须在 import dslighting 之前）
from dotenv import load_dotenv
load_dotenv()  # 从当前目录加载 .env 文件

import dslighting
import logging
logging.basicConfig(level=logging.DEBUG)  # 启用调试日志

from dslighting.core.config_builder import ConfigBuilder
def main():
    print("=" * 80)
    print("DSLighting 快速测试 - Bike Sharing Demand")
    print("=" * 80)
    print()



    data = dslighting.load_data("bike-sharing-demand")

    # agent = dslighting.Agent(
    #     workflow="autokaggle",
    #     model= "openai/deepseek-ai/DeepSeek-V3.1-Terminus",
    #     temperature=0.7,
    #     max_iterations=1,
    # )

    agent = dslighting.Agent(
        model="openai/deepseek-ai/DeepSeek-V3.1-Terminus",  # 或其他 DeepSeek 模型
        workflow="automind",
        automind={
            "enable_rag": False  # 禁用知识库检索
        }
    )




    # 查看配置加载情况
    
    # builder = ConfigBuilder()
    # config = builder.build_config(model="openai/deepseek-ai/DeepSeek-V3.1-Terminus")
    # print(f"API Keys: {config.llm.api_keys}")
    # print(f"API Key: {config.llm.api_key}")
    # print(f"API Base: {config.llm.api_base}")

    # agent = dslighting.Agent(
    #     model= "openai/deepseek-ai/DeepSeek-V3.1-Terminus",
    #     workflow="dsagent",
    #     dsagent={
    #         "enable_rag": False  # 禁用知识库检索
    #     }
    # )


    result = agent.run(data)

    print(f"Output: {result.output}")
    print(f"Cost: ${result.cost:.2f}")

    print()
    print("=" * 80)
    print("测试结果:")
    print("=" * 80)
    print(f"成功: {result.success}")
    print(f"得分: {result.score}")
    print(f"成本: ${result.cost:.4f}")
    print(f"耗时: {result.duration:.1f} 秒")
    if result.workspace_path:
        print(f"工作空间: {result.workspace_path}")
    print()


if __name__ == "__main__":
    main()
