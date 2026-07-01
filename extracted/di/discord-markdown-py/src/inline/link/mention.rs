use std::{
	fmt::{self, Debug, Display, Formatter},
	marker::PhantomData,
	num::{NonZero, ParseIntError},
	str::FromStr,
};

use nom::{
	branch::alt,
	bytes::complete::tag,
	character::complete::{char, u64},
	combinator::{opt, recognize, value, verify},
	error::ParseError,
	sequence::{preceded, separated_pair, terminated},
	IResult, Parser,
};
use tracing::Level;

use crate::{span::TraceOk, unparse::Unparse, util::alphanumeric_with_extra, Input};

pub const SCHEME: &str = "https://";

#[derive(Debug)]
pub struct DomainError;

impl Display for DomainError {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		write!(f, "domain error")
	}
}

impl std::error::Error for DomainError {}

#[derive(Debug)]
pub struct BucketError;

impl Display for BucketError {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		write!(f, "bucket error")
	}
}

impl std::error::Error for BucketError {}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum Environment {
	Production,
	Canary,
	Ptb,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(try_from = "&str", into = "String")
)]
pub enum PrimaryDomain {
	Main(Environment),
	App(Environment),
	Staging,
}

impl PrimaryDomain {
	const MAIN_PRODUCTION: &str = "discord.com";
	const MAIN_CANARY: &str = "canary.discord.com";
	const MAIN_PTB: &str = "ptb.discord.com";
	const APP_PRODUCTION: &str = "discordapp.com";
	const APP_CANARY: &str = "canary.discordapp.com";
	const APP_PTB: &str = "ptb.discordapp.com";
	const STAGING: &str = "staging.discord.co";
}

impl Display for PrimaryDomain {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		f.write_str(match self {
			Self::Main(Environment::Production) => Self::MAIN_PRODUCTION,
			Self::Main(Environment::Canary) => Self::MAIN_CANARY,
			Self::Main(Environment::Ptb) => Self::MAIN_PTB,
			Self::App(Environment::Production) => Self::APP_PRODUCTION,
			Self::App(Environment::Canary) => Self::APP_CANARY,
			Self::App(Environment::Ptb) => Self::APP_PTB,
			Self::Staging => Self::STAGING,
		})
	}
}

impl FromStr for PrimaryDomain {
	type Err = DomainError;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		Ok(match s {
			Self::MAIN_PRODUCTION => Self::Main(Environment::Production),
			Self::MAIN_CANARY => Self::Main(Environment::Canary),
			Self::MAIN_PTB => Self::Main(Environment::Ptb),
			Self::APP_PRODUCTION => Self::App(Environment::Production),
			Self::APP_CANARY => Self::App(Environment::Canary),
			Self::APP_PTB => Self::App(Environment::Ptb),
			Self::STAGING => Self::Staging,
			_ => return Err(DomainError),
		})
	}
}

impl TryFrom<&str> for PrimaryDomain {
	type Error = <Self as FromStr>::Err;

	fn try_from(value: &str) -> Result<Self, Self::Error> {
		value.parse()
	}
}

impl From<PrimaryDomain> for String {
	fn from(value: PrimaryDomain) -> Self {
		value.to_string()
	}
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(try_from = "&str", into = "String")
)]
pub enum AttachmentDomain {
	Media,
	Images,
	Cdn,
}

impl AttachmentDomain {
	const MEDIA: &str = "media.discordapp.net";
	const IMAGES: &str = "images.discordapp.net";
	const CDN: &str = "cdn.discordapp.com";
}

impl Display for AttachmentDomain {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		f.write_str(match self {
			Self::Media => Self::MEDIA,
			Self::Images => Self::IMAGES,
			Self::Cdn => Self::CDN,
		})
	}
}

impl FromStr for AttachmentDomain {
	type Err = DomainError;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		Ok(match s {
			Self::MEDIA => Self::Media,
			Self::IMAGES => Self::Images,
			Self::CDN => Self::Cdn,
			_ => return Err(DomainError),
		})
	}
}

impl TryFrom<&str> for AttachmentDomain {
	type Error = <Self as FromStr>::Err;

	fn try_from(value: &str) -> Result<Self, Self::Error> {
		value.parse()
	}
}

impl From<AttachmentDomain> for String {
	fn from(value: AttachmentDomain) -> Self {
		value.to_string()
	}
}

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(rename_all = "snake_case")
)]
pub enum AttachmentBucket {
	Attachments,
	EphemeralAttachments,
}

impl AttachmentBucket {
	const ATTACHMENTS: &str = "attachments";
	const EPHEMERAL_ATTACHMENTS: &str = "ephemeral-attachments";
}

impl Display for AttachmentBucket {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		f.write_str(match self {
			Self::Attachments => Self::ATTACHMENTS,
			Self::EphemeralAttachments => Self::EPHEMERAL_ATTACHMENTS,
		})
	}
}

