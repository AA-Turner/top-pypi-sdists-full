export const __webpack_ids__=["9005"];export const __webpack_modules__={22543:function(t,e,o){o.r(e);var i=o(73742),r=o(59048),a=o(7616),n=o(31733),l=o(29740);o(78645),o(40830);const s={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class d extends r.oi{render(){return r.dy`
      <div
        class="issue-type ${(0,n.$)({[this.alertType]:!0})}"
        role="alert"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <slot name="icon">
            <ha-svg-icon .path=${s[this.alertType]}></ha-svg-icon>
          </slot>
        </div>
        <div class=${(0,n.$)({content:!0,narrow:this.narrow})}>
          <div class="main-content">
            ${this.title?r.dy`<div class="title">${this.title}</div>`:r.Ld}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${this.dismissable?r.dy`<ha-icon-button
                    @click=${this._dismissClicked}
                    label="Dismiss alert"
                    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  ></ha-icon-button>`:r.Ld}
            </slot>
          </div>
        </div>
      </div>
    `}_dismissClicked(){(0,l.B)(this,"alert-dismissed-clicked")}constructor(...t){super(...t),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}d.styles=r.iv`
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
  `,(0,i.__decorate)([(0,a.Cb)()],d.prototype,"title",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:"alert-type"})],d.prototype,"alertType",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean})],d.prototype,"dismissable",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean})],d.prototype,"narrow",void 0),d=(0,i.__decorate)([(0,a.Mo)("ha-alert")],d)},30337:function(t,e,o){o.a(t,(async function(t,e){try{o(11807);var i=o(73742),r=o(71328),a=o(59048),n=o(7616),l=o(63871),s=t([r]);r=(s.then?(await s)():s)[0];class d extends r.Z{attachInternals(){const t=super.attachInternals();return Object.defineProperty(t,"states",{value:new l.C(this,t.states)}),t}static get styles(){return[r.Z.styles,a.iv`
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
      `]}constructor(...t){super(...t),this.variant="brand"}}d=(0,i.__decorate)([(0,n.Mo)("ha-button")],d),e()}catch(d){e(d)}}))},86932:function(t,e,o){o.d(e,{G:()=>d});var i=o(73742),r=o(59048),a=o(7616),n=o(31733),l=o(29740),s=o(98012);o(40830);class d extends r.oi{render(){const t=this.noCollapse?r.Ld:r.dy`
          <ha-svg-icon
            .path=${"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}
            class="summary-icon ${(0,n.$)({expanded:this.expanded})}"
          ></ha-svg-icon>
        `;return r.dy`
      <div class="top ${(0,n.$)({expanded:this.expanded})}">
        <div
          id="summary"
          class=${(0,n.$)({noCollapse:this.noCollapse})}
          @click=${this._toggleContainer}
          @keydown=${this._toggleContainer}
          @focus=${this._focusChanged}
          @blur=${this._focusChanged}
          role="button"
          tabindex=${this.noCollapse?-1:0}
          aria-expanded=${this.expanded}
          aria-controls="sect1"
        >
          ${this.leftChevron?t:r.Ld}
          <slot name="leading-icon"></slot>
          <slot name="header">
            <div class="header">
              ${this.header}
              <slot class="secondary" name="secondary">${this.secondary}</slot>
            </div>
          </slot>
          ${this.leftChevron?r.Ld:t}
          <slot name="icons"></slot>
        </div>
      </div>
      <div
        class="container ${(0,n.$)({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?r.dy`<slot></slot>`:""}
      </div>
    `}willUpdate(t){super.willUpdate(t),t.has("expanded")&&(this._showContent=this.expanded,setTimeout((()=>{this._container.style.overflow=this.expanded?"initial":"hidden"}),300))}_handleTransitionEnd(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}async _toggleContainer(t){if(t.defaultPrevented)return;if("keydown"===t.type&&"Enter"!==t.key&&" "!==t.key)return;if(t.preventDefault(),this.noCollapse)return;const e=!this.expanded;(0,l.B)(this,"expanded-will-change",{expanded:e}),this._container.style.overflow="hidden",e&&(this._showContent=!0,await(0,s.y)());const o=this._container.scrollHeight;this._container.style.height=`${o}px`,e||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=e,(0,l.B)(this,"expanded-changed",{expanded:this.expanded})}_focusChanged(t){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===t.type)}constructor(...t){super(...t),this.expanded=!1,this.outlined=!1,this.leftChevron=!1,this.noCollapse=!1,this._showContent=this.expanded}}d.styles=r.iv`
    :host {
      display: block;
    }

    .top {
      display: flex;
      align-items: center;
      border-radius: var(--ha-card-border-radius, 12px);
    }

    .top.expanded {
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }

    .top.focused {
      background: var(--input-fill-color);
    }

    :host([outlined]) {
      box-shadow: none;
      border-width: 1px;
      border-style: solid;
      border-color: var(--outline-color);
      border-radius: var(--ha-card-border-radius, 12px);
    }

    .summary-icon {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      direction: var(--direction);
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
    }

    :host([left-chevron]) .summary-icon,
    ::slotted([slot="leading-icon"]) {
      margin-left: 0;
      margin-right: 8px;
      margin-inline-start: 0;
      margin-inline-end: 8px;
    }

    #summary {
      flex: 1;
      display: flex;
      padding: var(--expansion-panel-summary-padding, 0 8px);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: var(--ha-font-weight-medium);
      outline: none;
    }
    #summary.noCollapse {
      cursor: default;
    }

    .summary-icon.expanded {
      transform: rotate(180deg);
    }

    .header,
    ::slotted([slot="header"]) {
      flex: 1;
      overflow-wrap: anywhere;
    }

    .container {
      padding: var(--expansion-panel-content-padding, 0 8px);
      overflow: hidden;
      transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
    }

    .container.expanded {
      height: auto;
    }

    .secondary {
      display: block;
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
    }
  `,(0,i.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],d.prototype,"expanded",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],d.prototype,"outlined",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:"left-chevron",type:Boolean,reflect:!0})],d.prototype,"leftChevron",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:"no-collapse",type:Boolean,reflect:!0})],d.prototype,"noCollapse",void 0),(0,i.__decorate)([(0,a.Cb)()],d.prototype,"header",void 0),(0,i.__decorate)([(0,a.Cb)()],d.prototype,"secondary",void 0),(0,i.__decorate)([(0,a.SB)()],d.prototype,"_showContent",void 0),(0,i.__decorate)([(0,a.IO)(".container")],d.prototype,"_container",void 0),d=(0,i.__decorate)([(0,a.Mo)("ha-expansion-panel")],d)},93795:function(t,e,o){var i=o(73742),r=o(84859),a=o(7686),n=o(59048),l=o(7616);class s extends r.K{renderRipple(){return this.noninteractive?"":super.renderRipple()}static get styles(){return[a.W,n.iv`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `,"rtl"===document.dir?n.iv`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `:n.iv``]}}s=(0,i.__decorate)([(0,l.Mo)("ha-list-item")],s)},39651:function(t,e,o){var i=o(73742),r=o(92560),a=o(84862),n=o(7616);class l extends r.Kh{}l.styles=a.W,l=(0,i.__decorate)([(0,n.Mo)("ha-list")],l)},59462:function(t,e,o){var i=o(73742),r=o(69287),a=o(70840),n=o(59048),l=o(7616),s=o(31733);o(39651);class d extends r.HB{get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("ha-list")),this.listElement_}renderList(){const t="menu"===this.innerRole?"menuitem":"option",e=this.renderListClasses();return n.dy`<ha-list
      rootTabbable
      .innerAriaLabel=${this.innerAriaLabel}
      .innerRole=${this.innerRole}
      .multi=${this.multi}
      class=${(0,s.$)(e)}
      .itemRoles=${t}
      .wrapFocus=${this.wrapFocus}
      .activatable=${this.activatable}
      @action=${this.onAction}
    >
      <slot></slot>
    </ha-list>`}}d.styles=a.W,d=(0,i.__decorate)([(0,l.Mo)("ha-menu")],d)},4820:function(t,e,o){var i=o(73742),r=o(1516),a=o(82028),n=o(59048),l=o(7616),s=o(19408);class d extends r.H{firstUpdated(){super.firstUpdated(),this.addEventListener("change",(()=>{this.haptic&&(0,s.j)("light")}))}constructor(...t){super(...t),this.haptic=!1}}d.styles=[a.W,n.iv`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `],(0,i.__decorate)([(0,l.Cb)({type:Boolean})],d.prototype,"haptic",void 0),d=(0,i.__decorate)([(0,l.Mo)("ha-switch")],d)},19408:function(t,e,o){o.d(e,{j:()=>r});var i=o(29740);const r=t=>{(0,i.B)(window,"haptic",t)}},63871:function(t,e,o){o.d(e,{C:()=>i});class i extends Set{add(t){super.add(t);const e=this._existing;if(e)try{e.add(t)}catch{e.add(`--${t}`)}else this._el.setAttribute(`state-${t}`,"");return this}delete(t){super.delete(t);const e=this._existing;return e?(e.delete(t),e.delete(`--${t}`)):this._el.removeAttribute(`state-${t}`),!0}has(t){return super.has(t)}clear(){for(const t of this)this.delete(t)}constructor(t,e=null){super(),this._existing=null,this._el=t,this._existing=e}}const r=CSSStyleSheet.prototype.replaceSync;Object.defineProperty(CSSStyleSheet.prototype,"replaceSync",{value:function(t){t=t.replace(/:state\(([^)]+)\)/g,":where(:state($1), :--$1, [state-$1])"),r.call(this,t)}})},65793:function(t,e,o){o.d(e,{Am:()=>s,Wl:()=>a,Yh:()=>n,f3:()=>r,jQ:()=>g,q$:()=>l,tu:()=>v});var i=o(24110);const r={payload:t=>null==t.payload?"":Array.isArray(t.payload)?t.payload.reduce(((t,e)=>t+e.toString(16).padStart(2,"0")),"0x"):t.payload.toString(),valueWithUnit:t=>null==t.value?"":"number"==typeof t.value||"boolean"==typeof t.value||"string"==typeof t.value?t.value.toString()+(t.unit?" "+t.unit:""):(0,i.$w)(t.value),timeWithMilliseconds:t=>new Date(t.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:t=>new Date(t.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:t=>null==t.dpt_main?"":null==t.dpt_sub?t.dpt_main.toString():t.dpt_main.toString()+"."+t.dpt_sub.toString().padStart(3,"0"),dptNameNumber:t=>{const e=r.dptNumber(t);return null==t.dpt_name?`DPT ${e}`:e?`DPT ${e} ${t.dpt_name}`:t.dpt_name}},a=t=>null==t?"":t.main+(t.sub?"."+t.sub.toString().padStart(3,"0"):""),n=t=>t.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),l=t=>t.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+t.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),s=t=>{const e=new Date(t),o=t.match(/\.(\d{6})/),i=o?o[1]:"000000";return e.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+e.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit"})+"."+i},d=1e3,c=1e3,h=60*c,p=60*h,u=2,m=3;function v(t){const e=t.indexOf(".");if(-1===e)return 1e3*Date.parse(t);let o=t.indexOf("Z",e);-1===o&&(o=t.indexOf("+",e),-1===o&&(o=t.indexOf("-",e))),-1===o&&(o=t.length);const i=t.slice(0,e)+t.slice(o),r=Date.parse(i);let a=t.slice(e+1,o);return a.length<6?a=a.padEnd(6,"0"):a.length>6&&(a=a.slice(0,6)),1e3*r+Number(a)}function g(t,e="milliseconds"){if(null==t)return"—";const o=t<0?"-":"",i=Math.abs(t),r="milliseconds"===e?Math.round(i/d):Math.floor(i/d),a="microseconds"===e?i%d:0,n=Math.floor(r/p),l=Math.floor(r%p/h),s=Math.floor(r%h/c),v=r%c,g=t=>t.toString().padStart(u,"0"),f=t=>t.toString().padStart(m,"0"),b="microseconds"===e?`.${f(v)}${f(a)}`:`.${f(v)}`,y=`${g(l)}:${g(s)}`;return`${o}${n>0?`${g(n)}:${y}`:y}${b}`}}};
//# sourceMappingURL=9005.cd89bf94ea2bc467.js.map