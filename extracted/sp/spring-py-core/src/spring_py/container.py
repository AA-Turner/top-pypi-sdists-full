from typing import List, Type, Dict, Any, Union
import inspect


class BeanInfo:
    """Bean信息类"""
    def __init__(self, name: str, cls: Type, attributes: dict = None):
        self.name = name
        self.cls = cls
        self.attributes = attributes or {}
        self.instance = None  # 存储单例实例
        self.full_name = f"{cls.__module__}.{cls.__name__}"  # 完整类名


class Container:
    """IoC容器"""
    def __init__(self):
        self._beans: Dict[Type, BeanInfo] = {}
        self._beans_by_name: Dict[str, BeanInfo] = {}  # 按名称索引
        self._beans_by_full_name: Dict[str, BeanInfo] = {}  # 按完整类名索引
        self._scanner = None

    def register(self, bean_info: BeanInfo):
        """注册Bean"""
        self._beans[bean_info.cls] = bean_info
        self._beans_by_name[bean_info.name] = bean_info
        self._beans_by_full_name[bean_info.full_name] = bean_info

    def get(self, cls: Type) -> BeanInfo:
        """获取Bean信息"""
        # 直接类型匹配
        bean_info = self._beans.get(cls)
        if bean_info:
            return bean_info
        
        # 如果直接匹配失败，尝试通过类名和模块匹配
        cls_name = cls.__name__
        cls_module = cls.__module__
        
        # 首先尝试找相同模块的同名类
        for registered_cls, bean_info in self._beans.items():
            if (registered_cls.__name__ == cls_name and 
                registered_cls.__module__ == cls_module):
                return bean_info
        
        # 如果没有相同模块的，返回第一个同名类
        for registered_cls, bean_info in self._beans.items():
            if registered_cls.__name__ == cls_name:
                return bean_info
        
        return None

    def get_by_name(self, name: str) -> BeanInfo:
        """按名称获取Bean信息"""
        return self._beans_by_name.get(name)

    def get_by_full_name(self, full_name: str) -> BeanInfo:
        """按完整类名获取Bean信息"""
        return self._beans_by_full_name.get(full_name)

    def get_instance(self, cls_or_name: Union[Type, str]):
        """获取Bean实例（单例）"""
        if isinstance(cls_or_name, str):
            bean_info = self.get_by_name(cls_or_name)
        else:
            bean_info = self.get(cls_or_name)
            
        if bean_info is None:
            return None
        
        if bean_info.instance is None:
            # 创建实例
            try:
                bean_info.instance = bean_info.cls()
            except Exception as e:
                print(f"Error creating instance of {bean_info.cls.__name__}: {e}")
                return None
        
        return bean_info.instance

    def list_beans(self) -> List[Type]:
        """列出所有注册的Bean类型"""
        return list(self._beans.keys())

    def scan_components(self, base_packages: List[str] = None) -> List[Type]:
        """扫描并注册组件"""
        from .scanner import ComponentScanner
        import inspect
        
        if not self._scanner:
            self._scanner = ComponentScanner(base_packages)
        
        components = self._scanner.scan()
        
        # 注册发现的组件
        for component_cls in components:
            bean_info = BeanInfo(
                name=component_cls.__name__.lower(),
                cls=component_cls,
                attributes={}
            )
            self.register(bean_info)
        
        # 处理@Configuration类中的@Bean方法
        self._process_bean_methods(components)
        
        return components
    
    def _process_bean_methods(self, components: List[Type]):
        """处理@Configuration类中的@Bean方法"""
        import inspect
        from .annotation import Bean
        
        for component_cls in components:
            # 只处理@Configuration类
            if not getattr(component_cls, '__configuration__', False):
                continue
            
            print(f"🔍 Processing @Bean methods in {component_cls.__name__}")
            
            # 获取配置类实例
            config_instance = self.get_instance(component_cls)
            if config_instance is None:
                continue
            
            # 扫描类中所有属性（包括方法）
            for attr_name in dir(component_cls):
                if attr_name.startswith('_'):
                    continue
                    
                try:
                    attr = getattr(component_cls, attr_name)
                    
                    # 检查是否为Bean装饰器
                    if isinstance(attr, Bean):
                        print(f"   Found @Bean method: {attr_name}")
                        
                        # 调用@Bean方法获取实例
                        bean_instance = getattr(config_instance, attr_name)()
                        bean_class = type(bean_instance)
                        
                        # 注册Bean实例
                        bean_info = BeanInfo(
                            name=attr_name.lower(),
                            cls=bean_class,
                            attributes={'factory_method': attr_name}
                        )
                        bean_info.instance = bean_instance  # 直接设置实例
                        
                        self.register(bean_info)
                        print(f"   ✓ Registered bean: {bean_class.__name__} (name: {attr_name.lower()})")
                        
                except Exception as e:
                    print(f"   ❌ Error processing {attr_name}: {e}")
    
    def get_component_info(self):
        """获取组件扫描信息"""
        if self._scanner:
            return self._scanner.get_component_info()
        return {}
