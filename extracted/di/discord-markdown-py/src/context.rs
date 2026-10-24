use std::{collections::HashSet, fmt::Debug, marker::PhantomData, rc::Rc};

use nom::Parser;
use start_sequence::StartSequence;
use syntax_set::ContextualSyntaxes;
use terminal_sequence::TerminalSequence;

use crate::{
	context::{fuel::Fuel, line_prefix::LinePrefix, matched_pairs::MatchedPairsParser},
	error::ParseError,
	range::delim::Offset,
	scope::Scope,
};

use super::{
	Input,
	node::Element,
	scope::ScopeSet,
	span::Span,
	syntax::{Syntax, SyntaxHints, SyntaxSet},
};

pub mod fuel;
mod line_prefix;
mod matched_pairs;
mod start_sequence;
mod syntax;
mod syntax_set;
mod terminal_sequence;

/// The amount of fuel [`Options::default`] gives a parse.
///
/// Sized so that content a user can plausibly send finishes with a wide margin, while a
/// pathological input still terminates. Two measurements set it, taken against a release build:
///
/// - Real messages are nowhere near it. The announcement posts in `test_content` need 12–66 fuel;
///   ordinary prose costs about 1 fuel per line plus well under 1 per 100 bytes, because a run of
///   plain text is a single inline parse no matter how long it is.
/// - Adversarial input is what costs. The most expensive 4000-character inputs the timeout tests
///   know about -- short lines that each open a delimiter, some before block syntax -- burn about
///   2.6k, under 1 fuel per byte, in about 3ms. That is the realistic worst case for a Discord
///   message, whose limit is 4000 characters, and this default is far above it.
///
/// Modifiers no longer backtrack at all, so the default leaves room for rules that might. The
/// effect is to cap a pathological parse rather than letting it run unbounded. A caller parsing
/// only message-length content can safely tighten this a long way; see [`Options::fuel`] for what
/// moving it in either direction costs.
pub const DEFAULT_FUEL: u32 = 500_000;

#[derive(Debug, Clone, Copy)]
pub struct Options {
	/// The syntax the parse recognizes. Anything written in syntax outside this set is text.
	pub syntaxes: SyntaxSet,
	/// Whether a link may carry the `dev` scheme, e.g. `dev://branch/main`. The surfaces it
	/// reaches only exist in some clients.
	///
	/// This is not a [`Syntax`]: every way of writing a link can carry the scheme. Without it a
	/// `dev` URL is not a URL, so every way of writing one is text.
	pub dev_links: bool,
	/// How much work the parse is allowed to do before it gives up with
	/// [`fuel::OutOfFuel`].
	///
	/// One unit of fuel buys one invocation of the inline parser, or one line of block content.
	/// Those are the parser's units of backtracking, so the count includes every attempt that a
	/// rule later abandons — which is exactly where pathological input spends its time. Fuel is a
	/// single tank shared by the whole parse, not a per-rule or per-nesting-level allowance, so it
	/// bounds total work rather than depth.
	///
	/// Fuel consumption tracks the parser's running time, but it is not a wall-clock budget. A unit
	/// costs on the order of a quarter of a microsecond in a release build, but a single unit's cost
	/// varies with the input, resolving modifiers is not metered at all (it is linear), and rule
	/// changes move it. Treat a fuel figure as a bound on work, and re-measure after changing the
	/// parser rather than assuming it still buys the same number of milliseconds.
	///
	/// Raising this lets more (or more adversarial) content parse, at the cost of a higher
	/// worst-case time and allocation count per parse. Lowering it caps that worst case more
	/// tightly, at the risk of rejecting legitimate content — a parse that runs dry fails outright
	/// with [`fuel::OutOfFuel`] and returns no partial AST, so a limit set too low is a
	/// correctness bug, not a graceful degradation. Callers running untrusted content under a
	/// latency budget should pick a value by measuring their own corpus and leaving generous
	/// headroom; [`DEFAULT_FUEL`] is that measurement done against Discord's 4000-character
	/// message limit.
	pub fuel: u32,
}

impl Default for Options {
	fn default() -> Self {
		Self {
			syntaxes: SyntaxSet::all(),
			dev_links: true,
			fuel: DEFAULT_FUEL,
		}
	}
}

