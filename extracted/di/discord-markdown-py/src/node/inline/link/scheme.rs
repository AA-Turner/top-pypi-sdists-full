use url::Url;

use crate::rule::{Rule, RuleSet};

/// A URL scheme this parser accepts, and the rules a URL carrying it must satisfy.
pub trait Scheme {
	/// The scheme's name, as it is written before the `://`.
	fn name(&self) -> &'static str;

	/// Whether `url`, which need not carry this scheme, is a valid URL under it.
	fn validate(&self, url: &Url) -> bool;

	/// The [`Rule`] a caller must allow for a URL to carry this scheme, if any.
	fn rule(&self) -> Option<Rule> {
		None
	}

	/// Whether `rules` permits this scheme.
	fn allowed_by(&self, rules: RuleSet) -> bool {
		self.rule().is_none_or(|rule| rules.contains(rule))
	}
}

pub const HTTP: Standard = Standard("http");
pub const HTTPS: Standard = Standard("https");
pub const DISCORD: Standard = Standard("discord");
pub const DEV: Dev = Dev;
pub const TEL: Contact = Contact("tel");
pub const SMS: Contact = Contact("sms");
pub const MAILTO: Contact = Contact("mailto");

/// A scheme whose only requirement is a host.
pub struct Standard(&'static str);

impl Scheme for Standard {
	fn name(&self) -> &'static str {
		self.0
	}

	fn validate(&self, url: &Url) -> bool {
		url.scheme() == self.0 && url.has_host()
	}
}

/// A scheme that addresses a person rather than a host, such as `tel` or `mailto`.
pub struct Contact(&'static str);

impl Scheme for Contact {
	fn name(&self) -> &'static str {
		self.0
	}

	fn validate(&self, url: &Url) -> bool {
		url.scheme() == self.0 && !url.path().is_empty()
	}
}

/// The `dev` scheme, which addresses a fixed set of client surfaces rather than a host.
///
/// Gated on [`Rule::DevLink`]: the surfaces it reaches only exist in some clients.
pub struct Dev;

impl Scheme for Dev {
	fn name(&self) -> &'static str {
		"dev"
	}

	fn validate(&self, url: &Url) -> bool {
		url.scheme() == self.name()
			&& url.username().is_empty()
			&& url.password().is_none()
			&& url.port().is_none()
			&& url
				.domain()
				.is_some_and(|domain| VALID_DEV_DOMAINS.contains(&domain))
	}

	fn rule(&self) -> Option<Rule> {
		Some(Rule::DevLink)
	}
}

/// Domains that are valid for URLs with a scheme matching [`Dev`].
pub const VALID_DEV_DOMAINS: [&str; 4] = ["branch", "experiment", "playground", "devtools"];

/// Every scheme a URL may be written with.
pub static ALL: &[&(dyn Scheme + Sync)] = &[&HTTP, &HTTPS, &DISCORD, &DEV, &TEL, &SMS, &MAILTO];

/// The schemes link detection will pick a URL out of unmarked text for.
///
/// [`DISCORD`] is deliberately absent: it is valid to *write* (`<discord://foo>`), but detecting it
/// would mean treating a bare `discord` as a start sequence, and that sequence -- unlike a real
/// scheme -- can begin in the middle of a word.
pub static DETECTED: &[&(dyn Scheme + Sync)] = &[&HTTP, &HTTPS, &DEV];
