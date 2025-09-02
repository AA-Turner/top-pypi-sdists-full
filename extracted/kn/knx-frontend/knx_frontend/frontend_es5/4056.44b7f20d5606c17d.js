"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["4056"],{49590:function(e,t,o){o.a(e,(async function(e,i){try{o.r(t),o.d(t,{HaIconPicker:function(){return k}});o(39710),o(26847),o(2394),o(18574),o(81738),o(94814),o(22960),o(6989),o(72489),o(1455),o(67886),o(65451),o(46015),o(38334),o(94880),o(75643),o(29761),o(56389),o(27530);var a=o(73742),r=o(59048),s=o(7616),n=o(28105),l=o(29740),c=o(18610),d=o(54693),h=(o(3847),o(57264),e([d]));d=(h.then?(await h)():h)[0];let u,p,v,_,g,b=e=>e,y=[],m=!1;const f=async()=>{m=!0;const e=await o.e("4813").then(o.t.bind(o,81405,19));y=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(c.g).forEach((e=>{t.push($(e))})),(await Promise.all(t)).forEach((e=>{y.push(...e)}))},$=async e=>{try{const t=c.g[e].getIconList;if("function"!=typeof t)return[];const o=await t();return o.map((t=>{var o;return{icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:null!==(o=t.keywords)&&void 0!==o?o:[]}}))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},w=e=>(0,r.dy)(u||(u=b`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    ${0}
  </ha-combo-box-item>
`),e.icon,e.icon);class k extends r.oi{render(){return(0,r.dy)(p||(p=b`
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
    `),this.hass,this._value,m?this._iconProvider:void 0,this.label,this.helper,this.disabled,this.required,this.placeholder,this.errorMessage,this.invalid,w,this._openedChanged,this._valueChanged,this._value||this.placeholder?(0,r.dy)(v||(v=b`
              <ha-icon .icon=${0} slot="icon">
              </ha-icon>
            `),this._value||this.placeholder):(0,r.dy)(_||(_=b`<slot slot="icon" name="fallback"></slot>`)))}async _openedChanged(e){e.detail.value&&!m&&(await f(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,l.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,n.Z)(((e,t=y)=>{if(!e)return t;const o=[],i=(e,t)=>o.push({icon:e,rank:t});for(const a of t)a.parts.has(e)?i(a.icon,1):a.keywords.includes(e)?i(a.icon,2):a.icon.includes(e)?i(a.icon,3):a.keywords.some((t=>t.includes(e)))&&i(a.icon,4);return 0===o.length&&i(e,0),o.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const o=this._filterIcons(e.filter.toLowerCase(),y),i=e.page*e.pageSize,a=i+e.pageSize;t(o.slice(i,a),o.length)}}}k.styles=(0,r.iv)(g||(g=b`
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
  `)),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],k.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)()],k.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],k.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],k.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)()],k.prototype,"placeholder",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"error-message"})],k.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],k.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],k.prototype,"required",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],k.prototype,"invalid",void 0),k=(0,a.__decorate)([(0,s.Mo)("ha-icon-picker")],k),i()}catch(u){i(u)}}))},60540:function(e,t,o){o.a(e,(async function(e,i){try{o.r(t);o(26847),o(87799),o(27530);var a=o(73742),r=o(59048),s=o(7616),n=o(29740),l=o(49590),c=(o(38573),o(77204)),d=e([l]);l=(d.then?(await d)():d)[0];let h,u,p=e=>e;class v extends r.oi{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||""):(this._name="",this._icon="")}focus(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}render(){return this.hass?(0,r.dy)(h||(h=p`
      <div class="form">
        <ha-textfield
          .value=${0}
          .configValue=${0}
          @input=${0}
          .label=${0}
          autoValidate
          required
          .validationMessage=${0}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${0}
          .value=${0}
          .configValue=${0}
          @value-changed=${0}
          .label=${0}
        ></ha-icon-picker>
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon")):r.Ld}_valueChanged(e){var t;if(!this.new&&!this._item)return;e.stopPropagation();const o=e.target.configValue,i=(null===(t=e.detail)||void 0===t?void 0:t.value)||e.target.value;if(this[`_${o}`]===i)return;const a=Object.assign({},this._item);i?a[o]=i:delete a[o],(0,n.B)(this,"value-changed",{value:a})}static get styles(){return[c.Qx,(0,r.iv)(u||(u=p`
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
      `))]}constructor(...e){super(...e),this.new=!1}}(0,a.__decorate)([(0,s.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],v.prototype,"new",void 0),(0,a.__decorate)([(0,s.SB)()],v.prototype,"_name",void 0),(0,a.__decorate)([(0,s.SB)()],v.prototype,"_icon",void 0),v=(0,a.__decorate)([(0,s.Mo)("ha-input_button-form")],v),i()}catch(h){i(h)}}))}}]);
//# sourceMappingURL=4056.44b7f20d5606c17d.js.map