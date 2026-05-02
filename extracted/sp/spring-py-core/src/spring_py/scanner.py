"""
组件扫描器 - 扫描被Spring注解标记的类
"""

import os
import sys
import importlib
import importlib.util
import inspect
import logging
from typing import List, Type, Set, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ComponentScanner:
    """组件扫描器 - 发现被Spring注解标记的类"""
    
    def __init__(self, base_packages: List[str] = None, exclude_patterns: List[str] = None):
        """
        初始化组件扫描器
        
        Args:
            base_packages: 要扫描的基础包列表
            exclude_patterns: 要排除的模块模式列表
        """
        self.base_packages = base_packages or [self._get_default_base_package()]
        self.exclude_patterns = exclude_patterns or ['test_*', '*_test', '__pycache__']
        self.scanned_modules: Set[str] = set()
        self.found_components: List[Type] = []
        
        logger.info(f"ComponentScanner initialized with base packages: {self.base_packages}")
    
    def _get_default_base_package(self) -> str:
        """获取默认的基础包"""
        # 获取调用者的模块路径作为默认扫描路径
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)
        if caller_module and caller_module.__file__:
            return str(Path(caller_module.__file__).parent)
        return os.getcwd()
    
    def scan(self) -> List[Type]:
        """
        执行组件扫描
        
        Returns:
            发现的组件类列表
        """
        self.found_components = []
        self.scanned_modules = set()
        
        logger.info("Starting component scan...")
        
        for base_package in self.base_packages:
            try:
                self._scan_package(base_package)
            except Exception as e:
                logger.error(f"Error scanning package {base_package}: {e}")
        
        logger.info(f"Component scan completed. Found {len(self.found_components)} components in {len(self.scanned_modules)} modules")
        return self.found_components
    
    def _scan_package(self, package_path: str):
        """扫描指定包路径"""
        if os.path.isdir(package_path):
            # 扫描目录
            self._scan_directory(package_path)
        else:
            # 尝试作为模块名导入
            try:
                module = importlib.import_module(package_path)
                self._scan_module(module)
            except ImportError as e:
                logger.warning(f"Could not import module {package_path}: {e}")
    
    def _scan_directory(self, directory_path: str):
        """扫描目录中的Python文件"""
        directory = Path(directory_path)
        
        # 确保目录在Python路径中
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
        
        # 递归扫描所有.py文件
        for py_file in directory.rglob("*.py"):
            if self._should_exclude_file(py_file):
                continue
            
            # 计算模块名
            relative_path = py_file.relative_to(directory)
            module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')
            
            if module_name in self.scanned_modules:
                continue
            
            try:
                # 导入模块
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 扫描模块中的组件
                    self._scan_module(module)
                    self.scanned_modules.add(module_name)
                    
            except Exception as e:
                logger.warning(f"Error importing module {module_name} from {py_file}: {e}")
    
    def _scan_module(self, module) -> List[Type]:
        """扫描模块中的组件"""
        components = []
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # 只扫描定义在当前模块中的类
            if obj.__module__ != module.__name__:
                continue
            
            if self._is_spring_component(obj):
                components.append(obj)
                self.found_components.append(obj)
                logger.debug(f"Found component: {obj.__name__} in {module.__name__}")
        
        return components
    
    def _is_spring_component(self, cls: Type) -> bool:
        """检查类是否被Spring注解标记"""
        # 检查@Component注解
        if hasattr(cls, '__component__') and cls.__component__:
            return True
        
        # 检查@Configuration注解
        if hasattr(cls, '__configuration__') and cls.__configuration__:
            return True
        
        return False
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """检查是否应该排除文件"""
        file_name = file_path.name
        
        # 排除测试文件和其他不需要的文件
        exclude_patterns = [
            '__pycache__',
            '.pyc',
            '__init__.py',  # 可以选择是否排除
            'test_*.py',
            '*_test.py'
        ]
        
        for pattern in exclude_patterns:
            if self._match_pattern(file_name, pattern):
                return True
        
        return False
    
    def _match_pattern(self, text: str, pattern: str) -> bool:
        """简单的模式匹配"""
        if '*' not in pattern:
            return text == pattern
        
        # 简单的通配符匹配
        if pattern.startswith('*') and pattern.endswith('*'):
            return pattern[1:-1] in text
        elif pattern.startswith('*'):
            return text.endswith(pattern[1:])
        elif pattern.endswith('*'):
            return text.startswith(pattern[:-1])
        else:
            import fnmatch
            return fnmatch.fnmatch(text, pattern)
    
    def get_components_by_annotation(self, annotation_attr: str) -> List[Type]:
        """根据注解属性获取组件列表"""
        result = []
        for component in self.found_components:
            if hasattr(component, annotation_attr) and getattr(component, annotation_attr):
                result.append(component)
        return result
    
    def get_component_info(self) -> Dict[str, Any]:
        """获取扫描结果的详细信息"""
        info = {
            'total_components': len(self.found_components),
            'scanned_modules': len(self.scanned_modules),
            'components_by_type': {},
            'component_details': []
        }
        
        # 按类型统计组件
        type_counts = {'component': 0, 'configuration': 0}
        for component in self.found_components:
            if hasattr(component, '__component__') and component.__component__:
                type_counts['component'] += 1
                comp_type = 'component'
            elif hasattr(component, '__configuration__') and component.__configuration__:
                type_counts['configuration'] += 1
                comp_type = 'configuration'
            else:
                comp_type = 'unknown'
            
            # 组件详细信息
            info['component_details'].append({
                'name': component.__name__,
                'type': comp_type,
                'module': component.__module__
            })
        
        info['components_by_type'] = type_counts
        return info


def scan_components(base_packages: List[str] = None, 
                   exclude_patterns: List[str] = None) -> List[Type]:
    """
    便捷函数：扫描组件
    
    Args:
        base_packages: 要扫描的基础包列表
        exclude_patterns: 要排除的模块模式列表
        
    Returns:
        发现的组件类列表
    """
    scanner = ComponentScanner(base_packages, exclude_patterns)
    return scanner.scan()
