from pprint import pprint
from deepdiff.difflib import SequenceMatcher


class MyClass:
    def __init__(self, x):
        self.x = x


obj1 = MyClass(1)
obj2 = MyClass(2)


t1 = [0, 1, 2, 3, 'h', 5, 6, 7, 8, 'a', 'b', 'c', obj1]
t2 = [0, 1, 2, 3, 5, 6, 7, 8, 'a', 'b', 'c', obj2]


seq = SequenceMatcher(isjunk=None, a=t1, b=t2, autojunk=False)

matching_blocks = seq.get_matching_blocks()

opscode = seq.get_opcodes()

pprint(opscode, indent=2)
