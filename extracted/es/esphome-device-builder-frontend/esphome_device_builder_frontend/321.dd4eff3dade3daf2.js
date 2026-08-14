"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[321],{3984(e,t,a){a.r(t),a.d(t,{ESPHomePageSecrets:()=>j});var r=a(9104),i=a(289),s=a(5077),o=a(9356),l=a(4342),n=a(3835),d=a(1556),c=a(4835),h=a(3140),u=a(7051),p=a(9877),v=a(1529),m=a(918),_=a(1093),g=a(3854),y=a(4818),f=a(348),b=a(9470),w=a(9808),$=a(8851);let x=/^(<<|[A-Za-z_][A-Za-z0-9_.\-]*):(?:[ \t]+([^\n]*))?$/,k=/^[A-Za-z_][A-Za-z0-9_.\-]*$/,z=/^[!&*|>[{]/,E=/^[!&*|>[\]{}@`%]/;function S(e){return""!==e&&E.test(e)?`"${(0,b.k9)(e)}"`:(0,$.Rm)(e)}function q(e){let t=e.split("\n"),a=[];for(let e=0;e<t.length;e++){let r=t[e].match(x);if(!r)continue;let[,i,s]=r;a.push({key:i,line:e,...function(e,t,a){let{value:r}=(0,w.bw)(e??""),i=r.trim();return""===i||i.startsWith("#")?{value:"",editable:!function(e,t){for(let a=t+1;a<e.length;a++){let t=e[a];if(!(""===t.trim()||t.trimStart().startsWith("#")))return/^[ \t]/.test(t)}return!1}(t,a)}:z.test(i)?{value:"",editable:!1}:{value:(0,w.Ir)(i),editable:!0}}(s,t,e)})}return a}function C(e,t,a){let r=e.split("\n"),i=r[t]?.match(x);if(!i)return null;let[,s,o]=i,{value:l,comment:n}=(0,w.bw)(o??"");return r[t]=a(s,l,n),r.join("\n")}var A=a(9317);let O=(0,s.AH)`
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
`;a(9577),a(9218),a(2522),a(8768);var L=a(2974),D=a(5660),P=a(6029),G=a(9460),Y=a(3330);let F=(0,s.AH)`
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
`;function R(e,t,a,r){var i,s=arguments.length,o=s<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,a):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,r);else for(var l=e.length-1;l>=0;l--)(i=e[l])&&(o=(s<3?i(o):s>3?i(t,a,o):i(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}a(1687),a(4063),a(2216),a(8944),(0,_.C)({"alert-circle-outline":i.mdiAlertCircleOutline,close:i.mdiClose,plus:i.mdiPlus});class U extends s.WF{render(){let e=q(this.value),t=function(e){let t=[],a=new Map;for(let r of e){let e=r.key.indexOf("__"),i=e>0?r.key.slice(0,e):null,s=i?(0,f.GY)(i)||i:null;a.has(s)||(a.set(s,[]),t.push(s)),a.get(s).push(r)}return(a.has(null)?[null,...t.filter(e=>null!==e)]:t).map(e=>({device:e,entries:a.get(e)}))}(e),a=t.some(e=>null!==e.device);return(0,s.qy)`
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
      </h2>`;let t=this._devices.find(t=>t.name.replace(/-/g,"_")===e.replace(/-/g,"_"));if(!t)return(0,s.qy)`<h2 class="group-header">${e}</h2>`;let a=`/device/${encodeURIComponent(t.configuration)}`,r=(0,G.cV)(a);return(0,s.qy)`<h2 class="group-header">
      <a
        href=${r}
        class="group-link"
        title=${this._localize("secrets.open_device")}
        @click=${e=>{e.metaKey||e.ctrlKey||e.shiftKey||0!==e.button||(e.preventDefault(),(0,v.oo)(a).catch(()=>window.location.assign(r)))}}
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
          @password-input-change=${t=>{var a,r,i;return this._emit((a=this.value,r=e.line,i=t.detail.value,C(a,r,(e,t,a)=>`${e}: ${S(i)}${a}`)))}}
        ></esphome-password-input>
        <button
          type="button"
          class="icon-btn"
          title=${this._localize("secrets.remove_secret")}
          aria-label=${this._localize("secrets.remove_secret")}
          @click=${()=>{var t,a;let r;return this._emit((t=this.value,a=e.line,r=t.split("\n"),a<0||a>=r.length||!x.test(r[a])?null:(r.splice(a,1),r.join("\n"))))}}
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
      </div>`}_onKeyChange(e,t,a){var r,i;let s=a.value.trim();if(s===e.key){this._keyError=null;return}if(!k.test(s)){this._keyError={line:e.line,message:this._localize("secrets.invalid_key")},a.value=e.key;return}if(t.some(t=>t.line!==e.line&&t.key===s)){this._keyError={line:e.line,message:this._localize("secrets.duplicate_key")},a.value=e.key;return}this._keyError=null,this._emit((r=this.value,i=e.line,C(r,i,(e,t,a)=>""===t&&""===a?`${s}:`:`${s}: ${t}${a}`)))}_addKey(){let e=this._addTarget?(0,f.GY)(this._addTarget):"",t=this._addName.trim();return e?`${e}__${t}`:t}_addKeyError(){var e;return(e=this._addName.trim(),k.test(e))?q(this.value).some(e=>e.key===this._addKey())?this._localize("secrets.duplicate_key"):null:this._localize("secrets.invalid_key")}_emit(e){if(null===e){(0,m.UG)(this._localize("secrets.edit_out_of_sync")),this.requestUpdate();return}this._keyError=null,this.value=e,(0,Y.r)(this,"yaml-change",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.value="",this.revealSensitive=!1,this._keyError=null,this._addOpen=!1,this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._openAdd=()=>{this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._addOpen=!0},this._closeAdd=()=>{this._addOpen=!1},this._confirmAdd=()=>{if(!this._addOpen)return;let e=this._addKeyError();if(e){this._addError=e;return}this._addOpen=!1,this._emit(function(e,t,a){let r=`${t}: ${S(a)}`;if(""===e)return`${r}
