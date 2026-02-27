"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["94896"],{38962:function(e,t,i){i.a(e,async function(e,a){try{i.r(t);i(62953);var o=i(40445),s=i(96196),r=i(77845),n=i(94333),l=i(1087),d=i(26300),h=(i(67094),e([d]));d=(h.then?(await h)():h)[0];let c,p,v,u,g=e=>e;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",f={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class b extends s.WF{render(){return(0,s.qy)(c||(c=g` <div class="issue-type ${0}" role="alert"> <div class="icon ${0}"> <slot name="icon"> <ha-svg-icon .path="${0}"></ha-svg-icon> </slot> </div> <div class="${0}"> <div class="main-content"> ${0} <slot></slot> </div> <div class="action"> <slot name="action"> ${0} </slot> </div> </div> </div> `),(0,n.H)({[this.alertType]:!0}),this.title?"":"no-title",f[this.alertType],(0,n.H)({content:!0,narrow:this.narrow}),this.title?(0,s.qy)(p||(p=g`<div class="title">${0}</div>`),this.title):s.s6,this.dismissable?(0,s.qy)(v||(v=g`<ha-icon-button @click="${0}" label="Dismiss alert" .path="${0}"></ha-icon-button>`),this._dismissClicked,m):s.s6)}_dismissClicked(){(0,l.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}b.styles=(0,s.AH)(u||(u=g`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--ha-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`)),(0,o.Cg)([(0,r.MZ)()],b.prototype,"title",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"alert-type"})],b.prototype,"alertType",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],b.prototype,"dismissable",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],b.prototype,"narrow",void 0),b=(0,o.Cg)([(0,r.EM)("ha-alert")],b),a()}catch(c){a(c)}})},93444:function(e,t,i){var a=i(40445),o=i(96196),s=i(77845);let r,n,l=e=>e;class d extends o.WF{render(){return(0,o.qy)(r||(r=l` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(n||(n=l`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,a.Cg)([(0,s.EM)("ha-dialog-footer")],d)},76538:function(e,t,i){i(62953);var a=i(40445),o=i(96196),s=i(77845);let r,n,l,d,h,c,p=e=>e;class v extends o.WF{render(){const e=(0,o.qy)(r||(r=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(n||(n=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(l||(l=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(d||(d=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,a.Cg)([(0,s.MZ)({type:String,attribute:"subtitle-position"})],v.prototype,"subtitlePosition",void 0),(0,a.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],v.prototype,"showBorder",void 0),v=(0,a.Cg)([(0,s.EM)("ha-dialog-header")],v)},72554:function(e,t,i){i.a(e,async function(e,t){try{i(3362),i(62953);var a=i(40445),o=i(93900),s=i(96196),r=i(77845),n=i(32288),l=i(1087),d=i(59992),h=i(14503),c=i(22348),p=(i(76538),i(26300)),v=e([o,p,d]);[o,p,d]=v.then?(await v)():v;let u,g,m,f,b,y,_,w=e=>e;const x="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class L extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,s.qy)(u||(u=w` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,n.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?s.s6:(0,s.qy)(g||(g=w` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",x,void 0!==this.headerTitle?(0,s.qy)(m||(m=w`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,s.qy)(f||(f=w`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,s.qy)(b||(b=w`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,s.qy)(y||(y=w`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const i=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&i&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,(0,s.AH)(_||(_=w`
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

        :host([width="full"]) wa-dialog {
          --width: var(--full-width);
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,c.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,l.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,l.r)(this,"closed"))}}}(0,a.Cg)([(0,r.MZ)({attribute:!1})],L.prototype,"hass",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],L.prototype,"ariaLabelledBy",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],L.prototype,"ariaDescribedBy",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],L.prototype,"open",void 0),(0,a.Cg)([(0,r.MZ)({reflect:!0})],L.prototype,"type",void 0),(0,a.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],L.prototype,"width",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],L.prototype,"preventScrimClose",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"header-title"})],L.prototype,"headerTitle",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],L.prototype,"headerSubtitle",void 0),(0,a.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],L.prototype,"headerSubtitlePosition",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],L.prototype,"flexContent",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,attribute:"without-header"})],L.prototype,"withoutHeader",void 0),(0,a.Cg)([(0,r.wk)()],L.prototype,"_open",void 0),(0,a.Cg)([(0,r.P)(".body")],L.prototype,"bodyContainer",void 0),(0,a.Cg)([(0,r.wk)()],L.prototype,"_bodyScrolled",void 0),(0,a.Cg)([(0,r.Ls)({passive:!0})],L.prototype,"_handleBodyScroll",null),L=(0,a.Cg)([(0,r.EM)("ha-dialog")],L),t()}catch(u){t(u)}})},43661:function(e,t,i){i.r(t),i.d(t,{HaIconNext:function(){return n}});i(62953);var a=i(40445),o=i(77845),s=i(63091),r=i(67094);class n extends r.HaSvgIcon{constructor(...e){super(...e),this.path="rtl"===s.G.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}(0,a.Cg)([(0,o.MZ)()],n.prototype,"path",void 0),n=(0,a.Cg)([(0,o.EM)("ha-icon-next")],n)},28732:function(e,t,i){var a=i(40445),o=i(27686),s=i(7731),r=i(96196),n=i(77845);let l,d,h,c=e=>e;class p extends o.J{renderRipple(){return this.noninteractive?"":super.renderRipple()}static get styles(){return[s.R,(0,r.AH)(l||(l=c`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`)),"rtl"===document.dir?(0,r.AH)(d||(d=c`span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}`)):(0,r.AH)(h||(h=c``))]}}p=(0,a.Cg)([(0,n.EM)("ha-list-item")],p)},65829:function(e,t,i){i.a(e,async function(e,a){try{i.r(t),i.d(t,{HaSpinner:function(){return c}});var o=i(40445),s=i(55262),r=i(96196),n=i(77845),l=e([s]);s=(l.then?(await l)():l)[0];let d,h=e=>e;class c extends s.A{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-spinner-size","16px");break;case"small":this.style.setProperty("--ha-spinner-size","28px");break;case"medium":this.style.setProperty("--ha-spinner-size","48px");break;case"large":this.style.setProperty("--ha-spinner-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}static get styles(){return[s.A.styles,(0,r.AH)(d||(d=h`:host{--indicator-color:var(
            --ha-spinner-indicator-color,
            var(--primary-color)
          );--track-color:var(--ha-spinner-divider-color, var(--divider-color));--track-width:4px;--speed:3.5s;font-size:var(--ha-spinner-size, 48px)}`))]}}(0,o.Cg)([(0,n.MZ)()],c.prototype,"size",void 0),c=(0,o.Cg)([(0,n.EM)("ha-spinner")],c),a()}catch(d){a(d)}})},59992:function(e,t,i){i.a(e,async function(e,a){try{i.d(t,{V:function(){return u}});i(62953);var o=i(40445),s=i(88696),r=i(96196),n=i(94333),l=i(77845),d=e([s]);s=(d.then?(await d)():d)[0];let h,c,p=e=>e;const v=e=>void 0===e?[]:Array.isArray(e)?e:[e],u=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){var t;null===(t=super.firstUpdated)||void 0===t||t.call(this,e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){var t;null===(t=super.updated)||void 0===t||t.call(this,e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return(0,r.qy)(h||(h=p` <div class="${0}"></div> <div class="${0}"></div> `),(0,n.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled}),(0,n.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable}))}static get styles(){var e;const t=Object.getPrototypeOf(this);return[...v(null!==(e=null==t?void 0:t.styles)&&void 0!==e?e:[]),(0,r.AH)(c||(c=p`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`))]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){var e,t;this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),null===(e=(t=this._resize).unobserve)||void 0===e||e.call(t,this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:i=0,clientHeight:a=0,scrollTop:o=0}=e;this._contentScrollable=i-a>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{var t;const i=e.currentTarget;this._contentScrolled=(null!==(t=i.scrollTop)&&void 0!==t?t:0)>this.scrollFadeThreshold,this._updateScrollableState(i)},this._resize=new s.P(this,{target:null,callback:e=>{var t;const i=null===(t=e[0])||void 0===t?void 0:t.target;i&&this._updateScrollableState(i)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t};a()}catch(h){a(h)}})},50881:function(e,t,i){i.a(e,async function(e,a){try{i.r(t);i(74423),i(3362),i(62953);var o=i(40445),s=i(96196),r=i(77845),n=i(1087),l=i(38962),d=i(18350),h=(i(43661),i(28732),i(65829)),c=(i(93444),i(72554)),p=i(72001),v=i(14503),u=e([l,d,h,c]);[l,d,h,c]=u.then?(await u)():u;let g,m,f,b,y,_,w,x,L,C,$,k,M,S,H=e=>e;const z="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z",A="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",V="M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z",E="M22 14H21C21 10.13 17.87 7 14 7H13V5.73C13.6 5.39 14 4.74 14 4C14 2.9 13.11 2 12 2S10 2.9 10 4C10 4.74 10.4 5.39 11 5.73V7H10C6.13 7 3 10.13 3 14H2C1.45 14 1 14.45 1 15V18C1 18.55 1.45 19 2 19H3V20C3 21.11 3.9 22 5 22H19C20.11 22 21 21.11 21 20V19H22C22.55 19 23 18.55 23 18V15C23 14.45 22.55 14 22 14M9.86 16.68L8.68 17.86L7.5 16.68L6.32 17.86L5.14 16.68L6.32 15.5L5.14 14.32L6.32 13.14L7.5 14.32L8.68 13.14L9.86 14.32L8.68 15.5L9.86 16.68M18.86 16.68L17.68 17.86L16.5 16.68L15.32 17.86L14.14 16.68L15.32 15.5L14.14 14.32L15.32 13.14L16.5 14.32L17.68 13.14L18.86 14.32L17.68 15.5L18.86 16.68Z",q="M13 19C13 18.7 13 18.3 13.1 18H8V16H6V8H8V6H16V8H18V13.1C18.3 13 18.7 13 19 13C19.3 13 19.7 13 20 13.1V8H22V2H16V4H8V2H2V8H4V16H2V22H8V20H13.1C13 19.7 13 19.3 13 19M18 4H20V6H18V4M4 4H6V6H4V4M6 20H4V18H6V20M22.5 16.9L20.4 19L22.5 21.1L21.1 22.5L19 20.4L16.9 22.5L15.5 21.1L17.6 19L15.5 16.9L16.9 15.5L19 17.6L21.1 15.5L22.5 16.9Z",T=120;class Z extends s.WF{disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe()}async showDialog(e){if(this._entryId=e.entryId,this._deviceId=e.deviceId,this._onClose=e.onClose,this._open=!0,this._deviceId){const e=await(0,p.mQ)(this.hass,this._deviceId);this._device=this.hass.devices[this._deviceId],this._step=e.status===p.zI.Dead?"start_removal":"start"}else e.skipConfirmation?this._startExclusion():this._step="start_exclusion"}render(){if(!this._entryId)return s.s6;const e=this.hass.localize("ui.panel.config.zwave_js.remove_node.title");return(0,s.qy)(g||(g=H` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" prevent-scrim-close @closed="${0}"> <ha-icon-button slot="headerNavigationIcon" .path="${0}" @click="${0}" .label="${0}"></ha-icon-button> <div class="content">${0}</div> ${0} </ha-dialog> `),this.hass,this._open,e,this.handleDialogClosed,A,this.closeDialog,this.hass.localize("ui.common.close"),this._renderStepContent(),"start"===this._step?s.s6:(0,s.qy)(m||(m=H`<ha-dialog-footer slot="footer"> ${0} </ha-dialog-footer>`),this._renderAction()))}_renderStepContent(){return"start"===this._step?(0,s.qy)(f||(f=H` <ha-svg-icon .path="${0}"></ha-svg-icon> <p> ${0} </p> <div class="menu-options"> <ha-list-item hasMeta @click="${0}"> <span>${0}</span> <ha-icon-next slot="meta"></ha-icon-next> </ha-list-item> <ha-list-item hasMeta @click="${0}"> <span>${0}</span> <ha-icon-next slot="meta"></ha-icon-next> </ha-list-item> </div> `),q,this.hass.localize("ui.panel.config.zwave_js.remove_node.introduction"),this._startExclusion,this.hass.localize("ui.panel.config.zwave_js.remove_node.menu_exclude_device"),this._startRemoval,this.hass.localize("ui.panel.config.zwave_js.remove_node.menu_remove_device")):"start_removal"===this._step?(0,s.qy)(b||(b=H` <ha-svg-icon .path="${0}"></ha-svg-icon> <p> ${0} </p> `),E,this.hass.localize("ui.panel.config.zwave_js.remove_node.failed_node_intro",{name:this._device.name_by_user||this._device.name})):"start_exclusion"===this._step?(0,s.qy)(y||(y=H` <ha-svg-icon .path="${0}"></ha-svg-icon> <p> ${0} </p> `),q,this.hass.localize("ui.panel.config.zwave_js.remove_node.exclusion_intro")):["exclusion","remove"].includes(this._step)?(0,s.qy)(_||(_=H` <ha-spinner></ha-spinner> <div> <p> ${0} </p> </div> `),this.hass.localize("ui.panel.config.zwave_js.remove_node."+("exclusion"===this._step?"follow_device_instructions":"removing_device"))):"finished"===this._step?(0,s.qy)(w||(w=H` <ha-svg-icon .path="${0}" class="success"></ha-svg-icon> <p> ${0} </p>`),z,this.hass.localize("ui.panel.config.zwave_js.remove_node.exclusion_finished",{id:(0,s.qy)(x||(x=H`<b>${0}</b>`),this._node.node_id)})):(0,s.qy)(L||(L=H` <ha-svg-icon .path="${0}" class="failed"></ha-svg-icon> <p> ${0} </p> ${0} `),V,this.hass.localize("ui.panel.config.zwave_js.remove_node.exclusion_failed"),this._error?(0,s.qy)(C||(C=H`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):s.s6)}_renderAction(){return"start"===this._step?s.s6:"start_removal"===this._step?(0,s.qy)($||($=H` <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}" destructive> ${0} </ha-button> `),this.closeDialog,this.hass.localize("ui.common.cancel"),this._startRemoval,this.hass.localize("ui.common.remove")):"start_exclusion"===this._step?(0,s.qy)(k||(k=H` <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}" destructive> ${0} </ha-button> `),this.closeDialog,this.hass.localize("ui.common.cancel"),this._startExclusion,this.hass.localize("ui.panel.config.zwave_js.remove_node.start_exclusion")):(0,s.qy)(M||(M=H` <ha-button slot="primaryAction" @click="${0}"> ${0} </ha-button> `),this.closeDialog,this.hass.localize("exclusion"===this._step?"ui.panel.config.zwave_js.remove_node.cancel_exclusion":"ui.common.close"))}_startExclusion(){this._subscribed=this.hass.connection.subscribeMessage(this._handleMessage,{type:"zwave_js/remove_node",entry_id:this._entryId}).catch(e=>{this._step="failed",this._error=e.message}),this._step="exclusion",this._removeNodeTimeoutHandle=window.setTimeout(()=>{this._unsubscribe(),this._step="timeout"},1e3*T)}_startRemoval(){this._subscribed=(0,p.tj)(this.hass,this._deviceId,this._handleMessage).catch(e=>{this._step="failed",this._error=e.message}),this._step="remove"}_stopExclusion(){try{this.hass.callWS({type:"zwave_js/stop_exclusion",entry_id:this._entryId})}catch(e){console.error(e)}}closeDialog(){this._open?this._open=!1:this.handleDialogClosed()}handleDialogClosed(){this._unsubscribe(),this._entryId=void 0,this._step="start",this._open=!1,this._onClose&&this._onClose(),(0,n.r)(this,"dialog-closed",{dialog:this.localName})}static get styles(){return[v.nA,(0,s.AH)(S||(S=H`.content{display:flex;align-items:center;flex-direction:column;gap:var(--ha-space-4);text-align:center}.content ha-spinner{padding:32px 0}.content p{color:var(--secondary-text-color)}ha-svg-icon{padding:32px 0;width:48px;height:48px}ha-svg-icon.success{color:var(--success-color)}ha-svg-icon.failed{color:var(--error-color)}ha-alert{width:100%}.menu-options{align-self:stretch}ha-list-item{--mdc-list-side-padding:24px}`))]}constructor(...e){super(...e),this._step="start",this._open=!1,this._handleMessage=e=>{"exclusion failed"===e.event&&(this._unsubscribe(),this._step="failed"),"exclusion stopped"===e.event&&(this._step="remove"),"node removed"===e.event&&(this._step="finished",this._node=e.node,this._unsubscribe())},this._unsubscribe=()=>{this._subscribed&&(this._subscribed.then(e=>e&&e()),this._subscribed=void 0),"exclusion"===this._step&&this._entryId&&this._stopExclusion(),this._removeNodeTimeoutHandle&&clearTimeout(this._removeNodeTimeoutHandle)}}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],Z.prototype,"hass",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_entryId",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_deviceId",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_step",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_node",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_onClose",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_error",void 0),(0,o.Cg)([(0,r.wk)()],Z.prototype,"_open",void 0),Z=(0,o.Cg)([(0,r.EM)("dialog-zwave_js-remove-node")],Z),a()}catch(g){a(g)}})},69235:function(e,t,i){i.a(e,async function(e,t){try{i(3362),i(62953);"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await i.e("71055").then(i.bind(i,52370))).default),t()}catch(a){t(a)}},1)},22348:function(e,t,i){i.d(t,{V:function(){return o}});var a=i(37177);const o=e=>!!e.auth.external&&a.n},37177:function(e,t,i){i.d(t,{n:function(){return a}});i(27495);const a=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}}]);
//# sourceMappingURL=94896.ea3bbf1dc3d5442d.js.map