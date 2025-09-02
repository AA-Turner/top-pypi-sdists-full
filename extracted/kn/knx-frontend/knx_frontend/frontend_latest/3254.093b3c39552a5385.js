/*! For license information please see 3254.093b3c39552a5385.js.LICENSE.txt */
export const __webpack_ids__=["3254"];export const __webpack_modules__={49590:function(e,t,o){o.r(t),o.d(t,{HaIconPicker:()=>u});var i=o(73742),s=o(59048),a=o(7616),r=o(28105),n=o(29740),c=o(18610);o(90256),o(3847),o(57264);let h=[],d=!1;const l=async e=>{try{const t=c.g[e].getIconList;if("function"!=typeof t)return[];const o=await t();return o.map((t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]})))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},p=e=>s.dy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class u extends s.oi{render(){return s.dy`
      <ha-combo-box
        .hass=${this.hass}
        item-value-path="icon"
        item-label-path="icon"
        .value=${this._value}
        allow-custom-value
        .dataProvider=${d?this._iconProvider:void 0}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .placeholder=${this.placeholder}
        .errorMessage=${this.errorMessage}
        .invalid=${this.invalid}
        .renderer=${p}
        icon
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        ${this._value||this.placeholder?s.dy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:s.dy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!d&&(await(async()=>{d=!0;const e=await o.e("4813").then(o.t.bind(o,81405,19));h=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(c.g).forEach((e=>{t.push(l(e))})),(await Promise.all(t)).forEach((e=>{h.push(...e)}))})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,r.Z)(((e,t=h)=>{if(!e)return t;const o=[],i=(e,t)=>o.push({icon:e,rank:t});for(const s of t)s.parts.has(e)?i(s.icon,1):s.keywords.includes(e)?i(s.icon,2):s.icon.includes(e)?i(s.icon,3):s.keywords.some((t=>t.includes(e)))&&i(s.icon,4);return 0===o.length&&i(e,0),o.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const o=this._filterIcons(e.filter.toLowerCase(),h),i=e.page*e.pageSize,s=i+e.pageSize;t(o.slice(i,s),o.length)}}}u.styles=s.iv`
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
  `,(0,i.__decorate)([(0,a.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,i.__decorate)([(0,a.Cb)()],u.prototype,"value",void 0),(0,i.__decorate)([(0,a.Cb)()],u.prototype,"label",void 0),(0,i.__decorate)([(0,a.Cb)()],u.prototype,"helper",void 0),(0,i.__decorate)([(0,a.Cb)()],u.prototype,"placeholder",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,i.__decorate)([(0,a.Cb)({type:Boolean})],u.prototype,"invalid",void 0),u=(0,i.__decorate)([(0,a.Mo)("ha-icon-picker")],u)},37339:function(e,t,o){o.a(e,(async function(e,i){try{o.r(t),o.d(t,{HaIconSelector:()=>p});var s=o(73742),a=o(59048),r=o(7616),n=o(12790),c=o(29740),h=o(54974),d=(o(49590),o(27882)),l=e([d,h]);[d,h]=l.then?(await l)():l;class p extends a.oi{render(){const e=this.context?.icon_entity,t=e?this.hass.states[e]:void 0,o=this.selector.icon?.placeholder||t?.attributes.icon||t&&(0,n.C)((0,h.gD)(this.hass,t));return a.dy`
      <ha-icon-picker
        .hass=${this.hass}
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .placeholder=${this.selector.icon?.placeholder??o}
        @value-changed=${this._valueChanged}
      >
        ${!o&&t?a.dy`
              <ha-state-icon
                slot="fallback"
                .hass=${this.hass}
                .stateObj=${t}
              ></ha-state-icon>
            `:a.Ld}
      </ha-icon-picker>
    `}_valueChanged(e){(0,c.B)(this,"value-changed",{value:e.detail.value})}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}(0,s.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,s.__decorate)([(0,r.Cb)()],p.prototype,"value",void 0),(0,s.__decorate)([(0,r.Cb)()],p.prototype,"label",void 0),(0,s.__decorate)([(0,r.Cb)()],p.prototype,"helper",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"required",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"context",void 0),p=(0,s.__decorate)([(0,r.Mo)("ha-selector-icon")],p),i()}catch(p){i(p)}}))},27882:function(e,t,o){o.a(e,(async function(e,t){try{var i=o(73742),s=o(59048),a=o(7616),r=o(12790),n=o(18088),c=o(54974),h=(o(3847),o(40830),e([c]));c=(h.then?(await h)():h)[0];class d extends s.oi{render(){const e=this.icon||this.stateObj&&this.hass?.entities[this.stateObj.entity_id]?.icon||this.stateObj?.attributes.icon;if(e)return s.dy`<ha-icon .icon=${e}></ha-icon>`;if(!this.stateObj)return s.Ld;if(!this.hass)return this._renderFallback();const t=(0,c.gD)(this.hass,this.stateObj,this.stateValue).then((e=>e?s.dy`<ha-icon .icon=${e}></ha-icon>`:this._renderFallback()));return s.dy`${(0,r.C)(t)}`}_renderFallback(){const e=(0,n.N)(this.stateObj);return s.dy`
      <ha-svg-icon
        .path=${c.Ls[e]||c.Rb}
      ></ha-svg-icon>
    `}}(0,i.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"stateObj",void 0),(0,i.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"stateValue",void 0),(0,i.__decorate)([(0,a.Cb)()],d.prototype,"icon",void 0),d=(0,i.__decorate)([(0,a.Mo)("ha-state-icon")],d),t()}catch(d){t(d)}}))},12790:function(e,t,o){o.d(t,{C:()=>p});var i=o(35340),s=o(5277),a=o(93847);class r{disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}constructor(e){this.G=e}}class n{get(){return this.Y}pause(){this.Y??=new Promise((e=>this.Z=e))}resume(){this.Z?.(),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var c=o(83522);const h=e=>!(0,s.pt)(e)&&"function"==typeof e.then,d=1073741823;class l extends a.sR{render(...e){return e.find((e=>!h(e)))??i.Jb}update(e,t){const o=this._$Cbt;let s=o.length;this._$Cbt=t;const a=this._$CK,r=this._$CX;this.isConnected||this.disconnected();for(let i=0;i<t.length&&!(i>this._$Cwt);i++){const e=t[i];if(!h(e))return this._$Cwt=i,e;i<s&&e===o[i]||(this._$Cwt=d,s=0,Promise.resolve(e).then((async t=>{for(;r.get();)await r.get();const o=a.deref();if(void 0!==o){const i=o._$Cbt.indexOf(e);i>-1&&i<o._$Cwt&&(o._$Cwt=i,o.setValue(t))}})))}return i.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=d,this._$Cbt=[],this._$CK=new r(this),this._$CX=new n}}const p=(0,c.XM)(l)}};
//# sourceMappingURL=3254.093b3c39552a5385.js.map