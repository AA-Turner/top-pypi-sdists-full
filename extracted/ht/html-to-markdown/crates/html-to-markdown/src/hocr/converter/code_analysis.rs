//! Code block analysis and validation

use super::hierarchy::CodeLineInfo;
use super::keywords::{contains_keyword_token, is_shell_prompt, starts_with_keyword};

/// Check if a line looks like it's part of a bullet list
pub fn is_bullet_like(line: &str) -> bool {
    let trimmed = line.trim_start();
    if trimmed.is_empty() {
        return false;
    }

    if trimmed.starts_with("- ") || trimmed.starts_with("* ") || trimmed.starts_with("+ ") || trimmed.starts_with("•")
    {
        return true;
    }

    let mut chars = trimmed.chars().peekable();
    let mut digit_count = 0;
    while let Some(&ch) = chars.peek() {
        if ch.is_ascii_digit() {
            digit_count += 1;
            chars.next();
            continue;
        }
        break;
    }

    if digit_count > 0 {
        if let Some(&ch) = chars.peek() {
            if (ch == '.' || ch == ')') && chars.clone().nth(1).is_some_and(char::is_whitespace) {
                return true;
            }
        }
    }

    false
}

/// Determine if lines form a paragraph of code
pub fn is_code_paragraph(lines: &[CodeLineInfo]) -> bool {
    if lines.is_empty() {
        return false;
    }

    let mut strong_markers = 0;
    let mut moderate_markers = 0;
    let mut total = 0;

    for info in lines {
        let text = info.text.trim();
        if text.is_empty() {
            continue;
        }

        if is_bullet_like(&info.text) {
            return false;
        }

        total += 1;
        let lower = text.to_lowercase();
        let trimmed = text.trim_start();

        let documentation_tokens = [
            "definition",
            "theorem",
            "lemma",
            "proof",
            "corollary",
            "algorithm",
            "figure",
            "table",
            "appendix",
        ];
        if documentation_tokens
            .iter()
            .any(|token| contains_keyword_token(&lower, token))
        {
            return false;
        }

        let has_keyword = (starts_with_keyword(trimmed, "function") && text.contains('('))
            || (starts_with_keyword(trimmed, "return")
                && trimmed.chars().nth("return".len()).is_none_or(char::is_whitespace))
            || trimmed.starts_with("console.")
            || starts_with_keyword(trimmed, "async")
            || starts_with_keyword(trimmed, "await")
            || (starts_with_keyword(trimmed, "class") && (text.contains('{') || text.contains(':')))
            || (starts_with_keyword(trimmed, "struct") && text.contains('{'))
            || (starts_with_keyword(trimmed, "enum") && text.contains('{'))
            || (starts_with_keyword(trimmed, "def") && (text.contains('(') || text.contains(':')))
            || (starts_with_keyword(trimmed, "fn") && text.contains('('))
            || (starts_with_keyword(trimmed, "pub")
                && (text.contains("fn") || text.contains("struct") || text.contains("enum")))
            || starts_with_keyword(trimmed, "import")
            || starts_with_keyword(trimmed, "using")
            || starts_with_keyword(trimmed, "namespace")
            || starts_with_keyword(trimmed, "public")
            || starts_with_keyword(trimmed, "private")
            || starts_with_keyword(trimmed, "protected")
            || starts_with_keyword(trimmed, "static")
            || starts_with_keyword(trimmed, "void")
            || starts_with_keyword(trimmed, "try")
            || starts_with_keyword(trimmed, "catch")
            || starts_with_keyword(trimmed, "finally")
            || starts_with_keyword(trimmed, "throw")
            || starts_with_keyword(trimmed, "typedef")
            || starts_with_keyword(trimmed, "package")
            || starts_with_keyword(trimmed, "module");

        let has_symbol = text.contains(';') || text.contains("::");

        if has_keyword || has_symbol {
            strong_markers += 1;
            continue;
        }

        if is_shell_prompt(text) {
            strong_markers += 1;
            continue;
        }
        let has_assignment = text.contains(" = ")
            || text.contains("+=")
            || text.contains("-=")
            || text.contains("*=")
            || text.contains("/=")
            || text.contains(" := ")
            || text.contains(" == ");

        let has_arrow = text.contains("=>");
        let has_brace = text.contains('{') || text.contains('}');
        let has_pointer_arrow = text.contains("->");

        if has_assignment || has_arrow || has_brace || has_pointer_arrow {
            moderate_markers += 1;
        }
    }

    if total == 0 {
        return false;
    }
    if strong_markers == 0 {
        return false;
    }
    if strong_markers * 2 >= total {
        return true;
    }
    (strong_markers + moderate_markers) * 2 >= total
}

