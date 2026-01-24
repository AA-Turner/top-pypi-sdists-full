export const __rspack_esm_id="87448";export const __rspack_esm_ids=["87448"];export const __webpack_modules__={93444(e,t,a){var o=a(62826),i=a(96196),s=a(44457);class r extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}r=(0,o.Cg)([(0,s.EM)("ha-dialog-footer")],r)},45100(e,t,a){a.r(t),a.d(t,{HaIconButtonPrev:()=>l});var o=a(62826),i=a(96196),s=a(44457),r=a(63091);a(26300);class l extends i.WF{render(){return i.qy` <ha-icon-button .disabled="${this.disabled}" .label="${this.label||this.hass?.localize("ui.common.back")||"Back"}" .path="${this._icon}"></ha-icon-button> `}constructor(...e){super(...e),this.disabled=!1,this._icon="rtl"===r.G.document.dir?"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z":"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],l.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],l.prototype,"disabled",void 0),(0,o.Cg)([(0,s.MZ)()],l.prototype,"label",void 0),(0,o.Cg)([(0,s.wk)()],l.prototype,"_icon",void 0),l=(0,o.Cg)([(0,s.EM)("ha-icon-button-prev")],l)},45331(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),s=a(96196),r=a(44457),l=a(32288),n=a(1087),d=a(59992),h=a(14503),c=(a(76538),a(26300),e([i]));i=(c.then?(await c)():c)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class g extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return s.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?s.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:s.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?s.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:s.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,h.dp,s.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],g.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],g.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],g.prototype,"open",void 0),(0,o.Cg)([(0,r.MZ)({reflect:!0})],g.prototype,"type",void 0),(0,o.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],g.prototype,"width",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],g.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-title"})],g.prototype,"headerTitle",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],g.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],g.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],g.prototype,"flexContent",void 0),(0,o.Cg)([(0,r.wk)()],g.prototype,"_open",void 0),(0,o.Cg)([(0,r.P)(".body")],g.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,r.wk)()],g.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,r.Ls)({passive:!0})],g.prototype,"_handleBodyScroll",null),g=(0,o.Cg)([(0,r.EM)("ha-wa-dialog")],g),t()}catch(e){t(e)}})},59992(e,t,a){a.d(t,{V:()=>n});var o=a(62826),i=a(88696),s=a(96196),r=a(94333),l=a(44457);const n=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return s.qy` <div class="${(0,r.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,r.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],s.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t}},6891(e,t,a){a.a(e,async function(e,o){try{a.r(t);var i=a(62826),s=a(96196),r=a(44457),l=a(1087),n=a(63130),d=a(18350),h=(a(93444),a(26300),a(45100),a(45331)),c=(a(17308),a(2846),a(71418),a(31420)),p=a(14503),g=a(81619),u=e([d,h,c]);[d,h,c]=u.then?(await u)():u;const f="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",m="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z",b="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z",y=["current","new","done"];class v extends s.WF{showDialog(e){this._params=e,this._step=y[0],this._open=!0,this._newEncryptionKey=(0,c.cq)()}closeDialog(){return this._params.cancel&&this._params.cancel(),this._open&&(0,l.r)(this,"dialog-closed",{dialog:this.localName}),this._open=!1,this._step=void 0,this._params=void 0,this._newEncryptionKey=void 0,!0}_done(){this._params?.submit(!0),this.closeDialog()}_previousStep(){const e=y.indexOf(this._step);0!==e&&(this._step=y[e-1])}_nextStep(){const e=y.indexOf(this._step);e!==y.length-1&&(this._step=y[e+1])}render(){const e="current"===this._step||"new"===this._step?this.hass.localize(`ui.panel.config.backup.dialogs.change_encryption_key.${this._step}.title`):"";return s.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" header-title="${e}" prevent-scrim-close @closed="${this.closeDialog}"> ${"new"===this._step?s.qy` <ha-icon-button-prev slot="headerNavigationIcon" @click="${this._previousStep}"></ha-icon-button-prev> `:s.qy` <ha-icon-button slot="headerNavigationIcon" data-dialog="close" .label="${this.hass.localize("ui.common.close")}" .path="${f}"></ha-icon-button> `} ${this._renderStepContent()} <ha-dialog-footer slot="footer"> ${"current"===this._step?s.qy` <ha-button slot="primaryAction" @click="${this._nextStep}"> ${this.hass.localize("ui.common.next")} </ha-button> `:"new"===this._step?s.qy` <ha-button slot="primaryAction" @click="${this._submit}" .disabled="${!this._newEncryptionKey}" variant="danger"> ${this.hass.localize("ui.panel.config.backup.dialogs.change_encryption_key.actions.change")} </ha-button> `:s.qy` <ha-button slot="primaryAction" @click="${this._done}"> ${this.hass.localize("ui.panel.config.backup.dialogs.change_encryption_key.actions.done")} </ha-button> `} </ha-dialog-footer> </ha-wa-dialog> `}_renderStepContent(){switch(this._step){case"current":return s.qy` <p> ${this.hass.localize("ui.panel.config.backup.dialogs.change_encryption_key.current.description")} </p> <div class="encryption-key"> <p>${this._params?.currentKey}</p> <ha-icon-button .path="${m}" @click="${this._copyOldKeyToClipboard}"></ha-icon-button> </div> <ha-md-list> <ha-md-list-item> <span slot="headline"> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_old_emergency_kit")} </span> <span slot="supporting-text"> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_old_emergency_kit_description")} </span> <ha-button slot="end" @click="${this._downloadOld}"> <ha-svg-icon .path="${b}" slot="start"></ha-svg-icon> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_old_emergency_kit_action")} </ha-button> </ha-md-list-item> </ha-md-list> `;case"new":return s.qy` <p> ${this.hass.localize("ui.panel.config.backup.dialogs.change_encryption_key.new.description")} </p> <div class="encryption-key"> <p>${this._newEncryptionKey}</p> <ha-icon-button .path="${m}" @click="${this._copyKeyToClipboard}"></ha-icon-button> </div> <ha-md-list> <ha-md-list-item> <span slot="headline"> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_emergency_kit")} </span> <span slot="supporting-text"> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_emergency_kit_description")} </span> <ha-button slot="end" @click="${this._downloadNew}"> <ha-svg-icon .path="${b}" slot="start"></ha-svg-icon> ${this.hass.localize("ui.panel.config.backup.encryption_key.download_emergency_kit_action")} </ha-button> </ha-md-list-item> </ha-md-list> `;case"done":return s.qy` <div class="done"> <img src="/static/images/voice-assistant/hi.png" alt="Casita Home Assistant logo"> <h1> ${this.hass.localize("ui.panel.config.backup.dialogs.change_encryption_key.done.title")} </h1> </div> `}return s.s6}async _copyKeyToClipboard(){await(0,n.l)(this._newEncryptionKey,this.renderRoot.querySelector("div")),(0,g.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")})}async _copyOldKeyToClipboard(){this._params?.currentKey&&(await(0,n.l)(this._params.currentKey,this.renderRoot.querySelector("div")),(0,g.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")}))}_downloadOld(){this._params?.currentKey&&(0,c.Sx)(this.hass,this._params.currentKey,"old")}_downloadNew(){this._newEncryptionKey&&(0,c.Sx)(this.hass,this._newEncryptionKey)}async _submit(){this._newEncryptionKey&&(this._params.saveKey(this._newEncryptionKey),this._nextStep())}static get styles(){return[p.RF,p.nA,s.AH`ha-wa-dialog{--dialog-content-padding:var(--ha-space-2) var(--ha-space-6)}ha-md-list{background:0 0;--md-list-item-leading-space:0;--md-list-item-trailing-space:0}.encryption-key{border:1px solid var(--divider-color);background-color:var(--primary-background-color);border-radius:var(--ha-border-radius-md);padding:16px;display:flex;flex-direction:row;align-items:center;gap:var(--ha-space-6)}.encryption-key p{margin:0;flex:1;font-size:var(--ha-font-size-xl);font-family:var(--ha-font-family-code);font-style:normal;font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed);text-align:center}.encryption-key ha-icon-button{flex:none;margin:-16px}p{margin-top:0}.done{text-align:center}`]}constructor(...e){super(...e),this._open=!1}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],v.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],v.prototype,"_open",void 0),(0,i.Cg)([(0,r.wk)()],v.prototype,"_step",void 0),(0,i.Cg)([(0,r.wk)()],v.prototype,"_params",void 0),(0,i.Cg)([(0,r.wk)()],v.prototype,"_newEncryptionKey",void 0),v=(0,i.Cg)([(0,r.EM)("ha-dialog-change-backup-encryption-key")],v),o()}catch(e){o(e)}})},99793(e,t,a){a.d(t,{A:()=>o});const o=a(96196).AH`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`},93900(e,t,a){a.a(e,async function(e,t){try{var o=a(96196),i=a(44457),s=a(94333),r=a(32288),l=a(17051),n=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),g=a(97039),u=a(92070),f=a(9395),m=a(32510),b=a(17060),y=a(88496),v=a(99793),w=e([y,b]);[y,b]=w.then?(await w)():w;var _=Object.defineProperty,k=Object.getOwnPropertyDescriptor,x=(e,t,a,o)=>{for(var i,s=o>1?void 0:o?k(t,a):t,r=e.length-1;r>=0;r--)(i=e[r])&&(s=(o?i(t,a,s):i(s))||s);return o&&s&&_(t,a,s),s};let S=class extends m.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,g.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,g.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,g.I7)(this);const a=this.originalTrigger;"function"==typeof a?.focus&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new h.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,g.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){const e=!this.withoutHeader,t=this.hasSlotController.test("footer");return o.qy` <dialog aria-labelledby="${this.ariaLabelledby??"title"}" aria-describedby="${(0,r.J)(this.ariaDescribedby)}" part="dialog" class="${(0,s.H)({dialog:!0,open:this.open})}" @cancel="${this.handleDialogCancel}" @click="${this.handleDialogClick}" @pointerdown="${this.handleDialogPointerDown}"> ${e?o.qy` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${this.label.length>0?this.label:String.fromCharCode(8203)} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${e=>this.requestClose(e.target)}"> <wa-icon name="xmark" label="${this.localize.term("close")}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `:""} <div part="body" class="body"><slot></slot></div> ${t?o.qy` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `:""} </dialog> `}constructor(){super(...arguments),this.localize=new b.c(this),this.hasSlotController=new u.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};S.css=v.A,x([(0,i.P)(".dialog")],S.prototype,"dialog",2),x([(0,i.MZ)({type:Boolean,reflect:!0})],S.prototype,"open",2),x([(0,i.MZ)({reflect:!0})],S.prototype,"label",2),x([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],S.prototype,"withoutHeader",2),x([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],S.prototype,"lightDismiss",2),x([(0,i.MZ)({attribute:"aria-labelledby"})],S.prototype,"ariaLabelledby",2),x([(0,i.MZ)({attribute:"aria-describedby"})],S.prototype,"ariaDescribedby",2),x([(0,f.w)("open",{waitUntilFirstUpdate:!0})],S.prototype,"handleOpenChange",1),S=x([(0,i.EM)("wa-dialog")],S),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&a?.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===e?.localName?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(e){t(e)}})},91081(e,t,a){function o(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}a.d(t,{A:()=>o})},31247(e,t,a){a.d(t,{v:()=>o});a(18111),a(22489),a(61701);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},97039(e,t,a){a.d(t,{I7:()=>r,JG:()=>s,Rt:()=>l});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(91081);const i=new Set;function s(e){if(i.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function r(e){i.delete(e),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function l(e,t,a="vertical",i="smooth"){const s=(0,o.A)(e,t),r=s.top+t.scrollTop,l=s.left+t.scrollLeft,n=t.scrollLeft,d=t.scrollLeft+t.offsetWidth,h=t.scrollTop,c=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(l<n?t.scrollTo({left:l,behavior:i}):l+e.clientWidth>d&&t.scrollTo({left:l-t.offsetWidth+e.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(r<h?t.scrollTo({top:r,behavior:i}):r+e.clientHeight>c&&t.scrollTo({top:r-t.offsetHeight+e.clientHeight,behavior:i}))}}};
//# sourceMappingURL=87448.365d9f4a0ba701d6.js.map