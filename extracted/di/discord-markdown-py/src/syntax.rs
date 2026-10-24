use std::{fmt::Debug, hash::Hash, marker::PhantomData};

use enumset::{EnumSet, EnumSetType, enum_set};
use memchr::{memchr, memmem::find};
use nom::Parser;
use start_sequence::StartSequence;
use variant_struct::VariantStruct;

#[cfg(doc)]
use super::{
	node::{Block, Inline},
	scope::Scope,
};

use super::{Input, error::ParseError, node::inline::link};

mod start_sequence;

/// One way of writing markup, which a caller can enable or disable on its own.
///
/// Several syntaxes can produce the same node: [`Syntax::MaskedLink`], [`Syntax::DetectedLink`],
/// [`Syntax::AutoLink`] and [`Syntax::ContactLink`] all produce an [`Inline::Link`]. Groups such
/// as [`Syntax::LINKS`] name the usual sets.
///
/// How each is recognized varies: [`Syntax::INLINE`] and [`Syntax::BLOCK`] have parsers, tried in
/// [`Syntax::PARSE_ORDER`], while [`Syntax::MODIFIERS`] are resolved from delimiters after the
/// parse (see [`crate::range`]).
///
/// Each discriminant is the syntax's bit in a [`SyntaxSet`], which the bindings take as an integer
/// (see [`crate::Options::from_flags`]). Those bits are public: never renumber a syntax, and give a
/// new one the next free bit, whatever its place in the parse order. Bit 30 is
/// [`crate::Options::DEV_LINKS`], and a syntax numbered into it fails to compile, so today there is
/// no free bit: a new syntax needs wider flags.
#[derive(EnumSetType, Debug, PartialOrd, Ord, Hash, VariantStruct)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(rename_all = "snake_case"),
	enumset(serialize_repr = "list")
)]
pub enum Syntax {
	// inline
	/// `<:name:id>` or `<a:name:id>`
	CustomEmoji = 0,
	/// `:smile:`
	ColonEmoji = 1,
	/// A unicode emoji written as itself.
	UnicodeEmoji = 2,
	/// `[text](url "title")`
	MaskedLink = 3,
	/// A URL in running text, like `https://discord.com`.
	DetectedLink = 4,
	/// `<https://discord.com>`
	AutoLink = 5,
	/// A phone number or email address in angle brackets, like `<+1 555 0100>`.
	ContactLink = 6,
	/// `<@id>`
	UserMention = 7,
	/// `<#id>`
	ChannelMention = 8,
	/// `<@&id>`
	RoleMention = 9,
	/// `<@$id>`
	GameMention = 10,
	/// `</name:id>`
	CommandMention = 11,
	/// `@everyone`
	EveryoneMention = 12,
	/// `@here`
	HereMention = 13,
	/// `<id:home>` and the other fixed client destinations.
	StaticMention = 14,
	/// `<t:1234567890:R>`
	Timestamp = 15,
	/// ```` ``` ````
	CodeBlock = 16,
	/// `` `code` ``
	Code = 17,
	/// ``` ``code`` ```, which can hold a single backtick.
	DoubleCode = 18,
	// modifiers
	/// `**bold**`
	Bold = 19,
	/// `*italic*`
	AsteriskItalic = 20,
	/// `_italic_`
	UnderscoreItalic = 21,
	/// `__underline__`
	Underline = 22,
	/// `~~strikethrough~~`
	Strikethrough = 23,
	/// `||spoiler||`
	Spoiler = 24,
	// block
	/// `# heading`
	Heading = 25,
	/// `- item` or `1. item`
	List = 26,
	/// `> quote`, one line at a time.
	Quote = 27,
	/// `>>> quote`, quoting everything after it.
	MultilineQuote = 28,
	/// `-# small`
	Small = 29,
}

/// A collection of [`Syntax`]es.
///
/// A strict definition of inline/block syntax might preclude block elements (like the heading) from
/// appearing inside inline elements (like the italics). We are explicitly less strict because, for
/// example, it is more intuitive to italicize a large chunk of content by surrounding the entire
/// thing in italics rather than italicizing each block individually.
///
/// ```md
/// _
/// # foo
/// _
/// ```
///
/// cbindgen:ignore
pub type SyntaxSet = EnumSet<Syntax>;

impl Syntax {
	/// Syntaxes parsed within a line.
	///
	/// Inline syntax can appear anywhere, although a top-level inline node will get wrapped in a
	/// [`Block::Paragraph`] which is the base "block" node.
	pub const INLINE: SyntaxSet = enum_set!(
		Self::CustomEmoji
			| Self::ColonEmoji
			| Self::UnicodeEmoji
			| Self::MaskedLink
			| Self::DetectedLink
			| Self::AutoLink
			| Self::ContactLink
			| Self::UserMention
			| Self::ChannelMention
			| Self::RoleMention
			| Self::GameMention
			| Self::CommandMention
			| Self::EveryoneMention
			| Self::HereMention
			| Self::StaticMention
			| Self::Timestamp
			| Self::CodeBlock
			| Self::Code
			| Self::DoubleCode
	);

