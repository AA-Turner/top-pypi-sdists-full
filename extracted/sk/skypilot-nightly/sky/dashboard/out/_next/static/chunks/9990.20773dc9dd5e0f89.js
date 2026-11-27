"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9990],{27325:function(e,t,n){n.d(t,{Z:function(){return a}});/**
 * @license lucide-react v0.407.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let a=(0,n(60998).Z)("Copy",[["rect",{width:"14",height:"14",x:"8",y:"8",rx:"2",ry:"2",key:"17jyea"}],["path",{d:"M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2",key:"zix9uf"}]])},33441:function(e,t,n){n.d(t,{Z:function(){return a}});/**
 * @license lucide-react v0.407.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let a=(0,n(60998).Z)("Info",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 16v-4",key:"1dtifu"}],["path",{d:"M12 8h.01",key:"e9boi3"}]])},88507:function(e,t,n){n.d(t,{Z:function(){return a}});/**
 * @license lucide-react v0.407.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let a=(0,n(60998).Z)("MessageSquare",[["path",{d:"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z",key:"1lielz"}]])},13626:function(e,t,n){n.d(t,{Z:function(){return a}});/**
 * @license lucide-react v0.407.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let a=(0,n(60998).Z)("RotateCw",[["path",{d:"M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8",key:"1p45f6"}],["path",{d:"M21 3v5h-5",key:"1q7to0"}]])},28586:function(e,t,n){n.d(t,{Z:function(){return a}});/**
 * @license lucide-react v0.407.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let a=(0,n(60998).Z)("Users",[["path",{d:"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2",key:"1yyitq"}],["circle",{cx:"9",cy:"7",r:"4",key:"nufk8"}],["path",{d:"M22 21v-2a4 4 0 0 0-3-3.87",key:"kshegd"}],["path",{d:"M16 3.13a4 4 0 0 1 0 7.75",key:"1da9ce"}]])},51564:function(e,t,n){n.d(t,{CV:function(){return l},IM:function(){return h},Xe:function(){return k},iY:function(){return y},pi:function(){return f},rA:function(){return s}});var a=n(67294),r=n(6378),c=n(51214),i=n(17324),u=n(32045);let o="default",d=/^[a-z]([-_a-z0-9]*[a-z0-9])?$/;function l(e,t){var n;return t&&t!==o?(null==e?void 0:null===(n=e[t])||void 0===n?void 0:n.name)||t:t||o}function s(e){return e?e.length>63?"Name must be at most ".concat(63," characters."):d.test(e)?null:"Use lowercase letters, numbers, dashes and underscores; start with a letter and end with a letter or number.":"Name is required."}function f(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,a=Object.keys(e||{}).filter(e=>e!==n),r=a.find(n=>l(e,n)===t);return void 0!==r?{id:r,byId:!1}:a.includes(t)?{id:t,byId:!0}:null}function h(e,t,n){return n.byId?'"'.concat(t,'" is the id of workspace "').concat(l(e,n.id),'".'):'Workspace "'.concat(t,'" already exists.')}function k(){let[e,t]=(0,a.useState)(()=>{let e=r.ZP.getCached(i.getWorkspaces);return{config:e||{},loaded:null!=e}}),{config:n,loaded:u}=e;return(0,a.useEffect)(()=>{let e=!1;r.ZP.get(i.getWorkspaces).then(n=>{e||t({config:n||{},loaded:!0})}).catch(()=>{e||t(e=>({...e,loaded:!0}))});let n=setInterval(()=>{let e=r.ZP.getCached(i.getWorkspaces);e&&t(t=>t.config===e?t:{config:e,loaded:!0})},c.nb.REFRESH_INTERVAL);return()=>{e=!0,clearInterval(n)}},[]),{workspacesConfig:n,isWorkspaceWritable:e=>{var t;return!!u&&(null===(t=n[e||o])||void 0===t?void 0:t.writable)!==!1},workspaceName:e=>l(n,e),loaded:u}}function y(){r.ZP.invalidate(i.getWorkspaces),r.ZP.invalidateFunction(i.getEnabledCloudsBatch),r.ZP.invalidate(u.CI),r.ZP.invalidate(u.Xg)}}}]);