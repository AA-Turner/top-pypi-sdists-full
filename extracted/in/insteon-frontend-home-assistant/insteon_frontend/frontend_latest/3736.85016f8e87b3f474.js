export const __webpack_id__="3736";export const __webpack_ids__=["3736"];export const __webpack_modules__={39651:function(t,o,e){e.r(o),e.d(o,{HaIconButtonGroup:()=>n});var i=e(62826),r=e(96196),a=e(77845);class n extends r.WF{render(){return r.qy`<slot></slot>`}}n.styles=r.AH`
    :host {
      position: relative;
      display: flex;
      flex-direction: row;
      align-items: center;
      height: 48px;
      border-radius: var(--ha-border-radius-4xl);
      background-color: rgba(139, 145, 151, 0.1);
      box-sizing: border-box;
      width: auto;
      padding: 0;
    }
    ::slotted(.separator) {
      background-color: rgba(var(--rgb-primary-text-color), 0.15);
      width: 1px;
      margin: 0 1px;
      height: 40px;
    }
  `,n=(0,i.__decorate)([(0,a.EM)("ha-icon-button-group")],n)},48939:function(t,o,e){e.a(t,async function(t,i){try{e.r(o),e.d(o,{HaIconButtonToolbar:()=>h});var r=e(62826),a=e(96196),n=e(77845),s=(e(22598),e(60733),e(39651),e(88422)),l=t([s]);s=(l.then?(await l)():l)[0];class h extends a.WF{findToolbarButtons(t=""){const o=this._buttons?.filter(t=>t.classList.contains("icon-toolbar-button"));if(!o||!o.length)return;if(!t.length)return o;const e=o.filter(o=>o.querySelector(t));return e.length?e:void 0}findToolbarButtonById(t){const o=this.shadowRoot?.getElementById(t);if(o&&"ha-icon-button"===o.localName)return o}render(){return a.qy`
      <ha-icon-button-group class="icon-toolbar-buttongroup">
        ${this.items.map(t=>"string"==typeof t?a.qy`<div class="icon-toolbar-divider" role="separator"></div>`:a.qy`<ha-tooltip
                  .disabled=${!t.tooltip}
                  .for=${t.id??"icon-button-"+t.label}
                  >${t.tooltip??""}</ha-tooltip
                >
                <ha-icon-button
                  class="icon-toolbar-button"
                  .id=${t.id??"icon-button-"+t.label}
                  @click=${t.action}
                  .label=${t.label}
                  .path=${t.path}
                  .disabled=${t.disabled??!1}
                ></ha-icon-button>`)}
      </ha-icon-button-group>
    `}constructor(...t){super(...t),this.items=[]}}h.styles=a.AH`
    :host {
      position: absolute;
      top: 0px;
      width: 100%;
      display: flex;
      flex-direction: row-reverse;
      background-color: var(
        --icon-button-toolbar-color,
        var(--secondary-background-color, whitesmoke)
      );
      --icon-button-toolbar-height: 32px;
      --icon-button-toolbar-button: calc(
        var(--icon-button-toolbar-height) - 4px
      );
      --icon-button-toolbar-icon: calc(
        var(--icon-button-toolbar-height) - 10px
      );
    }

    .icon-toolbar-divider {
      height: var(--icon-button-toolbar-icon);
      margin: 0px 4px;
      border: 0.5px solid
        var(--divider-color, var(--secondary-text-color, transparent));
    }

    .icon-toolbar-buttongroup {
      background-color: transparent;
      padding-right: 4px;
      height: var(--icon-button-toolbar-height);
      gap: var(--ha-space-2);
    }

    .icon-toolbar-button {
      color: var(--secondary-text-color);
      --mdc-icon-button-size: var(--icon-button-toolbar-button);
      --mdc-icon-size: var(--icon-button-toolbar-icon);
      /* Ensure button is clickable on iOS */
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }
  `,(0,r.__decorate)([(0,n.MZ)({type:Array,attribute:!1})],h.prototype,"items",void 0),(0,r.__decorate)([(0,n.YG)("ha-icon-button")],h.prototype,"_buttons",void 0),h=(0,r.__decorate)([(0,n.EM)("ha-icon-button-toolbar")],h),i()}catch(h){i(h)}})},88422:function(t,o,e){e.a(t,async function(t,o){try{var i=e(62826),r=e(52630),a=e(96196),n=e(77845),s=t([r]);r=(s.then?(await s)():s)[0];class l extends r.A{static get styles(){return[r.A.styles,a.AH`
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
      `]}constructor(...t){super(...t),this.showDelay=150,this.hideDelay=150}}(0,i.__decorate)([(0,n.MZ)({attribute:"show-delay",type:Number})],l.prototype,"showDelay",void 0),(0,i.__decorate)([(0,n.MZ)({attribute:"hide-delay",type:Number})],l.prototype,"hideDelay",void 0),l=(0,i.__decorate)([(0,n.EM)("ha-tooltip")],l),o()}catch(l){o(l)}})},61171:function(t,o,e){e.d(o,{A:()=>i});const i=e(96196).AH`:host {
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
`},52630:function(t,o,e){e.a(t,async function(t,i){try{e.d(o,{A:()=>x});var r=e(96196),a=e(77845),n=e(94333),s=e(17051),l=e(42462),h=e(28438),p=e(98779),d=e(27259),c=e(984),u=e(53720),b=e(9395),v=e(32510),w=e(40158),y=e(61171),g=t([w]);w=(g.then?(await g)():g)[0];var m=Object.defineProperty,f=Object.getOwnPropertyDescriptor,k=(t,o,e,i)=>{for(var r,a=i>1?void 0:i?f(o,e):o,n=t.length-1;n>=0;n--)(r=t[n])&&(a=(i?r(o,e,a):r(a))||a);return i&&a&&m(o,e,a),a};let x=class extends v.A{connectedCallback(){super.connectedCallback(),this.eventController.signal.aborted&&(this.eventController=new AbortController),this.open&&(this.open=!1,this.updateComplete.then(()=>{this.open=!0})),this.id||(this.id=(0,u.N)("wa-tooltip-")),this.for&&this.anchor?(this.anchor=null,this.handleForChange()):this.for&&this.handleForChange()}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("keydown",this.handleDocumentKeyDown),this.eventController.abort(),this.anchor&&this.removeFromAriaLabelledBy(this.anchor,this.id)}firstUpdated(){this.body.hidden=!this.open,this.open&&(this.popup.active=!0,this.popup.reposition())}hasTrigger(t){return this.trigger.split(" ").includes(t)}addToAriaLabelledBy(t,o){const e=(t.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean);e.includes(o)||(e.push(o),t.setAttribute("aria-labelledby",e.join(" ")))}removeFromAriaLabelledBy(t,o){const e=(t.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean).filter(t=>t!==o);e.length>0?t.setAttribute("aria-labelledby",e.join(" ")):t.removeAttribute("aria-labelledby")}async handleOpenChange(){if(this.open){if(this.disabled)return;const t=new p.k;if(this.dispatchEvent(t),t.defaultPrevented)return void(this.open=!1);document.addEventListener("keydown",this.handleDocumentKeyDown,{signal:this.eventController.signal}),this.body.hidden=!1,this.popup.active=!0,await(0,d.Ud)(this.popup.popup,"show-with-scale"),this.popup.reposition(),this.dispatchEvent(new l.q)}else{const t=new h.L;if(this.dispatchEvent(t),t.defaultPrevented)return void(this.open=!1);document.removeEventListener("keydown",this.handleDocumentKeyDown),await(0,d.Ud)(this.popup.popup,"hide-with-scale"),this.popup.active=!1,this.body.hidden=!0,this.dispatchEvent(new s.Z)}}handleForChange(){const t=this.getRootNode();if(!t)return;const o=this.for?t.getElementById(this.for):null,e=this.anchor;if(o===e)return;const{signal:i}=this.eventController;o&&(this.addToAriaLabelledBy(o,this.id),o.addEventListener("blur",this.handleBlur,{capture:!0,signal:i}),o.addEventListener("focus",this.handleFocus,{capture:!0,signal:i}),o.addEventListener("click",this.handleClick,{signal:i}),o.addEventListener("mouseover",this.handleMouseOver,{signal:i}),o.addEventListener("mouseout",this.handleMouseOut,{signal:i})),e&&(this.removeFromAriaLabelledBy(e,this.id),e.removeEventListener("blur",this.handleBlur,{capture:!0}),e.removeEventListener("focus",this.handleFocus,{capture:!0}),e.removeEventListener("click",this.handleClick),e.removeEventListener("mouseover",this.handleMouseOver),e.removeEventListener("mouseout",this.handleMouseOut)),this.anchor=o}async handleOptionsChange(){this.hasUpdated&&(await this.updateComplete,this.popup.reposition())}handleDisabledChange(){this.disabled&&this.open&&this.hide()}async show(){if(!this.open)return this.open=!0,(0,c.l)(this,"wa-after-show")}async hide(){if(this.open)return this.open=!1,(0,c.l)(this,"wa-after-hide")}render(){return r.qy`
      <wa-popup
        part="base"
        exportparts="
          popup:base__popup,
          arrow:base__arrow
        "
        class=${(0,n.H)({tooltip:!0,"tooltip-open":this.open})}
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
    `}constructor(){super(...arguments),this.placement="top",this.disabled=!1,this.distance=8,this.open=!1,this.skidding=0,this.showDelay=150,this.hideDelay=0,this.trigger="hover focus",this.withoutArrow=!1,this.for=null,this.anchor=null,this.eventController=new AbortController,this.handleBlur=()=>{this.hasTrigger("focus")&&this.hide()},this.handleClick=()=>{this.hasTrigger("click")&&(this.open?this.hide():this.show())},this.handleFocus=()=>{this.hasTrigger("focus")&&this.show()},this.handleDocumentKeyDown=t=>{"Escape"===t.key&&(t.stopPropagation(),this.hide())},this.handleMouseOver=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.show(),this.showDelay))},this.handleMouseOut=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.hide(),this.hideDelay))}}};x.css=y.A,x.dependencies={"wa-popup":w.A},k([(0,a.P)("slot:not([name])")],x.prototype,"defaultSlot",2),k([(0,a.P)(".body")],x.prototype,"body",2),k([(0,a.P)("wa-popup")],x.prototype,"popup",2),k([(0,a.MZ)()],x.prototype,"placement",2),k([(0,a.MZ)({type:Boolean,reflect:!0})],x.prototype,"disabled",2),k([(0,a.MZ)({type:Number})],x.prototype,"distance",2),k([(0,a.MZ)({type:Boolean,reflect:!0})],x.prototype,"open",2),k([(0,a.MZ)({type:Number})],x.prototype,"skidding",2),k([(0,a.MZ)({attribute:"show-delay",type:Number})],x.prototype,"showDelay",2),k([(0,a.MZ)({attribute:"hide-delay",type:Number})],x.prototype,"hideDelay",2),k([(0,a.MZ)()],x.prototype,"trigger",2),k([(0,a.MZ)({attribute:"without-arrow",type:Boolean,reflect:!0})],x.prototype,"withoutArrow",2),k([(0,a.MZ)()],x.prototype,"for",2),k([(0,a.wk)()],x.prototype,"anchor",2),k([(0,b.w)("open",{waitUntilFirstUpdate:!0})],x.prototype,"handleOpenChange",1),k([(0,b.w)("for")],x.prototype,"handleForChange",1),k([(0,b.w)(["distance","placement","skidding"])],x.prototype,"handleOptionsChange",1),k([(0,b.w)("disabled")],x.prototype,"handleDisabledChange",1),x=k([(0,a.EM)("wa-tooltip")],x),i()}catch(x){i(x)}})}};
//# sourceMappingURL=3736.85016f8e87b3f474.js.map