impl FromStr for AttachmentBucket {
	type Err = BucketError;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		Ok(match s {
			Self::ATTACHMENTS => Self::Attachments,
			Self::EPHEMERAL_ATTACHMENTS => Self::EphemeralAttachments,
			_ => return Err(BucketError),
		})
	}
}

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum MentionLink {
	Channel {
		domain: PrimaryDomain,
		guild_id: IdOrMe,
		channel_id: u64,
	},
	Message {
		domain: PrimaryDomain,
		guild_id: IdOrMe,
		channel_id: u64,
		message_id: u64,
	},
	Attachment {
		domain: AttachmentDomain,
		bucket: AttachmentBucket,
		channel_id: u64,
		attachment_id: u64,
		name: String,
	},
}

impl Display for MentionLink {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		match self {
			Self::Channel {
				domain,
				guild_id,
				channel_id,
			} => write!(f, "{SCHEME}{domain}/channels/{guild_id}/{channel_id}"),
			Self::Message {
				domain,
				guild_id,
				channel_id,
				message_id,
			} => write!(
				f,
				"{SCHEME}{domain}/channels/{guild_id}/{channel_id}/{message_id}"
			),
			Self::Attachment {
				domain,
				bucket,
				channel_id,
				attachment_id,
				name,
			} => {
				write!(
					f,
					"{SCHEME}{domain}/{bucket}/{channel_id}/{attachment_id}/{}",
					name.as_str()
				)
			}
		}
	}
}

impl Unparse for MentionLink {
	fn fmt(&self, f: &mut Formatter) -> fmt::Result {
		write!(f, "{self}")
	}
}

/// A snowflake ID that can also be the literal "@me".
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum IdOrMe {
	Me,
	Id(NonZero<u64>),
}

#[cfg(feature = "serde")]
impl serde::Serialize for IdOrMe {
	fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
	where
		S: serde::Serializer,
	{
		self.to_string().serialize(serializer)
	}
}

#[cfg(feature = "serde")]
impl<'de> serde::Deserialize<'de> for IdOrMe {
	fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
	where
		D: serde::Deserializer<'de>,
	{
		let s: &str = serde::Deserialize::deserialize(deserializer)?;
		s.parse().map_err(serde::de::Error::custom)
	}
}

impl Display for IdOrMe {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		match self {
			Self::Me => write!(f, "@me"),
			Self::Id(id) => write!(f, "{id}"),
		}
	}
}

impl FromStr for IdOrMe {
	type Err = ParseIntError;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		match s {
			"@me" => Ok(Self::Me),
			other => Ok(Self::Id(other.parse()?)),
		}
	}
}

fn id_or_me<'data, E>(data: Input<'data>) -> IResult<Input<'data>, IdOrMe, E>
where
	E: ParseError<Input<'data>>,
{
	alt((
		verify(u64, |val| *val != 0).map(|val| {
			IdOrMe::Id(
				val.try_into()
					.expect("value has been checked to be non-zero"),
			)
		}),
		value(IdOrMe::Me, tag("@me")),
	))
	.parse_complete(data)
}

fn main_domain_link<'data, E>(data: Input<'data>) -> IResult<Input<'data>, MentionLink, E>
where
	E: ParseError<Input<'data>>,
{
	preceded(
		tag(SCHEME),
		(
			alt((
				tag(PrimaryDomain::MAIN_PRODUCTION),
				tag(PrimaryDomain::MAIN_CANARY),
				tag(PrimaryDomain::MAIN_PTB),
				tag(PrimaryDomain::APP_PRODUCTION),
				tag(PrimaryDomain::APP_CANARY),
				tag(PrimaryDomain::APP_PTB),
				tag(PrimaryDomain::STAGING),
			))
			.map(|domain: Input<'_>| {
				domain
					.content
					.parse::<PrimaryDomain>()
					.expect("tag should produce valid values")
			}),
			preceded(tag("/channels/"), id_or_me),
			preceded(char('/'), u64),
			opt(preceded(char('/'), u64)),
		),
	)
	.map(
		|(domain, guild_id, channel_id, message_id)| match message_id {
			Some(message_id) => MentionLink::Message {
				domain,
				guild_id,
				channel_id,
				message_id,
			},
			None => MentionLink::Channel {
				domain,
				guild_id,
				channel_id,
			},
		},
	)
	.parse_complete(data)
}

fn attachment_name<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	terminated(
		recognize(separated_pair(
			alphanumeric_with_extra("_-"),
			char('.'),
			alphanumeric_with_extra("_-"),
		)),
		// NOTE: this is a pretty hacky way to represent query strings, but is accurate to how internal
		// link parsing works today
		alphanumeric_with_extra("_-=&?"),
	)
	.parse_complete(data)
}