/// Check if code block is likely valid and not just prose
pub fn is_confident_code_block(lines: &[CodeLineInfo]) -> bool {
    let mut total = 0;
    let mut keyword_lines = 0;
    let mut punctuation_lines = 0;
    let mut assignment_lines = 0;
    let mut shell_lines = 0;
    let mut indent_lines = 0;

    let min_x = lines.iter().map(|info| info.x1).min().unwrap_or_default();

    for info in lines {
        let text = info.text.trim();
        if text.is_empty() {
            continue;
        }
        total += 1;

        if is_shell_prompt(text) {
            shell_lines += 1;
        }

        let trimmed = text.trim_start();

        if (starts_with_keyword(trimmed, "function") && text.contains('('))
            || trimmed.starts_with("console.")
            || (starts_with_keyword(trimmed, "return")
                && trimmed.chars().nth("return".len()).is_none_or(char::is_whitespace))
            || starts_with_keyword(trimmed, "async")
            || starts_with_keyword(trimmed, "await")
            || (starts_with_keyword(trimmed, "class") && (text.contains('{') || text.contains(':')))
            || (starts_with_keyword(trimmed, "struct") && text.contains('{'))
            || (starts_with_keyword(trimmed, "enum") && text.contains('{'))
            || (starts_with_keyword(trimmed, "def") && (text.contains('(') || text.contains(':')))
            || (starts_with_keyword(trimmed, "fn") && text.contains('('))
            || (starts_with_keyword(trimmed, "pub")
                && (text.contains("fn") || text.contains("struct") || text.contains("enum")))
            || starts_with_keyword(trimmed, "import")
            || starts_with_keyword(trimmed, "using")
            || starts_with_keyword(trimmed, "namespace")
            || starts_with_keyword(trimmed, "public")
            || starts_with_keyword(trimmed, "private")
            || starts_with_keyword(trimmed, "protected")
            || starts_with_keyword(trimmed, "static")
            || starts_with_keyword(trimmed, "void")
            || starts_with_keyword(trimmed, "try")
            || starts_with_keyword(trimmed, "catch")
            || starts_with_keyword(trimmed, "finally")
            || starts_with_keyword(trimmed, "throw")
            || starts_with_keyword(trimmed, "typedef")
            || starts_with_keyword(trimmed, "package")
            || starts_with_keyword(trimmed, "module")
        {
            keyword_lines += 1;
        }

        if text.contains(';')
            || text.contains('{')
            || text.contains('}')
            || text.contains("::")
            || text.contains("->")
            || text.contains("=>")
        {
            punctuation_lines += 1;
        }

        if text.contains(" = ")
            || text.contains("+=")
            || text.contains("-=")
            || text.contains("*=")
            || text.contains("/=")
            || text.contains(" := ")
            || text.contains(" == ")
        {
            assignment_lines += 1;
        }

        if info.x1 > min_x + 8 {
            indent_lines += 1;
        }
    }

    if total < 3 {
        return false;
    }

    if shell_lines >= 2 && shell_lines * 2 >= total {
        return true;
    }

    if keyword_lines >= 2 && assignment_lines >= 1 {
        return true;
    }

    if keyword_lines >= 1 && punctuation_lines >= 1 && assignment_lines >= 1 {
        return true;
    }

    if indent_lines == total && keyword_lines >= 1 && assignment_lines >= 1 {
        return true;
    }

    false
}
