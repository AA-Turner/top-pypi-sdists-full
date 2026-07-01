use std::fmt::Display;

use crate::Input;

pub trait ParseError<'data>:
	nom::error::ParseError<Input<'data>>
	+ nom::error::ContextError<Input<'data>>
	+ nom::error::FromExternalError<Input<'data>, url::ParseError>
	+ nom::error::FromExternalError<Input<'data>, Cancelled>
{
}

impl<'data> ParseError<'data> for () {}

#[cfg(test)]
impl<'data> ParseError<'data> for nom_language::error::VerboseError<Input<'data>> {}

impl<'data> ParseError<'data> for nom::error::Error<Input<'data>> {}

#[derive(Debug)]
pub struct Cancelled;

impl Display for Cancelled {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str("parse cancelled")
	}
}

impl std::error::Error for Cancelled {}
