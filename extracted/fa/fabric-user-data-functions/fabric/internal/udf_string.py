# Since str can't have a binding different than the Generic binding, we change its annotation to this class so it can be bound differently
class UdfString:
    def __init__(self, value: str):
        self.value = value

    def __name__(self):
        return 'UdfString'

    def __str__(self):
        return self.value
