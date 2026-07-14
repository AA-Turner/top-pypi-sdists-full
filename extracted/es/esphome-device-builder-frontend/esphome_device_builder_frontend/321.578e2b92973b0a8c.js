"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[321],{3984(e,t,a){a.r(t),a.d(t,{ESPHomePageSecrets:()=>U});var i=a(5172),r=a(9165),s=a(2009),o=a(7622),l=a(4342),n=a(1556),d=a(3140),c=a(9460),h=a(9877),p=a(1529),u=a(918),v=a(1093),_=a(4818),m=a(7967),g=a(9470),y=a(9808),f=a(8851);let w=/^(<<|[A-Za-z_][A-Za-z0-9_.\-]*):(?:[ \t]+([^\n]*))?$/,b=/^[A-Za-z_][A-Za-z0-9_.\-]*$/,$=/^[!&*|>[{]/,x=/^[!&*|>[\]{}@`%]/;function k(e){return""!==e&&x.test(e)?`"${(0,g.k9)(e)}"`:(0,f.Rm)(e)}function z(e){let t=e.split("\n"),a=[];for(let e=0;e<t.length;e++){let i=t[e].match(w);if(!i)continue;let[,r,s]=i;a.push({key:r,line:e,...function(e,t,a){let{value:i}=(0,y.bw)(e??""),r=i.trim();return""===r||r.startsWith("#")?{value:"",editable:!function(e,t){for(let a=t+1;a<e.length;a++){let t=e[a];if(!(""===t.trim()||t.trimStart().startsWith("#")))return/^[ \t]/.test(t)}return!1}(t,a)}:$.test(r)?{value:"",editable:!1}:{value:(0,y.Ir)(r),editable:!0}}(s,t,e)})}return a}function E(e,t,a){let i=e.split("\n"),r=i[t]?.match(w);if(!r)return null;let[,s,o]=r,{value:l,comment:n}=(0,y.bw)(o??"");return i[t]=a(s,l,n),i.join("\n")}var S=a(9317);let q=(0,s.AH)`
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

  .loading {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: var(--wa-color-text-quiet);
  }
