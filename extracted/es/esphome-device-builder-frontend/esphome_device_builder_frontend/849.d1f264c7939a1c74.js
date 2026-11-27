"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[849],{1682(e,a,t){var i=t(9104),o=t(5077),r=t(9356),s=t(1556),l=t(1529),n=t(918),c=t(6578),p=t(4095),d=t(3626);function h(e,a,t,i){var o,r=arguments.length,s=r<3?a:null===i?i=Object.getOwnPropertyDescriptor(a,t):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,a,t,i);else for(var l=e.length-1;l>=0;l--)(o=e[l])&&(s=(r<3?o(s):r>3?o(a,t,s):o(a,t))||s);return r>3&&s&&Object.defineProperty(a,t,s),s}t(8768);class g extends o.WF{async open(e){let a,t=++this._opening;try{a=await this._api.getFileUsage(e)}catch(e){t===this._opening&&(0,d.k)(this._localize,"packages.usage_failed",e);return}t===this._opening&&(this._usage=a,this._path=e,await this.updateComplete,t===this._opening&&this._confirm?.open())}render(){return(0,o.qy)`
      <esphome-confirm-dialog
        ?destructive=${!0}
        heading=${this._localize("packages.delete_title",{path:this._path})}
        confirm-label=${this._localize("packages.delete")}
        @confirm=${this._delete}
      >
        <div slot="body">
          ${(0,p.Ko)(this._usage,{localize:this._localize,devices:this._devices,usedKey:"packages.delete_used_message",unusedKey:"packages.delete_unused_message",open:e=>{this._confirm?.close(),(0,l.oo)(e)}})}
        </div>
      </esphome-confirm-dialog>
    `}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._path="",this._usage=p.yJ,this._opening=0,this._delete=async()=>{let e=this._path;try{await this._api.deleteFile(e)}catch(e){(0,d.k)(this._localize,"packages.delete_failed",e);return}(0,n.VX)(this._localize("packages.deleted",{path:e})),this.dispatchEvent(new CustomEvent("file-deleted",{detail:{path:e},bubbles:!0}))}}}g.styles=[c.F1,p.yT,(0,o.AH)`
      :host {
        display: contents;
      }
    `],h([(0,i.Fg)({context:s.$F,subscribe:!0}),(0,r.wk)()],g.prototype,"_localize",void 0),h([(0,i.Fg)({context:s.Ie})],g.prototype,"_api",void 0),h([(0,i.Fg)({context:s.xJ,subscribe:!0}),(0,r.wk)()],g.prototype,"_devices",void 0),h([(0,r.wk)()],g.prototype,"_path",void 0),h([(0,r.wk)()],g.prototype,"_usage",void 0),h([(0,r.P)("esphome-confirm-dialog")],g.prototype,"_confirm",void 0),h([(0,r.EM)("esphome-delete-file-dialog")],g)},2207(e,a,t){var i=t(9104),o=t(5077),r=t(9356),s=t(1556),l=t(1404),n=t(6848),c=t(3140),p=t(325),d=t(1108),h=t(6578),g=t(4095),_=t(3626);function m(e,a,t,i){var o,r=arguments.length,s=r<3?a:null===i?i=Object.getOwnPropertyDescriptor(a,t):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,a,t,i);else for(var l=e.length-1;l>=0;l--)(o=e[l])&&(s=(r<3?o(s):r>3?o(a,t,s):o(a,t))||s);return r>3&&s&&Object.defineProperty(a,t,s),s}t(1813),t(9835);class u extends o.WF{async open(e){let a,t=++this._opening;try{a=await this._api.getFileUsage(e)}catch(e){t===this._opening&&(0,_.k)(this._localize,"packages.usage_failed",e);return}t===this._opening&&(this._path=e,this._name=(0,d.bV)(e),this._usage=a,this._skip=new Set,this._dialog.open=!0)}get _newPath(){return`${(0,d.yS)(this._path)}/${this._name.trim()}`}get problem(){return this._name.includes("/")?"packages.rename_name_only":this._newPath===this._path?"packages.rename_same":(0,d.DW)(this._newPath)}render(){let e=this._name.trim()?this.problem:null;return(0,o.qy)`
      <esphome-base-dialog
        ?open=${this._dialog.open}
        .label=${this._localize("packages.rename_title",{path:this._path})}
        .confirmOnEnter=${this._confirm}
        @request-close=${this._dialog.onRequestClose}
      >
        <div class="name">
          <span class="folder">${(0,d.yS)(this._path)}/</span>
          <input
            type="text"
            autofocus
            autocomplete="off"
            spellcheck="false"
            aria-label=${this._localize("packages.rename_label")}
            .value=${this._name}
            @input=${e=>this._name=e.currentTarget.value}
          />
        </div>
        ${e?(0,o.qy)`<p class="problem" role="alert">${this._localize(e)}</p>`:o.s6}
        ${this._renderReferrers()}
        <div class="actions">
          <button class="btn btn--cancel" @click=${this._close}>
            ${this._localize("layout.cancel")}
          </button>
          <button
            class="btn btn--primary"
            ?disabled=${!this._name.trim()||null!==this.problem}
            @click=${this._confirm}
          >
            ${this._localize("packages.rename")}
          </button>
        </div>
      </esphome-base-dialog>
    `}_renderReferrers(){let{referenced_by:e,rewritable:a}=this._usage,t=e.filter(e=>!a.includes(e));return(0,o.qy)`<p class="usage-message">
        ${a.length>0?this._localize("packages.rename_referrers",{count:a.length}):this._localize("packages.rename_no_referrers")}
      </p>
      ${a.length>0?(0,o.qy)`<ul class="link-list">
              ${a.map(e=>{let a=this._referrerItem(e);return(0,o.qy)`<li class="link-row check-row">
                  <wa-checkbox
                    .checked=${!this._skip.has(e)}
                    @change=${a=>this._toggle(e,a.target.checked)}
                    ><span class="link-label">${a.label}</span></wa-checkbox
                  >
                  ${a.detail?(0,o.qy)`<span class="link-detail">${a.detail}</span>`:o.s6}
                </li>`})}
            </ul>`:o.s6}
      ${t.length>0?(0,o.qy)`<p class="usage-message">
                ${this._localize("packages.rename_manual",{count:t.length})}
              </p>
              ${(0,h.tM)(t.map(e=>({...this._referrerItem(e),url:null})),()=>void 0)}`:o.s6}
      ${(0,g.Cg)(this._usage,this._localize)}`}_referrerItem(e){return(0,d.ch)(e)?{label:e,detail:this._localize("packages.rename_archived")}:""===(0,d.yS)(e)?(0,h.zb)([e],this._devices)[0]:{label:e}}_toggle(e,a){let t=new Set(this._skip);a?t.delete(e):t.add(e),this._skip=t}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._path="",this._name="",this._usage=g.yJ,this._skip=new Set,this._dialog=new p.T(this),this._opening=0,this._close=()=>{this._dialog.open=!1},this._confirm=()=>{this._dialog.open&&this._name.trim()&&null===this.problem&&(this._close(),this.dispatchEvent(new CustomEvent("rename-file",{detail:{path:this._path,newPath:this._newPath,skip:[...this._skip]},bubbles:!0})))}}}u.styles=[c.G9,n.dC,l.V,l.E,h.F1,g.yT,(0,o.AH)`
      esphome-base-dialog {
        --width: 520px;
      }
      esphome-base-dialog::part(body) {
        padding: 0 var(--wa-space-l) var(--wa-space-l);
      }
      .name {
        display: flex;
        align-items: center;
        gap: 2px;
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
      }
      .folder {
        color: var(--wa-color-text-quiet);
        white-space: nowrap;
      }
      .name input {
        flex: 1;
        min-width: 0;
        box-sizing: border-box;
        padding: 8px 10px;
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-m);
        background: var(--wa-color-surface-default);
        color: var(--wa-color-text-normal);
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-s);
      }
      .problem {
        margin: 6px 0 0;
        font-size: var(--wa-font-size-xs);
        color: var(--esphome-error);
      }
      .check-row {
        align-items: center;
      }
      .check-row wa-checkbox {
        flex: 1;
        min-width: 0;
      }
    `],m([(0,i.Fg)({context:s.$F,subscribe:!0}),(0,r.wk)()],u.prototype,"_localize",void 0),m([(0,i.Fg)({context:s.Ie})],u.prototype,"_api",void 0),m([(0,i.Fg)({context:s.xJ,subscribe:!0}),(0,r.wk)()],u.prototype,"_devices",void 0),m([(0,r.wk)()],u.prototype,"_path",void 0),m([(0,r.wk)()],u.prototype,"_name",void 0),m([(0,r.wk)()],u.prototype,"_usage",void 0),m([(0,r.wk)()],u.prototype,"_skip",void 0),m([(0,r.EM)("esphome-rename-file-dialog")],u)},6387(e,a,t){t.r(a);var i=t(9104),o=t(289),r=t(5077),s=t(9356),l=t(4342),n=t(3835),c=t(3626),p=t(1556),d=t(4835),h=t(3140),g=t(1108),_=t(1529),m=t(1093),u=t(3854);function w(e,a,t,i){var o,r=arguments.length,s=r<3?a:null===i?i=Object.getOwnPropertyDescriptor(a,t):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,a,t,i);else for(var l=e.length-1;l>=0;l--)(o=e[l])&&(s=(r<3?o(s):r>3?o(a,t,s):o(a,t))||s);return r>3&&s&&Object.defineProperty(a,t,s),s}t(9577),t(9218),t(2522),t(1682),t(2101),t(2207),(0,m.C)({delete:o.mdiDelete,devices:o.mdiDevices,"package-variant-closed":o.mdiPackageVariantClosed,plus:o.mdiPlus,"rename-outline":o.mdiRenameOutline});let f=e=>`# ${e}
