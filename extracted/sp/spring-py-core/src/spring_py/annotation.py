from typing import Any, Type, get_type_hints


def Component(cls: type) -> type:
    """组件注解装饰器"""
    cls.__component__ = True
    return cls

def Service(cls: type) -> type:
    """服务类注解装饰器"""
    cls.__component__ = True
    cls.__service__ = True
    return cls

def RestController(cls: type) -> type:
    """REST控制器注解装饰器"""
    cls.__component__ = True
    cls.__controller__ = True
    return cls

def Configuration(cls: type) -> type:
    """配置类注解装饰器"""
    cls.__configuration__ = True
    return cls


class Bean:
    """Bean方法装饰器"""
    def __init__(self, method):
        self.method = method
        self.method.__bean__ = True

    def __set_name__(self, owner, name):
        """
        当装饰器被应用到类方法时调用
        owner: 方法所属的类
        name:  方法名
        """
        print(f"方法 {name} 属于类: {owner.__name__}")

        # TODO: 后续可以添加验证逻辑
        # if not getattr(owner, '__configuration__', False):
        #     raise ValueError(f"@Bean 只能在 @Configuration 类中使用，但 {owner.__name__} 未标记为 @Configuration")

        self.owner = owner
        self.name = name

    def __call__(self, *args, **kwargs):
        print(f"调用 Bean: {self.method.__name__}")
        return self.method(self, *args, **kwargs)


class Autowired:
    """
    用于字段自动注入的描述符 - 使用全局上下文
    """
    def __init__(self, required: bool = True):
        self.required = required
    
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

    def __get__(self, obj, owner=None):
        if obj is None:
            return self

        # 检查是否已经注入过
        private_name = f"_autowired_{self.name}"
        if hasattr(obj, private_name):
            return getattr(obj, private_name)

        # 获取字段的类型（通过类型注解）
        dep_type = self._resolve_type()
        if dep_type is None:
            if self.required:
                raise TypeError(f"字段 {self.owner.__name__}.{self.name} 缺少类型注解或无法解析")
            return None

        # 从全局容器获取实例
        from .global_context import get_bean, is_context_initialized
        
        if not is_context_initialized():
            if self.required:
                raise RuntimeError(f"GlobalContext未初始化，无法注入 {dep_type}")
            return None

        try:
            instance = get_bean(dep_type)
            if instance is None and self.required:
                # 尝试按类名查找
                instance = get_bean(dep_type.__name__.lower())
                
            if instance is None and self.required:
                raise ValueError(f"无法从容器中获取 {dep_type} 的实例")
            
            # 缓存注入的实例
            if instance is not None:
                setattr(obj, private_name, instance)
            return instance
            
        except Exception as e:
            if self.required:
                raise RuntimeError(f"依赖注入失败: {e}")
            return None
    
    def _resolve_type(self):
        """解析类型注解"""
        try:
            # 首先尝试使用get_type_hints（处理大多数情况）
            hints = get_type_hints(self.owner)
            if self.name in hints:
                return hints[self.name]
        except (NameError, AttributeError, TypeError):
            pass
        
        # 如果get_type_hints失败，尝试直接从__annotations__获取
        annotations = getattr(self.owner, '__annotations__', {})
        if self.name not in annotations:
            return None
            
        dep_type = annotations[self.name]
        
        # 处理字符串类型注解（前向引用）
        if isinstance(dep_type, str):
            dep_type = self._resolve_string_type(dep_type)
        
        return dep_type
    
    def _resolve_string_type(self, type_str: str):
        """解析字符串类型注解"""
        import sys
        import importlib
        
        # 获取定义这个类的模块
        module = sys.modules.get(self.owner.__module__)
        if module is None:
            return None
        
        # 首先在模块的全局命名空间中查找
        if hasattr(module, type_str):
            return getattr(module, type_str)
        
        # 尝试在模块的globals中查找
        module_globals = getattr(module, '__dict__', {})
        if type_str in module_globals:
            return module_globals[type_str]
        
        # 如果包含点号，可能是完整的模块路径
        if '.' in type_str:
            try:
                module_path, class_name = type_str.rsplit('.', 1)
                target_module = importlib.import_module(module_path)
                return getattr(target_module, class_name)
            except (ImportError, AttributeError):
                pass
        
        return None

    def __set__(self, obj, value):
        # 支持手动赋值覆盖
        private_name = f"_autowired_{self.name}"
        setattr(obj, private_name, value)
