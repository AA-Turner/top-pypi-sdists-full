"use strict";(self.rspackChunkjupyterlab_nvdashboard=self.rspackChunkjupyterlab_nvdashboard||[]).push([[232],{8475(t,e,o){var r=o(1601),n=o.n(r),a=o(6314),i=o.n(a)()(n());i.push([t.id,`/*
 * SPDX-FileCopyrightText: Copyright (c) 2021-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 */

/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/

[data-jp-theme-light='true'] {
  --nv-custom-tick-color: #000;
  --nv-custom-chart-title-color: #000;
}

[data-jp-theme-light='false'] {
  --nv-custom-tick-color: #ff7900;
  --nv-custom-chart-title-color: #ff7900;
}

.gpu-dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: stretch; /* Stretch buttons across the div */
  padding: 10px;
  background-color: var(--jp-layout-color1);
  font-family: 'Courier New', Courier, monospace;
  word-spacing: 5px;
  font-variant: all-small-caps;
}

.gradient-background {
  background: linear-gradient(
    to bottom,
    var(--jp-layout-color0),
    var(--jp-layout-color1)
  );
  overflow-y: hidden;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  font-family: 'Courier New', Courier, monospace;
  word-spacing: 5px;
  font-variant: all-small-caps;
}

/* Time series charts need to have a min height for seekbar to be visible without scrolling*/
.size-constrained-widgets-lg {
  min-width: 25vw !important;
  min-height: 45vh !important;
}

/* default min size constraints for all widgets */
.size-constrained-widgets {
  min-width: 25vw !important;
  min-height: 25vh !important;
}

.gpu-dashboard-header {
  display: flex; /* Use flexbox layout */
  align-items: center; /* Align items vertically */
  justify-content: space-between; /* Space evenly between items */
  font-size: 25px; /* Adjust font size */
  font-weight: bold;
  margin-bottom: 10px;
  color: #ff7900;
}

.gpu-dashboard-footer {
  font-size: 18px;
  color: #ff7900;
  margin-top: 30px;
}

.gpu-dashboard-footer-body {
  font-variant: petite-caps;
}

.gpu-dashboard-divider {
  width: 100%;
  border: none;
  border-top: 1px solid #ff7900;
  margin: -8px -5px 10px 0;
}

.header-text {
  align-self: flex-start; /* Align text to the left */
}
.header-button {
  background: transparent;
}

.gpu-dashboard-button {
  margin: 5px 0;
  padding: 10px 20px;
  background: transparent;
  color: #ff7900;
  cursor: pointer;
  max-width: 250px;
  display: block !important;
  text-align: left; /* Left align button text */
  font-size: 16px;
  border: 2px solid #ff3e00a8; /* Green border */
  transition:
    border 0.3s,
    box-shadow 0.3s; /* Add a transition effect */
}

.gpu-dashboard-button:hover {
  border: 2px solid #ff3e00a8; /* Green border on hover */
  box-shadow: 0 0 5px 2px #ff7900; /* Reduced blur for the glowing effect on hover */
}

.nv-header-icon-text {
  font-family: 'Courier New', Courier, monospace;
  word-spacing: 5px;
  font-variant: all-small-caps;
  color: #ff7900;
  margin-right: 3px;
  font-size: 15px;
}

.nv-header-icon-text:hover {
  text-shadow:
    -0.25px 0 #ff7900,
    0 0.25px #ff7900,
    0.25px 0 #ff7900,
    0 -0.25px #ff7900;
}
.chart-title {
  padding-left: 62px;
  font-size: 22px;
  color: var(--nv-custom-chart-title-color);
}

.multi-chart-title {
  padding-left: 62px;
  font-size: 18px;
  color: var(--nv-custom-chart-title-color);
}

.custom-tooltip {
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color0);
  font-size: 18px;
  border: 1px solid var(--jp-border-color1);
  padding: 8px; /* Add padding as needed */
  text-align: center;
}

.tooltip-title {
  font-weight: bold;
  margin-bottom: 4px; /* Add margin as needed */
  color: var(--nv-custom-chart-title-color);
}

.lm-TabBar-tabIcon {
  padding-right: 5px;
  margin-top: 3px;
}

.hidden-brush-for-sync {
  display: none !important;
}

.gpu-dashboard-toolbar-button {
  height: 40px;
}

.nv-header-icon:hover {
  stroke: #ff7900;
}

.nv-header-icon svg path {
  fill: #ff7900 !important;
  font-size: 5px !important;
}

.nv-icon-custom {
  stroke: #ff7900;
  fill: #ff7900;
  height: 10px !important;
  width: 20px;
}

.nv-icon-custom-time-series {
  stroke: #ff7900;
  fill: #ff7900;
}

.nv-axis-custom text {
  font-size: 18px;
  fill: var(--nv-custom-tick-color);
}

.nv-custom-legend {
  font-size: 18px;
}

.recharts-legend-item {
  font-size: 17px;
}
`,""]),o.d(e,{},{A:i})},6314(t){t.exports=function(t){var e=[];return e.toString=function(){return this.map(function(e){var o="",r=void 0!==e[5];return e[4]&&(o+="@supports (".concat(e[4],") {")),e[2]&&(o+="@media ".concat(e[2]," {")),r&&(o+="@layer".concat(e[5].length>0?" ".concat(e[5]):""," {")),o+=t(e),r&&(o+="}"),e[2]&&(o+="}"),e[4]&&(o+="}"),o}).join("")},e.i=function(t,o,r,n,a){"string"==typeof t&&(t=[[null,t,void 0]]);var i={};if(r)for(var s=0;s<this.length;s++){var c=this[s][0];null!=c&&(i[c]=!0)}for(var l=0;l<t.length;l++){var p=[].concat(t[l]);r&&i[p[0]]||(void 0!==a&&(void 0===p[5]||(p[1]="@layer".concat(p[5].length>0?" ".concat(p[5]):""," {").concat(p[1],"}")),p[5]=a),o&&(p[2]&&(p[1]="@media ".concat(p[2]," {").concat(p[1],"}")),p[2]=o),n&&(p[4]?(p[1]="@supports (".concat(p[4],") {").concat(p[1],"}"),p[4]=n):p[4]="".concat(n)),e.push(p))}},e}},1601(t){t.exports=function(t){return t[1]}},5072(t){var e=[];function o(t){for(var o=-1,r=0;r<e.length;r++)if(e[r].identifier===t){o=r;break}return o}function r(t,r){for(var n={},a=[],i=0;i<t.length;i++){var s=t[i],c=r.base?s[0]+r.base:s[0],l=n[c]||0,p="".concat(c," ").concat(l);n[c]=l+1;var d=o(p),f={css:s[1],media:s[2],sourceMap:s[3],supports:s[4],layer:s[5]};if(-1!==d)e[d].references++,e[d].updater(f);else{var u=function(t,e){var o=e.domAPI(e);return o.update(t),function(e){e?(e.css!==t.css||e.media!==t.media||e.sourceMap!==t.sourceMap||e.supports!==t.supports||e.layer!==t.layer)&&o.update(t=e):o.remove()}}(f,r);r.byIndex=i,e.splice(i,0,{identifier:p,updater:u,references:1})}a.push(p)}return a}t.exports=function(t,n){var a=r(t=t||[],n=n||{});return function(t){t=t||[];for(var i=0;i<a.length;i++){var s=o(a[i]);e[s].references--}for(var c=r(t,n),l=0;l<a.length;l++){var p=o(a[l]);0===e[p].references&&(e[p].updater(),e.splice(p,1))}a=c}}},7659(t){var e={};t.exports=function(t,o){var r=function(t){if(void 0===e[t]){var o=document.querySelector(t);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement)try{o=o.contentDocument.head}catch(t){o=null}e[t]=o}return e[t]}(t);if(!r)throw Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");r.appendChild(o)}},540(t){t.exports=function(t){var e=document.createElement("style");return t.setAttributes(e,t.attributes),t.insert(e,t.options),e}},5056(t,e,o){t.exports=function(t){var e=o.nc;e&&t.setAttribute("nonce",e)}},7825(t){t.exports=function(t){if("u"<typeof document)return{update:function(){},remove:function(){}};var e=t.insertStyleElement(t);return{update:function(o){var r,n,a;r="",o.supports&&(r+="@supports (".concat(o.supports,") {")),o.media&&(r+="@media ".concat(o.media," {")),(n=void 0!==o.layer)&&(r+="@layer".concat(o.layer.length>0?" ".concat(o.layer):""," {")),r+=o.css,n&&(r+="}"),o.media&&(r+="}"),o.supports&&(r+="}"),(a=o.sourceMap)&&"u">typeof btoa&&(r+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")),t.styleTagTransform(r,e,t.options)},remove:function(){var t;null===(t=e).parentNode||t.parentNode.removeChild(t)}}}},1113(t){t.exports=function(t,e){if(e.styleSheet)e.styleSheet.cssText=t;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(t))}}},8579(t,e,o){var r=o(5072),n=o.n(r),a=o(7825),i=o.n(a),s=o(7659),c=o.n(s),l=o(5056),p=o.n(l),d=o(540),f=o.n(d),u=o(1113),h=o.n(u),m=o(8475),v={};v.styleTagTransform=h(),v.setAttributes=p(),v.insert=c().bind(null,"head"),v.domAPI=i(),v.insertStyleElement=f(),n()(m.A,v),m.A&&m.A.locals&&m.A.locals}}]);