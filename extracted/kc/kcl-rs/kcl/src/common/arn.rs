//! Minimal port of the AWS SDK `software.amazon.awssdk.arns.Arn` /
//! `ArnResource` types.
//!
//! The Rust AWS SDK crates do not expose a standalone ARN parser, but the KCL
//! relies on a handful of ARN operations: parsing, accessing
//! `partition`/`service`/`region`/`accountId`, splitting the resource into a
//! `resourceType`/`resource`, and round-tripping back to the canonical
//! `arn:partition:service:region:account:resource` string. This module
//! reproduces exactly those behaviors.

/// The resource portion of an ARN, split into type / resource / qualifier.
///
/// Mirrors `software.amazon.awssdk.arns.ArnResource`.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ArnResource {
    resource_type: Option<String>,
    resource: String,
    qualifier: Option<String>,
}

impl ArnResource {
    /// Parse a resource string, e.g. `stream/my-stream` -> type `stream`,
    /// resource `my-stream`. Matches the AWS SDK splitting rules: the resource
    /// type is delimited by the first `:` or `/`, and a trailing `:` in the
    /// remainder delimits an optional qualifier.
    pub fn from_string(resource: &str) -> ArnResource {
        // Type boundary: first ':' else first '/'.
        let type_boundary = resource.find(':').or_else(|| resource.find('/'));

        match type_boundary {
            None => ArnResource {
                resource_type: None,
                resource: resource.to_string(),
                qualifier: None,
            },
            Some(boundary) => {
                let resource_type = &resource[..boundary];
                let remainder = &resource[boundary + 1..];
                // Qualifier: next ':' in remainder.
                match remainder.find(':') {
                    Some(q) => ArnResource {
                        resource_type: Some(resource_type.to_string()),
                        resource: remainder[..q].to_string(),
                        qualifier: Some(remainder[q + 1..].to_string()),
                    },
                    None => ArnResource {
                        resource_type: Some(resource_type.to_string()),
                        resource: remainder.to_string(),
                        qualifier: None,
                    },
                }
            }
        }
    }

    /// The resource type, e.g. `stream`.
    pub fn resource_type(&self) -> Option<&str> {
        self.resource_type.as_deref()
    }

    /// The resource identifier, e.g. the stream name.
    pub fn resource(&self) -> &str {
        &self.resource
    }

    /// The optional qualifier.
    pub fn qualifier(&self) -> Option<&str> {
        self.qualifier.as_deref()
    }
}

/// An Amazon Resource Name.
///
/// Mirrors `software.amazon.awssdk.arns.Arn`. An empty region or account-id
/// segment is treated as absent (`None`), matching the SDK's `Optional`
/// semantics.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Arn {
    partition: String,
    service: String,
    region: Option<String>,
    account_id: Option<String>,
    resource: String,
}

impl Arn {
    /// Build an ARN from parts. Empty `region`/`account_id` become `None`.
    pub fn new(
        partition: impl Into<String>,
        service: impl Into<String>,
        region: Option<String>,
        account_id: Option<String>,
        resource: impl Into<String>,
    ) -> Arn {
        Arn {
            partition: partition.into(),
            service: service.into(),
            region: region.filter(|s| !s.is_empty()),
            account_id: account_id.filter(|s| !s.is_empty()),
            resource: resource.into(),
        }
    }

    /// Parse an ARN string of the form
    /// `arn:partition:service:region:account-id:resource`.
    pub fn from_string(arn: &str) -> Result<Arn, String> {
        // Split into exactly the 6 top-level segments; the resource itself may
        // contain further ':' so we bound the split.
        let parts: Vec<&str> = arn.splitn(6, ':').collect();
        if parts.len() != 6 || parts[0] != "arn" {
            return Err(format!(
                "Malformed ARN - doesn't start with 'arn:': {}",
                arn
            ));
        }
        if parts[1].is_empty() {
            return Err(format!("Malformed ARN - no AWS partition: {}", arn));
        }
        if parts[2].is_empty() {
            return Err(format!("Malformed ARN - no service specified: {}", arn));
        }
        if parts[5].is_empty() {
            return Err(format!("Malformed ARN - no resource specified: {}", arn));
        }
        Ok(Arn::new(
            parts[1].to_string(),
            parts[2].to_string(),
            Some(parts[3].to_string()),
            Some(parts[4].to_string()),
            parts[5].to_string(),
        ))
    }

    pub fn partition(&self) -> &str {
        &self.partition
    }

    pub fn service(&self) -> &str {
        &self.service
    }

    pub fn region(&self) -> Option<&str> {
        self.region.as_deref()
    }

    pub fn account_id(&self) -> Option<&str> {
        self.account_id.as_deref()
    }

    /// The raw resource string (everything after the account-id segment).
    pub fn resource_as_string(&self) -> &str {
        &self.resource
    }

    /// The parsed resource.
    pub fn resource(&self) -> ArnResource {
        ArnResource::from_string(&self.resource)
    }
}

impl std::fmt::Display for Arn {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "arn:{}:{}:{}:{}:{}",
            self.partition,
            self.service,
            self.region.as_deref().unwrap_or(""),
            self.account_id.as_deref().unwrap_or(""),
            self.resource
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_kinesis_stream_arn() {
        let arn =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/my-stream").unwrap();
        assert_eq!(arn.partition(), "aws");
        assert_eq!(arn.service(), "kinesis");
        assert_eq!(arn.region(), Some("us-east-1"));
        assert_eq!(arn.account_id(), Some("123456789012"));
        assert_eq!(arn.resource().resource_type(), Some("stream"));
        assert_eq!(arn.resource().resource(), "my-stream");
    }

    #[test]
    fn round_trips_through_to_string() {
        let s = "arn:aws:kinesis:us-east-1:123456789012:stream/my-stream";
        let arn = Arn::from_string(s).unwrap();
        assert_eq!(arn.to_string(), s);
    }

    #[test]
    fn empty_region_is_absent() {
        let arn = Arn::from_string("arn:aws:s3:::my-bucket").unwrap();
        assert_eq!(arn.region(), None);
        assert_eq!(arn.account_id(), None);
        assert_eq!(arn.resource().resource(), "my-bucket");
    }

    #[test]
    fn rejects_non_arn() {
        assert!(Arn::from_string("not-an-arn").is_err());
    }
}
