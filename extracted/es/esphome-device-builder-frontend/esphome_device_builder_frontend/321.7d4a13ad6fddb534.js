"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[321],{3984(e,t,a){a.r(t),a.d(t,{ESPHomePageSecrets:()=>M});var i=a(9104),r=a(289),s=a(5077),o=a(9356),l=a(4342),n=a(3835),d=a(1556),c=a(4835),h=a(3140),u=a(7051),p=a(9877),v=a(1529),m=a(918),_=a(1093),g=a(3854),y=a(4818),f=a(348),b=a(9470),w=a(9808),$=a(8851);let x=/^(?:"((?:[^"\\\n]|\\.)+)"|'((?:[^'\n]|'')+)'|(<<|[A-Za-z_][A-Za-z0-9_.\-]*)):(?:[ \t]+([^\n]*))?$/;function k(e){let[,t,a,i,r]=e;return void 0!==t?{key:t,quote:'"',rest:r}:void 0!==a?{key:a,quote:"'",rest:r}:{key:i,quote:"",rest:r}}let z=/^[A-Za-z_][A-Za-z0-9_.\-]*$/,E=/^[!&*|>[{]/,S=/^[!&*|>[\]{}@`%]/;function q(e){return z.test(e)}function C(e){return""!==e&&S.test(e)?`"${(0,b.k9)(e)}"`:(0,$.Rm)(e)}function A(e){let t=e.split("\n"),a=[];for(let e=0;e<t.length;e++){let i=t[e].match(x);if(!i)continue;let{key:r,rest:s}=k(i),{value:o,editable:l}=function(e,t,a){let{value:i}=(0,w.dZ)(e??""),r=i.trim();return""===r?{value:"",editable:!function(e,t){for(let a=t+1;a<e.length;a++){let t=e[a];if(!(""===t.trim()||t.trimStart().startsWith("#")))return/^[ \t]/.test(t)}return!1}(t,a)}:E.test(r)?{value:"",editable:!1}:{value:(0,w.Ir)(r),editable:!0}}(s,t,e),n=q(r);a.push({key:r,line:e,value:n?o:"",editable:l&&n})}return a}function O(e,t,a){let i=e.split("\n"),r=i[t]?.match(x);if(!r)return null;let{key:s,quote:o,rest:l}=k(r),{value:n,comment:d}=(0,w.dZ)(l??"");return i[t]=a(s,o,n,d),i.join("\n")}var L=a(9317);let D=(0,s.AH)`
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
`;a(9577),a(9218),a(2522),a(8768);var P=a(2974),G=a(5660),Y=a(6029),F=a(9460),R=a(3330);let U=(0,s.AH)`
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
`;function T(e,t,a,i){var r,s=arguments.length,o=s<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,a):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,i);else for(var l=e.length-1;l>=0;l--)(r=e[l])&&(o=(s<3?r(o):s>3?r(t,a,o):r(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}a(1687),a(4063),a(2216),a(8944),(0,_.C)({"alert-circle-outline":r.mdiAlertCircleOutline,close:r.mdiClose,plus:r.mdiPlus});class K extends s.WF{render(){let e=A(this.value),t=function(e){let t=new Set,a=new Set;for(let{key:i}of e)t.has(i)&&a.add(i),t.add(i);return a}(e),a=function(e){let t=[],a=new Map;for(let i of e){let e=i.key.indexOf("__"),r=e>0?i.key.slice(0,e):null,s=r?(0,f.GY)(r)||r:null;a.has(s)||(a.set(s,[]),t.push(s)),a.get(s).push(i)}return(a.has(null)?[null,...t.filter(e=>null!==e)]:t).map(e=>({device:e,entries:a.get(e)}))}(e),i=a.some(e=>null!==e.device);return(0,s.qy)`
      ${0===e.length?(0,s.qy)`<div class="empty" role="status">
              ${this._localize("secrets.empty")}
            </div>`:i?(0,s.qy)`<div class="groups">
                ${a.map(a=>this._renderGroup(a,e,t))}
              </div>`:(0,s.qy)`<div class="rows">
                ${e.map(a=>this._renderRow(a,e,t))}
              </div>`}
      <div class="add-row">
        <button type="button" class="btn btn--add" @click=${this._openAdd}>
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${this._localize("secrets.add_secret")}
        </button>
      </div>
      ${this._renderAddDialog()}
    `}_renderGroup(e,t,a){return(0,s.qy)`<div class="group">
      ${this._renderGroupHeader(e.device)}
      <div class="rows">
        ${e.entries.map(e=>this._renderRow(e,t,a))}
      </div>
    </div>`}_renderGroupHeader(e){if(null===e)return(0,s.qy)`<h2 class="group-header">
        ${this._localize("secrets.group_shared")}
      </h2>`;let t=this._devices.find(t=>t.name.replace(/-/g,"_")===e.replace(/-/g,"_"));if(!t)return(0,s.qy)`<h2 class="group-header">${e}</h2>`;let a=`/device/${encodeURIComponent(t.configuration)}`,i=(0,F.cV)(a);return(0,s.qy)`<h2 class="group-header">
      <a
        href=${i}
        class="group-link"
        title=${this._localize("secrets.open_device")}
        @click=${e=>{e.metaKey||e.ctrlKey||e.shiftKey||0!==e.button||(e.preventDefault(),(0,v.oo)(a).catch(()=>window.location.assign(i)))}}
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
            .value=${(0,P.V)(this._addName)}
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
    </esphome-base-dialog>`}_renderRow(e,t,a){let i=this._keyError?.line===e.line?this._keyError?.message??null:a.has(e.key)?this._localize("secrets.duplicate_row"):null,r=null!==i,o=`key-hint-${e.line}`,l=r?(0,s.qy)`<div id=${o} class="key-error">${i}</div>`:s.s6;return e.editable?(0,s.qy)`<div class="row">
        <input
          type="text"
          class=${r?"invalid":""}
          .value=${(0,P.V)(e.key)}
          autocomplete="off"
          spellcheck="false"
          placeholder=${this._localize("secrets.key_placeholder")}
          aria-label=${this._localize("secrets.key_placeholder")}
          aria-invalid=${r?"true":"false"}
          aria-describedby=${r?o:s.s6}
          @change=${a=>this._onKeyChange(e,t,a.currentTarget)}
        />
        <esphome-password-input
          class="value-input"
          .value=${e.value}
          .revealed=${this.revealSensitive}
          label=${this._localize("secrets.value_placeholder")}
          placeholder=${this._localize("secrets.value_placeholder")}
          @password-input-change=${t=>{var a,i,r;return this._emit((a=this.value,i=e.line,r=t.detail.value,O(a,i,(e,t,a,i)=>`${t}${e}${t}: ${C(r)}${i}`)))}}
        ></esphome-password-input>
        <button
          type="button"
          class="icon-btn"
          title=${this._localize("secrets.remove_secret")}
          aria-label=${this._localize("secrets.remove_secret")}
          @click=${()=>{var t,a;let i;return this._emit((t=this.value,a=e.line,i=t.split("\n"),a<0||a>=i.length||!x.test(i[a])?null:(i.splice(a,1),i.join("\n"))))}}
        >
          <wa-icon library="mdi" name="close"></wa-icon>
        </button>
      </div>
      ${l}`:(0,s.qy)`<div class="row row--advanced">
          <input
            type="text"
            class=${r?"invalid":""}
            .value=${e.key}
            readonly
            aria-label=${this._localize("secrets.key_placeholder")}
            aria-invalid=${r?"true":"false"}
            aria-describedby=${r?o:s.s6}
          />
          <span class="advanced-badge">
            <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
            ${this._localize("secrets.advanced_badge")}
          </span>
          <span></span>
        </div>
        ${l}`}_onKeyChange(e,t,a){var i,r;let s=a.value.trim();if(s===e.key){this._keyError=null;return}if(!q(s)){this._keyError={line:e.line,message:this._localize("secrets.invalid_key")},a.value=e.key;return}if(t.some(t=>t.line!==e.line&&t.key===s)){this._keyError={line:e.line,message:this._localize("secrets.duplicate_key")},a.value=e.key;return}this._keyError=null,this._emit((i=this.value,r=e.line,O(i,r,(e,t,a,i)=>""===a?`${t}${s}${t}:${i}`:`${t}${s}${t}: ${a}${i}`)))}_addKey(){let e=this._addTarget?(0,f.GY)(this._addTarget):"",t=this._addName.trim();return e?`${e}__${t}`:t}_addKeyError(){return q(this._addName.trim())?A(this.value).some(e=>e.key===this._addKey())?this._localize("secrets.duplicate_key"):null:this._localize("secrets.invalid_key")}_emit(e){if(null===e){(0,m.UG)(this._localize("secrets.edit_out_of_sync")),this.requestUpdate();return}this._keyError=null,this.value=e,(0,R.r)(this,"yaml-change",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.value="",this.revealSensitive=!1,this._keyError=null,this._addOpen=!1,this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._openAdd=()=>{this._addTarget="",this._addName="",this._addValue="",this._addError=null,this._addOpen=!0},this._closeAdd=()=>{this._addOpen=!1},this._confirmAdd=()=>{if(!this._addOpen)return;let e=this._addKeyError();if(e){this._addError=e;return}this._addOpen=!1,this._emit(function(e,t,a){let i=`${t}: ${C(a)}`;if(""===e)return`${i}
