"""
测试使用打包后的spring-py
"""
import sys
import os

# 方式1：直接导入（如果已安装）
try:
    from spring_py import Component, Configuration, ApplicationContext
    print("✓ 成功导入spring_py包")
except ImportError:
    print("✗ 无法导入spring_py包，尝试添加路径...")
    # 方式2：添加本地src路径
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from spring_py import Component, Configuration, ApplicationContext
    print("✓ 从本地路径导入spring_py包")

@Component
class TestService:
    def test_method(self):
        return "Test successful!"

@Configuration  
class TestConfig:
    def __init__(self):
        self.test_setting = "configured"

def main():
    print("\n=== 测试Spring-Py包 ===")
    
    # 创建应用上下文
    context = ApplicationContext()
    
    # 扫描组件
    components = context.scan_components([os.path.dirname(__file__)])
    print(f"发现 {len(components)} 个组件")
    
    # 获取服务实例
    test_service = context.get_bean(TestService)
    if test_service:
        result = test_service.test_method()
        print(f"服务调用结果: {result}")
    
    # 获取配置实例
    test_config = context.get_bean(TestConfig)
    if test_config:
        print(f"配置设置: {test_config.test_setting}")
    
    print("✓ Spring-Py包测试成功！")

if __name__ == "__main__":
    main()