impl Options {
	/// The bit of [`Options::flags`] that sets [`Options::dev_links`]. The bits below it are
	/// [`Options::syntaxes`], each at its [`Syntax`]'s discriminant.
	///
	/// It sits below the sign bit so that every flag is a positive 32-bit integer, which
	/// JavaScript's bitwise operators and Kotlin's `Int` both keep intact.
	///
	/// Its bit is public, like every syntax's, so it never moves. A syntax given this bit or a
	/// higher one fails to compile; see [`Options::SYNTAX_BITS`].
	pub const DEV_LINKS: u32 = 1 << 30;

	/// The bits of [`Options::flags`] that hold [`Options::syntaxes`]: everything below
	/// [`Options::DEV_LINKS`].
	pub const SYNTAX_BITS: u32 = Self::DEV_LINKS - 1;

	/// Every flag: all syntax, and [`Options::DEV_LINKS`]. These are all the bits below the sign
	/// bit, so there is no room for another syntax without moving to a wider integer.
	pub const ALL_FLAGS: u32 = Self::SYNTAX_BITS | Self::DEV_LINKS;

	/// Options from the integer the bindings take: a [`SyntaxSet`]'s bits plus
	/// [`Options::DEV_LINKS`]. Bits no syntax uses are ignored, so `u32::MAX` allows everything
	/// this version knows of.
	///
	/// Zero allows everything too, like [`Options::ALL_FLAGS`]: a parse with no syntax at all is
	/// just text, so zero is free to mean the default instead. Since unused bits are ignored, flags
	/// holding only those count as zero.
	#[must_use]
	pub fn from_flags(flags: u32, fuel: u32) -> Self {
		let flags = match flags & Self::ALL_FLAGS {
			0 => Self::ALL_FLAGS,
			flags => flags,
		};
		Self {
			// only the syntax bits, so `DEV_LINKS` could never be read as a syntax even if one
			// were given its bit
			syntaxes: SyntaxSet::from_u32_truncated(flags & Self::SYNTAX_BITS),
			dev_links: flags & Self::DEV_LINKS != 0,
			fuel,
		}
	}

	/// These options' flags; see [`Options::from_flags`].
	#[must_use]
	pub fn flags(&self) -> u32 {
		let dev_links = if self.dev_links { Self::DEV_LINKS } else { 0 };
		self.syntaxes.as_u32() | dev_links
	}
}

// Every syntax's bit has to sit below `DEV_LINKS`, or the two would share a bit in the flags the
// bindings send. `bit_width` is one past the highest discriminant, so this fails to compile as soon
// as a syntax is numbered into `DEV_LINKS` or above.
const _: () = assert!(
	SyntaxSet::bit_width() <= Options::DEV_LINKS.trailing_zeros(),
	"a `Syntax` discriminant reaches `Options::DEV_LINKS`: there are no free flag bits left, so \
	 adding a syntax means widening the flags, not taking this bit"
);

// `ALL_FLAGS` stays a positive `i32`, as JavaScript and Kotlin need.
const _: () = assert!(Options::ALL_FLAGS <= i32::MAX as u32);

/// An inline parse context which controls how child parsers handle child and terminal content.
///
/// As we descend the parse tree, context accumulates disabled syntax and global terminals based on
/// each [`Scope`]. This is essential for 2 purposes:
///
/// 1. Parent scopes can control what syntax is enabled inside them.
/// 2. Parent scopes can get terminated rather than beginning a new node.
///
/// As context descends, each [`Scope::disabled_syntaxes`] is subtracted from the parent
/// [`Context::syntaxes`]. This ensures that the allowed syntax only becomes more restrictive.
///
/// Each scope is accumulated in a [`ScopeSet`] which parses the [`Scope::terminal_sequence`] and
/// [`Scope::global_terminal_sequence`] in [`Context::guard_terminal_sequence`].
#[derive(Debug, Clone)]
pub struct Context {
	/// The scope being parsed.
	pub scope: Scope,
	/// Syntax allowed in this scope, derived from all enclosing scopes.
	pub syntaxes: SyntaxSet,
	/// See [`Options::dev_links`].
	pub dev_links: bool,
	// This struct is huge so we reference count it to keep it off the stack and reduce allocations
	pub hints: Rc<SyntaxHints>,
	/// The depth of the innermost enclosing list, used to implement a cap to list depth. This is
	/// 1-indexed for lists — an unnested list is at depth 1 — and is 0 when not inside a list at
	/// all.
	///
	/// This is a `u8` because the maximum is [`crate::node::block::list::MAX_DEPTH`].
	pub list_depth: u8,
	parents: ScopeSet,
	/// Shared by every context of a parse, including the ones [`Context::fresh`] hands out, so that
	/// the budget covers the parse as a whole rather than resetting per scope. See
	/// [`Context::remaining_fuel`].
	fuel: Fuel,
	/// See [`Context::is_disabled_opener`].
	disabled_openers: Rc<HashSet<Offset>>,
}

