"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[35],{7038(e,t,i){i.r(t),i.d(t,{ESPHomePageDevice:()=>nS});var o,a=i(9104),r=i(289),n=i(5077),s=i(9356),l=i(1502),d=i(918),c=i(6668),h=i(8159),p=i(8267),u=i(2854),m=i(1079);class v{hostConnected(){}get deviceState(){return this._host.device?.runtime_state.state??c.g.UNKNOWN}get deviceTargetPlatform(){return this._host.device?.target_platform??""}get deviceCurrentAddress(){return this._host.device?.ip||this._host.device?.address||""}get canFlashBootloader(){return(0,h.A)(this._host.device)}get neverFlashed(){return(0,p.g)(this._host.device)}_logsHost(e){return{api:this._host.api,logsDialog:e,localize:this._host.localize}}_openCommand(e,t,i,o){"install"===t&&this._host.openActiveJobProgress()||this._host.commandDialog?.openForDevice(e,t,{port:i,...o})}constructor(e){this.installMethodOpen=!1,this.methodMode="install",this.onInstall=()=>{!this._host.device||this._host.openActiveJobProgress()||(this.methodMode="install",this.installMethodOpen=!0,this._host.requestUpdate())},this.onLogs=()=>{let e=this._host.device,t=this._host.logsDialog;e&&t&&(0,u.r)(this._logsHost(t),e,()=>{this.methodMode="logs",this.installMethodOpen=!0,this._host.requestUpdate()})},this.onUpdate=()=>{let e=this._host.device;e&&this._openCommand(e,"install")},this.onInstallMethodClose=()=>{this.installMethodOpen=!1,this.methodMode="install",this._host.requestUpdate()},this.onInstallMethodSelect=e=>{let t=this._host.device,i=this.methodMode;if(this.installMethodOpen=!1,this.methodMode="install",this._host.requestUpdate(),!t)return;let{method:o,port:a}=e.detail;if("logs"===i){let e=this._host.logsDialog;if(!e)return;(0,u.e)(this._logsHost(e),t,o,a);return}this._host.openActiveJobProgress()||(0,m.D)(o,a,{device:t,firmwareDialog:this._host.firmwareDialog,openInstall:(e,i)=>this._openCommand(t,"install",e,i)})},this._host=e,e.addController(this)}}var g=i(8451),f=i(7895),_=i(1556),b=i(3140),y=i(2812),w=i(9460),$=i(9363),x=i(5084),k=i(157),z=i(9877),C=i(2439),q=i(3632),S=i(1529),A=i(2063),M=i(1093),P=i(8360),E=i(9317),F=i(3682),L=i(9328);function O(e,t){if(void 0===t||!Number.isInteger(t)||t<1||!e)return null;let i=(0,L.VN)(e,t);return i?{sectionKey:(0,L.gU)(i),sectionFromLine:i.fromLine,range:{fromLine:t,toLine:t}}:null}var R=i(332),T=i(9757),D=i(2761),I=i(1254),B=i(6689),j=i(5091);let K=(0,n.AH)`
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
`;i(9218),i(9968),i(4584);var U=i(6734),Z=i(3330),N=i(4818);let V="esphome-editor-split-ratio",H=e=>Math.min(.75,Math.max(.25,e)),G=e=>{try{localStorage.setItem(V,String(e))}catch{}},W=(0,n.AH)`
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
`;var Y=i(6048);i(9577),i(2522),i(8768);var J=i(5343);function Q(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}class X extends n.WF{render(){if(this._darkMode?this.setAttribute("dark",""):this.removeAttribute("dark"),this.oldValue===this.newValue)return(0,n.qy)`<div class="empty">${this._localize("device.diff_no_changes")}</div>`;let e=function(e,t){let i=e.split("\n"),o=t.split("\n"),a=i.length,r=o.length,n=[];for(let e=0;e<=a;e++)n.push(new Uint32Array(r+1));for(let e=1;e<=a;e++)for(let t=1;t<=r;t++)n[e][t]=i[e-1]===o[t-1]?n[e-1][t-1]+1:Math.max(n[e-1][t],n[e][t-1]);let s=[],l=a,d=r;for(;l>0||d>0;)l>0&&d>0&&i[l-1]===o[d-1]?(s.push({type:"context",oldLine:l,newLine:d,content:i[l-1]}),l--,d--):d>0&&(0===l||n[l][d-1]>=n[l-1][d])?(s.push({type:"add",newLine:d,content:o[d-1]}),d--):(s.push({type:"remove",oldLine:l,content:i[l-1]}),l--);return s.reverse()}(this.oldValue,this.newValue);return(0,n.qy)`
      <table>
        <tbody>
          ${e.map(e=>this._renderLine(e))}
        </tbody>
      </table>
    `}_renderLine(e){let t="add"===e.type?"+":"remove"===e.type?"-":" ",i="remove"===e.type?e.oldLine:e.newLine;return(0,n.qy)`
      <tr class=${e.type}>
        <td class="gutter">${i??(0,n.qy)`&nbsp;`}</td>
        <td class="marker">${t}</td>
        <td class="content">${e.content||n.s6}</td>
      </tr>
    `}constructor(...e){super(...e),this._darkMode=(0,J.yk)(),this._localize=e=>e,this.oldValue="",this.newValue=""}}X.styles=(0,n.AH)`
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
  `,Q([(0,a.Fg)({context:_.B6,subscribe:!0}),(0,s.wk)()],X.prototype,"_darkMode",void 0),Q([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],X.prototype,"_localize",void 0),Q([(0,s.MZ)()],X.prototype,"oldValue",void 0),Q([(0,s.MZ)()],X.prototype,"newValue",void 0),X=Q([(0,s.EM)("esphome-yaml-diff")],X),i(4022);var ee=i(6254),et=i(8259),ei=i(9728);function eo(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({broom:r.mdiBroom,"check-circle-outline":r.mdiCheckCircleOutline,"dots-vertical":r.mdiDotsVertical,"open-in-new":r.mdiOpenInNew,"text-box-outline":r.mdiTextBoxOutline});class ea extends ei.o{render(){let e=this._localize("device.actions_menu");return(0,n.qy)`
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
      ${this._open?(0,n.qy)`
              <div class="backdrop" @click=${this._close}></div>
              <!-- Opens upward, so DOM order inverts distance from the
                   trigger: frequent actions (Logs) last / nearest the
                   click, rare ones (Clean build) first / furthest. -->
              <div class="menu" role="menu">
                <div
                  class="menu-item ${this.busy?"menu-item--disabled":""}"
                  role="menuitem"
                  tabindex=${this.busy?"-1":"0"}
                  aria-disabled=${this.busy?"true":"false"}
                  title=${this.busy?this._localize("dashboard.action_clean_build_busy"):n.s6}
                  @click=${this.busy?void 0:this._onCleanBuild}
                  @keydown=${this.busy?void 0:this._onItemKeydown}
                >
                  <wa-icon library="mdi" name="broom"></wa-icon>
                  <span class="menu-item-label"
                    >${this._localize("dashboard.action_clean_build")}</span
                  >
                </div>
                <div class="menu-divider" role="separator"></div>
                ${this.webUiUrl?(0,et.w)(this.webUiUrl,this._localize,{className:"menu-item menu-item--link",onClick:this._close,withLabel:!0,role:"menuitem"}):n.s6}
                <div
                  class="menu-item ${this.validateDisabled?"menu-item--disabled":""}"
                  role="menuitem"
                  tabindex=${this.validateDisabled?"-1":"0"}
                  aria-disabled=${this.validateDisabled?"true":"false"}
                  title=${this.validateDisabled?this._localize("device.validate_disabled_pending"):n.s6}
                  @click=${this.validateDisabled?void 0:this._onValidate}
                  @keydown=${this.validateDisabled?void 0:this._onItemKeydown}
                >
                  <wa-icon library="mdi" name="check-circle-outline"></wa-icon>
                  <span class="menu-item-label"
                    >${this._localize("device.validate")}</span
                  >
                </div>
                <div
                  class="menu-item"
                  role="menuitem"
                  tabindex="0"
                  @click=${this._onLogs}
                  @keydown=${this._onItemKeydown}
                >
                  <wa-icon library="mdi" name="text-box-outline"></wa-icon>
                  <span class="menu-item-label"
                    >${this._localize("device.show_logs")}</span
                  >
                </div>
              </div>
            `:n.s6}
    `}constructor(...e){super(...e),this._localize=e=>e,this.busy=!1,this.validateDisabled=!1,this.webUiUrl="",this._onLogs=()=>{this._close(),this._emit("open-logs")},this._onValidate=()=>{this.validateDisabled||(this._close(),this._emit("validate"))},this._onCleanBuild=()=>{this.busy||(this._close(),this._emit("clean-build"))}}}ea.styles=[b.G,ee.x,(0,n.AH)`
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
    `],eo([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],ea.prototype,"_localize",void 0),eo([(0,s.MZ)({type:Boolean})],ea.prototype,"busy",void 0),eo([(0,s.MZ)({type:Boolean,attribute:"validate-disabled"})],ea.prototype,"validateDisabled",void 0),eo([(0,s.MZ)({attribute:!1})],ea.prototype,"webUiUrl",void 0),ea=eo([(0,s.EM)("esphome-device-actions-menu")],ea);var er=i(8763),en=i(6910);let es=(0,n.AH)`
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
`,el="cog-outline",ed="memory",ec="arrow-decision-outline";(0,M.C)({[el]:r.mdiCogOutline,[ed]:r.mdiMemory,[ec]:r.mdiArrowDecisionOutline}),i(751),i(8197);let eh=(0,n.AH)`
  .intro {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    margin: 0 0 var(--wa-space-m) 0;
    line-height: 1.5;
  }
  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
  }
  .required {
    color: var(--esphome-error, #d92d20);
  }
  .error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }
`;var ep=i(5660),eu=i(325),em=i(8283),ev=i(3074);let eg=(0,n.AH)`
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
`;function ef(e){return e.replace(/ (Component|Configuration)$/,"")||e}var e_=i(6570);function eb(e){return e.name?e.name:e.title?L.TM.has(ey(e.component_id))?ef(e.title):e.title:e.id}function ey(e){return(0,e_.iZ)(e).domain}function ew(e,t){let i=e.parent_id?t.find(t=>t.id===e.parent_id):void 0;return i?`${e.component_id} \xb7 ${eb(i)}`:e.component_id}function e$(e){return!e.is_entity_container}function ex(e){return e.find(e$)}function ek(e,t){return t?e.filter(e=>e.id===t.id||e.parent_id===t.id):e}function ez(e,t){if(!t||!e$(t))return[];let i=ey(t.component_id);return e.filter(e=>!e.is_device_level&&(e.applies_to.includes(t.component_id)||e.applies_to.includes(i)))}var eC=i(8175);function eq(){return{trigger_id:null,trigger_params:{},actions:[]}}function eS(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[o,...a]=t;if(0===a.length){if(void 0===i||""===i){let t={...e};return delete t[o],t}return{...e,[o]:i}}let r=e[o]&&"object"==typeof e[o]&&!Array.isArray(e[o])?e[o]:{};return{...e,[o]:eS(r,a,i)}}function eA(e,t,i){if(t<0||t>=e.length)return e;let o=e.slice();return o[t]=i,o}function eM(e,t){if(t<0||t>=e.length)return e;let i=e.slice();return i.splice(t,1),i}function eP(e,t,i){if(t<0||i<0||t>=e.length||i>=e.length||t===i)return e;let o=e.slice();return[o[t],o[i]]=[o[i],o[t]],o}function eE(e){return(0,eC.wr)(e)?Number(e):null}function eF(e){switch(e.kind){case"device_on":return void 0===e.index?`automation:device_on:${e.trigger}`:`automation:device_on:${e.trigger}:${e.index}`;case"component_on":return void 0===e.index?`automation:component_on:${e.component_id}:${e.trigger}`:`automation:component_on:${e.component_id}:${e.trigger}:${e.index}`;case"component_action":return`automation:component_action:${e.component_id}:${e.field}`;case"script":return`automation:script:${e.id}`;case"interval":return`automation:interval:${e.index}`;case"light_effect":return`automation:light_effect:${e.component_id}:${e.index}`;case"api_action":return`automation:api_action:${e.action_name}`}}function eL(e,t){let i=e.split("\n"),o=t.fromLine-1,a=Math.max(0,t.toLine-t.fromLine+1),r=t.replacement.endsWith("\n")?t.replacement.slice(0,-1):t.replacement,n=""===r?[]:r.split("\n");return[...i.slice(0,o),...n,...i.slice(o+a)].join("\n")}function eO(e){if(!e.startsWith("automation:"))return null;let t=e.split(":");switch(t[1]){case"device_on":if(!t[2])return null;if(3===t.length)return{kind:"device_on",trigger:t[2]};if(4===t.length){let e=eE(t[3]);return null===e?null:{kind:"device_on",trigger:t[2],index:e}}return null;case"component_on":if(!t[2]||!t[3])return null;if(4===t.length)return{kind:"component_on",component_id:t[2],trigger:t[3]};if(5===t.length){let e=eE(t[4]);return null===e?null:{kind:"component_on",component_id:t[2],trigger:t[3],index:e}}return null;case"component_action":return 4===t.length&&t[2]&&t[3]?{kind:"component_action",component_id:t[2],field:t[3]}:null;case"script":return t[2]?{kind:"script",id:t[2]}:null;case"interval":{let e=Number(t[2]);return Number.isFinite(e)?{kind:"interval",index:e}:null}case"light_effect":{let e=Number(t[3]);return t[2]&&Number.isFinite(e)?{kind:"light_effect",component_id:t[2],index:e}:null}case"api_action":return t[2]?{kind:"api_action",action_name:t[2]}:null;default:return null}}function eR(e,t,i,o){let a=eL(t,o);e.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})),e.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:eF(i)},bubbles:!0,composed:!0}))}i(1687),i(4063),i(2216);let eT=(0,n.AH)`
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
`;function eD(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}let eI={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1};class eB extends n.WF{render(){let{plan:e,order:t}=this._plan();return 0===t.length?(0,n.qy)`<p class="error" role="status">
        ${this._localize("device.automation_target_no_components")}
      </p>`:(0,n.qy)`<div class="field">
      <label class="field-label" id="component-target-label">
        ${this._localize("device.automation_wizard_pick_component")}
      </label>
      <div
        class="component-list"
        role="radiogroup"
        aria-labelledby="component-target-label"
        @keydown=${e=>this._onKeydown(e,t)}
      >
        ${e.map(e=>{if(!("header"in e))return this._renderChoice(e,t);let i=`component-group-${e.header.id}`;return(0,n.qy)`<div
            class="component-group-wrap"
            role="group"
            aria-labelledby=${i}
          >
            <p class="component-group" id=${i}>
              ${eb(e.header)}
              <span class="component-group-id">(${e.header.component_id})</span>
            </p>
            ${e.subs.map(e=>this._renderChoice(e,t))}
          </div>`})}
      </div>
    </div>`}_plan(){let e=new Set(this.devices.filter(e=>e.is_entity_container).map(e=>e.id)),t=new Map;for(let i of this.devices){if(!i.parent_id||!e.has(i.parent_id))continue;let o=t.get(i.parent_id)??[];o.push(i),t.set(i.parent_id,o)}let i=[],o=[];for(let a of this.devices)if(a.is_entity_container){let e=t.get(a.id)??[];if(0===e.length)continue;i.push({header:a,subs:e}),o.push(...e.map(e=>e.id))}else a.parent_id&&e.has(a.parent_id)||(i.push(a),o.push(a.id));return{plan:i,order:o}}_renderChoice(e,t){let i=e.id===this.value,o=i||!t.includes(this.value)&&t[0]===e.id;return(0,n.qy)`<div
      class="component-choice ${i?"component-choice--selected":""}"
      role="radio"
      aria-checked=${i?"true":"false"}
      aria-disabled=${this.disabled?"true":"false"}
      data-id=${e.id}
      tabindex=${o?"0":"-1"}
      @click=${()=>this._select(e.id)}
    >
      <span class="component-choice-name truncate">${eb(e)}</span>
      <span class="component-domain">${e.component_id}</span>
    </div>`}_onKeydown(e,t){if(this.disabled||0===t.length)return;let i=e.target?.closest(".component-choice"),o=i?.dataset.id??null;if("Enter"===e.key||" "===e.key){o&&(e.preventDefault(),this._select(o));return}let a=eI[e.key]??0;if(0===a)return;e.preventDefault();let r=o?t.indexOf(o):-1,n=t[(r+a+t.length)%t.length];this._select(n),this.updateComplete.then(()=>{let e=this.shadowRoot?.querySelector(`.component-choice[data-id="${n}"]`);e?.focus()})}_select(e){this.disabled||(0,Z.r)(this,"component-change",{componentId:e})}constructor(...e){super(...e),this._localize=e=>e,this.devices=[],this.value="",this.disabled=!1}}function ej(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}eB.styles=[b.G,U.U,eT],eD([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],eB.prototype,"_localize",void 0),eD([(0,s.MZ)({attribute:!1})],eB.prototype,"devices",void 0),eD([(0,s.MZ)()],eB.prototype,"value",void 0),eD([(0,s.MZ)({type:Boolean})],eB.prototype,"disabled",void 0),eB=eD([(0,s.EM)("esphome-component-target-picker")],eB);class eK extends n.WF{open(e){this._prefilled=void 0!==e,this._kind=e?.kind??"device_on",this._componentId=e?.kind==="component_on"?e.componentId:"",this._prefillComponentId=this._componentId,this._triggerId=null,this._intervalValue="",this._intervalUnit="s",this._error="",this._dialog.open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration){this._loading=!0;try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml);let e=this._prefillContainer();e&&(this._componentId=this._available.devices.find(t=>t.parent_id===e.id)?.id??""),this._preselectUniqueTrigger()}catch(e){this._error=(0,em.u)(e)}finally{this._loading=!1}}}_prefillContainer(){if(!this._prefilled||"component_on"!==this._kind||!this._prefillComponentId)return;let e=this._available?.devices.find(e=>e.id===this._prefillComponentId);return e?.is_entity_container?e:void 0}render(){let e=this.boardName?this._localize("device.add_automation_dialog_title",{name:this.boardName}):this._localize("device.add_automation");return(0,n.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      ${this._loading&&!this._available?(0,n.qy)`<div style="text-align: center; padding: 32px;">
              <wa-spinner></wa-spinner>
            </div>`:this._renderForm()}
    </esphome-base-dialog>`}_renderForm(){let e=this._filteredTriggers(),t="interval"===this._kind,i=!this._prefilled,o=this._prefillContainer(),a="component_on"===this._kind&&(!this._prefilled||!!o),r=!!o&&!ex(ek(this._available?.devices??[],o));return(0,n.qy)`
      <p class="intro">
        ${(0,en.Gc)(this._localize("device.automation_header_description"))}
      </p>
      ${i?(0,n.qy)`<div class="field">
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
                <wa-option
                  value="component_on"
                  ?selected=${"component_on"===this._kind}
                >
                  ${this._localize("device.automation_target_component")}
                </wa-option>
                <wa-option value="interval" ?selected=${"interval"===this._kind}>
                  ${this._localize("device.automation_target_interval")}
                </wa-option>
              </wa-select>
            </div>`:n.s6}
      ${r?(0,n.qy)`<p class="field-desc">
              ${this._localize("device.automation_container_no_entities")}
            </p>`:(0,n.qy)`
              ${a?this._renderComponentRow(o):n.s6}
              ${"interval"===this._kind?this._renderIntervalRow():n.s6}
              ${!t?this._renderTriggerRow(e):n.s6}
            `}
      ${this._error?(0,n.qy)`<p class="error" role="alert">${this._error}</p>`:n.s6}
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
    `}_renderComponentRow(e){let t=ek(this._available?.devices??[],e);return(0,n.qy)`<esphome-component-target-picker
      .devices=${t}
      .value=${this._componentId}
      ?disabled=${this._saving}
      @component-change=${e=>this._onComponentChange(e.detail.componentId)}
    ></esphome-component-target-picker>`}_renderIntervalRow(){return(0,n.qy)`<div class="field">
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
          ${["us","ms","s","min","h","d"].map(e=>(0,n.qy)`<wa-option value=${e} ?selected=${e===this._intervalUnit}
                >${this._localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
    </div>`}_renderTriggerRow(e){if(0===e.length)return(0,n.qy)`<p class="error">
        ${this._localize("device.automation_trigger_none_available")}
      </p>`;let t=e.find(e=>e.id===this._triggerId);return(0,n.qy)`<div class="field">
      <label class="field-label" id="trigger-label">
        ${this._localize("device.automation_wizard_pick_trigger")}
      </label>
      <wa-select
        aria-labelledby="trigger-label"
        value=${this._triggerId??""}
        ?disabled=${this._saving}
        @change=${e=>this._triggerId=e.target.value}
      >
        ${e.map(e=>(0,n.qy)`<wa-option value=${e.id} ?selected=${e.id===this._triggerId}>
              ${e.name}
            </wa-option>`)}
      </wa-select>
      ${t?.description?(0,n.qy)`<p class="field-desc">${(0,en.Gc)(t.description)}</p>`:n.s6}
    </div>`}_filteredTriggers(){let e=this._available?.triggers??[];if("device_on"===this._kind){let t=this._existingDeviceTriggers();return e.filter(e=>e.is_device_level&&(!t.has(e.id)||e.supports_list))}if("component_on"===this._kind){let t=this._available?.devices.find(e=>e.id===this._componentId),i=this._existingComponentTriggers(this._componentId);return ez(e,t).filter(e=>!i.has(this._bareTrigger(e.id))||e.supports_list)}return[]}_existingDeviceTriggers(){let e=new Set;for(let t of(0,L.vB)(this.yaml))"esphome"===t.parentKey&&t.eventKey&&e.add(t.eventKey);return e}_existingComponentTriggers(e){let t=new Set;for(let i of(0,L.vB)(this.yaml))i.id===e&&i.eventKey&&t.add(i.eventKey);return t}_bareTrigger(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_onKindChange(e){if(this._kind=e,this._triggerId=null,"component_on"===e){let e=this._available?.devices??[];this._componentId=ex(e)?.id??""}else this._componentId="";this._preselectUniqueTrigger()}_onComponentChange(e){this._componentId=e,this._triggerId=null,this._preselectUniqueTrigger()}_preselectUniqueTrigger(){let e=this._filteredTriggers();1===e.length&&(this._triggerId=e[0].id)}_canContinue(){return"interval"===this._kind?""!==this._intervalValue.trim():!!this._triggerId&&("component_on"!==this._kind||!!this._componentId)}_buildLocation(){if("device_on"===this._kind){let e=this._available?.triggers.find(e=>e.id===this._triggerId);if(e?.supports_list){let e=(0,L.vB)(this.yaml).filter(e=>"esphome"===e.parentKey&&e.eventKey===this._triggerId).length;return{kind:"device_on",trigger:this._triggerId,index:e}}return{kind:"device_on",trigger:this._triggerId}}if("component_on"===this._kind){let e=this._triggerId.indexOf("."),t=e>=0?this._triggerId.slice(e+1):this._triggerId,i=this._available?.triggers.find(e=>e.id===this._triggerId);if(i?.supports_list){let e=(0,L.vB)(this.yaml).filter(e=>e.id===this._componentId&&e.eventKey===t).length;return{kind:"component_on",component_id:this._componentId,trigger:t,index:e}}return{kind:"component_on",component_id:this._componentId,trigger:t}}return{kind:"interval",index:(0,L.vB)(this.yaml).filter(e=>"interval"===e.parentKey).length}}_catalogTriggerId(e){return"interval"===e.kind?null:this._triggerId}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new eu.T(this),this._kind="device_on",this._componentId="",this._prefillComponentId="",this._triggerId=null,this._prefilled=!1,this._intervalValue="",this._intervalUnit="s",this._available=null,this._loading=!0,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e=this._buildLocation(),t={trigger_id:this._catalogTriggerId(e),trigger_params:"interval"===this._kind?{interval:`${this._intervalValue.trim()}${this._intervalUnit}`}:{},actions:[]},{yaml_diff:i}=await this._api.upsertAutomation(this.configuration,t,e,this.yaml);eR(this,this.yaml,e,i),this._dialog.open=!1}catch(t){let e=(0,ev.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}eK.styles=[b.G,ep.z9,eh,eg],ej([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],eK.prototype,"_localize",void 0),ej([(0,a.Fg)({context:_.Ie})],eK.prototype,"_api",void 0),ej([(0,s.MZ)()],eK.prototype,"boardName",void 0),ej([(0,s.MZ)()],eK.prototype,"configuration",void 0),ej([(0,s.MZ)()],eK.prototype,"yaml",void 0),ej([(0,s.MZ)({attribute:!1})],eK.prototype,"board",void 0),ej([(0,s.wk)()],eK.prototype,"_kind",void 0),ej([(0,s.wk)()],eK.prototype,"_componentId",void 0),ej([(0,s.wk)()],eK.prototype,"_prefillComponentId",void 0),ej([(0,s.wk)()],eK.prototype,"_triggerId",void 0),ej([(0,s.wk)()],eK.prototype,"_prefilled",void 0),ej([(0,s.wk)()],eK.prototype,"_intervalValue",void 0),ej([(0,s.wk)()],eK.prototype,"_intervalUnit",void 0),ej([(0,s.wk)()],eK.prototype,"_available",void 0),ej([(0,s.wk)()],eK.prototype,"_loading",void 0),ej([(0,s.wk)()],eK.prototype,"_saving",void 0),ej([(0,s.wk)()],eK.prototype,"_error",void 0),eK=ej([(0,s.EM)("esphome-add-automation-dialog")],eK);var eU=i(6848),eZ=i(6016),eN=i(5795),eV=i(4125);function eH(e){let t=new Set;if(!e)return t;for(let i of e.split("\n")){if(!/^\s/.test(i))continue;let e=(0,eV.KJ)(i,"id");null!==e&&t.add(e)}return t}var eG=i(8851),eW=((o={}).SENSOR="sensor",o.BINARY_SENSOR="binary_sensor",o.SWITCH="switch",o.LIGHT="light",o.FAN="fan",o.COVER="cover",o.CLIMATE="climate",o.BUTTON="button",o.NUMBER="number",o.SELECT="select",o.TEXT="text",o.TEXT_SENSOR="text_sensor",o.LOCK="lock",o.VALVE="valve",o.MEDIA_PLAYER="media_player",o.SPEAKER="speaker",o.MICROPHONE="microphone",o.CAMERA="camera",o.DISPLAY="display",o.TOUCHSCREEN="touchscreen",o.OUTPUT="output",o.DATETIME="datetime",o.EVENT="event",o.UPDATE="update",o.ALARM="alarm_control_panel",o.CORE="core",o.BUS="bus",o.AUTOMATION="automation",o.OTA="ota",o.TIME="time",o.AUDIO_ADC="audio_adc",o.AUDIO_DAC="audio_dac",o.CANBUS="canbus",o.IMAGE="image",o.INFRARED="infrared",o.MEDIA_SOURCE="media_source",o.MOTION="motion",o.ONE_WIRE="one_wire",o.PACKET_TRANSPORT="packet_transport",o.RADIO_FREQUENCY="radio_frequency",o.STEPPER="stepper",o.WATER_HEATER="water_heater",o.MISC="misc",o.FEATURED="featured",o);let eY=["core","ota","update"];var eJ=i(5016),eQ=i(2930);let eX=new(i(2342)).e,e0=new Set(Object.values(eW));function e1(e,t,i){if(0===e.length)return[];let o=i??(0,eG.Zn)(t),a=(0,eG.u)(t),r=new Set;for(let e of a){let t=e.indexOf(".");-1!==t&&r.add(e.slice(t+1))}return e.filter(e=>!(0,eJ.p)(o,e)&&(e.includes(".")?!a.has(e):!(!e0.has(e)&&r.has(e))))}async function e2(e,t,i,o){let a=new Set,r=t.filter(e=>!e.includes("."));if(0===r.length)return a;let n=o.platform?(0,eJ.bk)(o.platform):void 0;return await Promise.all(r.map(async t=>{var r;let s;for(let l of(await (r=o.boardId??void 0,s=`${t}|${n??""}|${r??""}`,eX.fetch(s,()=>(0,eQ._)(e,{provides:t,platform:n??void 0,board_id:r??void 0}).then(e=>new Set(e.map(e=>e.id)))))))if((0,eJ.p)(i,l)){a.add(t);break}})),a}var e6=i(4008),e3=i(7169),e5=i(4117);async function e4(e,t){if(e._submitting)return;let i=e._selected;e._submitError="";let o=++e._depNavSeq,a=null;try{a=await (0,e5.Sn)(e._api,t,e.platform||void 0,e.board?.id??void 0)}catch{a=null}if(o===e._depNavSeq){if(i&&(e._returnTo=i,e._depDomain=t),a){var r,n,s;let o,l=i?.bus_constraints?.[t],d=l?function(e,t){let i={},o=[],a={},r=t=>e.find(e=>e.key===t),n=null,s=null;for(let[e,l]of Object.entries(t)){if("min_frequency"===e){"number"==typeof l&&(n=l);continue}if("max_frequency"===e){"number"==typeof l&&(s=l);continue}if(e.startsWith("require_")){!0===l&&o.push(`${e.slice(8)}_pin`);continue}let t=r(e);if(!t)continue;if(Array.isArray(l)){let o=t.multi_value?[]:l.filter(e=>"string"==typeof e||"number"==typeof e);if(0===o.length)continue;a[e]=o;let r=o[0],n=t.default_value;(null==n||String(n)!==String(r))&&(i[e]=t.type===e6.Hh.STRING?String(r):r);continue}let d=t.default_value;(null==d||String(d)!==String(l))&&(i[e]=t.type===e6.Hh.STRING?String(l):l)}if(null!==n||null!==s){let e=r("frequency"),t=e?.unit_options?.length?e.unit_options:["Hz"],o=(0,e3.D6)(e?.default_value,t),a=null;null===o?a=s??n:null!==s&&o>s?a=s:null!==n&&o<n&&(a=n),null!==a&&(i.frequency=(0,e3.j1)(a,t))}if(0===Object.keys(i).length&&0===o.length&&0===Object.keys(a).length)return null;let l={fields:i,required:o};return Object.keys(a).length>0&&(l.optionOverrides=a),l}(a.config_entries,l):null,c=e.board?.featured_components?.find(e=>e.component_id===a.id);r=d,n=function(e){if(!e)return null;let t={};for(let[i,o]of Object.entries(e.fields))null!==o.value&&void 0!==o.value&&(t[i]=o.value);return Object.keys(t).length>0?{fields:t,required:[]}:null}(c),e._depPrefill=r?n?{fields:{...n.fields,...r.fields},required:[...r.required,...n.required],...r.optionOverrides?{optionOverrides:r.optionOverrides}:{}}:r:n,e._selected=c?(s=a,0===(o=new Set(Object.entries(c.fields).filter(([,e])=>e.locked).map(([e])=>e))).size?s:{...s,config_entries:s.config_entries.map(e=>o.has(e.key)?{...e,locked:!0}:e)}):a;return}e._selected=null,await e.updateComplete,o===e._depNavSeq&&e._catalog?.filterByDomain(t)}}async function e8(e,t,i){let o=++e._selectionSeq,a=i??e.board?.id??void 0;try{let i=await (0,e5.Sn)(e._api,t,e.platform||void 0,a);if(o!==e._selectionSeq)return{kind:"stale"};if(!i)return{kind:"error",message:e._localize("device.add_component_load_failed")};return{kind:"ok",entry:i}}catch(t){if(o!==e._selectionSeq)return{kind:"stale"};return{kind:"error",message:(0,ev.K)(t,e._localize,"device.add_component_error")}}}let e9=(0,n.AH)`
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
`;var e7=i(271);function te(e,t){if(e.type===e6.Hh.INTEGER)return(0,e7.s)(t);if(e.type===e6.Hh.FLOAT)return tt(t);if(e.type===e6.Hh.BOOLEAN){let e=t.trim();return""===e?"":(0,eG.FY)(e)??e}return t}function tt(e){let t=e.trim();if(""===t)return"";let i=Number(t);return Number.isFinite(i)?i:t}function ti(e,t){let i={};for(let o of e){if(o.hidden)continue;let e=t[o.key];if(o.type===e6.Hh.NESTED){let t=o.config_entries??[];if(o.multi_value){let a=(0,eC.ly)(e).map(e=>ti(t,e)).filter(e=>Object.keys(e).length>0);a.length>0&&(i[o.key]=a);continue}let a=ti(t,(0,eC.qY)(e));Object.keys(a).length>0&&(i[o.key]=a);continue}if(void 0!==e){if(Array.isArray(e)){if(0===e.length)continue;i[o.key]=e;continue}if(""===e){o.required&&(i[o.key]=e);continue}o.type===e6.Hh.INTEGER&&"hex"!==o.display_format?i[o.key]=(0,e7.s)(e):o.type===e6.Hh.FLOAT?i[o.key]="number"==typeof e&&Number.isFinite(e)?e:te(o,String(e)):o.type===e6.Hh.BOOLEAN?i[o.key]="string"==typeof e?te(o,e):e:i[o.key]=e}}return i}var to=i(5957);let ta=new Set(["name"]);function tr(e,t={}){var i;let o,a={requiredOnly:e.requiredOnly,showAdvanced:e.showAdvanced,presentComponents:e.presentComponents,targetPlatform:e.board?.esphome.platform??null,rootValues:e.values,...t};return i=a.rootValues,a.rootValues=(o=e.board?.esphome)&&e.sectionKey===o.platform&&null!=o.variant?{variant:o.variant,...i}:i,a}function tn(e,t){let i=t[e.key];if(e.type===e6.Hh.NESTED)return e.multi_value?i instanceof eG.ho||Array.isArray(i)&&i.length>0:(0,eC.Qd)(i)?(e.config_entries??[]).some(e=>tn(e,i)):void 0!==i;return void 0!==i}function ts(e,t,i){let o=[];for(let a of e)if((0,to.VP)(a,t,i.presentComponents,i.targetPlatform,i.rootValues,e)&&(!a.advanced||i.showAdvanced||tn(a,t))){if(a.type===e6.Hh.NESTED){if(!a.multi_value){let e=ts(a.config_entries??[],(0,eC.qY)(t[a.key]),i),o=t[a.key],r="string"==typeof o||"number"==typeof o||"boolean"==typeof o;if(0===e.length&&!r)continue}}else if(i.requiredOnly&&!a.required&&!ta.has(a.key))continue;o.push(a)}return o}let tl=/^\*\*(Required —|Set at most one of:|Set together)/;function td(e,t,i){let o=t.filter(e=>(0,to.rf)(i[e])).length;switch(e){case"exactly_one":return 1===o;case"at_least_one":return o>=1;case"at_most_one":return o<=1;case"none_or_all":case"all_or_none":return 0===o||o===t.length}}let tc=(0,n.AH)`
  .warning-banner {
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-warning-fill-quiet, #fff7e0);
    color: var(--wa-color-warning-text-quiet, #6b4f00);
    border-left: 3px solid var(--wa-color-warning-border-loud, #f0b400);
    font-size: var(--wa-font-size-s);
  }
`,th=(0,n.AH)`
  .danger-banner {
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-danger-fill-quiet);
    border: var(--wa-border-width-s) solid var(--wa-color-danger-60);
    color: var(--wa-color-danger-text-normal);
  }

  .danger-banner wa-icon {
    flex: 0 0 auto;
    font-size: 1.25rem;
    margin-top: 0.05rem;
    color: var(--wa-color-danger-60);
  }

  .danger-banner-text {
    display: flex;
    flex-direction: column;
    gap: 3px;
    line-height: 1.4;
    min-width: 0;
  }

  .danger-banner-text > * {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-semibold);
    word-break: break-word;
  }
`;var tp=i(1480),tu=i(615);function tm(e,t){if(e.translation_key){let i=e.translation_params||void 0,o=t(e.translation_key,i);if(o&&o!==e.translation_key)return o}return e.label?e.label:e.key.split("_").map(e=>e?e[0].toUpperCase()+e.slice(1):e).join(" ")}var tv=i(2748),tg=i(7967),tf=i(355),t_=i(5413),tb=i(9470);let ty=(0,n.AH)`
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

  /* Keep the toggle's original vertical hit area (the shared base is flush). */
  .pin-advanced .disclosure-toggle {
    padding: 2px 0;
  }

  /* The shared disclosure renders the quiet toggle + panel; the bordered indent
     rail for the long-form fields is pin-specific, scoped to this disclosure's
     panel so it overrides the shared margin-only default. */
  .pin-advanced .disclosure-panel {
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
`,tw=(0,n.AH)`
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

  .field-warning {
    color: var(--esphome-warning, #d97706);
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
  /* The .substitution-note chip styles live in substitution-note.styles.js
     (pulled into fieldRendererStyles) so the automation editor can share
     them; only .secret-note is here. */
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

  /* Inline "generate a key" action stacked under the API encryption-key
     input — a quiet link-style button, not a heavy form control. */
  .generate-key {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    align-self: flex-start;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: var(--esphome-primary);
    font-size: var(--wa-font-size-2xs);
    transition: color 0.12s;
  }

  .generate-key:hover {
    text-decoration: underline;
  }

  .generate-key wa-icon {
    font-size: 14px;
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

  /* Stacks a row's input above its substitution hint while the remove
     button stays beside the input column. */
  .multi-row .multi-value-cell {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
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
     them so each row stays compact. A templatable value (Value / λ
     Lambda toggle) nests its field one level deeper under
     .templatable-field, so match that too or the label re-appears
     and offsets the input. */
  .map-row .map-value > .field > label,
  .map-row .map-value > .field > p.field-description,
  .map-row .map-value > .templatable-field > .field > label,
  .map-row .map-value > .templatable-field > .field > p.field-description {
    display: none;
  }

  .map-row .map-value > .field,
  .map-row .map-value > .templatable-field > .field {
    gap: 0;
  }

  /* A templatable value stacks its Value / λ Lambda toggle above the input
     (a full-width field column). In a compact map row that drops the input
     below the toggle and out of line with the key; lay the toggle and input
     on one row instead so the value aligns with the key input. */
  .map-row .map-value > .templatable-field {
    flex-direction: row;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .map-row .map-value > .templatable-field > .field {
    flex: 1;
    min-width: 0;
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
`,t$=(0,n.AH)`
  /* Reactive prompt for an unsatisfied cross-field constraint group
     (e.g. "set exactly one of: chipset, manual timings"). Layers the
     icon+text row and spacing onto the shared .warning-banner shape;
     shown only while the group is unmet, so a satisfied group adds no
     noise. */
  .constraint-banner {
    display: flex;
    gap: var(--wa-space-s);
    align-items: center;
    margin-bottom: var(--wa-space-m);
  }
  .constraint-banner wa-icon {
    flex-shrink: 0;
  }

  /* Header of a folded either/or constraint cluster (the .nested-group box):
     a muted caption of the rule, warm-toned while the rule is unmet. */
  .constraint-cluster-header {
    display: flex;
    gap: var(--wa-space-s);
    align-items: center;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }
  .constraint-cluster-header.unsatisfied {
    color: var(--wa-color-warning-text-quiet, currentColor);
  }
  .constraint-cluster-header wa-icon {
    flex-shrink: 0;
  }

  /* Radio chooser for an exactly-one cluster: small gap above the selected
     alternative's fields so the radios read as the box's control. */
  .constraint-cluster-radios {
    margin-bottom: var(--wa-space-2xs);
  }

  /* wa-radio's checked dot is "fill: currentColor", and its
     ":host(:state(checked)) .control { color: ... }" rule ties on specificity
     with the default "color: transparent" — the attribute selector wins the
     tie here, so the dot renders invisible. Force the activated color onto the
     control part of a checked radio (aria-checked is reliably reflected). */
  .constraint-cluster-radios wa-radio[aria-checked="true"]::part(control) {
    color: var(--wa-form-control-activated-color) !important;
  }
`,tx=(0,n.AH)`
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
`;function tk({isLambda:e,disabled:t,localize:i,onSwitch:o}){return(0,n.qy)`
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
        @click=${()=>o(!1)}
      >
        ${i("device.automation_literal")}
      </button>
      <button
        type="button"
        role="tab"
        class=${e?"active":""}
        aria-selected=${e}
        ?disabled=${t}
        @click=${()=>o(!0)}
      >
        ${i("device.automation_lambda")}
      </button>
    </div>
  `}let tz=(0,n.AH)`
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
`,tC=(0,n.AH)`
  .substitution-note {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

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

  .substitution-note code {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-2xs);
    padding: 1px 4px;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }
`,tq=[b.G,ep.z9,tc,tw,ty,tp.a,tx,t$,tz,tC];function tS(e,t){return t.disabled||e.locked}(0,M.C)({"alert-circle-outline":r.mdiAlertCircleOutline,"auto-fix":r.mdiAutoFix,"code-braces":r.mdiCodeBraces,"key-variant":r.mdiKeyVariant,"lock-outline":r.mdiLockOutline});let tA=e=>JSON.stringify(e),tM=e=>{try{let t=JSON.parse(e);if(Array.isArray(t))return t.map(String)}catch{}return e?e.split("."):[]};function tP(e,t,i){if(!(0,t_.RB)(e))return n.s6;let o=(0,t_.rq)(e,t);if((0,t_.RB)(o)){let e=i("device.substitution_unresolved_hint");return(0,n.qy)`<span
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
      <span>${i("device.substitution_unresolved")}</span>
    </span>`}let a=i("device.substitution_resolves_to");return(0,n.qy)`<span
    class="substitution-note"
    role="note"
    aria-label=${`${a}: ${o}`}
    title=${a}
  >
    <wa-icon library="mdi" name="code-braces"></wa-icon>
    <code>${o}</code>
  </span>`}function tE(e,t){return tm(e,t.localize)}function tF(e,t){return e.help_link?(0,n.qy)`<a
    class="help-button"
    href=${e.help_link}
    target="_blank"
    rel="noreferrer"
    title=${t.localize("device.docs")}
  >
    <wa-icon library="mdi" name="open-in-new"></wa-icon>
  </a>`:n.s6}function tL(e,t,i={}){var o,a;let r,s,{includeHelpLink:l=!0}=i;return(0,n.qy)`
    <label class="field-label">
      ${tE(e,t)}
      ${e.required?(0,n.qy)`<span class="required">*</span>`:n.s6}
      ${e.locked?(0,n.qy)`<wa-icon
              class="lock-icon"
              library="mdi"
              name="lock-outline"
              title=${t.localize("device.field_locked_by_board")}
            ></wa-icon>`:n.s6}
      ${l&&e.help_link?tF(e,t):n.s6}
    </label>
    ${o=e,a=t,r=o.description??"",(s=a.reactiveConstraintKeys?.has(o.key)?function(e){if(!e.startsWith("**"))return e;let t=e.split("\n\n"),i=0;for(;i<t.length&&tl.test(t[i].trim());)i++;return t.slice(i).join("\n\n").trim()}(r):r)?(0,n.qy)`<p class="field-description">${(0,en.Gc)(s)}</p>`:n.s6}
  `}function tO(e,t){let i=t.errorAt(e);return(0,tv.O)(i?t.localize(i.code,i.params):void 0)}function tR(e,t,i,o,a=n.s6){return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)} ${o} ${a} ${tO(t,i)}
    </div>
  `}function tT(e,t,i,o){return(0,eC.k4)(o)?null:tI(e,t,i)}function tD(e,t,i,o){return"string"==typeof o?tB(e,"text",t,i):tI(e,t,i)}function tI(e,t,i){return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <p class="field-description">${i.localize("device.value_yaml_only")}</p>
      ${tO(t,i)}
    </div>
  `}function tB(e,t,i,o){let a,r=o.getAt(i),s=tT(e,i,o,r);if(s)return s;let l=String(r??""),d=null!==o.errorAt(i),c=String(e.default_value??""),h=tS(e,o),p="password"===t||(0,tg.Un)(o.sectionKey,e.key),u=(0,tf.D)(l),m=p&&null!==u,v=p?(0,tg.WA)(o.sectionKey,e.key,o.deviceName??"","password"===t,i):[],g=p?(0,n.qy)`<esphome-secret-picker
        ?full=${m}
        .disabled=${h}
        .fieldLabel=${tE(e,o)}
        .selectedKey=${u??""}
        .value=${l}
        .deviceName=${o.deviceName??""}
        .recommendedKeys=${v}
        @secret-selected=${e=>o.emitChange(i,e.detail.value)}
      ></esphome-secret-picker>`:n.s6,f=(0,tu.hp)(o.sectionKey,i)&&!m&&!h&&!(0,t_.R_)(l)&&!(0,tu.lk)(l),_=f?(0,n.qy)`<button
        type="button"
        class="generate-key"
        @click=${()=>o.emitChange(i,(0,tu.My)())}
      >
        <wa-icon library="mdi" name="auto-fix"></wa-icon>
        <span>${o.localize("device.generate_encryption_key")}</span>
      </button>`:n.s6,b=e=>m?g:p||f?(0,n.qy)`<div class="field-input-row">
            ${e}${g}${_}
          </div>`:e,y=g===n.s6?null===(a=(0,tf.D)(l))?n.s6:(0,n.qy)`<span class="secret-note">
    <wa-icon library="mdi" name="key-variant"></wa-icon>
    <span>${o.localize("device.value_from_secret")}</span>
    <code>${a}</code>
  </span>`:n.s6,w="password"===t?n.s6:tP(l,o.substitutions,o.localize);if(e.suggestions&&e.suggestions.length>0)return tj(e,i,l,d,h,o);if("password"===t){let t=(0,n.qy)`<esphome-password-input
      .value=${l}
      .invalid=${d}
      .disabled=${h}
      .placeholder=${c}
      @password-input-change=${e=>o.emitChange(i,e.detail.value)}
    ></esphome-password-input>`;return(0,n.qy)`
      <div class="field" data-field-key=${tA(i)}>
        ${tL(e,o)} ${b(t)} ${y}
        ${tO(i,o)}
      </div>
    `}let $=(0,tb.td)(l),x=(0,n.qy)`<input
    type=${t}
    autocomplete="off"
    class=${d?"invalid":""}
    .value=${$?(0,tb.kk)(l):l}
    ?disabled=${h}
    placeholder=${c}
    @input=${t=>{let a=t.target.value,r=$?(0,tb.pV)(a):a;o.emitChange(i,te(e,r))}}
  />`;return(0,n.qy)`
    <div class="field" data-field-key=${tA(i)}>
      ${tL(e,o)} ${b(x)} ${y} ${w}
      ${tO(i,o)}
    </div>
  `}function tj(e,t,i,o,a,r){let s=i.toLowerCase(),l=String(e.default_value??"");return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,r)}
      <wa-select
        class=${o?"invalid":""}
        ?disabled=${a}
        placeholder=${l}
        @change=${i=>r.emitChange(t,te(e,i.target.value))}
      >
        ${(e.suggestions??[]).map(e=>{let t=String(e);return(0,n.qy)`<wa-option value=${t} ?selected=${t.toLowerCase()===s}
            >${t}</wa-option
          >`})}
      </wa-select>
      ${tO(t,r)}
    </div>
  `}function tK(e,t,i,o={}){let a=i.scopeValues(t);return(o.includeAdvanced?ts(e.config_entries??[],a,tr(i,{showAdvanced:!0,rootValues:i.scopeValues([])})):i.filterRenderable(e.config_entries??[],a)).map(e=>i.renderEntry(e,[...t,e.key]))}function tU(e,t,i){let o=new Map(t.map(e=>[e.key,e])),a=e=>{let t=o.get(e);return t?tE(t,i):e},r=new Set,n=[];for(let i of e){let e=o.get(i)?.group;if(!e){n.push(a(i));continue}if(r.has(e))continue;r.add(e);let s=t.filter(t=>t.group===e).map(e=>a(e.key));n.push(s.length>1?`(${s.join(", ")})`:s[0])}return n.join(", ")}function tZ(e,t){let i=new Map(e.members.map(e=>[e.key,e]));return(e.cardinality?.keys??[]).flatMap(o=>{let a=i.get(o);if(!a)return[];let r=a.group?e.members.filter(e=>e.group===a.group):[a];return[{id:r[0].key,members:r,label:r.map(e=>tE(e,t)).join(", ")}]})}function tN(e,t){let i=t.scopeValues([]),o=t.board?.esphome.platform??null,a=!e.cardinality||td(e.cardinality.kind,e.cardinality.keys,i),r=td("all_or_none",e.inclusiveKeys,i),s=!a&&e.cardinality?{kind:e.cardinality.kind,keys:e.cardinality.keys,satisfied:!1}:r?{kind:e.cardinality?.kind??"all_or_none",keys:e.cardinality?.keys??e.inclusiveKeys,satisfied:!0}:{kind:"all_or_none",keys:e.inclusiveKeys,satisfied:!1},l=t.localize(`device.constraint_${s.kind}`,{keys:tU(s.keys,t.entries,t)}),d=e.members.filter(e=>void 0!==t.getAt([e.key])||(0,to.VP)(e,i,t.presentComponents,o,void 0,t.entries));return d.length?(0,n.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${tA([e.members[0].key])}
    >
      <div class="constraint-cluster-header ${s.satisfied?"":"unsatisfied"}">
        ${s.satisfied?n.s6:(0,n.qy)`<wa-icon library="mdi" name="alert-circle-outline"></wa-icon>`}
        <span>${l}</span>
      </div>
      <div class="nested-fields">
        ${d.map(e=>t.renderEntry(e,[e.key]))}
      </div>
    </div>
  `:n.s6}let tV="__none__";function tH(e,t,i,o){let a=function(e){let t=new Map;for(let i of e)if(i.exclusive_group){let e=t.get(i.exclusive_group)??[];e.push(i),t.set(i.exclusive_group,e)}let i=new Set,o=[];for(let a of e)a.exclusive_group?i.has(a.exclusive_group)||(i.add(a.exclusive_group),o.push(t.get(a.exclusive_group))):o.push(a);return o}(e),{clusters:r,memberKeys:n}=function(e,t){let i=new Map(e.map(e=>[e.key,e])),o=new Map;for(let t of e)t.group&&!t.exclusive_group&&o.set(t.group,[...o.get(t.group)??[],t.key]);let a=[],r=new Set;for(let n of o.values()){let o=new Set(n),s=t.find(e=>e.keys.some(e=>o.has(e)));if(s)for(let e of s.keys)i.get(e)?.exclusive_group||o.add(e);let l=e.filter(e=>o.has(e.key));l.forEach(e=>r.add(e.key));let d=s?s.keys.filter(e=>l.some(t=>t.key===e)).length:0;a.push({members:l,cardinality:d>=2?s:void 0,inclusiveKeys:n})}return{clusters:a,memberKeys:r}}(e,i),s=new Map(r.map(e=>[e.members[0].key,e])),l=new Set(ts(e.filter(e=>!e.exclusive_group&&!n.has(e.key)),t,o));return{ordered:a,clusters:r,memberKeys:n,clusterByFirstKey:s,visible:l}}function tG(e,t){let{entries:i,requiredGroups:o,values:a,presentComponents:r,targetPlatform:n,formatKeys:s}=e,l=[],d=new Map(i.map(e=>[e.key,e])),c=e=>e.some(e=>{let t=d.get(e);return void 0!==t&&(void 0!==(0,eC.O6)(a,[e])||(0,to.VP)(t,a,r,n,void 0,i))});for(let e of o)!e.keys.some(e=>t.has(e))&&c(e.keys)&&(td(e.kind,e.keys,a)||l.push({kind:e.kind,keys:s(e.keys)}));let h=new Map;for(let e of i)e.group&&h.set(e.group,[...h.get(e.group)??[],e.key]);for(let e of h.values())!e.some(e=>t.has(e))&&c(e)&&(td("all_or_none",e,a)||l.push({kind:"all_or_none",keys:s(e)}));return l}function tW(e,t,i){return tr({requiredOnly:!0,showAdvanced:!1,presentComponents:i,board:t,values:e})}function tY(e){let{entries:t,component:i,board:o,yaml:a,prefillReference:r,prefillFields:n,restoredValues:s,localize:l}=e,d=function e(t,i,o,a=!1){let r={};for(let n of t){if(n.type===e6.Hh.NESTED){let t=e(n.config_entries??[],i,o,a);n.required&&null!=n.platform_type&&void 0===t.name&&void 0===t.id&&(t.name=tm(n,o)),Object.keys(t).length>0&&(r[n.key]=t);continue}if(n.required||a&&n.from_preset){if(n.references_component&&!n.locked){let e=(0,e_.Zm)(i,n.references_component,[]),t=(a&&n.from_preset&&"string"==typeof n.default_value&&e.some(e=>e.id===n.default_value)?n.default_value:void 0)??(0,e_.z)(e,i)?.id;void 0!==t?r[n.key]=n.multi_value?[t]:t:n.multi_value&&n.required&&(r[n.key]=[]);continue}null!=n.default_value?r[n.key]=n.multi_value?Array.isArray(n.default_value)?[...n.default_value]:[String(n.default_value)]:n.default_value:n.multi_value&&n.required&&(r[n.key]=[])}}return r}(t,a,l,(0,eN.sO)(i.id)),c=d;if(t.find(e=>"id"===e.key&&e.type===e6.Hh.ID)&&void 0===c.id){let e=function(e,t,i){let o=!(0,eN.sO)(e)&&e.includes(".");if(!t&&!o)return null;let a=e.toLowerCase().replace(/[^a-z0-9_]+/g,"_"),r=1,n=`${a}_${r}`;for(;i.has(n);)r++,n=`${a}_${r}`;return n}(i.id,i.multi_conf,eH(a));null!==e&&(c={...c,id:e})}if(c=function(e,t,i,o){if(!i?.pins?.length||e.includes("."))return o;let a=o;for(let o of t){if(o.type!==e6.Hh.PIN||void 0!==a[o.key])continue;let t=o.key.toLowerCase().replace(/_(pin|gpio)$/,""),r=`${e}_${t}`,n=i.pins.find(e=>e.features.includes(r));n&&(a={...a,[o.key]:n.gpio})}return a}(i.id,t,o,c),s&&(c={...c,...s}),r){let e=function e(t,i,o,a={}){for(let r of t){if(r.type===e6.Hh.NESTED){let t=e(r.config_entries??[],i,[...o,r.key],a);if(t)return t;continue}if(r.references_component===i){let e=[...o,r.key];if(void 0!==(0,eC.O6)(a,e))continue;return e}}return null}(t,r.domain,[],d);e&&(c=(0,eC.Oe)(c,e,r.id))}return n&&(c={...c,...n}),c}let tJ=new Set(["adc","dac","ota"]);function tQ(e){return e?"featured"===e?"Recommended":e.split("_").filter(e=>e.length>0).map(e=>tJ.has(e.toLowerCase())?e.toUpperCase():e[0].toUpperCase()+e.slice(1)).join(" "):""}var tX=i(9023);class t0{hostConnected(){this._unsubscribe=(0,e5.Ej)(()=>{this._host.requestUpdate()})}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}resolve(e){return(0,e5.CQ)(e,this._getPlatform())?.name??e}kickoff(e){let t=this._getApi();if(!t)return;let i=this._getPlatform();for(let o of e)void 0===(0,e5.CQ)(o,i)&&(0,e5.Sn)(t,o,i).catch(()=>{})}constructor(e,t,i){this._host=e,this._getApi=t,this._getPlatform=i,e.addController(this)}}function t1(e,t){if(!t?.length)return e;let i=new Set(t);return e.map(e=>i.has(e.key)&&!e.required?{...e,required:!0}:e)}function t2(e,t){return t&&0!==Object.keys(t).length?e.map(e=>{let i=t[e.key];if(!i?.length||e.multi_value)return e;let o=new Map((e.options??[]).map(e=>[e.value,e]));return{...e,options:i.map(e=>o.get(String(e))??{label:String(e),value:String(e)}),default_value:e.type===e6.Hh.STRING?String(i[0]):i[0]}}):e}let t6=(0,n.AH)`
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

  /* Deltas over the shared .btn chrome (dialogActionButtonStyles,
     layered before this module in the host's static styles): icon +
     label sit inline-centred, disabled applies to every variant (this
     form's variants are .btn-primary / .btn-secondary, not the shared
     modifier classes), and the opacity change is animated. */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
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
`;function t3(e,t){let i=e,o=!1;for(let e of t){if((0,eC.wr)(e))continue;let t=i.find(t=>t.key===e);if(!t||t.hidden)return!1;t.advanced&&(o=!0),i=t.config_entries??[]}return o}function t5(e,t){return t?e.find(e=>e.configuration===t)?.name??"":""}var t4=i(7064);let t8=(0,t4.Y)({name:"pin-registry-modes",fetch:e=>e.getPinRegistryModes(),fallback:e=>(console.warn("pin-registry-modes fetch failed; Mode flags unscoped",e),Object.create(null))});function t9(){return t8.getCached()}function t7(e){return t8.subscribe(e)}function ie(e){return t8.fetch(e)}function it(e){if(e.assignedSlot)return e.assignedSlot;if(e.parentElement)return e.parentElement;let t=e.getRootNode();return t instanceof ShadowRoot?t.host:null}class ii{hostConnected(){this._unsubscribe=this._binding.subscribe(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}hostUpdated(){if(this._kicked)return;let e=this._api();e&&(this._kicked=!0,this._binding.fetch(e))}get value(){return this._binding.getCached()}constructor(e,t,i){this._host=e,this._binding=t,this._api=i,this._kicked=!1,e.addController(this)}}class io{hostUpdated(){this._syncRadioGroups()}reset(){this._choices.clear(),this._stash.clear()}getChoice(e){return this._choices.get(e)}setChoice(e,t){this._choices.set(e,t),this._host.requestUpdate()}getStash(e,t){return this._stash.get(`${e} ${t}`)}setStash(e,t,i){this._stash.set(`${e} ${t}`,i)}clearStash(e,t){this._stash.delete(`${e} ${t}`)}async _syncRadioGroups(){let e=this._host.shadowRoot;if(!e)return;let t=[...e.querySelectorAll("wa-radio-group")];if(0!==t.length)for(let e of(await Promise.all(t.map(e=>e.updateComplete?.catch(()=>{}))),t))e.syncRadioElements?.()}constructor(e){this._host=e,this._choices=new Map,this._stash=new Map,e.addController(this)}}let ia=["focusin","pointerdown","input","change"];class ir{hostConnected(){for(let e of ia)this.host.addEventListener(e,this._onInteraction)}hostDisconnected(){for(let e of ia)this.host.removeEventListener(e,this._onInteraction)}constructor(e){this.host=e,this._onInteraction=e=>{var t,i,o;let a=e.composedPath().find(e=>e instanceof HTMLElement&&e.hasAttribute("data-field-key"));if(!a)return;let r=a.getAttribute("data-field-key")??"";if(!r.startsWith("["))return;let n=tM(r);if(!n.length)return;let{emit:s,focusedKey:l}=(t=e.type,i=tA(n),o=this._focusedKey,"change"===t?{emit:i===o,focusedKey:o}:{emit:"focusin"===t||i!==o,focusedKey:i});this._focusedKey=l,s&&this.host.dispatchEvent(new CustomEvent("field-focus",{detail:{path:n},bubbles:!0,composed:!0}))},e.addController(this)}}let is="field--highlight";function il(e){window.matchMedia?.("(prefers-reduced-motion: reduce)").matches||(e.classList.remove(is),e.offsetWidth,e.classList.add(is),e.addEventListener("animationend",()=>e.classList.remove(is),{once:!0}))}function id(e){e.scrollIntoView({block:"center"}),il(e)}class ic{maybeScroll(e){let t=this.host.focusFieldPath,i=t?.length?tA(t):void 0,o=e.has("focusFieldPath")||e.has("entries")||e.has("values")||e.has("showAdvanced"),{gate:a,scroll:r}=function(e,t,i){let{scrolledKey:o,lastFocusKey:a,tries:r}=e;t!==a&&(a=t,o=void 0,r=0);let n=!!t&&o!==t&&r<3&&i;return n&&r++,{gate:{scrolledKey:o,lastFocusKey:a,tries:r},scroll:n}}({scrolledKey:this._scrolledKey,lastFocusKey:this._lastFocusKey,tries:this._tries},i,o);this._scrolledKey=a.scrolledKey,this._lastFocusKey=a.lastFocusKey,this._tries=a.tries,r&&t?.length&&i&&this._scrollTo(t,i)}async _scrollTo(e,t){var i;let{host:o}=this;if(!o.shadowRoot)return;for(let t=1;t<e.length;t++)o.openNested(e.slice(0,t).join("."));for(let t of(i=this._gatingDecls(o.shadowRoot),i.filter(t=>t.prefix.length>0&&t.prefix.length<e.length&&t.prefix.every((t,i)=>t===e[i])).map(e=>e.key)))o.openNested(t);await o.updateComplete;let a=o.focusFieldPath;if(a&&tA(a)===t)for(let i=e.length;i>=1;i--){let a=this._find(o.shadowRoot,e.slice(0,i));if(!a)continue;a.scrollIntoView({block:"center"});let r=tA(e.slice(0,i)),n=Date.now();(r!==this._lastFlashKey||n-this._lastFlashAt>1e4)&&(this._lastFlashKey=r,this._lastFlashAt=n,il(a)),i===e.length&&(this._scrolledKey=t);return}}_gatingDecls(e){let t=[];for(let i of e.querySelectorAll("[data-reveal-for]")){let e=i.getAttribute("data-field-key");e&&t.push({prefix:tM(i.getAttribute("data-reveal-for")??""),key:e})}return t}_find(e,t){for(let i of e.querySelectorAll("[data-field-key]")){let e=tM(i.getAttribute("data-field-key")??"");if(e.length===t.length&&e.every((e,i)=>e===t[i]))return i}for(let i of e.querySelectorAll("*")){if(!i.localName.includes("-"))continue;let e=i.shadowRoot,o=e?this._find(e,t):null;if(o)return o}return null}constructor(e){this.host=e,this._lastFlashAt=0,this._tries=0}}i(8606),i(2542),i(269),i(4350);var ih=i(1959);let ip=(0,n.AH)`
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
`;function iu(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({close:r.mdiClose,magnify:r.mdiMagnify,palette:r.mdiPalette});let im=null;function iv(e){return e?e.startsWith("mdi:")?e.slice(4):e:""}class ig extends n.WF{willUpdate(e){e.has("_open")&&this._dismiss.set(this._open),e.has("value")&&!this._loaded&&iv(this.value)&&this._ensureCatalogLoaded()}async _toggle(){this.disabled||(this._open?this._close():await this._openPanel())}async _openPanel(){this._open=!0,this.setAttribute("open",""),await this._ensureCatalogLoaded(),await this.updateComplete,this._searchInput?.focus()}async _ensureCatalogLoaded(){this._loaded||(this._catalog=await (im||(im=(async()=>{let e=await Promise.resolve().then(i.bind(i,289)),t=[];for(let[i,o]of Object.entries(e)){if(!i.startsWith("mdi")||"string"!=typeof o)continue;let e=i.slice(3);if(!e)continue;let a=e.replace(/^[A-Z]/,e=>e.toLowerCase()).replace(/([A-Z])/g,"-$1").replace(/_/g,"-").toLowerCase();t.push({name:a,path:o})}return t.sort((e,t)=>e.name.localeCompare(t.name)),t})().catch(e=>(console.error("[mdi-icon-picker] failed to load catalog:",e),im=null,[])))),this._loaded=!0)}_close(){this._open=!1,this.removeAttribute("open"),this._query=""}_select(e){let t=`mdi:${e}`;this.value=t,(0,Z.r)(this,"change",{value:t}),this._close()}_clear(e){e.stopPropagation(),this.value="",(0,Z.r)(this,"change",{value:""})}_onSearchInput(e){this._query=e.target.value}_renderTriggerIcon(){let e=iv(this.value);if(!e)return(0,n.qy)`<span class="trigger-icon trigger-icon--empty">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${r.mdiPalette}></path>
        </svg>
      </span>`;let t=this._catalog.find(t=>t.name===e);return t?(0,n.qy)`<span class="trigger-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${t.path}></path>
        </svg>
      </span>`:(0,n.qy)`<span class="trigger-icon">
      <wa-icon library="mdi" name=${e} style="font-size: 16px;"></wa-icon>
    </span>`}_renderPanel(){if(!this._loaded)return(0,n.qy)`<div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="loading">Loading icons…</div>
      </div>`;let e=function(e,t){if(!t)return e.slice(0,400);let i=t.trim().toLowerCase().replace(/\s+/g,"-");if(!i)return e.slice(0,400);let o=[],a=[],r=[];for(let t of e)if(t.name===i?o.push(t):t.name.startsWith(i)?a.push(t):t.name.includes(i)&&r.push(t),o.length+a.length+r.length>=800)break;return[...o,...a,...r].slice(0,400)}(this._catalog,this._query),t=iv(this.value);return(0,n.qy)`
      <div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="search">
          <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d=${r.mdiMagnify}></path>
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
          ${0===e.length?(0,n.qy)`<div class="empty">
                  <wa-icon
                    library="mdi"
                    name="magnify"
                    style="font-size: 24px;"
                  ></wa-icon>
                  No icons match “${this._query}”
                </div>`:(0,n.qy)`<div class="grid">
                  ${e.map(e=>(0,n.qy)`
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
          ${t?(0,n.qy)`<span class="footer-name">mdi:${t}</span>`:n.s6}
        </div>
      </div>
    `}render(){let e=iv(this.value),t=`trigger${this.invalid?" invalid":""}`;return(0,n.qy)`
      <button
        type="button"
        class=${t}
        ?disabled=${this.disabled}
        @click=${this._toggle}
      >
        ${this._renderTriggerIcon()}
        <span
          class=${e?"trigger-label truncate":"trigger-label placeholder truncate"}
        >
          ${e?`mdi:${e}`:this.placeholder}
        </span>
        ${e&&!this.disabled?(0,n.qy)`<span
                class="trigger-clear"
                role="button"
                tabindex="-1"
                title="Clear"
                @click=${this._clear}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
                  <path fill="currentColor" d=${r.mdiClose}></path>
                </svg>
              </span>`:n.s6}
        <svg class="trigger-chevron" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M7,10L12,15L17,10H7Z"></path>
        </svg>
      </button>
      ${this._open?this._renderPanel():n.s6}
    `}constructor(...e){super(...e),this.value="",this.placeholder="Choose an icon…",this.invalid=!1,this.disabled=!1,this._open=!1,this._catalog=[],this._query="",this._loaded=!1,this._dismiss=new ih.J(this,()=>this._close(),{escapeTarget:document,onEscape:e=>e.stopPropagation()})}}function i_(e,t,i){return t||i?(0,n.qy)`<span class="option-stack">
    <span class="option-label">${e}</span>
    ${t?(0,n.qy)`<small class="option-description-note">${t}</small>`:n.s6}
    ${i?(0,n.qy)`<small class="option-default-note">${i}</small>`:n.s6}
  </span>`:(0,n.qy)`<span class="option-label">${e}</span>`}ig.styles=[ep.z9,U.U,ip],iu([(0,s.MZ)()],ig.prototype,"value",void 0),iu([(0,s.MZ)()],ig.prototype,"placeholder",void 0),iu([(0,s.MZ)({type:Boolean})],ig.prototype,"invalid",void 0),iu([(0,s.MZ)({type:Boolean})],ig.prototype,"disabled",void 0),iu([(0,s.wk)()],ig.prototype,"_open",void 0),iu([(0,s.wk)()],ig.prototype,"_catalog",void 0),iu([(0,s.wk)()],ig.prototype,"_query",void 0),iu([(0,s.wk)()],ig.prototype,"_loaded",void 0),iu([(0,s.P)(".search-input")],ig.prototype,"_searchInput",void 0),ig=iu([(0,s.EM)("esphome-mdi-icon-picker")],ig);let ib=(0,n.AH)`
  :host {
    display: block;
  }

  .control {
    position: relative;
    display: block;
  }

  /* Leave room for the chevron sitting over the input's right edge. */
  input {
    padding-right: 34px;
  }

  .chevron {
    position: absolute;
    top: 0;
    right: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 32px;
    padding: 0;
    background: transparent;
    border: 0;
    color: var(--wa-color-text-quiet);
    font-size: 18px;
    cursor: pointer;
  }

  .chevron:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  .listbox {
    max-height: 280px;
    overflow-y: auto;
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    box-shadow: var(--wa-shadow-m);
    padding: var(--wa-space-2xs);
  }

  .option {
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
    cursor: pointer;
  }

  .option--active {
    background: var(--esphome-tint, var(--wa-color-surface-border));
  }

  .option-label {
    display: block;
  }
`;function iy(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(7816),(0,M.C)({"chevron-down":r.mdiChevronDown});class iw extends n.WF{render(){let e=this._filtered,t=this._open?this._query:this.value,i=this._open&&e.length>0,o=i&&this._active>=0&&this._active<e.length?`option-${this._active}`:n.s6;return(0,n.qy)`
      <wa-popup placement="bottom-start" sync="width" distance="4" ?active=${i}>
        <div slot="anchor" class="control">
          <input
            type="text"
            class=${this.invalid?"invalid":""}
            role="combobox"
            aria-autocomplete="list"
            aria-invalid=${this.invalid?"true":n.s6}
            aria-expanded=${i?"true":"false"}
            aria-controls=${i?"listbox":n.s6}
            aria-activedescendant=${o}
            aria-label=${this.label||n.s6}
            .value=${t}
            placeholder=${this.placeholder}
            ?disabled=${this.disabled}
            autocomplete="off"
            spellcheck="false"
            @focus=${this._open_}
            @input=${this._onInput}
            @keydown=${this._onKeyDown}
            @blur=${this._close}
          />
          <button
            class="chevron"
            type="button"
            tabindex="-1"
            ?disabled=${this.disabled}
            aria-hidden="true"
            @mousedown=${this._preventBlur}
            @click=${this._toggle}
          >
            <wa-icon library="mdi" name="chevron-down"></wa-icon>
          </button>
        </div>
        ${i?(0,n.qy)`<div
                id="listbox"
                class="listbox"
                role="listbox"
                @mousedown=${this._preventBlur}
              >
                ${e.map((e,t)=>(0,n.qy)`<div
                      id="option-${t}"
                      class="option truncate ${t===this._active?"option--active":""}"
                      role="option"
                      aria-selected=${e.value===this.value?"true":"false"}
                      @mousedown=${this._preventBlur}
                      @click=${()=>this._select(e)}
                      @mouseenter=${()=>this._active=t}
                    >
                      ${i_(e.label,e.description,this._isDefault(e)?this.defaultNote:void 0)}
                    </div>`)}
              </div>`:n.s6}
      </wa-popup>
    `}_isDefault(e){return""!==this.defaultNote&&""!==this.defaultValue&&e.value.toLowerCase()===this.defaultValue.toLowerCase()}get _filtered(){if(!this._dirty)return this.options;let e=this._query.trim().toLowerCase();return e?this.options.filter(t=>t.value.toLowerCase().includes(e)||t.label.toLowerCase().includes(e)||t.description?.toLowerCase().includes(e)):this.options}_select(e){this.value=e.value,this._query=e.value,this._emit(e.value),this._close()}_emit(e){this.dispatchEvent(new CustomEvent("options-combobox-change",{detail:{value:e},bubbles:!1,composed:!1}))}_scrollActiveIntoView(){this.updateComplete.then(()=>this._activeOption?.scrollIntoView({block:"nearest"}))}constructor(...e){super(...e),this.options=[],this.value="",this.placeholder="",this.disabled=!1,this.invalid=!1,this.label="",this.defaultValue="",this.defaultNote="",this._open=!1,this._query="",this._dirty=!1,this._active=-1,this._committed="",this._open_=()=>{this.disabled||this._open||(this._open=!0,this._committed=this.value,this._query=this.value,this._dirty=!1,this._active=this.options.findIndex(e=>e.value===this.value),this._active>=0&&this._scrollActiveIntoView())},this._close=()=>{this._open=!1,this._active=-1,this._dirty=!1},this._toggle=()=>{this.disabled||(this._open?this._close():(this._open_(),this._input?.focus()))},this._preventBlur=e=>e.preventDefault(),this._onInput=e=>{let t=e.target.value;this._query=t,this._dirty=!0,this._open=!0,this._active=-1,this._emit(t)},this._onKeyDown=e=>{let t=this._filtered;switch(e.key){case"ArrowDown":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active>=t.length-1?0:this._active+1,this._scrollActiveIntoView());break;case"ArrowUp":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active<=0?t.length-1:this._active-1,this._scrollActiveIntoView());break;case"Enter":this._open&&this._active>=0&&t[this._active]?(e.preventDefault(),this._select(t[this._active])):this._close();break;case"Escape":this._open&&(e.preventDefault(),e.stopPropagation(),this.value=this._committed,this._query=this._committed,this._emit(this._committed),this._close());break;case"Tab":this._close()}}}}iw.styles=[ep.z9,U.U,ib],iy([(0,s.MZ)({attribute:!1})],iw.prototype,"options",void 0),iy([(0,s.MZ)()],iw.prototype,"value",void 0),iy([(0,s.MZ)()],iw.prototype,"placeholder",void 0),iy([(0,s.MZ)({type:Boolean})],iw.prototype,"disabled",void 0),iy([(0,s.MZ)({type:Boolean})],iw.prototype,"invalid",void 0),iy([(0,s.MZ)()],iw.prototype,"label",void 0),iy([(0,s.MZ)()],iw.prototype,"defaultValue",void 0),iy([(0,s.MZ)()],iw.prototype,"defaultNote",void 0),iy([(0,s.wk)()],iw.prototype,"_open",void 0),iy([(0,s.wk)()],iw.prototype,"_query",void 0),iy([(0,s.wk)()],iw.prototype,"_dirty",void 0),iy([(0,s.wk)()],iw.prototype,"_active",void 0),iy([(0,s.P)("input")],iw.prototype,"_input",void 0),iy([(0,s.P)(".option--active")],iw.prototype,"_activeOption",void 0),iw=iy([(0,s.EM)("esphome-options-combobox")],iw);let i$="__esphome_add_new__",ix="__esphome_auto__";var ik=i(410);let iz={INPUT:{input:!0},OUTPUT:{output:!0},INPUT_PULLUP:{input:!0,pullup:!0},OUTPUT_OPEN_DRAIN:{output:!0,open_drain:!0},INPUT_PULLDOWN_16:{input:!0,pulldown:!0},INPUT_PULLDOWN:{input:!0,pulldown:!0},INPUT_OUTPUT_OPEN_DRAIN:{input:!0,output:!0,open_drain:!0}};function iC(e){let t=iz[e.toUpperCase()];return t?{...t}:null}var iq=i(1376);let iS=new WeakMap;function iA(e,t,i){let o=i.getAt(t);if(!e.multi_value&&(0,eG.$z)(o)&&("string"==typeof o||"number"==typeof o||"boolean"==typeof o))return(0,n.qy)`
      <div class="field" data-field-key=${tA(t)}>
        ${tL(e,i)}
        <p class="field-description">
          ${i.localize("device.value_set_in_yaml",{value:String(o)})}
        </p>
        ${tO(t,i)}
      </div>
    `;let a=t.join(".");(e.required||(0,eG.$z)(o))&&i.seedNestedOpen(a);let r=i.nestedOpenSections.has(a),s=null!=e.platform_type&&!e.required,l=s&&(0,eG.$z)(o),d=tE(e,i),c=i.localize("device.enable_entity",{name:d});return(0,n.qy)`
    <div class="nested-group" data-field-key=${tA(t)}>
      <div class="nested-header">
        ${s?(0,n.qy)`<wa-switch
                class="nested-enable"
                .checked=${l}
                ?disabled=${tS(e,i)}
                aria-label=${c}
                title=${c}
                @change=${e=>(function(e,t,i,o,a,r){let n,s=((n=iS.get(r.stashOwner))||(n=new Map,iS.set(r.stashOwner,n)),n);if(o){let o=s.get(t);o&&(0,eG.$z)(o)?(s.delete(t),r.emitChange(e,o)):r.emitChange([...e,"name"],a),i||r.toggleNested(t)}else{let o=r.getAt(e);(0,eC.Qd)(o)&&(0,eG.$z)(o)&&s.set(t,o),r.emitChange(e,void 0),i&&r.toggleNested(t)}})(t,a,r,e.target.checked,d,i)}
              ></wa-switch>`:n.s6}
        <button
          type="button"
          class="nested-toggle"
          aria-expanded=${r}
          @click=${()=>i.toggleNested(a)}
        >
          <wa-icon library="mdi" name=${r?"chevron-up":"chevron-down"}></wa-icon>
          <span class="nested-title">${d}</span>
          ${e.platform_type?(0,n.qy)`<span class="nested-platform">${e.platform_type}</span>`:n.s6}
        </button>
        ${tF(e,i)}
      </div>
      ${e.description?(0,n.qy)`<p class="nested-desc">${(0,en.Gc)(e.description)}</p>`:n.s6}
      ${r?(0,n.qy)`<div class="nested-fields">${tK(e,t,i)}</div>`:n.s6}
    </div>
  `}var iM=i(5089),iP=i(721),iE=i(7288),iF=i(5490);let iL=["us","ms","s","min","h","d"],iO={us:"us",µs:"us",microseconds:"us",ms:"ms",milliseconds:"ms",s:"s",sec:"s",seconds:"s",min:"min",minutes:"min",h:"h",hours:"h",d:"d",days:"d"},iR=Object.keys(iO).map(e=>e.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|"),iT=RegExp(`^(\\d+(?:\\.\\d+)?)\\s*(${iR})?$`),iD=RegExp(`^\\d+(?:\\.\\d+)?\\s*(?:${iR})$`);function iI(e){return"string"==typeof e&&iD.test(e.trim())}function iB(e){if(null==e||""===e)return{value:"",unit:"s",parseable:!0};let t=String(e).trim(),i=t.match(iT);if(i){let[,e,t]=i;return{value:e,unit:t?iO[t]:"s",parseable:!0}}return{value:t,unit:"s",parseable:!1}}function ij(e,t){let i=e.trim();return""===i?"":`${i}${t}`}function iK(e){return null==e||""===e?"":(0,iF.uS)(e)||String(e)}let iU=new WeakMap;function iZ(e,t,i){let o=i.getAt(t),a=tT(e,t,i,o);if(a)return a;let r=(0,eG.FY)(o);if(null===r&&(0,to.rf)(o))return tD(e,t,i,o);let s=(null==o?(0,eG.FY)(e.default_value):r)===!0;return(0,n.qy)`
    <div class="switch-field" data-field-key=${tA(t)}>
      <div class="field-info">${tL(e,i,{includeHelpLink:!1})}</div>
      ${tF(e,i)}
      <wa-switch
        ?checked=${s}
        ?disabled=${tS(e,i)}
        aria-label=${tE(e,i)}
        @change=${e=>i.emitChange(t,e.target.checked)}
      ></wa-switch>
    </div>
  `}function iN(e,t,i=""){if(!t)return e;let o=i.toLowerCase(),a=e.filter(e=>!e.variants?.length||e.variants.includes(t)||e.value.toLowerCase()===o);return a.length>0?a:e}function iV(e,t){let i="string"==typeof e?e.trim():(0,eC.Qd)(e)&&"string"==typeof e.number?e.number.trim():"";if(!i)return null;let o=i.toLowerCase(),a=t.find(e=>e.aliases?.some(e=>e.toLowerCase()===o));return a?a.gpio:null}function iH(e,t){return(0,n.qy)`<wa-option
    class=${e.warn?"pin-option pin-option--warn":"pin-option"}
    value=${e.optValue}
    .label=${e.primary}
    ?selected=${e.optValue===t}
    ?disabled=${e.disabled}
    title=${e.titleText}
  >
    <span class="pin-option-stack">
      <span class="pin-option-primary">
        ${e.primary}
        ${e.warn?(0,n.qy)`<wa-icon
                class="pin-warn-icon"
                library="mdi"
                name="alert-circle-outline"
              ></wa-icon>`:n.s6}
      </span>
      ${e.secondary?(0,n.qy)`<span class="pin-option-secondary">${e.secondary}</span>`:n.s6}
    </span>
  </wa-option>`}function iG(e,t,i,o,a,r){let s=i.filterRenderable(e.config_entries??[],i.scopeValues(t));if(0===s.length)return n.s6;let l=`${t.join(".")}:pin-advanced`,d=i.scopeValues(t);a&&Object.keys(d).some(e=>"number"!==e&&void 0!==d[e])&&i.seedNestedOpen(l);let c=i.nestedOpenSections.has(l);return(0,n.qy)`
    <div
      class="pin-advanced"
      data-field-key="${l}"
      data-reveal-for="${tA(t)}"
    >
      ${(0,iq.u)({open:c,onToggle:()=>{!r&&(i.toggleNested(l),c||a||null==o||""===o||i.emitChange(t,{number:o}))},localize:i.localize,labelKey:"device.pin_advanced",variant:"quiet",iconBefore:!0,disabled:r,body:()=>(0,n.qy)`${s.map(e=>(function(e,t,i){var o,a,r,n,s,l,d,c;let h,p,u,m,v,g,f;if("mode"!==e.key||e.type!==e6.Hh.NESTED)return i.renderEntry(e,[...t,e.key]);let _=[...t,e.key],b=i.getAt(_),y=function(e,t){if(!t||!(0,eC.Qd)(e))return null;for(let i of Object.keys(e))if(Object.prototype.hasOwnProperty.call(t,i)){let e=t[i];return e.length>0?e:null}return null}(i.getAt(t),i.pinRegistryModes),w=y?(a=e,h=new Set([...y,..."string"==typeof(o=b)?Object.keys(iC(o)??{}):(0,eC.Qd)(o)?Object.keys(o):[]]),p=(a.config_entries??[]).filter(e=>h.has(e.key)),{...a,config_entries:p}):e;return"string"!=typeof b||(0,t_.R_)(b)?i.renderEntry(w,_):(r=w,n=_,(m="string"==typeof(u=(s=i).getAt(n))?iC(u):null)?iA(r,n,(l=s,d=n,c=m,v=d.join("."),g=e=>e.length===d.length+1&&e.slice(0,d.length).join(".")===v?e[d.length]:null,(f={...l,getAt:e=>{if(e.join(".")===v)return c;let t=g(e);return null!==t?c[t]:l.getAt(e)},scopeValues:e=>e.join(".")===v?{...c}:l.scopeValues(e),emitChange:(e,t)=>{let i=g(e);if(null===i)return void l.emitChange(e,t);let o={...c};t?o[i]=!0:delete o[i],l.emitChange(d,o)}}).renderEntry=(e,t)=>e.type===e6.Hh.BOOLEAN?iZ(e,t,f):l.renderEntry(e,t),f)):iA(r,n,s))})(e,t,i))}`})}
    </div>
  `}var iW=i(8067);function iY(e,t){let i=e.getAt(t);return Array.isArray(i)?i:[]}function iJ(e,t,i){return{addItem:()=>e.emitChange(t,[...iY(e,t),i()]),removeAt:i=>{e.clearEditingMagnitudesUnder(t),e.emitChange(t,iY(e,t).filter((e,t)=>t!==i))}}}function iQ(e,t){return 0===e.length?(0,n.qy)`<p class="field-description">${t.localize("device.multi_value_empty")}</p>`:n.s6}function iX(e,t,i){return(0,n.qy)`
    <button
      type="button"
      class="multi-btn"
      ?disabled=${t}
      aria-label=${e.localize("device.multi_value_remove")}
      @click=${i}
    >
      <wa-icon library="mdi" name="close"></wa-icon>
    </button>
  `}function i0(e,t,i){return(0,n.qy)`
    <button
      type="button"
      class="multi-btn multi-add"
      ?disabled=${t}
      @click=${i}
    >
      <wa-icon library="mdi" name="plus"></wa-icon>
      ${e.localize("device.multi_value_add")}
    </button>
  `}let i1=new(i(2741)).E({name:"automation-body-cache",bucketKey:()=>"",cacheMisses:!1,fetch:(e,t)=>{let i=t.map(e=>{let t=e.indexOf("/");return{type:e.slice(0,t),id:e.slice(t+1)}});return e.getAutomationBodies(i)}});function i2(e,t,i){return i1.fetch(e,`${t}/${i}`,void 0)}async function i6(e,t,i,o=i2){let a=await o(e,t,i.id);if(a&&"config_entries"in a)return i.config_entries=structuredClone(a.config_entries),"required_groups"in a&&(i.required_groups=structuredClone(a.required_groups)),"ok";let r=null===a?"no body returned":"body shape missing config_entries";return console.warn(`automation-body: ${t}/${i.id} ${r}; form will render empty`),null===a?"missingBody":"missingField"}function i3(){return{succeeded:0,missingBody:0,missingField:0,rejected:0}}function i5(e,t){e["ok"===t?"succeeded":t]++}function i4(e,t){return`${e??""}|${t??""}`}let i8={triggers:(0,t4.Y)({name:"automation-catalog-cache:triggers",key:i4,fetch:(e,t,i)=>e.getAutomationTriggers(t,i)}),actions:(0,t4.Y)({name:"automation-catalog-cache:actions",key:i4,fetch:(e,t,i)=>e.getAutomationActions(t,i)}),conditions:(0,t4.Y)({name:"automation-catalog-cache:conditions",key:i4,fetch:(e,t,i)=>e.getAutomationConditions(t,i)}),light_effects:(0,t4.Y)({name:"automation-catalog-cache:light_effects",key:i4,fetch:(e,t,i)=>e.getLightEffects(t,i)}),filters:(0,t4.Y)({name:"automation-catalog-cache:filters",key:i4,fetch:(e,t,i)=>e.getFilters(t,i)})};function i9(e,t){return i8.triggers.getCached(e,t)}async function i7(e,t,i){let o=await i8.light_effects.fetch(e,t,i);return ot("light_effects",t,i,o,t=>oo(e,"light_effects",t))}async function oe(e,t,i){let o=await i8.filters.fetch(e,t,i);return ot("filters",t,i,o,t=>oo(e,"filters",t))}async function ot(e,t,i,o,a){if(0===(await a(o)).succeeded)return o;let r=[...o];return i8[e].update(r,t,i),r}let oi=new WeakSet;async function oo(e,t,i){let o=i3(),a=i.filter(e=>!oi.has(e));if(0===a.length)return o;for(let i of(await Promise.allSettled(a.map(async i=>{let a=await i6(e,t,i);"ok"===a&&oi.add(i),i5(o,a)}))))"rejected"===i.status&&(o.rejected++,console.warn(`${t} hydration failed`,i.reason));let r=o.missingBody+o.missingField+o.rejected;return r>0&&console.warn(`${t} hydration: ${o.succeeded} ok, ${r} failed (missingBody=${o.missingBody}, missingField=${o.missingField}, rejected=${o.rejected})`),o}function oa(e){let t=Object.values(i8).map(t=>t.subscribe(e));return()=>{for(let e of t)e()}}var or=i(8339);function on(e){let t=Object.keys(e);return 1===t.length?t[0]:""}function os(e){return e?e.replace(/_/g," ").replace(/\b\w/g,e=>e.toUpperCase()):""}let ol={time_period:e6.Hh.TIME_PERIOD,float:e6.Hh.FLOAT,integer:e6.Hh.INTEGER,string:e6.Hh.STRING,lambda:e6.Hh.LAMBDA},od={light_effects:{cache:()=>i8.light_effects.getCached(void 0,void 0),fetch:e=>i7(e),parentToken:e=>e,dedupByTypeId:!0},filter:{cache:()=>i8.filters.getCached(void 0,void 0),fetch:e=>oe(e),parentToken:e=>e.split(".",1)[0],dedupByTypeId:!1}};function oc(e){return Array.isArray(e)?e:[]}function oh(e){let t=[],i=[];return e.forEach((e,o)=>{!(null===e||"object"!=typeof e||Array.isArray(e))&&Object.keys(e).length<=1&&(t.push(e),i.push(o))}),{items:t,positions:i}}function op(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}class ou extends n.WF{connectedCallback(){super.connectedCallback();let e=this._ops();if(null===e)return;this._unsubscribe=oa(()=>{if(!this.isConnected)return;let e=this._ops();if(null===e)return;let t=e.cache();void 0!==t&&(this._catalog=t,this._fetchError=!1)});let t=e.cache();this._fetchError=!1,void 0!==t?this._catalog=t:this._kickFetch(e)}updated(){if(this._kickedFetch||null!==this._catalog||this._fetchError||!this._api)return;let e=this._ops();null!==e&&void 0===e.cache()&&this._kickFetch(e)}_kickFetch(e){this._api&&(this._kickedFetch=!0,e.fetch(this._api).catch(e=>{console.error("Failed to fetch registry catalog",e),this.isConnected&&(this._fetchError=!0)}))}_ops(){return od[this.entry?.registry??""]??null}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe?.(),this._unsubscribe=void 0,this._kickedFetch=!1}render(){let e=this._ops();if(null===e)return(0,n.qy)`
        <div class="field" data-field-key=${tA(this.path)}>
          ${tL(this.entry,this.ctx)}
          <p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_unsupported")}
          </p>
          ${tO(this.path,this.ctx)}
        </div>
      `;let t=this.ctx.getAt(this.path);if(t instanceof eG.ho||void 0!==t&&!Array.isArray(t))return(0,n.qy)`
        <div class="field" data-field-key=${tA(this.path)}>
          ${tL(this.entry,this.ctx)}
          <p class="field-description">
            ${this.ctx.localize("device.multi_value_yaml_only")}
          </p>
          ${tO(this.path,this.ctx)}
        </div>
      `;let{items:i}=oh(oc(t)),o=tS(this.entry,this.ctx),a=this.ctx.sectionKey?e.parentToken(this.ctx.sectionKey):"",r=(this._catalog??[]).filter(e=>!a||0===e.applies_to.length||e.applies_to.includes(a)),s=null!==this._catalog&&0===this._catalog.length,l=this._fetchError?(0,n.qy)`<p class="registry-list-fallback">
          ${this.ctx.localize("device.registry_list_error")}
          ${this._api?(0,n.qy)`<button type="button" class="multi-btn" @click=${this._retryFetch}>
                  ${this.ctx.localize("device.registry_list_retry")}
                </button>`:n.s6}
        </p>`:null===this._catalog?(0,n.qy)`<p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_loading")}
          </p>`:s?(0,n.qy)`<p class="registry-list-fallback">
              ${this.ctx.localize("device.registry_list_empty_catalog")}
            </p>`:0===r.length?(0,n.qy)`<p class="registry-list-fallback">
                ${this.ctx.localize("device.registry_list_no_applicable_options")}
              </p>`:n.s6,d=o||0===r.length;return(0,n.qy)`
      <div class="field" data-field-key=${tA(this.path)}>
        ${tL(this.entry,this.ctx)} ${iQ(i,this.ctx)}
        ${l}
        ${i.map((t,a)=>this._renderRow(t,a,r,i,o,e.dedupByTypeId))}
        ${i0(this.ctx,d,()=>this._addItem())}
        ${tO(this.path,this.ctx)}
      </div>
    `}_renderRow(e,t,i,o,a,r){let s=on(e),l=new Set;r&&o.forEach((e,i)=>{if(i===t)return;let o=on(e);o&&l.add(o)});let d=i.find(e=>e.id===s),c=void 0!==d,h=[...i].sort((e,t)=>e.id.localeCompare(t.id)),p=s?e[s]:null,u=null!==p&&"object"==typeof p&&!Array.isArray(p)&&!(0,iW.b)(p)&&!(p instanceof eG.ho),m=u?null:this._scalarDispatchType(d,p),v=(null===p||u)&&d?.config_entries?d.config_entries:[];return(0,n.qy)`
      <div class="registry-list-item" data-row-index=${t}>
        <div class="registry-list-row">
          <wa-select
            .value=${s}
            ?disabled=${a}
            placeholder=${this.ctx.localize("device.registry_list_select")}
            aria-label=${this.ctx.localize("device.registry_list_row_label",{index:String(t+1)})}
            @change=${e=>{let i=e.target.value;this._renameRow(t,i)}}
          >
            ${!c&&s?(0,n.qy)`<wa-option value=${s} selected
                    >${os(s)}</wa-option
                  >`:n.s6}
            ${h.filter(e=>e.id===s||!l.has(e.id)).map(e=>(0,n.qy)`<wa-option value=${e.id} ?selected=${e.id===s}
                    >${os(e.id)}</wa-option
                  >`)}
          </wa-select>
          ${iX(this.ctx,a,()=>this._removeAt(t))}
        </div>
        ${this._renderSubForm(t,s,m,v,d?.templatable??!1)}
      </div>
    `}_mutateEditable(e){let t=oc(this.ctx.getAt(this.path)),{items:i,positions:o}=oh(t),a=e(i);this.ctx.emitChange(this.path,function(e,t,i){let o=[...e];if(t.forEach((e,t)=>{t<i.length&&(o[e]=i[t])}),i.length<t.length)for(let e of t.slice(i.length).reverse())o.splice(e,1);else if(i.length>t.length){let e=t.length>0?t[t.length-1]+1:o.length;o.splice(e,0,...i.slice(t.length))}return o}(t,o,a))}_scalarDispatchType(e,t){let i=e?.value_type;return i&&Object.prototype.hasOwnProperty.call(ol,i)?ol[i]:iI(t)?e6.Hh.TIME_PERIOD:null}_renderSubForm(e,t,i,o,a){return null!==i?(0,n.qy)`<div class="registry-list-sub-form">
        ${this.ctx.renderEntry((0,or.h)({type:i,templatable:a}),[...this.path,String(e),t])}
      </div>`:o.length>0?(0,n.qy)`<div class="registry-list-sub-form">
        ${o.map(i=>this.ctx.renderEntry(i,[...this.path,String(e),t,i.key]))}
      </div>`:n.s6}_addItem(){this._mutateEditable(e=>[...e,{}])}_removeAt(e){this._mutateEditable(t=>t.filter((t,i)=>i!==e))}_renameRow(e,t){this._mutateEditable(i=>{if(!t)return i;let o=i[e];return o&&on(o)!==t?i.map((i,o)=>o===e?{[t]:null}:i):i})}constructor(...e){super(...e),this.path=[],this._catalog=null,this._fetchError=!1,this._kickedFetch=!1,this._retryFetch=()=>{if(!this._api)return;let e=this._ops();null!==e&&(this._fetchError=!1,e.fetch(this._api).catch(e=>{console.error("Failed to retry registry catalog fetch",e),this.isConnected&&(this._fetchError=!0)}))}}}ou.styles=[...tq,(0,n.AH)`
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
    `],op([(0,a.Fg)({context:_.Ie})],ou.prototype,"_api",void 0),op([(0,s.MZ)({attribute:!1})],ou.prototype,"entry",void 0),op([(0,s.MZ)({attribute:!1})],ou.prototype,"path",void 0),op([(0,s.MZ)({attribute:!1})],ou.prototype,"ctx",void 0),op([(0,s.wk)()],ou.prototype,"_catalog",void 0),op([(0,s.wk)()],ou.prototype,"_fetchError",void 0),ou=op([(0,s.EM)("esphome-registry-list")],ou);var om=i(5719),ov=i(9177),og=i(6838),of=i(5475),o_=i(7915),ob=i(6320),oy=i(2125),ow=i(4256),o$=i(6250);function ox(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}let ok=of.YH.define();class oz extends o$.U{render(){return(0,n.qy)`<div class="cm-wrap ${this.invalid?"invalid":""}"></div>`}firstUpdated(){this._mountEditor()}updated(e){if(this._view&&(e.has("_darkMode")&&this._view.dispatch({effects:this._themeCompartment.reconfigure((0,oy.P5)(this._darkMode))}),e.has("disabled")&&this._view.dispatch({effects:this._editableCompartment.reconfigure(o_.Lz.editable.of(!this.disabled))}),e.has("value"))){let e=this._view.state.doc.toString();e!==this.value&&this._view.dispatch({changes:{from:0,to:e.length,insert:this.value},annotations:ok.of(!0)})}}_mountEditor(){this._mountView(this.value,[ob.oQ,(0,ow.O)(this._localize),(0,ov.I)(),og.Xt.of("  "),o_.w4.of([om.Yc]),this._editableCompartment.of(o_.Lz.editable.of(!this.disabled)),this._themeCompartment.of((0,oy.P5)(this._darkMode)),oy.gn,o_.Lz.updateListener.of(e=>{if(e.docChanged&&!e.transactions.some(e=>void 0!==e.annotation(ok))){let t=e.state.doc.toString();(0,Z.r)(this,"lambda-change",{value:t})}})])}constructor(...e){super(...e),this._darkMode=(0,J.yk)(),this._localize=e=>e,this.value="",this.disabled=!1,this.invalid=!1,this.placeholder="",this._themeCompartment=new of.xx,this._editableCompartment=new of.xx}}function oC(e){return(0,iW.b)(e)?e._lambda:e instanceof eG.ho?e.body:null==e?"":String(e)}function oq(e,t,i){let o=i.getAt(t),a=oC(o),r=null!==i.errorAt(t),s=tS(e,i),l=(0,iW.b)(o)?o._tag:void 0;return tR(e,t,i,(0,n.qy)`<esphome-lambda-editor
      .value=${a}
      .invalid=${r}
      ?disabled=${s}
      placeholder=${String(e.default_value??"")}
      @lambda-change=${e=>i.emitChange(t,l?{_lambda:e.detail.value,_tag:l}:{_lambda:e.detail.value})}
    ></esphome-lambda-editor>`)}oz.styles=(0,n.AH)`
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
  `,ox([(0,a.Fg)({context:_.B6,subscribe:!0}),(0,s.wk)()],oz.prototype,"_darkMode",void 0),ox([(0,a.Fg)({context:_.$F}),(0,s.wk)()],oz.prototype,"_localize",void 0),ox([(0,s.MZ)()],oz.prototype,"value",void 0),ox([(0,s.MZ)({type:Boolean,reflect:!0})],oz.prototype,"disabled",void 0),ox([(0,s.MZ)({type:Boolean})],oz.prototype,"invalid",void 0),ox([(0,s.MZ)()],oz.prototype,"placeholder",void 0),oz=ox([(0,s.EM)("esphome-lambda-editor")],oz);let oS=new WeakMap;i(8944);var oA=i(1209);async function oM(e,t,i){let{created:o}=await e.setSecret(t,i,!1);return o&&window.dispatchEvent(new CustomEvent("secrets-saved")),{created:o}}async function oP(e,t,i){await e.setSecret(t,i,!0),window.dispatchEvent(new CustomEvent("secrets-saved"))}async function oE(e,t,i,o,a){try{return await a(),(0,oA.ik)(e),!0}catch(e){return console.error(i,e),(0,d.UG)(o(t)),!1}}function oF(e,t,i,o,a){return oE(e,a.errorKey,a.logLabel,o,async()=>{let{created:r}=await oM(e,t,i);d.me[r?"success":"info"](o(r?a.createdKey:"device.secret_picker_linked",{key:t}))})}i(1958),i(5910);var oL=i(8990),oO=i(9309);function oR(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({alert:r.mdiAlert,"content-copy":r.mdiContentCopy});class oT extends n.WF{willUpdate(e){(e.has("secretKey")||e.has("present"))&&(this._draftValue="",this._stored=null,this._busy=!1,this._loading=!1,this._loadError=!1,this._loadToken++,this._opToken++)}updated(){this.present&&this.secretKey&&this._api&&null===this._stored&&!this._loading&&!this._loadError&&this._loadStored()}render(){return this.present?this._renderEdit():this._renderCreate()}get _dirty(){return null!==this._stored&&this._draftValue!==this._stored}get _hasDraft(){return""!==this._draftValue.trim()}get _loadingStored(){return this.present&&null===this._stored}_renderEdit(){return this._loadError?this._renderLoadError():(0,n.qy)`<div class="row">
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
      ></esphome-confirm-dialog>`}_renderLoadError(){return(0,n.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_reveal_error")}
        <button class="retry link-button" type="button" @click=${this._retry}>
          ${this._localize("device.secret_picker_retry")}
        </button>
      </span>
    </div>`}_renderCreate(){return(0,n.qy)`<div class="fix">
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
    </div>`}_renderInput(){return(0,n.qy)`<esphome-password-input
      class="value"
      .value=${this._draftValue}
      .disabled=${this._busy||this._loadingStored}
      .placeholder=${this._localize(this.present?"device.secret_picker_value":"device.secret_picker_missing_placeholder")}
      .label=${this._localize("device.secret_picker_value_label",{key:this.secretKey})}
      @password-input-change=${e=>{this._draftValue=e.detail.value}}
      @keydown=${e=>{"Enter"===e.key&&(e.preventDefault(),this.present?this._save():this._create())}}
    ></esphome-password-input>`}async _loadStored(){let e=++this._loadToken;this._loading=!0;let t=null,i=!1;try{let e=await this._api.getConfig("secrets.yaml");t=(0,tg.Tv)(e,this.secretKey)}catch{i=!0,(0,d.UG)(this._localize("device.secret_picker_reveal_error"))}if(e===this._loadToken){if(this._loading=!1,i){this._loadError=!0;return}this._stored=t??"",this._draftValue=this._stored}}async _run(e,t){let i=this._api;if(!i||!this.secretKey||this._busy)return;let o=this._opToken;this._busy=!0;try{let a=await e(i);if(o!==this._opToken)return;a&&t()}finally{o===this._opToken&&(this._busy=!1)}}constructor(...e){super(...e),this._localize=e=>e,this.secretKey="",this.present=!1,this.deviceName="",this._draftValue="",this._stored=null,this._busy=!1,this._loadError=!1,this._loadToken=0,this._opToken=0,this._loading=!1,this._retry=()=>{this._loadError=!1},this._copy=async()=>{await (0,oO.l)(this._draftValue)&&(0,d.VX)(this._localize("device.secret_reveal_copied"))},this._create=()=>{this._hasDraft&&this._run(e=>oF(e,this.secretKey,this._draftValue,this._localize,{createdKey:"device.secret_picker_missing_created",errorKey:"device.secret_picker_missing_error",logLabel:"Secret create failed"}),()=>{this._draftValue=""})},this._save=()=>{if(this._dirty){if((0,tg.e2)(this.secretKey,this.deviceName))return void this._confirmDialog?.open();this._persist()}},this._persist=()=>{this._run(e=>{var t,i,o,a;return t=this.secretKey,i=this._draftValue,o=this._localize,oE(e,(a={savedKey:"device.secret_picker_saved",errorKey:"device.secret_picker_save_error",logLabel:"Secret save failed"}).errorKey,a.logLabel,o,async()=>{await oP(e,t,i),(0,d.VX)(o(a.savedKey,{key:t}))})},()=>{this._stored=this._draftValue})}}}function oD(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}oT.styles=[oL.R,(0,n.AH)`
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
    `],oR([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],oT.prototype,"_localize",void 0),oR([(0,a.Fg)({context:_.Ie,subscribe:!0}),(0,s.wk)()],oT.prototype,"_api",void 0),oR([(0,s.MZ)({attribute:"secret-key"})],oT.prototype,"secretKey",void 0),oR([(0,s.MZ)({type:Boolean})],oT.prototype,"present",void 0),oR([(0,s.MZ)({attribute:"device-name"})],oT.prototype,"deviceName",void 0),oR([(0,s.P)("esphome-confirm-dialog")],oT.prototype,"_confirmDialog",void 0),oR([(0,s.wk)()],oT.prototype,"_draftValue",void 0),oR([(0,s.wk)()],oT.prototype,"_stored",void 0),oR([(0,s.wk)()],oT.prototype,"_busy",void 0),oR([(0,s.wk)()],oT.prototype,"_loadError",void 0),oT=oR([(0,s.EM)("esphome-secret-value")],oT),(0,M.C)({alert:r.mdiAlert,check:r.mdiCheck,"chevron-down":r.mdiChevronDown,"key-variant":r.mdiKeyVariant,plus:r.mdiPlus,"shield-key-outline":r.mdiShieldKeyOutline});class oI extends n.WF{get _keys(){return this._secretKeys.value}get _migrateTarget(){return this.recommendedKeys[0]??""}get _canMigrate(){return""===this.selectedKey&&""!==this.value&&""!==this._migrateTarget&&void 0!==this._keys&&!this._keys.includes(this._migrateTarget)}get _missing(){return""!==this.selectedKey&&void 0!==this._keys&&!this._keys.includes(this.selectedKey)}render(){let e=""!==this.selectedKey,t=this._missing,i=(0,tg.Jw)(this._keys??[],[...this.recommendedKeys,this.selectedKey],this.deviceName,this._devices.map(e=>e.name)),o=new Set(i),a=new Set(this.recommendedKeys),r=this.recommendedKeys.filter(e=>o.has(e)),s=i.filter(e=>!a.has(e));return(0,n.qy)`
      <wa-dropdown @wa-select=${this._onSelect}>
        <button
          slot="trigger"
          class=${t?"trigger missing":e?"trigger selected":"trigger"}
          type="button"
          ?disabled=${this.disabled}
          aria-label=${this._localize(t?"device.secret_picker_aria_missing":"device.secret_picker_aria",{field:this.fieldLabel})}
        >
          <wa-icon
            class="key"
            library="mdi"
            name=${t?"alert":"key-variant"}
          ></wa-icon>
          ${e?(0,n.qy)`<span class="label">${this.selectedKey}</span>`:(0,n.qy)`<span class="placeholder"
                  >${this._localize("device.secret_picker_label")}</span
                >`}
          <wa-icon class="chevron" library="mdi" name="chevron-down"></wa-icon>
        </button>
        ${this._canMigrate?(0,n.qy)`<wa-dropdown-item class="migrate" value=${"__esphome_migrate_secret__"}>
                  <wa-icon slot="icon" library="mdi" name="shield-key-outline"></wa-icon>
                  ${this._localize("device.secret_picker_migrate",{key:this._migrateTarget})}
                </wa-dropdown-item>
                <wa-divider role="separator"></wa-divider>`:n.s6}
        ${r.length?(0,n.qy)`<small class="group-label" aria-hidden="true"
                  >${this._localize("device.secret_picker_related")}</small
                >
                ${r.map(e=>this._renderKeyItem(e))}
                ${s.length?(0,n.qy)`<small class="group-label" aria-hidden="true"
                        >${this._localize("device.secret_picker_shared")}</small
                      >`:n.s6}`:n.s6}
        ${s.map(e=>this._renderKeyItem(e))}
        ${i.length?n.s6:(0,n.qy)`<wa-dropdown-item class="empty" disabled role="status"
                >${this._localize("device.secret_picker_empty")}</wa-dropdown-item
              >`}
        <wa-divider role="separator"></wa-divider>
        <wa-dropdown-item class="create" value=${"__esphome_create_secret__"}>
          <wa-icon slot="icon" library="mdi" name="plus"></wa-icon>
          ${this._localize("device.secret_picker_create")}
        </wa-dropdown-item>
        ${e?(0,n.qy)`<wa-dropdown-item class="manual" value=${"__esphome_manual_value__"}>
                ${this._localize("device.secret_picker_manual")}
              </wa-dropdown-item>`:n.s6}
      </wa-dropdown>
      ${e?(0,n.qy)`<esphome-secret-value
              secret-key=${this.selectedKey}
              ?present=${!t}
              device-name=${this.deviceName}
            ></esphome-secret-value>`:n.s6}
    `}_renderKeyItem(e){return(0,n.qy)`<wa-dropdown-item
      value=${e}
      aria-selected=${e===this.selectedKey?"true":"false"}
    >
      ${e===this.selectedKey?(0,n.qy)`<wa-icon slot="icon" class="check" library="mdi" name="check"></wa-icon>`:n.s6}
      ${e}
    </wa-dropdown-item>`}_onSelect(e){let t=e.detail.item,i=t.classList;if(i?.contains("create"))return void(0,S.oo)("/secrets");if(i?.contains("migrate"))return void this._migrate();if(i?.contains("manual"))return void this._manual();let o=t.value??"";o&&this._emit(`!secret ${o}`)}async _manual(){if(!this._api||!this.selectedKey)return void this._emit("");try{let e=await this._api.getConfig("secrets.yaml");this._emit((0,tg.Tv)(e,this.selectedKey)??"")}catch{(0,d.UG)(this._localize("device.secret_picker_manual_error"))}}_emit(e){this.dispatchEvent(new CustomEvent("secret-selected",{detail:{value:e},bubbles:!0,composed:!0}))}async _migrate(){let e=this._migrateTarget;this._api&&e&&this.value&&await oF(this._api,e,this.value,this._localize,{createdKey:"device.secret_picker_migrated",errorKey:"device.secret_picker_migrate_error",logLabel:"Secret migration failed"})&&this._emit(`!secret ${e}`)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.disabled=!1,this.deviceName="",this.full=!1,this.fieldLabel="",this.selectedKey="",this.value="",this.recommendedKeys=[],this._secretKeys=new ii(this,{getCached:oA.BW,subscribe:oA.Ft,fetch:oA.RX},()=>this._api)}}function oB(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}oI.styles=(0,n.AH)`
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
  `,oD([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],oI.prototype,"_localize",void 0),oD([(0,a.Fg)({context:_.Ie,subscribe:!0}),(0,s.wk)()],oI.prototype,"_api",void 0),oD([(0,a.Fg)({context:_.xJ,subscribe:!0}),(0,s.wk)()],oI.prototype,"_devices",void 0),oD([(0,s.MZ)({type:Boolean})],oI.prototype,"disabled",void 0),oD([(0,s.MZ)({attribute:"device-name"})],oI.prototype,"deviceName",void 0),oD([(0,s.MZ)({type:Boolean,reflect:!0})],oI.prototype,"full",void 0),oD([(0,s.MZ)({attribute:"field-label"})],oI.prototype,"fieldLabel",void 0),oD([(0,s.MZ)({attribute:"selected-key"})],oI.prototype,"selectedKey",void 0),oD([(0,s.MZ)()],oI.prototype,"value",void 0),oD([(0,s.MZ)({attribute:!1})],oI.prototype,"recommendedKeys",void 0),oI=oD([(0,s.EM)("esphome-secret-picker")],oI),(0,M.C)({"alert-circle-outline":r.mdiAlertCircleOutline,"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,close:r.mdiClose,"open-in-new":r.mdiOpenInNew,plus:r.mdiPlus});class oj extends n.WF{render(){let e=this._buildCtx(),t=this.requiredOnly?function(e){let t=new Map;for(let i of e)i.exclusive_group&&t.set(i.exclusive_group,(t.get(i.exclusive_group)??!1)||!!i.required);let i=e=>e.exclusive_group?t.get(e.exclusive_group):!!e.required;return[...e.filter(i),...e.filter(e=>!i(e))]}(this.entries):this.entries;return this.advancedSection?this._renderWithAdvancedSection(t,e):this._renderFlat(t,e)}_renderFlat(e,t){let i=tH(e,this.values,this.requiredGroups,tr(this)),o=this._makeItemRenderer(i,t);return(0,n.qy)`${this._renderConstraintBanners(t,i.memberKeys)}${i.ordered.map(o)}`}_renderWithAdvancedSection(e,t){let i=tH(e,this.values,this.requiredGroups,tr(this,{showAdvanced:!0})),o=this._makeItemRenderer(i,t),a=this._advancedUnitClassifier(i),r=t.board?.esphome.platform??null,s=e=>e.members.some(e=>void 0!==(0,eC.O6)(this.values,[e.key])||(0,to.VP)(e,this.values,this.presentComponents,r,void 0,this.entries)),l=new Set(i.clusters.filter(s).map(e=>e.members[0].key)),d=i.ordered.filter(e=>!!Array.isArray(e)||(i.memberKeys.has(e.key)?l.has(e.key):i.visible.has(e))),c=d.filter(e=>!a(e)),h=d.filter(e=>a(e)),p=function e(t){for(let i of t)if(i.advanced||i.type===e6.Hh.NESTED&&e(i.config_entries??[]))return!0;return!1}(e),u=h.length>0&&0===c.length&&!this.forceAdvancedControl&&!this.gateAdvanced,m=[],v=h;if(this.gateAdvanced){let e=e=>{if(Array.isArray(e))return e.some(e=>tn(e,this.values));if(i.memberKeys.has(e.key)){let t=i.clusterByFirstKey.get(e.key);return!!t?.members.some(e=>tn(e,this.values))}return tn(e,this.values)};for(let t of(v=[],h)){let i;if(this.showAdvanced){let o=Array.isArray(t)?t[0].key:t.key;i=this._openAdvancedPlacement.get(o)??e(t),this._openAdvancedPlacement.set(o,i)}else i=e(t);(i?m:v).push(t)}}let g=this._effectiveForceOpen(),f=this.showAdvanced||g||u,_=this.forceAdvancedControl||p&&!u,b=v.length+this.advancedExtraCount;return(0,n.qy)`${this._renderConstraintBanners(t,i.memberKeys)}${c.map(o)}${m.map(o)}${_?this._renderAdvancedControl(f,b,g):n.s6}${f?v.map(o):n.s6}`}_makeItemRenderer(e,t){return i=>{if(Array.isArray(i)){let e,o,a,r,s,l,d,c;return e=i.filter(e=>void 0!==t.getAt([e.key])),o=e[0]?.key??"",a=i.find(e=>e.key===o),r=t.scopeValues([]),s=t.board?.esphome.platform??null,l=i.filter(e=>void 0!==t.getAt([e.key])||(0,to.VP)(e,r,t.presentComponents,s,void 0,t.entries)),d=t.disabled||l.every(e=>e.locked),c=`exclusive-group-${i[0].key}`,(0,n.qy)`
    <div class="field" data-field-key=${tA(a?[a.key]:[])}>
      <label class="field-label" id=${c}>
        ${t.localize("device.exclusive_group_label")}
        <span class="required">*</span>
      </label>
      <wa-select
        data-no-value-sync
        aria-labelledby=${c}
        ?disabled=${d}
        @change=${e=>{let o=e.target.value;var a=o===tV?"":o;for(let e of i)e.key!==a&&void 0!==t.getAt([e.key])&&t.emitChange([e.key],void 0);a&&void 0===t.getAt([a])&&t.emitChange([a],{})}}
      >
        <wa-option value=${tV} ?selected=${""===o}>
          ${t.localize("device.exclusive_group_placeholder")}
        </wa-option>
        ${l.map(e=>(0,n.qy)`<wa-option value=${e.key} ?selected=${e.key===o}
              >${tE(e,t)}</wa-option
            >`)}
      </wa-select>
      ${e.length>1?(0,n.qy)`<p class="field-description exclusive-group-conflict">
              ${t.localize("device.exclusive_group_conflict")}
            </p>`:n.s6}
      ${a?(0,n.qy)`<div class="nested-fields">
              ${tK(a,[a.key],t,{includeAdvanced:!0})}
            </div>`:n.s6}
    </div>
  `}if(e.memberKeys.has(i.key)){let o=e.clusterByFirstKey.get(i.key);return o?o.cardinality?.kind==="exactly_one"?function(e,t){let i=e.members[0].key,o=t.scopeValues([]),a=t.board?.esphome.platform??null,r=e=>void 0!==t.getAt([e.key])||(0,to.VP)(e,o,t.presentComponents,a,void 0,t.entries),s=tZ(e,t).filter(e=>e.members.some(r));if(s.length<2)return tN(e,t);let l=t.getClusterChoice(i)??s.find(e=>e.members.some(e=>(0,to.rf)(t.getAt([e.key]))))?.id,d=s.find(e=>e.id===l),c=t.localize("device.constraint_exactly_one_radio"),h=`constraint-cluster-${i}`,p=(d?.members??[]).filter(r);return(0,n.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${tA([i])}
    >
      <div id=${h} class="constraint-cluster-header">
        <span>${c}</span>
      </div>
      <wa-radio-group
        class="constraint-cluster-radios"
        aria-labelledby=${h}
        .value=${l??""}
        ?disabled=${t.disabled}
        @change=${i=>(function(e,t,i){let o=e.members[0].key,a=tZ(e,t),r=a.find(e=>e.id===i);if(r){for(let e of a)if(e.id!==i)for(let{key:i}of e.members){let e=t.getAt([i]);void 0!==e&&(t.setClusterStash(o,i,e),t.emitChange([i],void 0))}for(let{key:e}of r.members){let i=t.getClusterStash(o,e);void 0!==i&&(t.emitChange([e],i),t.clearClusterStash(o,e))}t.setClusterChoice(o,i)}})(e,t,i.target.value)}
      >
        ${s.map(e=>(0,n.qy)`<wa-radio value=${e.id}>${e.label}</wa-radio>`)}
      </wa-radio-group>
      ${p.length?(0,n.qy)`<div class="nested-fields">
              ${p.map(e=>t.renderEntry(e,[e.key]))}
            </div>`:n.s6}
    </div>
  `}(o,t):tN(o,t):n.s6}return e.visible.has(i)?this._renderEntry(i,i.key?[i.key]:[],t):n.s6}}_advancedForceOpen(){return this.entries.some(e=>e.advanced&&tn(e,this.values))}_effectiveForceOpen(){return!this.gateAdvanced&&this._advancedForceOpen()}_advancedUnitClassifier(e){let t=new Map;for(let i of e.clusters){let e=i.members.every(e=>e.advanced);for(let o of i.members)t.set(o.key,e)}return i=>Array.isArray(i)?i.length>0&&i.every(e=>e.advanced):e.memberKeys.has(i.key)?t.get(i.key)??!1:!!i.advanced}_renderAdvancedControl(e,t,i){let o=t>0?this._localize("device.show_advanced_count",{count:t}):this._localize("device.show_advanced");return(0,n.qy)`<div class="advanced-toggle-row">
      <wa-switch
        size="small"
        ?disabled=${i}
        .checked=${e}
        @change=${e=>{let t=e.currentTarget,i=t.parentElement;i&&(this._advancedControlAnchor={top:i.getBoundingClientRect().top,at:performance.now()}),this._emitAdvancedToggle(t.checked)}}
      >
        ${o}
      </wa-switch>
    </div>`}_restoreAdvancedControlAnchor(e){let t=this._advancedControlAnchor;if(!t||!e.has("showAdvanced")||(this._advancedControlAnchor=void 0,performance.now()-t.at>2e3))return;let i=this.shadowRoot?.querySelector(".advanced-toggle-row");if(!i)return;let o=function(e){for(let t=it(e);t;t=it(t))if(t instanceof HTMLElement&&t.scrollHeight>t.clientHeight){let e=getComputedStyle(t).overflowY;if("auto"===e||"scroll"===e)return t}return null}(i);o&&(o.scrollTop+=i.getBoundingClientRect().top-t.top)}_emitAdvancedToggle(e){(0,Z.r)(this,"advanced-toggle",{show:e})}_renderConstraintBanners(e,t){let i=tG({entries:this.entries,requiredGroups:this.requiredGroups,values:this.values,presentComponents:this.presentComponents,targetPlatform:e.board?.esphome.platform??null,formatKeys:t=>tU(t,this.entries,e)},t);return 0===i.length?n.s6:i.map(({kind:t,keys:i})=>(0,n.qy)`
        <div class="warning-banner constraint-banner">
          <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
          <span>${e.localize(`device.constraint_${t}`,{keys:i})}</span>
        </div>
      `)}willUpdate(e){e.has("entries")&&void 0!==e.get("entries")&&(this._pendingUnits.clear(),this._editingMagnitudes.clear(),this._openAdvancedPlacement.clear(),this._constraintClusters.reset(),this._seededNestedOpen.clear()),e.has("showAdvanced")&&!this.showAdvanced&&this._openAdvancedPlacement.clear()}_pathOf(e){return tM(e.getAttribute("data-field-key")??"")}updated(e){super.updated(e),this._syncSelectValues(),this._fieldScroll.maybeScroll(e),this.advancedSection&&!this.showAdvanced&&this._effectiveForceOpen()&&this._emitAdvancedToggle(!0),this._maybeRevealForFocus(),this._restoreAdvancedControlAnchor(e)}_maybeRevealForFocus(){if(!this.advancedSection||this.showAdvanced||!this.focusFieldPath?.length||0===this.entries.length)return;let e=tA(this.focusFieldPath);e!==this._focusRevealKey&&(this._focusRevealKey=e,t3(this.entries,this.focusFieldPath)&&this._emitAdvancedToggle(!0))}async _syncSelectValues(){if(this.shadowRoot)for(let e of this.shadowRoot.querySelectorAll("[data-field-key]")){let t=e.querySelector("wa-select");if(!t)continue;if(t.hasAttribute("data-no-value-sync")){await this._syncSelectedAttr(t);continue}if(t.updateComplete)try{await t.updateComplete}catch{}let i=this._pathOf(e);if(!i.length)continue;let o=(0,eC.O6)(this.values,i);if(!(0,eC.k4)(o)){""!==(Array.isArray(t.value)?t.value[0]??"":t.value??"")&&(t.value="");continue}let a=String(o??""),r=Array.from(t.querySelectorAll("wa-option")),n=a.match(/^\s*(?:GPIO)?(\d+)\s*$/i)?.[1],s=e=>r.find(t=>t.value?.toLowerCase()===e.toLowerCase()),l=a?s(a)??(n?s(`GPIO${n}`):void 0):null,d=l?.value??a;(Array.isArray(t.value)?t.value[0]??"":t.value??"")!==d&&(t.value=d)}}async _syncSelectedAttr(e){if(e.updateComplete)try{await e.updateComplete}catch{}let t=e.querySelector("wa-option[selected]"),i=t?.value??"";(Array.isArray(e.value)?e.value[0]??"":e.value??"")!==i&&(e.value=i)}_renderEntry(e,t,i){try{return this._renderEntryUnsafe(e,t,i)}catch(o){console.error("esphome-config-entry-form: render failed for entry",{key:e.key,type:e.type,path:t},o);let i=(0,em.u)(o);return(0,n.qy)`<div class="render-error" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div>
          <strong> ${this._localize("device.entry_render_error_title")} </strong>
          <code class="render-error-key"
            >${e.key||"(empty key)"} · ${e.type}</code
          >
          <pre class="render-error-message">${i}</pre>
        </div>
      </div>`}}_renderEntryUnsafe(e,t,i){var o,a;if(e.templatable&&(o=e.type)!==e6.Hh.NESTED&&o!==e6.Hh.MAP&&o!==e6.Hh.DIVIDER&&o!==e6.Hh.LABEL&&o!==e6.Hh.ALERT){let o,r,s,l,d,c,h;return a=()=>this._renderEntryLeaf(e,t,i),o=i.getAt(t),r=(0,iW.b)(o),(s=oS.get(i.stashOwner))||(s=new Map,oS.set(i.stashOwner,s)),l=t.join("."),(d=s.get(l))||(d={},s.set(l,d)),c=d,h=tA(t),(0,n.qy)`
    <div class="templatable-field" data-field-key=${h}>
      ${tk({isLambda:r,disabled:i.disabled,localize:i.localize,onSwitch:e=>{e!==r&&(r?(c.lambda=(0,iW.b)(o)?o._lambda:"",i.emitChange(t,c.literal??"")):(c.literal=o,i.emitChange(t,{_lambda:c.lambda??"",_tag:"!lambda"})))}})}
      ${r?oq(e,t,i):a()}
    </div>
  `}return this._renderEntryLeaf(e,t,i)}_renderEntryLeaf(e,t,i){let o=i.getAt(t);if((0,t_.zZ)(o)){let o=e.type===e6.Hh.SECURE_STRING?"password":"text";return tB(e,o,t,i)}if(e.type===e6.Hh.DIVIDER)return(0,n.qy)`<wa-divider></wa-divider>`;if(e.type===e6.Hh.LABEL)return(0,n.qy)`<p class="label-entry">${tE(e,i)}</p>`;if(e.type===e6.Hh.ALERT)return(0,n.qy)`<div class="alert-entry">${tE(e,i)}</div>`;if(e.type===e6.Hh.NESTED)return e.multi_value?function(e,t,i){let o=i.getAt(t);if(o instanceof eG.ho)return(0,n.qy)`
      <div class="nested-list" data-field-key=${tA(t)}>
        ${tL(e,i)}
        <p class="field-description">${i.localize("device.multi_value_yaml_only")}</p>
        ${tO(t,i)}
      </div>
    `;let a=(0,eC.ly)(o),r=tS(e,i),{addItem:s,removeAt:l}=iJ(i,t,()=>({})),d=tE(e,i),c=e.config_entries??[];return(0,n.qy)`
    <div class="nested-list" data-field-key=${tA(t)}>
      ${tL(e,i)} ${iQ(a,i)}
      ${a.map((e,o)=>{let a=[...t,String(o)],s=i.filterRenderable(c,e);return(0,n.qy)`
          <div class="nested-list-item" data-field-key=${tA(a)}>
            <div class="nested-list-item-header">
              <span class="nested-list-item-title"> ${d} ${o+1} </span>
              ${iX(i,r,()=>l(o))}
            </div>
            <div class="nested-fields">
              ${s.map(e=>i.renderEntry(e,[...a,e.key]))}
            </div>
          </div>
        `})}
      ${i0(i,r,s)} ${tO(t,i)}
    </div>
  `}(e,t,i):iA(e,t,i);if(e.type===e6.Hh.MAP){let o,a,r,s,l,d;return o=(e.config_entries??[])[0],s=Object.keys(r=(a=i.getAt(t))&&"object"==typeof a&&!Array.isArray(a)?a:{}),l=tS(e,i),d=()=>{let e=i.getAt(t);return e&&"object"==typeof e&&!Array.isArray(e)?Object.assign(Object.create(null),e):Object.create(null)},(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      ${0===s.length?(0,n.qy)`<p class="field-description">${i.localize("device.map_empty")}</p>`:n.s6}
      ${s.map(e=>{let a,s,c;return a=[...t,e],s=r[e],c=!(0,eC.k4)(s)&&!(0,iW.b)(s),(0,n.qy)`
      <div class="map-row" data-field-key=${tA(a)}>
        <input
          type="text"
          class="multi-input map-key-input"
          .value=${e}
          ?disabled=${l}
          @change=${o=>((e,o)=>{if(e===o||!o)return;let a=i.getAt(t);if(!a||"object"!=typeof a||Array.isArray(a)||o in a)return;let r=Object.create(null);for(let[t,i]of Object.entries(a))r[t===e?o:t]=i;i.emitChange(t,r)})(e,o.target.value)}
        />
        <div class="map-value">
          ${c?(0,n.qy)`<p class="map-value-yaml-only">
                  ${i.localize("device.map_value_edit_in_yaml")}
                </p>`:o?i.renderEntry(o,a):n.s6}
        </div>
        <button
          type="button"
          class="multi-btn"
          ?disabled=${l}
          aria-label=${i.localize("device.map_remove")}
          @click=${()=>{let o;e in(o=d())&&(delete o[e],i.emitChange(t,o))}}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </div>
    `})}
      <button
        type="button"
        class="multi-btn multi-add"
        ?disabled=${l}
        @click=${()=>{let e=d(),o=1;for(;`new_${o}`in e;)o++;e[`new_${o}`]="",i.emitChange(t,e)}}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${i.localize("device.map_add")}
      </button>
      ${tO(t,i)}
    </div>
  `}if(e.type===e6.Hh.REGISTRY_LIST)return(0,n.qy)`<esphome-registry-list
    .entry=${e}
    .path=${t}
    .ctx=${i}
  ></esphome-registry-list>`;if(e.multi_value)return function(e,t,i){let o=iY(i,t);if(o.some(e=>!(0,eC.k4)(e)))return tI(e,t,i);let a=(e.type===e6.Hh.INTEGER||e.type===e6.Hh.FLOAT)&&"hex"!==e.display_format,r=a&&e.type===e6.Hh.INTEGER,s=a&&e.type===e6.Hh.FLOAT,l=a?o.map(e=>String(e??"")):o.map(e=>(0,tb.hZ)(String(e))),d=tS(e,i),{addItem:c,removeAt:h}=iJ(i,t,()=>"");return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)} ${iQ(l,i)}
      ${l.map((l,c)=>{let p=s&&null!=o[c]&&""!==o[c]&&Number.isFinite(Number(String(o[c]))),u=[...t,String(c)],m=null!==i.errorAt(u),v=r?i.getEditingMagnitude(u)??l:l;return(0,n.qy)`
          <div class="multi-row">
            <div class="multi-value-cell">
              <input
                type=${p?"number":"text"}
                autocomplete="off"
                spellcheck="false"
                step=${p?"any":n.s6}
                class="multi-input ${m?"invalid":""}"
                .value=${v}
                ?disabled=${d}
                @input=${o=>{let n,s=o.target.value;r&&i.setEditingMagnitude(u,s),(n=[...iY(i,t)])[c]=a?te(e,s):(0,tb.iI)(s),i.emitChange(t,n)}}
                @blur=${()=>{r&&i.clearEditingMagnitude(u)}}
              />
              ${tP(String(o[c]??""),i.substitutions,i.localize)}
              ${tO(u,i)}
            </div>
            ${iX(i,d,()=>h(c))}
          </div>
        `})}
      ${i0(i,d,c)} ${tO(t,i)}
    </div>
  `}(e,t,i);if(e.references_component)return function(e,t,i){let o=e.references_component||"",a=i.resolveInterfaceProviders(o),r=(0,e_.Zm)(i.yaml,o,a??[]),s=i.getAt(t),l=tT(e,t,i,s);if(l)return l;let d=String(s??""),c=null!==i.errorAt(t),h=""===d?(0,e_.z)(r,i.yaml):null,p=(e,t,i)=>(0,n.qy)`
    <wa-option
      class="id-option"
      value=${e}
      .label=${t}
      ?selected=${e===d}
    >
      <span class="id-option-stack">
        <span class="id-option-primary">${t}</span>
        <span class="id-option-secondary">${i}</span>
      </span>
    </wa-option>
  `,u=""!==d&&!r.some(e=>e.id===d),m=u?p(d,d,i.localize("device.id_reference_unresolved",{domain:o})):n.s6,v=!c&&null!==a&&(0,e_.Ty)(d,r,i.yaml),g=v?(0,tv.O)(i.localize("device.id_reference_unknown_error",{id:d})):n.s6,f=0===r.length&&!u,_=f&&!e.required&&(0,eG.Zn)(i.yaml).has(o),b=e=>{let a=e.target,r=a.value;if(r===i$){a.value=d,i.requestAddComponent(o);return}i.emitChange(t,r===ix?"":r)},y=e.required||""===d?n.s6:p(ix,i.localize("device.id_reference_auto"),i.localize("device.id_reference_auto_detail",{domain:o})),w=(0,n.qy)`
    <wa-option
      class="id-option id-option-add ${f&&!_?"id-option-add--solo":""}"
      value=${i$}
    >
      <span class="id-option-stack">
        <span class="id-option-primary id-option-primary-add">
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${i.localize("device.id_reference_add",{domain:o})}
        </span>
      </span>
    </wa-option>
  `;return f?(0,n.qy)`
      <div class="field" data-field-key=${tA(t)}>
        ${tL(e,i)}
        <wa-select
          class=${c?"invalid":""}
          ?disabled=${tS(e,i)}
          placeholder=${i.localize(_?"device.id_reference_auto_configured":"device.id_reference_empty",{domain:o})}
          @change=${b}
        >
          ${_?p(ix,i.localize("device.id_reference_auto"),i.localize("device.id_reference_auto_detail",{domain:o})):n.s6}
          ${w}
        </wa-select>
        ${tO(t,i)}
      </div>
    `:(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <wa-select
        class=${c||v?"invalid":""}
        ?disabled=${tS(e,i)}
        placeholder=${h?(0,t_.rq)(h.name,i.substitutions)||h.id:n.s6}
        @change=${b}
      >
        ${y} ${m}
        ${r.map(e=>{let t=e.name?`${e.id} \xb7 ${o}`:o,a=(0,t_.rq)(e.name,i.substitutions);return p(e.id,a||e.id,e===h?`${t} \xb7 ${i.localize("device.default_option_tag")}`:t)})}
        ${w}
      </wa-select>
      ${tO(t,i)}${g}
    </div>
  `}(e,t,i);if(e.options&&e.options.length>0)return function(e,t,i){let o,a,r=i.getAt(t),s=tT(e,t,i,r);if(s)return s;let l=String(r??""),d=null!==i.errorAt(t),c=tS(e,i);if(e.suggestions&&e.suggestions.length>0)return tj(e,t,l,d,c,i);let h=(a=((o=String(i.getAt(["board"])??""))?(0,iM.S)(o):i.board?.esphome.variant??"").toLowerCase()).startsWith("esp32")?a:"";if(e.allow_custom_value&&e.options&&e.options.length>0){let o=(0,to.yz)(l,e.options);return(0,n.qy)`
      <div class="field" data-field-key=${tA(t)}>
        ${tL(e,i)}
        <esphome-options-combobox
          .options=${iN(e.options,h,l)}
          .value=${l}
          label=${e.label}
          placeholder=${String(e.default_value??"")}
          .defaultValue=${String(e.default_value??"")}
          .defaultNote=${i.localize("device.default_option_tag")}
          ?disabled=${c}
          ?invalid=${d}
          @options-combobox-change=${o=>i.emitChange(t,te(e,o.detail.value))}
        ></esphome-options-combobox>
        ${tO(t,i)}
        ${o?(0,n.qy)`<span class="field-warning" role="status"
                >${i.localize("validation.did_you_mean",{suggestion:o})}</span
              >`:n.s6}
      </div>
    `}let p=l.toLowerCase(),u=function(e,t,i){if(i&&"variant"===e.key&&"esp32"===t.sectionKey)return e.options?.some(e=>e.value.toLowerCase()===i)?i:void 0}(e,i,h)??(null!=e.default_value?String(e.default_value):""),m=u.toLowerCase(),v=e.options?.find(e=>e.value.toLowerCase()===m),g=v?.label??u,{clearable:f,visibleOptions:_}=function(e){let t=iU.get(e);if(!t){let i=e.options??[];t={clearable:i.some(e=>""===e.value),visibleOptions:i.filter(e=>""!==e.value)},iU.set(e,t)}return t}(e),b=iN(_,h,l);return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <wa-select
        class=${d?"invalid":""}
        ?disabled=${c}
        .withClear=${f}
        placeholder=${g}
        @change=${o=>i.emitChange(t,te(e,o.target.value))}
      >
        ${f?(0,n.qy)`<wa-icon slot="clear-icon" library="mdi" name="close"></wa-icon>`:n.s6}
        ${b.map(e=>{let t=e.value.toLowerCase()===p,o=""!==u&&e.value.toLowerCase()===m?i.localize("device.default_option_tag"):void 0;return o||e.description?(0,n.qy)`<wa-option
            value=${e.value}
            .label=${e.label}
            ?selected=${t}
          >
            ${i_(e.label,e.description,o)}
          </wa-option>`:(0,n.qy)`<wa-option value=${e.value} ?selected=${t}
              >${i_(e.label)}</wa-option
            >`})}
      </wa-select>
      ${tO(t,i)}
    </div>
  `}(e,t,i);switch(e.type){case e6.Hh.BOOLEAN:return iZ(e,t,i);case e6.Hh.SELECT:return tB(e,"text",t,i);case e6.Hh.SECURE_STRING:return tB(e,"password",t,i);case e6.Hh.INTEGER:case e6.Hh.FLOAT:return function(e,t,i){var o,a,r,s,l,d;if(e.suggestions&&e.suggestions.length>0)return tB(e,"number",t,i);let c=i.getAt(t),h=tT(e,t,i,c);if(h)return h;if("hex"===e.display_format){let s,l,d,c,h;return o=e,a=t,s=(r=i).getAt(a),l=null!==r.errorAt(a),d=tS(o,r),c=r.getEditingMagnitude(a)??iK(s),h=iK(o.default_value),tR(o,a,r,(0,n.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${l?"invalid":""}
      .value=${c}
      ?disabled=${d}
      placeholder=${h}
      @input=${e=>{let t=e.target.value;(r.setEditingMagnitude(a,t),""===t)?r.emitChange(a,""):r.emitChange(a,(0,iF.uS)((0,iF.EG)(t))||t)}}
      @blur=${()=>r.clearEditingMagnitude(a)}
    />`)}if(e.type===e6.Hh.INTEGER){let o,a,r;return s=e,l=t,o=(d=i).getEditingMagnitude(l)??String(d.getAt(l)??""),a=null!==d.errorAt(l),r=tS(s,d),tR(s,l,d,(0,n.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${a?"invalid":""}
      .value=${o}
      ?disabled=${r}
      placeholder=${String(s.default_value??"")}
      @input=${e=>{let t=e.target.value;d.setEditingMagnitude(l,t),d.emitChange(l,(0,e7.s)(t))}}
      @blur=${()=>d.clearEditingMagnitude(l)}
    />`)}if(null!=c&&!Number.isFinite(Number(String(c))))return tD(e,t,i,c);let p=String(c??""),u=null!==i.errorAt(t),m=e.range?String(e.range[0]):void 0,v=e.range?String(e.range[1]):void 0,g=tS(e,i);return tR(e,t,i,(0,n.qy)`<input
      type="number"
      class=${u?"invalid":""}
      .value=${p}
      ?disabled=${g}
      min=${m??""}
      max=${v??""}
      step="any"
      placeholder=${String(e.default_value??"")}
      @input=${o=>{let a=o.target.value;i.emitChange(t,te(e,a))}}
    />`)}(e,t,i);case e6.Hh.FLOAT_WITH_UNIT:return function(e,t,i){let o=e.unit_options??[],a=o[0]??"",r=i.getAt(t),s=tT(e,t,i,r);if(s)return s;let l=(0,e3.Eb)(r,o),d=i.getEditingMagnitude(t);if(null===l.value&&null==d&&null!=r&&""!==String(r).trim())return tD(e,t,i,r);let c=d??(null===l.value?"":String(l.value)),h=(0,e3.E3)(r,e.default_value,i.getPendingUnit(t),o),p=(0,e3.hX)(o,e.range,[a,(0,e3.Ji)(e.default_value,o),h]),u=(0,e3.x9)(e.default_value,o),m=null!==i.errorAt(t),v=tS(e,i),g=h===a,f=e.range&&g?String(e.range[0]):void 0,_=e.range&&g?String(e.range[1]):void 0,b=e=>i.emitChange(t,(0,e3.BR)(e));return(0,n.qy)`
    <div class="field float-with-unit" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <div class="float-with-unit-inputs">
        <input
          type="number"
          class=${m?"invalid":""}
          .value=${c}
          ?disabled=${v}
          min=${(0,iE.J)(f)}
          max=${(0,iE.J)(_)}
          step="any"
          placeholder=${u}
          @input=${e=>{let o=e.target.value;i.setEditingMagnitude(t,o);let a=tt(o);""===a?(i.setPendingUnit(t,h),b({value:null,unit:h})):"number"==typeof a?b({value:a,unit:h}):i.emitChange(t,a+h)}}
          @blur=${()=>i.clearEditingMagnitude(t)}
        />
        ${p.length>1?(0,n.qy)`
                <wa-select
                  data-no-value-sync
                  ?disabled=${v}
                  @change=${e=>{let o=e.target.value;null===l.value?i.setPendingUnit(t,o):b({value:l.value,unit:o})}}
                >
                  ${p.map(e=>(0,n.qy)`<wa-option value=${e} ?selected=${e===h}
                        >${e}</wa-option
                      >`)}
                </wa-select>
              `:(0,n.qy)`<span class="float-with-unit-suffix">${h}</span>`}
      </div>
      ${tO(t,i)}
    </div>
  `}(e,t,i);case e6.Hh.TIME_PERIOD:return function(e,t,i){let o=i.getAt(t),a=tT(e,t,i,o);if(a)return a;let r=iB(o),s=null!==i.errorAt(t),l=tS(e,i);if(!r.parseable)return tD(e,t,i,o);let d=void 0!==e.default_value&&null!==e.default_value?iB(e.default_value):null,c=d&&d.parseable?d.value:"",h=null!=o&&""!==o?r.unit:d?.parseable?d.unit:r.unit;return(0,n.qy)`
    <div class="field time-period" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <div class="time-period-inputs">
        <input
          type="text"
          inputmode="decimal"
          class=${s?"invalid":""}
          .value=${r.value}
          ?disabled=${l}
          placeholder=${c}
          @input=${e=>{let o=e.target.value;i.emitChange(t,ij(o,h))}}
        />
        <wa-select
          data-no-value-sync
          ?disabled=${l}
          @change=${e=>{let o=e.target.value;i.emitChange(t,ij(r.value,o))}}
        >
          ${iL.map(e=>(0,n.qy)`<wa-option value=${e} ?selected=${e===h}
                >${i.localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
      ${tO(t,i)}
    </div>
  `}(e,t,i);case e6.Hh.PIN:return function(e,t,i){let o=i.getAt(t);if((0,eC.Qd)(o)&&(0,t_.zZ)(o.number)){var a,r,s,l,d;let c,h,p;return a=e,r=t,s=i,l=o,d=o.number,c=[...r,"number"],h=null!==s.errorAt(c),p=tS(a,s),(0,n.qy)`
    <div class="field" data-field-key=${tA(r)}>
      ${tL(a,s)}
      <input
        type="text"
        autocomplete="off"
        class=${h?"invalid":""}
        .value=${d}
        ?disabled=${p}
        @input=${e=>s.emitChange(c,e.target.value)}
      />
      ${tP(d,s.substitutions,s.localize)}
      ${tO(c,s)}
      ${iG(a,r,s,l,!0,p)}
    </div>
  `}if(!i.board||0===i.board.pins.length)return tB(e,"text",t,i);let c=(0,ik.E7)(o);if("string"==typeof c)return function(e,t,i,o,a){let[r,s,l]=o.split(":");return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <input
        type="text"
        readonly
        .value=${i.localize("device.pin_on_expander",{provider:r,hub:s,channel:l})}
      />
      ${tO(t,i)}
      ${iG(e,t,i,a,(0,eC.Qd)(a),tS(e,i))}
    </div>
  `}(e,t,i,c,o);let h=("number"==typeof c?c:null)??iV(o,i.board.pins),p=i.board.esphome.platform,u=null!==h?(0,ik.m5)(h,p):(0,eC.k4)(o)?String(o??""):"",m=null!==i.errorAt(t),v=null!=e.default_value?(0,ik.j8)(e.default_value)??iV(e.default_value,i.board.pins):null,g=null!==v?i.board.pins.find(e=>e.gpio===v)?.label??(0,ik.m5)(v,p):"",f=i.board.pins;if(e.suggestions&&e.suggestions.length>0){let t=new Set(e.suggestions.map(ik.j8).filter(e=>null!==e));if(t.size>0){let e=f.filter(e=>t.has(e.gpio));e.length>0&&(f=e)}}null!==h&&!f.some(e=>e.gpio===h)&&i.board.pins.some(e=>e.gpio===h)&&(f=[i.board.pins.find(e=>e.gpio===h),...f]);let _=(0,e_.zq)(i.yaml,i.fromLine,(0,e_.lz)(i.yaml,i.fromLine)),b=function(e){let t=new Set;for(let i of e.board?.featured_components??[])if(i.component_id===e.sectionKey)for(let e of Object.values(i.locked_pins??{}))"number"==typeof e&&t.add(e);return t}(i);null!==h&&b.add(h);let y=tS(e,i),w=(0,eC.Qd)(o);return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <wa-select
        data-no-value-sync
        class=${m?"invalid":""}
        placeholder=${g}
        ?disabled=${y}
        @change=${e=>{let o=e.target.value;w?i.emitChange([...t,"number"],o):i.emitChange(t,o)}}
      >
        ${function(e,t,i,o,a,r){let s=[],l=[],d=[];for(let a of e){let e=function(e,t,i,o,a){let r=(0,ik.m5)(e.gpio,a.board?.esphome.platform),n=e.label||r,s=e.occupied_by||"",l=i.get(e.gpio)||"",d=(t.pin_mode===e6.l3.OUTPUT||t.pin_mode===e6.l3.INPUT_OUTPUT)&&e.features.includes(e6.k6.INPUT_ONLY),c=(t.pin_features??[]).every(t=>e.features.includes(t)),h=!1===e.available,p=h&&!o.has(e.gpio),u=!!(s||l),m=s?a.localize("device.pin_occupied_by",{name:s}):l?a.localize("device.pin_used_by",{name:l}):"",v=d?a.localize("device.pin_input_only"):"",g=e.notes||(h?a.localize("device.pin_unavailable"):""),f=[];return e.label&&e.label!==r&&f.push(r),m&&f.push(m),v&&f.push(v),g&&f.push(g),{optValue:r,primary:n,secondary:f.join(" • "),titleText:[m,v,g].filter(Boolean).join(" — "),warn:u||d,reserved:h,disabled:p,supported:c&&!d}}(a,t,i,o,r);(e.reserved?d:e.supported?s:l).push(e)}let c=s.length>0&&l.length>0,h=(t.pin_features??[]).map(e=>e.toUpperCase()).join(", "),p=(e,t)=>(0,n.qy)`${t?(0,n.qy)`<wa-divider class="pin-group-divider" aria-hidden="true"></wa-divider>`:n.s6} <small class="pin-group-label" aria-hidden="true">${e}</small>`;return(0,n.qy)`
    ${c&&h?p(r.localize("device.pin_group_supports",{features:h}),!1):n.s6}
    ${s.map(e=>iH(e,a))}
    ${c?p(r.localize("device.pin_group_other"),!0):n.s6}
    ${l.map(e=>iH(e,a))}
    ${d.length>0?p(r.localize("device.pin_group_reserved"),!0):n.s6}
    ${d.map(e=>iH(e,a))}
  `}(f,e,_,b,u,i)}
      </wa-select>
      ${tO(t,i)}
      ${iG(e,t,i,o,w,y)}
    </div>
  `}(e,t,i);case e6.Hh.COLOR:let a;return a=i.getAt(t),(0,to.rf)(a)&&!(0,iP.fd)(String(a))?tD(e,t,i,a):tB(e,"color",t,i);case e6.Hh.MAC_ADDRESS:return tB(e,"text",t,i);case e6.Hh.LAMBDA:return oq(e,t,i);case e6.Hh.JSON:return function(e,t,i){let o=i.getAt(t),a=o instanceof eG.ho;if(!a){let a=tT(e,t,i,o);if(a)return a}let r=a?o.body:String(o??""),s=null!==i.errorAt(t);return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <textarea
        class="textarea-field ${s?"invalid":""}"
        rows="4"
        ?disabled=${tS(e,i)}
        .value=${r}
        placeholder=${String(e.default_value??"")}
        @input=${e=>{let r=e.target.value;i.emitChange(t,a?eG.ho.fromBodyText(r,o):r)}}
      ></textarea>
      ${tO(t,i)}
    </div>
  `}(e,t,i);case e6.Hh.ICON:let r=i.getAt(t),s=tT(e,t,i,r);if(s)return s;let l=String(r??""),d=null!==i.errorAt(t);return(0,n.qy)`
    <div class="field" data-field-key=${tA(t)}>
      ${tL(e,i)}
      <esphome-mdi-icon-picker
        .value=${l}
        .invalid=${d}
        .disabled=${tS(e,i)}
        .placeholder=${String(e.default_value??"Choose an icon…")}
        @change=${e=>i.emitChange(t,e.detail.value)}
      ></esphome-mdi-icon-picker>
      ${tO(t,i)}
    </div>
  `;case e6.Hh.TRIGGER:return(0,n.qy)`<div class="field" data-field-key=${tA(t)}>
          ${tE(e,i)}
          <button
            type="button"
            class="edit-actions-button"
            ?disabled=${i.disabled}
            @click=${()=>this._emitEditActionField(e.key)}
          >
            ${i.localize("device.automation_action_field_edit")}
          </button>
        </div>`;case e6.Hh.UNKNOWN:return tI(e,t,i);default:return tB(e,"text",t,i)}}_buildCtx(){let e=new Set;for(let t of this.requiredGroups)for(let i of t.keys)e.add(i);for(let t of this.entries)t.group&&e.add(t.key);let t={localize:this._localize,disabled:this.disabled,yaml:this.yaml,substitutions:this._parseSubstitutions(this.yaml),fromLine:this.fromLine,sectionKey:this.sectionKey,deviceName:t5(this._devices,this.configuration),board:this.board,pinRegistryModes:this._pinRegistryModes.value,requiredOnly:this.requiredOnly,showAdvanced:this.showAdvanced,presentComponents:this.presentComponents,reactiveConstraintKeys:e,entries:this.entries,nestedOpenSections:this._nestedOpenSections,getAt:e=>(0,eC.O6)(this.values,e),errorAt:e=>this.errors.get(e.join("."))??null,emitChange:(e,t)=>this._emitChange(e,t),toggleNested:e=>this._toggleNested(e),seedNestedOpen:e=>this._seedNestedOpen(e),requestAddComponent:e=>this._requestAddComponent(e),resolveInterfaceProviders:e=>this._resolveInterfaceProviders(e),scopeValues:e=>this._scopeValues(e),filterRenderable:this._filterRenderable,getPendingUnit:e=>this._pendingUnits.get(e.join(".")),setPendingUnit:(e,t)=>{this._pendingUnits.set(e.join("."),t),this.requestUpdate()},getEditingMagnitude:e=>this._editingMagnitudes.get(e.join(".")),setEditingMagnitude:(e,t)=>{this._editingMagnitudes.set(e.join("."),t)},clearEditingMagnitude:e=>{this._editingMagnitudes.delete(e.join("."))},clearEditingMagnitudesUnder:e=>{let t=e.join("."),i=`${t}.`;for(let e of[...this._editingMagnitudes.keys()])(e===t||e.startsWith(i))&&this._editingMagnitudes.delete(e)},getClusterChoice:e=>this._constraintClusters.getChoice(e),setClusterChoice:(e,t)=>this._constraintClusters.setChoice(e,t),getClusterStash:(e,t)=>this._constraintClusters.getStash(e,t),setClusterStash:(e,t,i)=>this._constraintClusters.setStash(e,t,i),clearClusterStash:(e,t)=>this._constraintClusters.clearStash(e,t),stashOwner:this,renderEntry:()=>n.s6};return t.renderEntry=(e,i)=>this._renderEntry(e,i,t),t}_scopeValues(e){let t=(0,eC.O6)(this.values,e);return t&&"object"==typeof t&&!Array.isArray(t)?t:{}}_emitChange(e,t){this.dispatchEvent(new CustomEvent("value-change",{detail:{path:e,value:t},bubbles:!0,composed:!0}))}_emitEditActionField(e){this.dispatchEvent(new CustomEvent("edit-action-field",{detail:{field:e},bubbles:!0,composed:!0}))}_toggleNested(e){let t=new Set(this._nestedOpenSections);t.has(e)?t.delete(e):t.add(e),this._nestedOpenSections=t}openNested(e){if(this._nestedOpenSections.has(e))return;let t=new Set(this._nestedOpenSections);t.add(e),this._nestedOpenSections=t}_seedNestedOpen(e){this._seededNestedOpen.has(e)||(this._seededNestedOpen.add(e),this._nestedOpenSections.add(e))}_requestAddComponent(e){(0,Z.r)(this,"request-add-component",{domain:e})}_resolveInterfaceProviders(e){if(!e)return[];let t=this._interfaceProviders.get(e);return t||(this._api&&!this._interfaceProvidersPending.has(e)&&(this._interfaceProvidersPending.add(e),(0,eQ._)(this._api,{provides:e}).then(t=>{this._interfaceProviders.set(e,t.map(t=>(0,e_.G_)(t,e))),this.requestUpdate()}).catch(t=>console.warn("[config-entry-form] provider fetch failed for",e,t)).finally(()=>this._interfaceProvidersPending.delete(e))),null)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._pinRegistryModes=new ii(this,{getCached:t9,subscribe:t7,fetch:ie},()=>this._api),this.entries=[],this.values={},this.requiredGroups=[],this.errors=new Map,this.board=null,this.disabled=!1,this.showAdvanced=!1,this.advancedSection=!1,this.forceAdvancedControl=!1,this.gateAdvanced=!1,this.advancedExtraCount=0,this.requiredOnly=!1,this.yaml="",this.sectionKey="",this.configuration="",this.presentComponents=new Set,this._nestedOpenSections=new Set,this._seededNestedOpen=new Set,this._interfaceProviders=new Map,this._interfaceProvidersPending=new Set,this._fieldScroll=new ic(this),this._fieldFocus=new ir(this),this._pendingUnits=new Map,this._editingMagnitudes=new Map,this._constraintClusters=new io(this),this._openAdvancedPlacement=new Map,this._filterRenderable=(e,t)=>ts(e,t,tr(this)),this._parseSubstitutions=(0,l.A)(t_.Gr)}}function oK(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}oj.styles=[tq,(0,n.AH)`
      /* "Show advanced settings" switch (advanced-section mode): sits at the
         basic/advanced boundary; flipping it on reveals the advanced fields
         rendered below it. */
      .advanced-toggle-row {
        display: flex;
        font-size: var(--wa-font-size-s);
      }

      .advanced-toggle-row wa-switch {
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-quiet);
      }
    `],oB([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],oj.prototype,"_localize",void 0),oB([(0,a.Fg)({context:_.Ie,subscribe:!0}),(0,s.wk)()],oj.prototype,"_api",void 0),oB([(0,a.Fg)({context:_.xJ,subscribe:!0}),(0,s.wk)()],oj.prototype,"_devices",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"entries",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"values",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"requiredGroups",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"errors",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"board",void 0),oB([(0,s.MZ)({type:Boolean})],oj.prototype,"disabled",void 0),oB([(0,s.MZ)({type:Boolean,attribute:"show-advanced"})],oj.prototype,"showAdvanced",void 0),oB([(0,s.MZ)({type:Boolean,attribute:"advanced-section"})],oj.prototype,"advancedSection",void 0),oB([(0,s.MZ)({type:Boolean,attribute:"force-advanced-control"})],oj.prototype,"forceAdvancedControl",void 0),oB([(0,s.MZ)({type:Boolean,attribute:"gate-advanced"})],oj.prototype,"gateAdvanced",void 0),oB([(0,s.MZ)({type:Number,attribute:"advanced-extra-count"})],oj.prototype,"advancedExtraCount",void 0),oB([(0,s.MZ)({type:Boolean,attribute:"required-only"})],oj.prototype,"requiredOnly",void 0),oB([(0,s.MZ)()],oj.prototype,"yaml",void 0),oB([(0,s.MZ)({type:Number,attribute:"from-line"})],oj.prototype,"fromLine",void 0),oB([(0,s.MZ)({attribute:"section-key"})],oj.prototype,"sectionKey",void 0),oB([(0,s.MZ)()],oj.prototype,"configuration",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"presentComponents",void 0),oB([(0,s.MZ)({attribute:!1})],oj.prototype,"focusFieldPath",void 0),oB([(0,s.wk)()],oj.prototype,"_nestedOpenSections",void 0),oj=oB([(0,s.EM)("esphome-config-entry-form")],oj),(0,M.C)({"alert-circle-outline":r.mdiAlertCircleOutline});class oU extends n.WF{get currentValues(){return{...this._values}}get _entries(){return this._overlayOptions(this._overlayRequired(this.component.config_entries,this.extraRequired),this.optionOverrides)}willUpdate(e){super.willUpdate(e),(e.has("component")||!this._initialized)&&this.component&&(this._initialized=!0,this._initValues(),this._localBlockMessage="",this._depResolver.kickoff(this.component.dependencies??[])),(e.has("component")||e.has("yaml")||e.has("board"))&&this._resolveProvidedDeps()}_missingDeps(e){return e1(this.component.dependencies??[],this.yaml,e).filter(e=>!this._providedDeps.has(e))}async _resolveProvidedDeps(){let e=++this._providesSeq;this._providedDeps.size&&(this._providedDeps=new Set);let t=this._api,i=this.component?.dependencies??[];if(!t||0===i.length)return;let o=(0,eG.Zn)(this.yaml),a=e1(i,this.yaml,o);if(0!==a.length)try{let i=await e2(t,a,o,{platform:this.board?.esphome.platform??null,boardId:this.board?.id??null});e===this._providesSeq&&(i.size||this._providedDeps.size)&&(this._providedDeps=i)}catch(e){console.warn("[add-component-form] provides lookup failed",e)}}_initValues(){this._values=tY({entries:this._entries,component:this.component,board:this.board,yaml:this.yaml,prefillReference:this.prefillReference,prefillFields:this.prefillFields,restoredValues:this.restoredValues,localize:this._localize})}render(){let e=this.submitting,t=(0,eG.Zn)(this.yaml),i=this._missingDeps(t),o=(0,to.JK)(this._entries,this._values,t,this.board?.esphome.platform??null),a=!this._hasRequiredErrors(o);return(0,n.qy)`
      <div class="form">
        <p class="form-desc">${(0,en.Gc)(this.component.description)}</p>
        ${i.length>0?this._renderMissingDeps(i):n.s6}
        <esphome-config-entry-form
          .entries=${this._entries}
          .requiredGroups=${this.component.required_groups??[]}
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
        ${this._showYaml?(0,n.qy)`<pre class="yaml-preview">${this._generateYamlPreview()}</pre>`:n.s6}
        ${this.submitError?(0,n.qy)`<p class="error">${this.submitError}</p>`:n.s6}
        ${this._localBlockMessage?(0,n.qy)`<p class="error">${this._localBlockMessage}</p>`:n.s6}
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
            ?disabled=${e||!a||i.length>0}
            @click=${this._onSubmit}
          >
            ${this.submitting?this._localize("device.adding"):this._localize("device.add_component_action")}
          </button>
        </div>
      </div>
    `}_renderMissingDeps(e){return(0,n.qy)`
      <div class="deps-warning" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div class="deps-warning-body">
          <div class="deps-warning-title">
            ${this._localize("device.missing_dependencies_title",{name:this.component.name})}
          </div>
          <div>${this._localize("device.missing_dependencies_body")}</div>
          <div class="deps-warning-actions">
            ${e.map(e=>(0,n.qy)`<button
                  type="button"
                  class="dep-button"
                  @click=${()=>this._onAddDep(e)}
                >
                  ${this._localize("device.missing_dependencies_add",{domain:this._depResolver.resolve(e)})}
                </button>`)}
          </div>
        </div>
      </div>
    `}_onAddDep(e){(0,Z.r)(this,"navigate-to-dep",{domain:e})}_hasRequiredErrors(e){for(let t of e.values())if("validation.required"===t.code)return!0;return!1}_labelForErrorKey(e){let t,i=e.split("."),o=this._entries;for(let e of i){if(!o||!(t=o.find(t=>t.key===e)))break;o=t.type===e6.Hh.NESTED?t.config_entries??[]:null}return t?tm(t,this._localize):e}_anyErrorIsVisible(e,t){var i,o;if(0===e.size)return!1;let a=(i=this._entries,o=this._values,function e(t,i,o,a=[],r=new Set){for(let n of ts(t,i,o)){if(n.type===e6.Hh.NESTED){let t=n.config_entries??[];n.multi_value?(0,eC.ly)(i[n.key]).forEach((i,s)=>{e(t,i,o,[...a,n.key,String(s)],r)}):e(t,(0,eC.qY)(i[n.key]),o,[...a,n.key],r),r.add([...a,n.key].join("."));continue}n.multi_value&&Array.isArray(i[n.key])&&i[n.key].forEach((e,t)=>{r.add([...a,n.key,String(t)].join("."))}),r.add([...a,n.key].join("."))}return r}(i,o,tW(o,this.board,t)));for(let t of e.keys())if(a.has(t))return!0;return!1}_onValueChange(e){let{path:t,value:i}=e.detail;this._values=(0,eC.Oe)(this._values,t,i);let o=(0,to.iL)(this._errors,t.join("."));o&&(this._errors=o),this._localBlockMessage&&(this._localBlockMessage="")}_generateYamlPreview(){let e=(0,eN.Ze)(this.component.id,this.board),t=[`${e}:`];return t.push(...(0,eG.ym)(this._values,"  ")),t.join("\n")}_onCancel(){(0,Z.r)(this,"form-cancel")}_onSubmit(){this._localBlockMessage="";let e=(0,eG.Zn)(this.yaml),t=this._missingDeps(e);if(t.length>0){this._localBlockMessage=`${this._localize("device.missing_dependencies_title",{name:this.component.name})} (${t.join(", ")})`;return}let i=(0,to.JK)(this._entries,this._values,e,this.board?.esphome.platform??null);if(i.size>0){if(this._errors=i,!this._anyErrorIsVisible(i,e)){let e=[...i.entries()].map(([e,t])=>`${this._labelForErrorKey(e)}: ${this._localize(t.code,t.params)}`).join("; ");this._localBlockMessage=`${this._localize("device.add_component_hidden_validation_error")} (${e})`}return}this._errors=new Map,this._localBlockMessage="";let o=ti(this._entries,this._values);(0,Z.r)(this,"form-submit",{fields:o})}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this.yaml="",this.prefillReference=null,this.prefillFields=null,this.extraRequired=null,this.restoredValues=null,this.optionOverrides=null,this.submitting=!1,this.submitError="",this._values={},this._errors=new Map,this._localBlockMessage="",this._showYaml=!1,this._providedDeps=new Set,this._providesSeq=0,this._depResolver=new t0(this,()=>this._api,()=>this.board?.esphome.platform||void 0),this._overlayRequired=(0,l.A)(t1),this._overlayOptions=(0,l.A)(t2),this._initialized=!1}}oU.styles=[b.G,ep.z9,tX.V,t6],oK([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],oU.prototype,"_localize",void 0),oK([(0,a.Fg)({context:_.Ie})],oU.prototype,"_api",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"component",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"board",void 0),oK([(0,s.MZ)()],oU.prototype,"yaml",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"prefillReference",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"prefillFields",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"extraRequired",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"restoredValues",void 0),oK([(0,s.MZ)({attribute:!1})],oU.prototype,"optionOverrides",void 0),oK([(0,s.MZ)({type:Boolean})],oU.prototype,"submitting",void 0),oK([(0,s.MZ)()],oU.prototype,"submitError",void 0),oK([(0,s.wk)()],oU.prototype,"_values",void 0),oK([(0,s.wk)()],oU.prototype,"_errors",void 0),oK([(0,s.wk)()],oU.prototype,"_localBlockMessage",void 0),oK([(0,s.wk)()],oU.prototype,"_showYaml",void 0),oK([(0,s.wk)()],oU.prototype,"_providedDeps",void 0),oU=oK([(0,s.EM)("esphome-add-component-form")],oU);var oZ=i(8719),oN=i(4996),oV=i(9295),oH=i(1188),oG=i(1448);class oW{hostConnected(){this._observer.observe(this._host)}hostDisconnected(){this._observer.disconnect()}constructor(e,t){this._host=e,this._observer=new ResizeObserver(t),e.addController(this)}}var oY=i(2814),oJ=i(2743),oQ=i(1148);let oX=(0,l.A)(eG.Zn),o0=(0,l.A)(eG.u),o1=(0,l.A)(eH);function o2(e,t){let i=e.fields?.id?.value;return"string"==typeof i&&t.has(i)}function o6(e,t){return!!e.locked_pins&&(0,e_.cN)(t,(0,e_.iZ)(e.component_id).domain,e.locked_pins)}function o3(e){let t=oX(e.yaml),i=o0(e.yaml),o=e.lockedCategories.length>0,a=e._components.filter(t=>(0,to.Cs)(t.supported_platforms,e.platform)),r=o?new Set(a.map(e=>e.id)):null,n=new Map,s=e.board;if(s)for(let e of s.featured_components??[])n.set((0,eN.m0)(s.id,e.id),e);let l=n.size?o1(e.yaml):new Set;return a.filter(o=>{let a=n.get(o.id);if(a&&(o2(a,l)||o6(a,e.yaml)))return!1;let s=a?.component_id??o.id;return!(!o.multi_conf&&(0,eJ.by)(s,t,i)||r&&o.id.includes(".")&&o.dependencies.length>0&&!o.dependencies.every(e=>r.has(e)||t.has(e)))&&!0})}let o5=(0,l.A)((e,t)=>{let i=e?.featured_bundles??[];if(!e||0===i.length)return new Set;let o=new Map;for(let t of e.featured_components??[]){let e=t.fields?.id?.value;"string"==typeof e&&o.set(t.id,e)}let a=o1(t),r=new Set;for(let e of i){let t=e.component_ids.map(e=>o.get(e)).filter(e=>void 0!==e);t.length>0&&t.every(e=>a.has(e))&&r.add(e.id)}return r});function o4(e){let t=o5(e.board,e.yaml);return(e.board?.featured_bundles??[]).filter(e=>!t.has(e.id))}function o8(e){let t=(e._search??"").trim();return o4(e).filter(e=>(0,oQ.K)(t,e.name,e.description,e.id))}function o9(e,t){let i=e.board;if(!i)return 0;let o=i.featured_components??[],a=oX(e.yaml),r=o0(e.yaml),n=o.length?o1(e.yaml):new Set,s=t?.applyQuery??!0,l=s?(e._search??"").trim():"";return o.filter(t=>!o2(t,n)&&!o6(t,e.yaml)&&(!1!==t.multi_conf||!(0,eJ.by)(t.component_id,a,r))&&(0,oQ.K)(l,t.name??void 0,t.description??void 0,t.id)).length+(s?o8(e):o4(e)).length}function o7(e){let t=e.target;return!t?.closest("a, button")}function ae(e,t){return(0,n.qy)`<span
      id=${e}
      class="component-category-chip component-category-chip--recommended"
      tabindex=${t?"0":"-1"}
      >${tQ("featured")}</span
    >
    ${t?(0,n.qy)`<wa-tooltip for=${e}>${t}</wa-tooltip>`:n.s6}`}function at(e,t){let i=e._expandedId===t;return(0,n.qy)`<button
    class="expand-button"
    type="button"
    aria-pressed=${i}
    title=${e._localize("wizard.expand_board")}
    @click=${()=>e._onToggleExpand(t)}
  >
    <wa-icon
      library="mdi"
      name=${i?"arrow-collapse-all":"arrow-expand-all"}
    ></wa-icon>
  </button>`}let ai=(0,n.AH)`
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
    outline: var(--esphome-focus-outline);
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

  /* Board-recommendation identity: same pill as its sibling chips so the
     row reads as one family, recolored primary so it stands out from the
     muted category chips (frontend #1220). */
  .component-category-chip--recommended {
    color: var(--esphome-primary);
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
    font-weight: var(--wa-font-weight-bold);
  }

  /* Focusable (tabindex) so keyboard users can raise the explainer
     tooltip; wa-tooltip's default trigger is hover+focus. */
  .component-category-chip--recommended:focus-visible {
    outline: none;
    box-shadow: var(--esphome-focus-ring-tight);
  }

  .component-description {
    margin: 0;
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.4;
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
    outline: var(--esphome-focus-outline);
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

  /* Featured cards read as the curated set via a thicker edge in the same
     neutral border color — distinguished by weight, not hue, so it stays
     subtle. Drawn as an inset ring (box-shadow), not a wider border, so the
     box model — and thus the card size — matches the regular cards beside it. */
  .component-card--featured {
    --featured-ring: var(--wa-color-surface-border);
    box-shadow: inset 0 0 0 var(--wa-border-width-s) var(--featured-ring);
    /* transition doesn't accumulate across rules, so restate the base card's
       animated properties alongside the ring. */
    transition:
      border-color var(--wa-transition-normal) var(--wa-transition-easing),
      box-shadow var(--wa-transition-normal) var(--wa-transition-easing),
      background var(--wa-transition-normal) var(--wa-transition-easing);
  }

  /* Track the border's primary highlight on hover / focus so the ring doesn't
     stay a stale neutral while the border lights up. */
  .component-card--featured:hover,
  .component-card--featured:focus-within {
    --featured-ring: var(--esphome-primary);
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
`;function ao(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}i(1306),(0,M.C)({"arrow-collapse-all":r.mdiArrowCollapseAll,"arrow-expand-all":r.mdiArrowExpandAll,memory:r.mdiMemory,"open-in-new":r.mdiOpenInNew,"package-variant-closed":r.mdiPackageVariantClosed,plus:r.mdiPlus});class aa extends n.WF{get _components(){return this._list.items}get _total(){return this._list.total}_prefersFeatured(){return 0===this.lockedCategories.length&&!!this.boardId&&o9(this,{applyQuery:!1})>0}_recommendationInclusive(){return this._category===eW.FEATURED||"all"===this._category}load(){this._provides="",this._prefersFeatured()?this._category=eW.FEATURED:this._category===eW.FEATURED&&(this._category="all"),this._fetchComponents()}filterByDomain(e){Object.values(eW).includes(e)?(this._search="",this._provides="",this._category=e):(this._search=e,this._provides=e,this._category="all"),this._fetchComponents()}_fetchComponents(){let e=this._search.trim()||void 0,t=this.lockedCategories.length>0,i={category:t?this.lockedCategories:"all"!==this._category?this._category:void 0,exclude_category:!t&&this.excludeCategories.length>0?this.excludeCategories:void 0,platform:this.platform||void 0,board_id:this.boardId||void 0},o=this._provides;this._list.reset(async(t,a)=>{let r=o?await this._api.getComponents({...i,offset:t,limit:a,provides:o}):await this._api.getComponents({...i,offset:t,limit:a,query:e});return 0===t&&o&&0===r.components.length&&(this._provides="",o="",r=await this._api.getComponents({...i,offset:t,limit:a,query:e})),0===t&&(this._categories=r.categories),{items:r.components,total:r.total}})}firstUpdated(){document.fonts?.ready.then(()=>this._measureDescriptionOverflow())}updated(){this._measureDescriptionOverflow(),this._list.loading||0!==this.lockedCategories.length||this._category!==eW.FEATURED||this._provides||o3(this).length+o8(this).length!==0||(this._category="all",this._fetchComponents())}render(){var e;let t,i,o,a,r,s,l,d;if(this._list.loading&&!this._list.hasLoaded)return(0,n.qy)`<div class="loading">
        ${this._localize("device.loading_components")}
      </div>`;let c=(e=this._localize,t=new Set(this.excludeCategories),i=this._categories.filter(e=>!t.has(e.id)),o=this.lockedCategories.length?0:o9(this),a=i.filter(e=>e.id!==eW.FEATURED),r=t.size?a.reduce((e,t)=>e+t.count,0)+o:this._total,s=new Intl.Collator(void 0,{sensitivity:"base"}),l=a.map(e=>({id:e.id,label:tQ(e.id),count:e.count})).sort((e,t)=>s.compare(e.label,t.label)),d=[],o>0&&d.push({id:eW.FEATURED,label:e("device.component_category_featured"),count:o}),d.push({id:"all",label:e("device.component_category_all"),count:r}),d.push(...l),d),h=0===this.lockedCategories.length,p=this._recommendationInclusive()?o8(this):[],u=o3(this),m=function(e){let t=new Map;for(let i of e){let e=JSON.stringify([i.category,i.name]),o=t.get(e);o?o.push(i):t.set(e,[i])}let i=new Set;for(let e of t.values())if(e.length>1)for(let t of e)i.add(t.id);return i}(u);return(0,n.qy)`
      ${h?(0,n.qy)`<div class="sidebar">
              <p class="sidebar-label">
                ${this._localize("device.component_categories")}
              </p>
              ${c.map(({id:e,label:t,count:i})=>(0,n.qy)`
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
            </div>`:n.s6}
      <div class="main">
        <input
          type="search"
          autocomplete="off"
          .value=${this._search}
          @input=${this._onSearchInput}
          placeholder=${this._localize("device.search_components_placeholder")}
        />
        ${!this._list.loading?(0,n.qy)`<span class="result-count"
                >${this._localize("device.components_count",{visible:u.length+p.length,total:this._total+p.length})}</span
              >`:n.s6}
        <div class="grid-scroll">
          <div class="components-grid">
            ${this._list.loading?(0,n.qy)`<p class="empty">
                    ${this._localize("device.loading_components")}
                  </p>`:u.length+p.length?(0,n.qy)`
                      ${p.map(e=>{var t;let i,o,a,r,s;return t=this,i=!!e.image_url&&!t._imageFailed.has(e.id),o=t.board?t._localize("device.recommended_chip_tooltip",{board:t.board.name}):"",a=`bundle.${e.id}`,s=(r=t._expandedId===a)||t._overflowingDescriptions.has(a),(0,n.qy)`
    <article
      class="component-card component-card--featured ${r?"component-card--expanded":""}"
      @click=${i=>{o7(i)&&t._onAddBundle(e)}}
    >
      <div class="component-card-header">
        ${i?(0,n.qy)`<div class="component-image">
                <img
                  src=${e.image_url}
                  alt=${e.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>t._onImageError(e.id)}
                />
              </div>`:(0,n.qy)`<div class="component-image--placeholder">
                <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
              </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title truncate">${e.name}</h3>
          ${ae(`recommended-chip-bundle-${e.id}`,o)}
        </div>
        <span class="bundle-badge">
          <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
          ${t._localize("device.featured_bundle_badge")}
        </span>
        ${s?at(t,a):n.s6}
      </div>
      ${e.description?(0,n.qy)`<p
              class="component-description ${r?"":"component-description--clamp line-clamp-2"}"
              data-component-id=${a}
            >
              ${(0,en.Gc)(e.description)}
            </p>`:n.s6}
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
                      ${u.map(e=>(function(e,t,i,o,a,r=!1){var s,l;let d,c=!!t.image_url&&!e._imageFailed.has(t.id),h=i||e._overflowingDescriptions.has(t.id),p="all"===(s=e._category)||"featured"===s?tQ((o?t.underlying_category:t.category)??""):"",u=r?-1===(d=(l=t.id).indexOf("."))?"":l.slice(d+1).split("_").filter(e=>e.length>0).map(e=>e.toUpperCase()).join(" "):"",m=o&&e.board?a("device.recommended_chip_tooltip",{board:e.board.name}):"";return(0,n.qy)`
    <article
      class="component-card ${i?"component-card--expanded":""} ${o?"component-card--featured":""}"
      @click=${i=>{o7(i)&&e._onAdd(t)}}
    >
      <div class="component-card-header">
        ${c?(0,n.qy)`<div class="component-image">
                <img
                  src=${t.image_url}
                  alt=${t.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>e._onImageError(t.id)}
                />
              </div>`:(0,n.qy)`<div class="component-image--placeholder">
                <wa-icon library="mdi" name="memory"></wa-icon>
              </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title truncate">${t.name}</h3>
          ${o?ae(`recommended-chip-${t.id}`,m):n.s6}
          ${p?(0,n.qy)`<span class="component-category-chip">${p}</span>`:n.s6}
          ${u?(0,n.qy)`<span class="component-category-chip">${u}</span>`:n.s6}
        </div>
        ${h?at(e,t.id):n.s6}
      </div>
      <p
        class="component-description ${i?"":"component-description--clamp line-clamp-2"}"
        data-component-id=${t.id}
      >
        ${(0,en.Gc)(t.description)}
      </p>
      <div class="card-footer">
        <a class="more-info" href=${t.docs_url} target="_blank" rel="noreferrer">
          ${a("device.more_info")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <button
          class="select-component"
          type="button"
          @click=${()=>e._onAdd(t)}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${a("device.add_component_action")}
        </button>
      </div>
    </article>
  `})(this,e,e.id===this._expandedId,(0,eN.sO)(e.id),this._localize,m.has(e.id)))}
                    `:(0,n.qy)`<p class="empty">
                      ${this._localize(this._list.hasError?"device.components_load_error":"device.no_components_found")}
                    </p>`}
          </div>
          ${(0,oJ.F)({loadingMore:this._list.loadingMore,error:this._list.hasError&&this._list.items.length>0,hasMore:this._list.hasMore,localize:this._localize,loadingLabelKey:"device.loading_components",errorLabelKey:"device.components_load_more_error",onRetry:()=>this._list.loadMore()})}
        </div>
      </div>
    `}_onToggleExpand(e){this._expandedId=this._expandedId===e?null:e}_measureDescriptionOverflow(){if(!(0,oH.z)(this))return;let e=function(e){let t=new Set;for(let i of e){let e=i.dataset.componentId;e&&i.scrollHeight>i.clientHeight&&t.add(e)}return t}(this._clampedDescriptions);this._expandedId&&e.add(this._expandedId),this._overflowingDescriptions=e}_onImageError(e){if(this._imageFailed.has(e))return;let t=new Set(this._imageFailed);t.add(e),this._imageFailed=t}_onAdd(e){(0,Z.r)(this,"add-component",{component:e})}_onAddBundle(e){(0,Z.r)(this,"add-bundle",{bundle:e,boardId:this.boardId})}constructor(...e){super(...e),this._localize=e=>e,this.platform="",this.boardId="",this.board=null,this.yaml="",this.lockedCategories=[],this.excludeCategories=[],this._list=new oG.S(this),this._categories=[],this._search="",this._category="all",this._provides="",this._expandedId=null,this._imageFailed=new Set,this._overflowingDescriptions=new Set,this._resize=new oW(this,()=>this._measureDescriptionOverflow()),this._intersection=new oV.Q(this,()=>this._list.loadMore()),this._debouncedSearch=(0,oN.s)(()=>this._fetchComponents(),300),this._onSearchInput=e=>{this._search=e.target.value,this._provides="",this._recommendationInclusive()&&this._prefersFeatured()&&(this._category=this._search.trim()?"all":eW.FEATURED),this._debouncedSearch()}}}function ar(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aa.styles=[b.G,ep.z9,U.U,ai,oZ.f],ao([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aa.prototype,"_localize",void 0),ao([(0,a.Fg)({context:_.Ie})],aa.prototype,"_api",void 0),ao([(0,s.MZ)()],aa.prototype,"platform",void 0),ao([(0,s.MZ)({attribute:"board-id"})],aa.prototype,"boardId",void 0),ao([(0,s.MZ)({attribute:!1})],aa.prototype,"board",void 0),ao([(0,s.MZ)()],aa.prototype,"yaml",void 0),ao([(0,s.MZ)({attribute:!1})],aa.prototype,"lockedCategories",void 0),ao([(0,s.MZ)({attribute:!1})],aa.prototype,"excludeCategories",void 0),ao([(0,s.wk)()],aa.prototype,"_categories",void 0),ao([(0,s.wk)()],aa.prototype,"_search",void 0),ao([(0,s.wk)()],aa.prototype,"_category",void 0),ao([(0,s.wk)()],aa.prototype,"_provides",void 0),ao([(0,s.wk)()],aa.prototype,"_expandedId",void 0),ao([(0,s.wk)()],aa.prototype,"_imageFailed",void 0),ao([(0,s.wk)({hasChanged:(e,t)=>!t||!(0,oY.c)(e,t)})],aa.prototype,"_overflowingDescriptions",void 0),ao([(0,s.YG)(".component-description--clamp[data-component-id]")],aa.prototype,"_clampedDescriptions",void 0),aa=ao([(0,s.EM)("esphome-component-catalog")],aa),(0,M.C)({close:r.mdiClose,"arrow-left":r.mdiArrowLeft,"package-variant-closed":r.mdiPackageVariantClosed});class an extends n.WF{get _restoredValuesForMount(){return this._returnTo?null:this._returnValues}open(){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0,this.updateComplete.then(()=>this._catalog?.load())}openWithSearch(e){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0,this.updateComplete.then(()=>this._catalog?.filterByDomain(e))}_clearDetourFields(){this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._depPrefill=null,this._returnValues=null}_resetDetourState(){this._clearDetourFields(),this._bundleQueue=[],this._bundleProgress=null,this._depNavSeq++,this._selectionSeq++}render(){var e;let t=null!==this._selected,i=this.lockedCategories.length>0,o=i?this.boardName?"device.add_config_dialog_title":"device.add_config":this.boardName?"device.add_component_dialog_title":"device.add_component",a=t?function(e,t,i){if(i.core)return e;let o=tQ(t);return o?`${e} \xb7 ${o}`:e}(this._selected.name,this._selected.category,{core:i}):this.boardName?this._localize(o,{name:this.boardName}):this._localize(o);return(0,n.qy)`
      <esphome-base-dialog
        class=${t?"form-view":""}
        ?open=${this._dialog.open}
        ?busy=${this._submitting}
        .label=${a}
        @request-close=${this._dialog.onRequestClose}
        @add-component=${this._onComponentSelected}
        @add-bundle=${this._onBundleSelected}
        @form-cancel=${this._onBack}
        @form-submit=${this._onFormSubmit}
        @navigate-to-dep=${this._onNavigateToDep}
        @request-add-component=${this._onNavigateToDep}
      >
        ${t?(0,n.qy)`<button
                slot="header-prefix"
                class="back-button"
                title=${this._localize("layout.back")}
                aria-label=${this._localize("layout.back")}
                @click=${this._onBack}
              >
                <wa-icon library="mdi" name="arrow-left"></wa-icon>
              </button>`:n.s6}
        ${this._returnTo?(0,n.qy)`<div class="return-banner">
                ${this._localize("device.return_to_after_dep_prefix")}
                <strong>${this._returnTo.name}</strong>
                ${this._localize("device.return_to_after_dep_suffix")}
              </div>`:n.s6}
        ${t&&this._bundleProgress?(0,n.qy)`<div class="bundle-banner">
                <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
                <span
                  >${this._localize("device.bundle_step_progress",{current:this._bundleProgress.current,total:this._bundleProgress.total,name:this._bundleProgress.bundleName})}</span
                >
              </div>`:n.s6}
        ${!t&&this._submitError?(0,n.qy)`<div class="catalog-error" role="alert">${this._submitError}</div>`:n.s6}
        <esphome-component-catalog
          ?hidden=${t}
          .platform=${this.platform}
          .boardId=${this.board?.id??""}
          .board=${this.board}
          .yaml=${this.yaml}
          .lockedCategories=${this.lockedCategories}
          .excludeCategories=${(e={isCoreLocked:i,isInDepDetour:null!==this._returnTo}).isCoreLocked||e.isInDepDetour?[]:eY}
        ></esphome-component-catalog>
        ${t?(0,n.qy)`<esphome-add-component-form
                .component=${this._selected}
                .board=${this.board}
                .yaml=${this.yaml}
                .prefillReference=${this._prefillReference}
                .prefillFields=${this._depPrefill?.fields??null}
                .restoredValues=${this._restoredValuesForMount}
                .extraRequired=${this._depPrefill?.required??null}
                .optionOverrides=${this._depPrefill?.optionOverrides??null}
                .submitting=${this._submitting}
                .submitError=${this._submitError}
              ></esphome-add-component-form>`:n.s6}
      </esphome-base-dialog>
    `}async _onComponentSelected(e){e.stopPropagation();let t=await e8(this,e.detail.component.id);if("stale"===t.kind)return;if("error"===t.kind){this._submitError=t.message;return}let i=this._missingRequiredPrereqs(t.entry);if(i&&i.unresolved.length>0){this._submitError=this._localize("device.prereq_unresolved",{name:t.entry.name,ids:i.unresolved.join(", ")});return}if(i&&i.missing.length>0)return void await this._startFeaturedSequence([...i.missing,t.entry.id],i.boardId,this._localize("device.adding_prerequisites_for",{name:t.entry.name}));this._selected=t.entry,this._submitError="";let o=this._fastPathFields(t.entry);o&&await this._submitComponent(o,!0)}_missingRequiredPrereqs(e){let t=this.board;if(!t||!(0,eN.sO)(e.id))return null;let i=t.featured_components??[],o=i.find(i=>(0,eN.m0)(t.id,i.id)===e.id);if(!o?.requires?.length)return null;let a=eH(this.yaml),r=[],n=[];for(let s of o.requires){let o=i.find(e=>e.id===s);if(!o){console.warn(`Featured component '${e.id}' requires '${s}', which is not in the board catalog.`),n.push(s);continue}let l=o.fields.id?.value;"string"==typeof l&&a.has(l)||r.push((0,eN.m0)(t.id,s))}return{boardId:t.id,missing:r,unresolved:n}}async _startFeaturedSequence(e,t,i){let[o,...a]=e,r=await e8(this,o,t);return"stale"!==r.kind&&("error"===r.kind?(this._submitError=r.message,!1):(this._clearDetourFields(),this._bundleQueue=a,this._bundleProgress={current:1,total:e.length,bundleName:i},this._selected=r.entry,this._submitError="",!0))}_fastPathFields(e){var t,i,o;let a,r,n;if(null!==this._prefillReference||null!==this._depPrefill)return null;let s=(0,eG.Zn)(this.yaml);if(e1(e.dependencies??[],this.yaml,s).length>0)return null;let l=tY({entries:e.config_entries,component:e,board:this.board,yaml:this.yaml,prefillReference:null,prefillFields:null,restoredValues:null,localize:this._localize});return(t=e.config_entries,i=e.required_groups??[],a=tW(l,this.board,s),r=tH(t,l,i,a),o=e=>(0,to.VP)(e,l,a.presentComponents,a.targetPlatform??null,a.rootValues,t),(n=e=>e.some(e=>!e.locked&&o(e)))([...r.visible])||r.clusters.some(e=>n(e.members))||r.ordered.some(e=>Array.isArray(e)&&n(e))||tG({entries:t,requiredGroups:i,values:l,presentComponents:s,targetPlatform:a.targetPlatform??null,formatKeys:()=>""},r.memberKeys).length>0)?null:ti(e.config_entries,l)}async _onBundleSelected(e){if(e.stopPropagation(),this._submitting)return;let{bundle:t,boardId:i}=e.detail;if(!i||0===t.component_ids.length||!this.configuration)return;let o=t.component_ids.map(e=>(0,eN.m0)(i,e));this._clearDetourFields(),this._submitting=!0,this._submitError="",this._depNavSeq++;let a=this.yaml||void 0,r=null,n=!1,s=async e=>{n&&this._dispatchDraft(this.yaml);let a=await this._startFeaturedSequence(o.slice(e),i,t.name);this._submitting=!1,a&&(r&&(this._prefillReference=r),this._bundleProgress={current:e+1,total:o.length,bundleName:t.name})},l=eH(this.yaml);try{for(let e=0;e<o.length;e++){let t=await e8(this,o[e],i);if("stale"===t.kind){n&&this._dispatchDraft(this.yaml);return}if("error"===t.kind){n&&this._dispatchDraft(this.yaml),this._submitError=t.message;return}let d=t.entry,c=this._fastPathFields(d);if(null===c)return void await s(e);let h=c.id;if("string"==typeof h&&l.has(h)){r=this._chainReference(d,c);continue}let{yaml:p}=await this._api.addComponent(this.configuration,{component_id:o[e],fields:c},a);a=p,n=!0,"string"==typeof h&&l.add(h),this.yaml=p,r=this._chainReference(d,c)}n&&this._dispatchDraft(this.yaml),this._dialog.open=!1,this._selected=null,this._resetDetourState();let e=n?this._localize("device.bundle_added",{name:t.name}):this._localize("device.bundle_already_present",{name:t.name});(0,d.VX)(e)}catch(e){n&&this._dispatchDraft(this.yaml),this._submitError=(0,ev.K)(e,this._localize,"device.add_component_error"),(0,d.UG)(this._submitError)}finally{this._submitting=!1}}_dispatchDraft(e){(0,Z.r)(this,"yaml-draft",{yaml:e})}_chainReference(e,t){let i=t.id;return"string"==typeof i&&e.category?{domain:e.category,id:i}:null}_onBack(){if(!this._submitting){if(this._returnTo){let e=this._returnTo,t=this._returnValues;this._resetDetourState(),this._returnValues=t,this._selected=e,this._submitError="";return}this._resetDetourState(),this._selected=null,this._submitError=""}}_onNavigateToDep(e){return e.stopPropagation(),this._returnValues=this._form?.currentValues??null,e4(this,e.detail.domain)}_onFormSubmit(e){return e.stopPropagation(),this._submitComponent(e.detail.fields)}async _submitComponent(e,t=!1){if(this._selected&&this.configuration&&!this._submitting){this._submitting=!0,this._submitError="",this._depNavSeq++;try{let{yaml:o}=await this._api.addComponent(this.configuration,{component_id:this._selected.id,fields:e},this.yaml||void 0);if(this._dispatchDraft(o),this._returnTo){var i;let t=this._returnTo,o=this._depDomain,a=e.id;o&&"string"==typeof a&&(i=this._selected,i.id===o||i.category===o)?this._prefillReference={domain:o,id:a}:this._prefillReference=null,this._returnTo=null,this._depDomain=null,this._depPrefill=null,this._selected=t}else if(this._bundleQueue.length>0&&this._bundleProgress){let t=this._bundleQueue[0],i=this._bundleQueue.slice(1),o=await e8(this,t);if("stale"===o.kind)return;if("error"===o.kind){this._submitError=o.message;return}let a=o.entry;this._prefillReference=this._chainReference(this._selected,e),this._bundleQueue=i,this._bundleProgress={...this._bundleProgress,current:this._bundleProgress.current+1},this._returnValues=null,this._selected=a}else{let i=this._selected.id,a=this._selected.name,r=e.id,n=(0,L.BB)(o,i,"string"==typeof r?r:void 0);n&&(0,Z.r)(this,"section-select",n),this._dialog.open=!1,this._selected=null,this._resetDetourState(),t&&(0,d.VX)(this._localize("device.component_added",{name:a}))}}catch(e){this._submitError=(0,ev.K)(e,this._localize,"device.add_component_error"),t&&(0,d.UG)(this._submitError)}finally{this._submitting=!1}}}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml="",this.lockedCategories=[],this._dialog=new eu.T(this),this._returnValues=null,this._selected=null,this._submitting=!1,this._submitError="",this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._depPrefill=null,this._bundleQueue=[],this._bundleProgress=null,this._selectionSeq=0,this._depNavSeq=0}}function as(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}an.styles=[b.G,(0,eZ._)("esphome-base-dialog"),eU.c4,e9],ar([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],an.prototype,"_localize",void 0),ar([(0,a.Fg)({context:_.Ie})],an.prototype,"_api",void 0),ar([(0,s.MZ)()],an.prototype,"boardName",void 0),ar([(0,s.MZ)()],an.prototype,"configuration",void 0),ar([(0,s.MZ)()],an.prototype,"platform",void 0),ar([(0,s.MZ)({attribute:!1})],an.prototype,"board",void 0),ar([(0,s.MZ)()],an.prototype,"yaml",void 0),ar([(0,s.MZ)({attribute:!1})],an.prototype,"lockedCategories",void 0),ar([(0,s.P)("esphome-component-catalog")],an.prototype,"_catalog",void 0),ar([(0,s.P)("esphome-add-component-form")],an.prototype,"_form",void 0),ar([(0,s.wk)()],an.prototype,"_returnValues",void 0),ar([(0,s.wk)()],an.prototype,"_selected",void 0),ar([(0,s.wk)()],an.prototype,"_submitting",void 0),ar([(0,s.wk)()],an.prototype,"_submitError",void 0),ar([(0,s.wk)()],an.prototype,"_returnTo",void 0),ar([(0,s.wk)()],an.prototype,"_depDomain",void 0),ar([(0,s.wk)()],an.prototype,"_prefillReference",void 0),ar([(0,s.wk)()],an.prototype,"_depPrefill",void 0),ar([(0,s.wk)()],an.prototype,"_bundleQueue",void 0),ar([(0,s.wk)()],an.prototype,"_bundleProgress",void 0),an=ar([(0,s.EM)("esphome-add-component-dialog")],an);class al extends n.WF{open(){this._inner.open()}render(){return(0,n.qy)`<esphome-add-component-dialog
      .lockedCategories=${eY}
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .platform=${this.platform}
      .board=${this.board}
      .yaml=${this.yaml}
    ></esphome-add-component-dialog>`}constructor(...e){super(...e),this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml=""}}as([(0,s.MZ)()],al.prototype,"boardName",void 0),as([(0,s.MZ)()],al.prototype,"configuration",void 0),as([(0,s.MZ)()],al.prototype,"platform",void 0),as([(0,s.MZ)({attribute:!1})],al.prototype,"board",void 0),as([(0,s.MZ)()],al.prototype,"yaml",void 0),as([(0,s.P)("esphome-add-component-dialog")],al.prototype,"_inner",void 0),al=as([(0,s.EM)("esphome-add-config-dialog")],al);var ad=i(4103),ac=i(664);class ah{hostConnected(){(0,Z.r)(this._host,"section-mount",{node:this._host})}hostDisconnected(){this._clearTimer(),(0,Z.r)(this._host,"section-unmount",{node:this._host})}get dirty(){return this._dirty}get deleting(){return this._deleting}get inFlightWrite(){return this._deleting||this._applyInFlight}shouldSkipReload(){return this._applyInFlight||this._host.yaml===this._lastSelfWrittenYaml}withValue(e){let t={...this._host.value??eq(),...e};this._host.value=t,(0,Z.r)(this._host,"automation-change",{value:t,location:this._host.location}),this.scheduleAutoApply()}scheduleAutoApply(){this._host.addMode||this._options.isReadOnly()||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this.autoApply()},200))}async flushPending(){if(this._applyTimer)this._clearTimer(),await this.autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}async autoApply(){let e=this._options.getApi(),t=this._host.location,i=this._host.value;if(e&&t&&i){if(this._options.isReadOnly())return void this._setDirty(!1);if(!this._options.canApply||this._options.canApply(t)){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:o}=await e.upsertAutomation(this._host.configuration,i,t,this._host.yaml),a=eL(this._host.yaml,o);this._lastSelfWrittenYaml=a,this._host.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0}))}catch(e){this._surfaceSaveError(e)}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this.autoApply()):this._setDirty(!1)}}}}async delete(){let e=this._options.getApi();if(e&&this._host.location&&!this._deleting){this._clearTimer(),this._setDeleting(!0),this._options.setError("");try{let{yaml_diff:t}=await e.deleteAutomation(this._host.configuration,this._host.location,this._host.yaml),i=eL(this._host.yaml,t);await e.updateConfig(this._host.configuration,i),this._host.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:i},bubbles:!0,composed:!0})),this._host.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(e){this._surfaceSaveError(e)}finally{this._setDeleting(!1)}}}_surfaceSaveError(e){let t=this._options.getLocalize(),i=(0,ev.K)(e,t,"device.automation_save_error");this._options.setError(i),(0,d.UG)(t("device.automation_save_error"),{description:i})}_clearTimer(){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null)}_setDirty(e){this._dirty!==e&&(this._dirty=e,this._host.requestUpdate(),(0,Z.r)(this._host,"dirty-change",{dirty:e}))}_setDeleting(e){this._deleting=e,this._host.requestUpdate()}constructor(e,t){this._host=e,this._options=t,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._deleting=!1,e.addController(this)}}var ap=i(2640);let au=(0,n.AH)`
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
`,am=(0,n.AH)`
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
  /* Input and wa-select chrome both come from the shared inputStyles,
     keyed on --wa-form-control-height, so the pair stays equal-height. */
  .ae-delay-row wa-select {
    width: 100%;
  }
`,av=(0,n.AH)`
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
`,ag=[(0,n.AH)`
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
`,av,am,au,ap.Z,tC,U.U],af=new Set(["condition","all","any"]);function a_(e){return{node:e.node.slice(1),field:e.field}}function ab(e){return e&&e.node.length>0?e:null}function ay(e){return e&&0===e.node.length?e.field:void 0}function aw(e,t){let i=ay(e);return i?.[0]===t?i[1]??"":null}function a$(e){return e?JSON.stringify([e.node,e.field]):void 0}function ax(e,t){return a$(e)!==a$(t)}function ak(e,t,i){if(!e||!i?.length)return null;let o=function(e,t){let i=t&&function(e){switch(e.kind){case"device_on":case"component_on":return{keys:[e.trigger],index:e.index};case"component_action":return{keys:[e.field]};case"interval":return{keys:["interval"],index:e.index};case"script":return{keys:["script"],index:"any"};case"api_action":return{keys:["api","actions"],index:"any"};default:return null}}(t);if(!i)return null;let o=e.indexOf(i.keys[0]);for(;o>=0&&!i.keys.every((t,i)=>e[o+i]===t);)o=e.indexOf(i.keys[0],o+1);if(o<0)return null;let a=e.slice(o+i.keys.length);return void 0===i.index?a:"any"===i.index?"number"==typeof a[0]?a.slice(1):null:a[0]===i.index?a.slice(1):null}(i,t);return o?function(e,t){if(0===t.length)return null;let i=t=>aS(e.actions,aC,aA,t,[],null),o=t[0];return"then"===o?i(t.slice(1)):"number"==typeof o?i(t):i(t)??{node:[],field:t.map(String)}}(e,o):null}function az(){return(0,l.A)(ak)}let aC=e=>e.action_id,aq=e=>e.condition_id;function aS(e,t,i,o,a,r){if(0===o.length)return r;let n=o[0];if("number"==typeof n){let s=o[1];if("string"==typeof s){let r=void 0!==e[n]&&t(e[n])===s?n:e.findIndex(e=>t(e)===s);if(r>=0)return i(e[r],o.slice(2),[...a,r])}return void 0!==e[n]?{node:[...a,n],field:[]}:r}let s=e.findIndex(e=>t(e)===n);return s>=0?i(e[s],o.slice(1),[...a,s]):r}function aA(e,t,i){let o={node:i,field:[]};if(0===t.length)return o;let a=t[0];if("string"==typeof a){if(af.has(a))return aS(e.conditions??[],aq,aM,t.slice(1),[...i,"conditions"],o);if(e.children&&Object.prototype.hasOwnProperty.call(e.children,a))return aS(e.children[a],aC,aA,t.slice(1),[...i,a],o);if(e.conditions?.some(e=>e.condition_id===a))return aS(e.conditions,aq,aM,t,[...i,"conditions"],o)}return{node:i,field:t.map(String)}}function aM(e,t,i){let o={node:i,field:[]};if(0===t.length)return o;let a=e.children??[],r=t[0];return a.length>0&&("number"==typeof r||a.some(e=>e.condition_id===r))?aS(a,aq,aM,t,i,o):{node:i,field:t.map(String)}}function aP(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({close:r.mdiClose,magnify:r.mdiMagnify,plus:r.mdiPlus});class aE extends n.WF{open(){this._activeTab="action"===this.kind?"by-target":"by-type",this._query="",this._dialog.open=!0}render(){let e="action"===this.kind?this._localize("device.automation_pick_action"):this._localize("device.automation_pick_condition"),t=this._localize("device.automation_pick_search"),i="action"===this.kind?["by-target","by-type","building-blocks"]:["by-type","building-blocks"];return(0,n.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      .label=${e}
      @request-close=${this._dialog.onRequestClose}
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
        ${i.map(e=>(0,n.qy)`<button
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
    </esphome-base-dialog>`}_tabLabel(e){switch(e){case"by-target":return this._localize("device.automation_pick_tab_by_target");case"by-type":return this._localize("device.automation_pick_tab_by_type");case"building-blocks":return this._localize("device.automation_pick_tab_building_blocks")}}_renderActiveTab(){let e=this._applyQuery(this.items);switch(this._activeTab){case"by-target":return this._renderByTarget(e);case"by-type":return this._renderByType(e);case"building-blocks":return this._renderBuildingBlocks(e)}}_applyQuery(e){let t=this._query.trim().toLowerCase();return t?e.filter(e=>e.id.toLowerCase().includes(t)||e.name.toLowerCase().includes(t)||(e.description??"").toLowerCase().includes(t)):e}_renderByTarget(e){if(0===this.devices.length)return(0,n.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_targets")}
      </p>`;let t=this.devices.filter(e$).map(t=>{let i=ey(t.component_id),o=e.filter(e=>"domain"in e&&(e.domain===i||e.domain===t.component_id));return{device:t,matching:o}}).filter(e=>e.matching.length>0);return 0===t.length?(0,n.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,n.qy)`${t.map(({device:e,matching:t})=>(0,n.qy)`
        <p class="picker-group-label">
          ${eb(e)}
          <span class="ae-muted">(${ew(e,this.devices)})</span>
        </p>
        ${t.map(t=>this._renderRow(t,()=>this._pick(t.id,function(e,t){if(!t.has_explicit_id)return;let i=ey(t.component_id),o=e.config_entries.find(e=>e.references_component===i);if(o)return{[o.key]:t.id}}(t,e))))}
      `)}`}_renderByType(e){let t=new Map;for(let i of e){if(!("domain"in i)||"core"===i.domain)continue;let e=ey(i.domain),o=t.get(e)??[];o.push(i),t.set(e,o)}let i=Array.from(t.keys()).sort();return 0===i.length?(0,n.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,n.qy)`${i.map(e=>(0,n.qy)`
        <p class="picker-group-label">${e}</p>
        ${(t.get(e)??[]).map(e=>this._renderRow(e,()=>this._pick(e.id)))}
      `)}`}_renderBuildingBlocks(e){let t=e.filter(e=>"domain"in e&&"core"===e.domain);return 0===t.length?(0,n.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,n.qy)`${t.map(e=>this._renderRow(e,()=>this._pick(e.id)))}`}_renderRow(e,t){return(0,n.qy)`<div
      class="picker-row"
      role="button"
      tabindex="0"
      @click=${t}
      @keydown=${e=>{("Enter"===e.key||" "===e.key)&&(e.preventDefault(),t())}}
    >
      <div class="picker-row-body">
        <span class="picker-row-title">${e.name}</span>
        ${e.description?(0,n.qy)`<span class="picker-row-desc line-clamp-2">
                ${(0,en.Gc)(e.description)}
              </span>`:n.s6}
      </div>
      <span class="picker-row-add" aria-hidden="true">
        <wa-icon library="mdi" name="plus"></wa-icon>
      </span>
    </div>`}_pick(e,t){this.dispatchEvent(new CustomEvent("catalog-picked",{detail:{id:e,preFilledParams:t},bubbles:!0,composed:!0})),this._dialog.open=!1}constructor(...e){super(...e),this._localize=e=>e,this.kind="action",this.items=[],this.devices=[],this._dialog=new eu.T(this),this._activeTab="by-target",this._query=""}}function aF(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aE.styles=[b.G,ep.z9,U.U,(0,n.AH)`
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
    `],aP([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aE.prototype,"_localize",void 0),aP([(0,s.MZ)()],aE.prototype,"kind",void 0),aP([(0,s.MZ)({attribute:!1})],aE.prototype,"items",void 0),aP([(0,s.MZ)({attribute:!1})],aE.prototype,"devices",void 0),aP([(0,s.wk)()],aE.prototype,"_activeTab",void 0),aP([(0,s.wk)()],aE.prototype,"_query",void 0),aE=aP([(0,s.EM)("esphome-catalog-picker-dialog")],aE),(0,M.C)({"arrow-down":r.mdiArrowDown,"arrow-up":r.mdiArrowUp,close:r.mdiClose,delete:r.mdiDelete,"pencil-outline":r.mdiPencilOutline,plus:r.mdiPlus});let aL=[];class aO extends n.WF{willUpdate(e){e.has("focusTarget")&&(this._focusScrolled=!1)}updated(){this._maybeScrollRow()}render(){return(0,n.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?n.s6:(0,n.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_only_when")}</label
              >`}
        ${0===this.conditions.length?(0,n.qy)`<p class="ae-empty">${this._localize("device.add_condition")}</p>`:this.conditions.map((e,t)=>this._renderNode(e,t))}
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
    `}_renderNode(e,t){let i=this.catalog.find(t=>t.id===e.condition_id),o=this.conditions.length-1,a=this.focusTarget?.node[0]===t?this.focusTarget:null,r=a&&a.node.length>1?a_(a):null,s=a&&1===a.node.length&&a.field.length>0?a.field:void 0;return(0,n.qy)`
      <div class="ae-row">
        <div class="ae-row-header">
          <button
            type="button"
            class="ae-row-picker"
            ?disabled=${this.disabled}
            @click=${()=>this._openPickerForChange(t)}
          >
            <span class="ae-row-picker-name truncate">
              ${i?.name??e.condition_id}
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
              ?disabled=${this.disabled||t===o}
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
          ${i?.description?(0,n.qy)`<p class="ae-row-desc">${(0,en.Gc)(i.description)}</p>`:n.s6}
          ${i&&i.config_entries.length>0?(0,n.qy)`<esphome-config-entry-form
                  .entries=${i.config_entries}
                  .values=${e.params}
                  .requiredGroups=${i.required_groups??aL}
                  .board=${this.board}
                  .yaml=${this.yaml}
                  .focusFieldPath=${s}
                  ?disabled=${this.disabled}
                  advanced-section
                  ?show-advanced=${this._advancedIdxs.has(t)}
                  @value-change=${e=>this._onParamChange(t,e)}
                  @advanced-toggle=${e=>this._onAdvancedToggle(t,e)}
                ></esphome-config-entry-form>`:n.s6}
          ${i?.accepts_condition_list?(0,n.qy)`<div class="ae-nested">
                  <p class="ae-nested-label">
                    ${this._localize("device.automation_condition")}
                  </p>
                  <esphome-automation-condition-tree
                    no-header
                    .conditions=${e.children??[]}
                    .focusTarget=${r}
                    .catalog=${this.catalog}
                    .devices=${this.devices}
                    .board=${this.board}
                    .yaml=${this.yaml}
                    ?disabled=${this.disabled}
                    @conditions-change=${e=>this._onChildrenChange(t,e)}
                  ></esphome-automation-condition-tree>
                </div>`:n.s6}
        </div>
      </div>
    `}_openPickerForChange(e){0!==this.catalog.length&&(this._changingIdx=e,this._picker.open())}_onParamChange(e,t){t.stopPropagation();let i=this.conditions[e],o=eS(i.params,t.detail.path,t.detail.value);this._emit(eA(this.conditions,e,{...i,params:o}))}_onAdvancedToggle(e,t){t.stopPropagation(),this._setRowAdvanced(e,t.detail.show)}_setRowAdvanced(e,t){let i=new Set(this._advancedIdxs);t?i.add(e):i.delete(e),this._advancedIdxs=i}_onChildrenChange(e,t){t.stopPropagation();let i=this.conditions[e];this._emit(eA(this.conditions,e,{...i,children:t.detail.conditions}))}_move(e,t){let i=new Set(this._advancedIdxs);this._advancedIdxs.has(e)?i.add(t):i.delete(t),this._advancedIdxs.has(t)?i.add(e):i.delete(e),this._advancedIdxs=i,this._emit(eP(this.conditions,e,t))}_remove(e){this._advancedIdxs=new Set([...this._advancedIdxs].filter(t=>t!==e).map(t=>t>e?t-1:t)),this._emit(eM(this.conditions,e))}_maybeScrollRow(){let e=this.focusTarget;if(!e||this._focusScrolled)return;this._focusScrolled=!0;let t=e.node[0];if("number"!=typeof t)return;let i=this.catalog.find(e=>e.id===this.conditions[t]?.condition_id);if(!(e.node.length>1?!i?.accepts_condition_list:0===e.field.length||!i||0===i.config_entries.length))return;let o=this.shadowRoot?.querySelectorAll(".ae-row")[t];o&&id(o)}_emit(e){(0,Z.r)(this,"conditions-change",{conditions:e})}constructor(...e){super(...e),this._localize=e=>e,this.conditions=[],this.catalog=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.devices=[],this.focusTarget=null,this._changingIdx=-1,this._advancedIdxs=new Set,this._focusScrolled=!1,this._openPickerForAdd=()=>{0!==this.catalog.length&&(this._changingIdx=-1,this._picker.open())},this._onConditionPicked=e=>{e.stopPropagation();let t={condition_id:e.detail.id,params:{},children:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._changingIdx>=0?(this._setRowAdvanced(this._changingIdx,!1),this._emit(eA(this.conditions,this._changingIdx,t))):this._emit([...this.conditions,t]),this._changingIdx=-1}}}aO.styles=[b.G,ep.z9,ag,tz],aF([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aO.prototype,"_localize",void 0),aF([(0,s.MZ)({attribute:!1})],aO.prototype,"conditions",void 0),aF([(0,s.MZ)({attribute:!1})],aO.prototype,"catalog",void 0),aF([(0,s.MZ)({attribute:!1})],aO.prototype,"board",void 0),aF([(0,s.MZ)()],aO.prototype,"yaml",void 0),aF([(0,s.MZ)({type:Boolean})],aO.prototype,"disabled",void 0),aF([(0,s.MZ)({type:Boolean,attribute:"no-header"})],aO.prototype,"noHeader",void 0),aF([(0,s.MZ)({attribute:!1})],aO.prototype,"devices",void 0),aF([(0,s.MZ)({attribute:!1,hasChanged:ax})],aO.prototype,"focusTarget",void 0),aF([(0,s.P)("esphome-catalog-picker-dialog")],aO.prototype,"_picker",void 0),aF([(0,s.wk)()],aO.prototype,"_changingIdx",void 0),aF([(0,s.wk)()],aO.prototype,"_advancedIdxs",void 0),aO=aF([(0,s.EM)("esphome-automation-condition-tree")],aO);let aR={us:"microseconds",ms:"milliseconds",s:"seconds",min:"minutes",h:"hours",d:"days"};function aT(e){let t=e.id;return(0,iW.b)(t)?t:null}function aD(e){for(let t of iL){let i=e[aR[t]];if(void 0!==i&&""!==i&&null!==i)return{value:String(i),unit:t}}let t=e.id;if("string"==typeof t&&iI(t)){let e=iB(t);return{value:e.value,unit:e.unit}}return{value:"",unit:"s"}}function aI(e){let t={...e};for(let e of iL)delete t[aR[e]];return delete t.id,t}function aB(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({"arrow-down":r.mdiArrowDown,"arrow-up":r.mdiArrowUp,"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,close:r.mdiClose,delete:r.mdiDelete,"pencil-outline":r.mdiPencilOutline});let aj=[];function aK(e){return e?.id==="if"||e?.id==="wait_until"}function aU(e){return!!e&&"delay"!==e.id&&e.config_entries.length>0}class aZ extends n.WF{willUpdate(e){if(e.has("value")){let t=e.get("value");t&&t.action_id!==this.value.action_id&&(this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null)}e.has("focusTarget")&&(this._focusScrolled=!1,this.focusTarget&&(this._collapsed=!1))}updated(){this._maybeScrollSelf()}_maybeScrollSelf(){let e=this.focusTarget;if(!e||this._focusScrolled||(this._focusScrolled=!0,!this._isTerminalFocus(e)))return;let t=this.shadowRoot?.querySelector(".ae-row");t&&id(t)}_isTerminalFocus(e){let t=this.catalog.find(e=>e.id===this.value.action_id),i=e.node[0];return"conditions"===i?!aK(t):"string"==typeof i?!(t?.accepts_action_list??[]).includes(i):0===e.field.length||!aU(t)}render(){let e=this.catalog.find(e=>e.id===this.value.action_id),t=this._collapsed;return(0,n.qy)`
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
        <esphome-catalog-picker-dialog
          kind="action"
          .items=${this.catalog}
          .devices=${this.devices}
          @catalog-picked=${this._onActionPicked}
        ></esphome-catalog-picker-dialog>
        ${t?n.s6:(0,n.qy)`<div class="ae-row-body">
                ${e?.description?(0,n.qy)`<p class="ae-row-desc">${(0,en.Gc)(e.description)}</p>`:n.s6}
                ${this._renderActionParams(e)} ${this._renderScriptParams(e)}
                ${this._renderConditionGate(e)} ${this._renderNestedLists(e)}
              </div>`}
      </div>
    `}_renderScriptParams(e){if(e?.id!=="script.execute")return n.s6;let t=String(this.value.params.id??""),i=this.scripts.find(e=>e.id===t);return i&&0!==i.parameters.length?(0,n.qy)`<div class="ae-nested">
      <p class="ae-nested-label">
        ${this._localize("device.automation_script_parameters")}
      </p>
      ${i.parameters.map(e=>(0,n.qy)`<label class="ae-section-label" for="script-${e.name}"
              >${e.name} <span class="ae-muted">${e.type}</span></label
            >
            <input
              id="script-${e.name}"
              type=${"int"===e.type||"float"===e.type?"number":"text"}
              ?disabled=${this.disabled}
              .value=${String(this.value.params[e.name]??"")}
              @input=${t=>{var i;let o=t.target.value;this._patchParams({[e.name]:(i=e.type,"int"===i?(0,e7.s)(o):"float"===i?tt(o):o)})}}
            />`)}
    </div>`:n.s6}_renderConditionGate(e){return aK(e)?(0,n.qy)`<div class="ae-nested">
      <p class="ae-nested-label">${this._localize("device.automation_only_when")}</p>
      <esphome-automation-condition-tree
        no-header
        .conditions=${this.value.conditions??[]}
        .focusTarget=${this.focusTarget?.node[0]==="conditions"?a_(this.focusTarget):null}
        .catalog=${this.conditionCatalog}
        .devices=${this.devices}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${this.disabled}
        @conditions-change=${this._onConditionsChange}
      ></esphome-automation-condition-tree>
    </div>`:n.s6}_nestedListLabel(e){return"else"===e?this._localize("device.automation_else"):"then"===e?this._localize("device.automation_action"):e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}_renderNestedLists(e){return e&&e.accepts_action_list&&0!==e.accepts_action_list.length?e.accepts_action_list.map(e=>(0,n.qy)`<div class="ae-nested">
          <p class="ae-nested-label">${this._nestedListLabel(e)}</p>
          <esphome-automation-action-list
            no-header
            .actions=${this.value.children?.[e]??[]}
            .focusTarget=${this.focusTarget?.node[0]===e?a_(this.focusTarget):null}
            .catalog=${this.catalog}
            .conditionCatalog=${this.conditionCatalog}
            .scripts=${this.scripts}
            .devices=${this.devices}
            .board=${this.board}
            .yaml=${this.yaml}
            ?disabled=${this.disabled}
            @actions-change=${t=>{t.stopPropagation(),this._onChildrenChange(e,t.detail.actions)}}
          ></esphome-automation-action-list>
        </div>`):n.s6}_renderActionParams(e){if(e?.id==="delay")return this._renderDelayParams();if(!aU(e))return n.s6;let t=this.focusTarget;return(0,n.qy)`<esphome-config-entry-form
      .entries=${e.config_entries}
      .values=${this.value.params}
      .requiredGroups=${e.required_groups??aj}
      .board=${this.board}
      .yaml=${this.yaml}
      .focusFieldPath=${t&&0===t.node.length&&t.field.length>0?t.field:void 0}
      ?disabled=${this.disabled}
      advanced-section
      ?show-advanced=${this._showAdvanced}
      @value-change=${this._onParamChange}
      @advanced-toggle=${this._onAdvancedToggle}
    ></esphome-config-entry-form>`}_renderDelayParams(){var e,t,i;let o;return o=aT((e={params:this.value.params??{},disabled:this.disabled,localize:this._localize,onWrite:(e,t)=>this._writeDelay(e,t),onWriteLambda:e=>this._writeDelayLambda(e),onToggle:e=>this._toggleDelayLambda(e)}).params),(0,n.qy)`<div class="ae-delay">
    ${tk({isLambda:null!==o,disabled:e.disabled,localize:e.localize,onSwitch:t=>e.onToggle(t)})}
    ${o?(t=o,i=e,(0,n.qy)`<esphome-lambda-editor
    .value=${oC(t)}
    ?disabled=${i.disabled}
    @lambda-change=${e=>i.onWriteLambda(e.detail.value)}
  ></esphome-lambda-editor>`):function(e){let{value:t,unit:i}=aD(e.params);return(0,n.qy)`<div class="ae-delay-row">
    <div class="ae-delay-value">
      <label class="field-label" for="ae-delay-value-input">
        ${e.localize("device.automation_action_delay_value")}
      </label>
      <input
        id="ae-delay-value-input"
        type="text"
        inputmode="decimal"
        .value=${t}
        placeholder="0"
        ?disabled=${e.disabled}
        @input=${t=>e.onWrite(t.target.value,i)}
      />
    </div>
    <div class="ae-delay-unit">
      <label class="field-label" id="ae-delay-unit-label">
        ${e.localize("device.automation_action_delay_unit")}
      </label>
      <wa-select
        id="ae-delay-unit-select"
        aria-labelledby="ae-delay-unit-label"
        value=${i}
        ?disabled=${e.disabled}
        @change=${i=>e.onWrite(t,i.target.value)}
      >
        ${iL.map(t=>(0,n.qy)`<wa-option value=${t} ?selected=${t===i}>
              ${e.localize(`device.automation_action_delay_unit_${t}`)}
            </wa-option>`)}
      </wa-select>
    </div>
  </div>`}(e)}
  </div>`}_toggleDelayLambda(e){let t=this.value.params??{},i=aT(t);if(e!==(null!==i))if(e)this._delayLiteralStash=aD(t),this._writeDelayLambda(this._delayLambdaStash);else{this._delayLambdaStash=oC(i);let{value:e,unit:t}=this._delayLiteralStash??{value:"",unit:"s"};this._writeDelay(e,t)}}_writeDelay(e,t){var i;let o,a;this._emit({...this.value,params:(i=this.value.params??{},o=e.trim(),a=aI(i),o&&(a[aR[t]]=o),a)})}_writeDelayLambda(e){var t;let i;this._delayLambdaStash=e,this._emit({...this.value,params:(t=this.value.params??{},(i=aI(t)).id={_lambda:e,_tag:"!lambda"},i)})}_patchParams(e){this._emit({...this.value,params:{...this.value.params,...e}})}_onChildrenChange(e,t){let i={...this.value.children??{},[e]:t};this._emit({...this.value,children:i})}_reorder(e){(0,Z.r)(this,"action-reorder",{delta:e})}_emit(e){(0,Z.r)(this,"action-change",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.first=!1,this.last=!1,this.focusTarget=null,this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null,this._focusScrolled=!1,this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._openPicker=()=>{this._picker.open()},this._onActionPicked=e=>{e.stopPropagation(),this._emit({action_id:e.detail.id,params:{...e.detail.preFilledParams??{}},children:{},conditions:[]})},this._onParamChange=e=>{e.stopPropagation();let t=eS(this.value.params,e.detail.path,e.detail.value);this._emit({...this.value,params:t})},this._onConditionsChange=e=>{e.stopPropagation(),this._emit({...this.value,conditions:e.detail.conditions})},this._onDelete=()=>{(0,Z.r)(this,"action-delete")}}}function aN(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aZ.styles=[b.G,ep.z9,ag,tx,tz],aB([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aZ.prototype,"_localize",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"value",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"catalog",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"conditionCatalog",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"scripts",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"devices",void 0),aB([(0,s.MZ)({attribute:!1})],aZ.prototype,"board",void 0),aB([(0,s.MZ)()],aZ.prototype,"yaml",void 0),aB([(0,s.MZ)({type:Boolean})],aZ.prototype,"disabled",void 0),aB([(0,s.MZ)({type:Boolean})],aZ.prototype,"first",void 0),aB([(0,s.MZ)({type:Boolean})],aZ.prototype,"last",void 0),aB([(0,s.MZ)({attribute:!1,hasChanged:ax})],aZ.prototype,"focusTarget",void 0),aB([(0,s.P)("esphome-catalog-picker-dialog")],aZ.prototype,"_picker",void 0),aB([(0,s.wk)()],aZ.prototype,"_collapsed",void 0),aB([(0,s.wk)()],aZ.prototype,"_showAdvanced",void 0),aB([(0,s.wk)()],aZ.prototype,"_delayLambdaStash",void 0),aB([(0,s.wk)()],aZ.prototype,"_delayLiteralStash",void 0),aZ=aB([(0,s.EM)("esphome-automation-action-node")],aZ),(0,M.C)({plus:r.mdiPlus});class aV extends n.WF{render(){return(0,n.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?n.s6:(0,n.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_action")}</label
              >`}
        ${0===this.actions.length?(0,n.qy)`<p class="empty-message--dashed" role="status">
                ${this._localize("device.automation_actions_empty")}
              </p>`:this.actions.map((e,t)=>this._renderRow(e,t,t===this.actions.length-1))}
        ${this.hideAdd?n.s6:(0,n.qy)`<button
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
    `}_renderRow(e,t,i){return(0,n.qy)`<esphome-automation-action-node
      .value=${e}
      .focusTarget=${this.focusTarget?.node[0]===t?a_(this.focusTarget):null}
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
    ></esphome-automation-action-node>`}_onActionChange(e,t){t.stopPropagation(),this._emit(eA(this.actions,e,t.detail.value))}_onReorder(e,t){t.stopPropagation(),this._emit(eP(this.actions,e,e+t.detail.delta))}_onDelete(e,t){t.stopPropagation(),this._emit(eM(this.actions,e))}_emit(e){(0,Z.r)(this,"actions-change",{actions:e})}constructor(...e){super(...e),this._localize=e=>e,this.actions=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.hideAdd=!1,this.focusTarget=null,this.openPicker=()=>{0!==this.catalog.length&&this._picker.open()},this._onActionPicked=e=>{e.stopPropagation();let t={action_id:e.detail.id,params:{},children:{},conditions:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._emit([...this.actions,t])}}}function aH(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}aV.styles=[b.G,ep.z9,ag],aN([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aV.prototype,"_localize",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"actions",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"catalog",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"conditionCatalog",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"scripts",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"devices",void 0),aN([(0,s.MZ)({attribute:!1})],aV.prototype,"board",void 0),aN([(0,s.MZ)()],aV.prototype,"yaml",void 0),aN([(0,s.MZ)({type:Boolean})],aV.prototype,"disabled",void 0),aN([(0,s.MZ)({type:Boolean,attribute:"no-header"})],aV.prototype,"noHeader",void 0),aN([(0,s.MZ)({type:Boolean,attribute:"hide-add"})],aV.prototype,"hideAdd",void 0),aN([(0,s.MZ)({attribute:!1,hasChanged:ax})],aV.prototype,"focusTarget",void 0),aN([(0,s.P)("esphome-catalog-picker-dialog")],aV.prototype,"_picker",void 0),aV=aN([(0,s.EM)("esphome-automation-action-list")],aV),(0,M.C)({close:r.mdiClose,plus:r.mdiPlus});let aG=["int","float","bool","string"];class aW extends n.WF{willUpdate(e){e.has("focusParam")&&(this._focusScrolled=!1)}updated(e){if(e.has("value")){let e=this._readFromWire(),t=this._params.filter(e=>e.name);t.length===e.length&&t.every((t,i)=>t.name===e[i].name&&t.type===e[i].type)||(this._params=e)}this._maybeScrollToParam()}render(){return(0,n.qy)`<div class="field">
      ${this.fieldLabel?(0,n.qy)`<label class="field-label">${this.fieldLabel}</label>`:n.s6}
      ${this.description?(0,n.qy)`<p class="field-description">${(0,en.Gc)(this.description)}</p>`:n.s6}
      ${0===this._params.length?n.s6:(0,n.qy)`<div class="script-params-list">
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
    </div>`}_renderRow(e,t){return(0,n.qy)`<div class="script-param-row">
      <input
        type="text"
        ?disabled=${this.disabled}
        placeholder=${this.namePlaceholder}
        .value=${e.name}
        @input=${i=>this._updateRow(t,{...e,name:(0,ac.e)(i.target.value)})}
      />
      <wa-select
        value=${e.type}
        ?disabled=${this.disabled}
        @change=${i=>this._updateRow(t,{...e,type:i.target.value})}
      >
        ${aG.map(t=>(0,n.qy)`<wa-option value=${t} ?selected=${t===e.type}>${t}</wa-option>`)}
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
    </div>`}_maybeScrollToParam(){if(null===this.focusParam||this._focusScrolled)return;if(""===this.focusParam){this._focusScrolled=!0;let e=this.shadowRoot?.querySelector(".field");e&&id(e);return}let e=this._params.findIndex(e=>e.name===this.focusParam);if(e<0)return;let t=this.shadowRoot?.querySelectorAll(".script-param-row")[e];t&&(this._focusScrolled=!0,id(t))}_readFromWire(){return this.value&&"object"==typeof this.value?Object.entries(this.value).map(([e,t])=>({name:e,type:String(t??"string")})):[]}_emit(e){this._params=e;let t={};for(let{name:i,type:o}of e)i&&(t[i]=o);this.dispatchEvent(new CustomEvent("value-change",{detail:{value:t},bubbles:!0,composed:!0}))}_updateRow(e,t){let i=this._params.slice();i[e]=t,this._emit(i)}_removeRow(e){let t=this._params.slice();t.splice(e,1),this._emit(t)}constructor(...e){super(...e),this._localize=e=>e,this.value={},this.disabled=!1,this.fieldLabel="",this.description="",this.addLabel="",this.namePlaceholder="",this.focusParam=null,this._params=[],this._focusScrolled=!1,this._addRow=()=>{this._emit([...this._params,{name:"",type:"int"}])}}}aW.styles=[b.G,ep.z9,ag,tz],aH([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],aW.prototype,"_localize",void 0),aH([(0,s.MZ)({attribute:!1})],aW.prototype,"value",void 0),aH([(0,s.MZ)({type:Boolean})],aW.prototype,"disabled",void 0),aH([(0,s.MZ)()],aW.prototype,"fieldLabel",void 0),aH([(0,s.MZ)()],aW.prototype,"description",void 0),aH([(0,s.MZ)()],aW.prototype,"addLabel",void 0),aH([(0,s.MZ)()],aW.prototype,"namePlaceholder",void 0),aH([(0,s.MZ)()],aW.prototype,"focusParam",void 0),aH([(0,s.wk)()],aW.prototype,"_params",void 0),aW=aH([(0,s.EM)("esphome-callable-params-editor")],aW);let aY=["triggers","actions","conditions"];async function aJ(e,t,i,o=aY){let a=i3(),r=[],n=(t,o)=>{for(let n of o)r.push(i6(e,t,n,i).then(e=>{i5(a,e)}))};for(let e of(o.includes("triggers")&&n("triggers",t.triggers),o.includes("actions")&&n("actions",t.actions),o.includes("conditions")&&n("conditions",t.conditions),await Promise.allSettled(r)))"rejected"===e.status&&(a.rejected++,console.warn("automation-editor: body fetch failed",e.reason));return a}async function aQ(e,t,i){try{let o=await e.getAvailableAutomations(t,i?.yaml);if(i?.isStale?.())return{status:"stale"};let a={...o,triggers:o.triggers.map(e=>({...e})),actions:o.actions.map(e=>({...e})),conditions:o.conditions.map(e=>({...e}))};i?.onPaint?.(a);let r=await aJ(e,a,void 0,i?.lists);if(i?.isStale?.())return{status:"stale"};let n={...a,triggers:[...a.triggers],actions:[...a.actions],conditions:[...a.conditions]};return{status:"ok",available:n,hydration:r}}catch(e){if(i?.isStale?.())return{status:"stale"};return{status:"error",error:e}}}class aX{hostDisconnected(){this._seq++}async load(e,t,i,o){if(!e||!t)return{};let a=++this._seq,r=o?.onPaint,n=await aQ(e,t,{isStale:()=>a!==this._seq,yaml:o?.yaml,lists:o?.lists??["actions","conditions"],onPaint:r?e=>{a===this._seq&&r(e)}:void 0});return a!==this._seq?{}:function(e,t){if("stale"===e.status)return{};if("error"===e.status)return{error:(0,em.u)(e.error)};let{missingBody:i,missingField:o,rejected:a}=e.hydration,r=i+o+a;return r>0&&(0,d.UG)(t("device.automation_partial_hydration",{count:r})),{available:e.available}}(n,i)}constructor(e){this._seq=0,e.addController(this)}}class a0{hostConnected(){}get active(){return this._active}resolve(e,t,i){let o=eF(t),a=e.find(e=>eF(e.location)===o);return!a||i&&a.location.kind!==i?(this._set(null),null):(this._set(a.error??null,a.unsupported??!1),null!=a.error)?null:{tree:a.automation,location:a.location}}renderPanel(e){return this._unsupported?(0,n.qy)`<div class="empty-message--dashed" role="note">
        <p>${e("device.yaml_only_section")}</p>
      </div>`:(0,n.qy)`<div class="empty-message--dashed" role="alert">
      <p class="ae-error">${e("device.automation_parse_error")}</p>
      ${this._message?(0,n.qy)`<p>${this._message}</p>`:n.s6}
    </div>`}_set(e,t=!1){let i=null!=e;(this._active!==i||this._message!==(e??"")||this._unsupported!==t)&&(this._active=i,this._message=e??"",this._unsupported=t,this._host.requestUpdate())}constructor(e){this._host=e,this._active=!1,this._message="",this._unsupported=!1,e.addController(this)}}function a1(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({delete:r.mdiDelete,"open-in-new":r.mdiOpenInNew,webhook:r.mdiWebhook});let a2=`${ad.Ik}/components/api.html`;class a6 extends n.WF{get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._load()}updated(e){if(this._maybeFlashName(),e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.action_name!==this.location.action_name&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}flushPending(){return this._engine.flushPending()}render(){if(this._loading)return(0,n.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??eq(),t=this._available?.devices??[],i=this._available?.scripts??[],o=this._available?.actions??[],a=this._available?.conditions??[],r=this._engine.deleting,s=this._resolveFocus(this.value,this.location,this.focusYamlPath);return(0,n.qy)`
      ${this._renderHeader()} ${this._renderActionNameField(r)}
      <esphome-callable-params-editor
        .value=${e.trigger_params.variables??{}}
        .focusParam=${aw(s,"variables")}
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
          ${(0,en.Gc)(this._localize("device.api_action_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          .focusTarget=${ab(s)}
          .actions=${e.actions}
          .catalog=${o}
          .conditionCatalog=${a}
          .scripts=${i}
          .devices=${t}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${r}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,n.qy)`<p class="ae-error" role="alert">${this._error}</p>`:n.s6}
      ${this.location&&this.value&&!this.addMode?(0,n.qy)`<div class="ae-actions">
              <button
                type="button"
                class="ae-danger"
                ?disabled=${r}
                @click=${this._onDelete}
              >
                <wa-icon library="mdi" name="delete"></wa-icon>
                ${this._localize("dashboard.delete")}
              </button>
            </div>`:n.s6}
    `}_renderHeader(){return(0,n.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">
          ${this._localize("device.api_action_header_title_static")}
        </h2>
        <a class="ae-header-docs" href=${a2} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">
          ${(0,en.Gc)(this._localize("device.api_action_header_description"))}
        </p>
      </div>
      <div class="ae-header-icon">
        <wa-icon library="mdi" name="webhook"></wa-icon>
      </div>
    </div>`}_renderActionNameField(e){let t=this.location?.action_name??"";return(0,n.qy)`<div class="field">
      <label class="field-label" for="api-action-name">
        ${this._localize("device.api_action_id_label")}
      </label>
      <p class="field-description">
        ${(0,en.Gc)(this._localize("device.api_action_id_description"))}
      </p>
      <input
        id="api-action-name"
        type="text"
        .value=${t}
        ?disabled=${e}
        ?readonly=${!this.addMode}
        @input=${e=>this._onActionNameChange(e.target.value)}
      />
    </div>`}_maybeFlashName(){let e=this._resolveFocus(this.value,this.location,this.focusYamlPath),t=ay(e)?.[0];if("action"!==t&&"service"!==t)return;let i=a$(e);if(i===this._nameFlashKey)return;let o=this.shadowRoot?.querySelector("#api-action-name")?.closest(".field");o&&(this._nameFlashKey=i,id(o))}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable()}catch(e){this._error=(0,em.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"api_action");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,ev.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}_onActionNameChange(e){let t=(0,ac.e)(e);t&&(this.location={kind:"api_action",action_name:t},this._engine.scheduleAutoApply())}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._resolveFocus=az(),this._available=null,this._loading=!0,this._error="",this._parseError=new a0(this),this._engine=new ah(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,canApply:e=>"api_action"===e.kind&&!!e.action_name,setError:e=>{this._error=e}}),this._catalogLoad=new aX(this),this._onVariablesChange=e=>{e.stopPropagation();let t=this.value??eq();this._engine.withValue({trigger_params:{...t.trigger_params,variables:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}async function a3(e,t,i){let o=(0,e5.CQ)("interval",t,i);if(o)return o;try{return await (0,e5.Sn)(e,"interval",t,i)??null}catch{return null}}function a5(e,t){let i=((e.endsWith("_action")?e.slice(0,-7):e)||e).replace(/_/g," ").trim()||"action";return t("device.action_field_label",{name:i[0].toUpperCase()+i.slice(1)})}function a4(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}a6.styles=[b.G,ep.z9,ag,tz],a1([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],a6.prototype,"_localize",void 0),a1([(0,a.Fg)({context:_.Ie})],a6.prototype,"_api",void 0),a1([(0,s.MZ)()],a6.prototype,"configuration",void 0),a1([(0,s.MZ)({attribute:!1})],a6.prototype,"board",void 0),a1([(0,s.MZ)()],a6.prototype,"platform",void 0),a1([(0,s.MZ)({attribute:!1})],a6.prototype,"value",void 0),a1([(0,s.MZ)({attribute:!1})],a6.prototype,"location",void 0),a1([(0,s.MZ)({type:Boolean,attribute:"add-mode"})],a6.prototype,"addMode",void 0),a1([(0,s.MZ)()],a6.prototype,"yaml",void 0),a1([(0,s.MZ)({attribute:!1})],a6.prototype,"focusYamlPath",void 0),a1([(0,s.wk)()],a6.prototype,"_available",void 0),a1([(0,s.wk)()],a6.prototype,"_loading",void 0),a1([(0,s.wk)()],a6.prototype,"_error",void 0),a6=a1([(0,s.EM)("esphome-api-action-editor")],a6),(0,M.C)({"arrow-decision-outline":r.mdiArrowDecisionOutline,"open-in-new":r.mdiOpenInNew});let a8=["device_on","component_on","interval","script"];class a9 extends n.WF{render(){let e=this.value&&"component_action"!==this.value.kind?this.value.kind:"device_on";return(0,n.qy)`
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
          ${a8.map(t=>(0,n.qy)`<wa-option value=${t} ?selected=${t===e}
                >${this._kindLabel(t)}</wa-option
              >`)}
        </wa-select>
        ${this._renderKindBody(e)}
      </div>
    `}_kindLabel(e){switch(e){case"device_on":return this._localize("device.automation_target_device");case"component_on":return this._localize("device.automation_target_component");case"interval":return this._localize("device.automation_target_interval");case"script":return this._localize("device.automation_target_script");case"api_action":return this._localize("device.automation_target_api_action");case"light_effect":return this._localize("device.automation_light_effect")}}_renderKindBody(e){if("device_on"===e||"interval"===e)return n.s6;if("component_on"===e){let e=this.value?.kind==="component_on"?this.value.component_id:"",t=this.devices.filter(e$);return 0===t.length?(0,n.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_components")}
        </p>`:(0,n.qy)`
        <label class="ae-section-label" id="component-id-label"
          >${this._localize("device.automation_target_component_label")}</label
        >
        <wa-select
          aria-labelledby="component-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onComponentChange(e.target.value)}
        >
          ${t.map(t=>(0,n.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${eb(t)}
                <span class="ae-muted"
                  >(${ew(t,this.devices)})</span
                ></wa-option
              >`)}
        </wa-select>
      `}if("script"===e){let e=this.value?.kind==="script"?this.value.id:"";return this.locked?(0,n.qy)`
          <label class="ae-section-label">
            ${this._localize("device.automation_target_script_label")}
          </label>
          <p class="ae-section-desc">${e}</p>
        `:(0,n.qy)`
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
      `}if("api_action"===e){let e=this.value?.kind==="api_action"?this.value.action_name:"";return(0,n.qy)`
        <label class="ae-section-label">
          ${this._localize("device.automation_target_api_action_label")}
        </label>
        <p class="ae-section-desc">${e}</p>
      `}if("light_effect"===e){let e=this.value?.kind==="light_effect"?this.value.component_id:"",t=this.devices.filter(e=>e.component_id.startsWith("light."));return 0===t.length?(0,n.qy)`<p class="ae-empty" role="status">
          ${this._localize("device.automation_target_no_lights")}
        </p>`:(0,n.qy)`
        <label class="ae-section-label" id="light-id-label"
          >${this._localize("device.automation_target_light_label")}</label
        >
        <wa-select
          aria-labelledby="light-id-label"
          value=${e}
          ?disabled=${this.disabled||this.locked}
          @change=${e=>this._onLightChange(e.target.value)}
        >
          ${t.map(t=>(0,n.qy)`<wa-option value=${t.id} ?selected=${t.id===e}
                >${eb(t)}</wa-option
              >`)}
        </wa-select>
      `}return n.s6}_onKindChange(e){let t=e.target.value,i=(()=>{switch(t){case"device_on":return{kind:t,trigger:"on_boot"};case"interval":return{kind:t,index:0};case"component_on":{let e=ex(this.devices);return e?{kind:t,component_id:e.id,trigger:""}:null}case"script":return{kind:t,id:this.scripts.length?this.scripts[0].id:""};case"light_effect":{let e=this.devices.find(e=>e.component_id.startsWith("light."));return e?{kind:t,component_id:e.id,index:0}:null}case"api_action":return null}})();this._emit(i)}_onComponentChange(e){this.value?.kind==="component_on"&&this._emit({...this.value,component_id:e})}_onScriptChange(e){this._emit({kind:"script",id:e})}_onLightChange(e){this.value?.kind==="light_effect"&&this._emit({...this.value,component_id:e})}_emit(e){this.dispatchEvent(new CustomEvent("target-change",{detail:{target:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value=null,this.devices=[],this.scripts=[],this.disabled=!1,this.locked=!1}}function a7(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}a9.styles=[b.G,ep.z9,ag],a4([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],a9.prototype,"_localize",void 0),a4([(0,s.MZ)({attribute:!1})],a9.prototype,"value",void 0),a4([(0,s.MZ)({attribute:!1})],a9.prototype,"devices",void 0),a4([(0,s.MZ)({attribute:!1})],a9.prototype,"scripts",void 0),a4([(0,s.MZ)({type:Boolean})],a9.prototype,"disabled",void 0),a4([(0,s.MZ)({type:Boolean})],a9.prototype,"locked",void 0),a9=a4([(0,s.EM)("esphome-automation-target-picker")],a9);class re extends n.WF{willUpdate(e){e.has("triggerId")&&(this._showAdvanced=!1)}render(){if(!this.target)return(0,n.qy)`<p class="ae-empty">
        ${this._localize("device.automation_target_placeholder")}
      </p>`;if("interval"===this.target.kind||"script"===this.target.kind||"api_action"===this.target.kind||"light_effect"===this.target.kind)return n.s6;let e=this._filteredTriggers(),t=e.find(e=>e.id===this.triggerId),i="component_on"===this.target.kind?this.target.component_id:null,o=i?this.devices.find(e=>e.id===i)??null:null;return(0,n.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="trigger-label"
          >${this._localize("device.automation_trigger")}</label
        >
        ${o?(0,n.qy)`<p class="ae-section-desc">
                ${this._localize("device.automation_trigger_on_component",{component:eb(o),domain:o.component_id})}
              </p>`:n.s6}
        ${0===e.length?(0,n.qy)`<p class="ae-empty" role="status">
                ${this._localize("device.automation_trigger_none_available")}
              </p>`:(0,n.qy)`<wa-select
                aria-labelledby="trigger-label"
                value=${this.triggerId??""}
                ?disabled=${this.disabled}
                @change=${this._onTriggerChange}
              >
                ${e.map(e=>(0,n.qy)`<wa-option value=${e.id} ?selected=${e.id===this.triggerId}
                      >${e.name}</wa-option
                    >`)}
              </wa-select>`}
        ${t?.description?(0,n.qy)`<p class="ae-section-desc">${(0,en.Gc)(t.description)}</p>`:n.s6}
        ${t&&t.config_entries.length>0?(0,n.qy)`<esphome-config-entry-form
                .entries=${t.config_entries}
                .values=${this.triggerParams}
                .board=${this.board}
                .yaml=${this.yaml}
                ?disabled=${this.disabled}
                advanced-section
                ?show-advanced=${this._showAdvanced}
                @value-change=${this._onParamChange}
                @advanced-toggle=${this._onAdvancedToggle}
              ></esphome-config-entry-form>`:n.s6}
      </div>
    `}_filteredTriggers(){if(!this.target)return[];if("device_on"===this.target.kind)return this.triggers.filter(e=>e.is_device_level);if("component_on"===this.target.kind){let e=this.target.component_id,t=this.devices.find(t=>t.id===e);return ez(this.triggers,t)}return[]}constructor(...e){super(...e),this._localize=e=>e,this.target=null,this.triggers=[],this.devices=[],this.triggerId=null,this.triggerParams={},this.board=null,this.yaml="",this.disabled=!1,this._showAdvanced=!1,this._onTriggerChange=e=>{let t=e.target.value;(0,Z.r)(this,"trigger-change",{triggerId:t,params:{}})},this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onParamChange=e=>{e.stopPropagation();let t=eS(this.triggerParams,e.detail.path,e.detail.value);(0,Z.r)(this,"trigger-params-change",{params:t})}}}function rt(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}re.styles=[b.G,ep.z9,ag],a7([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],re.prototype,"_localize",void 0),a7([(0,s.MZ)({attribute:!1})],re.prototype,"target",void 0),a7([(0,s.MZ)({attribute:!1})],re.prototype,"triggers",void 0),a7([(0,s.MZ)({attribute:!1})],re.prototype,"devices",void 0),a7([(0,s.MZ)()],re.prototype,"triggerId",void 0),a7([(0,s.MZ)({attribute:!1})],re.prototype,"triggerParams",void 0),a7([(0,s.MZ)({attribute:!1})],re.prototype,"board",void 0),a7([(0,s.MZ)()],re.prototype,"yaml",void 0),a7([(0,s.MZ)({type:Boolean})],re.prototype,"disabled",void 0),a7([(0,s.wk)()],re.prototype,"_showAdvanced",void 0),re=a7([(0,s.EM)("esphome-automation-trigger-picker")],re),(0,M.C)({delete:r.mdiDelete});class ri extends n.WF{get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._editMode=!this.addMode}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&eF(t)!==eF(this.location)&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend(),(e.has("location")||e.has("platform"))&&this.location?.kind==="interval"&&this._loadIntervalComponent()}async _loadIntervalComponent(){if(!this._api)return;let e=await a3(this._api,this.platform||void 0,this.board?.id);e&&(this._intervalComponent=e)}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml);this._error="";let t=this._parseError.resolve(e,this.location);t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,ev.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}async _loadAvailable(){if(!this._api||!this.configuration)return;this._loading=!0,this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize,{lists:["triggers","actions","conditions"],yaml:this.yaml,onPaint:e=>{this._available=e,this._loading=!1}});void 0!==t&&(this._error=t,this._loading=!1),e&&(this._available=e,this._loading=!1)}render(){var e,t,i,o,a,r,s,l,d,c,h;let p,u,m,v,g,f;if(this._loading)return(0,n.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let _=this.value??eq(),b=this.location,y=this._available?.devices??[],w=this._available?.scripts??[],$=this._available?.triggers??[],x=this._available?.actions??[],k=this._available?.conditions??[],z=this._engine.deleting,C=_.trigger_id??(b?.kind==="device_on"?b.trigger||null:b?.kind==="component_on"&&function(e,t){if("component_on"!==e.kind||!e.trigger)return null;let i=t.find(t=>t.id===e.component_id),o=i?ey(i.component_id):null;return o?`${o}.${e.trigger}`:e.trigger}(b,y)||null),q=C?$.find(e=>e.id===C)??null:null,S=this._resolveFocus(this.value,this.location,this.focusYamlPath);return(0,n.qy)`
      ${e=this.location,t=this._intervalComponent,i=this._localize,p=e?.kind==="interval"?t:null,u=p?.name??(e?.kind==="interval"?i("device.automation_interval_label"):q&&(e?.kind==="device_on"||e?.kind==="component_on")?q.name:e?.kind==="component_action"?a5(e.field,i):i("device.automation_header_title_static")),m=p?.docs_url??q?.docs_url??"",v=p?.description??q?.description??i("device.automation_header_description"),g=p?.image_url??"",(0,n.qy)`<div class="ae-header">
    <div class="ae-header-text">
      <h2 class="ae-header-title">${u}</h2>
      ${m?(0,n.qy)`<a
              class="ae-header-docs"
              href=${m}
              target="_blank"
              rel="noreferrer"
            >
              ${i("device.docs")}
              <wa-icon library="mdi" name="open-in-new"></wa-icon>
            </a>`:n.s6}
      <p class="ae-header-desc">${(0,en.Gc)(v)}</p>
    </div>
    <div class="ae-header-icon">
      ${g?(0,n.qy)`<img alt="" src=${g} />`:(0,n.qy)`<wa-icon library="mdi" name="arrow-decision-outline"></wa-icon>`}
    </div>
  </div>`}
      ${this.addMode?(o={target:b,triggers:$,devices:y,scripts:w,effectiveTriggerId:C,automation:_,board:this.board,yaml:this.yaml,disabled:z,onTargetChange:this._onTargetChange,onTriggerChange:this._onTriggerChange,onTriggerParamsChange:this._onTriggerParamsChange},(0,n.qy)`
    <esphome-automation-target-picker
      .value=${o.target}
      .devices=${o.devices}
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
  `):(0,n.qy)`${function(e,t,i,o){var a;return e&&("component_on"===e.kind||"component_action"===e.kind)?(a=function(e,t,i){switch(e.kind){case"device_on":return i("device.automation_target_device");case"component_on":case"component_action":{let i=t.find(t=>t.id===e.component_id);if(!i)return e.component_id;return`${eb(i)} (${i.component_id})`}case"interval":return i("device.automation_target_interval_n",{index:e.index+1});case"script":return e.id;case"api_action":return e.action_name;case"light_effect":return e.component_id}}(e,t,o),(0,n.qy)`<div class="field">
    <label class="field-label"> ${o("device.automation_target")} </label>
    <input type="text" readonly .value=${a} />
    ${tP(a,i,o)}
  </div>`):n.s6}(this.location,y,this._parseSubstitutions(this.yaml),this._localize)}${d=(a={location:this.location,intervalComponent:this._intervalComponent,activeTrigger:q,automation:_,board:this.board,yaml:this.yaml,disabled:z,showAdvanced:this._showAdvanced,focusFieldPath:ay(S),onValueChange:this._onTriggerParamsValueChange,onAdvancedToggle:this._onAdvancedToggle}).location,c=a.intervalComponent,h=a.activeTrigger,0===(f=d?.kind==="interval"?c?c.config_entries.filter(e=>"then"!==e.key):[]:h?.config_entries??[]).length?n.s6:(0,n.qy)`
    <esphome-config-entry-form
      .entries=${f}
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
      ${r={automation:_,catalog:x,conditionCatalog:k,scripts:w,devices:y,board:this.board,yaml:this.yaml,disabled:z,localize:this._localize,focusTarget:ab(S),onOpenPicker:()=>this._actionList?.openPicker(),onActionsChange:this._onActionsChange},(0,n.qy)`
    <div class="field">
      <div class="ae-actions-header">
        <label class="field-label"> ${r.localize("device.automation_action")} </label>
        <button
          type="button"
          class="ae-section-add"
          ?disabled=${r.disabled||0===r.catalog.length}
          @click=${r.onOpenPicker}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${r.localize("device.add_action")}
        </button>
      </div>
      <p class="field-description">
        ${(0,en.Gc)(r.localize("device.automation_actions_description"))}
      </p>
      <esphome-automation-action-list
        no-header
        hide-add
        .focusTarget=${r.focusTarget??null}
        .actions=${r.automation.actions}
        .catalog=${r.catalog}
        .conditionCatalog=${r.conditionCatalog}
        .scripts=${r.scripts}
        .devices=${r.devices}
        .board=${r.board}
        .yaml=${r.yaml}
        ?disabled=${r.disabled}
        @actions-change=${r.onActionsChange}
      ></esphome-automation-action-list>
    </div>
  `}
      ${this._error?(0,n.qy)`<p class="ae-error" role="alert">${this._error}</p>`:n.s6}
      ${this.location&&this.value&&!this.addMode?(s=this._localize,l=this._onDelete,(0,n.qy)`<div class="ae-actions">
    <button type="button" class="ae-danger" ?disabled=${z} @click=${l}>
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${s("device.delete_automation")}
    </button>
  </div>`):n.s6}
    `}flushPending(){return this._engine.flushPending()}static get _actionStyles(){return null}get _devicesForTest(){return this._available?.devices??[]}get _scriptsForTest(){return this._available?.scripts??[]}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._intervalComponent=null,this._loading=!0,this._error="",this._parseError=new a0(this),this._catalogLoad=new aX(this),this._showAdvanced=!1,this._engine=new ah(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,setError:e=>{this._error=e}}),this._editMode=!1,this._parseSubstitutions=(0,l.A)(t_.Gr),this._resolveFocus=az(),this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onTriggerParamsValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,o=eS((this.value??eq()).trigger_params,t,i);this._engine.withValue({trigger_params:o})},this._onTargetChange=e=>{e.stopPropagation(),this.location=e.detail.target,this._engine.withValue({trigger_id:null,trigger_params:{}})},this._onTriggerChange=e=>{if(e.stopPropagation(),this._engine.withValue({trigger_id:e.detail.triggerId,trigger_params:e.detail.params}),this.location?.kind==="device_on")this.location={...this.location,trigger:e.detail.triggerId};else if(this.location?.kind==="component_on"){var t;let i,o=(i=(t=e.detail.triggerId).indexOf("."))>=0?t.slice(i+1):t;this.location={...this.location,trigger:o}}},this._onTriggerParamsChange=e=>{e.stopPropagation(),this._engine.withValue({trigger_params:e.detail.params})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}function ro(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}ri.styles=[b.G,ep.z9,ag],rt([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],ri.prototype,"_localize",void 0),rt([(0,a.Fg)({context:_.Ie})],ri.prototype,"_api",void 0),rt([(0,s.MZ)()],ri.prototype,"configuration",void 0),rt([(0,s.MZ)({attribute:!1})],ri.prototype,"board",void 0),rt([(0,s.MZ)()],ri.prototype,"platform",void 0),rt([(0,s.MZ)({attribute:!1})],ri.prototype,"value",void 0),rt([(0,s.MZ)({attribute:!1})],ri.prototype,"location",void 0),rt([(0,s.MZ)({type:Boolean,attribute:"add-mode"})],ri.prototype,"addMode",void 0),rt([(0,s.MZ)()],ri.prototype,"yaml",void 0),rt([(0,s.MZ)({attribute:!1})],ri.prototype,"focusYamlPath",void 0),rt([(0,s.P)("esphome-automation-action-list")],ri.prototype,"_actionList",void 0),rt([(0,s.wk)()],ri.prototype,"_available",void 0),rt([(0,s.wk)()],ri.prototype,"_intervalComponent",void 0),rt([(0,s.wk)()],ri.prototype,"_loading",void 0),rt([(0,s.wk)()],ri.prototype,"_error",void 0),rt([(0,s.wk)()],ri.prototype,"_showAdvanced",void 0),rt([(0,s.wk)()],ri.prototype,"_editMode",void 0),ri=rt([(0,s.EM)("esphome-automation-editor")],ri),(0,M.C)({delete:r.mdiDelete,"open-in-new":r.mdiOpenInNew,"script-text-outline":r.mdiScriptTextOutline});class ra extends n.WF{willUpdate(){let e=this._resolveFocus(this.value,this.location,this.focusYamlPath),t=a$(e);t!==this._paramsRevealKey&&(this._paramsRevealKey=t,null!==aw(e,"parameters")&&(this._showAdvanced=!0))}get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._load()}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.id!==this.location.id&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable(),this._loadScriptComponent()}catch(e){this._error=(0,em.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _loadScriptComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,e5.CQ)("script",e,t);if(i){this._scriptComponent=i;return}try{let i=await (0,e5.Sn)(this._api,"script",e,t);i&&(this._scriptComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"script");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,ev.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}render(){if(this._loading)return(0,n.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??eq(),t=this._available?.devices??[],i=this._available?.scripts??[],o=this._available?.actions??[],a=this._available?.conditions??[],r=this._engine.deleting,s=this._resolveFocus(this.value,this.location,this.focusYamlPath);return(0,n.qy)`
      ${this._renderHeader()} ${this._renderConfigForm(e,r,s)}
      ${this._showAdvanced?this._renderParametersField(e,r,s):n.s6}
      <div class="field">
        <div class="ae-actions-header">
          <label class="field-label">
            ${this._localize("device.automation_action")}
          </label>
          <button
            type="button"
            class="ae-section-add"
            ?disabled=${r||0===o.length}
            @click=${()=>this._actionList?.openPicker()}
          >
            <wa-icon library="mdi" name="plus"></wa-icon>
            ${this._localize("device.add_action")}
          </button>
        </div>
        <p class="field-description">
          ${(0,en.Gc)(this._localize("device.script_actions_description"))}
        </p>
        <esphome-automation-action-list
          no-header
          hide-add
          .focusTarget=${ab(s)}
          .actions=${e.actions}
          .catalog=${o}
          .conditionCatalog=${a}
          .scripts=${i}
          .devices=${t}
          .board=${this.board}
          .yaml=${this.yaml}
          ?disabled=${r}
          @actions-change=${this._onActionsChange}
        ></esphome-automation-action-list>
      </div>
      ${this._error?(0,n.qy)`<p class="ae-error" role="alert">${this._error}</p>`:n.s6}
      ${this.location&&this.value&&!this.addMode?(0,n.qy)`<div class="ae-actions">
              <button
                type="button"
                class="ae-danger"
                ?disabled=${r}
                @click=${this._onDelete}
              >
                <wa-icon library="mdi" name="delete"></wa-icon>
                ${this._localize("device.delete_script")}
              </button>
            </div>`:n.s6}
    `}_renderHeader(){let e=this._scriptComponent,t=e?.name??this._localize("device.script_header_title_static"),i=e?.description??this._localize("device.script_header_description"),o=e?.docs_url??`${ad.Ik}/components/script.html`,a=e?.image_url??"";return(0,n.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${t}</h2>
        <a class="ae-header-docs" href=${o} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">${(0,en.Gc)(i)}</p>
      </div>
      <div class="ae-header-icon">
        ${a?(0,n.qy)`<img alt="" src=${a} />`:(0,n.qy)`<wa-icon library="mdi" name="script-text-outline"></wa-icon>`}
      </div>
    </div>`}_renderConfigForm(e,t,i){let o=this._scriptComponent;if(!o)return n.s6;let a=o.config_entries.filter(e=>"parameters"!==e.key&&"then"!==e.key),r=this._hasParametersEntry();return 0!==a.length||r?(0,n.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${e.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        .focusFieldPath=${null===aw(i,"parameters")?ay(i):void 0}
        ?disabled=${t}
        advanced-section
        ?force-advanced-control=${r}
        .advancedExtraCount=${+!!r}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onConfigFormValueChange}
        @advanced-toggle=${this._onAdvancedToggle}
      ></esphome-config-entry-form>
    `:n.s6}_hasParametersEntry(){return this._scriptComponent?.config_entries.some(e=>"parameters"===e.key)??!1}_renderParametersField(e,t,i){let o=e.trigger_params.parameters??{};return(0,n.qy)`<esphome-callable-params-editor
      .value=${o}
      .focusParam=${aw(i,"parameters")}
      ?disabled=${t}
      .fieldLabel=${this._localize("device.automation_script_parameters")}
      .description=${this._localize("device.script_parameters_description")}
      .addLabel=${this._localize("device.script_add_parameter")}
      .namePlaceholder=${this._localize("device.script_parameter_name_placeholder")}
      @value-change=${this._onParametersChange}
    ></esphome-callable-params-editor>`}flushPending(){return this._engine.flushPending()}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._resolveFocus=az(),this._available=null,this._loading=!0,this._error="",this._parseError=new a0(this),this._scriptComponent=null,this._showAdvanced=!1,this._engine=new ah(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,canApply:e=>"script"===e.kind&&!!e.id,setError:e=>{this._error=e}}),this._catalogLoad=new aX(this),this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onConfigFormValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,o=this.value??eq(),a=1===t.length&&"id"===t[0]?(0,ac.e)(String(i??"")):i,r=eS(o.trigger_params,t,a);if(1===t.length&&"id"===t[0]){let e=String(a??"");e&&(this.location={kind:"script",id:e})}this._engine.withValue({trigger_params:r})},this._onParametersChange=e=>{e.stopPropagation();let t=this.value??eq();this._engine.withValue({trigger_params:{...t.trigger_params,parameters:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}ra.styles=[b.G,ep.z9,ag],ro([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],ra.prototype,"_localize",void 0),ro([(0,a.Fg)({context:_.Ie})],ra.prototype,"_api",void 0),ro([(0,s.MZ)()],ra.prototype,"configuration",void 0),ro([(0,s.MZ)({attribute:!1})],ra.prototype,"board",void 0),ro([(0,s.MZ)()],ra.prototype,"platform",void 0),ro([(0,s.MZ)({attribute:!1})],ra.prototype,"value",void 0),ro([(0,s.MZ)({attribute:!1})],ra.prototype,"location",void 0),ro([(0,s.MZ)({type:Boolean,attribute:"add-mode"})],ra.prototype,"addMode",void 0),ro([(0,s.MZ)()],ra.prototype,"yaml",void 0),ro([(0,s.MZ)({attribute:!1})],ra.prototype,"focusYamlPath",void 0),ro([(0,s.P)("esphome-automation-action-list")],ra.prototype,"_actionList",void 0),ro([(0,s.wk)()],ra.prototype,"_available",void 0),ro([(0,s.wk)()],ra.prototype,"_loading",void 0),ro([(0,s.wk)()],ra.prototype,"_error",void 0),ro([(0,s.wk)()],ra.prototype,"_scriptComponent",void 0),ro([(0,s.wk)()],ra.prototype,"_showAdvanced",void 0),ra=ro([(0,s.EM)("esphome-script-editor")],ra),i(2547);var rr=i(6049);class rn{hostConnected(){this._unsubscribe=oa(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}ensure(){let{api:e,platform:t,boardId:i}=this._context();e&&void 0===i9(t,i)&&i8.triggers.fetch(e,t,i).catch(()=>{})}resolveName(e,t,i){let{platform:o,boardId:a}=this._context(),r=i9(o,a);if(!r)return i;let n="esphome"===e?t:`${e}.${t}`;return r.find(e=>e.id===n)?.name||i}hasTriggersFor(e){let{platform:t,boardId:i}=this._context(),o=i9(t,i);return!o||o.some(t=>t.applies_to.some(t=>e.includes(t)))}constructor(e,t){this._host=e,this._context=t,e.addController(this)}}let rs=new Set(["external_components","packages"]),rl=(0,n.AH)`
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
`;i(900);var rd=i(9789);let rc=e=>"!lambda"===e.tag&&"|-"===e.marker,rh=e=>({_lambda:new eG.ho(e).body.replace(/\n+$/,""),_tag:"!lambda"}),rp=(e,t,i)=>rc(e)?rh(i):new eG.ho(i,t);var ru=i(9808);let rm=(e,t,i)=>{if(e.includes(".")||(0,rd.CI)(t))return null;let{value:o,comment:a}=(0,ru.X9)(t,i);return""===o?{key:e,value:null}:o.startsWith("[")&&o.endsWith("]")?{key:e,value:eG.aZ.wrap((0,ru.Wg)(o),a)}:{key:e,value:(0,ru.Qj)(o)}},rv=(e,t)=>{let i=e.match(t);return i?rm(i[1],i[3].trim(),i[2].length>0):null},rg=(e,t,i)=>{let o=-1,a=t-1;for(let r=t;r<e.length;r++){if(""===e[r].trim())continue;let t=(0,rd.MG)(e[r]).length;if(-1===o){if(t<=i)break;o=t}else if(t<o)break;a=r}return a+1},rf=(e,t,i)=>{let{dashIndent:o,firstDashIdx:a}=((e,t,i)=>{let o=t;for(;o<e.length&&(0,rd.BJ)(e[o]);)o++;return o>=e.length?{dashIndent:i,firstDashIdx:o}:{dashIndent:e[o].match(/^( *)-/)?.[1]??i,firstDashIdx:o}})(e,t,`${i}  `),r=(e[a]??"").match(rd.o1),n=r?" ".repeat(r[1].length):(0,rd.G5)(e,a+1,o)??`${o}  `,{endIdx:s,isComplex:l}=((e,t,i)=>{let o=!1;for(let a=t;a<e.length;a++){let t=e[a];if(!(0,rd.BJ)(t)){if((0,rd.PM)(t,i.length))return{endIdx:a,isComplex:o};!o&&(rd.PL.test(t)||rd.uT.test(t)||rd.Vi.test(t))&&(o=!0)}}return{endIdx:e.length,isComplex:o}})(e,t,i);if(l){let i=ry(e,t,o,n);return i?{value:i.items,endIdx:i.endIdx,isEmptyScalarList:!1,listSource:i.items.length>0?{itemRanges:i.itemRanges,dashIndent:o}:void 0}:{value:new eG.ho(e.slice(t,s)),endIdx:s,isEmptyScalarList:!1}}let{items:d,endIdx:c,itemRanges:h,inlineComments:p}=((e,t,i,o)=>{let a=[],r=[],n=[],s=t;for(;s<e.length;s++){if((0,rd.BJ)(e[s]))continue;if(!e[s].startsWith(i))break;let t=e[s].match(o);if(!t)break;let{value:l,comment:d}=(0,ru.dZ)(t[1].trim());a.push((0,ru.Tg)((0,ru.Ir)(l),(0,ru.N_)(l))),r.push([s,s+1]),n.push(d)}return{items:a,endIdx:s,itemRanges:r,inlineComments:n}})(e,t,`${o}- `,(0,rd.iu)(o));return{value:d,endIdx:c,isEmptyScalarList:0===d.length,listSource:{itemRanges:h,inlineComments:p,dashIndent:o}}},r_=(e,t,i)=>{let o=(0,rd.K7)(e,t+1);if(o>=e.length)return null;let a=(0,rd.MG)(e[o]);return a.length<=i?null:e[o].slice(a.length).startsWith("-")?"bail":rw(e,t+1,a)},rb=(e,t,i,o,a)=>{let r=t;for(;r<e.length;){let t=e[r];if((0,rd.BJ)(t)){r++;continue}if(!t.startsWith(i))break;if(t.startsWith(`${i} `))return null;let n=rv(t,o);if(!n)return null;if(null===n.value){let t=r_(e,r,i.length);if("bail"===t)return null;if(t){a[n.key]=Object.keys(t.values).length>0?t.values:n.value,r=t.endIdx;continue}}a[n.key]=n.value,r++}return r},ry=(e,t,i,o)=>{let a=RegExp(`^${i}-\\s+(${rd.bn}):(\\s*)(.*)$`),r=RegExp(`^${o}(${rd.bn}):(\\s*)(.*)$`),n=t=>{let n=Object.create(null),s=null;if(!rd.Vi.test(e[t])){let o=e[t].match(a);if(!o)return null;let r=o[1],l=o[2].length>0,d=o[3].trim();if(!l&&""!==d)return null;let c=(0,rd.CI)(d);if(c){if(!rc(c))return null;let o=rg(e,t+1,`${i}  `.length),a=(0,rd.K7)(e,o);return a<e.length&&(0,rd.MG)(e[a]).length>i.length?null:(n[r]=rh(e.slice(t+1,o)),{item:n,endIdx:o})}let h=rm(r,d,l);if(!h)return null;n[h.key]=h.value,null===h.value&&(s=h.key)}if(null!==s){let a=e[t].match(rd.o1)?.[1].length??i.length+2,l=r_(e,t,a);if("bail"===l)return null;if(l){Object.keys(l.values).length>0&&(n[s]=l.values);let t=rb(e,l.endIdx,o,r,n);return null===t?null:{item:n,endIdx:t}}}let l=rb(e,t+1,o,r,n);return null===l?null:{item:n,endIdx:l}},s=[],l=[],d=t;for(;d<e.length;){if((0,rd.BJ)(e[d])){d++;continue}if(!(0,rd.AL)(e[d],i))break;let t=n(d);if(!t)return null;s.push(t.item);let o=t.endIdx;for(;o>d+1&&(0,rd.BJ)(e[o-1]);)o--;l.push([d,o]),d=t.endIdx}return{items:s,endIdx:d,itemRanges:l}};function rw(e,t,i){let o=(0,rd.zM)(i),a=Object.create(null),r=t;for(;r<e.length;){let t=e[r];if((0,rd.BJ)(t)){r++;continue}if(!t.startsWith(i))break;let n=t.match(o);if(!n){r++;continue}let s=n[1],l=n[2].length>0,d=n[3].trim(),c=(0,rd.CI)(d);if(c){let t=rg(e,r+1,i.length);a[s]=rp(c,d,e.slice(r+1,t)),r=t;continue}let{value:h,comment:p}=(0,ru.X9)(d,l);if(""===h){let t=(0,rd.K7)(e,r+1);if(t<e.length&&(0,rd.SU)(e[t],i)){let{value:t,endIdx:o}=rf(e,r+1,i);a[s]=t,r=o;continue}if(t<e.length){let o=(0,rd.MG)(e[t]);if(o.length>i.length){let t=rw(e,r+1,o);Object.keys(t.values).length>0&&(a[s]=t.values),r=t.endIdx;continue}}a[s]=null,r++;continue}h.startsWith("[")&&h.endsWith("]")?a[s]=eG.aZ.wrap((0,ru.Wg)(h),p):a[s]=(0,ru.Qj)(h),r++}return{values:a,endIdx:r}}function r$(e,t,i){if(void 0!==i)return i-1;for(let i=0;i<e.length;i++)if(e[i].startsWith(`${t}:`))return i;return -1}function rx(e,t,i){let o=Object.create(null),a=new Map,r=(e,t,i)=>{let o={span:{start:t,end:i,leadStart:t}};return a.set(e,o),o},n=r$(e,t,i);if(n<0)return{values:o,keys:a,childIndent:"",isListItem:!1,startIdx:n};let s=rd.WV.test(e[n]),l=(0,rd.eq)(e,n,s),d=(0,rd.zM)(l),c=t=>{let i=(0,rd.K7)(e,t);if(i>=e.length)return null;let o=(0,rd.MG)(e[i]);return o.length<=l.length?null:rw(e,t,o)};if(!s&&rr.sU.has(t)){let i=(0,rd.MG)(e[n]),r=(0,rd.K7)(e,n+1);if(r<e.length&&(0,rd.SU)(e[r],i))return o[t]=rf(e,n+1,i).value,{values:o,keys:a,childIndent:l,isListItem:s,startIdx:n}}if(s){let t=e[n].match(rd.L1);if(t){let i=e[n],r=i.slice(i.indexOf(":",i.indexOf("-"))+1),{value:s,comment:l}=(0,ru.bw)(r),d=s.trim();if(""!==d)l&&a.set(t[1],{comment:l}),o[t[1]]=(0,ru.Qj)(d);else{let e=c(n+1);e&&Object.keys(e.values).length>0&&(o[t[1]]=e.values)}}}let h=s?(e[n].match(/^(\s*)-/)??["",""])[1].length:-1;for(let t=n+1;t<e.length;t++){let i=e[t];if((0,rd.BJ)(i))continue;if(s){let e=i.match(/^(\s*)-(\s|$)/);if(e&&e[1].length===h||rd.QW.test(i))break}else if(rd.QW.test(i))break;let a=i.match(d);if(!a)continue;let n=a[1],p=a[2].length>0,u=a[3].trim(),m=(0,rd.CI)(u);if(m){let i=rg(e,t+1,l.length);o[n]=rp(m,u,e.slice(t+1,i)),r(n,t,i),t=i-1;continue}let{value:v,comment:g}=(0,ru.X9)(u,p);if(""===v){let i=(0,rd.K7)(e,t+1);if(i<e.length&&(0,rd.SU)(e[i],l)){let{value:i,endIdx:a,isEmptyScalarList:s,listSource:d}=rf(e,t+1,l);if(!s){o[n]=i;let e=r(n,t,a);d&&(e.listSource=d),g&&(e.comment=g),t=a-1}continue}let a=c(t+1),s=a?.endIdx??t+1;o[n]=a&&Object.keys(a.values).length>0?a.values:null;let d=r(n,t,s);g&&(d.comment=g),t=s-1;continue}if(v.startsWith("[")&&v.endsWith("]")){o[n]=(0,ru.Wg)(v);let e=r(n,t,t+1);e.flowList=!0,g&&(e.comment=g);continue}o[n]=(0,ru.Qj)(v);let f=r(n,t,t+1);g&&(f.comment=g)}for(let{span:t}of a.values()){if(!t)continue;let i=t.start+1,o=t.end,a=!1;for(;o>i&&(0,rd.BJ)(e[o-1])&&(0,rd.MG)(e[o-1]).length<=l.length;)o--,(0,rd.w5)(e[o])&&(a=!0);a&&(t.end=o)}let p=n+1;for(let{span:t}of a.values()){if(!t)continue;let i=t.start;for(;i>p&&(0,rd.BJ)(e[i-1]);)i--;t.leadStart=i,p=t.end}return{values:o,keys:a,childIndent:l,isListItem:s,startIdx:n}}function rk(e,t){if(e===t)return!0;if(e instanceof eG.ho||t instanceof eG.ho)return e instanceof eG.ho&&t instanceof eG.ho&&e.inlineHeader===t.inlineHeader&&e.lines.length===t.lines.length&&e.lines.every((e,i)=>e===t.lines[i]);if(Array.isArray(e)||Array.isArray(t))return Array.isArray(e)&&Array.isArray(t)&&e.length===t.length&&e.every((e,i)=>rk(e,t[i]));if((0,eC.Qd)(e)&&(0,eC.Qd)(t)){let i=Object.keys(e);return i.length===Object.keys(t).length&&i.every(i=>Object.prototype.hasOwnProperty.call(t,i)&&rk(e[i],t[i]))}return!1}let rz=e=>(0,eC.k4)(e)&&null!=e,rC=e=>rz(e)||(0,eC.Qd)(e);function rq(e,t,i){let o=r$(e,t,i);if(o<0)return{start:-1,end:-1};let a=rd.WV.test(e[o]),r=a?(e[o].match(/^(\s*)-/)??["",""])[1].length:-1,n=e.length;for(let t=o+1;t<e.length;t++)if(a){let i=e[t].match(/^(\s*)-(\s|$)/);if(i&&i[1].length===r||rd.QW.test(e[t])){n=t;break}}else if(rd.QW.test(e[t])){n=t;break}return{start:o,end:n}}function rS(e){if(e._draftTimer=null,!e._config)return;let t=(0,rr.a7)(e.sectionKey,e._config.entries);e._fieldErrors=(0,to.JK)(t,e._values,e._presentComponents,e.board?.esphome.platform??null,e.sectionKey);let i=(0,L.uv)(e.yaml,e.sectionKey,e.fromLine);if(void 0===i)return void e._setDirty(!1);let o=function(e,t,i,o,a={}){let r=e.split("\n"),{start:n,end:s}=rq(r,t,o);if(n<0)return e;let l=rd.WV.test(r[n]),d=(0,rd.eq)(r,n,l),c=function(e,t,i,o){let a=-1;for(let o=t+1;o<i;o++){let t=e[o];if(""===t.trim()||(0,rd.w5)(t))continue;let i=(0,rd.MG)(t).length;i>a&&(a=i)}return a<0?o:a}(r,n,s,d.length),h=s;for(;h>n+1;){let e=r[h-1];if(""===e.trim()){h--;continue}let t=(0,rd.MG)(e).length;if((0,rd.w5)(e)&&(t<=d.length||t<c))h--;else break}let p=h;if(rr.sU.has(t)){let o=i[t];if(!Array.isArray(o))return e;let s=(0,eG.ym)({[t]:o},(0,rd.MG)(r[n]),{...a,indentStep:a.indentStep??(d||"  ")});return r.splice(n,p-n,...s),r.join("\n")}let u=rx(r,t,o),m=-1;for(let{span:e}of u.keys.values())e&&e.end>m&&(m=e.end);m>=0&&(p=m);let v=r[n],g=new Set;if(l){let e=v.match(rd.L1);if(e){let t=e[1];if(Object.prototype.hasOwnProperty.call(i,t))if(function(e){if(null==e)return!1;let t=typeof e;return"string"===t||"number"===t||"boolean"===t}(i[t])){if(g.add(t),!rk(i[t],u.values[t])){let e=v.match(/^(\s*)-(\s+)/),o=`${e[1]}-${e[2]}`,a=u.keys.get(t)?.comment??"";v=`${o}${t}: ${(0,eG.Rm)(i[t])}${a}`}}else{let e=(v.match(/^(\s*)-/)??["",""])[1];v=`${e}-`}}}let f=!l&&d?d:"  ",_=[v,...function(e,t,i,o,a,r){let n=[];for(let[h,p]of Object.entries(i)){var s,l,d,c;if(o.has(h))continue;let i=t.keys.get(h),u=i?.span,m=t.values[h];if(u&&rk(p,m)){n.push(...e.slice(u.leadStart,u.end));continue}let v=i&&function(e,t,i,o,a,r){let{span:n,listSource:s}=t;if(!n||!s||!Array.isArray(i)||!Array.isArray(o)||0===o.length||!o.every(rC))return null;let l=0;for(;l<i.length&&l<o.length&&rk(i[l],o[l]);)l++;let d=0;for(;d<i.length-l&&d<o.length-l&&rk(i[i.length-1-d],o[o.length-1-d]);)d++;let{itemRanges:c,dashIndent:h}=s,p=`${a}${r.indentStep??"  "}`,u=e=>0===e?n.start+1:c[e-1][1],m=i.length===o.length;if(h!==p){for(let e=l;e<o.length-d;e++)if(!(m&&rk(i[e],o[e]))&&!rz(o[e]))return null}let v=[];v.push(...e.slice(n.leadStart,u(l)));for(let t=l;t<o.length-d;t++){if(m&&rk(i[t],o[t])){v.push(...e.slice(u(t),c[t][1]));continue}if(m&&v.push(...e.slice(u(t),c[t][0])),rz(o[t])){let e=m?s.inlineComments?.[t]??"":"";v.push(`${h}- ${(0,eG.Rm)(o[t])}${e}`)}else v.push(...(0,eG.qV)(o[t],a,r))}return v.push(...e.slice(u(i.length-d),n.end)),v}(e,i,m,p,a,r);if(v){n.push(...v);continue}u&&n.push(...e.slice(u.leadStart,u.start));let g=(s=i,l=h,d=p,c=a,(s?.flowList&&Array.isArray(d)&&0!==d.length&&d.every(rz)?[`${c}${l}: ${(0,eG.P1)(d)}`]:null)??(0,eG.ym)({[h]:p},a,r));i?.comment&&1===g.length&&(g[0]+=i.comment),n.push(...g)}return n}(r,u,i,g,d,{...a,indentStep:a.indentStep??f})];return r.splice(n,p-n,..._),r.join("\n")}(e.yaml,e.sectionKey,e._values,i,{keepEmptyStrings:rr.fq.has(e.sectionKey)});e._setDirty(!1),o!==e.yaml&&(e._lastSelfWrittenYaml=o,(0,Z.r)(e,"yaml-draft",{yaml:o}))}async function rA(e){if(!e._config)return;let t=(0,L.uv)(e.yaml,e.sectionKey,e.fromLine);if(void 0===t){e._error=e._localize("device.section_delete_error");return}e._deleting=!0,e._error="";let i=e._config.title;try{let o=function(e,t,i){let o=e.split("\n"),{start:a,end:r}=rq(o,t,i);if(a<0)return e;let n=rd.WV.test(o[a]);if(o.splice(a,r-a),n){let e=a-1;for(;e>=0&&!rd.QW.test(o[e]);)e--;if(e>=0){let t=!1,i=o.length;for(let a=e+1;a<o.length;a++){if(rd.QW.test(o[a])){i=a;break}if(""!==o[a].trim()){t=!0;break}}t||o.splice(e,i-e)}}return o.join("\n")}(e.yaml,e.sectionKey,t);if(o===e.yaml){e._error=e._localize("device.section_delete_error");return}await e._api.updateConfig(e.configuration,o),e._setDirty(!1),(0,Z.r)(e,"yaml-updated",{yaml:o}),(0,Z.r)(e,"section-select",{sectionKey:null}),(0,d.VX)(e._localize("device.section_deleted",{name:i}))}catch(t){e._error=(0,ev.K)(t,e._localize,"device.section_delete_error")}finally{e._deleting=!1}}async function rM(e){let t=++e._loadId;e._loading=!0,e._error="",e._config=null,e._isUnknown=!1,e._isPlatformDomain=!1,e._setDirty(!1),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),e._lastSelfWrittenYaml=null;try{var i;let o=e.board?.esphome.platform,a=await (0,e5.Sn)(e._api,e.sectionKey,o);if(t!==e._loadId)return;let r=e.yaml;if(a)e._config={section_key:e.sectionKey,section_type:"core",title:a.name,description:a.description,docs_url:a.docs_url,icon:"",image_url:a.image_url,entries:a.config_entries,required_groups:a.required_groups??[]};else{let i=(0,I.Po)(await (0,D.ak)(e._api)).has(e.sectionKey);if(t!==e._loadId)return;e._config={section_key:e.sectionKey,section_type:"core",title:e.sectionKey,description:"",docs_url:"",icon:"",image_url:"",entries:[],required_groups:[]},e._isPlatformDomain=i,e._isUnknown=!i}let n=(0,L.uv)(r,e.sectionKey,e.fromLine),s=(i=e.sectionKey,rx(r.split("\n"),i,n).values);e._values=(0,iF.Dq)(s,e._config.entries),e._resolvedFromLine=n,e._presentComponents=(0,eG.Zn)(r)}catch(o){if(t!==e._loadId)return;let i=o instanceof Error?o.message:"";e._error=i.includes("timed out")?e._localize("device.load_config_error"):i||e._localize("device.load_config_error")}finally{t===e._loadId&&(e._loading=!1)}}function rP(e,t){if(e._showAdvanced||!e._config||e._autoRevealedSections.has(e.sectionKey))return;let i=(0,rr.a7)(e.sectionKey,e._config.entries);t.some(e=>t3(i,e))&&(e._autoRevealedSections.add(e.sectionKey),e._setShowAdvanced(!0))}function rE(e,t){e.dispatchEvent(new CustomEvent("apply-section-values",{detail:{changes:t},bubbles:!0,composed:!0}))}let rF=(0,n.AH)`
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
`;function rL(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({update:r.mdiUpdate});let rO=/^GPIO(\d+)_(IN|OUT)$/,rR={ethernet:[{key:"clk_mode",copyPrefix:"ethernet_clk_mode",migrate:e=>{if("string"!=typeof e)return null;let t=rO.exec(e.trim().toUpperCase().replace(/ /g,"_"));return t?[{path:["clk"],value:{pin:`GPIO${t[1]}`,mode:"IN"===t[2]?"CLK_EXT_IN":"CLK_OUT"}},{path:["clk_mode"],value:void 0}]:null}}]},rT=e=>Object.prototype.hasOwnProperty.call(rR,e);class rD extends n.WF{_migratable(){if(!rT(this.sectionKey))return[];let e=[];for(let t of rR[this.sectionKey]){if(!Object.prototype.hasOwnProperty.call(this.values,t.key))continue;let i=this.entries.find(e=>e.key===t.key);if(i&&!(0,to.VP)(i,this.values,void 0,void 0,void 0,this.entries))continue;let o=t.migrate(this.values[t.key]);o&&e.push({option:t,changes:o})}return e}_onMigrate(e){rE(this,e),(0,d.VX)(this._localize("device.deprecation_applied"))}render(){let e=this._migratable();return 0===e.length?n.s6:e.map(({option:e,changes:t})=>(0,n.qy)`
        <div class="notice" role="note">
          <wa-icon library="mdi" name="update"></wa-icon>
          <div class="body">
            <p>${this._localize(`device.${e.copyPrefix}_notice`)}</p>
            <button type="button" class="cta" @click=${()=>this._onMigrate(t)}>
              ${this._localize(`device.${e.copyPrefix}_migrate`)}
            </button>
          </div>
        </div>
      `)}constructor(...e){super(...e),this._localize=e=>e,this.sectionKey="",this.values={},this.entries=[]}}async function rI(e=4){let t=Math.max(1,Math.trunc(e)),{PASSPHRASE_WORDS:o}=await i.e(820).then(i.bind(i,2503)),a=o.length,r=Math.floor(0x100000000/a)*a,n=new Uint32Array(1),s=[];for(;s.length<t;)crypto.getRandomValues(n),n[0]>=r||s.push(o[n[0]%a]);return s.join("-")}rD.styles=[b.G,rF],rL([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],rD.prototype,"_localize",void 0),rL([(0,s.MZ)()],rD.prototype,"sectionKey",void 0),rL([(0,s.MZ)({attribute:!1})],rD.prototype,"values",void 0),rL([(0,s.MZ)({attribute:!1})],rD.prototype,"entries",void 0),rD=rL([(0,s.EM)("esphome-deprecation-notice")],rD);var rB=i(8818);function rj(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({"lock-alert":r.mdiLockAlert});let rK=()=>rI(),rU={api:{secretSection:"api",marker:"encryption",copyPrefix:"api_encryption",fields:[{path:["encryption","key"],generate:tu.My,secretField:"key"}]},"ota.esphome":{secretSection:"ota.esphome",marker:"password",copyPrefix:"ota_password",fields:[{path:["password"],generate:rK,secretField:"password"}]},web_server:{secretSection:"web_server",marker:"auth",copyPrefix:"web_auth",fields:[{path:["auth","username"],generate:()=>rI(1)},{path:["auth","password"],generate:rK,secretField:"password"}]}},rZ=e=>Object.prototype.hasOwnProperty.call(rU,e);class rN extends n.WF{get _setting(){return rZ(this.sectionKey)?rU[this.sectionKey]:void 0}willUpdate(e){(e.has("yaml")||e.has("fromLine")||e.has("sectionKey"))&&(this._markerAbsent=!!this._setting&&!this._markerPresent())}_resolvedFields(){let e=this._setting;if(!e)return[];let t=t5(this._devices,this.configuration);return e.fields.map(i=>({field:i,key:i.secretField?(0,tg.WA)(e.secretSection,i.secretField,t,!0)[0]??"":""}))}get _ready(){let e=this._resolvedFields();return e.length>0&&e.every(e=>!e.field.secretField||""!==e.key)}_markerPresent(){let e=this._setting;if(!e)return!1;let t=this.yaml.split("\n"),i=r$(t,this.sectionKey.split(".")[0],this.fromLine);if(i<0)return!1;let o=RegExp(`^${e.marker}\\s*:`),a=null;for(let e=i+1;e<t.length;e++){let i=t[e];if(""===i.trim()||i.trimStart().startsWith("#"))continue;if(rd.QW.test(i))break;let r=(0,rB._j)(i);if(null===a&&(a=r),r<a)break;if(r===a&&o.test(i.trimStart()))return!0}return!1}render(){let e=this._setting;return e&&this._markerAbsent?(0,n.qy)`
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
    `:n.s6}_renderDialogBody(e){let[t,i=""]=this._localize(`device.${e.copyPrefix}_dialog_body`).split("{key}"),o=this._resolvedFields().filter(e=>e.field.secretField).map((e,t)=>(0,n.qy)`${t>0?", ":""}<code>${e.key}</code>`);return(0,n.qy)`${t}${o}${i}`}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.sectionKey="",this.yaml="",this.configuration="",this._markerAbsent=!1,this._generating=!1,this._onCta=()=>{this._ready&&this._dialog?.open()},this._onGenerate=async()=>{let e=this._setting,t=this._resolvedFields();if(!this._generating&&this._api&&e&&this._ready){this._generating=!0;try{let e=[];for(let{field:i,key:o}of t){let t=await i.generate();i.secretField?(await oM(this._api,o,t),e.push({path:i.path,value:`!secret ${o}`})):e.push({path:i.path,value:t})}rE(this,e),(0,d.VX)(this._localize("device.security_applied"))}catch(t){console.error("Security secret generation failed",t),(0,d.UG)(this._localize(`device.${e.copyPrefix}_error`))}finally{this._generating=!1}}}}}rN.styles=[b.G,rF,(0,n.AH)`
      .dialog-body code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
        padding: 1px 5px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
        word-break: break-all;
      }
    `],rj([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],rN.prototype,"_localize",void 0),rj([(0,a.Fg)({context:_.Ie,subscribe:!0}),(0,s.wk)()],rN.prototype,"_api",void 0),rj([(0,a.Fg)({context:_.xJ,subscribe:!0}),(0,s.wk)()],rN.prototype,"_devices",void 0),rj([(0,s.MZ)()],rN.prototype,"sectionKey",void 0),rj([(0,s.MZ)()],rN.prototype,"yaml",void 0),rj([(0,s.MZ)()],rN.prototype,"configuration",void 0),rj([(0,s.MZ)({type:Number})],rN.prototype,"fromLine",void 0),rj([(0,s.wk)()],rN.prototype,"_markerAbsent",void 0),rj([(0,s.wk)()],rN.prototype,"_generating",void 0),rj([(0,s.P)("esphome-confirm-dialog")],rN.prototype,"_dialog",void 0),rN=rj([(0,s.EM)("esphome-security-notice")],rN);let rV=(0,n.AH)`
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
`;function rH(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({plus:r.mdiPlus,pencil:r.mdiPencil,delete:r.mdiDelete});class rG extends n.WF{render(){if(0===this.rows.length&&void 0===this.addLabel)return n.s6;let e=""!==this.busyKey;return(0,n.qy)`<div class="list">
      <div class="header">
        <h4 class="title">${this.heading}</h4>
        ${void 0!==this.addLabel?(0,n.qy)`<button type="button" class="add" @click=${this._onAdd}>
                <wa-icon library="mdi" name="plus"></wa-icon>
                ${this.addLabel}
              </button>`:n.s6}
      </div>
      ${0===this.rows.length?void 0!==this.emptyText?(0,n.qy)`<p class="empty-message--dashed" role="status">${this.emptyText}</p>`:n.s6:(0,n.qy)`<ul class="rows">
              ${this.rows.map(t=>(0,n.qy)`<li class="row">
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
    </div>`}_emit(e,t){(0,Z.r)(this,e,{key:t})}constructor(...e){super(...e),this.heading="",this.rows=[],this.busyKey="",this.editLabel="",this.deleteLabel="",this._onAdd=()=>{(0,Z.r)(this,"add")}}}function rW(e){if("api"!==e.sectionKey)return n.s6;let t=(0,L.vB)(e.yaml).filter(e=>e.key.startsWith("automation:api_action:")).map(e=>({key:e.key,label:e.id??""}));return(0,n.qy)`<esphome-section-automation-list
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
  ></esphome-section-automation-list>`}function rY(e){var t,i;let o=e._shortcutTarget();if(null===o)return n.s6;let a=(t=(0,L.vB)(e.yaml),i=t=>{var i,o;let a;return i=e,a=(o=t).displayLabel||o.eventKey||"",o.eventKey?i._triggerCatalog.resolveName(o.parentKey??"esphome",o.eventKey,a):a},t.filter(e=>!!e.eventKey&&("device_on"===o.kind?"esphome"===e.parentKey:e.id===o.componentId||e.parentComponentId===o.componentId)).map(e=>({key:e.key,label:void 0!==e.parentComponentId?`${e.name??e.id} → ${i(e)}`:i(e)}))),r="device_on"===o.kind?e._localize("device.automations_list_title_device"):e._localize("device.automations_list_title");return(0,n.qy)`<esphome-section-automation-list
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
  ></esphome-section-automation-list>`}function rJ(e){return(0,n.qy)`<div class="yaml-only-notice" role="note">
    <wa-icon library="mdi" name="information-outline"></wa-icon>
    <div class="yaml-only-notice-body">${e}</div>
  </div>`}function rQ(e,t){return t?(0,n.qy)`<div class="actions">
    <button
      class="delete-button"
      ?disabled=${e._deleting}
      @click=${()=>e._confirmDialog?.open()}
    >
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${e._localize("device.delete_section")}
    </button>
  </div>`:n.s6}function rX(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}rG.styles=[b.G,ap.Z,U.U,rV],rH([(0,s.MZ)()],rG.prototype,"heading",void 0),rH([(0,s.MZ)({attribute:!1})],rG.prototype,"rows",void 0),rH([(0,s.MZ)({attribute:"add-label"})],rG.prototype,"addLabel",void 0),rH([(0,s.MZ)({attribute:"empty-text"})],rG.prototype,"emptyText",void 0),rH([(0,s.MZ)({attribute:"busy-key"})],rG.prototype,"busyKey",void 0),rH([(0,s.MZ)({attribute:"edit-label"})],rG.prototype,"editLabel",void 0),rH([(0,s.MZ)({attribute:"delete-label"})],rG.prototype,"deleteLabel",void 0),rG=rH([(0,s.EM)("esphome-section-automation-list")],rG),(0,M.C)({close:r.mdiClose});class r0 extends n.WF{open(){this._name="",this._error="",this._dialog.open=!0}render(){let e=this.boardName?this._localize("device.add_api_action_dialog_title",{name:this.boardName}):this._localize("device.add_api_action");return(0,n.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,en.Gc)(this._localize("device.api_action_header_description"))}
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
          @input=${e=>{this._name=(0,ac.e)(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,n.qy)`<p class="error" role="alert">${this._error}</p>`:n.s6}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._name&&!(0,L.vB)(this.yaml).some(e=>e.key===`automation:api_action:${this._name}`)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new eu.T(this),this._name="",this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"api_action",action_name:this._name},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{},actions:[]},e,this.yaml),i=eL(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:eF(e)},bubbles:!0,composed:!0})),this._dialog.open=!1}catch(t){let e=(0,ev.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}r0.styles=[b.G,ep.z9,eh,(0,n.AH)`
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
    `],rX([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],r0.prototype,"_localize",void 0),rX([(0,a.Fg)({context:_.Ie})],r0.prototype,"_api",void 0),rX([(0,s.MZ)()],r0.prototype,"boardName",void 0),rX([(0,s.MZ)()],r0.prototype,"configuration",void 0),rX([(0,s.MZ)()],r0.prototype,"yaml",void 0),rX([(0,s.MZ)({attribute:!1})],r0.prototype,"board",void 0),rX([(0,s.wk)()],r0.prototype,"_name",void 0),rX([(0,s.wk)()],r0.prototype,"_saving",void 0),rX([(0,s.wk)()],r0.prototype,"_error",void 0),r0=rX([(0,s.EM)("esphome-add-api-action-dialog")],r0);let r1=new Set(["api","script","interval","external_components","packages","substitutions","globals","dashboard_import"]);function r2(e,t,i){let o=(0,L.MT)(e),a=o.filter(e=>(0,L.gU)(e)===t);return 0===a.length?null:{sections:o,match:void 0!==i?a.find(e=>e.fromLine===i)??a[0]:a[0]}}function r6(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({"alert-circle-outline":r.mdiAlertCircleOutline,delete:r.mdiDelete,"information-outline":r.mdiInformationOutline,"open-in-new":r.mdiOpenInNew,pencil:r.mdiPencil,"plus-circle-outline":r.mdiPlusCircleOutline});let r3=new Set(["esphome"]);class r5 extends n.WF{get _showAdvanced(){return this._advancedShownSections.has(this.sectionKey)}_setShowAdvanced(e){let t=new Set(this._advancedShownSections);e?t.add(this.sectionKey):t.delete(this.sectionKey),this._advancedShownSections=t}willUpdate(e){e.has("backendErrors")&&this._clearedBackendPaths.size&&(this._clearedBackendPaths=new Set),(e.has("sectionKey")||e.has("configuration")||e.has("fromLine"))&&this.sectionKey&&this.configuration&&rM(this),this._revealAdvancedForFocus(e),this._revealAdvancedForErrors(e)}_revealAdvancedForErrors(e){(e.has("backendErrors")||e.has("_config"))&&this.backendErrors.fields.size&&rP(this,[...this.backendErrors.fields.keys()].map(e=>e.split(".")))}_revealAdvancedForFocus(e){(e.has("focusFieldPath")||e.has("_config"))&&this.focusFieldPath?.length&&rP(this,[this.focusFieldPath])}updated(){this._triggerCatalog.ensure(),function(e){if("api"!==e.sectionKey)return;let t=e.focusFieldPath?.[0];if("actions"!==t&&"services"!==t)return;let i=JSON.stringify(e.focusFieldPath);if(i===e._apiListFlashKey)return;let o=e.shadowRoot?.querySelector("esphome-section-automation-list");o&&(e._apiListFlashKey=i,id(o))}(this)}connectedCallback(){super.connectedCallback(),(0,Z.r)(this,"section-mount",{node:this})}disconnectedCallback(){super.disconnectedCallback(),this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null),(0,Z.r)(this,"section-unmount",{node:this})}flushPending(){null!==this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null,rS(this))}reload(){this.sectionKey&&this.configuration&&null===this._draftTimer&&this.yaml!==this._lastSelfWrittenYaml&&rM(this)}get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,(0,Z.r)(this,"dirty-change",{dirty:e}))}_scheduleDraftFlush(){this._draftTimer&&clearTimeout(this._draftTimer),this._draftTimer=setTimeout(()=>rS(this),r5.DRAFT_DEBOUNCE_MS)}_onShowYamlEditor(){(0,Z.r)(this,"show-yaml-editor")}_onAddPlatform(){(0,Z.r)(this,"request-add-component",{domain:this.sectionKey})}render(){var e,t;let i,o,a;if(this._loading)return(0,n.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`;if(this._error&&!this._config)return(0,n.qy)`<p class="error">${this._error}</p>`;if(!this._config)return n.s6;let r=this._config,s=(0,rr.a7)(this.sectionKey,r.entries),l=(e=this.sectionKey,t=s.length,rs.has(e)||0===t),d=[...this.yamlPaneVisible?[]:this.backendErrors.sectionMessages,...l?this.backendErrors.fieldMessages:[]],c=!r3.has(this.sectionKey);return(0,n.qy)`
      ${i=this._isUnknown||this._isPlatformDomain,o=this._isUnknown?this._localize("device.external_component_title"):this._isPlatformDomain?this._localize("device.platform_section_title"):r.title,(0,n.qy)`
    <div class="section-header">
      <div class="section-header-info">
        <div class="section-header-title-row">
          <h3 class="section-title">${o}</h3>
          ${(0,en.RQ)(r.docs_url)?(0,n.qy)`<a
                  class="docs-link"
                  href=${r.docs_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ${this._localize("device.docs")}
                  <wa-icon library="mdi" name="open-in-new"></wa-icon>
                </a>`:n.s6}
        </div>
        ${i?(0,n.qy)`<p class="section-subtitle">${this.sectionKey}</p>`:n.s6}
        ${r.description?(0,n.qy)`<p class="section-desc">${(0,en.Gc)(r.description)}</p>`:n.s6}
      </div>
      ${i?n.s6:(0,n.qy)`<div class="section-image">
              <img
                src=${r.image_url||(0,er.uG)()}
                alt=${r.title}
                referrerpolicy="no-referrer"
                @error=${er.jt}
              />
            </div>`}
    </div>
    ${d.length>0?(0,n.qy)`<div class="danger-banner section-error-banner" role="alert">
            <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
            <div class="danger-banner-text">
              ${d.map(e=>(0,n.qy)`<p>${e}</p>`)}
            </div>
          </div>`:n.s6}
  `}
      ${this._isPlatformDomain?(0,n.qy)`${rJ((0,n.qy)`
    <p>
      ${this._localize("device.platform_domain_section",{key:this.sectionKey})}
    </p>
    <button type="button" class="yaml-only-notice-cta" @click=${this._onAddPlatform}>
      ${this._localize("device.id_reference_add",{domain:this.sectionKey})}
    </button>
  `)}
  ${rQ(this,c)}`:l?(0,n.qy)`${rJ((0,n.qy)`
    <p>${this._localize("device.yaml_only_section")}</p>
    ${this.yamlPaneVisible?n.s6:(0,n.qy)`<button
            type="button"
            class="yaml-only-notice-cta"
            @click=${this._onShowYamlEditor}
          >
            ${this._localize("device.show_yaml_editor")}
          </button>`}
  `)}
  ${rW(this)} ${rY(this)}
  ${function(e){var t,i;let o=e._resolveComponentId();if(null===o)return n.s6;let a=(t=(0,L.vB)(e.yaml),i=t=>a5(t,e._localize),t.filter(e=>void 0!==e.actionField&&e.id===o).map(e=>({key:e.key,label:i(e.actionField)})));return(0,n.qy)`<esphome-section-automation-list
    .heading=${e._localize("device.action_fields_list_title")}
    .rows=${a}
    edit-label=${e._localize("device.action_fields_list_edit")}
    delete-label=${e._localize("device.action_fields_list_delete")}
    busy-key=${e._deletingRow}
    @edit=${e._onEditRow}
    @delete=${e._onDeleteRow}
  ></esphome-section-automation-list>`}(this)} ${rQ(this,c)}`:(a=(0,rr.a7)(this.sectionKey,r.entries),(0,n.qy)`
    ${rZ(this.sectionKey)?(0,n.qy)`<esphome-security-notice
            .sectionKey=${this.sectionKey}
            .yaml=${this.yaml}
            .configuration=${this.configuration}
            .fromLine=${this._resolvedFromLine}
            @apply-section-values=${this._onApplySectionValues}
          ></esphome-security-notice>`:n.s6}
    ${rT(this.sectionKey)?(0,n.qy)`<esphome-deprecation-notice
            .sectionKey=${this.sectionKey}
            .values=${this._values}
            .entries=${a}
            @apply-section-values=${this._onApplySectionValues}
          ></esphome-deprecation-notice>`:n.s6}
    <esphome-config-entry-form
      .entries=${a}
      .requiredGroups=${r.required_groups}
      .values=${this._values}
      .errors=${this._mergeErrors(this.backendErrors.fields,this._clearedBackendPaths,this._fieldErrors)}
      .board=${this.board}
      .yaml=${this.yaml}
      .fromLine=${this._resolvedFromLine}
      .sectionKey=${this.sectionKey}
      .configuration=${this.configuration}
      .focusFieldPath=${this.focusFieldPath}
      .presentComponents=${this._presentComponents}
      advanced-section
      gate-advanced
      ?show-advanced=${this._showAdvanced}
      @value-change=${this._onValueChange}
      @advanced-toggle=${this._onAdvancedToggle}
      @edit-action-field=${this._onEditActionField}
    ></esphome-config-entry-form>
    ${this._error?(0,n.qy)`<p class="error">${this._error}</p>`:n.s6}
    ${rW(this)} ${rY(this)}
    ${rQ(this,c)}
  `)}
      ${"api"!==this.sectionKey?n.s6:(0,n.qy)`<esphome-add-api-action-dialog
    .boardName=${this.boardName}
    .configuration=${this.configuration}
    .board=${this.board}
    .yaml=${this.yaml}
    @automation-added=${this._onApiActionAdded}
  ></esphome-add-api-action-dialog>`} ${null===this._shortcutTarget()?n.s6:(0,n.qy)`<esphome-add-automation-dialog
    .boardName=${this.boardName}
    .configuration=${this.configuration}
    .board=${this.board}
    .yaml=${this.yaml}
    @automation-added=${this._onAutomationAdded}
  ></esphome-add-automation-dialog>`}
      ${!c?n.s6:(0,n.qy)`<esphome-confirm-dialog
    heading=${this._localize("device.delete_section")}
    confirm-label=${this._localize("device.delete_section")}
    message=${this._localize("device.confirm_delete_section",{name:r.title})}
    destructive
    @confirm=${this._onDeleteConfirmed}
  ></esphome-confirm-dialog>`}
    `}_shortcutTarget(){return function(e,t,i,o){if(r1.has(t))return null;if("esphome"===t)return{kind:"device_on"};let a=r2(e,t,i);return null!==a&&o([a.match.parentKey??a.match.key,t])?{kind:"component_on",componentId:(0,L.MX)(a.sections,a.match)}:null}(this.yaml,this.sectionKey,this._resolvedFromLine,e=>this._triggerCatalog.hasTriggersFor(e))}_resolveComponentId(){var e;let t;return e=this.yaml,null===(t=r2(e,this.sectionKey,this._resolvedFromLine))?null:(0,L.MX)(t.sections,t.match)}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.sectionKey="",this.backendErrors=y.eV,this.yaml="",this.yamlPaneVisible=!0,this.board=null,this.boardName="",this._config=null,this._values={},this._loading=!1,this._dirty=!1,this._error="",this._deletingRow="",this._isUnknown=!1,this._isPlatformDomain=!1,this._fieldErrors=new Map,this._clearedBackendPaths=new Set,this._advancedShownSections=new Set,this._presentComponents=new Set,this._autoRevealedSections=new Set,this._deleting=!1,this._loadId=0,this._draftTimer=null,this._lastSelfWrittenYaml=null,this._triggerCatalog=new rn(this,()=>({api:this._api,platform:this.board?.esphome.platform||void 0,boardId:this.board?.id})),this._mergeErrors=(0,l.A)((e,t,i)=>{if(0===e.size)return i;let o=new Map;for(let[i,a]of e)t.has(i)||o.set(i,a);if(0===o.size)return i;for(let[e,t]of i)o.set(e,t);return o}),this._onAdvancedToggle=e=>{this._setShowAdvanced(e.detail.show)},this._onValueChange=e=>(function(e,t){let{path:i,value:o}=t.detail;e._values=(0,eC.Oe)(e._values,i,o),e._setDirty(!0);let a=i.join("."),r=(0,to.iL)(e._fieldErrors,a);r&&(e._fieldErrors=r);let n=`${a}.`,s=null;for(let t of e.backendErrors.fields.keys())(t===a||t.startsWith(n))&&!e._clearedBackendPaths.has(t)&&(s??=new Set(e._clearedBackendPaths)).add(t);s&&(e._clearedBackendPaths=s),e._scheduleDraftFlush()})(this,e),this._onDeleteConfirmed=()=>rA(this),this._onApplySectionValues=e=>(function(e,t){for(let{path:i,value:o}of t)e._values=(0,eC.Oe)(e._values,i,o);e._setDirty(!0),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),rS(e)})(this,e.detail.changes),this._onOpenAddApiAction=()=>{this._addApiActionDialog?.open()},this._onApiActionAdded=e=>{e.stopPropagation(),(0,Z.r)(this,"section-select",{sectionKey:e.detail.sectionKey})},this._onEditRow=e=>{e.stopPropagation(),(0,Z.r)(this,"section-select",{sectionKey:e.detail.key})},this._onDeleteRow=async e=>{e.stopPropagation();let t=e.detail.key,i=eO(t);if(this._api&&i&&!this._deletingRow){this._deletingRow=t;try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,i,this.yaml),t=eL(this.yaml,e);await this._api.updateConfig(this.configuration,t),(0,Z.r)(this,"yaml-updated",{yaml:t})}catch(t){let e=(0,ev.K)(t,this._localize,"device.automation_save_error");(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._deletingRow=""}}},this._onOpenAddAutomation=()=>{let e=this._shortcutTarget();null!==e&&("device_on"===e.kind?this._addAutomationDialog?.open({kind:"device_on"}):this._addAutomationDialog?.open({kind:"component_on",componentId:e.componentId}))},this._onAutomationAdded=e=>{e.stopPropagation(),(0,Z.r)(this,"section-select",{sectionKey:e.detail.sectionKey})},this._onEditActionField=e=>{e.stopPropagation();let t=this._resolveComponentId();if(null===t)return;let i=eF({kind:"component_action",component_id:t,field:e.detail.field});(0,Z.r)(this,"section-select",{sectionKey:i})}}}function r4(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}r5.DRAFT_DEBOUNCE_MS=200,r5.styles=[b.G,ep.z9,th,rl,tz],r6([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],r5.prototype,"_localize",void 0),r6([(0,a.Fg)({context:_.Ie})],r5.prototype,"_api",void 0),r6([(0,s.MZ)()],r5.prototype,"configuration",void 0),r6([(0,s.MZ)()],r5.prototype,"sectionKey",void 0),r6([(0,s.MZ)({type:Number})],r5.prototype,"fromLine",void 0),r6([(0,s.MZ)({attribute:!1})],r5.prototype,"focusFieldPath",void 0),r6([(0,s.MZ)({attribute:!1})],r5.prototype,"backendErrors",void 0),r6([(0,s.MZ)()],r5.prototype,"yaml",void 0),r6([(0,s.MZ)({attribute:!1})],r5.prototype,"yamlPaneVisible",void 0),r6([(0,s.MZ)({attribute:!1})],r5.prototype,"board",void 0),r6([(0,s.MZ)()],r5.prototype,"boardName",void 0),r6([(0,s.wk)()],r5.prototype,"_config",void 0),r6([(0,s.wk)()],r5.prototype,"_values",void 0),r6([(0,s.wk)()],r5.prototype,"_loading",void 0),r6([(0,s.wk)()],r5.prototype,"_dirty",void 0),r6([(0,s.wk)()],r5.prototype,"_error",void 0),r6([(0,s.wk)()],r5.prototype,"_deletingRow",void 0),r6([(0,s.wk)()],r5.prototype,"_isUnknown",void 0),r6([(0,s.wk)()],r5.prototype,"_isPlatformDomain",void 0),r6([(0,s.wk)()],r5.prototype,"_fieldErrors",void 0),r6([(0,s.wk)()],r5.prototype,"_clearedBackendPaths",void 0),r6([(0,s.wk)()],r5.prototype,"_advancedShownSections",void 0),r6([(0,s.wk)()],r5.prototype,"_presentComponents",void 0),r6([(0,s.wk)()],r5.prototype,"_resolvedFromLine",void 0),r6([(0,s.P)("esphome-confirm-dialog")],r5.prototype,"_confirmDialog",void 0),r6([(0,s.P)("esphome-add-api-action-dialog")],r5.prototype,"_addApiActionDialog",void 0),r6([(0,s.P)("esphome-add-automation-dialog")],r5.prototype,"_addAutomationDialog",void 0),r6([(0,s.wk)()],r5.prototype,"_deleting",void 0),r5=r6([(0,s.EM)("esphome-device-section-config")],r5),(0,M.C)({"open-in-new":r.mdiOpenInNew,"arrow-left":r.mdiArrowLeft,close:r.mdiClose,"party-popper":r.mdiPartyPopper,"plus-circle-outline":r.mdiPlusCircleOutline,usb:r.mdiUsb});class r8 extends n.WF{willUpdate(e){e.has("board")&&this._refreshAlternateBoards()}updated(e){if(e.has("yaml")&&this.selectedSection){var t,i;let o=()=>{this._sectionConfig?.reload(),this._automationEditor?.reload(),this._scriptEditor?.reload(),this._apiActionEditor?.reload()};(this._reloadTimer&&(clearTimeout(this._reloadTimer),this._reloadTimer=null),t=e.get("yaml"),i=this.yaml,t||!i)?this._reloadTimer=setTimeout(o,1e3):o()}}connectedCallback(){super.connectedCallback(),this.addEventListener("request-add-component",this._onRequestAddComponent)}disconnectedCallback(){super.disconnectedCallback(),this._reloadTimer&&clearTimeout(this._reloadTimer),this.removeEventListener("request-add-component",this._onRequestAddComponent)}async _refreshAlternateBoards(){let e=this.board;if(!e){this._alternatesForBoardId=null,this._alternateBoards=[];return}if(e.id!==this._alternatesForBoardId){this._alternatesForBoardId=e.id,this._alternateBoards=[];try{let t=await this._api.getCompatibleBoards(e.id);if(this._alternatesForBoardId!==e.id)return;this._alternateBoards=t.filter(t=>t.id!==e.id)}catch(t){console.error("Failed to load compatible boards:",t),this._alternatesForBoardId===e.id&&(this._alternatesForBoardId=null,this._alternateBoards=[])}}}render(){let e=this.board;return(0,n.qy)`
      ${!this.selectedSection&&e?(0,n.qy)`
              <div class="board-header">
                <div class="board-info">
                  <h3 class="board-name">${e.name}</h3>
                  <div class="board-tags">
                    ${e.tags.map(e=>(0,n.qy)`<wa-badge variant="brand" pill>${e}</wa-badge>`)}
                    <a
                      class="board-info-link"
                      href=${e.docs_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      ${this._localize("device.more_info")}
                      <wa-icon library="mdi" name="open-in-new"></wa-icon>
                    </a>
                    ${this._alternateBoards.length>0?(0,n.qy)`<button
                            type="button"
                            class="board-change-link"
                            @click=${this._openChangeBoard}
                          >
                            ${this._localize("device.change_board_link")}
                          </button>`:n.s6}
                  </div>
                  <p class="board-description">${(0,en.Gc)(e.description)}</p>
                </div>
                <div class="board-image">
                  <img
                    src=${(0,er.Ru)(e)}
                    alt=${e.name}
                    referrerpolicy="no-referrer"
                    @error=${er.jt}
                  />
                </div>
              </div>
              <div class="board-separator"></div>
            `:n.s6}
      ${this.selectedSection?this._renderSelectedSection():(0,n.qy)`
              ${this.justCreated?this._renderWelcomeBanner():n.s6}
              ${this._renderStepSection({title:this._localize("device.step_core"),desc:this._localize("device.step_core_desc"),icon:el,action:this._localize("device.show_core_configuration"),section:"core"})}
              ${this._renderStepSection({title:this._localize("device.step_components"),desc:this._localize("device.step_components_desc"),icon:ed,action:this._localize("device.show_components"),section:"components"})}
              ${this._renderStepSection({title:this._localize("device.step_automations"),desc:this._localize("device.step_automations_desc"),icon:ec,action:this._localize("device.show_automations"),section:"automations"})}
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
    `}_renderSelectedSection(){let e=this.selectedSection,t=e.startsWith("automation:")?this._locationForKey(e):null;return t?.kind==="script"?(0,n.qy)`<esphome-script-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-script-editor>`:t?.kind==="api_action"?(0,n.qy)`<esphome-api-action-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-api-action-editor>`:t?(0,n.qy)`<esphome-automation-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
        .focusYamlPath=${this.focusYamlPath}
      ></esphome-automation-editor>`:(0,n.qy)`<esphome-device-section-config
      .configuration=${this.configuration}
      .sectionKey=${e}
      .fromLine=${this.selectedFromLine}
      .focusFieldPath=${this.focusFieldPath}
      .backendErrors=${this.backendErrors}
      .yaml=${this.yaml}
      .board=${this.board}
      .boardName=${this.board?.name??""}
      .yamlPaneVisible=${this.yamlPaneVisible}
    ></esphome-device-section-config>`}_renderStepSection(e){return(0,n.qy)`
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
    `}_onShowNavSection(e){(0,Z.r)(this,"nav-section-show",{section:e})}_renderWelcomeBanner(){return this.board?(0,n.qy)`
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
    `:n.s6}_onDismissWelcome(){(0,Z.r)(this,"just-created-dismiss")}_onWelcomeInstall(){(0,Z.r)(this,"request-install")}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this._alternateBoards=[],this._alternatesForBoardId=null,this.yaml="",this.configuration="",this.justCreated=!1,this.yamlPaneVisible=!0,this.selectedSection=null,this.backendErrors=y.eV,this._reloadTimer=null,this._onRequestAddComponent=e=>{let t=e.detail;t?.domain&&(e.stopPropagation(),this._addComponentDialog?.openWithSearch(t.domain))},this._openChangeBoard=()=>{this._changeBoardDialog?.open()},this._onSelectBoard=e=>{e.stopPropagation(),(0,Z.r)(this,"change-board",e.detail)},this._locationForKey=(0,l.A)(eO)}}function r9(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}r8.styles=[b.G,es],r4([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],r8.prototype,"_localize",void 0),r4([(0,a.Fg)({context:_.Ie})],r8.prototype,"_api",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"board",void 0),r4([(0,s.wk)()],r8.prototype,"_alternateBoards",void 0),r4([(0,s.MZ)()],r8.prototype,"yaml",void 0),r4([(0,s.MZ)()],r8.prototype,"configuration",void 0),r4([(0,s.MZ)({type:Boolean})],r8.prototype,"justCreated",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"yamlPaneVisible",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"selectedSection",void 0),r4([(0,s.MZ)({type:Number})],r8.prototype,"selectedFromLine",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"focusFieldPath",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"focusYamlPath",void 0),r4([(0,s.MZ)({attribute:!1})],r8.prototype,"backendErrors",void 0),r4([(0,s.P)("esphome-device-section-config")],r8.prototype,"_sectionConfig",void 0),r4([(0,s.P)("esphome-automation-editor")],r8.prototype,"_automationEditor",void 0),r4([(0,s.P)("esphome-script-editor")],r8.prototype,"_scriptEditor",void 0),r4([(0,s.P)("esphome-api-action-editor")],r8.prototype,"_apiActionEditor",void 0),r4([(0,s.P)("esphome-add-component-dialog")],r8.prototype,"_addComponentDialog",void 0),r4([(0,s.P)("esphome-add-automation-dialog")],r8.prototype,"_addAutomationDialog",void 0),r4([(0,s.P)("esphome-add-config-dialog")],r8.prototype,"_addConfigDialog",void 0),r4([(0,s.P)("esphome-change-board-dialog")],r8.prototype,"_changeBoardDialog",void 0),r8=r4([(0,s.EM)("esphome-device-board-info")],r8),(0,M.C)({"alert-circle-outline":r.mdiAlertCircleOutline});class r7 extends n.WF{willUpdate(e){(e.has("errors")||e.has("caretLine")||e.has("editorFocused")||e.has("completionOpen"))&&this._evaluate()}disconnectedCallback(){super.disconnectedCallback(),this._cancelRevealTimer()}render(){return 0===this._visible.length?n.s6:(0,n.qy)`<div class="danger-banner invalid-banner" role="alert">
      <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
      <div class="danger-banner-text">
        ${this._visible.slice(0,6).map(e=>(0,n.qy)`<span
              >${(0,en.zA)(e.message)}${e.fix?(0,n.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto link-button"
                        title=${this._localize("yaml_editor.error_auto_fix_hint")}
                        @click=${()=>this._onAutoFix(e.fix)}
                      >
                        ${this._localize("yaml_editor.error_auto_fix")}
                      </button>
                    `:n.s6}${e.line?(0,n.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto link-button"
                        @click=${()=>this._onGotoLine(e.line)}
                      >
                        ${this._localize("yaml_editor.error_go_to_line",{line:e.line})}
                      </button>
                    `:n.s6}</span
            >`)}
        ${this._visible.length>6?(0,n.qy)`<span class="invalid-banner-more"
                >${this._localize("device.editor_invalid_more",{count:this._visible.length-6})}</span
              >`:n.s6}
      </div>
    </div>`}_onAutoFix(e){this.dispatchEvent(new CustomEvent("banner-auto-fix",{detail:{fix:e},bubbles:!0,composed:!0}))}_onGotoLine(e){this.dispatchEvent(new CustomEvent("banner-goto-line",{detail:{line:e},bubbles:!0,composed:!0}))}_evaluate(){if(0===this.errors.length){this._cancelRevealTimer(),this._visible.length&&(this._visible=[]);return}if(this._visible.length>0||this._shouldReveal()){this._cancelRevealTimer(),this._visible=this.errors;return}this.completionOpen?this._cancelRevealTimer():this._armRevealTimer()}_shouldReveal(){return!this.completionOpen&&(!!(!this.editorFocused||this.errors.some(e=>"parse"!==e.kind&&void 0===e.line)||this.errors.some(e=>void 0!==e.line&&Math.abs(e.line-this.caretLine)>3))||performance.now()-this.getLastEditAt()>=15e3)}_armRevealTimer(){this._cancelRevealTimer();let e=15e3-(performance.now()-this.getLastEditAt());this._revealTimer=setTimeout(()=>{this._revealTimer=void 0,this._evaluate()},Math.max(e,100))}_cancelRevealTimer(){void 0!==this._revealTimer&&(clearTimeout(this._revealTimer),this._revealTimer=void 0)}constructor(...e){super(...e),this._localize=e=>e,this.errors=[],this.caretLine=0,this.editorFocused=!1,this.completionOpen=!1,this.getLastEditAt=()=>-1/0,this._visible=[]}}function ne(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}r7.styles=[th,oL.R,(0,n.AH)`
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
    `],r9([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],r7.prototype,"_localize",void 0),r9([(0,s.MZ)({attribute:!1})],r7.prototype,"errors",void 0),r9([(0,s.MZ)({type:Number})],r7.prototype,"caretLine",void 0),r9([(0,s.MZ)({type:Boolean})],r7.prototype,"editorFocused",void 0),r9([(0,s.MZ)({type:Boolean})],r7.prototype,"completionOpen",void 0),r9([(0,s.MZ)({attribute:!1})],r7.prototype,"getLastEditAt",void 0),r9([(0,s.wk)()],r7.prototype,"_visible",void 0),r7=r9([(0,s.EM)("esphome-editor-invalid-banner")],r7),(0,M.C)({"chevron-down":r.mdiChevronDown,"content-save":r.mdiContentSave,eye:r.mdiEye,"eye-off":r.mdiEyeOff,"dock-left":r.mdiDockLeft,"dock-right":r.mdiDockRight,"view-split-vertical":r.mdiViewSplitVertical,upload:r.mdiUpload,"file-compare":r.mdiFileCompare});class nt extends n.WF{connectedCallback(){super.connectedCallback(),this._isMobile=this._mql.matches,this._mql.addEventListener("change",this._onMqlChange),window.addEventListener(f.ax,this._onTourReveal)}disconnectedCallback(){super.disconnectedCallback(),this._mql.removeEventListener("change",this._onMqlChange),window.removeEventListener(f.ax,this._onTourReveal)}render(){var e;let t,i,o=(0,z.wS)(this.layout,this._isMobile),a=!this._isMobile&&this.navCollapsed&&"right"===o,r=this._localize("device.editor_title_ready",{name:this.deviceTitle});return(0,n.qy)`
      <section class="card">
        <header class="card-header ${a?"card-header--compact":""}">
          <slot name="header-start"></slot>
          <div class="editor-header-main">
            <div class="editor-header-titlerow">
              <h2 class="editor-header-title truncate">${r}</h2>
              ${this.configuration&&!a?(0,n.qy)`<span class="editor-header-file truncate"
                      >${this.configuration}</span
                    >`:n.s6}
            </div>
          </div>
          ${e={localize:this._localize,effectiveLayout:o,revealSensitive:this._revealSensitive,showDiffButton:this._showDiffButton,showDiff:this._showDiff,yaml:this.yaml,savedYaml:this.savedYaml,onToggleRevealSensitive:()=>this._toggleRevealSensitive(),onToggleDiff:()=>this._toggleDiff(),onSetLayout:e=>this._setLayout(e)},(0,n.qy)`<div class="header-actions">
    ${"left"!==e.effectiveLayout?(t=e.localize(e.revealSensitive?"device.yaml_mask_sensitive":"device.yaml_reveal_sensitive"),(0,n.qy)`<button
              type="button"
              class="ghost-icon-btn diff-toggle"
              aria-pressed=${e.revealSensitive}
              aria-label=${t}
              @click=${e.onToggleRevealSensitive}
              title=${t}
            >
              <wa-icon
                library="mdi"
                name=${e.revealSensitive?"eye-off":"eye"}
              ></wa-icon>
            </button>`):n.s6}
    ${e.showDiffButton?(i=e.showDiff?e.localize("device.diff_view_editor"):e.localize("device.diff_view_diff"),(0,n.qy)`<button
              type="button"
              class="ghost-icon-btn diff-toggle"
              aria-pressed=${e.showDiff}
              ?disabled=${e.yaml===e.savedYaml&&!e.showDiff}
              aria-label=${i}
              @click=${e.onToggleDiff}
              title=${i}
            >
              <wa-icon library="mdi" name="file-compare"></wa-icon>
            </button>`):n.s6}
    <div
      class="layout-toggle"
      role="group"
      aria-label=${e.localize("device.editor_layout_label")}
      ${(0,f.Wf)("layout-toggle")}
    >
      <button
        type="button"
        class="ghost-icon-btn"
        aria-pressed=${"left"===e.effectiveLayout}
        @click=${()=>e.onSetLayout("left")}
        aria-label=${e.localize("device.layout_components_only")}
        title=${e.localize("device.layout_components_only")}
      >
        <wa-icon library="mdi" name="dock-left"></wa-icon>
      </button>
      <button
        class="ghost-icon-btn split-btn"
        type="button"
        aria-pressed=${"both"===e.effectiveLayout}
        @click=${()=>e.onSetLayout("both")}
        aria-label=${e.localize("device.layout_split")}
        title=${e.localize("device.layout_split")}
      >
        <wa-icon library="mdi" name="view-split-vertical"></wa-icon>
      </button>
      <button
        type="button"
        class="ghost-icon-btn"
        aria-pressed=${"right"===e.effectiveLayout}
        @click=${()=>e.onSetLayout("right")}
        aria-label=${e.localize("device.layout_yaml_only")}
        title=${e.localize("device.layout_yaml_only")}
      >
        <wa-icon library="mdi" name="dock-right"></wa-icon>
      </button>
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
              ${this.saving?(0,n.qy)`<wa-spinner></wa-spinner>`:(0,n.qy)`<wa-icon library="mdi" name="content-save"></wa-icon>`}
              ${this._localize("device.save")}
            </button>
          </div>
          <div
            class="editor-layout ${"both"===o?"editor-layout--both":"left"===o?"editor-layout--left":"editor-layout--right"} ${this._dragging?"dragging":""}"
            style=${"both"===o?`grid-template-columns: ${this._splitRatio}fr var(--pane-divider-width) ${1-this._splitRatio}fr`:""}
          >
            <div class="editor-pane editor-pane--left" ${(0,f.Wf)("central")}>
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
            ${"both"===o?(0,n.qy)`<div
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
                  ></div>`:n.s6}
            <div class="editor-pane editor-pane--right" ${(0,f.Wf)("yaml")}>
              <div class="editor-pane-body">
                ${this._showDiff?(0,n.qy)`<esphome-yaml-diff
                        .oldValue=${this.savedYaml}
                        .newValue=${this.yaml}
                      ></esphome-yaml-diff>`:(0,n.qy)`<esphome-yaml-editor
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
              ${!this._showDiff?(0,n.qy)`<esphome-editor-invalid-banner
                      .errors=${this._liveErrors}
                      .caretLine=${this._caretLine}
                      .editorFocused=${this._editorFocused}
                      .completionOpen=${this._completionOpen}
                      .getLastEditAt=${this._getLastEditAt}
                      @banner-auto-fix=${this._onBannerAutoFix}
                      @banner-goto-line=${this._onBannerGotoLine}
                    ></esphome-editor-invalid-banner>`:n.s6}
            </div>
          </div>
        </div>
        ${this._autoFixConfirmOpen?(0,n.qy)`<esphome-confirm-dialog
                class="auto-fix-confirm"
                heading=${this._localize("yaml_editor.auto_fix_confirm_heading")}
                message=${this._localize("yaml_editor.auto_fix_confirm_message")}
                confirm-label=${this._localize("yaml_editor.auto_fix_confirm_apply")}
              ></esphome-confirm-dialog>`:n.s6}
      </section>
    `}_onSave(){(0,Z.r)(this,"save-yaml")}_onValidate(){(0,Z.r)(this,"validate-device")}_toggleDiff(){this._showDiff=!this._showDiff}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_renderPrimaryAction(){var e={localize:this._localize,showUpdate:this.showUpdate,showModified:this.showModified,busy:this.busy,installedVersion:this.installedVersion,availableVersion:this.availableVersion,onUpdate:()=>this._onUpdate(),onInstall:()=>this._onInstall()};if(e.showUpdate)return(0,n.qy)`<div class="install-split">
      <button
        type="button"
        class="install-fab install-split__main"
        ${(0,f.Wf)("install")}
        @click=${e.onUpdate}
        title=${(0,Y.w3)(e.localize,e.busy,e.installedVersion,e.availableVersion,"dashboard.update")}
      >
        <wa-icon library="mdi" name="upload"></wa-icon>
        ${(0,Y.MV)(e.localize,e.busy,"dashboard.update")}
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
    </div>`;let t=(0,Y.MV)(e.localize,e.busy,"dashboard.install");return(0,n.qy)`<button
    type="button"
    class="install-fab ${e.showModified?"":"install-fab--muted"}"
    ${(0,f.Wf)("install")}
    @click=${e.onInstall}
    title=${t}
  >
    <wa-icon library="mdi" name="upload"></wa-icon>
    ${t}
  </button>`}_onInstall(){(0,Z.r)(this,"install-device")}_onUpdate(){(0,Z.r)(this,"update-device")}willUpdate(e){if(e.has("configuration")&&(this._liveErrors.length&&(this._liveErrors=[]),this._caretLine=0,this._lastEditAt=-1/0,this._editorFocused=!1,this._completionOpen=!1),this._showDiff&&e.has("_showDiffButton")&&!this._showDiffButton){this._showDiff=!1;return}this._showDiff&&e.has("savedYaml")&&this.yaml===this.savedYaml&&(this._showDiff=!1)}_onYamlDiagnostics(e){if(e.detail.configuration!==this.configuration)return;let t=e.detail.errors;t.length===this._liveErrors.length&&t.every((e,t)=>{let i=this._liveErrors[t];return e.message===i.message&&e.line===i.line&&e.kind===i.kind&&e.fix?.line===i.fix?.line&&e.fix?.indent===i.fix?.indent&&e.fix?.key===i.fix?.key})||(this._liveErrors=t)}_onYamlCursorLine(e){this._caretLine=e.detail.line}_onYamlCompletionOpen(e){this._completionOpen=e.detail.open}_onBannerAutoFix(e){this._autoFix(e.detail.fix)}_onBannerGotoLine(e){this._gotoErrorLine(e.detail.line)}_autoFix(e){let t=this._yamlEditor;if(!t){console.error("[auto-fix] no editor ref"),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed"));return}t.applyAutoFix(e,()=>this._confirmAutoFix()).then(e=>{"stale"===e?(0,d.KQ)(this._localize("yaml_editor.auto_fix_stale")):"unavailable"===e&&(console.error("[auto-fix] editor unavailable"),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed")))}).catch(e=>{console.error("[auto-fix] could not run:",e),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed"))})}async _confirmAutoFix(){if(this._autoFixConfirmOpen)return!1;this._autoFixConfirmOpen=!0,await this.updateComplete;let e=this._autoFixConfirmDialog;if(!e)throw this._autoFixConfirmOpen=!1,Error("auto-fix confirm dialog failed to mount");try{return await new Promise(t=>{let i=i=>{e.removeEventListener("confirm",o),e.removeEventListener("cancel",a),t(i)},o=()=>i(!0),a=()=>i(!1);e.addEventListener("confirm",o),e.addEventListener("cancel",a),e.open()})}finally{this._autoFixConfirmOpen=!1}}_gotoErrorLine(e){(0,Z.r)(this,"goto-line",{line:e})}_setLayout(e){(0,Z.r)(this,"layout-change",e)}_onShowYamlEditor(e){e.stopPropagation(),this._setLayout("both")}_onYamlChange(e){this._lastEditAt=performance.now(),(0,Z.r)(this,"yaml-change",e.detail)}constructor(...e){super(...e),this._localize=e=>e,this.yaml="",this.layout="both",this.navCollapsed=!1,this.deviceTitle="",this.board=null,this.justCreated=!1,this.webUiUrl="",this._isMobile=!1,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._saveShortcut=new N.k(this,()=>{this.hasUnsavedEdits&&this._onSave()}),this._onTourReveal=e=>{var t,i;let o,{id:a}=e.detail,r=(t=this.layout,i=this._isMobile,o=(0,z.wS)(t,i),"central"===a&&"right"===o?i?"left":"both":"yaml"===a&&"left"===o?i?"right":"both":null);r&&(0,Z.r)(this,g.um,r)},this.highlightRange=null,this.scrollToHighlight=!1,this.configuration="",this.selectedSection=null,this.backendErrors=y.eV,this.savedYaml="",this.hasUnsavedEdits=!1,this.saving=!1,this.showModified=!1,this.showUpdate=!1,this.installedVersion="",this.availableVersion="",this.busy=!1,this._showDiffButton=!1,this._showDiff=!1,this._revealSensitive=!1,this._liveErrors=[],this._caretLine=0,this._editorFocused=!1,this._completionOpen=!1,this._lastEditAt=-1/0,this._getLastEditAt=()=>this._lastEditAt,this._splitRatio=(()=>{try{let e=localStorage.getItem(V),t=null===e?NaN:Number.parseFloat(e);return Number.isFinite(t)?H(t):.5}catch{return .5}})(),this._dragging=!1,this._onEditorFocusIn=()=>{this._editorFocused=!0},this._onEditorFocusOut=e=>{let t=e.currentTarget;this._editorFocused=e.relatedTarget instanceof Node&&t.contains(e.relatedTarget)},this._autoFixConfirmOpen=!1,this._onDividerPointerDown=e=>{if(0!==e.button)return;let t=this._layoutEl;if(!t)return;e.preventDefault();let i=t.getBoundingClientRect();this._dragging=!0;let o=e.currentTarget;o.setPointerCapture(e.pointerId);let a=o.getBoundingClientRect().width,r=i.width-a,n=e=>{r<=0||(this._splitRatio=H((e.clientX-i.left-a/2)/r))},s=()=>{this._dragging=!1,G(this._splitRatio),o.removeEventListener("pointermove",n),o.removeEventListener("pointerup",s),o.removeEventListener("pointercancel",s),o.removeEventListener("lostpointercapture",s)};o.addEventListener("pointermove",n),o.addEventListener("pointerup",s),o.addEventListener("pointercancel",s),o.addEventListener("lostpointercapture",s)},this._onDividerKeydown=e=>{let t=((e,t)=>{let i;if("ArrowLeft"===t)i=e-.02;else if("ArrowRight"===t)i=e+.02;else if("Home"===t)i=.25;else{if("End"!==t)return null;i=.75}return H(i)})(this._splitRatio,e.key);null!==t&&(e.preventDefault(),this._splitRatio=t,G(this._splitRatio))}}}nt.styles=[b.G,U.U,W],ne([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],nt.prototype,"_localize",void 0),ne([(0,s.MZ)()],nt.prototype,"yaml",void 0),ne([(0,s.MZ)()],nt.prototype,"layout",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"navCollapsed",void 0),ne([(0,s.MZ)()],nt.prototype,"deviceTitle",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"board",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"justCreated",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"webUiUrl",void 0),ne([(0,s.wk)()],nt.prototype,"_isMobile",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"highlightRange",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"scrollToHighlight",void 0),ne([(0,s.MZ)()],nt.prototype,"configuration",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"selectedSection",void 0),ne([(0,s.MZ)({type:Number})],nt.prototype,"selectedFromLine",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"focusFieldPath",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"focusYamlPath",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"backendErrors",void 0),ne([(0,s.MZ)({attribute:!1})],nt.prototype,"savedYaml",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"hasUnsavedEdits",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"saving",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"showModified",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"showUpdate",void 0),ne([(0,s.MZ)()],nt.prototype,"installedVersion",void 0),ne([(0,s.MZ)()],nt.prototype,"availableVersion",void 0),ne([(0,s.MZ)({type:Boolean})],nt.prototype,"busy",void 0),ne([(0,a.Fg)({context:_.Pt,subscribe:!0}),(0,s.wk)()],nt.prototype,"_showDiffButton",void 0),ne([(0,s.wk)()],nt.prototype,"_showDiff",void 0),ne([(0,s.wk)()],nt.prototype,"_revealSensitive",void 0),ne([(0,s.wk)()],nt.prototype,"_liveErrors",void 0),ne([(0,s.wk)()],nt.prototype,"_caretLine",void 0),ne([(0,s.wk)()],nt.prototype,"_editorFocused",void 0),ne([(0,s.wk)()],nt.prototype,"_completionOpen",void 0),ne([(0,s.wk)()],nt.prototype,"_splitRatio",void 0),ne([(0,s.wk)()],nt.prototype,"_dragging",void 0),ne([(0,s.P)(".editor-layout")],nt.prototype,"_layoutEl",void 0),ne([(0,s.P)("esphome-yaml-editor")],nt.prototype,"_yamlEditor",void 0),ne([(0,s.P)("esphome-confirm-dialog.auto-fix-confirm")],nt.prototype,"_autoFixConfirmDialog",void 0),ne([(0,s.wk)()],nt.prototype,"_autoFixConfirmOpen",void 0),nt=ne([(0,s.EM)("esphome-device-editor")],nt);class ni{get tick(){return this._tick}hostConnected(){this._unsubscribes=this._subscribes.map(e=>e(()=>{this._tick++,this._host.requestUpdate()}))}hostDisconnected(){for(let e of this._unsubscribes)e();this._unsubscribes=[]}constructor(e,t){this._host=e,this._subscribes=t,this._tick=0,this._unsubscribes=[],e.addController(this)}}let no=(0,n.AH)`
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
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-s) var(--wa-space-s) var(--wa-space-s) var(--wa-space-m);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    flex-shrink: 0;
  }

  .card-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    /* Match the editor header title's line-height so both header bars are the
       same height (their dividers line up) and the title baselines align.
       line-height 1 clipped the descender 'g' (#827) and left this header about
       0.4px shorter than the editor's, offsetting the divider by a pixel. */
    line-height: var(--wa-line-height-normal);
    min-width: 0;
  }

  .header-actions {
    display: inline-flex;
    align-items: center;
    gap: 0;
  }

  /* Box + hover come from .ghost-icon-btn (shared.ts). Both buttons swap
     the shared padding for a fixed width/height and add a hover
     transition; the icon size is per-site. */
  .collapse-btn,
  .search-btn {
    width: 30px;
    height: 22px;
    padding: 0;
    border-radius: var(--wa-border-radius-m);
    transition: background 0.12s;
  }

  /* Active search toggle gets a subtle tint, not the ghost-icon-btn filled
     state; reset the color too so the icon stays primary, not on-primary. */
  .search-btn[aria-pressed="true"] {
    background: color-mix(in srgb, var(--esphome-primary), transparent 88%);
    color: var(--esphome-primary);
  }

  .collapse-btn wa-icon,
  .search-btn wa-icon {
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

  .nav-subgroup-count,
  .nav-item-error-badge {
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
  }

  .nav-item-subtitle {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-weight: normal;
    margin: 0;
    line-height: 1.2;
  }

  /* Error-count pill on a row (or a collapsed subgroup header) whose
     section carries backend validation errors. Shares the count pill's
     geometry above; only the color treatment differs. */
  .nav-item-error-badge {
    margin-left: auto;
    font-weight: var(--wa-font-weight-semibold);
    color: var(--esphome-error);
    background: color-mix(in srgb, var(--esphome-error), transparent 88%);
    flex-shrink: 0;
  }

  .nav-subgroup-header .nav-item-error-badge {
    margin-left: 0;
  }

  .nav-item-chevron {
    margin-left: auto;
    font-size: var(--wa-font-size-l);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  /* The chevron yields the right edge when an error badge holds it. */
  .nav-item-error-badge ~ .nav-item-chevron {
    margin-left: 0;
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
`;function na(e){let{core:t,components:i,automations:o}=(0,L.uU)((0,L.MT)(e)),a=(0,L.vB)(e);return{core:t,components:i,automations:[...o.filter(e=>"script"!==e.key&&"interval"!==e.key),...a].filter(e=>!e.key.startsWith("automation:light_effect:")&&!e.key.startsWith("automation:unscoped:")).sort((e,t)=>e.fromLine-t.fromLine),substitutions:(0,t_.Gr)(e)}}function nr(e){let t=[],i=new Map;for(let o of e){let e=o.item.key,a=i.get(e);a||(a=[],i.set(e,a),t.push(e)),a.push(o)}return t.map(e=>({key:e,rows:i.get(e)}))}function nn(e,t,i){let o=(0,L.gU)(e);if("automation"===t)return function(e,t,i){if("script"===e.parentKey){let o=i.localize("device.script_header_title_static"),a=(0,t_.rq)(e.id??t,i.substitutions);return{primary:o,secondary:a!==o?a:void 0}}if("interval"===e.parentKey){let t=i.localize("device.automation_interval_label"),o=e.meta?.every;return{primary:t,secondary:o?i.localize("device.automation_interval_every_n",{time:o}):void 0}}if("esphome"===e.parentKey&&e.eventKey)return{primary:nd(i.triggerCatalog.resolveName("esphome",e.eventKey,nl(e.eventKey)))};if(e.parentKey&&e.eventKey){let t=nd(i.triggerCatalog.resolveName(e.parentKey,e.eventKey,nl(e.eventKey)));return{primary:t,secondary:ns(e,i,t)}}if(e.parentKey&&e.actionField){let t=a5(e.actionField,i.localize);return{primary:t,secondary:ns(e,i,t)}}return{primary:e.displayLabel||t}}(e,o,i);let a=o,r=(0,e5.CQ)(o,i.platform||void 0);r?.name&&(a=r.name),"core"===t&&(a=ef(a));let n="core"===t&&"esphome"===e.key&&i.deviceName?i.deviceName:(0,t_.rq)(e.name||e.id||"",i.substitutions)||void 0,s=n&&n!==a?n:void 0;return{primary:a,secondary:s}}function ns(e,t,i){let o=e.name||e.id,a=o?(0,t_.rq)(o,t.substitutions):nc(e.parentKey??"");return a!==i?a:void 0}function nl(e){return e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}function nd(e){let t=e.lastIndexOf(" → ");return t>=0?e.slice(t+3):e}function nc(e){let t=e.replace(/_/g," ");return t.charAt(0).toUpperCase()+t.slice(1)}let nh={esphome:["chip",r.mdiChip],wifi:["wifi",r.mdiWifi],ethernet:["ethernet",r.mdiEthernet],mdns:["radio-tower",r.mdiRadioTower],network:["lan",r.mdiLan],api:["api",r.mdiApi],ota:["cloud-upload-outline",r.mdiCloudUploadOutline],dashboard_import:["cloud-upload-outline",r.mdiCloudUploadOutline],logger:["card-text-outline",r.mdiCardTextOutline],syslog:["card-text-outline",r.mdiCardTextOutline],web_server:["web",r.mdiWeb],http_request:["web",r.mdiWeb],captive_portal:["wifi-lock",r.mdiWifiLock],improv_serial:["wifi-cog",r.mdiWifiCog],esp32_improv:["wifi-cog",r.mdiWifiCog],mqtt:["swap-horizontal",r.mdiSwapHorizontal],wireguard:["vpn",r.mdiVpn],socket:["connection",r.mdiConnection],udp:["connection",r.mdiConnection],async_tcp:["connection",r.mdiConnection],espnow:["connection",r.mdiConnection],serial_proxy:["connection",r.mdiConnection],sim800l:["connection",r.mdiConnection],prometheus:["chart-line",r.mdiChartLine],statsd:["chart-line",r.mdiChartLine],runtime_stats:["chart-line",r.mdiChartLine],time:["clock-outline",r.mdiClockOutline],sntp:["clock-outline",r.mdiClockOutline],interval:["clock-outline",r.mdiClockOutline],script:["script-text-outline",r.mdiScriptTextOutline],uart:["serial-port",r.mdiSerialPort],i2c:["connection",r.mdiConnection],spi:["connection",r.mdiConnection],modbus:["connection",r.mdiConnection],modbus_controller:["connection",r.mdiConnection],modbus_server:["connection",r.mdiConnection],esp32:["cpu-32-bit",r.mdiCpu32Bit],esp8266:["cpu-32-bit",r.mdiCpu32Bit],rp2040:["cpu-32-bit",r.mdiCpu32Bit],rp2:["cpu-32-bit",r.mdiCpu32Bit],bk72xx:["cpu-32-bit",r.mdiCpu32Bit],rtl87xx:["cpu-32-bit",r.mdiCpu32Bit],ln882x:["cpu-32-bit",r.mdiCpu32Bit],libretiny:["cpu-32-bit",r.mdiCpu32Bit],nrf52:["cpu-32-bit",r.mdiCpu32Bit],host:["chip",r.mdiChip],esp32_hosted:["wifi",r.mdiWifi],esp32_ble:["bluetooth",r.mdiBluetooth],esp32_ble_tracker:["bluetooth",r.mdiBluetooth],ble:["bluetooth",r.mdiBluetooth],bluetooth_proxy:["bluetooth",r.mdiBluetooth],ble_client:["bluetooth",r.mdiBluetooth],ble_nus:["bluetooth",r.mdiBluetooth],esp32_ble_beacon:["bluetooth",r.mdiBluetooth],esp32_ble_server:["bluetooth",r.mdiBluetooth],zephyr_ble_server:["bluetooth",r.mdiBluetooth],rp2040_ble:["bluetooth",r.mdiBluetooth],exposure_notifications:["bluetooth",r.mdiBluetooth],airthings_ble:["bluetooth",r.mdiBluetooth],bedjet:["bluetooth",r.mdiBluetooth],mopeka_ble:["bluetooth",r.mdiBluetooth],radon_eye_ble:["bluetooth",r.mdiBluetooth],ruuvi_ble:["bluetooth",r.mdiBluetooth],xiaomi_ble:["bluetooth",r.mdiBluetooth],xiaomi_rtcgq02lm:["bluetooth",r.mdiBluetooth],zwave_proxy:["z-wave",r.mdiZWave],zigbee:["zigbee",r.mdiZigbee],openthread:["zigbee",r.mdiZigbee],usb_host:["usb",r.mdiUsb],usb_uart:["usb",r.mdiUsb],usb_cdc_acm:["usb",r.mdiUsb],tinyusb:["usb",r.mdiUsb],psram:["memory",r.mdiMemory],preferences:["content-save-cog-outline",r.mdiContentSaveCogOutline],power_supply:["power-plug",r.mdiPowerPlug],esp_ldo:["power-plug",r.mdiPowerPlug],sy6970:["power-plug",r.mdiPowerPlug],deep_sleep:["power-sleep",r.mdiPowerSleep],status_led:["led-on",r.mdiLedOn],safe_mode:["restart-alert",r.mdiRestartAlert],factory_reset:["restart-alert",r.mdiRestartAlert],debug:["bug",r.mdiBug],globals:["variable",r.mdiVariable],substitutions:["code-braces",r.mdiCodeBraces],packages:["package-variant-closed",r.mdiPackageVariantClosed],external_components:["puzzle-outline",r.mdiPuzzleOutline],mapping:["cog",r.mdiCog],json:["code-json",r.mdiCodeJson],bytebuffer:["code-array",r.mdiCodeArray],split_buffer:["code-array",r.mdiCodeArray],sha256:["pound-box-outline",r.mdiPoundBoxOutline],hmac_md5:["pound-box-outline",r.mdiPoundBoxOutline],hmac_sha256:["pound-box-outline",r.mdiPoundBoxOutline],remote_receiver:["remote",r.mdiRemote],remote_transmitter:["remote",r.mdiRemote],cc1101:["remote",r.mdiRemote],sx126x:["remote",r.mdiRemote],sx127x:["remote",r.mdiRemote],lightwaverf:["remote",r.mdiRemote],rf_bridge:["remote",r.mdiRemote],pn532:["nfc-variant",r.mdiNfcVariant],pn532_i2c:["nfc-variant",r.mdiNfcVariant],pn532_spi:["nfc-variant",r.mdiNfcVariant],pn7150_i2c:["nfc-variant",r.mdiNfcVariant],pn7160_i2c:["nfc-variant",r.mdiNfcVariant],pn7160_spi:["nfc-variant",r.mdiNfcVariant],rc522_i2c:["nfc-variant",r.mdiNfcVariant],rc522_spi:["nfc-variant",r.mdiNfcVariant],rdm6300:["nfc-variant",r.mdiNfcVariant],ld2410:["motion-sensor",r.mdiMotionSensor],ld2412:["motion-sensor",r.mdiMotionSensor],ld2420:["motion-sensor",r.mdiMotionSensor],ld2450:["motion-sensor",r.mdiMotionSensor],rd03d:["motion-sensor",r.mdiMotionSensor],at581x:["motion-sensor",r.mdiMotionSensor],dfrobot_sen0395:["motion-sensor",r.mdiMotionSensor],hlk_fm22x:["motion-sensor",r.mdiMotionSensor],seeed_mr24hpc1:["motion-sensor",r.mdiMotionSensor],seeed_mr60bha2:["motion-sensor",r.mdiMotionSensor],seeed_mr60fda2:["motion-sensor",r.mdiMotionSensor],esp32_touch:["gesture-tap-button",r.mdiGestureTapButton],cap1188:["gesture-tap-button",r.mdiGestureTapButton],mpr121:["gesture-tap-button",r.mdiGestureTapButton],ttp229_bsf:["gesture-tap-button",r.mdiGestureTapButton],ttp229_lsf:["gesture-tap-button",r.mdiGestureTapButton],matrix_keypad:["dialpad",r.mdiDialpad],wiegand:["dialpad",r.mdiDialpad],key_collector:["dialpad",r.mdiDialpad],fingerprint_grow:["fingerprint",r.mdiFingerprint],i2s_audio:["volume-high",r.mdiVolumeHigh],audio:["volume-high",r.mdiVolumeHigh],audio_file:["volume-high",r.mdiVolumeHigh],microphone:["microphone",r.mdiMicrophone],micro_wake_word:["microphone",r.mdiMicrophone],voice_assistant:["microphone-message",r.mdiMicrophoneMessage],speaker:["speaker",r.mdiSpeaker],dfplayer:["speaker",r.mdiSpeaker],rtttl:["speaker",r.mdiSpeaker],adalight:["lightbulb-outline",r.mdiLightbulbOutline],wled:["lightbulb-outline",r.mdiLightbulbOutline],e131:["lightbulb-outline",r.mdiLightbulbOutline],my9231:["lightbulb-outline",r.mdiLightbulbOutline],sm16716:["lightbulb-outline",r.mdiLightbulbOutline],sm2135:["lightbulb-outline",r.mdiLightbulbOutline],sm2235:["lightbulb-outline",r.mdiLightbulbOutline],sm2335:["lightbulb-outline",r.mdiLightbulbOutline],bp1658cj:["lightbulb-outline",r.mdiLightbulbOutline],bp5758d:["lightbulb-outline",r.mdiLightbulbOutline],tlc59208f:["lightbulb-outline",r.mdiLightbulbOutline],tlc5947:["lightbulb-outline",r.mdiLightbulbOutline],tlc5971:["lightbulb-outline",r.mdiLightbulbOutline],tm1651:["lightbulb-outline",r.mdiLightbulbOutline],adc128s102:["gauge",r.mdiGauge],ads1115:["gauge",r.mdiGauge],ads1118:["gauge",r.mdiGauge],mcp3008:["gauge",r.mdiGauge],mcp3204:["gauge",r.mdiGauge],as5600:["gauge",r.mdiGauge],dac7678:["export-variant",r.mdiExportVariant],gp8403:["export-variant",r.mdiExportVariant],mcp4728:["export-variant",r.mdiExportVariant],mcp4461:["export-variant",r.mdiExportVariant],pca9685:["export-variant",r.mdiExportVariant],servo:["export-variant",r.mdiExportVariant],grove_tb6612fng:["export-variant",r.mdiExportVariant],mcp23008:["connection",r.mdiConnection],mcp23016:["connection",r.mdiConnection],mcp23017:["connection",r.mdiConnection],mcp23s08:["connection",r.mdiConnection],mcp23s17:["connection",r.mdiConnection],pca6416a:["connection",r.mdiConnection],pca9554:["connection",r.mdiConnection],pcf8574:["connection",r.mdiConnection],pi4ioe5v6408:["connection",r.mdiConnection],xl9535:["connection",r.mdiConnection],max6956:["connection",r.mdiConnection],sn74hc165:["connection",r.mdiConnection],sn74hc595:["connection",r.mdiConnection],cd74hc4067:["connection",r.mdiConnection],tca9548a:["connection",r.mdiConnection],tca9555:["connection",r.mdiConnection],ch422g:["connection",r.mdiConnection],ch423:["connection",r.mdiConnection],sx1509:["connection",r.mdiConnection],m5stack_8angle:["connection",r.mdiConnection],i2c_device:["connection",r.mdiConnection],spi_device:["connection",r.mdiConnection],vbus:["connection",r.mdiConnection],tuya:["connection",r.mdiConnection],wk2132_i2c:["serial-port",r.mdiSerialPort],wk2132_spi:["serial-port",r.mdiSerialPort],wk2168_i2c:["serial-port",r.mdiSerialPort],wk2168_spi:["serial-port",r.mdiSerialPort],wk2204_i2c:["serial-port",r.mdiSerialPort],wk2204_spi:["serial-port",r.mdiSerialPort],wk2212_i2c:["serial-port",r.mdiSerialPort],wk2212_spi:["serial-port",r.mdiSerialPort],apds9960:["gauge",r.mdiGauge],as3935_i2c:["gauge",r.mdiGauge],as3935_spi:["gauge",r.mdiGauge],bme680_bsec:["gauge",r.mdiGauge],bme68x_bsec2_i2c:["gauge",r.mdiGauge],gdk101:["gauge",r.mdiGauge],msa3xx:["gauge",r.mdiGauge],ezo_pmp:["gauge",r.mdiGauge],daly_bms:["gauge",r.mdiGauge],pylontech:["gauge",r.mdiGauge],pipsolar:["gauge",r.mdiGauge],sun_gtil2:["gauge",r.mdiGauge],sml:["gauge",r.mdiGauge],dsmr:["gauge",r.mdiGauge],teleinfo:["gauge",r.mdiGauge],dlms_meter:["gauge",r.mdiGauge],emontx:["gauge",r.mdiGauge],emc2101:["fan",r.mdiFan],gps:["crosshairs-gps",r.mdiCrosshairsGps],sun:["weather-sunny",r.mdiWeatherSunny],opentherm:["thermostat",r.mdiThermostat],uponor_smatrix:["thermostat",r.mdiThermostat],micronova:["thermostat",r.mdiThermostat],sprinkler:["sprinkler-variant",r.mdiSprinklerVariant],sensor:["gauge",r.mdiGauge],binary_sensor:["checkbox-marked-circle-outline",r.mdiCheckboxMarkedCircleOutline],text_sensor:["text-box-outline",r.mdiTextBoxOutline],switch:["toggle-switch-outline",r.mdiToggleSwitchOutline],light:["lightbulb-outline",r.mdiLightbulbOutline],output:["export-variant",r.mdiExportVariant],number:["numeric",r.mdiNumeric],select:["form-dropdown",r.mdiFormDropdown],button:["gesture-tap-button",r.mdiGestureTapButton],fan:["fan",r.mdiFan],cover:["window-shutter",r.mdiWindowShutter],climate:["thermostat",r.mdiThermostat],text:["form-textbox",r.mdiFormTextbox],lock:["lock-outline",r.mdiLockOutline],valve:["valve",r.mdiValve],media_player:["speaker",r.mdiSpeaker],display:["monitor",r.mdiMonitor],lvgl:["monitor",r.mdiMonitor],graphical_display_menu:["monitor",r.mdiMonitor],lcd_menu:["monitor",r.mdiMonitor],datetime:["calendar-clock",r.mdiCalendarClock],camera:["camera-outline",r.mdiCameraOutline],esp32_camera:["camera-outline",r.mdiCameraOutline],esp32_camera_web_server:["camera-outline",r.mdiCameraOutline],camera_encoder:["camera-outline",r.mdiCameraOutline],event:["bell-outline",r.mdiBellOutline],alarm_control_panel:["shield-home-outline",r.mdiShieldHomeOutline],graph:["chart-line",r.mdiChartLine],color:["palette",r.mdiPalette],qr_code:["qrcode",r.mdiQrcode],font:["format-font",r.mdiFormatFont],image:["image-outline",r.mdiImageOutline],online_image:["image-sync-outline",r.mdiImageSyncOutline],animation:["image-multiple-outline",r.mdiImageMultipleOutline]},np=["shape-outline",r.mdiShapeOutline];function nu(e,t,i){var o;let{item:a,labels:r}=e,{primary:s,secondary:l}=r,d=a.parentKey??a.key,c=t.errorCount?.(a)??0;return(0,n.qy)`
    <div
      class="nav-item ${t.selectedLine===a.fromLine?"nav-item--selected":""} ${t.hoveredLine===a.fromLine?"nav-item--hovered":""}"
      ${(0,f.Wf)("esphome"===a.key&&t.tourAnchorId?`${t.tourAnchorId}-item`:void 0)}
      @mouseenter=${()=>t.onItemEnter(a)}
      @mouseleave=${()=>t.onItemLeave()}
      @click=${()=>t.onItemClick(a)}
    >
      ${i?"esphome"===(o=d)?(0,n.qy)`<wa-icon
      class="nav-item-icon"
      src=${(0,w.cV)("/assets/logo/esphome-mono.svg")}
      title="ESPHome"
    ></wa-icon>`:(0,n.qy)`<wa-icon
    class="nav-item-icon"
    library="mdi"
    name=${(nh[o]??np)[0]}
    title=${nc(o)}
  ></wa-icon>`:n.s6}
      <div class="nav-item-content">
        <p class="truncate">${s}</p>
        ${l?(0,n.qy)`<span class="nav-item-subtitle truncate">${l}</span>`:n.s6}
      </div>
      ${c>0?nm(c,t):n.s6}
      <wa-icon class="nav-item-chevron" library="mdi" name="chevron-right"></wa-icon>
    </div>
  `}function nm(e,t){return(0,n.qy)`<span
    class="nav-item-error-badge"
    role="img"
    aria-label=${t.errorLabel(e)}
    >${e}</span
  >`}function nv(e){("Enter"===e.key||" "===e.key)&&(e.preventDefault(),e.currentTarget.click())}(0,M.C)(Object.fromEntries([...Object.values(nh),np]));class ng{hostUpdated(){let{selectedLine:e,buckets:t,openSections:i,filtering:o}=this._read();if(null===e){this._scrolledLine=null,this._revealedLine=null;return}if(null!==this._revealedLine&&this._revealedLine!==e&&(this._revealedLine=null),e===this._scrolledLine)return;let a=t.core.some(t=>t.fromLine===e)?0:t.components.some(t=>t.fromLine===e)?1:t.automations.some(t=>t.fromLine===e)?2:-1;if(-1===a){this._scrolledLine=e;return}if(!o&&!i.has(a)&&this._revealedLine!==e){this._revealedLine=e,this._host.dispatchEvent(new CustomEvent("section-reveal",{detail:{index:a},bubbles:!0,composed:!0}));return}this._revealedLine=e;let r=this._host.renderRoot.querySelector(".nav-item--selected");r&&r.getClientRects().length>0&&(r.scrollIntoView({block:"nearest"}),this._scrolledLine=e)}constructor(e,t){this._host=e,this._read=t,this._scrolledLine=null,this._revealedLine=null,e.addController(this)}}function nf(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({close:r.mdiClose});class n_ extends n.WF{open(){this._id="",this._error="",this._dialog.open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml)}catch(e){this._error=(0,em.u)(e)}}render(){let e=this.boardName?this._localize("device.add_script_dialog_title",{name:this.boardName}):this._localize("device.add_script");return(0,n.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,en.Gc)(this._localize("device.script_header_description"))}
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
          @input=${e=>{this._id=(0,ac.e)(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,n.qy)`<p class="error" role="alert">${this._error}</p>`:n.s6}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._id&&!this._available?.scripts.some(e=>e.id===this._id)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new eu.T(this),this._id="",this._available=null,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"script",id:this._id},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{mode:"single"},actions:[]},e,this.yaml);eR(this,this.yaml,e,t),this._dialog.open=!1}catch(t){let e=(0,ev.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}n_.styles=[b.G,ep.z9,eh,(0,n.AH)`
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
    `],nf([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],n_.prototype,"_localize",void 0),nf([(0,a.Fg)({context:_.Ie})],n_.prototype,"_api",void 0),nf([(0,s.MZ)()],n_.prototype,"boardName",void 0),nf([(0,s.MZ)()],n_.prototype,"configuration",void 0),nf([(0,s.MZ)()],n_.prototype,"yaml",void 0),nf([(0,s.MZ)({attribute:!1})],n_.prototype,"board",void 0),nf([(0,s.wk)()],n_.prototype,"_id",void 0),nf([(0,s.wk)()],n_.prototype,"_available",void 0),nf([(0,s.wk)()],n_.prototype,"_saving",void 0),nf([(0,s.wk)()],n_.prototype,"_error",void 0),n_=nf([(0,s.EM)("esphome-add-script-dialog")],n_);let nb=(0,n.AH)`
  :host {
    display: block;
  }

  :host([hidden]) {
    display: none;
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
    /* Wrapper draws the border, so it carries the shared control height. */
    ${ep.BJ}
  }

  .search:focus-within {
    ${ep.jq}
  }

  input {
    flex: 1;
    min-width: 0;
    border: none;
    background: transparent;
    color: var(--wa-color-text-normal);
    ${ep.xw}
    /* 16px floor avoids iOS focus-zoom in the mobile drawer (overrides the
       shared 14px); the wrapper holds the height, so this doesn't grow it. */
    font-size: max(16px, var(--wa-font-size-s));
    font-family: inherit;
    padding: 0;
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
`;function ny(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({close:r.mdiClose});class nw extends n.WF{focusInput(){this._input?.focus()}render(){let e=this._localize("device.navigator_search_placeholder");return(0,n.qy)`
      <div class="search">
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
        ${this.value?(0,n.qy)`<button
                type="button"
                class="search-clear"
                @click=${this._clear}
                title=${this._localize("device.navigator_search_clear")}
                aria-label=${this._localize("device.navigator_search_clear")}
              >
                <wa-icon library="mdi" name="close"></wa-icon>
              </button>`:n.s6}
      </div>
      ${this.value&&this.resultLabel?(0,n.qy)`<p class="search-result" role="status">${this.resultLabel}</p>`:n.s6}
    `}_emit(e){(0,Z.r)(this,"navigator-search",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this.value="",this.resultLabel="",this._onInput=e=>{this.value=e.target.value,this._emit(this.value)},this._onKeydown=e=>{"Escape"===e.key&&this._input?.value&&(e.stopPropagation(),this._clear())},this._clear=()=>{this.value="",this._emit(""),this._input?.focus()}}}function n$(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}nw.styles=[b.G,nb],ny([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],nw.prototype,"_localize",void 0),ny([(0,s.MZ)()],nw.prototype,"value",void 0),ny([(0,s.MZ)()],nw.prototype,"resultLabel",void 0),ny([(0,s.P)("input")],nw.prototype,"_input",void 0),nw=ny([(0,s.EM)("esphome-navigator-search")],nw),(0,M.C)({"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,"chevron-right":r.mdiChevronRight,cog:r.mdiCog,magnify:r.mdiMagnify,menu:r.mdiMenu,"plus-circle-outline":r.mdiPlusCircleOutline,"script-text-outline":r.mdiScriptTextOutline});class nx extends n.WF{willUpdate(e){if((e.has("yaml")||e.has("platform")||e.has("platformReady"))&&this.yaml&&this.platformReady&&this._kickoffNameResolves(),(e.has("selectedKey")||e.has("yaml")||e.has("selectedFromLine"))&&this.yaml){if(!this.selectedKey){this._selectedLine=null,this._selectedRange=null;return}let e=[...(0,L.MT)(this.yaml),...(0,L.vB)(this.yaml)],t=(void 0!==this.selectedFromLine?e.find(e=>e.fromLine===this.selectedFromLine):void 0)??e.find(e=>(0,L.gU)(e)===this.selectedKey);t&&(this._selectedLine=t.fromLine,this._selectedRange={fromLine:t.fromLine,toLine:t.toLine})}}render(){let e=this._deriveBuckets(this.yaml),{core:t,components:i,automations:o}=e,a=[{label:this._localize("device.section_core"),desc:this._localize("device.section_core_desc"),icon:el,items:t,category:"core",actions:[{label:this._localize("device.add_config"),icon:"cog",onClick:()=>this._addConfigDialog.open()}]},{label:this._localize("device.section_components"),desc:this._localize("device.section_components_desc"),icon:ed,items:i,category:"component",actions:[{label:this._localize("device.add_component"),icon:ed,onClick:()=>this._addComponentDialog.open()}]},{label:this._localize("device.section_automations"),desc:this._localize("device.section_automations_desc"),icon:ec,items:o,category:"automation",actions:[{label:this._localize("device.add_automation"),icon:ec,onClick:()=>this._addAutomationDialog.open()},{label:this._localize("device.add_script"),icon:"script-text-outline",onClick:()=>this._addScriptDialog.open()}]}],r=this._resolveLabels(e,this._caches.tick,this.platform,this.deviceName,this._localize),s=this._query.trim(),l=s.length>0,d=l?r.map(e=>e.filter(({item:e,labels:t})=>(0,oQ.K)(s,t.primary,t.secondary,e.id,e.name))):null,c=a.reduce((e,t)=>e+t.items.length,0),h=this._expertMode&&(c>=15||this._searchOpen),p=this._expertMode&&(this._searchOpen||l),u=d?d.reduce((e,t)=>e+t.length,0):0,m=l&&u>0?this._localize("device.navigator_search_count",{count:u,total:c}):"";return(0,n.qy)`
      <section class="card" ${(0,f.Wf)(this.tourAnchorId)}>
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
          <h2 class="card-title truncate">${this._localize("device.navigator_title")}</h2>
          <div class="header-actions">
            ${h?(0,n.qy)`<button
                    type="button"
                    class="ghost-icon-btn search-btn"
                    aria-pressed=${p}
                    @click=${this._toggleSearch}
                    title=${this._localize("device.navigator_search_toggle")}
                    aria-label=${this._localize("device.navigator_search_toggle")}
                  >
                    <wa-icon library="mdi" name="magnify"></wa-icon>
                  </button>`:n.s6}
            <button
              type="button"
              class="ghost-icon-btn collapse-btn"
              @click=${this._onCollapseClick}
              title=${this._localize("device.hide_navigator")}
              aria-label=${this._localize("device.hide_navigator")}
            >
              <wa-icon library="mdi" name="menu"></wa-icon>
            </button>
          </div>
        </header>
        <div class="card-body">
          <esphome-navigator-search
            ?hidden=${!p}
            .value=${this._query}
            .resultLabel=${m}
            @navigator-search=${this._onSearchChange}
          ></esphome-navigator-search>
          ${l?n.s6:(0,n.qy)`<p class="italic">${this._localize("device.navigator_desc")}</p>`}
          <div class="separator"></div>
          ${l&&0===u?(0,n.qy)`<p class="nav-empty" role="status">
                  ${this._localize("device.navigator_search_none")}
                </p>`:a.map(({label:e,desc:t,icon:i,category:o,actions:a},s)=>{var c;let h=d?.[s]??r[s];return(c={label:e,desc:t,icon:i,actions:a,rows:h,groups:"component"===o?this._groupComponents(h):void 0,collapsedGroups:this._collapsedGroups,onToggleGroup:e=>this._toggleGroup(e),open:!!l||this.openSections.has(s),filtering:l,selectedLine:this._selectedLine,hoveredLine:this._hoveredLine,tourAnchorId:0===s&&this.tourAnchorId?this.classList.contains("drawer-nav")?"nav-mobile-core":"nav-core":void 0,errorCount:this.errorCounts.size?e=>this.errorCounts.get((0,y.pA)((0,L.gU)(e),e.fromLine))??0:void 0,errorLabel:e=>this._localize("device.navigator_error_count",{count:e}),onToggle:()=>{l||this._toggleSection(s)},onItemEnter:e=>this._onItemHover(e.fromLine,e.fromLine,e.toLine),onItemLeave:()=>this._onItemLeave(),onItemClick:e=>this._onItemClick(e)}).filtering&&0===c.rows.length?n.s6:(0,n.qy)`
    <div
      class="nav-content"
      role=${(0,iE.J)(c.filtering?void 0:"button")}
      tabindex=${(0,iE.J)(c.filtering?void 0:"0")}
      aria-expanded=${(0,iE.J)(c.filtering?void 0:c.open?"true":"false")}
      ${(0,f.Wf)(c.tourAnchorId)}
      @click=${c.filtering?void 0:c.onToggle}
      @keydown=${c.filtering?void 0:nv}
    >
      <div class="nav-content-label">
        <wa-icon library="mdi" name=${c.icon}></wa-icon>
        <p>${c.label}</p>
      </div>
      ${c.filtering?n.s6:(0,n.qy)`<wa-icon
              class="nav-content-chevron"
              library="mdi"
              name=${c.open?"chevron-up":"chevron-down"}
            ></wa-icon>`}
    </div>
    ${c.open?(0,n.qy)`
            <div class="separator"></div>
            ${c.filtering?n.s6:(0,n.qy)`<p class="italic">${c.desc}</p>`}
            ${c.groups?c.groups.map(e=>{var t,i;let o,a,r,s,l,d;return 1!==e.rows.length||e.rows[0].item.platform?(t=e,o=(i=c).filtering||!i.collapsedGroups?.has(t.key),a=!i.filtering,r=i.errorCount,s=!o&&r?t.rows.reduce((e,t)=>e+r(t.item),0):0,l=()=>{a&&i.onToggleGroup?.(t.key)},d=`navgroup-${t.key}`,(0,n.qy)`
    <div
      class="nav-subgroup-header ${a?"":"nav-subgroup-header--static"}"
      role=${(0,iE.J)(a?"button":void 0)}
      tabindex=${(0,iE.J)(a?"0":void 0)}
      aria-expanded=${(0,iE.J)(a?String(o):void 0)}
      aria-controls=${(0,iE.J)(a?d:void 0)}
      @click=${l}
      @keydown=${e=>{a&&("Enter"===e.key||" "===e.key)&&(e.preventDefault(),l())}}
    >
      <wa-icon
        class="nav-subgroup-icon"
        library="mdi"
        name=${(nh[t.key]??np)[0]}
      ></wa-icon>
      <span class="nav-subgroup-title">${nc(t.key)}</span>
      <span class="nav-subgroup-count">${t.rows.length}</span>
      ${s>0?nm(s,i):n.s6}
      ${a?(0,n.qy)`<wa-icon
              class="nav-subgroup-chevron"
              library="mdi"
              name=${o?"chevron-up":"chevron-down"}
            ></wa-icon>`:n.s6}
    </div>
    ${o?(0,n.qy)`<div id=${d} class="nav-items nav-items--grouped">
            ${t.rows.map(e=>nu(e,i,!1))}
          </div>`:n.s6}
  `):(0,n.qy)`<div class="nav-items nav-items--single">
    ${nu(e.rows[0],c,!0)}
  </div>`}):c.rows.length>0?(0,n.qy)`<div class="nav-items">
                      ${c.rows.map(e=>nu(e,c,!0))}
                    </div>`:n.s6}
            ${c.filtering?n.s6:(0,n.qy)`<div class="nav-items">
                    ${c.actions.map(e=>(0,n.qy)`<div class="action-item" @click=${()=>e.onClick()}>
    <div>
      <wa-icon library="mdi" name=${e.icon}></wa-icon>
      <p>${e.label}</p>
    </div>
    <wa-icon library="mdi" name="plus-circle-outline"></wa-icon>
  </div>`)}
                  </div>`}
          `:n.s6}
    <div class="separator"></div>
  `})}
        </div>
      </section>
    `}_toggleSection(e){(0,Z.r)(this,"section-toggle",{index:e})}_toggleGroup(e){let t=new Set(this._collapsedGroups);t.delete(e)||t.add(e),this._collapsedGroups=t}_kickoffNameResolves(){if(!this._api)return;let e=(0,L.MT)(this.yaml),{core:t,components:i}=(0,L.uU)(e),o=this.platform||void 0;for(let e of[...t,...i]){let t=(0,L.gU)(e);void 0===(0,e5.CQ)(t,o)&&(0,e5.Sn)(this._api,t,o).catch(()=>{})}this._triggerCatalog.ensure()}_onItemHover(e,t,i){this._hoveredLine=e,this._emitHighlight({fromLine:t,toLine:i},!1)}_onItemLeave(){this._hoveredLine=null,this._emitHighlight(this._selectedRange,!1)}_onItemClick(e){let{fromLine:t,toLine:i}=e,o=(0,L.gU)(e);this._selectedLine===t?(this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._emitHighlight(this._hoveredLine===t?{fromLine:t,toLine:i}:null,!1),this._emitSectionSelect(null,void 0)):(this.selectedKey=o,this._selectedLine=t,this._selectedRange={fromLine:t,toLine:i},this._emitHighlight({fromLine:t,toLine:i},!0),this._emitSectionSelect(o,t))}_emitHighlight(e,t){(0,Z.r)(this,"yaml-highlight",{range:e,scroll:t})}_emitSectionSelect(e,t){(0,Z.r)(this,"section-select",{sectionKey:e,fromLine:t})}constructor(...e){super(...e),this._localize=e=>e,this._caches=new ni(this,[e5.Ej,oa]),this._triggerCatalog=new rn(this,()=>({api:this._api,platform:this.platform||void 0,boardId:this.board?.id})),this._reveal=new ng(this,()=>({selectedLine:this._selectedLine,buckets:this._deriveBuckets(this.yaml),openSections:this.openSections,filtering:this._query.trim().length>0})),this.openSections=new Set,this.yaml="",this._deriveBuckets=(0,l.A)(na),this._groupComponents=(0,l.A)(nr),this._resolveLabels=(0,l.A)((e,t,i,o,a)=>{var r;return r={triggerCatalog:this._triggerCatalog,platform:i,deviceName:o,localize:a,substitutions:e.substitutions},[e.core.map(e=>({item:e,labels:nn(e,"core",r)})),e.components.map(e=>({item:e,labels:nn(e,"component",r)})),e.automations.map(e=>({item:e,labels:nn(e,"automation",r)}))]}),this.board=null,this.boardName="",this.configuration="",this.deviceName="",this.platform="",this.platformReady=!1,this.selectedKey=null,this.errorCounts=new Map,this._selectedLine=null,this._selectedRange=null,this._hoveredLine=null,this._expertMode=!1,this._query="",this._searchOpen=!1,this._collapsedGroups=new Set,this._onSearchChange=e=>{this._query=e.detail.value},this._toggleSearch=()=>{if(this._searchOpen||this._query){this._searchOpen=!1,this._query="";return}this._searchOpen=!0,this.updateComplete.then(()=>this._search?.focusInput())},this._onCollapseClick=()=>{(0,Z.r)(this,"nav-collapse")},this._onAutomationAdded=e=>{e.stopPropagation(),this._emitSectionSelect(e.detail.sectionKey,void 0)}}}nx.styles=[b.G,U.U,no],n$([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],nx.prototype,"_localize",void 0),n$([(0,a.Fg)({context:_.Ie})],nx.prototype,"_api",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"openSections",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"tourAnchorId",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"yaml",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"board",void 0),n$([(0,s.MZ)()],nx.prototype,"boardName",void 0),n$([(0,s.MZ)()],nx.prototype,"configuration",void 0),n$([(0,s.MZ)()],nx.prototype,"deviceName",void 0),n$([(0,s.MZ)()],nx.prototype,"platform",void 0),n$([(0,s.MZ)({type:Boolean})],nx.prototype,"platformReady",void 0),n$([(0,s.P)("esphome-add-config-dialog")],nx.prototype,"_addConfigDialog",void 0),n$([(0,s.P)("esphome-add-component-dialog")],nx.prototype,"_addComponentDialog",void 0),n$([(0,s.P)("esphome-add-automation-dialog")],nx.prototype,"_addAutomationDialog",void 0),n$([(0,s.P)("esphome-add-script-dialog")],nx.prototype,"_addScriptDialog",void 0),n$([(0,s.P)("esphome-navigator-search")],nx.prototype,"_search",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"selectedKey",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"selectedFromLine",void 0),n$([(0,s.MZ)({attribute:!1})],nx.prototype,"errorCounts",void 0),n$([(0,s.wk)()],nx.prototype,"_selectedLine",void 0),n$([(0,s.wk)()],nx.prototype,"_selectedRange",void 0),n$([(0,s.wk)()],nx.prototype,"_hoveredLine",void 0),n$([(0,a.Fg)({context:_.Pt,subscribe:!0}),(0,s.wk)()],nx.prototype,"_expertMode",void 0),n$([(0,s.wk)()],nx.prototype,"_query",void 0),n$([(0,s.wk)()],nx.prototype,"_searchOpen",void 0),n$([(0,s.wk)()],nx.prototype,"_collapsedGroups",void 0),nx=n$([(0,s.EM)("esphome-device-navigator")],nx),i(5973),i(7747),i(8687),i(9786);var nk=i(6029);function nz(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}(0,M.C)({"alert-outline":r.mdiAlertOutline});class nC extends n.WF{get _canGoToError(){return this.firstErrorLine>0&&!this.firstErrorFile}open(){this._resolvedExit=null,this._dialog.open=!0}close(){this._dialog.open=!1}render(){let e=this._localize("device.yaml_invalid_message",{count:this.errorCount}),t=this.firstErrorFile?this._localize("device.yaml_invalid_in_included_file",{file:this.firstErrorFile,line:this.firstErrorLine}):"";return(0,n.qy)`
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
            ${t?(0,n.qy)`<div class="included-file">${t}</div>`:n.s6}
            ${this.firstErrorMessage?(0,n.qy)`<div class="first-error">${this.firstErrorMessage}</div>`:n.s6}
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
    `}_goto(){this._canGoToError&&null===this._resolvedExit&&(this._resolvedExit="goto",this.close(),(0,Z.r)(this,"goto",{line:this.firstErrorLine,col:this.firstErrorCol}))}_saveAnyway(){this._resolvedExit="save-anyway",this.close(),(0,Z.r)(this,"save-anyway")}_onAfterHide(){this._dialog.open=!1,null===this._resolvedExit&&(0,Z.r)(this,"cancel")}constructor(...e){super(...e),this._localize=e=>e,this.errorCount=0,this.firstErrorLine=0,this.firstErrorCol=0,this.firstErrorMessage="",this.firstErrorFile="",this._dialog=new eu.T(this),this._resolvedExit=null,this._gotoOnEnter=()=>{this._canGoToError&&this._goto()}}}function nq(e,t,i,o){var a,r=arguments.length,n=r<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,o);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}nC.styles=[b.G,nk.W,(0,n.AH)`
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
    `],nz([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],nC.prototype,"_localize",void 0),nz([(0,s.MZ)({type:Number})],nC.prototype,"errorCount",void 0),nz([(0,s.MZ)({type:Number})],nC.prototype,"firstErrorLine",void 0),nz([(0,s.MZ)({type:Number})],nC.prototype,"firstErrorCol",void 0),nz([(0,s.MZ)()],nC.prototype,"firstErrorMessage",void 0),nz([(0,s.MZ)()],nC.prototype,"firstErrorFile",void 0),nC=nz([(0,s.EM)("esphome-yaml-validation-dialog")],nC),(0,M.C)({"arrow-left":r.mdiArrowLeft,"chevron-right":r.mdiChevronRight,menu:r.mdiMenu});class nS extends n.WF{get _device(){return this._devices.find(e=>e.configuration===this.id)??null}_navErrorCounts(e,t){let i=this._baseErrorCounts(e);if(null===t||!i.has(t))return i;let o=new Map(i);return o.delete(t),o}_createInstallController(){let e=this;return new v({addController:t=>e.addController(t),removeController:t=>e.removeController(t),requestUpdate:()=>e.requestUpdate(),get updateComplete(){return e.updateComplete},get device(){return e._device},get commandDialog(){return e._commandDialog??null},get firmwareDialog(){return e._firmwareDialog??null},get logsDialog(){return e._logsDialog??null},get api(){return e._api},get localize(){return e._localize},openActiveJobProgress:()=>e._showActiveJobProgress()})}get _isYamlDirty(){return this._yaml!==this._savedYaml}get _isDirty(){return this._isYamlDirty||this._sectionDirty}async connectedCallback(){super.connectedCallback(),this._loadPreferences(),(0,S.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("keydown",this._onKeydown),this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),(0,S.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),window.removeEventListener("keydown",this._onKeydown),this._mql.removeEventListener("change",this._onMqlChange),this._unsavedGuard.cancelPending()}updated(e){e.has("id")&&this.id&&(this._justCreated=(0,q.RI)(this.id),this._loadedBoardId=null,this._board=null,this._platformReady=!1,this._backendErrors.length&&(this._backendErrors=[]),this._heldUnknownInstance=null,this._kickKnownKeys(),this._loadYaml());let t=this._device?.board_id??null;t&&t!==this._loadedBoardId?(this._loadedBoardId=t,this._board=null,this._platformReady=!1,this._loadBoard(t)):!t&&(null!==this._loadedBoardId&&(this._loadedBoardId=null,this._board=null),(null!==this._device||this._devicesLoaded)&&(this._platformReady=!0))}_readStoredLayout(){let e=localStorage.getItem("esphome-editor-layout");return"both"===e||"left"===e||"right"===e?e:null}async _loadPreferences(){let e=this._readStoredLayout();e&&(this._layout=e);try{let t=await this._api.getPreferences();this._navCollapsed=!t.navigator_visible,e||null!==this._readStoredLayout()||(this._layout=(0,z.r5)(t.device_editor_layout))}catch(e){console.warn("Failed to load device preferences:",e)}}async _loadBoard(e){try{let t=await (0,$.tK)(this._api,e);this._loadedBoardId===e&&(this._board=t,this._platformReady=!0)}catch(t){console.error("Failed to load board:",t),this._loadedBoardId===e&&(this._board=null,this._platformReady=!0)}}async _loadYaml(){try{let e=await this._api.getConfig(this.id);this._yaml=e,this._savedYaml=e,this._maybeResolveLineFromUrl()}catch(e){console.error("Failed to load YAML:",e)}}_maybeResolveLineFromUrl(){if(void 0===this._pendingUrlLine||!this._yaml)return;let e=this._pendingUrlLine;this._pendingUrlLine=void 0;let t=function(e,t,i){let o=O(e,t);if(!o||null!==i&&i!==o.sectionKey)return null;let a=(0,F.L2)(e,o.range.fromLine);return{...o,fieldPath:a?(0,y.es)(a.path):[],yamlPath:a?.indexedPath}}(this._yaml,e,this._selectedSection);t&&(this._selectedSection=t.sectionKey,this._selectedFromLine=t.sectionFromLine,this._focusFieldPath=t.fieldPath,this._focusYamlPath=t.yamlPath,this._setHighlight(t.range,!0))}_boardDisagreement(){if(!this._board)return null;let e=(0,T.G)(this._yaml);return e&&(0,T.n)(e,this._board)?e:null}_openBoardReselect(){return(0,x.UM)(this._boardReselectDialog,{configuration:this.id,yaml:this._yaml})}async _maybePromptBoardReselect(){if(this._suppressBoardPrompt)return;let e=this._boardDisagreement();if(!e)return;let t=`${this.id}|${e.platform}|${e.board}|${e.variant}`;this._boardPromptShownFor===t||(this._boardPromptShownFor=t,await this._openBoardReselect().catch(e=>(console.error("Board reselect prompt failed:",e),!1))||this._boardPromptShownFor!==t||(this._boardPromptShownFor=null))}_jumpToErrorLine(e){if(!e||e<1)return;"left"===this._layout&&this._cacheLayout("both"),this._setHighlight({fromLine:e,toLine:e},!0,!0);let t=O(this._yaml,e);t&&(this._selectedSection=t.sectionKey)}_resolveValidationPrompt(e){let t=this._pendingValidationResolve;this._pendingValidationResolve=null,t?.(e)}_showActiveJobProgress(){return(0,C.xW)(this._activeJobs,this.id,this._commandDialog,this._devices,this._localize)}_cleanBuild(e){this._commandDialog.configuration=e.configuration,this._commandDialog.name=e.friendly_name||e.name,this._commandDialog.open("clean")}render(){let e=this._device?.friendly_name||this._device?.name||this.id||this._localize("dashboard.create_device"),t=this._isMobile?!this._drawerOpen:this._navCollapsed,i=this._localize("device.back");return(0,n.qy)`
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
            .focusYamlPath=${this._focusYamlPath}
            .backendErrors=${this._instanceBackendErrors(this._backendErrors,this._selectedSection,this._selectedFromLine)}
            .justCreated=${this._justCreated}
            @just-created-dismiss=${this._dismissJustCreated}
            @request-install=${this._saveThenInstall}
            @goto-line=${this._onEditorGoToLine}
            @change-board=${this._onChangeBoard}
            @open-logs=${this._onEditorOpenLogs}
            @clean-build=${this._onEditorCleanBuild}
            ?hasUnsavedEdits=${this._isDirty}
            ?saving=${this._saving}
            ?showModified=${!!this._device&&(0,k.EJ)(this._device)}
            ?showUpdate=${!!this._device&&(0,k.QH)(this._device)}
            .installedVersion=${this._device?.runtime_state.deployed_version??""}
            .availableVersion=${this._device?.current_version??""}
            .webUiUrl=${this._device?(0,R.Gv)(this._device):""}
            ?busy=${this._activeJobs.has(this.id)}
          >
            ${t||this._selectedSection?(0,n.qy)`<div slot="header-start" class="header-start-group">
                    ${t?(0,n.qy)`<button
                            type="button"
                            class="ghost-icon-btn nav-toggle-btn"
                            ${(0,f.Wf)("nav-toggle")}
                            @click=${this._onNavExpand}
                            title=${this._localize("device.show_navigator")}
                            aria-label=${this._localize("device.show_navigator")}
                          >
                            <wa-icon library="mdi" name="menu"></wa-icon>
                          </button>`:n.s6}
                    ${this._selectedSection?(0,n.qy)`<button
                            class="ghost-icon-btn back-btn"
                            @click=${this._onBack}
                            title=${i}
                            aria-label=${i}
                          >
                            <wa-icon library="mdi" name="arrow-left"></wa-icon>
                          </button>`:n.s6}
                  </div>`:n.s6}
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
          @request-change-board=${this._onRequestChangeBoard}
        ></esphome-firmware-install-dialog>
        <esphome-logs-dialog></esphome-logs-dialog>
        <esphome-install-method-dialog
          ?open=${this._installCtrl.installMethodOpen}
          .deviceState=${this._installCtrl.deviceState}
          .deviceTargetPlatform=${this._installCtrl.deviceTargetPlatform}
          .deviceCurrentAddress=${this._installCtrl.deviceCurrentAddress}
          .canFlashBootloader=${this._installCtrl.canFlashBootloader}
          .neverFlashed=${this._installCtrl.neverFlashed}
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
    `}_onSectionToggle(e){let{index:t}=e.detail,i=new Set;this._openSections.has(t)||i.add(t),this._openSections=i,this._updateUrl()}_onSectionReveal(e){let{index:t}=e.detail;this._openSections.has(t)||(this._openSections=new Set([t]),this._updateUrl())}_onNavSectionShow(e){let t={core:0,components:1,automations:2}[e.detail.section];if(void 0===t)return;let i=new Set([t]);this._openSections=i,this._updateUrl(),this._drawerOpen=!0,this._navCollapsed&&(this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{}))}_onLayoutChange(e){this._persistLayout(e.detail)}_cacheLayout(e){this._layout=e,localStorage.setItem("esphome-editor-layout",e)}_persistLayout(e){this._cacheLayout(e),this._api.updatePreferences({device_editor_layout:(0,z.jr)(e)}).catch(e=>console.warn("Failed to persist device layout preference:",e))}_renderNavigator(e){let t="desktop-nav"===e?!this._isMobile&&!this._navCollapsed:this._isMobile&&this._drawerOpen;return(0,n.qy)`<esphome-device-navigator
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
    ></esphome-device-navigator>`}_setYaml(e){this._yaml=e,"active"===this._errorHighlight&&(this._errorHighlight="edited")}_onYamlChange(e){this._setYaml(e.detail.value),this._retryPendingFieldLine()}_onYamlDiagnostics(e){if(e.detail.configuration!==this.id)return;"edited"===this._errorHighlight&&this._setHighlight(null,!1);let t=(0,y.cU)(this._yaml,e.detail.mapped);(t.length||this._backendErrors.length)&&(this._backendErrors=t)}_onYamlCursorLine(e){this._clearPendingFieldLine();let t=e.detail.path??[],i=(0,L.tO)(this._yaml,e.detail.line,t);if(!i)return;let o=(0,y.es)(t),a=(0,L.gU)(i);if(a===this._selectedSection&&i.fromLine===this._selectedFromLine){this._focusFieldPath=o,this._focusYamlPath=e.detail.indexedPath;return}if(!0===e.detail.viaEdit&&null!==this._knownTopLevelKeys&&!this._knownTopLevelKeys.has(i.key)){this._heldUnknownInstance=(0,y.pA)(a,i.fromLine);return}this._heldUnknownInstance=null,this._guardSectionSwitch(()=>{this._selectedSection=a,this._selectedFromLine=i.fromLine,this._focusFieldPath=o,this._focusYamlPath=e.detail.indexedPath,this._clearBlockHighlight(),this._updateUrl()})}_focusedSection(){if(!this._selectedSection)return;let e=(0,L.MT)(this._yaml);return(void 0!==this._selectedFromLine?e.find(e=>e.fromLine===this._selectedFromLine):void 0)??e.find(e=>(0,L.gU)(e)===this._selectedSection)}_highlightFieldLine(e){let t=this._focusedSection(),i=t?(0,L.of)(this._yaml,t,e):null;return null!==i&&this._setHighlight({fromLine:i,toLine:i},!0),{section:t,found:null!==i}}_onFieldFocus(e){let t=this._focusedFieldPath=e.detail.path;if(!t.length)return;let{section:i,found:o}=this._highlightFieldLine(t);o?this._clearPendingFieldLine():(this._pendingFieldLine=!0,this._pendingFieldSection={section:this._selectedSection,fromLine:this._selectedFromLine},this._setHighlight(i?{fromLine:i.fromLine,toLine:i.toLine}:null,void 0!==i))}_retryPendingFieldLine(){if(this._pendingFieldLine&&this._focusedFieldPath?.length){if(this._pendingFieldSection?.section!==this._selectedSection||this._pendingFieldSection?.fromLine!==this._selectedFromLine)return void this._clearPendingFieldLine();this._highlightFieldLine(this._focusedFieldPath).found&&this._clearPendingFieldLine()}}_clearPendingFieldLine(){this._pendingFieldLine=!1,this._pendingFieldSection=void 0}_onYamlHighlight(e){this._setHighlight(e.detail.range,e.detail.scroll)}_onYamlUserEdit(){this._clearBlockHighlight()}_clearBlockHighlight(){this._highlightRange&&"none"===this._errorHighlight&&this._setHighlight(null,!1)}_setHighlight(e,t,i=!1){this._highlightRange=e,this._scrollToHighlight=t,this._errorHighlight=i&&null!==e?"active":"none"}_onYamlUpdated(e){this._setYaml(e.detail.yaml),this._savedYaml=e.detail.yaml}_onYamlDraft(e){this._setYaml(e.detail.yaml),this._retryPendingFieldLine()}_onSectionSelect(e){let{sectionKey:t,fromLine:i}=e.detail;if(this._heldUnknownInstance=null,t===this._selectedSection&&i===this._selectedFromLine){this._drawerOpen=!1;return}this._guardSectionSwitch(()=>{let e=this._selectedSection,o=this._selectedFromLine;null===t?this._sectionHistory=[]:null!==e&&(this._sectionHistory=[...this._sectionHistory,{key:e,fromLine:o}]),this._selectedSection=t,this._selectedFromLine=i,this._focusFieldPath=void 0,this._focusYamlPath=void 0,this._drawerOpen=!1,this._updateUrl()})}_guardSectionSwitch(e){this._activeSection?.flushPending(),e()}_kickKnownKeys(){this._catalogKicked||(this._catalogKicked=!0,(0,D.ak)(this._api).then(e=>{this._knownTopLevelKeys=(0,I.Bt)(e),null===this._knownTopLevelKeys&&(this._catalogKicked=!1)}))}_readUrlParam(e,t){var i;return i=window.location.search,new URLSearchParams(i).get(e)??t}_readUrlLine(){let e=new URLSearchParams(window.location.search).get("line");if(!e)return;let t=Number(e);return Number.isNaN(t)?void 0:t}_readUrlSections(){let e;return(e=new URLSearchParams(window.location.search).get("open"))?e.split(",").map(Number).filter(e=>!Number.isNaN(e)):[]}_updateUrl(){var e,t,i;let o,a,r,n=(e=window.location.search,t=window.location.pathname,i={selectedSection:this._selectedSection,selectedFromLine:this._selectedFromLine,openSections:this._openSections},o=new URLSearchParams(e),i.selectedSection?(o.set("section",i.selectedSection),void 0!==i.selectedFromLine?o.set("line",String(i.selectedFromLine)):o.delete("line")):(o.delete("section"),o.delete("line")),(a=[...i.openSections]).length>0?o.set("open",a.join(",")):o.delete("open"),r=o.toString(),`${t}${r?`?${r}`:""}`);window.history.replaceState(window.history.state,"",n)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._devicesLoaded=!1,this._activeJobs=new Map,this.id="",this._justCreated=!1,this._layout="both",this._tourLayout=new g.d_(this,()=>this._layout,e=>{this._layout=e}),this._openSections=new Set(this._readUrlSections()),this._board=null,this._platformReady=!1,this._loadedBoardId=null,this._highlightRange=null,this._scrollToHighlight=!1,this._errorHighlight="none",this._selectedSection=this._readUrlParam("section",null),this._pendingUrlLine=this._readUrlLine(),this._backendErrors=[],this._heldUnknownInstance=null,this._knownTopLevelKeys=null,this._catalogKicked=!1,this._instanceBackendErrors=(0,l.A)(y.Oq),this._baseErrorCounts=(0,l.A)(y.lt),this._pendingFieldLine=!1,this._sectionHistory=[],this._drawerOpen=!1,this._navCollapsed=!1,this._isMobile=window.matchMedia("(max-width: 900px)").matches,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._yaml="",this._savedYaml="",this._saving=!1,this._activeSection=null,this._sectionDirty=!1,this._suppressBoardPrompt=!1,this._boardPromptShownFor=null,this._validationErrorCount=0,this._validationFirstLine=0,this._validationFirstCol=0,this._validationFirstMessage="",this._validationFirstFile="",this._onPostInstallShowLogs=(0,A.ei)(()=>this._logsDialog,()=>this._localize),this._installCtrl=this._createInstallController(),this._unsavedGuard=new E._,this._allowingLeave=!1,this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._confirmLeave=async()=>{this._activeSection?.flushPending();let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>(!this._isYamlDirty||!!await this._saveYaml())&&(this._allowingLeave=!0,!0)});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._activeSection?.flushPending(),this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._activeSection?.flushPending(),this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,w.cV)(`/device/${this.id}`)),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onKeydown=e=>{if("Escape"!==e.key||e.defaultPrevented)return;let t=e.composedPath()[0];if(!(0,P.t)(t)){if(this._drawerOpen){e.preventDefault(),this._drawerOpen=!1;return}e.preventDefault(),(0,S.SJ)()}},this._dismissJustCreated=()=>{this._justCreated=!1},this._onChangeBoard=async e=>{let t=e.detail?.boardId,i=this._device;if(t&&i&&t!==i.board_id){if(this._isDirty)return void(0,d.UG)(this._localize("device.change_board_unsaved"));await (0,x.Xt)(this._api,this._localize,i.configuration,t)}},this._pendingValidationResolve=null,this._saveYaml=async()=>{if(this._saving||null!==this._pendingValidationResolve)return!1;this._saving=!0;try{if(await this._activeSection?.flushPending(),!this._isYamlDirty)return!0;if(this.id)try{let e=(0,B.mL)(this.id,this._yaml)??await this._api.validateYaml(this.id,this._yaml),t=(0,j.tu)(e,this._yaml,this._localize);if(t.count>0){this._validationErrorCount=t.count,this._validationFirstLine=t.first?.line??0,this._validationFirstCol=t.first?.col??0,this._validationFirstMessage=t.first?.message??"";let e=t.first?.file??null;return this._validationFirstFile=e&&this.id&&!(0,j.lg)(e,this.id)?(0,j.P8)(e):"",new Promise(e=>{this._pendingValidationResolve=e,this._yamlValidationDialog.open()})}}catch(e){console.debug("[save-yaml] validate_yaml failed, saving anyway:",e)}return await this._doSaveYaml()}finally{this._saving=!1}},this._doSaveYaml=async()=>{let e=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let t=!0;try{await this._api.updateConfig(this.id,this._yaml)}catch(i){(i instanceof Error?i.message:"").includes("timed out")||(t=!1,this._savedYaml=e,console.error("Failed to save YAML:",i))}finally{this._saving=!1}t&&"none"!==this._errorHighlight&&this._setHighlight(null,!1);let i=t?"device.yaml_saved":"device.yaml_save_error";return(t?d.VX:d.UG)(this._localize(i)),t&&this._maybePromptBoardReselect(),t},this._onRequestChangeBoard=e=>{let t=e.detail.configuration===this.id&&!this._isDirty;(0,x.UM)(this._boardReselectDialog,{configuration:e.detail.configuration,yaml:t?this._yaml:void 0})},this._onValidationSaveAnyway=async()=>{let e=await this._doSaveYaml();this._resolveValidationPrompt(e)},this._onValidationGoTo=e=>{this._jumpToErrorLine(e.detail.line),this._resolveValidationPrompt(!1)},this._onEditorGoToLine=e=>{this._jumpToErrorLine(e.detail.line)},this._onValidationCancel=()=>{this._resolveValidationPrompt(!1)},this._onValidateClick=()=>{this._device&&(this._commandDialog.configuration=this._device.configuration,this._commandDialog.name=this._device.friendly_name||this._device.name,this._commandDialog.open("validate"))},this._installAfterSave=async e=>{let t;if(!this._showActiveJobProgress()){this._suppressBoardPrompt=!0;try{t=await this._saveYaml()}catch(e){console.error("Failed to save before install:",e),(0,d.UG)(this._localize("device.yaml_save_error"));return}finally{this._suppressBoardPrompt=!1}if(t&&!(this._boardDisagreement()&&await this._openBoardReselect()))try{await e()}catch(e){console.error("Install entry failed:",e),(0,d.UG)(this._localize("device.install_start_failed"))}}},this._saveThenInstall=()=>this._installAfterSave(this._installCtrl.onInstall),this._saveThenUpdate=()=>this._installAfterSave(this._installCtrl.onUpdate),this._onCleanBuild=e=>{this._cleanBuild(e.detail)},this._onEditorOpenLogs=()=>this._installCtrl.onLogs(),this._onEditorCleanBuild=()=>{this._device&&this._cleanBuild(this._device)},this._onRequestOpenEditor=e=>{e.stopPropagation(),e.detail.configuration!==this._device?.configuration&&(0,S.oo)(`/device/${encodeURIComponent(e.detail.configuration)}`)},this._onBack=()=>{this._heldUnknownInstance=null,this._guardSectionSwitch(()=>{let e=this._sectionHistory.length?this._sectionHistory[this._sectionHistory.length-1]:null;e?(this._sectionHistory=this._sectionHistory.slice(0,-1),this._selectedSection=e.key,this._selectedFromLine=e.fromLine):(this._selectedSection=null,this._selectedFromLine=void 0),this._setHighlight(null,!1),this._updateUrl()})},this._onNavExpand=()=>{if(this._isMobile){this._drawerOpen=!0;return}this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{})},this._onNavCollapse=()=>{if(this._isMobile){this._drawerOpen=!1;return}this._navCollapsed=!0,this._api.updatePreferences({navigator_visible:!1}).catch(()=>{})},this._onSectionMount=e=>{this._activeSection=e.detail.node,this._sectionDirty=e.detail.node.dirty},this._onSectionUnmount=e=>{this._activeSection===e.detail.node&&(this._activeSection=null,this._sectionDirty=!1)},this._onSectionDirtyChange=e=>{this._sectionDirty=e.detail.dirty}}}nS.styles=[b.G,K],nq([(0,a.Fg)({context:_.$F,subscribe:!0}),(0,s.wk)()],nS.prototype,"_localize",void 0),nq([(0,a.Fg)({context:_.xJ,subscribe:!0}),(0,s.wk)()],nS.prototype,"_devices",void 0),nq([(0,a.Fg)({context:_.UL,subscribe:!0}),(0,s.wk)()],nS.prototype,"_devicesLoaded",void 0),nq([(0,a.Fg)({context:_.Ie})],nS.prototype,"_api",void 0),nq([(0,a.Fg)({context:_.EM,subscribe:!0}),(0,s.wk)()],nS.prototype,"_activeJobs",void 0),nq([(0,s.MZ)()],nS.prototype,"id",void 0),nq([(0,s.wk)()],nS.prototype,"_justCreated",void 0),nq([(0,s.wk)()],nS.prototype,"_layout",void 0),nq([(0,s.wk)()],nS.prototype,"_openSections",void 0),nq([(0,s.wk)()],nS.prototype,"_board",void 0),nq([(0,s.wk)()],nS.prototype,"_platformReady",void 0),nq([(0,s.wk)()],nS.prototype,"_highlightRange",void 0),nq([(0,s.wk)()],nS.prototype,"_scrollToHighlight",void 0),nq([(0,s.wk)()],nS.prototype,"_selectedSection",void 0),nq([(0,s.wk)()],nS.prototype,"_selectedFromLine",void 0),nq([(0,s.wk)()],nS.prototype,"_focusFieldPath",void 0),nq([(0,s.wk)()],nS.prototype,"_focusYamlPath",void 0),nq([(0,s.wk)()],nS.prototype,"_backendErrors",void 0),nq([(0,s.wk)()],nS.prototype,"_heldUnknownInstance",void 0),nq([(0,s.wk)()],nS.prototype,"_sectionHistory",void 0),nq([(0,s.wk)()],nS.prototype,"_drawerOpen",void 0),nq([(0,s.wk)()],nS.prototype,"_navCollapsed",void 0),nq([(0,s.wk)()],nS.prototype,"_isMobile",void 0),nq([(0,s.wk)()],nS.prototype,"_yaml",void 0),nq([(0,s.wk)()],nS.prototype,"_savedYaml",void 0),nq([(0,s.wk)()],nS.prototype,"_saving",void 0),nq([(0,s.P)("esphome-unsaved-changes-dialog")],nS.prototype,"_unsavedDialog",void 0),nq([(0,s.wk)()],nS.prototype,"_sectionDirty",void 0),nq([(0,s.P)("esphome-command-dialog")],nS.prototype,"_commandDialog",void 0),nq([(0,s.P)("esphome-firmware-install-dialog")],nS.prototype,"_firmwareDialog",void 0),nq([(0,s.P)("esphome-logs-dialog")],nS.prototype,"_logsDialog",void 0),nq([(0,s.P)("esphome-yaml-validation-dialog")],nS.prototype,"_yamlValidationDialog",void 0),nq([(0,s.P)("esphome-board-reselect-dialog")],nS.prototype,"_boardReselectDialog",void 0),nq([(0,s.wk)()],nS.prototype,"_validationErrorCount",void 0),nq([(0,s.wk)()],nS.prototype,"_validationFirstLine",void 0),nq([(0,s.wk)()],nS.prototype,"_validationFirstCol",void 0),nq([(0,s.wk)()],nS.prototype,"_validationFirstMessage",void 0),nq([(0,s.wk)()],nS.prototype,"_validationFirstFile",void 0),nS=nq([(0,s.EM)("esphome-page-device")],nS)}}]);
//# sourceMappingURL=35.12cb279d98b83adb.js.map