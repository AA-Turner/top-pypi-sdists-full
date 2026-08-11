"use strict";(self.rspackChunkjupyterlab_chat_extension=self.rspackChunkjupyterlab_chat_extension||[]).push([[232],{541(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n),p=o(5804),c=o(8028),l=o(436),s=o(7824),d=o(7611),u=i()(a());u.i(p.A),u.i(c.A),u.i(l.A),u.i(s.A),u.i(d.A),u.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/
`,""]),o.d(t,{},{A:u})},436(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n)()(a());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/* Chat search input in toolbar */
.jp-chat-search-input {
  padding: 4px 8px;
  border: 1px solid var(--jp-border-color1);
  border-radius: 3px;
  background: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  font-size: var(--jp-ui-font-size1);
  min-width: 150px;
  outline: none;
}

.jp-chat-search-input:focus {
  border-color: var(--jp-brand-color1);
  box-shadow: inset 0 0 0 1px var(--jp-brand-color1);
}

.jp-chat-search-input::placeholder {
  color: var(--jp-ui-font-color2);
}

/* Chat selector popup */
.jp-chat-selector-popup {
  background: var(--jp-layout-color1);
  border: 1px solid var(--jp-border-color1);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgb(0 0 0 / 15%);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 10;
  position: fixed;
  min-width: 150px;
  max-width: 300px;
  max-height: 400px;
}

/* Popup list container */
.jp-chat-selector-popup-list {
  list-style: none;
  margin: 0;
  padding: 4px 0;
  overflow-y: auto;
  max-height: 400px;
}

/* Popup list item */
.jp-chat-selector-popup-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.1s ease;
}

.jp-chat-selector-popup-item:hover {
  background: var(--jp-layout-color2);
}

.jp-chat-selector-popup-item-active {
  background: var(--jp-brand-color1);
  color: var(--jp-ui-inverse-font-color1);
}

.jp-chat-selector-popup-item-active:hover {
  background: var(--jp-brand-color1);
}

/* Item content layout */
.jp-chat-selector-popup-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  min-height: 32px;
}

.jp-chat-selector-popup-item-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

/* Item label (chat name) */
.jp-chat-selector-popup-item-label {
  font-size: var(--jp-ui-font-size1);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
}

.jp-chat-selector-popup-item-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
}

/* Cached indicator (bullet) */
.jp-chat-selector-popup-item-indicator {
  font-size: 8px;
  color: var(--jp-brand-color1);
  line-height: 1;
}

.jp-chat-selector-popup-item-active .jp-chat-selector-popup-item-indicator {
  color: var(--jp-layout-color3);
}

/* Close button */
.jp-chat-selector-popup-item-close:hover {
  background: var(--jp-layout-color3);
  color: var(--jp-ui-font-color0);
}

.jp-chat-selector-popup-item-active
  .jp-chat-selector-popup-item-close
  .jp-icon3[fill] {
  fill: var(--jp-layout-color3);
  opacity: 0.8;
}

.jp-chat-selector-popup-item-active .jp-chat-selector-popup-item-close:hover {
  background: rgb(0 0 0 / 20%);
  opacity: 1;
}

/* Empty state */
.jp-chat-selector-popup-empty {
  padding: 12px;
  text-align: center;
  color: var(--jp-ui-font-color2);
  font-style: italic;
  font-size: var(--jp-ui-font-size1);
}

/* Scrollbar styling for the list */
.jp-chat-selector-popup-list::-webkit-scrollbar {
  width: 8px;
}

.jp-chat-selector-popup-list::-webkit-scrollbar-track {
  background: var(--jp-layout-color1);
}

.jp-chat-selector-popup-list::-webkit-scrollbar-thumb {
  background: var(--jp-scrollbar-thumb-color);
  border-radius: 4px;
}

.jp-chat-selector-popup-list::-webkit-scrollbar-thumb:hover {
  background: var(--jp-scrollbar-thumb-hover-color);
}
`,""]),o.d(t,{},{A:i})},8028(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n)()(a());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