impl Context {
	/// Create a new context from the specified options.
	#[must_use]
	pub fn new(options: Options) -> Self {
		Self {
			scope: Scope::None,
			syntaxes: options.syntaxes,
			dev_links: options.dev_links,
			hints: Rc::new(SyntaxHints::default()),
			list_depth: 0,
			parents: ScopeSet::new(),
			fuel: Fuel::new(options.fuel),
			disabled_openers: Rc::new(HashSet::new()),
		}
	}

	#[must_use]
	pub fn with_disabled_openers(self, disabled: &HashSet<Offset>) -> Self {
		let disabled_openers = Rc::new(self.disabled_openers.union(disabled).copied().collect());

		Self {
			disabled_openers,
			..self
		}
	}

	/// Whether the delimiter run at `offset` is one that an earlier parse read before block syntax,
	/// as in `*1. foo`, but that matched nothing. Its line is a paragraph; see
	/// [`crate::range::delim::opener`].
	#[must_use]
	pub fn is_disabled_opener(&self, offset: Offset) -> bool {
		self.disabled_openers.contains(&offset)
	}

	/// This parse's fuel tank, started at [`Options::fuel`]. The inline parser spends a unit per
	/// invocation and the block parser a unit per line.
	///
	/// This is how a caller measures what its own corpus costs, which is what picking a value for
	/// [`Options::fuel`] rests on. [`crate::parse`] builds its context internally, so measuring
	/// means driving the parser directly and keeping a handle on the context — every context
	/// derived from it draws down the same tank, so the one here still reflects the whole parse
	/// when it finishes:
	///
	/// ```
	/// # use discord_markdown::{context::{Context, Options}, node::block};
	/// # use nom::{combinator::all_consuming, Finish, Parser};
	/// let options = Options::default();
	/// let context = Context::new(options);
	///
	/// let result = all_consuming(block::block::<(), nom::error::Error<_>>(context.clone()))
	///     .parse_complete("**hello** world".into())
	///     .finish();
	///
	/// assert!(result.is_ok());
	/// println!("used {} fuel", options.fuel - context.remaining_fuel().get());
	/// ```
	#[must_use]
	pub fn remaining_fuel(&self) -> &Fuel {
		&self.fuel
	}

	/// Create a new context with a deeper list level.
	#[must_use]
	pub fn with_deeper_list(&self) -> Context {
		Context {
			list_depth: self.list_depth + 1,
			..self.clone()
		}
	}

	/// Create a new context by entering `scope`. This will subtract the
	/// [`Scope::disabled_syntaxes`] from the current allowed syntax.
	#[must_use]
	pub fn with_scope(self, scope: Scope) -> Context {
		Context {
			scope,
			syntaxes: self.syntaxes - scope.disabled_syntaxes(),
			parents: self.parents | self.scope,
			..self
		}
	}

	#[must_use]
	pub fn with_hints(&self, input: &Input) -> Self {
		if !self.hints.any_unknown() {
			return self.clone();
		}

		let hints = self.hints.for_syntaxes(self.syntaxes, input);

		Self {
			hints: Rc::new(hints),
			..self.clone()
		}
	}

	/// Create a fresh context with the same allowed syntax but reset all scope state. It still
	/// draws from this parse's fuel tank.
	#[must_use]
	pub fn fresh(&self) -> Self {
		Self {
			scope: Scope::None,
			syntaxes: self.syntaxes,
			dev_links: self.dev_links,
			hints: Rc::new(SyntaxHints::default()),
			list_depth: 0,
			parents: ScopeSet::new(),
			fuel: self.fuel.clone(),
			disabled_openers: Rc::clone(&self.disabled_openers),
		}
	}

