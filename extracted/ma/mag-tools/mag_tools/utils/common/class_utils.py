from dataclasses import dataclass, field
from types import NoneType
from typing import Any, Optional, Type, get_origin, get_args, Union, get_type_hints


class ClassUtils:
    @staticmethod
    def get_origin_type(input_type: Type) -> Type | None:
        """
        获取原始类型
            判断输入是否为 Optional 类型，如果是，则返回其内部类型。

        :param input_type: 待检查的类型
        :return: Optional 内部的类型（如果是 Optional），否则返回原始类型或 None
        """
        origin_type = get_origin(input_type)
        if origin_type is Union:  # 判断是否为 Union 类型
            args = get_args(input_type)  # 提取 Union 内的类型参数
            # 判断是否恰好包含两个类型，并且其中一个是 NoneType
            if len(args) == 2 and NoneType in args:
                return next(arg for arg in args if arg is not NoneType)
        # 如果不是 Optional 类型，直接返回输入类型
        return origin_type if origin_type else input_type

    @staticmethod
    def isinstance(bean: Any, cls_types: [Type, ...]) -> bool:
        return any(isinstance(bean, cls_type) for cls_type in cls_types)

    @staticmethod
    def get_field_type_of_class(clazz: type, field_name: str) -> Type | None:
        """
        获取指定字段名的类型。
        :param clazz: 要检查的类
        :param field_name: 字段名
        :return: 字段的类型，如果字段不存在则返回 None
        """
        field_type = get_type_hints(clazz)
        return field_type.get(field_name, None)

    @staticmethod
    def get_field_type_of_bean(bean: Any, field_name: str) -> Optional[Type]:
        """
        根据对象和字段名获取字段的类型

        :param bean: 对象
        :param field_name: 字段名
        :return: 字段的类型
        """
        # 获取对象的类型注解
        annotations = getattr(bean, '__annotations__', {})

        # 如果字段在类型注解中，返回类型注解
        if field_name in annotations:
            return annotations[field_name]

        # 否则，尝试获取实例变量的类型
        return type(getattr(bean, field_name, None))


# 示例使用
@dataclass
class MyClass:
    name: str = field()
    age: int = field()

if __name__ == '__main__':
    obj = MyClass("Alice", 30)
    print(ClassUtils.get_field_type_of_bean(obj, 'name'))  # 输出: <class 'str'>
    print(ClassUtils.get_field_type_of_bean(obj, 'age'))  # 输出: <class 'int'>
    print(ClassUtils.get_field_type_of_class(MyClass, 'name'))  # 输出: <class 'str'>