.jp-chat-SettingsHeader {
  font-size: var(--jp-ui-font-size3);
  font-weight: 400;
  color: var(--jp-ui-font-color1);
}
`,""]),o.d(t,{},{A:i})},5804(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n)()(a());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

.jp-chat-widget {
  min-height: 0;
  flex-grow: 1;
}

.jp-chat-message-container {
  position: relative;
}

.jp-chat-rendered-message hr {
  color: #00000026;
  background-color: transparent;
}

.jp-chat-message .jp-RenderedHTMLCommon > :last-child {
  margin-bottom: 0;
}

/*
 * Selectors must be nested in \`.jp-ThemedContainer\` to have a higher
 * specificity than selectors in rules provided by JupyterLab.
 *
 * See: https://jupyterlab.readthedocs.io/en/latest/extension/extension_migration.html#css-styling
 * See also: https://github.com/jupyterlab/jupyter-ai/issues/1090
 */
.jp-ThemedContainer .jp-chat-welcome-message {
  padding: 0 1em;
}

.jp-ThemedContainer .jp-chat-rendered-message .jp-RenderedHTMLCommon {
  padding-right: 0;
}

.jp-ThemedContainer .jp-chat-rendered-message .jp-RenderedJSON {
  padding-left: 5px;
}

.jp-ThemedContainer .jp-chat-rendered-message .jp-RenderedMarkdown pre,
.jp-ThemedContainer .jp-chat-welcome-message .jp-RenderedMarkdown pre {
  background-color: var(--jp-cell-editor-background);
  overflow-x: auto;
  white-space: pre;
  margin: 0;
  padding: 4px 6px;
  border: var(--jp-border-width) solid var(--jp-cell-editor-border-color);
}

.jp-ThemedContainer .jp-RenderedMarkdown pre > code {
  background-color: inherit;
  overflow-x: inherit;
  white-space: inherit;
}

.jp-ThemedContainer .jp-RenderedHTMLCommon mjx-container {
  font-size: 119%;
}

.jp-chat-toolbar {
  opacity: 0;
  transition: opacity 0.15s ease;
  position: absolute;
  right: 0;
  top: -20px;
  font-size: var(--jp-ui-font-size0);
  color: var(--jp-ui-font-color3);
  background-color: var(--jp-layout-color2);
  box-shadow: var(--jp-elevation-z2);
}

.jp-chat-toolbar:hover {
  cursor: pointer;
  color: var(--jp-ui-font-color2);
}

.jp-chat-message-container:hover .jp-chat-toolbar {
  opacity: 1;
}

.jp-chat-toolbar > .jp-ToolbarButtonComponent {
  margin-top: 0;
}

.jp-chat-navigation {
  position: absolute;
  right: 10px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  min-width: 0;
}

.jp-chat-navigation-unread {
  border: solid 2px var(--jp-cell-inprompt-font-color);
}

.jp-chat-navigation::part(control) {
  padding: 0;
}

.jp-chat-navigation-top {
  top: 10px;
}

.jp-chat-navigation-top svg {
  transform: rotate(180deg);
}

.jp-chat-navigation-bottom {
  bottom: 120px;
}

.jp-chat-mention {
  border-radius: 4px;
  padding: 2px 0;
  font-weight: bold;
}

.jp-chat-sidepanel .jp-chat-open {
  flex: 1 1 0%;
  min-width: 0;
  max-width: fit-content;
}

/* Sidepanel styles */
.jp-chat-sidepanel {
  display: flex;
  flex-direction: column;
}

.jp-chat-sidepanel .jp-chat-add svg path.jp-icon3 {
  stroke: var(--jp-inverse-layout-color3);
  stroke-width: 2;
}

.jp-chat-sidepanel-widget {
  min-height: 0;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.jp-chat-sidepanel-widget-toolbar > .jp-chat-sidepanel-widget-title {
  display: block;
  align-content: center;
  max-width: 16em;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-transform: uppercase;
  color: var(--jp-ui-font-color1);
  font-size: var(--jp-ui-font-size0);
  font-weight: bold;
}
`,""]),o.d(t,{},{A:i})},1304(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n),p=o(541),c=i()(a());c.i(p.A),c.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
`,""]),o.d(t,{},{A:c})},7824(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n)()(a());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/*
  * INPUT CONTAINER (component and toolbar)
  */
.jp-chat-input-container {
  position: relative;
  transition: all 150ms ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 0 0 auto;
}

.jp-chat-input-container.jp-chat-drag-hover::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgb(33 150 243 / 10%);
  border: 2px dashed var(--mui-palette-primary-main);
  border-radius: 4px;
  pointer-events: none;
  z-index: 1;
}

.jp-chat-input-container.jp-chat-drag-hover::before {
  content: 'Drop files or cells here';
  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--mui-palette-primary-main);
  font-size: 12px;
  font-weight: 500;
  pointer-events: none;
  background: var(--jp-layout-color0);
  padding: 2px 8px;
  border-radius: 3px;
  white-space: nowrap;
}

.jp-chat-input-toolbar .jp-chat-send-include-opener {
  padding: 4px 0;
}

.jp-chat-input-container:focus-within > div:first-of-type {
  border-color: var(--mui-palette-primary-main);
}
`,""]),o.d(t,{},{A:i})},7611(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n)()(a());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

