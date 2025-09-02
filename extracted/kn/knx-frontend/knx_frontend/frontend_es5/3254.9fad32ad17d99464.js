/*! For license information please see 3254.9fad32ad17d99464.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["3254"],{49590:function(t,e,o){o.a(t,(async function(t,i){try{o.r(e),o.d(e,{HaIconPicker:function(){return w}});o(39710),o(26847),o(2394),o(18574),o(81738),o(94814),o(22960),o(6989),o(72489),o(1455),o(67886),o(65451),o(46015),o(38334),o(94880),o(75643),o(29761),o(56389),o(27530);var s=o(73742),a=o(59048),r=o(7616),n=o(28105),c=o(29740),d=o(18610),l=o(54693),h=(o(3847),o(57264),t([l]));l=(h.then?(await h)():h)[0];let u,p,v,_,b,y=t=>t,$=[],C=!1;const f=async()=>{C=!0;const t=await o.e("4813").then(o.t.bind(o,81405,19));$=t.default.map((t=>({icon:`mdi:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords})));const e=[];Object.keys(d.g).forEach((t=>{e.push(g(t))})),(await Promise.all(e)).forEach((t=>{$.push(...t)}))},g=async t=>{try{const e=d.g[t].getIconList;if("function"!=typeof e)return[];const o=await e();return o.map((e=>{var o;return{icon:`${t}:${e.name}`,parts:new Set(e.name.split("-")),keywords:null!==(o=e.keywords)&&void 0!==o?o:[]}}))}catch(e){return console.warn(`Unable to load icon list for ${t} iconset`),[]}},m=t=>(0,a.dy)(u||(u=y`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    ${0}
  </ha-combo-box-item>
`),t.icon,t.icon);class w extends a.oi{render(){return(0,a.dy)(p||(p=y`
      <ha-combo-box
        .hass=${0}
        item-value-path="icon"
        item-label-path="icon"
        .value=${0}
        allow-custom-value
        .dataProvider=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .placeholder=${0}
        .errorMessage=${0}
        .invalid=${0}
        .renderer=${0}
        icon
        @opened-changed=${0}
        @value-changed=${0}
      >
        ${0}
      </ha-combo-box>
    `),this.hass,this._value,C?this._iconProvider:void 0,this.label,this.helper,this.disabled,this.required,this.placeholder,this.errorMessage,this.invalid,m,this._openedChanged,this._valueChanged,this._value||this.placeholder?(0,a.dy)(v||(v=y`
              <ha-icon .icon=${0} slot="icon">
              </ha-icon>
            `),this._value||this.placeholder):(0,a.dy)(_||(_=y`<slot slot="icon" name="fallback"></slot>`)))}async _openedChanged(t){t.detail.value&&!C&&(await f(),this.requestUpdate())}_valueChanged(t){t.stopPropagation(),this._setValue(t.detail.value)}_setValue(t){this.value=t,(0,c.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,n.Z)(((t,e=$)=>{if(!t)return e;const o=[],i=(t,e)=>o.push({icon:t,rank:e});for(const s of e)s.parts.has(t)?i(s.icon,1):s.keywords.includes(t)?i(s.icon,2):s.icon.includes(t)?i(s.icon,3):s.keywords.some((e=>e.includes(t)))&&i(s.icon,4);return 0===o.length&&i(t,0),o.sort(((t,e)=>t.rank-e.rank))})),this._iconProvider=(t,e)=>{const o=this._filterIcons(t.filter.toLowerCase(),$),i=t.page*t.pageSize,s=i+t.pageSize;e(o.slice(i,s),o.length)}}}w.styles=(0,a.iv)(b||(b=y`
    *[slot="icon"] {
      color: var(--primary-text-color);
      position: relative;
      bottom: 2px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `)),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],w.prototype,"hass",void 0),(0,s.__decorate)([(0,r.Cb)()],w.prototype,"value",void 0),(0,s.__decorate)([(0,r.Cb)()],w.prototype,"label",void 0),(0,s.__decorate)([(0,r.Cb)()],w.prototype,"helper",void 0),(0,s.__decorate)([(0,r.Cb)()],w.prototype,"placeholder",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:"error-message"})],w.prototype,"errorMessage",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],w.prototype,"disabled",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],w.prototype,"required",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],w.prototype,"invalid",void 0),w=(0,s.__decorate)([(0,r.Mo)("ha-icon-picker")],w),i()}catch(u){i(u)}}))},37339:function(t,e,o){o.a(t,(async function(t,i){try{o.r(e),o.d(e,{HaIconSelector:function(){return b}});o(26847),o(27530);var s=o(73742),a=o(59048),r=o(7616),n=o(28177),c=o(29740),d=o(54974),l=o(49590),h=o(27882),u=t([l,h,d]);[l,h,d]=u.then?(await u)():u;let p,v,_=t=>t;class b extends a.oi{render(){var t,e,o,i;const s=null===(t=this.context)||void 0===t?void 0:t.icon_entity,r=s?this.hass.states[s]:void 0,c=(null===(e=this.selector.icon)||void 0===e?void 0:e.placeholder)||(null==r?void 0:r.attributes.icon)||r&&(0,n.C)((0,d.gD)(this.hass,r));return(0,a.dy)(p||(p=_`
      <ha-icon-picker
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        .placeholder=${0}
        @value-changed=${0}
      >
        ${0}
      </ha-icon-picker>
    `),this.hass,this.label,this.value,this.required,this.disabled,this.helper,null!==(o=null===(i=this.selector.icon)||void 0===i?void 0:i.placeholder)&&void 0!==o?o:c,this._valueChanged,!c&&r?(0,a.dy)(v||(v=_`
              <ha-state-icon
                slot="fallback"
                .hass=${0}
                .stateObj=${0}
              ></ha-state-icon>
            `),this.hass,r):a.Ld)}_valueChanged(t){(0,c.B)(this,"value-changed",{value:t.detail.value})}constructor(...t){super(...t),this.disabled=!1,this.required=!0}}(0,s.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"selector",void 0),(0,s.__decorate)([(0,r.Cb)()],b.prototype,"value",void 0),(0,s.__decorate)([(0,r.Cb)()],b.prototype,"label",void 0),(0,s.__decorate)([(0,r.Cb)()],b.prototype,"helper",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],b.prototype,"disabled",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],b.prototype,"required",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"context",void 0),b=(0,s.__decorate)([(0,r.Mo)("ha-selector-icon")],b),i()}catch(p){i(p)}}))},27882:function(t,e,o){o.a(t,(async function(t,e){try{var i=o(73742),s=o(59048),a=o(7616),r=o(28177),n=o(18088),c=o(54974),d=(o(3847),o(40830),t([c]));c=(d.then?(await d)():d)[0];let l,h,u,p,v=t=>t;class _ extends s.oi{render(){var t,e;const o=this.icon||this.stateObj&&(null===(t=this.hass)||void 0===t||null===(t=t.entities[this.stateObj.entity_id])||void 0===t?void 0:t.icon)||(null===(e=this.stateObj)||void 0===e?void 0:e.attributes.icon);if(o)return(0,s.dy)(l||(l=v`<ha-icon .icon=${0}></ha-icon>`),o);if(!this.stateObj)return s.Ld;if(!this.hass)return this._renderFallback();const i=(0,c.gD)(this.hass,this.stateObj,this.stateValue).then((t=>t?(0,s.dy)(h||(h=v`<ha-icon .icon=${0}></ha-icon>`),t):this._renderFallback()));return(0,s.dy)(u||(u=v`${0}`),(0,r.C)(i))}_renderFallback(){const t=(0,n.N)(this.stateObj);return(0,s.dy)(p||(p=v`
      <ha-svg-icon
        .path=${0}
      ></ha-svg-icon>
    `),c.Ls[t]||c.Rb)}}(0,i.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"stateObj",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"stateValue",void 0),(0,i.__decorate)([(0,a.Cb)()],_.prototype,"icon",void 0),_=(0,i.__decorate)([(0,a.Mo)("ha-state-icon")],_),e()}catch(l){e(l)}}))},28177:function(t,e,o){o.d(e,{C:function(){return u}});o(26847),o(81738),o(29981),o(1455),o(27530);var i=o(35340),s=o(5277),a=o(93847);o(84730),o(15411),o(40777);class r{disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}constructor(t){this.G=t}}class n{get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null!==(t=this.Z)&&void 0!==t&&t.call(this),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var c=o(83522);const d=t=>!(0,s.pt)(t)&&"function"==typeof t.then,l=1073741823;class h extends a.sR{render(...t){var e;return null!==(e=t.find((t=>!d(t))))&&void 0!==e?e:i.Jb}update(t,e){const o=this._$Cbt;let s=o.length;this._$Cbt=e;const a=this._$CK,r=this._$CX;this.isConnected||this.disconnected();for(let i=0;i<e.length&&!(i>this._$Cwt);i++){const t=e[i];if(!d(t))return this._$Cwt=i,t;i<s&&t===o[i]||(this._$Cwt=l,s=0,Promise.resolve(t).then((async e=>{for(;r.get();)await r.get();const o=a.deref();if(void 0!==o){const i=o._$Cbt.indexOf(t);i>-1&&i<o._$Cwt&&(o._$Cwt=i,o.setValue(e))}})))}return i.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=l,this._$Cbt=[],this._$CK=new r(this),this._$CX=new n}}const u=(0,c.XM)(h)}}]);
//# sourceMappingURL=3254.9fad32ad17d99464.js.map