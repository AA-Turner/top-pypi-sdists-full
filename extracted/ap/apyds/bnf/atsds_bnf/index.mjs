import { InputStream, CommonTokenStream, ErrorListener } from "antlr4";
import DspLexer from "./DspLexer.js";
import DspParser from "./DspParser.js";
import DspVisitor from "./DspVisitor.js";
import DsLexer from "./DsLexer.js";
import DsParser from "./DsParser.js";
import DsVisitor from "./DsVisitor.js";

class ThrowingErrorListener extends ErrorListener {
    syntaxError(recognizer, offendingSymbol, line, column, msg, e) {
        throw new Error(`line ${line}:${column} ${msg}`);
    }
}

class ParseVisitor extends DspVisitor {
    visitRule_pool(ctx) {
        return ctx
            .rule_()
            .map((r) => this.visit(r))
            .join("\n\n");
    }

    visitRule(ctx) {
        const result = ctx.term().map((t) => this.visit(t));
        if (result.length === 1) {
            return `----\n${result[0]}\n`;
        } else {
            const conclusion = result.pop();
            const length = Math.max(...result.map((premise) => premise.length));
            result.push("-".repeat(Math.max(length, 4)));
            result.push(conclusion);
            result.push("");
            return result.join("\n");
        }
    }

    visitSymbol(ctx) {
        return ctx.SYMBOL().getText();
    }

    visitParentheses(ctx) {
        return this.visit(ctx.term());
    }

    visitSubscript(ctx) {
        return `(subscript ${ctx
            .term()
            .map((t) => this.visit(t))
            .join(" ")})`;
    }

    visitFunction(ctx) {
        return `(function ${ctx
            .term()
            .map((t) => this.visit(t))
            .join(" ")})`;
    }

    visitUnary(ctx) {
        return `(unary ${ctx.getChild(0).getText()} ${this.visit(ctx.term())})`;
    }

    visitBinary(ctx) {
        return `(binary ${ctx.getChild(1).getText()} ${this.visit(ctx.term(0))} ${this.visit(ctx.term(1))})`;
    }
}

class UnparseVisitor extends DsVisitor {
    visitRule_pool(ctx) {
        return ctx
            .rule_()
            .map((r) => this.visit(r))
            .join("\n");
    }

    visitRule(ctx) {
        const result = ctx.term().map((t) => this.visit(t));
        const conclusion = result.pop();
        return `${result.join(", ")} => ${conclusion}`;
    }

    visitSymbol(ctx) {
        return ctx.SYMBOL().getText();
    }

    visitSubscript(ctx) {
        return `${this.visit(ctx.term(0))}[${ctx
            .term()
            .slice(1)
            .map((t) => this.visit(t))
            .join(", ")}]`;
    }

    visitFunction(ctx) {
        return `${this.visit(ctx.term(0))}(${ctx
            .term()
            .slice(1)
            .map((t) => this.visit(t))
            .join(", ")})`;
    }

    visitUnary(ctx) {
        return `(${ctx.getChild(1).getText()} ${this.visit(ctx.term())})`;
    }

    visitBinary(ctx) {
        return `(${this.visit(ctx.term(0))} ${ctx.getChild(1).getText()} ${this.visit(ctx.term(1))})`;
    }
}

export function parse(input) {
    const chars = new InputStream(input);
    const lexer = new DspLexer(chars);
    lexer.removeErrorListeners();
    lexer.addErrorListener(new ThrowingErrorListener());
    const tokens = new CommonTokenStream(lexer);
    const parser = new DspParser(tokens);
    parser.removeErrorListeners();
    parser.addErrorListener(new ThrowingErrorListener());
    const tree = parser.rule_pool();
    const visitor = new ParseVisitor();
    return visitor.visit(tree);
}

export function unparse(input) {
    const chars = new InputStream(input);
    const lexer = new DsLexer(chars);
    lexer.removeErrorListeners();
    lexer.addErrorListener(new ThrowingErrorListener());
    const tokens = new CommonTokenStream(lexer);
    const parser = new DsParser(tokens);
    parser.removeErrorListeners();
    parser.addErrorListener(new ThrowingErrorListener());
    const tree = parser.rule_pool();
    const visitor = new UnparseVisitor();
    return visitor.visit(tree);
}
