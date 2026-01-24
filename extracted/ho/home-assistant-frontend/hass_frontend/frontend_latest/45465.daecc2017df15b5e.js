export const __rspack_esm_id="45465";export const __rspack_esm_ids=["45465"];export const __webpack_modules__={77122(e,t,i){i.a(e,async function(e,t){try{i(18111),i(22489),i(61701);var a=i(62826),o=i(96196),r=i(44457),l=i(22786),d=i(1087),n=i(78649),s=(i(85938),i(82474)),h=e([s]);s=(h.then?(await h)():h)[0];const c="M21 11H3V9H21V11M21 13H3V15H21V13Z";class p extends o.WF{render(){if(!this.hass)return o.s6;const e=this._currentEntities;return o.qy` ${this.label?o.qy`<label>${this.label}</label>`:o.s6} <ha-sortable .disabled="${!this.reorder||this.disabled}" handle-selector=".entity-handle" @item-moved="${this._entityMoved}"> <div class="list"> ${e.map(e=>o.qy` <div class="entity"> <ha-entity-picker .curValue="${e}" .hass="${this.hass}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeEntities="${this.includeEntities}" .excludeEntities="${this.excludeEntities}" .includeDeviceClasses="${this.includeDeviceClasses}" .includeUnitOfMeasurement="${this.includeUnitOfMeasurement}" .entityFilter="${this.entityFilter}" .value="${e}" .disabled="${this.disabled}" .createDomains="${this.createDomains}" @value-changed="${this._entityChanged}"></ha-entity-picker> ${this.reorder?o.qy` <ha-svg-icon class="entity-handle" .path="${c}"></ha-svg-icon> `:o.s6} </div> `)} </div> </ha-sortable> <div> <ha-entity-picker .hass="${this.hass}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeEntities="${this.includeEntities}" .excludeEntities="${this._excludeEntities(this.value,this.excludeEntities)}" .includeDeviceClasses="${this.includeDeviceClasses}" .includeUnitOfMeasurement="${this.includeUnitOfMeasurement}" .entityFilter="${this.entityFilter}" .placeholder="${this.placeholder}" .helper="${this.helper}" .disabled="${this.disabled}" .createDomains="${this.createDomains}" .required="${this.required&&!e.length}" @value-changed="${this._addEntity}" .addButton="${e.length>0}"></ha-entity-picker> </div> `}_entityMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,a=this._currentEntities,o=a[t],r=[...a];r.splice(t,1),r.splice(i,0,o),this._updateEntities(r)}get _currentEntities(){return this.value||[]}async _updateEntities(e){this.value=e,(0,d.r)(this,"value-changed",{value:e})}_entityChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,n.n)(i))return;const a=this._currentEntities;i&&!a.includes(i)?this._updateEntities(a.map(e=>e===t?i:e)):this._updateEntities(a.filter(e=>e!==t))}async _addEntity(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.reorder=!1,this._excludeEntities=(0,l.A)((e,t)=>void 0===e?t:[...t||[],...e])}}p.styles=o.AH`div{margin-top:8px}label{display:block;margin:0 0 8px}.entity{display:flex;flex-direction:row;align-items:center}.entity ha-entity-picker{flex:1}.entity-handle{padding:8px;cursor:move;cursor:grab}`,(0,a.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,a.Cg)([(0,r.MZ)({type:Array})],p.prototype,"value",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean})],p.prototype,"required",void 0),(0,a.Cg)([(0,r.MZ)()],p.prototype,"label",void 0),(0,a.Cg)([(0,r.MZ)()],p.prototype,"placeholder",void 0),(0,a.Cg)([(0,r.MZ)()],p.prototype,"helper",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"include-domains"})],p.prototype,"includeDomains",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"exclude-domains"})],p.prototype,"excludeDomains",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"include-device-classes"})],p.prototype,"includeDeviceClasses",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"include-unit-of-measurement"})],p.prototype,"includeUnitOfMeasurement",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"include-entities"})],p.prototype,"includeEntities",void 0),(0,a.Cg)([(0,r.MZ)({type:Array,attribute:"exclude-entities"})],p.prototype,"excludeEntities",void 0),(0,a.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"entityFilter",void 0),(0,a.Cg)([(0,r.MZ)({attribute:!1,type:Array})],p.prototype,"createDomains",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean})],p.prototype,"reorder",void 0),p=(0,a.Cg)([(0,r.EM)("ha-entities-picker")],p),t()}catch(e){t(e)}})},93444(e,t,i){var a=i(62826),o=i(96196),r=i(44457);class l extends o.WF{render(){return o.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[o.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}l=(0,a.Cg)([(0,r.EM)("ha-dialog-footer")],l)},76538(e,t,i){var a=i(62826),o=i(96196),r=i(44457);class l extends o.WF{render(){const e=o.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=o.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return o.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?o.qy`${t}${e}`:o.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[o.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,a.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],l.prototype,"subtitlePosition",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],l.prototype,"showBorder",void 0),l=(0,a.Cg)([(0,r.EM)("ha-dialog-header")],l)},75709(e,t,i){var a=i(62826),o=i(68846),r=i(92347),l=i(96196),d=i(44457),n=i(63091);class s extends o.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const i=t?"trailing":"leading";return l.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${t?1:-1}"> <slot name="${i}Icon"></slot> </span> `}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}s.styles=[r.R,l.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`,"rtl"===n.G.document.dir?l.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:l.AH``],(0,a.Cg)([(0,d.MZ)({type:Boolean})],s.prototype,"invalid",void 0),(0,a.Cg)([(0,d.MZ)({attribute:"error-message"})],s.prototype,"errorMessage",void 0),(0,a.Cg)([(0,d.MZ)({type:Boolean})],s.prototype,"icon",void 0),(0,a.Cg)([(0,d.MZ)({type:Boolean})],s.prototype,"iconTrailing",void 0),(0,a.Cg)([(0,d.MZ)()],s.prototype,"autocomplete",void 0),(0,a.Cg)([(0,d.MZ)({type:Boolean})],s.prototype,"autocorrect",void 0),(0,a.Cg)([(0,d.MZ)({attribute:"input-spellcheck"})],s.prototype,"inputSpellcheck",void 0),(0,a.Cg)([(0,d.P)("input")],s.prototype,"formElement",void 0),s=(0,a.Cg)([(0,d.EM)("ha-textfield")],s)},45331(e,t,i){i.a(e,async function(e,t){try{var a=i(62826),o=i(93900),r=i(96196),l=i(44457),d=i(32288),n=i(1087),s=i(59992),h=i(14503),c=(i(76538),i(26300),e([o]));o=(c.then?(await c)():c)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class g extends((0,s.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,d.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,d.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,h.dp,r.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}(0,a.Cg)([(0,l.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,a.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],g.prototype,"ariaLabelledBy",void 0),(0,a.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],g.prototype,"ariaDescribedBy",void 0),(0,a.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],g.prototype,"open",void 0),(0,a.Cg)([(0,l.MZ)({reflect:!0})],g.prototype,"type",void 0),(0,a.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],g.prototype,"width",void 0),(0,a.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],g.prototype,"preventScrimClose",void 0),(0,a.Cg)([(0,l.MZ)({attribute:"header-title"})],g.prototype,"headerTitle",void 0),(0,a.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],g.prototype,"headerSubtitle",void 0),(0,a.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],g.prototype,"headerSubtitlePosition",void 0),(0,a.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],g.prototype,"flexContent",void 0),(0,a.Cg)([(0,l.wk)()],g.prototype,"_open",void 0),(0,a.Cg)([(0,l.P)(".body")],g.prototype,"bodyContainer",void 0),(0,a.Cg)([(0,l.wk)()],g.prototype,"_bodyScrolled",void 0),(0,a.Cg)([(0,l.Ls)({passive:!0})],g.prototype,"_handleBodyScroll",null),g=(0,a.Cg)([(0,l.EM)("ha-wa-dialog")],g),t()}catch(e){t(e)}})},284(e,t,i){i.a(e,async function(e,a){try{i.r(t),i.d(t,{DialogEditHome:()=>g});var o=i(62826),r=i(96196),l=i(44457),d=i(1087),n=i(77122),s=(i(38962),i(18350)),h=(i(93444),i(45331)),c=i(14503),p=e([n,s,h]);[n,s,h]=p.then?(await p)():p;class g extends r.WF{showDialog(e){this._params=e,this._config={...e.config},this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._params=void 0,this._config=void 0,this._submitting=!1,(0,d.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params?r.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" .headerTitle="${this.hass.localize("ui.panel.home.editor.title")}" @closed="${this._dialogClosed}"> <p class="description"> ${this.hass.localize("ui.panel.home.editor.description")} </p> <ha-entities-picker autofocus .hass="${this.hass}" .value="${this._config?.favorite_entities||[]}" .label="${this.hass.localize("ui.panel.lovelace.editor.strategy.home.favorite_entities")}" .placeholder="${this.hass.localize("ui.panel.lovelace.editor.strategy.home.add_favorite_entity")}" .helper="${this.hass.localize("ui.panel.home.editor.favorite_entities_helper")}" reorder @value-changed="${this._favoriteEntitiesChanged}"></ha-entities-picker> <ha-alert alert-type="info"> ${this.hass.localize("ui.panel.home.editor.areas_hint",{areas_page:r.qy`<a href="/config/areas?historyBack=1" @click="${this.closeDialog}">${this.hass.localize("ui.panel.home.editor.areas_page")}</a>`})} </ha-alert> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${this.closeDialog}" .disabled="${this._submitting}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._save}" .disabled="${this._submitting}"> ${this.hass.localize("ui.common.save")} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `:r.s6}_favoriteEntitiesChanged(e){const t=e.detail.value;this._config={...this._config,favorite_entities:t.length>0?t:void 0}}async _save(){if(this._params&&this._config){this._submitting=!0;try{await this._params.saveConfig(this._config),this.closeDialog()}catch(e){console.error("Failed to save home configuration:",e)}finally{this._submitting=!1}}}constructor(...e){super(...e),this._open=!1,this._submitting=!1}}g.styles=[c.nA,r.AH`ha-wa-dialog{--dialog-content-padding:var(--ha-space-6)}.description{margin:0 0 var(--ha-space-4) 0;color:var(--secondary-text-color)}ha-entities-picker{display:block}ha-alert{display:block;margin-top:var(--ha-space-4)}`],(0,o.Cg)([(0,l.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.Cg)([(0,l.wk)()],g.prototype,"_params",void 0),(0,o.Cg)([(0,l.wk)()],g.prototype,"_config",void 0),(0,o.Cg)([(0,l.wk)()],g.prototype,"_open",void 0),(0,o.Cg)([(0,l.wk)()],g.prototype,"_submitting",void 0),g=(0,o.Cg)([(0,l.EM)("dialog-edit-home")],g),a()}catch(e){a(e)}})},85614(e,t,i){i.d(t,{i:()=>a});const a=async()=>{await Promise.all([i.e("22564"),i.e("22309")]).then(i.bind(i,42735))}},22348(e,t,i){i.d(t,{V:()=>o});var a=i(37177);const o=e=>!!e.auth.external&&a.n},37177(e,t,i){i.d(t,{n:()=>a});const a=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}};
//# sourceMappingURL=45465.daecc2017df15b5e.js.map