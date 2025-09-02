export const __webpack_ids__=["727"];export const __webpack_modules__={49590:function(e,t,o){o.r(t),o.d(t,{HaIconPicker:()=>u});var i=o(73742),a=o(59048),s=o(7616),r=o(28105),n=o(29740),l=o(18610);o(90256),o(3847),o(57264);let c=[],d=!1;const h=async e=>{try{const t=l.g[e].getIconList;if("function"!=typeof t)return[];const o=await t();return o.map((t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]})))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},p=e=>a.dy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class u extends a.oi{render(){return a.dy`
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
        ${this._value||this.placeholder?a.dy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:a.dy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!d&&(await(async()=>{d=!0;const e=await o.e("4813").then(o.t.bind(o,81405,19));c=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(l.g).forEach((e=>{t.push(h(e))})),(await Promise.all(t)).forEach((e=>{c.push(...e)}))})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,r.Z)(((e,t=c)=>{if(!e)return t;const o=[],i=(e,t)=>o.push({icon:e,rank:t});for(const a of t)a.parts.has(e)?i(a.icon,1):a.keywords.includes(e)?i(a.icon,2):a.icon.includes(e)?i(a.icon,3):a.keywords.some((t=>t.includes(e)))&&i(a.icon,4);return 0===o.length&&i(e,0),o.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const o=this._filterIcons(e.filter.toLowerCase(),c),i=e.page*e.pageSize,a=i+e.pageSize;t(o.slice(i,a),o.length)}}}u.styles=a.iv`
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
  `,(0,i.__decorate)([(0,s.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,i.__decorate)([(0,s.Cb)()],u.prototype,"value",void 0),(0,i.__decorate)([(0,s.Cb)()],u.prototype,"label",void 0),(0,i.__decorate)([(0,s.Cb)()],u.prototype,"helper",void 0),(0,i.__decorate)([(0,s.Cb)()],u.prototype,"placeholder",void 0),(0,i.__decorate)([(0,s.Cb)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],u.prototype,"invalid",void 0),u=(0,i.__decorate)([(0,s.Mo)("ha-icon-picker")],u)},33767:function(e,t,o){o.r(t);var i=o(73742),a=o(59048),s=o(7616),r=o(29740),n=(o(49590),o(38573),o(77204));class l extends a.oi{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||""):(this._name="",this._icon="")}focus(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}render(){return this.hass?a.dy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
      </div>
    `:a.Ld}_valueChanged(e){if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,o=e.detail?.value||e.target.value;if(this[`_${t}`]===o)return;const i={...this._item};o?i[t]=o:delete i[t],(0,r.B)(this,"value-changed",{value:i})}static get styles(){return[n.Qx,a.iv`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          padding: 16px 0;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}constructor(...e){super(...e),this.new=!1}}(0,i.__decorate)([(0,s.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"new",void 0),(0,i.__decorate)([(0,s.SB)()],l.prototype,"_name",void 0),(0,i.__decorate)([(0,s.SB)()],l.prototype,"_icon",void 0),l=(0,i.__decorate)([(0,s.Mo)("ha-input_boolean-form")],l)}};
//# sourceMappingURL=727.5c830af471f2ec90.js.map