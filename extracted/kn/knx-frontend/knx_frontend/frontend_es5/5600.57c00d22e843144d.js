"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5600"],{45917:function(e,t,r){r.a(e,(async function(e,a){try{r.r(t),r.d(t,{HaLabelSelector:function(){return v}});r(26847),r(27530);var i=r(73742),o=r(59048),s=r(7616),n=r(74608),l=r(29740),d=r(19442),u=e([d]);d=(u.then?(await u)():u)[0];let c,h,b,p=e=>e;class v extends o.oi{render(){var e;return this.selector.label.multiple?(0,o.dy)(c||(c=p`
        <ha-labels-picker
          no-add
          .hass=${0}
          .value=${0}
          .required=${0}
          .disabled=${0}
          .label=${0}
          @value-changed=${0}
        >
        </ha-labels-picker>
      `),this.hass,(0,n.r)(null!==(e=this.value)&&void 0!==e?e:[]),this.required,this.disabled,this.label,this._handleChange):(0,o.dy)(h||(h=p`
      <ha-label-picker
        no-add
        .hass=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .label=${0}
        @value-changed=${0}
      >
      </ha-label-picker>
    `),this.hass,this.value,this.required,this.disabled,this.label,this._handleChange)}_handleChange(e){let t=e.detail.value;this.value!==t&&((""===t||Array.isArray(t)&&0===t.length)&&!this.required&&(t=void 0),(0,l.B)(this,"value-changed",{value:t}))}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}v.styles=(0,o.iv)(b||(b=p`
    ha-labels-picker {
      display: block;
      width: 100%;
    }
  `)),(0,i.__decorate)([(0,s.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,i.__decorate)([(0,s.Cb)()],v.prototype,"value",void 0),(0,i.__decorate)([(0,s.Cb)()],v.prototype,"name",void 0),(0,i.__decorate)([(0,s.Cb)()],v.prototype,"label",void 0),(0,i.__decorate)([(0,s.Cb)()],v.prototype,"placeholder",void 0),(0,i.__decorate)([(0,s.Cb)()],v.prototype,"helper",void 0),(0,i.__decorate)([(0,s.Cb)({attribute:!1})],v.prototype,"selector",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],v.prototype,"disabled",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],v.prototype,"required",void 0),v=(0,i.__decorate)([(0,s.Mo)("ha-selector-label")],v),a()}catch(c){a(c)}}))},88865:function(e,t,r){r.d(t,{B:function(){return o}});r(40777),r(2394),r(87799),r(1455);const a=e=>{let t=[];function r(r,a){e=a?r:Object.assign(Object.assign({},e),r);let i=t;for(let t=0;t<i.length;t++)i[t](e)}return{get state(){return e},action(t){function a(e){r(e,!1)}return function(){let r=[e];for(let e=0;e<arguments.length;e++)r.push(arguments[e]);let i=t.apply(this,r);if(null!=i)return i instanceof Promise?i.then(a):a(i)}},setState:r,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let r=[];for(let a=0;a<t.length;a++)t[a]===e?e=null:r.push(t[a]);t=r}(e)}}}},i=(e,t,r,i,o={unsubGrace:!0})=>{if(e[t])return e[t];let s,n,l=0,d=a();const u=()=>{if(!r)throw new Error("Collection does not support refresh");return r(e).then((e=>d.setState(e,!0)))},c=()=>u().catch((t=>{if(e.connected)throw t})),h=()=>{n=void 0,s&&s.then((e=>{e()})),d.clearState(),e.removeEventListener("ready",u),e.removeEventListener("disconnected",b)},b=()=>{n&&(clearTimeout(n),h())};return e[t]={get state(){return d.state},refresh:u,subscribe(t){l++,1===l&&(()=>{if(void 0!==n)return clearTimeout(n),void(n=void 0);i&&(s=i(e,d)),r&&(e.addEventListener("ready",c),c()),e.addEventListener("disconnected",b)})();const a=d.subscribe(t);return void 0!==d.state&&setTimeout((()=>t(d.state)),0),()=>{a(),l--,l||(o.unsubGrace?n=setTimeout(h,5e3):h())}}},e[t]},o=(e,t,r,a,o)=>i(a,e,t,r).subscribe(o)}}]);
//# sourceMappingURL=5600.57c00d22e843144d.js.map