/// Sanitizes SDK keys embedded in strings by masking characters after `secret-`.
/// Keeps the first 5 chars of the key and replaces the rest with `*****`.
/// Use this for ANY log output that may include URLs or messages containing SDK keys.
pub fn sanitize_secret_key(input: &str) -> String {
    input
        .split("secret-")
        .enumerate()
        .map(|(i, part)| {
            if i == 0 {
                part.to_string()
            } else {
                let key_end = part
                    .find(|c: char| !c.is_alphanumeric())
                    .unwrap_or(part.len());
                let (key, rest) = part.split_at(key_end);
                let prefix_end = key
                    .char_indices()
                    .nth(5)
                    .map_or(key.len(), |(index, _)| index);
                format!("secret-{}*****{rest}", &key[..prefix_end])
            }
        })
        .collect()
}
