"use strict";(self.rspackChunk_jupyterlab_git=self.rspackChunk_jupyterlab_git||[]).push([[232],{90(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n)()(i());a.push([e.id,`.jp-remote-text {
  font-size: 1rem;
}

.jp-remote-options-wrapper {
  margin: 4px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  row-gap: 5px;
}

.jp-button-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.jp-option {
  height: fit-content !important;
  appearance: auto !important;
  margin: 0;
}

.jp-force-box-container {
  margin-top: 1rem;
  display: flex;
  align-items: flex-end;
  column-gap: 5px;
}
`,""]),o.d(r,{},{A:a})},8475(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n),p=o(9065),d=o(2372),c=o(3767),l=o(7057),s=o(90),f=a()(i());f.i(p.A),f.i(d.A),f.i(c.A),f.i(l.A),f.i(s.A),f.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

.jp-git-tab-mod-preview {
  font-style: italic;
}

.not-saved > .lm-TabBar-tabCloseIcon > :not(:hover) > .jp-icon-busy[fill] {
  fill: var(--jp-inverse-layout-color3);
}

.not-saved > .lm-TabBar-tabCloseIcon > :not(:hover) > .jp-icon3[fill] {
  fill: none;
}
`,""]),o.d(r,{},{A:f})},2372(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n)()(i());a.push([e.id,`.jp-CredentialsBox input[type='text'],
.jp-CredentialsBox input[type='password'] {
  display: block;
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
}

.jp-CredentialsBox input[type='checkbox'] {
  display: inline-block;
}

.jp-CredentialsBox-warning {
  color: var(--jp-warn-color0);
}

.jp-CredentialsBox-label-checkbox {
  display: flex;
  align-items: center;
}

.jp-CredentialsBox-wrapper {
  margin-top: 10px;
}
`,""]),o.d(r,{},{A:a})},3767(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n)()(i());a.push([e.id,`.jp-git-diff-error {
  width: auto;
  padding: 16px;
  color: var(--jp-ui-font-color1);
  font-size: var(--jp-ui-font-size1);
  background: var(--jp-error-color3);
}

.jp-git-diff-error-message {
  color: var(--jp-error-color1);
  margin-left: 5px;
}

.jp-git-diff-root {
  min-width: 2px;
  min-height: 30px;
  height: 100%;
  display: flex;
  flex-direction: column;
  outline: none;
  background: var(--jp-layout-color0);
  color: var(--jp-ui-font-color0);
  padding: 0;
}

.jp-git-diff-root .cm-editor {
  height: 100%;
}

button.jp-git-diff-refresh {
  border: solid 1px var(--jp-warn-color2);
}

button.jp-git-diff-resolve {
  border: solid 1px var(--jp-success-color2);
}

button.jp-git-diff-refresh .jp-ToolbarButtonComponent-label {
  color: var(--jp-warn-color1);
}

button.jp-git-diff-resolve .jp-ToolbarButtonComponent-label {
  color: var(--jp-success-color1);
}

.jp-git-diff-banner,
.jp-git-merge-banner {
  flex: 0 0 auto;
  margin: 2px 0;
  display: grid;
  grid-auto-rows: minmax(18px, auto);
  width: 100%;
}

.jp-git-diff-banner {
  grid-template-columns: 47% 6% 47%;
}

.jp-git-diff-banner span {
  padding: 0 4px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
}

.jp-git-merge-banner span {
  padding: 0 4px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
}

.jp-git-diff-banner span:first-child {
  grid-column: 1;
}

.jp-git-diff-banner span:last-child {
  grid-column: 3;
}

.jp-git-diff-banner span:first-of-type {
  background-color: var(--jp-git-diff-deleted-color1);
}

.jp-git-diff-banner span:last-of-type {
  background-color: var(--jp-git-diff-added-color1);
}

.jp-git-merge-banner {
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.jp-git-merge-banner span:first-of-type {
  background-color: var(--jp-merge-local-color1);
}

.jp-git-merge-banner span:last-of-type {
  background-color: var(--jp-git-diff-added-color1);
}

.jp-git-diff-root .cm-merge {
  position: relative;
  white-space: pre;
  border: var(--codemirror-border);
  border-radius: 0;
  background: var(--jp-cell-editor-background);
}

.jp-git-diff-root .cm {
  background: var(--jp-layout-color0);
}

.jp-git-diff-root .cm-merge,
.cm-merge .cm {
  height: auto;
}

.jp-git-diff-root .cm-merge-4pane .cm-merge-pane-deleted {
  display: none;
}

.jp-git-diff-root .cm-merge-pane-unchanged {
  width: 100%;
}

.jp-git-diff-root .cm-merge-pane {
  display: inline-block;
  white-space: normal;
  vertical-align: top;
}

.jp-git-diff-root .cm-merge-pane-rightmost {
  position: absolute;
  right: 0;
  z-index: 1;
}

.jp-Notebook-merge .jp-Merge-conflict {
  background-color: var(--jp-merge-both-color2);
}

.jp-git-diff-root .cm-merge-r-deleted,
.jp-git-diff-root .cm-merge-l-deleted,
.jp-git-diff-root .cm-diff-left-editor .cm-merge-r-chunk {
  background-color: var(--jp-git-diff-deleted-color);
}

.jp-git-diff-root
  .cm-merge-left-editor
  .cm-merge-l-chunk:not(.jp-Merge-conflict) {
  background-color: var(--jp-merge-local-color);
}

.jp-git-diff-root .cm-merge-r-inserted,
.jp-git-diff-root .cm-merge-l-inserted,
.jp-git-diff-root .cm-diff-right-editor .cm-merge-r-chunk,
.jp-git-diff-root .cm-merge-right-editor .cm-merge-r-chunk {
  background-color: var(--jp-git-diff-added-color);
}

.jp-git-diff-root .cm-merge-left-editor .cm-merge-l-inserted {
  background-color: var(--jp-merge-local-color1);
}

.jp-git-diff-root .cm-merge-spacer {
  background-image: repeating-linear-gradient(
    145deg,
    transparent,
    transparent 10px,
    var(--jp-border-color0) 10px,
    var(--jp-border-color0) 12px
  );
}

/* Hide drag handles */
.jp-git-diff-root .jp-Notebook-merge .jp-DragPanel-dragHandle {
  display: none;
}

.jp-git-diff-parent-widget .jp-Merge-notebook-controls {
  margin-bottom: 0;
  padding: 0;
  background-color: transparent;
  border: none;
}
`,""]),o.d(r,{},{A:a})},7057(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n)()(i());a.push([e.id,`.jp-git-StatusWidget {
  display: flex;
  align-items: center;
}
`,""]),o.d(r,{},{A:a})},9065(e,r,o){var t=o(1601),i=o.n(t),n=o(6314),a=o.n(n)()(i());a.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

:root {
  --jp-git-diff-added-color: rgb(155 185 85 / 20%);
  --jp-git-diff-added-color1: rgb(155 185 85 / 40%);
  --jp-git-diff-deleted-color: rgb(255 0 0 / 20%);
  --jp-git-diff-deleted-color1: rgb(255 0 0 / 40%);
  --jp-git-diff-output-border-color: rgb(0 141 255 / 70%);
  --jp-git-diff-output-color: rgb(0 141 255 / 30%);
  --jp-merge-local-color: rgb(31 31 224 / 20%);
  --jp-merge-local-color1: rgb(31 31 224 / 40%);
}
`,""]),o.d(r,{},{A:a})},6314(e){e.exports=function(e){var r=[];return r.toString=function(){return this.map(function(r){var o="",t=void 0!==r[5];return r[4]&&(o+="@supports (".concat(r[4],") {")),r[2]&&(o+="@media ".concat(r[2]," {")),t&&(o+="@layer".concat(r[5].length>0?" ".concat(r[5]):""," {")),o+=e(r),t&&(o+="}"),r[2]&&(o+="}"),r[4]&&(o+="}"),o}).join("")},r.i=function(e,o,t,i,n){"string"==typeof e&&(e=[[null,e,void 0]]);var a={};if(t)for(var p=0;p<this.length;p++){var d=this[p][0];null!=d&&(a[d]=!0)}for(var c=0;c<e.length;c++){var l=[].concat(e[c]);t&&a[l[0]]||(void 0!==n&&(void 0===l[5]||(l[1]="@layer".concat(l[5].length>0?" ".concat(l[5]):""," {").concat(l[1],"}")),l[5]=n),o&&(l[2]&&(l[1]="@media ".concat(l[2]," {").concat(l[1],"}")),l[2]=o),i&&(l[4]?(l[1]="@supports (".concat(l[4],") {").concat(l[1],"}"),l[4]=i):l[4]="".concat(i)),r.push(l))}},r}},1601(e){e.exports=function(e){return e[1]}},5072(e){var r=[];function o(e){for(var o=-1,t=0;t<r.length;t++)if(r[t].identifier===e){o=t;break}return o}function t(e,t){for(var i={},n=[],a=0;a<e.length;a++){var p=e[a],d=t.base?p[0]+t.base:p[0],c=i[d]||0,l="".concat(d," ").concat(c);i[d]=c+1;var s=o(l),f={css:p[1],media:p[2],sourceMap:p[3],supports:p[4],layer:p[5]};if(-1!==s)r[s].references++,r[s].updater(f);else{var g=function(e,r){var o=r.domAPI(r);return o.update(e),function(r){r?(r.css!==e.css||r.media!==e.media||r.sourceMap!==e.sourceMap||r.supports!==e.supports||r.layer!==e.layer)&&o.update(e=r):o.remove()}}(f,t);t.byIndex=a,r.splice(a,0,{identifier:l,updater:g,references:1})}n.push(l)}return n}e.exports=function(e,i){var n=t(e=e||[],i=i||{});return function(e){e=e||[];for(var a=0;a<n.length;a++){var p=o(n[a]);r[p].references--}for(var d=t(e,i),c=0;c<n.length;c++){var l=o(n[c]);0===r[l].references&&(r[l].updater(),r.splice(l,1))}n=d}}},7659(e){var r={};e.exports=function(e,o){var t=function(e){if(void 0===r[e]){var o=document.querySelector(e);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement)try{o=o.contentDocument.head}catch(e){o=null}r[e]=o}return r[e]}(e);if(!t)throw Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");t.appendChild(o)}},540(e){e.exports=function(e){var r=document.createElement("style");return e.setAttributes(r,e.attributes),e.insert(r,e.options),r}},5056(e,r,o){e.exports=function(e){var r=o.nc;r&&e.setAttribute("nonce",r)}},7825(e){e.exports=function(e){if("u"<typeof document)return{update:function(){},remove:function(){}};var r=e.insertStyleElement(e);return{update:function(o){var t,i,n;t="",o.supports&&(t+="@supports (".concat(o.supports,") {")),o.media&&(t+="@media ".concat(o.media," {")),(i=void 0!==o.layer)&&(t+="@layer".concat(o.layer.length>0?" ".concat(o.layer):""," {")),t+=o.css,i&&(t+="}"),o.media&&(t+="}"),o.supports&&(t+="}"),(n=o.sourceMap)&&"u">typeof btoa&&(t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(n))))," */")),e.styleTagTransform(t,r,e.options)},remove:function(){var e;null===(e=r).parentNode||e.parentNode.removeChild(e)}}}},1113(e){e.exports=function(e,r){if(r.styleSheet)r.styleSheet.cssText=e;else{for(;r.firstChild;)r.removeChild(r.firstChild);r.appendChild(document.createTextNode(e))}}},8579(e,r,o){var t=o(5072),i=o.n(t),n=o(7825),a=o.n(n),p=o(7659),d=o.n(p),c=o(5056),l=o.n(c),s=o(540),f=o.n(s),g=o(1113),u=o.n(g),m=o(8475),j={};j.styleTagTransform=u(),j.setAttributes=l(),j.insert=d().bind(null,"head"),j.domAPI=a(),j.insertStyleElement=f(),i()(m.A,j),m.A&&m.A.locals&&m.A.locals}}]);