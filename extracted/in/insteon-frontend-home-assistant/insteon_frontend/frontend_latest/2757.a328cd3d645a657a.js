export const __webpack_id__="2757";export const __webpack_ids__=["2757"];export const __webpack_modules__={87328:function(t,e,i){i.d(e,{aH:()=>r});var s=i(16727),a=i(91889);const n=[" ",": "," - "],o=t=>t.toLowerCase()!==t,r=(t,e,i)=>{const s=e[t.entity_id];return s?d(s,i):(0,a.u)(t)},d=(t,e,i)=>{const r=t.name||("original_name"in t&&null!=t.original_name?String(t.original_name):void 0),d=t.device_id?e[t.device_id]:void 0;if(!d)return r||(i?(0,a.u)(i):void 0);const c=(0,s.xn)(d);return c!==r?c&&r&&((t,e)=>{const i=t.toLowerCase(),s=e.toLowerCase();for(const a of n){const e=`${s}${a}`;if(i.startsWith(e)){const i=t.substring(e.length);if(i.length)return o(i.substr(0,i.indexOf(" ")))?i:i[0].toUpperCase()+i.slice(1)}}})(r,c)||r:void 0}},79384:function(t,e,i){i.d(e,{Cf:()=>d});var s=i(56403),a=i(16727),n=i(87328),o=i(47644),r=i(87400);const d=(t,e,i,d,c,l)=>{const{device:u,area:h,floor:p}=(0,r.l)(t,i,d,c,l);return e.map(e=>{switch(e.type){case"entity":return(0,n.aH)(t,i,d);case"device":return u?(0,a.xn)(u):void 0;case"area":return h?(0,s.A)(h):void 0;case"floor":return p?(0,o.X)(p):void 0;case"text":return e.text;default:return""}})}},45996:function(t,e,i){i.d(e,{n:()=>a});const s=/^(\w+)\.(\w+)$/,a=t=>s.test(t)},79599:function(t,e,i){function s(t){const e=t.language||"en";return t.translationMetadata.translations[e]&&t.translationMetadata.translations[e].isRTL||!1}function a(t){return n(s(t))}function n(t){return t?"rtl":"ltr"}i.d(e,{Vc:()=>a,qC:()=>s})},82965:function(t,e,i){i.a(t,async function(t,e){try{var s=i(62826),a=i(96196),n=i(77845),o=i(22786),r=i(92542),d=i(79384),c=i(45996),l=i(79599),u=i(22800),h=i(84125),p=i(50218),_=i(64070),y=(i(94343),i(96943)),g=(i(60961),i(91720)),m=t([y,g]);[y,g]=m.then?(await m)():m;const v="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",b="M11,13.5V21.5H3V13.5H11M12,2L17.5,11H6.5L12,2M17.5,13C20,13 22,15 22,17.5C22,20 20,22 17.5,22C15,22 13,20 13,17.5C13,15 15,13 17.5,13Z",f="___create-new-entity___";class $ extends a.WF{firstUpdated(t){super.firstUpdated(t),this.hass.loadBackendTranslation("title")}get _showEntityId(){return this.showEntityId||this.hass.userData?.showEntityIdPicker}render(){const t=this.placeholder??this.hass.localize("ui.components.entity.entity-picker.placeholder");return a.qy`
      <ha-generic-picker
        .hass=${this.hass}
        .disabled=${this.disabled}
        .autofocus=${this.autofocus}
        .allowCustomValue=${this.allowCustomEntity}
        .label=${this.label}
        .helper=${this.helper}
        .searchLabel=${this.searchLabel}
        .notFoundLabel=${this._notFoundLabel}
        .placeholder=${t}
        .value=${this.addButton?void 0:this.value}
        .rowRenderer=${this._rowRenderer}
        .getItems=${this._getItems}
        .getAdditionalItems=${this._getAdditionalItems}
        .hideClearIcon=${this.hideClearIcon}
        .searchFn=${this._searchFn}
        .valueRenderer=${this._valueRenderer}
        @value-changed=${this._valueChanged}
        .addButtonLabel=${this.addButton?this.hass.localize("ui.components.entity.entity-picker.add"):void 0}
      >
      </ha-generic-picker>
    `}async open(){await this.updateComplete,await(this._picker?.open())}_valueChanged(t){t.stopPropagation();const e=t.detail.value;if(e){if(e.startsWith(f)){const t=e.substring(f.length);return void(0,_.$)(this,{domain:t,dialogClosedCallback:t=>{t.entityId&&this._setValue(t.entityId)}})}(0,c.n)(e)&&this._setValue(e)}else this._setValue(void 0)}_setValue(t){this.value=t,(0,r.r)(this,"value-changed",{value:t}),(0,r.r)(this,"change")}constructor(...t){super(...t),this.autofocus=!1,this.disabled=!1,this.required=!1,this.showEntityId=!1,this.hideClearIcon=!1,this.addButton=!1,this._valueRenderer=t=>{const e=t||"",i=this.hass.states[e];if(!i)return a.qy`
        <ha-svg-icon
          slot="start"
          .path=${b}
          style="margin: 0 4px"
        ></ha-svg-icon>
        <span slot="headline">${e}</span>
      `;const[s,n,o]=(0,d.Cf)(i,[{type:"entity"},{type:"device"},{type:"area"}],this.hass.entities,this.hass.devices,this.hass.areas,this.hass.floors),r=(0,l.qC)(this.hass),c=s||n||e,u=[o,s?n:void 0].filter(Boolean).join(r?" ◂ ":" ▸ ");return a.qy`
      <state-badge
        .hass=${this.hass}
        .stateObj=${i}
        slot="start"
      ></state-badge>
      <span slot="headline">${c}</span>
      <span slot="supporting-text">${u}</span>
    `},this._rowRenderer=(t,{index:e})=>{const i=this._showEntityId;return a.qy`
      <ha-combo-box-item type="button" compact .borderTop=${0!==e}>
        ${t.icon_path?a.qy`
              <ha-svg-icon
                slot="start"
                style="margin: 0 4px"
                .path=${t.icon_path}
              ></ha-svg-icon>
            `:a.qy`
              <state-badge
                slot="start"
                .stateObj=${t.stateObj}
                .hass=${this.hass}
              ></state-badge>
            `}
        <span slot="headline">${t.primary}</span>
        ${t.secondary?a.qy`<span slot="supporting-text">${t.secondary}</span>`:a.s6}
        ${t.stateObj&&i?a.qy`
              <span slot="supporting-text" class="code">
                ${t.stateObj.entity_id}
              </span>
            `:a.s6}
        ${t.domain_name&&!i?a.qy`
              <div slot="trailing-supporting-text" class="domain">
                ${t.domain_name}
              </div>
            `:a.s6}
      </ha-combo-box-item>
    `},this._getAdditionalItems=()=>this._getCreateItems(this.hass.localize,this.createDomains),this._getCreateItems=(0,o.A)((t,e)=>e?.length?e.map(e=>{const i=t("ui.components.entity.entity-picker.create_helper",{domain:(0,p.z)(e)?t(`ui.panel.config.helpers.types.${e}`):(0,h.p$)(t,e)});return{id:f+e,primary:i,secondary:t("ui.components.entity.entity-picker.new_entity"),icon_path:v}}):[]),this._getEntitiesMemoized=(0,o.A)(u.wz),this._getItems=()=>this._getEntitiesMemoized(this.hass,this.includeDomains,this.excludeDomains,this.entityFilter,this.includeDeviceClasses,this.includeUnitOfMeasurement,this.includeEntities,this.excludeEntities,this.value),this._searchFn=(t,e)=>{const i=e.findIndex(e=>e.stateObj?.entity_id===t);if(-1===i)return e;const[s]=e.splice(i,1);return e.unshift(s),e},this._notFoundLabel=t=>this.hass.localize("ui.components.entity.entity-picker.no_match",{term:a.qy`<b>‘${t}’</b>`})}}(0,s.__decorate)([(0,n.MZ)({attribute:!1})],$.prototype,"hass",void 0),(0,s.__decorate)([(0,n.MZ)({type:Boolean})],$.prototype,"autofocus",void 0),(0,s.__decorate)([(0,n.MZ)({type:Boolean})],$.prototype,"disabled",void 0),(0,s.__decorate)([(0,n.MZ)({type:Boolean})],$.prototype,"required",void 0),(0,s.__decorate)([(0,n.MZ)({type:Boolean,attribute:"allow-custom-entity"})],$.prototype,"allowCustomEntity",void 0),(0,s.__decorate)([(0,n.MZ)({type:Boolean,attribute:"show-entity-id"})],$.prototype,"showEntityId",void 0),(0,s.__decorate)([(0,n.MZ)()],$.prototype,"label",void 0),(0,s.__decorate)([(0,n.MZ)()],$.prototype,"value",void 0),(0,s.__decorate)([(0,n.MZ)()],$.prototype,"helper",void 0),(0,s.__decorate)([(0,n.MZ)()],$.prototype,"placeholder",void 0),(0,s.__decorate)([(0,n.MZ)({type:String,attribute:"search-label"})],$.prototype,"searchLabel",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:!1,type:Array})],$.prototype,"createDomains",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"include-domains"})],$.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"exclude-domains"})],$.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"include-device-classes"})],$.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"include-unit-of-measurement"})],$.prototype,"includeUnitOfMeasurement",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"include-entities"})],$.prototype,"includeEntities",void 0),(0,s.__decorate)([(0,n.MZ)({type:Array,attribute:"exclude-entities"})],$.prototype,"excludeEntities",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:!1})],$.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:"hide-clear-icon",type:Boolean})],$.prototype,"hideClearIcon",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:"add-button",type:Boolean})],$.prototype,"addButton",void 0),(0,s.__decorate)([(0,n.P)("ha-generic-picker")],$.prototype,"_picker",void 0),$=(0,s.__decorate)([(0,n.EM)("ha-entity-picker")],$),e()}catch(v){e(v)}})},31136:function(t,e,i){i.d(e,{HV:()=>n,Hh:()=>a,KF:()=>r,ON:()=>o,g0:()=>l,s7:()=>d});var s=i(99245);const a="unavailable",n="unknown",o="on",r="off",d=[a,n],c=[a,n,r],l=(0,s.g)(d);(0,s.g)(c)},22800:function(t,e,i){i.d(e,{BM:()=>f,Bz:()=>m,G3:()=>p,G_:()=>_,Ox:()=>v,P9:()=>b,hN:()=>y,jh:()=>u,v:()=>h,wz:()=>$});var s=i(70570),a=i(22786),n=i(41144),o=i(79384),r=i(91889),d=(i(25749),i(79599)),c=i(40404),l=i(84125);const u=(t,e)=>{if(e.name)return e.name;const i=t.states[e.entity_id];return i?(0,r.u)(i):e.original_name?e.original_name:e.entity_id},h=(t,e)=>t.callWS({type:"config/entity_registry/get",entity_id:e}),p=(t,e)=>t.callWS({type:"config/entity_registry/get_entries",entity_ids:e}),_=(t,e,i)=>t.callWS({type:"config/entity_registry/update",entity_id:e,...i}),y=t=>t.sendMessagePromise({type:"config/entity_registry/list"}),g=(t,e)=>t.subscribeEvents((0,c.s)(()=>y(t).then(t=>e.setState(t,!0)),500,!0),"entity_registry_updated"),m=(t,e)=>(0,s.N)("_entityRegistry",y,g,t,e),v=(0,a.A)(t=>{const e={};for(const i of t)e[i.entity_id]=i;return e}),b=(0,a.A)(t=>{const e={};for(const i of t)e[i.id]=i;return e}),f=(t,e)=>t.callWS({type:"config/entity_registry/get_automatic_entity_ids",entity_ids:e}),$=(t,e,i,s,a,c,u,h,p,_="")=>{let y=[],g=Object.keys(t.states);return u&&(g=g.filter(t=>u.includes(t))),h&&(g=g.filter(t=>!h.includes(t))),e&&(g=g.filter(t=>e.includes((0,n.m)(t)))),i&&(g=g.filter(t=>!i.includes((0,n.m)(t)))),y=g.map(e=>{const i=t.states[e],s=(0,r.u)(i),[a,c,u]=(0,o.Cf)(i,[{type:"entity"},{type:"device"},{type:"area"}],t.entities,t.devices,t.areas,t.floors),h=(0,l.p$)(t.localize,(0,n.m)(e)),p=(0,d.qC)(t),y=a||c||e,g=[u,a?c:void 0].filter(Boolean).join(p?" ◂ ":" ▸ ");return{id:`${_}${e}`,primary:y,secondary:g,domain_name:h,sorting_label:[c,a].filter(Boolean).join("_"),search_labels:[a,c,u,h,s,e].filter(Boolean),stateObj:i}}),a&&(y=y.filter(t=>t.id===p||t.stateObj?.attributes.device_class&&a.includes(t.stateObj.attributes.device_class))),c&&(y=y.filter(t=>t.id===p||t.stateObj?.attributes.unit_of_measurement&&c.includes(t.stateObj.attributes.unit_of_measurement))),s&&(y=y.filter(t=>t.id===p||t.stateObj&&s(t.stateObj))),y}},64070:function(t,e,i){i.d(e,{$:()=>n});var s=i(92542);const a=()=>Promise.all([i.e("6767"),i.e("3785"),i.e("8738"),i.e("8991")]).then(i.bind(i,40386)),n=(t,e)=>{(0,s.r)(t,"show-dialog",{dialogTag:"dialog-helper-detail",dialogImport:a,dialogParams:e})}}};
//# sourceMappingURL=2757.a328cd3d645a657a.js.map