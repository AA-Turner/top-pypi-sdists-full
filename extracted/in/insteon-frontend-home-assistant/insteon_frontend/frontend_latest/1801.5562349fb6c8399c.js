/*! For license information please see 1801.5562349fb6c8399c.js.LICENSE.txt */
export const __webpack_id__="1801";export const __webpack_ids__=["1801"];export const __webpack_modules__={56161:function(t,e,o){o.d(e,{P:()=>r});const r=t=>(e,o)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach((t,o)=>e.constructor._observers.set(o,t))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach((t,e)=>{const o=this.constructor._observers.get(e);void 0!==o&&o.call(this,this[e],t)})}}e.constructor._observers.set(o,t)}},61171:function(t,e,o){o.d(e,{A:()=>r});const r=o(96196).AH`:host {
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
`},52630:function(t,e,o){o.a(t,async function(t,r){try{o.d(e,{A:()=>C});var i=o(96196),n=o(77845),s=o(94333),a=o(17051),h=o(42462),l=o(28438),p=o(98779),d=o(27259),c=o(984),u=o(53720),b=o(9395),v=o(32510),w=o(40158),y=o(61171),f=t([w]);w=(f.then?(await f)():f)[0];var g=Object.defineProperty,m=Object.getOwnPropertyDescriptor,k=(t,e,o,r)=>{for(var i,n=r>1?void 0:r?m(e,o):e,s=t.length-1;s>=0;s--)(i=t[s])&&(n=(r?i(e,o,n):i(n))||n);return r&&n&&g(e,o,n),n};let C=class extends v.A{connectedCallback(){super.connectedCallback(),this.eventController.signal.aborted&&(this.eventController=new AbortController),this.open&&(this.open=!1,this.updateComplete.then(()=>{this.open=!0})),this.id||(this.id=(0,u.N)("wa-tooltip-")),this.for&&this.anchor?(this.anchor=null,this.handleForChange()):this.for&&this.handleForChange()}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("keydown",this.handleDocumentKeyDown),this.eventController.abort(),this.anchor&&this.removeFromAriaLabelledBy(this.anchor,this.id)}firstUpdated(){this.body.hidden=!this.open,this.open&&(this.popup.active=!0,this.popup.reposition())}hasTrigger(t){return this.trigger.split(" ").includes(t)}addToAriaLabelledBy(t,e){const o=(t.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean);o.includes(e)||(o.push(e),t.setAttribute("aria-labelledby",o.join(" ")))}removeFromAriaLabelledBy(t,e){const o=(t.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean).filter(t=>t!==e);o.length>0?t.setAttribute("aria-labelledby",o.join(" ")):t.removeAttribute("aria-labelledby")}async handleOpenChange(){if(this.open){if(this.disabled)return;const t=new p.k;if(this.dispatchEvent(t),t.defaultPrevented)return void(this.open=!1);document.addEventListener("keydown",this.handleDocumentKeyDown,{signal:this.eventController.signal}),this.body.hidden=!1,this.popup.active=!0,await(0,d.Ud)(this.popup.popup,"show-with-scale"),this.popup.reposition(),this.dispatchEvent(new h.q)}else{const t=new l.L;if(this.dispatchEvent(t),t.defaultPrevented)return void(this.open=!1);document.removeEventListener("keydown",this.handleDocumentKeyDown),await(0,d.Ud)(this.popup.popup,"hide-with-scale"),this.popup.active=!1,this.body.hidden=!0,this.dispatchEvent(new a.Z)}}handleForChange(){const t=this.getRootNode();if(!t)return;const e=this.for?t.getElementById(this.for):null,o=this.anchor;if(e===o)return;const{signal:r}=this.eventController;e&&(this.addToAriaLabelledBy(e,this.id),e.addEventListener("blur",this.handleBlur,{capture:!0,signal:r}),e.addEventListener("focus",this.handleFocus,{capture:!0,signal:r}),e.addEventListener("click",this.handleClick,{signal:r}),e.addEventListener("mouseover",this.handleMouseOver,{signal:r}),e.addEventListener("mouseout",this.handleMouseOut,{signal:r})),o&&(this.removeFromAriaLabelledBy(o,this.id),o.removeEventListener("blur",this.handleBlur,{capture:!0}),o.removeEventListener("focus",this.handleFocus,{capture:!0}),o.removeEventListener("click",this.handleClick),o.removeEventListener("mouseover",this.handleMouseOver),o.removeEventListener("mouseout",this.handleMouseOut)),this.anchor=e}async handleOptionsChange(){this.hasUpdated&&(await this.updateComplete,this.popup.reposition())}handleDisabledChange(){this.disabled&&this.open&&this.hide()}async show(){if(!this.open)return this.open=!0,(0,c.l)(this,"wa-after-show")}async hide(){if(this.open)return this.open=!1,(0,c.l)(this,"wa-after-hide")}render(){return i.qy`
      <wa-popup
        part="base"
        exportparts="
          popup:base__popup,
          arrow:base__arrow
        "
        class=${(0,s.H)({tooltip:!0,"tooltip-open":this.open})}
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
    `}constructor(){super(...arguments),this.placement="top",this.disabled=!1,this.distance=8,this.open=!1,this.skidding=0,this.showDelay=150,this.hideDelay=0,this.trigger="hover focus",this.withoutArrow=!1,this.for=null,this.anchor=null,this.eventController=new AbortController,this.handleBlur=()=>{this.hasTrigger("focus")&&this.hide()},this.handleClick=()=>{this.hasTrigger("click")&&(this.open?this.hide():this.show())},this.handleFocus=()=>{this.hasTrigger("focus")&&this.show()},this.handleDocumentKeyDown=t=>{"Escape"===t.key&&(t.stopPropagation(),this.hide())},this.handleMouseOver=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.show(),this.showDelay))},this.handleMouseOut=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.hide(),this.hideDelay))}}};C.css=y.A,C.dependencies={"wa-popup":w.A},k([(0,n.P)("slot:not([name])")],C.prototype,"defaultSlot",2),k([(0,n.P)(".body")],C.prototype,"body",2),k([(0,n.P)("wa-popup")],C.prototype,"popup",2),k([(0,n.MZ)()],C.prototype,"placement",2),k([(0,n.MZ)({type:Boolean,reflect:!0})],C.prototype,"disabled",2),k([(0,n.MZ)({type:Number})],C.prototype,"distance",2),k([(0,n.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",2),k([(0,n.MZ)({type:Number})],C.prototype,"skidding",2),k([(0,n.MZ)({attribute:"show-delay",type:Number})],C.prototype,"showDelay",2),k([(0,n.MZ)({attribute:"hide-delay",type:Number})],C.prototype,"hideDelay",2),k([(0,n.MZ)()],C.prototype,"trigger",2),k([(0,n.MZ)({attribute:"without-arrow",type:Boolean,reflect:!0})],C.prototype,"withoutArrow",2),k([(0,n.MZ)()],C.prototype,"for",2),k([(0,n.wk)()],C.prototype,"anchor",2),k([(0,b.w)("open",{waitUntilFirstUpdate:!0})],C.prototype,"handleOpenChange",1),k([(0,b.w)("for")],C.prototype,"handleForChange",1),k([(0,b.w)(["distance","placement","skidding"])],C.prototype,"handleOptionsChange",1),k([(0,b.w)("disabled")],C.prototype,"handleDisabledChange",1),C=k([(0,n.EM)("wa-tooltip")],C),r()}catch(C){r(C)}})},70570:function(t,e,o){o.d(e,{N:()=>n});const r=t=>{let e=[];function o(o,r){t=r?o:Object.assign(Object.assign({},t),o);let i=e;for(let e=0;e<i.length;e++)i[e](t)}return{get state(){return t},action(e){function r(t){o(t,!1)}return function(){let o=[t];for(let t=0;t<arguments.length;t++)o.push(arguments[t]);let i=e.apply(this,o);if(null!=i)return i instanceof Promise?i.then(r):r(i)}},setState:o,clearState(){t=void 0},subscribe(t){return e.push(t),()=>{!function(t){let o=[];for(let r=0;r<e.length;r++)e[r]===t?t=null:o.push(e[r]);e=o}(t)}}}},i=(t,e,o,i,n={unsubGrace:!0})=>{if(t[e])return t[e];let s,a,h=0,l=r();const p=()=>{if(!o)throw new Error("Collection does not support refresh");return o(t).then(t=>l.setState(t,!0))},d=()=>p().catch(e=>{if(t.connected)throw e}),c=()=>{a=void 0,s&&s.then(t=>{t()}),l.clearState(),t.removeEventListener("ready",p),t.removeEventListener("disconnected",u)},u=()=>{a&&(clearTimeout(a),c())};return t[e]={get state(){return l.state},refresh:p,subscribe(e){h++,1===h&&(()=>{if(void 0!==a)return clearTimeout(a),void(a=void 0);i&&(s=i(t,l)),o&&(t.addEventListener("ready",d),d()),t.addEventListener("disconnected",u)})();const r=l.subscribe(e);return void 0!==l.state&&setTimeout(()=>e(l.state),0),()=>{r(),h--,h||(n.unsubGrace?a=setTimeout(c,5e3):c())}}},t[e]},n=(t,e,o,r,n)=>i(r,t,e,o).subscribe(n)},95192:function(t,e,o){function r(t){return new Promise((e,o)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>o(t.error)})}function i(t,e){let o;return(i,n)=>(()=>{if(o)return o;const i=indexedDB.open(t);return i.onupgradeneeded=()=>i.result.createObjectStore(e),o=r(i),o.then(t=>{t.onclose=()=>o=void 0},()=>{}),o})().then(t=>n(t.transaction(e,i).objectStore(e)))}let n;function s(){return n||(n=i("keyval-store","keyval")),n}function a(t,e=s()){return e("readonly",e=>r(e.get(t)))}function h(t,e,o=s()){return o("readwrite",o=>(o.put(e,t),r(o.transaction)))}function l(t=s()){return t("readwrite",t=>(t.clear(),r(t.transaction)))}o.d(e,{IU:()=>l,Jt:()=>a,Yd:()=>r,hZ:()=>h,y$:()=>i})}};
//# sourceMappingURL=1801.5562349fb6c8399c.js.map