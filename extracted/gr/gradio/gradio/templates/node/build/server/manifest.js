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
		client: {"start":"_app/immutable/entry/start.cqy29eLR.js","app":"_app/immutable/entry/app.kcIR80OZ.js","imports":["_app/immutable/entry/start.cqy29eLR.js","_app/immutable/chunks/client.DfhAhigx.js","_app/immutable/entry/app.kcIR80OZ.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-DP_4ZXSI.js')),
			__memo(() => import('./chunks/1-Co_9XrTq.js')),
			__memo(() => import('./chunks/2-Ds6SgjAN.js').then(function (n) { return n.aG; }))
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
