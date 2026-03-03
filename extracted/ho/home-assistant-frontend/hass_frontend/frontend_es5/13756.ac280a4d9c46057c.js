"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["13756"],{64481:function(e,t,a){a.d(t,{D:function(){return i},J:function(){return r}});a(3362);let o=!1;try{o="true"===window.localStorage.getItem("disableViewTransition")}catch(l){}const i=e=>{o=e},r=e=>{if(!document.startViewTransition||o)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},93444:function(e,t,a){var o=a(40445),i=a(96196),r=a(77845);let l,s,d=e=>e;class n extends i.WF{render(){return(0,i.qy)(l||(l=d` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,i.AH)(s||(s=d`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}n=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],n)},76538:function(e,t,a){a(62953);var o=a(40445),i=a(96196),r=a(77845);let l,s,d,n,h,c,p=e=>e;class u extends i.WF{render(){const e=(0,i.qy)(l||(l=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(s||(s=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(d||(d=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(n||(n=p`${0}${0}`),t,e):(0,i.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],u)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var o=a(40445),i=a(93900),r=a(96196),l=a(77845),s=a(32288),d=a(1087),n=a(64481),h=a(59992),c=a(14503),p=a(22348),u=(a(76538),a(26300)),g=e([i,u,h]);[i,u,h]=g.then?(await g)():g;let v,f,b,m,w,y,_,x=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class $ extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(v||(v=x` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,s.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(f||(f=x` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(b||(b=x`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(m||(m=x`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(w||(w=x`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=x`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,n.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(_||(_=x`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,d.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,d.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,d.r)(this,"closed"))}}}(0,o.Cg)([(0,l.MZ)({attribute:!1})],$.prototype,"hass",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],$.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],$.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],$.prototype,"open",void 0),(0,o.Cg)([(0,l.MZ)({reflect:!0})],$.prototype,"type",void 0),(0,o.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],$.prototype,"width",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],$.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-title"})],$.prototype,"headerTitle",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],$.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],$.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],$.prototype,"flexContent",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,attribute:"without-header"})],$.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,l.wk)()],$.prototype,"_open",void 0),(0,o.Cg)([(0,l.P)(".body")],$.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,l.wk)()],$.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,l.Ls)({passive:!0})],$.prototype,"_handleBodyScroll",null),$=(0,o.Cg)([(0,l.EM)("ha-dialog")],$),t()}catch(v){t(v)}})},606:function(e,t,a){a.a(e,async function(e,t){try{a(18111),a(61701),a(62953);var o=a(40445),i=a(96196),r=a(77845),l=a(32288),s=a(22786),d=a(1087),n=a(29823),h=(a(70947),a(3449),a(88285)),c=(a(67094),e([n,h]));[n,h]=c.then?(await c)():c;let p,u,g,v,f,b,m,w,y,_=e=>e;class x extends i.WF{render(){return this.disabled?(0,i.qy)(p||(p=_`${0}${0}`),this._renderField(),this._renderHelper()):(0,i.qy)(u||(u=_` <ha-dropdown placement="bottom" @wa-select="${0}" @wa-show="${0}" @wa-hide="${0}"> ${0} ${0} </ha-dropdown> ${0} `),this._handleSelect,this._handleShow,this._handleHide,this._renderField(),this.options?this.options.map(e=>{var t;return(0,i.qy)(g||(g=_` <ha-dropdown-item .value="${0}" .disabled="${0}" .selected="${0}"> ${0} <div class="content"> ${0} ${0} </div> </ha-dropdown-item> `),"string"==typeof e?e:e.value,"string"!=typeof e&&(null!==(t=e.disabled)&&void 0!==t&&t),this.value===("string"==typeof e?e:e.value),e.iconPath?(0,i.qy)(v||(v=_`<ha-svg-icon slot="icon" .path="${0}"></ha-svg-icon>`),e.iconPath):i.s6,"string"==typeof e?e:e.label||e.value,e.secondary?(0,i.qy)(f||(f=_`<div class="secondary">${0}</div>`),e.secondary):i.s6)}):(0,i.qy)(b||(b=_`<slot></slot>`)),this._renderHelper())}_renderField(){const e=this._getValueLabel(this.options,this.value);return(0,i.qy)(m||(m=_` <ha-picker-field slot="trigger" type="button" class="${0}" compact="compact" aria-label="${0}" @clear="${0}" .label="${0}" .value="${0}" .required="${0}" .disabled="${0}" .hideClearIcon="${0}"> </ha-picker-field> `),this._opened?"opened":"",(0,l.J)(this.label),this._clearValue,this.label,e,this.required,this.disabled,!this.clearable||this.required||this.disabled||!this.value)}_renderHelper(){return this.helper?(0,i.qy)(w||(w=_`<ha-input-helper-text .disabled="${0}">${0}</ha-input-helper-text>`),this.disabled,this.helper):i.s6}_handleSelect(e){e.stopPropagation();const t=e.detail.item.value;t!==this.value&&(0,d.r)(this,"selected",{value:t})}_clearValue(){!this.disabled&&this.value&&(0,d.r)(this,"selected",{value:void 0})}_handleShow(){this.style.setProperty("--select-menu-width",`${this._triggerField.offsetWidth}px`),this._opened=!0}_handleHide(){this._opened=!1}constructor(...e){super(...e),this.clearable=!1,this.required=!1,this.disabled=!1,this._opened=!1,this._getValueLabel=(0,s.A)((e,t)=>{if(!e||!t)return t;for(const a of e)if("string"==typeof a&&a===t||"string"!=typeof a&&a.value===t)return"string"==typeof a?a:a.label||a.value;return t})}}x.styles=(0,i.AH)(y||(y=_`:host{position:relative}ha-picker-field.opened{--mdc-text-field-idle-line-color:var(--primary-color)}ha-dropdown-item .content{display:flex;gap:var(--ha-space-1);flex-direction:column}ha-dropdown-item .secondary{font-size:var(--ha-font-size-s);color:var(--ha-color-text-secondary)}ha-dropdown::part(menu){min-width:var(--select-menu-width)}ha-input-helper-text{display:block;margin:var(--ha-space-2) 0 0}`)),(0,o.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"clearable",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"options",void 0),(0,o.Cg)([(0,r.MZ)()],x.prototype,"label",void 0),(0,o.Cg)([(0,r.MZ)()],x.prototype,"helper",void 0),(0,o.Cg)([(0,r.MZ)()],x.prototype,"value",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"required",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"disabled",void 0),(0,o.Cg)([(0,r.wk)()],x.prototype,"_opened",void 0),(0,o.Cg)([(0,r.P)("ha-picker-field")],x.prototype,"_triggerField",void 0),x=(0,o.Cg)([(0,r.EM)("ha-select")],x),t()}catch(p){t(p)}})},59992:function(e,t,a){a.a(e,async function(e,o){try{a.d(t,{V:function(){return g}});a(62953);var i=a(40445),r=a(88696),l=a(96196),s=a(94333),d=a(77845),n=e([r]);r=(n.then?(await n)():n)[0];let h,c,p=e=>e;const u=e=>void 0===e?[]:Array.isArray(e)?e:[e],g=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,l.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...u(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,l.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,d.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,d.wk)()],t.prototype,"_contentScrollable",void 0),t};o()}catch(h){o(h)}})},99063:function(e,t,a){a.a(e,async function(e,o){try{a.r(t);a(74423),a(44114),a(26910),a(3362),a(27495),a(25440),a(62953);var i=a(40445),r=a(96196),l=a(77845),s=a(1087),d=a(18350),n=(a(93444),a(606)),h=a(72554),c=a(82e3),p=a(90600),u=a(14503),g=a(30039),v=e([d,n,h]);[d,n,h]=v.then?(await v)():v;let f,b,m=e=>e;const w=500;class y extends r.WF{showDialog(e){var t;this._dialogParams=e,this._lineCount=(null===(t=this._dialogParams)||void 0===t?void 0:t.defaultLineCount)||w,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._dialogParams=void 0,this._lineCount=w,(0,s.r)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._dialogParams)return r.s6;const e=[100,500,1e3,5e3,1e4];!e.includes(this._lineCount)&&this._lineCount&&(e.push(this._lineCount),e.sort((e,t)=>e-t));const t=`${this._dialogParams.header}${0===this._dialogParams.boot?"":` · ${-1===this._dialogParams.boot?this.hass.localize("ui.panel.config.logs.previous"):this.hass.localize("ui.panel.config.logs.startups_ago",{boot:-1*this._dialogParams.boot})}`}`;return(0,r.qy)(f||(f=m` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" header-subtitle="${0}" width="small" @closed="${0}"> <div class="content"> <div> ${0}: </div> <ha-select .label="${0}" @selected="${0}" .value="${0}" .options="${0}"></ha-select> </div> <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this.hass.localize("ui.panel.config.logs.download_logs"),t,this._dialogClosed,this.hass.localize("ui.panel.config.logs.select_number_of_lines"),this.hass.localize("ui.panel.config.logs.lines"),this._setNumberOfLogs,String(this._lineCount),e.map(e=>String(e)),this.closeDialog,this.hass.localize("ui.common.cancel"),this._downloadLogs,this.hass.localize("ui.common.download"))}async _downloadLogs(){const e=this._dialogParams.provider,t=this._dialogParams.boot,a=(new Date).toISOString().replace(/:/g,"-"),o=(0,p.Yd)(e,this._lineCount,t),i="core"!==e?`${e}_${a}.log`:`home-assistant_${a}.log`,r=await(0,c.e0)(this.hass,o);(0,g.R)(r.path,i),this.closeDialog()}_setNumberOfLogs(e){this._lineCount=Number(e.detail.value)}static get styles(){return[u.RF,u.nA,(0,r.AH)(b||(b=m`:host{direction:var(--direction)}.content{display:flex;flex-direction:column;align-items:center;gap:var(--ha-space-2)}ha-select{width:100%}`))]}constructor(...e){super(...e),this._open=!1,this._lineCount=w}}(0,i.Cg)([(0,l.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,i.Cg)([(0,l.wk)()],y.prototype,"_dialogParams",void 0),(0,i.Cg)([(0,l.wk)()],y.prototype,"_open",void 0),(0,i.Cg)([(0,l.wk)()],y.prototype,"_lineCount",void 0),y=(0,i.Cg)([(0,l.EM)("dialog-download-logs")],y),o()}catch(f){o(f)}})},22348:function(e,t,a){a.d(t,{V:function(){return i}});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177:function(e,t,a){a.d(t,{n:function(){return o}});a(27495);const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=13756.ac280a4d9c46057c.js.map