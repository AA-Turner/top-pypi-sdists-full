use nom_language::error::{convert_error, VerboseError};

use crate::Input;

pub fn handle_nom_err<'data>(input: &'data str) -> impl Fn(VerboseError<Input<'data>>) -> String {
	move |error| {
		let error = convert_error(input.into(), error);
		eprintln!("{error}");
		error
	}
}
