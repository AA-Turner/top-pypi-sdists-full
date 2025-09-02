/*! For license information please see 1345.9e809796515bfa63.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1345"],{52245:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(81738),i(94814),i(6989),i(1455),i(56389),i(27530);var s=i(73742),r=i(59048),n=i(7616),o=i(28105),a=i(29740),l=i(27087),d=(i(48374),i(39711)),c=e([d]);d=(c.then?(await c)():c)[0];let u,h,p,y,v,_=e=>e;const b="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z";class $ extends r.oi{render(){if(!this.hass)return r.Ld;const e=this._currentEntities;return(0,r.dy)(u||(u=_`
      ${0}
      <ha-sortable
        .disabled=${0}
        handle-selector=".entity-handle"
        @item-moved=${0}
      >
        <div class="list">
          ${0}
        </div>
      </ha-sortable>
      <div>
        <ha-entity-picker
          allow-custom-entity
          .hass=${0}
          .includeDomains=${0}
          .excludeDomains=${0}
          .includeEntities=${0}
          .excludeEntities=${0}
          .includeDeviceClasses=${0}
          .includeUnitOfMeasurement=${0}
          .entityFilter=${0}
          .placeholder=${0}
          .helper=${0}
          .disabled=${0}
          .createDomains=${0}
          .required=${0}
          @value-changed=${0}
        ></ha-entity-picker>
      </div>
    `),this.label?(0,r.dy)(h||(h=_`<label>${0}</label>`),this.label):r.Ld,!this.reorder||this.disabled,this._entityMoved,e.map((e=>(0,r.dy)(p||(p=_`
              <div class="entity">
                <ha-entity-picker
                  allow-custom-entity
                  .curValue=${0}
                  .hass=${0}
                  .includeDomains=${0}
                  .excludeDomains=${0}
                  .includeEntities=${0}
                  .excludeEntities=${0}
                  .includeDeviceClasses=${0}
                  .includeUnitOfMeasurement=${0}
                  .entityFilter=${0}
                  .value=${0}
                  .disabled=${0}
                  .createDomains=${0}
                  @value-changed=${0}
                ></ha-entity-picker>
                ${0}
              </div>
            `),e,this.hass,this.includeDomains,this.excludeDomains,this.includeEntities,this.excludeEntities,this.includeDeviceClasses,this.includeUnitOfMeasurement,this.entityFilter,e,this.disabled,this.createDomains,this._entityChanged,this.reorder?(0,r.dy)(y||(y=_`
                      <ha-svg-icon
                        class="entity-handle"
                        .path=${0}
                      ></ha-svg-icon>
                    `),b):r.Ld))),this.hass,this.includeDomains,this.excludeDomains,this.includeEntities,this._excludeEntities(this.value,this.excludeEntities),this.includeDeviceClasses,this.includeUnitOfMeasurement,this.entityFilter,this.placeholder,this.helper,this.disabled,this.createDomains,this.required&&!e.length,this._addEntity)}_entityMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,s=this._currentEntities,r=s[t],n=[...s];n.splice(t,1),n.splice(i,0,r),this._updateEntities(n)}get _currentEntities(){return this.value||[]}async _updateEntities(e){this.value=e,(0,a.B)(this,"value-changed",{value:e})}_entityChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,l.T)(i))return;const s=this._currentEntities;i&&!s.includes(i)?this._updateEntities(s.map((e=>e===t?i:e))):this._updateEntities(s.filter((e=>e!==t)))}async _addEntity(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.reorder=!1,this._excludeEntities=(0,o.Z)(((e,t)=>void 0===e?t:[...t||[],...e]))}}$.styles=(0,r.iv)(v||(v=_`
    div {
      margin-top: 8px;
    }
    label {
      display: block;
      margin: 0 0 8px;
    }
    .entity {
      display: flex;
      flex-direction: row;
      align-items: center;
    }
    .entity ha-entity-picker {
      flex: 1;
    }
    .entity-handle {
      padding: 8px;
      cursor: move; /* fallback if grab cursor is unsupported */
      cursor: grab;
    }
  `)),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array})],$.prototype,"value",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"disabled",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"required",void 0),(0,s.__decorate)([(0,n.Cb)()],$.prototype,"label",void 0),(0,s.__decorate)([(0,n.Cb)()],$.prototype,"placeholder",void 0),(0,s.__decorate)([(0,n.Cb)()],$.prototype,"helper",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-domains"})],$.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"exclude-domains"})],$.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-device-classes"})],$.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-unit-of-measurement"})],$.prototype,"includeUnitOfMeasurement",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-entities"})],$.prototype,"includeEntities",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"exclude-entities"})],$.prototype,"excludeEntities",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],$.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1,type:Array})],$.prototype,"createDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"reorder",void 0),$=(0,s.__decorate)([(0,n.Mo)("ha-entities-picker")],$),t()}catch(u){t(u)}}))},87393:function(e,t,i){i.a(e,(async function(e,s){try{i.r(t),i.d(t,{HaEntitySelector:function(){return b}});i(26847),i(81738),i(94814),i(72489),i(27530);var r=i(73742),n=i(59048),o=i(7616),a=i(74608),l=i(29740),d=i(71170),c=i(45103),u=i(52245),h=i(39711),p=e([u,h]);[u,h]=p.then?(await p)():p;let y,v,_=e=>e;class b extends n.oi{_hasIntegration(e){var t;return(null===(t=e.entity)||void 0===t?void 0:t.filter)&&(0,a.r)(e.entity.filter).some((e=>e.integration))}willUpdate(e){var t,i;e.get("selector")&&void 0!==this.value&&(null!==(t=this.selector.entity)&&void 0!==t&&t.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,l.B)(this,"value-changed",{value:this.value})):null!==(i=this.selector.entity)&&void 0!==i&&i.multiple||!Array.isArray(this.value)||(this.value=this.value[0],(0,l.B)(this,"value-changed",{value:this.value})))}render(){var e,t,i,s;return this._hasIntegration(this.selector)&&!this._entitySources?n.Ld:null!==(e=this.selector.entity)&&void 0!==e&&e.multiple?(0,n.dy)(v||(v=_`
      <ha-entities-picker
        .hass=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .includeEntities=${0}
        .excludeEntities=${0}
        .reorder=${0}
        .entityFilter=${0}
        .createDomains=${0}
        .disabled=${0}
        .required=${0}
      ></ha-entities-picker>
    `),this.hass,this.value,this.label,this.helper,this.selector.entity.include_entities,this.selector.entity.exclude_entities,null!==(t=this.selector.entity.reorder)&&void 0!==t&&t,this._filterEntities,this._createDomains,this.disabled,this.required):(0,n.dy)(y||(y=_`<ha-entity-picker
        .hass=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .includeEntities=${0}
        .excludeEntities=${0}
        .entityFilter=${0}
        .createDomains=${0}
        .disabled=${0}
        .required=${0}
        allow-custom-entity
      ></ha-entity-picker>`),this.hass,this.value,this.label,this.helper,null===(i=this.selector.entity)||void 0===i?void 0:i.include_entities,null===(s=this.selector.entity)||void 0===s?void 0:s.exclude_entities,this._filterEntities,this._createDomains,this.disabled,this.required)}updated(e){super.updated(e),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,d.m)(this.hass).then((e=>{this._entitySources=e})),e.has("selector")&&(this._createDomains=(0,c.bq)(this.selector))}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._filterEntities=e=>{var t;return null===(t=this.selector)||void 0===t||null===(t=t.entity)||void 0===t||!t.filter||(0,a.r)(this.selector.entity.filter).some((t=>(0,c.lV)(t,e,this._entitySources)))}}}(0,r.__decorate)([(0,o.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,r.__decorate)([(0,o.Cb)({attribute:!1})],b.prototype,"selector",void 0),(0,r.__decorate)([(0,o.SB)()],b.prototype,"_entitySources",void 0),(0,r.__decorate)([(0,o.Cb)()],b.prototype,"value",void 0),(0,r.__decorate)([(0,o.Cb)()],b.prototype,"label",void 0),(0,r.__decorate)([(0,o.Cb)()],b.prototype,"helper",void 0),(0,r.__decorate)([(0,o.Cb)({type:Boolean})],b.prototype,"disabled",void 0),(0,r.__decorate)([(0,o.Cb)({type:Boolean})],b.prototype,"required",void 0),(0,r.__decorate)([(0,o.SB)()],b.prototype,"_createDomains",void 0),b=(0,r.__decorate)([(0,o.Mo)("ha-selector-entity")],b),s()}catch(y){s(y)}}))},71170:function(e,t,i){i.d(t,{m:function(){return n}});i(26847),i(1455),i(27530);const s=async(e,t,i,r,n,...o)=>{const a=n,l=a[e],d=l=>r&&r(n,l.result)!==l.cacheKey?(a[e]=void 0,s(e,t,i,r,n,...o)):l.result;if(l)return l instanceof Promise?l.then(d):d(l);const c=i(n,...o);return a[e]=c,c.then((i=>{a[e]={result:i,cacheKey:null==r?void 0:r(n,i)},setTimeout((()=>{a[e]=void 0}),t)}),(()=>{a[e]=void 0})),c},r=e=>e.callWS({type:"entity/source"}),n=e=>s("_entitySources",3e4,r,(e=>Object.keys(e.states).length),e)},28177:function(e,t,i){i.d(t,{C:function(){return h}});i(26847),i(81738),i(29981),i(1455),i(27530);var s=i(35340),r=i(5277),n=i(93847);i(84730),i(15411),i(40777);class o{disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}constructor(e){this.G=e}}class a{get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null!==(e=this.Z)&&void 0!==e&&e.call(this),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var l=i(83522);const d=e=>!(0,r.pt)(e)&&"function"==typeof e.then,c=1073741823;class u extends n.sR{render(...e){var t;return null!==(t=e.find((e=>!d(e))))&&void 0!==t?t:s.Jb}update(e,t){const i=this._$Cbt;let r=i.length;this._$Cbt=t;const n=this._$CK,o=this._$CX;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$Cwt);s++){const e=t[s];if(!d(e))return this._$Cwt=s,e;s<r&&e===i[s]||(this._$Cwt=c,r=0,Promise.resolve(e).then((async t=>{for(;o.get();)await o.get();const i=n.deref();if(void 0!==i){const s=i._$Cbt.indexOf(e);s>-1&&s<i._$Cwt&&(i._$Cwt=s,i.setValue(t))}})))}return s.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=c,this._$Cbt=[],this._$CK=new o(this),this._$CX=new a}}const h=(0,l.XM)(u)}}]);
//# sourceMappingURL=1345.9e809796515bfa63.js.map