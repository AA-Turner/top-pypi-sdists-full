"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["4751"],{37235:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(18574),i(81738),i(6989),i(87799),i(1455),i(27530);var o=i(73742),a=i(59048),n=i(7616),r=i(29740),s=i(92949),d=i(51068),l=i(47469),c=i(37198),h=i(54693),p=(i(57264),e([h]));h=(p.then?(await p)():p)[0];let u,_,b=e=>e;class y extends a.oi{open(){var e;null===(e=this._comboBox)||void 0===e||e.open()}focus(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}firstUpdated(){this._getConfigEntries()}render(){return this._configEntries?(0,a.dy)(u||(u=b`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        .renderer=${0}
        .items=${0}
        item-value-path="entry_id"
        item-id-path="entry_id"
        item-label-path="title"
        @value-changed=${0}
      ></ha-combo-box>
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.config-entry-picker.config_entry"):this.label,this._value,this.required,this.disabled,this.helper,this._rowRenderer,this._configEntries,this._valueChanged):a.Ld}_onImageLoad(e){e.target.style.visibility="initial"}_onImageError(e){e.target.style.visibility="hidden"}async _getConfigEntries(){(0,d.pB)(this.hass,{type:["device","hub","service"],domain:this.integration}).then((e=>{this._configEntries=e.map((e=>Object.assign(Object.assign({},e),{},{localized_domain_name:(0,l.Lh)(this.hass.localize,e.domain)}))).sort(((e,t)=>(0,s.fe)(e.localized_domain_name+e.title,t.localized_domain_name+t.title,this.hass.locale.language)))}))}get _value(){return this.value||""}_valueChanged(e){e.stopPropagation();const t=e.detail.value;t!==this._value&&this._setValue(t)}_setValue(e){this.value=e,setTimeout((()=>{(0,r.B)(this,"value-changed",{value:e}),(0,r.B)(this,"change")}),0)}constructor(...e){super(...e),this.value="",this.disabled=!1,this.required=!1,this._rowRenderer=e=>{var t;return(0,a.dy)(_||(_=b`
    <ha-combo-box-item type="button">
      <span slot="headline">
        ${0}
      </span>
      <span slot="supporting-text">${0}</span>
      <img
        alt=""
        slot="start"
        src=${0}
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
        @error=${0}
        @load=${0}
      />
    </ha-combo-box-item>
  `),e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry"),e.localized_domain_name,(0,c.X1)({domain:e.domain,type:"icon",darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode}),this._onImageError,this._onImageLoad)}}}(0,o.__decorate)([(0,n.Cb)()],y.prototype,"integration",void 0),(0,o.__decorate)([(0,n.Cb)()],y.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],y.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],y.prototype,"helper",void 0),(0,o.__decorate)([(0,n.SB)()],y.prototype,"_configEntries",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],y.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,o.__decorate)([(0,n.IO)("ha-combo-box")],y.prototype,"_comboBox",void 0),y=(0,o.__decorate)([(0,n.Mo)("ha-config-entry-picker")],y),t()}catch(u){t(u)}}))},33301:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{HaConfigEntrySelector:function(){return p}});i(26847),i(27530);var a=i(73742),n=i(59048),r=i(7616),s=i(37235),d=e([s]);s=(d.then?(await d)():d)[0];let l,c,h=e=>e;class p extends n.oi{render(){var e;return(0,n.dy)(l||(l=h`<ha-config-entry-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .disabled=${0}
      .required=${0}
      .integration=${0}
      allow-custom-entity
    ></ha-config-entry-picker>`),this.hass,this.value,this.label,this.helper,this.disabled,this.required,null===(e=this.selector.config_entry)||void 0===e?void 0:e.integration)}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}p.styles=(0,n.iv)(c||(c=h`
    ha-config-entry-picker {
      width: 100%;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,a.__decorate)([(0,r.Cb)()],p.prototype,"value",void 0),(0,a.__decorate)([(0,r.Cb)()],p.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)()],p.prototype,"helper",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"required",void 0),p=(0,a.__decorate)([(0,r.Mo)("ha-selector-config_entry")],p),o()}catch(l){o(l)}}))},47469:function(e,t,i){i.d(t,{F3:function(){return a},Lh:function(){return o},t4:function(){return n}});i(16811);const o=(e,t,i)=>e(`component.${t}.title`)||(null==i?void 0:i.name)||t,a=(e,t)=>{const i={type:"manifest/list"};return t&&(i.integrations=t),e.callWS(i)},n=(e,t)=>e.callWS({type:"manifest/get",integration:t})},37198:function(e,t,i){i.d(t,{X1:function(){return o},u4:function(){return a},zC:function(){return n}});i(44261);const o=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,a=e=>e.split("/")[4],n=e=>e.startsWith("https://brands.home-assistant.io/")}}]);
//# sourceMappingURL=4751.939049e88718e82f.js.map