import type { TurboModule } from "react-native";
import { TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
	parseToAstString(content: string, flags?: number, fuel?: number): string;
	parseLosslessToAstString(
		content: string,
		flags?: number,
		fuel?: number,
	): string;
	unparseFromAstString(ast: string): string;
}

export default TurboModuleRegistry.getEnforcing<Spec>("DiscordMarkdown");
