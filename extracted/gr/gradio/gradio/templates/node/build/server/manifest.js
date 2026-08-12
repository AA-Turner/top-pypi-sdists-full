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
		client: {start:"_app/immutable/entry/start.awSncZ7L.js",app:"_app/immutable/entry/app.DgvmMzAu.js",imports:["_app/immutable/entry/start.awSncZ7L.js","_app/immutable/chunks/CuYodknk.js","_app/immutable/chunks/C0NAgWyT.js","_app/immutable/chunks/CYcOlznv.js","_app/immutable/entry/app.DgvmMzAu.js","_app/immutable/chunks/C0NAgWyT.js","_app/immutable/chunks/CYcOlznv.js","_app/immutable/chunks/DjaDRR0M.js","_app/immutable/chunks/Bq9Tj-av.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-Cz2w3y_5.js')),
			__memo(() => import('./chunks/1-DRSEpS4d.js')),
			__memo(() => import('./chunks/2-CeB9nkXm.js').then(function (n) { return n.$; }))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/([^]*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
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
