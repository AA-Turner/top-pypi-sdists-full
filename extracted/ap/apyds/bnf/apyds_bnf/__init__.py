__all__ = ["parse", "unparse"]

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from .DspLexer import DspLexer
from .DspParser import DspParser
from .DspVisitor import DspVisitor
from .DsLexer import DsLexer
from .DsParser import DsParser
from .DsVisitor import DsVisitor


class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"line {line}:{column} {msg}")


class ParseVisitor(DspVisitor):
    def visitRule_pool(self, ctx):
        return "\n\n".join(self.visit(r) for r in ctx.rule_())

    def visitRule(self, ctx):
        result = [self.visit(t) for t in ctx.term()]
        if len(result) == 1:
            return f"----\n{result[0]}\n"
        else:
            conclusion = result.pop()
            length = max(len(premise) for premise in result)
            result.append("-" * max(length, 4))
            result.append(conclusion)
            result.append("")
            return "\n".join(result)

    def visitSymbol(self, ctx):
        return ctx.SYMBOL().getText()

    def visitParentheses(self, ctx):
        return self.visit(ctx.term())

    def visitSubscript(self, ctx):
        return f"(subscript {' '.join(self.visit(t) for t in ctx.term())})"

    def visitFunction(self, ctx):
        return f"(function {' '.join(self.visit(t) for t in ctx.term())})"

    def visitUnary(self, ctx):
        return f"(unary {ctx.getChild(0).getText()} {self.visit(ctx.term())})"

    def visitBinary(self, ctx):
        return f"(binary {ctx.getChild(1).getText()} {self.visit(ctx.term(0))} {self.visit(ctx.term(1))})"


class UnparseVisitor(DsVisitor):
    def visitRule_pool(self, ctx):
        return "\n".join(self.visit(r) for r in ctx.rule_())

    def visitRule(self, ctx):
        result = [self.visit(t) for t in ctx.term()]
        conclusion = result.pop()
        return f"{', '.join(result)} => {conclusion}"

    def visitSymbol(self, ctx):
        return ctx.SYMBOL().getText()

    def visitSubscript(self, ctx):
        return f"{self.visit(ctx.term(0))}[{', '.join(self.visit(t) for t in ctx.term()[1:])}]"

    def visitFunction(self, ctx):
        return f"{self.visit(ctx.term(0))}({', '.join(self.visit(t) for t in ctx.term()[1:])})"

    def visitUnary(self, ctx):
        return f"({ctx.getChild(1).getText()} {self.visit(ctx.term())})"

    def visitBinary(self, ctx):
        return f"({self.visit(ctx.term(0))} {ctx.getChild(1).getText()} {self.visit(ctx.term(1))})"


def parse(input: str) -> str:
    chars = InputStream(input)
    lexer = DspLexer(chars)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ThrowingErrorListener())
    tokens = CommonTokenStream(lexer)
    parser = DspParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(ThrowingErrorListener())
    tree = parser.rule_pool()
    visitor = ParseVisitor()
    return visitor.visit(tree)


def unparse(input: str) -> str:
    chars = InputStream(input)
    lexer = DsLexer(chars)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ThrowingErrorListener())
    tokens = CommonTokenStream(lexer)
    parser = DsParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(ThrowingErrorListener())
    tree = parser.rule_pool()
    visitor = UnparseVisitor()
    return visitor.visit(tree)