`;a(3238),a(2202),a(6117),a(8768);var L=a(71),C=a(5660),P=a(6029);let A=(0,s.AH)`
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
`;function D(e,t,a,i){var r,s=arguments.length,o=s<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,a):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,i);else for(var l=e.length-1;l>=0;l--)(r=e[l])&&(o=(s<3?r(o):s>3?r(t,a,o):r(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}a(986),a(9691),a(2216),a(8944),(0,v.C)({"alert-circle-outline":r.mdiAlertCircleOutline,close:r.mdiClose,plus:r.mdiPlus});class O extends s.WF{render(){let e=z(this.value),t=function(e){let t=[],a=new Map;for(let i of e){let e=i.key.indexOf("__"),r=e>0?i.key.slice(0,e):null,s=r?(0,m.GY)(r)||r:null;a.has(s)||(a.set(s,[]),t.push(s)),a.get(s).push(i)}return(a.has(null)?[null,...t.filter(e=>null!==e)]:t).map(e=>({device:e,entries:a.get(e)}))}(e),a=t.some(e=>null!==e.device);return(0,s.qy)`
      ${0===e.length?(0,s.qy)`<div class="empty" role="status">
              ${this._localize("secrets.empty")}
            </div>`:a?(0,s.qy)`<div class="groups">
                ${t.map(t=>this._renderGroup(t,e))}
              </div>`:(0,s.qy)`<div class="rows">
                ${e.map(t=>this._renderRow(t,e))}
              </div>`}
      <div class="add-row">
        <button type="button" class="btn btn--add" @click=${this._openAdd}>
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("secrets.add_secret")}
        </button>
      </div>
      ${this._renderAddDialog()}
    `}_renderGroup(e,t){return(0,s.qy)`<div class="group">
      ${this._renderGroupHeader(e.device)}
      <div class="rows">
        ${e.entries.map(e=>this._renderRow(e,t))}
      </div>
    </div>`}_renderGroupHeader(e){if(null===e)return(0,s.qy)`<h2 class="group-header">
        ${this._localize("secrets.group_shared")}
      </h2>`;let t=this._devices.find(t=>t.name.replace(/-/g,"_")===e.replace(/-/g,"_"));if(!t)return(0,s.qy)`<h2 class="group-header">${e}</h2>`;let a=`/device/${encodeURIComponent(t.configuration)}`,i=(0,c.cV)(a);return(0,s.qy)`<h2 class="group-header">
      <a
        href=${i}
        class="group-link"
        title=${this._localize("secrets.open_device")}
        @click=${e=>{e.metaKey||e.ctrlKey||e.shiftKey||0!==e.button||(e.preventDefault(),(0,p.oo)(a).catch(()=>window.location.assign(i)))}}
        >${e}</a
      >
    </h2>`}_renderAddDialog(){return(0,s.qy)`<esphome-base-dialog
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
            ${this._devices.map(e=>(0,s.qy)`<wa-option value=${e.name}>${e.friendly_name||e.name}</wa-option>`)}
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
            .value=${(0,L.V)(this._addName)}
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
        ${this._addError?(0,s.qy)`<div class="key-error" role="alert">${this._addError}</div>`:s.s6}
      </div>
      <div class="actions">
        <button class="btn btn--cancel" @click=${this._closeAdd}>
          ${this._localize("layout.cancel")}
        </button>
        <button class="btn btn--add" @click=${this._confirmAdd}>
          ${this._localize("secrets.add_secret")}
        </button>
      </div>
    </esphome-base-dialog>`}_renderRow(e,t){let a=this._keyError?.line===e.line;return e.editable?(0,s.qy)`<div class="row">
        <input
          type="text"
          class=${a?"invalid":""}
          .value=${(0,L.V)(e.key)}
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
          @password-input-change=${t=>{var a,i,r;return this._emit((a=this.value,i=e.line,r=t.detail.value,E(a,i,(e,t,a)=>`${e}: ${k(r)}${a}`)))}}
        ></esphome-password-input>
        <button
          type="button"
          class="icon-btn"
          title=${this._localize("secrets.remove_secret")}
          aria-label=${this._localize("secrets.remove_secret")}
          @click=${()=>{var t,a;let i;return this._emit((t=this.value,a=e.line,i=t.split("\n"),a<0||a>=i.length||!w.test(i[a])?null:(i.splice(a,1),i.join("\n"))))}}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </div>
      ${a?(0,s.qy)`<div class="key-error">${this._keyError?.message}</div>`:s.s6}`:(0,s.qy)`<div class="row row--advanced">
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
      </div>`}_onKeyChange(e,t,a){var i,r;let s=a.value.trim();if(s===e.key){this._keyError=null;return}if(!b.test(s)){this._keyError={line:e.line,message:this._localize("secrets.invalid_key")},a.value=e.key;return}if(t.some(t=>t.line!==e.line&&t.key===s)){this._keyError={line:e.line,message:this._localize("secrets.duplicate_key")},a.value=e.key;return}this._keyError=null,this._emit((i=this.value,r=e.line,E(i,r,(e,t,a)=>""===t&&""===a?`${s}:`:`${s}: ${t}${a}`)))}_addKey(){let e=this._addTarget?(0,m.GY)(this._addTarget):"",t=this._addName.trim();return e?`${e}__${t}`:t}_addKeyError(){var e;return(e=this._addName.trim(),b.test(e))?z(this.value).some(e=>e.key===this._addKey())?this._localize("secrets.duplicate_key"):null:this._localize("secrets.invalid_key")}_emit(e){if(null===e){(0,u.UG)(this._localize("secrets.edit_out_of_sync")),this.requestUpdate();return}this._keyError=null,this.value=e,this.dispatchEvent(new CustomEvent("yaml-change",{detail:{value:e},bubbles:!0,composed:!0}))}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.value="",this.revealSensitive=!1,this._keyError=null,this._addOpen=!1,this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._openAdd=()=>{this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._addOpen=!0},this._closeAdd=()=>{this._addOpen=!1},this._confirmAdd=()=>{if(!this._addOpen)return;let e=this._addKeyError();if(e){this._addError=e;return}this._addOpen=!1,this._emit(function(e,t,a){let i=`${t}: ${k(a)}`;if(""===e)return`${i}
