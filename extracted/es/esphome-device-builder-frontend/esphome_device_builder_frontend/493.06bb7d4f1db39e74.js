"use strict";(globalThis.rspackChunkesphome_frontend=globalThis.rspackChunkesphome_frontend||[]).push([[493],{4148(e,a,t){t.r(a);var s=t(5172),i=t(9165),r=t(2009),o=t(3442),l=t(261),n=t(1556),d=t(3140),v=t(1093);function c(e,a,t,s){var i,r=arguments.length,o=r<3?a:null===s?s=Object.getOwnPropertyDescriptor(a,t):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,a,t,s);else for(var l=e.length-1;l>=0;l--)(i=e[l])&&(o=(r<3?i(o):r>3?i(a,t,o):i(a,t))||o);return r>3&&o&&Object.defineProperty(a,t,o),o}t(3238),t(1062),t(2202),t(6117),t(5024),(0,v.C)({"content-save":i.mdiContentSave,eye:i.mdiEye,"eye-off":i.mdiEyeOff});let h="secrets.yaml";class p extends r.WF{async connectedCallback(){super.connectedCallback(),window.addEventListener("secrets-saved",this._onExternalSecretsSaved),await this._loadFromServer()}disconnectedCallback(){window.removeEventListener("secrets-saved",this._onExternalSecretsSaved),super.disconnectedCallback()}async _loadFromServer(){try{let e=await this._api.getConfig(h);this._yaml=e,this._savedYaml=e}catch{let e=this._localize("secrets.file_header");this._yaml=e,this._savedYaml=e}this._loaded=!0}render(){let e=this._localize(this._revealSensitive?"secrets.hide_values":"secrets.reveal_values");return(0,r.qy)`
      <div class="page">
        <div class="page-header">
          <div class="page-title">
            <h1>${this._localize("secrets.title")}</h1>
            <p>${this._localize("secrets.desc")}</p>
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
        <wa-divider></wa-divider>
        <div class="editor-card">
          ${this._loaded?(0,r.qy)`
                <button
                  type="button"
                  class="save-button"
                  ?disabled=${this._saving||this._yaml===this._savedYaml||""===this._yaml.trim()}
                  @click=${this._save}
                >
                  <wa-icon library="mdi" name="content-save"></wa-icon>
                  ${this._saving?this._localize("secrets.saving"):this._localize("secrets.save")}
                </button>
                <esphome-yaml-editor
                  .value=${this._yaml}
                  .maskAllValues=${!0}
                  .revealSensitive=${this._revealSensitive}
                  @yaml-change=${e=>{this._yaml=e.detail.value}}
                ></esphome-yaml-editor>
              `:(0,r.qy)`<div class="loading"><wa-spinner></wa-spinner></div>`}
        </div>
      </div>
    `}_toggleRevealSensitive(){this._revealSensitive=!this._revealSensitive}async _save(){let e=this._savedYaml;this._savedYaml=this._yaml,this._saving=!0;let a=!0;try{await this._api.updateConfig(h,this._yaml)}catch(t){(t instanceof Error?t.message:"").includes("timed out")||(a=!1,this._savedYaml=e)}finally{this._saving=!1}a&&window.dispatchEvent(new CustomEvent("secrets-saved",{detail:{source:this}}));let t=a?"secrets.saved":"secrets.save_error";(a?l.A.success:l.A.error)(this._localize(t),{richColors:!0})}constructor(...e){super(...e),this._localize=e=>e,this._yaml="",this._savedYaml="",this._saving=!1,this._loaded=!1,this._revealSensitive=!1,this._onExternalSecretsSaved=e=>{e.detail?.source===this||this._yaml===this._savedYaml&&this._loadFromServer()}}}p.styles=[d.G,(0,r.AH)`
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
        padding: var(--wa-space-l);
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
        padding: 8px 16px;
        border-radius: var(--wa-border-radius-m);
        cursor: pointer;
        font-size: var(--wa-font-size-xs);
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

      .loading {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        color: var(--wa-color-text-quiet);
      }
    `],c([(0,s.Fg)({context:n.$F,subscribe:!0}),(0,o.wk)()],p.prototype,"_localize",void 0),c([(0,s.Fg)({context:n.Ie})],p.prototype,"_api",void 0),c([(0,o.wk)()],p.prototype,"_yaml",void 0),c([(0,o.wk)()],p.prototype,"_savedYaml",void 0),c([(0,o.wk)()],p.prototype,"_saving",void 0),c([(0,o.wk)()],p.prototype,"_loaded",void 0),c([(0,o.wk)()],p.prototype,"_revealSensitive",void 0),p=c([(0,o.EM)("esphome-page-secrets")],p),t.d(a,{ESPHomePageSecrets:()=>p})}}]);
//# sourceMappingURL=493.06bb7d4f1db39e74.js.map