// C header for the Rust parser's C ABI. Must match `ffi/c/src/lib.rs`.
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Result of `dmd_parse` or `dmd_unparse`. Must be freed with `dmd_parse_result_free`.
typedef struct DmdParseResult {
	// UTF-8 bytes of the call's output when `ok` -- the JSON AST for `dmd_parse`, the markdown
	// for `dmd_unparse` -- or of an error message otherwise. Not NUL-terminated, and never null.
	uint8_t *data;
	// Length of `data` in bytes.
	size_t len;
	// Whether parsing succeeded.
	bool ok;
} DmdParseResult;

// The `fuel` argument to `dmd_parse` that selects the parser's own default budget. Zero is the
// sentinel because a C caller cannot spell "absent" and a budget of zero is not a request anyone
// can mean — it fails every parse that reaches the inline parser. Pass 1 for the smallest real
// budget.
#define DMD_FUEL_DEFAULT 0u

// Parses `content` (UTF-8, `content_len` bytes) into a JSON AST. `allowed_rules` is either
// null (all rules) or a JSON array of rule names (UTF-8, `allowed_rules_len` bytes).
//
// `fuel` bounds how much work the parse may do before it gives up; pass `DMD_FUEL_DEFAULT` for
// the parser's own budget. Running out is an ordinary failed result — `ok` is false and `data`
// is `parser ran out of fuel` — not a crash.
DmdParseResult dmd_parse(const uint8_t *content, size_t content_len,
	const uint8_t *allowed_rules, size_t allowed_rules_len, uint32_t fuel);

// Turns a JSON AST (UTF-8, `ast_len` bytes) back into the markdown it came from. Takes what
// `dmd_parse` produced, `{"$bigint": "<value>"}` wrappers and all.
//
// The AST does not retain every detail of how the source was written, so the output is not
// byte-exact for everything: text is not re-escaped, italics always come back as `_`, and
// unordered lists always as `* `. A malformed AST is an ordinary failed result, not a crash.
DmdParseResult dmd_unparse(const uint8_t *ast, size_t ast_len);

// Frees a result returned by `dmd_parse` or `dmd_unparse`.
void dmd_parse_result_free(DmdParseResult result);

#ifdef __cplusplus
}
#endif
