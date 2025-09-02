"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["2296"],{49590:function(e,i,t){t.a(e,(async function(e,a){try{t.r(i),t.d(i,{HaIconPicker:function(){return w}});t(39710),t(26847),t(2394),t(18574),t(81738),t(94814),t(22960),t(6989),t(72489),t(1455),t(67886),t(65451),t(46015),t(38334),t(94880),t(75643),t(29761),t(56389),t(27530);var o=t(73742),s=t(59048),n=t(7616),r=t(28105),l=t(29740),h=t(18610),d=t(54693),c=(t(3847),t(57264),e([d]));d=(c.then?(await c)():c)[0];let u,p,_,v,m,g=e=>e,y=[],b=!1;const $=async()=>{b=!0;const e=await t.e("4813").then(t.t.bind(t,81405,19));y=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const i=[];Object.keys(h.g).forEach((e=>{i.push(f(e))})),(await Promise.all(i)).forEach((e=>{y.push(...e)}))},f=async e=>{try{const i=h.g[e].getIconList;if("function"!=typeof i)return[];const t=await i();return t.map((i=>{var t;return{icon:`${e}:${i.name}`,parts:new Set(i.name.split("-")),keywords:null!==(t=i.keywords)&&void 0!==t?t:[]}}))}catch(i){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},x=e=>(0,s.dy)(u||(u=g`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    ${0}
  </ha-combo-box-item>
`),e.icon,e.icon);class w extends s.oi{render(){return(0,s.dy)(p||(p=g`
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
    `),this.hass,this._value,b?this._iconProvider:void 0,this.label,this.helper,this.disabled,this.required,this.placeholder,this.errorMessage,this.invalid,x,this._openedChanged,this._valueChanged,this._value||this.placeholder?(0,s.dy)(_||(_=g`
              <ha-icon .icon=${0} slot="icon">
              </ha-icon>
            `),this._value||this.placeholder):(0,s.dy)(v||(v=g`<slot slot="icon" name="fallback"></slot>`)))}async _openedChanged(e){e.detail.value&&!b&&(await $(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,l.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,r.Z)(((e,i=y)=>{if(!e)return i;const t=[],a=(e,i)=>t.push({icon:e,rank:i});for(const o of i)o.parts.has(e)?a(o.icon,1):o.keywords.includes(e)?a(o.icon,2):o.icon.includes(e)?a(o.icon,3):o.keywords.some((i=>i.includes(e)))&&a(o.icon,4);return 0===t.length&&a(e,0),t.sort(((e,i)=>e.rank-i.rank))})),this._iconProvider=(e,i)=>{const t=this._filterIcons(e.filter.toLowerCase(),y),a=e.page*e.pageSize,o=a+e.pageSize;i(t.slice(a,o),t.length)}}}w.styles=(0,s.iv)(m||(m=g`
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
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],w.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)()],w.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],w.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],w.prototype,"helper",void 0),(0,o.__decorate)([(0,n.Cb)()],w.prototype,"placeholder",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"error-message"})],w.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],w.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],w.prototype,"required",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],w.prototype,"invalid",void 0),w=(0,o.__decorate)([(0,n.Mo)("ha-icon-picker")],w),a()}catch(u){a(u)}}))},6184:function(e,i,t){t.a(e,(async function(e,a){try{t.r(i);t(26847),t(87799),t(27530);var o=t(73742),s=t(59048),n=t(7616),r=t(29740),l=(t(86932),t(49590)),h=(t(4820),t(38573),t(77204)),d=e([l]);l=(d.then?(await d)():d)[0];let c,u,p=e=>e;class _ extends s.oi{set item(e){var i,t,a,o,s;(this._item=e,e)?(this._name=e.name||"",this._icon=e.icon||"",this._maximum=null!==(i=e.maximum)&&void 0!==i?i:void 0,this._minimum=null!==(t=e.minimum)&&void 0!==t?t:void 0,this._restore=null===(a=e.restore)||void 0===a||a,this._step=null!==(o=e.step)&&void 0!==o?o:1,this._initial=null!==(s=e.initial)&&void 0!==s?s:0):(this._name="",this._icon="",this._maximum=void 0,this._minimum=void 0,this._restore=!0,this._step=1,this._initial=0)}focus(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}render(){return this.hass?(0,s.dy)(c||(c=p`
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
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-textfield
          .value=${0}
          .configValue=${0}
          type="number"
          @input=${0}
          .label=${0}
        ></ha-textfield>
        <ha-expansion-panel
          header=${0}
          outlined
        >
          <ha-textfield
            .value=${0}
            .configValue=${0}
            type="number"
            @input=${0}
            .label=${0}
          ></ha-textfield>
          <div class="row">
            <ha-switch
              .checked=${0}
              .configValue=${0}
              @change=${0}
            >
            </ha-switch>
            <div>
              ${0}
            </div>
          </div>
        </ha-expansion-panel>
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),this._minimum,"minimum",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.minimum"),this._maximum,"maximum",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.maximum"),this._initial,"initial",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.initial"),this.hass.localize("ui.dialogs.helper_settings.generic.advanced_settings"),this._step,"step",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.step"),this._restore,"restore",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.counter.restore")):s.Ld}_valueChanged(e){var i;if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target,a=t.configValue,o="number"===t.type?""!==t.value?Number(t.value):void 0:"ha-switch"===t.localName?e.target.checked:(null===(i=e.detail)||void 0===i?void 0:i.value)||t.value;if(this[`_${a}`]===o)return;const s=Object.assign({},this._item);void 0===o||""===o?delete s[a]:s[a]=o,(0,r.B)(this,"value-changed",{value:s})}static get styles(){return[h.Qx,(0,s.iv)(u||(u=p`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          margin-top: 12px;
          margin-bottom: 12px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .row div {
          margin-left: 16px;
          margin-inline-start: 16px;
          margin-inline-end: initial;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `))]}constructor(...e){super(...e),this.new=!1}}(0,o.__decorate)([(0,n.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],_.prototype,"new",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_name",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_icon",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_maximum",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_minimum",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_restore",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_initial",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_step",void 0),_=(0,o.__decorate)([(0,n.Mo)("ha-counter-form")],_),a()}catch(c){a(c)}}))}}]);
//# sourceMappingURL=2296.3371a6f97eb87ccc.js.map