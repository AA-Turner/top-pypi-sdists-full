"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["99889"],{69558:function(e,t,a){a.d(t,{_:function(){return r}});a(16280),a(18111),a(7588),a(62953);var i=a(96196),o=a(54495);const r=(0,o.u$)(class extends o.WL{update(e,[t,a]){return this._element&&this._element.localName===t?(a&&Object.entries(a).forEach(([e,t])=>{this._element[e]=t}),i.c0):this.render(t,a)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach(([e,t])=>{this._element[e]=t}),this._element}constructor(e){if(super(e),e.type!==o.OA.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}})},64481:function(e,t,a){a.d(t,{D:function(){return o},J:function(){return r}});a(3362);let i=!1;try{i="true"===window.localStorage.getItem("disableViewTransition")}catch(n){}const o=e=>{i=e},r=e=>{if(!document.startViewTransition||i)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},93444:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845);let n,s,l=e=>e;class d extends o.WF{render(){return(0,o.qy)(n||(n=l` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(s||(s=l`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,i.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845);let n,s,l,d,c,h,p=e=>e;class g extends o.WF{render(){const e=(0,o.qy)(n||(n=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(s||(s=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(l||(l=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(d||(d=p`${0}${0}`),t,e):(0,o.qy)(c||(c=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(h||(h=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],g.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],g.prototype,"showBorder",void 0),g=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],g)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var i=a(40445),o=a(93900),r=a(96196),n=a(77845),s=a(32288),l=a(1087),d=a(64481),c=a(59992),h=a(14503),p=a(22348),g=(a(76538),a(26300)),u=e([o,g,c]);[o,g,c]=u.then?(await u)():u;let m,v,f,b,y,x,_,w=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class k extends((0,c.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(m||(m=w` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,s.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(v||(v=w` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(f||(f=w`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(b||(b=w`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(y||(y=w`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(x||(x=w`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,(0,r.AH)(_||(_=w`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,l.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,l.r)(this,"closed"))}}}(0,i.Cg)([(0,n.MZ)({attribute:!1})],k.prototype,"hass",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"aria-labelledby"})],k.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"aria-describedby"})],k.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],k.prototype,"open",void 0),(0,i.Cg)([(0,n.MZ)({reflect:!0})],k.prototype,"type",void 0),(0,i.Cg)([(0,n.MZ)({type:String,reflect:!0,attribute:"width"})],k.prototype,"width",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],k.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"header-title"})],k.prototype,"headerTitle",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"header-subtitle"})],k.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,n.MZ)({type:String,attribute:"header-subtitle-position"})],k.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],k.prototype,"flexContent",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,attribute:"without-header"})],k.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,n.wk)()],k.prototype,"_open",void 0),(0,i.Cg)([(0,n.P)(".body")],k.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,n.wk)()],k.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,n.Ls)({passive:!0})],k.prototype,"_handleBodyScroll",null),k=(0,i.Cg)([(0,n.EM)("ha-dialog")],k),t()}catch(m){t(m)}})},90248:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaIconButtonArrowPrev:function(){return u}});a(62953);var o=a(40445),r=a(96196),n=a(77845),s=a(63091),l=a(26300),d=e([l]);l=(d.then?(await d)():d)[0];let c,h=e=>e;const p="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",g="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z";class u extends r.WF{render(){var e;return(0,r.qy)(c||(c=h` <ha-icon-button .disabled="${0}" .label="${0}" .path="${0}" .href="${0}" .target="${0}" .rel="${0}" .download="${0}"></ha-icon-button> `),this.disabled,this.label||(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.back"))||"Back",this._icon,this.href,this.target,this.rel,this.download)}constructor(...e){super(...e),this.disabled=!1,this._icon="rtl"===s.G.document.dir?g:p}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],u.prototype,"disabled",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"label",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"href",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"target",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"rel",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"download",void 0),(0,o.Cg)([(0,n.wk)()],u.prototype,"_icon",void 0),u=(0,o.Cg)([(0,n.EM)("ha-icon-button-arrow-prev")],u),i()}catch(c){i(c)}})},26300:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaIconButton:function(){return m}});a(62953);var o=a(40445),r=a(96196),n=a(77845),s=a(32288),l=a(18350),d=(a(67094),e([l]));l=(d.then?(await d)():d)[0];let c,h,p,g,u=e=>e;class m extends r.WF{render(){return(0,r.qy)(c||(c=u` <ha-button appearance="plain" variant="neutral" aria-label="${0}" title="${0}" aria-haspopup="${0}" .disabled="${0}" .iconTag="${0}" .href="${0}" .target="${0}" .rel="${0}" .download="${0}"> ${0} </ha-button> `),(0,s.J)(this.label),(0,s.J)(this.hideTitle?void 0:this.label),(0,s.J)(this.ariaHasPopup),this.disabled,this.path?"ha-svg-icon":"span",this.href,this.target,this.rel,this.download,this.path?(0,r.qy)(h||(h=u`<ha-svg-icon .path="${0}"></ha-svg-icon>`),this.path):(0,r.qy)(p||(p=u`<span><slot></slot></span>`)))}constructor(...e){super(...e),this.disabled=!1,this.hideTitle=!1,this.selected=!1}}m.shadowRootOptions={mode:"open",delegatesFocus:!0},m.styles=(0,r.AH)(g||(g=u`:host{display:inline-block;outline:0;--ha-button-height:var(--ha-icon-button-size, 48px)}ha-button{position:relative;isolation:isolate;--wa-form-control-padding-inline:var(
        --ha-icon-button-padding-inline,
        --ha-space-2
      );--wa-color-on-normal:currentColor;--wa-color-fill-quiet:transparent;--ha-button-label-overflow:visible}ha-button::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background-color:currentColor;opacity:0;pointer-events:none}ha-button::part(base){width:var(--wa-form-control-height);aspect-ratio:1;outline-offset:-4px}ha-button::part(label){display:flex}:host([selected]) ha-button::after{opacity:.1}@media (hover:hover){:host(:hover:not([disabled])) ha-button::after{opacity:.1}}`)),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],m.prototype,"disabled",void 0),(0,o.Cg)([(0,n.MZ)({type:String})],m.prototype,"path",void 0),(0,o.Cg)([(0,n.MZ)({type:String})],m.prototype,"label",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"aria-haspopup"})],m.prototype,"ariaHasPopup",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"hide-title",type:Boolean})],m.prototype,"hideTitle",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],m.prototype,"selected",void 0),(0,o.Cg)([(0,n.MZ)()],m.prototype,"href",void 0),(0,o.Cg)([(0,n.MZ)()],m.prototype,"target",void 0),(0,o.Cg)([(0,n.MZ)()],m.prototype,"rel",void 0),(0,o.Cg)([(0,n.MZ)()],m.prototype,"download",void 0),m=(0,o.Cg)([(0,n.EM)("ha-icon-button")],m),i()}catch(c){i(c)}})},43661:function(e,t,a){a.r(t),a.d(t,{HaIconNext:function(){return s}});a(62953);var i=a(40445),o=a(77845),r=a(63091),n=a(67094);class s extends n.HaSvgIcon{constructor(...e){super(...e),this.path="rtl"===r.G.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}(0,i.Cg)([(0,o.MZ)()],s.prototype,"path",void 0),s=(0,i.Cg)([(0,o.EM)("ha-icon-next")],s)},2846:function(e,t,a){a.d(t,{G:function(){return p},J:function(){return h}});var i=a(40445),o=a(12415),r=a(82553),n=a(96196),s=a(77845);a(54276);let l,d,c=e=>e;const h=[r.R,(0,n.AH)(l||(l=c`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`))];class p extends o.n{renderRipple(){return"text"===this.type?n.s6:(0,n.qy)(d||(d=c`<ha-ripple part="ripple" for="item" ?disabled="${0}"></ha-ripple>`),this.disabled&&"link"!==this.type)}}p.styles=h,p=(0,i.Cg)([(0,s.EM)("ha-md-list-item")],p)},17308:function(e,t,a){var i=a(40445),o=a(49838),r=a(11245),n=a(96196),s=a(77845);let l;class d extends o.B{}d.styles=[r.R,(0,n.AH)(l||(l=(e=>e)`:host{--md-sys-color-surface:var(--card-background-color)}`))],d=(0,i.Cg)([(0,s.EM)("ha-md-list")],d)},54276:function(e,t,a){a(62953);var i=a(40445),o=a(76482),r=a(91382),n=a(96245),s=a(96196),l=a(77845);let d;class c extends r.n{attach(e){super.attach(e),this.attachableTouchController.attach(e)}disconnectedCallback(){super.disconnectedCallback(),this.hovered=!1,this.pressed=!1}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(e,t){null==e||e.removeEventListener("touchend",this._handleTouchEnd),null==t||t.addEventListener("touchend",this._handleTouchEnd)}constructor(...e){super(...e),this.attachableTouchController=new o.i(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}c.styles=[n.R,(0,s.AH)(d||(d=(e=>e)`:host{--md-ripple-hover-opacity:var(--ha-ripple-hover-opacity, 0.08);--md-ripple-pressed-opacity:var(--ha-ripple-pressed-opacity, 0.12);--md-ripple-hover-color:var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );--md-ripple-pressed-color:var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        )}`))],c=(0,i.Cg)([(0,l.EM)("ha-ripple")],c)},65829:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaSpinner:function(){return h}});var o=a(40445),r=a(55262),n=a(96196),s=a(77845),l=e([r]);r=(l.then?(await l)():l)[0];let d,c=e=>e;class h extends r.A{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-spinner-size","16px");break;case"small":this.style.setProperty("--ha-spinner-size","28px");break;case"medium":this.style.setProperty("--ha-spinner-size","48px");break;case"large":this.style.setProperty("--ha-spinner-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}static get styles(){return[r.A.styles,(0,n.AH)(d||(d=c`:host{--indicator-color:var(
            --ha-spinner-indicator-color,
            var(--primary-color)
          );--track-color:var(--ha-spinner-divider-color, var(--divider-color));--track-width:4px;--speed:3.5s;font-size:var(--ha-spinner-size, 48px)}`))]}}(0,o.Cg)([(0,s.MZ)()],h.prototype,"size",void 0),h=(0,o.Cg)([(0,s.EM)("ha-spinner")],h),i()}catch(d){i(d)}})},67094:function(e,t,a){a.r(t),a.d(t,{HaSvgIcon:function(){return h}});var i=a(40445),o=a(96196),r=a(77845);let n,s,l,d,c=e=>e;class h extends o.WF{render(){return(0,o.JW)(n||(n=c` <svg viewBox="${0}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${0} ${0} </g> </svg>`),this.viewBox||"0 0 24 24",this.path?(0,o.JW)(s||(s=c`<path class="primary-path" d="${0}"></path>`),this.path):o.s6,this.secondaryPath?(0,o.JW)(l||(l=c`<path class="secondary-path" d="${0}"></path>`),this.secondaryPath):o.s6)}}h.styles=(0,o.AH)(d||(d=c`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`)),(0,i.Cg)([(0,r.MZ)()],h.prototype,"path",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],h.prototype,"secondaryPath",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],h.prototype,"viewBox",void 0),h=(0,i.Cg)([(0,r.EM)("ha-svg-icon")],h)},75709:function(e,t,a){a.d(t,{h:function(){return u}});a(62953);var i=a(40445),o=a(71714),r=a(92347),n=a(96196),s=a(77845),l=a(63091);let d,c,h,p,g=e=>e;class u extends o.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const a=t?"trailing":"leading";return(0,n.qy)(d||(d=g` <span class="mdc-text-field__icon mdc-text-field__icon--${0}" tabindex="${0}"> <slot name="${0}Icon"></slot> </span> `),a,t?1:-1,a)}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}u.styles=[r.R,(0,n.AH)(c||(c=g`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding-top:var(--text-field-padding-top,0px);padding-bottom:var(--text-field-padding-bottom,0px);padding-inline-start:var(--text-field-padding-start,16px);padding-inline-end:var(--text-field-padding-end,16px)}.mdc-text-field__affix--suffix{padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-trailing-icon{padding-inline-start:var(--text-field-suffix-padding-left,16px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:var(--direction)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`)),"rtl"===l.G.document.dir?(0,n.AH)(h||(h=g`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`)):(0,n.AH)(p||(p=g``))],(0,i.Cg)([(0,s.MZ)({type:Boolean})],u.prototype,"invalid",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],u.prototype,"icon",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],u.prototype,"iconTrailing",void 0),(0,i.Cg)([(0,s.MZ)()],u.prototype,"autocomplete",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],u.prototype,"autocorrect",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"input-spellcheck"})],u.prototype,"inputSpellcheck",void 0),(0,i.Cg)([(0,s.P)("input")],u.prototype,"formElement",void 0),u=(0,i.Cg)([(0,s.EM)("ha-textfield")],u)},20559:function(e,t,a){a.d(t,{JW:function(){return y},OW:function(){return v},PO:function(){return h},VN:function(){return d},XG:function(){return p},eB:function(){return m},gZ:function(){return u},hM:function(){return c},k2:function(){return l},lU:function(){return g},nc:function(){return f},vX:function(){return b},z1:function(){return s}});a(18111),a(22489),a(20116),a(61701),a(3362),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(62953);var i=a(36312),o=a(91926),r=a(28989),n=a(16790),s=function(e){return e.THREAD="thread",e.WIFI="wifi",e.ETHERNET="ethernet",e.UNKNOWN="unknown",e}({});const l=e=>{var t;return null===(t=e.auth.external)||void 0===t?void 0:t.config.canCommissionMatter},d=async e=>{if((0,i.x)(e,"thread")){const t=(await(0,n.sL)(e)).datasets.find(e=>e.preferred);if(t)return e.auth.external.fireMessage({type:"matter/commission",payload:{active_operational_dataset:(await(0,n.dy)(e,t.dataset_id)).tlv,border_agent_id:t.preferred_border_agent_id,mac_extended_address:t.preferred_extended_address,extended_pan_id:t.extended_pan_id}})}return e.auth.external.fireMessage({type:"matter/commission"})},c=(e,t)=>{let a;const i=(0,r.Ag)(e.connection,e=>{if(!a)return void(a=new Set(Object.values(e).filter(e=>e.identifiers.find(e=>"matter"===e[0])).map(e=>e.id)));const r=Object.values(e).filter(e=>e.identifiers.find(e=>"matter"===e[0])&&!a.has(e.id));r.length&&(i(),a=void 0,null==t||t(),(0,o.o)(`/config/devices/device/${r[0].id}`))});return()=>{i(),a=void 0}},h=(e,t)=>e.callWS({type:"matter/commission",code:t}),p=(e,t)=>e.callWS({type:"matter/commission_on_network",pin:t}),g=(e,t,a)=>e.callWS({type:"matter/set_wifi_credentials",network_name:t,password:a}),u=(e,t)=>e.callWS({type:"matter/set_thread",thread_operation_dataset:t}),m=(e,t)=>e.callWS({type:"matter/node_diagnostics",device_id:t}),v=(e,t)=>e.callWS({type:"matter/ping_node",device_id:t}),f=(e,t)=>e.callWS({type:"matter/open_commissioning_window",device_id:t}),b=(e,t,a)=>e.callWS({type:"matter/remove_matter_fabric",device_id:t,fabric_index:a}),y=(e,t)=>e.callWS({type:"matter/interview_node",device_id:t})},16790:function(e,t,a){a.d(t,{It:function(){return s},W4:function(){return d},dy:function(){return n},l1:function(){return c},rY:function(){return l},sL:function(){return r},wm:function(){return o}});class i{processEvent(e){return"router_discovered"===e.type?this.routers[e.key]=e.data:"router_removed"===e.type&&delete this.routers[e.key],Object.values(this.routers)}constructor(){this.routers={}}}const o=(e,t)=>{const a=new i;return e.connection.subscribeMessage(e=>t(a.processEvent(e)),{type:"thread/discover_routers"})},r=e=>e.callWS({type:"thread/list_datasets"}),n=(e,t)=>e.callWS({type:"thread/get_dataset_tlv",dataset_id:t}),s=(e,t,a)=>e.callWS({type:"thread/add_dataset_tlv",source:t,tlv:a}),l=(e,t)=>e.callWS({type:"thread/delete_dataset",dataset_id:t}),d=(e,t)=>e.callWS({type:"thread/set_preferred_dataset",dataset_id:t}),c=(e,t,a,i)=>e.callWS({type:"thread/set_preferred_border_agent",dataset_id:t,border_agent_id:a,extended_address:i})},59992:function(e,t,a){a.a(e,async function(e,i){try{a.d(t,{V:function(){return u}});a(62953);var o=a(40445),r=a(88696),n=a(96196),s=a(94333),l=a(77845),d=e([r]);r=(d.then?(await d)():d)[0];let c,h,p=e=>e;const g=e=>void 0===e?[]:Array.isArray(e)?e:[e],u=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,n.qy)(c||(c=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...g(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,n.AH)(h||(h=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const a=e.currentTarget;this._contentScrolled=(null!==(t=a.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(a)},this._resize=new r.P(this,{target:null,callback:e=>{var t;const a=null===(t=e[0])||void 0===t?void 0:t.target;a&&this._updateScrollableState(a)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t};i()}catch(c){i(c)}})},7664:function(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(3362),a(27495),a(25440),a(79978),a(62953);var o=a(40445),r=a(96196),n=a(77845),s=a(69558),l=a(1087),d=(a(93444),a(90248)),c=a(18350),h=a(72554),p=a(20559),g=a(14503),u=(a(32280),a(41834),a(16946),a(85810),a(10625),a(70978),a(2205)),m=a(11988),v=a(81619),f=e([d,c,h,u,m]);[d,c,h,u,m]=f.then?(await f)():f;let b,y,x,_,w,C,k,$=e=>e;const z={main:void 0,new:"main",existing:"main",google_home:"existing",google_home_fallback:"google_home",apple_home:"existing",generic:"existing",commissioning:void 0};class S extends r.WF{showDialog(){this._open=!0,this._unsub=(0,p.hM)(this.hass,()=>this.closeDialog())}closeDialog(){this._open=!1}_dialogClosed(){var e;this._open=!1,this._step="main",this._pairingCode="",null===(e=this._unsub)||void 0===e||e.call(this),this._unsub=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}_handleStepSelected(e){this._step=e.detail.step,this._pairingCode=""}_handlePairingCodeChanged(e){this._pairingCode=e.detail.code}_back(){const e=z[this._step];e&&(this._step=e)}_renderStep(){return(0,r.qy)(b||(b=$` <div @pairing-code-changed="${0}" @step-selected="${0}" .hass="${0}"> ${0} </div> `),this._handlePairingCodeChanged,this._handleStepSelected,this.hass,(0,s._)(`matter-add-device-${this._step.replaceAll("_","-")}`,{hass:this.hass}))}async _addDevice(){const e=this._pairingCode,t=this._step;try{this._step="commissioning",await(0,p.PO)(this.hass,e)}catch(a){(0,v.P)(this,{message:this.hass.localize("ui.dialogs.matter-add-device.add_device_failed"),duration:2e3})}this._step=t}_renderActions(){return"apple_home"===this._step||"google_home_fallback"===this._step||"generic"===this._step?(0,r.qy)(y||(y=$` <ha-button slot="primaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> `),this._addDevice,!this._pairingCode,this.hass.localize("ui.dialogs.matter-add-device.add_device")):"new"===this._step?(0,r.qy)(x||(x=$` <ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button> `),this.closeDialog,this.hass.localize("ui.common.ok")):r.s6}render(){if(!this._open)return r.s6;const e=this.hass.localize(`ui.dialogs.matter-add-device.${this._step}.header`),t=z[this._step],a=this._renderActions();return(0,r.qy)(_||(_=$` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" prevent-scrim-close @closed="${0}"> ${0} ${0} ${0} </ha-dialog> `),this.hass,this._open,e,this._dialogClosed,t?(0,r.qy)(w||(w=$` <ha-icon-button-arrow-prev slot="headerNavigationIcon" .hass="${0}" @click="${0}"></ha-icon-button-arrow-prev> `),this.hass,this._back):r.s6,this._renderStep(),a===r.s6?r.s6:(0,r.qy)(C||(C=$`<ha-dialog-footer slot="footer"> ${0} </ha-dialog-footer>`),a))}constructor(...e){super(...e),this._open=!1,this._pairingCode="",this._step="main"}}S.styles=[g.nA,(0,r.AH)(k||(k=$`:host{--horizontal-padding:24px}ha-dialog{--dialog-content-padding:0}@media all and (max-width:450px),all and (max-height:500px){:host{--horizontal-padding:16px}}.loading{padding:24px;display:flex;align-items:center;justify-content:center}`))],(0,o.Cg)([(0,n.MZ)({attribute:!1})],S.prototype,"hass",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_open",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_pairingCode",void 0),(0,o.Cg)([(0,n.wk)()],S.prototype,"_step",void 0),S=(0,o.Cg)([(0,n.EM)("dialog-matter-add-device")],S),i()}catch(b){i(b)}})},32280:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(2846),a(17308),a(75709),a(10465));let l,d,c,h=e=>e;class p extends o.WF{render(){return(0,o.qy)(l||(l=h` <div class="content"> <ol> <li> ${0} </li> <li> ${0} </li> <li> ${0} </li> </ol> <br> <p> ${0} </p> <ha-textfield label="${0}" .value="${0}" @input="${0}"></ha-textfield> </div> `),this.hass.localize("ui.dialogs.matter-add-device.apple_home.step_1",{accessory_settings:(0,o.qy)(d||(d=h`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.apple_home.accessory_settings"))}),this.hass.localize("ui.dialogs.matter-add-device.apple_home.step_2",{turn_on_pairing_mode:(0,o.qy)(c||(c=h`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.apple_home.turn_on_pairing_mode"))}),this.hass.localize("ui.dialogs.matter-add-device.apple_home.step_3"),this.hass.localize("ui.dialogs.matter-add-device.apple_home.code_instructions"),this.hass.localize("ui.dialogs.matter-add-device.apple_home.setup_code"),this._code,this._onCodeChanged)}_onCodeChanged(e){const t=e.currentTarget.value;this._code=t,(0,n.r)(this,"pairing-code-changed",{code:t})}constructor(...e){super(...e),this._code=""}}p.styles=[s.g],(0,i.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],p.prototype,"_code",void 0),p=(0,i.Cg)([(0,r.EM)("matter-add-device-apple-home")],p)},11988:function(e,t,a){a.a(e,async function(e,t){try{var i=a(40445),o=a(96196),r=a(77845),n=a(10465),s=a(65829),l=e([s]);s=(l.then?(await l)():l)[0];let d,c,h=e=>e;class p extends o.WF{render(){return(0,o.qy)(d||(d=h` <div class="content"> <ha-spinner size="medium"></ha-spinner> <p> ${0} </p> </div> `),this.hass.localize("ui.dialogs.matter-add-device.commissioning.note"))}}p.styles=[n.g,(0,o.AH)(c||(c=h`.content{display:flex;align-items:center;flex-direction:column;text-align:center}ha-spinner{margin-bottom:24px}`))],(0,i.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),p=(0,i.Cg)([(0,r.EM)("matter-add-device-commissioning")],p),t()}catch(d){t(d)}})},41834:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(17308),a(2846),a(10465));let l,d,c=e=>e;class h extends o.WF{render(){return(0,o.qy)(l||(l=c` <div class="content"> <p> ${0} </p> </div> <ha-md-list> <ha-md-list-item interactive type="button" .step="${0}" @click="${0}" @keydown="${0}"> <img src="/static/images/logo_google_home.png" alt="" class="logo" slot="start"> <span slot="headline"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> <ha-md-list-item interactive type="button" .step="${0}" @click="${0}" @keydown="${0}"> <img src="/static/images/logo_apple_home.png" alt="" class="logo" slot="start"> <span slot="headline"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> <ha-md-list-item interactive type="button" .step="${0}" @click="${0}" @keydown="${0}"> <div class="logo" slot="start"> <ha-svg-icon path="${0}"></ha-svg-icon> </div> <span slot="headline"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> </ha-md-list> `),this.hass.localize("ui.dialogs.matter-add-device.existing.question"),"google_home",this._onItemClick,this._onItemClick,this.hass.localize("ui.dialogs.matter-add-device.existing.answer_google_home"),"apple_home",this._onItemClick,this._onItemClick,this.hass.localize("ui.dialogs.matter-add-device.existing.answer_apple_home"),"generic",this._onItemClick,this._onItemClick,"M12,3L2,12H5V20H19V12H22L12,3M12,8.5C14.34,8.5 16.46,9.43 18,10.94L16.8,12.12C15.58,10.91 13.88,10.17 12,10.17C10.12,10.17 8.42,10.91 7.2,12.12L6,10.94C7.54,9.43 9.66,8.5 12,8.5M12,11.83C13.4,11.83 14.67,12.39 15.6,13.3L14.4,14.47C13.79,13.87 12.94,13.5 12,13.5C11.06,13.5 10.21,13.87 9.6,14.47L8.4,13.3C9.33,12.39 10.6,11.83 12,11.83M12,15.17C12.94,15.17 13.7,15.91 13.7,16.83C13.7,17.75 12.94,18.5 12,18.5C11.06,18.5 10.3,17.75 10.3,16.83C10.3,15.91 11.06,15.17 12,15.17Z",this.hass.localize("ui.dialogs.matter-add-device.existing.answer_generic"))}_onItemClick(e){if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;const t=e.currentTarget.step;(0,n.r)(this,"step-selected",{step:t})}}h.styles=[s.g,(0,o.AH)(d||(d=c`.logo{width:48px;height:48px;border-radius:var(--ha-border-radius-lg);border:1px solid var(--divider-color);padding:10px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;object-fit:contain}.logo ha-svg-icon{--mdc-icon-size:36px}`))],(0,i.Cg)([(0,r.MZ)({attribute:!1})],h.prototype,"hass",void 0),h=(0,i.Cg)([(0,r.EM)("matter-add-device-existing")],h)},16946:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(2846),a(17308),a(75709),a(10465));let l,d=e=>e;class c extends o.WF{render(){return(0,o.qy)(l||(l=d` <div class="content"> <p> ${0} </p> <ha-textfield label="${0}" .value="${0}" @input="${0}"></ha-textfield> </div> `),this.hass.localize("ui.dialogs.matter-add-device.generic.code_instructions"),this.hass.localize("ui.dialogs.matter-add-device.generic.setup_code"),this._code,this._onCodeChanged)}_onCodeChanged(e){const t=e.currentTarget.value;this._code=t,(0,n.r)(this,"pairing-code-changed",{code:t})}constructor(...e){super(...e),this._code=""}}c.styles=[s.g],(0,i.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],c.prototype,"_code",void 0),c=(0,i.Cg)([(0,r.EM)("matter-add-device-generic")],c)},10625:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(2846),a(17308),a(75709),a(10465));let l,d,c,h,p=e=>e;class g extends o.WF{render(){return(0,o.qy)(l||(l=p` <div class="content"> <ol> <li> ${0} </li> <li> ${0} </li> <li> ${0} </li> </ol> <br> <p> ${0} </p> <ha-textfield label="${0}" .value="${0}" @input="${0}"></ha-textfield> </div> `),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.step_1"),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.step_2",{linked_matter_apps_services:(0,o.qy)(d||(d=p`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.linked_matter_apps_services"))}),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.step_3",{link_apps_services:(0,o.qy)(c||(c=p`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.link_apps_services")),use_pairing_code:(0,o.qy)(h||(h=p`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.use_pairing_code"))}),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.code_instructions"),this.hass.localize("ui.dialogs.matter-add-device.google_home_fallback.pairing_code"),this._code,this._onCodeChanged)}_onCodeChanged(e){const t=e.currentTarget.value;this._code=t,(0,n.r)(this,"pairing-code-changed",{code:t})}constructor(...e){super(...e),this._code=""}}g.styles=[s.g],(0,i.Cg)([(0,r.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],g.prototype,"_code",void 0),g=(0,i.Cg)([(0,r.EM)("matter-add-device-google-home-fallback")],g)},85810:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(2846),a(17308),a(10465));let l,d,c,h,p=e=>e;class g extends o.WF{render(){return(0,o.qy)(l||(l=p` <div class="content"> <ol> <li> ${0} </li> <li> ${0} </li> <li> ${0} <span class="link" type="button" tabindex="0" @keydown="${0}" @click="${0}"> ${0} </span> </li> <li> ${0} </li> </ol> <br> </div> `),this.hass.localize("ui.dialogs.matter-add-device.google_home.step_1"),this.hass.localize("ui.dialogs.matter-add-device.google_home.step_2",{linked_matter_apps_services:(0,o.qy)(d||(d=p`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.google_home.linked_matter_apps_services"))}),this.hass.localize("ui.dialogs.matter-add-device.google_home.step_3",{link_apps_services:(0,o.qy)(c||(c=p`<b>${0}</b>`),this.hass.localize("ui.dialogs.matter-add-device.google_home.link_apps_services")),home_assistant:(0,o.qy)(h||(h=p`<b>Home Assistant</b>`))}),this._nextStep,this._nextStep,this.hass.localize("ui.dialogs.matter-add-device.google_home.no_home_assistant"),this.hass.localize("ui.dialogs.matter-add-device.google_home.redirect"))}_nextStep(){(0,n.r)(this,"step-selected",{step:"google_home_fallback"})}}g.styles=[s.g],(0,i.Cg)([(0,r.MZ)({attribute:!1})],g.prototype,"hass",void 0),g=(0,i.Cg)([(0,r.EM)("matter-add-device-google-home")],g)},70978:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845),n=a(1087),s=(a(43661),a(2846),a(17308),a(10465));let l,d=e=>e;class c extends o.WF{render(){return(0,o.qy)(l||(l=d` <div class="content"> <p class="text"> ${0} </p> </div> <ha-md-list> <ha-md-list-item interactive type="button" .step="${0}" @click="${0}" @keydown="${0}"> <span slot="headline"> ${0} </span> <span slot="supporting-text"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> <ha-md-list-item interactive type="button" .step="${0}" @click="${0}" @keydown="${0}"> <span slot="headline"> ${0} </span> <span slot="supporting-text"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> </ha-md-list> `),this.hass.localize("ui.dialogs.matter-add-device.main.question"),"new",this._onItemClick,this._onItemClick,this.hass.localize("ui.dialogs.matter-add-device.main.answer_new"),this.hass.localize("ui.dialogs.matter-add-device.main.answer_new_description"),"existing",this._onItemClick,this._onItemClick,this.hass.localize("ui.dialogs.matter-add-device.main.answer_existing"),this.hass.localize("ui.dialogs.matter-add-device.main.answer_existing_description"))}_onItemClick(e){if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;const t=e.currentTarget.step;(0,n.r)(this,"step-selected",{step:t})}}c.styles=[s.g],(0,i.Cg)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),c=(0,i.Cg)([(0,r.EM)("matter-add-device-main")],c)},2205:function(e,t,a){a.a(e,async function(e,t){try{var i=a(40445),o=a(96196),r=a(77845),n=a(65829),s=a(20559),l=a(10465),d=e([n]);n=(d.then?(await d)():d)[0];let c,h,p,g=e=>e;class u extends o.WF{firstUpdated(){(0,s.k2)(this.hass)&&(0,s.VN)(this.hass)}render(){return(0,s.k2)(this.hass)?(0,o.qy)(c||(c=g` <div class="content"> <ha-spinner size="medium"></ha-spinner> </div> `)):(0,o.qy)(h||(h=g` <div class="content"> <p>${0}</p> <p> ${0} </p> <div class="app-qr"> <a target="_blank" rel="noreferrer noopener" href="https://apps.apple.com/app/home-assistant/id1099568401?mt=8"> <img loading="lazy" src="/static/images/appstore.svg" alt="${0}" class="icon"> <img loading="lazy" src="/static/images/qr-appstore.svg" alt="${0}"> </a> <a target="_blank" rel="noreferrer noopener" href="https://play.google.com/store/apps/details?id=io.homeassistant.companion.android"> <img loading="lazy" src="/static/images/playstore.svg" alt="${0}" class="icon"> <img loading="lazy" src="/static/images/qr-playstore.svg" alt="${0}"> </a> </div> </div> `),this.hass.localize("ui.dialogs.matter-add-device.new.note"),this.hass.localize("ui.dialogs.matter-add-device.new.download_app"),this.hass.localize("ui.dialogs.matter-add-device.new.appstore"),this.hass.localize("ui.dialogs.matter-add-device.new.appstore"),this.hass.localize("ui.dialogs.matter-add-device.new.playstore"),this.hass.localize("ui.dialogs.matter-add-device.new.playstore"))}}u.styles=[l.g,(0,o.AH)(p||(p=g`.app-qr{margin:24px auto 0 auto;display:flex;justify-content:space-between;padding:0 24px;box-sizing:border-box;gap:var(--ha-space-4);width:100%;max-width:400px}.app-qr a,.app-qr img{flex:1}`))],(0,i.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),u=(0,i.Cg)([(0,r.EM)("matter-add-device-new")],u),t()}catch(c){t(c)}})},10465:function(e,t,a){a.d(t,{g:function(){return o}});let i;const o=(0,a(96196).AH)(i||(i=(e=>e)`.content{padding:16px var(--horizontal-padding,16px)}p{margin:0}p:not(:last-child){margin-bottom:8px}ol{padding-inline-start:20px;margin-block-start:0;margin-block-end:8px}li{margin-bottom:8px}.link{color:var(--primary-color);cursor:pointer;text-decoration:underline}ha-md-list{padding:0;--md-list-item-leading-space:var(--horizontal-padding, 16px);--md-list-item-trailing-space:var(--horizontal-padding, 16px);margin-bottom:16px}ha-textfield{width:100%}`))},69235:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953);"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await a.e("71055").then(a.bind(a,52370))).default),t()}catch(i){t(i)}},1)},14503:function(e,t,a){a.d(t,{RF:function(){return p},dp:function(){return m},kO:function(){return u},nA:function(){return g},og:function(){return h}});var i=a(96196);let o,r,n,s,l,d,c=e=>e;const h=(0,i.AH)(o||(o=c`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`)),p=(0,i.AH)(r||(r=c`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${0} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`),h),g=(0,i.AH)(n||(n=c`
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
`)),u=(0,i.AH)(s||(s=c`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
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
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`)),m=(0,i.AH)(l||(l=c`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`));(0,i.AH)(d||(d=c`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`))},22348:function(e,t,a){a.d(t,{V:function(){return o}});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177:function(e,t,a){a.d(t,{n:function(){return i}});a(27495);const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=99889.a88b389d8e3724f1.js.map