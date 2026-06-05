"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[843],{1270(e,t,i){let a,o;i.r(t),i.d(t,{ESPHomePageDevice:()=>a0});var r,n=i(5172),s=i(9165),l=i(2009),d=i(3442),c=i(261),h=i(6668);class p{hostConnected(){}get deviceState(){return this._host.device?.state??h.g.UNKNOWN}get deviceTargetPlatform(){return this._host.device?.target_platform??""}get deviceCurrentAddress(){return this._host.device?.ip||this._host.device?.address||""}_openCommand(e,t,i){let a=this._host.commandDialog;a&&(a.configuration=e.configuration,a.name=e.friendly_name||e.name,a.open(t,i?{port:i}:void 0))}constructor(e){this.installMethodOpen=!1,this.onInstall=()=>{this._host.device&&(this.installMethodOpen=!0,this._host.requestUpdate())},this.onUpdate=()=>{let e=this._host.device;e&&this._openCommand(e,"install")},this.onInstallMethodClose=()=>{this.installMethodOpen=!1,this._host.requestUpdate()},this.onInstallMethodSelect=e=>{let t=this._host.device;if(this.installMethodOpen=!1,this._host.requestUpdate(),!t)return;let{method:i,port:a}=e.detail;"ota"===i?this._openCommand(t,"install",a??"OTA"):"server-serial"===i?this._openCommand(t,"install",a):"web-serial"===i?this._host.firmwareDialog?.installWebSerial(t):"web-download"===i?this._host.firmwareDialog?.installWebDownload(t):"binary-download"===i&&this._host.firmwareDialog?.installBinaryDownload(t)},this._host=e,e.addController(this)}}var u=i(1556),m=i(3140),v=i(9460),g=i(3632),f=i(1529),_=i(2063),b=i(1093),y=i(4008);function w(e={}){return{key:"",type:y.Hh.STRING,label:"",default_value:null,required:!1,description:null,options:null,allow_custom_value:!1,range:null,display_format:null,registry:null,unit_options:null,help_link:null,multi_value:!1,hidden:!1,advanced:!1,translation_key:null,translation_params:null,templatable:!1,depends_on:null,depends_on_value:null,depends_on_value_not:null,depends_on_component:null,references_component:null,pin_features:[],pin_mode:null,locked:!1,suggestions:null,config_entries:null,platform_type:null,supported_platforms:void 0,...e}}let $=new Set(["substitutions"]),x=new Set(["globals"]),k=new Set(["substitutions"]),z=[w({type:y.Hh.MAP,config_entries:[w({key:"value",label:"Value",required:!0})]})];function C(e,t){return $.has(e)?z:x.has(e)?[w({key:e,type:y.Hh.NESTED,multi_value:!0,label:E[e]??"Item",config_entries:t})]:t}let E={globals:"Global variable"};class A{run(e){return e.dirty?this._active?Promise.resolve(!1):new Promise(t=>{this._active={save:e.save,resolve:t},e.open()}):Promise.resolve(!0)}onDiscard(){let e=this._active;this._active=null,e?.resolve(!0)}async onSave(){let e=this._active;if(this._active=null,!e)return;let t=!1;try{t=await e.save()}catch{t=!1}e.resolve(t)}onCancel(){let e=this._active;this._active=null,e?.resolve(!1)}get isPending(){return null!==this._active}constructor(){this._active=null,this.cancelPending=this.onCancel}}i(3983);var q=i(8818);let S=/^\s*-(\s|$)/,M=/^\d+$/;function L(e){return""===e.trim()||e.startsWith("#")}function P(e){if(a===e&&o)return o;let t=e.split("\n"),i=[];for(let e=0;e<t.length;e++){let a=t[e].match(/^([a-zA-Z_][a-zA-Z0-9_]*):/);if(a){if(i.length>0){let a=i[i.length-1],o=a.fromLine-1,r=e-1;for(;r>o&&L(t[r]);)r--;a.toLine=r+1}i.push({key:a[1],fromLine:e+1,toLine:t.length})}}if(i.length>0){let e=i[i.length-1],a=e.fromLine-1,o=t.length-1;for(o>=0&&""===t[o]&&o--;o>a&&L(t[o]);)o--;e.toLine=o+1}let r=[];for(let e of i)r.push(...function(e,t){if(x.has(t.key))return[{key:t.key,fromLine:t.fromLine,toLine:t.toLine}];let i=t.fromLine-1,a=t.toLine-1,o=[];for(let t=i+1;t<=a;t++)(/^  -\s/.test(e[t])||/^  -$/.test(e[t]))&&o.push(t);if(0===o.length){let o="",r="";for(let t=i+1;t<=a;t++){let i=e[t].match(/^\s{2}name:\s*["']?(.+?)["']?\s*$/);i&&(o=i[1]);let a=e[t].match(/^\s{2}id:\s*["']?(\S+?)["']?\s*$/);a&&(r=a[1])}return[{key:t.key,fromLine:t.fromLine,toLine:t.toLine,name:o||void 0,id:r||void 0}]}let r=[];for(let i=0;i<o.length;i++){let n=o[i],s=i+1<o.length?o[i+1]-1:a,l="",d="",c="",h=R(e[n]);for(let t=n;t<=s;t++){let i=e[t];if(t!==n&&(i.match(/^ */)?.[0].length??0)!==h)continue;let a=i.match(/^\s+(?:-\s+)?name:\s*["']?(.+?)["']?\s*$/);a&&(l=a[1]);let o=i.match(/^\s+(?:-\s+)?id:\s*["']?(\S+?)["']?\s*$/);o&&(d=o[1]);let r=i.match(/^\s+(?:-\s+)?platform:\s*["']?(\S+?)["']?\s*$/);r&&(c=r[1])}r.push({key:t.key,fromLine:n+1,toLine:s+1,name:l||void 0,id:d||void 0,platform:c||void 0,parentKey:t.key})}return r}(t,e));return a=e,o=r,r}function F(e,t){let i=null,a=1/0;for(let o of e){if(t<o.fromLine||t>o.toLine)continue;let e=o.toLine-o.fromLine;e<a&&(i=o,a=e)}return i}function T(e,t){let i=t.parentKey;if(void 0===i)return t.id??t.key;if(t.id)return t.id;let a=0;for(let o of e)o.parentKey===i&&o.fromLine<t.fromLine&&a++;return`${i}_${a}`}function R(e){let t=e.match(/^\s*-\s+(?=\S)/)?.[0].length;return void 0!==t?t:(e.match(/^ */)?.[0].length??0)+2}let D=/^(\s+)([a-z0-9_]+_action):/;function I(e){let t=e.split("\n"),i=P(e),a=[];for(let e=0;e<t.length;e++){let o=t[e].match(/^(\s+)(on_[a-zA-Z_]+):/);if(!o)continue;let r=o[1].length,n=o[2],s=e+1,l=O(t,e,r),d=F(i,s);if(d&&void 0===d.parentKey&&"esphome"===d.key){a.push({key:`automation:device_on:${n}`,displayLabel:`esphome → ${n}`,fromLine:s,toLine:l,parentKey:"esphome",eventKey:n});continue}let c=null;if(d&&r===R(t[d.fromLine-1]??"")&&(c=T(i,d)),d&&c){let e=d.name||c,i={id:c,name:d.name??void 0,parentKey:d.parentKey??d.key,eventKey:n},o=function(e,t,i){let a=N(e,t,i);return 0===a.length?null:a.every(t=>(function(e,t){let i=e[t.fromLine-1]??"";if(K.test(i))return!0;let a=R(i);for(let i=t.fromLine;i<t.toLine&&i<e.length;i++){let t=e[i].match(B);if(t&&t[1].length===a)return!0}return!1})(e,t))?a:null}(t,s,l);o?o.forEach((t,o)=>{a.push({...i,key:`automation:component_on:${c}:${n}:${o}`,displayLabel:`${e} → ${n} #${o+1}`,fromLine:t.fromLine,toLine:t.toLine})}):a.push({...i,key:`automation:component_on:${c}:${n}`,displayLabel:`${e} → ${n}`,fromLine:s,toLine:l});continue}a.push({key:`automation:unscoped:${n}:${s}`,displayLabel:n,fromLine:s,toLine:l,eventKey:n})}for(let e=0;e<t.length;e++){let o=t[e].match(D);if(!o)continue;let r=o[1].length,n=o[2];if(n.startsWith("on_"))continue;let s=e+1,l=F(i,s);if(!l||r!==R(t[l.fromLine-1]??""))continue;let d=T(i,l);if(!d)continue;let c=l.name||d;a.push({key:`automation:component_action:${d}:${n}`,displayLabel:`${c} → ${n}`,fromLine:s,toLine:O(t,e,r),id:d,parentKey:l.parentKey??l.key,actionField:n})}for(let e of["script","interval"]){let i=j(t,e);i&&N(t,i.fromLine,i.toLine).forEach((i,o)=>{let r="script"===e?U(t,i.fromLine,"id"):null,n="script"===e&&r?`automation:script:${r}`:`automation:interval:${o}`,s="script"===e&&r?`script: ${r}`:`interval #${o+1}`,l={};if("interval"===e){let e=U(t,i.fromLine,"interval");e&&(l.every=e)}a.push({key:n,displayLabel:s,fromLine:i.fromLine,toLine:i.toLine,id:"script"===e&&r?r:void 0,parentKey:e,meta:Object.keys(l).length>0?l:void 0})})}let o=j(t,"api");if(o){let e=function(e,t,i,a){let o=null;for(let a=t;a<i&&a<e.length;a++){let t=e[a];if(""===t.trim())continue;let i=(t.match(/^(\s+)/)??["",""])[1].length;if(i>0){o=i;break}}if(null===o)return null;let r=RegExp(`^\\s{${o}}${a}\\s*:`);for(let a=t;a<i&&a<e.length;a++)if(r.test(e[a]))return{fromLine:a+1,toLine:O(e,a,o)};return null}(t,o.fromLine,o.toLine,"actions");if(e)for(let i of N(t,e.fromLine,e.toLine)){let e=U(t,i.fromLine,"action")??U(t,i.fromLine,"service");e&&a.push({key:`automation:api_action:${e}`,displayLabel:`API: ${e}`,fromLine:i.fromLine,toLine:i.toLine,id:e,parentKey:"api"})}}return a}function O(e,t,i){for(let a=t+1;a<e.length;a++)if(""!==e[a].trim()&&(e[a].match(/^(\s*)/)??["",""])[1].length<=i)return a;return e.length}function j(e,t){for(let i=0;i<e.length;i++)if(e[i].match(RegExp(`^${t}\\s*:`)))return{fromLine:i+1,toLine:O(e,i,0)};return null}function N(e,t,i){let a=[],o=null,r=null;for(let n=t;n<i&&n<e.length;n++){let t=e[n];if(""===t.trim())continue;let i=t.match(/^(\s*)-\s/);if(!i)continue;let s=i[1].length;null===o&&(o=s),s>o||(r&&a.push({fromLine:r.fromLine,toLine:n}),r={fromLine:n+1})}return r&&a.push({fromLine:r.fromLine,toLine:i}),a}let Z="then|seconds|minutes|hours|days_of_week|days_of_month|months|at|cron",B=RegExp(`^(\\s*)(?:${Z})\\s*:`),K=RegExp(`^\\s*-\\s+(?:${Z})\\s*:`);function U(e,t,i){let a=e[t-1],o=`${i}:\\s*["']?([^"'\\s]+)["']?`,r=a.match(RegExp(`^\\s*-\\s*${o}`));if(r)return r[1];let n=a.match(/^(\s*)-/)?.[1].length??0,s=RegExp(`^\\s+${o}`);for(let i=t;i<e.length;i++){let t=e[i];if(""===t.trim())continue;if((t.match(/^(\s*)/)??["",""])[1].length<=n)break;let a=t.match(s);if(a)return a[1]}return null}let H=new Set(["esp32","esp8266","rp2040","bk72xx","rtl87xx","ln882x","nrf52","host","esphome","logger","api","ota","wifi","ethernet","mqtt","mdns","network","web_server","captive_portal","improv_serial","safe_mode","debug","preferences","update","external_components","packages","substitutions","dashboard_import","globals"]),W=new Set(["script","interval"]);function V(e){let t=[],i=[],a=[];for(let o of e)H.has(o.key)?t.push(o):W.has(o.key)?a.push(o):i.push(o);return{core:t,components:i,automations:a}}function Y(e,t){let i=F(I(e).filter(e=>!e.key.startsWith("automation:unscoped:")),t);return i||F(P(e),t)}function G(e){return e.platform?e.platform.startsWith(`${e.key}.`)?e.platform:`${e.key}.${e.platform}`:e.key}function J(e,t,i){if(!e||!t)return;let a=P(e).filter(e=>G(e)===t);if(0!==a.length)return 1===a.length||void 0===i?a[0].fromLine:a.reduce((e,t)=>Math.abs(t.fromLine-i)<Math.abs(e.fromLine-i)?t:e).fromLine}function Q(e,t,i){if(void 0===t||!Number.isInteger(t)||t<1||null!==i||!e)return null;let a=Y(e,t);return a?{sectionKey:G(a),range:{fromLine:t,toLine:t}}:null}var X=i(1269);let ee=/line\s+(\d+)\s*,\s*column\s+(\d+)/i,et=/line\s+(\d+)/i,ei=(0,l.AH)`
  :host {
    display: block;
  }

  .page {
    box-sizing: border-box;
    padding: var(--wa-space-l) var(--wa-space-l) 0;
    min-height: calc(100vh - var(--esphome-header-height));
  }

  .layout-grid {
    display: grid;
    grid-template-columns: minmax(230px, 1fr) minmax(0, 5fr);
    gap: var(--wa-space-l);
    height: calc(
      100vh - var(--esphome-header-height) - var(--esphome-footer-height) - var(
          --wa-space-l
        )
    );
    transition: grid-template-columns 0.25s ease;
  }

  .layout-grid.nav-collapsed {
    grid-template-columns: minmax(0, 5fr);
  }

  .layout-grid.nav-collapsed .desktop-nav {
    display: none;
  }

  .drawer,
  .drawer-backdrop {
    display: none;
  }

  .back-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: color-mix(in srgb, var(--esphome-on-primary), transparent 80%);
    color: var(--esphome-on-primary);
    cursor: pointer;
    padding: 4px;
    border-radius: var(--wa-border-radius-m);
    margin-right: var(--wa-space-xs);
  }

  .back-btn wa-icon {
    font-size: 14px;
  }

  .back-btn:hover {
    background: color-mix(in srgb, var(--esphome-on-primary), transparent 70%);
  }

  /* Sticky-bookmark expand affordance. Anchored to the left edge of
     the page wrapper (position: relative below), so it hugs the
     editor card and reads as a tab hanging off its side. Visible
     only when the navigator is hidden (desktop collapsed or mobile
     drawer closed) — the parent component gates rendering via the
     showEdgeTab flag, so we don't need a CSS hide branch. */
  .page {
    position: relative;
  }

  .nav-edge-tab {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 5;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    /* Width spans the page's left padding minus a small inset, so
       the tab's right edge stops short of the editor card and the
       gap (--wa-space-2xs) reads as deliberate breathing room. */
    width: calc(var(--wa-space-l) - var(--wa-space-2xs));
    height: 44px;
    padding: 0;
    border: none;
    border-radius: 0 var(--wa-border-radius-m) var(--wa-border-radius-m) 0;
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    cursor: pointer;
    box-shadow: var(--wa-elevation-02);
    transition: background 0.12s;
  }

  .nav-edge-tab:hover {
    background: color-mix(in srgb, var(--esphome-primary), black 8%);
  }

  .nav-edge-tab wa-icon {
    font-size: 18px;
  }

  @media (max-width: 900px) {
    .nav-edge-tab {
      /* Mobile page has no padding so the calc width collapses to a
         negative value — fall back to a fixed width that sticks the
         tab off the viewport's left edge over the editor. */
      width: 24px;
    }
  }

  @media (max-width: 900px) {
    /* Drop the page padding on mobile so the editor goes edge-to-edge.
       The card itself is already small at this width — wasting ~16px
       on each side to a frame just makes it harder to read; logs go
       full-screen the same way for the same reason.
       Each dvh line is paired with a vh fallback above it so
       pre-2022 browsers that don't recognise dvh still pick up the
       mobile sizing instead of dropping the declaration and falling
       through to the desktop rule (which had an extra
       2 * var(--wa-space-l) subtracted and would leave a gap). */
    .page {
      padding: 0;
      min-height: calc(
        100vh - var(--esphome-header-height) - var(--esphome-footer-height)
      );
      min-height: calc(
        100dvh - var(--esphome-header-height) - var(--esphome-footer-height)
      );
    }

    .layout-grid {
      grid-template-columns: 1fr;
      gap: 0;
      height: calc(100vh - var(--esphome-header-height) - var(--esphome-footer-height));
      height: calc(100dvh - var(--esphome-header-height) - var(--esphome-footer-height));
    }

    .desktop-nav {
      display: none !important;
    }

    .drawer-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.4);
      z-index: 99;
    }

    .drawer-backdrop--open {
      display: block;
    }

    .drawer {
      display: block;
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: 300px;
      max-width: 85vw;
      z-index: 100;
      background: var(--wa-color-surface-default);
      box-shadow: var(--wa-shadow-l);
      overflow-y: auto;
      transform: translateX(-100%);
      transition: transform 0.25s ease;
      --navigator-border-radius: 0;
      --navigator-border: none;
    }

    .drawer--open {
      transform: translateX(0);
    }
  }
`;i(2202),i(9968);let ea=(0,l.AH)`
  :host {
    display: contents;
  }

  .card {
    background: var(--wa-color-surface-default);
    border-radius: var(--wa-border-radius-l);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    box-shadow: var(--wa-elevation-02);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  /* Navigator hidden + YAML-only layout = the title bar is the only
     non-editor chrome left on screen. Squeeze it so it gives the
     YAML editor back the vertical space the user already implicitly
     asked for by collapsing both panels. */
  .card-header--compact {
    padding: var(--wa-space-2xs) var(--wa-space-m);
  }

  .card-header--compact .editor-header-title {
    font-size: var(--wa-font-size-2xs);
  }

  .card-header--compact .layout-toggle wa-icon,
  .card-header--compact .diff-toggle wa-icon {
    font-size: 16px;
  }

  ::slotted([slot="header-start"]) {
    margin-right: var(--wa-space-xs);
  }

  .editor-header-main {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
    flex: 1;
  }

  .editor-header-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .editor-floating-actions {
    position: absolute;
    bottom: var(--wa-space-m);
    right: var(--wa-space-m);
    z-index: 10;
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .save-button,
  .validate-button,
  .install-fab {
    display: inline-flex;
    align-items: center;
    box-sizing: border-box;
    gap: 3px;
    padding: 7px 14px;
    border: var(--wa-border-width-s) solid transparent;
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    line-height: 1;
    transition:
      background 0.12s,
      border-color 0.12s,
      box-shadow 0.12s,
      transform 0.12s;
  }

  .save-button {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    box-shadow: var(--esphome-primary-shadow);
  }

  .save-button:hover:not(:disabled) {
    background: var(--esphome-primary-hover);
    box-shadow: var(--esphome-primary-shadow-hover);
    transform: translateY(-1px);
  }

  .save-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .save-button:disabled {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 35%,
      var(--wa-color-surface-default)
    );
    color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
  }

  /* Subordinate to Save: surface-tinted variant so the primary
     action stays visually dominant. The disabled state (YAML buffer
     dirty) is the more common one — a bright primary button there
     would compete with Save for attention. */
  .validate-button {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    border-color: var(--wa-color-surface-border);
  }

  .validate-button:hover:not(:disabled) {
    background: var(--wa-color-surface-raised);
    border-color: color-mix(in srgb, var(--wa-color-text-normal), transparent 70%);
  }

  .validate-button:disabled {
    background: var(--wa-color-surface-default);
    color: color-mix(in srgb, var(--wa-color-text-normal), transparent 55%);
    border-color: var(--wa-color-surface-border);
    cursor: not-allowed;
  }

  .install-fab {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 10%,
      var(--wa-color-surface-default)
    );
    color: var(--esphome-primary);
    border-color: var(--esphome-tint-border);
  }

  .install-fab:hover:not(:disabled) {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 18%,
      var(--wa-color-surface-default)
    );
    border-color: var(--esphome-primary);
  }

  .install-fab:disabled {
    background: var(--wa-color-surface-default);
    color: color-mix(in srgb, var(--esphome-primary), transparent 50%);
    border-color: var(--wa-color-surface-border);
    cursor: not-allowed;
  }

  .save-button wa-icon,
  .validate-button wa-icon,
  .install-fab wa-icon {
    font-size: 16px;
  }

  /* Tooltip carrier so the "why disabled" hint reaches mouse users
     even when the underlying button has the disabled attribute
     (which suppresses pointer events on the button itself). */
  .validate-button-wrap {
    display: inline-flex;
  }

  .header-actions {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .diff-toggle {
    border: none;
    background: transparent;
    color: var(--esphome-on-primary);
    padding: 2px 4px;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .diff-toggle[aria-pressed="true"] {
    background: color-mix(in srgb, var(--esphome-on-primary), transparent 85%);
  }

  .diff-toggle:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .diff-toggle wa-icon {
    font-size: 18px;
  }

  .layout-toggle {
    display: inline-flex;
    align-items: center;
    gap: 2px;
  }

  .layout-toggle button {
    border: none;
    background: transparent;
    color: var(--esphome-on-primary);
    padding: 2px 4px;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .layout-toggle button[aria-pressed="true"] {
    background: color-mix(in srgb, var(--esphome-on-primary), transparent 85%);
  }

  .layout-toggle button:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .layout-toggle wa-icon {
    font-size: 18px;
  }

  .card-body {
    position: relative;
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .editor-layout {
    flex: 1;
    min-height: 0;
    display: grid;
    gap: 0;
  }

  .editor-layout--both {
    grid-template-columns: 1fr 1px 1fr;
  }

  .editor-layout--left {
    grid-template-columns: 1fr;
  }

  .editor-layout--right {
    grid-template-columns: 1fr;
  }

  .editor-pane {
    padding: var(--wa-space-m);
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    min-height: 0;
    overflow: hidden;
  }

  .editor-pane--left {
    overflow-y: auto;
  }

  /* The floating Install / Validate / Save row overlays the
     bottom-right of the card body. Reserve room below the
     content so the last lines sit a header-matching
     var(--wa-space-m) above the buttons (button bottom inset +
     button height + the same top-of-pane gap the editor already
     has via .editor-pane's padding).
     Applied to:
     - .editor-pane--right always (the row sits over its bottom-right
       in both-pane + right-only layouts).
     - .editor-layout--left .editor-pane--left (board-info-only
       layout, where the right pane is hidden and the buttons now
       overlap the full-width left pane). */
  .editor-pane--right,
  .editor-layout--left .editor-pane--left {
    padding-bottom: calc(var(--wa-space-m) * 2 + 2.25rem);
  }

  .editor-pane-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  /* Document-level "configuration invalid" banner above the editor.
     A flex child of .editor-pane (column + gap), so it sits above the
     editor body and the body's flex:1 reclaims the rest. */
  .invalid-banner {
    flex: 0 0 auto;
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-danger-fill-quiet);
    border: var(--wa-border-width-s) solid var(--wa-color-danger-60);
    color: var(--wa-color-danger-text-normal);
  }

  .invalid-banner-icon {
    flex: 0 0 auto;
    font-size: 1.25rem;
    margin-top: 0.05rem;
    color: var(--wa-color-danger-60);
  }

  .invalid-banner-text {
    display: flex;
    flex-direction: column;
    gap: 3px;
    line-height: 1.4;
    min-width: 0;
  }

  .invalid-banner-error {
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-semibold);
    word-break: break-word;
  }

  .invalid-banner-more {
    font-size: var(--wa-font-size-2xs);
    opacity: 0.85;
  }

  .editor-pane-body {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .pane-divider {
    background: var(--wa-color-surface-border);
    width: 1px;
    align-self: stretch;
  }

  .editor-layout--left .editor-pane--right,
  .editor-layout--right .editor-pane--left {
    display: none;
  }

  @media (max-width: 900px) {
    .layout-toggle .split-btn {
      display: none;
    }

    /* Drop the card frame on mobile — the page wrapper already
       removes its padding so the editor occupies the full viewport.
       Border / border-radius / shadow at small widths just shave
       pixels off the editing area without adding any meaning. */
    .card {
      border: none;
      border-radius: 0;
      box-shadow: none;
    }
  }
`;function eo(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(3238);class er extends l.WF{render(){if(this._darkMode?this.setAttribute("dark",""):this.removeAttribute("dark"),this.oldValue===this.newValue)return(0,l.qy)`<div class="empty">${this._localize("device.diff_no_changes")}</div>`;let e=function(e,t){let i=e.split("\n"),a=t.split("\n"),o=i.length,r=a.length,n=[];for(let e=0;e<=o;e++)n.push(new Uint32Array(r+1));for(let e=1;e<=o;e++)for(let t=1;t<=r;t++)n[e][t]=i[e-1]===a[t-1]?n[e-1][t-1]+1:Math.max(n[e-1][t],n[e][t-1]);let s=[],l=o,d=r;for(;l>0||d>0;)l>0&&d>0&&i[l-1]===a[d-1]?(s.push({type:"context",oldLine:l,newLine:d,content:i[l-1]}),l--,d--):d>0&&(0===l||n[l][d-1]>=n[l-1][d])?(s.push({type:"add",newLine:d,content:a[d-1]}),d--):(s.push({type:"remove",oldLine:l,content:i[l-1]}),l--);return s.reverse()}(this.oldValue,this.newValue);return(0,l.qy)`
      <table>
        <tbody>
          ${e.map(e=>this._renderLine(e))}
        </tbody>
      </table>
    `}_renderLine(e){let t="add"===e.type?"+":"remove"===e.type?"-":" ",i="remove"===e.type?e.oldLine:e.newLine;return(0,l.qy)`
      <tr class=${e.type}>
        <td class="gutter">${i??(0,l.qy)`&nbsp;`}</td>
        <td class="marker">${t}</td>
        <td class="content">${e.content||l.s6}</td>
      </tr>
    `}constructor(...e){super(...e),this._darkMode=!1,this._localize=e=>e,this.oldValue="",this.newValue=""}}er.styles=(0,l.AH)`
    :host {
      display: block;
      flex: 1;
      min-height: 0;
      position: relative;
      overflow: auto;
      font-family: "JetBrains Mono", "Fira Code", monospace;
      font-size: 13px;
      line-height: 1.5;
      background: var(--diff-bg);
      color: var(--diff-fg);
      --diff-bg: #ffffff;
      --diff-fg: #1f2328;
      --diff-gutter-bg: #f6f8fa;
      --diff-gutter-fg: #6e7781;
      --diff-add-bg: #e6ffec;
      --diff-add-marker-bg: #abf2bc;
      --diff-add-fg: #1a7f37;
      --diff-remove-bg: #ffebe9;
      --diff-remove-marker-bg: #ffcecb;
      --diff-remove-fg: #cf222e;
      --diff-empty-fg: #8c959f;
    }

    :host([dark]) {
      --diff-bg: #0d1117;
      --diff-fg: #e6edf3;
      --diff-gutter-bg: #161b22;
      --diff-gutter-fg: #7d8590;
      --diff-add-bg: #033a16;
      --diff-add-marker-bg: #1a7f37;
      --diff-add-fg: #aff5b4;
      --diff-remove-bg: #67060c;
      --diff-remove-marker-bg: #b62324;
      --diff-remove-fg: #ffcecb;
      --diff-empty-fg: #6e7681;
    }

    .empty {
      padding: var(--wa-space-l);
      text-align: center;
      color: var(--diff-empty-fg);
      font-family: var(--wa-font-family-body);
      font-size: var(--wa-font-size-s);
    }

    table {
      border-collapse: collapse;
      width: 100%;
      table-layout: fixed;
    }

    tr {
      vertical-align: top;
    }

    .gutter {
      width: 1em;
      padding: 0 8px;
      padding-right: 14px;
      text-align: right;
      background: var(--diff-gutter-bg);
      color: var(--diff-gutter-fg);
      user-select: none;
      white-space: nowrap;
    }

    .marker {
      width: 1.5em;
      padding: 0 6px;
      text-align: center;
      user-select: none;
      font-weight: 600;
      border-right: 1px solid color-mix(in srgb, var(--diff-fg), transparent 90%);
    }

    .content {
      padding: 0 8px;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      font-variant-ligatures: none;
    }

    tr.add .marker,
    tr.add .content {
      background: var(--diff-add-bg);
      color: var(--diff-add-fg);
    }

    tr.add .marker {
      background: var(--diff-add-marker-bg);
    }

    tr.remove .marker,
    tr.remove .content {
      background: var(--diff-remove-bg);
      color: var(--diff-remove-fg);
    }

    tr.remove .marker {
      background: var(--diff-remove-marker-bg);
    }
  `,eo([(0,n.Fg)({context:u.B6,subscribe:!0}),(0,d.wk)()],er.prototype,"_darkMode",void 0),eo([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],er.prototype,"_localize",void 0),eo([(0,d.MZ)()],er.prototype,"oldValue",void 0),eo([(0,d.MZ)()],er.prototype,"newValue",void 0),er=eo([(0,d.EM)("esphome-yaml-diff")],er),i(2248);var en=i(8763),es=i(6910);let el=(0,l.AH)`
  :host {
    display: flex;
    flex-direction: column;
  }

  .board-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    gap: var(--wa-space-l);
  }

  .board-info {
    display: flex;
    flex-direction: column;
    flex: 1;
    gap: var(--wa-space-s);
    min-width: 0;
  }

  .board-name {
    margin: 0;
  }

  .board-image {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 140px;
    height: 100px;
    padding: var(--wa-space-s);
    background: var(--wa-color-surface-lowered);
    border-radius: var(--wa-border-radius-l);
    box-sizing: border-box;
  }

  .board-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .board-tags {
    display: flex;
    flex-wrap: wrap;
    gap: var(--wa-space-2xs);
  }

  .board-info-link {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    font-size: var(--wa-font-size-xs);
    color: var(--esphome-primary);
    text-decoration: underline;
    margin-left: var(--wa-space-s);
  }

  .board-info-link:hover {
    text-decoration: none;
  }

  /* A <button> styled to read as a sibling link to "More info". */
  .board-change-link {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    font-size: var(--wa-font-size-xs);
    font-family: inherit;
    color: var(--esphome-primary);
    text-decoration: underline;
    margin-left: var(--wa-space-s);
    padding: 0;
    border: none;
    background: none;
    cursor: pointer;
  }

  .board-change-link:hover {
    text-decoration: none;
  }

  .board-description {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .board-separator {
    height: 1px;
    background-color: var(--wa-color-surface-lowered);
    width: 100%;
    margin-top: var(--wa-space-m);
  }

  /* ─── Just-created welcome banner ─── */

  .welcome-banner {
    margin-top: var(--wa-space-m);
  }

  .welcome-banner-title {
    margin: var(--wa-space-xs) 0 var(--wa-space-2xs);
    font-size: var(--wa-font-size-m);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  .welcome-banner-text {
    margin: 0;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
    line-height: 1.5;
  }

  .welcome-banner-close {
    position: absolute;
    top: var(--wa-space-2xs);
    right: var(--wa-space-2xs);
    background: transparent;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    border-radius: var(--wa-border-radius-s);
    transition:
      background 0.12s,
      color 0.12s;
  }

  .welcome-banner-close:hover {
    background: var(--esphome-tint-strong);
    color: var(--wa-color-text-normal);
  }

  .welcome-banner-close wa-icon {
    font-size: 18px;
    display: block;
  }

  /* ─── Step CTA ─── */

  .step-section {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    padding-top: var(--wa-space-m);
  }

  .step-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  .step-desc {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .action-item {
    padding: var(--wa-space-2xs) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: transparent;
    color: var(--esphome-primary);
    border: var(--wa-border-width-s) solid var(--esphome-primary);
    gap: var(--wa-space-s);
    cursor: pointer;
    user-select: none;
    font-family: inherit;
    font-size: inherit;
    transition:
      background 0.12s,
      color 0.12s;
    align-self: flex-start;
    /* Equal width across the three step CTAs so they line up
       visually no matter how long the longest label is. */
    width: 280px;
    max-width: 100%;
    margin-top: var(--wa-space-s);
  }

  .action-item:hover {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .action-item:focus-visible {
    outline: 2px solid var(--esphome-primary);
    outline-offset: 2px;
  }

  .action-item p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .action-item wa-icon {
    font-size: var(--wa-font-size-l);
  }

  .action-item div {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }
`;i(4636),i(7473);var ed=i(5660);let ec=(0,l.AH)`
  esphome-base-dialog {
    --width: 560px;
  }
  esphome-base-dialog::part(body) {
    padding: var(--wa-space-l);
  }
  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    margin-bottom: var(--wa-space-m);
  }
  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
  }
  .field-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
    margin: 0;
  }
  .field-desc a {
    color: var(--wa-color-brand-fill-loud, #0b5cad);
  }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--wa-space-s);
    margin-top: var(--wa-space-l);
  }

  .actions button {
    display: inline-flex;
    align-items: center;
    box-sizing: border-box;
    gap: 3px;
    padding: 7px 14px;
    border: var(--wa-border-width-s) solid transparent;
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    line-height: 1;
    transition:
      background 0.12s,
      border-color 0.12s,
      box-shadow 0.12s,
      transform 0.12s;
  }
  .actions .primary {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    box-shadow: var(--esphome-primary-shadow);
  }
  .actions .primary:hover:not(:disabled) {
    background: var(--esphome-primary-hover);
    box-shadow: var(--esphome-primary-shadow-hover);
    transform: translateY(-1px);
  }
  .actions .primary:active:not(:disabled) {
    transform: translateY(0);
  }
  .actions .primary:disabled {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 35%,
      var(--wa-color-surface-default)
    );
    color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
  }
  .error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }
  .intro {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    margin: 0 0 var(--wa-space-m) 0;
    line-height: 1.5;
  }
  /* Interval-row pairing: matches the editor's inline
     TIME_PERIOD layout so the dialog reads as the same
     kind of compound input the user will see again in the
     section editor. */
  .interval-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }
  .interval-inputs > input {
    flex: 1 1 auto;
    min-width: 0;
  }
  .interval-inputs > wa-select {
    flex: 0 0 auto;
    min-width: 6rem;
  }
`;function eh(){return{trigger_id:null,trigger_params:{},actions:[]}}function ep(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a,...o]=t;if(0===o.length){if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}let r=e[a]&&"object"==typeof e[a]&&!Array.isArray(e[a])?e[a]:{};return{...e,[a]:ep(r,o,i)}}function eu(e,t,i){if(t<0||t>=e.length)return e;let a=e.slice();return a[t]=i,a}function em(e,t){if(t<0||t>=e.length)return e;let i=e.slice();return i.splice(t,1),i}function ev(e,t,i){if(t<0||i<0||t>=e.length||i>=e.length||t===i)return e;let a=e.slice();return[a[t],a[i]]=[a[i],a[t]],a}function eg(e){switch(e.kind){case"device_on":return`automation:device_on:${e.trigger}`;case"component_on":return void 0===e.index?`automation:component_on:${e.component_id}:${e.trigger}`:`automation:component_on:${e.component_id}:${e.trigger}:${e.index}`;case"component_action":return`automation:component_action:${e.component_id}:${e.field}`;case"script":return`automation:script:${e.id}`;case"interval":return`automation:interval:${e.index}`;case"light_effect":return`automation:light_effect:${e.component_id}:${e.index}`;case"api_action":return`automation:api_action:${e.action_name}`}}function ef(e,t){let i=e.split("\n"),a=t.fromLine-1,o=Math.max(0,t.toLine-t.fromLine+1),r=t.replacement.endsWith("\n")?t.replacement.slice(0,-1):t.replacement,n=""===r?[]:r.split("\n");return[...i.slice(0,a),...n,...i.slice(a+o)].join("\n")}function e_(e){if(!e.startsWith("automation:"))return null;let t=e.split(":");switch(t[1]){case"device_on":return t[2]?{kind:"device_on",trigger:t[2]}:null;case"component_on":if(t.length<4)return null;if(t.length>=5){let e=Number(t[4]);return Number.isInteger(e)&&e>=0?{kind:"component_on",component_id:t[2],trigger:t[3],index:e}:null}return{kind:"component_on",component_id:t[2],trigger:t[3]};case"component_action":return 4===t.length&&t[2]&&t[3]?{kind:"component_action",component_id:t[2],field:t[3]}:null;case"script":return t[2]?{kind:"script",id:t[2]}:null;case"interval":{let e=Number(t[2]);return Number.isFinite(e)?{kind:"interval",index:e}:null}case"light_effect":{let e=Number(t[3]);return t[2]&&Number.isFinite(e)?{kind:"light_effect",component_id:t[2],index:e}:null}case"api_action":return t[2]?{kind:"api_action",action_name:t[2]}:null;default:return null}}function eb(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(986),i(256),i(6117),i(9288);class ey extends l.WF{open(e){this._prefilled=void 0!==e,this._kind=e?.kind??"device_on",this._componentId=e?.kind==="component_on"?e.componentId:"",this._triggerId=null,this._intervalValue="",this._intervalUnit="s",this._error="",this._open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration){this._loading=!0;try{this._available=await this._api.getAvailableAutomations(this.configuration)}catch(e){this._error=e instanceof Error?e.message:String(e)}finally{this._loading=!1}}}render(){let e=this.boardName?this._localize("device.add_automation_dialog_title",{name:this.boardName}):this._localize("device.add_automation");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      @request-close=${this._onRequestClose}
    >
      ${this._loading&&!this._available?(0,l.qy)`<div style="text-align: center; padding: 32px;">
            <wa-spinner></wa-spinner>
          </div>`:this._renderForm()}
    </esphome-base-dialog>`}_renderForm(){let e=this._filteredTriggers(),t="component_on"!==this._kind,i="interval"===this._kind,a=!this._prefilled,o="component_on"===this._kind&&!this._prefilled;return(0,l.qy)`
      <p class="intro">
        ${(0,es.G)(this._localize("device.automation_header_description"))}
      </p>
      ${a?(0,l.qy)`<div class="field">
            <label class="field-label" id="kind-label">
              ${this._localize("device.automation_wizard_pick_target")}
            </label>
            <wa-select
              aria-labelledby="kind-label"
              value=${this._kind}
              ?disabled=${this._saving}
              @change=${e=>this._onKindChange(e.target.value)}
            >
              <wa-option value="device_on" ?selected=${"device_on"===this._kind}>
                ${this._localize("device.automation_target_device")}
              </wa-option>
              <wa-option value="component_on" ?selected=${"component_on"===this._kind}>
                ${this._localize("device.automation_target_component")}
              </wa-option>
              <wa-option value="interval" ?selected=${"interval"===this._kind}>
                ${this._localize("device.automation_target_interval")}
              </wa-option>
            </wa-select>
          </div>`:l.s6}
      ${o?this._renderComponentRow(t):l.s6}
      ${"interval"===this._kind?this._renderIntervalRow():l.s6}
      ${!i?this._renderTriggerRow(e):l.s6}
      ${this._error?(0,l.qy)`<p class="error" role="alert">${this._error}</p>`:l.s6}
      <div class="actions">
        <button
          type="button"
          class="primary"
          ?disabled=${this._saving||!this._canContinue()}
          @click=${this._onContinue}
        >
          ${this._saving?this._localize("device.adding"):this._localize("device.add_automation_continue")}
        </button>
      </div>
    `}_renderComponentRow(e){let t=this._available?.devices??[];return 0===t.length?(0,l.qy)`<p class="error">
        ${this._localize("device.automation_target_no_components")}
      </p>`:(0,l.qy)`<div class="field">
      <label class="field-label" id="component-label">
        ${this._localize("device.automation_wizard_pick_component")}
      </label>
      <wa-select
        aria-labelledby="component-label"
        value=${this._componentId}
        ?disabled=${this._saving||e}
        @change=${e=>this._onComponentChange(e.target.value)}
      >
        ${t.map(e=>(0,l.qy)`<wa-option value=${e.id} ?selected=${e.id===this._componentId}>
              ${e.name??e.id} (${e.component_id})
            </wa-option>`)}
      </wa-select>
    </div>`}_renderIntervalRow(){return(0,l.qy)`<div class="field">
      <label class="field-label" id="interval-label">
        ${this._localize("device.automation_interval_label")}
      </label>
      <div class="interval-inputs">
        <input
          type="text"
          inputmode="decimal"
          aria-labelledby="interval-label"
          .value=${this._intervalValue}
          placeholder="0"
          ?disabled=${this._saving}
          @input=${e=>{this._intervalValue=e.target.value}}
        />
        <wa-select
          aria-label=${this._localize("device.automation_action_delay_unit")}
          ?disabled=${this._saving}
          @change=${e=>{this._intervalUnit=e.target.value}}
        >
          ${["us","ms","s","min","h","d"].map(e=>(0,l.qy)`<wa-option value=${e} ?selected=${e===this._intervalUnit}
                >${this._localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
    </div>`}_renderTriggerRow(e){if(0===e.length)return(0,l.qy)`<p class="error">
        ${this._localize("device.automation_trigger_none_available")}
      </p>`;let t=e.find(e=>e.id===this._triggerId);return(0,l.qy)`<div class="field">
      <label class="field-label" id="trigger-label">
        ${this._localize("device.automation_wizard_pick_trigger")}
      </label>
      <wa-select
        aria-labelledby="trigger-label"
        value=${this._triggerId??""}
        ?disabled=${this._saving}
        @change=${e=>this._triggerId=e.target.value}
      >
        ${e.map(e=>(0,l.qy)`<wa-option value=${e.id} ?selected=${e.id===this._triggerId}>
              ${e.name}
            </wa-option>`)}
      </wa-select>
      ${t?.description?(0,l.qy)`<p class="field-desc">${(0,es.G)(t.description)}</p>`:l.s6}
    </div>`}_filteredTriggers(){let e=this._available?.triggers??[];if("device_on"===this._kind){let t=this._existingDeviceTriggers();return e.filter(e=>e.is_device_level&&!t.has(e.id))}if("component_on"===this._kind){if(!this._componentId)return[];let t=this._available?.devices.find(e=>e.id===this._componentId);if(!t)return[];let[i]=t.component_id.split("."),a=this._existingComponentTriggers(this._componentId);return e.filter(e=>!e.is_device_level&&(e.applies_to.includes(t.component_id)||e.applies_to.includes(i))&&(!a.has(this._bareTrigger(e.id))||e.repeatable))}return[]}_existingDeviceTriggers(){let e=new Set;for(let t of I(this.yaml))"esphome"===t.parentKey&&t.eventKey&&e.add(t.eventKey);return e}_existingComponentTriggers(e){let t=new Set;for(let i of I(this.yaml))i.id===e&&i.eventKey&&t.add(i.eventKey);return t}_bareTrigger(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_onKindChange(e){if(this._kind=e,this._triggerId=null,"component_on"===e){let e=this._available?.devices??[];this._componentId=e[0]?.id??""}else this._componentId=""}_onComponentChange(e){this._componentId=e,this._triggerId=null}_canContinue(){return"interval"===this._kind?""!==this._intervalValue.trim():!!this._triggerId&&("component_on"!==this._kind||!!this._componentId)}_buildLocation(){if("device_on"===this._kind)return{kind:"device_on",trigger:this._triggerId};if("component_on"===this._kind){let e=this._triggerId.indexOf("."),t=e>=0?this._triggerId.slice(e+1):this._triggerId,i=this._available?.triggers.find(e=>e.id===this._triggerId);if(i?.repeatable){let e=I(this.yaml).filter(e=>e.id===this._componentId&&e.eventKey===t).length;return{kind:"component_on",component_id:this._componentId,trigger:t,index:e}}return{kind:"component_on",component_id:this._componentId,trigger:t}}return{kind:"interval",index:I(this.yaml).filter(e=>"interval"===e.parentKey).length}}_catalogTriggerId(e){return"interval"===e.kind?null:this._triggerId}_dispatchAdded(e,t){let i=ef(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:eg(e)},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._kind="device_on",this._componentId="",this._triggerId=null,this._prefilled=!1,this._intervalValue="",this._intervalUnit="s",this._available=null,this._loading=!0,this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e=this._buildLocation(),t={trigger_id:this._catalogTriggerId(e),trigger_params:"interval"===this._kind?{interval:`${this._intervalValue.trim()}${this._intervalUnit}`}:{},actions:[]},{yaml_diff:i}=await this._api.upsertAutomation(this.configuration,t,e,this.yaml);this._dispatchAdded(e,i),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}ey.styles=[m.G,ed.z,ec],eb([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ey.prototype,"_localize",void 0),eb([(0,n.Fg)({context:u.Ie})],ey.prototype,"_api",void 0),eb([(0,d.MZ)()],ey.prototype,"boardName",void 0),eb([(0,d.MZ)()],ey.prototype,"configuration",void 0),eb([(0,d.MZ)()],ey.prototype,"yaml",void 0),eb([(0,d.MZ)({attribute:!1})],ey.prototype,"board",void 0),eb([(0,d.wk)()],ey.prototype,"_open",void 0),eb([(0,d.wk)()],ey.prototype,"_kind",void 0),eb([(0,d.wk)()],ey.prototype,"_componentId",void 0),eb([(0,d.wk)()],ey.prototype,"_triggerId",void 0),eb([(0,d.wk)()],ey.prototype,"_prefilled",void 0),eb([(0,d.wk)()],ey.prototype,"_intervalValue",void 0),eb([(0,d.wk)()],ey.prototype,"_intervalUnit",void 0),eb([(0,d.wk)()],ey.prototype,"_available",void 0),eb([(0,d.wk)()],ey.prototype,"_loading",void 0),eb([(0,d.wk)()],ey.prototype,"_saving",void 0),eb([(0,d.wk)()],ey.prototype,"_error",void 0),ey=eb([(0,d.EM)("esphome-add-automation-dialog")],ey);var ew=i(6848),e$=i(6016),ex=i(8851),ek=((r={}).SENSOR="sensor",r.BINARY_SENSOR="binary_sensor",r.SWITCH="switch",r.LIGHT="light",r.FAN="fan",r.COVER="cover",r.CLIMATE="climate",r.BUTTON="button",r.NUMBER="number",r.SELECT="select",r.TEXT="text",r.TEXT_SENSOR="text_sensor",r.LOCK="lock",r.VALVE="valve",r.MEDIA_PLAYER="media_player",r.SPEAKER="speaker",r.MICROPHONE="microphone",r.CAMERA="camera",r.DISPLAY="display",r.TOUCHSCREEN="touchscreen",r.OUTPUT="output",r.DATETIME="datetime",r.EVENT="event",r.UPDATE="update",r.ALARM="alarm_control_panel",r.CORE="core",r.BUS="bus",r.AUTOMATION="automation",r.OTA="ota",r.TIME="time",r.AUDIO_ADC="audio_adc",r.AUDIO_DAC="audio_dac",r.CANBUS="canbus",r.INFRARED="infrared",r.MEDIA_SOURCE="media_source",r.ONE_WIRE="one_wire",r.PACKET_TRANSPORT="packet_transport",r.STEPPER="stepper",r.WATER_HEATER="water_heater",r.MISC="misc",r.FEATURED="featured",r);let ez=["core","ota","update"];var eC=i(4117);async function eE(e,t){if(e._submitting)return;let i=e._selected;e._submitError="";let a=++e._depNavSeq,o=null;try{o=await (0,eC.Sn)(e._api,t,e.platform||void 0,e.board?.id??void 0)}catch{o=null}if(a===e._depNavSeq){if(i&&(e._returnTo=i,e._depDomain=t),o){e._selected=o;return}e._selected=null,await e.updateComplete,a===e._depNavSeq&&e._catalog?.filterByDomain(t)}}async function eA(e,t,i){let a=++e._selectionSeq,o=i??e.board?.id??void 0;try{let i=await (0,eC.Sn)(e._api,t,e.platform||void 0,o);if(a!==e._selectionSeq)return{kind:"stale"};if(!i)return{kind:"error",message:e._localize("device.add_component_error")};return{kind:"ok",entry:i}}catch(t){if(a!==e._selectionSeq)return{kind:"stale"};return{kind:"error",message:t instanceof Error?t.message:e._localize("device.add_component_error")}}}let eq=(0,l.AH)`
  esphome-base-dialog {
    --width: 900px;
  }

  esphome-base-dialog.form-view {
    --width: 480px;
  }

  /* Primary header + 40x40 close + .back-button come from
     primaryHeaderDialogStyles (dialog-chrome.ts). */
  esphome-base-dialog::part(body) {
    padding: var(--wa-space-l);
  }

  /* Breadcrumb that shows up while the user is detoured into
     "add a dependency" mid-way through adding another component.
     Tells them we'll bring them back to the original after. */
  .return-banner {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    background: var(--esphome-tint);
    border-left: 3px solid var(--esphome-primary);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
  }

  .return-banner strong {
    color: var(--wa-color-text-normal);
    font-weight: var(--wa-font-weight-semibold);
  }

  .bundle-banner {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-xs) var(--wa-space-s);
    background: var(--esphome-tint);
    border-left: 3px solid var(--esphome-primary);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-normal);
  }

  .bundle-banner wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  /* Surfaces a hydrate / WS-transport failure on the catalog
     view; the form's own banner is unreachable when _selected
     is still null. */
  .catalog-error {
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-xs) var(--wa-space-s);
    background: color-mix(in srgb, var(--wa-color-danger-60), transparent 88%);
    border-left: 3px solid var(--wa-color-danger-60);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
  }
`;class eS{hostConnected(){this._unsubscribe=(0,eC.Ej)(()=>{this._host.requestUpdate()})}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}resolve(e){return(0,eC.CQ)(e,this._getPlatform())?.name??e}kickoff(e){let t=this._getApi();if(!t)return;let i=this._getPlatform();for(let a of e)void 0===(0,eC.CQ)(a,i)&&(0,eC.Sn)(t,a,i).catch(()=>{})}constructor(e,t,i){this._host=e,this._getApi=t,this._getPlatform=i,e.addController(this)}}var eM=i(5957),eL=i(8175);let eP=(0,l.AH)`
  :host {
    display: block;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
  }

  .form-desc {
    margin: 0 0 var(--wa-space-m);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-xs);
  }

  label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  label .required {
    color: var(--esphome-error);
    margin-left: 2px;
  }

  select {
    width: 100%;
    padding: 9px 14px;
    font-size: var(--wa-font-size-s);
    font-family: inherit;
    color: var(--wa-color-text-normal);
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-l);
    box-sizing: border-box;
    outline: none;
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
  }

  select:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  select.invalid {
    border-color: var(--esphome-error);
  }

  select:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .field-error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-xs);
  }

  .array-row {
    display: flex;
    gap: var(--wa-space-xs);
  }

  .array-row input {
    flex: 1;
  }

  .array-btn {
    background: none;
    border: var(--wa-border-width-m) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    padding: 0 var(--wa-space-s);
    cursor: pointer;
    font-family: inherit;
    color: var(--wa-color-text-normal);
  }

  .array-btn:hover:not(:disabled) {
    background: var(--wa-color-surface-lowered);
  }

  .array-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .yaml-preview {
    margin: 0;
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    font-family: var(--wa-font-family-code, monospace);
    font-size: var(--wa-font-size-xs);
    white-space: pre;
    overflow-x: auto;
    color: var(--wa-color-text-normal);
  }

  .toggle-link {
    background: none;
    border: none;
    padding: 0;
    color: var(--esphome-primary);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    text-decoration: underline;
    align-self: flex-start;
  }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--wa-space-s);
    padding-top: var(--wa-space-m);
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    cursor: pointer;
    border: none;
    transition:
      background 0.12s,
      opacity 0.12s;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-secondary {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .btn-secondary:hover:not(:disabled) {
    background: var(--wa-color-surface-border);
  }

  .btn-primary {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--esphome-primary-hover);
  }

  .error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-s);
  }

  /* Banner shown when the component has unmet dependencies
     (e.g. a gpio light needs a configured output: first). */
  .deps-warning {
    display: flex;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: color-mix(in srgb, var(--esphome-warning, #d97706), transparent 88%);
    border: var(--wa-border-width-s) solid var(--esphome-warning, #d97706);
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-s);
    line-height: 1.45;
  }

  .deps-warning wa-icon {
    flex-shrink: 0;
    font-size: 20px;
    color: var(--esphome-warning, #d97706);
  }

  .deps-warning-body {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    flex: 1;
    min-width: 0;
  }

  .deps-warning-title {
    font-weight: var(--wa-font-weight-bold);
  }

  .deps-warning-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .dep-button {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    background: var(--esphome-warning, #d97706);
    color: var(--esphome-on-primary, white);
    border: none;
    border-radius: var(--wa-border-radius-m);
    font-family: inherit;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    cursor: pointer;
    transition: opacity 0.12s;
  }

  .dep-button:hover {
    opacity: 0.9;
  }
`;function eF(e){let t=e.key??(()=>""),i=new Map,a=new Map,o=new Set,r=0,n=()=>{for(let t of o)try{t()}catch(t){console.error(`${e.name} listener threw`,t)}};return{getCached:(...e)=>i.get(t(...e)),fetch(o,...s){let l,d=t(...s);if(i.has(d))return Promise.resolve(i.get(d));let c=a.get(d);if(c)return c;let h=r;try{l=e.fetch(o,...s)}catch(e){l=Promise.reject(e)}let p=l.then(e=>(h===r&&(i.set(d,e),a.delete(d),n()),e)).catch(t=>{if(h===r&&a.delete(d),void 0===e.fallback)throw t;let o=e.fallback(t);return h===r&&(i.set(d,o),n()),o});return a.set(d,p),p},update(e,...a){i.set(t(...a),e),n()},subscribe:e=>(o.add(e),()=>{o.delete(e)}),reset(){r+=1,i.clear(),a.clear(),o.clear()}}}let eT=eF({name:"pin-registry-modes",fetch:e=>e.getPinRegistryModes(),fallback:e=>(console.warn("pin-registry-modes fetch failed; Mode flags unscoped",e),Object.create(null))}),eR=new Set(["name"]);function eD(e,t){let i=t[e.key];if(e.type===y.Hh.NESTED)return e.multi_value?i instanceof ex.ho||Array.isArray(i)&&i.length>0:(0,eL.Qd)(i)?(e.config_entries??[]).some(e=>eD(e,i)):void 0!==i;return void 0!==i}function eI(e,t,i){let a=[];for(let o of e)if((0,eM.VP)(o,t,i.presentComponents,i.targetPlatform)&&(!o.advanced||i.showAdvanced||eD(o,t))){if(o.type===y.Hh.NESTED){if(!o.multi_value&&0===eI(o.config_entries??[],(0,eL.qY)(t[o.key]),i).length&&!eD(o,t))continue}else if(i.requiredOnly&&!o.required&&!eR.has(o.key))continue;a.push(o)}return a}var eO=i(2748);let ej=(0,l.AH)`
  :host {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
  }

  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .field-label .required {
    color: var(--esphome-error);
  }

  /* Indicator on featured-component fields the board has pinned to a
     fixed value. Sits next to the help-link icon. */
  .field-label .lock-icon {
    font-size: 13px;
    color: var(--wa-color-text-quiet);
  }

  .field-error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .field-description {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0;
  }

  .field-description + input,
  .field-description + textarea,
  .field-description + wa-select {
    margin-top: 8px;
  }

  /* Hint shown below a string/password input when the value is a
     !secret reference — clarifies that the field points into
     secrets.yaml instead of holding a literal value. */
  .secret-note {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .secret-note wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  .secret-note code {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-2xs);
    padding: 1px 4px;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .help-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    font-size: 16px;
    transition: color 0.12s;
    margin-left: auto;
  }

  .help-button:hover {
    color: var(--esphome-primary);
  }

  /* ─── Nested group ──────────────────────────────────────── */
  .nested-group {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
  }

  .nested-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .nested-enable {
    flex-shrink: 0;
  }

  .nested-toggle {
    display: flex;
    flex: 1;
    min-width: 0;
    align-items: center;
    gap: var(--wa-space-2xs);
    background: none;
    border: none;
    padding: 0;
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
    cursor: pointer;
    text-align: left;
  }

  .nested-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0;
  }

  .nested-toggle:hover {
    color: var(--esphome-primary);
  }

  .nested-toggle wa-icon {
    font-size: 18px;
  }

  .nested-title {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
  }

  .nested-platform {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-normal);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-default);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
    margin-left: var(--wa-space-xs);
  }

  .nested-fields {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    padding-top: var(--wa-space-xs);
  }

  /* ─── nested list (repeatable nested mapping) ───────────── */
  .nested-list {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  .nested-list-item {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-xs);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
  }

  .nested-list-item-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .nested-list-item-title {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  /* ─── multi-value rows ──────────────────────────────────── */
  .multi-row {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .multi-row .multi-input {
    flex: 1;
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    padding: 6px 12px;
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    outline: none;
    box-sizing: border-box;
    transition:
      border-color 0.12s,
      box-shadow 0.12s;
  }

  .multi-row .multi-input:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .multi-row .multi-input.invalid {
    border-color: var(--esphome-error);
  }

  .multi-row .multi-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .combobox-input {
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    padding: 6px 12px;
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    outline: none;
    box-sizing: border-box;
    transition:
      border-color 0.12s,
      box-shadow 0.12s;
  }

  .combobox-input:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .combobox-input.invalid {
    border-color: var(--esphome-error);
  }

  .combobox-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .multi-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 4px 10px;
    background: transparent;
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-quiet);
    font-family: inherit;
    font-size: var(--wa-font-size-xs);
    cursor: pointer;
    transition:
      background 0.12s,
      border-color 0.12s,
      color 0.12s;
  }

  .multi-btn:hover {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .multi-btn wa-icon {
    font-size: 14px;
  }

  .multi-add {
    align-self: flex-start;
    margin-top: var(--wa-space-2xs);
  }

  /* ─── Map (key/value) rows ──────────────────────────────── */
  .map-row {
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-2xs);
  }

  .map-row .map-key-input {
    flex: 1;
    min-width: 0;
  }

  .map-row .map-value {
    flex: 1.5;
    min-width: 0;
  }

  /* Inside a map row the value's label and description are
     redundant (the map itself has those at the top) — suppress
     them so each row stays compact. */
  .map-row .map-value > .field > label,
  .map-row .map-value > .field > p.field-description {
    display: none;
  }

  .map-row .map-value > .field {
    gap: 0;
  }

  /* "Complex value — edit in YAML" placeholder for map rows whose
     value isn't a primitive (lists / dicts can't round-trip through
     a single text input). Quiet, italic, padded to vertically
     match the size of a wa-input so the row alignment is preserved. */
  .map-row .map-value-yaml-only {
    margin: 0;
    padding: var(--wa-space-2xs) var(--wa-space-s);
    color: var(--wa-color-text-quiet);
    font-style: italic;
    font-size: var(--wa-font-size-s);
    line-height: var(--wa-form-control-line-height, 1.5);
  }

  /* Per-entry render-error tile. A renderer that throws (or
     receives a malformed entry shape) would otherwise leave a
     silent gap in the form — the user can't tell whether their
     data is gone or the form just doesn't show that field. The
     tile makes the failure visible with the entry's key/type
     and the error message so a user can report the problem
     instead of silently losing their work. */
  .render-error {
    display: flex;
    gap: var(--wa-space-s);
    align-items: flex-start;
    padding: var(--wa-space-s);
    border: 1px solid var(--wa-color-danger-fill-loud, currentColor);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-danger-fill-quiet, transparent);
    color: var(--wa-color-danger-on-quiet, currentColor);
  }
  .render-error wa-icon {
    flex-shrink: 0;
    margin-top: 2px;
  }
  .render-error > div {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    min-width: 0;
  }
  .render-error-key {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    opacity: 0.85;
  }
  .render-error-message {
    margin: 0;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    white-space: pre-wrap;
    word-break: break-word;
  }

  .textarea-field {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    padding: var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    resize: vertical;
    min-height: 80px;
  }

  .textarea-field.invalid {
    border-color: var(--esphome-error);
  }

  /* ─── Pin selector option layout ─────────────────────────── */
  .pin-option-stack {
    display: inline-flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.25;
  }

  .pin-option-primary {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .pin-option-secondary {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-style: italic;
  }

  .pin-option[disabled] .pin-option-primary,
  .pin-option[disabled] .pin-option-secondary {
    color: var(--wa-color-text-quiet);
  }

  .pin-warn-icon {
    color: var(--esphome-warning, #d97706);
    font-size: 14px;
    flex-shrink: 0;
  }

  .pin-option--warn .pin-option-secondary {
    color: var(--esphome-warning, #d97706);
    font-style: normal;
  }

  /* Section labels for the Recommended / Other pins groups in the GPIO
     picker (issue #1012). Presentational only — wa-select skips
     non-option children for selection / keyboard nav. */
  .pin-group-label {
    display: block;
    padding: var(--wa-space-2xs) var(--wa-space-s) 0;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--wa-color-text-quiet);
  }

  .pin-group-divider {
    margin: var(--wa-space-2xs) 0;
  }

  /* ─── Pin "Advanced" disclosure (long-form fields) ──────── */
  /* Compact toggle that opens the long-form pin fields (mode
     flags, inverted) attached by the catalog's
     _pin_long_form_extras helper. Visually subordinate to the
     primary GPIO picker — the user has to opt in to the
     advanced fields per pin. */
  .pin-advanced {
    margin-top: var(--wa-space-2xs);
  }

  .pin-advanced-toggle {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: none;
    border: none;
    padding: 2px 0;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-2xs);
    cursor: pointer;
  }

  .pin-advanced-toggle:hover {
    color: var(--wa-color-text-normal);
  }

  .pin-advanced-fields {
    margin-top: var(--wa-space-xs);
    padding-left: var(--wa-space-s);
    border-left: 2px solid var(--wa-color-surface-border);
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  /* ─── ID reference picker option layout ──────────────────── */
  .id-option-stack {
    display: inline-flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.25;
  }

  /* Visually distinguish the "Add new …" entry at the bottom of
     the dropdown — same pattern as Home Assistant's entity
     pickers. Coloured to read as an action, not a value. */
  .id-option-add {
    border-top: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    margin-top: var(--wa-space-2xs);
  }

  .id-option-add--solo {
    border-top: none;
    margin-top: 0;
  }

  .id-option-primary-add {
    color: var(--esphome-primary);
    font-weight: var(--wa-font-weight-bold);
  }

  .id-option-primary-add wa-icon {
    font-size: 14px;
  }

  .id-option-primary {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .id-option-secondary {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-style: italic;
  }

  .alert-entry {
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .label-entry {
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-subtle);
    font-style: italic;
  }

  .switch-field {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: var(--wa-space-m);
    row-gap: var(--wa-space-2xs);
    align-items: center;
  }

  .switch-field .field-info {
    grid-column: 1;
    grid-row: 1 / span 2;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .switch-field > .help-button {
    grid-column: 2;
    grid-row: 1;
    margin-left: 0;
    align-self: start;
  }

  .switch-field > wa-switch {
    grid-column: 2;
    grid-row: 2;
    justify-self: end;
  }

  .switch-field:not(:has(> .help-button)) > wa-switch {
    grid-row: 1 / span 2;
  }

  wa-select {
    width: 100%;
  }

  .float-with-unit-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .float-with-unit-inputs > input[type="number"] {
    flex: 1 1 auto;
    min-width: 0;
  }

  .float-with-unit-inputs > wa-select {
    flex: 0 0 auto;
    width: auto;
    min-width: 6rem;
  }

  /* Time-period field: numeric input + unit picker. Same layout
     as float_with_unit so the eye reads them as the same kind of
     compound control. */
  .time-period-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .time-period-inputs > input {
    flex: 1 1 auto;
    min-width: 0;
  }

  .time-period-inputs > wa-select {
    flex: 0 0 auto;
    width: auto;
    min-width: 6rem;
  }

  .float-with-unit-suffix {
    flex: 0 0 auto;
    color: var(--wa-color-text-subtle);
    font-size: var(--wa-font-size-s);
  }

  /* Templatable field wrapper — small literal/lambda tab strip
     above the active body. The toggle is a pair of buttons rather
     than a wa-tab-group to keep the markup leaf-cheap and the
     keyboard story explicit. */
  .templatable-field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
  }

  .templatable-toggle {
    display: inline-flex;
    align-self: flex-start;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    padding: 2px;
  }

  .templatable-toggle button {
    appearance: none;
    border: none;
    background: transparent;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    padding: 4px 10px;
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
  }

  .templatable-toggle button.active {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    box-shadow: var(--wa-shadow-xs);
  }

  .templatable-toggle button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  /* TRIGGER (action-list) field — a button that opens the automation
     editor for the field's bare action list (cover open_action, …),
     since the actions can't be edited inline as a single value. */
  .edit-actions-button {
    appearance: none;
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border: 1px solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-raised, transparent);
    color: var(--wa-color-text-normal);
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    cursor: pointer;
    transition: background 0.12s;
  }

  .edit-actions-button:hover:not(:disabled) {
    background: var(--wa-color-surface-lowered);
  }

  .edit-actions-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`,eN=(0,l.AH)`
  /* Brief glow when navigated to from the YAML cursor — mirrors the
     dashboard's just-added card flash. */
  .field--highlight {
    animation: field-highlight-glow 2s ease-out 1;
  }
  @keyframes field-highlight-glow {
    0% {
      box-shadow: 0 0 0 0 color-mix(in srgb, var(--esphome-primary), transparent 40%);
    }
    50% {
      box-shadow: 0 0 0 6px color-mix(in srgb, var(--esphome-primary), transparent 70%);
    }
    100% {
      box-shadow: 0 0 0 0 color-mix(in srgb, var(--esphome-primary), transparent 100%);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .field--highlight {
      animation: none;
    }
  }
`,eZ=[m.G,ed.z,ej,eN];function eB(e,t){return t.disabled||e.locked}(0,b.C)({"key-variant":s.mdiKeyVariant,"lock-outline":s.mdiLockOutline});let eK=e=>JSON.stringify(e),eU=e=>{try{let t=JSON.parse(e);if(Array.isArray(t))return t.map(String)}catch{}return e?e.split("."):[]},eH=/^!secret\s+(\S+)\s*$/;function eW(e,t){let i=e.match(eH);return i?(0,l.qy)`<span class="secret-note">
    <wa-icon library="mdi" name="key-variant"></wa-icon>
    <span>${t.localize("device.value_from_secret")}</span>
    <code>${i[1]}</code>
  </span>`:l.s6}function eV(e,t){if(e.translation_key){let i=e.translation_params||void 0,a=t(e.translation_key,i);if(a&&a!==e.translation_key)return a}return e.label?e.label:e.key.split("_").map(e=>e?e[0].toUpperCase()+e.slice(1):e).join(" ")}function eY(e,t){return eV(e,t.localize)}function eG(e,t){return e.help_link?(0,l.qy)`<a
    class="help-button"
    href=${e.help_link}
    target="_blank"
    rel="noreferrer"
    title=${t.localize("device.docs")}
  >
    <wa-icon library="mdi" name="open-in-new"></wa-icon>
  </a>`:l.s6}function eJ(e,t,i={}){let{includeHelpLink:a=!0}=i;return(0,l.qy)`
    <label class="field-label">
      ${eY(e,t)}
      ${e.required?(0,l.qy)`<span class="required">*</span>`:l.s6}
      ${e.locked?(0,l.qy)`<wa-icon
            class="lock-icon"
            library="mdi"
            name="lock-outline"
            title=${t.localize("device.field_locked_by_board")}
          ></wa-icon>`:l.s6}
      ${a&&e.help_link?eG(e,t):l.s6}
    </label>
    ${e.description?(0,l.qy)`<p class="field-description">${(0,es.G)(e.description)}</p>`:l.s6}
  `}function eQ(e,t){let i=t.errorAt(e);return(0,eO.O)(i?t.localize(i.code,i.params):void 0)}function eX(e,t,i,a,o=l.s6){return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)} ${a} ${o} ${eQ(t,i)}
    </div>
  `}function e0(e,t,i,a){return(0,eL.k4)(a)?null:(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <p class="field-description">${i.localize("device.value_yaml_only")}</p>
      ${eQ(t,i)}
    </div>
  `}function e1(e,t,i,a){var o,r,n,s,d,c;let h,p,u,m=a.getAt(i),v=e0(e,i,a,m);if(v)return v;let g=String(m??""),f=null!==a.errorAt(i),_=String(e.default_value??""),b=eB(e,a);return e.suggestions&&e.suggestions.length>0?(o=e,r=i,n=g,s=f,d=b,c=a,h=n.toLowerCase(),p=String(o.default_value??""),u=o.type===y.Hh.INTEGER||o.type===y.Hh.FLOAT,(0,l.qy)`
    <div class="field" data-field-key=${eK(r)}>
      ${eJ(o,c)}
      <wa-select
        class=${s?"invalid":""}
        ?disabled=${d}
        placeholder=${p}
        @change=${e=>c.emitChange(r,(e=>{if(!u||""===e)return e;let t=o.type===y.Hh.INTEGER?parseInt(e,10):Number(e);return Number.isFinite(t)?t:e})(e.target.value))}
      >
        ${(o.suggestions??[]).map(e=>{let t=String(e);return(0,l.qy)`<wa-option value=${t} ?selected=${t.toLowerCase()===h}
            >${t}</wa-option
          >`})}
      </wa-select>
      ${eQ(r,c)}
    </div>
  `):"password"===t?(0,l.qy)`
      <div class="field" data-field-key=${eK(i)}>
        ${eJ(e,a)}
        <esphome-password-input
          .value=${g}
          .invalid=${f}
          .disabled=${b}
          .placeholder=${_}
          @password-input-change=${e=>a.emitChange(i,e.detail.value)}
        ></esphome-password-input>
        ${eW(g,a)} ${eQ(i,a)}
      </div>
    `:(0,l.qy)`
    <div class="field" data-field-key=${eK(i)}>
      ${eJ(e,a)}
      <input
        type=${t}
        class=${f?"invalid":""}
        .value=${g}
        ?disabled=${b}
        placeholder=${_}
        @input=${e=>a.emitChange(i,e.target.value)}
      />
      ${eW(g,a)} ${eQ(i,a)}
    </div>
  `}let e2=["focusin","pointerdown","input","change"];class e6{hostConnected(){for(let e of e2)this.host.addEventListener(e,this._onInteraction)}hostDisconnected(){for(let e of e2)this.host.removeEventListener(e,this._onInteraction)}constructor(e){this.host=e,this._onInteraction=e=>{var t,i,a;let o=e.composedPath().find(e=>e instanceof HTMLElement&&e.hasAttribute("data-field-key"));if(!o)return;let r=o.getAttribute("data-field-key")??"";if(!r.startsWith("["))return;let n=eU(r);if(!n.length)return;let{emit:s,focusedKey:l}=(t=e.type,i=eK(n),a=this._focusedKey,"change"===t?{emit:i===a,focusedKey:a}:{emit:"focusin"===t||i!==a,focusedKey:i});this._focusedKey=l,s&&this.host.dispatchEvent(new CustomEvent("field-focus",{detail:{path:n},bubbles:!0,composed:!0}))},e.addController(this)}}let e3="field--highlight";class e4{maybeScroll(e){let t=this.host.focusFieldPath,i=t?.length?eK(t):void 0,a=e.has("focusFieldPath")||e.has("entries")||e.has("values"),{gate:o,scroll:r}=function(e,t,i){let{scrolledKey:a,lastFocusKey:o,tries:r}=e;t!==o&&(o=t,a=void 0,r=0);let n=!!t&&a!==t&&r<3&&i;return n&&r++,{gate:{scrolledKey:a,lastFocusKey:o,tries:r},scroll:n}}({scrolledKey:this._scrolledKey,lastFocusKey:this._lastFocusKey,tries:this._tries},i,a);this._scrolledKey=o.scrolledKey,this._lastFocusKey=o.lastFocusKey,this._tries=o.tries,r&&t?.length&&i&&this._scrollTo(t,i)}async _scrollTo(e,t){var i;let{host:a}=this;if(!a.shadowRoot)return;for(let t=1;t<e.length;t++)a.openNested(e.slice(0,t).join("."));for(let t of(i=this._gatingDecls(a.shadowRoot),i.filter(t=>t.prefix.length>0&&t.prefix.length<e.length&&t.prefix.every((t,i)=>t===e[i])).map(e=>e.key)))a.openNested(t);await a.updateComplete;let o=a.focusFieldPath;if(o&&eK(o)===t)for(let i=e.length;i>=1;i--){let o=this._find(a.shadowRoot,e.slice(0,i));if(!o)continue;o.scrollIntoView({block:"center"});let r=eK(e.slice(0,i)),n=Date.now();!window.matchMedia?.("(prefers-reduced-motion: reduce)").matches&&(r!==this._lastFlashKey||n-this._lastFlashAt>1e4)&&(this._lastFlashKey=r,this._lastFlashAt=n,o.classList.remove(e3),o.offsetWidth,o.classList.add(e3),o.addEventListener("animationend",()=>o.classList.remove(e3),{once:!0})),i===e.length&&(this._scrolledKey=t);return}}_gatingDecls(e){let t=[];for(let i of e.querySelectorAll("[data-reveal-for]")){let e=i.getAttribute("data-field-key");e&&t.push({prefix:eU(i.getAttribute("data-reveal-for")??""),key:e})}return t}_find(e,t){for(let i of e.querySelectorAll("[data-field-key]")){let e=eU(i.getAttribute("data-field-key")??"");if(e.length===t.length&&e.every((e,i)=>e===t[i]))return i}for(let i of e.querySelectorAll("*")){if(!i.localName.includes("-"))continue;let e=i.shadowRoot,a=e?this._find(e,t):null;if(a)return a}return null}constructor(e){this.host=e,this._lastFlashAt=0,this._tries=0}}i(1062),i(6135);var e5=i(9665);let e8=(0,l.AH)`
  :host {
    display: block;
    position: relative;
  }

  /* Trigger — shaped like the project's standard input */
  .trigger {
    width: 100%;
    box-sizing: border-box;
    min-height: var(--wa-form-control-height);
    padding: 0 14px;
    font-size: var(--wa-font-size-s);
    font-family: inherit;
    line-height: var(--wa-form-control-value-line-height);
    color: var(--wa-color-text-normal);
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    outline: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    text-align: left;
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
  }

  .trigger:focus,
  :host([open]) .trigger {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .trigger.invalid {
    border-color: var(--esphome-error);
  }

  .trigger.invalid:focus {
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--esphome-error), transparent 80%);
  }

  .trigger:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .trigger-icon {
    width: 22px;
    height: 22px;
    flex: 0 0 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-s);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .trigger-icon svg {
    width: 16px;
    height: 16px;
  }

  .trigger-icon--empty {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-quiet);
  }

  .trigger-label {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-family: var(--wa-font-family-code, monospace);
    font-size: var(--wa-font-size-s);
  }

  .trigger-label.placeholder {
    color: var(--wa-color-text-quiet);
    font-family: inherit;
  }

  .trigger-clear {
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-s);
  }

  .trigger-clear:hover {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .trigger-chevron {
    width: 14px;
    height: 14px;
    color: var(--wa-color-text-quiet);
    flex: 0 0 14px;
    transition: transform 0.15s;
  }

  :host([open]) .trigger-chevron {
    transform: rotate(180deg);
  }

  /* Panel */
  .panel {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    max-height: 380px;
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    box-shadow:
      0 8px 24px rgba(0, 0, 0, 0.12),
      0 2px 6px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    animation: panelIn 0.12s ease-out;
  }

  @keyframes panelIn {
    from {
      opacity: 0;
      transform: translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .search {
    position: relative;
    padding: 10px 12px;
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .search-icon {
    position: absolute;
    left: 22px;
    top: 50%;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    color: var(--wa-color-text-quiet);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    box-sizing: border-box;
    padding: 7px 10px 7px 32px !important;
    min-height: 32px !important;
    font-size: var(--wa-font-size-s);
  }

  .grid-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
    gap: 4px;
  }

  .icon-cell {
    position: relative;
    aspect-ratio: 1;
    background: none;
    border: 1px solid transparent;
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--wa-color-text-normal);
    padding: 0;
    transition:
      background 0.1s,
      border-color 0.1s,
      color 0.1s,
      transform 0.08s;
  }

  .icon-cell svg {
    width: 20px;
    height: 20px;
  }

  .icon-cell:hover {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-color: var(--esphome-tint-border);
    transform: scale(1.06);
  }

  .icon-cell--selected {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .icon-cell--selected:hover {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    transform: scale(1.06);
  }

  .empty,
  .loading {
    padding: 24px 16px;
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .footer {
    padding: 6px 12px;
    border-top: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-name {
    font-family: var(--wa-font-family-code, monospace);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-xs);
  }
`;function e9(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({close:s.mdiClose,magnify:s.mdiMagnify,palette:s.mdiPalette});let e7=null;function te(e){return e?e.startsWith("mdi:")?e.slice(4):e:""}class tt extends l.WF{connectedCallback(){super.connectedCallback(),document.addEventListener("click",this._onDocumentClick,!0)}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("click",this._onDocumentClick,!0)}willUpdate(e){e.has("_open")&&this._escape.set(this._open),e.has("value")&&!this._loaded&&te(this.value)&&this._ensureCatalogLoaded()}async _toggle(){this.disabled||(this._open?this._close():await this._openPanel())}async _openPanel(){this._open=!0,this.setAttribute("open",""),await this._ensureCatalogLoaded(),await this.updateComplete,this._searchInput?.focus()}async _ensureCatalogLoaded(){this._loaded||(this._catalog=await (e7||(e7=(async()=>{let e=await Promise.resolve().then(i.bind(i,9165)),t=[];for(let[i,a]of Object.entries(e)){if(!i.startsWith("mdi")||"string"!=typeof a)continue;let e=i.slice(3);if(!e)continue;let o=e.replace(/^[A-Z]/,e=>e.toLowerCase()).replace(/([A-Z])/g,"-$1").replace(/_/g,"-").toLowerCase();t.push({name:o,path:a})}return t.sort((e,t)=>e.name.localeCompare(t.name)),t})().catch(e=>(console.error("[mdi-icon-picker] failed to load catalog:",e),e7=null,[])))),this._loaded=!0)}_close(){this._open=!1,this.removeAttribute("open"),this._query=""}_select(e){let t=`mdi:${e}`;this.value=t,this.dispatchEvent(new CustomEvent("change",{detail:{value:t},bubbles:!0,composed:!0})),this._close()}_clear(e){e.stopPropagation(),this.value="",this.dispatchEvent(new CustomEvent("change",{detail:{value:""},bubbles:!0,composed:!0}))}_onSearchInput(e){this._query=e.target.value}_renderTriggerIcon(){let e=te(this.value);if(!e)return(0,l.qy)`<span class="trigger-icon trigger-icon--empty">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${s.mdiPalette}></path>
        </svg>
      </span>`;let t=this._catalog.find(t=>t.name===e);return t?(0,l.qy)`<span class="trigger-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${t.path}></path>
        </svg>
      </span>`:(0,l.qy)`<span class="trigger-icon">
      <wa-icon library="mdi" name=${e} style="font-size: 16px;"></wa-icon>
    </span>`}_renderPanel(){if(!this._loaded)return(0,l.qy)`<div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="loading">Loading icons…</div>
      </div>`;let e=function(e,t){if(!t)return e.slice(0,400);let i=t.trim().toLowerCase().replace(/\s+/g,"-");if(!i)return e.slice(0,400);let a=[],o=[],r=[];for(let t of e)if(t.name===i?a.push(t):t.name.startsWith(i)?o.push(t):t.name.includes(i)&&r.push(t),a.length+o.length+r.length>=800)break;return[...a,...o,...r].slice(0,400)}(this._catalog,this._query),t=te(this.value);return(0,l.qy)`
      <div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="search">
          <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d=${s.mdiMagnify}></path>
          </svg>
          <input
            type="text"
            class="search-input"
            placeholder="Search ${this._catalog.length.toLocaleString()} icons…"
            .value=${this._query}
            @input=${this._onSearchInput}
            @keydown=${t=>{"Enter"===t.key&&e.length>0&&(t.preventDefault(),this._select(e[0].name))}}
          />
        </div>
        <div class="grid-wrap">
          ${0===e.length?(0,l.qy)`<div class="empty">
                <wa-icon library="mdi" name="magnify" style="font-size: 24px;"></wa-icon>
                No icons match “${this._query}”
              </div>`:(0,l.qy)`<div class="grid">
                ${e.map(e=>(0,l.qy)`
                    <button
                      type="button"
                      class=${e.name===t?"icon-cell icon-cell--selected":"icon-cell"}
                      title=${`mdi:${e.name}`}
                      @click=${()=>this._select(e.name)}
                    >
                      <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path fill="currentColor" d=${e.path}></path>
                      </svg>
                    </button>
                  `)}
              </div>`}
        </div>
        <div class="footer">
          <span>
            ${0===e.length?"No matches":e.length>=400?`400+ of ${this._catalog.length.toLocaleString()}`:`${e.length} of ${this._catalog.length.toLocaleString()}`}
          </span>
          ${t?(0,l.qy)`<span class="footer-name">mdi:${t}</span>`:l.s6}
        </div>
      </div>
    `}render(){let e=te(this.value),t=`trigger${this.invalid?" invalid":""}`;return(0,l.qy)`
      <button
        type="button"
        class=${t}
        ?disabled=${this.disabled}
        @click=${this._toggle}
      >
        ${this._renderTriggerIcon()}
        <span class=${e?"trigger-label":"trigger-label placeholder"}>
          ${e?`mdi:${e}`:this.placeholder}
        </span>
        ${e&&!this.disabled?(0,l.qy)`<span
              class="trigger-clear"
              role="button"
              tabindex="-1"
              title="Clear"
              @click=${this._clear}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
                <path fill="currentColor" d=${s.mdiClose}></path>
              </svg>
            </span>`:l.s6}
        <svg class="trigger-chevron" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M7,10L12,15L17,10H7Z"></path>
        </svg>
      </button>
      ${this._open?this._renderPanel():l.s6}
    `}constructor(...e){super(...e),this.value="",this.placeholder="Choose an icon…",this.invalid=!1,this.disabled=!1,this._open=!1,this._catalog=[],this._query="",this._loaded=!1,this._escape=new e5.u(this,e=>{e.stopPropagation(),this._close()},{target:document}),this._onDocumentClick=e=>{!this._open||e.composedPath().includes(this)||this._close()}}}tt.styles=[ed.z,e8],e9([(0,d.MZ)()],tt.prototype,"value",void 0),e9([(0,d.MZ)()],tt.prototype,"placeholder",void 0),e9([(0,d.MZ)({type:Boolean})],tt.prototype,"invalid",void 0),e9([(0,d.MZ)({type:Boolean})],tt.prototype,"disabled",void 0),e9([(0,d.wk)()],tt.prototype,"_open",void 0),e9([(0,d.wk)()],tt.prototype,"_catalog",void 0),e9([(0,d.wk)()],tt.prototype,"_query",void 0),e9([(0,d.wk)()],tt.prototype,"_loaded",void 0),e9([(0,d.P)(".search-input")],tt.prototype,"_searchInput",void 0),tt=e9([(0,d.EM)("esphome-mdi-icon-picker")],tt);let ti=/^\s*(?:GPIO)?(\d+)\s*$/i,ta=/^\s*P(\d+)\.(\d+)\s*$/i,to=/^\s*P(\d+)\s*$/i,tr=/^\s*PA(\d+)\s*$/i,tn=/^\s*PB(\d+)\s*$/i;function ts(e){if("number"==typeof e&&Number.isFinite(e))return e;if("string"==typeof e){let t=e.match(ti);if(t)return Number(t[1]);let i=e.match(ta);if(i&&32>Number(i[2]))return 32*Number(i[1])+Number(i[2]);let a=e.match(tr);if(a)return Number(a[1]);let o=e.match(tn);if(o)return 16+Number(o[1]);let r=e.match(to);if(r)return Number(r[1])}return null===e||"object"!=typeof e||Array.isArray(e)?null:ts(e.number)}function tl(e,t){return"nrf52"===t?`P${Math.floor(e/32)}.${e%32}`:"bk72xx"===t?`P${e}`:`GPIO${e}`}let td=/GPIO(\d+)/gi,tc=/\bP(?:A(\d+)|B(\d+)|(\d+)\.(\d+)|(\d+))\b/gi;function th(e){let t,i;return{get(a){if(void 0!==t&&e(a,t))return i},set(e,a){t=e,i=a},clear(){t=void 0,i=void 0}}}let tp=th((e,t)=>e.yaml===t.yaml&&e.excludeFromLine===t.excludeFromLine&&e.excludeToLine===t.excludeToLine),tu=new Set(["name","friendly_name","comment"]),tm=/^(\s*)(?:-\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*:/,tv=/:\s*[|>][+-]?\d*\s*(?:#.*)?$/,tg=e=>e.length-e.trimStart().length,tf=th((e,t)=>e.yaml===t.yaml&&e.domain===t.domain),t_="__esphome_add_new__",tb={INPUT:{input:!0},OUTPUT:{output:!0},INPUT_PULLUP:{input:!0,pullup:!0},OUTPUT_OPEN_DRAIN:{output:!0,open_drain:!0},INPUT_PULLDOWN_16:{input:!0,pulldown:!0},INPUT_PULLDOWN:{input:!0,pulldown:!0},INPUT_OUTPUT_OPEN_DRAIN:{input:!0,output:!0,open_drain:!0}};function ty(e){let t=tb[e.toUpperCase()];return t?{...t}:null}let tw=new WeakMap;function t$(e,t,i){let a=i.getAt(t);if(!e.multi_value&&("string"==typeof a||"number"==typeof a||"boolean"==typeof a))return(0,l.qy)`
      <div class="field" data-field-key=${eK(t)}>
        ${eJ(e,i)}
        <p class="field-description">
          ${i.localize("device.value_set_in_yaml",{value:String(a)})}
        </p>
        ${eQ(t,i)}
      </div>
    `;let o=t.join("."),r=i.nestedOpenSections.has(o),n=i.requiredOnly?!r:r,s=i.filterRenderable(e.config_entries??[],i.scopeValues(t)),d=null!=e.platform_type&&!e.required,c=d&&(0,ex.$z)(i.getAt(t)),h=eY(e,i),p=i.localize("device.enable_entity",{name:h});return(0,l.qy)`
    <div class="nested-group" data-field-key=${eK(t)}>
      <div class="nested-header">
        ${d?(0,l.qy)`<wa-switch
              class="nested-enable"
              .checked=${c}
              ?disabled=${eB(e,i)}
              aria-label=${p}
              title=${p}
              @change=${e=>(function(e,t,i,a,o,r){let n,s=((n=tw.get(r.stashOwner))||(n=new Map,tw.set(r.stashOwner,n)),n);if(a){let a=s.get(t);a&&(0,ex.$z)(a)?(s.delete(t),r.emitChange(e,a)):r.emitChange([...e,"name"],o),i||r.toggleNested(t)}else{let a=r.getAt(e);(0,eL.Qd)(a)&&(0,ex.$z)(a)&&s.set(t,a),r.emitChange(e,void 0),i&&r.toggleNested(t)}})(t,o,n,e.target.checked,h,i)}
            ></wa-switch>`:l.s6}
        <button
          type="button"
          class="nested-toggle"
          aria-expanded=${n}
          @click=${()=>i.toggleNested(o)}
        >
          <wa-icon library="mdi" name=${n?"chevron-up":"chevron-down"}></wa-icon>
          <span class="nested-title">${h}</span>
          ${e.platform_type?(0,l.qy)`<span class="nested-platform">${e.platform_type}</span>`:l.s6}
        </button>
        ${eG(e,i)}
      </div>
      ${e.description?(0,l.qy)`<p class="nested-desc">${(0,es.G)(e.description)}</p>`:l.s6}
      ${n?(0,l.qy)`<div class="nested-fields">
            ${s.map(e=>i.renderEntry(e,[...t,e.key]))}
          </div>`:l.s6}
    </div>
  `}var tx=i(2477),tk=i(7169),tz=i(5490);let tC=new WeakMap;function tE(e){return null==e||""===e?"":(0,tz.uS)(e)||String(e)}let tA=["us","ms","s","min","h","d"],tq=RegExp(`^\\d+(?:\\.\\d+)?(?:${tA.map(e=>e.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|")})$`);function tS(e){if(null==e||""===e)return{value:"",unit:"s",parseable:!0};let t=String(e).trim(),i=t.match(/^(\d+(?:\.\d+)?)(us|ms|s|min|h|d)?$/);if(i){let[,e,t]=i;return{value:e,unit:t??"s",parseable:!0}}return{value:t,unit:"s",parseable:!1}}function tM(e,t){let i=e.trim();return""===i?"":`${i}${t}`}function tL(e,t,i){let a=i.getAt(t),o=e0(e,t,i,a);if(o)return o;let r=null==a?e.default_value:a,n=!0===(0,ex.FY)(r);return(0,l.qy)`
    <div class="switch-field" data-field-key=${eK(t)}>
      <div class="field-info">${eJ(e,i,{includeHelpLink:!1})}</div>
      ${eG(e,i)}
      <wa-switch
        ?checked=${n}
        ?disabled=${eB(e,i)}
        aria-label=${eY(e,i)}
        @change=${e=>i.emitChange(t,e.target.checked)}
      ></wa-switch>
    </div>
  `}function tP(e,t){return(0,l.qy)`<wa-option
    class=${e.warn?"pin-option pin-option--warn":"pin-option"}
    value=${e.optValue}
    .label=${e.primary}
    ?selected=${e.optValue===t}
    ?disabled=${e.reserved}
    title=${e.titleText}
  >
    <span class="pin-option-stack">
      <span class="pin-option-primary">
        ${e.primary}
        ${e.warn?(0,l.qy)`<wa-icon
              class="pin-warn-icon"
              library="mdi"
              name="alert-circle-outline"
            ></wa-icon>`:l.s6}
      </span>
      ${e.secondary?(0,l.qy)`<span class="pin-option-secondary">${e.secondary}</span>`:l.s6}
    </span>
  </wa-option>`}function tF(e,t){let i=e.getAt(t);return Array.isArray(i)?i:[]}function tT(e,t,i){return{addItem:()=>e.emitChange(t,[...tF(e,t),i()]),removeAt:i=>e.emitChange(t,tF(e,t).filter((e,t)=>t!==i))}}function tR(e,t){return 0===e.length?(0,l.qy)`<p class="field-description">${t.localize("device.multi_value_empty")}</p>`:l.s6}function tD(e,t,i){return(0,l.qy)`
    <button
      type="button"
      class="multi-btn"
      ?disabled=${t}
      aria-label=${e.localize("device.multi_value_remove")}
      @click=${i}
    >
      <wa-icon library="mdi" name="close"></wa-icon>
    </button>
  `}function tI(e,t,i){return(0,l.qy)`
    <button
      type="button"
      class="multi-btn multi-add"
      ?disabled=${t}
      @click=${i}
    >
      <wa-icon library="mdi" name="plus"></wa-icon>
      ${e.localize("device.multi_value_add")}
    </button>
  `}var tO=i(8067);let tj=new(i(2741)).E({name:"automation-body-cache",bucketKey:()=>"",cacheMisses:!1,fetch:(e,t)=>{let i=t.map(e=>{let t=e.indexOf("/");return{type:e.slice(0,t),id:e.slice(t+1)}});return e.getAutomationBodies(i)}});function tN(e,t,i){return tj.fetch(e,`${t}/${i}`,void 0)}async function tZ(e,t,i,a=tN){let o=await a(e,t,i.id);if(o&&"config_entries"in o)return i.config_entries=structuredClone(o.config_entries),"ok";let r=null===o?"no body returned":"body shape missing config_entries";return console.warn(`automation-body: ${t}/${i.id} ${r}; form will render empty`),null===o?"missingBody":"missingField"}function tB(){return{succeeded:0,missingBody:0,missingField:0,rejected:0}}function tK(e,t){e["ok"===t?"succeeded":t]++}function tU(e,t){return`${e??""}|${t??""}`}let tH={triggers:eF({name:"automation-catalog-cache:triggers",key:tU,fetch:(e,t,i)=>e.getAutomationTriggers(t,i)}),actions:eF({name:"automation-catalog-cache:actions",key:tU,fetch:(e,t,i)=>e.getAutomationActions(t,i)}),conditions:eF({name:"automation-catalog-cache:conditions",key:tU,fetch:(e,t,i)=>e.getAutomationConditions(t,i)}),light_effects:eF({name:"automation-catalog-cache:light_effects",key:tU,fetch:(e,t,i)=>e.getLightEffects(t,i)}),filters:eF({name:"automation-catalog-cache:filters",key:tU,fetch:(e,t,i)=>e.getFilters(t,i)})};function tW(e,t){return tH.triggers.getCached(e,t)}async function tV(e,t,i){let a=await tH.light_effects.fetch(e,t,i);return tG("light_effects",t,i,a,t=>tQ(e,"light_effects",t))}async function tY(e,t,i){let a=await tH.filters.fetch(e,t,i);return tG("filters",t,i,a,t=>tQ(e,"filters",t))}async function tG(e,t,i,a,o){if(0===(await o(a)).succeeded)return a;let r=[...a];return tH[e].update(r,t,i),r}let tJ=new WeakSet;async function tQ(e,t,i){let a=tB(),o=i.filter(e=>!tJ.has(e));if(0===o.length)return a;for(let i of(await Promise.allSettled(o.map(async i=>{let o=await tZ(e,t,i);"ok"===o&&tJ.add(i),tK(a,o)}))))"rejected"===i.status&&(a.rejected++,console.warn(`${t} hydration failed`,i.reason));let r=a.missingBody+a.missingField+a.rejected;return r>0&&console.warn(`${t} hydration: ${a.succeeded} ok, ${r} failed (missingBody=${a.missingBody}, missingField=${a.missingField}, rejected=${a.rejected})`),a}function tX(e){let t=Object.values(tH).map(t=>t.subscribe(e));return()=>{for(let e of t)e()}}function t0(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}function t1(e){let t=Object.keys(e);return 1===t.length?t[0]:""}function t2(e){return e?e.replace(/_/g," ").replace(/\b\w/g,e=>e.toUpperCase()):""}let t6={time_period:y.Hh.TIME_PERIOD,float:y.Hh.FLOAT,integer:y.Hh.INTEGER,string:y.Hh.STRING,lambda:y.Hh.LAMBDA},t3={light_effects:{cache:()=>tH.light_effects.getCached(void 0,void 0),fetch:e=>tV(e),parentToken:e=>e,dedupByTypeId:!0},filter:{cache:()=>tH.filters.getCached(void 0,void 0),fetch:e=>tY(e),parentToken:e=>e.split(".",1)[0],dedupByTypeId:!1}};function t4(e){return Array.isArray(e)?e:[]}function t5(e){let t=[],i=[];return e.forEach((e,a)=>{!(null===e||"object"!=typeof e||Array.isArray(e))&&Object.keys(e).length<=1&&(t.push(e),i.push(a))}),{items:t,positions:i}}class t8 extends l.WF{connectedCallback(){super.connectedCallback();let e=this._ops();if(null===e)return;this._unsubscribe=tX(()=>{if(!this.isConnected)return;let e=this._ops();if(null===e)return;let t=e.cache();void 0!==t&&(this._catalog=t,this._fetchError=!1)});let t=e.cache();this._fetchError=!1,void 0!==t?this._catalog=t:this._kickFetch(e)}updated(){if(this._kickedFetch||null!==this._catalog||this._fetchError||!this._api)return;let e=this._ops();null!==e&&void 0===e.cache()&&this._kickFetch(e)}_kickFetch(e){this._api&&(this._kickedFetch=!0,e.fetch(this._api).catch(e=>{console.error("Failed to fetch registry catalog",e),this.isConnected&&(this._fetchError=!0)}))}_ops(){return t3[this.entry?.registry??""]??null}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe?.(),this._unsubscribe=void 0,this._kickedFetch=!1}render(){let e=this._ops();if(null===e)return(0,l.qy)`
        <div class="field" data-field-key=${eK(this.path)}>
          ${eJ(this.entry,this.ctx)}
          <p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_unsupported")}
          </p>
          ${eQ(this.path,this.ctx)}
        </div>
      `;let t=this.ctx.getAt(this.path);if(t instanceof ex.ho||void 0!==t&&!Array.isArray(t))return(0,l.qy)`
        <div class="field" data-field-key=${eK(this.path)}>
          ${eJ(this.entry,this.ctx)}
          <p class="field-description">
            ${this.ctx.localize("device.multi_value_yaml_only")}
          </p>
          ${eQ(this.path,this.ctx)}
        </div>
      `;let{items:i}=t5(t4(t)),a=eB(this.entry,this.ctx),o=this.ctx.sectionKey?e.parentToken(this.ctx.sectionKey):"",r=(this._catalog??[]).filter(e=>!o||0===e.applies_to.length||e.applies_to.includes(o)),n=null!==this._catalog&&0===this._catalog.length,s=this._fetchError?(0,l.qy)`<p class="registry-list-fallback">
          ${this.ctx.localize("device.registry_list_error")}
          ${this._api?(0,l.qy)`<button type="button" class="multi-btn" @click=${this._retryFetch}>
                ${this.ctx.localize("device.registry_list_retry")}
              </button>`:l.s6}
        </p>`:null===this._catalog?(0,l.qy)`<p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_loading")}
          </p>`:n?(0,l.qy)`<p class="registry-list-fallback">
              ${this.ctx.localize("device.registry_list_empty_catalog")}
            </p>`:0===r.length?(0,l.qy)`<p class="registry-list-fallback">
                ${this.ctx.localize("device.registry_list_no_applicable_options")}
              </p>`:l.s6,d=a||0===r.length;return(0,l.qy)`
      <div class="field" data-field-key=${eK(this.path)}>
        ${eJ(this.entry,this.ctx)} ${tR(i,this.ctx)}
        ${s}
        ${i.map((t,o)=>this._renderRow(t,o,r,i,a,e.dedupByTypeId))}
        ${tI(this.ctx,d,()=>this._addItem())}
        ${eQ(this.path,this.ctx)}
      </div>
    `}_renderRow(e,t,i,a,o,r){let n=t1(e),s=new Set;r&&a.forEach((e,i)=>{if(i===t)return;let a=t1(e);a&&s.add(a)});let d=i.find(e=>e.id===n),c=void 0!==d,h=[...i].sort((e,t)=>e.id.localeCompare(t.id)),p=n?e[n]:null,u=null!==p&&"object"==typeof p&&!Array.isArray(p)&&!(0,tO.b)(p)&&!(p instanceof ex.ho),m=u?null:this._scalarDispatchType(d,p),v=(null===p||u)&&d?.config_entries?d.config_entries:[];return(0,l.qy)`
      <div class="registry-list-item" data-row-index=${t}>
        <div class="registry-list-row">
          <wa-select
            .value=${n}
            ?disabled=${o}
            placeholder=${this.ctx.localize("device.registry_list_select")}
            aria-label=${this.ctx.localize("device.registry_list_row_label",{index:String(t+1)})}
            @change=${e=>{let i=e.target.value;this._renameRow(t,i)}}
          >
            ${!c&&n?(0,l.qy)`<wa-option value=${n} selected
                  >${t2(n)}</wa-option
                >`:l.s6}
            ${h.filter(e=>e.id===n||!s.has(e.id)).map(e=>(0,l.qy)`<wa-option value=${e.id} ?selected=${e.id===n}
                    >${t2(e.id)}</wa-option
                  >`)}
          </wa-select>
          ${tD(this.ctx,o,()=>this._removeAt(t))}
        </div>
        ${this._renderSubForm(t,n,m,v)}
      </div>
    `}_mutateEditable(e){let t=t4(this.ctx.getAt(this.path)),{items:i,positions:a}=t5(t),o=e(i);this.ctx.emitChange(this.path,function(e,t,i){let a=[...e];if(t.forEach((e,t)=>{t<i.length&&(a[e]=i[t])}),i.length<t.length)for(let e of t.slice(i.length).reverse())a.splice(e,1);else if(i.length>t.length){let e=t.length>0?t[t.length-1]+1:a.length;a.splice(e,0,...i.slice(t.length))}return a}(t,a,o))}_scalarDispatchType(e,t){let i=e?.value_type;return i&&Object.prototype.hasOwnProperty.call(t6,i)?t6[i]:"string"==typeof t&&tq.test(t.trim())?y.Hh.TIME_PERIOD:null}_renderSubForm(e,t,i,a){return null!==i?(0,l.qy)`<div class="registry-list-sub-form">
        ${this.ctx.renderEntry(w({type:i}),[...this.path,String(e),t])}
      </div>`:a.length>0?(0,l.qy)`<div class="registry-list-sub-form">
        ${a.map(i=>this.ctx.renderEntry(i,[...this.path,String(e),t,i.key]))}
      </div>`:l.s6}_addItem(){this._mutateEditable(e=>[...e,{}])}_removeAt(e){this._mutateEditable(t=>t.filter((t,i)=>i!==e))}_renameRow(e,t){this._mutateEditable(i=>{if(!t)return i;let a=i[e];return a&&t1(a)!==t?i.map((i,a)=>a===e?{[t]:null}:i):i})}constructor(...e){super(...e),this.path=[],this._catalog=null,this._fetchError=!1,this._kickedFetch=!1,this._retryFetch=()=>{if(!this._api)return;let e=this._ops();null!==e&&(this._fetchError=!1,e.fetch(this._api).catch(e=>{console.error("Failed to retry registry catalog fetch",e),this.isConnected&&(this._fetchError=!0)}))}}}t8.styles=[...eZ,(0,l.AH)`
      :host {
        display: block;
      }
      .registry-list-item {
        margin-bottom: 1rem;
      }
      .registry-list-row {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin-bottom: 0.5rem;
      }
      .registry-list-row wa-select {
        flex: 1;
      }
      .registry-list-sub-form {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-left: 1rem;
        padding-left: 1rem;
        border-left: 2px solid var(--wa-color-surface-border);
      }
      .registry-list-fallback {
        color: var(--wa-color-neutral-fill-loud);
        font-size: 0.9rem;
      }
    `],t0([(0,n.Fg)({context:u.Ie})],t8.prototype,"_api",void 0),t0([(0,d.MZ)({attribute:!1})],t8.prototype,"entry",void 0),t0([(0,d.MZ)({attribute:!1})],t8.prototype,"path",void 0),t0([(0,d.MZ)({attribute:!1})],t8.prototype,"ctx",void 0),t0([(0,d.wk)()],t8.prototype,"_catalog",void 0),t0([(0,d.wk)()],t8.prototype,"_fetchError",void 0),t8=t0([(0,d.EM)("esphome-registry-list")],t8);var t9=i(5230),t7=i(5659),ie=i(5874),it=i(3107),ii=i(792),ia=i(2727),io=i(924);function ir(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}class is extends l.WF{render(){return(0,l.qy)`<div class="cm-wrap ${this.invalid?"invalid":""}"></div>`}firstUpdated(){this._mountEditor()}updated(e){if(this._view&&(e.has("_darkMode")&&this._view.dispatch({effects:this._themeCompartment.reconfigure(this._darkMode?io.Ts:io.jL)}),e.has("disabled")&&this._view.dispatch({effects:this._editableCompartment.reconfigure(ii.Lz.editable.of(!this.disabled))}),e.has("value"))){let e=this._view.state.doc.toString();e!==this.value&&this._view.dispatch({changes:{from:0,to:e.length,insert:this.value}})}}disconnectedCallback(){super.disconnectedCallback(),this._view?.destroy(),this._view=null}_mountEditor(){this._view=new ii.Lz({state:it.$t.create({doc:this.value,extensions:[ia.oQ,(0,t7.I)(),ie.Xt.of("  "),ii.w4.of([t9.Yc]),this._editableCompartment.of(ii.Lz.editable.of(!this.disabled)),this._themeCompartment.of(this._darkMode?io.Ts:io.jL),ii.Lz.theme({"&":{height:"100%"}}),ii.Lz.updateListener.of(e=>{if(e.docChanged){let t=e.state.doc.toString();this.dispatchEvent(new CustomEvent("lambda-change",{detail:{value:t},bubbles:!0,composed:!0}))}})]}),parent:this._container})}constructor(...e){super(...e),this._darkMode=!1,this.value="",this.disabled=!1,this.invalid=!1,this.placeholder="",this._view=null,this._themeCompartment=new it.xx,this._editableCompartment=new it.xx}}function il(e,t,i){var a;let o=(a=i.getAt(t),(0,tO.b)(a)?a._lambda:a instanceof ex.ho?a.body:null==a?"":String(a)),r=null!==i.errorAt(t),n=eB(e,i);return eX(e,t,i,(0,l.qy)`<esphome-lambda-editor
      .value=${o}
      .invalid=${r}
      ?disabled=${n}
      placeholder=${String(e.default_value??"")}
      @lambda-change=${e=>i.emitChange(t,{_lambda:e.detail.value})}
    ></esphome-lambda-editor>`)}is.styles=(0,l.AH)`
    :host {
      display: block;
    }
    .cm-wrap {
      border: 1px solid var(--wa-color-neutral-border-quiet, #d1d5db);
      border-radius: 6px;
      overflow: hidden;
      min-height: 96px;
    }
    .cm-wrap.invalid {
      border-color: var(--wa-color-danger-fill-loud, #d92d20);
    }
    :host([disabled]) .cm-wrap {
      opacity: 0.6;
    }
    .cm-editor {
      font-family: "JetBrains Mono", "Fira Code", monospace;
      font-size: 13px;
      min-height: 96px;
      max-height: 320px;
    }
    .cm-editor .cm-scroller {
      overflow: auto;
    }
    .cm-editor.cm-focused {
      outline: 2px solid var(--wa-color-brand-fill-loud, #0b5cad);
      outline-offset: -1px;
    }
  `,ir([(0,n.Fg)({context:u.B6,subscribe:!0}),(0,d.wk)()],is.prototype,"_darkMode",void 0),ir([(0,d.MZ)()],is.prototype,"value",void 0),ir([(0,d.MZ)({type:Boolean,reflect:!0})],is.prototype,"disabled",void 0),ir([(0,d.MZ)({type:Boolean})],is.prototype,"invalid",void 0),ir([(0,d.MZ)()],is.prototype,"placeholder",void 0),ir([(0,d.P)(".cm-wrap")],is.prototype,"_container",void 0),is=ir([(0,d.EM)("esphome-lambda-editor")],is);let id=new WeakMap;function ic(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(8944),(0,b.C)({"alert-circle-outline":s.mdiAlertCircleOutline,"chevron-down":s.mdiChevronDown,"chevron-up":s.mdiChevronUp,close:s.mdiClose,"open-in-new":s.mdiOpenInNew,plus:s.mdiPlus});class ih extends l.WF{render(){let e=this._buildCtx(),t=this._filterRenderable(this.entries,this.values);return(0,l.qy)`${t.map(t=>this._renderEntry(t,t.key?[t.key]:[],e))}`}connectedCallback(){var e;super.connectedCallback(),this._unsubPinRegistryModes=(e=()=>this.requestUpdate(),eT.subscribe(e))}disconnectedCallback(){super.disconnectedCallback(),this._unsubPinRegistryModes?.(),this._unsubPinRegistryModes=void 0}willUpdate(e){e.has("entries")&&void 0!==e.get("entries")&&(this._pendingUnits.clear(),this._editingMagnitudes.clear(),this._seededNestedOpen.clear())}_pathOf(e){return eU(e.getAttribute("data-field-key")??"")}updated(e){if(super.updated(e),this._syncSelectValues(),this._fieldScroll.maybeScroll(e),this._api&&!this._pinRegistryModesKicked){var t;this._pinRegistryModesKicked=!0,t=this._api,eT.fetch(t)}}async _syncSelectValues(){if(this.shadowRoot)for(let e of this.shadowRoot.querySelectorAll("[data-field-key]")){let t=e.querySelector("wa-select");if(!t)continue;if(t.hasAttribute("data-no-value-sync")){await this._syncSelectedAttr(t);continue}if(t.updateComplete)try{await t.updateComplete}catch{}let i=this._pathOf(e);if(!i.length)continue;let a=(0,eL.O6)(this.values,i);if(!(0,eL.k4)(a)){""!==(Array.isArray(t.value)?t.value[0]??"":t.value??"")&&(t.value="");continue}let o=String(a??""),r=Array.from(t.querySelectorAll("wa-option")),n=o.match(/^\s*(?:GPIO)?(\d+)\s*$/i)?.[1],s=e=>r.find(t=>t.value?.toLowerCase()===e.toLowerCase()),l=o?s(o)??(n?s(`GPIO${n}`):void 0):null,d=l?.value??o;(Array.isArray(t.value)?t.value[0]??"":t.value??"")!==d&&(t.value=d)}}async _syncSelectedAttr(e){if(e.updateComplete)try{await e.updateComplete}catch{}let t=e.querySelector("wa-option[selected]"),i=t?.value??"";i&&(Array.isArray(e.value)?e.value[0]??"":e.value??"")!==i&&(e.value=i)}_renderEntry(e,t,i){try{return this._renderEntryUnsafe(e,t,i)}catch(a){console.error("esphome-config-entry-form: render failed for entry",{key:e.key,type:e.type,path:t},a);let i=a instanceof Error?a.message:String(a);return(0,l.qy)`<div class="render-error" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div>
          <strong> ${this._localize("device.entry_render_error_title")} </strong>
          <code class="render-error-key"
            >${e.key||"(empty key)"} · ${e.type}</code
          >
          <pre class="render-error-message">${i}</pre>
        </div>
      </div>`}}_renderEntryUnsafe(e,t,i){var a,o;if(e.templatable&&(a=e.type)!==y.Hh.NESTED&&a!==y.Hh.MAP&&a!==y.Hh.DIVIDER&&a!==y.Hh.LABEL&&a!==y.Hh.ALERT){let a,r,n,s,d,c,h,p;return o=()=>this._renderEntryLeaf(e,t,i),a=i.getAt(t),r=(0,tO.b)(a),(n=id.get(i.stashOwner))||(n=new Map,id.set(i.stashOwner,n)),s=t.join("."),(d=n.get(s))||(d={},n.set(s,d)),c=d,h=eK(t),p=e=>{e!==r&&(r?(c.lambda=(0,tO.b)(a)?a._lambda:"",i.emitChange(t,c.literal??"")):(c.literal=a,i.emitChange(t,{_lambda:c.lambda??""})))},(0,l.qy)`
    <div class="templatable-field" data-field-key=${h}>
      <div
        class="templatable-toggle"
        role="tablist"
        aria-label=${i.localize("device.automation_literal")}
      >
        <button
          type="button"
          role="tab"
          class=${!r?"active":""}
          aria-selected=${!r}
          ?disabled=${i.disabled}
          @click=${()=>p(!1)}
        >
          ${i.localize("device.automation_literal")}
        </button>
        <button
          type="button"
          role="tab"
          class=${r?"active":""}
          aria-selected=${r}
          ?disabled=${i.disabled}
          @click=${()=>p(!0)}
        >
          ${i.localize("device.automation_lambda")}
        </button>
      </div>
      ${r?il(e,t,i):o()}
    </div>
  `}return this._renderEntryLeaf(e,t,i)}_renderEntryLeaf(e,t,i){if(e.type===y.Hh.DIVIDER)return(0,l.qy)`<wa-divider></wa-divider>`;if(e.type===y.Hh.LABEL)return(0,l.qy)`<p class="label-entry">${eY(e,i)}</p>`;if(e.type===y.Hh.ALERT)return(0,l.qy)`<div class="alert-entry">${eY(e,i)}</div>`;if(e.type===y.Hh.NESTED)return e.multi_value?function(e,t,i){let a=i.getAt(t);if(a instanceof ex.ho)return(0,l.qy)`
      <div class="nested-list" data-field-key=${eK(t)}>
        ${eJ(e,i)}
        <p class="field-description">${i.localize("device.multi_value_yaml_only")}</p>
        ${eQ(t,i)}
      </div>
    `;let o=(0,eL.ly)(a),r=eB(e,i),{addItem:n,removeAt:s}=tT(i,t,()=>({})),d=eY(e,i),c=e.config_entries??[];return(0,l.qy)`
    <div class="nested-list" data-field-key=${eK(t)}>
      ${eJ(e,i)} ${tR(o,i)}
      ${o.map((e,a)=>{let o=[...t,String(a)],n=i.filterRenderable(c,e);return(0,l.qy)`
          <div class="nested-list-item" data-field-key=${eK(o)}>
            <div class="nested-list-item-header">
              <span class="nested-list-item-title"> ${d} ${a+1} </span>
              ${tD(i,r,()=>s(a))}
            </div>
            <div class="nested-fields">
              ${n.map(e=>i.renderEntry(e,[...o,e.key]))}
            </div>
          </div>
        `})}
      ${tI(i,r,n)} ${eQ(t,i)}
    </div>
  `}(e,t,i):t$(e,t,i);if(e.type===y.Hh.MAP){let a,o,r,n,s,d;return a=(e.config_entries??[])[0],n=Object.keys(r=(o=i.getAt(t))&&"object"==typeof o&&!Array.isArray(o)?o:{}),s=eB(e,i),d=()=>{let e=i.getAt(t);return e&&"object"==typeof e&&!Array.isArray(e)?Object.assign(Object.create(null),e):Object.create(null)},(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      ${0===n.length?(0,l.qy)`<p class="field-description">${i.localize("device.map_empty")}</p>`:l.s6}
      ${n.map(e=>{let o,n;return o=[...t,e],n=!(0,eL.k4)(r[e]),(0,l.qy)`
      <div class="map-row" data-field-key=${eK(o)}>
        <input
          type="text"
          class="multi-input map-key-input"
          .value=${e}
          ?disabled=${s}
          @change=${a=>((e,a)=>{if(e===a||!a)return;let o=i.getAt(t);if(!o||"object"!=typeof o||Array.isArray(o)||a in o)return;let r=Object.create(null);for(let[t,i]of Object.entries(o))r[t===e?a:t]=i;i.emitChange(t,r)})(e,a.target.value)}
        />
        <div class="map-value">
          ${n?(0,l.qy)`<p class="map-value-yaml-only">
                ${i.localize("device.map_value_edit_in_yaml")}
              </p>`:a?i.renderEntry(a,o):l.s6}
        </div>
        <button
          type="button"
          class="multi-btn"
          ?disabled=${s}
          aria-label=${i.localize("device.map_remove")}
          @click=${()=>{let a;e in(a=d())&&(delete a[e],i.emitChange(t,a))}}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </div>
    `})}
      <button
        type="button"
        class="multi-btn multi-add"
        ?disabled=${s}
        @click=${()=>{let e=d(),a=1;for(;`new_${a}`in e;)a++;e[`new_${a}`]="",i.emitChange(t,e)}}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${i.localize("device.map_add")}
      </button>
      ${eQ(t,i)}
    </div>
  `}if(e.type===y.Hh.REGISTRY_LIST)return(0,l.qy)`<esphome-registry-list
    .entry=${e}
    .path=${t}
    .ctx=${i}
  ></esphome-registry-list>`;if(e.multi_value)return function(e,t,i){let a=tF(i,t).map(e=>String(e)),o=null!==i.errorAt(t),r=eB(e,i),{addItem:n,removeAt:s}=tT(i,t,()=>"");return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)} ${tR(a,i)}
      ${a.map((e,a)=>(0,l.qy)`
          <div class="multi-row">
            <input
              type="text"
              class="multi-input ${o?"invalid":""}"
              .value=${e}
              ?disabled=${r}
              @input=${e=>{var o;let r;return o=e.target.value,void((r=[...tF(i,t)])[a]=o,i.emitChange(t,r))}}
            />
            ${tD(i,r,()=>s(a))}
          </div>
        `)}
      ${tI(i,r,n)} ${eQ(t,i)}
    </div>
  `}(e,t,i);if(e.references_component)return function(e,t,i){let a=e.references_component||"",o=function(e,t){if(!t)return[];let i={yaml:e,domain:t},a=tf.get(i);if(a)return a;let o=e.split("\n"),r=[],n=!1,s="",l="",d=()=>{s&&r.push({id:s,name:l}),s="",l=""};for(let e of o){let i=e.match(/^([a-zA-Z_][a-zA-Z0-9_]*):/);if(i){d(),n=i[1]===t;continue}if(!n)continue;/^\s*-\s/.test(e)&&d();let a=e.match(/^\s+(?:-\s+)?id:\s*["']?(\S+?)["']?\s*$/);if(a){s=a[1];continue}let o=e.match(/^\s+(?:-\s+)?name:\s*["']?(.+?)["']?\s*$/);o&&(l=o[1])}return d(),tf.set(i,r),r}(i.yaml,a),r=i.getAt(t),n=e0(e,t,i,r);if(n)return n;let s=String(r??""),d=null!==i.errorAt(t),c=0===o.length,h=e=>{let o=e.target,r=o.value;if(r===t_){o.value=s,i.requestAddComponent(a);return}i.emitChange(t,r)},p=(0,l.qy)`
    <wa-option
      class="id-option id-option-add ${c?"id-option-add--solo":""}"
      value=${t_}
    >
      <span class="id-option-stack">
        <span class="id-option-primary id-option-primary-add">
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${i.localize("device.id_reference_add",{domain:a})}
        </span>
      </span>
    </wa-option>
  `;return c?(0,l.qy)`
      <div class="field" data-field-key=${eK(t)}>
        ${eJ(e,i)}
        <wa-select
          class=${d?"invalid":""}
          ?disabled=${eB(e,i)}
          placeholder=${i.localize("device.id_reference_empty",{domain:a})}
          @change=${h}
        >
          ${p}
        </wa-select>
        ${eQ(t,i)}
      </div>
    `:(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <wa-select
        class=${d?"invalid":""}
        ?disabled=${eB(e,i)}
        @change=${h}
      >
        ${o.map(e=>(0,l.qy)`<wa-option
              class="id-option"
              value=${e.id}
              .label=${e.name||e.id}
              ?selected=${e.id===s}
            >
              <span class="id-option-stack">
                <span class="id-option-primary">${e.name||e.id}</span>
                <span class="id-option-secondary"
                  >${e.name?`${e.id} \xb7 ${a}`:a}</span
                >
              </span>
            </wa-option>`)}
        ${p}
      </wa-select>
      ${eQ(t,i)}
    </div>
  `}(e,t,i);if(e.options&&e.options.length>0)return function(e,t,i){let a=i.getAt(t),o=e0(e,t,i,a);if(o)return o;let r=String(a??""),n=null!==i.errorAt(t),s=eB(e,i);if(e.suggestions&&e.suggestions.length>0){let a=r.toLowerCase();return(0,l.qy)`
      <div class="field" data-field-key=${eK(t)}>
        ${eJ(e,i)}
        <wa-select
          class=${n?"invalid":""}
          ?disabled=${s}
          placeholder=${String(e.default_value??"")}
          @change=${e=>i.emitChange(t,e.target.value)}
        >
          ${e.suggestions.map(e=>{let t=String(e);return(0,l.qy)`<wa-option value=${t} ?selected=${t.toLowerCase()===a}
              >${t}</wa-option
            >`})}
        </wa-select>
        ${eQ(t,i)}
      </div>
    `}if(e.allow_custom_value&&e.options&&e.options.length>0){let a=`combobox-${t.join("-")}`;return(0,l.qy)`
      <div class="field" data-field-key=${eK(t)}>
        ${eJ(e,i)}
        <input
          type="text"
          class="combobox-input ${n?"invalid":""}"
          list=${a}
          .value=${r}
          ?disabled=${s}
          placeholder=${String(e.default_value??"")}
          @input=${e=>i.emitChange(t,e.target.value)}
        />
        <datalist id=${a}>
          ${e.options.map(e=>(0,l.qy)`<option value=${e.value}>${e.label}</option>`)}
        </datalist>
        ${eQ(t,i)}
      </div>
    `}let d=r.toLowerCase(),c=null!=e.default_value?String(e.default_value):"",h=e.options?.find(e=>e.value.toLowerCase()===c.toLowerCase()),p=h?.label??c,{clearable:u,visibleOptions:m}=function(e){let t=tC.get(e);if(!t){let i=e.options??[];t={clearable:i.some(e=>""===e.value),visibleOptions:i.filter(e=>""!==e.value)},tC.set(e,t)}return t}(e);return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <wa-select
        class=${n?"invalid":""}
        ?disabled=${s}
        .withClear=${u}
        placeholder=${p}
        @change=${e=>i.emitChange(t,e.target.value)}
      >
        ${u?(0,l.qy)`<wa-icon slot="clear-icon" library="mdi" name="close"></wa-icon>`:l.s6}
        ${m.map(e=>(0,l.qy)`<wa-option
              value=${e.value}
              ?selected=${e.value.toLowerCase()===d}
              >${e.label}</wa-option
            >`)}
      </wa-select>
      ${eQ(t,i)}
    </div>
  `}(e,t,i);switch(e.type){case y.Hh.BOOLEAN:return tL(e,t,i);case y.Hh.SELECT:return e1(e,"text",t,i);case y.Hh.SECURE_STRING:return e1(e,"password",t,i);case y.Hh.INTEGER:case y.Hh.FLOAT:return function(e,t,i){if(e.suggestions&&e.suggestions.length>0)return e1(e,"number",t,i);let a=i.getAt(t),o=e0(e,t,i,a);if(o)return o;if("hex"===e.display_format){var r,n,s;let a,o,d,c,h;return r=e,n=t,a=(s=i).getAt(n),o=null!==s.errorAt(n),d=eB(r,s),c=s.getEditingMagnitude(n)??tE(a),h=tE(r.default_value),eX(r,n,s,(0,l.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${o?"invalid":""}
      .value=${c}
      ?disabled=${d}
      placeholder=${h}
      @input=${e=>{let t=e.target.value;(s.setEditingMagnitude(n,t),""===t)?s.emitChange(n,""):s.emitChange(n,(0,tz.uS)((0,tz.EG)(t))||t)}}
      @blur=${()=>s.clearEditingMagnitude(n)}
    />`)}let d=String(a??""),c=null!==i.errorAt(t),h=e.range?String(e.range[0]):void 0,p=e.range?String(e.range[1]):void 0,u=eB(e,i);return eX(e,t,i,(0,l.qy)`<input
      type="number"
      class=${c?"invalid":""}
      .value=${d}
      ?disabled=${u}
      min=${h??""}
      max=${p??""}
      step=${e.type===y.Hh.FLOAT?"any":"1"}
      placeholder=${String(e.default_value??"")}
      @input=${e=>{let a=e.target.value;i.emitChange(t,""===a?"":Number(a))}}
    />`)}(e,t,i);case y.Hh.FLOAT_WITH_UNIT:return function(e,t,i){let a=e.unit_options??[],o=a[0]??"",r=i.getAt(t),n=e0(e,t,i,r);if(n)return n;let s=(0,tk.Eb)(r,a),d=i.getEditingMagnitude(t)??(null===s.value?"":String(s.value)),c=(0,tk.E3)(r,e.default_value,i.getPendingUnit(t),a),h=(0,tk.x9)(e.default_value,a),p=null!==i.errorAt(t),u=eB(e,i),m=c===o,v=e.range&&m?String(e.range[0]):void 0,g=e.range&&m?String(e.range[1]):void 0,f=e=>i.emitChange(t,(0,tk.BR)(e));return(0,l.qy)`
    <div class="field float-with-unit" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <div class="float-with-unit-inputs">
        <input
          type="number"
          class=${p?"invalid":""}
          .value=${d}
          ?disabled=${u}
          min=${(0,tx.J)(v)}
          max=${(0,tx.J)(g)}
          step="any"
          placeholder=${h}
          @input=${e=>{let a=e.target.value;i.setEditingMagnitude(t,a),""===a&&i.setPendingUnit(t,c);let o=""===a?null:Number(a);f({value:Number.isFinite(o)?o:null,unit:c})}}
          @blur=${()=>i.clearEditingMagnitude(t)}
        />
        ${a.length>1?(0,l.qy)`
              <wa-select
                data-no-value-sync
                ?disabled=${u}
                @change=${e=>{let a=e.target.value;null===s.value?i.setPendingUnit(t,a):f({value:s.value,unit:a})}}
              >
                ${a.map(e=>(0,l.qy)`<wa-option value=${e} ?selected=${e===c}
                      >${e}</wa-option
                    >`)}
              </wa-select>
            `:(0,l.qy)`<span class="float-with-unit-suffix">${c}</span>`}
      </div>
      ${eQ(t,i)}
    </div>
  `}(e,t,i);case y.Hh.TIME_PERIOD:return function(e,t,i){let a=i.getAt(t),o=e0(e,t,i,a);if(o)return o;let r=tS(a),n=null!==i.errorAt(t),s=eB(e,i);if(!r.parseable)return e1(e,"text",t,i);let d=void 0!==e.default_value&&null!==e.default_value?tS(e.default_value):null,c=d&&d.parseable?d.value:"",h=null!=a&&""!==a?r.unit:d?.parseable?d.unit:r.unit;return(0,l.qy)`
    <div class="field time-period" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <div class="time-period-inputs">
        <input
          type="text"
          inputmode="decimal"
          class=${n?"invalid":""}
          .value=${r.value}
          ?disabled=${s}
          placeholder=${c}
          @input=${e=>{let a=e.target.value;i.emitChange(t,tM(a,h))}}
        />
        <wa-select
          data-no-value-sync
          ?disabled=${s}
          @change=${e=>{let a=e.target.value;i.emitChange(t,tM(r.value,a))}}
        >
          ${tA.map(e=>(0,l.qy)`<wa-option value=${e} ?selected=${e===h}
                >${i.localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
      ${eQ(t,i)}
    </div>
  `}(e,t,i);case y.Hh.PIN:return function(e,t,i){if(!i.board||0===i.board.pins.length)return e1(e,"text",t,i);let a=i.getAt(t),o=ts(a),r=i.board.esphome.platform,n=null!==o?tl(o,r):(0,eL.k4)(a)?String(a??""):"",s=null!==i.errorAt(t),d=i.board.pins;if(e.suggestions&&e.suggestions.length>0){let t=new Set(e.suggestions.map(ts).filter(e=>null!==e));if(t.size>0){let e=d.filter(e=>t.has(e.gpio));e.length>0&&(d=e)}}null!==o&&!d.some(e=>e.gpio===o)&&i.board.pins.some(e=>e.gpio===o)&&(d=[i.board.pins.find(e=>e.gpio===o),...d]);let c=function(e,t,i){let a={yaml:e,excludeFromLine:t,excludeToLine:i},o=tp.get(a);if(o)return o;let r=new Map;if(!e)return r;let n=e.split("\n"),s="",l=-1;for(let e=0;e<n.length;e++){let a=n[e],o=a.match(/^([a-zA-Z_][a-zA-Z0-9_]*):/);if(o){s=o[1],l=-1;continue}let d=e+1;if(void 0!==t&&void 0!==i&&d>=t&&d<=i||!s)continue;if(l>=0){if(""===a.trim()||tg(a)>l)continue;l=-1}let c=a.match(tm);if(c&&tu.has(c[2].toLowerCase())){tv.test(a)&&(l=c[1].length);continue}for(let e of function(e){let t=[];for(let i of e.matchAll(td))t.push(Number(i[1]));for(let i of e.matchAll(tc))if(void 0!==i[1])t.push(Number(i[1]));else if(void 0!==i[2])t.push(16+Number(i[2]));else if(void 0!==i[3]&&void 0!==i[4]){let e=Number(i[4]);e<32&&t.push(32*Number(i[3])+e)}else void 0!==i[5]&&t.push(Number(i[5]));return t}(function(e){let t=e.match(/(^|\s)#/);return null===t?e:e.slice(0,(t.index??0)+t[1].length)}(a)))r.has(e)||r.set(e,s)}return tp.set(a,r),r}(i.yaml,i.fromLine,function(e,t){if(void 0===t)return;let i=e.split("\n");for(let e=t;e<i.length;e++){let t=i[e];if(""!==t&&/^[a-zA-Z]/.test(t))return e}return i.length}(i.yaml,i.fromLine)),h=eB(e,i),p=(0,eL.Qd)(a);return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <wa-select
        data-no-value-sync
        class=${s?"invalid":""}
        ?disabled=${h}
        @change=${e=>{let a=e.target.value;p?i.emitChange([...t,"number"],a):i.emitChange(t,a)}}
      >
        ${function(e,t,i,a,o){let r=[],n=[],s=[];for(let a of e){let e=function(e,t,i,a){let o=tl(e.gpio,a.board?.esphome.platform),r=e.label||o,n=e.occupied_by||"",s=i.get(e.gpio)||"",l=(t.pin_mode===y.l3.OUTPUT||t.pin_mode===y.l3.INPUT_OUTPUT)&&e.features.includes(y.k6.INPUT_ONLY),d=(t.pin_features??[]).every(t=>e.features.includes(t)),c=!1===e.available,h=!!(n||s),p=n?a.localize("device.pin_occupied_by",{name:n}):s?a.localize("device.pin_used_by",{name:s}):"",u=l?a.localize("device.pin_input_only"):"",m=e.notes||(c?a.localize("device.pin_unavailable"):""),v=[];return e.label&&e.label!==o&&v.push(o),p&&v.push(p),u&&v.push(u),m&&v.push(m),{optValue:o,primary:r,secondary:v.join(" • "),titleText:[p,u,m].filter(Boolean).join(" — "),warn:h||l,reserved:c,supported:d&&!l}}(a,t,i,o);(e.reserved?s:e.supported?r:n).push(e)}let d=r.length>0&&n.length>0,c=(t.pin_features??[]).map(e=>e.toUpperCase()).join(", "),h=(e,t)=>(0,l.qy)`${t?(0,l.qy)`<wa-divider class="pin-group-divider" aria-hidden="true"></wa-divider>`:l.s6} <small class="pin-group-label" aria-hidden="true">${e}</small>`;return(0,l.qy)`
    ${d&&c?h(o.localize("device.pin_group_supports",{features:c}),!1):l.s6}
    ${r.map(e=>tP(e,a))}
    ${d?h(o.localize("device.pin_group_other"),!0):l.s6}
    ${n.map(e=>tP(e,a))}
    ${s.length>0?h(o.localize("device.pin_group_reserved"),!0):l.s6}
    ${s.map(e=>tP(e,a))}
  `}(d,e,c,n,i)}
      </wa-select>
      ${eQ(t,i)}
      ${function(e,t,i,a,o,r){let n=i.filterRenderable(e.config_entries??[],i.scopeValues(t));if(0===n.length)return l.s6;let s=`${t.join(".")}:pin-advanced`,d=i.scopeValues(t);o&&Object.keys(d).some(e=>"number"!==e&&void 0!==d[e])&&i.seedNestedOpen(s);let c=i.nestedOpenSections.has(s);return(0,l.qy)`
    <div
      class="pin-advanced"
      data-field-key="${s}"
      data-reveal-for="${eK(t)}"
    >
      <button
        type="button"
        class="pin-advanced-toggle"
        aria-expanded=${c}
        ?disabled=${r}
        @click=${()=>{!r&&(i.toggleNested(s),c||o||null==a||""===a||i.emitChange(t,{number:a}))}}
      >
        <wa-icon library="mdi" name=${c?"chevron-up":"chevron-down"}></wa-icon>
        <span>${i.localize("device.pin_advanced")}</span>
      </button>
      ${c?(0,l.qy)`<div class="pin-advanced-fields">
            ${n.map(e=>(function(e,t,i){var a,o,r,n,s,l,d,c;let h,p,u,m,v,g,f;if("mode"!==e.key||e.type!==y.Hh.NESTED)return i.renderEntry(e,[...t,e.key]);let _=[...t,e.key],b=i.getAt(_),w=function(e,t){if(!t||!(0,eL.Qd)(e))return null;for(let i of Object.keys(e))if(Object.prototype.hasOwnProperty.call(t,i)){let e=t[i];return e.length>0?e:null}return null}(i.getAt(t),i.pinRegistryModes),$=w?(o=e,h=new Set([...w,..."string"==typeof(a=b)?Object.keys(ty(a)??{}):(0,eL.Qd)(a)?Object.keys(a):[]]),p=(o.config_entries??[]).filter(e=>h.has(e.key)),{...o,config_entries:p}):e;return"string"==typeof b?(r=$,n=_,(m="string"==typeof(u=(s=i).getAt(n))?ty(u):null)?t$(r,n,(l=s,d=n,c=m,v=d.join("."),g=e=>e.length===d.length+1&&e.slice(0,d.length).join(".")===v?e[d.length]:null,(f={...l,getAt:e=>{if(e.join(".")===v)return c;let t=g(e);return null!==t?c[t]:l.getAt(e)},scopeValues:e=>e.join(".")===v?{...c}:l.scopeValues(e),emitChange:(e,t)=>{let i=g(e);if(null===i)return void l.emitChange(e,t);let a={...c};t?a[i]=!0:delete a[i],l.emitChange(d,a)}}).renderEntry=(e,t)=>e.type===y.Hh.BOOLEAN?tL(e,t,f):l.renderEntry(e,t),f)):t$(r,n,s)):i.renderEntry($,_)})(e,t,i))}
          </div>`:l.s6}
    </div>
  `}(e,t,i,a,p,h)}
    </div>
  `}(e,t,i);case y.Hh.COLOR:return e1(e,"color",t,i);case y.Hh.MAC_ADDRESS:return e1(e,"text",t,i);case y.Hh.LAMBDA:return il(e,t,i);case y.Hh.JSON:return function(e,t,i){let a=i.getAt(t),o=a instanceof ex.ho;if(!o){let o=e0(e,t,i,a);if(o)return o}let r=o?a.body:String(a??""),n=null!==i.errorAt(t);return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <textarea
        class="textarea-field ${n?"invalid":""}"
        rows="4"
        ?disabled=${eB(e,i)}
        .value=${r}
        placeholder=${String(e.default_value??"")}
        @input=${e=>{let r=e.target.value;i.emitChange(t,o?ex.ho.fromBodyText(r,a):r)}}
      ></textarea>
      ${eQ(t,i)}
    </div>
  `}(e,t,i);case y.Hh.ICON:let a=i.getAt(t),o=e0(e,t,i,a);if(o)return o;let r=String(a??""),n=null!==i.errorAt(t);return(0,l.qy)`
    <div class="field" data-field-key=${eK(t)}>
      ${eJ(e,i)}
      <esphome-mdi-icon-picker
        .value=${r}
        .invalid=${n}
        .disabled=${eB(e,i)}
        .placeholder=${String(e.default_value??"Choose an icon…")}
        @change=${e=>i.emitChange(t,e.detail.value)}
      ></esphome-mdi-icon-picker>
      ${eQ(t,i)}
    </div>
  `;case y.Hh.TRIGGER:return(0,l.qy)`<div class="field" data-field-key=${eK(t)}>
          ${eY(e,i)}
          <button
            type="button"
            class="edit-actions-button"
            ?disabled=${i.disabled}
            @click=${()=>this._emitEditActionField(e.key)}
          >
            ${i.localize("device.automation_action_field_edit")}
          </button>
        </div>`;default:return e1(e,"text",t,i)}}_buildCtx(){let e={localize:this._localize,disabled:this.disabled,yaml:this.yaml,fromLine:this.fromLine,sectionKey:this.sectionKey,board:this.board,pinRegistryModes:eT.getCached(),requiredOnly:this.requiredOnly,nestedOpenSections:this._nestedOpenSections,getAt:e=>(0,eL.O6)(this.values,e),errorAt:e=>this.errors.get(e.join("."))??null,emitChange:(e,t)=>this._emitChange(e,t),toggleNested:e=>this._toggleNested(e),seedNestedOpen:e=>this._seedNestedOpen(e),requestAddComponent:e=>this._requestAddComponent(e),scopeValues:e=>this._scopeValues(e),filterRenderable:this._filterRenderable,getPendingUnit:e=>this._pendingUnits.get(e.join(".")),setPendingUnit:(e,t)=>{this._pendingUnits.set(e.join("."),t),this.requestUpdate()},getEditingMagnitude:e=>this._editingMagnitudes.get(e.join(".")),setEditingMagnitude:(e,t)=>{this._editingMagnitudes.set(e.join("."),t)},clearEditingMagnitude:e=>{this._editingMagnitudes.delete(e.join("."))},stashOwner:this,renderEntry:()=>l.s6};return e.renderEntry=(t,i)=>this._renderEntry(t,i,e),e}_scopeValues(e){let t=(0,eL.O6)(this.values,e);return t&&"object"==typeof t&&!Array.isArray(t)?t:{}}_emitChange(e,t){this.dispatchEvent(new CustomEvent("value-change",{detail:{path:e,value:t},bubbles:!0,composed:!0}))}_emitEditActionField(e){this.dispatchEvent(new CustomEvent("edit-action-field",{detail:{field:e},bubbles:!0,composed:!0}))}_toggleNested(e){let t=new Set(this._nestedOpenSections);t.has(e)?t.delete(e):t.add(e),this._nestedOpenSections=t}openNested(e){if(this.requiredOnly||this._nestedOpenSections.has(e))return;let t=new Set(this._nestedOpenSections);t.add(e),this._nestedOpenSections=t}_seedNestedOpen(e){this.requiredOnly||this._seededNestedOpen.has(e)||(this._seededNestedOpen.add(e),this._nestedOpenSections.add(e))}_requestAddComponent(e){this.dispatchEvent(new CustomEvent("request-add-component",{detail:{domain:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._pinRegistryModesKicked=!1,this.entries=[],this.values={},this.errors=new Map,this.board=null,this.disabled=!1,this.showAdvanced=!1,this.requiredOnly=!1,this.yaml="",this.sectionKey="",this.presentComponents=new Set,this._nestedOpenSections=new Set,this._seededNestedOpen=new Set,this._fieldScroll=new e4(this),this._fieldFocus=new e6(this),this._pendingUnits=new Map,this._editingMagnitudes=new Map,this._filterRenderable=(e,t)=>eI(e,t,{requiredOnly:this.requiredOnly,showAdvanced:this.showAdvanced,presentComponents:this.presentComponents,targetPlatform:this.board?.esphome.platform??null})}}function ip(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}ih.styles=eZ,ic([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ih.prototype,"_localize",void 0),ic([(0,n.Fg)({context:u.Ie,subscribe:!0}),(0,d.wk)()],ih.prototype,"_api",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"entries",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"values",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"errors",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"board",void 0),ic([(0,d.MZ)({type:Boolean})],ih.prototype,"disabled",void 0),ic([(0,d.MZ)({type:Boolean,attribute:"show-advanced"})],ih.prototype,"showAdvanced",void 0),ic([(0,d.MZ)({type:Boolean,attribute:"required-only"})],ih.prototype,"requiredOnly",void 0),ic([(0,d.MZ)()],ih.prototype,"yaml",void 0),ic([(0,d.MZ)({type:Number,attribute:"from-line"})],ih.prototype,"fromLine",void 0),ic([(0,d.MZ)({attribute:"section-key"})],ih.prototype,"sectionKey",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"presentComponents",void 0),ic([(0,d.MZ)({attribute:!1})],ih.prototype,"focusFieldPath",void 0),ic([(0,d.wk)()],ih.prototype,"_nestedOpenSections",void 0),ih=ic([(0,d.EM)("esphome-config-entry-form")],ih),(0,b.C)({"alert-circle-outline":s.mdiAlertCircleOutline});class iu extends l.WF{willUpdate(e){super.willUpdate(e),(e.has("component")||!this._initialized)&&this.component&&(this._initialized=!0,this._initValues(),this._localBlockMessage="",this._depResolver.kickoff(this.component.dependencies??[]))}_initValues(){let e=this.component.id.startsWith("featured."),t=this._seedDefaults(this.component.config_entries,e);if(this.component.config_entries.find(e=>"id"===e.key&&e.type===y.Hh.ID)&&void 0===t.id){let e=this._generateDefaultId();null!==e&&(t={...t,id:e})}if(t=function(e,t,i,a){if(!i?.pins?.length||e.includes("."))return a;let o=a;for(let a of t){if(a.type!==y.Hh.PIN||void 0!==o[a.key])continue;let t=a.key.toLowerCase().replace(/_(pin|gpio)$/,""),r=`${e}_${t}`,n=i.pins.find(e=>e.features.includes(r));n&&(o={...o,[a.key]:n.gpio})}return o}(this.component.id,this.component.config_entries,this.board,t),this.prefillReference){let e=this._findReferencePath(this.component.config_entries,this.prefillReference.domain,[]);e&&(t=(0,eL.Oe)(t,e,this.prefillReference.id))}this._values=t}_findReferencePath(e,t,i){for(let a of e){if(a.type===y.Hh.NESTED){let e=this._findReferencePath(a.config_entries??[],t,[...i,a.key]);if(e)return e;continue}if(a.references_component===t)return[...i,a.key]}return null}_seedDefaults(e,t=!1){let i={};for(let a of e){if(a.type===y.Hh.NESTED){let e=this._seedDefaults(a.config_entries??[],t);Object.keys(e).length>0&&(i[a.key]=e);continue}(t||a.required)&&(null!=a.default_value?i[a.key]=a.multi_value?[String(a.default_value)]:a.default_value:a.multi_value&&a.required&&(i[a.key]=[]))}return i}_generateDefaultId(){return function(e,t,i){if(!t&&!e.includes("."))return null;let a=e.replace(/\./g,"_").toLowerCase(),o=1,r=`${a}_${o}`;for(;i.has(r);)o++,r=`${a}_${o}`;return r}(this.component.id,this.component.multi_conf,function(e){let t=new Set;if(!e)return t;for(let i of e.split("\n")){let e=i.match(/^\s+(?:-\s+)?id:\s*["']?(\S+?)["']?\s*$/);e&&t.add(e[1])}return t}(this.yaml))}render(){let e=this.submitting,t=(0,ex.Zn)(this.yaml),i=(this.component.dependencies??[]).filter(e=>!t.has(e)),a=(0,eM.JK)(this.component.config_entries,this._values,t,this.board?.esphome.platform??null),o=!this._hasRequiredErrors(a);return(0,l.qy)`
      <div class="form">
        <p class="form-desc">${(0,es.G)(this.component.description)}</p>
        ${i.length>0?this._renderMissingDeps(i):l.s6}
        <esphome-config-entry-form
          .entries=${this.component.config_entries}
          .values=${this._values}
          .errors=${this._errors}
          .board=${this.board}
          .yaml=${this.yaml}
          .presentComponents=${t}
          ?disabled=${e}
          ?required-only=${!0}
          @value-change=${this._onValueChange}
        ></esphome-config-entry-form>
        <button
          type="button"
          class="toggle-link"
          @click=${()=>{this._showYaml=!this._showYaml}}
        >
          ${this._showYaml?this._localize("device.yaml_preview_toggle"):this._localize("device.yaml_preview")}
        </button>
        ${this._showYaml?(0,l.qy)`<pre class="yaml-preview">${this._generateYamlPreview()}</pre>`:l.s6}
        ${this.submitError?(0,l.qy)`<p class="error">${this.submitError}</p>`:l.s6}
        ${this._localBlockMessage?(0,l.qy)`<p class="error">${this._localBlockMessage}</p>`:l.s6}
        <div class="actions">
          <button
            class="btn btn-secondary"
            ?disabled=${e}
            @click=${this._onCancel}
          >
            ${this._localize("wizard.back")}
          </button>
          <button
            class="btn btn-primary"
            ?disabled=${e||!o||i.length>0}
            @click=${this._onSubmit}
          >
            ${this.submitting?this._localize("device.adding"):this._localize("device.add_component_action")}
          </button>
        </div>
      </div>
    `}_renderMissingDeps(e){return(0,l.qy)`
      <div class="deps-warning" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div class="deps-warning-body">
          <div class="deps-warning-title">
            ${this._localize("device.missing_dependencies_title",{name:this.component.name})}
          </div>
          <div>${this._localize("device.missing_dependencies_body")}</div>
          <div class="deps-warning-actions">
            ${e.map(e=>(0,l.qy)`<button
                  type="button"
                  class="dep-button"
                  @click=${()=>this._onAddDep(e)}
                >
                  ${this._localize("device.missing_dependencies_add",{domain:this._depResolver.resolve(e)})}
                </button>`)}
          </div>
        </div>
      </div>
    `}_onAddDep(e){this.dispatchEvent(new CustomEvent("navigate-to-dep",{detail:{domain:e},bubbles:!0,composed:!0}))}_hasRequiredErrors(e){for(let t of e.values())if("validation.required"===t.code)return!0;return!1}_labelForErrorKey(e){let t,i=e.split("."),a=this.component.config_entries;for(let e of i){if(!a||!(t=a.find(t=>t.key===e)))break;a=t.type===y.Hh.NESTED?t.config_entries??[]:null}return t?eV(t,this._localize):e}_anyErrorIsVisible(e,t){if(0===e.size)return!1;let i=function e(t,i,a,o=[],r=new Set){for(let n of eI(t,i,a)){if(n.type===y.Hh.NESTED){let t=n.config_entries??[];n.multi_value?(0,eL.ly)(i[n.key]).forEach((i,s)=>{e(t,i,a,[...o,n.key,String(s)],r)}):e(t,(0,eL.qY)(i[n.key]),a,[...o,n.key],r),r.add([...o,n.key].join("."));continue}r.add([...o,n.key].join("."))}return r}(this.component.config_entries,this._values,{requiredOnly:!0,showAdvanced:!1,presentComponents:t,targetPlatform:this.board?.esphome.platform??null});for(let t of e.keys())if(i.has(t))return!0;return!1}_onValueChange(e){let{path:t,value:i}=e.detail;this._values=(0,eL.Oe)(this._values,t,i);let a=t.join(".");if(this._errors.has(a)){let e=new Map(this._errors);e.delete(a),this._errors=e}this._localBlockMessage&&(this._localBlockMessage="")}_generateYamlPreview(){let e=[`${this.component.id}:`];return e.push(...(0,ex.ym)(this._values,"  ")),e.join("\n")}_onCancel(){this.dispatchEvent(new CustomEvent("form-cancel",{bubbles:!0,composed:!0}))}_onSubmit(){this._localBlockMessage="";let e=(0,ex.Zn)(this.yaml),t=(this.component.dependencies??[]).filter(t=>!e.has(t));if(t.length>0){this._localBlockMessage=`${this._localize("device.missing_dependencies_title",{name:this.component.name})} (${t.join(", ")})`;return}let i=(0,eM.JK)(this.component.config_entries,this._values,e,this.board?.esphome.platform??null);if(i.size>0){if(this._errors=i,!this._anyErrorIsVisible(i,e)){let e=[...i.entries()].map(([e,t])=>`${this._labelForErrorKey(e)}: ${this._localize(t.code,t.params)}`).join("; ");this._localBlockMessage=`${this._localize("device.add_component_hidden_validation_error")} (${e})`}return}this._errors=new Map,this._localBlockMessage="";let a=function e(t,i){let a={};for(let o of t){if(o.hidden)continue;let t=i[o.key];if(o.type===y.Hh.NESTED){let i=null===t||"object"!=typeof t||Array.isArray(t)?{}:t,r=e(o.config_entries??[],i);Object.keys(r).length>0&&(a[o.key]=r);continue}if(void 0!==t){if(Array.isArray(t)){if(0===t.length)continue;a[o.key]=t;continue}if(""===t){o.required&&(a[o.key]=t);continue}if(o.type===y.Hh.INTEGER&&"hex"!==o.display_format){let e="number"==typeof t?t:Number.parseInt(String(t),10);Number.isNaN(e)||(a[o.key]=e)}else if(o.type===y.Hh.FLOAT){let e="number"==typeof t?t:Number.parseFloat(String(t));Number.isNaN(e)||(a[o.key]=e)}else o.type===y.Hh.BOOLEAN?a[o.key]=!0===(0,ex.FY)(t):a[o.key]=t}}return a}(this.component.config_entries,this._values);this.dispatchEvent(new CustomEvent("form-submit",{detail:{fields:a},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this.yaml="",this.prefillReference=null,this.submitting=!1,this.submitError="",this._values={},this._errors=new Map,this._localBlockMessage="",this._showYaml=!1,this._depResolver=new eS(this,()=>this._api,()=>this.board?.esphome.platform||void 0),this._initialized=!1}}iu.styles=[m.G,ed.z,eP],ip([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iu.prototype,"_localize",void 0),ip([(0,n.Fg)({context:u.Ie})],iu.prototype,"_api",void 0),ip([(0,d.MZ)({attribute:!1})],iu.prototype,"component",void 0),ip([(0,d.MZ)({attribute:!1})],iu.prototype,"board",void 0),ip([(0,d.MZ)()],iu.prototype,"yaml",void 0),ip([(0,d.MZ)({attribute:!1})],iu.prototype,"prefillReference",void 0),ip([(0,d.MZ)({type:Boolean})],iu.prototype,"submitting",void 0),ip([(0,d.MZ)()],iu.prototype,"submitError",void 0),ip([(0,d.wk)()],iu.prototype,"_values",void 0),ip([(0,d.wk)()],iu.prototype,"_errors",void 0),ip([(0,d.wk)()],iu.prototype,"_localBlockMessage",void 0),ip([(0,d.wk)()],iu.prototype,"_showYaml",void 0),iu=ip([(0,d.EM)("esphome-add-component-form")],iu);var im=i(4996);let iv=new Set(["adc","dac","ota"]);function ig(e){let t=e.target;return!t?.closest("a, button")}let i_=(0,l.AH)`
  :host {
    display: flex;
    height: 480px;
    gap: 0;
  }

  :host([hidden]) {
    display: none;
  }

  .sidebar {
    width: 160px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    padding-right: var(--wa-space-m);
    border-right: 1px solid var(--wa-color-surface-border);
    overflow-y: auto;
  }

  .sidebar-label {
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 var(--wa-space-2xs);
    flex-shrink: 0;
  }

  .category-btn {
    border: none;
    background: none;
    cursor: pointer;
    text-align: left;
    padding: var(--wa-space-xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    transition: background 0.1s;
    font-family: inherit;
    flex-shrink: 0;
  }

  .category-btn:hover {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .category-btn--active {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .category-btn-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-xs);
  }

  .category-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 18px;
    height: 18px;
    padding: 0 4px;
    border-radius: 9px;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    background: var(--wa-color-surface-raised);
    color: var(--wa-color-text-subtle);
    flex-shrink: 0;
    box-sizing: border-box;
  }

  .category-btn--active .category-count {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    padding-left: var(--wa-space-m);
    padding-top: 3px;
    padding-right: 3px;
    overflow: hidden;
  }

  input[type="search"] {
    flex-shrink: 0;
  }

  .result-count {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
    margin-top: -6px;
  }

  .grid-scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: var(--wa-space-2xs);
  }

  /* auto-fill + minmax so the grid drops 2 → 1 column as soon as a card
     would shrink below ~340px — avoids hard viewport breakpoints. */
  .components-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 8px;
    align-content: start;
  }

  /* Below the shared phone breakpoint (modal viewport on phones) collapse sidebar into a
     horizontal chip row above the grid. */
  @media (max-width: ${600}px) {
    /* The dialog hosting the catalog goes full-screen on phones, so fill the
       available height (the body's flex track) rather than capping at 70vh,
       which would leave the bottom of the screen empty. */
    :host {
      flex-direction: column;
      height: 100%;
    }

    .sidebar {
      width: 100%;
      flex-direction: row;
      gap: var(--wa-space-2xs);
      padding-right: 0;
      padding-bottom: var(--wa-space-s);
      margin-bottom: var(--wa-space-s);
      overflow-x: auto;
      overflow-y: hidden;
      border-right: none;
      border-bottom: 1px solid var(--wa-color-surface-border);
    }

    .sidebar-label {
      display: none;
    }

    .category-btn {
      flex-shrink: 0;
      white-space: nowrap;
    }

    .main {
      padding-left: 0;
      padding-right: 0;
    }

    /* Drop the desktop 340px column floor: in the full-screen mobile dialog
       the body is narrower than 340px on small phones (e.g. 375px − padding),
       and minmax(340px, …) would force a track wider than the viewport and
       clip the cards. A single minmax(0, 1fr) column shrinks to fit. */
    .components-grid {
      grid-template-columns: minmax(0, 1fr);
    }
  }

  .component-card {
    border-radius: var(--wa-border-radius-l);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    padding: var(--wa-space-s) var(--wa-space-m);
    box-sizing: border-box;
    min-width: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 6px;
    cursor: pointer;
    transition:
      border-color var(--wa-transition-normal) var(--wa-transition-easing),
      background var(--wa-transition-normal) var(--wa-transition-easing);
  }

  .component-card:hover {
    border-color: var(--esphome-primary);
    background: var(--esphome-tint-faint);
  }

  .component-card:focus-within {
    border-color: var(--esphome-primary);
  }

  .component-card--expanded {
    grid-column: 1 / -1;
  }

  .expand-button {
    border: none;
    background: none;
    cursor: pointer;
    padding: 2px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
    color: var(--esphome-primary);
    font-size: 15px;
  }

  .expand-button:focus-visible {
    outline: 2px solid var(--esphome-primary);
    outline-offset: 1px;
  }

  .expand-button wa-icon {
    transition: transform var(--wa-transition-normal) var(--wa-transition-easing);
  }

  .component-card-header {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .component-image,
  .component-image--placeholder {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-subtle);
    flex-shrink: 0;
    color: var(--esphome-primary);
    font-size: 28px;
    box-sizing: border-box;
  }

  .component-image {
    padding: 4px;
  }

  .component-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* ESPHome's monochrome SVG illustrations are black-on-transparent —
     invert + hue-rotate in dark mode (apply-theme.ts root var). Scoped
     to SVGs so JPGs/PNGs keep their original colours. */
  .component-image img[src$=".svg"] {
    filter: var(--esphome-svg-filter, none);
  }

  .component-card-header-text {
    flex: 1;
    min-width: 0;
  }

  .component-title {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Category chip disambiguates same-name catalog entries (sensor.debug
     vs text_sensor.debug). Only shown under "All" / "Featured" — see
     shouldShowCategoryChip. */
  .component-category-chip {
    display: inline-block;
    margin-top: 2px;
    padding: 0 6px;
    font-size: 9px;
    font-weight: var(--wa-font-weight-semibold);
    line-height: 1.6;
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-raised);
    border: 1px solid var(--wa-color-border);
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .component-description {
    margin: 0;
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.4;
  }

  .component-description--clamp {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-xs);
    margin-top: auto;
  }

  .more-info {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    font-size: var(--wa-font-size-2xs);
    color: var(--esphome-primary);
    text-decoration: none;
  }

  .more-info:hover {
    text-decoration: underline;
  }

  .more-info wa-icon {
    font-size: 11px;
  }

  .select-component {
    display: flex;
    align-items: center;
    gap: 3px;
    border: none;
    background: none;
    padding: 0;
    border-radius: 4px;
    font-family: inherit;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--esphome-primary);
    cursor: pointer;
  }

  .select-component:focus-visible {
    outline: 2px solid var(--esphome-primary);
    outline-offset: 3px;
  }

  .empty {
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    padding: var(--wa-space-xl);
    grid-column: 1 / -1;
  }

  .loading {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
  }

  /* Featured cards get a subtle primary border so they read as the
     curated set, distinct from the regular catalog. */
  .component-card--featured {
    border-color: var(--esphome-tint-border);
  }

  .bundle-badge {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--esphome-primary);
    background: var(--esphome-tint);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
  }

  .bundle-badge wa-icon {
    font-size: 11px;
  }
`;function ib(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({"arrow-collapse-all":s.mdiArrowCollapseAll,"arrow-expand-all":s.mdiArrowExpandAll,memory:s.mdiMemory,"open-in-new":s.mdiOpenInNew,"package-variant-closed":s.mdiPackageVariantClosed,plus:s.mdiPlus});class iy extends l.WF{load(){let e=(this.board?.featured_components?.length??0)+(this.board?.featured_bundles?.length??0);0===this.lockedCategories.length&&this.boardId&&e>0?this._category=ek.FEATURED:this._category===ek.FEATURED&&(this._category="all"),this._fetchComponents()}filterByDomain(e){Object.values(ek).includes(e)?(this._search="",this._category=e):(this._search=e,this._category="all"),this._fetchComponents()}async _fetchComponents(){this._loading=!0;try{let e=this._search.trim()||void 0,t=this.lockedCategories.length>0,i=t?this.lockedCategories:"all"!==this._category?this._category:void 0,a=!t&&this.excludeCategories.length>0?this.excludeCategories:void 0,o=await this._api.getComponents({query:e,category:i,exclude_category:a,platform:this.platform||void 0,board_id:this.boardId||void 0,limit:50});this._components=o.components,this._categories=o.categories,this._total=o.total}catch(e){console.error("Failed to load component catalog:",e)}finally{this._loading=!1,this._initialLoad=!1}}render(){var e;let t,i,a,o,r,n,s,d,c,h,p,u,m,v,g;if(this._initialLoad&&this._loading)return(0,l.qy)`<div class="loading">
        ${this._localize("device.loading_components")}
      </div>`;let f=(e=this._localize,t=new Set(this.excludeCategories),a=(i=this._categories.filter(e=>!t.has(e.id))).find(e=>e.id===ek.FEATURED),o=this.board?.featured_bundles?.length??0,r=a?a.count+o:o,n=i.filter(e=>e.id!==ek.FEATURED),s=t.size?n.reduce((e,t)=>e+t.count,0):this._total,d=new Intl.Collator(void 0,{sensitivity:"base"}),c=n.map(t=>{let i=`device.component_category_${t.id}`,a=e(i);return{id:t.id,label:a!==i?a:t.name,count:t.count}}).sort((e,t)=>d.compare(e.label,t.label)),h=[],r>0&&h.push({id:ek.FEATURED,label:e("device.component_category_featured"),count:r}),h.push({id:"all",label:e("device.component_category_all"),count:s}),h.push(...c),h),_=0===this.lockedCategories.length,b=this._category===ek.FEATURED?(p=this.board?.featured_bundles??[],(u=this._search.trim().toLowerCase())?p.filter(e=>e.name.toLowerCase().includes(u)||e.description.toLowerCase().includes(u)||e.id.toLowerCase().includes(u)):p):[],y=(m=this.yaml?(0,ex.Zn)(this.yaml):new Set,v=this.yaml?(0,ex.u)(this.yaml):new Set,g=this.lockedCategories.length>0?new Set(this._components.map(e=>e.id)):null,this._components.filter(e=>{if(!e.multi_conf){if(e.id.includes(".")){if(v.has(e.id))return!1}else if(m.has(e.id))return!1}return(!(g&&e.id.includes("."))||!(e.dependencies.length>0)||!!e.dependencies.every(e=>g.has(e)||m.has(e)))&&!0}));return(0,l.qy)`
      ${_?(0,l.qy)`<div class="sidebar">
            <p class="sidebar-label">${this._localize("device.component_categories")}</p>
            ${f.map(({id:e,label:t,count:i})=>(0,l.qy)`
                <button
                  class="category-btn ${this._category===e?"category-btn--active":""}"
                  type="button"
                  @click=${()=>{this._category=e,this._fetchComponents()}}
                >
                  <span class="category-btn-inner">
                    <span>${t}</span>
                    <span class="category-count">${i}</span>
                  </span>
                </button>
              `)}
          </div>`:l.s6}
      <div class="main">
        <input
          type="search"
          autocomplete="off"
          .value=${this._search}
          @input=${this._onSearchInput}
          placeholder=${this._localize("device.search_components_placeholder")}
        />
        ${!this._loading?(0,l.qy)`<span class="result-count"
              >${y.length+b.length} of ${this._total+b.length}
              components</span
            >`:""}
        <div class="grid-scroll">
          <div class="components-grid">
            ${this._loading?(0,l.qy)`<p class="empty">${this._localize("device.loading_components")}</p>`:y.length+b.length?(0,l.qy)`
                    ${b.map(e=>{var t;return t=this,(0,l.qy)`
    <article
      class="component-card component-card--featured"
      @click=${i=>{ig(i)&&t._onAddBundle(e)}}
    >
      <div class="component-card-header">
        <div class="component-image--placeholder">
          <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
        </div>
        <div class="component-card-header-text">
          <h3 class="component-title">${e.name}</h3>
        </div>
        <span class="bundle-badge">
          <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
          ${t._localize("device.featured_bundle_badge")}
        </span>
      </div>
      ${e.description?(0,l.qy)`<p class="component-description component-description--clamp">
            ${(0,es.G)(e.description)}
          </p>`:l.s6}
      <div class="card-footer">
        <span></span>
        <button
          class="select-component"
          type="button"
          @click=${()=>t._onAddBundle(e)}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${t._localize("device.add_component_action")}
        </button>
      </div>
    </article>
  `})}
                    ${y.map(e=>{var t,i,a,o,r,n;let s,d;return t=this,i=e.id===this._expandedId,a=this._category===ek.FEATURED,o=this._localize,s=!!e.image_url&&!t._imageFailed.has(e.id),d=("all"===(r=t._category)||"featured"===r)&&(n=e.category)?n.split("_").filter(e=>e.length>0).map(e=>iv.has(e.toLowerCase())?e.toUpperCase():e[0].toUpperCase()+e.slice(1)).join(" "):"",(0,l.qy)`
    <article
      class="component-card ${i?"component-card--expanded":""} ${a?"component-card--featured":""}"
      @click=${i=>{ig(i)&&t._onAdd(e)}}
    >
      <div class="component-card-header">
        ${s?(0,l.qy)`<div class="component-image">
              <img
                src=${e.image_url}
                alt=${e.name}
                referrerpolicy="no-referrer"
                loading="lazy"
                @error=${()=>t._onImageError(e.id)}
              />
            </div>`:(0,l.qy)`<div class="component-image--placeholder">
              <wa-icon library="mdi" name="memory"></wa-icon>
            </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title">${e.name}</h3>
          ${d?(0,l.qy)`<span class="component-category-chip">${d}</span>`:l.s6}
        </div>
        <button
          class="expand-button"
          type="button"
          aria-pressed=${i}
          title=${o("wizard.expand_board")}
          @click=${()=>t._onToggleExpand(e)}
        >
          <wa-icon
            library="mdi"
            name=${i?"arrow-collapse-all":"arrow-expand-all"}
          ></wa-icon>
        </button>
      </div>
      <p class="component-description ${i?"":"component-description--clamp"}">
        ${(0,es.G)(e.description)}
      </p>
      <div class="card-footer">
        <a class="more-info" href=${e.docs_url} target="_blank" rel="noreferrer">
          ${o("device.more_info")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <button
          class="select-component"
          type="button"
          @click=${()=>t._onAdd(e)}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${o("device.add_component_action")}
        </button>
      </div>
    </article>
  `})}
                  `:(0,l.qy)`<p class="empty">
                    ${this._localize("device.no_components_found")}
                  </p>`}
          </div>
        </div>
      </div>
    `}_onToggleExpand(e){this._expandedId=this._expandedId===e.id?null:e.id}_onImageError(e){if(this._imageFailed.has(e))return;let t=new Set(this._imageFailed);t.add(e),this._imageFailed=t}_onAdd(e){this.dispatchEvent(new CustomEvent("add-component",{detail:{component:e},bubbles:!0,composed:!0}))}_onAddBundle(e){this.dispatchEvent(new CustomEvent("add-bundle",{detail:{bundle:e,boardId:this.boardId},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.platform="",this.boardId="",this.board=null,this.yaml="",this.lockedCategories=[],this.excludeCategories=[],this._components=[],this._categories=[],this._total=0,this._loading=!0,this._initialLoad=!0,this._search="",this._category="all",this._expandedId=null,this._imageFailed=new Set,this._debouncedSearch=(0,im.s)(()=>this._fetchComponents(),300),this._onSearchInput=e=>{this._search=e.target.value,this._debouncedSearch()}}}function iw(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iy.styles=[m.G,ed.z,i_],ib([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iy.prototype,"_localize",void 0),ib([(0,n.Fg)({context:u.Ie})],iy.prototype,"_api",void 0),ib([(0,d.MZ)()],iy.prototype,"platform",void 0),ib([(0,d.MZ)({attribute:"board-id"})],iy.prototype,"boardId",void 0),ib([(0,d.MZ)({attribute:!1})],iy.prototype,"board",void 0),ib([(0,d.MZ)()],iy.prototype,"yaml",void 0),ib([(0,d.MZ)({attribute:!1})],iy.prototype,"lockedCategories",void 0),ib([(0,d.MZ)({attribute:!1})],iy.prototype,"excludeCategories",void 0),ib([(0,d.wk)()],iy.prototype,"_components",void 0),ib([(0,d.wk)()],iy.prototype,"_categories",void 0),ib([(0,d.wk)()],iy.prototype,"_total",void 0),ib([(0,d.wk)()],iy.prototype,"_loading",void 0),ib([(0,d.wk)()],iy.prototype,"_initialLoad",void 0),ib([(0,d.wk)()],iy.prototype,"_search",void 0),ib([(0,d.wk)()],iy.prototype,"_category",void 0),ib([(0,d.wk)()],iy.prototype,"_expandedId",void 0),ib([(0,d.wk)()],iy.prototype,"_imageFailed",void 0),iy=ib([(0,d.EM)("esphome-component-catalog")],iy),(0,b.C)({close:s.mdiClose,"arrow-left":s.mdiArrowLeft,"package-variant-closed":s.mdiPackageVariantClosed});class i$ extends l.WF{open(){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._open=!0,this.updateComplete.then(()=>this._catalog?.load())}openWithSearch(e){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._open=!0,this.updateComplete.then(()=>this._catalog?.filterByDomain(e))}_resetDetourState(){this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=[],this._bundleProgress=null,this._depNavSeq++,this._selectionSeq++}render(){var e;let t=null!==this._selected,i=this.lockedCategories.length>0,a=i?this.boardName?"device.add_config_dialog_title":"device.add_config":this.boardName?"device.add_component_dialog_title":"device.add_component",o=t?this._selected.name:this.boardName?this._localize(a,{name:this.boardName}):this._localize(a);return(0,l.qy)`
      <esphome-base-dialog
        class=${t?"form-view":""}
        ?open=${this._open}
        ?busy=${this._submitting}
        .label=${o}
        @request-close=${this._onRequestClose}
        @add-component=${this._onComponentSelected}
        @add-bundle=${this._onBundleSelected}
        @form-cancel=${this._onBack}
        @form-submit=${this._onFormSubmit}
        @navigate-to-dep=${this._onNavigateToDep}
        @request-add-component=${this._onNavigateToDep}
      >
        ${t?(0,l.qy)`<button
              slot="header-prefix"
              class="back-button"
              title=${this._localize("layout.back")}
              aria-label=${this._localize("layout.back")}
              @click=${this._onBack}
            >
              <wa-icon library="mdi" name="arrow-left"></wa-icon>
            </button>`:l.s6}
        ${this._returnTo?(0,l.qy)`<div class="return-banner">
              ${this._localize("device.return_to_after_dep_prefix")}
              <strong>${this._returnTo.name}</strong>
              ${this._localize("device.return_to_after_dep_suffix")}
            </div>`:l.s6}
        ${t&&this._bundleProgress?(0,l.qy)`<div class="bundle-banner">
              <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
              <span
                >${this._localize("device.bundle_step_progress",{current:this._bundleProgress.current,total:this._bundleProgress.total,name:this._bundleProgress.bundleName})}</span
              >
            </div>`:l.s6}
        ${!t&&this._submitError?(0,l.qy)`<div class="catalog-error" role="alert">${this._submitError}</div>`:l.s6}
        <esphome-component-catalog
          ?hidden=${t}
          .platform=${this.platform}
          .boardId=${this.board?.id??""}
          .board=${this.board}
          .yaml=${this.yaml}
          .lockedCategories=${this.lockedCategories}
          .excludeCategories=${(e={isCoreLocked:i,isInDepDetour:null!==this._returnTo}).isCoreLocked||e.isInDepDetour?[]:ez}
        ></esphome-component-catalog>
        ${t?(0,l.qy)`<esphome-add-component-form
              .component=${this._selected}
              .board=${this.board}
              .yaml=${this.yaml}
              .prefillReference=${this._prefillReference}
              .submitting=${this._submitting}
              .submitError=${this._submitError}
            ></esphome-add-component-form>`:l.s6}
      </esphome-base-dialog>
    `}async _onComponentSelected(e){e.stopPropagation();let t=await eA(this,e.detail.component.id);if("stale"!==t.kind){if("error"===t.kind){this._submitError=t.message;return}if(this._selected=t.entry,this._submitError="",0===t.entry.config_entries.length){let e=(0,ex.Zn)(this.yaml);(t.entry.dependencies??[]).some(t=>!e.has(t))||await this._submitComponent({},!0)}}}async _onBundleSelected(e){if(e.stopPropagation(),this._submitting)return;let{bundle:t,boardId:i}=e.detail;if(!i||0===t.component_ids.length)return;let a=t.component_ids.map(e=>`featured.${i}.${e}`),[o,...r]=a,n=await eA(this,o,i);if("stale"===n.kind)return;if("error"===n.kind){this._submitError=n.message;return}let s=n.entry;this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=r,this._bundleProgress={current:1,total:a.length,bundleName:t.name},this._selected=s,this._submitError=""}_onBack(){if(!this._submitting){if(this._returnTo){let e=this._returnTo;this._resetDetourState(),this._selected=e,this._submitError="";return}this._resetDetourState(),this._selected=null,this._submitError=""}}_onNavigateToDep(e){return e.stopPropagation(),eE(this,e.detail.domain)}_onFormSubmit(e){return e.stopPropagation(),this._submitComponent(e.detail.fields)}async _submitComponent(e,t=!1){if(this._selected&&this.configuration&&!this._submitting){this._submitting=!0,this._submitError="",this._depNavSeq++;try{let{yaml:a}=await this._api.addComponent(this.configuration,{component_id:this._selected.id,fields:e},this.yaml||void 0);if(this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})),this._returnTo){var i;let t=this._returnTo,a=this._depDomain,o=e.id;a&&"string"==typeof o&&(i=this._selected,i.id===a||i.category===a)?this._prefillReference={domain:a,id:o}:this._prefillReference=null,this._returnTo=null,this._depDomain=null,this._selected=t}else if(this._bundleQueue.length>0&&this._bundleProgress){let t=this._bundleQueue[0],i=this._bundleQueue.slice(1),a=await eA(this,t);if("stale"===a.kind)return;if("error"===a.kind){this._submitError=a.message;return}let o=a.entry,r=e.id,n=this._selected.category;"string"==typeof r&&n?this._prefillReference={domain:n,id:r}:this._prefillReference=null,this._bundleQueue=i,this._bundleProgress={...this._bundleProgress,current:this._bundleProgress.current+1},this._selected=o}else{let i=this._selected.id,o=this._selected.name,r=e.id,n=function(e,t,i){let a=P(e);if(!t.includes(".")){let e=a.find(e=>e.key===t&&!e.platform);if(e)return{sectionKey:e.key,fromLine:e.fromLine}}let o=a.filter(e=>G(e)===t);if(0===o.length)return null;if(1===o.length)return{sectionKey:G(o[0]),fromLine:o[0].fromLine};if(i){let t=e.split("\n"),a=RegExp(`^\\s+(?:-\\s+)?id:\\s*["']?${i}["']?\\s*$`);for(let e of o)for(let i=e.fromLine-1;i<e.toLine&&i<t.length;i++)if(a.test(t[i]))return{sectionKey:G(e),fromLine:e.fromLine}}let r=o[o.length-1];return{sectionKey:G(r),fromLine:r.fromLine}}(a,i,"string"==typeof r?r:void 0);n&&this.dispatchEvent(new CustomEvent("section-select",{detail:n,bubbles:!0,composed:!0})),this._open=!1,this._selected=null,this._resetDetourState(),t&&c.A.success(this._localize("device.component_added",{name:o}),{richColors:!0})}}catch(e){this._submitError=e instanceof Error?e.message:this._localize("device.add_component_error"),t&&c.A.error(this._submitError,{richColors:!0})}finally{this._submitting=!1}}}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml="",this.lockedCategories=[],this._open=!1,this._selected=null,this._submitting=!1,this._submitError="",this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=[],this._bundleProgress=null,this._selectionSeq=0,this._depNavSeq=0,this._onRequestClose=()=>{this._open=!1}}}function ix(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i$.styles=[m.G,(0,e$._)("esphome-base-dialog"),ew.c4,eq],iw([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i$.prototype,"_localize",void 0),iw([(0,n.Fg)({context:u.Ie})],i$.prototype,"_api",void 0),iw([(0,d.MZ)()],i$.prototype,"boardName",void 0),iw([(0,d.MZ)()],i$.prototype,"configuration",void 0),iw([(0,d.MZ)()],i$.prototype,"platform",void 0),iw([(0,d.MZ)({attribute:!1})],i$.prototype,"board",void 0),iw([(0,d.MZ)()],i$.prototype,"yaml",void 0),iw([(0,d.MZ)({attribute:!1})],i$.prototype,"lockedCategories",void 0),iw([(0,d.wk)()],i$.prototype,"_open",void 0),iw([(0,d.P)("esphome-component-catalog")],i$.prototype,"_catalog",void 0),iw([(0,d.wk)()],i$.prototype,"_selected",void 0),iw([(0,d.wk)()],i$.prototype,"_submitting",void 0),iw([(0,d.wk)()],i$.prototype,"_submitError",void 0),iw([(0,d.wk)()],i$.prototype,"_returnTo",void 0),iw([(0,d.wk)()],i$.prototype,"_depDomain",void 0),iw([(0,d.wk)()],i$.prototype,"_prefillReference",void 0),iw([(0,d.wk)()],i$.prototype,"_bundleQueue",void 0),iw([(0,d.wk)()],i$.prototype,"_bundleProgress",void 0),i$=iw([(0,d.EM)("esphome-add-component-dialog")],i$);class ik extends l.WF{open(){this._inner.open()}render(){return(0,l.qy)`<esphome-add-component-dialog
      .lockedCategories=${ez}
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .platform=${this.platform}
      .board=${this.board}
      .yaml=${this.yaml}
    ></esphome-add-component-dialog>`}constructor(...e){super(...e),this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml=""}}function iz(e){return e.replace(/[^a-zA-Z0-9_]+/g,"_")}function iC(e){for(let t of e)if(t.advanced||t.type===y.Hh.NESTED&&iC(t.config_entries??[]))return!0;return!1}function iE(e,t,i){return(0,l.qy)`<div class="advanced-toggle-row">
    <wa-switch
      .checked=${e}
      @change=${e=>i(e.target.checked)}
    >
      ${t("device.show_advanced")}
    </wa-switch>
  </div>`}ix([(0,d.MZ)()],ik.prototype,"boardName",void 0),ix([(0,d.MZ)()],ik.prototype,"configuration",void 0),ix([(0,d.MZ)()],ik.prototype,"platform",void 0),ix([(0,d.MZ)({attribute:!1})],ik.prototype,"board",void 0),ix([(0,d.MZ)()],ik.prototype,"yaml",void 0),ix([(0,d.P)("esphome-add-component-dialog")],ik.prototype,"_inner",void 0),ik=ix([(0,d.EM)("esphome-add-config-dialog")],ik);let iA=(0,l.AH)`
  :host {
    display: flex;
    flex-direction: column;
    /* Matches config-entry-form's :host gap so the editor's
       top-level rows (header, form, parameters, actions, …) sit
       at the same vertical rhythm as the catalog form's fields.
       Without this, the bespoke .field siblings render in a
       different cadence and the page reads as two different forms
       stitched together. */
    gap: var(--wa-space-m);
  }

  /* Component-style header card — at the top of the edit pane for
     automations and scripts. Mirrors the layout from
     device-board-info's section header so the editor reads as the
     "section editor" for an automation / script. */
  .ae-header {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: flex-start;
    gap: var(--wa-space-l);
    padding-bottom: var(--wa-space-m);
    /* The :host gap takes care of vertical spacing between the
       header and the next row, so the legacy margin-bottom would
       compound. Just keep the border + bottom padding so the
       divider line still reads as a section break. */
    border-bottom: 1px solid var(--wa-color-neutral-border-quiet, #e1e4e8);
  }

  .ae-header-text {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    min-width: 0;
  }

  .ae-header-title {
    margin: 0;
    font-size: var(--wa-font-size-l);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  /* Section-type subtitle under the main header title. Kept for
     the script editor which renders the id as a subtitle below
     the static "Script" title. The automation editor doesn't use
     a subtitle anymore — its identity (target + trigger) is in
     the read-only form fields below the header. */
  .ae-header-subtitle {
    margin: 0;
    font-size: var(--wa-font-size-m);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
  }

  /* Readonly inputs (target / trigger identity fields on the
     automation editor) read as form fields but the user can't
     edit them. Slightly different from the editable inputs:
     muted background + cursor: default to signal non-interactive. */
  input[readonly] {
    background: var(--wa-color-surface-lowered);
    cursor: default;
    color: var(--wa-color-text-quiet);
  }

  .ae-header-docs {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    color: var(--wa-color-brand-fill-loud, #0b5cad);
    font-size: var(--wa-font-size-2xs);
    text-decoration: none;
    align-self: flex-start;
  }

  .ae-header-docs:hover {
    text-decoration: underline;
  }

  .ae-header-docs wa-icon {
    font-size: 12px;
  }

  .ae-header-desc {
    margin: 0;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .ae-header-icon {
    flex: 0 0 auto;
    width: 64px;
    height: 64px;
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-lowered);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .ae-header-icon wa-icon {
    font-size: 32px;
    color: var(--wa-color-brand-fill-loud, #0b5cad);
  }

  /* Component-catalog image (used for interval automations: we pull
     the parent component's image_url to give the same visual cue a
     user gets from a regular component editor). Sized to fit the
     64x64 slot without stretching pixel art. */
  .ae-header-icon img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }

  /* "Show advanced settings" toggle row — mirrors the device
     section-config layout so the eye reads the two surfaces as
     the same kind of form. */
  .advanced-toggle-row {
    display: flex;
    justify-content: flex-start;
    margin-top: var(--wa-space-s);
    font-size: var(--wa-font-size-s);
  }
  .advanced-toggle-row wa-switch {
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
  }

  /* One titled panel — used for target, trigger, conditions, actions,
     and for any nested sub-panels inside a control-flow action. */
  .ae-section {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-m);
    border: 1px solid var(--wa-color-neutral-border-quiet, #e1e4e8);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-default);
  }

  .ae-section + .ae-section {
    margin-top: var(--wa-space-m);
  }

  .ae-section-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
  }

  /* Component-config-form-equivalent .field styles. Used in the
     script editor so the id / mode / parameters rows read the
     same as the regular component edit form (which uses
     config-entry-form.styles.ts's own .field family). Two
     separate style files because the scopes are different, but
     the visual contract is identical. */
  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
  }

  /* No .field + .field margin: the :host above hands out
     --wa-space-m gap to every direct child via flex layout,
     so a sibling-adjacent rule would double up the spacing.
     Components that render the script editor inside a different
     container (e.g. tests, the legacy add-mode pane) just lose the
     between-field gap on those isolated cases — acceptable for now;
     the canonical mount path goes through the page which always
     gets the :host gap. */

  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .field-label .required {
    color: var(--esphome-error, #d92d20);
  }

  .field-description {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0;
  }

  .field-description + input,
  .field-description + textarea,
  .field-description + wa-select {
    margin-top: 8px;
  }

  /* Script-parameter list row — one (name, type, remove) tuple per
     declared script parameter. Inline 3-column grid because each
     row has fixed-ish widths and we want them to align tidily. */
  .script-params-list {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    margin-bottom: var(--wa-space-2xs);
  }

  .script-param-row {
    display: grid;
    grid-template-columns: 1fr 7rem auto;
    gap: var(--wa-space-2xs);
    align-items: center;
  }

  .script-param-remove {
    appearance: none;
    border: 1px solid transparent;
    background: transparent;
    color: var(--wa-color-text-quiet);
    width: 32px;
    height: 32px;
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .script-param-remove:hover:not(:disabled) {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .script-param-remove:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* Standalone "+ Add parameter" button — same modest styling as
     the nested action-list add buttons (not the prominent
     full-width primary). */
  .script-param-add {
    align-self: flex-start;
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    appearance: none;
    border: 1px dashed var(--wa-color-neutral-border-quiet, #d1d5db);
    background: transparent;
    color: var(--wa-color-text-quiet);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    margin-top: var(--wa-space-2xs);
  }

  .script-param-add:hover:not(:disabled) {
    border-color: var(--wa-color-brand-fill-loud, #0b5cad);
    color: var(--wa-color-brand-fill-loud, #0b5cad);
  }

  .script-param-add:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .ae-section-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0 0 var(--wa-space-2xs) 0;
  }

  .ae-muted {
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-2xs);
    margin-left: var(--wa-space-2xs);
  }

  .ae-row {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    padding: var(--wa-space-m);
    border: 1px solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-raised);
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
  }

  .ae-row:hover {
    border-color: color-mix(in srgb, var(--wa-color-text-normal), transparent 80%);
    box-shadow:
      0 1px 2px rgba(0, 0, 0, 0.03),
      0 2px 8px rgba(0, 0, 0, 0.04);
  }

  .ae-row.ae-row--collapsed {
    gap: 0;
    padding: var(--wa-space-xs) var(--wa-space-m);
  }

  .ae-row-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-m);
    min-width: 0;
  }

  .ae-row-body {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    min-width: 0;
  }

  .ae-row-desc {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  /* Each action / condition row lives inside its own custom
     element shadow, so .ae-row + .ae-row would never match — the
     rows aren't siblings in any one tree. The selector below
     targets where the elements ARE siblings (inside the
     action-list / condition-tree shadow), and that's exactly
     where the rule fires because the list/tree pulls in this same
     stylesheet. */
  esphome-automation-action-node + esphome-automation-action-node,
  esphome-automation-condition-node + esphome-automation-condition-node {
    margin-top: var(--wa-space-m);
    display: block;
  }

  .ae-row-picker {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    appearance: none;
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    cursor: pointer;
    color: var(--wa-color-text-normal);
    text-align: left;
    min-width: 0;
    font-family: inherit;
    transition: color 0.12s;
  }

  .ae-row-picker:hover:not(:disabled) {
    color: var(--wa-color-brand-fill-loud, var(--esphome-primary));
  }

  .ae-row-picker:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .ae-row-picker-name {
    font-size: var(--wa-font-size-m);
    font-weight: var(--wa-font-weight-bold);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .ae-row-picker wa-icon {
    color: var(--wa-color-text-quiet);
    font-size: 14px;
    flex: 0 0 auto;
    opacity: 0.7;
    transition:
      opacity 0.12s,
      color 0.12s;
  }

  .ae-row-picker:hover:not(:disabled) wa-icon {
    color: var(--wa-color-brand-fill-loud, var(--esphome-primary));
    opacity: 1;
  }

  /* Horizontal toolbar living in the row header, opposite the
     title cluster. Was vertical when the layout was a 2-column
     grid; now the header is a single flex row, so a horizontal
     toolbar reads more naturally next to the title. */
  .ae-row-controls {
    display: flex;
    flex-direction: row;
    gap: 2px;
    align-items: center;
    flex: 0 0 auto;
  }

  /* Compact circular icon buttons matching the per-row edit/delete
     pattern used by the api-actions / automations tables in the
     section editor. The wa-icon child's font-size is left at its
     default so the glyph keeps the same size — only the hit-target
     shrinks and rounds around it. */
  .ae-row-controls button {
    appearance: none;
    border: 1px solid transparent;
    background: transparent;
    color: var(--wa-color-text-quiet);
    width: 26px;
    height: 26px;
    border-radius: 6px;
    cursor: pointer;
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .ae-row-controls button:hover:not(:disabled) {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
  }

  /* Destructive variant — same shape as siblings but a red-tinted
     hover wash + red glyph colour, mirroring the api-actions-row-
     delete treatment so destructive intent reads consistently
     across the app. */
  .ae-row-controls .ae-row-delete:hover:not(:disabled) {
    background: color-mix(in srgb, var(--esphome-error), transparent 90%);
    color: var(--esphome-error);
  }

  .ae-row-controls button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* Nested action list — indents children of a control-flow action
     so the tree structure reads at a glance. */
  .ae-nested {
    margin-top: var(--wa-space-s);
    margin-left: var(--wa-space-m);
    padding-left: var(--wa-space-m);
    border-left: 2px solid var(--wa-color-neutral-border-quiet, #e1e4e8);
  }

  .ae-nested-label {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: var(--wa-space-2xs);
  }

  /* Add button — used at the bottom of every list. The default is
     a modest dashed affordance for nested lists (then/else inside
     an "if"). The top-level list (wrapped in .ae-section) gets
     the prominent overlay below — that's the primary "Add action"
     / "Add condition" the user reaches for from a fresh
     automation, so it should pop. */
  /* Bespoke value + unit picker the Delay action uses instead of
     its six separate time-component string inputs. Keeps the user
     in the same "one knob" mental model as the interval form
     (which is a single time_period string). */
  .ae-delay-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--wa-space-m);
  }
  .ae-delay-row .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    margin-bottom: var(--wa-space-2xs);
    display: block;
  }
  .ae-delay-row input,
  .ae-delay-row select {
    width: 100%;
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border: 1px solid var(--wa-color-neutral-border-quiet, #d1d5db);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-default);
    font-size: var(--wa-font-size-s);
    box-sizing: border-box;
  }

  .ae-add {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--wa-space-2xs);
    width: 100%;
    appearance: none;
    border: 1px solid var(--wa-color-brand-fill-loud, var(--esphome-primary));
    background: var(--esphome-primary-light);
    color: var(--wa-color-brand-fill-loud, var(--esphome-primary));
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    margin-top: var(--wa-space-s);
    transition:
      background 0.12s,
      border-color 0.12s,
      color 0.12s;
  }

  .ae-add:hover:not(:disabled) {
    background: color-mix(
      in srgb,
      var(--wa-color-brand-fill-loud, var(--esphome-primary)) 18%,
      transparent
    );
  }

  .ae-add:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Nested add buttons (inside then / else / while / repeat) —
     dashed, quiet so the eye reads the prominent outer button as
     the primary CTA. :host-context() reaches across the
     action-list's shadow boundary into the parent action-node's
     .ae-nested wrapper, which is the only way a sibling
     custom-element with its own shadow can scope the rule. They
     still pick up the brand color on hover for affordance. */
  :host-context(.ae-nested) .ae-add {
    border: 1px dashed var(--wa-color-neutral-border-quiet, #d1d5db);
    color: var(--wa-color-text-quiet);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }

  :host-context(.ae-nested) .ae-add:hover:not(:disabled) {
    border-color: var(--wa-color-brand-fill-loud, #0b5cad);
    color: var(--wa-color-brand-fill-loud, #0b5cad);
    background: transparent;
  }

  .ae-error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .ae-empty {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-style: italic;
  }

  .ae-actions-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
  }

  .ae-section-add {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    background: var(--wa-color-brand-fill-loud, var(--esphome-primary));
    color: var(--wa-color-brand-on-loud, var(--esphome-on-primary));
    border: var(--wa-border-width-s) solid
      var(--wa-color-brand-fill-loud, var(--esphome-primary));
    padding: 2px var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-semibold);
    font-family: inherit;
    transition:
      background 0.12s,
      border-color 0.12s;
  }

  .ae-section-add:hover:not(:disabled) {
    background: color-mix(
      in srgb,
      var(--wa-color-brand-fill-loud, var(--esphome-primary)),
      black 10%
    );
    border-color: color-mix(
      in srgb,
      var(--wa-color-brand-fill-loud, var(--esphome-primary)),
      black 10%
    );
  }

  .ae-section-add:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .ae-section-add wa-icon {
    font-size: 14px;
  }

  .ae-empty-block {
    margin: 0;
    padding: var(--wa-space-m) var(--wa-space-s);
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    font-style: italic;
    border: 1px dashed var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-lowered, transparent);
  }

  /* Bottom-of-editor save / delete buttons. */
  .ae-actions {
    display: flex;
    gap: var(--wa-space-s);
    margin-top: var(--wa-space-m);
    justify-content: flex-end;
  }

  .ae-actions button {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    appearance: none;
    border: 1px solid transparent;
    padding: var(--wa-space-2xs) var(--wa-space-m);
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
  }

  .ae-actions .ae-primary {
    background: var(--wa-color-brand-fill-loud, #0b5cad);
    color: white;
  }

  .ae-actions .ae-primary:hover:not(:disabled) {
    filter: brightness(1.05);
  }

  .ae-actions .ae-danger {
    gap: 4px;
    background: #e54d2e;
    color: #ffffff;
    border: var(--wa-border-width-s) solid #e54d2e;
    padding: var(--wa-space-xs) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    transition:
      background 0.12s,
      border-color 0.12s;
  }

  .ae-actions .ae-danger:hover:not(:disabled) {
    background: color-mix(in srgb, #e54d2e, black 10%);
    border-color: color-mix(in srgb, #e54d2e, black 10%);
  }

  .ae-actions .ae-danger wa-icon {
    font-size: 16px;
  }

  .ae-actions button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;function iq(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({close:s.mdiClose,magnify:s.mdiMagnify,plus:s.mdiPlus});class iS extends l.WF{open(){this._activeTab="action"===this.kind?"by-target":"by-type",this._query="",this._open=!0}render(){let e="action"===this.kind?this._localize("device.automation_pick_action"):this._localize("device.automation_pick_condition"),t=this._localize("device.automation_pick_search"),i="action"===this.kind?["by-target","by-type","building-blocks"]:["by-type","building-blocks"];return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      .label=${e}
      @request-close=${this._onRequestClose}
    >
      <div class="picker-search">
        <div class="picker-search-wrap">
          <wa-icon
            class="picker-search-icon"
            library="mdi"
            name="magnify"
            aria-hidden="true"
          ></wa-icon>
          <input
            class="picker-search-input"
            type="search"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            aria-label=${t}
            .value=${this._query}
            placeholder=${t}
            @input=${e=>this._query=e.target.value}
          />
        </div>
      </div>
      <div class="picker-tabs" role="tablist">
        ${i.map(e=>(0,l.qy)`<button
              type="button"
              role="tab"
              class="picker-tab ${this._activeTab===e?"active":""}"
              aria-selected=${this._activeTab===e}
              @click=${()=>this._activeTab=e}
            >
              ${this._tabLabel(e)}
            </button>`)}
      </div>
      <div class="picker-body" role="tabpanel">${this._renderActiveTab()}</div>
    </esphome-base-dialog>`}_tabLabel(e){switch(e){case"by-target":return this._localize("device.automation_pick_tab_by_target");case"by-type":return this._localize("device.automation_pick_tab_by_type");case"building-blocks":return this._localize("device.automation_pick_tab_building_blocks")}}_renderActiveTab(){let e=this._applyQuery(this.items);switch(this._activeTab){case"by-target":return this._renderByTarget(e);case"by-type":return this._renderByType(e);case"building-blocks":return this._renderBuildingBlocks(e)}}_applyQuery(e){let t=this._query.trim().toLowerCase();return t?e.filter(e=>e.id.toLowerCase().includes(t)||e.name.toLowerCase().includes(t)||(e.description??"").toLowerCase().includes(t)):e}_renderByTarget(e){if(0===this.devices.length)return(0,l.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_targets")}
      </p>`;let t=this.devices.map(t=>{let[i]=t.component_id.split("."),a=e.filter(e=>"domain"in e&&(e.domain===i||e.domain===t.component_id));return{device:t,matching:a}}).filter(e=>e.matching.length>0);return 0===t.length?(0,l.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,l.qy)`${t.map(({device:e,matching:t})=>(0,l.qy)`
        <p class="picker-group-label">
          ${e.name??e.id}
          <span class="ae-muted">(${e.component_id})</span>
        </p>
        ${t.map(t=>this._renderRow(t,()=>this._pick(t.id,this._preFillFor(t,e))))}
      `)}`}_renderByType(e){let t=new Map;for(let i of e){if(!("domain"in i)||"core"===i.domain)continue;let e=i.domain.split(".")[0],a=t.get(e)??[];a.push(i),t.set(e,a)}let i=Array.from(t.keys()).sort();return 0===i.length?(0,l.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,l.qy)`${i.map(e=>(0,l.qy)`
        <p class="picker-group-label">${e}</p>
        ${(t.get(e)??[]).map(e=>this._renderRow(e,()=>this._pick(e.id)))}
      `)}`}_renderBuildingBlocks(e){let t=e.filter(e=>"domain"in e&&"core"===e.domain);return 0===t.length?(0,l.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,l.qy)`${t.map(e=>this._renderRow(e,()=>this._pick(e.id)))}`}_renderRow(e,t){return(0,l.qy)`<div
      class="picker-row"
      role="button"
      tabindex="0"
      @click=${t}
      @keydown=${e=>{("Enter"===e.key||" "===e.key)&&(e.preventDefault(),t())}}
    >
      <div class="picker-row-body">
        <span class="picker-row-title">${e.name}</span>
        ${e.description?(0,l.qy)`<span class="picker-row-desc">
              ${(0,es.G)(e.description)}
            </span>`:l.s6}
      </div>
      <span class="picker-row-add" aria-hidden="true">
        <wa-icon library="mdi" name="plus"></wa-icon>
      </span>
    </div>`}_preFillFor(e,t){let[i]=t.component_id.split("."),a=e.config_entries.find(e=>e.references_component===i);if(a)return{[a.key]:t.id}}_pick(e,t){this.dispatchEvent(new CustomEvent("catalog-picked",{detail:{id:e,preFilledParams:t},bubbles:!0,composed:!0})),this._open=!1}constructor(...e){super(...e),this._localize=e=>e,this.kind="action",this.items=[],this.devices=[],this._open=!1,this._activeTab="by-target",this._query="",this._onRequestClose=()=>{this._open=!1}}}function iM(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iS.styles=[m.G,ed.z,(0,l.AH)`
      esphome-base-dialog {
        --width: 640px;
      }

      esphome-base-dialog::part(body) {
        padding: 0;
      }

      /* Search field — mirrors the dashboard's .search-wrap +
         .search-input pattern (absolute-positioned leading icon over
         a fully-chromed native <input> that inherits styling from
         inputStyles). Padding lives on the outer container so the
         input has breathing room from the dialog edges. */
      .picker-search {
        padding: var(--wa-space-l) var(--wa-space-l) var(--wa-space-s);
      }

      .picker-search-wrap {
        position: relative;
      }

      .picker-search-icon {
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 18px;
        color: var(--wa-color-text-quiet);
        pointer-events: none;
        z-index: 1;
      }

      .picker-search-wrap .picker-search-input {
        padding-left: 36px;
      }

      .picker-tabs {
        display: inline-flex;
        align-items: center;
        gap: 2px;
        padding: 4px;
        margin: 0 var(--wa-space-l) var(--wa-space-s);
        background: var(--wa-color-surface-lowered);
        border-radius: var(--wa-border-radius-m);
        color: var(--wa-color-text-quiet);
      }

      .picker-tab {
        appearance: none;
        border: none;
        background: transparent;
        color: inherit;
        padding: 4px var(--wa-space-m);
        font-size: var(--wa-font-size-s);
        font-weight: var(--wa-font-weight-semibold);
        font-family: inherit;
        cursor: pointer;
        border-radius: calc(var(--wa-border-radius-m) - 2px);
        transition:
          background 0.12s,
          color 0.12s,
          box-shadow 0.12s;
      }

      .picker-tab:hover:not(.active) {
        color: var(--wa-color-text-normal);
      }

      .picker-tab.active {
        background: var(--wa-color-surface-raised);
        color: var(--wa-color-text-normal);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
      }

      .picker-body {
        height: min(60vh, 500px);
        min-height: 320px;
        overflow-y: auto;
        padding: 0 var(--wa-space-l) var(--wa-space-l);
      }

      .picker-group-label {
        font-size: var(--wa-font-size-2xs);
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-quiet);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin: var(--wa-space-m) var(--wa-space-2xs) var(--wa-space-2xs);
      }

      .picker-group-label:first-child {
        margin-top: var(--wa-space-2xs);
      }

      .picker-row {
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center;
        gap: var(--wa-space-m);
        padding: var(--wa-space-s) var(--wa-space-m);
        border-radius: var(--wa-border-radius-m);
        cursor: pointer;
        transition: background 0.12s;
      }

      .picker-row:hover,
      .picker-row:focus-visible {
        background: var(--wa-color-surface-lowered);
        outline: none;
      }

      .picker-row-body {
        display: flex;
        flex-direction: column;
        gap: 2px;
        min-width: 0;
      }

      .picker-row-title {
        font-size: var(--wa-font-size-s);
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-normal);
      }

      .picker-row-desc {
        font-size: var(--wa-font-size-2xs);
        color: var(--wa-color-text-quiet);
        line-height: 1.4;
        /* Clamp to two lines — descriptions can be long but the
           picker shouldn't grow each row past a manageable height. */
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .picker-row-add {
        display: grid;
        place-items: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: transparent;
        color: var(--wa-color-text-quiet);
        flex: 0 0 auto;
        line-height: 0;
        transition:
          background 0.12s,
          color 0.12s;
      }

      .picker-row-add wa-icon {
        display: block;
        width: 18px;
        height: 18px;
        font-size: 18px;
        line-height: 0;
      }

      .picker-row:hover .picker-row-add,
      .picker-row:focus-visible .picker-row-add {
        background: var(--wa-color-brand-fill-loud, var(--esphome-primary));
        color: var(--wa-color-brand-on-loud, var(--esphome-on-primary));
      }

      .picker-empty {
        text-align: center;
        color: var(--wa-color-text-quiet);
        font-size: var(--wa-font-size-s);
        padding: var(--wa-space-xl) var(--wa-space-l);
        font-style: italic;
      }
    `],iq([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iS.prototype,"_localize",void 0),iq([(0,d.MZ)()],iS.prototype,"kind",void 0),iq([(0,d.MZ)({attribute:!1})],iS.prototype,"items",void 0),iq([(0,d.MZ)({attribute:!1})],iS.prototype,"devices",void 0),iq([(0,d.wk)()],iS.prototype,"_open",void 0),iq([(0,d.wk)()],iS.prototype,"_activeTab",void 0),iq([(0,d.wk)()],iS.prototype,"_query",void 0),iS=iq([(0,d.EM)("esphome-catalog-picker-dialog")],iS),(0,b.C)({"arrow-down":s.mdiArrowDown,"arrow-up":s.mdiArrowUp,close:s.mdiClose,delete:s.mdiDelete,"pencil-outline":s.mdiPencilOutline,plus:s.mdiPlus});class iL extends l.WF{render(){return(0,l.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?l.s6:(0,l.qy)`<label class="ae-section-label"
              >${this._localize("device.automation_only_when")}</label
            >`}
        ${0===this.conditions.length?(0,l.qy)`<p class="ae-empty">${this._localize("device.add_condition")}</p>`:this.conditions.map((e,t)=>this._renderNode(e,t))}
        <button
          type="button"
          class="ae-add"
          ?disabled=${this.disabled||0===this.catalog.length}
          @click=${this._openPickerForAdd}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("device.add_condition")}
        </button>
        <esphome-catalog-picker-dialog
          kind="condition"
          .items=${this.catalog}
          .devices=${this.devices}
          @catalog-picked=${this._onConditionPicked}
        ></esphome-catalog-picker-dialog>
      </div>
    `}_renderNode(e,t){let i=this.catalog.find(t=>t.id===e.condition_id),a=this.conditions.length-1;return(0,l.qy)`
      <div class="ae-row">
        <div class="ae-row-header">
          <button
            type="button"
            class="ae-row-picker"
            ?disabled=${this.disabled}
            @click=${()=>this._openPickerForChange(t)}
          >
            <span class="ae-row-picker-name"> ${i?.name??e.condition_id} </span>
            <wa-icon library="mdi" name="pencil-outline"></wa-icon>
          </button>
          <div class="ae-row-controls">
            <button
              type="button"
              ?disabled=${this.disabled||0===t}
              aria-label=${this._localize("device.automation_move_up")}
              @click=${()=>this._move(t,t-1)}
            >
              <wa-icon library="mdi" name="arrow-up"></wa-icon>
            </button>
            <button
              type="button"
              ?disabled=${this.disabled||t===a}
              aria-label=${this._localize("device.automation_move_down")}
              @click=${()=>this._move(t,t+1)}
            >
              <wa-icon library="mdi" name="arrow-down"></wa-icon>
            </button>
            <button
              type="button"
              class="ae-row-delete"
              ?disabled=${this.disabled}
              aria-label=${this._localize("device.automation_remove")}
              @click=${()=>this._remove(t)}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
            </button>
          </div>
        </div>
        <div class="ae-row-body">
          ${i?.description?(0,l.qy)`<p class="ae-row-desc">${(0,es.G)(i.description)}</p>`:l.s6}
          ${i&&i.config_entries.length>0?(0,l.qy)`<esphome-config-entry-form
                .entries=${i.config_entries}
                .values=${e.params}
                .board=${this.board}
                .yaml=${this.yaml}
                ?disabled=${this.disabled}
                @value-change=${e=>this._onParamChange(t,e)}
              ></esphome-config-entry-form>`:l.s6}
          ${i?.accepts_condition_list?(0,l.qy)`<div class="ae-nested">
                <p class="ae-nested-label">
                  ${this._localize("device.automation_condition")}
                </p>
                <esphome-automation-condition-tree
                  no-header
                  .conditions=${e.children??[]}
                  .catalog=${this.catalog}
                  .devices=${this.devices}
                  .board=${this.board}
                  .yaml=${this.yaml}
                  ?disabled=${this.disabled}
                  @conditions-change=${e=>this._onChildrenChange(t,e)}
                ></esphome-automation-condition-tree>
              </div>`:l.s6}
        </div>
      </div>
    `}_openPickerForChange(e){0!==this.catalog.length&&(this._changingIdx=e,this._picker.open())}_onParamChange(e,t){t.stopPropagation();let i=this.conditions[e],a=ep(i.params,t.detail.path,t.detail.value);this._emit(eu(this.conditions,e,{...i,params:a}))}_onChildrenChange(e,t){t.stopPropagation();let i=this.conditions[e];this._emit(eu(this.conditions,e,{...i,children:t.detail.conditions}))}_move(e,t){this._emit(ev(this.conditions,e,t))}_remove(e){this._emit(em(this.conditions,e))}_emit(e){this.dispatchEvent(new CustomEvent("conditions-change",{detail:{conditions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.conditions=[],this.catalog=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.devices=[],this._changingIdx=-1,this._openPickerForAdd=()=>{0!==this.catalog.length&&(this._changingIdx=-1,this._picker.open())},this._onConditionPicked=e=>{e.stopPropagation();let t={condition_id:e.detail.id,params:{},children:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._changingIdx>=0?this._emit(eu(this.conditions,this._changingIdx,t)):this._emit([...this.conditions,t]),this._changingIdx=-1}}}function iP(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iL.styles=[m.G,ed.z,iA],iM([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iL.prototype,"_localize",void 0),iM([(0,d.MZ)({attribute:!1})],iL.prototype,"conditions",void 0),iM([(0,d.MZ)({attribute:!1})],iL.prototype,"catalog",void 0),iM([(0,d.MZ)({attribute:!1})],iL.prototype,"board",void 0),iM([(0,d.MZ)()],iL.prototype,"yaml",void 0),iM([(0,d.MZ)({type:Boolean})],iL.prototype,"disabled",void 0),iM([(0,d.MZ)({type:Boolean,attribute:"no-header"})],iL.prototype,"noHeader",void 0),iM([(0,d.MZ)({attribute:!1})],iL.prototype,"devices",void 0),iM([(0,d.P)("esphome-catalog-picker-dialog")],iL.prototype,"_picker",void 0),iM([(0,d.wk)()],iL.prototype,"_changingIdx",void 0),iL=iM([(0,d.EM)("esphome-automation-condition-tree")],iL),(0,b.C)({"arrow-down":s.mdiArrowDown,"arrow-up":s.mdiArrowUp,"chevron-down":s.mdiChevronDown,"chevron-up":s.mdiChevronUp,close:s.mdiClose,delete:s.mdiDelete,"pencil-outline":s.mdiPencilOutline});let iF=["us","ms","s","min","h","d"],iT={us:"microseconds",ms:"milliseconds",s:"seconds",min:"minutes",h:"hours",d:"days"};class iR extends l.WF{willUpdate(e){if(!e.has("value"))return;let t=e.get("value");t&&t.action_id!==this.value.action_id&&(this._collapsed=!1,this._showAdvanced=!1)}render(){let e=this.catalog.find(e=>e.id===this.value.action_id),t=this._collapsed;return(0,l.qy)`
      <div class="ae-row ${t?"ae-row--collapsed":""}">
        <div class="ae-row-header">
          <button
            type="button"
            class="ae-row-picker"
            ?disabled=${this.disabled}
            title=${this._localize("device.automation_action_pick")}
            @click=${this._openPicker}
          >
            <span class="ae-row-picker-name"> ${e?.name??this.value.action_id} </span>
            <wa-icon library="mdi" name="pencil-outline"></wa-icon>
          </button>
          <div class="ae-row-controls">
            <button
              type="button"
              aria-label=${t?this._localize("device.automation_action_expand"):this._localize("device.automation_action_collapse")}
              aria-expanded=${t?"false":"true"}
              @click=${()=>{this._collapsed=!this._collapsed}}
            >
              <wa-icon
                library="mdi"
                name=${t?"chevron-down":"chevron-up"}
              ></wa-icon>
            </button>
            <button
              type="button"
              ?disabled=${this.disabled||this.first}
              aria-label=${this._localize("device.automation_move_up")}
              @click=${()=>this._reorder(-1)}
            >
              <wa-icon library="mdi" name="arrow-up"></wa-icon>
            </button>
            <button
              type="button"
              ?disabled=${this.disabled||this.last}
              aria-label=${this._localize("device.automation_move_down")}
              @click=${()=>this._reorder(1)}
            >
              <wa-icon library="mdi" name="arrow-down"></wa-icon>
            </button>
            <button
              type="button"
              class="ae-row-delete"
              ?disabled=${this.disabled}
              aria-label=${this._localize("device.automation_remove")}
              @click=${this._onDelete}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
            </button>
          </div>
        </div>
        <esphome-catalog-picker-dialog
          kind="action"
          .items=${this.catalog}
          .devices=${this.devices}
          @catalog-picked=${this._onActionPicked}
        ></esphome-catalog-picker-dialog>
        ${t?l.s6:(0,l.qy)`<div class="ae-row-body">
              ${e?.description?(0,l.qy)`<p class="ae-row-desc">${(0,es.G)(e.description)}</p>`:l.s6}
              ${this._renderActionParams(e)} ${this._renderScriptParams(e)}
              ${this._renderConditionGate(e)} ${this._renderNestedLists(e)}
            </div>`}
      </div>
    `}_renderScriptParams(e){if(e?.id!=="script.execute")return l.s6;let t=String(this.value.params.id??""),i=this.scripts.find(e=>e.id===t);return i&&0!==i.parameters.length?(0,l.qy)`<div class="ae-nested">
      <p class="ae-nested-label">
        ${this._localize("device.automation_script_parameters")}
      </p>
      ${i.parameters.map(e=>(0,l.qy)`<label class="ae-section-label" for="script-${e.name}"
              >${e.name} <span class="ae-muted">${e.type}</span></label
            >
            <input
              id="script-${e.name}"
              type=${"int"===e.type||"float"===e.type?"number":"text"}
              ?disabled=${this.disabled}
              .value=${String(this.value.params[e.name]??"")}
              @input=${t=>{let i=t.target.value,a="int"===e.type?""===i?"":parseInt(i,10):"float"===e.type?""===i?"":Number(i):i;this._patchParams({[e.name]:a})}}
            />`)}
    </div>`:l.s6}_renderConditionGate(e){return e&&("if"===e.id||"wait_until"===e.id)?(0,l.qy)`<div class="ae-nested">
      <p class="ae-nested-label">${this._localize("device.automation_only_when")}</p>
      <esphome-automation-condition-tree
        no-header
        .conditions=${this.value.conditions??[]}
        .catalog=${this.conditionCatalog}
        .devices=${this.devices}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        @conditions-change=${this._onConditionsChange}
      ></esphome-automation-condition-tree>
    </div>`:l.s6}_renderNestedLists(e){return e&&e.accepts_action_list&&0!==e.accepts_action_list.length?e.accepts_action_list.map(e=>(0,l.qy)`<div class="ae-nested">
          <p class="ae-nested-label">
            ${"else"===e?this._localize("device.automation_else"):this._localize("device.automation_action")}
          </p>
          <esphome-automation-action-list
            no-header
            .actions=${this.value.children?.[e]??[]}
            .catalog=${this.catalog}
            .conditionCatalog=${this.conditionCatalog}
            .scripts=${this.scripts}
            .devices=${this.devices}
            .board=${this.board}
            .yaml=${this.yaml}
            ?disabled=${this.disabled}
            @actions-change=${t=>{t.stopPropagation(),this._onChildrenChange(e,t.detail.actions)}}
          ></esphome-automation-action-list>
        </div>`):l.s6}_renderActionParams(e){var t,i;let a;if(!e)return l.s6;if("delay"===e.id)return this._renderDelayParams();if(0===e.config_entries.length)return l.s6;let{showAdvanced:o,showToggle:r}=(t=e.config_entries,i=this._showAdvanced,{showAdvanced:(a=t.length>0&&t.every(e=>e.advanced))||i,showToggle:iC(t)&&!a});return(0,l.qy)`<esphome-config-entry-form
        .entries=${e.config_entries}
        .values=${this.value.params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        ?show-advanced=${o}
        @value-change=${this._onParamChange}
      ></esphome-config-entry-form>
      ${r?iE(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}`}_renderDelayParams(){let{value:e,unit:t}=this._readDelay();return(0,l.qy)`<div class="ae-delay-row">
      <div class="ae-delay-value">
        <label class="field-label" for="ae-delay-value-input">
          ${this._localize("device.automation_action_delay_value")}
        </label>
        <input
          id="ae-delay-value-input"
          type="text"
          inputmode="decimal"
          .value=${e}
          placeholder="0"
          ?disabled=${this.disabled}
          @input=${e=>this._writeDelay(e.target.value,t)}
        />
      </div>
      <div class="ae-delay-unit">
        <label class="field-label" for="ae-delay-unit-select">
          ${this._localize("device.automation_action_delay_unit")}
        </label>
        <select
          id="ae-delay-unit-select"
          ?disabled=${this.disabled}
          @change=${t=>this._writeDelay(e,t.target.value)}
        >
          ${iF.map(e=>(0,l.qy)`<option value=${e} ?selected=${e===t}>
                ${this._localize(`device.automation_action_delay_unit_${e}`)}
              </option>`)}
        </select>
      </div>
    </div>`}_readDelay(){let e=this.value.params??{};for(let t of iF){let i=e[iT[t]];if(void 0!==i&&""!==i&&null!==i)return{value:String(i),unit:t}}let t=e.id;if("string"==typeof t){let e=t.match(/^(\d+(?:\.\d+)?)(us|ms|s|min|h|d)$/);if(e){let[,t,i]=e;return{value:t,unit:i}}}return{value:"",unit:"s"}}_writeDelay(e,t){let i=e.trim(),a={...this.value.params??{}};for(let e of iF)delete a[iT[e]];delete a.id,i&&(a[iT[t]]=i),this._emit({...this.value,params:a})}_patchParams(e){this._emit({...this.value,params:{...this.value.params,...e}})}_onChildrenChange(e,t){let i={...this.value.children??{},[e]:t};this._emit({...this.value,children:i})}_reorder(e){this.dispatchEvent(new CustomEvent("action-reorder",{detail:{delta:e},bubbles:!0,composed:!0}))}_emit(e){this.dispatchEvent(new CustomEvent("action-change",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.first=!1,this.last=!1,this._collapsed=!1,this._showAdvanced=!1,this._openPicker=()=>{this._picker.open()},this._onActionPicked=e=>{e.stopPropagation(),this._emit({action_id:e.detail.id,params:{...e.detail.preFilledParams??{}},children:{},conditions:[]})},this._onParamChange=e=>{e.stopPropagation();let t=ep(this.value.params,e.detail.path,e.detail.value);this._emit({...this.value,params:t})},this._onConditionsChange=e=>{e.stopPropagation(),this._emit({...this.value,conditions:e.detail.conditions})},this._onDelete=()=>{this.dispatchEvent(new CustomEvent("action-delete",{bubbles:!0,composed:!0}))}}}function iD(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iR.styles=[m.G,ed.z,iA],iP([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iR.prototype,"_localize",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"value",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"catalog",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"conditionCatalog",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"scripts",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"devices",void 0),iP([(0,d.MZ)({attribute:!1})],iR.prototype,"board",void 0),iP([(0,d.MZ)()],iR.prototype,"yaml",void 0),iP([(0,d.MZ)({type:Boolean})],iR.prototype,"disabled",void 0),iP([(0,d.MZ)({type:Boolean})],iR.prototype,"first",void 0),iP([(0,d.MZ)({type:Boolean})],iR.prototype,"last",void 0),iP([(0,d.P)("esphome-catalog-picker-dialog")],iR.prototype,"_picker",void 0),iP([(0,d.wk)()],iR.prototype,"_collapsed",void 0),iP([(0,d.wk)()],iR.prototype,"_showAdvanced",void 0),iR=iP([(0,d.EM)("esphome-automation-action-node")],iR),(0,b.C)({plus:s.mdiPlus});class iI extends l.WF{render(){return(0,l.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?l.s6:(0,l.qy)`<label class="ae-section-label"
              >${this._localize("device.automation_action")}</label
            >`}
        ${0===this.actions.length?(0,l.qy)`<p class="ae-empty-block" role="status">
              ${this._localize("device.automation_actions_empty")}
            </p>`:this.actions.map((e,t)=>this._renderRow(e,t,t===this.actions.length-1))}
        ${this.hideAdd?l.s6:(0,l.qy)`<button
              type="button"
              class="ae-add"
              ?disabled=${this.disabled||0===this.catalog.length}
              @click=${this.openPicker}
            >
              <wa-icon library="mdi" name="plus"></wa-icon>
              ${this._localize("device.add_action")}
            </button>`}
        <esphome-catalog-picker-dialog
          kind="action"
          .items=${this.catalog}
          .devices=${this.devices}
          @catalog-picked=${this._onActionPicked}
        ></esphome-catalog-picker-dialog>
      </div>
    `}_renderRow(e,t,i){return(0,l.qy)`<esphome-automation-action-node
      .value=${e}
      .catalog=${this.catalog}
      .conditionCatalog=${this.conditionCatalog}
      .scripts=${this.scripts}
      .devices=${this.devices}
      .board=${this.board}
      .yaml=${this.yaml}
      ?disabled=${this.disabled}
      ?first=${0===t}
      ?last=${i}
      @action-change=${e=>this._onActionChange(t,e)}
      @action-reorder=${e=>this._onReorder(t,e)}
      @action-delete=${e=>this._onDelete(t,e)}
    ></esphome-automation-action-node>`}_onActionChange(e,t){t.stopPropagation(),this._emit(eu(this.actions,e,t.detail.value))}_onReorder(e,t){t.stopPropagation(),this._emit(ev(this.actions,e,e+t.detail.delta))}_onDelete(e,t){t.stopPropagation(),this._emit(em(this.actions,e))}_emit(e){this.dispatchEvent(new CustomEvent("actions-change",{detail:{actions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.actions=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.hideAdd=!1,this.openPicker=()=>{0!==this.catalog.length&&this._picker.open()},this._onActionPicked=e=>{e.stopPropagation();let t={action_id:e.detail.id,params:{},children:{},conditions:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._emit([...this.actions,t])}}}function iO(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iI.styles=[m.G,ed.z,iA],iD([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iI.prototype,"_localize",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"actions",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"catalog",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"conditionCatalog",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"scripts",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"devices",void 0),iD([(0,d.MZ)({attribute:!1})],iI.prototype,"board",void 0),iD([(0,d.MZ)()],iI.prototype,"yaml",void 0),iD([(0,d.MZ)({type:Boolean})],iI.prototype,"disabled",void 0),iD([(0,d.MZ)({type:Boolean,attribute:"no-header"})],iI.prototype,"noHeader",void 0),iD([(0,d.MZ)({type:Boolean,attribute:"hide-add"})],iI.prototype,"hideAdd",void 0),iD([(0,d.P)("esphome-catalog-picker-dialog")],iI.prototype,"_picker",void 0),iI=iD([(0,d.EM)("esphome-automation-action-list")],iI),(0,b.C)({close:s.mdiClose,plus:s.mdiPlus});let ij=["int","float","bool","string"];class iN extends l.WF{updated(e){if(!e.has("value"))return;let t=this._readFromWire(),i=this._params.filter(e=>e.name);i.length===t.length&&i.every((e,i)=>e.name===t[i].name&&e.type===t[i].type)||(this._params=t)}render(){return(0,l.qy)`<div class="field">
      ${this.fieldLabel?(0,l.qy)`<label class="field-label">${this.fieldLabel}</label>`:l.s6}
      ${this.description?(0,l.qy)`<p class="field-description">${(0,es.G)(this.description)}</p>`:l.s6}
      ${0===this._params.length?l.s6:(0,l.qy)`<div class="script-params-list">
            ${this._params.map((e,t)=>this._renderRow(e,t))}
          </div>`}
      <button
        type="button"
        class="script-param-add"
        ?disabled=${this.disabled}
        @click=${this._addRow}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${this.addLabel}
      </button>
    </div>`}_renderRow(e,t){return(0,l.qy)`<div class="script-param-row">
      <input
        type="text"
        ?disabled=${this.disabled}
        placeholder=${this.namePlaceholder}
        .value=${e.name}
        @input=${i=>this._updateRow(t,{...e,name:iz(i.target.value)})}
      />
      <wa-select
        value=${e.type}
        ?disabled=${this.disabled}
        @change=${i=>this._updateRow(t,{...e,type:i.target.value})}
      >
        ${ij.map(t=>(0,l.qy)`<wa-option value=${t} ?selected=${t===e.type}>${t}</wa-option>`)}
      </wa-select>
      <button
        type="button"
        class="script-param-remove"
        ?disabled=${this.disabled}
        aria-label=${this._localize("device.automation_remove")}
        @click=${()=>this._removeRow(t)}
      >
        <wa-icon library="mdi" name="close"></wa-icon>
      </button>
    </div>`}_readFromWire(){return this.value&&"object"==typeof this.value?Object.entries(this.value).map(([e,t])=>({name:e,type:String(t??"string")})):[]}_emit(e){this._params=e;let t={};for(let{name:i,type:a}of e)i&&(t[i]=a);this.dispatchEvent(new CustomEvent("value-change",{detail:{value:t},bubbles:!0,composed:!0}))}_updateRow(e,t){let i=this._params.slice();i[e]=t,this._emit(i)}_removeRow(e){let t=this._params.slice();t.splice(e,1),this._emit(t)}constructor(...e){super(...e),this._localize=e=>e,this.value={},this.disabled=!1,this.fieldLabel="",this.description="",this.addLabel="",this.namePlaceholder="",this._params=[],this._addRow=()=>{this._emit([...this._params,{name:"",type:"int"}])}}}iN.styles=[m.G,ed.z,iA],iO([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iN.prototype,"_localize",void 0),iO([(0,d.MZ)({attribute:!1})],iN.prototype,"value",void 0),iO([(0,d.MZ)({type:Boolean})],iN.prototype,"disabled",void 0),iO([(0,d.MZ)()],iN.prototype,"fieldLabel",void 0),iO([(0,d.MZ)()],iN.prototype,"description",void 0),iO([(0,d.MZ)()],iN.prototype,"addLabel",void 0),iO([(0,d.MZ)()],iN.prototype,"namePlaceholder",void 0),iO([(0,d.wk)()],iN.prototype,"_params",void 0),iN=iO([(0,d.EM)("esphome-callable-params-editor")],iN);class iZ{hostConnected(){}get active(){return this._active}resolve(e,t,i){let a=eg(t),o=e.find(e=>eg(e.location)===a);return!o||i&&o.location.kind!==i?(this._set(null),null):(this._set(o.error??null),null!=o.error)?null:{tree:o.automation,location:o.location}}renderPanel(e){return(0,l.qy)`<div class="ae-empty-block" role="alert">
      <p class="ae-error">${e("device.automation_parse_error")}</p>
      ${this._message?(0,l.qy)`<p>${this._message}</p>`:l.s6}
    </div>`}_set(e){let t=null!=e;(this._active!==t||this._message!==(e??""))&&(this._active=t,this._message=e??"",this._host.requestUpdate())}constructor(e){this._host=e,this._active=!1,this._message="",e.addController(this)}}function iB(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({delete:s.mdiDelete,"open-in-new":s.mdiOpenInNew,webhook:s.mdiWebhook});class iK extends l.WF{get dirty(){return this._dirty}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._load(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.action_name!==this.location.action_name&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??eh(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._deleting;return(0,l.qy)`
      ${this._renderHeader()} ${this._renderActionNameField(r)}
      <esphome-callable-params-editor
        .value=${e.trigger_params.variables??{}}
        ?disabled=${r}
        .fieldLabel=${this._localize("device.api_action_variables")}
        .description=${this._localize("device.api_action_variables_description")}
        .addLabel=${this._localize("device.api_action_add_variable")}
        .namePlaceholder=${this._localize("device.api_action_variable_name_placeholder")}
        @value-change=${this._onVariablesChange}
      ></esphome-callable-params-editor>
      <div class="field">
        <label class="field-label"> ${this._localize("device.automation_action")} </label>
        <p class="field-description">
          ${(0,es.G)(this._localize("device.api_action_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          .actions=${e.actions}
          .catalog=${a}
          .conditionCatalog=${o}
          .scripts=${i}
          .devices=${t}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${r}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,l.qy)`<p class="ae-error" role="alert">${this._error}</p>`:l.s6}
      ${this.location&&this.value&&!this.addMode?(0,l.qy)`<div class="ae-actions">
            <button
              type="button"
              class="ae-danger"
              ?disabled=${r}
              @click=${this._onDelete}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
              ${this._localize("dashboard.delete")}
            </button>
          </div>`:l.s6}
    `}_renderHeader(){return(0,l.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">
          ${this._localize("device.api_action_header_title_static")}
        </h2>
        <a class="ae-header-docs" href=${"https://esphome.io/components/api.html"} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">
          ${(0,es.G)(this._localize("device.api_action_header_description"))}
        </p>
      </div>
      <div class="ae-header-icon">
        <wa-icon library="mdi" name="webhook"></wa-icon>
      </div>
    </div>`}_renderActionNameField(e){let t=this.location?.action_name??"";return(0,l.qy)`<div class="field">
      <label class="field-label" for="api-action-name">
        ${this._localize("device.api_action_id_label")}
      </label>
      <p class="field-description">
        ${(0,es.G)(this._localize("device.api_action_id_description"))}
      </p>
      <input
        id="api-action-name"
        type="text"
        .value=${t}
        ?disabled=${e}
        ?readonly=${!this.addMode}
        @input=${e=>this._onActionNameChange(e.target.value)}
      />
    </div>`}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable()}catch(e){this._error=e instanceof Error?e.message:String(e)}finally{this._loading=!1}}}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration)}catch(e){this._error=e instanceof Error?e.message:String(e)}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"api_action");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_onActionNameChange(e){let t=iz(e);t&&(this.location={kind:"api_action",action_name:t},this._scheduleAutoApply())}_withValue(e){let t={...this.value??eh(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this.location.action_name){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=ef(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new iZ(this),this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._onVariablesChange=e=>{e.stopPropagation();let t=this.value??eh();this._withValue({trigger_params:{...t.trigger_params,variables:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=ef(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}function iU(e,t){let i=((e.endsWith("_action")?e.slice(0,-7):e)||e).replace(/_/g," ").trim()||"action";return t("device.action_field_label",{name:i[0].toUpperCase()+i.slice(1)})}function iH(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iK.styles=[m.G,ed.z,iA],iB([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iK.prototype,"_localize",void 0),iB([(0,n.Fg)({context:u.Ie})],iK.prototype,"_api",void 0),iB([(0,d.MZ)()],iK.prototype,"configuration",void 0),iB([(0,d.MZ)({attribute:!1})],iK.prototype,"board",void 0),iB([(0,d.MZ)()],iK.prototype,"platform",void 0),iB([(0,d.MZ)({attribute:!1})],iK.prototype,"value",void 0),iB([(0,d.MZ)({attribute:!1})],iK.prototype,"location",void 0),iB([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],iK.prototype,"addMode",void 0),iB([(0,d.MZ)()],iK.prototype,"yaml",void 0),iB([(0,d.wk)()],iK.prototype,"_available",void 0),iB([(0,d.wk)()],iK.prototype,"_loading",void 0),iB([(0,d.wk)()],iK.prototype,"_deleting",void 0),iB([(0,d.wk)()],iK.prototype,"_error",void 0),iB([(0,d.wk)()],iK.prototype,"_dirty",void 0),iK=iB([(0,d.EM)("esphome-api-action-editor")],iK);let iW=["device_on","component_on","interval","script"];class iV extends l.WF{render(){let e=this.value&&"component_action"!==this.value.kind?this.value.kind:"device_on";return(0,l.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="target-kind-label"
          >${this._localize("device.automation_target")}</label
        >
        <wa-select
          aria-labelledby="target-kind-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${this._onKindChange}
        >
          ${iW.map(t=>(0,l.qy)`<wa-option value=${t} ?selected=${t===e}
                >${this._kindLabel(t)}</wa-option
              >`)}
        </wa-select>
        ${this._renderKindBody(e)}
      </div>
    `}_kindLabel(e){switch(e){case"device_on":return this._localize("device.automation_target_device");case"component_on":return this._localize("device.automation_target_component");case"interval":return this._localize("device.automation_target_interval");case"script":return this._localize("device.automation_target_script");case"api_action":return this._localize("device.automation_target_api_action");case"light_effect":return this._localize("device.automation_light_effect")}}_renderKindBody(e){if("device_on"===e||"interval"===e)return l.s6;if("component_on"===e){let e=this.value?.kind==="component_on"?this.value.component_id:"";return 0===this.devices.length?(0,l.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_components")}
        </p>`:(0,l.qy)`
        <label class="ae-section-label" id="component-id-label"
          >${this._localize("device.automation_target_component_label")}</label
        >
        <wa-select
          aria-labelledby="component-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onComponentChange(e.target.value)}
        >
          ${this.devices.map(t=>(0,l.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${t.name??t.id}
                <span class="ae-muted">(${t.component_id})</span></wa-option
              >`)}
        </wa-select>
      `}if("script"===e){let e=this.value?.kind==="script"?this.value.id:"";return this.locked?(0,l.qy)`
          <label class="ae-section-label">
            ${this._localize("device.automation_target_script_label")}
          </label>
          <p class="ae-section-desc">${e}</p>
        `:(0,l.qy)`
        <label class="ae-section-label" for="script-id-input">
          ${this._localize("device.automation_target_script_new_id_label")}
        </label>
        <input
          id="script-id-input"
          type="text"
          .value=${e}
          placeholder=${this._localize("device.automation_target_script_id_placeholder")}
          ?disabled=${this.disabled}
          @input=${e=>this._onScriptChange(e.target.value)}
        />
      `}if("api_action"===e){let e=this.value?.kind==="api_action"?this.value.action_name:"";return(0,l.qy)`
        <label class="ae-section-label">
          ${this._localize("device.automation_target_api_action_label")}
        </label>
        <p class="ae-section-desc">${e}</p>
      `}if("light_effect"===e){let e=this.value?.kind==="light_effect"?this.value.component_id:"",t=this.devices.filter(e=>e.component_id.startsWith("light."));return 0===t.length?(0,l.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_lights")}
        </p>`:(0,l.qy)`
        <label class="ae-section-label" id="light-id-label"
          >${this._localize("device.automation_target_light_label")}</label
        >
        <wa-select
          aria-labelledby="light-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onLightChange(e.target.value)}
        >
          ${t.map(t=>(0,l.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${t.name??t.id}</wa-option
              >`)}
        </wa-select>
      `}return l.s6}_onKindChange(e){let t=e.target.value,i=(()=>{switch(t){case"device_on":return{kind:t,trigger:"on_boot"};case"interval":return{kind:t,index:0};case"component_on":return this.devices.length?{kind:t,component_id:this.devices[0].id,trigger:""}:null;case"script":return{kind:t,id:this.scripts.length?this.scripts[0].id:""};case"light_effect":{let e=this.devices.find(e=>e.component_id.startsWith("light."));return e?{kind:t,component_id:e.id,index:0}:null}case"api_action":return null}})();this._emit(i)}_onComponentChange(e){this.value?.kind==="component_on"&&this._emit({...this.value,component_id:e})}_onScriptChange(e){this._emit({kind:"script",id:e})}_onLightChange(e){this.value?.kind==="light_effect"&&this._emit({...this.value,component_id:e})}_emit(e){this.dispatchEvent(new CustomEvent("target-change",{detail:{target:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value=null,this.devices=[],this.scripts=[],this.disabled=!1,this.locked=!1}}function iY(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iV.styles=[m.G,ed.z,iA],iH([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iV.prototype,"_localize",void 0),iH([(0,d.MZ)({attribute:!1})],iV.prototype,"value",void 0),iH([(0,d.MZ)({attribute:!1})],iV.prototype,"devices",void 0),iH([(0,d.MZ)({attribute:!1})],iV.prototype,"scripts",void 0),iH([(0,d.MZ)({type:Boolean})],iV.prototype,"disabled",void 0),iH([(0,d.MZ)({type:Boolean})],iV.prototype,"locked",void 0),iV=iH([(0,d.EM)("esphome-automation-target-picker")],iV);class iG extends l.WF{render(){if(!this.target)return(0,l.qy)`<p class="ae-empty">
        ${this._localize("device.automation_target_placeholder")}
      </p>`;if("interval"===this.target.kind||"script"===this.target.kind||"api_action"===this.target.kind||"light_effect"===this.target.kind)return l.s6;let e=this._filteredTriggers(),t=e.find(e=>e.id===this.triggerId),i="component_on"===this.target.kind?this.target.component_id:null,a=i?this.devices.find(e=>e.id===i)??null:null;return(0,l.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="trigger-label"
          >${this._localize("device.automation_trigger")}</label
        >
        ${a?(0,l.qy)`<p class="ae-section-desc">
              ${this._localize("device.automation_trigger_on_component",{component:a.name??a.id,domain:a.component_id})}
            </p>`:l.s6}
        ${0===e.length?(0,l.qy)`<p class="ae-empty" role="status">
              ${this._localize("device.automation_trigger_none_available")}
            </p>`:(0,l.qy)`<wa-select
              aria-labelledby="trigger-label"
              value=${this.triggerId??""}
              ?disabled=${this.disabled}
              @change=${this._onTriggerChange}
            >
              ${e.map(e=>(0,l.qy)`<wa-option value=${e.id} ?selected=${e.id===this.triggerId}
                    >${e.name}</wa-option
                  >`)}
            </wa-select>`}
        ${t?.description?(0,l.qy)`<p class="ae-section-desc">${(0,es.G)(t.description)}</p>`:l.s6}
        ${t&&t.config_entries.length>0?(0,l.qy)`<esphome-config-entry-form
              .entries=${t.config_entries}
              .values=${this.triggerParams}
              .board=${this.board}
              .yaml=${this.yaml}
              ?disabled=${this.disabled}
              @value-change=${this._onParamChange}
            ></esphome-config-entry-form>`:l.s6}
      </div>
    `}_filteredTriggers(){if(!this.target)return[];if("device_on"===this.target.kind)return this.triggers.filter(e=>e.is_device_level);if("component_on"===this.target.kind){let e=this.target.component_id,t=this.devices.find(t=>t.id===e);if(!t)return[];let[i]=t.component_id.split(".");return this.triggers.filter(e=>!e.is_device_level&&(e.applies_to.includes(t.component_id)||e.applies_to.includes(i)))}return[]}constructor(...e){super(...e),this._localize=e=>e,this.target=null,this.triggers=[],this.devices=[],this.triggerId=null,this.triggerParams={},this.board=null,this.yaml="",this.disabled=!1,this._onTriggerChange=e=>{let t=e.target.value;this.dispatchEvent(new CustomEvent("trigger-change",{detail:{triggerId:t,params:{}},bubbles:!0,composed:!0}))},this._onParamChange=e=>{e.stopPropagation();let t=ep(this.triggerParams,e.detail.path,e.detail.value);this.dispatchEvent(new CustomEvent("trigger-params-change",{detail:{params:t},bubbles:!0,composed:!0}))}}}async function iJ(e,t,i){let a=tB(),o=[],r=(t,r)=>{for(let n of r)o.push(tZ(e,t,n,i).then(e=>{tK(a,e)}))};for(let e of(r("triggers",t.triggers),r("actions",t.actions),r("conditions",t.conditions),await Promise.allSettled(o)))"rejected"===e.status&&(a.rejected++,console.warn("automation-editor: body fetch failed",e.reason));return a}async function iQ(e,t,i){try{let a=await e.getAvailableAutomations(t);if(i?.isStale?.())return{status:"stale"};let o={...a,triggers:a.triggers.map(e=>({...e})),actions:a.actions.map(e=>({...e})),conditions:a.conditions.map(e=>({...e}))};i?.onPaint?.(o);let r=await iJ(e,o);if(i?.isStale?.())return{status:"stale"};let n={...o,triggers:[...o.triggers],actions:[...o.actions],conditions:[...o.conditions]};return{status:"ok",available:n,hydration:r}}catch(e){if(i?.isStale?.())return{status:"stale"};return{status:"error",error:e}}}function iX(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}iG.styles=[m.G,ed.z,iA],iY([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iG.prototype,"_localize",void 0),iY([(0,d.MZ)({attribute:!1})],iG.prototype,"target",void 0),iY([(0,d.MZ)({attribute:!1})],iG.prototype,"triggers",void 0),iY([(0,d.MZ)({attribute:!1})],iG.prototype,"devices",void 0),iY([(0,d.MZ)()],iG.prototype,"triggerId",void 0),iY([(0,d.MZ)({attribute:!1})],iG.prototype,"triggerParams",void 0),iY([(0,d.MZ)({attribute:!1})],iG.prototype,"board",void 0),iY([(0,d.MZ)()],iG.prototype,"yaml",void 0),iY([(0,d.MZ)({type:Boolean})],iG.prototype,"disabled",void 0),iG=iY([(0,d.EM)("esphome-automation-trigger-picker")],iG),(0,b.C)({"arrow-decision-outline":s.mdiArrowDecisionOutline,delete:s.mdiDelete,"open-in-new":s.mdiOpenInNew});class i0 extends l.WF{get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._editMode=!this.addMode,this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&eg(t)!==eg(this.location)&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend(),(e.has("location")||e.has("platform"))&&this.location?.kind==="interval"&&this._loadIntervalComponent()}async _loadIntervalComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,eC.CQ)("interval",e,t);if(i){this._intervalComponent=i;return}try{let i=await (0,eC.Sn)(this._api,"interval",e,t);i&&(this._intervalComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml);this._error="";let t=this._parseError.resolve(e,this.location);t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}async _loadAvailable(){if(!this._api||!this.configuration)return;let e=++this._loadAvailableSeq;this._loading=!0,this._error="";try{let t=await iQ(this._api,this.configuration,{onPaint:t=>{e===this._loadAvailableSeq&&(this._available=t,this._loading=!1)},isStale:()=>e!==this._loadAvailableSeq});if("stale"===t.status)return;if("error"===t.status){this._error=t.error instanceof Error?t.error.message:String(t.error);return}this._available=t.available;let{missingBody:i,missingField:a,rejected:o}=t.hydration,r=i+a+o;r>0&&c.A.error(this._localize("device.automation_partial_hydration",{count:String(r)}),{richColors:!0})}finally{e===this._loadAvailableSeq&&(this._loading=!1)}}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??eh(),t=this.location,i=this._available?.devices??[],a=this._available?.scripts??[],o=this._available?.triggers??[],r=this._available?.actions??[],n=this._available?.conditions??[],s=this._deleting,d=e.trigger_id??(t?.kind==="device_on"?t.trigger||null:t?.kind==="component_on"&&this._catalogIdFor(t)||null),c=d?o.find(e=>e.id===d)??null:null;return(0,l.qy)`
      ${this._renderHeader(c)}
      ${this.addMode?this._renderAddModePickers(t,o,i,a,d,e,s):(0,l.qy)`${this._renderIdentityFields(c)}${this._renderTriggerParamsForm(c,e,s)}`}
      <div class="field">
        <div class="ae-actions-header">
          <label class="field-label">
            ${this._localize("device.automation_action")}
          </label>
          <button
            type="button"
            class="ae-section-add"
            ?disabled=${s||0===r.length}
            @click=${()=>this._actionList?.openPicker()}
          >
            <wa-icon library="mdi" name="plus"></wa-icon>
            ${this._localize("device.add_action")}
          </button>
        </div>
        <p class="field-description">
          ${(0,es.G)(this._localize("device.automation_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          hide-add
          .actions=${e.actions}
          .catalog=${r}
          .conditionCatalog=${n}
          .scripts=${a}
          .devices=${i}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${s}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,l.qy)`<p class="ae-error" role="alert">${this._error}</p>`:l.s6}
      ${this.location&&this.value&&!this.addMode?(0,l.qy)`<div class="ae-actions">
            <button
              type="button"
              class="ae-danger"
              ?disabled=${s}
              @click=${this._onDelete}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
              ${this._localize("device.delete_automation")}
            </button>
          </div>`:l.s6}
    `}_renderTriggerParamsForm(e,t,i){let a=this._paramFormEntries(e);if(0===a.length)return l.s6;let o=iC(a);return(0,l.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${t.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${i}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onTriggerParamsValueChange}
      ></esphome-config-entry-form>
      ${o?iE(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}
    `}_paramFormEntries(e){if(this.location?.kind==="interval"){let e=this._intervalComponent;return e?e.config_entries.filter(e=>"then"!==e.key):[]}return e?.config_entries??[]}_renderAddModePickers(e,t,i,a,o,r,n){return(0,l.qy)`
      <esphome-automation-target-picker
        .value=${e}
        .devices=${i}
        .scripts=${a}
        ?disabled=${n}
        @target-change=${this._onTargetChange}
      ></esphome-automation-target-picker>
      <esphome-automation-trigger-picker
        .target=${e}
        .triggers=${t}
        .devices=${i}
        .triggerId=${o}
        .triggerParams=${r.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${n}
        @trigger-change=${this._onTriggerChange}
        @trigger-params-change=${this._onTriggerParamsChange}
      ></esphome-automation-trigger-picker>
    `}_applyParamPatch(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a,...o]=t;if(0===o.length){if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}let r=e[a]&&"object"==typeof e[a]&&!Array.isArray(e[a])?e[a]:{};return{...e,[a]:this._applyParamPatch(r,o,i)}}_renderHeader(e){let t=this.location,i=t?.kind==="interval"?this._intervalComponent:null,a=i?.name??this._headerTitle(e),o=i?.docs_url??e?.docs_url??"",r=i?.description??e?.description??this._localize("device.automation_header_description"),n=i?.image_url??"";return(0,l.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${a}</h2>
        ${o?(0,l.qy)`<a
              class="ae-header-docs"
              href=${o}
              target="_blank"
              rel="noreferrer"
            >
              ${this._localize("device.docs")}
              <wa-icon library="mdi" name="open-in-new"></wa-icon>
            </a>`:l.s6}
        <p class="ae-header-desc">${(0,es.G)(r)}</p>
      </div>
      <div class="ae-header-icon">
        ${n?(0,l.qy)`<img alt="" src=${n} />`:(0,l.qy)`<wa-icon library="mdi" name="arrow-decision-outline"></wa-icon>`}
      </div>
    </div>`}_headerTitle(e){let t=this.location;return t?.kind==="interval"?this._localize("device.automation_interval_label"):e&&(t?.kind==="device_on"||t?.kind==="component_on")?e.name:t?.kind==="component_action"?iU(t.field,this._localize):this._localize("device.automation_header_title_static")}_renderIdentityFields(e){let t=this.location;if(!t||"component_on"!==t.kind&&"component_action"!==t.kind)return l.s6;let i=this._targetMetadataValue(t);return(0,l.qy)`<div class="field">
      <label class="field-label"> ${this._localize("device.automation_target")} </label>
      <input type="text" readonly .value=${i} />
    </div>`}_targetMetadataValue(e){switch(e.kind){case"device_on":return this._localize("device.automation_target_device");case"component_on":case"component_action":{let t=this._available?.devices.find(t=>t.id===e.component_id);if(!t)return e.component_id;let i=t.name??t.id;return`${i} (${t.component_id})`}case"interval":return this._localize("device.automation_target_interval_n",{index:e.index+1});case"script":return e.id;case"api_action":return e.action_name;case"light_effect":return e.component_id}}_withValue(e){let t={...this.value??eh(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=ef(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}_bareTriggerKey(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_catalogIdFor(e){if("component_on"!==e.kind||!e.trigger)return null;let t=this._available?.devices.find(t=>t.id===e.component_id),i=t?.component_id.split(".")[0]??null;return i?`${i}.${e.trigger}`:e.trigger}static get _actionStyles(){return null}get _devicesForTest(){return this._available?.devices??[]}get _scriptsForTest(){return this._available?.scripts??[]}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loadAvailableSeq=0,this._intervalComponent=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new iZ(this),this._showAdvanced=!1,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._editMode=!1,this._onTriggerParamsValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=this.value??eh(),o=this._applyParamPatch(a.trigger_params,t,i);this._withValue({trigger_params:o})},this._onTargetChange=e=>{e.stopPropagation(),this.location=e.detail.target,this._withValue({trigger_id:null,trigger_params:{}})},this._onTriggerChange=e=>{if(e.stopPropagation(),this._withValue({trigger_id:e.detail.triggerId,trigger_params:e.detail.params}),this.location?.kind==="device_on")this.location={...this.location,trigger:e.detail.triggerId};else if(this.location?.kind==="component_on"){let t=this._bareTriggerKey(e.detail.triggerId);this.location={...this.location,trigger:t}}},this._onTriggerParamsChange=e=>{e.stopPropagation(),this._withValue({trigger_params:e.detail.params})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=ef(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}function i1(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i0.styles=[m.G,ed.z,iA],iX([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i0.prototype,"_localize",void 0),iX([(0,n.Fg)({context:u.Ie})],i0.prototype,"_api",void 0),iX([(0,d.MZ)()],i0.prototype,"configuration",void 0),iX([(0,d.MZ)({attribute:!1})],i0.prototype,"board",void 0),iX([(0,d.MZ)()],i0.prototype,"platform",void 0),iX([(0,d.MZ)({attribute:!1})],i0.prototype,"value",void 0),iX([(0,d.MZ)({attribute:!1})],i0.prototype,"location",void 0),iX([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],i0.prototype,"addMode",void 0),iX([(0,d.MZ)()],i0.prototype,"yaml",void 0),iX([(0,d.P)("esphome-automation-action-list")],i0.prototype,"_actionList",void 0),iX([(0,d.wk)()],i0.prototype,"_available",void 0),iX([(0,d.wk)()],i0.prototype,"_intervalComponent",void 0),iX([(0,d.wk)()],i0.prototype,"_loading",void 0),iX([(0,d.wk)()],i0.prototype,"_deleting",void 0),iX([(0,d.wk)()],i0.prototype,"_error",void 0),iX([(0,d.wk)()],i0.prototype,"_showAdvanced",void 0),iX([(0,d.wk)()],i0.prototype,"_dirty",void 0),iX([(0,d.wk)()],i0.prototype,"_editMode",void 0),i0=iX([(0,d.EM)("esphome-automation-editor")],i0),(0,b.C)({delete:s.mdiDelete,"open-in-new":s.mdiOpenInNew,"script-text-outline":s.mdiScriptTextOutline});class i2 extends l.WF{get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._load(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.id!==this.location.id&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable(),this._loadScriptComponent()}catch(e){this._error=e instanceof Error?e.message:String(e)}finally{this._loading=!1}}}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration)}catch(e){this._error=e instanceof Error?e.message:String(e)}}async _loadScriptComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,eC.CQ)("script",e,t);if(i){this._scriptComponent=i;return}try{let i=await (0,eC.Sn)(this._api,"script",e,t);i&&(this._scriptComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"script");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??eh(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._deleting;return(0,l.qy)`
      ${this._renderHeader()} ${this._renderConfigForm(e,r)}
      ${this._showAdvanced?this._renderParametersField(e,r):l.s6}
      <div class="field">
        <div class="ae-actions-header">
          <label class="field-label">
            ${this._localize("device.automation_action")}
          </label>
          <button
            type="button"
            class="ae-section-add"
            ?disabled=${r||0===a.length}
            @click=${()=>this._actionList?.openPicker()}
          >
            <wa-icon library="mdi" name="plus"></wa-icon>
            ${this._localize("device.add_action")}
          </button>
        </div>
        <p class="field-description">
          ${(0,es.G)(this._localize("device.script_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          hide-add
          .actions=${e.actions}
          .catalog=${a}
          .conditionCatalog=${o}
          .scripts=${i}
          .devices=${t}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${r}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,l.qy)`<p class="ae-error" role="alert">${this._error}</p>`:l.s6}
      ${this.location&&this.value&&!this.addMode?(0,l.qy)`<div class="ae-actions">
            <button
              type="button"
              class="ae-danger"
              ?disabled=${r}
              @click=${this._onDelete}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
              ${this._localize("device.delete_script")}
            </button>
          </div>`:l.s6}
    `}_renderHeader(){let e=this._scriptComponent,t=e?.name??this._localize("device.script_header_title_static"),i=e?.description??this._localize("device.script_header_description"),a=e?.docs_url??"https://esphome.io/components/script.html",o=e?.image_url??"";return(0,l.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${t}</h2>
        <a class="ae-header-docs" href=${a} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">${(0,es.G)(i)}</p>
      </div>
      <div class="ae-header-icon">
        ${o?(0,l.qy)`<img alt="" src=${o} />`:(0,l.qy)`<wa-icon library="mdi" name="script-text-outline"></wa-icon>`}
      </div>
    </div>`}_renderConfigForm(e,t){let i=this._scriptComponent;if(!i)return l.s6;let a=i.config_entries.filter(e=>"parameters"!==e.key&&"then"!==e.key);return 0===a.length?l.s6:(0,l.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${e.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${t}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onConfigFormValueChange}
      ></esphome-config-entry-form>
      ${this._renderAdvancedToggle(a)}
    `}_renderAdvancedToggle(e){return iC(e)||this._hasParametersEntry()?iE(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}_hasParametersEntry(){return this._scriptComponent?.config_entries.some(e=>"parameters"===e.key)??!1}_patchParams(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a]=t;if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}_renderParametersField(e,t){let i=e.trigger_params.parameters??{};return(0,l.qy)`<esphome-callable-params-editor
      .value=${i}
      ?disabled=${t}
      .fieldLabel=${this._localize("device.automation_script_parameters")}
      .description=${this._localize("device.script_parameters_description")}
      .addLabel=${this._localize("device.script_add_parameter")}
      .namePlaceholder=${this._localize("device.script_parameter_name_placeholder")}
      @value-change=${this._onParametersChange}
    ></esphome-callable-params-editor>`}_withValue(e){let t={...this.value??eh(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this.location.id){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=ef(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new iZ(this),this._scriptComponent=null,this._showAdvanced=!1,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._onConfigFormValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=this.value??eh(),o=1===t.length&&"id"===t[0]?iz(String(i??"")):i,r=this._patchParams(a.trigger_params,t,o);if(1===t.length&&"id"===t[0]){let e=String(o??"");e&&(this.location={kind:"script",id:e})}this._withValue({trigger_params:r})},this._onParametersChange=e=>{e.stopPropagation();let t=this.value??eh();this._withValue({trigger_params:{...t.trigger_params,parameters:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=ef(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}i2.styles=[m.G,ed.z,iA],i1([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i2.prototype,"_localize",void 0),i1([(0,n.Fg)({context:u.Ie})],i2.prototype,"_api",void 0),i1([(0,d.MZ)()],i2.prototype,"configuration",void 0),i1([(0,d.MZ)({attribute:!1})],i2.prototype,"board",void 0),i1([(0,d.MZ)()],i2.prototype,"platform",void 0),i1([(0,d.MZ)({attribute:!1})],i2.prototype,"value",void 0),i1([(0,d.MZ)({attribute:!1})],i2.prototype,"location",void 0),i1([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],i2.prototype,"addMode",void 0),i1([(0,d.MZ)()],i2.prototype,"yaml",void 0),i1([(0,d.P)("esphome-automation-action-list")],i2.prototype,"_actionList",void 0),i1([(0,d.wk)()],i2.prototype,"_available",void 0),i1([(0,d.wk)()],i2.prototype,"_loading",void 0),i1([(0,d.wk)()],i2.prototype,"_deleting",void 0),i1([(0,d.wk)()],i2.prototype,"_error",void 0),i1([(0,d.wk)()],i2.prototype,"_scriptComponent",void 0),i1([(0,d.wk)()],i2.prototype,"_showAdvanced",void 0),i1([(0,d.wk)()],i2.prototype,"_dirty",void 0),i2=i1([(0,d.EM)("esphome-script-editor")],i2);let i6=(0,l.AH)`
  esphome-base-dialog {
    --width: 480px;
  }

  esphome-base-dialog::part(body) {
    padding: 0 var(--wa-space-l);
  }

  .intro {
    margin: 0 0 var(--wa-space-m);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }

  .board-list {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-xs);
    max-height: 48vh;
    overflow-y: auto;
  }

  .board-row {
    display: flex;
    align-items: center;
    gap: var(--wa-space-m);
    width: 100%;
    padding: var(--wa-space-s);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-lowered);
    font-family: inherit;
    text-align: left;
    cursor: pointer;
    transition:
      border-color 0.12s,
      background 0.12s;
  }

  .board-row:hover {
    border-color: var(--esphome-primary);
    background: var(--wa-color-surface-border);
  }

  .board-row:focus-visible {
    outline: var(--wa-border-width-m) solid var(--esphome-primary);
    outline-offset: 2px;
  }

  .board-thumb {
    width: 48px;
    height: 48px;
    object-fit: contain;
    flex-shrink: 0;
    border-radius: var(--wa-border-radius-s);
  }

  .board-meta {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
    flex: 1;
  }

  .board-name {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  .board-mfr {
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
  }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--wa-space-s);
    padding: var(--wa-space-m) 0 var(--wa-space-l);
  }

  .btn {
    padding: 8px 18px;
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    cursor: pointer;
    border: none;
    transition: background 0.12s;
  }

  .btn--cancel {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .btn--cancel:hover {
    background: var(--wa-color-surface-border);
  }
`;function i3(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}class i4 extends l.WF{open(){this._open=!0}close(){this._open=!1}render(){return(0,l.qy)`
      <esphome-base-dialog
        ?open=${this._open}
        .label=${this._localize("device.change_board_title")}
        @request-close=${this._onRequestClose}
      >
        <p class="intro">
          ${this._localize("device.change_board_desc",{name:this.currentBoard?.name??""})}
        </p>
        <div class="board-list">
          ${this.boards.map(e=>this._renderBoard(e))}
        </div>
        <div class="actions">
          <button class="btn btn--cancel" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_renderBoard(e){return(0,l.qy)`
      <button type="button" class="board-row" @click=${()=>this._select(e)}>
        <img
          class="board-thumb"
          src=${(0,en.Ru)(e)}
          alt=${e.name}
          referrerpolicy="no-referrer"
          @error=${en.jt}
        />
        <div class="board-meta">
          <span class="board-name">${e.name}</span>
          ${e.manufacturer?(0,l.qy)`<span class="board-mfr">${e.manufacturer}</span>`:l.s6}
        </div>
        ${e.is_generic?(0,l.qy)`<wa-badge variant="neutral" pill
              >${this._localize("device.change_board_generic_tag")}</wa-badge
            >`:l.s6}
      </button>
    `}_select(e){this.close(),this.dispatchEvent(new CustomEvent("select-board",{detail:{boardId:e.id},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.currentBoard=null,this.boards=[],this._open=!1,this._onRequestClose=()=>{this._open=!1}}}i4.styles=[m.G,ew.dC,ew.rG,i6],i3([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i4.prototype,"_localize",void 0),i3([(0,d.MZ)({attribute:!1})],i4.prototype,"currentBoard",void 0),i3([(0,d.MZ)({attribute:!1})],i4.prototype,"boards",void 0),i3([(0,d.wk)()],i4.prototype,"_open",void 0),i4=i3([(0,d.EM)("esphome-change-board-dialog")],i4);class i5{hostConnected(){this._unsubscribe=tX(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}ensure(){let{api:e,platform:t,boardId:i}=this._context();e&&void 0===tW(t,i)&&tH.triggers.fetch(e,t,i).catch(()=>{})}resolveName(e,t,i){let{platform:a,boardId:o}=this._context(),r=tW(a,o);if(!r)return i;let n="esphome"===e?t:`${e}.${t}`;return r.find(e=>e.id===n)?.name||i}hasTriggersFor(e){let{platform:t,boardId:i}=this._context(),a=tW(t,i);return!a||a.some(t=>t.applies_to.some(t=>e.includes(t)))}constructor(e,t){this._host=e,this._context=t,e.addController(this)}}var i8=i(383);function i9(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(8768),(0,b.C)({close:s.mdiClose});class i7 extends l.WF{open(){this._name="",this._error="",this._open=!0}render(){let e=this.boardName?this._localize("device.add_api_action_dialog_title",{name:this.boardName}):this._localize("device.add_api_action");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      @request-close=${this._onRequestClose}
    >
      <p class="intro">
        ${(0,es.G)(this._localize("device.api_action_header_description"))}
      </p>
      <div class="field">
        <label class="field-label" for="api-action-id-input">
          ${this._localize("device.automation_target_api_action_new_id_label")}
          <span class="required">*</span>
        </label>
        <input
          id="api-action-id-input"
          type="text"
          .value=${this._name}
          placeholder=${this._localize("device.automation_target_api_action_id_placeholder")}
          ?disabled=${this._saving}
          @input=${e=>{this._name=iz(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,l.qy)`<p class="error" role="alert">${this._error}</p>`:l.s6}
      <div class="actions">
        <button
          type="button"
          class="primary"
          ?disabled=${this._saving||!this._canContinue()}
          @click=${this._onContinue}
        >
          ${this._saving?this._localize("device.adding"):this._localize("device.add_automation_continue")}
        </button>
      </div>
    </esphome-base-dialog>`}_canContinue(){return!!this._name&&!I(this.yaml).some(e=>e.key===`automation:api_action:${this._name}`)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._name="",this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"api_action",action_name:this._name},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{},actions:[]},e,this.yaml),i=ef(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:eg(e)},bubbles:!0,composed:!0})),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}i7.styles=[m.G,ed.z,(0,l.AH)`
      esphome-base-dialog {
        --width: 480px;
      }
      esphome-base-dialog::part(body) {
        padding: var(--wa-space-l);
      }
      .intro {
        font-size: var(--wa-font-size-s);
        color: var(--wa-color-text-quiet);
        margin: 0 0 var(--wa-space-m) 0;
        line-height: 1.5;
      }
      .intro code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-2xs);
        padding: 1px 4px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
      }
      .field {
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-2xs);
      }
      .field-label {
        font-size: var(--wa-font-size-s);
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-normal);
      }
      .required {
        color: var(--esphome-error, #d92d20);
      }
      .actions {
        display: flex;
        justify-content: flex-end;
        gap: var(--wa-space-s);
        margin-top: var(--wa-space-l);
      }

      .actions button {
        display: inline-flex;
        align-items: center;
        box-sizing: border-box;
        gap: 3px;
        padding: 7px 14px;
        border: var(--wa-border-width-s) solid transparent;
        border-radius: var(--wa-border-radius-m);
        cursor: pointer;
        font-size: var(--wa-font-size-xs);
        font-weight: var(--wa-font-weight-bold);
        font-family: inherit;
        line-height: 1;
        transition:
          background 0.12s,
          border-color 0.12s,
          box-shadow 0.12s,
          transform 0.12s;
      }
      .actions .primary {
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
        box-shadow: var(--esphome-primary-shadow);
      }
      .actions .primary:hover:not(:disabled) {
        background: var(--esphome-primary-hover);
        box-shadow: var(--esphome-primary-shadow-hover);
        transform: translateY(-1px);
      }
      .actions .primary:active:not(:disabled) {
        transform: translateY(0);
      }
      .actions .primary:disabled {
        background: color-mix(
          in srgb,
          var(--esphome-primary) 35%,
          var(--wa-color-surface-default)
        );
        color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
      }
      .error {
        color: var(--esphome-error, #d92d20);
        font-size: var(--wa-font-size-2xs);
        margin-top: var(--wa-space-2xs);
      }
    `],i9([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i7.prototype,"_localize",void 0),i9([(0,n.Fg)({context:u.Ie})],i7.prototype,"_api",void 0),i9([(0,d.MZ)()],i7.prototype,"boardName",void 0),i9([(0,d.MZ)()],i7.prototype,"configuration",void 0),i9([(0,d.MZ)()],i7.prototype,"yaml",void 0),i9([(0,d.MZ)({attribute:!1})],i7.prototype,"board",void 0),i9([(0,d.wk)()],i7.prototype,"_open",void 0),i9([(0,d.wk)()],i7.prototype,"_name",void 0),i9([(0,d.wk)()],i7.prototype,"_saving",void 0),i9([(0,d.wk)()],i7.prototype,"_error",void 0),i7=i9([(0,d.EM)("esphome-add-api-action-dialog")],i7);let ae=(0,l.AH)`
  /* Manage-list block (Automations / API actions / component actions).
     Inline title + "Add X" button on row 1, then either the rows or an
     empty placeholder below — the breathing room between those two reads
     as the visual divider, so the gap is deliberately bigger than the
     row-to-row spacing inside the list. */
  .list {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    padding-top: var(--wa-space-s);
    border-top: 1px solid var(--wa-color-surface-border);
  }

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
  }

  .title {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    margin: 0;
    color: var(--wa-color-text-normal);
  }

  .add {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    background: var(--wa-color-brand-fill-loud, var(--esphome-primary));
    color: var(--wa-color-brand-on-loud, var(--esphome-on-primary));
    border: var(--wa-border-width-s) solid
      var(--wa-color-brand-fill-loud, var(--esphome-primary));
    padding: 2px var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-semibold);
    font-family: inherit;
    transition:
      background 0.12s,
      border-color 0.12s;
  }

  .add:hover {
    background: color-mix(
      in srgb,
      var(--wa-color-brand-fill-loud, var(--esphome-primary)),
      black 10%
    );
    border-color: color-mix(
      in srgb,
      var(--wa-color-brand-fill-loud, var(--esphome-primary)),
      black 10%
    );
  }

  .add wa-icon {
    font-size: 14px;
  }

  .empty {
    margin: 0;
    padding: var(--wa-space-m) var(--wa-space-s);
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    font-style: italic;
    border: 1px dashed var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-lowered, transparent);
  }

  .rows {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    border: 1px solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    overflow: hidden;
    background: var(--wa-color-surface-raised, transparent);
  }

  .row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
    padding: var(--wa-space-xs) var(--wa-space-s);
    border-top: 1px solid var(--wa-color-surface-border);
    background: transparent;
    transition: background 0.12s;
  }

  .row:first-child {
    border-top: none;
  }

  .row:hover {
    background: var(--wa-color-surface-lowered);
  }

  .name {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .row-buttons {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .row-edit,
  .row-delete {
    appearance: none;
    border: 1px solid transparent;
    background: transparent;
    color: var(--wa-color-text-quiet);
    width: 26px;
    height: 26px;
    border-radius: 6px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .row-edit:hover:not(:disabled) {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
  }

  .row-delete:hover:not(:disabled) {
    background: color-mix(in srgb, var(--esphome-error), transparent 90%);
    color: var(--esphome-error);
  }

  .row-edit:disabled,
  .row-delete:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
`;function at(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({plus:s.mdiPlus,pencil:s.mdiPencil,delete:s.mdiDelete});class ai extends l.WF{render(){if(0===this.rows.length&&void 0===this.addLabel)return l.s6;let e=""!==this.busyKey;return(0,l.qy)`<div class="list">
      <div class="header">
        <h4 class="title">${this.heading}</h4>
        ${void 0!==this.addLabel?(0,l.qy)`<button type="button" class="add" @click=${this._onAdd}>
              <wa-icon library="mdi" name="plus"></wa-icon>
              ${this.addLabel}
            </button>`:l.s6}
      </div>
      ${0===this.rows.length?void 0!==this.emptyText?(0,l.qy)`<p class="empty" role="status">${this.emptyText}</p>`:l.s6:(0,l.qy)`<ul class="rows">
            ${this.rows.map(t=>(0,l.qy)`<li class="row">
                  <span class="name">${t.label}</span>
                  <div class="row-buttons">
                    <button
                      type="button"
                      class="row-edit"
                      aria-label=${this.editLabel}
                      title=${this.editLabel}
                      ?disabled=${e}
                      @click=${()=>this._emit("edit",t.key)}
                    >
                      <wa-icon library="mdi" name="pencil"></wa-icon>
                    </button>
                    <button
                      type="button"
                      class="row-delete"
                      aria-label=${this.deleteLabel}
                      title=${this.deleteLabel}
                      ?disabled=${e}
                      @click=${()=>this._emit("delete",t.key)}
                    >
                      <wa-icon library="mdi" name="delete"></wa-icon>
                    </button>
                  </div>
                </li>`)}
          </ul>`}
    </div>`}_emit(e,t){this.dispatchEvent(new CustomEvent(e,{detail:{key:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this.heading="",this.rows=[],this.busyKey="",this.editLabel="",this.deleteLabel="",this._onAdd=()=>{this.dispatchEvent(new CustomEvent("add",{bubbles:!0,composed:!0}))}}}ai.styles=[m.G,ae],at([(0,d.MZ)()],ai.prototype,"heading",void 0),at([(0,d.MZ)({attribute:!1})],ai.prototype,"rows",void 0),at([(0,d.MZ)({attribute:"add-label"})],ai.prototype,"addLabel",void 0),at([(0,d.MZ)({attribute:"empty-text"})],ai.prototype,"emptyText",void 0),at([(0,d.MZ)({attribute:"busy-key"})],ai.prototype,"busyKey",void 0),at([(0,d.MZ)({attribute:"edit-label"})],ai.prototype,"editLabel",void 0),at([(0,d.MZ)({attribute:"delete-label"})],ai.prototype,"deleteLabel",void 0),ai=at([(0,d.EM)("esphome-section-automation-list")],ai);let aa=(0,l.AH)`
  :host {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    margin-top: var(--wa-space-m);
  }

  .section-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    gap: var(--wa-space-l);
    padding-bottom: var(--wa-space-m);
    margin-bottom: var(--wa-space-m);
    border-bottom: 1px solid var(--wa-color-surface-lowered);
  }

  .section-header-info {
    display: flex;
    flex-direction: column;
    flex: 1;
    gap: var(--wa-space-s);
    min-width: 0;
  }

  .section-header-title-row {
    display: flex;
    align-items: center;
    gap: var(--wa-space-m);
    flex-wrap: wrap;
  }

  .section-image {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 140px;
    height: 100px;
    padding: var(--wa-space-s);
    background: var(--wa-color-surface-lowered);
    border-radius: var(--wa-border-radius-l);
    box-sizing: border-box;
  }

  .section-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* Match the catalog's dark-mode treatment for the same monochrome
     SVG illustrations — see component-catalog.ts for the rationale. */
  .section-image img[src$=".svg"] {
    filter: var(--esphome-svg-filter, none);
  }

  .section-title {
    margin: 0;
    font-size: var(--wa-font-size-l);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  .section-subtitle {
    margin: 0;
    font-family: var(--wa-font-family-code);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }

  .section-desc {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .docs-link {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    font-size: var(--wa-font-size-xs);
    color: var(--esphome-primary);
    text-decoration: underline;
  }

  .docs-link:hover {
    text-decoration: none;
  }

  .docs-link wa-icon {
    font-size: 14px;
  }

  esphome-config-entry-form {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
  }

  /* "Show advanced settings" toggle row, shown below the form when
     the section has any advanced entries (at any depth). */
  .advanced-toggle-row {
    display: flex;
    justify-content: flex-start;
    margin-top: var(--wa-space-s);
    font-size: var(--wa-font-size-s);
  }

  .advanced-toggle-row wa-switch {
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
  }

  .actions {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
    padding-top: var(--wa-space-s);
  }
  .delete-button {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-left: auto;
    background: #e54d2e;
    color: #ffffff;
    border: var(--wa-border-width-s) solid #e54d2e;
    padding: var(--wa-space-xs) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    transition:
      background 0.12s,
      border-color 0.12s;
  }

  .delete-button:hover:not(:disabled) {
    background: color-mix(in srgb, #e54d2e, black 10%);
    border-color: color-mix(in srgb, #e54d2e, black 10%);
  }

  .delete-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .delete-button wa-icon {
    font-size: 16px;
  }

  .error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-s);
  }

  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--wa-space-xl);
  }

  /* Stand-in shown when a section has no editable form fields
     (substitutions, globals, packages) — tells the user to edit
     this part via the YAML pane instead of presenting an empty
     form. Includes a "Show YAML editor" CTA when the pane is
     hidden by the current layout. */
  .yaml-only-notice {
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-lowered);
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-s);
    line-height: 1.5;
  }

  .yaml-only-notice wa-icon {
    flex-shrink: 0;
    font-size: 20px;
    color: var(--esphome-primary);
  }

  .yaml-only-notice-body {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    flex: 1;
    min-width: 0;
  }

  .yaml-only-notice p {
    margin: 0;
  }

  .yaml-only-notice-cta {
    align-self: flex-start;
    padding: var(--wa-space-2xs) var(--wa-space-m);
    border: var(--wa-border-width-s) solid var(--esphome-primary);
    border-radius: var(--wa-border-radius-m);
    background: transparent;
    color: var(--esphome-primary);
    font-family: inherit;
    font-size: inherit;
    font-weight: var(--wa-font-weight-bold);
    cursor: pointer;
    transition:
      background 0.12s,
      color 0.12s;
  }

  .yaml-only-notice-cta:hover {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }
`,ao="[a-zA-Z_][^\\s:#]*",ar=/^[a-zA-Z_]/,an=RegExp(`^\\s+-\\s+(${ao}):\\s*(.*)$`),as=/^\s+-(\s|$)/,al=/^[^"']*:\s*[|>][-+]?\s*(?:#.*)?$/,ad=/^[|>][-+]?$/,ac=/^\s+-\s*$/,ah=/^\s+-\s+[a-zA-Z_][\w.]*:(?:\s|$)/,ap=e=>RegExp(`^${e}(${ao}):\\s*(.*)$`),au=e=>e.trim().startsWith("#"),am=e=>""===e.trim()||au(e),av=(e,t)=>{let i=t;for(;i<e.length&&am(e[i]);)i++;return i},ag=e=>e.match(/^ */)[0],af=(e,t,i)=>{let a=e[t],o=i?a.indexOf("-")+1:ag(a).length;for(let i=t+1;i<e.length;i++){let t=e[i];if(am(t))continue;if(ar.test(t))break;let a=ag(t);if(a.length>o)return a;break}return i?"    ":"  "},a_=(e,t)=>{let i=`${t}-`;if(!e.startsWith(i))return!1;let a=e.slice(i.length);return""===a||a.startsWith(" ")},ab=(e,t)=>{let i=ag(e);if(i.length<t.length)return!1;let a=e.slice(i.length);return"-"===a||a.startsWith("- ")},ay=e=>e.startsWith('"')&&e.endsWith('"')||e.startsWith("'")&&e.endsWith("'")?e.slice(1,-1):e,aw=e=>{let t=e.startsWith('"')&&e.endsWith('"')||e.startsWith("'")&&e.endsWith("'"),i=ay(e);if(!t){let e=(0,ex.FY)(i);if(null!==e)return e}return i},a$=e=>{let t=e.slice(1,-1).trim();return""===t?[]:t.split(",").map(e=>ay(e.trim()))},ax=(e,t,i)=>{let{dashIndent:a,firstDashIdx:o}=((e,t,i)=>{let a=t;for(;a<e.length&&am(e[a]);)a++;return a>=e.length?{dashIndent:i,firstDashIdx:a}:{dashIndent:e[a].match(/^( *)-/)?.[1]??i,firstDashIdx:a}})(e,t,`${i}  `),r=((e,t,i)=>{for(let a=t;a<e.length;a++){let t=e[a];if(am(t))continue;let o=ag(t);if(o.length<=i.length)break;if("-"!==t[o.length])return o}return null})(e,o+1,a)??`${a}  `,{endIdx:n,isComplex:s}=aC(e,t,i);if(s){let i=az(e,t,a,r);return i?{value:i.items,endIdx:i.endIdx,isEmptyScalarList:!1}:{value:new ex.ho(e.slice(t,n)),endIdx:n,isEmptyScalarList:!1}}let{items:l,endIdx:d}=((e,t,i,a)=>{let o=[],r=t;for(;r<e.length;r++){if(am(e[r]))continue;if(!e[r].startsWith(i))break;let t=e[r].match(a);if(!t)break;o.push(ay(t[1].trim()))}return{items:o,endIdx:r}})(e,t,`${a}- `,RegExp(`^${a}-\\s+(.*)$`));return{value:l,endIdx:d,isEmptyScalarList:0===l.length}},ak=(e,t)=>{var i,a;let o=e.match(t);return o?(i=o[1],a=o[2].trim(),i.includes(".")||ad.test(a)?null:""===a?{key:i,value:null}:{key:i,value:aw(a)}):null},az=(e,t,i,a)=>{let o=RegExp(`^${i}-\\s+(${ao}):\\s*(.*)$`),r=RegExp(`^${a}(${ao}):\\s*(.*)$`),n=t=>{let n=Object.create(null),s=null;if(!ac.test(e[t])){let i=ak(e[t],o);if(!i)return null;n[i.key]=i.value,null===i.value&&(s=i.key)}if(null!==s){let a=i.length+2,o=av(e,t+1);if(o<e.length){let i=ag(e[o]);if(i.length>a){if(e[o].slice(i.length).startsWith("-"))return null;let a=aA(e,t+1,i);return Object.keys(a.values).length>0&&(n[s]=a.values),{item:n,endIdx:a.endIdx}}}}let l=((e,t,i,a,o)=>{let r=t;for(;r<e.length;){let t=e[r];if(am(t)){r++;continue}if(!t.startsWith(i))break;if(t.startsWith(`${i} `))return null;let n=ak(t,a);if(!n)return null;o[n.key]=n.value,r++}return r})(e,t+1,a,r,n);return null===l?null:{item:n,endIdx:l}},s=[],l=t;for(;l<e.length;){if(am(e[l])){l++;continue}if(!a_(e[l],i))break;let t=n(l);if(!t)return null;s.push(t.item),l=t.endIdx}return{items:s,endIdx:l}},aC=(e,t,i)=>{let a=!1;for(let o=t;o<e.length;o++){let t=e[o];if(am(t))continue;let r=t.match(/^ */)[0];if(r.length<i.length)return{endIdx:o,isComplex:a};if(r.length===i.length){let e=t.slice(r.length);if("-"!==e&&!e.startsWith("- "))return{endIdx:o,isComplex:a}}!a&&(al.test(t)||ah.test(t)||ac.test(t))&&(a=!0)}return{endIdx:e.length,isComplex:a}};function aE(e,t,i){if(void 0!==i)return i-1;for(let i=0;i<e.length;i++)if(e[i].startsWith(`${t}:`))return i;return -1}function aA(e,t,i){let a=ap(i),o=Object.create(null),r=t;for(;r<e.length;){let t=e[r];if(am(t)){r++;continue}if(!t.startsWith(i))break;let n=t.match(a);if(!n){r++;continue}let s=n[1],l=n[2].trim();if(ad.test(l)){let{endIdx:t}=aC(e,r+1,i);o[s]=new ex.ho(e.slice(r+1,t),l),r=t;continue}if(""===l){let t=av(e,r+1);if(t<e.length&&ab(e[t],i)){let{value:t,endIdx:a}=ax(e,r+1,i);o[s]=t,r=a;continue}if(t<e.length){let a=ag(e[t]);if(a.length>i.length){let t=aA(e,r+1,a);Object.keys(t.values).length>0&&(o[s]=t.values),r=t.endIdx;continue}}r++;continue}l.startsWith("[")&&l.endsWith("]")?o[s]=a$(l):o[s]=aw(l),r++}return{values:o,endIdx:r}}function aq(e,t,i){let a=aE(e,t,i);if(a<0)return{start:-1,end:-1};let o=as.test(e[a]),r=o?(e[a].match(/^(\s*)-/)??["",""])[1].length:-1,n=e.length;for(let t=a+1;t<e.length;t++)if(o){let i=e[t].match(/^(\s*)-(\s|$)/);if(i&&i[1].length===r||ar.test(e[t])){n=t;break}}else if(ar.test(e[t])){n=t;break}return{start:a,end:n}}function aS(e){if(e._draftTimer=null,!e._config)return;let t=C(e.sectionKey,e._config.entries);e._fieldErrors=(0,eM.JK)(t,e._values,e._presentComponents,e.board?.esphome.platform??null);let i=J(e.yaml,e.sectionKey,e.fromLine);if(void 0===i)return void e._setDirty(!1);let a=function(e,t,i,a,o={}){let r=e.split("\n"),{start:n,end:s}=aq(r,t,a);if(n<0)return e;let l=as.test(r[n]),d=af(r,n,l),c=s,h=!1;for(;c>n+1;){let e=r[c-1];if(""===e.trim())c--;else if(au(e)&&ag(e).length<=d.length)h=!0,c--;else break}let p=h?c:s;if(x.has(t)){let a=i[t];if(!Array.isArray(a))return e;let s=(0,ex.ym)({[t]:a},ag(r[n]),{...o,indentStep:o.indentStep??(d||"  ")});return r.splice(n,p-n,...s),r.join("\n")}let u=i,m=r[n];if(l){let e=m.match(an);if(e){let t=e[1];if(Object.prototype.hasOwnProperty.call(i,t)){let e=m.match(/^(\s+)-(\s+)/),a=e[1],o=`${a}-${e[2]}`;if(function(e){if(null==e)return!1;let t=typeof e;return"string"===t||"number"===t||"boolean"===t}(i[t])){m=`${o}${t}: ${(0,ex.Rm)(i[t])}`;let{[t]:e,...a}=i;u=a}else m=`${a}-`}}}let v=!l&&d?d:"  ",g=[m,...(0,ex.ym)(u,d,{...o,indentStep:o.indentStep??v})];return r.splice(n,p-n,...g),r.join("\n")}(e.yaml,e.sectionKey,e._values,i,{keepEmptyStrings:k.has(e.sectionKey)});e._setDirty(!1),a!==e.yaml&&(e._lastSelfWrittenYaml=a,e.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})))}async function aM(e){if(!e._config)return;let t=J(e.yaml,e.sectionKey,e.fromLine);if(void 0===t){e._error=e._localize("device.section_delete_error");return}e._deleting=!0,e._error="";let i=e._config.title;try{let a=function(e,t,i){let a=e.split("\n"),{start:o,end:r}=aq(a,t,i);if(o<0)return e;let n=as.test(a[o]);if(a.splice(o,r-o),n){let e=o-1;for(;e>=0&&!ar.test(a[e]);)e--;if(e>=0){let t=!1,i=a.length;for(let o=e+1;o<a.length;o++){if(ar.test(a[o])){i=o;break}if(""!==a[o].trim()){t=!0;break}}t||a.splice(e,i-e)}}return a.join("\n")}(e.yaml,e.sectionKey,t);if(a===e.yaml){e._error=e._localize("device.section_delete_error");return}await e._api.updateConfig(e.configuration,a),e._setDirty(!1),e.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:a},bubbles:!0,composed:!0})),e.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0})),c.A.success(e._localize("device.section_deleted",{name:i}),{richColors:!0})}catch(t){e._error=t instanceof Error?t.message:e._localize("device.section_delete_error")}finally{e._deleting=!1}}async function aL(e){let t=++e._loadId;e._loading=!0,e._error="",e._config=null,e._isUnknown=!1,e._setDirty(!1),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),e._lastSelfWrittenYaml=null;try{let i=e.board?.esphome.platform,a=await (0,eC.Sn)(e._api,e.sectionKey,i);if(t!==e._loadId)return;let o=e.yaml;a?e._config={section_key:e.sectionKey,section_type:"core",title:a.name,description:a.description,docs_url:a.docs_url,icon:"",image_url:a.image_url,entries:a.config_entries}:(e._config={section_key:e.sectionKey,section_type:"core",title:e.sectionKey,description:"",docs_url:"",icon:"",image_url:"",entries:[]},e._isUnknown=!0);let r=J(o,e.sectionKey,e.fromLine),n=function(e,t,i){let a=e.split("\n"),o=Object.create(null),r=aE(a,t,i);if(r<0)return o;let n=as.test(a[r]),s=af(a,r,n),l=ap(s);if(!n&&x.has(t)){let e=av(a,r+1);if(e<a.length&&ab(a[e],s))return o[t]=ax(a,r+1,s).value,o}if(n){let e=a[r].match(an);if(e){let t=e[2].trim();""!==t&&(o[e[1]]=aw(t))}}let d=n?(a[r].match(/^(\s*)-/)??["",""])[1].length:-1;for(let e=r+1;e<a.length;e++){let t=a[e];if(am(t))continue;if(n){let e=t.match(/^(\s*)-(\s|$)/);if(e&&e[1].length===d||ar.test(t))break}else if(ar.test(t))break;let i=t.match(l);if(!i)continue;let r=i[1],c=i[2].trim();if(ad.test(c)){let{endIdx:t}=aC(a,e+1,s);o[r]=new ex.ho(a.slice(e+1,t),c),e=t-1;continue}if(""===c){let t=av(a,e+1);if(t>=a.length)continue;let i=a[t];if(ab(i,s)){let{value:t,endIdx:i,isEmptyScalarList:n}=ax(a,e+1,s);n||(o[r]=t,e=i-1);continue}let n=ag(i);if(n.length>s.length){let t=aA(a,e+1,n);Object.keys(t.values).length>0&&(o[r]=t.values),e=t.endIdx-1}continue}if(c.startsWith("[")&&c.endsWith("]")){o[r]=a$(c);continue}o[r]=aw(c)}return o}(o,e.sectionKey,r);e._values=(0,tz.Dq)(n,e._config.entries),e._resolvedFromLine=r,e._presentComponents=(0,ex.Zn)(o)}catch(a){if(t!==e._loadId)return;let i=a instanceof Error?a.message:"";e._error=i.includes("timed out")?e._localize("device.load_config_error"):i||e._localize("device.load_config_error")}finally{t===e._loadId&&(e._loading=!1)}}function aP(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({delete:s.mdiDelete,"information-outline":s.mdiInformationOutline,"open-in-new":s.mdiOpenInNew,pencil:s.mdiPencil,"plus-circle-outline":s.mdiPlusCircleOutline});let aF=new Set(["esphome"]);class aT extends l.WF{get _showAdvanced(){return this._advancedShownSections.has(this.sectionKey)}_setShowAdvanced(e){let t=new Set(this._advancedShownSections);e?t.add(this.sectionKey):t.delete(this.sectionKey),this._advancedShownSections=t}updated(e){(e.has("sectionKey")||e.has("configuration")||e.has("fromLine"))&&this.sectionKey&&this.configuration&&aL(this),this._triggerCatalog.ensure()}connectedCallback(){super.connectedCallback(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}flushPending(){null!==this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null,aS(this))}reload(){this.sectionKey&&this.configuration&&null===this._draftTimer&&this.yaml!==this._lastSelfWrittenYaml&&aL(this)}get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_scheduleDraftFlush(){this._draftTimer&&clearTimeout(this._draftTimer),this._draftTimer=setTimeout(()=>aS(this),aT.DRAFT_DEBOUNCE_MS)}_onShowYamlEditor(){this.dispatchEvent(new CustomEvent("show-yaml-editor",{bubbles:!0,composed:!0}))}render(){if(this._loading)return(0,l.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`;if(this._error&&!this._config)return(0,l.qy)`<p class="error">${this._error}</p>`;if(!this._config)return l.s6;let e=this._showAdvanced,t=C(this.sectionKey,this._config.entries),i=iC(t),a=(0,i8.r)(this.sectionKey,t.length),o=!aF.has(this.sectionKey);return(0,l.qy)`
      <div class="section-header">
        <div class="section-header-info">
          <div class="section-header-title-row">
            <h3 class="section-title">
              ${this._isUnknown?this._localize("device.custom_component_title"):this._config.title}
            </h3>
            ${this._config.docs_url?(0,l.qy)`<a
                  class="docs-link"
                  href=${this._config.docs_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  ${this._localize("device.docs")}
                  <wa-icon library="mdi" name="open-in-new"></wa-icon>
                </a>`:l.s6}
          </div>
          ${this._isUnknown?(0,l.qy)`<p class="section-subtitle">${this.sectionKey}</p>`:l.s6}
          ${this._config.description?(0,l.qy)`<p class="section-desc">
                ${(0,es.G)(this._config.description)}
              </p>`:l.s6}
        </div>
        ${this._isUnknown?l.s6:(0,l.qy)`<div class="section-image">
              <img
                src=${this._config.image_url||(0,en.uG)()}
                alt=${this._config.title}
                referrerpolicy="no-referrer"
                @error=${en.jt}
              />
            </div>`}
      </div>
      ${a?(0,l.qy)`<div class="yaml-only-notice" role="note">
              <wa-icon library="mdi" name="information-outline"></wa-icon>
              <div class="yaml-only-notice-body">
                <p>${this._localize("device.yaml_only_section")}</p>
                ${this.yamlPaneVisible?l.s6:(0,l.qy)`<button
                      type="button"
                      class="yaml-only-notice-cta"
                      @click=${this._onShowYamlEditor}
                    >
                      ${this._localize("device.show_yaml_editor")}
                    </button>`}
              </div>
            </div>
            ${this._renderApiActionsTable()} ${this._renderTriggersTable()}
            ${this._renderActionFieldsTable()} ${this._renderActionsRow(o)}`:(0,l.qy)`
            <esphome-config-entry-form
              .entries=${t}
              .values=${this._values}
              .errors=${this._fieldErrors}
              .board=${this.board}
              .yaml=${this.yaml}
              .fromLine=${this._resolvedFromLine}
              .sectionKey=${this.sectionKey}
              .focusFieldPath=${this.focusFieldPath}
              .presentComponents=${this._presentComponents}
              ?show-advanced=${e}
              @value-change=${this._onValueChange}
              @edit-action-field=${this._onEditActionField}
            ></esphome-config-entry-form>
            ${i?iE(e,this._localize,e=>this._setShowAdvanced(e)):l.s6}
            ${this._error?(0,l.qy)`<p class="error">${this._error}</p>`:l.s6}
            ${this._renderApiActionsTable()} ${this._renderTriggersTable()}
            ${this._renderActionsRow(o)}
          `}
      ${this._renderApiActionDialog()} ${this._renderAddAutomationDialog()}
      ${o?(0,l.qy)`<esphome-confirm-dialog
            heading=${this._localize("device.delete_section")}
            confirm-label=${this._localize("device.delete_section")}
            message=${this._localize("device.confirm_delete_section",{name:this._config.title})}
            destructive
            @confirm=${this._onDeleteConfirmed}
          ></esphome-confirm-dialog>`:l.s6}
    `}_renderDeleteButton(){return(0,l.qy)`<button
      class="delete-button"
      ?disabled=${this._deleting}
      @click=${()=>this._confirmDialog?.open()}
    >
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${this._localize("device.delete_section")}
    </button>`}_renderApiActionsTable(){if("api"!==this.sectionKey)return l.s6;let e=I(this.yaml).filter(e=>e.key.startsWith("automation:api_action:")).map(e=>({key:e.key,label:e.id??""}));return(0,l.qy)`<esphome-section-automation-list
      .heading=${this._localize("device.api_actions_list_title")}
      .rows=${e}
      add-label=${this._localize("device.add_api_action")}
      empty-text=${this._localize("device.api_actions_list_empty")}
      edit-label=${this._localize("device.api_actions_list_edit")}
      delete-label=${this._localize("device.api_actions_list_delete")}
      busy-key=${this._deletingRow}
      @add=${this._onOpenAddApiAction}
      @edit=${this._onEditRow}
      @delete=${this._onDeleteRow}
    ></esphome-section-automation-list>`}_renderActionsRow(e){return e?(0,l.qy)`<div class="actions">${this._renderDeleteButton()}</div>`:l.s6}_renderApiActionDialog(){return"api"!==this.sectionKey?l.s6:(0,l.qy)`<esphome-add-api-action-dialog
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .board=${this.board}
      .yaml=${this.yaml}
      @automation-added=${this._onApiActionAdded}
    ></esphome-add-api-action-dialog>`}_shortcutTarget(){if(aR.has(this.sectionKey))return null;if("esphome"===this.sectionKey)return{kind:"device_on"};let e=this._resolveComponentMatch();if(null===e)return null;let t=[e.match.parentKey??e.match.key,this.sectionKey];return this._triggerCatalog.hasTriggersFor(t)?{kind:"component_on",componentId:T(e.sections,e.match)}:null}_resolveComponentMatch(){let e=P(this.yaml),t=e.filter(e=>G(e)===this.sectionKey);return 0===t.length?null:{sections:e,match:void 0!==this._resolvedFromLine?t.find(e=>e.fromLine===this._resolvedFromLine)??t[0]:t[0]}}_resolveComponentId(){let e=this._resolveComponentMatch();return null===e?null:T(e.sections,e.match)}_renderTriggersTable(){let e=this._shortcutTarget();if(null===e)return l.s6;let t=I(this.yaml).filter(t=>!!t.eventKey&&("device_on"===e.kind?"esphome"===t.parentKey:t.id===e.componentId)).map(e=>({key:e.key,label:this._triggerLabel(e)})),i="device_on"===e.kind?this._localize("device.automations_list_title_device"):this._localize("device.automations_list_title");return(0,l.qy)`<esphome-section-automation-list
      .heading=${i}
      .rows=${t}
      add-label=${this._localize("device.add_automation")}
      empty-text=${this._localize("device.automations_list_empty")}
      edit-label=${this._localize("device.automations_list_edit")}
      delete-label=${this._localize("device.automations_list_delete")}
      busy-key=${this._deletingRow}
      @add=${this._onOpenAddAutomation}
      @edit=${this._onEditRow}
      @delete=${this._onDeleteRow}
    ></esphome-section-automation-list>`}_renderActionFieldsTable(){let e=this._resolveComponentId();if(null===e)return l.s6;let t=I(this.yaml).filter(t=>void 0!==t.actionField&&t.id===e).map(e=>({key:e.key,label:iU(e.actionField??"",this._localize)}));return(0,l.qy)`<esphome-section-automation-list
      .heading=${this._localize("device.action_fields_list_title")}
      .rows=${t}
      edit-label=${this._localize("device.action_fields_list_edit")}
      delete-label=${this._localize("device.action_fields_list_delete")}
      busy-key=${this._deletingRow}
      @edit=${this._onEditRow}
      @delete=${this._onDeleteRow}
    ></esphome-section-automation-list>`}_triggerLabel(e){let t=e.displayLabel||e.eventKey||"";return e.eventKey?this._triggerCatalog.resolveName(e.parentKey??"esphome",e.eventKey,t):t}_renderAddAutomationDialog(){return null===this._shortcutTarget()?l.s6:(0,l.qy)`<esphome-add-automation-dialog
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .board=${this.board}
      .yaml=${this.yaml}
      @automation-added=${this._onAutomationAdded}
    ></esphome-add-automation-dialog>`}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.sectionKey="",this.yaml="",this.yamlPaneVisible=!0,this.board=null,this.boardName="",this._config=null,this._values={},this._loading=!1,this._dirty=!1,this._error="",this._deletingRow="",this._isUnknown=!1,this._fieldErrors=new Map,this._advancedShownSections=new Set,this._presentComponents=new Set,this._deleting=!1,this._loadId=0,this._draftTimer=null,this._lastSelfWrittenYaml=null,this._triggerCatalog=new i5(this,()=>({api:this._api,platform:this.board?.esphome.platform||void 0,boardId:this.board?.id})),this._onValueChange=e=>(function(e,t){let{path:i,value:a}=t.detail;e._values=(0,eL.Oe)(e._values,i,a),e._setDirty(!0);let o=i.join(".");if(e._fieldErrors.has(o)){let t=new Map(e._fieldErrors);t.delete(o),e._fieldErrors=t}e._scheduleDraftFlush()})(this,e),this._onDeleteConfirmed=()=>aM(this),this._onOpenAddApiAction=()=>{this._addApiActionDialog?.open()},this._onApiActionAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditRow=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.key},bubbles:!0,composed:!0}))},this._onDeleteRow=async e=>{e.stopPropagation();let t=e.detail.key,i=e_(t);if(this._api&&i&&!this._deletingRow){this._deletingRow=t;try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,i,this.yaml),t=ef(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deletingRow=""}}},this._onOpenAddAutomation=()=>{let e=this._shortcutTarget();null!==e&&("device_on"===e.kind?this._addAutomationDialog?.open({kind:"device_on"}):this._addAutomationDialog?.open({kind:"component_on",componentId:e.componentId}))},this._onAutomationAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditActionField=e=>{e.stopPropagation();let t=this._resolveComponentId();if(null===t)return;let i=eg({kind:"component_action",component_id:t,field:e.detail.field});this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:i},bubbles:!0,composed:!0}))}}}aT.DRAFT_DEBOUNCE_MS=200,aT.styles=[m.G,ed.z,aa],aP([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aT.prototype,"_localize",void 0),aP([(0,n.Fg)({context:u.Ie})],aT.prototype,"_api",void 0),aP([(0,d.MZ)()],aT.prototype,"configuration",void 0),aP([(0,d.MZ)()],aT.prototype,"sectionKey",void 0),aP([(0,d.MZ)({type:Number})],aT.prototype,"fromLine",void 0),aP([(0,d.MZ)({attribute:!1})],aT.prototype,"focusFieldPath",void 0),aP([(0,d.MZ)()],aT.prototype,"yaml",void 0),aP([(0,d.MZ)({type:Boolean})],aT.prototype,"yamlPaneVisible",void 0),aP([(0,d.MZ)({attribute:!1})],aT.prototype,"board",void 0),aP([(0,d.MZ)()],aT.prototype,"boardName",void 0),aP([(0,d.wk)()],aT.prototype,"_config",void 0),aP([(0,d.wk)()],aT.prototype,"_values",void 0),aP([(0,d.wk)()],aT.prototype,"_loading",void 0),aP([(0,d.wk)()],aT.prototype,"_dirty",void 0),aP([(0,d.wk)()],aT.prototype,"_error",void 0),aP([(0,d.wk)()],aT.prototype,"_deletingRow",void 0),aP([(0,d.wk)()],aT.prototype,"_isUnknown",void 0),aP([(0,d.wk)()],aT.prototype,"_fieldErrors",void 0),aP([(0,d.wk)()],aT.prototype,"_advancedShownSections",void 0),aP([(0,d.wk)()],aT.prototype,"_presentComponents",void 0),aP([(0,d.wk)()],aT.prototype,"_resolvedFromLine",void 0),aP([(0,d.P)("esphome-confirm-dialog")],aT.prototype,"_confirmDialog",void 0),aP([(0,d.P)("esphome-add-api-action-dialog")],aT.prototype,"_addApiActionDialog",void 0),aP([(0,d.P)("esphome-add-automation-dialog")],aT.prototype,"_addAutomationDialog",void 0),aP([(0,d.wk)()],aT.prototype,"_deleting",void 0),aT=aP([(0,d.EM)("esphome-device-section-config")],aT);let aR=new Set(["api","script","interval","external_components","packages","substitutions","globals","dashboard_import"]);function aD(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({"open-in-new":s.mdiOpenInNew,memory:s.mdiMemory,"arrow-decision-outline":s.mdiArrowDecisionOutline,"arrow-left":s.mdiArrowLeft,"cog-outline":s.mdiCogOutline,close:s.mdiClose,"party-popper":s.mdiPartyPopper,"plus-circle-outline":s.mdiPlusCircleOutline});class aI extends l.WF{updated(e){if(e.has("board")&&this._refreshAlternateBoards(),e.has("yaml")&&this.selectedSection){var t,i;let a=()=>{this._sectionConfig?.reload(),this._automationEditor?.reload(),this._scriptEditor?.reload(),this._apiActionEditor?.reload()};(this._reloadTimer&&(clearTimeout(this._reloadTimer),this._reloadTimer=null),t=e.get("yaml"),i=this.yaml,t||!i)?this._reloadTimer=setTimeout(a,1e3):a()}}connectedCallback(){super.connectedCallback(),this.addEventListener("request-add-component",this._onRequestAddComponent)}disconnectedCallback(){super.disconnectedCallback(),this._reloadTimer&&clearTimeout(this._reloadTimer),this.removeEventListener("request-add-component",this._onRequestAddComponent)}async _refreshAlternateBoards(){let e=this.board;if(!e){this._alternatesForBoardId=null,this._alternateBoards=[];return}if(e.id!==this._alternatesForBoardId){this._alternatesForBoardId=e.id,this._alternateBoards=[];try{let t=await this._api.getCompatibleBoards(e.id);if(this._alternatesForBoardId!==e.id)return;this._alternateBoards=t.filter(t=>t.id!==e.id)}catch(t){console.error("Failed to load compatible boards:",t),this._alternatesForBoardId===e.id&&(this._alternatesForBoardId=null,this._alternateBoards=[])}}}render(){let e=this.board;return(0,l.qy)`
      ${!this.selectedSection&&e?(0,l.qy)`
            <div class="board-header">
              <div class="board-info">
                <h3 class="board-name">${e.name}</h3>
                <div class="board-tags">
                  ${e.tags.map(e=>(0,l.qy)`<wa-badge variant="brand" pill>${e}</wa-badge>`)}
                  <a
                    class="board-info-link"
                    href=${e.docs_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    ${this._localize("device.more_info")}
                    <wa-icon library="mdi" name="open-in-new"></wa-icon>
                  </a>
                  ${this._alternateBoards.length>0?(0,l.qy)`<button
                        type="button"
                        class="board-change-link"
                        @click=${this._openChangeBoard}
                      >
                        ${this._localize("device.change_board_link")}
                      </button>`:l.s6}
                </div>
                <p class="board-description">${(0,es.G)(e.description)}</p>
              </div>
              <div class="board-image">
                <img
                  src=${(0,en.Ru)(e)}
                  alt=${e.name}
                  referrerpolicy="no-referrer"
                  @error=${en.jt}
                />
              </div>
            </div>
            <div class="board-separator"></div>
          `:l.s6}
      ${this.selectedSection?this._renderSelectedSection():(0,l.qy)`
            ${this.justCreated?this._renderWelcomeBanner():l.s6}
            ${this._renderStepSection({title:this._localize("device.step_core"),desc:this._localize("device.step_core_desc"),icon:"cog-outline",action:this._localize("device.show_core_configuration"),section:"core"})}
            ${this._renderStepSection({title:this._localize("device.step_components"),desc:this._localize("device.step_components_desc"),icon:"memory",action:this._localize("device.show_components"),section:"components"})}
            ${this._renderStepSection({title:this._localize("device.step_automations"),desc:this._localize("device.step_automations_desc"),icon:"arrow-decision-outline",action:this._localize("device.show_automations"),section:"automations"})}
          `}

      <esphome-add-config-dialog
        .boardName=${e?.name??""}
        .configuration=${this.configuration}
        .platform=${e?.esphome.platform??""}
        .board=${e}
        .yaml=${this.yaml}
      ></esphome-add-config-dialog>
      <esphome-add-component-dialog
        .boardName=${e?.name??""}
        .configuration=${this.configuration}
        .platform=${e?.esphome.platform??""}
        .board=${e}
        .yaml=${this.yaml}
      ></esphome-add-component-dialog>
      <esphome-add-automation-dialog
        .boardName=${e?.name??""}
        .configuration=${this.configuration}
        .board=${e}
        .yaml=${this.yaml}
      ></esphome-add-automation-dialog>
      <esphome-change-board-dialog
        .currentBoard=${e}
        .boards=${this._alternateBoards}
        @select-board=${this._onSelectBoard}
      ></esphome-change-board-dialog>
    `}_renderSelectedSection(){let e=this.selectedSection,t=e.startsWith("automation:")?e_(e):null;return t?.kind==="script"?(0,l.qy)`<esphome-script-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
      ></esphome-script-editor>`:t?.kind==="api_action"?(0,l.qy)`<esphome-api-action-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
      ></esphome-api-action-editor>`:t?(0,l.qy)`<esphome-automation-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
      ></esphome-automation-editor>`:(0,l.qy)`<esphome-device-section-config
      .configuration=${this.configuration}
      .sectionKey=${e}
      .fromLine=${this.selectedFromLine}
      .focusFieldPath=${this.focusFieldPath}
      .yaml=${this.yaml}
      .board=${this.board}
      .boardName=${this.board?.name??""}
      ?yamlPaneVisible=${this.yamlPaneVisible}
    ></esphome-device-section-config>`}_renderStepSection(e){return(0,l.qy)`
      <div class="step-section">
        <h4 class="step-title">${e.title}</h4>
        <p class="step-desc">${e.desc}</p>
        <button
          type="button"
          class="action-item"
          @click=${()=>this._onShowNavSection(e.section)}
        >
          <div>
            <wa-icon library="mdi" name=${e.icon}></wa-icon>
            <p>${e.action}</p>
          </div>
          <wa-icon library="mdi" name="arrow-left"></wa-icon>
        </button>
      </div>
    `}_onShowNavSection(e){this.dispatchEvent(new CustomEvent("nav-section-show",{detail:{section:e},bubbles:!0,composed:!0}))}_renderWelcomeBanner(){return this.board?(0,l.qy)`
      <wa-callout class="welcome-banner" variant="brand" role="status">
        <wa-icon slot="icon" library="mdi" name="party-popper"></wa-icon>
        <p class="welcome-banner-title">
          ${this._localize("device.welcome_banner_title",{name:this.board.name})}
        </p>
        <p class="welcome-banner-text">${this._localize("device.welcome_banner_body")}</p>
        <button
          type="button"
          class="welcome-banner-close"
          aria-label=${this._localize("device.welcome_banner_dismiss")}
          @click=${this._onDismissWelcome}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </wa-callout>
    `:l.s6}_onDismissWelcome(){this.dispatchEvent(new CustomEvent("just-created-dismiss",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this._alternateBoards=[],this._alternatesForBoardId=null,this.yaml="",this.configuration="",this.justCreated=!1,this.yamlPaneVisible=!0,this.selectedSection=null,this._reloadTimer=null,this._onRequestAddComponent=e=>{let t=e.detail;t?.domain&&(e.stopPropagation(),this._addComponentDialog?.openWithSearch(t.domain))},this._openChangeBoard=()=>{this._changeBoardDialog?.open()},this._onSelectBoard=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("change-board",{detail:e.detail,bubbles:!0,composed:!0}))}}}function aO(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aI.styles=[m.G,el],aD([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aI.prototype,"_localize",void 0),aD([(0,n.Fg)({context:u.Ie})],aI.prototype,"_api",void 0),aD([(0,d.MZ)({attribute:!1})],aI.prototype,"board",void 0),aD([(0,d.wk)()],aI.prototype,"_alternateBoards",void 0),aD([(0,d.MZ)()],aI.prototype,"yaml",void 0),aD([(0,d.MZ)()],aI.prototype,"configuration",void 0),aD([(0,d.MZ)({type:Boolean})],aI.prototype,"justCreated",void 0),aD([(0,d.MZ)({type:Boolean})],aI.prototype,"yamlPaneVisible",void 0),aD([(0,d.MZ)({attribute:!1})],aI.prototype,"selectedSection",void 0),aD([(0,d.MZ)({type:Number})],aI.prototype,"selectedFromLine",void 0),aD([(0,d.MZ)({attribute:!1})],aI.prototype,"focusFieldPath",void 0),aD([(0,d.P)("esphome-device-section-config")],aI.prototype,"_sectionConfig",void 0),aD([(0,d.P)("esphome-automation-editor")],aI.prototype,"_automationEditor",void 0),aD([(0,d.P)("esphome-script-editor")],aI.prototype,"_scriptEditor",void 0),aD([(0,d.P)("esphome-api-action-editor")],aI.prototype,"_apiActionEditor",void 0),aD([(0,d.P)("esphome-add-component-dialog")],aI.prototype,"_addComponentDialog",void 0),aD([(0,d.P)("esphome-add-automation-dialog")],aI.prototype,"_addAutomationDialog",void 0),aD([(0,d.P)("esphome-add-config-dialog")],aI.prototype,"_addConfigDialog",void 0),aD([(0,d.P)("esphome-change-board-dialog")],aI.prototype,"_changeBoardDialog",void 0),aI=aD([(0,d.EM)("esphome-device-board-info")],aI),(0,b.C)({"alert-circle-outline":s.mdiAlertCircleOutline,"check-circle-outline":s.mdiCheckCircleOutline,"content-save":s.mdiContentSave,eye:s.mdiEye,"eye-off":s.mdiEyeOff,"layout-left":s.mdiDockLeft,"layout-right":s.mdiDockRight,"layout-split":s.mdiViewSplitHorizontal,upload:s.mdiUpload,"vector-difference":s.mdiVectorDifference});class aj extends l.WF{connectedCallback(){super.connectedCallback(),this._isMobile=this._mql.matches,this._mql.addEventListener("change",this._onMqlChange),window.addEventListener("keydown",this._onGlobalKeyDown)}disconnectedCallback(){super.disconnectedCallback(),this._mql.removeEventListener("change",this._onMqlChange),window.removeEventListener("keydown",this._onGlobalKeyDown)}render(){let e,t=this._isMobile&&"both"===this.layout?"right":this.layout,i=!this._isMobile&&this.navCollapsed&&"right"===t,a=this._localize("device.editor_title_ready",{name:this.deviceTitle});return(0,l.qy)`
      <section class="card">
        <header class="card-header ${i?"card-header--compact":""}">
          <slot name="header-start"></slot>
          <div class="editor-header-main">
            <h2 class="editor-header-title">${a}</h2>
          </div>
          <div class="header-actions">
            ${"left"!==t?(e=this._localize(this._revealSensitive?"device.yaml_mask_sensitive":"device.yaml_reveal_sensitive"),(0,l.qy)`<button
                    type="button"
                    class="diff-toggle"
                    aria-pressed=${this._revealSensitive}
                    aria-label=${e}
                    @click=${this._toggleRevealSensitive}
                    title=${e}
                  >
                    <wa-icon
                      library="mdi"
                      name=${this._revealSensitive?"eye-off":"eye"}
                    ></wa-icon>
                  </button>`):l.s6}
            ${this._showDiffButton?(0,l.qy)`<button
                  type="button"
                  class="diff-toggle"
                  aria-pressed=${this._showDiff}
                  ?disabled=${this.yaml===this.savedYaml&&!this._showDiff}
                  @click=${this._toggleDiff}
                  title=${this._showDiff?this._localize("device.diff_view_editor"):this._localize("device.diff_view_diff")}
                >
                  <wa-icon library="mdi" name="vector-difference"></wa-icon>
                </button>`:l.s6}
            <div
              class="layout-toggle"
              aria-label=${this._localize("device.editor_layout_label")}
            >
              <button
                type="button"
                aria-pressed=${"left"===t}
                @click=${()=>this._setLayout("left")}
                title=${this._localize("device.layout_components_only")}
              >
                <wa-icon library="mdi" name="layout-left"></wa-icon>
              </button>
              <button
                class="split-btn"
                type="button"
                aria-pressed=${"both"===t}
                @click=${()=>this._setLayout("both")}
                title=${this._localize("device.layout_split")}
              >
                <wa-icon library="mdi" name="layout-split"></wa-icon>
              </button>
              <button
                type="button"
                aria-pressed=${"right"===t}
                @click=${()=>this._setLayout("right")}
                title=${this._localize("device.layout_yaml_only")}
              >
                <wa-icon library="mdi" name="layout-right"></wa-icon>
              </button>
            </div>
          </div>
        </header>
        <div class="card-body">
          <div class="editor-floating-actions">
            ${this.hasUpdateAvailable?(0,l.qy)`<button
                  type="button"
                  class="install-fab"
                  ?disabled=${this.busy}
                  @click=${this._onUpdate}
                  title=${this._localize("dashboard.update")}
                >
                  <wa-icon library="mdi" name="upload"></wa-icon>
                  ${this._localize("dashboard.update")}
                </button>`:this.hasPendingChanges?(0,l.qy)`<button
                    type="button"
                    class="install-fab"
                    ?disabled=${this.busy}
                    @click=${this._onInstall}
                    title=${this._localize("dashboard.install")}
                  >
                    <wa-icon library="mdi" name="upload"></wa-icon>
                    ${this._localize("dashboard.install")}
                  </button>`:l.s6}
            <!-- Span wrapper carries the title because a disabled
                 button isn't focusable and most browsers won't
                 surface its tooltip on hover. The disabled state
                 is still announced via the button's own disabled
                 attribute; the span just makes the why-disabled
                 hint reachable for mouse users. -->
            <span
              class="validate-button-wrap"
              title=${this.hasUnsavedEdits?this._localize("device.validate_disabled_pending"):this._localize("device.validate_yaml")}
            >
              <button
                type="button"
                class="validate-button"
                ?disabled=${this.hasUnsavedEdits}
                @click=${this._onValidate}
              >
                <wa-icon library="mdi" name="check-circle-outline"></wa-icon>
                ${this._localize("device.validate")}
              </button>
            </span>
            <button
              type="button"
              class="save-button"
              ?disabled=${!this.hasUnsavedEdits}
              @click=${this._onSave}
              title=${this._localize("device.save_yaml")}
            >
              <wa-icon library="mdi" name="content-save"></wa-icon>
              ${this._localize("device.save")}
            </button>
          </div>
          <div class=${`editor-layout ${"both"===t?"editor-layout--both":"left"===t?"editor-layout--left":"editor-layout--right"}`}>
            <div class="editor-pane editor-pane--left">
              <esphome-device-board-info
                .board=${this.board}
                .yaml=${this.yaml}
                .configuration=${this.configuration}
                .selectedSection=${this.selectedSection}
                .selectedFromLine=${this.selectedFromLine}
                .focusFieldPath=${this.focusFieldPath}
                .justCreated=${this.justCreated}
                ?yamlPaneVisible=${"left"!==t}
                @show-yaml-editor=${this._onShowYamlEditor}
              ></esphome-device-board-info>
            </div>
            ${"both"===t?(0,l.qy)`<div class="pane-divider"></div>`:l.s6}
            <div class="editor-pane editor-pane--right">
              ${!this._showDiff&&this._liveErrors.length>0?(0,l.qy)`<div class="invalid-banner" role="alert">
                    <wa-icon
                      library="mdi"
                      name="alert-circle-outline"
                      class="invalid-banner-icon"
                    ></wa-icon>
                    <div class="invalid-banner-text">
                      ${this._liveErrors.slice(0,6).map(e=>(0,l.qy)`<span class="invalid-banner-error">${e}</span>`)}
                      ${this._liveErrors.length>6?(0,l.qy)`<span class="invalid-banner-more"
                            >${this._localize("device.editor_invalid_more",{count:this._liveErrors.length-6})}</span
                          >`:l.s6}
                    </div>
                  </div>`:l.s6}
              <div class="editor-pane-body">
                ${this._showDiff?(0,l.qy)`<esphome-yaml-diff
                      .oldValue=${this.savedYaml}
                      .newValue=${this.yaml}
                    ></esphome-yaml-diff>`:(0,l.qy)`<esphome-yaml-editor
                      .value=${this.yaml}
                      .configuration=${this.configuration}
                      .highlightRange=${this.highlightRange}
                      .scrollToHighlight=${this.scrollToHighlight}
                      .revealSensitive=${this._revealSensitive}
                      @yaml-change=${this._onYamlChange}
                      @yaml-diagnostics=${this._onYamlDiagnostics}
                    ></esphome-yaml-editor>`}
              </div>
            </div>
          </div>
        </div>
      </section>
    `}_onSave(){this.dispatchEvent(new CustomEvent("save-yaml",{bubbles:!0,composed:!0}))}_onValidate(){this.dispatchEvent(new CustomEvent("validate-device",{bubbles:!0,composed:!0}))}_toggleDiff(){this._showDiff=!this._showDiff}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_onInstall(){this.dispatchEvent(new CustomEvent("install-device",{bubbles:!0,composed:!0}))}_onUpdate(){this.dispatchEvent(new CustomEvent("update-device",{bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&(this._liveErrors=[]),this._showDiff&&e.has("_showDiffButton")&&!this._showDiffButton){this._showDiff=!1;return}this._showDiff&&e.has("savedYaml")&&this.yaml===this.savedYaml&&(this._showDiff=!1)}_onYamlDiagnostics(e){if(e.detail.configuration!==this.configuration)return;let t=e.detail.errors;t.length===this._liveErrors.length&&t.every((e,t)=>e===this._liveErrors[t])||(this._liveErrors=t)}_setLayout(e){this.dispatchEvent(new CustomEvent("layout-change",{detail:e,bubbles:!0,composed:!0}))}_onShowYamlEditor(e){e.stopPropagation(),this._setLayout("both")}_onYamlChange(e){this.dispatchEvent(new CustomEvent("yaml-change",{detail:e.detail,bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.yaml="",this.layout="both",this.navCollapsed=!1,this.deviceTitle="",this.board=null,this.justCreated=!1,this._isMobile=!1,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._onGlobalKeyDown=e=>{(e.metaKey||e.ctrlKey)&&!e.shiftKey&&"s"===e.key.toLowerCase()&&(e.preventDefault(),this.hasUnsavedEdits&&this._onSave())},this.highlightRange=null,this.scrollToHighlight=!1,this.configuration="",this.selectedSection=null,this.savedYaml="",this.hasUnsavedEdits=!1,this.hasPendingChanges=!1,this.hasUpdateAvailable=!1,this.busy=!1,this._showDiffButton=!1,this._showDiff=!1,this._revealSensitive=!1,this._liveErrors=[]}}aj.styles=[m.G,ea],aO([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aj.prototype,"_localize",void 0),aO([(0,d.MZ)()],aj.prototype,"yaml",void 0),aO([(0,d.MZ)()],aj.prototype,"layout",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"navCollapsed",void 0),aO([(0,d.MZ)()],aj.prototype,"deviceTitle",void 0),aO([(0,d.MZ)({attribute:!1})],aj.prototype,"board",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"justCreated",void 0),aO([(0,d.wk)()],aj.prototype,"_isMobile",void 0),aO([(0,d.MZ)({attribute:!1})],aj.prototype,"highlightRange",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"scrollToHighlight",void 0),aO([(0,d.MZ)()],aj.prototype,"configuration",void 0),aO([(0,d.MZ)({attribute:!1})],aj.prototype,"selectedSection",void 0),aO([(0,d.MZ)({type:Number})],aj.prototype,"selectedFromLine",void 0),aO([(0,d.MZ)({attribute:!1})],aj.prototype,"focusFieldPath",void 0),aO([(0,d.MZ)({attribute:!1})],aj.prototype,"savedYaml",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"hasUnsavedEdits",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"hasPendingChanges",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"hasUpdateAvailable",void 0),aO([(0,d.MZ)({type:Boolean})],aj.prototype,"busy",void 0),aO([(0,n.Fg)({context:u.El,subscribe:!0}),(0,d.wk)()],aj.prototype,"_showDiffButton",void 0),aO([(0,d.wk)()],aj.prototype,"_showDiff",void 0),aO([(0,d.wk)()],aj.prototype,"_revealSensitive",void 0),aO([(0,d.wk)()],aj.prototype,"_liveErrors",void 0),aj=aO([(0,d.EM)("esphome-device-editor")],aj);var aN=i(1811);let aZ=(0,l.AH)`
  :host {
    display: contents;
  }

  .card {
    background: var(--wa-color-surface-default);
    border-radius: var(--navigator-border-radius, var(--wa-border-radius-l));
    border: var(
      --navigator-border,
      var(--wa-border-width-s) solid var(--wa-color-surface-border)
    );
    box-shadow: var(--wa-elevation-02);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    flex-shrink: 0;
  }

  .card-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .collapse-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: var(--esphome-on-primary);
    cursor: pointer;
    padding: 2px 4px;
    border-radius: var(--wa-border-radius-s);
  }

  .collapse-btn:hover {
    background: color-mix(in srgb, var(--esphome-on-primary), transparent 85%);
  }

  .collapse-btn wa-icon {
    font-size: 18px;
  }

  .card-body {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .italic {
    font-style: italic;
    font-size: var(--wa-font-size-2xs);
    padding: 0 var(--wa-space-m);
    margin: var(--wa-space-xs) 0;
    flex-shrink: 0;
  }

  .separator {
    height: 1px;
    background: var(--wa-color-surface-border);
    margin: var(--wa-space-2xs) 0;
    flex-shrink: 0;
  }

  .nav-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--wa-space-m);
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
  }

  .nav-content:hover p {
    color: var(--esphome-primary);
  }

  .nav-content p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .nav-content wa-icon {
    font-size: var(--wa-font-size-xl);
    color: var(--esphome-primary);
  }

  .nav-items {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-xs) var(--wa-space-m);
  }

  .nav-item {
    padding: 0 var(--wa-space-2xs);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
    transition:
      background 0.1s,
      border-color 0.1s;
  }

  .nav-item:hover,
  .nav-item--hovered {
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
  }

  .nav-item--selected {
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
  }

  .nav-item-content {
    display: flex;
    flex-direction: column;
    min-width: 0;
    padding: var(--wa-space-xs) 0;
  }

  .nav-item-content p {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .nav-item-subtitle {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-weight: normal;
    margin: 0;
    line-height: 1.2;
  }

  .nav-item wa-icon {
    font-size: var(--wa-font-size-xl);
    color: var(--esphome-primary);
  }

  .action-item {
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
    display: flex;
    align-items: center;
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
    transition:
      background 0.1s,
      border-color 0.1s;
  }

  .action-item:hover,
  .action-item--hovered {
    opacity: 0.9;
  }

  .action-item p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .action-item wa-icon {
    font-size: var(--wa-font-size-l);
  }

  .action-item div {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--wa-space-2xs);
  }
`;function aB(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({close:s.mdiClose});class aK extends l.WF{open(){this._id="",this._error="",this._open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration)}catch(e){this._error=e instanceof Error?e.message:String(e)}}render(){let e=this.boardName?this._localize("device.add_script_dialog_title",{name:this.boardName}):this._localize("device.add_script");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      @request-close=${this._onRequestClose}
    >
      <p class="intro">
        ${(0,es.G)(this._localize("device.script_header_description"))}
      </p>
      <div class="field">
        <label class="field-label" for="script-id-input">
          ${this._localize("device.automation_target_script_new_id_label")}
          <span class="required">*</span>
        </label>
        <input
          id="script-id-input"
          type="text"
          .value=${this._id}
          placeholder=${this._localize("device.automation_target_script_id_placeholder")}
          ?disabled=${this._saving}
          @input=${e=>{this._id=iz(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,l.qy)`<p class="error" role="alert">${this._error}</p>`:l.s6}
      <div class="actions">
        <button
          type="button"
          class="primary"
          ?disabled=${this._saving||!this._canContinue()}
          @click=${this._onContinue}
        >
          ${this._saving?this._localize("device.adding"):this._localize("device.add_automation_continue")}
        </button>
      </div>
    </esphome-base-dialog>`}_canContinue(){return!!this._id&&!this._available?.scripts.some(e=>e.id===this._id)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._id="",this._available=null,this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"script",id:this._id},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{mode:"single"},actions:[]},e,this.yaml),i=ef(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:eg(e)},bubbles:!0,composed:!0})),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}function aU(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aK.styles=[m.G,ed.z,(0,l.AH)`
      esphome-base-dialog {
        --width: 480px;
      }
      esphome-base-dialog::part(body) {
        padding: var(--wa-space-l);
      }
      .intro {
        font-size: var(--wa-font-size-s);
        color: var(--wa-color-text-quiet);
        margin: 0 0 var(--wa-space-m) 0;
        line-height: 1.5;
      }
      .intro code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-2xs);
        padding: 1px 4px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
      }
      .field {
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-2xs);
      }
      .field-label {
        font-size: var(--wa-font-size-s);
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-normal);
      }
      .required {
        color: var(--esphome-error, #d92d20);
      }
      .actions {
        display: flex;
        justify-content: flex-end;
        gap: var(--wa-space-s);
        margin-top: var(--wa-space-l);
      }

      .actions button {
        display: inline-flex;
        align-items: center;
        box-sizing: border-box;
        gap: 3px;
        padding: 7px 14px;
        border: var(--wa-border-width-s) solid transparent;
        border-radius: var(--wa-border-radius-m);
        cursor: pointer;
        font-size: var(--wa-font-size-xs);
        font-weight: var(--wa-font-weight-bold);
        font-family: inherit;
        line-height: 1;
        transition:
          background 0.12s,
          border-color 0.12s,
          box-shadow 0.12s,
          transform 0.12s;
      }
      .actions .primary {
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
        box-shadow: var(--esphome-primary-shadow);
      }
      .actions .primary:hover:not(:disabled) {
        background: var(--esphome-primary-hover);
        box-shadow: var(--esphome-primary-shadow-hover);
        transform: translateY(-1px);
      }
      .actions .primary:active:not(:disabled) {
        transform: translateY(0);
      }
      .actions .primary:disabled {
        background: color-mix(
          in srgb,
          var(--esphome-primary) 35%,
          var(--wa-color-surface-default)
        );
        color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
      }
      .error {
        color: var(--esphome-error, #d92d20);
        font-size: var(--wa-font-size-2xs);
        margin-top: var(--wa-space-2xs);
      }
    `],aB([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aK.prototype,"_localize",void 0),aB([(0,n.Fg)({context:u.Ie})],aK.prototype,"_api",void 0),aB([(0,d.MZ)()],aK.prototype,"boardName",void 0),aB([(0,d.MZ)()],aK.prototype,"configuration",void 0),aB([(0,d.MZ)()],aK.prototype,"yaml",void 0),aB([(0,d.MZ)({attribute:!1})],aK.prototype,"board",void 0),aB([(0,d.wk)()],aK.prototype,"_open",void 0),aB([(0,d.wk)()],aK.prototype,"_id",void 0),aB([(0,d.wk)()],aK.prototype,"_available",void 0),aB([(0,d.wk)()],aK.prototype,"_saving",void 0),aB([(0,d.wk)()],aK.prototype,"_error",void 0),aK=aB([(0,d.EM)("esphome-add-script-dialog")],aK),(0,b.C)({"chevron-down":s.mdiChevronDown,"chevron-left":s.mdiChevronLeft,"chevron-up":s.mdiChevronUp,"chevron-right":s.mdiChevronRight,cog:s.mdiCog,"arrow-decision-outline":s.mdiArrowDecisionOutline,memory:s.mdiMemory,"plus-circle-outline":s.mdiPlusCircleOutline,"script-text-outline":s.mdiScriptTextOutline});class aH extends l.WF{connectedCallback(){super.connectedCallback(),this._unsubscribeCache=(0,eC.Ej)(()=>{this._cacheTick++})}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribeCache?.(),this._unsubscribeCache=void 0}willUpdate(e){if((e.has("yaml")||e.has("platform")||e.has("platformReady"))&&this.yaml&&this.platformReady&&this._kickoffNameResolves(),(e.has("selectedKey")||e.has("yaml")||e.has("selectedFromLine"))&&this.yaml){if(!this.selectedKey){this._selectedLine=null,this._selectedRange=null;return}let e=[...P(this.yaml),...I(this.yaml)],t=(void 0!==this.selectedFromLine?e.find(e=>e.fromLine===this.selectedFromLine):void 0)??e.find(e=>G(e)===this.selectedKey);t&&(this._selectedLine=t.fromLine,this._selectedRange={fromLine:t.fromLine,toLine:t.toLine})}}render(){let{core:e,components:t,automations:i}=this._deriveBuckets(this.yaml),a=[{label:this._localize("device.section_core"),desc:this._localize("device.section_core_desc"),items:e,category:"core",actions:[{label:this._localize("device.add_config"),icon:"cog",onClick:()=>this._addConfigDialog.open()}]},{label:this._localize("device.section_components"),desc:this._localize("device.section_components_desc"),items:t,category:"component",actions:[{label:this._localize("device.add_component"),icon:"memory",onClick:()=>this._addComponentDialog.open()}]},{label:this._localize("device.section_automations"),desc:this._localize("device.section_automations_desc"),items:i,category:"automation",actions:[{label:this._localize("device.add_automation"),icon:"arrow-decision-outline",onClick:()=>this._addAutomationDialog.open()},{label:this._localize("device.add_script"),icon:"script-text-outline",onClick:()=>this._addScriptDialog.open()}]}];return(0,l.qy)`
      <section class="card">
        <esphome-add-config-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .platform=${this.platform}
          .board=${this.board}
          .yaml=${this.yaml}
        ></esphome-add-config-dialog>
        <esphome-add-component-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .platform=${this.platform}
          .board=${this.board}
          .yaml=${this.yaml}
        ></esphome-add-component-dialog>
        <esphome-add-automation-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .board=${this.board}
          .yaml=${this.yaml}
          @automation-added=${this._onAutomationAdded}
        ></esphome-add-automation-dialog>
        <esphome-add-script-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .board=${this.board}
          .yaml=${this.yaml}
          @automation-added=${this._onAutomationAdded}
        ></esphome-add-script-dialog>
        <header class="card-header">
          <h2 class="card-title">${this._localize("device.navigator_title")}</h2>
          <button
            type="button"
            class="collapse-btn"
            @click=${this._onCollapseClick}
            title=${this._localize("device.hide_navigator")}
            aria-label=${this._localize("device.hide_navigator")}
          >
            <wa-icon library="mdi" name="chevron-left"></wa-icon>
          </button>
        </header>
        <div class="card-body">
          <p class="italic">${this._localize("device.navigator_desc")}</p>
          <div class="separator"></div>
          ${a.map(({label:e,desc:t,items:i,category:a,actions:o},r)=>{let n=this.openSections.has(r);return(0,l.qy)`
              <div class="nav-content" @click=${()=>this._toggleSection(r)}>
                <p>${e}</p>
                <wa-icon
                  library="mdi"
                  name=${n?"chevron-up":"chevron-down"}
                ></wa-icon>
              </div>
              ${n?(0,l.qy)`
                    <div class="separator"></div>
                    <p class="italic">${t}</p>
                    ${i.length>0?(0,l.qy)`
                          <div class="nav-items">
                            ${i.map(e=>{let{primary:t,secondary:i}=this._navItemLabels(e,a);return(0,l.qy)`
                                <div
                                  class="nav-item ${this._selectedLine===e.fromLine?"nav-item--selected":""} ${this._hoveredLine===e.fromLine?"nav-item--hovered":""}"
                                  @mouseenter=${()=>this._onItemHover(e.fromLine,e.fromLine,e.toLine)}
                                  @mouseleave=${()=>this._onItemLeave()}
                                  @click=${()=>this._onItemClick(e)}
                                >
                                  <div class="nav-item-content">
                                    <p>${t}</p>
                                    ${i?(0,l.qy)`<span class="nav-item-subtitle"
                                          >${i}</span
                                        >`:l.s6}
                                  </div>
                                  <wa-icon library="mdi" name="chevron-right"></wa-icon>
                                </div>
                              `})}
                          </div>
                        `:l.s6}
                    <div class="nav-items">
                      ${o.map(e=>(0,l.qy)`<div class="action-item" @click=${()=>e.onClick()}>
                            <div>
                              <wa-icon library="mdi" name=${e.icon}></wa-icon>
                              <p>${e.label}</p>
                            </div>
                            <wa-icon library="mdi" name="plus-circle-outline"></wa-icon>
                          </div>`)}
                    </div>
                  `:l.s6}
              <div class="separator"></div>
            `})}
        </div>
      </section>
    `}_toggleSection(e){this.dispatchEvent(new CustomEvent("section-toggle",{detail:{index:e},bubbles:!0,composed:!0}))}_kickoffNameResolves(){if(!this._api)return;let{core:e,components:t}=V(P(this.yaml)),i=this.platform||void 0;for(let a of[...e,...t]){let e=G(a);void 0===(0,eC.CQ)(e,i)&&(0,eC.Sn)(this._api,e,i).catch(()=>{})}this._triggerCatalog.ensure()}_navItemLabels(e,t){let i=G(e);if("automation"===t)return this._automationLabels(e,i);let a=i,o=(0,eC.CQ)(i,this.platform||void 0);o?.name&&(a=o.name);let r=e.name||e.id,n=r&&r!==a?r:void 0;return{primary:a,secondary:n}}_automationLabels(e,t){if("script"===e.parentKey){let i=this._localize("device.script_header_title_static"),a=e.id??t;return{primary:i,secondary:a!==i?a:void 0}}if("interval"===e.parentKey){let t=this._localize("device.automation_interval_label"),i=e.meta?.every;return{primary:t,secondary:i?this._localize("device.automation_interval_every_n",{time:i}):void 0}}if("esphome"===e.parentKey&&e.eventKey)return{primary:this._triggerCatalog.resolveName("esphome",e.eventKey,`${this._prettyDomain("esphome")} → ${e.eventKey}`)};if(e.parentKey&&e.eventKey){let t=`${this._prettyDomain(e.parentKey)} → ${e.eventKey}`,i=this._triggerCatalog.resolveName(e.parentKey,e.eventKey,t),a=e.name||e.id;return{primary:i,secondary:a&&a!==i?a:void 0}}return{primary:e.displayLabel||t}}_prettyDomain(e){let t=e.replace(/_/g," ");return t.charAt(0).toUpperCase()+t.slice(1)}_onItemHover(e,t,i){this._hoveredLine=e,this._emitHighlight({fromLine:t,toLine:i},!1)}_onItemLeave(){this._hoveredLine=null,this._emitHighlight(this._selectedRange,!1)}_onItemClick(e){let{fromLine:t,toLine:i}=e,a=G(e);this._selectedLine===t?(this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._emitHighlight(this._hoveredLine===t?{fromLine:t,toLine:i}:null,!1),this._emitSectionSelect(null,void 0)):(this.selectedKey=a,this._selectedLine=t,this._selectedRange={fromLine:t,toLine:i},this._emitHighlight({fromLine:t,toLine:i},!0),this._emitSectionSelect(a,t))}_emitHighlight(e,t){this.dispatchEvent(new CustomEvent("yaml-highlight",{detail:{range:e,scroll:t},bubbles:!0,composed:!0}))}_emitSectionSelect(e,t){this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e,fromLine:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._cacheTick=0,this._triggerCatalog=new i5(this,()=>({api:this._api,platform:this.platform||void 0,boardId:this.board?.id})),this.openSections=new Set,this.yaml="",this._deriveBuckets=(0,aN.A)(e=>{let{core:t,components:i,automations:a}=V(P(e)),o=I(e);return{core:t,components:i,automations:[...a.filter(e=>"script"!==e.key&&"interval"!==e.key),...o].filter(e=>!e.key.startsWith("automation:light_effect:")&&!e.key.startsWith("automation:unscoped:")).sort((e,t)=>e.fromLine-t.fromLine)}}),this.board=null,this.boardName="",this.configuration="",this.platform="",this.platformReady=!1,this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._hoveredLine=null,this._onCollapseClick=()=>{this.dispatchEvent(new CustomEvent("nav-collapse",{bubbles:!0,composed:!0}))},this._onAutomationAdded=e=>{e.stopPropagation(),this._emitSectionSelect(e.detail.sectionKey,void 0)}}}aH.styles=[m.G,aZ],aU([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aH.prototype,"_localize",void 0),aU([(0,n.Fg)({context:u.Ie})],aH.prototype,"_api",void 0),aU([(0,d.wk)()],aH.prototype,"_cacheTick",void 0),aU([(0,d.MZ)({attribute:!1})],aH.prototype,"openSections",void 0),aU([(0,d.MZ)({attribute:!1})],aH.prototype,"yaml",void 0),aU([(0,d.MZ)({attribute:!1})],aH.prototype,"board",void 0),aU([(0,d.MZ)()],aH.prototype,"boardName",void 0),aU([(0,d.MZ)()],aH.prototype,"configuration",void 0),aU([(0,d.MZ)()],aH.prototype,"platform",void 0),aU([(0,d.MZ)({type:Boolean})],aH.prototype,"platformReady",void 0),aU([(0,d.P)("esphome-add-config-dialog")],aH.prototype,"_addConfigDialog",void 0),aU([(0,d.P)("esphome-add-component-dialog")],aH.prototype,"_addComponentDialog",void 0),aU([(0,d.P)("esphome-add-automation-dialog")],aH.prototype,"_addAutomationDialog",void 0),aU([(0,d.P)("esphome-add-script-dialog")],aH.prototype,"_addScriptDialog",void 0),aU([(0,d.MZ)({attribute:!1})],aH.prototype,"selectedKey",void 0),aU([(0,d.MZ)({attribute:!1})],aH.prototype,"selectedFromLine",void 0),aU([(0,d.wk)()],aH.prototype,"_selectedLine",void 0),aU([(0,d.wk)()],aH.prototype,"_selectedRange",void 0),aU([(0,d.wk)()],aH.prototype,"_hoveredLine",void 0),aH=aU([(0,d.EM)("esphome-device-navigator")],aH),i(536),i(1221),i(6895);var aW=i(6286);function aV(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({"alert-outline":s.mdiAlertOutline,"content-save":s.mdiContentSave});class aY extends l.WF{open(){this._resolved=!1,this._open=!0,this._enter.set(!0)}close(){this._open=!1}render(){return(0,l.qy)`
      <esphome-base-dialog
        ?open=${this._open}
        @request-close=${this._onRequestClose}
        @after-hide=${this._onAfterHide}
      >
        <div class="body">
          <div class="icon-wrap">
            <wa-icon library="mdi" name="alert-outline"></wa-icon>
          </div>
          <div class="text">
            <h2 class="heading">${this._localize("device.unsaved_title")}</h2>
            <p class="message">${this._localize("device.unsaved_message")}</p>
          </div>
        </div>
        <div class="actions">
          <button class="btn btn--ghost" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
          <button class="btn btn--discard" @click=${this._onDiscard}>
            ${this._localize("device.discard_changes")}
          </button>
          <button class="btn btn--save" @click=${this._onSave}>
            <wa-icon library="mdi" name="content-save"></wa-icon>
            ${this._localize("device.save_and_leave")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_onDiscard(){this._resolved=!0,this.close(),this.dispatchEvent(new CustomEvent("discard",{bubbles:!0,composed:!0}))}_onSave(){this._resolved||(this._resolved=!0,this.close(),this.dispatchEvent(new CustomEvent("save",{bubbles:!0,composed:!0})))}_onAfterHide(){this._open=!1,this._enter.set(!1),this._resolved||this.dispatchEvent(new CustomEvent("cancel",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._open=!1,this._resolved=!1,this._enter=new aW.J(this,()=>this._onSave()),this._onRequestClose=()=>{this._open=!1}}}aY.styles=[m.G,(0,l.AH)`
      esphome-base-dialog {
        --width: 460px;
      }

      /* This prompt renders its own icon + heading in the body, so the
         wrapper's title/close-button header isn't used — hide it (and the
         unused footer). The shared close-button-clearance fix is moot here. */
      esphome-base-dialog::part(header),
      esphome-base-dialog::part(footer) {
        display: none;
      }

      esphome-base-dialog::part(body) {
        padding: 0;
      }

      .body {
        display: flex;
        gap: var(--wa-space-m);
        padding: var(--wa-space-l) var(--wa-space-l) var(--wa-space-m);
      }

      .icon-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        flex-shrink: 0;
        background: color-mix(in srgb, var(--esphome-warning), transparent 85%);
        color: var(--esphome-warning);
      }

      .icon-wrap wa-icon {
        font-size: 24px;
      }

      .text {
        flex: 1;
        min-width: 0;
      }

      .heading {
        margin: 0 0 var(--wa-space-2xs);
        font-size: var(--wa-font-size-m);
        font-weight: var(--wa-font-weight-bold);
        color: var(--wa-color-text-normal);
      }

      .message {
        margin: 0;
        font-size: var(--wa-font-size-s);
        color: var(--wa-color-text-quiet);
        line-height: 1.5;
      }

      .actions {
        display: flex;
        justify-content: flex-end;
        gap: var(--wa-space-xs);
        padding: var(--wa-space-s) var(--wa-space-m) var(--wa-space-m);
      }

      .btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: var(--wa-border-radius-m);
        font-size: var(--wa-font-size-s);
        font-weight: var(--wa-font-weight-bold);
        font-family: inherit;
        cursor: pointer;
        border: none;
        transition:
          background 0.12s,
          color 0.12s;
      }

      .btn--ghost {
        background: transparent;
        color: var(--wa-color-text-quiet);
      }

      .btn--ghost:hover {
        background: var(--wa-color-surface-lowered);
        color: var(--wa-color-text-normal);
      }

      .btn--discard {
        background: transparent;
        color: var(--esphome-error);
      }

      .btn--discard:hover {
        background: color-mix(in srgb, var(--esphome-error), transparent 92%);
      }

      .btn--save {
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
        box-shadow: 0 1px 2px color-mix(in srgb, var(--esphome-primary), transparent 70%);
      }

      .btn--save:hover {
        background: var(--esphome-primary-hover);
      }

      .btn wa-icon {
        font-size: 16px;
      }
    `],aV([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aY.prototype,"_localize",void 0),aV([(0,d.wk)()],aY.prototype,"_open",void 0),aY=aV([(0,d.EM)("esphome-unsaved-changes-dialog")],aY);var aG=i(6029);function aJ(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,b.C)({"alert-outline":s.mdiAlertOutline});class aQ extends l.WF{open(){this._resolvedExit=null,this._open=!0,this._enter.set(!0)}close(){this._open=!1}render(){let e=1===this.errorCount?"device.yaml_invalid_message_singular":"device.yaml_invalid_message_plural",t=this._localize(e,{count:String(this.errorCount)}),i=this.firstErrorLine>0;return(0,l.qy)`
      <esphome-base-dialog
        ?open=${this._open}
        .label=${this._localize("device.yaml_invalid_title")}
        @request-close=${this._onRequestClose}
        @after-hide=${this._onAfterHide}
      >
        <div class="body">
          <div class="icon-wrap">
            <wa-icon library="mdi" name="alert-outline"></wa-icon>
          </div>
          <div class="text">
            ${t}
            ${this.firstErrorMessage?(0,l.qy)`<div class="first-error">${this.firstErrorMessage}</div>`:l.s6}
          </div>
        </div>
        <div class="actions">
          <button class="btn btn--cancel" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
          <button class="btn btn--goto" ?disabled=${!i} @click=${this._goto}>
            ${this._localize("device.yaml_invalid_go_to_error")}
          </button>
          <button class="btn btn--save-anyway" @click=${this._saveAnyway}>
            ${this._localize("device.yaml_invalid_save_anyway")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_goto(){null===this._resolvedExit&&(this._resolvedExit="goto",this.close(),this.dispatchEvent(new CustomEvent("goto",{detail:{line:this.firstErrorLine,col:this.firstErrorCol},bubbles:!0,composed:!0})))}_saveAnyway(){this._resolvedExit="save-anyway",this.close(),this.dispatchEvent(new CustomEvent("save-anyway",{bubbles:!0,composed:!0}))}_onAfterHide(){this._open=!1,this._enter.set(!1),null===this._resolvedExit&&this.dispatchEvent(new CustomEvent("cancel",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.errorCount=0,this.firstErrorLine=0,this.firstErrorCol=0,this.firstErrorMessage="",this._open=!1,this._resolvedExit=null,this._enter=new aW.J(this,()=>{this.firstErrorLine>0&&this._goto()}),this._onRequestClose=()=>{this._open=!1}}}function aX(e,t,i,a){var o,r=arguments.length,n=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(r<3?o(n):r>3?o(t,i,n):o(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aQ.styles=[m.G,aG.W,(0,l.AH)`
      esphome-base-dialog {
        --width: 480px;
      }

      .icon-wrap {
        background: color-mix(in srgb, var(--esphome-error), transparent 88%);
        color: var(--esphome-error);
      }

      .first-error {
        margin-top: var(--wa-space-xs);
        font-family: var(--wa-font-family-code);
        font-size: var(--wa-font-size-2xs);
        color: var(--wa-color-text-normal);
        background: var(--wa-color-surface-lowered);
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-s);
        padding: var(--wa-space-xs) var(--wa-space-s);
        white-space: pre-wrap;
        word-break: break-word;
      }

      .btn--goto {
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
      }

      .btn--goto:hover:not(:disabled) {
        background: var(--esphome-primary-hover);
      }

      .btn--save-anyway {
        background: var(--esphome-error);
        color: var(--esphome-on-primary);
      }

      .btn--save-anyway:hover {
        background: color-mix(in srgb, var(--esphome-error), black 10%);
      }
    `],aJ([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aQ.prototype,"_localize",void 0),aJ([(0,d.MZ)({type:Number})],aQ.prototype,"errorCount",void 0),aJ([(0,d.MZ)({type:Number})],aQ.prototype,"firstErrorLine",void 0),aJ([(0,d.MZ)({type:Number})],aQ.prototype,"firstErrorCol",void 0),aJ([(0,d.MZ)()],aQ.prototype,"firstErrorMessage",void 0),aJ([(0,d.wk)()],aQ.prototype,"_open",void 0),aQ=aJ([(0,d.EM)("esphome-yaml-validation-dialog")],aQ),(0,b.C)({"arrow-left":s.mdiArrowLeft,"chevron-right":s.mdiChevronRight});class a0 extends l.WF{get _device(){return this._devices.find(e=>e.configuration===this.id)??null}_createInstallController(){let e=this;return new p({addController:t=>e.addController(t),removeController:t=>e.removeController(t),requestUpdate:()=>e.requestUpdate(),get updateComplete(){return e.updateComplete},get device(){return e._device},get commandDialog(){return e._commandDialog??null},get firmwareDialog(){return e._firmwareDialog??null}})}get _isYamlDirty(){return this._yaml!==this._savedYaml}get _isDirty(){return this._isYamlDirty||this._sectionDirty}async connectedCallback(){super.connectedCallback(),this._loadPreferences(),(0,f.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("keydown",this._onKeydown),this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),(0,f.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),window.removeEventListener("keydown",this._onKeydown),this._mql.removeEventListener("change",this._onMqlChange),this._unsavedGuard.cancelPending()}_isTextEntry(e){if(!e)return!1;let t=e.tagName;if("INPUT"===t||"TEXTAREA"===t||"SELECT"===t||e.isContentEditable)return!0;let i=e;for(;i;){if("ESPHOME-YAML-EDITOR"===i.tagName)return!0;i=i.parentElement}return!1}updated(e){e.has("id")&&this.id&&(this._justCreated=(0,g.RI)(this.id),this._loadedBoardId=null,this._board=null,this._platformReady=!1,this._loadYaml());let t=this._device?.board_id??null;t&&t!==this._loadedBoardId?(this._loadedBoardId=t,this._board=null,this._platformReady=!1,this._loadBoard(t)):!t&&(null!==this._loadedBoardId&&(this._loadedBoardId=null,this._board=null),(null!==this._device||this._devicesLoaded)&&(this._platformReady=!0))}async _loadPreferences(){let e=localStorage.getItem("esphome-editor-layout");("both"===e||"left"===e||"right"===e)&&(this._layout=e);try{let e=await this._api.getPreferences();this._navCollapsed=!e.navigator_visible}catch{}}async _loadBoard(e){try{let t=await this._api.getBoard(e);this._loadedBoardId===e&&(this._board=t,this._platformReady=!0)}catch(t){console.error("Failed to load board:",t),this._loadedBoardId===e&&(this._board=null,this._platformReady=!0)}}async _loadYaml(){try{let e=await this._api.getConfig(this.id);this._yaml=e,this._savedYaml=e,this._maybeResolveLineFromUrl()}catch(e){console.error("Failed to load YAML:",e)}}_maybeResolveLineFromUrl(){let e=Q(this._yaml,this._selectedFromLine,this._selectedSection);e&&(this._selectedSection=e.sectionKey,this._highlightRange=e.range,this._scrollToHighlight=!0)}_resolveValidationPrompt(e){let t=this._pendingValidationResolve;this._pendingValidationResolve=null,t?.(e)}render(){let e=this._device?.friendly_name||this._device?.name||this.id||this._localize("dashboard.create_device"),t=this._isMobile?!this._drawerOpen:this._navCollapsed,i=this._localize("device.back");return(0,l.qy)`
      <!-- Mobile drawer -->
      <div
        class="drawer-backdrop ${this._drawerOpen?"drawer-backdrop--open":""}"
        @click=${()=>{this._drawerOpen=!1}}
      ></div>
      <div
        class="drawer ${this._drawerOpen?"drawer--open":""}"
        @section-toggle=${this._onSectionToggle}
        @section-select=${this._onSectionSelect}
        @yaml-highlight=${this._onYamlHighlight}
        @yaml-updated=${this._onYamlUpdated}
        @yaml-draft=${this._onYamlDraft}
        @nav-collapse=${this._onNavCollapse}
      >
        ${this._renderNavigator("drawer-nav")}
      </div>

      <div class="page">
        <div
          class="layout-grid ${this._navCollapsed?"nav-collapsed":""}"
          @section-toggle=${this._onSectionToggle}
          @layout-change=${this._onLayoutChange}
          @yaml-change=${this._onYamlChange}
          @yaml-cursor-line=${this._onYamlCursorLine}
          @yaml-highlight=${this._onYamlHighlight}
          @yaml-updated=${this._onYamlUpdated}
          @yaml-draft=${this._onYamlDraft}
          @section-select=${this._onSectionSelect}
          @section-mount=${this._onSectionMount}
          @section-unmount=${this._onSectionUnmount}
          @field-focus=${this._onFieldFocus}
          @dirty-change=${this._onSectionDirtyChange}
          @nav-section-show=${this._onNavSectionShow}
          @nav-collapse=${this._onNavCollapse}
          @save-yaml=${this._saveYaml}
          @validate-device=${this._onValidateClick}
          @install-device=${this._installCtrl.onInstall}
          @update-device=${this._installCtrl.onUpdate}
        >
          ${this._renderNavigator("desktop-nav")}
          <esphome-device-editor
            .yaml=${this._yaml}
            .savedYaml=${this._savedYaml}
            .layout=${this._layout}
            ?navCollapsed=${this._navCollapsed}
            .deviceTitle=${e}
            .board=${this._board}
            .highlightRange=${this._highlightRange}
            .scrollToHighlight=${this._scrollToHighlight}
            .configuration=${this.id}
            .selectedSection=${this._selectedSection}
            .selectedFromLine=${this._selectedFromLine}
            .focusFieldPath=${this._focusFieldPath}
            .justCreated=${this._justCreated}
            @just-created-dismiss=${this._dismissJustCreated}
            @change-board=${this._onChangeBoard}
            ?hasUnsavedEdits=${this._isDirty}
            ?hasPendingChanges=${this._device?.has_pending_changes===!0}
            ?hasUpdateAvailable=${this._device?.update_available===!0}
            ?busy=${this._activeJobs.has(this.id)}
          >
            ${this._selectedSection?(0,l.qy)`<button
                  slot="header-start"
                  class="back-btn"
                  @click=${this._onBack}
                  title=${i}
                  aria-label=${i}
                >
                  <wa-icon library="mdi" name="arrow-left"></wa-icon>
                </button>`:l.s6}
          </esphome-device-editor>
        </div>
        ${t?(0,l.qy)`<button
              type="button"
              class="nav-edge-tab"
              @click=${this._onNavExpand}
              title=${this._localize("device.show_navigator")}
              aria-label=${this._localize("device.show_navigator")}
            >
              <wa-icon library="mdi" name="chevron-right"></wa-icon>
            </button>`:l.s6}
      </div>
      <esphome-unsaved-changes-dialog
        @discard=${this._onUnsavedDiscard}
        @save=${this._onUnsavedSave}
        @cancel=${this._onUnsavedCancel}
      ></esphome-unsaved-changes-dialog>
      <esphome-command-dialog
        @request-show-logs-after-install=${this._onPostInstallShowLogs}
        @request-open-editor=${this._onRequestOpenEditor}
      ></esphome-command-dialog>
      <esphome-firmware-install-dialog
        @request-show-logs-after-install=${this._onPostInstallShowLogs}
        @clean-build=${this._onCleanBuild}
        @request-open-editor=${this._onRequestOpenEditor}
      ></esphome-firmware-install-dialog>
      <esphome-logs-dialog></esphome-logs-dialog>
      <esphome-install-method-dialog
        ?open=${this._installCtrl.installMethodOpen}
        .deviceState=${this._installCtrl.deviceState}
        .deviceTargetPlatform=${this._installCtrl.deviceTargetPlatform}
        .deviceCurrentAddress=${this._installCtrl.deviceCurrentAddress}
        @close=${this._installCtrl.onInstallMethodClose}
        @select-method=${this._installCtrl.onInstallMethodSelect}
      ></esphome-install-method-dialog>
      <esphome-yaml-validation-dialog
        .errorCount=${this._validationErrorCount}
        .firstErrorLine=${this._validationFirstLine}
        .firstErrorCol=${this._validationFirstCol}
        .firstErrorMessage=${this._validationFirstMessage}
        @save-anyway=${this._onValidationSaveAnyway}
        @goto=${this._onValidationGoTo}
        @cancel=${this._onValidationCancel}
      ></esphome-yaml-validation-dialog>
    `}_onSectionToggle(e){let{index:t}=e.detail,i=new Set;this._openSections.has(t)||i.add(t),this._openSections=i,this._updateUrl()}_onNavSectionShow(e){let t={core:0,components:1,automations:2}[e.detail.section];if(void 0===t)return;let i=new Set([t]);this._openSections=i,this._updateUrl(),this._drawerOpen=!0,this._navCollapsed&&(this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{}))}_onLayoutChange(e){this._layout=e.detail,localStorage.setItem("esphome-editor-layout",e.detail)}_renderNavigator(e){return(0,l.qy)`<esphome-device-navigator
      class=${e}
      .openSections=${this._openSections}
      .yaml=${this._yaml}
      .board=${this._board}
      .boardName=${this._board?.name??""}
      .configuration=${this.id}
      .platform=${this._board?.esphome.platform??""}
      .platformReady=${this._platformReady}
      .selectedKey=${this._selectedSection}
      .selectedFromLine=${this._selectedFromLine}
    ></esphome-device-navigator>`}_onYamlChange(e){this._yaml=e.detail.value,this._retryPendingFieldLine()}_onYamlCursorLine(e){this._clearPendingFieldLine();let t=Y(this._yaml,e.detail.line);if(!t)return;let i=e.detail.path??[],a=i.length>1&&x.has(i[0])?i:i.slice(1),o=G(t);if(o===this._selectedSection&&t.fromLine===this._selectedFromLine){this._focusFieldPath=a;return}this._guardSectionSwitch(()=>{this._selectedSection=o,this._selectedFromLine=t.fromLine,this._focusFieldPath=a,this._updateUrl()})}_focusedSection(){if(!this._selectedSection)return;let e=P(this._yaml);return(void 0!==this._selectedFromLine?e.find(e=>e.fromLine===this._selectedFromLine):void 0)??e.find(e=>G(e)===this._selectedSection)}_highlightFieldLine(e){let t=this._focusedSection(),i=t?function(e,t,i){if(i[0]===t.key&&(i=i.slice(1)),0===i.length)return null;let a=e.split("\n"),o=t.fromLine-1,r=Math.min(t.toLine-1,a.length-1);if(o<0||o>=a.length)return null;let n=e=>S.test(e)?R(e):(0,q._j)(e),s=(e,t)=>{for(let i=e;i<=t;i++){let e=(0,q.eJ)(a[i]);if(e.trim())return(0,q._j)(e)}return null},l=(e,t,i,o)=>{let r=o[0],d=o.slice(1);if(M.test(r)){let o=[];for(let r=e;r<=t;r++){let e=(0,q.eJ)(a[r]);e.trim()&&(0,q._j)(e)===i&&S.test(e)&&o.push(r)}if(o.length){let e=o[Number(r)];return void 0===e?null:0===d.length?e+1:l(e,Number(r)+1<o.length?o[Number(r)+1]-1:t,R(a[e]),d)}}for(let o=e;o<=t;o++){let e=(0,q.eJ)(a[o]);if(!e.trim()||n(e)!==i)continue;let c=e.match(q.Ud);if(!c||c[1]!==r)continue;if(0===d.length)return o+1;let h=t;for(let e=o+1;e<=t;e++){let t=(0,q.eJ)(a[e]);if(t.trim()&&(0,q._j)(t)<=i){h=e-1;break}}let p=s(o+1,h);return null===p?null:l(o+1,h,p,d)}return null};if(S.test(a[o]))return l(o,r,R(a[o]),i);let d=s(o+1,r);return null===d?null:l(o+1,r,d,i)}(this._yaml,t,e):null;return null!==i&&(this._highlightRange={fromLine:i,toLine:i},this._scrollToHighlight=!0),{section:t,found:null!==i}}_onFieldFocus(e){let t=this._focusedFieldPath=e.detail.path;if(!t.length)return;let{section:i,found:a}=this._highlightFieldLine(t);a?this._clearPendingFieldLine():(this._pendingFieldLine=!0,this._pendingFieldSection={section:this._selectedSection,fromLine:this._selectedFromLine},this._highlightRange=i?{fromLine:i.fromLine,toLine:i.toLine}:null,this._scrollToHighlight=void 0!==i)}_retryPendingFieldLine(){if(this._pendingFieldLine&&this._focusedFieldPath?.length){if(this._pendingFieldSection?.section!==this._selectedSection||this._pendingFieldSection?.fromLine!==this._selectedFromLine)return void this._clearPendingFieldLine();this._highlightFieldLine(this._focusedFieldPath).found&&this._clearPendingFieldLine()}}_clearPendingFieldLine(){this._pendingFieldLine=!1,this._pendingFieldSection=void 0}_onYamlHighlight(e){this._highlightRange=e.detail.range,this._scrollToHighlight=e.detail.scroll}_onYamlUpdated(e){this._yaml=e.detail.yaml,this._savedYaml=e.detail.yaml}_onYamlDraft(e){this._yaml=e.detail.yaml,this._retryPendingFieldLine()}_onSectionSelect(e){let{sectionKey:t,fromLine:i}=e.detail;if(t===this._selectedSection&&i===this._selectedFromLine){this._drawerOpen=!1;return}this._guardSectionSwitch(()=>{let e=this._selectedSection,a=this._selectedFromLine;null===t?this._sectionHistory=[]:null!==e&&(this._sectionHistory=[...this._sectionHistory,{key:e,fromLine:a}]),this._selectedSection=t,this._selectedFromLine=i,this._drawerOpen=!1,this._updateUrl()})}_guardSectionSwitch(e){this._activeSection?.flushPending(),e()}_readUrlParam(e,t){return new URLSearchParams(window.location.search).get(e)??t}_readUrlLine(){let e=new URLSearchParams(window.location.search).get("line");if(!e)return;let t=Number(e);return Number.isNaN(t)?void 0:t}_readUrlSections(){let e=new URLSearchParams(window.location.search).get("open");return e?e.split(",").map(Number).filter(e=>!Number.isNaN(e)):[]}_updateUrl(){let e=new URLSearchParams(window.location.search);this._selectedSection?(e.set("section",this._selectedSection),void 0!==this._selectedFromLine?e.set("line",String(this._selectedFromLine)):e.delete("line")):(e.delete("section"),e.delete("line")),this._openSections.size>0?e.set("open",[...this._openSections].join(",")):e.delete("open");let t=e.toString(),i=`${window.location.pathname}${t?`?${t}`:""}`;window.history.replaceState(window.history.state,"",i)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._devicesLoaded=!1,this._activeJobs=new Map,this.id="",this._justCreated=!1,this._layout="both",this._openSections=new Set(this._readUrlSections()),this._board=null,this._platformReady=!1,this._loadedBoardId=null,this._highlightRange=null,this._scrollToHighlight=!1,this._selectedSection=this._readUrlParam("section",null),this._selectedFromLine=this._readUrlLine(),this._pendingFieldLine=!1,this._sectionHistory=[],this._drawerOpen=!1,this._navCollapsed=!1,this._isMobile=window.matchMedia("(max-width: 900px)").matches,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._yaml="",this._savedYaml="",this._activeSection=null,this._sectionDirty=!1,this._validationErrorCount=0,this._validationFirstLine=0,this._validationFirstCol=0,this._validationFirstMessage="",this._onPostInstallShowLogs=(0,_.ei)(()=>this._logsDialog,()=>this._localize),this._installCtrl=this._createInstallController(),this._unsavedGuard=new A,this._allowingLeave=!1,this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._confirmLeave=async()=>{this._activeSection?.flushPending();let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>(!this._isYamlDirty||!!await this._saveYaml())&&(this._allowingLeave=!0,!0)});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._activeSection?.flushPending(),this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._activeSection?.flushPending(),this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,v.cV)(`/device/${this.id}`)),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onKeydown=e=>{if("Escape"!==e.key||e.defaultPrevented)return;let t=e.composedPath()[0];if(!this._isTextEntry(t)){if(this._drawerOpen){e.preventDefault(),this._drawerOpen=!1;return}e.preventDefault(),window.history.back()}},this._dismissJustCreated=()=>{this._justCreated=!1},this._onChangeBoard=async e=>{let t=e.detail?.boardId,i=this._device;if(t&&i&&t!==i.board_id){if(this._isDirty)return void c.A.error(this._localize("device.change_board_unsaved"),{richColors:!0});try{await this._api.updateDevice({configuration:i.configuration,board_id:t}),await this._loadYaml(),c.A.success(this._localize("device.change_board_success"),{richColors:!0})}catch(e){console.error("Failed to change board:",e),c.A.error(this._localize("device.change_board_error"),{richColors:!0})}}},this._pendingValidationResolve=null,this._saveYaml=async()=>{if(await this._activeSection?.flushPending(),!this._isYamlDirty)return!0;if(this.id)try{let e=(0,X.mL)(this.id,this._yaml)??await this._api.validateYaml(this.id,this._yaml),t=function(e){let t=e.yaml_errors??[],i=e.validation_errors??[],a=t.length+i.length;if(0===a)return{count:0,first:null};if(t.length>0){let e=(t[0].message??"").trim(),i=0,o=0,r=e.match(ee);if(r)i=Number.parseInt(r[1],10),o=Number.parseInt(r[2],10);else{let t=e.match(et);t&&(i=Number.parseInt(t[1],10))}return(!Number.isFinite(i)||i<1)&&(i=0),(!Number.isFinite(o)||o<1)&&(o=0),{count:a,first:{line:i,col:o,message:e||"Invalid YAML"}}}let o=i[0],r=Math.max(1,(o.range?.start_line??0)+1),n=Math.max(1,(o.range?.start_col??0)+1);return{count:a,first:{line:r,col:n,message:(o.message??"Invalid configuration").trim()}}}(e);if(t.count>0)return this._validationErrorCount=t.count,this._validationFirstLine=t.first?.line??0,this._validationFirstCol=t.first?.col??0,this._validationFirstMessage=t.first?.message??"",this._pendingValidationResolve?.(!1),new Promise(e=>{this._pendingValidationResolve=e,this._yamlValidationDialog.open()})}catch(e){console.debug("[save-yaml] validate_yaml failed, saving anyway:",e)}return this._doSaveYaml()},this._doSaveYaml=async()=>{let e=this._savedYaml;this._savedYaml=this._yaml;let t=!0;try{await this._api.updateConfig(this.id,this._yaml)}catch(i){(i instanceof Error?i.message:"").includes("timed out")||(t=!1,this._savedYaml=e,console.error("Failed to save YAML:",i))}let i=t?"device.yaml_saved":"device.yaml_save_error";return(t?c.A.success:c.A.error)(this._localize(i),{richColors:!0}),t},this._onValidationSaveAnyway=async()=>{let e=await this._doSaveYaml();this._resolveValidationPrompt(e)},this._onValidationGoTo=e=>{let t=e.detail.line;if(t&&t>=1){"left"===this._layout&&(this._layout="both",localStorage.setItem("esphome-editor-layout","both")),this._highlightRange={fromLine:t,toLine:t},this._scrollToHighlight=!0;let e=Q(this._yaml,t,null);e&&(this._selectedSection=e.sectionKey)}this._resolveValidationPrompt(!1)},this._onValidationCancel=()=>{this._resolveValidationPrompt(!1)},this._onValidateClick=()=>{this._device&&(this._commandDialog.configuration=this._device.configuration,this._commandDialog.name=this._device.friendly_name||this._device.name,this._commandDialog.open("validate"))},this._onCleanBuild=e=>{let t=e.detail;this._commandDialog.configuration=t.configuration,this._commandDialog.name=t.friendly_name||t.name,this._commandDialog.open("clean")},this._onRequestOpenEditor=e=>{e.stopPropagation(),e.detail.configuration!==this._device?.configuration&&(0,f.oo)(`/device/${encodeURIComponent(e.detail.configuration)}`)},this._onBack=()=>{this._guardSectionSwitch(()=>{let e=this._sectionHistory.length?this._sectionHistory[this._sectionHistory.length-1]:null;e?(this._sectionHistory=this._sectionHistory.slice(0,-1),this._selectedSection=e.key,this._selectedFromLine=e.fromLine):(this._selectedSection=null,this._selectedFromLine=void 0),this._highlightRange=null,this._scrollToHighlight=!1,this._updateUrl()})},this._onNavExpand=()=>{if(this._isMobile){this._drawerOpen=!0;return}this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{})},this._onNavCollapse=()=>{if(this._isMobile){this._drawerOpen=!1;return}this._navCollapsed=!0,this._api.updatePreferences({navigator_visible:!1}).catch(()=>{})},this._onSectionMount=e=>{this._activeSection=e.detail.node,this._sectionDirty=e.detail.node.dirty},this._onSectionUnmount=e=>{this._activeSection===e.detail.node&&(this._activeSection=null,this._sectionDirty=!1)},this._onSectionDirtyChange=e=>{this._sectionDirty=e.detail.dirty}}}a0.styles=[m.G,ei],aX([(0,n.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],a0.prototype,"_localize",void 0),aX([(0,n.Fg)({context:u.xJ,subscribe:!0}),(0,d.wk)()],a0.prototype,"_devices",void 0),aX([(0,n.Fg)({context:u.UL,subscribe:!0}),(0,d.wk)()],a0.prototype,"_devicesLoaded",void 0),aX([(0,n.Fg)({context:u.Ie})],a0.prototype,"_api",void 0),aX([(0,n.Fg)({context:u.EM,subscribe:!0}),(0,d.wk)()],a0.prototype,"_activeJobs",void 0),aX([(0,d.MZ)()],a0.prototype,"id",void 0),aX([(0,d.wk)()],a0.prototype,"_justCreated",void 0),aX([(0,d.wk)()],a0.prototype,"_layout",void 0),aX([(0,d.wk)()],a0.prototype,"_openSections",void 0),aX([(0,d.wk)()],a0.prototype,"_board",void 0),aX([(0,d.wk)()],a0.prototype,"_platformReady",void 0),aX([(0,d.wk)()],a0.prototype,"_highlightRange",void 0),aX([(0,d.wk)()],a0.prototype,"_scrollToHighlight",void 0),aX([(0,d.wk)()],a0.prototype,"_selectedSection",void 0),aX([(0,d.wk)()],a0.prototype,"_selectedFromLine",void 0),aX([(0,d.wk)()],a0.prototype,"_focusFieldPath",void 0),aX([(0,d.wk)()],a0.prototype,"_sectionHistory",void 0),aX([(0,d.wk)()],a0.prototype,"_drawerOpen",void 0),aX([(0,d.wk)()],a0.prototype,"_navCollapsed",void 0),aX([(0,d.wk)()],a0.prototype,"_isMobile",void 0),aX([(0,d.wk)()],a0.prototype,"_yaml",void 0),aX([(0,d.wk)()],a0.prototype,"_savedYaml",void 0),aX([(0,d.P)("esphome-unsaved-changes-dialog")],a0.prototype,"_unsavedDialog",void 0),aX([(0,d.wk)()],a0.prototype,"_sectionDirty",void 0),aX([(0,d.P)("esphome-command-dialog")],a0.prototype,"_commandDialog",void 0),aX([(0,d.P)("esphome-firmware-install-dialog")],a0.prototype,"_firmwareDialog",void 0),aX([(0,d.P)("esphome-logs-dialog")],a0.prototype,"_logsDialog",void 0),aX([(0,d.P)("esphome-yaml-validation-dialog")],a0.prototype,"_yamlValidationDialog",void 0),aX([(0,d.wk)()],a0.prototype,"_validationErrorCount",void 0),aX([(0,d.wk)()],a0.prototype,"_validationFirstLine",void 0),aX([(0,d.wk)()],a0.prototype,"_validationFirstCol",void 0),aX([(0,d.wk)()],a0.prototype,"_validationFirstMessage",void 0),a0=aX([(0,d.EM)("esphome-page-device")],a0)}}]);
//# sourceMappingURL=843.620b65a945bc7069.js.map