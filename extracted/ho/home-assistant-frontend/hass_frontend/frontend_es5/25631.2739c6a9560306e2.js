"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["25631"],{64481:function(e,t,a){a.d(t,{D:function(){return o},J:function(){return r}});a(3362);let i=!1;try{i="true"===window.localStorage.getItem("disableViewTransition")}catch(l){}const o=e=>{i=e},r=e=>{if(!document.startViewTransition||i)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},76538:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845);let l,n,d,s,h,c,p=e=>e;class u extends o.WF{render(){const e=(0,o.qy)(l||(l=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(n||(n=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(d||(d=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(s||(s=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],u)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var i=a(40445),o=a(93900),r=a(96196),l=a(77845),n=a(32288),d=a(1087),s=a(64481),h=a(59992),c=a(14503),p=a(22348),u=(a(76538),a(26300)),f=e([o,u,h]);[o,u,h]=f.then?(await f)():f;let g,v,m,b,x,y,w,_=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class S extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(g||(g=_` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,n.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(v||(v=_` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(m||(m=_`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=_`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(x||(x=_`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(y||(y=_`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,s.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(w||(w=_`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,d.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,d.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,d.r)(this,"closed"))}}}(0,i.Cg)([(0,l.MZ)({attribute:!1})],S.prototype,"hass",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],S.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],S.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],S.prototype,"open",void 0),(0,i.Cg)([(0,l.MZ)({reflect:!0})],S.prototype,"type",void 0),(0,i.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],S.prototype,"width",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],S.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-title"})],S.prototype,"headerTitle",void 0),(0,i.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],S.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],S.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],S.prototype,"flexContent",void 0),(0,i.Cg)([(0,l.MZ)({type:Boolean,attribute:"without-header"})],S.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,l.wk)()],S.prototype,"_open",void 0),(0,i.Cg)([(0,l.P)(".body")],S.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,l.wk)()],S.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,l.Ls)({passive:!0})],S.prototype,"_handleBodyScroll",null),S=(0,i.Cg)([(0,l.EM)("ha-dialog")],S),t()}catch(g){t(g)}})},11382:function(e,t,a){a(3362),a(62953);var i=a(40445),o=a(96196),r=a(77845),l=a(94333),n=a(1087),d=a(12587);a(67094);let s,h,c,p,u=e=>e;class f extends o.WF{render(){const e=this.noCollapse?o.s6:(0,o.qy)(s||(s=u` <ha-svg-icon .path="${0}" class="summary-icon ${0}"></ha-svg-icon> `),"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z",(0,l.H)({expanded:this.expanded}));return(0,o.qy)(h||(h=u` <div class="top ${0}"> <div id="summary" class="${0}" @click="${0}" @keydown="${0}" @focus="${0}" @blur="${0}" role="button" tabindex="${0}" aria-expanded="${0}" aria-controls="sect1" part="summary"> ${0} <slot name="leading-icon"></slot> <slot name="header"> <div class="header"> ${0} <slot class="secondary" name="secondary">${0}</slot> </div> </slot> ${0} <slot name="icons"></slot> </div> </div> <div class="container ${0}" @transitionend="${0}" role="region" aria-labelledby="summary" aria-hidden="${0}" tabindex="-1"> ${0} </div> `),(0,l.H)({expanded:this.expanded}),(0,l.H)({noCollapse:this.noCollapse}),this._toggleContainer,this._toggleContainer,this._focusChanged,this._focusChanged,this.noCollapse?-1:0,this.expanded,this.leftChevron?e:o.s6,this.header,this.secondary,this.leftChevron?o.s6:e,(0,l.H)({expanded:this.expanded}),this._handleTransitionEnd,!this.expanded,this._showContent?(0,o.qy)(c||(c=u`<slot></slot>`)):"")}willUpdate(e){super.willUpdate(e),e.has("expanded")&&(this._showContent=this.expanded,setTimeout(()=>{this._container.style.overflow=this.expanded?"initial":"hidden"},300))}_handleTransitionEnd(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}async _toggleContainer(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,n.r)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,d.E)());const a=this._container.scrollHeight;this._container.style.height=`${a}px`,t||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=t,(0,n.r)(this,"expanded-changed",{expanded:this.expanded})}_focusChanged(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}constructor(...e){super(...e),this.expanded=!1,this.outlined=!1,this.leftChevron=!1,this.noCollapse=!1,this._showContent=this.expanded}}f.styles=(0,o.AH)(p||(p=u`:host{display:block}.top{display:flex;align-items:center;border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg))}.top.expanded{border-bottom-left-radius:0px;border-bottom-right-radius:0px}.top.focused{background:var(--input-fill-color)}:host([outlined]){box-shadow:none;border-width:1px;border-style:solid;border-color:var(--outline-color);border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg))}.summary-icon{transition:transform 150ms cubic-bezier(.4, 0, .2, 1);direction:var(--direction);margin-left:8px;margin-inline-start:8px;margin-inline-end:initial;border-radius:var(--ha-border-radius-circle)}#summary:focus-visible ha-svg-icon.summary-icon{background-color:var(--ha-color-fill-neutral-normal-active)}::slotted([slot=leading-icon]),:host([left-chevron]) .summary-icon{margin-left:0;margin-right:8px;margin-inline-start:0;margin-inline-end:8px}#summary{flex:1;display:flex;padding:var(--expansion-panel-summary-padding,0 8px);min-height:48px;align-items:center;cursor:pointer;overflow:hidden;font-weight:var(--ha-font-weight-medium);outline:0}#summary.noCollapse{cursor:default}.summary-icon.expanded{transform:rotate(180deg)}.header,::slotted([slot=header]){flex:1;overflow-wrap:anywhere;color:var(--primary-text-color)}.container{padding:var(--expansion-panel-content-padding,0 8px);overflow:hidden;transition:height .3s cubic-bezier(.4, 0, .2, 1);height:0px}.container.expanded{height:auto}.secondary{display:block;color:var(--secondary-text-color);font-size:var(--ha-font-size-s)}`)),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],f.prototype,"expanded",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],f.prototype,"outlined",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"left-chevron",type:Boolean,reflect:!0})],f.prototype,"leftChevron",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"no-collapse",type:Boolean,reflect:!0})],f.prototype,"noCollapse",void 0),(0,i.Cg)([(0,r.MZ)()],f.prototype,"header",void 0),(0,i.Cg)([(0,r.MZ)()],f.prototype,"secondary",void 0),(0,i.Cg)([(0,r.wk)()],f.prototype,"_showContent",void 0),(0,i.Cg)([(0,r.P)(".container")],f.prototype,"_container",void 0),f=(0,i.Cg)([(0,r.EM)("ha-expansion-panel")],f)},75709:function(e,t,a){a.d(t,{h:function(){return f}});a(62953);var i=a(40445),o=a(71714),r=a(92347),l=a(96196),n=a(77845),d=a(63091);let s,h,c,p,u=e=>e;class f extends o.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const a=t?"trailing":"leading";return(0,l.qy)(s||(s=u` <span class="mdc-text-field__icon mdc-text-field__icon--${0}" tabindex="${0}"> <slot name="${0}Icon"></slot> </span> `),a,t?1:-1,a)}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}f.styles=[r.R,(0,l.AH)(h||(h=u`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding-top:var(--text-field-padding-top,0px);padding-bottom:var(--text-field-padding-bottom,0px);padding-inline-start:var(--text-field-padding-start,16px);padding-inline-end:var(--text-field-padding-end,16px)}.mdc-text-field__affix--suffix{padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-trailing-icon{padding-inline-start:var(--text-field-suffix-padding-left,16px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:var(--direction)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`)),"rtl"===d.G.document.dir?(0,l.AH)(c||(c=u`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`)):(0,l.AH)(p||(p=u``))],(0,i.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"invalid",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"error-message"})],f.prototype,"errorMessage",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"icon",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"iconTrailing",void 0),(0,i.Cg)([(0,n.MZ)()],f.prototype,"autocomplete",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"autocorrect",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"input-spellcheck"})],f.prototype,"inputSpellcheck",void 0),(0,i.Cg)([(0,n.P)("input")],f.prototype,"formElement",void 0),f=(0,i.Cg)([(0,n.EM)("ha-textfield")],f)},3103:function(e,t,a){a.a(e,async function(e,t){try{a(18111),a(22489),a(3362),a(62953);var i=a(40445),o=a(96196),r=a(77845),l=a(26300),n=(a(67094),a(75709),a(1087)),d=e([l]);l=(d.then?(await d)():d)[0];let s,h,c,p=e=>e;const u="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",f="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z";class g extends o.WF{focus(){var e;null===(e=this._input)||void 0===e||e.focus()}render(){return(0,o.qy)(s||(s=p` <ha-textfield .autofocus="${0}" autocomplete="off" .label="${0}" .value="${0}" icon .iconTrailing="${0}" @input="${0}"> <slot name="prefix" slot="leadingIcon"> <ha-svg-icon tabindex="-1" class="prefix" .path="${0}"></ha-svg-icon> </slot> <div class="trailing" slot="trailingIcon"> ${0} <slot name="suffix"></slot> </div> </ha-textfield> `),this.autofocus,this.label||this.hass.localize("ui.common.search"),this.filter||"",this.filter||this.suffix,this._filterInputChanged,f,this.filter&&(0,o.qy)(h||(h=p` <ha-icon-button @click="${0}" .label="${0}" .path="${0}" class="clear-button"></ha-icon-button> `),this._clearSearch,this.hass.localize("ui.common.clear"),u))}async _filterChanged(e){(0,n.r)(this,"value-changed",{value:String(e)})}async _filterInputChanged(e){this._filterChanged(e.target.value)}async _clearSearch(){this._filterChanged("")}constructor(...e){super(...e),this.suffix=!1,this.autofocus=!1}}g.styles=(0,o.AH)(c||(c=p`:host{display:inline-flex}ha-icon-button,ha-svg-icon{color:var(--primary-text-color)}ha-svg-icon{outline:0}.clear-button{--mdc-icon-size:20px}ha-textfield{display:inherit}.trailing{display:flex;align-items:center}`)),(0,i.Cg)([(0,r.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)()],g.prototype,"filter",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],g.prototype,"suffix",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],g.prototype,"autofocus",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],g.prototype,"label",void 0),(0,i.Cg)([(0,r.P)("ha-textfield",!0)],g.prototype,"_input",void 0),g=(0,i.Cg)([(0,r.EM)("search-input")],g),t()}catch(s){t(s)}})},92158:function(e,t,a){a.d(t,{G:function(){return r},m:function(){return l}});a(3362);var i=a(62384),o=a(47351);const r=async e=>(0,i.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/hardware/audio",method:"get"}):(0,o.PS)(await e.callApi("GET","hassio/hardware/audio")),l=async e=>(0,i.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/hardware/info",method:"get"}):(0,o.PS)(await e.callApi("GET","hassio/hardware/info"))},59992:function(e,t,a){a.a(e,async function(e,i){try{a.d(t,{V:function(){return f}});a(62953);var o=a(40445),r=a(88696),l=a(96196),n=a(94333),d=a(77845),s=e([r]);r=(s.then?(await s)():s)[0];let h,c,p=e=>e;const u=e=>void 0===e?[]:Array.isArray(e)?e:[e],f=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,l.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,n.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,n.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...u(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,l.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,d.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,d.wk)()],t.prototype,"_contentScrollable",void 0),t};i()}catch(h){i(h)}})},63874:function(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(74423),a(26910),a(18111),a(22489),a(61701),a(33110),a(3362),a(62953);var o=a(40445),r=a(53289),l=a(96196),n=a(77845),d=a(22786),s=a(1087),h=a(52220),c=(a(11382),a(43661),a(72554)),p=a(3103),u=a(47351),f=a(92158),g=a(65063),v=a(14503),m=e([c,p]);[c,p]=m.then?(await m)():m;let b,x,y,w,_=e=>e;const C=(0,d.A)((e,t,a,i)=>t.devices.filter(t=>{var i;return(e||["tty","gpio","input"].includes(t.subsystem))&&((null===(i=t.by_id)||void 0===i?void 0:i.toLowerCase().includes(a))||t.name.toLowerCase().includes(a)||t.dev_path.toLocaleLowerCase().includes(a)||JSON.stringify(t.attributes).toLocaleLowerCase().includes(a))}).sort((e,t)=>(0,h.xL)(e.name,t.name,i)));class S extends l.WF{async showDialog(){try{this._hardware=await(0,f.m)(this.hass),this._open=!0}catch(e){await(0,g.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.hardware.available_hardware.failed_to_get"),text:(0,u.VR)(e)})}}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._open=!1,this._hardware=void 0,(0,s.r)(this,"dialog-closed",{dialog:this.localName})}render(){var e;if(!this._hardware)return l.s6;const t=C((null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced)||!1,this._hardware,(this._filter||"").toLowerCase(),this.hass.locale.language);return(0,l.qy)(b||(b=_` <ha-dialog .hass="${0}" .open="${0}" flexcontent header-title="${0}" @closed="${0}"> <div class="content-container"> <search-input autofocus .hass="${0}" .filter="${0}" @value-changed="${0}" .label="${0}"> </search-input> <div class="devices-container ha-scrollbar"> ${0} </div> </div> </ha-dialog> `),this.hass,this._open,this.hass.localize("ui.panel.config.hardware.available_hardware.title"),this._dialogClosed,this.hass,this._filter,this._handleSearchChange,this.hass.localize("ui.panel.config.hardware.available_hardware.search"),t.map(e=>(0,l.qy)(x||(x=_` <ha-expansion-panel .header="${0}" .secondary="${0}" outlined> <div class="device-property"> <span> ${0}: </span> <span>${0}</span> </div> <div class="device-property"> <span> ${0}: </span> <code>${0}</code> </div> ${0} <div class="attributes"> <span> ${0}: </span> <pre>${0}</pre> </div> </ha-expansion-panel> `),e.name,e.by_id||void 0,this.hass.localize("ui.panel.config.hardware.available_hardware.subsystem"),e.subsystem,this.hass.localize("ui.panel.config.hardware.available_hardware.device_path"),e.dev_path,e.by_id?(0,l.qy)(y||(y=_` <div class="device-property"> <span> ${0}: </span> <code>${0}</code> </div> `),this.hass.localize("ui.panel.config.hardware.available_hardware.id"),e.by_id):l.s6,this.hass.localize("ui.panel.config.hardware.available_hardware.attributes"),(0,r.dump)(e.attributes,{indent:2}))))}_handleSearchChange(e){this._filter=e.detail.value}static get styles(){return[v.dp,(0,l.AH)(w||(w=_`ha-dialog{--dialog-content-padding:0}.content-container{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden}.devices-container{padding:var(--ha-space-6);overflow-y:auto;flex:1;min-height:0}ha-expansion-panel{flex:1;margin:4px 0}code,pre{background-color:var(--markdown-code-background-color,none);border-radius:var(--ha-border-radius-sm)}pre{padding:16px;overflow:auto;line-height:var(--ha-line-height-normal);font-family:var(--ha-font-family-code)}code{font-size:var(--ha-font-size-s);padding:.2em .4em}search-input{margin:8px 16px 0;display:block}.device-property{display:flex;justify-content:space-between}.attributes{margin-top:12px}`))]}constructor(...e){super(...e),this._open=!1}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],S.prototype,"hass",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_hardware",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_filter",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_open",void 0),S=(0,o.Cg)([(0,n.EM)("ha-dialog-hardware-available")],S),i()}catch(b){i(b)}})},22348:function(e,t,a){a.d(t,{V:function(){return o}});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177:function(e,t,a){a.d(t,{n:function(){return i}});a(27495);const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=25631.2739c6a9560306e2.js.map