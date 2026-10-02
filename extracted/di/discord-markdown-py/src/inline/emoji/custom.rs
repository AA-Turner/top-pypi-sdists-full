use std::borrow::Cow;

use nom::{
	bytes::{tag, take_while1},
	character::{char, complete::u64},
	combinator::opt,
	error::ParseError,
	sequence::delimited,
	AsChar, IResult, Parser,
};

use crate::{unparse::Unparse, Input};

pub const OPEN_DELIMITER: &str = "<";
pub const CLOSE_DELIMITER: &str = ">";

/// A custom emoji.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Custom<'data> {
	pub animated: bool,
	pub name: Cow<'data, str>,
	pub id: u64,
}

impl Unparse for Custom<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		let Self { animated, name, id } = self;
		// The `a` sits *before* the opening colon; see [`parse`].
		let animated = if *animated { "a" } else { "" };

		write!(f, "{OPEN_DELIMITER}{animated}:{name}:{id}{CLOSE_DELIMITER}")
	}
}

/// Parse a custom emoji.
///
/// # Errors
/// If the content does not begin with a custom emoji.
pub fn parse<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Custom<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		tag(OPEN_DELIMITER),
		(
			opt(char('a')).map(|animated| animated.is_some()),
			char(':'),
			take_while1(|ch: char| ch.is_alphanum() || ch == '_'),
			char(':'),
			u64,
		),
		tag(CLOSE_DELIMITER),
	)
	.map(
		|(animated, _, name, _, id): (bool, char, Input<'data>, char, u64)| Custom {
			animated,
			name: Cow::Borrowed(name.content),
			id,
		},
	)
	.parse_complete(data)
}

#[cfg(test)]
mod test {
	use nom::{combinator::all_consuming, Finish, Parser};

	use super::parse;
	use crate::{test_utils::handle_nom_err, unparse::Unparse};

	/// A custom emoji has to unparse back into exactly what was written.
	///
	/// Transposing the `a` and the colon produced `<:a:name:id>`, and dropped the colon entirely
	/// for a still emoji -- neither of which parses back as an emoji at all.
	#[test]
	fn unparse_round_trips() {
		for s in ["<:pepe:873227248453443624>", "<a:pepe:873227248453443624>"] {
			let (rem, res) = all_consuming(parse)
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.unwrap_or_else(|err| panic!("unable to parse {s}: {err}"));

			assert_eq!(rem, "");
			assert_eq!(res.unparse().to_string(), s, "{s}");
		}
	}
}
