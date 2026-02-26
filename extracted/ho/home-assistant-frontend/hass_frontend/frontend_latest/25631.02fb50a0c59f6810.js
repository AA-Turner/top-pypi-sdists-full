export const __rspack_esm_id="25631";export const __rspack_esm_ids=["25631"];export const __webpack_modules__={76538(e,t,a){var i=a(62826),o=a(96196),r=a(97735);class l extends o.WF{render(){const e=o.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=o.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return o.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?o.qy`${t}${e}`:o.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[o.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],l.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],l.prototype,"showBorder",void 0),l=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],l)},72554(e,t,a){a.a(e,async function(e,t){try{var i=a(62826),o=a(93900),r=a(96196),l=a(97735),d=a(32288),s=a(1087),n=a(59992),h=a(14503),c=a(22348),p=(a(76538),a(26300)),g=e([o,p]);[o,p]=g.then?(await g)():g;const f="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class u extends((0,n.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,d.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,d.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?r.s6:r.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${f}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){const t=e.detail?.source===e.target.dialog;this.preventScrimClose&&this._escapePressed&&t&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,r.AH`
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
          color: var(--primary-text-color);
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,s.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,c.V)(this.hass)){const e=this.querySelector("[autofocus]");return void(null!==e&&(e.id||(e.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:e.id}})))}this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,s.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,s.r)(this,"closed"))}}}(0,i.Cg)([(0,l.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],u.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],u.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],u.prototype,"open",void 0),(0,i.Cg)([(0,l.MZ)({reflect:!0})],u.prototype,"type",void 0),(0,i.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],u.prototype,"width",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],u.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-title"})],u.prototype,"headerTitle",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],u.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],u.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],u.prototype,"flexContent",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,attribute:"without-header"})],u.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,l.wk)()],u.prototype,"_open",void 0),(0,i.Cg)([(0,l.P)(".body")],u.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,l.wk)()],u.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,l.Ls)({passive:!0})],u.prototype,"_handleBodyScroll",null),u=(0,i.Cg)([(0,l.EM)("ha-dialog")],u),t()}catch(e){t(e)}})},11382(e,t,a){var i=a(62826),o=a(96196),r=a(97735),l=a(94333),d=a(1087),s=a(12587);a(67094);class n extends o.WF{render(){const e=this.noCollapse?o.s6:o.qy` <ha-svg-icon .path="${"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}" class="summary-icon ${(0,l.H)({expanded:this.expanded})}"></ha-svg-icon> `;return o.qy` <div class="top ${(0,l.H)({expanded:this.expanded})}"> <div id="summary" class="${(0,l.H)({noCollapse:this.noCollapse})}" @click="${this._toggleContainer}" @keydown="${this._toggleContainer}" @focus="${this._focusChanged}" @blur="${this._focusChanged}" role="button" tabindex="${this.noCollapse?-1:0}" aria-expanded="${this.expanded}" aria-controls="sect1" part="summary"> ${this.leftChevron?e:o.s6} <slot name="leading-icon"></slot> <slot name="header"> <div class="header"> ${this.header} <slot class="secondary" name="secondary">${this.secondary}</slot> </div> </slot> ${this.leftChevron?o.s6:e} <slot name="icons"></slot> </div> </div> <div class="container ${(0,l.H)({expanded:this.expanded})}" @transitionend="${this._handleTransitionEnd}" role="region" aria-labelledby="summary" aria-hidden="${!this.expanded}" tabindex="-1"> ${this._showContent?o.qy`<slot></slot>`:""} </div> `}willUpdate(e){super.willUpdate(e),e.has("expanded")&&(this._showContent=this.expanded,setTimeout(()=>{this._container.style.overflow=this.expanded?"initial":"hidden"},300))}_handleTransitionEnd(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}async _toggleContainer(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,d.r)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,s.E)());const a=this._container.scrollHeight;this._container.style.height=`${a}px`,t||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=t,(0,d.r)(this,"expanded-changed",{expanded:this.expanded})}_focusChanged(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}constructor(...e){super(...e),this.expanded=!1,this.outlined=!1,this.leftChevron=!1,this.noCollapse=!1,this._showContent=this.expanded}}n.styles=o.AH`:host{display:block}.top{display:flex;align-items:center;border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg))}.top.expanded{border-bottom-left-radius:0px;border-bottom-right-radius:0px}.top.focused{background:var(--input-fill-color)}:host([outlined]){box-shadow:none;border-width:1px;border-style:solid;border-color:var(--outline-color);border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg))}.summary-icon{transition:transform 150ms cubic-bezier(.4, 0, .2, 1);direction:var(--direction);margin-left:8px;margin-inline-start:8px;margin-inline-end:initial;border-radius:var(--ha-border-radius-circle)}#summary:focus-visible ha-svg-icon.summary-icon{background-color:var(--ha-color-fill-neutral-normal-active)}::slotted([slot=leading-icon]),:host([left-chevron]) .summary-icon{margin-left:0;margin-right:8px;margin-inline-start:0;margin-inline-end:8px}#summary{flex:1;display:flex;padding:var(--expansion-panel-summary-padding,0 8px);min-height:48px;align-items:center;cursor:pointer;overflow:hidden;font-weight:var(--ha-font-weight-medium);outline:0}#summary.noCollapse{cursor:default}.summary-icon.expanded{transform:rotate(180deg)}.header,::slotted([slot=header]){flex:1;overflow-wrap:anywhere;color:var(--primary-text-color)}.container{padding:var(--expansion-panel-content-padding,0 8px);overflow:hidden;transition:height .3s cubic-bezier(.4, 0, .2, 1);height:0px}.container.expanded{height:auto}.secondary{display:block;color:var(--secondary-text-color);font-size:var(--ha-font-size-s)}`,(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],n.prototype,"expanded",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],n.prototype,"outlined",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"left-chevron",type:Boolean,reflect:!0})],n.prototype,"leftChevron",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"no-collapse",type:Boolean,reflect:!0})],n.prototype,"noCollapse",void 0),(0,i.Cg)([(0,r.MZ)()],n.prototype,"header",void 0),(0,i.Cg)([(0,r.MZ)()],n.prototype,"secondary",void 0),(0,i.Cg)([(0,r.wk)()],n.prototype,"_showContent",void 0),(0,i.Cg)([(0,r.P)(".container")],n.prototype,"_container",void 0),n=(0,i.Cg)([(0,r.EM)("ha-expansion-panel")],n)},75709(e,t,a){a.d(t,{h:()=>n});var i=a(62826),o=a(71714),r=a(92347),l=a(96196),d=a(97735),s=a(63091);class n extends o.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const a=t?"trailing":"leading";return l.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${a}" tabindex="${t?1:-1}"> <slot name="${a}Icon"></slot> </span> `}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}n.styles=[r.R,l.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`,"rtl"===s.G.document.dir?l.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:l.AH``],(0,i.Cg)([(0,d.MZ)({type:Boolean})],n.prototype,"invalid",void 0),(0,i.Cg)([(0,d.MZ)({attribute:"error-message"})],n.prototype,"errorMessage",void 0),(0,i.Cg)([(0,d.MZ)({type:Boolean})],n.prototype,"icon",void 0),(0,i.Cg)([(0,d.MZ)({type:Boolean})],n.prototype,"iconTrailing",void 0),(0,i.Cg)([(0,d.MZ)()],n.prototype,"autocomplete",void 0),(0,i.Cg)([(0,d.MZ)({type:Boolean})],n.prototype,"autocorrect",void 0),(0,i.Cg)([(0,d.MZ)({attribute:"input-spellcheck"})],n.prototype,"inputSpellcheck",void 0),(0,i.Cg)([(0,d.P)("input")],n.prototype,"formElement",void 0),n=(0,i.Cg)([(0,d.EM)("ha-textfield")],n)},3103(e,t,a){a.a(e,async function(e,t){try{a(18111),a(22489);var i=a(62826),o=a(96196),r=a(97735),l=a(26300),d=(a(67094),a(75709),a(1087)),s=e([l]);l=(s.then?(await s)():s)[0];const n="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",h="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z";class c extends o.WF{focus(){this._input?.focus()}render(){return o.qy` <ha-textfield .autofocus="${this.autofocus}" autocomplete="off" .label="${this.label||this.hass.localize("ui.common.search")}" .value="${this.filter||""}" icon .iconTrailing="${this.filter||this.suffix}" @input="${this._filterInputChanged}"> <slot name="prefix" slot="leadingIcon"> <ha-svg-icon tabindex="-1" class="prefix" .path="${h}"></ha-svg-icon> </slot> <div class="trailing" slot="trailingIcon"> ${this.filter&&o.qy` <ha-icon-button @click="${this._clearSearch}" .label="${this.hass.localize("ui.common.clear")}" .path="${n}" class="clear-button"></ha-icon-button> `} <slot name="suffix"></slot> </div> </ha-textfield> `}async _filterChanged(e){(0,d.r)(this,"value-changed",{value:String(e)})}async _filterInputChanged(e){this._filterChanged(e.target.value)}async _clearSearch(){this._filterChanged("")}constructor(...e){super(...e),this.suffix=!1,this.autofocus=!1}}c.styles=o.AH`:host{display:inline-flex}ha-icon-button,ha-svg-icon{color:var(--primary-text-color)}ha-svg-icon{outline:0}.clear-button{--mdc-icon-size:20px}ha-textfield{display:inherit}.trailing{display:flex;align-items:center}`,(0,i.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)()],c.prototype,"filter",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],c.prototype,"suffix",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],c.prototype,"autofocus",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],c.prototype,"label",void 0),(0,i.Cg)([(0,r.P)("ha-textfield",!0)],c.prototype,"_input",void 0),c=(0,i.Cg)([(0,r.EM)("search-input")],c),t()}catch(e){t(e)}})},92158(e,t,a){a.d(t,{G:()=>r,m:()=>l});var i=a(62384),o=a(47351);const r=async e=>(0,i.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/hardware/audio",method:"get"}):(0,o.PS)(await e.callApi("GET","hassio/hardware/audio")),l=async e=>(0,i.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/hardware/info",method:"get"}):(0,o.PS)(await e.callApi("GET","hassio/hardware/info"))},59992(e,t,a){a.d(t,{V:()=>s});var i=a(62826),o=a(88696),r=a(96196),l=a(94333),d=a(97735);const s=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,l.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,l.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new o.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,d.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,d.wk)()],t.prototype,"_contentScrollable",void 0),t}},63874(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(18111),a(22489),a(61701),a(33110);var o=a(62826),r=a(53289),l=a(96196),d=a(97735),s=a(22786),n=a(1087),h=a(52220),c=(a(11382),a(43661),a(72554)),p=a(3103),g=a(47351),f=a(92158),u=a(65063),v=a(14503),m=e([c,p]);[c,p]=m.then?(await m)():m;const x=(0,s.A)((e,t,a,i)=>t.devices.filter(t=>(e||["tty","gpio","input"].includes(t.subsystem))&&(t.by_id?.toLowerCase().includes(a)||t.name.toLowerCase().includes(a)||t.dev_path.toLocaleLowerCase().includes(a)||JSON.stringify(t.attributes).toLocaleLowerCase().includes(a))).sort((e,t)=>(0,h.xL)(e.name,t.name,i)));class b extends l.WF{async showDialog(){try{this._hardware=await(0,f.m)(this.hass),this._open=!0}catch(e){await(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.hardware.available_hardware.failed_to_get"),text:(0,g.VR)(e)})}}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._open=!1,this._hardware=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._hardware)return l.s6;const e=x(this.hass.userData?.showAdvanced||!1,this._hardware,(this._filter||"").toLowerCase(),this.hass.locale.language);return l.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" flexcontent header-title="${this.hass.localize("ui.panel.config.hardware.available_hardware.title")}" @closed="${this._dialogClosed}"> <div class="content-container"> <search-input autofocus .hass="${this.hass}" .filter="${this._filter}" @value-changed="${this._handleSearchChange}" .label="${this.hass.localize("ui.panel.config.hardware.available_hardware.search")}"> </search-input> <div class="devices-container ha-scrollbar"> ${e.map(e=>l.qy` <ha-expansion-panel .header="${e.name}" .secondary="${e.by_id||void 0}" outlined> <div class="device-property"> <span> ${this.hass.localize("ui.panel.config.hardware.available_hardware.subsystem")}: </span> <span>${e.subsystem}</span> </div> <div class="device-property"> <span> ${this.hass.localize("ui.panel.config.hardware.available_hardware.device_path")}: </span> <code>${e.dev_path}</code> </div> ${e.by_id?l.qy` <div class="device-property"> <span> ${this.hass.localize("ui.panel.config.hardware.available_hardware.id")}: </span> <code>${e.by_id}</code> </div> `:l.s6} <div class="attributes"> <span> ${this.hass.localize("ui.panel.config.hardware.available_hardware.attributes")}: </span> <pre>${(0,r.dump)(e.attributes,{indent:2})}</pre> </div> </ha-expansion-panel> `)} </div> </div> </ha-dialog> `}_handleSearchChange(e){this._filter=e.detail.value}static get styles(){return[v.dp,l.AH`ha-dialog{--dialog-content-padding:0}.content-container{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden}.devices-container{padding:var(--ha-space-6);overflow-y:auto;flex:1;min-height:0}ha-expansion-panel{flex:1;margin:4px 0}code,pre{background-color:var(--markdown-code-background-color,none);border-radius:var(--ha-border-radius-sm)}pre{padding:16px;overflow:auto;line-height:var(--ha-line-height-normal);font-family:var(--ha-font-family-code)}code{font-size:var(--ha-font-size-s);padding:.2em .4em}search-input{margin:8px 16px 0;display:block}.device-property{display:flex;justify-content:space-between}.attributes{margin-top:12px}`]}constructor(...e){super(...e),this._open=!1}}(0,o.Cg)([(0,d.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.Cg)([(0,d.wk)()],b.prototype,"_hardware",void 0),(0,o.Cg)([(0,d.wk)()],b.prototype,"_filter",void 0),(0,o.Cg)([(0,d.wk)()],b.prototype,"_open",void 0),b=(0,o.Cg)([(0,d.EM)("ha-dialog-hardware-available")],b),i()}catch(e){i(e)}})},22348(e,t,a){a.d(t,{V:()=>o});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177(e,t,a){a.d(t,{n:()=>i});const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}};
//# sourceMappingURL=25631.02fb50a0c59f6810.js.map