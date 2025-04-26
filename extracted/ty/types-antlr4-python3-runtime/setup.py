from setuptools import setup

name = "types-antlr4-python3-runtime"
description = "Typing stubs for antlr4-python3-runtime"
long_description = '''
## Typing stubs for antlr4-python3-runtime

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`antlr4-python3-runtime`](https://github.com/antlr/antlr4) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`antlr4-python3-runtime`.

This version of `types-antlr4-python3-runtime` aims to provide accurate annotations
for `antlr4-python3-runtime==4.13.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/antlr4-python3-runtime. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `5445a4a243f5e41c9b4ab8b4ffa93da0820218bb` and was tested
with mypy 1.10.0, pyright 1.1.363, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="4.13.0.20240519",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/antlr4-python3-runtime.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['antlr4-stubs'],
      package_data={'antlr4-stubs': ['BufferedTokenStream.pyi', 'CommonTokenFactory.pyi', 'CommonTokenStream.pyi', 'FileStream.pyi', 'InputStream.pyi', 'IntervalSet.pyi', 'LL1Analyzer.pyi', 'Lexer.pyi', 'ListTokenSource.pyi', 'Parser.pyi', 'ParserInterpreter.pyi', 'ParserRuleContext.pyi', 'PredictionContext.pyi', 'Recognizer.pyi', 'RuleContext.pyi', 'StdinStream.pyi', 'Token.pyi', 'TokenStreamRewriter.pyi', 'Utils.pyi', '__init__.pyi', '_pygrun.pyi', 'atn/ATN.pyi', 'atn/ATNConfig.pyi', 'atn/ATNConfigSet.pyi', 'atn/ATNDeserializationOptions.pyi', 'atn/ATNDeserializer.pyi', 'atn/ATNSimulator.pyi', 'atn/ATNState.pyi', 'atn/ATNType.pyi', 'atn/LexerATNSimulator.pyi', 'atn/LexerAction.pyi', 'atn/LexerActionExecutor.pyi', 'atn/ParserATNSimulator.pyi', 'atn/PredictionMode.pyi', 'atn/SemanticContext.pyi', 'atn/Transition.pyi', 'atn/__init__.pyi', 'dfa/DFA.pyi', 'dfa/DFASerializer.pyi', 'dfa/DFAState.pyi', 'dfa/__init__.pyi', 'error/DiagnosticErrorListener.pyi', 'error/ErrorListener.pyi', 'error/ErrorStrategy.pyi', 'error/Errors.pyi', 'error/__init__.pyi', 'tree/Chunk.pyi', 'tree/ParseTreeMatch.pyi', 'tree/ParseTreePattern.pyi', 'tree/ParseTreePatternMatcher.pyi', 'tree/RuleTagToken.pyi', 'tree/TokenTagToken.pyi', 'tree/Tree.pyi', 'tree/Trees.pyi', 'tree/__init__.pyi', 'xpath/XPath.pyi', 'xpath/XPathLexer.pyi', 'xpath/__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
