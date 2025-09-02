"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["7665"],{4910:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(81738),i(94814),i(6989),i(1455),i(56389),i(27530);var s=i(73742),r=i(59048),a=i(7616),o=i(29740),d=i(66299),c=i(99495),n=e([c]);c=(n.then?(await n)():n)[0];let l,h,u,v=e=>e;class p extends((0,d.f)(r.oi)){render(){if(!this.hass)return r.Ld;const e=this._currentAreas;return(0,r.dy)(l||(l=v`
      ${0}
      <div>
        <ha-area-picker
          .noAdd=${0}
          .hass=${0}
          .label=${0}
          .helper=${0}
          .includeDomains=${0}
          .excludeDomains=${0}
          .includeDeviceClasses=${0}
          .deviceFilter=${0}
          .entityFilter=${0}
          .disabled=${0}
          .placeholder=${0}
          .required=${0}
          @value-changed=${0}
          .excludeAreas=${0}
        ></ha-area-picker>
      </div>
    `),e.map((e=>(0,r.dy)(h||(h=v`
          <div>
            <ha-area-picker
              .curValue=${0}
              .noAdd=${0}
              .hass=${0}
              .value=${0}
              .label=${0}
              .includeDomains=${0}
              .excludeDomains=${0}
              .includeDeviceClasses=${0}
              .deviceFilter=${0}
              .entityFilter=${0}
              .disabled=${0}
              @value-changed=${0}
            ></ha-area-picker>
          </div>
        `),e,this.noAdd,this.hass,e,this.pickedAreaLabel,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.disabled,this._areaChanged))),this.noAdd,this.hass,this.pickAreaLabel,this.helper,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.disabled,this.placeholder,this.required&&!e.length,this._addArea,e)}get _currentAreas(){return this.value||[]}async _updateAreas(e){this.value=e,(0,o.B)(this,"value-changed",{value:e})}_areaChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t)return;const s=this._currentAreas;i&&!s.includes(i)?this._updateAreas(s.map((e=>e===t?i:e))):this._updateAreas(s.filter((e=>e!==t)))}_addArea(e){e.stopPropagation();const t=e.detail.value;if(!t)return;e.currentTarget.value="";const i=this._currentAreas;i.includes(t)||this._updateAreas([...i,t])}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1}}p.styles=(0,r.iv)(u||(u=v`
    div {
      margin-top: 8px;
    }
  `)),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,a.Cb)()],p.prototype,"label",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array})],p.prototype,"value",void 0),(0,s.__decorate)([(0,a.Cb)()],p.prototype,"helper",void 0),(0,s.__decorate)([(0,a.Cb)()],p.prototype,"placeholder",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean,attribute:"no-add"})],p.prototype,"noAdd",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"include-domains"})],p.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"exclude-domains"})],p.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"include-device-classes"})],p.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"deviceFilter",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:"picked-area-label"})],p.prototype,"pickedAreaLabel",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:"pick-area-label"})],p.prototype,"pickAreaLabel",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],p.prototype,"required",void 0),p=(0,s.__decorate)([(0,a.Mo)("ha-areas-picker")],p),t()}catch(l){t(l)}}))},97034:function(e,t,i){i.a(e,(async function(e,s){try{i.r(t),i.d(t,{HaAreaSelector:function(){return C}});i(26847),i(81738),i(72489),i(27530);var r=i(73742),a=i(59048),o=i(7616),d=i(28105),c=i(74608),n=i(57774),l=i(29740),h=i(71170),u=i(51068),v=i(45103),p=i(99495),_=i(4910),b=e([p,_]);[p,_]=b.then?(await b)():b;let y,$,f=e=>e;class C extends a.oi{_hasIntegration(e){var t,i;return(null===(t=e.area)||void 0===t?void 0:t.entity)&&(0,c.r)(e.area.entity).some((e=>e.integration))||(null===(i=e.area)||void 0===i?void 0:i.device)&&(0,c.r)(e.area.device).some((e=>e.integration))}willUpdate(e){var t,i;e.get("selector")&&void 0!==this.value&&(null!==(t=this.selector.area)&&void 0!==t&&t.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,l.B)(this,"value-changed",{value:this.value})):null!==(i=this.selector.area)&&void 0!==i&&i.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,l.B)(this,"value-changed",{value:this.value})))}updated(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,h.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,u.pB)(this.hass).then((e=>{this._configEntries=e})))}render(){var e,t,i,s,r;return this._hasIntegration(this.selector)&&!this._entitySources?a.Ld:null!==(e=this.selector.area)&&void 0!==e&&e.multiple?(0,a.dy)($||($=f`
      <ha-areas-picker
        .hass=${0}
        .value=${0}
        .helper=${0}
        .pickAreaLabel=${0}
        no-add
        .deviceFilter=${0}
        .entityFilter=${0}
        .disabled=${0}
        .required=${0}
      ></ha-areas-picker>
    `),this.hass,this.value,this.helper,this.label,null!==(t=this.selector.area)&&void 0!==t&&t.device?this._filterDevices:void 0,null!==(i=this.selector.area)&&void 0!==i&&i.entity?this._filterEntities:void 0,this.disabled,this.required):(0,a.dy)(y||(y=f`
        <ha-area-picker
          .hass=${0}
          .value=${0}
          .label=${0}
          .helper=${0}
          no-add
          .deviceFilter=${0}
          .entityFilter=${0}
          .disabled=${0}
          .required=${0}
        ></ha-area-picker>
      `),this.hass,this.value,this.label,this.helper,null!==(s=this.selector.area)&&void 0!==s&&s.device?this._filterDevices:void 0,null!==(r=this.selector.area)&&void 0!==r&&r.entity?this._filterEntities:void 0,this.disabled,this.required)}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._deviceIntegrationLookup=(0,d.Z)(n.HP),this._filterEntities=e=>{var t;return null===(t=this.selector.area)||void 0===t||!t.entity||(0,c.r)(this.selector.area.entity).some((t=>(0,v.lV)(t,e,this._entitySources)))},this._filterDevices=e=>{var t;if(null===(t=this.selector.area)||void 0===t||!t.device)return!0;const i=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,c.r)(this.selector.area.device).some((t=>(0,v.lE)(t,e,i)))}}}(0,r.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"hass",void 0),(0,r.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"selector",void 0),(0,r.__decorate)([(0,o.Cb)()],C.prototype,"value",void 0),(0,r.__decorate)([(0,o.Cb)()],C.prototype,"label",void 0),(0,r.__decorate)([(0,o.Cb)()],C.prototype,"helper",void 0),(0,r.__decorate)([(0,o.Cb)({type:Boolean})],C.prototype,"disabled",void 0),(0,r.__decorate)([(0,o.Cb)({type:Boolean})],C.prototype,"required",void 0),(0,r.__decorate)([(0,o.SB)()],C.prototype,"_entitySources",void 0),(0,r.__decorate)([(0,o.SB)()],C.prototype,"_configEntries",void 0),C=(0,r.__decorate)([(0,o.Mo)("ha-selector-area")],C),s()}catch(y){s(y)}}))},71170:function(e,t,i){i.d(t,{m:function(){return a}});i(26847),i(1455),i(27530);const s=async(e,t,i,r,a,...o)=>{const d=a,c=d[e],n=c=>r&&r(a,c.result)!==c.cacheKey?(d[e]=void 0,s(e,t,i,r,a,...o)):c.result;if(c)return c instanceof Promise?c.then(n):n(c);const l=i(a,...o);return d[e]=l,l.then((i=>{d[e]={result:i,cacheKey:null==r?void 0:r(a,i)},setTimeout((()=>{d[e]=void 0}),t)}),(()=>{d[e]=void 0})),l},r=e=>e.callWS({type:"entity/source"}),a=e=>s("_entitySources",3e4,r,(e=>Object.keys(e.states).length),e)},66299:function(e,t,i){i.d(t,{f:function(){return a}});i(39710),i(26847),i(81738),i(72489),i(1455),i(56389),i(27530);var s=i(73742),r=i(7616);const a=e=>{class t extends e{connectedCallback(){super.connectedCallback(),this._checkSubscribed()}disconnectedCallback(){if(super.disconnectedCallback(),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}updated(e){if(super.updated(e),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this._checkSubscribed()}hassSubscribe(){return[]}_checkSubscribed(){var e;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(e=this.hassSubscribeRequiredHostProps)&&void 0!==e&&e.some((e=>void 0===this[e]))||(this.__unsubs=this.hassSubscribe())}}return(0,s.__decorate)([(0,r.Cb)({attribute:!1})],t.prototype,"hass",void 0),t}}}]);
//# sourceMappingURL=7665.863a8a21f2e49a19.js.map