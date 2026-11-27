"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[76],{1682(e,t,i){var a=i(9104),o=i(5077),s=i(9356),l=i(1556),r=i(1529),n=i(918),h=i(6578),d=i(4095),c=i(3626);function p(e,t,i,a){var o,s=arguments.length,l=s<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,i,a);else for(var r=e.length-1;r>=0;r--)(o=e[r])&&(l=(s<3?o(l):s>3?o(t,i,l):o(t,i))||l);return s>3&&l&&Object.defineProperty(t,i,l),l}i(8768);class g extends o.WF{async open(e){let t,i=++this._opening;try{t=await this._api.getFileUsage(e)}catch(e){i===this._opening&&(0,c.k)(this._localize,"packages.usage_failed",e);return}i===this._opening&&(this._usage=t,this._path=e,await this.updateComplete,i===this._opening&&this._confirm?.open())}render(){return(0,o.qy)`
      <esphome-confirm-dialog
        ?destructive=${!0}
        heading=${this._localize("packages.delete_title",{path:this._path})}
        confirm-label=${this._localize("packages.delete")}
        @confirm=${this._delete}
      >
        <div slot="body">
          ${(0,d.Ko)(this._usage,{localize:this._localize,devices:this._devices,usedKey:"packages.delete_used_message",unusedKey:"packages.delete_unused_message",open:e=>{this._confirm?.close(),(0,r.oo)(e)}})}
        </div>
      </esphome-confirm-dialog>
    `}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._path="",this._usage=d.yJ,this._opening=0,this._delete=async()=>{let e=this._path;try{await this._api.deleteFile(e)}catch(e){(0,c.k)(this._localize,"packages.delete_failed",e);return}(0,n.VX)(this._localize("packages.deleted",{path:e})),this.dispatchEvent(new CustomEvent("file-deleted",{detail:{path:e},bubbles:!0}))}}}g.styles=[h.F1,d.yT,(0,o.AH)`
      :host {
        display: contents;
      }
    `],p([(0,a.Fg)({context:l.$F,subscribe:!0}),(0,s.wk)()],g.prototype,"_localize",void 0),p([(0,a.Fg)({context:l.Ie})],g.prototype,"_api",void 0),p([(0,a.Fg)({context:l.xJ,subscribe:!0}),(0,s.wk)()],g.prototype,"_devices",void 0),p([(0,s.wk)()],g.prototype,"_path",void 0),p([(0,s.wk)()],g.prototype,"_usage",void 0),p([(0,s.P)("esphome-confirm-dialog")],g.prototype,"_confirm",void 0),p([(0,s.EM)("esphome-delete-file-dialog")],g)},2207(e,t,i){var a=i(9104),o=i(5077),s=i(9356),l=i(1556),r=i(1404),n=i(6848),h=i(3140),d=i(325),c=i(1108),p=i(6578),g=i(4095),_=i(3626);function m(e,t,i,a){var o,s=arguments.length,l=s<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,i,a);else for(var r=e.length-1;r>=0;r--)(o=e[r])&&(l=(s<3?o(l):s>3?o(t,i,l):o(t,i))||l);return s>3&&l&&Object.defineProperty(t,i,l),l}i(1813),i(9835);class u extends o.WF{async open(e){let t,i=++this._opening;try{t=await this._api.getFileUsage(e)}catch(e){i===this._opening&&(0,_.k)(this._localize,"packages.usage_failed",e);return}i===this._opening&&(this._path=e,this._name=(0,c.bV)(e),this._usage=t,this._skip=new Set,this._dialog.open=!0)}get _newPath(){return`${(0,c.yS)(this._path)}/${this._name.trim()}`}get problem(){return this._name.includes("/")?"packages.rename_name_only":this._newPath===this._path?"packages.rename_same":(0,c.DW)(this._newPath)}render(){let e=this._name.trim()?this.problem:null;return(0,o.qy)`
      <esphome-base-dialog
        ?open=${this._dialog.open}
        .label=${this._localize("packages.rename_title",{path:this._path})}
        .confirmOnEnter=${this._confirm}
        @request-close=${this._dialog.onRequestClose}
      >
        <div class="name">
          <span class="folder">${(0,c.yS)(this._path)}/</span>
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
    `}_renderReferrers(){let{referenced_by:e,rewritable:t}=this._usage,i=e.filter(e=>!t.includes(e));return(0,o.qy)`<p class="usage-message">
        ${t.length>0?this._localize("packages.rename_referrers",{count:t.length}):this._localize("packages.rename_no_referrers")}
      </p>
      ${t.length>0?(0,o.qy)`<ul class="link-list">
              ${t.map(e=>{let t=this._referrerItem(e);return(0,o.qy)`<li class="link-row check-row">
                  <wa-checkbox
                    .checked=${!this._skip.has(e)}
                    @change=${t=>this._toggle(e,t.target.checked)}
                    ><span class="link-label">${t.label}</span></wa-checkbox
                  >
                  ${t.detail?(0,o.qy)`<span class="link-detail">${t.detail}</span>`:o.s6}
                </li>`})}
            </ul>`:o.s6}
      ${i.length>0?(0,o.qy)`<p class="usage-message">
                ${this._localize("packages.rename_manual",{count:i.length})}
              </p>
              ${(0,p.tM)(i.map(e=>({...this._referrerItem(e),url:null})),()=>void 0)}`:o.s6}
      ${(0,g.Cg)(this._usage,this._localize)}`}_referrerItem(e){return(0,c.ch)(e)?{label:e,detail:this._localize("packages.rename_archived")}:""===(0,c.yS)(e)?(0,p.zb)([e],this._devices)[0]:{label:e}}_toggle(e,t){let i=new Set(this._skip);t?i.delete(e):i.add(e),this._skip=i}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._path="",this._name="",this._usage=g.yJ,this._skip=new Set,this._dialog=new d.T(this),this._opening=0,this._close=()=>{this._dialog.open=!1},this._confirm=()=>{this._dialog.open&&this._name.trim()&&null===this.problem&&(this._close(),this.dispatchEvent(new CustomEvent("rename-file",{detail:{path:this._path,newPath:this._newPath,skip:[...this._skip]},bubbles:!0})))}}}u.styles=[h.G9,n.dC,r.V,r.E,p.F1,g.yT,(0,o.AH)`
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
    `],m([(0,a.Fg)({context:l.$F,subscribe:!0}),(0,s.wk)()],u.prototype,"_localize",void 0),m([(0,a.Fg)({context:l.Ie})],u.prototype,"_api",void 0),m([(0,a.Fg)({context:l.xJ,subscribe:!0}),(0,s.wk)()],u.prototype,"_devices",void 0),m([(0,s.wk)()],u.prototype,"_path",void 0),m([(0,s.wk)()],u.prototype,"_name",void 0),m([(0,s.wk)()],u.prototype,"_usage",void 0),m([(0,s.wk)()],u.prototype,"_skip",void 0),m([(0,s.EM)("esphome-rename-file-dialog")],u)},3423(e,t,i){i.r(t);var a=i(9104),o=i(289),s=i(5077),l=i(9356),r=i(4342),n=i(3835),h=i(3626),d=i(1556),c=i(4835),p=i(3140),g=i(2097),_=i(7051),m=i(1108),u=i(1529),v=i(918),f=i(1093),b=i(3854),w=i(4818),y=i(9317),k=i(5858);function x(e,t,i,a){var o,s=arguments.length,l=s<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,i,a);else for(var r=e.length-1;r>=0;r--)(o=e[r])&&(l=(s<3?o(l):s>3?o(t,i,l):o(t,i))||l);return s>3&&l&&Object.defineProperty(t,i,l),l}i(9577),i(9218),i(2522),i(8768),i(8297),i(1682),i(2101),i(2207),i(9786),i(9931),(0,f.C)({"content-save":o.mdiContentSave,delete:o.mdiDelete,devices:o.mdiDevices,menu:o.mdiMenu,"rename-outline":o.mdiRenameOutline});class $ extends s.WF{connectedCallback(){super.connectedCallback(),window.addEventListener("beforeunload",this._onBeforeUnload)}disconnectedCallback(){window.removeEventListener("beforeunload",this._onBeforeUnload),this._unsavedGuard.cancelPending(),super.disconnectedCallback()}willUpdate(e){e.has("path")&&this.path&&(this._reloadDialog?.close(),this._yaml=this._savedYaml="",this._selectedSection=null,this._selectedFromLine=void 0,this._highlight=null,this._scrollToHighlight=!1,this._load.start())}get _showNav(){return"ready"===this._load.state&&!this._navCollapsed}get _isDirty(){return this._yaml!==this._savedYaml}get _isPackage(){return""!==(0,m.yS)(this.path)}render(){return(0,s.qy)`
      <div class="page">
        <div class="page-header">
          <div class="page-title">
            <h1>${(0,m.bV)(this.path)}</h1>
            <p>${this.path}</p>
          </div>
          ${this._navCollapsed?(0,s.qy)`<button
                  type="button"
                  class="header-button"
                  @click=${()=>this._navCollapsed=!1}
                >
                  <wa-icon library="mdi" name="menu"></wa-icon>
                  ${this._localize("device.show_navigator")}
                </button>`:null}
          <button type="button" class="header-button" @click=${this._showUsage}>
            <wa-icon library="mdi" name="devices"></wa-icon>
            ${this._localize("packages.show_usage")}
          </button>
          ${this._isPackage?(0,s.qy)`<button
                    type="button"
                    class="header-button header-button--accent"
                    ?disabled=${this._isDirty}
                    title=${this._isDirty?this._localize("packages.rename_save_first"):""}
                    @click=${this._openRename}
                  >
                    <wa-icon library="mdi" name="rename-outline"></wa-icon>
                    ${this._localize("packages.rename")}
                  </button>
                  <button
                    type="button"
                    class="header-button header-button--danger"
                    @click=${this._confirmDelete}
                  >
                    <wa-icon library="mdi" name="delete"></wa-icon>
                    ${this._localize("packages.delete")}
                  </button>`:null}
        </div>
        <div class="body ${this._showNav?"":"no-nav"}">
          ${this._showNav?(0,s.qy)`<esphome-device-navigator
                  readonly
                  platformReady
                  .yaml=${this._yaml}
                  .configuration=${this.path}
                  .selectedKey=${this._selectedSection}
                  .selectedFromLine=${this._selectedFromLine}
                  .openSections=${this._openSections}
                  @section-toggle=${e=>this._openSections=this._openSections.has(e.detail.index)?new Set:new Set([e.detail.index])}
                  @section-reveal=${e=>this._openSections=new Set([e.detail.index])}
                  @section-select=${this._onSectionSelect}
                  @yaml-highlight=${this._onYamlHighlight}
                  @nav-collapse=${()=>this._navCollapsed=!0}
                ></esphome-device-navigator>`:null}
          <div class="editor-card">
            ${(0,b.C)({loading:"loading"===this._load.state,loadingMessage:this._localize("file.loading"),loadingLead:(0,s.qy)`<wa-spinner></wa-spinner>`,error:"error"===this._load.state?this._localize("file.load_failed"):"missing"===this._load.state?this._localize("file.not_found",{path:this.path}):null,errorActions:()=>"error"===this._load.state?(0,s.qy)`<wa-button size="small" @click=${this._load.retry}>
                      ${this._localize("command.retry")}
                    </wa-button>`:(0,s.qy)`<wa-button size="small" @click=${()=>(0,u.oo)("/packages")}>
                      ${this._localize("packages.title")}
                    </wa-button>`,content:()=>(0,s.qy)`
                <button
                  type="button"
                  class="save-button"
                  ?disabled=${this._saving||!this._isDirty}
                  @click=${this._save}
                >
                  <wa-icon library="mdi" name="content-save"></wa-icon>
                  ${this._localize(this._saving?"file.saving":"file.save")}
                </button>
                <div class="editor-pane" ?inert=${this._renamingPath===this.path}>
                  <esphome-yaml-editor
                    completion
                    .filePath=${this.path}
                    .value=${this._yaml}
                    .highlightRange=${this._highlight}
                    .scrollToHighlight=${this._scrollToHighlight}
                    @yaml-change=${this._onYamlChange}
                  ></esphome-yaml-editor>
                </div>
              `})}
          </div>
        </div>
      </div>
      <esphome-unsaved-changes-dialog
        heading=${this._localize("file.unsaved_title")}
        message=${this._localize("file.unsaved_message")}
        @discard=${()=>this._unsavedGuard.onDiscard()}
        @save=${()=>this._unsavedGuard.onSave()}
        @cancel=${()=>this._unsavedGuard.onCancel()}
      ></esphome-unsaved-changes-dialog>
      <esphome-confirm-dialog
        destructive
        heading=${this._localize("file.reload_title")}
        message=${this._localize("file.reload_message")}
        confirm-label=${this._localize("file.reload_confirm")}
        @confirm=${this._load.retry}
      ></esphome-confirm-dialog>
      <esphome-delete-file-dialog
        @file-deleted=${this._onDeleted}
      ></esphome-delete-file-dialog>
      <esphome-file-list-dialog></esphome-file-list-dialog>
      <esphome-rename-file-dialog
        @rename-file=${this._rename}
      ></esphome-rename-file-dialog>
    `}async _announceSaved(e){let t=[];try{t=(await this._api.getFileUsage(e)).used_by}catch{}0===t.length?(0,v.VX)(this._localize("file.saved",{path:e})):(0,v.VX)(this._localize("file.saved",{path:e}),{description:this._localize("file.saved_used_by",{count:t.length}),duration:8e3,action:{label:this._localize("file.install_users"),onClick:()=>void(0,g.p)(t,{api:this._api,localize:this._localize,appVersion:this._appVersion,pairings:this._pairings?.values()??[]})}})}constructor(...e){super(...e),this._localize=e=>e,this._apiConnected=!1,this._appVersion="",this._pairings=null,this.path="",this._yaml="",this._savedYaml="",this._saving=!1,this._renamingPath=null,this._selectedSection=null,this._highlight=null,this._scrollToHighlight=!1,this._navCollapsed=!1,this._openSections=new Set([1]),this._load=new _.r(this,{api:()=>this._api,connected:()=>this._apiConnected,configuration:()=>this.path,attempts:4,commit:e=>{this._yaml=e,this._savedYaml=e},onApiError:e=>e.errorCode===n.O.NOT_FOUND?"missing":void 0,onRefreshFailed:()=>(0,v.UG)(this._localize("file.reload_failed"))}),this._unsavedGuard=new y._,this._saveShortcut=new w.k(this,()=>{this._isDirty&&!this._saving&&""!==this._yaml.trim()&&this._save()}),this._leaveGuard=new u.KO(this,{confirmLeave:()=>this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:()=>this._save()}),isDirty:()=>this._isDirty,url:()=>(0,m.zI)(this.path)}),this._onBeforeUnload=e=>{this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onYamlChange=e=>{this._yaml=e.detail.value,this._highlight=null},this._onSectionSelect=e=>{this._selectedSection=e.detail.sectionKey,this._selectedFromLine=e.detail.fromLine},this._onYamlHighlight=e=>{this._highlight=e.detail.range,this._scrollToHighlight=e.detail.scroll},this._pendingSave=null,this._save=()=>{let e=this._pendingSave;if(e)return e.path===this.path?e.result:((0,v.UG)(this._localize("file.save_busy")),Promise.resolve(!1));let t=this._write().finally(()=>this._pendingSave=null);return this._pendingSave={path:this.path,result:t},t},this._write=async()=>{let e=this.path,t=this._yaml;this._saving=!0;try{await this._api.updateConfig(e,t,{expected:this._savedYaml})}catch(t){return t instanceof r.LG&&t.errorCode===n.O.PRECONDITION_FAILED?(0,v.UG)(this._localize("file.changed_on_disk"),{duration:8e3,action:{label:this._localize("file.reload"),onClick:()=>{this.path===e&&(this._isDirty?this._reloadDialog?.open():this._load.start())}}}):(0,h.k)(this._localize,"file.save_error",t),!1}finally{this._saving=!1}return this._announceSaved(e),this.path===e&&(this._savedYaml=t,this.isConnected&&this._yaml===t)},this._showUsage=()=>void this._usageDialog?.showUsage(this.path),this._openRename=()=>void this._renameDialog?.open(this.path),this._rename=async e=>{if(this._isDirty)return void(0,v.UG)(this._localize("packages.rename_save_first"));this._renamingPath=e.detail.path;try{let t=await (0,h.H)(this._api,this._localize,e.detail);null!==t&&this.isConnected&&this.path===e.detail.path&&await (0,u.oo)((0,m.zI)(t))}finally{this._renamingPath=null}},this._confirmDelete=()=>void this._deleteDialog?.open(this.path),this._onDeleted=e=>{this.isConnected&&e.detail.path===this.path&&(this._savedYaml=this._yaml,(0,u.oo)("/packages"))}}}$.styles=[p.G9,c.I,k.E,(0,s.AH)`
      .page-title p {
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      }
      .header-button {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
        border-radius: var(--wa-border-radius-m);
        background: transparent;
        color: var(--wa-color-text-normal);
        font: inherit;
        font-size: var(--wa-font-size-xs);
        font-weight: var(--wa-font-weight-bold);
        cursor: pointer;
      }
      .header-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      .header-button:hover:not(:disabled) {
        background: var(--wa-color-surface-lowered);
      }
      .header-button--accent {
        color: var(--esphome-primary);
      }
      .header-button--accent:hover:not(:disabled) {
        background: var(--esphome-tint);
        border-color: var(--esphome-tint-border);
      }
      .header-button--danger {
        color: var(--esphome-error);
      }
      .header-button--danger:hover:not(:disabled) {
        background: color-mix(in srgb, var(--esphome-error), transparent 92%);
      }
      .header-button wa-icon {
        font-size: 16px;
      }
      .body {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: minmax(230px, 1fr) minmax(0, 4fr);
        gap: var(--wa-space-m);
      }
      .body.no-nav {
        grid-template-columns: minmax(0, 1fr);
      }
      @media (max-width: 900px) {
        .body {
          grid-template-columns: minmax(0, 1fr);
        }
        esphome-device-navigator {
          display: none;
        }
      }
    `],x([(0,a.Fg)({context:d.$F,subscribe:!0}),(0,l.wk)()],$.prototype,"_localize",void 0),x([(0,a.Fg)({context:d.Ie})],$.prototype,"_api",void 0),x([(0,a.Fg)({context:d.Lh,subscribe:!0}),(0,l.wk)()],$.prototype,"_apiConnected",void 0),x([(0,a.Fg)({context:d.wo,subscribe:!0}),(0,l.wk)()],$.prototype,"_appVersion",void 0),x([(0,a.Fg)({context:d._2,subscribe:!0}),(0,l.wk)()],$.prototype,"_pairings",void 0),x([(0,l.MZ)()],$.prototype,"path",void 0),x([(0,l.wk)()],$.prototype,"_yaml",void 0),x([(0,l.wk)()],$.prototype,"_savedYaml",void 0),x([(0,l.wk)()],$.prototype,"_saving",void 0),x([(0,l.wk)()],$.prototype,"_renamingPath",void 0),x([(0,l.wk)()],$.prototype,"_selectedSection",void 0),x([(0,l.wk)()],$.prototype,"_selectedFromLine",void 0),x([(0,l.wk)()],$.prototype,"_highlight",void 0),x([(0,l.wk)()],$.prototype,"_scrollToHighlight",void 0),x([(0,l.wk)()],$.prototype,"_navCollapsed",void 0),x([(0,l.wk)()],$.prototype,"_openSections",void 0),x([(0,l.P)("esphome-unsaved-changes-dialog")],$.prototype,"_unsavedDialog",void 0),x([(0,l.P)("esphome-delete-file-dialog")],$.prototype,"_deleteDialog",void 0),x([(0,l.P)("esphome-file-list-dialog")],$.prototype,"_usageDialog",void 0),x([(0,l.P)("esphome-rename-file-dialog")],$.prototype,"_renameDialog",void 0),x([(0,l.P)("esphome-confirm-dialog")],$.prototype,"_reloadDialog",void 0),$=x([(0,l.EM)("esphome-page-file")],$),i.d(t,{ESPHomePageFile:()=>$})},5858(e,t,i){var a=i(5077);let o=(0,a.AH)`
  :host {
    display: flex;
    flex-direction: column;
    height: calc(100vh - var(--esphome-header-height) - var(--esphome-footer-height));
    box-sizing: border-box;
  }

  .page {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: var(--wa-space-l) var(--content-gutter);
    gap: var(--wa-space-m);
    overflow: hidden;
  }

  .page-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-m);
    flex-shrink: 0;
  }

  .page-title {
    flex: 1;
  }

  .page-title h1 {
    margin: 0 0 2px;
    font-size: var(--wa-font-size-l);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  .page-title p {
    margin: 0;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }

  .editor-card {
    flex: 1;
    position: relative;
    background: var(--wa-color-surface-default);
    border-radius: var(--wa-border-radius-l);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    box-shadow: var(--wa-elevation-02);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .save-button {
    position: absolute;
    bottom: var(--wa-space-m);
    right: var(--wa-space-m);
    z-index: 10;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border: none;
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    /* Match the shared .btn size so Save aligns with Add secret. */
    padding: var(--esphome-button-padding);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    box-shadow: var(--esphome-primary-shadow);
    transition:
      background 0.12s,
      box-shadow 0.12s,
      transform 0.12s;
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
    opacity: 0.4;
    cursor: not-allowed;
    box-shadow: none;
  }

  .save-button wa-icon {
    font-size: 16px;
  }

  .reveal-toggle {
    border: var(--wa-border-width-s) solid var(--esphome-primary);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    padding: 6px 12px;
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: inherit;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    transition: background 0.12s;
  }

  .reveal-toggle:hover {
    background: var(--esphome-tint-strong);
  }

  .reveal-toggle wa-icon {
    font-size: 16px;
  }

  .layout-toggle {
    display: inline-flex;
    align-items: center;
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    overflow: hidden;
    flex-shrink: 0;
  }

  .layout-toggle button {
    border: none;
    background: transparent;
    color: var(--wa-color-text-quiet);
    padding: 6px 10px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .layout-toggle button + button {
    border-left: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .layout-toggle button[aria-pressed="true"] {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .layout-toggle wa-icon {
    font-size: 18px;
  }

  .editor-pane {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    /* The editor scrolls itself and owns its padding, so its scrollbar
       sits at the card edge, not over the row controls. */
    padding: 0;
  }

  .editor-pane > * {
    flex: 1;
    min-height: 0;
  }

  @media (max-width: 900px) {
    .page {
      padding-block: var(--wa-space-s);
    }
    .page-header {
      flex-wrap: wrap;
    }
    .page-title {
      flex-basis: 100%;
    }
  }

  /* Placement only; the block itself comes from loadMessageStyles. The
     auto-margin pairing centers the ladder — the message alone, or the
     message plus the Retry button, which sizes to content instead of
     stretching to the card's width. */
  .message {
    margin-top: auto;
  }
  .message:last-child {
    margin-bottom: auto;
  }
  .message ~ wa-button {
    align-self: center;
    margin-top: var(--wa-space-m);
    margin-bottom: auto;
  }
`;i.d(t,{},{E:o})}}]);
//# sourceMappingURL=76.7f78bbddc483b219.js.map