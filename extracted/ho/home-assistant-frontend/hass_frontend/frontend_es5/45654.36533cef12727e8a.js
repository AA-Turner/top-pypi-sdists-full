"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["45654"],{93444:function(e,t,a){var o=a(40445),i=a(96196),r=a(77845);let l,s,n=e=>e;class d extends i.WF{render(){return(0,i.qy)(l||(l=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,i.AH)(s||(s=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){a(62953);var o=a(40445),i=a(96196),r=a(77845);let l,s,n,d,h,c,p=e=>e;class u extends i.WF{render(){const e=(0,i.qy)(l||(l=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(s||(s=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(d||(d=p`${0}${0}`),t,e):(0,i.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],u)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953);var o=a(40445),i=a(93900),r=a(96196),l=a(77845),s=a(32288),n=a(1087),d=a(59992),h=a(14503),c=a(22348),p=(a(76538),a(26300)),u=e([i,p,d]);[i,p,d]=u.then?(await u)():u;let g,v,m,b,f,y,w,_=e=>e;const x="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class C extends((0,d.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(g||(g=_` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,s.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(v||(v=_` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",x,void 0!==this.headerTitle?(0,r.qy)(m||(m=_`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=_`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(f||(f=_`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=_`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,(0,r.AH)(w||(w=_`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,c.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,n.r)(this,"closed"))}}}(0,o.Cg)([(0,l.MZ)({attribute:!1})],C.prototype,"hass",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],C.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],C.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",void 0),(0,o.Cg)([(0,l.MZ)({reflect:!0})],C.prototype,"type",void 0),(0,o.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],C.prototype,"width",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],C.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-title"})],C.prototype,"headerTitle",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],C.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],C.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],C.prototype,"flexContent",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,attribute:"without-header"})],C.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,l.wk)()],C.prototype,"_open",void 0),(0,o.Cg)([(0,l.P)(".body")],C.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,l.wk)()],C.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,l.Ls)({passive:!0})],C.prototype,"_handleBodyScroll",null),C=(0,o.Cg)([(0,l.EM)("ha-dialog")],C),t()}catch(g){t(g)}})},52763:function(e,t,a){a.a(e,async function(e,o){try{a.d(t,{U:function(){return $}});a(18111),a(7588),a(61701),a(3362),a(62953);var i=a(40445),r=a(96196),l=a(77845),s=a(69558),n=a(1087),d=a(38962),h=(a(11399),e([d]));d=(h.then?(await h)():h)[0];let c,p,u,g,v,m,b,f,y,w=e=>e;const _={boolean:()=>Promise.all([a.e("83431"),a.e("8477"),a.e("21934")]).then(a.bind(a,46990)),constant:()=>a.e("65733").then(a.bind(a,90820)),float:()=>Promise.all([a.e("31065"),a.e("17477")]).then(a.bind(a,20676)),grid:()=>a.e("60761").then(a.bind(a,70208)),expandable:()=>a.e("45001").then(a.bind(a,40003)),integer:()=>Promise.all([a.e("87272"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("8477"),a.e("21543"),a.e("31302"),a.e("43413")]).then(a.bind(a,20036)),multi_select:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("8477"),a.e("54849"),a.e("78219")]).then(a.bind(a,36182)),positive_time_period_dict:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("84128"),a.e("16508"),a.e("78320")]).then(a.bind(a,89422)),select:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("84848"),a.e("78398"),a.e("39005"),a.e("35873"),a.e("39680")]).then(a.bind(a,63804)),string:()=>Promise.all([a.e("31065"),a.e("31802")]).then(a.bind(a,54753)),optional_actions:()=>Promise.all([a.e("87272"),a.e("30628"),a.e("34995"),a.e("37909")]).then(a.bind(a,8456))},x=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null,C=(e,t)=>e&&t.name?e[t.name]:null,S=(e,t)=>e&&t.name?e[t.name]:null;class $ extends r.WF{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof r.mN&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach(e=>{var t;"selector"in e||null===(t=_[e.type])||void 0===t||t.call(_)})}render(){return(0,r.qy)(c||(c=w` <div class="root" part="root"> ${0} ${0} </div> `),this.error&&this.error.base?(0,r.qy)(p||(p=w` <ha-alert alert-type="error"> ${0} </ha-alert> `),this._computeError(this.error.base,this.schema)):"",this.schema.map(e=>{var t;const a=C(this.error,e),o=S(this.warning,e);return(0,r.qy)(u||(u=w` ${0} ${0} `),a?(0,r.qy)(g||(g=w` <ha-alert own-margin alert-type="error"> ${0} </ha-alert> `),this._computeError(a,e)):o?(0,r.qy)(v||(v=w` <ha-alert own-margin alert-type="warning"> ${0} </ha-alert> `),this._computeWarning(o,e)):"","selector"in e?(0,r.qy)(m||(m=w`<ha-selector .schema="${0}" .hass="${0}" .narrow="${0}" .name="${0}" .selector="${0}" .value="${0}" .label="${0}" .disabled="${0}" .placeholder="${0}" .helper="${0}" .localizeValue="${0}" .required="${0}" .context="${0}"></ha-selector>`),e,this.hass,this.narrow,e.name,e.selector,x(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?void 0:e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,s._)(this.fieldElementName(e.type),Object.assign({schema:e,data:x(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))}))}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,n.r)(this,"value-changed",{value:this.data})})}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?(0,r.qy)(b||(b=w`<ul> ${0} </ul>`),e.map(e=>(0,r.qy)(f||(f=w`<li> ${0} </li>`),this.computeError?this.computeError(e,t):e))):this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}$.shadowRootOptions={mode:"open",delegatesFocus:!0},$.styles=(0,r.AH)(y||(y=w`.root>*{display:block}.root>:not([own-margin]):not(:last-child){margin-bottom:24px}ha-alert[own-margin]{margin-bottom:4px}`)),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"hass",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean})],$.prototype,"narrow",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"data",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"schema",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"error",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"warning",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean})],$.prototype,"disabled",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"computeError",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"computeWarning",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"computeLabel",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"computeHelper",void 0),(0,i.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"localizeValue",void 0),$=(0,i.Cg)([(0,l.EM)("ha-form")],$),o()}catch(c){o(c)}})},87285:function(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{DialogForm:function(){return m}});a(3362),a(62953);var i=a(40445),r=a(96196),l=a(77845),s=a(1087),n=a(18350),d=a(52763),h=(a(93444),a(72554)),c=a(14503),p=e([n,d,h]);[n,d,h]=p.then?(await p)():p;let u,g,v=e=>e;class m extends r.WF{async showDialog(e){this._params=e,this._data=e.data||{},this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){var e,t;this._closeState||(null===(e=this._params)||void 0===e||null===(t=e.cancel)||void 0===t||t.call(e));this._closeState=void 0,this._params=void 0,this._data={},this._open=!1,(0,s.r)(this,"dialog-closed",{dialog:this.localName})}_submit(){var e,t;this._closeState="submitted",null===(e=this._params)||void 0===e||null===(t=e.submit)||void 0===t||t.call(e,this._data),this.closeDialog()}_cancel(){var e,t;this._closeState="canceled",null===(e=this._params)||void 0===e||null===(t=e.cancel)||void 0===t||t.call(e),this.closeDialog()}_valueChanged(e){this._data=e.detail.value}render(){return this._params&&this.hass?(0,r.qy)(u||(u=v` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" prevent-scrim-close @closed="${0}"> <ha-form autofocus .hass="${0}" .computeLabel="${0}" .computeHelper="${0}" .data="${0}" .schema="${0}" @value-changed="${0}"> </ha-form> <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this._params.title,this._dialogClosed,this.hass,this._params.computeLabel,this._params.computeHelper,this._data,this._params.schema,this._valueChanged,this._cancel,this._params.cancelText||this.hass.localize("ui.common.cancel"),this._submit,this._params.submitText||this.hass.localize("ui.common.save")):r.s6}constructor(...e){super(...e),this._data={},this._open=!1}}m.styles=[c.nA,(0,r.AH)(g||(g=v``))],(0,i.Cg)([(0,l.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,i.Cg)([(0,l.wk)()],m.prototype,"_params",void 0),(0,i.Cg)([(0,l.wk)()],m.prototype,"_data",void 0),(0,i.Cg)([(0,l.wk)()],m.prototype,"_open",void 0),(0,i.Cg)([(0,l.wk)()],m.prototype,"_closeState",void 0),m=(0,i.Cg)([(0,l.EM)("dialog-form")],m),o()}catch(u){o(u)}})},59992:function(e,t,a){a.a(e,async function(e,o){try{a.d(t,{V:function(){return g}});a(62953);var i=a(40445),r=a(88696),l=a(96196),s=a(94333),n=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let h,c,p=e=>e;const u=e=>void 0===e?[]:Array.isArray(e)?e:[e],g=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,l.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...u(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,l.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,n.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,n.wk)()],t.prototype,"_contentScrollable",void 0),t};o()}catch(h){o(h)}})},22348:function(e,t,a){a.d(t,{V:function(){return i}});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177:function(e,t,a){a.d(t,{n:function(){return o}});a(27495);const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=45654.36533cef12727e8a.js.map