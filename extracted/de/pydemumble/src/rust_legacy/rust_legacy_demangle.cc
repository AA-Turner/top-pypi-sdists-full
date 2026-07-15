#include "rust_legacy_demangle.h"

#include <cctype>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <limits>
#include <string>
#include <string_view>
#include <vector>

static bool isHexDigit(char c) {
  return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f');
}

static bool isHexDigitCaseInsensitive(char c) {
  return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') ||
         (c >= 'A' && c <= 'F');
}

// Rust hashes are hex digits (either case, any length) with an 'h'
// prepended. See legacy.rs's is_rust_hash.
static bool isRustHash(std::string_view s) {
  if (s.empty() || s[0] != 'h')
    return false;
  for (size_t i = 1; i < s.size(); ++i)
    if (!isHexDigitCaseInsensitive(s[i]))
      return false;
  return true;
}

// Mirrors char::is_control(): C0 controls and DEL/C1 controls.
static bool isControlCodepoint(uint32_t cp) {
  return cp <= 0x1F || (cp >= 0x7F && cp <= 0x9F);
}

static void appendUtf8(std::string& out, uint32_t cp) {
  if (cp < 0x80) {
    out += static_cast<char>(cp);
  } else if (cp < 0x800) {
    out += static_cast<char>(0xC0 | (cp >> 6));
    out += static_cast<char>(0x80 | (cp & 0x3F));
  } else if (cp < 0x10000) {
    out += static_cast<char>(0xE0 | (cp >> 12));
    out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
    out += static_cast<char>(0x80 | (cp & 0x3F));
  } else {
    out += static_cast<char>(0xF0 | (cp >> 18));
    out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
    out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
    out += static_cast<char>(0x80 | (cp & 0x3F));
  }
}

struct DecodedSegment {
  std::string text;
  bool had_escape;
};

// Port of the per-element loop in legacy.rs's Display::fmt. An unrecognized
// or malformed escape stops de-escaping entirely and the remainder of the
// segment is copied verbatim, matching Rust's `break`-out-of-loop behavior.
static DecodedSegment decodeSegment(std::string_view seg) {
  std::string result;
  bool had_escape = false;

  std::string_view rest = seg;
  if (rest.size() >= 2 && rest[0] == '_' && rest[1] == '$')
    rest.remove_prefix(1);

  for (;;) {
    if (rest.empty())
      break;

    if (rest[0] == '.') {
      if (rest.size() >= 2 && rest[1] == '.') {
        result += "::";
        rest.remove_prefix(2);
      } else {
        result += '.';
        rest.remove_prefix(1);
      }
      continue;
    }

    if (rest[0] == '$') {
      size_t end = rest.find('$', 1);
      if (end == std::string_view::npos)
        break;
      std::string_view escape = rest.substr(1, end - 1);
      std::string_view after_escape = rest.substr(end + 1);

      const char* unescaped = nullptr;
      if (escape == "SP") unescaped = "@";
      else if (escape == "BP") unescaped = "*";
      else if (escape == "RF") unescaped = "&";
      else if (escape == "LT") unescaped = "<";
      else if (escape == "GT") unescaped = ">";
      else if (escape == "LP") unescaped = "(";
      else if (escape == "RP") unescaped = ")";
      else if (escape == "C") unescaped = ",";

      if (unescaped) {
        result += unescaped;
        rest = after_escape;
        had_escape = true;
        continue;
      }

      if (!escape.empty() && escape[0] == 'u') {
        std::string_view digits = escape.substr(1);
        bool all_lower_hex = !digits.empty();
        for (char c : digits) {
          if (!isHexDigit(c)) {
            all_lower_hex = false;
            break;
          }
        }
        if (all_lower_hex) {
          unsigned long cp =
              strtoul(std::string(digits).c_str(), nullptr, 16);
          bool valid_scalar =
              cp <= 0x10FFFF && !(cp >= 0xD800 && cp <= 0xDFFF);
          if (valid_scalar && !isControlCodepoint(static_cast<uint32_t>(cp))) {
            appendUtf8(result, static_cast<uint32_t>(cp));
            rest = after_escape;
            had_escape = true;
            continue;
          }
        }
      }

      // Unknown or malformed escape: stop de-escaping, keep raw remainder.
      break;
    }

    size_t i = rest.find_first_of("$.");
    if (i == std::string_view::npos) {
      result += rest;
      rest = std::string_view();
      break;
    }
    result += rest.substr(0, i);
    rest = rest.substr(i);
  }

  result += rest;
  return {std::move(result), had_escape};
}

char* rustLegacyDemangle(std::string_view s) {
  // Rust legacy mangled names start with "_ZN", "__ZN", or "ZN".
  if (s.size() >= 4 && s.substr(0, 4) == "__ZN") {
    s.remove_prefix(4);
  } else if (s.size() >= 3 && s.substr(0, 3) == "_ZN") {
    s.remove_prefix(3);
  } else if (s.size() >= 2 && s.substr(0, 2) == "ZN") {
    s.remove_prefix(2);
  } else {
    return nullptr;
  }

  // Check for non-ASCII characters, which are not valid in Rust legacy mangled names.
  for (size_t i = 0; i < s.size(); ++i) {
    if (static_cast<int>(s[i]) & 0x80) {
      return nullptr;
    }
  }

  std::vector<std::string_view> segments;
  size_t pos = 0;
  while (pos < s.size() && static_cast<unsigned char>(s[pos]) != 'E') {
    if (!std::isdigit(static_cast<unsigned char>(s[pos])))
      return nullptr;

    size_t len = 0;
    while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) {
      size_t d = static_cast<size_t>(s[pos] - '0');
      if (len > (std::numeric_limits<size_t>::max() - d) / 10)
        return nullptr;
      len = len * 10 + d;
      ++pos;
    }
    if (len > s.size() - pos)
      return nullptr;
    segments.push_back(s.substr(pos, len));
    pos += len;
  }

  if (segments.empty())
    return nullptr;

  std::vector<DecodedSegment> decoded;
  decoded.reserve(segments.size());
  bool has_escapes = false;
  for (const auto& seg : segments) {
    decoded.push_back(decodeSegment(seg));
    has_escapes = has_escapes || decoded.back().had_escape;
  }

  bool has_hash = isRustHash(segments.back());
  if (has_hash && segments.size() == 1)
    return nullptr;

  if (!has_hash && !has_escapes)
    return nullptr;

  std::string result;
  size_t end = has_hash ? segments.size() - 1 : segments.size();
  for (size_t i = 0; i < end; ++i) {
    if (i > 0)
      result += "::";
    result += decoded[i].text;
  }

  char* out = static_cast<char*>(std::malloc(result.size() + 1));
  if (!out)
    return nullptr;
  std::memcpy(out, result.data(), result.size());
  out[result.size()] = '\0';
  return out;
}
