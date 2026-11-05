use url::Url;

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	lossless::TokenKind,
	span::{Span, Syntax, Trace},
};

use super::{Scope, auto, verify_url};

/// The character that opens and closes a title.
const TITLE_QUOTE: char = '"';
/// The character that makes the next [`TITLE_QUOTE`] or [`TITLE_ESCAPE`] stand for itself.
const TITLE_ESCAPE: char = '\\';

/// Whether a title has to escape `ch` to contain it.
fn needs_escape(ch: char) -> bool {
	ch == TITLE_QUOTE || ch == TITLE_ESCAPE
}

/// Parse a masked link title.
///
/// A backslash escapes a double quote or another backslash; before anything else it is literal.
fn parse_title(input: &mut Input) -> PResult<String> {
	input.char(TITLE_QUOTE)?;
	let mut title = String::new();
	loop {
		title.push_str(input.take_while(|ch| !needs_escape(ch)));
		if input.char(TITLE_QUOTE).is_ok() {
			break;
		}
		input.char(TITLE_ESCAPE)?;
		match input.satisfy(needs_escape) {
			Ok(escaped) => title.push(escaped),
			Err(_) => title.push(TITLE_ESCAPE),
		}
	}
	if title.is_empty() {
		Err(Fail::NoMatch)
	} else {
		Ok(title)
	}
}

/// Parse the link segment of a masked link, including its title.
///
/// The title is shown to the reader on hover, so it carries the same guard as the text segment: a
/// title that reads as a link masks a destination the reader never sees. Like the text segment's,
/// that guard is the caller's to run.
///
/// # Errors
/// If the content does not begin with a link segment.
#[tracing::instrument(name = "segment_parser", level = "trace", skip_all, fields(ok, output))]
pub fn segment<S: Span>(
	input: &mut Input,
	context: &Context,
) -> PResult<(Url, Option<String>, S::Syntax)> {
	let link_grammar = context.clone().with_scope(Scope::MaskedLinkLink);

	let open = input.token::<S, _>(TokenKind::DestinationOpen, |input| input.char('('))?;
	// TODO: handle matched parentheses inside the link content
	let (url, url_syntax) = match input.attempt(|input| auto::auto::<S>(input, context))? {
		Some(auto) => auto,
		None => {
			input.with_token::<S, _>(TokenKind::Url, |input| verify_url(input, &link_grammar))?
		}
	};
	let title = input.attempt(|input| {
		let space = input.token::<S, _>(TokenKind::Whitespace, Input::space1)?;
		let (title, title_syntax) = input.with_token::<S, _>(TokenKind::Title, parse_title)?;
		Ok((title, space.join(title_syntax)))
	})?;
	let close = input.token::<S, _>(TokenKind::DestinationClose, |input| input.char(')'))?;

	let (title, title_syntax) = match title {
		Some((title, syntax)) => (Some(title), syntax),
		None => (None, S::Syntax::default()),
	};
	let syntax = open.join(url_syntax).join(title_syntax).join(close);
	Ok((url, title, syntax)).trace()
}
