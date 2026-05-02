"""
应用启动器 - 类似Spring Boot的启动方式
"""
import os
import sys
import inspect
from typing import List, Optional, Type
from .global_context import initialize_context

class SpringApplication:
    """Spring应用启动器"""
    
    @staticmethod
    def run(main_class: Type = None, base_packages: List[str] = None):
        """
        启动Spring应用
        
        Args:
            main_class: 主类（通常是调用这个方法的类）
            base_packages: 要扫描的包列表
        """
        if main_class is None:
            # 自动获取调用者的模块
            frame = inspect.currentframe().f_back
            caller_module = inspect.getmodule(frame)
            if caller_module and caller_module.__file__:
                main_class_dir = os.path.dirname(caller_module.__file__)
                base_packages = base_packages or [main_class_dir]
        
        if base_packages is None:
            base_packages = [os.getcwd()]
        
        print(f"🚀 Starting Spring-Py application...")
        print(f"📦 Scanning packages: {base_packages}")
        
        # 初始化全局上下文
        context = initialize_context(base_packages)
        
        print(f"✅ Application started successfully!")
        return context

# 装饰器版本
def SpringBootApplication(base_packages: List[str] = None):
    """
    Spring Boot应用装饰器
    """
    def decorator(cls):
        cls._spring_base_packages = base_packages
        
        # 添加run方法到类
        def run(self):
            packages = getattr(self, '_spring_base_packages', None)
            if packages is None:
                # 使用类所在的目录
                packages = [os.path.dirname(inspect.getfile(cls))]
            return SpringApplication.run(cls, packages)
        
        cls.run = run
        return cls
    
    return decorator
