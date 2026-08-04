"use strict";(self.rspackChunk_jupyter_docprovider_extension=self.rspackChunk_jupyter_docprovider_extension||[]).push([[306],{2078(e,o,r){var t=r(6758),n=r.n(t),a=r(935),i=r.n(a),l=r(9256),p=r(3028),s=r(9921),d=r(2674),c=i()(n());c.i(l.A),c.i(p.A),c.i(s.A),c.i(d.A),c.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

.jp-shared-link-body {
    user-select: none;
}
`,""]),r.d(o,{},{A:c})},9256(e,o,r){var t=r(6758),n=r.n(t),a=r(935),i=r.n(a)()(n());i.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

.jp-MenuBar-label {
  margin-left: 25px;
}

.jp-MenuBar-anonymousIcon span {
  width: 24px;
  text-align: center;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-MenuBar-anonymousIcon,
.jp-MenuBar-imageIcon {
  position: absolute;
  top: 1px;
  left: 8px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  vertical-align: middle;
  border-radius: 100%;
}

.jp-MenuBar-imageIcon img {
  width: 24px;
  border-radius: 100%;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-UserMenu-caretDownIcon {
  height: 22px;
  position: relative;
  top: 15%;
}
`,""]),r.d(o,{},{A:i})},2674(e,o,r){var t=r(6758),n=r.n(t),a=r(935),i=r.n(a)()(n());i.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

.jp-shared-link-body {
  user-select: none;
}

.jp-ManageSharesBody-search-container {
  margin-bottom: 10px;
}

.jp-ManageSharesBody-search-input {
  width: 100%;
  padding: 5px;
  margin-top: 5px;
}

.jp-ManageSharesBody-search-results {
  height: 10em;
  overflow-y: auto;
  border: 1px solid var(--jp-border-color0);
  padding: 5px;
  flex-shrink: 0;
}

.jp-ManageSharesBody-user-item {
  padding: 5px;
  cursor: pointer;
}

.jp-ManageSharesBody-user-item:hover {
  background-color: var(--jp-border-color3);
}

.jp-ManageSharesBody-selected-users {
  margin-top: 10px;
  height: 10em;
  overflow-y: auto;
  border: 1px solid var(--jp-border-color0);
  flex-shrink: 0;
}

.jp-ManageSharesBody-url-input {
  width: 100%;
  padding: 5px;
  margin-top: 10px;
}

.jp-ManageSharesBody-shares-table {
  width: 100%;
}

.jp-ManageSharesBody-shares-table td:nth-child(2),
.jp-ManageSharesBody-shares-table td:nth-child(3) {
  text-align: center;
}

.jp-Dialog-content:has(.jp-shared-link-body) {
    max-height: 750px;
}
`,""]),r.d(o,{},{A:i})},3028(e,o,r){var t=r(6758),n=r.n(t),a=r(935),i=r.n(a)()(n());i.push([e.id,`/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/************************************************************
                      Main Panel
*************************************************************/

.jp-RTCPanel {
  min-width: var(--jp-sidebar-min-width) !important;
  color: var(--jp-ui-font-color1);
  background: var(--jp-layout-color1);
  font-size: var(--jp-ui-font-size1);
}

/************************************************************
                      User Info Panel
*************************************************************/
.jp-UserInfoPanel {
  display: flex;
  flex-direction: column;
  max-height: 140px;
  padding-top: 3px;
}

.jp-UserInfo-Container {
  margin: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.jp-UserInfo-Icon {
  margin: auto;
  width: 50px;
  height: 50px;
  border-radius: 50px;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

.jp-UserInfo-Icon span {
  margin: auto;
  text-align: center;
  font-size: 25px;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-UserInfo-Info {
  margin: 20px;
  display: inline-flex;
  flex-direction: column;
}

.jp-UserInfo-Info label {
  font-weight: bold;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-UserInfo-Info input {
  text-decoration: none;
  border-top: none;
  border-left: none;
  border-right: none;
  border-color: var(--jp-ui-font-color1);
  border-width: 0.5px;
  background-color: transparent;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

/************************************************************
                Collaborators Info Panel
*************************************************************/

.jp-CollaboratorsPanel {
  overflow-y: auto;
}

.jp-CollaboratorsList {
  flex-direction: column;
  display: flex;
  z-index: 1000;
}

.jp-CollaboratorHeader {
  padding: 10px;
  display: flex;
  align-items: center;
  font-size: var(--jp-ui-font-size0);
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-CollaboratorHeader > span {
  padding-left: 7px;
}

.jp-ClickableCollaborator:hover {
  cursor: pointer;
  background-color: var(--jp-layout-color2);
  fill: var(--jp-ui-font-color0);
  color: var(--jp-ui-font-color0);
}

.jp-CollaboratorHeaderCollapser {
  transform: rotate(-90deg);
  margin: auto 0;
  height: 16px;
}

.jp-CollaboratorHeader:not(.jp-ClickableCollaborator) .jp-CollaboratorHeaderCollapser {
  visibility: hidden;
}

.jp-CollaboratorHeaderCollapser.jp-mod-expanded {
  transform: rotate(0deg);
}

.jp-CollaboratorIcon {
  border-radius: 100%;
  padding: 2px;
  width: 24px;
  height: 24px;
  display: flex;
}

.jp-CollaboratorIcon > span {
  text-align: center;
  margin: auto;
  font-size: 12px;
  fill: var(--jp-ui-font-color1);
  color: var(--jp-ui-font-color1);
}

.jp-CollaboratorFiles {
  padding-left: 1em;
  margin-top: 0;
  box-shadow: 0 2px 2px -2px rgb(0 0 0 / 24%);

}

/************************************************************
                User Info Details
*************************************************************/
.jp-UserInfo-Field {
  display: flex;
  justify-content: space-between;
}

.jp-UserInfo-Field > label,
.jp-UserInfo-Field > input {
  padding: 0.5em 1em;
  margin: 0.25em 0;
}

.jp-UserInfo-Field > label {
  font-weight: bold;
}

.jp-UserInfo-Field > input {
  border: none;
}

.jp-UserInfo-Field > input:not(:disabled) {
  cursor: pointer;
  background-color: var(--jp-input-background);
}

.jp-UserInfo-Field > input:focus {
  border: solid 1px var(--jp-cell-editor-active-border-color);
}

.jp-UserInfo-Field > input:focus-visible {
  outline: none;
}
`,""]),r.d(o,{},{A:i})},9921(e,o,r){var t=r(6758),n=r.n(t),a=r(935),i=r.n(a)()(n());i.push([e.id,`/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|---------------------------------------------------------------------------- */

.jp-toolbar-users-item {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
}

.jp-toolbar-users-item .jp-MenuBar-anonymousIcon,
.jp-toolbar-users-item .jp-MenuBar-imageIcon {
  position: relative;
  left: 0;
  height: 22px;
  width: 22px;
  box-sizing: border-box;
  cursor: default;
}
`,""]),r.d(o,{},{A:i})},935(e){e.exports=function(e){var o=[];return o.toString=function(){return this.map(function(o){var r="",t=void 0!==o[5];return o[4]&&(r+="@supports (".concat(o[4],") {")),o[2]&&(r+="@media ".concat(o[2]," {")),t&&(r+="@layer".concat(o[5].length>0?" ".concat(o[5]):""," {")),r+=e(o),t&&(r+="}"),o[2]&&(r+="}"),o[4]&&(r+="}"),r}).join("")},o.i=function(e,r,t,n,a){"string"==typeof e&&(e=[[null,e,void 0]]);var i={};if(t)for(var l=0;l<this.length;l++){var p=this[l][0];null!=p&&(i[p]=!0)}for(var s=0;s<e.length;s++){var d=[].concat(e[s]);t&&i[d[0]]||(void 0!==a&&(void 0===d[5]||(d[1]="@layer".concat(d[5].length>0?" ".concat(d[5]):""," {").concat(d[1],"}")),d[5]=a),r&&(d[2]&&(d[1]="@media ".concat(d[2]," {").concat(d[1],"}")),d[2]=r),n&&(d[4]?(d[1]="@supports (".concat(d[4],") {").concat(d[1],"}"),d[4]=n):d[4]="".concat(n)),o.push(d))}},o}},6758(e){e.exports=function(e){return e[1]}},2591(e){var o=[];function r(e){for(var r=-1,t=0;t<o.length;t++)if(o[t].identifier===e){r=t;break}return r}function t(e,t){for(var n={},a=[],i=0;i<e.length;i++){var l=e[i],p=t.base?l[0]+t.base:l[0],s=n[p]||0,d="".concat(p," ").concat(s);n[p]=s+1;var c=r(d),u={css:l[1],media:l[2],sourceMap:l[3],supports:l[4],layer:l[5]};if(-1!==c)o[c].references++,o[c].updater(u);else{var f=function(e,o){var r=o.domAPI(o);return r.update(e),function(o){o?(o.css!==e.css||o.media!==e.media||o.sourceMap!==e.sourceMap||o.supports!==e.supports||o.layer!==e.layer)&&r.update(e=o):r.remove()}}(u,t);t.byIndex=i,o.splice(i,0,{identifier:d,updater:f,references:1})}a.push(d)}return a}e.exports=function(e,n){var a=t(e=e||[],n=n||{});return function(e){e=e||[];for(var i=0;i<a.length;i++){var l=r(a[i]);o[l].references--}for(var p=t(e,n),s=0;s<a.length;s++){var d=r(a[s]);0===o[d].references&&(o[d].updater(),o.splice(d,1))}a=p}}},8128(e){var o={};e.exports=function(e,r){var t=function(e){if(void 0===o[e]){var r=document.querySelector(e);if(window.HTMLIFrameElement&&r instanceof window.HTMLIFrameElement)try{r=r.contentDocument.head}catch(e){r=null}o[e]=r}return o[e]}(e);if(!t)throw Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");t.appendChild(r)}},3051(e){e.exports=function(e){var o=document.createElement("style");return e.setAttributes(o,e.attributes),e.insert(o,e.options),o}},855(e,o,r){e.exports=function(e){var o=r.nc;o&&e.setAttribute("nonce",o)}},1740(e){e.exports=function(e){if("u"<typeof document)return{update:function(){},remove:function(){}};var o=e.insertStyleElement(e);return{update:function(r){var t,n,a;t="",r.supports&&(t+="@supports (".concat(r.supports,") {")),r.media&&(t+="@media ".concat(r.media," {")),(n=void 0!==r.layer)&&(t+="@layer".concat(r.layer.length>0?" ".concat(r.layer):""," {")),t+=r.css,n&&(t+="}"),r.media&&(t+="}"),r.supports&&(t+="}"),(a=r.sourceMap)&&"u">typeof btoa&&(t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")),e.styleTagTransform(t,o,e.options)},remove:function(){var e;null===(e=o).parentNode||e.parentNode.removeChild(e)}}}},3656(e){e.exports=function(e,o){if(o.styleSheet)o.styleSheet.cssText=e;else{for(;o.firstChild;)o.removeChild(o.firstChild);o.appendChild(document.createTextNode(e))}}},9361(e,o,r){var t=r(2591),n=r.n(t),a=r(1740),i=r.n(a),l=r(8128),p=r.n(l),s=r(855),d=r.n(s),c=r(3051),u=r.n(c),f=r(3656),h=r.n(f),m=r(2078),g={};g.styleTagTransform=h(),g.setAttributes=d(),g.insert=p().bind(null,"head"),g.domAPI=i(),g.insertStyleElement=u(),n()(m.A,g),m.A&&m.A.locals&&m.A.locals}}]);