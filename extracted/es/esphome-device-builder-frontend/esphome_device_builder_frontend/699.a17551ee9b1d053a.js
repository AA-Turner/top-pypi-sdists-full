"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[699],{774(e,t,a){a.r(t),a.d(t,{ESPHomePageSecrets:()=>Y});var r=a(5172),i=a(9165),o=a(2009),s=a(3442),l=a(261),n=a(4342),d=a(1556),c=a(3140),h=a(9460),p=a(1529),u=a(1093),v=a(9317);a(3238),a(2202),a(6117);var m=a(71),_=a(5660),g=a(6029),y=a(9470),f=a(9808),b=a(8851);let w=/^(<<|[A-Za-z_][A-Za-z0-9_.\-]*):(?:[ \t]+([^\n]*))?$/,$=/^[A-Za-z_][A-Za-z0-9_.\-]*$/,x=/^[!&*|>[{]/,k=/^[!&*|>[\]{}@`%]/;function z(e){return""!==e&&k.test(e)?`"${(0,y.k9)(e)}"`:(0,b.Rm)(e)}function S(e){let t=e.split("\n"),a=[];for(let e=0;e<t.length;e++){let r=t[e].match(w);if(!r)continue;let[,i,o]=r;a.push({key:i,line:e,...function(e,t,a){let{value:r}=(0,f.bw)(e??""),i=r.trim();return""===i||i.startsWith("#")?{value:"",editable:!function(e,t){for(let a=t+1;a<e.length;a++){let t=e[a];if(!(""===t.trim()||t.trimStart().startsWith("#")))return/^[ \t]/.test(t)}return!1}(t,a)}:x.test(i)?{value:"",editable:!1}:{value:(0,f.Ir)(i),editable:!0}}(o,t,e)})}return a}function E(e,t,a){let r=e.split("\n"),i=r[t]?.match(w);if(!i)return null;let[,o,s]=i,{value:l,comment:n}=(0,f.bw)(s??"");return r[t]=a(o,l,n),r.join("\n")}let C=(0,o.AH)`
  :host {
    display: block;
    height: 100%;
    box-sizing: border-box;
    overflow-y: auto;
    /* Reserve the gutter so the scrollbar clears the row controls. */
    scrollbar-gutter: stable;
    /* Sole scroll container for the form pane; owns its padding plus
       bottom clearance for the floating Save button. */
    padding: var(--wa-space-m);
    padding-bottom: calc(var(--wa-space-m) * 2 + 2.25rem);
  }

  .rows {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  .groups {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-l);
  }

  .group-header {
    margin: 0 0 var(--wa-space-s);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-quiet);
    text-transform: none;
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    padding-bottom: 4px;
  }

  .group-link {
    color: var(--esphome-primary);
    text-decoration: none;
  }

  .group-link:hover {
    text-decoration: underline;
  }

  /* Keep the dialog tidy and let every field span its full width — the
     base-dialog body is a row layout meant for icon + text, so the add
     form overrides it to a stretched column. */
  esphome-base-dialog {
    --width: 480px;
  }

  .add-body {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: var(--wa-space-m);
  }

  .add-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
  }

  .add-field-label {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
  }

  /* .add-select (wa-select) chrome comes from the shared inputStyles
     combobox rule, keyed on --wa-form-control-height, so it matches the
     name input beside it without hand-rolled duplication. */
  .add-field input,
  .add-field esphome-password-input,
  .add-select {
    width: 100%;
    box-sizing: border-box;
  }

  .btn--add {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .btn--add:hover {
    background: var(--esphome-primary-hover);
  }

  /* The password input is a block custom element; stretch it into the
     value column so it lines up with the key input and remove button. */
  .value-input {
    min-width: 0;
  }

  .row {
    display: grid;
    grid-template-columns: minmax(8rem, 1fr) minmax(8rem, 2fr) auto;
    gap: var(--wa-space-s);
    align-items: center;
  }

  .row--advanced {
    grid-template-columns: minmax(8rem, 1fr) minmax(8rem, 2fr) auto;
  }

  .key-error {
    grid-column: 1 / -1;
    margin: -2px 0 2px;
    font-size: var(--wa-font-size-2xs);
    color: var(--esphome-error);
  }

  .advanced-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0 12px;
    min-height: var(--wa-form-control-height);
    box-sizing: border-box;
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-xs);
  }

  .advanced-badge wa-icon {
    font-size: 15px;
    flex-shrink: 0;
  }

  .icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: var(--wa-form-control-height);
    height: var(--wa-form-control-height);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-raised);
    color: var(--wa-color-text-quiet);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    flex-shrink: 0;
    transition:
      color 0.12s,
      border-color 0.12s,
      background 0.12s;
  }

  .icon-btn:hover {
    color: var(--esphome-error);
    border-color: var(--esphome-error);
  }

  .icon-btn wa-icon {
    font-size: 16px;
  }

  .add-row {
    margin-top: var(--wa-space-m);
  }

  .empty {
    padding: var(--wa-space-l) 0;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
  }
