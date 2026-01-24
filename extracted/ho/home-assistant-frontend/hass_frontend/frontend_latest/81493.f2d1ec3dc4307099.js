export const __rspack_esm_id="81493";export const __rspack_esm_ids=["81493"];export const __webpack_modules__={93444(t,e,a){var o=a(62826),i=a(96196),s=a(44457);class r extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}r=(0,o.Cg)([(0,s.EM)("ha-dialog-footer")],r)},71418(t,e,a){var o=a(62826),i=a(96196),s=a(44457);a(26300),a(75709);class r extends i.WF{render(){return i.qy`<ha-textfield .invalid="${this.invalid}" .errorMessage="${this.errorMessage}" .icon="${this.icon}" .iconTrailing="${this.iconTrailing}" .autocomplete="${this.autocomplete}" .autocorrect="${this.autocorrect}" .inputSpellcheck="${this.inputSpellcheck}" .value="${this.value}" .placeholder="${this.placeholder}" .label="${this.label}" .disabled="${this.disabled}" .required="${this.required}" .minLength="${this.minLength}" .maxLength="${this.maxLength}" .outlined="${this.outlined}" .helper="${this.helper}" .validateOnInitialRender="${this.validateOnInitialRender}" .validationMessage="${this.validationMessage}" .autoValidate="${this.autoValidate}" .pattern="${this.pattern}" .size="${this.size}" .helperPersistent="${this.helperPersistent}" .charCounter="${this.charCounter}" .endAligned="${this.endAligned}" .prefix="${this.prefix}" .name="${this.name}" .inputMode="${this.inputMode}" .readOnly="${this.readOnly}" .autocapitalize="${this.autocapitalize}" .type="${this._unmaskedPassword?"text":"password"}" .suffix="${i.qy`<div style="width:24px"></div>`}" @input="${this._handleInputEvent}" @change="${this._handleChangeEvent}"></ha-textfield> <ha-icon-button .label="${this.hass?.localize(this._unmaskedPassword?"ui.components.selectors.text.hide_password":"ui.components.selectors.text.show_password")||(this._unmaskedPassword?"Hide password":"Show password")}" @click="${this._toggleUnmaskedPassword}" .path="${this._unmaskedPassword?"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z":"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"}"></ha-icon-button>`}focus(){this._textField.focus()}checkValidity(){return this._textField.checkValidity()}reportValidity(){return this._textField.reportValidity()}setCustomValidity(t){return this._textField.setCustomValidity(t)}layout(){return this._textField.layout()}_toggleUnmaskedPassword(){this._unmaskedPassword=!this._unmaskedPassword}_handleInputEvent(t){this.value=t.target.value}_handleChangeEvent(t){this.value=t.target.value,this._reDispatchEvent(t)}_reDispatchEvent(t){const e=new Event(t.type,t);this.dispatchEvent(e)}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0,this.value="",this.placeholder="",this.label="",this.disabled=!1,this.required=!1,this.minLength=-1,this.maxLength=-1,this.outlined=!1,this.helper="",this.validateOnInitialRender=!1,this.validationMessage="",this.autoValidate=!1,this.pattern="",this.size=null,this.helperPersistent=!1,this.charCounter=!1,this.endAligned=!1,this.prefix="",this.suffix="",this.name="",this.readOnly=!1,this.autocapitalize="",this._unmaskedPassword=!1}}r.styles=i.AH`:host{display:block;position:relative}ha-textfield{width:100%}ha-icon-button{position:absolute;top:8px;right:8px;inset-inline-start:initial;inset-inline-end:8px;--mdc-icon-button-size:40px;--mdc-icon-size:20px;color:var(--secondary-text-color);direction:var(--direction)}`,(0,o.Cg)([(0,s.MZ)({attribute:!1})],r.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"invalid",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"error-message"})],r.prototype,"errorMessage",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"icon",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"iconTrailing",void 0),(0,o.Cg)([(0,s.MZ)()],r.prototype,"autocomplete",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"autocorrect",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"input-spellcheck"})],r.prototype,"inputSpellcheck",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"value",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"placeholder",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"label",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],r.prototype,"disabled",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"required",void 0),(0,o.Cg)([(0,s.MZ)({type:Number})],r.prototype,"minLength",void 0),(0,o.Cg)([(0,s.MZ)({type:Number})],r.prototype,"maxLength",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],r.prototype,"outlined",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"helper",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"validateOnInitialRender",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"validationMessage",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"autoValidate",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"pattern",void 0),(0,o.Cg)([(0,s.MZ)({type:Number})],r.prototype,"size",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"helperPersistent",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"charCounter",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"endAligned",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"prefix",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"suffix",void 0),(0,o.Cg)([(0,s.MZ)({type:String})],r.prototype,"name",void 0),(0,o.Cg)([(0,s.MZ)({type:String,attribute:"input-mode"})],r.prototype,"inputMode",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],r.prototype,"readOnly",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1,type:String})],r.prototype,"autocapitalize",void 0),(0,o.Cg)([(0,s.wk)()],r.prototype,"_unmaskedPassword",void 0),(0,o.Cg)([(0,s.P)("ha-textfield")],r.prototype,"_textField",void 0),(0,o.Cg)([(0,s.Ls)({passive:!0})],r.prototype,"_handleInputEvent",null),(0,o.Cg)([(0,s.Ls)({passive:!0})],r.prototype,"_handleChangeEvent",null),r=(0,o.Cg)([(0,s.EM)("ha-password-field")],r)},45331(t,e,a){a.a(t,async function(t,e){try{var o=a(62826),i=a(93900),s=a(96196),r=a(44457),l=a(32288),n=a(1087),d=a(59992),h=a(14503),c=(a(76538),a(26300),t([i]));i=(c.then?(await c)():c)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class g extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(t){super.updated(t),t.has("open")&&(this._open=this.open)}render(){return s.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?s.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:s.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?s.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:s.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(t){this._bodyScrolled=t.target.scrollTop>0}static get styles(){return[...super.styles,h.dp,s.AH`
        wa-dialog {
          --full-width: var(
            --ha-dialog-width-full,
            min(95vw, var(--safe-width))
          );
          --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
          --spacing: var(--dialog-content-padding, var(--ha-space-6));
          --show-duration: var(--ha-dialog-show-duration, 200ms);
          --hide-duration: var(--ha-dialog-hide-duration, 200ms);
          --ha-dialog-surface-background: var(
            --card-background-color,
            var(--ha-color-surface-default)
          );
          --wa-color-surface-raised: var(
            --ha-dialog-surface-background,
            var(--card-background-color, var(--ha-color-surface-default))
          );
          --wa-panel-border-radius: var(
            --ha-dialog-border-radius,
            var(--ha-border-radius-3xl)
          );
          max-width: var(--ha-dialog-max-width, var(--safe-width));
        }
        @media (prefers-reduced-motion: reduce) {
          wa-dialog {
            --show-duration: 0ms;
            --hide-duration: 0ms;
          }
        }

        :host([width="small"]) wa-dialog {
          --width: min(var(--ha-dialog-width-sm, 320px), var(--full-width));
        }

        :host([width="large"]) wa-dialog {
          --width: min(var(--ha-dialog-width-lg, 1024px), var(--full-width));
        }

        :host([width="full"]) wa-dialog {
          --width: var(--full-width);
        }

        wa-dialog::part(dialog) {
          min-width: var(--width, var(--full-width));
          max-width: var(--width, var(--full-width));
          max-height: var(
            --ha-dialog-max-height,
            calc(var(--safe-height) - var(--ha-space-20))
          );
          min-height: var(--ha-dialog-min-height);
          margin-top: var(--dialog-surface-margin-top, auto);
          /* Used to offset the dialog from the safe areas when space is limited */
          transform: translate(
            calc(
              var(--safe-area-offset-left, 0px) - var(
                  --safe-area-offset-right,
                  0px
                )
            ),
            calc(
              var(--safe-area-offset-top, 0px) - var(
                  --safe-area-offset-bottom,
                  0px
                )
            )
          );
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          :host([type="standard"]) {
            --ha-dialog-border-radius: 0;

            wa-dialog {
              /* Make the container fill the whole screen width and not the safe width */
              --full-width: var(--ha-dialog-width-full, 100vw);
              --width: var(--full-width);
            }

            wa-dialog::part(dialog) {
              /* Make the dialog fill the whole screen height and not the safe height */
              min-height: var(--ha-dialog-min-height, 100vh);
              min-height: var(--ha-dialog-min-height, 100dvh);
              max-height: var(--ha-dialog-max-height, 100vh);
              max-height: var(--ha-dialog-max-height, 100dvh);
              margin-top: 0;
              margin-bottom: 0;
              /* Use safe area as padding instead of the container size */
              padding-top: var(--safe-area-inset-top);
              padding-bottom: var(--safe-area-inset-bottom);
              padding-left: var(--safe-area-inset-left);
              padding-right: var(--safe-area-inset-right);
              /* Reset the transform to center the dialog */
              transform: none;
            }
          }
        }

        .header-title-container {
          display: flex;
          align-items: center;
        }

        .header-title {
          margin: 0;
          margin-bottom: 0;
          color: var(--ha-dialog-header-title-color, var(--primary-text-color));
          font-size: var(
            --ha-dialog-header-title-font-size,
            var(--ha-font-size-2xl)
          );
          line-height: var(
            --ha-dialog-header-title-line-height,
            var(--ha-line-height-condensed)
          );
          font-weight: var(
            --ha-dialog-header-title-font-weight,
            var(--ha-font-weight-normal)
          );
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          margin-right: var(--ha-space-3);
        }

        wa-dialog::part(body) {
          padding: 0;
          display: flex;
          flex-direction: column;
          max-width: 100%;
          overflow: hidden;
        }

        .content-wrapper {
          position: relative;
          flex: 1;
          display: flex;
          flex-direction: column;
          min-height: 0;
        }

        .body {
          position: var(--dialog-content-position, relative);
          padding: var(
            --dialog-content-padding,
            0 var(--ha-space-6) var(--ha-space-6) var(--ha-space-6)
          );
          overflow: auto;
          flex-grow: 1;
        }
        :host([flexcontent]) .body {
          max-width: 100%;
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        wa-dialog::part(footer) {
          padding: 0;
        }

        ::slotted([slot="footer"]) {
          display: flex;
          padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4)
            var(--ha-space-4);
          gap: var(--ha-space-3);
          justify-content: flex-end;
          align-items: center;
          width: 100%;
        }
      `]}constructor(...t){super(...t),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],g.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],g.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],g.prototype,"open",void 0),(0,o.Cg)([(0,r.MZ)({reflect:!0})],g.prototype,"type",void 0),(0,o.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],g.prototype,"width",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],g.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-title"})],g.prototype,"headerTitle",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],g.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],g.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],g.prototype,"flexContent",void 0),(0,o.Cg)([(0,r.wk)()],g.prototype,"_open",void 0),(0,o.Cg)([(0,r.P)(".body")],g.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,r.wk)()],g.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,r.Ls)({passive:!0})],g.prototype,"_handleBodyScroll",null),g=(0,o.Cg)([(0,r.EM)("ha-wa-dialog")],g),e()}catch(t){e(t)}})},59992(t,e,a){a.d(e,{V:()=>n});var o=a(62826),i=a(88696),s=a(96196),r=a(94333),l=a(44457);const n=t=>{class e extends t{get scrollableElement(){return e.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(t){super.firstUpdated?.(t),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(t){super.updated?.(t),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(t=!1){return s.qy` <div class="${(0,r.H)({"fade-top":!0,rounded:t,visible:this._contentScrolled})}"></div> <div class="${(0,r.H)({"fade-bottom":!0,rounded:t,visible:this._contentScrollable})}"></div> `}static get styles(){const t=Object.getPrototypeOf(this);var e;return[...void 0===(e=t?.styles??[])?[]:Array.isArray(e)?e:[e],s.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const t=this.scrollableElement;t!==this._scrollTarget&&(this._detachScrollableElement(),t&&(this._scrollTarget=t,t.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(t),this._updateScrollableState(t)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(t){const e=parseFloat(getComputedStyle(t).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=t;this._contentScrollable=a-o>i+e+this.scrollFadeSafeAreaPadding}constructor(...t){super(...t),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=t=>{const e=t.currentTarget;this._contentScrolled=(e.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(e)},this._resize=new i.P(this,{target:null,callback:t=>{const e=t[0]?.target;e&&this._updateScrollableState(e)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return e.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],e.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],e.prototype,"_contentScrollable",void 0),e}},44244(t,e,a){a.a(t,async function(t,o){try{a.r(e);var i=a(62826),s=a(96196),r=a(44457),l=a(1087),n=(a(38962),a(18350)),d=(a(93444),a(45331)),h=(a(71418),a(31420)),c=a(14503),p=a(63993),g=t([n,d,h,p]);[n,d,h,p]=g.then?(await g)():g;class u extends s.WF{showDialog(t){this._open=!0,this._params=t}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._open&&(0,l.r)(this,"dialog-closed",{dialog:this.localName}),this._open=!1,this._params=void 0,this._encryptionKey="",this._error=""}render(){return this._params?s.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" header-title="${this.hass.localize("ui.panel.config.backup.dialogs.download.title")}" prevent-scrim-close @closed="${this._dialogClosed}"> <p> ${this.hass.localize("ui.panel.config.backup.dialogs.download.description")} </p> <p> ${this.hass.localize("ui.panel.config.backup.dialogs.download.download_backup_encrypted",{download_it_encrypted:s.qy`<button class="link" @click="${this._downloadEncrypted}"> ${this.hass.localize("ui.panel.config.backup.dialogs.download.download_it_encrypted")} </button>`})} </p> <ha-password-field .label="${this.hass.localize("ui.panel.config.backup.dialogs.download.encryption_key")}" @input="${this._keyChanged}"></ha-password-field> ${this._error?s.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:s.s6} <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${this._cancel}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._submit}"> ${this.hass.localize("ui.panel.config.backup.dialogs.download.download")} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `:s.s6}_cancel(){this.closeDialog()}async _submit(){if(""!==this._encryptionKey)try{await(0,h.Zm)(this.hass,this._params.backup.backup_id,this._agentId,this._encryptionKey),(0,p.s)(this.hass,this._params.backup.backup_id,this._agentId,this._encryptionKey),this.closeDialog()}catch(t){"password_incorrect"===t?.code?this._error=this.hass.localize("ui.panel.config.backup.dialogs.download.incorrect_encryption_key"):"decrypt_not_supported"===t?.code?this._error=this.hass.localize("ui.panel.config.backup.dialogs.download.decryption_not_supported"):alert(t.message)}}_keyChanged(t){this._encryptionKey=t.currentTarget.value,this._error=""}get _agentId(){return this._params?.agentId?this._params.agentId:(0,h.EB)(Object.keys(this._params.backup.agents))}async _downloadEncrypted(){(0,p.s)(this.hass,this._params.backup.backup_id,this._agentId),this.closeDialog()}static get styles(){return[c.RF,c.nA,s.AH`ha-wa-dialog{--dialog-content-padding:var(--ha-space-2) var(--ha-space-6)}button.link{background:0 0;border:none;padding:0;font-size:var(--ha-font-size-m);color:var(--primary-color);text-decoration:underline;cursor:pointer}`]}constructor(...t){super(...t),this._open=!1,this._encryptionKey="",this._error=""}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_open",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_params",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_encryptionKey",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_error",void 0),u=(0,i.Cg)([(0,r.EM)("ha-dialog-download-decrypted-backup")],u),o()}catch(t){o(t)}})},99793(t,e,a){a.d(e,{A:()=>o});const o=a(96196).AH`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`},93900(t,e,a){a.a(t,async function(t,e){try{var o=a(96196),i=a(44457),s=a(94333),r=a(32288),l=a(17051),n=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),g=a(97039),u=a(92070),v=a(9395),y=a(32510),f=a(17060),m=a(88496),b=a(99793),w=t([m,f]);[m,f]=w.then?(await w)():w;var _=Object.defineProperty,C=Object.getOwnPropertyDescriptor,x=(t,e,a,o)=>{for(var i,s=o>1?void 0:o?C(e,a):e,r=t.length-1;r>=0;r--)(i=t[r])&&(s=(o?i(e,a,s):i(s))||s);return o&&s&&_(e,a,s),s};let k=class extends y.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,g.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,g.I7)(this),this.removeOpenListeners()}async requestClose(t){const e=new d.L({source:t});if(this.dispatchEvent(e),e.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,g.I7)(this);const a=this.originalTrigger;"function"==typeof a?.focus&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(t){t.preventDefault(),this.dialog.classList.contains("hide")||t.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(t){const e=t.target.closest('[data-dialog="close"]');e&&(t.stopPropagation(),this.requestClose(e))}async handleDialogPointerDown(t){t.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const t=new h.k;this.dispatchEvent(t),t.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,g.JG)(this),requestAnimationFrame(()=>{const t=this.querySelector("[autofocus]");t&&"function"==typeof t.focus?t.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){const t=!this.withoutHeader,e=this.hasSlotController.test("footer");return o.qy` <dialog aria-labelledby="${this.ariaLabelledby??"title"}" aria-describedby="${(0,r.J)(this.ariaDescribedby)}" part="dialog" class="${(0,s.H)({dialog:!0,open:this.open})}" @cancel="${this.handleDialogCancel}" @click="${this.handleDialogClick}" @pointerdown="${this.handleDialogPointerDown}"> ${t?o.qy` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${this.label.length>0?this.label:String.fromCharCode(8203)} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${t=>this.requestClose(t.target)}"> <wa-icon name="xmark" label="${this.localize.term("close")}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `:""} <div part="body" class="body"><slot></slot></div> ${e?o.qy` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `:""} </dialog> `}constructor(){super(...arguments),this.localize=new f.c(this),this.hasSlotController=new u.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=t=>{"Escape"===t.key&&this.open&&(t.preventDefault(),t.stopPropagation(),this.requestClose(this.dialog))}}};k.css=b.A,x([(0,i.P)(".dialog")],k.prototype,"dialog",2),x([(0,i.MZ)({type:Boolean,reflect:!0})],k.prototype,"open",2),x([(0,i.MZ)({reflect:!0})],k.prototype,"label",2),x([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],k.prototype,"withoutHeader",2),x([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],k.prototype,"lightDismiss",2),x([(0,i.MZ)({attribute:"aria-labelledby"})],k.prototype,"ariaLabelledby",2),x([(0,i.MZ)({attribute:"aria-describedby"})],k.prototype,"ariaDescribedby",2),x([(0,v.w)("open",{waitUntilFirstUpdate:!0})],k.prototype,"handleOpenChange",1),k=x([(0,i.EM)("wa-dialog")],k),document.addEventListener("click",t=>{const e=t.target.closest("[data-dialog]");if(e instanceof Element){const[t,a]=(0,p.v)(e.getAttribute("data-dialog")||"");if("open"===t&&a?.length){const t=e.getRootNode().getElementById(a);"wa-dialog"===t?.localName?t.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),e()}catch(t){e(t)}})},91081(t,e,a){function o(t,e){return{top:Math.round(t.getBoundingClientRect().top-e.getBoundingClientRect().top),left:Math.round(t.getBoundingClientRect().left-e.getBoundingClientRect().left)}}a.d(e,{A:()=>o})},31247(t,e,a){a.d(e,{v:()=>o});a(18111),a(22489),a(61701);function o(t){return t.split(" ").map(t=>t.trim()).filter(t=>""!==t)}},97039(t,e,a){a.d(e,{I7:()=>r,JG:()=>s,Rt:()=>l});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(91081);const i=new Set;function s(t){if(i.add(t),!document.documentElement.classList.contains("wa-scroll-lock")){const t=function(){const t=document.documentElement.clientWidth;return Math.abs(window.innerWidth-t)}()+function(){const t=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(t)||!t?0:t}();let e=getComputedStyle(document.documentElement).scrollbarGutter;e&&"auto"!==e||(e="stable"),t<2&&(e=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",e),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${t}px`)}}function r(t){i.delete(t),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function l(t,e,a="vertical",i="smooth"){const s=(0,o.A)(t,e),r=s.top+e.scrollTop,l=s.left+e.scrollLeft,n=e.scrollLeft,d=e.scrollLeft+e.offsetWidth,h=e.scrollTop,c=e.scrollTop+e.offsetHeight;"horizontal"!==a&&"both"!==a||(l<n?e.scrollTo({left:l,behavior:i}):l+t.clientWidth>d&&e.scrollTo({left:l-e.offsetWidth+t.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(r<h?e.scrollTo({top:r,behavior:i}):r+t.clientHeight>c&&e.scrollTo({top:r-e.offsetHeight+t.clientHeight,behavior:i}))}}};
//# sourceMappingURL=81493.f2d1ec3dc4307099.js.map