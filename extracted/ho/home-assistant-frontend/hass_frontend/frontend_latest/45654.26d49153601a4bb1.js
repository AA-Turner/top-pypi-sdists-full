/*! For license information please see 45654.26d49153601a4bb1.js.LICENSE.txt */
export const __rspack_esm_id="45654";export const __rspack_esm_ids=["45654"];export const __webpack_modules__={93444(e,t,a){var o=a(62826),i=a(96196),s=a(97735);class r extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}r=(0,o.Cg)([(0,s.EM)("ha-dialog-footer")],r)},76538(e,t,a){var o=a(62826),i=a(96196),s=a(97735);class r extends i.WF{render(){const e=i.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=i.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return i.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?i.qy`${t}${e}`:i.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[i.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,s.MZ)({type:String,attribute:"subtitle-position"})],r.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],r.prototype,"showBorder",void 0),r=(0,o.Cg)([(0,s.EM)("ha-dialog-header")],r)},72554(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),s=a(96196),r=a(97735),l=a(32288),n=a(1087),d=a(59992),h=a(14503),c=a(22348),p=(a(76538),a(26300)),u=e([i,p]);[i,p]=u.then?(await u)():u;const g="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class m extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return s.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?s.s6:s.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${g}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?s.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:s.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?s.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:s.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){const t=e.detail?.source===e.target.dialog;this.preventScrimClose&&this._escapePressed&&t&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,s.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,c.V)(this.hass)){const e=this.querySelector("[autofocus]");return void(null!==e&&(e.id||(e.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:e.id}})))}this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,n.r)(this,"closed"))}}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],m.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],m.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],m.prototype,"open",void 0),(0,o.Cg)([(0,r.MZ)({reflect:!0})],m.prototype,"type",void 0),(0,o.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],m.prototype,"width",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],m.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-title"})],m.prototype,"headerTitle",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],m.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],m.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],m.prototype,"flexContent",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"without-header"})],m.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,r.wk)()],m.prototype,"_open",void 0),(0,o.Cg)([(0,r.P)(".body")],m.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,r.wk)()],m.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,r.Ls)({passive:!0})],m.prototype,"_handleBodyScroll",null),m=(0,o.Cg)([(0,r.EM)("ha-dialog")],m),t()}catch(e){t(e)}})},52763(e,t,a){a.a(e,async function(e,o){try{a.d(t,{U:()=>m});a(18111),a(7588),a(61701);var i=a(62826),s=a(96196),r=a(97735),l=a(69558),n=a(1087),d=a(38962),h=(a(11399),e([d]));d=(h.then?(await h)():h)[0];const c={boolean:()=>Promise.all([a.e("83431"),a.e("8477"),a.e("21934")]).then(a.bind(a,46990)),constant:()=>a.e("65733").then(a.bind(a,90820)),float:()=>Promise.all([a.e("31065"),a.e("17477")]).then(a.bind(a,20676)),grid:()=>a.e("60761").then(a.bind(a,70208)),expandable:()=>a.e("45001").then(a.bind(a,40003)),integer:()=>Promise.all([a.e("96261"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("8477"),a.e("21543"),a.e("81782"),a.e("36485")]).then(a.bind(a,20036)),multi_select:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("8477"),a.e("96617"),a.e("39771")]).then(a.bind(a,36182)),positive_time_period_dict:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("91576"),a.e("88995")]).then(a.bind(a,89422)),select:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("18360"),a.e("78398"),a.e("74463")]).then(a.bind(a,63804)),string:()=>Promise.all([a.e("31065"),a.e("31802")]).then(a.bind(a,54753)),optional_actions:()=>Promise.all([a.e("96261"),a.e("30628"),a.e("34995"),a.e("49373")]).then(a.bind(a,8456))},p=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null,u=(e,t)=>e&&t.name?e[t.name]:null,g=(e,t)=>e&&t.name?e[t.name]:null;class m extends s.WF{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof s.mN&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach(e=>{"selector"in e||c[e.type]?.()})}render(){return s.qy` <div class="root" part="root"> ${this.error&&this.error.base?s.qy` <ha-alert alert-type="error"> ${this._computeError(this.error.base,this.schema)} </ha-alert> `:""} ${this.schema.map(e=>{const t=u(this.error,e),a=g(this.warning,e);return s.qy` ${t?s.qy` <ha-alert own-margin alert-type="error"> ${this._computeError(t,e)} </ha-alert> `:a?s.qy` <ha-alert own-margin alert-type="warning"> ${this._computeWarning(a,e)} </ha-alert> `:""} ${"selector"in e?s.qy`<ha-selector .schema="${e}" .hass="${this.hass}" .narrow="${this.narrow}" .name="${e.name}" .selector="${e.selector}" .value="${p(this.data,e)}" .label="${this._computeLabel(e,this.data)}" .disabled="${e.disabled||this.disabled||!1}" .placeholder="${e.required?void 0:e.default}" .helper="${this._computeHelper(e)}" .localizeValue="${this.localizeValue}" .required="${e.required||!1}" .context="${this._generateContext(e)}"></ha-selector>`:(0,l._)(this.fieldElementName(e.type),{schema:e,data:p(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})} `})} </div> `}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...a},(0,n.r)(this,"value-changed",{value:this.data})})}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?s.qy`<ul> ${e.map(e=>s.qy`<li> ${this.computeError?this.computeError(e,t):e} </li>`)} </ul>`:this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}m.shadowRootOptions={mode:"open",delegatesFocus:!0},m.styles=s.AH`.root>*{display:block}.root>:not([own-margin]):not(:last-child){margin-bottom:24px}ha-alert[own-margin]{margin-bottom:4px}`,(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"narrow",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"data",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"schema",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"error",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"warning",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"disabled",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeError",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeWarning",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeLabel",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeHelper",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"localizeValue",void 0),m=(0,i.Cg)([(0,r.EM)("ha-form")],m),o()}catch(e){o(e)}})},87285(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{DialogForm:()=>u});var i=a(62826),s=a(96196),r=a(97735),l=a(1087),n=a(18350),d=a(52763),h=(a(93444),a(72554)),c=a(14503),p=e([n,d,h]);[n,d,h]=p.then?(await p)():p;class u extends s.WF{async showDialog(e){this._params=e,this._data=e.data||{},this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._closeState||this._params?.cancel?.(),this._closeState=void 0,this._params=void 0,this._data={},this._open=!1,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}_submit(){this._closeState="submitted",this._params?.submit?.(this._data),this.closeDialog()}_cancel(){this._closeState="canceled",this._params?.cancel?.(),this.closeDialog()}_valueChanged(e){this._data=e.detail.value}render(){return this._params&&this.hass?s.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" header-title="${this._params.title}" prevent-scrim-close @closed="${this._dialogClosed}"> <ha-form autofocus .hass="${this.hass}" .computeLabel="${this._params.computeLabel}" .computeHelper="${this._params.computeHelper}" .data="${this._data}" .schema="${this._params.schema}" @value-changed="${this._valueChanged}"> </ha-form> <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${this._cancel}"> ${this._params.cancelText||this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._submit}"> ${this._params.submitText||this.hass.localize("ui.common.save")} </ha-button> </ha-dialog-footer> </ha-dialog> `:s.s6}constructor(...e){super(...e),this._data={},this._open=!1}}u.styles=[c.nA,s.AH``],(0,i.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_params",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_data",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_open",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_closeState",void 0),u=(0,i.Cg)([(0,r.EM)("dialog-form")],u),o()}catch(e){o(e)}})},59992(e,t,a){a.d(t,{V:()=>n});var o=a(62826),i=a(88696),s=a(96196),r=a(94333),l=a(97735);const n=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return s.qy` <div class="${(0,r.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,r.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],s.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t}},22348(e,t,a){a.d(t,{V:()=>i});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177(e,t,a){a.d(t,{n:()=>o});const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},93900(e,t,a){a.a(e,async function(e,t){try{var o=a(96196),i=a(97735),s=a(94333),r=a(32288),l=a(17051),n=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),u=a(93949),g=a(92070),m=a(9395),f=a(12754),v=a(17060),b=a(88496),w=a(91470),y=e([b,v]);[b,v]=y.then?(await y)():y;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,C=(e,t,a,o)=>{for(var i,s=o>1?void 0:o?x(t,a):t,r=e.length-1;r>=0;r--)(i=e[r])&&(s=(o?i(t,a,s):i(s))||s);return o&&s&&_(t,a,s),s};let $=class extends f.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,u.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,u.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,u.I7)(this);const a=this.originalTrigger;"function"==typeof a?.focus&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new h.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,u.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){const e=!this.withoutHeader,t=this.hasSlotController.test("footer");return o.qy` <dialog aria-labelledby="${this.ariaLabelledby??"title"}" aria-describedby="${(0,r.J)(this.ariaDescribedby)}" part="dialog" class="${(0,s.H)({dialog:!0,open:this.open})}" @cancel="${this.handleDialogCancel}" @click="${this.handleDialogClick}" @pointerdown="${this.handleDialogPointerDown}"> ${e?o.qy` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${this.label.length>0?this.label:String.fromCharCode(8203)} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${e=>this.requestClose(e.target)}"> <wa-icon name="xmark" label="${this.localize.term("close")}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `:""} <div part="body" class="body"><slot></slot></div> ${t?o.qy` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `:""} </dialog> `}constructor(){super(...arguments),this.localize=new v.c(this),this.hasSlotController=new g.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};$.css=w.A,C([(0,i.P)(".dialog")],$.prototype,"dialog",2),C([(0,i.MZ)({type:Boolean,reflect:!0})],$.prototype,"open",2),C([(0,i.MZ)({reflect:!0})],$.prototype,"label",2),C([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],$.prototype,"withoutHeader",2),C([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],$.prototype,"lightDismiss",2),C([(0,i.MZ)({attribute:"aria-labelledby"})],$.prototype,"ariaLabelledby",2),C([(0,i.MZ)({attribute:"aria-describedby"})],$.prototype,"ariaDescribedby",2),C([(0,m.w)("open",{waitUntilFirstUpdate:!0})],$.prototype,"handleOpenChange",1),$=C([(0,i.EM)("wa-dialog")],$),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&a?.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===e?.localName?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(e){t(e)}})},91470(e,t,a){a.d(t,{A:()=>o});var o=a(96196).AH`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`},31247(e,t,a){a.d(t,{v:()=>o});a(18111),a(22489),a(61701);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},93949(e,t,a){a.d(t,{Rt:()=>r,I7:()=>s,JG:()=>i});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);const o=new Set;function i(e){if(o.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function s(e){o.delete(e),0===o.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function r(e,t,a="vertical",o="smooth"){const i=function(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}(e,t),s=i.top+t.scrollTop,r=i.left+t.scrollLeft,l=t.scrollLeft,n=t.scrollLeft+t.offsetWidth,d=t.scrollTop,h=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(r<l?t.scrollTo({left:r,behavior:o}):r+e.clientWidth>n&&t.scrollTo({left:r-t.offsetWidth+e.clientWidth,behavior:o})),"vertical"!==a&&"both"!==a||(s<d?t.scrollTo({top:s,behavior:o}):s+e.clientHeight>h&&t.scrollTo({top:s-t.offsetHeight+e.clientHeight,behavior:o}))}},88696(e,t,a){a.d(t,{P:()=>s});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(37540),i=a(42017);class s{handleChanges(e){this.value=this.callback?.(e,this.u)}hostConnected(){for(const e of this.t)this.observe(e)}hostDisconnected(){this.disconnect()}async hostUpdated(){!this.o&&this.i&&this.handleChanges([]),this.i=!1}observe(e){this.t.add(e),this.u.observe(e,this.l),this.i=!0,this.h.requestUpdate()}unobserve(e){this.t.delete(e),this.u.unobserve(e)}disconnect(){this.u.disconnect()}target(e){return r(this,e)}constructor(e,{target:t,config:a,callback:o,skipInitial:i}){this.t=new Set,this.o=!1,this.i=!1,this.h=e,null!==t&&this.t.add(t??e),this.l=a,this.o=i??this.o,this.callback=o,window.ResizeObserver?(this.u=new ResizeObserver(e=>{this.handleChanges(e),this.h.requestUpdate()}),e.addController(this)):console.warn("ResizeController error: browser does not support ResizeObserver.")}}const r=(0,i.u$)(class extends o.Kq{render(e,t){}update(e,[t,a]){this.controller=t,this.part=e,this.observe=a,!1===a?(t.unobserve(e.element),this.observing=!1):!1===this.observing&&(t.observe(e.element),this.observing=!0)}disconnected(){this.controller?.unobserve(this.part.element),this.observing=!1}reconnected(){!1!==this.observe&&!1===this.observing&&(this.controller?.observe(this.part.element),this.observing=!0)}constructor(){super(...arguments),this.observing=!1}})},37540(e,t,a){a.d(t,{Kq:()=>c});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(63937),i=a(42017);const s=(e,t)=>{const a=e._$AN;if(void 0===a)return!1;for(const e of a)e._$AO?.(t,!1),s(e,t);return!0},r=e=>{let t,a;do{if(void 0===(t=e._$AM))break;a=t._$AN,a.delete(e),e=t}while(0===a?.size)},l=e=>{for(let t;t=e._$AM;e=t){let a=t._$AN;if(void 0===a)t._$AN=a=new Set;else if(a.has(e))break;a.add(e),h(t)}};function n(e){void 0!==this._$AN?(r(this),this._$AM=e,l(this)):this._$AM=e}function d(e,t=!1,a=0){const o=this._$AH,i=this._$AN;if(void 0!==i&&0!==i.size)if(t)if(Array.isArray(o))for(let e=a;e<o.length;e++)s(o[e],!1),r(o[e]);else null!=o&&(s(o,!1),r(o));else s(this,e)}const h=e=>{e.type==i.OA.CHILD&&(e._$AP??=d,e._$AQ??=n)};class c extends i.WL{_$AT(e,t,a){super._$AT(e,t,a),l(this),this.isConnected=e._$AU}_$AO(e,t=!0){e!==this.isConnected&&(this.isConnected=e,e?this.reconnected?.():this.disconnected?.()),t&&(s(this,e),r(this))}setValue(e){if((0,o.Rt)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}constructor(){super(...arguments),this._$AN=void 0}}}};
//# sourceMappingURL=45654.26d49153601a4bb1.js.map