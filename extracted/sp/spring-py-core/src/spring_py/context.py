from typing import List, Type, Optional
from .container import Container, BeanInfo
from .scanner import ComponentScanner

# 全局应用上下文实例
_application_context: Optional['ApplicationContext'] = None


class ApplicationContext:
    """应用上下文 - 管理整个应用的组件生命周期"""

    def __init__(self, base_packages: List[str] = None):
        self.container = Container()
        self.base_packages = base_packages
        
        # 设置全局上下文
        global _application_context
        _application_context = self

    def scan_components(self, base_packages: List[str] = None):
        """扫描并注册所有组件"""
        packages = base_packages or self.base_packages
        components = self.container.scan_components(packages)

        print("--- 扫描组件 ---")
        print(f"Scanned {len(components)} components:")
        for component in components:
            print(f"  - {component.__name__} ({component.__module__})")
        
        # 显示@Bean方法创建的组件
        all_beans = self.container.list_beans()
        bean_only_components = [bean for bean in all_beans if bean not in components]
        
        if bean_only_components:
            print(f"\n@Bean方法创建的组件 ({len(bean_only_components)}):")
            for bean_cls in bean_only_components:
                bean_info = self.container.get(bean_cls)
                factory_method = bean_info.attributes.get('factory_method', 'unknown')
                print(f"  - {bean_cls.__name__} (from @Bean method: {factory_method})")
        
        return components
    
    def get_bean(self, cls_or_name):
        """获取Bean实例"""
        if isinstance(cls_or_name, str):
            # 按名称查找
            bean_info = self.container.get_by_name(cls_or_name)
            if bean_info:
                return self.container.get_instance(cls_or_name)
        else:
            # 按类型查找
            return self.container.get_instance(cls_or_name)
        return None
    
    def list_components(self):
        """列出所有组件"""
        return self.container.list_beans()
    
    def get_component_info(self):
        """获取组件信息"""
        return self.container.get_component_info()


def get_application_context() -> Optional[ApplicationContext]:
    """获取全局应用上下文"""
    return _application_context


def set_application_context(context: ApplicationContext):
    """设置全局应用上下文"""
    global _application_context
    _application_context = context
