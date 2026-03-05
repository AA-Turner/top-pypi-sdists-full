"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["40901"],{38962:function(e,t,i){i.a(e,async function(e,a){try{i.r(t);i(62953);var o=i(40445),r=i(96196),s=i(77845),l=i(94333),n=i(1087),d=i(26300),h=(i(67094),e([d]));d=(h.then?(await h)():h)[0];let c,p,g,v,u=e=>e;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",f={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class y extends r.WF{render(){return(0,r.qy)(c||(c=u` <div class="issue-type ${0}" role="alert"> <div class="icon ${0}"> <slot name="icon"> <ha-svg-icon .path="${0}"></ha-svg-icon> </slot> </div> <div class="${0}"> <div class="main-content"> ${0} <slot></slot> </div> <div class="action"> <slot name="action"> ${0} </slot> </div> </div> </div> `),(0,l.H)({[this.alertType]:!0}),this.title?"":"no-title",f[this.alertType],(0,l.H)({content:!0,narrow:this.narrow}),this.title?(0,r.qy)(p||(p=u`<div class="title">${0}</div>`),this.title):r.s6,this.dismissable?(0,r.qy)(g||(g=u`<ha-icon-button @click="${0}" label="Dismiss alert" .path="${0}"></ha-icon-button>`),this._dismissClicked,m):r.s6)}_dismissClicked(){(0,n.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}y.styles=(0,r.AH)(v||(v=u`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--ha-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`)),(0,o.Cg)([(0,s.MZ)()],y.prototype,"title",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"alert-type"})],y.prototype,"alertType",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],y.prototype,"dismissable",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],y.prototype,"narrow",void 0),y=(0,o.Cg)([(0,s.EM)("ha-alert")],y),a()}catch(c){a(c)}})},75064:function(e,t,i){i(62953);var a=i(40445),o=i(96196),r=i(77845),s=i(2846);let l;class n extends s.G{constructor(...e){super(...e),this.borderTop=!1}}n.styles=[...s.J,(0,o.AH)(l||(l=(e=>e)`:host{--md-list-item-one-line-container-height:48px;--md-list-item-two-line-container-height:64px}:host([border-top]) md-item{border-top:1px solid var(--divider-color)}[slot=start]{--state-icon-color:var(--secondary-text-color)}[slot=overline]{line-height:1.15rem;font-size:calc(var(--mdc-typography-subtitle1-font-size, 1rem) * .75);font-weight:var(--mdc-typography-subtitle1-font-weight,400);font-family:var(
          --mdc-typography-subtitle1-font-family,
          var(--mdc-typography-font-family)
        );color:var(--mdc-select-label-ink-color,rgba(0,0,0,.6))}[slot=headline]{line-height:var(--ha-line-height-normal);font-size:var(--ha-font-size-m);white-space:nowrap}[slot=supporting-text]{line-height:var(--ha-line-height-normal);font-size:var(--ha-font-size-s);white-space:nowrap}::slotted(img),::slotted(state-badge){width:32px;height:32px}::slotted(.code){font-family:var(--ha-font-family-code);font-size:var(--ha-font-size-xs)}::slotted(.domain){font-size:var(--ha-font-size-s);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal);align-self:flex-end;max-width:30%;text-overflow:ellipsis;overflow:hidden;white-space:nowrap}`))],(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"border-top"})],n.prototype,"borderTop",void 0),n=(0,a.Cg)([(0,r.EM)("ha-combo-box-item")],n)},93444:function(e,t,i){var a=i(40445),o=i(96196),r=i(77845);let s,l,n=e=>e;class d extends o.WF{render(){return(0,o.qy)(s||(s=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(l||(l=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,a.Cg)([(0,r.EM)("ha-dialog-footer")],d)},76538:function(e,t,i){i(62953);var a=i(40445),o=i(96196),r=i(77845);let s,l,n,d,h,c,p=e=>e;class g extends o.WF{render(){const e=(0,o.qy)(s||(s=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(l||(l=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(d||(d=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,a.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],g.prototype,"subtitlePosition",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],g.prototype,"showBorder",void 0),g=(0,a.Cg)([(0,r.EM)("ha-dialog-header")],g)},72554:function(e,t,i){i.a(e,async function(e,t){try{i(3362),i(62953),i(49255);var a=i(40445),o=i(93900),r=i(96196),s=i(77845),l=i(32288),n=i(1087),d=i(64481),h=i(59992),c=i(14503),p=i(22348),g=(i(76538),i(26300)),v=e([o,g,h]);[o,g,h]=v.then?(await v)():v;let u,m,f,y,b,w,x,_=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class $ extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(u||(u=_` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(m||(m=_` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(f||(f=_`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(y||(y=_`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(b||(b=_`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(w||(w=_`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const i=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&i&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(x||(x=_`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,n.r)(this,"closed"))}}}(0,a.Cg)([(0,s.MZ)({attribute:!1})],$.prototype,"hass",void 0),(0,a.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],$.prototype,"ariaLabelledBy",void 0),(0,a.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],$.prototype,"ariaDescribedBy",void 0),(0,a.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],$.prototype,"open",void 0),(0,a.Cg)([(0,s.MZ)({reflect:!0})],$.prototype,"type",void 0),(0,a.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],$.prototype,"width",void 0),(0,a.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],$.prototype,"preventScrimClose",void 0),(0,a.Cg)([(0,s.MZ)({attribute:"header-title"})],$.prototype,"headerTitle",void 0),(0,a.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],$.prototype,"headerSubtitle",void 0),(0,a.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],$.prototype,"headerSubtitlePosition",void 0),(0,a.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],$.prototype,"flexContent",void 0),(0,a.Cg)([(0,s.MZ)({type:Boolean,attribute:"without-header"})],$.prototype,"withoutHeader",void 0),(0,a.Cg)([(0,s.wk)()],$.prototype,"_open",void 0),(0,a.Cg)([(0,s.P)(".body")],$.prototype,"bodyContainer",void 0),(0,a.Cg)([(0,s.wk)()],$.prototype,"_bodyScrolled",void 0),(0,a.Cg)([(0,s.Ls)({passive:!0})],$.prototype,"_handleBodyScroll",null),$=(0,a.Cg)([(0,s.EM)("ha-dialog")],$),t()}catch(u){t(u)}})},3449:function(e,t,i){i(62953);var a=i(40445),o=i(96196),r=i(77845);let s,l,n=e=>e;class d extends o.WF{render(){return(0,o.qy)(s||(s=n`<slot></slot>`))}constructor(...e){super(...e),this.disabled=!1}}d.styles=(0,o.AH)(l||(l=n`:host{display:block;color:var(--mdc-text-field-label-ink-color,rgba(0,0,0,.6));font-size:.75rem;padding-left:16px;padding-right:16px;padding-inline-start:16px;padding-inline-end:16px;letter-spacing:var(
        --mdc-typography-caption-letter-spacing,
        .0333333333em
      );line-height:normal}:host([disabled]){color:var(--mdc-text-field-disabled-ink-color,rgba(0,0,0,.6))}`)),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],d.prototype,"disabled",void 0),d=(0,a.Cg)([(0,r.EM)("ha-input-helper-text")],d)},2846:function(e,t,i){i.d(t,{G:function(){return p},J:function(){return c}});var a=i(40445),o=i(12415),r=i(82553),s=i(96196),l=i(77845);i(54276);let n,d,h=e=>e;const c=[r.R,(0,s.AH)(n||(n=h`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`))];class p extends o.n{renderRipple(){return"text"===this.type?s.s6:(0,s.qy)(d||(d=h`<ha-ripple part="ripple" for="item" ?disabled="${0}"></ha-ripple>`),this.disabled&&"link"!==this.type)}}p.styles=c,p=(0,a.Cg)([(0,l.EM)("ha-md-list-item")],p)},88285:function(e,t,i){i.a(e,async function(e,t){try{i(3362),i(62953);var a=i(40445),o=i(16527),r=i(96196),s=i(77845),l=i(32288),n=i(1087),d=i(38911),h=i(17894),c=(i(75064),i(88945),i(26300)),p=e([c]);c=(p.then?(await p)():p)[0];let g,v,u,m,f,y,b,w,x,_,C=e=>e;const $="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",k="M7,10L12,15L17,10H7Z";class M extends((0,h.c)(r.WF)){async focus(){var e;await this.updateComplete,await(null===(e=this.item)||void 0===e?void 0:e.focus())}render(){var e,t,i;const a=!!this.value,o=!(!this.value||this.required||this.disabled||this.hideClearIcon),s=null!==(e=this.placeholder)&&void 0!==e?e:this.label,n=this.label&&a?(0,r.qy)(g||(g=C`<span slot="overline">${0}${0}</span>`),this.label,this.required?" *":""):r.s6,d=a?this.valueRenderer?this.valueRenderer(null!==(t=this.value)&&void 0!==t?t:""):(0,r.qy)(v||(v=C`<span slot="headline">${0}</span>`),this.value):s?(0,r.qy)(u||(u=C`<span slot="headline" class="placeholder"> ${0}${0} </span>`),s,this.required?" *":""):r.s6;return(0,r.qy)(m||(m=C` <ha-combo-box-item aria-label="${0}" .disabled="${0}" type="button" compact="compact"> ${0} ${0}${0} ${0} ${0} <ha-svg-icon class="arrow" slot="end" .path="${0}"></ha-svg-icon> </ha-combo-box-item> `),(0,l.J)(this.label||this.placeholder),this.disabled,this.image?(0,r.qy)(f||(f=C`<img alt="${0}" slot="start" .src="${0}" crossorigin="anonymous" referrerpolicy="no-referrer">`),null!==(i=this.label)&&void 0!==i?i:"",this.image):this.icon?(0,r.qy)(y||(y=C`<ha-icon slot="start" .icon="${0}"></ha-icon>`),this.icon):(0,r.qy)(b||(b=C`<slot name="start"></slot>`)),n,d,this.unknown?(0,r.qy)(w||(w=C`<div slot="supporting-text" class="unknown"> ${0} </div>`),this.unknownItemText||this.localize("ui.components.combo-box.unknown_item")):r.s6,o?(0,r.qy)(x||(x=C` <ha-icon-button class="clear" slot="end" @click="${0}" .path="${0}"></ha-icon-button> `),this._clear,$):r.s6,k)}_clear(e){e.stopPropagation(),(0,n.r)(this,"clear")}static get styles(){return[(0,r.AH)(_||(_=C`ha-combo-box-item[disabled]{background-color:var(--mdc-text-field-disabled-fill-color,#f5f5f5)}ha-combo-box-item{position:relative;background-color:var(--mdc-text-field-fill-color,#f5f5f5);border-radius:var(--ha-border-radius-sm);border-end-end-radius:0;border-end-start-radius:0;--md-list-item-one-line-container-height:56px;--md-list-item-two-line-container-height:56px;--md-list-item-top-space:0px;--md-list-item-bottom-space:0px;--md-list-item-leading-space:var(--ha-space-4);--md-list-item-trailing-space:var(--ha-space-2);--ha-md-list-item-gap:var(--ha-space-2);--md-focus-ring-width:0px;--md-focus-ring-duration:0s}ha-combo-box-item[disabled]:after{background-color:var(--mdc-text-field-disabled-line-color,rgba(0,0,0,.42))}ha-combo-box-item:after{display:block;content:"";position:absolute;pointer-events:none;bottom:0;left:0;right:0;height:1px;width:100%;background-color:var(--mdc-text-field-idle-line-color,rgba(0,0,0,.42));transform:height 180ms ease-in-out,background-color 180ms ease-in-out}ha-combo-box-item:focus:after{height:2px;background-color:var(--mdc-theme-primary)}:host([unknown]) ha-combo-box-item{background-color:var(--ha-color-fill-warning-quiet-resting)}:host([invalid]) ha-combo-box-item:after{height:2px;background-color:var(--mdc-theme-error,var(--error-color,#b00020))}.clear{margin:0 -8px;--ha-icon-button-size:32px;--ha-icon-button-padding-inline:var(--ha-space-1)}.arrow{--mdc-icon-size:20px;width:32px}.placeholder{color:var(--secondary-text-color)}:host([invalid]) .placeholder{color:var(--mdc-theme-error,var(--error-color,#b00020))}.unknown{color:var(--ha-color-on-warning-normal)}`))]}constructor(...e){super(...e),this.invalid=!1}}(0,a.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],M.prototype,"invalid",void 0),(0,a.Cg)([(0,s.P)("ha-combo-box-item",!0)],M.prototype,"item",void 0),(0,a.Cg)([(0,s.wk)(),(0,o.Fg)({context:d.$F,subscribe:!0})],M.prototype,"localize",void 0),M=(0,a.Cg)([(0,s.EM)("ha-picker-field")],M),t()}catch(g){t(g)}})},5850:function(e,t,i){i(3362);var a=i(40445),o=i(96196),r=i(69880),s=i(34875),l=i(7731),n=i(77845),d=i(1087);let h;class c extends r.a{async onChange(e){super.onChange(e),(0,d.r)(this,e.type)}}c.styles=[l.R,s.R,(0,o.AH)(h||(h=(e=>e)`:host{--mdc-theme-secondary:var(--primary-color)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,16px);margin-inline-start:0px;direction:var(--direction)}.mdc-deprecated-list-item__meta{flex-shrink:0;direction:var(--direction);margin-inline-start:auto;margin-inline-end:0}.mdc-deprecated-list-item__graphic{margin-top:var(--radio-list-item-graphic-margin-top)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{margin-inline-start:0;margin-inline-end:var(--mdc-list-item-graphic-margin,32px)}`))],c=(0,a.Cg)([(0,n.EM)("ha-radio-list-item")],c)},606:function(e,t,i){i.a(e,async function(e,t){try{i(18111),i(61701),i(62953);var a=i(40445),o=i(96196),r=i(77845),s=i(32288),l=i(22786),n=i(1087),d=i(29823),h=(i(70947),i(3449),i(88285)),c=(i(67094),e([d,h]));[d,h]=c.then?(await c)():c;let p,g,v,u,m,f,y,b,w,x=e=>e;class _ extends o.WF{render(){return this.disabled?(0,o.qy)(p||(p=x`${0}${0}`),this._renderField(),this._renderHelper()):(0,o.qy)(g||(g=x` <ha-dropdown placement="bottom" @wa-select="${0}" @wa-show="${0}" @wa-hide="${0}"> ${0} ${0} </ha-dropdown> ${0} `),this._handleSelect,this._handleShow,this._handleHide,this._renderField(),this.options?this.options.map(e=>{var t;return(0,o.qy)(v||(v=x` <ha-dropdown-item .value="${0}" .disabled="${0}" .selected="${0}"> ${0} <div class="content"> ${0} ${0} </div> </ha-dropdown-item> `),"string"==typeof e?e:e.value,"string"!=typeof e&&(null!==(t=e.disabled)&&void 0!==t&&t),this.value===("string"==typeof e?e:e.value),e.iconPath?(0,o.qy)(u||(u=x`<ha-svg-icon slot="icon" .path="${0}"></ha-svg-icon>`),e.iconPath):o.s6,"string"==typeof e?e:e.label||e.value,e.secondary?(0,o.qy)(m||(m=x`<div class="secondary">${0}</div>`),e.secondary):o.s6)}):(0,o.qy)(f||(f=x`<slot></slot>`)),this._renderHelper())}_renderField(){const e=this._getValueLabel(this.options,this.value);return(0,o.qy)(y||(y=x` <ha-picker-field slot="trigger" type="button" class="${0}" compact="compact" aria-label="${0}" @clear="${0}" .label="${0}" .value="${0}" .required="${0}" .disabled="${0}" .hideClearIcon="${0}"> </ha-picker-field> `),this._opened?"opened":"",(0,s.J)(this.label),this._clearValue,this.label,e,this.required,this.disabled,!this.clearable||this.required||this.disabled||!this.value)}_renderHelper(){return this.helper?(0,o.qy)(b||(b=x`<ha-input-helper-text .disabled="${0}">${0}</ha-input-helper-text>`),this.disabled,this.helper):o.s6}_handleSelect(e){e.stopPropagation();const t=e.detail.item.value;t!==this.value&&(0,n.r)(this,"selected",{value:t})}_clearValue(){!this.disabled&&this.value&&(0,n.r)(this,"selected",{value:void 0})}_handleShow(){this.style.setProperty("--select-menu-width",`${this._triggerField.offsetWidth}px`),this._opened=!0}_handleHide(){this._opened=!1}constructor(...e){super(...e),this.clearable=!1,this.required=!1,this.disabled=!1,this._opened=!1,this._getValueLabel=(0,l.A)((e,t)=>{if(!e||!t)return t;for(const i of e)if("string"==typeof i&&i===t||"string"!=typeof i&&i.value===t)return"string"==typeof i?i:i.label||i.value;return t})}}_.styles=(0,o.AH)(w||(w=x`:host{position:relative}ha-picker-field.opened{--mdc-text-field-idle-line-color:var(--primary-color)}ha-dropdown-item .content{display:flex;gap:var(--ha-space-1);flex-direction:column}ha-dropdown-item .secondary{font-size:var(--ha-font-size-s);color:var(--ha-color-text-secondary)}ha-dropdown::part(menu){min-width:var(--select-menu-width)}ha-input-helper-text{display:block;margin:var(--ha-space-2) 0 0}`)),(0,a.Cg)([(0,r.MZ)({type:Boolean})],_.prototype,"clearable",void 0),(0,a.Cg)([(0,r.MZ)({attribute:!1})],_.prototype,"options",void 0),(0,a.Cg)([(0,r.MZ)()],_.prototype,"label",void 0),(0,a.Cg)([(0,r.MZ)()],_.prototype,"helper",void 0),(0,a.Cg)([(0,r.MZ)()],_.prototype,"value",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean})],_.prototype,"required",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean})],_.prototype,"disabled",void 0),(0,a.Cg)([(0,r.wk)()],_.prototype,"_opened",void 0),(0,a.Cg)([(0,r.P)("ha-picker-field")],_.prototype,"_triggerField",void 0),_=(0,a.Cg)([(0,r.EM)("ha-select")],_),t()}catch(p){t(p)}})},91984:function(e,t,i){i.d(t,{R:function(){return a}});function a(e){return"strategy"in e}},17894:function(e,t,i){i.d(t,{c:function(){return r}});i(62953);var a=i(40445),o=i(77845);const r=e=>{class t extends e{constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.unknown=!1,this.hideClearIcon=!1}}return(0,a.Cg)([(0,o.MZ)({type:Boolean})],t.prototype,"disabled",void 0),(0,a.Cg)([(0,o.MZ)({type:Boolean})],t.prototype,"required",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"icon",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"image",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"label",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"placeholder",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"helper",void 0),(0,a.Cg)([(0,o.MZ)()],t.prototype,"value",void 0),(0,a.Cg)([(0,o.MZ)({type:Boolean,reflect:!0})],t.prototype,"unknown",void 0),(0,a.Cg)([(0,o.MZ)({attribute:"unknown-item-text"})],t.prototype,"unknownItemText",void 0),(0,a.Cg)([(0,o.MZ)({attribute:"hide-clear-icon",type:Boolean})],t.prototype,"hideClearIcon",void 0),(0,a.Cg)([(0,o.MZ)({attribute:!1})],t.prototype,"valueRenderer",void 0),t}},54564:function(e,t,i){i.a(e,async function(e,a){try{i.r(t),i.d(t,{HuiDialogSelectView:function(){return k}});i(26910),i(18111),i(61701),i(13579),i(3362),i(62953);var o=i(40445),r=i(96196),s=i(77845),l=i(1087),n=i(38962),d=i(18350),h=(i(88945),i(93444),i(8630),i(5850),i(606)),c=i(72554),p=i(35952),g=i(91984),v=i(71730),u=i(99774),m=i(14503),f=e([n,d,h,c]);[n,d,h,c]=f.then?(await f)():f;let y,b,w,x,_,C,$=e=>e;class k extends r.WF{showDialog(e){this._config=e.lovelaceConfig,this._urlPath=e.urlPath,this._params=e,this._open=!0,this._params.allowDashboardChange&&this._getDashboards()}closeDialog(){this._open=!1}_dialogClosed(){this._params=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._params)return r.s6;const e=(0,u.EN)(this.hass);return(0,r.qy)(y||(y=$` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" @closed="${0}"> ${0} ${0} <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" @click="${0}" appearance="plain"> ${0} </ha-button> <ha-button slot="primaryAction" .disabled="${0}" @click="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this._params.header||this.hass.localize("ui.panel.lovelace.editor.select_view.header"),this._dialogClosed,this._params.allowDashboardChange?(0,r.qy)(b||(b=$`<ha-select .label="${0}" .disabled="${0}" .value="${0}" @selected="${0}" autofocus .options="${0}"> </ha-select>`),this.hass.localize("ui.panel.lovelace.editor.select_view.dashboard_label"),!this._dashboards.length,this._urlPath||e,this._dashboardChanged,this._dashboards.map(e=>({value:e.url_path,label:`${e.title}${"lovelace"===e.id?` (${this.hass.localize("ui.common.default")})`:""}`,disabled:"storage"!==e.mode})).sort((e,t)=>"lovelace"===e.value?-1:"lovelace"===t.value?1:e.label.localeCompare(t.label))):r.s6,!this._config||(this._config.views||[]).length<1?(0,r.qy)(w||(w=$`<ha-alert alert-type="error">${0}</ha-alert>`),this.hass.localize(this._config?"ui.panel.lovelace.editor.select_view.no_views":"ui.panel.lovelace.editor.select_view.no_config")):this._config.views.length>1?(0,r.qy)(x||(x=$` <ha-list> ${0} </ha-list> `),this._config.views.map((e,t)=>{var i,a;const o=(0,g.R)(e);return(0,r.qy)(_||(_=$` <ha-radio-list-item .graphic="${0}" @click="${0}" .value="${0}" .selected="${0}" .disabled="${0}" ?autofocus="${0}"> <span> ${0}${0} </span> <ha-icon .icon="${0}" slot="graphic"></ha-icon> </ha-radio-list-item> `),null!==(i=this._config)&&void 0!==i&&i.views.some(({icon:e})=>e)?"icon":r.s6,this._viewChanged,t.toString(),this._selectedViewIdx===t,o&&!(null!==(a=this._params)&&void 0!==a&&a.includeStrategyViews),0===t&&!this._params.allowDashboardChange,e.title,o?` (${this.hass.localize("ui.panel.lovelace.editor.select_view.strategy_type")})`:r.s6,e.icon)})):r.s6,this.closeDialog,this.hass.localize("ui.common.cancel"),!this._config||(this._config.views||[]).length<1,this._selectView,this._params.actionLabel||this.hass.localize("ui.common.move"))}async _getDashboards(){this._dashboards=this._params.dashboards||await(0,v.SJ)(this.hass)}async _dashboardChanged(e){let t=e.detail.value;if(t!==this._urlPath){"lovelace"===t&&(t=null),this._urlPath=t,this._selectedViewIdx=0;try{this._config=await(0,p.Dz)(this.hass.connection,t,!1)}catch(i){this._config=void 0}}}_viewChanged(e){const t=Number(e.target.value);isNaN(t)||(this._selectedViewIdx=t)}_selectView(){(0,l.r)(this,"view-selected",{view:this._selectedViewIdx}),this._params.viewSelectedCallback(this._urlPath,this._config,this._selectedViewIdx),this.closeDialog()}static get styles(){return[m.nA,(0,r.AH)(C||(C=$`ha-select{width:100%}mwc-radio-list-item{direction:ltr}`))]}constructor(...e){super(...e),this._dashboards=[],this._selectedViewIdx=0,this._open=!1}}(0,o.Cg)([(0,s.wk)()],k.prototype,"_params",void 0),(0,o.Cg)([(0,s.wk)()],k.prototype,"_dashboards",void 0),(0,o.Cg)([(0,s.wk)()],k.prototype,"_urlPath",void 0),(0,o.Cg)([(0,s.wk)()],k.prototype,"_config",void 0),(0,o.Cg)([(0,s.wk)()],k.prototype,"_selectedViewIdx",void 0),(0,o.Cg)([(0,s.wk)()],k.prototype,"_open",void 0),k=(0,o.Cg)([(0,s.EM)("hui-dialog-select-view")],k),a()}catch(y){a(y)}})}}]);
//# sourceMappingURL=40901.112b577e395ad77d.js.map