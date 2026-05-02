import os
import ast
from typing import List, Dict, Any


class SpreadyDecoratorParser:
    def __init__(self, directoryPath: str):
        self.directoryPath = directoryPath
        self.pyFiles: List[str] = []
        self.readFilePaths()
        self.spreadyRouts: Dict[str, Any] = {}
        self.parse()

    def readFilePaths(self):
        filter = ".py"
        for path, subdirs, files in os.walk(self.directoryPath):
            for name in files:
                _f = os.path.join(path, name)
                if _f.lower().endswith(filter):
                    self.pyFiles.append(_f)

        return self.pyFiles

    @staticmethod
    def parse_ast(filename):
        with open(filename, "rt") as file:
            return ast.parse(file.read(), filename=filename)

    @staticmethod
    def top_level_functions(body):
        return (f for f in body if isinstance(f, ast.FunctionDef))

    def get_functions(self, filename):
        functions = []
        tree = self.parse_ast(filename)
        for func in self.top_level_functions(tree.body):
            functions.append(func)
        return functions

    def parse(self):
        for f in self.pyFiles:
            self.parseModule(f)
        return self.spreadyRouts

    def parseModule(self, filePath: str):
        functions = self.get_functions(filePath)
        modulePath = filePath.replace("/", ".").replace(".py", "")
        for func in functions:
            decors = func.decorator_list
            for decor in decors:
                if decor.func.id == "sproute":
                    for decor_arg in decor.keywords:
                        if decor_arg.arg == "path":
                            self.spreadyRouts[
                                decor_arg.value.value
                            ] = f"{modulePath}.{func.name}"
        return self.spreadyRouts


if __name__ == "__main__":
    p = SpreadyDecoratorParser("tests")
    print(p.spreadyRouts)
