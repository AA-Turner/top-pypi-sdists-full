export const __webpack_ids__=["2998"];export const __webpack_modules__={74608:function(t,o,e){function a(t){return null==t||Array.isArray(t)?t:[t]}e.d(o,{r:()=>a})},42822:function(t,o,e){e.d(o,{p:()=>a});const a=(t,o)=>t&&t.config.components.includes(o)},40985:function(t,o,e){e.d(o,{i:()=>i});const a=(0,e(48112).P)((t=>{history.replaceState({scrollPosition:t},"")}),300);function i(t){return(o,e)=>{if("object"==typeof e)throw new Error("This decorator does not support this compilation type.");const i=o.connectedCallback;o.connectedCallback=function(){i.call(this);const o=this[e];o&&this.updateComplete.then((()=>{const e=this.renderRoot.querySelector(t);e&&setTimeout((()=>{e.scrollTop=o}),0)}))};const r=Object.getOwnPropertyDescriptor(o,e);let n;if(void 0===r)n={get(){return this[`__${String(e)}`]||history.state?.scrollPosition},set(t){a(t),this[`__${String(e)}`]=t},configurable:!0,enumerable:!0};else{const t=r.set;n={...r,set(o){a(o),this[`__${String(e)}`]=o,t?.call(this,o)}}}Object.defineProperty(o,e,n)}}},48112:function(t,o,e){e.d(o,{P:()=>a});const a=(t,o,e=!0,a=!0)=>{let i,r=0;const n=(...n)=>{const s=()=>{r=!1===e?0:Date.now(),i=void 0,t(...n)},l=Date.now();r||!1!==e||(r=l);const c=o-(l-r);c<=0||c>o?(i&&(clearTimeout(i),i=void 0),r=l,t(...n)):i||!1===a||(i=window.setTimeout(s,c))};return n.cancel=()=>{clearTimeout(i),i=void 0,r=0},n}},64218:function(t,o,e){e.r(o),e.d(o,{HaIconButtonArrowPrev:()=>s});var a=e(73742),i=e(59048),r=e(7616),n=e(51597);e(78645);class s extends i.oi{render(){return i.dy`
      <ha-icon-button
        .disabled=${this.disabled}
        .label=${this.label||this.hass?.localize("ui.common.back")||"Back"}
        .path=${this._icon}
      ></ha-icon-button>
    `}constructor(...t){super(...t),this.disabled=!1,this._icon="rtl"===n.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}}(0,a.__decorate)([(0,r.Cb)({attribute:!1})],s.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],s.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)()],s.prototype,"label",void 0),(0,a.__decorate)([(0,r.SB)()],s.prototype,"_icon",void 0),s=(0,a.__decorate)([(0,r.Mo)("ha-icon-button-arrow-prev")],s)},78645:function(t,o,e){e.r(o),e.d(o,{HaIconButton:()=>s});var a=e(73742),i=(e(1023),e(59048)),r=e(7616),n=e(25191);e(40830);class s extends i.oi{focus(){this._button?.focus()}render(){return i.dy`
      <mwc-icon-button
        aria-label=${(0,n.o)(this.label)}
        title=${(0,n.o)(this.hideTitle?void 0:this.label)}
        aria-haspopup=${(0,n.o)(this.ariaHasPopup)}
        .disabled=${this.disabled}
      >
        ${this.path?i.dy`<ha-svg-icon .path=${this.path}></ha-svg-icon>`:i.dy`<slot></slot>`}
      </mwc-icon-button>
    `}constructor(...t){super(...t),this.disabled=!1,this.hideTitle=!1}}s.shadowRootOptions={mode:"open",delegatesFocus:!0},s.styles=i.iv`
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
  `,(0,a.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({type:String})],s.prototype,"path",void 0),(0,a.__decorate)([(0,r.Cb)({type:String})],s.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)({type:String,attribute:"aria-haspopup"})],s.prototype,"ariaHasPopup",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"hide-title",type:Boolean})],s.prototype,"hideTitle",void 0),(0,a.__decorate)([(0,r.IO)("mwc-icon-button",!0)],s.prototype,"_button",void 0),s=(0,a.__decorate)([(0,r.Mo)("ha-icon-button")],s)},38098:function(t,o,e){var a=e(73742),i=e(59048),r=e(7616),n=e(29740);class s{processMessage(t){if("removed"===t.type)for(const o of Object.keys(t.notifications))delete this.notifications[o];else this.notifications={...this.notifications,...t.notifications};return Object.values(this.notifications)}constructor(){this.notifications={}}}e(78645);class l extends i.oi{connectedCallback(){super.connectedCallback(),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}disconnectedCallback(){super.disconnectedCallback(),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}render(){if(!this._show)return i.Ld;const t=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return i.dy`
      <ha-icon-button
        .label=${this.hass.localize("ui.sidebar.sidebar_toggle")}
        .path=${"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}
        @click=${this._toggleMenu}
      ></ha-icon-button>
      ${t?i.dy`<div class="dot"></div>`:""}
    `}firstUpdated(t){super.firstUpdated(t),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}willUpdate(t){if(super.willUpdate(t),!t.has("narrow")&&!t.has("hass"))return;const o=t.has("hass")?t.get("hass"):this.hass,e=(t.has("narrow")?t.get("narrow"):this.narrow)||"always_hidden"===o?.dockedSidebar,a=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&e===a||(this._show=a||this._alwaysVisible,a?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}_subscribeNotifications(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((t,o)=>{const e=new s,a=t.subscribeMessage((t=>o(e.processMessage(t))),{type:"persistent_notification/subscribe"});return()=>{a.then((t=>t?.()))}})(this.hass.connection,(t=>{this._hasNotifications=t.length>0}))}_toggleMenu(){(0,n.B)(this,"hass-toggle-menu")}constructor(...t){super(...t),this.hassio=!1,this.narrow=!1,this._hasNotifications=!1,this._show=!1,this._alwaysVisible=!1,this._attachNotifOnConnect=!1}}l.styles=i.iv`
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
  `,(0,a.__decorate)([(0,r.Cb)({type:Boolean})],l.prototype,"hassio",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],l.prototype,"narrow",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,r.SB)()],l.prototype,"_hasNotifications",void 0),(0,a.__decorate)([(0,r.SB)()],l.prototype,"_show",void 0),l=(0,a.__decorate)([(0,r.Mo)("ha-menu-button")],l)},40830:function(t,o,e){e.r(o),e.d(o,{HaSvgIcon:()=>n});var a=e(73742),i=e(59048),r=e(7616);class n extends i.oi{render(){return i.YP`
    <svg
      viewBox=${this.viewBox||"0 0 24 24"}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${this.path?i.YP`<path class="primary-path" d=${this.path}></path>`:i.Ld}
        ${this.secondaryPath?i.YP`<path class="secondary-path" d=${this.secondaryPath}></path>`:i.Ld}
      </g>
    </svg>`}}n.styles=i.iv`
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
  `,(0,a.__decorate)([(0,r.Cb)()],n.prototype,"path",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],n.prototype,"secondaryPath",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],n.prototype,"viewBox",void 0),n=(0,a.__decorate)([(0,r.Mo)("ha-svg-icon")],n)},62790:function(t,o,e){var a=e(73742),i=e(59048),r=e(7616),n=e(31733),s=e(28105),l=e(74608),c=e(42822);const h=(t,o)=>!o.component||(0,l.r)(o.component).some((o=>(0,c.p)(t,o))),d=(t,o)=>!o.not_component||!(0,l.r)(o.not_component).some((o=>(0,c.p)(t,o))),p=t=>t.core,b=(t,o)=>(t=>t.advancedOnly)(o)&&!(t=>t.userData?.showAdvanced)(t);var v=e(40985),u=(e(64218),e(38098),e(40830),e(25191)),f=e(67466),m=e(86857),g=e(51544);class y extends m.H{attach(t){super.attach(t),this.attachableTouchController.attach(t)}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(t,o){t?.removeEventListener("touchend",this._handleTouchEnd),o?.addEventListener("touchend",this._handleTouchEnd)}constructor(...t){super(...t),this.attachableTouchController=new f.J(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}y.styles=[g.W,i.iv`
      :host {
        --md-ripple-hover-opacity: var(--ha-ripple-hover-opacity, 0.08);
        --md-ripple-pressed-opacity: var(--ha-ripple-pressed-opacity, 0.12);
        --md-ripple-hover-color: var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
        --md-ripple-pressed-color: var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
      }
    `],y=(0,a.__decorate)([(0,r.Mo)("ha-ripple")],y);class _ extends i.oi{render(){return i.dy`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${(0,u.o)(this.name)}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?i.dy`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        <ha-ripple></ha-ripple>
      </div>
    `}_handleKeyDown(t){"Enter"===t.key&&t.target.click()}constructor(...t){super(...t),this.active=!1,this.narrow=!1}}_.styles=i.iv`
    div {
      padding: 0 32px;
      display: flex;
      flex-direction: column;
      text-align: center;
      box-sizing: border-box;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: var(--header-height);
      cursor: pointer;
      position: relative;
      outline: none;
    }

    .name {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }

    :host([active]) {
      color: var(--primary-color);
    }

    :host(:not([narrow])[active]) div {
      border-bottom: 2px solid var(--primary-color);
    }

    :host([narrow]) {
      min-width: 0;
      display: flex;
      justify-content: center;
      overflow: hidden;
    }

    :host([narrow]) div {
      padding: 0 4px;
    }

    div:focus-visible:before {
      position: absolute;
      display: block;
      content: "";
      inset: 0;
      background-color: var(--secondary-text-color);
      opacity: 0.08;
    }
  `,(0,a.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],_.prototype,"active",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],_.prototype,"narrow",void 0),(0,a.__decorate)([(0,r.Cb)()],_.prototype,"name",void 0),_=(0,a.__decorate)([(0,r.Mo)("ha-tab")],_);var w=e(77204);class x extends i.oi{willUpdate(t){t.has("route")&&(this._activeTab=this.tabs.find((t=>`${this.route.prefix}${this.route.path}`.includes(t.path)))),super.willUpdate(t)}render(){const t=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),o=t.length>1;return i.dy`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${this.mainPage||!this.backPath&&history.state?.root?i.dy`
                  <ha-menu-button
                    .hassio=${this.supervisor}
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:this.backPath?i.dy`
                    <a href=${this.backPath}>
                      <ha-icon-button-arrow-prev
                        .hass=${this.hass}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `:i.dy`
                    <ha-icon-button-arrow-prev
                      .hass=${this.hass}
                      @click=${this._backTapped}
                    ></ha-icon-button-arrow-prev>
                  `}
            ${this.narrow||!o?i.dy`<div class="main-title">
                  <slot name="header">${o?"":t[0]}</slot>
                </div>`:""}
            ${o&&!this.narrow?i.dy`<div id="tabbar">${t}</div>`:""}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${o&&this.narrow?i.dy`<div id="tabbar" class="bottom-bar">${t}</div>`:""}
      </div>
      <div class="container">
        ${this.pane?i.dy`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`:i.Ld}
        <div
          class="content ha-scrollbar ${(0,n.$)({tabs:o})}"
          @scroll=${this._saveScrollPos}
        >
          <slot></slot>
          ${this.hasFab?i.dy`<div class="fab-bottom-space"></div>`:i.Ld}
        </div>
      </div>
      <div id="fab" class=${(0,n.$)({tabs:o})}>
        <slot name="fab"></slot>
      </div>
    `}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop}_backTapped(){this.backCallback?this.backCallback():history.back()}static get styles(){return[w.$c,i.iv`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .container {
          display: flex;
          height: calc(100% - var(--header-height));
        }

        :host([narrow]) .container {
          height: 100%;
        }

        ha-menu-button {
          margin-right: 24px;
          margin-inline-end: 24px;
          margin-inline-start: initial;
        }

        .toolbar {
          font-size: var(--ha-font-size-xl);
          height: var(--header-height);
          background-color: var(--sidebar-background-color);
          font-weight: var(--ha-font-weight-normal);
          border-bottom: 1px solid var(--divider-color);
          box-sizing: border-box;
        }
        .toolbar-content {
          padding: 8px 12px;
          display: flex;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar-content {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }
        .bottom-bar a {
          width: 25%;
        }

        #tabbar {
          display: flex;
          font-size: var(--ha-font-size-m);
          overflow: hidden;
        }

        #tabbar > a {
          overflow: hidden;
          max-width: 45%;
        }

        #tabbar.bottom-bar {
          position: absolute;
          bottom: 0;
          left: 0;
          padding: 0 16px;
          box-sizing: border-box;
          background-color: var(--sidebar-background-color);
          border-top: 1px solid var(--divider-color);
          justify-content: space-around;
          z-index: 2;
          font-size: var(--ha-font-size-s);
          width: 100%;
          padding-bottom: var(--safe-area-inset-bottom);
        }

        #tabbar:not(.bottom-bar) {
          flex: 1;
          justify-content: center;
        }

        :host(:not([narrow])) #toolbar-icon {
          min-width: 40px;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          display: flex;
          flex-shrink: 0;
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          flex: 1;
          max-height: var(--header-height);
          line-height: var(--ha-line-height-normal);
          color: var(--sidebar-text-color);
          margin: var(--main-title-margin, var(--margin-title));
        }

        .content {
          position: relative;
          width: calc(
            100% - var(--safe-area-inset-left) - var(--safe-area-inset-right)
          );
          margin-left: var(--safe-area-inset-left);
          margin-right: var(--safe-area-inset-right);
          margin-inline-start: var(--safe-area-inset-left);
          margin-inline-end: var(--safe-area-inset-right);
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([narrow]) .content {
          height: calc(100% - var(--header-height));
          height: calc(
            100% - var(--header-height) - var(--safe-area-inset-bottom)
          );
        }

        :host([narrow]) .content.tabs {
          height: calc(100% - 2 * var(--header-height));
          height: calc(
            100% - 2 * var(--header-height) - var(--safe-area-inset-bottom)
          );
        }

        .content .fab-bottom-space {
          height: calc(64px + var(--safe-area-inset-bottom));
        }

        :host([narrow]) .content.tabs .fab-bottom-space {
          height: calc(80px + var(--safe-area-inset-bottom));
        }

        #fab {
          position: fixed;
          right: calc(16px + var(--safe-area-inset-right));
          inset-inline-end: calc(16px + var(--safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + var(--safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + var(--safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }

        .pane {
          border-right: 1px solid var(--divider-color);
          border-inline-end: 1px solid var(--divider-color);
          border-inline-start: initial;
          box-sizing: border-box;
          display: flex;
          flex: 0 0 var(--sidepane-width, 250px);
          width: var(--sidepane-width, 250px);
          flex-direction: column;
          position: relative;
        }
        .pane .ha-scrollbar {
          flex: 1;
        }
      `]}constructor(...t){super(...t),this.supervisor=!1,this.mainPage=!1,this.narrow=!1,this.isWide=!1,this.pane=!1,this.hasFab=!1,this._getTabs=(0,s.Z)(((t,o,e,a,r,n)=>{const s=t.filter((t=>((t,o)=>(p(o)||h(t,o))&&!b(t,o)&&d(t,o))(this.hass,t)));if(s.length<2){if(1===s.length){const t=s[0];return[t.translationKey?n(t.translationKey):t.name]}return[""]}return s.map((t=>i.dy`
          <a href=${t.path}>
            <ha-tab
              .hass=${this.hass}
              .active=${t.path===o?.path}
              .narrow=${this.narrow}
              .name=${t.translationKey?n(t.translationKey):t.name}
            >
              ${t.iconPath?i.dy`<ha-svg-icon
                    slot="icon"
                    .path=${t.iconPath}
                  ></ha-svg-icon>`:""}
            </ha-tab>
          </a>
        `))}))}}(0,a.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],x.prototype,"supervisor",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"localizeFunc",void 0),(0,a.__decorate)([(0,r.Cb)({type:String,attribute:"back-path"})],x.prototype,"backPath",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"backCallback",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,attribute:"main-page"})],x.prototype,"mainPage",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"route",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"tabs",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],x.prototype,"narrow",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0,attribute:"is-wide"})],x.prototype,"isWide",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],x.prototype,"pane",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,attribute:"has-fab"})],x.prototype,"hasFab",void 0),(0,a.__decorate)([(0,r.SB)()],x.prototype,"_activeTab",void 0),(0,a.__decorate)([(0,v.i)(".content")],x.prototype,"_savedScrollPos",void 0),(0,a.__decorate)([(0,r.hO)({passive:!0})],x.prototype,"_saveScrollPos",null),x=(0,a.__decorate)([(0,r.Mo)("hass-tabs-subpage")],x)},77204:function(t,o,e){e.d(o,{$c:()=>s,Qx:()=>r,k1:()=>i,yu:()=>n});var a=e(59048);const i=a.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
    outline: none;
  }
`,r=a.iv`
  :host {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-m);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-normal);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
    margin-inline-start: 20px;
    margin-inline-end: initial;
  }

  h1 {
    font-family: var(--ha-font-family-heading);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-2xl);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-condensed);
  }

  h2 {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: var(--ha-font-size-xl);
    font-weight: var(--ha-font-weight-medium);
    line-height: var(--ha-line-height-normal);
  }

  h3 {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-l);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-normal);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  ${i}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,n=a.iv`
  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - var(--safe-area-inset-right) - var(--safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - var(--safe-area-inset-right) - var(--safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: 0;
    }
  }
  .error {
    color: var(--error-color);
  }
`,s=a.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`;a.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`}};
//# sourceMappingURL=2998.51822e0ff55c2446.js.map