	/// Syntaxes that wrap inline content, recorded as delimiters and resolved after the parse.
	///
	/// A modifier wraps only inline content. Covering several blocks, it splits into a fragment
	/// inside each -- so `*1. foo\n2. bar*` is a list of two italics. See [`Inline::modifier_kind`].
	pub const MODIFIERS: SyntaxSet = enum_set!(
		Self::Bold
			| Self::AsteriskItalic
			| Self::UnderscoreItalic
			| Self::Underline
			| Self::Strikethrough
			| Self::Spoiler
	);

	/// Syntaxes parsed only at the start of a line.
	pub const BLOCK: SyntaxSet =
		enum_set!(Self::Heading | Self::List | Self::Quote | Self::MultilineQuote | Self::Small);

	/// Every way of writing an emoji.
	pub const EMOJI: SyntaxSet =
		enum_set!(Self::CustomEmoji | Self::ColonEmoji | Self::UnicodeEmoji);

	/// Every way of writing a link.
	pub const LINKS: SyntaxSet =
		enum_set!(Self::MaskedLink | Self::DetectedLink | Self::AutoLink | Self::ContactLink);

	/// Every way of writing a mention.
	pub const MENTIONS: SyntaxSet = enum_set!(
		Self::UserMention
			| Self::ChannelMention
			| Self::RoleMention
			| Self::GameMention
			| Self::CommandMention
			| Self::EveryoneMention
			| Self::HereMention
			| Self::StaticMention
	);

	/// Both ways of writing inline code.
	pub const CODE_SPANS: SyntaxSet = enum_set!(Self::Code | Self::DoubleCode);

	/// Both ways of writing an italic.
	pub const ITALIC: SyntaxSet = enum_set!(Self::AsteriskItalic | Self::UnderscoreItalic);

	/// Both ways of writing a quote.
	pub const QUOTES: SyntaxSet = enum_set!(Self::Quote | Self::MultilineQuote);

	/// The groups the bindings name alongside each syntax's own flag, by the name they give them.
	pub const GROUPS: [(&'static str, SyntaxSet); 6] = [
		("EMOJI", Self::EMOJI),
		("LINKS", Self::LINKS),
		("MENTIONS", Self::MENTIONS),
		("CODE_SPANS", Self::CODE_SPANS),
		("ITALIC", Self::ITALIC),
		("QUOTES", Self::QUOTES),
	];

	/// The name the bindings give this syntax's flag: the variant in upper snake case, e.g.
	/// `CUSTOM_EMOJI`.
	#[must_use]
	pub fn flag_name(self) -> String {
		let mut name = String::new();
		for (i, ch) in format!("{self:?}").chars().enumerate() {
			if i > 0 && ch.is_ascii_uppercase() {
				name.push('_');
			}
			name.push(ch.to_ascii_uppercase());
		}
		name
	}

	/// The order the parser tries [`Syntax::INLINE`] and [`Syntax::BLOCK`] in, kept apart from the
	/// bit numbering so that a new syntax can go anywhere in it.
	///
	/// The order matters where syntaxes share an opener: a custom emoji, an auto link, a contact
	/// link, most mentions and a timestamp all begin with `<`, and the first to match wins.
	pub const PARSE_ORDER: [Self; 24] = [
		Self::CustomEmoji,
		Self::ColonEmoji,
		Self::UnicodeEmoji,
		Self::MaskedLink,
		Self::DetectedLink,
		Self::AutoLink,
		Self::ContactLink,
		Self::UserMention,
		Self::ChannelMention,
		Self::RoleMention,
		Self::GameMention,
		Self::CommandMention,
		Self::EveryoneMention,
		Self::HereMention,
		Self::StaticMention,
		Self::Timestamp,
		Self::CodeBlock,
		Self::Code,
		Self::DoubleCode,
		Self::Heading,
		Self::List,
		Self::Quote,
		Self::MultilineQuote,
		Self::Small,
	];

	/// A parser for whatever begins this syntax. Running text stops wherever an allowed syntax
	/// could begin, so that its parser gets a chance there.
	///
	/// Fails for syntax with no such opener: modifiers, which the inline parser records as
	/// delimiters instead, unicode emoji, which text checks for itself, and block syntax, which
	/// only begins a line.
	#[must_use]
	pub fn start_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		StartSequence(self, PhantomData)
	}

	/// Compute a precheck hint for this syntax given the remaining input.
	///
	/// Returns [`ByteHint::NotApplicable`] for syntax that already fails in O(1) and needs no
	/// precheck. Returns [`ByteHint::Absent`] or [`ByteHint::Present`] for syntax whose parser
	/// would do O(N) work before failing on adversarial input.
	///
	/// Every syntax returns a non-[`ByteHint::Unknown`] value so that [`SyntaxHints`] can detect
	/// when all hints are populated and short-circuit future calls.
	#[must_use]
	pub fn precheck_hint(self, input: &Input) -> ByteHint {
		let bytes = input.as_bytes();

		match self {
			Self::MaskedLink => match find(bytes, link::masked::TEXT_LINK_DIVIDER) {
				None => ByteHint::Absent,
				Some(pos) => {
					if memchr(
						link::masked::LINK_TERMINAL,
						&bytes[pos + link::masked::TEXT_LINK_DIVIDER.len()..],
					)
					.is_some()
					{
						ByteHint::Present(input.start + pos)
					} else {
						ByteHint::Absent
					}
				}
			},
			Self::AutoLink
			| Self::ContactLink
			| Self::UserMention
			| Self::ChannelMention
			| Self::RoleMention
			| Self::GameMention
			| Self::CommandMention
			| Self::StaticMention
			| Self::Timestamp
			| Self::CustomEmoji => match memchr(b'>', bytes) {
				None => ByteHint::Absent,
				Some(pos) => ByteHint::Present(input.start + pos),
			},
			_ => ByteHint::NotApplicable,
		}
	}
}

