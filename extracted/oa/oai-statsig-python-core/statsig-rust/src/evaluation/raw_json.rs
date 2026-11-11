use std::{borrow::Cow, fmt};

use serde::{
    Deserialize, Deserializer,
    de::{DeserializeSeed, Error, MapAccess, Visitor},
};

// serde_json has no public borrow-or-own RawValue deserializer. Use the same
// private newtype protocol as its &RawValue and Box<RawValue implementations,
// retaining the already-validated text without copying or parsing it again.
// Compatibility tests cover borrowed, reader, and Value deserializers so a
// serde_json upgrade cannot silently change this protocol.
const RAW_VALUE_TOKEN: &str = "$serde_json::private::RawValue";

pub(crate) struct RawJson<'a>(pub(crate) Cow<'a, str>);

impl<'de> Deserialize<'de> for RawJson<'de> {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct RawVisitor;

        impl<'de> Visitor<'de> for RawVisitor {
            type Value = RawJson<'de>;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("raw JSON value")
            }

            fn visit_map<M: MapAccess<'de>>(self, mut map: M) -> Result<Self::Value, M::Error> {
                map.next_key_seed(RawKeyVisitor)?
                    .ok_or_else(|| M::Error::custom("missing raw JSON value"))?;
                map.next_value_seed(RawTextVisitor).map(RawJson)
            }
        }

        deserializer.deserialize_newtype_struct(RAW_VALUE_TOKEN, RawVisitor)
    }
}

// Match RawValue's string-only identifier contract; deriving a field identifier
// would also accept numeric variant indexes and byte strings.
struct RawKeyVisitor;

impl<'de> DeserializeSeed<'de> for RawKeyVisitor {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_identifier(self)
    }
}

impl<'de> Visitor<'de> for RawKeyVisitor {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("raw value")
    }

    fn visit_str<E: Error>(self, value: &str) -> Result<Self::Value, E> {
        if value == RAW_VALUE_TOKEN {
            Ok(())
        } else {
            Err(E::custom("unexpected raw value"))
        }
    }
}

struct RawTextVisitor;

impl<'de> DeserializeSeed<'de> for RawTextVisitor {
    type Value = Cow<'de, str>;

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl<'de> Visitor<'de> for RawTextVisitor {
    type Value = Cow<'de, str>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("raw JSON text")
    }

    fn visit_borrowed_str<E: Error>(self, value: &'de str) -> Result<Self::Value, E> {
        Ok(Cow::Borrowed(value))
    }

    fn visit_str<E: Error>(self, value: &str) -> Result<Self::Value, E> {
        Ok(Cow::Owned(value.to_owned()))
    }

    fn visit_string<E: Error>(self, value: String) -> Result<Self::Value, E> {
        Ok(Cow::Owned(value))
    }
}
