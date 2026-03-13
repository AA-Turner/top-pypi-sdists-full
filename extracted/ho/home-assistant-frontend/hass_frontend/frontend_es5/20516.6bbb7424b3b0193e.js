"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["20516"],{64481:function(e,t,a){a.d(t,{D:function(){return o},J:function(){return r}});a(3362);let i=!1;try{i="true"===window.localStorage.getItem("disableViewTransition")}catch{}const o=e=>{i=e},r=e=>{if(!document.startViewTransition||i)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},76538:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845);let l,s,n,d,h,c,p=e=>e;class g extends o.WF{render(){const e=(0,o.qy)(l||(l=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(s||(s=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(d||(d=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],g.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],g.prototype,"showBorder",void 0),g=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],g)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var i=a(40445),o=a(93900),r=a(96196),l=a(77845),s=a(32288),n=a(1087),d=a(64481),h=a(59992),c=a(14503),p=a(22348),g=(a(76538),a(26300)),u=e([o,g,h]);[o,g,h]=u.then?(await u)():u;let v,m,f,b,w,y,_,x=e=>e;const S="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class C extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(v||(v=x` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,s.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(m||(m=x` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",S,void 0!==this.headerTitle?(0,r.qy)(f||(f=x`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=x`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(w||(w=x`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=x`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(_||(_=x`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,n.r)(this,"closed"))}}}(0,i.Cg)([(0,l.MZ)({attribute:!1})],C.prototype,"hass",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],C.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],C.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",void 0),(0,i.Cg)([(0,l.MZ)({reflect:!0})],C.prototype,"type",void 0),(0,i.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],C.prototype,"width",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],C.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-title"})],C.prototype,"headerTitle",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],C.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],C.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],C.prototype,"flexContent",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,attribute:"without-header"})],C.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,l.wk)()],C.prototype,"_open",void 0),(0,i.Cg)([(0,l.P)(".body")],C.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,l.wk)()],C.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,l.Ls)({passive:!0})],C.prototype,"_handleBodyScroll",null),C=(0,i.Cg)([(0,l.EM)("ha-dialog")],C),t()}catch(v){t(v)}})},28732:function(e,t,a){var i=a(40445),o=a(27686),r=a(7731),l=a(96196),s=a(77845);let n,d,h,c=e=>e;class p extends o.J{renderRipple(){return this.noninteractive?"":super.renderRipple()}static get styles(){return[r.R,(0,l.AH)(n||(n=c`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`)),"rtl"===document.dir?(0,l.AH)(d||(d=c`span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}`)):(0,l.AH)(h||(h=c``))]}}p=(0,i.Cg)([(0,s.EM)("ha-list-item")],p)},8630:function(e,t,a){var i=a(40445),o=a(70402),r=a(11081),l=a(77845);class s extends o.iY{}s.styles=r.R,s=(0,i.Cg)([(0,l.EM)("ha-list")],s)},59992:function(e,t,a){a.a(e,async function(e,i){try{a.d(t,{V:function(){return u}});a(62953);var o=a(40445),r=a(88696),l=a(96196),s=a(94333),n=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let h,c,p=e=>e;const g=e=>void 0===e?[]:Array.isArray(e)?e:[e],u=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,l.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...g(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,l.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,n.wk)()],t.prototype,"_contentScrollable",void 0),t};i()}catch(h){i(h)}})},39535:function(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(3362),a(62953);var o=a(40445),r=a(96196),l=a(77845),s=a(1087),n=a(72554),d=(a(8630),a(28732),e([n]));n=(d.then?(await d)():d)[0];let h,c,p=e=>e;const g="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class u extends r.WF{async showDialog(e){this.localize=e.localize,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this.localize=void 0,(0,s.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this.localize?(0,r.qy)(h||(h=p`<ha-dialog .open="${0}" header-title="${0}" @closed="${0}"> <ha-list> <a target="_blank" rel="noreferrer noopener" href="https://community.home-assistant.io/"> <ha-list-item hasMeta graphic="icon"> <img src="/static/icons/favicon-192x192.png" slot="graphic" alt="Home Assistant Logo"> ${0} <ha-svg-icon slot="meta" .path="${0}"></ha-svg-icon> </ha-list-item> </a> <a target="_blank" rel="noreferrer noopener" href="https://newsletter.openhomefoundation.org/"> <ha-list-item hasMeta graphic="icon"> <img src="/static/icons/logo_ohf.svg" slot="graphic" alt="Open Home Foundation Logo"> ${0} <ha-svg-icon slot="meta" .path="${0}"></ha-svg-icon> </ha-list-item> </a> <a target="_blank" rel="noreferrer noopener" href="https://www.home-assistant.io/join-chat"> <ha-list-item hasMeta graphic="icon"> <img src="/static/images/logo_discord.png" slot="graphic" alt="Discord Logo"> ${0} <ha-svg-icon slot="meta" .path="${0}"></ha-svg-icon> </ha-list-item> </a> <a target="_blank" rel="noreferrer noopener" href="https://fosstodon.org/@homeassistant"> <ha-list-item hasMeta graphic="icon"> <img src="/static/images/logo_mastodon.svg" slot="graphic" alt="Mastodon Logo"> ${0} <ha-svg-icon slot="meta" .path="${0}"></ha-svg-icon> </ha-list-item> </a> </ha-list> </ha-dialog>`),this._open,this.localize("ui.panel.page-onboarding.welcome.community"),this._dialogClosed,this.localize("ui.panel.page-onboarding.welcome.forums"),g,this.localize("ui.panel.page-onboarding.welcome.open_home_newsletter"),g,this.localize("ui.panel.page-onboarding.welcome.discord"),g,this.localize("ui.panel.page-onboarding.welcome.mastodon"),g):r.s6}constructor(...e){super(...e),this._open=!1}}u.styles=(0,r.AH)(c||(c=p`ha-dialog{--dialog-content-padding:0}ha-list-item{height:56px;--mdc-list-item-meta-size:20px}a{text-decoration:none}`)),(0,o.Cg)([(0,l.MZ)({attribute:!1})],u.prototype,"localize",void 0),(0,o.Cg)([(0,l.wk)()],u.prototype,"_open",void 0),u=(0,o.Cg)([(0,l.EM)("community-dialog")],u),i()}catch(h){i(h)}})},22348:function(e,t,a){a.d(t,{V:function(){return o}});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177:function(e,t,a){a.d(t,{n:function(){return i}});a(27495);const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=20516.6bbb7424b3b0193e.js.map