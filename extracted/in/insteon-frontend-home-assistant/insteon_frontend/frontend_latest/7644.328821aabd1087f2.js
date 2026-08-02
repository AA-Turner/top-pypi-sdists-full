/*! For license information please see 7644.328821aabd1087f2.js.LICENSE.txt */
export const __webpack_id__="7644";export const __webpack_ids__=["7644"];export const __webpack_modules__={53623:function(e,t,o){o.a(e,async function(e,i){try{o.r(t),o.d(t,{HaIconOverflowMenu:()=>c});var r=o(62826),n=o(96196),a=o(77845),s=o(94333),l=o(39396),d=(o(63419),o(60733),o(60961),o(88422)),h=(o(99892),o(32072),e([d]));d=(h.then?(await h)():h)[0];const p="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class c extends n.WF{render(){return 0===this.items.length?n.s6:n.qy`
      ${this.narrow?n.qy` <!-- Collapsed representation for small screens -->
            <ha-md-button-menu
              @click=${this._handleIconOverflowMenuOpened}
              positioning="popover"
            >
              <ha-icon-button
                .label=${this.hass.localize("ui.common.overflow_menu")}
                .path=${p}
                slot="trigger"
              ></ha-icon-button>

              ${this.items.map(e=>e.divider?n.qy`<ha-md-divider
                      role="separator"
                      tabindex="-1"
                    ></ha-md-divider>`:n.qy`<ha-md-menu-item
                      ?disabled=${e.disabled}
                      .clickAction=${e.action}
                      class=${(0,s.H)({warning:Boolean(e.warning)})}
                    >
                      <ha-svg-icon
                        slot="start"
                        class=${(0,s.H)({warning:Boolean(e.warning)})}
                        .path=${e.path}
                      ></ha-svg-icon>
                      ${e.label}
                    </ha-md-menu-item>`)}
            </ha-md-button-menu>`:n.qy`
            <!-- Icon representation for big screens -->
            ${this.items.map(e=>e.narrowOnly?n.s6:e.divider?n.qy`<div role="separator"></div>`:n.qy`<ha-tooltip
                        .disabled=${!e.tooltip}
                        .for="icon-button-${e.label}"
                        >${e.tooltip??""} </ha-tooltip
                      ><ha-icon-button
                        .id="icon-button-${e.label}"
                        @click=${e.action}
                        .label=${e.label}
                        .path=${e.path}
                        ?disabled=${e.disabled}
                      ></ha-icon-button> `)}
          `}
    `}_handleIconOverflowMenuOpened(e){e.stopPropagation()}static get styles(){return[l.RF,n.AH`
        :host {
          display: flex;
          justify-content: flex-end;
          cursor: initial;
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
      `]}constructor(...e){super(...e),this.items=[],this.narrow=!1}}(0,r.__decorate)([(0,a.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,r.__decorate)([(0,a.MZ)({type:Array})],c.prototype,"items",void 0),(0,r.__decorate)([(0,a.MZ)({type:Boolean})],c.prototype,"narrow",void 0),c=(0,r.__decorate)([(0,a.EM)("ha-icon-overflow-menu")],c),i()}catch(p){i(p)}})},63419:function(e,t,o){var i=o(62826),r=o(96196),n=o(77845),a=o(92542),s=(o(41742),o(26139)),l=o(8889),d=o(63374);class h extends s.W1{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(e){e.detail.reason.kind===d.fi.KEYDOWN&&e.detail.reason.key===d.NV.ESCAPE||e.detail.initiator.clickAction?.(e.detail.initiator)}}h.styles=[l.R,r.AH`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `],h=(0,i.__decorate)([(0,n.EM)("ha-md-menu")],h);class p extends r.WF{get items(){return this._menu.items}focus(){this._menu.open?this._menu.focus():this._triggerButton?.focus()}render(){return r.qy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <ha-md-menu
        .quick=${this.quick}
        .positioning=${this.positioning}
        .hasOverflow=${this.hasOverflow}
        .anchorCorner=${this.anchorCorner}
        .menuCorner=${this.menuCorner}
        @opening=${this._handleOpening}
        @closing=${this._handleClosing}
      >
        <slot></slot>
      </ha-md-menu>
    `}_handleOpening(){(0,a.r)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,a.r)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...e){super(...e),this.disabled=!1,this.anchorCorner="end-start",this.menuCorner="start-start",this.hasOverflow=!1,this.quick=!1}}p.styles=r.AH`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `,(0,i.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,i.__decorate)([(0,n.MZ)()],p.prototype,"positioning",void 0),(0,i.__decorate)([(0,n.MZ)({attribute:"anchor-corner"})],p.prototype,"anchorCorner",void 0),(0,i.__decorate)([(0,n.MZ)({attribute:"menu-corner"})],p.prototype,"menuCorner",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean,attribute:"has-overflow"})],p.prototype,"hasOverflow",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"quick",void 0),(0,i.__decorate)([(0,n.P)("ha-md-menu",!0)],p.prototype,"_menu",void 0),p=(0,i.__decorate)([(0,n.EM)("ha-md-button-menu")],p)},32072:function(e,t,o){var i=o(62826),r=o(10414),n=o(18989),a=o(96196),s=o(77845);class l extends r.c{}l.styles=[n.R,a.AH`
      :host {
        --md-divider-color: var(--divider-color);
      }
    `],l=(0,i.__decorate)([(0,s.EM)("ha-md-divider")],l)},99892:function(e,t,o){var i=o(62826),r=o(54407),n=o(28522),a=o(96196),s=o(77845);class l extends r.K{}l.styles=[n.R,a.AH`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);
        --md-sys-color-secondary-container: rgba(
          var(--rgb-primary-color),
          0.15
        );
        --md-sys-color-on-secondary-container: var(--text-primary-color);
        --mdc-icon-size: 16px;

        --md-sys-color-on-primary-container: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-menu-item-label-text-font: Roboto, sans-serif;
      }
      :host(.warning) {
        --md-menu-item-label-text-color: var(--error-color);
        --md-menu-item-leading-icon-color: var(--error-color);
      }
      ::slotted([slot="headline"]) {
        text-wrap: nowrap;
      }
      :host([disabled]) {
        opacity: 1;
        --md-menu-item-label-text-color: var(--disabled-text-color);
        --md-menu-item-leading-icon-color: var(--disabled-text-color);
      }
    `],(0,i.__decorate)([(0,s.MZ)({attribute:!1})],l.prototype,"clickAction",void 0),l=(0,i.__decorate)([(0,s.EM)("ha-md-menu-item")],l)},88422:function(e,t,o){o.a(e,async function(e,t){try{var i=o(62826),r=o(52630),n=o(96196),a=o(77845),s=e([r]);r=(s.then?(await s)():s)[0];class l extends r.A{static get styles(){return[r.A.styles,n.AH`
        :host {
          --wa-tooltip-background-color: var(--secondary-background-color);
          --wa-tooltip-content-color: var(--primary-text-color);
          --wa-tooltip-font-family: var(
            --ha-tooltip-font-family,
            var(--ha-font-family-body)
          );
          --wa-tooltip-font-size: var(
            --ha-tooltip-font-size,
            var(--ha-font-size-s)
          );
          --wa-tooltip-font-weight: var(
            --ha-tooltip-font-weight,
            var(--ha-font-weight-normal)
          );
          --wa-tooltip-line-height: var(
            --ha-tooltip-line-height,
            var(--ha-line-height-condensed)
          );
          --wa-tooltip-padding: 8px;
          --wa-tooltip-border-radius: var(
            --ha-tooltip-border-radius,
            var(--ha-border-radius-sm)
          );
          --wa-tooltip-arrow-size: var(--ha-tooltip-arrow-size, 8px);
          --wa-z-index-tooltip: var(--ha-tooltip-z-index, 1000);
        }
      `]}constructor(...e){super(...e),this.showDelay=150,this.hideDelay=150}}(0,i.__decorate)([(0,a.MZ)({attribute:"show-delay",type:Number})],l.prototype,"showDelay",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"hide-delay",type:Number})],l.prototype,"hideDelay",void 0),l=(0,i.__decorate)([(0,a.EM)("ha-tooltip")],l),t()}catch(l){t(l)}})},61171:function(e,t,o){o.d(t,{A:()=>i});const i=o(96196).AH`:host {
  --max-width: 30ch;
  display: inline-block;
  position: absolute;
  color: var(--wa-tooltip-content-color);
  font-size: var(--wa-tooltip-font-size);
  line-height: var(--wa-tooltip-line-height);
  text-align: start;
  white-space: normal;
}
.tooltip {
  --arrow-size: var(--wa-tooltip-arrow-size);
  --arrow-color: var(--wa-tooltip-background-color);
}
.tooltip::part(popup) {
  z-index: 1000;
}
.tooltip[placement^=top]::part(popup) {
  transform-origin: bottom;
}
.tooltip[placement^=bottom]::part(popup) {
  transform-origin: top;
}
.tooltip[placement^=left]::part(popup) {
  transform-origin: right;
}
.tooltip[placement^=right]::part(popup) {
  transform-origin: left;
}
.body {
  display: block;
  width: max-content;
  max-width: var(--max-width);
  border-radius: var(--wa-tooltip-border-radius);
  background-color: var(--wa-tooltip-background-color);
  border: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
  padding: 0.25em 0.5em;
  user-select: none;
  -webkit-user-select: none;
}
.tooltip::part(arrow) {
  border-bottom: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
  border-right: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
}
`},52630:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{A:()=>_});var r=o(96196),n=o(77845),a=o(94333),s=o(17051),l=o(42462),d=o(28438),h=o(98779),p=o(27259),c=o(984),m=o(53720),u=o(9395),y=o(32510),v=o(40158),g=o(61171),b=e([v]);v=(b.then?(await b)():b)[0];var f=Object.defineProperty,w=Object.getOwnPropertyDescriptor,x=(e,t,o,i)=>{for(var r,n=i>1?void 0:i?w(t,o):t,a=e.length-1;a>=0;a--)(r=e[a])&&(n=(i?r(t,o,n):r(n))||n);return i&&n&&f(t,o,n),n};let _=class extends y.A{connectedCallback(){super.connectedCallback(),this.eventController.signal.aborted&&(this.eventController=new AbortController),this.open&&(this.open=!1,this.updateComplete.then(()=>{this.open=!0})),this.id||(this.id=(0,m.N)("wa-tooltip-")),this.for&&this.anchor?(this.anchor=null,this.handleForChange()):this.for&&this.handleForChange()}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("keydown",this.handleDocumentKeyDown),this.eventController.abort(),this.anchor&&this.removeFromAriaLabelledBy(this.anchor,this.id)}firstUpdated(){this.body.hidden=!this.open,this.open&&(this.popup.active=!0,this.popup.reposition())}hasTrigger(e){return this.trigger.split(" ").includes(e)}addToAriaLabelledBy(e,t){const o=(e.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean);o.includes(t)||(o.push(t),e.setAttribute("aria-labelledby",o.join(" ")))}removeFromAriaLabelledBy(e,t){const o=(e.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean).filter(e=>e!==t);o.length>0?e.setAttribute("aria-labelledby",o.join(" ")):e.removeAttribute("aria-labelledby")}async handleOpenChange(){if(this.open){if(this.disabled)return;const e=new h.k;if(this.dispatchEvent(e),e.defaultPrevented)return void(this.open=!1);document.addEventListener("keydown",this.handleDocumentKeyDown,{signal:this.eventController.signal}),this.body.hidden=!1,this.popup.active=!0,await(0,p.Ud)(this.popup.popup,"show-with-scale"),this.popup.reposition(),this.dispatchEvent(new l.q)}else{const e=new d.L;if(this.dispatchEvent(e),e.defaultPrevented)return void(this.open=!1);document.removeEventListener("keydown",this.handleDocumentKeyDown),await(0,p.Ud)(this.popup.popup,"hide-with-scale"),this.popup.active=!1,this.body.hidden=!0,this.dispatchEvent(new s.Z)}}handleForChange(){const e=this.getRootNode();if(!e)return;const t=this.for?e.getElementById(this.for):null,o=this.anchor;if(t===o)return;const{signal:i}=this.eventController;t&&(this.addToAriaLabelledBy(t,this.id),t.addEventListener("blur",this.handleBlur,{capture:!0,signal:i}),t.addEventListener("focus",this.handleFocus,{capture:!0,signal:i}),t.addEventListener("click",this.handleClick,{signal:i}),t.addEventListener("mouseover",this.handleMouseOver,{signal:i}),t.addEventListener("mouseout",this.handleMouseOut,{signal:i})),o&&(this.removeFromAriaLabelledBy(o,this.id),o.removeEventListener("blur",this.handleBlur,{capture:!0}),o.removeEventListener("focus",this.handleFocus,{capture:!0}),o.removeEventListener("click",this.handleClick),o.removeEventListener("mouseover",this.handleMouseOver),o.removeEventListener("mouseout",this.handleMouseOut)),this.anchor=t}async handleOptionsChange(){this.hasUpdated&&(await this.updateComplete,this.popup.reposition())}handleDisabledChange(){this.disabled&&this.open&&this.hide()}async show(){if(!this.open)return this.open=!0,(0,c.l)(this,"wa-after-show")}async hide(){if(this.open)return this.open=!1,(0,c.l)(this,"wa-after-hide")}render(){return r.qy`
      <wa-popup
        part="base"
        exportparts="
          popup:base__popup,
          arrow:base__arrow
        "
        class=${(0,a.H)({tooltip:!0,"tooltip-open":this.open})}
        placement=${this.placement}
        distance=${this.distance}
        skidding=${this.skidding}
        flip
        shift
        ?arrow=${!this.withoutArrow}
        hover-bridge
        .anchor=${this.anchor}
      >
        <div part="body" class="body">
          <slot></slot>
        </div>
      </wa-popup>
    `}constructor(){super(...arguments),this.placement="top",this.disabled=!1,this.distance=8,this.open=!1,this.skidding=0,this.showDelay=150,this.hideDelay=0,this.trigger="hover focus",this.withoutArrow=!1,this.for=null,this.anchor=null,this.eventController=new AbortController,this.handleBlur=()=>{this.hasTrigger("focus")&&this.hide()},this.handleClick=()=>{this.hasTrigger("click")&&(this.open?this.hide():this.show())},this.handleFocus=()=>{this.hasTrigger("focus")&&this.show()},this.handleDocumentKeyDown=e=>{"Escape"===e.key&&(e.stopPropagation(),this.hide())},this.handleMouseOver=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.show(),this.showDelay))},this.handleMouseOut=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.hide(),this.hideDelay))}}};_.css=g.A,_.dependencies={"wa-popup":v.A},x([(0,n.P)("slot:not([name])")],_.prototype,"defaultSlot",2),x([(0,n.P)(".body")],_.prototype,"body",2),x([(0,n.P)("wa-popup")],_.prototype,"popup",2),x([(0,n.MZ)()],_.prototype,"placement",2),x([(0,n.MZ)({type:Boolean,reflect:!0})],_.prototype,"disabled",2),x([(0,n.MZ)({type:Number})],_.prototype,"distance",2),x([(0,n.MZ)({type:Boolean,reflect:!0})],_.prototype,"open",2),x([(0,n.MZ)({type:Number})],_.prototype,"skidding",2),x([(0,n.MZ)({attribute:"show-delay",type:Number})],_.prototype,"showDelay",2),x([(0,n.MZ)({attribute:"hide-delay",type:Number})],_.prototype,"hideDelay",2),x([(0,n.MZ)()],_.prototype,"trigger",2),x([(0,n.MZ)({attribute:"without-arrow",type:Boolean,reflect:!0})],_.prototype,"withoutArrow",2),x([(0,n.MZ)()],_.prototype,"for",2),x([(0,n.wk)()],_.prototype,"anchor",2),x([(0,u.w)("open",{waitUntilFirstUpdate:!0})],_.prototype,"handleOpenChange",1),x([(0,u.w)("for")],_.prototype,"handleForChange",1),x([(0,u.w)(["distance","placement","skidding"])],_.prototype,"handleOptionsChange",1),x([(0,u.w)("disabled")],_.prototype,"handleDisabledChange",1),_=x([(0,n.EM)("wa-tooltip")],_),i()}catch(_){i(_)}})},18989:function(e,t,o){o.d(t,{R:()=>i});const i=o(96196).AH`:host{box-sizing:border-box;color:var(--md-divider-color, var(--md-sys-color-outline-variant, #cac4d0));display:flex;height:var(--md-divider-thickness, 1px);width:100%}:host([inset]),:host([inset-start]){padding-inline-start:16px}:host([inset]),:host([inset-end]){padding-inline-end:16px}:host::before{background:currentColor;content:"";height:100%;width:100%}@media(forced-colors: active){:host::before{background:CanvasText}}
`},10414:function(e,t,o){o.d(t,{c:()=>a});var i=o(62826),r=o(96196),n=o(77845);class a extends r.WF{constructor(){super(...arguments),this.inset=!1,this.insetStart=!1,this.insetEnd=!1}}(0,i.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0})],a.prototype,"inset",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"inset-start"})],a.prototype,"insetStart",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"inset-end"})],a.prototype,"insetEnd",void 0)},58791:function(e,t,o){o.d(t,{X:()=>r});var i=o(63374);class r{get typeaheadText(){if(null!==this.internalTypeaheadText)return this.internalTypeaheadText;const e=this.getHeadlineElements(),t=[];return e.forEach(e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())}),0===t.length&&this.getDefaultElements().forEach(e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())}),0===t.length&&this.getSupportingTextElements().forEach(e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())}),t.join(" ")}get tagName(){switch(this.host.type){case"link":return"a";case"button":return"button";default:return"li"}}get role(){return"option"===this.host.type?"option":"menuitem"}hostConnected(){this.host.toggleAttribute("md-menu-item",!0)}hostUpdate(){this.host.href&&(this.host.type="link")}setTypeaheadText(e){this.internalTypeaheadText=e}constructor(e,t){this.host=e,this.internalTypeaheadText=null,this.onClick=()=>{this.host.keepOpen||this.host.dispatchEvent((0,i.xr)(this.host,{kind:i.fi.CLICK_SELECTION}))},this.onKeydown=e=>{if(this.host.href&&"Enter"===e.code){const e=this.getInteractiveElement();e instanceof HTMLAnchorElement&&e.click()}if(e.defaultPrevented)return;const t=e.code;this.host.keepOpen&&"Escape"!==t||(0,i.Rb)(t)&&(e.preventDefault(),this.host.dispatchEvent((0,i.xr)(this.host,{kind:i.fi.KEYDOWN,key:t})))},this.getHeadlineElements=t.getHeadlineElements,this.getSupportingTextElements=t.getSupportingTextElements,this.getDefaultElements=t.getDefaultElements,this.getInteractiveElement=t.getInteractiveElement,this.host.addController(this)}}},28522:function(e,t,o){o.d(t,{R:()=>i});const i=o(96196).AH`:host{display:flex;--md-ripple-hover-color: var(--md-menu-item-hover-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-hover-opacity: var(--md-menu-item-hover-state-layer-opacity, 0.08);--md-ripple-pressed-color: var(--md-menu-item-pressed-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-pressed-opacity: var(--md-menu-item-pressed-state-layer-opacity, 0.12)}:host([disabled]){opacity:var(--md-menu-item-disabled-opacity, 0.3);pointer-events:none}md-focus-ring{z-index:1;--md-focus-ring-shape: 8px}a,button,li{background:none;border:none;padding:0;margin:0;text-align:unset;text-decoration:none}.list-item{border-radius:inherit;display:flex;flex:1;max-width:inherit;min-width:inherit;outline:none;-webkit-tap-highlight-color:rgba(0,0,0,0)}.list-item:not(.disabled){cursor:pointer}[slot=container]{pointer-events:none}md-ripple{border-radius:inherit}md-item{border-radius:inherit;flex:1;color:var(--md-menu-item-label-text-color, var(--md-sys-color-on-surface, #1d1b20));font-family:var(--md-menu-item-label-text-font, var(--md-sys-typescale-body-large-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-label-text-size, var(--md-sys-typescale-body-large-size, 1rem));line-height:var(--md-menu-item-label-text-line-height, var(--md-sys-typescale-body-large-line-height, 1.5rem));font-weight:var(--md-menu-item-label-text-weight, var(--md-sys-typescale-body-large-weight, var(--md-ref-typeface-weight-regular, 400)));min-height:var(--md-menu-item-one-line-container-height, 56px);padding-top:var(--md-menu-item-top-space, 12px);padding-bottom:var(--md-menu-item-bottom-space, 12px);padding-inline-start:var(--md-menu-item-leading-space, 16px);padding-inline-end:var(--md-menu-item-trailing-space, 16px)}md-item[multiline]{min-height:var(--md-menu-item-two-line-container-height, 72px)}[slot=supporting-text]{color:var(--md-menu-item-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-supporting-text-font, var(--md-sys-typescale-body-medium-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-supporting-text-size, var(--md-sys-typescale-body-medium-size, 0.875rem));line-height:var(--md-menu-item-supporting-text-line-height, var(--md-sys-typescale-body-medium-line-height, 1.25rem));font-weight:var(--md-menu-item-supporting-text-weight, var(--md-sys-typescale-body-medium-weight, var(--md-ref-typeface-weight-regular, 400)))}[slot=trailing-supporting-text]{color:var(--md-menu-item-trailing-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-trailing-supporting-text-font, var(--md-sys-typescale-label-small-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-trailing-supporting-text-size, var(--md-sys-typescale-label-small-size, 0.6875rem));line-height:var(--md-menu-item-trailing-supporting-text-line-height, var(--md-sys-typescale-label-small-line-height, 1rem));font-weight:var(--md-menu-item-trailing-supporting-text-weight, var(--md-sys-typescale-label-small-weight, var(--md-ref-typeface-weight-medium, 500)))}:is([slot=start],[slot=end])::slotted(*){fill:currentColor}[slot=start]{color:var(--md-menu-item-leading-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}[slot=end]{color:var(--md-menu-item-trailing-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}.list-item{background-color:var(--md-menu-item-container-color, transparent)}.list-item.selected{background-color:var(--md-menu-item-selected-container-color, var(--md-sys-color-secondary-container, #e8def8))}.selected:not(.disabled) ::slotted(*){color:var(--md-menu-item-selected-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b))}@media(forced-colors: active){:host([disabled]),:host([disabled]) slot{color:GrayText;opacity:1}.list-item{position:relative}.list-item.selected::before{content:"";position:absolute;inset:0;box-sizing:border-box;border-radius:inherit;pointer-events:none;border:3px double CanvasText}}
`},54407:function(e,t,o){o.d(t,{K:()=>p});var i=o(62826),r=(o(4469),o(20903),o(71970),o(96196)),n=o(77845),a=o(94333),s=o(28345),l=o(20618),d=o(58791);const h=(0,l.n)(r.WF);class p extends h{get typeaheadText(){return this.menuItemController.typeaheadText}set typeaheadText(e){this.menuItemController.setTypeaheadText(e)}render(){return this.renderListItem(r.qy`
      <md-item>
        <div slot="container">
          ${this.renderRipple()} ${this.renderFocusRing()}
        </div>
        <slot name="start" slot="start"></slot>
        <slot name="end" slot="end"></slot>
        ${this.renderBody()}
      </md-item>
    `)}renderListItem(e){const t="link"===this.type;let o;switch(this.menuItemController.tagName){case"a":o=s.eu`a`;break;case"button":o=s.eu`button`;break;default:o=s.eu`li`}const i=t&&this.target?this.target:r.s6;return s.qy`
      <${o}
        id="item"
        tabindex=${this.disabled&&!t?-1:0}
        role=${this.menuItemController.role}
        aria-label=${this.ariaLabel||r.s6}
        aria-selected=${this.ariaSelected||r.s6}
        aria-checked=${this.ariaChecked||r.s6}
        aria-expanded=${this.ariaExpanded||r.s6}
        aria-haspopup=${this.ariaHasPopup||r.s6}
        class="list-item ${(0,a.H)(this.getRenderClasses())}"
        href=${this.href||r.s6}
        target=${i}
        @click=${this.menuItemController.onClick}
        @keydown=${this.menuItemController.onKeydown}
      >${e}</${o}>
    `}renderRipple(){return r.qy` <md-ripple
      part="ripple"
      for="item"
      ?disabled=${this.disabled}></md-ripple>`}renderFocusRing(){return r.qy` <md-focus-ring
      part="focus-ring"
      for="item"
      inward></md-focus-ring>`}getRenderClasses(){return{disabled:this.disabled,selected:this.selected}}renderBody(){return r.qy`
      <slot></slot>
      <slot name="overline" slot="overline"></slot>
      <slot name="headline" slot="headline"></slot>
      <slot name="supporting-text" slot="supporting-text"></slot>
      <slot
        name="trailing-supporting-text"
        slot="trailing-supporting-text"></slot>
    `}focus(){this.listItemRoot?.focus()}constructor(){super(...arguments),this.disabled=!1,this.type="menuitem",this.href="",this.target="",this.keepOpen=!1,this.selected=!1,this.menuItemController=new d.X(this,{getHeadlineElements:()=>this.headlineElements,getSupportingTextElements:()=>this.supportingTextElements,getDefaultElements:()=>this.defaultElements,getInteractiveElement:()=>this.listItemRoot})}}p.shadowRootOptions={...r.WF.shadowRootOptions,delegatesFocus:!0},(0,i.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,i.__decorate)([(0,n.MZ)()],p.prototype,"type",void 0),(0,i.__decorate)([(0,n.MZ)()],p.prototype,"href",void 0),(0,i.__decorate)([(0,n.MZ)()],p.prototype,"target",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean,attribute:"keep-open"})],p.prototype,"keepOpen",void 0),(0,i.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"selected",void 0),(0,i.__decorate)([(0,n.P)(".list-item")],p.prototype,"listItemRoot",void 0),(0,i.__decorate)([(0,n.KN)({slot:"headline"})],p.prototype,"headlineElements",void 0),(0,i.__decorate)([(0,n.KN)({slot:"supporting-text"})],p.prototype,"supportingTextElements",void 0),(0,i.__decorate)([(0,n.gZ)({slot:""})],p.prototype,"defaultElements",void 0),(0,i.__decorate)([(0,n.MZ)({attribute:"typeahead-text"})],p.prototype,"typeaheadText",null)}};
//# sourceMappingURL=7644.328821aabd1087f2.js.map