`;function q(e,t,a,r){var i,o=arguments.length,s=o<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,a):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,a,r);else for(var l=e.length-1;l>=0;l--)(i=e[l])&&(s=(o<3?i(s):o>3?i(t,a,s):i(t,a))||s);return o>3&&s&&Object.defineProperty(t,a,s),s}a(986),a(1604),a(2216),a(8944),(0,u.C)({"alert-circle-outline":i.mdiAlertCircleOutline,close:i.mdiClose,plus:i.mdiPlus});class A extends o.WF{render(){let e=S(this.value),t=function(e){let t=[],a=new Map;for(let r of e){let e=r.key.indexOf("__"),i=e>0?r.key.slice(0,e):null;a.has(i)||(a.set(i,[]),t.push(i)),a.get(i).push(r)}return(a.has(null)?[null,...t.filter(e=>null!==e)]:t).map(e=>({device:e,entries:a.get(e)}))}(e),a=t.some(e=>null!==e.device);return(0,o.qy)`
      ${0===e.length?(0,o.qy)`<div class="empty" role="status">${this._localize("secrets.empty")}</div>`:a?(0,o.qy)`<div class="groups">
              ${t.map(t=>this._renderGroup(t,e))}
            </div>`:(0,o.qy)`<div class="rows">
              ${e.map(t=>this._renderRow(t,e))}
            </div>`}
      <div class="add-row">
        <button type="button" class="btn btn--add" @click=${this._openAdd}>
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("secrets.add_secret")}
        </button>
      </div>
      ${this._renderAddDialog()}
    `}_renderGroup(e,t){return(0,o.qy)`<div class="group">
      ${this._renderGroupHeader(e.device)}
      <div class="rows">
        ${e.entries.map(e=>this._renderRow(e,t))}
      </div>
    </div>`}_renderGroupHeader(e){if(null===e)return(0,o.qy)`<h2 class="group-header">
        ${this._localize("secrets.group_shared")}
      </h2>`;let t=this._devices.find(t=>t.name.replace(/-/g,"_")===e.replace(/-/g,"_"));if(!t)return(0,o.qy)`<h2 class="group-header">${e}</h2>`;let a=`/device/${encodeURIComponent(t.configuration)}`,r=(0,h.cV)(a);return(0,o.qy)`<h2 class="group-header">
      <a
        href=${r}
        class="group-link"
        title=${this._localize("secrets.open_device")}
        @click=${e=>{e.metaKey||e.ctrlKey||e.shiftKey||0!==e.button||(e.preventDefault(),(0,p.oo)(a).catch(()=>window.location.assign(r)))}}
        >${e}</a
      >
    </h2>`}_renderAddDialog(){return(0,o.qy)`<esphome-base-dialog
      ?open=${this._addOpen}
      .label=${this._localize("secrets.add_dialog_title")}
      .confirmOnEnter=${this._confirmAdd}
      @request-close=${this._closeAdd}
      @after-hide=${this._closeAdd}
    >
      <div class="body add-body">
        <div class="add-field">
          <span class="add-field-label" id="secret-target-label"
            >${this._localize("secrets.add_dialog_target")}</span
          >
          <wa-select
            class="add-select"
            aria-labelledby="secret-target-label"
            value=${this._addTarget}
            @change=${e=>{this._addTarget=e.target.value,this._addError&&(this._addError=this._addKeyError())}}
          >
            <wa-option value="">${this._localize("secrets.group_shared")}</wa-option>
            ${this._devices.map(e=>(0,o.qy)`<wa-option value=${e.name}>${e.friendly_name||e.name}</wa-option>`)}
          </wa-select>
        </div>
        <label class="add-field">
          <span class="add-field-label"
            >${this._localize("secrets.key_placeholder")}</span
          >
          <input
            class="add-name ${this._addError?"invalid":""}"
            type="text"
            autocomplete="off"
            spellcheck="false"
            .value=${(0,m.V)(this._addName)}
            aria-invalid=${this._addError?"true":"false"}
            @input=${e=>{this._addName=e.target.value,this._addError=null}}
          />
        </label>
        <label class="add-field">
          <span class="add-field-label"
            >${this._localize("secrets.value_placeholder")}</span
          >
          <esphome-password-input
            .value=${this._addValue}
            .revealed=${this.revealSensitive}
            label=${this._localize("secrets.value_placeholder")}
            placeholder=${this._localize("secrets.value_placeholder")}
            @password-input-change=${e=>this._addValue=e.detail.value}
          ></esphome-password-input>
        </label>
        ${this._addError?(0,o.qy)`<div class="key-error" role="alert">${this._addError}</div>`:o.s6}
      </div>
      <div class="actions">
        <button class="btn btn--cancel" @click=${this._closeAdd}>
          ${this._localize("layout.cancel")}
        </button>
        <button class="btn btn--add" @click=${this._confirmAdd}>
          ${this._localize("secrets.add_secret")}
        </button>
      </div>
    </esphome-base-dialog>`}_renderRow(e,t){let a=this._keyError?.line===e.line;return e.editable?(0,o.qy)`<div class="row">
        <input
          type="text"
          class=${a?"invalid":""}
          .value=${(0,m.V)(e.key)}
          autocomplete="off"
          spellcheck="false"
          placeholder=${this._localize("secrets.key_placeholder")}
          aria-label=${this._localize("secrets.key_placeholder")}
          aria-invalid=${a?"true":"false"}
          @change=${a=>this._onKeyChange(e,t,a.currentTarget)}
        />
        <esphome-password-input
          class="value-input"
          .value=${e.value}
          .revealed=${this.revealSensitive}
          label=${this._localize("secrets.value_placeholder")}
          placeholder=${this._localize("secrets.value_placeholder")}
          @password-input-change=${t=>{var a,r,i;return this._emit((a=this.value,r=e.line,i=t.detail.value,E(a,r,(e,t,a)=>`${e}: ${z(i)}${a}`)))}}
        ></esphome-password-input>
        <button
          type="button"
          class="icon-btn"
          title=${this._localize("secrets.remove_secret")}
          aria-label=${this._localize("secrets.remove_secret")}
          @click=${()=>{var t,a;let r;return this._emit((t=this.value,a=e.line,r=t.split("\n"),a<0||a>=r.length||!w.test(r[a])?null:(r.splice(a,1),r.join("\n"))))}}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </div>
      ${a?(0,o.qy)`<div class="key-error">${this._keyError?.message}</div>`:o.s6}`:(0,o.qy)`<div class="row row--advanced">
        <input
          type="text"
          .value=${e.key}
          readonly
          aria-label=${this._localize("secrets.key_placeholder")}
        />
        <span class="advanced-badge">
          <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
          ${this._localize("secrets.advanced_badge")}
        </span>
        <span></span>
      </div>`}_onKeyChange(e,t,a){var r,i;let o=a.value.trim();if(o===e.key){this._keyError=null;return}if(!$.test(o)){this._keyError={line:e.line,message:this._localize("secrets.invalid_key")},a.value=e.key;return}if(t.some(t=>t.line!==e.line&&t.key===o)){this._keyError={line:e.line,message:this._localize("secrets.duplicate_key")},a.value=e.key;return}this._keyError=null,this._emit((r=this.value,i=e.line,E(r,i,(e,t,a)=>""===t&&""===a?`${o}:`:`${o}: ${t}${a}`)))}_addKey(){return(this._addTarget?`${this._addTarget}__`:"")+this._addName.trim()}_addKeyError(){var e;return(e=this._addName.trim(),$.test(e))?S(this.value).some(e=>e.key===this._addKey())?this._localize("secrets.duplicate_key"):null:this._localize("secrets.invalid_key")}_emit(e){if(null===e){l.A.error(this._localize("secrets.edit_out_of_sync"),{richColors:!0}),this.requestUpdate();return}this._keyError=null,this.value=e,this.dispatchEvent(new CustomEvent("yaml-change",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.value="",this.revealSensitive=!1,this._keyError=null,this._addOpen=!1,this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._openAdd=()=>{this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._addOpen=!0},this._closeAdd=()=>{this._addOpen=!1},this._confirmAdd=()=>{if(!this._addOpen)return;let e=this._addKeyError();if(e){this._addError=e;return}this._addOpen=!1,this._emit(function(e,t,a){let r=`${t}: ${z(a)}`;if(""===e)return`${r}