`;let r=e.endsWith("\n")?"":"\n";return`${e}${r}${i}
`}(this.value,this._addKey(),this._addValue))}}}function Y(e,t,a,i){var r,s=arguments.length,o=s<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,a):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,i);else for(var l=e.length-1;l>=0;l--)(r=e[l])&&(o=(s<3?r(o):s>3?r(t,a,o):r(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}O.styles=[d.G,C.z9,P.W,A],D([(0,i.Fg)({context:n.$F,subscribe:!0}),(0,o.wk)()],O.prototype,"_localize",void 0),D([(0,i.Fg)({context:n.xJ,subscribe:!0}),(0,o.wk)()],O.prototype,"_devices",void 0),D([(0,o.MZ)()],O.prototype,"value",void 0),D([(0,o.MZ)({type:Boolean})],O.prototype,"revealSensitive",void 0),D([(0,o.wk)()],O.prototype,"_keyError",void 0),D([(0,o.wk)()],O.prototype,"_addOpen",void 0),D([(0,o.wk)()],O.prototype,"_addTarget",void 0),D([(0,o.wk)()],O.prototype,"_addName",void 0),D([(0,o.wk)()],O.prototype,"_addValue",void 0),D([(0,o.wk)()],O.prototype,"_addError",void 0),O=D([(0,o.EM)("esphome-secrets-structured-editor")],O),a(9786),a(7715),(0,v.C)({"code-braces":r.mdiCodeBraces,"content-save":r.mdiContentSave,eye:r.mdiEye,"eye-off":r.mdiEyeOff,"form-textbox":r.mdiFormTextbox});let F="secrets.yaml",G="esphome-secrets-layout",R=["form","yaml"];class U extends s.WF{async connectedCallback(){super.connectedCallback();let e=this._readStoredLayout();e?this._layout=e:this._seedLayoutFromBackend(),(0,p.fe)(this._confirmLeave),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("popstate",this._onPopState,{capture:!0}),window.addEventListener("secrets-saved",this._onExternalSecretsSaved),await this._loadFromServer()}_readStoredLayout(){let e=localStorage.getItem(G);return R.includes(e)?e:null}async _seedLayoutFromBackend(){try{let e=await this._api.getPreferences();null===this._readStoredLayout()&&(this._layout=(0,h.OU)(e.secrets_editor_layout))}catch(e){console.warn("Failed to load secrets layout preference:",e)}}_setLayout(e){this._layout=e,localStorage.setItem(G,e),this._api.updatePreferences({secrets_editor_layout:(0,h.aQ)(e)}).catch(e=>console.warn("Failed to persist secrets layout preference:",e))}disconnectedCallback(){(0,p.fe)(null),window.removeEventListener("beforeunload",this._onBeforeUnload),window.removeEventListener("popstate",this._onPopState,{capture:!0}),this._unsavedGuard.cancelPending(),this._settlePendingWipe?.(!1),window.removeEventListener("secrets-saved",this._onExternalSecretsSaved),super.disconnectedCallback()}get _isDirty(){return this._yaml!==this._savedYaml}async _loadFromServer(){try{let e=await this._api.getConfig(F);this._yaml=e,this._savedYaml=e}catch{let e=this._localize("secrets.file_header");this._yaml=e,this._savedYaml=e}this._loaded=!0}render(){let e=this._localize(this._revealSensitive?"secrets.hide_values":"secrets.reveal_values");return(0,s.qy)`
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
              <wa-icon library="mdi" name="form-textbox"></wa-icon>
            </button>
            <button
              type="button"
              aria-pressed=${"yaml"===this._layout}
              aria-label=${this._localize("secrets.layout_yaml")}
              title=${this._localize("secrets.layout_yaml")}
              @click=${()=>this._setLayout("yaml")}
            >
              <wa-icon library="mdi" name="code-braces"></wa-icon>
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
          ${this._loaded?(0,s.qy)`
                  <button
                    type="button"
                    class="save-button"
                    ?disabled=${this._saving||this._yaml===this._savedYaml}
                    @click=${this._save}
                  >
                    <wa-icon library="mdi" name="content-save"></wa-icon>
                    ${this._saving?this._localize("secrets.saving"):this._localize("secrets.save")}
                  </button>
                  <div class="editor-pane">
                    ${"form"===this._layout?(0,s.qy)`<esphome-secrets-structured-editor
                            .value=${this._yaml}
                            .revealSensitive=${this._revealSensitive}
                            @yaml-change=${this._onYamlChange}
                          ></esphome-secrets-structured-editor>`:(0,s.qy)`<esphome-yaml-editor
                            .value=${this._yaml}
                            .maskAllValues=${!0}
                            .revealSensitive=${this._revealSensitive}
                            @yaml-change=${this._onYamlChange}
                          ></esphome-yaml-editor>`}
                  </div>
                `:(0,s.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`}
        </div>
      </div>
      <esphome-unsaved-changes-dialog
        heading=${this._localize("secrets.unsaved_title")}
        message=${this._localize("secrets.unsaved_message")}
        @discard=${this._onUnsavedDiscard}
        @save=${this._onUnsavedSave}
        @cancel=${this._onUnsavedCancel}
      ></esphome-unsaved-changes-dialog>
      <esphome-confirm-dialog
        ?destructive=${!0}
        heading=${this._localize("secrets.wipe_title")}
        message=${this._localize("secrets.wipe_message")}
        confirm-label=${this._localize("secrets.wipe_confirm")}
      ></esphome-confirm-dialog>
    `}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_confirmWipe(){let e=this._wipeDialog;return e?new Promise(t=>{let a=a=>{e.removeEventListener("confirm",i),e.removeEventListener("cancel",r),this._settlePendingWipe=null,t(a)},i=()=>a(!0),r=()=>a(!1);this._settlePendingWipe=a,e.addEventListener("confirm",i),e.addEventListener("cancel",r),e.open()}):Promise.resolve(!1)}async _save(){if(0===z(this._yaml).length&&z(this._savedYaml).length>0&&!await this._confirmWipe())return!1;let e=""===this._yaml.trim(),t=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let a=!0,i="";try{e?await this._api.updateConfig(F,this._yaml,{allowWipe:!0}):await this._api.updateConfig(F,this._yaml)}catch(e){(e instanceof Error?e.message:"").includes("timed out")||(a=!1,this._savedYaml=t,i=(0,l.v)(e))}finally{this._saving=!1}if(a&&window.dispatchEvent(new CustomEvent("secrets-saved",{detail:{source:this}})),a)return(0,u.VX)(this._localize("secrets.saved")),!0;let r=this._localize("secrets.save_error");return(0,u.UG)(i?`${r}: ${i}`:r),!1}constructor(...e){super(...e),this._localize=e=>e,this._yaml="",this._savedYaml="",this._saving=!1,this._loaded=!1,this._revealSensitive=!1,this._layout="form",this._unsavedGuard=new S._,this._saveShortcut=new _.k(this,()=>{this._isDirty&&!this._saving&&""!==this._yaml.trim()&&this._save()}),this._allowingLeave=!1,this._settlePendingWipe=null,this._confirmLeave=async()=>{let e=await this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:async()=>{let e=await this._save();return e&&(this._allowingLeave=!0),e}});return e&&(this._allowingLeave=!0),e},this._onBeforeUnload=e=>{this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onPopState=e=>{if(this._allowingLeave){this._allowingLeave=!1;return}this._isDirty&&(e.stopImmediatePropagation(),window.history.pushState({},"",(0,c.cV)("/secrets")),this._confirmLeave().then(e=>{e&&(this._allowingLeave=!0,window.history.back())}))},this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._onExternalSecretsSaved=e=>{e.detail?.source===this||this._yaml===this._savedYaml&&this._loadFromServer()},this._onYamlChange=e=>{this._yaml=e.detail.value}}}U.styles=[d.G,q],Y([(0,i.Fg)({context:n.$F,subscribe:!0}),(0,o.wk)()],U.prototype,"_localize",void 0),Y([(0,i.Fg)({context:n.Ie})],U.prototype,"_api",void 0),Y([(0,o.wk)()],U.prototype,"_yaml",void 0),Y([(0,o.wk)()],U.prototype,"_savedYaml",void 0),Y([(0,o.wk)()],U.prototype,"_saving",void 0),Y([(0,o.wk)()],U.prototype,"_loaded",void 0),Y([(0,o.wk)()],U.prototype,"_revealSensitive",void 0),Y([(0,o.wk)()],U.prototype,"_layout",void 0),Y([(0,o.P)("esphome-unsaved-changes-dialog")],U.prototype,"_unsavedDialog",void 0),Y([(0,o.P)("esphome-confirm-dialog")],U.prototype,"_wipeDialog",void 0),U=Y([(0,o.EM)("esphome-page-secrets")],U)}}]);
//# sourceMappingURL=321.578e2b92973b0a8c.js.map