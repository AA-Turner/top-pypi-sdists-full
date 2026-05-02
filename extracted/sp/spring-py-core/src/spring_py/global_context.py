"""
全局应用上下文管理器 - 类似Spring的ApplicationContext
"""
import threading
from typing import Optional, List, Type, Any
from .context import ApplicationContext

class GlobalContextManager:
    """全局上下文管理器 - 单例模式"""
    
    _instance: Optional['GlobalContextManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialized', False):
            self._context: Optional[ApplicationContext] = None
            self._initialized = True
    
    def initialize(self, base_packages: List[str] = None):
        """初始化全局上下文"""
        if self._context is None:
            self._context = ApplicationContext(base_packages)
            components = self._context.scan_components(base_packages)
            print(f"✓ GlobalContext initialized with {len(components)} components")
        return self._context
    
    def get_context(self) -> Optional[ApplicationContext]:
        """获取当前上下文"""
        return self._context
    
    def get_bean(self, cls_or_name) -> Any:
        """获取Bean实例"""
        if self._context is None:
            raise RuntimeError("GlobalContext not initialized. Call initialize_context() first.")
        
        result = self._context.get_bean(cls_or_name)
        
        # 调试信息
        if result is None:
            print(f"⚠️  Failed to get bean: {cls_or_name}")
            if hasattr(cls_or_name, '__name__'):
                print(f"   Type: {cls_or_name.__name__}")
                print(f"   Module: {getattr(cls_or_name, '__module__', 'unknown')}")
            
            # 显示所有已注册的Bean
            components = self._context.list_components()
            print(f"   Available beans: {[c.__name__ for c in components]}")
        
        return result
    
    def get_controllers(self):
        """获取所有控制器"""
        controllers = []
        for component in self._context.list_components():
            if hasattr(component, '__controller__'):
                controllers.append(get_bean(component))
        return controllers
    
    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._context is not None


# 全局实例
_global_manager = GlobalContextManager()

# 便捷函数
def initialize_context(base_packages: List[str] = None) -> ApplicationContext:
    """初始化全局上下文"""
    return _global_manager.initialize(base_packages)

def get_context() -> Optional[ApplicationContext]:
    """获取全局上下文"""
    return _global_manager.get_context()

def get_bean(cls_or_name) -> Any:
    """从全局上下文获取Bean"""
    return _global_manager.get_bean(cls_or_name)

def is_context_initialized() -> bool:
    """检查全局上下文是否已初始化"""
    return _global_manager.is_initialized()

def get_all_controllers() -> List[Type]:
    """获取所有控制器"""
    return _global_manager.get_controllers()