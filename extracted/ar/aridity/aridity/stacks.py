from .model import Resolvable, Text
from .util import NoSuchPathException
from contextlib import contextmanager
import re

class ThreadLocalResolvable(Resolvable):

    def __init__(self, threadlocals, name):
        self.threadlocals = threadlocals
        self.name = name

    def resolve(self, scope):
        return getattr(self.threadlocals, self.name).resolve(scope)

class Stack:

    def __init__(self, label):
        self.stack = []
        self.label = label

    @contextmanager
    def pushimpl(self, value):
        self.stack.append(value)
        try:
            yield value
        finally:
            self.stack.pop()

    def head(self):
        try:
            return self.stack[-1]
        except IndexError:
            raise NoSuchPathException(f"Head of thread-local stack: {self.label}")

class SimpleStack(Stack):

    def push(self, value):
        return self.pushimpl(value)

    def resolve(self, scope):
        return self.head()

class IndentStack(Stack):

    class Monitor:

        nontrivialtextblock = re.compile(r'(?:.*[\r\n]+)+')
        indentpattern = re.compile(r'\s*')

        def __init__(self):
            self.parts = []

        def __call__(self, text):
            m = self.nontrivialtextblock.match(text)
            if m is None:
                self.parts.append(text)
            else:
                self.parts[:] = text[m.end():],

        def indent(self):
            return Text(self.indentpattern.match(''.join(self.parts)).group())

    def push(self):
        return self.pushimpl(self.Monitor())

    def resolve(self, scope):
        return self.head().indent()
