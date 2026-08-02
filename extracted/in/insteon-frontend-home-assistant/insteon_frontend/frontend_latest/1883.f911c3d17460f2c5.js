/*! For license information please see 1883.f911c3d17460f2c5.js.LICENSE.txt */
export const __webpack_id__="1883";export const __webpack_ids__=["1883"];export const __webpack_modules__={26537:function(e,t,i){i.d(t,{Si:()=>r});var s=i(62826),a=i(96196),o=i(77845);i(22598),i(60961);const r=e=>{switch(e.level){case 0:return"M11,10H13V16H11V10M22,12H19V20H5V12H2L12,3L22,12M15,10A2,2 0 0,0 13,8H11A2,2 0 0,0 9,10V16A2,2 0 0,0 11,18H13A2,2 0 0,0 15,16V10Z";case 1:return"M12,3L2,12H5V20H19V12H22L12,3M10,8H14V18H12V10H10V8Z";case 2:return"M12,3L2,12H5V20H19V12H22L12,3M9,8H13A2,2 0 0,1 15,10V12A2,2 0 0,1 13,14H11V16H15V18H9V14A2,2 0 0,1 11,12H13V10H9V8Z";case 3:return"M12,3L22,12H19V20H5V12H2L12,3M15,11.5V10C15,8.89 14.1,8 13,8H9V10H13V12H11V14H13V16H9V18H13A2,2 0 0,0 15,16V14.5A1.5,1.5 0 0,0 13.5,13A1.5,1.5 0 0,0 15,11.5Z";case-1:return"M12,3L2,12H5V20H19V12H22L12,3M11,15H7V13H11V15M15,18H13V10H11V8H15V18Z"}return"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"};class n extends a.WF{render(){if(!this.floor)return a.s6;if(this.floor.icon)return a.qy`<ha-icon .icon=${this.floor.icon}></ha-icon>`;const e=r(this.floor);return a.qy`<ha-svg-icon .path=${e}></ha-svg-icon>`}}(0,s.__decorate)([(0,o.MZ)({attribute:!1})],n.prototype,"floor",void 0),(0,s.__decorate)([(0,o.MZ)()],n.prototype,"icon",void 0),n=(0,s.__decorate)([(0,o.EM)("ha-floor-icon")],n)},76894:function(e,t,i){i.a(e,async function(e,t){try{var s=i(62826),a=i(96196),o=i(77845),r=i(22786),n=i(92542),l=i(41144),h=i(47644),d=i(54110),c=i(74839),p=i(53083),u=i(10234),_=i(379),y=(i(94343),i(26537),i(96943)),m=(i(60733),i(60961),e([y]));y=(m.then?(await m)():m)[0];const v="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",g="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z",f="___ADD_NEW___";class b extends a.WF{async open(){await this.updateComplete,await(this._picker?.open())}render(){const e=this.placeholder??this.hass.localize("ui.components.floor-picker.floor"),t=this._computeValueRenderer(this.hass.floors);return a.qy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .label=${this.label}
        .notFoundLabel=${this._notFoundLabel}
        .emptyLabel=${this.hass.localize("ui.components.floor-picker.no_floors")}
        .placeholder=${e}
        .value=${this.value}
        .getItems=${this._getItems}
        .getAdditionalItems=${this._getAdditionalItems}
        .valueRenderer=${t}
        .rowRenderer=${this._rowRenderer}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}_valueChanged(e){e.stopPropagation();const t=e.detail.value;if(t){if(t.startsWith(f)){this.hass.loadFragmentTranslation("config");const e=t.substring(f.length);return void(0,_.k)(this,{suggestedName:e,createEntry:async(e,t)=>{try{const i=await(0,p.KD)(this.hass,e);t.forEach(e=>{(0,d.gs)(this.hass,e,{floor_id:i.floor_id})}),this._setValue(i.floor_id)}catch(i){(0,u.K$)(this,{title:this.hass.localize("ui.components.floor-picker.failed_create_floor"),text:i.message})}}})}this._setValue(t)}else this._setValue(void 0)}_setValue(e){this.value=e,(0,n.r)(this,"value-changed",{value:e}),(0,n.r)(this,"change")}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1,this._computeValueRenderer=(0,r.A)(e=>e=>{const t=this.hass.floors[e];if(!t)return a.qy`
            <ha-svg-icon slot="start" .path=${g}></ha-svg-icon>
            <span slot="headline">${t}</span>
          `;const i=t?(0,h.X)(t):void 0;return a.qy`
          <ha-floor-icon slot="start" .floor=${t}></ha-floor-icon>
          <span slot="headline">${i}</span>
        `}),this._getFloors=(0,r.A)((e,t,i,s,a,o,r,n,d,u)=>{const _=Object.values(e),y=Object.values(t),m=Object.values(i),v=Object.values(s);let g,f,b={};(a||o||r||n||d)&&(b=(0,c.g2)(v),g=m,f=v.filter(e=>e.area_id),a&&(g=g.filter(e=>{const t=b[e.id];return!(!t||!t.length)&&b[e.id].some(e=>a.includes((0,l.m)(e.entity_id)))}),f=f.filter(e=>a.includes((0,l.m)(e.entity_id)))),o&&(g=g.filter(e=>{const t=b[e.id];return!t||!t.length||v.every(e=>!o.includes((0,l.m)(e.entity_id)))}),f=f.filter(e=>!o.includes((0,l.m)(e.entity_id)))),r&&(g=g.filter(e=>{const t=b[e.id];return!(!t||!t.length)&&b[e.id].some(e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&r.includes(t.attributes.device_class))})}),f=f.filter(e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&r.includes(t.attributes.device_class)})),n&&(g=g.filter(e=>n(e))),d&&(g=g.filter(e=>{const t=b[e.id];return!(!t||!t.length)&&b[e.id].some(e=>{const t=this.hass.states[e.entity_id];return!!t&&d(t)})}),f=f.filter(e=>{const t=this.hass.states[e.entity_id];return!!t&&d(t)})));let w,$=_;if(g&&(w=g.filter(e=>e.area_id).map(e=>e.area_id)),f&&(w=(w??[]).concat(f.filter(e=>e.area_id).map(e=>e.area_id))),w){const e=(0,p._o)(y);$=$.filter(t=>e[t.floor_id]?.some(e=>w.includes(e.area_id)))}u&&($=$.filter(e=>!u.includes(e.floor_id)));return $.map(e=>{const t=(0,h.X)(e);return{id:e.floor_id,primary:t,floor:e,sorting_label:e.level?.toString()||"zzzzz",search_labels:[t,e.floor_id,...e.aliases].filter(e=>Boolean(e))}})}),this._rowRenderer=e=>a.qy`
    <ha-combo-box-item type="button" compact>
      ${e.icon_path?a.qy`
            <ha-svg-icon
              slot="start"
              style="margin: 0 4px"
              .path=${e.icon_path}
            ></ha-svg-icon>
          `:a.qy`
            <ha-floor-icon
              slot="start"
              .floor=${e.floor}
              style="margin: 0 4px"
            ></ha-floor-icon>
          `}
      <span slot="headline">${e.primary}</span>
    </ha-combo-box-item>
  `,this._getItems=()=>this._getFloors(this.hass.floors,this.hass.areas,this.hass.devices,this.hass.entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeFloors),this._allFloorNames=(0,r.A)(e=>Object.values(e).map(e=>(0,h.X)(e)?.toLowerCase()).filter(Boolean)),this._getAdditionalItems=e=>{if(this.noAdd)return[];const t=this._allFloorNames(this.hass.floors);return e&&!t.includes(e.toLowerCase())?[{id:f+e,primary:this.hass.localize("ui.components.floor-picker.add_new_sugestion",{name:e}),icon_path:v}]:[{id:f,primary:this.hass.localize("ui.components.floor-picker.add_new"),icon_path:v}]},this._notFoundLabel=e=>this.hass.localize("ui.components.floor-picker.no_match",{term:a.qy`<b>‘${e}’</b>`})}}(0,s.__decorate)([(0,o.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,s.__decorate)([(0,o.MZ)()],b.prototype,"label",void 0),(0,s.__decorate)([(0,o.MZ)()],b.prototype,"value",void 0),(0,s.__decorate)([(0,o.MZ)()],b.prototype,"helper",void 0),(0,s.__decorate)([(0,o.MZ)()],b.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.MZ)({type:Boolean,attribute:"no-add"})],b.prototype,"noAdd",void 0),(0,s.__decorate)([(0,o.MZ)({type:Array,attribute:"include-domains"})],b.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,o.MZ)({type:Array,attribute:"exclude-domains"})],b.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,o.MZ)({type:Array,attribute:"include-device-classes"})],b.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,o.MZ)({type:Array,attribute:"exclude-floors"})],b.prototype,"excludeFloors",void 0),(0,s.__decorate)([(0,o.MZ)({attribute:!1})],b.prototype,"deviceFilter",void 0),(0,s.__decorate)([(0,o.MZ)({attribute:!1})],b.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,o.MZ)({type:Boolean})],b.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.MZ)({type:Boolean})],b.prototype,"required",void 0),(0,s.__decorate)([(0,o.P)("ha-generic-picker")],b.prototype,"_picker",void 0),b=(0,s.__decorate)([(0,o.EM)("ha-floor-picker")],b),t()}catch(v){t(v)}})},53083:function(e,t,i){i.d(t,{KD:()=>s,_o:()=>a});const s=(e,t)=>e.callWS({type:"config/floor_registry/create",...t}),a=e=>{const t={};for(const i of e)i.floor_id&&(i.floor_id in t||(t[i.floor_id]=[]),t[i.floor_id].push(i));return t}},71437:function(e,t,i){i.d(t,{Sn:()=>s,q2:()=>a,tb:()=>o});const s="timestamp",a="temperature",o="humidity"},76218:function(e,t,i){i.a(e,async function(e,s){try{i.r(t);var a=i(62826),o=i(96196),r=i(77845),n=i(92542),l=i(82965),h=(i(17963),i(45783)),d=i(95637),c=i(76894),p=(i(88867),i(32649)),u=i(41881),_=(i(2809),i(78740),i(54110)),y=i(71437),m=i(10234),v=i(39396),g=e([l,h,c,p,u]);[l,h,c,p,u]=g.then?(await g)():g;const f={round:!1,type:"image/jpeg",quality:.75},b=["sensor"],w=[y.q2],$=[y.tb];class C extends o.WF{async showDialog(e){this._params=e,this._error=void 0,this._params.entry?(this._name=this._params.entry.name,this._aliases=this._params.entry.aliases,this._labels=this._params.entry.labels,this._picture=this._params.entry.picture,this._icon=this._params.entry.icon,this._floor=this._params.entry.floor_id,this._temperatureEntity=this._params.entry.temperature_entity_id,this._humidityEntity=this._params.entry.humidity_entity_id):(this._name=this._params.suggestedName||"",this._aliases=[],this._labels=[],this._picture=null,this._icon=null,this._floor=null,this._temperatureEntity=null,this._humidityEntity=null),await this.updateComplete}closeDialog(){this._error="",this._params=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}_renderSettings(e){return o.qy`
      ${e?o.qy`
            <ha-settings-row>
              <span slot="heading">
                ${this.hass.localize("ui.panel.config.areas.editor.area_id")}
              </span>
              <span slot="description"> ${e.area_id} </span>
            </ha-settings-row>
          `:o.s6}

      <ha-textfield
        .value=${this._name}
        @input=${this._nameChanged}
        .label=${this.hass.localize("ui.panel.config.areas.editor.name")}
        .validationMessage=${this.hass.localize("ui.panel.config.areas.editor.name_required")}
        required
        dialogInitialFocus
      ></ha-textfield>

      <ha-icon-picker
        .hass=${this.hass}
        .value=${this._icon}
        @value-changed=${this._iconChanged}
        .label=${this.hass.localize("ui.panel.config.areas.editor.icon")}
      ></ha-icon-picker>

      <ha-floor-picker
        .hass=${this.hass}
        .value=${this._floor}
        @value-changed=${this._floorChanged}
        .label=${this.hass.localize("ui.panel.config.areas.editor.floor")}
      ></ha-floor-picker>

      <ha-labels-picker
        .label=${this.hass.localize("ui.components.label-picker.labels")}
        .hass=${this.hass}
        .value=${this._labels}
        @value-changed=${this._labelsChanged}
        .placeholder=${this.hass.localize("ui.panel.config.areas.editor.add_labels")}
      ></ha-labels-picker>

      <ha-picture-upload
        .hass=${this.hass}
        .value=${this._picture}
        crop
        select-media
        .cropOptions=${f}
        @change=${this._pictureChanged}
      ></ha-picture-upload>
    `}_renderAliasExpansion(){return o.qy`
      <ha-expansion-panel
        outlined
        .header=${this.hass.localize("ui.panel.config.areas.editor.aliases_section")}
        expanded
      >
        <div class="content">
          <p class="description">
            ${this.hass.localize("ui.panel.config.areas.editor.aliases_description")}
          </p>
          <ha-aliases-editor
            .hass=${this.hass}
            .aliases=${this._aliases}
            @value-changed=${this._aliasesChanged}
          ></ha-aliases-editor>
        </div>
      </ha-expansion-panel>
    `}_renderRelatedEntitiesExpansion(){return o.qy`
      <ha-expansion-panel
        outlined
        .header=${this.hass.localize("ui.panel.config.areas.editor.related_entities_section")}
        expanded
      >
        <div class="content">
          <ha-entity-picker
            .hass=${this.hass}
            .label=${this.hass.localize("ui.panel.config.areas.editor.temperature_entity")}
            .helper=${this.hass.localize("ui.panel.config.areas.editor.temperature_entity_description")}
            .value=${this._temperatureEntity}
            .includeDomains=${b}
            .includeDeviceClasses=${w}
            .entityFilter=${this._areaEntityFilter}
            @value-changed=${this._sensorChanged}
          ></ha-entity-picker>

          <ha-entity-picker
            .hass=${this.hass}
            .label=${this.hass.localize("ui.panel.config.areas.editor.humidity_entity")}
            .helper=${this.hass.localize("ui.panel.config.areas.editor.humidity_entity_description")}
            .value=${this._humidityEntity}
            .includeDomains=${b}
            .includeDeviceClasses=${$}
            .entityFilter=${this._areaEntityFilter}
            @value-changed=${this._sensorChanged}
          ></ha-entity-picker>
        </div>
      </ha-expansion-panel>
    `}render(){if(!this._params)return o.s6;const e=this._params.entry,t=!this._isNameValid(),i=!e;return o.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,d.l)(this.hass,e?this.hass.localize("ui.panel.config.areas.editor.update_area"):this.hass.localize("ui.panel.config.areas.editor.create_area"))}
      >
        <div>
          ${this._error?o.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            ${this._renderSettings(e)} ${this._renderAliasExpansion()}
            ${i?o.s6:this._renderRelatedEntitiesExpansion()}
          </div>
        </div>
        ${i?o.s6:o.qy`<ha-button
              slot="secondaryAction"
              variant="danger"
              appearance="plain"
              @click=${this._deleteArea}
            >
              ${this.hass.localize("ui.common.delete")}
            </ha-button>`}
        <ha-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${t||!!this._submitting}
        >
          ${e?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.create")}
        </ha-button>
      </ha-dialog>
    `}_isNameValid(){return""!==this._name.trim()}_nameChanged(e){this._error=void 0,this._name=e.target.value}_floorChanged(e){this._error=void 0,this._floor=e.detail.value}_iconChanged(e){this._error=void 0,this._icon=e.detail.value}_labelsChanged(e){this._error=void 0,this._labels=e.detail.value}_pictureChanged(e){this._error=void 0,this._picture=e.target.value}_aliasesChanged(e){this._aliases=e.detail.value}_sensorChanged(e){this[`_${e.target.includeDeviceClasses[0]}Entity`]=e.detail.value||null}async _updateEntry(){const e=!this._params.entry;this._submitting=!0;try{const t={name:this._name.trim(),picture:this._picture||(e?void 0:null),icon:this._icon||(e?void 0:null),floor_id:this._floor||(e?void 0:null),labels:this._labels||null,aliases:this._aliases,temperature_entity_id:this._temperatureEntity,humidity_entity_id:this._humidityEntity};e?await this._params.createEntry(t):await this._params.updateEntry(t),this.closeDialog()}catch(t){this._error=t.message||this.hass.localize("ui.panel.config.areas.editor.unknown_error")}finally{this._submitting=!1}}async _deleteArea(){if(!this._params?.entry)return;await(0,m.dk)(this,{title:this.hass.localize("ui.panel.config.areas.delete.confirmation_title",{name:this._params.entry.name}),text:this.hass.localize("ui.panel.config.areas.delete.confirmation_text"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0})&&(await(0,_.uG)(this.hass,this._params.entry.area_id),this.closeDialog())}static get styles(){return[v.nA,o.AH`
        ha-textfield {
          display: block;
        }
        ha-expansion-panel {
          --expansion-panel-content-padding: 0;
        }
        ha-aliases-editor,
        ha-entity-picker,
        ha-floor-picker,
        ha-icon-picker,
        ha-labels-picker,
        ha-picture-upload,
        ha-expansion-panel {
          display: block;
          margin-bottom: 16px;
        }
        ha-dialog {
          --mdc-dialog-min-width: min(600px, 100vw);
        }
        .content {
          padding: 12px;
        }
        .description {
          margin: 0 0 16px 0;
        }
      `]}constructor(...e){super(...e),this._areaEntityFilter=e=>{const t=this.hass.entities[e.entity_id];if(!t)return!1;const i=this._params.entry.area_id;if(t.area_id===i)return!0;if(!t.device_id)return!1;const s=this.hass.devices[t.device_id];return s&&s.area_id===i}}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],C.prototype,"hass",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_name",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_aliases",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_labels",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_picture",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_icon",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_floor",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_temperatureEntity",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_humidityEntity",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_error",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_params",void 0),(0,a.__decorate)([(0,r.wk)()],C.prototype,"_submitting",void 0),customElements.define("dialog-area-registry-detail",C),s()}catch(f){s(f)}})},379:function(e,t,i){i.d(t,{k:()=>o});var s=i(92542);const a=()=>Promise.all([i.e("9291"),i.e("3785"),i.e("5989"),i.e("274"),i.e("4363"),i.e("2542")]).then(i.bind(i,96573)),o=(e,t)=>{(0,s.r)(e,"show-dialog",{dialogTag:"dialog-floor-registry-detail",dialogImport:a,dialogParams:t})}},61171:function(e,t,i){i.d(t,{A:()=>s});const s=i(96196).AH`:host {
  --max-width: 30ch;
  display: inline-block;
  position: absolute;
  color: var(--wa-tooltip-content-color);
  font-size: var(--wa-tooltip-font-size);
  line-height: var(--wa-tooltip-line-height);
  text-align: start;
  white-space: normal;
}
.tooltip {
  --arrow-size: var(--wa-tooltip-arrow-size);
  --arrow-color: var(--wa-tooltip-background-color);
}
.tooltip::part(popup) {
  z-index: 1000;
}
.tooltip[placement^=top]::part(popup) {
  transform-origin: bottom;
}
.tooltip[placement^=bottom]::part(popup) {
  transform-origin: top;
}
.tooltip[placement^=left]::part(popup) {
  transform-origin: right;
}
.tooltip[placement^=right]::part(popup) {
  transform-origin: left;
}
.body {
  display: block;
  width: max-content;
  max-width: var(--max-width);
  border-radius: var(--wa-tooltip-border-radius);
  background-color: var(--wa-tooltip-background-color);
  border: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
  padding: 0.25em 0.5em;
  user-select: none;
  -webkit-user-select: none;
}
.tooltip::part(arrow) {
  border-bottom: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
  border-right: var(--wa-tooltip-border-width) var(--wa-tooltip-border-style) var(--wa-tooltip-border-color);
}
`},52630:function(e,t,i){i.a(e,async function(e,s){try{i.d(t,{A:()=>$});var a=i(96196),o=i(77845),r=i(94333),n=i(17051),l=i(42462),h=i(28438),d=i(98779),c=i(27259),p=i(984),u=i(53720),_=i(9395),y=i(32510),m=i(40158),v=i(61171),g=e([m]);m=(g.then?(await g)():g)[0];var f=Object.defineProperty,b=Object.getOwnPropertyDescriptor,w=(e,t,i,s)=>{for(var a,o=s>1?void 0:s?b(t,i):t,r=e.length-1;r>=0;r--)(a=e[r])&&(o=(s?a(t,i,o):a(o))||o);return s&&o&&f(t,i,o),o};let $=class extends y.A{connectedCallback(){super.connectedCallback(),this.eventController.signal.aborted&&(this.eventController=new AbortController),this.open&&(this.open=!1,this.updateComplete.then(()=>{this.open=!0})),this.id||(this.id=(0,u.N)("wa-tooltip-")),this.for&&this.anchor?(this.anchor=null,this.handleForChange()):this.for&&this.handleForChange()}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("keydown",this.handleDocumentKeyDown),this.eventController.abort(),this.anchor&&this.removeFromAriaLabelledBy(this.anchor,this.id)}firstUpdated(){this.body.hidden=!this.open,this.open&&(this.popup.active=!0,this.popup.reposition())}hasTrigger(e){return this.trigger.split(" ").includes(e)}addToAriaLabelledBy(e,t){const i=(e.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean);i.includes(t)||(i.push(t),e.setAttribute("aria-labelledby",i.join(" ")))}removeFromAriaLabelledBy(e,t){const i=(e.getAttribute("aria-labelledby")||"").split(/\s+/).filter(Boolean).filter(e=>e!==t);i.length>0?e.setAttribute("aria-labelledby",i.join(" ")):e.removeAttribute("aria-labelledby")}async handleOpenChange(){if(this.open){if(this.disabled)return;const e=new d.k;if(this.dispatchEvent(e),e.defaultPrevented)return void(this.open=!1);document.addEventListener("keydown",this.handleDocumentKeyDown,{signal:this.eventController.signal}),this.body.hidden=!1,this.popup.active=!0,await(0,c.Ud)(this.popup.popup,"show-with-scale"),this.popup.reposition(),this.dispatchEvent(new l.q)}else{const e=new h.L;if(this.dispatchEvent(e),e.defaultPrevented)return void(this.open=!1);document.removeEventListener("keydown",this.handleDocumentKeyDown),await(0,c.Ud)(this.popup.popup,"hide-with-scale"),this.popup.active=!1,this.body.hidden=!0,this.dispatchEvent(new n.Z)}}handleForChange(){const e=this.getRootNode();if(!e)return;const t=this.for?e.getElementById(this.for):null,i=this.anchor;if(t===i)return;const{signal:s}=this.eventController;t&&(this.addToAriaLabelledBy(t,this.id),t.addEventListener("blur",this.handleBlur,{capture:!0,signal:s}),t.addEventListener("focus",this.handleFocus,{capture:!0,signal:s}),t.addEventListener("click",this.handleClick,{signal:s}),t.addEventListener("mouseover",this.handleMouseOver,{signal:s}),t.addEventListener("mouseout",this.handleMouseOut,{signal:s})),i&&(this.removeFromAriaLabelledBy(i,this.id),i.removeEventListener("blur",this.handleBlur,{capture:!0}),i.removeEventListener("focus",this.handleFocus,{capture:!0}),i.removeEventListener("click",this.handleClick),i.removeEventListener("mouseover",this.handleMouseOver),i.removeEventListener("mouseout",this.handleMouseOut)),this.anchor=t}async handleOptionsChange(){this.hasUpdated&&(await this.updateComplete,this.popup.reposition())}handleDisabledChange(){this.disabled&&this.open&&this.hide()}async show(){if(!this.open)return this.open=!0,(0,p.l)(this,"wa-after-show")}async hide(){if(this.open)return this.open=!1,(0,p.l)(this,"wa-after-hide")}render(){return a.qy`
      <wa-popup
        part="base"
        exportparts="
          popup:base__popup,
          arrow:base__arrow
        "
        class=${(0,r.H)({tooltip:!0,"tooltip-open":this.open})}
        placement=${this.placement}
        distance=${this.distance}
        skidding=${this.skidding}
        flip
        shift
        ?arrow=${!this.withoutArrow}
        hover-bridge
        .anchor=${this.anchor}
      >
        <div part="body" class="body">
          <slot></slot>
        </div>
      </wa-popup>
    `}constructor(){super(...arguments),this.placement="top",this.disabled=!1,this.distance=8,this.open=!1,this.skidding=0,this.showDelay=150,this.hideDelay=0,this.trigger="hover focus",this.withoutArrow=!1,this.for=null,this.anchor=null,this.eventController=new AbortController,this.handleBlur=()=>{this.hasTrigger("focus")&&this.hide()},this.handleClick=()=>{this.hasTrigger("click")&&(this.open?this.hide():this.show())},this.handleFocus=()=>{this.hasTrigger("focus")&&this.show()},this.handleDocumentKeyDown=e=>{"Escape"===e.key&&(e.stopPropagation(),this.hide())},this.handleMouseOver=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.show(),this.showDelay))},this.handleMouseOut=()=>{this.hasTrigger("hover")&&(clearTimeout(this.hoverTimeout),this.hoverTimeout=window.setTimeout(()=>this.hide(),this.hideDelay))}}};$.css=v.A,$.dependencies={"wa-popup":m.A},w([(0,o.P)("slot:not([name])")],$.prototype,"defaultSlot",2),w([(0,o.P)(".body")],$.prototype,"body",2),w([(0,o.P)("wa-popup")],$.prototype,"popup",2),w([(0,o.MZ)()],$.prototype,"placement",2),w([(0,o.MZ)({type:Boolean,reflect:!0})],$.prototype,"disabled",2),w([(0,o.MZ)({type:Number})],$.prototype,"distance",2),w([(0,o.MZ)({type:Boolean,reflect:!0})],$.prototype,"open",2),w([(0,o.MZ)({type:Number})],$.prototype,"skidding",2),w([(0,o.MZ)({attribute:"show-delay",type:Number})],$.prototype,"showDelay",2),w([(0,o.MZ)({attribute:"hide-delay",type:Number})],$.prototype,"hideDelay",2),w([(0,o.MZ)()],$.prototype,"trigger",2),w([(0,o.MZ)({attribute:"without-arrow",type:Boolean,reflect:!0})],$.prototype,"withoutArrow",2),w([(0,o.MZ)()],$.prototype,"for",2),w([(0,o.wk)()],$.prototype,"anchor",2),w([(0,_.w)("open",{waitUntilFirstUpdate:!0})],$.prototype,"handleOpenChange",1),w([(0,_.w)("for")],$.prototype,"handleForChange",1),w([(0,_.w)(["distance","placement","skidding"])],$.prototype,"handleOptionsChange",1),w([(0,_.w)("disabled")],$.prototype,"handleDisabledChange",1),$=w([(0,o.EM)("wa-tooltip")],$),s()}catch($){s($)}})},3890:function(e,t,i){i.d(t,{T:()=>p});var s=i(5055),a=i(63937),o=i(37540);class r{disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}constructor(e){this.G=e}}class n{get(){return this.Y}pause(){this.Y??=new Promise(e=>this.Z=e)}resume(){this.Z?.(),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var l=i(42017);const h=e=>!(0,a.sO)(e)&&"function"==typeof e.then,d=1073741823;class c extends o.Kq{render(...e){return e.find(e=>!h(e))??s.c0}update(e,t){const i=this._$Cbt;let a=i.length;this._$Cbt=t;const o=this._$CK,r=this._$CX;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$Cwt);s++){const e=t[s];if(!h(e))return this._$Cwt=s,e;s<a&&e===i[s]||(this._$Cwt=d,a=0,Promise.resolve(e).then(async t=>{for(;r.get();)await r.get();const i=o.deref();if(void 0!==i){const s=i._$Cbt.indexOf(e);s>-1&&s<i._$Cwt&&(i._$Cwt=s,i.setValue(t))}}))}return s.c0}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=d,this._$Cbt=[],this._$CK=new r(this),this._$CX=new n}}const p=(0,l.u$)(c)}};
//# sourceMappingURL=1883.f911c3d17460f2c5.js.map