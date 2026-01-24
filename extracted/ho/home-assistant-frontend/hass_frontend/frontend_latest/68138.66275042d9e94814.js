/*! For license information please see 68138.66275042d9e94814.js.LICENSE.txt */
export const __rspack_esm_id="68138";export const __rspack_esm_ids=["68138"];export const __webpack_modules__={69093(t,e,a){a.d(e,{t:()=>r});var o=a(71727);const r=t=>(0,o.m)(t.entity_id)},82286(t,e,a){a.d(e,{$:()=>o});const o=(t,e)=>r(t.attributes,e),r=(t,e)=>0!==(t.supported_features&e)},72554(t,e,a){a.d(e,{l:()=>c});var o=a(62826),r=a(30728),n=a(47705),i=a(96196),s=a(44457);a(22444),a(26300);const l=["button","ha-list-item"],c=(t,e)=>i.qy` <div class="header_title"> <ha-icon-button .label="${t?.localize("ui.common.close")??"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> <span>${e}</span> </div> `;class d extends r.u{scrollToPos(t,e){this.contentElement?.scrollTo(t,e)}renderHeading(){return i.qy`<slot name="heading"> ${super.renderHeading()} </slot>`}firstUpdated(){super.firstUpdated(),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,l].join(", "),this._updateScrolledAttribute(),this.contentElement?.addEventListener("scroll",this._onScroll,{passive:!0})}disconnectedCallback(){super.disconnectedCallback(),this.contentElement.removeEventListener("scroll",this._onScroll)}_updateScrolledAttribute(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}constructor(...t){super(...t),this._onScroll=()=>{this._updateScrolledAttribute()}}}d.styles=[n.R,i.AH`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:var(--ha-font-weight-normal);--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding:var(--ha-space-3) var(--ha-space-4) var(--ha-space-4) var(--ha-space-4)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center);padding:var(--dialog-container-padding,0)}.mdc-dialog__title{padding:var(--ha-space-4) var(--ha-space-4) 0 var(--ha-space-4)}.mdc-dialog__title:has(span){padding:var(--ha-space-3) var(--ha-space-3) 0}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,var(--ha-space-6))}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:var(--dialog-content-padding,var(--ha-space-6))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-width:var(--mdc-dialog-min-width,auto);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,var(--ha-border-radius-3xl));-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff));padding:var(--dialog-surface-padding,0)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{display:flex;align-items:center;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block;padding-left:var(--ha-space-1);padding-right:var(--ha-space-1);margin-right:var(--ha-space-3);margin-inline-end:var(--ha-space-3);margin-inline-start:initial}.header_button{text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:calc(var(--ha-space-3) * -1);direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0!important;direction:var(--direction)}`],d=(0,o.Cg)([(0,s.EM)("ha-dialog")],d)},69709(t,e,a){a(18111),a(22489),a(61701),a(18237);var o=a(62826),r=a(96196),n=a(44457),i=a(1420),s=a(30015),l=a.n(s),c=a(1087),d=(a(14603),a(47566),a(98721),a(2209));let h;var p=a(996);const u=t=>r.qy`${t}`,g=new p.G(1e3),m={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class v extends r.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const t=this._computeCacheKey();g.set(t,this.innerHTML)}}createRenderRoot(){return this}update(t){super.update(t),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(t){if(!this.innerHTML&&this.cache){const t=this._computeCacheKey();g.has(t)&&((0,r.XX)(u((0,i._)(g.get(t))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const t=await(async(t,e,o)=>(h||(h=(0,d.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),h.renderMarkdown(t,e,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,r.XX)(u((0,i._)(t.join(""))),this.renderRoot),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const t=e.currentNode;if(t instanceof HTMLAnchorElement&&t.host!==document.location.host)t.target="_blank",t.rel="noreferrer noopener";else if(t instanceof HTMLImageElement)this.lazyImages&&(t.loading="lazy"),t.addEventListener("load",this._resize);else if(t instanceof HTMLQuoteElement){const a=t.firstElementChild?.firstChild?.textContent&&m.reType.exec(t.firstElementChild.firstChild.textContent);if(a){const{type:o}=a.groups,r=document.createElement("ha-alert");r.alertType=m.typeToHaAlert[o.toLowerCase()],r.append(...Array.from(t.childNodes).map(t=>{const e=Array.from(t.childNodes);if(!this.breaks&&e.length){const t=e[0];t.nodeType===Node.TEXT_NODE&&t.textContent===a.input&&t.textContent?.includes("\n")&&(t.textContent=t.textContent.split("\n").slice(1).join("\n"))}return e}).reduce((t,e)=>t.concat(e),[]).filter(t=>t.textContent&&t.textContent!==a.input)),e.parentNode().replaceChild(r,t)}}else t instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(t.localName)&&a(96175)(`./${t.localName}`)}}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,c.r)(this,"content-resize")}}(0,o.Cg)([(0,n.MZ)()],v.prototype,"content",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"allow-svg",type:Boolean})],v.prototype,"allowSvg",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"allow-data-url",type:Boolean})],v.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],v.prototype,"breaks",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"lazy-images"})],v.prototype,"lazyImages",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],v.prototype,"cache",void 0),v=(0,o.Cg)([(0,n.EM)("ha-markdown-element")],v)},3587(t,e,a){var o=a(62826),r=a(96196),n=a(44457);a(69709);class i extends r.WF{async getUpdateComplete(){const t=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),t}render(){return this.content?r.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:r.s6}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}i.styles=r.AH`
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
      --markdown-table-border-width: attr(border, 0);
      --markdown-table-padding-inline: 0;
      --markdown-table-padding-block: 0;
      th {
        vertical-align: attr(align, center);
      }
      td {
        vertical-align: attr(align, left);
      }
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
  `,(0,o.Cg)([(0,n.MZ)()],i.prototype,"content",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"allow-svg",type:Boolean})],i.prototype,"allowSvg",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"allow-data-url",type:Boolean})],i.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],i.prototype,"breaks",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"lazy-images"})],i.prototype,"lazyImages",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],i.prototype,"cache",void 0),(0,o.Cg)([(0,n.P)("ha-markdown-element")],i.prototype,"_markdownElement",void 0),i=(0,o.Cg)([(0,n.EM)("ha-markdown")],i)},24367(t,e,a){a.d(e,{L:()=>r,z:()=>n});var o=a(23832);const r=["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"],n=(0,o.g)(r)},15056(t,e,a){a.a(t,async function(t,o){try{a.r(e);var r=a(62826),n=a(96196),i=a(44457),s=a(18350),l=(a(72554),a(52763),a(3587),a(65829)),c=a(82e3),d=a(14503),h=t([s,l]);[s,l]=h.then?(await h)():h;let p=0;class u extends n.WF{showDialog({continueFlowId:t,mfaModuleId:e,dialogClosedCallback:a}){this._instance=p++,this._dialogClosedCallback=a,this._opened=!0;const o=t?this.hass.callWS({type:"auth/setup_mfa",flow_id:t}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:e}),r=this._instance;o.then(t=>{r===this._instance&&this._processStep(t)})}closeDialog(){this._step&&this._flowDone(),this._opened=!1}render(){return this._opened?n.qy` <ha-dialog open .heading="${this._computeStepTitle()}" @closed="${this.closeDialog}"> <div> ${this._errorMessage?n.qy`<div class="error">${this._errorMessage}</div>`:""} ${this._step?n.qy`${"abort"===this._step.type?n.qy` <ha-markdown allow-svg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.abort.${this._step.reason}`)}"></ha-markdown>`:"create_entry"===this._step.type?n.qy`<p> ${this.hass.localize("ui.panel.profile.mfa_setup.step_done",{step:this._step.title||this._step.handler})} </p>`:"form"===this._step.type?n.qy`<ha-markdown allow-svg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.description`,this._step.description_placeholders)}"></ha-markdown> <ha-form .hass="${this.hass}" .data="${this._stepData}" .schema="${(0,c.Hg)(this._step.data_schema)}" .error="${this._step.errors}" .computeLabel="${this._computeLabel}" .computeError="${this._computeError}" @value-changed="${this._stepDataChanged}"></ha-form>`:""}`:n.qy`<div class="init-spinner"> <ha-spinner></ha-spinner> </div>`} </div> <ha-button slot="primaryAction" @click="${this.closeDialog}" appearance="${["abort","create_entry"].includes(this._step?.type||"")?"accent":"plain"}">${this.hass.localize(["abort","create_entry"].includes(this._step?.type||"")?"ui.panel.profile.mfa_setup.close":"ui.common.cancel")}</ha-button> ${"form"===this._step?.type?n.qy`<ha-button slot="primaryAction" .disabled="${this._loading}" @click="${this._submitStep}">${this.hass.localize("ui.panel.profile.mfa_setup.submit")}</ha-button>`:n.s6} </ha-dialog> `:n.s6}static get styles(){return[d.nA,n.AH`.error{color:red}ha-dialog{max-width:500px}ha-markdown{--markdown-svg-background-color:white;--markdown-svg-color:black;display:block;margin:0 auto}ha-markdown a{color:var(--primary-color)}ha-markdown-element p{text-align:center}ha-markdown-element code{background-color:transparent}ha-markdown-element>:last-child{margin-bottom:revert}.init-spinner{padding:10px 100px 34px;text-align:center}`]}firstUpdated(t){super.firstUpdated(t),this.hass.loadBackendTranslation("mfa_setup","auth"),this.addEventListener("keypress",t=>{"Enter"===t.key&&this._submitStep()})}_stepDataChanged(t){this._stepData=t.detail.value}_submitStep(){this._loading=!0,this._errorMessage=void 0;const t=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then(e=>{t===this._instance&&(this._processStep(e),this._loading=!1)},t=>{this._errorMessage=t&&t.body&&t.body.message||"Unknown error occurred",this._loading=!1})}_processStep(t){t.errors||(t.errors={}),this._step=t,0===Object.keys(t.errors).length&&(this._stepData={})}_flowDone(){const t=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));this._dialogClosedCallback({flowFinished:t}),this._errorMessage=void 0,this._step=void 0,this._stepData={},this._dialogClosedCallback=void 0,this.closeDialog()}_computeStepTitle(){return"abort"===this._step?.type?this.hass.localize("ui.panel.profile.mfa_setup.title_aborted"):"create_entry"===this._step?.type?this.hass.localize("ui.panel.profile.mfa_setup.title_success"):"form"===this._step?.type?this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.title`):""}constructor(...t){super(...t),this._loading=!1,this._opened=!1,this._stepData={},this._computeLabel=t=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.data.${t.name}`)||t.name,this._computeError=t=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.error.${t}`)||t}}(0,r.Cg)([(0,i.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_dialogClosedCallback",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_instance",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_loading",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_opened",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_stepData",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_step",void 0),(0,r.Cg)([(0,i.wk)()],u.prototype,"_errorMessage",void 0),u=(0,r.Cg)([(0,i.EM)("ha-mfa-module-setup-flow")],u),o()}catch(t){o(t)}})},996(t,e,a){a.d(e,{G:()=>o});class o{get(t){return this._cache.get(t)}set(t,e){this._cache.set(t,e),this._expiration&&window.setTimeout(()=>this._cache.delete(t),this._expiration)}has(t){return this._cache.has(t)}constructor(t){this._cache=new Map,this._expiration=t}}},96175(t,e,a){var o={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","52074","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-button-toolbar.ts":["9882","52074","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function r(t){if(!a.o(o,t))return Promise.resolve().then(function(){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e});var e=o[t],r=e[0];return Promise.all(e.slice(1).map(a.e)).then(function(){return a(r)})}r.keys=()=>Object.keys(o),r.id=96175,t.exports=r},48646(t,e,a){var o=a(69565),r=a(28551),n=a(1767),i=a(50851);t.exports=function(t,e){e&&"string"==typeof t||r(t);var a=i(t);return n(r(void 0!==a?o(a,t):t))}},30531(t,e,a){var o=a(46518),r=a(69565),n=a(79306),i=a(28551),s=a(1767),l=a(48646),c=a(19462),d=a(9539),h=a(96395),p=a(30684),u=a(84549),g=!h&&!p("flatMap",function(){}),m=!h&&!g&&u("flatMap",TypeError),v=h||g||m,_=c(function(){for(var t,e,a=this.iterator,o=this.mapper;;){if(e=this.inner)try{if(!(t=i(r(e.next,e.iterator))).done)return t.value;this.inner=null}catch(t){d(a,"throw",t)}if(t=i(r(this.next,a)),this.done=!!t.done)return;try{this.inner=l(o(t.value,this.counter++),!1)}catch(t){d(a,"throw",t)}}});o({target:"Iterator",proto:!0,real:!0,forced:v},{flatMap:function(t){i(this);try{n(t)}catch(t){d(this,"throw",t)}return m?r(m,this,t):new _(s(this),{mapper:t,inner:null})}})},2209(t,e,a){a.d(e,{LV:()=>p});a(18111),a(61701),a(18237);const o=Symbol("Comlink.proxy"),r=Symbol("Comlink.endpoint"),n=Symbol("Comlink.releaseProxy"),i=Symbol("Comlink.finalizer"),s=Symbol("Comlink.thrown"),l=t=>"object"==typeof t&&null!==t||"function"==typeof t,c=new Map([["proxy",{canHandle:t=>l(t)&&t[o],serialize(t){const{port1:e,port2:a}=new MessageChannel;return d(t,e),[a,[a]]},deserialize:t=>(t.start(),p(t))}],["throw",{canHandle:t=>l(t)&&s in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function d(t,e=globalThis,a=["*"]){e.addEventListener("message",function r(n){if(!n||!n.data)return;if(!function(t,e){for(const a of t){if(e===a||"*"===a)return!0;if(a instanceof RegExp&&a.test(e))return!0}return!1}(a,n.origin))return void console.warn(`Invalid origin '${n.origin}' for comlink proxy`);const{id:l,type:c,path:p}=Object.assign({path:[]},n.data),u=(n.data.argumentList||[]).map(w);let g;try{const e=p.slice(0,-1).reduce((t,e)=>t[e],t),a=p.reduce((t,e)=>t[e],t);switch(c){case"GET":g=a;break;case"SET":e[p.slice(-1)[0]]=w(n.data.value),g=!0;break;case"APPLY":g=a.apply(e,u);break;case"CONSTRUCT":g=function(t){return Object.assign(t,{[o]:!0})}(new a(...u));break;case"ENDPOINT":{const{port1:e,port2:a}=new MessageChannel;d(t,a),g=function(t,e){return f.set(t,e),t}(e,[e])}break;case"RELEASE":g=void 0;break;default:return}}catch(t){g={value:t,[s]:0}}Promise.resolve(g).catch(t=>({value:t,[s]:0})).then(a=>{const[o,n]=y(a);e.postMessage(Object.assign(Object.assign({},o),{id:l}),n),"RELEASE"===c&&(e.removeEventListener("message",r),h(e),i in t&&"function"==typeof t[i]&&t[i]())}).catch(t=>{const[a,o]=y({value:new TypeError("Unserializable return value"),[s]:0});e.postMessage(Object.assign(Object.assign({},a),{id:l}),o)})}),e.start&&e.start()}function h(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function p(t,e){const a=new Map;return t.addEventListener("message",function(t){const{data:e}=t;if(!e||!e.id)return;const o=a.get(e.id);if(o)try{o(e)}finally{a.delete(e.id)}}),_(t,a,[],e)}function u(t){if(t)throw new Error("Proxy has been released and is not useable")}function g(t){return k(t,new Map,{type:"RELEASE"}).then(()=>{h(t)})}const m=new WeakMap,v="FinalizationRegistry"in globalThis&&new FinalizationRegistry(t=>{const e=(m.get(t)||0)-1;m.set(t,e),0===e&&g(t)});function _(t,e,a=[],o=function(){}){let i=!1;const s=new Proxy(o,{get(o,r){if(u(i),r===n)return()=>{!function(t){v&&v.unregister(t)}(s),g(t),e.clear(),i=!0};if("then"===r){if(0===a.length)return{then:()=>s};const o=k(t,e,{type:"GET",path:a.map(t=>t.toString())}).then(w);return o.then.bind(o)}return _(t,e,[...a,r])},set(o,r,n){u(i);const[s,l]=y(n);return k(t,e,{type:"SET",path:[...a,r].map(t=>t.toString()),value:s},l).then(w)},apply(o,n,s){u(i);const l=a[a.length-1];if(l===r)return k(t,e,{type:"ENDPOINT"}).then(w);if("bind"===l)return _(t,e,a.slice(0,-1));const[c,d]=b(s);return k(t,e,{type:"APPLY",path:a.map(t=>t.toString()),argumentList:c},d).then(w)},construct(o,r){u(i);const[n,s]=b(r);return k(t,e,{type:"CONSTRUCT",path:a.map(t=>t.toString()),argumentList:n},s).then(w)}});return function(t,e){const a=(m.get(e)||0)+1;m.set(e,a),v&&v.register(t,e,t)}(s,t),s}function b(t){const e=t.map(y);return[e.map(t=>t[0]),(a=e.map(t=>t[1]),Array.prototype.concat.apply([],a))];var a}const f=new WeakMap;function y(t){for(const[e,a]of c)if(a.canHandle(t)){const[o,r]=a.serialize(t);return[{type:"HANDLER",name:e,value:o},r]}return[{type:"RAW",value:t},f.get(t)||[]]}function w(t){switch(t.type){case"HANDLER":return c.get(t.name).deserialize(t.value);case"RAW":return t.value}}function k(t,e,a,o){return new Promise(r=>{const n=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");e.set(n,r),t.start&&t.start(),t.postMessage(Object.assign({id:n},a),o)})}}};
//# sourceMappingURL=68138.66275042d9e94814.js.map