`;let i=e.endsWith("\n")?"":"\n";return`${e}${i}${r}
`}(this.value,this._addKey(),this._addValue))}}}function L(e,t,a,r){var i,o=arguments.length,s=o<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,a):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,a,r);else for(var l=e.length-1;l>=0;l--)(i=e[l])&&(s=(o<3?i(s):o>3?i(t,a,s):i(t,a))||s);return o>3&&s&&Object.defineProperty(t,a,s),s}A.styles=[c.G,_.z9,g.W,C],q([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,s.wk)()],A.prototype,"_localize",void 0),q([(0,r.Fg)({context:d.xJ,subscribe:!0}),(0,s.wk)()],A.prototype,"_devices",void 0),q([(0,s.MZ)()],A.prototype,"value",void 0),q([(0,s.MZ)({type:Boolean})],A.prototype,"revealSensitive",void 0),q([(0,s.wk)()],A.prototype,"_keyError",void 0),q([(0,s.wk)()],A.prototype,"_addOpen",void 0),q([(0,s.wk)()],A.prototype,"_addTarget",void 0),q([(0,s.wk)()],A.prototype,"_addName",void 0),q([(0,s.wk)()],A.prototype,"_addValue",void 0),q([(0,s.wk)()],A.prototype,"_addError",void 0),A=q([(0,s.EM)("esphome-secrets-structured-editor")],A),a(9786),a(2975),(0,u.C)({"content-save":i.mdiContentSave,"dock-left":i.mdiDockLeft,"dock-right":i.mdiDockRight,eye:i.mdiEye,"eye-off":i.mdiEyeOff});let D="secrets.yaml",O="esphome-secrets-layout",R=["form","yaml"];class Y extends o.WF{async connectedCallback(){super.connectedCallback(),this._layout=this._readStoredLayout(),(0,p.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("secrets-saved",this._onExternalSecretsSaved),await this._loadFromServer()}_readStoredLayout(){let e=localStorage.getItem(O);return R.includes(e)?e:"form"}_setLayout(e){this._layout=e,localStorage.setItem(O,e)}disconnectedCallback(){(0,p.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),this._unsavedGuard.cancelPending(),window.removeEventListener("secrets-saved",this._onExternalSecretsSaved),super.disconnectedCallback()}get _isDirty(){return this._yaml!==this._savedYaml}async _loadFromServer(){try{let e=await this._api.getConfig(D);this._yaml=e,this._savedYaml=e}catch{let e=this._localize("secrets.file_header");this._yaml=e,this._savedYaml=e}this._loaded=!0}render(){let e=this._localize(this._revealSensitive?"secrets.hide_values":"secrets.reveal_values");return(0,o.qy)`
      <div class="page">
        <div class="page-header">
          <div class="page-title">
            <h1>${this._localize("secrets.title")}</h1>
            <p>${this._localize("secrets.desc")}</p>
          </div>
          <div
            class="layout-toggle"
            role="group"
            aria-label=${this._localize("secrets.layout_label")}
          >
            <button
              type="button"
              aria-pressed=${"form"===this._layout}
              aria-label=${this._localize("secrets.layout_form")}
              title=${this._localize("secrets.layout_form")}
              @click=${()=>this._setLayout("form")}
            >
              <wa-icon library="mdi" name="dock-left"></wa-icon>
            </button>
            <button
              type="button"
              aria-pressed=${"yaml"===this._layout}
              aria-label=${this._localize("secrets.layout_yaml")}
              title=${this._localize("secrets.layout_yaml")}
              @click=${()=>this._setLayout("yaml")}
            >
              <wa-icon library="mdi" name="dock-right"></wa-icon>
            </button>
          </div>
          <button
            type="button"
            class="reveal-toggle"
            aria-pressed=${this._revealSensitive}
            @click=${this._toggleRevealSensitive}
          >
            <wa-icon
              library="mdi"
              name=${this._revealSensitive?"eye-off":"eye"}
            ></wa-icon>
            ${e}
          </button>
        </div>
        <div class="editor-card">
          ${this._loaded?(0,o.qy)`
                <button
                  type="button"
                  class="save-button"
                  ?disabled=${this._saving||this._yaml===this._savedYaml||""===this._yaml.trim()}
                  @click=${this._save}
                >
                  <wa-icon library="mdi" name="content-save"></wa-icon>
                  ${this._saving?this._localize("secrets.saving"):this._localize("secrets.save")}
                </button>
                <div class=${`editor-layout editor-layout--${this._layout}`}>
                  <div class="editor-pane editor-pane--form">
                    <esphome-secrets-structured-editor
                      .value=${this._yaml}
                      .revealSensitive=${this._revealSensitive}
                      @yaml-change=${this._onYamlChange}
                    ></esphome-secrets-structured-editor>
                  </div>
                  <div class="editor-pane editor-pane--yaml">
                    <esphome-yaml-editor
                      .value=${this._yaml}
                      .maskAllValues=${!0}
                      .revealSensitive=${this._revealSensitive}
                      @yaml-change=${this._onYamlChange}
                    ></esphome-yaml-editor>
                  </div>
                </div>
              `:(0,o.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`}
        </div>
      </div>
      <esphome-unsaved-changes-dialog
        heading=${this._localize("secrets.unsaved_title")}
        message=${this._localize("secrets.unsaved_message")}
        @discard=${this._onUnsavedDiscard}
        @save=${this._onUnsavedSave}
        @cancel=${this._onUnsavedCancel}
      ></esphome-unsaved-changes-dialog>
    `}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}async _save(){let e=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let t=!0,a="";try{await this._api.updateConfig(D,this._yaml)}catch(r){(r instanceof Error?r.message:"").includes("timed out")||(t=!1,this._savedYaml=e,a=(0,n.v)(r))}finally{this._saving=!1}if(t&&window.dispatchEvent(new CustomEvent("secrets-saved",{detail:{source:this}})),t)return l.A.success(this._localize("secrets.saved"),{richColors:!0}),!0;let r=this._localize("secrets.save_error");return l.A.error(a?`${r}: ${a}`:r,{richColors:!0}),!1}constructor(...e){super(...e),this._localize=e=>e,this._yaml="",this._savedYaml="",this._saving=!1,this._loaded=!1,this._revealSensitive=!1,this._layout="form",this._unsavedGuard=new v._,this._allowingLeave=!1,this._confirmLeave=async()=>{let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>{let e=await this._save();return e&&(this._allowingLeave=!0),e}});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,h.cV)("/secrets")),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._onExternalSecretsSaved=e=>{e.detail?.source===this||this._yaml===this._savedYaml&&this._loadFromServer()},this._onYamlChange=e=>{this._yaml=e.detail.value}}}Y.styles=[c.G,(0,o.AH)`
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

      .editor-layout {
        flex: 1;
        min-height: 0;
        display: grid;
        gap: 0;
      }

      .editor-layout--form,
      .editor-layout--yaml {
        grid-template-columns: 1fr;
      }

      .editor-pane {
        min-height: 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
      }

      .editor-pane > * {
        flex: 1;
        min-height: 0;
      }

      /* The editor scrolls itself and owns its padding, so its scrollbar
         sits at the card edge, not over the row controls. */
      .editor-pane--form {
        padding: 0;
      }

      .editor-layout--yaml .editor-pane--form,
      .editor-layout--form .editor-pane--yaml {
        display: none;
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

      .loading {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        color: var(--wa-color-text-quiet);
      }
    `],L([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,s.wk)()],Y.prototype,"_localize",void 0),L([(0,r.Fg)({context:d.Ie})],Y.prototype,"_api",void 0),L([(0,s.wk)()],Y.prototype,"_yaml",void 0),L([(0,s.wk)()],Y.prototype,"_savedYaml",void 0),L([(0,s.wk)()],Y.prototype,"_saving",void 0),L([(0,s.wk)()],Y.prototype,"_loaded",void 0),L([(0,s.wk)()],Y.prototype,"_revealSensitive",void 0),L([(0,s.wk)()],Y.prototype,"_layout",void 0),L([(0,s.P)("esphome-unsaved-changes-dialog")],Y.prototype,"_unsavedDialog",void 0),Y=L([(0,s.EM)("esphome-page-secrets")],Y)}}]);
//# sourceMappingURL=699.a17551ee9b1d053a.js.map