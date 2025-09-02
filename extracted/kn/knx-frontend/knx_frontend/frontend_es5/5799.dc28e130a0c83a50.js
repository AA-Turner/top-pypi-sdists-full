"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5799"],{1893:function(e,t,a){a.d(t,{Q:function(){return o}});a(64455),a(6202);const o=e=>e.replace(/^_*(.)|_+(.)/g,((e,t,a)=>t?t.toUpperCase():" "+a.toUpperCase()))},20797:function(e,t,a){a.a(e,(async function(e,t){try{a(39710),a(26847),a(2394),a(81738),a(94814),a(22960),a(6989),a(87799),a(1455),a(56389),a(27530);var o=a(73742),i=a(59048),n=a(7616),s=a(29740),r=a(1893),l=a(8265),d=a(54693),h=(a(57264),a(3847),e([d]));d=(h.then?(await h)():h)[0];let p,c,u,v,_=e=>e;const b=[],m=e=>(0,i.dy)(p||(p=_`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    <span slot="headline">${0}</span>
    ${0}
  </ha-combo-box-item>
`),e.icon,e.title||e.path,e.title?(0,i.dy)(c||(c=_`<span slot="supporting-text">${0}</span>`),e.path):i.Ld),g=(e,t,a)=>{var o,i,n;return{path:`/${e}/${null!==(o=t.path)&&void 0!==o?o:a}`,icon:null!==(i=t.icon)&&void 0!==i?i:"mdi:view-compact",title:null!==(n=t.title)&&void 0!==n?n:t.path?(0,r.Q)(t.path):`${a}`}},y=(e,t)=>{var a;return{path:`/${t.url_path}`,icon:null!==(a=t.icon)&&void 0!==a?a:"mdi:view-dashboard",title:t.url_path===e.defaultPanel?e.localize("panel.states"):e.localize(`panel.${t.title}`)||t.title||(t.url_path?(0,r.Q)(t.url_path):"")}};class f extends i.oi{render(){return(0,i.dy)(u||(u=_`
      <ha-combo-box
        .hass=${0}
        item-value-path="path"
        item-label-path="path"
        .value=${0}
        allow-custom-value
        .filteredItems=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .renderer=${0}
        @opened-changed=${0}
        @value-changed=${0}
        @filter-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this._value,this.navigationItems,this.label,this.helper,this.disabled,this.required,m,this._openedChanged,this._valueChanged,this._filterChanged)}async _openedChanged(e){this._opened=e.detail.value,this._opened&&!this.navigationItemsLoaded&&this._loadNavigationItems()}async _loadNavigationItems(){this.navigationItemsLoaded=!0;const e=Object.entries(this.hass.panels).map((([e,t])=>Object.assign({id:e},t))),t=e.filter((e=>"lovelace"===e.component_name)),a=await Promise.all(t.map((e=>(0,l.Q2)(this.hass.connection,"lovelace"===e.url_path?null:e.url_path,!0).then((t=>[e.id,t])).catch((t=>[e.id,void 0]))))),o=new Map(a);this.navigationItems=[];for(const i of e){this.navigationItems.push(y(this.hass,i));const e=o.get(i.id);e&&"views"in e&&e.views.forEach(((e,t)=>this.navigationItems.push(g(i.url_path,e,t))))}this.comboBox.filteredItems=this.navigationItems}shouldUpdate(e){return!this._opened||e.has("_opened")}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,s.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}_filterChanged(e){const t=e.detail.value.toLowerCase();if(t.length>=2){const e=[];this.navigationItems.forEach((a=>{(a.path.toLowerCase().includes(t)||a.title.toLowerCase().includes(t))&&e.push(a)})),e.length>0?this.comboBox.filteredItems=e:this.comboBox.filteredItems=[]}else this.comboBox.filteredItems=this.navigationItems}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._opened=!1,this.navigationItemsLoaded=!1,this.navigationItems=b}}f.styles=(0,i.iv)(v||(v=_`
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
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)()],f.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],f.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],f.prototype,"helper",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],f.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],f.prototype,"required",void 0),(0,o.__decorate)([(0,n.SB)()],f.prototype,"_opened",void 0),(0,o.__decorate)([(0,n.IO)("ha-combo-box",!0)],f.prototype,"comboBox",void 0),f=(0,o.__decorate)([(0,n.Mo)("ha-navigation-picker")],f),t()}catch(p){t(p)}}))},53306:function(e,t,a){a.a(e,(async function(e,o){try{a.r(t),a.d(t,{HaNavigationSelector:function(){return c}});a(26847),a(27530);var i=a(73742),n=a(59048),s=a(7616),r=a(29740),l=a(20797),d=e([l]);l=(d.then?(await d)():d)[0];let h,p=e=>e;class c extends n.oi{render(){return(0,n.dy)(h||(h=p`
      <ha-navigation-picker
        .hass=${0}
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        .helper=${0}
        @value-changed=${0}
      ></ha-navigation-picker>
    `),this.hass,this.label,this.value,this.required,this.disabled,this.helper,this._valueChanged)}_valueChanged(e){(0,r.B)(this,"value-changed",{value:e.detail.value})}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}(0,i.__decorate)([(0,s.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,i.__decorate)([(0,s.Cb)({attribute:!1})],c.prototype,"selector",void 0),(0,i.__decorate)([(0,s.Cb)()],c.prototype,"value",void 0),(0,i.__decorate)([(0,s.Cb)()],c.prototype,"label",void 0),(0,i.__decorate)([(0,s.Cb)()],c.prototype,"helper",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],c.prototype,"disabled",void 0),(0,i.__decorate)([(0,s.Cb)({type:Boolean})],c.prototype,"required",void 0),c=(0,i.__decorate)([(0,s.Mo)("ha-selector-navigation")],c),o()}catch(h){o(h)}}))},8265:function(e,t,a){a.d(t,{Q2:function(){return o}});const o=(e,t,a)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:a})}}]);
//# sourceMappingURL=5799.dc28e130a0c83a50.js.map