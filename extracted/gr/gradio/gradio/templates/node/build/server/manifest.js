const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.CuVjEoEH.js","app":"_app/immutable/entry/app.DxX1j3jX.js","imports":["_app/immutable/entry/start.CuVjEoEH.js","_app/immutable/chunks/client.d4j4BO8F.js","_app/immutable/entry/app.DxX1j3jX.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-g7RWuaTC.js')),
			__memo(() => import('./chunks/1-Dfla5SOd.js')),
			__memo(() => import('./chunks/2-B27tEoSH.js').then(function (n) { return n.aF; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
