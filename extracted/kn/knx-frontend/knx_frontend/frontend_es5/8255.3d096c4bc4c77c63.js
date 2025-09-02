"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8255"],{22543:function(o,t,e){e.r(t);e(26847),e(27530);var r=e(73742),a=e(59048),i=e(7616),n=e(31733),s=e(29740);e(78645),e(40830);let l,c,d,h,p=o=>o;const u={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class v extends a.oi{render(){return(0,a.dy)(l||(l=p`
      <div
        class="issue-type ${0}"
        role="alert"
      >
        <div class="icon ${0}">
          <slot name="icon">
            <ha-svg-icon .path=${0}></ha-svg-icon>
          </slot>
        </div>
        <div class=${0}>
          <div class="main-content">
            ${0}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${0}
            </slot>
          </div>
        </div>
      </div>
    `),(0,n.$)({[this.alertType]:!0}),this.title?"":"no-title",u[this.alertType],(0,n.$)({content:!0,narrow:this.narrow}),this.title?(0,a.dy)(c||(c=p`<div class="title">${0}</div>`),this.title):a.Ld,this.dismissable?(0,a.dy)(d||(d=p`<ha-icon-button
                    @click=${0}
                    label="Dismiss alert"
                    .path=${0}
                  ></ha-icon-button>`),this._dismissClicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):a.Ld)}_dismissClicked(){(0,s.B)(this,"alert-dismissed-clicked")}constructor(...o){super(...o),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}v.styles=(0,a.iv)(h||(h=p`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
    }
    .issue-type::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      z-index: 1;
    }
    .icon.no-title {
      align-self: center;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      text-align: var(--float-start);
    }
    .content.narrow {
      flex-direction: column;
      align-items: flex-end;
    }
    .action {
      z-index: 1;
      width: min-content;
      --mdc-theme-primary: var(--primary-text-color);
    }
    .main-content {
      overflow-wrap: anywhere;
      word-break: break-word;
      margin-left: 8px;
      margin-right: 0;
      margin-inline-start: 8px;
      margin-inline-end: 0;
    }
    .title {
      margin-top: 2px;
      font-weight: var(--ha-font-weight-bold);
    }
    .action ha-icon-button {
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::after {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::after {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::after {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::after {
      background-color: var(--success-color);
    }
    :host ::slotted(ul) {
      margin: 0;
      padding-inline-start: 20px;
    }
  `)),(0,r.__decorate)([(0,i.Cb)()],v.prototype,"title",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:"alert-type"})],v.prototype,"alertType",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],v.prototype,"dismissable",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],v.prototype,"narrow",void 0),v=(0,r.__decorate)([(0,i.Mo)("ha-alert")],v)},30337:function(o,t,e){e.a(o,(async function(o,t){try{e(26847),e(27530),e(11807);var r=e(73742),a=e(71328),i=e(59048),n=e(7616),s=e(63871),l=o([a]);a=(l.then?(await l)():l)[0];let c,d=o=>o;class h extends a.Z{attachInternals(){const o=super.attachInternals();return Object.defineProperty(o,"states",{value:new s.C(this,o.states)}),o}static get styles(){return[a.Z.styles,(0,i.iv)(c||(c=d`
        .button {
          /* set theme vars */
          --wa-form-control-padding-inline: 16px;
          --wa-font-weight-action: var(--ha-font-weight-medium);
          --wa-border-radius-pill: 9999px;
          --wa-form-control-border-radius: var(
            --ha-button-radius,
            var(--wa-border-radius-pill)
          );

          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 40px)
          );

          font-size: var(--ha-font-size-m);
          line-height: 1;
        }

        :host([size="small"]) .button {
          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 32px)
          );
          font-size: var(--wa-font-size-s, var(--ha-font-size-m));
        }

        :host([variant="brand"]) {
          --color-fill-normal-active: var(--color-fill-primary-normal-active);
          --color-fill-normal-hover: var(--color-fill-primary-normal-hover);
          --color-fill-loud-active: var(--color-fill-primary-loud-active);
          --color-fill-loud-hover: var(--color-fill-primary-loud-hover);
        }

        :host([variant="neutral"]) {
          --color-fill-normal-active: var(--color-fill-neutral-normal-active);
          --color-fill-normal-hover: var(--color-fill-neutral-normal-hover);
          --color-fill-loud-active: var(--color-fill-neutral-loud-active);
          --color-fill-loud-hover: var(--color-fill-neutral-loud-hover);
        }

        :host([variant="success"]) {
          --color-fill-normal-active: var(--color-fill-success-normal-active);
          --color-fill-normal-hover: var(--color-fill-success-normal-hover);
          --color-fill-loud-active: var(--color-fill-success-loud-active);
          --color-fill-loud-hover: var(--color-fill-success-loud-hover);
        }

        :host([variant="warning"]) {
          --color-fill-normal-active: var(--color-fill-warning-normal-active);
          --color-fill-normal-hover: var(--color-fill-warning-normal-hover);
          --color-fill-loud-active: var(--color-fill-warning-loud-active);
          --color-fill-loud-hover: var(--color-fill-warning-loud-hover);
        }

        :host([variant="danger"]) {
          --color-fill-normal-active: var(--color-fill-danger-normal-active);
          --color-fill-normal-hover: var(--color-fill-danger-normal-hover);
          --color-fill-loud-active: var(--color-fill-danger-loud-active);
          --color-fill-loud-hover: var(--color-fill-danger-loud-hover);
        }

        :host([appearance~="plain"]) .button {
          color: var(--wa-color-on-normal);
        }
        :host([appearance~="plain"]) .button.disabled {
          background-color: var(--transparent-none);
          color: var(--color-on-disabled-quiet);
        }

        :host([appearance~="outlined"]) .button.disabled {
          background-color: var(--transparent-none);
          color: var(--color-on-disabled-quiet);
        }

        @media (hover: hover) {
          :host([appearance~="filled"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--color-fill-normal-hover);
          }
          :host([appearance~="accent"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--color-fill-loud-hover);
          }
          :host([appearance~="plain"])
            .button:not(.disabled):not(.loading):hover {
            color: var(--wa-color-on-normal);
          }
        }
        :host([appearance~="filled"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--color-fill-normal-active);
        }
        :host([appearance~="filled"]) .button.disabled {
          background-color: var(--color-fill-disabled-normal-resting);
          color: var(--color-on-disabled-normal);
        }

        :host([appearance~="accent"]) .button {
          background-color: var(
            --wa-color-fill-loud,
            var(--wa-color-neutral-fill-loud)
          );
        }
        :host([appearance~="accent"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--color-fill-loud-active);
        }
        :host([appearance~="accent"]) .button.disabled {
          background-color: var(--color-fill-disabled-loud-resting);
          color: var(--color-on-disabled-loud);
        }

        :host([loading]) {
          pointer-events: none;
        }

        .button.disabled {
          opacity: 1;
        }
      `))]}constructor(...o){super(...o),this.variant="brand"}}h=(0,r.__decorate)([(0,n.Mo)("ha-button")],h),t()}catch(c){t(c)}}))},64218:function(o,t,e){e.r(t),e.d(t,{HaIconButtonArrowPrev:function(){return c}});e(26847),e(27530);var r=e(73742),a=e(59048),i=e(7616),n=e(51597);e(78645);let s,l=o=>o;class c extends a.oi{render(){var o;return(0,a.dy)(s||(s=l`
      <ha-icon-button
        .disabled=${0}
        .label=${0}
        .path=${0}
      ></ha-icon-button>
    `),this.disabled,this.label||(null===(o=this.hass)||void 0===o?void 0:o.localize("ui.common.back"))||"Back",this._icon)}constructor(...o){super(...o),this.disabled=!1,this._icon="rtl"===n.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}}(0,r.__decorate)([(0,i.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,r.__decorate)([(0,i.Cb)()],c.prototype,"label",void 0),(0,r.__decorate)([(0,i.SB)()],c.prototype,"_icon",void 0),c=(0,r.__decorate)([(0,i.Mo)("ha-icon-button-arrow-prev")],c)},78645:function(o,t,e){e.r(t),e.d(t,{HaIconButton:function(){return p}});e(26847),e(27530);var r=e(73742),a=(e(1023),e(59048)),i=e(7616),n=e(25191);e(40830);let s,l,c,d,h=o=>o;class p extends a.oi{focus(){var o;null===(o=this._button)||void 0===o||o.focus()}render(){return(0,a.dy)(s||(s=h`
      <mwc-icon-button
        aria-label=${0}
        title=${0}
        aria-haspopup=${0}
        .disabled=${0}
      >
        ${0}
      </mwc-icon-button>
    `),(0,n.o)(this.label),(0,n.o)(this.hideTitle?void 0:this.label),(0,n.o)(this.ariaHasPopup),this.disabled,this.path?(0,a.dy)(l||(l=h`<ha-svg-icon .path=${0}></ha-svg-icon>`),this.path):(0,a.dy)(c||(c=h`<slot></slot>`)))}constructor(...o){super(...o),this.disabled=!1,this.hideTitle=!1}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},p.styles=(0,a.iv)(d||(d=h`
    :host {
      display: inline-block;
      outline: none;
    }
    :host([disabled]) {
      pointer-events: none;
    }
    mwc-icon-button {
      --mdc-theme-on-primary: currentColor;
      --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
    }
  `)),(0,r.__decorate)([(0,i.Cb)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,r.__decorate)([(0,i.Cb)({type:String})],p.prototype,"path",void 0),(0,r.__decorate)([(0,i.Cb)({type:String})],p.prototype,"label",void 0),(0,r.__decorate)([(0,i.Cb)({type:String,attribute:"aria-haspopup"})],p.prototype,"ariaHasPopup",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:"hide-title",type:Boolean})],p.prototype,"hideTitle",void 0),(0,r.__decorate)([(0,i.IO)("mwc-icon-button",!0)],p.prototype,"_button",void 0),p=(0,r.__decorate)([(0,i.Mo)("ha-icon-button")],p)},38098:function(o,t,e){e(40777),e(26847),e(27530);var r=e(73742),a=e(59048),i=e(7616),n=e(29740);e(87799);class s{processMessage(o){if("removed"===o.type)for(const t of Object.keys(o.notifications))delete this.notifications[t];else this.notifications=Object.assign(Object.assign({},this.notifications),o.notifications);return Object.values(this.notifications)}constructor(){this.notifications={}}}e(78645);let l,c,d,h=o=>o;class p extends a.oi{connectedCallback(){super.connectedCallback(),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}disconnectedCallback(){super.disconnectedCallback(),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}render(){if(!this._show)return a.Ld;const o=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return(0,a.dy)(l||(l=h`
      <ha-icon-button
        .label=${0}
        .path=${0}
        @click=${0}
      ></ha-icon-button>
      ${0}
    `),this.hass.localize("ui.sidebar.sidebar_toggle"),"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z",this._toggleMenu,o?(0,a.dy)(c||(c=h`<div class="dot"></div>`)):"")}firstUpdated(o){super.firstUpdated(o),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}willUpdate(o){if(super.willUpdate(o),!o.has("narrow")&&!o.has("hass"))return;const t=o.has("hass")?o.get("hass"):this.hass,e=(o.has("narrow")?o.get("narrow"):this.narrow)||"always_hidden"===(null==t?void 0:t.dockedSidebar),r=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&e===r||(this._show=r||this._alwaysVisible,r?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}_subscribeNotifications(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((o,t)=>{const e=new s,r=o.subscribeMessage((o=>t(e.processMessage(o))),{type:"persistent_notification/subscribe"});return()=>{r.then((o=>null==o?void 0:o()))}})(this.hass.connection,(o=>{this._hasNotifications=o.length>0}))}_toggleMenu(){(0,n.B)(this,"hass-toggle-menu")}constructor(...o){super(...o),this.hassio=!1,this.narrow=!1,this._hasNotifications=!1,this._show=!1,this._alwaysVisible=!1,this._attachNotifOnConnect=!1}}p.styles=(0,a.iv)(d||(d=h`
    :host {
      position: relative;
    }
    .dot {
      pointer-events: none;
      position: absolute;
      background-color: var(--accent-color);
      width: 12px;
      height: 12px;
      top: 9px;
      right: 7px;
      inset-inline-end: 7px;
      inset-inline-start: initial;
      border-radius: 50%;
      border: 2px solid var(--app-header-background-color);
    }
  `)),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],p.prototype,"hassio",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],p.prototype,"narrow",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,r.__decorate)([(0,i.SB)()],p.prototype,"_hasNotifications",void 0),(0,r.__decorate)([(0,i.SB)()],p.prototype,"_show",void 0),p=(0,r.__decorate)([(0,i.Mo)("ha-menu-button")],p)},40830:function(o,t,e){e.r(t),e.d(t,{HaSvgIcon:function(){return h}});var r=e(73742),a=e(59048),i=e(7616);let n,s,l,c,d=o=>o;class h extends a.oi{render(){return(0,a.YP)(n||(n=d`
    <svg
      viewBox=${0}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${0}
        ${0}
      </g>
    </svg>`),this.viewBox||"0 0 24 24",this.path?(0,a.YP)(s||(s=d`<path class="primary-path" d=${0}></path>`),this.path):a.Ld,this.secondaryPath?(0,a.YP)(l||(l=d`<path class="secondary-path" d=${0}></path>`),this.secondaryPath):a.Ld)}}h.styles=(0,a.iv)(c||(c=d`
    :host {
      display: var(--ha-icon-display, inline-flex);
      align-items: center;
      justify-content: center;
      position: relative;
      vertical-align: middle;
      fill: var(--icon-primary-color, currentcolor);
      width: var(--mdc-icon-size, 24px);
      height: var(--mdc-icon-size, 24px);
    }
    svg {
      width: 100%;
      height: 100%;
      pointer-events: none;
      display: block;
    }
    path.primary-path {
      opacity: var(--icon-primary-opactity, 1);
    }
    path.secondary-path {
      fill: var(--icon-secondary-color, currentcolor);
      opacity: var(--icon-secondary-opactity, 0.5);
    }
  `)),(0,r.__decorate)([(0,i.Cb)()],h.prototype,"path",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],h.prototype,"secondaryPath",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],h.prototype,"viewBox",void 0),h=(0,r.__decorate)([(0,i.Mo)("ha-svg-icon")],h)},65706:function(o,t,e){e.a(o,(async function(o,r){try{e.r(t);e(26847),e(27530);var a=e(73742),i=e(59048),n=e(7616),s=(e(64218),e(30337)),l=(e(38098),e(22543),o([s]));s=(l.then?(await l)():l)[0];let c,d,h,p,u,v=o=>o;class b extends i.oi{render(){var o,t;return(0,i.dy)(c||(c=v`
      ${0}
      <div class="content">
        <ha-alert alert-type="error">${0}</ha-alert>
        <slot>
          <ha-button appearance="plain" size="small" @click=${0}>
            ${0}
          </ha-button>
        </slot>
      </div>
    `),this.toolbar?(0,i.dy)(d||(d=v`<div class="toolbar">
            ${0}
          </div>`),this.rootnav||null!==(o=history.state)&&void 0!==o&&o.root?(0,i.dy)(h||(h=v`
                  <ha-menu-button
                    .hass=${0}
                    .narrow=${0}
                  ></ha-menu-button>
                `),this.hass,this.narrow):(0,i.dy)(p||(p=v`
                  <ha-icon-button-arrow-prev
                    .hass=${0}
                    @click=${0}
                  ></ha-icon-button-arrow-prev>
                `),this.hass,this._handleBack)):"",this.error,this._handleBack,null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.back"))}_handleBack(){history.back()}static get styles(){return[(0,i.iv)(u||(u=v`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: var(--ha-font-size-xl);
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: var(--ha-font-weight-normal);
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          color: var(--primary-text-color);
          height: calc(100% - var(--header-height));
          display: flex;
          padding: 16px;
          align-items: center;
          justify-content: center;
          flex-direction: column;
          box-sizing: border-box;
        }
        a {
          color: var(--primary-color);
        }
        ha-alert {
          margin-bottom: 16px;
        }
      `))]}constructor(...o){super(...o),this.toolbar=!0,this.rootnav=!1,this.narrow=!1}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],b.prototype,"toolbar",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],b.prototype,"rootnav",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],b.prototype,"narrow",void 0),(0,a.__decorate)([(0,n.Cb)()],b.prototype,"error",void 0),b=(0,a.__decorate)([(0,n.Mo)("hass-error-screen")],b),r()}catch(c){r(c)}}))},63871:function(o,t,e){e.d(t,{C:function(){return r}});e(26847),e(64455),e(67886),e(65451),e(46015),e(38334),e(94880),e(75643),e(29761),e(6202),e(27530);class r extends Set{add(o){super.add(o);const t=this._existing;if(t)try{t.add(o)}catch(e){t.add(`--${o}`)}else this._el.setAttribute(`state-${o}`,"");return this}delete(o){super.delete(o);const t=this._existing;return t?(t.delete(o),t.delete(`--${o}`)):this._el.removeAttribute(`state-${o}`),!0}has(o){return super.has(o)}clear(){for(const o of this)this.delete(o)}constructor(o,t=null){super(),this._existing=null,this._el=o,this._existing=t}}const a=CSSStyleSheet.prototype.replaceSync;Object.defineProperty(CSSStyleSheet.prototype,"replaceSync",{value:function(o){o=o.replace(/:state\(([^)]+)\)/g,":where(:state($1), :--$1, [state-$1])"),a.call(this,o)}})},17322:function(o,t,e){var r=e(47441),a=Math.floor,i=function(o,t){var e=o.length;if(e<8)for(var n,s,l=1;l<e;){for(s=l,n=o[l];s&&t(o[s-1],n)>0;)o[s]=o[--s];s!==l++&&(o[s]=n)}else for(var c=a(e/2),d=i(r(o,0,c),t),h=i(r(o,c),t),p=d.length,u=h.length,v=0,b=0;v<p||b<u;)o[v+b]=v<p&&b<u?t(d[v],h[b])<=0?d[v++]:h[b++]:v<p?d[v++]:h[b++];return o};o.exports=i},61392:function(o,t,e){var r=e(37579).match(/firefox\/(\d+)/i);o.exports=!!r&&+r[1]},71949:function(o,t,e){var r=e(37579);o.exports=/MSIE|Trident/.test(r)},53047:function(o,t,e){var r=e(37579).match(/AppleWebKit\/(\d+)\./);o.exports=!!r&&+r[1]},95766:function(o,t,e){var r=e(30456),a=e(18050);o.exports=function(o){if(a){try{return r.process.getBuiltinModule(o)}catch(t){}try{return Function('return require("'+o+'")')()}catch(t){}}}}}]);
//# sourceMappingURL=8255.3d096c4bc4c77c63.js.map