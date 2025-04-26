use tombi_syntax::T;

use super::{Parse, Parser};
use crate::parse::{leading_comments, tailing_comment};

impl Parse for tombi_ast::Comma {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        leading_comments(p);

        assert!(p.at(T![,]));

        p.eat(T![,]);
        tailing_comment(p);
        m.complete(p, T!(,));
    }
}
