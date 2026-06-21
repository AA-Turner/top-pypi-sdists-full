#[derive(Debug)]
pub enum Change {
    AppendTop {
        new: Vec<tombi_syntax::SyntaxElement>,
    },
    Append {
        base: tombi_syntax::SyntaxElement,
        new: Vec<tombi_syntax::SyntaxElement>,
    },
    Remove {
        target: tombi_syntax::SyntaxElement,
    },
    ReplaceRange {
        old: std::ops::RangeInclusive<tombi_syntax::SyntaxElement>,
        new: Vec<tombi_syntax::SyntaxElement>,
    },
}
