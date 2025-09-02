/*! For license information please see 8749.8009648273a312f1.js.LICENSE.txt */
export const __webpack_ids__=["8749"];export const __webpack_modules__={52245:function(e,t,i){i.a(e,(async function(e,t){try{var s=i(73742),r=i(59048),n=i(7616),a=i(28105),o=i(29740),d=i(27087),c=(i(48374),i(39711)),l=e([c]);c=(l.then?(await l)():l)[0];const h="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z";class u extends r.oi{render(){if(!this.hass)return r.Ld;const e=this._currentEntities;return r.dy`
      ${this.label?r.dy`<label>${this.label}</label>`:r.Ld}
      <ha-sortable
        .disabled=${!this.reorder||this.disabled}
        handle-selector=".entity-handle"
        @item-moved=${this._entityMoved}
      >
        <div class="list">
          ${e.map((e=>r.dy`
              <div class="entity">
                <ha-entity-picker
                  allow-custom-entity
                  .curValue=${e}
                  .hass=${this.hass}
                  .includeDomains=${this.includeDomains}
                  .excludeDomains=${this.excludeDomains}
                  .includeEntities=${this.includeEntities}
                  .excludeEntities=${this.excludeEntities}
                  .includeDeviceClasses=${this.includeDeviceClasses}
                  .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
                  .entityFilter=${this.entityFilter}
                  .value=${e}
                  .disabled=${this.disabled}
                  .createDomains=${this.createDomains}
                  @value-changed=${this._entityChanged}
                ></ha-entity-picker>
                ${this.reorder?r.dy`
                      <ha-svg-icon
                        class="entity-handle"
                        .path=${h}
                      ></ha-svg-icon>
                    `:r.Ld}
              </div>
            `))}
        </div>
      </ha-sortable>
      <div>
        <ha-entity-picker
          allow-custom-entity
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeEntities=${this.includeEntities}
          .excludeEntities=${this._excludeEntities(this.value,this.excludeEntities)}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
          .entityFilter=${this.entityFilter}
          .placeholder=${this.placeholder}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .createDomains=${this.createDomains}
          .required=${this.required&&!e.length}
          @value-changed=${this._addEntity}
        ></ha-entity-picker>
      </div>
    `}_entityMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,s=this._currentEntities,r=s[t],n=[...s];n.splice(t,1),n.splice(i,0,r),this._updateEntities(n)}get _currentEntities(){return this.value||[]}async _updateEntities(e){this.value=e,(0,o.B)(this,"value-changed",{value:e})}_entityChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,d.T)(i))return;const s=this._currentEntities;i&&!s.includes(i)?this._updateEntities(s.map((e=>e===t?i:e))):this._updateEntities(s.filter((e=>e!==t)))}async _addEntity(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.reorder=!1,this._excludeEntities=(0,a.Z)(((e,t)=>void 0===e?t:[...t||[],...e]))}}u.styles=r.iv`
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
  `,(0,s.__decorate)([(0,n.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array})],u.prototype,"value",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,s.__decorate)([(0,n.Cb)()],u.prototype,"label",void 0),(0,s.__decorate)([(0,n.Cb)()],u.prototype,"placeholder",void 0),(0,s.__decorate)([(0,n.Cb)()],u.prototype,"helper",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-domains"})],u.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"exclude-domains"})],u.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-device-classes"})],u.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-unit-of-measurement"})],u.prototype,"includeUnitOfMeasurement",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"include-entities"})],u.prototype,"includeEntities",void 0),(0,s.__decorate)([(0,n.Cb)({type:Array,attribute:"exclude-entities"})],u.prototype,"excludeEntities",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],u.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1,type:Array})],u.prototype,"createDomains",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],u.prototype,"reorder",void 0),u=(0,s.__decorate)([(0,n.Mo)("ha-entities-picker")],u),t()}catch(h){t(h)}}))},87393:function(e,t,i){i.a(e,(async function(e,s){try{i.r(t),i.d(t,{HaEntitySelector:()=>y});var r=i(73742),n=i(59048),a=i(7616),o=i(74608),d=i(29740),c=i(71170),l=i(45103),h=i(52245),u=i(39711),p=e([h,u]);[h,u]=p.then?(await p)():p;class y extends n.oi{_hasIntegration(e){return e.entity?.filter&&(0,o.r)(e.entity.filter).some((e=>e.integration))}willUpdate(e){e.get("selector")&&void 0!==this.value&&(this.selector.entity?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,d.B)(this,"value-changed",{value:this.value})):!this.selector.entity?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,d.B)(this,"value-changed",{value:this.value})))}render(){return this._hasIntegration(this.selector)&&!this._entitySources?n.Ld:this.selector.entity?.multiple?n.dy`
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .reorder=${this.selector.entity.reorder??!1}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entities-picker>
    `:n.dy`<ha-entity-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity?.include_entities}
        .excludeEntities=${this.selector.entity?.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-entity-picker>`}updated(e){super.updated(e),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,c.m)(this.hass).then((e=>{this._entitySources=e})),e.has("selector")&&(this._createDomains=(0,l.bq)(this.selector))}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._filterEntities=e=>!this.selector?.entity?.filter||(0,o.r)(this.selector.entity.filter).some((t=>(0,l.lV)(t,e,this._entitySources)))}}(0,r.__decorate)([(0,a.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,r.__decorate)([(0,a.Cb)({attribute:!1})],y.prototype,"selector",void 0),(0,r.__decorate)([(0,a.SB)()],y.prototype,"_entitySources",void 0),(0,r.__decorate)([(0,a.Cb)()],y.prototype,"value",void 0),(0,r.__decorate)([(0,a.Cb)()],y.prototype,"label",void 0),(0,r.__decorate)([(0,a.Cb)()],y.prototype,"helper",void 0),(0,r.__decorate)([(0,a.Cb)({type:Boolean})],y.prototype,"disabled",void 0),(0,r.__decorate)([(0,a.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,r.__decorate)([(0,a.SB)()],y.prototype,"_createDomains",void 0),y=(0,r.__decorate)([(0,a.Mo)("ha-selector-entity")],y),s()}catch(y){s(y)}}))},71170:function(e,t,i){i.d(t,{m:()=>n});const s=async(e,t,i,r,n,...a)=>{const o=n,d=o[e],c=d=>r&&r(n,d.result)!==d.cacheKey?(o[e]=void 0,s(e,t,i,r,n,...a)):d.result;if(d)return d instanceof Promise?d.then(c):c(d);const l=i(n,...a);return o[e]=l,l.then((i=>{o[e]={result:i,cacheKey:r?.(n,i)},setTimeout((()=>{o[e]=void 0}),t)}),(()=>{o[e]=void 0})),l},r=e=>e.callWS({type:"entity/source"}),n=e=>s("_entitySources",3e4,r,(e=>Object.keys(e.states).length),e)},12790:function(e,t,i){i.d(t,{C:()=>u});var s=i(35340),r=i(5277),n=i(93847);class a{disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}constructor(e){this.G=e}}class o{get(){return this.Y}pause(){this.Y??=new Promise((e=>this.Z=e))}resume(){this.Z?.(),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var d=i(83522);const c=e=>!(0,r.pt)(e)&&"function"==typeof e.then,l=1073741823;class h extends n.sR{render(...e){return e.find((e=>!c(e)))??s.Jb}update(e,t){const i=this._$Cbt;let r=i.length;this._$Cbt=t;const n=this._$CK,a=this._$CX;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$Cwt);s++){const e=t[s];if(!c(e))return this._$Cwt=s,e;s<r&&e===i[s]||(this._$Cwt=l,r=0,Promise.resolve(e).then((async t=>{for(;a.get();)await a.get();const i=n.deref();if(void 0!==i){const s=i._$Cbt.indexOf(e);s>-1&&s<i._$Cwt&&(i._$Cwt=s,i.setValue(t))}})))}return s.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=l,this._$Cbt=[],this._$CK=new a(this),this._$CX=new o}}const u=(0,d.XM)(h)}};
//# sourceMappingURL=8749.8009648273a312f1.js.map