.jp-chat-placeholder {
  text-align: center;
  color: var(--jp-content-font-color2);
}

.jp-chat-placeholder > h3 {
  margin-bottom: var(--jp-content-heading-margin-bottom);
}

.jp-chat-placeholder-chat-item {
  color: var(--jp-content-font-color1);
  background: none;
  border: none;
  padding: 2px 0;
  font: inherit;
  cursor: pointer;
  text-align: left;
  text-decoration: none;
}

.jp-chat-placeholder-chat-item:hover {
  text-decoration: underline;
  font-weight: bold;
}
`,""]),o.d(t,{},{A:i})},4296(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n),p=o(2385),c=i()(a());c.i(p.A),c.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/*
  See the JupyterLab Developer Guide for useful CSS Patterns:

  https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/
`,""]),o.d(t,{},{A:c})},6214(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n),p=o(1304),c=i()(a());c.i(p.A),c.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/*
  See the JupyterLab Developer Guide for useful CSS Patterns:

  https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/

.jp-lab-chat-main-panel
  .jp-ToolbarButtonComponent[data-command='jupyterlab-chat:moveChat']
  svg {
  transform: rotate(180deg);
}

.jp-lab-chat-title-unread .lm-TabBar-tabLabel::before {
  content: '* ';
}
`,""]),o.d(t,{},{A:c})},2385(e,t,o){var r=o(6758),a=o.n(r),n=o(935),i=o.n(n),p=o(6214),c=i()(a());c.i(p.A),c.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
`,""]),o.d(t,{},{A:c})},935(e){e.exports=function(e){var t=[];return t.toString=function(){return this.map(function(t){var o="",r=void 0!==t[5];return t[4]&&(o+="@supports (".concat(t[4],") {")),t[2]&&(o+="@media ".concat(t[2]," {")),r&&(o+="@layer".concat(t[5].length>0?" ".concat(t[5]):""," {")),o+=e(t),r&&(o+="}"),t[2]&&(o+="}"),t[4]&&(o+="}"),o}).join("")},t.i=function(e,o,r,a,n){"string"==typeof e&&(e=[[null,e,void 0]]);var i={};if(r)for(var p=0;p<this.length;p++){var c=this[p][0];null!=c&&(i[c]=!0)}for(var l=0;l<e.length;l++){var s=[].concat(e[l]);r&&i[s[0]]||(void 0!==n&&(void 0===s[5]||(s[1]="@layer".concat(s[5].length>0?" ".concat(s[5]):""," {").concat(s[1],"}")),s[5]=n),o&&(s[2]&&(s[1]="@media ".concat(s[2]," {").concat(s[1],"}")),s[2]=o),a&&(s[4]?(s[1]="@supports (".concat(s[4],") {").concat(s[1],"}"),s[4]=a):s[4]="".concat(a)),t.push(s))}},t}},6758(e){e.exports=function(e){return e[1]}},2591(e){var t=[];function o(e){for(var o=-1,r=0;r<t.length;r++)if(t[r].identifier===e){o=r;break}return o}function r(e,r){for(var a={},n=[],i=0;i<e.length;i++){var p=e[i],c=r.base?p[0]+r.base:p[0],l=a[c]||0,s="".concat(c," ").concat(l);a[c]=l+1;var d=o(s),u={css:p[1],media:p[2],sourceMap:p[3],supports:p[4],layer:p[5]};if(-1!==d)t[d].references++,t[d].updater(u);else{var h=function(e,t){var o=t.domAPI(t);return o.update(e),function(t){t?(t.css!==e.css||t.media!==e.media||t.sourceMap!==e.sourceMap||t.supports!==e.supports||t.layer!==e.layer)&&o.update(e=t):o.remove()}}(u,r);r.byIndex=i,t.splice(i,0,{identifier:s,updater:h,references:1})}n.push(s)}return n}e.exports=function(e,a){var n=r(e=e||[],a=a||{});return function(e){e=e||[];for(var i=0;i<n.length;i++){var p=o(n[i]);t[p].references--}for(var c=r(e,a),l=0;l<n.length;l++){var s=o(n[l]);0===t[s].references&&(t[s].updater(),t.splice(s,1))}n=c}}},8128(e){var t={};e.exports=function(e,o){var r=function(e){if(void 0===t[e]){var o=document.querySelector(e);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement)try{o=o.contentDocument.head}catch(e){o=null}t[e]=o}return t[e]}(e);if(!r)throw Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");r.appendChild(o)}},3051(e){e.exports=function(e){var t=document.createElement("style");return e.setAttributes(t,e.attributes),e.insert(t,e.options),t}},855(e,t,o){e.exports=function(e){var t=o.nc;t&&e.setAttribute("nonce",t)}},1740(e){e.exports=function(e){if("u"<typeof document)return{update:function(){},remove:function(){}};var t=e.insertStyleElement(e);return{update:function(o){var r,a,n;r="",o.supports&&(r+="@supports (".concat(o.supports,") {")),o.media&&(r+="@media ".concat(o.media," {")),(a=void 0!==o.layer)&&(r+="@layer".concat(o.layer.length>0?" ".concat(o.layer):""," {")),r+=o.css,a&&(r+="}"),o.media&&(r+="}"),o.supports&&(r+="}"),(n=o.sourceMap)&&"u">typeof btoa&&(r+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(n))))," */")),e.styleTagTransform(r,t,e.options)},remove:function(){var e;null===(e=t).parentNode||e.parentNode.removeChild(e)}}}},3656(e){e.exports=function(e,t){if(t.styleSheet)t.styleSheet.cssText=e;else{for(;t.firstChild;)t.removeChild(t.firstChild);t.appendChild(document.createTextNode(e))}}},8579(e,t,o){var r=o(2591),a=o.n(r),n=o(1740),i=o.n(n),p=o(8128),c=o.n(p),l=o(855),s=o.n(l),d=o(3051),u=o.n(d),h=o(3656),m=o.n(h),f=o(4296),v={};v.styleTagTransform=m(),v.setAttributes=s(),v.insert=c().bind(null,"head"),v.domAPI=i(),v.insertStyleElement=u(),a()(f.A,v),f.A&&f.A.locals&&f.A.locals}}]);