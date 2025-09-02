/*! For license information please see 760.7da9baf915e5ced9.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["760"],{83379:function(e,t,o){o.a(e,(async function(e,i){try{o.r(t),o.d(t,{HaIconOverflowMenu:function(){return _}});o(26847),o(81738),o(6989),o(27530);var r=o(73742),n=o(59048),a=o(7616),s=o(31733),l=o(77204),d=(o(51431),o(78645),o(40830),o(27341)),c=(o(72633),o(1963),e([d]));d=(c.then?(await c)():c)[0];let m,p,h,u,v,g,y,f,b=e=>e;const x="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class _ extends n.oi{render(){return(0,n.dy)(m||(m=b`
      ${0}
    `),this.narrow?(0,n.dy)(p||(p=b` <!-- Collapsed representation for small screens -->
            <ha-md-button-menu
              @click=${0}
              positioning="popover"
            >
              <ha-icon-button
                .label=${0}
                .path=${0}
                slot="trigger"
              ></ha-icon-button>

              ${0}
            </ha-md-button-menu>`),this._handleIconOverflowMenuOpened,this.hass.localize("ui.common.overflow_menu"),x,this.items.map((e=>e.divider?(0,n.dy)(h||(h=b`<ha-md-divider
                      role="separator"
                      tabindex="-1"
                    ></ha-md-divider>`)):(0,n.dy)(u||(u=b`<ha-md-menu-item
                      ?disabled=${0}
                      .clickAction=${0}
                      class=${0}
                    >
                      <ha-svg-icon
                        slot="start"
                        class=${0}
                        .path=${0}
                      ></ha-svg-icon>
                      ${0}
                    </ha-md-menu-item> `),e.disabled,e.action,(0,s.$)({warning:Boolean(e.warning)}),(0,s.$)({warning:Boolean(e.warning)}),e.path,e.label)))):(0,n.dy)(v||(v=b`
            <!-- Icon representation for big screens -->
            ${0}
          `),this.items.map((e=>{var t;return e.narrowOnly?n.Ld:e.divider?(0,n.dy)(g||(g=b`<div role="separator"></div>`)):(0,n.dy)(y||(y=b`<ha-tooltip
                      .disabled=${0}
                      .content=${0}
                    >
                      <ha-icon-button
                        @click=${0}
                        .label=${0}
                        .path=${0}
                        ?disabled=${0}
                      ></ha-icon-button>
                    </ha-tooltip>`),!e.tooltip,null!==(t=e.tooltip)&&void 0!==t?t:"",e.action,e.label,e.path,e.disabled)}))))}_handleIconOverflowMenuOpened(e){e.stopPropagation()}static get styles(){return[l.Qx,(0,n.iv)(f||(f=b`
        :host {
          display: flex;
          justify-content: flex-end;
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
      `))]}constructor(...e){super(...e),this.items=[],this.narrow=!1}}(0,r.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,r.__decorate)([(0,a.Cb)({type:Array})],_.prototype,"items",void 0),(0,r.__decorate)([(0,a.Cb)({type:Boolean})],_.prototype,"narrow",void 0),_=(0,r.__decorate)([(0,a.Mo)("ha-icon-overflow-menu")],_),i()}catch(m){i(m)}}))},51431:function(e,t,o){o(26847),o(27530);var i=o(73742),r=o(59048),n=o(7616),a=o(29740),s=(o(90380),o(10051)),l=o(91646),d=o(67419);let c;class m extends s.v2{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(e){var t,o;e.detail.reason.kind===d.GB.KEYDOWN&&e.detail.reason.key===d.KC.ESCAPE||null===(t=(o=e.detail.initiator).clickAction)||void 0===t||t.call(o,e.detail.initiator)}}m.styles=[l.W,(0,r.iv)(c||(c=(e=>e)`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `))],m=(0,i.__decorate)([(0,n.Mo)("ha-md-menu")],m);let p,h,u=e=>e;class v extends r.oi{get items(){return this._menu.items}focus(){var e;this._menu.open?this._menu.focus():null===(e=this._triggerButton)||void 0===e||e.focus()}render(){return(0,r.dy)(p||(p=u`
      <div @click=${0}>
        <slot name="trigger" @slotchange=${0}></slot>
      </div>
      <ha-md-menu
        .positioning=${0}
        .hasOverflow=${0}
        @opening=${0}
        @closing=${0}
      >
        <slot></slot>
      </ha-md-menu>
    `),this._handleClick,this._setTriggerAria,this.positioning,this.hasOverflow,this._handleOpening,this._handleClosing)}_handleOpening(){(0,a.B)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,a.B)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...e){super(...e),this.disabled=!1,this.hasOverflow=!1}}v.styles=(0,r.iv)(h||(h=u`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `)),(0,i.__decorate)([(0,n.Cb)({type:Boolean})],v.prototype,"disabled",void 0),(0,i.__decorate)([(0,n.Cb)()],v.prototype,"positioning",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean,attribute:"has-overflow"})],v.prototype,"hasOverflow",void 0),(0,i.__decorate)([(0,n.IO)("ha-md-menu",!0)],v.prototype,"_menu",void 0),v=(0,i.__decorate)([(0,n.Mo)("ha-md-button-menu")],v)},1963:function(e,t,o){var i=o(73742),r=o(66923),n=o(93952),a=o(59048),s=o(7616);let l;class d extends r.i{}d.styles=[n.W,(0,a.iv)(l||(l=(e=>e)`
      :host {
        --md-divider-color: var(--divider-color);
      }
    `))],d=(0,i.__decorate)([(0,s.Mo)("ha-md-divider")],d)},72633:function(e,t,o){var i=o(73742),r=o(94598),n=o(15215),a=o(59048),s=o(7616);let l;class d extends r.${}d.styles=[n.W,(0,a.iv)(l||(l=(e=>e)`
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
    `))],(0,i.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"clickAction",void 0),d=(0,i.__decorate)([(0,s.Mo)("ha-md-menu-item")],d)},27341:function(e,t,o){o.a(e,(async function(e,t){try{var i=o(73742),r=o(52634),n=o(62685),a=o(59048),s=o(7616),l=o(75535),d=e([r]);r=(d.then?(await d)():d)[0];let c,m=e=>e;(0,l.jx)("tooltip.show",{keyframes:[{opacity:0},{opacity:1}],options:{duration:150,easing:"ease"}}),(0,l.jx)("tooltip.hide",{keyframes:[{opacity:1},{opacity:0}],options:{duration:400,easing:"ease"}});class p extends r.Z{}p.styles=[n.Z,(0,a.iv)(c||(c=m`
      :host {
        --sl-tooltip-background-color: var(--secondary-background-color);
        --sl-tooltip-color: var(--primary-text-color);
        --sl-tooltip-font-family: var(
          --ha-tooltip-font-family,
          var(--ha-font-family-body)
        );
        --sl-tooltip-font-size: var(
          --ha-tooltip-font-size,
          var(--ha-font-size-s)
        );
        --sl-tooltip-font-weight: var(
          --ha-tooltip-font-weight,
          var(--ha-font-weight-normal)
        );
        --sl-tooltip-line-height: var(
          --ha-tooltip-line-height,
          var(--ha-line-height-condensed)
        );
        --sl-tooltip-padding: 8px;
        --sl-tooltip-border-radius: var(--ha-tooltip-border-radius, 4px);
        --sl-tooltip-arrow-size: var(--ha-tooltip-arrow-size, 8px);
        --sl-z-index-tooltip: var(--ha-tooltip-z-index, 1000);
      }
    `))],p=(0,i.__decorate)([(0,s.Mo)("ha-tooltip")],p),t()}catch(c){t(c)}}))},93952:function(e,t,o){o.d(t,{W:function(){return r}});let i;const r=(0,o(59048).iv)(i||(i=(e=>e)`:host{box-sizing:border-box;color:var(--md-divider-color, var(--md-sys-color-outline-variant, #cac4d0));display:flex;height:var(--md-divider-thickness, 1px);width:100%}:host([inset]),:host([inset-start]){padding-inline-start:16px}:host([inset]),:host([inset-end]){padding-inline-end:16px}:host::before{background:currentColor;content:"";height:100%;width:100%}@media(forced-colors: active){:host::before{background:CanvasText}}
`))},66923:function(e,t,o){o.d(t,{i:function(){return a}});o(26847),o(27530);var i=o(73742),r=o(59048),n=o(7616);class a extends r.oi{constructor(){super(...arguments),this.inset=!1,this.insetStart=!1,this.insetEnd=!1}}(0,i.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],a.prototype,"inset",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0,attribute:"inset-start"})],a.prototype,"insetStart",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0,attribute:"inset-end"})],a.prototype,"insetEnd",void 0)},15215:function(e,t,o){o.d(t,{W:function(){return r}});let i;const r=(0,o(59048).iv)(i||(i=(e=>e)`:host{display:flex;--md-ripple-hover-color: var(--md-menu-item-hover-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-hover-opacity: var(--md-menu-item-hover-state-layer-opacity, 0.08);--md-ripple-pressed-color: var(--md-menu-item-pressed-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-pressed-opacity: var(--md-menu-item-pressed-state-layer-opacity, 0.12)}:host([disabled]){opacity:var(--md-menu-item-disabled-opacity, 0.3);pointer-events:none}md-focus-ring{z-index:1;--md-focus-ring-shape: 8px}a,button,li{background:none;border:none;padding:0;margin:0;text-align:unset;text-decoration:none}.list-item{border-radius:inherit;display:flex;flex:1;max-width:inherit;min-width:inherit;outline:none;-webkit-tap-highlight-color:rgba(0,0,0,0)}.list-item:not(.disabled){cursor:pointer}[slot=container]{pointer-events:none}md-ripple{border-radius:inherit}md-item{border-radius:inherit;flex:1;color:var(--md-menu-item-label-text-color, var(--md-sys-color-on-surface, #1d1b20));font-family:var(--md-menu-item-label-text-font, var(--md-sys-typescale-body-large-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-label-text-size, var(--md-sys-typescale-body-large-size, 1rem));line-height:var(--md-menu-item-label-text-line-height, var(--md-sys-typescale-body-large-line-height, 1.5rem));font-weight:var(--md-menu-item-label-text-weight, var(--md-sys-typescale-body-large-weight, var(--md-ref-typeface-weight-regular, 400)));min-height:var(--md-menu-item-one-line-container-height, 56px);padding-top:var(--md-menu-item-top-space, 12px);padding-bottom:var(--md-menu-item-bottom-space, 12px);padding-inline-start:var(--md-menu-item-leading-space, 16px);padding-inline-end:var(--md-menu-item-trailing-space, 16px)}md-item[multiline]{min-height:var(--md-menu-item-two-line-container-height, 72px)}[slot=supporting-text]{color:var(--md-menu-item-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-supporting-text-font, var(--md-sys-typescale-body-medium-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-supporting-text-size, var(--md-sys-typescale-body-medium-size, 0.875rem));line-height:var(--md-menu-item-supporting-text-line-height, var(--md-sys-typescale-body-medium-line-height, 1.25rem));font-weight:var(--md-menu-item-supporting-text-weight, var(--md-sys-typescale-body-medium-weight, var(--md-ref-typeface-weight-regular, 400)))}[slot=trailing-supporting-text]{color:var(--md-menu-item-trailing-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-trailing-supporting-text-font, var(--md-sys-typescale-label-small-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-trailing-supporting-text-size, var(--md-sys-typescale-label-small-size, 0.6875rem));line-height:var(--md-menu-item-trailing-supporting-text-line-height, var(--md-sys-typescale-label-small-line-height, 1rem));font-weight:var(--md-menu-item-trailing-supporting-text-weight, var(--md-sys-typescale-label-small-weight, var(--md-ref-typeface-weight-medium, 500)))}:is([slot=start],[slot=end])::slotted(*){fill:currentColor}[slot=start]{color:var(--md-menu-item-leading-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}[slot=end]{color:var(--md-menu-item-trailing-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}.list-item{background-color:var(--md-menu-item-container-color, transparent)}.list-item.selected{background-color:var(--md-menu-item-selected-container-color, var(--md-sys-color-secondary-container, #e8def8))}.selected:not(.disabled) ::slotted(*){color:var(--md-menu-item-selected-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b))}@media(forced-colors: active){:host([disabled]),:host([disabled]) slot{color:GrayText;opacity:1}.list-item{position:relative}.list-item.selected::before{content:"";position:absolute;inset:0;box-sizing:border-box;border-radius:inherit;pointer-events:none;border:3px double CanvasText}}
`))},94598:function(e,t,o){o.d(t,{$:function(){return _}});o(26847),o(87799),o(27530);var i=o(73742),r=(o(31073),o(79239),o(12253),o(59048)),n=o(7616),a=o(31733),s=o(3939),l=o(67749),d=(o(37908),o(2394),o(81738),o(22960),o(20655),o(67419));class c{get typeaheadText(){if(null!==this.internalTypeaheadText)return this.internalTypeaheadText;const e=this.getHeadlineElements(),t=[];return e.forEach((e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())})),0===t.length&&this.getDefaultElements().forEach((e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())})),0===t.length&&this.getSupportingTextElements().forEach((e=>{e.textContent&&e.textContent.trim()&&t.push(e.textContent.trim())})),t.join(" ")}get tagName(){switch(this.host.type){case"link":return"a";case"button":return"button";default:return"li"}}get role(){return"option"===this.host.type?"option":"menuitem"}hostConnected(){this.host.toggleAttribute("md-menu-item",!0)}hostUpdate(){this.host.href&&(this.host.type="link")}setTypeaheadText(e){this.internalTypeaheadText=e}constructor(e,t){this.host=e,this.internalTypeaheadText=null,this.onClick=()=>{this.host.keepOpen||this.host.dispatchEvent((0,d.d7)(this.host,{kind:d.GB.CLICK_SELECTION}))},this.onKeydown=e=>{if(this.host.href&&"Enter"===e.code){const e=this.getInteractiveElement();e instanceof HTMLAnchorElement&&e.click()}if(e.defaultPrevented)return;const t=e.code;this.host.keepOpen&&"Escape"!==t||(0,d.kE)(t)&&(e.preventDefault(),this.host.dispatchEvent((0,d.d7)(this.host,{kind:d.GB.KEYDOWN,key:t})))},this.getHeadlineElements=t.getHeadlineElements,this.getSupportingTextElements=t.getSupportingTextElements,this.getDefaultElements=t.getDefaultElements,this.getInteractiveElement=t.getInteractiveElement,this.host.addController(this)}}let m,p,h,u,v,g,y,f,b=e=>e;const x=(0,l.T)(r.oi);class _ extends x{get typeaheadText(){return this.menuItemController.typeaheadText}set typeaheadText(e){this.menuItemController.setTypeaheadText(e)}render(){return this.renderListItem((0,r.dy)(m||(m=b`
      <md-item>
        <div slot="container">
          ${0} ${0}
        </div>
        <slot name="start" slot="start"></slot>
        <slot name="end" slot="end"></slot>
        ${0}
      </md-item>
    `),this.renderRipple(),this.renderFocusRing(),this.renderBody()))}renderListItem(e){const t="link"===this.type;let o;switch(this.menuItemController.tagName){case"a":o=(0,s.i0)(p||(p=b`a`));break;case"button":o=(0,s.i0)(h||(h=b`button`));break;default:o=(0,s.i0)(u||(u=b`li`))}const i=t&&this.target?this.target:r.Ld;return(0,s.dy)(v||(v=b`
      <${0}
        id="item"
        tabindex=${0}
        role=${0}
        aria-label=${0}
        aria-selected=${0}
        aria-checked=${0}
        aria-expanded=${0}
        aria-haspopup=${0}
        class="list-item ${0}"
        href=${0}
        target=${0}
        @click=${0}
        @keydown=${0}
      >${0}</${0}>
    `),o,this.disabled&&!t?-1:0,this.menuItemController.role,this.ariaLabel||r.Ld,this.ariaSelected||r.Ld,this.ariaChecked||r.Ld,this.ariaExpanded||r.Ld,this.ariaHasPopup||r.Ld,(0,a.$)(this.getRenderClasses()),this.href||r.Ld,i,this.menuItemController.onClick,this.menuItemController.onKeydown,e,o)}renderRipple(){return(0,r.dy)(g||(g=b` <md-ripple
      part="ripple"
      for="item"
      ?disabled=${0}></md-ripple>`),this.disabled)}renderFocusRing(){return(0,r.dy)(y||(y=b` <md-focus-ring
      part="focus-ring"
      for="item"
      inward></md-focus-ring>`))}getRenderClasses(){return{disabled:this.disabled,selected:this.selected}}renderBody(){return(0,r.dy)(f||(f=b`
      <slot></slot>
      <slot name="overline" slot="overline"></slot>
      <slot name="headline" slot="headline"></slot>
      <slot name="supporting-text" slot="supporting-text"></slot>
      <slot
        name="trailing-supporting-text"
        slot="trailing-supporting-text"></slot>
    `))}focus(){var e;null===(e=this.listItemRoot)||void 0===e||e.focus()}constructor(){super(...arguments),this.disabled=!1,this.type="menuitem",this.href="",this.target="",this.keepOpen=!1,this.selected=!1,this.menuItemController=new c(this,{getHeadlineElements:()=>this.headlineElements,getSupportingTextElements:()=>this.supportingTextElements,getDefaultElements:()=>this.defaultElements,getInteractiveElement:()=>this.listItemRoot})}}_.shadowRootOptions=Object.assign(Object.assign({},r.oi.shadowRootOptions),{},{delegatesFocus:!0}),(0,i.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],_.prototype,"disabled",void 0),(0,i.__decorate)([(0,n.Cb)()],_.prototype,"type",void 0),(0,i.__decorate)([(0,n.Cb)()],_.prototype,"href",void 0),(0,i.__decorate)([(0,n.Cb)()],_.prototype,"target",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean,attribute:"keep-open"})],_.prototype,"keepOpen",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean})],_.prototype,"selected",void 0),(0,i.__decorate)([(0,n.IO)(".list-item")],_.prototype,"listItemRoot",void 0),(0,i.__decorate)([(0,n.NH)({slot:"headline"})],_.prototype,"headlineElements",void 0),(0,i.__decorate)([(0,n.NH)({slot:"supporting-text"})],_.prototype,"supportingTextElements",void 0),(0,i.__decorate)([(0,n.vZ)({slot:""})],_.prototype,"defaultElements",void 0),(0,i.__decorate)([(0,n.Cb)({attribute:"typeahead-text"})],_.prototype,"typeaheadText",null)}}]);
//# sourceMappingURL=760.7da9baf915e5ced9.js.map