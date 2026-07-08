"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[37],{2180(e,t,i){i.r(t),i.d(t,{ESPHomePageDevice:()=>rP});var a,o=i(5172),r=i(9165),s=i(2009),n=i(3442),l=i(1811),d=i(918),c=i(6668),h=i(8159),p=i(1079);class u{hostConnected(){}get deviceState(){return this._host.device?.state??c.g.UNKNOWN}get deviceTargetPlatform(){return this._host.device?.target_platform??""}get deviceCurrentAddress(){return this._host.device?.ip||this._host.device?.address||""}get canFlashBootloader(){return(0,h.A)(this._host.device)}_openCommand(e,t,i,a){this._host.commandDialog?.openForDevice(e,t,{port:i,...a})}constructor(e){this.installMethodOpen=!1,this.onInstall=()=>{this._host.device&&(this.installMethodOpen=!0,this._host.requestUpdate())},this.onUpdate=()=>{let e=this._host.device;e&&this._openCommand(e,"install")},this.onInstallMethodClose=()=>{this.installMethodOpen=!1,this._host.requestUpdate()},this.onInstallMethodSelect=e=>{let t=this._host.device;if(this.installMethodOpen=!1,this._host.requestUpdate(),!t)return;let{method:i,port:a}=e.detail;(0,p.D)(i,a,{device:t,firmwareDialog:this._host.firmwareDialog,openInstall:(e,i)=>this._openCommand(t,"install",e,i)})},this._host=e,e.addController(this)}}var m=i(1556),v=i(3140),g=i(2812),f=i(9460),_=i(9363),b=i(157),y=i(9877),w=i(3632),$=i(1529),x=i(2063),k=i(1093),z=i(9317),C=i(9328);function q(e,t,i){if(void 0===t||!Number.isInteger(t)||t<1||null!==i||!e)return null;let a=(0,C.VN)(e,t);return a?{sectionKey:(0,C.gU)(a),range:{fromLine:t,toLine:t}}:null}var E=i(1269),S=i(5091);let A=(0,s.AH)`
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
`;i(2202),i(9968);var M=i(4818);let P="esphome-editor-split-ratio",L=e=>Math.min(.75,Math.max(.25,e)),F=e=>{try{localStorage.setItem(P,String(e))}catch{}},O=(0,s.AH)`
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
    bottom: var(--wa-space-xs);
    right: var(--wa-space-xs);
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
  .validate-button wa-icon,
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
`;var R=i(6048);i(3238),i(6117),i(8768);var T=i(5343);function D(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}class I extends s.WF{render(){if(this._darkMode?this.setAttribute("dark",""):this.removeAttribute("dark"),this.oldValue===this.newValue)return(0,s.qy)`<div class="empty">${this._localize("device.diff_no_changes")}</div>`;let e=function(e,t){let i=e.split("\n"),a=t.split("\n"),o=i.length,r=a.length,s=[];for(let e=0;e<=o;e++)s.push(new Uint32Array(r+1));for(let e=1;e<=o;e++)for(let t=1;t<=r;t++)s[e][t]=i[e-1]===a[t-1]?s[e-1][t-1]+1:Math.max(s[e-1][t],s[e][t-1]);let n=[],l=o,d=r;for(;l>0||d>0;)l>0&&d>0&&i[l-1]===a[d-1]?(n.push({type:"context",oldLine:l,newLine:d,content:i[l-1]}),l--,d--):d>0&&(0===l||s[l][d-1]>=s[l-1][d])?(n.push({type:"add",newLine:d,content:a[d-1]}),d--):(n.push({type:"remove",oldLine:l,content:i[l-1]}),l--);return n.reverse()}(this.oldValue,this.newValue);return(0,s.qy)`
      <table>
        <tbody>
          ${e.map(e=>this._renderLine(e))}
        </tbody>
      </table>
    `}_renderLine(e){let t="add"===e.type?"+":"remove"===e.type?"-":" ",i="remove"===e.type?e.oldLine:e.newLine;return(0,s.qy)`
      <tr class=${e.type}>
        <td class="gutter">${i??(0,s.qy)`&nbsp;`}</td>
        <td class="marker">${t}</td>
        <td class="content">${e.content||s.s6}</td>
      </tr>
    `}constructor(...e){super(...e),this._darkMode=(0,T.yk)(),this._localize=e=>e,this.oldValue="",this.newValue=""}}I.styles=(0,s.AH)`
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
  `,D([(0,o.Fg)({context:m.B6,subscribe:!0}),(0,n.wk)()],I.prototype,"_darkMode",void 0),D([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],I.prototype,"_localize",void 0),D([(0,n.MZ)()],I.prototype,"oldValue",void 0),D([(0,n.MZ)()],I.prototype,"newValue",void 0),I=D([(0,n.EM)("esphome-yaml-diff")],I),i(2542);var j=i(8763),B=i(6910);let N=(0,s.AH)`
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
`,Z="cog-outline",K="memory",U="arrow-decision-outline";(0,k.C)({[Z]:r.mdiCogOutline,[K]:r.mdiMemory,[U]:r.mdiArrowDecisionOutline}),i(4636),i(7473);let V=(0,s.AH)`
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
`;var G=i(5660),H=i(325),W=i(8283),Y=i(3074);let Q=(0,s.AH)`
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
`;function J(e){return e.replace(/ (Component|Configuration)$/,"")||e}var X=i(6570);function ee(e){return e.name?e.name:e.title?C.TM.has(et(e.component_id))?J(e.title):e.title:e.id}function et(e){return(0,X.iZ)(e).domain}function ei(e,t){let i=e.parent_id?t.find(t=>t.id===e.parent_id):void 0;return i?`${e.component_id} \xb7 ${ee(i)}`:e.component_id}function ea(e){return!e.is_entity_container}function eo(e){return e.find(ea)}function er(e,t){return t?e.filter(e=>e.id===t.id||e.parent_id===t.id):e}function es(e,t){if(!t||!ea(t))return[];let i=et(t.component_id);return e.filter(e=>!e.is_device_level&&(e.applies_to.includes(t.component_id)||e.applies_to.includes(i)))}var en=i(8175);function el(){return{trigger_id:null,trigger_params:{},actions:[]}}function ed(e,t,i){if(0===t.length)return i&&"object"==typeof i&&!Array.isArray(i)?{...i}:{};let[a,...o]=t;if(0===o.length){if(void 0===i||""===i){let t={...e};return delete t[a],t}return{...e,[a]:i}}let r=e[a]&&"object"==typeof e[a]&&!Array.isArray(e[a])?e[a]:{};return{...e,[a]:ed(r,o,i)}}function ec(e,t,i){if(t<0||t>=e.length)return e;let a=e.slice();return a[t]=i,a}function eh(e,t){if(t<0||t>=e.length)return e;let i=e.slice();return i.splice(t,1),i}function ep(e,t,i){if(t<0||i<0||t>=e.length||i>=e.length||t===i)return e;let a=e.slice();return[a[t],a[i]]=[a[i],a[t]],a}function eu(e){return(0,en.wr)(e)?Number(e):null}function em(e){switch(e.kind){case"device_on":return void 0===e.index?`automation:device_on:${e.trigger}`:`automation:device_on:${e.trigger}:${e.index}`;case"component_on":return void 0===e.index?`automation:component_on:${e.component_id}:${e.trigger}`:`automation:component_on:${e.component_id}:${e.trigger}:${e.index}`;case"component_action":return`automation:component_action:${e.component_id}:${e.field}`;case"script":return`automation:script:${e.id}`;case"interval":return`automation:interval:${e.index}`;case"light_effect":return`automation:light_effect:${e.component_id}:${e.index}`;case"api_action":return`automation:api_action:${e.action_name}`}}function ev(e,t){let i=e.split("\n"),a=t.fromLine-1,o=Math.max(0,t.toLine-t.fromLine+1),r=t.replacement.endsWith("\n")?t.replacement.slice(0,-1):t.replacement,s=""===r?[]:r.split("\n");return[...i.slice(0,a),...s,...i.slice(a+o)].join("\n")}function eg(e){if(!e.startsWith("automation:"))return null;let t=e.split(":");switch(t[1]){case"device_on":if(!t[2])return null;if(3===t.length)return{kind:"device_on",trigger:t[2]};if(4===t.length){let e=eu(t[3]);return null===e?null:{kind:"device_on",trigger:t[2],index:e}}return null;case"component_on":if(!t[2]||!t[3])return null;if(4===t.length)return{kind:"component_on",component_id:t[2],trigger:t[3]};if(5===t.length){let e=eu(t[4]);return null===e?null:{kind:"component_on",component_id:t[2],trigger:t[3],index:e}}return null;case"component_action":return 4===t.length&&t[2]&&t[3]?{kind:"component_action",component_id:t[2],field:t[3]}:null;case"script":return t[2]?{kind:"script",id:t[2]}:null;case"interval":{let e=Number(t[2]);return Number.isFinite(e)?{kind:"interval",index:e}:null}case"light_effect":{let e=Number(t[3]);return t[2]&&Number.isFinite(e)?{kind:"light_effect",component_id:t[2],index:e}:null}case"api_action":return t[2]?{kind:"api_action",action_name:t[2]}:null;default:return null}}function ef(e,t,i,a){let o=ev(t,a);e.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:o},bubbles:!0,composed:!0})),e.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:em(i)},bubbles:!0,composed:!0}))}i(986),i(1604),i(2216);let e_=(0,s.AH)`
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
`;function eb(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}let ey={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1};class ew extends s.WF{render(){let{plan:e,order:t}=this._plan();return 0===t.length?(0,s.qy)`<p class="error" role="status">
        ${this._localize("device.automation_target_no_components")}
      </p>`:(0,s.qy)`<div class="field">
      <label class="field-label" id="component-target-label">
        ${this._localize("device.automation_wizard_pick_component")}
      </label>
      <div
        class="component-list"
        role="radiogroup"
        aria-labelledby="component-target-label"
        @keydown=${e=>this._onKeydown(e,t)}
      >
        ${e.map(e=>{if(!("header"in e))return this._renderChoice(e,t);let i=`component-group-${e.header.id}`;return(0,s.qy)`<div
            class="component-group-wrap"
            role="group"
            aria-labelledby=${i}
          >
            <p class="component-group" id=${i}>
              ${ee(e.header)}
              <span class="component-group-id">(${e.header.component_id})</span>
            </p>
            ${e.subs.map(e=>this._renderChoice(e,t))}
          </div>`})}
      </div>
    </div>`}_plan(){let e=new Set(this.devices.filter(e=>e.is_entity_container).map(e=>e.id)),t=new Map;for(let i of this.devices){if(!i.parent_id||!e.has(i.parent_id))continue;let a=t.get(i.parent_id)??[];a.push(i),t.set(i.parent_id,a)}let i=[],a=[];for(let o of this.devices)if(o.is_entity_container){let e=t.get(o.id)??[];if(0===e.length)continue;i.push({header:o,subs:e}),a.push(...e.map(e=>e.id))}else o.parent_id&&e.has(o.parent_id)||(i.push(o),a.push(o.id));return{plan:i,order:a}}_renderChoice(e,t){let i=e.id===this.value,a=i||!t.includes(this.value)&&t[0]===e.id;return(0,s.qy)`<div
      class="component-choice ${i?"component-choice--selected":""}"
      role="radio"
      aria-checked=${i?"true":"false"}
      aria-disabled=${this.disabled?"true":"false"}
      data-id=${e.id}
      tabindex=${a?"0":"-1"}
      @click=${()=>this._select(e.id)}
    >
      <span class="component-choice-name">${ee(e)}</span>
      <span class="component-domain">${e.component_id}</span>
    </div>`}_onKeydown(e,t){if(this.disabled||0===t.length)return;let i=e.target?.closest(".component-choice"),a=i?.dataset.id??null;if("Enter"===e.key||" "===e.key){a&&(e.preventDefault(),this._select(a));return}let o=ey[e.key]??0;if(0===o)return;e.preventDefault();let r=a?t.indexOf(a):-1,s=t[(r+o+t.length)%t.length];this._select(s),this.updateComplete.then(()=>{let e=this.shadowRoot?.querySelector(`.component-choice[data-id="${s}"]`);e?.focus()})}_select(e){this.disabled||this.dispatchEvent(new CustomEvent("component-change",{detail:{componentId:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.devices=[],this.value="",this.disabled=!1}}function e$(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ew.styles=[v.G,e_],eb([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ew.prototype,"_localize",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"devices",void 0),eb([(0,n.MZ)()],ew.prototype,"value",void 0),eb([(0,n.MZ)({type:Boolean})],ew.prototype,"disabled",void 0),ew=eb([(0,n.EM)("esphome-component-target-picker")],ew);class ex extends s.WF{open(e){this._prefilled=void 0!==e,this._kind=e?.kind??"device_on",this._componentId=e?.kind==="component_on"?e.componentId:"",this._prefillComponentId=this._componentId,this._triggerId=null,this._intervalValue="",this._intervalUnit="s",this._error="",this._dialog.open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration){this._loading=!0;try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml);let e=this._prefillContainer();e&&(this._componentId=this._available.devices.find(t=>t.parent_id===e.id)?.id??"")}catch(e){this._error=(0,W.u)(e)}finally{this._loading=!1}}}_prefillContainer(){if(!this._prefilled||"component_on"!==this._kind||!this._prefillComponentId)return;let e=this._available?.devices.find(e=>e.id===this._prefillComponentId);return e?.is_entity_container?e:void 0}render(){let e=this.boardName?this._localize("device.add_automation_dialog_title",{name:this.boardName}):this._localize("device.add_automation");return(0,s.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      ${this._loading&&!this._available?(0,s.qy)`<div style="text-align: center; padding: 32px;">
              <wa-spinner></wa-spinner>
            </div>`:this._renderForm()}
    </esphome-base-dialog>`}_renderForm(){let e=this._filteredTriggers(),t="interval"===this._kind,i=!this._prefilled,a=this._prefillContainer(),o="component_on"===this._kind&&(!this._prefilled||!!a),r=!!a&&!eo(er(this._available?.devices??[],a));return(0,s.qy)`
      <p class="intro">
        ${(0,B.Gc)(this._localize("device.automation_header_description"))}
      </p>
      ${i?(0,s.qy)`<div class="field">
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
            </div>`:s.s6}
      ${r?(0,s.qy)`<p class="field-desc">
              ${this._localize("device.automation_container_no_entities")}
            </p>`:(0,s.qy)`
              ${o?this._renderComponentRow(a):s.s6}
              ${"interval"===this._kind?this._renderIntervalRow():s.s6}
              ${!t?this._renderTriggerRow(e):s.s6}
            `}
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
    `}_renderComponentRow(e){let t=er(this._available?.devices??[],e);return(0,s.qy)`<esphome-component-target-picker
      .devices=${t}
      .value=${this._componentId}
      ?disabled=${this._saving}
      @component-change=${e=>this._onComponentChange(e.detail.componentId)}
    ></esphome-component-target-picker>`}_renderIntervalRow(){return(0,s.qy)`<div class="field">
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
          ${["us","ms","s","min","h","d"].map(e=>(0,s.qy)`<wa-option value=${e} ?selected=${e===this._intervalUnit}
                >${this._localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
    </div>`}_renderTriggerRow(e){if(0===e.length)return(0,s.qy)`<p class="error">
        ${this._localize("device.automation_trigger_none_available")}
      </p>`;let t=e.find(e=>e.id===this._triggerId);return(0,s.qy)`<div class="field">
      <label class="field-label" id="trigger-label">
        ${this._localize("device.automation_wizard_pick_trigger")}
      </label>
      <wa-select
        aria-labelledby="trigger-label"
        value=${this._triggerId??""}
        ?disabled=${this._saving}
        @change=${e=>this._triggerId=e.target.value}
      >
        ${e.map(e=>(0,s.qy)`<wa-option value=${e.id} ?selected=${e.id===this._triggerId}>
              ${e.name}
            </wa-option>`)}
      </wa-select>
      ${t?.description?(0,s.qy)`<p class="field-desc">${(0,B.Gc)(t.description)}</p>`:s.s6}
    </div>`}_filteredTriggers(){let e=this._available?.triggers??[];if("device_on"===this._kind){let t=this._existingDeviceTriggers();return e.filter(e=>e.is_device_level&&(!t.has(e.id)||e.supports_list))}if("component_on"===this._kind){let t=this._available?.devices.find(e=>e.id===this._componentId),i=this._existingComponentTriggers(this._componentId);return es(e,t).filter(e=>!i.has(this._bareTrigger(e.id))||e.supports_list)}return[]}_existingDeviceTriggers(){let e=new Set;for(let t of(0,C.vB)(this.yaml))"esphome"===t.parentKey&&t.eventKey&&e.add(t.eventKey);return e}_existingComponentTriggers(e){let t=new Set;for(let i of(0,C.vB)(this.yaml))i.id===e&&i.eventKey&&t.add(i.eventKey);return t}_bareTrigger(e){let t=e.indexOf(".");return t>=0?e.slice(t+1):e}_onKindChange(e){if(this._kind=e,this._triggerId=null,"component_on"===e){let e=this._available?.devices??[];this._componentId=eo(e)?.id??""}else this._componentId=""}_onComponentChange(e){this._componentId=e,this._triggerId=null}_canContinue(){return"interval"===this._kind?""!==this._intervalValue.trim():!!this._triggerId&&("component_on"!==this._kind||!!this._componentId)}_buildLocation(){if("device_on"===this._kind){let e=this._available?.triggers.find(e=>e.id===this._triggerId);if(e?.supports_list){let e=(0,C.vB)(this.yaml).filter(e=>"esphome"===e.parentKey&&e.eventKey===this._triggerId).length;return{kind:"device_on",trigger:this._triggerId,index:e}}return{kind:"device_on",trigger:this._triggerId}}if("component_on"===this._kind){let e=this._triggerId.indexOf("."),t=e>=0?this._triggerId.slice(e+1):this._triggerId,i=this._available?.triggers.find(e=>e.id===this._triggerId);if(i?.supports_list){let e=(0,C.vB)(this.yaml).filter(e=>e.id===this._componentId&&e.eventKey===t).length;return{kind:"component_on",component_id:this._componentId,trigger:t,index:e}}return{kind:"component_on",component_id:this._componentId,trigger:t}}return{kind:"interval",index:(0,C.vB)(this.yaml).filter(e=>"interval"===e.parentKey).length}}_catalogTriggerId(e){return"interval"===e.kind?null:this._triggerId}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new H.T(this),this._kind="device_on",this._componentId="",this._prefillComponentId="",this._triggerId=null,this._prefilled=!1,this._intervalValue="",this._intervalUnit="s",this._available=null,this._loading=!0,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e=this._buildLocation(),t={trigger_id:this._catalogTriggerId(e),trigger_params:"interval"===this._kind?{interval:`${this._intervalValue.trim()}${this._intervalUnit}`}:{},actions:[]},{yaml_diff:i}=await this._api.upsertAutomation(this.configuration,t,e,this.yaml);ef(this,this.yaml,e,i),this._dialog.open=!1}catch(t){let e=(0,Y.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}ex.styles=[v.G,G.z9,V,Q],e$([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ex.prototype,"_localize",void 0),e$([(0,o.Fg)({context:m.Ie})],ex.prototype,"_api",void 0),e$([(0,n.MZ)()],ex.prototype,"boardName",void 0),e$([(0,n.MZ)()],ex.prototype,"configuration",void 0),e$([(0,n.MZ)()],ex.prototype,"yaml",void 0),e$([(0,n.MZ)({attribute:!1})],ex.prototype,"board",void 0),e$([(0,n.wk)()],ex.prototype,"_kind",void 0),e$([(0,n.wk)()],ex.prototype,"_componentId",void 0),e$([(0,n.wk)()],ex.prototype,"_prefillComponentId",void 0),e$([(0,n.wk)()],ex.prototype,"_triggerId",void 0),e$([(0,n.wk)()],ex.prototype,"_prefilled",void 0),e$([(0,n.wk)()],ex.prototype,"_intervalValue",void 0),e$([(0,n.wk)()],ex.prototype,"_intervalUnit",void 0),e$([(0,n.wk)()],ex.prototype,"_available",void 0),e$([(0,n.wk)()],ex.prototype,"_loading",void 0),e$([(0,n.wk)()],ex.prototype,"_saving",void 0),e$([(0,n.wk)()],ex.prototype,"_error",void 0),ex=e$([(0,n.EM)("esphome-add-automation-dialog")],ex);var ek=i(6848),ez=i(6016),eC=i(5795),eq=i(4125);function eE(e){let t=new Set;if(!e)return t;for(let i of e.split("\n")){if(!/^\s/.test(i))continue;let e=(0,eq.KJ)(i,"id");null!==e&&t.add(e)}return t}var eS=i(8851),eA=((a={}).SENSOR="sensor",a.BINARY_SENSOR="binary_sensor",a.SWITCH="switch",a.LIGHT="light",a.FAN="fan",a.COVER="cover",a.CLIMATE="climate",a.BUTTON="button",a.NUMBER="number",a.SELECT="select",a.TEXT="text",a.TEXT_SENSOR="text_sensor",a.LOCK="lock",a.VALVE="valve",a.MEDIA_PLAYER="media_player",a.SPEAKER="speaker",a.MICROPHONE="microphone",a.CAMERA="camera",a.DISPLAY="display",a.TOUCHSCREEN="touchscreen",a.OUTPUT="output",a.DATETIME="datetime",a.EVENT="event",a.UPDATE="update",a.ALARM="alarm_control_panel",a.CORE="core",a.BUS="bus",a.AUTOMATION="automation",a.OTA="ota",a.TIME="time",a.AUDIO_ADC="audio_adc",a.AUDIO_DAC="audio_dac",a.CANBUS="canbus",a.INFRARED="infrared",a.MEDIA_SOURCE="media_source",a.MOTION="motion",a.ONE_WIRE="one_wire",a.PACKET_TRANSPORT="packet_transport",a.RADIO_FREQUENCY="radio_frequency",a.STEPPER="stepper",a.WATER_HEATER="water_heater",a.MISC="misc",a.FEATURED="featured",a);let eM=["core","ota","update"],eP=new(i(2342)).e,eL=new Set(Object.values(eA));function eF(e,t,i){if(0===e.length)return[];let a=i??(0,eS.Zn)(t),o=(0,eS.u)(t),r=new Set;for(let e of o){let t=e.indexOf(".");-1!==t&&r.add(e.slice(t+1))}return e.filter(e=>!a.has(e)&&(e.includes(".")?!o.has(e):!(!eL.has(e)&&r.has(e))))}async function eO(e,t,i,a){let o=new Set,r=t.filter(e=>!e.includes("."));return 0===r.length||await Promise.all(r.map(async t=>{var r,s;let n;for(let l of(await (r=a.platform??void 0,s=a.boardId??void 0,n=`${t}|${r??""}|${s??""}`,eP.fetch(n,()=>e.getComponents({provides:t,platform:r??void 0,board_id:s??void 0,limit:200}).then(e=>new Set(e.components.map(e=>e.id)))))))if(i.has(l)){o.add(t);break}})),o}var eR=i(4008),eT=i(7169),eD=i(4117);async function eI(e,t){if(e._submitting)return;let i=e._selected;e._submitError="";let a=++e._depNavSeq,o=null;try{o=await (0,eD.Sn)(e._api,t,e.platform||void 0,e.board?.id??void 0)}catch{o=null}if(a===e._depNavSeq){if(i&&(e._returnTo=i,e._depDomain=t),o){var r,s,n;let a,l=i?.bus_constraints?.[t],d=l?function(e,t){let i={},a=[],o={},r=t=>e.find(e=>e.key===t),s=null,n=null;for(let[e,l]of Object.entries(t)){if("min_frequency"===e){"number"==typeof l&&(s=l);continue}if("max_frequency"===e){"number"==typeof l&&(n=l);continue}if(e.startsWith("require_")){!0===l&&a.push(`${e.slice(8)}_pin`);continue}let t=r(e);if(!t)continue;if(Array.isArray(l)){let a=t.multi_value?[]:l.filter(e=>"string"==typeof e||"number"==typeof e);if(0===a.length)continue;o[e]=a;let r=a[0],s=t.default_value;(null==s||String(s)!==String(r))&&(i[e]=t.type===eR.Hh.STRING?String(r):r);continue}let d=t.default_value;(null==d||String(d)!==String(l))&&(i[e]=t.type===eR.Hh.STRING?String(l):l)}if(null!==s||null!==n){let e=r("frequency"),t=e?.unit_options?.length?e.unit_options:["Hz"],a=(0,eT.D6)(e?.default_value,t),o=null;null===a?o=n??s:null!==n&&a>n?o=n:null!==s&&a<s&&(o=s),null!==o&&(i.frequency=(0,eT.j1)(o,t))}if(0===Object.keys(i).length&&0===a.length&&0===Object.keys(o).length)return null;let l={fields:i,required:a};return Object.keys(o).length>0&&(l.optionOverrides=o),l}(o.config_entries,l):null,c=e.board?.featured_components?.find(e=>e.component_id===o.id);r=d,s=function(e){if(!e)return null;let t={};for(let[i,a]of Object.entries(e.fields))null!==a.value&&void 0!==a.value&&(t[i]=a.value);return Object.keys(t).length>0?{fields:t,required:[]}:null}(c),e._depPrefill=r?s?{fields:{...s.fields,...r.fields},required:[...r.required,...s.required],...r.optionOverrides?{optionOverrides:r.optionOverrides}:{}}:r:s,e._selected=c?(n=o,0===(a=new Set(Object.entries(c.fields).filter(([,e])=>e.locked).map(([e])=>e))).size?n:{...n,config_entries:n.config_entries.map(e=>a.has(e.key)?{...e,locked:!0}:e)}):o;return}e._selected=null,await e.updateComplete,a===e._depNavSeq&&e._catalog?.filterByDomain(t)}}async function ej(e,t,i){let a=++e._selectionSeq,o=i??e.board?.id??void 0;try{let i=await (0,eD.Sn)(e._api,t,e.platform||void 0,o);if(a!==e._selectionSeq)return{kind:"stale"};if(!i)return{kind:"error",message:e._localize("device.add_component_load_failed")};return{kind:"ok",entry:i}}catch(t){if(a!==e._selectionSeq)return{kind:"stale"};return{kind:"error",message:(0,Y.K)(t,e._localize,"device.add_component_error")}}}let eB=(0,s.AH)`
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
`;var eN=i(271);function eZ(e,t){let i={};for(let a of e){if(a.hidden)continue;let e=t[a.key];if(a.type===eR.Hh.NESTED){let t=a.config_entries??[];if(a.multi_value){let o=(0,en.ly)(e).map(e=>eZ(t,e)).filter(e=>Object.keys(e).length>0);o.length>0&&(i[a.key]=o);continue}let o=eZ(t,(0,en.qY)(e));Object.keys(o).length>0&&(i[a.key]=o);continue}if(void 0!==e){if(Array.isArray(e)){if(0===e.length)continue;i[a.key]=e;continue}if(""===e){a.required&&(i[a.key]=e);continue}if(a.type===eR.Hh.INTEGER&&"hex"!==a.display_format)i[a.key]=(0,eN.s)(e);else if(a.type===eR.Hh.FLOAT){let t="number"==typeof e?e:Number.parseFloat(String(e));Number.isNaN(t)||(i[a.key]=t)}else a.type===eR.Hh.BOOLEAN?i[a.key]=!0===(0,eS.FY)(e):i[a.key]=e}}return i}var eK=i(5957);let eU=new Set(["name"]);function eV(e,t={}){return{requiredOnly:e.requiredOnly,showAdvanced:e.showAdvanced,presentComponents:e.presentComponents,targetPlatform:e.board?.esphome.platform??null,...t}}function eG(e,t){let i=t[e.key];if(e.type===eR.Hh.NESTED)return e.multi_value?i instanceof eS.ho||Array.isArray(i)&&i.length>0:(0,en.Qd)(i)?(e.config_entries??[]).some(e=>eG(e,i)):void 0!==i;return void 0!==i}function eH(e,t,i){let a=[];for(let o of e)if((0,eK.VP)(o,t,i.presentComponents,i.targetPlatform)&&(!o.advanced||i.showAdvanced||eG(o,t))){if(o.type===eR.Hh.NESTED){if(!o.multi_value){let e=eH(o.config_entries??[],(0,en.qY)(t[o.key]),i),a=t[o.key],r="string"==typeof a||"number"==typeof a||"boolean"==typeof a;if(0===e.length&&!r)continue}}else if(i.requiredOnly&&!o.required&&!eU.has(o.key))continue;a.push(o)}return a}let eW=/^\*\*(Required —|Set at most one of:|Set together)/;function eY(e,t,i){let a=t.filter(e=>(0,eK.rf)(i[e])).length;switch(e){case"exactly_one":return 1===a;case"at_least_one":return a>=1;case"at_most_one":return a<=1;case"none_or_all":case"all_or_none":return 0===a||a===t.length}}let eQ=(0,s.AH)`
  .warning-banner {
    padding: var(--wa-space-s) var(--wa-space-m);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-warning-fill-quiet, #fff7e0);
    color: var(--wa-color-warning-text-quiet, #6b4f00);
    border-left: 3px solid var(--wa-color-warning-border-loud, #f0b400);
    font-size: var(--wa-font-size-s);
  }
`,eJ=(0,s.AH)`
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
`;var eX=i(1480),e0=i(615);function e1(e,t){if(e.translation_key){let i=e.translation_params||void 0,a=t(e.translation_key,i);if(a&&a!==e.translation_key)return a}return e.label?e.label:e.key.split("_").map(e=>e?e[0].toUpperCase()+e.slice(1):e).join(" ")}var e2=i(2748),e6=i(7967),e3=i(355),e4=i(5413),e5=i(9470);let e8=(0,s.AH)`
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
`,e9=(0,s.AH)`
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
`,e7=(0,s.AH)`
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
`,te=(0,s.AH)`
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
`;function tt({isLambda:e,disabled:t,localize:i,onSwitch:a}){return(0,s.qy)`
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
  `}let ti=(0,s.AH)`
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
`,ta=(0,s.AH)`
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
`,to=[v.G,G.z9,eQ,e9,e8,eX.a,te,e7,ti,ta];function tr(e,t){return t.disabled||e.locked}function ts(e,t){if(e.type===eR.Hh.INTEGER)return(0,eN.s)(t);if(e.type!==eR.Hh.FLOAT||""===t)return t;let i=Number(t);return Number.isFinite(i)?i:t}(0,k.C)({"alert-circle-outline":r.mdiAlertCircleOutline,"auto-fix":r.mdiAutoFix,"code-braces":r.mdiCodeBraces,"key-variant":r.mdiKeyVariant,"lock-outline":r.mdiLockOutline});let tn=e=>JSON.stringify(e),tl=e=>{try{let t=JSON.parse(e);if(Array.isArray(t))return t.map(String)}catch{}return e?e.split("."):[]};function td(e,t,i){if(!(0,e4.RB)(e))return s.s6;let a=(0,e4.rq)(e,t);if((0,e4.RB)(a)){let e=i("device.substitution_unresolved_hint");return(0,s.qy)`<span
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
    </span>`}let o=i("device.substitution_resolves_to");return(0,s.qy)`<span
    class="substitution-note"
    role="note"
    aria-label=${`${o}: ${a}`}
    title=${o}
  >
    <wa-icon library="mdi" name="code-braces"></wa-icon>
    <code>${a}</code>
  </span>`}function tc(e,t){return e1(e,t.localize)}function th(e,t){return e.help_link?(0,s.qy)`<a
    class="help-button"
    href=${e.help_link}
    target="_blank"
    rel="noreferrer"
    title=${t.localize("device.docs")}
  >
    <wa-icon library="mdi" name="open-in-new"></wa-icon>
  </a>`:s.s6}function tp(e,t,i={}){var a,o;let r,n,{includeHelpLink:l=!0}=i;return(0,s.qy)`
    <label class="field-label">
      ${tc(e,t)}
      ${e.required?(0,s.qy)`<span class="required">*</span>`:s.s6}
      ${e.locked?(0,s.qy)`<wa-icon
              class="lock-icon"
              library="mdi"
              name="lock-outline"
              title=${t.localize("device.field_locked_by_board")}
            ></wa-icon>`:s.s6}
      ${l&&e.help_link?th(e,t):s.s6}
    </label>
    ${a=e,o=t,r=a.description??"",(n=o.reactiveConstraintKeys?.has(a.key)?function(e){if(!e.startsWith("**"))return e;let t=e.split("\n\n"),i=0;for(;i<t.length&&eW.test(t[i].trim());)i++;return t.slice(i).join("\n\n").trim()}(r):r)?(0,s.qy)`<p class="field-description">${(0,B.Gc)(n)}</p>`:s.s6}
  `}function tu(e,t){let i=t.errorAt(e);return(0,e2.O)(i?t.localize(i.code,i.params):void 0)}function tm(e,t,i,a,o=s.s6){return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)} ${a} ${o} ${tu(t,i)}
    </div>
  `}function tv(e,t,i,a){return(0,en.k4)(a)?null:tg(e,t,i)}function tg(e,t,i){return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <p class="field-description">${i.localize("device.value_yaml_only")}</p>
      ${tu(t,i)}
    </div>
  `}function tf(e,t,i,a){let o,r=a.getAt(i),n=tv(e,i,a,r);if(n)return n;let l=String(r??""),d=null!==a.errorAt(i),c=String(e.default_value??""),h=tr(e,a),p="password"===t||(0,e6.Un)(a.sectionKey,e.key),u=(0,e3.D)(l),m=p&&null!==u,v=p?(0,e6.WA)(a.sectionKey,e.key,a.deviceName??"","password"===t,i):[],g=p?(0,s.qy)`<esphome-secret-picker
        ?full=${m}
        .disabled=${h}
        .fieldLabel=${tc(e,a)}
        .selectedKey=${u??""}
        .value=${l}
        .deviceName=${a.deviceName??""}
        .recommendedKeys=${v}
        @secret-selected=${e=>a.emitChange(i,e.detail.value)}
      ></esphome-secret-picker>`:s.s6,f=(0,e0.hp)(a.sectionKey,i)&&!m&&!h&&!(0,e4.R_)(l)&&!(0,e0.lk)(l),_=f?(0,s.qy)`<button
        type="button"
        class="generate-key"
        @click=${()=>a.emitChange(i,(0,e0.My)())}
      >
        <wa-icon library="mdi" name="auto-fix"></wa-icon>
        <span>${a.localize("device.generate_encryption_key")}</span>
      </button>`:s.s6,b=e=>m?g:p||f?(0,s.qy)`<div class="field-input-row">
            ${e}${g}${_}
          </div>`:e,y=g===s.s6?null===(o=(0,e3.D)(l))?s.s6:(0,s.qy)`<span class="secret-note">
    <wa-icon library="mdi" name="key-variant"></wa-icon>
    <span>${a.localize("device.value_from_secret")}</span>
    <code>${o}</code>
  </span>`:s.s6,w="password"===t?s.s6:td(l,a.substitutions,a.localize);if(e.suggestions&&e.suggestions.length>0){var $,x,k,z,C,q;let t,o;return $=e,x=i,k=l,z=d,C=h,q=a,t=k.toLowerCase(),o=String($.default_value??""),(0,s.qy)`
    <div class="field" data-field-key=${tn(x)}>
      ${tp($,q)}
      <wa-select
        class=${z?"invalid":""}
        ?disabled=${C}
        placeholder=${o}
        @change=${e=>q.emitChange(x,ts($,e.target.value))}
      >
        ${($.suggestions??[]).map(e=>{let i=String(e);return(0,s.qy)`<wa-option value=${i} ?selected=${i.toLowerCase()===t}
            >${i}</wa-option
          >`})}
      </wa-select>
      ${tu(x,q)}
    </div>
  `}if("password"===t){let t=(0,s.qy)`<esphome-password-input
      .value=${l}
      .invalid=${d}
      .disabled=${h}
      .placeholder=${c}
      @password-input-change=${e=>a.emitChange(i,e.detail.value)}
    ></esphome-password-input>`;return(0,s.qy)`
      <div class="field" data-field-key=${tn(i)}>
        ${tp(e,a)} ${b(t)} ${y}
        ${tu(i,a)}
      </div>
    `}let E=(0,e5.td)(l),S=(0,s.qy)`<input
    type=${t}
    autocomplete="off"
    class=${d?"invalid":""}
    .value=${E?(0,e5.kk)(l):l}
    ?disabled=${h}
    placeholder=${c}
    @input=${e=>{let t=e.target.value;a.emitChange(i,E?(0,e5.pV)(t):t)}}
  />`;return(0,s.qy)`
    <div class="field" data-field-key=${tn(i)}>
      ${tp(e,a)} ${b(S)} ${y} ${w}
      ${tu(i,a)}
    </div>
  `}function t_(e,t,i,a={}){let o=i.scopeValues(t);return(a.includeAdvanced?eH(e.config_entries??[],o,eV(i,{showAdvanced:!0})):i.filterRenderable(e.config_entries??[],o)).map(e=>i.renderEntry(e,[...t,e.key]))}function tb(e,t,i){let a=new Map(t.map(e=>[e.key,e])),o=e=>{let t=a.get(e);return t?tc(t,i):e},r=new Set,s=[];for(let i of e){let e=a.get(i)?.group;if(!e){s.push(o(i));continue}if(r.has(e))continue;r.add(e);let n=t.filter(t=>t.group===e).map(e=>o(e.key));s.push(n.length>1?`(${n.join(", ")})`:n[0])}return s.join(", ")}function ty(e,t){let i=new Map(e.members.map(e=>[e.key,e]));return(e.cardinality?.keys??[]).flatMap(a=>{let o=i.get(a);if(!o)return[];let r=o.group?e.members.filter(e=>e.group===o.group):[o];return[{id:r[0].key,members:r,label:r.map(e=>tc(e,t)).join(", ")}]})}function tw(e,t){let i=t.scopeValues([]),a=t.board?.esphome.platform??null,o=!e.cardinality||eY(e.cardinality.kind,e.cardinality.keys,i),r=eY("all_or_none",e.inclusiveKeys,i),n=!o&&e.cardinality?{kind:e.cardinality.kind,keys:e.cardinality.keys,satisfied:!1}:r?{kind:e.cardinality?.kind??"all_or_none",keys:e.cardinality?.keys??e.inclusiveKeys,satisfied:!0}:{kind:"all_or_none",keys:e.inclusiveKeys,satisfied:!1},l=t.localize(`device.constraint_${n.kind}`,{keys:tb(n.keys,t.entries??e.members,t)}),d=e.members.filter(e=>void 0!==t.getAt([e.key])||(0,eK.VP)(e,i,t.presentComponents,a));return d.length?(0,s.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${tn([e.members[0].key])}
    >
      <div class="constraint-cluster-header ${n.satisfied?"":"unsatisfied"}">
        ${n.satisfied?s.s6:(0,s.qy)`<wa-icon library="mdi" name="alert-circle-outline"></wa-icon>`}
        <span>${l}</span>
      </div>
      <div class="nested-fields">
        ${d.map(e=>t.renderEntry(e,[e.key]))}
      </div>
    </div>
  `:s.s6}let t$="__none__";function tx(e,t,i,a){let o=function(e){let t=new Map;for(let i of e)if(i.exclusive_group){let e=t.get(i.exclusive_group)??[];e.push(i),t.set(i.exclusive_group,e)}let i=new Set,a=[];for(let o of e)o.exclusive_group?i.has(o.exclusive_group)||(i.add(o.exclusive_group),a.push(t.get(o.exclusive_group))):a.push(o);return a}(e),{clusters:r,memberKeys:s}=function(e,t){let i=new Map(e.map(e=>[e.key,e])),a=new Map;for(let t of e)t.group&&!t.exclusive_group&&a.set(t.group,[...a.get(t.group)??[],t.key]);let o=[],r=new Set;for(let s of a.values()){let a=new Set(s),n=t.find(e=>e.keys.some(e=>a.has(e)));if(n)for(let e of n.keys)i.get(e)?.exclusive_group||a.add(e);let l=e.filter(e=>a.has(e.key));l.forEach(e=>r.add(e.key));let d=n?n.keys.filter(e=>l.some(t=>t.key===e)).length:0;o.push({members:l,cardinality:d>=2?n:void 0,inclusiveKeys:s})}return{clusters:o,memberKeys:r}}(e,i),n=new Set(eH(e.filter(e=>!e.exclusive_group&&!s.has(e.key)),t,a));return{ordered:o,clusters:r,memberKeys:s,visible:n}}function tk(e,t){let{entries:i,requiredGroups:a,values:o,presentComponents:r,targetPlatform:s,formatKeys:n}=e,l=[],d=new Map(i.map(e=>[e.key,e])),c=e=>e.some(e=>{let t=d.get(e);return void 0!==t&&(void 0!==(0,en.O6)(o,[e])||(0,eK.VP)(t,o,r,s))});for(let e of a)!e.keys.some(e=>t.has(e))&&c(e.keys)&&(eY(e.kind,e.keys,o)||l.push({kind:e.kind,keys:n(e.keys)}));let h=new Map;for(let e of i)e.group&&h.set(e.group,[...h.get(e.group)??[],e.key]);for(let e of h.values())!e.some(e=>t.has(e))&&c(e)&&(eY("all_or_none",e,o)||l.push({kind:"all_or_none",keys:n(e)}));return l}function tz(e,t){return eV({requiredOnly:!0,showAdvanced:!1,presentComponents:t,board:e})}function tC(e){let{entries:t,component:i,board:a,yaml:o,prefillReference:r,prefillFields:s,restoredValues:n,localize:l}=e,d=function e(t,i,a,o=!1){let r={};for(let s of t){if(s.type===eR.Hh.NESTED){let t=e(s.config_entries??[],i,a,o);s.required&&null!=s.platform_type&&void 0===t.name&&void 0===t.id&&(t.name=e1(s,a)),Object.keys(t).length>0&&(r[s.key]=t);continue}if(s.required||o&&s.from_preset){if(s.references_component&&!s.locked){let e=(0,X.Zm)(i,s.references_component,[]),t=(o&&s.from_preset&&"string"==typeof s.default_value&&e.some(e=>e.id===s.default_value)?s.default_value:void 0)??(0,X.z)(e,i)?.id;void 0!==t?r[s.key]=s.multi_value?[t]:t:s.multi_value&&s.required&&(r[s.key]=[]);continue}null!=s.default_value?r[s.key]=s.multi_value?Array.isArray(s.default_value)?[...s.default_value]:[String(s.default_value)]:s.default_value:s.multi_value&&s.required&&(r[s.key]=[])}}return r}(t,o,l,(0,eC.sO)(i.id)),c=d;if(t.find(e=>"id"===e.key&&e.type===eR.Hh.ID)&&void 0===c.id){let e=function(e,t,i){let a=!(0,eC.sO)(e)&&e.includes(".");if(!t&&!a)return null;let o=e.toLowerCase().replace(/[^a-z0-9_]+/g,"_"),r=1,s=`${o}_${r}`;for(;i.has(s);)r++,s=`${o}_${r}`;return s}(i.id,i.multi_conf,eE(o));null!==e&&(c={...c,id:e})}if(c=function(e,t,i,a){if(!i?.pins?.length||e.includes("."))return a;let o=a;for(let a of t){if(a.type!==eR.Hh.PIN||void 0!==o[a.key])continue;let t=a.key.toLowerCase().replace(/_(pin|gpio)$/,""),r=`${e}_${t}`,s=i.pins.find(e=>e.features.includes(r));s&&(o={...o,[a.key]:s.gpio})}return o}(i.id,t,a,c),n&&(c={...c,...n}),r){let e=function e(t,i,a,o={}){for(let r of t){if(r.type===eR.Hh.NESTED){let t=e(r.config_entries??[],i,[...a,r.key],o);if(t)return t;continue}if(r.references_component===i){let e=[...a,r.key];if(void 0!==(0,en.O6)(o,e))continue;return e}}return null}(t,r.domain,[],d);e&&(c=(0,en.Oe)(c,e,r.id))}return s&&(c={...c,...s}),c}let tq=new Set(["adc","dac","ota"]);function tE(e){return e?e.split("_").filter(e=>e.length>0).map(e=>tq.has(e.toLowerCase())?e.toUpperCase():e[0].toUpperCase()+e.slice(1)).join(" "):""}var tS=i(9023);class tA{hostConnected(){this._unsubscribe=(0,eD.Ej)(()=>{this._host.requestUpdate()})}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}resolve(e){return(0,eD.CQ)(e,this._getPlatform())?.name??e}kickoff(e){let t=this._getApi();if(!t)return;let i=this._getPlatform();for(let a of e)void 0===(0,eD.CQ)(a,i)&&(0,eD.Sn)(t,a,i).catch(()=>{})}constructor(e,t,i){this._host=e,this._getApi=t,this._getPlatform=i,e.addController(this)}}function tM(e,t){if(!t?.length)return e;let i=new Set(t);return e.map(e=>i.has(e.key)&&!e.required?{...e,required:!0}:e)}function tP(e,t){return t&&0!==Object.keys(t).length?e.map(e=>{let i=t[e.key];if(!i?.length||e.multi_value)return e;let a=new Map((e.options??[]).map(e=>[e.value,e]));return{...e,options:i.map(e=>a.get(String(e))??{label:String(e),value:String(e)}),default_value:e.type===eR.Hh.STRING?String(i[0]):i[0]}}):e}let tL=(0,s.AH)`
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
`;function tF(e,t){return t?e.find(e=>e.configuration===t)?.name??"":""}var tO=i(7064);let tR=(0,tO.Y)({name:"pin-registry-modes",fetch:e=>e.getPinRegistryModes(),fallback:e=>(console.warn("pin-registry-modes fetch failed; Mode flags unscoped",e),Object.create(null))});function tT(){return tR.getCached()}function tD(e){return tR.subscribe(e)}function tI(e){return tR.fetch(e)}class tj{hostConnected(){this._unsubscribe=this._binding.subscribe(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}hostUpdated(){if(this._kicked)return;let e=this._api();e&&(this._kicked=!0,this._binding.fetch(e))}get value(){return this._binding.getCached()}constructor(e,t,i){this._host=e,this._binding=t,this._api=i,this._kicked=!1,e.addController(this)}}class tB{hostUpdated(){this._syncRadioGroups()}reset(){this._choices.clear(),this._stash.clear()}getChoice(e){return this._choices.get(e)}setChoice(e,t){this._choices.set(e,t),this._host.requestUpdate()}getStash(e,t){return this._stash.get(`${e} ${t}`)}setStash(e,t,i){this._stash.set(`${e} ${t}`,i)}clearStash(e,t){this._stash.delete(`${e} ${t}`)}async _syncRadioGroups(){let e=this._host.shadowRoot;if(!e)return;let t=[...e.querySelectorAll("wa-radio-group")];if(0!==t.length)for(let e of(await Promise.all(t.map(e=>e.updateComplete?.catch(()=>{}))),t))e.syncRadioElements?.()}constructor(e){this._host=e,this._choices=new Map,this._stash=new Map,e.addController(this)}}let tN=["focusin","pointerdown","input","change"];class tZ{hostConnected(){for(let e of tN)this.host.addEventListener(e,this._onInteraction)}hostDisconnected(){for(let e of tN)this.host.removeEventListener(e,this._onInteraction)}constructor(e){this.host=e,this._onInteraction=e=>{var t,i,a;let o=e.composedPath().find(e=>e instanceof HTMLElement&&e.hasAttribute("data-field-key"));if(!o)return;let r=o.getAttribute("data-field-key")??"";if(!r.startsWith("["))return;let s=tl(r);if(!s.length)return;let{emit:n,focusedKey:l}=(t=e.type,i=tn(s),a=this._focusedKey,"change"===t?{emit:i===a,focusedKey:a}:{emit:"focusin"===t||i!==a,focusedKey:i});this._focusedKey=l,n&&this.host.dispatchEvent(new CustomEvent("field-focus",{detail:{path:s},bubbles:!0,composed:!0}))},e.addController(this)}}let tK="field--highlight";class tU{maybeScroll(e){let t=this.host.focusFieldPath,i=t?.length?tn(t):void 0,a=e.has("focusFieldPath")||e.has("entries")||e.has("values"),{gate:o,scroll:r}=function(e,t,i){let{scrolledKey:a,lastFocusKey:o,tries:r}=e;t!==o&&(o=t,a=void 0,r=0);let s=!!t&&a!==t&&r<3&&i;return s&&r++,{gate:{scrolledKey:a,lastFocusKey:o,tries:r},scroll:s}}({scrolledKey:this._scrolledKey,lastFocusKey:this._lastFocusKey,tries:this._tries},i,a);this._scrolledKey=o.scrolledKey,this._lastFocusKey=o.lastFocusKey,this._tries=o.tries,r&&t?.length&&i&&this._scrollTo(t,i)}async _scrollTo(e,t){var i;let{host:a}=this;if(!a.shadowRoot)return;for(let t=1;t<e.length;t++)a.openNested(e.slice(0,t).join("."));for(let t of(i=this._gatingDecls(a.shadowRoot),i.filter(t=>t.prefix.length>0&&t.prefix.length<e.length&&t.prefix.every((t,i)=>t===e[i])).map(e=>e.key)))a.openNested(t);await a.updateComplete;let o=a.focusFieldPath;if(o&&tn(o)===t)for(let i=e.length;i>=1;i--){let o=this._find(a.shadowRoot,e.slice(0,i));if(!o)continue;o.scrollIntoView({block:"center"});let r=tn(e.slice(0,i)),s=Date.now();!window.matchMedia?.("(prefers-reduced-motion: reduce)").matches&&(r!==this._lastFlashKey||s-this._lastFlashAt>1e4)&&(this._lastFlashKey=r,this._lastFlashAt=s,o.classList.remove(tK),o.offsetWidth,o.classList.add(tK),o.addEventListener("animationend",()=>o.classList.remove(tK),{once:!0})),i===e.length&&(this._scrolledKey=t);return}}_gatingDecls(e){let t=[];for(let i of e.querySelectorAll("[data-reveal-for]")){let e=i.getAttribute("data-field-key");e&&t.push({prefix:tl(i.getAttribute("data-reveal-for")??""),key:e})}return t}_find(e,t){for(let i of e.querySelectorAll("[data-field-key]")){let e=tl(i.getAttribute("data-field-key")??"");if(e.length===t.length&&e.every((e,i)=>e===t[i]))return i}for(let i of e.querySelectorAll("*")){if(!i.localName.includes("-"))continue;let e=i.shadowRoot,a=e?this._find(e,t):null;if(a)return a}return null}constructor(e){this.host=e,this._lastFlashAt=0,this._tries=0}}i(1062),i(2462),i(945),i(6135);var tV=i(9665);let tG=(0,s.AH)`
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
`;function tH(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({close:r.mdiClose,magnify:r.mdiMagnify,palette:r.mdiPalette});let tW=null;function tY(e){return e?e.startsWith("mdi:")?e.slice(4):e:""}class tQ extends s.WF{connectedCallback(){super.connectedCallback(),document.addEventListener("click",this._onDocumentClick,!0)}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("click",this._onDocumentClick,!0)}willUpdate(e){e.has("_open")&&this._escape.set(this._open),e.has("value")&&!this._loaded&&tY(this.value)&&this._ensureCatalogLoaded()}async _toggle(){this.disabled||(this._open?this._close():await this._openPanel())}async _openPanel(){this._open=!0,this.setAttribute("open",""),await this._ensureCatalogLoaded(),await this.updateComplete,this._searchInput?.focus()}async _ensureCatalogLoaded(){this._loaded||(this._catalog=await (tW||(tW=(async()=>{let e=await Promise.resolve().then(i.bind(i,9165)),t=[];for(let[i,a]of Object.entries(e)){if(!i.startsWith("mdi")||"string"!=typeof a)continue;let e=i.slice(3);if(!e)continue;let o=e.replace(/^[A-Z]/,e=>e.toLowerCase()).replace(/([A-Z])/g,"-$1").replace(/_/g,"-").toLowerCase();t.push({name:o,path:a})}return t.sort((e,t)=>e.name.localeCompare(t.name)),t})().catch(e=>(console.error("[mdi-icon-picker] failed to load catalog:",e),tW=null,[])))),this._loaded=!0)}_close(){this._open=!1,this.removeAttribute("open"),this._query=""}_select(e){let t=`mdi:${e}`;this.value=t,this.dispatchEvent(new CustomEvent("change",{detail:{value:t},bubbles:!0,composed:!0})),this._close()}_clear(e){e.stopPropagation(),this.value="",this.dispatchEvent(new CustomEvent("change",{detail:{value:""},bubbles:!0,composed:!0}))}_onSearchInput(e){this._query=e.target.value}_renderTriggerIcon(){let e=tY(this.value);if(!e)return(0,s.qy)`<span class="trigger-icon trigger-icon--empty">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${r.mdiPalette}></path>
        </svg>
      </span>`;let t=this._catalog.find(t=>t.name===e);return t?(0,s.qy)`<span class="trigger-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${t.path}></path>
        </svg>
      </span>`:(0,s.qy)`<span class="trigger-icon">
      <wa-icon library="mdi" name=${e} style="font-size: 16px;"></wa-icon>
    </span>`}_renderPanel(){if(!this._loaded)return(0,s.qy)`<div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="loading">Loading icons…</div>
      </div>`;let e=function(e,t){if(!t)return e.slice(0,400);let i=t.trim().toLowerCase().replace(/\s+/g,"-");if(!i)return e.slice(0,400);let a=[],o=[],r=[];for(let t of e)if(t.name===i?a.push(t):t.name.startsWith(i)?o.push(t):t.name.includes(i)&&r.push(t),a.length+o.length+r.length>=800)break;return[...a,...o,...r].slice(0,400)}(this._catalog,this._query),t=tY(this.value);return(0,s.qy)`
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
          ${0===e.length?(0,s.qy)`<div class="empty">
                  <wa-icon
                    library="mdi"
                    name="magnify"
                    style="font-size: 24px;"
                  ></wa-icon>
                  No icons match “${this._query}”
                </div>`:(0,s.qy)`<div class="grid">
                  ${e.map(e=>(0,s.qy)`
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
          ${t?(0,s.qy)`<span class="footer-name">mdi:${t}</span>`:s.s6}
        </div>
      </div>
    `}render(){let e=tY(this.value),t=`trigger${this.invalid?" invalid":""}`;return(0,s.qy)`
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
        ${e&&!this.disabled?(0,s.qy)`<span
                class="trigger-clear"
                role="button"
                tabindex="-1"
                title="Clear"
                @click=${this._clear}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
                  <path fill="currentColor" d=${r.mdiClose}></path>
                </svg>
              </span>`:s.s6}
        <svg class="trigger-chevron" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M7,10L12,15L17,10H7Z"></path>
        </svg>
      </button>
      ${this._open?this._renderPanel():s.s6}
    `}constructor(...e){super(...e),this.value="",this.placeholder="Choose an icon…",this.invalid=!1,this.disabled=!1,this._open=!1,this._catalog=[],this._query="",this._loaded=!1,this._escape=new tV.u(this,e=>{e.stopPropagation(),this._close()},{target:document}),this._onDocumentClick=e=>{!this._open||e.composedPath().includes(this)||this._close()}}}tQ.styles=[G.z9,tG],tH([(0,n.MZ)()],tQ.prototype,"value",void 0),tH([(0,n.MZ)()],tQ.prototype,"placeholder",void 0),tH([(0,n.MZ)({type:Boolean})],tQ.prototype,"invalid",void 0),tH([(0,n.MZ)({type:Boolean})],tQ.prototype,"disabled",void 0),tH([(0,n.wk)()],tQ.prototype,"_open",void 0),tH([(0,n.wk)()],tQ.prototype,"_catalog",void 0),tH([(0,n.wk)()],tQ.prototype,"_query",void 0),tH([(0,n.wk)()],tQ.prototype,"_loaded",void 0),tH([(0,n.P)(".search-input")],tQ.prototype,"_searchInput",void 0),tQ=tH([(0,n.EM)("esphome-mdi-icon-picker")],tQ);let tJ=(0,s.AH)`
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
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .option--active {
    background: var(--esphome-tint, var(--wa-color-surface-border));
  }

  .option-label {
    display: block;
  }
`;function tX(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}i(7982),(0,k.C)({"chevron-down":r.mdiChevronDown});class t0 extends s.WF{render(){let e=this._filtered,t=this._open?this._query:this.value,i=this._open&&e.length>0,a=i&&this._active>=0&&this._active<e.length?`option-${this._active}`:s.s6;return(0,s.qy)`
      <wa-popup placement="bottom-start" sync="width" distance="4" ?active=${i}>
        <div slot="anchor" class="control">
          <input
            type="text"
            class=${this.invalid?"invalid":""}
            role="combobox"
            aria-autocomplete="list"
            aria-invalid=${this.invalid?"true":s.s6}
            aria-expanded=${i?"true":"false"}
            aria-controls=${i?"listbox":s.s6}
            aria-activedescendant=${a}
            aria-label=${this.label||s.s6}
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
        ${i?(0,s.qy)`<div
                id="listbox"
                class="listbox"
                role="listbox"
                @mousedown=${this._preventBlur}
              >
                ${e.map((e,t)=>(0,s.qy)`<div
                      id="option-${t}"
                      class="option ${t===this._active?"option--active":""}"
                      role="option"
                      aria-selected=${e.value===this.value?"true":"false"}
                      @mousedown=${this._preventBlur}
                      @click=${()=>this._select(e)}
                      @mouseenter=${()=>this._active=t}
                    >
                      ${this._isDefault(e)?(0,s.qy)`<span class="option-default-stack">
                              <span class="option-label">${e.label}</span>
                              <small class="option-default-note"
                                >${this.defaultNote}</small
                              >
                            </span>`:(0,s.qy)`<span class="option-label">${e.label}</span>`}
                    </div>`)}
              </div>`:s.s6}
      </wa-popup>
    `}_isDefault(e){return""!==this.defaultNote&&""!==this.defaultValue&&e.value.toLowerCase()===this.defaultValue.toLowerCase()}get _filtered(){if(!this._dirty)return this.options;let e=this._query.trim().toLowerCase();return e?this.options.filter(t=>t.value.toLowerCase().includes(e)||t.label.toLowerCase().includes(e)):this.options}_select(e){this.value=e.value,this._query=e.value,this._emit(e.value),this._close()}_emit(e){this.dispatchEvent(new CustomEvent("options-combobox-change",{detail:{value:e},bubbles:!1,composed:!1}))}_scrollActiveIntoView(){this.updateComplete.then(()=>this._activeOption?.scrollIntoView({block:"nearest"}))}constructor(...e){super(...e),this.options=[],this.value="",this.placeholder="",this.disabled=!1,this.invalid=!1,this.label="",this.defaultValue="",this.defaultNote="",this._open=!1,this._query="",this._dirty=!1,this._active=-1,this._committed="",this._open_=()=>{this.disabled||this._open||(this._open=!0,this._committed=this.value,this._query=this.value,this._dirty=!1,this._active=this.options.findIndex(e=>e.value===this.value),this._active>=0&&this._scrollActiveIntoView())},this._close=()=>{this._open=!1,this._active=-1,this._dirty=!1},this._toggle=()=>{this.disabled||(this._open?this._close():(this._open_(),this._input?.focus()))},this._preventBlur=e=>e.preventDefault(),this._onInput=e=>{let t=e.target.value;this._query=t,this._dirty=!0,this._open=!0,this._active=-1,this._emit(t)},this._onKeyDown=e=>{let t=this._filtered;switch(e.key){case"ArrowDown":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active>=t.length-1?0:this._active+1,this._scrollActiveIntoView());break;case"ArrowUp":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active<=0?t.length-1:this._active-1,this._scrollActiveIntoView());break;case"Enter":this._open&&this._active>=0&&t[this._active]?(e.preventDefault(),this._select(t[this._active])):this._close();break;case"Escape":this._open&&(e.preventDefault(),e.stopPropagation(),this.value=this._committed,this._query=this._committed,this._emit(this._committed),this._close());break;case"Tab":this._close()}}}}t0.styles=[G.z9,tJ],tX([(0,n.MZ)({attribute:!1})],t0.prototype,"options",void 0),tX([(0,n.MZ)()],t0.prototype,"value",void 0),tX([(0,n.MZ)()],t0.prototype,"placeholder",void 0),tX([(0,n.MZ)({type:Boolean})],t0.prototype,"disabled",void 0),tX([(0,n.MZ)({type:Boolean})],t0.prototype,"invalid",void 0),tX([(0,n.MZ)()],t0.prototype,"label",void 0),tX([(0,n.MZ)()],t0.prototype,"defaultValue",void 0),tX([(0,n.MZ)()],t0.prototype,"defaultNote",void 0),tX([(0,n.wk)()],t0.prototype,"_open",void 0),tX([(0,n.wk)()],t0.prototype,"_query",void 0),tX([(0,n.wk)()],t0.prototype,"_dirty",void 0),tX([(0,n.wk)()],t0.prototype,"_active",void 0),tX([(0,n.P)("input")],t0.prototype,"_input",void 0),tX([(0,n.P)(".option--active")],t0.prototype,"_activeOption",void 0),t0=tX([(0,n.EM)("esphome-options-combobox")],t0);let t1="__esphome_add_new__";var t2=i(410);let t6={INPUT:{input:!0},OUTPUT:{output:!0},INPUT_PULLUP:{input:!0,pullup:!0},OUTPUT_OPEN_DRAIN:{output:!0,open_drain:!0},INPUT_PULLDOWN_16:{input:!0,pulldown:!0},INPUT_PULLDOWN:{input:!0,pulldown:!0},INPUT_OUTPUT_OPEN_DRAIN:{input:!0,output:!0,open_drain:!0}};function t3(e){let t=t6[e.toUpperCase()];return t?{...t}:null}var t4=i(1376);let t5=new WeakMap;function t8(e,t,i){let a=i.getAt(t);if(!e.multi_value&&("string"==typeof a||"number"==typeof a||"boolean"==typeof a))return(0,s.qy)`
      <div class="field" data-field-key=${tn(t)}>
        ${tp(e,i)}
        <p class="field-description">
          ${i.localize("device.value_set_in_yaml",{value:String(a)})}
        </p>
        ${tu(t,i)}
      </div>
    `;let o=t.join(".");(e.required||(0,eS.$z)(a))&&i.seedNestedOpen(o);let r=i.nestedOpenSections.has(o),n=null!=e.platform_type&&!e.required,l=n&&(0,eS.$z)(i.getAt(t)),d=tc(e,i),c=i.localize("device.enable_entity",{name:d});return(0,s.qy)`
    <div class="nested-group" data-field-key=${tn(t)}>
      <div class="nested-header">
        ${n?(0,s.qy)`<wa-switch
                class="nested-enable"
                .checked=${l}
                ?disabled=${tr(e,i)}
                aria-label=${c}
                title=${c}
                @change=${e=>(function(e,t,i,a,o,r){let s,n=((s=t5.get(r.stashOwner))||(s=new Map,t5.set(r.stashOwner,s)),s);if(a){let a=n.get(t);a&&(0,eS.$z)(a)?(n.delete(t),r.emitChange(e,a)):r.emitChange([...e,"name"],o),i||r.toggleNested(t)}else{let a=r.getAt(e);(0,en.Qd)(a)&&(0,eS.$z)(a)&&n.set(t,a),r.emitChange(e,void 0),i&&r.toggleNested(t)}})(t,o,r,e.target.checked,d,i)}
              ></wa-switch>`:s.s6}
        <button
          type="button"
          class="nested-toggle"
          aria-expanded=${r}
          @click=${()=>i.toggleNested(o)}
        >
          <wa-icon library="mdi" name=${r?"chevron-up":"chevron-down"}></wa-icon>
          <span class="nested-title">${d}</span>
          ${e.platform_type?(0,s.qy)`<span class="nested-platform">${e.platform_type}</span>`:s.s6}
        </button>
        ${th(e,i)}
      </div>
      ${e.description?(0,s.qy)`<p class="nested-desc">${(0,B.Gc)(e.description)}</p>`:s.s6}
      ${r?(0,s.qy)`<div class="nested-fields">${t_(e,t,i)}</div>`:s.s6}
    </div>
  `}var t9=i(5089),t7=i(2477),ie=i(5490);let it=["us","ms","s","min","h","d"],ii={us:"us",µs:"us",microseconds:"us",ms:"ms",milliseconds:"ms",s:"s",sec:"s",seconds:"s",min:"min",minutes:"min",h:"h",hours:"h",d:"d",days:"d"},ia=Object.keys(ii).map(e=>e.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|"),io=RegExp(`^(\\d+(?:\\.\\d+)?)\\s*(${ia})?$`),ir=RegExp(`^\\d+(?:\\.\\d+)?\\s*(?:${ia})$`);function is(e){return"string"==typeof e&&ir.test(e.trim())}function il(e){if(null==e||""===e)return{value:"",unit:"s",parseable:!0};let t=String(e).trim(),i=t.match(io);if(i){let[,e,t]=i;return{value:e,unit:t?ii[t]:"s",parseable:!0}}return{value:t,unit:"s",parseable:!1}}function id(e,t){let i=e.trim();return""===i?"":`${i}${t}`}function ic(e){return null==e||""===e?"":(0,ie.uS)(e)||String(e)}let ih=new WeakMap;function ip(e,t,i){let a=i.getAt(t),o=tv(e,t,i,a);if(o)return o;let r=null==a?e.default_value:a,n=!0===(0,eS.FY)(r);return(0,s.qy)`
    <div class="switch-field" data-field-key=${tn(t)}>
      <div class="field-info">${tp(e,i,{includeHelpLink:!1})}</div>
      ${th(e,i)}
      <wa-switch
        ?checked=${n}
        ?disabled=${tr(e,i)}
        aria-label=${tc(e,i)}
        @change=${e=>i.emitChange(t,e.target.checked)}
      ></wa-switch>
    </div>
  `}function iu(e,t,i=""){if(!t)return e;let a=i.toLowerCase(),o=e.filter(e=>!e.variants?.length||e.variants.includes(t)||e.value.toLowerCase()===a);return o.length>0?o:e}function im(e,t){let i="string"==typeof e?e.trim():(0,en.Qd)(e)&&"string"==typeof e.number?e.number.trim():"";if(!i)return null;let a=i.toLowerCase(),o=t.find(e=>e.aliases?.some(e=>e.toLowerCase()===a));return o?o.gpio:null}function iv(e,t){return(0,s.qy)`<wa-option
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
        ${e.warn?(0,s.qy)`<wa-icon
                class="pin-warn-icon"
                library="mdi"
                name="alert-circle-outline"
              ></wa-icon>`:s.s6}
      </span>
      ${e.secondary?(0,s.qy)`<span class="pin-option-secondary">${e.secondary}</span>`:s.s6}
    </span>
  </wa-option>`}function ig(e,t,i,a,o,r){let n=i.filterRenderable(e.config_entries??[],i.scopeValues(t));if(0===n.length)return s.s6;let l=`${t.join(".")}:pin-advanced`,d=i.scopeValues(t);o&&Object.keys(d).some(e=>"number"!==e&&void 0!==d[e])&&i.seedNestedOpen(l);let c=i.nestedOpenSections.has(l);return(0,s.qy)`
    <div
      class="pin-advanced"
      data-field-key="${l}"
      data-reveal-for="${tn(t)}"
    >
      ${(0,t4.u)({open:c,onToggle:()=>{!r&&(i.toggleNested(l),c||o||null==a||""===a||i.emitChange(t,{number:a}))},localize:i.localize,labelKey:"device.pin_advanced",variant:"quiet",iconBefore:!0,disabled:r,body:()=>(0,s.qy)`${n.map(e=>(function(e,t,i){var a,o,r,s,n,l,d,c;let h,p,u,m,v,g,f;if("mode"!==e.key||e.type!==eR.Hh.NESTED)return i.renderEntry(e,[...t,e.key]);let _=[...t,e.key],b=i.getAt(_),y=function(e,t){if(!t||!(0,en.Qd)(e))return null;for(let i of Object.keys(e))if(Object.prototype.hasOwnProperty.call(t,i)){let e=t[i];return e.length>0?e:null}return null}(i.getAt(t),i.pinRegistryModes),w=y?(o=e,h=new Set([...y,..."string"==typeof(a=b)?Object.keys(t3(a)??{}):(0,en.Qd)(a)?Object.keys(a):[]]),p=(o.config_entries??[]).filter(e=>h.has(e.key)),{...o,config_entries:p}):e;return"string"==typeof b?(r=w,s=_,(m="string"==typeof(u=(n=i).getAt(s))?t3(u):null)?t8(r,s,(l=n,d=s,c=m,v=d.join("."),g=e=>e.length===d.length+1&&e.slice(0,d.length).join(".")===v?e[d.length]:null,(f={...l,getAt:e=>{if(e.join(".")===v)return c;let t=g(e);return null!==t?c[t]:l.getAt(e)},scopeValues:e=>e.join(".")===v?{...c}:l.scopeValues(e),emitChange:(e,t)=>{let i=g(e);if(null===i)return void l.emitChange(e,t);let a={...c};t?a[i]=!0:delete a[i],l.emitChange(d,a)}}).renderEntry=(e,t)=>e.type===eR.Hh.BOOLEAN?ip(e,t,f):l.renderEntry(e,t),f)):t8(r,s,n)):i.renderEntry(w,_)})(e,t,i))}`})}
    </div>
  `}var i_=i(8067);function ib(e,t){let i=e.getAt(t);return Array.isArray(i)?i:[]}function iy(e,t,i){return{addItem:()=>e.emitChange(t,[...ib(e,t),i()]),removeAt:i=>e.emitChange(t,ib(e,t).filter((e,t)=>t!==i))}}function iw(e,t){return 0===e.length?(0,s.qy)`<p class="field-description">${t.localize("device.multi_value_empty")}</p>`:s.s6}function i$(e,t,i){return(0,s.qy)`
    <button
      type="button"
      class="multi-btn"
      ?disabled=${t}
      aria-label=${e.localize("device.multi_value_remove")}
      @click=${i}
    >
      <wa-icon library="mdi" name="close"></wa-icon>
    </button>
  `}function ix(e,t,i){return(0,s.qy)`
    <button
      type="button"
      class="multi-btn multi-add"
      ?disabled=${t}
      @click=${i}
    >
      <wa-icon library="mdi" name="plus"></wa-icon>
      ${e.localize("device.multi_value_add")}
    </button>
  `}let ik=new(i(2741)).E({name:"automation-body-cache",bucketKey:()=>"",cacheMisses:!1,fetch:(e,t)=>{let i=t.map(e=>{let t=e.indexOf("/");return{type:e.slice(0,t),id:e.slice(t+1)}});return e.getAutomationBodies(i)}});function iz(e,t,i){return ik.fetch(e,`${t}/${i}`,void 0)}async function iC(e,t,i,a=iz){let o=await a(e,t,i.id);if(o&&"config_entries"in o)return i.config_entries=structuredClone(o.config_entries),"ok";let r=null===o?"no body returned":"body shape missing config_entries";return console.warn(`automation-body: ${t}/${i.id} ${r}; form will render empty`),null===o?"missingBody":"missingField"}function iq(){return{succeeded:0,missingBody:0,missingField:0,rejected:0}}function iE(e,t){e["ok"===t?"succeeded":t]++}function iS(e,t){return`${e??""}|${t??""}`}let iA={triggers:(0,tO.Y)({name:"automation-catalog-cache:triggers",key:iS,fetch:(e,t,i)=>e.getAutomationTriggers(t,i)}),actions:(0,tO.Y)({name:"automation-catalog-cache:actions",key:iS,fetch:(e,t,i)=>e.getAutomationActions(t,i)}),conditions:(0,tO.Y)({name:"automation-catalog-cache:conditions",key:iS,fetch:(e,t,i)=>e.getAutomationConditions(t,i)}),light_effects:(0,tO.Y)({name:"automation-catalog-cache:light_effects",key:iS,fetch:(e,t,i)=>e.getLightEffects(t,i)}),filters:(0,tO.Y)({name:"automation-catalog-cache:filters",key:iS,fetch:(e,t,i)=>e.getFilters(t,i)})};function iM(e,t){return iA.triggers.getCached(e,t)}async function iP(e,t,i){let a=await iA.light_effects.fetch(e,t,i);return iF("light_effects",t,i,a,t=>iR(e,"light_effects",t))}async function iL(e,t,i){let a=await iA.filters.fetch(e,t,i);return iF("filters",t,i,a,t=>iR(e,"filters",t))}async function iF(e,t,i,a,o){if(0===(await o(a)).succeeded)return a;let r=[...a];return iA[e].update(r,t,i),r}let iO=new WeakSet;async function iR(e,t,i){let a=iq(),o=i.filter(e=>!iO.has(e));if(0===o.length)return a;for(let i of(await Promise.allSettled(o.map(async i=>{let o=await iC(e,t,i);"ok"===o&&iO.add(i),iE(a,o)}))))"rejected"===i.status&&(a.rejected++,console.warn(`${t} hydration failed`,i.reason));let r=a.missingBody+a.missingField+a.rejected;return r>0&&console.warn(`${t} hydration: ${a.succeeded} ok, ${r} failed (missingBody=${a.missingBody}, missingField=${a.missingField}, rejected=${a.rejected})`),a}function iT(e){let t=Object.values(iA).map(t=>t.subscribe(e));return()=>{for(let e of t)e()}}var iD=i(8339);function iI(e){let t=Object.keys(e);return 1===t.length?t[0]:""}function ij(e){return e?e.replace(/_/g," ").replace(/\b\w/g,e=>e.toUpperCase()):""}let iB={time_period:eR.Hh.TIME_PERIOD,float:eR.Hh.FLOAT,integer:eR.Hh.INTEGER,string:eR.Hh.STRING,lambda:eR.Hh.LAMBDA},iN={light_effects:{cache:()=>iA.light_effects.getCached(void 0,void 0),fetch:e=>iP(e),parentToken:e=>e,dedupByTypeId:!0},filter:{cache:()=>iA.filters.getCached(void 0,void 0),fetch:e=>iL(e),parentToken:e=>e.split(".",1)[0],dedupByTypeId:!1}};function iZ(e){return Array.isArray(e)?e:[]}function iK(e){let t=[],i=[];return e.forEach((e,a)=>{!(null===e||"object"!=typeof e||Array.isArray(e))&&Object.keys(e).length<=1&&(t.push(e),i.push(a))}),{items:t,positions:i}}function iU(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}class iV extends s.WF{connectedCallback(){super.connectedCallback();let e=this._ops();if(null===e)return;this._unsubscribe=iT(()=>{if(!this.isConnected)return;let e=this._ops();if(null===e)return;let t=e.cache();void 0!==t&&(this._catalog=t,this._fetchError=!1)});let t=e.cache();this._fetchError=!1,void 0!==t?this._catalog=t:this._kickFetch(e)}updated(){if(this._kickedFetch||null!==this._catalog||this._fetchError||!this._api)return;let e=this._ops();null!==e&&void 0===e.cache()&&this._kickFetch(e)}_kickFetch(e){this._api&&(this._kickedFetch=!0,e.fetch(this._api).catch(e=>{console.error("Failed to fetch registry catalog",e),this.isConnected&&(this._fetchError=!0)}))}_ops(){return iN[this.entry?.registry??""]??null}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe?.(),this._unsubscribe=void 0,this._kickedFetch=!1}render(){let e=this._ops();if(null===e)return(0,s.qy)`
        <div class="field" data-field-key=${tn(this.path)}>
          ${tp(this.entry,this.ctx)}
          <p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_unsupported")}
          </p>
          ${tu(this.path,this.ctx)}
        </div>
      `;let t=this.ctx.getAt(this.path);if(t instanceof eS.ho||void 0!==t&&!Array.isArray(t))return(0,s.qy)`
        <div class="field" data-field-key=${tn(this.path)}>
          ${tp(this.entry,this.ctx)}
          <p class="field-description">
            ${this.ctx.localize("device.multi_value_yaml_only")}
          </p>
          ${tu(this.path,this.ctx)}
        </div>
      `;let{items:i}=iK(iZ(t)),a=tr(this.entry,this.ctx),o=this.ctx.sectionKey?e.parentToken(this.ctx.sectionKey):"",r=(this._catalog??[]).filter(e=>!o||0===e.applies_to.length||e.applies_to.includes(o)),n=null!==this._catalog&&0===this._catalog.length,l=this._fetchError?(0,s.qy)`<p class="registry-list-fallback">
          ${this.ctx.localize("device.registry_list_error")}
          ${this._api?(0,s.qy)`<button type="button" class="multi-btn" @click=${this._retryFetch}>
                  ${this.ctx.localize("device.registry_list_retry")}
                </button>`:s.s6}
        </p>`:null===this._catalog?(0,s.qy)`<p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_loading")}
          </p>`:n?(0,s.qy)`<p class="registry-list-fallback">
              ${this.ctx.localize("device.registry_list_empty_catalog")}
            </p>`:0===r.length?(0,s.qy)`<p class="registry-list-fallback">
                ${this.ctx.localize("device.registry_list_no_applicable_options")}
              </p>`:s.s6,d=a||0===r.length;return(0,s.qy)`
      <div class="field" data-field-key=${tn(this.path)}>
        ${tp(this.entry,this.ctx)} ${iw(i,this.ctx)}
        ${l}
        ${i.map((t,o)=>this._renderRow(t,o,r,i,a,e.dedupByTypeId))}
        ${ix(this.ctx,d,()=>this._addItem())}
        ${tu(this.path,this.ctx)}
      </div>
    `}_renderRow(e,t,i,a,o,r){let n=iI(e),l=new Set;r&&a.forEach((e,i)=>{if(i===t)return;let a=iI(e);a&&l.add(a)});let d=i.find(e=>e.id===n),c=void 0!==d,h=[...i].sort((e,t)=>e.id.localeCompare(t.id)),p=n?e[n]:null,u=null!==p&&"object"==typeof p&&!Array.isArray(p)&&!(0,i_.b)(p)&&!(p instanceof eS.ho),m=u?null:this._scalarDispatchType(d,p),v=(null===p||u)&&d?.config_entries?d.config_entries:[];return(0,s.qy)`
      <div class="registry-list-item" data-row-index=${t}>
        <div class="registry-list-row">
          <wa-select
            .value=${n}
            ?disabled=${o}
            placeholder=${this.ctx.localize("device.registry_list_select")}
            aria-label=${this.ctx.localize("device.registry_list_row_label",{index:String(t+1)})}
            @change=${e=>{let i=e.target.value;this._renameRow(t,i)}}
          >
            ${!c&&n?(0,s.qy)`<wa-option value=${n} selected
                    >${ij(n)}</wa-option
                  >`:s.s6}
            ${h.filter(e=>e.id===n||!l.has(e.id)).map(e=>(0,s.qy)`<wa-option value=${e.id} ?selected=${e.id===n}
                    >${ij(e.id)}</wa-option
                  >`)}
          </wa-select>
          ${i$(this.ctx,o,()=>this._removeAt(t))}
        </div>
        ${this._renderSubForm(t,n,m,v,d?.templatable??!1)}
      </div>
    `}_mutateEditable(e){let t=iZ(this.ctx.getAt(this.path)),{items:i,positions:a}=iK(t),o=e(i);this.ctx.emitChange(this.path,function(e,t,i){let a=[...e];if(t.forEach((e,t)=>{t<i.length&&(a[e]=i[t])}),i.length<t.length)for(let e of t.slice(i.length).reverse())a.splice(e,1);else if(i.length>t.length){let e=t.length>0?t[t.length-1]+1:a.length;a.splice(e,0,...i.slice(t.length))}return a}(t,a,o))}_scalarDispatchType(e,t){let i=e?.value_type;return i&&Object.prototype.hasOwnProperty.call(iB,i)?iB[i]:is(t)?eR.Hh.TIME_PERIOD:null}_renderSubForm(e,t,i,a,o){return null!==i?(0,s.qy)`<div class="registry-list-sub-form">
        ${this.ctx.renderEntry((0,iD.h)({type:i,templatable:o}),[...this.path,String(e),t])}
      </div>`:a.length>0?(0,s.qy)`<div class="registry-list-sub-form">
        ${a.map(i=>this.ctx.renderEntry(i,[...this.path,String(e),t,i.key]))}
      </div>`:s.s6}_addItem(){this._mutateEditable(e=>[...e,{}])}_removeAt(e){this._mutateEditable(t=>t.filter((t,i)=>i!==e))}_renameRow(e,t){this._mutateEditable(i=>{if(!t)return i;let a=i[e];return a&&iI(a)!==t?i.map((i,a)=>a===e?{[t]:null}:i):i})}constructor(...e){super(...e),this.path=[],this._catalog=null,this._fetchError=!1,this._kickedFetch=!1,this._retryFetch=()=>{if(!this._api)return;let e=this._ops();null!==e&&(this._fetchError=!1,e.fetch(this._api).catch(e=>{console.error("Failed to retry registry catalog fetch",e),this.isConnected&&(this._fetchError=!0)}))}}}iV.styles=[...to,(0,s.AH)`
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
    `],iU([(0,o.Fg)({context:m.Ie})],iV.prototype,"_api",void 0),iU([(0,n.MZ)({attribute:!1})],iV.prototype,"entry",void 0),iU([(0,n.MZ)({attribute:!1})],iV.prototype,"path",void 0),iU([(0,n.MZ)({attribute:!1})],iV.prototype,"ctx",void 0),iU([(0,n.wk)()],iV.prototype,"_catalog",void 0),iU([(0,n.wk)()],iV.prototype,"_fetchError",void 0),iV=iU([(0,n.EM)("esphome-registry-list")],iV);var iG=i(5230),iH=i(5659),iW=i(5874),iY=i(3107),iQ=i(792),iJ=i(2727),iX=i(2125),i0=i(4256),i1=i(6250);function i2(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}let i6=iY.YH.define();class i3 extends i1.U{render(){return(0,s.qy)`<div class="cm-wrap ${this.invalid?"invalid":""}"></div>`}firstUpdated(){this._mountEditor()}updated(e){if(this._view&&(e.has("_darkMode")&&this._view.dispatch({effects:this._themeCompartment.reconfigure((0,iX.P5)(this._darkMode))}),e.has("disabled")&&this._view.dispatch({effects:this._editableCompartment.reconfigure(iQ.Lz.editable.of(!this.disabled))}),e.has("value"))){let e=this._view.state.doc.toString();e!==this.value&&this._view.dispatch({changes:{from:0,to:e.length,insert:this.value},annotations:i6.of(!0)})}}_mountEditor(){this._mountView(this.value,[iJ.oQ,(0,i0.O)(this._localize),(0,iH.I)(),iW.Xt.of("  "),iQ.w4.of([iG.Yc]),this._editableCompartment.of(iQ.Lz.editable.of(!this.disabled)),this._themeCompartment.of((0,iX.P5)(this._darkMode)),iX.gn,iQ.Lz.updateListener.of(e=>{if(e.docChanged&&!e.transactions.some(e=>void 0!==e.annotation(i6))){let t=e.state.doc.toString();this.dispatchEvent(new CustomEvent("lambda-change",{detail:{value:t},bubbles:!0,composed:!0}))}})])}constructor(...e){super(...e),this._darkMode=(0,T.yk)(),this._localize=e=>e,this.value="",this.disabled=!1,this.invalid=!1,this.placeholder="",this._themeCompartment=new iY.xx,this._editableCompartment=new iY.xx}}function i4(e){return(0,i_.b)(e)?e._lambda:e instanceof eS.ho?e.body:null==e?"":String(e)}function i5(e,t,i){let a=i.getAt(t),o=i4(a),r=null!==i.errorAt(t),n=tr(e,i),l=(0,i_.b)(a)?a._tag:void 0;return tm(e,t,i,(0,s.qy)`<esphome-lambda-editor
      .value=${o}
      .invalid=${r}
      ?disabled=${n}
      placeholder=${String(e.default_value??"")}
      @lambda-change=${e=>i.emitChange(t,l?{_lambda:e.detail.value,_tag:l}:{_lambda:e.detail.value})}
    ></esphome-lambda-editor>`)}i3.styles=(0,s.AH)`
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
  `,i2([(0,o.Fg)({context:m.B6,subscribe:!0}),(0,n.wk)()],i3.prototype,"_darkMode",void 0),i2([(0,o.Fg)({context:m.$F}),(0,n.wk)()],i3.prototype,"_localize",void 0),i2([(0,n.MZ)()],i3.prototype,"value",void 0),i2([(0,n.MZ)({type:Boolean,reflect:!0})],i3.prototype,"disabled",void 0),i2([(0,n.MZ)({type:Boolean})],i3.prototype,"invalid",void 0),i2([(0,n.MZ)()],i3.prototype,"placeholder",void 0),i3=i2([(0,n.EM)("esphome-lambda-editor")],i3);let i8=new WeakMap;i(8944);var i9=i(1209);async function i7(e,t,i){let{created:a}=await e.setSecret(t,i,!1);return a&&window.dispatchEvent(new CustomEvent("secrets-saved")),{created:a}}async function ae(e,t,i){await e.setSecret(t,i,!0),window.dispatchEvent(new CustomEvent("secrets-saved"))}async function at(e,t,i,a,o){try{return await o(),(0,i9.ik)(e),!0}catch(e){return console.error(i,e),(0,d.UG)(a(t)),!1}}function ai(e,t,i,a,o){return at(e,o.errorKey,o.logLabel,a,async()=>{let{created:r}=await i7(e,t,i);d.me[r?"success":"info"](a(r?o.createdKey:"device.secret_picker_linked",{key:t}))})}i(4604),i(9489);var aa=i(9309);function ao(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({alert:r.mdiAlert,"content-copy":r.mdiContentCopy});class ar extends s.WF{willUpdate(e){(e.has("secretKey")||e.has("present"))&&(this._draftValue="",this._stored=null,this._busy=!1,this._loading=!1,this._loadError=!1,this._loadToken++,this._opToken++)}updated(){this.present&&this.secretKey&&this._api&&null===this._stored&&!this._loading&&!this._loadError&&this._loadStored()}render(){return this.present?this._renderEdit():this._renderCreate()}get _dirty(){return null!==this._stored&&this._draftValue!==this._stored}get _hasDraft(){return""!==this._draftValue.trim()}get _loadingStored(){return this.present&&null===this._stored}_renderEdit(){return this._loadError?this._renderLoadError():(0,s.qy)`<div class="row">
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
      ></esphome-confirm-dialog>`}_renderLoadError(){return(0,s.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_reveal_error")}
        <button class="retry" type="button" @click=${this._retry}>
          ${this._localize("device.secret_picker_retry")}
        </button>
      </span>
    </div>`}_renderCreate(){return(0,s.qy)`<div class="fix">
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
    </div>`}_renderInput(){return(0,s.qy)`<esphome-password-input
      class="value"
      .value=${this._draftValue}
      .disabled=${this._busy||this._loadingStored}
      .placeholder=${this._localize(this.present?"device.secret_picker_value":"device.secret_picker_missing_placeholder")}
      .label=${this._localize("device.secret_picker_value_label",{key:this.secretKey})}
      @password-input-change=${e=>{this._draftValue=e.detail.value}}
      @keydown=${e=>{"Enter"===e.key&&(e.preventDefault(),this.present?this._save():this._create())}}
    ></esphome-password-input>`}async _loadStored(){let e=++this._loadToken;this._loading=!0;let t=null,i=!1;try{let e=await this._api.getConfig("secrets.yaml");t=(0,e6.Tv)(e,this.secretKey)}catch{i=!0,(0,d.UG)(this._localize("device.secret_picker_reveal_error"))}if(e===this._loadToken){if(this._loading=!1,i){this._loadError=!0;return}this._stored=t??"",this._draftValue=this._stored}}async _run(e,t){let i=this._api;if(!i||!this.secretKey||this._busy)return;let a=this._opToken;this._busy=!0;try{let o=await e(i);if(a!==this._opToken)return;o&&t()}finally{a===this._opToken&&(this._busy=!1)}}constructor(...e){super(...e),this._localize=e=>e,this.secretKey="",this.present=!1,this.deviceName="",this._draftValue="",this._stored=null,this._busy=!1,this._loadError=!1,this._loadToken=0,this._opToken=0,this._loading=!1,this._retry=()=>{this._loadError=!1},this._copy=async()=>{await (0,aa.l)(this._draftValue)&&(0,d.VX)(this._localize("device.secret_reveal_copied"))},this._create=()=>{this._hasDraft&&this._run(e=>ai(e,this.secretKey,this._draftValue,this._localize,{createdKey:"device.secret_picker_missing_created",errorKey:"device.secret_picker_missing_error",logLabel:"Secret create failed"}),()=>{this._draftValue=""})},this._save=()=>{if(this._dirty){if((0,e6.e2)(this.secretKey,this.deviceName))return void this._confirmDialog?.open();this._persist()}},this._persist=()=>{this._run(e=>{var t,i,a,o;return t=this.secretKey,i=this._draftValue,a=this._localize,at(e,(o={savedKey:"device.secret_picker_saved",errorKey:"device.secret_picker_save_error",logLabel:"Secret save failed"}).errorKey,o.logLabel,a,async()=>{await ae(e,t,i),(0,d.VX)(a(o.savedKey,{key:t}))})},()=>{this._stored=this._draftValue})}}}function as(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ar.styles=(0,s.AH)`
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
  `,ao([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ar.prototype,"_localize",void 0),ao([(0,o.Fg)({context:m.Ie,subscribe:!0}),(0,n.wk)()],ar.prototype,"_api",void 0),ao([(0,n.MZ)({attribute:"secret-key"})],ar.prototype,"secretKey",void 0),ao([(0,n.MZ)({type:Boolean})],ar.prototype,"present",void 0),ao([(0,n.MZ)({attribute:"device-name"})],ar.prototype,"deviceName",void 0),ao([(0,n.P)("esphome-confirm-dialog")],ar.prototype,"_confirmDialog",void 0),ao([(0,n.wk)()],ar.prototype,"_draftValue",void 0),ao([(0,n.wk)()],ar.prototype,"_stored",void 0),ao([(0,n.wk)()],ar.prototype,"_busy",void 0),ao([(0,n.wk)()],ar.prototype,"_loadError",void 0),ar=ao([(0,n.EM)("esphome-secret-value")],ar),(0,k.C)({alert:r.mdiAlert,check:r.mdiCheck,"chevron-down":r.mdiChevronDown,"key-variant":r.mdiKeyVariant,plus:r.mdiPlus,"shield-key-outline":r.mdiShieldKeyOutline});class an extends s.WF{get _keys(){return this._secretKeys.value}get _migrateTarget(){return this.recommendedKeys[0]??""}get _canMigrate(){return""===this.selectedKey&&""!==this.value&&""!==this._migrateTarget&&void 0!==this._keys&&!this._keys.includes(this._migrateTarget)}get _missing(){return""!==this.selectedKey&&void 0!==this._keys&&!this._keys.includes(this.selectedKey)}render(){let e=""!==this.selectedKey,t=this._missing,i=(0,e6.Jw)(this._keys??[],[...this.recommendedKeys,this.selectedKey],this.deviceName,this._devices.map(e=>e.name)),a=new Set(i),o=new Set(this.recommendedKeys),r=this.recommendedKeys.filter(e=>a.has(e)),n=i.filter(e=>!o.has(e));return(0,s.qy)`
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
          ${e?(0,s.qy)`<span class="label">${this.selectedKey}</span>`:(0,s.qy)`<span class="placeholder"
                  >${this._localize("device.secret_picker_label")}</span
                >`}
          <wa-icon class="chevron" library="mdi" name="chevron-down"></wa-icon>
        </button>
        ${this._canMigrate?(0,s.qy)`<wa-dropdown-item class="migrate" value=${"__esphome_migrate_secret__"}>
                  <wa-icon slot="icon" library="mdi" name="shield-key-outline"></wa-icon>
                  ${this._localize("device.secret_picker_migrate",{key:this._migrateTarget})}
                </wa-dropdown-item>
                <wa-divider role="separator"></wa-divider>`:s.s6}
        ${r.length?(0,s.qy)`<small class="group-label" aria-hidden="true"
                  >${this._localize("device.secret_picker_related")}</small
                >
                ${r.map(e=>this._renderKeyItem(e))}
                ${n.length?(0,s.qy)`<small class="group-label" aria-hidden="true"
                        >${this._localize("device.secret_picker_shared")}</small
                      >`:s.s6}`:s.s6}
        ${n.map(e=>this._renderKeyItem(e))}
        ${i.length?s.s6:(0,s.qy)`<wa-dropdown-item class="empty" disabled role="status"
                >${this._localize("device.secret_picker_empty")}</wa-dropdown-item
              >`}
        <wa-divider role="separator"></wa-divider>
        <wa-dropdown-item class="create" value=${"__esphome_create_secret__"}>
          <wa-icon slot="icon" library="mdi" name="plus"></wa-icon>
          ${this._localize("device.secret_picker_create")}
        </wa-dropdown-item>
        ${e?(0,s.qy)`<wa-dropdown-item class="manual" value=${"__esphome_manual_value__"}>
                ${this._localize("device.secret_picker_manual")}
              </wa-dropdown-item>`:s.s6}
      </wa-dropdown>
      ${e?(0,s.qy)`<esphome-secret-value
              secret-key=${this.selectedKey}
              ?present=${!t}
              device-name=${this.deviceName}
            ></esphome-secret-value>`:s.s6}
    `}_renderKeyItem(e){return(0,s.qy)`<wa-dropdown-item
      value=${e}
      aria-selected=${e===this.selectedKey?"true":"false"}
    >
      ${e===this.selectedKey?(0,s.qy)`<wa-icon slot="icon" class="check" library="mdi" name="check"></wa-icon>`:s.s6}
      ${e}
    </wa-dropdown-item>`}_onSelect(e){let t=e.detail.item,i=t.classList;if(i?.contains("create"))return void(0,$.oo)("/secrets");if(i?.contains("migrate"))return void this._migrate();if(i?.contains("manual"))return void this._manual();let a=t.value??"";a&&this._emit(`!secret ${a}`)}async _manual(){if(!this._api||!this.selectedKey)return void this._emit("");try{let e=await this._api.getConfig("secrets.yaml");this._emit((0,e6.Tv)(e,this.selectedKey)??"")}catch{(0,d.UG)(this._localize("device.secret_picker_manual_error"))}}_emit(e){this.dispatchEvent(new CustomEvent("secret-selected",{detail:{value:e},bubbles:!0,composed:!0}))}async _migrate(){let e=this._migrateTarget;this._api&&e&&this.value&&await ai(this._api,e,this.value,this._localize,{createdKey:"device.secret_picker_migrated",errorKey:"device.secret_picker_migrate_error",logLabel:"Secret migration failed"})&&this._emit(`!secret ${e}`)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.disabled=!1,this.deviceName="",this.full=!1,this.fieldLabel="",this.selectedKey="",this.value="",this.recommendedKeys=[],this._secretKeys=new tj(this,{getCached:i9.BW,subscribe:i9.Ft,fetch:i9.RX},()=>this._api)}}function al(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}an.styles=(0,s.AH)`
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
  `,as([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],an.prototype,"_localize",void 0),as([(0,o.Fg)({context:m.Ie,subscribe:!0}),(0,n.wk)()],an.prototype,"_api",void 0),as([(0,o.Fg)({context:m.xJ,subscribe:!0}),(0,n.wk)()],an.prototype,"_devices",void 0),as([(0,n.MZ)({type:Boolean})],an.prototype,"disabled",void 0),as([(0,n.MZ)({attribute:"device-name"})],an.prototype,"deviceName",void 0),as([(0,n.MZ)({type:Boolean,reflect:!0})],an.prototype,"full",void 0),as([(0,n.MZ)({attribute:"field-label"})],an.prototype,"fieldLabel",void 0),as([(0,n.MZ)({attribute:"selected-key"})],an.prototype,"selectedKey",void 0),as([(0,n.MZ)()],an.prototype,"value",void 0),as([(0,n.MZ)({attribute:!1})],an.prototype,"recommendedKeys",void 0),an=as([(0,n.EM)("esphome-secret-picker")],an),(0,k.C)({"alert-circle-outline":r.mdiAlertCircleOutline,"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,close:r.mdiClose,"open-in-new":r.mdiOpenInNew,plus:r.mdiPlus});class ad extends s.WF{render(){let e=this._buildCtx(),t=this.requiredOnly?function(e){let t=new Map;for(let i of e)i.exclusive_group&&t.set(i.exclusive_group,(t.get(i.exclusive_group)??!1)||!!i.required);let i=e=>e.exclusive_group?t.get(e.exclusive_group):!!e.required;return[...e.filter(i),...e.filter(e=>!i(e))]}(this.entries):this.entries;return this.advancedSection?this._renderWithAdvancedSection(t,e):this._renderFlat(t,e)}_renderFlat(e,t){let i=tx(e,this.values,this.requiredGroups,eV(this)),a=this._makeItemRenderer(i,t);return(0,s.qy)`${this._renderConstraintBanners(t,i.memberKeys)}${i.ordered.map(a)}`}_renderWithAdvancedSection(e,t){let i=tx(e,this.values,this.requiredGroups,eV(this,{showAdvanced:!0})),a=this._makeItemRenderer(i,t),o=this._advancedUnitClassifier(i),r=i.ordered.filter(e=>!o(e)),n=i.ordered.filter(e=>o(e)),l=function e(t){for(let i of t)if(i.advanced||i.type===eR.Hh.NESTED&&e(i.config_entries??[]))return!0;return!1}(e),d=n.length>0&&0===r.length,c=this._advancedForceOpen(),h=this.showAdvanced||c||d&&!this.forceAdvancedControl,p=this.forceAdvancedControl||l&&!d,u=n.length+this.advancedExtraCount;return(0,s.qy)`${this._renderConstraintBanners(t,i.memberKeys)}${r.map(a)}${p?this._renderAdvancedControl(h,u,c):s.s6}${h?n.map(a):s.s6}`}_makeItemRenderer(e,t){let i=new Map(e.clusters.map(e=>[e.members[0].key,e]));return a=>{if(Array.isArray(a)){let e,i,o,r,n,l,d,c;return e=a.filter(e=>void 0!==t.getAt([e.key])),i=e[0]?.key??"",o=a.find(e=>e.key===i),r=t.scopeValues([]),n=t.board?.esphome.platform??null,l=a.filter(e=>void 0!==t.getAt([e.key])||(0,eK.VP)(e,r,t.presentComponents,n)),d=t.disabled||l.every(e=>e.locked),c=`exclusive-group-${a[0].key}`,(0,s.qy)`
    <div class="field" data-field-key=${tn(o?[o.key]:[])}>
      <label class="field-label" id=${c}>
        ${t.localize("device.exclusive_group_label")}
        <span class="required">*</span>
      </label>
      <wa-select
        data-no-value-sync
        aria-labelledby=${c}
        ?disabled=${d}
        @change=${e=>{let i=e.target.value;var o=i===t$?"":i;for(let e of a)e.key!==o&&void 0!==t.getAt([e.key])&&t.emitChange([e.key],void 0);o&&void 0===t.getAt([o])&&t.emitChange([o],{})}}
      >
        <wa-option value=${t$} ?selected=${""===i}>
          ${t.localize("device.exclusive_group_placeholder")}
        </wa-option>
        ${l.map(e=>(0,s.qy)`<wa-option value=${e.key} ?selected=${e.key===i}
              >${tc(e,t)}</wa-option
            >`)}
      </wa-select>
      ${e.length>1?(0,s.qy)`<p class="field-description exclusive-group-conflict">
              ${t.localize("device.exclusive_group_conflict")}
            </p>`:s.s6}
      ${o?(0,s.qy)`<div class="nested-fields">
              ${t_(o,[o.key],t,{includeAdvanced:!0})}
            </div>`:s.s6}
    </div>
  `}if(e.memberKeys.has(a.key)){let e=i.get(a.key);return e?e.cardinality?.kind==="exactly_one"?function(e,t){let i=e.members[0].key,a=t.scopeValues([]),o=t.board?.esphome.platform??null,r=e=>void 0!==t.getAt([e.key])||(0,eK.VP)(e,a,t.presentComponents,o),n=ty(e,t).filter(e=>e.members.some(r));if(n.length<2)return tw(e,t);let l=t.getClusterChoice(i)??n.find(e=>e.members.some(e=>(0,eK.rf)(t.getAt([e.key]))))?.id,d=n.find(e=>e.id===l),c=t.localize("device.constraint_exactly_one_radio"),h=`constraint-cluster-${i}`,p=(d?.members??[]).filter(r);return(0,s.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${tn([i])}
    >
      <div id=${h} class="constraint-cluster-header">
        <span>${c}</span>
      </div>
      <wa-radio-group
        class="constraint-cluster-radios"
        aria-labelledby=${h}
        .value=${l??""}
        ?disabled=${t.disabled}
        @change=${i=>(function(e,t,i){let a=e.members[0].key,o=ty(e,t),r=o.find(e=>e.id===i);if(r){for(let e of o)if(e.id!==i)for(let{key:i}of e.members){let e=t.getAt([i]);void 0!==e&&(t.setClusterStash(a,i,e),t.emitChange([i],void 0))}for(let{key:e}of r.members){let i=t.getClusterStash(a,e);void 0!==i&&(t.emitChange([e],i),t.clearClusterStash(a,e))}t.setClusterChoice(a,i)}})(e,t,i.target.value)}
      >
        ${n.map(e=>(0,s.qy)`<wa-radio value=${e.id}>${e.label}</wa-radio>`)}
      </wa-radio-group>
      ${p.length?(0,s.qy)`<div class="nested-fields">
              ${p.map(e=>t.renderEntry(e,[e.key]))}
            </div>`:s.s6}
    </div>
  `}(e,t):tw(e,t):s.s6}return e.visible.has(a)?this._renderEntry(a,a.key?[a.key]:[],t):s.s6}}_advancedForceOpen(){return this.entries.some(e=>e.advanced&&eG(e,this.values))}_advancedUnitClassifier(e){let t=new Map;for(let i of e.clusters){let e=i.members.every(e=>e.advanced);for(let a of i.members)t.set(a.key,e)}return i=>Array.isArray(i)?i.length>0&&i.every(e=>e.advanced):e.memberKeys.has(i.key)?t.get(i.key)??!1:!!i.advanced}_renderAdvancedControl(e,t,i){let a=t>0?this._localize("device.show_advanced_count",{count:t}):this._localize("device.show_advanced");return(0,s.qy)`<div class="advanced-toggle-row">
      <wa-switch
        size="small"
        ?disabled=${i}
        .checked=${e}
        @change=${e=>this._emitAdvancedToggle(e.target.checked)}
      >
        ${a}
      </wa-switch>
    </div>`}_emitAdvancedToggle(e){this.dispatchEvent(new CustomEvent("advanced-toggle",{detail:{show:e},bubbles:!0,composed:!0}))}_renderConstraintBanners(e,t){let i=tk({entries:this.entries,requiredGroups:this.requiredGroups,values:this.values,presentComponents:this.presentComponents,targetPlatform:e.board?.esphome.platform??null,formatKeys:t=>tb(t,this.entries,e)},t);return 0===i.length?s.s6:i.map(({kind:t,keys:i})=>(0,s.qy)`
        <div class="warning-banner constraint-banner">
          <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
          <span>${e.localize(`device.constraint_${t}`,{keys:i})}</span>
        </div>
      `)}willUpdate(e){e.has("entries")&&void 0!==e.get("entries")&&(this._pendingUnits.clear(),this._editingMagnitudes.clear(),this._constraintClusters.reset(),this._seededNestedOpen.clear())}_pathOf(e){return tl(e.getAttribute("data-field-key")??"")}updated(e){super.updated(e),this._syncSelectValues(),this._fieldScroll.maybeScroll(e),this.advancedSection&&!this.showAdvanced&&this._advancedForceOpen()&&this._emitAdvancedToggle(!0)}async _syncSelectValues(){if(this.shadowRoot)for(let e of this.shadowRoot.querySelectorAll("[data-field-key]")){let t=e.querySelector("wa-select");if(!t)continue;if(t.hasAttribute("data-no-value-sync")){await this._syncSelectedAttr(t);continue}if(t.updateComplete)try{await t.updateComplete}catch{}let i=this._pathOf(e);if(!i.length)continue;let a=(0,en.O6)(this.values,i);if(!(0,en.k4)(a)){""!==(Array.isArray(t.value)?t.value[0]??"":t.value??"")&&(t.value="");continue}let o=String(a??""),r=Array.from(t.querySelectorAll("wa-option")),s=o.match(/^\s*(?:GPIO)?(\d+)\s*$/i)?.[1],n=e=>r.find(t=>t.value?.toLowerCase()===e.toLowerCase()),l=o?n(o)??(s?n(`GPIO${s}`):void 0):null,d=l?.value??o;(Array.isArray(t.value)?t.value[0]??"":t.value??"")!==d&&(t.value=d)}}async _syncSelectedAttr(e){if(e.updateComplete)try{await e.updateComplete}catch{}let t=e.querySelector("wa-option[selected]"),i=t?.value??"";(Array.isArray(e.value)?e.value[0]??"":e.value??"")!==i&&(e.value=i)}_renderEntry(e,t,i){try{return this._renderEntryUnsafe(e,t,i)}catch(a){console.error("esphome-config-entry-form: render failed for entry",{key:e.key,type:e.type,path:t},a);let i=(0,W.u)(a);return(0,s.qy)`<div class="render-error" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div>
          <strong> ${this._localize("device.entry_render_error_title")} </strong>
          <code class="render-error-key"
            >${e.key||"(empty key)"} · ${e.type}</code
          >
          <pre class="render-error-message">${i}</pre>
        </div>
      </div>`}}_renderEntryUnsafe(e,t,i){var a,o;if(e.templatable&&(a=e.type)!==eR.Hh.NESTED&&a!==eR.Hh.MAP&&a!==eR.Hh.DIVIDER&&a!==eR.Hh.LABEL&&a!==eR.Hh.ALERT){let a,r,n,l,d,c,h;return o=()=>this._renderEntryLeaf(e,t,i),a=i.getAt(t),r=(0,i_.b)(a),(n=i8.get(i.stashOwner))||(n=new Map,i8.set(i.stashOwner,n)),l=t.join("."),(d=n.get(l))||(d={},n.set(l,d)),c=d,h=tn(t),(0,s.qy)`
    <div class="templatable-field" data-field-key=${h}>
      ${tt({isLambda:r,disabled:i.disabled,localize:i.localize,onSwitch:e=>{e!==r&&(r?(c.lambda=(0,i_.b)(a)?a._lambda:"",i.emitChange(t,c.literal??"")):(c.literal=a,i.emitChange(t,{_lambda:c.lambda??"",_tag:"!lambda"})))}})}
      ${r?i5(e,t,i):o()}
    </div>
  `}return this._renderEntryLeaf(e,t,i)}_renderEntryLeaf(e,t,i){let a=i.getAt(t);if("string"==typeof a&&(0,e4.R_)(a)){let a=e.type===eR.Hh.SECURE_STRING?"password":"text";return tf(e,a,t,i)}if(e.type===eR.Hh.DIVIDER)return(0,s.qy)`<wa-divider></wa-divider>`;if(e.type===eR.Hh.LABEL)return(0,s.qy)`<p class="label-entry">${tc(e,i)}</p>`;if(e.type===eR.Hh.ALERT)return(0,s.qy)`<div class="alert-entry">${tc(e,i)}</div>`;if(e.type===eR.Hh.NESTED)return e.multi_value?function(e,t,i){let a=i.getAt(t);if(a instanceof eS.ho)return(0,s.qy)`
      <div class="nested-list" data-field-key=${tn(t)}>
        ${tp(e,i)}
        <p class="field-description">${i.localize("device.multi_value_yaml_only")}</p>
        ${tu(t,i)}
      </div>
    `;let o=(0,en.ly)(a),r=tr(e,i),{addItem:n,removeAt:l}=iy(i,t,()=>({})),d=tc(e,i),c=e.config_entries??[];return(0,s.qy)`
    <div class="nested-list" data-field-key=${tn(t)}>
      ${tp(e,i)} ${iw(o,i)}
      ${o.map((e,a)=>{let o=[...t,String(a)],n=i.filterRenderable(c,e);return(0,s.qy)`
          <div class="nested-list-item" data-field-key=${tn(o)}>
            <div class="nested-list-item-header">
              <span class="nested-list-item-title"> ${d} ${a+1} </span>
              ${i$(i,r,()=>l(a))}
            </div>
            <div class="nested-fields">
              ${n.map(e=>i.renderEntry(e,[...o,e.key]))}
            </div>
          </div>
        `})}
      ${ix(i,r,n)} ${tu(t,i)}
    </div>
  `}(e,t,i):t8(e,t,i);if(e.type===eR.Hh.MAP){let a,o,r,n,l,d;return a=(e.config_entries??[])[0],n=Object.keys(r=(o=i.getAt(t))&&"object"==typeof o&&!Array.isArray(o)?o:{}),l=tr(e,i),d=()=>{let e=i.getAt(t);return e&&"object"==typeof e&&!Array.isArray(e)?Object.assign(Object.create(null),e):Object.create(null)},(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      ${0===n.length?(0,s.qy)`<p class="field-description">${i.localize("device.map_empty")}</p>`:s.s6}
      ${n.map(e=>{let o,n,c;return o=[...t,e],n=r[e],c=!(0,en.k4)(n)&&!(0,i_.b)(n),(0,s.qy)`
      <div class="map-row" data-field-key=${tn(o)}>
        <input
          type="text"
          class="multi-input map-key-input"
          .value=${e}
          ?disabled=${l}
          @change=${a=>((e,a)=>{if(e===a||!a)return;let o=i.getAt(t);if(!o||"object"!=typeof o||Array.isArray(o)||a in o)return;let r=Object.create(null);for(let[t,i]of Object.entries(o))r[t===e?a:t]=i;i.emitChange(t,r)})(e,a.target.value)}
        />
        <div class="map-value">
          ${c?(0,s.qy)`<p class="map-value-yaml-only">
                  ${i.localize("device.map_value_edit_in_yaml")}
                </p>`:a?i.renderEntry(a,o):s.s6}
        </div>
        <button
          type="button"
          class="multi-btn"
          ?disabled=${l}
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
        ?disabled=${l}
        @click=${()=>{let e=d(),a=1;for(;`new_${a}`in e;)a++;e[`new_${a}`]="",i.emitChange(t,e)}}
      >
        <wa-icon library="mdi" name="plus"></wa-icon>
        ${i.localize("device.map_add")}
      </button>
      ${tu(t,i)}
    </div>
  `}if(e.type===eR.Hh.REGISTRY_LIST)return(0,s.qy)`<esphome-registry-list
    .entry=${e}
    .path=${t}
    .ctx=${i}
  ></esphome-registry-list>`;if(e.multi_value)return function(e,t,i){let a=ib(i,t);if(a.some(e=>!(0,en.k4)(e)))return tg(e,t,i);let o=(e.type===eR.Hh.INTEGER||e.type===eR.Hh.FLOAT)&&"hex"!==e.display_format,r=o?a.map(e=>String(e??"")):a.map(e=>(0,e5.hZ)(String(e))),n=null!==i.errorAt(t),l=tr(e,i),{addItem:d,removeAt:c}=iy(i,t,()=>"");return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)} ${iw(r,i)}
      ${r.map((a,r)=>(0,s.qy)`
          <div class="multi-row">
            <input
              type=${o?"number":"text"}
              step=${o?e.type===eR.Hh.FLOAT?"any":"1":s.s6}
              class="multi-input ${n?"invalid":""}"
              .value=${a}
              ?disabled=${l}
              @input=${e=>{var a;let s;return a=e.target.value,void((s=[...ib(i,t)])[r]=o?""===a?"":Number(a):(0,e5.iI)(a),i.emitChange(t,s))}}
            />
            ${i$(i,l,()=>c(r))}
          </div>
        `)}
      ${ix(i,l,d)} ${tu(t,i)}
    </div>
  `}(e,t,i);if(e.references_component)return function(e,t,i){let a=e.references_component||"",o=i.resolveInterfaceProviders(a),r=(0,X.Zm)(i.yaml,a,o??[]),n=i.getAt(t),l=tv(e,t,i,n);if(l)return l;let d=String(n??""),c=null!==i.errorAt(t),h=""===d?(0,X.z)(r,i.yaml):null,p=(e,t,i)=>(0,s.qy)`
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
  `,u=""!==d&&!r.some(e=>e.id===d),m=u?p(d,d,i.localize("device.id_reference_unresolved",{domain:a})):s.s6,v=!c&&null!==o&&(0,X.Ty)(d,r,i.yaml),g=v?(0,e2.O)(i.localize("device.id_reference_unknown_error",{id:d})):s.s6,f=0===r.length&&!u,_=e=>{let o=e.target,r=o.value;if(r===t1){o.value=d,i.requestAddComponent(a);return}i.emitChange(t,r)},b=(0,s.qy)`
    <wa-option
      class="id-option id-option-add ${f?"id-option-add--solo":""}"
      value=${t1}
    >
      <span class="id-option-stack">
        <span class="id-option-primary id-option-primary-add">
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${i.localize("device.id_reference_add",{domain:a})}
        </span>
      </span>
    </wa-option>
  `;return f?(0,s.qy)`
      <div class="field" data-field-key=${tn(t)}>
        ${tp(e,i)}
        <wa-select
          class=${c?"invalid":""}
          ?disabled=${tr(e,i)}
          placeholder=${i.localize("device.id_reference_empty",{domain:a})}
          @change=${_}
        >
          ${b}
        </wa-select>
        ${tu(t,i)}
      </div>
    `:(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <wa-select
        class=${c||v?"invalid":""}
        ?disabled=${tr(e,i)}
        placeholder=${h?(0,e4.rq)(h.name,i.substitutions)||h.id:s.s6}
        @change=${_}
      >
        ${m}
        ${r.map(e=>{let t=e.name?`${e.id} \xb7 ${a}`:a,o=(0,e4.rq)(e.name,i.substitutions);return p(e.id,o||e.id,e===h?`${t} \xb7 ${i.localize("device.default_option_tag")}`:t)})}
        ${b}
      </wa-select>
      ${tu(t,i)}${g}
    </div>
  `}(e,t,i);if(e.options&&e.options.length>0)return function(e,t,i){let a,o,r=i.getAt(t),n=tv(e,t,i,r);if(n)return n;let l=String(r??""),d=null!==i.errorAt(t),c=tr(e,i);if(e.suggestions&&e.suggestions.length>0){let a=l.toLowerCase();return(0,s.qy)`
      <div class="field" data-field-key=${tn(t)}>
        ${tp(e,i)}
        <wa-select
          class=${d?"invalid":""}
          ?disabled=${c}
          placeholder=${String(e.default_value??"")}
          @change=${e=>i.emitChange(t,e.target.value)}
        >
          ${e.suggestions.map(e=>{let t=String(e);return(0,s.qy)`<wa-option value=${t} ?selected=${t.toLowerCase()===a}
              >${t}</wa-option
            >`})}
        </wa-select>
        ${tu(t,i)}
      </div>
    `}let h=(o=((a=String(i.getAt(["board"])??""))?(0,t9.S)(a):i.board?.esphome.variant??"").toLowerCase()).startsWith("esp32")?o:"";if(e.allow_custom_value&&e.options&&e.options.length>0){let a=(0,eK.yz)(l,e.options);return(0,s.qy)`
      <div class="field" data-field-key=${tn(t)}>
        ${tp(e,i)}
        <esphome-options-combobox
          .options=${iu(e.options,h,l)}
          .value=${l}
          label=${e.label}
          placeholder=${String(e.default_value??"")}
          .defaultValue=${String(e.default_value??"")}
          .defaultNote=${i.localize("device.default_option_tag")}
          ?disabled=${c}
          ?invalid=${d}
          @options-combobox-change=${a=>i.emitChange(t,ts(e,a.detail.value))}
        ></esphome-options-combobox>
        ${tu(t,i)}
        ${a?(0,s.qy)`<span class="field-warning" role="status"
                >${i.localize("validation.did_you_mean",{suggestion:a})}</span
              >`:s.s6}
      </div>
    `}let p=l.toLowerCase(),u=function(e,t,i){if(i&&"variant"===e.key&&"esp32"===t.sectionKey)return e.options?.some(e=>e.value.toLowerCase()===i)?i:void 0}(e,i,h)??(null!=e.default_value?String(e.default_value):""),m=u.toLowerCase(),v=e.options?.find(e=>e.value.toLowerCase()===m),g=v?.label??u,{clearable:f,visibleOptions:_}=function(e){let t=ih.get(e);if(!t){let i=e.options??[];t={clearable:i.some(e=>""===e.value),visibleOptions:i.filter(e=>""!==e.value)},ih.set(e,t)}return t}(e),b=iu(_,h,l);return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <wa-select
        class=${d?"invalid":""}
        ?disabled=${c}
        .withClear=${f}
        placeholder=${g}
        @change=${e=>i.emitChange(t,e.target.value)}
      >
        ${f?(0,s.qy)`<wa-icon slot="clear-icon" library="mdi" name="close"></wa-icon>`:s.s6}
        ${b.map(e=>{let t=e.value.toLowerCase()===p;return""===u||e.value.toLowerCase()!==m?(0,s.qy)`<wa-option value=${e.value} ?selected=${t}
              >${e.label}</wa-option
            >`:(0,s.qy)`<wa-option
            value=${e.value}
            .label=${e.label}
            ?selected=${t}
          >
            <span class="option-default-stack">
              <span>${e.label}</span>
              <small class="option-default-note"
                >${i.localize("device.default_option_tag")}</small
              >
            </span>
          </wa-option>`})}
      </wa-select>
      ${tu(t,i)}
    </div>
  `}(e,t,i);switch(e.type){case eR.Hh.BOOLEAN:return ip(e,t,i);case eR.Hh.SELECT:return tf(e,"text",t,i);case eR.Hh.SECURE_STRING:return tf(e,"password",t,i);case eR.Hh.INTEGER:case eR.Hh.FLOAT:return function(e,t,i){var a,o,r,n,l,d;if(e.suggestions&&e.suggestions.length>0)return tf(e,"number",t,i);let c=i.getAt(t),h=tv(e,t,i,c);if(h)return h;if("hex"===e.display_format){let n,l,d,c,h;return a=e,o=t,n=(r=i).getAt(o),l=null!==r.errorAt(o),d=tr(a,r),c=r.getEditingMagnitude(o)??ic(n),h=ic(a.default_value),tm(a,o,r,(0,s.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${l?"invalid":""}
      .value=${c}
      ?disabled=${d}
      placeholder=${h}
      @input=${e=>{let t=e.target.value;(r.setEditingMagnitude(o,t),""===t)?r.emitChange(o,""):r.emitChange(o,(0,ie.uS)((0,ie.EG)(t))||t)}}
      @blur=${()=>r.clearEditingMagnitude(o)}
    />`)}if(e.type===eR.Hh.INTEGER){let a,o,r;return n=e,l=t,a=(d=i).getEditingMagnitude(l)??String(d.getAt(l)??""),o=null!==d.errorAt(l),r=tr(n,d),tm(n,l,d,(0,s.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${o?"invalid":""}
      .value=${a}
      ?disabled=${r}
      placeholder=${String(n.default_value??"")}
      @input=${e=>{let t=e.target.value;d.setEditingMagnitude(l,t),d.emitChange(l,(0,eN.s)(t))}}
      @blur=${()=>d.clearEditingMagnitude(l)}
    />`)}let p=String(c??""),u=null!==i.errorAt(t),m=e.range?String(e.range[0]):void 0,v=e.range?String(e.range[1]):void 0,g=tr(e,i);return tm(e,t,i,(0,s.qy)`<input
      type="number"
      class=${u?"invalid":""}
      .value=${p}
      ?disabled=${g}
      min=${m??""}
      max=${v??""}
      step="any"
      placeholder=${String(e.default_value??"")}
      @input=${e=>{let a=e.target.value;i.emitChange(t,""===a?"":Number(a))}}
    />`)}(e,t,i);case eR.Hh.FLOAT_WITH_UNIT:return function(e,t,i){let a=e.unit_options??[],o=a[0]??"",r=i.getAt(t),n=tv(e,t,i,r);if(n)return n;let l=(0,eT.Eb)(r,a),d=i.getEditingMagnitude(t)??(null===l.value?"":String(l.value)),c=(0,eT.E3)(r,e.default_value,i.getPendingUnit(t),a),h=(0,eT.hX)(a,e.range,[o,(0,eT.Ji)(e.default_value,a),c]),p=(0,eT.x9)(e.default_value,a),u=null!==i.errorAt(t),m=tr(e,i),v=c===o,g=e.range&&v?String(e.range[0]):void 0,f=e.range&&v?String(e.range[1]):void 0,_=e=>i.emitChange(t,(0,eT.BR)(e));return(0,s.qy)`
    <div class="field float-with-unit" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <div class="float-with-unit-inputs">
        <input
          type="number"
          class=${u?"invalid":""}
          .value=${d}
          ?disabled=${m}
          min=${(0,t7.J)(g)}
          max=${(0,t7.J)(f)}
          step="any"
          placeholder=${p}
          @input=${e=>{let a=e.target.value;i.setEditingMagnitude(t,a),""===a&&i.setPendingUnit(t,c);let o=""===a?null:Number(a);_({value:Number.isFinite(o)?o:null,unit:c})}}
          @blur=${()=>i.clearEditingMagnitude(t)}
        />
        ${h.length>1?(0,s.qy)`
                <wa-select
                  data-no-value-sync
                  ?disabled=${m}
                  @change=${e=>{let a=e.target.value;null===l.value?i.setPendingUnit(t,a):_({value:l.value,unit:a})}}
                >
                  ${h.map(e=>(0,s.qy)`<wa-option value=${e} ?selected=${e===c}
                        >${e}</wa-option
                      >`)}
                </wa-select>
              `:(0,s.qy)`<span class="float-with-unit-suffix">${c}</span>`}
      </div>
      ${tu(t,i)}
    </div>
  `}(e,t,i);case eR.Hh.TIME_PERIOD:return function(e,t,i){let a=i.getAt(t),o=tv(e,t,i,a);if(o)return o;let r=il(a),n=null!==i.errorAt(t),l=tr(e,i);if(!r.parseable)return tf(e,"text",t,i);let d=void 0!==e.default_value&&null!==e.default_value?il(e.default_value):null,c=d&&d.parseable?d.value:"",h=null!=a&&""!==a?r.unit:d?.parseable?d.unit:r.unit;return(0,s.qy)`
    <div class="field time-period" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <div class="time-period-inputs">
        <input
          type="text"
          inputmode="decimal"
          class=${n?"invalid":""}
          .value=${r.value}
          ?disabled=${l}
          placeholder=${c}
          @input=${e=>{let a=e.target.value;i.emitChange(t,id(a,h))}}
        />
        <wa-select
          data-no-value-sync
          ?disabled=${l}
          @change=${e=>{let a=e.target.value;i.emitChange(t,id(r.value,a))}}
        >
          ${it.map(e=>(0,s.qy)`<wa-option value=${e} ?selected=${e===h}
                >${i.localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
      ${tu(t,i)}
    </div>
  `}(e,t,i);case eR.Hh.PIN:return function(e,t,i){if(!i.board||0===i.board.pins.length)return tf(e,"text",t,i);let a=i.getAt(t),o=(0,t2.E7)(a);if("string"==typeof o)return function(e,t,i,a,o){let[r,n,l]=a.split(":");return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <input
        type="text"
        readonly
        .value=${i.localize("device.pin_on_expander",{provider:r,hub:n,channel:l})}
      />
      ${tu(t,i)}
      ${ig(e,t,i,o,(0,en.Qd)(o),tr(e,i))}
    </div>
  `}(e,t,i,o,a);let r=("number"==typeof o?o:null)??im(a,i.board.pins),n=i.board.esphome.platform,l=null!==r?(0,t2.m5)(r,n):(0,en.k4)(a)?String(a??""):"",d=null!==i.errorAt(t),c=null!=e.default_value?(0,t2.j8)(e.default_value)??im(e.default_value,i.board.pins):null,h=null!==c?i.board.pins.find(e=>e.gpio===c)?.label??(0,t2.m5)(c,n):"",p=i.board.pins;if(e.suggestions&&e.suggestions.length>0){let t=new Set(e.suggestions.map(t2.j8).filter(e=>null!==e));if(t.size>0){let e=p.filter(e=>t.has(e.gpio));e.length>0&&(p=e)}}null!==r&&!p.some(e=>e.gpio===r)&&i.board.pins.some(e=>e.gpio===r)&&(p=[i.board.pins.find(e=>e.gpio===r),...p]);let u=(0,X.zq)(i.yaml,i.fromLine,(0,X.lz)(i.yaml,i.fromLine)),m=function(e){let t=new Set;for(let i of e.board?.featured_components??[])if(i.component_id===e.sectionKey)for(let e of Object.values(i.locked_pins??{}))"number"==typeof e&&t.add(e);return t}(i);null!==r&&m.add(r);let v=tr(e,i),g=(0,en.Qd)(a);return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <wa-select
        data-no-value-sync
        class=${d?"invalid":""}
        placeholder=${h}
        ?disabled=${v}
        @change=${e=>{let a=e.target.value;g?i.emitChange([...t,"number"],a):i.emitChange(t,a)}}
      >
        ${function(e,t,i,a,o,r){let n=[],l=[],d=[];for(let o of e){let e=function(e,t,i,a,o){let r=(0,t2.m5)(e.gpio,o.board?.esphome.platform),s=e.label||r,n=e.occupied_by||"",l=i.get(e.gpio)||"",d=(t.pin_mode===eR.l3.OUTPUT||t.pin_mode===eR.l3.INPUT_OUTPUT)&&e.features.includes(eR.k6.INPUT_ONLY),c=(t.pin_features??[]).every(t=>e.features.includes(t)),h=!1===e.available,p=h&&!a.has(e.gpio),u=!!(n||l),m=n?o.localize("device.pin_occupied_by",{name:n}):l?o.localize("device.pin_used_by",{name:l}):"",v=d?o.localize("device.pin_input_only"):"",g=e.notes||(h?o.localize("device.pin_unavailable"):""),f=[];return e.label&&e.label!==r&&f.push(r),m&&f.push(m),v&&f.push(v),g&&f.push(g),{optValue:r,primary:s,secondary:f.join(" • "),titleText:[m,v,g].filter(Boolean).join(" — "),warn:u||d,reserved:h,disabled:p,supported:c&&!d}}(o,t,i,a,r);(e.reserved?d:e.supported?n:l).push(e)}let c=n.length>0&&l.length>0,h=(t.pin_features??[]).map(e=>e.toUpperCase()).join(", "),p=(e,t)=>(0,s.qy)`${t?(0,s.qy)`<wa-divider class="pin-group-divider" aria-hidden="true"></wa-divider>`:s.s6} <small class="pin-group-label" aria-hidden="true">${e}</small>`;return(0,s.qy)`
    ${c&&h?p(r.localize("device.pin_group_supports",{features:h}),!1):s.s6}
    ${n.map(e=>iv(e,o))}
    ${c?p(r.localize("device.pin_group_other"),!0):s.s6}
    ${l.map(e=>iv(e,o))}
    ${d.length>0?p(r.localize("device.pin_group_reserved"),!0):s.s6}
    ${d.map(e=>iv(e,o))}
  `}(p,e,u,m,l,i)}
      </wa-select>
      ${tu(t,i)}
      ${ig(e,t,i,a,g,v)}
    </div>
  `}(e,t,i);case eR.Hh.COLOR:return tf(e,"color",t,i);case eR.Hh.MAC_ADDRESS:return tf(e,"text",t,i);case eR.Hh.LAMBDA:return i5(e,t,i);case eR.Hh.JSON:return function(e,t,i){let a=i.getAt(t),o=a instanceof eS.ho;if(!o){let o=tv(e,t,i,a);if(o)return o}let r=o?a.body:String(a??""),n=null!==i.errorAt(t);return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <textarea
        class="textarea-field ${n?"invalid":""}"
        rows="4"
        ?disabled=${tr(e,i)}
        .value=${r}
        placeholder=${String(e.default_value??"")}
        @input=${e=>{let r=e.target.value;i.emitChange(t,o?eS.ho.fromBodyText(r,a):r)}}
      ></textarea>
      ${tu(t,i)}
    </div>
  `}(e,t,i);case eR.Hh.ICON:let o=i.getAt(t),r=tv(e,t,i,o);if(r)return r;let n=String(o??""),l=null!==i.errorAt(t);return(0,s.qy)`
    <div class="field" data-field-key=${tn(t)}>
      ${tp(e,i)}
      <esphome-mdi-icon-picker
        .value=${n}
        .invalid=${l}
        .disabled=${tr(e,i)}
        .placeholder=${String(e.default_value??"Choose an icon…")}
        @change=${e=>i.emitChange(t,e.detail.value)}
      ></esphome-mdi-icon-picker>
      ${tu(t,i)}
    </div>
  `;case eR.Hh.TRIGGER:return(0,s.qy)`<div class="field" data-field-key=${tn(t)}>
          ${tc(e,i)}
          <button
            type="button"
            class="edit-actions-button"
            ?disabled=${i.disabled}
            @click=${()=>this._emitEditActionField(e.key)}
          >
            ${i.localize("device.automation_action_field_edit")}
          </button>
        </div>`;case eR.Hh.UNKNOWN:return tg(e,t,i);default:return tf(e,"text",t,i)}}_buildCtx(){let e=new Set;for(let t of this.requiredGroups)for(let i of t.keys)e.add(i);for(let t of this.entries)t.group&&e.add(t.key);let t={localize:this._localize,disabled:this.disabled,yaml:this.yaml,substitutions:this._parseSubstitutions(this.yaml),fromLine:this.fromLine,sectionKey:this.sectionKey,deviceName:tF(this._devices,this.configuration),board:this.board,pinRegistryModes:this._pinRegistryModes.value,requiredOnly:this.requiredOnly,showAdvanced:this.showAdvanced,presentComponents:this.presentComponents,reactiveConstraintKeys:e,entries:this.entries,nestedOpenSections:this._nestedOpenSections,getAt:e=>(0,en.O6)(this.values,e),errorAt:e=>this.errors.get(e.join("."))??null,emitChange:(e,t)=>this._emitChange(e,t),toggleNested:e=>this._toggleNested(e),seedNestedOpen:e=>this._seedNestedOpen(e),requestAddComponent:e=>this._requestAddComponent(e),resolveInterfaceProviders:e=>this._resolveInterfaceProviders(e),scopeValues:e=>this._scopeValues(e),filterRenderable:this._filterRenderable,getPendingUnit:e=>this._pendingUnits.get(e.join(".")),setPendingUnit:(e,t)=>{this._pendingUnits.set(e.join("."),t),this.requestUpdate()},getEditingMagnitude:e=>this._editingMagnitudes.get(e.join(".")),setEditingMagnitude:(e,t)=>{this._editingMagnitudes.set(e.join("."),t)},clearEditingMagnitude:e=>{this._editingMagnitudes.delete(e.join("."))},getClusterChoice:e=>this._constraintClusters.getChoice(e),setClusterChoice:(e,t)=>this._constraintClusters.setChoice(e,t),getClusterStash:(e,t)=>this._constraintClusters.getStash(e,t),setClusterStash:(e,t,i)=>this._constraintClusters.setStash(e,t,i),clearClusterStash:(e,t)=>this._constraintClusters.clearStash(e,t),stashOwner:this,renderEntry:()=>s.s6};return t.renderEntry=(e,i)=>this._renderEntry(e,i,t),t}_scopeValues(e){let t=(0,en.O6)(this.values,e);return t&&"object"==typeof t&&!Array.isArray(t)?t:{}}_emitChange(e,t){this.dispatchEvent(new CustomEvent("value-change",{detail:{path:e,value:t},bubbles:!0,composed:!0}))}_emitEditActionField(e){this.dispatchEvent(new CustomEvent("edit-action-field",{detail:{field:e},bubbles:!0,composed:!0}))}_toggleNested(e){let t=new Set(this._nestedOpenSections);t.has(e)?t.delete(e):t.add(e),this._nestedOpenSections=t}openNested(e){if(this._nestedOpenSections.has(e))return;let t=new Set(this._nestedOpenSections);t.add(e),this._nestedOpenSections=t}_seedNestedOpen(e){this._seededNestedOpen.has(e)||(this._seededNestedOpen.add(e),this._nestedOpenSections.add(e))}_requestAddComponent(e){this.dispatchEvent(new CustomEvent("request-add-component",{detail:{domain:e},bubbles:!0,composed:!0}))}_resolveInterfaceProviders(e){if(!e)return[];let t=this._interfaceProviders.get(e);return t||(this._api&&!this._interfaceProvidersPending.has(e)&&(this._interfaceProvidersPending.add(e),this._api.getComponents({provides:e,limit:200}).then(t=>{this._interfaceProviders.set(e,t.components.map(t=>(0,X.G_)(t,e))),this.requestUpdate()}).catch(t=>console.warn("[config-entry-form] provider fetch failed for",e,t)).finally(()=>this._interfaceProvidersPending.delete(e))),null)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._pinRegistryModes=new tj(this,{getCached:tT,subscribe:tD,fetch:tI},()=>this._api),this.entries=[],this.values={},this.requiredGroups=[],this.errors=new Map,this.board=null,this.disabled=!1,this.showAdvanced=!1,this.advancedSection=!1,this.forceAdvancedControl=!1,this.advancedExtraCount=0,this.requiredOnly=!1,this.yaml="",this.sectionKey="",this.configuration="",this.presentComponents=new Set,this._nestedOpenSections=new Set,this._seededNestedOpen=new Set,this._interfaceProviders=new Map,this._interfaceProvidersPending=new Set,this._fieldScroll=new tU(this),this._fieldFocus=new tZ(this),this._pendingUnits=new Map,this._editingMagnitudes=new Map,this._constraintClusters=new tB(this),this._filterRenderable=(e,t)=>eH(e,t,eV(this)),this._parseSubstitutions=(0,l.A)(e4.Gr)}}function ac(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ad.styles=[to,(0,s.AH)`
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
    `],al([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ad.prototype,"_localize",void 0),al([(0,o.Fg)({context:m.Ie,subscribe:!0}),(0,n.wk)()],ad.prototype,"_api",void 0),al([(0,o.Fg)({context:m.xJ,subscribe:!0}),(0,n.wk)()],ad.prototype,"_devices",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"entries",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"values",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"requiredGroups",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"errors",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"board",void 0),al([(0,n.MZ)({type:Boolean})],ad.prototype,"disabled",void 0),al([(0,n.MZ)({type:Boolean,attribute:"show-advanced"})],ad.prototype,"showAdvanced",void 0),al([(0,n.MZ)({type:Boolean,attribute:"advanced-section"})],ad.prototype,"advancedSection",void 0),al([(0,n.MZ)({type:Boolean,attribute:"force-advanced-control"})],ad.prototype,"forceAdvancedControl",void 0),al([(0,n.MZ)({type:Number,attribute:"advanced-extra-count"})],ad.prototype,"advancedExtraCount",void 0),al([(0,n.MZ)({type:Boolean,attribute:"required-only"})],ad.prototype,"requiredOnly",void 0),al([(0,n.MZ)()],ad.prototype,"yaml",void 0),al([(0,n.MZ)({type:Number,attribute:"from-line"})],ad.prototype,"fromLine",void 0),al([(0,n.MZ)({attribute:"section-key"})],ad.prototype,"sectionKey",void 0),al([(0,n.MZ)()],ad.prototype,"configuration",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"presentComponents",void 0),al([(0,n.MZ)({attribute:!1})],ad.prototype,"focusFieldPath",void 0),al([(0,n.wk)()],ad.prototype,"_nestedOpenSections",void 0),ad=al([(0,n.EM)("esphome-config-entry-form")],ad),(0,k.C)({"alert-circle-outline":r.mdiAlertCircleOutline});class ah extends s.WF{get currentValues(){return{...this._values}}get _entries(){return this._overlayOptions(this._overlayRequired(this.component.config_entries,this.extraRequired),this.optionOverrides)}willUpdate(e){super.willUpdate(e),(e.has("component")||!this._initialized)&&this.component&&(this._initialized=!0,this._initValues(),this._localBlockMessage="",this._depResolver.kickoff(this.component.dependencies??[])),(e.has("component")||e.has("yaml")||e.has("board"))&&this._resolveProvidedDeps()}_missingDeps(e){return eF(this.component.dependencies??[],this.yaml,e).filter(e=>!this._providedDeps.has(e))}async _resolveProvidedDeps(){let e=++this._providesSeq;this._providedDeps.size&&(this._providedDeps=new Set);let t=this._api,i=this.component?.dependencies??[];if(!t||0===i.length)return;let a=(0,eS.Zn)(this.yaml),o=eF(i,this.yaml,a);if(0!==o.length)try{let i=await eO(t,o,a,{platform:this.board?.esphome.platform??null,boardId:this.board?.id??null});e===this._providesSeq&&(i.size||this._providedDeps.size)&&(this._providedDeps=i)}catch(e){console.warn("[add-component-form] provides lookup failed",e)}}_initValues(){this._values=tC({entries:this._entries,component:this.component,board:this.board,yaml:this.yaml,prefillReference:this.prefillReference,prefillFields:this.prefillFields,restoredValues:this.restoredValues,localize:this._localize})}render(){let e=this.submitting,t=(0,eS.Zn)(this.yaml),i=this._missingDeps(t),a=(0,eK.JK)(this._entries,this._values,t,this.board?.esphome.platform??null),o=!this._hasRequiredErrors(a);return(0,s.qy)`
      <div class="form">
        <p class="form-desc">${(0,B.Gc)(this.component.description)}</p>
        ${i.length>0?this._renderMissingDeps(i):s.s6}
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
        ${this._showYaml?(0,s.qy)`<pre class="yaml-preview">${this._generateYamlPreview()}</pre>`:s.s6}
        ${this.submitError?(0,s.qy)`<p class="error">${this.submitError}</p>`:s.s6}
        ${this._localBlockMessage?(0,s.qy)`<p class="error">${this._localBlockMessage}</p>`:s.s6}
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
    `}_renderMissingDeps(e){return(0,s.qy)`
      <div class="deps-warning" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div class="deps-warning-body">
          <div class="deps-warning-title">
            ${this._localize("device.missing_dependencies_title",{name:this.component.name})}
          </div>
          <div>${this._localize("device.missing_dependencies_body")}</div>
          <div class="deps-warning-actions">
            ${e.map(e=>(0,s.qy)`<button
                  type="button"
                  class="dep-button"
                  @click=${()=>this._onAddDep(e)}
                >
                  ${this._localize("device.missing_dependencies_add",{domain:this._depResolver.resolve(e)})}
                </button>`)}
          </div>
        </div>
      </div>
    `}_onAddDep(e){this.dispatchEvent(new CustomEvent("navigate-to-dep",{detail:{domain:e},bubbles:!0,composed:!0}))}_hasRequiredErrors(e){for(let t of e.values())if("validation.required"===t.code)return!0;return!1}_labelForErrorKey(e){let t,i=e.split("."),a=this._entries;for(let e of i){if(!a||!(t=a.find(t=>t.key===e)))break;a=t.type===eR.Hh.NESTED?t.config_entries??[]:null}return t?e1(t,this._localize):e}_anyErrorIsVisible(e,t){var i,a;if(0===e.size)return!1;let o=(i=this._entries,a=this._values,function e(t,i,a,o=[],r=new Set){for(let s of eH(t,i,a)){if(s.type===eR.Hh.NESTED){let t=s.config_entries??[];s.multi_value?(0,en.ly)(i[s.key]).forEach((i,n)=>{e(t,i,a,[...o,s.key,String(n)],r)}):e(t,(0,en.qY)(i[s.key]),a,[...o,s.key],r),r.add([...o,s.key].join("."));continue}r.add([...o,s.key].join("."))}return r}(i,a,tz(this.board,t)));for(let t of e.keys())if(o.has(t))return!0;return!1}_onValueChange(e){let{path:t,value:i}=e.detail;this._values=(0,en.Oe)(this._values,t,i);let a=t.join(".");if(this._errors.has(a)){let e=new Map(this._errors);e.delete(a),this._errors=e}this._localBlockMessage&&(this._localBlockMessage="")}_generateYamlPreview(){let e=(0,eC.Ze)(this.component.id,this.board),t=[`${e}:`];return t.push(...(0,eS.ym)(this._values,"  ")),t.join("\n")}_onCancel(){this.dispatchEvent(new CustomEvent("form-cancel",{bubbles:!0,composed:!0}))}_onSubmit(){this._localBlockMessage="";let e=(0,eS.Zn)(this.yaml),t=this._missingDeps(e);if(t.length>0){this._localBlockMessage=`${this._localize("device.missing_dependencies_title",{name:this.component.name})} (${t.join(", ")})`;return}let i=(0,eK.JK)(this._entries,this._values,e,this.board?.esphome.platform??null);if(i.size>0){if(this._errors=i,!this._anyErrorIsVisible(i,e)){let e=[...i.entries()].map(([e,t])=>`${this._labelForErrorKey(e)}: ${this._localize(t.code,t.params)}`).join("; ");this._localBlockMessage=`${this._localize("device.add_component_hidden_validation_error")} (${e})`}return}this._errors=new Map,this._localBlockMessage="";let a=eZ(this._entries,this._values);this.dispatchEvent(new CustomEvent("form-submit",{detail:{fields:a},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this.yaml="",this.prefillReference=null,this.prefillFields=null,this.extraRequired=null,this.restoredValues=null,this.optionOverrides=null,this.submitting=!1,this.submitError="",this._values={},this._errors=new Map,this._localBlockMessage="",this._showYaml=!1,this._providedDeps=new Set,this._providesSeq=0,this._depResolver=new tA(this,()=>this._api,()=>this.board?.esphome.platform||void 0),this._overlayRequired=(0,l.A)(tM),this._overlayOptions=(0,l.A)(tP),this._initialized=!1}}ah.styles=[v.G,G.z9,tS.V,tL],ac([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ah.prototype,"_localize",void 0),ac([(0,o.Fg)({context:m.Ie})],ah.prototype,"_api",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"component",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"board",void 0),ac([(0,n.MZ)()],ah.prototype,"yaml",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"prefillReference",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"prefillFields",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"extraRequired",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"restoredValues",void 0),ac([(0,n.MZ)({attribute:!1})],ah.prototype,"optionOverrides",void 0),ac([(0,n.MZ)({type:Boolean})],ah.prototype,"submitting",void 0),ac([(0,n.MZ)()],ah.prototype,"submitError",void 0),ac([(0,n.wk)()],ah.prototype,"_values",void 0),ac([(0,n.wk)()],ah.prototype,"_errors",void 0),ac([(0,n.wk)()],ah.prototype,"_localBlockMessage",void 0),ac([(0,n.wk)()],ah.prototype,"_showYaml",void 0),ac([(0,n.wk)()],ah.prototype,"_providedDeps",void 0),ah=ac([(0,n.EM)("esphome-add-component-form")],ah);var ap=i(8719),au=i(4996),am=i(9295),av=i(1448),ag=i(2743);function af(e,t,i){return e.includes(".")?i.has(e):t.has(e)}function a_(e,...t){if(!e)return!0;let i=e.toLowerCase();return t.some(e=>void 0!==e&&e.toLowerCase().includes(i))}let ab=(0,l.A)(eS.Zn),ay=(0,l.A)(eS.u),aw=(0,l.A)(eE);function a$(e,t){let i=e.fields?.id?.value;return"string"==typeof i&&t.has(i)}function ax(e,t){return!!e.locked_pins&&(0,X.cN)(t,(0,X.iZ)(e.component_id).domain,e.locked_pins)}function ak(e){let t=ab(e.yaml),i=ay(e.yaml),a=e.lockedCategories.length>0,o=e._components.filter(t=>(0,eK.Cs)(t.supported_platforms,e.platform)),r=a?new Set(o.map(e=>e.id)):null,s=new Map,n=e.board;if(n)for(let e of n.featured_components??[])s.set((0,eC.m0)(n.id,e.id),e);let l=s.size?aw(e.yaml):new Set;return o.filter(a=>{let o=s.get(a.id);if(o&&(a$(o,l)||ax(o,e.yaml)))return!1;let n=o?.component_id??a.id;return!(!a.multi_conf&&af(n,t,i)||r&&a.id.includes(".")&&a.dependencies.length>0&&!a.dependencies.every(e=>r.has(e)||t.has(e)))&&!0})}let az=(0,l.A)((e,t)=>{let i=e?.featured_bundles??[];if(!e||0===i.length)return new Set;let a=new Map;for(let t of e.featured_components??[]){let e=t.fields?.id?.value;"string"==typeof e&&a.set(t.id,e)}let o=aw(t),r=new Set;for(let e of i){let t=e.component_ids.map(e=>a.get(e)).filter(e=>void 0!==e);t.length>0&&t.every(e=>o.has(e))&&r.add(e.id)}return r});function aC(e){let t=az(e.board,e.yaml);return(e.board?.featured_bundles??[]).filter(e=>!t.has(e.id))}function aq(e){let t=(e._search??"").trim();return aC(e).filter(e=>a_(t,e.name,e.description,e.id))}function aE(e,t){let i=e.board;if(!i)return 0;let a=i.featured_components??[],o=ab(e.yaml),r=ay(e.yaml),s=a.length?aw(e.yaml):new Set,n=t?.applyQuery??!0,l=n?(e._search??"").trim():"";return a.filter(t=>!a$(t,s)&&!ax(t,e.yaml)&&(!1!==t.multi_conf||!af(t.component_id,o,r))&&a_(l,t.name??void 0,t.description??void 0,t.id)).length+(n?aq(e):aC(e)).length}function aS(e){let t=e.target;return!t?.closest("a, button")}let aA=(0,s.AH)`
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
`;function aM(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({"arrow-collapse-all":r.mdiArrowCollapseAll,"arrow-expand-all":r.mdiArrowExpandAll,memory:r.mdiMemory,"open-in-new":r.mdiOpenInNew,"package-variant-closed":r.mdiPackageVariantClosed,plus:r.mdiPlus});class aP extends s.WF{get _components(){return this._list.items}get _total(){return this._list.total}_prefersFeatured(){return 0===this.lockedCategories.length&&!!this.boardId&&aE(this,{applyQuery:!1})>0}_recommendationInclusive(){return this._category===eA.FEATURED||"all"===this._category}load(){this._provides="",this._prefersFeatured()?this._category=eA.FEATURED:this._category===eA.FEATURED&&(this._category="all"),this._fetchComponents()}filterByDomain(e){Object.values(eA).includes(e)?(this._search="",this._provides="",this._category=e):(this._search=e,this._provides=e,this._category="all"),this._fetchComponents()}_fetchComponents(){let e=this._search.trim()||void 0,t=this.lockedCategories.length>0,i={category:t?this.lockedCategories:"all"!==this._category?this._category:void 0,exclude_category:!t&&this.excludeCategories.length>0?this.excludeCategories:void 0,platform:this.platform||void 0,board_id:this.boardId||void 0},a=this._provides;this._list.reset(async(t,o)=>{let r=a?await this._api.getComponents({...i,offset:t,limit:o,provides:a}):await this._api.getComponents({...i,offset:t,limit:o,query:e});return 0===t&&a&&0===r.components.length&&(this._provides="",a="",r=await this._api.getComponents({...i,offset:t,limit:o,query:e})),0===t&&(this._categories=r.categories),{items:r.components,total:r.total}})}updated(){this._list.loading||0!==this.lockedCategories.length||this._category!==eA.FEATURED||this._provides||ak(this).length+aq(this).length!==0||(this._category="all",this._fetchComponents()),this._intersection.observeIfPresent(this._sentinel,null,"200px")}render(){var e;let t,i,a,o,r,n,l,d;if(this._list.loading&&!this._list.hasLoaded)return(0,s.qy)`<div class="loading">
        ${this._localize("device.loading_components")}
      </div>`;let c=(e=this._localize,t=new Set(this.excludeCategories),i=this._categories.filter(e=>!t.has(e.id)),a=this.lockedCategories.length?0:aE(this),o=i.filter(e=>e.id!==eA.FEATURED),r=t.size?o.reduce((e,t)=>e+t.count,0)+a:this._total,n=new Intl.Collator(void 0,{sensitivity:"base"}),l=o.map(e=>({id:e.id,label:tE(e.id),count:e.count})).sort((e,t)=>n.compare(e.label,t.label)),d=[],a>0&&d.push({id:eA.FEATURED,label:e("device.component_category_featured"),count:a}),d.push({id:"all",label:e("device.component_category_all"),count:r}),d.push(...l),d),h=0===this.lockedCategories.length,p=this._recommendationInclusive()?aq(this):[],u=ak(this),m=function(e){let t=new Map;for(let i of e){let e=JSON.stringify([i.category,i.name]),a=t.get(e);a?a.push(i):t.set(e,[i])}let i=new Set;for(let e of t.values())if(e.length>1)for(let t of e)i.add(t.id);return i}(u);return(0,s.qy)`
      ${h?(0,s.qy)`<div class="sidebar">
              <p class="sidebar-label">
                ${this._localize("device.component_categories")}
              </p>
              ${c.map(({id:e,label:t,count:i})=>(0,s.qy)`
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
            </div>`:s.s6}
      <div class="main">
        <input
          type="search"
          autocomplete="off"
          .value=${this._search}
          @input=${this._onSearchInput}
          placeholder=${this._localize("device.search_components_placeholder")}
        />
        ${!this._list.loading?(0,s.qy)`<span class="result-count"
                >${this._localize("device.components_count",{visible:u.length+p.length,total:this._total+p.length})}</span
              >`:s.s6}
        <div class="grid-scroll">
          <div class="components-grid">
            ${this._list.loading?(0,s.qy)`<p class="empty">
                    ${this._localize("device.loading_components")}
                  </p>`:u.length+p.length?(0,s.qy)`
                      ${p.map(e=>{var t;let i;return t=this,i=!!e.image_url&&!t._imageFailed.has(e.id),(0,s.qy)`
    <article
      class="component-card component-card--featured"
      @click=${i=>{aS(i)&&t._onAddBundle(e)}}
    >
      <div class="component-card-header">
        ${i?(0,s.qy)`<div class="component-image">
                <img
                  src=${e.image_url}
                  alt=${e.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>t._onImageError(e.id)}
                />
              </div>`:(0,s.qy)`<div class="component-image--placeholder">
                <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
              </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title">${e.name}</h3>
        </div>
        <span class="bundle-badge">
          <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
          ${t._localize("device.featured_bundle_badge")}
        </span>
      </div>
      ${e.description?(0,s.qy)`<p class="component-description component-description--clamp">
              ${(0,B.Gc)(e.description)}
            </p>`:s.s6}
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
                      ${u.map(e=>(function(e,t,i,a,o,r=!1){var n,l;let d,c=!!t.image_url&&!e._imageFailed.has(t.id),h="all"===(n=e._category)||"featured"===n?tE(t.category):"",p=r?-1===(d=(l=t.id).indexOf("."))?"":l.slice(d+1).split("_").filter(e=>e.length>0).map(e=>e.toUpperCase()).join(" "):"";return(0,s.qy)`
    <article
      class="component-card ${i?"component-card--expanded":""} ${a?"component-card--featured":""}"
      @click=${i=>{aS(i)&&e._onAdd(t)}}
    >
      <div class="component-card-header">
        ${c?(0,s.qy)`<div class="component-image">
                <img
                  src=${t.image_url}
                  alt=${t.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>e._onImageError(t.id)}
                />
              </div>`:(0,s.qy)`<div class="component-image--placeholder">
                <wa-icon library="mdi" name="memory"></wa-icon>
              </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title">${t.name}</h3>
          ${h?(0,s.qy)`<span class="component-category-chip">${h}</span>`:s.s6}
          ${p?(0,s.qy)`<span class="component-category-chip">${p}</span>`:s.s6}
        </div>
        <button
          class="expand-button"
          type="button"
          aria-pressed=${i}
          title=${o("wizard.expand_board")}
          @click=${()=>e._onToggleExpand(t)}
        >
          <wa-icon
            library="mdi"
            name=${i?"arrow-collapse-all":"arrow-expand-all"}
          ></wa-icon>
        </button>
      </div>
      <p class="component-description ${i?"":"component-description--clamp"}">
        ${(0,B.Gc)(t.description)}
      </p>
      <div class="card-footer">
        <a class="more-info" href=${t.docs_url} target="_blank" rel="noreferrer">
          ${o("device.more_info")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <button
          class="select-component"
          type="button"
          @click=${()=>e._onAdd(t)}
        >
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${o("device.add_component_action")}
        </button>
      </div>
    </article>
  `})(this,e,e.id===this._expandedId,(0,eC.sO)(e.id),this._localize,m.has(e.id)))}
                    `:(0,s.qy)`<p class="empty">
                      ${this._localize(this._list.hasError?"device.components_load_error":"device.no_components_found")}
                    </p>`}
          </div>
          ${(0,ag.F)({loadingMore:this._list.loadingMore,error:this._list.hasError&&this._list.items.length>0,hasMore:this._list.hasMore,localize:this._localize,loadingLabelKey:"device.loading_components",errorLabelKey:"device.components_load_more_error",onRetry:()=>this._list.loadMore(),loadingClass:"empty"})}
        </div>
      </div>
    `}_onToggleExpand(e){this._expandedId=this._expandedId===e.id?null:e.id}_onImageError(e){if(this._imageFailed.has(e))return;let t=new Set(this._imageFailed);t.add(e),this._imageFailed=t}_onAdd(e){this.dispatchEvent(new CustomEvent("add-component",{detail:{component:e},bubbles:!0,composed:!0}))}_onAddBundle(e){this.dispatchEvent(new CustomEvent("add-bundle",{detail:{bundle:e,boardId:this.boardId},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.platform="",this.boardId="",this.board=null,this.yaml="",this.lockedCategories=[],this.excludeCategories=[],this._list=new av.S(this),this._categories=[],this._search="",this._category="all",this._provides="",this._expandedId=null,this._imageFailed=new Set,this._intersection=new am.Q(this,()=>this._list.loadMore()),this._debouncedSearch=(0,au.s)(()=>this._fetchComponents(),300),this._onSearchInput=e=>{this._search=e.target.value,this._provides="",this._recommendationInclusive()&&this._prefersFeatured()&&(this._category=this._search.trim()?"all":eA.FEATURED),this._debouncedSearch()}}}function aL(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aP.styles=[v.G,G.z9,aA,ap.f],aM([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],aP.prototype,"_localize",void 0),aM([(0,o.Fg)({context:m.Ie})],aP.prototype,"_api",void 0),aM([(0,n.MZ)()],aP.prototype,"platform",void 0),aM([(0,n.MZ)({attribute:"board-id"})],aP.prototype,"boardId",void 0),aM([(0,n.MZ)({attribute:!1})],aP.prototype,"board",void 0),aM([(0,n.MZ)()],aP.prototype,"yaml",void 0),aM([(0,n.MZ)({attribute:!1})],aP.prototype,"lockedCategories",void 0),aM([(0,n.MZ)({attribute:!1})],aP.prototype,"excludeCategories",void 0),aM([(0,n.wk)()],aP.prototype,"_categories",void 0),aM([(0,n.wk)()],aP.prototype,"_search",void 0),aM([(0,n.wk)()],aP.prototype,"_category",void 0),aM([(0,n.wk)()],aP.prototype,"_provides",void 0),aM([(0,n.wk)()],aP.prototype,"_expandedId",void 0),aM([(0,n.wk)()],aP.prototype,"_imageFailed",void 0),aM([(0,n.P)(".sentinel")],aP.prototype,"_sentinel",void 0),aP=aM([(0,n.EM)("esphome-component-catalog")],aP),(0,k.C)({close:r.mdiClose,"arrow-left":r.mdiArrowLeft,"package-variant-closed":r.mdiPackageVariantClosed});class aF extends s.WF{get _restoredValuesForMount(){return this._returnTo?null:this._returnValues}open(){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0,this.updateComplete.then(()=>this._catalog?.load())}openWithSearch(e){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0,this.updateComplete.then(()=>this._catalog?.filterByDomain(e))}_clearDetourFields(){this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._depPrefill=null,this._returnValues=null}_resetDetourState(){this._clearDetourFields(),this._bundleQueue=[],this._bundleProgress=null,this._depNavSeq++,this._selectionSeq++}render(){var e;let t=null!==this._selected,i=this.lockedCategories.length>0,a=i?this.boardName?"device.add_config_dialog_title":"device.add_config":this.boardName?"device.add_component_dialog_title":"device.add_component",o=t?function(e,t,i){if(i.core)return e;let a=tE(t);return a?`${e} \xb7 ${a}`:e}(this._selected.name,this._selected.category,{core:i}):this.boardName?this._localize(a,{name:this.boardName}):this._localize(a);return(0,s.qy)`
      <esphome-base-dialog
        class=${t?"form-view":""}
        ?open=${this._dialog.open}
        ?busy=${this._submitting}
        .label=${o}
        @request-close=${this._dialog.onRequestClose}
        @add-component=${this._onComponentSelected}
        @add-bundle=${this._onBundleSelected}
        @form-cancel=${this._onBack}
        @form-submit=${this._onFormSubmit}
        @navigate-to-dep=${this._onNavigateToDep}
        @request-add-component=${this._onNavigateToDep}
      >
        ${t?(0,s.qy)`<button
                slot="header-prefix"
                class="back-button"
                title=${this._localize("layout.back")}
                aria-label=${this._localize("layout.back")}
                @click=${this._onBack}
              >
                <wa-icon library="mdi" name="arrow-left"></wa-icon>
              </button>`:s.s6}
        ${this._returnTo?(0,s.qy)`<div class="return-banner">
                ${this._localize("device.return_to_after_dep_prefix")}
                <strong>${this._returnTo.name}</strong>
                ${this._localize("device.return_to_after_dep_suffix")}
              </div>`:s.s6}
        ${t&&this._bundleProgress?(0,s.qy)`<div class="bundle-banner">
                <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
                <span
                  >${this._localize("device.bundle_step_progress",{current:this._bundleProgress.current,total:this._bundleProgress.total,name:this._bundleProgress.bundleName})}</span
                >
              </div>`:s.s6}
        ${!t&&this._submitError?(0,s.qy)`<div class="catalog-error" role="alert">${this._submitError}</div>`:s.s6}
        <esphome-component-catalog
          ?hidden=${t}
          .platform=${this.platform}
          .boardId=${this.board?.id??""}
          .board=${this.board}
          .yaml=${this.yaml}
          .lockedCategories=${this.lockedCategories}
          .excludeCategories=${(e={isCoreLocked:i,isInDepDetour:null!==this._returnTo}).isCoreLocked||e.isInDepDetour?[]:eM}
        ></esphome-component-catalog>
        ${t?(0,s.qy)`<esphome-add-component-form
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
              ></esphome-add-component-form>`:s.s6}
      </esphome-base-dialog>
    `}async _onComponentSelected(e){e.stopPropagation();let t=await ej(this,e.detail.component.id);if("stale"===t.kind)return;if("error"===t.kind){this._submitError=t.message;return}let i=this._missingRequiredPrereqs(t.entry);if(i&&i.unresolved.length>0){this._submitError=this._localize("device.prereq_unresolved",{name:t.entry.name,ids:i.unresolved.join(", ")});return}if(i&&i.missing.length>0)return void await this._startFeaturedSequence([...i.missing,t.entry.id],i.boardId,this._localize("device.adding_prerequisites_for",{name:t.entry.name}));this._selected=t.entry,this._submitError="";let a=this._fastPathFields(t.entry);a&&await this._submitComponent(a,!0)}_missingRequiredPrereqs(e){let t=this.board;if(!t||!(0,eC.sO)(e.id))return null;let i=t.featured_components??[],a=i.find(i=>(0,eC.m0)(t.id,i.id)===e.id);if(!a?.requires?.length)return null;let o=eE(this.yaml),r=[],s=[];for(let n of a.requires){let a=i.find(e=>e.id===n);if(!a){console.warn(`Featured component '${e.id}' requires '${n}', which is not in the board catalog.`),s.push(n);continue}let l=a.fields.id?.value;"string"==typeof l&&o.has(l)||r.push((0,eC.m0)(t.id,n))}return{boardId:t.id,missing:r,unresolved:s}}async _startFeaturedSequence(e,t,i){let[a,...o]=e,r=await ej(this,a,t);return"stale"!==r.kind&&("error"===r.kind?(this._submitError=r.message,!1):(this._clearDetourFields(),this._bundleQueue=o,this._bundleProgress={current:1,total:e.length,bundleName:i},this._selected=r.entry,this._submitError="",!0))}_fastPathFields(e){var t,i,a;let o,r,s;if(null!==this._prefillReference||null!==this._depPrefill)return null;let n=(0,eS.Zn)(this.yaml);if(eF(e.dependencies??[],this.yaml,n).length>0)return null;let l=tC({entries:e.config_entries,component:e,board:this.board,yaml:this.yaml,prefillReference:null,prefillFields:null,restoredValues:null,localize:this._localize});return(t=e.config_entries,i=e.required_groups??[],r=tx(t,l,i,o=tz(this.board,n)),a=e=>(0,eK.VP)(e,l,o.presentComponents,o.targetPlatform??null),(s=e=>e.some(e=>!e.locked&&a(e)))([...r.visible])||r.clusters.some(e=>s(e.members))||r.ordered.some(e=>Array.isArray(e)&&s(e))||tk({entries:t,requiredGroups:i,values:l,presentComponents:n,targetPlatform:o.targetPlatform??null,formatKeys:()=>""},r.memberKeys).length>0)?null:eZ(e.config_entries,l)}async _onBundleSelected(e){if(e.stopPropagation(),this._submitting)return;let{bundle:t,boardId:i}=e.detail;if(!i||0===t.component_ids.length||!this.configuration)return;let a=t.component_ids.map(e=>(0,eC.m0)(i,e));this._clearDetourFields(),this._submitting=!0,this._submitError="",this._depNavSeq++;let o=this.yaml||void 0,r=null,s=!1,n=async e=>{s&&this._dispatchDraft(this.yaml);let o=await this._startFeaturedSequence(a.slice(e),i,t.name);this._submitting=!1,o&&(r&&(this._prefillReference=r),this._bundleProgress={current:e+1,total:a.length,bundleName:t.name})},l=eE(this.yaml);try{for(let e=0;e<a.length;e++){let t=await ej(this,a[e],i);if("stale"===t.kind){s&&this._dispatchDraft(this.yaml);return}if("error"===t.kind){s&&this._dispatchDraft(this.yaml),this._submitError=t.message;return}let d=t.entry,c=this._fastPathFields(d);if(null===c)return void await n(e);let h=c.id;if("string"==typeof h&&l.has(h)){r=this._chainReference(d,c);continue}let{yaml:p}=await this._api.addComponent(this.configuration,{component_id:a[e],fields:c},o);o=p,s=!0,"string"==typeof h&&l.add(h),this.yaml=p,r=this._chainReference(d,c)}s&&this._dispatchDraft(this.yaml),this._dialog.open=!1,this._selected=null,this._resetDetourState();let e=s?this._localize("device.bundle_added",{name:t.name}):this._localize("device.bundle_already_present",{name:t.name});(0,d.VX)(e)}catch(e){s&&this._dispatchDraft(this.yaml),this._submitError=(0,Y.K)(e,this._localize,"device.add_component_error"),(0,d.UG)(this._submitError)}finally{this._submitting=!1}}_dispatchDraft(e){this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:e},bubbles:!0,composed:!0}))}_chainReference(e,t){let i=t.id;return"string"==typeof i&&e.category?{domain:e.category,id:i}:null}_onBack(){if(!this._submitting){if(this._returnTo){let e=this._returnTo,t=this._returnValues;this._resetDetourState(),this._returnValues=t,this._selected=e,this._submitError="";return}this._resetDetourState(),this._selected=null,this._submitError=""}}_onNavigateToDep(e){return e.stopPropagation(),this._returnValues=this._form?.currentValues??null,eI(this,e.detail.domain)}_onFormSubmit(e){return e.stopPropagation(),this._submitComponent(e.detail.fields)}async _submitComponent(e,t=!1){if(this._selected&&this.configuration&&!this._submitting){this._submitting=!0,this._submitError="",this._depNavSeq++;try{let{yaml:a}=await this._api.addComponent(this.configuration,{component_id:this._selected.id,fields:e},this.yaml||void 0);if(this._dispatchDraft(a),this._returnTo){var i;let t=this._returnTo,a=this._depDomain,o=e.id;a&&"string"==typeof o&&(i=this._selected,i.id===a||i.category===a)?this._prefillReference={domain:a,id:o}:this._prefillReference=null,this._returnTo=null,this._depDomain=null,this._depPrefill=null,this._selected=t}else if(this._bundleQueue.length>0&&this._bundleProgress){let t=this._bundleQueue[0],i=this._bundleQueue.slice(1),a=await ej(this,t);if("stale"===a.kind)return;if("error"===a.kind){this._submitError=a.message;return}let o=a.entry;this._prefillReference=this._chainReference(this._selected,e),this._bundleQueue=i,this._bundleProgress={...this._bundleProgress,current:this._bundleProgress.current+1},this._returnValues=null,this._selected=o}else{let i=this._selected.id,o=this._selected.name,r=e.id,s=(0,C.BB)(a,i,"string"==typeof r?r:void 0);s&&this.dispatchEvent(new CustomEvent("section-select",{detail:s,bubbles:!0,composed:!0})),this._dialog.open=!1,this._selected=null,this._resetDetourState(),t&&(0,d.VX)(this._localize("device.component_added",{name:o}))}}catch(e){this._submitError=(0,Y.K)(e,this._localize,"device.add_component_error"),t&&(0,d.UG)(this._submitError)}finally{this._submitting=!1}}}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml="",this.lockedCategories=[],this._dialog=new H.T(this),this._returnValues=null,this._selected=null,this._submitting=!1,this._submitError="",this._returnTo=null,this._depDomain=null,this._prefillReference=null,this._depPrefill=null,this._bundleQueue=[],this._bundleProgress=null,this._selectionSeq=0,this._depNavSeq=0}}function aO(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aF.styles=[v.G,(0,ez._)("esphome-base-dialog"),ek.c4,eB],aL([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],aF.prototype,"_localize",void 0),aL([(0,o.Fg)({context:m.Ie})],aF.prototype,"_api",void 0),aL([(0,n.MZ)()],aF.prototype,"boardName",void 0),aL([(0,n.MZ)()],aF.prototype,"configuration",void 0),aL([(0,n.MZ)()],aF.prototype,"platform",void 0),aL([(0,n.MZ)({attribute:!1})],aF.prototype,"board",void 0),aL([(0,n.MZ)()],aF.prototype,"yaml",void 0),aL([(0,n.MZ)({attribute:!1})],aF.prototype,"lockedCategories",void 0),aL([(0,n.P)("esphome-component-catalog")],aF.prototype,"_catalog",void 0),aL([(0,n.P)("esphome-add-component-form")],aF.prototype,"_form",void 0),aL([(0,n.wk)()],aF.prototype,"_returnValues",void 0),aL([(0,n.wk)()],aF.prototype,"_selected",void 0),aL([(0,n.wk)()],aF.prototype,"_submitting",void 0),aL([(0,n.wk)()],aF.prototype,"_submitError",void 0),aL([(0,n.wk)()],aF.prototype,"_returnTo",void 0),aL([(0,n.wk)()],aF.prototype,"_depDomain",void 0),aL([(0,n.wk)()],aF.prototype,"_prefillReference",void 0),aL([(0,n.wk)()],aF.prototype,"_depPrefill",void 0),aL([(0,n.wk)()],aF.prototype,"_bundleQueue",void 0),aL([(0,n.wk)()],aF.prototype,"_bundleProgress",void 0),aF=aL([(0,n.EM)("esphome-add-component-dialog")],aF);class aR extends s.WF{open(){this._inner.open()}render(){return(0,s.qy)`<esphome-add-component-dialog
      .lockedCategories=${eM}
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .platform=${this.platform}
      .board=${this.board}
      .yaml=${this.yaml}
    ></esphome-add-component-dialog>`}constructor(...e){super(...e),this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml=""}}aO([(0,n.MZ)()],aR.prototype,"boardName",void 0),aO([(0,n.MZ)()],aR.prototype,"configuration",void 0),aO([(0,n.MZ)()],aR.prototype,"platform",void 0),aO([(0,n.MZ)({attribute:!1})],aR.prototype,"board",void 0),aO([(0,n.MZ)()],aR.prototype,"yaml",void 0),aO([(0,n.P)("esphome-add-component-dialog")],aR.prototype,"_inner",void 0),aR=aO([(0,n.EM)("esphome-add-config-dialog")],aR);var aT=i(4103),aD=i(664);class aI{hostConnected(){this._host.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this._host},bubbles:!0,composed:!0}))}hostDisconnected(){this._clearTimer(),this._host.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this._host},bubbles:!0,composed:!0}))}get dirty(){return this._dirty}get deleting(){return this._deleting}get inFlightWrite(){return this._deleting||this._applyInFlight}shouldSkipReload(){return this._applyInFlight||this._host.yaml===this._lastSelfWrittenYaml}withValue(e){let t={...this._host.value??el(),...e};this._host.value=t,this._host.dispatchEvent(new CustomEvent("automation-change",{detail:{value:t,location:this._host.location},bubbles:!0,composed:!0})),this.scheduleAutoApply()}scheduleAutoApply(){this._host.addMode||this._options.isReadOnly()||(this._setDirty(!0),this._applyTimer&&clearTimeout(this._applyTimer),this._applyTimer=setTimeout(()=>{this._applyTimer=null,this.autoApply()},200))}async flushPending(){if(this._applyTimer)this._clearTimer(),await this.autoApply();else if(this._applyInFlight)for(;this._applyInFlight;)await new Promise(e=>setTimeout(e,20))}async autoApply(){let e=this._options.getApi(),t=this._host.location,i=this._host.value;if(e&&t&&i){if(this._options.isReadOnly())return void this._setDirty(!1);if(!this._options.canApply||this._options.canApply(t)){if(this._applyInFlight){this._applyDirty=!0;return}this._applyInFlight=!0,this._applyDirty=!1;try{let{yaml_diff:a}=await e.upsertAutomation(this._host.configuration,i,t,this._host.yaml),o=ev(this._host.yaml,a);this._lastSelfWrittenYaml=o,this._host.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:o},bubbles:!0,composed:!0}))}catch(e){this._surfaceSaveError(e)}finally{this._applyInFlight=!1,this._applyDirty?(this._applyDirty=!1,this.autoApply()):this._setDirty(!1)}}}}async delete(){let e=this._options.getApi();if(e&&this._host.location&&!this._deleting){this._clearTimer(),this._setDeleting(!0),this._options.setError("");try{let{yaml_diff:t}=await e.deleteAutomation(this._host.configuration,this._host.location,this._host.yaml),i=ev(this._host.yaml,t);await e.updateConfig(this._host.configuration,i),this._host.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:i},bubbles:!0,composed:!0})),this._host.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0}))}catch(e){this._surfaceSaveError(e)}finally{this._setDeleting(!1)}}}_surfaceSaveError(e){let t=this._options.getLocalize(),i=(0,Y.K)(e,t,"device.automation_save_error");this._options.setError(i),(0,d.UG)(t("device.automation_save_error"),{description:i})}_clearTimer(){this._applyTimer&&(clearTimeout(this._applyTimer),this._applyTimer=null)}_setDirty(e){this._dirty!==e&&(this._dirty=e,this._host.requestUpdate(),this._host.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_setDeleting(e){this._deleting=e,this._host.requestUpdate()}constructor(e,t){this._host=e,this._options=t,this._applyTimer=null,this._applyInFlight=!1,this._applyDirty=!1,this._lastSelfWrittenYaml=null,this._dirty=!1,this._deleting=!1,e.addController(this)}}let aj=(0,s.AH)`
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
`,aB=(0,s.AH)`
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
  /* Input and wa-select chrome both come from the shared inputStyles,
     keyed on --wa-form-control-height, so the pair stays equal-height. */
  .ae-delay-row wa-select {
    width: 100%;
  }
`,aN=(0,s.AH)`
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
`,aZ=[(0,s.AH)`
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
`,aN,aB,aj,ta];function aK(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({close:r.mdiClose,magnify:r.mdiMagnify,plus:r.mdiPlus});class aU extends s.WF{open(){this._activeTab="action"===this.kind?"by-target":"by-type",this._query="",this._dialog.open=!0}render(){let e="action"===this.kind?this._localize("device.automation_pick_action"):this._localize("device.automation_pick_condition"),t=this._localize("device.automation_pick_search"),i="action"===this.kind?["by-target","by-type","building-blocks"]:["by-type","building-blocks"];return(0,s.qy)`<esphome-base-dialog
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
        ${i.map(e=>(0,s.qy)`<button
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
    </esphome-base-dialog>`}_tabLabel(e){switch(e){case"by-target":return this._localize("device.automation_pick_tab_by_target");case"by-type":return this._localize("device.automation_pick_tab_by_type");case"building-blocks":return this._localize("device.automation_pick_tab_building_blocks")}}_renderActiveTab(){let e=this._applyQuery(this.items);switch(this._activeTab){case"by-target":return this._renderByTarget(e);case"by-type":return this._renderByType(e);case"building-blocks":return this._renderBuildingBlocks(e)}}_applyQuery(e){let t=this._query.trim().toLowerCase();return t?e.filter(e=>e.id.toLowerCase().includes(t)||e.name.toLowerCase().includes(t)||(e.description??"").toLowerCase().includes(t)):e}_renderByTarget(e){if(0===this.devices.length)return(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_targets")}
      </p>`;let t=this.devices.filter(ea).map(t=>{let i=et(t.component_id),a=e.filter(e=>"domain"in e&&(e.domain===i||e.domain===t.component_id));return{device:t,matching:a}}).filter(e=>e.matching.length>0);return 0===t.length?(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,s.qy)`${t.map(({device:e,matching:t})=>(0,s.qy)`
        <p class="picker-group-label">
          ${ee(e)}
          <span class="ae-muted">(${ei(e,this.devices)})</span>
        </p>
        ${t.map(t=>this._renderRow(t,()=>this._pick(t.id,this._preFillFor(t,e))))}
      `)}`}_renderByType(e){let t=new Map;for(let i of e){if(!("domain"in i)||"core"===i.domain)continue;let e=et(i.domain),a=t.get(e)??[];a.push(i),t.set(e,a)}let i=Array.from(t.keys()).sort();return 0===i.length?(0,s.qy)`<p class="picker-empty">
        ${this._localize("device.automation_pick_no_results")}
      </p>`:(0,s.qy)`${i.map(e=>(0,s.qy)`
        <p class="picker-group-label">${e}</p>
        ${(t.get(e)??[]).map(e=>this._renderRow(e,()=>this._pick(e.id)))}
      `)}`}_renderBuildingBlocks(e){let t=e.filter(e=>"domain"in e&&"core"===e.domain);return 0===t.length?(0,s.qy)`<p class="picker-empty">
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
        ${e.description?(0,s.qy)`<span class="picker-row-desc">
                ${(0,B.Gc)(e.description)}
              </span>`:s.s6}
      </div>
      <span class="picker-row-add" aria-hidden="true">
        <wa-icon library="mdi" name="plus"></wa-icon>
      </span>
    </div>`}_preFillFor(e,t){let i=et(t.component_id),a=e.config_entries.find(e=>e.references_component===i);if(a)return{[a.key]:t.id}}_pick(e,t){this.dispatchEvent(new CustomEvent("catalog-picked",{detail:{id:e,preFilledParams:t},bubbles:!0,composed:!0})),this._dialog.open=!1}constructor(...e){super(...e),this._localize=e=>e,this.kind="action",this.items=[],this.devices=[],this._dialog=new H.T(this),this._activeTab="by-target",this._query=""}}function aV(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aU.styles=[v.G,G.z9,(0,s.AH)`
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
    `],aK([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],aU.prototype,"_localize",void 0),aK([(0,n.MZ)()],aU.prototype,"kind",void 0),aK([(0,n.MZ)({attribute:!1})],aU.prototype,"items",void 0),aK([(0,n.MZ)({attribute:!1})],aU.prototype,"devices",void 0),aK([(0,n.wk)()],aU.prototype,"_activeTab",void 0),aK([(0,n.wk)()],aU.prototype,"_query",void 0),aU=aK([(0,n.EM)("esphome-catalog-picker-dialog")],aU),(0,k.C)({"arrow-down":r.mdiArrowDown,"arrow-up":r.mdiArrowUp,close:r.mdiClose,delete:r.mdiDelete,"pencil-outline":r.mdiPencilOutline,plus:r.mdiPlus});class aG extends s.WF{render(){return(0,s.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?s.s6:(0,s.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_only_when")}</label
              >`}
        ${0===this.conditions.length?(0,s.qy)`<p class="ae-empty">${this._localize("device.add_condition")}</p>`:this.conditions.map((e,t)=>this._renderNode(e,t))}
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
    `}_renderNode(e,t){let i=this.catalog.find(t=>t.id===e.condition_id),a=this.conditions.length-1;return(0,s.qy)`
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
          ${i?.description?(0,s.qy)`<p class="ae-row-desc">${(0,B.Gc)(i.description)}</p>`:s.s6}
          ${i&&i.config_entries.length>0?(0,s.qy)`<esphome-config-entry-form
                  .entries=${i.config_entries}
                  .values=${e.params}
                  .board=${this.board}
                  .yaml=${this.yaml}
                  ?disabled=${this.disabled}
                  @value-change=${e=>this._onParamChange(t,e)}
                ></esphome-config-entry-form>`:s.s6}
          ${i?.accepts_condition_list?(0,s.qy)`<div class="ae-nested">
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
                </div>`:s.s6}
        </div>
      </div>
    `}_openPickerForChange(e){0!==this.catalog.length&&(this._changingIdx=e,this._picker.open())}_onParamChange(e,t){t.stopPropagation();let i=this.conditions[e],a=ed(i.params,t.detail.path,t.detail.value);this._emit(ec(this.conditions,e,{...i,params:a}))}_onChildrenChange(e,t){t.stopPropagation();let i=this.conditions[e];this._emit(ec(this.conditions,e,{...i,children:t.detail.conditions}))}_move(e,t){this._emit(ep(this.conditions,e,t))}_remove(e){this._emit(eh(this.conditions,e))}_emit(e){this.dispatchEvent(new CustomEvent("conditions-change",{detail:{conditions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.conditions=[],this.catalog=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.devices=[],this._changingIdx=-1,this._openPickerForAdd=()=>{0!==this.catalog.length&&(this._changingIdx=-1,this._picker.open())},this._onConditionPicked=e=>{e.stopPropagation();let t={condition_id:e.detail.id,params:{},children:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._changingIdx>=0?this._emit(ec(this.conditions,this._changingIdx,t)):this._emit([...this.conditions,t]),this._changingIdx=-1}}}aG.styles=[v.G,G.z9,aZ],aV([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],aG.prototype,"_localize",void 0),aV([(0,n.MZ)({attribute:!1})],aG.prototype,"conditions",void 0),aV([(0,n.MZ)({attribute:!1})],aG.prototype,"catalog",void 0),aV([(0,n.MZ)({attribute:!1})],aG.prototype,"board",void 0),aV([(0,n.MZ)()],aG.prototype,"yaml",void 0),aV([(0,n.MZ)({type:Boolean})],aG.prototype,"disabled",void 0),aV([(0,n.MZ)({type:Boolean,attribute:"no-header"})],aG.prototype,"noHeader",void 0),aV([(0,n.MZ)({attribute:!1})],aG.prototype,"devices",void 0),aV([(0,n.P)("esphome-catalog-picker-dialog")],aG.prototype,"_picker",void 0),aV([(0,n.wk)()],aG.prototype,"_changingIdx",void 0),aG=aV([(0,n.EM)("esphome-automation-condition-tree")],aG);let aH={us:"microseconds",ms:"milliseconds",s:"seconds",min:"minutes",h:"hours",d:"days"};function aW(e){let t=e.id;return(0,i_.b)(t)?t:null}function aY(e){for(let t of it){let i=e[aH[t]];if(void 0!==i&&""!==i&&null!==i)return{value:String(i),unit:t}}let t=e.id;if("string"==typeof t&&is(t)){let e=il(t);return{value:e.value,unit:e.unit}}return{value:"",unit:"s"}}function aQ(e){let t={...e};for(let e of it)delete t[aH[e]];return delete t.id,t}function aJ(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({"arrow-down":r.mdiArrowDown,"arrow-up":r.mdiArrowUp,"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,close:r.mdiClose,delete:r.mdiDelete,"pencil-outline":r.mdiPencilOutline});class aX extends s.WF{willUpdate(e){if(!e.has("value"))return;let t=e.get("value");t&&t.action_id!==this.value.action_id&&(this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null)}render(){let e=this.catalog.find(e=>e.id===this.value.action_id),t=this._collapsed;return(0,s.qy)`
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
        ${t?s.s6:(0,s.qy)`<div class="ae-row-body">
                ${e?.description?(0,s.qy)`<p class="ae-row-desc">${(0,B.Gc)(e.description)}</p>`:s.s6}
                ${this._renderActionParams(e)} ${this._renderScriptParams(e)}
                ${this._renderConditionGate(e)} ${this._renderNestedLists(e)}
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
              @input=${t=>{let i=t.target.value,a="int"===e.type?""===i?"":parseInt(i,10):"float"===e.type?""===i?"":Number(i):i;this._patchParams({[e.name]:a})}}
            />`)}
    </div>`:s.s6}_renderConditionGate(e){return e&&("if"===e.id||"wait_until"===e.id)?(0,s.qy)`<div class="ae-nested">
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
    </div>`:s.s6}_nestedListLabel(e){return"else"===e?this._localize("device.automation_else"):"then"===e?this._localize("device.automation_action"):e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}_renderNestedLists(e){return e&&e.accepts_action_list&&0!==e.accepts_action_list.length?e.accepts_action_list.map(e=>(0,s.qy)`<div class="ae-nested">
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
        </div>`):s.s6}_renderActionParams(e){return e?"delay"===e.id?this._renderDelayParams():0===e.config_entries.length?s.s6:(0,s.qy)`<esphome-config-entry-form
      .entries=${e.config_entries}
      .values=${this.value.params}
      .board=${this.board}
      .yaml=${this.yaml}
      ?disabled=${this.disabled}
      advanced-section
      ?show-advanced=${this._showAdvanced}
      @value-change=${this._onParamChange}
      @advanced-toggle=${this._onAdvancedToggle}
    ></esphome-config-entry-form>`:s.s6}_renderDelayParams(){var e,t,i;let a;return a=aW((e={params:this.value.params??{},disabled:this.disabled,localize:this._localize,onWrite:(e,t)=>this._writeDelay(e,t),onWriteLambda:e=>this._writeDelayLambda(e),onToggle:e=>this._toggleDelayLambda(e)}).params),(0,s.qy)`<div class="ae-delay">
    ${tt({isLambda:null!==a,disabled:e.disabled,localize:e.localize,onSwitch:t=>e.onToggle(t)})}
    ${a?(t=a,i=e,(0,s.qy)`<esphome-lambda-editor
    .value=${i4(t)}
    ?disabled=${i.disabled}
    @lambda-change=${e=>i.onWriteLambda(e.detail.value)}
  ></esphome-lambda-editor>`):function(e){let{value:t,unit:i}=aY(e.params);return(0,s.qy)`<div class="ae-delay-row">
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
        ${it.map(t=>(0,s.qy)`<wa-option value=${t} ?selected=${t===i}>
              ${e.localize(`device.automation_action_delay_unit_${t}`)}
            </wa-option>`)}
      </wa-select>
    </div>
  </div>`}(e)}
  </div>`}_toggleDelayLambda(e){let t=this.value.params??{},i=aW(t);if(e!==(null!==i))if(e)this._delayLiteralStash=aY(t),this._writeDelayLambda(this._delayLambdaStash);else{this._delayLambdaStash=i4(i);let{value:e,unit:t}=this._delayLiteralStash??{value:"",unit:"s"};this._writeDelay(e,t)}}_writeDelay(e,t){var i;let a,o;this._emit({...this.value,params:(i=this.value.params??{},a=e.trim(),o=aQ(i),a&&(o[aH[t]]=a),o)})}_writeDelayLambda(e){var t;let i;this._delayLambdaStash=e,this._emit({...this.value,params:(t=this.value.params??{},(i=aQ(t)).id={_lambda:e,_tag:"!lambda"},i)})}_patchParams(e){this._emit({...this.value,params:{...this.value.params,...e}})}_onChildrenChange(e,t){let i={...this.value.children??{},[e]:t};this._emit({...this.value,children:i})}_reorder(e){this.dispatchEvent(new CustomEvent("action-reorder",{detail:{delta:e},bubbles:!0,composed:!0}))}_emit(e){this.dispatchEvent(new CustomEvent("action-change",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.first=!1,this.last=!1,this._collapsed=!1,this._showAdvanced=!1,this._delayLambdaStash="",this._delayLiteralStash=null,this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._openPicker=()=>{this._picker.open()},this._onActionPicked=e=>{e.stopPropagation(),this._emit({action_id:e.detail.id,params:{...e.detail.preFilledParams??{}},children:{},conditions:[]})},this._onParamChange=e=>{e.stopPropagation();let t=ed(this.value.params,e.detail.path,e.detail.value);this._emit({...this.value,params:t})},this._onConditionsChange=e=>{e.stopPropagation(),this._emit({...this.value,conditions:e.detail.conditions})},this._onDelete=()=>{this.dispatchEvent(new CustomEvent("action-delete",{bubbles:!0,composed:!0}))}}}function a0(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}aX.styles=[v.G,G.z9,aZ,te],aJ([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],aX.prototype,"_localize",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"value",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"catalog",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"conditionCatalog",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"scripts",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"devices",void 0),aJ([(0,n.MZ)({attribute:!1})],aX.prototype,"board",void 0),aJ([(0,n.MZ)()],aX.prototype,"yaml",void 0),aJ([(0,n.MZ)({type:Boolean})],aX.prototype,"disabled",void 0),aJ([(0,n.MZ)({type:Boolean})],aX.prototype,"first",void 0),aJ([(0,n.MZ)({type:Boolean})],aX.prototype,"last",void 0),aJ([(0,n.P)("esphome-catalog-picker-dialog")],aX.prototype,"_picker",void 0),aJ([(0,n.wk)()],aX.prototype,"_collapsed",void 0),aJ([(0,n.wk)()],aX.prototype,"_showAdvanced",void 0),aJ([(0,n.wk)()],aX.prototype,"_delayLambdaStash",void 0),aJ([(0,n.wk)()],aX.prototype,"_delayLiteralStash",void 0),aX=aJ([(0,n.EM)("esphome-automation-action-node")],aX),(0,k.C)({plus:r.mdiPlus});class a1 extends s.WF{render(){return(0,s.qy)`
      <div class=${this.noHeader?"":"ae-section"}>
        ${this.noHeader?s.s6:(0,s.qy)`<label class="ae-section-label"
                >${this._localize("device.automation_action")}</label
              >`}
        ${0===this.actions.length?(0,s.qy)`<p class="ae-empty-block" role="status">
                ${this._localize("device.automation_actions_empty")}
              </p>`:this.actions.map((e,t)=>this._renderRow(e,t,t===this.actions.length-1))}
        ${this.hideAdd?s.s6:(0,s.qy)`<button
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
    `}_renderRow(e,t,i){return(0,s.qy)`<esphome-automation-action-node
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
    ></esphome-automation-action-node>`}_onActionChange(e,t){t.stopPropagation(),this._emit(ec(this.actions,e,t.detail.value))}_onReorder(e,t){t.stopPropagation(),this._emit(ep(this.actions,e,e+t.detail.delta))}_onDelete(e,t){t.stopPropagation(),this._emit(eh(this.actions,e))}_emit(e){this.dispatchEvent(new CustomEvent("actions-change",{detail:{actions:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.actions=[],this.catalog=[],this.conditionCatalog=[],this.scripts=[],this.devices=[],this.board=null,this.yaml="",this.disabled=!1,this.noHeader=!1,this.hideAdd=!1,this.openPicker=()=>{0!==this.catalog.length&&this._picker.open()},this._onActionPicked=e=>{e.stopPropagation();let t={action_id:e.detail.id,params:{},children:{},conditions:[]};e.detail.preFilledParams&&(t.params={...t.params,...e.detail.preFilledParams}),this._emit([...this.actions,t])}}}function a2(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}a1.styles=[v.G,G.z9,aZ],a0([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],a1.prototype,"_localize",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"actions",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"catalog",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"conditionCatalog",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"scripts",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"devices",void 0),a0([(0,n.MZ)({attribute:!1})],a1.prototype,"board",void 0),a0([(0,n.MZ)()],a1.prototype,"yaml",void 0),a0([(0,n.MZ)({type:Boolean})],a1.prototype,"disabled",void 0),a0([(0,n.MZ)({type:Boolean,attribute:"no-header"})],a1.prototype,"noHeader",void 0),a0([(0,n.MZ)({type:Boolean,attribute:"hide-add"})],a1.prototype,"hideAdd",void 0),a0([(0,n.P)("esphome-catalog-picker-dialog")],a1.prototype,"_picker",void 0),a1=a0([(0,n.EM)("esphome-automation-action-list")],a1),(0,k.C)({close:r.mdiClose,plus:r.mdiPlus});let a6=["int","float","bool","string"];class a3 extends s.WF{updated(e){if(!e.has("value"))return;let t=this._readFromWire(),i=this._params.filter(e=>e.name);i.length===t.length&&i.every((e,i)=>e.name===t[i].name&&e.type===t[i].type)||(this._params=t)}render(){return(0,s.qy)`<div class="field">
      ${this.fieldLabel?(0,s.qy)`<label class="field-label">${this.fieldLabel}</label>`:s.s6}
      ${this.description?(0,s.qy)`<p class="field-description">${(0,B.Gc)(this.description)}</p>`:s.s6}
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
        @input=${i=>this._updateRow(t,{...e,name:(0,aD.e)(i.target.value)})}
      />
      <wa-select
        value=${e.type}
        ?disabled=${this.disabled}
        @change=${i=>this._updateRow(t,{...e,type:i.target.value})}
      >
        ${a6.map(t=>(0,s.qy)`<wa-option value=${t} ?selected=${t===e.type}>${t}</wa-option>`)}
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
    </div>`}_readFromWire(){return this.value&&"object"==typeof this.value?Object.entries(this.value).map(([e,t])=>({name:e,type:String(t??"string")})):[]}_emit(e){this._params=e;let t={};for(let{name:i,type:a}of e)i&&(t[i]=a);this.dispatchEvent(new CustomEvent("value-change",{detail:{value:t},bubbles:!0,composed:!0}))}_updateRow(e,t){let i=this._params.slice();i[e]=t,this._emit(i)}_removeRow(e){let t=this._params.slice();t.splice(e,1),this._emit(t)}constructor(...e){super(...e),this._localize=e=>e,this.value={},this.disabled=!1,this.fieldLabel="",this.description="",this.addLabel="",this.namePlaceholder="",this._params=[],this._addRow=()=>{this._emit([...this._params,{name:"",type:"int"}])}}}a3.styles=[v.G,G.z9,aZ],a2([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],a3.prototype,"_localize",void 0),a2([(0,n.MZ)({attribute:!1})],a3.prototype,"value",void 0),a2([(0,n.MZ)({type:Boolean})],a3.prototype,"disabled",void 0),a2([(0,n.MZ)()],a3.prototype,"fieldLabel",void 0),a2([(0,n.MZ)()],a3.prototype,"description",void 0),a2([(0,n.MZ)()],a3.prototype,"addLabel",void 0),a2([(0,n.MZ)()],a3.prototype,"namePlaceholder",void 0),a2([(0,n.wk)()],a3.prototype,"_params",void 0),a3=a2([(0,n.EM)("esphome-callable-params-editor")],a3);let a4=["triggers","actions","conditions"];async function a5(e,t,i,a=a4){let o=iq(),r=[],s=(t,a)=>{for(let s of a)r.push(iC(e,t,s,i).then(e=>{iE(o,e)}))};for(let e of(a.includes("triggers")&&s("triggers",t.triggers),a.includes("actions")&&s("actions",t.actions),a.includes("conditions")&&s("conditions",t.conditions),await Promise.allSettled(r)))"rejected"===e.status&&(o.rejected++,console.warn("automation-editor: body fetch failed",e.reason));return o}async function a8(e,t,i){try{let a=await e.getAvailableAutomations(t,i?.yaml);if(i?.isStale?.())return{status:"stale"};let o={...a,triggers:a.triggers.map(e=>({...e})),actions:a.actions.map(e=>({...e})),conditions:a.conditions.map(e=>({...e}))};i?.onPaint?.(o);let r=await a5(e,o,void 0,i?.lists);if(i?.isStale?.())return{status:"stale"};let s={...o,triggers:[...o.triggers],actions:[...o.actions],conditions:[...o.conditions]};return{status:"ok",available:s,hydration:r}}catch(e){if(i?.isStale?.())return{status:"stale"};return{status:"error",error:e}}}class a9{hostDisconnected(){this._seq++}async load(e,t,i,a){if(!e||!t)return{};let o=++this._seq,r=a?.onPaint,s=await a8(e,t,{isStale:()=>o!==this._seq,yaml:a?.yaml,lists:a?.lists??["actions","conditions"],onPaint:r?e=>{o===this._seq&&r(e)}:void 0});return o!==this._seq?{}:function(e,t){if("stale"===e.status)return{};if("error"===e.status)return{error:(0,W.u)(e.error)};let{missingBody:i,missingField:a,rejected:o}=e.hydration,r=i+a+o;return r>0&&(0,d.UG)(t("device.automation_partial_hydration",{count:r})),{available:e.available}}(s,i)}constructor(e){this._seq=0,e.addController(this)}}class a7{hostConnected(){}get active(){return this._active}resolve(e,t,i){let a=em(t),o=e.find(e=>em(e.location)===a);return!o||i&&o.location.kind!==i?(this._set(null),null):(this._set(o.error??null,o.unsupported??!1),null!=o.error)?null:{tree:o.automation,location:o.location}}renderPanel(e){return this._unsupported?(0,s.qy)`<div class="ae-empty-block" role="note">
        <p>${e("device.yaml_only_section")}</p>
      </div>`:(0,s.qy)`<div class="ae-empty-block" role="alert">
      <p class="ae-error">${e("device.automation_parse_error")}</p>
      ${this._message?(0,s.qy)`<p>${this._message}</p>`:s.s6}
    </div>`}_set(e,t=!1){let i=null!=e;(this._active!==i||this._message!==(e??"")||this._unsupported!==t)&&(this._active=i,this._message=e??"",this._unsupported=t,this._host.requestUpdate())}constructor(e){this._host=e,this._active=!1,this._message="",this._unsupported=!1,e.addController(this)}}function oe(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({delete:r.mdiDelete,"open-in-new":r.mdiOpenInNew,webhook:r.mdiWebhook});let ot=`${aT.Ik}/components/api.html`;class oi extends s.WF{get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._load()}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.action_name!==this.location.action_name&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}flushPending(){return this._engine.flushPending()}render(){if(this._loading)return(0,s.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??el(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._engine.deleting;return(0,s.qy)`
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
          ${(0,B.Gc)(this._localize("device.api_action_actions_description"))}
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
      ${this._error?(0,s.qy)`<p class="ae-error" role="alert">${this._error}</p>`:s.s6}
      ${this.location&&this.value&&!this.addMode?(0,s.qy)`<div class="ae-actions">
              <button
                type="button"
                class="ae-danger"
                ?disabled=${r}
                @click=${this._onDelete}
              >
                <wa-icon library="mdi" name="delete"></wa-icon>
                ${this._localize("dashboard.delete")}
              </button>
            </div>`:s.s6}
    `}_renderHeader(){return(0,s.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">
          ${this._localize("device.api_action_header_title_static")}
        </h2>
        <a class="ae-header-docs" href=${ot} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">
          ${(0,B.Gc)(this._localize("device.api_action_header_description"))}
        </p>
      </div>
      <div class="ae-header-icon">
        <wa-icon library="mdi" name="webhook"></wa-icon>
      </div>
    </div>`}_renderActionNameField(e){let t=this.location?.action_name??"";return(0,s.qy)`<div class="field">
      <label class="field-label" for="api-action-name">
        ${this._localize("device.api_action_id_label")}
      </label>
      <p class="field-description">
        ${(0,B.Gc)(this._localize("device.api_action_id_description"))}
      </p>
      <input
        id="api-action-name"
        type="text"
        .value=${t}
        ?disabled=${e}
        ?readonly=${!this.addMode}
        @input=${e=>this._onActionNameChange(e.target.value)}
      />
    </div>`}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable()}catch(e){this._error=(0,W.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"api_action");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,Y.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}_onActionNameChange(e){let t=(0,aD.e)(e);t&&(this.location={kind:"api_action",action_name:t},this._engine.scheduleAutoApply())}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._error="",this._parseError=new a7(this),this._engine=new aI(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,canApply:e=>"api_action"===e.kind&&!!e.action_name,setError:e=>{this._error=e}}),this._catalogLoad=new a9(this),this._onVariablesChange=e=>{e.stopPropagation();let t=this.value??el();this._engine.withValue({trigger_params:{...t.trigger_params,variables:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}async function oa(e,t,i){let a=(0,eD.CQ)("interval",t,i);if(a)return a;try{return await (0,eD.Sn)(e,"interval",t,i)??null}catch{return null}}function oo(e,t){let i=((e.endsWith("_action")?e.slice(0,-7):e)||e).replace(/_/g," ").trim()||"action";return t("device.action_field_label",{name:i[0].toUpperCase()+i.slice(1)})}function or(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}oi.styles=[v.G,G.z9,aZ],oe([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],oi.prototype,"_localize",void 0),oe([(0,o.Fg)({context:m.Ie})],oi.prototype,"_api",void 0),oe([(0,n.MZ)()],oi.prototype,"configuration",void 0),oe([(0,n.MZ)({attribute:!1})],oi.prototype,"board",void 0),oe([(0,n.MZ)()],oi.prototype,"platform",void 0),oe([(0,n.MZ)({attribute:!1})],oi.prototype,"value",void 0),oe([(0,n.MZ)({attribute:!1})],oi.prototype,"location",void 0),oe([(0,n.MZ)({type:Boolean,attribute:"add-mode"})],oi.prototype,"addMode",void 0),oe([(0,n.MZ)()],oi.prototype,"yaml",void 0),oe([(0,n.wk)()],oi.prototype,"_available",void 0),oe([(0,n.wk)()],oi.prototype,"_loading",void 0),oe([(0,n.wk)()],oi.prototype,"_error",void 0),oi=oe([(0,n.EM)("esphome-api-action-editor")],oi),(0,k.C)({"arrow-decision-outline":r.mdiArrowDecisionOutline,"open-in-new":r.mdiOpenInNew});let os=["device_on","component_on","interval","script"];class on extends s.WF{render(){let e=this.value&&"component_action"!==this.value.kind?this.value.kind:"device_on";return(0,s.qy)`
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
          ${os.map(t=>(0,s.qy)`<wa-option value=${t} ?selected=${t===e}
                >${this._kindLabel(t)}</wa-option
              >`)}
        </wa-select>
        ${this._renderKindBody(e)}
      </div>
    `}_kindLabel(e){switch(e){case"device_on":return this._localize("device.automation_target_device");case"component_on":return this._localize("device.automation_target_component");case"interval":return this._localize("device.automation_target_interval");case"script":return this._localize("device.automation_target_script");case"api_action":return this._localize("device.automation_target_api_action");case"light_effect":return this._localize("device.automation_light_effect")}}_renderKindBody(e){if("device_on"===e||"interval"===e)return s.s6;if("component_on"===e){let e=this.value?.kind==="component_on"?this.value.component_id:"",t=this.devices.filter(ea);return 0===t.length?(0,s.qy)`<p class="ae-empty" role="status">
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
                >${ee(t)}
                <span class="ae-muted"
                  >(${ei(t,this.devices)})</span
                ></wa-option
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
                >${ee(t)}</wa-option
              >`)}
        </wa-select>
      `}return s.s6}_onKindChange(e){let t=e.target.value,i=(()=>{switch(t){case"device_on":return{kind:t,trigger:"on_boot"};case"interval":return{kind:t,index:0};case"component_on":{let e=eo(this.devices);return e?{kind:t,component_id:e.id,trigger:""}:null}case"script":return{kind:t,id:this.scripts.length?this.scripts[0].id:""};case"light_effect":{let e=this.devices.find(e=>e.component_id.startsWith("light."));return e?{kind:t,component_id:e.id,index:0}:null}case"api_action":return null}})();this._emit(i)}_onComponentChange(e){this.value?.kind==="component_on"&&this._emit({...this.value,component_id:e})}_onScriptChange(e){this._emit({kind:"script",id:e})}_onLightChange(e){this.value?.kind==="light_effect"&&this._emit({...this.value,component_id:e})}_emit(e){this.dispatchEvent(new CustomEvent("target-change",{detail:{target:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value=null,this.devices=[],this.scripts=[],this.disabled=!1,this.locked=!1}}function ol(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}on.styles=[v.G,G.z9,aZ],or([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],on.prototype,"_localize",void 0),or([(0,n.MZ)({attribute:!1})],on.prototype,"value",void 0),or([(0,n.MZ)({attribute:!1})],on.prototype,"devices",void 0),or([(0,n.MZ)({attribute:!1})],on.prototype,"scripts",void 0),or([(0,n.MZ)({type:Boolean})],on.prototype,"disabled",void 0),or([(0,n.MZ)({type:Boolean})],on.prototype,"locked",void 0),on=or([(0,n.EM)("esphome-automation-target-picker")],on);class od extends s.WF{render(){if(!this.target)return(0,s.qy)`<p class="ae-empty">
        ${this._localize("device.automation_target_placeholder")}
      </p>`;if("interval"===this.target.kind||"script"===this.target.kind||"api_action"===this.target.kind||"light_effect"===this.target.kind)return s.s6;let e=this._filteredTriggers(),t=e.find(e=>e.id===this.triggerId),i="component_on"===this.target.kind?this.target.component_id:null,a=i?this.devices.find(e=>e.id===i)??null:null;return(0,s.qy)`
      <div class="ae-section">
        <label class="ae-section-label" id="trigger-label"
          >${this._localize("device.automation_trigger")}</label
        >
        ${a?(0,s.qy)`<p class="ae-section-desc">
                ${this._localize("device.automation_trigger_on_component",{component:ee(a),domain:a.component_id})}
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
        ${t?.description?(0,s.qy)`<p class="ae-section-desc">${(0,B.Gc)(t.description)}</p>`:s.s6}
        ${t&&t.config_entries.length>0?(0,s.qy)`<esphome-config-entry-form
                .entries=${t.config_entries}
                .values=${this.triggerParams}
                .board=${this.board}
                .yaml=${this.yaml}
                ?disabled=${this.disabled}
                @value-change=${this._onParamChange}
              ></esphome-config-entry-form>`:s.s6}
      </div>
    `}_filteredTriggers(){if(!this.target)return[];if("device_on"===this.target.kind)return this.triggers.filter(e=>e.is_device_level);if("component_on"===this.target.kind){let e=this.target.component_id,t=this.devices.find(t=>t.id===e);return es(this.triggers,t)}return[]}constructor(...e){super(...e),this._localize=e=>e,this.target=null,this.triggers=[],this.devices=[],this.triggerId=null,this.triggerParams={},this.board=null,this.yaml="",this.disabled=!1,this._onTriggerChange=e=>{let t=e.target.value;this.dispatchEvent(new CustomEvent("trigger-change",{detail:{triggerId:t,params:{}},bubbles:!0,composed:!0}))},this._onParamChange=e=>{e.stopPropagation();let t=ed(this.triggerParams,e.detail.path,e.detail.value);this.dispatchEvent(new CustomEvent("trigger-params-change",{detail:{params:t},bubbles:!0,composed:!0}))}}}function oc(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}od.styles=[v.G,G.z9,aZ],ol([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],od.prototype,"_localize",void 0),ol([(0,n.MZ)({attribute:!1})],od.prototype,"target",void 0),ol([(0,n.MZ)({attribute:!1})],od.prototype,"triggers",void 0),ol([(0,n.MZ)({attribute:!1})],od.prototype,"devices",void 0),ol([(0,n.MZ)()],od.prototype,"triggerId",void 0),ol([(0,n.MZ)({attribute:!1})],od.prototype,"triggerParams",void 0),ol([(0,n.MZ)({attribute:!1})],od.prototype,"board",void 0),ol([(0,n.MZ)()],od.prototype,"yaml",void 0),ol([(0,n.MZ)({type:Boolean})],od.prototype,"disabled",void 0),od=ol([(0,n.EM)("esphome-automation-trigger-picker")],od),(0,k.C)({delete:r.mdiDelete});class oh extends s.WF{get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._editMode=!this.addMode}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&em(t)!==em(this.location)&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend(),(e.has("location")||e.has("platform"))&&this.location?.kind==="interval"&&this._loadIntervalComponent()}async _loadIntervalComponent(){if(!this._api)return;let e=await oa(this._api,this.platform||void 0,this.board?.id);e&&(this._intervalComponent=e)}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml);this._error="";let t=this._parseError.resolve(e,this.location);t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,Y.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}async _loadAvailable(){if(!this._api||!this.configuration)return;this._loading=!0,this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize,{lists:["triggers","actions","conditions"],yaml:this.yaml,onPaint:e=>{this._available=e,this._loading=!1}});void 0!==t&&(this._error=t,this._loading=!1),e&&(this._available=e,this._loading=!1)}render(){var e,t,i,a,o,r,n,l,d,c,h;let p,u,m,v,g,f;if(this._loading)return(0,s.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let _=this.value??el(),b=this.location,y=this._available?.devices??[],w=this._available?.scripts??[],$=this._available?.triggers??[],x=this._available?.actions??[],k=this._available?.conditions??[],z=this._engine.deleting,C=_.trigger_id??(b?.kind==="device_on"?b.trigger||null:b?.kind==="component_on"&&function(e,t){if("component_on"!==e.kind||!e.trigger)return null;let i=t.find(t=>t.id===e.component_id),a=i?et(i.component_id):null;return a?`${a}.${e.trigger}`:e.trigger}(b,y)||null),q=C?$.find(e=>e.id===C)??null:null;return(0,s.qy)`
      ${e=this.location,t=this._intervalComponent,i=this._localize,p=e?.kind==="interval"?t:null,u=p?.name??(e?.kind==="interval"?i("device.automation_interval_label"):q&&(e?.kind==="device_on"||e?.kind==="component_on")?q.name:e?.kind==="component_action"?oo(e.field,i):i("device.automation_header_title_static")),m=p?.docs_url??q?.docs_url??"",v=p?.description??q?.description??i("device.automation_header_description"),g=p?.image_url??"",(0,s.qy)`<div class="ae-header">
    <div class="ae-header-text">
      <h2 class="ae-header-title">${u}</h2>
      ${m?(0,s.qy)`<a
              class="ae-header-docs"
              href=${m}
              target="_blank"
              rel="noreferrer"
            >
              ${i("device.docs")}
              <wa-icon library="mdi" name="open-in-new"></wa-icon>
            </a>`:s.s6}
      <p class="ae-header-desc">${(0,B.Gc)(v)}</p>
    </div>
    <div class="ae-header-icon">
      ${g?(0,s.qy)`<img alt="" src=${g} />`:(0,s.qy)`<wa-icon library="mdi" name="arrow-decision-outline"></wa-icon>`}
    </div>
  </div>`}
      ${this.addMode?(a={target:b,triggers:$,devices:y,scripts:w,effectiveTriggerId:C,automation:_,board:this.board,yaml:this.yaml,disabled:z,onTargetChange:this._onTargetChange,onTriggerChange:this._onTriggerChange,onTriggerParamsChange:this._onTriggerParamsChange},(0,s.qy)`
    <esphome-automation-target-picker
      .value=${a.target}
      .devices=${a.devices}
      .scripts=${a.scripts}
      ?disabled=${a.disabled}
      @target-change=${a.onTargetChange}
    ></esphome-automation-target-picker>
    <esphome-automation-trigger-picker
      .target=${a.target}
      .triggers=${a.triggers}
      .devices=${a.devices}
      .triggerId=${a.effectiveTriggerId}
      .triggerParams=${a.automation.trigger_params}
      .board=${a.board}
      .yaml=${a.yaml}
      ?disabled=${a.disabled}
      @trigger-change=${a.onTriggerChange}
      @trigger-params-change=${a.onTriggerParamsChange}
    ></esphome-automation-trigger-picker>
  `):(0,s.qy)`${function(e,t,i,a){var o;return e&&("component_on"===e.kind||"component_action"===e.kind)?(o=function(e,t,i){switch(e.kind){case"device_on":return i("device.automation_target_device");case"component_on":case"component_action":{let i=t.find(t=>t.id===e.component_id);if(!i)return e.component_id;return`${ee(i)} (${i.component_id})`}case"interval":return i("device.automation_target_interval_n",{index:e.index+1});case"script":return e.id;case"api_action":return e.action_name;case"light_effect":return e.component_id}}(e,t,a),(0,s.qy)`<div class="field">
    <label class="field-label"> ${a("device.automation_target")} </label>
    <input type="text" readonly .value=${o} />
    ${td(o,i,a)}
  </div>`):s.s6}(this.location,y,this._parseSubstitutions(this.yaml),this._localize)}${d=(o={location:this.location,intervalComponent:this._intervalComponent,activeTrigger:q,automation:_,board:this.board,yaml:this.yaml,disabled:z,showAdvanced:this._showAdvanced,onValueChange:this._onTriggerParamsValueChange,onAdvancedToggle:this._onAdvancedToggle}).location,c=o.intervalComponent,h=o.activeTrigger,0===(f=d?.kind==="interval"?c?c.config_entries.filter(e=>"then"!==e.key):[]:h?.config_entries??[]).length?s.s6:(0,s.qy)`
    <esphome-config-entry-form
      .entries=${f}
      .values=${o.automation.trigger_params}
      .board=${o.board}
      .yaml=${o.yaml}
      ?disabled=${o.disabled}
      advanced-section
      ?show-advanced=${o.showAdvanced}
      @value-change=${o.onValueChange}
      @advanced-toggle=${o.onAdvancedToggle}
    ></esphome-config-entry-form>
  `}`}
      ${r={automation:_,catalog:x,conditionCatalog:k,scripts:w,devices:y,board:this.board,yaml:this.yaml,disabled:z,localize:this._localize,onOpenPicker:()=>this._actionList?.openPicker(),onActionsChange:this._onActionsChange},(0,s.qy)`
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
        ${(0,B.Gc)(r.localize("device.automation_actions_description"))}
      </p>
      <esphome-automation-action-list
        no-header
        hide-add
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
      ${this._error?(0,s.qy)`<p class="ae-error" role="alert">${this._error}</p>`:s.s6}
      ${this.location&&this.value&&!this.addMode?(n=this._localize,l=this._onDelete,(0,s.qy)`<div class="ae-actions">
    <button type="button" class="ae-danger" ?disabled=${z} @click=${l}>
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${n("device.delete_automation")}
    </button>
  </div>`):s.s6}
    `}flushPending(){return this._engine.flushPending()}static get _actionStyles(){return null}get _devicesForTest(){return this._available?.devices??[]}get _scriptsForTest(){return this._available?.scripts??[]}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._intervalComponent=null,this._loading=!0,this._error="",this._parseError=new a7(this),this._catalogLoad=new a9(this),this._showAdvanced=!1,this._engine=new aI(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,setError:e=>{this._error=e}}),this._editMode=!1,this._parseSubstitutions=(0,l.A)(e4.Gr),this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onTriggerParamsValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=ed((this.value??el()).trigger_params,t,i);this._engine.withValue({trigger_params:a})},this._onTargetChange=e=>{e.stopPropagation(),this.location=e.detail.target,this._engine.withValue({trigger_id:null,trigger_params:{}})},this._onTriggerChange=e=>{if(e.stopPropagation(),this._engine.withValue({trigger_id:e.detail.triggerId,trigger_params:e.detail.params}),this.location?.kind==="device_on")this.location={...this.location,trigger:e.detail.triggerId};else if(this.location?.kind==="component_on"){var t;let i,a=(i=(t=e.detail.triggerId).indexOf("."))>=0?t.slice(i+1):t;this.location={...this.location,trigger:a}}},this._onTriggerParamsChange=e=>{e.stopPropagation(),this._engine.withValue({trigger_params:e.detail.params})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}function op(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}oh.styles=[v.G,G.z9,aZ],oc([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],oh.prototype,"_localize",void 0),oc([(0,o.Fg)({context:m.Ie})],oh.prototype,"_api",void 0),oc([(0,n.MZ)()],oh.prototype,"configuration",void 0),oc([(0,n.MZ)({attribute:!1})],oh.prototype,"board",void 0),oc([(0,n.MZ)()],oh.prototype,"platform",void 0),oc([(0,n.MZ)({attribute:!1})],oh.prototype,"value",void 0),oc([(0,n.MZ)({attribute:!1})],oh.prototype,"location",void 0),oc([(0,n.MZ)({type:Boolean,attribute:"add-mode"})],oh.prototype,"addMode",void 0),oc([(0,n.MZ)()],oh.prototype,"yaml",void 0),oc([(0,n.P)("esphome-automation-action-list")],oh.prototype,"_actionList",void 0),oc([(0,n.wk)()],oh.prototype,"_available",void 0),oc([(0,n.wk)()],oh.prototype,"_intervalComponent",void 0),oc([(0,n.wk)()],oh.prototype,"_loading",void 0),oc([(0,n.wk)()],oh.prototype,"_error",void 0),oc([(0,n.wk)()],oh.prototype,"_showAdvanced",void 0),oc([(0,n.wk)()],oh.prototype,"_editMode",void 0),oh=oc([(0,n.EM)("esphome-automation-editor")],oh),(0,k.C)({delete:r.mdiDelete,"open-in-new":r.mdiOpenInNew,"script-text-outline":r.mdiScriptTextOutline});class ou extends s.WF{get dirty(){return this._engine.dirty}get inFlightWrite(){return this._engine.inFlightWrite}connectedCallback(){super.connectedCallback(),this._load()}updated(e){if(e.has("configuration")&&this._loadAvailable(),e.has("location")&&!this.addMode){let t=e.get("location");t&&this.location&&t.id!==this.location.id&&(this.value=null)}!this.addMode&&(e.has("location")||e.has("configuration")||e.has("_loading"))&&this.location&&null===this.value&&!this._loading&&this._hydrateFromBackend()}async _load(){if(this._api){this._loading=!0,this._error="";try{this.configuration&&await this._loadAvailable(),this._loadScriptComponent()}catch(e){this._error=(0,W.u)(e)}finally{this._loading=!1}}}async _loadAvailable(){this._error="";let{available:e,error:t}=await this._catalogLoad.load(this._api,this.configuration,this._localize);void 0!==t&&(this._error=t),e&&(this._available=e)}async _loadScriptComponent(){if(!this._api)return;let e=this.platform||void 0,t=this.board?.id,i=(0,eD.CQ)("script",e,t);if(i){this._scriptComponent=i;return}try{let i=await (0,eD.Sn)(this._api,"script",e,t);i&&(this._scriptComponent=i)}catch{}}async _hydrateFromBackend(){if(this._api&&this.configuration&&this.location)try{let e=await this._api.parseDeviceAutomations(this.configuration,this.yaml),t=this._parseError.resolve(e,this.location,"script");t&&(this.location=t.location,this.value=t.tree)}catch(e){this._error=(0,Y.K)(e,this._localize,"device.automation_parse_error")}}reload(){this.addMode||!this.location||this._engine.shouldSkipReload()||this._hydrateFromBackend()}render(){if(this._loading)return(0,s.qy)`<div class="ae-empty">
        <wa-spinner></wa-spinner>
        ${this._localize("device.loading_automation_catalog")}
      </div>`;if(this._parseError.active)return this._parseError.renderPanel(this._localize);let e=this.value??el(),t=this._available?.devices??[],i=this._available?.scripts??[],a=this._available?.actions??[],o=this._available?.conditions??[],r=this._engine.deleting;return(0,s.qy)`
      ${this._renderHeader()} ${this._renderConfigForm(e,r)}
      ${this._showAdvanced?this._renderParametersField(e,r):s.s6}
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
          ${(0,B.Gc)(this._localize("device.script_actions_description"))}
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
      ${this._error?(0,s.qy)`<p class="ae-error" role="alert">${this._error}</p>`:s.s6}
      ${this.location&&this.value&&!this.addMode?(0,s.qy)`<div class="ae-actions">
              <button
                type="button"
                class="ae-danger"
                ?disabled=${r}
                @click=${this._onDelete}
              >
                <wa-icon library="mdi" name="delete"></wa-icon>
                ${this._localize("device.delete_script")}
              </button>
            </div>`:s.s6}
    `}_renderHeader(){let e=this._scriptComponent,t=e?.name??this._localize("device.script_header_title_static"),i=e?.description??this._localize("device.script_header_description"),a=e?.docs_url??`${aT.Ik}/components/script.html`,o=e?.image_url??"";return(0,s.qy)`<div class="ae-header">
      <div class="ae-header-text">
        <h2 class="ae-header-title">${t}</h2>
        <a class="ae-header-docs" href=${a} target="_blank" rel="noreferrer">
          ${this._localize("device.docs")}
          <wa-icon library="mdi" name="open-in-new"></wa-icon>
        </a>
        <p class="ae-header-desc">${(0,B.Gc)(i)}</p>
      </div>
      <div class="ae-header-icon">
        ${o?(0,s.qy)`<img alt="" src=${o} />`:(0,s.qy)`<wa-icon library="mdi" name="script-text-outline"></wa-icon>`}
      </div>
    </div>`}_renderConfigForm(e,t){let i=this._scriptComponent;if(!i)return s.s6;let a=i.config_entries.filter(e=>"parameters"!==e.key&&"then"!==e.key),o=this._hasParametersEntry();return 0!==a.length||o?(0,s.qy)`
      <esphome-config-entry-form
        .entries=${a}
        .values=${e.trigger_params}
        .board=${this.board}
        .yaml=${this.yaml}
        ?disabled=${t}
        advanced-section
        ?force-advanced-control=${o}
        .advancedExtraCount=${+!!o}
        ?show-advanced=${this._showAdvanced}
        @value-change=${this._onConfigFormValueChange}
        @advanced-toggle=${this._onAdvancedToggle}
      ></esphome-config-entry-form>
    `:s.s6}_hasParametersEntry(){return this._scriptComponent?.config_entries.some(e=>"parameters"===e.key)??!1}_renderParametersField(e,t){let i=e.trigger_params.parameters??{};return(0,s.qy)`<esphome-callable-params-editor
      .value=${i}
      ?disabled=${t}
      .fieldLabel=${this._localize("device.automation_script_parameters")}
      .description=${this._localize("device.script_parameters_description")}
      .addLabel=${this._localize("device.script_add_parameter")}
      .namePlaceholder=${this._localize("device.script_parameter_name_placeholder")}
      @value-change=${this._onParametersChange}
    ></esphome-callable-params-editor>`}flushPending(){return this._engine.flushPending()}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.board=null,this.platform="",this.value=null,this.location=null,this.addMode=!1,this.yaml="",this._available=null,this._loading=!0,this._error="",this._parseError=new a7(this),this._scriptComponent=null,this._showAdvanced=!1,this._engine=new aI(this,{getApi:()=>this._api,getLocalize:()=>this._localize,isReadOnly:()=>this._parseError.active,canApply:e=>"script"===e.kind&&!!e.id,setError:e=>{this._error=e}}),this._catalogLoad=new a9(this),this._onAdvancedToggle=e=>{this._showAdvanced=e.detail.show},this._onConfigFormValueChange=e=>{e.stopPropagation();let{path:t,value:i}=e.detail,a=this.value??el(),o=1===t.length&&"id"===t[0]?(0,aD.e)(String(i??"")):i,r=ed(a.trigger_params,t,o);if(1===t.length&&"id"===t[0]){let e=String(o??"");e&&(this.location={kind:"script",id:e})}this._engine.withValue({trigger_params:r})},this._onParametersChange=e=>{e.stopPropagation();let t=this.value??el();this._engine.withValue({trigger_params:{...t.trigger_params,parameters:e.detail.value}})},this._onActionsChange=e=>{e.stopPropagation(),this._engine.withValue({actions:e.detail.actions})},this._onDelete=()=>{this._engine.delete()}}}ou.styles=[v.G,G.z9,aZ],op([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ou.prototype,"_localize",void 0),op([(0,o.Fg)({context:m.Ie})],ou.prototype,"_api",void 0),op([(0,n.MZ)()],ou.prototype,"configuration",void 0),op([(0,n.MZ)({attribute:!1})],ou.prototype,"board",void 0),op([(0,n.MZ)()],ou.prototype,"platform",void 0),op([(0,n.MZ)({attribute:!1})],ou.prototype,"value",void 0),op([(0,n.MZ)({attribute:!1})],ou.prototype,"location",void 0),op([(0,n.MZ)({type:Boolean,attribute:"add-mode"})],ou.prototype,"addMode",void 0),op([(0,n.MZ)()],ou.prototype,"yaml",void 0),op([(0,n.P)("esphome-automation-action-list")],ou.prototype,"_actionList",void 0),op([(0,n.wk)()],ou.prototype,"_available",void 0),op([(0,n.wk)()],ou.prototype,"_loading",void 0),op([(0,n.wk)()],ou.prototype,"_error",void 0),op([(0,n.wk)()],ou.prototype,"_scriptComponent",void 0),op([(0,n.wk)()],ou.prototype,"_showAdvanced",void 0),ou=op([(0,n.EM)("esphome-script-editor")],ou);let om=(0,s.AH)`
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
`;function ov(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}class og extends s.WF{open(){this._dialog.open=!0}close(){this._dialog.open=!1}render(){return(0,s.qy)`
      <esphome-base-dialog
        ?open=${this._dialog.open}
        .label=${this._localize("device.change_board_title")}
        @request-close=${this._dialog.onRequestClose}
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
    `}_renderBoard(e){return(0,s.qy)`
      <button type="button" class="board-row" @click=${()=>this._select(e)}>
        <img
          class="board-thumb"
          src=${(0,j.Ru)(e)}
          alt=${e.name}
          referrerpolicy="no-referrer"
          @error=${j.jt}
        />
        <div class="board-meta">
          <span class="board-name">${e.name}</span>
          ${e.manufacturer?(0,s.qy)`<span class="board-mfr">${e.manufacturer}</span>`:s.s6}
        </div>
        ${e.is_generic?(0,s.qy)`<wa-badge variant="neutral" pill
                >${this._localize("device.change_board_generic_tag")}</wa-badge
              >`:s.s6}
      </button>
    `}_select(e){this.close(),this.dispatchEvent(new CustomEvent("select-board",{detail:{boardId:e.id},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.currentBoard=null,this.boards=[],this._dialog=new H.T(this)}}og.styles=[v.G,ek.dC,ek.rG,tS.E,tS.V,om],ov([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],og.prototype,"_localize",void 0),ov([(0,n.MZ)({attribute:!1})],og.prototype,"currentBoard",void 0),ov([(0,n.MZ)({attribute:!1})],og.prototype,"boards",void 0),og=ov([(0,n.EM)("esphome-change-board-dialog")],og);var of=i(6049);class o_{hostConnected(){this._unsubscribe=iT(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}ensure(){let{api:e,platform:t,boardId:i}=this._context();e&&void 0===iM(t,i)&&iA.triggers.fetch(e,t,i).catch(()=>{})}resolveName(e,t,i){let{platform:a,boardId:o}=this._context(),r=iM(a,o);if(!r)return i;let s="esphome"===e?t:`${e}.${t}`;return r.find(e=>e.id===s)?.name||i}hasTriggersFor(e){let{platform:t,boardId:i}=this._context(),a=iM(t,i);return!a||a.some(t=>t.applies_to.some(t=>e.includes(t)))}constructor(e,t){this._host=e,this._context=t,e.addController(this)}}let ob=new Set(["external_components","packages"]);function oy(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({close:r.mdiClose});class ow extends s.WF{open(){this._name="",this._error="",this._dialog.open=!0}render(){let e=this.boardName?this._localize("device.add_api_action_dialog_title",{name:this.boardName}):this._localize("device.add_api_action");return(0,s.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,B.Gc)(this._localize("device.api_action_header_description"))}
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
          @input=${e=>{this._name=(0,aD.e)(e.target.value),this._error=""}}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._name&&!(0,C.vB)(this.yaml).some(e=>e.key===`automation:api_action:${this._name}`)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new H.T(this),this._name="",this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"api_action",action_name:this._name},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{},actions:[]},e,this.yaml),i=ev(this.yaml,t);this.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:i},bubbles:!0,composed:!0})),this.dispatchEvent(new CustomEvent("automation-added",{detail:{sectionKey:em(e)},bubbles:!0,composed:!0})),this._dialog.open=!1}catch(t){let e=(0,Y.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}ow.styles=[v.G,G.z9,V,(0,s.AH)`
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
    `],oy([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ow.prototype,"_localize",void 0),oy([(0,o.Fg)({context:m.Ie})],ow.prototype,"_api",void 0),oy([(0,n.MZ)()],ow.prototype,"boardName",void 0),oy([(0,n.MZ)()],ow.prototype,"configuration",void 0),oy([(0,n.MZ)()],ow.prototype,"yaml",void 0),oy([(0,n.MZ)({attribute:!1})],ow.prototype,"board",void 0),oy([(0,n.wk)()],ow.prototype,"_name",void 0),oy([(0,n.wk)()],ow.prototype,"_saving",void 0),oy([(0,n.wk)()],ow.prototype,"_error",void 0),ow=oy([(0,n.EM)("esphome-add-api-action-dialog")],ow);let o$=(0,s.AH)`
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
`;function ox(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({plus:r.mdiPlus,pencil:r.mdiPencil,delete:r.mdiDelete});class ok extends s.WF{render(){if(0===this.rows.length&&void 0===this.addLabel)return s.s6;let e=""!==this.busyKey;return(0,s.qy)`<div class="list">
      <div class="header">
        <h4 class="title">${this.heading}</h4>
        ${void 0!==this.addLabel?(0,s.qy)`<button type="button" class="add" @click=${this._onAdd}>
                <wa-icon library="mdi" name="plus"></wa-icon>
                ${this.addLabel}
              </button>`:s.s6}
      </div>
      ${0===this.rows.length?void 0!==this.emptyText?(0,s.qy)`<p class="empty" role="status">${this.emptyText}</p>`:s.s6:(0,s.qy)`<ul class="rows">
              ${this.rows.map(t=>(0,s.qy)`<li class="row">
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
    </div>`}_emit(e,t){this.dispatchEvent(new CustomEvent(e,{detail:{key:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this.heading="",this.rows=[],this.busyKey="",this.editLabel="",this.deleteLabel="",this._onAdd=()=>{this.dispatchEvent(new CustomEvent("add",{bubbles:!0,composed:!0}))}}}ok.styles=[v.G,o$],ox([(0,n.MZ)()],ok.prototype,"heading",void 0),ox([(0,n.MZ)({attribute:!1})],ok.prototype,"rows",void 0),ox([(0,n.MZ)({attribute:"add-label"})],ok.prototype,"addLabel",void 0),ox([(0,n.MZ)({attribute:"empty-text"})],ok.prototype,"emptyText",void 0),ox([(0,n.MZ)({attribute:"busy-key"})],ok.prototype,"busyKey",void 0),ox([(0,n.MZ)({attribute:"edit-label"})],ok.prototype,"editLabel",void 0),ox([(0,n.MZ)({attribute:"delete-label"})],ok.prototype,"deleteLabel",void 0),ok=ox([(0,n.EM)("esphome-section-automation-list")],ok);let oz=(0,s.AH)`
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
`;i(3983);var oC=i(9789);let oq=e=>"!lambda"===e.tag&&"|-"===e.marker,oE=e=>({_lambda:new eS.ho(e).body.replace(/\n+$/,""),_tag:"!lambda"}),oS=(e,t,i)=>oq(e)?oE(i):new eS.ho(i,t);var oA=i(9808);let oM=(e,t)=>{if(e.includes(".")||(0,oC.CI)(t))return null;if(""===t)return{key:e,value:null};let{value:i}=(0,oA.bw)(t);return i.startsWith("[")&&i.endsWith("]")?{key:e,value:(0,oA.Wg)(i)}:{key:e,value:(0,oA.Qj)(t)}},oP=(e,t)=>{let i=e.match(t);return i?oM(i[1],i[2].trim()):null},oL=(e,t,i)=>{let a=-1,o=t-1;for(let r=t;r<e.length;r++){if(""===e[r].trim())continue;let t=(0,oC.MG)(e[r]).length;if(-1===a){if(t<=i)break;a=t}else if(t<a)break;o=r}return o+1},oF=(e,t,i)=>{let{dashIndent:a,firstDashIdx:o}=((e,t,i)=>{let a=t;for(;a<e.length&&(0,oC.BJ)(e[a]);)a++;return a>=e.length?{dashIndent:i,firstDashIdx:a}:{dashIndent:e[a].match(/^( *)-/)?.[1]??i,firstDashIdx:a}})(e,t,`${i}  `),r=(e[o]??"").match(oC.o1),s=r?" ".repeat(r[1].length):(0,oC.G5)(e,o+1,a)??`${a}  `,{endIdx:n,isComplex:l}=((e,t,i)=>{let a=!1;for(let o=t;o<e.length;o++){let t=e[o];if(!(0,oC.BJ)(t)){if((0,oC.PM)(t,i.length))return{endIdx:o,isComplex:a};!a&&(oC.PL.test(t)||oC.uT.test(t)||oC.Vi.test(t))&&(a=!0)}}return{endIdx:e.length,isComplex:a}})(e,t,i);if(l){let i=oT(e,t,a,s);return i?{value:i.items,endIdx:i.endIdx,isEmptyScalarList:!1}:{value:new eS.ho(e.slice(t,n)),endIdx:n,isEmptyScalarList:!1}}let{items:d,endIdx:c}=((e,t,i,a)=>{let o=[],r=t;for(;r<e.length;r++){if((0,oC.BJ)(e[r]))continue;if(!e[r].startsWith(i))break;let t=e[r].match(a);if(!t)break;o.push((0,oA.Ir)(t[1].trim()))}return{items:o,endIdx:r}})(e,t,`${a}- `,(0,oC.iu)(a));return{value:d,endIdx:c,isEmptyScalarList:0===d.length}},oO=(e,t,i)=>{let a=(0,oC.K7)(e,t+1);if(a>=e.length)return null;let o=(0,oC.MG)(e[a]);return o.length<=i?null:e[a].slice(o.length).startsWith("-")?"bail":oD(e,t+1,o)},oR=(e,t,i,a,o)=>{let r=t;for(;r<e.length;){let t=e[r];if((0,oC.BJ)(t)){r++;continue}if(!t.startsWith(i))break;if(t.startsWith(`${i} `))return null;let s=oP(t,a);if(!s)return null;if(null===s.value){let t=oO(e,r,i.length);if("bail"===t)return null;if(t){o[s.key]=Object.keys(t.values).length>0?t.values:s.value,r=t.endIdx;continue}}o[s.key]=s.value,r++}return r},oT=(e,t,i,a)=>{let o=RegExp(`^${i}-\\s+(${oC.bn}):\\s*(.*)$`),r=RegExp(`^${a}(${oC.bn}):\\s*(.*)$`),s=t=>{let s=Object.create(null),n=null;if(!oC.Vi.test(e[t])){let a=e[t].match(o);if(!a)return null;let r=a[1],l=a[2].trim(),d=(0,oC.CI)(l);if(d){if(!oq(d))return null;let a=oL(e,t+1,`${i}  `.length),o=(0,oC.K7)(e,a);return o<e.length&&(0,oC.MG)(e[o]).length>i.length?null:(s[r]=oE(e.slice(t+1,a)),{item:s,endIdx:a})}let c=oM(r,l);if(!c)return null;s[c.key]=c.value,null===c.value&&(n=c.key)}if(null!==n){let o=e[t].match(oC.o1)?.[1].length??i.length+2,l=oO(e,t,o);if("bail"===l)return null;if(l){Object.keys(l.values).length>0&&(s[n]=l.values);let t=oR(e,l.endIdx,a,r,s);return null===t?null:{item:s,endIdx:t}}}let l=oR(e,t+1,a,r,s);return null===l?null:{item:s,endIdx:l}},n=[],l=t;for(;l<e.length;){if((0,oC.BJ)(e[l])){l++;continue}if(!(0,oC.AL)(e[l],i))break;let t=s(l);if(!t)return null;n.push(t.item),l=t.endIdx}return{items:n,endIdx:l}};function oD(e,t,i){let a=(0,oC.zM)(i),o=Object.create(null),r=t;for(;r<e.length;){let t=e[r];if((0,oC.BJ)(t)){r++;continue}if(!t.startsWith(i))break;let s=t.match(a);if(!s){r++;continue}let n=s[1],l=s[2].trim(),d=(0,oC.CI)(l);if(d){let t=oL(e,r+1,i.length);o[n]=oS(d,l,e.slice(r+1,t)),r=t;continue}if(""===l){let t=(0,oC.K7)(e,r+1);if(t<e.length&&(0,oC.SU)(e[t],i)){let{value:t,endIdx:a}=oF(e,r+1,i);o[n]=t,r=a;continue}if(t<e.length){let a=(0,oC.MG)(e[t]);if(a.length>i.length){let t=oD(e,r+1,a);Object.keys(t.values).length>0&&(o[n]=t.values),r=t.endIdx;continue}}r++;continue}l.startsWith("[")&&l.endsWith("]")?o[n]=(0,oA.Wg)(l):o[n]=(0,oA.Qj)(l),r++}return{values:o,endIdx:r}}function oI(e,t,i){if(void 0!==i)return i-1;for(let i=0;i<e.length;i++)if(e[i].startsWith(`${t}:`))return i;return -1}function oj(e,t,i){let a=Object.create(null),o=new Map,r=new Map,s=(e,t,i)=>{o.set(e,{start:t,end:i,leadStart:t})},n=oI(e,t,i);if(n<0)return{values:a,spans:o,comments:r,childIndent:"",isListItem:!1,startIdx:n};let l=oC.WV.test(e[n]),d=(0,oC.eq)(e,n,l),c=(0,oC.zM)(d),h=t=>{let i=(0,oC.K7)(e,t);if(i>=e.length)return null;let a=(0,oC.MG)(e[i]);return a.length<=d.length?null:oD(e,t,a)};if(!l&&of.sU.has(t)){let i=(0,oC.MG)(e[n]),s=(0,oC.K7)(e,n+1);if(s<e.length&&(0,oC.SU)(e[s],i))return a[t]=oF(e,n+1,i).value,{values:a,spans:o,comments:r,childIndent:d,isListItem:l,startIdx:n}}if(l){let t=e[n].match(oC.L1);if(t){let i=e[n],o=i.slice(i.indexOf(":",i.indexOf("-"))+1),{value:s,comment:l}=(0,oA.bw)(o),d=s.trim();if(""!==d)l&&r.set(t[1],l),a[t[1]]=(0,oA.Qj)(d);else{let e=h(n+1);e&&Object.keys(e.values).length>0&&(a[t[1]]=e.values)}}}let p=l?(e[n].match(/^(\s*)-/)??["",""])[1].length:-1;for(let t=n+1;t<e.length;t++){let i=e[t];if((0,oC.BJ)(i))continue;if(l){let e=i.match(/^(\s*)-(\s|$)/);if(e&&e[1].length===p||oC.QW.test(i))break}else if(oC.QW.test(i))break;let o=i.match(c);if(!o)continue;let n=o[1],u=o[2].trim(),m=(0,oC.CI)(u);if(m){let i=oL(e,t+1,d.length);a[n]=oS(m,u,e.slice(t+1,i)),s(n,t,i),t=i-1;continue}if(""===u){let i=(0,oC.K7)(e,t+1);if(i>=e.length)continue;let o=e[i];if((0,oC.SU)(o,d)){let{value:i,endIdx:o,isEmptyScalarList:r}=oF(e,t+1,d);r||(a[n]=i,s(n,t,o),t=o-1);continue}let r=h(t+1);r&&(Object.keys(r.values).length>0&&(a[n]=r.values,s(n,t,r.endIdx)),t=r.endIdx-1);continue}let{value:v,comment:g}=(0,oA.bw)(u);if(g&&r.set(n,g),v.startsWith("[")&&v.endsWith("]")){a[n]=(0,oA.Wg)(v),s(n,t,t+1);continue}a[n]=(0,oA.Qj)(v),s(n,t,t+1)}for(let t of o.values()){let i=t.start+1,a=t.end,o=!1;for(;a>i&&(0,oC.BJ)(e[a-1])&&(0,oC.MG)(e[a-1]).length<=d.length;)a--,(0,oC.w5)(e[a])&&(o=!0);o&&(t.end=a)}let u=n+1;for(let t of o.values()){let i=t.start;for(;i>u&&(0,oC.BJ)(e[i-1]);)i--;t.leadStart=i,u=t.end}return{values:a,spans:o,comments:r,childIndent:d,isListItem:l,startIdx:n}}function oB(e,t){if(e===t)return!0;if(e instanceof eS.ho||t instanceof eS.ho)return e instanceof eS.ho&&t instanceof eS.ho&&e.inlineHeader===t.inlineHeader&&e.lines.length===t.lines.length&&e.lines.every((e,i)=>e===t.lines[i]);if(Array.isArray(e)||Array.isArray(t))return Array.isArray(e)&&Array.isArray(t)&&e.length===t.length&&e.every((e,i)=>oB(e,t[i]));if((0,en.Qd)(e)&&(0,en.Qd)(t)){let i=Object.keys(e);return i.length===Object.keys(t).length&&i.every(i=>Object.prototype.hasOwnProperty.call(t,i)&&oB(e[i],t[i]))}return!1}function oN(e,t,i){let a=oI(e,t,i);if(a<0)return{start:-1,end:-1};let o=oC.WV.test(e[a]),r=o?(e[a].match(/^(\s*)-/)??["",""])[1].length:-1,s=e.length;for(let t=a+1;t<e.length;t++)if(o){let i=e[t].match(/^(\s*)-(\s|$)/);if(i&&i[1].length===r||oC.QW.test(e[t])){s=t;break}}else if(oC.QW.test(e[t])){s=t;break}return{start:a,end:s}}function oZ(e){if(e._draftTimer=null,!e._config)return;let t=(0,of.a7)(e.sectionKey,e._config.entries);e._fieldErrors=(0,eK.JK)(t,e._values,e._presentComponents,e.board?.esphome.platform??null,e.sectionKey);let i=(0,C.uv)(e.yaml,e.sectionKey,e.fromLine);if(void 0===i)return void e._setDirty(!1);let a=function(e,t,i,a,o={}){let r=e.split("\n"),{start:s,end:n}=oN(r,t,a);if(s<0)return e;let l=oC.WV.test(r[s]),d=(0,oC.eq)(r,s,l),c=function(e,t,i,a){let o=-1;for(let a=t+1;a<i;a++){let t=e[a];if(""===t.trim()||(0,oC.w5)(t))continue;let i=(0,oC.MG)(t).length;i>o&&(o=i)}return o<0?a:o}(r,s,n,d.length),h=n;for(;h>s+1;){let e=r[h-1];if(""===e.trim()){h--;continue}let t=(0,oC.MG)(e).length;if((0,oC.w5)(e)&&(t<=d.length||t<c))h--;else break}let p=h;if(of.sU.has(t)){let a=i[t];if(!Array.isArray(a))return e;let n=(0,eS.ym)({[t]:a},(0,oC.MG)(r[s]),{...o,indentStep:o.indentStep??(d||"  ")});return r.splice(s,p-s,...n),r.join("\n")}let u=oj(r,t,a),m=-1;for(let e of u.spans.values())e.end>m&&(m=e.end);m>=0&&(p=m);let v=r[s],g=new Set;if(l){let e=v.match(oC.L1);if(e){let t=e[1];if(Object.prototype.hasOwnProperty.call(i,t))if(function(e){if(null==e)return!1;let t=typeof e;return"string"===t||"number"===t||"boolean"===t}(i[t])){if(g.add(t),!oB(i[t],u.values[t])){let e=v.match(/^(\s*)-(\s+)/),a=`${e[1]}-${e[2]}`,o=u.comments.get(t)??"";v=`${a}${t}: ${(0,eS.Rm)(i[t])}${o}`}}else{let e=(v.match(/^(\s*)-/)??["",""])[1];v=`${e}-`}}}let f=!l&&d?d:"  ",_=[v,...function(e,t,i,a,o,r){let s=[];for(let[n,l]of Object.entries(i)){if(a.has(n))continue;let i=t.spans.get(n);if(i&&oB(l,t.values[n])){s.push(...e.slice(i.leadStart,i.end));continue}i&&s.push(...e.slice(i.leadStart,i.start));let d=(0,eS.ym)({[n]:l},o,r),c=t.comments.get(n);c&&1===d.length&&(d[0]+=c),s.push(...d)}return s}(r,u,i,g,d,{...o,indentStep:o.indentStep??f})];return r.splice(s,p-s,..._),r.join("\n")}(e.yaml,e.sectionKey,e._values,i,{keepEmptyStrings:of.fq.has(e.sectionKey)});e._setDirty(!1),a!==e.yaml&&(e._lastSelfWrittenYaml=a,e.dispatchEvent(new CustomEvent("yaml-draft",{detail:{yaml:a},bubbles:!0,composed:!0})))}async function oK(e){if(!e._config)return;let t=(0,C.uv)(e.yaml,e.sectionKey,e.fromLine);if(void 0===t){e._error=e._localize("device.section_delete_error");return}e._deleting=!0,e._error="";let i=e._config.title;try{let a=function(e,t,i){let a=e.split("\n"),{start:o,end:r}=oN(a,t,i);if(o<0)return e;let s=oC.WV.test(a[o]);if(a.splice(o,r-o),s){let e=o-1;for(;e>=0&&!oC.QW.test(a[e]);)e--;if(e>=0){let t=!1,i=a.length;for(let o=e+1;o<a.length;o++){if(oC.QW.test(a[o])){i=o;break}if(""!==a[o].trim()){t=!0;break}}t||a.splice(e,i-e)}}return a.join("\n")}(e.yaml,e.sectionKey,t);if(a===e.yaml){e._error=e._localize("device.section_delete_error");return}await e._api.updateConfig(e.configuration,a),e._setDirty(!1),e.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:a},bubbles:!0,composed:!0})),e.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:null},bubbles:!0,composed:!0})),(0,d.VX)(e._localize("device.section_deleted",{name:i}))}catch(t){e._error=(0,Y.K)(t,e._localize,"device.section_delete_error")}finally{e._deleting=!1}}async function oU(e){let t=++e._loadId;e._loading=!0,e._error="",e._config=null,e._isUnknown=!1,e._setDirty(!1),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),e._lastSelfWrittenYaml=null;try{var i;let a=e.board?.esphome.platform,o=await (0,eD.Sn)(e._api,e.sectionKey,a);if(t!==e._loadId)return;let r=e.yaml;o?e._config={section_key:e.sectionKey,section_type:"core",title:o.name,description:o.description,docs_url:o.docs_url,icon:"",image_url:o.image_url,entries:o.config_entries,required_groups:o.required_groups??[]}:(e._config={section_key:e.sectionKey,section_type:"core",title:e.sectionKey,description:"",docs_url:"",icon:"",image_url:"",entries:[],required_groups:[]},e._isUnknown=!0);let s=(0,C.uv)(r,e.sectionKey,e.fromLine),n=(i=e.sectionKey,oj(r.split("\n"),i,s).values);e._values=(0,ie.Dq)(n,e._config.entries),e._resolvedFromLine=s,e._presentComponents=(0,eS.Zn)(r)}catch(a){if(t!==e._loadId)return;let i=a instanceof Error?a.message:"";e._error=i.includes("timed out")?e._localize("device.load_config_error"):i||e._localize("device.load_config_error")}finally{t===e._loadId&&(e._loading=!1)}}let oV=new Set(["api","script","interval","external_components","packages","substitutions","globals","dashboard_import"]);function oG(e,t,i){let a=(0,C.MT)(e),o=a.filter(e=>(0,C.gU)(e)===t);return 0===o.length?null:{sections:a,match:void 0!==i?o.find(e=>e.fromLine===i)??o[0]:o[0]}}function oH(e,t){e.dispatchEvent(new CustomEvent("apply-section-values",{detail:{changes:t},bubbles:!0,composed:!0}))}let oW=(0,s.AH)`
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
`;function oY(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({update:r.mdiUpdate});let oQ=/^GPIO(\d+)_(IN|OUT)$/,oJ={ethernet:[{key:"clk_mode",copyPrefix:"ethernet_clk_mode",migrate:e=>{if("string"!=typeof e)return null;let t=oQ.exec(e.trim().toUpperCase().replace(/ /g,"_"));return t?[{path:["clk"],value:{pin:`GPIO${t[1]}`,mode:"IN"===t[2]?"CLK_EXT_IN":"CLK_OUT"}},{path:["clk_mode"],value:void 0}]:null}}]},oX=e=>Object.prototype.hasOwnProperty.call(oJ,e);class o0 extends s.WF{_migratable(){if(!oX(this.sectionKey))return[];let e=[];for(let t of oJ[this.sectionKey]){if(!Object.prototype.hasOwnProperty.call(this.values,t.key))continue;let i=this.entries.find(e=>e.key===t.key);if(i&&!(0,eK.VP)(i,this.values))continue;let a=t.migrate(this.values[t.key]);a&&e.push({option:t,changes:a})}return e}_onMigrate(e){oH(this,e),(0,d.VX)(this._localize("device.deprecation_applied"))}render(){let e=this._migratable();return 0===e.length?s.s6:e.map(({option:e,changes:t})=>(0,s.qy)`
        <div class="notice" role="note">
          <wa-icon library="mdi" name="update"></wa-icon>
          <div class="body">
            <p>${this._localize(`device.${e.copyPrefix}_notice`)}</p>
            <button type="button" class="cta" @click=${()=>this._onMigrate(t)}>
              ${this._localize(`device.${e.copyPrefix}_migrate`)}
            </button>
          </div>
        </div>
      `)}constructor(...e){super(...e),this._localize=e=>e,this.sectionKey="",this.values={},this.entries=[]}}async function o1(e=4){let t=Math.max(1,Math.trunc(e)),{PASSPHRASE_WORDS:a}=await i.e(820).then(i.bind(i,2503)),o=a.length,r=Math.floor(0x100000000/o)*o,s=new Uint32Array(1),n=[];for(;n.length<t;)crypto.getRandomValues(s),s[0]>=r||n.push(a[s[0]%o]);return n.join("-")}o0.styles=[v.G,oW],oY([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],o0.prototype,"_localize",void 0),oY([(0,n.MZ)()],o0.prototype,"sectionKey",void 0),oY([(0,n.MZ)({attribute:!1})],o0.prototype,"values",void 0),oY([(0,n.MZ)({attribute:!1})],o0.prototype,"entries",void 0),o0=oY([(0,n.EM)("esphome-deprecation-notice")],o0);var o2=i(8818);function o6(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({"lock-alert":r.mdiLockAlert});let o3=()=>o1(),o4={api:{secretSection:"api",marker:"encryption",copyPrefix:"api_encryption",fields:[{path:["encryption","key"],generate:e0.My,secretField:"key"}]},"ota.esphome":{secretSection:"ota.esphome",marker:"password",copyPrefix:"ota_password",fields:[{path:["password"],generate:o3,secretField:"password"}]},web_server:{secretSection:"web_server",marker:"auth",copyPrefix:"web_auth",fields:[{path:["auth","username"],generate:()=>o1(1)},{path:["auth","password"],generate:o3,secretField:"password"}]}},o5=e=>Object.prototype.hasOwnProperty.call(o4,e);class o8 extends s.WF{get _setting(){return o5(this.sectionKey)?o4[this.sectionKey]:void 0}willUpdate(e){(e.has("yaml")||e.has("fromLine")||e.has("sectionKey"))&&(this._markerAbsent=!!this._setting&&!this._markerPresent())}_resolvedFields(){let e=this._setting;if(!e)return[];let t=tF(this._devices,this.configuration);return e.fields.map(i=>({field:i,key:i.secretField?(0,e6.WA)(e.secretSection,i.secretField,t,!0)[0]??"":""}))}get _ready(){let e=this._resolvedFields();return e.length>0&&e.every(e=>!e.field.secretField||""!==e.key)}_markerPresent(){let e=this._setting;if(!e)return!1;let t=this.yaml.split("\n"),i=oI(t,this.sectionKey.split(".")[0],this.fromLine);if(i<0)return!1;let a=RegExp(`^${e.marker}\\s*:`),o=null;for(let e=i+1;e<t.length;e++){let i=t[e];if(""===i.trim()||i.trimStart().startsWith("#"))continue;if(oC.QW.test(i))break;let r=(0,o2._j)(i);if(null===o&&(o=r),r<o)break;if(r===o&&a.test(i.trimStart()))return!0}return!1}render(){let e=this._setting;return e&&this._markerAbsent?(0,s.qy)`
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
    `:s.s6}_renderDialogBody(e){let[t,i=""]=this._localize(`device.${e.copyPrefix}_dialog_body`).split("{key}"),a=this._resolvedFields().filter(e=>e.field.secretField).map((e,t)=>(0,s.qy)`${t>0?", ":""}<code>${e.key}</code>`);return(0,s.qy)`${t}${a}${i}`}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.sectionKey="",this.yaml="",this.configuration="",this._markerAbsent=!1,this._generating=!1,this._onCta=()=>{this._ready&&this._dialog?.open()},this._onGenerate=async()=>{let e=this._setting,t=this._resolvedFields();if(!this._generating&&this._api&&e&&this._ready){this._generating=!0;try{let e=[];for(let{field:i,key:a}of t){let t=await i.generate();i.secretField?(await i7(this._api,a,t),e.push({path:i.path,value:`!secret ${a}`})):e.push({path:i.path,value:t})}oH(this,e),(0,d.VX)(this._localize("device.security_applied"))}catch(t){console.error("Security secret generation failed",t),(0,d.UG)(this._localize(`device.${e.copyPrefix}_error`))}finally{this._generating=!1}}}}}function o9(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}o8.styles=[v.G,oW,(0,s.AH)`
      .dialog-body code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
        padding: 1px 5px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
        word-break: break-all;
      }
    `],o6([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],o8.prototype,"_localize",void 0),o6([(0,o.Fg)({context:m.Ie,subscribe:!0}),(0,n.wk)()],o8.prototype,"_api",void 0),o6([(0,o.Fg)({context:m.xJ,subscribe:!0}),(0,n.wk)()],o8.prototype,"_devices",void 0),o6([(0,n.MZ)()],o8.prototype,"sectionKey",void 0),o6([(0,n.MZ)()],o8.prototype,"yaml",void 0),o6([(0,n.MZ)()],o8.prototype,"configuration",void 0),o6([(0,n.MZ)({type:Number})],o8.prototype,"fromLine",void 0),o6([(0,n.wk)()],o8.prototype,"_markerAbsent",void 0),o6([(0,n.wk)()],o8.prototype,"_generating",void 0),o6([(0,n.P)("esphome-confirm-dialog")],o8.prototype,"_dialog",void 0),o8=o6([(0,n.EM)("esphome-security-notice")],o8),(0,k.C)({"alert-circle-outline":r.mdiAlertCircleOutline,delete:r.mdiDelete,"information-outline":r.mdiInformationOutline,"open-in-new":r.mdiOpenInNew,pencil:r.mdiPencil,"plus-circle-outline":r.mdiPlusCircleOutline});let o7=new Set(["esphome"]);class re extends s.WF{get _showAdvanced(){return this._advancedShownSections.has(this.sectionKey)}_setShowAdvanced(e){let t=new Set(this._advancedShownSections);e?t.add(this.sectionKey):t.delete(this.sectionKey),this._advancedShownSections=t}willUpdate(e){e.has("backendErrors")&&this._clearedBackendPaths.size&&(this._clearedBackendPaths=new Set),(e.has("sectionKey")||e.has("configuration")||e.has("fromLine"))&&this.sectionKey&&this.configuration&&oU(this),this._revealAdvancedForFocus(e),this._revealAdvancedForErrors(e)}_revealAdvancedForErrors(e){(e.has("backendErrors")||e.has("_config"))&&this.backendErrors.fields.size&&this._autoRevealAdvanced([...this.backendErrors.fields.keys()].map(e=>e.split(".")))}_revealAdvancedForFocus(e){(e.has("focusFieldPath")||e.has("_config"))&&this.focusFieldPath?.length&&this._autoRevealAdvanced([this.focusFieldPath])}_autoRevealAdvanced(e){if(this._showAdvanced||!this._config||this._autoRevealedSections.has(this.sectionKey))return;let t=(0,of.a7)(this.sectionKey,this._config.entries);e.some(e=>(function(e,t){let i=e,a=!1;for(let e of t){if((0,en.wr)(e))continue;let t=i.find(t=>t.key===e);if(!t)return!1;t.advanced&&(a=!0),i=t.config_entries??[]}return a})(t,e))&&(this._autoRevealedSections.add(this.sectionKey),this._setShowAdvanced(!0))}updated(){this._triggerCatalog.ensure()}connectedCallback(){super.connectedCallback(),this.dispatchEvent(new CustomEvent("section-mount",{detail:{node:this},bubbles:!0,composed:!0}))}disconnectedCallback(){super.disconnectedCallback(),this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null),this.dispatchEvent(new CustomEvent("section-unmount",{detail:{node:this},bubbles:!0,composed:!0}))}flushPending(){null!==this._draftTimer&&(clearTimeout(this._draftTimer),this._draftTimer=null,oZ(this))}reload(){this.sectionKey&&this.configuration&&null===this._draftTimer&&this.yaml!==this._lastSelfWrittenYaml&&oU(this)}get dirty(){return this._dirty}_setDirty(e){this._dirty!==e&&(this._dirty=e,this.dispatchEvent(new CustomEvent("dirty-change",{detail:{dirty:e},bubbles:!0,composed:!0})))}_scheduleDraftFlush(){this._draftTimer&&clearTimeout(this._draftTimer),this._draftTimer=setTimeout(()=>oZ(this),re.DRAFT_DEBOUNCE_MS)}_onShowYamlEditor(){this.dispatchEvent(new CustomEvent("show-yaml-editor",{bubbles:!0,composed:!0}))}render(){var e,t;if(this._loading)return(0,s.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`;if(this._error&&!this._config)return(0,s.qy)`<p class="error">${this._error}</p>`;if(!this._config)return s.s6;let i=this._showAdvanced,a=(0,of.a7)(this.sectionKey,this._config.entries),o=(e=this.sectionKey,t=a.length,ob.has(e)||0===t),r=[...this.yamlPaneVisible?[]:this.backendErrors.sectionMessages,...o?this.backendErrors.fieldMessages:[]],n=!o7.has(this.sectionKey);return(0,s.qy)`
      <div class="section-header">
        <div class="section-header-info">
          <div class="section-header-title-row">
            <h3 class="section-title">
              ${this._isUnknown?this._localize("device.external_component_title"):this._config.title}
            </h3>
            ${this._config.docs_url?(0,s.qy)`<a
                    class="docs-link"
                    href=${this._config.docs_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    ${this._localize("device.docs")}
                    <wa-icon library="mdi" name="open-in-new"></wa-icon>
                  </a>`:s.s6}
          </div>
          ${this._isUnknown?(0,s.qy)`<p class="section-subtitle">${this.sectionKey}</p>`:s.s6}
          ${this._config.description?(0,s.qy)`<p class="section-desc">
                  ${(0,B.Gc)(this._config.description)}
                </p>`:s.s6}
        </div>
        ${this._isUnknown?s.s6:(0,s.qy)`<div class="section-image">
                <img
                  src=${this._config.image_url||(0,j.uG)()}
                  alt=${this._config.title}
                  referrerpolicy="no-referrer"
                  @error=${j.jt}
                />
              </div>`}
      </div>
      ${r.length>0?(0,s.qy)`<div class="danger-banner section-error-banner" role="alert">
              <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
              <div class="danger-banner-text">
                ${r.map(e=>(0,s.qy)`<p>${e}</p>`)}
              </div>
            </div>`:s.s6}
      ${o?(0,s.qy)`<div class="yaml-only-notice" role="note">
                <wa-icon library="mdi" name="information-outline"></wa-icon>
                <div class="yaml-only-notice-body">
                  <p>${this._localize("device.yaml_only_section")}</p>
                  ${this.yamlPaneVisible?s.s6:(0,s.qy)`<button
                          type="button"
                          class="yaml-only-notice-cta"
                          @click=${this._onShowYamlEditor}
                        >
                          ${this._localize("device.show_yaml_editor")}
                        </button>`}
                </div>
              </div>
              ${this._renderApiActionsTable()} ${this._renderTriggersTable()}
              ${this._renderActionFieldsTable()} ${this._renderActionsRow(n)}`:(0,s.qy)`
              ${o5(this.sectionKey)?(0,s.qy)`<esphome-security-notice
                      .sectionKey=${this.sectionKey}
                      .yaml=${this.yaml}
                      .configuration=${this.configuration}
                      .fromLine=${this._resolvedFromLine}
                      @apply-section-values=${this._onApplySectionValues}
                    ></esphome-security-notice>`:s.s6}
              ${oX(this.sectionKey)?(0,s.qy)`<esphome-deprecation-notice
                      .sectionKey=${this.sectionKey}
                      .values=${this._values}
                      .entries=${a}
                      @apply-section-values=${this._onApplySectionValues}
                    ></esphome-deprecation-notice>`:s.s6}
              <esphome-config-entry-form
                .entries=${a}
                .requiredGroups=${this._config.required_groups}
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
                ?show-advanced=${i}
                @value-change=${this._onValueChange}
                @advanced-toggle=${this._onAdvancedToggle}
                @edit-action-field=${this._onEditActionField}
              ></esphome-config-entry-form>
              ${this._error?(0,s.qy)`<p class="error">${this._error}</p>`:s.s6}
              ${this._renderApiActionsTable()} ${this._renderTriggersTable()}
              ${this._renderActionsRow(n)}
            `}
      ${this._renderApiActionDialog()} ${this._renderAddAutomationDialog()}
      ${n?(0,s.qy)`<esphome-confirm-dialog
              heading=${this._localize("device.delete_section")}
              confirm-label=${this._localize("device.delete_section")}
              message=${this._localize("device.confirm_delete_section",{name:this._config.title})}
              destructive
              @confirm=${this._onDeleteConfirmed}
            ></esphome-confirm-dialog>`:s.s6}
    `}_renderDeleteButton(){return(0,s.qy)`<button
      class="delete-button"
      ?disabled=${this._deleting}
      @click=${()=>this._confirmDialog?.open()}
    >
      <wa-icon library="mdi" name="delete"></wa-icon>
      ${this._localize("device.delete_section")}
    </button>`}_renderApiActionsTable(){if("api"!==this.sectionKey)return s.s6;let e=(0,C.vB)(this.yaml).filter(e=>e.key.startsWith("automation:api_action:")).map(e=>({key:e.key,label:e.id??""}));return(0,s.qy)`<esphome-section-automation-list
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
    ></esphome-section-automation-list>`}_renderActionsRow(e){return e?(0,s.qy)`<div class="actions">${this._renderDeleteButton()}</div>`:s.s6}_renderApiActionDialog(){return"api"!==this.sectionKey?s.s6:(0,s.qy)`<esphome-add-api-action-dialog
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .board=${this.board}
      .yaml=${this.yaml}
      @automation-added=${this._onApiActionAdded}
    ></esphome-add-api-action-dialog>`}_shortcutTarget(){return function(e,t,i,a){if(oV.has(t))return null;if("esphome"===t)return{kind:"device_on"};let o=oG(e,t,i);return null!==o&&a([o.match.parentKey??o.match.key,t])?{kind:"component_on",componentId:(0,C.MX)(o.sections,o.match)}:null}(this.yaml,this.sectionKey,this._resolvedFromLine,e=>this._triggerCatalog.hasTriggersFor(e))}_resolveComponentId(){var e;let t;return e=this.yaml,null===(t=oG(e,this.sectionKey,this._resolvedFromLine))?null:(0,C.MX)(t.sections,t.match)}_renderTriggersTable(){var e,t;let i=this._shortcutTarget();if(null===i)return s.s6;let a=(e=(0,C.vB)(this.yaml),t=e=>this._triggerLabel(e),e.filter(e=>!!e.eventKey&&("device_on"===i.kind?"esphome"===e.parentKey:e.id===i.componentId||e.parentComponentId===i.componentId)).map(e=>({key:e.key,label:void 0!==e.parentComponentId?`${e.name??e.id} → ${t(e)}`:t(e)}))),o="device_on"===i.kind?this._localize("device.automations_list_title_device"):this._localize("device.automations_list_title");return(0,s.qy)`<esphome-section-automation-list
      .heading=${o}
      .rows=${a}
      add-label=${this._localize("device.add_automation")}
      empty-text=${this._localize("device.automations_list_empty")}
      edit-label=${this._localize("device.automations_list_edit")}
      delete-label=${this._localize("device.automations_list_delete")}
      busy-key=${this._deletingRow}
      @add=${this._onOpenAddAutomation}
      @edit=${this._onEditRow}
      @delete=${this._onDeleteRow}
    ></esphome-section-automation-list>`}_renderActionFieldsTable(){var e,t;let i=this._resolveComponentId();if(null===i)return s.s6;let a=(e=(0,C.vB)(this.yaml),t=e=>oo(e,this._localize),e.filter(e=>void 0!==e.actionField&&e.id===i).map(e=>({key:e.key,label:t(e.actionField)})));return(0,s.qy)`<esphome-section-automation-list
      .heading=${this._localize("device.action_fields_list_title")}
      .rows=${a}
      edit-label=${this._localize("device.action_fields_list_edit")}
      delete-label=${this._localize("device.action_fields_list_delete")}
      busy-key=${this._deletingRow}
      @edit=${this._onEditRow}
      @delete=${this._onDeleteRow}
    ></esphome-section-automation-list>`}_triggerLabel(e){let t=e.displayLabel||e.eventKey||"";return e.eventKey?this._triggerCatalog.resolveName(e.parentKey??"esphome",e.eventKey,t):t}_renderAddAutomationDialog(){return null===this._shortcutTarget()?s.s6:(0,s.qy)`<esphome-add-automation-dialog
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .board=${this.board}
      .yaml=${this.yaml}
      @automation-added=${this._onAutomationAdded}
    ></esphome-add-automation-dialog>`}constructor(...e){super(...e),this._localize=e=>e,this.configuration="",this.sectionKey="",this.backendErrors=g.eV,this.yaml="",this.yamlPaneVisible=!0,this.board=null,this.boardName="",this._config=null,this._values={},this._loading=!1,this._dirty=!1,this._error="",this._deletingRow="",this._isUnknown=!1,this._fieldErrors=new Map,this._clearedBackendPaths=new Set,this._advancedShownSections=new Set,this._presentComponents=new Set,this._autoRevealedSections=new Set,this._deleting=!1,this._loadId=0,this._draftTimer=null,this._lastSelfWrittenYaml=null,this._triggerCatalog=new o_(this,()=>({api:this._api,platform:this.board?.esphome.platform||void 0,boardId:this.board?.id})),this._mergeErrors=(0,l.A)((e,t,i)=>{if(0===e.size)return i;let a=new Map;for(let[i,o]of e)t.has(i)||a.set(i,o);if(0===a.size)return i;for(let[e,t]of i)a.set(e,t);return a}),this._onAdvancedToggle=e=>{this._setShowAdvanced(e.detail.show)},this._onValueChange=e=>(function(e,t){let{path:i,value:a}=t.detail;e._values=(0,en.Oe)(e._values,i,a),e._setDirty(!0);let o=i.join(".");if(e._fieldErrors.has(o)){let t=new Map(e._fieldErrors);t.delete(o),e._fieldErrors=t}e.backendErrors.fields.has(o)&&!e._clearedBackendPaths.has(o)&&(e._clearedBackendPaths=new Set(e._clearedBackendPaths).add(o)),e._scheduleDraftFlush()})(this,e),this._onDeleteConfirmed=()=>oK(this),this._onApplySectionValues=e=>(function(e,t){for(let{path:i,value:a}of t)e._values=(0,en.Oe)(e._values,i,a);e._setDirty(!0),e._draftTimer&&(clearTimeout(e._draftTimer),e._draftTimer=null),oZ(e)})(this,e.detail.changes),this._onOpenAddApiAction=()=>{this._addApiActionDialog?.open()},this._onApiActionAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditRow=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.key},bubbles:!0,composed:!0}))},this._onDeleteRow=async e=>{e.stopPropagation();let t=e.detail.key,i=eg(t);if(this._api&&i&&!this._deletingRow){this._deletingRow=t;try{let{yaml_diff:e}=await this._api.deleteAutomation(this.configuration,i,this.yaml),t=ev(this.yaml,e);await this._api.updateConfig(this.configuration,t),this.dispatchEvent(new CustomEvent("yaml-updated",{detail:{yaml:t},bubbles:!0,composed:!0}))}catch(t){let e=(0,Y.K)(t,this._localize,"device.automation_save_error");(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._deletingRow=""}}},this._onOpenAddAutomation=()=>{let e=this._shortcutTarget();null!==e&&("device_on"===e.kind?this._addAutomationDialog?.open({kind:"device_on"}):this._addAutomationDialog?.open({kind:"component_on",componentId:e.componentId}))},this._onAutomationAdded=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e.detail.sectionKey},bubbles:!0,composed:!0}))},this._onEditActionField=e=>{e.stopPropagation();let t=this._resolveComponentId();if(null===t)return;let i=em({kind:"component_action",component_id:t,field:e.detail.field});this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:i},bubbles:!0,composed:!0}))}}}function rt(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}re.DRAFT_DEBOUNCE_MS=200,re.styles=[v.G,G.z9,eJ,oz],o9([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],re.prototype,"_localize",void 0),o9([(0,o.Fg)({context:m.Ie})],re.prototype,"_api",void 0),o9([(0,n.MZ)()],re.prototype,"configuration",void 0),o9([(0,n.MZ)()],re.prototype,"sectionKey",void 0),o9([(0,n.MZ)({type:Number})],re.prototype,"fromLine",void 0),o9([(0,n.MZ)({attribute:!1})],re.prototype,"focusFieldPath",void 0),o9([(0,n.MZ)({attribute:!1})],re.prototype,"backendErrors",void 0),o9([(0,n.MZ)()],re.prototype,"yaml",void 0),o9([(0,n.MZ)({attribute:!1})],re.prototype,"yamlPaneVisible",void 0),o9([(0,n.MZ)({attribute:!1})],re.prototype,"board",void 0),o9([(0,n.MZ)()],re.prototype,"boardName",void 0),o9([(0,n.wk)()],re.prototype,"_config",void 0),o9([(0,n.wk)()],re.prototype,"_values",void 0),o9([(0,n.wk)()],re.prototype,"_loading",void 0),o9([(0,n.wk)()],re.prototype,"_dirty",void 0),o9([(0,n.wk)()],re.prototype,"_error",void 0),o9([(0,n.wk)()],re.prototype,"_deletingRow",void 0),o9([(0,n.wk)()],re.prototype,"_isUnknown",void 0),o9([(0,n.wk)()],re.prototype,"_fieldErrors",void 0),o9([(0,n.wk)()],re.prototype,"_clearedBackendPaths",void 0),o9([(0,n.wk)()],re.prototype,"_advancedShownSections",void 0),o9([(0,n.wk)()],re.prototype,"_presentComponents",void 0),o9([(0,n.wk)()],re.prototype,"_resolvedFromLine",void 0),o9([(0,n.P)("esphome-confirm-dialog")],re.prototype,"_confirmDialog",void 0),o9([(0,n.P)("esphome-add-api-action-dialog")],re.prototype,"_addApiActionDialog",void 0),o9([(0,n.P)("esphome-add-automation-dialog")],re.prototype,"_addAutomationDialog",void 0),o9([(0,n.wk)()],re.prototype,"_deleting",void 0),re=o9([(0,n.EM)("esphome-device-section-config")],re),(0,k.C)({"open-in-new":r.mdiOpenInNew,"arrow-left":r.mdiArrowLeft,close:r.mdiClose,"party-popper":r.mdiPartyPopper,"plus-circle-outline":r.mdiPlusCircleOutline});class ri extends s.WF{willUpdate(e){e.has("board")&&this._refreshAlternateBoards()}updated(e){if(e.has("yaml")&&this.selectedSection){var t,i;let a=()=>{this._sectionConfig?.reload(),this._automationEditor?.reload(),this._scriptEditor?.reload(),this._apiActionEditor?.reload()};(this._reloadTimer&&(clearTimeout(this._reloadTimer),this._reloadTimer=null),t=e.get("yaml"),i=this.yaml,t||!i)?this._reloadTimer=setTimeout(a,1e3):a()}}connectedCallback(){super.connectedCallback(),this.addEventListener("request-add-component",this._onRequestAddComponent)}disconnectedCallback(){super.disconnectedCallback(),this._reloadTimer&&clearTimeout(this._reloadTimer),this.removeEventListener("request-add-component",this._onRequestAddComponent)}async _refreshAlternateBoards(){let e=this.board;if(!e){this._alternatesForBoardId=null,this._alternateBoards=[];return}if(e.id!==this._alternatesForBoardId){this._alternatesForBoardId=e.id,this._alternateBoards=[];try{let t=await this._api.getCompatibleBoards(e.id);if(this._alternatesForBoardId!==e.id)return;this._alternateBoards=t.filter(t=>t.id!==e.id)}catch(t){console.error("Failed to load compatible boards:",t),this._alternatesForBoardId===e.id&&(this._alternatesForBoardId=null,this._alternateBoards=[])}}}render(){let e=this.board;return(0,s.qy)`
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
                  <p class="board-description">${(0,B.Gc)(e.description)}</p>
                </div>
                <div class="board-image">
                  <img
                    src=${(0,j.Ru)(e)}
                    alt=${e.name}
                    referrerpolicy="no-referrer"
                    @error=${j.jt}
                  />
                </div>
              </div>
              <div class="board-separator"></div>
            `:s.s6}
      ${this.selectedSection?this._renderSelectedSection():(0,s.qy)`
              ${this.justCreated?this._renderWelcomeBanner():s.s6}
              ${this._renderStepSection({title:this._localize("device.step_core"),desc:this._localize("device.step_core_desc"),icon:Z,action:this._localize("device.show_core_configuration"),section:"core"})}
              ${this._renderStepSection({title:this._localize("device.step_components"),desc:this._localize("device.step_components_desc"),icon:K,action:this._localize("device.show_components"),section:"components"})}
              ${this._renderStepSection({title:this._localize("device.step_automations"),desc:this._localize("device.step_automations_desc"),icon:U,action:this._localize("device.show_automations"),section:"automations"})}
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
    `}_renderSelectedSection(){let e=this.selectedSection,t=e.startsWith("automation:")?eg(e):null;return t?.kind==="script"?(0,s.qy)`<esphome-script-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
      ></esphome-script-editor>`:t?.kind==="api_action"?(0,s.qy)`<esphome-api-action-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
      ></esphome-api-action-editor>`:t?(0,s.qy)`<esphome-automation-editor
        .configuration=${this.configuration}
        .board=${this.board}
        .platform=${this.board?.esphome.platform??""}
        .location=${t}
        .yaml=${this.yaml}
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
    `}_onShowNavSection(e){this.dispatchEvent(new CustomEvent("nav-section-show",{detail:{section:e},bubbles:!0,composed:!0}))}_renderWelcomeBanner(){return this.board?(0,s.qy)`
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
    `:s.s6}_onDismissWelcome(){this.dispatchEvent(new CustomEvent("just-created-dismiss",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.board=null,this._alternateBoards=[],this._alternatesForBoardId=null,this.yaml="",this.configuration="",this.justCreated=!1,this.yamlPaneVisible=!0,this.selectedSection=null,this.backendErrors=g.eV,this._reloadTimer=null,this._onRequestAddComponent=e=>{let t=e.detail;t?.domain&&(e.stopPropagation(),this._addComponentDialog?.openWithSearch(t.domain))},this._openChangeBoard=()=>{this._changeBoardDialog?.open()},this._onSelectBoard=e=>{e.stopPropagation(),this.dispatchEvent(new CustomEvent("change-board",{detail:e.detail,bubbles:!0,composed:!0}))}}}function ra(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ri.styles=[v.G,N],rt([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ri.prototype,"_localize",void 0),rt([(0,o.Fg)({context:m.Ie})],ri.prototype,"_api",void 0),rt([(0,n.MZ)({attribute:!1})],ri.prototype,"board",void 0),rt([(0,n.wk)()],ri.prototype,"_alternateBoards",void 0),rt([(0,n.MZ)()],ri.prototype,"yaml",void 0),rt([(0,n.MZ)()],ri.prototype,"configuration",void 0),rt([(0,n.MZ)({type:Boolean})],ri.prototype,"justCreated",void 0),rt([(0,n.MZ)({attribute:!1})],ri.prototype,"yamlPaneVisible",void 0),rt([(0,n.MZ)({attribute:!1})],ri.prototype,"selectedSection",void 0),rt([(0,n.MZ)({type:Number})],ri.prototype,"selectedFromLine",void 0),rt([(0,n.MZ)({attribute:!1})],ri.prototype,"focusFieldPath",void 0),rt([(0,n.MZ)({attribute:!1})],ri.prototype,"backendErrors",void 0),rt([(0,n.P)("esphome-device-section-config")],ri.prototype,"_sectionConfig",void 0),rt([(0,n.P)("esphome-automation-editor")],ri.prototype,"_automationEditor",void 0),rt([(0,n.P)("esphome-script-editor")],ri.prototype,"_scriptEditor",void 0),rt([(0,n.P)("esphome-api-action-editor")],ri.prototype,"_apiActionEditor",void 0),rt([(0,n.P)("esphome-add-component-dialog")],ri.prototype,"_addComponentDialog",void 0),rt([(0,n.P)("esphome-add-automation-dialog")],ri.prototype,"_addAutomationDialog",void 0),rt([(0,n.P)("esphome-add-config-dialog")],ri.prototype,"_addConfigDialog",void 0),rt([(0,n.P)("esphome-change-board-dialog")],ri.prototype,"_changeBoardDialog",void 0),ri=rt([(0,n.EM)("esphome-device-board-info")],ri),(0,k.C)({"alert-circle-outline":r.mdiAlertCircleOutline});class ro extends s.WF{willUpdate(e){(e.has("errors")||e.has("caretLine")||e.has("editorFocused")||e.has("completionOpen"))&&this._evaluate()}disconnectedCallback(){super.disconnectedCallback(),this._cancelRevealTimer()}render(){return 0===this._visible.length?s.s6:(0,s.qy)`<div class="danger-banner invalid-banner" role="alert">
      <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
      <div class="danger-banner-text">
        ${this._visible.slice(0,6).map(e=>(0,s.qy)`<span
              >${(0,B.zA)(e.message)}${e.fix?(0,s.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto"
                        title=${this._localize("yaml_editor.error_auto_fix_hint")}
                        @click=${()=>this._onAutoFix(e.fix)}
                      >
                        ${this._localize("yaml_editor.error_auto_fix")}
                      </button>
                    `:s.s6}${e.line?(0,s.qy)`
                      <button
                        type="button"
                        class="invalid-banner-goto"
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
    </div>`}_onAutoFix(e){this.dispatchEvent(new CustomEvent("banner-auto-fix",{detail:{fix:e},bubbles:!0,composed:!0}))}_onGotoLine(e){this.dispatchEvent(new CustomEvent("banner-goto-line",{detail:{line:e},bubbles:!0,composed:!0}))}_evaluate(){if(0===this.errors.length){this._cancelRevealTimer(),this._visible.length&&(this._visible=[]);return}if(this._visible.length>0||this._shouldReveal()){this._cancelRevealTimer(),this._visible=this.errors;return}this.completionOpen?this._cancelRevealTimer():this._armRevealTimer()}_shouldReveal(){return!this.completionOpen&&(!!(!this.editorFocused||this.errors.some(e=>"parse"!==e.kind&&void 0===e.line)||this.errors.some(e=>void 0!==e.line&&Math.abs(e.line-this.caretLine)>3))||performance.now()-this.getLastEditAt()>=15e3)}_armRevealTimer(){this._cancelRevealTimer();let e=15e3-(performance.now()-this.getLastEditAt());this._revealTimer=setTimeout(()=>{this._revealTimer=void 0,this._evaluate()},Math.max(e,100))}_cancelRevealTimer(){void 0!==this._revealTimer&&(clearTimeout(this._revealTimer),this._revealTimer=void 0)}constructor(...e){super(...e),this._localize=e=>e,this.errors=[],this.caretLine=0,this.editorFocused=!1,this.completionOpen=!1,this.getLastEditAt=()=>-1/0,this._visible=[]}}function rr(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}ro.styles=[eJ,(0,s.AH)`
      :host {
        display: contents;
      }

      .invalid-banner {
        flex: 0 0 auto;
      }

      .invalid-banner-goto {
        appearance: none;
        margin-left: 0.35em;
        padding: 0;
        border: none;
        background: none;
        color: inherit;
        font: inherit;
        font-weight: var(--wa-font-weight-semibold);
        text-decoration: underline;
        cursor: pointer;
        white-space: nowrap;
      }

      .invalid-banner-goto:hover {
        text-decoration: none;
      }

      .invalid-banner-more {
        font-size: var(--wa-font-size-2xs);
        opacity: 0.85;
      }
    `],ra([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],ro.prototype,"_localize",void 0),ra([(0,n.MZ)({attribute:!1})],ro.prototype,"errors",void 0),ra([(0,n.MZ)({type:Number})],ro.prototype,"caretLine",void 0),ra([(0,n.MZ)({type:Boolean})],ro.prototype,"editorFocused",void 0),ra([(0,n.MZ)({type:Boolean})],ro.prototype,"completionOpen",void 0),ra([(0,n.MZ)({attribute:!1})],ro.prototype,"getLastEditAt",void 0),ra([(0,n.wk)()],ro.prototype,"_visible",void 0),ro=ra([(0,n.EM)("esphome-editor-invalid-banner")],ro),(0,k.C)({"check-circle-outline":r.mdiCheckCircleOutline,"chevron-down":r.mdiChevronDown,"content-save":r.mdiContentSave,eye:r.mdiEye,"eye-off":r.mdiEyeOff,"dock-left":r.mdiDockLeft,"dock-right":r.mdiDockRight,"view-split-vertical":r.mdiViewSplitVertical,upload:r.mdiUpload,"file-compare":r.mdiFileCompare});class rs extends s.WF{connectedCallback(){super.connectedCallback(),this._isMobile=this._mql.matches,this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),this._mql.removeEventListener("change",this._onMqlChange)}render(){var e;let t,i,a=this._isMobile&&"both"===this.layout?"right":this.layout,o=!this._isMobile&&this.navCollapsed&&"right"===a,r=this._localize("device.editor_title_ready",{name:this.deviceTitle});return(0,s.qy)`
      <section class="card">
        <header class="card-header ${o?"card-header--compact":""}">
          <slot name="header-start"></slot>
          <div class="editor-header-main">
            <div class="editor-header-titlerow">
              <h2 class="editor-header-title">${r}</h2>
              ${this.configuration&&!o?(0,s.qy)`<span class="editor-header-file">${this.configuration}</span>`:s.s6}
            </div>
          </div>
          ${e={localize:this._localize,effectiveLayout:a,revealSensitive:this._revealSensitive,showDiffButton:this._showDiffButton,showDiff:this._showDiff,yaml:this.yaml,savedYaml:this.savedYaml,onToggleRevealSensitive:()=>this._toggleRevealSensitive(),onToggleDiff:()=>this._toggleDiff(),onSetLayout:e=>this._setLayout(e)},(0,s.qy)`<div class="header-actions">
    ${"left"!==e.effectiveLayout?(t=e.localize(e.revealSensitive?"device.yaml_mask_sensitive":"device.yaml_reveal_sensitive"),(0,s.qy)`<button
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
            </button>`):s.s6}
    ${e.showDiffButton?(i=e.showDiff?e.localize("device.diff_view_editor"):e.localize("device.diff_view_diff"),(0,s.qy)`<button
              type="button"
              class="ghost-icon-btn diff-toggle"
              aria-pressed=${e.showDiff}
              ?disabled=${e.yaml===e.savedYaml&&!e.showDiff}
              aria-label=${i}
              @click=${e.onToggleDiff}
              title=${i}
            >
              <wa-icon library="mdi" name="file-compare"></wa-icon>
            </button>`):s.s6}
    <div
      class="layout-toggle"
      role="group"
      aria-label=${e.localize("device.editor_layout_label")}
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
            ${this._renderPrimaryAction()}
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
            class="editor-layout ${"both"===a?"editor-layout--both":"left"===a?"editor-layout--left":"editor-layout--right"} ${this._dragging?"dragging":""}"
            style=${"both"===a?`grid-template-columns: ${this._splitRatio}fr var(--pane-divider-width) ${1-this._splitRatio}fr`:""}
          >
            <div class="editor-pane editor-pane--left">
              <esphome-device-board-info
                .board=${this.board}
                .yaml=${this.yaml}
                .configuration=${this.configuration}
                .selectedSection=${this.selectedSection}
                .selectedFromLine=${this.selectedFromLine}
                .focusFieldPath=${this.focusFieldPath}
                .backendErrors=${this.backendErrors}
                .justCreated=${this.justCreated}
                .yamlPaneVisible=${"left"!==a}
                @show-yaml-editor=${this._onShowYamlEditor}
              ></esphome-device-board-info>
            </div>
            ${"both"===a?(0,s.qy)`<div
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
                  ></div>`:s.s6}
            <div class="editor-pane editor-pane--right">
              <div class="editor-pane-body">
                ${this._showDiff?(0,s.qy)`<esphome-yaml-diff
                        .oldValue=${this.savedYaml}
                        .newValue=${this.yaml}
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
    `}_onSave(){this.dispatchEvent(new CustomEvent("save-yaml",{bubbles:!0,composed:!0}))}_onValidate(){this.dispatchEvent(new CustomEvent("validate-device",{bubbles:!0,composed:!0}))}_toggleDiff(){this._showDiff=!this._showDiff}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_renderPrimaryAction(){var e;return(e={localize:this._localize,showUpdate:this.showUpdate,showModified:this.showModified,busy:this.busy,installedVersion:this.installedVersion,availableVersion:this.availableVersion,onUpdate:()=>this._onUpdate(),onInstall:()=>this._onInstall()}).showUpdate?(0,s.qy)`<div class="install-split">
      <button
        type="button"
        class="install-fab install-split__main"
        ?disabled=${e.busy}
        @click=${e.onUpdate}
        title=${(0,R.a)(e.localize,e.installedVersion,e.availableVersion,"dashboard.update")}
      >
        <wa-icon library="mdi" name="upload"></wa-icon>
        ${e.localize("dashboard.update")}
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
    </div>`:(0,s.qy)`<button
    type="button"
    class="install-fab ${e.showModified?"":"install-fab--muted"}"
    ?disabled=${e.busy}
    @click=${e.onInstall}
    title=${e.localize("dashboard.install")}
  >
    <wa-icon library="mdi" name="upload"></wa-icon>
    ${e.localize("dashboard.install")}
  </button>`}_onInstall(){this.dispatchEvent(new CustomEvent("install-device",{bubbles:!0,composed:!0}))}_onUpdate(){this.dispatchEvent(new CustomEvent("update-device",{bubbles:!0,composed:!0}))}willUpdate(e){if(e.has("configuration")&&(this._liveErrors.length&&(this._liveErrors=[]),this._caretLine=0,this._lastEditAt=-1/0,this._editorFocused=!1,this._completionOpen=!1),this._showDiff&&e.has("_showDiffButton")&&!this._showDiffButton){this._showDiff=!1;return}this._showDiff&&e.has("savedYaml")&&this.yaml===this.savedYaml&&(this._showDiff=!1)}_onYamlDiagnostics(e){if(e.detail.configuration!==this.configuration)return;let t=e.detail.errors;t.length===this._liveErrors.length&&t.every((e,t)=>{let i=this._liveErrors[t];return e.message===i.message&&e.line===i.line&&e.kind===i.kind&&e.fix?.line===i.fix?.line&&e.fix?.indent===i.fix?.indent&&e.fix?.key===i.fix?.key})||(this._liveErrors=t)}_onYamlCursorLine(e){this._caretLine=e.detail.line}_onYamlCompletionOpen(e){this._completionOpen=e.detail.open}_onBannerAutoFix(e){this._autoFix(e.detail.fix)}_onBannerGotoLine(e){this._gotoErrorLine(e.detail.line)}_autoFix(e){let t=this._yamlEditor;if(!t){console.error("[auto-fix] no editor ref"),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed"));return}t.applyIndentFix(e,()=>this._confirmAutoFix()).then(e=>{"stale"===e?(0,d.KQ)(this._localize("yaml_editor.auto_fix_stale")):"unavailable"===e&&(console.error("[auto-fix] editor unavailable"),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed")))}).catch(e=>{console.error("[auto-fix] could not run:",e),(0,d.UG)(this._localize("yaml_editor.auto_fix_failed"))})}async _confirmAutoFix(){if(this._autoFixConfirmOpen)return!1;this._autoFixConfirmOpen=!0,await this.updateComplete;let e=this._autoFixConfirmDialog;if(!e)throw this._autoFixConfirmOpen=!1,Error("auto-fix confirm dialog failed to mount");try{return await new Promise(t=>{let i=i=>{e.removeEventListener("confirm",a),e.removeEventListener("cancel",o),t(i)},a=()=>i(!0),o=()=>i(!1);e.addEventListener("confirm",a),e.addEventListener("cancel",o),e.open()})}finally{this._autoFixConfirmOpen=!1}}_gotoErrorLine(e){this.dispatchEvent(new CustomEvent("goto-line",{detail:{line:e},bubbles:!0,composed:!0}))}_setLayout(e){this.dispatchEvent(new CustomEvent("layout-change",{detail:e,bubbles:!0,composed:!0}))}_onShowYamlEditor(e){e.stopPropagation(),this._setLayout("both")}_onYamlChange(e){this._lastEditAt=performance.now(),this.dispatchEvent(new CustomEvent("yaml-change",{detail:e.detail,bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.yaml="",this.layout="both",this.navCollapsed=!1,this.deviceTitle="",this.board=null,this.justCreated=!1,this._isMobile=!1,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._saveShortcut=new M.k(this,()=>{this.hasUnsavedEdits&&this._onSave()}),this.highlightRange=null,this.scrollToHighlight=!1,this.configuration="",this.selectedSection=null,this.backendErrors=g.eV,this.savedYaml="",this.hasUnsavedEdits=!1,this.saving=!1,this.showModified=!1,this.showUpdate=!1,this.installedVersion="",this.availableVersion="",this.busy=!1,this._showDiffButton=!1,this._showDiff=!1,this._revealSensitive=!1,this._liveErrors=[],this._caretLine=0,this._editorFocused=!1,this._completionOpen=!1,this._lastEditAt=-1/0,this._getLastEditAt=()=>this._lastEditAt,this._splitRatio=(()=>{try{let e=localStorage.getItem(P),t=null===e?NaN:Number.parseFloat(e);return Number.isFinite(t)?L(t):.5}catch{return .5}})(),this._dragging=!1,this._onEditorFocusIn=()=>{this._editorFocused=!0},this._onEditorFocusOut=e=>{let t=e.currentTarget;this._editorFocused=e.relatedTarget instanceof Node&&t.contains(e.relatedTarget)},this._autoFixConfirmOpen=!1,this._onDividerPointerDown=e=>{if(0!==e.button)return;let t=this._layoutEl;if(!t)return;e.preventDefault();let i=t.getBoundingClientRect();this._dragging=!0;let a=e.currentTarget;a.setPointerCapture(e.pointerId);let o=a.getBoundingClientRect().width,r=i.width-o,s=e=>{r<=0||(this._splitRatio=L((e.clientX-i.left-o/2)/r))},n=()=>{this._dragging=!1,F(this._splitRatio),a.removeEventListener("pointermove",s),a.removeEventListener("pointerup",n),a.removeEventListener("pointercancel",n),a.removeEventListener("lostpointercapture",n)};a.addEventListener("pointermove",s),a.addEventListener("pointerup",n),a.addEventListener("pointercancel",n),a.addEventListener("lostpointercapture",n)},this._onDividerKeydown=e=>{let t=((e,t)=>{let i;if("ArrowLeft"===t)i=e-.02;else if("ArrowRight"===t)i=e+.02;else if("Home"===t)i=.25;else{if("End"!==t)return null;i=.75}return L(i)})(this._splitRatio,e.key);null!==t&&(e.preventDefault(),this._splitRatio=t,F(this._splitRatio))}}}rs.styles=[v.G,O],rr([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],rs.prototype,"_localize",void 0),rr([(0,n.MZ)()],rs.prototype,"yaml",void 0),rr([(0,n.MZ)()],rs.prototype,"layout",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"navCollapsed",void 0),rr([(0,n.MZ)()],rs.prototype,"deviceTitle",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"board",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"justCreated",void 0),rr([(0,n.wk)()],rs.prototype,"_isMobile",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"highlightRange",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"scrollToHighlight",void 0),rr([(0,n.MZ)()],rs.prototype,"configuration",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"selectedSection",void 0),rr([(0,n.MZ)({type:Number})],rs.prototype,"selectedFromLine",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"focusFieldPath",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"backendErrors",void 0),rr([(0,n.MZ)({attribute:!1})],rs.prototype,"savedYaml",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"hasUnsavedEdits",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"saving",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"showModified",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"showUpdate",void 0),rr([(0,n.MZ)()],rs.prototype,"installedVersion",void 0),rr([(0,n.MZ)()],rs.prototype,"availableVersion",void 0),rr([(0,n.MZ)({type:Boolean})],rs.prototype,"busy",void 0),rr([(0,o.Fg)({context:m.Pt,subscribe:!0}),(0,n.wk)()],rs.prototype,"_showDiffButton",void 0),rr([(0,n.wk)()],rs.prototype,"_showDiff",void 0),rr([(0,n.wk)()],rs.prototype,"_revealSensitive",void 0),rr([(0,n.wk)()],rs.prototype,"_liveErrors",void 0),rr([(0,n.wk)()],rs.prototype,"_caretLine",void 0),rr([(0,n.wk)()],rs.prototype,"_editorFocused",void 0),rr([(0,n.wk)()],rs.prototype,"_completionOpen",void 0),rr([(0,n.wk)()],rs.prototype,"_splitRatio",void 0),rr([(0,n.wk)()],rs.prototype,"_dragging",void 0),rr([(0,n.P)(".editor-layout")],rs.prototype,"_layoutEl",void 0),rr([(0,n.P)("esphome-yaml-editor")],rs.prototype,"_yamlEditor",void 0),rr([(0,n.P)("esphome-confirm-dialog.auto-fix-confirm")],rs.prototype,"_autoFixConfirmDialog",void 0),rr([(0,n.wk)()],rs.prototype,"_autoFixConfirmOpen",void 0),rs=rr([(0,n.EM)("esphome-device-editor")],rs);class rn{get tick(){return this._tick}hostConnected(){this._unsubscribes=this._subscribes.map(e=>e(()=>{this._tick++,this._host.requestUpdate()}))}hostDisconnected(){for(let e of this._unsubscribes)e();this._unsubscribes=[]}constructor(e,t){this._host=e,this._subscribes=t,this._tick=0,this._unsubscribes=[],e.addController(this)}}let rl=(0,s.AH)`
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
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
`;function rd(e){let{core:t,components:i,automations:a}=(0,C.uU)((0,C.MT)(e)),o=(0,C.vB)(e);return{core:t,components:i,automations:[...a.filter(e=>"script"!==e.key&&"interval"!==e.key),...o].filter(e=>!e.key.startsWith("automation:light_effect:")&&!e.key.startsWith("automation:unscoped:")).sort((e,t)=>e.fromLine-t.fromLine),substitutions:(0,e4.Gr)(e)}}function rc(e){let t=[],i=new Map;for(let a of e){let e=a.item.key,o=i.get(e);o||(o=[],i.set(e,o),t.push(e)),o.push(a)}return t.map(e=>({key:e,rows:i.get(e)}))}function rh(e,t,i){let a=(0,C.gU)(e);if("automation"===t)return function(e,t,i){if("script"===e.parentKey){let a=i.localize("device.script_header_title_static"),o=(0,e4.rq)(e.id??t,i.substitutions);return{primary:a,secondary:o!==a?o:void 0}}if("interval"===e.parentKey){let t=i.localize("device.automation_interval_label"),a=e.meta?.every;return{primary:t,secondary:a?i.localize("device.automation_interval_every_n",{time:a}):void 0}}if("esphome"===e.parentKey&&e.eventKey)return{primary:rm(i.triggerCatalog.resolveName("esphome",e.eventKey,ru(e.eventKey)))};if(e.parentKey&&e.eventKey){let t=rm(i.triggerCatalog.resolveName(e.parentKey,e.eventKey,ru(e.eventKey)));return{primary:t,secondary:rp(e,i,t)}}if(e.parentKey&&e.actionField){let t=oo(e.actionField,i.localize);return{primary:t,secondary:rp(e,i,t)}}return{primary:e.displayLabel||t}}(e,a,i);let o=a,r=(0,eD.CQ)(a,i.platform||void 0);r?.name&&(o=r.name),"core"===t&&(o=J(o));let s="core"===t&&"esphome"===e.key&&i.deviceName?i.deviceName:(0,e4.rq)(e.name||e.id||"",i.substitutions)||void 0,n=s&&s!==o?s:void 0;return{primary:o,secondary:n}}function rp(e,t,i){let a=e.name||e.id,o=a?(0,e4.rq)(a,t.substitutions):rv(e.parentKey??"");return o!==i?o:void 0}function ru(e){return e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}function rm(e){let t=e.lastIndexOf(" → ");return t>=0?e.slice(t+3):e}function rv(e){let t=e.replace(/_/g," ");return t.charAt(0).toUpperCase()+t.slice(1)}let rg={esphome:["chip",r.mdiChip],wifi:["wifi",r.mdiWifi],ethernet:["ethernet",r.mdiEthernet],mdns:["radio-tower",r.mdiRadioTower],network:["lan",r.mdiLan],api:["api",r.mdiApi],ota:["cloud-upload-outline",r.mdiCloudUploadOutline],dashboard_import:["cloud-upload-outline",r.mdiCloudUploadOutline],logger:["card-text-outline",r.mdiCardTextOutline],syslog:["card-text-outline",r.mdiCardTextOutline],web_server:["web",r.mdiWeb],http_request:["web",r.mdiWeb],captive_portal:["wifi-lock",r.mdiWifiLock],improv_serial:["wifi-cog",r.mdiWifiCog],esp32_improv:["wifi-cog",r.mdiWifiCog],mqtt:["swap-horizontal",r.mdiSwapHorizontal],wireguard:["vpn",r.mdiVpn],socket:["connection",r.mdiConnection],udp:["connection",r.mdiConnection],async_tcp:["connection",r.mdiConnection],espnow:["connection",r.mdiConnection],serial_proxy:["connection",r.mdiConnection],sim800l:["connection",r.mdiConnection],prometheus:["chart-line",r.mdiChartLine],statsd:["chart-line",r.mdiChartLine],runtime_stats:["chart-line",r.mdiChartLine],time:["clock-outline",r.mdiClockOutline],sntp:["clock-outline",r.mdiClockOutline],interval:["clock-outline",r.mdiClockOutline],script:["script-text-outline",r.mdiScriptTextOutline],uart:["serial-port",r.mdiSerialPort],i2c:["connection",r.mdiConnection],spi:["connection",r.mdiConnection],modbus:["connection",r.mdiConnection],modbus_controller:["connection",r.mdiConnection],modbus_server:["connection",r.mdiConnection],esp32:["cpu-32-bit",r.mdiCpu32Bit],esp8266:["cpu-32-bit",r.mdiCpu32Bit],rp2040:["cpu-32-bit",r.mdiCpu32Bit],rp2:["cpu-32-bit",r.mdiCpu32Bit],bk72xx:["cpu-32-bit",r.mdiCpu32Bit],rtl87xx:["cpu-32-bit",r.mdiCpu32Bit],ln882x:["cpu-32-bit",r.mdiCpu32Bit],libretiny:["cpu-32-bit",r.mdiCpu32Bit],nrf52:["cpu-32-bit",r.mdiCpu32Bit],host:["chip",r.mdiChip],esp32_hosted:["wifi",r.mdiWifi],esp32_ble:["bluetooth",r.mdiBluetooth],esp32_ble_tracker:["bluetooth",r.mdiBluetooth],ble:["bluetooth",r.mdiBluetooth],bluetooth_proxy:["bluetooth",r.mdiBluetooth],ble_client:["bluetooth",r.mdiBluetooth],ble_nus:["bluetooth",r.mdiBluetooth],esp32_ble_beacon:["bluetooth",r.mdiBluetooth],esp32_ble_server:["bluetooth",r.mdiBluetooth],zephyr_ble_server:["bluetooth",r.mdiBluetooth],rp2040_ble:["bluetooth",r.mdiBluetooth],exposure_notifications:["bluetooth",r.mdiBluetooth],airthings_ble:["bluetooth",r.mdiBluetooth],bedjet:["bluetooth",r.mdiBluetooth],mopeka_ble:["bluetooth",r.mdiBluetooth],radon_eye_ble:["bluetooth",r.mdiBluetooth],ruuvi_ble:["bluetooth",r.mdiBluetooth],xiaomi_ble:["bluetooth",r.mdiBluetooth],xiaomi_rtcgq02lm:["bluetooth",r.mdiBluetooth],zwave_proxy:["z-wave",r.mdiZWave],zigbee:["zigbee",r.mdiZigbee],openthread:["zigbee",r.mdiZigbee],usb_host:["usb",r.mdiUsb],usb_uart:["usb",r.mdiUsb],usb_cdc_acm:["usb",r.mdiUsb],tinyusb:["usb",r.mdiUsb],psram:["memory",r.mdiMemory],preferences:["content-save-cog-outline",r.mdiContentSaveCogOutline],power_supply:["power-plug",r.mdiPowerPlug],esp_ldo:["power-plug",r.mdiPowerPlug],sy6970:["power-plug",r.mdiPowerPlug],deep_sleep:["power-sleep",r.mdiPowerSleep],status_led:["led-on",r.mdiLedOn],safe_mode:["restart-alert",r.mdiRestartAlert],factory_reset:["restart-alert",r.mdiRestartAlert],debug:["bug",r.mdiBug],globals:["variable",r.mdiVariable],substitutions:["code-braces",r.mdiCodeBraces],packages:["package-variant-closed",r.mdiPackageVariantClosed],external_components:["puzzle-outline",r.mdiPuzzleOutline],mapping:["cog",r.mdiCog],json:["code-json",r.mdiCodeJson],bytebuffer:["code-array",r.mdiCodeArray],split_buffer:["code-array",r.mdiCodeArray],sha256:["pound-box-outline",r.mdiPoundBoxOutline],hmac_md5:["pound-box-outline",r.mdiPoundBoxOutline],hmac_sha256:["pound-box-outline",r.mdiPoundBoxOutline],remote_receiver:["remote",r.mdiRemote],remote_transmitter:["remote",r.mdiRemote],cc1101:["remote",r.mdiRemote],sx126x:["remote",r.mdiRemote],sx127x:["remote",r.mdiRemote],lightwaverf:["remote",r.mdiRemote],rf_bridge:["remote",r.mdiRemote],pn532:["nfc-variant",r.mdiNfcVariant],pn532_i2c:["nfc-variant",r.mdiNfcVariant],pn532_spi:["nfc-variant",r.mdiNfcVariant],pn7150_i2c:["nfc-variant",r.mdiNfcVariant],pn7160_i2c:["nfc-variant",r.mdiNfcVariant],pn7160_spi:["nfc-variant",r.mdiNfcVariant],rc522_i2c:["nfc-variant",r.mdiNfcVariant],rc522_spi:["nfc-variant",r.mdiNfcVariant],rdm6300:["nfc-variant",r.mdiNfcVariant],ld2410:["motion-sensor",r.mdiMotionSensor],ld2412:["motion-sensor",r.mdiMotionSensor],ld2420:["motion-sensor",r.mdiMotionSensor],ld2450:["motion-sensor",r.mdiMotionSensor],rd03d:["motion-sensor",r.mdiMotionSensor],at581x:["motion-sensor",r.mdiMotionSensor],dfrobot_sen0395:["motion-sensor",r.mdiMotionSensor],hlk_fm22x:["motion-sensor",r.mdiMotionSensor],seeed_mr24hpc1:["motion-sensor",r.mdiMotionSensor],seeed_mr60bha2:["motion-sensor",r.mdiMotionSensor],seeed_mr60fda2:["motion-sensor",r.mdiMotionSensor],esp32_touch:["gesture-tap-button",r.mdiGestureTapButton],cap1188:["gesture-tap-button",r.mdiGestureTapButton],mpr121:["gesture-tap-button",r.mdiGestureTapButton],ttp229_bsf:["gesture-tap-button",r.mdiGestureTapButton],ttp229_lsf:["gesture-tap-button",r.mdiGestureTapButton],matrix_keypad:["dialpad",r.mdiDialpad],wiegand:["dialpad",r.mdiDialpad],key_collector:["dialpad",r.mdiDialpad],fingerprint_grow:["fingerprint",r.mdiFingerprint],i2s_audio:["volume-high",r.mdiVolumeHigh],audio:["volume-high",r.mdiVolumeHigh],audio_file:["volume-high",r.mdiVolumeHigh],microphone:["microphone",r.mdiMicrophone],micro_wake_word:["microphone",r.mdiMicrophone],voice_assistant:["microphone-message",r.mdiMicrophoneMessage],speaker:["speaker",r.mdiSpeaker],dfplayer:["speaker",r.mdiSpeaker],rtttl:["speaker",r.mdiSpeaker],adalight:["lightbulb-outline",r.mdiLightbulbOutline],wled:["lightbulb-outline",r.mdiLightbulbOutline],e131:["lightbulb-outline",r.mdiLightbulbOutline],my9231:["lightbulb-outline",r.mdiLightbulbOutline],sm16716:["lightbulb-outline",r.mdiLightbulbOutline],sm2135:["lightbulb-outline",r.mdiLightbulbOutline],sm2235:["lightbulb-outline",r.mdiLightbulbOutline],sm2335:["lightbulb-outline",r.mdiLightbulbOutline],bp1658cj:["lightbulb-outline",r.mdiLightbulbOutline],bp5758d:["lightbulb-outline",r.mdiLightbulbOutline],tlc59208f:["lightbulb-outline",r.mdiLightbulbOutline],tlc5947:["lightbulb-outline",r.mdiLightbulbOutline],tlc5971:["lightbulb-outline",r.mdiLightbulbOutline],tm1651:["lightbulb-outline",r.mdiLightbulbOutline],adc128s102:["gauge",r.mdiGauge],ads1115:["gauge",r.mdiGauge],ads1118:["gauge",r.mdiGauge],mcp3008:["gauge",r.mdiGauge],mcp3204:["gauge",r.mdiGauge],as5600:["gauge",r.mdiGauge],dac7678:["export-variant",r.mdiExportVariant],gp8403:["export-variant",r.mdiExportVariant],mcp4728:["export-variant",r.mdiExportVariant],mcp4461:["export-variant",r.mdiExportVariant],pca9685:["export-variant",r.mdiExportVariant],servo:["export-variant",r.mdiExportVariant],grove_tb6612fng:["export-variant",r.mdiExportVariant],mcp23008:["connection",r.mdiConnection],mcp23016:["connection",r.mdiConnection],mcp23017:["connection",r.mdiConnection],mcp23s08:["connection",r.mdiConnection],mcp23s17:["connection",r.mdiConnection],pca6416a:["connection",r.mdiConnection],pca9554:["connection",r.mdiConnection],pcf8574:["connection",r.mdiConnection],pi4ioe5v6408:["connection",r.mdiConnection],xl9535:["connection",r.mdiConnection],max6956:["connection",r.mdiConnection],sn74hc165:["connection",r.mdiConnection],sn74hc595:["connection",r.mdiConnection],cd74hc4067:["connection",r.mdiConnection],tca9548a:["connection",r.mdiConnection],tca9555:["connection",r.mdiConnection],ch422g:["connection",r.mdiConnection],ch423:["connection",r.mdiConnection],sx1509:["connection",r.mdiConnection],m5stack_8angle:["connection",r.mdiConnection],i2c_device:["connection",r.mdiConnection],spi_device:["connection",r.mdiConnection],vbus:["connection",r.mdiConnection],tuya:["connection",r.mdiConnection],wk2132_i2c:["serial-port",r.mdiSerialPort],wk2132_spi:["serial-port",r.mdiSerialPort],wk2168_i2c:["serial-port",r.mdiSerialPort],wk2168_spi:["serial-port",r.mdiSerialPort],wk2204_i2c:["serial-port",r.mdiSerialPort],wk2204_spi:["serial-port",r.mdiSerialPort],wk2212_i2c:["serial-port",r.mdiSerialPort],wk2212_spi:["serial-port",r.mdiSerialPort],apds9960:["gauge",r.mdiGauge],as3935_i2c:["gauge",r.mdiGauge],as3935_spi:["gauge",r.mdiGauge],bme680_bsec:["gauge",r.mdiGauge],bme68x_bsec2_i2c:["gauge",r.mdiGauge],gdk101:["gauge",r.mdiGauge],msa3xx:["gauge",r.mdiGauge],ezo_pmp:["gauge",r.mdiGauge],daly_bms:["gauge",r.mdiGauge],pylontech:["gauge",r.mdiGauge],pipsolar:["gauge",r.mdiGauge],sun_gtil2:["gauge",r.mdiGauge],sml:["gauge",r.mdiGauge],dsmr:["gauge",r.mdiGauge],teleinfo:["gauge",r.mdiGauge],dlms_meter:["gauge",r.mdiGauge],emontx:["gauge",r.mdiGauge],emc2101:["fan",r.mdiFan],gps:["crosshairs-gps",r.mdiCrosshairsGps],sun:["weather-sunny",r.mdiWeatherSunny],opentherm:["thermostat",r.mdiThermostat],uponor_smatrix:["thermostat",r.mdiThermostat],micronova:["thermostat",r.mdiThermostat],sprinkler:["sprinkler-variant",r.mdiSprinklerVariant],sensor:["gauge",r.mdiGauge],binary_sensor:["checkbox-marked-circle-outline",r.mdiCheckboxMarkedCircleOutline],text_sensor:["text-box-outline",r.mdiTextBoxOutline],switch:["toggle-switch-outline",r.mdiToggleSwitchOutline],light:["lightbulb-outline",r.mdiLightbulbOutline],output:["export-variant",r.mdiExportVariant],number:["numeric",r.mdiNumeric],select:["form-dropdown",r.mdiFormDropdown],button:["gesture-tap-button",r.mdiGestureTapButton],fan:["fan",r.mdiFan],cover:["window-shutter",r.mdiWindowShutter],climate:["thermostat",r.mdiThermostat],text:["form-textbox",r.mdiFormTextbox],lock:["lock-outline",r.mdiLockOutline],valve:["valve",r.mdiValve],media_player:["speaker",r.mdiSpeaker],display:["monitor",r.mdiMonitor],lvgl:["monitor",r.mdiMonitor],graphical_display_menu:["monitor",r.mdiMonitor],lcd_menu:["monitor",r.mdiMonitor],datetime:["calendar-clock",r.mdiCalendarClock],camera:["camera-outline",r.mdiCameraOutline],esp32_camera:["camera-outline",r.mdiCameraOutline],esp32_camera_web_server:["camera-outline",r.mdiCameraOutline],camera_encoder:["camera-outline",r.mdiCameraOutline],event:["bell-outline",r.mdiBellOutline],alarm_control_panel:["shield-home-outline",r.mdiShieldHomeOutline],graph:["chart-line",r.mdiChartLine],color:["palette",r.mdiPalette],qr_code:["qrcode",r.mdiQrcode],font:["format-font",r.mdiFormatFont],image:["image-outline",r.mdiImageOutline],online_image:["image-sync-outline",r.mdiImageSyncOutline],animation:["image-multiple-outline",r.mdiImageMultipleOutline]},rf=["shape-outline",r.mdiShapeOutline];function r_(e,t,i){var a;let{item:o,labels:r}=e,{primary:n,secondary:l}=r,d=o.parentKey??o.key,c=t.errorCount?.(o)??0;return(0,s.qy)`
    <div
      class="nav-item ${t.selectedLine===o.fromLine?"nav-item--selected":""} ${t.hoveredLine===o.fromLine?"nav-item--hovered":""}"
      @mouseenter=${()=>t.onItemEnter(o)}
      @mouseleave=${()=>t.onItemLeave()}
      @click=${()=>t.onItemClick(o)}
    >
      ${i?"esphome"===(a=d)?(0,s.qy)`<wa-icon
      class="nav-item-icon"
      src=${(0,f.cV)("/assets/logo/esphome-mono.svg")}
      title="ESPHome"
    ></wa-icon>`:(0,s.qy)`<wa-icon
    class="nav-item-icon"
    library="mdi"
    name=${(rg[a]??rf)[0]}
    title=${rv(a)}
  ></wa-icon>`:s.s6}
      <div class="nav-item-content">
        <p>${n}</p>
        ${l?(0,s.qy)`<span class="nav-item-subtitle">${l}</span>`:s.s6}
      </div>
      ${c>0?rb(c,t):s.s6}
      <wa-icon class="nav-item-chevron" library="mdi" name="chevron-right"></wa-icon>
    </div>
  `}function rb(e,t){return(0,s.qy)`<span
    class="nav-item-error-badge"
    role="img"
    aria-label=${t.errorLabel(e)}
    >${e}</span
  >`}(0,k.C)(Object.fromEntries([...Object.values(rg),rf]));class ry{hostUpdated(){let{selectedLine:e,buckets:t,openSections:i,filtering:a}=this._read();if(null===e){this._scrolledLine=null,this._revealedLine=null;return}if(null!==this._revealedLine&&this._revealedLine!==e&&(this._revealedLine=null),e===this._scrolledLine)return;let o=t.core.some(t=>t.fromLine===e)?0:t.components.some(t=>t.fromLine===e)?1:t.automations.some(t=>t.fromLine===e)?2:-1;if(-1===o){this._scrolledLine=e;return}if(!a&&!i.has(o)&&this._revealedLine!==e){this._revealedLine=e,this._host.dispatchEvent(new CustomEvent("section-reveal",{detail:{index:o},bubbles:!0,composed:!0}));return}this._revealedLine=e;let r=this._host.renderRoot.querySelector(".nav-item--selected");r&&r.getClientRects().length>0&&(r.scrollIntoView({block:"nearest"}),this._scrolledLine=e)}constructor(e,t){this._host=e,this._read=t,this._scrolledLine=null,this._revealedLine=null,e.addController(this)}}function rw(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({close:r.mdiClose});class r$ extends s.WF{open(){this._id="",this._error="",this._dialog.open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml)}catch(e){this._error=(0,W.u)(e)}}render(){let e=this.boardName?this._localize("device.add_script_dialog_title",{name:this.boardName}):this._localize("device.add_script");return(0,s.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,B.Gc)(this._localize("device.script_header_description"))}
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
          @input=${e=>{this._id=(0,aD.e)(e.target.value),this._error=""}}
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
    </esphome-base-dialog>`}_canContinue(){return!!this._id&&!this._available?.scripts.some(e=>e.id===this._id)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new H.T(this),this._id="",this._available=null,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"script",id:this._id},{yaml_diff:t}=await this._api.upsertAutomation(this.configuration,{trigger_id:null,trigger_params:{mode:"single"},actions:[]},e,this.yaml);ef(this,this.yaml,e,t),this._dialog.open=!1}catch(t){let e=(0,Y.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,d.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}r$.styles=[v.G,G.z9,V,(0,s.AH)`
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
    `],rw([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],r$.prototype,"_localize",void 0),rw([(0,o.Fg)({context:m.Ie})],r$.prototype,"_api",void 0),rw([(0,n.MZ)()],r$.prototype,"boardName",void 0),rw([(0,n.MZ)()],r$.prototype,"configuration",void 0),rw([(0,n.MZ)()],r$.prototype,"yaml",void 0),rw([(0,n.MZ)({attribute:!1})],r$.prototype,"board",void 0),rw([(0,n.wk)()],r$.prototype,"_id",void 0),rw([(0,n.wk)()],r$.prototype,"_available",void 0),rw([(0,n.wk)()],r$.prototype,"_saving",void 0),rw([(0,n.wk)()],r$.prototype,"_error",void 0),r$=rw([(0,n.EM)("esphome-add-script-dialog")],r$);let rx=(0,s.AH)`
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
    ${G.BJ}
  }

  .search:focus-within {
    ${G.jq}
  }

  input {
    flex: 1;
    min-width: 0;
    border: none;
    background: transparent;
    color: var(--wa-color-text-normal);
    ${G.xw}
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
`;function rk(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({close:r.mdiClose});class rz extends s.WF{focusInput(){this._input?.focus()}render(){let e=this._localize("device.navigator_search_placeholder");return(0,s.qy)`
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
        ${this.value?(0,s.qy)`<button
                type="button"
                class="search-clear"
                @click=${this._clear}
                title=${this._localize("device.navigator_search_clear")}
                aria-label=${this._localize("device.navigator_search_clear")}
              >
                <wa-icon library="mdi" name="close"></wa-icon>
              </button>`:s.s6}
      </div>
      ${this.value&&this.resultLabel?(0,s.qy)`<p class="search-result" role="status">${this.resultLabel}</p>`:s.s6}
    `}_emit(e){this.dispatchEvent(new CustomEvent("navigator-search",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.value="",this.resultLabel="",this._onInput=e=>{this.value=e.target.value,this._emit(this.value)},this._onKeydown=e=>{"Escape"===e.key&&this._input?.value&&(e.stopPropagation(),this._clear())},this._clear=()=>{this.value="",this._emit(""),this._input?.focus()}}}function rC(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}rz.styles=[v.G,rx],rk([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],rz.prototype,"_localize",void 0),rk([(0,n.MZ)()],rz.prototype,"value",void 0),rk([(0,n.MZ)()],rz.prototype,"resultLabel",void 0),rk([(0,n.P)("input")],rz.prototype,"_input",void 0),rz=rk([(0,n.EM)("esphome-navigator-search")],rz),(0,k.C)({"chevron-down":r.mdiChevronDown,"chevron-up":r.mdiChevronUp,"chevron-right":r.mdiChevronRight,cog:r.mdiCog,magnify:r.mdiMagnify,menu:r.mdiMenu,"plus-circle-outline":r.mdiPlusCircleOutline,"script-text-outline":r.mdiScriptTextOutline});class rq extends s.WF{willUpdate(e){if((e.has("yaml")||e.has("platform")||e.has("platformReady"))&&this.yaml&&this.platformReady&&this._kickoffNameResolves(),(e.has("selectedKey")||e.has("yaml")||e.has("selectedFromLine"))&&this.yaml){if(!this.selectedKey){this._selectedLine=null,this._selectedRange=null;return}let e=[...(0,C.MT)(this.yaml),...(0,C.vB)(this.yaml)],t=(void 0!==this.selectedFromLine?e.find(e=>e.fromLine===this.selectedFromLine):void 0)??e.find(e=>(0,C.gU)(e)===this.selectedKey);t&&(this._selectedLine=t.fromLine,this._selectedRange={fromLine:t.fromLine,toLine:t.toLine})}}render(){let e=this._deriveBuckets(this.yaml),{core:t,components:i,automations:a}=e,o=[{label:this._localize("device.section_core"),desc:this._localize("device.section_core_desc"),icon:Z,items:t,category:"core",actions:[{label:this._localize("device.add_config"),icon:"cog",onClick:()=>this._addConfigDialog.open()}]},{label:this._localize("device.section_components"),desc:this._localize("device.section_components_desc"),icon:K,items:i,category:"component",actions:[{label:this._localize("device.add_component"),icon:K,onClick:()=>this._addComponentDialog.open()}]},{label:this._localize("device.section_automations"),desc:this._localize("device.section_automations_desc"),icon:U,items:a,category:"automation",actions:[{label:this._localize("device.add_automation"),icon:U,onClick:()=>this._addAutomationDialog.open()},{label:this._localize("device.add_script"),icon:"script-text-outline",onClick:()=>this._addScriptDialog.open()}]}],r=this._resolveLabels(e,this._caches.tick,this.platform,this.deviceName,this._localize),n=this._query.trim(),l=n.length>0,d=l?r.map(e=>e.filter(({item:e,labels:t})=>a_(n,t.primary,t.secondary,e.id,e.name))):null,c=o.reduce((e,t)=>e+t.items.length,0),h=this._expertMode&&(c>=15||this._searchOpen),p=this._expertMode&&(this._searchOpen||l),u=d?d.reduce((e,t)=>e+t.length,0):0,m=l&&u>0?this._localize("device.navigator_search_count",{count:u,total:c}):"";return(0,s.qy)`
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
          <div class="header-actions">
            ${h?(0,s.qy)`<button
                    type="button"
                    class="ghost-icon-btn search-btn"
                    aria-pressed=${p}
                    @click=${this._toggleSearch}
                    title=${this._localize("device.navigator_search_toggle")}
                    aria-label=${this._localize("device.navigator_search_toggle")}
                  >
                    <wa-icon library="mdi" name="magnify"></wa-icon>
                  </button>`:s.s6}
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
          ${l?s.s6:(0,s.qy)`<p class="italic">${this._localize("device.navigator_desc")}</p>`}
          <div class="separator"></div>
          ${l&&0===u?(0,s.qy)`<p class="nav-empty" role="status">
                  ${this._localize("device.navigator_search_none")}
                </p>`:o.map(({label:e,desc:t,icon:i,category:a,actions:o},n)=>{var c;let h=d?.[n]??r[n];return(c={label:e,desc:t,icon:i,actions:o,rows:h,groups:"component"===a?this._groupComponents(h):void 0,collapsedGroups:this._collapsedGroups,onToggleGroup:e=>this._toggleGroup(e),open:!!l||this.openSections.has(n),filtering:l,selectedLine:this._selectedLine,hoveredLine:this._hoveredLine,errorCount:this.errorCounts.size?e=>this.errorCounts.get((0,g.pA)((0,C.gU)(e),e.fromLine))??0:void 0,errorLabel:e=>this._localize("device.navigator_error_count",{count:e}),onToggle:()=>{l||this._toggleSection(n)},onItemEnter:e=>this._onItemHover(e.fromLine,e.fromLine,e.toLine),onItemLeave:()=>this._onItemLeave(),onItemClick:e=>this._onItemClick(e)}).filtering&&0===c.rows.length?s.s6:(0,s.qy)`
    <div class="nav-content" @click=${()=>c.onToggle()}>
      <div class="nav-content-label">
        <wa-icon library="mdi" name=${c.icon}></wa-icon>
        <p>${c.label}</p>
      </div>
      ${c.filtering?s.s6:(0,s.qy)`<wa-icon
              class="nav-content-chevron"
              library="mdi"
              name=${c.open?"chevron-up":"chevron-down"}
            ></wa-icon>`}
    </div>
    ${c.open?(0,s.qy)`
            <div class="separator"></div>
            ${c.filtering?s.s6:(0,s.qy)`<p class="italic">${c.desc}</p>`}
            ${c.groups?c.groups.map(e=>{var t,i;let a,o,r,n,l,d;return 1!==e.rows.length||e.rows[0].item.platform?(t=e,a=(i=c).filtering||!i.collapsedGroups?.has(t.key),o=!i.filtering,r=i.errorCount,n=!a&&r?t.rows.reduce((e,t)=>e+r(t.item),0):0,l=()=>{o&&i.onToggleGroup?.(t.key)},d=`navgroup-${t.key}`,(0,s.qy)`
    <div
      class="nav-subgroup-header ${o?"":"nav-subgroup-header--static"}"
      role=${(0,t7.J)(o?"button":void 0)}
      tabindex=${(0,t7.J)(o?"0":void 0)}
      aria-expanded=${(0,t7.J)(o?String(a):void 0)}
      aria-controls=${(0,t7.J)(o?d:void 0)}
      @click=${l}
      @keydown=${e=>{o&&("Enter"===e.key||" "===e.key)&&(e.preventDefault(),l())}}
    >
      <wa-icon
        class="nav-subgroup-icon"
        library="mdi"
        name=${(rg[t.key]??rf)[0]}
      ></wa-icon>
      <span class="nav-subgroup-title">${rv(t.key)}</span>
      <span class="nav-subgroup-count">${t.rows.length}</span>
      ${n>0?rb(n,i):s.s6}
      ${o?(0,s.qy)`<wa-icon
              class="nav-subgroup-chevron"
              library="mdi"
              name=${a?"chevron-up":"chevron-down"}
            ></wa-icon>`:s.s6}
    </div>
    ${a?(0,s.qy)`<div id=${d} class="nav-items nav-items--grouped">
            ${t.rows.map(e=>r_(e,i,!1))}
          </div>`:s.s6}
  `):(0,s.qy)`<div class="nav-items nav-items--single">
    ${r_(e.rows[0],c,!0)}
  </div>`}):c.rows.length>0?(0,s.qy)`<div class="nav-items">
                      ${c.rows.map(e=>r_(e,c,!0))}
                    </div>`:s.s6}
            ${c.filtering?s.s6:(0,s.qy)`<div class="nav-items">
                    ${c.actions.map(e=>(0,s.qy)`<div class="action-item" @click=${()=>e.onClick()}>
    <div>
      <wa-icon library="mdi" name=${e.icon}></wa-icon>
      <p>${e.label}</p>
    </div>
    <wa-icon library="mdi" name="plus-circle-outline"></wa-icon>
  </div>`)}
                  </div>`}
          `:s.s6}
    <div class="separator"></div>
  `})}
        </div>
      </section>
    `}_toggleSection(e){this.dispatchEvent(new CustomEvent("section-toggle",{detail:{index:e},bubbles:!0,composed:!0}))}_toggleGroup(e){let t=new Set(this._collapsedGroups);t.delete(e)||t.add(e),this._collapsedGroups=t}_kickoffNameResolves(){if(!this._api)return;let e=(0,C.MT)(this.yaml),{core:t,components:i}=(0,C.uU)(e),a=this.platform||void 0;for(let e of[...t,...i]){let t=(0,C.gU)(e);void 0===(0,eD.CQ)(t,a)&&(0,eD.Sn)(this._api,t,a).catch(()=>{})}this._triggerCatalog.ensure()}_onItemHover(e,t,i){this._hoveredLine=e,this._emitHighlight({fromLine:t,toLine:i},!1)}_onItemLeave(){this._hoveredLine=null,this._emitHighlight(this._selectedRange,!1)}_onItemClick(e){let{fromLine:t,toLine:i}=e,a=(0,C.gU)(e);this._selectedLine===t?(this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._emitHighlight(this._hoveredLine===t?{fromLine:t,toLine:i}:null,!1),this._emitSectionSelect(null,void 0)):(this.selectedKey=a,this._selectedLine=t,this._selectedRange={fromLine:t,toLine:i},this._emitHighlight({fromLine:t,toLine:i},!0),this._emitSectionSelect(a,t))}_emitHighlight(e,t){this.dispatchEvent(new CustomEvent("yaml-highlight",{detail:{range:e,scroll:t},bubbles:!0,composed:!0}))}_emitSectionSelect(e,t){this.dispatchEvent(new CustomEvent("section-select",{detail:{sectionKey:e,fromLine:t},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._caches=new rn(this,[eD.Ej,iT]),this._triggerCatalog=new o_(this,()=>({api:this._api,platform:this.platform||void 0,boardId:this.board?.id})),this._reveal=new ry(this,()=>({selectedLine:this._selectedLine,buckets:this._deriveBuckets(this.yaml),openSections:this.openSections,filtering:this._query.trim().length>0})),this.openSections=new Set,this.yaml="",this._deriveBuckets=(0,l.A)(rd),this._groupComponents=(0,l.A)(rc),this._resolveLabels=(0,l.A)((e,t,i,a,o)=>{var r;return r={triggerCatalog:this._triggerCatalog,platform:i,deviceName:a,localize:o,substitutions:e.substitutions},[e.core.map(e=>({item:e,labels:rh(e,"core",r)})),e.components.map(e=>({item:e,labels:rh(e,"component",r)})),e.automations.map(e=>({item:e,labels:rh(e,"automation",r)}))]}),this.board=null,this.boardName="",this.configuration="",this.deviceName="",this.platform="",this.platformReady=!1,this.selectedKey=null,this.errorCounts=new Map,this._selectedLine=null,this._selectedRange=null,this._hoveredLine=null,this._expertMode=!1,this._query="",this._searchOpen=!1,this._collapsedGroups=new Set,this._onSearchChange=e=>{this._query=e.detail.value},this._toggleSearch=()=>{if(this._searchOpen||this._query){this._searchOpen=!1,this._query="";return}this._searchOpen=!0,this.updateComplete.then(()=>this._search?.focusInput())},this._onCollapseClick=()=>{this.dispatchEvent(new CustomEvent("nav-collapse",{bubbles:!0,composed:!0}))},this._onAutomationAdded=e=>{e.stopPropagation(),this._emitSectionSelect(e.detail.sectionKey,void 0)}}}rq.styles=[v.G,rl],rC([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],rq.prototype,"_localize",void 0),rC([(0,o.Fg)({context:m.Ie})],rq.prototype,"_api",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"openSections",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"yaml",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"board",void 0),rC([(0,n.MZ)()],rq.prototype,"boardName",void 0),rC([(0,n.MZ)()],rq.prototype,"configuration",void 0),rC([(0,n.MZ)()],rq.prototype,"deviceName",void 0),rC([(0,n.MZ)()],rq.prototype,"platform",void 0),rC([(0,n.MZ)({type:Boolean})],rq.prototype,"platformReady",void 0),rC([(0,n.P)("esphome-add-config-dialog")],rq.prototype,"_addConfigDialog",void 0),rC([(0,n.P)("esphome-add-component-dialog")],rq.prototype,"_addComponentDialog",void 0),rC([(0,n.P)("esphome-add-automation-dialog")],rq.prototype,"_addAutomationDialog",void 0),rC([(0,n.P)("esphome-add-script-dialog")],rq.prototype,"_addScriptDialog",void 0),rC([(0,n.P)("esphome-navigator-search")],rq.prototype,"_search",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"selectedKey",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"selectedFromLine",void 0),rC([(0,n.MZ)({attribute:!1})],rq.prototype,"errorCounts",void 0),rC([(0,n.wk)()],rq.prototype,"_selectedLine",void 0),rC([(0,n.wk)()],rq.prototype,"_selectedRange",void 0),rC([(0,n.wk)()],rq.prototype,"_hoveredLine",void 0),rC([(0,o.Fg)({context:m.Pt,subscribe:!0}),(0,n.wk)()],rq.prototype,"_expertMode",void 0),rC([(0,n.wk)()],rq.prototype,"_query",void 0),rC([(0,n.wk)()],rq.prototype,"_searchOpen",void 0),rC([(0,n.wk)()],rq.prototype,"_collapsedGroups",void 0),rq=rC([(0,n.EM)("esphome-device-navigator")],rq),i(5973),i(3640),i(6895),i(9786);var rE=i(6029);function rS(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}(0,k.C)({"alert-outline":r.mdiAlertOutline});class rA extends s.WF{get _canGoToError(){return this.firstErrorLine>0&&!this.firstErrorFile}open(){this._resolvedExit=null,this._dialog.open=!0}close(){this._dialog.open=!1}render(){let e=this._localize("device.yaml_invalid_message",{count:this.errorCount}),t=this.firstErrorFile?this._localize("device.yaml_invalid_in_included_file",{file:this.firstErrorFile,line:this.firstErrorLine}):"";return(0,s.qy)`
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
    `}_goto(){this._canGoToError&&null===this._resolvedExit&&(this._resolvedExit="goto",this.close(),this.dispatchEvent(new CustomEvent("goto",{detail:{line:this.firstErrorLine,col:this.firstErrorCol},bubbles:!0,composed:!0})))}_saveAnyway(){this._resolvedExit="save-anyway",this.close(),this.dispatchEvent(new CustomEvent("save-anyway",{bubbles:!0,composed:!0}))}_onAfterHide(){this._dialog.open=!1,null===this._resolvedExit&&this.dispatchEvent(new CustomEvent("cancel",{bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this.errorCount=0,this.firstErrorLine=0,this.firstErrorCol=0,this.firstErrorMessage="",this.firstErrorFile="",this._dialog=new H.T(this),this._resolvedExit=null,this._gotoOnEnter=()=>{this._canGoToError&&this._goto()}}}function rM(e,t,i,a){var o,r=arguments.length,s=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,a);else for(var n=e.length-1;n>=0;n--)(o=e[n])&&(s=(r<3?o(s):r>3?o(t,i,s):o(t,i))||s);return r>3&&s&&Object.defineProperty(t,i,s),s}rA.styles=[v.G,rE.W,(0,s.AH)`
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
    `],rS([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],rA.prototype,"_localize",void 0),rS([(0,n.MZ)({type:Number})],rA.prototype,"errorCount",void 0),rS([(0,n.MZ)({type:Number})],rA.prototype,"firstErrorLine",void 0),rS([(0,n.MZ)({type:Number})],rA.prototype,"firstErrorCol",void 0),rS([(0,n.MZ)()],rA.prototype,"firstErrorMessage",void 0),rS([(0,n.MZ)()],rA.prototype,"firstErrorFile",void 0),rA=rS([(0,n.EM)("esphome-yaml-validation-dialog")],rA),(0,k.C)({"arrow-left":r.mdiArrowLeft,"chevron-right":r.mdiChevronRight,menu:r.mdiMenu});class rP extends s.WF{get _device(){return this._devices.find(e=>e.configuration===this.id)??null}_createInstallController(){let e=this;return new u({addController:t=>e.addController(t),removeController:t=>e.removeController(t),requestUpdate:()=>e.requestUpdate(),get updateComplete(){return e.updateComplete},get device(){return e._device},get commandDialog(){return e._commandDialog??null},get firmwareDialog(){return e._firmwareDialog??null}})}get _isYamlDirty(){return this._yaml!==this._savedYaml}get _isDirty(){return this._isYamlDirty||this._sectionDirty}async connectedCallback(){super.connectedCallback(),this._loadPreferences(),(0,$.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("keydown",this._onKeydown),this._mql.addEventListener("change",this._onMqlChange)}disconnectedCallback(){super.disconnectedCallback(),(0,$.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),window.removeEventListener("keydown",this._onKeydown),this._mql.removeEventListener("change",this._onMqlChange),this._unsavedGuard.cancelPending()}_isTextEntry(e){if(!e)return!1;let t=e.tagName;if("INPUT"===t||"TEXTAREA"===t||"SELECT"===t||e.isContentEditable)return!0;let i=e;for(;i;){if("ESPHOME-YAML-EDITOR"===i.tagName)return!0;i=i.parentElement}return!1}updated(e){e.has("id")&&this.id&&(this._justCreated=(0,w.RI)(this.id),this._loadedBoardId=null,this._board=null,this._platformReady=!1,this._backendErrors.length&&(this._backendErrors=[]),this._loadYaml());let t=this._device?.board_id??null;t&&t!==this._loadedBoardId?(this._loadedBoardId=t,this._board=null,this._platformReady=!1,this._loadBoard(t)):!t&&(null!==this._loadedBoardId&&(this._loadedBoardId=null,this._board=null),(null!==this._device||this._devicesLoaded)&&(this._platformReady=!0))}_readStoredLayout(){let e=localStorage.getItem("esphome-editor-layout");return"both"===e||"left"===e||"right"===e?e:null}async _loadPreferences(){let e=this._readStoredLayout();e&&(this._layout=e);try{let t=await this._api.getPreferences();this._navCollapsed=!t.navigator_visible,e||null!==this._readStoredLayout()||(this._layout=(0,y.r5)(t.device_editor_layout))}catch(e){console.warn("Failed to load device preferences:",e)}}async _loadBoard(e){try{let t=await (0,_.tK)(this._api,e);this._loadedBoardId===e&&(this._board=t,this._platformReady=!0)}catch(t){console.error("Failed to load board:",t),this._loadedBoardId===e&&(this._board=null,this._platformReady=!0)}}async _loadYaml(){try{let e=await this._api.getConfig(this.id);this._yaml=e,this._savedYaml=e,this._maybeResolveLineFromUrl()}catch(e){console.error("Failed to load YAML:",e)}}_maybeResolveLineFromUrl(){let e=q(this._yaml,this._selectedFromLine,this._selectedSection);e&&(this._selectedSection=e.sectionKey,this._setHighlight(e.range,!0))}_jumpToErrorLine(e){if(!e||e<1)return;"left"===this._layout&&this._cacheLayout("both"),this._setHighlight({fromLine:e,toLine:e},!0,!0);let t=q(this._yaml,e,null);t&&(this._selectedSection=t.sectionKey)}_resolveValidationPrompt(e){let t=this._pendingValidationResolve;this._pendingValidationResolve=null,t?.(e)}render(){let e=this._device?.friendly_name||this._device?.name||this.id||this._localize("dashboard.create_device"),t=this._isMobile?!this._drawerOpen:this._navCollapsed,i=this._localize("device.back");return(0,s.qy)`
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
            .backendErrors=${this._instanceBackendErrors(this._backendErrors,this._selectedSection,this._selectedFromLine)}
            .justCreated=${this._justCreated}
            @just-created-dismiss=${this._dismissJustCreated}
            @goto-line=${this._onEditorGoToLine}
            @change-board=${this._onChangeBoard}
            ?hasUnsavedEdits=${this._isDirty}
            ?saving=${this._saving}
            ?showModified=${!!this._device&&(0,b.EJ)(this._device)}
            ?showUpdate=${!!this._device&&(0,b.QH)(this._device)}
            .installedVersion=${this._device?.deployed_version??""}
            .availableVersion=${this._device?.current_version??""}
            ?busy=${this._activeJobs.has(this.id)}
          >
            ${t||this._selectedSection?(0,s.qy)`<div slot="header-start" class="header-start-group">
                    ${t?(0,s.qy)`<button
                            type="button"
                            class="ghost-icon-btn nav-toggle-btn"
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
          .canFlashBootloader=${this._installCtrl.canFlashBootloader}
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
      </div>
    `}_onSectionToggle(e){let{index:t}=e.detail,i=new Set;this._openSections.has(t)||i.add(t),this._openSections=i,this._updateUrl()}_onSectionReveal(e){let{index:t}=e.detail;this._openSections.has(t)||(this._openSections=new Set([t]),this._updateUrl())}_onNavSectionShow(e){let t={core:0,components:1,automations:2}[e.detail.section];if(void 0===t)return;let i=new Set([t]);this._openSections=i,this._updateUrl(),this._drawerOpen=!0,this._navCollapsed&&(this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{}))}_onLayoutChange(e){this._persistLayout(e.detail)}_cacheLayout(e){this._layout=e,localStorage.setItem("esphome-editor-layout",e)}_persistLayout(e){this._cacheLayout(e),this._api.updatePreferences({device_editor_layout:(0,y.jr)(e)}).catch(e=>console.warn("Failed to persist device layout preference:",e))}_renderNavigator(e){return(0,s.qy)`<esphome-device-navigator
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
      .errorCounts=${this._navErrorCounts(this._backendErrors)}
    ></esphome-device-navigator>`}_setYaml(e){this._yaml=e,"active"===this._errorHighlight&&(this._errorHighlight="edited")}_onYamlChange(e){this._setYaml(e.detail.value),this._retryPendingFieldLine()}_onYamlDiagnostics(e){if(e.detail.configuration!==this.id)return;"edited"===this._errorHighlight&&this._setHighlight(null,!1);let t=(0,g.cU)(this._yaml,e.detail.mapped);(t.length||this._backendErrors.length)&&(this._backendErrors=t)}_onYamlCursorLine(e){this._clearPendingFieldLine();let t=e.detail.path??[],i=(0,C.tO)(this._yaml,e.detail.line,t);if(!i)return;let a=(0,g.es)(t),o=(0,C.gU)(i);if(o===this._selectedSection&&i.fromLine===this._selectedFromLine){this._focusFieldPath=a;return}this._guardSectionSwitch(()=>{this._selectedSection=o,this._selectedFromLine=i.fromLine,this._focusFieldPath=a,this._clearBlockHighlight(),this._updateUrl()})}_focusedSection(){if(!this._selectedSection)return;let e=(0,C.MT)(this._yaml);return(void 0!==this._selectedFromLine?e.find(e=>e.fromLine===this._selectedFromLine):void 0)??e.find(e=>(0,C.gU)(e)===this._selectedSection)}_highlightFieldLine(e){let t=this._focusedSection(),i=t?(0,C.of)(this._yaml,t,e):null;return null!==i&&this._setHighlight({fromLine:i,toLine:i},!0),{section:t,found:null!==i}}_onFieldFocus(e){let t=this._focusedFieldPath=e.detail.path;if(!t.length)return;let{section:i,found:a}=this._highlightFieldLine(t);a?this._clearPendingFieldLine():(this._pendingFieldLine=!0,this._pendingFieldSection={section:this._selectedSection,fromLine:this._selectedFromLine},this._setHighlight(i?{fromLine:i.fromLine,toLine:i.toLine}:null,void 0!==i))}_retryPendingFieldLine(){if(this._pendingFieldLine&&this._focusedFieldPath?.length){if(this._pendingFieldSection?.section!==this._selectedSection||this._pendingFieldSection?.fromLine!==this._selectedFromLine)return void this._clearPendingFieldLine();this._highlightFieldLine(this._focusedFieldPath).found&&this._clearPendingFieldLine()}}_clearPendingFieldLine(){this._pendingFieldLine=!1,this._pendingFieldSection=void 0}_onYamlHighlight(e){this._setHighlight(e.detail.range,e.detail.scroll)}_onYamlUserEdit(){this._clearBlockHighlight()}_clearBlockHighlight(){this._highlightRange&&"none"===this._errorHighlight&&this._setHighlight(null,!1)}_setHighlight(e,t,i=!1){this._highlightRange=e,this._scrollToHighlight=t,this._errorHighlight=i&&null!==e?"active":"none"}_onYamlUpdated(e){this._setYaml(e.detail.yaml),this._savedYaml=e.detail.yaml}_onYamlDraft(e){this._setYaml(e.detail.yaml),this._retryPendingFieldLine()}_onSectionSelect(e){let{sectionKey:t,fromLine:i}=e.detail;if(t===this._selectedSection&&i===this._selectedFromLine){this._drawerOpen=!1;return}this._guardSectionSwitch(()=>{let e=this._selectedSection,a=this._selectedFromLine;null===t?this._sectionHistory=[]:null!==e&&(this._sectionHistory=[...this._sectionHistory,{key:e,fromLine:a}]),this._selectedSection=t,this._selectedFromLine=i,this._drawerOpen=!1,this._updateUrl()})}_guardSectionSwitch(e){this._activeSection?.flushPending(),e()}_readUrlParam(e,t){var i;return i=window.location.search,new URLSearchParams(i).get(e)??t}_readUrlLine(){let e=new URLSearchParams(window.location.search).get("line");if(!e)return;let t=Number(e);return Number.isNaN(t)?void 0:t}_readUrlSections(){let e;return(e=new URLSearchParams(window.location.search).get("open"))?e.split(",").map(Number).filter(e=>!Number.isNaN(e)):[]}_updateUrl(){var e,t,i;let a,o,r,s=(e=window.location.search,t=window.location.pathname,i={selectedSection:this._selectedSection,selectedFromLine:this._selectedFromLine,openSections:this._openSections},a=new URLSearchParams(e),i.selectedSection?(a.set("section",i.selectedSection),void 0!==i.selectedFromLine?a.set("line",String(i.selectedFromLine)):a.delete("line")):(a.delete("section"),a.delete("line")),(o=[...i.openSections]).length>0?a.set("open",o.join(",")):a.delete("open"),r=a.toString(),`${t}${r?`?${r}`:""}`);window.history.replaceState(window.history.state,"",s)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._devicesLoaded=!1,this._activeJobs=new Map,this.id="",this._justCreated=!1,this._layout="both",this._openSections=new Set(this._readUrlSections()),this._board=null,this._platformReady=!1,this._loadedBoardId=null,this._highlightRange=null,this._scrollToHighlight=!1,this._errorHighlight="none",this._selectedSection=this._readUrlParam("section",null),this._selectedFromLine=this._readUrlLine(),this._backendErrors=[],this._instanceBackendErrors=(0,l.A)(g.Oq),this._navErrorCounts=(0,l.A)(g.lt),this._pendingFieldLine=!1,this._sectionHistory=[],this._drawerOpen=!1,this._navCollapsed=!1,this._isMobile=window.matchMedia("(max-width: 900px)").matches,this._mql=window.matchMedia("(max-width: 900px)"),this._onMqlChange=e=>{this._isMobile=e.matches},this._yaml="",this._savedYaml="",this._saving=!1,this._activeSection=null,this._sectionDirty=!1,this._validationErrorCount=0,this._validationFirstLine=0,this._validationFirstCol=0,this._validationFirstMessage="",this._validationFirstFile="",this._onPostInstallShowLogs=(0,x.ei)(()=>this._logsDialog,()=>this._localize),this._installCtrl=this._createInstallController(),this._unsavedGuard=new z._,this._allowingLeave=!1,this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._confirmLeave=async()=>{this._activeSection?.flushPending();let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>(!this._isYamlDirty||!!await this._saveYaml())&&(this._allowingLeave=!0,!0)});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._activeSection?.flushPending(),this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._activeSection?.flushPending(),this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,f.cV)(`/device/${this.id}`)),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onKeydown=e=>{if("Escape"!==e.key||e.defaultPrevented)return;let t=e.composedPath()[0];if(!this._isTextEntry(t)){if(this._drawerOpen){e.preventDefault(),this._drawerOpen=!1;return}e.preventDefault(),window.history.back()}},this._dismissJustCreated=()=>{this._justCreated=!1},this._onChangeBoard=async e=>{let t=e.detail?.boardId,i=this._device;if(t&&i&&t!==i.board_id){if(this._isDirty)return void(0,d.UG)(this._localize("device.change_board_unsaved"));try{await this._api.updateDevice({configuration:i.configuration,board_id:t}),await this._loadYaml(),(0,d.VX)(this._localize("device.change_board_success"))}catch(e){console.error("Failed to change board:",e),(0,d.UG)(this._localize("device.change_board_error"))}}},this._pendingValidationResolve=null,this._saveYaml=async()=>{if(this._saving||null!==this._pendingValidationResolve)return!1;this._saving=!0;try{if(await this._activeSection?.flushPending(),!this._isYamlDirty)return!0;if(this.id)try{let e=(0,E.mL)(this.id,this._yaml)??await this._api.validateYaml(this.id,this._yaml),t=(0,S.tu)(e,this._yaml,this._localize);if(t.count>0){this._validationErrorCount=t.count,this._validationFirstLine=t.first?.line??0,this._validationFirstCol=t.first?.col??0,this._validationFirstMessage=t.first?.message??"";let e=t.first?.file??null;return this._validationFirstFile=e&&this.id&&!(0,S.lg)(e,this.id)?(0,S.P8)(e):"",new Promise(e=>{this._pendingValidationResolve=e,this._yamlValidationDialog.open()})}}catch(e){console.debug("[save-yaml] validate_yaml failed, saving anyway:",e)}return await this._doSaveYaml()}finally{this._saving=!1}},this._doSaveYaml=async()=>{let e=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let t=!0;try{await this._api.updateConfig(this.id,this._yaml)}catch(i){(i instanceof Error?i.message:"").includes("timed out")||(t=!1,this._savedYaml=e,console.error("Failed to save YAML:",i))}finally{this._saving=!1}t&&"none"!==this._errorHighlight&&this._setHighlight(null,!1);let i=t?"device.yaml_saved":"device.yaml_save_error";return(t?d.VX:d.UG)(this._localize(i)),t},this._onValidationSaveAnyway=async()=>{let e=await this._doSaveYaml();this._resolveValidationPrompt(e)},this._onValidationGoTo=e=>{this._jumpToErrorLine(e.detail.line),this._resolveValidationPrompt(!1)},this._onEditorGoToLine=e=>{this._jumpToErrorLine(e.detail.line)},this._onValidationCancel=()=>{this._resolveValidationPrompt(!1)},this._onValidateClick=()=>{this._device&&(this._commandDialog.configuration=this._device.configuration,this._commandDialog.name=this._device.friendly_name||this._device.name,this._commandDialog.open("validate"))},this._installAfterSave=async e=>{let t;try{t=await this._saveYaml()}catch(e){console.error("Failed to save before install:",e),(0,d.UG)(this._localize("device.yaml_save_error"));return}t&&e()},this._saveThenInstall=()=>this._installAfterSave(this._installCtrl.onInstall),this._saveThenUpdate=()=>this._installAfterSave(this._installCtrl.onUpdate),this._onCleanBuild=e=>{let t=e.detail;this._commandDialog.configuration=t.configuration,this._commandDialog.name=t.friendly_name||t.name,this._commandDialog.open("clean")},this._onRequestOpenEditor=e=>{e.stopPropagation(),e.detail.configuration!==this._device?.configuration&&(0,$.oo)(`/device/${encodeURIComponent(e.detail.configuration)}`)},this._onBack=()=>{this._guardSectionSwitch(()=>{let e=this._sectionHistory.length?this._sectionHistory[this._sectionHistory.length-1]:null;e?(this._sectionHistory=this._sectionHistory.slice(0,-1),this._selectedSection=e.key,this._selectedFromLine=e.fromLine):(this._selectedSection=null,this._selectedFromLine=void 0),this._setHighlight(null,!1),this._updateUrl()})},this._onNavExpand=()=>{if(this._isMobile){this._drawerOpen=!0;return}this._navCollapsed=!1,this._api.updatePreferences({navigator_visible:!0}).catch(()=>{})},this._onNavCollapse=()=>{if(this._isMobile){this._drawerOpen=!1;return}this._navCollapsed=!0,this._api.updatePreferences({navigator_visible:!1}).catch(()=>{})},this._onSectionMount=e=>{this._activeSection=e.detail.node,this._sectionDirty=e.detail.node.dirty},this._onSectionUnmount=e=>{this._activeSection===e.detail.node&&(this._activeSection=null,this._sectionDirty=!1)},this._onSectionDirtyChange=e=>{this._sectionDirty=e.detail.dirty}}}rP.styles=[v.G,A],rM([(0,o.Fg)({context:m.$F,subscribe:!0}),(0,n.wk)()],rP.prototype,"_localize",void 0),rM([(0,o.Fg)({context:m.xJ,subscribe:!0}),(0,n.wk)()],rP.prototype,"_devices",void 0),rM([(0,o.Fg)({context:m.UL,subscribe:!0}),(0,n.wk)()],rP.prototype,"_devicesLoaded",void 0),rM([(0,o.Fg)({context:m.Ie})],rP.prototype,"_api",void 0),rM([(0,o.Fg)({context:m.EM,subscribe:!0}),(0,n.wk)()],rP.prototype,"_activeJobs",void 0),rM([(0,n.MZ)()],rP.prototype,"id",void 0),rM([(0,n.wk)()],rP.prototype,"_justCreated",void 0),rM([(0,n.wk)()],rP.prototype,"_layout",void 0),rM([(0,n.wk)()],rP.prototype,"_openSections",void 0),rM([(0,n.wk)()],rP.prototype,"_board",void 0),rM([(0,n.wk)()],rP.prototype,"_platformReady",void 0),rM([(0,n.wk)()],rP.prototype,"_highlightRange",void 0),rM([(0,n.wk)()],rP.prototype,"_scrollToHighlight",void 0),rM([(0,n.wk)()],rP.prototype,"_selectedSection",void 0),rM([(0,n.wk)()],rP.prototype,"_selectedFromLine",void 0),rM([(0,n.wk)()],rP.prototype,"_focusFieldPath",void 0),rM([(0,n.wk)()],rP.prototype,"_backendErrors",void 0),rM([(0,n.wk)()],rP.prototype,"_sectionHistory",void 0),rM([(0,n.wk)()],rP.prototype,"_drawerOpen",void 0),rM([(0,n.wk)()],rP.prototype,"_navCollapsed",void 0),rM([(0,n.wk)()],rP.prototype,"_isMobile",void 0),rM([(0,n.wk)()],rP.prototype,"_yaml",void 0),rM([(0,n.wk)()],rP.prototype,"_savedYaml",void 0),rM([(0,n.wk)()],rP.prototype,"_saving",void 0),rM([(0,n.P)("esphome-unsaved-changes-dialog")],rP.prototype,"_unsavedDialog",void 0),rM([(0,n.wk)()],rP.prototype,"_sectionDirty",void 0),rM([(0,n.P)("esphome-command-dialog")],rP.prototype,"_commandDialog",void 0),rM([(0,n.P)("esphome-firmware-install-dialog")],rP.prototype,"_firmwareDialog",void 0),rM([(0,n.P)("esphome-logs-dialog")],rP.prototype,"_logsDialog",void 0),rM([(0,n.P)("esphome-yaml-validation-dialog")],rP.prototype,"_yamlValidationDialog",void 0),rM([(0,n.wk)()],rP.prototype,"_validationErrorCount",void 0),rM([(0,n.wk)()],rP.prototype,"_validationFirstLine",void 0),rM([(0,n.wk)()],rP.prototype,"_validationFirstCol",void 0),rM([(0,n.wk)()],rP.prototype,"_validationFirstMessage",void 0),rM([(0,n.wk)()],rP.prototype,"_validationFirstFile",void 0),rP=rM([(0,n.EM)("esphome-page-device")],rP)}}]);
//# sourceMappingURL=37.fa66a6310e09dcc4.js.map