fn media_domain_link<'data, E>(data: Input<'data>) -> IResult<Input<'data>, MentionLink, E>
where
	E: ParseError<Input<'data>>,
{
	preceded(
		tag(SCHEME),
		(
			alt((
				tag(AttachmentDomain::MEDIA),
				tag(AttachmentDomain::IMAGES),
				tag(AttachmentDomain::CDN),
			))
			.map(|domain: Input<'_>| {
				domain
					.content
					.parse::<AttachmentDomain>()
					.expect("tag should produce valid values")
			}),
			preceded(
				char('/'),
				alt((
					tag(AttachmentBucket::ATTACHMENTS),
					tag(AttachmentBucket::EPHEMERAL_ATTACHMENTS),
				))
				.map(|bucket: Input<'_>| {
					bucket
						.content
						.parse::<AttachmentBucket>()
						.expect("tag should produce valid values")
				}),
			),
			preceded(char('/'), u64),
			preceded(char('/'), u64),
			preceded(char('/'), attachment_name),
		)
			.map(
				|(domain, bucket, channel_id, attachment_id, name)| MentionLink::Attachment {
					domain,
					bucket,
					channel_id,
					attachment_id,
					name: name.to_string(),
				},
			),
	)
	.parse_complete(data)
}

struct MentionParser<E>(PhantomData<E>);

impl<E> Debug for MentionParser<E> {
	fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
		f.debug_tuple("MentionParser").field(&self.0).finish()
	}
}

impl<'data, E> Parser<Input<'data>> for MentionParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = MentionLink;
	type Error = E;

	#[tracing::instrument(name = "mention_parser", level = Level::TRACE, fields(ok))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		alt((main_domain_link, media_domain_link))
			.process::<OM>(input)
			.trace_ok()
	}
}

/// Parse mention link content. These are links to internal Discord resources (such as messages)
/// that are rendered separately from normal hyperlinking.
///
/// # Errors
/// If the content does not start with mention link content.
#[must_use]
pub fn mention_link<'data, E>() -> impl Parser<Input<'data>, Output = MentionLink, Error = E>
where
	E: ParseError<Input<'data>>,
{
	MentionParser(PhantomData)
}

#[cfg(test)]
mod test {
	use std::num::NonZero;

	use nom::{Finish, Parser};

	use crate::{
		inline::link::mention::{IdOrMe, MentionLink},
		test_utils::handle_nom_err,
	};

	use super::{mention_link, AttachmentBucket, AttachmentDomain, Environment, PrimaryDomain};

	#[test]
	fn test_channel() {
		let s = "https://discord.com/channels/123/456";
		let (rem, res) = mention_link()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("should parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			MentionLink::Channel {
				domain: PrimaryDomain::Main(Environment::Production),
				guild_id: IdOrMe::Id(NonZero::new(123).unwrap()),
				channel_id: 456,
			}
		);
	}

	#[test]
	fn test_dm_channel() {
		let s = "https://discord.com/channels/@me/123";
		let (rem, res) = mention_link()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("should parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			MentionLink::Channel {
				domain: PrimaryDomain::Main(Environment::Production),
				guild_id: IdOrMe::Me,
				channel_id: 123,
			}
		);
	}

	#[test]
	fn test_message() {
		let s = "https://discord.com/channels/123/456/789";
		let (rem, res) = mention_link()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("should parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			MentionLink::Message {
				domain: PrimaryDomain::Main(Environment::Production),
				guild_id: IdOrMe::Id(NonZero::new(123).unwrap()),
				channel_id: 456,
				message_id: 789,
			}
		);
	}

	#[test]
	fn test_dm_message() {
		let s = "https://discord.com/channels/@me/123/456";
		let (rem, res) = mention_link()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("should parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			MentionLink::Message {
				domain: PrimaryDomain::Main(Environment::Production),
				guild_id: IdOrMe::Me,
				channel_id: 123,
				message_id: 456,
			}
		);
	}

	#[test]
	#[allow(clippy::unreadable_literal)]
	fn test_attachment() {
		let s = "https://cdn.discordapp.com/attachments/1131998342231113792/1243314701262127134/file-sXRcnkYMh5xlEBbznqU8OZCH.png?ex=675b558c&is=675a040c&hm=2ad960a5518c6e769803181f963ed41aed6a506a0f92658565da8514f53d0663&";
		let (rem, res) = mention_link()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("should parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			MentionLink::Attachment {
				domain: AttachmentDomain::Cdn,
				bucket: AttachmentBucket::Attachments,
				channel_id: 1131998342231113792,
				attachment_id: 1243314701262127134,
				name: "file-sXRcnkYMh5xlEBbznqU8OZCH.png".to_string(),
			}
		);
	}
}