`;let r=e.endsWith("\n")?"":"\n";return`${e}${r}${i}
`}(this.value,this._addKey(),this._addValue))}}}function V(e,t,a,i){var r,s=arguments.length,o=s<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,a):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,i);else for(var l=e.length-1;l>=0;l--)(r=e[l])&&(o=(s<3?r(o):s>3?r(t,a,o):r(t,a))||o);return s>3&&o&&Object.defineProperty(t,a,o),o}K.styles=[h.G,G.z9,Y.W,U],T([(0,i.Fg)({context:d.$F,subscribe:!0}),(0,o.wk)()],K.prototype,"_localize",void 0),T([(0,i.Fg)({context:d.xJ,subscribe:!0}),(0,o.wk)()],K.prototype,"_devices",void 0),T([(0,o.MZ)()],K.prototype,"value",void 0),T([(0,o.MZ)({type:Boolean})],K.prototype,"revealSensitive",void 0),T([(0,o.wk)()],K.prototype,"_keyError",void 0),T([(0,o.wk)()],K.prototype,"_addOpen",void 0),T([(0,o.wk)()],K.prototype,"_addTarget",void 0),T([(0,o.wk)()],K.prototype,"_addName",void 0),T([(0,o.wk)()],K.prototype,"_addValue",void 0),T([(0,o.wk)()],K.prototype,"_addError",void 0),K=T([(0,o.EM)("esphome-secrets-structured-editor")],K),a(7405),a(4022),(0,_.C)({"code-braces":r.mdiCodeBraces,"content-save":r.mdiContentSave,eye:r.mdiEye,"eye-off":r.mdiEyeOff,"form-textbox":r.mdiFormTextbox});let W="secrets.yaml",j="esphome-secrets-layout",N=["form","yaml"];class M extends s.WF{async connectedCallback(){super.connectedCallback();let e=this._readStoredLayout();e?this._layout=e:this._seedLayoutFromBackend(),window.addEventListener("beforeunload",this._onBeforeUnload),window.addEventListener("secrets-saved",this._onExternalSecretsSaved),await this._load.start()}_readStoredLayout(){let e=localStorage.getItem(j);return N.includes(e)?e:null}async _seedLayoutFromBackend(){try{let e=await this._api.getPreferences();null===this._readStoredLayout()&&(this._layout=(0,p.OU)(e.secrets_editor_layout))}catch(e){console.warn("Failed to load secrets layout preference:",e)}}_setLayout(e){this._layout=e,localStorage.setItem(j,e),this._api.updatePreferences({secrets_editor_layout:(0,p.aQ)(e)}).catch(e=>console.warn("Failed to persist secrets layout preference:",e))}disconnectedCallback(){window.removeEventListener("beforeunload",this._onBeforeUnload),this._unsavedGuard.cancelPending(),this._settlePendingWipe?.(!1),window.removeEventListener("secrets-saved",this._onExternalSecretsSaved),super.disconnectedCallback()}get _isDirty(){return this._yaml!==this._savedYaml}render(){let e=this._localize(this._revealSensitive?"secrets.hide_values":"secrets.reveal_values");return(0,s.qy)`
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
    `}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}_confirmWipe(){let e=this._wipeDialog;return e?new Promise(t=>{let a=a=>{e.removeEventListener("confirm",i),e.removeEventListener("cancel",r),this._settlePendingWipe=null,t(a)},i=()=>a(!0),r=()=>a(!1);this._settlePendingWipe=a,e.addEventListener("confirm",i),e.addEventListener("cancel",r),e.open()}):Promise.resolve(!1)}async _save(){if(0===A(this._yaml).length&&A(this._savedYaml).length>0&&!await this._confirmWipe())return!1;let e=""===this._yaml.trim(),t=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let a=!0,i="";try{e?await this._api.updateConfig(W,this._yaml,{allowWipe:!0}):await this._api.updateConfig(W,this._yaml)}catch(e){(e instanceof Error?e.message:"").includes("timed out")||(a=!1,this._savedYaml=t,i=(0,l.vS)(e))}finally{this._saving=!1}if(a&&window.dispatchEvent(new CustomEvent("secrets-saved",{detail:{source:this}})),a)return(0,m.VX)(this._localize("secrets.saved")),!0;let r=this._localize("secrets.save_error");return(0,m.UG)(i?`${r}: ${i}`:r),!1}constructor(...e){super(...e),this._localize=e=>e,this._apiConnected=!1,this._yaml="",this._savedYaml="",this._saving=!1,this._load=new u.r(this,{api:()=>this._api,connected:()=>this._apiConnected,configuration:()=>W,attempts:4,commit:e=>{this._yaml=e,this._savedYaml=e},onApiError:e=>e.errorCode===n.O.NOT_FOUND?{seed:this._localize("secrets.file_header")}:void 0,onRefreshFailed:()=>(0,m.UG)(this._localize("secrets.reload_failed"))}),this._revealSensitive=!1,this._layout="form",this._unsavedGuard=new L._,this._saveShortcut=new y.k(this,()=>{this._isDirty&&!this._saving&&""!==this._yaml.trim()&&this._save()}),this._leaveGuard=new v.KO(this,{confirmLeave:()=>this._confirmLeave(),isDirty:()=>this._isDirty,url:()=>"/secrets"}),this._settlePendingWipe=null,this._confirmLeave=async()=>this._unsavedGuard.run({dirty:this._isDirty,open:()=>this._unsavedDialog?.open(),save:()=>this._save()}),this._onBeforeUnload=e=>{this._isDirty&&(e.preventDefault(),e.returnValue="")},this._onUnsavedDiscard=()=>this._unsavedGuard.onDiscard(),this._onUnsavedSave=()=>this._unsavedGuard.onSave(),this._onUnsavedCancel=()=>this._unsavedGuard.onCancel(),this._onExternalSecretsSaved=e=>{e.detail?.source===this||this._yaml===this._savedYaml&&this._load.refresh()},this._onYamlChange=e=>{this._yaml=e.detail.value}}}M.styles=[h.G,c.I,D],V([(0,i.Fg)({context:d.$F,subscribe:!0}),(0,o.wk)()],M.prototype,"_localize",void 0),V([(0,i.Fg)({context:d.Ie})],M.prototype,"_api",void 0),V([(0,i.Fg)({context:d.Lh,subscribe:!0}),(0,o.wk)()],M.prototype,"_apiConnected",void 0),V([(0,o.wk)()],M.prototype,"_yaml",void 0),V([(0,o.wk)()],M.prototype,"_savedYaml",void 0),V([(0,o.wk)()],M.prototype,"_saving",void 0),V([(0,o.wk)()],M.prototype,"_revealSensitive",void 0),V([(0,o.wk)()],M.prototype,"_layout",void 0),V([(0,o.P)("esphome-unsaved-changes-dialog")],M.prototype,"_unsavedDialog",void 0),V([(0,o.P)("esphome-confirm-dialog")],M.prototype,"_wipeDialog",void 0),M=V([(0,o.EM)("esphome-page-secrets")],M)}}]);
//# sourceMappingURL=321.7d4a13ad6fddb534.js.map