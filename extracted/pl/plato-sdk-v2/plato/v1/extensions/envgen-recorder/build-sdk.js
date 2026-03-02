const esbuild = require('esbuild');
const path = require('path');

esbuild.build({
  entryPoints: [path.resolve(__dirname, '../../javascript/src/plato/client.ts')],
  bundle: true,
  outfile: 'plato-sdk-bundle.js',
  format: 'iife',
  globalName: 'PlatoSDK',
  platform: 'browser',
  target: 'es2020',
  sourcemap: true,
  minify: false
}).then(() => console.log('✅ SDK bundled')).catch(err => {
  console.error('❌ Failed:', err);
  process.exit(1);
});
