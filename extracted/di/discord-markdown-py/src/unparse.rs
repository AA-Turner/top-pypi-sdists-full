use std::fmt::{from_fn, Display, Formatter, Result};

/// Turns AST nodes back into the markdown that they came from. For example:
///
/// `{"type": "bold": "value": [{"type": "text", "value": "foo"}]}` -> `**foo**`
pub trait Unparse {
	/// Format the output markdown content
	///
	/// # Errors
	/// If formatting fails
	fn fmt(&self, f: &mut Formatter) -> Result;

	fn unparse(&self) -> impl Display {
		from_fn(|f| self.fmt(f))
	}
}

impl<T> Unparse for Vec<T>
where
	T: Unparse,
{
	fn fmt(&self, f: &mut Formatter) -> Result {
		for item in self {
			item.fmt(f)?;
		}

		Ok(())
	}
}
