export const __webpack_ids__=["5799"];export const __webpack_modules__={91391:function(e,t,a){var o=a(73742),i=a(59048),s=a(7616),l=a(29740);const r=e=>e.replace(/^_*(.)|_+(.)/g,((e,t,a)=>t?t.toUpperCase():" "+a.toUpperCase()));a(90256),a(57264),a(3847);const n=[],d=e=>i.dy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    <span slot="headline">${e.title||e.path}</span>
    ${e.title?i.dy`<span slot="supporting-text">${e.path}</span>`:i.Ld}
  </ha-combo-box-item>
`,h=(e,t,a)=>({path:`/${e}/${t.path??a}`,icon:t.icon??"mdi:view-compact",title:t.title??(t.path?r(t.path):`${a}`)}),p=(e,t)=>({path:`/${t.url_path}`,icon:t.icon??"mdi:view-dashboard",title:t.url_path===e.defaultPanel?e.localize("panel.states"):e.localize(`panel.${t.title}`)||t.title||(t.url_path?r(t.url_path):"")});class c extends i.oi{render(){return i.dy`
      <ha-combo-box
        .hass=${this.hass}
        item-value-path="path"
        item-label-path="path"
        .value=${this._value}
        allow-custom-value
        .filteredItems=${this.navigationItems}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .renderer=${d}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
        @filter-changed=${this._filterChanged}
      >
      </ha-combo-box>
    `}async _openedChanged(e){this._opened=e.detail.value,this._opened&&!this.navigationItemsLoaded&&this._loadNavigationItems()}async _loadNavigationItems(){this.navigationItemsLoaded=!0;const e=Object.entries(this.hass.panels).map((([e,t])=>({id:e,...t}))),t=e.filter((e=>"lovelace"===e.component_name)),a=await Promise.all(t.map((e=>{return(t=this.hass.connection,a="lovelace"===e.url_path?null:e.url_path,o=!0,t.sendMessagePromise({type:"lovelace/config",url_path:a,force:o})).then((t=>[e.id,t])).catch((t=>[e.id,void 0]));var t,a,o}))),o=new Map(a);this.navigationItems=[];for(const i of e){this.navigationItems.push(p(this.hass,i));const e=o.get(i.id);e&&"views"in e&&e.views.forEach(((e,t)=>this.navigationItems.push(h(i.url_path,e,t))))}this.comboBox.filteredItems=this.navigationItems}shouldUpdate(e){return!this._opened||e.has("_opened")}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,l.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}_filterChanged(e){const t=e.detail.value.toLowerCase();if(t.length>=2){const e=[];this.navigationItems.forEach((a=>{(a.path.toLowerCase().includes(t)||a.title.toLowerCase().includes(t))&&e.push(a)})),e.length>0?this.comboBox.filteredItems=e:this.comboBox.filteredItems=[]}else this.comboBox.filteredItems=this.navigationItems}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._opened=!1,this.navigationItemsLoaded=!1,this.navigationItems=n}}c.styles=i.iv`
    ha-icon,
    ha-svg-icon {
      color: var(--primary-text-color);
      position: relative;
      bottom: 0px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `,(0,o.__decorate)([(0,s.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)()],c.prototype,"label",void 0),(0,o.__decorate)([(0,s.Cb)()],c.prototype,"value",void 0),(0,o.__decorate)([(0,s.Cb)()],c.prototype,"helper",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],c.prototype,"required",void 0),(0,o.__decorate)([(0,s.SB)()],c.prototype,"_opened",void 0),(0,o.__decorate)([(0,s.IO)("ha-combo-box",!0)],c.prototype,"comboBox",void 0),c=(0,o.__decorate)([(0,s.Mo)("ha-navigation-picker")],c)},53306:function(e,t,a){a.r(t),a.d(t,{HaNavigationSelector:()=>r});var o=a(73742),i=a(59048),s=a(7616),l=a(29740);a(91391);class r extends i.oi{render(){return i.dy`
      <ha-navigation-picker
        .hass=${this.hass}
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        @value-changed=${this._valueChanged}
      ></ha-navigation-picker>
    `}_valueChanged(e){(0,l.B)(this,"value-changed",{value:e.detail.value})}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}(0,o.__decorate)([(0,s.Cb)({attribute:!1})],r.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],r.prototype,"selector",void 0),(0,o.__decorate)([(0,s.Cb)()],r.prototype,"value",void 0),(0,o.__decorate)([(0,s.Cb)()],r.prototype,"label",void 0),(0,o.__decorate)([(0,s.Cb)()],r.prototype,"helper",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],r.prototype,"disabled",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],r.prototype,"required",void 0),r=(0,o.__decorate)([(0,s.Mo)("ha-selector-navigation")],r)}};
//# sourceMappingURL=5799.10ab3fcfb1a5ad34.js.map