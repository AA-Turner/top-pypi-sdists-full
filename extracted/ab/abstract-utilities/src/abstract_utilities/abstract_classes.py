class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
def get_inputs(cls, *args, **kwargs):
    """
    Dynamically construct a dataclass instance from args and kwargs,
    filling missing values from defaults in the dataclass.
    """
    fields = list(cls.__annotations__.keys())
    values = {}

    args = list(args)
    for field in fields:
        if field in kwargs:
            values[field] = kwargs[field]
        elif args:
            values[field] = args.pop(0)
        else:
            values[field] = getattr(cls(), field)  # default from dataclass

    return cls(**values)
