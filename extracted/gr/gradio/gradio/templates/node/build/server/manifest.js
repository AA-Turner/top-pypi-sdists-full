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
		client: {start:"_app/immutable/entry/start.DE6SIXo2.js",app:"_app/immutable/entry/app.CT4O_2Tu.js",imports:["_app/immutable/entry/start.DE6SIXo2.js","_app/immutable/chunks/whcNsXsi.js","_app/immutable/chunks/WS1bLMZz.js","_app/immutable/chunks/Cjcla-Y4.js","_app/immutable/entry/app.CT4O_2Tu.js","_app/immutable/chunks/WS1bLMZz.js","_app/immutable/chunks/Cjcla-Y4.js","_app/immutable/chunks/Bocc91eC.js","_app/immutable/chunks/C5-g0Q-M.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./chunks/0-ZYXl7Q_S.js')),
			__memo(() => import('./chunks/1-DY5DnOiq.js')),
			__memo(() => import('./chunks/2-CZxR0mQq.js').then(function (n) { return n.a3; }))
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
