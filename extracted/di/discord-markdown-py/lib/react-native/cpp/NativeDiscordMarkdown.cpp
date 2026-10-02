#include "NativeDiscordMarkdown.h"

#include <cmath>
#include <cstdint>
#include <optional>
#include <utility>

#include "discord_markdown_c.h"

namespace facebook::react {

namespace {

// Owns a `DmdParseResult` -- from either C-ABI call -- for the duration of a call.
class ParseResult {
public:
	explicit ParseResult(DmdParseResult result) : result_(result) {}
	~ParseResult() { dmd_parse_result_free(result_); }
	ParseResult(const ParseResult &) = delete;
	ParseResult &operator=(const ParseResult &) = delete;

	bool ok() const { return result_.ok; }
	std::string str() const {
		return std::string(reinterpret_cast<const char *>(result_.data), result_.len);
	}

private:
	DmdParseResult result_;
};

// Converts the JS number from the spec into the C ABI's fuel argument.
//
// JS numbers are doubles, so a request can arrive fractional, out of range, negative, or NaN.
// An absent or NaN budget takes the parser's default; anything else is clamped into range, with
// zero and negatives becoming 1 so that asking for "no budget" reads as the smallest real budget
// rather than tripping the default sentinel.
uint32_t toFuel(std::optional<double> fuel) {
	if (!fuel || std::isnan(*fuel)) {
		return DMD_FUEL_DEFAULT;
	}
	if (*fuel <= 1.0) {
		return 1;
	}
	if (*fuel >= static_cast<double>(UINT32_MAX)) {
		return UINT32_MAX;
	}
	return static_cast<uint32_t>(*fuel);
}

} // namespace

NativeDiscordMarkdown::NativeDiscordMarkdown(std::shared_ptr<CallInvoker> jsInvoker)
	: NativeDiscordMarkdownCxxSpec(std::move(jsInvoker)) {}

std::string NativeDiscordMarkdown::parseToAstString(
	jsi::Runtime &rt,
	std::string content,
	std::optional<std::string> allowedRules,
	std::optional<double> fuel) {
	const ParseResult result(dmd_parse(
		reinterpret_cast<const uint8_t *>(content.data()), content.size(),
		allowedRules ? reinterpret_cast<const uint8_t *>(allowedRules->data()) : nullptr,
		allowedRules ? allowedRules->size() : 0, toFuel(fuel)));

	if (!result.ok()) {
		throw jsi::JSError(rt, result.str());
	}
	return result.str();
}

std::string NativeDiscordMarkdown::unparseFromAstString(jsi::Runtime &rt, std::string ast) {
	const ParseResult result(
		dmd_unparse(reinterpret_cast<const uint8_t *>(ast.data()), ast.size()));

	if (!result.ok()) {
		throw jsi::JSError(rt, result.str());
	}
	return result.str();
}

} // namespace facebook::react
