// Applies the saved theme before first paint. A one-to-one port of the pre-paint script
// next-themes 0.4.6 injects in server-rendered apps (`M` in dist/index.mjs), with the
// arguments its ThemeProvider passes for src/App.tsx: attribute "class", storageKey "theme",
// defaultTheme "system", no forcedTheme, themes ["light", "dark"], no value map,
// enableSystem and enableColorScheme. An external file, so a 'self' CSP allows it.
(function () {
	var root = document.documentElement;
	var colorSchemes = ["light", "dark"];
	var themes = ["light", "dark"];
	function apply(theme) {
		root.classList.remove.apply(root.classList, themes);
		root.classList.add(theme);
		if (colorSchemes.indexOf(theme) !== -1) root.style.colorScheme = theme;
	}
	function system() {
		return window.matchMedia("(prefers-color-scheme: dark)").matches
			? "dark"
			: "light";
	}
	try {
		var saved = localStorage.getItem("theme") || "system";
		apply(saved === "system" ? system() : saved);
	} catch {}
})();
