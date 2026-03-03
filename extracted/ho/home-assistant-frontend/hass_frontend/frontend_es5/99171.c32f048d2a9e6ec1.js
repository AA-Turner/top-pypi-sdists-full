"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["99171"],{63130:function(e,t,a){a.d(t,{l:function(){return i}});a(3362);const i=async(e,t)=>{if(navigator.clipboard)try{return void(await navigator.clipboard.writeText(e))}catch(o){}const a=null!=t?t:document.body,i=document.createElement("textarea");i.value=e,a.appendChild(i),i.select(),document.execCommand("copy"),a.removeChild(i)}},93444:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845);let s,l,n=e=>e;class d extends o.WF{render(){return(0,o.qy)(s||(s=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(l||(l=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,i.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845);let s,l,n,d,h,c,p=e=>e;class g extends o.WF{render(){const e=(0,o.qy)(s||(s=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(l||(l=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(d||(d=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],g.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],g.prototype,"showBorder",void 0),g=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],g)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var i=a(40445),o=a(93900),r=a(96196),s=a(77845),l=a(32288),n=a(1087),d=a(64481),h=a(59992),c=a(14503),p=a(22348),g=(a(76538),a(26300)),u=e([o,g,h]);[o,g,h]=u.then?(await u)():u;let v,f,m,b,_,w,y,x=e=>e;const k="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class C extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(v||(v=x` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(f||(f=x` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",k,void 0!==this.headerTitle?(0,r.qy)(m||(m=x`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=x`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(_||(_=x`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(w||(w=x`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(y||(y=x`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,n.r)(this,"closed"))}}}(0,i.Cg)([(0,s.MZ)({attribute:!1})],C.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],C.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],C.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",void 0),(0,i.Cg)([(0,s.MZ)({reflect:!0})],C.prototype,"type",void 0),(0,i.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],C.prototype,"width",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],C.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-title"})],C.prototype,"headerTitle",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],C.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],C.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],C.prototype,"flexContent",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"without-header"})],C.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,s.wk)()],C.prototype,"_open",void 0),(0,i.Cg)([(0,s.P)(".body")],C.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,s.wk)()],C.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,s.Ls)({passive:!0})],C.prototype,"_handleBodyScroll",null),C=(0,i.Cg)([(0,s.EM)("ha-dialog")],C),t()}catch(v){t(v)}})},59992:function(e,t,a){a.a(e,async function(e,i){try{a.d(t,{V:function(){return u}});a(62953);var o=a(40445),r=a(88696),s=a(96196),l=a(94333),n=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let h,c,p=e=>e;const g=e=>void 0===e?[]:Array.isArray(e)?e:[e],u=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,s.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,l.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,l.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...g(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,s.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrollable",void 0),t};i()}catch(h){i(h)}})},72206:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaLongLivedAccessTokenDialog:function(){return V}});a(16280),a(18111),a(61701),a(3362),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(42762),a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(1087),n=a(63130),d=a(64481),h=a(38962),c=(a(75709),a(18350)),p=(a(93444),a(67094),a(72554)),g=a(81619),u=e([h,c,p]);[h,c,p]=u.then?(await u)():u;let v,f,m,b,_,w,y,x,k,C,S=e=>e;const $="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z",H="M3,11H5V13H3V11M11,5H13V9H11V5M9,11H13V15H11V13H9V11M15,11H17V13H19V11H21V13H19V15H21V19H19V21H17V19H13V21H11V17H15V15H17V13H15V11M19,19V15H17V19H19M15,3H21V9H15V3M17,5V7H19V5H17M3,3H9V9H3V3M5,5V7H7V5H5M3,15H9V21H3V15M5,17V19H7V17H5Z",M="/static/icons/favicon-192x192.png";class V extends r.WF{showDialog(e){this._createdCallback=e.createdCallback,this._existingNames=new Set(e.existingNames.map(e=>this._normalizeName(e))),this._renderDialog=!0,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._open=!1,this._renderDialog=!1,this._name="",this._token=void 0,this._existingNames=new Set,this._errorMessage=void 0,this._loading=!1,this._qrCode=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._renderDialog?(0,r.qy)(v||(v=S` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" prevent-scrim-close @closed="${0}"> <div class="content"> ${0} ${0} </div> <ha-dialog-footer slot="footer"> ${0} ${0} </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this._token?this.hass.localize("ui.panel.profile.long_lived_access_tokens.created_title",{name:this._name}):this.hass.localize("ui.panel.profile.long_lived_access_tokens.create"),this._dialogClosed,this._errorMessage?(0,r.qy)(f||(f=S`<ha-alert alert-type="error">${0}</ha-alert>`),this._errorMessage):r.s6,this._token?(0,r.qy)(m||(m=S` <p> ${0} </p> <div class="token-row"> <ha-textfield autofocus .value="${0}" type="text" readOnly="readOnly"></ha-textfield> <ha-button appearance="plain" @click="${0}"> <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> ${0} </ha-button> </div> <div id="qr"> ${0} </div> `),this.hass.localize("ui.panel.profile.long_lived_access_tokens.prompt_copy_token"),this._token,this._copyToken,$,this.hass.localize("ui.common.copy"),this._qrCode?this._qrCode:(0,r.qy)(b||(b=S` <ha-button appearance="plain" @click="${0}"> <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> ${0} </ha-button> `),this._generateQR,H,this.hass.localize("ui.panel.profile.long_lived_access_tokens.generate_qr_code"))):(0,r.qy)(_||(_=S` <ha-textfield autofocus .value="${0}" .label="${0}" .invalid="${0}" .errorMessage="${0}" required @input="${0}"></ha-textfield> `),this._name,this.hass.localize("ui.panel.profile.long_lived_access_tokens.name"),this._hasDuplicateName(),this.hass.localize("ui.panel.profile.long_lived_access_tokens.name_exists"),this._nameChanged),this._token?r.s6:(0,r.qy)(w||(w=S`<ha-button slot="secondaryAction" appearance="plain" @click="${0}"> ${0} </ha-button>`),this.closeDialog,this.hass.localize("ui.common.cancel")),this._token?(0,r.qy)(x||(x=S`<ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button>`),this.closeDialog,this.hass.localize("ui.common.close")):(0,r.qy)(y||(y=S`<ha-button slot="primaryAction" .disabled="${0}" @click="${0}"> ${0} </ha-button>`),this._isCreateDisabled(),this._createToken,this.hass.localize("ui.panel.profile.long_lived_access_tokens.create"))):r.s6}_nameChanged(e){this._name=e.currentTarget.value,this._errorMessage=void 0}_isCreateDisabled(){return this._loading||!this._name.trim()||this._hasDuplicateName()}async _createToken(){if(this._isCreateDisabled())return;const e=this._name.trim();this._loading=!0,this._errorMessage=void 0;try{this._token=await this.hass.callWS({type:"auth/long_lived_access_token",lifespan:3650,client_name:e}),this._name=e,this._createdCallback()}catch(t){this._errorMessage=t instanceof Error?t.message:String(t)}finally{this._loading=!1}}async _copyToken(){this._token&&(await(0,n.l)(this._token),(0,g.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")}))}_normalizeName(e){return e.trim().toLowerCase()}_hasDuplicateName(){return this._existingNames.has(this._normalizeName(this._name))}async _generateQR(){if(!this._token)return;const e=await a.e("51343").then(a.t.bind(a,81298,19)),t=await e.toCanvas(this._token,{width:512,errorCorrectionLevel:"Q"}),i=t.getContext("2d"),o=new Image;o.src=M,await new Promise(e=>{o.onload=e}),null==i||i.drawImage(o,t.width/3,t.height/3,t.width/3,t.height/3),await(0,d.J)(()=>{this._qrCode=(0,r.qy)(k||(k=S`<img alt="${0}" src="${0}">`),this.hass.localize("ui.panel.profile.long_lived_access_tokens.qr_code_image",{name:this._name}),t.toDataURL())})}static get styles(){return[(0,r.AH)(C||(C=S`#qr{text-align:center}#qr img{max-width:90%;height:auto;display:block;margin:0 auto}.content{display:grid;gap:var(--ha-space-4)}.token-row{display:flex;gap:var(--ha-space-2);align-items:center}.token-row ha-textfield{flex:1}p{margin:0}ha-textfield{display:block}`))]}constructor(...e){super(...e),this._open=!1,this._renderDialog=!1,this._name="",this._existingNames=new Set,this._loading=!1}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],V.prototype,"hass",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_qrCode",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_open",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_renderDialog",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_name",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_token",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_loading",void 0),(0,o.Cg)([(0,s.wk)()],V.prototype,"_errorMessage",void 0),V=(0,o.Cg)([(0,s.EM)("ha-long-lived-access-token-dialog")],V),i()}catch(v){i(v)}})},22348:function(e,t,a){a.d(t,{V:function(){return o}});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177:function(e,t,a){a.d(t,{n:function(){return i}});a(27495);const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=99171.c32f048d2a9e6ec1.js.map