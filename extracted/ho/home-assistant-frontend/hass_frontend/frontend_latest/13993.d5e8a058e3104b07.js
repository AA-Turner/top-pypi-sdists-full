export const __rspack_esm_id="13993";export const __rspack_esm_ids=["13993"];export const __webpack_modules__={69558(e,t,a){a.d(t,{_:()=>r});a(18111),a(7588);var o=a(96196),i=a(42017);const r=(0,i.u$)(class extends i.WL{update(e,[t,a]){return this._element&&this._element.localName===t?(a&&Object.entries(a).forEach(([e,t])=>{this._element[e]=t}),o.c0):this.render(t,a)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach(([e,t])=>{this._element[e]=t}),this._element}constructor(e){if(super(e),e.type!==i.OA.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}})},69093(e,t,a){a.d(t,{t:()=>i});var o=a(71727);const i=e=>(0,o.m)(e.entity_id)},82286(e,t,a){a.d(t,{$:()=>o});const o=(e,t)=>i(e.attributes,t),i=(e,t)=>0!==(e.supported_features&t)},93444(e,t,a){var o=a(62826),i=a(96196),r=a(97735);class s extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}s=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],s)},76538(e,t,a){var o=a(62826),i=a(96196),r=a(97735);class s extends i.WF{render(){const e=i.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=i.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return i.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?i.qy`${t}${e}`:i.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[i.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],s.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],s.prototype,"showBorder",void 0),s=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],s)},72554(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),r=a(96196),s=a(97735),n=a(32288),l=a(1087),d=a(64481),h=a(59992),c=a(14503),p=a(22348),u=(a(76538),a(26300)),m=e([i,u]);[i,u]=m.then?(await m)():m;const g="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class b extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,n.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?r.s6:r.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${g}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){const t=e.detail?.source===e.target.dialog;this.preventScrimClose&&this._escapePressed&&t&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,r.AH`
        wa-dialog {
          --full-width: var(
            --ha-dialog-width-full,
            min(95vw, var(--safe-width))
          );
          --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
          --spacing: var(--dialog-content-padding, var(--ha-space-6));
          --show-duration: var(--ha-dialog-show-duration, 200ms);
          --hide-duration: var(--ha-dialog-hide-duration, 200ms);
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

        :host([width="full"]) wa-dialog,
        :host([fullscreen]) wa-dialog {
          --width: var(--full-width);
        }

        :host([fullscreen]) wa-dialog::part(dialog) {
          min-height: var(--safe-height);
          max-height: var(--safe-height);
          margin-top: 0;
          transform: none;
        }

        :host([fullscreen]) .content-wrapper {
          overflow: hidden;
        }

        :host([fullscreen]) .body {
          overflow: hidden;
          padding: 0;
        }

        wa-dialog::part(dialog) {
          -webkit-backdrop-filter: var(
            --ha-dialog-surface-backdrop-filter,
            none
          );
          backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
          box-shadow: var(--dialog-box-shadow, var(--wa-shadow-l));
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

        wa-dialog::part(dialog)::backdrop {
          -webkit-backdrop-filter: var(
            --ha-dialog-scrim-backdrop-filter,
            var(--dialog-backdrop-filter, none)
          );
          backdrop-filter: var(
            --ha-dialog-scrim-backdrop-filter,
            var(--dialog-backdrop-filter, none)
          );
          background-color: var(--mdc-dialog-scrim-color, none);
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");return void(null!==e&&(e.id||(e.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:e.id}})))}this.querySelector("[autofocus]")?.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,l.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,l.r)(this,"closed"))}}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],b.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],b.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],b.prototype,"open",void 0),(0,o.Cg)([(0,s.MZ)({reflect:!0})],b.prototype,"type",void 0),(0,o.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],b.prototype,"width",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],b.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"header-title"})],b.prototype,"headerTitle",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],b.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],b.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],b.prototype,"flexContent",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,attribute:"without-header"})],b.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_open",void 0),(0,o.Cg)([(0,s.P)(".body")],b.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,s.Ls)({passive:!0})],b.prototype,"_handleBodyScroll",null),b=(0,o.Cg)([(0,s.EM)("ha-dialog")],b),t()}catch(e){t(e)}})},52763(e,t,a){a.a(e,async function(e,t){try{a(18111),a(7588),a(61701);var o=a(62826),i=a(96196),r=a(97735),s=a(69558),n=a(1087),l=a(38962),d=(a(11399),e([l]));l=(d.then?(await d)():d)[0];const h={boolean:()=>Promise.all([a.e("83431"),a.e("8477"),a.e("21934")]).then(a.bind(a,46990)),constant:()=>a.e("65733").then(a.bind(a,90820)),float:()=>Promise.all([a.e("31065"),a.e("17477")]).then(a.bind(a,20676)),grid:()=>a.e("60761").then(a.bind(a,70208)),expandable:()=>a.e("45001").then(a.bind(a,40003)),integer:()=>Promise.all([a.e("96261"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("8477"),a.e("21543"),a.e("81782"),a.e("36485")]).then(a.bind(a,20036)),multi_select:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("8477"),a.e("96617"),a.e("39771")]).then(a.bind(a,36182)),positive_time_period_dict:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("91576"),a.e("88995")]).then(a.bind(a,89422)),select:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("18360"),a.e("78398"),a.e("74463")]).then(a.bind(a,63804)),string:()=>Promise.all([a.e("31065"),a.e("31802")]).then(a.bind(a,54753)),optional_actions:()=>Promise.all([a.e("96261"),a.e("30628"),a.e("34995"),a.e("49373")]).then(a.bind(a,8456))},c=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null,p=(e,t)=>e&&t.name?e[t.name]:null,u=(e,t)=>e&&t.name?e[t.name]:null;class m extends i.WF{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.mN&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach(e=>{"selector"in e||h[e.type]?.()})}render(){return i.qy` <div class="root" part="root"> ${this.error&&this.error.base?i.qy` <ha-alert alert-type="error"> ${this._computeError(this.error.base,this.schema)} </ha-alert> `:""} ${this.schema.map(e=>{const t=p(this.error,e),a=u(this.warning,e);return i.qy` ${t?i.qy` <ha-alert own-margin alert-type="error"> ${this._computeError(t,e)} </ha-alert> `:a?i.qy` <ha-alert own-margin alert-type="warning"> ${this._computeWarning(a,e)} </ha-alert> `:""} ${"selector"in e?i.qy`<ha-selector .schema="${e}" .hass="${this.hass}" .narrow="${this.narrow}" .name="${e.name}" .selector="${e.selector}" .value="${c(this.data,e)}" .label="${this._computeLabel(e,this.data)}" .disabled="${e.disabled||this.disabled||!1}" .placeholder="${e.required?void 0:e.default}" .helper="${this._computeHelper(e)}" .localizeValue="${this.localizeValue}" .required="${e.required||!1}" .context="${this._generateContext(e)}"></ha-selector>`:(0,s._)(this.fieldElementName(e.type),{schema:e,data:c(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})} `})} </div> `}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...a},(0,n.r)(this,"value-changed",{value:this.data})})}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?i.qy`<ul> ${e.map(e=>i.qy`<li> ${this.computeError?this.computeError(e,t):e} </li>`)} </ul>`:this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}m.shadowRootOptions={mode:"open",delegatesFocus:!0},m.styles=i.AH`.root>*{display:block}.root>:not([own-margin]):not(:last-child){margin-bottom:24px}ha-alert[own-margin]{margin-bottom:4px}`,(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"narrow",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"data",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"schema",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"error",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"warning",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"disabled",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeError",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeWarning",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeLabel",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"computeHelper",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],m.prototype,"localizeValue",void 0),m=(0,o.Cg)([(0,r.EM)("ha-form")],m),t()}catch(e){t(e)}})},69709(e,t,a){a(18111),a(22489),a(61701),a(18237);var o=a(62826),i=a(96196),r=a(97735),s=a(1420),n=a(30015),l=a.n(n),d=a(1087),h=(a(14603),a(47566),a(98721),a(2209));let c;var p=a(996);const u=e=>i.qy`${e}`,m=new p.G(1e3),g={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class b extends i.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();m.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();m.has(e)&&((0,i.XX)(u((0,s._)(m.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,o)=>(c||(c=(0,h.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),c.renderMarkdown(e,t,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,i.XX)(u((0,s._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const a=e.firstElementChild?.firstChild?.textContent&&g.reType.exec(e.firstElementChild.firstChild.textContent);if(a){const{type:o}=a.groups,i=document.createElement("ha-alert");i.alertType=g.typeToHaAlert[o.toLowerCase()],i.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===a.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==a.input)),t.parentNode().replaceChild(i,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&a(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,d.r)(this,"content-resize")}}(0,o.Cg)([(0,r.MZ)()],b.prototype,"content",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],b.prototype,"allowSvg",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],b.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],b.prototype,"breaks",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],b.prototype,"lazyImages",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],b.prototype,"cache",void 0),b=(0,o.Cg)([(0,r.EM)("ha-markdown-element")],b)},3587(e,t,a){var o=a(62826),i=a(96196),r=a(97735);a(69709);class s extends i.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?i.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:i.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}s.styles=i.AH`
    :host {
      display: block;
    }
    ha-markdown-element {
      -ms-user-select: text;
      -webkit-user-select: text;
      -moz-user-select: text;
    }
    ha-markdown-element > *:first-child {
      margin-top: 0;
    }
    ha-markdown-element > *:last-child {
      margin-bottom: 0;
    }
    ha-alert {
      display: block;
      margin: var(--ha-space-1) 0;
    }
    a {
      color: var(--markdown-link-color, var(--primary-color));
    }
    img {
      background-color: var(--markdown-image-background-color);
      border-radius: var(--markdown-image-border-radius);
      max-width: 100%;
    }
    p:first-child > img:first-child {
      vertical-align: top;
    }
    p:first-child > img:last-child {
      vertical-align: top;
    }
    ha-markdown-element > :is(ol, ul) {
      padding-inline-start: var(--markdown-list-indent, revert);
    }
    li {
      &:has(input[type="checkbox"]) {
        list-style: none;
        & > input[type="checkbox"] {
          margin-left: 0;
        }
      }
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: var(--ha-border-radius-sm);
      color: var(--markdown-code-text-color, inherit);
    }
    code {
      font-size: var(--ha-font-size-s);
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: var(--ha-space-4);
      overflow: auto;
      line-height: var(--ha-line-height-condensed);
      font-family: var(--ha-font-family-code);
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: initial;
    }
    h2 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-bold);
    }
    hr {
      border-color: var(--divider-color);
      border-bottom: none;
      margin: var(--ha-space-4) 0;
    }
    table[role="presentation"] {
      --markdown-table-border-collapse: separate;
      --markdown-table-border-width: 0;
      --markdown-table-padding-inline: 0;
      --markdown-table-padding-block: 0;
      th,
      td {
        vertical-align: middle;
      }
    }
    table[role="presentation"] td[valign="top"],
    table[role="presentation"] th[valign="top"] {
      vertical-align: top;
    }
    table[role="presentation"] td[valign="middle"],
    table[role="presentation"] th[valign="middle"] {
      vertical-align: middle;
    }
    table[role="presentation"] td[valign="bottom"],
    table[role="presentation"] th[valign="bottom"] {
      vertical-align: bottom;
    }
    table[role="presentation"] td[valign="baseline"],
    table[role="presentation"] th[valign="baseline"] {
      vertical-align: baseline;
    }
    @supports (border-width: attr(border px, 0)) {
      table[role="presentation"] {
        --markdown-table-border-width: attr(border px, 0);
      }
      table[role="presentation"] th,
      table[role="presentation"] td {
        vertical-align: attr(valign, middle);
      }
    }
    table[role="presentation"][border="0"] {
      --markdown-table-border-width: 0;
    }
    table[role="presentation"][border="1"] {
      --markdown-table-border-width: 1px;
    }
    table[role="presentation"][border="2"] {
      --markdown-table-border-width: 2px;
    }
    table[role="presentation"][border="3"] {
      --markdown-table-border-width: 3px;
    }
    table {
      border-collapse: var(--markdown-table-border-collapse, collapse);
    }
    div:has(> table) {
      overflow: auto;
    }
    th {
      text-align: var(--markdown-table-text-align, start);
    }
    td,
    th {
      border-width: var(--markdown-table-border-width, 1px);
      border-style: var(--markdown-table-border-style, solid);
      border-color: var(--markdown-table-border-color, var(--divider-color));
      padding-inline: var(--markdown-table-padding-inline, 0.5em);
      padding-block: var(--markdown-table-padding-block, 0.25em);
    }
    blockquote {
      border-left: 4px solid var(--divider-color);
      margin-inline: 0;
      padding-inline: 1em;
    }
  `,(0,o.Cg)([(0,r.MZ)()],s.prototype,"content",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],s.prototype,"allowSvg",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],s.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"breaks",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],s.prototype,"lazyImages",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"cache",void 0),(0,o.Cg)([(0,r.P)("ha-markdown-element")],s.prototype,"_markdownElement",void 0),s=(0,o.Cg)([(0,r.EM)("ha-markdown")],s)},11399(e,t,a){a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(62826),i=a(96196),r=a(97735),s=a(22786),n=a(69558),l=a(95311);const d={action:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("39607"),a.e("25950"),a.e("46878"),a.e("69483"),a.e("29790"),a.e("78398"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("94860"),a.e("31693"),a.e("53065"),a.e("31863"),a.e("283"),a.e("30513"),a.e("7337")]).then(a.bind(a,6274)),addon:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("30329"),a.e("78398"),a.e("1398"),a.e("43305")]).then(a.bind(a,36784)),app:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("30329"),a.e("78398"),a.e("1398")]).then(a.bind(a,48585)),area:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("52710"),a.e("78398"),a.e("91012")]).then(a.bind(a,81857)),areas_display:()=>Promise.all([a.e("46095"),a.e("31065"),a.e("84510"),a.e("64135"),a.e("64280"),a.e("90363")]).then(a.bind(a,38235)),attribute:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("75091"),a.e("78398"),a.e("61173")]).then(a.bind(a,71498)),assist_pipeline:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("91133"),a.e("42791")]).then(a.bind(a,83642)),boolean:()=>Promise.all([a.e("83431"),a.e("36980"),a.e("28628")]).then(a.bind(a,30714)),choose:()=>a.e("93934").then(a.bind(a,58141)),color_rgb:()=>Promise.all([a.e("31065"),a.e("25840")]).then(a.bind(a,34931)),condition:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("25950"),a.e("46878"),a.e("98769"),a.e("78398"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("31693"),a.e("53065"),a.e("283"),a.e("27884")]).then(a.bind(a,81539)),config_entry:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("1962"),a.e("78398"),a.e("8851"),a.e("94886")]).then(a.bind(a,49347)),conversation_agent:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("19942"),a.e("25419"),a.e("73932")]).then(a.bind(a,94215)),constant:()=>a.e("77057").then(a.bind(a,39032)),country:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("72605"),a.e("62999"),a.e("78398"),a.e("70547"),a.e("18668")]).then(a.bind(a,94164)),date:()=>Promise.all([a.e("31065"),a.e("26669")]).then(a.bind(a,94351)),datetime:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("5250")]).then(a.bind(a,39045)),device:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("46878"),a.e("65273"),a.e("78398"),a.e("11679")]).then(a.bind(a,2270)),duration:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("69195"),a.e("40697")]).then(a.bind(a,79488)),entity:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("73958"),a.e("78398"),a.e("8851"),a.e("6330")]).then(a.bind(a,73863)),entity_name:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("12925"),a.e("78398"),a.e("98116")]).then(a.bind(a,7563)),statistic:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("3776"),a.e("78398"),a.e("8851"),a.e("54884"),a.e("2052")]).then(a.bind(a,28072)),file:()=>Promise.all([a.e("81407"),a.e("10523")]).then(a.bind(a,25078)),floor:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("6984"),a.e("83979"),a.e("78398"),a.e("57316"),a.e("6074")]).then(a.bind(a,9040)),label:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("62078"),a.e("78398"),a.e("66201"),a.e("90036")]).then(a.bind(a,99560)),language:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("97472"),a.e("78398"),a.e("25727")]).then(a.bind(a,15430)),navigation:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("34861"),a.e("25582"),a.e("99788"),a.e("85566"),a.e("71804"),a.e("78398"),a.e("8851"),a.e("19112"),a.e("30002"),a.e("21519"),a.e("25322"),a.e("12009"),a.e("99023"),a.e("59553"),a.e("31693"),a.e("67035"),a.e("14650")]).then(a.bind(a,58350)),number:()=>Promise.all([a.e("96261"),a.e("31065"),a.e("30628"),a.e("21543"),a.e("22933")]).then(a.bind(a,31157)),object:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("72130"),a.e("85010"),a.e("84059"),a.e("34310"),a.e("91148")]).then(a.bind(a,97951)),qr_code:()=>Promise.all([a.e("96261"),a.e("51343"),a.e("41899")]).then(a.bind(a,35313)),select:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("78398"),a.e("98444")]).then(a.bind(a,856)),selector:()=>a.e("77810").then(a.bind(a,13897)),state:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("10018"),a.e("78398"),a.e("45352")]).then(a.bind(a,12995)),backup_location:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("56235"),a.e("45009")]).then(a.bind(a,16360)),stt:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("13514"),a.e("38172")]).then(a.bind(a,42999)),target:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("95956"),a.e("30401"),a.e("78398"),a.e("8851"),a.e("19065"),a.e("24891"),a.e("12531")]).then(a.bind(a,84909)),template:()=>Promise.all([a.e("96261"),a.e("30628"),a.e("72130"),a.e("6852"),a.e("34310"),a.e("49648")]).then(a.bind(a,62166)),text:()=>Promise.all([a.e("31065"),a.e("84384")]).then(a.bind(a,47971)),time:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("35895"),a.e("34522")]).then(a.bind(a,42945)),icon:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("79581"),a.e("78398"),a.e("8851"),a.e("18844")]).then(a.bind(a,14885)),media:()=>Promise.all([a.e("3788"),a.e("99038"),a.e("83771")]).then(a.bind(a,59422)),theme:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("58276"),a.e("85212")]).then(a.bind(a,77655)),timezone:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("19180"),a.e("35540"),a.e("78398"),a.e("77070")]).then(a.bind(a,6719)),button_toggle:()=>a.e("7774").then(a.bind(a,79949)),trigger:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("25950"),a.e("46878"),a.e("30305"),a.e("78398"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("31693"),a.e("53065"),a.e("31863"),a.e("16997")]).then(a.bind(a,45078)),tts:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("80657"),a.e("56348")]).then(a.bind(a,59447)),tts_voice:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("3038"),a.e("20347"),a.e("32557")]).then(a.bind(a,41188)),location:()=>Promise.all([a.e("96261"),a.e("66139"),a.e("70622"),a.e("54083"),a.e("8851"),a.e("12122"),a.e("42001"),a.e("13112")]).then(a.bind(a,21160)),color_temp:()=>Promise.all([a.e("96261"),a.e("30628"),a.e("99788"),a.e("21543"),a.e("68506"),a.e("21519"),a.e("90764")]).then(a.bind(a,90780)),ui_action:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("92769"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("34861"),a.e("72130"),a.e("85010"),a.e("39607"),a.e("25582"),a.e("99788"),a.e("85566"),a.e("25950"),a.e("19208"),a.e("78398"),a.e("8851"),a.e("34310"),a.e("19112"),a.e("30002"),a.e("21519"),a.e("25322"),a.e("12009"),a.e("94860"),a.e("36332"),a.e("99023"),a.e("59553"),a.e("31693"),a.e("67035"),a.e("58106")]).then(a.bind(a,38389)),ui_color:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("57275"),a.e("78398"),a.e("94517")]).then(a.bind(a,52744)),ui_state_content:()=>Promise.all([a.e("96261"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("7997"),a.e("78398"),a.e("97931")]).then(a.bind(a,96074))},h=new Set(["ui-action","ui-color"]);class c extends i.WF{async focus(){await this.updateComplete,this.renderRoot.querySelector("#selector")?.focus()}get _type(){const e=Object.keys(this.selector)[0];return h.has(e)?e.replace("-","_"):e}willUpdate(e){e.has("selector")&&this.selector&&d[this._type]?.()}render(){return i.qy` ${(0,n._)(`ha-selector-${this._type}`,{hass:this.hass,narrow:this.narrow,name:this.name,selector:this._handleLegacySelector(this.selector),value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,localizeValue:this.localizeValue,id:"selector"})} `}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1,this.required=!0,this._handleLegacySelector=(0,s.A)(e=>{if("entity"in e)return(0,l.UU)(e);if("device"in e)return(0,l.tD)(e);const t=Object.keys(this.selector)[0];return h.has(t)?{[t.replace("-","_")]:e[t]}:e})}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],c.prototype,"narrow",void 0),(0,o.Cg)([(0,r.MZ)()],c.prototype,"name",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"selector",void 0),(0,o.Cg)([(0,r.MZ)()],c.prototype,"value",void 0),(0,o.Cg)([(0,r.MZ)()],c.prototype,"label",void 0),(0,o.Cg)([(0,r.MZ)()],c.prototype,"helper",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"localizeValue",void 0),(0,o.Cg)([(0,r.MZ)()],c.prototype,"placeholder",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],c.prototype,"disabled",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],c.prototype,"required",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"context",void 0),c=(0,o.Cg)([(0,r.EM)("ha-selector")],c)},95311(e,t,a){a.d(t,{DF:()=>u,Lo:()=>_,MH:()=>d,MM:()=>m,Qz:()=>p,Ru:()=>b,UU:()=>v,_7:()=>c,bZ:()=>h,m0:()=>l,tD:()=>f,vX:()=>g,wY:()=>y});a(44114),a(18111),a(22489),a(30531),a(7588),a(13579),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(44537),i=a(69093),r=a(82286),s=a(24367),n=a(28989);const l=(e,t,a,o,i,r,s)=>{const n=[],l=[],d=[];return Object.values(a).forEach(a=>{a.labels.includes(t)&&p(e,i,o,a.area_id,r,s)&&d.push(a.area_id)}),Object.values(o).forEach(a=>{a.labels.includes(t)&&u(e,Object.values(i),a,r,s)&&l.push(a.id)}),Object.values(i).forEach(a=>{a.labels.includes(t)&&m(e.states[a.entity_id],r,s)&&n.push(a.entity_id)}),{areas:d,devices:l,entities:n}},d=(e,t,a,o,i)=>{const r=[];return Object.values(a).forEach(a=>{a.floor_id===t&&p(e,e.entities,e.devices,a.area_id,o,i)&&r.push(a.area_id)}),{areas:r}},h=(e,t,a,o,i,r)=>{const s=[],n=[];return Object.values(a).forEach(a=>{a.area_id===t&&u(e,Object.values(o),a,i,r)&&n.push(a.id)}),Object.values(o).forEach(a=>{a.area_id===t&&m(e.states[a.entity_id],i,r)&&s.push(a.entity_id)}),{devices:n,entities:s}},c=(e,t,a,o,i)=>{const r=[];return Object.values(a).forEach(a=>{a.device_id===t&&m(e.states[a.entity_id],o,i)&&r.push(a.entity_id)}),{entities:r}},p=(e,t,a,o,i,r)=>!!Object.values(a).some(a=>!(a.area_id!==o||!u(e,Object.values(t),a,i,r)))||Object.values(t).some(t=>!(t.area_id!==o||!m(e.states[t.entity_id],i,r))),u=(e,t,a,i,r)=>{const s=r?(0,n.fk)(r,t):void 0;if(i.target?.device&&!(0,o.e)(i.target.device).some(e=>g(e,a,s)))return!1;if(i.target?.entity){return t.filter(e=>e.device_id===a.id).some(t=>{const a=e.states[t.entity_id];return m(a,i,r)})}return!0},m=(e,t,a)=>!!e&&(!t.target?.entity||(0,o.e)(t.target.entity).some(t=>b(t,e,a))),g=(e,t,a)=>{const{manufacturer:o,model:i,model_id:r,integration:s}=e;return(!o||t.manufacturer===o)&&((!i||t.model===i)&&((!r||t.model_id===r)&&!(s&&a&&!a?.[t.id]?.has(s))))},b=(e,t,a)=>{const{domain:s,device_class:n,supported_features:l,integration:d}=e;if(s){const e=(0,i.t)(t);if(Array.isArray(s)?!s.includes(e):e!==s)return!1}if(n){const e=t.attributes.device_class;if(e&&Array.isArray(n)?!n.includes(e):e!==n)return!1}return!(l&&!(0,o.e)(l).some(e=>(0,r.$)(t,e)))&&(!d||a?.[t.entity_id]?.domain===d)},v=e=>{if(!e.entity)return{entity:null};if("filter"in e.entity)return e;const{domain:t,integration:a,device_class:o,...i}=e.entity;return t||a||o?{entity:{...i,filter:{domain:t,integration:a,device_class:o}}}:{entity:i}},f=e=>{if(!e.device)return{device:null};if("filter"in e.device)return e;const{integration:t,manufacturer:a,model:o,...i}=e.device;return t||a||o?{device:{...i,filter:{integration:t,manufacturer:a,model:o}}}:{device:i}},_=e=>{let t;if("target"in e)t=(0,o.e)(e.target?.entity);else if("entity"in e){if(e.entity?.include_entities)return;t=(0,o.e)(e.entity?.filter)}if(!t)return;const a=t.flatMap(e=>e.integration||e.device_class||e.supported_features||!e.domain?[]:(0,o.e)(e.domain).filter(e=>(0,s.z)(e)));return[...new Set(a)]},y=(e,t,a,i,r,s={target:{}})=>{if(!t)return[];const n=new Set((0,o.e)(t.entity_id)),p=new Set((0,o.e)(t.device_id)),u=new Set((0,o.e)(t.area_id)),m=new Set((0,o.e)(t.floor_id));return new Set((0,o.e)(t.label_id)).forEach(t=>{const o=l(e,t,r,i,a,s);o.devices.forEach(e=>p.add(e)),o.entities.forEach(e=>n.add(e)),o.areas.forEach(e=>u.add(e))}),m.forEach(t=>{d(e,t,r,s).areas.forEach(e=>u.add(e))}),u.forEach(t=>{const o=h(e,t,i,a,s);o.devices.forEach(e=>p.add(e)),o.entities.forEach(e=>n.add(e))}),p.forEach(t=>{c(e,t,a,s).entities.forEach(e=>n.add(e))}),Array.from(n)}},59992(e,t,a){a.d(t,{V:()=>l});var o=a(62826),i=a(88696),r=a(96196),s=a(94333),n=a(97735);const l=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrollable",void 0),t}},24367(e,t,a){a.d(t,{L:()=>i,z:()=>r});var o=a(23832);const i=["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"],r=(0,o.g)(i)},15056(e,t,a){a.a(e,async function(e,o){try{a.r(t);var i=a(62826),r=a(96196),s=a(32288),n=a(97735),l=a(18350),d=(a(93444),a(72554)),h=a(52763),c=(a(3587),a(65829)),p=a(82e3),u=a(14503),m=e([l,d,h,c]);[l,d,h,c]=m.then?(await m)():m;let g=0;class b extends r.WF{showDialog({continueFlowId:e,mfaModuleId:t,dialogClosedCallback:a}){this._instance=g++,this._dialogClosedCallback=a,this._open=!0;const o=e?this.hass.callWS({type:"auth/setup_mfa",flow_id:e}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:t}),i=this._instance;o.then(e=>{i===this._instance&&this._processStep(e)})}closeDialog(){this._open=!1}_dialogClosed(){this._step?this._flowDone():this._resetDialogState()}render(){return void 0===this._instance?r.s6:r.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" prevent-scrim-close header-title="${this._computeStepTitle()}" @closed="${this._dialogClosed}"> <div> ${this._errorMessage?r.qy`<div class="error">${this._errorMessage}</div>`:""} ${this._step?r.qy`${"abort"===this._step.type?r.qy` <ha-markdown allow-svg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.abort.${this._step.reason}`)}"></ha-markdown>`:"create_entry"===this._step.type?r.qy`<p> ${this.hass.localize("ui.panel.profile.mfa_setup.step_done",{step:this._step.title||this._step.handler})} </p>`:"form"===this._step.type?r.qy`<ha-markdown allow-svg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.description`,this._step.description_placeholders)}"></ha-markdown> <ha-form autofocus .hass="${this.hass}" .data="${this._stepData}" .schema="${(0,p.Hg)(this._step.data_schema)}" .error="${this._step.errors}" .computeLabel="${this._computeLabel}" .computeError="${this._computeError}" @value-changed="${this._stepDataChanged}"></ha-form>`:""}`:r.qy`<div class="init-spinner"> <ha-spinner></ha-spinner> </div>`} </div> <ha-dialog-footer slot="footer"> <ha-button slot="${"form"===this._step?.type?"secondaryAction":"primaryAction"}" appearance="${(0,s.J)("form"===this._step?.type?"plain":void 0)}" @click="${this.closeDialog}">${this.hass.localize(["abort","create_entry"].includes(this._step?.type||"")?"ui.panel.profile.mfa_setup.close":"ui.common.cancel")}</ha-button> ${"form"===this._step?.type?r.qy`<ha-button slot="primaryAction" .disabled="${this._isSubmitDisabled()}" @click="${this._submitStep}">${this.hass.localize("ui.panel.profile.mfa_setup.submit")}</ha-button>`:r.s6} </ha-dialog-footer> </ha-dialog> `}static get styles(){return[u.nA,r.AH`.error{color:red}ha-markdown{--markdown-svg-background-color:white;--markdown-svg-color:black;display:block;margin:0 auto}ha-markdown a{color:var(--primary-color)}ha-markdown-element p{text-align:center}ha-markdown-element svg{display:block;margin:0 auto}ha-markdown-element code{background-color:transparent}ha-form{display:block;margin-top:var(--ha-space-4)}ha-markdown-element>:last-child{margin-bottom:revert}.init-spinner{padding:10px 100px 34px;text-align:center}`]}firstUpdated(e){super.firstUpdated(e),this.hass.loadBackendTranslation("mfa_setup","auth"),this.addEventListener("keypress",e=>{"Enter"===e.key&&this._submitStep()})}_stepDataChanged(e){this._stepData=e.detail.value}_submitStep(){if(this._isSubmitDisabled())return;this._loading=!0,this._errorMessage=void 0;const e=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then(t=>{e===this._instance&&(this._processStep(t),this._loading=!1)},e=>{this._errorMessage=e&&e.body&&e.body.message||"Unknown error occurred",this._loading=!1})}_isSubmitDisabled(){return this._loading||this._hasMissingRequiredFields()}_hasMissingRequiredFields(e=("form"===this._step?.type?this._step.data_schema:[])){for(const t of e)if("schema"in t){if(this._hasMissingRequiredFields(t.schema))return!0}else if(t.required&&void 0===t.default&&void 0===t.description?.suggested_value&&this._isEmptyValue(this._stepData[t.name]))return!0;return!1}_isEmptyValue(e){return null==e||("string"==typeof e?""===e.trim():Array.isArray(e)?0===e.length:"object"==typeof e&&0===Object.keys(e).length)}_processStep(e){e.errors||(e.errors={}),this._step=e,0===Object.keys(e.errors).length&&(this._stepData={})}_flowDone(){const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));this._dialogClosedCallback({flowFinished:e}),this._resetDialogState()}_resetDialogState(){this._errorMessage=void 0,this._step=void 0,this._stepData={},this._dialogClosedCallback=void 0,this._instance=void 0}_computeStepTitle(){return"abort"===this._step?.type?this.hass.localize("ui.panel.profile.mfa_setup.title_aborted"):"create_entry"===this._step?.type?this.hass.localize("ui.panel.profile.mfa_setup.title_success"):"form"===this._step?.type?this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.title`):""}constructor(...e){super(...e),this._loading=!1,this._open=!1,this._stepData={},this._computeLabel=e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.data.${e.name}`)||e.name,this._computeError=e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.error.${e}`)||e}}(0,i.Cg)([(0,n.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_dialogClosedCallback",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_instance",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_loading",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_open",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_stepData",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_step",void 0),(0,i.Cg)([(0,n.wk)()],b.prototype,"_errorMessage",void 0),b=(0,i.Cg)([(0,n.EM)("ha-mfa-module-setup-flow")],b),o()}catch(e){o(e)}})},996(e,t,a){a.d(t,{G:()=>o});a(45367),a(92731);class o{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},22348(e,t,a){a.d(t,{V:()=>i});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177(e,t,a){a.d(t,{n:()=>o});const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},96175(e,t,a){var o={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","30628","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","30628","34995","85545"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","30628","34995","85545"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-button-toolbar.ts":["9882","30628","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function i(e){if(!a.o(o,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=o[e],i=t[0];return Promise.all(t.slice(1).map(a.e)).then(function(){return a(i)})}i.keys=()=>Object.keys(o),i.id=96175,e.exports=i}};
//# sourceMappingURL=13993.d5e8a058e3104b07.js.map