"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["92678"],{64481:function(e,t,a){a.d(t,{D:function(){return o},J:function(){return r}});a(3362);let i=!1;try{i="true"===window.localStorage.getItem("disableViewTransition")}catch(s){}const o=e=>{i=e},r=e=>{if(!document.startViewTransition||i)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},38962:function(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(94333),n=a(1087),h=a(26300),d=(a(67094),e([h]));h=(d.then?(await d)():d)[0];let c,p,u,g,v=e=>e;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",f={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class y extends r.WF{render(){return(0,r.qy)(c||(c=v` <div class="issue-type ${0}" role="alert"> <div class="icon ${0}"> <slot name="icon"> <ha-svg-icon .path="${0}"></ha-svg-icon> </slot> </div> <div class="${0}"> <div class="main-content"> ${0} <slot></slot> </div> <div class="action"> <slot name="action"> ${0} </slot> </div> </div> </div> `),(0,l.H)({[this.alertType]:!0}),this.title?"":"no-title",f[this.alertType],(0,l.H)({content:!0,narrow:this.narrow}),this.title?(0,r.qy)(p||(p=v`<div class="title">${0}</div>`),this.title):r.s6,this.dismissable?(0,r.qy)(u||(u=v`<ha-icon-button @click="${0}" label="Dismiss alert" .path="${0}"></ha-icon-button>`),this._dismissClicked,m):r.s6)}_dismissClicked(){(0,n.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}y.styles=(0,r.AH)(g||(g=v`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--ha-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`)),(0,o.Cg)([(0,s.MZ)()],y.prototype,"title",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"alert-type"})],y.prototype,"alertType",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],y.prototype,"dismissable",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],y.prototype,"narrow",void 0),y=(0,o.Cg)([(0,s.EM)("ha-alert")],y),i()}catch(c){i(c)}})},986:function(e,t,a){a.a(e,async function(e,t){try{a(44114),a(18111),a(20116),a(7588),a(42762),a(62953);var i=a(40445),o=a(96196),r=a(77845),s=a(29485),l=a(22786),n=a(78870),h=a(1087),d=a(38508),c=e([d]);d=(c.then?(await c)():c)[0];let p,u,g,v,m,f,y,b,w,_,x=e=>e;const C="M20.65,20.87L18.3,18.5L12,12.23L8.44,8.66L7,7.25L4.27,4.5L3,5.77L5.78,8.55C3.23,11.69 3.42,16.31 6.34,19.24C7.9,20.8 9.95,21.58 12,21.58C13.79,21.58 15.57,21 17.03,19.8L19.73,22.5L21,21.23L20.65,20.87M12,19.59C10.4,19.59 8.89,18.97 7.76,17.83C6.62,16.69 6,15.19 6,13.59C6,12.27 6.43,11 7.21,10L12,14.77V19.59M12,5.1V9.68L19.25,16.94C20.62,14 20.09,10.37 17.65,7.93L12,2.27L8.3,5.97L9.71,7.38L12,5.1Z",$="M17.5,12A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 17.5,9A1.5,1.5 0 0,1 19,10.5A1.5,1.5 0 0,1 17.5,12M14.5,8A1.5,1.5 0 0,1 13,6.5A1.5,1.5 0 0,1 14.5,5A1.5,1.5 0 0,1 16,6.5A1.5,1.5 0 0,1 14.5,8M9.5,8A1.5,1.5 0 0,1 8,6.5A1.5,1.5 0 0,1 9.5,5A1.5,1.5 0 0,1 11,6.5A1.5,1.5 0 0,1 9.5,8M6.5,12A1.5,1.5 0 0,1 5,10.5A1.5,1.5 0 0,1 6.5,9A1.5,1.5 0 0,1 8,10.5A1.5,1.5 0 0,1 6.5,12M12,3A9,9 0 0,0 3,12A9,9 0 0,0 12,21A1.5,1.5 0 0,0 13.5,19.5C13.5,19.11 13.35,18.76 13.11,18.5C12.88,18.23 12.73,17.88 12.73,17.5A1.5,1.5 0 0,1 14.23,16H16A5,5 0 0,0 21,11C21,6.58 16.97,3 12,3Z";class k extends o.WF{render(){var e,t;const a=null!==(e=null!==(t=this.value)&&void 0!==t?t:this.defaultColor)&&void 0!==e?e:"";return(0,o.qy)(p||(p=x` <ha-generic-picker .hass="${0}" .disabled="${0}" .required="${0}" .hideClearIcon="${0}" .label="${0}" .helper="${0}" .value="${0}" .getItems="${0}" .rowRenderer="${0}" .valueRenderer="${0}" @value-changed="${0}" .notFoundLabel="${0}" .getAdditionalItems="${0}"> </ha-generic-picker> `),this.hass,this.disabled,this.required,!this.value&&!!this.defaultColor,this.label,this.helper,a,this._getItems,this._rowRenderer,this._valueRenderer,this._valueChanged,this.hass.localize("ui.components.color-picker.no_colors_found"),this._getAdditionalItems)}_renderColorCircle(e){return(0,o.qy)(u||(u=x` <span style="${0}"></span> `),(0,s.W)({"--circle-color":(0,n.MP)(e),display:"block","background-color":"var(--circle-color, var(--divider-color))",border:"1px solid var(--outline-color)","border-radius":"var(--ha-border-radius-pill)",width:"20px",height:"20px","box-sizing":"border-box"}))}_valueChanged(e){e.stopPropagation();const t=e.detail.value,a=t&&t===this.defaultColor?void 0:null!=t?t:void 0;this.value=a,(0,h.r)(this,"value-changed",{value:this.value})}constructor(...e){super(...e),this.includeState=!1,this.includeNone=!1,this.disabled=!1,this.required=!1,this._getAdditionalItems=e=>{if(!e||""===e.trim())return[];return this._getColors(this.includeNone,this.includeState,this.defaultColor,this.value).find(t=>t.id===e)?[]:[{id:e,primary:this.hass.localize("ui.components.color-picker.custom_color"),secondary:e}]},this._getItems=()=>this._getColors(this.includeNone,this.includeState,this.defaultColor,this.value),this._getColors=(0,l.A)((e,t,a,i)=>{const o=[],r=this.hass.localize("ui.components.color-picker.default"),s=(e,t)=>t&&r?`${e} (${r})`:e;if(e){const e=this.hass.localize("ui.components.color-picker.none")||"None";o.push({id:"none",primary:s(e,"none"===a),icon_path:C})}if(t){const e=this.hass.localize("ui.components.color-picker.state")||"State";o.push({id:"state",primary:s(e,"state"===a),icon_path:$})}Array.from(n.lt).forEach(e=>{const t=this.hass.localize(`ui.components.color-picker.colors.${e}`)||e;o.push({id:e,primary:s(t,a===e)})});const l="none"===i||"state"===i||n.lt.has(i||"");return i&&i.length>0&&!l&&o.push({id:i,primary:i}),o}),this._rowRenderer=e=>(0,o.qy)(g||(g=x` <ha-combo-box-item type="button" compact="compact"> ${0} <span slot="headline">${0}</span> ${0} </ha-combo-box-item> `),"none"===e.id?(0,o.qy)(v||(v=x`<ha-svg-icon slot="start" .path="${0}"></ha-svg-icon>`),C):"state"===e.id?(0,o.qy)(m||(m=x`<ha-svg-icon slot="start" .path="${0}"></ha-svg-icon>`),$):(0,o.qy)(f||(f=x`<span slot="start"> ${0} </span>`),this._renderColorCircle(e.id)),e.primary,e.secondary?(0,o.qy)(y||(y=x`<span slot="supporting-text">${0}</span>`),e.secondary):o.s6),this._valueRenderer=e=>"none"===e?(0,o.qy)(b||(b=x` <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> <span slot="headline"> ${0} </span> `),C,this.hass.localize("ui.components.color-picker.none")):"state"===e?(0,o.qy)(w||(w=x` <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> <span slot="headline"> ${0} </span> `),$,this.hass.localize("ui.components.color-picker.state")):(0,o.qy)(_||(_=x` <span slot="start">${0}</span> <span slot="headline"> ${0} </span> `),this._renderColorCircle(e),this.hass.localize(`ui.components.color-picker.colors.${e}`)||e)}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],k.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)()],k.prototype,"label",void 0),(0,i.Cg)([(0,r.MZ)()],k.prototype,"helper",void 0),(0,i.Cg)([(0,r.MZ)()],k.prototype,"value",void 0),(0,i.Cg)([(0,r.MZ)({type:String,attribute:"default_color"})],k.prototype,"defaultColor",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"include_state"})],k.prototype,"includeState",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"include_none"})],k.prototype,"includeNone",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],k.prototype,"disabled",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],k.prototype,"required",void 0),k=(0,i.Cg)([(0,r.EM)("ha-color-picker")],k),t()}catch(p){t(p)}})},93444:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845);let s,l,n=e=>e;class h extends o.WF{render(){return(0,o.qy)(s||(s=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(l||(l=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}h=(0,i.Cg)([(0,r.EM)("ha-dialog-footer")],h)},76538:function(e,t,a){a(62953);var i=a(40445),o=a(96196),r=a(77845);let s,l,n,h,d,c,p=e=>e;class u extends o.WF{render(){const e=(0,o.qy)(s||(s=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(l||(l=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(h||(h=p`${0}${0}`),t,e):(0,o.qy)(d||(d=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],u)},72554:function(e,t,a){a.a(e,async function(e,t){try{a(3362),a(62953),a(49255);var i=a(40445),o=a(93900),r=a(96196),s=a(77845),l=a(32288),n=a(1087),h=a(64481),d=a(59992),c=a(14503),p=a(22348),u=(a(76538),a(26300)),g=e([o,u,d]);[o,u,d]=g.then?(await g)():g;let v,m,f,y,b,w,_,x=e=>e;const C="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class $ extends((0,d.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(v||(v=x` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @keydown="${0}" @wa-hide="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> ${0} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> ${0} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleKeyDown,this._handleHide,this._handleShow,this._handleAfterShow,this._handleAfterHide,this.withoutHeader?r.s6:(0,r.qy)(m||(m=x` <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`),this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",C,void 0!==this.headerTitle?(0,r.qy)(f||(f=x`<span slot="title" class="title" id="ha-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(y||(y=x`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(b||(b=x`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(w||(w=x`<slot name="headerSubtitle" slot="subtitle"></slot>`))),this._handleBodyScroll,this.renderScrollableFades())}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,h.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){var t;const a=(null===(t=e.detail)||void 0===t?void 0:t.source)===e.target.dialog;this.preventScrimClose&&this._escapePressed&&a&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,(0,r.AH)(_||(_=x`
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
      `))]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");var t;if(null!==e)e.id||(e.id="ha-dialog-autofocus"),null===(t=this.hass)||void 0===t||null===(t=t.auth.external)||void 0===t||t.fireMessage({type:"focus_element",payload:{element_id:e.id}});return}null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,n.r)(this,"closed"))}}}(0,i.Cg)([(0,s.MZ)({attribute:!1})],$.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],$.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],$.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],$.prototype,"open",void 0),(0,i.Cg)([(0,s.MZ)({reflect:!0})],$.prototype,"type",void 0),(0,i.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],$.prototype,"width",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],$.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-title"})],$.prototype,"headerTitle",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],$.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],$.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],$.prototype,"flexContent",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"without-header"})],$.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,s.wk)()],$.prototype,"_open",void 0),(0,i.Cg)([(0,s.P)(".body")],$.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,s.wk)()],$.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,s.Ls)({passive:!0})],$.prototype,"_handleBodyScroll",null),$=(0,i.Cg)([(0,s.EM)("ha-dialog")],$),t()}catch(v){t(v)}})},64138:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaIconPicker:function(){return x}});a(74423),a(44114),a(26910),a(18111),a(22489),a(7588),a(61701),a(13579),a(3362),a(27495),a(25440),a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(22786),n=a(1087),h=a(57769),d=(a(75064),a(38508)),c=(a(88945),e([d]));d=(c.then?(await c)():c)[0];let p,u,g,v=e=>e,m=[],f=!1;const y=(e,t)=>{var a;const i=`${t}:${e.name}`,o=e.name,r=o.split("-"),s=null!==(a=e.keywords)&&void 0!==a?a:[],l={iconName:o};return r.forEach((e,t)=>{l[`part${t}`]=e}),s.forEach((e,t)=>{l[`keyword${t}`]=e}),{id:i,primary:i,icon:i,search_labels:l,sorting_label:i}},b=async()=>{f=!0;const e=await a.e("81340").then(a.t.bind(a,25143,19));m=e.default.map(e=>y(e,"mdi"));const t=[];Object.keys(h.y).forEach(e=>{t.push(w(e))}),(await Promise.all(t)).forEach(e=>{m.push(...e)})},w=async e=>{try{const t=h.y[e].getIconList;if("function"!=typeof t)return[];return(await t()).map(t=>y(t,e))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},_=e=>(0,r.qy)(p||(p=v` <ha-combo-box-item type="button"> <ha-icon .icon="${0}" slot="start"></ha-icon> ${0} </ha-combo-box-item> `),e.id,e.id);class x extends r.WF{render(){return(0,r.qy)(u||(u=v` <ha-generic-picker .hass="${0}" allow-custom-value .getItems="${0}" .helper="${0}" .disabled="${0}" .required="${0}" .errorMessage="${0}" .invalid="${0}" .rowRenderer="${0}" .icon="${0}" .label="${0}" .value="${0}" .searchFn="${0}" popover-placement="bottom-start" @value-changed="${0}"> <slot name="start"></slot> </ha-generic-picker> `),this.hass,this._getIconPickerItems,this.helper,this.disabled,this.required,this.errorMessage,this.invalid,_,this._icon,this.label,this._value,this._filterIcons,this._valueChanged)}firstUpdated(){f||b().then(()=>{this._getIconPickerItems=()=>m,this.requestUpdate()})}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.r)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _icon(){var e;return null!==(e=this.value)&&void 0!==e&&e.length?this.value:this.placeholder}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._getIconPickerItems=()=>m,this._filterIcons=(0,l.A)((e,t,a)=>{const i=e.toLowerCase().replace(/\s+/g,"-"),o=null!=a&&a.length?a:t;if(!i.length)return o;const r=[];for(const s of o){const e=(s.id.split(":")[1]||s.id).toLowerCase().split("-"),t=s.search_labels?Object.values(s.search_labels).filter(e=>null!==e).map(e=>e.toLowerCase()):[],a=s.id.toLowerCase();e.includes(i)?r.push({item:s,rank:1}):t.includes(i)?r.push({item:s,rank:2}):a.includes(i)?r.push({item:s,rank:3}):t.some(e=>e.includes(i))&&r.push({item:s,rank:4})}return r.sort((e,t)=>e.rank-t.rank).map(e=>e.item)})}}x.styles=(0,r.AH)(g||(g=v`ha-generic-picker{width:100%;display:block}`)),(0,o.Cg)([(0,s.MZ)({attribute:!1})],x.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)()],x.prototype,"value",void 0),(0,o.Cg)([(0,s.MZ)()],x.prototype,"label",void 0),(0,o.Cg)([(0,s.MZ)()],x.prototype,"helper",void 0),(0,o.Cg)([(0,s.MZ)()],x.prototype,"placeholder",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"error-message"})],x.prototype,"errorMessage",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],x.prototype,"disabled",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],x.prototype,"required",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],x.prototype,"invalid",void 0),x=(0,o.Cg)([(0,s.EM)("ha-icon-picker")],x),i()}catch(p){i(p)}})},2846:function(e,t,a){a.d(t,{G:function(){return p},J:function(){return c}});var i=a(40445),o=a(12415),r=a(82553),s=a(96196),l=a(77845);a(54276);let n,h,d=e=>e;const c=[r.R,(0,s.AH)(n||(n=d`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`))];class p extends o.n{renderRipple(){return"text"===this.type?s.s6:(0,s.qy)(h||(h=d`<ha-ripple part="ripple" for="item" ?disabled="${0}"></ha-ripple>`),this.disabled&&"link"!==this.type)}}p.styles=c,p=(0,i.Cg)([(0,l.EM)("ha-md-list-item")],p)},59646:function(e,t,a){a(62953);var i=a(40445),o=a(4845),r=a(49065),s=a(96196),l=a(77845),n=a(88360);let h;class d extends o.U{firstUpdated(){super.firstUpdated(),this.addEventListener("change",()=>{this.haptic&&(0,n.j)(this,"light")})}constructor(...e){super(...e),this.haptic=!1}}d.styles=[r.R,(0,s.AH)(h||(h=(e=>e)`:host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}`))],(0,i.Cg)([(0,l.MZ)({type:Boolean})],d.prototype,"haptic",void 0),d=(0,i.Cg)([(0,l.EM)("ha-switch")],d)},56304:function(e,t,a){a(62953);var i=a(40445),o=a(11896),r=a(92347),s=a(75057),l=a(96196),n=a(77845);let h;class d extends o.u{updated(e){super.updated(e),this.autogrow&&e.has("value")&&(this.mdcRoot.dataset.value=this.value+'=​"')}constructor(...e){super(...e),this.autogrow=!1}}d.styles=[r.R,s.R,(0,l.AH)(h||(h=(e=>e)`:host([autogrow]) .mdc-text-field{position:relative;min-height:74px;min-width:178px;max-height:200px}:host([autogrow]) .mdc-text-field:after{content:attr(data-value);margin-top:23px;margin-bottom:9px;line-height:var(--ha-line-height-normal);min-height:42px;padding:0px 32px 0 16px;letter-spacing:var(
          --mdc-typography-subtitle1-letter-spacing,
          .009375em
        );visibility:hidden;white-space:pre-wrap}:host([autogrow]) .mdc-text-field__input{position:absolute;height:calc(100% - 32px)}:host([autogrow]) .mdc-text-field.mdc-text-field--no-label:after{margin-top:16px;margin-bottom:16px}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start) top}@media only screen and (min-width:459px){:host([mobile-multiline]) .mdc-text-field__input{white-space:nowrap;max-height:16px}}`))],(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],d.prototype,"autogrow",void 0),d=(0,i.Cg)([(0,n.EM)("ha-textarea")],d)},88360:function(e,t,a){a.d(t,{j:function(){return o}});var i=a(1087);const o=(e,t)=>{(0,i.r)(e,"haptic",t)}},427:function(e,t,a){a.a(e,async function(e,i){try{a.r(t);a(89463),a(3362),a(42762),a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(1087),n=a(38962),h=a(18350),d=a(986),c=(a(93444),a(64138)),p=(a(59646),a(72554)),u=(a(56304),a(75709),a(14503)),g=e([n,h,d,c,p]);[n,h,d,c,p]=g.then?(await g)():g;let v,m,f,y,b,w=e=>e;class _ extends r.WF{showDialog(e){this._params=e,this._error=void 0,this._params.entry?(this._name=this._params.entry.name||"",this._icon=this._params.entry.icon||"",this._color=this._params.entry.color||"",this._description=this._params.entry.description||""):(this._name=this._params.suggestedName||"",this._icon="",this._color="",this._description=""),this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._params=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params?(0,r.qy)(v||(v=w` <ha-dialog .hass="${0}" .open="${0}" header-title="${0}" prevent-scrim-close @closed="${0}"> <div> ${0} <div class="form"> <ha-textfield autofocus .value="${0}" .configValue="${0}" @input="${0}" .label="${0}" .validationMessage="${0}" required></ha-textfield> <ha-icon-picker .value="${0}" .hass="${0}" .configValue="${0}" @value-changed="${0}" .label="${0}"></ha-icon-picker> <ha-color-picker .value="${0}" .configValue="${0}" .hass="${0}" @value-changed="${0}" .label="${0}"></ha-color-picker> <ha-textarea .value="${0}" .configValue="${0}" @input="${0}" .label="${0}"></ha-textarea> </div> </div> <ha-dialog-footer slot="footer"> ${0} <ha-button slot="primaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-dialog> `),this.hass,this._open,this._params.entry?this._params.entry.name||this._params.entry.label_id:this.hass.localize("ui.dialogs.label-detail.new_label"),this._dialogClosed,this._error?(0,r.qy)(m||(m=w`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):"",this._name,"name",this._input,this.hass.localize("ui.dialogs.label-detail.name"),this.hass.localize("ui.dialogs.label-detail.required_error_msg"),this._icon,this.hass,"icon",this._valueChanged,this.hass.localize("ui.dialogs.label-detail.icon"),this._color,"color",this.hass,this._valueChanged,this.hass.localize("ui.dialogs.label-detail.color"),this._description,"description",this._input,this.hass.localize("ui.dialogs.label-detail.description"),this._params.entry&&this._params.removeEntry?(0,r.qy)(f||(f=w` <ha-button slot="secondaryAction" variant="danger" appearance="plain" @click="${0}" .disabled="${0}"> ${0} </ha-button> `),this._deleteEntry,this._submitting,this.hass.localize("ui.common.delete")):(0,r.qy)(y||(y=w` <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> `),this.closeDialog,this.hass.localize("ui.common.cancel")),this._updateEntry,this._submitting||!this._name,this._params.entry?this.hass.localize("ui.common.update"):this.hass.localize("ui.common.create")):r.s6}_input(e){const t=e.target,a=t.configValue;this._error=void 0,this[`_${a}`]=t.value}_valueChanged(e){const t=e.target.configValue;this._error=void 0,this[`_${t}`]=e.detail.value||""}async _updateEntry(){this._submitting=!0;try{const e={name:this._name.trim(),icon:this._icon.trim()||null,color:this._color.trim()||null,description:this._description.trim()||null};this._params.entry?await this._params.updateEntry(e):await this._params.createEntry(e),this.closeDialog()}catch(e){this._error=e?e.message:"Unknown error"}finally{this._submitting=!1}}async _deleteEntry(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}static get styles(){return[u.nA,(0,r.AH)(b||(b=w`a{color:var(--primary-color)}ha-color-picker,ha-icon-picker,ha-textarea,ha-textfield{display:block}ha-color-picker,ha-textarea{margin-top:16px}`))]}constructor(...e){super(...e),this._submitting=!1,this._open=!1}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],_.prototype,"hass",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_name",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_icon",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_color",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_description",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_error",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_params",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_submitting",void 0),(0,o.Cg)([(0,s.wk)()],_.prototype,"_open",void 0),_=(0,o.Cg)([(0,s.EM)("dialog-label-detail")],_),i()}catch(v){i(v)}})},88438:function(e,t,a){a.d(t,{C:function(){return i}});const i="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0}}]);
//# sourceMappingURL=92678.69c8508f92c6da8b.js.map