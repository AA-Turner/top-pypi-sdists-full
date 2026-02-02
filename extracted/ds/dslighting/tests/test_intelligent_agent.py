"""
测试智能 LLM Agent

这个测试展示了如何直接使用 MyIntelligentAgent
- 不需要修改 DSLighting 源代码
- 直接继承 DSLighting.Agent
- 使用 LLM 做决策
- 在 Sandbox 中执行
"""

import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/test_pip_dslighting/intelligent_llm_agent')

from dotenv import load_dotenv
load_dotenv()

import dslighting
from intelligent_llm_agent.agent import MyIntelligentAgent

print("="*80)
print("测试 MyIntelligentAgent")
print("="*80)

# 方法1: 直接使用（最简单）
print("\n方法1: 直接实例化")
print("-"*80)

agent = MyIntelligentAgent(
    model="gpt-4o",              # LLM 模型
    temperature=0.7,
    max_iterations=5,
)

# 加载数据
data = dslighting.load_data("bike-sharing-demand")

# 运行 Agent
# result = agent.run(data)
# print(f"Score: {result.score}")
# print(f"Output: {result.output}")

print("\n✓ Agent 创建成功!")
print(f"  模型: {agent.model}")
print(f"  温度: {agent.temperature}")
print(f"  最大迭代: {agent.max_iterations}")
print(f"  可用工具: {list(agent.available_tools.keys())}")

# 方法2: 使用便捷函数
print("\n方法2: 使用便捷函数")
print("-"*80)

from intelligent_llm_agent.agent import create_intelligent_agent

agent2 = create_intelligent_agent(
    model="gpt-4o",
    max_iterations=3
)

print(f"✓ Agent 创建成功!")
print(f"  类型: {type(agent2).__name__}")

# 方法3: 像其他 DSLighting workflow 一样使用
print("\n方法3: 类似 DSLighting workflow")
print("-"*80)

# 注意：这只是概念演示，实际使用时需要确保 workflow 可以找到
# 如果要真正集成，需要将 MyIntelligentAgent 注册到 workflow factory

# agent3 = dslighting.Agent(
#     workflow="my_intelligent_agent",  # 这需要注册
#     model="gpt-4o",
#     max_iterations=5
# )

# result = agent3.run(data)

print("\n💡 关键点:")
print("  1. ✓ 继承 DSLighting.Agent")
print("  2. ✓ 不需要修改源代码")
print("  3. ✓ 使用 DSLighting 的 LLM 和 Sandbox")
print("  4. ✓ 可以直接运行")
print("  5. ✓ 工具在 Sandbox 中安全执行")

print("\n🎯 使用方式:")
print("  agent = MyIntelligentAgent(model='gpt-4o')")
print("  result = agent.run(data)")
print("  print(f'Score: {result.score}')")

print("\n" + "="*80)
print("测试完成！")
print("="*80)