/// A precomputed hint about whether a syntax's necessary bytes are present in the remaining
/// input. Used to skip O(N) inner-parse work when the syntax cannot possibly match.
///
/// Set once per top-level [`crate::node::inline::inline`] call via [`Syntax::precheck_hint`] and
/// propagated to child contexts so the scan is amortized.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub enum ByteHint {
	/// Not yet computed — the hint must be derived before use.
	#[default]
	Unknown,
	/// This syntax requires no precheck; always attempt it normally.
	NotApplicable,
	/// The necessary bytes are absent; the syntax cannot match at any position.
	Absent,
	/// The necessary bytes are present; the first occurrence is at this absolute byte offset.
	Present(usize),
}

/// Per-syntax precheck hints stored in [`crate::context::Context`].
///
/// Hints are computed once per top-level [`crate::node::inline::inline`] call and propagated to
/// all child contexts.
///
/// NOTE: as this struct has a field for each syntax, it is very large.
// TODO: we can probably optimize the size of this struct by only building it for syntax that needs
// byte hints.
pub type SyntaxHints = SyntaxStruct<ByteHint>;

impl SyntaxHints {
	/// Returns `true` if any tracked hint is still `Unknown` and needs to be computed.
	#[must_use]
	pub fn any_unknown(&self) -> bool {
		self.iter().any(|hint| *hint == ByteHint::Unknown)
	}

	/// Clone self with hints derived for the given `syntaxes`.
	///
	/// Calculated by running `input` through [`Syntax::precheck_hint`] for each syntax in the set.
	#[must_use]
	pub fn for_syntaxes(&self, syntaxes: SyntaxSet, input: &Input) -> Self {
		let mut new = self.clone();

		for (syntax, hint) in new.iter_variants_mut() {
			if *hint == ByteHint::Unknown {
				*hint = if syntaxes.contains(syntax) {
					syntax.precheck_hint(input)
				} else {
					ByteHint::NotApplicable
				};
			}
		}

		new
	}

	/// Whether `syntax` is known not to match anywhere in the rest of the input.
	#[must_use]
	pub fn rules_out(&self, syntax: Syntax) -> bool {
		*self.get(&syntax) == ByteHint::Absent
	}
}

#[cfg(test)]
mod test {
	use super::{Syntax, SyntaxSet};

	/// Every parsed syntax is tried exactly once.
	#[test]
	fn parse_order_covers_parsed_syntax() {
		let order = Syntax::PARSE_ORDER.into_iter().collect::<SyntaxSet>();
		assert_eq!(order.len(), Syntax::PARSE_ORDER.len());
		assert_eq!(order, Syntax::INLINE | Syntax::BLOCK);
	}

	/// The bits are what the bindings send, so they cannot move. Pin a few at either end.
	#[test]
	fn bits_are_stable() {
		assert_eq!(SyntaxSet::from(Syntax::CustomEmoji).as_u32(), 1 << 0);
		assert_eq!(SyntaxSet::from(Syntax::Bold).as_u32(), 1 << 19);
		assert_eq!(SyntaxSet::from(Syntax::Small).as_u32(), 1 << 29);
		assert_eq!(SyntaxSet::all().as_u32(), (1 << 30) - 1);
	}

	/// A flag name is unique, and none is taken by a group.
	#[test]
	fn flag_names_are_distinct() {
		assert_eq!(Syntax::CustomEmoji.flag_name(), "CUSTOM_EMOJI");

		let mut names = SyntaxSet::all()
			.iter()
			.map(Syntax::flag_name)
			.chain(Syntax::GROUPS.map(|(name, _)| name.to_owned()))
			.collect::<Vec<_>>();
		let count = names.len();
		names.sort();
		names.dedup();
		assert_eq!(names.len(), count);
	}

	#[test]
	fn sets_partition_every_syntax() {
		assert_eq!(
			SyntaxSet::all(),
			Syntax::INLINE ^ Syntax::BLOCK ^ Syntax::MODIFIERS
		);
	}

	/// The bindings take syntax sets as lists of these names.
	#[cfg(feature = "serde")]
	#[test]
	fn syntaxes_serialize_by_name() {
		let set: SyntaxSet = Syntax::MaskedLink | Syntax::AsteriskItalic;
		assert_eq!(
			serde_json::to_string(&set).expect("a syntax set serializes"),
			r#"["masked_link","asterisk_italic"]"#
		);
	}
}
