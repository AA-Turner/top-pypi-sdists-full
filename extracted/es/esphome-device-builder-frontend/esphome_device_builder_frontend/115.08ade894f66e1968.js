"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[115],{7958(e,t,i){let a,o;i.r(t),i.d(t,{ESPHomePageDevice:()=>oN});var r,s=i(5172),n=i(9165),l=i(2009),d=i(3442),c=i(261),p=i(6668);class h{hostConnected(){}get deviceState(){return this._host.device?.state??p.g.UNKNOWN}get deviceTargetPlatform(){return this._host.device?.target_platform??""}get deviceCurrentAddress(){return this._host.device?.ip||this._host.device?.address||""}_openCommand(e,t,i){let a=this._host.commandDialog;a&&(a.configuration=e.configuration,a.name=e.friendly_name||e.name,a.open(t,i?{port:i}:void 0))}constructor(e){this.installMethodOpen=!1,this.onInstall=()=>{this._host.device&&(this.installMethodOpen=!0,this._host.requestUpdate())},this.onUpdate=()=>{let e=this._host.device;e&&this._openCommand(e,"install")},this.onInstallMethodClose=()=>{this.installMethodOpen=!1,this._host.requestUpdate()},this.onInstallMethodSelect=e=>{let t=this._host.device;if(this.installMethodOpen=!1,this._host.requestUpdate(),!t)return;let{method:i,port:a}=e.detail;"ota"===i?this._openCommand(t,"install",a??"OTA"):"server-serial"===i?this._openCommand(t,"install",a):"web-serial"===i?this._host.firmwareDialog?.installWebSerial(t):"web-download"===i?this._host.firmwareDialog?.installWebDownload(t):"binary-download"===i&&this._host.firmwareDialog?.installBinaryDownload(t)},this._host=e,e.addController(this)}}var u=i(1556),m=i(3140),v=i(9460),g=i(3632),f=i(1529),_=i(2063),b=i(1093),y=i(6049),w=i(9317),$=i(9789),x=i(4125);let k=/^(\s+)([a-z0-9_]+_action):/,z=/^(\s+)(on_[a-zA-Z_]+):/,C=/^ *[A-Za-z_][\w.]*:\s*(#.*)?$/;function E(e){let t=e.split("\n"),i=(0,x.MT)(e),a=[];for(let e=0;e<t.length;e++){let o=t[e].match(z);if(!o)continue;let r=o[1].length,s=o[2],n=e+1,l=S(t,e,r),d=(0,x.lr)(i,n);if(d&&void 0===d.parentKey&&"esphome"===d.key){let e={parentKey:"esphome",eventKey:s},i=T(t,n,l);i?i.forEach((t,i)=>{a.push({...e,key:`automation:device_on:${s}:${i}`,displayLabel:`esphome → ${s} #${i+1}`,fromLine:t.fromLine,toLine:t.toLine})}):a.push({...e,key:`automation:device_on:${s}`,displayLabel:`esphome → ${s}`,fromLine:n,toLine:l});continue}let c=d?q(t,i,d,e,r):null;if(d&&c){let{componentId:e,displayName:i,parentComponentId:o}=c,r=i||e,p={id:e,name:i,parentKey:d.parentKey??d.key,eventKey:s,...void 0!==o?{parentComponentId:o}:{}},h=T(t,n,l);h?h.forEach((t,i)=>{a.push({...p,key:`automation:component_on:${e}:${s}:${i}`,displayLabel:`${r} → ${s} #${i+1}`,fromLine:t.fromLine,toLine:t.toLine})}):a.push({...p,key:`automation:component_on:${e}:${s}`,displayLabel:`${r} → ${s}`,fromLine:n,toLine:l});continue}a.push({key:`automation:unscoped:${s}:${n}`,displayLabel:s,fromLine:n,toLine:l,eventKey:s})}for(let e=0;e<t.length;e++){let o=t[e].match(k);if(!o)continue;let r=o[1].length,s=o[2];if(s.startsWith("on_"))continue;let n=e+1,l=(0,x.lr)(i,n),d=l&&q(t,i,l,e,r,!1);if(!l||!d)continue;let c=d.componentId;if(!c)continue;let p=l.name||c;a.push({key:`automation:component_action:${c}:${s}`,displayLabel:`${p} → ${s}`,fromLine:n,toLine:S(t,e,r),id:c,name:l.name,parentKey:l.parentKey??l.key,actionField:s})}for(let e of["script","interval"]){let i=A(t,e);i&&L(t,i.fromLine,i.toLine).forEach((i,o)=>{let r="script"===e?R(t,i.fromLine,"id"):null,s="script"===e&&r?`automation:script:${r}`:`automation:interval:${o}`,n="script"===e&&r?`script: ${r}`:`interval #${o+1}`,l={};if("interval"===e){let e=R(t,i.fromLine,"interval");e&&(l.every=e)}a.push({key:s,displayLabel:n,fromLine:i.fromLine,toLine:i.toLine,id:"script"===e&&r?r:void 0,parentKey:e,meta:Object.keys(l).length>0?l:void 0})})}let o=A(t,"api");if(o){let e=function(e,t,i,a){let o=null;for(let a=t;a<i&&a<e.length;a++){let t=e[a];if(""===t.trim())continue;let i=(t.match(/^(\s+)/)??["",""])[1].length;if(i>0){o=i;break}}if(null===o)return null;let r=RegExp(`^\\s{${o}}${a}\\s*:`);for(let a=t;a<i&&a<e.length;a++)if(r.test(e[a]))return{fromLine:a+1,toLine:S(e,a,o)};return null}(t,o.fromLine,o.toLine,"actions");if(e)for(let i of L(t,e.fromLine,e.toLine)){let e=R(t,i.fromLine,"action")??R(t,i.fromLine,"service");e&&a.push({key:`automation:api_action:${e}`,displayLabel:`API: ${e}`,fromLine:i.fromLine,toLine:i.toLine,id:e,parentKey:"api"})}}return a}function q(e,t,i,a,o,r=!0){let s=(0,x.IO)(e[i.fromLine-1]??"");if(o===s)return{componentId:(0,x.MX)(t,i),displayName:i.name??void 0};if(r&&o>s){let o=function(e,t,i){let a,o=-1;for(let a=t-1;a>=0;a--){if((0,$.BJ)(e[a]))continue;let t=(0,x.p0)(e[a]);if(t<i)return null;if(t===i){if(!C.test(e[a]))return null;o=a;break}}if(-1===o)return null;let r=null,s=-1;for(let t=o+1;t<e.length;t++){if((0,$.BJ)(e[t]))continue;let o=(0,x.p0)(e[t]);if(o<=i)break;-1===s&&(s=o),o!==s||x.X$.test(e[t])||(r=(0,x.KJ)(e[t],"id")??r,a=(0,x.KJ)(e[t],"name")??a)}return r?{id:r,name:a}:null}(e,a,s);if(o)return{componentId:o.id,displayName:o.name,parentComponentId:(0,x.MX)(t,i)}}return null}function S(e,t,i){for(let a=t+1;a<e.length;a++)if((0,$.PM)(e[a],i))return a;return e.length}function A(e,t){for(let i=0;i<e.length;i++)if(e[i].match(RegExp(`^${t}\\s*:`)))return{fromLine:i+1,toLine:S(e,i,0)};return null}function L(e,t,i){let a=[],o=null,r=null;for(let s=t;s<i&&s<e.length;s++){let t=e[s];if(""===t.trim())continue;let i=t.match(/^(\s*)-\s/);if(!i)continue;let n=i[1].length;null===o&&(o=n),n>o||(r&&a.push({fromLine:r.fromLine,toLine:s}),r={fromLine:s+1})}return r&&a.push({fromLine:r.fromLine,toLine:i}),a}let M="then|seconds|minutes|hours|days_of_week|days_of_month|months|at|cron",P=RegExp(`^(\\s*)(?:${M})\\s*:`),F=RegExp(`^\\s*-\\s+(?:${M})\\s*:`);function T(e,t,i){let a=L(e,t,i);return 0===a.length?null:a.every(t=>(function(e,t){let i=e[t.fromLine-1]??"";if(F.test(i))return!0;let a=(0,x.IO)(i);for(let i=t.fromLine;i<t.toLine&&i<e.length;i++){let t=e[i].match(P);if(t&&t[1].length===a)return!0}return!1})(e,t))?a:null}function R(e,t,i){let a=e[t-1],o=`${i}:\\s*["']?([^"'\\s]+)["']?`,r=a.match(RegExp(`^\\s*-\\s*${o}`));if(r)return r[1];let s=a.match(/^(\s*)-/)?.[1].length??0,n=RegExp(`^\\s+${o}`);for(let i=t;i<e.length;i++){let t=e[i];if(""===t.trim())continue;if((0,x.p0)(t)<=s)break;let a=t.match(n);if(a)return a[1]}return null}let D=new Set(["esp32","esp8266","rp2040","bk72xx","rtl87xx","ln882x","nrf52","host","esphome","logger","api","ota","wifi","ethernet","mqtt","mdns","network","web_server","captive_portal","improv_serial","safe_mode","debug","preferences","update","external_components","packages","substitutions","dashboard_import","globals"]),O=new Set(["script","interval"]);function I(e){let t=[],i=[],a=[];for(let o of e)D.has(o.key)?t.push(o):O.has(o.key)?a.push(o):i.push(o);return{core:t,components:i,automations:a}}function j(e,t){let i=E(e).filter(e=>!e.key.startsWith("automation:unscoped:")),a=(0,x.lr)(i,t);if(a)return a;let o=(0,x.MT)(e);return(0,x.lr)(o,t)}function N(e){return e.platform?e.platform.startsWith(`${e.key}.`)?e.platform:`${e.key}.${e.platform}`:e.key}function B(e,t,i){if(!e||!t)return;let a=(0,x.MT)(e).filter(e=>N(e)===t);if(0!==a.length)return 1===a.length||void 0===i?a[0].fromLine:a.reduce((e,t)=>Math.abs(t.fromLine-i)<Math.abs(e.fromLine-i)?t:e).fromLine}function K(e,t,i){if(void 0===t||!Number.isInteger(t)||t<1||null!==i||!e)return null;let a=j(e,t);return a?{sectionKey:N(a),range:{fromLine:t,toLine:t}}:null}var Z=i(1269);let U=/line\s+(\d+)\s*,\s*column\s+(\d+)/i,H=/line\s+(\d+)/i,V=(0,l.AH)`
  :host {
    display: block;
  }

  .page {
    box-sizing: border-box;
    padding: 0;
    min-height: calc(100vh - var(--esphome-header-height));
  }

  .layout-grid {
    display: grid;
    grid-template-columns: minmax(230px, 1fr) minmax(0, 5fr);
    gap: 1px;
    background: var(--wa-color-surface-border);
    height: calc(100vh - var(--esphome-header-height) - var(--esphome-footer-height));
    transition: grid-template-columns 0.25s ease;
    --navigator-border-radius: 0;
    --navigator-border: none;
    --navigator-shadow: none;
    --editor-border-radius: 0;
    --editor-border: none;
    --editor-shadow: none;
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

  /* Box + hover come from .ghost-icon-btn (shared.ts); this button uses
     a square 4px pad, a trailing margin, and a smaller (14px) icon. */
  .back-btn {
    padding: 4px;
    border-radius: var(--wa-border-radius-m);
    margin-right: var(--wa-space-xs);
  }

  .back-btn wa-icon {
    font-size: 14px;
  }

  .header-start-group {
    display: inline-flex;
    align-items: center;
    gap: 2px;
  }

  /* Box + hover + padding all come from .ghost-icon-btn (shared.ts);
     only the icon size is per-site. */
  .nav-toggle-btn wa-icon {
    font-size: 18px;
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
`;i(2202),i(9968);let G="esphome-editor-split-ratio",W=e=>Math.min(.75,Math.max(.25,e)),Y=e=>{try{localStorage.setItem(G,String(e))}catch{}},J=(0,l.AH)`
  :host {
    display: contents;
  }

  .card {
    background: var(--wa-color-surface-default);
    border-radius: var(--editor-border-radius, var(--wa-border-radius-l));
    border: var(
      --editor-border,
      var(--wa-border-width-s) solid var(--wa-color-surface-border)
    );
    box-shadow: var(--editor-shadow, var(--wa-elevation-02));
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  :host([navcollapsed]) .card-header {
    padding-left: var(--wa-space-2xs);
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

  .editor-header-titlerow {
    display: flex;
    align-items: baseline;
    gap: var(--wa-space-xs);
    min-width: 0;
  }

  .editor-header-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
  }

  .editor-header-file {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-normal);
    color: var(--esphome-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
    /* Yield before the device name when the header is tight; the
       filename is the secondary half of the title row. */
    flex-shrink: 2;
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

  /* Box + hover + pressed + disabled come from .ghost-icon-btn
     (shared.ts); only the icon size is per-site here. */
  .diff-toggle wa-icon {
    font-size: 18px;
  }

  .layout-toggle {
    display: inline-flex;
    align-items: center;
    gap: 2px;
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
    --pane-divider-width: 9px;
  }

  .editor-layout--both {
    grid-template-columns: 1fr var(--pane-divider-width) 1fr;
  }

  .editor-layout.dragging {
    cursor: col-resize;
    user-select: none;
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
    align-self: stretch;
    position: relative;
    background: transparent;
    cursor: col-resize;
    touch-action: none;
  }

  .pane-divider::before {
    content: "";
    position: absolute;
    inset: 0 50%;
    width: 1px;
    transform: translateX(-50%);
    background: var(--wa-color-surface-border);
    transition:
      background 0.12s,
      width 0.12s;
  }

  .pane-divider:hover::before,
  .pane-divider:focus-visible::before,
  .pane-divider.dragging::before {
    background: var(--esphome-primary);
    width: 2px;
  }

  .pane-divider:focus-visible {
    /* Transparent outline keeps a ring in forced-colors mode. */
    outline: 2px solid transparent;
    box-shadow: var(--esphome-focus-ring-tight);
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

    /* Hug the always-present leading menu/back control to the edge on
       mobile, not the wide title indent of the pre-hamburger design. */
    .card-header {
      padding-left: var(--wa-space-2xs);
    }
  }
`;function Q(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}i(3238);class X extends l.WF{render(){if(this._darkMode?this.setAttribute("dark",""):this.removeAttribute("dark"),this.oldValue===this.newValue)return(0,l.qy)`<div class="empty">${this._localize("device.diff_no_changes")}</div>`;let e=function(e,t){let i=e.split("\n"),a=t.split("\n"),o=i.length,r=a.length,s=[];for(let e=0;e<=o;e++)s.push(new Uint32Array(r+1));for(let e=1;e<=o;e++)for(let t=1;t<=r;t++)s[e][t]=i[e-1]===a[t-1]?s[e-1][t-1]+1:Math.max(s[e-1][t],s[e][t-1]);let n=[],l=o,d=r;for(;l>0||d>0;)l>0&&d>0&&i[l-1]===a[d-1]?(n.push({type:"context",oldLine:l,newLine:d,content:i[l-1]}),l--,d--):d>0&&(0===l||s[l][d-1]>=s[l-1][d])?(n.push({type:"add",newLine:d,content:a[d-1]}),d--):(n.push({type:"remove",oldLine:l,content:i[l-1]}),l--);return n.reverse()}(this.oldValue,this.newValue);return(0,l.qy)`
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
    `}constructor(...e){super(...e),this._darkMode=!1,this._localize=e=>e,this.oldValue="",this.newValue=""}}X.styles=(0,l.AH)`
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
  `,Q([(0,s.Fg)({context:u.B6,subscribe:!0}),(0,d.wk)()],X.prototype,"_darkMode",void 0),Q([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],X.prototype,"_localize",void 0),Q([(0,d.MZ)()],X.prototype,"oldValue",void 0),Q([(0,d.MZ)()],X.prototype,"newValue",void 0),X=Q([(0,d.EM)("esphome-yaml-diff")],X),i(2975);var ee=i(8763),et=i(6910);let ei=(0,l.AH)`
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
`,ea="cog-outline",eo="memory",er="arrow-decision-outline";(0,b.C)({[ea]:n.mdiCogOutline,[eo]:n.mdiMemory,[er]:n.mdiArrowDecisionOutline}),i(4636),i(7473);var es=i(5660),en=i(8283);let el=(0,l.AH)`
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
`;var ed=i(6570);function ec(e){return e.name??e.id}function ep(e){return(0,ed.iZ)(e).domain}function eh(e,t){let i=e.parent_id?t.find(t=>t.id===e.parent_id):void 0;return i?`${e.component_id} \xb7 ${ec(i)}`:e.component_id}function eu(e){return!e.is_entity_container}function em(e,t){if(!t||!eu(t))return[];let i=ep(t.component_id);return e.filter(e=>!e.is_device_level&&(e.applies_to.includes(t.component_id)||e.applies_to.includes(i)))}function ev(){return{trigger_id:null,trigger_params:{},actions:[]}}function eg(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a,...o]=t;if(0===o.length){if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}let r=e[a]&&"object"==typeof e[a]&&!Array.isArray(e[a])?e[a]:{};return{...e,[a]:eg(r,o,i)}}function ef(e,t,i){if(t<0||t>=e.length)return e;let a=e.slice();return a[t]=i,a}function e_(e,t){if(t<0||t>=e.length)return e;let i=e.slice();return i.splice(t,1),i}function eb(e,t,i){if(t<0||i<0||t>=e.length||i>=e.length||t===i)return e;let a=e.slice();return[a[t],a[i]]=[a[i],a[t]],a}function ey(e){return/^\d+$/.test(e)?Number(e):null}function ew(e){switch(e.kind){case"device_on":return void 0===e.index?`automation:device_on:${e.trigger}`:`automation:device_on:${e.trigger}:${e.index}`;case"component_on":return void 0===e.index?`automation:component_on:${e.component_id}:${e.trigger}`:`automation:component_on:${e.component_id}:${e.trigger}:${e.index}`;case"component_action":return`automation:component_action:${e.component_id}:${e.field}`;case"script":return`automation:script:${e.id}`;case"interval":return`automation:interval:${e.index}`;case"light_effect":return`automation:light_effect:${e.component_id}:${e.index}`;case"api_action":return`automation:api_action:${e.action_name}`}}function e$(e,t){let i=e.split("\n"),a=t.fromLine-1,o=Math.max(0,t.toLine-t.fromLine+1),r=t.replacement.endsWith("\n")?t.replacement.slice(0,-1):t.replacement,s=""===r?[]:r.split("\n");return[...i.slice(0,a),...s,...i.slice(a+o)].join("\n")}function ex(e){if(!e.startsWith("automation:"))return null;let t=e.split(":");switch(t[1]){case"device_on":if(!t[2])return null;if(3===t.length)return{kind:"device_on",trigger:t[2]};if(4===t.length){let e=ey(t[3]);return null===e?null:{kind:"device_on",trigger:t[2],index:e}}return null;case"component_on":if(!t[2]||!t[3])return null;if(4===t.length)return{kind:"component_on",component_id:t[2],trigger:t[3]};if(5===t.length){let e=ey(t[4]);return null===e?null:{kind:"component_on",component_id:t[2],trigger:t[3],index:e}}return null;case"component_action":return 4===t.length&&t[2]&&t[3]?{kind:"component_action",component_id:t[2],field:t[3]}:null;case"script":return t[2]?{kind:"script",id:t[2]}:null;case"interval":{let e=Number(t[2]);return Number.isFinite(e)?{kind:"interval",index:e}:null}case"light_effect":{let e=Number(t[3]);return t[2]&&Number.isFinite(e)?{kind:"light_effect",component_id:t[2],index:e}:null}case"api_action":return t[2]?{kind:"api_action",action_name:t[2]}:null;default:return null}}i(986),i(1604),i(6117),i(9288);let ek=(0,l.AH)`
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
  .error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }
  .component-list {
    display: flex;
    flex-direction: column;
    gap: 2px;
    max-height: 280px;
    overflow-y: auto;
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    padding: var(--wa-space-2xs);
  }
  /* The role=group wrapper carries the same column gap as the list, with a
     left rule + indented rows so a group's members read as nested under its
     header and a following loose row (e.g. wifi) is clearly outside it. */
  .component-group-wrap {
    display: flex;
    flex-direction: column;
    gap: 2px;
    border-left: 2px solid var(--wa-color-surface-border);
    margin-left: var(--wa-space-2xs);
    padding-left: var(--wa-space-2xs);
  }
  .component-group-wrap .component-choice {
    padding-left: var(--wa-space-m);
  }
  .component-group {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: var(--wa-space-s) var(--wa-space-2xs) var(--wa-space-2xs);
  }
  /* Trim the leading gap only when a group is the very first row (each
     group now sits in its own wrap, so :first-child on the header would
     match every group). */
  .component-group-wrap:first-child .component-group {
    margin-top: var(--wa-space-2xs);
  }
  .component-group-id {
    text-transform: none;
    letter-spacing: normal;
    font-weight: var(--wa-font-weight-normal);
  }
  .component-choice {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
    padding: var(--wa-space-xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    transition: background 0.12s;
  }
  .component-choice:hover,
  .component-choice:focus-visible {
    background: var(--wa-color-surface-lowered);
    outline: none;
  }
  .component-choice--selected {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 14%,
      var(--wa-color-surface-default)
    );
  }
  .component-choice[aria-disabled="true"] {
    opacity: 0.55;
    cursor: default;
    pointer-events: none;
  }
  .component-choice-name {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .component-domain {
    flex: 0 0 auto;
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-default);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
  }
`;function ez(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}let eC={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1};class eE extends l.WF{render(){let{plan:e,order:t}=this._plan();return 0===t.length?(0,l.qy)`<p class="error" role="status">
        ${this._localize("device.automation_target_no_components")}
      </p>`:(0,l.qy)`<div class="field">
      <label class="field-label" id="component-target-label">
        ${this._localize("device.automation_wizard_pick_component")}
      </label>
      <div
        class="component-list"
        role="radiogroup"
        aria-labelledby="component-target-label"
        @keydown=${e=>this._onKeydown(e,t)}
      >
        ${e.map(e=>{if(!("header"in e))return this._renderChoice(e,t);let i=`component-group-${e.header.id}`;return(0,l.qy)`<div
            class="component-group-wrap"
            role="group"
            aria-labelledby=${i}
          >
            <p class="component-group" id=${i}>
              ${ec(e.header)}
              <span class="component-group-id">(${e.header.component_id})</span>
            </p>
            ${e.subs.map(e=>this._renderChoice(e,t))}
          </div>`})}
      </div>
    </div>`}_plan(){let e=new Set(this.devices.filter(e=>e.is_entity_container).map(e=>e.id)),t=new Map;for(let i of this.devices){if(!i.parent_id||!e.has(i.parent_id))continue;let a=t.get(i.parent_id)??[];a.push(i),t.set(i.parent_id,a)}let i=[],a=[];for(let o of this.devices)if(o.is_entity_container){let e=t.get(o.id)??[];if(0===e.length)continue;i.push({header:o,subs:e}),a.push(...e.map(e=>e.id))}else o.parent_id&&e.has(o.parent_id)||(i.push(o),a.push(o.id));return{plan:i,order:a}}_renderChoice(e,t){let i=e.id===this.value,a=i||!t.includes(this.value)&&t[0]===e.id;return(0,l.qy)`<div
      class="component-choice ${i?"component-choice--selected":""}"
      role="radio"
      aria-checked=${i?"true":"false"}
      aria-disabled=${this.disabled?"true":"false"}
      data-id=${e.id}
      tabindex=${a?"0":"-1"}
      @click=${()=>this._select(e.id)}
    >
      <span class="component-choice-name">${ec(e)}</span>
      <span class="component-domain">${e.component_id}</span>
    </div>`}_onKeydown(e,t){if(this.disabled||0===t.length)return;let i=e.target?.closest(".component-choice"),a=i?.dataset.id??null;if("Enter"===e.key||" "===e.key){a&&(e.preventDefault(),this._select(a));return}let o=eC[e.key]??0;if(0===o)return;e.preventDefault();let r=a?t.indexOf(a):-1,s=t[(r+o+t.length)%t.length];this._select(s),this.updateComplete.then(()=>{let e=this.shadowRoot?.querySelector(`.component-choice[data-id="${s}"]`);e?.focus()})}_select(e){this.disabled||this.dispatchEvent(new CustomEvent("component-change",{detail:{componentId:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.devices=[],this.value="",this.disabled=!1}}function eq(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}eE.styles=[m.G,ek],ez([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],eE.prototype,"_localize",void 0),ez([(0,d.MZ)({attribute:!1})],eE.prototype,"devices",void 0),ez([(0,d.MZ)()],eE.prototype,"value",void 0),ez([(0,d.MZ)({type:Boolean})],eE.prototype,"disabled",void 0),eE=ez([(0,d.EM)("esphome-component-target-picker")],eE);class eS extends l.WF{open(e){this._prefilled=void 0!==e,this._kind=e?.kind??"device_on",this._componentId=e?.kind==="component_on"?e.componentId:"",this._prefillComponentId=this._componentId,this._triggerId=null,this._intervalValue="",this._intervalUnit="s",this._error="",this._open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration){this._loading=!0;try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml);let e=this._prefillContainer();e&&(this._componentId=this._available.devices.find(t=>t.parent_id===e.id)?.id??"")}catch(e){this._error=(0,en.u)(e)}finally{this._loading=!1}}}_prefillContainer(){if(!this._prefilled||"component_on"!==this._kind||!this._prefillComponentId)return;let e=this._available?.devices.find(e=>e.id===this._prefillComponentId);return e?.is_entity_container?e:void 0}render(){let e=this.boardName?this._localize("device.add_automation_dialog_title",{name:this.boardName}):this._localize("device.add_automation");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._onRequestClose}
    >
      ${this._loading&&!this._available?(0,l.qy)`<div style="text-align: center; padding: 32px;">
            <wa-spinner></wa-spinner>
          </div>`:this._renderForm()}
    </esphome-base-dialog>`}_renderForm(){let e=this._filteredTriggers(),t="interval"===this._kind,i=!this._prefilled,a=this._prefillContainer(),o="component_on"===this._kind&&(!this._prefilled||!!a);return(0,l.qy)`
      <p class="intro">
        ${(0,et.G)(this._localize("device.automation_header_description"))}
      </p>
      ${i?(0,l.qy)`<div class="field">
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
      ${o?this._renderComponentRow(a):l.s6}
      ${"interval"===this._kind?this._renderIntervalRow():l.s6}
      ${!t?this._renderTriggerRow(e):l.s6}
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
    `}_renderComponentRow(e){var t;let i=(t=this._available?.devices??[],e?t.filter(t=>t.id===e.id||t.parent_id===e.id):t);return(0,l.qy)`<esphome-component-target-picker
      .devices=${i}
      .value=${this._componentId}
      ?disabled=${this._saving}
      @component-change=${e=>this._onComponentChange(e.detail.componentId)}
    ></esphome-component-target-picker>`}_renderIntervalRow(){return(0,l.qy)`<div class="field">
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
      ${t?.description?(0,l.qy)`<p class="field-desc">${(0,et.G)(t.description)}</p>`:l.s6}
    </div>`}_filteredTriggers(){let e=this._available?.triggers??[];if("device_on"===this._kind){let t=this._existingDeviceTriggers();return e.filter(e=>e.is_device_level&&(!t.has(e.id)||e.supports_list))}if("component_on"===this._kind){let t=this._available?.devices.find(e=>e.id===this._componentId),i=this._existingComponentTriggers(this._componentId);return em(e,t).filter(e=>!i.has(this._bareTrigger(e.id))||e.supports_list)}return[]}_existingDeviceTriggers(){let e=new Set;for(let t of E(this.yaml))"esphome"===t.parentKey&&t.eventKey&&e.add(t.eventKey);return e}_existingComponentTriggers(e){let t=new Set;for(let i of E(this.yaml))i.id===e&&i.eventKey&&t.add(i.eventKey);return t}_bareTrigger(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_onKindChange(e){if(this._kind=e,this._triggerId=null,"component_on"===e){let e=this._available?.devices??[];this._componentId=e.find(eu)?.id??""}else this._componentId=""}_onComponentChange(e){this._componentId=e,this._triggerId=null}_canContinue(){return"interval"===this._kind?""!==this._intervalValue.trim():!!this._triggerId&&("component_on"!==this._kind||!!this._componentId)}_buildLocation(){if("device_on"===this._kind){let e=this._available?.triggers.find(e=>e.id===this._triggerId);if(e?.supports_list){let e=E(this.yaml).filter(e=>"esphome"===e.parentKey&&e.eventKey===this._triggerId).length;return{kind:"device_on",trigger:this._triggerId,index:e}}return{kind:"device_on",trigger:this._triggerId}}if("component_on"===this._kind){let e=this._triggerId.indexOf("."),t=e>=0?this._triggerId.slice(e+1):this._triggerId,i=this._available?.triggers.find(e=>e.id===this._triggerId);if(i?.supports_list){let e=E(this.yaml).filter(e=>e.id===this._componentId&&e.eventKey===t).length;return{kind:"component_on",component_id:this._componentId,trigger:t,index:e}}return{kind:"component_on",component_id:this._componentId,trigger:t}}return{kind:"interval",index:E(this.yaml).filter(e=>"interval"===e.parentKey).length}}_catalogTriggerId(e){return"interval"===e.kind?null:this._triggerId}_dispatchAdded(e,t){let i=e$(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:ew(e)},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._kind="device_on",this._componentId="",this._prefillComponentId="",this._triggerId=null,this._prefilled=!1,this._intervalValue="",this._intervalUnit="s",this._available=null,this._loading=!0,this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e=this._buildLocation(),t={trigger_id:this._catalogTriggerId(e),trigger_params:"interval"===this._kind?{interval:`${this._intervalValue.trim()}${this._intervalUnit}`}:{},actions:[]},{yaml_diff:i}=await this._api.upsertAutomation(this.configuration,t,e,this.yaml);this._dispatchAdded(e,i),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}eS.styles=[m.G,es.z,el],eq([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],eS.prototype,"_localize",void 0),eq([(0,s.Fg)({context:u.Ie})],eS.prototype,"_api",void 0),eq([(0,d.MZ)()],eS.prototype,"boardName",void 0),eq([(0,d.MZ)()],eS.prototype,"configuration",void 0),eq([(0,d.MZ)()],eS.prototype,"yaml",void 0),eq([(0,d.MZ)({attribute:!1})],eS.prototype,"board",void 0),eq([(0,d.wk)()],eS.prototype,"_open",void 0),eq([(0,d.wk)()],eS.prototype,"_kind",void 0),eq([(0,d.wk)()],eS.prototype,"_componentId",void 0),eq([(0,d.wk)()],eS.prototype,"_prefillComponentId",void 0),eq([(0,d.wk)()],eS.prototype,"_triggerId",void 0),eq([(0,d.wk)()],eS.prototype,"_prefilled",void 0),eq([(0,d.wk)()],eS.prototype,"_intervalValue",void 0),eq([(0,d.wk)()],eS.prototype,"_intervalUnit",void 0),eq([(0,d.wk)()],eS.prototype,"_available",void 0),eq([(0,d.wk)()],eS.prototype,"_loading",void 0),eq([(0,d.wk)()],eS.prototype,"_saving",void 0),eq([(0,d.wk)()],eS.prototype,"_error",void 0),eS=eq([(0,d.EM)("esphome-add-automation-dialog")],eS);var eA=i(6848),eL=i(6016),eM=i(8851),eP=((r={}).SENSOR="sensor",r.BINARY_SENSOR="binary_sensor",r.SWITCH="switch",r.LIGHT="light",r.FAN="fan",r.COVER="cover",r.CLIMATE="climate",r.BUTTON="button",r.NUMBER="number",r.SELECT="select",r.TEXT="text",r.TEXT_SENSOR="text_sensor",r.LOCK="lock",r.VALVE="valve",r.MEDIA_PLAYER="media_player",r.SPEAKER="speaker",r.MICROPHONE="microphone",r.CAMERA="camera",r.DISPLAY="display",r.TOUCHSCREEN="touchscreen",r.OUTPUT="output",r.DATETIME="datetime",r.EVENT="event",r.UPDATE="update",r.ALARM="alarm_control_panel",r.CORE="core",r.BUS="bus",r.AUTOMATION="automation",r.OTA="ota",r.TIME="time",r.AUDIO_ADC="audio_adc",r.AUDIO_DAC="audio_dac",r.CANBUS="canbus",r.INFRARED="infrared",r.MEDIA_SOURCE="media_source",r.ONE_WIRE="one_wire",r.PACKET_TRANSPORT="packet_transport",r.STEPPER="stepper",r.WATER_HEATER="water_heater",r.MISC="misc",r.FEATURED="featured",r);let eF=["core","ota","update"];var eT=i(4117);async function eR(e,t){if(e._submitting)return;let i=e._selected;e._submitError="";let a=++e._depNavSeq,o=null;try{o=await (0,eT.Sn)(e._api,t,e.platform||void 0,e.board?.id??void 0)}catch{o=null}if(a===e._depNavSeq){if(i&&(e._returnTo=i,e._depDomain=t),o){e._selected=o;return}e._selected=null,await e.updateComplete,a===e._depNavSeq&&e._catalog?.filterByDomain(t)}}async function eD(e,t,i){let a=++e._selectionSeq,o=i??e.board?.id??void 0;try{let i=await (0,eT.Sn)(e._api,t,e.platform||void 0,o);if(a!==e._selectionSeq)return{kind:"stale"};if(!i)return{kind:"error",message:e._localize("device.add_component_error")};return{kind:"ok",entry:i}}catch(t){if(a!==e._selectionSeq)return{kind:"stale"};return{kind:"error",message:t instanceof Error?t.message:e._localize("device.add_component_error")}}}let eO=(0,l.AH)`
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
`;var eI=i(4008);class ej{hostConnected(){this._unsubscribe=(0,eT.Ej)(()=>{this._host.requestUpdate()})}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}resolve(e){return(0,eT.CQ)(e,this._getPlatform())?.name??e}kickoff(e){let t=this._getApi();if(!t)return;let i=this._getPlatform();for(let a of e)void 0===(0,eT.CQ)(a,i)&&(0,eT.Sn)(t,a,i).catch(()=>{})}constructor(e,t,i){this._host=e,this._getApi=t,this._getPlatform=i,e.addController(this)}}var eN=i(5957),eB=i(8175),eK=i(271);let eZ=(0,l.AH)`
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
    padding: var(--esphome-button-padding);
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
`;var eU=i(1811);function eH(e,t){return t?e.find(e=>e.configuration===t)?.name??"":""}function eV(e){let t=e.key??(()=>""),i=new Map,a=new Map,o=new Set,r=0,s=()=>{for(let t of o)try{t()}catch(t){console.error(`${e.name} listener threw`,t)}};return{getCached:(...e)=>i.get(t(...e)),fetch(o,...n){let l,d=t(...n);if(i.has(d))return Promise.resolve(i.get(d));let c=a.get(d);if(c)return c;let p=r;try{l=e.fetch(o,...n)}catch(e){l=Promise.reject(e)}let h=l.then(e=>(p===r&&(i.set(d,e),a.delete(d),s()),e)).catch(t=>{if(p===r&&a.delete(d),void 0===e.fallback)throw t;let o=e.fallback(t);return p===r&&(i.set(d,o),s()),o});return a.set(d,h),h},update(e,...a){i.set(t(...a),e),s()},subscribe:e=>(o.add(e),()=>{o.delete(e)}),reset(){r+=1,i.clear(),a.clear(),o.clear()}}}let eG=eV({name:"pin-registry-modes",fetch:e=>e.getPinRegistryModes(),fallback:e=>(console.warn("pin-registry-modes fetch failed; Mode flags unscoped",e),Object.create(null))});function eW(){return eG.getCached()}function eY(e){return eG.subscribe(e)}function eJ(e){return eG.fetch(e)}class eQ{hostConnected(){this._unsubscribe=this._binding.subscribe(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}hostUpdated(){if(this._kicked)return;let e=this._api();e&&(this._kicked=!0,this._binding.fetch(e))}get value(){return this._binding.getCached()}constructor(e,t,i){this._host=e,this._binding=t,this._api=i,this._kicked=!1,e.addController(this)}}var eX=i(5413);let e0=new Set(["name"]);function e1(e,t={}){return{requiredOnly:e.requiredOnly,showAdvanced:e.showAdvanced,presentComponents:e.presentComponents,targetPlatform:e.board?.esphome.platform??null,...t}}function e2(e,t){let i=t[e.key];if(e.type===eI.Hh.NESTED)return e.multi_value?i instanceof eM.ho||Array.isArray(i)&&i.length>0:(0,eB.Qd)(i)?(e.config_entries??[]).some(e=>e2(e,i)):void 0!==i;return void 0!==i}function e6(e,t,i){let a=[];for(let o of e)if((0,eN.VP)(o,t,i.presentComponents,i.targetPlatform)&&(!o.advanced||i.showAdvanced||e2(o,t))){if(o.type===eI.Hh.NESTED){if(!o.multi_value&&0===e6(o.config_entries??[],(0,eB.qY)(t[o.key]),i).length&&!e2(o,t))continue}else if(i.requiredOnly&&!o.required&&!e0.has(o.key))continue;a.push(o)}return a}var e3=i(2748),e4=i(9470),e5=i(9808);let e8={wifi:{ssid:"wifi_ssid",password:"wifi_password"}},e9=new Set(Object.values(e8).flatMap(e=>Object.values(e))),e7={"ota.esphome":{password:"ota_password"},api:{key:"encryption_key"},web_server:{password:"web_password"}};function te(e){return e.toLowerCase().replace(/[^a-z0-9_]+/g,"_").replace(/^_+|_+$/g,"")}function tt(e,t){return[`${e}__${t}`,`${e}_${t}`]}function ti(e,t,i,a){let o=e8[e]?.[t];if(o)return[o];let r=te(i);if(!r)return[];let s=e7[e]?.[t];if(s)return tt(r,s);if(a){let i=te(`${e}_${t}`);return i?tt(r,i):[]}return[]}function ta(e,t){for(let i of e.split("\n")){if(!i||" "===i[0]||"	"===i[0]||"#"===i[0])continue;let e=i.search(/:(\s|$)/);if(e<0||i.slice(0,e).trim()!==t)continue;let a=(0,e5.bw)(i.slice(e+1)).value.trim();if(a.length>=2&&a.startsWith('"')&&a.endsWith('"'))return(0,e4.rq)(a.slice(1,-1));return(0,e5.Ir)(a)}return null}let to=(0,l.AH)`
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

  /* Templatable field wrapper — column holding the literal/lambda tab
     strip (styled by literalLambdaToggleStyles) above the active
     body. */
  .templatable-field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
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
`,tr=(0,l.AH)`
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
  .field-description + wa-select,
  /* Secret-eligible fields wrap the control in .field-input-row, or replace
     it with the picker in secret mode — keep the same post-description gap. */
  .field-description + .field-input-row,
  .field-description + esphome-secret-picker {
    margin-top: 8px;
  }

  /* Stacks a string/password input above its inline secret picker (only
     emitted for secret-eligible fields with a literal value). Stacked, not
     side-by-side, so the input keeps full width — a side-by-side picker
     squeezes the input and its value collides with the password reveal eye. */
  .field-input-row {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--wa-space-2xs);
  }

  .field-input-row > input,
  .field-input-row > esphome-password-input {
    align-self: stretch;
    min-width: 0;
  }

  /* Hint shown below a string/password input when the value is a
     !secret reference — clarifies that the field points into
     secrets.yaml instead of holding a literal value. */
  .secret-note,
  .substitution-note {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .secret-note wa-icon,
  .substitution-note wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  /* The "defined elsewhere" marker is a quiet heads-up, not a positive
     resolve, so its braces icon and text stay muted. */
  .substitution-note--external {
    color: var(--wa-color-text-quiet);
  }

  .substitution-note--external wa-icon {
    color: var(--wa-color-text-quiet);
  }

  /* …except the warning glyph, which signals the unresolved reference. */
  .substitution-note--external wa-icon.substitution-warn {
    color: var(--wa-color-warning-fill-loud, #b8860b);
  }

  .secret-note code,
  .substitution-note code {
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
`,ts=(0,l.AH)`
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
`;function tn({isLambda:e,disabled:t,localize:i,onSwitch:a}){return(0,l.qy)`
    <div
      class="templatable-toggle"
      role="tablist"
      aria-label=${i("device.automation_literal")}
    >
      <button
        type="button"
        role="tab"
        class=${!e?"active":""}
        aria-selected=${!e}
        ?disabled=${t}
        @click=${()=>a(!1)}
      >
        ${i("device.automation_literal")}
      </button>
      <button
        type="button"
        role="tab"
        class=${e?"active":""}
        aria-selected=${e}
        ?disabled=${t}
        @click=${()=>a(!0)}
      >
        ${i("device.automation_lambda")}
      </button>
    </div>
  `}let tl=(0,l.AH)`
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
`,td=[m.G,es.z,tr,to,ts,tl];function tc(e,t){return t.disabled||e.locked}(0,b.C)({"alert-circle-outline":n.mdiAlertCircleOutline,"code-braces":n.mdiCodeBraces,"key-variant":n.mdiKeyVariant,"lock-outline":n.mdiLockOutline});let tp=e=>JSON.stringify(e),th=e=>{try{let t=JSON.parse(e);if(Array.isArray(t))return t.map(String)}catch{}return e?e.split("."):[]},tu=/^!secret\s+(\S+)\s*$/;function tm(e,t){if(e.translation_key){let i=e.translation_params||void 0,a=t(e.translation_key,i);if(a&&a!==e.translation_key)return a}return e.label?e.label:e.key.split("_").map(e=>e?e[0].toUpperCase()+e.slice(1):e).join(" ")}function tv(e,t){return tm(e,t.localize)}function tg(e,t){return e.help_link?(0,l.qy)`<a
    class="help-button"
    href=${e.help_link}
    target="_blank"
    rel="noreferrer"
    title=${t.localize("device.docs")}
  >
    <wa-icon library="mdi" name="open-in-new"></wa-icon>
  </a>`:l.s6}function tf(e,t,i={}){let{includeHelpLink:a=!0}=i;return(0,l.qy)`
    <label class="field-label">
      ${tv(e,t)}
      ${e.required?(0,l.qy)`<span class="required">*</span>`:l.s6}
      ${e.locked?(0,l.qy)`<wa-icon
            class="lock-icon"
            library="mdi"
            name="lock-outline"
            title=${t.localize("device.field_locked_by_board")}
          ></wa-icon>`:l.s6}
      ${a&&e.help_link?tg(e,t):l.s6}
    </label>
    ${e.description?(0,l.qy)`<p class="field-description">${(0,et.G)(e.description)}</p>`:l.s6}
  `}function t_(e,t){let i=t.errorAt(e);return(0,e3.O)(i?t.localize(i.code,i.params):void 0)}function tb(e,t,i,a,o=l.s6){return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)} ${a} ${o} ${t_(t,i)}
    </div>
  `}function ty(e,t,i,a){return(0,eB.k4)(a)?null:tw(e,t,i)}function tw(e,t,i){return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <p class="field-description">${i.localize("device.value_yaml_only")}</p>
      ${t_(t,i)}
    </div>
  `}function t$(e,t,i,a){var o,r,s,n,d,c,p,h;let u,m=a.getAt(i),v=ty(e,i,a,m);if(v)return v;let g=String(m??""),f=null!==a.errorAt(i),_=String(e.default_value??""),b=tc(e,a),y="password"===t||(o=a.sectionKey,r=e.key,e8[o]?.[r]!==void 0),w=g.match(tu)?.[1]??null,$=y&&null!==w,x=y?ti(a.sectionKey,e.key,a.deviceName??"","password"===t):[],k=y?(0,l.qy)`<esphome-secret-picker
        ?full=${$}
        .disabled=${b}
        .fieldLabel=${tv(e,a)}
        .selectedKey=${w??""}
        .value=${g}
        .deviceName=${a.deviceName??""}
        .recommendedKeys=${x}
        @secret-selected=${e=>a.emitChange(i,e.detail.value)}
      ></esphome-secret-picker>`:l.s6,z=e=>y?$?k:(0,l.qy)`<div class="field-input-row">${e}${k}</div>`:e,C=k===l.s6?(u=g.match(tu))?(0,l.qy)`<span class="secret-note">
    <wa-icon library="mdi" name="key-variant"></wa-icon>
    <span>${a.localize("device.value_from_secret")}</span>
    <code>${u[1]}</code>
  </span>`:l.s6:l.s6,E="password"===t?l.s6:function(e,t){if(!(0,eX.RB)(e))return l.s6;let i=(0,eX.rq)(e,t.substitutions);if((0,eX.RB)(i)){let e=t.localize("device.substitution_unresolved_hint");return(0,l.qy)`<span
      class="substitution-note substitution-note--external"
      role="note"
      aria-label=${e}
      title=${e}
    >
      <wa-icon library="mdi" name="code-braces"></wa-icon>
      <wa-icon
        class="substitution-warn"
        library="mdi"
        name="alert-circle-outline"
      ></wa-icon>
      <span>${t.localize("device.substitution_unresolved")}</span>
    </span>`}let a=t.localize("device.substitution_resolves_to");return(0,l.qy)`<span
    class="substitution-note"
    role="note"
    aria-label=${`${a}: ${i}`}
    title=${a}
  >
    <wa-icon library="mdi" name="code-braces"></wa-icon>
    <code>${i}</code>
  </span>`}(g,a);if(e.suggestions&&e.suggestions.length>0){let t,o,r;return s=e,n=i,d=g,c=f,p=b,h=a,t=d.toLowerCase(),o=String(s.default_value??""),r=s.type===eI.Hh.INTEGER||s.type===eI.Hh.FLOAT,(0,l.qy)`
    <div class="field" data-field-key=${tp(n)}>
      ${tf(s,h)}
      <wa-select
        class=${c?"invalid":""}
        ?disabled=${p}
        placeholder=${o}
        @change=${e=>h.emitChange(n,(e=>{if(!r||""===e)return e;let t=s.type===eI.Hh.INTEGER?parseInt(e,10):Number(e);return Number.isFinite(t)?t:e})(e.target.value))}
      >
        ${(s.suggestions??[]).map(e=>{let i=String(e);return(0,l.qy)`<wa-option value=${i} ?selected=${i.toLowerCase()===t}
            >${i}</wa-option
          >`})}
      </wa-select>
      ${t_(n,h)}
    </div>
  `}if("password"===t){let t=(0,l.qy)`<esphome-password-input
      .value=${g}
      .invalid=${f}
      .disabled=${b}
      .placeholder=${_}
      @password-input-change=${e=>a.emitChange(i,e.detail.value)}
    ></esphome-password-input>`;return(0,l.qy)`
      <div class="field" data-field-key=${tp(i)}>
        ${tf(e,a)} ${z(t)} ${C}
        ${t_(i,a)}
      </div>
    `}let q=(0,l.qy)`<input
    type=${t}
    class=${f?"invalid":""}
    .value=${g}
    ?disabled=${b}
    placeholder=${_}
    @input=${e=>a.emitChange(i,e.target.value)}
  />`;return(0,l.qy)`
    <div class="field" data-field-key=${tp(i)}>
      ${tf(e,a)} ${z(q)} ${C} ${E}
      ${t_(i,a)}
    </div>
  `}function tx(e,t,i,a={}){let o=i.scopeValues(t);return(a.includeAdvanced?e6(e.config_entries??[],o,e1(i,{showAdvanced:!0})):i.filterRenderable(e.config_entries??[],o)).map(e=>i.renderEntry(e,[...t,e.key]))}let tk=["focusin","pointerdown","input","change"];class tz{hostConnected(){for(let e of tk)this.host.addEventListener(e,this._onInteraction)}hostDisconnected(){for(let e of tk)this.host.removeEventListener(e,this._onInteraction)}constructor(e){this.host=e,this._onInteraction=e=>{var t,i,a;let o=e.composedPath().find(e=>e instanceof HTMLElement&&e.hasAttribute("data-field-key"));if(!o)return;let r=o.getAttribute("data-field-key")??"";if(!r.startsWith("["))return;let s=th(r);if(!s.length)return;let{emit:n,focusedKey:l}=(t=e.type,i=tp(s),a=this._focusedKey,"change"===t?{emit:i===a,focusedKey:a}:{emit:"focusin"===t||i!==a,focusedKey:i});this._focusedKey=l,n&&this.host.dispatchEvent(new CustomEvent("field-focus",{detail:{path:s},bubbles:!0,composed:!0}))},e.addController(this)}}let tC="field--highlight";class tE{maybeScroll(e){let t=this.host.focusFieldPath,i=t?.length?tp(t):void 0,a=e.has("focusFieldPath")||e.has("entries")||e.has("values"),{gate:o,scroll:r}=function(e,t,i){let{scrolledKey:a,lastFocusKey:o,tries:r}=e;t!==o&&(o=t,a=void 0,r=0);let s=!!t&&a!==t&&r<3&&i;return s&&r++,{gate:{scrolledKey:a,lastFocusKey:o,tries:r},scroll:s}}({scrolledKey:this._scrolledKey,lastFocusKey:this._lastFocusKey,tries:this._tries},i,a);this._scrolledKey=o.scrolledKey,this._lastFocusKey=o.lastFocusKey,this._tries=o.tries,r&&t?.length&&i&&this._scrollTo(t,i)}async _scrollTo(e,t){var i;let{host:a}=this;if(!a.shadowRoot)return;for(let t=1;t<e.length;t++)a.openNested(e.slice(0,t).join("."));for(let t of(i=this._gatingDecls(a.shadowRoot),i.filter(t=>t.prefix.length>0&&t.prefix.length<e.length&&t.prefix.every((t,i)=>t===e[i])).map(e=>e.key)))a.openNested(t);await a.updateComplete;let o=a.focusFieldPath;if(o&&tp(o)===t)for(let i=e.length;i>=1;i--){let o=this._find(a.shadowRoot,e.slice(0,i));if(!o)continue;o.scrollIntoView({block:"center"});let r=tp(e.slice(0,i)),s=Date.now();!window.matchMedia?.("(prefers-reduced-motion: reduce)").matches&&(r!==this._lastFlashKey||s-this._lastFlashAt>1e4)&&(this._lastFlashKey=r,this._lastFlashAt=s,o.classList.remove(tC),o.offsetWidth,o.classList.add(tC),o.addEventListener("animationend",()=>o.classList.remove(tC),{once:!0})),i===e.length&&(this._scrolledKey=t);return}}_gatingDecls(e){let t=[];for(let i of e.querySelectorAll("[data-reveal-for]")){let e=i.getAttribute("data-field-key");e&&t.push({prefix:th(i.getAttribute("data-reveal-for")??""),key:e})}return t}_find(e,t){for(let i of e.querySelectorAll("[data-field-key]")){let e=th(i.getAttribute("data-field-key")??"");if(e.length===t.length&&e.every((e,i)=>e===t[i]))return i}for(let i of e.querySelectorAll("*")){if(!i.localName.includes("-"))continue;let e=i.shadowRoot,a=e?this._find(e,t):null;if(a)return a}return null}constructor(e){this.host=e,this._lastFlashAt=0,this._tries=0}}i(1062),i(6135);var tq=i(9665);let tS=(0,l.AH)`
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
`;function tA(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({close:n.mdiClose,magnify:n.mdiMagnify,palette:n.mdiPalette});let tL=null;function tM(e){return e?e.startsWith("mdi:")?e.slice(4):e:""}class tP extends l.WF{connectedCallback(){super.connectedCallback(),document.addEventListener("click",this._onDocumentClick,!0)}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("click",this._onDocumentClick,!0)}willUpdate(e){e.has("_open")&&this._escape.set(this._open),e.has("value")&&!this._loaded&&tM(this.value)&&this._ensureCatalogLoaded()}async _toggle(){this.disabled||(this._open?this._close():await this._openPanel())}async _openPanel(){this._open=!0,this.setAttribute("open",""),await this._ensureCatalogLoaded(),await this.updateComplete,this._searchInput?.focus()}async _ensureCatalogLoaded(){this._loaded||(this._catalog=await (tL||(tL=(async()=>{let e=await Promise.resolve().then(i.bind(i,9165)),t=[];for(let[i,a]of Object.entries(e)){if(!i.startsWith("mdi")||"string"!=typeof a)continue;let e=i.slice(3);if(!e)continue;let o=e.replace(/^[A-Z]/,e=>e.toLowerCase()).replace(/([A-Z])/g,"-$1").replace(/_/g,"-").toLowerCase();t.push({name:o,path:a})}return t.sort((e,t)=>e.name.localeCompare(t.name)),t})().catch(e=>(console.error("[mdi-icon-picker] failed to load catalog:",e),tL=null,[])))),this._loaded=!0)}_close(){this._open=!1,this.removeAttribute("open"),this._query=""}_select(e){let t=`mdi:${e}`;this.value=t,this.dispatchEvent(new CustomEvent("change",{detail:{value:t},bubbles:!0,composed:!0})),this._close()}_clear(e){e.stopPropagation(),this.value="",this.dispatchEvent(new CustomEvent("change",{detail:{value:""},bubbles:!0,composed:!0}))}_onSearchInput(e){this._query=e.target.value}_renderTriggerIcon(){let e=tM(this.value);if(!e)return(0,l.qy)`<span class="trigger-icon trigger-icon--empty">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${n.mdiPalette}></path>
        </svg>
      </span>`;let t=this._catalog.find(t=>t.name===e);return t?(0,l.qy)`<span class="trigger-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${t.path}></path>
        </svg>
      </span>`:(0,l.qy)`<span class="trigger-icon">
      <wa-icon library="mdi" name=${e} style="font-size: 16px;"></wa-icon>
    </span>`}_renderPanel(){if(!this._loaded)return(0,l.qy)`<div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="loading">Loading icons…</div>
      </div>`;let e=function(e,t){if(!t)return e.slice(0,400);let i=t.trim().toLowerCase().replace(/\s+/g,"-");if(!i)return e.slice(0,400);let a=[],o=[],r=[];for(let t of e)if(t.name===i?a.push(t):t.name.startsWith(i)?o.push(t):t.name.includes(i)&&r.push(t),a.length+o.length+r.length>=800)break;return[...a,...o,...r].slice(0,400)}(this._catalog,this._query),t=tM(this.value);return(0,l.qy)`
      <div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="search">
          <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d=${n.mdiMagnify}></path>
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
    `}render(){let e=tM(this.value),t=`trigger${this.invalid?" invalid":""}`;return(0,l.qy)`
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
                <path fill="currentColor" d=${n.mdiClose}></path>
              </svg>
            </span>`:l.s6}
        <svg class="trigger-chevron" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M7,10L12,15L17,10H7Z"></path>
        </svg>
      </button>
      ${this._open?this._renderPanel():l.s6}
    `}constructor(...e){super(...e),this.value="",this.placeholder="Choose an icon…",this.invalid=!1,this.disabled=!1,this._open=!1,this._catalog=[],this._query="",this._loaded=!1,this._escape=new tq.u(this,e=>{e.stopPropagation(),this._close()},{target:document}),this._onDocumentClick=e=>{!this._open||e.composedPath().includes(this)||this._close()}}}tP.styles=[es.z,tS],tA([(0,d.MZ)()],tP.prototype,"value",void 0),tA([(0,d.MZ)()],tP.prototype,"placeholder",void 0),tA([(0,d.MZ)({type:Boolean})],tP.prototype,"invalid",void 0),tA([(0,d.MZ)({type:Boolean})],tP.prototype,"disabled",void 0),tA([(0,d.wk)()],tP.prototype,"_open",void 0),tA([(0,d.wk)()],tP.prototype,"_catalog",void 0),tA([(0,d.wk)()],tP.prototype,"_query",void 0),tA([(0,d.wk)()],tP.prototype,"_loaded",void 0),tA([(0,d.P)(".search-input")],tP.prototype,"_searchInput",void 0),tP=tA([(0,d.EM)("esphome-mdi-icon-picker")],tP);let tF="__esphome_add_new__";var tT=i(410);let tR={INPUT:{input:!0},OUTPUT:{output:!0},INPUT_PULLUP:{input:!0,pullup:!0},OUTPUT_OPEN_DRAIN:{output:!0,open_drain:!0},INPUT_PULLDOWN_16:{input:!0,pulldown:!0},INPUT_PULLDOWN:{input:!0,pulldown:!0},INPUT_OUTPUT_OPEN_DRAIN:{input:!0,output:!0,open_drain:!0}};function tD(e){let t=tR[e.toUpperCase()];return t?{...t}:null}let tO=new WeakMap;function tI(e,t,i){let a=i.getAt(t);if(!e.multi_value&&("string"==typeof a||"number"==typeof a||"boolean"==typeof a))return(0,l.qy)`
      <div class="field" data-field-key=${tp(t)}>
        ${tf(e,i)}
        <p class="field-description">
          ${i.localize("device.value_set_in_yaml",{value:String(a)})}
        </p>
        ${t_(t,i)}
      </div>
    `;let o=t.join(".");(0,eM.$z)(a)&&i.seedNestedOpen(o);let r=i.nestedOpenSections.has(o),s=i.requiredOnly?!r:r,n=null!=e.platform_type&&!e.required,d=n&&(0,eM.$z)(i.getAt(t)),c=tv(e,i),p=i.localize("device.enable_entity",{name:c});return(0,l.qy)`
    <div class="nested-group" data-field-key=${tp(t)}>
      <div class="nested-header">
        ${n?(0,l.qy)`<wa-switch
              class="nested-enable"
              .checked=${d}
              ?disabled=${tc(e,i)}
              aria-label=${p}
              title=${p}
              @change=${e=>(function(e,t,i,a,o,r){let s,n=((s=tO.get(r.stashOwner))||(s=new Map,tO.set(r.stashOwner,s)),s);if(a){let a=n.get(t);a&&(0,eM.$z)(a)?(n.delete(t),r.emitChange(e,a)):r.emitChange([...e,"name"],o),i||r.toggleNested(t)}else{let a=r.getAt(e);(0,eB.Qd)(a)&&(0,eM.$z)(a)&&n.set(t,a),r.emitChange(e,void 0),i&&r.toggleNested(t)}})(t,o,s,e.target.checked,c,i)}
            ></wa-switch>`:l.s6}
        <button
          type="button"
          class="nested-toggle"
          aria-expanded=${s}
          @click=${()=>i.toggleNested(o)}
        >
          <wa-icon library="mdi" name=${s?"chevron-up":"chevron-down"}></wa-icon>
          <span class="nested-title">${c}</span>
          ${e.platform_type?(0,l.qy)`<span class="nested-platform">${e.platform_type}</span>`:l.s6}
        </button>
        ${tg(e,i)}
      </div>
      ${e.description?(0,l.qy)`<p class="nested-desc">${(0,et.G)(e.description)}</p>`:l.s6}
      ${s?(0,l.qy)`<div class="nested-fields">${tx(e,t,i)}</div>`:l.s6}
    </div>
  `}var tj=i(2477),tN=i(7169),tB=i(5490);let tK=new WeakMap;function tZ(e){return null==e||""===e?"":(0,tB.uS)(e)||String(e)}let tU=["us","ms","s","min","h","d"],tH=RegExp(`^\\d+(?:\\.\\d+)?(?:${tU.map(e=>e.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|")})$`);function tV(e){if(null==e||""===e)return{value:"",unit:"s",parseable:!0};let t=String(e).trim(),i=t.match(/^(\d+(?:\.\d+)?)(us|ms|s|min|h|d)?$/);if(i){let[,e,t]=i;return{value:e,unit:t??"s",parseable:!0}}return{value:t,unit:"s",parseable:!1}}function tG(e,t){let i=e.trim();return""===i?"":`${i}${t}`}function tW(e,t,i){let a=i.getAt(t),o=ty(e,t,i,a);if(o)return o;let r=null==a?e.default_value:a,s=!0===(0,eM.FY)(r);return(0,l.qy)`
    <div class="switch-field" data-field-key=${tp(t)}>
      <div class="field-info">${tf(e,i,{includeHelpLink:!1})}</div>
      ${tg(e,i)}
      <wa-switch
        ?checked=${s}
        ?disabled=${tc(e,i)}
        aria-label=${tv(e,i)}
        @change=${e=>i.emitChange(t,e.target.checked)}
      ></wa-switch>
    </div>
  `}function tY(e,t){return(0,l.qy)`<wa-option
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
  </wa-option>`}function tJ(e,t){let i=e.getAt(t);return Array.isArray(i)?i:[]}function tQ(e,t,i){return{addItem:()=>e.emitChange(t,[...tJ(e,t),i()]),removeAt:i=>e.emitChange(t,tJ(e,t).filter((e,t)=>t!==i))}}function tX(e,t){return 0===e.length?(0,l.qy)`<p class="field-description">${t.localize("device.multi_value_empty")}</p>`:l.s6}function t0(e,t,i){return(0,l.qy)`
    <button
      type="button"
      class="multi-btn"
      ?disabled=${t}
      aria-label=${e.localize("device.multi_value_remove")}
      @click=${i}
    >
      <wa-icon library="mdi" name="close"></wa-icon>
    </button>
  `}function t1(e,t,i){return(0,l.qy)`
    <button
      type="button"
      class="multi-btn multi-add"
      ?disabled=${t}
      @click=${i}
    >
      <wa-icon library="mdi" name="plus"></wa-icon>
      ${e.localize("device.multi_value_add")}
    </button>
  `}var t2=i(8067);let t6=new(i(2741)).E({name:"automation-body-cache",bucketKey:()=>"",cacheMisses:!1,fetch:(e,t)=>{let i=t.map(e=>{let t=e.indexOf("/");return{type:e.slice(0,t),id:e.slice(t+1)}});return e.getAutomationBodies(i)}});function t3(e,t,i){return t6.fetch(e,`${t}/${i}`,void 0)}async function t4(e,t,i,a=t3){let o=await a(e,t,i.id);if(o&&"config_entries"in o)return i.config_entries=structuredClone(o.config_entries),"ok";let r=null===o?"no body returned":"body shape missing config_entries";return console.warn(`automation-body: ${t}/${i.id} ${r}; form will render empty`),null===o?"missingBody":"missingField"}function t5(){return{succeeded:0,missingBody:0,missingField:0,rejected:0}}function t8(e,t){e["ok"===t?"succeeded":t]++}function t9(e,t){return`${e??""}|${t??""}`}let t7={triggers:eV({name:"automation-catalog-cache:triggers",key:t9,fetch:(e,t,i)=>e.getAutomationTriggers(t,i)}),actions:eV({name:"automation-catalog-cache:actions",key:t9,fetch:(e,t,i)=>e.getAutomationActions(t,i)}),conditions:eV({name:"automation-catalog-cache:conditions",key:t9,fetch:(e,t,i)=>e.getAutomationConditions(t,i)}),light_effects:eV({name:"automation-catalog-cache:light_effects",key:t9,fetch:(e,t,i)=>e.getLightEffects(t,i)}),filters:eV({name:"automation-catalog-cache:filters",key:t9,fetch:(e,t,i)=>e.getFilters(t,i)})};function ie(e,t){return t7.triggers.getCached(e,t)}async function it(e,t,i){let a=await t7.light_effects.fetch(e,t,i);return ia("light_effects",t,i,a,t=>ir(e,"light_effects",t))}async function ii(e,t,i){let a=await t7.filters.fetch(e,t,i);return ia("filters",t,i,a,t=>ir(e,"filters",t))}async function ia(e,t,i,a,o){if(0===(await o(a)).succeeded)return a;let r=[...a];return t7[e].update(r,t,i),r}let io=new WeakSet;async function ir(e,t,i){let a=t5(),o=i.filter(e=>!io.has(e));if(0===o.length)return a;for(let i of(await Promise.allSettled(o.map(async i=>{let o=await t4(e,t,i);"ok"===o&&io.add(i),t8(a,o)}))))"rejected"===i.status&&(a.rejected++,console.warn(`${t} hydration failed`,i.reason));let r=a.missingBody+a.missingField+a.rejected;return r>0&&console.warn(`${t} hydration: ${a.succeeded} ok, ${r} failed (missingBody=${a.missingBody}, missingField=${a.missingField}, rejected=${a.rejected})`),a}function is(e){let t=Object.values(t7).map(t=>t.subscribe(e));return()=>{for(let e of t)e()}}var il=i(8339);function id(e){let t=Object.keys(e);return 1===t.length?t[0]:""}function ic(e){return e?e.replace(/_/g," ").replace(/\b\w/g,e=>e.toUpperCase()):""}let ip={time_period:eI.Hh.TIME_PERIOD,float:eI.Hh.FLOAT,integer:eI.Hh.INTEGER,string:eI.Hh.STRING,lambda:eI.Hh.LAMBDA},ih={light_effects:{cache:()=>t7.light_effects.getCached(void 0,void 0),fetch:e=>it(e),parentToken:e=>e,dedupByTypeId:!0},filter:{cache:()=>t7.filters.getCached(void 0,void 0),fetch:e=>ii(e),parentToken:e=>e.split(".",1)[0],dedupByTypeId:!1}};function iu(e){return Array.isArray(e)?e:[]}function im(e){let t=[],i=[];return e.forEach((e,a)=>{!(null===e||"object"!=typeof e||Array.isArray(e))&&Object.keys(e).length<=1&&(t.push(e),i.push(a))}),{items:t,positions:i}}function iv(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}class ig extends l.WF{connectedCallback(){super.connectedCallback();let e=this._ops();if(null===e)return;this._unsubscribe=is(()=>{if(!this.isConnected)return;let e=this._ops();if(null===e)return;let t=e.cache();void 0!==t&&(this._catalog=t,this._fetchError=!1)});let t=e.cache();this._fetchError=!1,void 0!==t?this._catalog=t:this._kickFetch(e)}updated(){if(this._kickedFetch||null!==this._catalog||this._fetchError||!this._api)return;let e=this._ops();null!==e&&void 0===e.cache()&&this._kickFetch(e)}_kickFetch(e){this._api&&(this._kickedFetch=!0,e.fetch(this._api).catch(e=>{console.error("Failed to fetch registry catalog",e),this.isConnected&&(this._fetchError=!0)}))}_ops(){return ih[this.entry?.registry??""]??null}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe?.(),this._unsubscribe=void 0,this._kickedFetch=!1}render(){let e=this._ops();if(null===e)return(0,l.qy)`
        <div class="field" data-field-key=${tp(this.path)}>
          ${tf(this.entry,this.ctx)}
          <p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_unsupported")}
          </p>
          ${t_(this.path,this.ctx)}
        </div>
      `;let t=this.ctx.getAt(this.path);if(t instanceof eM.ho||void 0!==t&&!Array.isArray(t))return(0,l.qy)`
        <div class="field" data-field-key=${tp(this.path)}>
          ${tf(this.entry,this.ctx)}
          <p class="field-description">
            ${this.ctx.localize("device.multi_value_yaml_only")}
          </p>
          ${t_(this.path,this.ctx)}
        </div>
      `;let{items:i}=im(iu(t)),a=tc(this.entry,this.ctx),o=this.ctx.sectionKey?e.parentToken(this.ctx.sectionKey):"",r=(this._catalog??[]).filter(e=>!o||0===e.applies_to.length||e.applies_to.includes(o)),s=null!==this._catalog&&0===this._catalog.length,n=this._fetchError?(0,l.qy)`<p class="registry-list-fallback">
          ${this.ctx.localize("device.registry_list_error")}
          ${this._api?(0,l.qy)`<button type="button" class="multi-btn" @click=${this._retryFetch}>
                ${this.ctx.localize("device.registry_list_retry")}
              </button>`:l.s6}
        </p>`:null===this._catalog?(0,l.qy)`<p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_loading")}
          </p>`:s?(0,l.qy)`<p class="registry-list-fallback">
              ${this.ctx.localize("device.registry_list_empty_catalog")}
            </p>`:0===r.length?(0,l.qy)`<p class="registry-list-fallback">
                ${this.ctx.localize("device.registry_list_no_applicable_options")}
              </p>`:l.s6,d=a||0===r.length;return(0,l.qy)`
      <div class="field" data-field-key=${tp(this.path)}>
        ${tf(this.entry,this.ctx)} ${tX(i,this.ctx)}
        ${n}
        ${i.map((t,o)=>this._renderRow(t,o,r,i,a,e.dedupByTypeId))}
        ${t1(this.ctx,d,()=>this._addItem())}
        ${t_(this.path,this.ctx)}
      </div>
    `}_renderRow(e,t,i,a,o,r){let s=id(e),n=new Set;r&&a.forEach((e,i)=>{if(i===t)return;let a=id(e);a&&n.add(a)});let d=i.find(e=>e.id===s),c=void 0!==d,p=[...i].sort((e,t)=>e.id.localeCompare(t.id)),h=s?e[s]:null,u=null!==h&&"object"==typeof h&&!Array.isArray(h)&&!(0,t2.b)(h)&&!(h instanceof eM.ho),m=u?null:this._scalarDispatchType(d,h),v=(null===h||u)&&d?.config_entries?d.config_entries:[];return(0,l.qy)`
      <div class="registry-list-item" data-row-index=${t}>
        <div class="registry-list-row">
          <wa-select
            .value=${s}
            ?disabled=${o}
            placeholder=${this.ctx.localize("device.registry_list_select")}
            aria-label=${this.ctx.localize("device.registry_list_row_label",{index:String(t+1)})}
            @change=${e=>{let i=e.target.value;this._renameRow(t,i)}}
          >
            ${!c&&s?(0,l.qy)`<wa-option value=${s} selected
                  >${ic(s)}</wa-option
                >`:l.s6}
            ${p.filter(e=>e.id===s||!n.has(e.id)).map(e=>(0,l.qy)`<wa-option value=${e.id} ?selected=${e.id===s}
                    >${ic(e.id)}</wa-option
                  >`)}
          </wa-select>
          ${t0(this.ctx,o,()=>this._removeAt(t))}
        </div>
        ${this._renderSubForm(t,s,m,v,d?.templatable??!1)}
      </div>
    `}_mutateEditable(e){let t=iu(this.ctx.getAt(this.path)),{items:i,positions:a}=im(t),o=e(i);this.ctx.emitChange(this.path,function(e,t,i){let a=[...e];if(t.forEach((e,t)=>{t<i.length&&(a[e]=i[t])}),i.length<t.length)for(let e of t.slice(i.length).reverse())a.splice(e,1);else if(i.length>t.length){let e=t.length>0?t[t.length-1]+1:a.length;a.splice(e,0,...i.slice(t.length))}return a}(t,a,o))}_scalarDispatchType(e,t){let i=e?.value_type;return i&&Object.prototype.hasOwnProperty.call(ip,i)?ip[i]:"string"==typeof t&&tH.test(t.trim())?eI.Hh.TIME_PERIOD:null}_renderSubForm(e,t,i,a,o){return null!==i?(0,l.qy)`<div class="registry-list-sub-form">
        ${this.ctx.renderEntry((0,il.h)({type:i,templatable:o}),[...this.path,String(e),t])}
      </div>`:a.length>0?(0,l.qy)`<div class="registry-list-sub-form">
        ${a.map(i=>this.ctx.renderEntry(i,[...this.path,String(e),t,i.key]))}
      </div>`:l.s6}_addItem(){this._mutateEditable(e=>[...e,{}])}_removeAt(e){this._mutateEditable(t=>t.filter((t,i)=>i!==e))}_renameRow(e,t){this._mutateEditable(i=>{if(!t)return i;let a=i[e];return a&&id(a)!==t?i.map((i,a)=>a===e?{[t]:null}:i):i})}constructor(...e){super(...e),this.path=[],this._catalog=null,this._fetchError=!1,this._kickedFetch=!1,this._retryFetch=()=>{if(!this._api)return;let e=this._ops();null!==e&&(this._fetchError=!1,e.fetch(this._api).catch(e=>{console.error("Failed to retry registry catalog fetch",e),this.isConnected&&(this._fetchError=!0)}))}}}ig.styles=[...td,(0,l.AH)`
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
    `],iv([(0,s.Fg)({context:u.Ie})],ig.prototype,"_api",void 0),iv([(0,d.MZ)({attribute:!1})],ig.prototype,"entry",void 0),iv([(0,d.MZ)({attribute:!1})],ig.prototype,"path",void 0),iv([(0,d.MZ)({attribute:!1})],ig.prototype,"ctx",void 0),iv([(0,d.wk)()],ig.prototype,"_catalog",void 0),iv([(0,d.wk)()],ig.prototype,"_fetchError",void 0),ig=iv([(0,d.EM)("esphome-registry-list")],ig);let i_="__none__";var ib=i(5230),iy=i(5659),iw=i(5874),i$=i(3107),ix=i(792),ik=i(2727),iz=i(2125),iC=i(4256),iE=i(6250);function iq(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}let iS=i$.YH.define();class iA extends iE.U{render(){return(0,l.qy)`<div class="cm-wrap ${this.invalid?"invalid":""}"></div>`}firstUpdated(){this._mountEditor()}updated(e){if(this._view&&(e.has("_darkMode")&&this._view.dispatch({effects:this._themeCompartment.reconfigure((0,iz.P5)(this._darkMode))}),e.has("disabled")&&this._view.dispatch({effects:this._editableCompartment.reconfigure(ix.Lz.editable.of(!this.disabled))}),e.has("value"))){let e=this._view.state.doc.toString();e!==this.value&&this._view.dispatch({changes:{from:0,to:e.length,insert:this.value},annotations:iS.of(!0)})}}_mountEditor(){this._mountView(this.value,[ik.oQ,(0,iC.O)(this._localize),(0,iy.I)(),iw.Xt.of("  "),ix.w4.of([ib.Yc]),this._editableCompartment.of(ix.Lz.editable.of(!this.disabled)),this._themeCompartment.of((0,iz.P5)(this._darkMode)),iz.gn,ix.Lz.updateListener.of(e=>{if(e.docChanged&&!e.transactions.some(e=>void 0!==e.annotation(iS))){let t=e.state.doc.toString();this.dispatchEvent(new CustomEvent("lambda-change",{detail:{value:t},bubbles:!0,composed:!0}))}})])}constructor(...e){super(...e),this._darkMode=!1,this._localize=e=>e,this.value="",this.disabled=!1,this.invalid=!1,this.placeholder="",this._themeCompartment=new i$.xx,this._editableCompartment=new i$.xx}}function iL(e){return(0,t2.b)(e)?e._lambda:e instanceof eM.ho?e.body:null==e?"":String(e)}function iM(e,t,i){let a=i.getAt(t),o=iL(a),r=null!==i.errorAt(t),s=tc(e,i),n=(0,t2.b)(a)?a._tag:void 0;return tb(e,t,i,(0,l.qy)`<esphome-lambda-editor
      .value=${o}
      .invalid=${r}
      ?disabled=${s}
      placeholder=${String(e.default_value??"")}
      @lambda-change=${e=>i.emitChange(t,n?{_lambda:e.detail.value,_tag:n}:{_lambda:e.detail.value})}
    ></esphome-lambda-editor>`)}iA.styles=(0,l.AH)`
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
  `,iq([(0,s.Fg)({context:u.B6,subscribe:!0}),(0,d.wk)()],iA.prototype,"_darkMode",void 0),iq([(0,s.Fg)({context:u.$F}),(0,d.wk)()],iA.prototype,"_localize",void 0),iq([(0,d.MZ)()],iA.prototype,"value",void 0),iq([(0,d.MZ)({type:Boolean,reflect:!0})],iA.prototype,"disabled",void 0),iq([(0,d.MZ)({type:Boolean})],iA.prototype,"invalid",void 0),iq([(0,d.MZ)()],iA.prototype,"placeholder",void 0),iA=iq([(0,d.EM)("esphome-lambda-editor")],iA);let iP=new WeakMap;i(8944);let iF=eV({name:"secret-keys",fetch:e=>e.getSecretKeys(),fallback:e=>(console.warn("secret-keys fetch failed; secret picker empty",e),[])});function iT(){return iF.getCached()}function iR(e){return iF.subscribe(e)}function iD(e){return a=e,iF.fetch(e)}function iO(e){return(a=e,o)?o:o=Promise.resolve().then(()=>e.getSecretKeys()).then(e=>{iF.update(e)}).catch(e=>{console.warn("secret-keys refresh failed; keeping cached list",e)}).finally(()=>{o=void 0})}async function iI(e,t,i){let{created:a}=await e.setSecret(t,i,!1);return a&&window.dispatchEvent(new CustomEvent("secrets-saved")),{created:a}}async function ij(e,t,i){await e.setSecret(t,i,!0),window.dispatchEvent(new CustomEvent("secrets-saved"))}async function iN(e,t,i,a,o){try{return await o(),iO(e),!0}catch(e){return console.error(i,e),c.A.error(a(t),{richColors:!0}),!1}}function iB(e,t,i,a,o){return iN(e,o.errorKey,o.logLabel,a,async()=>{let{created:r}=await iI(e,t,i);c.A[r?"success":"info"](a(r?o.createdKey:"device.secret_picker_linked",{key:t}),{richColors:!0})})}"u">typeof window&&window.addEventListener("secrets-saved",()=>{a&&iO(a)}),i(4604),i(2615);var iK=i(9309);function iZ(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}i(8768),(0,b.C)({alert:n.mdiAlert,"content-copy":n.mdiContentCopy});class iU extends l.WF{willUpdate(e){(e.has("secretKey")||e.has("present"))&&(this._draftValue="",this._stored=null,this._busy=!1,this._loading=!1,this._loadError=!1,this._loadToken++,this._opToken++)}updated(){this.present&&this.secretKey&&this._api&&null===this._stored&&!this._loading&&!this._loadError&&this._loadStored()}render(){return this.present?this._renderEdit():this._renderCreate()}get _dirty(){return null!==this._stored&&this._draftValue!==this._stored}get _hasDraft(){return""!==this._draftValue.trim()}get _loadingStored(){return this.present&&null===this._stored}_renderEdit(){return this._loadError?this._renderLoadError():(0,l.qy)`<div class="row">
        ${this._renderInput()}
        <button
          class="copy"
          type="button"
          ?disabled=${this._busy||this._loadingStored}
          title=${this._localize("device.secret_reveal_copy")}
          aria-label=${this._localize("device.secret_reveal_copy")}
          @click=${this._copy}
        >
          <wa-icon library="mdi" name="content-copy"></wa-icon>
        </button>
        <button
          class="save"
          type="button"
          ?disabled=${this._busy||!this._dirty}
          @click=${this._save}
        >
          ${this._localize("device.secret_picker_save")}
        </button>
      </div>
      <esphome-confirm-dialog
        heading=${this._localize("device.secret_picker_shared_confirm_title")}
        confirm-label=${this._localize("device.secret_picker_save")}
        message=${this._localize("device.secret_picker_shared_confirm_message",{key:this.secretKey})}
        @confirm=${this._persist}
      ></esphome-confirm-dialog>`}_renderLoadError(){return(0,l.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_reveal_error")}
        <button class="retry" type="button" @click=${this._retry}>
          ${this._localize("device.secret_picker_retry")}
        </button>
      </span>
    </div>`}_renderCreate(){return(0,l.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_missing",{key:this.secretKey})}
      </span>
      <div class="row">
        ${this._renderInput()}
        <button
          class="save"
          type="button"
          ?disabled=${this._busy||!this._hasDraft}
          @click=${this._create}
        >
          ${this._localize("device.secret_picker_missing_create")}
        </button>
      </div>
    </div>`}_renderInput(){return(0,l.qy)`<esphome-password-input
      class="value"
      .value=${this._draftValue}
      .disabled=${this._busy||this._loadingStored}
      .placeholder=${this._localize(this.present?"device.secret_picker_value":"device.secret_picker_missing_placeholder")}
      .label=${this._localize("device.secret_picker_value_label",{key:this.secretKey})}
      @password-input-change=${e=>{this._draftValue=e.detail.value}}
      @keydown=${e=>{"Enter"===e.key&&(e.preventDefault(),this.present?this._save():this._create())}}
    ></esphome-password-input>`}async _loadStored(){let e=++this._loadToken;this._loading=!0;let t=null,i=!1;try{let e=await this._api.getConfig("secrets.yaml");t=ta(e,this.secretKey)}catch{i=!0,c.A.error(this._localize("device.secret_picker_reveal_error"),{richColors:!0})}if(e===this._loadToken){if(this._loading=!1,i){this._loadError=!0;return}this._stored=t??"",this._draftValue=this._stored}}async _run(e,t){let i=this._api;if(!i||!this.secretKey||this._busy)return;let a=this._opToken;this._busy=!0;try{let o=await e(i);if(a!==this._opToken)return;o&&t()}finally{a===this._opToken&&(this._busy=!1)}}constructor(...e){super(...e),this._localize=e=>e,this.secretKey="",this.present=!1,this.deviceName="",this._draftValue="",this._stored=null,this._busy=!1,this._loadError=!1,this._loadToken=0,this._opToken=0,this._loading=!1,this._retry=()=>{this._loadError=!1},this._copy=async()=>{await (0,iK.l)(this._draftValue)&&c.A.success(this._localize("device.secret_reveal_copied"),{richColors:!0})},this._create=()=>{this._hasDraft&&this._run(e=>iB(e,this.secretKey,this._draftValue,this._localize,{createdKey:"device.secret_picker_missing_created",errorKey:"device.secret_picker_missing_error",logLabel:"Secret create failed"}),()=>{this._draftValue=""})},this._save=()=>{if(this._dirty){var e;let t;if(e=this.secretKey,!(t=te(this.deviceName))||!e.startsWith(`${t}__`))return void this._confirmDialog?.open();this._persist()}},this._persist=()=>{this._run(e=>{var t,i,a,o;return t=this.secretKey,i=this._draftValue,a=this._localize,iN(e,(o={savedKey:"device.secret_picker_saved",errorKey:"device.secret_picker_save_error",logLabel:"Secret save failed"}).errorKey,o.logLabel,a,async()=>{await ij(e,t,i),c.A.success(a(o.savedKey,{key:t}),{richColors:!0})})},()=>{this._stored=this._draftValue})}}}function iH(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}iU.styles=(0,l.AH)`
    :host {
      display: block;
    }

    .fix {
      display: flex;
      flex-direction: column;
      gap: var(--wa-space-2xs);
      padding-left: var(--wa-space-2xs);
    }

    .msg {
      display: flex;
      align-items: center;
      gap: var(--wa-space-2xs);
      font-size: var(--wa-font-size-xs);
      color: var(--wa-color-danger-border, var(--wa-color-danger-60));
    }

    .row {
      display: flex;
      align-items: center;
      gap: var(--wa-space-xs);
    }

    /* esphome-password-input is display:block; flex so it shares the row. */
    esphome-password-input {
      flex: 1;
      min-width: 0;
    }

    .copy {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      flex-shrink: 0;
      padding: 0;
      border: none;
      border-radius: var(--wa-border-radius-m);
      background: transparent;
      color: var(--wa-color-text-quiet);
      cursor: pointer;
      transition:
        background 0.12s,
        color 0.12s;
    }

    .copy:hover:not(:disabled) {
      background: var(--wa-color-surface-border);
      color: var(--wa-color-text-normal);
    }

    .copy:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .copy wa-icon {
      font-size: 15px;
    }

    .retry {
      padding: 0;
      border: none;
      background: transparent;
      color: var(--esphome-primary);
      font: inherit;
      cursor: pointer;
      text-decoration: underline;
    }

    .save {
      padding: 0 14px;
      min-height: var(--wa-form-control-height);
      box-sizing: border-box;
      flex-shrink: 0;
      border: var(--wa-border-width-s) solid var(--esphome-primary);
      border-radius: var(--wa-border-radius-m);
      background: var(--esphome-primary);
      color: var(--wa-color-surface-default);
      font-family: inherit;
      font-size: var(--wa-font-size-s);
      cursor: pointer;
      transition:
        opacity 0.12s,
        background 0.12s;
    }

    .save:hover:not(:disabled) {
      opacity: 0.9;
    }

    .save:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `,iZ([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iU.prototype,"_localize",void 0),iZ([(0,s.Fg)({context:u.Ie,subscribe:!0}),(0,d.wk)()],iU.prototype,"_api",void 0),iZ([(0,d.MZ)({attribute:"secret-key"})],iU.prototype,"secretKey",void 0),iZ([(0,d.MZ)({type:Boolean})],iU.prototype,"present",void 0),iZ([(0,d.MZ)({attribute:"device-name"})],iU.prototype,"deviceName",void 0),iZ([(0,d.P)("esphome-confirm-dialog")],iU.prototype,"_confirmDialog",void 0),iZ([(0,d.wk)()],iU.prototype,"_draftValue",void 0),iZ([(0,d.wk)()],iU.prototype,"_stored",void 0),iZ([(0,d.wk)()],iU.prototype,"_busy",void 0),iZ([(0,d.wk)()],iU.prototype,"_loadError",void 0),iU=iZ([(0,d.EM)("esphome-secret-value")],iU),(0,b.C)({alert:n.mdiAlert,check:n.mdiCheck,"chevron-down":n.mdiChevronDown,"key-variant":n.mdiKeyVariant,plus:n.mdiPlus,"shield-key-outline":n.mdiShieldKeyOutline});class iV extends l.WF{get _keys(){return this._secretKeys.value}get _migrateTarget(){return this.recommendedKeys[0]??""}get _canMigrate(){return""===this.selectedKey&&""!==this.value&&""!==this._migrateTarget&&void 0!==this._keys&&!this._keys.includes(this._migrateTarget)}get _missing(){return""!==this.selectedKey&&void 0!==this._keys&&!this._keys.includes(this.selectedKey)}render(){var e,t,i,a;let o,r,s=""!==this.selectedKey,n=this._missing,d=(e=this._keys??[],t=[...this.recommendedKeys,this.selectedKey],i=this.deviceName,a=this._devices.map(e=>e.name),o=new Set(t.filter(Boolean)),r=new Set(function(e,t,i){let a=te(t);if(!a)return[...e];let o=new Set(i.map(e=>te(e)).filter(e=>e&&e!==a));return 0===o.size?[...e]:e.filter(e=>{let t=e.indexOf("__");return t<=0||!o.has(e.slice(0,t))})}(e,i,a)),e.filter(e=>o.has(e)||r.has(e)&&!e9.has(e))),c=new Set(d),p=new Set(this.recommendedKeys),h=this.recommendedKeys.filter(e=>c.has(e)),u=d.filter(e=>!p.has(e));return(0,l.qy)`
      <wa-dropdown @wa-select=${this._onSelect}>
        <button
          slot="trigger"
          class=${n?"trigger missing":s?"trigger selected":"trigger"}
          type="button"
          ?disabled=${this.disabled}
          aria-label=${this._localize(n?"device.secret_picker_aria_missing":"device.secret_picker_aria",{field:this.fieldLabel})}
        >
          <wa-icon
            class="key"
            library="mdi"
            name=${n?"alert":"key-variant"}
          ></wa-icon>
          ${s?(0,l.qy)`<span class="label">${this.selectedKey}</span>`:(0,l.qy)`<span class="placeholder"
                >${this._localize("device.secret_picker_label")}</span
              >`}
          <wa-icon class="chevron" library="mdi" name="chevron-down"></wa-icon>
        </button>
        ${this._canMigrate?(0,l.qy)`<wa-dropdown-item class="migrate" value=${"__esphome_migrate_secret__"}>
                <wa-icon slot="icon" library="mdi" name="shield-key-outline"></wa-icon>
                ${this._localize("device.secret_picker_migrate",{key:this._migrateTarget})}
              </wa-dropdown-item>
              <wa-divider role="separator"></wa-divider>`:l.s6}
        ${h.length?(0,l.qy)`<small class="group-label" aria-hidden="true"
                >${this._localize("device.secret_picker_related")}</small
              >
              ${h.map(e=>this._renderKeyItem(e))}
              ${u.length?(0,l.qy)`<small class="group-label" aria-hidden="true"
                    >${this._localize("device.secret_picker_shared")}</small
                  >`:l.s6}`:l.s6}
        ${u.map(e=>this._renderKeyItem(e))}
        ${d.length?l.s6:(0,l.qy)`<wa-dropdown-item class="empty" disabled role="status"
              >${this._localize("device.secret_picker_empty")}</wa-dropdown-item
            >`}
        <wa-divider role="separator"></wa-divider>
        <wa-dropdown-item class="create" value=${"__esphome_create_secret__"}>
          <wa-icon slot="icon" library="mdi" name="plus"></wa-icon>
          ${this._localize("device.secret_picker_create")}
        </wa-dropdown-item>
        ${s?(0,l.qy)`<wa-dropdown-item class="manual" value=${"__esphome_manual_value__"}>
              ${this._localize("device.secret_picker_manual")}
            </wa-dropdown-item>`:l.s6}
      </wa-dropdown>
      ${s?(0,l.qy)`<esphome-secret-value
            secret-key=${this.selectedKey}
            ?present=${!n}
            device-name=${this.deviceName}
          ></esphome-secret-value>`:l.s6}
    `}_renderKeyItem(e){return(0,l.qy)`<wa-dropdown-item
      value=${e}
      aria-selected=${e===this.selectedKey?"true":"false"}
    >
      ${e===this.selectedKey?(0,l.qy)`<wa-icon slot="icon" class="check" library="mdi" name="check"></wa-icon>`:l.s6}
      ${e}
    </wa-dropdown-item>`}_onSelect(e){let t=e.detail.item,i=t.classList;if(i?.contains("create"))return void(0,f.oo)("/secrets");if(i?.contains("migrate"))return void this._migrate();if(i?.contains("manual"))return void this._manual();let a=t.value??"";a&&this._emit(`!secret ${a}`)}async _manual(){if(!this._api||!this.selectedKey)return void this._emit("");try{let e=await this._api.getConfig("secrets.yaml");this._emit(ta(e,this.selectedKey)??"")}catch{c.A.error(this._localize("device.secret_picker_manual_error"),{richColors:!0})}}_emit(e){this.dispatchEvent(new CustomEvent("secret-selected",{detail:{value:e},bubbles:!0,composed:!0}))}async _migrate(){let e=this._migrateTarget;this._api&&e&&this.value&&await iB(this._api,e,this.value,this._localize,{createdKey:"device.secret_picker_migrated",errorKey:"device.secret_picker_migrate_error",logLabel:"Secret migration failed"})&&this._emit(`!secret ${e}`)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.disabled=!1,this.deviceName="",this.full=!1,this.fieldLabel="",this.selectedKey="",this.value="",this.recommendedKeys=[],this._secretKeys=new eQ(this,{getCached:iT,subscribe:iR,fetch:iD},()=>this._api)}}function iG(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}iV.styles=(0,l.AH)`
    :host {
      display: inline-flex;
    }

    :host([full]) {
      display: flex;
      flex-direction: column;
      align-items: stretch;
      gap: var(--wa-space-2xs);
      width: 100%;
    }

    :host([full]) wa-dropdown,
    :host([full]) .trigger {
      width: 100%;
    }

    :host([full]) .chevron {
      margin-left: auto;
    }

    .trigger {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 0 10px;
      min-height: 34px;
      box-sizing: border-box;
      background: transparent;
      border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
      border-radius: var(--wa-border-radius-m);
      color: var(--wa-color-text-quiet);
      font-family: inherit;
      font-size: var(--wa-font-size-xs);
      white-space: nowrap;
      cursor: pointer;
      transition:
        background 0.12s,
        border-color 0.12s,
        color 0.12s;
    }

    .trigger:hover:not(:disabled) {
      color: var(--esphome-primary);
      border-color: var(--esphome-primary);
      background: var(--esphome-tint);
    }

    /* Reads as a select that's already pointed at a secret. */
    .trigger.selected {
      color: var(--wa-color-text-normal);
      border-color: var(--esphome-primary);
    }

    /* Referenced secret is absent from secrets.yaml — flag it. */
    .trigger.missing {
      color: var(--wa-color-text-normal);
      border-color: var(--wa-color-danger-border, var(--wa-color-danger-60));
    }

    .trigger.missing .key {
      color: var(--wa-color-danger-border, var(--wa-color-danger-60));
    }

    .trigger:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .trigger .key {
      font-size: 15px;
      color: var(--esphome-primary);
    }

    .trigger .label {
      /* flex + min-width:0 so a long key actually shrinks and ellipsizes
         inside the inline-flex trigger (notably in full / width:100% mode). */
      flex: 1;
      min-width: 0;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .trigger .placeholder {
      color: var(--wa-color-text-quiet);
    }

    .trigger .chevron {
      font-size: 14px;
    }

    /* Keep the menu inside the viewport on small screens and wrap long
       keys / the migrate label instead of overflowing off-screen. */
    wa-dropdown::part(menu) {
      max-width: min(92vw, 340px);
      box-sizing: border-box;
    }

    wa-dropdown-item {
      max-width: min(92vw, 340px);
      box-sizing: border-box;
    }

    wa-dropdown-item::part(label) {
      white-space: normal;
      overflow-wrap: anywhere;
    }

    .group-label {
      display: block;
      padding: var(--wa-space-2xs) var(--wa-space-s) 0;
      font-size: var(--wa-font-size-2xs);
      font-weight: var(--wa-font-weight-semibold);
      color: var(--wa-color-text-quiet);
      text-transform: uppercase;
    }

    .empty {
      color: var(--wa-color-text-quiet);
    }

    .check {
      font-size: 15px;
      color: var(--esphome-primary);
    }

    .create wa-icon,
    .migrate wa-icon {
      font-size: 15px;
    }
  `,iH([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iV.prototype,"_localize",void 0),iH([(0,s.Fg)({context:u.Ie,subscribe:!0}),(0,d.wk)()],iV.prototype,"_api",void 0),iH([(0,s.Fg)({context:u.xJ,subscribe:!0}),(0,d.wk)()],iV.prototype,"_devices",void 0),iH([(0,d.MZ)({type:Boolean})],iV.prototype,"disabled",void 0),iH([(0,d.MZ)({attribute:"device-name"})],iV.prototype,"deviceName",void 0),iH([(0,d.MZ)({type:Boolean,reflect:!0})],iV.prototype,"full",void 0),iH([(0,d.MZ)({attribute:"field-label"})],iV.prototype,"fieldLabel",void 0),iH([(0,d.MZ)({attribute:"selected-key"})],iV.prototype,"selectedKey",void 0),iH([(0,d.MZ)()],iV.prototype,"value",void 0),iH([(0,d.MZ)({attribute:!1})],iV.prototype,"recommendedKeys",void 0),iV=iH([(0,d.EM)("esphome-secret-picker")],iV),(0,b.C)({"alert-circle-outline":n.mdiAlertCircleOutline,"chevron-down":n.mdiChevronDown,"chevron-up":n.mdiChevronUp,close:n.mdiClose,"open-in-new":n.mdiOpenInNew,plus:n.mdiPlus});class iW extends l.WF{render(){let e=this._buildCtx(),t=function(e){let t=new Map;for(let i of e)if(i.exclusive_group){let e=t.get(i.exclusive_group)??[];e.push(i),t.set(i.exclusive_group,e)}let i=new Set,a=[];for(let o of e)o.exclusive_group?i.has(o.exclusive_group)||(i.add(o.exclusive_group),a.push(t.get(o.exclusive_group))):a.push(o);return a}(this.entries),i=this.entries.filter(e=>!e.exclusive_group),a=new Set(this._filterRenderable(i,this.values));return(0,l.qy)`${t.map(t=>{let i,o,r,s,n,d,c,p;return Array.isArray(t)?(i=t.filter(t=>void 0!==e.getAt([t.key])),o=i[0]?.key??"",r=t.find(e=>e.key===o),s=e.disabled,n=e.scopeValues([]),d=e.board?.esphome.platform??null,c=t.filter(t=>void 0!==e.getAt([t.key])||(0,eN.VP)(t,n,e.presentComponents,d)),p=`exclusive-group-${t[0].key}`,(0,l.qy)`
    <div class="field" data-field-key=${tp(r?[r.key]:[])}>
      <label class="field-label" id=${p}>
        ${e.localize("device.exclusive_group_label")}
        <span class="required">*</span>
      </label>
      <wa-select
        data-no-value-sync
        aria-labelledby=${p}
        ?disabled=${s}
        @change=${i=>{let a=i.target.value;var o=a===i_?"":a;for(let i of t)i.key!==o&&void 0!==e.getAt([i.key])&&e.emitChange([i.key],void 0);o&&void 0===e.getAt([o])&&e.emitChange([o],{})}}
      >
        <wa-option value=${i_} ?selected=${""===o}>
          ${e.localize("device.exclusive_group_placeholder")}
        </wa-option>
        ${c.map(t=>(0,l.qy)`<wa-option value=${t.key} ?selected=${t.key===o}
              >${tv(t,e)}</wa-option
            >`)}
      </wa-select>
      ${i.length>1?(0,l.qy)`<p class="field-description exclusive-group-conflict">
            ${e.localize("device.exclusive_group_conflict")}
          </p>`:l.s6}
      ${r?(0,l.qy)`<div class="nested-fields">
            ${tx(r,[r.key],e,{includeAdvanced:!0})}
          </div>`:l.s6}
    </div>
  `):a.has(t)?this._renderEntry(t,t.key?[t.key]:[],e):l.s6})}`}willUpdate(e){e.has("entries")&&void 0!==e.get("entries")&&(this._pendingUnits.clear(),this._editingMagnitudes.clear(),this._seededNestedOpen.clear())}_pathOf(e){return th(e.getAttribute("data-field-key")??"")}updated(e){super.updated(e),this._syncSelectValues(),this._fieldScroll.maybeScroll(e)}async _syncSelectValues(){if(this.shadowRoot)for(let e of this.shadowRoot.querySelectorAll("[data-field-key]")){let t=e.querySelector("wa-select");if(!t)continue;if(t.hasAttribute("data-no-value-sync")){await this._syncSelectedAttr(t);continue}if(t.updateComplete)try{await t.updateComplete}catch{}let i=this._pathOf(e);if(!i.length)continue;let a=(0,eB.O6)(this.values,i);if(!(0,eB.k4)(a)){""!==(Array.isArray(t.value)?t.value[0]??"":t.value??"")&&(t.value="");continue}let o=String(a??""),r=Array.from(t.querySelectorAll("wa-option")),s=o.match(/^\s*(?:GPIO)?(\d+)\s*$/i)?.[1],n=e=>r.find(t=>t.value?.toLowerCase()===e.toLowerCase()),l=o?n(o)??(s?n(`GPIO${s}`):void 0):null,d=l?.value??o;(Array.isArray(t.value)?t.value[0]??"":t.value??"")!==d&&(t.value=d)}}async _syncSelectedAttr(e){if(e.updateComplete)try{await e.updateComplete}catch{}let t=e.querySelector("wa-option[selected]"),i=t?.value??"";i&&(Array.isArray(e.value)?e.value[0]??"":e.value??"")!==i&&(e.value=i)}_renderEntry(e,t,i){try{return this._renderEntryUnsafe(e,t,i)}catch(a){console.error("esphome-config-entry-form: render failed for entry",{key:e.key,type:e.type,path:t},a);let i=(0,en.u)(a);return(0,l.qy)`<div class="render-error" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div>
          <strong> ${this._localize("device.entry_render_error_title")} </strong>
          <code class="render-error-key"
            >${e.key||"(empty key)"} · ${e.type}</code
          >
          <pre class="render-error-message">${i}</pre>
        </div>
      </div>`}}_renderEntryUnsafe(e,t,i){var a,o;if(e.templatable&&(a=e.type)!==eI.Hh.NESTED&&a!==eI.Hh.MAP&&a!==eI.Hh.DIVIDER&&a!==eI.Hh.LABEL&&a!==eI.Hh.ALERT){let a,r,s,n,d,c,p;return o=()=>this._renderEntryLeaf(e,t,i),a=i.getAt(t),r=(0,t2.b)(a),(s=iP.get(i.stashOwner))||(s=new Map,iP.set(i.stashOwner,s)),n=t.join("."),(d=s.get(n))||(d={},s.set(n,d)),c=d,p=tp(t),(0,l.qy)`
    <div class="templatable-field" data-field-key=${p}>
      ${tn({isLambda:r,disabled:i.disabled,localize:i.localize,onSwitch:e=>{e!==r&&(r?(c.lambda=(0,t2.b)(a)?a._lambda:"",i.emitChange(t,c.literal??"")):(c.literal=a,i.emitChange(t,{_lambda:c.lambda??"",_tag:"!lambda"})))}})}
      ${r?iM(e,t,i):o()}
    </div>
  `}return this._renderEntryLeaf(e,t,i)}_renderEntryLeaf(e,t,i){let a=i.getAt(t);if("string"==typeof a&&(0,eX.R_)(a)){let a=e.type===eI.Hh.SECURE_STRING?"password":"text";return t$(e,a,t,i)}if(e.type===eI.Hh.DIVIDER)return(0,l.qy)`<wa-divider></wa-divider>`;if(e.type===eI.Hh.LABEL)return(0,l.qy)`<p class="label-entry">${tv(e,i)}</p>`;if(e.type===eI.Hh.ALERT)return(0,l.qy)`<div class="alert-entry">${tv(e,i)}</div>`;if(e.type===eI.Hh.NESTED)return e.multi_value?function(e,t,i){let a=i.getAt(t);if(a instanceof eM.ho)return(0,l.qy)`
      <div class="nested-list" data-field-key=${tp(t)}>
        ${tf(e,i)}
        <p class="field-description">${i.localize("device.multi_value_yaml_only")}</p>
        ${t_(t,i)}
      </div>
    `;let o=(0,eB.ly)(a),r=tc(e,i),{addItem:s,removeAt:n}=tQ(i,t,()=>({})),d=tv(e,i),c=e.config_entries??[];return(0,l.qy)`
    <div class="nested-list" data-field-key=${tp(t)}>
      ${tf(e,i)} ${tX(o,i)}
      ${o.map((e,a)=>{let o=[...t,String(a)],s=i.filterRenderable(c,e);return(0,l.qy)`
          <div class="nested-list-item" data-field-key=${tp(o)}>
            <div class="nested-list-item-header">
              <span class="nested-list-item-title"> ${d} ${a+1} </span>
              ${t0(i,r,()=>n(a))}
            </div>
            <div class="nested-fields">
              ${s.map(e=>i.renderEntry(e,[...o,e.key]))}
            </div>
          </div>
        `})}
      ${t1(i,r,s)} ${t_(t,i)}
    </div>
  `}(e,t,i):tI(e,t,i);if(e.type===eI.Hh.MAP){let a,o,r,s,n,d;return a=(e.config_entries??[])[0],s=Object.keys(r=(o=i.getAt(t))&&"object"==typeof o&&!Array.isArray(o)?o:{}),n=tc(e,i),d=()=>{let e=i.getAt(t);return e&&"object"==typeof e&&!Array.isArray(e)?Object.assign(Object.create(null),e):Object.create(null)},(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      ${0===s.length?(0,l.qy)`<p class="field-description">${i.localize("device.map_empty")}</p>`:l.s6}
      ${s.map(e=>{let o,s;return o=[...t,e],s=!(0,eB.k4)(r[e]),(0,l.qy)`
      <div class="map-row" data-field-key=${tp(o)}>
        <input
          type="text"
          class="multi-input map-key-input"
          .value=${e}
          ?disabled=${n}
          @change=${a=>((e,a)=>{if(e===a||!a)return;let o=i.getAt(t);if(!o||"object"!=typeof o||Array.isArray(o)||a in o)return;let r=Object.create(null);for(let[t,i]of Object.entries(o))r[t===e?a:t]=i;i.emitChange(t,r)})(e,a.target.value)}
        />
        <div class="map-value">
          ${s?(0,l.qy)`<p class="map-value-yaml-only">
                ${i.localize("device.map_value_edit_in_yaml")}
              </p>`:a?i.renderEntry(a,o):l.s6}
        </div>
        <button
          type="button"
          class="multi-btn"
          ?disabled=${n}
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
        ?disabled=${n}
        @click=${()=>{let e=d(),a=1;for(;`new_${a}`in e;)a++;e[`new_${a}`]="",i.emitChange(t,e)}}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${i.localize("device.map_add")}
      </button>
      ${t_(t,i)}
    </div>
  `}if(e.type===eI.Hh.REGISTRY_LIST)return(0,l.qy)`<esphome-registry-list
    .entry=${e}
    .path=${t}
    .ctx=${i}
  ></esphome-registry-list>`;if(e.multi_value)return function(e,t,i){let a=tJ(i,t);if(a.some(e=>!(0,eB.k4)(e)))return tw(e,t,i);let o=(e.type===eI.Hh.INTEGER||e.type===eI.Hh.FLOAT)&&"hex"!==e.display_format,r=o?a.map(e=>String(e??"")):a.map(e=>(0,e4.hZ)(String(e))),s=null!==i.errorAt(t),n=tc(e,i),{addItem:d,removeAt:c}=tQ(i,t,()=>"");return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)} ${tX(r,i)}
      ${r.map((a,r)=>(0,l.qy)`
          <div class="multi-row">
            <input
              type=${o?"number":"text"}
              step=${o?e.type===eI.Hh.FLOAT?"any":"1":l.s6}
              class="multi-input ${s?"invalid":""}"
              .value=${a}
              ?disabled=${n}
              @input=${e=>{var a;let s;return a=e.target.value,void((s=[...tJ(i,t)])[r]=o?""===a?"":Number(a):(0,e4.iI)(a),i.emitChange(t,s))}}
            />
            ${t0(i,n,()=>c(r))}
          </div>
        `)}
      ${t1(i,n,d)} ${t_(t,i)}
    </div>
  `}(e,t,i);if(e.references_component)return function(e,t,i){let a=e.references_component||"",o=(0,ed.Zm)(i.yaml,a,i.resolveInterfaceProviders(a)),r=i.getAt(t),s=ty(e,t,i,r);if(s)return s;let n=String(r??""),d=null!==i.errorAt(t),c=(e,t,i)=>(0,l.qy)`
    <wa-option
      class="id-option"
      value=${e}
      .label=${t}
      ?selected=${e===n}
    >
      <span class="id-option-stack">
        <span class="id-option-primary">${t}</span>
        <span class="id-option-secondary">${i}</span>
      </span>
    </wa-option>
  `,p=""!==n&&!o.some(e=>e.id===n),h=p?c(n,n,i.localize("device.id_reference_unresolved",{domain:a})):l.s6,u=0===o.length&&!p,m=e=>{let o=e.target,r=o.value;if(r===tF){o.value=n,i.requestAddComponent(a);return}i.emitChange(t,r)},v=(0,l.qy)`
    <wa-option
      class="id-option id-option-add ${u?"id-option-add--solo":""}"
      value=${tF}
    >
      <span class="id-option-stack">
        <span class="id-option-primary id-option-primary-add">
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${i.localize("device.id_reference_add",{domain:a})}
        </span>
      </span>
    </wa-option>
  `;return u?(0,l.qy)`
      <div class="field" data-field-key=${tp(t)}>
        ${tf(e,i)}
        <wa-select
          class=${d?"invalid":""}
          ?disabled=${tc(e,i)}
          placeholder=${i.localize("device.id_reference_empty",{domain:a})}
          @change=${m}
        >
          ${v}
        </wa-select>
        ${t_(t,i)}
      </div>
    `:(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <wa-select
        class=${d?"invalid":""}
        ?disabled=${tc(e,i)}
        @change=${m}
      >
        ${h}
        ${o.map(e=>c(e.id,e.name||e.id,e.name?`${e.id} \xb7 ${a}`:a))}
        ${v}
      </wa-select>
      ${t_(t,i)}
    </div>
  `}(e,t,i);if(e.options&&e.options.length>0)return function(e,t,i){let a=i.getAt(t),o=ty(e,t,i,a);if(o)return o;let r=String(a??""),s=null!==i.errorAt(t),n=tc(e,i);if(e.suggestions&&e.suggestions.length>0){let a=r.toLowerCase();return(0,l.qy)`
      <div class="field" data-field-key=${tp(t)}>
        ${tf(e,i)}
        <wa-select
          class=${s?"invalid":""}
          ?disabled=${n}
          placeholder=${String(e.default_value??"")}
          @change=${e=>i.emitChange(t,e.target.value)}
        >
          ${e.suggestions.map(e=>{let t=String(e);return(0,l.qy)`<wa-option value=${t} ?selected=${t.toLowerCase()===a}
              >${t}</wa-option
            >`})}
        </wa-select>
        ${t_(t,i)}
      </div>
    `}if(e.allow_custom_value&&e.options&&e.options.length>0){let a=`combobox-${t.join("-")}`;return(0,l.qy)`
      <div class="field" data-field-key=${tp(t)}>
        ${tf(e,i)}
        <input
          type="text"
          class="combobox-input ${s?"invalid":""}"
          list=${a}
          .value=${r}
          ?disabled=${n}
          placeholder=${String(e.default_value??"")}
          @input=${e=>i.emitChange(t,e.target.value)}
        />
        <datalist id=${a}>
          ${e.options.map(e=>(0,l.qy)`<option value=${e.value}>${e.label}</option>`)}
        </datalist>
        ${t_(t,i)}
      </div>
    `}let d=r.toLowerCase(),c=null!=e.default_value?String(e.default_value):"",p=e.options?.find(e=>e.value.toLowerCase()===c.toLowerCase()),h=p?.label??c,{clearable:u,visibleOptions:m}=function(e){let t=tK.get(e);if(!t){let i=e.options??[];t={clearable:i.some(e=>""===e.value),visibleOptions:i.filter(e=>""!==e.value)},tK.set(e,t)}return t}(e);return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <wa-select
        class=${s?"invalid":""}
        ?disabled=${n}
        .withClear=${u}
        placeholder=${h}
        @change=${e=>i.emitChange(t,e.target.value)}
      >
        ${u?(0,l.qy)`<wa-icon slot="clear-icon" library="mdi" name="close"></wa-icon>`:l.s6}
        ${m.map(e=>(0,l.qy)`<wa-option
              value=${e.value}
              ?selected=${e.value.toLowerCase()===d}
              >${e.label}</wa-option
            >`)}
      </wa-select>
      ${t_(t,i)}
    </div>
  `}(e,t,i);switch(e.type){case eI.Hh.BOOLEAN:return tW(e,t,i);case eI.Hh.SELECT:return t$(e,"text",t,i);case eI.Hh.SECURE_STRING:return t$(e,"password",t,i);case eI.Hh.INTEGER:case eI.Hh.FLOAT:return function(e,t,i){var a,o,r,s,n,d;if(e.suggestions&&e.suggestions.length>0)return t$(e,"number",t,i);let c=i.getAt(t),p=ty(e,t,i,c);if(p)return p;if("hex"===e.display_format){let s,n,d,c,p;return a=e,o=t,s=(r=i).getAt(o),n=null!==r.errorAt(o),d=tc(a,r),c=r.getEditingMagnitude(o)??tZ(s),p=tZ(a.default_value),tb(a,o,r,(0,l.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${n?"invalid":""}
      .value=${c}
      ?disabled=${d}
      placeholder=${p}
      @input=${e=>{let t=e.target.value;(r.setEditingMagnitude(o,t),""===t)?r.emitChange(o,""):r.emitChange(o,(0,tB.uS)((0,tB.EG)(t))||t)}}
      @blur=${()=>r.clearEditingMagnitude(o)}
    />`)}if(e.type===eI.Hh.INTEGER){let a,o,r;return s=e,n=t,a=(d=i).getEditingMagnitude(n)??String(d.getAt(n)??""),o=null!==d.errorAt(n),r=tc(s,d),tb(s,n,d,(0,l.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${o?"invalid":""}
      .value=${a}
      ?disabled=${r}
      placeholder=${String(s.default_value??"")}
      @input=${e=>{let t=e.target.value;d.setEditingMagnitude(n,t),d.emitChange(n,(0,eK.s)(t))}}
      @blur=${()=>d.clearEditingMagnitude(n)}
    />`)}let h=String(c??""),u=null!==i.errorAt(t),m=e.range?String(e.range[0]):void 0,v=e.range?String(e.range[1]):void 0,g=tc(e,i);return tb(e,t,i,(0,l.qy)`<input
      type="number"
      class=${u?"invalid":""}
      .value=${h}
      ?disabled=${g}
      min=${m??""}
      max=${v??""}
      step="any"
      placeholder=${String(e.default_value??"")}
      @input=${e=>{let a=e.target.value;i.emitChange(t,""===a?"":Number(a))}}
    />`)}(e,t,i);case eI.Hh.FLOAT_WITH_UNIT:return function(e,t,i){let a=e.unit_options??[],o=a[0]??"",r=i.getAt(t),s=ty(e,t,i,r);if(s)return s;let n=(0,tN.Eb)(r,a),d=i.getEditingMagnitude(t)??(null===n.value?"":String(n.value)),c=(0,tN.E3)(r,e.default_value,i.getPendingUnit(t),a),p=(0,tN.hX)(a,e.range,[o,(0,tN.Ji)(e.default_value,a),c]),h=(0,tN.x9)(e.default_value,a),u=null!==i.errorAt(t),m=tc(e,i),v=c===o,g=e.range&&v?String(e.range[0]):void 0,f=e.range&&v?String(e.range[1]):void 0,_=e=>i.emitChange(t,(0,tN.BR)(e));return(0,l.qy)`
    <div class="field float-with-unit" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <div class="float-with-unit-inputs">
        <input
          type="number"
          class=${u?"invalid":""}
          .value=${d}
          ?disabled=${m}
          min=${(0,tj.J)(g)}
          max=${(0,tj.J)(f)}
          step="any"
          placeholder=${h}
          @input=${e=>{let a=e.target.value;i.setEditingMagnitude(t,a),""===a&&i.setPendingUnit(t,c);let o=""===a?null:Number(a);_({value:Number.isFinite(o)?o:null,unit:c})}}
          @blur=${()=>i.clearEditingMagnitude(t)}
        />
        ${p.length>1?(0,l.qy)`
              <wa-select
                data-no-value-sync
                ?disabled=${m}
                @change=${e=>{let a=e.target.value;null===n.value?i.setPendingUnit(t,a):_({value:n.value,unit:a})}}
              >
                ${p.map(e=>(0,l.qy)`<wa-option value=${e} ?selected=${e===c}
                      >${e}</wa-option
                    >`)}
              </wa-select>
            `:(0,l.qy)`<span class="float-with-unit-suffix">${c}</span>`}
      </div>
      ${t_(t,i)}
    </div>
  `}(e,t,i);case eI.Hh.TIME_PERIOD:return function(e,t,i){let a=i.getAt(t),o=ty(e,t,i,a);if(o)return o;let r=tV(a),s=null!==i.errorAt(t),n=tc(e,i);if(!r.parseable)return t$(e,"text",t,i);let d=void 0!==e.default_value&&null!==e.default_value?tV(e.default_value):null,c=d&&d.parseable?d.value:"",p=null!=a&&""!==a?r.unit:d?.parseable?d.unit:r.unit;return(0,l.qy)`
    <div class="field time-period" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <div class="time-period-inputs">
        <input
          type="text"
          inputmode="decimal"
          class=${s?"invalid":""}
          .value=${r.value}
          ?disabled=${n}
          placeholder=${c}
          @input=${e=>{let a=e.target.value;i.emitChange(t,tG(a,p))}}
        />
        <wa-select
          data-no-value-sync
          ?disabled=${n}
          @change=${e=>{let a=e.target.value;i.emitChange(t,tG(r.value,a))}}
        >
          ${tU.map(e=>(0,l.qy)`<wa-option value=${e} ?selected=${e===p}
                >${i.localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
      ${t_(t,i)}
    </div>
  `}(e,t,i);case eI.Hh.PIN:return function(e,t,i){if(!i.board||0===i.board.pins.length)return t$(e,"text",t,i);let a=i.getAt(t),o=(0,tT.E7)(a),r=i.board.esphome.platform,s=null!==o?(0,tT.m5)(o,r):(0,eB.k4)(a)?String(a??""):"",n=null!==i.errorAt(t),d=i.board.pins;if(e.suggestions&&e.suggestions.length>0){let t=new Set(e.suggestions.map(tT.E7).filter(e=>null!==e));if(t.size>0){let e=d.filter(e=>t.has(e.gpio));e.length>0&&(d=e)}}null!==o&&!d.some(e=>e.gpio===o)&&i.board.pins.some(e=>e.gpio===o)&&(d=[i.board.pins.find(e=>e.gpio===o),...d]);let c=(0,ed.zq)(i.yaml,i.fromLine,(0,ed.lz)(i.yaml,i.fromLine)),p=tc(e,i),h=(0,eB.Qd)(a);return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <wa-select
        data-no-value-sync
        class=${n?"invalid":""}
        ?disabled=${p}
        @change=${e=>{let a=e.target.value;h?i.emitChange([...t,"number"],a):i.emitChange(t,a)}}
      >
        ${function(e,t,i,a,o){let r=[],s=[],n=[];for(let a of e){let e=function(e,t,i,a){let o=(0,tT.m5)(e.gpio,a.board?.esphome.platform),r=e.label||o,s=e.occupied_by||"",n=i.get(e.gpio)||"",l=(t.pin_mode===eI.l3.OUTPUT||t.pin_mode===eI.l3.INPUT_OUTPUT)&&e.features.includes(eI.k6.INPUT_ONLY),d=(t.pin_features??[]).every(t=>e.features.includes(t)),c=!1===e.available,p=!!(s||n),h=s?a.localize("device.pin_occupied_by",{name:s}):n?a.localize("device.pin_used_by",{name:n}):"",u=l?a.localize("device.pin_input_only"):"",m=e.notes||(c?a.localize("device.pin_unavailable"):""),v=[];return e.label&&e.label!==o&&v.push(o),h&&v.push(h),u&&v.push(u),m&&v.push(m),{optValue:o,primary:r,secondary:v.join(" • "),titleText:[h,u,m].filter(Boolean).join(" — "),warn:p||l,reserved:c,supported:d&&!l}}(a,t,i,o);(e.reserved?n:e.supported?r:s).push(e)}let d=r.length>0&&s.length>0,c=(t.pin_features??[]).map(e=>e.toUpperCase()).join(", "),p=(e,t)=>(0,l.qy)`${t?(0,l.qy)`<wa-divider class="pin-group-divider" aria-hidden="true"></wa-divider>`:l.s6} <small class="pin-group-label" aria-hidden="true">${e}</small>`;return(0,l.qy)`
    ${d&&c?p(o.localize("device.pin_group_supports",{features:c}),!1):l.s6}
    ${r.map(e=>tY(e,a))}
    ${d?p(o.localize("device.pin_group_other"),!0):l.s6}
    ${s.map(e=>tY(e,a))}
    ${n.length>0?p(o.localize("device.pin_group_reserved"),!0):l.s6}
    ${n.map(e=>tY(e,a))}
  `}(d,e,c,s,i)}
      </wa-select>
      ${t_(t,i)}
      ${function(e,t,i,a,o,r){let s=i.filterRenderable(e.config_entries??[],i.scopeValues(t));if(0===s.length)return l.s6;let n=`${t.join(".")}:pin-advanced`,d=i.scopeValues(t);o&&Object.keys(d).some(e=>"number"!==e&&void 0!==d[e])&&i.seedNestedOpen(n);let c=i.nestedOpenSections.has(n);return(0,l.qy)`
    <div
      class="pin-advanced"
      data-field-key="${n}"
      data-reveal-for="${tp(t)}"
    >
      <button
        type="button"
        class="pin-advanced-toggle"
        aria-expanded=${c}
        ?disabled=${r}
        @click=${()=>{!r&&(i.toggleNested(n),c||o||null==a||""===a||i.emitChange(t,{number:a}))}}
      >
        <wa-icon library="mdi" name=${c?"chevron-up":"chevron-down"}></wa-icon>
        <span>${i.localize("device.pin_advanced")}</span>
      </button>
      ${c?(0,l.qy)`<div class="pin-advanced-fields">
            ${s.map(e=>(function(e,t,i){var a,o,r,s,n,l,d,c;let p,h,u,m,v,g,f;if("mode"!==e.key||e.type!==eI.Hh.NESTED)return i.renderEntry(e,[...t,e.key]);let _=[...t,e.key],b=i.getAt(_),y=function(e,t){if(!t||!(0,eB.Qd)(e))return null;for(let i of Object.keys(e))if(Object.prototype.hasOwnProperty.call(t,i)){let e=t[i];return e.length>0?e:null}return null}(i.getAt(t),i.pinRegistryModes),w=y?(o=e,p=new Set([...y,..."string"==typeof(a=b)?Object.keys(tD(a)??{}):(0,eB.Qd)(a)?Object.keys(a):[]]),h=(o.config_entries??[]).filter(e=>p.has(e.key)),{...o,config_entries:h}):e;return"string"==typeof b?(r=w,s=_,(m="string"==typeof(u=(n=i).getAt(s))?tD(u):null)?tI(r,s,(l=n,d=s,c=m,v=d.join("."),g=e=>e.length===d.length+1&&e.slice(0,d.length).join(".")===v?e[d.length]:null,(f={...l,getAt:e=>{if(e.join(".")===v)return c;let t=g(e);return null!==t?c[t]:l.getAt(e)},scopeValues:e=>e.join(".")===v?{...c}:l.scopeValues(e),emitChange:(e,t)=>{let i=g(e);if(null===i)return void l.emitChange(e,t);let a={...c};t?a[i]=!0:delete a[i],l.emitChange(d,a)}}).renderEntry=(e,t)=>e.type===eI.Hh.BOOLEAN?tW(e,t,f):l.renderEntry(e,t),f)):tI(r,s,n)):i.renderEntry(w,_)})(e,t,i))}
          </div>`:l.s6}
    </div>
  `}(e,t,i,a,h,p)}
    </div>
  `}(e,t,i);case eI.Hh.COLOR:return t$(e,"color",t,i);case eI.Hh.MAC_ADDRESS:return t$(e,"text",t,i);case eI.Hh.LAMBDA:return iM(e,t,i);case eI.Hh.JSON:return function(e,t,i){let a=i.getAt(t),o=a instanceof eM.ho;if(!o){let o=ty(e,t,i,a);if(o)return o}let r=o?a.body:String(a??""),s=null!==i.errorAt(t);return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <textarea
        class="textarea-field ${s?"invalid":""}"
        rows="4"
        ?disabled=${tc(e,i)}
        .value=${r}
        placeholder=${String(e.default_value??"")}
        @input=${e=>{let r=e.target.value;i.emitChange(t,o?eM.ho.fromBodyText(r,a):r)}}
      ></textarea>
      ${t_(t,i)}
    </div>
  `}(e,t,i);case eI.Hh.ICON:let o=i.getAt(t),r=ty(e,t,i,o);if(r)return r;let s=String(o??""),n=null!==i.errorAt(t);return(0,l.qy)`
    <div class="field" data-field-key=${tp(t)}>
      ${tf(e,i)}
      <esphome-mdi-icon-picker
        .value=${s}
        .invalid=${n}
        .disabled=${tc(e,i)}
        .placeholder=${String(e.default_value??"Choose an icon…")}
        @change=${e=>i.emitChange(t,e.detail.value)}
      ></esphome-mdi-icon-picker>
      ${t_(t,i)}
    </div>
  `;case eI.Hh.TRIGGER:return(0,l.qy)`<div class="field" data-field-key=${tp(t)}>
          ${tv(e,i)}
          <button
            type="button"
            class="edit-actions-button"
            ?disabled=${i.disabled}
            @click=${()=>this._emitEditActionField(e.key)}
          >
            ${i.localize("device.automation_action_field_edit")}
          </button>
        </div>`;case eI.Hh.UNKNOWN:return tw(e,t,i);default:return t$(e,"text",t,i)}}_buildCtx(){let e={localize:this._localize,disabled:this.disabled,yaml:this.yaml,substitutions:this._parseSubstitutions(this.yaml),fromLine:this.fromLine,sectionKey:this.sectionKey,deviceName:eH(this._devices,this.configuration),board:this.board,pinRegistryModes:this._pinRegistryModes.value,requiredOnly:this.requiredOnly,showAdvanced:this.showAdvanced,presentComponents:this.presentComponents,nestedOpenSections:this._nestedOpenSections,getAt:e=>(0,eB.O6)(this.values,e),errorAt:e=>this.errors.get(e.join("."))??null,emitChange:(e,t)=>this._emitChange(e,t),toggleNested:e=>this._toggleNested(e),seedNestedOpen:e=>this._seedNestedOpen(e),requestAddComponent:e=>this._requestAddComponent(e),resolveInterfaceProviders:e=>this._resolveInterfaceProviders(e),scopeValues:e=>this._scopeValues(e),filterRenderable:this._filterRenderable,getPendingUnit:e=>this._pendingUnits.get(e.join(".")),setPendingUnit:(e,t)=>{this._pendingUnits.set(e.join("."),t),this.requestUpdate()},getEditingMagnitude:e=>this._editingMagnitudes.get(e.join(".")),setEditingMagnitude:(e,t)=>{this._editingMagnitudes.set(e.join("."),t)},clearEditingMagnitude:e=>{this._editingMagnitudes.delete(e.join("."))},stashOwner:this,renderEntry:()=>l.s6};return e.renderEntry=(t,i)=>this._renderEntry(t,i,e),e}_scopeValues(e){let t=(0,eB.O6)(this.values,e);return t&&"object"==typeof t&&!Array.isArray(t)?t:{}}_emitChange(e,t){this.dispatchEvent(new CustomEvent("value-change",{detail:{path:e,value:t},bubbles:!0,composed:!0}))}_emitEditActionField(e){this.dispatchEvent(new CustomEvent("edit-action-field",{detail:{field:e},bubbles:!0,composed:!0}))}_toggleNested(e){let t=new Set(this._nestedOpenSections);t.has(e)?t.delete(e):t.add(e),this._nestedOpenSections=t}openNested(e){if(this.requiredOnly||this._nestedOpenSections.has(e))return;let t=new Set(this._nestedOpenSections);t.add(e),this._nestedOpenSections=t}_seedNestedOpen(e){this.requiredOnly||this._seededNestedOpen.has(e)||(this._seededNestedOpen.add(e),this._nestedOpenSections.add(e))}_requestAddComponent(e){this.dispatchEvent(new CustomEvent("request-add-component",{detail:{domain:e},bubbles:!0,composed:!0}))}_resolveInterfaceProviders(e){if(!e)return[];let t=this._interfaceProviders.get(e);return t||(this._api&&!this._interfaceProvidersPending.has(e)&&(this._interfaceProvidersPending.add(e),this._api.getComponents({provides:e,limit:200}).then(t=>{this._interfaceProviders.set(e,t.components.map(e=>(0,ed.iZ)(e.id))),this.requestUpdate()}).catch(t=>console.warn("[config-entry-form] provider fetch failed for",e,t)).finally(()=>this._interfaceProvidersPending.delete(e))),[])}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._pinRegistryModes=new eQ(this,{getCached:eW,subscribe:eY,fetch:eJ},()=>this._api),this.entries=[],this.values={},this.errors=new Map,this.board=null,this.disabled=!1,this.showAdvanced=!1,this.requiredOnly=!1,this.yaml="",this.sectionKey="",this.configuration="",this.presentComponents=new Set,this._nestedOpenSections=new Set,this._seededNestedOpen=new Set,this._interfaceProviders=new Map,this._interfaceProvidersPending=new Set,this._fieldScroll=new tE(this),this._fieldFocus=new tz(this),this._pendingUnits=new Map,this._editingMagnitudes=new Map,this._filterRenderable=(e,t)=>e6(e,t,e1(this)),this._parseSubstitutions=(0,eU.A)(eX.Gr)}}function iY(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}iW.styles=td,iG([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iW.prototype,"_localize",void 0),iG([(0,s.Fg)({context:u.Ie,subscribe:!0}),(0,d.wk)()],iW.prototype,"_api",void 0),iG([(0,s.Fg)({context:u.xJ,subscribe:!0}),(0,d.wk)()],iW.prototype,"_devices",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"entries",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"values",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"errors",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"board",void 0),iG([(0,d.MZ)({type:Boolean})],iW.prototype,"disabled",void 0),iG([(0,d.MZ)({type:Boolean,attribute:"show-advanced"})],iW.prototype,"showAdvanced",void 0),iG([(0,d.MZ)({type:Boolean,attribute:"required-only"})],iW.prototype,"requiredOnly",void 0),iG([(0,d.MZ)()],iW.prototype,"yaml",void 0),iG([(0,d.MZ)({type:Number,attribute:"from-line"})],iW.prototype,"fromLine",void 0),iG([(0,d.MZ)({attribute:"section-key"})],iW.prototype,"sectionKey",void 0),iG([(0,d.MZ)()],iW.prototype,"configuration",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"presentComponents",void 0),iG([(0,d.MZ)({attribute:!1})],iW.prototype,"focusFieldPath",void 0),iG([(0,d.wk)()],iW.prototype,"_nestedOpenSections",void 0),iW=iG([(0,d.EM)("esphome-config-entry-form")],iW),(0,b.C)({"alert-circle-outline":n.mdiAlertCircleOutline});class iJ extends l.WF{willUpdate(e){super.willUpdate(e),(e.has("component")||!this._initialized)&&this.component&&(this._initialized=!0,this._initValues(),this._localBlockMessage="",this._depResolver.kickoff(this.component.dependencies??[]))}_initValues(){let e=this.component.id.startsWith("featured."),t=this._seedDefaults(this.component.config_entries,e);if(this.component.config_entries.find(e=>"id"===e.key&&e.type===eI.Hh.ID)&&void 0===t.id){let e=this._generateDefaultId();null!==e&&(t={...t,id:e})}if(t=function(e,t,i,a){if(!i?.pins?.length||e.includes("."))return a;let o=a;for(let a of t){if(a.type!==eI.Hh.PIN||void 0!==o[a.key])continue;let t=a.key.toLowerCase().replace(/_(pin|gpio)$/,""),r=`${e}_${t}`,s=i.pins.find(e=>e.features.includes(r));s&&(o={...o,[a.key]:s.gpio})}return o}(this.component.id,this.component.config_entries,this.board,t),this.prefillReference){let e=this._findReferencePath(this.component.config_entries,this.prefillReference.domain,[]);e&&(t=(0,eB.Oe)(t,e,this.prefillReference.id))}this._values=t}_findReferencePath(e,t,i){for(let a of e){if(a.type===eI.Hh.NESTED){let e=this._findReferencePath(a.config_entries??[],t,[...i,a.key]);if(e)return e;continue}if(a.references_component===t)return[...i,a.key]}return null}_seedDefaults(e,t=!1){let i={};for(let a of e){if(a.type===eI.Hh.NESTED){let e=this._seedDefaults(a.config_entries??[],t);Object.keys(e).length>0&&(i[a.key]=e);continue}(t||a.required)&&(null!=a.default_value?i[a.key]=a.multi_value?[String(a.default_value)]:a.default_value:a.multi_value&&a.required&&(i[a.key]=[]))}return i}_generateDefaultId(){return function(e,t,i){if(!t&&!e.includes("."))return null;let a=e.replace(/\./g,"_").toLowerCase(),o=1,r=`${a}_${o}`;for(;i.has(r);)o++,r=`${a}_${o}`;return r}(this.component.id,this.component.multi_conf,function(e){let t=new Set;if(!e)return t;for(let i of e.split("\n")){if(!/^\s/.test(i))continue;let e=(0,x.KJ)(i,"id");null!==e&&t.add(e)}return t}(this.yaml))}render(){let e=this.submitting,t=(0,eM.Zn)(this.yaml),i=(this.component.dependencies??[]).filter(e=>!t.has(e)),a=(0,eN.JK)(this.component.config_entries,this._values,t,this.board?.esphome.platform??null),o=!this._hasRequiredErrors(a);return(0,l.qy)`
      <div class="form">
        <p class="form-desc">${(0,et.G)(this.component.description)}</p>
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
    `}_onAddDep(e){this.dispatchEvent(new CustomEvent("navigate-to-dep",{detail:{domain:e},bubbles:!0,composed:!0}))}_hasRequiredErrors(e){for(let t of e.values())if("validation.required"===t.code)return!0;return!1}_labelForErrorKey(e){let t,i=e.split("."),a=this.component.config_entries;for(let e of i){if(!a||!(t=a.find(t=>t.key===e)))break;a=t.type===eI.Hh.NESTED?t.config_entries??[]:null}return t?tm(t,this._localize):e}_anyErrorIsVisible(e,t){if(0===e.size)return!1;let i=function e(t,i,a,o=[],r=new Set){for(let s of e6(t,i,a)){if(s.type===eI.Hh.NESTED){let t=s.config_entries??[];s.multi_value?(0,eB.ly)(i[s.key]).forEach((i,n)=>{e(t,i,a,[...o,s.key,String(n)],r)}):e(t,(0,eB.qY)(i[s.key]),a,[...o,s.key],r),r.add([...o,s.key].join("."));continue}r.add([...o,s.key].join("."))}return r}(this.component.config_entries,this._values,{requiredOnly:!0,showAdvanced:!1,presentComponents:t,targetPlatform:this.board?.esphome.platform??null});for(let t of e.keys())if(i.has(t))return!0;return!1}_onValueChange(e){let{path:t,value:i}=e.detail;this._values=(0,eB.Oe)(this._values,t,i);let a=t.join(".");if(this._errors.has(a)){let e=new Map(this._errors);e.delete(a),this._errors=e}this._localBlockMessage&&(this._localBlockMessage="")}_generateYamlPreview(){let e=[`${this.component.id}:`];return e.push(...(0,eM.ym)(this._values,"  ")),e.join("\n")}_onCancel(){this.dispatchEvent(new CustomEvent("form-cancel",{bubbles:!0,composed:!0}))}_onSubmit(){this._localBlockMessage="";let e=(0,eM.Zn)(this.yaml),t=(this.component.dependencies??[]).filter(t=>!e.has(t));if(t.length>0){this._localBlockMessage=`${this._localize("device.missing_dependencies_title",{name:this.component.name})} (${t.join(", ")})`;return}let i=(0,eN.JK)(this.component.config_entries,this._values,e,this.board?.esphome.platform??null);if(i.size>0){if(this._errors=i,!this._anyErrorIsVisible(i,e)){let e=[...i.entries()].map(([e,t])=>`${this._labelForErrorKey(e)}: ${this._localize(t.code,t.params)}`).join("; ");this._localBlockMessage=`${this._localize("device.add_component_hidden_validation_error")} (${e})`}return}this._errors=new Map,this._localBlockMessage="";let a=function e(t,i){let a={};for(let o of t){if(o.hidden)continue;let t=i[o.key];if(o.type===eI.Hh.NESTED){let i=null===t||"object"!=typeof t||Array.isArray(t)?{}:t,r=e(o.config_entries??[],i);Object.keys(r).length>0&&(a[o.key]=r);continue}if(void 0!==t){if(Array.isArray(t)){if(0===t.length)continue;a[o.key]=t;continue}if(""===t){o.required&&(a[o.key]=t);continue}if(o.type===eI.Hh.INTEGER&&"hex"!==o.display_format)a[o.key]=(0,eK.s)(t);else if(o.type===eI.Hh.FLOAT){let e="number"==typeof t?t:Number.parseFloat(String(t));Number.isNaN(e)||(a[o.key]=e)}else o.type===eI.Hh.BOOLEAN?a[o.key]=!0===(0,eM.FY)(t):a[o.key]=t}}return a}(this.component.config_entries,this._values);this.dispatchEvent(new CustomEvent("form-submit",{detail:{fields:a},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this.yaml="",this.prefillReference=null,this.submitting=!1,this.submitError="",this._values={},this._errors=new Map,this._localBlockMessage="",this._showYaml=!1,this._depResolver=new ej(this,()=>this._api,()=>this.board?.esphome.platform||void 0),this._initialized=!1}}iJ.styles=[m.G,es.z,eZ],iY([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],iJ.prototype,"_localize",void 0),iY([(0,s.Fg)({context:u.Ie})],iJ.prototype,"_api",void 0),iY([(0,d.MZ)({attribute:!1})],iJ.prototype,"component",void 0),iY([(0,d.MZ)({attribute:!1})],iJ.prototype,"board",void 0),iY([(0,d.MZ)()],iJ.prototype,"yaml",void 0),iY([(0,d.MZ)({attribute:!1})],iJ.prototype,"prefillReference",void 0),iY([(0,d.MZ)({type:Boolean})],iJ.prototype,"submitting",void 0),iY([(0,d.MZ)()],iJ.prototype,"submitError",void 0),iY([(0,d.wk)()],iJ.prototype,"_values",void 0),iY([(0,d.wk)()],iJ.prototype,"_errors",void 0),iY([(0,d.wk)()],iJ.prototype,"_localBlockMessage",void 0),iY([(0,d.wk)()],iJ.prototype,"_showYaml",void 0),iJ=iY([(0,d.EM)("esphome-add-component-form")],iJ);var iQ=i(4996);let iX=new Set(["adc","dac","ota"]);function i0(e){return e?e.split("_").filter(e=>e.length>0).map(e=>iX.has(e.toLowerCase())?e.toUpperCase():e[0].toUpperCase()+e.slice(1)).join(" "):""}function i1(e){let t=e.target;return!t?.closest("a, button")}let i2=(0,l.AH)`
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
`;function i6(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({"arrow-collapse-all":n.mdiArrowCollapseAll,"arrow-expand-all":n.mdiArrowExpandAll,memory:n.mdiMemory,"open-in-new":n.mdiOpenInNew,"package-variant-closed":n.mdiPackageVariantClosed,plus:n.mdiPlus});class i3 extends l.WF{load(){this._provides="";let e=(this.board?.featured_components?.length??0)+(this.board?.featured_bundles?.length??0);0===this.lockedCategories.length&&this.boardId&&e>0?this._category=eP.FEATURED:this._category===eP.FEATURED&&(this._category="all"),this._fetchComponents()}filterByDomain(e){Object.values(eP).includes(e)?(this._search="",this._provides="",this._category=e):(this._search=e,this._provides=e,this._category="all"),this._fetchComponents()}async _fetchComponents(){this._loading=!0;try{let e=this._search.trim()||void 0,t=this.lockedCategories.length>0,i=t?this.lockedCategories:"all"!==this._category?this._category:void 0,a=!t&&this.excludeCategories.length>0?this.excludeCategories:void 0,o={category:i,exclude_category:a,platform:this.platform||void 0,board_id:this.boardId||void 0,limit:50},r=this._provides?await this._api.getComponents({...o,provides:this._provides}):await this._api.getComponents({...o,query:e});this._provides&&0===r.components.length&&(this._provides="",r=await this._api.getComponents({...o,query:e})),this._components=r.components,this._categories=r.categories,this._total=r.total}catch(e){console.error("Failed to load component catalog:",e)}finally{this._loading=!1,this._initialLoad=!1}}render(){var e;let t,i,a,o,r,s,n,d,c,p,h,u,m,v,g;if(this._initialLoad&&this._loading)return(0,l.qy)`<div class="loading">
        ${this._localize("device.loading_components")}
      </div>`;let f=(e=this._localize,t=new Set(this.excludeCategories),a=(i=this._categories.filter(e=>!t.has(e.id))).find(e=>e.id===eP.FEATURED),o=this.board?.featured_bundles?.length??0,r=a?a.count+o:o,s=i.filter(e=>e.id!==eP.FEATURED),n=t.size?s.reduce((e,t)=>e+t.count,0):this._total,d=new Intl.Collator(void 0,{sensitivity:"base"}),c=s.map(e=>({id:e.id,label:i0(e.id),count:e.count})).sort((e,t)=>d.compare(e.label,t.label)),p=[],r>0&&p.push({id:eP.FEATURED,label:e("device.component_category_featured"),count:r}),p.push({id:"all",label:e("device.component_category_all"),count:n}),p.push(...c),p),_=0===this.lockedCategories.length,b=this._category===eP.FEATURED?(h=this.board?.featured_bundles??[],(u=this._search.trim().toLowerCase())?h.filter(e=>e.name.toLowerCase().includes(u)||e.description.toLowerCase().includes(u)||e.id.toLowerCase().includes(u)):h):[],y=(m=this.yaml?(0,eM.Zn)(this.yaml):new Set,v=this.yaml?(0,eM.u)(this.yaml):new Set,g=this.lockedCategories.length>0?new Set(this._components.map(e=>e.id)):null,this._components.filter(e=>{if(!e.multi_conf){if(e.id.includes(".")){if(v.has(e.id))return!1}else if(m.has(e.id))return!1}return(!(g&&e.id.includes("."))||!(e.dependencies.length>0)||!!e.dependencies.every(e=>g.has(e)||m.has(e)))&&!0}));return(0,l.qy)`
      ${_?(0,l.qy)`<div class="sidebar">
            <p class="sidebar-label">${this._localize("device.component_categories")}</p>
            ${f.map(({id:e,label:t,count:i})=>(0,l.qy)`
                <button
                  class="category-btn ${this._category===e?"category-btn--active":""}"
                  type="button"
                  @click=${()=>{this._category=e,this._provides="",this._fetchComponents()}}
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
              >${this._localize("device.components_count",{visible:y.length+b.length,total:this._total+b.length})}</span
            >`:l.s6}
        <div class="grid-scroll">
          <div class="components-grid">
            ${this._loading?(0,l.qy)`<p class="empty">${this._localize("device.loading_components")}</p>`:y.length+b.length?(0,l.qy)`
                    ${b.map(e=>{var t;return t=this,(0,l.qy)`
    <article
      class="component-card component-card--featured"
      @click=${i=>{i1(i)&&t._onAddBundle(e)}}
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
            ${(0,et.G)(e.description)}
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
                    ${y.map(e=>{var t,i,a,o,r;let s,n;return t=this,i=e.id===this._expandedId,a=this._category===eP.FEATURED,o=this._localize,s=!!e.image_url&&!t._imageFailed.has(e.id),n="all"===(r=t._category)||"featured"===r?i0(e.category):"",(0,l.qy)`
    <article
      class="component-card ${i?"component-card--expanded":""} ${a?"component-card--featured":""}"
      @click=${i=>{i1(i)&&t._onAdd(e)}}
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
          ${n?(0,l.qy)`<span class="component-category-chip">${n}</span>`:l.s6}
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
        ${(0,et.G)(e.description)}
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
    `}_onToggleExpand(e){this._expandedId=this._expandedId===e.id?null:e.id}_onImageError(e){if(this._imageFailed.has(e))return;let t=new Set(this._imageFailed);t.add(e),this._imageFailed=t}_onAdd(e){this.dispatchEvent(new CustomEvent("add-component",{detail:{component:e},bubbles:!0,composed:!0}))}_onAddBundle(e){this.dispatchEvent(new CustomEvent("add-bundle",{detail:{bundle:e,boardId:this.boardId},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.platform="",this.boardId="",this.board=null,this.yaml="",this.lockedCategories=[],this.excludeCategories=[],this._components=[],this._categories=[],this._total=0,this._loading=!0,this._initialLoad=!0,this._search="",this._category="all",this._provides="",this._expandedId=null,this._imageFailed=new Set,this._debouncedSearch=(0,iQ.s)(()=>this._fetchComponents(),300),this._onSearchInput=e=>{this._search=e.target.value,this._provides="",this._debouncedSearch()}}}function i4(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}i3.styles=[m.G,es.z,i2],i6([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i3.prototype,"_localize",void 0),i6([(0,s.Fg)({context:u.Ie})],i3.prototype,"_api",void 0),i6([(0,d.MZ)()],i3.prototype,"platform",void 0),i6([(0,d.MZ)({attribute:"board-id"})],i3.prototype,"boardId",void 0),i6([(0,d.MZ)({attribute:!1})],i3.prototype,"board",void 0),i6([(0,d.MZ)()],i3.prototype,"yaml",void 0),i6([(0,d.MZ)({attribute:!1})],i3.prototype,"lockedCategories",void 0),i6([(0,d.MZ)({attribute:!1})],i3.prototype,"excludeCategories",void 0),i6([(0,d.wk)()],i3.prototype,"_components",void 0),i6([(0,d.wk)()],i3.prototype,"_categories",void 0),i6([(0,d.wk)()],i3.prototype,"_total",void 0),i6([(0,d.wk)()],i3.prototype,"_loading",void 0),i6([(0,d.wk)()],i3.prototype,"_initialLoad",void 0),i6([(0,d.wk)()],i3.prototype,"_search",void 0),i6([(0,d.wk)()],i3.prototype,"_category",void 0),i6([(0,d.wk)()],i3.prototype,"_provides",void 0),i6([(0,d.wk)()],i3.prototype,"_expandedId",void 0),i6([(0,d.wk)()],i3.prototype,"_imageFailed",void 0),i3=i6([(0,d.EM)("esphome-component-catalog")],i3),(0,b.C)({close:n.mdiClose,"arrow-left":n.mdiArrowLeft,"package-variant-closed":n.mdiPackageVariantClosed});class i5 extends l.WF{open(){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._open=!0,this.updateComplete.then(()=>this._catalog?.load())}openWithSearch(e){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._open=!0,this.updateComplete.then(()=>this._catalog?.filterByDomain(e))}_resetDetourState(){this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=[],this._bundleProgress=null,this._depNavSeq++,this._selectionSeq++}render(){var e;let t=null!==this._selected,i=this.lockedCategories.length>0,a=i?this.boardName?"device.add_config_dialog_title":"device.add_config":this.boardName?"device.add_component_dialog_title":"device.add_component",o=t?this._selected.name:this.boardName?this._localize(a,{name:this.boardName}):this._localize(a);return(0,l.qy)`
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
          .excludeCategories=${(e={isCoreLocked:i,isInDepDetour:null!==this._returnTo}).isCoreLocked||e.isInDepDetour?[]:eF}
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
    `}async _onComponentSelected(e){e.stopPropagation();let t=await eD(this,e.detail.component.id);if("stale"!==t.kind){if("error"===t.kind){this._submitError=t.message;return}if(this._selected=t.entry,this._submitError="",0===t.entry.config_entries.length){let e=(0,eM.Zn)(this.yaml);(t.entry.dependencies??[]).some(t=>!e.has(t))||await this._submitComponent({},!0)}}}async _onBundleSelected(e){if(e.stopPropagation(),this._submitting)return;let{bundle:t,boardId:i}=e.detail;if(!i||0===t.component_ids.length)return;let a=t.component_ids.map(e=>`featured.${i}.${e}`),[o,...r]=a,s=await eD(this,o,i);if("stale"===s.kind)return;if("error"===s.kind){this._submitError=s.message;return}let n=s.entry;this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=r,this._bundleProgress={current:1,total:a.length,bundleName:t.name},this._selected=n,this._submitError=""}_onBack(){if(!this._submitting){if(this._returnTo){let e=this._returnTo;this._resetDetourState(),this._selected=e,this._submitError="";return}this._resetDetourState(),this._selected=null,this._submitError=""}}_onNavigateToDep(e){return e.stopPropagation(),eR(this,e.detail.domain)}_onFormSubmit(e){return e.stopPropagation(),this._submitComponent(e.detail.fields)}async _submitComponent(e,t=!1){if(this._selected&&this.configuration&&!this._submitting){this._submitting=!0,this._submitError="",this._depNavSeq++;try{let{yaml:a}=await this._api.addComponent(this.configuration,{component_id:this._selected.id,fields:e},this.yaml||void 0);if(this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})),this._returnTo){var i;let t=this._returnTo,a=this._depDomain,o=e.id;a&&"string"==typeof o&&(i=this._selected,i.id===a||i.category===a)?this._prefillReference={domain:a,id:o}:this._prefillReference=null,this._returnTo=null,this._depDomain=null,this._selected=t}else if(this._bundleQueue.length>0&&this._bundleProgress){let t=this._bundleQueue[0],i=this._bundleQueue.slice(1),a=await eD(this,t);if("stale"===a.kind)return;if("error"===a.kind){this._submitError=a.message;return}let o=a.entry,r=e.id,s=this._selected.category;"string"==typeof r&&s?this._prefillReference={domain:s,id:r}:this._prefillReference=null,this._bundleQueue=i,this._bundleProgress={...this._bundleProgress,current:this._bundleProgress.current+1},this._selected=o}else{let i=this._selected.id,o=this._selected.name,r=e.id,s=function(e,t,i){let a=(0,x.MT)(e);if(!t.includes(".")){let e=a.find(e=>e.key===t&&!e.platform);if(e)return{sectionKey:e.key,fromLine:e.fromLine}}let o=a.filter(e=>N(e)===t);if(0===o.length)return null;if(1===o.length)return{sectionKey:N(o[0]),fromLine:o[0].fromLine};if(i){let t=e.split("\n"),a=RegExp(`^\\s+(?:-\\s+)?id:\\s*["']?${i}["']?\\s*$`);for(let e of o)for(let i=e.fromLine-1;i<e.toLine&&i<t.length;i++)if(a.test(t[i]))return{sectionKey:N(e),fromLine:e.fromLine}}let r=o[o.length-1];return{sectionKey:N(r),fromLine:r.fromLine}}(a,i,"string"==typeof r?r:void 0);s&&this.dispatchEvent(new CustomEvent("section-select",{detail:s,bubbles:!0,composed:!0})),this._open=!1,this._selected=null,this._resetDetourState(),t&&c.A.success(this._localize("device.component_added",{name:o}),{richColors:!0})}}catch(e){this._submitError=e instanceof Error?e.message:this._localize("device.add_component_error"),t&&c.A.error(this._submitError,{richColors:!0})}finally{this._submitting=!1}}}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml="",this.lockedCategories=[],this._open=!1,this._selected=null,this._submitting=!1,this._submitError="",this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._bundleQueue=[],this._bundleProgress=null,this._selectionSeq=0,this._depNavSeq=0,this._onRequestClose=()=>{this._open=!1}}}function i8(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}i5.styles=[m.G,(0,eL._)("esphome-base-dialog"),eA.c4,eO],i4([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],i5.prototype,"_localize",void 0),i4([(0,s.Fg)({context:u.Ie})],i5.prototype,"_api",void 0),i4([(0,d.MZ)()],i5.prototype,"boardName",void 0),i4([(0,d.MZ)()],i5.prototype,"configuration",void 0),i4([(0,d.MZ)()],i5.prototype,"platform",void 0),i4([(0,d.MZ)({attribute:!1})],i5.prototype,"board",void 0),i4([(0,d.MZ)()],i5.prototype,"yaml",void 0),i4([(0,d.MZ)({attribute:!1})],i5.prototype,"lockedCategories",void 0),i4([(0,d.wk)()],i5.prototype,"_open",void 0),i4([(0,d.P)("esphome-component-catalog")],i5.prototype,"_catalog",void 0),i4([(0,d.wk)()],i5.prototype,"_selected",void 0),i4([(0,d.wk)()],i5.prototype,"_submitting",void 0),i4([(0,d.wk)()],i5.prototype,"_submitError",void 0),i4([(0,d.wk)()],i5.prototype,"_returnTo",void 0),i4([(0,d.wk)()],i5.prototype,"_depDomain",void 0),i4([(0,d.wk)()],i5.prototype,"_prefillReference",void 0),i4([(0,d.wk)()],i5.prototype,"_bundleQueue",void 0),i4([(0,d.wk)()],i5.prototype,"_bundleProgress",void 0),i5=i4([(0,d.EM)("esphome-add-component-dialog")],i5);class i9 extends l.WF{open(){this._inner.open()}render(){return(0,l.qy)`<esphome-add-component-dialog
      .lockedCategories=${eF}
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .platform=${this.platform}
      .board=${this.board}
      .yaml=${this.yaml}
    ></esphome-add-component-dialog>`}constructor(...e){super(...e),this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml=""}}i8([(0,d.MZ)()],i9.prototype,"boardName",void 0),i8([(0,d.MZ)()],i9.prototype,"configuration",void 0),i8([(0,d.MZ)()],i9.prototype,"platform",void 0),i8([(0,d.MZ)({attribute:!1})],i9.prototype,"board",void 0),i8([(0,d.MZ)()],i9.prototype,"yaml",void 0),i8([(0,d.P)("esphome-add-component-dialog")],i9.prototype,"_inner",void 0),i9=i8([(0,d.EM)("esphome-add-config-dialog")],i9);var i7=i(4103);function ae(e){return e.replace(/[^a-zA-Z0-9_]+/g,"_")}function at(e){for(let t of e)if(t.advanced||t.type===eI.Hh.NESTED&&at(t.config_entries??[]))return!0;return!1}function ai(e,t,i){return(0,l.qy)`<div class="advanced-toggle-row">
    <wa-switch
      .checked=${e}
      @change=${e=>i(e.target.checked)}
    >
      ${t("device.show_advanced")}
    </wa-switch>
  </div>`}let aa=(0,l.AH)`
  /* Add button — used at the bottom of every list. The default is
     a modest dashed affordance for nested lists (then/else inside
     an "if"). The top-level list (wrapped in .ae-section) gets
     the prominent overlay below — that's the primary "Add action"
     / "Add condition" the user reaches for from a fresh
     automation, so it should pop. */
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
`,ao=(0,l.AH)`
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

  /* Bespoke value + unit picker the Delay action uses instead of
     its six separate time-component string inputs. Keeps the user
     in the same "one knob" mental model as the interval form
     (which is a single time_period string). */
  .ae-delay {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }
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
`,ar=(0,l.AH)`
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
`,as=[(0,l.AH)`
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
`,ar,ao,aa];function an(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({close:n.mdiClose,magnify:n.mdiMagnify,plus:n.mdiPlus});class al extends l.WF{open(){this._activeTab="action"===this.kind?"by-target":"by-type",this._query="",this._open=!0}render(){let e="action"===this.kind?this._localize("device.automation_pick_action"):this._localize("device.automation_pick_condition"),t=this._localize("device.automation_pick_search"),i="action"===this.kind?["by-target","by-type","building-blocks"]:["by-type","building-blocks"];return(0,l.qy)`<esphome-base-dialog
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
      </p>`;let t=this.devices.filter(eu).map(t=>{let i=ep(t.component_id),a=e.filter(e=>"domain"in e&&(e.domain===i||e.domain===t.component_id));return{device:t,matching:a}}).filter(e=>e.matching.length>0);return 0===t.length?(0,l.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,l.qy)`${t.map(({device:e,matching:t})=>(0,l.qy)`
        <p class="picker-group-label">
          ${ec(e)}
          <span class="ae-muted">(${eh(e,this.devices)})</span>
        </p>
        ${t.map(t=>this._renderRow(t,()=>this._pick(t.id,this._preFillFor(t,e))))}
      `)}`}_renderByType(e){let t=new Map;for(let i of e){if(!("domain"in i)||"core"===i.domain)continue;let e=ep(i.domain),a=t.get(e)??[];a.push(i),t.set(e,a)}let i=Array.from(t.keys()).sort();return 0===i.length?(0,l.qy)`<p class="picker-empty">
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
              ${(0,et.G)(e.description)}
            </span>`:l.s6}
      </div>
      <span class="picker-row-add" aria-hidden="true">
        <wa-icon library="mdi" name="plus"></wa-icon>
      </span>
    </div>`}_preFillFor(e,t){let i=ep(t.component_id),a=e.config_entries.find(e=>e.references_component===i);if(a)return{[a.key]:t.id}}_pick(e,t){this.dispatchEvent(new CustomEvent("catalog-picked",{detail:{id:e,preFilledParams:t},bubbles:!0,composed:!0})),this._open=!1}constructor(...e){super(...e),this._localize=e=>e,this.kind="action",this.items=[],this.devices=[],this._open=!1,this._activeTab="by-target",this._query="",this._onRequestClose=()=>{this._open=!1}}}function ad(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}al.styles=[m.G,es.z,(0,l.AH)`
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
    `],an([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],al.prototype,"_localize",void 0),an([(0,d.MZ)()],al.prototype,"kind",void 0),an([(0,d.MZ)({attribute:!1})],al.prototype,"items",void 0),an([(0,d.MZ)({attribute:!1})],al.prototype,"devices",void 0),an([(0,d.wk)()],al.prototype,"_open",void 0),an([(0,d.wk)()],al.prototype,"_activeTab",void 0),an([(0,d.wk)()],al.prototype,"_query",void 0),al=an([(0,d.EM)("esphome-catalog-picker-dialog")],al),(0,b.C)({"arrow-down":n.mdiArrowDown,"arrow-up":n.mdiArrowUp,close:n.mdiClose,delete:n.mdiDelete,"pencil-outline":n.mdiPencilOutline,plus:n.mdiPlus});class ac extends l.WF{render(){return(0,l.qy)`
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
          ${i?.description?(0,l.qy)`<p class="ae-row-desc">${(0,et.G)(i.description)}</p>`:l.s6}
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
    `}_openPickerForChange(e){0!==this.catalog.length&&(this._changingIdx=e,this._picker.open())}_onParamChange(e,t){t.stopPropagation();let i=this.conditions[e],a=eg(i.params,t.detail.path,t.detail.value);this._emit(ef(this.conditions,e,{...i,params:a}))}_onChildrenChange(e,t){t.stopPropagation();let i=this.conditions[e];this._emit(ef(this.conditions,e,{...i,children:t.detail.conditions}))}_move(e,t){this._emit(eb(this.conditions,e,t))}_remove(e){this._emit(e_(this.conditions,e))}_emit(e){this.dispatchEvent(new CustomEvent("conditions-change",{detail:{conditions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.conditions=[],this.catalog=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.devices=[],this._changingIdx=-1,this._openPickerForAdd=()=>{0!==this.catalog.length&&(this._changingIdx=-1,this._picker.open())},this._onConditionPicked=e=>{e.stopPropagation();let t={condition_id:e.detail.id,params:{},children:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._changingIdx>=0?this._emit(ef(this.conditions,this._changingIdx,t)):this._emit([...this.conditions,t]),this._changingIdx=-1}}}function ap(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ac.styles=[m.G,es.z,as],ad([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ac.prototype,"_localize",void 0),ad([(0,d.MZ)({attribute:!1})],ac.prototype,"conditions",void 0),ad([(0,d.MZ)({attribute:!1})],ac.prototype,"catalog",void 0),ad([(0,d.MZ)({attribute:!1})],ac.prototype,"board",void 0),ad([(0,d.MZ)()],ac.prototype,"yaml",void 0),ad([(0,d.MZ)({type:Boolean})],ac.prototype,"disabled",void 0),ad([(0,d.MZ)({type:Boolean,attribute:"no-header"})],ac.prototype,"noHeader",void 0),ad([(0,d.MZ)({attribute:!1})],ac.prototype,"devices",void 0),ad([(0,d.P)("esphome-catalog-picker-dialog")],ac.prototype,"_picker",void 0),ad([(0,d.wk)()],ac.prototype,"_changingIdx",void 0),ac=ad([(0,d.EM)("esphome-automation-condition-tree")],ac),(0,b.C)({"arrow-down":n.mdiArrowDown,"arrow-up":n.mdiArrowUp,"chevron-down":n.mdiChevronDown,"chevron-up":n.mdiChevronUp,close:n.mdiClose,delete:n.mdiDelete,"pencil-outline":n.mdiPencilOutline});let ah=["us","ms","s","min","h","d"],au={us:"microseconds",ms:"milliseconds",s:"seconds",min:"minutes",h:"hours",d:"days"};class am extends l.WF{willUpdate(e){if(!e.has("value"))return;let t=e.get("value");t&&t.action_id!==this.value.action_id&&(this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null)}render(){let e=this.catalog.find(e=>e.id===this.value.action_id),t=this._collapsed;return(0,l.qy)`
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
              ${e?.description?(0,l.qy)`<p class="ae-row-desc">${(0,et.G)(e.description)}</p>`:l.s6}
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
    </div>`:l.s6}_nestedListLabel(e){return"else"===e?this._localize("device.automation_else"):"then"===e?this._localize("device.automation_action"):e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}_renderNestedLists(e){return e&&e.accepts_action_list&&0!==e.accepts_action_list.length?e.accepts_action_list.map(e=>(0,l.qy)`<div class="ae-nested">
          <p class="ae-nested-label">${this._nestedListLabel(e)}</p>
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
        </div>`):l.s6}_renderActionParams(e){var t,i;let a;if(!e)return l.s6;if("delay"===e.id)return this._renderDelayParams();if(0===e.config_entries.length)return l.s6;let{showAdvanced:o,showToggle:r}=(t=e.config_entries,i=this._showAdvanced,{showAdvanced:(a=t.length>0&&t.every(e=>e.advanced))||i,showToggle:at(t)&&!a});return(0,l.qy)`<esphome-config-entry-form
        .entries=${e.config_entries}
        .values=${this.value.params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        ?show-advanced=${o}
        @value-change=${this._onParamChange}
      ></esphome-config-entry-form>
      ${r?ai(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}`}_renderDelayParams(){let e=this._delayLambda();return(0,l.qy)`<div class="ae-delay">
      ${tn({isLambda:null!==e,disabled:this.disabled,localize:this._localize,onSwitch:e=>this._toggleDelayLambda(e)})}
      ${e?this._renderDelayLambda(e):this._renderDelayLiteral()}
    </div>`}_renderDelayLiteral(){let{value:e,unit:t}=this._readDelay();return(0,l.qy)`<div class="ae-delay-row">
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
          ${ah.map(e=>(0,l.qy)`<option value=${e} ?selected=${e===t}>
                ${this._localize(`device.automation_action_delay_unit_${e}`)}
              </option>`)}
        </select>
      </div>
    </div>`}_renderDelayLambda(e){return(0,l.qy)`<esphome-lambda-editor
      .value=${iL(e)}
      ?disabled=${this.disabled}
      @lambda-change=${e=>this._writeDelayLambda(e.detail.value)}
    ></esphome-lambda-editor>`}_delayLambda(){let e=(this.value.params??{}).id;return(0,t2.b)(e)?e:null}_toggleDelayLambda(e){if(e!==(null!==this._delayLambda()))if(e)this._delayLiteralStash=this._readDelay(),this._writeDelayLambda(this._delayLambdaStash);else{this._delayLambdaStash=iL(this._delayLambda());let{value:e,unit:t}=this._delayLiteralStash??{value:"",unit:"s"};this._writeDelay(e,t)}}_readDelay(){let e=this.value.params??{};for(let t of ah){let i=e[au[t]];if(void 0!==i&&""!==i&&null!==i)return{value:String(i),unit:t}}let t=e.id;if("string"==typeof t){let e=t.match(/^(\d+(?:\.\d+)?)(us|ms|s|min|h|d)$/);if(e){let[,t,i]=e;return{value:t,unit:i}}}return{value:"",unit:"s"}}_clearedDelayParams(){let e={...this.value.params??{}};for(let t of ah)delete e[au[t]];return delete e.id,e}_writeDelay(e,t){let i=e.trim(),a=this._clearedDelayParams();i&&(a[au[t]]=i),this._emit({...this.value,params:a})}_writeDelayLambda(e){this._delayLambdaStash=e;let t=this._clearedDelayParams();t.id={_lambda:e,_tag:"!lambda"},this._emit({...this.value,params:t})}_patchParams(e){this._emit({...this.value,params:{...this.value.params,...e}})}_onChildrenChange(e,t){let i={...this.value.children??{},[e]:t};this._emit({...this.value,children:i})}_reorder(e){this.dispatchEvent(new CustomEvent("action-reorder",{detail:{delta:e},bubbles:!0,composed:!0}))}_emit(e){this.dispatchEvent(new CustomEvent("action-change",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.first=!1,this.last=!1,this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null,this._openPicker=()=>{this._picker.open()},this._onActionPicked=e=>{e.stopPropagation(),this._emit({action_id:e.detail.id,params:{...e.detail.preFilledParams??{}},children:{},conditions:[]})},this._onParamChange=e=>{e.stopPropagation();let t=eg(this.value.params,e.detail.path,e.detail.value);this._emit({...this.value,params:t})},this._onConditionsChange=e=>{e.stopPropagation(),this._emit({...this.value,conditions:e.detail.conditions})},this._onDelete=()=>{this.dispatchEvent(new CustomEvent("action-delete",{bubbles:!0,composed:!0}))}}}function av(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}am.styles=[m.G,es.z,as,ts],ap([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],am.prototype,"_localize",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"value",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"catalog",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"conditionCatalog",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"scripts",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"devices",void 0),ap([(0,d.MZ)({attribute:!1})],am.prototype,"board",void 0),ap([(0,d.MZ)()],am.prototype,"yaml",void 0),ap([(0,d.MZ)({type:Boolean})],am.prototype,"disabled",void 0),ap([(0,d.MZ)({type:Boolean})],am.prototype,"first",void 0),ap([(0,d.MZ)({type:Boolean})],am.prototype,"last",void 0),ap([(0,d.P)("esphome-catalog-picker-dialog")],am.prototype,"_picker",void 0),ap([(0,d.wk)()],am.prototype,"_collapsed",void 0),ap([(0,d.wk)()],am.prototype,"_showAdvanced",void 0),ap([(0,d.wk)()],am.prototype,"_delayLambdaStash",void 0),ap([(0,d.wk)()],am.prototype,"_delayLiteralStash",void 0),am=ap([(0,d.EM)("esphome-automation-action-node")],am),(0,b.C)({plus:n.mdiPlus});class ag extends l.WF{render(){return(0,l.qy)`
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
    ></esphome-automation-action-node>`}_onActionChange(e,t){t.stopPropagation(),this._emit(ef(this.actions,e,t.detail.value))}_onReorder(e,t){t.stopPropagation(),this._emit(eb(this.actions,e,e+t.detail.delta))}_onDelete(e,t){t.stopPropagation(),this._emit(e_(this.actions,e))}_emit(e){this.dispatchEvent(new CustomEvent("actions-change",{detail:{actions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.actions=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.hideAdd=!1,this.openPicker=()=>{0!==this.catalog.length&&this._picker.open()},this._onActionPicked=e=>{e.stopPropagation();let t={action_id:e.detail.id,params:{},children:{},conditions:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._emit([...this.actions,t])}}}function af(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ag.styles=[m.G,es.z,as],av([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ag.prototype,"_localize",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"actions",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"catalog",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"conditionCatalog",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"scripts",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"devices",void 0),av([(0,d.MZ)({attribute:!1})],ag.prototype,"board",void 0),av([(0,d.MZ)()],ag.prototype,"yaml",void 0),av([(0,d.MZ)({type:Boolean})],ag.prototype,"disabled",void 0),av([(0,d.MZ)({type:Boolean,attribute:"no-header"})],ag.prototype,"noHeader",void 0),av([(0,d.MZ)({type:Boolean,attribute:"hide-add"})],ag.prototype,"hideAdd",void 0),av([(0,d.P)("esphome-catalog-picker-dialog")],ag.prototype,"_picker",void 0),ag=av([(0,d.EM)("esphome-automation-action-list")],ag),(0,b.C)({close:n.mdiClose,plus:n.mdiPlus});let a_=["int","float","bool","string"];class ab extends l.WF{updated(e){if(!e.has("value"))return;let t=this._readFromWire(),i=this._params.filter(e=>e.name);i.length===t.length&&i.every((e,i)=>e.name===t[i].name&&e.type===t[i].type)||(this._params=t)}render(){return(0,l.qy)`<div class="field">
      ${this.fieldLabel?(0,l.qy)`<label class="field-label">${this.fieldLabel}</label>`:l.s6}
      ${this.description?(0,l.qy)`<p class="field-description">${(0,et.G)(this.description)}</p>`:l.s6}
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
        @input=${i=>this._updateRow(t,{...e,name:ae(i.target.value)})}
      />
      <wa-select
        value=${e.type}
        ?disabled=${this.disabled}
        @change=${i=>this._updateRow(t,{...e,type:i.target.value})}
      >
        ${a_.map(t=>(0,l.qy)`<wa-option value=${t} ?selected=${t===e.type}>${t}</wa-option>`)}
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
    </div>`}_readFromWire(){return this.value&&"object"==typeof this.value?Object.entries(this.value).map(([e,t])=>({name:e,type:String(t??"string")})):[]}_emit(e){this._params=e;let t={};for(let{name:i,type:a}of e)i&&(t[i]=a);this.dispatchEvent(new CustomEvent("value-change",{detail:{value:t},bubbles:!0,composed:!0}))}_updateRow(e,t){let i=this._params.slice();i[e]=t,this._emit(i)}_removeRow(e){let t=this._params.slice();t.splice(e,1),this._emit(t)}constructor(...e){super(...e),this._localize=e=>e,this.value={},this.disabled=!1,this.fieldLabel="",this.description="",this.addLabel="",this.namePlaceholder="",this._params=[],this._addRow=()=>{this._emit([...this._params,{name:"",type:"int"}])}}}ab.styles=[m.G,es.z,as],af([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ab.prototype,"_localize",void 0),af([(0,d.MZ)({attribute:!1})],ab.prototype,"value",void 0),af([(0,d.MZ)({type:Boolean})],ab.prototype,"disabled",void 0),af([(0,d.MZ)()],ab.prototype,"fieldLabel",void 0),af([(0,d.MZ)()],ab.prototype,"description",void 0),af([(0,d.MZ)()],ab.prototype,"addLabel",void 0),af([(0,d.MZ)()],ab.prototype,"namePlaceholder",void 0),af([(0,d.wk)()],ab.prototype,"_params",void 0),ab=af([(0,d.EM)("esphome-callable-params-editor")],ab);let ay=["triggers","actions","conditions"];async function aw(e,t,i,a=ay){let o=t5(),r=[],s=(t,a)=>{for(let s of a)r.push(t4(e,t,s,i).then(e=>{t8(o,e)}))};for(let e of(a.includes("triggers")&&s("triggers",t.triggers),a.includes("actions")&&s("actions",t.actions),a.includes("conditions")&&s("conditions",t.conditions),await Promise.allSettled(r)))"rejected"===e.status&&(o.rejected++,console.warn("automation-editor: body fetch failed",e.reason));return o}async function a$(e,t,i){try{let a=await e.getAvailableAutomations(t,i?.yaml);if(i?.isStale?.())return{status:"stale"};let o={...a,triggers:a.triggers.map(e=>({...e})),actions:a.actions.map(e=>({...e})),conditions:a.conditions.map(e=>({...e}))};i?.onPaint?.(o);let r=await aw(e,o,void 0,i?.lists);if(i?.isStale?.())return{status:"stale"};let s={...o,triggers:[...o.triggers],actions:[...o.actions],conditions:[...o.conditions]};return{status:"ok",available:s,hydration:r}}catch(e){if(i?.isStale?.())return{status:"stale"};return{status:"error",error:e}}}class ax{hostDisconnected(){this._seq++}async load(e,t,i,a){if(!e||!t)return{};let o=++this._seq,r=a?.onPaint,s=await a$(e,t,{isStale:()=>o!==this._seq,yaml:a?.yaml,lists:a?.lists??["actions","conditions"],onPaint:r?e=>{o===this._seq&&r(e)}:void 0});return o!==this._seq?{}:function(e,t){if("stale"===e.status)return{};if("error"===e.status)return{error:(0,en.u)(e.error)};let{missingBody:i,missingField:a,rejected:o}=e.hydration,r=i+a+o;return r>0&&c.A.error(t("device.automation_partial_hydration",{count:String(r)}),{richColors:!0}),{available:e.available}}(s,i)}constructor(e){this._seq=0,e.addController(this)}}class ak{hostConnected(){}get active(){return this._active}resolve(e,t,i){let a=ew(t),o=e.find(e=>ew(e.location)===a);return!o||i&&o.location.kind!==i?(this._set(null),null):(this._set(o.error??null,o.unsupported??!1),null!=o.error)?null:{tree:o.automation,location:o.location}}renderPanel(e){return this._unsupported?(0,l.qy)`<div class="ae-empty-block" role="note">
        <p>${e("device.yaml_only_section")}</p>
      </div>`:(0,l.qy)`<div class="ae-empty-block" role="alert">
      <p class="ae-error">${e("device.automation_parse_error")}</p>
      ${this._message?(0,l.qy)`<p>${this._message}</p>`:l.s6}
    </div>`}_set(e,t=!1){let i=null!=e;(this._active!==i||this._message!==(e??"")||this._unsupported!==t)&&(this._active=i,this._message=e??"",this._unsupported=t,this._host.requestUpdate())}constructor(e){this._host=e,this._active=!1,this._message="",this._unsupported=!1,e.addController(this)}}function az(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({delete:n.mdiDelete,"open-in-new":n.mdiOpenInNew,webhook:n.mdiWebhook});let aC=`${i7.I}/components/api.html`;class aE extends l.WF{get dirty(){return this._dirty}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._load(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.action_name!==this.location.action_name&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??ev(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._deleting;return(0,l.qy)`
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
          ${(0,et.G)(this._localize("device.api_action_actions_description"))}
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
        <a class="ae-header-docs" href=${aC} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">
          ${(0,et.G)(this._localize("device.api_action_header_description"))}
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
        ${(0,et.G)(this._localize("device.api_action_id_description"))}
      </p>
      <input
        id="api-action-name"
        type="text"
        .value=${t}
        ?disabled=${e}
        ?readonly=${!this.addMode}
        @input=${e=>this._onActionNameChange(e.target.value)}
      />
    </div>`}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable()}catch(e){this._error=(0,en.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"api_action");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_onActionNameChange(e){let t=ae(e);t&&(this.location={kind:"api_action",action_name:t},this._scheduleAutoApply())}_withValue(e){let t={...this.value??ev(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this.location.action_name){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=e$(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new ak(this),this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._catalogLoad=new ax(this),this._dirty=!1,this._onVariablesChange=e=>{e.stopPropagation();let t=this.value??ev();this._withValue({trigger_params:{...t.trigger_params,variables:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=e$(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}function aq(e,t){let i=((e.endsWith("_action")?e.slice(0,-7):e)||e).replace(/_/g," ").trim()||"action";return t("device.action_field_label",{name:i[0].toUpperCase()+i.slice(1)})}function aS(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aE.styles=[m.G,es.z,as],az([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aE.prototype,"_localize",void 0),az([(0,s.Fg)({context:u.Ie})],aE.prototype,"_api",void 0),az([(0,d.MZ)()],aE.prototype,"configuration",void 0),az([(0,d.MZ)({attribute:!1})],aE.prototype,"board",void 0),az([(0,d.MZ)()],aE.prototype,"platform",void 0),az([(0,d.MZ)({attribute:!1})],aE.prototype,"value",void 0),az([(0,d.MZ)({attribute:!1})],aE.prototype,"location",void 0),az([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],aE.prototype,"addMode",void 0),az([(0,d.MZ)()],aE.prototype,"yaml",void 0),az([(0,d.wk)()],aE.prototype,"_available",void 0),az([(0,d.wk)()],aE.prototype,"_loading",void 0),az([(0,d.wk)()],aE.prototype,"_deleting",void 0),az([(0,d.wk)()],aE.prototype,"_error",void 0),az([(0,d.wk)()],aE.prototype,"_dirty",void 0),aE=az([(0,d.EM)("esphome-api-action-editor")],aE);let aA=["device_on","component_on","interval","script"];class aL extends l.WF{render(){let e=this.value&&"component_action"!==this.value.kind?this.value.kind:"device_on";return(0,l.qy)`
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
          ${aA.map(t=>(0,l.qy)`<wa-option value=${t} ?selected=${t===e}
                >${this._kindLabel(t)}</wa-option
              >`)}
        </wa-select>
        ${this._renderKindBody(e)}
      </div>
    `}_kindLabel(e){switch(e){case"device_on":return this._localize("device.automation_target_device");case"component_on":return this._localize("device.automation_target_component");case"interval":return this._localize("device.automation_target_interval");case"script":return this._localize("device.automation_target_script");case"api_action":return this._localize("device.automation_target_api_action");case"light_effect":return this._localize("device.automation_light_effect")}}_renderKindBody(e){if("device_on"===e||"interval"===e)return l.s6;if("component_on"===e){let e=this.value?.kind==="component_on"?this.value.component_id:"",t=this.devices.filter(eu);return 0===t.length?(0,l.qy)`<p class="ae-empty" role="status">
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
          ${t.map(t=>(0,l.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${ec(t)}
                <span class="ae-muted"
                  >(${eh(t,this.devices)})</span
                ></wa-option
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
                >${ec(t)}</wa-option
              >`)}
        </wa-select>
      `}return l.s6}_onKindChange(e){let t=e.target.value,i=(()=>{switch(t){case"device_on":return{kind:t,trigger:"on_boot"};case"interval":return{kind:t,index:0};case"component_on":{let e=this.devices.find(eu);return e?{kind:t,component_id:e.id,trigger:""}:null}case"script":return{kind:t,id:this.scripts.length?this.scripts[0].id:""};case"light_effect":{let e=this.devices.find(e=>e.component_id.startsWith("light."));return e?{kind:t,component_id:e.id,index:0}:null}case"api_action":return null}})();this._emit(i)}_onComponentChange(e){this.value?.kind==="component_on"&&this._emit({...this.value,component_id:e})}_onScriptChange(e){this._emit({kind:"script",id:e})}_onLightChange(e){this.value?.kind==="light_effect"&&this._emit({...this.value,component_id:e})}_emit(e){this.dispatchEvent(new CustomEvent("target-change",{detail:{target:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value=null,this.devices=[],this.scripts=[],this.disabled=!1,this.locked=!1}}function aM(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aL.styles=[m.G,es.z,as],aS([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aL.prototype,"_localize",void 0),aS([(0,d.MZ)({attribute:!1})],aL.prototype,"value",void 0),aS([(0,d.MZ)({attribute:!1})],aL.prototype,"devices",void 0),aS([(0,d.MZ)({attribute:!1})],aL.prototype,"scripts",void 0),aS([(0,d.MZ)({type:Boolean})],aL.prototype,"disabled",void 0),aS([(0,d.MZ)({type:Boolean})],aL.prototype,"locked",void 0),aL=aS([(0,d.EM)("esphome-automation-target-picker")],aL);class aP extends l.WF{render(){if(!this.target)return(0,l.qy)`<p class="ae-empty">
        ${this._localize("device.automation_target_placeholder")}
      </p>`;if("interval"===this.target.kind||"script"===this.target.kind||"api_action"===this.target.kind||"light_effect"===this.target.kind)return l.s6;let e=this._filteredTriggers(),t=e.find(e=>e.id===this.triggerId),i="component_on"===this.target.kind?this.target.component_id:null,a=i?this.devices.find(e=>e.id===i)??null:null;return(0,l.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="trigger-label"
          >${this._localize("device.automation_trigger")}</label
        >
        ${a?(0,l.qy)`<p class="ae-section-desc">
              ${this._localize("device.automation_trigger_on_component",{component:ec(a),domain:a.component_id})}
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
        ${t?.description?(0,l.qy)`<p class="ae-section-desc">${(0,et.G)(t.description)}</p>`:l.s6}
        ${t&&t.config_entries.length>0?(0,l.qy)`<esphome-config-entry-form
              .entries=${t.config_entries}
              .values=${this.triggerParams}
              .board=${this.board}
              .yaml=${this.yaml}
              ?disabled=${this.disabled}
              @value-change=${this._onParamChange}
            ></esphome-config-entry-form>`:l.s6}
      </div>
    `}_filteredTriggers(){if(!this.target)return[];if("device_on"===this.target.kind)return this.triggers.filter(e=>e.is_device_level);if("component_on"===this.target.kind){let e=this.target.component_id,t=this.devices.find(t=>t.id===e);return em(this.triggers,t)}return[]}constructor(...e){super(...e),this._localize=e=>e,this.target=null,this.triggers=[],this.devices=[],this.triggerId=null,this.triggerParams={},this.board=null,this.yaml="",this.disabled=!1,this._onTriggerChange=e=>{let t=e.target.value;this.dispatchEvent(new CustomEvent("trigger-change",{detail:{triggerId:t,params:{}},bubbles:!0,composed:!0}))},this._onParamChange=e=>{e.stopPropagation();let t=eg(this.triggerParams,e.detail.path,e.detail.value);this.dispatchEvent(new CustomEvent("trigger-params-change",{detail:{params:t},bubbles:!0,composed:!0}))}}}function aF(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aP.styles=[m.G,es.z,as],aM([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aP.prototype,"_localize",void 0),aM([(0,d.MZ)({attribute:!1})],aP.prototype,"target",void 0),aM([(0,d.MZ)({attribute:!1})],aP.prototype,"triggers",void 0),aM([(0,d.MZ)({attribute:!1})],aP.prototype,"devices",void 0),aM([(0,d.MZ)()],aP.prototype,"triggerId",void 0),aM([(0,d.MZ)({attribute:!1})],aP.prototype,"triggerParams",void 0),aM([(0,d.MZ)({attribute:!1})],aP.prototype,"board",void 0),aM([(0,d.MZ)()],aP.prototype,"yaml",void 0),aM([(0,d.MZ)({type:Boolean})],aP.prototype,"disabled",void 0),aP=aM([(0,d.EM)("esphome-automation-trigger-picker")],aP),(0,b.C)({"arrow-decision-outline":n.mdiArrowDecisionOutline,delete:n.mdiDelete,"open-in-new":n.mdiOpenInNew});class aT extends l.WF{get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._editMode=!this.addMode,this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&ew(t)!==ew(this.location)&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend(),(e.has("location")||e.has("platform"))&&this.location?.kind==="interval"&&this._loadIntervalComponent()}async _loadIntervalComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,eT.CQ)("interval",e,t);if(i){this._intervalComponent=i;return}try{let i=await (0,eT.Sn)(this._api,"interval",e,t);i&&(this._intervalComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml);this._error="";let t=this._parseError.resolve(e,this.location);t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}async _loadAvailable(){if(!this._api||!this.configuration)return;this._loading=!0,this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize,{lists:["triggers","actions","conditions"],yaml:this.yaml,onPaint:e=>{this._available=e,this._loading=!1}});void 0!==t&&(this._error=t,this._loading=!1),e&&(this._available=e,this._loading=!1)}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??ev(),t=this.location,i=this._available?.devices??[],a=this._available?.scripts??[],o=this._available?.triggers??[],r=this._available?.actions??[],s=this._available?.conditions??[],n=this._deleting,d=e.trigger_id??(t?.kind==="device_on"?t.trigger||null:t?.kind==="component_on"&&this._catalogIdFor(t)||null),c=d?o.find(e=>e.id===d)??null:null;return(0,l.qy)`
      ${this._renderHeader(c)}
      ${this.addMode?this._renderAddModePickers(t,o,i,a,d,e,n):(0,l.qy)`${this._renderIdentityFields(c)}${this._renderTriggerParamsForm(c,e,n)}`}
      <div class="field">
        <div class="ae-actions-header">
          <label class="field-label">
            ${this._localize("device.automation_action")}
          </label>
          <button
            type="button"
            class="ae-section-add"
            ?disabled=${n||0===r.length}
            @click=${()=>this._actionList?.openPicker()}
          >
            <wa-icon library="mdi" name="plus"></wa-icon>
            ${this._localize("device.add_action")}
          </button>
        </div>
        <p class="field-description">
          ${(0,et.G)(this._localize("device.automation_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          hide-add
          .actions=${e.actions}
          .catalog=${r}
          .conditionCatalog=${s}
          .scripts=${a}
          .devices=${i}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${n}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,l.qy)`<p class="ae-error" role="alert">${this._error}</p>`:l.s6}
      ${this.location&&this.value&&!this.addMode?(0,l.qy)`<div class="ae-actions">
            <button
              type="button"
              class="ae-danger"
              ?disabled=${n}
              @click=${this._onDelete}
            >
              <wa-icon library="mdi" name="delete"></wa-icon>
              ${this._localize("device.delete_automation")}
            </button>
          </div>`:l.s6}
    `}_renderTriggerParamsForm(e,t,i){let a=this._paramFormEntries(e);if(0===a.length)return l.s6;let o=at(a);return(0,l.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${t.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${i}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onTriggerParamsValueChange}
      ></esphome-config-entry-form>
      ${o?ai(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}
    `}_paramFormEntries(e){if(this.location?.kind==="interval"){let e=this._intervalComponent;return e?e.config_entries.filter(e=>"then"!==e.key):[]}return e?.config_entries??[]}_renderAddModePickers(e,t,i,a,o,r,s){return(0,l.qy)`
      <esphome-automation-target-picker
        .value=${e}
        .devices=${i}
        .scripts=${a}
        ?disabled=${s}
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
        ?disabled=${s}
        @trigger-change=${this._onTriggerChange}
        @trigger-params-change=${this._onTriggerParamsChange}
      ></esphome-automation-trigger-picker>
    `}_applyParamPatch(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a,...o]=t;if(0===o.length){if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}let r=e[a]&&"object"==typeof e[a]&&!Array.isArray(e[a])?e[a]:{};return{...e,[a]:this._applyParamPatch(r,o,i)}}_renderHeader(e){let t=this.location,i=t?.kind==="interval"?this._intervalComponent:null,a=i?.name??this._headerTitle(e),o=i?.docs_url??e?.docs_url??"",r=i?.description??e?.description??this._localize("device.automation_header_description"),s=i?.image_url??"";return(0,l.qy)`<div class="ae-header">
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
        <p class="ae-header-desc">${(0,et.G)(r)}</p>
      </div>
      <div class="ae-header-icon">
        ${s?(0,l.qy)`<img alt="" src=${s} />`:(0,l.qy)`<wa-icon library="mdi" name="arrow-decision-outline"></wa-icon>`}
      </div>
    </div>`}_headerTitle(e){let t=this.location;return t?.kind==="interval"?this._localize("device.automation_interval_label"):e&&(t?.kind==="device_on"||t?.kind==="component_on")?e.name:t?.kind==="component_action"?aq(t.field,this._localize):this._localize("device.automation_header_title_static")}_renderIdentityFields(e){let t=this.location;if(!t||"component_on"!==t.kind&&"component_action"!==t.kind)return l.s6;let i=this._targetMetadataValue(t);return(0,l.qy)`<div class="field">
      <label class="field-label"> ${this._localize("device.automation_target")} </label>
      <input type="text" readonly .value=${i} />
    </div>`}_targetMetadataValue(e){switch(e.kind){case"device_on":return this._localize("device.automation_target_device");case"component_on":case"component_action":{let t=this._available?.devices.find(t=>t.id===e.component_id);if(!t)return e.component_id;return`${ec(t)} (${t.component_id})`}case"interval":return this._localize("device.automation_target_interval_n",{index:e.index+1});case"script":return e.id;case"api_action":return e.action_name;case"light_effect":return e.component_id}}_withValue(e){let t={...this.value??ev(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=e$(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}_bareTriggerKey(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_catalogIdFor(e){if("component_on"!==e.kind||!e.trigger)return null;let t=this._available?.devices.find(t=>t.id===e.component_id),i=t?ep(t.component_id):null;return i?`${i}.${e.trigger}`:e.trigger}static get _actionStyles(){return null}get _devicesForTest(){return this._available?.devices??[]}get _scriptsForTest(){return this._available?.scripts??[]}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._intervalComponent=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new ak(this),this._catalogLoad=new ax(this),this._showAdvanced=!1,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._editMode=!1,this._onTriggerParamsValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=this.value??ev(),o=this._applyParamPatch(a.trigger_params,t,i);this._withValue({trigger_params:o})},this._onTargetChange=e=>{e.stopPropagation(),this.location=e.detail.target,this._withValue({trigger_id:null,trigger_params:{}})},this._onTriggerChange=e=>{if(e.stopPropagation(),this._withValue({trigger_id:e.detail.triggerId,trigger_params:e.detail.params}),this.location?.kind==="device_on")this.location={...this.location,trigger:e.detail.triggerId};else if(this.location?.kind==="component_on"){let t=this._bareTriggerKey(e.detail.triggerId);this.location={...this.location,trigger:t}}},this._onTriggerParamsChange=e=>{e.stopPropagation(),this._withValue({trigger_params:e.detail.params})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=e$(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}function aR(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aT.styles=[m.G,es.z,as],aF([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aT.prototype,"_localize",void 0),aF([(0,s.Fg)({context:u.Ie})],aT.prototype,"_api",void 0),aF([(0,d.MZ)()],aT.prototype,"configuration",void 0),aF([(0,d.MZ)({attribute:!1})],aT.prototype,"board",void 0),aF([(0,d.MZ)()],aT.prototype,"platform",void 0),aF([(0,d.MZ)({attribute:!1})],aT.prototype,"value",void 0),aF([(0,d.MZ)({attribute:!1})],aT.prototype,"location",void 0),aF([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],aT.prototype,"addMode",void 0),aF([(0,d.MZ)()],aT.prototype,"yaml",void 0),aF([(0,d.P)("esphome-automation-action-list")],aT.prototype,"_actionList",void 0),aF([(0,d.wk)()],aT.prototype,"_available",void 0),aF([(0,d.wk)()],aT.prototype,"_intervalComponent",void 0),aF([(0,d.wk)()],aT.prototype,"_loading",void 0),aF([(0,d.wk)()],aT.prototype,"_deleting",void 0),aF([(0,d.wk)()],aT.prototype,"_error",void 0),aF([(0,d.wk)()],aT.prototype,"_showAdvanced",void 0),aF([(0,d.wk)()],aT.prototype,"_dirty",void 0),aF([(0,d.wk)()],aT.prototype,"_editMode",void 0),aT=aF([(0,d.EM)("esphome-automation-editor")],aT),(0,b.C)({delete:n.mdiDelete,"open-in-new":n.mdiOpenInNew,"script-text-outline":n.mdiScriptTextOutline});class aD extends l.WF{get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}get inFlightWrite(){return this._deleting||this._applyInFlight}connectedCallback(){super.connectedCallback(),this._load(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.id!==this.location.id&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable(),this._loadScriptComponent()}catch(e){this._error=(0,en.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _loadScriptComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,eT.CQ)("script",e,t);if(i){this._scriptComponent=i;return}try{let i=await (0,eT.Sn)(this._api,"script",e,t);i&&(this._scriptComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"script");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=e instanceof Error?e.message:this._localize("device.automation_parse_error")}}reload(){this.addMode||!this.location||this._applyInFlight||this.yaml!==this._lastSelfWrittenYaml&&this._hydrateFromBackend()}render(){if(this._loading)return(0,l.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??ev(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._deleting;return(0,l.qy)`
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
          ${(0,et.G)(this._localize("device.script_actions_description"))}
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
    `}_renderHeader(){let e=this._scriptComponent,t=e?.name??this._localize("device.script_header_title_static"),i=e?.description??this._localize("device.script_header_description"),a=e?.docs_url??`${i7.I}/components/script.html`,o=e?.image_url??"";return(0,l.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${t}</h2>
        <a class="ae-header-docs" href=${a} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">${(0,et.G)(i)}</p>
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
    `}_renderAdvancedToggle(e){return at(e)||this._hasParametersEntry()?ai(this._showAdvanced,this._localize,e=>{this._showAdvanced=e}):l.s6}_hasParametersEntry(){return this._scriptComponent?.config_entries.some(e=>"parameters"===e.key)??!1}_patchParams(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a]=t;if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}_renderParametersField(e,t){let i=e.trigger_params.parameters??{};return(0,l.qy)`<esphome-callable-params-editor
      .value=${i}
      ?disabled=${t}
      .fieldLabel=${this._localize("device.automation_script_parameters")}
      .description=${this._localize("device.script_parameters_description")}
      .addLabel=${this._localize("device.script_add_parameter")}
      .namePlaceholder=${this._localize("device.script_parameter_name_placeholder")}
      @value-change=${this._onParametersChange}
    ></esphome-callable-params-editor>`}_withValue(e){let t={...this.value??ev(),...e};this.value=t,this.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this.location},bubbles:!0,composed:!0})),this._scheduleAutoApply()}_scheduleAutoApply(){this.addMode||this._parseError.active||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this._autoApply()},200))}async _autoApply(){if(this._api&&this.location&&this.value){if(this._parseError.active)return void this._setDirty(!1);if(this.location.id){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:e}=await this._api.upsertAutomation(this.configuration,this.value,this.location,this.yaml),t=e$(this.yaml,e);this._lastSelfWrittenYaml=t,this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this._autoApply()):this._setDirty(!1)}}}}async flushPending(){if(this._applyTimer)clearTimeout(this._applyTimer),this._applyTimer=null,await this._autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._deleting=!1,this._error="",this._parseError=new ak(this),this._scriptComponent=null,this._showAdvanced=!1,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._catalogLoad=new ax(this),this._dirty=!1,this._onConfigFormValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=this.value??ev(),o=1===t.length&&"id"===t[0]?ae(String(i??"")):i,r=this._patchParams(a.trigger_params,t,o);if(1===t.length&&"id"===t[0]){let e=String(o??"");e&&(this.location={kind:"script",id:e})}this._withValue({trigger_params:r})},this._onParametersChange=e=>{e.stopPropagation();let t=this.value??ev();this._withValue({trigger_params:{...t.trigger_params,parameters:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._withValue({actions:e.detail.actions})},this._onDelete=async()=>{if(this._api&&this.location&&!this._deleting){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null),this._deleting=!0,this._error="";try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,this.location,this.yaml),t=e$(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deleting=!1}}}}}aD.styles=[m.G,es.z,as],aR([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aD.prototype,"_localize",void 0),aR([(0,s.Fg)({context:u.Ie})],aD.prototype,"_api",void 0),aR([(0,d.MZ)()],aD.prototype,"configuration",void 0),aR([(0,d.MZ)({attribute:!1})],aD.prototype,"board",void 0),aR([(0,d.MZ)()],aD.prototype,"platform",void 0),aR([(0,d.MZ)({attribute:!1})],aD.prototype,"value",void 0),aR([(0,d.MZ)({attribute:!1})],aD.prototype,"location",void 0),aR([(0,d.MZ)({type:Boolean,attribute:"add-mode"})],aD.prototype,"addMode",void 0),aR([(0,d.MZ)()],aD.prototype,"yaml",void 0),aR([(0,d.P)("esphome-automation-action-list")],aD.prototype,"_actionList",void 0),aR([(0,d.wk)()],aD.prototype,"_available",void 0),aR([(0,d.wk)()],aD.prototype,"_loading",void 0),aR([(0,d.wk)()],aD.prototype,"_deleting",void 0),aR([(0,d.wk)()],aD.prototype,"_error",void 0),aR([(0,d.wk)()],aD.prototype,"_scriptComponent",void 0),aR([(0,d.wk)()],aD.prototype,"_showAdvanced",void 0),aR([(0,d.wk)()],aD.prototype,"_dirty",void 0),aD=aR([(0,d.EM)("esphome-script-editor")],aD);let aO=(0,l.AH)`
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
    padding: var(--esphome-button-padding);
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
`;function aI(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}class aj extends l.WF{open(){this._open=!0}close(){this._open=!1}render(){return(0,l.qy)`
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
          src=${(0,ee.Ru)(e)}
          alt=${e.name}
          referrerpolicy="no-referrer"
          @error=${ee.jt}
        />
        <div class="board-meta">
          <span class="board-name">${e.name}</span>
          ${e.manufacturer?(0,l.qy)`<span class="board-mfr">${e.manufacturer}</span>`:l.s6}
        </div>
        ${e.is_generic?(0,l.qy)`<wa-badge variant="neutral" pill
              >${this._localize("device.change_board_generic_tag")}</wa-badge
            >`:l.s6}
      </button>
    `}_select(e){this.close(),this.dispatchEvent(new CustomEvent("select-board",{detail:{boardId:e.id},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.currentBoard=null,this.boards=[],this._open=!1,this._onRequestClose=()=>{this._open=!1}}}aj.styles=[m.G,eA.dC,eA.rG,aO],aI([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aj.prototype,"_localize",void 0),aI([(0,d.MZ)({attribute:!1})],aj.prototype,"currentBoard",void 0),aI([(0,d.MZ)({attribute:!1})],aj.prototype,"boards",void 0),aI([(0,d.wk)()],aj.prototype,"_open",void 0),aj=aI([(0,d.EM)("esphome-change-board-dialog")],aj);class aN{hostConnected(){this._unsubscribe=is(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}ensure(){let{api:e,platform:t,boardId:i}=this._context();e&&void 0===ie(t,i)&&t7.triggers.fetch(e,t,i).catch(()=>{})}resolveName(e,t,i){let{platform:a,boardId:o}=this._context(),r=ie(a,o);if(!r)return i;let s="esphome"===e?t:`${e}.${t}`;return r.find(e=>e.id===s)?.name||i}hasTriggersFor(e){let{platform:t,boardId:i}=this._context(),a=ie(t,i);return!a||a.some(t=>t.applies_to.some(t=>e.includes(t)))}constructor(e,t){this._host=e,this._context=t,e.addController(this)}}var aB=i(383);function aK(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({close:n.mdiClose});class aZ extends l.WF{open(){this._name="",this._error="",this._open=!0}render(){let e=this.boardName?this._localize("device.add_api_action_dialog_title",{name:this.boardName}):this._localize("device.add_api_action");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._onRequestClose}
    >
      <p class="intro">
        ${(0,et.G)(this._localize("device.api_action_header_description"))}
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
          @input=${e=>{this._name=ae(e.target.value),this._error=""}}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._name&&!E(this.yaml).some(e=>e.key===`automation:api_action:${this._name}`)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._name="",this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"api_action",action_name:this._name},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{},actions:[]},e,this.yaml),i=e$(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:ew(e)},bubbles:!0,composed:!0})),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}aZ.styles=[m.G,es.z,(0,l.AH)`
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
    `],aK([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],aZ.prototype,"_localize",void 0),aK([(0,s.Fg)({context:u.Ie})],aZ.prototype,"_api",void 0),aK([(0,d.MZ)()],aZ.prototype,"boardName",void 0),aK([(0,d.MZ)()],aZ.prototype,"configuration",void 0),aK([(0,d.MZ)()],aZ.prototype,"yaml",void 0),aK([(0,d.MZ)({attribute:!1})],aZ.prototype,"board",void 0),aK([(0,d.wk)()],aZ.prototype,"_open",void 0),aK([(0,d.wk)()],aZ.prototype,"_name",void 0),aK([(0,d.wk)()],aZ.prototype,"_saving",void 0),aK([(0,d.wk)()],aZ.prototype,"_error",void 0),aZ=aK([(0,d.EM)("esphome-add-api-action-dialog")],aZ);let aU=(0,l.AH)`
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
`;function aH(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({plus:n.mdiPlus,pencil:n.mdiPencil,delete:n.mdiDelete});class aV extends l.WF{render(){if(0===this.rows.length&&void 0===this.addLabel)return l.s6;let e=""!==this.busyKey;return(0,l.qy)`<div class="list">
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
    </div>`}_emit(e,t){this.dispatchEvent(new CustomEvent(e,{detail:{key:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this.heading="",this.rows=[],this.busyKey="",this.editLabel="",this.deleteLabel="",this._onAdd=()=>{this.dispatchEvent(new CustomEvent("add",{bubbles:!0,composed:!0}))}}}aV.styles=[m.G,aU],aH([(0,d.MZ)()],aV.prototype,"heading",void 0),aH([(0,d.MZ)({attribute:!1})],aV.prototype,"rows",void 0),aH([(0,d.MZ)({attribute:"add-label"})],aV.prototype,"addLabel",void 0),aH([(0,d.MZ)({attribute:"empty-text"})],aV.prototype,"emptyText",void 0),aH([(0,d.MZ)({attribute:"busy-key"})],aV.prototype,"busyKey",void 0),aH([(0,d.MZ)({attribute:"edit-label"})],aV.prototype,"editLabel",void 0),aH([(0,d.MZ)({attribute:"delete-label"})],aV.prototype,"deleteLabel",void 0),aV=aH([(0,d.EM)("esphome-section-automation-list")],aV);let aG=(0,l.AH)`
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
`;i(3983);let aW=e=>"!lambda"===e.tag&&"|-"===e.marker,aY=e=>({_lambda:new eM.ho(e).body.replace(/\n+$/,""),_tag:"!lambda"}),aJ=(e,t,i)=>aW(e)?aY(i):new eM.ho(i,t),aQ=(e,t)=>{if(e.includes(".")||(0,$.CI)(t))return null;if(""===t)return{key:e,value:null};let{value:i}=(0,e5.bw)(t);return i.startsWith("[")&&i.endsWith("]")?{key:e,value:(0,e5.Wg)(i)}:{key:e,value:(0,e5.Qj)(t)}},aX=(e,t)=>{let i=e.match(t);return i?aQ(i[1],i[2].trim()):null},a0=(e,t,i)=>{let a=!1;for(let o=t;o<e.length;o++){let t=e[o];if(!(0,$.BJ)(t)){if((0,$.PM)(t,i.length))return{endIdx:o,isComplex:a};!a&&($.PL.test(t)||$.uT.test(t)||$.Vi.test(t))&&(a=!0)}}return{endIdx:e.length,isComplex:a}},a1=(e,t,i)=>{let{dashIndent:a,firstDashIdx:o}=((e,t,i)=>{let a=t;for(;a<e.length&&(0,$.BJ)(e[a]);)a++;return a>=e.length?{dashIndent:i,firstDashIdx:a}:{dashIndent:e[a].match(/^( *)-/)?.[1]??i,firstDashIdx:a}})(e,t,`${i}  `),r=(0,$.G5)(e,o+1,a)??`${a}  `,{endIdx:s,isComplex:n}=a0(e,t,i);if(n){let i=a2(e,t,a,r);return i?{value:i.items,endIdx:i.endIdx,isEmptyScalarList:!1}:{value:new eM.ho(e.slice(t,s)),endIdx:s,isEmptyScalarList:!1}}let{items:l,endIdx:d}=((e,t,i,a)=>{let o=[],r=t;for(;r<e.length;r++){if((0,$.BJ)(e[r]))continue;if(!e[r].startsWith(i))break;let t=e[r].match(a);if(!t)break;o.push((0,e5.Ir)(t[1].trim()))}return{items:o,endIdx:r}})(e,t,`${a}- `,(0,$.iu)(a));return{value:l,endIdx:d,isEmptyScalarList:0===l.length}},a2=(e,t,i,a)=>{let o=RegExp(`^${i}-\\s+(${$.bn}):\\s*(.*)$`),r=RegExp(`^${a}(${$.bn}):\\s*(.*)$`),s=t=>{let s=Object.create(null),n=null;if(!$.Vi.test(e[t])){let a=e[t].match(o);if(!a)return null;let r=a[1],l=a[2].trim(),d=(0,$.CI)(l);if(d){if(!aW(d))return null;let{endIdx:a}=a0(e,t+1,`${i}  `),o=(0,$.K7)(e,a);return o<e.length&&(0,$.MG)(e[o]).length>i.length?null:(s[r]=aY(e.slice(t+1,a)),{item:s,endIdx:a})}let c=aQ(r,l);if(!c)return null;s[c.key]=c.value,null===c.value&&(n=c.key)}if(null!==n){let a=i.length+2,o=(0,$.K7)(e,t+1);if(o<e.length){let i=(0,$.MG)(e[o]);if(i.length>a){if(e[o].slice(i.length).startsWith("-"))return null;let a=a4(e,t+1,i);return Object.keys(a.values).length>0&&(s[n]=a.values),{item:s,endIdx:a.endIdx}}}}let l=((e,t,i,a,o)=>{let r=t;for(;r<e.length;){let t=e[r];if((0,$.BJ)(t)){r++;continue}if(!t.startsWith(i))break;if(t.startsWith(`${i} `))return null;let s=aX(t,a);if(!s)return null;o[s.key]=s.value,r++}return r})(e,t+1,a,r,s);return null===l?null:{item:s,endIdx:l}},n=[],l=t;for(;l<e.length;){if((0,$.BJ)(e[l])){l++;continue}if(!(0,$.AL)(e[l],i))break;let t=s(l);if(!t)return null;n.push(t.item),l=t.endIdx}return{items:n,endIdx:l}};function a6(e,t,i){if(void 0!==i)return i-1;for(let i=0;i<e.length;i++)if(e[i].startsWith(`${t}:`))return i;return -1}function a3(e,t,i){let a=Object.create(null),o=new Map,r=new Map,s=(e,t,i)=>{o.set(e,{start:t,end:i,leadStart:t})},n=a6(e,t,i);if(n<0)return{values:a,spans:o,comments:r,childIndent:"",isListItem:!1,startIdx:n};let l=$.WV.test(e[n]),d=(0,$.eq)(e,n,l),c=(0,$.zM)(d);if(!l&&y.sU.has(t)){let i=(0,$.K7)(e,n+1);if(i<e.length&&(0,$.SU)(e[i],d))return a[t]=a1(e,n+1,d).value,{values:a,spans:o,comments:r,childIndent:d,isListItem:l,startIdx:n}}if(l){let t=e[n].match($.L1);if(t){let e=t[2].trim();if(""!==e){let{comment:i}=(0,e5.bw)(e);i&&r.set(t[1],i),a[t[1]]=(0,e5.Qj)(e)}}}let p=l?(e[n].match(/^(\s*)-/)??["",""])[1].length:-1;for(let t=n+1;t<e.length;t++){let i=e[t];if((0,$.BJ)(i))continue;if(l){let e=i.match(/^(\s*)-(\s|$)/);if(e&&e[1].length===p||$.QW.test(i))break}else if($.QW.test(i))break;let o=i.match(c);if(!o)continue;let n=o[1],h=o[2].trim(),u=(0,$.CI)(h);if(u){let{endIdx:i}=a0(e,t+1,d);a[n]=aJ(u,h,e.slice(t+1,i)),s(n,t,i),t=i-1;continue}if(""===h){let i=(0,$.K7)(e,t+1);if(i>=e.length)continue;let o=e[i];if((0,$.SU)(o,d)){let{value:i,endIdx:o,isEmptyScalarList:r}=a1(e,t+1,d);r||(a[n]=i,s(n,t,o),t=o-1);continue}let r=(0,$.MG)(o);if(r.length>d.length){let i=a4(e,t+1,r);Object.keys(i.values).length>0&&(a[n]=i.values,s(n,t,i.endIdx)),t=i.endIdx-1}continue}let{value:m,comment:v}=(0,e5.bw)(h);if(v&&r.set(n,v),m.startsWith("[")&&m.endsWith("]")){a[n]=(0,e5.Wg)(m),s(n,t,t+1);continue}a[n]=(0,e5.Qj)(m),s(n,t,t+1)}for(let t of o.values()){let i=t.start+1,a=t.end,o=!1;for(;a>i&&(0,$.BJ)(e[a-1])&&(0,$.MG)(e[a-1]).length<=d.length;)a--,(0,$.w5)(e[a])&&(o=!0);o&&(t.end=a)}let h=n+1;for(let t of o.values()){let i=t.start;for(;i>h&&(0,$.BJ)(e[i-1]);)i--;t.leadStart=i,h=t.end}return{values:a,spans:o,comments:r,childIndent:d,isListItem:l,startIdx:n}}function a4(e,t,i){let a=(0,$.zM)(i),o=Object.create(null),r=t;for(;r<e.length;){let t=e[r];if((0,$.BJ)(t)){r++;continue}if(!t.startsWith(i))break;let s=t.match(a);if(!s){r++;continue}let n=s[1],l=s[2].trim(),d=(0,$.CI)(l);if(d){let{endIdx:t}=a0(e,r+1,i);o[n]=aJ(d,l,e.slice(r+1,t)),r=t;continue}if(""===l){let t=(0,$.K7)(e,r+1);if(t<e.length&&(0,$.SU)(e[t],i)){let{value:t,endIdx:a}=a1(e,r+1,i);o[n]=t,r=a;continue}if(t<e.length){let a=(0,$.MG)(e[t]);if(a.length>i.length){let t=a4(e,r+1,a);Object.keys(t.values).length>0&&(o[n]=t.values),r=t.endIdx;continue}}r++;continue}l.startsWith("[")&&l.endsWith("]")?o[n]=(0,e5.Wg)(l):o[n]=(0,e5.Qj)(l),r++}return{values:o,endIdx:r}}function a5(e,t){if(e===t)return!0;if(e instanceof eM.ho||t instanceof eM.ho)return e instanceof eM.ho&&t instanceof eM.ho&&e.inlineHeader===t.inlineHeader&&e.lines.length===t.lines.length&&e.lines.every((e,i)=>e===t.lines[i]);if(Array.isArray(e)||Array.isArray(t))return Array.isArray(e)&&Array.isArray(t)&&e.length===t.length&&e.every((e,i)=>a5(e,t[i]));if((0,eB.Qd)(e)&&(0,eB.Qd)(t)){let i=Object.keys(e);return i.length===Object.keys(t).length&&i.every(i=>Object.prototype.hasOwnProperty.call(t,i)&&a5(e[i],t[i]))}return!1}function a8(e,t,i){let a=a6(e,t,i);if(a<0)return{start:-1,end:-1};let o=$.WV.test(e[a]),r=o?(e[a].match(/^(\s*)-/)??["",""])[1].length:-1,s=e.length;for(let t=a+1;t<e.length;t++)if(o){let i=e[t].match(/^(\s*)-(\s|$)/);if(i&&i[1].length===r||$.QW.test(e[t])){s=t;break}}else if($.QW.test(e[t])){s=t;break}return{start:a,end:s}}function a9(e){if(e._draftTimer=null,!e._config)return;let t=(0,y.a7)(e.sectionKey,e._config.entries);e._fieldErrors=(0,eN.JK)(t,e._values,e._presentComponents,e.board?.esphome.platform??null);let i=B(e.yaml,e.sectionKey,e.fromLine);if(void 0===i)return void e._setDirty(!1);let a=function(e,t,i,a,o={}){let r=e.split("\n"),{start:s,end:n}=a8(r,t,a);if(s<0)return e;let l=$.WV.test(r[s]),d=(0,$.eq)(r,s,l),c=n,p=!1;for(;c>s+1;){let e=r[c-1];if(""===e.trim())c--;else if((0,$.w5)(e)&&(0,$.MG)(e).length<=d.length)p=!0,c--;else break}let h=p?c:n;if(y.sU.has(t)){let a=i[t];if(!Array.isArray(a))return e;let n=(0,eM.ym)({[t]:a},(0,$.MG)(r[s]),{...o,indentStep:o.indentStep??(d||"  ")});return r.splice(s,h-s,...n),r.join("\n")}let u=a3(r,t,a),m=r[s],v=new Set;if(l){let e=m.match($.L1);if(e){let t=e[1];if(Object.prototype.hasOwnProperty.call(i,t))if(function(e){if(null==e)return!1;let t=typeof e;return"string"===t||"number"===t||"boolean"===t}(i[t])){if(v.add(t),!a5(i[t],u.values[t])){let e=m.match(/^(\s+)-(\s+)/),a=`${e[1]}-${e[2]}`,o=u.comments.get(t)??"";m=`${a}${t}: ${(0,eM.Rm)(i[t])}${o}`}}else{let e=(m.match(/^(\s+)-/)??["",""])[1];m=`${e}-`}}}let g=!l&&d?d:"  ",f=[m,...function(e,t,i,a,o,r){let s=[];for(let[n,l]of Object.entries(i)){if(a.has(n))continue;let i=t.spans.get(n);if(i&&a5(l,t.values[n])){s.push(...e.slice(i.leadStart,i.end));continue}i&&s.push(...e.slice(i.leadStart,i.start));let d=(0,eM.ym)({[n]:l},o,r),c=t.comments.get(n);c&&1===d.length&&(d[0]+=c),s.push(...d)}return s}(r,u,i,v,d,{...o,indentStep:o.indentStep??g})];return r.splice(s,h-s,...f),r.join("\n")}(e.yaml,e.sectionKey,e._values,i,{keepEmptyStrings:y.fq.has(e.sectionKey)});e._setDirty(!1),a!==e.yaml&&(e._lastSelfWrittenYaml=a,e.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})))}async function a7(e){if(!e._config)return;let t=B(e.yaml,e.sectionKey,e.fromLine);if(void 0===t){e._error=e._localize("device.section_delete_error");return}e._deleting=!0,e._error="";let i=e._config.title;try{let a=function(e,t,i){let a=e.split("\n"),{start:o,end:r}=a8(a,t,i);if(o<0)return e;let s=$.WV.test(a[o]);if(a.splice(o,r-o),s){let e=o-1;for(;e>=0&&!$.QW.test(a[e]);)e--;if(e>=0){let t=!1,i=a.length;for(let o=e+1;o<a.length;o++){if($.QW.test(a[o])){i=o;break}if(""!==a[o].trim()){t=!0;break}}t||a.splice(e,i-e)}}return a.join("\n")}(e.yaml,e.sectionKey,t);if(a===e.yaml){e._error=e._localize("device.section_delete_error");return}await e._api.updateConfig(e.configuration,a),e._setDirty(!1),e.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:a},bubbles:!0,composed:!0})),e.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0})),c.A.success(e._localize("device.section_deleted",{name:i}),{richColors:!0})}catch(t){e._error=t instanceof Error?t.message:e._localize("device.section_delete_error")}finally{e._deleting=!1}}async function oe(e){let t=++e._loadId;e._loading=!0,e._error="",e._config=null,e._isUnknown=!1,e._setDirty(!1),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),e._lastSelfWrittenYaml=null;try{var i;let a=e.board?.esphome.platform,o=await (0,eT.Sn)(e._api,e.sectionKey,a);if(t!==e._loadId)return;let r=e.yaml;o?e._config={section_key:e.sectionKey,section_type:"core",title:o.name,description:o.description,docs_url:o.docs_url,icon:"",image_url:o.image_url,entries:o.config_entries}:(e._config={section_key:e.sectionKey,section_type:"core",title:e.sectionKey,description:"",docs_url:"",icon:"",image_url:"",entries:[]},e._isUnknown=!0);let s=B(r,e.sectionKey,e.fromLine),n=(i=e.sectionKey,a3(r.split("\n"),i,s).values);e._values=(0,tB.Dq)(n,e._config.entries),e._resolvedFromLine=s,e._presentComponents=(0,eM.Zn)(r)}catch(a){if(t!==e._loadId)return;let i=a instanceof Error?a.message:"";e._error=i.includes("timed out")?e._localize("device.load_config_error"):i||e._localize("device.load_config_error")}finally{t===e._loadId&&(e._loading=!1)}}var ot=i(8100);async function oi(e=4){let t=Math.max(1,Math.trunc(e)),{PASSPHRASE_WORDS:a}=await i.e(820).then(i.bind(i,2503)),o=a.length,r=Math.floor(0x100000000/o)*o,s=new Uint32Array(1),n=[];for(;n.length<t;)crypto.getRandomValues(s),s[0]>=r||n.push(a[s[0]%o]);return n.join("-")}function oa(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({"lock-alert":n.mdiLockAlert});let oo=()=>oi(),or={api:{secretSection:"api",marker:"encryption",copyPrefix:"api_encryption",fields:[{path:["encryption","key"],generate:function(){return(0,ot.Y)(crypto.getRandomValues(new Uint8Array(32)).buffer)},secretField:"key"}]},"ota.esphome":{secretSection:"ota.esphome",marker:"password",copyPrefix:"ota_password",fields:[{path:["password"],generate:oo,secretField:"password"}]},web_server:{secretSection:"web_server",marker:"auth",copyPrefix:"web_auth",fields:[{path:["auth","username"],generate:()=>oi(1)},{path:["auth","password"],generate:oo,secretField:"password"}]}},os=e=>Object.prototype.hasOwnProperty.call(or,e);class on extends l.WF{get _setting(){return os(this.sectionKey)?or[this.sectionKey]:void 0}willUpdate(e){(e.has("yaml")||e.has("fromLine")||e.has("sectionKey"))&&(this._markerAbsent=!!this._setting&&!this._markerPresent())}_resolvedFields(){let e=this._setting;if(!e)return[];let t=eH(this._devices,this.configuration);return e.fields.map(i=>({field:i,key:i.secretField?ti(e.secretSection,i.secretField,t,!0)[0]??"":""}))}get _ready(){let e=this._resolvedFields();return e.length>0&&e.every(e=>!e.field.secretField||""!==e.key)}_markerPresent(){let e=this._setting;if(!e)return!1;let t=this.yaml.split("\n"),i=a6(t,this.sectionKey.split(".")[0],this.fromLine);if(i<0)return!1;let a=RegExp(`^${e.marker}\\s*:`),o=null;for(let e=i+1;e<t.length;e++){let i=t[e];if(""===i.trim()||i.trimStart().startsWith("#"))continue;if($.QW.test(i))break;let r=i.length-i.trimStart().length;if(null===o&&(o=r),r<o)break;if(r===o&&a.test(i.trimStart()))return!0}return!1}render(){let e=this._setting;return e&&this._markerAbsent?(0,l.qy)`
      <div class="notice" role="note">
        <wa-icon library="mdi" name="lock-alert"></wa-icon>
        <div class="body">
          <p>${this._localize(`device.${e.copyPrefix}_notice`)}</p>
          <button
            type="button"
            class="cta"
            ?disabled=${this._generating||!this._ready}
            @click=${this._onCta}
          >
            ${this._localize(`device.${e.copyPrefix}_enable`)}
          </button>
        </div>
      </div>
      <esphome-confirm-dialog
        heading=${this._localize(`device.${e.copyPrefix}_dialog_title`)}
        confirm-label=${this._localize("device.security_generate")}
        @confirm=${this._onGenerate}
      >
        <div slot="body" class="dialog-body">${this._renderDialogBody(e)}</div>
      </esphome-confirm-dialog>
    `:l.s6}_renderDialogBody(e){let[t,i=""]=this._localize(`device.${e.copyPrefix}_dialog_body`).split("{key}"),a=this._resolvedFields().filter(e=>e.field.secretField).map((e,t)=>(0,l.qy)`${t>0?", ":""}<code>${e.key}</code>`);return(0,l.qy)`${t}${a}${i}`}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.sectionKey="",this.yaml="",this.configuration="",this._markerAbsent=!1,this._generating=!1,this._onCta=()=>{this._ready&&this._dialog?.open()},this._onGenerate=async()=>{let e=this._setting,t=this._resolvedFields();if(!this._generating&&this._api&&e&&this._ready){this._generating=!0;try{let e=[];for(let{field:i,key:a}of t){let t=await i.generate();i.secretField?(await iI(this._api,a,t),e.push({path:i.path,value:`!secret ${a}`})):e.push({path:i.path,value:t})}this.dispatchEvent(new CustomEvent("apply-security-secrets",{detail:{secrets:e},bubbles:!0,composed:!0})),c.A.success(this._localize("device.security_applied"),{richColors:!0})}catch(t){console.error("Security secret generation failed",t),c.A.error(this._localize(`device.${e.copyPrefix}_error`),{richColors:!0})}finally{this._generating=!1}}}}}function ol(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}on.styles=[m.G,(0,l.AH)`
      .notice {
        display: flex;
        align-items: flex-start;
        gap: var(--wa-space-s);
        margin-bottom: var(--wa-space-m);
        padding: var(--wa-space-s) var(--wa-space-m);
        border: var(--wa-border-width-s) solid var(--esphome-warning, #f59e0b);
        background: color-mix(in srgb, var(--esphome-warning, #f59e0b), transparent 90%);
        border-radius: var(--wa-border-radius-m);
        color: var(--wa-color-text-normal);
        font-size: var(--wa-font-size-s);
        line-height: 1.5;
      }

      .notice wa-icon {
        flex-shrink: 0;
        font-size: 20px;
        color: var(--esphome-warning, #f59e0b);
      }

      .body {
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-s);
        flex: 1;
        min-width: 0;
      }

      .body p {
        margin: 0;
      }

      .cta {
        align-self: flex-start;
        padding: var(--wa-space-2xs) var(--wa-space-m);
        border: none;
        border-radius: var(--wa-border-radius-m);
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
        font-family: inherit;
        font-size: inherit;
        font-weight: var(--wa-font-weight-bold);
        cursor: pointer;
        transition:
          background 0.12s,
          opacity 0.12s;
      }

      .cta:hover:not(:disabled) {
        background: var(--esphome-primary-hover);
      }

      .cta:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      .dialog-body code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
        padding: 1px 5px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
        word-break: break-all;
      }
    `],oa([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],on.prototype,"_localize",void 0),oa([(0,s.Fg)({context:u.Ie,subscribe:!0}),(0,d.wk)()],on.prototype,"_api",void 0),oa([(0,s.Fg)({context:u.xJ,subscribe:!0}),(0,d.wk)()],on.prototype,"_devices",void 0),oa([(0,d.MZ)()],on.prototype,"sectionKey",void 0),oa([(0,d.MZ)()],on.prototype,"yaml",void 0),oa([(0,d.MZ)()],on.prototype,"configuration",void 0),oa([(0,d.MZ)({type:Number})],on.prototype,"fromLine",void 0),oa([(0,d.wk)()],on.prototype,"_markerAbsent",void 0),oa([(0,d.wk)()],on.prototype,"_generating",void 0),oa([(0,d.P)("esphome-confirm-dialog")],on.prototype,"_dialog",void 0),on=oa([(0,d.EM)("esphome-security-notice")],on),(0,b.C)({delete:n.mdiDelete,"information-outline":n.mdiInformationOutline,"open-in-new":n.mdiOpenInNew,pencil:n.mdiPencil,"plus-circle-outline":n.mdiPlusCircleOutline});let od=new Set(["esphome"]);class oc extends l.WF{get _showAdvanced(){return this._advancedShownSections.has(this.sectionKey)}_setShowAdvanced(e){let t=new Set(this._advancedShownSections);e?t.add(this.sectionKey):t.delete(this.sectionKey),this._advancedShownSections=t}willUpdate(e){(e.has("sectionKey")||e.has("configuration")||e.has("fromLine"))&&this.sectionKey&&this.configuration&&oe(this)}updated(){this._triggerCatalog.ensure()}connectedCallback(){super.connectedCallback(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}flushPending(){null!==this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null,a9(this))}reload(){this.sectionKey&&this.configuration&&null===this._draftTimer&&this.yaml!==this._lastSelfWrittenYaml&&oe(this)}get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_scheduleDraftFlush(){this._draftTimer&&clearTimeout(this._draftTimer),this._draftTimer=setTimeout(()=>a9(this),oc.DRAFT_DEBOUNCE_MS)}_onShowYamlEditor(){this.dispatchEvent(new CustomEvent("show-yaml-editor",{bubbles:!0,composed:!0}))}render(){if(this._loading)return(0,l.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`;if(this._error&&!this._config)return(0,l.qy)`<p class="error">${this._error}</p>`;if(!this._config)return l.s6;let e=this._showAdvanced,t=(0,y.a7)(this.sectionKey,this._config.entries),i=at(t),a=(0,aB.r)(this.sectionKey,t.length),o=!od.has(this.sectionKey);return(0,l.qy)`
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
                ${(0,et.G)(this._config.description)}
              </p>`:l.s6}
        </div>
        ${this._isUnknown?l.s6:(0,l.qy)`<div class="section-image">
              <img
                src=${this._config.image_url||(0,ee.uG)()}
                alt=${this._config.title}
                referrerpolicy="no-referrer"
                @error=${ee.jt}
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
            ${os(this.sectionKey)?(0,l.qy)`<esphome-security-notice
                  .sectionKey=${this.sectionKey}
                  .yaml=${this.yaml}
                  .configuration=${this.configuration}
                  .fromLine=${this._resolvedFromLine}
                  @apply-security-secrets=${this._onApplySecuritySecrets}
                ></esphome-security-notice>`:l.s6}
            <esphome-config-entry-form
              .entries=${t}
              .values=${this._values}
              .errors=${this._fieldErrors}
              .board=${this.board}
              .yaml=${this.yaml}
              .fromLine=${this._resolvedFromLine}
              .sectionKey=${this.sectionKey}
              .configuration=${this.configuration}
              .focusFieldPath=${this.focusFieldPath}
              .presentComponents=${this._presentComponents}
              ?show-advanced=${e}
              @value-change=${this._onValueChange}
              @edit-action-field=${this._onEditActionField}
            ></esphome-config-entry-form>
            ${i?ai(e,this._localize,e=>this._setShowAdvanced(e)):l.s6}
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
    </button>`}_renderApiActionsTable(){if("api"!==this.sectionKey)return l.s6;let e=E(this.yaml).filter(e=>e.key.startsWith("automation:api_action:")).map(e=>({key:e.key,label:e.id??""}));return(0,l.qy)`<esphome-section-automation-list
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
    ></esphome-add-api-action-dialog>`}_shortcutTarget(){if(op.has(this.sectionKey))return null;if("esphome"===this.sectionKey)return{kind:"device_on"};let e=this._resolveComponentMatch();if(null===e)return null;let t=[e.match.parentKey??e.match.key,this.sectionKey];return this._triggerCatalog.hasTriggersFor(t)?{kind:"component_on",componentId:(0,x.MX)(e.sections,e.match)}:null}_resolveComponentMatch(){let e=(0,x.MT)(this.yaml),t=e.filter(e=>N(e)===this.sectionKey);return 0===t.length?null:{sections:e,match:void 0!==this._resolvedFromLine?t.find(e=>e.fromLine===this._resolvedFromLine)??t[0]:t[0]}}_resolveComponentId(){let e=this._resolveComponentMatch();return null===e?null:(0,x.MX)(e.sections,e.match)}_renderTriggersTable(){let e=this._shortcutTarget();if(null===e)return l.s6;let t=E(this.yaml).filter(t=>!!t.eventKey&&("device_on"===e.kind?"esphome"===t.parentKey:t.id===e.componentId||t.parentComponentId===e.componentId)).map(e=>({key:e.key,label:void 0!==e.parentComponentId?`${e.name??e.id} → ${this._triggerLabel(e)}`:this._triggerLabel(e)})),i="device_on"===e.kind?this._localize("device.automations_list_title_device"):this._localize("device.automations_list_title");return(0,l.qy)`<esphome-section-automation-list
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
    ></esphome-section-automation-list>`}_renderActionFieldsTable(){let e=this._resolveComponentId();if(null===e)return l.s6;let t=E(this.yaml).filter(t=>void 0!==t.actionField&&t.id===e).map(e=>({key:e.key,label:aq(e.actionField??"",this._localize)}));return(0,l.qy)`<esphome-section-automation-list
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
    ></esphome-add-automation-dialog>`}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.sectionKey="",this.yaml="",this.yamlPaneVisible=!0,this.board=null,this.boardName="",this._config=null,this._values={},this._loading=!1,this._dirty=!1,this._error="",this._deletingRow="",this._isUnknown=!1,this._fieldErrors=new Map,this._advancedShownSections=new Set,this._presentComponents=new Set,this._deleting=!1,this._loadId=0,this._draftTimer=null,this._lastSelfWrittenYaml=null,this._triggerCatalog=new aN(this,()=>({api:this._api,platform:this.board?.esphome.platform||void 0,boardId:this.board?.id})),this._onValueChange=e=>(function(e,t){let{path:i,value:a}=t.detail;e._values=(0,eB.Oe)(e._values,i,a),e._setDirty(!0);let o=i.join(".");if(e._fieldErrors.has(o)){let t=new Map(e._fieldErrors);t.delete(o),e._fieldErrors=t}e._scheduleDraftFlush()})(this,e),this._onDeleteConfirmed=()=>a7(this),this._onApplySecuritySecrets=e=>(function(e,t){for(let{path:i,value:a}of t)e._values=(0,eB.Oe)(e._values,i,a);e._setDirty(!0),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),a9(e)})(this,e.detail.secrets),this._onOpenAddApiAction=()=>{this._addApiActionDialog?.open()},this._onApiActionAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditRow=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.key},bubbles:!0,composed:!0}))},this._onDeleteRow=async e=>{e.stopPropagation();let t=e.detail.key,i=ex(t);if(this._api&&i&&!this._deletingRow){this._deletingRow=t;try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,i,this.yaml),t=e$(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._deletingRow=""}}},this._onOpenAddAutomation=()=>{let e=this._shortcutTarget();null!==e&&("device_on"===e.kind?this._addAutomationDialog?.open({kind:"device_on"}):this._addAutomationDialog?.open({kind:"component_on",componentId:e.componentId}))},this._onAutomationAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditActionField=e=>{e.stopPropagation();let t=this._resolveComponentId();if(null===t)return;let i=ew({kind:"component_action",component_id:t,field:e.detail.field});this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:i},bubbles:!0,composed:!0}))}}}oc.DRAFT_DEBOUNCE_MS=200,oc.styles=[m.G,es.z,aG],ol([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oc.prototype,"_localize",void 0),ol([(0,s.Fg)({context:u.Ie})],oc.prototype,"_api",void 0),ol([(0,d.MZ)()],oc.prototype,"configuration",void 0),ol([(0,d.MZ)()],oc.prototype,"sectionKey",void 0),ol([(0,d.MZ)({type:Number})],oc.prototype,"fromLine",void 0),ol([(0,d.MZ)({attribute:!1})],oc.prototype,"focusFieldPath",void 0),ol([(0,d.MZ)()],oc.prototype,"yaml",void 0),ol([(0,d.MZ)({type:Boolean})],oc.prototype,"yamlPaneVisible",void 0),ol([(0,d.MZ)({attribute:!1})],oc.prototype,"board",void 0),ol([(0,d.MZ)()],oc.prototype,"boardName",void 0),ol([(0,d.wk)()],oc.prototype,"_config",void 0),ol([(0,d.wk)()],oc.prototype,"_values",void 0),ol([(0,d.wk)()],oc.prototype,"_loading",void 0),ol([(0,d.wk)()],oc.prototype,"_dirty",void 0),ol([(0,d.wk)()],oc.prototype,"_error",void 0),ol([(0,d.wk)()],oc.prototype,"_deletingRow",void 0),ol([(0,d.wk)()],oc.prototype,"_isUnknown",void 0),ol([(0,d.wk)()],oc.prototype,"_fieldErrors",void 0),ol([(0,d.wk)()],oc.prototype,"_advancedShownSections",void 0),ol([(0,d.wk)()],oc.prototype,"_presentComponents",void 0),ol([(0,d.wk)()],oc.prototype,"_resolvedFromLine",void 0),ol([(0,d.P)("esphome-confirm-dialog")],oc.prototype,"_confirmDialog",void 0),ol([(0,d.P)("esphome-add-api-action-dialog")],oc.prototype,"_addApiActionDialog",void 0),ol([(0,d.P)("esphome-add-automation-dialog")],oc.prototype,"_addAutomationDialog",void 0),ol([(0,d.wk)()],oc.prototype,"_deleting",void 0),oc=ol([(0,d.EM)("esphome-device-section-config")],oc);let op=new Set(["api","script","interval","external_components","packages","substitutions","globals","dashboard_import"]);function oh(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({"open-in-new":n.mdiOpenInNew,"arrow-left":n.mdiArrowLeft,close:n.mdiClose,"party-popper":n.mdiPartyPopper,"plus-circle-outline":n.mdiPlusCircleOutline});class ou extends l.WF{willUpdate(e){e.has("board")&&this._refreshAlternateBoards()}updated(e){if(e.has("yaml")&&this.selectedSection){var t,i;let a=()=>{this._sectionConfig?.reload(),this._automationEditor?.reload(),this._scriptEditor?.reload(),this._apiActionEditor?.reload()};(this._reloadTimer&&(clearTimeout(this._reloadTimer),this._reloadTimer=null),t=e.get("yaml"),i=this.yaml,t||!i)?this._reloadTimer=setTimeout(a,1e3):a()}}connectedCallback(){super.connectedCallback(),this.addEventListener("request-add-component",this._onRequestAddComponent)}disconnectedCallback(){super.disconnectedCallback(),this._reloadTimer&&clearTimeout(this._reloadTimer),this.removeEventListener("request-add-component",this._onRequestAddComponent)}async _refreshAlternateBoards(){let e=this.board;if(!e){this._alternatesForBoardId=null,this._alternateBoards=[];return}if(e.id!==this._alternatesForBoardId){this._alternatesForBoardId=e.id,this._alternateBoards=[];try{let t=await this._api.getCompatibleBoards(e.id);if(this._alternatesForBoardId!==e.id)return;this._alternateBoards=t.filter(t=>t.id!==e.id)}catch(t){console.error("Failed to load compatible boards:",t),this._alternatesForBoardId===e.id&&(this._alternatesForBoardId=null,this._alternateBoards=[])}}}render(){let e=this.board;return(0,l.qy)`
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
                <p class="board-description">${(0,et.G)(e.description)}</p>
              </div>
              <div class="board-image">
                <img
                  src=${(0,ee.Ru)(e)}
                  alt=${e.name}
                  referrerpolicy="no-referrer"
                  @error=${ee.jt}
                />
              </div>
            </div>
            <div class="board-separator"></div>
          `:l.s6}
      ${this.selectedSection?this._renderSelectedSection():(0,l.qy)`
            ${this.justCreated?this._renderWelcomeBanner():l.s6}
            ${this._renderStepSection({title:this._localize("device.step_core"),desc:this._localize("device.step_core_desc"),icon:ea,action:this._localize("device.show_core_configuration"),section:"core"})}
            ${this._renderStepSection({title:this._localize("device.step_components"),desc:this._localize("device.step_components_desc"),icon:eo,action:this._localize("device.show_components"),section:"components"})}
            ${this._renderStepSection({title:this._localize("device.step_automations"),desc:this._localize("device.step_automations_desc"),icon:er,action:this._localize("device.show_automations"),section:"automations"})}
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
    `}_renderSelectedSection(){let e=this.selectedSection,t=e.startsWith("automation:")?ex(e):null;return t?.kind==="script"?(0,l.qy)`<esphome-script-editor
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
    `:l.s6}_onDismissWelcome(){this.dispatchEvent(new CustomEvent("just-created-dismiss",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this._alternateBoards=[],this._alternatesForBoardId=null,this.yaml="",this.configuration="",this.justCreated=!1,this.yamlPaneVisible=!0,this.selectedSection=null,this._reloadTimer=null,this._onRequestAddComponent=e=>{let t=e.detail;t?.domain&&(e.stopPropagation(),this._addComponentDialog?.openWithSearch(t.domain))},this._openChangeBoard=()=>{this._changeBoardDialog?.open()},this._onSelectBoard=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("change-board",{detail:e.detail,bubbles:!0,composed:!0}))}}}function om(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ou.styles=[m.G,ei],oh([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ou.prototype,"_localize",void 0),oh([(0,s.Fg)({context:u.Ie})],ou.prototype,"_api",void 0),oh([(0,d.MZ)({attribute:!1})],ou.prototype,"board",void 0),oh([(0,d.wk)()],ou.prototype,"_alternateBoards",void 0),oh([(0,d.MZ)()],ou.prototype,"yaml",void 0),oh([(0,d.MZ)()],ou.prototype,"configuration",void 0),oh([(0,d.MZ)({type:Boolean})],ou.prototype,"justCreated",void 0),oh([(0,d.MZ)({type:Boolean})],ou.prototype,"yamlPaneVisible",void 0),oh([(0,d.MZ)({attribute:!1})],ou.prototype,"selectedSection",void 0),oh([(0,d.MZ)({type:Number})],ou.prototype,"selectedFromLine",void 0),oh([(0,d.MZ)({attribute:!1})],ou.prototype,"focusFieldPath",void 0),oh([(0,d.P)("esphome-device-section-config")],ou.prototype,"_sectionConfig",void 0),oh([(0,d.P)("esphome-automation-editor")],ou.prototype,"_automationEditor",void 0),oh([(0,d.P)("esphome-script-editor")],ou.prototype,"_scriptEditor",void 0),oh([(0,d.P)("esphome-api-action-editor")],ou.prototype,"_apiActionEditor",void 0),oh([(0,d.P)("esphome-add-component-dialog")],ou.prototype,"_addComponentDialog",void 0),oh([(0,d.P)("esphome-add-automation-dialog")],ou.prototype,"_addAutomationDialog",void 0),oh([(0,d.P)("esphome-add-config-dialog")],ou.prototype,"_addConfigDialog",void 0),oh([(0,d.P)("esphome-change-board-dialog")],ou.prototype,"_changeBoardDialog",void 0),ou=oh([(0,d.EM)("esphome-device-board-info")],ou),(0,b.C)({"alert-circle-outline":n.mdiAlertCircleOutline,"check-circle-outline":n.mdiCheckCircleOutline,"content-save":n.mdiContentSave,eye:n.mdiEye,"eye-off":n.mdiEyeOff,"layout-left":n.mdiDockLeft,"layout-right":n.mdiDockRight,"layout-split":n.mdiViewSplitHorizontal,upload:n.mdiUpload,"vector-difference":n.mdiVectorDifference});class ov extends l.WF{connectedCallback(){super.connectedCallback(),this._isMobile=this._mql.matches,this._mql.addEventListener("change",this._onMqlChange),window.addEventListener("keydown",this._onGlobalKeyDown)}disconnectedCallback(){super.disconnectedCallback(),this._mql.removeEventListener("change",this._onMqlChange),window.removeEventListener("keydown",this._onGlobalKeyDown)}render(){let e,t,i=this._isMobile&&"both"===this.layout?"right":this.layout,a=!this._isMobile&&this.navCollapsed&&"right"===i,o=this._localize("device.editor_title_ready",{name:this.deviceTitle});return(0,l.qy)`
      <section class="card">
        <header class="card-header ${a?"card-header--compact":""}">
          <slot name="header-start"></slot>
          <div class="editor-header-main">
            <div class="editor-header-titlerow">
              <h2 class="editor-header-title">${o}</h2>
              ${this.configuration&&!a?(0,l.qy)`<span class="editor-header-file">${this.configuration}</span>`:l.s6}
            </div>
          </div>
          <div class="header-actions">
            ${"left"!==i?(e=this._localize(this._revealSensitive?"device.yaml_mask_sensitive":"device.yaml_reveal_sensitive"),(0,l.qy)`<button
                    type="button"
                    class="ghost-icon-btn diff-toggle"
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
            ${this._showDiffButton?(t=this._showDiff?this._localize("device.diff_view_editor"):this._localize("device.diff_view_diff"),(0,l.qy)`<button
                    type="button"
                    class="ghost-icon-btn diff-toggle"
                    aria-pressed=${this._showDiff}
                    ?disabled=${this.yaml===this.savedYaml&&!this._showDiff}
                    aria-label=${t}
                    @click=${this._toggleDiff}
                    title=${t}
                  >
                    <wa-icon library="mdi" name="vector-difference"></wa-icon>
                  </button>`):l.s6}
            <div
              class="layout-toggle"
              aria-label=${this._localize("device.editor_layout_label")}
            >
              <button
                type="button"
                class="ghost-icon-btn"
                aria-pressed=${"left"===i}
                @click=${()=>this._setLayout("left")}
                aria-label=${this._localize("device.layout_components_only")}
                title=${this._localize("device.layout_components_only")}
              >
                <wa-icon library="mdi" name="layout-left"></wa-icon>
              </button>
              <button
                class="ghost-icon-btn split-btn"
                type="button"
                aria-pressed=${"both"===i}
                @click=${()=>this._setLayout("both")}
                aria-label=${this._localize("device.layout_split")}
                title=${this._localize("device.layout_split")}
              >
                <wa-icon library="mdi" name="layout-split"></wa-icon>
              </button>
              <button
                type="button"
                class="ghost-icon-btn"
                aria-pressed=${"right"===i}
                @click=${()=>this._setLayout("right")}
                aria-label=${this._localize("device.layout_yaml_only")}
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
          <div
            class="editor-layout ${"both"===i?"editor-layout--both":"left"===i?"editor-layout--left":"editor-layout--right"} ${this._dragging?"dragging":""}"
            style=${"both"===i?`grid-template-columns: ${this._splitRatio}fr var(--pane-divider-width) ${1-this._splitRatio}fr`:""}
          >
            <div class="editor-pane editor-pane--left">
              <esphome-device-board-info
                .board=${this.board}
                .yaml=${this.yaml}
                .configuration=${this.configuration}
                .selectedSection=${this.selectedSection}
                .selectedFromLine=${this.selectedFromLine}
                .focusFieldPath=${this.focusFieldPath}
                .justCreated=${this.justCreated}
                ?yamlPaneVisible=${"left"!==i}
                @show-yaml-editor=${this._onShowYamlEditor}
              ></esphome-device-board-info>
            </div>
            ${"both"===i?(0,l.qy)`<div
                  class="pane-divider ${this._dragging?"dragging":""}"
                  role="separator"
                  aria-orientation="vertical"
                  aria-label=${this._localize("device.resize_panes")}
                  aria-valuemin=${Math.round(25)}
                  aria-valuemax=${Math.round(75)}
                  aria-valuenow=${Math.round(100*this._splitRatio)}
                  aria-valuetext=${this._localize("device.resize_panes_value",{percent:Math.round(100*this._splitRatio)})}
                  tabindex="0"
                  @pointerdown=${this._onDividerPointerDown}
                  @keydown=${this._onDividerKeydown}
                ></div>`:l.s6}
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
    `}_onSave(){this.dispatchEvent(new CustomEvent("save-yaml",{bubbles:!0,composed:!0}))}_onValidate(){this.dispatchEvent(new CustomEvent("validate-device",{bubbles:!0,composed:!0}))}_toggleDiff(){this._showDiff=!this._showDiff}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_onInstall(){this.dispatchEvent(new CustomEvent("install-device",{bubbles:!0,composed:!0}))}_onUpdate(){this.dispatchEvent(new CustomEvent("update-device",{bubbles:!0,composed:!0}))}willUpdate(e){if(e.has("configuration")&&this._liveErrors.length&&(this._liveErrors=[]),this._showDiff&&e.has("_showDiffButton")&&!this._showDiffButton){this._showDiff=!1;return}this._showDiff&&e.has("savedYaml")&&this.yaml===this.savedYaml&&(this._showDiff=!1)}_onYamlDiagnostics(e){if(e.detail.configuration!==this.configuration)return;let t=e.detail.errors;t.length===this._liveErrors.length&&t.every((e,t)=>e===this._liveErrors[t])||(this._liveErrors=t)}_setLayout(e){this.dispatchEvent(new CustomEvent("layout-change",{detail:e,bubbles:!0,composed:!0}))}_onShowYamlEditor(e){e.stopPropagation(),this._setLayout("both")}_onYamlChange(e){this.dispatchEvent(new CustomEvent("yaml-change",{detail:e.detail,bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.yaml="",this.layout="both",this.navCollapsed=!1,this.deviceTitle="",this.board=null,this.justCreated=!1,this._isMobile=!1,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._onGlobalKeyDown=e=>{(e.metaKey||e.ctrlKey)&&!e.shiftKey&&"s"===e.key.toLowerCase()&&(e.preventDefault(),this.hasUnsavedEdits&&this._onSave())},this.highlightRange=null,this.scrollToHighlight=!1,this.configuration="",this.selectedSection=null,this.savedYaml="",this.hasUnsavedEdits=!1,this.hasPendingChanges=!1,this.hasUpdateAvailable=!1,this.busy=!1,this._showDiffButton=!1,this._showDiff=!1,this._revealSensitive=!1,this._liveErrors=[],this._splitRatio=(()=>{try{let e=localStorage.getItem(G),t=null===e?NaN:Number.parseFloat(e);return Number.isFinite(t)?W(t):.5}catch{return .5}})(),this._dragging=!1,this._onDividerPointerDown=e=>{if(0!==e.button)return;let t=this._layoutEl;if(!t)return;e.preventDefault();let i=t.getBoundingClientRect();this._dragging=!0;let a=e.currentTarget;a.setPointerCapture(e.pointerId);let o=a.getBoundingClientRect().width,r=i.width-o,s=e=>{r<=0||(this._splitRatio=W((e.clientX-i.left-o/2)/r))},n=()=>{this._dragging=!1,Y(this._splitRatio),a.removeEventListener("pointermove",s),a.removeEventListener("pointerup",n),a.removeEventListener("pointercancel",n),a.removeEventListener("lostpointercapture",n)};a.addEventListener("pointermove",s),a.addEventListener("pointerup",n),a.addEventListener("pointercancel",n),a.addEventListener("lostpointercapture",n)},this._onDividerKeydown=e=>{let t=((e,t)=>{let i;if("ArrowLeft"===t)i=e-.02;else if("ArrowRight"===t)i=e+.02;else if("Home"===t)i=.25;else{if("End"!==t)return null;i=.75}return W(i)})(this._splitRatio,e.key);null!==t&&(e.preventDefault(),this._splitRatio=t,Y(this._splitRatio))}}}ov.styles=[m.G,J],om([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],ov.prototype,"_localize",void 0),om([(0,d.MZ)()],ov.prototype,"yaml",void 0),om([(0,d.MZ)()],ov.prototype,"layout",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"navCollapsed",void 0),om([(0,d.MZ)()],ov.prototype,"deviceTitle",void 0),om([(0,d.MZ)({attribute:!1})],ov.prototype,"board",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"justCreated",void 0),om([(0,d.wk)()],ov.prototype,"_isMobile",void 0),om([(0,d.MZ)({attribute:!1})],ov.prototype,"highlightRange",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"scrollToHighlight",void 0),om([(0,d.MZ)()],ov.prototype,"configuration",void 0),om([(0,d.MZ)({attribute:!1})],ov.prototype,"selectedSection",void 0),om([(0,d.MZ)({type:Number})],ov.prototype,"selectedFromLine",void 0),om([(0,d.MZ)({attribute:!1})],ov.prototype,"focusFieldPath",void 0),om([(0,d.MZ)({attribute:!1})],ov.prototype,"savedYaml",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"hasUnsavedEdits",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"hasPendingChanges",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"hasUpdateAvailable",void 0),om([(0,d.MZ)({type:Boolean})],ov.prototype,"busy",void 0),om([(0,s.Fg)({context:u.El,subscribe:!0}),(0,d.wk)()],ov.prototype,"_showDiffButton",void 0),om([(0,d.wk)()],ov.prototype,"_showDiff",void 0),om([(0,d.wk)()],ov.prototype,"_revealSensitive",void 0),om([(0,d.wk)()],ov.prototype,"_liveErrors",void 0),om([(0,d.wk)()],ov.prototype,"_splitRatio",void 0),om([(0,d.wk)()],ov.prototype,"_dragging",void 0),om([(0,d.P)(".editor-layout")],ov.prototype,"_layoutEl",void 0),ov=om([(0,d.EM)("esphome-device-editor")],ov);class og{get tick(){return this._tick}hostConnected(){this._unsubscribes=this._subscribes.map(e=>e(()=>{this._tick++,this._host.requestUpdate()}))}hostDisconnected(){for(let e of this._unsubscribes)e();this._unsubscribes=[]}constructor(e,t){this._host=e,this._subscribes=t,this._tick=0,this._unsubscribes=[],e.addController(this)}}let of=(0,l.AH)`
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
    box-shadow: var(--navigator-shadow, var(--wa-elevation-02));
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
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    flex-shrink: 0;
  }

  .card-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    line-height: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
  }

  /* Box + hover come from .ghost-icon-btn (shared.ts). This button
     swaps the shared padding for a fixed width/height and adds a hover
     transition; the icon size is per-site. */
  .collapse-btn {
    width: 30px;
    height: 22px;
    padding: 0;
    border-radius: var(--wa-border-radius-m);
    transition: background 0.12s;
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

  .nav-empty {
    padding: var(--wa-space-l) var(--wa-space-m);
    margin: 0;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    text-align: center;
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

  .nav-content-label {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    min-width: 0;
  }

  .nav-content:hover p {
    color: var(--esphome-primary);
  }

  .nav-content p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .nav-content-label wa-icon {
    font-size: var(--wa-font-size-l);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  .nav-content-chevron {
    font-size: var(--wa-font-size-xl);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  .nav-subgroup-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    /* Match the flat rows' inter-block gap with margin-top (not vertical
       padding) so a header sits the same distance below the previous block
       as the rows do; the header-to-rows gap lives on .nav-items--grouped. */
    padding: 0 var(--wa-space-m);
    margin-top: var(--wa-space-2xs);
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
  }

  .nav-subgroup-header:not(.nav-subgroup-header--static):hover .nav-subgroup-title {
    color: var(--esphome-primary);
  }

  .nav-subgroup-header:focus-visible {
    outline: none;
    box-shadow: var(--esphome-focus-ring-tight);
    border-radius: var(--wa-border-radius-s);
  }

  /* While filtering the subgroup can't collapse, so it isn't interactive. */
  .nav-subgroup-header--static {
    cursor: default;
  }

  /* Muted leading domain glyph — on a domain subgroup header and on an
     ungrouped row (Core / Automations). Always visible. */
  .nav-subgroup-icon,
  .nav-item-icon {
    font-size: var(--wa-font-size-m);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
  }

  .nav-subgroup-title {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--wa-color-text-quiet);
  }

  .nav-subgroup-count {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-raised);
    border-radius: 999px;
    padding: 0 var(--wa-space-xs);
    line-height: 1.5;
  }

  .nav-subgroup-chevron {
    margin-left: auto;
    font-size: var(--wa-font-size-l);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
  }

  .nav-items {
    display: flex;
    flex-direction: column;
    /* Bordered rows need breathing room so adjacent boxes don't touch. */
    gap: var(--wa-space-2xs);
    /* var(--wa-space-m) horizontal inset lines the row boxes' left/right
       edges up under the section headers' content. */
    padding: var(--wa-space-xs) var(--wa-space-m);
  }

  /* Rows nested under a domain subgroup; the box edge keeps the shared
     var(--wa-space-m) inset. padding-top is the header-to-first-row gap;
     padding-bottom is 0 so the next block's own margin sets the gap. */
  .nav-items--grouped {
    padding-top: var(--wa-space-2xs);
    padding-bottom: 0;
  }

  /* A lone config-block domain (no "platform:", e.g. i2c / bluetooth_proxy)
     renders as one flat row in place of a header; platform components keep
     their header even with one item. Keep the shared box inset and only drop
     the vertical pad; margin-top carries the inter-block gap, since each
     single is its own one-row container. */
  .nav-items--single {
    padding-top: 0;
    padding-bottom: 0;
    margin-top: var(--wa-space-2xs);
  }

  .nav-item {
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    /* Uniform row height tracked off the type scale (two text lines plus the
       row's own breathing room) so a description-less row pads up to the same
       box as a title + description one instead of rendering shorter. */
    min-height: calc(2 * var(--wa-font-size-s) + var(--wa-space-m));
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    cursor: pointer;
    user-select: none;
    transition:
      background 0.1s,
      border-color 0.1s;
  }

  .nav-item:hover,
  .nav-item--hovered {
    background: var(--esphome-tint);
  }

  /* Selected adds the primary border so the open row stays distinct from a
     row that is merely hovered (which only tints the background). */
  .nav-item--selected {
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
  }

  .nav-item-content {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-width: 0;
    padding: var(--wa-space-2xs) 0;
  }

  .nav-item-content p {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .nav-item-subtitle {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-weight: normal;
    margin: 0;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .nav-item-chevron {
    margin-left: auto;
    font-size: var(--wa-font-size-l);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  /* Declutter the chevron only where hover exists; on touch (no hover)
     it stays visible so the "this row navigates" cue isn't lost. */
  @media (hover: hover) {
    .nav-item-chevron {
      opacity: 0;
      transition: opacity 0.1s;
    }

    .nav-item:hover .nav-item-chevron,
    .nav-item--hovered .nav-item-chevron,
    .nav-item--selected .nav-item-chevron {
      opacity: 1;
    }
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
`;function o_(e){let{core:t,components:i,automations:a}=I((0,x.MT)(e)),o=E(e);return{core:t,components:i,automations:[...a.filter(e=>"script"!==e.key&&"interval"!==e.key),...o].filter(e=>!e.key.startsWith("automation:light_effect:")&&!e.key.startsWith("automation:unscoped:")).sort((e,t)=>e.fromLine-t.fromLine),substitutions:(0,eX.Gr)(e)}}function ob(e){let t=[],i=new Map;for(let a of e){let e=a.item.key,o=i.get(e);o||(o=[],i.set(e,o),t.push(e)),o.push(a)}return t.map(e=>({key:e,rows:i.get(e)}))}function oy(e,t,i){let a=N(e);if("automation"===t)return function(e,t,i){if("script"===e.parentKey){let a=i.localize("device.script_header_title_static"),o=(0,eX.rq)(e.id??t,i.substitutions);return{primary:a,secondary:o!==a?o:void 0}}if("interval"===e.parentKey){let t=i.localize("device.automation_interval_label"),a=e.meta?.every;return{primary:t,secondary:a?i.localize("device.automation_interval_every_n",{time:a}):void 0}}if("esphome"===e.parentKey&&e.eventKey)return{primary:ox(i.triggerCatalog.resolveName("esphome",e.eventKey,o$(e.eventKey)))};if(e.parentKey&&e.eventKey){let t=ox(i.triggerCatalog.resolveName(e.parentKey,e.eventKey,o$(e.eventKey)));return{primary:t,secondary:ow(e,i,t)}}if(e.parentKey&&e.actionField){let t=o$(e.actionField.replace(/_action$/,""));return{primary:t,secondary:ow(e,i,t)}}return{primary:e.displayLabel||t}}(e,a,i);let o=a,r=(0,eT.CQ)(a,i.platform||void 0);r?.name&&(o=r.name),"core"===t&&(o=o.replace(/ (Component|Configuration)$/,"")||o);let s="core"===t&&"esphome"===e.key&&i.deviceName?i.deviceName:(0,eX.rq)(e.name||e.id||"",i.substitutions)||void 0,n=s&&s!==o?s:void 0;return{primary:o,secondary:n}}function ow(e,t,i){let a=e.name||e.id,o=a?(0,eX.rq)(a,t.substitutions):ok(e.parentKey??"");return o!==i?o:void 0}function o$(e){return e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}function ox(e){let t=e.lastIndexOf(" → ");return t>=0?e.slice(t+3):e}function ok(e){let t=e.replace(/_/g," ");return t.charAt(0).toUpperCase()+t.slice(1)}let oz={esphome:["chip",n.mdiChip],wifi:["wifi",n.mdiWifi],ethernet:["ethernet",n.mdiEthernet],mdns:["radio-tower",n.mdiRadioTower],network:["lan",n.mdiLan],api:["api",n.mdiApi],ota:["cloud-upload-outline",n.mdiCloudUploadOutline],dashboard_import:["cloud-upload-outline",n.mdiCloudUploadOutline],logger:["card-text-outline",n.mdiCardTextOutline],syslog:["card-text-outline",n.mdiCardTextOutline],web_server:["web",n.mdiWeb],http_request:["web",n.mdiWeb],captive_portal:["wifi-lock",n.mdiWifiLock],improv_serial:["wifi-cog",n.mdiWifiCog],esp32_improv:["wifi-cog",n.mdiWifiCog],mqtt:["swap-horizontal",n.mdiSwapHorizontal],wireguard:["vpn",n.mdiVpn],socket:["connection",n.mdiConnection],udp:["connection",n.mdiConnection],async_tcp:["connection",n.mdiConnection],espnow:["connection",n.mdiConnection],serial_proxy:["connection",n.mdiConnection],sim800l:["connection",n.mdiConnection],prometheus:["chart-line",n.mdiChartLine],statsd:["chart-line",n.mdiChartLine],runtime_stats:["chart-line",n.mdiChartLine],time:["clock-outline",n.mdiClockOutline],sntp:["clock-outline",n.mdiClockOutline],interval:["clock-outline",n.mdiClockOutline],script:["script-text-outline",n.mdiScriptTextOutline],uart:["serial-port",n.mdiSerialPort],i2c:["connection",n.mdiConnection],spi:["connection",n.mdiConnection],modbus:["connection",n.mdiConnection],modbus_controller:["connection",n.mdiConnection],modbus_server:["connection",n.mdiConnection],esp32:["cpu-32-bit",n.mdiCpu32Bit],esp8266:["cpu-32-bit",n.mdiCpu32Bit],rp2040:["cpu-32-bit",n.mdiCpu32Bit],bk72xx:["cpu-32-bit",n.mdiCpu32Bit],rtl87xx:["cpu-32-bit",n.mdiCpu32Bit],ln882x:["cpu-32-bit",n.mdiCpu32Bit],libretiny:["cpu-32-bit",n.mdiCpu32Bit],nrf52:["cpu-32-bit",n.mdiCpu32Bit],host:["chip",n.mdiChip],esp32_hosted:["wifi",n.mdiWifi],esp32_ble:["bluetooth",n.mdiBluetooth],esp32_ble_tracker:["bluetooth",n.mdiBluetooth],ble:["bluetooth",n.mdiBluetooth],bluetooth_proxy:["bluetooth",n.mdiBluetooth],ble_client:["bluetooth",n.mdiBluetooth],ble_nus:["bluetooth",n.mdiBluetooth],esp32_ble_beacon:["bluetooth",n.mdiBluetooth],esp32_ble_server:["bluetooth",n.mdiBluetooth],zephyr_ble_server:["bluetooth",n.mdiBluetooth],rp2040_ble:["bluetooth",n.mdiBluetooth],exposure_notifications:["bluetooth",n.mdiBluetooth],airthings_ble:["bluetooth",n.mdiBluetooth],bedjet:["bluetooth",n.mdiBluetooth],mopeka_ble:["bluetooth",n.mdiBluetooth],radon_eye_ble:["bluetooth",n.mdiBluetooth],ruuvi_ble:["bluetooth",n.mdiBluetooth],xiaomi_ble:["bluetooth",n.mdiBluetooth],xiaomi_rtcgq02lm:["bluetooth",n.mdiBluetooth],zwave_proxy:["z-wave",n.mdiZWave],zigbee:["zigbee",n.mdiZigbee],openthread:["zigbee",n.mdiZigbee],usb_host:["usb",n.mdiUsb],usb_uart:["usb",n.mdiUsb],usb_cdc_acm:["usb",n.mdiUsb],tinyusb:["usb",n.mdiUsb],psram:["memory",n.mdiMemory],preferences:["content-save-cog-outline",n.mdiContentSaveCogOutline],power_supply:["power-plug",n.mdiPowerPlug],esp_ldo:["power-plug",n.mdiPowerPlug],sy6970:["power-plug",n.mdiPowerPlug],deep_sleep:["power-sleep",n.mdiPowerSleep],status_led:["led-on",n.mdiLedOn],safe_mode:["restart-alert",n.mdiRestartAlert],factory_reset:["restart-alert",n.mdiRestartAlert],debug:["bug",n.mdiBug],globals:["variable",n.mdiVariable],substitutions:["code-braces",n.mdiCodeBraces],packages:["package-variant-closed",n.mdiPackageVariantClosed],external_components:["puzzle-outline",n.mdiPuzzleOutline],mapping:["cog",n.mdiCog],json:["code-json",n.mdiCodeJson],bytebuffer:["code-array",n.mdiCodeArray],split_buffer:["code-array",n.mdiCodeArray],sha256:["pound-box-outline",n.mdiPoundBoxOutline],hmac_md5:["pound-box-outline",n.mdiPoundBoxOutline],hmac_sha256:["pound-box-outline",n.mdiPoundBoxOutline],remote_receiver:["remote",n.mdiRemote],remote_transmitter:["remote",n.mdiRemote],cc1101:["remote",n.mdiRemote],sx126x:["remote",n.mdiRemote],sx127x:["remote",n.mdiRemote],lightwaverf:["remote",n.mdiRemote],rf_bridge:["remote",n.mdiRemote],pn532:["nfc-variant",n.mdiNfcVariant],pn532_i2c:["nfc-variant",n.mdiNfcVariant],pn532_spi:["nfc-variant",n.mdiNfcVariant],pn7150_i2c:["nfc-variant",n.mdiNfcVariant],pn7160_i2c:["nfc-variant",n.mdiNfcVariant],pn7160_spi:["nfc-variant",n.mdiNfcVariant],rc522_i2c:["nfc-variant",n.mdiNfcVariant],rc522_spi:["nfc-variant",n.mdiNfcVariant],rdm6300:["nfc-variant",n.mdiNfcVariant],ld2410:["motion-sensor",n.mdiMotionSensor],ld2412:["motion-sensor",n.mdiMotionSensor],ld2420:["motion-sensor",n.mdiMotionSensor],ld2450:["motion-sensor",n.mdiMotionSensor],rd03d:["motion-sensor",n.mdiMotionSensor],at581x:["motion-sensor",n.mdiMotionSensor],dfrobot_sen0395:["motion-sensor",n.mdiMotionSensor],hlk_fm22x:["motion-sensor",n.mdiMotionSensor],seeed_mr24hpc1:["motion-sensor",n.mdiMotionSensor],seeed_mr60bha2:["motion-sensor",n.mdiMotionSensor],seeed_mr60fda2:["motion-sensor",n.mdiMotionSensor],esp32_touch:["gesture-tap-button",n.mdiGestureTapButton],cap1188:["gesture-tap-button",n.mdiGestureTapButton],mpr121:["gesture-tap-button",n.mdiGestureTapButton],ttp229_bsf:["gesture-tap-button",n.mdiGestureTapButton],ttp229_lsf:["gesture-tap-button",n.mdiGestureTapButton],matrix_keypad:["dialpad",n.mdiDialpad],wiegand:["dialpad",n.mdiDialpad],key_collector:["dialpad",n.mdiDialpad],fingerprint_grow:["fingerprint",n.mdiFingerprint],i2s_audio:["volume-high",n.mdiVolumeHigh],audio:["volume-high",n.mdiVolumeHigh],audio_file:["volume-high",n.mdiVolumeHigh],microphone:["microphone",n.mdiMicrophone],micro_wake_word:["microphone",n.mdiMicrophone],voice_assistant:["microphone-message",n.mdiMicrophoneMessage],speaker:["speaker",n.mdiSpeaker],dfplayer:["speaker",n.mdiSpeaker],rtttl:["speaker",n.mdiSpeaker],adalight:["lightbulb-outline",n.mdiLightbulbOutline],wled:["lightbulb-outline",n.mdiLightbulbOutline],e131:["lightbulb-outline",n.mdiLightbulbOutline],my9231:["lightbulb-outline",n.mdiLightbulbOutline],sm16716:["lightbulb-outline",n.mdiLightbulbOutline],sm2135:["lightbulb-outline",n.mdiLightbulbOutline],sm2235:["lightbulb-outline",n.mdiLightbulbOutline],sm2335:["lightbulb-outline",n.mdiLightbulbOutline],bp1658cj:["lightbulb-outline",n.mdiLightbulbOutline],bp5758d:["lightbulb-outline",n.mdiLightbulbOutline],tlc59208f:["lightbulb-outline",n.mdiLightbulbOutline],tlc5947:["lightbulb-outline",n.mdiLightbulbOutline],tlc5971:["lightbulb-outline",n.mdiLightbulbOutline],tm1651:["lightbulb-outline",n.mdiLightbulbOutline],adc128s102:["gauge",n.mdiGauge],ads1115:["gauge",n.mdiGauge],ads1118:["gauge",n.mdiGauge],mcp3008:["gauge",n.mdiGauge],mcp3204:["gauge",n.mdiGauge],as5600:["gauge",n.mdiGauge],dac7678:["export-variant",n.mdiExportVariant],gp8403:["export-variant",n.mdiExportVariant],mcp4728:["export-variant",n.mdiExportVariant],mcp4461:["export-variant",n.mdiExportVariant],pca9685:["export-variant",n.mdiExportVariant],servo:["export-variant",n.mdiExportVariant],grove_tb6612fng:["export-variant",n.mdiExportVariant],mcp23008:["connection",n.mdiConnection],mcp23016:["connection",n.mdiConnection],mcp23017:["connection",n.mdiConnection],mcp23s08:["connection",n.mdiConnection],mcp23s17:["connection",n.mdiConnection],pca6416a:["connection",n.mdiConnection],pca9554:["connection",n.mdiConnection],pcf8574:["connection",n.mdiConnection],pi4ioe5v6408:["connection",n.mdiConnection],xl9535:["connection",n.mdiConnection],max6956:["connection",n.mdiConnection],sn74hc165:["connection",n.mdiConnection],sn74hc595:["connection",n.mdiConnection],cd74hc4067:["connection",n.mdiConnection],tca9548a:["connection",n.mdiConnection],tca9555:["connection",n.mdiConnection],ch422g:["connection",n.mdiConnection],ch423:["connection",n.mdiConnection],sx1509:["connection",n.mdiConnection],m5stack_8angle:["connection",n.mdiConnection],i2c_device:["connection",n.mdiConnection],spi_device:["connection",n.mdiConnection],vbus:["connection",n.mdiConnection],tuya:["connection",n.mdiConnection],wk2132_i2c:["serial-port",n.mdiSerialPort],wk2132_spi:["serial-port",n.mdiSerialPort],wk2168_i2c:["serial-port",n.mdiSerialPort],wk2168_spi:["serial-port",n.mdiSerialPort],wk2204_i2c:["serial-port",n.mdiSerialPort],wk2204_spi:["serial-port",n.mdiSerialPort],wk2212_i2c:["serial-port",n.mdiSerialPort],wk2212_spi:["serial-port",n.mdiSerialPort],apds9960:["gauge",n.mdiGauge],as3935_i2c:["gauge",n.mdiGauge],as3935_spi:["gauge",n.mdiGauge],bme680_bsec:["gauge",n.mdiGauge],bme68x_bsec2_i2c:["gauge",n.mdiGauge],gdk101:["gauge",n.mdiGauge],msa3xx:["gauge",n.mdiGauge],ezo_pmp:["gauge",n.mdiGauge],daly_bms:["gauge",n.mdiGauge],pylontech:["gauge",n.mdiGauge],pipsolar:["gauge",n.mdiGauge],sun_gtil2:["gauge",n.mdiGauge],sml:["gauge",n.mdiGauge],dsmr:["gauge",n.mdiGauge],teleinfo:["gauge",n.mdiGauge],dlms_meter:["gauge",n.mdiGauge],emontx:["gauge",n.mdiGauge],emc2101:["fan",n.mdiFan],gps:["crosshairs-gps",n.mdiCrosshairsGps],sun:["weather-sunny",n.mdiWeatherSunny],opentherm:["thermostat",n.mdiThermostat],uponor_smatrix:["thermostat",n.mdiThermostat],micronova:["thermostat",n.mdiThermostat],sprinkler:["sprinkler-variant",n.mdiSprinklerVariant],sensor:["gauge",n.mdiGauge],binary_sensor:["checkbox-marked-circle-outline",n.mdiCheckboxMarkedCircleOutline],text_sensor:["text-box-outline",n.mdiTextBoxOutline],switch:["toggle-switch-outline",n.mdiToggleSwitchOutline],light:["lightbulb-outline",n.mdiLightbulbOutline],output:["export-variant",n.mdiExportVariant],number:["numeric",n.mdiNumeric],select:["form-dropdown",n.mdiFormDropdown],button:["gesture-tap-button",n.mdiGestureTapButton],fan:["fan",n.mdiFan],cover:["window-shutter",n.mdiWindowShutter],climate:["thermostat",n.mdiThermostat],text:["form-textbox",n.mdiFormTextbox],lock:["lock-outline",n.mdiLockOutline],valve:["valve",n.mdiValve],media_player:["speaker",n.mdiSpeaker],display:["monitor",n.mdiMonitor],lvgl:["monitor",n.mdiMonitor],graphical_display_menu:["monitor",n.mdiMonitor],lcd_menu:["monitor",n.mdiMonitor],datetime:["calendar-clock",n.mdiCalendarClock],camera:["camera-outline",n.mdiCameraOutline],esp32_camera:["camera-outline",n.mdiCameraOutline],esp32_camera_web_server:["camera-outline",n.mdiCameraOutline],camera_encoder:["camera-outline",n.mdiCameraOutline],event:["bell-outline",n.mdiBellOutline],alarm_control_panel:["shield-home-outline",n.mdiShieldHomeOutline],graph:["chart-line",n.mdiChartLine],color:["palette",n.mdiPalette],qr_code:["qrcode",n.mdiQrcode],font:["format-font",n.mdiFormatFont],image:["image-outline",n.mdiImageOutline],online_image:["image-sync-outline",n.mdiImageSyncOutline],animation:["image-multiple-outline",n.mdiImageMultipleOutline]},oC=["shape-outline",n.mdiShapeOutline];function oE(e,t,i){var a;let{item:o,labels:r}=e,{primary:s,secondary:n}=r,d=o.parentKey??o.key;return(0,l.qy)`
    <div
      class="nav-item ${t.selectedLine===o.fromLine?"nav-item--selected":""} ${t.hoveredLine===o.fromLine?"nav-item--hovered":""}"
      @mouseenter=${()=>t.onItemEnter(o)}
      @mouseleave=${()=>t.onItemLeave()}
      @click=${()=>t.onItemClick(o)}
    >
      ${i?"esphome"===(a=d)?(0,l.qy)`<wa-icon
      class="nav-item-icon"
      src=${(0,v.cV)("/assets/logo/esphome-mono.svg")}
      title="ESPHome"
    ></wa-icon>`:(0,l.qy)`<wa-icon
    class="nav-item-icon"
    library="mdi"
    name=${(oz[a]??oC)[0]}
    title=${ok(a)}
  ></wa-icon>`:l.s6}
      <div class="nav-item-content">
        <p>${s}</p>
        ${n?(0,l.qy)`<span class="nav-item-subtitle">${n}</span>`:l.s6}
      </div>
      <wa-icon class="nav-item-chevron" library="mdi" name="chevron-right"></wa-icon>
    </div>
  `}(0,b.C)(Object.fromEntries([...Object.values(oz),oC]));class oq{hostUpdated(){let{selectedLine:e,buckets:t,openSections:i,filtering:a}=this._read();if(null===e){this._scrolledLine=null,this._revealedLine=null;return}if(null!==this._revealedLine&&this._revealedLine!==e&&(this._revealedLine=null),e===this._scrolledLine)return;let o=t.core.some(t=>t.fromLine===e)?0:t.components.some(t=>t.fromLine===e)?1:t.automations.some(t=>t.fromLine===e)?2:-1;if(-1===o){this._scrolledLine=e;return}if(!a&&!i.has(o)&&this._revealedLine!==e){this._revealedLine=e,this._host.dispatchEvent(new CustomEvent("section-reveal",{detail:{index:o},bubbles:!0,composed:!0}));return}this._revealedLine=e;let r=this._host.renderRoot.querySelector(".nav-item--selected");r&&r.getClientRects().length>0&&(r.scrollIntoView({block:"nearest"}),this._scrolledLine=e)}constructor(e,t){this._host=e,this._read=t,this._scrolledLine=null,this._revealedLine=null,e.addController(this)}}function oS(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({close:n.mdiClose});class oA extends l.WF{open(){this._id="",this._error="",this._open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml)}catch(e){this._error=(0,en.u)(e)}}render(){let e=this.boardName?this._localize("device.add_script_dialog_title",{name:this.boardName}):this._localize("device.add_script");return(0,l.qy)`<esphome-base-dialog
      ?open=${this._open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._onRequestClose}
    >
      <p class="intro">
        ${(0,et.G)(this._localize("device.script_header_description"))}
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
          @input=${e=>{this._id=ae(e.target.value),this._error=""}}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._id&&!this._available?.scripts.some(e=>e.id===this._id)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._open=!1,this._id="",this._available=null,this._saving=!1,this._error="",this._onRequestClose=()=>{this._open=!1},this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"script",id:this._id},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{mode:"single"},actions:[]},e,this.yaml),i=e$(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:ew(e)},bubbles:!0,composed:!0})),this._open=!1}catch(t){let e=t instanceof Error?t.message:this._localize("device.automation_save_error");this._error=e,c.A.error(this._localize("device.automation_save_error"),{description:e,richColors:!0})}finally{this._saving=!1}}}}}oA.styles=[m.G,es.z,(0,l.AH)`
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
    `],oS([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oA.prototype,"_localize",void 0),oS([(0,s.Fg)({context:u.Ie})],oA.prototype,"_api",void 0),oS([(0,d.MZ)()],oA.prototype,"boardName",void 0),oS([(0,d.MZ)()],oA.prototype,"configuration",void 0),oS([(0,d.MZ)()],oA.prototype,"yaml",void 0),oS([(0,d.MZ)({attribute:!1})],oA.prototype,"board",void 0),oS([(0,d.wk)()],oA.prototype,"_open",void 0),oS([(0,d.wk)()],oA.prototype,"_id",void 0),oS([(0,d.wk)()],oA.prototype,"_available",void 0),oS([(0,d.wk)()],oA.prototype,"_saving",void 0),oS([(0,d.wk)()],oA.prototype,"_error",void 0),oA=oS([(0,d.EM)("esphome-add-script-dialog")],oA);let oL=(0,l.AH)`
  :host {
    display: block;
  }

  .search {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    margin: var(--wa-space-s) var(--wa-space-s) var(--wa-space-2xs);
    padding: 0 var(--wa-space-s);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-default);
  }

  .search:focus-within {
    border-color: var(--esphome-primary);
  }

  .search-icon {
    font-size: var(--wa-font-size-l);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
  }

  input {
    flex: 1;
    min-width: 0;
    border: none;
    background: transparent;
    color: var(--wa-color-text-normal);
    /* 16px floor avoids iOS focus-zoom in the mobile drawer. */
    font-size: max(16px, var(--wa-font-size-s));
    font-family: inherit;
    padding: var(--wa-space-s) 0;
    outline: none;
  }

  /* The native clear affordance duplicates our own ✕ button. */
  input::-webkit-search-cancel-button {
    display: none;
  }

  .search-clear {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: var(--wa-color-text-quiet);
    cursor: pointer;
    padding: 2px;
    border-radius: var(--wa-border-radius-s);
    flex-shrink: 0;
  }

  .search-clear:hover {
    color: var(--wa-color-text-normal);
  }

  .search-clear wa-icon {
    display: block;
    font-size: var(--wa-font-size-m);
  }

  .search-result {
    margin: var(--wa-space-2xs) var(--wa-space-s) var(--wa-space-xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }
`;function oM(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({magnify:n.mdiMagnify,close:n.mdiClose});class oP extends l.WF{render(){let e=this._localize("device.navigator_search_placeholder");return(0,l.qy)`
      <div class="search">
        <wa-icon class="search-icon" library="mdi" name="magnify"></wa-icon>
        <input
          type="search"
          .value=${this.value}
          placeholder=${e}
          aria-label=${e}
          enterkeyhint="search"
          autocomplete="off"
          autocapitalize="off"
          autocorrect="off"
          spellcheck="false"
          @input=${this._onInput}
          @keydown=${this._onKeydown}
        />
        ${this.value?(0,l.qy)`<button
              type="button"
              class="search-clear"
              @click=${this._clear}
              title=${this._localize("device.navigator_search_clear")}
              aria-label=${this._localize("device.navigator_search_clear")}
            >
              <wa-icon library="mdi" name="close"></wa-icon>
            </button>`:l.s6}
      </div>
      ${this.value&&this.resultLabel?(0,l.qy)`<p class="search-result" role="status">${this.resultLabel}</p>`:l.s6}
    `}_emit(e){this.dispatchEvent(new CustomEvent("navigator-search",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value="",this.resultLabel="",this._onInput=e=>{this.value=e.target.value,this._emit(this.value)},this._onKeydown=e=>{"Escape"===e.key&&this._input?.value&&(e.stopPropagation(),this._clear())},this._clear=()=>{this.value="",this._emit(""),this._input?.focus()}}}function oF(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}oP.styles=[m.G,oL],oM([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oP.prototype,"_localize",void 0),oM([(0,d.MZ)()],oP.prototype,"value",void 0),oM([(0,d.MZ)()],oP.prototype,"resultLabel",void 0),oM([(0,d.P)("input")],oP.prototype,"_input",void 0),oP=oM([(0,d.EM)("esphome-navigator-search")],oP),(0,b.C)({"chevron-down":n.mdiChevronDown,"chevron-left":n.mdiChevronLeft,"chevron-up":n.mdiChevronUp,"chevron-right":n.mdiChevronRight,cog:n.mdiCog,menu:n.mdiMenu,"plus-circle-outline":n.mdiPlusCircleOutline,"script-text-outline":n.mdiScriptTextOutline});class oT extends l.WF{willUpdate(e){if((e.has("yaml")||e.has("platform")||e.has("platformReady"))&&this.yaml&&this.platformReady&&this._kickoffNameResolves(),(e.has("selectedKey")||e.has("yaml")||e.has("selectedFromLine"))&&this.yaml){if(!this.selectedKey){this._selectedLine=null,this._selectedRange=null;return}let e=[...(0,x.MT)(this.yaml),...E(this.yaml)],t=(void 0!==this.selectedFromLine?e.find(e=>e.fromLine===this.selectedFromLine):void 0)??e.find(e=>N(e)===this.selectedKey);t&&(this._selectedLine=t.fromLine,this._selectedRange={fromLine:t.fromLine,toLine:t.toLine})}}render(){let e=this._deriveBuckets(this.yaml),{core:t,components:i,automations:a}=e,o=[{label:this._localize("device.section_core"),desc:this._localize("device.section_core_desc"),icon:ea,items:t,category:"core",actions:[{label:this._localize("device.add_config"),icon:"cog",onClick:()=>this._addConfigDialog.open()}]},{label:this._localize("device.section_components"),desc:this._localize("device.section_components_desc"),icon:eo,items:i,category:"component",actions:[{label:this._localize("device.add_component"),icon:eo,onClick:()=>this._addComponentDialog.open()}]},{label:this._localize("device.section_automations"),desc:this._localize("device.section_automations_desc"),icon:er,items:a,category:"automation",actions:[{label:this._localize("device.add_automation"),icon:er,onClick:()=>this._addAutomationDialog.open()},{label:this._localize("device.add_script"),icon:"script-text-outline",onClick:()=>this._addScriptDialog.open()}]}],r=this._resolveLabels(e,this._caches.tick,this.platform,this.deviceName,this._localize),s=this._query.trim(),n=s.length>0,d=n?r.map(e=>e.filter(({item:e,labels:t})=>(function(e,...t){if(!e)return!0;let i=e.toLowerCase();return t.some(e=>void 0!==e&&e.toLowerCase().includes(i))})(s,t.primary,t.secondary,e.id,e.name))):null,c=o.reduce((e,t)=>e+t.items.length,0),p=d?d.reduce((e,t)=>e+t.length,0):0,h=n&&p>0?this._localize("device.navigator_search_count",{count:p,total:c}):"";return(0,l.qy)`
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
            class="ghost-icon-btn collapse-btn"
            @click=${this._onCollapseClick}
            title=${this._localize("device.hide_navigator")}
            aria-label=${this._localize("device.hide_navigator")}
          >
            <wa-icon library="mdi" name="menu"></wa-icon>
          </button>
        </header>
        <div class="card-body">
          <esphome-navigator-search
            .value=${this._query}
            .resultLabel=${h}
            @navigator-search=${this._onSearchChange}
          ></esphome-navigator-search>
          ${n?l.s6:(0,l.qy)`<p class="italic">${this._localize("device.navigator_desc")}</p>`}
          <div class="separator"></div>
          ${n&&0===p?(0,l.qy)`<p class="nav-empty" role="status">
                ${this._localize("device.navigator_search_none")}
              </p>`:o.map(({label:e,desc:t,icon:i,category:a,actions:o},s)=>{var c;let p=d?.[s]??r[s];return(c={label:e,desc:t,icon:i,actions:o,rows:p,groups:"component"===a?this._groupComponents(p):void 0,collapsedGroups:this._collapsedGroups,onToggleGroup:e=>this._toggleGroup(e),open:!!n||this.openSections.has(s),filtering:n,selectedLine:this._selectedLine,hoveredLine:this._hoveredLine,onToggle:()=>{n||this._toggleSection(s)},onItemEnter:e=>this._onItemHover(e.fromLine,e.fromLine,e.toLine),onItemLeave:()=>this._onItemLeave(),onItemClick:e=>this._onItemClick(e)}).filtering&&0===c.rows.length?l.s6:(0,l.qy)`
    <div class="nav-content" @click=${()=>c.onToggle()}>
      <div class="nav-content-label">
        <wa-icon library="mdi" name=${c.icon}></wa-icon>
        <p>${c.label}</p>
      </div>
      ${c.filtering?l.s6:(0,l.qy)`<wa-icon
            class="nav-content-chevron"
            library="mdi"
            name=${c.open?"chevron-up":"chevron-down"}
          ></wa-icon>`}
    </div>
    ${c.open?(0,l.qy)`
          <div class="separator"></div>
          ${c.filtering?l.s6:(0,l.qy)`<p class="italic">${c.desc}</p>`}
          ${c.groups?c.groups.map(e=>{var t,i;let a,o,r,s;return c.filtering||1!==e.rows.length||e.rows[0].item.platform?(t=e,a=(i=c).filtering||!i.collapsedGroups?.has(t.key),o=!i.filtering,r=()=>{o&&i.onToggleGroup?.(t.key)},s=`navgroup-${t.key}`,(0,l.qy)`
    <div
      class="nav-subgroup-header ${o?"":"nav-subgroup-header--static"}"
      role=${(0,tj.J)(o?"button":void 0)}
      tabindex=${(0,tj.J)(o?"0":void 0)}
      aria-expanded=${(0,tj.J)(o?String(a):void 0)}
      aria-controls=${(0,tj.J)(o?s:void 0)}
      @click=${r}
      @keydown=${e=>{o&&("Enter"===e.key||" "===e.key)&&(e.preventDefault(),r())}}
    >
      <wa-icon
        class="nav-subgroup-icon"
        library="mdi"
        name=${(oz[t.key]??oC)[0]}
      ></wa-icon>
      <span class="nav-subgroup-title">${ok(t.key)}</span>
      <span class="nav-subgroup-count">${t.rows.length}</span>
      ${o?(0,l.qy)`<wa-icon
            class="nav-subgroup-chevron"
            library="mdi"
            name=${a?"chevron-up":"chevron-down"}
          ></wa-icon>`:l.s6}
    </div>
    ${a?(0,l.qy)`<div id=${s} class="nav-items nav-items--grouped">
          ${t.rows.map(e=>oE(e,i,!1))}
        </div>`:l.s6}
  `):(0,l.qy)`<div class="nav-items nav-items--single">
    ${oE(e.rows[0],c,!0)}
  </div>`}):c.rows.length>0?(0,l.qy)`<div class="nav-items">
                  ${c.rows.map(e=>oE(e,c,!0))}
                </div>`:l.s6}
          ${c.filtering?l.s6:(0,l.qy)`<div class="nav-items">
                ${c.actions.map(e=>(0,l.qy)`<div class="action-item" @click=${()=>e.onClick()}>
    <div>
      <wa-icon library="mdi" name=${e.icon}></wa-icon>
      <p>${e.label}</p>
    </div>
    <wa-icon library="mdi" name="plus-circle-outline"></wa-icon>
  </div>`)}
              </div>`}
        `:l.s6}
    <div class="separator"></div>
  `})}
        </div>
      </section>
    `}_toggleSection(e){this.dispatchEvent(new CustomEvent("section-toggle",{detail:{index:e},bubbles:!0,composed:!0}))}_toggleGroup(e){let t=new Set(this._collapsedGroups);t.delete(e)||t.add(e),this._collapsedGroups=t}_kickoffNameResolves(){if(!this._api)return;let{core:e,components:t}=I((0,x.MT)(this.yaml)),i=this.platform||void 0;for(let a of[...e,...t]){let e=N(a);void 0===(0,eT.CQ)(e,i)&&(0,eT.Sn)(this._api,e,i).catch(()=>{})}this._triggerCatalog.ensure()}_onItemHover(e,t,i){this._hoveredLine=e,this._emitHighlight({fromLine:t,toLine:i},!1)}_onItemLeave(){this._hoveredLine=null,this._emitHighlight(this._selectedRange,!1)}_onItemClick(e){let{fromLine:t,toLine:i}=e,a=N(e);this._selectedLine===t?(this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._emitHighlight(this._hoveredLine===t?{fromLine:t,toLine:i}:null,!1),this._emitSectionSelect(null,void 0)):(this.selectedKey=a,this._selectedLine=t,this._selectedRange={fromLine:t,toLine:i},this._emitHighlight({fromLine:t,toLine:i},!0),this._emitSectionSelect(a,t))}_emitHighlight(e,t){this.dispatchEvent(new CustomEvent("yaml-highlight",{detail:{range:e,scroll:t},bubbles:!0,composed:!0}))}_emitSectionSelect(e,t){this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e,fromLine:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._caches=new og(this,[eT.Ej,is]),this._triggerCatalog=new aN(this,()=>({api:this._api,platform:this.platform||void 0,boardId:this.board?.id})),this._reveal=new oq(this,()=>({selectedLine:this._selectedLine,buckets:this._deriveBuckets(this.yaml),openSections:this.openSections,filtering:this._query.trim().length>0})),this.openSections=new Set,this.yaml="",this._deriveBuckets=(0,eU.A)(o_),this._groupComponents=(0,eU.A)(ob),this._resolveLabels=(0,eU.A)((e,t,i,a,o)=>{var r;return r={triggerCatalog:this._triggerCatalog,platform:i,deviceName:a,localize:o,substitutions:e.substitutions},[e.core.map(e=>({item:e,labels:oy(e,"core",r)})),e.components.map(e=>({item:e,labels:oy(e,"component",r)})),e.automations.map(e=>({item:e,labels:oy(e,"automation",r)}))]}),this.board=null,this.boardName="",this.configuration="",this.deviceName="",this.platform="",this.platformReady=!1,this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._hoveredLine=null,this._query="",this._collapsedGroups=new Set,this._onSearchChange=e=>{this._query=e.detail.value},this._onCollapseClick=()=>{this.dispatchEvent(new CustomEvent("nav-collapse",{bubbles:!0,composed:!0}))},this._onAutomationAdded=e=>{e.stopPropagation(),this._emitSectionSelect(e.detail.sectionKey,void 0)}}}oT.styles=[m.G,of],oF([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oT.prototype,"_localize",void 0),oF([(0,s.Fg)({context:u.Ie})],oT.prototype,"_api",void 0),oF([(0,d.MZ)({attribute:!1})],oT.prototype,"openSections",void 0),oF([(0,d.MZ)({attribute:!1})],oT.prototype,"yaml",void 0),oF([(0,d.MZ)({attribute:!1})],oT.prototype,"board",void 0),oF([(0,d.MZ)()],oT.prototype,"boardName",void 0),oF([(0,d.MZ)()],oT.prototype,"configuration",void 0),oF([(0,d.MZ)()],oT.prototype,"deviceName",void 0),oF([(0,d.MZ)()],oT.prototype,"platform",void 0),oF([(0,d.MZ)({type:Boolean})],oT.prototype,"platformReady",void 0),oF([(0,d.P)("esphome-add-config-dialog")],oT.prototype,"_addConfigDialog",void 0),oF([(0,d.P)("esphome-add-component-dialog")],oT.prototype,"_addComponentDialog",void 0),oF([(0,d.P)("esphome-add-automation-dialog")],oT.prototype,"_addAutomationDialog",void 0),oF([(0,d.P)("esphome-add-script-dialog")],oT.prototype,"_addScriptDialog",void 0),oF([(0,d.MZ)({attribute:!1})],oT.prototype,"selectedKey",void 0),oF([(0,d.MZ)({attribute:!1})],oT.prototype,"selectedFromLine",void 0),oF([(0,d.wk)()],oT.prototype,"_selectedLine",void 0),oF([(0,d.wk)()],oT.prototype,"_selectedRange",void 0),oF([(0,d.wk)()],oT.prototype,"_hoveredLine",void 0),oF([(0,d.wk)()],oT.prototype,"_query",void 0),oF([(0,d.wk)()],oT.prototype,"_collapsedGroups",void 0),oT=oF([(0,d.EM)("esphome-device-navigator")],oT),i(536),i(1221),i(6895),i(9786);var oR=i(6029),oD=i(6286);function oO(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,b.C)({"alert-outline":n.mdiAlertOutline});class oI extends l.WF{open(){this._resolvedExit=null,this._open=!0,this._enter.set(!0)}close(){this._open=!1}render(){let e=this._localize("device.yaml_invalid_message",{count:this.errorCount}),t=this.firstErrorLine>0;return(0,l.qy)`
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
            ${e}
            ${this.firstErrorMessage?(0,l.qy)`<div class="first-error">${this.firstErrorMessage}</div>`:l.s6}
          </div>
        </div>
        <div class="actions">
          <button class="btn btn--cancel" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
          <button class="btn btn--goto" ?disabled=${!t} @click=${this._goto}>
            ${this._localize("device.yaml_invalid_go_to_error")}
          </button>
          <button class="btn btn--save-anyway" @click=${this._saveAnyway}>
            ${this._localize("device.yaml_invalid_save_anyway")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_goto(){null===this._resolvedExit&&(this._resolvedExit="goto",this.close(),this.dispatchEvent(new CustomEvent("goto",{detail:{line:this.firstErrorLine,col:this.firstErrorCol},bubbles:!0,composed:!0})))}_saveAnyway(){this._resolvedExit="save-anyway",this.close(),this.dispatchEvent(new CustomEvent("save-anyway",{bubbles:!0,composed:!0}))}_onAfterHide(){this._open=!1,this._enter.set(!1),null===this._resolvedExit&&this.dispatchEvent(new CustomEvent("cancel",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.errorCount=0,this.firstErrorLine=0,this.firstErrorCol=0,this.firstErrorMessage="",this._open=!1,this._resolvedExit=null,this._enter=new oD.J(this,()=>{this.firstErrorLine>0&&this._goto()}),this._onRequestClose=()=>{this._open=!1}}}function oj(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}oI.styles=[m.G,oR.W,(0,l.AH)`
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
    `],oO([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oI.prototype,"_localize",void 0),oO([(0,d.MZ)({type:Number})],oI.prototype,"errorCount",void 0),oO([(0,d.MZ)({type:Number})],oI.prototype,"firstErrorLine",void 0),oO([(0,d.MZ)({type:Number})],oI.prototype,"firstErrorCol",void 0),oO([(0,d.MZ)()],oI.prototype,"firstErrorMessage",void 0),oO([(0,d.wk)()],oI.prototype,"_open",void 0),oI=oO([(0,d.EM)("esphome-yaml-validation-dialog")],oI),(0,b.C)({"arrow-left":n.mdiArrowLeft,"chevron-right":n.mdiChevronRight,menu:n.mdiMenu});class oN extends l.WF{get _device(){return this._devices.find(e=>e.configuration===this.id)??null}_createInstallController(){let e=this;return new h({addController:t=>e.addController(t),removeController:t=>e.removeController(t),requestUpdate:()=>e.requestUpdate(),get updateComplete(){return e.updateComplete},get device(){return e._device},get commandDialog(){return e._commandDialog??null},get firmwareDialog(){return e._firmwareDialog??null}})}get _isYamlDirty(){return this._yaml!==this._savedYaml}get _isDirty(){return this._isYamlDirty||this._sectionDirty}async connectedCallback(){super.connectedCallback(),this._loadPreferences(),(0,f.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("keydown",this._onKeydown),this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),(0,f.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),window.removeEventListener("keydown",this._onKeydown),this._mql.removeEventListener("change",this._onMqlChange),this._unsavedGuard.cancelPending()}_isTextEntry(e){if(!e)return!1;let t=e.tagName;if("INPUT"===t||"TEXTAREA"===t||"SELECT"===t||e.isContentEditable)return!0;let i=e;for(;i;){if("ESPHOME-YAML-EDITOR"===i.tagName)return!0;i=i.parentElement}return!1}updated(e){e.has("id")&&this.id&&(this._justCreated=(0,g.RI)(this.id),this._loadedBoardId=null,this._board=null,this._platformReady=!1,this._loadYaml());let t=this._device?.board_id??null;t&&t!==this._loadedBoardId?(this._loadedBoardId=t,this._board=null,this._platformReady=!1,this._loadBoard(t)):!t&&(null!==this._loadedBoardId&&(this._loadedBoardId=null,this._board=null),(null!==this._device||this._devicesLoaded)&&(this._platformReady=!0))}async _loadPreferences(){let e=localStorage.getItem("esphome-editor-layout");("both"===e||"left"===e||"right"===e)&&(this._layout=e);try{let e=await this._api.getPreferences();this._navCollapsed=!e.navigator_visible}catch{}}async _loadBoard(e){try{let t=await this._api.getBoard(e);this._loadedBoardId===e&&(this._board=t,this._platformReady=!0)}catch(t){console.error("Failed to load board:",t),this._loadedBoardId===e&&(this._board=null,this._platformReady=!0)}}async _loadYaml(){try{let e=await this._api.getConfig(this.id);this._yaml=e,this._savedYaml=e,this._maybeResolveLineFromUrl()}catch(e){console.error("Failed to load YAML:",e)}}_maybeResolveLineFromUrl(){let e=K(this._yaml,this._selectedFromLine,this._selectedSection);e&&(this._selectedSection=e.sectionKey,this._highlightRange=e.range,this._scrollToHighlight=!0)}_resolveValidationPrompt(e){let t=this._pendingValidationResolve;this._pendingValidationResolve=null,t?.(e)}render(){let e=this._device?.friendly_name||this._device?.name||this.id||this._localize("dashboard.create_device"),t=this._isMobile?!this._drawerOpen:this._navCollapsed,i=this._localize("device.back");return(0,l.qy)`
      <!-- Mobile drawer -->
      <div
        class="drawer-backdrop ${this._drawerOpen?"drawer-backdrop--open":""}"
        @click=${()=>{this._drawerOpen=!1}}
      ></div>
      <div
        class="drawer ${this._drawerOpen?"drawer--open":""}"
        @section-toggle=${this._onSectionToggle}
        @section-reveal=${this._onSectionReveal}
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
          @section-reveal=${this._onSectionReveal}
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
            ${t||this._selectedSection?(0,l.qy)`<div slot="header-start" class="header-start-group">
                  ${t?(0,l.qy)`<button
                        type="button"
                        class="ghost-icon-btn nav-toggle-btn"
                        @click=${this._onNavExpand}
                        title=${this._localize("device.show_navigator")}
                        aria-label=${this._localize("device.show_navigator")}
                      >
                        <wa-icon library="mdi" name="menu"></wa-icon>
                      </button>`:l.s6}
                  ${this._selectedSection?(0,l.qy)`<button
                        class="ghost-icon-btn back-btn"
                        @click=${this._onBack}
                        title=${i}
                        aria-label=${i}
                      >
                        <wa-icon library="mdi" name="arrow-left"></wa-icon>
                      </button>`:l.s6}
                </div>`:l.s6}
          </esphome-device-editor>
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
      </div>
    `}_onSectionToggle(e){let{index:t}=e.detail,i=new Set;this._openSections.has(t)||i.add(t),this._openSections=i,this._updateUrl()}_onSectionReveal(e){let{index:t}=e.detail;this._openSections.has(t)||(this._openSections=new Set([t]),this._updateUrl())}_onNavSectionShow(e){let t={core:0,components:1,automations:2}[e.detail.section];if(void 0===t)return;let i=new Set([t]);this._openSections=i,this._updateUrl(),this._drawerOpen=!0,this._navCollapsed&&(this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{}))}_onLayoutChange(e){this._layout=e.detail,localStorage.setItem("esphome-editor-layout",e.detail)}_renderNavigator(e){return(0,l.qy)`<esphome-device-navigator
      class=${e}
      .openSections=${this._openSections}
      .yaml=${this._yaml}
      .board=${this._board}
      .boardName=${this._board?.name??""}
      .configuration=${this.id}
      .deviceName=${this._device?.name??""}
      .platform=${this._board?.esphome.platform??""}
      .platformReady=${this._platformReady}
      .selectedKey=${this._selectedSection}
      .selectedFromLine=${this._selectedFromLine}
    ></esphome-device-navigator>`}_onYamlChange(e){this._yaml=e.detail.value,this._retryPendingFieldLine()}_onYamlCursorLine(e){this._clearPendingFieldLine();let t=j(this._yaml,e.detail.line);if(!t)return;let i=e.detail.path??[],a=i.length>1&&y.sU.has(i[0])?i:i.slice(1),o=N(t);if(o===this._selectedSection&&t.fromLine===this._selectedFromLine){this._focusFieldPath=a;return}this._guardSectionSwitch(()=>{this._selectedSection=o,this._selectedFromLine=t.fromLine,this._focusFieldPath=a,this._updateUrl()})}_focusedSection(){if(!this._selectedSection)return;let e=(0,x.MT)(this._yaml);return(void 0!==this._selectedFromLine?e.find(e=>e.fromLine===this._selectedFromLine):void 0)??e.find(e=>N(e)===this._selectedSection)}_highlightFieldLine(e){let t=this._focusedSection(),i=t?(0,x.of)(this._yaml,t,e):null;return null!==i&&(this._highlightRange={fromLine:i,toLine:i},this._scrollToHighlight=!0),{section:t,found:null!==i}}_onFieldFocus(e){let t=this._focusedFieldPath=e.detail.path;if(!t.length)return;let{section:i,found:a}=this._highlightFieldLine(t);a?this._clearPendingFieldLine():(this._pendingFieldLine=!0,this._pendingFieldSection={section:this._selectedSection,fromLine:this._selectedFromLine},this._highlightRange=i?{fromLine:i.fromLine,toLine:i.toLine}:null,this._scrollToHighlight=void 0!==i)}_retryPendingFieldLine(){if(this._pendingFieldLine&&this._focusedFieldPath?.length){if(this._pendingFieldSection?.section!==this._selectedSection||this._pendingFieldSection?.fromLine!==this._selectedFromLine)return void this._clearPendingFieldLine();this._highlightFieldLine(this._focusedFieldPath).found&&this._clearPendingFieldLine()}}_clearPendingFieldLine(){this._pendingFieldLine=!1,this._pendingFieldSection=void 0}_onYamlHighlight(e){this._highlightRange=e.detail.range,this._scrollToHighlight=e.detail.scroll}_onYamlUpdated(e){this._yaml=e.detail.yaml,this._savedYaml=e.detail.yaml}_onYamlDraft(e){this._yaml=e.detail.yaml,this._retryPendingFieldLine()}_onSectionSelect(e){let{sectionKey:t,fromLine:i}=e.detail;if(t===this._selectedSection&&i===this._selectedFromLine){this._drawerOpen=!1;return}this._guardSectionSwitch(()=>{let e=this._selectedSection,a=this._selectedFromLine;null===t?this._sectionHistory=[]:null!==e&&(this._sectionHistory=[...this._sectionHistory,{key:e,fromLine:a}]),this._selectedSection=t,this._selectedFromLine=i,this._drawerOpen=!1,this._updateUrl()})}_guardSectionSwitch(e){this._activeSection?.flushPending(),e()}_readUrlParam(e,t){return new URLSearchParams(window.location.search).get(e)??t}_readUrlLine(){let e=new URLSearchParams(window.location.search).get("line");if(!e)return;let t=Number(e);return Number.isNaN(t)?void 0:t}_readUrlSections(){let e=new URLSearchParams(window.location.search).get("open");return e?e.split(",").map(Number).filter(e=>!Number.isNaN(e)):[]}_updateUrl(){let e=new URLSearchParams(window.location.search);this._selectedSection?(e.set("section",this._selectedSection),void 0!==this._selectedFromLine?e.set("line",String(this._selectedFromLine)):e.delete("line")):(e.delete("section"),e.delete("line")),this._openSections.size>0?e.set("open",[...this._openSections].join(",")):e.delete("open");let t=e.toString(),i=`${window.location.pathname}${t?`?${t}`:""}`;window.history.replaceState(window.history.state,"",i)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._devicesLoaded=!1,this._activeJobs=new Map,this.id="",this._justCreated=!1,this._layout="both",this._openSections=new Set(this._readUrlSections()),this._board=null,this._platformReady=!1,this._loadedBoardId=null,this._highlightRange=null,this._scrollToHighlight=!1,this._selectedSection=this._readUrlParam("section",null),this._selectedFromLine=this._readUrlLine(),this._pendingFieldLine=!1,this._sectionHistory=[],this._drawerOpen=!1,this._navCollapsed=!1,this._isMobile=window.matchMedia("(max-width: 900px)").matches,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._yaml="",this._savedYaml="",this._activeSection=null,this._sectionDirty=!1,this._validationErrorCount=0,this._validationFirstLine=0,this._validationFirstCol=0,this._validationFirstMessage="",this._onPostInstallShowLogs=(0,_.ei)(()=>this._logsDialog,()=>this._localize),this._installCtrl=this._createInstallController(),this._unsavedGuard=new w._,this._allowingLeave=!1,this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._confirmLeave=async()=>{this._activeSection?.flushPending();let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>(!this._isYamlDirty||!!await this._saveYaml())&&(this._allowingLeave=!0,!0)});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._activeSection?.flushPending(),this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._activeSection?.flushPending(),this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,v.cV)(`/device/${this.id}`)),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onKeydown=e=>{if("Escape"!==e.key||e.defaultPrevented)return;let t=e.composedPath()[0];if(!this._isTextEntry(t)){if(this._drawerOpen){e.preventDefault(),this._drawerOpen=!1;return}e.preventDefault(),window.history.back()}},this._dismissJustCreated=()=>{this._justCreated=!1},this._onChangeBoard=async e=>{let t=e.detail?.boardId,i=this._device;if(t&&i&&t!==i.board_id){if(this._isDirty)return void c.A.error(this._localize("device.change_board_unsaved"),{richColors:!0});try{await this._api.updateDevice({configuration:i.configuration,board_id:t}),await this._loadYaml(),c.A.success(this._localize("device.change_board_success"),{richColors:!0})}catch(e){console.error("Failed to change board:",e),c.A.error(this._localize("device.change_board_error"),{richColors:!0})}}},this._pendingValidationResolve=null,this._saveYaml=async()=>{if(await this._activeSection?.flushPending(),!this._isYamlDirty)return!0;if(this.id)try{let e=(0,Z.mL)(this.id,this._yaml)??await this._api.validateYaml(this.id,this._yaml),t=function(e){let t=e.yaml_errors??[],i=e.validation_errors??[],a=t.length+i.length;if(0===a)return{count:0,first:null};if(t.length>0){let e=(t[0].message??"").trim(),i=0,o=0,r=e.match(U);if(r)i=Number.parseInt(r[1],10),o=Number.parseInt(r[2],10);else{let t=e.match(H);t&&(i=Number.parseInt(t[1],10))}return(!Number.isFinite(i)||i<1)&&(i=0),(!Number.isFinite(o)||o<1)&&(o=0),{count:a,first:{line:i,col:o,message:e||"Invalid YAML"}}}let o=i[0],r=Math.max(1,(o.range?.start_line??0)+1),s=Math.max(1,(o.range?.start_col??0)+1);return{count:a,first:{line:r,col:s,message:(o.message??"Invalid configuration").trim()}}}(e);if(t.count>0)return this._validationErrorCount=t.count,this._validationFirstLine=t.first?.line??0,this._validationFirstCol=t.first?.col??0,this._validationFirstMessage=t.first?.message??"",this._pendingValidationResolve?.(!1),new Promise(e=>{this._pendingValidationResolve=e,this._yamlValidationDialog.open()})}catch(e){console.debug("[save-yaml] validate_yaml failed, saving anyway:",e)}return this._doSaveYaml()},this._doSaveYaml=async()=>{let e=this._savedYaml;this._savedYaml=this._yaml;let t=!0;try{await this._api.updateConfig(this.id,this._yaml)}catch(i){(i instanceof Error?i.message:"").includes("timed out")||(t=!1,this._savedYaml=e,console.error("Failed to save YAML:",i))}let i=t?"device.yaml_saved":"device.yaml_save_error";return(t?c.A.success:c.A.error)(this._localize(i),{richColors:!0}),t},this._onValidationSaveAnyway=async()=>{let e=await this._doSaveYaml();this._resolveValidationPrompt(e)},this._onValidationGoTo=e=>{let t=e.detail.line;if(t&&t>=1){"left"===this._layout&&(this._layout="both",localStorage.setItem("esphome-editor-layout","both")),this._highlightRange={fromLine:t,toLine:t},this._scrollToHighlight=!0;let e=K(this._yaml,t,null);e&&(this._selectedSection=e.sectionKey)}this._resolveValidationPrompt(!1)},this._onValidationCancel=()=>{this._resolveValidationPrompt(!1)},this._onValidateClick=()=>{this._device&&(this._commandDialog.configuration=this._device.configuration,this._commandDialog.name=this._device.friendly_name||this._device.name,this._commandDialog.open("validate"))},this._onCleanBuild=e=>{let t=e.detail;this._commandDialog.configuration=t.configuration,this._commandDialog.name=t.friendly_name||t.name,this._commandDialog.open("clean")},this._onRequestOpenEditor=e=>{e.stopPropagation(),e.detail.configuration!==this._device?.configuration&&(0,f.oo)(`/device/${encodeURIComponent(e.detail.configuration)}`)},this._onBack=()=>{this._guardSectionSwitch(()=>{let e=this._sectionHistory.length?this._sectionHistory[this._sectionHistory.length-1]:null;e?(this._sectionHistory=this._sectionHistory.slice(0,-1),this._selectedSection=e.key,this._selectedFromLine=e.fromLine):(this._selectedSection=null,this._selectedFromLine=void 0),this._highlightRange=null,this._scrollToHighlight=!1,this._updateUrl()})},this._onNavExpand=()=>{if(this._isMobile){this._drawerOpen=!0;return}this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{})},this._onNavCollapse=()=>{if(this._isMobile){this._drawerOpen=!1;return}this._navCollapsed=!0,this._api.updatePreferences({navigator_visible:!1}).catch(()=>{})},this._onSectionMount=e=>{this._activeSection=e.detail.node,this._sectionDirty=e.detail.node.dirty},this._onSectionUnmount=e=>{this._activeSection===e.detail.node&&(this._activeSection=null,this._sectionDirty=!1)},this._onSectionDirtyChange=e=>{this._sectionDirty=e.detail.dirty}}}oN.styles=[m.G,V],oj([(0,s.Fg)({context:u.$F,subscribe:!0}),(0,d.wk)()],oN.prototype,"_localize",void 0),oj([(0,s.Fg)({context:u.xJ,subscribe:!0}),(0,d.wk)()],oN.prototype,"_devices",void 0),oj([(0,s.Fg)({context:u.UL,subscribe:!0}),(0,d.wk)()],oN.prototype,"_devicesLoaded",void 0),oj([(0,s.Fg)({context:u.Ie})],oN.prototype,"_api",void 0),oj([(0,s.Fg)({context:u.EM,subscribe:!0}),(0,d.wk)()],oN.prototype,"_activeJobs",void 0),oj([(0,d.MZ)()],oN.prototype,"id",void 0),oj([(0,d.wk)()],oN.prototype,"_justCreated",void 0),oj([(0,d.wk)()],oN.prototype,"_layout",void 0),oj([(0,d.wk)()],oN.prototype,"_openSections",void 0),oj([(0,d.wk)()],oN.prototype,"_board",void 0),oj([(0,d.wk)()],oN.prototype,"_platformReady",void 0),oj([(0,d.wk)()],oN.prototype,"_highlightRange",void 0),oj([(0,d.wk)()],oN.prototype,"_scrollToHighlight",void 0),oj([(0,d.wk)()],oN.prototype,"_selectedSection",void 0),oj([(0,d.wk)()],oN.prototype,"_selectedFromLine",void 0),oj([(0,d.wk)()],oN.prototype,"_focusFieldPath",void 0),oj([(0,d.wk)()],oN.prototype,"_sectionHistory",void 0),oj([(0,d.wk)()],oN.prototype,"_drawerOpen",void 0),oj([(0,d.wk)()],oN.prototype,"_navCollapsed",void 0),oj([(0,d.wk)()],oN.prototype,"_isMobile",void 0),oj([(0,d.wk)()],oN.prototype,"_yaml",void 0),oj([(0,d.wk)()],oN.prototype,"_savedYaml",void 0),oj([(0,d.P)("esphome-unsaved-changes-dialog")],oN.prototype,"_unsavedDialog",void 0),oj([(0,d.wk)()],oN.prototype,"_sectionDirty",void 0),oj([(0,d.P)("esphome-command-dialog")],oN.prototype,"_commandDialog",void 0),oj([(0,d.P)("esphome-firmware-install-dialog")],oN.prototype,"_firmwareDialog",void 0),oj([(0,d.P)("esphome-logs-dialog")],oN.prototype,"_logsDialog",void 0),oj([(0,d.P)("esphome-yaml-validation-dialog")],oN.prototype,"_yamlValidationDialog",void 0),oj([(0,d.wk)()],oN.prototype,"_validationErrorCount",void 0),oj([(0,d.wk)()],oN.prototype,"_validationFirstLine",void 0),oj([(0,d.wk)()],oN.prototype,"_validationFirstCol",void 0),oj([(0,d.wk)()],oN.prototype,"_validationFirstMessage",void 0),oN=oj([(0,d.EM)("esphome-page-device")],oN)}}]);
//# sourceMappingURL=115.08ade894f66e1968.js.map