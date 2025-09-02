"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1697"],{59624:function(e,o,t){t.a(e,(async function(e,o){try{t(26847),t(18574),t(81738),t(94814),t(1455),t(27530);var a=t(73742),s=t(59048),r=t(7616),i=t(42822),d=t(29740),n=t(92949),l=t(81086),c=(t(22543),t(54693)),h=(t(57264),e([c]));c=(h.then?(await h)():h)[0];let p,u,_,b,v=e=>e;const y=e=>(0,s.dy)(p||(p=v`
  <ha-combo-box-item type="button">
    <span slot="headline">${0}</span>
    <span slot="supporting-text">${0}</span>
    ${0}
  </ha-combo-box-item>
`),e.name,e.slug,e.icon?(0,s.dy)(u||(u=v`
          <img
            alt=""
            slot="start"
            .src="/api/hassio/addons/${0}/icon"
          />
        `),e.slug):s.Ld);class m extends s.oi{open(){var e;null===(e=this._comboBox)||void 0===e||e.open()}focus(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}firstUpdated(){this._getAddons()}render(){return this._error?(0,s.dy)(_||(_=v`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):this._addons?(0,s.dy)(b||(b=v`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        .renderer=${0}
        .items=${0}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${0}
      ></ha-combo-box>
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label,this._value,this.required,this.disabled,this.helper,y,this._addons,this._addonChanged):s.Ld}async _getAddons(){try{if((0,i.p)(this.hass,"hassio")){const e=await(0,l.yt)(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,o)=>(0,n.$K)(e.name,o.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}get _value(){return this.value||""}_addonChanged(e){e.stopPropagation();const o=e.detail.value;o!==this._value&&this._setValue(o)}_setValue(e){this.value=e,setTimeout((()=>{(0,d.B)(this,"value-changed",{value:e}),(0,d.B)(this,"change")}),0)}constructor(...e){super(...e),this.value="",this.disabled=!1,this.required=!1}}(0,a.__decorate)([(0,r.Cb)()],m.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)()],m.prototype,"value",void 0),(0,a.__decorate)([(0,r.Cb)()],m.prototype,"helper",void 0),(0,a.__decorate)([(0,r.SB)()],m.prototype,"_addons",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],m.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],m.prototype,"required",void 0),(0,a.__decorate)([(0,r.IO)("ha-combo-box")],m.prototype,"_comboBox",void 0),(0,a.__decorate)([(0,r.SB)()],m.prototype,"_error",void 0),m=(0,a.__decorate)([(0,r.Mo)("ha-addon-picker")],m),o()}catch(p){o(p)}}))},38245:function(e,o,t){t.a(e,(async function(e,a){try{t.r(o),t.d(o,{HaAddonSelector:function(){return p}});t(26847),t(27530);var s=t(73742),r=t(59048),i=t(7616),d=t(59624),n=e([d]);d=(n.then?(await n)():n)[0];let l,c,h=e=>e;class p extends r.oi{render(){return(0,r.dy)(l||(l=h`<ha-addon-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .disabled=${0}
      .required=${0}
      allow-custom-entity
    ></ha-addon-picker>`),this.hass,this.value,this.label,this.helper,this.disabled,this.required)}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}p.styles=(0,r.iv)(c||(c=h`
    ha-addon-picker {
      width: 100%;
    }
  `)),(0,s.__decorate)([(0,i.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,i.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,s.__decorate)([(0,i.Cb)()],p.prototype,"value",void 0),(0,s.__decorate)([(0,i.Cb)()],p.prototype,"label",void 0),(0,s.__decorate)([(0,i.Cb)()],p.prototype,"helper",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],p.prototype,"required",void 0),p=(0,s.__decorate)([(0,i.Mo)("ha-selector-addon")],p),a()}catch(l){a(l)}}))},81086:function(e,o,t){t.d(o,{fU:function(){return d},kP:function(){return i},yt:function(){return r}});t(40777),t(81738),t(29981),t(1455);var a=t(35859),s=t(10840);const r=async e=>(0,a.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,s.rY)(await e.callApi("GET","hassio/addons")),i=async(e,o)=>(0,a.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/start`,method:"post",timeout:null}):e.callApi("POST",`hassio/addons/${o}/start`),d=async(e,o)=>{(0,a.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/install`,method:"post",timeout:null}):await e.callApi("POST",`hassio/addons/${o}/install`)}},10840:function(e,o,t){t.d(o,{js:function(){return s},rY:function(){return a}});t(39710),t(26847),t(1455),t(67886),t(65451),t(46015),t(38334),t(94880),t(75643),t(29761),t(56389),t(27530),t(35859);const a=e=>e.data,s=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}}]);
//# sourceMappingURL=1697.6b28c903fcbce55c.js.map