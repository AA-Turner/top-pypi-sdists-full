mod builder;
mod error;
mod event;
mod marker;
mod output;
mod parse;
mod parsed;
mod parser;
mod token_set;

use error::TomlVersionedError;
pub use error::{Error, ErrorKind};
pub use event::Event;
use output::Output;
use parse::Parse;
pub use parsed::Parsed;
pub use tombi_syntax::{SyntaxKind, SyntaxNode, SyntaxToken};

pub fn parse(source: &str) -> Parsed<SyntaxNode> {
    parse_as::<tombi_ast::Root>(source)
}

#[allow(private_bounds)]
pub fn parse_as<P: Parse>(source: &str) -> Parsed<SyntaxNode> {
    let lexed = tombi_lexer::lex(source);
    let mut p = crate::parser::Parser::new(source, &lexed.tokens);

    P::parse(&mut p);

    let (tokens, events) = p.finish();

    let output = crate::event::process(events);

    let (green_tree, errs) = build_green_tree(source, &tokens, output);

    let mut errors = lexed
        .errors
        .into_iter()
        .map(crate::TomlVersionedError::from)
        .collect::<Vec<_>>();

    errors.extend(errs);

    Parsed::new(green_tree, errors)
}

pub fn parsed_and_ast(source: &str) -> (crate::Parsed<tombi_ast::Root>, tombi_ast::Root) {
    let parsed = crate::parse(source);

    let Some(parsed) = parsed.cast::<tombi_ast::Root>() else {
        unreachable!("TOML Root node is always a valid AST node even if source is empty.")
    };

    let root = parsed.tree();
    tracing::trace!("TOML AST before editing: {:#?}", root);

    (parsed, root)
}

pub fn build_green_tree(
    source: &str,
    tokens: &[tombi_lexer::Token],
    parser_output: crate::Output,
) -> (tombi_rg_tree::GreenNode, Vec<crate::TomlVersionedError>) {
    let mut builder = tombi_syntax::SyntaxTreeBuilder::<crate::TomlVersionedError>::default();

    builder::intersperse_trivia(source, tokens, &parser_output, &mut |step| match step {
        builder::Step::AddToken { kind, text } => {
            builder.token(kind, text);
        }
        builder::Step::StartNode { kind } => {
            builder.start_node(kind);
        }
        builder::Step::FinishNode => builder.finish_node(),
        builder::Step::Error { error } => builder.error(error),
    });

    builder.finish()
}

#[cfg(test)]
#[macro_export]
macro_rules! test_parser {
    {#[test] fn $name:ident($source:expr) -> Ok(_)} => {
        test_parser! {
            #[test]
            fn $name($source, Default::default()) -> Ok(_)
        }
    };

    {#[test] fn $name:ident($source:expr, $toml_version:expr) -> Ok(_)} => {
        #[test]
        fn $name() {
            use itertools::Itertools;

            let p = $crate::parse(textwrap::dedent($source).trim());
            pretty_assertions::assert_eq!(
                p.errors($toml_version).collect_vec(),
                Vec::<&$crate::Error>::new()
            )
        }
    };

    {#[test] fn $name:ident($source:expr) -> Err(
        [
            $(
                SyntaxError(
                    $error_kind:ident,
                    $line1:literal:$column1:literal..$line2:literal:$column2:literal
                )
            ),*$(,)*
        ]
    )} => {
        $crate::test_parser! {#[test] fn $name($source, Default::default()) -> Err([$(SyntaxError($error_kind, $line1:$column1..$line2:$column2)),*])}
    };

    {#[test] fn $name:ident($source:expr, $toml_version:expr) -> Err(
        [
            $(
                SyntaxError(
                    $error_kind:ident,
                    $line1:literal:$column1:literal..$line2:literal:$column2:literal
                )
            ),*$(,)*
        ]
    )} => {
        #[test]
        fn $name() {
            use itertools::Itertools;

            let p = $crate::parse(textwrap::dedent($source).trim());

            pretty_assertions::assert_eq!(
                p.errors($toml_version).collect_vec(),
                vec![$(&$crate::Error::new($error_kind, (($line1, $column1), ($line2, $column2)).into())),*]
            );
        }
    };
}
