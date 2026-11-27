"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[180],{6791(e,t,i){i.r(t),i.d(t,{ESPHomePageDevice:()=>oE});var o=i(9104),a=i(289),s=i(5077),r=i(9356),n=i(2971),l=i(9898),d=i(1502),c=i(3835),h=i(2765),p=i(418),u=i(2497),_=i(8041);async function m(e,t,i,o,a,s){let{yaml_diff:r}=await e.deleteAutomation(t,i,o),n=(0,_.lX)(o,r);await e.updateConfig(t,n),a(s(),{configuration:t,yaml:n,basedOn:o,removed:{kind:"automation",location:i}})}function v(e,t){let i=(0,h.D)(e),o=(0,h.D)(t),a=0;for(;a<o.length&&i[a]===o[a];)a++;let s=i.length-1,r=o.length-1;for(;r>=a&&s>=a&&i[s]===o[r];)s--,r--;return r>=a?null:i.slice(a,s+1)}var g=i(6668),f=i(8584),y=i(8159),b=i(2854),w=i(8267),$=i(2834),k=i(1079);class x{hostConnected(){}get deviceState(){return this._host.device?.runtime_state.state??g.g.UNKNOWN}get deviceTargetPlatform(){return this._host.device?.target_platform??""}get platformInstalls(){return(0,f.aE)(this._host.device)}get deviceCurrentAddress(){return this._host.device?.ip||this._host.device?.address||""}get canFlashBootloader(){return(0,y.A)(this._host.device)}get neverFlashed(){return(0,w.g)(this._host.device)}get otaNeedsUsb(){return(0,$.K)(this._host.device)}_logsHost(e){return{api:this._host.api,logsDialog:e,localize:this._host.localize}}_openCommand(e,t,i,o){"install"===t&&this._host.openActiveJobProgress()||this._host.commandDialog?.openForDevice(e,t,{port:i,...o})}constructor(e){this.installMethodOpen=!1,this.methodMode="install",this.onInstall=()=>{!this._host.device||this._host.openActiveJobProgress()||(this.methodMode="install",this.installMethodOpen=!0,this._host.requestUpdate())},this.onLogs=()=>{let e=this._host.device,t=this._host.logsDialog;e&&t&&(0,b.r)(this._logsHost(t),e,()=>{this.methodMode="logs",this.installMethodOpen=!0,this._host.requestUpdate()})},this.onUpdate=()=>{let e=this._host.device;if(e){if((0,$.K)(e))return void this.onInstall();this._openCommand(e,"install")}},this.onInstallMethodClose=()=>{this.installMethodOpen=!1,this.methodMode="install",this._host.requestUpdate()},this.onInstallMethodSelect=e=>{let t=this._host.device,i=this.methodMode;if(this.installMethodOpen=!1,this.methodMode="install",this._host.requestUpdate(),!t)return;let{method:o,port:a}=e.detail;if("logs"===i){let e=this._host.logsDialog;if(!e)return;(0,b.e)(this._logsHost(e),t,o,a);return}this._host.openActiveJobProgress()||(0,k.D)(o,a,{device:t,firmwareDialog:this._host.firmwareDialog,openInstall:(e,i)=>this._openCommand(t,"install",e,i)})},this._host=e,e.addController(this)}}var z=i(9877);function C(e,t,i){let o=(0,z.wS)(t,i);return"central"===e&&"right"===o?i?"left":"both":"yaml"===e&&"left"===o?i?"right":"both":null}var S=i(3425),F=i(8451),P=i(1556),q=i(4835),M=i(3140),L=i(2812),R=i(9363),A=i(5084),E=i(7051),T=i(157),D=i(2439),O=i(3632),U=i(1529),B=i(918),Z=i(9748),I=i(1093),K=i(3854),j=i(2814),V=i(8360),Y=i(9317),N=i(3682);function G(e,t){if(void 0===t||!Number.isInteger(t)||t<1||!e)return null;let i=(0,u.VN)(e,t);return i?{sectionKey:(0,u.gU)(i),sectionFromLine:i.fromLine,range:{fromLine:t,toLine:t}}:null}var H=i(332),W=i(9757),J=i(2761),X=i(1254),Q=i(6689),ee=i(9808),et=i(8310),ei=i(8851);let eo=/^\s*name_add_mac_suffix\s*:/,ea=/^(\s*name_add_mac_suffix\s*:\s*)([^#\s]+)/;function es(e){let t=e.split("\n"),i=er(t);return i<0?null:(t[i]=t[i].replace(ea,"$1false"),t.join("\n"))}function er(e){let t=(0,et.zZ)(e,"esphome",ea);if(t<0)return -1;let i=ea.exec(e[t]);return null!==i&&!0===(0,ei.FY)((0,ee.Ir)(i[2]))?t:-1}var en=i(9789),el=i(4125);let ed=/^encryption\s*:/,ec=/^password\s*:/,eh=/^platform\s*:/,ep=/^key\s*:/;function eu(e){let t=(0,h.D)(e),i=eg(e,t);if(!i||i.encryptionLine>=0||i.multiLine)return null;let o=/^(\s*-\s+)password\s*:(.*)$/.exec(t[i.line]);o&&(t[i.line]=`${o[1]}encryption:${(0,ee.bw)(o[2]).comment}`);let a=(0,et.zZ)(t,"ota",eh,i.line+1),s=em(t,ec,i.line+1);if(!o){let e=s>=0?s:a>=0?a+1:i.line+1;t.splice(e,0,`${i.childIndent}encryption:`)}return t.join((0,h.y)(e))}function e_(e){let t=(0,h.D)(e),i=eg(e,t);return!i||i.keyLine<0||i.multiLine?null:(em(t,ep,i.encryptionLine+1),t.join((0,h.y)(e)))}function em(e,t,i){let o=-1;for(let a=ev(e,t,i);a>=0;)e.splice(a,1),o=a,a=ev(e,t,i);return o}function ev(e,t,i){let o=(0,et.zZ)(e,"ota",t,i);return o===i-1?-1:o}function eg(e,t){let i=(0,el.MT)(e).find(e=>"ota"===e.key&&"esphome"===e.platform);if(!i)return null;let o=i.fromLine-1,a=(0,et.zZ)(t,"ota",ed,i.fromLine),s=(0,et.zZ)(t,"ota",ec,i.fromLine),r=a>=0?(0,et.zZ)(t,"ota",ep,a+1):-1,n=(0,en.eq)(t,o,void 0!==i.parentKey);return{line:o,childIndent:n,encryptionLine:a,passwordLine:s,keyLine:r,multiLine:s>=0&&ef(t,s,s===o?n:"")||r>=0&&ef(t,r,"")}}function ef(e,t,i){if(en.PL.test(e[t]))return!0;let o=Math.max((0,el.p0)(e[t]),i.length);for(let i=t+1;i<e.length;i++)if(!(0,en.BJ)(e[i]))return(0,el.p0)(e[i])>o;return!1}var ey=i(5091);let eb=(0,s.AH)`
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

  /* Load ladder in place of the editor: the grid holds a message and an
     optional action button instead of the nav + editor columns, so drop
     the column split and the 1px gap's border colour. */
  .layout-grid.load-state {
    grid-template-columns: 1fr;
    align-content: center;
    justify-items: center;
    gap: var(--wa-space-m);
    background: var(--wa-color-surface-default);
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
`;i(9577),i(9218),i(2522),i(9968),i(7441);var ew=i(6734),e$=i(3330),ek=i(4818);let ex="esphome-editor-split-ratio",ez=e=>Math.min(.75,Math.max(.25,e)),eC=e=>{try{localStorage.setItem(ex,String(e))}catch{}};var eS=i(8612);function eF(e,t,i,o=""){let a=e(t?"device.yaml_mask_sensitive":"device.yaml_reveal_sensitive");return(0,s.qy)`<button
      id="btn-reveal-sensitive"
      type="button"
      class="ghost-icon-btn ${o}"
      aria-pressed=${t}
      aria-label=${a}
      @click=${i}
    >
      <wa-icon library="mdi" name=${t?"eye-off":"eye"}></wa-icon>
    </button>
    <wa-tooltip for="btn-reveal-sensitive">${a}</wa-tooltip>`}i(1306),(0,I.C)({eye:a.mdiEye,"eye-off":a.mdiEyeOff});let eP=(0,s.AH)`
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
    min-width: 0;
  }

  .editor-header-file {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-normal);
    color: var(--esphome-primary);
    min-width: 0;
    /* Yield before the device name when the header is tight; the
       filename is the secondary half of the title row. */
    flex-shrink: 2;
  }

  .editor-floating-actions {
    position: absolute;
    bottom: var(--wa-space-xs);
    right: var(--wa-space-xs);
    z-index: 10;
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .save-button,
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

  .install-split {
    display: inline-flex;
    align-items: stretch;
  }

  /* Join the two halves into one split control: square the inner corners and
     overlap the seam by one border width so both buttons keep a full border.
     The hovered / focused half is raised so it owns a single, consistent seam
     colour (without the overlap, the seam keeps the un-hovered border). */
  .install-split__main,
  .install-split__caret {
    position: relative;
  }

  .install-split__main {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }

  .install-split__caret {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    margin-left: calc(-1 * var(--wa-border-width-s));
    padding-left: 8px;
    padding-right: 8px;
    gap: 0;
  }

  .install-split__main:hover:not(:disabled),
  .install-split__caret:hover:not(:disabled),
  .install-split__main:focus-visible,
  .install-split__caret:focus-visible {
    z-index: 1;
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

  /* In sync: nothing to apply, so drop the primary tint to a neutral, still
     usable button (you can re-flash, but the config matches the firmware). */
  .install-fab--muted {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    border-color: var(--wa-color-surface-border);
  }

  .install-fab--muted:hover:not(:disabled) {
    background: var(--wa-color-surface-raised);
    border-color: color-mix(in srgb, var(--wa-color-text-normal), transparent 70%);
  }

  /* Single size for every glyph; the fixed slot below derives its
     box from this one font-size, so there's nothing to keep in sync. */
  .save-button wa-icon,
  .save-button wa-spinner,
  .install-fab wa-icon {
    font-size: 16px;
  }

  /* Pin both the idle icon and the in-flight spinner to the same 1em
     square so swapping them can't reflow the button. wa-icon and
     wa-spinner measure differently on their own, hence both here. */
  .save-button wa-icon,
  .save-button wa-spinner {
    box-sizing: border-box;
    flex: none;
    width: 1em;
    height: 1em;
  }

  .save-button wa-spinner {
    --track-width: 2px;
    --indicator-color: currentColor;
    --track-color: color-mix(in srgb, currentColor 30%, transparent);
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

  /* The floating Install / Validate / Save row overlays the bottom-right and
     must sit BELOW the content, never over it. Reserve room below: button
     bottom inset (var(--wa-space-xs)) + button height (2.25rem) + a matching
     gap. Applies to the code editor (right pane) and the board-info-only layout
     where the row overlaps the full-width left pane. */
  .editor-pane--right,
  .editor-layout--left .editor-pane--left {
    padding-bottom: calc(2.25rem + var(--wa-space-xs) * 2);
  }

  /* The code editor brings its own line-number gutter, so the full
     var(--wa-space-m) inset the config form needs reads as wasted padding that
     shrinks the text area. Trim the editor pane to a tighter, even inset on the
     top + sides; the bottom keeps the action-row reserve above. */
  .editor-pane--right {
    position: relative;
    padding-top: var(--wa-space-xs);
    padding-inline: var(--wa-space-xs);
  }

  .editor-pane-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
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
`;var eq=i(6048);i(8768);var eM=i(8914),eL=i(5343);function eR(e,t){let i=e.split("\n"),o=t.split("\n"),a=i.length,s=o.length,r=[];for(let e=0;e<=a;e++)r.push(new Uint32Array(s+1));for(let e=1;e<=a;e++)for(let t=1;t<=s;t++)r[e][t]=i[e-1]===o[t-1]?r[e-1][t-1]+1:Math.max(r[e-1][t],r[e][t-1]);let n=[],l=a,d=s;for(;l>0||d>0;)l>0&&d>0&&i[l-1]===o[d-1]?(n.push({type:"context",oldLine:l,newLine:d,content:i[l-1]}),l--,d--):d>0&&(0===l||r[l][d-1]>=r[l-1][d])?(n.push({type:"add",newLine:d,content:o[d-1]}),d--):(n.push({type:"remove",oldLine:l,content:i[l-1]}),l--);return n.reverse()}var eA=i(7883);function eE(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}function eT(e){let t=new Map;for(let i of(0,eA.H)(e)){let e=t.get(i.line);e?e.push(i):t.set(i.line,[i])}return t}class eD extends s.WF{render(){if(this._darkMode?this.setAttribute("dark",""):this.removeAttribute("dark"),this.oldValue===this.newValue)return(0,s.qy)`<div class="empty">${this._localize("device.diff_no_changes")}</div>`;let e=this._diffLines(this.oldValue,this.newValue),t=this.revealSensitive?void 0:this._oldMasks(this.oldValue),i=this.revealSensitive?void 0:this._newMasks(this.newValue);return(0,s.qy)`
      <table>
        <tbody>
          ${e.map(e=>this._renderLine(e,t,i))}
        </tbody>
      </table>
    `}_renderLine(e,t,i){let o="add"===e.type?"+":"remove"===e.type?"-":" ",a="remove"===e.type?e.oldLine:e.newLine,r=void 0===e.oldLine?void 0:t?.get(e.oldLine),n=void 0===e.newLine?void 0:i?.get(e.newLine);return(0,s.qy)`
      <tr class=${e.type}>
        <td class="gutter">${a??(0,s.qy)`&nbsp;`}</td>
        <td class="marker">${o}</td>
        <td class="content">${this._renderContent(e.content,n??r)}</td>
      </tr>
    `}_renderContent(e,t){if(!t?.length)return e||s.s6;let i=[],o=0;for(let{valueFrom:a,valueTo:r}of t)a>o&&i.push(e.slice(o,a)),i.push((0,s.qy)`<span class="sensitive">${e.slice(a,r)}</span>`),o=r;return o<e.length&&i.push(e.slice(o)),i}constructor(...e){super(...e),this._darkMode=(0,eL.yk)(),this._localize=e=>e,this.oldValue="",this.newValue="",this.revealSensitive=!1,this._diffLines=(0,d.A)(eR),this._oldMasks=(0,d.A)(eT),this._newMasks=(0,d.A)(eT)}}eD.styles=(0,s.AH)`
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

    .content .sensitive {
      ${eM.V}
    }
  `,eE([(0,o.Fg)({context:P.B6,subscribe:!0}),(0,r.wk)()],eD.prototype,"_darkMode",void 0),eE([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],eD.prototype,"_localize",void 0),eE([(0,r.MZ)()],eD.prototype,"oldValue",void 0),eE([(0,r.MZ)()],eD.prototype,"newValue",void 0),eE([(0,r.MZ)({type:Boolean})],eD.prototype,"revealSensitive",void 0),eD=eE([(0,r.EM)("esphome-yaml-diff")],eD),i(9931);var eO=i(6254),eU=i(8259),eB=i(9728);function eZ(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({broom:a.mdiBroom,"check-circle-outline":a.mdiCheckCircleOutline,"dots-vertical":a.mdiDotsVertical,memory:a.mdiMemory,"open-in-new":a.mdiOpenInNew,"text-box-outline":a.mdiTextBoxOutline});class eI extends eB.o{render(){let e=this._localize("device.actions_menu");return(0,s.qy)`
      <button
        type="button"
        class="menu-btn"
        @click=${this._toggle}
        title=${e}
        aria-label=${e}
        aria-haspopup="menu"
        aria-expanded=${this._open?"true":"false"}
      >
        <wa-icon library="mdi" name="dots-vertical"></wa-icon>
      </button>
      ${this._open?(0,s.qy)`
              <div class="backdrop" @click=${this._close}></div>
              <!-- Opens upward, so DOM order inverts distance from the
                   trigger: frequent actions (Logs) last / nearest the
                   click, rare ones (Analyze memory, Clean build) first /
                   furthest. -->
              <div class="menu" role="menu">
                ${this._expertMode?this._renderItem({icon:"memory",labelKey:"dashboard.action_analyze_memory",onSelect:this._onAnalyzeMemory,disabledTitle:this.busy?this._localize("dashboard.action_analyze_memory_busy"):this.validateDisabled?this._localize("device.analyze_memory_disabled_pending"):null}):s.s6}
                ${this._renderItem({icon:"broom",labelKey:"dashboard.action_clean_build",onSelect:this._onCleanBuild,disabledTitle:this.busy?this._localize("dashboard.action_clean_build_busy"):null})}
                <div class="menu-divider" role="separator"></div>
                ${this.webUiUrl?(0,eU.w)(this.webUiUrl,this._localize,{className:"menu-item menu-item--link",onClick:this._close,withLabel:!0,role:"menuitem"}):s.s6}
                ${this._renderItem({icon:"check-circle-outline",labelKey:"device.validate",onSelect:this._onValidate,disabledTitle:this.validateDisabled?this._localize("device.validate_disabled_pending"):null})}
                ${this._renderItem({icon:"text-box-outline",labelKey:"device.show_logs",onSelect:this._onLogs,disabledTitle:null})}
              </div>
            `:s.s6}
    `}_renderItem(e){let t=null!==e.disabledTitle;return(0,s.qy)`
      <div
        class="menu-item ${t?"menu-item--disabled":""}"
        role="menuitem"
        tabindex=${t?"-1":"0"}
        aria-disabled=${t?"true":"false"}
        title=${e.disabledTitle??s.s6}
        @click=${t?void 0:e.onSelect}
        @keydown=${t?void 0:this._onItemKeydown}
      >
        <wa-icon library="mdi" name=${e.icon}></wa-icon>
        <span class="menu-item-label">${this._localize(e.labelKey)}</span>
      </div>
    `}constructor(...e){super(...e),this._localize=e=>e,this._expertMode=!1,this.busy=!1,this.validateDisabled=!1,this.webUiUrl="",this._onLogs=()=>{this._close(),this._emit("open-logs")},this._onValidate=()=>{this.validateDisabled||(this._close(),this._emit("validate"))},this._onCleanBuild=()=>{this.busy||(this._close(),this._emit("clean-build"))},this._onAnalyzeMemory=()=>{this.busy||this.validateDisabled||(this._close(),this._emit("analyze-memory"))}}}eI.styles=[M.G9,eO.x,(0,s.AH)`
      :host {
        position: relative;
        display: inline-flex;
      }
      .menu-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        width: 32px;
        height: 32px;
        padding: 0;
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-m);
        background: transparent;
        color: var(--wa-color-text-normal);
        cursor: pointer;
        transition:
          background 0.12s,
          border-color 0.12s;
      }
      .menu-btn:hover {
        background: var(--esphome-tint);
      }
      .menu-btn wa-icon {
        font-size: 18px;
      }
      /* Bottom action bar sits at the viewport foot — open upward. */
      .menu {
        position: absolute;
        bottom: calc(100% + var(--wa-space-xs));
        right: 0;
        min-width: 200px;
      }
      .menu-item--disabled {
        opacity: 0.5;
        cursor: default;
      }
      .menu-item--disabled:hover {
        background-color: transparent;
      }
    `],eZ([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],eI.prototype,"_localize",void 0),eZ([(0,o.Fg)({context:P.Pt,subscribe:!0}),(0,r.wk)()],eI.prototype,"_expertMode",void 0),eZ([(0,r.MZ)({type:Boolean})],eI.prototype,"busy",void 0),eZ([(0,r.MZ)({type:Boolean,attribute:"validate-disabled"})],eI.prototype,"validateDisabled",void 0),eZ([(0,r.MZ)({attribute:!1})],eI.prototype,"webUiUrl",void 0),eI=eZ([(0,r.EM)("esphome-device-actions-menu")],eI);var eK=i(8763),ej=i(6910),eV=i(5972);let eY={key:"device.config_migration_change_key",field:"device.config_migration_change_field",fold:"device.config_migration_change_fold",convert:"device.config_migration_change_convert",action:"device.config_migration_change_action"},eN=/\u0001([^\u0002]*)\u0002/g;function eG(e){return(0,s.qy)`
    <div class="notice" role="note">
      <wa-icon library="mdi" name=${e.icon}></wa-icon>
      <div class="body">
        <div class="text">${e.text}</div>
        ${e.onCta?(0,s.qy)`<div class="cta-row">
                <button type="button" class="cta" @click=${e.onCta}>
                  ${e.ctaLabel}
                </button>
                ${e.secondary?(0,s.qy)`<button
                        type="button"
                        class="cta cta--secondary"
                        @click=${e.secondary.onClick}
                      >
                        ${e.secondary.label}
                      </button>`:s.s6}
              </div>`:s.s6}
      </div>
      ${e.onDismiss?(0,s.qy)`
              <button
                type="button"
                class="notice-close"
                aria-label=${e.dismissLabel??""}
                @click=${e.onDismiss}
              >
                <wa-icon library="mdi" name="close"></wa-icon>
              </button>
            `:s.s6}
    </div>
  `}let eH=(0,s.AH)`
  .notice {
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-s);
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-s) var(--wa-space-m);
    border: var(--wa-border-width-s) solid
      var(--notice-accent, var(--esphome-warning, #f59e0b));
    background: color-mix(
      in srgb,
      var(--notice-accent, var(--esphome-warning, #f59e0b)),
      transparent 90%
    );
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-s);
    line-height: 1.5;
  }

  .notice wa-icon {
    flex-shrink: 0;
    font-size: 20px;
    color: var(--notice-accent, var(--esphome-warning, #f59e0b));
  }

  .body {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    flex: 1;
    min-width: 0;
  }

  .body p,
  .body .text {
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

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: var(--wa-space-s);
  }

  .cta--secondary {
    background: transparent;
    color: var(--esphome-primary);
    border: var(--wa-border-width-s) solid var(--esphome-primary);
  }

  .cta--secondary:hover:not(:disabled) {
    background: color-mix(in srgb, var(--esphome-primary), transparent 90%);
  }
`,eW=(0,s.AH)`
  .notice-close {
    flex-shrink: 0;
    background: transparent;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    border-radius: var(--wa-border-radius-s);
  }

  .notice-close:hover {
    color: var(--wa-color-text-normal);
  }

  .notice-close wa-icon {
    font-size: 18px;
    display: block;
  }
`;var eJ=i(1404),eX=i(6848),eQ=i(325);function e0(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}i(9835);class e1 extends s.WF{open(){this._revealSensitive=!1,this._confirmed=!1,this._dialog.open=!0}close(){this._dialog.requestClose()}render(){return(0,s.qy)`
      <esphome-base-dialog
        ?open=${this._dialog.open}
        .label=${this._localize("device.config_migration_preview_title",{configuration:this.configuration})}
        @after-hide=${this._dialog.onAfterHide}
      >
        ${this._dialog.open?(0,s.qy)`<div class="diff">
                <esphome-yaml-diff
                  .oldValue=${this.oldValue}
                  .newValue=${this.newValue}
                  .revealSensitive=${this._revealSensitive}
                ></esphome-yaml-diff>
              </div>`:s.s6}
        <div class="actions">
          ${eF(this._localize,this._revealSensitive,this._toggleRevealSensitive)}
          <button class="btn btn--cancel" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
          <button class="btn btn--primary" @click=${this._confirm}>
            ${this._localize("device.config_migration_migrate")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_confirm(){this._confirmed||(this._confirmed=!0,this.close(),(0,e$.r)(this,"request-migrate-config"))}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.oldValue="",this.newValue="",this._revealSensitive=!1,this._dialog=new eQ.T(this),this._confirmed=!1,this._toggleRevealSensitive=()=>{this._revealSensitive=!this._revealSensitive}}}function e2(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}e1.styles=[M.G9,eX.dC,eJ.V,eJ.E,(0,s.AH)`
      esphome-base-dialog {
        --width: min(900px, 95vw);
      }

      .diff {
        display: flex;
        height: min(60vh, 600px);
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-m);
        overflow: hidden;
      }
    `],e0([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],e1.prototype,"_localize",void 0),e0([(0,r.MZ)()],e1.prototype,"configuration",void 0),e0([(0,r.MZ)({attribute:!1})],e1.prototype,"oldValue",void 0),e0([(0,r.MZ)({attribute:!1})],e1.prototype,"newValue",void 0),e0([(0,r.wk)()],e1.prototype,"_revealSensitive",void 0),e1=e0([(0,r.EM)("esphome-config-migration-preview-dialog")],e1),(0,I.C)({update:a.mdiUpdate,close:a.mdiClose});class e3 extends s.WF{willUpdate(e){this.yaml&&this._api&&this._detectedFor!==this.configuration?(this._detectedFor=this.configuration,this._dismissed=!1,this._detection=null,this._cancelRecheck(),this._detect()):e.has("yaml")&&(null!==this._detection||void 0!==this._recheckTimer)&&!this._dismissed&&this._armRecheck()}disconnectedCallback(){super.disconnectedCallback(),this._cancelRecheck()}render(){let e=this._detection;if(null===e||this._dismissed)return s.s6;let t=e.changes.some(e=>e.required);return(0,s.qy)`
      <div class=${t?"required":s.s6}>
        ${eG({icon:"update",text:this._renderChanges(e.changes),ctaLabel:this._localize("device.config_migration_migrate"),onCta:()=>(0,e$.r)(this,"request-migrate-config"),secondary:e.yaml===this.yaml?{label:this._localize("device.config_migration_preview"),onClick:()=>this._preview?.open()}:void 0,dismissLabel:this._localize("device.config_migration_dismiss"),onDismiss:()=>{this._dismissed=!0,this._cancelRecheck()}})}
      </div>
      <esphome-config-migration-preview-dialog
        .configuration=${this.configuration}
        .oldValue=${e.yaml}
        .newValue=${e.migrated}
      ></esphome-config-migration-preview-dialog>
    `}_renderChanges(e){if(0===e.length)return this._localize("device.config_migration_notice_generic");let t=this._localize("device.config_migration_lead"),i=e.slice(0,10),o=e.length-i.length;return(0,s.qy)`
      <p>${t}</p>
      <ul>
        ${i.map(e=>{var t;return(0,s.qy)`<li>${t=this._localize,(0,s.qy)`${(function(e,t){let i=e=>`\x01${e}\x02`,o=e(eY[t.kind],{old:i(t.old),new:i(t.new),scope:i(t.scope)}),a=t.since?(0,eV.aY)(t.since):null,s=t.removed_in?(0,eV.aY)(t.removed_in):null;null===a||null===s||t.required?null!==a?o+=` ${e("device.config_migration_change_since",{version:a})}`:null===s||t.required||(o+=` ${e("device.config_migration_change_removed_in",{removed_in:s})}`):o+=` ${e("device.config_migration_change_since_removed_in",{version:a,removed_in:s})}`,t.required&&(o+=` ${e("device.config_migration_change_required")}`);let r=[],n=0;for(let e of o.matchAll(eN))e.index>n&&r.push(o.slice(n,e.index)),r.push({code:e[1]}),n=e.index+e[0].length;return n<o.length&&r.push(o.slice(n)),r})(t,e).map(e=>"string"==typeof e?e:(0,s.qy)`<code>${e.code}</code>`)}`}</li>`})}
        ${o>0?(0,s.qy)`<li>
                ${this._localize("device.editor_invalid_more",{count:o})}
              </li>`:s.s6}
      </ul>
    `}_armRecheck(){clearTimeout(this._recheckTimer),this._recheckTimer=setTimeout(()=>{this._recheckTimer=void 0,this._detect()},750)}_cancelRecheck(){clearTimeout(this._recheckTimer),this._recheckTimer=void 0}async _detect(){let{configuration:e,yaml:t,_api:i}=this;if(i)try{let{yaml_diff:o,changes:a}=await i.migrateConfig(t);if(e!==this.configuration)return;if(t!==this.yaml){!this._dismissed&&this.isConnected&&this._armRecheck();return}this._detection=null===o?null:{yaml:t,migrated:(0,_.lX)(t,o),changes:[...a].sort((e,t)=>Number(t.required)-Number(e.required))}}catch(e){console.warn("config-migration-notice: detection failed",e)}}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.yaml="",this._detection=null,this._dismissed=!1,this._detectedFor=null}}e3.styles=[eH,eW,(0,s.AH)`
      :host {
        display: block;
        /* Migration identity color — matches the dashboard dot and badge. */
        --notice-accent: var(--esphome-migration);
      }
      :host([hidden]) {
        display: none;
      }
      /* A spelling the installed ESPHome already rejects is an error, not a nudge. */
      .required {
        --notice-accent: var(--esphome-error);
      }
      p {
        margin: 0 0 var(--wa-space-2xs);
      }
      ul {
        margin: 0;
        padding-left: 1.2em;
      }
      code {
        font-family: var(--wa-font-family-code);
        font-size: var(--wa-font-size-xs);
      }
    `],e2([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],e3.prototype,"_localize",void 0),e2([(0,o.Fg)({context:P.Ie,subscribe:!0}),(0,r.wk)()],e3.prototype,"_api",void 0),e2([(0,r.MZ)()],e3.prototype,"configuration",void 0),e2([(0,r.MZ)({attribute:!1})],e3.prototype,"yaml",void 0),e2([(0,r.wk)()],e3.prototype,"_detection",void 0),e2([(0,r.wk)()],e3.prototype,"_dismissed",void 0),e2([(0,r.P)("esphome-config-migration-preview-dialog")],e3.prototype,"_preview",void 0),e3=e2([(0,r.EM)("esphome-config-migration-notice")],e3);var e6=i(6622);function e5(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"alert-outline":a.mdiAlertOutline,close:a.mdiClose});class e4 extends s.WF{willUpdate(e){e.has("configuration")&&(this._dismissed=!1)}render(){if(this._dismissed)return s.s6;let e=er(this.yaml.split("\n"))>=0;if(!e){let e=this._devices.find(e=>e.configuration===this.configuration)?.name_add_mac_suffix===!0;if(function(e){let t=e.split("\n"),i=(0,et.zZ)(t,"esphome",eo);if(i<0)return!1;let o=ea.exec(t[i]);return null!==o&&!1===(0,ei.FY)((0,ee.Ir)(o[2]))}(this.yaml)||!e)return s.s6}let t={icon:"alert-outline",text:(0,s.qy)`${this._localize("device.mac_suffix_notice")}
        <a href=${e6.WU} target="_blank" rel="noopener noreferrer"
          >${this._localize("device.mac_suffix_learn_more")}</a
        >`,dismissLabel:this._localize("device.mac_suffix_dismiss"),onDismiss:()=>{this._dismissed=!0}};return e?eG({...t,ctaLabel:this._localize("device.mac_suffix_disable"),onCta:()=>(0,e$.r)(this,"request-disable-mac-suffix")}):eG(t)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.configuration="",this.yaml="",this._dismissed=!1}}e4.styles=[eH,eW,(0,s.AH)`
      :host {
        display: block;
      }
      a {
        color: inherit;
      }
    `],e5([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],e4.prototype,"_localize",void 0),e5([(0,o.Fg)({context:P.xJ,subscribe:!0}),(0,r.wk)()],e4.prototype,"_devices",void 0),e5([(0,r.MZ)()],e4.prototype,"configuration",void 0),e5([(0,r.MZ)({attribute:!1})],e4.prototype,"yaml",void 0),e5([(0,r.wk)()],e4.prototype,"_dismissed",void 0),e4=e5([(0,r.EM)("esphome-mac-suffix-notice")],e4);let e9=/^(\d+)\.(\d+)(?:\.(\d+))?(.*)$/;function e8(e){let t=e9.exec(e.trim());return t?[Number(t[1]),Number(t[2]),Number(t[3]??0),+!t[4]]:null}function e7(e,t){let i=e8(e),o=e8(t);if(!i||!o)return!1;for(let e=0;e<i.length;e++)if(i[e]!==o[e])return i[e]>o[e];return!0}let te="2026.9.0";function tt({device:e,yaml:t,esphomeVersion:i}){var o,a,s;let r,n,l={present:null!==(n=eg(t,(0,h.D)(t))),hasEncryption:!!n&&n.encryptionLine>=0,hasPassword:!!n&&n.passwordLine>=0,hasOwnKey:!!n&&n.keyLine>=0,rewritable:!!n&&!n.multiLine};if(!l.present||!l.rewritable||!function(e){let t=(0,h.D)(e),i=(0,et.zZ)(t,"api",ed);if(i<0)return!1;let o=(0,et.zZ)(t,"api",ep,i+1);if(o<0)return!1;let a=t[o].replace(/^\s*key\s*:/,""),s=(0,ee.Ir)((0,ee.bw)(a).value.trim());return s.length>0&&!/^!\S*$/.test(s)}(t))return null;if(l.hasEncryption)return l.hasOwnKey?"drop_own_key":null;return e&&(r=(o=e).runtime_state,(0,T.OO)(o)&&r.api_encryption_active&&(s=a=r.deployed_version,e8(s)?.[3]===1)&&e7(a,te))?e7((0,eV.aY)(i),te)?l.hasPassword?"replace_password":"add":null:null}function ti(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"lock-alert":a.mdiLockAlert,close:a.mdiClose});class to extends s.WF{willUpdate(e){e.has("configuration")&&(this._dismissed=null);let t=this._devices.find(e=>e.configuration===this.configuration),i=t!==this._device;this._device=t,(i||e.has("yaml")||e.has("configuration")||e.has("_esphomeVersion"))&&(this._nudge=tt({device:t,yaml:this.yaml,esphomeVersion:this._esphomeVersion}))}render(){let e=this._nudge;if(!e||this._dismissed===e)return s.s6;let t="drop_own_key"===e;return eG({icon:"lock-alert",text:this._localize(`device.ota_encryption_notice_${e}`),ctaLabel:this._localize(t?"device.ota_encryption_use_api_key":"device.ota_encryption_enable"),onCta:()=>(0,e$.r)(this,t?"request-drop-ota-encryption-key":"request-enable-ota-encryption"),dismissLabel:this._localize("device.ota_encryption_dismiss"),onDismiss:()=>{this._dismissed=e}})}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._esphomeVersion="",this.configuration="",this.yaml="",this._dismissed=null,this._nudge=null}}to.styles=[eH,eW,(0,s.AH)`
      :host {
        display: block;
      }
    `],ti([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],to.prototype,"_localize",void 0),ti([(0,o.Fg)({context:P.xJ,subscribe:!0}),(0,r.wk)()],to.prototype,"_devices",void 0),ti([(0,o.Fg)({context:P.wo,subscribe:!0}),(0,r.wk)()],to.prototype,"_esphomeVersion",void 0),ti([(0,r.MZ)()],to.prototype,"configuration",void 0),ti([(0,r.MZ)({attribute:!1})],to.prototype,"yaml",void 0),ti([(0,r.wk)()],to.prototype,"_dismissed",void 0),ti([(0,r.wk)()],to.prototype,"_nudge",void 0),to=ti([(0,r.EM)("esphome-ota-encryption-notice")],to);let ta=(0,s.AH)`
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
    gap: var(--wa-space-s);
  }

  .board-info-link {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    font-size: var(--wa-font-size-xs);
    color: var(--esphome-primary);
    text-decoration: underline;
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

  /* Compact variant of .action-item (defined below; compound selector
     outweighs its base rules regardless of source order). */
  .action-item.welcome-banner-install {
    width: auto;
    margin-top: var(--wa-space-xs);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
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
    outline: var(--esphome-focus-outline);
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
`;var ts=i(5494);i(751),i(8197),i(7427);var tr=i(2493),tn=i(4103),tl=i(1746),td=i(7641);let tc=new Set(["condition","all","any"]);function th(e){return{node:e.node.slice(1),field:e.field}}function tp(e){return e&&e.node.length>0?e:null}function tu(e){return e&&0===e.node.length?e.field:void 0}function t_(e,t){let i=tu(e);return i?.[0]===t?i[1]??"":null}function tm(e){return e?JSON.stringify([e.node,e.field]):void 0}function tv(e,t){return tm(e)!==tm(t)}function tg(e,t,i){if(!e||!i?.length)return null;let o=function(e,t){let i=t&&function(e){switch(e.kind){case"device_on":case"component_on":return{keyPaths:[[e.trigger]],index:e.index};case"component_action":return{keyPaths:[(0,tl.Y)(e.field)]};case"interval":return{keyPaths:[["interval"]],index:e.index};case"script":return{keyPaths:[["script"]],index:"any"};case"api_action":return{keyPaths:td.i.map(e=>["api",e]),index:"any"};default:return null}}(t);if(!i)return null;let o=null;for(let t of i.keyPaths){let i=e.indexOf(t[0]);for(;i>=0&&!t.every((t,o)=>e[i+o]===t);)i=e.indexOf(t[0],i+1);if(i>=0){o=e.slice(i+t.length);break}}return null===o?null:void 0===i.index?o:"any"===i.index?"number"==typeof o[0]?o.slice(1):null:o[0]===i.index?o.slice(1):null}(i,t);return o?function(e,t){if(0===t.length)return null;let i=t=>tb(e.actions,tf,tw,t,[],null),o=t[0];return"then"===o?i(t.slice(1)):"number"==typeof o?i(t):i(t)??{node:[],field:t.map(String)}}(e,o):null}let tf=e=>e.action_id,ty=e=>e.condition_id;function tb(e,t,i,o,a,s){if(0===o.length)return s;let r=o[0];if("number"==typeof r){let n=o[1];if("string"==typeof n){let s=void 0!==e[r]&&t(e[r])===n?r:e.findIndex(e=>t(e)===n);if(s>=0)return i(e[s],o.slice(2),[...a,s])}return void 0!==e[r]?{node:[...a,r],field:[]}:s}let n=e.findIndex(e=>t(e)===r);return n>=0?i(e[n],o.slice(1),[...a,n]):s}function tw(e,t,i){let o={node:i,field:[]};if(0===t.length)return o;let a=t[0],s="number"==typeof a&&!!e.children&&Object.prototype.hasOwnProperty.call(e.children,"else");if(e.branches?.length||s)return function(e,t,i,o){let a=t[0],s="number"==typeof a?a:0,[r,...n]="number"==typeof a?t.slice(1):t;if("else"===r&&e.children?.else)return tb(e.children.else,tf,tw,n,[...i,"else"],o);let l=e.branches?.[s];if(!l)return o;let d=[...i,"branches",s],c={node:d,field:[]};return"if"===r?tb(l.conditions,ty,t$,n,[...d,"conditions"],c):"then"===r?tb(l.actions,tf,tw,n,[...d,"then"],c):c}(e,t,i,o);if("string"==typeof a){if(tc.has(a))return tb(e.conditions??[],ty,t$,"condition"===a?t.slice(1):t,[...i,"conditions"],o);if(e.children&&Object.prototype.hasOwnProperty.call(e.children,a))return tb(e.children[a],tf,tw,t.slice(1),[...i,a],o);if(e.conditions?.some(e=>e.condition_id===a))return tb(e.conditions,ty,t$,t,[...i,"conditions"],o)}return{node:i,field:t.map(String)}}function t$(e,t,i){let o={node:i,field:[]};if(0===t.length)return o;let a=e.children??[],s=t[0];return a.length>0&&("number"==typeof s||a.some(e=>e.condition_id===s))?tb(a,ty,t$,t,i,o):{node:i,field:t.map(String)}}var tk=i(8283),tx=i(6567),tz=i(4267),tC=i(5660),tS=i(3074);function tF(e,t){e.inert!==t&&(e.inert=t,e.ariaBusy=t?"true":null)}var tP=i(2342),tq=i(7491);let tM=new EventTarget;class tL{hostConnected(){this._connected=!0,this._detachedBasis=null,this._anchor=this._host.parentNode,this._lastRoundFailed=!1,this._announceUnmount=(0,tq.y5)(this._host)}hostDisconnected(){this._connected=!1,this._detachedBasis=this._host.yaml;let e=null!==this._debounce;this._cancelDebounce(),e&&this._anchor?.isConnected?this.autoApply():e&&console.warn("Dropped pending auto-apply: anchor detached"),this._announceUnmount?.(),this._announceUnmount=null}hostUpdated(){let e=this._host.location?(0,_.Ks)(this._host.location):null;e!==this._boundSectionKey&&(this._boundSectionKey=e,this._lastRoundFailed=!1)}notifyHydrated(){this._lastRoundFailed=!1}get dirty(){return this._dirty}get lastRoundFailed(){return this._lastRoundFailed}get deleting(){return null!==this._deleteMode}get inFlightWrite(){return null!==this._deleteMode||"applying"===this._apply.kind}shouldSkipReload(){return"applying"===this._apply.kind||this._host.yaml===this._lastSelfWrittenYaml}withValue(e){if(this._options.isReadOnly())return;let t={...this._host.value??(0,_.rN)(),...e};this._host.value=t,(0,e$.r)(this._host,"automation-change",{value:t,location:this._host.location}),this.scheduleAutoApply()}scheduleAutoApply(){if(!this._host.addMode&&!this._options.isReadOnly()){if(this._deleteMode){this._deleteMode.suppressed=!0,this._deleteMode.suppressedFor=this._host.location;return}this._setDirty(!0),this._cancelDebounce(),this._debounce=setTimeout(()=>{this._debounce=null,this.autoApply()},200)}}async flushPending(){for(;this._debounce||"applying"===this._apply.kind;)this._debounce?(this._cancelDebounce(),await this.autoApply()):"applying"===this._apply.kind&&(await this._apply.settled,await new Promise(e=>setTimeout(e)))}async autoApply(){let e,t=this._options.getApi(),i=this._host.location,o=this._host.value;if(!t||!i||!o)return;if(this._options.isReadOnly())return void this._setDirty(!1);if(this._options.canApply&&!this._options.canApply(i))return;if(this._deleteMode){this._deleteMode.suppressed=!0,this._deleteMode.suppressedFor=i;return}if("applying"===this._apply.kind){this._apply.queued=!0;return}let a={kind:"applying",queued:!1,settled:new Promise(t=>e=t),settle:e};this._apply=a;try{let e=this._host.configuration,a=this._connected?this._host.yaml:this._detachedBasis??this._host.yaml,s=(0,tq.fb)(this._host,"yaml-draft",this._anchor),{yaml_diff:r}=await t.upsertAutomation(e,o,i,a),n=(0,_.lX)(a,r);this._lastSelfWrittenYaml=n,this._connected||(this._detachedBasis=n);let l=null===this._host.location||(0,_.Ks)(this._host.location)!==(0,_.Ks)(i);s(this._connected,{configuration:e,yaml:n,basedOn:a,node:l?tM:this._host}),this._lastRoundFailed=!1}catch(e){null!==this._host.location&&(0,_.Ks)(this._host.location)===(0,_.Ks)(i)&&(this._lastRoundFailed=!0),this._connected||this._anchor?.isConnected?this._surfaceSaveError(e):console.error("Detached auto-apply round failed:",e)}finally{this._apply={kind:"idle"},a.queued?this.autoApply():null===this._debounce&&this._setDirty(!1),a.settle()}}async delete(){let e=this._options.getApi();if(!e||!this._host.location||this._deleteMode||this._options.isReadOnly())return;let t=this._host.location,i=this._host.configuration,o=(0,tq.fb)(this._host,"yaml-updated",this._anchor),a=null!==this._debounce;this._cancelDebounce();let s={suppressed:!1,suppressedFor:null};this._setDeleteMode(s),this._options.setError("");let r=!1;try{await this.flushPending();let a=this._host.yaml;await m(e,i,t,a,o,()=>this._connected),this._connected&&(!this._host.location||(0,_.Ks)(this._host.location)===(0,_.Ks)(t))&&this._host.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(e){r=!0,this._surfaceSaveError(e)}finally{this._setDeleteMode(null),this._settleDelete(s,{failed:r,hadPending:a,location:t})}}_settleDelete(e,t){let{suppressed:i,suppressedFor:o}=e,{failed:a,hadPending:s,location:r}=t;a?this._connected&&(i||s)&&this.scheduleAutoApply():i&&o&&this._connected&&this._host.location&&(0,_.Ks)(o)!==(0,_.Ks)(r)&&(0,_.Ks)(this._host.location)===(0,_.Ks)(o)?this.scheduleAutoApply():this._setDirty(!1)}_surfaceSaveError(e){let t=this._options.getLocalize(),i=(0,tS.K)(e,t,"device.automation_save_error");this._options.setError(i),(0,B.UG)(t("device.automation_save_error"),{description:i})}_cancelDebounce(){this._debounce&&(clearTimeout(this._debounce),this._debounce=null)}_setDirty(e){this._dirty!==e&&(this._dirty=e,this._host.requestUpdate(),(0,tq.IL)(this._host,"dirty-change",{dirty:e,node:this._host}))}_setDeleteMode(e){this._deleteMode=e,this._host.requestUpdate()}constructor(e,t){this._host=e,this._options=t,this._debounce=null,this._apply={kind:"idle"},this._deleteMode=null,this._lastSelfWrittenYaml=null,this._detachedBasis=null,this._dirty=!1,this._lastRoundFailed=!1,this._boundSectionKey=null,this._connected=!1,this._announceUnmount=null,this._anchor=null,e.addController(this)}}var tR=i(2640),tA=i(8144);let tE=(0,s.AH)`
  /* Add button — one dashed quiet affordance at the bottom of every
     list, top-level and nested alike (#1450); brand color on hover
     for affordance. Nested lists (via :host-context() reaching the
     parent action-node's .ae-nested wrapper, the only way a sibling
     custom-element with its own shadow can scope the rule) only
     tighten the density. */
  .ae-add {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--wa-space-2xs);
    width: 100%;
    appearance: none;
    border: 1px dashed var(--wa-color-neutral-border-quiet, #d1d5db);
    background: var(--esphome-primary-light);
    color: var(--wa-color-text-quiet);
    padding: var(--wa-space-xs) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-semibold);
    margin-top: var(--wa-space-s);
    transition:
      border-color 0.12s,
      color 0.12s;
  }

  .ae-add:hover:not(:disabled) {
    border-color: var(--wa-color-brand-fill-loud, var(--esphome-primary));
    color: var(--wa-color-brand-fill-loud, var(--esphome-primary));
  }

  .ae-add:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  :host-context(.ae-nested) .ae-add {
    padding: var(--wa-space-2xs) var(--wa-space-s);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
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
`,tT=(0,s.AH)`
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

  .ae-row-unknown {
    margin: 0;
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-neutral-fill-quiet);
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
`,tD=(0,s.AH)`
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
`,tO=[(0,s.AH)`
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
`,tD,tT,tE,tR.Z,tA.s,ew.U];var tU=i(5242);let tB=new Set(["homeassistant.service"]),tZ=["triggers","actions","conditions"],tI=new Set(["homeassistant.action",...tB]);class tK{hostDisconnected(){this._seq++}async load(e,t,i,o){if(!e||!t)return{};let a=++this._seq,s=o?.onPaint,r=await async function(e,t,i){try{let o=await e.getAvailableAutomations(t,i?.yaml);if(i?.isStale?.())return{status:"stale"};let a={...o,triggers:o.triggers.map(e=>({...e})),actions:o.actions.map(e=>({...e})),conditions:o.conditions.map(e=>({...e}))};i?.onPaint?.(a);let s=await async function(e,t,i,o=tZ){let a=(0,tU.FG)(),s=[],r=(t,o)=>{for(let r of o)s.push((0,tU.SN)(e,t,r,i).then(e=>{(0,tU.P0)(a,e)}))};for(let e of(o.includes("triggers")&&r("triggers",t.triggers),o.includes("actions")&&r("actions",t.actions),o.includes("conditions")&&r("conditions",t.conditions),await Promise.allSettled(s)))"rejected"===e.status&&(a.rejected++,console.warn("automation-editor: body fetch failed",e.reason));return a}(e,a,void 0,i?.lists);if(i?.isStale?.())return{status:"stale"};for(let e of a.actions)tI.has(e.id)&&(e.config_entries=e.config_entries.map(e=>"service"===e.key?{...e,hidden:!0}:e));let r={...a,triggers:[...a.triggers],actions:[...a.actions],conditions:[...a.conditions]};return{status:"ok",available:r,hydration:s}}catch(e){if(i?.isStale?.())return{status:"stale"};return{status:"error",error:e}}}(e,t,{isStale:()=>a!==this._seq,yaml:o?.yaml,lists:o?.lists??["actions","conditions"],onPaint:s?e=>{a===this._seq&&s(e)}:void 0});return a!==this._seq?{}:function(e,t){if("stale"===e.status)return{};if("error"===e.status)return{error:(0,tk.u)(e.error)};let{missingBody:i,missingField:o,rejected:a}=e.hydration,s=i+o+a;return s>0&&(0,B.UG)(t("device.automation_partial_hydration",{count:s})),{available:e.available}}(r,i)}constructor(e){this._seq=0,e.addController(this)}}class tj{hostConnected(){}get active(){return this._active}resolve(e,t,i){let o=(0,_.Ks)(t),a=e.find(e=>(0,_.Ks)(e.location)===o);return!a||i&&a.location.kind!==i?(this._set(null),null):(this._set(a.error??null,a.unsupported??!1),null!=a.error)?null:{tree:a.automation,location:a.location}}renderPanel(e){return this._unsupported?(0,s.qy)`<div class="empty-message--dashed" role="note">
        <p>${e("device.yaml_only_section")}</p>
      </div>`:(0,s.qy)`<div class="empty-message--dashed" role="alert">
      <p class="ae-error">${e("device.automation_parse_error")}</p>
      ${this._message?(0,s.qy)`<p>${this._message}</p>`:s.s6}
    </div>`}_set(e,t=!1){let i=null!=e;(this._active!==i||this._message!==(e??"")||this._unsupported!==t)&&(this._active=i,this._message=e??"",this._unsupported=t,this._host.requestUpdate())}constructor(e){this._host=e,this._active=!1,this._message="",this._unsupported=!1,e.addController(this)}}var tV=i(1165);function tY(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({delete:a.mdiDelete});class tN extends s.WF{get _held(){return this._hydrating||this._stale}_currentFocus(){return this._stale||(this._focus=this._resolveFocus(this._hydrating?null:this.value,this.location,this.focusYamlPath)),this._focus}_canApply(e){return!0}get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}flushPending(){return this._engine.flushPending()}get lastFlushFailed(){return this._engine.lastRoundFailed}renderStateGate(){return this._loading?(0,s.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`:this._parseError.active?this._parseError.renderPanel(this._localize):null}renderFooter(e){var t;let i;return(0,s.qy)`${this._error?(0,s.qy)`<p class="ae-error" role="alert">${this._error}</p>`:s.s6}${this.location&&this.value&&!this.addMode?(t={label:e.label,message:e.message(this.location),disabled:this._engine.deleting,onConfirm:this._onDelete},i=(0,tV._)(),(0,s.qy)`<div class="ae-actions">
      <button
        type="button"
        class="ae-danger"
        ?disabled=${t.disabled}
        @click=${()=>i.value?.open()}
      >
        <wa-icon library="mdi" name="delete"></wa-icon>
        ${t.label}
      </button>
    </div>
    <esphome-confirm-dialog
      ${(0,tV.K)(i)}
      heading=${t.label}
      confirm-label=${t.label}
      message=${t.message}
      destructive
      @confirm=${t.onConfirm}
    ></esphome-confirm-dialog>`):s.s6}`}async _hydrateFromBackend(){if(!this._api||!this.configuration||!this.location){this._stale&&(this.value=null),this._dropStaleTree(),this._stale=!1;return}let e=++this._hydrateId;null!==this.value||this.addMode||(this._hydrating=!0);let{configuration:t,yaml:i}=this,o=()=>e!==this._hydrateId||i!==this.yaml&&!this._hydrating,a=this._stale||!this._engine.shouldSkipReload();try{let e=await this._parses.fetch(`${t}\0${i}`,()=>this._api.parseDeviceAutomations(t,i));if(o())return;this._error="";let s=this._parseError.resolve(e,this.location);s?(this.location=s.location,this._retargeted&&(this._target++,this._showAdvanced=!1),this._retargeted=!1,a&&this._valuesRead++,this.value=s.tree,this._hydrating=!1,this._engine.notifyHydrated()):(this._stale&&!this._parseError.active&&(this.value=null),this._dropStaleTree())}catch(e){if(o())return;this._dropStaleTree(),this._error=(0,tS.K)(e,this._localize,"device.automation_parse_error");return}this._stale=i!==this.yaml}connectedCallback(){super.connectedCallback(),!this.hasUpdated||this.addMode||null!==this.value||this._loading||this._hydrateFromBackend()}disconnectedCallback(){super.disconnectedCallback(),this._hydrateId++,this._stale&&(this.value=null),this._stale=!1,this._dropStaleTree(),tF(this,!1)}_dropStaleTree(){this._hydrating&&(this.value=null,this._hydrating=!1)}willUpdate(e){if(e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&(0,_.Ks)(t)!==(0,_.Ks)(this.location)&&(this._hydrating=!0,this._retargeted=!0)}if(void 0!==e.get("yaml")&&!this.addMode){let e=!this._engine.shouldSkipReload();e&&!this._stale&&this._valuesRead++,this._stale=e&&null!==this.location&&null!==this.value&&!this._engine.dirty}tF(this,this._held)}updated(e){e.has("configuration")&&this._loadAvailable(),!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&(null===this.value||this._hydrating)&&!this._loading&&this._hydrateFromBackend()}reload(){this._stale=!this.addMode&&null!==this.location&&!this._engine.shouldSkipReload(),this._stale&&this._hydrateFromBackend()}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._error="",this._hydrating=!1,this._hydrateId=0,this._parses=new tP.e({evictOnSettle:!0}),this._resolveFocus=(0,d.A)(tg),this._target=0,this._retargeted=!1,this._valuesRead=0,this._stale=!1,this._showAdvanced=!1,this._focus=null,this._parseError=new tj(this),this._catalogLoad=new tK(this),this._engine=new tL(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active||this._held,canApply:e=>this._canApply(e),setError:e=>{this._error=e}}),this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onDelete=()=>{this._engine.delete()},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})}}}tN.styles=[M.G9,M.G4,tC.z9,tO],tY([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],tN.prototype,"_localize",void 0),tY([(0,o.Fg)({context:P.Ie})],tN.prototype,"_api",void 0),tY([(0,r.MZ)()],tN.prototype,"configuration",void 0),tY([(0,r.MZ)({attribute:!1})],tN.prototype,"board",void 0),tY([(0,r.MZ)()],tN.prototype,"platform",void 0),tY([(0,r.MZ)({attribute:!1})],tN.prototype,"value",void 0),tY([(0,r.MZ)({attribute:!1})],tN.prototype,"location",void 0),tY([(0,r.MZ)({type:Boolean,attribute:"add-mode"})],tN.prototype,"addMode",void 0),tY([(0,r.MZ)()],tN.prototype,"yaml",void 0),tY([(0,r.MZ)({attribute:!1})],tN.prototype,"focusYamlPath",void 0),tY([(0,r.wk)()],tN.prototype,"_available",void 0),tY([(0,r.wk)()],tN.prototype,"_loading",void 0),tY([(0,r.wk)()],tN.prototype,"_error",void 0),tY([(0,r.wk)()],tN.prototype,"_hydrating",void 0),tY([(0,o.Gt)({context:P.km})],tN.prototype,"_valuesRead",void 0),tY([(0,r.wk)()],tN.prototype,"_stale",void 0),tY([(0,r.wk)()],tN.prototype,"_showAdvanced",void 0);class tG extends tN{updated(e){this._maybeFlashName(),super.updated(e)}_renderNameField(e,t){return(0,s.qy)`<div class="field">
      <label class="field-label" for=${this._nameInputId}>${e.label}</label>
      <p class="field-description">${(0,ej.Gc)(e.description)}</p>
      <input
        id=${this._nameInputId}
        type="text"
        .value=${e.value}
        ?disabled=${t}
        readonly
      />
    </div>`}_maybeFlashName(){let e=this._currentFocus(),t=tu(e)?.[0];if(void 0===t||!this._nameYamlKeys.includes(t))return;let i=`${this._target}:${tm(e)}`;if(i===this._nameFlashKey)return;let o=this.shadowRoot?.querySelector(`#${this._nameInputId}`)?.closest(".field");o&&(this._nameFlashKey=i,(0,tx.uJ)(o))}connectedCallback(){super.connectedCallback(),this._load()}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable()}catch(e){this._error=(0,tk.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}}tG.styles=[tN.styles,tz.h];var tH=i(9214),tW=i(2943);i(4355);var tJ=i(3336);let tX=(0,s.AH)`
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

  .picker-body .disclosure-toggle {
    display: flex;
    width: 100%;
    margin: var(--wa-space-m) 0 var(--wa-space-2xs);
  }

  .picker-body .disclosure-toggle:first-child {
    margin-top: var(--wa-space-2xs);
  }

  .disclosure-toggle .picker-group-label {
    display: inline-flex;
    align-items: baseline;
    gap: var(--wa-space-2xs);
    margin: 0;
  }

  .picker-group-count {
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    font-weight: var(--wa-font-weight-normal);
    letter-spacing: normal;
    text-transform: none;
  }

  .picker-body .disclosure-panel {
    margin-top: 0;
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

  .picker-row-add svg {
    display: block;
    width: 18px;
    height: 18px;
    fill: currentColor;
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
`;var tQ=i(1480),t0=i(1020),t1=i(1376),t2=i(1148),t3=i(318);function t6(e,t=e=>e.domain){let i=new Map;for(let o of e){let e=t(o),a=i.get(e)??[];a.push(o),i.set(e,a)}return i}function t5(e,t){return t?e.filter(e=>e.id.toLowerCase().includes(t)||e.name.toLowerCase().includes(t)||(e.description??"").toLowerCase().includes(t)):e}function t4(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({close:a.mdiClose,magnify:a.mdiMagnify});class t9 extends s.WF{open(e){if(this._hiding){e&&(this._pending=e);return}e&&(this._request=e,this.kind=e.kind,this.items=e.items,this.devices=e.devices),this._activeTab="action"===this.kind?"by-target":"by-type",this._query="",this._targetOverrides=new Map,this._picked=!1,this._dialog.open=!0}render(){let e="action"===this.kind?this._localize("device.automation_pick_action"):this._localize("device.automation_pick_condition");return(0,s.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      .label=${e}
      @request-close=${this._onRequestClose}
      @after-hide=${this._onAfterHide}
    >
      ${this._dialog.open?this._renderBody():s.s6}
    </esphome-base-dialog>`}_renderBody(){let e=this._localize("device.automation_pick_search"),t="action"===this.kind?["by-target","by-type","building-blocks"]:["by-type","building-blocks"];return(0,s.qy)`<div class="picker-search">
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
            aria-label=${e}
            .value=${this._query}
            placeholder=${e}
            @input=${e=>this._query=e.target.value}
          />
        </div>
      </div>
      <div class="picker-tabs" role="tablist">
        ${t.map(e=>(0,s.qy)`<button
              type="button"
              role="tab"
              class="picker-tab ${this._activeTab===e?"active":""}"
              aria-selected=${this._activeTab===e}
              @click=${()=>this._activeTab=e}
            >
              ${this._tabLabel(e)}
            </button>`)}
      </div>
      <div class="picker-body" role="tabpanel">${this._renderActiveTab()}</div>`}_tabLabel(e){switch(e){case"by-target":return this._localize("device.automation_pick_tab_by_target");case"by-type":return this._localize("device.automation_pick_tab_by_type");case"building-blocks":return this._localize("device.automation_pick_tab_building_blocks")}}_renderActiveTab(){let e=this.items.filter(e=>!tB.has(e.id)),t=this._query.trim().toLowerCase();switch(this._activeTab){case"by-target":return this._renderByTarget(e,t);case"by-type":return this._renderByType(t5(e,t));case"building-blocks":return this._renderBuildingBlocks(t5(e,t))}}_renderByTarget(e,t){if(0===this.devices.length)return(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_targets")}
      </p>`;let i=t6(e),o=t?new Map([...i].map(([e,i])=>[e,t5(i,t)])):i,a=(0,t3.vJ)(this.devices),r=this.devices.filter(t3._B).flatMap(e=>{var a;let s,r,n,l=(0,t3.zl)(e),d=""!==t&&(0,t2.K)(t,l,e.id),c=(a=d?i:o,s=(0,t3.I7)(e.component_id),r=a.get(s)??[],(n=e.component_id===s?void 0:a.get(e.component_id))?r.concat(n):r);return c.length?[{device:e,name:l,matching:c,entityMatch:d}]:[]});if(0===r.length)return(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`;let n=r.length<=(t?5:1);return(0,s.qy)`${r.map(({device:e,name:i,matching:o,entityMatch:r})=>{let l=this._targetOverrides.get(e.id)??n;return(0,t1.u)({open:l,onToggle:()=>this._setTargetOpen(e.id,!l),localize:this._localize,labelText:this._renderGroupLabel(i,a(e),t&&!r?o.length:null),body:()=>(0,s.qy)`${o.map(t=>this._renderRow(t,()=>this._pick(t.id,(0,t3.TS)(t,e))))}`,variant:"quiet",iconBefore:!0})})}`}_renderGroupLabel(e,t,i){return(0,s.qy)`<span class="picker-group-label">${e}<span class="ae-muted">(${t})</span>${null===i?s.s6:(0,s.qy)`<span class="picker-group-count" aria-hidden="true">${i}</span>`}</span>`}_setTargetOpen(e,t){this._targetOverrides=new Map(this._targetOverrides).set(e,t)}_renderByType(e){let t=t6(e.filter(e=>"core"!==e.domain),e=>(0,t3.I7)(e.domain)),i=Array.from(t.keys()).sort();return 0===i.length?(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,s.qy)`${i.map(e=>(0,s.qy)`
        <p class="picker-group-label">${e}</p>
        ${(t.get(e)??[]).map(e=>this._renderRow(e,()=>this._pick(e.id)))}
      `)}`}_renderBuildingBlocks(e){let t=e.filter(e=>"core"===e.domain);return 0===t.length?(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,s.qy)`${t.map(e=>this._renderRow(e,()=>this._pick(e.id)))}`}_renderRow(e,t){return(0,s.qy)`<div
      class="picker-row"
      role="button"
      tabindex="0"
      @click=${t}
      @keydown=${e=>{("Enter"===e.key||" "===e.key)&&(e.preventDefault(),t())}}
    >
      <div class="picker-row-body">
        <span class="picker-row-title">${e.name}</span>
        ${e.description?(0,s.qy)`<span class="picker-row-desc line-clamp-2">
                ${(0,ej.Gc)(e.description)}
              </span>`:s.s6}
      </div>
      <span class="picker-row-add" aria-hidden="true">${(0,t0.R)(a.mdiPlus)}</span>
    </div>`}_pick(e,t){this._picked||(this._picked=!0,this._request?.onPicked({id:e,preFilledParams:t}),this._dialog.requestClose())}constructor(...e){super(...e),this._localize=e=>e,this.kind="action",this.items=[],this.devices=[],this._dialog=new eQ.T(this),this._activeTab="by-target",this._query="",this._targetOverrides=new Map,this._picked=!1,this._request=null,this._pending=null,this._hiding=!1,this._onRequestClose=()=>{this._hiding=!0},this._onAfterHide=()=>{if(this._dialog.onAfterHide(),!this._pending){this._hiding=!1,this._request=null;return}this.updateComplete.then(()=>{this._hiding=!1;let e=this._pending;this._pending=null,e&&this.open(e)})}}}function t8(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}function t7(e,t){(0,e$._)(e,"request-catalog-pick",t)||console.warn("request-catalog-pick found no esphome-catalog-picker-host above",e)}t9.styles=[M.G9,tC.z9,ew.U,tQ.a,tX],t4([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],t9.prototype,"_localize",void 0),t4([(0,r.MZ)()],t9.prototype,"kind",void 0),t4([(0,r.MZ)({attribute:!1})],t9.prototype,"items",void 0),t4([(0,r.MZ)({attribute:!1})],t9.prototype,"devices",void 0),t4([(0,r.wk)()],t9.prototype,"_activeTab",void 0),t4([(0,r.wk)()],t9.prototype,"_query",void 0),t4([(0,r.wk)()],t9.prototype,"_targetOverrides",void 0),t9=t4([(0,r.EM)("esphome-catalog-picker-dialog")],t9);class ie extends s.WF{connectedCallback(){super.connectedCallback(),this.addEventListener("request-catalog-pick",this._onRequest)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("request-catalog-pick",this._onRequest)}render(){return(0,s.qy)`<slot></slot>
      <esphome-catalog-picker-dialog></esphome-catalog-picker-dialog>`}constructor(...e){super(...e),this._onRequest=e=>{e.stopPropagation(),e.preventDefault(),this._picker.open(e.detail)}}}ie.styles=(0,s.AH)`
    :host {
      display: contents;
    }

    /* The host has no box, so keep the closed picker out of the section's
       flex flow; the open dialog renders in the top layer regardless. */
    esphome-catalog-picker-dialog {
      position: absolute;
    }
  `,t8([(0,r.P)("esphome-catalog-picker-dialog")],ie.prototype,"_picker",void 0),ie=t8([(0,r.EM)("esphome-catalog-picker-host")],ie);class it{keysFor(e){let t=new Map;this._items.forEach((e,i)=>ii(t,e,this._keys[i]));let i=e.map(e=>t.get(e)?.shift()),o=[...t].flatMap(([e,t])=>t.map(t=>({item:e,key:t}))),a=this._matchContent(e,i,o),s=new Set(a);return this._keys=a.map((e,t)=>{if(void 0!==e)return e;let i=this._keys[t];return void 0===i||s.has(i)?this._next++:(s.add(i),i)}),this._items=e,this._keys}_matchContent(e,t,i){let o=t.flatMap((e,t)=>void 0===e?[t]:[]),a=1===o.length&&1===i.length&&this._keys[o[0]]===i[0].key;if(0===o.length||0===i.length||a)return[...t];let s=new Map;for(let{item:e,key:t}of i)ii(s,io(e),t);return t.map((t,i)=>t??s.get(io(e[i]))?.shift())}constructor(){this._items=[],this._keys=[],this._next=0}}function ii(e,t,i){let o=e.get(t);o?o.push(i):e.set(t,[i])}function io(e){return JSON.stringify(e,(e,t)=>null===t||"object"!=typeof t||Array.isArray(t)?t:Object.fromEntries(Object.entries(t).filter(([,e])=>null===e||"object"!=typeof e||0!==Object.keys(e).length).sort(([e],[t])=>e<t?-1:+(e>t))))}function ia(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"arrow-down":a.mdiArrowDown,"arrow-up":a.mdiArrowUp,close:a.mdiClose,delete:a.mdiDelete,"pencil-outline":a.mdiPencilOutline,plus:a.mdiPlus});let is=[];class ir extends s.WF{willUpdate(e){if(!e.has("focusTarget"))return;this._focusScrolled=!1;let t=this.focusTarget?.node[0];this._focusRow="number"==typeof t?this._rows.keysFor(this.conditions)[t]:void 0}updated(e){e.has("conditions")&&this._refocus?.focus(),this._refocus=null,this._maybeScrollRow()}render(){let e=this._rows.keysFor(this.conditions);return(0,s.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?s.s6:(0,s.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_only_when")}</label
              >`}
        ${0===this.conditions.length?(0,s.qy)`<p class="ae-empty">${this._localize("device.add_condition")}</p>`:(0,tH.u)(this.conditions,(t,i)=>e[i],(t,i)=>this._renderNode(t,i,e[i]))}
        <button
          type="button"
          class="ae-add"
          ?disabled=${this.disabled||0===this.catalog.length}
          @click=${()=>this._openPicker(-1)}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("device.add_condition")}
        </button>
      </div>
    `}_renderNode(e,t,i){let o=this.catalog.find(t=>t.id===e.condition_id),a=this.conditions.length-1,r=this.focusTarget?.node[0]===t&&i===this._focusRow?this.focusTarget:null,n=r&&r.node.length>1?th(r):null,l=r&&1===r.node.length&&r.field.length>0?r.field:void 0;return(0,s.qy)`
      <div class="ae-row">
        <div class="ae-row-header">
          <button
            type="button"
            class="ae-row-picker"
            ?disabled=${this.disabled}
            @click=${()=>this._openPicker(t)}
          >
            <span class="ae-row-picker-name truncate">
              ${o?.name??e.condition_id}
            </span>
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
          ${o?.description?(0,s.qy)`<p class="ae-row-desc">${(0,ej.Gc)(o.description)}</p>`:s.s6}
          ${o&&(0,tJ.rq)(o).length>0?(0,s.qy)`<esphome-config-entry-form
                  .entries=${(0,tJ.rq)(o)}
                  .values=${e.params}
                  .requiredGroups=${o.required_groups??is}
                  .board=${this.board}
                  .yaml=${this.yaml}
                  .focusFieldPath=${l}
                  ?disabled=${this.disabled}
                  advanced-section
                  ?show-advanced=${this._advancedRows.has(i)}
                  @value-change=${e=>this._onParamChange(t,e)}
                  @advanced-toggle=${e=>this._onAdvancedToggle(t,e)}
                ></esphome-config-entry-form>`:s.s6}
          ${o?.accepts_condition_list?(0,s.qy)`<div class="ae-nested">
                  <p class="ae-nested-label">
                    ${this._localize("device.automation_condition")}
                  </p>
                  <esphome-automation-condition-tree
                    no-header
                    .conditions=${e.children??[]}
                    .focusTarget=${n}
                    .catalog=${this.catalog}
                    .devices=${this.devices}
                    .board=${this.board}
                    .yaml=${this.yaml}
                    ?disabled=${this.disabled}
                    @conditions-change=${e=>this._onChildrenChange(t,e)}
                  ></esphome-automation-condition-tree>
                </div>`:s.s6}
        </div>
      </div>
    `}_openPicker(e){0!==this.catalog.length&&(this._changingIdx=e,t7(this,{kind:"condition",items:this.catalog,devices:this.devices,onPicked:this._onConditionPicked}))}_onParamChange(e,t){t.stopPropagation();let i=this.conditions[e],o=(0,_.aG)(i.params,t.detail.path,t.detail.value);this._emit((0,_._D)(this.conditions,e,{...i,params:o}))}_onAdvancedToggle(e,t){t.stopPropagation(),this._setRowAdvanced(e,t.detail.show)}_setRowAdvanced(e,t){let i=this._rows.keysFor(this.conditions)[e],o=new Set(this._advancedRows);t?o.add(i):o.delete(i),this._advancedRows=o}_onChildrenChange(e,t){t.stopPropagation();let i=this.conditions[e];this._emit((0,_._D)(this.conditions,e,{...i,children:t.detail.conditions}))}_move(e,t){this._refocus=this.shadowRoot?.activeElement,this._emit((0,_.wg)(this.conditions,e,t))}_remove(e){this._emit((0,_.Wq)(this.conditions,e))}_maybeScrollRow(){let e=this.focusTarget;if(!e||this._focusScrolled)return;this._focusScrolled=!0;let t=e.node[0];if("number"!=typeof t)return;let i=this.catalog.find(e=>e.id===this.conditions[t]?.condition_id);if(!(e.node.length>1?!i?.accepts_condition_list:0===e.field.length||!i||0===(0,tJ.rq)(i).length))return;let o=this.shadowRoot?.querySelectorAll(".ae-row")[t];o&&(0,tx.uJ)(o)}_emit(e){(0,e$.r)(this,"conditions-change",{conditions:e})}constructor(...e){super(...e),this._localize=e=>e,this.conditions=[],this.catalog=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.devices=[],this.focusTarget=null,this._changingIdx=-1,this._advancedRows=new Set,this._rows=new it,this._focusScrolled=!1,this._refocus=null,this._onConditionPicked=e=>{let t=(0,_.LA)(e.id);e.preFilledParams&&(t.params={...t.params,...e.preFilledParams}),this._changingIdx>=0?(this._setRowAdvanced(this._changingIdx,!1),this._emit((0,_._D)(this.conditions,this._changingIdx,t))):this._emit([...this.conditions,t]),this._changingIdx=-1}}}function il(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}ir.styles=[M.G9,tC.z9,tO,tz.h],ia([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],ir.prototype,"_localize",void 0),ia([(0,r.MZ)({attribute:!1})],ir.prototype,"conditions",void 0),ia([(0,r.MZ)({attribute:!1})],ir.prototype,"catalog",void 0),ia([(0,r.MZ)({attribute:!1})],ir.prototype,"board",void 0),ia([(0,r.MZ)()],ir.prototype,"yaml",void 0),ia([(0,r.MZ)({type:Boolean})],ir.prototype,"disabled",void 0),ia([(0,r.MZ)({type:Boolean,attribute:"no-header"})],ir.prototype,"noHeader",void 0),ia([(0,r.MZ)({attribute:!1})],ir.prototype,"devices",void 0),ia([(0,r.MZ)({attribute:!1,hasChanged:tv})],ir.prototype,"focusTarget",void 0),ia([(0,r.wk)()],ir.prototype,"_changingIdx",void 0),ia([(0,r.wk)()],ir.prototype,"_advancedRows",void 0),ir=ia([(0,r.EM)("esphome-automation-condition-tree")],ir),(0,I.C)({"arrow-down":a.mdiArrowDown,"arrow-up":a.mdiArrowUp,delete:a.mdiDelete,plus:a.mdiPlus});class id extends s.WF{willUpdate(e){if(!e.has("focusTarget"))return;this._focusScrolled=!1;let t=this.focusTarget?.node[0];this._focusRow="number"==typeof t?this._rows.keysFor(this.branches)[t]:void 0}updated(e){e.has("branches")&&this._refocus?.focus(),this._refocus=null;let t=this.focusTarget;if(!t||this._focusScrolled||(this._focusScrolled=!0,1!==t.node.length||"number"!=typeof t.node[0]))return;let i=this.shadowRoot?.querySelectorAll(".ae-nested")[t.node[0]];i&&(0,tx.uJ)(i)}render(){let e=this._rows.keysFor(this.branches);return(0,s.qy)`
      ${(0,tH.u)(this.branches,(t,i)=>e[i],(t,i)=>this._renderBranch(t,i,e[i]))}
      <button
        type="button"
        class="ae-add"
        ?disabled=${this.disabled}
        @click=${this._addBranch}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${this._localize("device.automation_add_branch")}
      </button>
    `}_renderBranch(e,t,i){let o=this.focusTarget?.node[0]===t&&i===this._focusRow?th(this.focusTarget):null;return(0,s.qy)`<div class="ae-nested">
      <div class="ae-branch-header">
        <p class="ae-nested-label">
          ${this._localize("device.automation_branch",{n:t+1})}
        </p>
        <div class="ae-row-controls">
          <button
            type="button"
            ?disabled=${this.disabled||0===t}
            aria-label=${this._localize("device.automation_move_up")}
            @click=${e=>this._move(e,t,-1)}
          >
            <wa-icon library="mdi" name="arrow-up"></wa-icon>
          </button>
          <button
            type="button"
            ?disabled=${this.disabled||t===this.branches.length-1}
            aria-label=${this._localize("device.automation_move_down")}
            @click=${e=>this._move(e,t,1)}
          >
            <wa-icon library="mdi" name="arrow-down"></wa-icon>
          </button>
          <button
            type="button"
            class="ae-row-delete"
            ?disabled=${this.disabled||1===this.branches.length}
            aria-label=${this._localize("device.automation_remove_branch")}
            @click=${()=>this._emit((0,_.Wq)(this.branches,t))}
          >
            <wa-icon library="mdi" name="delete"></wa-icon>
          </button>
        </div>
      </div>
      <p class="ae-nested-label">${this._localize("device.automation_branch_if")}</p>
      <esphome-automation-condition-tree
        no-header
        .conditions=${e.conditions}
        .focusTarget=${o?.node[0]==="conditions"?th(o):null}
        .catalog=${this.conditionCatalog}
        .devices=${this.devices}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        @conditions-change=${e=>{e.stopPropagation(),this._patch(t,{conditions:e.detail.conditions})}}
      ></esphome-automation-condition-tree>
      <p class="ae-nested-label">${this._localize("device.automation_branch_then")}</p>
      <esphome-automation-action-list
        no-header
        .actions=${e.actions}
        .focusTarget=${o?.node[0]==="then"?th(o):null}
        .catalog=${this.catalog}
        .conditionCatalog=${this.conditionCatalog}
        .scripts=${this.scripts}
        .devices=${this.devices}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        @actions-change=${e=>{e.stopPropagation(),this._patch(t,{actions:e.detail.actions})}}
      ></esphome-automation-action-list>
    </div>`}_move(e,t,i){this._refocus=e.currentTarget,this._emit((0,_.wg)(this.branches,t,t+i))}_patch(e,t){this._emit((0,_._D)(this.branches,e,{...this.branches[e],...t}))}_emit(e){(0,e$.r)(this,"branches-change",{branches:e})}constructor(...e){super(...e),this._localize=e=>e,this.branches=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.focusTarget=null,this._rows=new it,this._focusScrolled=!1,this._refocus=null,this._addBranch=()=>{this._emit([...this.branches,(0,_.Ly)()])}}}function ic(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}id.styles=[M.G9,tO,tz.h,(0,s.AH)`
      .ae-branch-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--wa-space-xs);
      }
      .ae-branch-header .ae-nested-label {
        margin-bottom: 0;
      }
    `],il([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],id.prototype,"_localize",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"branches",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"catalog",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"conditionCatalog",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"scripts",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"devices",void 0),il([(0,r.MZ)({attribute:!1})],id.prototype,"board",void 0),il([(0,r.MZ)()],id.prototype,"yaml",void 0),il([(0,r.MZ)({type:Boolean})],id.prototype,"disabled",void 0),il([(0,r.MZ)({attribute:!1,hasChanged:tv})],id.prototype,"focusTarget",void 0),id=il([(0,r.EM)("esphome-automation-choose-branches")],id),i(1687),i(4063),(0,I.C)({"arrow-down":a.mdiArrowDown,"arrow-up":a.mdiArrowUp,"chevron-down":a.mdiChevronDown,"chevron-up":a.mdiChevronUp,close:a.mdiClose,delete:a.mdiDelete,"pencil-outline":a.mdiPencilOutline});let ih=[];function ip(e){return!!e?.has_condition_gate}class iu extends s.WF{willUpdate(e){if(e.has("value")){let t=e.get("value");t&&t.action_id!==this.value.action_id&&(this._collapsed=!1,this._showAdvanced=!1)}e.has("focusTarget")&&(this._focusScrolled=!1,this.focusTarget&&(this._collapsed=!1))}updated(){this._maybeScrollSelf()}_maybeScrollSelf(){let e=this.focusTarget;if(!e||this._focusScrolled||(this._focusScrolled=!0,!this._isTerminalFocus(e)))return;let t=this.shadowRoot?.querySelector(".ae-row");t&&(0,tx.uJ)(t)}_isTerminalFocus(e){let t=this.catalog.find(e=>e.id===this.value.action_id),i=e.node[0];return"conditions"===i?!ip(t):"branches"===i?!t?.has_branches:"string"==typeof i?!(t?.accepts_action_list??[]).includes(i):0===e.field.length||!t||0===(0,tJ.rq)(t).length}render(){let e=this.catalog.find(e=>e.id===this.value.action_id),t=this._collapsed;return(0,s.qy)`
      <div class="ae-row ${t?"ae-row--collapsed":""}">
        <div class="ae-row-header">
          <button
            type="button"
            class="ae-row-picker"
            ?disabled=${this.disabled}
            title=${this._localize("device.automation_action_pick")}
            @click=${this._openPicker}
          >
            <span class="ae-row-picker-name truncate">
              ${e?.name??this.value.action_id}
            </span>
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
        ${t?s.s6:(0,s.qy)`<div class="ae-row-body">
                ${this.value.unknown?(0,s.qy)`<p class="ae-row-unknown" role="note">
                        ${this._localize("device.automation_action_unknown")}
                      </p>`:s.s6}
                ${e?.description?(0,s.qy)`<p class="ae-row-desc">${(0,ej.Gc)(e.description)}</p>`:s.s6}
                ${this._renderActionParams(e)} ${this._renderScriptParams(e)}
                ${this._renderConditionGate(e)} ${this._renderBranches(e)}
                ${this._renderNestedLists(e)}
              </div>`}
      </div>
    `}_renderScriptParams(e){if(e?.id!=="script.execute")return s.s6;let t=String(this.value.params.id??""),i=this.scripts.find(e=>e.id===t);return i&&0!==i.parameters.length?(0,s.qy)`<div class="ae-nested">
      <p class="ae-nested-label">
        ${this._localize("device.automation_script_parameters")}
      </p>
      ${i.parameters.map(e=>(0,s.qy)`<label class="ae-section-label" for="script-${e.name}"
              >${e.name} <span class="ae-muted">${e.type}</span></label
            >
            <input
              id="script-${e.name}"
              type=${"int"===e.type||"float"===e.type?"number":"text"}
              ?disabled=${this.disabled}
              .value=${String(this.value.params[e.name]??"")}
              @input=${t=>{let i=t.target.value;this._patchParams({[e.name]:(0,tW.Ae)(e.type,i)})}}
            />`)}
    </div>`:s.s6}_renderConditionGate(e){return ip(e)?(0,s.qy)`<div class="ae-nested">
      <p class="ae-nested-label">${this._localize("device.automation_only_when")}</p>
      <esphome-automation-condition-tree
        no-header
        .conditions=${this.value.conditions??[]}
        .focusTarget=${this.focusTarget?.node[0]==="conditions"?th(this.focusTarget):null}
        .catalog=${this.conditionCatalog}
        .devices=${this.devices}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        @conditions-change=${this._onConditionsChange}
      ></esphome-automation-condition-tree>
    </div>`:s.s6}_renderBranches(e){return e?.has_branches?(0,s.qy)`<esphome-automation-choose-branches
      .branches=${this.value.branches??[]}
      .focusTarget=${this.focusTarget?.node[0]==="branches"?th(this.focusTarget):null}
      .catalog=${this.catalog}
      .conditionCatalog=${this.conditionCatalog}
      .scripts=${this.scripts}
      .devices=${this.devices}
      .board=${this.board}
      .yaml=${this.yaml}
      ?disabled=${this.disabled}
      @branches-change=${this._onBranchesChange}
    ></esphome-automation-choose-branches>`:s.s6}_nestedListLabel(e){return"else"===e?this._localize("device.automation_else"):"then"===e?this._localize("device.automation_action"):e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}_renderNestedLists(e){return e&&e.accepts_action_list&&0!==e.accepts_action_list.length?e.accepts_action_list.map(e=>(0,s.qy)`<div class="ae-nested">
          <p class="ae-nested-label">${this._nestedListLabel(e)}</p>
          <esphome-automation-action-list
            no-header
            .actions=${this.value.children?.[e]??[]}
            .focusTarget=${this.focusTarget?.node[0]===e?th(this.focusTarget):null}
            .catalog=${this.catalog}
            .conditionCatalog=${this.conditionCatalog}
            .scripts=${this.scripts}
            .devices=${this.devices}
            .board=${this.board}
            .yaml=${this.yaml}
            ?disabled=${this.disabled}
            @actions-change=${t=>{t.stopPropagation(),this._onChildrenChange(e,t.detail.actions)}}
          ></esphome-automation-action-list>
        </div>`):s.s6}_renderActionParams(e){let t=e?(0,tJ.rq)(e):[];if(!e||0===t.length)return s.s6;let i=this.focusTarget;return(0,s.qy)`<esphome-config-entry-form
      .entries=${t}
      .values=${this.value.params}
      .requiredGroups=${e.required_groups??ih}
      .board=${this.board}
      .yaml=${this.yaml}
      .focusFieldPath=${i&&0===i.node.length&&i.field.length>0?i.field:void 0}
      ?disabled=${this.disabled}
      advanced-section
      ?show-advanced=${this._showAdvanced}
      @value-change=${this._onParamChange}
      @advanced-toggle=${this._onAdvancedToggle}
    ></esphome-config-entry-form>`}_patchParams(e){this._emit({...this.value,params:{...this.value.params,...e}})}_onChildrenChange(e,t){let i={...this.value.children??{},[e]:t};this._emit({...this.value,children:i})}_reorder(e){(0,e$.r)(this,"action-reorder",{delta:e})}_emit(e){(0,e$.r)(this,"action-change",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.first=!1,this.last=!1,this.focusTarget=null,this._collapsed=!1,this._showAdvanced=!1,this._focusScrolled=!1,this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._openPicker=()=>{t7(this,{kind:"action",items:this.catalog,devices:this.devices,onPicked:this._onActionPicked})},this._onActionPicked=e=>{this._emit((0,_.Gi)(e.id,this.catalog.find(t=>t.id===e.id),e.preFilledParams))},this._onParamChange=e=>{e.stopPropagation();let t=(0,_.aG)(this.value.params,e.detail.path,e.detail.value);this._emit({...this.value,params:t})},this._onConditionsChange=e=>{e.stopPropagation(),this._emit({...this.value,conditions:e.detail.conditions})},this._onBranchesChange=e=>{e.stopPropagation(),this._emit({...this.value,branches:e.detail.branches})},this._onDelete=()=>{(0,e$.r)(this,"action-delete")}}}function i_(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}iu.styles=[M.G9,tC.z9,tO,tz.h],ic([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],iu.prototype,"_localize",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"value",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"catalog",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"conditionCatalog",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"scripts",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"devices",void 0),ic([(0,r.MZ)({attribute:!1})],iu.prototype,"board",void 0),ic([(0,r.MZ)()],iu.prototype,"yaml",void 0),ic([(0,r.MZ)({type:Boolean})],iu.prototype,"disabled",void 0),ic([(0,r.MZ)({type:Boolean})],iu.prototype,"first",void 0),ic([(0,r.MZ)({type:Boolean})],iu.prototype,"last",void 0),ic([(0,r.MZ)({attribute:!1,hasChanged:tv})],iu.prototype,"focusTarget",void 0),ic([(0,r.wk)()],iu.prototype,"_collapsed",void 0),ic([(0,r.wk)()],iu.prototype,"_showAdvanced",void 0),iu=ic([(0,r.EM)("esphome-automation-action-node")],iu),(0,I.C)({plus:a.mdiPlus});class im extends s.WF{willUpdate(e){if(!e.has("focusTarget"))return;let t=this.focusTarget?.node[0];this._focusRow="number"==typeof t?this._rows.keysFor(this.actions)[t]:void 0}updated(e){e.has("actions")&&this._refocus?.focus(),this._refocus=null}render(){let e=this._rows.keysFor(this.actions);return(0,s.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?s.s6:(0,s.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_action")}</label
              >`}
        ${0===this.actions.length?(0,s.qy)`<p class="empty-message--dashed" role="status">
                ${this._localize("device.automation_actions_empty")}
              </p>`:(0,tH.u)(this.actions,(t,i)=>e[i],(t,i)=>this._renderRow(t,i,e[i]))}
        <button
          type="button"
          class="ae-add"
          ?disabled=${this.disabled||0===this.catalog.length}
          @click=${this._openPicker}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("device.add_action")}
        </button>
      </div>
    `}_renderRow(e,t,i){let o=this.focusTarget,a=t===this.actions.length-1;return(0,s.qy)`<esphome-automation-action-node
      .value=${e}
      .focusTarget=${o?.node[0]===t&&i===this._focusRow?th(o):null}
      .catalog=${this.catalog}
      .conditionCatalog=${this.conditionCatalog}
      .scripts=${this.scripts}
      .devices=${this.devices}
      .board=${this.board}
      .yaml=${this.yaml}
      ?disabled=${this.disabled}
      ?first=${0===t}
      ?last=${a}
      @action-change=${e=>this._onActionChange(t,e)}
      @action-reorder=${e=>this._onReorder(t,e)}
      @action-delete=${e=>this._onDelete(t,e)}
    ></esphome-automation-action-node>`}_onActionChange(e,t){t.stopPropagation(),this._emit((0,_._D)(this.actions,e,t.detail.value))}_onReorder(e,t){t.stopPropagation();let i=t.currentTarget;this._refocus=i.shadowRoot?.activeElement,this._emit((0,_.wg)(this.actions,e,e+t.detail.delta))}_onDelete(e,t){t.stopPropagation(),this._emit((0,_.Wq)(this.actions,e))}_emit(e){(0,e$.r)(this,"actions-change",{actions:e})}constructor(...e){super(...e),this._localize=e=>e,this.actions=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.focusTarget=null,this._rows=new it,this._refocus=null,this._openPicker=()=>{0!==this.catalog.length&&t7(this,{kind:"action",items:this.catalog,devices:this.devices,onPicked:this._onActionPicked})},this._onActionPicked=e=>{let t=(0,_.Gi)(e.id,this.catalog.find(t=>t.id===e.id),e.preFilledParams);this._emit([...this.actions,t])}}}function iv(e){return(0,s.qy)`
    <div class="field">
      <label class="field-label"> ${e.localize("device.automation_action")} </label>
      <p class="field-description">
        ${(0,ej.Gc)(e.localize(e.descriptionKey))}
      </p>
      <esphome-catalog-picker-host>
        <esphome-automation-action-list
          no-header
          .focusTarget=${e.focusTarget??null}
          .actions=${e.automation.actions}
          .catalog=${e.catalog}
          .conditionCatalog=${e.conditionCatalog}
          .scripts=${e.scripts}
          .devices=${e.devices}
          .board=${e.board}
          .yaml=${e.yaml}
          ?disabled=${e.disabled}
          @actions-change=${e.onActionsChange}
        ></esphome-automation-action-list>
      </esphome-catalog-picker-host>
    </div>
  `}im.styles=[M.G9,tC.z9,tO],i_([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],im.prototype,"_localize",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"actions",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"catalog",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"conditionCatalog",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"scripts",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"devices",void 0),i_([(0,r.MZ)({attribute:!1})],im.prototype,"board",void 0),i_([(0,r.MZ)()],im.prototype,"yaml",void 0),i_([(0,r.MZ)({type:Boolean})],im.prototype,"disabled",void 0),i_([(0,r.MZ)({type:Boolean,attribute:"no-header"})],im.prototype,"noHeader",void 0),i_([(0,r.MZ)({attribute:!1,hasChanged:tv})],im.prototype,"focusTarget",void 0),im=i_([(0,r.EM)("esphome-automation-action-list")],im);var ig=i(664);function iy(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({close:a.mdiClose,plus:a.mdiPlus});let ib=["int","float","bool","string"];class iw extends s.WF{willUpdate(e){e.has("focusParam")&&(this._focusScrolled=!1)}updated(e){if(e.has("value")){let e=this._readFromWire(),t=this._params.filter(e=>e.name);t.length===e.length&&t.every((t,i)=>t.name===e[i].name&&t.type===e[i].type)||(this._params=e)}this._maybeScrollToParam()}render(){return(0,s.qy)`<div class="field">
      ${this.fieldLabel?(0,s.qy)`<label class="field-label">${this.fieldLabel}</label>`:s.s6}
      ${this.description?(0,s.qy)`<p class="field-description">${(0,ej.Gc)(this.description)}</p>`:s.s6}
      ${0===this._params.length?s.s6:(0,s.qy)`<div class="script-params-list">
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
    </div>`}_renderRow(e,t){return(0,s.qy)`<div class="script-param-row">
      <input
        type="text"
        ?disabled=${this.disabled}
        placeholder=${this.namePlaceholder}
        .value=${e.name}
        @input=${i=>this._updateRow(t,{...e,name:(0,ig.e)(i.target.value)})}
      />
      <wa-select
        value=${e.type}
        ?disabled=${this.disabled}
        @change=${i=>this._updateRow(t,{...e,type:i.target.value})}
      >
        ${ib.map(t=>(0,s.qy)`<wa-option value=${t} ?selected=${t===e.type}>${t}</wa-option>`)}
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
    </div>`}_maybeScrollToParam(){if(null===this.focusParam||this._focusScrolled)return;if(""===this.focusParam){this._focusScrolled=!0;let e=this.shadowRoot?.querySelector(".field");e&&(0,tx.uJ)(e);return}let e=this._params.findIndex(e=>e.name===this.focusParam);if(e<0)return;let t=this.shadowRoot?.querySelectorAll(".script-param-row")[e];t&&(this._focusScrolled=!0,(0,tx.uJ)(t))}_readFromWire(){return this.value&&"object"==typeof this.value?Object.entries(this.value).map(([e,t])=>({name:e,type:String(t??"string")})):[]}_emit(e){this._params=e;let t={};for(let{name:i,type:o}of e)i&&(t[i]=o);this.dispatchEvent(new CustomEvent("value-change",{detail:{value:t},bubbles:!0,composed:!0}))}_updateRow(e,t){let i=this._params.slice();i[e]=t,this._emit(i)}_removeRow(e){let t=this._params.slice();t.splice(e,1),this._emit(t)}constructor(...e){super(...e),this._localize=e=>e,this.value={},this.disabled=!1,this.fieldLabel="",this.description="",this.addLabel="",this.namePlaceholder="",this.focusParam=null,this._params=[],this._focusScrolled=!1,this._addRow=()=>{this._emit([...this._params,{name:"",type:"int"}])}}}iw.styles=[M.G9,tC.z9,tO,tz.h],iy([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],iw.prototype,"_localize",void 0),iy([(0,r.MZ)({attribute:!1})],iw.prototype,"value",void 0),iy([(0,r.MZ)({type:Boolean})],iw.prototype,"disabled",void 0),iy([(0,r.MZ)()],iw.prototype,"fieldLabel",void 0),iy([(0,r.MZ)()],iw.prototype,"description",void 0),iy([(0,r.MZ)()],iw.prototype,"addLabel",void 0),iy([(0,r.MZ)()],iw.prototype,"namePlaceholder",void 0),iy([(0,r.MZ)()],iw.prototype,"focusParam",void 0),iy([(0,r.wk)()],iw.prototype,"_params",void 0),iw=iy([(0,r.EM)("esphome-callable-params-editor")],iw),(0,I.C)({"open-in-new":a.mdiOpenInNew,webhook:a.mdiWebhook});let i$=`${tn.Ik}/components/api.html`;class ik extends tG{_canApply(e){return"api_action"===e.kind&&!!e.action_name}render(){let e=this.renderStateGate();if(e)return e;let t=this.value??(0,_.rN)(),i=this._available?.devices??[],o=this._available?.scripts??[],a=this._available?.actions??[],r=this._available?.conditions??[],n=this._engine.deleting,l=this._currentFocus();return(0,tr.D)(this._target,(0,s.qy)`
        ${this._renderHeader()}
        ${this._renderNameField({label:this._localize("device.api_action_id_label"),description:this._localize("device.api_action_id_description"),value:this.location?.action_name??""},n)}
        <esphome-callable-params-editor
          .value=${t.trigger_params.variables??{}}
          .focusParam=${t_(l,"variables")}
          ?disabled=${n}
          .fieldLabel=${this._localize("device.api_action_variables")}
          .description=${this._localize("device.api_action_variables_description")}
          .addLabel=${this._localize("device.api_action_add_variable")}
          .namePlaceholder=${this._localize("device.api_action_variable_name_placeholder")}
          @value-change=${this._onVariablesChange}
        ></esphome-callable-params-editor>
        ${iv({automation:t,catalog:a,conditionCatalog:r,scripts:o,devices:i,board:this.board,yaml:this.yaml,disabled:n,localize:this._localize,focusTarget:tp(l),descriptionKey:"device.api_action_actions_description",onActionsChange:this._onActionsChange})}
        ${this.renderFooter({label:this._localize("device.delete_api_action"),message:e=>this._localize("device.confirm_delete_api_action",{name:e.action_name})})}
      `)}_renderHeader(){return(0,s.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">
          ${this._localize("device.api_action_header_title_static")}
        </h2>
        <a class="ae-header-docs" href=${i$} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">
          ${(0,ej.Gc)(this._localize("device.api_action_header_description"))}
        </p>
      </div>
      <div class="ae-header-icon">
        <wa-icon library="mdi" name="webhook"></wa-icon>
      </div>
    </div>`}constructor(...e){super(...e),this._nameInputId="api-action-name",this._nameYamlKeys=["action","service"],this._onVariablesChange=e=>{e.stopPropagation();let t=this.value??(0,_.rN)();this._engine.withValue({trigger_params:{...t.trigger_params,variables:e.detail.value}})}}}ik=function(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}([(0,r.EM)("esphome-api-action-editor")],ik);var ix=i(4323);function iz(e,t,i){return e?.kind==="interval"?i("device.automation_interval_label"):t&&(e?.kind==="device_on"||e?.kind==="component_on")?t.name:e?.kind==="component_action"?(0,ix.t)(e.field,i):i("device.automation_header_title_static")}var iC=i(5413),iS=i(2353),iF=i(4117);function iP(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"arrow-decision-outline":a.mdiArrowDecisionOutline,"open-in-new":a.mdiOpenInNew});let iq=["device_on","component_on","interval","script"];class iM extends s.WF{render(){let e=this.value&&"component_action"!==this.value.kind?this.value.kind:"device_on";return(0,s.qy)`
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
          ${iq.map(t=>(0,s.qy)`<wa-option value=${t} ?selected=${t===e}
                >${this._kindLabel(t)}</wa-option
              >`)}
        </wa-select>
        ${this._renderKindBody(e)}
      </div>
    `}_kindLabel(e){switch(e){case"device_on":return this._localize("device.automation_target_device");case"component_on":return this._localize("device.automation_target_component");case"interval":return this._localize("device.automation_target_interval");case"script":return this._localize("device.automation_target_script");case"api_action":return this._localize("device.automation_target_api_action");case"light_effect":return this._localize("device.automation_light_effect")}}_renderKindBody(e){if("device_on"===e||"interval"===e)return s.s6;if("component_on"===e){let e=this.value?.kind==="component_on"?this.value.component_id:"",t=this.devices.filter(e=>(0,t3.e1)(e,this.triggers)),i=(0,t3.vJ)(this.devices);return 0===t.length?(0,s.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_components")}
        </p>`:(0,s.qy)`
        <label class="ae-section-label" id="component-id-label"
          >${this._localize("device.automation_target_component_label")}</label
        >
        <wa-select
          aria-labelledby="component-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onComponentChange(e.target.value)}
        >
          ${t.map(t=>(0,s.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${(0,t3.zl)(t)}
                <span class="ae-muted">(${i(t)})</span></wa-option
              >`)}
        </wa-select>
      `}if("script"===e){let e=this.value?.kind==="script"?this.value.id:"";return this.locked?(0,s.qy)`
          <label class="ae-section-label">
            ${this._localize("device.automation_target_script_label")}
          </label>
          <p class="ae-section-desc">${e}</p>
        `:(0,s.qy)`
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
      `}if("api_action"===e){let e=this.value?.kind==="api_action"?this.value.action_name:"";return(0,s.qy)`
        <label class="ae-section-label">
          ${this._localize("device.automation_target_api_action_label")}
        </label>
        <p class="ae-section-desc">${e}</p>
      `}if("light_effect"===e){let e=this.value?.kind==="light_effect"?this.value.component_id:"",t=this.devices.filter(e=>e.component_id.startsWith("light."));return 0===t.length?(0,s.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_lights")}
        </p>`:(0,s.qy)`
        <label class="ae-section-label" id="light-id-label"
          >${this._localize("device.automation_target_light_label")}</label
        >
        <wa-select
          aria-labelledby="light-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onLightChange(e.target.value)}
        >
          ${t.map(t=>(0,s.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${(0,t3.zl)(t)}</wa-option
              >`)}
        </wa-select>
      `}return s.s6}_onKindChange(e){let t=e.target.value,i=(()=>{switch(t){case"device_on":return{kind:t,trigger:"on_boot"};case"interval":return{kind:t,index:0};case"component_on":{let e=(0,t3.Oj)(this.devices,this.triggers);return e?{kind:t,component_id:e.id,trigger:""}:null}case"script":return{kind:t,id:this.scripts.length?this.scripts[0].id:""};case"light_effect":{let e=this.devices.find(e=>e.component_id.startsWith("light."));return e?{kind:t,component_id:e.id,index:0}:null}case"api_action":return null}})();this._emit(i)}_onComponentChange(e){this.value?.kind==="component_on"&&this._emit({...this.value,component_id:e})}_onScriptChange(e){this._emit({kind:"script",id:e})}_onLightChange(e){this.value?.kind==="light_effect"&&this._emit({...this.value,component_id:e})}_emit(e){this.dispatchEvent(new CustomEvent("target-change",{detail:{target:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value=null,this.devices=[],this.triggers=[],this.scripts=[],this.disabled=!1,this.locked=!1}}function iL(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}iM.styles=[M.G9,tC.z9,tO],iP([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],iM.prototype,"_localize",void 0),iP([(0,r.MZ)({attribute:!1})],iM.prototype,"value",void 0),iP([(0,r.MZ)({attribute:!1})],iM.prototype,"devices",void 0),iP([(0,r.MZ)({attribute:!1})],iM.prototype,"triggers",void 0),iP([(0,r.MZ)({attribute:!1})],iM.prototype,"scripts",void 0),iP([(0,r.MZ)({type:Boolean})],iM.prototype,"disabled",void 0),iP([(0,r.MZ)({type:Boolean})],iM.prototype,"locked",void 0),iM=iP([(0,r.EM)("esphome-automation-target-picker")],iM);class iR extends s.WF{willUpdate(e){e.has("triggerId")&&(this._showAdvanced=!1)}render(){if(!this.target)return(0,s.qy)`<p class="ae-empty">
        ${this._localize("device.automation_target_placeholder")}
      </p>`;if("interval"===this.target.kind||"script"===this.target.kind||"api_action"===this.target.kind||"light_effect"===this.target.kind)return s.s6;let e=this._filteredTriggers(),t=e.find(e=>e.id===this.triggerId),i="component_on"===this.target.kind?this.target.component_id:null,o=i?this.devices.find(e=>e.id===i)??null:null;return(0,s.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="trigger-label"
          >${this._localize("device.automation_trigger")}</label
        >
        ${o?(0,s.qy)`<p class="ae-section-desc">
                ${this._localize("device.automation_trigger_on_component",{component:(0,t3.zl)(o),domain:o.component_id})}
              </p>`:s.s6}
        ${0===e.length?(0,s.qy)`<p class="ae-empty" role="status">
                ${this._localize("device.automation_trigger_none_available")}
              </p>`:(0,s.qy)`<wa-select
                aria-labelledby="trigger-label"
                value=${this.triggerId??""}
                ?disabled=${this.disabled}
                @change=${this._onTriggerChange}
              >
                ${e.map(e=>(0,s.qy)`<wa-option value=${e.id} ?selected=${e.id===this.triggerId}
                      >${e.name}</wa-option
                    >`)}
              </wa-select>`}
        ${t?.description?(0,s.qy)`<p class="ae-section-desc">${(0,ej.Gc)(t.description)}</p>`:s.s6}
        ${t&&t.config_entries.length>0?(0,s.qy)`<esphome-config-entry-form
                .entries=${t.config_entries}
                .values=${this.triggerParams}
                .board=${this.board}
                .yaml=${this.yaml}
                ?disabled=${this.disabled}
                advanced-section
                ?show-advanced=${this._showAdvanced}
                @value-change=${this._onParamChange}
                @advanced-toggle=${this._onAdvancedToggle}
              ></esphome-config-entry-form>`:s.s6}
      </div>
    `}_filteredTriggers(){if(!this.target)return[];if("device_on"===this.target.kind)return this.triggers.filter(e=>e.is_device_level);if("component_on"===this.target.kind){let e=this.target.component_id,t=this.devices.find(t=>t.id===e);return(0,t3.mR)(this.triggers,t)}return[]}constructor(...e){super(...e),this._localize=e=>e,this.target=null,this.triggers=[],this.devices=[],this.triggerId=null,this.triggerParams={},this.board=null,this.yaml="",this.disabled=!1,this._showAdvanced=!1,this._onTriggerChange=e=>{let t=e.target.value;(0,e$.r)(this,"trigger-change",{triggerId:t,params:{}})},this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onParamChange=e=>{e.stopPropagation();let t=(0,_.aG)(this.triggerParams,e.detail.path,e.detail.value);(0,e$.r)(this,"trigger-params-change",{params:t})}}}iR.styles=[M.G9,tC.z9,tO],iL([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],iR.prototype,"_localize",void 0),iL([(0,r.MZ)({attribute:!1})],iR.prototype,"target",void 0),iL([(0,r.MZ)({attribute:!1})],iR.prototype,"triggers",void 0),iL([(0,r.MZ)({attribute:!1})],iR.prototype,"devices",void 0),iL([(0,r.MZ)()],iR.prototype,"triggerId",void 0),iL([(0,r.MZ)({attribute:!1})],iR.prototype,"triggerParams",void 0),iL([(0,r.MZ)({attribute:!1})],iR.prototype,"board",void 0),iL([(0,r.MZ)()],iR.prototype,"yaml",void 0),iL([(0,r.MZ)({type:Boolean})],iR.prototype,"disabled",void 0),iL([(0,r.wk)()],iR.prototype,"_showAdvanced",void 0),iR=iL([(0,r.EM)("esphome-automation-trigger-picker")],iR);var iA=i(2564);function iE(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}class iT extends tN{connectedCallback(){super.connectedCallback()}updated(e){super.updated(e),(e.has("location")||e.has("platform"))&&this.location?.kind==="interval"&&this._loadIntervalComponent()}async _loadIntervalComponent(){if(!this._api)return;let e=await async function(e,t,i){let o=(0,iF.CQ)("interval",t,i);if(o)return o;try{return await (0,iF.Sn)(e,"interval",t,i)??null}catch{return null}}(this._api,this.platform||void 0,this.board?.id);e&&(this._intervalComponent=e)}async _loadAvailable(){if(!this._api||!this.configuration)return;this._loading=!0,this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize,{lists:["triggers","actions","conditions"],yaml:this.yaml,onPaint:e=>{this._available=e,this._loading=!1}});void 0!==t&&(this._error=t,this._loading=!1),e&&(this._available=e,this._loading=!1)}render(){var e,t,i,o,a,r,n,l;let d,c,h,p,u,m,v=this.renderStateGate();if(v)return v;let g=this.value??(0,_.rN)(),f=this.location,y=this._available?.devices??[],b=this._available?.scripts??[],w=this._available?.triggers??[],$=this._available?.actions??[],k=this._available?.conditions??[],x=this._engine.deleting,z=g.trigger_id??(f?.kind==="device_on"?f.trigger||null:f?.kind==="component_on"&&function(e,t,i){if("component_on"!==e.kind||!e.trigger)return null;let o=t.find(t=>t.id===e.component_id);return o?(0,iS.$Z)(i,(0,iS.PM)(o),e.trigger)?.id??e.trigger:e.trigger}(f,y,w)||null),C=z?w.find(e=>e.id===z)??null:null,S=this._currentFocus();return(0,tr.D)(this._target,(0,s.qy)`
        ${(e=this.location,t=this._intervalComponent,i=this._localize,d=e?.kind==="interval"?t:null,c=d?.name??iz(e,C,i),h=d?.docs_url??C?.docs_url??"",p=d?.description??C?.description??i("device.automation_header_description"),u=d?.image_url??"",(0,s.qy)`<div class="ae-header">
    <div class="ae-header-text">
      <h2 class="ae-header-title">${c}</h2>
      ${h?(0,s.qy)`<a
              class="ae-header-docs"
              href=${h}
              target="_blank"
              rel="noreferrer"
            >
              ${i("device.docs")}
              <wa-icon library="mdi" name="open-in-new"></wa-icon>
            </a>`:s.s6}
      <p class="ae-header-desc">${(0,ej.Gc)(p)}</p>
    </div>
    <div class="ae-header-icon">
      ${u?(0,s.qy)`<img alt="" src=${u} />`:(0,s.qy)`<wa-icon library="mdi" name="arrow-decision-outline"></wa-icon>`}
    </div>
  </div>`)}
        ${this.addMode?(o={target:f,triggers:w,devices:y,scripts:b,effectiveTriggerId:z,automation:g,board:this.board,yaml:this.yaml,disabled:x,onTargetChange:this._onTargetChange,onTriggerChange:this._onTriggerChange,onTriggerParamsChange:this._onTriggerParamsChange},(0,s.qy)`
    <esphome-automation-target-picker
      .value=${o.target}
      .devices=${o.devices}
      .triggers=${o.triggers}
      .scripts=${o.scripts}
      ?disabled=${o.disabled}
      @target-change=${o.onTargetChange}
    ></esphome-automation-target-picker>
    <esphome-automation-trigger-picker
      .target=${o.target}
      .triggers=${o.triggers}
      .devices=${o.devices}
      .triggerId=${o.effectiveTriggerId}
      .triggerParams=${o.automation.trigger_params}
      .board=${o.board}
      .yaml=${o.yaml}
      ?disabled=${o.disabled}
      @trigger-change=${o.onTriggerChange}
      @trigger-params-change=${o.onTriggerParamsChange}
    ></esphome-automation-trigger-picker>
  `):(0,s.qy)`${function(e,t,i,o){var a;return e&&("component_on"===e.kind||"component_action"===e.kind)?(a=function(e,t,i){switch(e.kind){case"device_on":return i("device.automation_target_device");case"component_on":case"component_action":{let i=t.find(t=>t.id===e.component_id);if(!i)return e.component_id;return`${(0,t3.zl)(i)} (${i.component_id})`}case"interval":return i("device.automation_target_interval_n",{index:e.index+1});case"script":return e.id;case"api_action":return e.action_name;case"light_effect":return e.component_id}}(e,t,o),(0,s.qy)`<div class="field">
    <label class="field-label"> ${o("device.automation_target")} </label>
    <input type="text" readonly .value=${a} />
    ${(0,iA.Nk)(a,i,o)}
  </div>`):s.s6}(this.location,y,this._parseSubstitutions(this.yaml),this._localize)}${r=(a={location:this.location,intervalComponent:this._intervalComponent,activeTrigger:C,automation:g,board:this.board,yaml:this.yaml,disabled:x,showAdvanced:this._showAdvanced,focusFieldPath:tu(S),onValueChange:this._onTriggerParamsValueChange,onAdvancedToggle:this._onAdvancedToggle}).location,n=a.intervalComponent,l=a.activeTrigger,0===(m=r?.kind==="interval"?n?n.config_entries.filter(e=>"then"!==e.key):[]:l?.config_entries??[]).length?s.s6:(0,s.qy)`
    <esphome-config-entry-form
      .entries=${m}
      .values=${a.automation.trigger_params}
      .board=${a.board}
      .yaml=${a.yaml}
      .focusFieldPath=${a.focusFieldPath}
      ?disabled=${a.disabled}
      advanced-section
      ?show-advanced=${a.showAdvanced}
      @value-change=${a.onValueChange}
      @advanced-toggle=${a.onAdvancedToggle}
    ></esphome-config-entry-form>
  `}`}
        ${iv({automation:g,catalog:$,conditionCatalog:k,scripts:b,devices:y,board:this.board,yaml:this.yaml,disabled:x,localize:this._localize,focusTarget:tp(S),descriptionKey:"device.automation_actions_description",onActionsChange:this._onActionsChange})}
        ${this.renderFooter({label:this._localize("device.delete_automation"),message:()=>this._localize("device.confirm_delete_automation",{name:this._deleteTargetName(C)})})}
      `)}_deleteTargetName(e){let t=this.location;return e||t?.kind!=="device_on"&&t?.kind!=="component_on"?iz(t,e,this._localize):t.trigger}static get _actionStyles(){return null}get _devicesForTest(){return this._available?.devices??[]}get _scriptsForTest(){return this._available?.scripts??[]}constructor(...e){super(...e),this._intervalComponent=null,this._parseSubstitutions=(0,d.A)(iC.Gr),this._onTriggerParamsValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,o=this.value??(0,_.rN)(),a=(0,_.aG)(o.trigger_params,t,i);this._engine.withValue({trigger_params:a})},this._onTargetChange=e=>{e.stopPropagation(),this.location=e.detail.target,this._engine.withValue({trigger_id:null,trigger_params:{}})},this._onTriggerChange=e=>{if(e.stopPropagation(),this._engine.withValue({trigger_id:e.detail.triggerId,trigger_params:e.detail.params}),this.location?.kind==="device_on")this.location={...this.location,trigger:e.detail.triggerId};else if(this.location?.kind==="component_on"){let t=(0,iS.y1)(e.detail.triggerId);this.location={...this.location,trigger:t}}},this._onTriggerParamsChange=e=>{e.stopPropagation(),this._engine.withValue({trigger_params:e.detail.params})}}}function iD(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}iE([(0,r.wk)()],iT.prototype,"_intervalComponent",void 0),iT=iE([(0,r.EM)("esphome-automation-editor")],iT),(0,I.C)({"open-in-new":a.mdiOpenInNew,"script-text-outline":a.mdiScriptTextOutline});class iO extends tG{willUpdate(e){super.willUpdate(e);let t=this._currentFocus(),i=tm(t);i!==this._paramsRevealKey&&(this._paramsRevealKey=i,null!==t_(t,"parameters")&&(this._showAdvanced=!0))}_canApply(e){return"script"===e.kind&&!!e.id}async _load(){await super._load(),this._loadScriptComponent()}async _loadScriptComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,iF.CQ)("script",e,t);if(i){this._scriptComponent=i;return}try{let i=await (0,iF.Sn)(this._api,"script",e,t);i&&(this._scriptComponent=i)}catch{}}render(){let e=this.renderStateGate();if(e)return e;let t=this.value??(0,_.rN)(),i=this._available?.devices??[],o=this._available?.scripts??[],a=this._available?.actions??[],r=this._available?.conditions??[],n=this._engine.deleting,l=this._currentFocus();return(0,tr.D)(this._target,(0,s.qy)`
        ${this._renderHeader()}
        ${this._renderNameField({label:this._localize("device.script_id_label"),description:this._localize("device.script_id_description"),value:this.location?.id??""},n)}
        ${this._renderConfigForm(t,n,l)}
        ${this._showAdvanced?this._renderParametersField(t,n,l):s.s6}
        ${iv({automation:t,catalog:a,conditionCatalog:r,scripts:o,devices:i,board:this.board,yaml:this.yaml,disabled:n,localize:this._localize,focusTarget:tp(l),descriptionKey:"device.script_actions_description",onActionsChange:this._onActionsChange})}
        ${this.renderFooter({label:this._localize("device.delete_script"),message:e=>this._localize("device.confirm_delete_script",{name:e.id})})}
      `)}_renderHeader(){let e=this._scriptComponent,t=e?.name??this._localize("device.script_header_title_static"),i=e?.description??this._localize("device.script_header_description"),o=e?.docs_url??`${tn.Ik}/components/script.html`,a=e?.image_url??"";return(0,s.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${t}</h2>
        <a class="ae-header-docs" href=${o} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">${(0,ej.Gc)(i)}</p>
      </div>
      <div class="ae-header-icon">
        ${a?(0,s.qy)`<img alt="" src=${a} />`:(0,s.qy)`<wa-icon library="mdi" name="script-text-outline"></wa-icon>`}
      </div>
    </div>`}_renderConfigForm(e,t,i){let o=this._scriptComponent;if(!o)return s.s6;let a=o.config_entries.filter(e=>"id"!==e.key&&"parameters"!==e.key&&"then"!==e.key),r=this._hasParametersEntry();return 0!==a.length||r?(0,s.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${e.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        .focusFieldPath=${null===t_(i,"parameters")?tu(i):void 0}
        ?disabled=${t}
        advanced-section
        ?force-advanced-control=${r}
        .advancedExtraCount=${+!!r}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onConfigFormValueChange}
        @advanced-toggle=${this._onAdvancedToggle}
      ></esphome-config-entry-form>
    `:s.s6}_hasParametersEntry(){return this._scriptComponent?.config_entries.some(e=>"parameters"===e.key)??!1}_renderParametersField(e,t,i){let o=e.trigger_params.parameters??{};return(0,s.qy)`<esphome-callable-params-editor
      .value=${o}
      .focusParam=${t_(i,"parameters")}
      ?disabled=${t}
      .fieldLabel=${this._localize("device.automation_script_parameters")}
      .description=${this._localize("device.script_parameters_description")}
      .addLabel=${this._localize("device.script_add_parameter")}
      .namePlaceholder=${this._localize("device.script_parameter_name_placeholder")}
      @value-change=${this._onParametersChange}
    ></esphome-callable-params-editor>`}constructor(...e){super(...e),this._scriptComponent=null,this._nameInputId="script-id",this._nameYamlKeys=["id"],this._onConfigFormValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,o=this.value??(0,_.rN)(),a=(0,_.aG)(o.trigger_params,t,i);this._engine.withValue({trigger_params:a})},this._onParametersChange=e=>{e.stopPropagation();let t=this.value??(0,_.rN)();this._engine.withValue({trigger_params:{...t.trigger_params,parameters:e.detail.value}})}}}iD([(0,r.wk)()],iO.prototype,"_scriptComponent",void 0),iO=iD([(0,r.EM)("esphome-script-editor")],iO),i(2547);var iU=i(1262),iB=i(2919),iZ=i(6049),iI=i(7297);let iK=new Set(["external_components","packages"]),ij=(0,s.AH)`
  :host {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    /* No top margin: the shared .editor-pane padding already supplies the top
       gap. The extra margin pushed the structured editor below the YAML pane
       (#826); the automation/script editors never had it. */
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
`;var iV=i(565),iY=i(5795),iN=i(8175),iG=i(5490),iH=i(4008);function iW(e){let t=typeof e;return"string"===t||"number"===t||"boolean"===t||"bigint"===t}function iJ(e,t){let i=null;for(let o of t){if(o.type!==iH.Hh.NESTED)continue;let t=e[o.key];if(null==t)continue;let[a,s]=function(e,t){let i=e.maybe_key??null,o=e.config_entries??[];if(!e.multi_value)return iX(t,i,o);if(Array.isArray(t)){let e=null;return t.forEach((a,s)=>{let[r,n]=iX(a,i,o);r&&((e??=[...t])[s]=n)}),e?[!0,e]:[!1,t]}if(i&&(iW(t)||(0,iN.ex)(t))){let[,e]=iX(t,i,o);return[!0,[e]]}return[!1,t]}(o,t);a&&((i??=Object.create(Object.getPrototypeOf(e),Object.getOwnPropertyDescriptors(e)))[o.key]=s)}return i?[!0,i]:[!1,e]}function iX(e,t,i){return t&&iW(e)?[!0,{[t]:e}]:(0,iN.ex)(e)?iJ(e,i):[!1,e]}function iQ(e,t,i){let o=(0,u.uv)(i,e.sectionKey,e.fromLine),a=(0,et.wz)(i,e.sectionKey,o);e._values=function(e,t){let[i,o]=iJ(e,t);return i?o:e}((0,iG.Dq)(a,t.entries),t.entries),e._resolvedFromLine=o,e._presentComponents=(0,ei.Zn)(i),e._valuesStale=!1}async function i0(e){let t=++e._loadId;e._loading=!0,e._error="",e._setDirty(!1),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),e._lastSelfWrittenYaml=null;try{let i=e.board?.esphome.platform,o=await (0,iF.Sn)(e._api,e.sectionKey,i);if(t!==e._loadId)return;let a=e.yaml;if(o)e._config={section_key:e.sectionKey,section_type:"core",title:o.name,description:o.description,docs_url:o.docs_url??"",icon:"",image_url:o.image_url??"",entries:o.config_entries,required_groups:o.required_groups??[]},e._isPlatformDomain=!1,e._isUnknown=!1;else{let i=(0,X.Po)(await (0,J.ak)(e._api)).has(e.sectionKey);if(t!==e._loadId)return;e._config={section_key:e.sectionKey,section_type:"core",title:e.sectionKey,description:"",docs_url:"",icon:"",image_url:"",entries:[],required_groups:[]},e._isPlatformDomain=i,e._isUnknown=!i}a!==e._lastSelfWrittenYaml&&e._valuesRead++,iQ(e,e._config,a)}catch(o){if(t!==e._loadId)return;e._config=null,e._values={};let i=o instanceof Error?o.message:"";e._error=i.includes("timed out")?e._localize("device.load_config_error"):i||e._localize("device.load_config_error")}finally{t===e._loadId&&(e._loading=!1,e._reloading=!1)}}function i1(e){if(e._draftTimer=null,!e._config)return null;i2(e);let t=(0,u.uv)(e.yaml,e.sectionKey,e.fromLine);if(void 0===t)return e._setDirty(!1),null;let i=(0,p.Nj)(e.yaml,e.sectionKey,e._values,t,{keepEmptyStrings:iZ.fq.has(e.sectionKey)});return i3(e,i)}function i2(e){e._config&&(e._fieldErrors=(0,iV.JK)((0,iZ.a7)(e.sectionKey,e._config.entries),e._values,e._effectivePresentComponents,e.board?.esphome.platform??null,e.sectionKey))}function i3(e,t){return(e._setDirty(!1),t===e.yaml)?null:(e._lastSelfWrittenYaml=t,(0,tq.IL)(e,"yaml-draft",{configuration:e.configuration,yaml:t,basedOn:e.yaml,node:e}),t)}function i6(e,t){if(!(e._valuesStale&&e._config&&(iQ(e,e._config,e.yaml),1)))return t;let i=t.filter(({path:t})=>!(0,iN.rD)(e._values,t));return i.length!==t.length&&e._valuesRead++,i}function i5(e){return null!==e._draftTimer?(clearTimeout(e._draftTimer),i1(e)??e.yaml):e.yaml}var i4=i(615),i9=i(5217);async function i8(e=4){let t=Math.max(1,Math.trunc(e)),{PASSPHRASE_WORDS:o}=await i.e(820).then(i.bind(i,2503)),a=o.length,s=Math.floor(0x100000000/a)*a,r=new Uint32Array(1),n=[];for(;n.length<t;)crypto.getRandomValues(r),r[0]>=s||n.push(o[r[0]%a]);return n.join("-")}var i7=i(7967),oe=i(7228);function ot(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"lock-alert":a.mdiLockAlert});let oi=()=>i8(),oo={api:{secretSection:"api",markers:["encryption"],copyPrefix:"api_encryption",fields:[{path:["encryption","key"],generate:i4.My,secretField:"key"}]},"ota.esphome":{secretSection:"ota.esphome",markers:["password","encryption"],copyPrefix:"ota_password",fields:[{path:["password"],generate:oi,secretField:"password"}],suppressWhen:e=>null!==tt(e)},web_server:{secretSection:"web_server",markers:["auth"],copyPrefix:"web_auth",fields:[{path:["auth","username"],generate:()=>i8(1)},{path:["auth","password"],generate:oi,secretField:"password"}]}},oa=e=>Object.prototype.hasOwnProperty.call(oo,e);class os extends s.WF{get _setting(){return oa(this.sectionKey)?oo[this.sectionKey]:void 0}willUpdate(e){let t=e.has("yaml")||e.has("fromLine")||e.has("sectionKey"),i=this._devices.find(e=>e.configuration===this.configuration),o=i!==this._device||e.has("_esphomeVersion")||e.has("configuration");this._device=i,(t||o&&this._setting?.suppressWhen)&&(this._markerAbsent=!!this._setting&&!this._markerPresent()&&!this._suppressed())}_resolvedFields(){let e=this._setting;if(!e)return[];let t=(0,i9.k)(this._devices,this.configuration);return e.fields.map(i=>({field:i,key:i.secretField?(0,i7.WA)(e.secretSection,i.secretField,t,!0)[0]??"":""}))}get _ready(){let e=this._resolvedFields();return e.length>0&&e.every(e=>!e.field.secretField||""!==e.key)}_markerPresent(){let e=this._setting;if(!e)return!1;let t=this.sectionKey.split(".")[0],i=RegExp(`^(?:${e.markers.join("|")})\\s*:`);return(0,et.zZ)((0,h.D)(this.yaml),t,i,this.fromLine)>=0}_suppressed(){let e=this._setting?.suppressWhen;return!!e&&e({device:this._device,yaml:this.yaml,esphomeVersion:this._esphomeVersion})}render(){let e=this._setting;return e&&this._markerAbsent?(0,s.qy)`
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
    `:s.s6}_renderDialogBody(e){let[t,i=""]=this._localize(`device.${e.copyPrefix}_dialog_body`).split("{key}"),o=this._resolvedFields().filter(e=>e.field.secretField).map((e,t)=>(0,s.qy)`${t>0?", ":""}<code>${e.key}</code>`);return(0,s.qy)`${t}${o}${i}`}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._esphomeVersion="",this.sectionKey="",this.yaml="",this.configuration="",this._markerAbsent=!1,this._generating=!1,this._onCta=()=>{this._ready&&this._dialog?.open()},this._onGenerate=async()=>{let e=this._setting,t=this._resolvedFields();if(!this._generating&&this._api&&e&&this._ready){this._generating=!0;try{let e=[];for(let{field:i,key:o}of t){let t=await i.generate();i.secretField?(await (0,oe.j)(this._api,o,t),e.push({path:i.path,value:`!secret ${o}`})):e.push({path:i.path,value:t})}this.dispatchEvent(new CustomEvent("apply-section-values",{detail:{changes:e},bubbles:!0,composed:!0})),(0,B.VX)(this._localize("device.security_applied"))}catch(t){console.error("Security secret generation failed",t),(0,B.UG)(this._localize(`device.${e.copyPrefix}_error`))}finally{this._generating=!1}}}}}os.styles=[M.G9,eH,(0,s.AH)`
      .dialog-body code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
        padding: 1px 5px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
        word-break: break-all;
      }
    `],ot([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],os.prototype,"_localize",void 0),ot([(0,o.Fg)({context:P.Ie,subscribe:!0}),(0,r.wk)()],os.prototype,"_api",void 0),ot([(0,o.Fg)({context:P.xJ,subscribe:!0}),(0,r.wk)()],os.prototype,"_devices",void 0),ot([(0,o.Fg)({context:P.wo,subscribe:!0}),(0,r.wk)()],os.prototype,"_esphomeVersion",void 0),ot([(0,r.MZ)()],os.prototype,"sectionKey",void 0),ot([(0,r.MZ)()],os.prototype,"yaml",void 0),ot([(0,r.MZ)()],os.prototype,"configuration",void 0),ot([(0,r.MZ)({type:Number})],os.prototype,"fromLine",void 0),ot([(0,r.wk)()],os.prototype,"_markerAbsent",void 0),ot([(0,r.wk)()],os.prototype,"_generating",void 0),ot([(0,r.P)("esphome-confirm-dialog")],os.prototype,"_dialog",void 0),os=ot([(0,r.EM)("esphome-security-notice")],os);let or=(0,s.AH)`
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
`;function on(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({plus:a.mdiPlus,pencil:a.mdiPencil,delete:a.mdiDelete});class ol extends s.WF{render(){if(0===this.rows.length&&void 0===this.addLabel)return s.s6;let e=""!==this.busyKey;return(0,s.qy)`<div class="list">
      <div class="header">
        <h4 class="title">${this.heading}</h4>
        ${void 0!==this.addLabel?(0,s.qy)`<button type="button" class="add" @click=${this._onAdd}>
                <wa-icon library="mdi" name="plus"></wa-icon>
                ${this.addLabel}
              </button>`:s.s6}
      </div>
      ${0===this.rows.length?void 0!==this.emptyText?(0,s.qy)`<p class="empty-message--dashed" role="status">${this.emptyText}</p>`:s.s6:(0,s.qy)`<ul class="rows">
              ${this.rows.map(t=>(0,s.qy)`<li class="row">
                    <span class="name truncate">${t.label}</span>
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
    </div>`}_emit(e,t){(0,e$.r)(this,e,{key:t})}constructor(...e){super(...e),this.heading="",this.rows=[],this.busyKey="",this.editLabel="",this.deleteLabel="",this._onAdd=()=>{(0,e$.r)(this,"add")}}}function od(e){if("api"!==e._renderedKey)return s.s6;let t=(0,u.vB)(e.yaml).filter(e=>e.key.startsWith("automation:api_action:")).map(e=>({key:e.key,label:e.id??""}));return(0,s.qy)`<esphome-section-automation-list
    .heading=${e._localize("device.api_actions_list_title")}
    .rows=${t}
    add-label=${e._localize("device.add_api_action")}
    empty-text=${e._localize("device.api_actions_list_empty")}
    edit-label=${e._localize("device.api_actions_list_edit")}
    delete-label=${e._localize("device.api_actions_list_delete")}
    busy-key=${e._deletingRow}
    @add=${e._onOpenAddApiAction}
    @edit=${e._onEditRow}
    @delete=${e._onDeleteRow}
  ></esphome-section-automation-list>`}function oc(e){var t,i;let o=e._shortcutTarget();if(null===o)return s.s6;let a=(t=(0,u.vB)(e.yaml),i=t=>{var i,o;let a;return i=e,a=(o=t).displayLabel||o.eventKey||"",o.eventKey?i._triggerCatalog.resolveName((0,iS.yZ)(o.parentKey??"esphome",o.hostPlatform),o.eventKey,a):a},t.filter(e=>!!e.eventKey&&("device_on"===o.kind?"esphome"===e.parentKey:e.id===o.componentId||e.parentComponentId===o.componentId)).map(e=>({key:e.key,label:void 0!==e.parentComponentId?`${e.name??e.id} → ${i(e)}`:i(e)}))),r="device_on"===o.kind?e._localize("device.automations_list_title_device"):e._localize("device.automations_list_title");return(0,s.qy)`<esphome-section-automation-list
    .heading=${r}
    .rows=${a}
    add-label=${e._localize("device.add_automation")}
    empty-text=${e._localize("device.automations_list_empty")}
    edit-label=${e._localize("device.automations_list_edit")}
    delete-label=${e._localize("device.automations_list_delete")}
    busy-key=${e._deletingRow}
    @add=${e._onOpenAddAutomation}
    @edit=${e._onEditRow}
    @delete=${e._onDeleteRow}
  ></esphome-section-automation-list>`}function oh(e){return(0,s.qy)`<div class="yaml-only-notice" role="note">
    <wa-icon library="mdi" name="information-outline"></wa-icon>
    <div class="yaml-only-notice-body">${e}</div>
  </div>`}function op(e,t){return t?(0,s.qy)`<div class="actions">
    <button
      class="delete-button"
      ?disabled=${e._deleting}
      @click=${()=>e._confirmDialog?.open()}
    >
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${e._localize("device.delete_section")}
    </button>
  </div>`:s.s6}ol.styles=[M.G9,tR.Z,ew.U,or],on([(0,r.MZ)()],ol.prototype,"heading",void 0),on([(0,r.MZ)({attribute:!1})],ol.prototype,"rows",void 0),on([(0,r.MZ)({attribute:"add-label"})],ol.prototype,"addLabel",void 0),on([(0,r.MZ)({attribute:"empty-text"})],ol.prototype,"emptyText",void 0),on([(0,r.MZ)({attribute:"busy-key"})],ol.prototype,"busyKey",void 0),on([(0,r.MZ)({attribute:"edit-label"})],ol.prototype,"editLabel",void 0),on([(0,r.MZ)({attribute:"delete-label"})],ol.prototype,"deleteLabel",void 0),ol=on([(0,r.EM)("esphome-section-automation-list")],ol);var ou=i(5865);function o_(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({close:a.mdiClose});class om extends s.WF{open(){this._name="",this._error="",this._dialog.open=!0}render(){let e=this.boardName?this._localize("device.add_api_action_dialog_title",{name:this.boardName}):this._localize("device.add_api_action");return(0,s.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,ej.Gc)(this._localize("device.api_action_header_description"))}
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
          @input=${e=>{this._name=(0,ig.e)(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,s.qy)`<p class="error" role="alert">${this._error}</p>`:s.s6}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._name&&!(0,u.vB)(this.yaml).some(e=>e.key===`automation:api_action:${this._name}`)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new eQ.T(this),this._name="",this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"api_action",action_name:this._name},t=this.configuration,i=this.yaml,{yaml_diff:o}=await this._api.upsertAutomation(t,{trigger_id:null,trigger_params:{},actions:[]},e,i),a=(0,_.lX)(i,o);(0,tq.IL)(this,"yaml-draft",{configuration:t,yaml:a,basedOn:i,node:this}),this.dispatchEvent(new CustomEvent("automation-added",{detail:{configuration:t,sectionKey:(0,_.Ks)(e)},bubbles:!0,composed:!0})),this._dialog.open=!1}catch(t){let e=(0,tS.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,B.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}om.styles=[M.G9,tC.z9,ou.h,(0,s.AH)`
      esphome-base-dialog {
        --width: 480px;
      }
      esphome-base-dialog::part(body) {
        padding: var(--wa-space-l);
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
    `],o_([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],om.prototype,"_localize",void 0),o_([(0,o.Fg)({context:P.Ie})],om.prototype,"_api",void 0),o_([(0,r.MZ)()],om.prototype,"boardName",void 0),o_([(0,r.MZ)()],om.prototype,"configuration",void 0),o_([(0,r.MZ)()],om.prototype,"yaml",void 0),o_([(0,r.MZ)({attribute:!1})],om.prototype,"board",void 0),o_([(0,r.wk)()],om.prototype,"_name",void 0),o_([(0,r.wk)()],om.prototype,"_saving",void 0),o_([(0,r.wk)()],om.prototype,"_error",void 0),om=o_([(0,r.EM)("esphome-add-api-action-dialog")],om),i(1752);var ov=i(6185),og=i(3508);function of(e,t){if(e._showAdvanced||!e._config||e._autoRevealedSections.has(e._renderedKey))return;let i=(0,iZ.a7)(e._renderedKey,e._config.entries),o=(0,og._r)(i,e._config.required_groups??[],e._values);t.some(t=>(0,ov.WG)(i,t,e._values,o))&&(e._autoRevealedSections.add(e._renderedKey),e._setShowAdvanced(!0))}let oy=new Set(["api","script","interval","external_components","packages","substitutions","globals","dashboard_import"]);function ob(e,t,i){let o=(0,u.MT)(e),a=o.filter(e=>(0,u.gU)(e)===t);return 0===a.length?null:{sections:o,match:void 0!==i?a.find(e=>e.fromLine===i)??a[0]:a[0]}}function ow(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"alert-circle-outline":a.mdiAlertCircleOutline,delete:a.mdiDelete,"information-outline":a.mdiInformationOutline,"open-in-new":a.mdiOpenInNew,pencil:a.mdiPencil,"plus-circle-outline":a.mdiPlusCircleOutline});let o$=new Set(["esphome"]);class ok extends s.WF{get _effectivePresentComponents(){return this._widenPresence(this._presentComponents,this.yaml,this._resolvedComponents)}get _renderedKey(){return this._config?.section_key??this.sectionKey}get _focusTarget(){return this._reloading?void 0:this.focusFieldPath}get _showAdvanced(){return this._advancedShownSections.has(this._renderedKey)}_setShowAdvanced(e){let t=new Set(this._advancedShownSections);e?t.add(this._renderedKey):t.delete(this._renderedKey),this._advancedShownSections=t}willUpdate(e){e.has("backendErrors")&&this._clearedBackendPaths.size&&(this._clearedBackendPaths=new Set),e.has("_resolvedComponents")&&this._config&&!this._reloading&&this._fieldErrors.size&&i2(this),e.has("yaml")&&this.yaml!==this._lastSelfWrittenYaml&&(this._valuesRead++,this._valuesStale=null===this._draftTimer),(e.has("sectionKey")||e.has("configuration")||e.has("fromLine"))&&this.sectionKey&&this.configuration&&(this._reloading=null!==this._config,i0(this)),this._revealAdvancedForFocus(e),this._revealAdvancedForErrors(e),tF(this,this._reloading)}_revealAdvancedForErrors(e){(e.has("backendErrors")||e.has("_config"))&&!this._reloading&&this.backendErrors.fields.size&&of(this,[...this.backendErrors.fields.keys()].map(e=>e.split(".")))}_revealAdvancedForFocus(e){!function(e,t){if(!t.has("focusFieldPath")&&!t.has("_config"))return;let i=e._focusTarget;i?.length&&of(e,[i])}(this,e)}updated(){this._triggerCatalog.ensure(),function(e){if("api"!==e._renderedKey)return;let t=e._focusTarget,i=t?.[0];if(!td.i.some(e=>e===i))return;let o=JSON.stringify(t);if(o===e._apiListFlashKey)return;let a=e.shadowRoot?.querySelector("esphome-section-automation-list");a&&(e._apiListFlashKey=o,(0,tx.uJ)(a))}(this)}connectedCallback(){super.connectedCallback(),this._announceUnmount=(0,tq.y5)(this)}disconnectedCallback(){super.disconnectedCallback(),this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null),this._announceUnmount?.(),this._announceUnmount=null}flushPending(){i5(this)}reload(){this.sectionKey&&this.configuration&&null===this._draftTimer&&this.yaml!==this._lastSelfWrittenYaml&&i0(this)}get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,(0,tq.IL)(this,"dirty-change",{dirty:e,node:this}))}_scheduleDraftFlush(){this._draftTimer&&clearTimeout(this._draftTimer),this._draftTimer=setTimeout(()=>i1(this),ok.DRAFT_DEBOUNCE_MS)}_onShowYamlEditor(){(0,e$.r)(this,"show-yaml-editor")}_onAddPlatform(){(0,e$.r)(this,"request-add-component",{domain:this.sectionKey})}render(){var e,t;let i,o,a,r,n,l,d,c;if(this._loading&&!this._config)return(0,s.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`;if(this._error&&!this._config)return(0,s.qy)`<p class="error">${this._error}</p>`;if(!this._config)return s.s6;let h=this._config,p=(0,iZ.a7)(h.section_key,h.entries),_=(e=h.section_key,t=p.length,iK.has(e)||0===t),m=[...this.yamlPaneVisible?[]:this.backendErrors.sectionMessages,..._?this.backendErrors.fieldMessages:[]],v=!o$.has(h.section_key);return(0,s.qy)`
      ${o=(i=this._isUnknown||this._isPlatformDomain)?null:(0,iY.lb)(this.board,h.section_key,this._values.id),a=this._isUnknown?this._localize("device.external_component_title"):this._isPlatformDomain?this._localize("device.platform_section_title"):h.title,r=o?.description??h.description,n=o?.image_url||h.image_url,l=o?(0,iY.mU)(o,h.title):null,d=i?h.section_key:l!==h.title?l:null,(0,s.qy)`
    <div class="section-header">
      <div class="section-header-info">
        <div class="section-header-title-row">
          <h3 class="section-title">${a}</h3>
          ${(0,ej.RQ)(h.docs_url)?(0,s.qy)`<a
                  class="docs-link"
                  href=${h.docs_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ${this._localize("device.docs")}
                  <wa-icon library="mdi" name="open-in-new"></wa-icon>
                </a>`:s.s6}
        </div>
        ${d?(0,s.qy)`<p class="section-subtitle">${d}</p>`:s.s6}
        ${r?(0,s.qy)`<p class="section-desc">${(0,ej.Gc)(r)}</p>`:s.s6}
      </div>
      ${i?s.s6:(0,s.qy)`<div class="section-image">
              <img
                src=${n||(0,eK.uG)()}
                alt=${a}
                referrerpolicy="no-referrer"
                @error=${eK.jt}
              />
            </div>`}
    </div>
    ${m.length>0?(0,s.qy)`<div class="danger-banner section-error-banner" role="alert">
            <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
            <div class="danger-banner-text">
              ${m.map(e=>(0,s.qy)`<p>${e}</p>`)}
            </div>
          </div>`:s.s6}
  `}
      ${this._isPlatformDomain?(0,s.qy)`${oh((0,s.qy)`
    <p>
      ${this._localize("device.platform_domain_section",{key:this._renderedKey})}
    </p>
    <button type="button" class="yaml-only-notice-cta" @click=${this._onAddPlatform}>
      ${this._localize("device.id_reference_add",{domain:this._renderedKey})}
    </button>
  `)}
  ${op(this,v)}`:_?(0,s.qy)`${oh((0,s.qy)`
    <p>${this._localize("device.yaml_only_section")}</p>
    ${this.yamlPaneVisible?s.s6:(0,s.qy)`<button
            type="button"
            class="yaml-only-notice-cta"
            @click=${this._onShowYamlEditor}
          >
            ${this._localize("device.show_yaml_editor")}
          </button>`}
  `)}
  ${od(this)} ${oc(this)}
  ${function(e){var t,i;let o=e._resolveComponentId();if(null===o)return s.s6;let a=(t=(0,u.vB)(e.yaml),i=t=>(0,ix.t)(t,e._localize),t.filter(e=>void 0!==e.actionField&&e.id===o).map(e=>({key:e.key,label:i(e.actionField)})));return(0,s.qy)`<esphome-section-automation-list
    .heading=${e._localize("device.action_fields_list_title")}
    .rows=${a}
    edit-label=${e._localize("device.action_fields_list_edit")}
    delete-label=${e._localize("device.action_fields_list_delete")}
    busy-key=${e._deletingRow}
    @edit=${e._onEditRow}
    @delete=${e._onDeleteRow}
  ></esphome-section-automation-list>`}(this)} ${op(this,v)}`:(c=(0,iZ.a7)(h.section_key,h.entries),(0,s.qy)`
    ${oa(h.section_key)?(0,s.qy)`<esphome-security-notice
            .sectionKey=${h.section_key}
            .yaml=${this.yaml}
            .configuration=${this.configuration}
            .fromLine=${this._resolvedFromLine}
            @apply-section-values=${this._onApplySectionValues}
          ></esphome-security-notice>`:s.s6}
    <esphome-config-entry-form
      .entries=${c}
      .requiredGroups=${h.required_groups}
      .values=${this._values}
      .errors=${this._mergeErrors(this.backendErrors.fields,this._clearedBackendPaths,this._fieldErrors)}
      .board=${this.board}
      .yaml=${this.yaml}
      .fromLine=${this._resolvedFromLine}
      .sectionKey=${h.section_key}
      .configuration=${this.configuration}
      .focusFieldPath=${this._focusTarget}
      .presentComponents=${this._effectivePresentComponents}
      advanced-section
      gate-advanced
      ?show-advanced=${this._showAdvanced}
      @value-change=${this._onValueChange}
      @advanced-toggle=${this._onAdvancedToggle}
      @edit-action-field=${this._onEditActionField}
    ></esphome-config-entry-form>
    ${this._error?(0,s.qy)`<p class="error">${this._error}</p>`:s.s6}
    ${od(this)} ${oc(this)}
    ${op(this,v)}
  `)}
      ${"api"!==this._renderedKey?s.s6:(0,s.qy)`<esphome-add-api-action-dialog
    .boardName=${this.boardName}
    .configuration=${this.configuration}
    .board=${this.board}
    .yaml=${this.yaml}
    @automation-added=${this._onApiActionAdded}
  ></esphome-add-api-action-dialog>`} ${null===this._shortcutTarget()?s.s6:(0,s.qy)`<esphome-add-automation-dialog
    .boardName=${this.boardName}
    .configuration=${this.configuration}
    .board=${this.board}
    .yaml=${this.yaml}
    @automation-added=${this._onAutomationAdded}
  ></esphome-add-automation-dialog>`}
      ${!v?s.s6:(0,s.qy)`<esphome-confirm-dialog
    heading=${this._localize("device.delete_section")}
    confirm-label=${this._localize("device.delete_section")}
    message=${this._localize("device.confirm_delete_section",{name:h.title})}
    destructive
    @confirm=${this._onDeleteConfirmed}
  ></esphome-confirm-dialog>`}
    `}_shortcutTarget(){return function(e,t,i,o){if(oy.has(t))return null;if("esphome"===t)return{kind:"device_on"};let a=ob(e,t,i);if(null===a)return null;let{match:s}=a;return o((0,iS.yZ)(s.parentKey??s.key,s.platform))?{kind:"component_on",componentId:(0,u.MX)(a.sections,a.match)}:null}(this.yaml,this._renderedKey,this._resolvedFromLine,e=>this._triggerCatalog.hasTriggersFor(e))}_resolveComponentId(){var e;let t;return e=this.yaml,null===(t=ob(e,this._renderedKey,this._resolvedFromLine))?null:(0,u.MX)(t.sections,t.match)}constructor(...e){super(...e),this._localize=e=>e,this._resolvedComponents=[],this.configuration="",this.sectionKey="",this.backendErrors=L.eV,this.yaml="",this.yamlPaneVisible=!0,this.board=null,this.boardName="",this._config=null,this._values={},this._loading=!1,this._dirty=!1,this._error="",this._deletingRow="",this._isUnknown=!1,this._isPlatformDomain=!1,this._fieldErrors=new Map,this._clearedBackendPaths=new Set,this._advancedShownSections=new Set,this._presentComponents=new Set,this._widenPresence=(0,d.A)(iB.H),this._autoRevealedSections=new Set,this._deleting=!1,this._loadId=0,this._valuesRead=0,this._valuesStale=!1,this._reloading=!1,this._draftTimer=null,this._announceUnmount=null,this._lastSelfWrittenYaml=null,this._triggerCatalog=new iI.Q(this,()=>({api:this._api,platform:this.board?.esphome.platform||void 0,boardId:this.board?.id})),this._mergeErrors=(0,d.A)((e,t,i)=>{if(0===e.size)return i;let o=new Map;for(let[i,a]of e)t.has(i)||o.set(i,a);if(0===o.size)return i;for(let[e,t]of i)o.set(e,t);return o}),this._onAdvancedToggle=e=>{this._setShowAdvanced(e.detail.show)},this.lastFlushFailed=!1,this._onValueChange=e=>(function(e,t){if(e._reloading||!i6(e,[t.detail]).length)return;let{path:i,value:o}=t.detail;e._values=(0,iN.Oe)(e._values,i,o),e._setDirty(!0);let a=i.join("."),s=(0,iV.iL)(e._fieldErrors,a);s&&(e._fieldErrors=s);let r=`${a}.`,n=null;for(let t of e.backendErrors.fields.keys())(t===a||t.startsWith(r))&&!e._clearedBackendPaths.has(t)&&(n??=new Set(e._clearedBackendPaths)).add(t);n&&(e._clearedBackendPaths=n),e._scheduleDraftFlush()})(this,e),this._onDeleteConfirmed=()=>(async function(e){if(!e._config||e._reloading)return;let t=i5(e),i=(0,u.uv)(t,e.sectionKey,e.fromLine);if(void 0===i){e._error=e._localize("device.section_delete_error");return}e._deleting=!0,e._error="";let o=e._config.title,a=(0,tq.fb)(e,"yaml-updated"),s=e.sectionKey,r=e.configuration;try{let n=(0,p.ju)(t,e.sectionKey,i);if(n===t){e._error=e._localize("device.section_delete_error");return}await e._api.updateConfig(r,n),e._setDirty(!1),a(e.isConnected,{configuration:r,yaml:n,basedOn:t,removed:{kind:"component",sectionKey:s,fromLine:i}}),e.isConnected&&e.sectionKey===s&&(0,e$.r)(e,"section-select",{sectionKey:null}),(0,B.VX)(e._localize("device.section_deleted",{name:o}))}catch(i){let t=(0,tS.K)(i,e._localize,"device.section_delete_error");e._error=t,(0,B.UG)(e._localize("device.section_delete_error"),{description:t})}finally{e._deleting=!1}})(this),this._onApplySectionValues=e=>(function(e,t){var i;if(e._reloading)return;let o=i6(e,t);if(!o.length)return;for(let{path:t,value:i}of o)e._values=(0,iN.Oe)(e._values,t,i);e._setDirty(!0),null!==e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null);let a=!(0,iY.K8)(e.sectionKey)&&!iZ.sU.has(e.sectionKey)&&!e._isPlatformDomain;void 0===(0,u.uv)(e.yaml,e.sectionKey,e.fromLine)&&a?(i2(i=e),i3(i,(0,p.Kd)(i.yaml,i.sectionKey,i._values,{keepEmptyStrings:iZ.fq.has(i.sectionKey)}))):i1(e)})(this,e.detail.changes),this._onOpenAddApiAction=()=>{this._addApiActionDialog?.open()},this._onApiActionAdded=e=>{(e.stopPropagation(),e.detail.configuration!==this.configuration)?console.warn("Dropped automation-added for",e.detail.configuration,"while showing",this.configuration):(0,e$.r)(this,"section-select",{sectionKey:e.detail.sectionKey})},this._onEditRow=e=>{e.stopPropagation(),(0,e$.r)(this,"section-select",{sectionKey:e.detail.key})},this._onDeleteRow=async e=>{e.stopPropagation();let t=e.detail.key,i=(0,_.ac)(t);if(!this._api||!i||this._deletingRow)return;this._deletingRow=t;let o=(0,tq.fb)(this,"yaml-updated");try{let e=this.configuration,t=i5(this);await m(this._api,e,i,t,o,()=>this.isConnected)}catch(t){let e=(0,tS.K)(t,this._localize,"device.automation_save_error");(0,B.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._deletingRow=""}},this._onOpenAddAutomation=()=>{let e=this._shortcutTarget();null!==e&&("device_on"===e.kind?this._addAutomationDialog?.open({kind:"device_on"}):this._addAutomationDialog?.open({kind:"component_on",componentId:e.componentId}))},this._onAutomationAdded=e=>{(e.stopPropagation(),e.detail.configuration!==this.configuration)?console.warn("Dropped automation-added for",e.detail.configuration,"while showing",this.configuration):(0,e$.r)(this,"section-select",{sectionKey:e.detail.sectionKey})},this._onEditActionField=e=>{e.stopPropagation();let t=this._resolveComponentId();if(null===t)return;let i=(0,_.Ks)({kind:"component_action",component_id:t,field:(0,tl.q)(e.detail.path)});(0,e$.r)(this,"section-select",{sectionKey:i})}}}function ox(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}ok.DRAFT_DEBOUNCE_MS=200,ok.styles=[M.G9,M.G4,tC.z9,iU.O,ij,tz.h],ow([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],ok.prototype,"_localize",void 0),ow([(0,o.Fg)({context:P.Ie})],ok.prototype,"_api",void 0),ow([(0,o.Fg)({context:P.I9,subscribe:!0}),(0,r.wk)()],ok.prototype,"_resolvedComponents",void 0),ow([(0,r.MZ)()],ok.prototype,"configuration",void 0),ow([(0,r.MZ)()],ok.prototype,"sectionKey",void 0),ow([(0,r.MZ)({type:Number})],ok.prototype,"fromLine",void 0),ow([(0,r.MZ)({attribute:!1})],ok.prototype,"focusFieldPath",void 0),ow([(0,r.MZ)({attribute:!1})],ok.prototype,"backendErrors",void 0),ow([(0,r.MZ)()],ok.prototype,"yaml",void 0),ow([(0,r.MZ)({attribute:!1})],ok.prototype,"yamlPaneVisible",void 0),ow([(0,r.MZ)({attribute:!1})],ok.prototype,"board",void 0),ow([(0,r.MZ)()],ok.prototype,"boardName",void 0),ow([(0,r.wk)()],ok.prototype,"_config",void 0),ow([(0,r.wk)()],ok.prototype,"_values",void 0),ow([(0,r.wk)()],ok.prototype,"_loading",void 0),ow([(0,r.wk)()],ok.prototype,"_dirty",void 0),ow([(0,r.wk)()],ok.prototype,"_error",void 0),ow([(0,r.wk)()],ok.prototype,"_deletingRow",void 0),ow([(0,r.wk)()],ok.prototype,"_isUnknown",void 0),ow([(0,r.wk)()],ok.prototype,"_isPlatformDomain",void 0),ow([(0,r.wk)()],ok.prototype,"_fieldErrors",void 0),ow([(0,r.wk)()],ok.prototype,"_clearedBackendPaths",void 0),ow([(0,r.wk)()],ok.prototype,"_advancedShownSections",void 0),ow([(0,r.wk)()],ok.prototype,"_presentComponents",void 0),ow([(0,r.wk)()],ok.prototype,"_resolvedFromLine",void 0),ow([(0,r.P)("esphome-confirm-dialog")],ok.prototype,"_confirmDialog",void 0),ow([(0,r.P)("esphome-add-api-action-dialog")],ok.prototype,"_addApiActionDialog",void 0),ow([(0,r.P)("esphome-add-automation-dialog")],ok.prototype,"_addAutomationDialog",void 0),ow([(0,r.wk)()],ok.prototype,"_deleting",void 0),ow([(0,o.Gt)({context:P.km})],ok.prototype,"_valuesRead",void 0),ok=ow([(0,r.EM)("esphome-device-section-config")],ok),(0,I.C)({"open-in-new":a.mdiOpenInNew,"arrow-left":a.mdiArrowLeft,close:a.mdiClose,"party-popper":a.mdiPartyPopper,"plus-circle-outline":a.mdiPlusCircleOutline,usb:a.mdiUsb});class oz extends s.WF{willUpdate(e){e.has("board")&&this._refreshAlternateBoards()}updated(e){if(e.has("yaml")&&this.selectedSection){var t,i;let o=()=>{this._sectionConfig?.reload(),this._automationEditor?.reload(),this._scriptEditor?.reload(),this._apiActionEditor?.reload()};(this._reloadTimer&&(clearTimeout(this._reloadTimer),this._reloadTimer=null),t=e.get("yaml"),i=this.yaml,t||!i)?this._reloadTimer=setTimeout(o,1e3):o()}}connectedCallback(){super.connectedCallback(),this.addEventListener("request-add-component",this._onRequestAddComponent)}disconnectedCallback(){super.disconnectedCallback(),this._reloadTimer&&clearTimeout(this._reloadTimer),this.removeEventListener("request-add-component",this._onRequestAddComponent)}async _refreshAlternateBoards(){let e=this.board;if(!e){this._alternatesForBoardId=null,this._alternateBoards=[];return}if(e.id!==this._alternatesForBoardId){this._alternatesForBoardId=e.id,this._alternateBoards=[];try{let t=await this._api.getCompatibleBoards(e.id);if(this._alternatesForBoardId!==e.id)return;this._alternateBoards=t.filter(t=>t.id!==e.id)}catch(t){console.error("Failed to load compatible boards:",t),this._alternatesForBoardId===e.id&&(this._alternatesForBoardId=null,this._alternateBoards=[])}}}render(){let e=this.board;return(0,s.qy)`
      ${!this.selectedSection&&e?(0,s.qy)`
              <div class="board-header">
                <div class="board-info">
                  <h3 class="board-name">${e.name}</h3>
                  <div class="board-tags">
                    ${e.tags.map(e=>(0,s.qy)`<wa-badge variant="brand" pill>${e}</wa-badge>`)}
                    <a
                      class="board-info-link"
                      href=${e.docs_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      ${this._localize("device.more_info")}
                      <wa-icon library="mdi" name="open-in-new"></wa-icon>
                    </a>
                    ${this._alternateBoards.length>0?(0,s.qy)`<button
                            type="button"
                            class="board-change-link"
                            @click=${this._openChangeBoard}
                          >
                            ${this._localize("device.change_board_link")}
                          </button>`:s.s6}
                  </div>
                  <p class="board-description">${(0,ej.Gc)(e.description)}</p>
                </div>
                <div class="board-image">
                  <img
                    src=${(0,eK.Ru)(e)}
                    alt=${e.name}
                    referrerpolicy="no-referrer"
                    @error=${eK.jt}
                  />
                </div>
              </div>
              <div class="board-separator"></div>
            `:s.s6}
      <esphome-config-migration-notice
        .configuration=${this.configuration}
        .yaml=${this.yaml}
      ></esphome-config-migration-notice>
      <esphome-mac-suffix-notice
        .configuration=${this.configuration}
        .yaml=${this.yaml}
      ></esphome-mac-suffix-notice>
      <esphome-ota-encryption-notice
        .configuration=${this.configuration}
        .yaml=${this.yaml}
      ></esphome-ota-encryption-notice>
      ${this.selectedSection?this._renderSelectedSection():(0,s.qy)`
              ${this.justCreated?this._renderWelcomeBanner():s.s6}
              ${this._renderStepSection({title:this._localize("device.step_core"),desc:this._localize("device.step_core_desc"),icon:ts.I.core,action:this._localize("device.show_core_configuration"),section:"core"})}
              ${this._renderStepSection({title:this._localize("device.step_components"),desc:this._localize("device.step_components_desc"),icon:ts.I.components,action:this._localize("device.show_components"),section:"components"})}
              ${this._renderStepSection({title:this._localize("device.step_automations"),desc:this._localize("device.step_automations_desc"),icon:ts.I.automations,action:this._localize("device.show_automations"),section:"automations"})}
            `}

      <esphome-add-component-dialog
        .boardName=${e?.name??""}
        .configuration=${this.configuration}
        .platform=${e?.esphome.platform??""}
        .board=${e}
        .yaml=${this.yaml}
      ></esphome-add-component-dialog>
      <esphome-change-board-dialog
        .currentBoard=${e}
        .boards=${this._alternateBoards}
        @select-board=${this._onSelectBoard}
      ></esphome-change-board-dialog>
    `}_renderSelectedSection(){let e=this.selectedSection,t=e.startsWith("automation:")?this._locationForKey(e):null;return t?.kind==="script"?(0,s.qy)`<esphome-script-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-script-editor>`:t?.kind==="api_action"?(0,s.qy)`<esphome-api-action-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-api-action-editor>`:t?(0,s.qy)`<esphome-automation-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-automation-editor>`:(0,s.qy)`<esphome-device-section-config
      .configuration=${this.configuration}
      .sectionKey=${e}
      .fromLine=${this.selectedFromLine}
      .focusFieldPath=${this.focusFieldPath}
      .backendErrors=${this.backendErrors}
      .yaml=${this.yaml}
      .board=${this.board}
      .boardName=${this.board?.name??""}
      .yamlPaneVisible=${this.yamlPaneVisible}
    ></esphome-device-section-config>`}_renderStepSection(e){return(0,s.qy)`
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
    `}_onShowNavSection(e){(0,e$.r)(this,"nav-section-show",{section:e})}_renderWelcomeBanner(){return this.board?(0,s.qy)`
      <wa-callout class="welcome-banner" variant="brand" role="status">
        <wa-icon slot="icon" library="mdi" name="party-popper"></wa-icon>
        <p class="welcome-banner-title">
          ${this._localize("device.welcome_banner_title",{name:this.board.name})}
        </p>
        <p class="welcome-banner-text">${this._localize("device.welcome_banner_body")}</p>
        <p class="welcome-banner-text">
          ${this._localize("device.welcome_banner_first_install")}
        </p>
        <button
          type="button"
          class="action-item welcome-banner-install"
          @click=${this._onWelcomeInstall}
        >
          <wa-icon library="mdi" name="usb"></wa-icon>
          ${this._localize("device.welcome_banner_install_button")}
        </button>
        <button
          type="button"
          class="welcome-banner-close"
          aria-label=${this._localize("device.welcome_banner_dismiss")}
          @click=${this._onDismissWelcome}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </wa-callout>
    `:s.s6}_onDismissWelcome(){(0,e$.r)(this,"just-created-dismiss")}_onWelcomeInstall(){(0,e$.r)(this,"request-install")}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this._alternateBoards=[],this._alternatesForBoardId=null,this.yaml="",this.configuration="",this.justCreated=!1,this.yamlPaneVisible=!0,this.selectedSection=null,this.backendErrors=L.eV,this._reloadTimer=null,this._onRequestAddComponent=e=>{let t=e.detail;t?.domain&&(e.stopPropagation(),this._addComponentDialog?.openWithSearch(t.domain))},this._openChangeBoard=()=>{this._changeBoardDialog?.open()},this._onSelectBoard=e=>{e.stopPropagation(),(0,e$.r)(this,"change-board",e.detail)},this._locationForKey=(0,d.A)(_.ac)}}oz.styles=[M.G9,ta],ox([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],oz.prototype,"_localize",void 0),ox([(0,o.Fg)({context:P.Ie})],oz.prototype,"_api",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"board",void 0),ox([(0,r.wk)()],oz.prototype,"_alternateBoards",void 0),ox([(0,r.MZ)()],oz.prototype,"yaml",void 0),ox([(0,r.MZ)()],oz.prototype,"configuration",void 0),ox([(0,r.MZ)({type:Boolean})],oz.prototype,"justCreated",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"yamlPaneVisible",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"selectedSection",void 0),ox([(0,r.MZ)({type:Number})],oz.prototype,"selectedFromLine",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"focusFieldPath",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"focusYamlPath",void 0),ox([(0,r.MZ)({attribute:!1})],oz.prototype,"backendErrors",void 0),ox([(0,r.P)("esphome-device-section-config")],oz.prototype,"_sectionConfig",void 0),ox([(0,r.P)("esphome-automation-editor")],oz.prototype,"_automationEditor",void 0),ox([(0,r.P)("esphome-script-editor")],oz.prototype,"_scriptEditor",void 0),ox([(0,r.P)("esphome-api-action-editor")],oz.prototype,"_apiActionEditor",void 0),ox([(0,r.P)("esphome-add-component-dialog")],oz.prototype,"_addComponentDialog",void 0),ox([(0,r.P)("esphome-change-board-dialog")],oz.prototype,"_changeBoardDialog",void 0),oz=ox([(0,r.EM)("esphome-device-board-info")],oz);var oC=i(8990);function oS(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"alert-circle-outline":a.mdiAlertCircleOutline});class oF extends s.WF{willUpdate(e){(e.has("errors")||e.has("caretLine")||e.has("editorFocused")||e.has("completionOpen"))&&this._evaluate()}disconnectedCallback(){super.disconnectedCallback(),this._cancelRevealTimer()}render(){return 0===this._visible.length?s.s6:(0,s.qy)`<div class="danger-banner invalid-banner" role="alert">
      <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
      <div class="danger-banner-text">
        ${this._visible.slice(0,6).map(e=>(0,s.qy)`<span
              >${(0,ej.zA)(e.message)}${e.fix?(0,s.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto link-button"
                        title=${this._localize("yaml_editor.error_auto_fix_hint")}
                        @click=${()=>this._onAutoFix(e.fix)}
                      >
                        ${this._localize("yaml_editor.error_auto_fix")}
                      </button>
                    `:s.s6}${e.line?(0,s.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto link-button"
                        @click=${()=>this._onGotoLine(e.line)}
                      >
                        ${this._localize("yaml_editor.error_go_to_line",{line:e.line})}
                      </button>
                    `:s.s6}</span
            >`)}
        ${this._visible.length>6?(0,s.qy)`<span class="invalid-banner-more"
                >${this._localize("device.editor_invalid_more",{count:this._visible.length-6})}</span
              >`:s.s6}
      </div>
    </div>`}_onAutoFix(e){this.dispatchEvent(new CustomEvent("banner-auto-fix",{detail:{fix:e},bubbles:!0,composed:!0}))}_onGotoLine(e){this.dispatchEvent(new CustomEvent("banner-goto-line",{detail:{line:e},bubbles:!0,composed:!0}))}_evaluate(){if(0===this.errors.length){this._cancelRevealTimer(),this._visible.length&&(this._visible=[]);return}if(this._visible.length>0||this._shouldReveal()){this._cancelRevealTimer(),this._visible=this.errors;return}this.completionOpen?this._cancelRevealTimer():this._armRevealTimer()}_shouldReveal(){return!this.completionOpen&&(!!(!this.editorFocused||this.errors.some(e=>"parse"!==e.kind&&void 0===e.line)||this.errors.some(e=>void 0!==e.line&&Math.abs(e.line-this.caretLine)>3))||performance.now()-this.getLastEditAt()>=15e3)}_armRevealTimer(){this._cancelRevealTimer();let e=15e3-(performance.now()-this.getLastEditAt());this._revealTimer=setTimeout(()=>{this._revealTimer=void 0,this._evaluate()},Math.max(e,100))}_cancelRevealTimer(){void 0!==this._revealTimer&&(clearTimeout(this._revealTimer),this._revealTimer=void 0)}constructor(...e){super(...e),this._localize=e=>e,this.errors=[],this.caretLine=0,this.editorFocused=!1,this.completionOpen=!1,this.getLastEditAt=()=>-1/0,this._visible=[]}}function oP(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}oF.styles=[iU.O,oC.R,(0,s.AH)`
      :host {
        display: contents;
      }

      .invalid-banner {
        flex: 0 0 auto;
      }

      /* Deltas over .link-button: banner-colored (not primary), bolder,
         and kept on one line inside the wrapping error text. */
      .invalid-banner-goto {
        appearance: none;
        margin-left: 0.35em;
        color: inherit;
        font-weight: var(--wa-font-weight-semibold);
        white-space: nowrap;
      }

      .invalid-banner-goto:hover {
        text-decoration: none;
      }

      .invalid-banner-more {
        font-size: var(--wa-font-size-2xs);
        opacity: 0.85;
      }
    `],oS([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],oF.prototype,"_localize",void 0),oS([(0,r.MZ)({attribute:!1})],oF.prototype,"errors",void 0),oS([(0,r.MZ)({type:Number})],oF.prototype,"caretLine",void 0),oS([(0,r.MZ)({type:Boolean})],oF.prototype,"editorFocused",void 0),oS([(0,r.MZ)({type:Boolean})],oF.prototype,"completionOpen",void 0),oS([(0,r.MZ)({attribute:!1})],oF.prototype,"getLastEditAt",void 0),oS([(0,r.wk)()],oF.prototype,"_visible",void 0),oF=oS([(0,r.EM)("esphome-editor-invalid-banner")],oF),(0,I.C)({"chevron-down":a.mdiChevronDown,"content-save":a.mdiContentSave,"dock-left":a.mdiDockLeft,"dock-right":a.mdiDockRight,"view-split-vertical":a.mdiViewSplitVertical,upload:a.mdiUpload,"file-compare":a.mdiFileCompare});class oq extends s.WF{connectedCallback(){super.connectedCallback(),this._isMobile=this._mql.matches,this._mql.addEventListener("change",this._onMqlChange),window.addEventListener(S.ax,this._onTourReveal)}disconnectedCallback(){super.disconnectedCallback(),this._mql.removeEventListener("change",this._onMqlChange),window.removeEventListener(S.ax,this._onTourReveal)}render(){var e;let t,i,o=(0,z.wS)(this.layout,this._isMobile),a=!this._isMobile&&this.navCollapsed&&"right"===o,r=this._localize("device.editor_title_ready",{name:this.deviceTitle});return(0,s.qy)`
      <section class="card">
        <header class="card-header ${a?"card-header--compact":""}">
          <slot name="header-start"></slot>
          <div class="editor-header-main">
            <div class="editor-header-titlerow">
              <h2 class="editor-header-title truncate">${r}</h2>
              ${this.configuration&&!a?(0,s.qy)`<span class="editor-header-file truncate"
                      >${this.configuration}</span
                    >`:s.s6}
            </div>
          </div>
          ${e={localize:this._localize,effectiveLayout:o,revealSensitive:this._revealSensitive,showDiffButton:this._showDiffButton,showDiff:this._showDiff,yaml:this.yaml,savedYaml:this.savedYaml,onToggleRevealSensitive:()=>this._toggleRevealSensitive(),onToggleDiff:()=>this._toggleDiff(),onSetLayout:e=>this._setLayout(e)},t=(t,i,o,a="")=>{let r=e.localize(o);return(0,s.qy)`<button
        id="btn-layout-${t}"
        type="button"
        class="ghost-icon-btn ${a}"
        aria-pressed=${e.effectiveLayout===t}
        @click=${()=>e.onSetLayout(t)}
        aria-label=${r}
      >
        <wa-icon library="mdi" name=${i}></wa-icon>
      </button>
      <wa-tooltip for="btn-layout-${t}">${r}</wa-tooltip>`},(0,s.qy)`<div class="header-actions">
    ${"left"!==e.effectiveLayout?eF(e.localize,e.revealSensitive,e.onToggleRevealSensitive,"diff-toggle"):s.s6}
    ${e.showDiffButton?(i=e.showDiff?e.localize("device.diff_view_editor"):e.localize("device.diff_view_diff"),(0,s.qy)`<button
                id="btn-diff-toggle"
                type="button"
                class="ghost-icon-btn diff-toggle"
                aria-pressed=${e.showDiff}
                ?disabled=${e.yaml===e.savedYaml&&!e.showDiff}
                aria-label=${i}
                @click=${e.onToggleDiff}
              >
                <wa-icon library="mdi" name="file-compare"></wa-icon>
              </button>
              <wa-tooltip for="btn-diff-toggle">${i}</wa-tooltip>`):s.s6}
    <div
      class="layout-toggle"
      role="group"
      aria-label=${e.localize("device.editor_layout_label")}
      ${(0,S.Wf)("layout-toggle")}
    >
      ${t("left","dock-left","device.layout_components_only")}
      ${t("both","view-split-vertical","device.layout_split","split-btn")}
      ${t("right","dock-right","device.layout_yaml_only")}
    </div>
  </div>`}
        </header>
        <div class="card-body">
          <div class="editor-floating-actions">
            <!-- Leftmost so it stays clear of Save in the lower-right corner:
                 a mis-tap on Save must not land on the overflow menu.
                 Carries Validate too (Install validates anyway, so the
                 explicit button rarely earned its slot on the bar). -->
            <esphome-device-actions-menu
              ?busy=${this.busy}
              ?validate-disabled=${this.hasUnsavedEdits}
              .webUiUrl=${this.webUiUrl}
              @validate=${this._onValidate}
            ></esphome-device-actions-menu>
            ${this._renderPrimaryAction()}
            <button
              type="button"
              class="save-button"
              ?disabled=${!this.hasUnsavedEdits||this.saving}
              aria-busy=${this.saving}
              @click=${this._onSave}
              title=${this._localize("device.save_yaml")}
            >
              ${this.saving?(0,s.qy)`<wa-spinner></wa-spinner>`:(0,s.qy)`<wa-icon library="mdi" name="content-save"></wa-icon>`}
              ${this._localize("device.save")}
            </button>
          </div>
          <div
            class="editor-layout ${"both"===o?"editor-layout--both":"left"===o?"editor-layout--left":"editor-layout--right"} ${this._dragging?"dragging":""}"
            style=${"both"===o?`grid-template-columns: ${this._splitRatio}fr var(--pane-divider-width) ${1-this._splitRatio}fr`:""}
          >
            <div class="editor-pane editor-pane--left" ${(0,S.Wf)("central")}>
              <esphome-device-board-info
                .board=${this.board}
                .yaml=${this.yaml}
                .configuration=${this.configuration}
                .selectedSection=${this.selectedSection}
                .selectedFromLine=${this.selectedFromLine}
                .focusFieldPath=${this.focusFieldPath}
                .focusYamlPath=${this.focusYamlPath}
                .backendErrors=${this.backendErrors}
                .justCreated=${this.justCreated}
                .yamlPaneVisible=${"left"!==o}
                @show-yaml-editor=${this._onShowYamlEditor}
              ></esphome-device-board-info>
            </div>
            ${"both"===o?(0,s.qy)`<div
                    class="pane-divider ${this._dragging?"dragging":""}"
                    role="separator"
                    aria-orientation="vertical"
                    aria-label=${this._localize("device.resize_panes")}
                    aria-valuemin=${25}
                    aria-valuemax=${75}
                    aria-valuenow=${Math.round(100*this._splitRatio)}
                    aria-valuetext=${this._localize("device.resize_panes_value",{percent:Math.round(100*this._splitRatio)})}
                    tabindex="0"
                    @pointerdown=${this._onDividerPointerDown}
                    @keydown=${this._onDividerKeydown}
                  ></div>`:s.s6}
            <div class="editor-pane editor-pane--right" ${(0,S.Wf)("yaml")}>
              <div class="editor-pane-body">
                ${this._showDiff?(0,s.qy)`<esphome-yaml-diff
                        .oldValue=${this.savedYaml}
                        .newValue=${this.yaml}
                        .revealSensitive=${this._revealSensitive}
                      ></esphome-yaml-diff>`:(0,s.qy)`<esphome-yaml-editor
                        .value=${this.yaml}
                        .configuration=${this.configuration}
                        .board=${this.board}
                        .highlightRange=${this.highlightRange}
                        .scrollToHighlight=${this.scrollToHighlight}
                        .revealSensitive=${this._revealSensitive}
                        @yaml-change=${this._onYamlChange}
                        @yaml-diagnostics=${this._onYamlDiagnostics}
                        @yaml-auto-fix=${this._onBannerAutoFix}
                        @yaml-cursor-line=${this._onYamlCursorLine}
                        @yaml-completion-open=${this._onYamlCompletionOpen}
                        @focusin=${this._onEditorFocusIn}
                        @focusout=${this._onEditorFocusOut}
                      ></esphome-yaml-editor>`}
              </div>
              ${!this._showDiff?(0,s.qy)`<esphome-editor-invalid-banner
                      .errors=${this._liveErrors}
                      .caretLine=${this._caretLine}
                      .editorFocused=${this._editorFocused}
                      .completionOpen=${this._completionOpen}
                      .getLastEditAt=${this._getLastEditAt}
                      @banner-auto-fix=${this._onBannerAutoFix}
                      @banner-goto-line=${this._onBannerGotoLine}
                    ></esphome-editor-invalid-banner>`:s.s6}
            </div>
          </div>
        </div>
        ${this._autoFixConfirmOpen?(0,s.qy)`<esphome-confirm-dialog
                class="auto-fix-confirm"
                heading=${this._localize("yaml_editor.auto_fix_confirm_heading")}
                message=${this._localize("yaml_editor.auto_fix_confirm_message")}
                confirm-label=${this._localize("yaml_editor.auto_fix_confirm_apply")}
              ></esphome-confirm-dialog>`:s.s6}
      </section>
    `}_onSave(){(0,e$.r)(this,"save-yaml")}_onValidate(){(0,e$.r)(this,"validate-device")}_toggleDiff(){this._showDiff=!this._showDiff}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_renderPrimaryAction(){var e={localize:this._localize,showUpdate:this.showUpdate,showModified:this.showModified,busy:this.busy,installedVersion:this.installedVersion,availableVersion:this.availableVersion,onUpdate:()=>this._onUpdate(),onInstall:()=>this._onInstall()};if(e.showUpdate)return(0,s.qy)`<div class="install-split">
      <button
        type="button"
        class="install-fab install-split__main"
        ${(0,S.Wf)("install")}
        @click=${e.onUpdate}
        title=${(0,eq.w3)(e.localize,e.busy,e.installedVersion,e.availableVersion,"dashboard.update")}
      >
        <wa-icon library="mdi" name="upload"></wa-icon>
        ${(0,eq.MV)(e.localize,e.busy,"dashboard.update")}
      </button>
      <button
        type="button"
        class="install-fab install-split__caret"
        ?disabled=${e.busy}
        @click=${e.onInstall}
        aria-label=${e.localize("device.install_choose_method")}
        title=${e.localize("device.install_choose_method")}
      >
        <wa-icon library="mdi" name="chevron-down"></wa-icon>
      </button>
    </div>`;let t=(0,eq.MV)(e.localize,e.busy,"dashboard.install");return(0,s.qy)`<button
    type="button"
    class="install-fab ${e.showModified?"":"install-fab--muted"}"
    ${(0,S.Wf)("install")}
    @click=${e.onInstall}
    title=${t}
  >
    <wa-icon library="mdi" name="upload"></wa-icon>
    ${t}
  </button>`}_onInstall(){(0,e$.r)(this,"install-device")}_onUpdate(){(0,e$.r)(this,"update-device")}willUpdate(e){if(e.has("configuration")&&(this._liveErrors.length&&(this._liveErrors=[]),this._caretLine=0,this._lastEditAt=-1/0,this._editorFocused=!1,this._completionOpen=!1),this._showDiff&&e.has("_showDiffButton")&&!this._showDiffButton){this._showDiff=!1;return}this._showDiff&&e.has("savedYaml")&&this.yaml===this.savedYaml&&(this._showDiff=!1)}_onYamlDiagnostics(e){if(e.detail.configuration!==this.configuration)return;let t=e.detail.errors;(0,j.r)(t,this._liveErrors,(e,t)=>e.message===t.message&&e.line===t.line&&e.kind===t.kind&&e.fix?.line===t.fix?.line&&e.fix?.indent===t.fix?.indent&&e.fix?.key===t.fix?.key)||(this._liveErrors=t)}_onYamlCursorLine(e){this._caretLine=e.detail.line}_onYamlCompletionOpen(e){this._completionOpen=e.detail.open}_onBannerAutoFix(e){this._autoFix(e.detail.fix)}_onBannerGotoLine(e){this._gotoErrorLine(e.detail.line)}_autoFix(e){let t=this._yamlEditor;if(!t){console.error("[auto-fix] no editor ref"),(0,B.UG)(this._localize("yaml_editor.auto_fix_failed"));return}t.applyAutoFix(e,()=>this._confirmAutoFix()).then(e=>{"stale"===e?(0,B.KQ)(this._localize("yaml_editor.auto_fix_stale")):"unavailable"===e&&(console.error("[auto-fix] editor unavailable"),(0,B.UG)(this._localize("yaml_editor.auto_fix_failed")))}).catch(e=>{console.error("[auto-fix] could not run:",e),(0,B.UG)(this._localize("yaml_editor.auto_fix_failed"))})}async _confirmAutoFix(){if(this._autoFixConfirmOpen)return!1;this._autoFixConfirmOpen=!0,await this.updateComplete;let e=this._autoFixConfirmDialog;if(!e)throw this._autoFixConfirmOpen=!1,Error("auto-fix confirm dialog failed to mount");try{return await new Promise(t=>{let i=i=>{e.removeEventListener("confirm",o),e.removeEventListener("cancel",a),t(i)},o=()=>i(!0),a=()=>i(!1);e.addEventListener("confirm",o),e.addEventListener("cancel",a),e.open()})}finally{this._autoFixConfirmOpen=!1}}_gotoErrorLine(e){(0,e$.r)(this,"goto-line",{line:e})}_setLayout(e){(0,e$.r)(this,"layout-change",e)}_onShowYamlEditor(e){e.stopPropagation(),this._setLayout("both")}_onYamlChange(e){this._lastEditAt=performance.now(),(0,e$.r)(this,"yaml-change",e.detail)}constructor(...e){super(...e),this._localize=e=>e,this.yaml="",this.layout="both",this.navCollapsed=!1,this.deviceTitle="",this.board=null,this.justCreated=!1,this.webUiUrl="",this._isMobile=!1,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._saveShortcut=new ek.k(this,()=>{this.hasUnsavedEdits&&this._onSave()}),this._onTourReveal=e=>{let{id:t}=e.detail,i=C(t,this.layout,this._isMobile);i&&(0,e$.r)(this,F.um,i)},this.highlightRange=null,this.scrollToHighlight=!1,this.configuration="",this.selectedSection=null,this.backendErrors=L.eV,this.savedYaml="",this.hasUnsavedEdits=!1,this.saving=!1,this.showModified=!1,this.showUpdate=!1,this.installedVersion="",this.availableVersion="",this.busy=!1,this._showDiffButton=!1,this._showDiff=!1,this._revealSensitive=!1,this._liveErrors=[],this._caretLine=0,this._editorFocused=!1,this._completionOpen=!1,this._lastEditAt=-1/0,this._getLastEditAt=()=>this._lastEditAt,this._splitRatio=(()=>{try{let e=localStorage.getItem(ex),t=null===e?0/0:Number.parseFloat(e);return Number.isFinite(t)?ez(t):.5}catch{return .5}})(),this._dragging=!1,this._toastClearance=new eS.E(this,()=>this._floatingActionsEl),this._onEditorFocusIn=()=>{this._editorFocused=!0},this._onEditorFocusOut=e=>{let t=e.currentTarget;this._editorFocused=e.relatedTarget instanceof Node&&t.contains(e.relatedTarget)},this._autoFixConfirmOpen=!1,this._onDividerPointerDown=e=>{if(0!==e.button)return;let t=this._layoutEl;if(!t)return;e.preventDefault();let i=t.getBoundingClientRect();this._dragging=!0;let o=e.currentTarget;o.setPointerCapture(e.pointerId);let a=o.getBoundingClientRect().width,s=i.width-a,r=e=>{s<=0||(this._splitRatio=ez((e.clientX-i.left-a/2)/s))},n=()=>{this._dragging=!1,eC(this._splitRatio),o.removeEventListener("pointermove",r),o.removeEventListener("pointerup",n),o.removeEventListener("pointercancel",n),o.removeEventListener("lostpointercapture",n)};o.addEventListener("pointermove",r),o.addEventListener("pointerup",n),o.addEventListener("pointercancel",n),o.addEventListener("lostpointercapture",n)},this._onDividerKeydown=e=>{let t=((e,t)=>{let i;if("ArrowLeft"===t)i=e-.02;else if("ArrowRight"===t)i=e+.02;else if("Home"===t)i=.25;else{if("End"!==t)return null;i=.75}return ez(i)})(this._splitRatio,e.key);null!==t&&(e.preventDefault(),this._splitRatio=t,eC(this._splitRatio))}}}oq.styles=[M.G9,ew.U,eP],oP([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],oq.prototype,"_localize",void 0),oP([(0,r.MZ)()],oq.prototype,"yaml",void 0),oP([(0,r.MZ)()],oq.prototype,"layout",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"navCollapsed",void 0),oP([(0,r.MZ)()],oq.prototype,"deviceTitle",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"board",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"justCreated",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"webUiUrl",void 0),oP([(0,r.wk)()],oq.prototype,"_isMobile",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"highlightRange",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"scrollToHighlight",void 0),oP([(0,r.MZ)()],oq.prototype,"configuration",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"selectedSection",void 0),oP([(0,r.MZ)({type:Number})],oq.prototype,"selectedFromLine",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"focusFieldPath",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"focusYamlPath",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"backendErrors",void 0),oP([(0,r.MZ)({attribute:!1})],oq.prototype,"savedYaml",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"hasUnsavedEdits",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"saving",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"showModified",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"showUpdate",void 0),oP([(0,r.MZ)()],oq.prototype,"installedVersion",void 0),oP([(0,r.MZ)()],oq.prototype,"availableVersion",void 0),oP([(0,r.MZ)({type:Boolean})],oq.prototype,"busy",void 0),oP([(0,o.Fg)({context:P.Pt,subscribe:!0}),(0,r.wk)()],oq.prototype,"_showDiffButton",void 0),oP([(0,r.wk)()],oq.prototype,"_showDiff",void 0),oP([(0,r.wk)()],oq.prototype,"_revealSensitive",void 0),oP([(0,r.wk)()],oq.prototype,"_liveErrors",void 0),oP([(0,r.wk)()],oq.prototype,"_caretLine",void 0),oP([(0,r.wk)()],oq.prototype,"_editorFocused",void 0),oP([(0,r.wk)()],oq.prototype,"_completionOpen",void 0),oP([(0,r.wk)()],oq.prototype,"_splitRatio",void 0),oP([(0,r.wk)()],oq.prototype,"_dragging",void 0),oP([(0,r.P)(".editor-layout")],oq.prototype,"_layoutEl",void 0),oP([(0,r.P)("esphome-yaml-editor")],oq.prototype,"_yamlEditor",void 0),oP([(0,r.P)("esphome-confirm-dialog.auto-fix-confirm")],oq.prototype,"_autoFixConfirmDialog",void 0),oP([(0,r.P)(".editor-floating-actions")],oq.prototype,"_floatingActionsEl",void 0),oP([(0,r.wk)()],oq.prototype,"_autoFixConfirmOpen",void 0),oq=oP([(0,r.EM)("esphome-device-editor")],oq),i(8297),i(8697),i(132),i(3199),i(9786);var oM=i(6029);function oL(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}(0,I.C)({"alert-outline":a.mdiAlertOutline});class oR extends s.WF{get _canGoToError(){return this.firstErrorLine>0&&!this.firstErrorFile}open(){this._resolvedExit=null,this._dialog.open=!0}close(){this._dialog.open=!1}render(){let e=this._localize("device.yaml_invalid_message",{count:this.errorCount}),t=this.firstErrorFile?this._localize("device.yaml_invalid_in_included_file",{file:this.firstErrorFile,line:this.firstErrorLine}):"";return(0,s.qy)`
      <esphome-base-dialog
        ?open=${this._dialog.open}
        .label=${this._localize("device.yaml_invalid_title")}
        .confirmOnEnter=${this._gotoOnEnter}
        @request-close=${this._dialog.onRequestClose}
        @after-hide=${this._onAfterHide}
      >
        <div class="body">
          <div class="icon-wrap">
            <wa-icon library="mdi" name="alert-outline"></wa-icon>
          </div>
          <div class="text">
            ${e}
            ${t?(0,s.qy)`<div class="included-file">${t}</div>`:s.s6}
            ${this.firstErrorMessage?(0,s.qy)`<div class="first-error">${this.firstErrorMessage}</div>`:s.s6}
          </div>
        </div>
        <div class="actions">
          <button class="btn btn--cancel" @click=${this.close}>
            ${this._localize("layout.cancel")}
          </button>
          <button
            class="btn btn--goto"
            ?disabled=${!this._canGoToError}
            @click=${this._goto}
          >
            ${this._localize("device.yaml_invalid_go_to_error")}
          </button>
          <button class="btn btn--save-anyway" @click=${this._saveAnyway}>
            ${this._localize("device.yaml_invalid_save_anyway")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_goto(){this._canGoToError&&null===this._resolvedExit&&(this._resolvedExit="goto",this.close(),(0,e$.r)(this,"goto",{line:this.firstErrorLine,col:this.firstErrorCol}))}_saveAnyway(){this._resolvedExit="save-anyway",this.close(),(0,e$.r)(this,"save-anyway")}_onAfterHide(){this._dialog.open=!1,null===this._resolvedExit&&(0,e$.r)(this,"cancel")}constructor(...e){super(...e),this._localize=e=>e,this.errorCount=0,this.firstErrorLine=0,this.firstErrorCol=0,this.firstErrorMessage="",this.firstErrorFile="",this._dialog=new eQ.T(this),this._resolvedExit=null,this._gotoOnEnter=()=>{this._canGoToError&&this._goto()}}}function oA(e,t,i,o){var a,s=arguments.length,r=s<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(a=e[n])&&(r=(s<3?a(r):s>3?a(t,i,r):a(t,i))||r);return s>3&&r&&Object.defineProperty(t,i,r),r}oR.styles=[M.G9,oM.W,(0,s.AH)`
      esphome-base-dialog {
        --width: 480px;
      }

      .icon-wrap {
        background: color-mix(in srgb, var(--esphome-error), transparent 88%);
        color: var(--esphome-error);
      }

      .included-file {
        margin-top: var(--wa-space-xs);
        color: var(--wa-color-text-normal);
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
    `],oL([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],oR.prototype,"_localize",void 0),oL([(0,r.MZ)({type:Number})],oR.prototype,"errorCount",void 0),oL([(0,r.MZ)({type:Number})],oR.prototype,"firstErrorLine",void 0),oL([(0,r.MZ)({type:Number})],oR.prototype,"firstErrorCol",void 0),oL([(0,r.MZ)()],oR.prototype,"firstErrorMessage",void 0),oL([(0,r.MZ)()],oR.prototype,"firstErrorFile",void 0),oR=oL([(0,r.EM)("esphome-yaml-validation-dialog")],oR),(0,I.C)({"arrow-left":a.mdiArrowLeft,"chevron-right":a.mdiChevronRight,menu:a.mdiMenu});class oE extends s.WF{get _device(){return this._devices.find(e=>e.configuration===this.id)??null}willUpdate(e){if(super.willUpdate(e),!e.has("_devices")&&!e.has("id"))return;let t=this._device,i=t?t.target_platform?[...t.loaded_integrations,t.target_platform]:t.loaded_integrations:[],o=this._providedResolvedComponents;(0,j.r)(i,o)||(this._providedResolvedComponents=i);let a=t?.loaded_platforms??[];(0,j.r)(a,this._providedResolvedPlatforms)||(this._providedResolvedPlatforms=a)}_navErrorCounts(e,t){let i=this._baseErrorCounts(e);if(null===t||!i.has(t))return i;let o=new Map(i);return o.delete(t),o}_createInstallController(){let e=this;return new x({addController:t=>e.addController(t),removeController:t=>e.removeController(t),requestUpdate:()=>e.requestUpdate(),get updateComplete(){return e.updateComplete},get device(){return e._device},get commandDialog(){return e._commandDialog??null},get firmwareDialog(){return e._firmwareDialog??null},get logsDialog(){return e._logsDialog??null},get api(){return e._api},get localize(){return e._localize},openActiveJobProgress:()=>e._showActiveJobProgress()})}get _isYamlDirty(){return this._yaml!==this._savedYaml}get _isDirty(){return this._isYamlDirty||this._sectionDirty}async connectedCallback(){super.connectedCallback(),this._loadPreferences(),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("keydown",this._onKeydown),this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("keydown",this._onKeydown),this._mql.removeEventListener("change",this._onMqlChange),this._cancelCursorSwitch(),this._unsavedGuard.cancelPending()}updated(e){e.has("id")&&this.id&&(this._justCreated=(0,O.RI)(this.id),this._loadedBoardId=null,this._board=null,this._platformReady=!1,this._backendErrors.length&&(this._backendErrors=[]),this._heldUnknownInstance=null,this._cancelCursorSwitch(),this._kickKnownKeys(),this._activeSection=null,this._sectionDirty=!1,this._yaml="",this._savedYaml="",this._load.start());let t=this._device?.board_id??null;t&&t!==this._loadedBoardId?(this._loadedBoardId=t,this._board=null,this._platformReady=!1,this._loadBoard(t)):!t&&(null!==this._loadedBoardId&&(this._loadedBoardId=null,this._board=null),(null!==this._device||this._devicesLoaded)&&(this._platformReady=!0))}_readStoredLayout(){let e=localStorage.getItem("esphome-editor-layout");return"both"===e||"left"===e||"right"===e?e:null}async _loadPreferences(){let e=this._readStoredLayout();e&&(this._layout=e);try{let t=await this._api.getPreferences();this._navCollapsed=!t.navigator_visible,e||null!==this._readStoredLayout()||(this._layout=(0,z.r5)(t.device_editor_layout))}catch(e){console.warn("Failed to load device preferences:",e)}if(this._pendingReveal){this._pendingReveal=!1;let e=C("central",this._layout,this._isMobile);e&&(this._layout=e),this.isConnected&&this._updateUrl()}}async _loadBoard(e){try{let t=await (0,R.tK)(this._api,e);this._loadedBoardId===e&&(this._board=t,this._platformReady=!0)}catch(t){console.error("Failed to load board:",t),this._loadedBoardId===e&&(this._board=null,this._platformReady=!0)}}_maybeResolveLineFromUrl(){if(void 0===this._pendingUrlLine||!this._yaml)return;let e=this._pendingUrlLine;this._pendingUrlLine=void 0;let t=function(e,t,i){let o=G(e,t);if(!o||null!==i&&i!==o.sectionKey)return null;let a=(0,N.L2)(e,o.range.fromLine);return{...o,fieldPath:a?(0,L.es)(a.path):[],yamlPath:a?.indexedPath}}(this._yaml,e,this._selectedSection);t&&(this._selectedSection=t.sectionKey,this._selectedFromLine=t.sectionFromLine,this._focusFieldPath=t.fieldPath,this._focusYamlPath=t.yamlPath,this._setHighlight(t.range,!0))}_boardDisagreement(){if(!this._board)return null;let e=(0,W.GP)(this._yaml);return e&&(0,W.nW)(e,this._board)?e:null}async _installChipDisagreement(){if(!this._board)return!1;let e=(0,W.GP)(this._yaml);if(null===e)return!1;try{return await (0,A.Qt)(this._api,e,this._board)}catch(e){return console.warn("Board disagreement check failed:",e),(0,B.KQ)(this._localize("device.board_check_failed")),!1}}_openBoardReselect(e={}){return(0,A.UM)(this._boardReselectDialog,{configuration:this.id,yaml:this._yaml,...e})}async _maybePromptBoardReselect(){if(this._suppressBoardPrompt)return;let e=this._boardDisagreement();if(!e)return;let t=`${this.id}|${e.platform}|${e.board}|${e.variant}`;this._boardPromptShownFor===t||(this._boardPromptShownFor=t,await this._openBoardReselect().catch(e=>(console.error("Board reselect prompt failed:",e),!1))||this._boardPromptShownFor!==t||(this._boardPromptShownFor=null))}_jumpToErrorLine(e){if(!e||e<1)return;"left"===this._layout&&this._cacheLayout("both"),this._setHighlight({fromLine:e,toLine:e},!0,!0);let t=G(this._yaml,e);t&&(this._selectedSection=t.sectionKey)}_resolveValidationPrompt(e){let t=this._pendingValidationResolve;this._pendingValidationResolve=null,t?.(e)}_showActiveJobProgress(){return(0,D.xW)(this._activeJobs,this.id,this._commandDialog,this._devices,this._localize)}render(){let e=this._device?.friendly_name||this._device?.name||this.id||this._localize("dashboard.create_device"),t=this._isMobile?!this._drawerOpen:this._navCollapsed,i=this._localize("device.back");return(0,s.qy)`
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
        ${"ready"===this._load.state&&this._isMobile?this._renderNavigator("drawer-nav"):s.s6}
      </div>

      <div class="page">
        <div
          class=${(0,l.H)({"layout-grid":!0,"nav-collapsed":this._navCollapsed,"load-state":"ready"!==this._load.state})}
          @section-toggle=${this._onSectionToggle}
          @section-reveal=${this._onSectionReveal}
          @layout-change=${this._onLayoutChange}
          @yaml-change=${this._onYamlChange}
          @yaml-diagnostics=${this._onYamlDiagnostics}
          @yaml-cursor-line=${this._onYamlCursorLine}
          @yaml-user-edit=${this._onYamlUserEdit}
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
          @install-device=${this._saveThenInstall}
          @update-device=${this._saveThenUpdate}
        >
          ${(0,n.P)("ready"===this._load.state?this._renderEditor(e,t,i):this._renderLoadState())}
        </div>
        <esphome-unsaved-changes-dialog
          @discard=${this._onUnsavedDiscard}
          @save=${this._onUnsavedSave}
          @cancel=${this._onUnsavedCancel}
        ></esphome-unsaved-changes-dialog>
        <esphome-command-dialog
          @request-show-logs-after-install=${this._onPostInstallShowLogs}
          @request-open-editor=${this._onRequestOpenEditor}
          @request-download-firmware=${this._onRequestDownloadFirmware}
        ></esphome-command-dialog>
        <esphome-firmware-install-dialog
          @request-show-logs-after-install=${this._onPostInstallShowLogs}
          @clean-build=${this._onCleanBuild}
          @request-open-editor=${this._onRequestOpenEditor}
          @request-change-board=${this._onRequestChangeBoard}
        ></esphome-firmware-install-dialog>
        <esphome-logs-dialog></esphome-logs-dialog>
        <esphome-install-method-dialog
          ?open=${this._installCtrl.installMethodOpen}
          .deviceState=${this._installCtrl.deviceState}
          .deviceTargetPlatform=${this._installCtrl.deviceTargetPlatform}
          .platformInstalls=${this._installCtrl.platformInstalls}
          .deviceCurrentAddress=${this._installCtrl.deviceCurrentAddress}
          .canFlashBootloader=${this._installCtrl.canFlashBootloader}
          .neverFlashed=${this._installCtrl.neverFlashed}
          .otaNeedsUsb=${this._installCtrl.otaNeedsUsb}
          .mode=${this._installCtrl.methodMode}
          @close=${this._installCtrl.onInstallMethodClose}
          @select-method=${this._installCtrl.onInstallMethodSelect}
        ></esphome-install-method-dialog>
        <esphome-yaml-validation-dialog
          .errorCount=${this._validationErrorCount}
          .firstErrorLine=${this._validationFirstLine}
          .firstErrorCol=${this._validationFirstCol}
          .firstErrorMessage=${this._validationFirstMessage}
          .firstErrorFile=${this._validationFirstFile}
          @save-anyway=${this._onValidationSaveAnyway}
          @goto=${this._onValidationGoTo}
          @cancel=${this._onValidationCancel}
        ></esphome-yaml-validation-dialog>
        <esphome-board-reselect-dialog></esphome-board-reselect-dialog>
      </div>
    `}_onSectionToggle(e){let{index:t}=e.detail,i=new Set;this._openSections.has(t)||i.add(t),this._openSections=i,this._updateUrl()}_onSectionReveal(e){let{index:t}=e.detail;this._openSections.has(t)||(this._openSections=new Set([t]),this._updateUrl())}_onNavSectionShow(e){let t={core:0,components:1,automations:2}[e.detail.section];if(void 0===t)return;let i=new Set([t]);this._openSections=i,this._updateUrl(),this._drawerOpen=!0,this._navCollapsed&&(this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{}))}_onLayoutChange(e){this._persistLayout(e.detail)}_cacheLayout(e){this._layout=e,localStorage.setItem("esphome-editor-layout",e)}_persistLayout(e){this._cacheLayout(e),this._api.updatePreferences({device_editor_layout:(0,z.jr)(e)}).catch(e=>console.warn("Failed to persist device layout preference:",e))}_renderNavigator(e){let t="desktop-nav"===e?!this._navCollapsed:this._drawerOpen;return(0,s.qy)`<esphome-device-navigator
      class=${e}
      .tourAnchorId=${t?"nav":void 0}
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
      .errorCounts=${this._navErrorCounts(this._backendErrors,this._heldUnknownInstance)}
    ></esphome-device-navigator>`}_renderEditor(e,t,i){return(0,s.qy)` ${!this._isMobile?this._renderNavigator("desktop-nav"):s.s6}
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
        .focusYamlPath=${this._focusYamlPath}
        .backendErrors=${this._instanceBackendErrors(this._backendErrors,this._selectedSection,this._selectedFromLine)}
        .justCreated=${this._justCreated}
        @just-created-dismiss=${this._dismissJustCreated}
        @request-install=${this._saveThenInstall}
        @request-migrate-config=${this._onMigrateConfig}
        @request-disable-mac-suffix=${this._onDisableMacSuffix}
        @request-enable-ota-encryption=${this._onEnableOtaEncryption}
        @request-drop-ota-encryption-key=${this._onDropOtaEncryptionKey}
        @goto-line=${this._onEditorGoToLine}
        @change-board=${this._onChangeBoard}
        @open-logs=${this._onEditorOpenLogs}
        @clean-build=${this._onEditorCleanBuild}
        @analyze-memory=${this._onEditorAnalyzeMemory}
        ?hasUnsavedEdits=${this._isDirty}
        ?saving=${this._saving}
        ?showModified=${!!this._device&&(0,T.EJ)(this._device)}
        ?showUpdate=${!!this._device&&(0,T.QH)(this._device)}
        .installedVersion=${this._device?.runtime_state.deployed_version??""}
        .availableVersion=${this._device?.current_version??""}
        .webUiUrl=${this._device?(0,H.Gv)(this._device):""}
        ?busy=${this._activeJobs.has(this.id)}
      >
        ${t||this._selectedSection?(0,s.qy)`<div slot="header-start" class="header-start-group">
                ${t?(0,s.qy)`<button
                        type="button"
                        class="ghost-icon-btn nav-toggle-btn"
                        ${(0,S.Wf)("nav-toggle")}
                        @click=${this._onNavExpand}
                        title=${this._localize("device.show_navigator")}
                        aria-label=${this._localize("device.show_navigator")}
                      >
                        <wa-icon library="mdi" name="menu"></wa-icon>
                      </button>`:s.s6}
                ${this._selectedSection?(0,s.qy)`<button
                        class="ghost-icon-btn back-btn"
                        @click=${this._onBack}
                        title=${i}
                        aria-label=${i}
                      >
                        <wa-icon library="mdi" name="arrow-left"></wa-icon>
                      </button>`:s.s6}
              </div>`:s.s6}
      </esphome-device-editor>`}_renderLoadState(){let e="loading"===this._load.state,t="missing"===this._load.state;return(0,K.C)({loading:e,loadingMessage:this._localize("device.loading_config"),loadingLead:(0,s.qy)`<wa-spinner></wa-spinner>`,error:e?null:this._localize(t?"device.load_not_found":"device.load_failed"),errorActions:()=>(0,s.qy)`<wa-button
          size="small"
          @click=${t?()=>(0,U.oo)("/"):this._load.retry}
        >
          ${this._localize(t?"device.back_to_dashboard":"command.retry")}
        </wa-button>`,content:()=>s.s6})}_setYaml(e){this._yaml=e,"active"===this._errorHighlight&&(this._errorHighlight="edited")}_onYamlChange(e){this._setYaml(e.detail.value),this._retryPendingFieldLine()}_onYamlDiagnostics(e){if(e.detail.configuration!==this.id)return;"edited"===this._errorHighlight&&this._setHighlight(null,!1);let t=(0,L.cU)(this._yaml,e.detail.mapped);(t.length||this._backendErrors.length)&&(this._backendErrors=t)}_onYamlCursorLine(e){this._clearPendingFieldLine(),this._cancelCursorSwitch();let t=e.detail,i=(0,u.tO)(this._yaml,t.line,t.path??[]);if(!i)return;if(t.viaEdit||t.pointer||this._isSelected((0,u.gU)(i),i.fromLine))return void this._applyCursorMove(t,i);let o=this._selectedSection,a=this._selectedFromLine,s=(0,u.gU)(i);this._cursorSwitchTimer=setTimeout(()=>{if(this._cursorSwitchTimer=null,o!==this._selectedSection||a!==this._selectedFromLine)return;let e=(0,u.fD)(this._yaml,s,i.fromLine);void 0!==e&&this._applyCursorMove(t,{...i,fromLine:e})},100)}_isSelected(e,t){return e===this._selectedSection&&t===this._selectedFromLine}_cancelCursorSwitch(){null!==this._cursorSwitchTimer&&(clearTimeout(this._cursorSwitchTimer),this._cursorSwitchTimer=null)}_applyCursorMove(e,t){let i=e.path??[],o=(0,L.es)(i),a=(0,u.gU)(t);if(this._isSelected(a,t.fromLine)){this._focusFieldPath=o,this._focusYamlPath=e.indexedPath;return}if(!0===e.viaEdit&&null!==this._knownTopLevelKeys&&!this._knownTopLevelKeys.has(t.key)){this._heldUnknownInstance=(0,L.pA)(a,t.fromLine);return}this._heldUnknownInstance=null,this._selectedSection=a,this._selectedFromLine=t.fromLine,this._focusFieldPath=o,this._focusYamlPath=e.indexedPath,this._clearBlockHighlight(),this._updateUrl(),this._kickSectionFlush()}_focusedSection(){if(!this._selectedSection)return;let e=(0,u.MT)(this._yaml);return(void 0!==this._selectedFromLine?e.find(e=>e.fromLine===this._selectedFromLine):void 0)??e.find(e=>(0,u.gU)(e)===this._selectedSection)}_highlightFieldLine(e){let t=this._focusedSection(),i=t?(0,u.of)(this._yaml,t,e):null;return null!==i&&this._setHighlight({fromLine:i,toLine:i},!0),{section:t,found:null!==i}}_onFieldFocus(e){let t=this._focusedFieldPath=e.detail.path;if(!t.length)return;let{section:i,found:o}=this._highlightFieldLine(t);o?this._clearPendingFieldLine():(this._pendingFieldLine=!0,this._pendingFieldSection={section:this._selectedSection,fromLine:this._selectedFromLine},this._setHighlight(i?{fromLine:i.fromLine,toLine:i.toLine}:null,void 0!==i))}_retryPendingFieldLine(){if(this._pendingFieldLine&&this._focusedFieldPath?.length){if(this._pendingFieldSection?.section!==this._selectedSection||this._pendingFieldSection?.fromLine!==this._selectedFromLine)return void this._clearPendingFieldLine();this._highlightFieldLine(this._focusedFieldPath).found&&this._clearPendingFieldLine()}}_clearPendingFieldLine(){this._pendingFieldLine=!1,this._pendingFieldSection=void 0}_onYamlHighlight(e){this._setHighlight(e.detail.range,e.detail.scroll)}_onYamlUserEdit(){this._clearBlockHighlight()}_clearBlockHighlight(){this._highlightRange&&"none"===this._errorHighlight&&this._setHighlight(null,!1)}_setHighlight(e,t,i=!1){this._highlightRange=e,this._scrollToHighlight=t,this._errorHighlight=i&&null!==e?"active":"none"}_onYamlUpdated(e){let{configuration:t,yaml:i,basedOn:o}=e.detail;if(t===this.id){if(o!==this._yaml){this._savedYaml=i,this._rebaseSupersededDelete(e.detail);return}this._setYaml(i),this._savedYaml=i,this._repinSelection(i)}}_repinSelection(e){if(!this._selectedSection)return;let t=(0,u.fD)(e,this._selectedSection,this._selectedFromLine);t!==this._selectedFromLine&&(void 0!==this._pendingFieldSection&&this._pendingFieldSection.fromLine===this._selectedFromLine&&(void 0===t?this._clearPendingFieldLine():this._pendingFieldSection.fromLine=t),this._selectedFromLine=t,this.isConnected&&this._updateUrl())}async _rebaseSupersededDelete(e){let t=this._yaml,i=null;try{i=await async function(e,t,i){let o,{removed:a,configuration:s}=e;if("automation"===a.kind){let{yaml_diff:e}=await i.deleteAutomation(s,a.location,t);o=(0,_.lX)(t,e)}else{let e=(0,u.fD)(t,a.sectionKey,a.fromLine);if(void 0===e)return null;o=(0,p.ju)(t,a.sectionKey,e)}let r=v(e.basedOn,e.yaml),n=v(t,o);return null===r||null===n||0===n.length||r.join("\n")!==n.join("\n")?null:o}(e,t,this._api)}catch(e){console.error("Re-base of superseded delete failed:",e),i=null}if(e.configuration===this.id){if(null!==i&&t===this._yaml){this._setYaml(i),this._repinSelection(i);return}(0,B.uA)(this._localize("device.delete_superseded"),{description:this._localize("device.delete_superseded_detail")})}}_onYamlDraft(e){if(e.detail.configuration!==this.id)return;let t=e.detail.node;e.detail.basedOn!==this._yaml&&t!==this._activeSection?(0,B.uA)(this._localize("device.draft_superseded"),{description:this._localize("device.draft_superseded_detail")}):(this._setYaml(e.detail.yaml),this._repinSelection(e.detail.yaml),this._retryPendingFieldLine())}async _onMigrateConfig(){let e,t=this.id,i=this._yaml;try{({yaml_diff:e}=await this._api.migrateConfig(i))}catch(e){t===this.id&&(0,B.UG)(this._localize("device.config_migration_failed"),{description:e instanceof Error?e.message:String(e)});return}if(t!==this.id)return;if(i!==this._yaml)return void(0,B.uA)(this._localize("device.draft_superseded"),{description:this._localize("device.draft_superseded_detail")});if(!e)return void(0,B.uA)(this._localize("device.config_migration_none"));let o=(0,_.lX)(i,e);this._setYaml(o),this._repinSelection(o),(0,B.VX)(this._localize("device.config_migration_applied"))}_onDisableMacSuffix(){this._applyDraftRewrite(es,"device.mac_suffix_applied")}_onEnableOtaEncryption(){this._applyDraftRewrite(eu,"device.ota_encryption_applied")}_onDropOtaEncryptionKey(){this._applyDraftRewrite(e_,"device.ota_encryption_key_dropped")}_applyDraftRewrite(e,t){let i=e(this._yaml);null!==i&&(this._setYaml(i),this._repinSelection(i),(0,B.VX)(this._localize(t)))}_onSectionSelect(e){let{sectionKey:t,fromLine:i}=e.detail;if(this._heldUnknownInstance=null,this._cancelCursorSwitch(),null!==t&&this._isSelected(t,i)){this._drawerOpen=!1;return}this._drawerOpen=!1;let o=this._selectedSection,a=this._selectedFromLine;null===t?this._sectionHistory=[]:null!==o&&(this._sectionHistory=[...this._sectionHistory,{key:o,fromLine:a}]),this._selectedSection=t,this._selectedFromLine=null!==t&&void 0!==i?(0,u.fD)(this._yaml,t,i):void 0,this._focusFieldPath=void 0,this._focusYamlPath=void 0,this._updateUrl(),this._kickSectionFlush()}_kickSectionFlush(){try{Promise.resolve(this._activeSection?.flushPending()).catch(e=>console.error("Outgoing section flush failed:",e))}catch(e){console.error("Outgoing section flush failed:",e)}}_kickKnownKeys(){this._catalogKicked||(this._catalogKicked=!0,(0,J.ak)(this._api).then(e=>{this._knownTopLevelKeys=(0,X.Bt)(e),null===this._knownTopLevelKeys&&(this._catalogKicked=!1)}))}_readUrlParam(e,t){var i;return i=window.location.search,new URLSearchParams(i).get(e)??t}_readUrlLine(){let e=new URLSearchParams(window.location.search).get("line");if(!e)return;let t=Number(e);return Number.isNaN(t)?void 0:t}_readUrlSections(){let e;return(e=new URLSearchParams(window.location.search).get("open"))?e.split(",").map(Number).filter(e=>!Number.isNaN(e)):[]}_updateUrl(){var e,t,i;let o,a,s,r=(e=window.location.search,t=window.location.pathname,i={selectedSection:this._selectedSection,selectedFromLine:this._selectedFromLine,openSections:this._openSections},(o=new URLSearchParams(e)).delete("reveal"),i.selectedSection?(o.set("section",i.selectedSection),void 0!==i.selectedFromLine?o.set("line",String(i.selectedFromLine)):o.delete("line")):(o.delete("section"),o.delete("line")),(a=[...i.openSections]).length>0?o.set("open",a.join(",")):o.delete("open"),s=o.toString(),`${t}${s?`?${s}`:""}`);window.history.replaceState(window.history.state,"",r)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._devicesLoaded=!1,this._apiConnected=!1,this._activeJobs=new Map,this.id="",this._justCreated=!1,this._layout="both",this._tourLayout=new F.d_(this,()=>this._layout,e=>{this._layout=e}),this._openSections=new Set(this._readUrlSections()),this._providedResolvedComponents=[],this._providedResolvedPlatforms=[],this._board=null,this._platformReady=!1,this._loadedBoardId=null,this._highlightRange=null,this._scrollToHighlight=!1,this._errorHighlight="none",this._selectedSection=this._readUrlParam("section",null),this._pendingUrlLine=this._readUrlLine(),this._pendingReveal=null!==this._readUrlParam("reveal",null),this._backendErrors=[],this._heldUnknownInstance=null,this._cursorSwitchTimer=null,this._knownTopLevelKeys=null,this._catalogKicked=!1,this._instanceBackendErrors=(0,d.A)(L.Oq),this._baseErrorCounts=(0,d.A)(L.lt),this._pendingFieldLine=!1,this._sectionHistory=[],this._drawerOpen=!1,this._navCollapsed=!1,this._isMobile=window.matchMedia("(max-width: 900px)").matches,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._yaml="",this._load=new E.r(this,{api:()=>this._api,connected:()=>this._apiConnected,configuration:()=>this.id,attempts:4,timeoutMs:3e4,commit:e=>{this._yaml=e,this._savedYaml=e},onReady:()=>this._maybeResolveLineFromUrl(),onApiError:e=>e.errorCode===c.O.NOT_FOUND?"missing":void 0}),this._savedYaml="",this._saving=!1,this._activeSection=null,this._sectionDirty=!1,this._suppressBoardPrompt=!1,this._boardPromptShownFor=null,this._validationErrorCount=0,this._validationFirstLine=0,this._validationFirstCol=0,this._validationFirstMessage="",this._validationFirstFile="",this._onPostInstallShowLogs=(0,Z.ei)(()=>this._logsDialog,()=>this._localize),this._installCtrl=this._createInstallController(),this._unsavedGuard=new Y._,this._leaveGuard=new U.KO(this,{confirmLeave:()=>this._confirmLeave(),isDirty:()=>(this._kickSectionFlush(),this._isDirty||(this._activeSection?.lastFlushFailed??!1)),url:()=>`/device/${this.id}`}),this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._confirmLeave=async()=>{let e=!1,t=!this._saving&&null===this._pendingValidationResolve;t&&(this._saving=!0);try{await this._activeSection?.flushPending()}catch(t){console.error("Section flush before leave failed:",t),e=!0}finally{t&&(this._saving=!1)}let i=()=>this._activeSection?.lastFlushFailed??!1;return await this._unsavedGuard.run({dirty:e||i()||this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>!!await this._saveYaml()&&(!i()||((0,B.UG)(this._localize("device.leave_last_change_unsaved")),!1))})},this._onBeforeUnload=e=>{this._kickSectionFlush(),(this._isDirty||this._activeSection?.lastFlushFailed)&&(e.preventDefault(),e.returnValue="")},this._onKeydown=e=>{if("Escape"!==e.key||e.defaultPrevented)return;let t=e.composedPath()[0];if(!(0,V.t)(t)){if(this._drawerOpen){e.preventDefault(),this._drawerOpen=!1;return}e.preventDefault(),(0,U.SJ)()}},this._dismissJustCreated=()=>{this._justCreated=!1},this._onChangeBoard=async e=>{let t=e.detail?.boardId,i=this._device;if(t&&i&&t!==i.board_id){if(this._isDirty)return void(0,B.UG)(this._localize("device.change_board_unsaved"));await (0,A.Xt)(this._api,this._localize,i.configuration,t)}},this._pendingValidationResolve=null,this._saveYaml=async()=>{if(this._saving||null!==this._pendingValidationResolve)return!1;this._saving=!0;try{if(await this._activeSection?.flushPending(),!this._isYamlDirty)return!0;if(this.id)try{let e=(0,Q.mL)(this.id,this._yaml)??await this._api.validateYaml(this.id,this._yaml),t=(0,ey.tu)(e,this._yaml,this._localize);if(t.count>0){this._validationErrorCount=t.count,this._validationFirstLine=t.first?.line??0,this._validationFirstCol=t.first?.col??0,this._validationFirstMessage=t.first?.message??"";let e=t.first?.file??null;return this._validationFirstFile=e&&this.id&&!(0,ey.lg)(e,this.id)?(0,ey.P8)(e):"",new Promise(e=>{this._pendingValidationResolve=e,this._yamlValidationDialog.open()})}}catch(e){console.debug("[save-yaml] validate_yaml failed, saving anyway:",e)}return await this._doSaveYaml()}finally{this._saving=!1}},this._doSaveYaml=async()=>{let e=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let t=!0;try{await this._api.updateConfig(this.id,this._yaml)}catch(i){(i instanceof Error?i.message:"").includes("timed out")||(t=!1,this._savedYaml=e,console.error("Failed to save YAML:",i))}finally{this._saving=!1}t&&"none"!==this._errorHighlight&&this._setHighlight(null,!1);let i=t?"device.yaml_saved":"device.yaml_save_error";return(t?B.VX:B.UG)(this._localize(i)),t&&this._maybePromptBoardReselect(),t},this._onRequestChangeBoard=e=>{let t=e.detail.configuration===this.id&&!this._isDirty;(0,A.UM)(this._boardReselectDialog,{configuration:e.detail.configuration,yaml:t?this._yaml:void 0})},this._onValidationSaveAnyway=async()=>{let e=await this._doSaveYaml();this._resolveValidationPrompt(e)},this._onValidationGoTo=e=>{this._jumpToErrorLine(e.detail.line),this._resolveValidationPrompt(!1)},this._onEditorGoToLine=e=>{this._jumpToErrorLine(e.detail.line)},this._onValidationCancel=()=>{this._resolveValidationPrompt(!1)},this._onValidateClick=()=>{this._device&&this._commandDialog.openForDevice(this._device,"validate")},this._installAfterSave=async e=>{let t;if(this._showActiveJobProgress())return;this._suppressBoardPrompt=!0;try{t=await this._saveYaml()}catch(e){console.error("Failed to save before install:",e),(0,B.UG)(this._localize("device.yaml_save_error"));return}finally{this._suppressBoardPrompt=!1}if(!t)return;let i=async()=>{try{await e()}catch(e){console.error("Install entry failed:",e),(0,B.UG)(this._localize("device.install_start_failed"))}};await this._installChipDisagreement()&&await this._openBoardReselect({onApplied:()=>void i()})||await i()},this._saveThenInstall=()=>this._installAfterSave(this._installCtrl.onInstall),this._saveThenUpdate=()=>this._installAfterSave(this._installCtrl.onUpdate),this._onCleanBuild=e=>{this._commandDialog.openForDevice(e.detail,"clean")},this._onEditorOpenLogs=()=>this._installCtrl.onLogs(),this._onEditorCleanBuild=()=>{this._device&&this._commandDialog.openForDevice(this._device,"clean")},this._onEditorAnalyzeMemory=()=>{this._device&&this._commandDialog.openForDevice(this._device,"analyze_memory")},this._onRequestOpenEditor=e=>{e.stopPropagation(),e.detail.configuration!==this._device?.configuration&&(0,U.oo)(`/device/${encodeURIComponent(e.detail.configuration)}`)},this._onRequestDownloadFirmware=e=>this._firmwareDialog.downloadArtifacts(e.detail),this._onBack=()=>{this._heldUnknownInstance=null;let e=this._sectionHistory.length?this._sectionHistory[this._sectionHistory.length-1]:null;e?(this._sectionHistory=this._sectionHistory.slice(0,-1),this._selectedSection=e.key,this._selectedFromLine=(0,u.fD)(this._yaml,e.key,e.fromLine)):(this._selectedSection=null,this._selectedFromLine=void 0),this._setHighlight(null,!1),this._updateUrl(),this._kickSectionFlush()},this._onNavExpand=()=>{if(this._isMobile){this._drawerOpen=!0;return}this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{})},this._onNavCollapse=()=>{if(this._isMobile){this._drawerOpen=!1;return}this._navCollapsed=!0,this._api.updatePreferences({navigator_visible:!1}).catch(()=>{})},this._onSectionMount=e=>{this._activeSection=e.detail.node,this._sectionDirty=e.detail.node.dirty},this._onSectionUnmount=e=>{this._activeSection===e.detail.node&&(this._activeSection=null,this._sectionDirty=!1)},this._onSectionDirtyChange=e=>{this._activeSection===e.detail.node&&(this._sectionDirty=e.detail.dirty)}}}oE.styles=[M.G9,q.I,eb],oA([(0,o.Fg)({context:P.$F,subscribe:!0}),(0,r.wk)()],oE.prototype,"_localize",void 0),oA([(0,o.Fg)({context:P.xJ,subscribe:!0}),(0,r.wk)()],oE.prototype,"_devices",void 0),oA([(0,o.Fg)({context:P.UL,subscribe:!0}),(0,r.wk)()],oE.prototype,"_devicesLoaded",void 0),oA([(0,o.Fg)({context:P.Lh,subscribe:!0}),(0,r.wk)()],oE.prototype,"_apiConnected",void 0),oA([(0,o.Fg)({context:P.Ie})],oE.prototype,"_api",void 0),oA([(0,o.Fg)({context:P.EM,subscribe:!0}),(0,r.wk)()],oE.prototype,"_activeJobs",void 0),oA([(0,r.MZ)()],oE.prototype,"id",void 0),oA([(0,r.wk)()],oE.prototype,"_justCreated",void 0),oA([(0,r.wk)()],oE.prototype,"_layout",void 0),oA([(0,r.wk)()],oE.prototype,"_openSections",void 0),oA([(0,o.Gt)({context:P.I9}),(0,r.wk)()],oE.prototype,"_providedResolvedComponents",void 0),oA([(0,o.Gt)({context:P.YY}),(0,r.wk)()],oE.prototype,"_providedResolvedPlatforms",void 0),oA([(0,r.wk)()],oE.prototype,"_board",void 0),oA([(0,r.wk)()],oE.prototype,"_platformReady",void 0),oA([(0,r.wk)()],oE.prototype,"_highlightRange",void 0),oA([(0,r.wk)()],oE.prototype,"_scrollToHighlight",void 0),oA([(0,r.wk)()],oE.prototype,"_selectedSection",void 0),oA([(0,r.wk)()],oE.prototype,"_selectedFromLine",void 0),oA([(0,r.wk)()],oE.prototype,"_focusFieldPath",void 0),oA([(0,r.wk)()],oE.prototype,"_focusYamlPath",void 0),oA([(0,r.wk)()],oE.prototype,"_backendErrors",void 0),oA([(0,r.wk)()],oE.prototype,"_heldUnknownInstance",void 0),oA([(0,r.wk)()],oE.prototype,"_sectionHistory",void 0),oA([(0,r.wk)()],oE.prototype,"_drawerOpen",void 0),oA([(0,r.wk)()],oE.prototype,"_navCollapsed",void 0),oA([(0,r.wk)()],oE.prototype,"_isMobile",void 0),oA([(0,r.wk)()],oE.prototype,"_yaml",void 0),oA([(0,r.wk)()],oE.prototype,"_savedYaml",void 0),oA([(0,r.wk)()],oE.prototype,"_saving",void 0),oA([(0,r.P)("esphome-unsaved-changes-dialog")],oE.prototype,"_unsavedDialog",void 0),oA([(0,r.wk)()],oE.prototype,"_sectionDirty",void 0),oA([(0,r.P)("esphome-command-dialog")],oE.prototype,"_commandDialog",void 0),oA([(0,r.P)("esphome-firmware-install-dialog")],oE.prototype,"_firmwareDialog",void 0),oA([(0,r.P)("esphome-logs-dialog")],oE.prototype,"_logsDialog",void 0),oA([(0,r.P)("esphome-yaml-validation-dialog")],oE.prototype,"_yamlValidationDialog",void 0),oA([(0,r.P)("esphome-board-reselect-dialog")],oE.prototype,"_boardReselectDialog",void 0),oA([(0,r.wk)()],oE.prototype,"_validationErrorCount",void 0),oA([(0,r.wk)()],oE.prototype,"_validationFirstLine",void 0),oA([(0,r.wk)()],oE.prototype,"_validationFirstCol",void 0),oA([(0,r.wk)()],oE.prototype,"_validationFirstMessage",void 0),oA([(0,r.wk)()],oE.prototype,"_validationFirstFile",void 0),oE=oA([(0,r.EM)("esphome-page-device")],oE)},9877(e,t,i){var o=i(3234);let a={left:o.GN.VISUAL,right:o.GN.YAML,both:o.GN.BOTH},s={[o.GN.VISUAL]:"left",[o.GN.YAML]:"right",[o.GN.BOTH]:"both"};i.d(t,{},{OU:function(e){return e===o.Bk.YAML?"yaml":"form"},aQ:function(e){return"yaml"===e?o.Bk.YAML:o.Bk.VISUAL},jr:function(e){return a[e]},r5:function(e){return s[e]??"both"},wS:function(e,t){return t&&"both"===e?"right":e}})}}]);
//# sourceMappingURL=180.64dcf7d1fc5d03fd.js.map