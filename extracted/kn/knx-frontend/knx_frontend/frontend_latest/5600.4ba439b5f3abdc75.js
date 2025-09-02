export const __webpack_ids__=["5600"];export const __webpack_modules__={45917:function(e,t,r){r.r(t),r.d(t,{HaLabelSelector:()=>d});var a=r(73742),o=r(59048),s=r(7616),i=r(74608),l=r(29740);r(19442);class d extends o.oi{render(){return this.selector.label.multiple?o.dy`
        <ha-labels-picker
          no-add
          .hass=${this.hass}
          .value=${(0,i.r)(this.value??[])}
          .required=${this.required}
          .disabled=${this.disabled}
          .label=${this.label}
          @value-changed=${this._handleChange}
        >
        </ha-labels-picker>
      `:o.dy`
      <ha-label-picker
        no-add
        .hass=${this.hass}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .label=${this.label}
        @value-changed=${this._handleChange}
      >
      </ha-label-picker>
    `}_handleChange(e){let t=e.detail.value;this.value!==t&&((""===t||Array.isArray(t)&&0===t.length)&&!this.required&&(t=void 0),(0,l.B)(this,"value-changed",{value:t}))}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}d.styles=o.iv`
    ha-labels-picker {
      display: block;
      width: 100%;
    }
  `,(0,a.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"name",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"placeholder",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"selector",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],d.prototype,"required",void 0),d=(0,a.__decorate)([(0,s.Mo)("ha-selector-label")],d)},88865:function(e,t,r){r.d(t,{B:()=>s});const a=e=>{let t=[];function r(r,a){e=a?r:Object.assign(Object.assign({},e),r);let o=t;for(let t=0;t<o.length;t++)o[t](e)}return{get state(){return e},action(t){function a(e){r(e,!1)}return function(){let r=[e];for(let e=0;e<arguments.length;e++)r.push(arguments[e]);let o=t.apply(this,r);if(null!=o)return o instanceof Promise?o.then(a):a(o)}},setState:r,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let r=[];for(let a=0;a<t.length;a++)t[a]===e?e=null:r.push(t[a]);t=r}(e)}}}},o=(e,t,r,o,s={unsubGrace:!0})=>{if(e[t])return e[t];let i,l,d=0,n=a();const c=()=>{if(!r)throw new Error("Collection does not support refresh");return r(e).then((e=>n.setState(e,!0)))},u=()=>c().catch((t=>{if(e.connected)throw t})),h=()=>{l=void 0,i&&i.then((e=>{e()})),n.clearState(),e.removeEventListener("ready",c),e.removeEventListener("disconnected",b)},b=()=>{l&&(clearTimeout(l),h())};return e[t]={get state(){return n.state},refresh:c,subscribe(t){d++,1===d&&(()=>{if(void 0!==l)return clearTimeout(l),void(l=void 0);o&&(i=o(e,n)),r&&(e.addEventListener("ready",u),u()),e.addEventListener("disconnected",b)})();const a=n.subscribe(t);return void 0!==n.state&&setTimeout((()=>t(n.state)),0),()=>{a(),d--,d||(s.unsubGrace?l=setTimeout(h,5e3):h())}}},e[t]},s=(e,t,r,a,s)=>o(a,e,t,r).subscribe(s)}};
//# sourceMappingURL=5600.4ba439b5f3abdc75.js.map