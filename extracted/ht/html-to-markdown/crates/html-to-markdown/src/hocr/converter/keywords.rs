//! Keyword and language detection for code block identification

/// Detect if a text line appears to be shell command prompt
pub fn is_shell_prompt(text: &str) -> bool {
    let trimmed = text.trim_start();
    if trimmed.is_empty() {
        return false;
    }

    trimmed.starts_with('$')
        || trimmed.starts_with('#')
        || trimmed.contains("]#")
        || trimmed.starts_with("sudo ")
        || trimmed.starts_with("./")
        || trimmed.starts_with("python ")
        || trimmed.starts_with("pip ")
        || trimmed.starts_with("uv ")
}

/// Check if a keyword appears at the start with proper word boundaries
pub fn starts_with_keyword(trimmed: &str, keyword: &str) -> bool {
    if !trimmed.starts_with(keyword) {
        return false;
    }
    if let Some(first) = trimmed.chars().next() {
        if !first.is_ascii_lowercase() {
            return false;
        }
    }
    match trimmed.chars().nth(keyword.len()) {
        None => true,
        Some(ch) => ch.is_whitespace() || matches!(ch, '(' | ':' | '{' | '[' | '.'),
    }
}

/// Check if a keyword token appears anywhere in text
pub fn contains_keyword_token(text: &str, keyword: &str) -> bool {
    text.split(|ch: char| !(ch.is_ascii_alphanumeric() || ch == '_'))
        .any(|token| token == keyword)
}

/// Detect programming language based on code patterns
pub fn detect_code_language(lines: &[String]) -> Option<&'static str> {
    let lower_lines: Vec<String> = lines.iter().map(|line| line.to_lowercase()).collect();
    if lower_lines.iter().any(|line| line.contains("function"))
        || lower_lines.iter().any(|line| line.contains("console."))
        || lower_lines.iter().any(|line| line.contains("const "))
    {
        return Some("javascript");
    }
    if lower_lines.iter().any(|line| line.contains("printf")) {
        return Some("c");
    }
    None
}
