import pytest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from spring_py import Component, Configuration, ApplicationContext

@Component
class UserService:
    def get_user(self, user_id):
        return f"User {user_id}"

@Component
class OrderService:
    def process_order(self, order_id):
        return f"Processing order {order_id}"

@Configuration
class AppConfig:
    def __init__(self):
        self.database_url = "localhost:3306"

def test_component_scanning():
    """测试组件扫描功能"""
    context = ApplicationContext()
    components = context.scan_components([os.path.dirname(__file__)])
    
    # 应该找到我们定义的组件
    component_names = [cls.__name__ for cls in components]
    assert "UserService" in component_names
    assert "OrderService" in component_names
    assert "AppConfig" in component_names

def test_application_context():
    """测试应用上下文"""
    context = ApplicationContext()
    context.scan_components([os.path.dirname(__file__)])
    
    # 测试获取bean
    user_service = context.get_bean(UserService)
    assert user_service is not None
    assert user_service.get_user(123) == "User 123"

def test_bean_singleton():
    """测试Bean单例模式"""
    context = ApplicationContext()
    context.scan_components([os.path.dirname(__file__)])
    
    # 多次获取同一个Bean应该返回同一个实例
    service1 = context.get_bean(UserService)
    service2 = context.get_bean(UserService)
    assert service1 is service2

if __name__ == "__main__":
    # 简单的测试运行
    test_component_scanning()
    test_application_context()
    test_bean_singleton()
    print("All tests passed!")
