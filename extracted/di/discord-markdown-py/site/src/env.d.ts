/// <reference types="@rsbuild/core/types" />

interface Window {
	/** Where @grafana/ui looks for its icon assets. See `GRAFANA_PUBLIC_PATH` in `index.tsx`. */
	__grafana_public_path__?: string;
}
