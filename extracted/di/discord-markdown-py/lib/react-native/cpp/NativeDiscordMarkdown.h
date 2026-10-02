#pragma once

#include <optional>
#include <string>

#include <RNDiscordMarkdownSpecJSI.h>

namespace facebook::react {

// A pure C++ TurboModule wrapping the Rust parser's C ABI. Registered on Android through
// autolinking (see `react-native.config.cjs`) and on iOS through the codegen
// `modulesProvider` (see `codegenConfig` in `package.json`).
class NativeDiscordMarkdown : public NativeDiscordMarkdownCxxSpec<NativeDiscordMarkdown> {
public:
	explicit NativeDiscordMarkdown(std::shared_ptr<CallInvoker> jsInvoker);

	// Parses markdown synchronously and returns the AST as a JSON string; throws a JS error
	// if the parser rejects the content. `allowedRules` is an optional JSON array of rule
	// names, matching the wasm binding. `fuel` optionally bounds how much work the parse may
	// do, defaulting to the parser's own budget; exhausting it throws like any other rejection.
	std::string parseToAstString(
		jsi::Runtime &rt,
		std::string content,
		std::optional<std::string> allowedRules,
		std::optional<double> fuel);

	// Turns a JSON AST back into the markdown it came from; throws a JS error if the AST is
	// malformed. Takes what `parseToAstString` produced, `$bigint` wrappers and all.
	std::string unparseFromAstString(jsi::Runtime &rt, std::string ast);
};

} // namespace facebook::react
