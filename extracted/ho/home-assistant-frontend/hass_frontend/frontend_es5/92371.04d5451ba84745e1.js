/*! For license information please see 92371.04d5451ba84745e1.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["92371"],{12587:function(e,t,a){a.d(t,{E:function(){return i},m:function(){return o}});a(3362);const o=e=>{requestAnimationFrame(()=>setTimeout(e,0))},i=()=>new Promise(e=>{o(e)})},64481:function(e,t,a){a.d(t,{D:function(){return i},J:function(){return r}});a(3362);let o=!1;try{o="true"===window.localStorage.getItem("disableViewTransition")}catch{}const i=e=>{o=e},r=e=>{if(!document.startViewTransition||o)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},85858:function(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{HaDialogDatePicker:function(){return w}});a(3362),a(62953);var i=a(40445),r=a(35769),n=a(67868),l=a(96196),s=a(77845),d=a(1087),h=a(12587),c=a(14503),u=a(18350),p=(a(93444),a(72554)),g=e([r,u,p]);[r,u,p]=g.then?(await g)():g;let f,v,m,b=e=>e;class w extends l.WF{async showDialog(e){await(0,h.E)(),this._params=e,this._value=e.value,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._params=void 0,(0,d.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params?(0,l.qy)(f||(f=b`<ha-dialog .hass="${0}" .open="${0}" width="small" without-header @closed="${0}"> <app-datepicker .value="${0}" .min="${0}" .max="${0}" .locale="${0}" @datepicker-value-updated="${0}" .firstDayOfWeek="${0}"></app-datepicker> <div class="bottom-actions"> ${0} <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> </div> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-dialog>`),this.hass,this._open,this._dialogClosed,this._value,this._params.min,this._params.max,this._params.locale,this._valueChanged,this._params.firstWeekday,this._params.canClear?(0,l.qy)(v||(v=b`<ha-button slot="secondaryAction" @click="${0}" variant="danger" appearance="plain"> ${0} </ha-button>`),this._clear,this.hass.localize("ui.dialogs.date-picker.clear")):l.s6,this._setToday,this.hass.localize("ui.dialogs.date-picker.today"),this.closeDialog,this.hass.localize("ui.common.cancel"),this._setValue,this.hass.localize("ui.common.ok")):l.s6}_valueChanged(e){this._value=e.detail.value}_clear(){var e;null===(e=this._params)||void 0===e||e.onChange(void 0),this.closeDialog()}_setToday(){const e=new Date;this._value=(0,n.GP)(e,"yyyy-MM-dd")}_setValue(){var e;this._value||this._setToday(),null===(e=this._params)||void 0===e||e.onChange(this._value),this.closeDialog()}constructor(...e){super(...e),this.disabled=!1,this._open=!1}}w.styles=[c.nA,(0,l.AH)(m||(m=b`ha-dialog{--dialog-content-padding:0}.bottom-actions{display:flex;gap:var(--ha-space-4);justify-content:center;align-items:center;width:100%;margin-bottom:var(--ha-space-1)}app-datepicker{display:block;margin-inline:auto;--app-datepicker-accent-color:var(--primary-color);--app-datepicker-bg-color:transparent;--app-datepicker-color:var(--primary-text-color);--app-datepicker-disabled-day-color:var(--disabled-text-color);--app-datepicker-focused-day-color:var(--text-primary-color);--app-datepicker-focused-year-bg-color:var(--primary-color);--app-datepicker-selector-color:var(--secondary-text-color);--app-datepicker-separator-color:var(--divider-color);--app-datepicker-weekday-color:var(--secondary-text-color)}app-datepicker::part(calendar-day):focus{outline:0}app-datepicker::part(body){direction:ltr}@media all and (max-width:450px),all and (max-height:500px){app-datepicker{width:100%}}`))],(0,i.Cg)([(0,s.MZ)({attribute:!1})],w.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)()],w.prototype,"value",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],w.prototype,"disabled",void 0),(0,i.Cg)([(0,s.MZ)()],w.prototype,"label",void 0),(0,i.Cg)([(0,s.wk)()],w.prototype,"_params",void 0),(0,i.Cg)([(0,s.wk)()],w.prototype,"_open",void 0),(0,i.Cg)([(0,s.wk)()],w.prototype,"_value",void 0),w=(0,i.Cg)([(0,s.EM)("ha-dialog-date-picker")],w),o()}catch(f){o(f)}})},93444:function(e,t,a){var o=a(40445),i=a(96196),r=a(77845);let n,l,s=e=>e;class d extends i.WF{render(){return(0,i.qy)(n||(n=s` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,i.AH)(l||(l=s`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){a(62953);var o=a(40445),i=a(96196),r=a(77845);let n,l,s,d,h,c,u=e=>e;class p extends i.WF{render(){const e=(0,i.qy)(n||(n=u`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(l||(l=u`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(s||(s=u` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(d||(d=u`${0}${0}`),t,e):(0,i.qy)(h||(h=u`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(c||(c=u`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],p.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],p.prototype,"showBorder",void 0),p=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],p)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var o=a(40445),i=a(93900),r=a(96196),n=a(77845),l=a(32288),s=a(1087),d=a(64481),h=a(59992),c=a(14503),u=a(22348),p=(a(76538),a(26300)),g=e([i,p,h]);[i,p,h]=g.then?(await g)():g;let f,v,m,b,w,y,x,_=e=>e;const k="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class C extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(f||(f=_` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(v||(v=_` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",k,void 0!==this.headerTitle?(0,r.qy)(m||(m=_`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=_`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(w||(w=_`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=_`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(x||(x=_`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,s.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,u.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,s.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,s.r)(this,"closed"))}}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],C.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-labelledby"})],C.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-describedby"})],C.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",void 0),(0,o.Cg)([(0,n.MZ)({reflect:!0})],C.prototype,"type",void 0),(0,o.Cg)([(0,n.MZ)({type:String,reflect:!0,attribute:"width"})],C.prototype,"width",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],C.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-title"})],C.prototype,"headerTitle",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-subtitle"})],C.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"header-subtitle-position"})],C.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],C.prototype,"flexContent",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"without-header"})],C.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,n.wk)()],C.prototype,"_open",void 0),(0,o.Cg)([(0,n.P)(".body")],C.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,n.wk)()],C.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,n.Ls)({passive:!0})],C.prototype,"_handleBodyScroll",null),C=(0,o.Cg)([(0,n.EM)("ha-dialog")],C),t()}catch(f){t(f)}})},59992:function(e,t,a){a.a(e,async function(e,o){try{a.d(t,{V:function(){return g}});a(62953);var i=a(40445),r=a(88696),n=a(96196),l=a(94333),s=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let h,c,u=e=>e;const p=e=>void 0===e?[]:Array.isArray(e)?e:[e],g=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,n.qy)(h||(h=u` <div class="${0}"></div> <div class="${0}"></div> `),(0,l.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,l.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...p(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,n.AH)(c||(c=u`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,s.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,s.wk)()],t.prototype,"_contentScrollable",void 0),t};o()}catch(h){o(h)}})},69235:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953);"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await a.e("71055").then(a.bind(a,52370))).default),t()}catch(o){t(o)}},1)},14503:function(e,t,a){a.d(t,{RF:function(){return u},dp:function(){return f},kO:function(){return g},nA:function(){return p},og:function(){return c}});var o=a(96196);let i,r,n,l,s,d,h=e=>e;const c=(0,o.AH)(i||(i=h`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`)),u=(0,o.AH)(r||(r=h`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${0} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`),c),p=(0,o.AH)(n||(n=h`
  ha-dialog,
  ha-adaptive-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
    --dialog-container-padding: var(--safe-area-inset-top, 0)
      var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
      var(--safe-area-inset-left, 0);
    --dialog-surface-padding: 0px;
  }

  ha-dialog .form,
  ha-adaptive-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog,
    ha-adaptive-dialog {
      --mdc-dialog-min-width: 100vw;
      --mdc-dialog-max-width: 100vw;
      --mdc-dialog-min-height: 100vh;
      --mdc-dialog-min-height: 100svh;
      --mdc-dialog-max-height: 100vh;
      --mdc-dialog-max-height: 100svh;
      --dialog-container-padding: 0px;
      --dialog-surface-padding: var(--safe-area-inset-top, 0)
        var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
        var(--safe-area-inset-left, 0);
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: var(--ha-border-radius-square);
    ha-dialog,
    ha-adaptive-dialog {
     --mdc-dialog-min-width: 100vw;
     --mdc-dialog-max-width: 100vw;
     --mdc-dialog-min-height: 100vh;
     --mdc-dialog-min-height: 100svh;
     --mdc-dialog-max-height: 100vh;
     --mdc-dialog-max-height: 100svh;
     --dialog-container-padding: 0px;
     --dialog-surface-padding: var(--safe-area-inset-top, 0)
       var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
       var(--safe-area-inset-left, 0);
     --vertical-align-dialog: flex-end;
   }
   ha-dialog {
      --ha-dialog-border-radius: var(--ha-border-radius-square);
   }
  }
  .error {
    color: var(--error-color);
  }
`)),g=(0,o.AH)(l||(l=h`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
      100vh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--mdc-dialog-max-height:calc(
      100svh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--ha-dialog-max-height:calc(
      100vh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--ha-dialog-max-height:calc(
      100svh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`)),f=(0,o.AH)(s||(s=h`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`));(0,o.AH)(d||(d=h`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`))},22348:function(e,t,a){a.d(t,{V:function(){return i}});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177:function(e,t,a){a.d(t,{n:function(){return o}});a(27495);const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},93900:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(27495),a(62953);var o=a(96196),i=a(77845),r=a(94333),n=a(32288),l=a(17051),s=a(42462),d=a(28438),h=a(98779),c=a(27259),u=a(31247),p=a(93949),g=a(92070),f=a(9395),v=a(12754),m=a(17060),b=a(88496),w=a(91470),y=e([b,m]);[b,m]=y.then?(await y)():y;let C,$,A,S=e=>e;var x=Object.defineProperty,_=Object.getOwnPropertyDescriptor,k=(e,t,a,o)=>{for(var i,r=o>1?void 0:o?_(t,a):t,n=e.length-1;n>=0;n--)(i=e[n])&&(r=(o?i(t,a,r):i(r))||r);return o&&r&&x(t,a,r),r};let E=class extends v.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,p.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,p.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,p.I7)(this);const a=this.originalTrigger;"function"==typeof(null==a?void 0:a.focus)&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new h.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,p.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new s.q))}render(){var e;const t=!this.withoutHeader,a=this.hasSlotController.test("footer");return(0,o.qy)(C||(C=S` <dialog aria-labelledby="${0}" aria-describedby="${0}" part="dialog" class="${0}" @cancel="${0}" @click="${0}" @pointerdown="${0}"> ${0} <div part="body" class="body"><slot></slot></div> ${0} </dialog> `),null!==(e=this.ariaLabelledby)&&void 0!==e?e:"title",(0,n.J)(this.ariaDescribedby),(0,r.H)({dialog:!0,open:this.open}),this.handleDialogCancel,this.handleDialogClick,this.handleDialogPointerDown,t?(0,o.qy)($||($=S` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${0} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${0}"> <wa-icon name="xmark" label="${0}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `),this.label.length>0?this.label:String.fromCharCode(8203),e=>this.requestClose(e.target),this.localize.term("close")):"",a?(0,o.qy)(A||(A=S` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `)):"")}constructor(){super(...arguments),this.localize=new m.c(this),this.hasSlotController=new g.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};E.css=w.A,k([(0,i.P)(".dialog")],E.prototype,"dialog",2),k([(0,i.MZ)({type:Boolean,reflect:!0})],E.prototype,"open",2),k([(0,i.MZ)({reflect:!0})],E.prototype,"label",2),k([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],E.prototype,"withoutHeader",2),k([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],E.prototype,"lightDismiss",2),k([(0,i.MZ)({attribute:"aria-labelledby"})],E.prototype,"ariaLabelledby",2),k([(0,i.MZ)({attribute:"aria-describedby"})],E.prototype,"ariaDescribedby",2),k([(0,f.w)("open",{waitUntilFirstUpdate:!0})],E.prototype,"handleOpenChange",1),E=k([(0,i.EM)("wa-dialog")],E),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,u.v)(t.getAttribute("data-dialog")||"");if("open"===e&&null!=a&&a.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===(null==e?void 0:e.localName)?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(C){t(C)}})},91470:function(e,t,a){a.d(t,{A:function(){return i}});let o;var i=(0,a(96196).AH)(o||(o=(e=>e)`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`))},17051:function(e,t,a){a.d(t,{Z:function(){return o}});class o extends Event{constructor(){super("wa-after-hide",{bubbles:!0,cancelable:!1,composed:!0})}}},42462:function(e,t,a){a.d(t,{q:function(){return o}});class o extends Event{constructor(){super("wa-after-show",{bubbles:!0,cancelable:!1,composed:!0})}}},28438:function(e,t,a){a.d(t,{L:function(){return o}});class o extends Event{constructor(e){super("wa-hide",{bubbles:!0,cancelable:!0,composed:!0}),this.detail=e}}},98779:function(e,t,a){a.d(t,{k:function(){return o}});class o extends Event{constructor(){super("wa-show",{bubbles:!0,cancelable:!0,composed:!0})}}},27259:function(e,t,a){a.d(t,{E9:function(){return r},Ud:function(){return i},i0:function(){return o}});a(3362);async function o(e,t,a){return e.animate(t,a).finished.catch(()=>{})}function i(e,t){return new Promise(a=>{const o=new AbortController,{signal:i}=o;if(e.classList.contains(t))return;e.classList.add(t);let r=!1,n=()=>{r||(r=!0,e.classList.remove(t),a(),o.abort())};e.addEventListener("animationend",n,{once:!0,signal:i}),e.addEventListener("animationcancel",n,{once:!0,signal:i}),requestAnimationFrame(()=>{r||0!==e.getAnimations().length||n()})})}function r(e){return(e=e.toString().toLowerCase()).indexOf("ms")>-1?parseFloat(e)||0:e.indexOf("s")>-1?1e3*(parseFloat(e)||0):parseFloat(e)||0}},31247:function(e,t,a){a.d(t,{v:function(){return o}});a(18111),a(22489),a(61701),a(42762);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},93949:function(e,t,a){a.d(t,{Rt:function(){return n},I7:function(){return r},JG:function(){return i}});a(27495),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(25440),a(62953);const o=new Set;function i(e){if(o.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function r(e){o.delete(e),0===o.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function n(e,t,a="vertical",o="smooth"){const i=function(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}(e,t),r=i.top+t.scrollTop,n=i.left+t.scrollLeft,l=t.scrollLeft,s=t.scrollLeft+t.offsetWidth,d=t.scrollTop,h=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(n<l?t.scrollTo({left:n,behavior:o}):n+e.clientWidth>s&&t.scrollTo({left:n-t.offsetWidth+e.clientWidth,behavior:o})),"vertical"!==a&&"both"!==a||(r<d?t.scrollTo({top:r,behavior:o}):r+e.clientHeight>h&&t.scrollTo({top:r-t.offsetHeight+e.clientHeight,behavior:o}))}},88696:function(e,t,a){a.a(e,async function(e,o){try{a.d(t,{P:function(){return s}});var i=a(69235),r=(a(3362),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(62953),a(37540)),n=a(42017),l=e([i]);i=(l.then?(await l)():l)[0];class s{handleChanges(e){var t;this.value=null===(t=this.callback)||void 0===t?void 0:t.call(this,e,this.u)}hostConnected(){for(const e of this.t)this.observe(e)}hostDisconnected(){this.disconnect()}async hostUpdated(){!this.o&&this.i&&this.handleChanges([]),this.i=!1}observe(e){this.t.add(e),this.u.observe(e,this.l),this.i=!0,this.h.requestUpdate()}unobserve(e){this.t.delete(e),this.u.unobserve(e)}disconnect(){this.u.disconnect()}target(e){return d(this,e)}constructor(e,{target:t,config:a,callback:o,skipInitial:i}){this.t=new Set,this.o=!1,this.i=!1,this.h=e,null!==t&&this.t.add(null!=t?t:e),this.l=a,this.o=null!=i?i:this.o,this.callback=o,window.ResizeObserver?(this.u=new ResizeObserver(e=>{this.handleChanges(e),this.h.requestUpdate()}),e.addController(this)):console.warn("ResizeController error: browser does not support ResizeObserver.")}}const d=(0,n.u$)(class extends r.Kq{render(e,t){}update(e,[t,a]){this.controller=t,this.part=e,this.observe=a,!1===a?(t.unobserve(e.element),this.observing=!1):!1===this.observing&&(t.observe(e.element),this.observing=!0)}disconnected(){var e;null!==(e=this.controller)&&void 0!==e&&e.unobserve(this.part.element),this.observing=!1}reconnected(){var e;!1!==this.observe&&!1===this.observing&&(null!==(e=this.controller)&&void 0!==e&&e.observe(this.part.element),this.observing=!0)}constructor(){super(...arguments),this.observing=!1}});o()}catch(s){o(s)}})},2045:function(e,t,a){a.d(t,{q:function(){return i}});let o={};function i(){return o}},74816:function(e,t,a){a.d(t,{x:function(){return i}});a(18111),a(20116),a(61701);var o=a(73420);function i(e,...t){const a=o.w.bind(null,e||t.find(e=>"object"==typeof e));return t.map(a)}},9160:function(e,t,a){a.d(t,{_P:function(){return n},my:function(){return o},s0:function(){return r},w4:function(){return i}});Math.pow(10,8);const o=6048e5,i=864e5,r=36e5,n=Symbol.for("constructDateFrom")},73420:function(e,t,a){a.d(t,{w:function(){return i}});var o=a(9160);function i(e,t){return"function"==typeof e?e(t):e&&"object"==typeof e&&o._P in e?e[o._P](t):e instanceof Date?new e.constructor(t):new Date(t)}},3952:function(e,t,a){a.d(t,{m:function(){return s}});a(62953);var o=a(83504);function i(e){const t=(0,o.a)(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return a.setUTCFullYear(t.getFullYear()),+e-+a}var r=a(74816),n=a(9160),l=a(35932);function s(e,t,a){const[o,s]=(0,r.x)(null==a?void 0:a.in,e,t),d=(0,l.o)(o),h=(0,l.o)(s),c=+d-i(d),u=+h-i(h);return Math.round((c-u)/n.w4)}},35932:function(e,t,a){a.d(t,{o:function(){return i}});var o=a(83504);function i(e,t){const a=(0,o.a)(e,null==t?void 0:t.in);return a.setHours(0,0,0,0),a}},52640:function(e,t,a){a.d(t,{k:function(){return r}});var o=a(2045),i=a(83504);function r(e,t){var a,r,n,l,s,d;const h=(0,o.q)(),c=null!==(a=null!==(r=null!==(n=null!==(l=null==t?void 0:t.weekStartsOn)&&void 0!==l?l:null==t||null===(s=t.locale)||void 0===s||null===(s=s.options)||void 0===s?void 0:s.weekStartsOn)&&void 0!==n?n:h.weekStartsOn)&&void 0!==r?r:null===(d=h.locale)||void 0===d||null===(d=d.options)||void 0===d?void 0:d.weekStartsOn)&&void 0!==a?a:0,u=(0,i.a)(e,null==t?void 0:t.in),p=u.getDay(),g=(p<c?7:0)+p-c;return u.setDate(u.getDate()-g),u.setHours(0,0,0,0),u}},83504:function(e,t,a){a.d(t,{a:function(){return i}});var o=a(73420);function i(e,t){return(0,o.w)(t||e,e)}},37540:function(e,t,a){a.d(t,{Kq:function(){return c}});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(62953);var o=a(63937),i=a(42017);const r=(e,t)=>{const a=e._$AN;if(void 0===a)return!1;for(const i of a){var o;null!==(o=i._$AO)&&void 0!==o&&o.call(i,t,!1),r(i,t)}return!0},n=e=>{let t,a;do{var o;if(void 0===(t=e._$AM))break;a=t._$AN,a.delete(e),e=t}while(0===(null===(o=a)||void 0===o?void 0:o.size))},l=e=>{for(let t;t=e._$AM;e=t){let a=t._$AN;if(void 0===a)t._$AN=a=new Set;else if(a.has(e))break;a.add(e),h(t)}};function s(e){void 0!==this._$AN?(n(this),this._$AM=e,l(this)):this._$AM=e}function d(e,t=!1,a=0){const o=this._$AH,i=this._$AN;if(void 0!==i&&0!==i.size)if(t)if(Array.isArray(o))for(let l=a;l<o.length;l++)r(o[l],!1),n(o[l]);else null!=o&&(r(o,!1),n(o));else r(this,e)}const h=e=>{var t,a;e.type==i.OA.CHILD&&(null!==(t=e._$AP)&&void 0!==t||(e._$AP=d),null!==(a=e._$AQ)&&void 0!==a||(e._$AQ=s))};class c extends i.WL{_$AT(e,t,a){super._$AT(e,t,a),l(this),this.isConnected=e._$AU}_$AO(e,t=!0){var a,o;e!==this.isConnected&&(this.isConnected=e,e?null===(a=this.reconnected)||void 0===a||a.call(this):null===(o=this.disconnected)||void 0===o||o.call(this)),t&&(r(this,e),n(this))}setValue(e){if((0,o.Rt)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}constructor(){super(...arguments),this._$AN=void 0}}},4937:function(e,t,a){a.d(t,{u:function(){return l}});a(16280),a(45367),a(92731),a(62953);var o=a(5055),i=a(42017),r=a(63937);const n=(e,t,a)=>{const o=new Map;for(let i=t;i<=a;i++)o.set(e[i],i);return o},l=(0,i.u$)(class extends i.WL{dt(e,t,a){let o;void 0===a?a=t:void 0!==t&&(o=t);const i=[],r=[];let n=0;for(const l of e)i[n]=o?o(l,n):n,r[n]=a(l,n),n++;return{values:r,keys:i}}render(e,t,a){return this.dt(e,t,a).values}update(e,[t,a,i]){var l;const s=(0,r.cN)(e),{values:d,keys:h}=this.dt(t,a,i);if(!Array.isArray(s))return this.ut=h,d;const c=null!==(l=this.ut)&&void 0!==l?l:this.ut=[],u=[];let p,g,f=0,v=s.length-1,m=0,b=d.length-1;for(;f<=v&&m<=b;)if(null===s[f])f++;else if(null===s[v])v--;else if(c[f]===h[m])u[m]=(0,r.lx)(s[f],d[m]),f++,m++;else if(c[v]===h[b])u[b]=(0,r.lx)(s[v],d[b]),v--,b--;else if(c[f]===h[b])u[b]=(0,r.lx)(s[f],d[b]),(0,r.Dx)(e,u[b+1],s[f]),f++,b--;else if(c[v]===h[m])u[m]=(0,r.lx)(s[v],d[m]),(0,r.Dx)(e,s[f],s[v]),v--,m++;else if(void 0===p&&(p=n(h,m,b),g=n(c,f,v)),p.has(c[f]))if(p.has(c[v])){const t=g.get(h[m]),a=void 0!==t?s[t]:null;if(null===a){const t=(0,r.Dx)(e,s[f]);(0,r.lx)(t,d[m]),u[m]=t}else u[m]=(0,r.lx)(a,d[m]),(0,r.Dx)(e,s[f],a),s[t]=null;m++}else(0,r.KO)(s[v]),v--;else(0,r.KO)(s[f]),f++;for(;m<=b;){const t=(0,r.Dx)(e,u[b+1]);(0,r.lx)(t,d[m]),u[m++]=t}for(;f<=v;){const e=s[f++];null!==e&&(0,r.KO)(e)}return this.ut=h,(0,r.mY)(e,u),o.c0}constructor(e){if(super(e),e.type!==i.OA.CHILD)throw Error("repeat() can only be used in text expressions")}})}}]);
//# sourceMappingURL=92371.04d5451ba84745e1.js.map