
class A:
    def __init__(self) -> None:
        return 1  # bad

class B:
    def __init__(self, x) -> None:
        if x:
            return  # ok
        else:
            return []  # bad

    class BNested:
        def __init__(self) -> None:
            yield  # bad


class C:
    def func(self):
        pass

    def __init__(self, k="") -> None:
        yield from []  # bad


class D(C):
    def __init__(self, k="") -> None:
        super().__init__(k)
        return None  # bad
    
class E:
    def __init__(self) -> None:
        yield "a"
