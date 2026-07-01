import collections
import itertools


class Element(list):
    start, split, end = None, None, None

    # Debugging aid
    def __repr__(self):
        return f"{self.__class__.__name__}([{self.expand_stack()[0]}])"

    @classmethod
    def parse(cls, chars, stack):
        # TODO: This stack is not being populated correctly and I don't know why

        stack = cls([cls.dtype()])
        while chars:
            char = chars.popleft()
            if char == cls.end:
                return stack
            if char == " ":
                continue
            if char == cls.split:
                stack.append(cls.dtype())
            elif (other_class := START_MAP.get(char)) is not None:
                other_class._parse(chars, stack)
            else:
                stack[-1] += char

        return stack

    @classmethod
    def _parse(cls, chars, stack):
        stack.append(cls.parse(chars, stack))


class Token(Element):
    dtype = str
    start, split, end = "(", None, ")"

    def expand_stack(self):
        return ["".join(self)]

    @classmethod
    def _parse(cls, chars, stack):
        depth = 1
        stack[-1] += "("

        while chars:
            char = chars.popleft()
            stack[-1] += char

            if char == "(":
                depth += 1
            if char == ")":
                depth -= 1

                if not depth:
                    return


class Serial(Element):
    dtype = Token
    start, split, end = None, ",", None

    def expand_stack(self):
        choiceSets = [item.expand_stack() for item in self]

        return [[s for s in stack if s] for stack in itertools.product(*choiceSets)]


class Parallel(Element):
    dtype = Token
    start, split, end = "{", ";", "}"

    def expand_stack(self):
        return list(itertools.chain(*[branch.expand_stack() for branch in self]))


START_MAP = {p.start: p for p in [Token, Serial, Parallel] if p.start}


def solution(specification):
    stack = Serial.parse(collections.deque(specification), [])
    call_stacks = stack.expand_stack()
    commands = []
    for call_stack in call_stacks:
        current = "input"
        for level in call_stack:
            if "(" in level:
                call, remainder = level.split("(", 1)
                current = f"{call}({current},{remainder}"
            else:
                current = f"{level}({current})"
        commands.append(current)

    # prepend a newline to each command
    # This is not a bug, but a requirement for the Codility grader.
    return "".join(f"\n{cmd}" for cmd in commands)


# print(solution("func1,func2,func3"))
print(solution("func1(kw=1),func2(1, 2, var1='a')"))
# print(solution("func1,{func2;func3}"))  # should be func2(func1(input))\nfunc3(func1(input))
# print(solution("func1,func2,{func3(x=1e-4);func3(x=1e-6);},{func4;func5},{func6}"))
