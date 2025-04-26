use tombi_syntax::SyntaxKind::{self, *};

use crate::output::Output;

#[derive(Debug, Clone)]
pub enum Event {
    Start {
        kind: tombi_syntax::SyntaxKind,
        forward_parent: Option<u32>,
    },

    Finish,

    /// Produce a single leaf-element.
    /// `n_raw_tokens` is used to glue complex contextual tokens.
    /// For example, lexer tokenizes `>>` as `>`, `>`, and
    /// `n_raw_tokens = 2` is used to produced a single `>>`.
    Token {
        kind: SyntaxKind,
        n_raw_tokens: u8,
    },

    Error {
        error: crate::TomlVersionedError,
    },
}

impl Event {
    pub(crate) fn tombstone() -> Self {
        Event::Start {
            kind: TOMBSTONE,
            forward_parent: None,
        }
    }
}

/// Generate the syntax tree with the control of events.
pub(super) fn process(mut events: Vec<Event>) -> Output {
    let mut output = Output::default();
    let mut forward_parents = Vec::new();

    for i in 0..events.len() {
        match std::mem::replace(&mut events[i], Event::tombstone()) {
            Event::Start {
                kind,
                forward_parent,
            } => {
                // For events[A, B, C], B is A's forward_parent, C is B's forward_parent,
                // in the normal control flow, the parent-child relation: `A -> B -> C`,
                // while with the magic forward_parent, it writes: `C <- B <- A`.

                // append `A` into parents.
                forward_parents.push(kind);
                let mut idx = i;
                let mut fp = forward_parent;
                while let Some(fwd) = fp {
                    idx += fwd as usize;
                    // append `A`'s forward_parent `B`
                    fp = match std::mem::replace(&mut events[idx], Event::tombstone()) {
                        Event::Start {
                            kind,
                            forward_parent,
                        } => {
                            forward_parents.push(kind);
                            forward_parent
                        }
                        _ => unreachable!(),
                    };
                    // append `B`'s forward_parent `C` in the next stage.
                }

                for kind in forward_parents.drain(..).rev() {
                    if kind != TOMBSTONE {
                        output.enter_node(kind);
                    }
                }
            }
            Event::Finish => output.leave_node(),
            Event::Token { kind, n_raw_tokens } => {
                output.token(kind, n_raw_tokens);
            }
            Event::Error { error } => output.error(error),
        }
    }

    output
}
