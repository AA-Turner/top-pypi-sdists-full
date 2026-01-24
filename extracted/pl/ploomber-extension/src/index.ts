import { plugin_settings } from './settings/index';
import { plugin_sharing } from './deploy-notebook/index';
export * from './version';
export default [
  plugin_settings,
  plugin_sharing
];
