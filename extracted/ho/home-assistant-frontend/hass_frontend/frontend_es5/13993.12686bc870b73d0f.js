(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["13993"],{69558:function(e,t,a){"use strict";a.d(t,{_:function(){return r}});a(16280),a(18111),a(7588),a(62953);var o=a(96196),i=a(54495);const r=(0,i.u$)(class extends i.WL{update(e,[t,a]){return this._element&&this._element.localName===t?(a&&Object.entries(a).forEach(([e,t])=>{this._element[e]=t}),o.c0):this.render(t,a)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach(([e,t])=>{this._element[e]=t}),this._element}constructor(e){if(super(e),e.type!==i.OA.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}})},69093:function(e,t,a){"use strict";a.d(t,{t:function(){return i}});var o=a(71727);const i=e=>(0,o.m)(e.entity_id)},82286:function(e,t,a){"use strict";a.d(t,{$:function(){return o}});const o=(e,t)=>i(e.attributes,t),i=(e,t)=>0!==(e.supported_features&t)},93444:function(e,t,a){"use strict";var o=a(40445),i=a(96196),r=a(77845);let n,s,l=e=>e;class d extends i.WF{render(){return(0,i.qy)(n||(n=l` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,i.AH)(s||(s=l`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){"use strict";a(62953);var o=a(40445),i=a(96196),r=a(77845);let n,s,l,d,h,c,p=e=>e;class u extends i.WF{render(){const e=(0,i.qy)(n||(n=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(s||(s=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(l||(l=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(d||(d=p`${0}${0}`),t,e):(0,i.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],u)},72554:function(e,t,a){"use strict";a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var o=a(40445),i=a(93900),r=a(96196),n=a(77845),s=a(32288),l=a(1087),d=a(64481),h=a(59992),c=a(14503),p=a(22348),u=(a(76538),a(26300)),m=e([i,u,h]);[i,u,h]=m.then?(await m)():m;let v,g,b,f,_,y,w,k=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class x extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(v||(v=k` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,s.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(g||(g=k` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(b||(b=k`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(f||(f=k`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(_||(_=k`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=k`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(w||(w=k`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,l.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,l.r)(this,"closed"))}}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],x.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-labelledby"})],x.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-describedby"})],x.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],x.prototype,"open",void 0),(0,o.Cg)([(0,n.MZ)({reflect:!0})],x.prototype,"type",void 0),(0,o.Cg)([(0,n.MZ)({type:String,reflect:!0,attribute:"width"})],x.prototype,"width",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],x.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-title"})],x.prototype,"headerTitle",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-subtitle"})],x.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"header-subtitle-position"})],x.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],x.prototype,"flexContent",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"without-header"})],x.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,n.wk)()],x.prototype,"_open",void 0),(0,o.Cg)([(0,n.P)(".body")],x.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,n.wk)()],x.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,n.Ls)({passive:!0})],x.prototype,"_handleBodyScroll",null),x=(0,o.Cg)([(0,n.EM)("ha-dialog")],x),t()}catch(v){t(v)}})},52763:function(e,t,a){"use strict";a.a(e,async function(e,t){try{a(18111),a(7588),a(61701),a(3362),a(62953);var o=a(40445),i=a(96196),r=a(77845),n=a(69558),s=a(1087),l=a(38962),d=(a(11399),e([l]));l=(d.then?(await d)():d)[0];let h,c,p,u,m,v,g,b,f,_=e=>e;const y={boolean:()=>Promise.all([a.e("83431"),a.e("8477"),a.e("21934")]).then(a.bind(a,46990)),constant:()=>a.e("65733").then(a.bind(a,90820)),float:()=>Promise.all([a.e("31065"),a.e("17477")]).then(a.bind(a,20676)),grid:()=>a.e("60761").then(a.bind(a,70208)),expandable:()=>a.e("45001").then(a.bind(a,40003)),integer:()=>Promise.all([a.e("87272"),a.e("31065"),a.e("30628"),a.e("83431"),a.e("8477"),a.e("21543"),a.e("31302"),a.e("43413")]).then(a.bind(a,20036)),multi_select:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("8477"),a.e("54849"),a.e("78219")]).then(a.bind(a,36182)),positive_time_period_dict:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("84128"),a.e("16508"),a.e("78320")]).then(a.bind(a,89422)),select:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("84848"),a.e("78398"),a.e("39005"),a.e("35873"),a.e("39680")]).then(a.bind(a,63804)),string:()=>Promise.all([a.e("31065"),a.e("31802")]).then(a.bind(a,54753)),optional_actions:()=>Promise.all([a.e("87272"),a.e("30628"),a.e("34995"),a.e("37909")]).then(a.bind(a,8456))},w=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null,k=(e,t)=>e&&t.name?e[t.name]:null,C=(e,t)=>e&&t.name?e[t.name]:null;class x extends i.WF{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.mN&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach(e=>{var t;"selector"in e||null===(t=y[e.type])||void 0===t||t.call(y)})}render(){return(0,i.qy)(h||(h=_` <div class="root" part="root"> ${0} ${0} </div> `),this.error&&this.error.base?(0,i.qy)(c||(c=_` <ha-alert alert-type="error"> ${0} </ha-alert> `),this._computeError(this.error.base,this.schema)):"",this.schema.map(e=>{var t;const a=k(this.error,e),o=C(this.warning,e);return(0,i.qy)(p||(p=_` ${0} ${0} `),a?(0,i.qy)(u||(u=_` <ha-alert own-margin alert-type="error"> ${0} </ha-alert> `),this._computeError(a,e)):o?(0,i.qy)(m||(m=_` <ha-alert own-margin alert-type="warning"> ${0} </ha-alert> `),this._computeWarning(o,e)):"","selector"in e?(0,i.qy)(v||(v=_`<ha-selector .schema="${0}" .hass="${0}" .narrow="${0}" .name="${0}" .selector="${0}" .value="${0}" .label="${0}" .disabled="${0}" .placeholder="${0}" .helper="${0}" .localizeValue="${0}" .required="${0}" .context="${0}"></ha-selector>`),e,this.hass,this.narrow,e.name,e.selector,w(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?void 0:e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,n._)(this.fieldElementName(e.type),Object.assign({schema:e,data:w(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))}))}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,s.r)(this,"value-changed",{value:this.data})})}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?(0,i.qy)(g||(g=_`<ul> ${0} </ul>`),e.map(e=>(0,i.qy)(b||(b=_`<li> ${0} </li>`),this.computeError?this.computeError(e,t):e))):this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}x.shadowRootOptions={mode:"open",delegatesFocus:!0},x.styles=(0,i.AH)(f||(f=_`.root>*{display:block}.root>:not([own-margin]):not(:last-child){margin-bottom:24px}ha-alert[own-margin]{margin-bottom:4px}`)),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"narrow",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"data",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"schema",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"error",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"warning",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"disabled",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"computeError",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"computeWarning",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"computeLabel",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"computeHelper",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"localizeValue",void 0),x=(0,o.Cg)([(0,r.EM)("ha-form")],x),t()}catch(h){t(h)}})},69709:function(e,t,a){"use strict";var o=a(59787),i=(a(74423),a(72712),a(18111),a(22489),a(61701),a(18237),a(3362),a(27495),a(62953),a(40445)),r=a(96196),n=a(77845),s=a(1420),l=a(30015),d=a.n(l),h=a(1087),c=(a(3296),a(27208),a(48408),a(14603),a(47566),a(98721),a(2209));let p;var u=a(996);let m,v=e=>e;const g=e=>(0,r.qy)(m||(m=v`${0}`),e),b=new u.G(1e3),f={reType:(0,o.A)(/((\[!(caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,{input:1,type:3}),typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class _ extends r.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();b.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();b.has(e)&&((0,r.XX)(g((0,s._)(b.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return d()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,o)=>(p||(p=(0,c.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),p.renderMarkdown(e,t,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,r.XX)(g((0,s._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){var o;const a=(null===(o=e.firstElementChild)||void 0===o||null===(o=o.firstChild)||void 0===o?void 0:o.textContent)&&f.reType.exec(e.firstElementChild.firstChild.textContent);if(a){const{type:o}=a.groups,i=document.createElement("ha-alert");i.alertType=f.typeToHaAlert[o.toLowerCase()],i.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){var o;const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===a.input&&null!==(o=e.textContent)&&void 0!==o&&o.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==a.input)),t.parentNode().replaceChild(i,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&a(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,h.r)(this,"content-resize")}}(0,i.Cg)([(0,n.MZ)()],_.prototype,"content",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"allow-svg",type:Boolean})],_.prototype,"allowSvg",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"allow-data-url",type:Boolean})],_.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean})],_.prototype,"breaks",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,attribute:"lazy-images"})],_.prototype,"lazyImages",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean})],_.prototype,"cache",void 0),_=(0,i.Cg)([(0,n.EM)("ha-markdown-element")],_)},3587:function(e,t,a){"use strict";a(3362),a(62953);var o=a(40445),i=a(96196),r=a(77845);a(69709);let n,s,l=e=>e;class d extends i.WF{async getUpdateComplete(){var e;const t=await super.getUpdateComplete();return await(null===(e=this._markdownElement)||void 0===e?void 0:e.updateComplete),t}render(){return this.content?(0,i.qy)(n||(n=l`<ha-markdown-element .content="${0}" .allowSvg="${0}" .allowDataUrl="${0}" .breaks="${0}" .lazyImages="${0}" .cache="${0}"></ha-markdown-element>`),this.content,this.allowSvg,this.allowDataUrl,this.breaks,this.lazyImages,this.cache):i.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}d.styles=(0,i.AH)(s||(s=l`
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
  `)),(0,o.Cg)([(0,r.MZ)()],d.prototype,"content",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],d.prototype,"allowSvg",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],d.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"breaks",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],d.prototype,"lazyImages",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"cache",void 0),(0,o.Cg)([(0,r.P)("ha-markdown-element")],d.prototype,"_markdownElement",void 0),d=(0,o.Cg)([(0,r.EM)("ha-markdown")],d)},11399:function(e,t,a){"use strict";a(3362),a(27495),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(25440),a(62953);var o=a(40445),i=a(96196),r=a(77845),n=a(22786),s=a(69558),l=a(95311);let d,h=e=>e;const c={action:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("89385"),a.e("30911"),a.e("25950"),a.e("87094"),a.e("5445"),a.e("20697"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("94860"),a.e("16508"),a.e("78547"),a.e("53065"),a.e("31863"),a.e("283"),a.e("30513"),a.e("7337")]).then(a.bind(a,6274)),addon:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("21161"),a.e("78398"),a.e("39005"),a.e("5850"),a.e("43305")]).then(a.bind(a,36784)),app:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("21161"),a.e("78398"),a.e("39005"),a.e("5850")]).then(a.bind(a,48585)),area:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("52563"),a.e("78398"),a.e("39005"),a.e("99586")]).then(a.bind(a,81857)),areas_display:()=>Promise.all([a.e("46095"),a.e("31065"),a.e("84510"),a.e("64135"),a.e("64280"),a.e("97899")]).then(a.bind(a,38235)),attribute:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("43542"),a.e("78398"),a.e("39005"),a.e("44421")]).then(a.bind(a,71498)),assist_pipeline:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("53525"),a.e("63071")]).then(a.bind(a,83642)),boolean:()=>Promise.all([a.e("83431"),a.e("36980"),a.e("28628")]).then(a.bind(a,30714)),choose:()=>a.e("93934").then(a.bind(a,58141)),color_rgb:()=>Promise.all([a.e("31065"),a.e("25840")]).then(a.bind(a,34931)),condition:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("30911"),a.e("25950"),a.e("33810"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("78547"),a.e("53065"),a.e("283"),a.e("7583")]).then(a.bind(a,81539)),config_entry:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("77850"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("64948")]).then(a.bind(a,49347)),conversation_agent:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("19942"),a.e("10192"),a.e("44770")]).then(a.bind(a,94215)),constant:()=>a.e("77057").then(a.bind(a,39032)),country:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("72605"),a.e("43695"),a.e("78398"),a.e("39005"),a.e("57279")]).then(a.bind(a,94164)),date:()=>Promise.all([a.e("31065"),a.e("26669")]).then(a.bind(a,94351)),datetime:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("95366"),a.e("20766")]).then(a.bind(a,39045)),device:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("66101"),a.e("78398"),a.e("39005"),a.e("9537")]).then(a.bind(a,2270)),duration:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("61747"),a.e("16508"),a.e("66300")]).then(a.bind(a,79488)),entity:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("30911"),a.e("7348"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("1535"),a.e("61804")]).then(a.bind(a,73863)),entity_name:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("37261"),a.e("78398"),a.e("39005"),a.e("88992")]).then(a.bind(a,7563)),statistic:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("30911"),a.e("70921"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("54884"),a.e("23855")]).then(a.bind(a,28072)),file:()=>Promise.all([a.e("19300"),a.e("54731")]).then(a.bind(a,25078)),floor:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("35806"),a.e("49769"),a.e("78398"),a.e("39005"),a.e("27495"),a.e("51962")]).then(a.bind(a,9040)),label:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("44174"),a.e("78398"),a.e("39005"),a.e("66201"),a.e("47411")]).then(a.bind(a,99560)),language:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("65923"),a.e("78398"),a.e("39005"),a.e("16633")]).then(a.bind(a,15430)),navigation:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("34861"),a.e("25582"),a.e("99788"),a.e("85566"),a.e("30911"),a.e("30398"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("19112"),a.e("30002"),a.e("21519"),a.e("25322"),a.e("12009"),a.e("99023"),a.e("59553"),a.e("78547"),a.e("1536"),a.e("68766")]).then(a.bind(a,58350)),number:()=>Promise.all([a.e("87272"),a.e("31065"),a.e("30628"),a.e("21543"),a.e("16195")]).then(a.bind(a,31157)),object:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("72130"),a.e("85010"),a.e("97163"),a.e("34310"),a.e("60610")]).then(a.bind(a,97951)),qr_code:()=>Promise.all([a.e("87272"),a.e("51343"),a.e("27483")]).then(a.bind(a,35313)),select:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("4939"),a.e("78398"),a.e("39005"),a.e("35873"),a.e("43527")]).then(a.bind(a,856)),selector:()=>a.e("77810").then(a.bind(a,13897)),state:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("10077"),a.e("78398"),a.e("39005"),a.e("13172")]).then(a.bind(a,12995)),backup_location:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("83431"),a.e("34995"),a.e("60987"),a.e("72777")]).then(a.bind(a,16360)),stt:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("75906"),a.e("87890")]).then(a.bind(a,42999)),target:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("30911"),a.e("95956"),a.e("58047"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("19065"),a.e("24891"),a.e("43030")]).then(a.bind(a,84909)),template:()=>Promise.all([a.e("87272"),a.e("30628"),a.e("72130"),a.e("15028"),a.e("34310"),a.e("822")]).then(a.bind(a,62166)),text:()=>Promise.all([a.e("31065"),a.e("84384")]).then(a.bind(a,47971)),time:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("34995"),a.e("98287"),a.e("93968")]).then(a.bind(a,42945)),icon:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("55469"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("56882")]).then(a.bind(a,14885)),media:()=>Promise.all([a.e("96919"),a.e("99038"),a.e("49091")]).then(a.bind(a,59422)),theme:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("20668"),a.e("80530")]).then(a.bind(a,77655)),timezone:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("32636"),a.e("35540"),a.e("78398"),a.e("39005"),a.e("25727"),a.e("42786")]).then(a.bind(a,6719)),button_toggle:()=>a.e("7774").then(a.bind(a,79949)),trigger:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("72130"),a.e("85010"),a.e("30911"),a.e("25950"),a.e("87094"),a.e("82647"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("34310"),a.e("12009"),a.e("78547"),a.e("53065"),a.e("31863"),a.e("61566")]).then(a.bind(a,45078)),tts:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("43049"),a.e("56146")]).then(a.bind(a,59447)),tts_voice:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("30628"),a.e("34995"),a.e("87811"),a.e("58485")]).then(a.bind(a,41188)),location:()=>Promise.all([a.e("87272"),a.e("66139"),a.e("70622"),a.e("5177"),a.e("8851"),a.e("12122"),a.e("76696"),a.e("99907")]).then(a.bind(a,21160)),color_temp:()=>Promise.all([a.e("87272"),a.e("30628"),a.e("99788"),a.e("21543"),a.e("29874"),a.e("21519"),a.e("25122")]).then(a.bind(a,90780)),ui_action:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("83431"),a.e("62453"),a.e("34995"),a.e("8477"),a.e("34861"),a.e("72130"),a.e("85010"),a.e("89385"),a.e("25582"),a.e("99788"),a.e("85566"),a.e("30911"),a.e("25950"),a.e("59984"),a.e("78398"),a.e("39005"),a.e("8851"),a.e("34310"),a.e("19112"),a.e("30002"),a.e("21519"),a.e("25322"),a.e("12009"),a.e("94860"),a.e("36332"),a.e("99023"),a.e("59553"),a.e("78547"),a.e("1536"),a.e("96924")]).then(a.bind(a,38389)),ui_color:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("55883"),a.e("78398"),a.e("39005"),a.e("58027")]).then(a.bind(a,52744)),ui_state_content:()=>Promise.all([a.e("87272"),a.e("46095"),a.e("31065"),a.e("30628"),a.e("92769"),a.e("62453"),a.e("88574"),a.e("78398"),a.e("39005"),a.e("64897")]).then(a.bind(a,96074))},p=new Set(["ui-action","ui-color"]);class u extends i.WF{async focus(){var e;await this.updateComplete,null===(e=this.renderRoot.querySelector("#selector"))||void 0===e||e.focus()}get _type(){const e=Object.keys(this.selector)[0];return p.has(e)?e.replace("-","_"):e}willUpdate(e){var t;e.has("selector")&&this.selector&&(null===(t=c[this._type])||void 0===t||t.call(c))}render(){return(0,i.qy)(d||(d=h` ${0} `),(0,s._)(`ha-selector-${this._type}`,{hass:this.hass,narrow:this.narrow,name:this.name,selector:this._handleLegacySelector(this.selector),value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,localizeValue:this.localizeValue,id:"selector"}))}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1,this.required=!0,this._handleLegacySelector=(0,n.A)(e=>{if("entity"in e)return(0,l.UU)(e);if("device"in e)return(0,l.tD)(e);const t=Object.keys(this.selector)[0];return p.has(t)?{[t.replace("-","_")]:e[t]}:e})}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],u.prototype,"narrow",void 0),(0,o.Cg)([(0,r.MZ)()],u.prototype,"name",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"selector",void 0),(0,o.Cg)([(0,r.MZ)()],u.prototype,"value",void 0),(0,o.Cg)([(0,r.MZ)()],u.prototype,"label",void 0),(0,o.Cg)([(0,r.MZ)()],u.prototype,"helper",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"localizeValue",void 0),(0,o.Cg)([(0,r.MZ)()],u.prototype,"placeholder",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],u.prototype,"disabled",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],u.prototype,"required",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"context",void 0),u=(0,o.Cg)([(0,r.EM)("ha-selector")],u)},95311:function(e,t,a){"use strict";a.d(t,{DF:function(){return g},Lo:function(){return k},MH:function(){return p},MM:function(){return b},Qz:function(){return v},Ru:function(){return _},UU:function(){return y},_7:function(){return m},bZ:function(){return u},m0:function(){return c},tD:function(){return w},vX:function(){return f},wY:function(){return C}});var o=a(20054),i=(a(78350),a(74423),a(44114),a(30237),a(18111),a(22489),a(30531),a(7588),a(13579),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(62953),a(44537)),r=a(69093),n=a(82286),s=a(24367),l=a(28989);const d=["domain","integration","device_class"],h=["integration","manufacturer","model"],c=(e,t,a,o,i,r,n)=>{const s=[],l=[],d=[];return Object.values(a).forEach(a=>{a.labels.includes(t)&&v(e,i,o,a.area_id,r,n)&&d.push(a.area_id)}),Object.values(o).forEach(a=>{a.labels.includes(t)&&g(e,Object.values(i),a,r,n)&&l.push(a.id)}),Object.values(i).forEach(a=>{a.labels.includes(t)&&b(e.states[a.entity_id],r,n)&&s.push(a.entity_id)}),{areas:d,devices:l,entities:s}},p=(e,t,a,o,i)=>{const r=[];return Object.values(a).forEach(a=>{a.floor_id===t&&v(e,e.entities,e.devices,a.area_id,o,i)&&r.push(a.area_id)}),{areas:r}},u=(e,t,a,o,i,r)=>{const n=[],s=[];return Object.values(a).forEach(a=>{a.area_id===t&&g(e,Object.values(o),a,i,r)&&s.push(a.id)}),Object.values(o).forEach(a=>{a.area_id===t&&b(e.states[a.entity_id],i,r)&&n.push(a.entity_id)}),{devices:s,entities:n}},m=(e,t,a,o,i)=>{const r=[];return Object.values(a).forEach(a=>{a.device_id===t&&b(e.states[a.entity_id],o,i)&&r.push(a.entity_id)}),{entities:r}},v=(e,t,a,o,i,r)=>!!Object.values(a).some(a=>!(a.area_id!==o||!g(e,Object.values(t),a,i,r)))||Object.values(t).some(t=>!(t.area_id!==o||!b(e.states[t.entity_id],i,r))),g=(e,t,a,o,r)=>{var n,s;const d=r?(0,l.fk)(r,t):void 0;if(null!==(n=o.target)&&void 0!==n&&n.device&&!(0,i.e)(o.target.device).some(e=>f(e,a,d)))return!1;if(null!==(s=o.target)&&void 0!==s&&s.entity){return t.filter(e=>e.device_id===a.id).some(t=>{const a=e.states[t.entity_id];return b(a,o,r)})}return!0},b=(e,t,a)=>{var o;return!!e&&(null===(o=t.target)||void 0===o||!o.entity||(0,i.e)(t.target.entity).some(t=>_(t,e,a)))},f=(e,t,a)=>{const{manufacturer:o,model:i,model_id:r,integration:n}=e;if(o&&t.manufacturer!==o)return!1;if(i&&t.model!==i)return!1;if(r&&t.model_id!==r)return!1;var s;if(n&&a&&(null==a||null===(s=a[t.id])||void 0===s||!s.has(n)))return!1;return!0},_=(e,t,a)=>{var o;const{domain:s,device_class:l,supported_features:d,integration:h}=e;if(s){const e=(0,r.t)(t);if(Array.isArray(s)?!s.includes(e):e!==s)return!1}if(l){const e=t.attributes.device_class;if(e&&Array.isArray(l)?!l.includes(e):e!==l)return!1}return!(d&&!(0,i.e)(d).some(e=>(0,n.$)(t,e)))&&(!h||(null==a||null===(o=a[t.entity_id])||void 0===o?void 0:o.domain)===h)},y=e=>{if(!e.entity)return{entity:null};if("filter"in e.entity)return e;const t=e.entity,{domain:a,integration:i,device_class:r}=t,n=(0,o.A)(t,d);return a||i||r?{entity:Object.assign(Object.assign({},n),{},{filter:{domain:a,integration:i,device_class:r}})}:{entity:n}},w=e=>{if(!e.device)return{device:null};if("filter"in e.device)return e;const t=e.device,{integration:a,manufacturer:i,model:r}=t,n=(0,o.A)(t,h);return a||i||r?{device:Object.assign(Object.assign({},n),{},{filter:{integration:a,manufacturer:i,model:r}})}:{device:n}},k=e=>{let t;var a;if("target"in e)t=(0,i.e)(null===(a=e.target)||void 0===a?void 0:a.entity);else if("entity"in e){var o,r;if(null!==(o=e.entity)&&void 0!==o&&o.include_entities)return;t=(0,i.e)(null===(r=e.entity)||void 0===r?void 0:r.filter)}if(!t)return;const n=t.flatMap(e=>e.integration||e.device_class||e.supported_features||!e.domain?[]:(0,i.e)(e.domain).filter(e=>(0,s.z)(e)));return[...new Set(n)]},C=(e,t,a,o,r,n={target:{}})=>{if(!t)return[];const s=new Set((0,i.e)(t.entity_id)),l=new Set((0,i.e)(t.device_id)),d=new Set((0,i.e)(t.area_id)),h=new Set((0,i.e)(t.floor_id));return new Set((0,i.e)(t.label_id)).forEach(t=>{const i=c(e,t,r,o,a,n);i.devices.forEach(e=>l.add(e)),i.entities.forEach(e=>s.add(e)),i.areas.forEach(e=>d.add(e))}),h.forEach(t=>{p(e,t,r,n).areas.forEach(e=>d.add(e))}),d.forEach(t=>{const i=u(e,t,o,a,n);i.devices.forEach(e=>l.add(e)),i.entities.forEach(e=>s.add(e))}),l.forEach(t=>{m(e,t,a,n).entities.forEach(e=>s.add(e))}),Array.from(s)}},59992:function(e,t,a){"use strict";a.a(e,async function(e,o){try{a.d(t,{V:function(){return m}});a(62953);var i=a(40445),r=a(88696),n=a(96196),s=a(94333),l=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let h,c,p=e=>e;const u=e=>void 0===e?[]:Array.isArray(e)?e:[e],m=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,n.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...u(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,n.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t};o()}catch(h){o(h)}})},24367:function(e,t,a){"use strict";a.d(t,{L:function(){return i},z:function(){return r}});var o=a(23832);const i=["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"],r=(0,o.g)(i)},15056:function(e,t,a){"use strict";a.a(e,async function(e,o){try{a.r(t);a(89463),a(74423),a(42762),a(62953);var i=a(40445),r=a(96196),n=a(32288),s=a(77845),l=a(18350),d=(a(93444),a(72554)),h=a(52763),c=(a(3587),a(65829)),p=a(82e3),u=a(14503),m=e([l,d,h,c]);[l,d,h,c]=m.then?(await m)():m;let v,g,b,f,_,y,w,k,C,x=e=>e,S=0;class E extends r.WF{showDialog({continueFlowId:e,mfaModuleId:t,dialogClosedCallback:a}){this._instance=S++,this._dialogClosedCallback=a,this._open=!0;const o=e?this.hass.callWS({type:"auth/setup_mfa",flow_id:e}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:t}),i=this._instance;o.then(e=>{i===this._instance&&this._processStep(e)})}closeDialog(){this._open=!1}_dialogClosed(){this._step?this._flowDone():this._resetDialogState()}render(){var e,t,a,o;return void 0===this._instance?r.s6:(0,r.qy)(v||(v=x` <ha-dialog .hass="${0}" .open="${0}" prevent-scrim-close header-title="${0}" @closed="${0}"> <div> ${0} ${0} </div> <ha-dialog-footer slot="footer"> <ha-button slot="${0}" appearance="${0}" @click="${0}">${0}</ha-button> ${0} </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this._computeStepTitle(),this._dialogClosed,this._errorMessage?(0,r.qy)(g||(g=x`<div class="error">${0}</div>`),this._errorMessage):"",this._step?(0,r.qy)(f||(f=x`${0}`),"abort"===this._step.type?(0,r.qy)(_||(_=x` <ha-markdown allow-svg breaks .content="${0}"></ha-markdown>`),this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.abort.${this._step.reason}`)):"create_entry"===this._step.type?(0,r.qy)(y||(y=x`<p> ${0} </p>`),this.hass.localize("ui.panel.profile.mfa_setup.step_done",{step:this._step.title||this._step.handler})):"form"===this._step.type?(0,r.qy)(w||(w=x`<ha-markdown allow-svg breaks .content="${0}"></ha-markdown> <ha-form autofocus .hass="${0}" .data="${0}" .schema="${0}" .error="${0}" .computeLabel="${0}" .computeError="${0}" @value-changed="${0}"></ha-form>`),this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.description`,this._step.description_placeholders),this.hass,this._stepData,(0,p.Hg)(this._step.data_schema),this._step.errors,this._computeLabel,this._computeError,this._stepDataChanged):""):(0,r.qy)(b||(b=x`<div class="init-spinner"> <ha-spinner></ha-spinner> </div>`)),"form"===(null===(e=this._step)||void 0===e?void 0:e.type)?"secondaryAction":"primaryAction",(0,n.J)("form"===(null===(t=this._step)||void 0===t?void 0:t.type)?"plain":void 0),this.closeDialog,this.hass.localize(["abort","create_entry"].includes((null===(a=this._step)||void 0===a?void 0:a.type)||"")?"ui.panel.profile.mfa_setup.close":"ui.common.cancel"),"form"===(null===(o=this._step)||void 0===o?void 0:o.type)?(0,r.qy)(k||(k=x`<ha-button slot="primaryAction" .disabled="${0}" @click="${0}">${0}</ha-button>`),this._isSubmitDisabled(),this._submitStep,this.hass.localize("ui.panel.profile.mfa_setup.submit")):r.s6)}static get styles(){return[u.nA,(0,r.AH)(C||(C=x`.error{color:red}ha-markdown{--markdown-svg-background-color:white;--markdown-svg-color:black;display:block;margin:0 auto}ha-markdown a{color:var(--primary-color)}ha-markdown-element p{text-align:center}ha-markdown-element svg{display:block;margin:0 auto}ha-markdown-element code{background-color:transparent}ha-form{display:block;margin-top:var(--ha-space-4)}ha-markdown-element>:last-child{margin-bottom:revert}.init-spinner{padding:10px 100px 34px;text-align:center}`))]}firstUpdated(e){super.firstUpdated(e),this.hass.loadBackendTranslation("mfa_setup","auth"),this.addEventListener("keypress",e=>{"Enter"===e.key&&this._submitStep()})}_stepDataChanged(e){this._stepData=e.detail.value}_submitStep(){if(this._isSubmitDisabled())return;this._loading=!0,this._errorMessage=void 0;const e=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then(t=>{e===this._instance&&(this._processStep(t),this._loading=!1)},e=>{this._errorMessage=e&&e.body&&e.body.message||"Unknown error occurred",this._loading=!1})}_isSubmitDisabled(){return this._loading||this._hasMissingRequiredFields()}_hasMissingRequiredFields(e=("form"===(e=>null===(e=this._step)||void 0===e?void 0:e.type)()?this._step.data_schema:[])){for(const a of e){var t;if("schema"in a){if(this._hasMissingRequiredFields(a.schema))return!0}else if(a.required&&void 0===a.default&&void 0===(null===(t=a.description)||void 0===t?void 0:t.suggested_value)&&this._isEmptyValue(this._stepData[a.name]))return!0}return!1}_isEmptyValue(e){return null==e||("string"==typeof e?""===e.trim():Array.isArray(e)?0===e.length:"object"==typeof e&&0===Object.keys(e).length)}_processStep(e){e.errors||(e.errors={}),this._step=e,0===Object.keys(e.errors).length&&(this._stepData={})}_flowDone(){const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));this._dialogClosedCallback({flowFinished:e}),this._resetDialogState()}_resetDialogState(){this._errorMessage=void 0,this._step=void 0,this._stepData={},this._dialogClosedCallback=void 0,this._instance=void 0}_computeStepTitle(){var e,t,a;return"abort"===(null===(e=this._step)||void 0===e?void 0:e.type)?this.hass.localize("ui.panel.profile.mfa_setup.title_aborted"):"create_entry"===(null===(t=this._step)||void 0===t?void 0:t.type)?this.hass.localize("ui.panel.profile.mfa_setup.title_success"):"form"===(null===(a=this._step)||void 0===a?void 0:a.type)?this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.title`):""}constructor(...e){super(...e),this._loading=!1,this._open=!1,this._stepData={},this._computeLabel=e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.data.${e.name}`)||e.name,this._computeError=e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.error.${e}`)||e}}(0,i.Cg)([(0,s.MZ)({attribute:!1})],E.prototype,"hass",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_dialogClosedCallback",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_instance",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_loading",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_open",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_stepData",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_step",void 0),(0,i.Cg)([(0,s.wk)()],E.prototype,"_errorMessage",void 0),E=(0,i.Cg)([(0,s.EM)("ha-mfa-module-setup-flow")],E),o()}catch(v){o(v)}})},996:function(e,t,a){"use strict";a.d(t,{G:function(){return o}});a(45367),a(92731),a(62953);class o{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},22348:function(e,t,a){"use strict";a.d(t,{V:function(){return i}});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177:function(e,t,a){"use strict";a.d(t,{n:function(){return o}});a(27495);const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},96175:function(e,t,a){var o={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","30628","41983"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","30628","34995","78097"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","30628","34995","78097"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","46095","31065","30628","92769","62453","78398","39005","73431"],"./ha-icon-button-toolbar.ts":["9882","30628","41983"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["3059","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","46095","31065","30628","92769","62453","78398","39005","73431"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["3059","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function i(e){if(!a.o(o,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=o[e],i=t[0];return Promise.all(t.slice(1).map(a.e)).then(function(){return a(i)})}i.keys=function(){return Object.keys(o)},i.id=96175,e.exports=i}}]);
//# sourceMappingURL=13993.12686bc870b73d0f.js.map