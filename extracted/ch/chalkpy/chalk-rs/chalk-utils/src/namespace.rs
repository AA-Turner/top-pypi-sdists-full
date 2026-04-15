use regex::Regex;
use std::sync::LazyLock;

const NAMESPACE_SEP: &str = "::";
static SNAKE_SUB_1: LazyLock<Regex> =
    LazyLock::new(|| Regex::new("(.)([A-Z][a-z]+)").expect("valid regex"));
static SNAKE_SUB_2: LazyLock<Regex> =
    LazyLock::new(|| Regex::new("__([A-Z])").expect("valid regex"));
static SNAKE_SUB_3: LazyLock<Regex> =
    LazyLock::new(|| Regex::new("([a-z0-9])([A-Z])").expect("valid regex"));

/// Port of `chalk.utils.string.to_snake_case`.
pub fn to_snake_case(name: &str) -> String {
    let name = SNAKE_SUB_1.replace_all(name, "${1}_${2}");
    let name = SNAKE_SUB_2.replace_all(&name, "_${1}");
    let name = SNAKE_SUB_3.replace_all(&name, "${1}_${2}");
    name.to_lowercase()
}

/// Prepend namespace parts (normalized to snake_case), then `name`, joined by `::`.
pub fn build_namespaced_name(namespace: Option<&str>, name: Option<&str>) -> String {
    let namespace = namespace.unwrap_or("");
    let name = name.unwrap_or("");

    let mut parts: Vec<String> = namespace
        .split(NAMESPACE_SEP)
        .filter(|segment| !segment.is_empty())
        .map(to_snake_case)
        .collect();

    if !name.is_empty() {
        parts.push(name.to_string());
    }

    parts.join(NAMESPACE_SEP)
}

#[cfg(test)]
mod tests {
    use super::{build_namespaced_name, to_snake_case, NAMESPACE_SEP};

    #[test]
    fn to_snake_case_examples() {
        let cases = [
            ("", ""),
            ("user", "user"),
            ("User", "user"),
            ("myFeatureName", "my_feature_name"),
            ("BankAccount", "bank_account"),
            ("already_snake_case", "already_snake_case"),
            ("__PrivateField", "__private_field"),
            ("User2FA", "user2_fa"),
        ];

        for (input, expected) in cases {
            assert_eq!(to_snake_case(input), expected);
        }
    }

    #[test]
    fn to_snake_case_is_idempotent_and_ascii_lowercase() {
        let cases = [
            "",
            "user",
            "User",
            "myFeatureName",
            "BankAccount::OtherStuff",
            "__PrivateField",
            "User2FA",
            "ABC",
        ];

        for input in cases {
            let first = to_snake_case(input);
            let second = to_snake_case(&first);
            assert!(!first.chars().any(|c| c.is_ascii_uppercase()));
            assert_eq!(first, second);
        }
    }

    #[test]
    fn build_namespaced_name_examples() {
        let cases = [
            (
                Some("User"),
                Some("my_feature_name"),
                "user::my_feature_name",
            ),
            (
                Some("BankAccount::OtherStuff"),
                Some("account_balance"),
                "bank_account::other_stuff::account_balance",
            ),
            (Some(""), Some("my_feature"), "my_feature"),
            (Some("User::"), Some("feature"), "user::feature"),
            (
                Some("::User::Account"),
                Some("feature"),
                "user::account::feature",
            ),
            (None, Some("name"), "name"),
            (Some("User"), None, "user"),
            (None, None, ""),
            (Some(""), None, ""),
        ];

        for (namespace, name, expected) in cases {
            assert_eq!(build_namespaced_name(namespace, name), expected);
        }
    }

    #[test]
    fn build_namespaced_name_matches_expected_join_examples() {
        let cases = [
            ("", ""),
            ("User", ""),
            ("User::BankAccount", "feature_name"),
            ("::User::", "feature_name"),
            ("Team::SubTeam::Model", "my_feature"),
        ];

        for (namespace, name) in cases {
            let mut expected_parts: Vec<String> = namespace
                .split(NAMESPACE_SEP)
                .filter(|segment| !segment.is_empty())
                .map(to_snake_case)
                .collect();
            if !name.is_empty() {
                expected_parts.push(name.to_string());
            }
            let expected = expected_parts.join(NAMESPACE_SEP);
            assert_eq!(build_namespaced_name(Some(namespace), Some(name)), expected);
        }
    }

    #[test]
    fn build_namespaced_name_treats_none_as_empty_examples() {
        let cases = [
            ("", ""),
            ("User", ""),
            ("User::Account", "feature"),
            ("::User::", "feature_name"),
        ];

        for (namespace, name) in cases {
            assert_eq!(
                build_namespaced_name(None, Some(name)),
                build_namespaced_name(Some(""), Some(name))
            );
            assert_eq!(
                build_namespaced_name(Some(namespace), None),
                build_namespaced_name(Some(namespace), Some(""))
            );
        }
    }
}
