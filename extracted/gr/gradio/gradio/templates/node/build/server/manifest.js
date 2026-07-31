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
		client: {start:"_app/immutable/entry/start.xlU_3S59.js",app:"_app/immutable/entry/app.DB6ygZEU.js",imports:["_app/immutable/entry/start.xlU_3S59.js","_app/immutable/chunks/D56IA9WF.js","_app/immutable/chunks/CS1Us75e.js","_app/immutable/chunks/6td1SFyl.js","_app/immutable/entry/app.DB6ygZEU.js","_app/immutable/chunks/CS1Us75e.js","_app/immutable/chunks/6td1SFyl.js","_app/immutable/chunks/BNrXEQcG.js","_app/immutable/chunks/VdUQV0jB.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-B1ZV6NbM.js')),
			__memo(() => import('./chunks/1-BI1aOweC.js')),
			__memo(() => import('./chunks/2-D5Dc1Jtq.js').then(function (n) { return n.$; }))
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