`;let i=e.endsWith("\n")?"":"\n";return`${e}${i}${r}
`}(this.value,this._addKey(),this._addValue))}}}function T(e,t,a,r){var i,s=arguments.length,o=s<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,a):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,r);else for(var l=e.length-1;l>=0;l--)(i=e[l])&&(o=(s<3?i(o):s>3?i(t,a,o):i(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}U.styles=[h.G,D.z9,P.W,F],R([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,o.wk)()],U.prototype,"_localize",void 0),R([(0,r.Fg)({context:d.xJ,subscribe:!0}),(0,o.wk)()],U.prototype,"_devices",void 0),R([(0,o.MZ)()],U.prototype,"value",void 0),R([(0,o.MZ)({type:Boolean})],U.prototype,"revealSensitive",void 0),R([(0,o.wk)()],U.prototype,"_keyError",void 0),R([(0,o.wk)()],U.prototype,"_addOpen",void 0),R([(0,o.wk)()],U.prototype,"_addTarget",void 0),R([(0,o.wk)()],U.prototype,"_addName",void 0),R([(0,o.wk)()],U.prototype,"_addValue",void 0),R([(0,o.wk)()],U.prototype,"_addError",void 0),U=R([(0,o.EM)("esphome-secrets-structured-editor")],U),a(7405),a(4022),(0,_.C)({"code-braces":i.mdiCodeBraces,"content-save":i.mdiContentSave,eye:i.mdiEye,"eye-off":i.mdiEyeOff,"form-textbox":i.mdiFormTextbox});let K="secrets.yaml",W="esphome-secrets-layout",V=["form","yaml"];class j extends s.WF{async connectedCallback(){super.connectedCallback();let e=this._readStoredLayout();e?this._layout=e:this._seedLayoutFromBackend(),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("secrets-saved",this._onExternalSecretsSaved),await this._load.start()}_readStoredLayout(){let e=localStorage.getItem(W);return V.includes(e)?e:null}async _seedLayoutFromBackend(){try{let e=await this._api.getPreferences();null===this._readStoredLayout()&&(this._layout=(0,p.OU)(e.secrets_editor_layout))}catch(e){console.warn("Failed to load secrets layout preference:",e)}}_setLayout(e){this._layout=e,localStorage.setItem(W,e),this._api.updatePreferences({secrets_editor_layout:(0,p.aQ)(e)}).catch(e=>console.warn("Failed to persist secrets layout preference:",e))}disconnectedCallback(){window.removeEventListener("beforeunload",this._onBeforeUnload),this._unsavedGuard.cancelPending(),this._settlePendingWipe?.(!1),window.removeEventListener("secrets-saved",this._onExternalSecretsSaved),super.disconnectedCallback()}get _isDirty(){return this._yaml!==this._savedYaml}render(){let e=this._localize(this._revealSensitive?"secrets.hide_values":"secrets.reveal_values");return(0,s.qy)`
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
          ${(0,g.C)({loading:"loading"===this._load.state,loadingMessage:this._localize("secrets.loading"),loadingLead:(0,s.qy)`<wa-spinner></wa-spinner>`,error:"error"===this._load.state?this._localize("secrets.load_failed"):null,errorActions:()=>(0,s.qy)`<wa-button size="small" @click=${this._load.retry}>
                ${this._localize("command.retry")}
              </wa-button>`,content:()=>(0,s.qy)`
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
            `})}
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
    `}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_confirmWipe(){let e=this._wipeDialog;return e?new Promise(t=>{let a=a=>{e.removeEventListener("confirm",r),e.removeEventListener("cancel",i),this._settlePendingWipe=null,t(a)},r=()=>a(!0),i=()=>a(!1);this._settlePendingWipe=a,e.addEventListener("confirm",r),e.addEventListener("cancel",i),e.open()}):Promise.resolve(!1)}async _save(){if(0===q(this._yaml).length&&q(this._savedYaml).length>0&&!await this._confirmWipe())return!1;let e=""===this._yaml.trim(),t=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let a=!0,r="";try{e?await this._api.updateConfig(K,this._yaml,{allowWipe:!0}):await this._api.updateConfig(K,this._yaml)}catch(e){(e instanceof Error?e.message:"").includes("timed out")||(a=!1,this._savedYaml=t,r=(0,l.vS)(e))}finally{this._saving=!1}if(a&&window.dispatchEvent(new CustomEvent("secrets-saved",{detail:{source:this}})),a)return(0,m.VX)(this._localize("secrets.saved")),!0;let i=this._localize("secrets.save_error");return(0,m.UG)(r?`${i}: ${r}`:i),!1}constructor(...e){super(...e),this._localize=e=>e,this._apiConnected=!1,this._yaml="",this._savedYaml="",this._saving=!1,this._load=new u.r(this,{api:()=>this._api,connected:()=>this._apiConnected,configuration:()=>K,attempts:4,commit:e=>{this._yaml=e,this._savedYaml=e},onApiError:e=>e.errorCode===n.O.NOT_FOUND?{seed:this._localize("secrets.file_header")}:void 0,onRefreshFailed:()=>(0,m.UG)(this._localize("secrets.reload_failed"))}),this._revealSensitive=!1,this._layout="form",this._unsavedGuard=new A._,this._saveShortcut=new y.k(this,()=>{this._isDirty&&!this._saving&&""!==this._yaml.trim()&&this._save()}),this._leaveGuard=new v.KO(this,{confirmLeave:()=>this._confirmLeave(),isDirty:()=>this._isDirty,url:()=>"/secrets"}),this._settlePendingWipe=null,this._confirmLeave=async()=>this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:()=>this._save()}),this._onBeforeUnload=e=>{this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._onExternalSecretsSaved=e=>{e.detail?.source===this||this._yaml===this._savedYaml&&this._load.refresh()},this._onYamlChange=e=>{this._yaml=e.detail.value}}}j.styles=[h.G,c.I,O],T([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,o.wk)()],j.prototype,"_localize",void 0),T([(0,r.Fg)({context:d.Ie})],j.prototype,"_api",void 0),T([(0,r.Fg)({context:d.Lh,subscribe:!0}),(0,o.wk)()],j.prototype,"_apiConnected",void 0),T([(0,o.wk)()],j.prototype,"_yaml",void 0),T([(0,o.wk)()],j.prototype,"_savedYaml",void 0),T([(0,o.wk)()],j.prototype,"_saving",void 0),T([(0,o.wk)()],j.prototype,"_revealSensitive",void 0),T([(0,o.wk)()],j.prototype,"_layout",void 0),T([(0,o.P)("esphome-unsaved-changes-dialog")],j.prototype,"_unsavedDialog",void 0),T([(0,o.P)("esphome-confirm-dialog")],j.prototype,"_wipeDialog",void 0),j=T([(0,o.EM)("esphome-page-secrets")],j)}}]);
//# sourceMappingURL=321.dd4eff3dade3daf2.js.map