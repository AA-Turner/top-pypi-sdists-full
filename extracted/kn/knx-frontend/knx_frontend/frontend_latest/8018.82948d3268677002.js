export const __webpack_ids__=["8018"];export const __webpack_modules__={49590:function(e,o,t){t.r(o),t.d(o,{HaIconPicker:()=>u});var a=t(73742),i=t(59048),r=t(7616),s=t(28105),n=t(29740),l=t(18610);t(90256),t(3847),t(57264);let c=[],d=!1;const h=async e=>{try{const o=l.g[e].getIconList;if("function"!=typeof o)return[];const t=await o();return t.map((o=>({icon:`${e}:${o.name}`,parts:new Set(o.name.split("-")),keywords:o.keywords??[]})))}catch(o){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},p=e=>i.dy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class u extends i.oi{render(){return i.dy`
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
        ${this._value||this.placeholder?i.dy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:i.dy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!d&&(await(async()=>{d=!0;const e=await t.e("4813").then(t.t.bind(t,81405,19));c=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const o=[];Object.keys(l.g).forEach((e=>{o.push(h(e))})),(await Promise.all(o)).forEach((e=>{c.push(...e)}))})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,s.Z)(((e,o=c)=>{if(!e)return o;const t=[],a=(e,o)=>t.push({icon:e,rank:o});for(const i of o)i.parts.has(e)?a(i.icon,1):i.keywords.includes(e)?a(i.icon,2):i.icon.includes(e)?a(i.icon,3):i.keywords.some((o=>o.includes(e)))&&a(i.icon,4);return 0===t.length&&a(e,0),t.sort(((e,o)=>e.rank-o.rank))})),this._iconProvider=(e,o)=>{const t=this._filterIcons(e.filter.toLowerCase(),c),a=e.page*e.pageSize,i=a+e.pageSize;o(t.slice(a,i),t.length)}}}u.styles=i.iv`
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
  `,(0,a.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"value",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"helper",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"placeholder",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"invalid",void 0),u=(0,a.__decorate)([(0,r.Mo)("ha-icon-picker")],u)}};
//# sourceMappingURL=8018.82948d3268677002.js.map