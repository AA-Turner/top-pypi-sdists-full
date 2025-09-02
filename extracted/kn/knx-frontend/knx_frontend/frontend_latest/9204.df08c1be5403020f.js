export const __webpack_ids__=["9204"];export const __webpack_modules__={12951:function(e,t,i){i.d(t,{I:()=>s,k:()=>a});const a=new Set(["primary","accent","disabled","red","pink","purple","deep-purple","indigo","blue","light-blue","cyan","teal","green","light-green","lime","yellow","amber","orange","deep-orange","brown","light-grey","grey","dark-grey","blue-grey","black","white"]);function s(e){return a.has(e)?`var(--${e}-color)`:e}},90024:function(e,t,i){var a=i(73742),s=i(59048),o=i(7616),l=i(28105),r=i(29740),c=i(76151),n=i(51729),d=i(42846),h=i(81665),p=i(66299),u=i(76948);i(75691),i(40830);const _="M17.63,5.84C17.27,5.33 16.67,5 16,5H5A2,2 0 0,0 3,7V17A2,2 0 0,0 5,19H16C16.67,19 17.27,18.66 17.63,18.15L22,12L17.63,5.84Z",b="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",y="___ADD_NEW___",v="___NO_LABELS___";class m extends((0,p.f)(s.oi)){async open(){await this.updateComplete,await(this._picker?.open())}hassSubscribe(){return[(0,d.f4)(this.hass.connection,(e=>{this._labels=e}))]}render(){const e=this.placeholder??this.hass.localize("ui.components.label-picker.label"),t=this._computeValueRenderer(this._labels);return s.dy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .label=${this.label}
        .notFoundLabel=${this.hass.localize("ui.components.label-picker.no_match")}
        .placeholder=${e}
        .value=${this.value}
        .getItems=${this._getItems}
        .getAdditionalItems=${this._getAdditionalItems}
        .valueRenderer=${t}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}_valueChanged(e){e.stopPropagation();const t=e.detail.value;if(t!==v)if(t)if(t.startsWith(y)){this.hass.loadFragmentTranslation("config");const e=t.substring(13);(0,u.T)(this,{suggestedName:e,createEntry:async e=>{try{const t=await(0,d.jo)(this.hass,e);this._setValue(t.label_id)}catch(t){(0,h.Ys)(this,{title:this.hass.localize("ui.components.label-picker.failed_create_label"),text:t.message})}}})}else this._setValue(t);else this._setValue(void 0)}_setValue(e){this.value=e,setTimeout((()=>{(0,r.B)(this,"value-changed",{value:e}),(0,r.B)(this,"change")}),0)}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1,this._labelMap=(0,l.Z)((e=>e?new Map(e.map((e=>[e.label_id,e]))):new Map)),this._computeValueRenderer=(0,l.Z)((e=>t=>{const i=this._labelMap(e).get(t);return i?s.dy`
          ${i.icon?s.dy`<ha-icon slot="start" .icon=${i.icon}></ha-icon>`:s.dy`<ha-svg-icon slot="start" .path=${_}></ha-svg-icon>`}
          <span slot="headline">${i.name}</span>
        `:s.dy`
            <ha-svg-icon slot="start" .path=${_}></ha-svg-icon>
            <span slot="headline">${t}</span>
          `})),this._getLabels=(0,l.Z)(((e,t,i,a,s,o,l,r,d,h)=>{if(!e||0===e.length)return[{id:v,primary:this.hass.localize("ui.components.label-picker.no_labels"),icon_path:_}];const p=Object.values(i),u=Object.values(a);let b,y,m={};(s||o||l||r||d)&&(m=(0,n.R6)(u),b=p,y=u.filter((e=>e.labels.length>0)),s&&(b=b.filter((e=>{const t=m[e.id];return!(!t||!t.length)&&m[e.id].some((e=>s.includes((0,c.M)(e.entity_id))))})),y=y.filter((e=>s.includes((0,c.M)(e.entity_id))))),o&&(b=b.filter((e=>{const t=m[e.id];return!t||!t.length||u.every((e=>!o.includes((0,c.M)(e.entity_id))))})),y=y.filter((e=>!o.includes((0,c.M)(e.entity_id))))),l&&(b=b.filter((e=>{const t=m[e.id];return!(!t||!t.length)&&m[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&l.includes(t.attributes.device_class))}))})),y=y.filter((e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&l.includes(t.attributes.device_class)}))),r&&(b=b.filter((e=>r(e)))),d&&(b=b.filter((e=>{const t=m[e.id];return!(!t||!t.length)&&m[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&d(t)}))})),y=y.filter((e=>{const t=this.hass.states[e.entity_id];return!!t&&d(t)}))));let g=e;const f=new Set;let C;b&&(C=b.filter((e=>e.area_id)).map((e=>e.area_id)),b.forEach((e=>{e.labels.forEach((e=>f.add(e)))}))),y&&(C=(C??[]).concat(y.filter((e=>e.area_id)).map((e=>e.area_id))),y.forEach((e=>{e.labels.forEach((e=>f.add(e)))}))),C&&C.forEach((e=>{t[e].labels.forEach((e=>f.add(e)))})),h&&(g=g.filter((e=>!h.includes(e.label_id)))),(b||y)&&(g=g.filter((e=>f.has(e.label_id))));return g.map((e=>({id:e.label_id,primary:e.name,icon:e.icon||void 0,icon_path:e.icon?void 0:_,sorting_label:e.name,search_labels:[e.name,e.label_id,e.description].filter((e=>Boolean(e)))})))})),this._getItems=()=>this._getLabels(this._labels,this.hass.areas,this.hass.devices,this.hass.entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeLabels),this._allLabelNames=(0,l.Z)((e=>e?[...new Set(e.map((e=>e.name.toLowerCase())).filter(Boolean))]:[])),this._getAdditionalItems=e=>{if(this.noAdd)return[];const t=this._allLabelNames(this._labels);return e&&!t.includes(e.toLowerCase())?[{id:y+e,primary:this.hass.localize("ui.components.label-picker.add_new_sugestion",{name:e}),icon_path:b}]:[{id:y,primary:this.hass.localize("ui.components.label-picker.add_new"),icon_path:b}]}}}(0,a.__decorate)([(0,o.Cb)({attribute:!1})],m.prototype,"hass",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"value",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"helper",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"placeholder",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean,attribute:"no-add"})],m.prototype,"noAdd",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"include-domains"})],m.prototype,"includeDomains",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-domains"})],m.prototype,"excludeDomains",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"include-device-classes"})],m.prototype,"includeDeviceClasses",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-label"})],m.prototype,"excludeLabels",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],m.prototype,"deviceFilter",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],m.prototype,"entityFilter",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],m.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],m.prototype,"required",void 0),(0,a.__decorate)([(0,o.SB)()],m.prototype,"_labels",void 0),(0,a.__decorate)([(0,o.IO)("ha-generic-picker")],m.prototype,"_picker",void 0),m=(0,a.__decorate)([(0,o.Mo)("ha-label-picker")],m)},19442:function(e,t,i){var a=i(73742),s=i(59048),o=i(7616),l=i(88245),r=i(28105),c=i(12951),n=i(29740),d=i(92949),h=i(42846),p=i(66299),u=i(76948);i(2414),i(91572),i(90024);class _ extends((0,p.f)(s.oi)){async open(){await this.updateComplete,await(this.labelPicker?.open())}async focus(){await this.updateComplete,await(this.labelPicker?.focus())}hassSubscribe(){return[(0,h.f4)(this.hass.connection,(e=>{const t={};e.forEach((e=>{t[e.label_id]=e})),this._labels=t}))]}render(){const e=this._sortedLabels(this.value,this._labels,this.hass.locale.language);return s.dy`
      ${this.label?s.dy`<label>${this.label}</label>`:s.Ld}
      ${e?.length?s.dy`<ha-chip-set>
            ${(0,l.r)(e,(e=>e?.label_id),(e=>{const t=e?.color?(0,c.I)(e.color):void 0;return s.dy`
                  <ha-input-chip
                    .item=${e}
                    @remove=${this._removeItem}
                    @click=${this._openDetail}
                    .label=${e?.name}
                    selected
                    style=${t?`--color: ${t}`:""}
                  >
                    ${e?.icon?s.dy`<ha-icon
                          slot="icon"
                          .icon=${e.icon}
                        ></ha-icon>`:s.Ld}
                  </ha-input-chip>
                `}))}
          </ha-chip-set>`:s.Ld}
      <ha-label-picker
        .hass=${this.hass}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .placeholder=${this.placeholder}
        .excludeLabels=${this.value}
        @value-changed=${this._labelChanged}
      >
      </ha-label-picker>
    `}get _value(){return this.value||[]}_removeItem(e){const t=e.currentTarget.item;this._setValue(this._value.filter((e=>e!==t.label_id)))}_openDetail(e){const t=e.currentTarget.item;(0,u.T)(this,{entry:t,updateEntry:async e=>{await(0,h.$0)(this.hass,t.label_id,e)}})}_labelChanged(e){e.stopPropagation();const t=e.detail.value;t&&!this._value.includes(t)&&(this._setValue([...this._value,t]),this.labelPicker.value="")}_setValue(e){this.value=e,setTimeout((()=>{(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}),0)}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1,this._sortedLabels=(0,r.Z)(((e,t,i)=>e?.map((e=>t?.[e])).sort(((e,t)=>(0,d.$K)(e?.name||"",t?.name||"",i)))))}}_.styles=s.iv`
    ha-chip-set {
      margin-bottom: 8px;
    }
    ha-input-chip {
      --md-input-chip-selected-container-color: var(--color, var(--grey-color));
      --ha-input-chip-selected-container-opacity: 0.5;
      --md-input-chip-selected-outline-width: 1px;
    }
    label {
      display: block;
      margin: 0 0 8px;
    }
  `,(0,a.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,a.__decorate)([(0,o.Cb)()],_.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"value",void 0),(0,a.__decorate)([(0,o.Cb)()],_.prototype,"helper",void 0),(0,a.__decorate)([(0,o.Cb)()],_.prototype,"placeholder",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean,attribute:"no-add"})],_.prototype,"noAdd",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"include-domains"})],_.prototype,"includeDomains",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-domains"})],_.prototype,"excludeDomains",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"include-device-classes"})],_.prototype,"includeDeviceClasses",void 0),(0,a.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-label"})],_.prototype,"excludeLabels",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"deviceFilter",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"entityFilter",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],_.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],_.prototype,"required",void 0),(0,a.__decorate)([(0,o.SB)()],_.prototype,"_labels",void 0),(0,a.__decorate)([(0,o.IO)("ha-label-picker",!0)],_.prototype,"labelPicker",void 0),_=(0,a.__decorate)([(0,o.Mo)("ha-labels-picker")],_)},42846:function(e,t,i){i.d(t,{$0:()=>d,f4:()=>c,jo:()=>n});var a=i(88865),s=i(92949),o=i(16811);const l=e=>e.sendMessagePromise({type:"config/label_registry/list"}).then((e=>e.sort(((e,t)=>(0,s.$K)(e.name,t.name))))),r=(e,t)=>e.subscribeEvents((0,o.D)((()=>l(e).then((e=>t.setState(e,!0)))),500,!0),"label_registry_updated"),c=(e,t)=>(0,a.B)("_labelRegistry",l,r,e,t),n=(e,t)=>e.callWS({type:"config/label_registry/create",...t}),d=(e,t,i)=>e.callWS({type:"config/label_registry/update",label_id:t,...i})},66299:function(e,t,i){i.d(t,{f:()=>o});var a=i(73742),s=i(7616);const o=e=>{class t extends e{connectedCallback(){super.connectedCallback(),this._checkSubscribed()}disconnectedCallback(){if(super.disconnectedCallback(),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}updated(e){if(super.updated(e),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this._checkSubscribed()}hassSubscribe(){return[]}_checkSubscribed(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}return(0,a.__decorate)([(0,s.Cb)({attribute:!1})],t.prototype,"hass",void 0),t}},76948:function(e,t,i){i.d(t,{T:()=>o});var a=i(29740);const s=()=>i.e("1550").then(i.bind(i,40504)),o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"dialog-label-detail",dialogImport:s,dialogParams:t})}}};
//# sourceMappingURL=9204.df08c1be5403020f.js.map