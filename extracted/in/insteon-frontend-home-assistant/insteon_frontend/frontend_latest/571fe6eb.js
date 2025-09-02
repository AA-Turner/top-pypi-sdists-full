/*! For license information please see 571fe6eb.js.LICENSE.txt */
"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[5297,5334,6609],{14114:(e,t,i)=>{i.d(t,{P:()=>n});const n=e=>(t,i)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,i)=>t.constructor._observers.set(i,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const i=this.constructor._observers.get(t);void 0!==i&&i.call(this,this[t],e)}))}}t.constructor._observers.set(i,e)}},61092:(e,t,i)=>{i.d(t,{K:()=>c});var n=i(43204),s=(i(91156),i(14114)),r=i(98734),o=i(9644),a=i(36924),l=i(8636);class c extends o.oi{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new r.A((()=>(this.shouldRenderRipple=!0,this.ripple))),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:e=>{const t=e.type;this.onDown("mousedown"===t?"mouseup":"touchend",e)}}]}get text(){const e=this.textContent;return e?e.trim():""}render(){const e=this.renderText(),t=this.graphic?this.renderGraphic():o.dy``,i=this.hasMeta?this.renderMeta():o.dy``;return o.dy`
      ${this.renderRipple()}
      ${t}
      ${e}
      ${i}`}renderRipple(){return this.shouldRenderRipple?o.dy`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?o.dy`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const e={multi:this.multipleGraphics};return o.dy`
      <span class="mdc-deprecated-list-item__graphic material-icons ${(0,l.$)(e)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return o.dy`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const e=this.twoline?this.renderTwoline():this.renderSingleLine();return o.dy`
      <span class="mdc-deprecated-list-item__text">
        ${e}
      </span>`}renderSingleLine(){return o.dy`<slot></slot>`}renderTwoline(){return o.dy`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(e,t){const i=()=>{window.removeEventListener(e,i),this.rippleHandlers.endPress()};window.addEventListener(e,i),this.rippleHandlers.startPress(t)}fireRequestSelected(e,t){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:t,selected:e}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const e of this.listeners)for(const t of e.eventNames)e.target.addEventListener(t,e.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const e of this.listeners)for(const t of e.eventNames)e.target.removeEventListener(t,e.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const e=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(e)}}(0,n.__decorate)([(0,a.IO)("slot")],c.prototype,"slotElement",void 0),(0,n.__decorate)([(0,a.GC)("mwc-ripple")],c.prototype,"ripple",void 0),(0,n.__decorate)([(0,a.Cb)({type:String})],c.prototype,"value",void 0),(0,n.__decorate)([(0,a.Cb)({type:String,reflect:!0})],c.prototype,"group",void 0),(0,n.__decorate)([(0,a.Cb)({type:Number,reflect:!0})],c.prototype,"tabindex",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0}),(0,s.P)((function(e){e?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],c.prototype,"disabled",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],c.prototype,"twoline",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],c.prototype,"activated",void 0),(0,n.__decorate)([(0,a.Cb)({type:String,reflect:!0})],c.prototype,"graphic",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],c.prototype,"multipleGraphics",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],c.prototype,"hasMeta",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0}),(0,s.P)((function(e){e?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],c.prototype,"noninteractive",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0}),(0,s.P)((function(e){const t=this.getAttribute("role"),i="gridcell"===t||"option"===t||"row"===t||"tab"===t;i&&e?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(e,"property")}))],c.prototype,"selected",void 0),(0,n.__decorate)([(0,a.SB)()],c.prototype,"shouldRenderRipple",void 0),(0,n.__decorate)([(0,a.SB)()],c.prototype,"_managingList",void 0)},96762:(e,t,i)=>{i.d(t,{W:()=>n});const n=i(9644).iv`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`},44577:(e,t,i)=>{var n=i(43204),s=i(36924),r=i(61092),o=i(96762);let a=class extends r.K{};a.styles=[o.W],a=(0,n.__decorate)([(0,s.Mo)("mwc-list-item")],a)},11581:(e,t,i)=>{i.d(t,{H:()=>_});var n=i(43204),s=(i(91156),i(38103)),r=i(78220),o=i(14114),a=i(98734),l=i(72774),c={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},d={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const h=function(e){function t(i){return e.call(this,(0,n.__assign)((0,n.__assign)({},t.defaultAdapter),i))||this}return(0,n.__extends)(t,e),Object.defineProperty(t,"strings",{get:function(){return d},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return c},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(c.DISABLED):this.adapter.removeClass(c.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(c.CHECKED):this.adapter.removeClass(c.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(d.ARIA_CHECKED_ATTR,""+!!e)},t}(l.K);var p=i(9644),u=i(36924),m=i(51346);class _ extends r.H{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=h,this.rippleHandlers=new a.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,r.q)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?p.dy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}render(){return p.dy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,m.o)(this.ariaLabel)}"
              aria-labelledby="${(0,m.o)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,n.__decorate)([(0,u.Cb)({type:Boolean}),(0,o.P)((function(e){this.mdcFoundation.setChecked(e)}))],_.prototype,"checked",void 0),(0,n.__decorate)([(0,u.Cb)({type:Boolean}),(0,o.P)((function(e){this.mdcFoundation.setDisabled(e)}))],_.prototype,"disabled",void 0),(0,n.__decorate)([s.L,(0,u.Cb)({attribute:"aria-label"})],_.prototype,"ariaLabel",void 0),(0,n.__decorate)([s.L,(0,u.Cb)({attribute:"aria-labelledby"})],_.prototype,"ariaLabelledBy",void 0),(0,n.__decorate)([(0,u.IO)(".mdc-switch")],_.prototype,"mdcRoot",void 0),(0,n.__decorate)([(0,u.IO)("input")],_.prototype,"formElement",void 0),(0,n.__decorate)([(0,u.GC)("mwc-ripple")],_.prototype,"ripple",void 0),(0,n.__decorate)([(0,u.SB)()],_.prototype,"shouldRenderRipple",void 0),(0,n.__decorate)([(0,u.hO)({passive:!0})],_.prototype,"handleRippleMouseDown",null),(0,n.__decorate)([(0,u.hO)({passive:!0})],_.prototype,"handleRippleTouchStart",null)},4301:(e,t,i)=>{i.d(t,{W:()=>n});const n=i(9644).iv`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`},65660:(e,t,i)=>{i(12249);const n=i(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content);var s=document.createElement("style");s.textContent="[hidden] { display: none !important; }",document.head.appendChild(s)},25782:(e,t,i)=>{i(12249),i(65660),i(70019),i(97968);var n=i(67139),s=i(50856),r=i(56289);(0,n.k)({_template:s.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[r.U]})},56289:(e,t,i)=>{i.d(t,{U:()=>y});i(12249);var n=i(18149);const s={properties:{focused:{type:Boolean,value:!1,notify:!0,readOnly:!0,reflectToAttribute:!0},disabled:{type:Boolean,value:!1,notify:!0,observer:"_disabledChanged",reflectToAttribute:!0},_oldTabIndex:{type:String},_boundFocusBlurHandler:{type:Function,value:function(){return this._focusBlurHandler.bind(this)}}},observers:["_changedControlState(focused, disabled)"],ready:function(){this.addEventListener("focus",this._boundFocusBlurHandler,!0),this.addEventListener("blur",this._boundFocusBlurHandler,!0)},_focusBlurHandler:function(e){this._setFocused("focus"===e.type)},_disabledChanged:function(e,t){this.setAttribute("aria-disabled",e?"true":"false"),this.style.pointerEvents=e?"none":"",e?(this._oldTabIndex=this.getAttribute("tabindex"),this._setFocused(!1),this.tabIndex=-1,this.blur()):void 0!==this._oldTabIndex&&(null===this._oldTabIndex?this.removeAttribute("tabindex"):this.setAttribute("tabindex",this._oldTabIndex))},_changedControlState:function(){this._controlStateChanged&&this._controlStateChanged()}};var r={"U+0008":"backspace","U+0009":"tab","U+001B":"esc","U+0020":"space","U+007F":"del"},o={8:"backspace",9:"tab",13:"enter",27:"esc",33:"pageup",34:"pagedown",35:"end",36:"home",32:"space",37:"left",38:"up",39:"right",40:"down",46:"del",106:"*"},a={shift:"shiftKey",ctrl:"ctrlKey",alt:"altKey",meta:"metaKey"},l=/[a-z0-9*]/,c=/U\+/,d=/^arrow/,h=/^space(bar)?/,p=/^escape$/;function u(e,t){var i="";if(e){var n=e.toLowerCase();" "===n||h.test(n)?i="space":p.test(n)?i="esc":1==n.length?t&&!l.test(n)||(i=n):i=d.test(n)?n.replace("arrow",""):"multiply"==n?"*":n}return i}function m(e,t){return e.key?u(e.key,t):e.detail&&e.detail.key?u(e.detail.key,t):(i=e.keyIdentifier,n="",i&&(i in r?n=r[i]:c.test(i)?(i=parseInt(i.replace("U+","0x"),16),n=String.fromCharCode(i).toLowerCase()):n=i.toLowerCase()),n||function(e){var t="";return Number(e)&&(t=e>=65&&e<=90?String.fromCharCode(32+e):e>=112&&e<=123?"f"+(e-112+1):e>=48&&e<=57?String(e-48):e>=96&&e<=105?String(e-96):o[e]),t}(e.keyCode)||"");var i,n}function _(e,t){return m(t,e.hasModifiers)===e.key&&(!e.hasModifiers||!!t.shiftKey==!!e.shiftKey&&!!t.ctrlKey==!!e.ctrlKey&&!!t.altKey==!!e.altKey&&!!t.metaKey==!!e.metaKey)}function f(e){return e.trim().split(" ").map((function(e){return function(e){return 1===e.length?{combo:e,key:e,event:"keydown"}:e.split("+").reduce((function(e,t){var i=t.split(":"),n=i[0],s=i[1];return n in a?(e[a[n]]=!0,e.hasModifiers=!0):(e.key=n,e.event=s||"keydown"),e}),{combo:e.split(":").shift()})}(e)}))}const y=[[{properties:{keyEventTarget:{type:Object,value:function(){return this}},stopKeyboardEventPropagation:{type:Boolean,value:!1},_boundKeyHandlers:{type:Array,value:function(){return[]}},_imperativeKeyBindings:{type:Object,value:function(){return{}}}},observers:["_resetKeyEventListeners(keyEventTarget, _boundKeyHandlers)"],keyBindings:{},registered:function(){this._prepKeyBindings()},attached:function(){this._listenKeyEventListeners()},detached:function(){this._unlistenKeyEventListeners()},addOwnKeyBinding:function(e,t){this._imperativeKeyBindings[e]=t,this._prepKeyBindings(),this._resetKeyEventListeners()},removeOwnKeyBindings:function(){this._imperativeKeyBindings={},this._prepKeyBindings(),this._resetKeyEventListeners()},keyboardEventMatchesKeys:function(e,t){for(var i=f(t),n=0;n<i.length;++n)if(_(i[n],e))return!0;return!1},_collectKeyBindings:function(){var e=this.behaviors.map((function(e){return e.keyBindings}));return-1===e.indexOf(this.keyBindings)&&e.push(this.keyBindings),e},_prepKeyBindings:function(){for(var e in this._keyBindings={},this._collectKeyBindings().forEach((function(e){for(var t in e)this._addKeyBinding(t,e[t])}),this),this._imperativeKeyBindings)this._addKeyBinding(e,this._imperativeKeyBindings[e]);for(var t in this._keyBindings)this._keyBindings[t].sort((function(e,t){var i=e[0].hasModifiers;return i===t[0].hasModifiers?0:i?-1:1}))},_addKeyBinding:function(e,t){f(e).forEach((function(e){this._keyBindings[e.event]=this._keyBindings[e.event]||[],this._keyBindings[e.event].push([e,t])}),this)},_resetKeyEventListeners:function(){this._unlistenKeyEventListeners(),this.isAttached&&this._listenKeyEventListeners()},_listenKeyEventListeners:function(){this.keyEventTarget&&Object.keys(this._keyBindings).forEach((function(e){var t=this._keyBindings[e],i=this._onKeyBindingEvent.bind(this,t);this._boundKeyHandlers.push([this.keyEventTarget,e,i]),this.keyEventTarget.addEventListener(e,i)}),this)},_unlistenKeyEventListeners:function(){for(var e,t,i,n;this._boundKeyHandlers.length;)t=(e=this._boundKeyHandlers.pop())[0],i=e[1],n=e[2],t.removeEventListener(i,n)},_onKeyBindingEvent:function(e,t){if(this.stopKeyboardEventPropagation&&t.stopPropagation(),!t.defaultPrevented)for(var i=0;i<e.length;i++){var n=e[i][0],s=e[i][1];if(_(n,t)&&(this._triggerKeyHandler(n,s,t),t.defaultPrevented))return}},_triggerKeyHandler:function(e,t,i){var n=Object.create(e);n.keyboardEvent=i;var s=new CustomEvent(e.event,{detail:n,cancelable:!0});this[t].call(this,s),s.defaultPrevented&&i.preventDefault()}},{properties:{pressed:{type:Boolean,readOnly:!0,value:!1,reflectToAttribute:!0,observer:"_pressedChanged"},toggles:{type:Boolean,value:!1,reflectToAttribute:!0},active:{type:Boolean,value:!1,notify:!0,reflectToAttribute:!0},pointerDown:{type:Boolean,readOnly:!0,value:!1},receivedFocusFromKeyboard:{type:Boolean,readOnly:!0},ariaActiveAttribute:{type:String,value:"aria-pressed",observer:"_ariaActiveAttributeChanged"}},listeners:{down:"_downHandler",up:"_upHandler",tap:"_tapHandler"},observers:["_focusChanged(focused)","_activeChanged(active, ariaActiveAttribute)"],keyBindings:{"enter:keydown":"_asyncClick","space:keydown":"_spaceKeyDownHandler","space:keyup":"_spaceKeyUpHandler"},_mouseEventRe:/^mouse/,_tapHandler:function(){this.toggles?this._userActivate(!this.active):this.active=!1},_focusChanged:function(e){this._detectKeyboardFocus(e),e||this._setPressed(!1)},_detectKeyboardFocus:function(e){this._setReceivedFocusFromKeyboard(!this.pointerDown&&e)},_userActivate:function(e){this.active!==e&&(this.active=e,this.fire("change"))},_downHandler:function(e){this._setPointerDown(!0),this._setPressed(!0),this._setReceivedFocusFromKeyboard(!1)},_upHandler:function(){this._setPointerDown(!1),this._setPressed(!1)},_spaceKeyDownHandler:function(e){var t=e.detail.keyboardEvent,i=(0,n.vz)(t).localTarget;this.isLightDescendant(i)||(t.preventDefault(),t.stopImmediatePropagation(),this._setPressed(!0))},_spaceKeyUpHandler:function(e){var t=e.detail.keyboardEvent,i=(0,n.vz)(t).localTarget;this.isLightDescendant(i)||(this.pressed&&this._asyncClick(),this._setPressed(!1))},_asyncClick:function(){this.async((function(){this.click()}),1)},_pressedChanged:function(e){this._changedButtonState()},_ariaActiveAttributeChanged:function(e,t){t&&t!=e&&this.hasAttribute(t)&&this.removeAttribute(t)},_activeChanged:function(e,t){this.toggles?this.setAttribute(this.ariaActiveAttribute,e?"true":"false"):this.removeAttribute(this.ariaActiveAttribute),this._changedButtonState()},_controlStateChanged:function(){this.disabled?this._setPressed(!1):this._changedButtonState()},_changedButtonState:function(){this._buttonStateChanged&&this._buttonStateChanged()}}],s,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(e,t,i)=>{i(12249),i(65660),i(70019);var n=i(67139),s=i(50856);(0,n.k)({_template:s.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(e,t,i)=>{i(65660),i(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(e,t,i)=>{i(12249),i(65660),i(97968);var n=i(67139),s=i(50856),r=i(56289);(0,n.k)({_template:s.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[r.U]})},70019:(e,t,i)=>{i(12249);const n=i(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},81096:(e,t,i)=>{i.d(t,{x:()=>ke});var n=i(26539);class s{constructor(){this.start=0,this.end=0,this.previous=null,this.parent=null,this.rules=null,this.parsedCssText="",this.cssText="",this.atRule=!1,this.type=0,this.keyframesName="",this.selector="",this.parsedSelector=""}}function r(e){return o(function(e){let t=new s;t.start=0,t.end=e.length;let i=t;for(let n=0,r=e.length;n<r;n++)if(e[n]===c){i.rules||(i.rules=[]);let e=i,t=e.rules[e.rules.length-1]||null;i=new s,i.start=n+1,i.parent=e,i.previous=t,e.rules.push(i)}else e[n]===d&&(i.end=n+1,i=i.parent||t);return t}(e=e.replace(h.comments,"").replace(h.port,"")),e)}function o(e,t){let i=t.substring(e.start,e.end-1);if(e.parsedCssText=e.cssText=i.trim(),e.parent){let n=e.previous?e.previous.end:e.parent.start;i=t.substring(n,e.start-1),i=function(e){return e.replace(/\\([0-9a-f]{1,6})\s/gi,(function(){let e=arguments[1],t=6-e.length;for(;t--;)e="0"+e;return"\\"+e}))}(i),i=i.replace(h.multipleSpaces," "),i=i.substring(i.lastIndexOf(";")+1);let s=e.parsedSelector=e.selector=i.trim();e.atRule=0===s.indexOf(m),e.atRule?0===s.indexOf(u)?e.type=l.MEDIA_RULE:s.match(h.keyframesRule)&&(e.type=l.KEYFRAMES_RULE,e.keyframesName=e.selector.split(h.multipleSpaces).pop()):0===s.indexOf(p)?e.type=l.MIXIN_RULE:e.type=l.STYLE_RULE}let n=e.rules;if(n)for(let s,r=0,a=n.length;r<a&&(s=n[r]);r++)o(s,t);return e}function a(e,t,i=""){let n="";if(e.cssText||e.rules){let i=e.rules;if(i&&!function(e){let t=e[0];return Boolean(t)&&Boolean(t.selector)&&0===t.selector.indexOf(p)}(i))for(let e,s=0,r=i.length;s<r&&(e=i[s]);s++)n=a(e,t,n);else n=t?e.cssText:function(e){return e=function(e){return e.replace(h.customProp,"").replace(h.mixinProp,"")}(e),function(e){return e.replace(h.mixinApply,"").replace(h.varApply,"")}(e)}(e.cssText),n=n.trim(),n&&(n="  "+n+"\n")}return n&&(e.selector&&(i+=e.selector+" "+c+"\n"),i+=n,e.selector&&(i+=d+"\n\n")),i}const l={STYLE_RULE:1,KEYFRAMES_RULE:7,MEDIA_RULE:4,MIXIN_RULE:1e3},c="{",d="}",h={comments:/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,port:/@import[^;]*;/gim,customProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?(?:[;\n]|$)/gim,mixinProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?{[^}]*?}(?:[;\n]|$)?/gim,mixinApply:/@apply\s*\(?[^);]*\)?\s*(?:[;\n]|$)?/gim,varApply:/[^;:]*?:[^;]*?var\([^;]*\)(?:[;\n]|$)?/gim,keyframesRule:/^@[^\s]*keyframes/,multipleSpaces:/\s+/g},p="--",u="@media",m="@";var _=i(60309);const f=new Set,y="shady-unscoped";function g(e){const t=e.textContent;if(!f.has(t)){f.add(t);const e=document.createElement("style");e.setAttribute("shady-unscoped",""),e.textContent=t,document.head.appendChild(e)}}function b(e){return e.hasAttribute(y)}function v(e,t){return e?("string"==typeof e&&(e=r(e)),t&&x(e,t),a(e,n.rd)):""}function w(e){return!e.__cssRules&&e.textContent&&(e.__cssRules=r(e.textContent)),e.__cssRules||null}function x(e,t,i,n){if(!e)return;let s=!1,r=e.type;if(n&&r===l.MEDIA_RULE){let t=e.selector.match(_.mA);t&&(window.matchMedia(t[1]).matches||(s=!0))}r===l.STYLE_RULE?t(e):i&&r===l.KEYFRAMES_RULE?i(e):r===l.MIXIN_RULE&&(s=!0);let o=e.rules;if(o&&!s)for(let a,l=0,c=o.length;l<c&&(a=o[l]);l++)x(a,t,i,n)}function C(e,t){let i=0;for(let n=t,s=e.length;n<s;n++)if("("===e[n])i++;else if(")"===e[n]&&0==--i)return n;return-1}function S(e,t){let i=e.indexOf("var(");if(-1===i)return t(e,"","","");let n=C(e,i+3),s=e.substring(i+4,n),r=e.substring(0,i),o=S(e.substring(n+1),t),a=s.indexOf(",");return-1===a?t(r,s.trim(),"",o):t(r,s.substring(0,a).trim(),s.substring(a+1).trim(),o)}window.ShadyDOM&&window.ShadyDOM.wrap;const k="css-build";function E(e){if(void 0!==n.Cp)return n.Cp;if(void 0===e.__cssBuild){const t=e.getAttribute(k);if(t)e.__cssBuild=t;else{const t=function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;if(t instanceof Comment){const e=t.textContent.trim().split(":");if(e[0]===k)return e[1]}return""}(e);""!==t&&function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;t.parentNode.removeChild(t)}(e),e.__cssBuild=t}}return e.__cssBuild||""}function P(e){return""!==E(e)}var A=i(10868);const O=/;\s*/m,T=/^\s*(initial)|(inherit)\s*$/,I=/\s*!important/,N="_-_";class D{constructor(){this._map={}}set(e,t){e=e.trim(),this._map[e]={properties:t,dependants:{}}}get(e){return e=e.trim(),this._map[e]||null}}let M=null;class R{constructor(){this._currentElement=null,this._measureElement=null,this._map=new D}detectMixin(e){return(0,A.OH)(e)}gatherStyles(e){const t=function(e){const t=[],i=e.querySelectorAll("style");for(let s=0;s<i.length;s++){const e=i[s];b(e)?n.WA||(g(e),e.parentNode.removeChild(e)):(t.push(e.textContent),e.parentNode.removeChild(e))}return t.join("").trim()}(e.content);if(t){const i=document.createElement("style");return i.textContent=t,e.content.insertBefore(i,e.content.firstChild),i}return null}transformTemplate(e,t){void 0===e._gatheredStyle&&(e._gatheredStyle=this.gatherStyles(e));const i=e._gatheredStyle;return i?this.transformStyle(i,t):null}transformStyle(e,t=""){let i=w(e);return this.transformRules(i,t),e.textContent=v(i),i}transformCustomStyle(e){let t=w(e);return x(t,(e=>{":root"===e.selector&&(e.selector="html"),this.transformRule(e)})),e.textContent=v(t),t}transformRules(e,t){this._currentElement=t,x(e,(e=>{this.transformRule(e)})),this._currentElement=null}transformRule(e){e.cssText=this.transformCssText(e.parsedCssText,e),":root"===e.selector&&(e.selector=":host > *")}transformCssText(e,t){return e=e.replace(_.CN,((e,i,n,s)=>this._produceCssProperties(e,i,n,s,t))),this._consumeCssProperties(e,t)}_getInitialValueForProperty(e){return this._measureElement||(this._measureElement=document.createElement("meta"),this._measureElement.setAttribute("apply-shim-measure",""),this._measureElement.style.all="initial",document.head.appendChild(this._measureElement)),window.getComputedStyle(this._measureElement).getPropertyValue(e)}_fallbacksFromPreviousRules(e){let t=e;for(;t.parent;)t=t.parent;const i={};let n=!1;return x(t,(t=>{n=n||t===e,n||t.selector===e.selector&&Object.assign(i,this._cssTextToMap(t.parsedCssText))})),i}_consumeCssProperties(e,t){let i=null;for(;i=_.$T.exec(e);){let n=i[0],s=i[1],r=i.index,o=r+n.indexOf("@apply"),a=r+n.length,l=e.slice(0,o),c=e.slice(a),d=t?this._fallbacksFromPreviousRules(t):{};Object.assign(d,this._cssTextToMap(l));let h=this._atApplyToCssProperties(s,d);e=`${l}${h}${c}`,_.$T.lastIndex=r+h.length}return e}_atApplyToCssProperties(e,t){e=e.replace(O,"");let i=[],n=this._map.get(e);if(n||(this._map.set(e,{}),n=this._map.get(e)),n){let s,r,o;this._currentElement&&(n.dependants[this._currentElement]=!0);const a=n.properties;for(s in a)o=t&&t[s],r=[s,": var(",e,N,s],o&&r.push(",",o.replace(I,"")),r.push(")"),I.test(a[s])&&r.push(" !important"),i.push(r.join(""))}return i.join("; ")}_replaceInitialOrInherit(e,t){let i=T.exec(t);return i&&(t=i[1]?this._getInitialValueForProperty(e):"apply-shim-inherit"),t}_cssTextToMap(e,t=!1){let i,n,s=e.split(";"),r={};for(let o,a,l=0;l<s.length;l++)o=s[l],o&&(a=o.split(":"),a.length>1&&(i=a[0].trim(),n=a.slice(1).join(":"),t&&(n=this._replaceInitialOrInherit(i,n)),r[i]=n));return r}_invalidateMixinEntry(e){if(M)for(let t in e.dependants)t!==this._currentElement&&M(t)}_produceCssProperties(e,t,i,n,s){if(i&&S(i,((e,t)=>{t&&this._map.get(t)&&(n=`@apply ${t};`)})),!n)return e;let r=this._consumeCssProperties(""+n,s),o=e.slice(0,e.indexOf("--")),a=this._cssTextToMap(r,!0),l=a,c=this._map.get(t),d=c&&c.properties;d?l=Object.assign(Object.create(d),a):this._map.set(t,l);let h,p,u=[],m=!1;for(h in l)p=a[h],void 0===p&&(p="initial"),d&&!(h in d)&&(m=!0),u.push(`${t}${N}${h}: ${p}`);return m&&this._invalidateMixinEntry(c),c&&(c.properties=l),i&&(o=`${e};${o}`),`${o}${u.join("; ")};`}}R.prototype.detectMixin=R.prototype.detectMixin,R.prototype.transformStyle=R.prototype.transformStyle,R.prototype.transformCustomStyle=R.prototype.transformCustomStyle,R.prototype.transformRules=R.prototype.transformRules,R.prototype.transformRule=R.prototype.transformRule,R.prototype.transformTemplate=R.prototype.transformTemplate,R.prototype._separator=N,Object.defineProperty(R.prototype,"invalidCallback",{get(){return M},set(e){M=e}});const L=R,H={},B="_applyShimCurrentVersion",F="_applyShimNextVersion",z="_applyShimValidatingVersion",j=Promise.resolve();function K(e){let t=H[e];t&&function(e){e[B]=e[B]||0,e[z]=e[z]||0,e[F]=(e[F]||0)+1}(t)}function $(e){return e[B]===e[F]}function U(e){return!$(e)&&e[z]===e[F]}function q(e){e[z]=e[F],e._validating||(e._validating=!0,j.then((function(){e[B]=e[F],e._validating=!1})))}i(34816);const Y=new L;class X{constructor(){this.customStyleInterface=null,Y.invalidCallback=K}ensure(){this.customStyleInterface||window.ShadyCSS.CustomStyleInterface&&(this.customStyleInterface=window.ShadyCSS.CustomStyleInterface,this.customStyleInterface.transformCallback=e=>{Y.transformCustomStyle(e)},this.customStyleInterface.validateCallback=()=>{requestAnimationFrame((()=>{this.customStyleInterface.enqueued&&this.flushCustomStyles()}))})}prepareTemplate(e,t){if(this.ensure(),P(e))return;H[t]=e;let i=Y.transformTemplate(e,t);e._styleAst=i}flushCustomStyles(){if(this.ensure(),!this.customStyleInterface)return;let e=this.customStyleInterface.processStyles();if(this.customStyleInterface.enqueued){for(let t=0;t<e.length;t++){let i=e[t],n=this.customStyleInterface.getStyleForCustomStyle(i);n&&Y.transformCustomStyle(n)}this.customStyleInterface.enqueued=!1}}styleSubtree(e,t){if(this.ensure(),t&&(0,A.wW)(e,t),e.shadowRoot){this.styleElement(e);let t=e.shadowRoot.children||e.shadowRoot.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}else{let t=e.children||e.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}}styleElement(e){this.ensure();let{is:t}=function(e){let t=e.localName,i="",n="";return t?t.indexOf("-")>-1?i=t:(n=t,i=e.getAttribute&&e.getAttribute("is")||""):(i=e.is,n=e.extends),{is:i,typeExtension:n}}(e),i=H[t];if((!i||!P(i))&&i&&!$(i)){U(i)||(this.prepareTemplate(i,t),q(i));let n=e.shadowRoot;if(n){let e=n.querySelector("style");e&&(e.__cssRules=i._styleAst,e.textContent=v(i._styleAst))}}}styleDocument(e){this.ensure(),this.styleSubtree(document.body,e)}}if(!window.ShadyCSS||!window.ShadyCSS.ScopingShim){const e=new X;let t=window.ShadyCSS&&window.ShadyCSS.CustomStyleInterface;window.ShadyCSS={prepareTemplate(t,i,n){e.flushCustomStyles(),e.prepareTemplate(t,i)},prepareTemplateStyles(e,t,i){window.ShadyCSS.prepareTemplate(e,t,i)},prepareTemplateDom(e,t){},styleSubtree(t,i){e.flushCustomStyles(),e.styleSubtree(t,i)},styleElement(t){e.flushCustomStyles(),e.styleElement(t)},styleDocument(t){e.flushCustomStyles(),e.styleDocument(t)},getComputedStyleValue(e,t){return(0,A.B7)(e,t)},flushCustomStyles(){e.flushCustomStyles()},nativeCss:n.rd,nativeShadow:n.WA,cssBuild:n.Cp,disableRuntime:n.jF},t&&(window.ShadyCSS.CustomStyleInterface=t)}window.ShadyCSS.ApplyShim=Y;var J=i(36608),W=i(60995),V=i(63933),G=i(76389);const Z=/:host\(:dir\((ltr|rtl)\)\)/g,Q=/([\s\w-#\.\[\]\*]*):dir\((ltr|rtl)\)/g,ee=/:dir\((?:ltr|rtl)\)/,te=Boolean(window.ShadyDOM&&window.ShadyDOM.inUse),ie=[];let ne=null,se="";function re(){se=document.documentElement.getAttribute("dir")}function oe(e){if(!e.__autoDirOptOut){e.setAttribute("dir",se)}}function ae(){re(),se=document.documentElement.getAttribute("dir");for(let e=0;e<ie.length;e++)oe(ie[e])}const le=(0,G.o)((e=>{te||ne||(re(),ne=new MutationObserver(ae),ne.observe(document.documentElement,{attributes:!0,attributeFilter:["dir"]}));const t=(0,V.Q)(e);class i extends t{static _processStyleText(e,i){return e=t._processStyleText.call(this,e,i),!te&&ee.test(e)&&(e=this._replaceDirInCssText(e),this.__activateDir=!0),e}static _replaceDirInCssText(e){let t=e;return t=t.replace(Z,':host([dir="$1"])'),t=t.replace(Q,':host([dir="$2"]) $1'),t}constructor(){super(),this.__autoDirOptOut=!1}ready(){super.ready(),this.__autoDirOptOut=this.hasAttribute("dir")}connectedCallback(){t.prototype.connectedCallback&&super.connectedCallback(),this.constructor.__activateDir&&(ne&&ne.takeRecords().length&&ae(),ie.push(this),oe(this))}disconnectedCallback(){if(t.prototype.disconnectedCallback&&super.disconnectedCallback(),this.constructor.__activateDir){const e=ie.indexOf(this);e>-1&&ie.splice(e,1)}}}return i.__activateDir=!1,i}));i(87529);function ce(){document.body.removeAttribute("unresolved")}"interactive"===document.readyState||"complete"===document.readyState?ce():window.addEventListener("DOMContentLoaded",ce);var de=i(18149),he=i(81668),pe=i(78956),ue=i(21683),me=i(4059),_e=i(62276);i(56646);const fe=window.ShadyDOM,ye=window.ShadyCSS;function ge(e,t){return(0,_e.r)(e).getRootNode()===t}var be=i(74460);const ve="disable-upgrade",we=e=>{for(;e;){const t=Object.getOwnPropertyDescriptor(e,"observedAttributes");if(t)return t.get;e=Object.getPrototypeOf(e.prototype).constructor}return()=>[]};(0,G.o)((e=>{const t=(0,J.SH)(e);let i=we(t);return class extends t{constructor(){super(),this.__isUpgradeDisabled}static get observedAttributes(){return i.call(this).concat(ve)}_initializeProperties(){this.hasAttribute(ve)?this.__isUpgradeDisabled=!0:super._initializeProperties()}_enableProperties(){this.__isUpgradeDisabled||super._enableProperties()}_canApplyPropertyDefault(e){return super._canApplyPropertyDefault(e)&&!(this.__isUpgradeDisabled&&this._isPropertyPending(e))}attributeChangedCallback(e,t,i,n){e==ve?this.__isUpgradeDisabled&&null==i&&(super._initializeProperties(),this.__isUpgradeDisabled=!1,(0,_e.r)(this).isConnected&&super.connectedCallback()):super.attributeChangedCallback(e,t,i,n)}connectedCallback(){this.__isUpgradeDisabled||super.connectedCallback()}disconnectedCallback(){this.__isUpgradeDisabled||super.disconnectedCallback()}}}));var xe=i(65412);const Ce="disable-upgrade";let Se=window.ShadyCSS;const ke=(0,G.o)((e=>{const t=(0,W._)((0,J.SH)(e)),i=J.PP?t:le(t),n=we(i),s={x:"pan-x",y:"pan-y",none:"none",all:"auto"};class r extends i{constructor(){super(),this.isAttached,this.__boundListeners,this._debouncers,this.__isUpgradeDisabled,this.__needsAttributesAtConnected,this._legacyForceObservedAttributes}static get importMeta(){return this.prototype.importMeta}created(){}__attributeReaction(e,t,i){(this.__dataAttributes&&this.__dataAttributes[e]||e===Ce)&&this.attributeChangedCallback(e,t,i,null)}setAttribute(e,t){if(be.j8&&!this._legacyForceObservedAttributes){const i=this.getAttribute(e);super.setAttribute(e,t),this.__attributeReaction(e,i,String(t))}else super.setAttribute(e,t)}removeAttribute(e){if(be.j8&&!this._legacyForceObservedAttributes){const t=this.getAttribute(e);super.removeAttribute(e),this.__attributeReaction(e,t,null)}else super.removeAttribute(e)}static get observedAttributes(){return be.j8&&!this.prototype._legacyForceObservedAttributes?(this.hasOwnProperty(JSCompiler_renameProperty("__observedAttributes",this))||(this.__observedAttributes=[],(0,xe.z2)(this.prototype)),this.__observedAttributes):n.call(this).concat(Ce)}_enableProperties(){this.__isUpgradeDisabled||super._enableProperties()}_canApplyPropertyDefault(e){return super._canApplyPropertyDefault(e)&&!(this.__isUpgradeDisabled&&this._isPropertyPending(e))}connectedCallback(){this.__needsAttributesAtConnected&&this._takeAttributes(),this.__isUpgradeDisabled||(super.connectedCallback(),this.isAttached=!0,this.attached())}attached(){}disconnectedCallback(){this.__isUpgradeDisabled||(super.disconnectedCallback(),this.isAttached=!1,this.detached())}detached(){}attributeChangedCallback(e,t,i,n){t!==i&&(e==Ce?this.__isUpgradeDisabled&&null==i&&(this._initializeProperties(),this.__isUpgradeDisabled=!1,(0,_e.r)(this).isConnected&&this.connectedCallback()):(super.attributeChangedCallback(e,t,i,n),this.attributeChanged(e,t,i)))}attributeChanged(e,t,i){}_initializeProperties(){if(be.nL&&this.hasAttribute(Ce))this.__isUpgradeDisabled=!0;else{let e=Object.getPrototypeOf(this);e.hasOwnProperty(JSCompiler_renameProperty("__hasRegisterFinished",e))||(this._registered(),e.__hasRegisterFinished=!0),super._initializeProperties(),this.root=this,this.created(),be.j8&&!this._legacyForceObservedAttributes&&(this.hasAttributes()?this._takeAttributes():this.parentNode||(this.__needsAttributesAtConnected=!0)),this._applyListeners()}}_takeAttributes(){const e=this.attributes;for(let t=0,i=e.length;t<i;t++){const i=e[t];this.__attributeReaction(i.name,null,i.value)}}_registered(){}ready(){this._ensureAttributes(),super.ready()}_ensureAttributes(){}_applyListeners(){}serialize(e){return this._serializeValue(e)}deserialize(e,t){return this._deserializeValue(e,t)}reflectPropertyToAttribute(e,t,i){this._propertyToAttribute(e,t,i)}serializeValueToAttribute(e,t,i){this._valueToNodeAttribute(i||this,e,t)}extend(e,t){if(!e||!t)return e||t;let i=Object.getOwnPropertyNames(t);for(let n,s=0;s<i.length&&(n=i[s]);s++){let i=Object.getOwnPropertyDescriptor(t,n);i&&Object.defineProperty(e,n,i)}return e}mixin(e,t){for(let i in t)e[i]=t[i];return e}chainObject(e,t){return e&&t&&e!==t&&(e.__proto__=t),e}instanceTemplate(e){let t=this.constructor._contentForTemplate(e);return document.importNode(t,!0)}fire(e,t,i){i=i||{},t=null==t?{}:t;let n=new Event(e,{bubbles:void 0===i.bubbles||i.bubbles,cancelable:Boolean(i.cancelable),composed:void 0===i.composed||i.composed});n.detail=t;let s=i.node||this;return(0,_e.r)(s).dispatchEvent(n),n}listen(e,t,i){e=e||this;let n=this.__boundListeners||(this.__boundListeners=new WeakMap),s=n.get(e);s||(s={},n.set(e,s));let r=t+i;s[r]||(s[r]=this._addMethodEventListenerToNode(e,t,i,this))}unlisten(e,t,i){e=e||this;let n=this.__boundListeners&&this.__boundListeners.get(e),s=t+i,r=n&&n[s];r&&(this._removeEventListenerFromNode(e,t,r),n[s]=null)}setScrollDirection(e,t){(0,he.BP)(t||this,s[e]||"auto")}$$(e){return this.root.querySelector(e)}get domHost(){let e=(0,_e.r)(this).getRootNode();return e instanceof DocumentFragment?e.host:e}distributeContent(){const e=(0,de.vz)(this);window.ShadyDOM&&e.shadowRoot&&ShadyDOM.flush()}getEffectiveChildNodes(){return(0,de.vz)(this).getEffectiveChildNodes()}queryDistributedElements(e){return(0,de.vz)(this).queryDistributedElements(e)}getEffectiveChildren(){return this.getEffectiveChildNodes().filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}getEffectiveTextContent(){let e=this.getEffectiveChildNodes(),t=[];for(let i,n=0;i=e[n];n++)i.nodeType!==Node.COMMENT_NODE&&t.push(i.textContent);return t.join("")}queryEffectiveChildren(e){let t=this.queryDistributedElements(e);return t&&t[0]}queryAllEffectiveChildren(e){return this.queryDistributedElements(e)}getContentChildNodes(e){let t=this.root.querySelector(e||"slot");return t?(0,de.vz)(t).getDistributedNodes():[]}getContentChildren(e){return this.getContentChildNodes(e).filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}isLightDescendant(e){const t=this;return t!==e&&(0,_e.r)(t).contains(e)&&(0,_e.r)(t).getRootNode()===(0,_e.r)(e).getRootNode()}isLocalDescendant(e){return this.root===(0,_e.r)(e).getRootNode()}scopeSubtree(e,t=!1){return function(e,t=!1){if(!fe||!ye)return null;if(!fe.handlesDynamicScoping)return null;const i=ye.ScopingShim;if(!i)return null;const n=i.scopeForNode(e),s=(0,_e.r)(e).getRootNode(),r=e=>{if(!ge(e,s))return;const t=Array.from(fe.nativeMethods.querySelectorAll.call(e,"*"));t.push(e);for(let r=0;r<t.length;r++){const e=t[r];if(!ge(e,s))continue;const o=i.currentScopeForNode(e);o!==n&&(""!==o&&i.unscopeNode(e,o),i.scopeNode(e,n))}};if(r(e),t){const t=new MutationObserver((e=>{for(let t=0;t<e.length;t++){const i=e[t];for(let e=0;e<i.addedNodes.length;e++){const t=i.addedNodes[e];t.nodeType===Node.ELEMENT_NODE&&r(t)}}}));return t.observe(e,{childList:!0,subtree:!0}),t}return null}(e,t)}getComputedStyleValue(e){return Se.getComputedStyleValue(this,e)}debounce(e,t,i){return this._debouncers=this._debouncers||{},this._debouncers[e]=pe.dx.debounce(this._debouncers[e],i>0?ue.Wc.after(i):ue.YA,t.bind(this))}isDebouncerActive(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];return!(!t||!t.isActive())}flushDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.flush()}cancelDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.cancel()}async(e,t){return t>0?ue.Wc.run(e.bind(this),t):~ue.YA.run(e.bind(this))}cancelAsync(e){e<0?ue.YA.cancel(~e):ue.Wc.cancel(e)}create(e,t){let i=document.createElement(e);if(t)if(i.setProperties)i.setProperties(t);else for(let n in t)i[n]=t[n];return i}elementMatches(e,t){return(0,de.Ku)(t||this,e)}toggleAttribute(e,t){let i=this;return 3===arguments.length&&(i=arguments[2]),1==arguments.length&&(t=!i.hasAttribute(e)),t?((0,_e.r)(i).setAttribute(e,""),!0):((0,_e.r)(i).removeAttribute(e),!1)}toggleClass(e,t,i){i=i||this,1==arguments.length&&(t=!i.classList.contains(e)),t?i.classList.add(e):i.classList.remove(e)}transform(e,t){(t=t||this).style.webkitTransform=e,t.style.transform=e}translate3d(e,t,i,n){n=n||this,this.transform("translate3d("+e+","+t+","+i+")",n)}arrayDelete(e,t){let i;if(Array.isArray(e)){if(i=e.indexOf(t),i>=0)return e.splice(i,1)}else{if(i=(0,me.U2)(this,e).indexOf(t),i>=0)return this.splice(e,i,1)}return null}_logger(e,t){switch(Array.isArray(t)&&1===t.length&&Array.isArray(t[0])&&(t=t[0]),e){case"log":case"warn":case"error":console[e](...t)}}_log(...e){this._logger("log",e)}_warn(...e){this._logger("warn",e)}_error(...e){this._logger("error",e)}_logf(e,...t){return["[%s::%s]",this.is,e,...t]}}return r.prototype.is="",r}))},67139:(e,t,i)=>{i.d(t,{k:()=>u});var n=i(81096),s=i(74460);const r={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,listeners:!0,hostAttributes:!0},o={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,behaviors:!0,_noAccessors:!0},a=Object.assign({listeners:!0,hostAttributes:!0,properties:!0,observers:!0},o);function l(e,t,i,n){!function(e,t,i){const n=e._noAccessors,s=Object.getOwnPropertyNames(e);for(let r=0;r<s.length;r++){let o=s[r];if(!(o in i))if(n)t[o]=e[o];else{let i=Object.getOwnPropertyDescriptor(e,o);i&&(i.configurable=!0,Object.defineProperty(t,o,i))}}}(t,e,n);for(let s in r)t[s]&&(i[s]=i[s]||[],i[s].push(t[s]))}function c(e,t,i){t=t||[];for(let n=e.length-1;n>=0;n--){let s=e[n];s?Array.isArray(s)?c(s,t):t.indexOf(s)<0&&(!i||i.indexOf(s)<0)&&t.unshift(s):console.warn("behavior is null, check for missing or 404 import")}return t}function d(e,t){for(const i in t){const n=e[i],s=t[i];e[i]=!("value"in s)&&n&&"value"in n?Object.assign({value:n.value},s):s}}const h=(0,n.x)(HTMLElement);function p(e,t,i){let n;const r={};class h extends t{static _finalizeClass(){if(this.hasOwnProperty(JSCompiler_renameProperty("generatedFrom",this))){if(n)for(let e,t=0;t<n.length;t++)e=n[t],e.properties&&this.createProperties(e.properties),e.observers&&this.createObservers(e.observers,e.properties);e.properties&&this.createProperties(e.properties),e.observers&&this.createObservers(e.observers,e.properties),this._prepareTemplate()}else t._finalizeClass.call(this)}static get properties(){const t={};if(n)for(let e=0;e<n.length;e++)d(t,n[e].properties);return d(t,e.properties),t}static get observers(){let t=[];if(n)for(let e,i=0;i<n.length;i++)e=n[i],e.observers&&(t=t.concat(e.observers));return e.observers&&(t=t.concat(e.observers)),t}created(){super.created();const e=r.created;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}_registered(){const e=h.prototype;if(!e.hasOwnProperty(JSCompiler_renameProperty("__hasRegisterFinished",e))){const t=Object.getPrototypeOf(this);t===e&&(e.__hasRegisterFinished=!0),super._registered(),s.nL&&!Object.hasOwnProperty(e,"__hasCopiedProperties")&&(e.__hasCopiedProperties=!0,p(e));let i=r.beforeRegister;if(i)for(let e=0;e<i.length;e++)i[e].call(t);if(i=r.registered,i)for(let e=0;e<i.length;e++)i[e].call(t)}}_applyListeners(){super._applyListeners();const e=r.listeners;if(e)for(let t=0;t<e.length;t++){const i=e[t];if(i)for(let e in i)this._addMethodEventListenerToNode(this,e,i[e])}}_ensureAttributes(){const e=r.hostAttributes;if(e)for(let t=e.length-1;t>=0;t--){const i=e[t];for(let e in i)this._ensureAttribute(e,i[e])}super._ensureAttributes()}ready(){super.ready();let e=r.ready;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}attached(){super.attached();let e=r.attached;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}detached(){super.detached();let e=r.detached;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}attributeChanged(e,t,i){super.attributeChanged();let n=r.attributeChanged;if(n)for(let s=0;s<n.length;s++)n[s].call(this,e,t,i)}}if(i){Array.isArray(i)||(i=[i]);let e=t.prototype.behaviors;n=c(i,null,e),h.prototype.behaviors=e?e.concat(i):n}const p=t=>{n&&function(e,t,i){for(let n=0;n<t.length;n++)l(e,t[n],i,a)}(t,n,r),l(t,e,r,o)};return s.nL||p(h.prototype),h.generatedFrom=e,h}i(56646);const u=function(e){let t;return t="function"==typeof e?e:u.Class(e),e._legacyForceObservedAttributes&&(t.prototype._legacyForceObservedAttributes=e._legacyForceObservedAttributes),customElements.define(t.is,t),t};u.Class=function(e,t){e||console.warn("Polymer.Class requires `info` argument");let i=t?t(h):h;return i=p(e,i,e.behaviors),i.is=i.prototype.is=e.is,i}},18149:(e,t,i)=>{i.d(t,{vz:()=>_,Ku:()=>d});i(56646);var n=i(62276),s=(i(74460),i(4507)),r=i(21683);function o(e){return"slot"===e.localName}let a=class{static getFlattenedNodes(e){const t=(0,n.r)(e);return o(e)?t.assignedNodes({flatten:!0}):Array.from(t.childNodes).map((e=>o(e)?(0,n.r)(e).assignedNodes({flatten:!0}):[e])).reduce(((e,t)=>e.concat(t)),[])}constructor(e,t){this._shadyChildrenObserver=null,this._nativeChildrenObserver=null,this._connected=!1,this._target=e,this.callback=t,this._effectiveNodes=[],this._observer=null,this._scheduled=!1,this._boundSchedule=()=>{this._schedule()},this.connect(),this._schedule()}connect(){o(this._target)?this._listenSlots([this._target]):(0,n.r)(this._target).children&&(this._listenSlots((0,n.r)(this._target).children),window.ShadyDOM?this._shadyChildrenObserver=window.ShadyDOM.observeChildren(this._target,(e=>{this._processMutations(e)})):(this._nativeChildrenObserver=new MutationObserver((e=>{this._processMutations(e)})),this._nativeChildrenObserver.observe(this._target,{childList:!0}))),this._connected=!0}disconnect(){o(this._target)?this._unlistenSlots([this._target]):(0,n.r)(this._target).children&&(this._unlistenSlots((0,n.r)(this._target).children),window.ShadyDOM&&this._shadyChildrenObserver?(window.ShadyDOM.unobserveChildren(this._shadyChildrenObserver),this._shadyChildrenObserver=null):this._nativeChildrenObserver&&(this._nativeChildrenObserver.disconnect(),this._nativeChildrenObserver=null)),this._connected=!1}_schedule(){this._scheduled||(this._scheduled=!0,r.YA.run((()=>this.flush())))}_processMutations(e){this._processSlotMutations(e),this.flush()}_processSlotMutations(e){if(e)for(let t=0;t<e.length;t++){let i=e[t];i.addedNodes&&this._listenSlots(i.addedNodes),i.removedNodes&&this._unlistenSlots(i.removedNodes)}}flush(){if(!this._connected)return!1;window.ShadyDOM&&ShadyDOM.flush(),this._nativeChildrenObserver?this._processSlotMutations(this._nativeChildrenObserver.takeRecords()):this._shadyChildrenObserver&&this._processSlotMutations(this._shadyChildrenObserver.takeRecords()),this._scheduled=!1;let e={target:this._target,addedNodes:[],removedNodes:[]},t=this.constructor.getFlattenedNodes(this._target),i=(0,s.c)(t,this._effectiveNodes);for(let s,r=0;r<i.length&&(s=i[r]);r++)for(let t,i=0;i<s.removed.length&&(t=s.removed[i]);i++)e.removedNodes.push(t);for(let s,r=0;r<i.length&&(s=i[r]);r++)for(let i=s.index;i<s.index+s.addedCount;i++)e.addedNodes.push(t[i]);this._effectiveNodes=t;let n=!1;return(e.addedNodes.length||e.removedNodes.length)&&(n=!0,this.callback.call(this._target,e)),n}_listenSlots(e){for(let t=0;t<e.length;t++){let i=e[t];o(i)&&i.addEventListener("slotchange",this._boundSchedule)}}_unlistenSlots(e){for(let t=0;t<e.length;t++){let i=e[t];o(i)&&i.removeEventListener("slotchange",this._boundSchedule)}}};i(93252),i(78956);const l=Element.prototype,c=l.matches||l.matchesSelector||l.mozMatchesSelector||l.msMatchesSelector||l.oMatchesSelector||l.webkitMatchesSelector,d=function(e,t){return c.call(e,t)};class h{constructor(e){window.ShadyDOM&&window.ShadyDOM.inUse&&window.ShadyDOM.patch(e),this.node=e}observeNodes(e){return new a(this.node,e)}unobserveNodes(e){e.disconnect()}notifyObserver(){}deepContains(e){if((0,n.r)(this.node).contains(e))return!0;let t=e,i=e.ownerDocument;for(;t&&t!==i&&t!==this.node;)t=(0,n.r)(t).parentNode||(0,n.r)(t).host;return t===this.node}getOwnerRoot(){return(0,n.r)(this.node).getRootNode()}getDistributedNodes(){return"slot"===this.node.localName?(0,n.r)(this.node).assignedNodes({flatten:!0}):[]}getDestinationInsertionPoints(){let e=[],t=(0,n.r)(this.node).assignedSlot;for(;t;)e.push(t),t=(0,n.r)(t).assignedSlot;return e}importNode(e,t){let i=this.node instanceof Document?this.node:this.node.ownerDocument;return(0,n.r)(i).importNode(e,t)}getEffectiveChildNodes(){return a.getFlattenedNodes(this.node)}queryDistributedElements(e){let t=this.getEffectiveChildNodes(),i=[];for(let n,s=0,r=t.length;s<r&&(n=t[s]);s++)n.nodeType===Node.ELEMENT_NODE&&d(n,e)&&i.push(n);return i}get activeElement(){let e=this.node;return void 0!==e._activeElement?e._activeElement:e.activeElement}}function p(e,t){for(let i=0;i<t.length;i++){let n=t[i];Object.defineProperty(e,n,{get:function(){return this.node[n]},configurable:!0})}}class u{constructor(e){this.event=e}get rootTarget(){return this.path[0]}get localTarget(){return this.event.target}get path(){return this.event.composedPath()}}h.prototype.cloneNode,h.prototype.appendChild,h.prototype.insertBefore,h.prototype.removeChild,h.prototype.replaceChild,h.prototype.setAttribute,h.prototype.removeAttribute,h.prototype.querySelector,h.prototype.querySelectorAll,h.prototype.parentNode,h.prototype.firstChild,h.prototype.lastChild,h.prototype.nextSibling,h.prototype.previousSibling,h.prototype.firstElementChild,h.prototype.lastElementChild,h.prototype.nextElementSibling,h.prototype.previousElementSibling,h.prototype.childNodes,h.prototype.children,h.prototype.classList,h.prototype.textContent,h.prototype.innerHTML;let m=h;if(window.ShadyDOM&&window.ShadyDOM.inUse&&window.ShadyDOM.noPatch&&window.ShadyDOM.Wrapper){class e extends window.ShadyDOM.Wrapper{}Object.getOwnPropertyNames(h.prototype).forEach((t=>{"activeElement"!=t&&(e.prototype[t]=h.prototype[t])})),p(e.prototype,["classList"]),m=e,Object.defineProperties(u.prototype,{localTarget:{get(){const e=this.event.currentTarget,t=e&&_(e).getOwnerRoot(),i=this.path;for(let n=0;n<i.length;n++){const e=i[n];if(_(e).getOwnerRoot()===t)return e}},configurable:!0},path:{get(){return window.ShadyDOM.composedPath(this.event)},configurable:!0}})}else!function(e,t){for(let i=0;i<t.length;i++){let n=t[i];e[n]=function(){return this.node[n].apply(this.node,arguments)}}}(h.prototype,["cloneNode","appendChild","insertBefore","removeChild","replaceChild","setAttribute","removeAttribute","querySelector","querySelectorAll","attachShadow"]),p(h.prototype,["parentNode","firstChild","lastChild","nextSibling","previousSibling","firstElementChild","lastElementChild","nextElementSibling","previousElementSibling","childNodes","children","classList","shadowRoot"]),function(e,t){for(let i=0;i<t.length;i++){let n=t[i];Object.defineProperty(e,n,{get:function(){return this.node[n]},set:function(e){this.node[n]=e},configurable:!0})}}(h.prototype,["textContent","innerHTML","className"]);const _=function(e){if((e=e||document)instanceof m)return e;if(e instanceof u)return e;let t=e.__domApi;return t||(t=e instanceof Event?new u(e):new m(e),e.__domApi=t),t}},60995:(e,t,i)=>{i.d(t,{_:()=>r});i(56646);var n=i(76389),s=i(81668);const r=(0,n.o)((e=>class extends e{_addEventListenerToNode(e,t,i){(0,s.NH)(e,t,i)||super._addEventListenerToNode(e,t,i)}_removeEventListenerFromNode(e,t,i){(0,s.ys)(e,t,i)||super._removeEventListenerFromNode(e,t,i)}}))},4507:(e,t,i)=>{i.d(t,{c:()=>c});i(56646);function n(e,t,i){return{index:e,removed:t,addedCount:i}}const s=0,r=1,o=2,a=3;function l(e,t,i,l,c,h){let p,u=0,m=0,_=Math.min(i-t,h-c);if(0==t&&0==c&&(u=function(e,t,i){for(let n=0;n<i;n++)if(!d(e[n],t[n]))return n;return i}(e,l,_)),i==e.length&&h==l.length&&(m=function(e,t,i){let n=e.length,s=t.length,r=0;for(;r<i&&d(e[--n],t[--s]);)r++;return r}(e,l,_-u)),c+=u,h-=m,(i-=m)-(t+=u)==0&&h-c==0)return[];if(t==i){for(p=n(t,[],0);c<h;)p.removed.push(l[c++]);return[p]}if(c==h)return[n(t,[],i-t)];let f=function(e){let t=e.length-1,i=e[0].length-1,n=e[t][i],l=[];for(;t>0||i>0;){if(0==t){l.push(o),i--;continue}if(0==i){l.push(a),t--;continue}let c,d=e[t-1][i-1],h=e[t-1][i],p=e[t][i-1];c=h<p?h<d?h:d:p<d?p:d,c==d?(d==n?l.push(s):(l.push(r),n=d),t--,i--):c==h?(l.push(a),t--,n=h):(l.push(o),i--,n=p)}return l.reverse(),l}(function(e,t,i,n,s,r){let o=r-s+1,a=i-t+1,l=new Array(o);for(let c=0;c<o;c++)l[c]=new Array(a),l[c][0]=c;for(let c=0;c<a;c++)l[0][c]=c;for(let c=1;c<o;c++)for(let i=1;i<a;i++)if(d(e[t+i-1],n[s+c-1]))l[c][i]=l[c-1][i-1];else{let e=l[c-1][i]+1,t=l[c][i-1]+1;l[c][i]=e<t?e:t}return l}(e,t,i,l,c,h));p=void 0;let y=[],g=t,b=c;for(let d=0;d<f.length;d++)switch(f[d]){case s:p&&(y.push(p),p=void 0),g++,b++;break;case r:p||(p=n(g,[],0)),p.addedCount++,g++,p.removed.push(l[b]),b++;break;case o:p||(p=n(g,[],0)),p.addedCount++,g++;break;case a:p||(p=n(g,[],0)),p.removed.push(l[b]),b++}return p&&y.push(p),y}function c(e,t){return l(e,0,e.length,t,0,t.length)}function d(e,t){return e===t}},78956:(e,t,i)=>{i.d(t,{Ex:()=>r,Jk:()=>o,dx:()=>n});i(56646),i(76389),i(21683);class n{constructor(){this._asyncModule=null,this._callback=null,this._timer=null}setConfig(e,t){this._asyncModule=e,this._callback=t,this._timer=this._asyncModule.run((()=>{this._timer=null,s.delete(this),this._callback()}))}cancel(){this.isActive()&&(this._cancelAsync(),s.delete(this))}_cancelAsync(){this.isActive()&&(this._asyncModule.cancel(this._timer),this._timer=null)}flush(){this.isActive()&&(this.cancel(),this._callback())}isActive(){return null!=this._timer}static debounce(e,t,i){return e instanceof n?e._cancelAsync():e=new n,e.setConfig(t,i),e}}let s=new Set;const r=function(e){s.add(e)},o=function(){const e=Boolean(s.size);return s.forEach((e=>{try{e.flush()}catch(t){setTimeout((()=>{throw t}))}})),e}},93252:(e,t,i)=>{i.d(t,{E:()=>n.Ex,y:()=>s});i(56646);var n=i(78956);const s=function(){let e,t;do{e=window.ShadyDOM&&ShadyDOM.flush(),window.ShadyCSS&&window.ShadyCSS.ScopingShim&&window.ShadyCSS.ScopingShim.flush(),t=(0,n.Jk)()}while(e||t)}},81668:(e,t,i)=>{i.d(t,{BP:()=>L,NH:()=>D,ys:()=>M});i(56646);var n=i(21683),s=i(78956),r=i(74460),o=i(62276);let a="string"==typeof document.head.style.touchAction,l="__polymerGestures",c="__polymerGesturesHandled",d="__polymerGesturesTouchAction",h=["mousedown","mousemove","mouseup","click"],p=[0,1,4,2],u=function(){try{return 1===new MouseEvent("test",{buttons:1}).buttons}catch(e){return!1}}();function m(e){return h.indexOf(e)>-1}let _=!1;function f(e){if(!m(e)&&"touchend"!==e)return a&&_&&r.f6?{passive:!0}:void 0}!function(){try{let e=Object.defineProperty({},"passive",{get(){_=!0}});window.addEventListener("test",null,e),window.removeEventListener("test",null,e)}catch(e){}}();let y=navigator.userAgent.match(/iP(?:[oa]d|hone)|Android/);const g=[],b={button:!0,input:!0,keygen:!0,meter:!0,output:!0,textarea:!0,progress:!0,select:!0},v={button:!0,command:!0,fieldset:!0,input:!0,keygen:!0,optgroup:!0,option:!0,select:!0,textarea:!0};function w(e){let t=Array.prototype.slice.call(e.labels||[]);if(!t.length){t=[];try{let i=e.getRootNode();if(e.id){let n=i.querySelectorAll(`label[for = '${e.id}']`);for(let e=0;e<n.length;e++)t.push(n[e])}}catch(i){}}return t}let x=function(e){let t=e.sourceCapabilities;var i;if((!t||t.firesTouchEvents)&&(e[c]={skip:!0},"click"===e.type)){let t=!1,n=A(e);for(let e=0;e<n.length;e++){if(n[e].nodeType===Node.ELEMENT_NODE)if("label"===n[e].localName)g.push(n[e]);else if(i=n[e],b[i.localName]){let i=w(n[e]);for(let e=0;e<i.length;e++)t=t||g.indexOf(i[e])>-1}if(n[e]===k.mouse.target)return}if(t)return;e.preventDefault(),e.stopPropagation()}};function C(e){let t=y?["click"]:h;for(let i,n=0;n<t.length;n++)i=t[n],e?(g.length=0,document.addEventListener(i,x,!0)):document.removeEventListener(i,x,!0)}function S(e){let t=e.type;if(!m(t))return!1;if("mousemove"===t){let t=void 0===e.buttons?1:e.buttons;return e instanceof window.MouseEvent&&!u&&(t=p[e.which]||0),Boolean(1&t)}return 0===(void 0===e.button?0:e.button)}let k={mouse:{target:null,mouseIgnoreJob:null},touch:{x:0,y:0,id:-1,scrollDecided:!1}};function E(e,t,i){e.movefn=t,e.upfn=i,document.addEventListener("mousemove",t),document.addEventListener("mouseup",i)}function P(e){document.removeEventListener("mousemove",e.movefn),document.removeEventListener("mouseup",e.upfn),e.movefn=null,e.upfn=null}r.z2&&document.addEventListener("touchend",(function(e){if(!r.z2)return;k.mouse.mouseIgnoreJob||C(!0),k.mouse.target=A(e)[0],k.mouse.mouseIgnoreJob=s.dx.debounce(k.mouse.mouseIgnoreJob,n.Wc.after(2500),(function(){C(),k.mouse.target=null,k.mouse.mouseIgnoreJob=null}))}),!!_&&{passive:!0});const A=window.ShadyDOM&&window.ShadyDOM.noPatch?window.ShadyDOM.composedPath:e=>e.composedPath&&e.composedPath()||[],O={},T=[];function I(e){const t=A(e);return t.length>0?t[0]:e.target}function N(e){let t,i=e.type,n=e.currentTarget[l];if(!n)return;let s=n[i];if(s){if(!e[c]&&(e[c]={},"touch"===i.slice(0,5))){let t=e.changedTouches[0];if("touchstart"===i&&1===e.touches.length&&(k.touch.id=t.identifier),k.touch.id!==t.identifier)return;a||"touchstart"!==i&&"touchmove"!==i||function(e){let t=e.changedTouches[0],i=e.type;if("touchstart"===i)k.touch.x=t.clientX,k.touch.y=t.clientY,k.touch.scrollDecided=!1;else if("touchmove"===i){if(k.touch.scrollDecided)return;k.touch.scrollDecided=!0;let i=function(e){let t="auto",i=A(e);for(let n,s=0;s<i.length;s++)if(n=i[s],n[d]){t=n[d];break}return t}(e),n=!1,s=Math.abs(k.touch.x-t.clientX),r=Math.abs(k.touch.y-t.clientY);e.cancelable&&("none"===i?n=!0:"pan-x"===i?n=r>s:"pan-y"===i&&(n=s>r)),n?e.preventDefault():B("track")}}(e)}if(t=e[c],!t.skip){for(let i,n=0;n<T.length;n++)i=T[n],s[i.name]&&!t[i.name]&&i.flow&&i.flow.start.indexOf(e.type)>-1&&i.reset&&i.reset();for(let n,r=0;r<T.length;r++)n=T[r],s[n.name]&&!t[n.name]&&(t[n.name]=!0,n[i](e))}}}function D(e,t,i){return!!O[t]&&(function(e,t,i){let n=O[t],s=n.deps,r=n.name,o=e[l];o||(e[l]=o={});for(let a,l,c=0;c<s.length;c++)a=s[c],y&&m(a)&&"click"!==a||(l=o[a],l||(o[a]=l={_count:0}),0===l._count&&e.addEventListener(a,N,f(a)),l[r]=(l[r]||0)+1,l._count=(l._count||0)+1);e.addEventListener(t,i),n.touchAction&&L(e,n.touchAction)}(e,t,i),!0)}function M(e,t,i){return!!O[t]&&(function(e,t,i){let n=O[t],s=n.deps,r=n.name,o=e[l];if(o)for(let a,l,c=0;c<s.length;c++)a=s[c],l=o[a],l&&l[r]&&(l[r]=(l[r]||1)-1,l._count=(l._count||1)-1,0===l._count&&e.removeEventListener(a,N,f(a)));e.removeEventListener(t,i)}(e,t,i),!0)}function R(e){T.push(e);for(let t=0;t<e.emits.length;t++)O[e.emits[t]]=e}function L(e,t){a&&e instanceof HTMLElement&&n.YA.run((()=>{e.style.touchAction=t})),e[d]=t}function H(e,t,i){let n=new Event(t,{bubbles:!0,cancelable:!0,composed:!0});if(n.detail=i,(0,o.r)(e).dispatchEvent(n),n.defaultPrevented){let e=i.preventer||i.sourceEvent;e&&e.preventDefault&&e.preventDefault()}}function B(e){let t=function(e){for(let t,i=0;i<T.length;i++){t=T[i];for(let i,n=0;n<t.emits.length;n++)if(i=t.emits[n],i===e)return t}return null}(e);t.info&&(t.info.prevent=!0)}function F(e,t,i,n){t&&H(t,e,{x:i.clientX,y:i.clientY,sourceEvent:i,preventer:n,prevent:function(e){return B(e)}})}function z(e,t,i){if(e.prevent)return!1;if(e.started)return!0;let n=Math.abs(e.x-t),s=Math.abs(e.y-i);return n>=5||s>=5}function j(e,t,i){if(!t)return;let n,s=e.moves[e.moves.length-2],r=e.moves[e.moves.length-1],o=r.x-e.x,a=r.y-e.y,l=0;s&&(n=r.x-s.x,l=r.y-s.y),H(t,"track",{state:e.state,x:i.clientX,y:i.clientY,dx:o,dy:a,ddx:n,ddy:l,sourceEvent:i,hover:function(){return function(e,t){let i=document.elementFromPoint(e,t),n=i;for(;n&&n.shadowRoot&&!window.ShadyDOM;){let s=n;if(n=n.shadowRoot.elementFromPoint(e,t),s===n)break;n&&(i=n)}return i}(i.clientX,i.clientY)}})}function K(e,t,i){let n=Math.abs(t.clientX-e.x),s=Math.abs(t.clientY-e.y),r=I(i||t);!r||v[r.localName]&&r.hasAttribute("disabled")||(isNaN(n)||isNaN(s)||n<=25&&s<=25||function(e){if("click"===e.type){if(0===e.detail)return!0;let t=I(e);if(!t.nodeType||t.nodeType!==Node.ELEMENT_NODE)return!0;let i=t.getBoundingClientRect(),n=e.pageX,s=e.pageY;return!(n>=i.left&&n<=i.right&&s>=i.top&&s<=i.bottom)}return!1}(t))&&(e.prevent||H(r,"tap",{x:t.clientX,y:t.clientY,sourceEvent:t,preventer:i}))}R({name:"downup",deps:["mousedown","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["down","up"],info:{movefn:null,upfn:null},reset:function(){P(this.info)},mousedown:function(e){if(!S(e))return;let t=I(e),i=this;E(this.info,(function(e){S(e)||(F("up",t,e),P(i.info))}),(function(e){S(e)&&F("up",t,e),P(i.info)})),F("down",t,e)},touchstart:function(e){F("down",I(e),e.changedTouches[0],e)},touchend:function(e){F("up",I(e),e.changedTouches[0],e)}}),R({name:"track",touchAction:"none",deps:["mousedown","touchstart","touchmove","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["track"],info:{x:0,y:0,state:"start",started:!1,moves:[],addMove:function(e){this.moves.length>2&&this.moves.shift(),this.moves.push(e)},movefn:null,upfn:null,prevent:!1},reset:function(){this.info.state="start",this.info.started=!1,this.info.moves=[],this.info.x=0,this.info.y=0,this.info.prevent=!1,P(this.info)},mousedown:function(e){if(!S(e))return;let t=I(e),i=this,n=function(e){let n=e.clientX,s=e.clientY;z(i.info,n,s)&&(i.info.state=i.info.started?"mouseup"===e.type?"end":"track":"start","start"===i.info.state&&B("tap"),i.info.addMove({x:n,y:s}),S(e)||(i.info.state="end",P(i.info)),t&&j(i.info,t,e),i.info.started=!0)};E(this.info,n,(function(e){i.info.started&&n(e),P(i.info)})),this.info.x=e.clientX,this.info.y=e.clientY},touchstart:function(e){let t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchmove:function(e){let t=I(e),i=e.changedTouches[0],n=i.clientX,s=i.clientY;z(this.info,n,s)&&("start"===this.info.state&&B("tap"),this.info.addMove({x:n,y:s}),j(this.info,t,i),this.info.state="track",this.info.started=!0)},touchend:function(e){let t=I(e),i=e.changedTouches[0];this.info.started&&(this.info.state="end",this.info.addMove({x:i.clientX,y:i.clientY}),j(this.info,t,i))}}),R({name:"tap",deps:["mousedown","click","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["click","touchend"]},emits:["tap"],info:{x:NaN,y:NaN,prevent:!1},reset:function(){this.info.x=NaN,this.info.y=NaN,this.info.prevent=!1},mousedown:function(e){S(e)&&(this.info.x=e.clientX,this.info.y=e.clientY)},click:function(e){S(e)&&K(this.info,e)},touchstart:function(e){const t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchend:function(e){K(this.info,e.changedTouches[0],e)}})},12249:(e,t,i)=>{var n=i(81096),s=(i(67139),i(56646),i(40729)),r=i(76389);function o(e,t,i,n,s){let r;s&&(r="object"==typeof i&&null!==i,r&&(n=e.__dataTemp[t]));let o=n!==i&&(n==n||i==i);return r&&o&&(e.__dataTemp[t]=i),o}const a=(0,r.o)((e=>class extends e{_shouldPropertyChange(e,t,i){return o(this,e,t,i,!0)}})),l=(0,r.o)((e=>class extends e{static get properties(){return{mutableData:Boolean}}_shouldPropertyChange(e,t,i){return o(this,e,t,i,this.mutableData)}}));a._mutablePropertyChange=o;var c=i(74460),d=i(62276);let h=null;function p(){return h}p.prototype=Object.create(HTMLTemplateElement.prototype,{constructor:{value:p,writable:!0}});const u=(0,s.q)(p),m=a(u);const _=(0,s.q)(class{});function f(e,t){for(let i=0;i<t.length;i++){let n=t[i];if(Boolean(e)!=Boolean(n.__hideTemplateChildren__))if(n.nodeType===Node.TEXT_NODE)e?(n.__polymerTextContent__=n.textContent,n.textContent=""):n.textContent=n.__polymerTextContent__;else if("slot"===n.localName)if(e)n.__polymerReplaced__=document.createComment("hidden-slot"),(0,d.r)((0,d.r)(n).parentNode).replaceChild(n.__polymerReplaced__,n);else{const e=n.__polymerReplaced__;e&&(0,d.r)((0,d.r)(e).parentNode).replaceChild(n,e)}else n.style&&(e?(n.__polymerDisplay__=n.style.display,n.style.display="none"):n.style.display=n.__polymerDisplay__);n.__hideTemplateChildren__=e,n._showHideChildren&&n._showHideChildren(e)}}class y extends _{constructor(e){super(),this._configureProperties(e),this.root=this._stampTemplate(this.__dataHost);let t=[];this.children=t;for(let n=this.root.firstChild;n;n=n.nextSibling)t.push(n),n.__templatizeInstance=this;this.__templatizeOwner&&this.__templatizeOwner.__hideTemplateChildren__&&this._showHideChildren(!0);let i=this.__templatizeOptions;(e&&i.instanceProps||!i.instanceProps)&&this._enableProperties()}_configureProperties(e){if(this.__templatizeOptions.forwardHostProp)for(let t in this.__hostProps)this._setPendingProperty(t,this.__dataHost["_host_"+t]);for(let t in e)this._setPendingProperty(t,e[t])}forwardHostProp(e,t){this._setPendingPropertyOrPath(e,t,!1,!0)&&this.__dataHost._enqueueClient(this)}_addEventListenerToNode(e,t,i){if(this._methodHost&&this.__templatizeOptions.parentModel)this._methodHost._addEventListenerToNode(e,t,(e=>{e.model=this,i(e)}));else{let n=this.__dataHost.__dataHost;n&&n._addEventListenerToNode(e,t,i)}}_showHideChildren(e){f(e,this.children)}_setUnmanagedPropertyToNode(e,t,i){e.__hideTemplateChildren__&&e.nodeType==Node.TEXT_NODE&&"textContent"==t?e.__polymerTextContent__=i:super._setUnmanagedPropertyToNode(e,t,i)}get parentModel(){let e=this.__parentModel;if(!e){let t;e=this;do{e=e.__dataHost.__dataHost}while((t=e.__templatizeOptions)&&!t.parentModel);this.__parentModel=e}return e}dispatchEvent(e){return!0}}y.prototype.__dataHost,y.prototype.__templatizeOptions,y.prototype._methodHost,y.prototype.__templatizeOwner,y.prototype.__hostProps;const g=a(y);function b(e){let t=e.__dataHost;return t&&t._methodHost||t}function v(e,t,i){let n=i.mutableData?g:y;S.mixin&&(n=S.mixin(n));let s=class extends n{};return s.prototype.__templatizeOptions=i,s.prototype._bindTemplate(e),function(e,t,i,n){let s=i.hostProps||{};for(let r in n.instanceProps){delete s[r];let t=n.notifyInstanceProp;t&&e.prototype._addPropertyEffect(r,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:C(r,t)})}if(n.forwardHostProp&&t.__dataHost)for(let r in s)i.hasHostProps||(i.hasHostProps=!0),e.prototype._addPropertyEffect(r,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:function(e,t,i){e.__dataHost._setPendingPropertyOrPath("_host_"+t,i[t],!0,!0)}})}(s,e,t,i),s}function w(e,t,i,n){let s=i.forwardHostProp;if(s&&t.hasHostProps){const a="template"==e.localName;let l=t.templatizeTemplateClass;if(!l){if(a){let e=i.mutableData?m:u;class n extends e{}l=t.templatizeTemplateClass=n}else{const i=e.constructor;class n extends i{}l=t.templatizeTemplateClass=n}let r=t.hostProps;for(let e in r)l.prototype._addPropertyEffect("_host_"+e,l.prototype.PROPERTY_EFFECT_TYPES.PROPAGATE,{fn:x(e,s)}),l.prototype._createNotifyingProperty("_host_"+e);c.a2&&n&&function(e,t,i){const n=i.constructor._properties,{propertyEffects:s}=e,{instanceProps:r}=t;for(let o in s)if(!(n[o]||r&&r[o])){const e=s[o];for(let t=0;t<e.length;t++){const{part:i}=e[t].info;if(!i.signature||!i.signature.static){console.warn(`Property '${o}' used in template but not declared in 'properties'; attribute will not be observed.`);break}}}}(t,i,n)}if(e.__dataProto&&Object.assign(e.__data,e.__dataProto),a)o=l,h=r=e,Object.setPrototypeOf(r,o.prototype),new o,h=null,e.__dataTemp={},e.__dataPending=null,e.__dataOld=null,e._enableProperties();else{Object.setPrototypeOf(e,l.prototype);const i=t.hostProps;for(let t in i)if(t="_host_"+t,t in e){const i=e[t];delete e[t],e.__data[t]=i}}}var r,o}function x(e,t){return function(e,i,n){t.call(e.__templatizeOwner,i.substring(6),n[i])}}function C(e,t){return function(e,i,n){t.call(e.__templatizeOwner,e,i,n[i])}}function S(e,t,i){if(c.XN&&!b(e))throw new Error("strictTemplatePolicy: template owner not trusted");if(i=i||{},e.__templatizeOwner)throw new Error("A <template> can only be templatized once");e.__templatizeOwner=t;let n=(t?t.constructor:y)._parseTemplate(e),s=n.templatizeInstanceClass;s||(s=v(e,n,i),n.templatizeInstanceClass=s);const r=b(e);w(e,n,i,r);let o=class extends s{};return o.prototype._methodHost=r,o.prototype.__dataHost=e,o.prototype.__templatizeOwner=t,o.prototype.__hostProps=n.hostProps,o}function k(e,t){let i;for(;t;)if(i=t.__dataHost?t:t.__templatizeInstance){if(i.__dataHost==e)return i;t=i.__dataHost}else t=(0,d.r)(t).parentNode;return null}var E=i(60995);let P=!1;function A(){if(c.nL&&!c.my){if(!P){P=!0;const e=document.createElement("style");e.textContent="dom-bind,dom-if,dom-repeat{display:none;}",document.head.appendChild(e)}return!0}return!1}const O=(0,E._)(l((0,s.q)(HTMLElement)));customElements.define("dom-bind",class extends O{static get observedAttributes(){return["mutable-data"]}constructor(){if(super(),c.XN)throw new Error("strictTemplatePolicy: dom-bind not allowed");this.root=null,this.$=null,this.__children=null}attributeChangedCallback(e,t,i,n){this.mutableData=!0}connectedCallback(){A()||(this.style.display="none"),this.render()}disconnectedCallback(){this.__removeChildren()}__insertChildren(){(0,d.r)((0,d.r)(this).parentNode).insertBefore(this.root,this)}__removeChildren(){if(this.__children)for(let e=0;e<this.__children.length;e++)this.root.appendChild(this.__children[e])}render(){let e;if(!this.__children){if(e=e||this.querySelector("template"),!e){let t=new MutationObserver((()=>{if(e=this.querySelector("template"),!e)throw new Error("dom-bind requires a <template> child");t.disconnect(),this.render()}));return void t.observe(this,{childList:!0})}this.root=this._stampTemplate(e),this.$=this.root.$,this.__children=[];for(let e=this.root.firstChild;e;e=e.nextSibling)this.__children[this.__children.length]=e;this._enableProperties()}this.__insertChildren(),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}});var T=i(28426),I=i(78956),N=i(93252),D=i(4059),M=i(21683);const R=l(T.H3);class L extends R{static get is(){return"dom-repeat"}static get template(){return null}static get properties(){return{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},itemsIndexAs:{type:String,value:"itemsIndex"},sort:{type:Function,observer:"__sortChanged"},filter:{type:Function,observer:"__filterChanged"},observe:{type:String,observer:"__observeChanged"},delay:Number,renderedItemCount:{type:Number,notify:!c.dJ,readOnly:!0},initialCount:{type:Number},targetFramerate:{type:Number,value:20},_targetFrameTime:{type:Number,computed:"__computeFrameTime(targetFramerate)"},notifyDomChange:{type:Boolean},reuseChunkedInstances:{type:Boolean}}}static get observers(){return["__itemsChanged(items.*)"]}constructor(){super(),this.__instances=[],this.__renderDebouncer=null,this.__itemsIdxToInstIdx={},this.__chunkCount=null,this.__renderStartTime=null,this.__itemsArrayChanged=!1,this.__shouldMeasureChunk=!1,this.__shouldContinueChunking=!1,this.__chunkingId=0,this.__sortFn=null,this.__filterFn=null,this.__observePaths=null,this.__ctor=null,this.__isDetached=!0,this.template=null,this._templateInfo}disconnectedCallback(){super.disconnectedCallback(),this.__isDetached=!0;for(let e=0;e<this.__instances.length;e++)this.__detachInstance(e);this.__chunkingId&&cancelAnimationFrame(this.__chunkingId)}connectedCallback(){if(super.connectedCallback(),A()||(this.style.display="none"),this.__isDetached){this.__isDetached=!1;let e=(0,d.r)((0,d.r)(this).parentNode);for(let t=0;t<this.__instances.length;t++)this.__attachInstance(t,e);this.__chunkingId&&this.__render()}}__ensureTemplatized(){if(!this.__ctor){const e=this;let t=this.template=e._templateInfo?e:this.querySelector("template");if(!t){let e=new MutationObserver((()=>{if(!this.querySelector("template"))throw new Error("dom-repeat requires a <template> child");e.disconnect(),this.__render()}));return e.observe(this,{childList:!0}),!1}let i={};i[this.as]=!0,i[this.indexAs]=!0,i[this.itemsIndexAs]=!0,this.__ctor=S(t,this,{mutableData:this.mutableData,parentModel:!0,instanceProps:i,forwardHostProp:function(e,t){let i=this.__instances;for(let n,s=0;s<i.length&&(n=i[s]);s++)n.forwardHostProp(e,t)},notifyInstanceProp:function(e,t,i){if((0,D.wB)(this.as,t)){let n=e[this.itemsIndexAs];t==this.as&&(this.items[n]=i);let s=(0,D.Iu)(this.as,`${JSCompiler_renameProperty("items",this)}.${n}`,t);this.notifyPath(s,i)}}})}return!0}__getMethodHost(){return this.__dataHost._methodHost||this.__dataHost}__functionFromPropertyValue(e){if("string"==typeof e){let t=e,i=this.__getMethodHost();return function(){return i[t].apply(i,arguments)}}return e}__sortChanged(e){this.__sortFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__filterChanged(e){this.__filterFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__computeFrameTime(e){return Math.ceil(1e3/e)}__observeChanged(){this.__observePaths=this.observe&&this.observe.replace(".*",".").split(" ")}__handleObservedPaths(e){if(this.__sortFn||this.__filterFn)if(e){if(this.__observePaths){let t=this.__observePaths;for(let i=0;i<t.length;i++)0===e.indexOf(t[i])&&this.__debounceRender(this.__render,this.delay)}}else this.__debounceRender(this.__render,this.delay)}__itemsChanged(e){this.items&&!Array.isArray(this.items)&&console.warn("dom-repeat expected array for `items`, found",this.items),this.__handleItemPath(e.path,e.value)||("items"===e.path&&(this.__itemsArrayChanged=!0),this.__debounceRender(this.__render))}__debounceRender(e,t=0){this.__renderDebouncer=I.dx.debounce(this.__renderDebouncer,t>0?M.Wc.after(t):M.YA,e.bind(this)),(0,N.E)(this.__renderDebouncer)}render(){this.__debounceRender(this.__render),(0,N.y)()}__render(){if(!this.__ensureTemplatized())return;let e=this.items||[];const t=this.__sortAndFilterItems(e),i=this.__calculateLimit(t.length);this.__updateInstances(e,i,t),this.initialCount&&(this.__shouldMeasureChunk||this.__shouldContinueChunking)&&(cancelAnimationFrame(this.__chunkingId),this.__chunkingId=requestAnimationFrame((()=>{this.__chunkingId=null,this.__continueChunking()}))),this._setRenderedItemCount(this.__instances.length),c.dJ&&!this.notifyDomChange||this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}__sortAndFilterItems(e){let t=new Array(e.length);for(let i=0;i<e.length;i++)t[i]=i;return this.__filterFn&&(t=t.filter(((t,i,n)=>this.__filterFn(e[t],i,n)))),this.__sortFn&&t.sort(((t,i)=>this.__sortFn(e[t],e[i]))),t}__calculateLimit(e){let t=e;const i=this.__instances.length;if(this.initialCount){let n;!this.__chunkCount||this.__itemsArrayChanged&&!this.reuseChunkedInstances?(t=Math.min(e,this.initialCount),n=Math.max(t-i,0),this.__chunkCount=n||1):(n=Math.min(Math.max(e-i,0),this.__chunkCount),t=Math.min(i+n,e)),this.__shouldMeasureChunk=n===this.__chunkCount,this.__shouldContinueChunking=t<e,this.__renderStartTime=performance.now()}return this.__itemsArrayChanged=!1,t}__continueChunking(){if(this.__shouldMeasureChunk){const e=performance.now()-this.__renderStartTime,t=this._targetFrameTime/e;this.__chunkCount=Math.round(this.__chunkCount*t)||1}this.__shouldContinueChunking&&this.__debounceRender(this.__render)}__updateInstances(e,t,i){const n=this.__itemsIdxToInstIdx={};let s;for(s=0;s<t;s++){let t=this.__instances[s],r=i[s],o=e[r];n[r]=s,t?(t._setPendingProperty(this.as,o),t._setPendingProperty(this.indexAs,s),t._setPendingProperty(this.itemsIndexAs,r),t._flushProperties()):this.__insertInstance(o,s,r)}for(let r=this.__instances.length-1;r>=s;r--)this.__detachAndRemoveInstance(r)}__detachInstance(e){let t=this.__instances[e];const i=(0,d.r)(t.root);for(let n=0;n<t.children.length;n++){let e=t.children[n];i.appendChild(e)}return t}__attachInstance(e,t){let i=this.__instances[e];t.insertBefore(i.root,this)}__detachAndRemoveInstance(e){this.__detachInstance(e),this.__instances.splice(e,1)}__stampInstance(e,t,i){let n={};return n[this.as]=e,n[this.indexAs]=t,n[this.itemsIndexAs]=i,new this.__ctor(n)}__insertInstance(e,t,i){const n=this.__stampInstance(e,t,i);let s=this.__instances[t+1],r=s?s.children[0]:this;return(0,d.r)((0,d.r)(this).parentNode).insertBefore(n.root,r),this.__instances[t]=n,n}_showHideChildren(e){for(let t=0;t<this.__instances.length;t++)this.__instances[t]._showHideChildren(e)}__handleItemPath(e,t){let i=e.slice(6),n=i.indexOf("."),s=n<0?i:i.substring(0,n);if(s==parseInt(s,10)){let e=n<0?"":i.substring(n+1);this.__handleObservedPaths(e);let r=this.__itemsIdxToInstIdx[s],o=this.__instances[r];if(o){let i=this.as+(e?"."+e:"");o._setPendingPropertyOrPath(i,t,!1,!0),o._flushProperties()}return!0}}itemForElement(e){let t=this.modelForElement(e);return t&&t[this.as]}indexForElement(e){let t=this.modelForElement(e);return t&&t[this.indexAs]}modelForElement(e){return k(this.template,e)}}customElements.define(L.is,L);class H extends T.H3{static get is(){return"dom-if"}static get template(){return null}static get properties(){return{if:{type:Boolean,observer:"__debounceRender"},restamp:{type:Boolean,observer:"__debounceRender"},notifyDomChange:{type:Boolean}}}constructor(){super(),this.__renderDebouncer=null,this._lastIf=!1,this.__hideTemplateChildren__=!1,this.__template,this._templateInfo}__debounceRender(){this.__renderDebouncer=I.dx.debounce(this.__renderDebouncer,M.YA,(()=>this.__render())),(0,N.E)(this.__renderDebouncer)}disconnectedCallback(){super.disconnectedCallback();const e=(0,d.r)(this).parentNode;e&&(e.nodeType!=Node.DOCUMENT_FRAGMENT_NODE||(0,d.r)(e).host)||this.__teardownInstance()}connectedCallback(){super.connectedCallback(),A()||(this.style.display="none"),this.if&&this.__debounceRender()}__ensureTemplate(){if(!this.__template){const e=this;let t=e._templateInfo?e:(0,d.r)(e).querySelector("template");if(!t){let e=new MutationObserver((()=>{if(!(0,d.r)(this).querySelector("template"))throw new Error("dom-if requires a <template> child");e.disconnect(),this.__render()}));return e.observe(this,{childList:!0}),!1}this.__template=t}return!0}__ensureInstance(){let e=(0,d.r)(this).parentNode;if(this.__hasInstance()){let t=this.__getInstanceNodes();if(t&&t.length){if((0,d.r)(this).previousSibling!==t[t.length-1])for(let i,n=0;n<t.length&&(i=t[n]);n++)(0,d.r)(e).insertBefore(i,this)}}else{if(!e)return!1;if(!this.__ensureTemplate())return!1;this.__createAndInsertInstance(e)}return!0}render(){(0,N.y)()}__render(){if(this.if){if(!this.__ensureInstance())return}else this.restamp&&this.__teardownInstance();this._showHideChildren(),c.dJ&&!this.notifyDomChange||this.if==this._lastIf||(this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this._lastIf=this.if)}__hasInstance(){}__getInstanceNodes(){}__createAndInsertInstance(e){}__teardownInstance(){}_showHideChildren(){}}const B=c.ew?class extends H{constructor(){super(),this.__instance=null,this.__syncInfo=null}__hasInstance(){return Boolean(this.__instance)}__getInstanceNodes(){return this.__instance.templateInfo.childNodes}__createAndInsertInstance(e){const t=this.__dataHost||this;if(c.XN&&!this.__dataHost)throw new Error("strictTemplatePolicy: template owner not trusted");const i=t._bindTemplate(this.__template,!0);i.runEffects=(e,t,i)=>{let n=this.__syncInfo;if(this.if)n&&(this.__syncInfo=null,this._showHideChildren(),t=Object.assign(n.changedProps,t)),e(t,i);else if(this.__instance)if(n||(n=this.__syncInfo={runEffects:e,changedProps:{}}),i)for(const s in t){const e=(0,D.Jz)(s);n.changedProps[e]=this.__dataHost[e]}else Object.assign(n.changedProps,t)},this.__instance=t._stampTemplate(this.__template,i),(0,d.r)(e).insertBefore(this.__instance,this)}__syncHostProperties(){const e=this.__syncInfo;e&&(this.__syncInfo=null,e.runEffects(e.changedProps,!1))}__teardownInstance(){const e=this.__dataHost||this;this.__instance&&(e._removeBoundDom(this.__instance),this.__instance=null,this.__syncInfo=null)}_showHideChildren(){const e=this.__hideTemplateChildren__||!this.if;this.__instance&&Boolean(this.__instance.__hidden)!==e&&(this.__instance.__hidden=e,f(e,this.__instance.templateInfo.childNodes)),e||this.__syncHostProperties()}}:class extends H{constructor(){super(),this.__ctor=null,this.__instance=null,this.__invalidProps=null}__hasInstance(){return Boolean(this.__instance)}__getInstanceNodes(){return this.__instance.children}__createAndInsertInstance(e){this.__ctor||(this.__ctor=S(this.__template,this,{mutableData:!0,forwardHostProp:function(e,t){this.__instance&&(this.if?this.__instance.forwardHostProp(e,t):(this.__invalidProps=this.__invalidProps||Object.create(null),this.__invalidProps[(0,D.Jz)(e)]=!0))}})),this.__instance=new this.__ctor,(0,d.r)(e).insertBefore(this.__instance.root,this)}__teardownInstance(){if(this.__instance){let e=this.__instance.children;if(e&&e.length){let t=(0,d.r)(e[0]).parentNode;if(t){t=(0,d.r)(t);for(let i,n=0;n<e.length&&(i=e[n]);n++)t.removeChild(i)}}this.__invalidProps=null,this.__instance=null}}__syncHostProperties(){let e=this.__invalidProps;if(e){this.__invalidProps=null;for(let t in e)this.__instance._setPendingProperty(t,this.__dataHost[t]);this.__instance._flushProperties()}}_showHideChildren(){const e=this.__hideTemplateChildren__||!this.if;this.__instance&&Boolean(this.__instance.__hidden)!==e&&(this.__instance.__hidden=e,this.__instance._showHideChildren(e)),e||this.__syncHostProperties()}};customElements.define(B.is,B);var F=i(4507),z=i(36608);let j=(0,r.o)((e=>{let t=(0,z.SH)(e);return class extends t{static get properties(){return{items:{type:Array},multi:{type:Boolean,value:!1},selected:{type:Object,notify:!0},selectedItem:{type:Object,notify:!0},toggle:{type:Boolean,value:!1}}}static get observers(){return["__updateSelection(multi, items.*)"]}constructor(){super(),this.__lastItems=null,this.__lastMulti=null,this.__selectedMap=null}__updateSelection(e,t){let i=t.path;if(i==JSCompiler_renameProperty("items",this)){let i=t.base||[],n=this.__lastItems;if(e!==this.__lastMulti&&this.clearSelection(),n){let e=(0,F.c)(i,n);this.__applySplices(e)}this.__lastItems=i,this.__lastMulti=e}else if(t.path==`${JSCompiler_renameProperty("items",this)}.splices`)this.__applySplices(t.value.indexSplices);else{let e=i.slice(`${JSCompiler_renameProperty("items",this)}.`.length),t=parseInt(e,10);e.indexOf(".")<0&&e==t&&this.__deselectChangedIdx(t)}}__applySplices(e){let t=this.__selectedMap;for(let n=0;n<e.length;n++){let i=e[n];t.forEach(((e,n)=>{e<i.index||(e>=i.index+i.removed.length?t.set(n,e+i.addedCount-i.removed.length):t.set(n,-1))}));for(let e=0;e<i.addedCount;e++){let n=i.index+e;t.has(this.items[n])&&t.set(this.items[n],n)}}this.__updateLinks();let i=0;t.forEach(((e,n)=>{e<0?(this.multi?this.splice(JSCompiler_renameProperty("selected",this),i,1):this.selected=this.selectedItem=null,t.delete(n)):i++}))}__updateLinks(){if(this.__dataLinkedPaths={},this.multi){let e=0;this.__selectedMap.forEach((t=>{t>=0&&this.linkPaths(`${JSCompiler_renameProperty("items",this)}.${t}`,`${JSCompiler_renameProperty("selected",this)}.${e++}`)}))}else this.__selectedMap.forEach((e=>{this.linkPaths(JSCompiler_renameProperty("selected",this),`${JSCompiler_renameProperty("items",this)}.${e}`),this.linkPaths(JSCompiler_renameProperty("selectedItem",this),`${JSCompiler_renameProperty("items",this)}.${e}`)}))}clearSelection(){this.__dataLinkedPaths={},this.__selectedMap=new Map,this.selected=this.multi?[]:null,this.selectedItem=null}isSelected(e){return this.__selectedMap.has(e)}isIndexSelected(e){return this.isSelected(this.items[e])}__deselectChangedIdx(e){let t=this.__selectedIndexForItemIndex(e);if(t>=0){let e=0;this.__selectedMap.forEach(((i,n)=>{t==e++&&this.deselect(n)}))}}__selectedIndexForItemIndex(e){let t=this.__dataLinkedPaths[`${JSCompiler_renameProperty("items",this)}.${e}`];if(t)return parseInt(t.slice(`${JSCompiler_renameProperty("selected",this)}.`.length),10)}deselect(e){let t=this.__selectedMap.get(e);if(t>=0){let i;this.__selectedMap.delete(e),this.multi&&(i=this.__selectedIndexForItemIndex(t)),this.__updateLinks(),this.multi?this.splice(JSCompiler_renameProperty("selected",this),i,1):this.selected=this.selectedItem=null}}deselectIndex(e){this.deselect(this.items[e])}select(e){this.selectIndex(this.items.indexOf(e))}selectIndex(e){let t=this.items[e];this.isSelected(t)?this.toggle&&this.deselectIndex(e):(this.multi||this.__selectedMap.clear(),this.__selectedMap.set(t,e),this.__updateLinks(),this.multi?this.push(JSCompiler_renameProperty("selected",this),t):this.selected=this.selectedItem=t)}}}))(T.H3);class K extends j{static get is(){return"array-selector"}static get template(){return null}}customElements.define(K.is,K);var $=i(34816),U=i(10868),q=i(26539);const Y=new $.ZP;window.ShadyCSS||(window.ShadyCSS={prepareTemplate(e,t,i){},prepareTemplateDom(e,t){},prepareTemplateStyles(e,t,i){},styleSubtree(e,t){Y.processStyles(),(0,U.wW)(e,t)},styleElement(e){Y.processStyles()},styleDocument(e){Y.processStyles(),(0,U.wW)(document.body,e)},getComputedStyleValue(e,t){return(0,U.B7)(e,t)},flushCustomStyles(){},nativeCss:q.rd,nativeShadow:q.WA,cssBuild:q.Cp,disableRuntime:q.jF}),window.ShadyCSS.CustomStyleInterface=Y;var X=i(15392);const J="include",W=window.ShadyCSS.CustomStyleInterface;class V extends HTMLElement{constructor(){super(),this._style=null,W.addCustomStyle(this)}getStyle(){if(this._style)return this._style;const e=this.querySelector("style");if(!e)return null;this._style=e;const t=e.getAttribute(J);return t&&(e.removeAttribute(J),e.textContent=(0,X.jv)(t)+e.textContent),this.ownerDocument!==window.document&&window.document.head.appendChild(this),this._style}}let G;window.customElements.define("custom-style",V),G=a._mutablePropertyChange;Boolean;i(50856);(0,n.x)(HTMLElement).prototype},60309:(e,t,i)=>{i.d(t,{$T:()=>s,CN:()=>n,mA:()=>r});const n=/(?:^|[;\s{]\s*)(--[\w-]*?)\s*:\s*(?:((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^)]*?\)|[^};{])+)|\{([^}]*)\}(?:(?=[;\s}])|$))/gi,s=/(?:^|\W+)@apply\s*\(?([^);\n]*)\)?/gi,r=/@media\s(.*)/},10868:(e,t,i)=>{i.d(t,{B7:()=>r,OH:()=>o,wW:()=>s});var n=i(60309);function s(e,t){for(let i in t)null===i?e.style.removeProperty(i):e.style.setProperty(i,t[i])}function r(e,t){const i=window.getComputedStyle(e).getPropertyValue(t);return i?i.trim():""}function o(e){const t=n.$T.test(e)||n.CN.test(e);return n.$T.lastIndex=0,n.CN.lastIndex=0,t}},34816:(e,t,i)=>{i.d(t,{ZP:()=>h});let n,s=null,r=window.HTMLImports&&window.HTMLImports.whenReady||null;function o(e){requestAnimationFrame((function(){r?r(e):(s||(s=new Promise((e=>{n=e})),"complete"===document.readyState?n():document.addEventListener("readystatechange",(()=>{"complete"===document.readyState&&n()}))),s.then((function(){e&&e()})))}))}const a="__seenByShadyCSS",l="__shadyCSSCachedStyle";let c=null,d=null;class h{constructor(){this.customStyles=[],this.enqueued=!1,o((()=>{window.ShadyCSS.flushCustomStyles&&window.ShadyCSS.flushCustomStyles()}))}enqueueDocumentValidation(){!this.enqueued&&d&&(this.enqueued=!0,o(d))}addCustomStyle(e){e[a]||(e[a]=!0,this.customStyles.push(e),this.enqueueDocumentValidation())}getStyleForCustomStyle(e){if(e[l])return e[l];let t;return t=e.getStyle?e.getStyle():e,t}processStyles(){const e=this.customStyles;for(let t=0;t<e.length;t++){const i=e[t];if(i[l])continue;const n=this.getStyleForCustomStyle(i);if(n){const e=n.__appliedElement||n;c&&c(e),i[l]=e}}return e}}h.prototype.addCustomStyle=h.prototype.addCustomStyle,h.prototype.getStyleForCustomStyle=h.prototype.getStyleForCustomStyle,h.prototype.processStyles=h.prototype.processStyles,Object.defineProperties(h.prototype,{transformCallback:{get(){return c},set(e){c=e}},validateCallback:{get(){return d},set(e){let t=!1;d||(t=!0),d=e,t&&this.enqueueDocumentValidation()}}})},26539:(e,t,i)=>{i.d(t,{Cp:()=>r,WA:()=>n,jF:()=>a,rd:()=>l});const n=!(window.ShadyDOM&&window.ShadyDOM.inUse);let s,r;function o(e){s=(!e||!e.shimcssproperties)&&(n||Boolean(!navigator.userAgent.match(/AppleWebKit\/601|Edge\/15/)&&window.CSS&&CSS.supports&&CSS.supports("box-shadow","0 0 0 var(--foo)")))}window.ShadyCSS&&void 0!==window.ShadyCSS.cssBuild&&(r=window.ShadyCSS.cssBuild);const a=Boolean(window.ShadyCSS&&window.ShadyCSS.disableRuntime);window.ShadyCSS&&void 0!==window.ShadyCSS.nativeCss?s=window.ShadyCSS.nativeCss:window.ShadyCSS?(o(window.ShadyCSS),window.ShadyCSS=void 0):o(window.WebComponents&&window.WebComponents.flags);const l=s},45666:(e,t,i)=>{i.d(t,{B:()=>r});const n=e=>{let t=[];function i(i,n){e=n?i:Object.assign(Object.assign({},e),i);let s=t;for(let t=0;t<s.length;t++)s[t](e)}return{get state(){return e},action(t){function n(e){i(e,!1)}return function(){let i=[e];for(let e=0;e<arguments.length;e++)i.push(arguments[e]);let s=t.apply(this,i);if(null!=s)return s instanceof Promise?s.then(n):n(s)}},setState:i,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let i=[];for(let n=0;n<t.length;n++)t[n]===e?e=null:i.push(t[n]);t=i}(e)}}}},s=(e,t,i,s,r={unsubGrace:!0})=>{if(e[t])return e[t];let o,a,l=0,c=n();const d=()=>{if(!i)throw new Error("Collection does not support refresh");return i(e).then((e=>c.setState(e,!0)))},h=()=>d().catch((t=>{if(e.connected)throw t})),p=()=>{a=void 0,o&&o.then((e=>{e()})),c.clearState(),e.removeEventListener("ready",d),e.removeEventListener("disconnected",u)},u=()=>{a&&(clearTimeout(a),p())};return e[t]={get state(){return c.state},refresh:d,subscribe(t){l++,1===l&&(()=>{if(void 0!==a)return clearTimeout(a),void(a=void 0);s&&(o=s(e,c)),i&&(e.addEventListener("ready",h),h()),e.addEventListener("disconnected",u)})();const n=c.subscribe(t);return void 0!==c.state&&setTimeout((()=>t(c.state)),0),()=>{n(),l--,l||(r.unsubGrace?a=setTimeout(p,5e3):p())}}},e[t]},r=(e,t,i,n,r)=>s(n,e,t,i).subscribe(r)},57835:(e,t,i)=>{i.d(t,{XM:()=>n.XM,Xe:()=>n.Xe,pX:()=>n.pX});var n=i(38941)}}]);
//# sourceMappingURL=571fe6eb.js.map