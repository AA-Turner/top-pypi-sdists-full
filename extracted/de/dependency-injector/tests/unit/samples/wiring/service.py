class Service:
    service_attr: int


class ServiceWithCallable:
    def __init__(self):
        self.foo = CallableDict({"bar": lambda: 10})

    def method_with_args(self, x, y):
        return x + y

    def method_with_kwargs(self, **kwargs):
        return kwargs


class CallableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self, *args, **kwargs):
        return {"args": args, "kwargs": kwargs}
