class _TemplateMetaclass(type):
    def __init__(cls, name, bases, dct) -> None:
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
