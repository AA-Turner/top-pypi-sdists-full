"""
测试 DSLighting v1.9.0 嵌套字典参数 API

验证：
1. 新的嵌套字典格式是否正常工作
2. 旧的平铺格式是否仍然兼容
3. 参数是否正确映射到 DSATConfig
"""
import sys
sys.path.insert(0, '/Users/liufan/Applications/Github/dslighting')

from dslighting.core.config_builder import ConfigBuilder

print("=" * 80)
print("测试 DSLighting v1.9.0 嵌套字典参数 API")
print("=" * 80)

builder = ConfigBuilder()

# Helper function to test config dict (before DSATConfig conversion)
def test_config_dict(**kwargs):
    """Test _build_user_config and return the dict"""
    return builder._build_user_config(**kwargs)

# ============================================================================
# 测试 1: AutoKaggle 嵌套字典格式
# ============================================================================
print("\n测试 1: AutoKaggle 嵌套字典格式")
print("-" * 40)

config_dict = test_config_dict(
    workflow="autokaggle",
    model="gpt-4o",
    temperature=0.5,

    # 新格式：嵌套字典
    autokaggle={
        "max_attempts_per_phase": 5,
        "success_threshold": 3.5
    }
)

assert config_dict["workflow"]["name"] == "autokaggle"
assert config_dict["llm"]["model"] == "gpt-4o"
assert config_dict["llm"]["temperature"] == 0.5
assert config_dict["agent"]["autokaggle"]["max_attempts_per_phase"] == 5
assert config_dict["agent"]["autokaggle"]["success_threshold"] == 3.5

print("✓ workflow.name: autokaggle")
print("✓ llm.model: gpt-4o")
print("✓ llm.temperature: 0.5")
print("✓ agent.autokaggle.max_attempts_per_phase: 5")
print("✓ agent.autokaggle.success_threshold: 3.5")
print("✓ 测试 1 通过")

# ============================================================================
# 测试 2: AIDE 嵌套字典格式
# ============================================================================
print("\n测试 2: AIDE 嵌套字典格式")
print("-" * 40)

config_dict = test_config_dict(
    workflow="aide",
    model="gpt-4o",
    temperature=0.7,
    max_iterations=10,

    # 新格式：嵌套字典
    aide={
        "num_drafts": 5,
        "debug_prob": 0.8,
        "max_debug_depth": 10
    }
)

assert config_dict["workflow"]["name"] == "aide"
assert config_dict["agent"]["search"]["num_drafts"] == 5
assert config_dict["agent"]["search"]["debug_prob"] == 0.8
assert config_dict["agent"]["search"]["max_debug_depth"] == 10

print("✓ workflow.name: aide")
print("✓ agent.search.num_drafts: 5")
print("✓ agent.search.debug_prob: 0.8")
print("✓ agent.search.max_debug_depth: 10")
print("✓ 测试 2 通过")

# ============================================================================
# 测试 3: AutoMind 嵌套字典格式
# ============================================================================
print("\n测试 3: AutoMind 嵌套字典格式")
print("-" * 40)

config_dict = test_config_dict(
    workflow="automind",
    model="gpt-4o",
    max_iterations=10,

    # 新格式：嵌套字典
    automind={
        "case_dir": "./experience_replay"
    }
)

assert config_dict["workflow"]["name"] == "automind"
assert config_dict["workflow"]["params"]["case_dir"] == "./experience_replay"

print("✓ workflow.name: automind")
print("✓ workflow.params.case_dir: ./experience_replay")
print("✓ 测试 3 通过")

# ============================================================================
# 测试 4: DS-Agent 嵌套字典格式
# ============================================================================
print("\n测试 4: DS-Agent 嵌套字典格式")
print("-" * 40)

config_dict = test_config_dict(
    workflow="dsagent",
    model="gpt-4o",
    max_iterations=15,

    # 新格式：嵌套字典
    dsagent={
        "case_dir": "./experience_replay"
    }
)

assert config_dict["workflow"]["name"] == "dsagent"
assert config_dict["workflow"]["params"]["case_dir"] == "./experience_replay"

print("✓ workflow.name: dsagent")
print("✓ workflow.params.case_dir: ./experience_replay")
print("✓ 测试 4 通过")

# ============================================================================
# 测试 5: 旧格式兼容性（平铺格式）
# ============================================================================
print("\n测试 5: 旧格式兼容性（平铺格式）")
print("-" * 40)

config_dict = test_config_dict(
    workflow="autokaggle",
    model="gpt-4o",

    # 旧格式：平铺参数
    autokaggle_max_attempts_per_phase=5,
    autokaggle_success_threshold=3.5
)

assert config_dict["agent"]["autokaggle"]["max_attempts_per_phase"] == 5
assert config_dict["agent"]["autokaggle"]["success_threshold"] == 3.5

print("✓ 旧格式仍然兼容")
print("✓ agent.autokaggle.max_attempts_per_phase: 5")
print("✓ agent.autokaggle.success_threshold: 3.5")
print("✓ 测试 5 通过")

# ============================================================================
# 测试 6: 完整示例
# ============================================================================
print("\n测试 6: 完整示例（用户实际使用）")
print("-" * 40)

config_dict = test_config_dict(
    workflow="autokaggle",
    model="openai/deepseek-ai/DeepSeek-V3.1-Terminus",
    temperature=0.7,
    max_iterations=1,
    keep_workspace=True,

    # AutoKaggle 独有参数
    autokaggle={
        "max_attempts_per_phase": 2,
        "success_threshold": 2.5
    }
)

assert config_dict["workflow"]["name"] == "autokaggle"
assert config_dict["llm"]["model"] == "openai/deepseek-ai/DeepSeek-V3.1-Terminus"
assert config_dict["llm"]["temperature"] == 0.7
assert config_dict["run"]["keep_all_workspaces"] == True
assert config_dict["agent"]["autokaggle"]["max_attempts_per_phase"] == 2
assert config_dict["agent"]["autokaggle"]["success_threshold"] == 2.5

print("✓ 完整配置正常工作")
print("✓ workflow: autokaggle")
print("✓ model: openai/deepseek-ai/DeepSeek-V3.1-Terminus")
print("✓ temperature: 0.7")
print("✓ keep_workspace: True")
print("✓ autokaggle.max_attempts_per_phase: 2")
print("✓ autokaggle.success_threshold: 2.5")
print("✓ 测试 6 通过")

# ============================================================================
# 总结
# ============================================================================
print("\n" + "=" * 80)
print("所有测试通过！v1.9.0 嵌套字典 API 工作正常")
print("=" * 80)
print("\n验证结果:")
print("  ✅ AutoKaggle 嵌套字典格式")
print("  ✅ AIDE 嵌套字典格式")
print("  ✅ AutoMind 嵌套字典格式")
print("  ✅ DS-Agent 嵌套字典格式")
print("  ✅ 旧格式向后兼容")
print("  ✅ 完整配置示例")
print("\n新 API 优势:")
print("  ✅ 参数分类清晰")
print("  ✅ 避免命名冲突")
print("  ✅ 提高可读性")
print("  ✅ 向后兼容")
print("=" * 80)