# Shared configuration. Include it from a device with:
#   packages:
#     shared: !include ${e}
`;class b extends r.WF{connectedCallback(){super.connectedCallback(),this._wasConnected=this._apiConnected,this._reload()}updated(){this._apiConnected&&!this._wasConnected&&this._reload(),this._wasConnected=this._apiConnected}render(){let e=this._newPath.trim()?(0,g.DW)(this._newPath):null;return(0,r.qy)`
      <div class="page">
        <div>
          <h1>${this._localize("packages.title")}</h1>
          <p class="desc">${this._localize("packages.desc")}</p>
        </div>
        <form class="create" @submit=${this._create}>
          <input
            type="text"
            autocomplete="off"
            spellcheck="false"
            class="path"
            aria-label=${this._localize("packages.new_label")}
            placeholder=${this._localize("packages.new_placeholder")}
            .value=${this._newPath}
            @input=${e=>this._newPath=e.currentTarget.value}
          />
          <button
            type="submit"
            class="primary"
            ?disabled=${this._creating||!this._newPath.trim()||null!==e}
          >
            <wa-icon library="mdi" name="plus"></wa-icon>
            ${this._localize("packages.new")}
          </button>
          ${e?(0,r.qy)`<p class="problem" role="alert">${this._localize(e)}</p>`:r.s6}
        </form>
        ${(0,u.C)({loading:"loading"===this._state,loadingMessage:this._localize("packages.loading"),loadingLead:(0,r.qy)`<wa-spinner></wa-spinner>`,error:"error"===this._state?this._localize("packages.load_failed"):null,errorActions:()=>(0,r.qy)`<wa-button size="small" @click=${this._reload}>
              ${this._localize("command.retry")}
            </wa-button>`,content:()=>this._renderList()})}
      </div>
      <esphome-delete-file-dialog
        @file-deleted=${this._reload}
      ></esphome-delete-file-dialog>
      <esphome-file-list-dialog></esphome-file-list-dialog>
      <esphome-rename-file-dialog
        @rename-file=${this._rename}
      ></esphome-rename-file-dialog>
    `}_renderList(){return 0===this._paths.length?(0,r.qy)`<div class="empty">
        <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
        <p>${this._localize("packages.empty")}</p>
      </div>`:(0,r.qy)`${[...(0,g.Je)(this._paths)].map(([e,a])=>(0,r.qy)`<section class="folder" aria-label=${e}>
          <h2 class="path">${e}/</h2>
          ${a.map(e=>(0,r.qy)`<div class="file">
                <button
                  type="button"
                  class="file-name path"
                  @click=${()=>(0,_.oo)((0,g.zI)(e))}
                >
                  ${(0,g.bV)(e)}
                </button>
                <button
                  type="button"
                  class="row-action"
                  @click=${()=>this._usageDialog?.showUsage(e)}
                >
                  <wa-icon library="mdi" name="devices"></wa-icon>
                  ${this._localize("packages.show_usage")}
                </button>
                <button
                  type="button"
                  class="row-action row-action--accent"
                  aria-label=${this._localize("packages.rename_named",{path:e})}
                  title=${this._localize("packages.rename")}
                  @click=${()=>this._renameDialog?.open(e)}
                >
                  <wa-icon library="mdi" name="rename-outline"></wa-icon>
                </button>
                <button
                  type="button"
                  class="row-action row-action--danger"
                  aria-label=${this._localize("packages.delete_named",{path:e})}
                  title=${this._localize("packages.delete")}
                  @click=${()=>this._deleteDialog?.open(e)}
                >
                  <wa-icon library="mdi" name="delete"></wa-icon>
                </button>
              </div>`)}
        </section>`)}`}constructor(...e){super(...e),this._localize=e=>e,this._apiConnected=!1,this._state="loading",this._paths=[],this._newPath="",this._creating=!1,this._wasConnected=!1,this._reloading=0,this._reload=async()=>{let e=++this._reloading;"ready"!==this._state&&(this._state="loading");try{await this._api.ready;let a=(await this._api.listPackages()).map(e=>e.path);if(e!==this._reloading)return;this._paths=a,this._state="ready"}catch(a){if(e!==this._reloading)return;console.error("Failed to list packages:",a),this._state="error"}},this._rename=async e=>{await (0,c.H)(this._api,this._localize,e.detail),this._reload()},this._create=async e=>{e.preventDefault();let a=this._newPath.trim();if(null===(0,g.DW)(a)){this._creating=!0;try{await this._api.createFile(a,f(a))}catch(a){let e=a instanceof l.LG&&a.errorCode===n.O.ALREADY_EXISTS?"packages.already_exists":"packages.create_failed";(0,c.k)(this._localize,e,a);return}finally{this._creating=!1}this._newPath="",this.isConnected&&(0,_.oo)((0,g.zI)(a))}}}}b.styles=[h.G9,d.I,(0,r.AH)`
      .page {
        max-width: 960px;
        margin: 0 auto;
        padding: var(--wa-space-l) var(--content-gutter);
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-l);
      }
      h1 {
        margin: 0 0 2px;
        font-size: var(--wa-font-size-l);
        font-weight: var(--wa-font-weight-bold);
      }
      .desc {
        margin: 0;
        font-size: var(--wa-font-size-s);
        color: var(--wa-color-text-quiet);
      }
      code,
      .path {
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      }
      .create {
        display: flex;
        flex-wrap: wrap;
        gap: var(--wa-space-s);
        align-items: center;
      }
      .create input {
        flex: 1;
        min-width: 220px;
        padding: 8px 10px;
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-m);
        background: var(--wa-color-surface-default);
        color: var(--wa-color-text-normal);
        font: inherit;
        font-size: var(--wa-font-size-s);
      }
      .create .problem {
        flex-basis: 100%;
        margin: 0;
        font-size: var(--wa-font-size-xs);
        color: var(--esphome-error);
      }
      .primary,
      .row-action {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border-radius: var(--wa-border-radius-m);
        font: inherit;
        font-size: var(--wa-font-size-xs);
        font-weight: var(--wa-font-weight-bold);
        cursor: pointer;
      }
      .primary {
        padding: var(--esphome-button-padding);
        border: none;
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
      }
      .primary:disabled {
        opacity: 0.4;
        cursor: not-allowed;
      }
      .folder {
        background: var(--wa-color-surface-default);
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-l);
        overflow: hidden;
      }
      .folder h2 {
        margin: 0;
        padding: 10px 16px;
        font-size: var(--wa-font-size-s);
        background: var(--wa-color-surface-lowered);
      }
      .file {
        display: flex;
        align-items: center;
        gap: var(--wa-space-s);
        padding: 8px 16px;
        border-top: var(--wa-border-width-s) solid var(--wa-color-surface-border);
      }
      .file-name {
        flex: 1;
        border: none;
        background: none;
        padding: 0;
        text-align: left;
        font: inherit;
        font-size: var(--wa-font-size-s);
        color: var(--esphome-primary);
        cursor: pointer;
        overflow-wrap: anywhere;
      }
      .file-name:hover {
        text-decoration: underline;
      }
      .row-action {
        padding: 4px 8px;
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        background: transparent;
        color: var(--wa-color-text-normal);
      }
      .row-action:hover {
        background: var(--wa-color-surface-lowered);
      }
      .row-action--accent {
        color: var(--esphome-primary);
      }
      .row-action--accent:hover {
        background: var(--esphome-tint);
        border-color: var(--esphome-tint-border);
      }
      .row-action--danger {
        color: var(--esphome-error);
      }
      .row-action--danger:hover {
        background: color-mix(in srgb, var(--esphome-error), transparent 92%);
      }
      .row-action wa-icon,
      .primary wa-icon {
        font-size: 16px;
      }
      .empty {
        padding: var(--wa-space-l);
        text-align: center;
        color: var(--wa-color-text-quiet);
        font-size: var(--wa-font-size-s);
      }
      .empty wa-icon {
        font-size: 40px;
      }
    `],w([(0,i.Fg)({context:p.$F,subscribe:!0}),(0,s.wk)()],b.prototype,"_localize",void 0),w([(0,i.Fg)({context:p.Ie})],b.prototype,"_api",void 0),w([(0,i.Fg)({context:p.Lh,subscribe:!0}),(0,s.wk)()],b.prototype,"_apiConnected",void 0),w([(0,s.wk)()],b.prototype,"_state",void 0),w([(0,s.wk)()],b.prototype,"_paths",void 0),w([(0,s.wk)()],b.prototype,"_newPath",void 0),w([(0,s.wk)()],b.prototype,"_creating",void 0),w([(0,s.P)("esphome-delete-file-dialog")],b.prototype,"_deleteDialog",void 0),w([(0,s.P)("esphome-file-list-dialog")],b.prototype,"_usageDialog",void 0),w([(0,s.P)("esphome-rename-file-dialog")],b.prototype,"_renameDialog",void 0),b=w([(0,s.EM)("esphome-page-packages")],b),t.d(a,{ESPHomePagePackages:()=>b},{newFileTemplate:f})},4835(e,a,t){var i=t(5077);let o=(0,i.AH)`
  .message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--wa-space-m);
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    text-align: center;
  }

  .message wa-spinner {
    font-size: 32px;
  }

  .message.error {
    color: var(--wa-color-danger-text-normal);
  }
`;t.d(a,{},{I:o})}}]);
//# sourceMappingURL=849.d1f264c7939a1c74.js.map