	/// Parse any allowed inline syntax in the current context. Modifiers are not among them: they
	/// are recorded as delimiters and resolved afterwards; see [`crate::range`].
	#[must_use]
	pub fn allowed_inline_syntax<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Element<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualSyntaxes::from_context(self, self.syntaxes & Syntax::INLINE)
	}

	/// Parse any allowed block syntax in the current context.
	#[must_use]
	pub fn allowed_block_syntax<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Element<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualSyntaxes::from_context(self, self.syntaxes & Syntax::BLOCK)
	}

	/// Get allowed start sequences for the current context. This is based on [`Self::syntaxes`]:
	/// for example, if [`Syntax::Code`] is in this set, then this will match its start sequence
	/// (`` ` ``).
	#[must_use]
	pub fn allowed_start_sequences<'ctx, 'data, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data> + 'ctx,
	{
		StartSequence(self.syntaxes, PhantomData)
	}

	/// Check whether we are in a terminal sequence; if not, apply the `normal` parser. Fails if a
	/// terminal sequence is encountered.
	pub fn guard_terminal_sequence<'ctx, 'data, O, E, P>(
		&'ctx self,
		normal: impl Fn() -> P + 'ctx,
	) -> impl Parser<Input<'data>, Output = O, Error = E> + 'ctx
	where
		E: ParseError<'data> + 'ctx,
		P: Parser<Input<'data>, Output = O, Error = E> + 'ctx,
		O: Debug,
	{
		TerminalSequence {
			context: self,
			normal,
			error: PhantomData,
		}
	}

	#[must_use]
	pub fn matched_pairs<'data, E>(
		&self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		MatchedPairsParser {
			scopes: self.scopes(),
			error: PhantomData,
		}
	}

	/// The line prefix required at the start of each line in this context, e.g. `> ` inside a
	/// quote. Matches the empty string when there is no enclosing container, so it can be applied
	/// unconditionally at the start of every line.
	#[must_use]
	pub fn line_prefix<'data, E>(
		&self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E> + use<'data, E>
	where
		E: ParseError<'data>,
	{
		LinePrefix {
			scopes: self.scopes(),
			error: PhantomData,
		}
	}

	/// The current scope and every scope enclosing it.
	#[must_use]
	pub fn scopes(&self) -> ScopeSet {
		self.parents | self.scope
	}
}

impl Default for Context {
	fn default() -> Self {
		Self::new(Options::default())
	}
}

#[cfg(test)]
mod test {
	use super::{Context, DEFAULT_FUEL, Options};
	use crate::scope::Scope;
	use crate::syntax::{Syntax, SyntaxSet};

	/// The syntax bits fill everything below [`Options::DEV_LINKS`], and the flags round trip.
	#[test]
	fn flags_layout() {
		assert_eq!(
			SyntaxSet::all().as_u32() | Options::DEV_LINKS,
			Options::ALL_FLAGS
		);
		assert_eq!(Options::default().flags(), Options::ALL_FLAGS);

		let options = Options::from_flags(Syntax::LINKS.as_u32(), 7);
		assert_eq!(options.syntaxes, Syntax::LINKS);
		assert!(!options.dev_links);
		assert_eq!(options.fuel, 7);

		// bits no syntax uses are ignored, so every bit set allows everything
		let everything = Options::from_flags(u32::MAX, DEFAULT_FUEL);
		assert_eq!(everything.flags(), Options::ALL_FLAGS);

		// and so does no bit set, since no syntax at all would be plain text
		for flags in [0, 1 << 31] {
			let zero = Options::from_flags(flags, DEFAULT_FUEL);
			assert_eq!(zero.flags(), Options::ALL_FLAGS, "flags {flags:#x}");
		}
	}

	/// Fuel is one tank for the whole parse: every context derived from the same [`Context::new`]
	/// draws from it, so nesting cannot mint more.
	#[test]
	fn derived_contexts_share_one_tank() {
		let context = Context::new(Options {
			fuel: 4,
			..Default::default()
		});

		let child = context.clone().with_scope(Scope::Quote);
		let grandchild = child.clone().with_deeper_list();
		// `fresh` resets scope state, but deliberately not the budget.
		let unrelated = grandchild.fresh();

		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(ctx.remaining_fuel().consume());
			assert_eq!(context.remaining_fuel(), ctx.remaining_fuel());
		}

		assert_eq!(*context.remaining_fuel(), 0);
		// The fourth draw emptied the tank; every context now reports empty rather than one of
		// them still holding a reserve.
		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(!ctx.remaining_fuel().consume());
		}
	}
}
